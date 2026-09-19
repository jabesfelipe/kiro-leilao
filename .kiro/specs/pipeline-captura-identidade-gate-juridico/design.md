# Design Document

Pipeline de Entrada: Captura, Identidade e Gate Jurídico

## Overview

Este design descreve a fatia de entrada do pipeline de análise: da captura bruta de
uma oferta até a liberação (ou bloqueio) pelo gate de validade jurídica, entregando
uma decisão explicável e persistida como snapshot.

A escolha arquitetural central é a **separação estrita entre orquestração e decisão**:
o LangGraph coordena o fluxo e carrega estado, mas toda regra de negócio e todo
cálculo vivem em motores determinísticos puros. Nenhum componente com LLM decide,
cria evidência ou converte desconhecido em confirmado.

Parte do código desta fatia já existe no repositório (`capture/`, `pipeline/`,
`orchestration/graph.py`) mas **nunca foi executado nem testado**. Este design
formaliza as decisões embutidas nele e trata a verificação como trabalho pendente.

### Princípios que governam o design

| Princípio | Consequência técnica |
|-----------|----------------------|
| Desconhecido ≠ zero | Todo campo opcional é `None`; nunca default numérico |
| Evidência tem proveniência | `Evidence` exige fonte, local, estado, autor e data |
| BLOCK não é compensável | Gate roda antes da economia; decisão respeita precedência |
| Nada é destrutivo | Captura imutável; análise versionada por snapshot |
| Determinismo no núcleo | Motores são funções puras, testáveis sem I/O |

## Architecture

### Fluxo de alto nível

```
RawCapture (payload bruto + hash)
      │
      ▼
[normalizar]  ──> NormalizedListing (campos ausentes = None)
      │
      ▼
[identidade]  ──> IdentityResult (I0..I4 + identificadores)
      │
      ▼
[validade_juridica] ──> LegalGateResult (OK | PENDENTE | BLOCK)
      │
      ├── BLOCK ou identidade < I2 ──────────────┐
      │                                          │
      ▼                                          ▼
[economia] ──> TCO, desconto líquido, margem  [decisao]
      │                                          │
      └──────────────────────────────────────────┤
                                                 ▼
                                          [explicacao] ──> END
```

A ordem não é convenção: é imposta pela topologia do grafo. Não existe caminho que
alcance `economia` sem passar por `validade_juridica`.

### Camadas e responsabilidades

```
src/radar/
├── capture/          # entrada: preserva e normaliza (sem decidir)
│   ├── schemas.py    # RawCapture, NormalizedListing
│   ├── parsing.py    # parsers pt-BR tolerantes
│   └── caixa.py      # normalizador da fonte CAIXA
├── pipeline/         # etapas de avaliação (determinísticas)
│   ├── identity.py   # níveis I0–I4, deduplicação
│   └── legal_gate.py # gate P0 (GATE-JUR-001..007)
├── engines/          # motores puros já existentes
│   ├── calculation.py
│   └── decision.py
├── orchestration/
│   └── graph.py      # nós LangGraph + estado compartilhado
└── db/               # persistência (snapshot imutável)
    ├── models.py
    └── repository.py
```

Regra de dependência: `capture` e `pipeline` não conhecem `db` nem `orchestration`.
O grafo depende de todos; ninguém depende do grafo. Isso mantém os motores testáveis
sem banco e sem LangGraph.

## Components and Interfaces

### 1. Captura e normalização

**`RawCapture`** preserva o payload como veio e deriva o fingerprint:

```python
class RawCapture(BaseModel):
    source_type: str          # caixa | leiloeiro | portal | cartorio
    source_name: str
    payload: dict[str, Any]   # bruto, imutável
    captured_at: datetime

    @property
    def fingerprint(self) -> str  # sha256 do JSON com chaves ordenadas
```

Decisão: o fingerprint usa `json.dumps(sort_keys=True)`, garantindo hash estável
independente da ordem das chaves (Requisito 1.2). Serve como chave natural de
deduplicação de captura (`UNIQUE (source_id, hash)` no banco).

**`NormalizedListing`** é a visão estruturada. Todo campo é opcional; `missing_fields()`
expõe as ausências relevantes que alimentam pendências.

**Normalizador da CAIXA** resolve rótulos por dicionário de aliases, comparando chaves
normalizadas (minúsculas, sem underscore). Isso absorve variação de rótulo da fonte
sem quebrar.

**Parsers pt-BR** (`parsing.py`) — todos retornam `None` quando não conseguem afirmar:

| Parser | Entrada | Saída |
|--------|---------|-------|
| `parse_money` | `"R$ 191.651,31"` | `191651.31` |
| `parse_area` | `"47,76 m²"` | `47.76` |
| `parse_percent` | `"5%"`, `5`, `0.05` | `0.05` |
| `parse_datetime` | `"15/09/2026 10:00"` | `datetime(2026,9,15,10,0)` |
| `parse_occupancy` | `"Desocupado"` | `False` |

Armadilha tratada explicitamente: `"desocupado"` contém a substring `"ocupado"`. O
parser testa os termos de vacância **antes** dos de ocupação, senão inverteria o
sentido — erro que classificaria imóvel livre como ocupado e distorceria o risco.

Decisão sobre `parse_percent`: valores `> 1` são interpretados como percentual
(`5` → `0.05`) e `≤ 1` como fração já normalizada (`0.05` → `0.05`). É heurística,
aceitável porque nenhuma comissão ou alíquota real do domínio ultrapassa 100%.

### 2. Identidade e deduplicação

```python
class IdentityLevel(IntEnum):
    I0_INDEFINIDA = 0   # confiança  0
    I1_FRACA      = 1   # confiança 35
    I2_PROVAVEL   = 2   # confiança 60
    I3_FORTE      = 3   # confiança 85
    I4_PLENA      = 4   # confiança 95
```

Classificação:

| Condição | Nível |
|----------|-------|
| Matrícula + (comarca ou cartório) | I4 |
| Matrícula isolada, ou id da fonte + endereço completo | I3 |
| Endereço completo + área | I2 |
| Apenas endereço ou apenas id da fonte | I1 |
| Nada disso | I0 |

`resolve_identity` devolve também os identificadores encontrados com confiança
individual (matrícula 95, id da fonte 85, endereço 60), que alimentam
`property_identifiers`.

**Deduplicação** (`is_same_property`) retorna `tuple[bool | None, str]` — o `None` é
deliberado: significa "não afirmável", distinto de "não é o mesmo". Hierarquia:

1. Ambas com matrícula → decisivo (iguais = mesmo; distintas = diferentes)
2. Mesmo identificador da fonte → mesmo imóvel (evidência forte)
3. Endereço igual + área compatível (tolerância 1 m²) → mesmo imóvel (provável)
4. Endereço igual + área divergente/ausente → `None`
5. Caso contrário → `None`

Preço não aparece em nenhum ramo. É proibição de projeto, não omissão: dois imóveis
distintos podem ter o mesmo lance mínimo, e usar preço produziria fusão indevida de
imóveis — erro que contaminaria todo o histórico.

### 3. Gate de validade jurídica (camada P0)

Modelado como catálogo de verificações avaliadas uniformemente:

```python
class CheckOutcome(str, Enum):
    CONFIRMED       # comprovado documentalmente
    IRREGULAR       # irregularidade material -> BLOCK
    UNKNOWN         # sem evidência -> PENDENTE
    NOT_APPLICABLE
```

| Código | Verificação |
|--------|-------------|
| GATE-JUR-001 | Consolidação da propriedade comprovada na matrícula |
| GATE-JUR-002 | Matrícula atualizada e consistente com o edital |
| GATE-JUR-003 | Constituição em mora comprovada |
| GATE-JUR-004 | Intimação/notificação para purgação da mora comprovada |
| GATE-JUR-005 | Cronologia coerente: mora → consolidação → leilão |
| GATE-JUR-006 | Processos judiciais sem impacto na validade |
| GATE-JUR-007 | Dados do certame sem divergência (data/hora/plataforma/valor) |

GATE-JUR-007 não vem da documentação original: foi derivado do caso real do item 227,
em que a data da sessão divergia entre o PDF do edital (15/09) e o portal (29/09), e
o Método Jabes determinou pausar. Sem esse gate, o sistema aceitaria silenciosamente
uma data errada.

**Agregação do resultado** — ordem importa:

```
qualquer IRREGULAR        -> BLOCK
senão qualquer UNKNOWN    -> PENDENTE
senão                     -> OK
```

`LegalGateInput.outcome()` retorna `UNKNOWN` para código não informado. Esse default
é a tradução direta de "ausência de evidência não é regularidade" (Requisito 5.4):
esquecer de informar uma verificação nunca resulta em liberação.

**Ocupação** é tratada fora da agregação de status, porque é risco econômico e não de
nulidade:

| Situação | Efeito |
|----------|--------|
| Ocupado | Risco `posse` severidade alta; status jurídico inalterado |
| Desconhecido | Pendência não bloqueante (estimar custo/prazo) |
| Desocupado | Nenhum risco de posse |

Cada verificação gera uma `Evidence` com `rule_refs=[código]`, inclusive quando
`UNKNOWN` — assim a ausência fica registrada e auditável, em vez de invisível.

### 4. Orquestração (LangGraph)

Estado compartilhado é `TypedDict` (`AnalysisState`), única via de comunicação entre
nós. Não há agentes conversando por texto livre.

Nós: `normalizar` → `identidade` → `validade_juridica` → [`economia`] → `decisao`
→ `explicacao`.

Roteamento condicional após o gate:

```python
def route_after_legal(state) -> str:
    if legal.legal_status == "BLOCK" or identity.level < 2:
        return "decisao"     # curto-circuito
    return "economia"
```

**Cálculo de confiança** — combina identidade e situação jurídica:

| Status jurídico | Confiança resultante |
|-----------------|----------------------|
| OK | `identidade + 10` (teto 100) |
| PENDENTE | `identidade × 0.7` |
| BLOCK | `identidade × 0.5` |

Decisão: a confiança não pode depender só da identidade, senão um imóvel bem
identificado com pendências jurídicas pareceria confiável. O rebaixamento
multiplicativo garante que pendência jurídica derrube a confiança abaixo do mínimo
para BUY (75), empurrando para MONITOR.

**Fallback sem LangGraph**: `run_analysis` tenta compilar o grafo e, em `ImportError`,
executa `_run_sequential` com a mesma ordem. Mantém os testes rodando sem a
dependência e evita que a orquestração se torne ponto único de falha.

### 5. Persistência

Reaproveita o que já existe e está validado contra o banco real:
`repository.save_analysis` grava `analyses` (versão crescente), `evidences`, `costs` e
`decisions`. Novidade desta fatia: gravar também `sources`, `captures`, `properties` e
`property_identifiers`.

```
save_capture(source, raw)      -> Capture   (idempotente por fingerprint)
resolve_or_create_property(ids) -> Property  (usa is_same_property)
save_analysis(opp, contract)    -> Analysis  (nova versão, nunca sobrescreve)
```

## Data Models

Modelos de domínio já definidos e reutilizados sem alteração: `Evidence`,
`CostBreakdown`, `Risk`, `Pending`, `AnalysisContract`.

Mapeamento dos artefatos desta fatia para o banco:

| Artefato do pipeline | Tabela | Observação |
|----------------------|--------|------------|
| `RawCapture` | `captures` | `raw` JSONB + `hash` único por fonte |
| `NormalizedListing` | `opportunities` (+`properties`) | dados do certame e físico |
| `IdentityResult.identifiers` | `property_identifiers` | tipo + valor + confiança |
| `LegalGateResult.evidences` | `evidences` | `rule_refs` com o código do gate |
| `LegalGateResult.pendings` | `pendings` | `blocks_buy` |
| `LegalGateResult.risks` | `risks` | categoria/severidade |
| `DecisionResult` | `decisions` | `deciding_layer` + `reasons` |

`legal_status` do gate alimenta `analyses.legal_status` (enum `OK|PENDENTE|BLOCK`).

## Error Handling

| Situação | Tratamento | Justificativa |
|----------|------------|---------------|
| Campo ilegível na fonte | `None` (UNKNOWN) + pendência | Nunca inventar valor |
| Payload sem nenhum identificador | Identidade I0 → curto-circuito | Não analisar imóvel incerto |
| Verificação jurídica não informada | `UNKNOWN` → PENDENTE | Ausência ≠ regularidade |
| `market_value` ausente | Economia não calcula; segue para decisão | Decisão trata `None` |
| Divisão por zero em `market_value` | `ValueError` explícito | Falha alto, não silencia |
| Captura duplicada | Reaproveita registro existente | Idempotência por fingerprint |
| LangGraph indisponível | Execução sequencial equivalente | Orquestração não é SPOF |

Decisão: erros de **dado** viram UNKNOWN/pendência (o negócio sabe lidar); erros de
**invariante** (mercado zero ou negativo) lançam exceção, porque indicam defeito de
programação e não devem produzir número silenciosamente errado.

## Testing Strategy

Três níveis, todos sem dependência de rede:

**Unitários (puros)** — parsers, identidade, deduplicação e gate. Casos obrigatórios:
- `"desocupado"` não é lido como ocupado
- percentual em três formatos (`"5%"`, `5`, `0.05`) converge para `0.05`
- campo ausente resulta em `None`, nunca `0`
- fingerprint estável sob reordenação de chaves
- matrículas distintas ⇒ imóveis diferentes
- preço igual **não** produz identidade
- gate sem informação ⇒ PENDENTE (não OK)
- gate com irregularidade ⇒ BLOCK mesmo com economia excelente

**Integração do pipeline** — grafo completo com o payload real do item 227:

| Cenário | Resultado esperado |
|---------|--------------------|
| Gate OK, economia insuficiente | `DO_NOT_BUY` na camada `ECONOMICS` |
| Gate BLOCK, desconto ótimo | `BLOCK` na camada `LEGAL_VALIDITY` |
| Gate PENDENTE, economia boa | `MONITOR` (confiança rebaixada) |
| Identidade I0 | curto-circuito, economia não executa |

**Golden Cases** — o item 227 é o caso de referência porque tem números verificados
contra a planilha do Método Jabes: TCO R$ 228.066,90 e desconto líquido 24%, que
reprova para revenda (mínimo 25%).

Persistência é validada por script contra o Postgres local, não em teste unitário,
para manter a suíte independente de infraestrutura.

## Design Decisions and Trade-offs

**Gate como catálogo de dados, não código condicional.** Adicionar verificação é
acrescentar entrada em `GATE_CHECKS`. Custo: todas compartilham a mesma lógica de
agregação, então uma verificação com semântica realmente diferente exigiria extensão
do modelo. Ganho: as sete atuais ficam uniformes e auditáveis.

**Verificações jurídicas como entrada, não como coleta automática.** O gate recebe
resultados; não consulta cartório nem tribunal. Reflete a limitação real do domínio
brasileiro (ausência de API confiável) apontada na análise da documentação. Permite
operar já com input manual e plugar automação depois sem mudar a lógica de decisão.

**Confiança rebaixada multiplicativamente em vez de bloqueio duro em PENDENTE.**
Alternativa descartada: tratar PENDENTE como reprovação. Isso destruiria o estado
MONITOR, que é justamente onde vive a maioria das oportunidades reais enquanto a
diligência não fecha.

**`None` como terceiro valor na deduplicação.** Um `bool` obrigaria escolher entre
"é" e "não é" quando a evidência não permite afirmar — exatamente o tipo de
adivinhação que a documentação proíbe.

## Correctness Properties

Invariantes que devem valer para **qualquer** entrada, adequadas a teste por
propriedade. Cada uma protege uma regra de negócio que, se violada, produz decisão
financeiramente errada.

Prioridade de implementação: **Property 11, 12 e 16** primeiro — sustentam a tese
central do produto ("desconto não compensa nulidade"). Depois 2, 4 e 8 (integridade
de dado) e por fim as demais.

### Property 1: Fingerprint invariante à ordem das chaves

Para qualquer payload, permutar a ordem das chaves não altera o `fingerprint`.
Violação causaria a mesma captura registrada várias vezes no banco.

**Validates: Requirements 1.2, 1.3**

### Property 2: Campo ausente nunca é preenchido

Se uma chave não existe no payload, o campo correspondente em `NormalizedListing` é
`None`. Violação significaria dado inventado sustentando decisão financeira.

**Validates: Requirements 2.2**

### Property 3: Percentual sempre normalizado

`parse_percent` retorna valor em `[0, 1]` ou `None`, para qualquer entrada.
Violação produziria comissão ou alíquota 100 vezes maior/menor.

**Validates: Requirements 2.3**

### Property 4: Ilegível é desconhecido, não zero

`parse_money` retorna `None` (nunca `0.0`) para entrada vazia ou não interpretável.
Violação faria custo desconhecido ser somado como zero, inflando a margem.

**Validates: Requirements 2.2, 2.3**

### Property 5: Vacância tem precedência sobre ocupação

Para qualquer texto contendo termo de vacância ("desocupado", "livre", "vazio"),
`parse_occupancy` retorna `False`. Violação classificaria imóvel livre como ocupado,
criando risco de posse inexistente.

**Validates: Requirements 2.4, 6.3**

### Property 6: Identidade é monotônica

Acrescentar identificadores a uma oferta nunca reduz o nível de identidade.
Violação significaria mais informação piorando a confiança.

**Validates: Requirements 3.1, 3.2, 3.3**

### Property 7: Deduplicação é simétrica

`is_same_property(a, b)` e `is_same_property(b, a)` produzem o mesmo veredito.
Violação tornaria o resultado dependente da ordem de comparação.

**Validates: Requirements 4.1**

### Property 8: Preço não influencia identidade

Alterar somente `min_bid` ou `avaliacao_fonte` nunca muda o veredito de identidade.
Violação permitiria preço coincidente fundir imóveis distintos.

**Validates: Requirements 4.4**

### Property 9: Matrículas distintas separam imóveis

Se ambas as ofertas têm matrícula e são diferentes, o resultado é sempre `False`.
Violação uniria imóveis distintos, contaminando todo o histórico.

**Validates: Requirements 4.1**

### Property 10: Escala de confiança é crescente

`IdentityLevel.confidence` cresce estritamente com o nível (I0 < I1 < I2 < I3 < I4).
Violação quebraria a coerência entre força de evidência e confiança.

**Validates: Requirements 3.1, 3.4**

### Property 11: BLOCK é absorvente no gate

Existindo ao menos uma verificação `IRREGULAR`, o status é `BLOCK`, independentemente
dos outros resultados. Violação permitiria irregularidade material compensada.

**Validates: Requirements 5.3, 5.6**

### Property 12: Verificação não informada nunca libera

Se algum código obrigatório não foi informado, o status nunca é `OK`.
Violação transformaria ausência de evidência em regularidade presumida.

**Validates: Requirements 5.4**

### Property 13: Toda verificação gera evidência

O número de evidências emitidas é igual ao número de verificações do catálogo,
inclusive as `UNKNOWN`. Violação deixaria lacuna sem registro auditável.

**Validates: Requirements 7.1, 7.2**

### Property 14: Ocupação não altera status jurídico

Para qualquer valor de ocupação (`True`, `False`, `None`), o `legal_status` permanece
determinado apenas pelas verificações. Violação trataria posse como nulidade.

**Validates: Requirements 6.1, 6.2**

### Property 15: OK exige comprovação completa

`legal_status == "OK"` se e somente se todas as verificações são `CONFIRMED` ou
`NOT_APPLICABLE`. Violação liberaria análise sem base documental.

**Validates: Requirements 5.5**

### Property 16: BLOCK jurídico nunca vira compra

Com `legal_status == "BLOCK"`, a decisão é `BLOCK` para qualquer combinação de
desconto, margem, liquidez, yield e score. É a regra central do produto.

**Validates: Requirements 5.6**

### Property 17: Custo total nunca é menor que o preço

`CostBreakdown.total >= preco`, pois todos os componentes são adições não negativas.
Violação subestimaria o custo e superestimaria a margem.

**Validates: Requirements 2.2**

### Property 18: Desconto líquido é consistente

`net_discount(tco, v) == 1 - tco/v` para todo `v > 0`. Violação tornaria o principal
indicador decisório inconsistente com sua definição canônica.

**Validates: Requirements 8.1**

### Property 19: Precedência de camadas é respeitada

A camada que determina a decisão é sempre a de menor índice entre as que eliminam a
oportunidade. Violação permitiria camada posterior sobrepor bloqueio anterior.

**Validates: Requirements 8.1, 8.5**

### Property 20: Curto-circuito impede cálculo econômico

Quando o roteamento indica curto-circuito (BLOCK ou identidade < I2), a etapa
econômica não é executada. Violação calcularia sobre premissa inválida.

**Validates: Requirements 3.5, 8.2, 8.3**

## Requirements Traceability

| Requisito | Onde é atendido |
|-----------|-----------------|
| 1 — Preservação da captura | `RawCapture` + `fingerprint`; `captures.hash` único |
| 2 — Normalização sem invenção | `parsing.py`, `normalize_caixa`, `missing_fields()` |
| 3 — Identidade I0–I4 | `IdentityLevel`, `resolve_identity`; corte em `route_after_legal` |
| 4 — Deduplicação | `is_same_property` com hierarquia e retorno `None` |
| 5 — Gate P0 | `GATE_CHECKS`, `evaluate_legal_gate`, agregação BLOCK/PENDENTE/OK |
| 6 — Ocupação como risco | Bloco de ocupação fora da agregação de status |
| 7 — Evidência com proveniência | `Evidence` por verificação, inclusive `UNKNOWN` |
| 8 — Orquestração ordenada | Topologia do grafo + `route_after_legal` |
| 9 — Snapshot imutável | `repository.save_analysis` com versão crescente |
