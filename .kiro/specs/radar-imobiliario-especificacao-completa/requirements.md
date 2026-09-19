# Requirements Document

Radar Imobiliário — Especificação Completa do Produto (Negócio + Arquitetura)

## Introduction

Este documento é a **fonte única de verdade** do produto Radar Imobiliário: uma
plataforma de inteligência que transforma ofertas de imóveis (inicialmente da CAIXA
Econômica Federal, em leilão e venda direta) em decisões de investimento
explicáveis, auditáveis e reproduzíveis.

### Fonte única normativa `[CANÔNICO]`

Este documento é o **único artefato normativo** do produto. Todo valor, regra, item de
checklist, fórmula e caso de prova está escrito aqui, sem referência por indireção a
qualquer outro arquivo. A documentação de negócio de origem (34 documentos de negócio e
arquitetura, o Checklist Mestre, a Matriz Canônica de Regras, a Matriz Mestra de Regras de
Decisão, a Base de Conhecimento de IA, o Método Jabes e a Arquitetura Técnica de IA) foi
auditada, consolidada e **absorvida**; as especificações canônicas internas anteriores
também. Nenhuma delas é fonte de trabalho: divergências entre esta spec e qualquer
material anterior resolvem-se sempre a favor desta spec.

A seção **Decisões de Consolidação** (`D1` a `D55`) é a memória de auditoria dessa
absorção: registra cada conflito encontrado, os lados em disputa, a decisão adotada e o
motivo. É o que permite entender, sem os documentos de origem, por que cada valor é o que é.

### Princípios de resolução de conflitos `[CANÔNICO]`

Estes princípios governaram a consolidação e governam qualquer conflito futuro.

| ID | Princípio |
|----|-----------|
| **P-A** | Onde os documentos divergem, prevalece a leitura que **não** converte ausência de informação nem incerteza em resultado favorável. |
| **P-B** | Onde existiam duas versões do mesmo documento com adendo, **o adendo prevalece sobre o corpo**. Verificado: as versões `v1.1` dos Documentos 15, 19 e 26 são o `v1.0` com adendo anexado e corpo não reconciliado — a própria folha de rosto continua dizendo "Versão 1.0". |
| **P-C** | O escopo mais específico prevalece, **exceto** quando o menos específico impõe bloqueio crítico ou restrição legal/documental. |
| **P-D** | A numeração de parâmetros do Documento 8 (Catálogo de Parâmetros) é **canônica**. Nenhuma renumeração silenciosa é admitida. |
| **P-E** | Distinguir sempre **ausência de evidência** (não sei ⇒ `PENDENTE`) de **evidência de ausência** (verifiquei e não existe ⇒ efeito da regra). `REPROVADO` fica reservado para evidência de irregularidade. |

### Princípio central

> **Preço é o dado. Oportunidade é a análise.**
>
> Um imóvel só é oportunidade quando o **custo econômico total** está suficientemente
> abaixo do **valor de mercado provável**, com liquidez, risco, confiança e aderência
> à estratégia compatíveis.
>
> **O preço máximo é definido por risco, mercado e custo total — nunca pela disputa.**

### Princípios invioláveis (regras de segurança do domínio)

Estes princípios têm precedência sobre qualquer outro requisito deste documento.
Nenhuma parametrização, exceção ou score pode contorná-los.

| ID | Princípio |
|----|-----------|
| SAFE-001 | Desconto não compensa nulidade. |
| SAFE-002 | Score, desconto, margem, yield, liquidez ou Investor Fit **nunca** superam um BLOCK jurídico. |
| SAFE-003 | Ausência de evidência **não** é regularidade: o resultado é `UNKNOWN`/`PENDENTE`. |
| SAFE-004 | `UNKNOWN` permanece `UNKNOWN` até existir nova evidência. |
| SAFE-005 | Custo ou risco desconhecido **nunca** é tratado como zero. |
| SAFE-006 | Consolidação registrada comprova o ato registral na data correspondente, e **não** a ausência de fatos posteriores. |
| SAFE-007 | O texto do ato registral prevalece sobre a simples detecção do evento registral. |
| SAFE-008 | Notificação/intimação é avaliada conforme o requisito aplicável ao caso concreto, não por presunção. |
| SAFE-009 | Nenhum componente automatizado cria evidência nem promove `UNKNOWN` para `CONFIRMED`. |
| SAFE-010 | Evidências contraditórias são preservadas, nunca sobrescritas. |
| SAFE-011 | Histórico é contexto e hipótese; nunca vira evidência atual automaticamente. |
| SAFE-012 | Avaliação da fonte (CAIXA) é referência informativa, nunca valor de mercado. |
| SAFE-013 | Ocupação é risco de posse e de economia, não nulidade automática do procedimento. |
| SAFE-014 | Existência isolada de processo judicial não é BLOCK automático. |
| SAFE-015 | Informação futura não pode ser usada para avaliar decisão passada (antiviés temporal). |
| SAFE-016 | Yield bruto não é yield líquido: o piso decisório de renda incide sobre o **líquido**. |
| SAFE-017 | Ausência de evidência (`PENDENTE`) e evidência de ausência (efeito da regra) são resultados distintos e nunca são fundidos. |

### Convenções

- `[CANÔNICO]` — valor decidido; alteração exige nova versão aprovada.
- `[DEFAULT]` — valor inicial parametrizável; sujeito a calibração.
- `[DEFAULT-DERIVADO]` — valor inicial deduzido de faixa qualitativa ou de teste de
  sensibilidade presente na documentação de origem; a derivação está declarada.
- `[PENDENTE-CALIBRAÇÃO]` — exige histórico real (10–20 análises) para fixar.
- `[PENDENTE-DECISÃO]` — decisão de negócio ainda não tomada.
- Toda fração é expressa em base 0–1 quando usada em cálculo e apresentada em
  percentual na interface.
- Valores monetários em BRL (`GLB-001`).

### Escopo

**Incluído:** conceito de negócio, atores, jornadas, todos os módulos funcionais,
regras de decisão determinísticas e parametrizáveis, checklists completos, valuation,
economia, risco e due diligence, gate jurídico, liquidez e saída, estratégias e
portfólio, score, ranking e motor de decisão, monitoramento e alertas, governança e
auditoria, experiência do investidor, interface de programação, parametrização, escopo e
priorização do MVP, e os guarda-corpos da arquitetura de IA (agentes, RAG, MCP, memória).

**Excluído:** execução automática de arremate/lance; substituição de parecer jurídico,
engenharia ou contabilidade; garantia de valorização, liquidez ou rentabilidade;
marketplace; gestão patrimonial completa; automação integral da due diligence.

---

## Glossary

**Glossário** — termos de sistema, jurídicos, econômicos e de produto usados de forma
normativa em todos os critérios de aceitação deste documento.

### Sistemas (nomes usados nos critérios de aceitação)

| Nome | Responsabilidade |
|------|------------------|
| **Radar** | O sistema como um todo, quando o requisito é transversal. |
| **Orquestrador** | Executa as etapas do pipeline na ordem obrigatória, com curto-circuito. |
| **Capturador** | Registra o snapshot bruto e imutável de uma fonte. |
| **Normalizador** | Converte a captura em visão estruturada comparável, sem inventar dado. |
| **Resolvedor_de_Identidade** | Determina o nível de identidade (I0–I4) do imóvel. |
| **Deduplicador** | Decide se uma captura representa imóvel já conhecido. |
| **Consolidador_de_Perfil** | Mantém a visão vigente do imóvel a partir de múltiplas capturas. |
| **Classificador_de_Localizacao** | Classifica a localização em classes A–E conforme parâmetros. |
| **Gate_Juridico** | Avalia a camada P0 (validade jurídica do procedimento). |
| **Motor_de_Valuation** | Seleciona comparáveis e produz faixas de valor com confiança. |
| **Motor_de_Calculo** | Executa todos os cálculos determinísticos (TCO, desconto, margem, yield, preço máximo, cenários). |
| **Motor_de_Risco** | Classifica riscos por categoria, probabilidade, impacto e severidade. |
| **Motor_de_Liquidez** | Estima liquidez de venda e de locação e prazos de saída. |
| **Motor_de_Estrategia** | Avalia aderência do ativo às estratégias ativas. |
| **Gestor_de_Portfolio** | Avalia capital, reserva, concentração e eficiência de capital. |
| **Motor_de_Score** | Calcula Opportunity Score e Investor Fit Score. |
| **Motor_de_Ranking** | Ordena oportunidades e explica a posição. |
| **Motor_de_Decisao** | Aplica a precedência canônica e emite a decisão. |
| **Motor_de_Explicabilidade** | Produz a justificativa rastreável da decisão. |
| **Gestor_de_Due_Diligence** | Controla fases, checklists, evidências e pendências. |
| **Monitor** | Detecta mudanças materiais e dispara reavaliação. |
| **Gestor_de_Alertas** | Emite alertas acionáveis com prioridade e anti-fadiga. |
| **Gestor_de_Governanca** | Versiona regras, parâmetros, exceções e trilha de auditoria. |
| **Gestor_de_Parametros** | Resolve parâmetros pela hierarquia de escopo. |
| **Camada_de_Evidencia** | Armazena evidência com proveniência e estado. |
| **Base_de_Conhecimento** | Recupera conhecimento normativo (regras, definições, casos) para os agentes. |
| **Interface_do_Investidor** | Apresenta o Radar, a ficha, a explicabilidade e as ações. |
| **Motor_de_Backtest** | Reproduz decisões históricas e mede acerto das regras. |

### Termos jurídicos do domínio de leilão

| Termo | Definição adotada |
|-------|-------------------|
| **Alienação fiduciária em garantia** | Garantia em que a propriedade do imóvel é transferida em caráter resolúvel ao credor (fiduciário), permanecendo o devedor (fiduciante) com a posse direta; regida pela Lei nº 9.514/97. |
| **Credor fiduciário** | Titular da propriedade fiduciária (no escopo inicial, a CAIXA). |
| **Devedor fiduciante** | Quem ofereceu o imóvel em garantia fiduciária. **Termo obrigatório em toda a spec** (ver `D46`): o devedor é o *fiduciante* e o credor é o *fiduciário*. O material de origem escrevia "devedor fiduciário" em `JUR-CHK-010`, `JUR-CHK-011` e na Matriz Canônica; está errado e foi corrigido aqui. |
| **Constituição em mora** | Ato pelo qual o devedor é formalmente colocado em situação de inadimplência, marco inicial do procedimento de execução extrajudicial. |
| **Intimação para purgação da mora** | Comunicação ao devedor fiduciante para quitar o débito no prazo legal; pode ser pessoal ou, subsidiariamente, por edital. |
| **Purgação da mora** | Quitação do débito pelo devedor dentro do prazo, que reverte o procedimento. |
| **Consolidação da propriedade** | Averbação na matrícula que torna plena, em nome do credor fiduciário, a propriedade antes resolúvel, após a não purgação da mora. |
| **Primeira praça / primeiro leilão** | Primeira sessão pública de venda; no regime do art. 27 da Lei nº 9.514/97, o valor mínimo é o valor de avaliação do imóvel. |
| **Segunda praça / segundo leilão** | Sessão subsequente, realizada quando a primeira é negativa; o valor mínimo corresponde ao valor da dívida acrescido de encargos e despesas. |
| **Leilão negativo** | Sessão encerrada sem arrematante; sua averbação na matrícula é elemento de verificação registral. |
| **Averbação** | Anotação na matrícula de fato que altera ou complementa o registro. |
| **Arrematação** | Aquisição do imóvel em leilão pelo maior lance válido. |
| **Adjudicação** | Transferência do imóvel ao credor quando não há arrematante que cubra o mínimo legal. |
| **Imissão na posse** | Ato pelo qual o adquirente obtém a posse direta do imóvel, judicial ou extrajudicialmente. |
| **Evicção** | Perda do imóvel pelo adquirente em razão de direito anterior de terceiro reconhecido; a responsabilidade do vendedor por evicção é cláusula a ser localizada no edital. |
| **Débitos propter rem** | Obrigações que acompanham a coisa e não a pessoa (tipicamente condomínio e IPTU), podendo ser exigidas do adquirente conforme o edital e a legislação aplicável. |
| **Ônus reais** | Gravames sobre o imóvel (hipoteca, usufruto, servidão, penhora) constantes da matrícula. |
| **Penhora / indisponibilidade** | Constrição judicial sobre o bem ou sobre os direitos do devedor, que pode impedir ou dificultar a transferência. |
| **Cessão de posição contratual** | Transferência, pelo devedor fiduciante a terceiro, de sua posição no contrato, frequentemente origem de posse de terceiro no imóvel. |
| **Cláusula de vigência (locação)** | Cláusula que, averbada na matrícula, permite que a locação subsista perante o adquirente. |
| **Cadeia dominial** | Sequência histórica de titularidades do imóvel na matrícula. |
| **Edital** | Documento oficial do certame; fonte primária das condições, prazos, responsabilidades e garantias da operação. |
| **Comissão do leiloeiro** | Percentual devido ao leiloeiro, tipicamente fora do lance, integrando o custo de aquisição. |
| **Vaga autônoma** | Vaga de garagem com matrícula própria, que pode não estar abrangida pela oferta da unidade. |

### Termos econômicos e de produto

| Termo | Definição adotada |
|-------|-------------------|
| **Fonte (Source)** | Origem da informação (CAIXA, leiloeiro, portal, cartório, condomínio, visita, analista). |
| **Captura (Capture)** | Snapshot imutável do que uma fonte informou em determinado momento. |
| **Imóvel (Property)** | Ativo físico/documental identificado; permanente. |
| **Oportunidade (Opportunity)** | Tese econômica sobre um Imóvel em determinado contexto de oferta; dinâmica. |
| **Análise (Analysis)** | Fotografia versionada e imutável da tese em uma data. |
| **Preço de oferta / lance mínimo** | Valor pedido pela fonte para adquirir o imóvel. |
| **Avaliação da fonte** | Valor de referência divulgado pela fonte. Informativo. |
| **Valor de mercado provável** | Estimativa do valor em condições normais de negociação. |
| **Valor de venda rápida** | Valor estimado para saída acelerada. |
| **Custo econômico total (TCO)** | Capital total necessário para adquirir e colocar o imóvel em condição de saída conforme a estratégia. |
| **Desconto da fonte** | `1 − preço / avaliação da fonte`. **Informativo, nunca decisório.** |
| **Desconto de mercado** | `1 − preço / valor de mercado provável`. |
| **Desconto líquido** | `1 − TCO / valor de mercado provável`. **Métrica decisória.** |
| **Margem de segurança** | `(valor de mercado − TCO) / valor de mercado`. |
| **Preço máximo** | Maior preço de aquisição compatível com a estratégia, o risco e o retorno exigido. |
| **Preço-alvo** | Preço desejado, com folga acima do mínimo exigido. |
| **Break-even de saída** | Menor preço de venda que cobre todo o capital empregado. |
| **Carrying cost** | Custo do tempo até a saída (condomínio, tributos, manutenção, financiamento, custo de oportunidade). |
| **Opportunity Score** | Atratividade da oportunidade em si (0–100). |
| **Investor Fit Score** | Aderência da oportunidade a um investidor específico (0–100). |
| **Confiança** | Qualidade da evidência que sustenta a análise (0–100). Dimensão independente do risco. |
| **Liquidez** | Capacidade de converter o imóvel em caixa ou renda em prazo e faixa de preço razoáveis (0–100). |
| **Hard Rule** | Regra eliminatória; não compensável por score. |
| **Soft Rule** | Regra que altera o score sem eliminar. |
| **Conditional Rule** | Regra que permite avançar apenas sob condição objetiva. |
| **Informational Rule** | Regra que gera informação ou alerta, sem decidir. |
| **Exception Rule (Override)** | Exceção explicitamente autorizada, justificada, com prazo e evidência. |
| **Gate** | Ponto de verificação que pode interromper o pipeline. |
| **Pendência (Pending)** | Questão não resolvida, com impacto, responsável, prazo e condição de encerramento. |
| **Materialidade** | Limiar a partir do qual uma mudança exige reavaliação. |
| **Frescor (freshness)** | Prazo de validade de uma informação por categoria. |
| **Golden Case** | Caso real com resultado esperado conhecido, usado para validar o comportamento do Radar. |

---

## Atores e Papéis

| Papel | Responsabilidade | Pode alterar |
|-------|------------------|--------------|
| **Investidor** | Define objetivos, capital, estratégias, limites e tomada de decisão final. | Perfil, estratégias, parâmetros de escopo investidor, decisões, exceções dentro de alçada. |
| **Analista** | Executa a análise, registra evidências e conclui pendências. | Evidências, pendências, análises, resultados de checklist. |
| **Gestor** | Aprova mudanças relevantes de negócio (pesos, limites). | Parâmetros de escopo global e estratégia. |
| **Curador de Regras** | Mantém o catálogo canônico de regras e sua coerência. | Regras e versões de regra. |
| **Auditor** | Verifica rastreabilidade e integridade; não altera conteúdo. | Nada (somente leitura). |
| **Especialista Jurídico** | Interpreta questões jurídicas que exigem parecer profissional. | Evidências e pareceres jurídicos. |
| **Especialista Físico** | Avalia condição construtiva e orçamento de reforma. | Evidências físicas e orçamentos. |
| **Radar (sistema)** | Captura, calcula, aplica regras, pontua, ranqueia, explica, monitora e registra. | Fatos calculados, scores, rankings, alertas, snapshots. |

Em operação individual, um mesmo indivíduo pode acumular papéis; a trilha de
auditoria registra o papel exercido em cada ato.

---

## Jornada Macro do Negócio

```
FONTES → CAPTURA → NORMALIZAÇÃO → IDENTIFICAÇÃO → DEDUPLICAÇÃO → QUALIFICAÇÃO
      → PERFIL CONSOLIDADO → VALIDADE JURÍDICA (P0) → COMPARÁVEIS → VALUATION
      → CUSTO → RISCO → LIQUIDEZ → ESTRATÉGIA → REGRAS → SCORE → FIT → RANKING
      → EXPLICAÇÃO → ANÁLISE → DUE DILIGENCE → DECISÃO → HISTÓRICO
      → MONITORAMENTO → RESULTADO → APRENDIZADO
```

### Fases do pipeline (`PipelinePhase`) `[CANÔNICO]` — 16 fases

Duas fases foram acrescentadas em relação à versão anterior desta spec (`D47`):
`QUALIFIED`, que materializa o gate `G1`, e `CONSOLIDATED`, que materializa o
Consolidador de Perfil. Ambas existiam como componentes e não existiam como marco
persistido, o que tornava o traço de execução incapaz de comprovar que passaram.

| Ordem | Fase | Produz |
|-------|------|--------|
| 1 | `CAPTURED` | Captura original preservada (fonte, hash, data). |
| 2 | `NORMALIZED` | Oferta normalizada com campos ausentes explicitamente `UNKNOWN`. |
| 3 | `IDENTIFIED` | Nível de identidade I0–I4 e identificadores. |
| 4 | `DEDUPLICATED` | Vínculo a Imóvel único ou criação de candidato. |
| 5 | `QUALIFIED` | Resultado do gate `G1`: elegibilidade mínima de dados e de escopo. |
| 6 | `CONSOLIDATED` | Perfil consolidado do imóvel com estado de informação por campo e divergências preservadas. |
| 7 | `LEGAL_VALIDATED` | Resultado do gate P0 (`OK`/`PENDENTE`/`BLOCK`). |
| 8 | `ENRICHED` | Comparáveis, localização, contexto, débitos, ocupação. |
| 9 | `VALUATED` | Faixas de valor + confiança do valuation. |
| 10 | `COSTED` | TCO, desconto líquido, margem, yield, preço máximo, cenários. |
| 11 | `SCORED` | Opportunity Score + Investor Fit + confiança consolidada. |
| 12 | `RANKED` | Posição no radar e explicação da posição. |
| 13 | `IN_ANALYSIS` | Due diligence em curso, pendências abertas. |
| 14 | `DECIDED` | Decisão registrada com justificativa e versões. |
| 15 | `MONITORED` | Gatilhos ativos de reavaliação. |
| 16 | `CLOSED` | Encerrada (arrematada, perdida, expirada, sem interesse). |

### Estados de decisão (`DecisionState`) `[CANÔNICO]`

| Código | Significado | Veredito Método Jabes |
|--------|-------------|-----------------------|
| `BUY` | Arrematar dentro do teto de preço. | A |
| `BUY_IF` | Arrematar sob condição objetiva ou teto definido. | B / D |
| `MONITOR` | Tese interessante, diligência ou timing incompletos. | C |
| `DO_NOT_BUY` | Economia ou estratégia não compensam. | E (econômico) |
| `BLOCK` | Impedimento crítico; não participar. | E (jurídico) |
| `PENDING` | Estado antes de `DECIDED`. | — |

### Transições de fase válidas

```
CAPTURED → NORMALIZED → IDENTIFIED → DEDUPLICATED → QUALIFIED → CONSOLIDATED
   → LEGAL_VALIDATED → ENRICHED → VALUATED → COSTED → SCORED → RANKED
   → IN_ANALYSIS → DECIDED → MONITORED → CLOSED

Curto-circuitos:
   LEGAL_VALIDATED --(BLOCK jurídico)--> DECIDED[BLOCK]
   IDENTIFIED      --(identidade < I2)--> DECIDED[PENDING|DO_NOT_BUY]
   qualquer fase   --(bloqueio crítico)--> DECIDED[BLOCK]

Reentradas:
   MONITORED       --(gatilho material)--> IN_ANALYSIS (nova versão de análise)
   DECIDED[BUY_IF] --(condição satisfeita)--> IN_ANALYSIS → DECIDED
   DECIDED[*]      --(mudança material)--> IN_ANALYSIS (nova versão)
```

### Estados da captura (`CaptureState`)

`Captured` · `Normalized` · `Identified` · `Matched` · `Qualified` · `Enriched` ·
`Expired` · `Superseded` · `Rejected` · `Error`

### Estados do imóvel (`PropertyState`)

`Candidate` · `Active` · `Monitoring` · `Opportunity` · `Acquired` · `Sold` ·
`Inactive` · `Closed`

---

## Catálogo Normativo de Parâmetros

Toda decisão de negócio é governada por parâmetros nomeados, versionados e
resolvidos pela hierarquia de escopo. Os valores abaixo são os **defaults de
fábrica** (versão de parâmetros `1.0.0`).

### Hierarquia de escopo e precedência de resolução `[CANÔNICO]`

```
Global → Perfil do Investidor → Estratégia → Localização → Tipo de Imóvel
       → Oportunidade → Exceção autorizada
```
O escopo mais específico prevalece, **exceto** quando o escopo menos específico
impõe bloqueio crítico ou restrição legal/documental (ver precedência de conflitos).

### GLB — Globais

| ID | Parâmetro | Valor default | Unidade | Status |
|----|-----------|---------------|---------|--------|
| GLB-001 | `moeda` | BRL | — | `[CANÔNICO]` |
| GLB-002 | `margem_minima_global` | 0,15 | fração | `[DEFAULT]` (`D9`) |
| GLB-003 | `confianca_minima_para_buy` | 75 | 0–100 | `[DEFAULT]` |
| GLB-004 | `score_minimo_global` | 60 | 0–100 | `[DEFAULT]` |
| GLB-005 | `risco_maximo_aceitavel` | medio | baixo\|medio\|alto | `[DEFAULT]` |
| GLB-006 | `liquidez_minima_global` | 70 | 0–100 | `[DEFAULT]` (`D7`) |
| GLB-007 | `custo_oportunidade_capital_aa` | taxa Selic vigente | % a.a. | `[DEFAULT-DERIVADO]` — referência financeira do custo do tempo; usada no carrying de `R30.3` (`D14`) |
| GLB-008 | `horizonte_investimento_padrao` | 24 | meses | `[DEFAULT]` |
| GLB-009 | `tolerancia_excecoes` | baixa | baixa\|media\|alta | `[DEFAULT]` |
| GLB-010 | `validade_analise_dias` | 30 | dias | `[DEFAULT]` |
| GLB-011 | `retorno_minimo_exigido_aa` | Selic + 15 p.p. | % a.a. | `[DEFAULT]` — hurdle de aceitação usado em `R33.9` (`D14`) |

`GLB-007` e `GLB-011` são parâmetros **distintos** com funções distintas: o primeiro é o
preço do tempo do capital e entra no custo; o segundo é o retorno mínimo que o investidor
exige e é comparado com o retorno produzido. Antes da consolidação, um único parâmetro
acumulava as duas funções e o retorno exigido era cobrado duas vezes — uma dentro do custo
e outra como limiar de aprovação (`D14`).

### INV — Perfil do Investidor

| ID | Parâmetro | Valor default | Unidade | Status |
|----|-----------|---------------|---------|--------|
| INV-001 | `capital_disponivel` | 300.000 | BRL | `[DEFAULT]` |
| INV-002 | `ticket_maximo` | 250.000 | BRL | `[DEFAULT]` |
| INV-003 | `entrada_maxima` | 100.000 | BRL | `[DEFAULT]` |
| INV-004 | `parcela_maxima_mensal` | 3.000 | BRL/mês | `[DEFAULT]` |
| INV-005 | `reserva_minima` | 50.000 | BRL | `[DEFAULT]` |
| INV-006 | `horizonte` | medio | curto\|medio\|longo | `[DEFAULT]` |
| INV-007 | `objetivo` | renda + revenda | lista | `[DEFAULT]` |
| INV-008 | `tolerancia_reforma` | 2 | nível 0–4 | `[DEFAULT]` |
| INV-009 | `tolerancia_risco` | media | baixa\|media\|alta | `[DEFAULT]` |
| INV-010 | `aceita_ocupacao` | condicional | sim\|nao\|condicional | `[DEFAULT]` |
| INV-011 | `aceita_financiamento` | nao | sim\|nao | `[DEFAULT]` |
| INV-012 | `aceita_consorcio` | nao | sim\|nao | `[DEFAULT]` |
| INV-013 | `prioridade_liquidez` | alta | baixa\|media\|alta | `[DEFAULT]` |
| INV-014 | `prioridade_renda` | media | baixa\|media\|alta | `[DEFAULT]` |
| INV-015 | `percentual_maximo_do_capital_por_operacao` | 0,25 | fração | `[DEFAULT]` |
| INV-016 | `percentual_maximo_do_patrimonio_por_operacao` | 0,15 | fração | `[DEFAULT]` |
| INV-017 | `indice_conforto_pessoal_minimo` | 60 | 0–100 | `[DEFAULT]` (Método Jabes, pilar Contexto Humano) |
| INV-018 | `exige_parecer_juridico_registrado_para_aceitar_risco_juridico_relevante` | sim | sim\|nao | `[DEFAULT]` (`D5`) |
| INV-019 | `reserva_minima_pct_patrimonio_liquido` | 0,10 | fração do patrimônio líquido | `[DEFAULT]` (`D41`) |
| INV-020 | `esforco_operacional_aceitavel` | medio | baixo\|medio\|alto | `[DEFAULT]` (`D41`) |
| INV-021 | `meta_de_renda_mensal` | (não definida) | BRL/mês | `[DEFAULT]` (`D41`) |

`INV-018` **não** condiciona o hard stop de parecer jurídico. O hard stop `HS-09` dispara
sempre que a aceitação de um risco depender de parecer jurídico e o parecer não estiver
registrado como evidência, independentemente do valor de `INV-018` (`D5`). O parâmetro
existe para declarar a exigência do investidor, não para desligar a proteção.

A reserva mínima aplicável é o **maior** valor entre `INV-005` (absoluta) e
`INV-019 × patrimônio líquido` (percentual).

### LOC — Localização

| ID | Parâmetro | Valor default | Unidade | Status |
|----|-----------|---------------|---------|--------|
| LOC-001 | `cidades_permitidas` | (vazio = todas) | lista | `[DEFAULT]` |
| LOC-002 | `cidades_bloqueadas` | (vazio) | lista | `[DEFAULT]` |
| LOC-003 | `bairros_prioritarios` (classe A) | (vazio) | lista | `[DEFAULT]` |
| LOC-004 | `bairros_aceitaveis` (classe B) | (vazio) | lista | `[DEFAULT]` |
| LOC-005 | `bairros_condicionais` (classe C) | (vazio) | lista | `[DEFAULT]` |
| LOC-006 | `zonas_de_exclusao` (classe E) | (vazio) | geometrias/lista | `[DEFAULT]` |
| LOC-007 | `distancia_referencia_max` | 2,0 | km | `[DEFAULT]` |
| LOC-008 | `liquidez_minima_regional` | 70 | 0–100 | `[DEFAULT]` |
| LOC-009 | `valorizacao_historica_minima_aa` | (não decidido) | % a.a. | `[PENDENTE-DECISÃO]` — não aplicado; requisito dependente reportado como NÃO AVALIADO |
| LOC-010 | `yield_regional_minimo` | (não decidido) | % mês | `[PENDENTE-DECISÃO]` — não aplicado; requisito dependente reportado como NÃO AVALIADO |
| LOC-011 | `perfil_socioeconomico_aceitavel` | (vazio = todos) | lista | `[DEFAULT]` — **informativo**; não entra em liquidez, risco nem qualidade (`D15`) |
| LOC-012 | `restricao_risco_local` | (vazio) | lista | `[DEFAULT]` |
| LOC-013 | `desconto_liquido_adicional_classe_C` | 0,35 | fração | `[DEFAULT]` (compensação obrigatória; ID novo por `D15`) |

### TIP — Tipo de Imóvel

| ID | Parâmetro | Valor default | Status |
|----|-----------|---------------|--------|
| TIP-001 | `tipos_aceitos` = apartamento, casa, sobrado, terreno, sala/conjunto, loja, galpão, rural, outros | `[DEFAULT]` |
| TIP-002 | `tipos_bloqueados` = (vazio) | `[DEFAULT]` |
| TIP-003 | `quartos_minimos` = 1 | `[DEFAULT]` |
| TIP-004 | `quartos_maximos` = (sem limite) | `[DEFAULT]` |
| TIP-005 | `area_minima_m2` = (sem limite) | `[DEFAULT]` |
| TIP-006 | `area_maxima_m2` = (sem limite) | `[DEFAULT]` |
| TIP-007 | `vagas_minimas` = 0 | `[DEFAULT]` |
| TIP-008 | `condominio_maximo_mensal` = (sem limite absoluto; ver CUS/REN) | `[DEFAULT]` |
| TIP-009 | `aceita_mcmv` = condicional | `[DEFAULT]` |
| TIP-010 | `aceita_reforma` = condicional | `[DEFAULT]` |
| TIP-011 | `aceita_terreno` = sim | `[DEFAULT]` |
| TIP-012 | `aceita_imovel_ocupado` = condicional | `[DEFAULT]` |

### PRI — Preço, Ticket e Desconto

| ID | Parâmetro | Valor default | Unidade | Status |
|----|-----------|---------------|---------|--------|
| PRI-001 | `preco_minimo` | 80.000 | BRL | `[DEFAULT]` |
| PRI-002 | `preco_maximo` | 400.000 | BRL | `[DEFAULT]` |
| PRI-003 | `desconto_minimo_sobre_avaliacao` | 0,20 | fração | `[DEFAULT]` — informativo |
| PRI-004 | `desconto_minimo_sobre_mercado` | 0,15 | fração | `[DEFAULT]` |
| PRI-005 | `desconto_liquido_minimo_global` | 0,15 | fração | `[DEFAULT]` (piso global; estratégia prevalece se mais restritiva) (`D10`) |
| PRI-006 | `faixa_ticket_prioritaria` | 150.000 – 250.000 | BRL | `[DEFAULT]` |
| PRI-007 | `desconto_excepcional` | ≥ 0,30 | fração | `[DEFAULT]` — aciona exceção auditável |
| PRI-008 | `preco_m2_maximo` | (não decidido) | BRL/m² | `[PENDENTE-DECISÃO]` — não aplicado; requisito dependente reportado como NÃO AVALIADO |
| PRI-009 | `preco_m2_maximo_relativo_mediana` | 1,00 | fração da mediana | `[DEFAULT]` |

### CUS — Custos (componentes do TCO)

| ID | Componente | Default | Unidade | Status |
|----|-----------|---------|---------|--------|
| CUS-001 | `preco_lance` | (obrigatório da oferta) | BRL | `[CANÔNICO]` |
| CUS-002 | `comissao_leiloeiro_pct` | 0,05 | fração do preço | `[DEFAULT]` (edital prevalece) |
| CUS-003 | `itbi_pct` | 0,02 | fração do preço | `[DEFAULT]` (município prevalece) |
| CUS-004 | `registro_documentacao` | 3.000 | BRL | `[DEFAULT]` |
| CUS-005 | `condominio_debitos` | (obrigatório investigar) | BRL | `[CANÔNICO]` |
| CUS-006 | `tributos_debitos` (IPTU e taxas) | (obrigatório investigar) | BRL | `[CANÔNICO]` |
| CUS-007 | `reforma` | faixa por nível 0–4 | BRL | `[CANÔNICO]` |
| CUS-008 | `desocupacao` | faixa por cenário | BRL | `[CANÔNICO]` |
| CUS-009 | `regularizacao` | faixa por cenário | BRL | `[CANÔNICO]` |
| CUS-010 | `custo_financeiro` | 0 (padrão à vista) | BRL | `[DEFAULT]` |
| CUS-011 | `reserva_imprevistos_pct` | 0,05 | fração do custo de aquisição | `[DEFAULT]` |
| CUS-012 | `custo_venda_corretagem_pct` | 0,06 | fração do preço de venda | `[DEFAULT]` |
| CUS-013 | `ir_ganho_capital_pct` | 0,15 | fração do ganho | `[DEFAULT]` — simplificação declarada; ver `PEND-IR` |
| CUS-014 | `custo_juridico_potencial` | (obrigatório investigar) | BRL | `[CANÔNICO]` — estado `UNKNOWN` gera contingência e pendência (`D13`) |
| CUS-015 | `probabilidade_juridica` | (obrigatório investigar) | fração 0–1 | `[CANÔNICO]` — estado `UNKNOWN` gera contingência e pendência (`D13`) |
| CUS-016 | `carrying_mensal` | condomínio + IPTU e taxas + seguro e manutenção + custo financeiro + despesas operacionais + custo de oportunidade do capital (`GLB-007`) | BRL/mês | `[CANÔNICO]` (`D32`) |
| CUS-017 | `contingencia_reforma_pct` por nível | N0 = 0,00 · N1 = 0,10 · N2 = 0,15 · N3 = 0,25 · N4 = 0,50 | fração do orçamento | `[DEFAULT-DERIVADO]` de +10%, +25% e +50%; **N2 = 0,15 é interpolação** ⇒ `[PENDENTE-CALIBRAÇÃO]` (`D54`) |
| CUS-018 | `contingencia_adicional_sem_vistoria_pct` | 0,10 | fração adicional | `[PENDENTE-CALIBRAÇÃO]` — derivação sem sensibilidade documentada (`D54`) |
| CUS-019 | `contingencia_adicional_imovel_ocupado_pct` | 0,10 | fração adicional | `[PENDENTE-CALIBRAÇÃO]` — derivação sem sensibilidade documentada (`D54`) |

**Custo desconhecido nunca é zero.** `CUS-005`, `CUS-006`, `CUS-014` e `CUS-015` não têm
valor default: o default é o estado `UNKNOWN`, que obriga contingência, pendência e marca
o preço máximo como provisório. Atribuir zero a qualquer um deles exige evidência de que o
componente não é aplicável ou é efetivamente nulo (`R26.10`, SAFE-005, `D13`).

**Escopo do TCO e o componente de custo de oportunidade.** O custo econômico total é o
custo de **adquirir e transformar até a condição de saída**; ele **não** inclui custos de
saída nem imposto de renda sobre ganho de capital, que pertencem exclusivamente à perna de
venda (`D26`). Pela mesma razão, o componente `custo de oportunidade do capital` de
`CUS-016` integra o carrying apenas nas análises de custo do tempo e de eficiência de
capital (`R30.2`, `R30.3`); ele é **excluído** do TCO usado em desconto líquido, margem e
ROI, porque nessas métricas o retorno exigido já é cobrado pelo limiar `GLB-011`. Somar nos
dois lugares cobraria o mesmo retorno duas vezes.

### VAL — Valuation

A numeração abaixo é a do Documento 8 restaurada (`P-D`, `D15`). A versão anterior desta
spec havia renumerado silenciosamente as faixas `VAL` e `CMP`, perdido dois parâmetros
(`VAL-008` margem conservadora e `CMP-008` estado de conservação) e apontado
referências cruzadas para os IDs errados. A tabela de equivalência
**ID antigo → ID novo** está publicada no fim desta seção.

| ID | Parâmetro | Valor default | Status |
|----|-----------|---------------|--------|
| VAL-001 | `comparaveis_minimos` | 5 | `[DEFAULT]` |
| VAL-002 | `priorizar_mesmo_condominio` | sim | `[CANÔNICO]` |
| VAL-003 | `raio_maximo_comparaveis_km` | 1,0 | `[DEFAULT]` |
| VAL-004 | `janela_temporal_comparaveis_meses` | 12 | `[DEFAULT]` |
| VAL-005 | `peso_comparavel_recente` | decaimento linear até a janela `VAL-004` | `[DEFAULT]` |
| VAL-006 | `peso_mesmo_condominio` | alto (2,0× relativo) | `[DEFAULT]` |
| VAL-007 | `desconto_venda_rapida_pct` | 0,05 a 0,15 | `[DEFAULT]` |
| VAL-008 | `margem_conservadora_pct` | 0,10 | `[DEFAULT-DERIVADO]` — fração subtraída do valor `base` para obter o valor `conservador`; derivada do ponto médio da faixa de `VAL-007`. **Reintroduzido** (`D15`) |
| VAL-009 | `confianca_minima_valuation` | 70 | `[DEFAULT]` |
| VAL-010 | `diferenca_maxima_entre_fontes_pct` | 0,15 | `[DEFAULT-DERIVADO]` (acima disso, conflito material) |
| VAL-011 | `comparaveis_ideais` | 7 | `[DEFAULT]` — limiar único, não faixa (`D30`) |

### CMP — Comparáveis

| ID | Critério | Default | Status |
|----|----------|---------|--------|
| CMP-001 | `prioridade_mesmo_condominio` | máxima | `[CANÔNICO]` |
| CMP-002 | `prioridade_mesmo_bairro` | alta | `[CANÔNICO]` |
| CMP-003 | `distancia_comparavel_max_km` | 1,0 (alinhado a `VAL-003`) | `[DEFAULT]` |
| CMP-004 | `tolerancia_area_pct` | ± 0,20 | `[DEFAULT]` |
| CMP-005 | `tolerancia_quartos` | ± 1 | `[DEFAULT]` |
| CMP-006 | `tolerancia_vagas` | ± 1 | `[DEFAULT]` |
| CMP-007 | `padrao_construtivo_compativel` | obrigatório | `[CANÔNICO]` |
| CMP-008 | `estado_conservacao_ajuste_obrigatorio` | sim | `[CANÔNICO]` — **Reintroduzido** (`D15`); é a variável que mais separa imóvel de leilão de imóvel anunciado |
| CMP-009 | `anuncio_muito_antigo` | penalizar além de `CMP-011` | `[CANÔNICO]` |
| CMP-010 | `outlier` | excluir ou penalizar conforme `CMP-012` | `[CANÔNICO]` |
| CMP-011 | `idade_maxima_anuncio_meses` | 12 | `[DEFAULT]` |
| CMP-012 | `criterio_outlier` | fora de ± 1,5 × IQR do preço por m² da amostra | `[DEFAULT-DERIVADO]` |
| CMP-013 | `penalidade_anuncio_antigo` | −50% de peso além de 6 meses | `[DEFAULT-DERIVADO]` |
| CMP-014 | `qualidade_comparavel` | classes A–E e U conforme hierarquia de evidências de mercado | `[CANÔNICO]` |

### Tabela de equivalência de identificadores (ID antigo → ID novo) `[CANÔNICO]`

Publicada para que nenhuma leitura futura reintroduza a renumeração corrigida por `D15`.

| ID antigo nesta spec | Parâmetro | ID novo (canônico) |
|----------------------|-----------|--------------------|
| `VAL-002` | comparáveis ideais | `VAL-011` |
| `VAL-003` | priorizar mesmo condomínio | `VAL-002` |
| `VAL-004` | raio máximo de comparáveis | `VAL-003` |
| `VAL-005` | janela temporal de comparáveis | `VAL-004` |
| `VAL-006` | desconto de venda rápida | `VAL-007` |
| `VAL-007` | confiança mínima de valuation | `VAL-009` |
| `VAL-008` | diferença máxima entre fontes | `VAL-010` |
| `VAL-009` | peso de mesmo condomínio | `VAL-006` |
| `VAL-010` | peso de comparável recente | `VAL-005` |
| — | margem conservadora | `VAL-008` (reintroduzido) |
| `CMP-003` | tolerância de área | `CMP-004` |
| `CMP-004` | tolerância de quartos | `CMP-005` |
| `CMP-005` | tolerância de vagas | `CMP-006` |
| `CMP-006` | padrão construtivo compatível | `CMP-007` |
| `CMP-007` | idade máxima do anúncio | `CMP-011` |
| `CMP-008` | penalidade de anúncio antigo | `CMP-013` |
| `CMP-009` | critério de outlier por IQR | `CMP-012` |
| `CMP-010` | qualidade do comparável | `CMP-014` |
| — | distância máxima do comparável | `CMP-003` |
| — | estado de conservação como ajuste obrigatório | `CMP-008` (reintroduzido) |
| — | anúncio muito antigo | `CMP-009` |
| — | outlier | `CMP-010` |
| `LOC-011` | desconto líquido adicional de classe C | `LOC-013` |
| — | perfil socioeconômico aceitável | `LOC-011` (restaurado) |
| `ALT-010` | pendência vencida | `ALT-016` |
| — | reavaliação por evento material | `ALT-010` (restaurado) |

### REN — Renda, Aluguel e Yield

| ID | Parâmetro | Valor default | Status |
|----|-----------|---------------|--------|
| REN-001 | `aluguel_mensal_estimado` | (estimado com confiança) | `[CANÔNICO]` |
| REN-002 | `yield_bruto_mensal_minimo` | 0,0080 | `[DEFAULT]` — **informativo; perdeu efeito decisório** (`D31`) |
| REN-003 | `yield_bruto_mensal_alvo` | 0,0100 | `[DEFAULT]` |
| REN-004 | `vacancia_pct` | 0,05 | `[DEFAULT]` |
| REN-005 | `inadimplencia_pct` | (obrigatório investigar) | `[CANÔNICO]` — estado `UNKNOWN` gera contingência e pendência (`D13`) |
| REN-006 | `condominio_nao_recuperavel_mensal` | (do imóvel) | `[CANÔNICO]` |
| REN-007 | `iptu_nao_recuperavel_mensal` | (do imóvel) | `[CANÔNICO]` |
| REN-008 | `manutencao_mensal` | 100 BRL ou 5% do aluguel, o maior | `[DEFAULT-DERIVADO]` |
| REN-009 | `yield_liquido_mensal_minimo` | 0,0080 | `[CANÔNICO]` `[PENDENTE-CALIBRAÇÃO]` — piso **decisório**, incide sobre o yield **líquido** (`D31`) |
| REN-010 | `prazo_maximo_para_alugar_dias` | 90 | `[DEFAULT]` |
| REN-011 | `aluguel_por_cenario` | conservador / base / otimista | `[CANÔNICO]` |
| REN-012 | `ir_aluguel_pct` | (não decidido) | `[PENDENTE-DECISÃO]` — sem default numérico; enquanto pendente, o yield líquido é emitido como **provisório** (`D13`) |

**Por que o piso incide sobre o líquido** (`D31`, SAFE-016). No caso de prova do item 227 o
yield bruto mensal é 0,833% e o líquido é 0,4955%. Um piso de 0,80% aplicado ao **bruto**
aprovaria a estratégia de renda em um imóvel cujo aluguel líquido é 62% do bruto
(`1.170 ÷ 1.900 = 0,6158`); aplicado ao **líquido**, reprova. Aplicar o piso ao bruto
transformaria custos recorrentes desconhecidos ou não deduzidos em melhora da tese, o que
`P-A` e SAFE-005 proíbem.

**Base do imposto de renda sobre aluguel** `[CANÔNICO]` (`D31`):
`base_ir_aluguel = máx(0; aluguel − condomínio não recuperável − IPTU não recuperável − manutenção − seguro e taxas) × REN-012`.
Enquanto `REN-012` estiver `[PENDENTE-DECISÃO]`, o imposto não é aplicado e o yield líquido
é rotulado como provisório; ele **não** é tratado como zero comprovado.

### LIQ — Liquidez

| ID | Parâmetro | Valor default | Status |
|----|-----------|---------------|--------|
| LIQ-001 | `score_liquidez_minimo_global` | 70 | `[DEFAULT]` (`D7`) |
| LIQ-002 | `prazo_maximo_venda_dias` | 180 | `[DEFAULT]` |
| LIQ-003 | `prazo_alvo_venda_dias` | 90 | `[DEFAULT]` |
| LIQ-004 | `desconto_maximo_para_saida_pct` | 0,10 | `[DEFAULT]` |
| LIQ-005 | `compradores_potenciais_minimos` | (não decidido) | `[PENDENTE-DECISÃO]` — não aplicado; requisito dependente reportado como NÃO AVALIADO |
| LIQ-006 | `demanda_aluguel_minima` | media | `[DEFAULT]` |
| LIQ-007 | `liquidez_por_bairro` | score regional | `[CANÔNICO]` |
| LIQ-008 | `liquidez_por_ticket` | score por faixa | `[CANÔNICO]` |
| LIQ-009 | `prazo_maximo_carregamento_meses` | 24 | `[DEFAULT]` (FIN-CHK-023) |
| LIQ-010 | `margem_adicional_por_prazo` | 0–3 m: +0% · 3–6 m: +2 p.p. · 6–12 m: +5 p.p. · >12 m: +10 p.p. | `[DEFAULT-DERIVADO]` das faixas de custo do tempo |
| LIQ-011 | `margem_minima_liquidez_baixa` | 0,30 | `[DEFAULT]` — margem mínima exigida quando o score de liquidez está abaixo do mínimo da estratégia (`D43`) |

`LIQ-010` e `LIQ-011` tratam de compensações diferentes e cumulativas: `LIQ-010` compensa
**prazo**, `LIQ-011` compensa **iliquidez**. Antes da consolidação, `R45.10` exigia "margem
adicional" sem número e `LIQ-010` era indevidamente usado como se cobrisse liquidez (`D43`).

### RISK — Risco

| ID | Risco | Tratamento default | Status |
|----|-------|--------------------|--------|
| RISK-001 | `risco_juridico_critico` | BLOCK | `[CANÔNICO]` |
| RISK-002 | `ocupacao` | risco alto com custo e prazo no cenário; severidade `critico` e BLOCK quando o impacto é crítico e não há estratégia de desocupação, ou quando há posse litigiosa com evidência de litígio; ocupação desconhecida ⇒ `PENDENTE` de prioridade `alta` mais contingência | `[CANÔNICO]` (`D2`) |
| RISK-003 | `debitos_incertos` | contingência + pendência | `[CANÔNICO]` |
| RISK-004 | `matricula_inconsistente` | PENDENTE; BLOCK se conflito material | `[CANÔNICO]` |
| RISK-005 | `processo_relevante` | investigar objeto, fase, decisão e impacto | `[CANÔNICO]` |
| RISK-006 | `reforma_elevada` | penalidade de score + contingência | `[CANÔNICO]` |
| RISK-007 | `baixa_liquidez` | penalidade; bloqueio quando abaixo do mínimo da estratégia | `[CANÔNICO]` |
| RISK-008 | `dados_insuficientes` | redução de confiança | `[CANÔNICO]` |
| RISK-009 | `risco_desocupacao` | cenário de prazo e custo | `[CANÔNICO]` |
| RISK-010 | `risco_revenda` | penalidade de score | `[CANÔNICO]` |
| RISK-011 | `matriz_probabilidade_impacto` | conforme tabela do Domínio G | `[CANÔNICO]` |

### CONF — Confiança e Qualidade dos Dados

| ID | Parâmetro | Valor default | Status |
|----|-----------|---------------|--------|
| CONF-001 | `confianca_preco` | dimensão independente 0–100 | `[CANÔNICO]` |
| CONF-002 | `confianca_valuation` | dimensão independente 0–100 | `[CANÔNICO]` |
| CONF-003 | `confianca_aluguel` | dimensão independente 0–100 | `[CANÔNICO]` |
| CONF-004 | `confianca_custos` | dimensão independente 0–100 | `[CANÔNICO]` |
| CONF-005 | `confianca_juridica` | dimensão independente 0–100 | `[CANÔNICO]` |
| CONF-006 | `dados_minimos_para_score` | conjunto G0–G2 do Domínio A | `[CANÔNICO]` |
| CONF-007 | `fator_confianca` | 90–100 → 1,00 · 75–89 → 0,95 · 60–74 → 0,88 · 40–59 → 0,75 · 0–39 → 0,60 | `[DEFAULT]` |
| CONF-008 | `validade_evidencia_dias` por categoria | ver tabela FRESH | `[DEFAULT]` |
| CONF-009 | `confianca_consolidada` | mínimo ponderado das dimensões obrigatórias da etapa | `[DEFAULT-DERIVADO]` |
| CONF-010 | `nivel_confianca_nomeado` | ver tabela de níveis abaixo | `[CANÔNICO]` (`D12`) |

**Escala nomeada de confiança** `[CANÔNICO]` (`D12`). Os seis níveis abaixo são a face
qualitativa da mesma escala numérica de `CONF-007`; não são uma escala paralela.

| Nível | Faixa | Fator (`CONF-007`) | Interpretação | Efeito na decisão |
|-------|-------|--------------------|---------------|-------------------|
| `muito_alta` | 90–100 | 1,00 | Evidência robusta e atual | Recomendação normal |
| `alta` | 75–89 | 0,95 | Boa evidência | Pequena cautela |
| `media` | 60–74 | 0,88 | Evidência razoável | Score e recomendação com ressalva |
| `baixa` | 40–59 | 0,75 | Muitas estimativas ou lacunas | Priorizar investigação; `BUY` impedido por `GLB-003` |
| `muito_baixa` | 0–39 | 0,60 | Tese pouco sustentada | Não recomendar compra |
| `inconclusiva` | — | — | Dimensão crítica ausente ou conflitante | `PENDENTE` ou `BLOCK` conforme a dimensão (`R50.5`, `R55.15`) |

`inconclusiva` **não** é uma faixa numérica: é o estado em que uma dimensão obrigatória de
confiança é `UNKNOWN` ou conflitante. Nesse estado o Radar não se limita a deixar de
recomendar — emite `PENDENTE` ou `BLOCK`. A versão anterior desta spec usava uma faixa
`insuficiente` inexistente nas fontes; o termo foi eliminado (`D12`).

### FRESH — Frescor dos Dados

| Categoria | Validade default | Status |
|-----------|------------------|--------|
| Preço e status da oferta | 3 dias | `[DEFAULT-DERIVADO]` de "sensibilidade muito alta" |
| Data/hora/plataforma do certame | 1 dia (revalidação obrigatória no dia do lance) | `[CANÔNICO]` |
| Condições de venda (edital) | 7 dias | `[DEFAULT-DERIVADO]` |
| Comparáveis de venda e aluguel | 90 dias | `[DEFAULT-DERIVADO]` |
| Aluguel de mercado | 60 dias | `[DEFAULT-DERIVADO]` |
| Valuation | 90 dias | `[DEFAULT-DERIVADO]` |
| Matrícula e documentação registral | **até mudança ou evidência nova**, com revalidação obrigatória antes da decisão de compra e alerta de revalidação aos 30 dias | `[CANÔNICO]` (`D48`) |
| Processos judiciais | 15 dias | `[DEFAULT-DERIVADO]` |
| Estimativa de reforma | 90 dias | `[DEFAULT-DERIVADO]` |
| Infraestrutura da região | 365 dias | `[DEFAULT-DERIVADO]` |
| Localização estrutural | 730 dias | `[DEFAULT-DERIVADO]` |
| Score e ranking | reavaliação a cada mudança material | `[CANÔNICO]` |

### SCORE — Pesos e Faixas

Esta é a única seção do catálogo que não tinha coluna de identificador, embora `R62.11`
exija versão vigente para todo parâmetro aplicado. Os identificadores abaixo fecham a
lacuna (`D40`).

**`SCORE-001` — Pesos mestres do Opportunity Score** `[DEFAULT]` `[PENDENTE-CALIBRAÇÃO]`

| Fator | Peso |
|-------|------|
| `desconto_liquido` | 0,25 |
| `margem_seguranca` | 0,20 |
| `liquidez` | 0,15 |
| `localizacao` | 0,15 |
| `risco` | 0,10 |
| `yield_renda` | 0,05 |
| `valorizacao` | 0,05 |
| `qualidade_oportunidade` | 0,05 |
| **Total** | **1,00** |

**`SCORE-002` — Pesos por estratégia (overrides)** `[DEFAULT]` — cada coluna soma 1,00

O fator `qualidade_oportunidade` passa a constar das cinco colunas. Antes da consolidação
ele estava ausente dos overrides e, como as colunas já fechavam 1,00 sem ele, seu peso
efetivo por estratégia era **zero** — contrariando `R49.2` e `R60.2`, que o exigem como
componente. Os demais pesos foram reduzidos proporcionalmente para abrir os 0,05
(`D22`).

| Fator | revenda | renda | valorizacao | mcmv | terreno |
|-------|---------|-------|-------------|------|---------|
| `desconto_liquido` | 0,28 | 0,14 | 0,14 | 0,19 | 0,24 |
| `margem_seguranca` | 0,19 | 0,14 | 0,14 | 0,14 | 0,19 |
| `liquidez` | 0,19 | 0,19 | 0,14 | 0,19 | 0,14 |
| `localizacao` | 0,14 | 0,19 | 0,29 | 0,14 | 0,24 |
| `yield_renda` | 0,00 | 0,19 | 0,05 | 0,14 | 0,00 |
| `valorizacao` | 0,10 | 0,05 | 0,14 | 0,05 | 0,10 |
| `risco` | 0,05 | 0,05 | 0,05 | 0,10 | 0,04 |
| `qualidade_oportunidade` | 0,05 | 0,05 | 0,05 | 0,05 | 0,05 |
| **Total** | **1,00** | **1,00** | **1,00** | **1,00** | **1,00** |

**`SCORE-005` — Score econômico (indicador informativo)** `[DEFAULT]` (`D44`)

Indicador auxiliar de sete componentes, **sem efeito decisório**. Existe para comunicar a
qualidade econômica isolada e não substitui nem alimenta o Opportunity Score; os pesos são
diferentes dos pesos mestres e a versão anterior desta spec o arrolava como concordante com
eles, o que era leitura errada da fonte.

| Componente | Peso |
|------------|------|
| `desconto` | 25 |
| `margem` | 25 |
| `roi` | 15 |
| `liquidez` | 10 |
| `prazo` | 10 |
| `risco_economico` | 10 |
| `complexidade` | 5 |
| **Total** | **100** |

**`SCORE-003` — Faixas de classificação do score** `[CANÔNICO]`

| Faixa | Classe | Rótulo | Ação típica |
|-------|--------|--------|-------------|
| 90–100 | 🔥 | Excepcional | Prioridade máxima |
| 80–89 | 🟢 | Excelente | Análise rápida |
| 70–79 | 🟡 | Muito boa | Priorizar |
| 60–69 | 🟠 | Interessante | Monitorar/analisar |
| 50–59 | ⚪ | Especulativa | Baixa prioridade; só avança com exceção autorizada |
| 0–49 | 🔴 | Fraca | Baixa prioridade |

A ação típica da faixa 50–59 foi corrigida (`D11`). A fonte era internamente contraditória:
uma seção dizia "somente se a estratégia aceitar" e outra dizia `DO NOT BUY`. Como o score
mínimo por estratégia vai de 65 a 75, **nenhuma** estratégia aceita 50–59 pela regra normal;
o único caminho é exceção autorizada, e `R55.7` continua emitindo `DO_NOT_BUY` para score
abaixo de 60.

**`SCORE-004` — Score mínimo por estratégia** `[DEFAULT]`

| Estratégia | Score mínimo |
|------------|--------------|
| revenda | 75 |
| renda | 70 |
| mcmv | 65 |
| valorizacao | 65 |
| terreno | 65 |
| customizada | `GLB-004` |

**`SCORE-006` — Pesos do Investor Fit Score** `[DEFAULT]` — sete componentes (`D21`)

Liquidez versus necessidade, horizonte e esforço operacional estavam ausentes. O componente
`qualidade economica` presente na fonte foi **excluído**: ele é o Opportunity Score e
incluí-lo no Fit violaria a separação obrigatória entre os dois scores. Os pesos da fonte
foram renormalizados sobre os sete componentes restantes.

| Componente | Peso |
|------------|------|
| `aderencia_estrategia` | 0,27 |
| `aderencia_risco` | 0,20 |
| `liquidez_vs_necessidade` | 0,13 |
| `aderencia_capital` | 0,13 |
| `diversificacao` | 0,13 |
| `esforco_operacional` | 0,07 |
| `horizonte` | 0,07 |
| **Total** | **1,00** |

`investor_fit_minimo` = 60 `[DEFAULT]` (`SCORE-007`)

**`SCORE-008` — Score composto de prioridade** `[CANÔNICO]` (`D23`)

`score_prioridade = Opportunity Score × fator de confiança × fator de Investor Fit × ajuste de capital × ajuste de portfólio`

Cinco fatores. O `ajuste de portfólio` cobre o bônus de equilíbrio entre estratégias e a
penalização por capital imobilizado. **Concentração e diversificação entram apenas pelo
componente `diversificacao` do Investor Fit**, e não também no ajuste de portfólio: contá-las
nos dois lugares penalizaria a mesma característica duas vezes. Essa escolha fica registrada
aqui porque é a única forma de manter a decomposição do score auditável.

**`SCORE-009` — Escalas de prioridade** `[CANÔNICO]` (`D24`)

Duas escalas coexistiam com rótulos concorrentes (`P1`–`P5` para atratividade e `P0`–`P4`
para urgência). A escala de atratividade foi renomeada para `A1`–`A5`, eliminando a colisão.

| Escala | Significado | Valores |
|--------|-------------|---------|
| Urgência | Janela de tempo e criticidade do evento | `P0` · `P1` · `P2` · `P3` · `P4` · `BLOCK` |
| Atratividade combinada | Atratividade com aderência e capital | `A1` · `A2` · `A3` · `A4` · `A5` |

Disparadores de `P0`: janela curta de certame; evento crítico; **oportunidade excepcional**.
O terceiro disparador constava da fonte e estava ausente desta spec.

### STR — Thresholds por Estratégia `[CANÔNICO]` (valores `[DEFAULT]`)

| Estratégia | `desconto_liquido_min` | `margem_min` | `yield_liquido_mensal_min` | `liquidez_min` | `prazo_saida_max` | `ticket_max` |
|------------|------------------------|--------------|----------------------------|----------------|-------------------|--------------|
| revenda | 0,25 | 0,20 | — | 75 | 180 dias | 400.000 |
| renda | 0,15 | 0,15 | 0,0080 | 70 | — | 300.000 |
| valorizacao | 0,15 | 0,15 | — | 60 `[DEFAULT-DERIVADO]` | — | `INV-002` |
| mcmv | 0,20 | 0,15 | 0,0080 | 70 | 180 dias | `INV-002` |
| terreno | 0,20 | 0,20 | — | 50 `[DEFAULT-DERIVADO]` | 365 dias | `INV-002` |
| customizada | configurável | configurável | configurável | configurável | configurável | configurável |

`liquidez_min` de `valorizacao` e `terreno` é derivado: os três valores documentados são
revenda 75, renda 70 e mcmv 70; a hierarquia relativa anterior era `valorizacao = renda − 10`
e `terreno = renda − 20`, o que produz 60 e 50 (`D7`).

`ticket_max` por estratégia prevalece sobre `INV-002` quando declarado, por `P-C`. `INV-002`
de R$ 250.000 é o default do perfil, aplicável quando a estratégia não declara ticket (`D41`).

**Parâmetros próprios de cada estratégia** `[DEFAULT]` (`D42`) — antes tratados como
critérios de avaliação sem parâmetro correspondente.

| Estratégia | Parâmetro próprio | Valor default |
|------------|-------------------|---------------|
| renda | `reforma_maxima_nivel` | 2 |
| renda | `prazo_maximo_estabilizacao_dias` | 180 |
| renda | `concentracao_maxima_por_regiao` | 0,40 |
| revenda | `custo_maximo_reforma` | 0,10 × valor de mercado provável |
| revenda | `capital_maximo_por_operacao` | `INV-015` |
| valorizacao | `horizonte_minimo_meses` | 36 |
| valorizacao | `tolerancia_capital_imobilizado` | alta |
| mcmv | `custo_maximo_reforma` | 0,08 × valor de mercado provável |
| mcmv | `potencial_revenda_minimo` | aderência ≥ 60 |
| terreno | `capital_imobilizado_maximo` | 0,20 do capital destinado a imóveis |

### PORT — Portfólio e Alocação `[CANÔNICO]` (extensão desta spec, `D41`)

| ID | Parâmetro | Valor default | Status |
|----|-----------|---------------|--------|
| PORT-001 | `alocacao_alvo_por_estrategia` | revenda 0,40 · renda 0,40 · valorizacao 0,10 · mcmv 0,05 · terreno 0,05 | `[DEFAULT]` |
| PORT-002 | `desvio_maximo_da_alocacao_alvo` | 0,15 | `[DEFAULT]` |
| PORT-003 | `limite_concentracao_por_dimensao` | localização 0,40 · tipo 0,50 · estratégia `PORT-001` + `PORT-002` · faixa de ticket 0,50 · fonte 0,70 · nível de risco 0,30 | `[DEFAULT]` |
| PORT-004 | `capital_imobilizado_maximo` | 0,70 do capital destinado a imóveis | `[DEFAULT]` |
| PORT-005 | `bonus_equilibrio_estrategias` | +0,05 no ajuste de portfólio quando a operação reduz o desvio de `PORT-001` | `[DEFAULT]` |
| PORT-006 | `penalidade_capital_imobilizado` | −0,10 no ajuste de portfólio quando `PORT-004` é excedido | `[DEFAULT]` |
| PORT-007 | `faixas_de_acao_por_posicao` | Top 1–3 due diligence completa · 4–10 análise aprofundada · 11–30 monitoramento ativo · demais monitoramento passivo · `BLOCK` fora do ranking | `[CANÔNICO]` |
| PORT-008 | `ordem_de_desempate_por_estrategia` | configurável; default na ordem de `R52.4` | `[DEFAULT]` |

Sem `PORT-001` e `PORT-002` não há como medir desvio de alocação nem aplicar o bônus de
equilíbrio de `SCORE-008`.

### EXC — Exceções

| ID | Parâmetro | Obrigatoriedade |
|----|-----------|-----------------|
| EXC-001 | `regra_excepcionada` | obrigatório |
| EXC-002 | `prazo_de_validade` | obrigatório |
| EXC-003 | `justificativa` | obrigatório |
| EXC-004 | `evidencia` | obrigatório |
| EXC-005 | `alcada_de_aprovacao` | obrigatório |
| EXC-006 | `impacto_no_score` | obrigatório |
| EXC-007 | `reavaliacao_automatica_ao_expirar` | obrigatório |
| EXC-008 | `valor_normal` e `valor_excepcional` | obrigatório |
| EXC-009 | `risco_aceito` | obrigatório |

### ALT — Alertas

| ID | Evento | Gatilho default | Prioridade |
|----|--------|-----------------|------------|
| ALT-001 | Nova oportunidade relevante | score ≥ `GLB-004` e sem BLOCK | Alta |
| ALT-002 | Queda de preço | queda ≥ 0,10 do preço vigente | Alta |
| ALT-003 | Score cruzou limiar | cruzou 70 ou 80 | Média/Alta |
| ALT-004 | Valuation alterado materialmente | variação ≥ 0,05 do valor base | Média/Alta |
| ALT-005 | Novo risco crítico | severidade `critico` | Crítica |
| ALT-006 | Risco resolvido | risco encerrado com evidência | Média |
| ALT-007 | Condição de compra atingida | condição objetiva de `BUY_IF` satisfeita | Alta |
| ALT-008 | Oportunidade ou evidência vencendo | dentro de 20% do prazo de frescor restante | Média |
| ALT-009 | Status do certame alterado | mudança de data, praça, plataforma ou valor mínimo | Média |
| ALT-010 | Reavaliação por evento material | qualquer evento material registrado (`MON-001` a `MON-016`) | Média |
| ALT-011 | Reserva mínima comprometida | capital livre < `INV-005` | Crítica |
| ALT-012 | Parâmetro ou regra alterada | publicação de nova versão vigente | Informativa |
| ALT-013 | Entrou no Top 3 / Top 10 | mudança de faixa de ranking | Alta |
| ALT-014 | Caiu 20 ou mais posições | deterioração material | Média |
| ALT-015 | Alerta de aprendizado | regra com falso positivo acima do limiar | Informativa |
| ALT-016 | Pendência vencida | prazo da pendência ultrapassado | Média |
| ALT-017 | Subiu 20 ou mais posições | melhoria material de ranking | Alta |
| ALT-018 | Saiu do Top 10 | deterioração de faixa de ranking | Média |
| ALT-019 | Passou a `BLOCK` | decisão vigente mudou para `BLOCK` | Crítica |
| ALT-020 | Revalidação registral devida | 30 dias desde a última certidão de matrícula (`D48`) | Alta |

`frequencia_maxima_por_oportunidade` = 3 alertas/dia `[DEFAULT]`
`agrupar_alertas_relacionados` = sim `[CANÔNICO]`

### MON — Monitoramento e Materialidade

| ID | Gatilho | Limiar de materialidade default | Ação |
|----|---------|---------------------------------|------|
| MON-001 | Mudança de preço | ≥ 0,05 | Recalcular economia, score e ranking |
| MON-002 | Mudança de status/praça | qualquer | Reavaliar elegibilidade e workflow |
| MON-003 | Novo comparável relevante | qualidade ≥ C e dentro do raio/janela | Atualizar valuation |
| MON-004 | Novo risco | qualquer | Recalcular risco e decisão |
| MON-005 | Mudança de aluguel | ≥ 0,05 | Atualizar yield |
| MON-006 | Mudança de estratégia ativa | qualquer | Recalcular Fit e ranking |
| MON-007 | Regra ou parâmetro alterado | qualquer | Reprocessar conforme vigência |
| MON-008 | Evidência vencida | prazo FRESH excedido | Reduzir confiança e gerar pendência |
| MON-009 | Mudança de capital disponível | ≥ 0,10 | Recalcular prioridade e ranking |
| MON-010 | Mudança de liquidez | ≥ 10 pontos | Recalcular score e margem exigida |
| MON-011 | **Pendência resolvida** | qualquer | Recalcular confiança, score e ranking (`D39`) |
| MON-012 | Oferta concorrente aumenta | ≥ 0,20 na quantidade de concorrentes | Reduzir liquidez; recalcular prazo e preço de saída |
| MON-013 | Preços de venda da região caem | ≥ 0,05 na mediana de preço por m² | Recalcular valuation, desconto e margem |
| MON-014 | Aluguéis da região sobem | ≥ 0,05 no aluguel de referência | Recalcular yield e aderência à renda |
| MON-015 | Condições de financiamento melhoram ou pioram | qualquer mudança material de taxa, prazo ou elegibilidade | Recalcular liquidez, financiabilidade e público-alvo |
| MON-016 | Infraestrutura da região melhora, ou entra nova concorrência forte | qualquer | Recalcular localização, liquidez e valorização |
| MON-017 | Nova oportunidade excepcional entra no universo | `PRI-007` satisfeito e sem `BLOCK` | Recomparar a carteira e o ranking (`D39`) |

`MON-011` é o gatilho mais frequente da due diligence e estava ausente: sem ele, resolver
uma pendência não recalculava a confiança nem devolvia a oportunidade ao ranking.

---

## Requirements

**Requisitos** — organizados por domínio funcional. A numeração dos requisitos é
contínua e estável: `Requisito N.M` identifica o critério de aceitação `M` do
requisito `N` em todo o documento, nos anexos e nas propriedades de correção.

### Domínio A — Fontes, Captura e Normalização

### Requirement 1: Gestão de fontes independentes

**User Story:** Como investidor, quero que a origem do imóvel seja apenas um atributo, para que novas instituições sejam incorporadas sem redefinir o produto.

#### Acceptance Criteria

1. THE Radar SHALL manter cada fonte como entidade própria com tipo, nome, URL, abrangência geográfica, periodicidade esperada, campos disponíveis, confiabilidade histórica de 0 a 100, situação ativa ou inativa e data da última captura.
2. WHEN uma nova fonte é cadastrada, THE Radar SHALL aplicar a esta fonte o mesmo modelo conceitual de Captura, Imóvel, Oportunidade e Análise já vigente.
3. THE Radar SHALL aceitar fontes dos tipos instituição vendedora, leiloeiro, portal imobiliário, cartório ou registro público, condomínio, pesquisa de mercado, visita física e entrada manual do analista.
4. WHERE a fonte é uma entrada manual do analista, THE Radar SHALL marcar a informação resultante como interpretação e registrar o autor.
5. THE Radar SHALL atribuir a cada fonte uma confiabilidade por categoria de dado, conforme a hierarquia: nível A confirmado, B forte, C indicado, D estimado, E incerto, U desconhecido.
6. IF uma fonte está inativa, THEN THE Radar SHALL preservar as capturas já registradas por esta fonte e interromper novas capturas desta fonte.

### Requirement 2: Preservação da captura original

**User Story:** Como auditor, quero que o dado original da fonte seja preservado intacto, para que qualquer conclusão seja rastreável até a origem.

#### Acceptance Criteria

1. WHEN uma oferta é capturada de uma fonte, THE Capturador SHALL armazenar o payload bruto sem alteração, junto com tipo de fonte, nome da fonte, identificador da publicação, referência ou URL, e data e hora da captura.
2. WHEN uma captura é registrada, THE Capturador SHALL calcular um fingerprint estável do conteúdo, independente da ordem das chaves do payload.
3. IF duas capturas da mesma fonte possuem o mesmo fingerprint, THEN THE Capturador SHALL tratar as duas como a mesma captura e manter um único registro.
4. THE Capturador SHALL preservar toda captura registrada de forma imutável, sem sobrescrita e sem exclusão.
5. WHEN uma correção posterior é necessária, THE Capturador SHALL registrar uma nova captura e manter a captura anterior consultável com estado `Superseded`.
6. WHEN a captura contém referências a imagens ou documentos, THE Capturador SHALL preservar estas referências com a data de observação.
7. THE Capturador SHALL registrar o preço e o status exatamente como informados pela fonte, além das versões normalizadas.

### Requirement 3: Normalização sem invenção de dados

**User Story:** Como analista, quero que campos ausentes permaneçam explicitamente desconhecidos, para não confundir ausência de informação com informação favorável.

#### Acceptance Criteria

1. WHEN uma captura é normalizada, THE Normalizador SHALL extrair identificação, localização, características físicas, dados do certame, condições comerciais e situação de ocupação.
2. IF um campo não está presente ou não é interpretável com segurança, THEN THE Normalizador SHALL registrar este campo como `UNKNOWN` e SHALL preservar o valor original quando existir.
3. THE Normalizador SHALL manter o valor original de cada campo junto do valor normalizado.
4. WHEN valores monetários, áreas, percentuais e datas vêm em formato brasileiro, THE Normalizador SHALL interpretá-los corretamente, incluindo os formatos `R$ 191.651,31`, `47,76 m²`, `5%` e `15/09/2026 10:00`.
4.1. THE Normalizador SHALL interpretar o mesmo número com a mesma magnitude em qualquer notação aceita, incluindo `1.234,56` com ponto de milhar, `1234,56` sem separador de milhar e `1234.56` com ponto decimal, e SHALL abster-se de tratar o ponto como separador de milhar quando ele é o único separador presente e é seguido por uma ou duas casas.
4.2. THE Normalizador SHALL exigir que a unidade de percentual venha declarada na entrada, distinguindo fração de porcentagem, e SHALL abster-se de inferir a unidade pela magnitude do valor.
4.3. THE Normalizador SHALL interpretar percentuais com casas decimais, incluindo `2,5%` que corresponde a `0,025`.
4.4. IF um valor numérico não é interpretável sem ambiguidade, THEN THE Normalizador SHALL registrá-lo como `UNKNOWN` e SHALL abster-se de retornar zero.
5. WHEN uma área é extraída, THE Normalizador SHALL registrar também o tipo de área entre privativa, comum, total e terreno, e SHALL marcar o tipo como `UNKNOWN` quando a fonte não o declarar.
6. THE Normalizador SHALL mapear o tipo de imóvel para a taxonomia do Radar, com os grupos apartamento, casa, sobrado, terreno, comercial, rural e outros, e SHALL usar o valor `desconhecido` quando a evidência for insuficiente.
7. THE Normalizador SHALL mapear o status da oferta para um estado padronizado do Radar e SHALL preservar o texto original do status.
8. WHEN a fonte indica situação de ocupação, THE Normalizador SHALL distinguir `ocupado`, `desocupado` e `desconhecido` sem ambiguidade de correspondência parcial de texto.
9. WHEN a normalização termina, THE Normalizador SHALL disponibilizar a lista de campos relevantes ausentes para alimentar as pendências.
10. THE Normalizador SHALL tratar o valor de avaliação informado pela fonte como referência informativa e SHALL registrar este valor em campo distinto do valor de mercado.
11. THE Normalizador SHALL persistir a oferta normalizada vinculada à captura de origem, de forma que a normalização vigente na data da análise seja reproduzível.

### Requirement 4: Dados mínimos e gates de dados

**User Story:** Como investidor, quero que o Radar declare o que falta antes de recomendar, para não receber recomendações baseadas em lacunas.

#### Acceptance Criteria

1. THE Radar SHALL exigir, para o gate `G0` de captura, a presença de fonte, data e hora da captura, identificação mínima do imóvel, preço e status.
2. THE Radar SHALL exigir, para o gate `G1` de qualificação, a presença de localização em nível de município e bairro ou região, tipo de imóvel e área conhecida ou explicitamente `UNKNOWN`.
3. THE Radar SHALL exigir, para o gate `G2` de mercado, evidência suficiente para estimar valor conforme `VAL-001` ou a declaração explícita de insuficiência.
4. THE Radar SHALL exigir, para o gate `G3` de economia, o custo econômico total com os componentes conhecidos calculados e os desconhecidos explicitamente identificados.
5. THE Radar SHALL exigir, para o gate `G4` de estratégia, aderência a pelo menos uma estratégia ativa.
6. THE Radar SHALL exigir, para o gate `G5` de risco, a ausência de bloqueio crítico conhecido.
7. THE Radar SHALL exigir, para o gate `G6` de recomendação, score, confiança consolidada e explicação disponíveis.
8. THE Radar SHALL exigir, para o gate `G7` de compra, a resolução de todas as pendências classificadas como críticas.
9. IF um gate não é satisfeito, THEN THE Radar SHALL interromper a progressão nesse ponto, SHALL registrar o gate não satisfeito e SHALL listar exatamente qual informação falta.
10. IF um dado obrigatório está ausente, THEN THE Radar SHALL classificar o impacto da ausência em baixo, médio, alto ou crítico e SHALL reduzir a confiança da dimensão correspondente.

### Requirement 5: Enriquecimento progressivo

**User Story:** Como investidor, quero que o esforço de investigação seja proporcional ao potencial, para não gastar tempo igual em todas as ofertas.

#### Acceptance Criteria

1. THE Radar SHALL organizar o enriquecimento em nove níveis: nível 0 captura, nível 1 normalização, nível 2 identificação, nível 3 mercado, nível 4 econômico, nível 5 risco, nível 6 estratégia, nível 7 due diligence e nível 8 pós-decisão.
2. THE Radar SHALL classificar o potencial preliminar da oportunidade em exatamente uma faixa qualitativa — `descartavel`, `baixo`, `medio`, `alto` ou `excepcional` — a partir do desconto sobre o valor de referência da fonte, do enquadramento no escopo de localização e tipo, e do enquadramento no ticket, sem depender de score.
3. WHERE o potencial preliminar é `descartavel` OR `baixo`, THE Radar SHALL limitar o enriquecimento aos níveis 0 a 2.
4. WHERE o potencial preliminar é `medio`, THE Radar SHALL executar os níveis 0 a 4.
5. WHERE o potencial preliminar é `alto` OR `excepcional`, THE Radar SHALL executar os níveis 0 a 6.
6. WHERE a oportunidade está entre as três primeiras posições do ranking, THE Radar SHALL executar o nível 7.
7. THE Radar SHALL derivar a profundidade de enriquecimento exclusivamente do potencial preliminar e da posição no ranking, AND SHALL abster-se de derivá-la do Opportunity Score.
8. WHEN cada informação é enriquecida, THE Radar SHALL registrar origem, data de obtenção e nível de confiança desta informação.

### Requirement 6: Conflitos entre fontes

**User Story:** Como analista, quero que divergências entre fontes sejam explicitadas, para que nenhuma escolha silenciosa distorça a análise.

#### Acceptance Criteria

1. WHEN duas fontes informam valores diferentes para o mesmo campo, THE Consolidador_de_Perfil SHALL preservar ambos os valores com suas origens e datas.
2. WHEN a divergência de valor de mercado entre fontes excede `VAL-010`, THE Consolidador_de_Perfil SHALL classificar a divergência como material, SHALL registrar pendência e SHALL reduzir a confiança da dimensão afetada.
3. IF a situação de ocupação informada por fontes distintas é divergente, THEN THE Consolidador_de_Perfil SHALL registrar pendência de prioridade crítica até a confirmação.
4. IF a matrícula informada por fontes distintas é divergente, THEN THE Deduplicador SHALL manter os registros separados e SHALL registrar conflito de identidade.
5. WHEN o status da oferta é divergente, THE Consolidador_de_Perfil SHALL adotar a informação mais recente como vigente, SHALL preservar a anterior no histórico e SHALL gerar evento de mudança de status.
6. THE Consolidador_de_Perfil SHALL escolher o valor vigente apenas para a decisão atual e SHALL manter o histórico completo das divergências.
7. WHEN a divergência é entre fonte oficial e anúncio, THE Consolidador_de_Perfil SHALL priorizar a fonte adequada ao tipo de dado e SHALL registrar o critério de priorização aplicado.

---

### Domínio B — Identidade e Deduplicação

### Requirement 7: Resolução de identidade do imóvel

**User Story:** Como analista, quero saber o quão certo estou de qual imóvel estou analisando, porque analisar o imóvel errado invalida todo o resto.

#### Acceptance Criteria

1. WHEN uma oferta normalizada é avaliada, THE Resolvedor_de_Identidade SHALL classificar a identidade em exatamente um dos cinco níveis: `I0` desconhecida, `I1` candidata, `I2` provável, `I3` confirmada ou `I4` documental.
2. WHERE existe documentação registral que identifique o imóvel acompanhada de contexto registral de comarca ou cartório, THE Resolvedor_de_Identidade SHALL classificar a identidade como `I4`, AND SHALL aceitar como documentação registral a matrícula, a certidão de ônus, a escritura registrada e o ato ou averbação registral que identifique o imóvel.
3. WHERE existe matrícula sem contexto registral, OR existe identificador oficial da fonte acompanhado de endereço completo com unidade, OR existe endereço completo com unidade sem matrícula e sem identificador oficial, THE Resolvedor_de_Identidade SHALL classificar a identidade como no máximo `I3`.
4. WHERE existe endereço completo com área compatível e sem unidade identificada, THE Resolvedor_de_Identidade SHALL classificar a identidade como no máximo `I2`.
5. WHERE existe apenas endereço parcial OR apenas identificador da fonte, THE Resolvedor_de_Identidade SHALL classificar a identidade como `I1`.
6. THE Resolvedor_de_Identidade SHALL considerar como sinais de identidade, em ordem decrescente de força: matrícula com unidade, identificador oficial do imóvel, endereço completo com unidade, condomínio com bloco e unidade e área, endereço com características compatíveis, imagem semelhante, e similaridade de título ou descrição.
7. THE Resolvedor_de_Identidade SHALL atribuir a preço, avaliação da fonte e desconto a força `baixa`, SHALL rejeitar cada um deles como sinal isolado de identidade AND SHALL rejeitar todos eles como sinal de deduplicação.
7.1. THE Resolvedor_de_Identidade SHALL tratar `imagem_semelhante` como sinal complementar de força `media`, utilizável para reforçar ou contestar outros sinais e nunca como sinal isolado de identidade.
8. WHEN a identidade é resolvida, THE Resolvedor_de_Identidade SHALL registrar cada identificador encontrado com o respectivo grau de confiança.
9. IF a identidade é inferior a `I2`, THEN THE Orquestrador SHALL impedir a progressão para a etapa de valuation e SHALL encaminhar a análise diretamente para a decisão.
10. IF a identidade é `I2`, THEN THE Radar SHALL permitir a análise econômica e SHALL reduzir a confiança consolidada, sem liberar a decisão `BUY`.
11. IF não existe matrícula, THEN THE Resolvedor_de_Identidade SHALL registrar pendência exigindo certidão atualizada antes de qualquer liberação de compra.
12. IF existe conflito material entre identificadores, THEN THE Resolvedor_de_Identidade SHALL registrar conflito de identidade e SHALL resultar em `PENDENTE` até a resolução.

### Requirement 8: Chave conceitual de identidade

**User Story:** Como analista, quero que o Radar registre a unidade e o empreendimento, para distinguir apartamentos diferentes no mesmo endereço.

#### Acceptance Criteria

1. THE Normalizador SHALL extrair e registrar, quando disponíveis, os campos empreendimento ou condomínio, torre, bloco, unidade e vaga.
2. THE Resolvedor_de_Identidade SHALL construir a chave conceitual de identidade a partir de uma das combinações: matrícula; identificador oficial da fonte; município com logradouro, número e unidade; condomínio com bloco e unidade.
3. WHERE nenhum identificador forte está disponível, THE Resolvedor_de_Identidade SHALL usar a combinação de endereço, área, quartos e vagas como identidade provável e SHALL marcar o resultado como provável.
4. IF o endereço é conhecido e a unidade é desconhecida, THEN THE Resolvedor_de_Identidade SHALL classificar a identidade como no máximo `I2` e SHALL registrar pendência de identificação da unidade.

### Requirement 9: Deduplicação por força de evidência

**User Story:** Como analista, quero que ofertas do mesmo imóvel sejam reconhecidas como uma só, sem unir imóveis distintos por coincidência.

#### Acceptance Criteria

1. WHEN duas ofertas possuem matrícula, THE Deduplicador SHALL usar a matrícula como evidência decisiva, tratando matrículas iguais como o mesmo imóvel e matrículas distintas como imóveis diferentes.
2. WHERE não existe matrícula e existe o mesmo identificador oficial da mesma fonte, THE Deduplicador SHALL tratar as ofertas como o mesmo imóvel por evidência muito forte.
3. WHERE existem condomínio e unidade iguais, THE Deduplicador SHALL tratar as ofertas como o mesmo imóvel por evidência muito forte.
4. WHERE existe apenas endereço completo igual, THE Deduplicador SHALL exigir compatibilidade de área dentro de `CMP-004` para afirmar identidade, AND SHALL retornar resultado indefinido quando a área divergir ou estiver ausente.
5. THE Deduplicador SHALL tratar preço, avaliação da fonte e desconto como sinais inválidos para deduplicação.
5.1. THE Deduplicador SHALL considerar como sinais complementares parametrizáveis de deduplicação, além dos sinais de identidade: descrição semelhante com peso `fraco`, área próxima dentro de `CMP-004` com peso `medio`, quantidade de quartos igual com peso `medio`, quantidade de vagas igual com peso `fraco`, e imagem semelhante com peso `medio`.
5.2. THE Deduplicador SHALL exigir a combinação de pelo menos dois sinais complementares de peso `medio` para elevar um veredito indefinido a correspondência provável, AND SHALL abster-se de elevar o veredito com base apenas em sinais de peso `fraco`.
6. IF as evidências são insuficientes, THEN THE Deduplicador SHALL retornar resultado indefinido, SHALL criar um imóvel candidato e SHALL manter os registros separados.
7. WHEN uma correspondência é apenas provável, THE Deduplicador SHALL registrar a associação como reversível e SHALL solicitar validação.
8. THE Deduplicador SHALL realizar fusão definitiva apenas quando a evidência é decisiva ou muito forte.
9. WHEN uma associação é desfeita, THE Deduplicador SHALL preservar o histórico da associação anterior e o motivo da correção.
10. WHEN o Deduplicador associa uma captura a um imóvel, THE Deduplicador SHALL registrar quais sinais coincidiram, quais divergiram, quais fontes foram comparadas, o nível de confiança atribuído e se houve validação manual.
11. IF unidades diferentes do mesmo condomínio são avaliadas, THEN THE Deduplicador SHALL tratá-las como imóveis distintos.
12. WHEN uma oferta encerrada é republicada, THE Deduplicador SHALL tentar associá-la ao imóvel histórico existente antes de criar um novo imóvel.

### Requirement 10: Perfil consolidado do imóvel

**User Story:** Como investidor, quero uma visão única e vigente do imóvel, mesmo quando várias fontes o descrevem de formas diferentes.

#### Acceptance Criteria

1. THE Consolidador_de_Perfil SHALL manter, por imóvel, o endereço normalizado, as características físicas, o preço vigente, o histórico de preços, o status vigente, a matrícula, a área com seu tipo, as imagens observadas e a confiança da consolidação.
2. THE Consolidador_de_Perfil SHALL classificar cada campo do perfil em exatamente um tipo de informação: `OBSERVED`, `CONFIRMED`, `CALCULATED`, `ESTIMATED`, `INFERRED` ou `UNKNOWN`.
3. WHEN uma nova captura é associada ao imóvel, THE Consolidador_de_Perfil SHALL atualizar a visão vigente e SHALL preservar a visão anterior no histórico.
4. THE Consolidador_de_Perfil SHALL derivar as características do perfil da fonte de maior confiabilidade para cada categoria de dado e SHALL registrar qual fonte sustentou cada campo.
5. WHEN a fonte de um campo do perfil é uma inferência, THE Consolidador_de_Perfil SHALL marcar o campo como `INFERRED` e SHALL registrar a premissa utilizada.
6. THE Consolidador_de_Perfil SHALL versionar o perfil consolidado com numeração crescente, SHALL registrar em cada versão a data, o autor ou processo, os campos alterados e o motivo, AND SHALL preservar as versões anteriores sem sobrescrita.
7. THE Consolidador_de_Perfil SHALL manter o histórico de preços como série própria, com valor, moeda, data de observação, fonte, tipo de preço entre lance mínimo, preço de venda direta e avaliação da fonte, e a variação em relação à observação anterior.
8. THE Consolidador_de_Perfil SHALL organizar o perfil consolidado nos grupos Identificação, Localização, Físico, Condominial, Ocupacional, Qualidade, Oferta, Documental e Consolidação, com estado de informação por campo em todos os grupos.
9. THE Consolidador_de_Perfil SHALL registrar, no grupo Condominial, o valor do condomínio, a existência de débitos, as obras em curso, a situação da convenção, a existência de portaria e a situação financeira do condomínio quando disponíveis.
10. THE Consolidador_de_Perfil SHALL registrar, no grupo Ocupacional, o estado de ocupação, o ocupante quando identificado, a existência de locação, a origem da posse e as evidências correspondentes.
11. THE Consolidador_de_Perfil SHALL registrar, no grupo Qualidade, o estado de conservação, o nível de reforma estimado, o padrão construtivo e a idade aparente do imóvel.

### Requirement 11: Classificação de localização

**User Story:** Como investidor, quero configurar minhas regiões sem que o Radar assuma que regiões de menor renda são ruins.

#### Acceptance Criteria

1. THE Classificador_de_Localizacao SHALL classificar cada imóvel em exatamente uma classe de localização: `A` prioritária, `B` boa, `C` condicional, `D` indesejada ou `E` bloqueada.
2. THE Classificador_de_Localizacao SHALL derivar a classe exclusivamente dos parâmetros `LOC-001` a `LOC-013` vigentes, sem valores fixos por bairro embutidos no produto.
3. WHERE a localização é classe `E`, THE Motor_de_Decisao SHALL emitir `DO_NOT_BUY` pela camada de elegibilidade para todas as estratégias.
4. WHERE a localização é classe `C`, THE Motor_de_Estrategia SHALL exigir desconto líquido igual ou superior a `LOC-013` para considerar a oportunidade aderente.
5. WHERE a localização é classe `D`, THE Motor_de_Estrategia SHALL considerar a oportunidade aderente apenas sob exceção autorizada registrada.
6. THE Classificador_de_Localizacao SHALL avaliar segurança, serviços, comércio, transporte, acesso, infraestrutura, perfil de demanda, faixa de preço predominante e liquidez regional como dimensões independentes.
7. THE Classificador_de_Localizacao SHALL tratar perfil socioeconômico da região como dimensão informativa e SHALL manter esta dimensão separada das dimensões de liquidez, risco e qualidade.
8. IF um único indicador de localização é desfavorável, THEN THE Classificador_de_Localizacao SHALL reduzir a pontuação da dimensão correspondente e SHALL manter a oportunidade elegível.

---

### Domínio C — Gate de Validade Jurídica (Camada P0)

### Requirement 12: Precedência absoluta do gate jurídico

**User Story:** Como investidor, quero que oportunidades juridicamente inexecutáveis sejam bloqueadas antes de eu ver qualquer desconto atraente.

#### Acceptance Criteria

1. WHEN uma análise é executada, THE Orquestrador SHALL executar o Gate_Juridico antes de calcular valuation, custo econômico, desconto, margem, yield, liquidez ou score.
2. IF o Gate_Juridico retorna `BLOCK`, THEN THE Orquestrador SHALL desviar diretamente para a decisão, sem executar as etapas de mercado, economia, liquidez, estratégia e score.
3. THE Motor_de_Decisao SHALL manter a decisão `BLOCK` independentemente do valor de score, desconto, margem, yield, liquidez, Investor Fit ou eficiência de capital.
4. WHEN o Gate_Juridico retorna `BLOCK`, THE Motor_de_Risco SHALL registrar risco de categoria jurídica com severidade `critico`.
5. THE Gate_Juridico SHALL classificar o resultado da camada P0 em exatamente um dos estados: `REGULAR_COMPROVADO`, `PENDENTE`, `RISCO_JURIDICO`, `BLOCK` ou `INCONCLUSIVO`.
6. THE Gate_Juridico SHALL mapear `REGULAR_COMPROVADO` para `legal_status = OK`, `PENDENTE` e `INCONCLUSIVO` para `legal_status = PENDENTE`, e `BLOCK` para `legal_status = BLOCK`.
7. WHERE o resultado da camada P0 é `RISCO_JURIDICO`, THE Motor_de_Decisao SHALL emitir `BUY_IF`, `MONITOR` ou `BLOCK` conforme o impacto e a possibilidade de saneamento registrados.
8. IF o `legal_status` é `PENDENTE`, THEN THE Motor_de_Decisao SHALL impedir a decisão `BUY` e SHALL permitir no máximo `BUY_IF` ou `MONITOR`.
9. THE Gate_Juridico SHALL avaliar exatamente **19 verificações**: as treze verificações `RULE-JUR-001` a `RULE-JUR-013`, as quatro verificações `RULE-ED-001` a `RULE-ED-004`, e as duas verificações de identidade e registro `RULE-ID-001` e `RULE-ID-002`.
10. THE Gate_Juridico SHALL abster-se de avaliar `RULE-OCC-001`, `RULE-OCC-002`, `RULE-LOC-001` e `RULE-LOC-002` como parte do gate, AND THE Motor_de_Risco SHALL avaliá-las na camada 6 de risco.
11. THE Gate_Juridico SHALL registrar, para cada uma das 19 verificações, o resultado, a evidência, a localização documental e a regra de origem.

**Crosswalk do gate de validade jurídica** `[CANÔNICO]` (`D16`). A fonte de origem enunciava
o gate em seis itens `GATE-JUR-*`; esta spec o executa pelas regras canônicas. O mapa abaixo
torna a correspondência explícita e verificável.

| Item de origem | Objeto | Regras canônicas correspondentes | Camada |
|----------------|--------|----------------------------------|--------|
| `GATE-JUR-001` | Consolidação da propriedade | `RULE-JUR-002`, `RULE-JUR-013` | 1 |
| `GATE-JUR-002` | Constituição em mora e notificação | `RULE-JUR-003`, `RULE-JUR-004` | 1 |
| `GATE-JUR-003` | Intimações relativas aos leilões | `RULE-JUR-005` | 1 |
| `GATE-JUR-004` | Edital, cronologia e coerência | `RULE-ED-001`, `RULE-JUR-006` | 1 |
| `GATE-JUR-005` | Processos judiciais | `RULE-JUR-007` | 1 |
| `GATE-JUR-006` | Ocupação e locação | `RULE-OCC-001`, `RULE-OCC-002`, `RULE-LOC-001`, `RULE-LOC-002` | **6 — risco, não gate** |

A família `RULE-REG-001` a `RULE-REG-004`, citada em versões anteriores desta spec como se
integrasse o gate, **não existe em nenhuma fonte** e foi removida. As verificações registrais
estão em `RULE-ID-002`, `RULE-JUR-012`, `RULE-JUR-013` e `RULE-ED-004` (`D16`).

### Requirement 13: Verificações registrais e de titularidade

**User Story:** Como investidor, quero que a cadeia registral seja comprovada documentalmente, porque o anúncio da CAIXA não prova a regularidade do procedimento.

#### Acceptance Criteria

1. THE Gate_Juridico SHALL verificar a existência de matrícula atualizada, identificando o proprietário atual, os atos relevantes e a data de emissão da certidão.
2. IF a matrícula está ausente, THEN THE Gate_Juridico SHALL retornar `PENDENTE` para a verificação `RULE-ID-002` e SHALL registrar pendência de obtenção de certidão atualizada.
3. THE Gate_Juridico SHALL tratar a certidão de matrícula como válida até que exista mudança registral ou evidência nova, AND SHALL exigir revalidação registral antes de qualquer decisão de compra.
3.1. WHEN 30 dias se passam desde a emissão da certidão de matrícula vigente, THE Gestor_de_Alertas SHALL emitir o alerta `ALT-020` de revalidação registral devida.
3.2. IF a revalidação registral exigida pelo critério 3 não foi realizada, THEN THE Motor_de_Decisao SHALL impedir a decisão `BUY` e SHALL registrar pendência de prioridade `critica`.
4. IF existe conflito material entre a titularidade da matrícula e a titularidade declarada na oferta, THEN THE Gate_Juridico SHALL retornar `BLOCK`.
5. THE Gate_Juridico SHALL identificar o contrato de alienação fiduciária e o credor fiduciário, e SHALL verificar o registro do contrato na matrícula.
6. THE Gate_Juridico SHALL verificar a averbação da consolidação da propriedade em nome do credor fiduciário, registrando a data do ato, o número do ato ou averbação e o texto integral do ato quando disponível.
7. IF a consolidação exigida para a modalidade analisada não está comprovada na matrícula, THEN THE Gate_Juridico SHALL impedir a decisão `BUY` e SHALL retornar `PENDENTE` ou `BLOCK` conforme a fase do procedimento.
8. WHEN o texto do ato de consolidação está disponível, THE Gate_Juridico SHALL extrair as declarações sobre intimação e sobre ausência de purgação da mora e SHALL registrá-las como evidência com localização exata no documento.
9. WHEN a consolidação é comprovada, THE Gate_Juridico SHALL registrar que o ato registral está comprovado na data correspondente AND SHALL manter como `UNKNOWN` os fatos posteriores não verificados.
10. THE Gate_Juridico SHALL identificar ônus, averbações, gravames e restrições vigentes na matrícula e SHALL distinguir gravame histórico já baixado de gravame atual.
11. IF existe penhora, indisponibilidade ou arresto vigente que impeça a transferência, THEN THE Gate_Juridico SHALL retornar `BLOCK`.
12. WHERE a averbação dos leilões negativos consta com situação `em tratamento` ou equivalente, THE Gate_Juridico SHALL classificar o item como pendência registral, SHALL reduzir a confiança jurídica, SHALL incorporar o custo e o prazo de regularização ao custo econômico total AND SHALL abster-se de retornar `BLOCK` apenas por esta situação.
13. THE Gate_Juridico SHALL registrar a situação da averbação dos leilões negativos em exatamente um de quatro estados: `averbado`, `em_tratamento`, `nao_se_aplica` ou `desconhecido`.
14. IF a vaga de garagem possui matrícula autônoma e a abrangência da oferta sobre esta vaga é indeterminada, THEN THE Gate_Juridico SHALL retornar `PENDENTE` para a verificação registral da vaga.

### Requirement 14: Constituição em mora e intimações

**User Story:** Como investidor, quero que a cadeia de notificações seja verificada no caso concreto, para não arrematar um procedimento anulável.

#### Acceptance Criteria

1. THE Gate_Juridico SHALL identificar o devedor fiduciante e SHALL verificar a existência do ato de constituição em mora, registrando data, destinatário, meio e endereço utilizados.
2. IF o ato de constituição em mora não é localizado, THEN THE Gate_Juridico SHALL retornar `PENDENTE` e SHALL registrar risco jurídico de severidade `alto`.
3. IF existe irregularidade material comprovada na constituição em mora, THEN THE Gate_Juridico SHALL retornar `BLOCK`.
4. THE Gate_Juridico SHALL verificar a intimação para purgação da mora, registrando modalidade, destinatário, endereço, data, comprovação de recebimento ou recusa, prazo legal aplicável e eventual intimação subsidiária por edital.
5. WHEN a intimação pessoal não é comprovada, THE Gate_Juridico SHALL verificar a existência de intimação por edital e SHALL registrar o resultado desta verificação.
6. IF o conjunto de evidências sobre a intimação para purgação da mora é inconclusivo, THEN THE Gate_Juridico SHALL retornar `PENDENTE`.
7. THE Gate_Juridico SHALL verificar as comunicações legalmente exigíveis sobre as datas dos leilões aplicáveis ao caso concreto, registrando datas, destinatários e comprovantes.
8. IF a comunicação sobre as datas dos leilões não possui evidência, THEN THE Gate_Juridico SHALL retornar `PENDENTE`.
9. IF a comunicação sobre as datas dos leilões apresenta irregularidade material comprovada, THEN THE Gate_Juridico SHALL retornar `BLOCK`.
10. THE Gate_Juridico SHALL avaliar a exigibilidade de cada intimação conforme a modalidade do procedimento e o caso concreto, sem presumir exigência ou dispensa.

### Requirement 15: Edital, cronologia e coerência do certame

**User Story:** Como investidor, quero que o edital seja lido integralmente e confrontado com a matrícula, porque o edital define as obrigações que eu assumo.

#### Acceptance Criteria

1. THE Gate_Juridico SHALL exigir o edital oficial vigente, registrando número, versão, data e fingerprint do documento.
2. IF o edital oficial não está disponível, THEN THE Gate_Juridico SHALL retornar `PENDENTE`.
3. THE Gate_Juridico SHALL extrair do edital o primeiro leilão, o segundo leilão quando aplicável, datas, horários, plataforma, valor mínimo de cada praça, comissão do leiloeiro, forma e prazo de pagamento, e o resultado das praças já realizadas.
4. THE Gate_Juridico SHALL verificar a coerência cronológica entre constituição em mora, consolidação da propriedade e datas dos leilões.
5. IF a cronologia apresenta conflito material com a modalidade ou com os documentos, THEN THE Gate_Juridico SHALL retornar `BLOCK` ou `PENDENTE` conforme a natureza do conflito e SHALL registrar a inconsistência como evidência.
6. IF a matrícula e o edital apresentam conflito material sobre identificação, área, unidade ou titularidade, THEN THE Gate_Juridico SHALL retornar `BLOCK`.
7. IF existe divergência entre a data, o horário, a plataforma, o leiloeiro ou o valor mínimo informados pelo portal da fonte e os informados no edital, THEN THE Gate_Juridico SHALL retornar `PENDENTE` e SHALL registrar a divergência com as duas informações e suas origens.
8. THE Gate_Juridico SHALL extrair do edital a cláusula de responsabilidade por evicção de direito e SHALL registrar o item e a página em que a cláusula consta.
9. IF o edital foi obtido AND o edital comprovadamente não contém cláusula de garantia contra evicção, THEN THE Gate_Juridico SHALL retornar `BLOCK` e THE Radar SHALL impedir a liberação de lance.
9.1. IF o edital não foi obtido, OR a cláusula de garantia contra evicção não foi verificada, THEN THE Gate_Juridico SHALL retornar `PENDENTE`, THE Motor_de_Decisao SHALL impedir a decisão `BUY` AND THE Radar SHALL impedir a liberação de lance.
9.2. THE Radar SHALL distinguir, no registro e na explicação, a ausência comprovada de cláusula, que é evidência de ausência e produz `BLOCK`, da não verificação da cláusula, que é ausência de evidência e produz `PENDENTE`.
10. WHEN a cláusula de evicção apresenta exclusões, ressalvas ou limitações, THE Gate_Juridico SHALL registrar cada limitação e THE Motor_de_Risco SHALL elevar o risco jurídico e a contingência correspondente.
11. THE Gate_Juridico SHALL extrair do edital a responsabilidade por débitos anteriores de condomínio, IPTU e demais encargos.
12. IF a responsabilidade por um débito anterior não é determinável a partir do edital, THEN THE Motor_de_Calculo SHALL criar contingência para o valor estimado deste débito AND THE Gate_Juridico SHALL registrar pendência.
13. THE Gate_Juridico SHALL registrar as regras específicas do edital que alterem custo, prazo, posse ou obrigações do arrematante.

### Requirement 16: Processos judiciais e risco de nulidade

**User Story:** Como investidor, quero que processos sejam avaliados pelo impacto real, para não descartar boas oportunidades nem ignorar riscos verdadeiros.

#### Acceptance Criteria

1. THE Gate_Juridico SHALL pesquisar processos relacionados ao imóvel, à matrícula, ao devedor fiduciante e ao procedimento de execução.
2. WHEN um processo é identificado, THE Gate_Juridico SHALL registrar número, tribunal, comarca, partes, polo, objeto, pedidos, decisões, liminares e tutelas, fase atual, última movimentação e valor envolvido quando disponível.
3. THE Gate_Juridico SHALL classificar o impacto de cada processo sobre a validade do procedimento em `nenhum`, `potencial`, `material_mitigavel` ou `material_impeditivo`.
4. IF o impacto classificado é `material_impeditivo` sem mitigação comprovada, THEN THE Gate_Juridico SHALL retornar `BLOCK`.
5. IF o impacto classificado é `potencial` ou `material_mitigavel`, THEN THE Gate_Juridico SHALL retornar `RISCO_JURIDICO` e SHALL registrar a condição de mitigação.
6. THE Gate_Juridico SHALL abster-se de retornar `BLOCK` com base apenas na existência de um processo.
7. THE Gate_Juridico SHALL pesquisar especificamente ações anulatórias e ações de sustação do leilão anteriores à data do certame.
8. IF existe decisão liminar que atinge o leilão ou o procedimento, THEN THE Gate_Juridico SHALL retornar `BLOCK` até a resolução ou a mitigação comprovada.

### Requirement 17: Sinais jurídicos de investigação obrigatória

**User Story:** Como investidor, quero que sinais historicamente associados a nulidade sejam investigados, sem que virem bloqueio automático.

#### Acceptance Criteria

1. WHEN o percentual quitado do contrato de alienação fiduciária é igual ou superior a 0,80, THE Gate_Juridico SHALL registrar sinal de investigação jurídica específica, SHALL registrar risco jurídico de severidade `alto` AND SHALL abster-se de retornar `BLOCK` apenas por este percentual.
2. WHEN o imóvel residencial de pessoa física foi oferecido em garantia de dívida de terceiro, THE Gate_Juridico SHALL registrar sinal de investigação jurídica específica e SHALL retornar `PENDENTE` ou `BLOCK` conforme a evidência do caso concreto.
3. WHEN o valor mínimo do segundo leilão é inferior a 0,50 do valor de avaliação, THE Gate_Juridico SHALL emitir alerta jurídico, SHALL exigir validação da modalidade e da norma vigente, SHALL reduzir a confiança jurídica AND SHALL abster-se de retornar `BLOCK` apenas por este percentual.
4. WHEN os direitos do devedor fiduciante foram penhorados ou tornados indisponíveis, THE Gate_Juridico SHALL avaliar se a constrição impede ou dificulta a transferência e SHALL retornar `BLOCK` quando a constrição for impeditiva.
5. THE Gate_Juridico SHALL registrar cada sinal de investigação como evidência com proveniência, estado e localização documental.

### Requirement 18: Ocupação e posse como risco econômico

**User Story:** Como investidor, quero que ocupação seja tratada como custo e prazo, não como impedimento jurídico, para não descartar boas oportunidades.

#### Acceptance Criteria

1. THE Gate_Juridico SHALL determinar a situação de ocupação em exatamente um dos sete estados: `desocupado_confirmado`, `livre_nao_confirmado`, `ocupado_pelo_devedor`, `ocupado_por_terceiro`, `ocupado_por_inquilino`, `posse_litigiosa` ou `desconhecido`.
2. IF o imóvel está ocupado, THEN THE Motor_de_Risco SHALL registrar risco de posse de severidade `alto` AND THE Gate_Juridico SHALL abster-se de tratar a ocupação como nulidade do procedimento.
2.1. IF a ocupação possui impacto classificado como crítico AND não existe estratégia de desocupação registrada, THEN THE Motor_de_Risco SHALL registrar severidade `critico` e THE Motor_de_Decisao SHALL emitir `BLOCK` pela camada 0.
2.2. IF a situação de ocupação é `posse_litigiosa` AND existe evidência de litígio sobre a posse, THEN THE Motor_de_Risco SHALL registrar severidade `critico` e THE Motor_de_Decisao SHALL emitir `BLOCK` pela camada 0.
2.3. WHERE a situação de ocupação é `livre_nao_confirmado`, THE Gate_Juridico SHALL reduzir a confiança da dimensão de ocupação e SHALL registrar pendência de confirmação de desocupação, AND SHALL abster-se de tratar o imóvel como desocupado comprovado.
3. IF a situação de ocupação é `desconhecido`, THEN THE Gate_Juridico SHALL registrar pendência de prioridade `alta` para estimativa de custo e prazo de desocupação, SHALL registrar contingência de desocupação, SHALL reduzir a confiança da dimensão de ocupação AND SHALL permitir a continuidade da análise.
3.1. THE Gate_Juridico SHALL abster-se de classificar a ocupação desconhecida como pendência de prioridade `critica`, porque a continuidade da análise econômica é exigida pelo critério 3.
4. WHEN o imóvel está comprovadamente desocupado, THE Motor_de_Risco SHALL abster-se de registrar risco de posse.
5. WHEN a ocupação é relevante, THE Motor_de_Calculo SHALL incluir no custo econômico total o custo estimado de desocupação e o custo de carregamento pelo prazo estimado de desocupação.
6. WHEN existe terceiro ocupante, THE Gate_Juridico SHALL investigar a origem da posse, incluindo eventual contrato de compra e venda ou cessão de posição contratual entre o devedor fiduciante e o terceiro.
7. IF a origem da posse de terceiro é relevante e não comprovada, THEN THE Gate_Juridico SHALL retornar `PENDENTE` e SHALL registrar risco de posse de severidade `alto`.
8. THE Gate_Juridico SHALL manter o risco de posse como categoria distinta do risco de nulidade em todos os registros e explicações.

### Requirement 19: Locação e efeitos perante o adquirente

**User Story:** Como investidor, quero saber se existe locação que me vincule, sem presumir que a locação anula o leilão.

#### Acceptance Criteria

1. THE Gate_Juridico SHALL verificar a existência de contrato de locação e SHALL registrar, quando o contrato é obtido, data de início, data de término, valor do aluguel, garantia, cláusula de vigência e eventual registro ou averbação na matrícula.
2. THE Gate_Juridico SHALL comparar a data do contrato de locação com a data da garantia fiduciária e SHALL registrar a relação temporal apurada.
3. WHEN existe cláusula de vigência averbada na matrícula, THE Gate_Juridico SHALL registrar que a locação pode subsistir perante o adquirente e THE Motor_de_Liquidez SHALL incorporar esta restrição ao prazo de saída.
4. IF existe conflito entre as condições da locação e a garantia fiduciária, THEN THE Gate_Juridico SHALL retornar `RISCO_JURIDICO` e SHALL registrar pendência de análise jurídica específica.
5. THE Gate_Juridico SHALL abster-se de presumir nulidade do leilão com base apenas na existência de inquilino.
6. WHEN existe locação vigente, THE Motor_de_Calculo SHALL calcular o impacto da locação sobre posse, prazo de saída e rentabilidade, e SHALL registrar este impacto no cenário econômico.

### Requirement 20: Evidência jurídica com proveniência obrigatória

**User Story:** Como auditor, quero rastrear cada conclusão jurídica até o documento que a sustenta, para poder defender ou revisar a decisão depois.

#### Acceptance Criteria

1. WHEN uma verificação jurídica é registrada, THE Camada_de_Evidencia SHALL gravar identificação da regra, fonte, documento, localização exata da prova, fato afirmado, valor, estado da evidência, confiança de 0 a 100, autor do registro, data de observação e data de extração.
2. THE Camada_de_Evidencia SHALL classificar cada evidência em exatamente um estado: `OBSERVED`, `CONFIRMED`, `CALCULATED`, `ESTIMATED`, `INFERRED` ou `UNKNOWN`.
3. THE Camada_de_Evidencia SHALL rejeitar o registro de evidência sem fonte identificada.
4. THE Camada_de_Evidencia SHALL rejeitar a alteração do estado de uma evidência de `UNKNOWN` para `CONFIRMED` sem o registro de uma nova evidência de suporte.
5. WHEN evidências contraditórias existem sobre o mesmo fato, THE Camada_de_Evidencia SHALL preservar todas as evidências e SHALL marcar o fato como conflitante.
6. THE Camada_de_Evidencia SHALL registrar cada evidência de forma append-only.
7. WHEN uma verificação obrigatória não possui evidência, THE Camada_de_Evidencia SHALL registrar uma evidência de estado `UNKNOWN` com confiança 0, explicitando que a ausência de prova não constitui regularidade.

---

### Domínio D — Mercado, Comparáveis e Valuation

### Requirement 21: Seleção e qualificação de comparáveis

**User Story:** Como investidor, quero saber de onde veio o valor de mercado, para poder discordar de uma premissa específica.

#### Acceptance Criteria

1. THE Motor_de_Valuation SHALL selecionar comparáveis priorizando, em ordem decrescente: transações efetivamente realizadas; ofertas muito semelhantes e recentes no mesmo condomínio; ofertas na mesma microárea; ofertas no mesmo bairro; ofertas em regiões próximas comparáveis.
2. THE Motor_de_Valuation SHALL registrar, para cada comparável, fonte, endereço ou condomínio, tipo, área com seu tipo, quartos, vagas, preço, preço por metro quadrado, aluguel quando disponível, condomínio, data de observação, link e classe de qualidade.
3. THE Motor_de_Valuation SHALL classificar cada comparável em uma classe de qualidade: `A` transação comparável realizada; `B` oferta muito semelhante e atual; `C` oferta semelhante com ajustes; `D` estimativa indireta ou amostra reduzida; `E` analogia fraca ou dado antigo; `U` evidência insuficiente.
4. THE Motor_de_Valuation SHALL restringir comparáveis ao raio `VAL-003` e à janela temporal `VAL-004`, salvo registro explícito de exceção com justificativa.
5. THE Motor_de_Valuation SHALL distinguir preço anunciado de preço efetivamente transacionado em todos os registros e cálculos.
6. IF apenas preços anunciados estão disponíveis, THEN THE Motor_de_Valuation SHALL utilizá-los como evidência AND SHALL reduzir a confiança do valuation.
7. THE Motor_de_Valuation SHALL excluir da amostra comparáveis com erro evidente e comparáveis de segmento incompatível, registrando o motivo da exclusão.
8. THE Motor_de_Valuation SHALL identificar outliers pelo critério `CMP-012` e SHALL registrar, para cada outlier, a decisão de excluir ou de ajustar com a respectiva justificativa.
9. WHEN um outlier se repete na amostra, THE Motor_de_Valuation SHALL registrar a hipótese de submercado distinto e SHALL manter a investigação como pendência.
10. THE Motor_de_Valuation SHALL aplicar ajustes explícitos e registrados para diferenças de área, quartos, vagas, padrão construtivo, estado de conservação, andar, posição, condomínio, localização e data.
10.1. THE Motor_de_Valuation SHALL tratar o ajuste por estado de conservação como obrigatório conforme `CMP-008`, AND SHALL registrar pendência e reduzir a confiança do valuation quando o estado de conservação do imóvel ou do comparável for desconhecido.
10.2. WHEN a idade do anúncio comparável excede `CMP-011`, THE Motor_de_Valuation SHALL excluir o comparável da amostra; WHEN a idade excede metade de `CMP-011` e não excede `CMP-011`, THE Motor_de_Valuation SHALL aplicar a penalidade de peso `CMP-013`.
11. THE Motor_de_Valuation SHALL comparar preço por metro quadrado utilizando o mesmo tipo de área para o imóvel e para o comparável.
12. IF o tipo de área do imóvel ou do comparável é desconhecido, THEN THE Motor_de_Valuation SHALL registrar pendência e SHALL reduzir a confiança do valuation.

### Requirement 22: Quantidade de comparáveis e confiança do valuation

**User Story:** Como investidor, quero que poucos comparáveis reduzam a confiança, para não receber falsa precisão.

#### Acceptance Criteria

1. WHEN a quantidade de comparáveis de classe `A` ou `B` é igual ou superior a `VAL-011`, THE Motor_de_Valuation SHALL atribuir confiança de valuation na faixa 90 a 100.
2. WHEN a quantidade de comparáveis de classe `A` a `C` é igual ou superior a `VAL-011` e a condição do critério 1 não é satisfeita, THE Motor_de_Valuation SHALL atribuir confiança de valuation na faixa 75 a 89.
3. WHEN a quantidade de comparáveis de classe `A` a `C` é igual ou superior a `VAL-001` e inferior a `VAL-011`, OR a amostra atinge `VAL-011` com qualidade predominante `D`, THE Motor_de_Valuation SHALL atribuir confiança de valuation na faixa 60 a 74.
4. WHEN a quantidade de comparáveis aproveitáveis é inferior a `VAL-001` e superior a 1, THE Motor_de_Valuation SHALL ampliar a faixa de valor AND SHALL atribuir confiança de valuation na faixa 40 a 59.
4.1. WHEN existe exatamente um comparável aproveitável, THE Motor_de_Valuation SHALL tratar este comparável como evidência isolada AND SHALL atribuir confiança de valuation na faixa 0 a 39.
5. IF não existe comparável aproveitável, THEN THE Motor_de_Valuation SHALL retornar valuation `INCONCLUSIVO` e SHALL registrar pendência de mercado.
6. IF a confiança do valuation é inferior a `VAL-009`, THEN THE Motor_de_Decisao SHALL impedir a decisão `BUY` pela camada de dados e confiança.
7. THE Motor_de_Valuation SHALL considerar quantidade, qualidade, atualidade, semelhança e dispersão da amostra ao calcular a confiança do valuation.
8. THE Motor_de_Valuation SHALL registrar a metodologia aplicada, a amostra utilizada, os ajustes realizados e as premissas assumidas em cada valuation.

### Requirement 23: Faixas de valor e cenários de valuation

**User Story:** Como investidor, quero uma faixa de valor e não um número único, para entender o intervalo de incerteza.

#### Acceptance Criteria

1. WHEN o valuation é produzido, THE Motor_de_Valuation SHALL emitir quatro referências de valor: `conservador`, `base`, `otimista` e `venda_rapida`.
2. THE Motor_de_Valuation SHALL derivar o valor `base` da mediana da amostra ajustada de comparáveis.
2.1. THE Motor_de_Valuation SHALL derivar o valor `conservador` aplicando a margem conservadora `VAL-008` sobre o valor `base`.
3. THE Motor_de_Valuation SHALL derivar o valor `venda_rapida` aplicando o desconto `VAL-007` sobre o valor `conservador`.
4. THE Motor_de_Valuation SHALL emitir cada referência de valor acompanhada da confiança correspondente e do método utilizado.
5. THE Motor_de_Valuation SHALL utilizar o valor `conservador` como referência dos testes de robustez e o valor `base` como referência da decisão principal.
6. THE Motor_de_Valuation SHALL abster-se de utilizar o valor `otimista` como referência única de qualquer decisão.
7. THE Motor_de_Valuation SHALL registrar o valor de avaliação da fonte como campo distinto e SHALL abster-se de usá-lo como valor de mercado.
8. IF o valor de avaliação da fonte é superior ao valor `otimista` da amostra de comparáveis, THEN THE Motor_de_Valuation SHALL registrar esta divergência como evidência e SHALL registrar pendência de investigação.

### Requirement 24: Métodos de valuation por tipo de ativo

**User Story:** Como investidor, quero que terreno, casa e apartamento sejam avaliados por métodos adequados a cada natureza.

#### Acceptance Criteria

1. THE Motor_de_Valuation SHALL suportar os métodos comparativo, preço por metro quadrado ajustado, mesmo condomínio, capitalização de renda, residual ou de potencial, analogia de mercado e híbrido.
2. WHERE o imóvel é apartamento, THE Motor_de_Valuation SHALL priorizar o método de mesmo condomínio e SHALL considerar área privativa, condomínio, vagas, andar, elevador, posição, padrão do condomínio e estado da unidade.
3. WHERE o imóvel é casa ou sobrado, THE Motor_de_Valuation SHALL considerar área de terreno, área construída, padrão, conservação, vagas, microlocalização e potencial de reforma ou ampliação.
4. WHERE o imóvel é terreno, THE Motor_de_Valuation SHALL aplicar o método residual ou de potencial e SHALL considerar zoneamento, uso permitido, potencial construtivo, dimensões, testada, profundidade, topografia, infraestrutura disponível, restrições ambientais, demanda de lotes, custos de desenvolvimento e prazo provável de saída.
5. WHERE o imóvel é de segmento MCMV ou baixa renda, THE Motor_de_Valuation SHALL considerar ticket compatível com o público-alvo, demanda efetiva, disponibilidade de financiamento, aluguel praticado, liquidez e comparáveis do mesmo segmento.
6. THE Motor_de_Valuation SHALL abster-se de exigir yield de aluguel para terrenos.
7. THE Motor_de_Valuation SHALL tratar a classificação socioeconômica do público como dimensão informativa e SHALL abster-se de usá-la como proxy de risco ou de qualidade.
8. THE Motor_de_Valuation SHALL registrar qual método foi aplicado em cada referência de valor emitida.

### Requirement 25: Gatilhos de revaluation

**User Story:** Como investidor, quero que o valor seja reestimado quando o mercado muda, para não decidir com base em dado vencido.

#### Acceptance Criteria

1. WHEN um novo comparável de classe `A` a `C` dentro do raio e da janela é registrado, THE Monitor SHALL disparar novo valuation.
2. WHEN o prazo de frescor do valuation definido em FRESH é excedido, THE Monitor SHALL marcar o valuation como vencido, SHALL reduzir a confiança do valuation AND SHALL disparar novo valuation.
3. WHEN o aluguel de mercado varia em `MON-005` ou mais, THE Monitor SHALL disparar novo valuation pelo método de capitalização de renda quando aplicável.
4. WHEN uma informação física relevante do imóvel é alterada, THE Monitor SHALL disparar novo valuation.
5. WHEN a estratégia ativa é alterada, THE Motor_de_Valuation SHALL recalcular o preço máximo sem necessariamente recalcular o valor de mercado.

---

### Domínio E — Economia, Custos e Rentabilidade

### Requirement 26: Custo econômico total

**User Story:** Como investidor, quero saber quanto a operação realmente custa, para não confundir desconto de entrada com lucro.

#### Acceptance Criteria

1. THE Motor_de_Calculo SHALL calcular o custo econômico total como a soma dos **treze** componentes aplicáveis: preço ou lance; comissão do leiloeiro; ITBI e tributos de aquisição; registro, escritura e documentação; débitos de condomínio assumidos; débitos de tributos e taxas assumidos; regularização; reforma; desocupação; reserva para imprevistos; custo jurídico esperado; custo de carregamento; e custo financeiro.
1.1. THE Motor_de_Calculo SHALL excluir do custo econômico total os custos de saída e o imposto de renda sobre ganho de capital, AND SHALL computá-los exclusivamente na perna de venda conforme `R27.9` e `R27.10`.
1.2. THE Motor_de_Calculo SHALL excluir do custo econômico total o componente de custo de oportunidade do capital de `CUS-016`, AND SHALL utilizá-lo apenas nas métricas de custo do tempo e de eficiência de capital de `R30.2` e `R30.3`.
2. THE Motor_de_Calculo SHALL calcular a comissão do leiloeiro como `preço × CUS-002` e SHALL adotar o percentual do edital quando este estiver disponível.
3. THE Motor_de_Calculo SHALL calcular o ITBI como `preço × CUS-003` e SHALL adotar a alíquota municipal quando esta estiver disponível.
4. THE Motor_de_Calculo SHALL calcular o custo jurídico esperado como `custo jurídico potencial × probabilidade jurídica`.
5. THE Motor_de_Calculo SHALL calcular a reserva para imprevistos como `custo de aquisição × CUS-011`.
6. THE Motor_de_Calculo SHALL calcular o custo de carregamento como `carrying mensal × prazo estimado até a saída em meses`.
7. THE Motor_de_Calculo SHALL classificar cada componente de custo em exatamente um estado: `CONFIRMED`, `ESTIMATED`, `CALCULATED` ou `UNKNOWN`.
8. IF um componente de custo é `UNKNOWN` e o impacto estimado é alto, THEN THE Motor_de_Calculo SHALL criar contingência com faixa estimada AND THE Motor_de_Decisao SHALL impedir a decisão `BUY`.
9. IF um componente de custo crítico é `UNKNOWN`, THEN THE Motor_de_Decisao SHALL emitir no máximo `BUY_IF` ou `MONITOR` e SHALL registrar a condição objetiva de liberação.
10. THE Motor_de_Calculo SHALL atribuir valor zero a um componente de custo apenas quando existir evidência de que o componente não é aplicável ou é efetivamente nulo.
11. THE Motor_de_Calculo SHALL manter os componentes de custo separados e individualmente consultáveis, além do total.
12. IF o custo econômico total possui componente `UNKNOWN` de impacto alto ou crítico, THEN THE Motor_de_Calculo SHALL emitir o preço máximo como provisório e SHALL registrar que o preço máximo definitivo depende da resolução da pendência.

### Requirement 27: Métricas econômicas determinísticas

**User Story:** Como investidor, quero que as métricas econômicas sejam sempre calculadas da mesma forma, para poder comparar oportunidades.

#### Acceptance Criteria

1. THE Motor_de_Calculo SHALL calcular `desconto_da_fonte = 1 − (preço ÷ avaliação da fonte)` e SHALL marcar esta métrica como informativa.
2. THE Motor_de_Calculo SHALL calcular `desconto_de_mercado = 1 − (preço ÷ valor de mercado provável)`.
3. THE Motor_de_Calculo SHALL calcular `desconto_liquido = 1 − (custo econômico total ÷ valor de mercado provável)`.
4. THE Motor_de_Calculo SHALL calcular `margem_absoluta = valor de mercado provável − custo econômico total`.
5. THE Motor_de_Calculo SHALL calcular `margem_percentual = (valor de mercado provável − custo econômico total) ÷ valor de mercado provável`.
6. THE Motor_de_Calculo SHALL calcular `yield_bruto_mensal = aluguel mensal ÷ custo econômico total` e `yield_bruto_anual = yield_bruto_mensal × 12`.
7. THE Motor_de_Calculo SHALL calcular `aluguel_liquido = máximo(0; aluguel mensal − condomínio não recuperável − IPTU não recuperável − manutenção − seguro e taxas − perda por vacância − perda por inadimplência − imposto de renda sobre aluguel)`.
7.1. THE Motor_de_Calculo SHALL calcular `base_ir_aluguel = máximo(0; aluguel mensal − condomínio não recuperável − IPTU não recuperável − manutenção − seguro e taxas)` e `imposto de renda sobre aluguel = base_ir_aluguel × REN-012`.
7.2. WHILE `REN-012` permanece `[PENDENTE-DECISÃO]`, THE Motor_de_Calculo SHALL emitir o yield líquido como provisório e SHALL registrar que o imposto sobre aluguel não foi aplicado, AND SHALL abster-se de registrar o imposto como zero comprovado.
8. THE Motor_de_Calculo SHALL calcular `yield_liquido_mensal = aluguel líquido ÷ custo econômico total` e `yield_liquido_anual = yield_liquido_mensal × 12`.
9. THE Motor_de_Calculo SHALL calcular `venda_liquida = preço de venda − corretagem de venda − outros custos de venda − imposto de renda sobre ganho de capital`.
10. THE Motor_de_Calculo SHALL calcular `base_de_ir = máximo(0; preço de venda − corretagem de venda − outros custos de venda − custo econômico total)`.
11. THE Motor_de_Calculo SHALL calcular `lucro_liquido = venda líquida − custo econômico total`.
12. THE Motor_de_Calculo SHALL calcular `roi_liquido = lucro líquido ÷ custo econômico total`.
13. THE Motor_de_Calculo SHALL calcular `margem_liquida = lucro líquido ÷ preço de venda`.
14. THE Motor_de_Calculo SHALL calcular `break_even_de_saida` como o preço de venda que produz lucro líquido igual a zero.
15. THE Motor_de_Calculo SHALL calcular `desconto_estressado = 1 − (custo estressado ÷ valor de saída estressado)`.
16. IF o valor de mercado provável é igual ou inferior a zero, THEN THE Motor_de_Calculo SHALL rejeitar o cálculo das métricas dependentes e SHALL registrar erro de dado de entrada.
17. THE Motor_de_Calculo SHALL executar todos os cálculos deste requisito de forma determinística, sem depender de modelo de linguagem.

### Requirement 28: Preço máximo por estratégia

**User Story:** Como investidor, quero saber o teto racional de entrada por estratégia, para nunca deixar a disputa definir meu lance.

#### Acceptance Criteria

1. THE Motor_de_Calculo SHALL calcular um preço máximo por estratégia ativa, de forma retroativa a partir do valor econômico de saída.
2. WHERE a estratégia é revenda, THE Motor_de_Calculo SHALL calcular o preço máximo resolvendo o preço para o qual o ROI líquido resultante é exatamente igual ao ROI alvo da estratégia, pela expressão `preço_maximo = (V×(1−c_v)×(1−t) − F×(1+r−t)) ÷ ((1 + c_c + c_itbi)×(1+r−t))`, em que `V` é o preço de venda de referência, `c_v` é `CUS-012`, `t` é `CUS-013`, `F` é o somatório dos custos fixos de aquisição e de preparação, `c_c` é `CUS-002`, `c_itbi` é `CUS-003` e `r` é o ROI alvo da estratégia.
2.1. THE Motor_de_Calculo SHALL incluir `c_itbi` no coeficiente proporcional ao preço, porque o ITBI é proporcional ao preço de aquisição; para as entradas do caso de prova `F.1` o resultado é **R$ 182.158,03**.
2.2. WHERE a reserva para imprevistos é aplicada proporcionalmente conforme `CUS-011`, THE Motor_de_Calculo SHALL usar `k = (1 + CUS-011) × (1 + c_c + c_itbi)` como coeficiente proporcional e `F = (1 + CUS-011) × custos fixos exceto reserva + custo de carregamento`, resultando em `preço_maximo = (V×(1−c_v)×(1−t) − F×(1+r−t)) ÷ (k×(1+r−t))`.
3. THE Motor_de_Calculo SHALL satisfazer a propriedade inversa: ao usar o preço máximo como preço de aquisição, o ROI líquido recalculado pelas fórmulas do Requirement 27 SHALL ser igual ao ROI alvo dentro da tolerância de 10^-6.
4. WHERE o investidor solicita a forma fechada conservadora do método de referência, THE Motor_de_Calculo SHALL calcular `preço_maximo_conservador = (V×(1−c_v) − t×(V×(1−c_v) − F) − F) ÷ (1 + c_c×(1+t) + r)` AND SHALL apresentar este valor como **referência informativa**.
4.1. THE Motor_de_Calculo SHALL abster-se de apresentar o teto conservador do critério 4 como limite superior garantido, porque ele pode exceder o preço máximo exato.
4.2. THE Motor_de_Calculo SHALL definir o **teto decisório** como `mínimo(preço máximo exato do critério 2; preço máximo ajustado ao risco do critério 9)`.
5. WHERE a estratégia é renda, THE Motor_de_Calculo SHALL calcular o preço máximo resolvendo o preço para o qual o yield líquido mensal resultante é igual ao `yield_liquido_mensal_min` da estratégia.
6. WHERE a estratégia é valorização, THE Motor_de_Calculo SHALL calcular o preço máximo a partir do valor futuro projetado ajustado ao risco e ao horizonte, subtraindo custos, carregamento e a margem exigida.
7. WHERE a estratégia é MCMV, THE Motor_de_Calculo SHALL calcular o preço máximo a partir do valor compatível com a demanda e a capacidade de financiamento do público-alvo, subtraindo custos e margem.
8. WHERE a estratégia é terreno, THE Motor_de_Calculo SHALL calcular o preço máximo a partir do valor econômico do potencial de uso, subtraindo custos de desenvolvimento, custos de aquisição e margem.
9. THE Motor_de_Calculo SHALL calcular `preco_maximo_ajustado_ao_risco = preço máximo econômico − custo esperado de risco − contingência de risco − margem adicional exigida`.
10. WHEN a liquidez estimada está abaixo do mínimo da estratégia, THE Motor_de_Calculo SHALL reduzir o preço máximo pela margem adicional de `LIQ-010` correspondente ao prazo estimado.
11. IF a liquidez é indefinida, THEN THE Motor_de_Calculo SHALL abster-se de emitir preço máximo definitivo e SHALL emitir preço máximo provisório marcado como dependente de pendência.
12. WHEN o preço máximo é calculado, THE Motor_de_Calculo SHALL emitir também o preço-alvo, definido como o preço máximo reduzido pela folga configurada pelo investidor.
13. IF o preço de oferta é superior ao preço máximo ajustado ao risco da estratégia, THEN THE Motor_de_Decisao SHALL emitir `DO_NOT_BUY` para esta estratégia.
14. WHEN o preço de oferta está entre o preço-alvo e o preço máximo, THE Motor_de_Decisao SHALL emitir `BUY_IF` com teto explícito ou `MONITOR`, conforme a robustez do cenário.
15. THE Radar SHALL permitir que o mesmo imóvel possua preços máximos diferentes por estratégia.
16. THE Radar SHALL apresentar o preço máximo como limite, nunca como preço recomendado de compra.

### Requirement 29: Reforma, contingência e regularização

**User Story:** Como investidor, quero que a reforma seja tratada por faixa e não por falsa precisão, para não ter a margem destruída por surpresa.

#### Acceptance Criteria

1. THE Motor_de_Calculo SHALL classificar a reforma em exatamente um nível: `0` sem reforma relevante; `1` cosmética; `2` leve ou moderada; `3` significativa; `4` pesada ou estrutural.
2. WHILE não existe orçamento confirmado, THE Motor_de_Calculo SHALL representar a reforma como faixa com valor mínimo, base e máximo.
3. THE Motor_de_Calculo SHALL aplicar a contingência de reforma conforme `CUS-017` para o nível classificado.
4. WHERE não houve vistoria do imóvel, THE Motor_de_Calculo SHALL somar a contingência adicional `CUS-018`.
5. WHERE o imóvel está ocupado, THE Motor_de_Calculo SHALL somar a contingência adicional `CUS-019`.
6. IF existe suspeita de problema estrutural sem confirmação, THEN THE Gestor_de_Due_Diligence SHALL registrar pendência de prioridade crítica AND THE Motor_de_Decisao SHALL impedir a decisão `BUY`.
7. THE Motor_de_Calculo SHALL separar reforma necessária de reforma desejável e SHALL incluir apenas a reforma necessária no cenário base.
8. WHERE a estratégia é renda, THE Motor_de_Calculo SHALL considerar como reforma necessária o mínimo exigido para locação.
9. WHERE a estratégia é revenda, THE Motor_de_Calculo SHALL avaliar a reforma contra o preço de saída e o prazo de venda.
10. THE Motor_de_Calculo SHALL registrar custo, prazo e efeito da reforma sobre liquidez e valor de saída.
11. THE Motor_de_Calculo SHALL registrar o custo de regularização documental ou de obra como componente distinto do custo de reforma.

### Requirement 30: Capital imobilizado e custo do tempo

**User Story:** Como investidor, quero que o tempo do capital entre na conta, para não comparar operações de prazos diferentes como se fossem iguais.

#### Acceptance Criteria

1. THE Motor_de_Calculo SHALL calcular o capital inicial, o capital total, o prazo de imobilização estimado em meses e o capital exposto ao risco da operação.
2. THE Motor_de_Calculo SHALL modelar o custo de carregamento por mês, incluindo condomínio, tributos e taxas, manutenção, seguro quando aplicável, custo financeiro e custo de oportunidade do capital.
3. THE Motor_de_Calculo SHALL calcular o custo de oportunidade do capital usando `GLB-007` como taxa de referência.
3.1. THE Motor_de_Calculo SHALL calcular `roi_anualizado = (1 + roi_liquido)^(12 ÷ prazo em meses) − 1` e SHALL usar esta métrica como a grandeza comparável com `GLB-011`.
3.2. IF o prazo em meses é igual ou inferior a zero, THEN THE Motor_de_Calculo SHALL rejeitar o cálculo de `roi_anualizado` e SHALL registrar erro de dado de entrada.
4. THE Motor_de_Calculo SHALL calcular `margem_por_mes = margem absoluta ÷ prazo de imobilização em meses`.
5. THE Motor_de_Calculo SHALL calcular `retorno_por_capital = lucro líquido ÷ capital total`.
6. IF o prazo estimado de imobilização excede `LIQ-009`, THEN THE Motor_de_Estrategia SHALL classificar a oportunidade como não aderente à estratégia AND THE Gestor_de_Alertas SHALL emitir alerta de prazo.
7. WHEN o prazo estimado de imobilização aumenta, THE Motor_de_Calculo SHALL recalcular o custo de carregamento e a margem exigida.
8. THE Motor_de_Calculo SHALL suportar o cálculo de valor presente líquido e de taxa interna de retorno para operações com múltiplos fluxos.
9. THE Radar SHALL apresentar valor presente líquido e taxa interna de retorno como métricas complementares e SHALL manter risco, liquidez e confiança como dimensões independentes.

### Requirement 31: Financiamento

**User Story:** Como investidor, quero comparar compra à vista e financiada, para escolher a estrutura de capital adequada.

#### Acceptance Criteria

1. WHERE o investidor aceita financiamento, THE Motor_de_Calculo SHALL modelar entrada, parcelas, juros, seguros, tarifas, prazo, amortização e saldo devedor.
2. THE Motor_de_Calculo SHALL incluir os juros e os custos financeiros no custo econômico total.
3. THE Motor_de_Calculo SHALL permitir a simulação de quitação antecipada em caso de venda antes do término do prazo.
4. THE Motor_de_Calculo SHALL comparar o retorno sobre capital próprio entre os cenários à vista, financiado e híbrido.
5. IF a parcela simulada excede `INV-004`, THEN THE Gestor_de_Portfolio SHALL classificar a operação como não aderente ao capital do investidor.
6. IF a forma de pagamento informada pela fonte exclui financiamento, THEN THE Motor_de_Calculo SHALL modelar apenas os cenários compatíveis com recursos próprios e recursos permitidos pelo edital.

### Requirement 32: Cenários e sensibilidade

**User Story:** Como investidor, quero saber se a tese sobrevive quando as premissas pioram, para medir a robustez antes de decidir.

#### Acceptance Criteria

1. THE Motor_de_Calculo SHALL produzir quatro cenários econômicos: `otimista`, `base`, `conservador` e `estressado`.
2. THE Motor_de_Calculo SHALL montar o cenário `conservador` com valor de saída reduzido, custos elevados e prazo estendido em relação ao cenário `base`.
3. THE Motor_de_Calculo SHALL montar o cenário `estressado` com valor de saída muito reduzido, custos muito elevados e prazo muito estendido.
4. THE Motor_de_Calculo SHALL calcular, para cada cenário, o custo econômico total, a margem, o ROI líquido e o prazo resultantes.
5. THE Motor_de_Calculo SHALL executar análise de sensibilidade sobre preço de saída nas variações de −0,05, −0,10 e −0,15; sobre reforma nas variações de +0,10, +0,25 e +0,50; sobre prazo nas variações de +3, +6 e +12 meses; sobre aluguel nas variações de −0,05, −0,10 e −0,15; sobre vacância nas variações de +3 e +6 meses; e sobre custos nas variações de +0,10 e +0,20.
6. THE Motor_de_Calculo SHALL classificar a robustez da operação em exatamente um nível: `muito_alta` quando funciona no conservador com boa margem; `alta` quando funciona no conservador com margem reduzida; `media` quando funciona no base e é sensível; `baixa` quando funciona apenas próximo do otimista; `especulativa` quando depende de múltiplas premissas favoráveis; `inviavel` quando não funciona no base nem no conservador.
7. IF a tese não sobrevive ao cenário `conservador`, THEN THE Motor_de_Decisao SHALL emitir no máximo `BUY_IF` pela camada de cenário.
8. IF a tese funciona apenas no cenário `otimista`, THEN THE Motor_de_Score SHALL classificar a oportunidade como especulativa.
9. IF a tese não é viável no cenário `base`, THEN THE Motor_de_Decisao SHALL emitir `DO_NOT_BUY`.
10. IF o cenário `conservador` depende de um dado `UNKNOWN`, THEN THE Motor_de_Decisao SHALL emitir `MONITOR` ou `BUY_IF` e SHALL registrar a pendência determinante.
11. THE Motor_de_Calculo SHALL calcular os limites do ponto de equilíbrio: preço de venda mínimo que cobre todos os custos; preço de compra máximo que mantém a margem exigida; aumento máximo suportado de reforma; queda máxima suportada de aluguel; e aumento máximo suportado de prazo.

### Requirement 33: Regras de decisão econômica

**User Story:** Como investidor, quero regras econômicas explícitas, para entender exatamente por que uma oportunidade foi reprovada.

#### Acceptance Criteria

1. IF o custo econômico total excede o valor de mercado `conservador`, THEN THE Motor_de_Decisao SHALL emitir `DO_NOT_BUY` ou `BLOCK` conforme a severidade do risco associado.
2. IF o preço de oferta excede o preço máximo da estratégia, THEN THE Motor_de_Decisao SHALL emitir `DO_NOT_BUY` para esta estratégia.
3. IF o desconto líquido é inferior ao `desconto_liquido_min` da estratégia, THEN THE Motor_de_Decisao SHALL emitir `DO_NOT_BUY` pela camada de economia.
4. IF a margem percentual é inferior à `margem_min` da estratégia, THEN THE Motor_de_Decisao SHALL emitir `DO_NOT_BUY` ou `BUY_IF` conforme a existência de condição objetiva de melhoria.
5. IF o custo de reforma excede o limite de tolerância `INV-008` do investidor, THEN THE Motor_de_Decisao SHALL emitir `BUY_IF` ou `DO_NOT_BUY`.
6. IF o yield líquido mensal é inferior ao `yield_liquido_mensal_min` da estratégia, THEN THE Motor_de_Estrategia SHALL classificar a oportunidade como não aderente às estratégias de renda e MCMV.
7. IF a diferença absoluta entre o break-even de saída e o **preço atual**, dividida pelo preço atual, é inferior a 0,05, THEN THE Motor_de_Decisao SHALL emitir `MONITOR`.
7.1. THE Motor_de_Calculo SHALL expressar o limiar do critério 7 como fração do preço atual, AND SHALL abster-se de compará-lo com o valor de mercado conservador.
8. WHEN o cenário `conservador` permanece robusto, THE Motor_de_Score SHALL elevar o componente de qualidade da oportunidade.
9. IF o `roi_anualizado` é inferior a `GLB-011`, THEN THE Motor_de_Decisao SHALL emitir `DO_NOT_BUY` pela camada de economia.
10. THE Motor_de_Decisao SHALL registrar, para cada decisão econômica, a métrica avaliada, o valor apurado, o limite aplicado e o parâmetro de origem do limite.

---

### Domínio F — Risco e Due Diligence

### Requirement 34: Classificação de risco

**User Story:** Como investidor, quero que riscos sejam classificados por categoria e severidade, para saber o que pode destruir a tese.

#### Acceptance Criteria

1. THE Motor_de_Risco SHALL classificar cada risco em exatamente uma categoria: `juridico`, `documental`, `ocupacao`, `financeiro`, `fisico`, `mercado`, `liquidez`, `operacional`, `estrategico` ou `informacional`.
2. THE Motor_de_Risco SHALL registrar, para cada risco, probabilidade, impacto, exposição de capital, incerteza, capacidade de mitigação, prazo potencial e estado da evidência.
3. THE Motor_de_Risco SHALL derivar a severidade do risco da matriz de probabilidade e impacto, produzindo `baixo`, `medio`, `alto` ou `critico`.
4. THE Motor_de_Risco SHALL aplicar a seguinte matriz de probabilidade e impacto: probabilidade baixa com impacto baixo resulta em `baixo`; probabilidade baixa com impacto médio resulta em `baixo`; probabilidade baixa com impacto alto resulta em `medio`; probabilidade baixa com impacto crítico resulta em `alto`; probabilidade média com impacto baixo resulta em `baixo`; probabilidade média com impacto médio resulta em `medio`; probabilidade média com impacto alto resulta em `alto`; probabilidade média com impacto crítico resulta em `critico`; probabilidade alta com impacto baixo resulta em `medio`; probabilidade alta com impacto médio resulta em `alto`; probabilidade alta com impacto alto resulta em `critico`; probabilidade alta com impacto crítico resulta em `critico`.
5. IF a severidade de um risco é `critico`, THEN THE Motor_de_Decisao SHALL emitir `BLOCK`, independentemente do estado da evidência.
5.1. WHERE a severidade `critico` decorre de evidência `ESTIMATED` ou `INFERRED`, THE Motor_de_Decisao SHALL registrar a decisão como bloqueio por risco crítico presumido AND SHALL registrar a condição objetiva de desbloqueio, que é confirmar ou afastar o risco com evidência.
5.2. THE Motor_de_Decisao SHALL abster-se de condicionar o bloqueio por risco crítico ao nível de confiança, AND SHALL manter o bloqueio reversível apenas pela condição registrada no critério 5.1.
6. IF a severidade de um risco é `alto`, THEN THE Motor_de_Decisao SHALL emitir `BUY_IF`, `MONITOR` ou `BLOCK` conforme a economia e a mitigação registradas.
7. WHEN a severidade de um risco é `medio`, THE Motor_de_Score SHALL reduzir o componente de risco do score e SHALL registrar a mitigação exigida.
8. THE Motor_de_Risco SHALL manter severidade e confiança como dimensões independentes.
9. THE Motor_de_Risco SHALL registrar um risco de estado `UNKNOWN` quando a categoria não foi investigada, e SHALL abster-se de classificá-lo como `baixo`.
10. THE Motor_de_Risco SHALL registrar a estratégia de mitigação adotada entre `eliminar`, `evitar`, `reduzir`, `transferir`, `aceitar` e `condicionar`.
11. WHEN a mitigação adotada é `aceitar`, THE Gestor_de_Governanca SHALL exigir registro de exceção com justificativa, evidência, limite e prazo.

### Requirement 35: Risco versus incerteza

**User Story:** Como investidor, quero que o Radar separe o que ele sabe do que ele não sabe, para eu entender o tamanho da minha ignorância.

#### Acceptance Criteria

1. WHEN um risco é conhecido e quantificável, THE Motor_de_Calculo SHALL incorporar o custo esperado deste risco ao custo econômico total.
2. WHEN um risco é conhecido e não quantificável, THE Motor_de_Estrategia SHALL elevar a margem exigida AND THE Motor_de_Decisao SHALL emitir decisão condicionada.
3. IF um dado desconhecido possui impacto baixo, THEN THE Gestor_de_Due_Diligence SHALL registrar pendência de prioridade baixa e SHALL permitir a decisão.
4. IF um dado desconhecido possui impacto alto, THEN THE Motor_de_Decisao SHALL emitir `BUY_IF` ou `MONITOR`.
5. IF um dado desconhecido possui impacto crítico, THEN THE Motor_de_Decisao SHALL impedir a decisão `BUY` e SHALL emitir `PENDING` ou `BLOCK` conforme a natureza do dado.
6. THE Motor_de_Risco SHALL calcular a margem de segurança exigida de forma crescente com o risco e com a incerteza, conforme: risco baixo com confiança alta exige a margem mínima da estratégia; risco médio exige margem acrescida; risco alto mitigável exige margem acrescida com condição objetiva; risco alto incerto exige margem substancialmente acrescida; risco crítico não admite margem compensatória.

### Requirement 36: Fases da Due Diligence

**User Story:** Como analista, quero fases progressivas de diligência, para investir esforço proporcional ao estágio da tese.

#### Acceptance Criteria

1. THE Gestor_de_Due_Diligence SHALL organizar a investigação em oito fases: `DD-0` triagem de bloqueios óbvios; `DD-1` documental; `DD-2` jurídica; `DD-3` financeira; `DD-4` ocupação; `DD-5` física; `DD-6` mercado; `DD-7` final com resolução de pendências.
2. THE Gestor_de_Due_Diligence SHALL executar a fase `DD-0` antes de qualquer investigação subsequente.
3. THE Gestor_de_Due_Diligence SHALL registrar, para cada item de cada fase, um resultado em exatamente um dos estados: `confirmado`, `parcialmente_confirmado`, `nao_confirmado`, `conflitante`, `nao_aplicavel` ou `desconhecido`.
3.1. THE Gestor_de_Due_Diligence SHALL expressar o resultado na ausência de evidência exclusivamente no vocabulário do critério 3 combinado com os estados de pendência e de decisão desta spec, AND SHALL abster-se de usar qualquer rótulo fora desses conjuntos.
3.2. THE Gestor_de_Due_Diligence SHALL reservar o resultado `REPROVADO` para evidência de irregularidade, AND SHALL registrar a falta de informação como `desconhecido` com pendência de prioridade proporcional ao impacto.
4. THE Gestor_de_Due_Diligence SHALL exigir evidência com proveniência para cada item crítico e SHALL marcar como `desconhecido` cada item crítico sem evidência.
5. THE Gestor_de_Due_Diligence SHALL avaliar todos os itens do Anexo A, do Anexo B e do Anexo C aplicáveis ao caso concreto.
6. WHEN a profundidade da diligência é definida, THE Gestor_de_Due_Diligence SHALL derivar a profundidade do score, do valor da operação, do risco, da estratégia e do custo de investigação.
7. IF a fase `DD-0` identifica bloqueio óbvio, THEN THE Orquestrador SHALL encerrar as fases subsequentes e SHALL encaminhar a análise para a decisão.

### Requirement 37: Pendências

**User Story:** Como analista, quero que cada pendência tenha dono, prazo e condição de encerramento, para que a diligência avance.

#### Acceptance Criteria

1. WHEN uma pendência é registrada, THE Gestor_de_Due_Diligence SHALL gravar o item pendente, o motivo, o impacto, o responsável, o prazo, a condição objetiva de liberação e a evidência que a encerrará.
2. THE Gestor_de_Due_Diligence SHALL classificar cada pendência em exatamente uma prioridade: `critica`, `alta`, `media` ou `baixa`.
3. IF existe pendência de prioridade `critica` em aberto, THEN THE Motor_de_Decisao SHALL impedir qualquer decisão além de `PENDING`, `MONITOR` ou `BLOCK`.
4. IF existe pendência de prioridade `alta` em aberto, THEN THE Motor_de_Decisao SHALL impedir a decisão `BUY` e SHALL permitir `BUY_IF`.
5. WHEN existe pendência de prioridade `media` em aberto, THE Motor_de_Score SHALL reduzir a confiança consolidada.
6. WHEN existe pendência de prioridade `baixa` em aberto, THE Motor_de_Decisao SHALL permitir a decisão e SHALL registrar a pendência na explicação.
7. WHEN uma pendência é resolvida, THE Gestor_de_Due_Diligence SHALL registrar a evidência de encerramento, a data e o autor, AND SHALL preservar o registro da pendência como histórico.
8. WHEN o prazo de uma pendência é ultrapassado, THE Gestor_de_Alertas SHALL emitir o alerta `ALT-016`.
9. WHEN uma pendência é resolvida, THE Monitor SHALL disparar o gatilho `MON-011` e THE Radar SHALL recalcular a confiança consolidada, o Opportunity Score, o Investor Fit e o ranking.

### Requirement 38: Visita física

**User Story:** Como investidor, quero registrar o que foi observado e o que não foi acessado, para não confundir observação com laudo técnico.

#### Acceptance Criteria

1. WHEN uma visita é registrada, THE Gestor_de_Due_Diligence SHALL gravar data, responsável, fotos com data, observações e a lista de áreas não acessadas.
2. THE Gestor_de_Due_Diligence SHALL registrar o estado observado de estrutura, instalação elétrica, instalação hidráulica, infiltração, cobertura, pisos e revestimentos, cozinha e banheiros, portas e janelas, áreas comuns, elevadores, vagas e acesso.
3. THE Gestor_de_Due_Diligence SHALL classificar cada observação de visita com o estado `OBSERVED` e SHALL abster-se de classificá-la como `CONFIRMED`.
4. THE Gestor_de_Due_Diligence SHALL registrar que uma observação visual não constitui laudo técnico.
5. IF a visita não foi realizada, THEN THE Motor_de_Calculo SHALL aplicar a contingência adicional `CUS-018` AND THE Gestor_de_Due_Diligence SHALL registrar pendência de vistoria de prioridade `alta`.
5.1. IF a condição estrutural do imóvel é desconhecida, THEN THE Gestor_de_Due_Diligence SHALL registrar pendência de prioridade `alta` AND THE Motor_de_Calculo SHALL registrar contingência de reforma estrutural, AND THE Radar SHALL abster-se de tratar a condição desconhecida apenas como contingência sem pendência.
6. WHERE a estratégia e o nível de risco exigem visita conforme parametrização, THE Motor_de_Decisao SHALL impedir a decisão `BUY` sem registro de visita.

### Requirement 39: Contexto humano e conforto pessoal

**User Story:** Como investidor, quero registrar meu grau de conforto com a operação, porque uma operação tecnicamente boa pode ser inaceitável para mim.

#### Acceptance Criteria

1. THE Gestor_de_Due_Diligence SHALL registrar, quando as informações estiverem disponíveis, o perfil do proprietário anterior, o tempo de propriedade, o tempo de residência, a situação de ocupação, indícios de vulnerabilidade e a situação aparente do ocupante.
2. THE Gestor_de_Due_Diligence SHALL registrar o Índice de Conforto Pessoal informado pelo investidor, em escala de 0 a 100.
3. IF o Índice de Conforto Pessoal é inferior a `INV-017`, THEN THE Motor_de_Decisao SHALL emitir no máximo `MONITOR` e SHALL registrar o critério pessoal como motivo.
4. IF a aceitação de um risco relevante depende de parecer jurídico AND o parecer jurídico não está registrado como evidência, THEN THE Motor_de_Decisao SHALL emitir `BLOCK` e THE Radar SHALL impedir a liberação de lance.
4.1. THE Motor_de_Decisao SHALL aplicar o critério 4 independentemente do valor de `INV-018`, AND SHALL abster-se de condicionar este bloqueio a qualquer parâmetro do perfil.
4.2. WHEN uma regra eliminatória expressa do investidor é acionada, THE Motor_de_Decisao SHALL emitir `BLOCK`, AND SHALL abster-se de emitir `DO_NOT_BUY`, porque `BLOCK` sai do ranking operacional e `DO_NOT_BUY` permanece nele.
5. THE Motor_de_Explicabilidade SHALL apresentar o critério de contexto humano como dimensão declarada pelo investidor, separada das dimensões técnicas.
6. THE Radar SHALL registrar as informações de contexto humano sem inferir características pessoais não declaradas em fonte identificada.

---

### Domínio G — Liquidez, Demanda e Saída

### Requirement 40: Score de liquidez

**User Story:** Como investidor, quero saber se consigo sair do investimento, porque margem sem saída é falsa oportunidade.

#### Acceptance Criteria

1. THE Motor_de_Liquidez SHALL calcular liquidez de venda e liquidez de locação como escores independentes na escala de 0 a 100.
2. THE Motor_de_Liquidez SHALL derivar a categoria de liquidez do score numérico em exatamente **sete faixas**, contínuas e sem lacuna sobre todo o domínio de 0 a 100: 90 a 100 resulta em `muito_alta`; 80 a 89 resulta em `alta`; 70 a 79 resulta em `boa`; 60 a 69 resulta em `media`; 50 a 59 resulta em `baixa`; 40 a 49 resulta em `muito_baixa`; 0 a 39 resulta em `iliquida`.
3. THE Motor_de_Liquidez SHALL compor o score de liquidez a partir de demanda com peso 0,25; preço competitivo com peso 0,20; liquidez histórica ou estimada com peso 0,20; ticket e financiabilidade com peso 0,15; concorrência com peso 0,10; condição do imóvel com peso 0,05; e situação documental e operacional com peso 0,05.
4. THE Motor_de_Liquidez SHALL considerar localização, faixa de preço, tipo, área, dormitórios, vagas, padrão, conservação, condomínio, financiabilidade, infraestrutura, perfil do público local e oferta concorrente como fatores de demanda.
5. THE Motor_de_Liquidez SHALL estimar tempo de venda e tempo de locação em dias, e SHALL registrar o método de estimativa.
6. IF os dados são insuficientes para estimar liquidez, THEN THE Motor_de_Liquidez SHALL retornar liquidez `indefinida`, SHALL reduzir a confiança consolidada AND SHALL registrar pendência.
7. IF o score de liquidez é inferior ao `liquidez_min` da estratégia, THEN THE Motor_de_Decisao SHALL emitir `DO_NOT_BUY` ou `BUY_IF` conforme a existência de exceção autorizada.
8. IF o score de liquidez é inferior a 50, THEN THE Motor_de_Decisao SHALL emitir `MONITOR` ou `DO_NOT_BUY` e SHALL exigir exceção formal para qualquer decisão de compra.
9. THE Motor_de_Liquidez SHALL identificar o público-alvo do imóvel entre morador, investidor, primeiro imóvel, segmento MCMV, alto padrão, usuário comercial e comprador de terreno.
10. THE Motor_de_Liquidez SHALL avaliar a liquidez do imóvel dentro do seu submercado de ticket, e SHALL abster-se de generalizar a liquidez do bairro para todas as faixas de preço.
11. THE Motor_de_Liquidez SHALL registrar a quantidade e as características da oferta concorrente considerada.

### Requirement 41: Preço e prazo de saída

**User Story:** Como investidor, quero preço de saída por cenário e prazo estimado, para dimensionar o custo do tempo.

#### Acceptance Criteria

1. THE Motor_de_Liquidez SHALL emitir preço de saída nos cenários `otimista`, `base`, `conservador` e `venda_rapida`.
2. THE Motor_de_Liquidez SHALL derivar o preço de saída dos comparáveis e do público-alvo identificado, e SHALL abster-se de igualá-lo automaticamente ao valor de mercado estimado.
3. THE Motor_de_Liquidez SHALL estimar o prazo de saída e SHALL classificar o impacto do prazo conforme: 0 a 3 meses resulta em carregamento baixo; 3 a 6 meses resulta em moderado; 6 a 12 meses resulta em alto; acima de 12 meses resulta em muito alto com margem adicional exigida.
4. THE Motor_de_Liquidez SHALL aplicar a margem adicional de `LIQ-010` correspondente ao prazo estimado.
5. IF o prazo estimado de venda excede `LIQ-002`, THEN THE Motor_de_Decisao SHALL emitir `BUY_IF` ou `DO_NOT_BUY`.
6. IF o preço de saída no cenário `conservador` não cobre o capital total empregado, THEN THE Motor_de_Decisao SHALL emitir `DO_NOT_BUY`.
7. WHEN a venda rápida é modelada, THE Motor_de_Calculo SHALL recalcular margem e ROI com o preço de venda rápida.
8. THE Motor_de_Liquidez SHALL registrar o desconto necessário para acelerar a saída e SHALL compará-lo com `LIQ-004`.

### Requirement 42: Estratégias de saída e operações híbridas

**User Story:** Como investidor, quero combinar renda e revenda na mesma operação, para aproveitar o ativo enquanto aguardo a saída.

#### Acceptance Criteria

1. THE Motor_de_Estrategia SHALL suportar estratégias de saída híbridas, incluindo comprar e reformar e alugar e vender posteriormente, comprar e alugar enquanto aguarda valorização, e comprar e regularizar e desenvolver e vender.
2. WHEN uma estratégia híbrida é selecionada, THE Motor_de_Calculo SHALL modelar o fluxo em etapas, com custos, receitas e prazos de cada etapa.
3. THE Motor_de_Calculo SHALL calcular o retorno total da estratégia híbrida somando o retorno de renda no período e o resultado da saída final.
4. THE Motor_de_Liquidez SHALL avaliar a liquidez exigida em cada etapa da estratégia híbrida.

### Requirement 43: Monitoramento de liquidez

**User Story:** Como investidor, quero ser avisado quando a saída ficar mais difícil, para reagir antes de perder margem.

#### Acceptance Criteria

1. THE Monitor SHALL acompanhar a quantidade de concorrentes, os preços dos concorrentes, o aluguel de mercado, a demanda, o tempo de anúncio, as condições de financiamento, o ticket do segmento e as mudanças de infraestrutura.
2. WHEN o score de liquidez varia em `MON-010` ou mais, THE Monitor SHALL disparar recálculo de score, de margem exigida e de preço máximo.
3. WHEN a liquidez melhora acima do gatilho configurado, THE Gestor_de_Alertas SHALL emitir alerta de fortalecimento da oportunidade.
4. WHEN o imóvel permanece sem interessados além do prazo alvo `LIQ-003`, THE Gestor_de_Alertas SHALL emitir alerta negativo de liquidez.

---

### Domínio H — Estratégias, Investidor e Portfólio

### Requirement 44: Estratégias simultâneas e aderência

**User Story:** Como investidor, quero avaliar o mesmo imóvel por várias estratégias, porque um ativo pode servir a uma tese e não a outra.

#### Acceptance Criteria

1. THE Radar SHALL suportar **seis** estratégias de investimento parametrizáveis: `revenda`, `renda`, `valorizacao`, `mcmv`, `terreno` e `customizada`.
1.1. WHERE a estratégia é `customizada`, THE Radar SHALL permitir que o investidor defina os thresholds da tabela `STR`, os pesos de `SCORE-002`, o score mínimo de `SCORE-004` e os critérios de avaliação aplicáveis, AND SHALL versionar a definição como qualquer outro parâmetro.
2. THE Radar SHALL suportar perfis de ativo `apartamento`, `casa_sobrado`, `um_dormitorio`, `comercial`, `galpao`, `terreno`, `rural`, `outros` e `desconhecido` como modificadores de critérios, e SHALL manter estes perfis distintos das estratégias de investimento.
2.1. WHERE o perfil de ativo é `desconhecido`, THE Motor_de_Estrategia SHALL registrar pendência de classificação e SHALL reduzir a confiança consolidada, AND SHALL abster-se de aplicar os critérios de qualquer perfil específico.
3. THE Motor_de_Estrategia SHALL avaliar cada oportunidade contra todas as estratégias ativas do investidor e SHALL emitir um resultado de aderência por estratégia.
4. THE Motor_de_Estrategia SHALL classificar a aderência em uma escala de 0 a 100 e SHALL derivar a interpretação conforme: 90 a 100 totalmente alinhada; 80 a 89 muito alinhada; 70 a 79 alinhada; 60 a 69 parcial; 50 a 59 especulativa; abaixo de 50 fora da estratégia.
5. IF a aderência a uma estratégia é inferior a 50, THEN THE Motor_de_Decisao SHALL emitir `DO_NOT_BUY` para esta estratégia.
6. THE Radar SHALL permitir que a mesma oportunidade resulte em decisões diferentes para estratégias diferentes.
7. WHEN uma oportunidade é aderente a mais de uma estratégia, THE Motor_de_Ranking SHALL registrar este fato como fator informativo de priorização.
8. THE Motor_de_Estrategia SHALL aplicar os thresholds da tabela `STR` vigente para cada estratégia avaliada.
9. WHERE existe parâmetro de estratégia específico, THE Gestor_de_Parametros SHALL aplicar o parâmetro específico em lugar do parâmetro global, exceto quando o global impõe bloqueio crítico ou restrição legal.
10. THE Motor_de_Estrategia SHALL registrar, para cada estratégia avaliada, os critérios atendidos, os critérios não atendidos e os parâmetros aplicados.

### Requirement 45: Critérios por estratégia

**User Story:** Como investidor, quero que cada estratégia avalie o que realmente importa nela, para não receber um score genérico.

#### Acceptance Criteria

1. WHERE a estratégia é `renda`, THE Motor_de_Estrategia SHALL avaliar yield líquido mensal, aluguel provável, vacância esperada, custos recorrentes, relação entre condomínio e aluguel, demanda locatícia, prazo de estabilização, liquidez de locação e viabilidade de saída futura.
2. WHERE a estratégia é `revenda`, THE Motor_de_Estrategia SHALL avaliar desconto líquido, margem após reforma, custo de reforma, prazo de saída, custo de carregamento, custos de saída, preço de saída conservador e sensibilidade a desconto na venda.
3. WHERE a estratégia é `valorizacao`, THE Motor_de_Estrategia SHALL avaliar qualidade da localização, infraestrutura futura, tendência de mercado, preço relativo, horizonte de investimento, renda durante a espera, custo de carregamento e liquidez futura.
4. WHERE a estratégia é `mcmv`, THE Motor_de_Estrategia SHALL avaliar ticket compatível com o público, demanda efetiva, disponibilidade de financiamento, aluguel relativo à renda local, liquidez de venda e de locação, condição do imóvel e localização dentro dos parâmetros configurados.
5. WHERE a estratégia é `terreno`, THE Motor_de_Estrategia SHALL avaliar zoneamento, uso permitido, potencial construtivo, testada, profundidade, formato, topografia, infraestrutura, restrições ambientais, preço por metro quadrado, demanda de compradores, prazo de desenvolvimento e risco de desenvolvimento.
6. WHERE o perfil de ativo é `apartamento`, THE Motor_de_Estrategia SHALL avaliar condomínio, vaga, andar, elevador, posição, padrão do condomínio, área privativa, estado e comparáveis do mesmo empreendimento.
7. WHERE o perfil de ativo é `casa_sobrado`, THE Motor_de_Estrategia SHALL avaliar terreno, área construída, conservação, garagem, regularização, custo de manutenção, liquidez da rua e potencial de ampliação.
8. WHERE o perfil de ativo é `um_dormitorio`, THE Motor_de_Estrategia SHALL avaliar demanda locatícia específica, ticket, aluguel, condomínio, liquidez e público comprador, AND SHALL abster-se de descartar o ativo com base apenas na quantidade de dormitórios.
9. THE Motor_de_Estrategia SHALL abster-se de excluir automaticamente qualquer tipo de imóvel ou segmento socioeconômico.
10. IF o score de liquidez está abaixo do `liquidez_min` da estratégia, THEN THE Motor_de_Estrategia SHALL exigir margem percentual igual ou superior a `LIQ-011`.
10.1. THE Motor_de_Estrategia SHALL aplicar cumulativamente a margem adicional por prazo de `LIQ-010` e a margem mínima por liquidez baixa de `LIQ-011`, porque compensam fatores distintos.
11. WHERE o imóvel é atípico para o seu submercado, THE Motor_de_Valuation SHALL exigir comparáveis de qualidade superior, elevando o requisito mínimo de classe `C` para classe `B`, AND THE Motor_de_Estrategia SHALL registrar a atipicidade como fator de liquidez.
12. WHERE a estratégia é `renda`, THE Motor_de_Estrategia SHALL aplicar como critérios próprios da estratégia o `reforma_maxima_nivel`, o `prazo_maximo_estabilizacao_dias` e a `concentracao_maxima_por_regiao` da tabela de parâmetros próprios de estratégia.
13. WHERE a estratégia é `revenda`, THE Motor_de_Estrategia SHALL aplicar como critérios próprios o `custo_maximo_reforma` e o `capital_maximo_por_operacao`.
14. WHERE a estratégia é `valorizacao`, THE Motor_de_Estrategia SHALL aplicar como critérios próprios o `horizonte_minimo_meses` e a `tolerancia_capital_imobilizado`.
15. WHERE a estratégia é `mcmv`, THE Motor_de_Estrategia SHALL avaliar também o custo de reforma contra `custo_maximo_reforma` e o potencial de revenda contra `potencial_revenda_minimo`.
16. WHERE a estratégia é `terreno`, THE Motor_de_Estrategia SHALL avaliar também o ticket contra o `ticket_max` aplicável e o capital imobilizado contra `capital_imobilizado_maximo`.
17. WHERE o perfil de ativo é `apartamento`, THE Motor_de_Estrategia SHALL avaliar também preço por metro quadrado, quantidade de dormitórios, financiabilidade, demanda de locação e demanda de venda.
18. WHERE o perfil de ativo é `casa_sobrado`, THE Motor_de_Estrategia SHALL avaliar também o ticket, a adequação ao público familiar, a financiabilidade e o uso alternativo do imóvel.

### Requirement 46: Capital, reserva e limite por operação

**User Story:** Como investidor, quero que o Radar respeite meu capital e minha reserva, para não me recomendar uma operação que me descapitaliza.

#### Acceptance Criteria

1. THE Gestor_de_Portfolio SHALL distinguir patrimônio total, capital líquido, reserva, capital destinado a imóveis, capital disponível no momento, capital comprometido e capital livre.
2. THE Gestor_de_Portfolio SHALL avaliar o limite por operação contra o custo econômico total, e SHALL abster-se de avaliá-lo apenas contra o preço de aquisição.
3. THE Gestor_de_Portfolio SHALL aplicar o mais restritivo entre `INV-002`, `INV-015` e `INV-016` quando múltiplos limites forem aplicáveis.
4. IF o custo econômico total excede o limite por operação aplicável, THEN THE Motor_de_Decisao SHALL emitir `BLOCK` operacional por capital, exceto quando existir exceção formal registrada.
5. IF o capital livre após a operação simulada resulta inferior à reserva mínima aplicável, THEN THE Motor_de_Decisao SHALL emitir `BLOCK` operacional por reserva comprometida.
5.1. THE Gestor_de_Portfolio SHALL calcular a reserva mínima aplicável como o maior valor entre `INV-005` e o produto de `INV-019` pelo patrimônio líquido do investidor.
6. THE Gestor_de_Portfolio SHALL abster-se de considerar disponível a totalidade do capital, reservando sempre a reserva mínima aplicável.
6.1. THE Gestor_de_Portfolio SHALL registrar no perfil do investidor o esforço operacional aceitável `INV-020` e a meta de renda mensal `INV-021`, AND SHALL usar ambos como componentes do Investor Fit.
7. WHEN o capital livre é reduzido, THE Motor_de_Ranking SHALL priorizar eficiência de capital sobre retorno absoluto.
8. THE Gestor_de_Portfolio SHALL calcular as cinco métricas de eficiência: `eficiencia_de_capital = retorno líquido ÷ capital total`; `eficiencia_temporal = margem ÷ prazo em meses`; `renda_por_capital = renda líquida anual ÷ capital total`; `margem_por_capital = margem absoluta ÷ capital total`; e `renda_liquida_por_risco = renda líquida anual ÷ índice de severidade de risco da operação`.
9. THE Gestor_de_Portfolio SHALL considerar reservas específicas para custos inesperados, reforma, vacância e carregamento, e contingências jurídicas.

### Requirement 47: Concentração e diversificação

**User Story:** Como investidor, quero controlar concentração, para que um único fator não comprometa grande parte do meu capital.

#### Acceptance Criteria

1. THE Gestor_de_Portfolio SHALL controlar concentração por localização, por tipo de imóvel, por estratégia, por faixa de ticket, por fonte de origem e por nível de risco, aplicando os limites de `PORT-003`.
1.1. THE Gestor_de_Portfolio SHALL manter a alocação-alvo por estratégia `PORT-001`, SHALL calcular o desvio da carteira em relação a ela e SHALL comparar o desvio com `PORT-002`.
2. IF a concentração resultante excede o limite configurado para a dimensão avaliada, THEN THE Motor_de_Ranking SHALL reduzir a prioridade da oportunidade e THE Motor_de_Score SHALL aplicar penalidade ao componente `diversificacao` do Investor Fit.
3. WHEN a oportunidade melhora a diversificação desejada, THE Motor_de_Score SHALL elevar o componente `diversificacao` do Investor Fit.
3.1. WHEN a operação reduz o desvio da alocação-alvo, THE Motor_de_Ranking SHALL aplicar o bônus `PORT-005` ao ajuste de portfólio do score composto.
4. IF o capital imobilizado excede `PORT-004`, THEN THE Motor_de_Ranking SHALL aplicar a penalidade `PORT-006` ao ajuste de portfólio e SHALL reduzir a prioridade de novas oportunidades operacionalmente complexas.
4.1. THE Motor_de_Score SHALL computar concentração e diversificação exclusivamente no componente `diversificacao` do Investor Fit, AND SHALL abster-se de computá-las novamente no ajuste de portfólio do score composto.
5. THE Gestor_de_Portfolio SHALL representar o portfólio atual com ativo, valor investido, valor atual estimado, renda líquida, estratégia, liquidez, risco, localização e situação.
6. THE Gestor_de_Portfolio SHALL avaliar cada nova oportunidade no contexto do portfólio existente.

### Requirement 48: Simulação de alocação antes da decisão

**User Story:** Como investidor, quero simular o efeito da compra no meu portfólio antes de decidir, para enxergar o custo de oportunidade.

#### Acceptance Criteria

1. WHEN o investidor solicita a simulação de uma oportunidade, THE Gestor_de_Portfolio SHALL calcular o capital necessário, o capital residual, o percentual do portfólio, a exposição estratégica resultante, a exposição de risco resultante, o impacto na renda e a liquidez consolidada do portfólio.
2. THE Gestor_de_Portfolio SHALL executar a simulação também no cenário `conservador`.
3. THE Gestor_de_Portfolio SHALL comparar a oportunidade simulada com as demais oportunidades que competem pelo mesmo capital.
4. WHEN a simulação é concluída, THE Gestor_de_Portfolio SHALL emitir recomendação de alocação com justificativa.
5. THE Gestor_de_Portfolio SHALL comparar o retorno da oportunidade com alternativas de referência de custo de oportunidade configuradas pelo investidor.

---

### Domínio I — Score, Ranking e Motor de Decisão

### Requirement 49: Opportunity Score

**User Story:** Como investidor, quero uma nota de atratividade explicável, para comparar oportunidades objetivamente.

#### Acceptance Criteria

1. THE Motor_de_Score SHALL calcular o Opportunity Score na escala de 0 a 100 apenas após a aprovação das camadas 0 a 7 da precedência canônica.
2. THE Motor_de_Score SHALL compor o Opportunity Score a partir dos fatores `desconto_liquido`, `margem_seguranca`, `liquidez`, `localizacao`, `risco`, `yield_renda`, `valorizacao` e `qualidade_oportunidade`, cada um normalizado na escala de 0 a 100.
3. THE Motor_de_Score SHALL aplicar os pesos mestres da tabela SCORE quando nenhum peso específico de estratégia estiver vigente.
4. WHERE existem pesos específicos da estratégia avaliada, THE Motor_de_Score SHALL aplicar os pesos da estratégia e SHALL registrar qual conjunto de pesos foi usado.
5. THE Motor_de_Score SHALL rejeitar conjuntos de pesos cuja soma seja diferente de 1,00.
6. THE Motor_de_Score SHALL classificar o Opportunity Score nas faixas da tabela SCORE e SHALL usar o valor numérico para ranking.
7. THE Motor_de_Score SHALL registrar a contribuição individual de cada fator ao score final.
8. THE Motor_de_Score SHALL registrar a versão dos pesos utilizada em cada cálculo.
9. IF os dados mínimos definidos em `CONF-006` não estão disponíveis, THEN THE Motor_de_Score SHALL abster-se de emitir Opportunity Score e SHALL registrar score indefinido.

### Requirement 50: Confiança consolidada

**User Story:** Como investidor, quero que a confiança seja independente do score, para distinguir oportunidade boa de oportunidade comprovada.

#### Acceptance Criteria

1. THE Motor_de_Score SHALL calcular a confiança consolidada na escala de 0 a 100 a partir das dimensões `CONF-001` a `CONF-005`.
2. THE Motor_de_Score SHALL manter a confiança consolidada como dimensão independente do Opportunity Score e do nível de risco.
3. THE Motor_de_Score SHALL derivar o fator de confiança da confiança consolidada conforme `CONF-007`.
4. THE Motor_de_Score SHALL calcular a confiança consolidada de forma determinística, versionada e reproduzível a partir das dimensões registradas.
5. IF uma dimensão de confiança obrigatória para a etapa é `UNKNOWN` OR apresenta evidências conflitantes, THEN THE Motor_de_Score SHALL classificar a confiança consolidada como `inconclusiva` e THE Motor_de_Decisao SHALL emitir `PENDENTE` ou `BLOCK` conforme a criticidade da dimensão afetada.
5.1. THE Motor_de_Score SHALL derivar o nível nomeado de confiança conforme `CONF-010`, AND SHALL abster-se de usar qualquer rótulo fora dos seis níveis ali definidos.
6. IF a confiança consolidada é inferior a `GLB-003`, THEN THE Motor_de_Decisao SHALL impedir a decisão `BUY`.
7. THE Motor_de_Score SHALL abster-se de usar a confiança consolidada para contornar qualquer camada de bloqueio.

### Requirement 51: Investor Fit Score

**User Story:** Como investidor, quero saber se uma oportunidade boa é adequada a mim, porque essas são perguntas diferentes.

#### Acceptance Criteria

1. THE Motor_de_Score SHALL calcular o Investor Fit Score na escala de 0 a 100 a partir dos **sete** componentes `aderencia_estrategia`, `aderencia_risco`, `liquidez_vs_necessidade`, `aderencia_capital`, `diversificacao`, `esforco_operacional` e `horizonte`, com os pesos de `SCORE-006`.
1.1. THE Motor_de_Score SHALL abster-se de incluir qualquer componente de qualidade econômica no Investor Fit Score, porque a qualidade econômica é o Opportunity Score e a separação entre os dois scores é obrigatória.
2. THE Motor_de_Score SHALL manter o Investor Fit Score separado do Opportunity Score em todos os registros e apresentações.
3. IF o Investor Fit Score é inferior a `investor_fit_minimo`, THEN THE Motor_de_Decisao SHALL emitir `DO_NOT_BUY` ou SHALL reduzir a prioridade conforme a parametrização vigente.
4. THE Motor_de_Score SHALL abster-se de usar o Investor Fit Score para converter um `BLOCK` em `BUY`.
5. IF o capital ou a reserva do investidor são excedidos, THEN THE Motor_de_Decisao SHALL emitir `BLOCK` operacional por capital, prevalecendo a regra mais restritiva.
6. THE Radar SHALL permitir que o mesmo imóvel possua Investor Fit Scores diferentes para investidores ou estratégias diferentes.

### Requirement 52: Score composto e ranking

**User Story:** Como investidor, quero uma fila priorizada e explicada, para saber onde investir meu tempo agora.

#### Acceptance Criteria

1. THE Motor_de_Ranking SHALL calcular o score de prioridade conforme `SCORE-008`, como o produto de **cinco** fatores: `Opportunity Score × fator de confiança × fator de Investor Fit × ajuste de capital × ajuste de portfólio`.
1.1. THE Motor_de_Ranking SHALL compor o ajuste de portfólio a partir do bônus de equilíbrio de estratégias `PORT-005` e da penalização por capital imobilizado `PORT-006`, AND SHALL abster-se de incluir concentração e diversificação nesse ajuste.
2. THE Motor_de_Ranking SHALL normalizar cada fator multiplicativo na faixa de 0 a 1 para evitar distorção de escala.
3. THE Motor_de_Ranking SHALL excluir do ranking operacional toda oportunidade com decisão `BLOCK`.
4. THE Motor_de_Ranking SHALL ordenar as oportunidades pelo score de prioridade e SHALL aplicar, em caso de empate, os critérios de desempate na ordem: maior aderência à estratégia; maior confiança; maior margem de segurança; maior liquidez; menor risco; menor capital necessário; melhor efeito de diversificação; maior urgência.
4.1. WHERE a estratégia avaliada define ordem de desempate própria em `PORT-008`, THE Motor_de_Ranking SHALL aplicar a ordem da estratégia e SHALL registrar qual ordem foi aplicada.
5. THE Motor_de_Ranking SHALL permitir a ordenação do ranking de forma absoluta, relativa, por estratégia, por portfólio e por janela temporal.
6. THE Motor_de_Ranking SHALL classificar a urgência em `P0` janela curta, evento crítico ou oportunidade excepcional; `P1` excelente e pronta para análise; `P2` muito boa sem urgência; `P3` interessante e requer enriquecimento; `P4` monitoramento; e `BLOCK` fora do ranking operacional.
6.1. THE Motor_de_Ranking SHALL classificar a atratividade combinada em `A1` a `A5`, combinando atratividade, aderência e capital, AND SHALL manter esta escala nominalmente distinta da escala de urgência conforme `SCORE-009`.
6.2. THE Motor_de_Ranking SHALL aplicar as faixas de ação por posição de `PORT-007`, definindo a profundidade de investigação devida a cada posição.
7. THE Motor_de_Ranking SHALL manter atratividade e urgência como dimensões independentes.
8. THE Motor_de_Ranking SHALL identificar as oportunidades que competem pelo mesmo capital disponível.
9. THE Motor_de_Ranking SHALL destacar o conjunto de oportunidades não dominadas em retorno, risco, liquidez e capital.
10. WHEN a posição de uma oportunidade é apresentada, THE Motor_de_Explicabilidade SHALL informar a razão da posição, a razão de não estar em primeiro lugar, a condição que a faria subir, a condição que a faria cair, o risco principal e a pendência principal.
11. THE Motor_de_Ranking SHALL registrar a versão dos pesos e das regras usadas em cada cálculo de ranking, com a data e a hora do cálculo.
12. THE Motor_de_Ranking SHALL preservar o histórico das posições anteriores de cada oportunidade.

### Requirement 53: Precedência canônica de decisão

**User Story:** Como investidor, quero uma ordem única de decisão, para que nenhum score alto esconda um problema grave.

#### Acceptance Criteria

1. THE Motor_de_Decisao SHALL avaliar exatamente **onze camadas**, numeradas de 0 a 10, na ordem: camada 0 bloqueios críticos; camada 1 validade jurídica; camada 2 elegibilidade; camada 3 dados e confiança; camada 4 economia; camada 5 estratégia; camada 6 risco; camada 7 liquidez; camada 8 score; camada 9 capital e concentração; camada 10 ranking.
1.1. THE Motor_de_Decisao SHALL tratar a decisão final como a **saída** da avaliação das onze camadas, AND SHALL abster-se de tratá-la como uma camada adicional.
1.2. THE Motor_de_Decisao SHALL avaliar, dentro da camada 0, o risco de severidade `critico`, a ocupação com impacto crítico sem estratégia de desocupação, a posse litigiosa com evidência de litígio, a regra eliminatória expressa do investidor e o comprometimento da reserva mínima aplicável.
1.3. THE Motor_de_Decisao SHALL avaliar, dentro da camada 1, o resultado do Gate_Juridico e as 19 verificações de `R12.9`.
1.4. THE Motor_de_Decisao SHALL avaliar, dentro da camada 2, a identidade mínima `I2`, a localização, o tipo de imóvel e o ticket em relação a `PRI-001` e `PRI-002`.
1.5. THE Motor_de_Decisao SHALL avaliar, dentro da camada 3, a confiança consolidada em relação a `GLB-003`, a confiança do valuation em relação a `VAL-009` e as pendências abertas.
1.6. THE Motor_de_Decisao SHALL avaliar, dentro da camada 4, o desconto líquido, a margem, o preço máximo, o `roi_anualizado` em relação a `GLB-011` e, como sub-verificação, a robustez do cenário conservador.
1.7. THE Motor_de_Decisao SHALL avaliar, dentro da camada 5, a aderência à estratégia, o `yield_liquido_mensal_min`, o `prazo_saida_max` e os critérios próprios de cada estratégia.
1.8. THE Motor_de_Decisao SHALL avaliar, dentro da camada 6, os riscos de severidade `alto` e `medio`, e as verificações `RULE-OCC-001`, `RULE-OCC-002`, `RULE-LOC-001` e `RULE-LOC-002`.
1.9. THE Motor_de_Decisao SHALL avaliar, dentro da camada 7, o `liquidez_min` da estratégia, o limiar de `R40.8` e as compensações `LIQ-010` e `LIQ-011`.
1.10. THE Motor_de_Decisao SHALL avaliar, dentro da camada 8, o Opportunity Score, o score mínimo de `SCORE-004` e a matriz de `R55`.
1.11. THE Motor_de_Decisao SHALL avaliar, dentro da camada 9, o Investor Fit mínimo, os limites de capital de `R46` e os limites de concentração de `PORT-003`.
1.12. THE Motor_de_Decisao SHALL avaliar, dentro da camada 10, a posição no ranking e as faixas de ação de `PORT-007`.
2. THE Motor_de_Decisao SHALL avaliar uma camada apenas quando a camada anterior não eliminou a oportunidade.
3. WHEN uma ou mais camadas eliminam a oportunidade, THE Motor_de_Decisao SHALL reportar como camada determinante a de **menor índice** entre elas.
4. THE Motor_de_Decisao SHALL abster-se de permitir que uma camada posterior anule o resultado eliminatório de uma camada anterior.
5. THE Motor_de_Decisao SHALL emitir a decisão final em exatamente um dos estados `BUY`, `BUY_IF`, `MONITOR`, `DO_NOT_BUY` ou `BLOCK`.
6. WHEN a decisão é `BUY`, THE Motor_de_Decisao SHALL verificar previamente que não existe bloqueio crítico, que o gate jurídico é `OK`, que a oportunidade é elegível, que a confiança consolidada é igual ou superior a `GLB-003`, que o desconto líquido e a margem atendem à estratégia, que a tese sobrevive ao cenário `conservador`, que nenhum risco `alto` permanece sem mitigação registrada, que a liquidez atende ao mínimo da estratégia, que o Opportunity Score atende ao mínimo da estratégia, que o Investor Fit atende ao mínimo, que o capital, a reserva e a concentração são respeitados, e que não existe pendência de prioridade `critica` ou `alta` em aberto.
7. WHEN a decisão é `BUY_IF`, THE Motor_de_Decisao SHALL registrar pelo menos uma condição objetiva, verificável, com impacto conhecido na tese e com teto de preço quando aplicável.
8. WHEN a decisão é `MONITOR`, THE Motor_de_Decisao SHALL registrar o motivo do monitoramento e pelo menos um gatilho objetivo de reentrada.
9. WHEN a decisão é `DO_NOT_BUY`, THE Motor_de_Decisao SHALL registrar a justificativa econômica ou estratégica que a determinou.
10. WHEN a decisão é `BLOCK`, THE Motor_de_Decisao SHALL registrar o motivo impeditivo e, quando existir, a condição de desbloqueio.
11. THE Motor_de_Decisao SHALL distinguir `DO_NOT_BUY`, que é decisão econômica ou estratégica, de `BLOCK`, que é impedimento ou risco impeditivo.

### Requirement 54: Tipos de regra e resolução de conflitos

**User Story:** Como curador de regras, quero tipos de regra explícitos e precedência definida, para que o comportamento seja previsível.

#### Acceptance Criteria

1. THE Radar SHALL classificar cada regra em exatamente um tipo: `hard`, `soft`, `conditional`, `informational`, `strategy` ou `exception`.
2. THE Motor_de_Decisao SHALL avaliar as regras `hard` antes de qualquer cálculo de score.
3. THE Motor_de_Score SHALL aplicar as regras `soft` como ajuste de score, sem eliminar a oportunidade.
4. THE Motor_de_Decisao SHALL converter uma regra `conditional` satisfeita em liberação e uma regra `conditional` não satisfeita em `BUY_IF`.
5. THE Gestor_de_Alertas SHALL tratar as regras `informational` como geradoras de evento, sem efeito decisório.
6. THE Motor_de_Decisao SHALL resolver conflitos entre regras pela precedência: bloqueio jurídico ou risco crítico prevalece sobre todos; restrição legal ou documental prevalece sobre regra de exclusão; regra de exclusão prevalece sobre regra condicional; regra condicional prevalece sobre preferência de estratégia; preferência de estratégia prevalece sobre preferência de tipo de imóvel; preferência de tipo de imóvel prevalece sobre score e ranking.
7. THE Motor_de_Decisao SHALL resolver conflito entre regra `hard` e score mantendo o resultado da regra `hard`.
8. THE Motor_de_Decisao SHALL resolver conflito entre dado `CONFIRMED` e dado `ESTIMATED` adotando o dado `CONFIRMED`.
9. THE Motor_de_Decisao SHALL resolver conflito entre versões de regra adotando a versão vigente na data da análise e SHALL preservar o histórico das versões anteriores.
10. THE Motor_de_Decisao SHALL resolver conflito entre regra global e regra de estratégia adotando a **regra de estratégia**, por ser o escopo mais específico, AND SHALL adotar a regra global apenas quando esta impõe bloqueio crítico ou restrição legal ou documental.
10.1. THE Motor_de_Decisao SHALL aplicar a mesma precedência a todo par de escopos da hierarquia de configuração: o escopo mais específico prevalece, exceto quando o menos específico impõe bloqueio crítico ou restrição legal ou documental.
11. THE Motor_de_Decisao SHALL resolver conflito entre preço atual e preço histórico usando o preço atual para a decisão e o preço histórico para o histórico.

### Requirement 55: Matriz de ação por score e confiança

**User Story:** Como investidor, quero saber como score e confiança se combinam, para calibrar minha expectativa de ação.

#### Acceptance Criteria

1. WHERE o Opportunity Score está entre 90 e 100 e a confiança consolidada é igual ou superior a 75, THE Motor_de_Decisao SHALL emitir `BUY` quando as demais camadas estiverem satisfeitas.
2. WHERE o Opportunity Score está entre 90 e 100 e a confiança consolidada está entre 60 e 74, THE Motor_de_Decisao SHALL emitir `BUY_IF`.
3. WHERE o Opportunity Score está entre 90 e 100 e a confiança consolidada é inferior a 60, THE Motor_de_Decisao SHALL emitir `MONITOR`.
4. WHERE o Opportunity Score está entre 80 e 89 e a confiança consolidada é igual ou superior a 75, THE Motor_de_Decisao SHALL emitir `BUY` ou `BUY_IF` conforme a robustez do cenário.
5. WHERE o Opportunity Score está entre 70 e 79 e a confiança consolidada é igual ou superior a 75, THE Motor_de_Decisao SHALL emitir `BUY` ou `BUY_IF` conforme a robustez do cenário.
6. WHERE o Opportunity Score está entre 60 e 69 e a confiança consolidada é igual ou superior a 75, THE Motor_de_Decisao SHALL emitir `MONITOR` ou `BUY_IF`.
7. WHERE o Opportunity Score é inferior a 60, THE Motor_de_Decisao SHALL emitir `DO_NOT_BUY`.
8. WHERE existe `BLOCK` em qualquer camada, THE Motor_de_Decisao SHALL emitir `BLOCK` independentemente do Opportunity Score e da confiança.
9. WHERE a confiança consolidada é `inconclusiva`, THE Motor_de_Decisao SHALL emitir `PENDENTE` ou `BLOCK` conforme a criticidade da dimensão ausente ou conflitante, AND SHALL abster-se de emitir qualquer recomendação de compra.
10. WHERE o Opportunity Score está entre 80 e 89 e a confiança consolidada está entre 60 e 74, THE Motor_de_Decisao SHALL emitir `BUY_IF`.
11. WHERE o Opportunity Score está entre 80 e 89 e a confiança consolidada é inferior a 60, THE Motor_de_Decisao SHALL emitir `MONITOR`.
12. WHERE o Opportunity Score está entre 70 e 79 e a confiança consolidada está entre 60 e 74, THE Motor_de_Decisao SHALL emitir `MONITOR` ou `BUY_IF`.
13. WHERE o Opportunity Score está entre 70 e 79 e a confiança consolidada é inferior a 60, THE Motor_de_Decisao SHALL emitir `MONITOR`.
14. WHERE o Opportunity Score está entre 60 e 69 e a confiança consolidada está entre 60 e 74, THE Motor_de_Decisao SHALL emitir `MONITOR`.
15. WHERE o Opportunity Score está entre 60 e 69 e a confiança consolidada é inferior a 60, THE Motor_de_Decisao SHALL emitir `DO_NOT_BUY`.
16. THE Motor_de_Decisao SHALL tratar a matriz abaixo como a enumeração completa e exaustiva das combinações de faixa de score e faixa de confiança.

**Matriz de ação por score × confiança** `[CANÔNICO]` — 15 células mais a linha de bloqueio.
As faixas de confiança são as de `CONF-007`: alta ≥ 75, média 60–74, baixa < 60.

| Score | Confiança alta (≥ 75) | Confiança média (60–74) | Confiança baixa (< 60) |
|-------|-----------------------|-------------------------|------------------------|
| 90–100 | `BUY` | `BUY_IF` | `MONITOR` |
| 80–89 | `BUY` ou `BUY_IF` | `BUY_IF` | `MONITOR` |
| 70–79 | `BUY` ou `BUY_IF` | `MONITOR` ou `BUY_IF` | `MONITOR` |
| 60–69 | `MONITOR` ou `BUY_IF` | `MONITOR` | `DO_NOT_BUY` |
| < 60 | `DO_NOT_BUY` | `DO_NOT_BUY` | `DO_NOT_BUY` |
| `BLOCK` em qualquer camada | `BLOCK` | `BLOCK` | `BLOCK` |

A célula 60–69 com confiança baixa é `DO_NOT_BUY`, e não `MONITOR`: com score apenas
interessante e evidência fraca não existe tese a manter viva, apenas investigação a fazer.
A matriz é o limite superior da decisão; as camadas 0 a 9 podem sempre produzir resultado
mais restritivo.

### Requirement 56: Explicabilidade obrigatória

**User Story:** Como investidor, quero entender e poder discordar de cada conclusão, apontando exatamente qual premissa mudar.

#### Acceptance Criteria

1. WHEN uma decisão é emitida, THE Motor_de_Explicabilidade SHALL produzir a tese de investimento em uma frase, as principais evidências, os principais riscos, as pendências, as condições para compra, o preço máximo, os resultados dos cenários conservador, base e estressado, a próxima ação, a data da análise e as versões de regras e parâmetros aplicadas.
2. THE Motor_de_Explicabilidade SHALL responder, para cada oportunidade recomendada: por que apareceu; por que está barata; quanto vale; quanto realmente custa; qual o desconto líquido; qual a margem; qual o risco; qual a liquidez; para qual estratégia serve; por que é adequada ao investidor; o que ainda precisa ser confirmado; e o que faria a tese deixar de ser válida.
3. THE Motor_de_Explicabilidade SHALL informar a camada que determinou a decisão e a regra que a determinou.
4. THE Motor_de_Explicabilidade SHALL informar a contribuição de cada fator ao score e as penalidades aplicadas.
5. THE Motor_de_Explicabilidade SHALL identificar explicitamente cada valor como observado, confirmado, calculado, estimado, inferido ou desconhecido.
6. THE Motor_de_Explicabilidade SHALL apresentar cada exceção autorizada que influenciou o resultado.
7. THE Motor_de_Explicabilidade SHALL produzir a explicação em linguagem de negócio compreensível sem conhecimento técnico.
8. IF a explicação não pode ser vinculada a evidências e regras registradas, THEN THE Radar SHALL classificar a análise como incompleta e SHALL impedir o registro de decisão de compra.
9. THE Motor_de_Explicabilidade SHALL explicar também as rejeições e os bloqueios com o mesmo nível de detalhe das recomendações.

---

### Domínio J — Monitoramento, Alertas e Aprendizado

### Requirement 57: Monitoramento contínuo e materialidade

**User Story:** Como investidor, quero que a tese continue viva depois da primeira análise, para não perder oportunidades que melhoram.

#### Acceptance Criteria

1. THE Monitor SHALL acompanhar preço, valuation, comparáveis, aluguel, liquidez, risco, situação física, estratégia ativa, capital disponível e concentração do portfólio.
2. THE Monitor SHALL classificar cada mudança detectada em um nível de materialidade: `critico`, `alto`, `medio`, `baixo` ou `informativo`.
3. THE Monitor SHALL aplicar os limiares de materialidade `MON-001` a `MON-017` vigentes.
3.1. THE Monitor SHALL acompanhar obrigatoriamente os seis sinais de mercado `MON-012` a `MON-016`: aumento da oferta concorrente; queda dos preços de venda da região; alta dos aluguéis da região; melhora ou piora das condições de financiamento; melhora da infraestrutura da região; e entrada de nova concorrência forte.
3.2. WHEN uma nova oportunidade satisfaz `PRI-007` e não possui `BLOCK`, THE Monitor SHALL disparar `MON-017` e THE Gestor_de_Portfolio SHALL recomparar a carteira e o ranking automaticamente.
4. IF a materialidade da mudança é `critico`, THEN THE Motor_de_Decisao SHALL reavaliar imediatamente e SHALL emitir `BLOCK` quando o gatilho for risco impeditivo.
5. IF a materialidade da mudança é `alto`, THEN THE Orquestrador SHALL executar reavaliação completa.
6. IF a materialidade da mudança é `medio`, THEN THE Orquestrador SHALL executar reavaliação parcial das dimensões afetadas.
7. IF a materialidade da mudança é `baixo` ou `informativo`, THEN THE Monitor SHALL registrar a mudança no histórico sem disparar reavaliação.
8. WHEN uma reavaliação é executada, THE Monitor SHALL registrar quais dimensões foram reprocessadas e o motivo.
9. THE Monitor SHALL reprocessar apenas as camadas afetadas pela mudança detectada e SHALL propagar o efeito ao score e ao ranking.
10. WHILE uma oportunidade está em `MONITORED`, THE Monitor SHALL manter registrados o motivo do monitoramento, a tese atual, o gatilho de reentrada, o gatilho de abandono, o preço-alvo, o score mínimo, a liquidez mínima, as pendências relevantes e a data da próxima revisão.
10.1. THE Monitor SHALL manter o objeto de monitoramento em exatamente um dos dez estados: `ativo`, `aguardando_preco`, `aguardando_evidencia`, `aguardando_liquidez`, `aguardando_condicao_de_compra`, `aguardando_decisao_do_investidor`, `suspenso_pelo_investidor`, `reaberto`, `abandonado` e `encerrado`.
10.2. WHEN o estado do objeto de monitoramento muda, THE Monitor SHALL registrar o estado anterior, o novo estado, o gatilho e a data, AND SHALL preservar o histórico completo das transições.
11. WHILE uma oportunidade está em `DECIDED` com estado `BUY_IF`, THE Monitor SHALL acompanhar cada condição objetiva registrada e SHALL emitir o alerta `ALT-007` quando uma condição for satisfeita.

### Requirement 58: Reentrada e abandono de tese

**User Story:** Como investidor, quero que oportunidades rejeitadas voltem quando os fatos mudarem, sem eu precisar reprocurá-las.

#### Acceptance Criteria

1. WHEN o preço cai ao patamar de interesse configurado, THE Monitor SHALL reabrir a análise da oportunidade com nova versão.
2. WHEN um risco anteriormente impeditivo é resolvido com evidência, THE Monitor SHALL reabrir a análise da oportunidade.
3. WHEN a liquidez melhora acima do mínimo da estratégia, THE Monitor SHALL reabrir a análise da oportunidade.
4. WHEN o valuation aumenta materialmente, THE Monitor SHALL reabrir a análise da oportunidade.
5. WHEN uma nova estratégia passa a aceitar o imóvel, THE Monitor SHALL recalcular a aderência e o Investor Fit.
6. WHEN dados anteriormente desconhecidos são confirmados, THE Monitor SHALL reabrir a análise da oportunidade.
7. WHEN o investidor abandona uma tese, THE Radar SHALL exigir o registro do motivo entre margem desaparecida, preço máximo ultrapassado, risco inaceitável, liquidez abaixo do mínimo, demanda inexistente, custo de reforma inviável, capital indisponível ou alternativa claramente superior.
8. WHEN uma tese é abandonada, THE Radar SHALL preservar o histórico completo e SHALL permitir a reabertura quando o gatilho configurado ocorrer.

### Requirement 59: Alertas acionáveis

**User Story:** Como investidor, quero poucos alertas relevantes com ação sugerida, para não ser inundado de ruído.

#### Acceptance Criteria

1. WHEN um alerta é emitido, THE Gestor_de_Alertas SHALL informar o evento, o impacto quantificado, a consequência na tese e a próxima ação recomendada.
2. THE Gestor_de_Alertas SHALL atribuir a cada alerta uma prioridade entre `P0` crítico, `P1` urgente, `P2` alto, `P3` médio, `P4` baixo e `informativo`.
3. THE Gestor_de_Alertas SHALL emitir os alertas do catálogo `ALT-001` a `ALT-020` conforme os gatilhos vigentes.
3.1. THE Gestor_de_Alertas SHALL emitir os três alertas de ranking `ALT-017` subiu 20 ou mais posições, `ALT-018` saiu do Top 10 e `ALT-019` passou a `BLOCK`.
4. THE Gestor_de_Alertas SHALL agrupar alertas relacionados de uma mesma oportunidade em uma única notificação.
5. THE Gestor_de_Alertas SHALL abster-se de emitir dois alertas para o mesmo fato sem que exista mudança material entre eles.
6. THE Gestor_de_Alertas SHALL respeitar o limite `frequencia_maxima_por_oportunidade` vigente.
7. THE Gestor_de_Alertas SHALL permitir que o investidor configure tipos de alerta ativos, prioridade mínima, estratégias observadas, regiões observadas, preço-alvo, score mínimo, margem mínima, eventos de risco e frequência de resumo.
8. THE Gestor_de_Alertas SHALL permitir que o investidor silencie os alertas de uma oportunidade específica sem encerrar o monitoramento.
9. WHEN o investidor aciona um alerta, THE Interface_do_Investidor SHALL apresentar diretamente o contexto que motivou o alerta.
10. THE Gestor_de_Alertas SHALL elevar a prioridade de um alerta somente quando a situação subjacente piorar.

### Requirement 60: Resultado real, backtest e aprendizado

**User Story:** Como investidor, quero saber onde o Radar erra, para calibrar as regras com evidência.

#### Acceptance Criteria

1. WHEN uma aquisição é registrada, THE Radar SHALL registrar preço efetivamente pago, custos reais, custo real de reforma, prazo real de reforma, aluguel realizado, vacância real, preço de venda efetivo, prazo real de saída e retorno realizado.
2. THE Motor_de_Backtest SHALL comparar previsto e realizado para valuation, reforma, aluguel, prazo, custo, liquidez e retorno.
3. THE Motor_de_Backtest SHALL medir precisão, recall, taxa de falso positivo, taxa de falso negativo, erro de valuation, erro de prazo, erro de aluguel e erro de custo.
3.1. THE Motor_de_Backtest SHALL manter no backtest a coorte de oportunidades **rejeitadas** e a coorte de oportunidades **ignoradas**, com o resultado observado de cada uma, AND SHALL usá-las como população do indicador de falso negativo.
3.2. THE Motor_de_Backtest SHALL registrar o indicador de falso positivo como a proporção de oportunidades recomendadas cujo resultado observado não confirmou a tese, e o indicador de falso negativo como a proporção de oportunidades rejeitadas ou ignoradas cujo resultado observado teria confirmado a tese.
3.3. THE Motor_de_Backtest SHALL aplicar controle de sobreajuste, separando a amostra de calibração da amostra de verificação e SHALL registrar o desempenho em ambas antes de propor qualquer calibração.
3.4. IF o desempenho na amostra de calibração supera o desempenho na amostra de verificação além do limiar configurado, THEN THE Motor_de_Backtest SHALL rejeitar a proposta de calibração e SHALL registrar o indício de sobreajuste.
4. WHEN o backtest é executado, THE Motor_de_Backtest SHALL reproduzir o estado histórico usando exclusivamente as informações disponíveis na data original e as versões de regras e parâmetros vigentes naquela data.
5. THE Motor_de_Backtest SHALL rejeitar a utilização de informação posterior à data da decisão avaliada.
6. WHEN o aprendizado identifica um padrão, THE Motor_de_Backtest SHALL propor a calibração, SHALL medir o impacto histórico da proposta e SHALL registrar a proposta como rascunho.
7. THE Motor_de_Backtest SHALL abster-se de alterar automaticamente qualquer regra classificada como crítica.
8. THE Motor_de_Backtest SHALL comparar a versão vigente com a versão proposta antes de qualquer publicação.
9. WHEN uma regra apresenta taxa de falso positivo acima do limiar configurado, THE Gestor_de_Alertas SHALL emitir o alerta `ALT-015`.
10. THE Radar SHALL registrar conhecimento negativo, incluindo regiões com liquidez superestimada, tipos de imóvel com reforma problemática, estimativas de aluguel excessivamente otimistas, riscos recorrentes, estratégias que falharam e regras que produziram falsos positivos.
11. THE Radar SHALL registrar conhecimento positivo contextualizado por cidade, região, tipo, faixa de ticket, estratégia, liquidez, yield observado e perfil histórico de risco.

---

### Domínio K — Governança, Auditoria e Versionamento

### Requirement 61: Snapshot imutável da análise

**User Story:** Como auditor, quero reconstruir qualquer decisão passada, para entender por que ela foi tomada naquela data.

#### Acceptance Criteria

1. WHEN uma análise é persistida, THE Gestor_de_Governanca SHALL criar uma nova versão com numeração crescente por oportunidade.
2. THE Gestor_de_Governanca SHALL preservar as análises anteriores sem sobrescrita.
3. WHEN uma análise é persistida, THE Gestor_de_Governanca SHALL gravar as evidências, os fatos, as pendências, os riscos, os custos, os valuations, os cenários, os comparáveis, os scores, o ranking e a decisão vinculados àquela versão.
4. WHEN uma análise é persistida, THE Gestor_de_Governanca SHALL registrar a versão das regras, a versão dos parâmetros, a versão dos pesos de score, a versão do grafo de orquestração, a versão do modelo de linguagem e a versão dos prompts aplicáveis.
5. WHEN uma nova análise da mesma oportunidade é executada, THE Orquestrador SHALL consultar as versões anteriores como contexto AND SHALL abster-se de tratá-las como evidência atual.
6. THE Gestor_de_Governanca SHALL identificar a análise vigente como a de maior número de versão.
7. THE Gestor_de_Governanca SHALL registrar, para cada análise, a identificação da oportunidade, a data e hora, o estado, o Opportunity Score, o Investor Fit, a confiança, o valuation, o custo, o risco, a liquidez, a estratégia, as regras aplicadas, as exceções, a justificativa e as evidências.

### Requirement 62: Versionamento de regras e parâmetros

**User Story:** Como gestor, quero que mudanças relevantes gerem nova versão, para que o passado não seja reescrito.

#### Acceptance Criteria

1. THE Gestor_de_Governanca SHALL atribuir a cada regra e a cada parâmetro um identificador, uma versão, uma data de criação, uma data de início de vigência, uma data de encerramento quando aplicável, uma situação e um motivo de mudança.
2. THE Gestor_de_Governanca SHALL classificar cada objeto governado em uma situação: `rascunho`, `em_revisao`, `aprovado`, `ativo`, `retirado` ou `historico`.
3. WHEN uma mudança pode alterar uma decisão, THE Gestor_de_Governanca SHALL criar uma nova versão do objeto governado.
4. THE Gestor_de_Governanca SHALL classificar o nível de mudança em `baixo` para texto e classificação informativa, `medio` para parâmetro operacional, `alto` para peso de score e para mudança de faixa de classificação, e `critico` para regra de bloqueio.
4.1. WHERE a mudança altera os limites de qualquer faixa de classificação de score, de confiança, de liquidez, de severidade ou de aderência, THE Gestor_de_Governanca SHALL classificar o nível de mudança como `alto`, SHALL exigir backtest e SHALL exigir aprovação registrada antes da vigência.
5. IF o nível de mudança é `alto`, THEN THE Gestor_de_Governanca SHALL exigir aprovação registrada antes da vigência.
6. IF o nível de mudança é `critico`, THEN THE Gestor_de_Governanca SHALL exigir aprovação formal registrada, evidência e preservação do histórico antes da vigência.
7. IF a mudança altera a fórmula do score ou introduz novo componente, THEN THE Gestor_de_Governanca SHALL exigir a execução de backtest antes da aprovação.
8. THE Gestor_de_Governanca SHALL aplicar uma nova versão apenas às análises executadas a partir da data de vigência.
9. THE Gestor_de_Governanca SHALL registrar o valor anterior, o valor novo, o motivo e o aprovador em cada alteração de parâmetro ou peso.
10. THE Gestor_de_Parametros SHALL resolver cada parâmetro pela hierarquia de escopo vigente e SHALL registrar qual escopo forneceu o valor aplicado.
11. THE Gestor_de_Parametros SHALL rejeitar a aplicação de parâmetro sem versão vigente.
12. WHEN um parâmetro é removido, THE Gestor_de_Governanca SHALL preservar o histórico das análises que o utilizaram.

### Requirement 63: Exceções auditáveis

**User Story:** Como gestor, quero que exceções sejam explícitas e temporárias, para não virarem regra silenciosa.

#### Acceptance Criteria

1. WHEN uma exceção é criada, THE Gestor_de_Governanca SHALL exigir o registro da regra excepcionada, do valor normal, do valor excepcional, do risco aceito, da justificativa, da evidência, da alçada de aprovação, do prazo de validade e do impacto no score.
2. THE Gestor_de_Governanca SHALL preservar a regra original ativa e SHALL registrar a exceção como registro adicional.
3. THE Gestor_de_Governanca SHALL rejeitar a criação de exceção sem justificativa ou sem evidência.
4. THE Gestor_de_Governanca SHALL rejeitar exceção que contorne bloqueio jurídico ou risco crítico, independentemente da alçada de aprovação invocada.
4.1. THE Gestor_de_Governanca SHALL manter a proibição do critério 4 como absoluta, sem exceção por autorização. Esta é um **endurecimento deliberado** em relação à documentação de origem, que admitia a superação de bloqueio crítico "com autorização adequada" (`D40`).
5. WHEN o prazo de validade de uma exceção expira, THE Gestor_de_Governanca SHALL restaurar a regra padrão e SHALL disparar reavaliação das oportunidades afetadas.
6. THE Motor_de_Explicabilidade SHALL apresentar toda exceção aplicada na explicação da decisão.
7. WHEN uma mesma regra é excepcionada de forma recorrente acima do limiar configurado, THE Gestor_de_Governanca SHALL registrar recomendação de revisão da regra.

### Requirement 64: Trilha de auditoria

**User Story:** Como auditor, quero uma trilha completa de eventos, para verificar integridade e responsabilidade.

#### Acceptance Criteria

1. THE Gestor_de_Governanca SHALL registrar em trilha append-only os eventos: captura criada; oferta normalizada; imóvel identificado; fontes associadas; duplicidade resolvida; conflito registrado; valuation alterado; custo alterado; risco criado; risco resolvido; regra aplicada; score alterado; ranking alterado; alerta emitido; pendência criada; pendência resolvida; decisão registrada; exceção criada; exceção expirada; parâmetro alterado; regra versionada; resultado real registrado.
2. WHEN um evento é registrado, THE Gestor_de_Governanca SHALL gravar data e hora, ator, papel exercido, objeto afetado, valor anterior, valor novo e motivo.
3. THE Gestor_de_Governanca SHALL abster-se de permitir a exclusão ou a alteração de registros da trilha de auditoria.
4. THE Gestor_de_Governanca SHALL registrar, para cada execução de análise, um identificador de execução, o identificador do imóvel, a versão do grafo, o agente e o nó executados, o modelo e a versão de prompt quando aplicável, a ferramenta invocada, o hash das entradas e das saídas, a latência, a contagem de tokens, as recuperações realizadas, os identificadores de evidência e de regra, os erros e a decisão resultante.
5. THE Gestor_de_Governanca SHALL manter os indicadores de governança: proporção de decisões reproduzíveis; proporção de regras com versão; proporção de decisões com justificativa; proporção de decisões com evidência; proporção de exceções justificadas; proporção de mudanças auditáveis; e quantidade de dados sem origem.

### Requirement 65: Controle de qualidade das regras

**User Story:** Como curador de regras, quero verificar coerência e cobertura antes de publicar, para não introduzir contradição.

#### Acceptance Criteria

1. WHEN uma regra é submetida para aprovação, THE Gestor_de_Governanca SHALL verificar coerência com as demais regras vigentes, cobertura dos cenários relevantes, comportamento nos limites, reprodutibilidade das decisões históricas, melhoria comprovada por backtest, suficiência da evidência conforme o critério 1.1 e clareza da explicabilidade.
1.1. THE Gestor_de_Governanca SHALL classificar a qualidade de cada evidência em exatamente um dos cinco níveis: `forte` documento oficial ou registral com localização exata; `boa` documento oficial sem localização exata, ou registro de terceiro verificável; `moderada` informação de fonte identificada sem documento; `fraca` estimativa, inferência ou fonte não verificável; `ausente` sem evidência.
1.2. THE Gestor_de_Governanca SHALL considerar a evidência suficiente para uma regra jurídica crítica apenas quando a qualidade for `forte` ou `boa`.
1.3. THE Gestor_de_Governanca SHALL registrar o nível de qualidade da evidência em cada verificação avaliada, AND SHALL propagá-lo à confiança da dimensão correspondente.
2. IF uma regra submetida contradiz uma regra vigente, THEN THE Gestor_de_Governanca SHALL rejeitar a submissão e SHALL registrar a contradição identificada.
3. IF uma regra submetida altera decisões históricas, THEN THE Gestor_de_Governanca SHALL exigir registro explícito do impacto antes da aprovação.
4. THE Gestor_de_Governanca SHALL exigir que toda regra jurídica crítica possua fonte e proveniência registradas.
5. THE Gestor_de_Governanca SHALL exigir que toda regra com condição ambígua possua campo de interpretação preenchido.
6. THE Gestor_de_Governanca SHALL exigir que todo Golden Case possua resultado esperado e a lista de fatos que o invalidariam.

---

### Domínio L — Interface e Experiência do Investidor

### Requirement 66: Navegação e visões do Radar

**User Story:** Como investidor, quero entender em segundos o que merece minha atenção hoje.

#### Acceptance Criteria

1. THE Interface_do_Investidor SHALL disponibilizar as áreas: visão geral, radar de oportunidades, minhas oportunidades, análises, due diligence, alertas, mercado, estratégias, configurações, histórico, relatórios e backtest.
2. THE Interface_do_Investidor SHALL apresentar na visão geral as oportunidades novas, as melhores oportunidades por estratégia, as mudanças relevantes, os alertas críticos, as análises pendentes, as teses em monitoramento e os indicadores consolidados.
3. THE Interface_do_Investidor SHALL permitir filtrar o radar por estratégia, localização, tipo, preço, desconto nominal, desconto de mercado, desconto líquido, margem, yield, liquidez, score, risco, confiança, situação e fonte.
4. THE Interface_do_Investidor SHALL permitir ordenar o radar por melhor score, maior margem, maior desconto líquido, maior yield, maior liquidez, maior confiança, mais recente e maior melhoria.
4.1. THE Interface_do_Investidor SHALL disponibilizar as **oito visões pré-definidas** do radar: Top oportunidades; por estratégia; por região; novidades; queda de preço; score crescente; em monitoramento; e bloqueadas com motivo.
4.2. THE Interface_do_Investidor SHALL apresentar a visão de bloqueadas com a camada determinante e o motivo impeditivo de cada oportunidade, AND SHALL manter estas oportunidades fora do ranking operacional.
5. THE Interface_do_Investidor SHALL apresentar, em cada card de oportunidade, tipo e localização, preço, valor de mercado base, custo econômico total, desconto líquido, margem, yield quando aplicável, liquidez, score, confiança, risco, estratégia mais aderente e o motivo principal.
6. THE Interface_do_Investidor SHALL disponibilizar em cada card as ações salvar, analisar, monitorar, rejeitar e criar alerta.
7. THE Interface_do_Investidor SHALL apresentar preço sempre acompanhado do valor de mercado e do custo econômico total.
8. THE Interface_do_Investidor SHALL apresentar score sempre acompanhado da explicação da composição.
9. THE Interface_do_Investidor SHALL apresentar valuation sempre acompanhado da confiança.
10. THE Interface_do_Investidor SHALL apresentar risco e confiança em posição visível na visão resumida.
11. THE Interface_do_Investidor SHALL identificar visualmente cada valor como observado, confirmado, calculado, estimado, inferido ou desconhecido.
12. THE Interface_do_Investidor SHALL permitir o aprofundamento progressivo do resumo para o detalhe e do detalhe para a evidência original.

### Requirement 67: Ficha da oportunidade

**User Story:** Como investidor, quero uma ficha que reúna a tese completa, para decidir sem abrir dezenas de telas.

#### Acceptance Criteria

1. THE Interface_do_Investidor SHALL apresentar na ficha os blocos resumo executivo, imóvel, preço e histórico, mercado, economia, estratégias, riscos, pendências, evidências, due diligence, linha do tempo e decisão.
2. THE Interface_do_Investidor SHALL apresentar no cabeçalho da ficha a classificação, o score da estratégia ativa, a confiança, o preço atual, a faixa de valor de mercado, o custo econômico total, a margem em valor e percentual, o nível de risco, a situação no workflow e a recomendação.
3. THE Interface_do_Investidor SHALL apresentar a recomendação acompanhada de uma frase explicativa.
4. THE Interface_do_Investidor SHALL apresentar na visão de mercado a lista de comparáveis com distância, preço por metro quadrado, área, quartos, vagas, condição, fonte, data, classe de qualidade e ajustes aplicados.
5. THE Interface_do_Investidor SHALL disponibilizar acesso à evidência original de cada comparável quando esta evidência existir.
6. THE Interface_do_Investidor SHALL apresentar na visão de economia os blocos aquisição, tributos e documentos, débitos, reforma, regularização, financeiro, saída, total, valor de mercado por cenário e resultado.
7. THE Interface_do_Investidor SHALL permitir que o investidor altere premissas em um cenário derivado, preservando o cenário original.
8. THE Interface_do_Investidor SHALL apresentar os quatro cenários econômicos e o resultado de cada um.
9. THE Interface_do_Investidor SHALL apresentar, por estratégia, o nome, o objetivo, a aderência, o score, os pontos fortes, os pontos fracos, as condições de aprovação e a recomendação.
10. THE Interface_do_Investidor SHALL apresentar na visão de explicabilidade por que a oportunidade entrou, por que pontuou alto, por que perdeu pontos, qual o risco, qual a incerteza, o que precisa ser confirmado e o que invalidaria a tese.
11. THE Interface_do_Investidor SHALL apresentar a due diligence como checklist com progresso, e cada pendência com responsável, prioridade, prazo, evidência e impacto na decisão.
12. THE Interface_do_Investidor SHALL apresentar a linha do tempo com captura inicial, alterações de preço, alterações de status, novos comparáveis, alterações de valuation, alterações de score, novos riscos, pendências resolvidas, decisões e reavaliações.

### Requirement 68: Comparação, rejeição e monitoramento na interface

**User Story:** Como investidor, quero comparar e descartar oportunidades rapidamente, sem perder o histórico.

#### Acceptance Criteria

1. THE Interface_do_Investidor SHALL permitir a comparação simultânea de duas a cinco oportunidades, apresentando preço, valor de mercado, custo total, desconto líquido, margem, yield, liquidez, risco, confiança, score, pendências e estratégia.
2. WHEN o investidor rejeita uma oportunidade, THE Interface_do_Investidor SHALL exigir a seleção de um motivo entre preço, mercado, liquidez, localização, risco, documentação, reforma, estratégia, dados e outro, e SHALL exigir texto livre obrigatório quando o motivo for outro.
3. WHEN uma oportunidade é rejeitada, THE Radar SHALL preservar a oportunidade no histórico e SHALL permitir o retorno desta oportunidade ao radar quando as condições mudarem.
4. THE Interface_do_Investidor SHALL apresentar na visão de monitoramento o motivo do monitoramento, a condição de entrada, o score atual, a data da última atualização, o próximo gatilho e os alertas relacionados.
5. WHEN o investidor seleciona uma estratégia ativa, THE Interface_do_Investidor SHALL reinterpretar filtros prioritários, score, ranking, explicação e indicadores apresentados, AND SHALL preservar inalterados os dados fundamentais do imóvel.
6. THE Interface_do_Investidor SHALL separar filtro de visualização de regra eliminatória, e SHALL abster-se de eliminar oportunidades em razão de filtro de visualização.
7. THE Interface_do_Investidor SHALL registrar a decisão do investidor entre interessado, não interessado, monitorar, analisar, descartar, favorito, já analisado e adquirido, e SHALL preservar cada registro no histórico.

### Requirement 69: Relatórios de negócio

**User Story:** Como investidor, quero visões consolidadas, para avaliar o desempenho do meu processo.

#### Acceptance Criteria

1. THE Interface_do_Investidor SHALL disponibilizar relatórios de radar diário, melhores oportunidades, oportunidades por estratégia, oportunidades por região, mudanças de preço, oportunidades bloqueadas com motivos, risco por severidade, pendências de due diligence, evolução do score, desempenho das regras, histórico de decisões, resultado por estratégia e taxa de conversão em aquisição.
2. THE Interface_do_Investidor SHALL apresentar em cada relatório a data de referência e as versões de regras e parâmetros aplicadas.
3. THE Radar SHALL manter os indicadores de negócio: oportunidades relevantes por mês; taxa de falso positivo; taxa de oportunidades analisadas; margem média das oportunidades; desconto real médio; tempo entre captura e alerta; proporção de oportunidades com alta confiança; oportunidades que chegaram à aquisição; e resultado realizado.
4. THE Radar SHALL manter os indicadores do pipeline: tempo de capturado a qualificado; tempo de qualificado a análise; duração da due diligence; taxa de pendências resolvidas; taxa de aprovação; taxa de reprovação; proporção de alertas acionáveis; e taxa de falso alerta.

---

### Domínio M — Orquestração e Arquitetura de IA

### Requirement 70: Orquestração com ordem obrigatória

**User Story:** Como responsável técnico, quero que a ordem das etapas seja garantida pela orquestração, para que nenhuma análise pule um gate.

#### Acceptance Criteria

1. THE Orquestrador SHALL executar as etapas na ordem: normalização; identidade; deduplicação; **qualificação**; **consolidação de perfil**; validade jurídica; enriquecimento; mercado e valuation; economia; risco; liquidez; estratégia; regras; score; Investor Fit; ranking; decisão; explicação; persistência; memória.
1.1. THE Orquestrador SHALL registrar as fases `QUALIFIED` e `CONSOLIDATED` no traço de execução, AND SHALL abster-se de executar a validade jurídica antes de ambas.
2. IF o Gate_Juridico retorna `BLOCK`, THEN THE Orquestrador SHALL desviar para a decisão sem executar as etapas subsequentes de mercado, economia, liquidez, estratégia e score.
3. IF a identidade é inferior a `I2`, THEN THE Orquestrador SHALL desviar para a decisão.
4. IF um bloqueio crítico é confirmado em qualquer etapa, THEN THE Orquestrador SHALL desviar para a decisão.
5. WHEN cada etapa conclui, THE Orquestrador SHALL atualizar a fase do pipeline conforme a máquina de estados canônica.
6. THE Orquestrador SHALL manter o estado compartilhado como único meio de comunicação entre as etapas.
7. THE Orquestrador SHALL exigir intervenção humana registrada nos pontos mínimos enumerados em `R83.5`, AND SHALL permitir a configuração de pontos adicionais sem remover os mínimos.
8. WHEN a análise termina, THE Orquestrador SHALL produzir a explicação consolidada e SHALL persistir o snapshot da análise.
9. THE Orquestrador SHALL registrar a versão do grafo de orquestração em cada execução.

### Requirement 71: Guarda-corpos dos componentes de IA

**User Story:** Como responsável técnico, quero que o modelo de linguagem não decida regra crítica, para manter o determinismo das decisões.

#### Acceptance Criteria

1. THE Radar SHALL executar os cálculos financeiros exclusivamente no Motor_de_Calculo, de forma determinística.
2. THE Radar SHALL executar a precedência de decisão exclusivamente no Motor_de_Decisao, de forma determinística.
3. THE Base_de_Conhecimento SHALL recuperar definições, regras, checklists, exceções, casos e documentação, AND SHALL abster-se de executar cálculos críticos e de emitir decisão.
4. THE Radar SHALL restringir os agentes de linguagem à interpretação de documentos, à seleção de regras aplicáveis, à formulação de perguntas de investigação, à explicação de achados e à coordenação de ferramentas.
5. THE Radar SHALL rejeitar a criação de evidência por agente de linguagem.
6. THE Radar SHALL rejeitar o preenchimento de lacuna jurídica por suposição de agente de linguagem.
7. THE Radar SHALL rejeitar a afirmação de consulta a fonte que não foi efetivamente consultada.
8. THE Radar SHALL apresentar conflitos entre fontes em lugar de ocultá-los.
9. THE Radar SHALL indicar, em conclusões jurídicas, a dependência de legislação e jurisprudência vigentes.
10. THE Radar SHALL registrar cada ferramenta invocada, com entradas, saídas e resultado, na trilha de auditoria.

### Requirement 72: Ingestão de conhecimento e memória

**User Story:** Como responsável técnico, quero que todo documento passe pela mesma esteira, para que nada seja conhecimento apenas por estar em uma pasta.

#### Acceptance Criteria

1. WHEN um documento é adicionado, THE Base_de_Conhecimento SHALL executar a esteira de fingerprint, catalogação da fonte, extração, limpeza, classificação, segmentação semântica, atribuição de metadados, geração de representação vetorial e persistência.
2. THE Base_de_Conhecimento SHALL classificar cada segmento em exatamente um dos **quinze** tipos: `REGRA`, `DEFINICAO`, `FORMULA`, `CHECKLIST`, `EVIDENCIA`, `CASO`, `ANALISE`, `MANUAL`, `PARAMETER`, `EXCEPTION`, `DECISION`, `GOVERNANCE`, `EVIDENCE_GUIDE`, `STRATEGY` ou `SAFETY`.
2.1. THE Base_de_Conhecimento SHALL indexar os princípios invioláveis `SAFE-001` a `SAFE-017` como `SAFETY`, as exceções `EXC-001` a `EXC-009` como `EXCEPTION`, o catálogo normativo de parâmetros como `PARAMETER`, as Decisões de Consolidação como `DECISION`, os requisitos de governança como `GOVERNANCE`, os critérios de qualidade de evidência como `EVIDENCE_GUIDE` e os critérios por estratégia como `STRATEGY`.
3. THE Base_de_Conhecimento SHALL registrar, para cada segmento, identificador do documento, identificador da seção, identificador do segmento, tipo, domínio, tópico, identificador de regra, identificador de checklist, identificador de caso, estratégia, tipo de fonte, identificador da fonte, versão, início e fim de vigência, data de criação, prioridade, tipo de entidade, jurisdição e confiança.
3.1. THE Base_de_Conhecimento SHALL armazenar o texto-fonte e a paráfrase em campos distintos e explicitamente rotulados, AND SHALL rejeitar a indexação de segmento em que o texto-fonte e a paráfrase estejam fundidos no mesmo campo.
3.2. WHEN um segmento é recuperado, THE Base_de_Conhecimento SHALL informar qual parte do conteúdo é texto-fonte e qual é paráfrase.
4. THE Base_de_Conhecimento SHALL rejeitar a indexação de item crítico sem identificador.
5. THE Base_de_Conhecimento SHALL rejeitar a indexação de regra jurídica crítica sem fonte e proveniência.
6. THE Base_de_Conhecimento SHALL rejeitar a indexação de parâmetro histórico sem a marcação de que o parâmetro não é universal.
7. THE Radar SHALL manter três camadas de memória: conhecimento normativo; histórico estruturado de análises e eventos; contexto específico do imóvel com casos semelhantes.
8. WHEN uma nova análise é iniciada, THE Orquestrador SHALL recuperar as análises anteriores, as decisões, as pendências, as evidências recentes, as alterações e os casos semelhantes como contexto.
9. THE Radar SHALL registrar cada item recuperado da memória histórica como hipótese e SHALL abster-se de tratá-lo como evidência atual.

### Requirement 73: Testes de invariantes e Golden Cases

**User Story:** Como responsável técnico, quero invariantes verificadas automaticamente, para que os princípios invioláveis não regridam.

#### Acceptance Criteria

1. THE Radar SHALL manter um conjunto de Golden Cases com resultado esperado e a lista de fatos que invalidariam o resultado.
2. THE Radar SHALL manter testes que verifiquem que nenhuma evidência é criada sem fonte.
3. THE Radar SHALL manter testes que verifiquem que `UNKNOWN` não se transforma em `CONFIRMED` sem nova evidência.
4. THE Radar SHALL manter testes que verifiquem que score, desconto, margem, yield, liquidez e Investor Fit não superam um `BLOCK`.
5. THE Radar SHALL manter testes que verifiquem que toda decisão está vinculada a evidências e regras registradas.
6. THE Radar SHALL manter testes que verifiquem que o histórico não é convertido em fato atual.
7. THE Radar SHALL manter testes que verifiquem os cálculos determinísticos contra os valores publicados nos Golden Cases do Anexo F, incluindo a verificação inversa do preço máximo de `F.1.5`.
8. THE Radar SHALL manter os testes de regressão `REG-001` a `REG-035` do Anexo E.

---

### Domínio N — Dicionário de Entidades, Escopo e Priorização

### Requirement 74: Entidades e campos obrigatórios do dicionário

**User Story:** Como responsável técnico, quero que toda entidade que as regras exigem exista no dicionário, para que nenhuma regra dependa de estrutura inexistente.

#### Acceptance Criteria

1. THE Radar SHALL manter **Localização** como entidade própria, com endereço, região, classe de localização, perfil de demanda, liquidez regional e faixa de preço predominante.
2. THE Radar SHALL manter **Due Diligence** como entidade própria, com escopo, fase, situação, pendências vinculadas, evidências vinculadas e resultado consolidado.
3. THE Radar SHALL manter **Score** como entidade própria com composição, registrando score bruto, componentes, pesos aplicados, bônus, penalizações, confiança, score final, estratégia avaliada e versão dos pesos.
4. THE Radar SHALL manter **Versão do Perfil Consolidado** como entidade própria, com numeração, data, campos alterados, autor ou processo e motivo.
5. THE Radar SHALL manter **Histórico de Preços** como entidade própria, com valor, moeda, data de observação, fonte, tipo de preço e variação em relação à observação anterior.
6. THE Radar SHALL manter **Divergência** como entidade própria, com data, fonte A, informação A, fonte B, informação B, dimensão afetada, materialidade e impacto na decisão.
7. THE Radar SHALL manter **Posição de Portfólio** como entidade própria, com ativo, valor investido, valor atual estimado, renda líquida, estratégia, liquidez, risco, localização e situação.
8. THE Radar SHALL manter **Resultado Real** como entidade própria, com os campos exigidos por `R60.1`.
9. THE Normalizador SHALL extrair e registrar o campo `banheiros` como característica física do imóvel.
10. THE Normalizador SHALL extrair e registrar o campo `complemento` do endereço, distinto de logradouro, número e unidade.
11. THE Radar SHALL rejeitar a aplicação de qualquer regra que dependa de entidade ou campo ausente do dicionário, AND SHALL reportar o requisito dependente como NÃO AVALIADO.

### Requirement 75: Escopo, priorização e controle de escopo

**User Story:** Como gestor, quero saber o que entra na primeira versão e em que ordem, para que a ordem de implementação seja derivável do documento.

#### Acceptance Criteria

1. THE Radar SHALL tratar como capacidades `P0`, obrigatórias na primeira versão operacional, exatamente **23** capacidades: `P0-01` fonte e captura; `P0-02` normalização; `P0-03` identificação do imóvel; `P0-04` deduplicação básica; `P0-05` perfil consolidado; `P0-06` comparáveis; `P0-07` valuation; `P0-08` custo econômico total; `P0-09` desconto e margem; `P0-10` risco básico; `P0-11` liquidez básica; `P0-12` estratégia; `P0-13` regras; `P0-14` Opportunity Score; `P0-15` Investor Fit; `P0-16` ranking; `P0-17` explicabilidade; `P0-18` análise profunda; `P0-19` pendências e evidências; `P0-20` decisão; `P0-21` histórico; `P0-22` monitoramento básico; e `P0-23` validade jurídica do procedimento.
2. THE Radar SHALL tratar como capacidades `P1`, posteriores à primeira versão, exatamente **nove** capacidades: novas fontes e instituições; mais automações de enriquecimento; alertas avançados; monitoramento mais sofisticado; mais estratégias; backtest ampliado; modelos de liquidez mais sofisticados; comparação avançada de portfólio; e relatórios avançados.
3. THE Radar SHALL tratar como capacidades `P2`, de evolução, exatamente **oito** capacidades: aprendizado estatístico avançado; predições mais sofisticadas; expansão ampla de mercados; modelos específicos por submercado; automação da due diligence; inteligência avançada de documentos; novos canais de comunicação; e recursos colaborativos.
4. THE Radar SHALL tratar como **fora da primeira versão** exatamente **nove** itens: cobertura de todas as instituições; cobertura de todos os portais; aplicativo completo; automação jurídica completa; aprendizado de máquina avançado; execução automática de compra; gestão patrimonial completa; marketplace; e definição da arquitetura técnica definitiva.
5. THE Radar SHALL atribuir a cada requisito deste documento exatamente uma classificação de prioridade entre `P0`, `P1`, `P2` e `fora do MVP`, registrada no Índice de Requisitos.
6. WHEN uma nova necessidade é proposta, THE Gestor_de_Governanca SHALL classificá-la em exatamente uma das seis categorias de controle de escopo: `P0 obrigatório` entra na primeira versão; `P1 importante` entra no backlog posterior; `P2 evolução` entra no roteiro; `experimento` é testado separadamente; `fora da tese` não entra; `mudança estrutural` exige revisão de impacto antes de alterar a base.
7. IF uma necessidade é classificada como `mudança estrutural`, THEN THE Gestor_de_Governanca SHALL exigir registro de impacto sobre requisitos, parâmetros e regras vigentes antes de qualquer alteração.

### Requirement 76: Análise profunda

**User Story:** Como investidor, quero uma análise estruturada com argumentos dos dois lados, para decidir com a tese testada e não apenas pontuada.

#### Acceptance Criteria

1. WHEN uma análise profunda é aberta, THE Radar SHALL exigir o registro da tese de investimento em uma frase.
2. THE Radar SHALL exigir o registro dos argumentos a favor da tese, cada um vinculado a evidência ou a métrica calculada.
3. THE Radar SHALL exigir o registro dos argumentos contra a tese, cada um vinculado a evidência, risco ou pendência.
4. THE Radar SHALL exigir o registro de um contraponto para cada argumento contra, ou o registro explícito de que não existe contraponto.
5. THE Radar SHALL exigir resposta registrada para as **oito** perguntas da análise profunda: por que isso é uma oportunidade; o valor estimado é defensável; a margem continua boa após os custos; é possível sair quando necessário; o que pode destruir a tese; o que ainda não se sabe; a tese sobrevive ao cenário estressado; e a conclusão entre comprar, condicionar, monitorar ou rejeitar.
6. IF qualquer das oito perguntas do critério 5 está sem resposta registrada, THEN THE Motor_de_Decisao SHALL impedir a decisão `BUY` e SHALL classificar a análise profunda como incompleta.
7. THE Motor_de_Explicabilidade SHALL apresentar os argumentos a favor, os argumentos contra e os contrapontos na explicação da decisão.
8. THE Radar SHALL preservar cada versão da análise profunda no histórico, sem sobrescrita.

### Requirement 77: Cenários como espaço de teste de premissas

**User Story:** Como investidor, quero testar minhas próprias premissas sem destruir o cenário original, para entender onde a tese quebra.

#### Acceptance Criteria

1. THE Interface_do_Investidor SHALL apresentar os quatro cenários `otimista`, `base`, `conservador` e `estressado` com as premissas de cada um explicitadas.
2. WHEN o investidor altera uma premissa, THE Radar SHALL criar um cenário derivado identificado, SHALL preservar o cenário de origem e SHALL registrar quais premissas foram alteradas.
3. THE Radar SHALL recalcular, no cenário derivado, o custo econômico total, o desconto líquido, a margem, o ROI líquido, o `roi_anualizado`, o yield líquido, o prazo e a robustez.
4. THE Radar SHALL apresentar, para cada cenário, a resposta à pergunta de robustez: a tese continua funcionando se as premissas piorarem.
5. THE Radar SHALL marcar todo cenário derivado pelo investidor como hipótese, AND SHALL abster-se de usá-lo como base de decisão sem registro explícito de adoção.
6. THE Radar SHALL registrar o autor, a data e o motivo de cada cenário derivado.

### Requirement 78: Configurações do investidor

**User Story:** Como investidor, quero configurar meu perfil em um lugar só, para que todas as regras passem a refletir meus critérios.

#### Acceptance Criteria

1. THE Interface_do_Investidor SHALL disponibilizar a configuração do perfil organizada em exatamente **doze** grupos: capital; ticket; estratégias; localização; tipos de imóvel; desconto; margem; yield; liquidez; risco; reforma; e alertas.
2. THE Interface_do_Investidor SHALL apresentar, no grupo capital, capital disponível, reserva absoluta, reserva percentual do patrimônio líquido, entrada máxima e parcela máxima.
3. THE Interface_do_Investidor SHALL apresentar, no grupo estratégias, as estratégias ativas, a prioridade de cada uma e a alocação-alvo `PORT-001`.
4. THE Interface_do_Investidor SHALL apresentar, no grupo localização, as listas prioritária, aceitável, condicional e bloqueada.
5. WHEN uma configuração é alterada, THE Gestor_de_Governanca SHALL criar nova versão do parâmetro correspondente, SHALL registrar valor anterior, valor novo, autor e data, AND SHALL disparar reprocessamento conforme `MON-006` e `MON-007`.
6. THE Interface_do_Investidor SHALL apresentar, para cada configuração, o identificador do parâmetro correspondente do catálogo normativo e o escopo em que o valor se aplica.
7. THE Interface_do_Investidor SHALL rejeitar configuração que contorne bloqueio jurídico ou risco crítico.

### Requirement 79: Interface de programação

**User Story:** Como responsável técnico, quero que toda capacidade apresentada na interface tenha contrato de programação, para que a interface não dependa de comportamento não especificado.

#### Acceptance Criteria

1. THE Radar SHALL expor a visão geral consolidada, retornando oportunidades novas, melhores por estratégia, mudanças relevantes, alertas críticos, análises pendentes, teses em monitoramento e indicadores consolidados.
2. THE Radar SHALL expor as ações do card de oportunidade: salvar, monitorar e criar alerta, cada uma registrando ator, papel, data e motivo quando aplicável.
3. THE Radar SHALL expor a linha do tempo de uma oportunidade, retornando os eventos de `R67.12` em ordem cronológica com a versão de análise correspondente.
4. THE Radar SHALL expor a comparação de duas a cinco oportunidades, retornando os indicadores de `R68.1`.
5. IF a comparação recebe menos de duas ou mais de cinco oportunidades, THEN THE Radar SHALL rejeitar a requisição com a causa explicitada.
6. THE Radar SHALL expor a visão de monitoramento, retornando motivo, condição de entrada, estado do objeto de monitoramento, score atual, data da última atualização, próximo gatilho e alertas relacionados.
7. THE Radar SHALL expor o registro das **oito** decisões do investidor: interessado; não interessado; monitorar; analisar; descartar; favorito; já analisado; e adquirido.
8. THE Radar SHALL exigir autenticação e autorização em toda operação exposta, AND SHALL rejeitar requisição não autenticada.
9. WHEN uma requisição contém valor fora de domínio, THE Radar SHALL rejeitá-la informando o campo e a causa, AND SHALL abster-se de retornar erro genérico de execução.
10. THE Radar SHALL registrar cada operação exposta na trilha de auditoria conforme `R64.2`.

### Requirement 80: Qualidade de evidência e indicadores de aprendizado

**User Story:** Como gestor, quero medir onde o Radar erra nas duas direções, para calibrar sem trocar um erro por outro.

#### Acceptance Criteria

1. THE Gestor_de_Governanca SHALL manter o indicador de falso positivo e o indicador de falso negativo como métricas distintas e publicadas em conjunto.
2. THE Motor_de_Backtest SHALL calcular o indicador de falso negativo sobre a coorte de oportunidades rejeitadas e ignoradas de `R60.3.1`.
3. IF a coorte de rejeitadas e ignoradas está vazia, THEN THE Motor_de_Backtest SHALL reportar o indicador de falso negativo como NÃO AVALIADO, AND SHALL abster-se de reportá-lo como zero.
4. WHEN uma calibração é proposta, THE Motor_de_Backtest SHALL apresentar o efeito simultâneo sobre os dois indicadores, AND SHALL registrar a troca aceita.
5. THE Gestor_de_Governanca SHALL classificar a qualidade da evidência de cada verificação conforme `R65.1.1` e SHALL publicar a distribuição de qualidade por domínio.

### Requirement 81: Alocação, eficiência de capital e faixas de ação

**User Story:** Como investidor, quero saber quanto devo alocar em cada tese e o que fazer com cada faixa do ranking, para transformar o ranking em ação.

#### Acceptance Criteria

1. THE Gestor_de_Portfolio SHALL manter a alocação-alvo por estratégia `PORT-001` como configuração versionada e SHALL apresentar o desvio atual da carteira.
2. THE Gestor_de_Portfolio SHALL apresentar as cinco métricas de eficiência de `R46.8` por operação e consolidadas para a carteira.
3. THE Motor_de_Ranking SHALL aplicar as faixas de ação `PORT-007`, atribuindo due diligence completa às posições 1 a 3, análise aprofundada às posições 4 a 10, monitoramento ativo às posições 11 a 30, monitoramento passivo às demais, e exclusão do ranking operacional às oportunidades `BLOCK`.
4. WHEN a posição de uma oportunidade muda de faixa de ação, THE Gestor_de_Alertas SHALL emitir `ALT-013`, `ALT-017` ou `ALT-018` conforme a direção e a magnitude da mudança.
5. THE Gestor_de_Portfolio SHALL comparar o desvio de alocação com `PORT-002` e SHALL registrar a recomendação de rebalanceamento quando o desvio for excedido.

### Requirement 82: Disciplina de lance e revalidação final

**User Story:** Como investidor, quero que a disciplina de lance seja verificável item a item, para que nenhuma liberação de lance dependa de memória.

#### Acceptance Criteria

1. THE Radar SHALL avaliar os **nove** hard stops `HS-01` a `HS-09` do Anexo C.3 e SHALL registrar o resultado de cada um com evidência.
2. IF qualquer hard stop está acionado, THEN THE Radar SHALL emitir `NAO_DAR_LANCE` independentemente do restante da avaliação.
3. THE Radar SHALL avaliar os **doze** itens pré-lance `PL-01` a `PL-12` do Anexo C.4 e SHALL registrar o resultado de cada um com data e responsável.
4. THE Radar SHALL avaliar as **nove** verificações de evicção `E01` a `E09` do Anexo C.2 e SHALL registrar o item e a página do edital que sustentam cada resultado.
5. THE Radar SHALL avaliar os **doze** itens da revalidação final do dia do lance `RL-01` a `RL-12` do Anexo C.7.
6. THE Radar SHALL emitir `PODE_DAR_LANCE` somente quando os doze itens `PL-01` a `PL-12` e os doze itens `RL-01` a `RL-12` estiverem satisfeitos, nenhum hard stop estiver acionado, o lance máximo autorizado e o lance máximo absoluto estiverem definidos, e o lance atual não exceder o lance máximo absoluto.
7. THE Radar SHALL registrar a comissão do leiloeiro como valor **fora do lance** e SHALL somá-la ao custo total de aquisição.
8. THE Radar SHALL registrar as **seis** verificações de histórico do leiloeiro do Anexo C.5: registro oficial na Junta Comercial; site oficial; experiência com a instituição vendedora; reclamações relevantes; histórico de divergências; e plataforma utilizada.
9. WHEN uma divergência documental é identificada, THE Radar SHALL registrá-la conforme `R74.6` e SHALL mantê-la aberta até a confirmação em fonte oficial.
10. IF existe divergência documental pendente, THEN THE Radar SHALL emitir `NAO_DAR_LANCE`.

### Requirement 83: Fronteira dos componentes de IA e intervenção humana

**User Story:** Como responsável técnico, quero a fronteira dos agentes escrita e a lista mínima de intervenção humana, para que não seja possível configurar zero supervisão.

#### Acceptance Criteria

1. THE Radar SHALL mapear cada agente de linguagem para uma função sem poder de decisão e sem poder de criação de evidência.
2. THE Radar SHALL restringir o agente de extração documental à produção de propostas de evidência, cada uma contendo o fato afirmado, o documento, a localização documental exata e a confiança da extração.
3. THE Camada_de_Evidencia SHALL promover uma proposta de evidência a evidência registrada somente por ato humano registrado OR por regra determinística explicitamente declarada.
4. THE Radar SHALL rejeitar a atribuição de valuation, de cálculo de custo econômico total ou de decisão a qualquer agente de linguagem.
5. THE Radar SHALL exigir intervenção humana registrada, no mínimo, nos seguintes pontos: promoção de evidência jurídica a `CONFIRMED`; aceitação de risco de severidade `alto`; criação de exceção; aprovação de mudança de nível `alto` ou `critico`; confirmação de divergência documental; liberação de lance; e registro de decisão de compra.
6. THE Radar SHALL rejeitar configuração que remova qualquer um dos pontos mínimos do critério 5.
7. THE Radar SHALL registrar, para cada intervenção humana, o ator, o papel exercido, a data, o objeto afetado e a justificativa.

---

# Anexo A — Checklist Mestre de Análise de Leilão (normativo, 136 itens)

Cada item é avaliado e registrado individualmente com resultado, evidência e
localização documental. A coluna **Ausente ⇒** define o resultado quando não há
evidência, em observância a SAFE-003 e a `P-E`. A coluna **Efeito** define o impacto no
gate ou no cálculo.

**Vocabulário da coluna "Ausente ⇒"** `[CANÔNICO]` (`D49`). A coluna usa exclusivamente os
seis resultados de item de checklist de `R36.3` — `confirmado`, `parcialmente_confirmado`,
`nao_confirmado`, `conflitante`, `nao_aplicavel`, `desconhecido` — combinados com a
prioridade de pendência de `R37.2` e com os estados de decisão de `R53.5`. A versão anterior
desta spec usava oito valores ad hoc, entre eles `REPROVADO` para itens em que a informação
apenas faltava. Pelo princípio `P-E`, `REPROVADO` fica reservado para **evidência de
irregularidade**; falta de informação é `PENDENTE` com prioridade proporcional ao impacto.

## A.1 Identificação (MC-001 a MC-007)

| ID | Verificação | Aprovado quando | Reprovado quando | Ausente ⇒ | Efeito | Regra |
|----|-------------|-----------------|------------------|-----------|--------|-------|
| MC-001 | Fonte, banco ou leiloeiro identificados | Fonte nomeada e rastreável | Fonte não identificável | `PENDENTE` | Gate G0 | RULE-ID-001 |
| MC-002 | Número do imóvel ou identificação da oferta | Identificador da fonte registrado | Identificadores conflitantes | `PENDENTE` | Gate G0 | RULE-ID-001 |
| MC-003 | Matrícula identificada | Número de matrícula registrado | Matrículas divergentes entre fontes | `PENDENTE` | Identidade ≤ I3 | RULE-ID-001 |
| MC-004 | Comarca e cartório identificados | Comarca ou cartório registrados | Contexto registral incompatível com o endereço | `PENDENTE` | Identidade ≤ I3 | RULE-ID-001 |
| MC-005 | Endereço completo conferido | Logradouro, número, unidade, bairro, município e UF conferidos | Endereço incompatível com a matrícula | `PENDENTE` | Identidade ≤ I2 | RULE-ID-001 |
| MC-006 | Área, unidade, vagas e características conferidas | Área com tipo declarado e características conferidas | Área da fonte incompatível com a matrícula | `PENDENTE` | Reduz confiança de valuation | RULE-ID-001 |
| MC-007 | Captura original preservada | Snapshot com fingerprint e data registrados | Captura comprovadamente alterada ou sobrescrita ⇒ `REPROVADO` | `PENDENTE` crítico | Gate G0 bloqueia análise | RULE-ID-001 |

## A.2 Matrícula e titularidade (MC-008 a MC-016)

| ID | Verificação | Aprovado quando | Reprovado quando | Ausente ⇒ | Efeito | Regra |
|----|-------------|-----------------|------------------|-----------|--------|-------|
| MC-008 | Matrícula atualizada obtida | Certidão dentro do prazo FRESH registral | Certidão fora do prazo sem justificativa | `PENDENTE` | P0 `PENDENTE` | RULE-ID-002 |
| MC-009 | Proprietário atual conferido | Titularidade coerente com a oferta | Titularidade incompatível | `PENDENTE` | Conflito material ⇒ `BLOCK` | RULE-ID-002 |
| MC-010 | Alienação fiduciária identificada | Contrato e garantia identificados na matrícula | Garantia inexistente para a modalidade analisada | `PENDENTE` | P0 `PENDENTE` | RULE-JUR-001 |
| MC-011 | Credor fiduciário identificado | Credor nomeado e coerente com o vendedor | Credor divergente do vendedor | `PENDENTE` | P0 `PENDENTE` | RULE-JUR-001 |
| MC-012 | Averbações relevantes analisadas | Todas as averbações lidas e classificadas | Averbação impeditiva vigente | `PENDENTE` | Averbação impeditiva ⇒ `BLOCK` | RULE-JUR-013 |
| MC-013 | Consolidação da propriedade comprovada, quando aplicável | Ato de consolidação averbado e legível | Consolidação exigida e ausente | `PENDENTE` | Impede `BUY`; `BLOCK` conforme fase | RULE-JUR-002 |
| MC-014 | Data da consolidação registrada | Data extraída do ato | Data incoerente com a cronologia | `PENDENTE` | Incoerência ⇒ `BLOCK` | RULE-JUR-013 |
| MC-015 | Ato ou averbação registral identificado | Número do ato registrado (ex.: AV-13) | Ato não localizável na matrícula | `PENDENTE` | P0 `PENDENTE` | RULE-JUR-013 |
| MC-016 | Inconsistências de titularidade inexistentes ou tratadas | Sem inconsistência, ou inconsistência com tratamento documentado | Inconsistência material sem tratamento | `PENDENTE` | `BLOCK` | RULE-ID-002 |

## A.3 Constituição em mora e notificações (MC-017 a MC-026)

| ID | Verificação | Aprovado quando | Reprovado quando | Ausente ⇒ | Efeito | Regra |
|----|-------------|-----------------|------------------|-----------|--------|-------|
| MC-017 | Devedor fiduciante identificado | Devedor nomeado na matrícula ou no contrato | Devedor divergente entre documentos | `PENDENTE` | P0 `PENDENTE` | RULE-JUR-004 |
| MC-018 | Constituição em mora localizada | Documento de constituição localizado | Irregularidade material comprovada | `PENDENTE` | Irregularidade ⇒ `BLOCK` | RULE-JUR-003 |
| MC-019 | Notificação para purgação da mora verificada | Prova de intimação localizada | Intimação comprovadamente irregular | `PENDENTE` | Irregularidade ⇒ `BLOCK` | RULE-JUR-004 |
| MC-020 | Data da notificação registrada | Data extraída da prova | Data incoerente com a cronologia | `PENDENTE` | Incoerência ⇒ `BLOCK`/`PENDENTE` | RULE-JUR-004 |
| MC-021 | Meio, endereço e destinatário conferidos | Meio, endereço e destinatário registrados | Destinatário ou endereço incorretos | `PENDENTE` | Irregularidade ⇒ `BLOCK` | RULE-JUR-004 |
| MC-022 | Prazo legal aplicável conferido | Prazo aplicável identificado e respeitado | Prazo comprovadamente desrespeitado | `PENDENTE` | `BLOCK` | RULE-JUR-004 |
| MC-023 | Evidência documental disponível | Documento anexado com localização | Documento inexistente | `PENDENTE` | Impede `BUY` | RULE-JUR-004 |
| MC-024 | Devolução, recusa ou ausência de recebimento analisada | Situação analisada e classificada | Ausência de recebimento sem intimação subsidiária | `PENDENTE` | `PENDENTE`/`BLOCK` | RULE-JUR-004 |
| MC-025 | Intimações legalmente exigíveis relacionadas ao leilão verificadas | Comunicações das datas dos leilões comprovadas | Ausência comprovada de comunicação exigível | `PENDENTE` | `BLOCK` | RULE-JUR-005 |
| MC-026 | Datas e destinatários das intimações conferidos | Datas e destinatários coerentes | Datas ou destinatários incoerentes | `PENDENTE` | `BLOCK`/`PENDENTE` | RULE-JUR-005 |

## A.4 Edital e cronologia do leilão (MC-027 a MC-034)

| ID | Verificação | Aprovado quando | Reprovado quando | Ausente ⇒ | Efeito | Regra |
|----|-------------|-----------------|------------------|-----------|--------|-------|
| MC-027 | Edital oficial obtido | Edital vigente com número, versão e fingerprint | Edital vigente não confirmado | `PENDENTE` | Hard stop de lance | RULE-ED-001 |
| MC-028 | Primeiro leilão identificado | Data, hora, plataforma e valor mínimo registrados | Dados do primeiro leilão inconsistentes | `PENDENTE` | P0 `PENDENTE` | RULE-ED-001 |
| MC-029 | Segundo leilão identificado, quando aplicável | Data, hora, plataforma e valor mínimo registrados | Dados do segundo leilão inconsistentes | `PENDENTE` | P0 `PENDENTE` | RULE-ED-001 |
| MC-030 | Datas e horários conferidos | Portal e edital coincidem | Divergência entre portal e edital | `PENDENTE` | Hard stop até confirmação | RULE-ED-001 |
| MC-031 | Resultado dos leilões conhecido | Resultado de cada praça registrado | Resultado incompatível com a oferta atual | `PENDENTE` | P0 `PENDENTE` | RULE-ED-001 |
| MC-032 | Cronologia mora → consolidação → leilão coerente | Sequência coerente com a modalidade | Conflito material de cronologia | `PENDENTE` | `BLOCK`/`PENDENTE` | RULE-JUR-006 |
| MC-033 | Matrícula e edital sem conflito material | Identificação, área e titularidade coincidem | Conflito material | `PENDENTE` | `BLOCK` | RULE-ED-001 |
| MC-034 | Regras específicas do edital analisadas | Cláusulas de custo, prazo, posse e obrigações registradas | Cláusula crítica incompatível com a tese | `PENDENTE` | `BLOCK` conforme cláusula | RULE-ED-001 |

## A.5 Processos judiciais e risco de nulidade (MC-035 a MC-043)

| ID | Verificação | Aprovado quando | Reprovado quando | Ausente ⇒ | Efeito | Regra |
|----|-------------|-----------------|------------------|-----------|--------|-------|
| MC-035 | Pesquisa judicial realizada | Pesquisa executada com data e escopo registrados | Pesquisa não realizada antes da decisão | `PENDENTE` | Impede `BUY` | RULE-JUR-007 |
| MC-036 | Processos envolvendo o devedor analisados | Processos listados e classificados | Processo com impacto material sem mitigação | `PENDENTE` | `BLOCK` | RULE-JUR-007 |
| MC-037 | Processos envolvendo imóvel ou matrícula analisados | Processos listados e classificados | Processo com impacto material sem mitigação | `PENDENTE` | `BLOCK` | RULE-JUR-007 |
| MC-038 | Ações anulatórias ou de sustação pesquisadas | Pesquisa específica registrada | Ação anulatória com efeito sobre o certame | `PENDENTE` | `BLOCK` | RULE-JUR-007 |
| MC-039 | Liminares e tutelas identificadas | Decisões listadas com efeito registrado | Liminar que atinge o leilão | `PENDENTE` | `BLOCK` | RULE-JUR-007 |
| MC-040 | Decisões relevantes analisadas | Teor e efeito de cada decisão registrados | Decisão impeditiva vigente | `PENDENTE` | `BLOCK` | RULE-JUR-007 |
| MC-041 | Fase atual registrada | Fase e última movimentação registradas | Fase indeterminável | `PENDENTE` | Reduz confiança jurídica | RULE-JUR-007 |
| MC-042 | Impacto sobre a validade do leilão classificado | Impacto classificado em nenhum, potencial, material mitigável ou material impeditivo | Impacto material impeditivo | `PENDENTE` | `BLOCK` quando impeditivo | RULE-JUR-007 |
| MC-043 | Processo não tratado como BLOCK automático apenas por existir | Classificação baseada em objeto, fase e efeito | Bloqueio emitido apenas pela existência do processo | — | Invariante de qualidade | RULE-JUR-007 |

## A.6 Ocupação (MC-044 a MC-052)

| ID | Verificação | Aprovado quando | Reprovado quando | Ausente ⇒ | Efeito | Regra |
|----|-------------|-----------------|------------------|-----------|--------|-------|
| MC-044 | Situação de ocupação conhecida | Situação determinada com evidência | Evidências conflitantes sem resolução | `PENDENTE` alta | Reduz confiança; `BLOCK` quando impacto crítico sem estratégia de desocupação, ou posse litigiosa com evidência de litígio | RULE-OCC-001, RULE-RSK-005 |
| MC-045 | Desocupado confirmado, ocupado ou desconhecido | Estado registrado entre os sete estados canônicos | Estado indeterminado com fontes divergentes | `PENDENTE` alta | Permite a continuidade da análise (`R18.3`) | RULE-OCC-001 |
| MC-046 | Ocupante identificado, quando possível | Ocupante identificado | Identificação incompatível com a matrícula | `PENDENTE` | Reduz confiança | RULE-OCC-001 |
| MC-047 | Proprietário ou devedor ocupa | Situação respondida com evidência | — | `PENDENTE` | Risco de posse `alto` | RULE-OCC-001 |
| MC-048 | Terceiro ocupa | Situação respondida com evidência | Posse de terceiro sem origem conhecida | `PENDENTE` | Risco de posse `alto` | RULE-OCC-002 |
| MC-049 | Inquilino ocupa | Situação respondida com evidência | Locação com efeitos não avaliados | `PENDENTE` | Risco de posse `alto` | RULE-LOC-001 |
| MC-050 | Evidência da ocupação registrada | Evidência com fonte, data e localização | Afirmação sem evidência | `PENDENTE` | Impede `BUY` | RULE-OCC-001 |
| MC-051 | Custo e prazo de desocupação estimados | Faixa de custo e prazo registrada | Custo tratado como zero sem evidência | `PENDENTE` | Contingência obrigatória | RULE-OCC-001 |
| MC-052 | Risco de posse separado do risco de nulidade | Registros em categorias distintas | Ocupação tratada como nulidade | — | Invariante de qualidade | RULE-OCC-002 |

## A.7 Locação e inquilino (MC-053 a MC-063)

| ID | Verificação | Aprovado quando | Reprovado quando | Ausente ⇒ | Efeito | Regra |
|----|-------------|-----------------|------------------|-----------|--------|-------|
| MC-053 | Existe contrato de locação | Resposta com evidência | — | `PENDENTE` | Reduz confiança | RULE-LOC-001 |
| MC-054 | Contrato obtido | Contrato anexado | Contrato existente e não obtido antes da decisão | `PENDENTE` | Impede `BUY` | RULE-LOC-002 |
| MC-055 | Data de início e término | Datas registradas | Datas incoerentes com a garantia | `PENDENTE` | `RISCO_JURIDICO` | RULE-LOC-002 |
| MC-056 | Valor do aluguel | Valor registrado | Valor incompatível com o mercado sem justificativa | `PENDENTE` | Ajusta yield e confiança | RULE-LOC-002 |
| MC-057 | Garantia | Modalidade de garantia registrada | Garantia inexistente em locação vigente | `PENDENTE` | Eleva risco de inadimplência | RULE-LOC-002 |
| MC-058 | Cláusula de vigência | Presença ou ausência registrada | Cláusula de vigência averbada não considerada | `PENDENTE` | Restringe prazo de saída | RULE-LOC-002 |
| MC-059 | Registro ou averbação na matrícula, quando aplicável | Situação registral da locação registrada | Averbação existente e ignorada | `PENDENTE` | Restringe posse | RULE-LOC-002 |
| MC-060 | Data do contrato comparada à garantia fiduciária | Comparação registrada | Comparação não realizada | `PENDENTE` | `RISCO_JURIDICO` | RULE-LOC-002 |
| MC-061 | Efeitos jurídicos da locação avaliados | Efeitos registrados com fundamento | Efeitos presumidos sem fundamento | `PENDENTE` | `PENDENTE`/`RISCO_JURIDICO` | RULE-LOC-001 |
| MC-062 | Impacto em posse, prazo e rentabilidade calculado | Impacto quantificado no cenário | Impacto não incorporado ao cenário | `PENDENTE` | Recalcular economia | RULE-LOC-002 |
| MC-063 | Nulidade não presumida pela existência de inquilino | Registros mantêm as categorias separadas | Nulidade presumida | — | Invariante de qualidade | RULE-LOC-002 |

## A.8 Dívidas e encargos (MC-064 a MC-069)

| ID | Verificação | Aprovado quando | Reprovado quando | Ausente ⇒ | Efeito | Regra |
|----|-------------|-----------------|------------------|-----------|--------|-------|
| MC-064 | Condomínio | Valor mensal e débitos confirmados com a administração | Débito relevante com responsabilidade indefinida | `PENDENTE` + contingência | Entra no TCO | RULE-ED-003 |
| MC-065 | IPTU | Situação cadastral e débitos confirmados | Débito relevante com responsabilidade indefinida | `PENDENTE` + contingência | Entra no TCO | RULE-ED-003 |
| MC-066 | Água, luz e outros encargos | Situação confirmada com as concessionárias | Encargo relevante desconhecido | `PENDENTE` + contingência | Entra no TCO | RULE-ED-003 |
| MC-067 | Débitos informados pela fonte | Valores informados registrados | Valores da fonte divergentes dos credores | `PENDENTE` | Registrar conflito | RULE-ED-003 |
| MC-068 | Responsabilidade por cada débito identificada | Responsabilidade determinada pelo edital ou pela norma | Responsabilidade indeterminável | `PENDENTE` | Impede decisão final | RULE-ED-003 |
| MC-069 | Contingência criada para valores desconhecidos | Contingência registrada com faixa | Valor desconhecido comprovadamente tratado como zero ⇒ `REPROVADO` | `PENDENTE` crítico | Violação de SAFE-005 quando zerado | RULE-ED-003 |

## A.9 Mercado e valuation (MC-070 a MC-076)

| ID | Verificação | Aprovado quando | Reprovado quando | Ausente ⇒ | Efeito | Regra |
|----|-------------|-----------------|------------------|-----------|--------|-------|
| MC-070 | Comparáveis suficientes | Quantidade ≥ `VAL-001` | Quantidade insuficiente e valuation apresentado como preciso | Valuation `INCONCLUSIVO` | Impede `BUY` | RULE-MKT-001 |
| MC-071 | Preferência por mesmo condomínio | Comparáveis do mesmo condomínio priorizados quando existem | Comparáveis do mesmo condomínio ignorados | — | Reduz confiança | RULE-MKT-001 |
| MC-072 | Preço por metro quadrado comparado | Comparação com o mesmo tipo de área | Comparação entre áreas de tipos distintos | `PENDENTE` | Reduz confiança | RULE-MKT-001 |
| MC-073 | Cenários conservador, base e otimista | Três referências emitidas com confiança | Valor pontual único apresentado | `PENDENTE` | Impede decisão | RULE-MKT-003 |
| MC-074 | Valor de venda rápida | Valor emitido com desconto `VAL-007` | Valor ausente em operação de revenda | `PENDENTE` | Impede teste de liquidez | RULE-MKT-003 |
| MC-075 | Confiança do valuation | Confiança calculada e ≥ `VAL-009` | Confiança abaixo de `VAL-009` | Confiança `inconclusiva` | Impede `BUY` | RULE-MKT-003 |
| MC-076 | Anomalias e outliers tratados | Outliers identificados, excluídos ou ajustados com registro | Outliers mantidos sem tratamento | — | Reduz confiança | RULE-MKT-004 |

## A.10 Economia da operação (MC-077 a MC-090)

| ID | Verificação | Aprovado quando | Reprovado quando | Ausente ⇒ | Efeito | Regra |
|----|-------------|-----------------|------------------|-----------|--------|-------|
| MC-077 | Preço de aquisição | Preço vigente registrado com data | Preço desatualizado usado na decisão | `PENDENTE` | Bloqueia cálculo | RULE-FIN-001 |
| MC-078 | ITBI, registro e escritura aplicáveis | Alíquotas e valores registrados | Componente omitido do TCO | Estimativa + `PENDENTE` | Entra no TCO | RULE-FIN-001 |
| MC-079 | Comissão do leiloeiro | Percentual do edital registrado | Comissão omitida do TCO | Estimativa `CUS-002` | Entra no TCO | RULE-FIN-001 |
| MC-080 | Débitos e contingências | Valores e contingências registrados | Débito relevante omitido | Contingência obrigatória | Entra no TCO | RULE-FIN-001 |
| MC-081 | Reforma | Nível 0–4 e faixa de custo registrados | Reforma comprovadamente tratada como zero sem vistoria ⇒ `REPROVADO` | `PENDENTE` alta + contingência | Entra no TCO; condição estrutural desconhecida exige pendência, não apenas contingência | RULE-FIN-006, RULE-RSK-008 |
| MC-082 | Regularização | Custo e prazo estimados | Custo omitido havendo pendência registral | Estimativa + `PENDENTE` | Entra no TCO | RULE-FIN-006 |
| MC-083 | Custo de desocupação | Faixa de custo e prazo registrados | Custo omitido em imóvel ocupado | Faixa + `PENDENTE` | Entra no TCO | RULE-FIN-006 |
| MC-084 | Carrying cost | Carrying mensal × prazo estimado registrado | Carrying omitido | Estimativa | Entra no TCO | RULE-FIN-001 |
| MC-085 | Financiamento, se houver | Juros, tarifas e prazo registrados | Custo financeiro omitido | Estimativa | Entra no TCO | RULE-FIN-001 |
| MC-086 | Custos de saída | Corretagem e tributos de saída registrados | Custos de saída omitidos na revenda | Estimativa `CUS-012`/`CUS-013` | Entra no resultado | RULE-FIN-001 |
| MC-087 | Custo econômico total | Soma completa dos componentes aplicáveis | Componente aplicável omitido | TCO incompleto | Impede preço máximo definitivo | RULE-FIN-001 |
| MC-088 | Desconto líquido | Calculado sobre o TCO e o valor de mercado | Desconto da fonte usado como decisório | Não calculável | Impede decisão econômica | RULE-FIN-002 |
| MC-089 | Margem de segurança | Calculada e testada em cenários | Margem abaixo do mínimo da estratégia | Não calculável | `DO_NOT_BUY`/`BUY_IF` | RULE-FIN-003 |
| MC-090 | Preço máximo por estratégia | Calculado por estratégia ativa | Preço de oferta acima do preço máximo | Provisório | `DO_NOT_BUY` quando excedido | RULE-FIN-004 |

## A.11 Liquidez e saída (MC-091 a MC-098)

| ID | Verificação | Aprovado quando | Reprovado quando | Ausente ⇒ | Efeito | Regra |
|----|-------------|-----------------|------------------|-----------|--------|-------|
| MC-091 | Demanda de locação | Demanda estimada com evidência | Demanda abaixo de `LIQ-006` | `indefinida` | Reduz aderência à renda | RULE-LIQ-002 |
| MC-092 | Demanda de venda | Demanda estimada com evidência | Demanda insuficiente para a estratégia | `indefinida` | Reduz score | RULE-LIQ-001 |
| MC-093 | Oferta concorrente | Quantidade e características registradas | Concorrência não avaliada | `indefinida` | Reduz confiança | RULE-LIQ-001 |
| MC-094 | Tempo estimado para alugar | Prazo em dias ≤ `REN-010` | Prazo acima do limite | `indefinida` | `BUY_IF`/`DO_NOT_BUY` | RULE-LIQ-001 |
| MC-095 | Tempo estimado para vender | Prazo em dias ≤ `LIQ-002` | Prazo acima do limite | `indefinida` | `BUY_IF`/`DO_NOT_BUY` | RULE-LIQ-001 |
| MC-096 | Preço de saída conservador | Valor registrado e coerente com comparáveis | Preço de saída otimista usado como base | `PENDENTE` | Impede robustez | RULE-LIQ-001 |
| MC-097 | Prazo máximo de carregamento | Prazo estimado ≤ `LIQ-009` | Prazo acima de `LIQ-009` | `indefinida` | `DO_NOT_BUY` para a estratégia | RULE-LIQ-003 |
| MC-098 | Risco de liquidez | Risco classificado com severidade | Liquidez abaixo do mínimo sem compensação | `UNKNOWN` | Exige margem adicional | RULE-LIQ-001 |

## A.12 Estratégia do investidor (MC-099 a MC-109)

| ID | Verificação | Aprovado quando | Reprovado quando | Ausente ⇒ | Efeito | Regra |
|----|-------------|-----------------|------------------|-----------|--------|-------|
| MC-099 | Renda | Critérios da estratégia renda avaliados | Não aderente à renda | Não avaliada | Exclui a estratégia | RULE-STR-001 |
| MC-100 | Revenda | Critérios da estratégia revenda avaliados | Não aderente à revenda | Não avaliada | Exclui a estratégia | RULE-STR-001 |
| MC-101 | Valorização | Critérios da estratégia valorização avaliados | Não aderente à valorização | Não avaliada | Exclui a estratégia | RULE-STR-001 |
| MC-102 | MCMV e baixa renda | Critérios do segmento avaliados | Não aderente ao segmento | Não avaliada | Exclui a estratégia | RULE-STR-001 |
| MC-103 | Terreno | Critérios de terreno avaliados | Não aderente | Não avaliada | Exclui a estratégia | RULE-STR-001 |
| MC-104 | Apartamento | Critérios do perfil avaliados | Não aderente ao perfil | Não avaliada | Ajusta critérios | RULE-STR-001 |
| MC-105 | Casa e sobrado | Critérios do perfil avaliados | Não aderente ao perfil | Não avaliada | Ajusta critérios | RULE-STR-001 |
| MC-106 | Um dormitório | Critérios do perfil avaliados | Não aderente ao perfil | Não avaliada | Ajusta critérios | RULE-STR-001 |
| MC-107 | Estratégia efetivamente compatível | Pelo menos uma estratégia com aderência ≥ 50 | Nenhuma estratégia compatível | Não avaliada | `DO_NOT_BUY`; regra eliminatória expressa do investidor ⇒ `BLOCK` (`D3`) | RULE-STR-001, RULE-RSK-009 |
| MC-108 | Capital disponível | Capital livre ≥ TCO e reserva preservada | TCO acima do limite por operação | `PENDENTE` | `BLOCK` operacional | RULE-STR-002 |
| MC-109 | Concentração de carteira avaliada | Concentração calculada por dimensão | Concentração acima do limite | Não avaliada | Penaliza prioridade | RULE-STR-002 |

## A.13 Score e decisão (MC-110 a MC-117)

| ID | Verificação | Aprovado quando | Reprovado quando | Ausente ⇒ | Efeito | Regra |
|----|-------------|-----------------|------------------|-----------|--------|-------|
| MC-110 | Opportunity Score calculado | Score emitido após os gates críticos | Score emitido antes dos gates | Score indefinido | Impede ranking | RULE-SCR-001 |
| MC-111 | Investor Fit calculado | Fit emitido com os sete componentes de `SCORE-006` | Fit abaixo do mínimo | Fit indefinido | Reduz prioridade | RULE-SCR-002 |
| MC-112 | Confiança calculada | Confiança consolidada emitida com nível nomeado de `CONF-010` | Confiança abaixo de `GLB-003` | Confiança `inconclusiva` | Impede `BUY`; `PENDENTE` ou `BLOCK` conforme a dimensão | RULE-SCR-002 |
| MC-113 | Ajuste por capital e carteira | Ajuste de capital e ajuste de portfólio aplicados conforme `SCORE-008` | Ajuste não aplicado havendo restrição | Não aplicado | Distorce ranking | RULE-SCR-002 |
| MC-114 | Ranking calculado | Posição e explicação emitidas | `BLOCK` presente no ranking operacional | Não calculado | Violação de SAFE-002 | RULE-DEC-001 |
| MC-115 | Explicação do score registrada | Contribuição de cada fator registrada | Score sem explicação | Não registrada | Análise incompleta | RULE-DEC-002 |
| MC-116 | Decisão emitida entre BUY, BUY IF, MONITOR, DO NOT BUY e BLOCK | Decisão em um dos cinco estados com camada determinante | Decisão fora do enum canônico | `PENDING` | Bloqueia registro | RULE-DEC-001 |
| MC-117 | Toda decisão possui evidências e justificativa | Decisão vinculada a evidências e regras versionadas | Decisão sem vínculo | Não registrada | Impede compra | RULE-DEC-002 |

## A.14 Gate final de validade jurídica (MC-118 a MC-125)

| ID | Verificação | Aprovado quando | Reprovado quando | Ausente ⇒ | Efeito | Regra |
|----|-------------|-----------------|------------------|-----------|--------|-------|
| MC-118 | Consolidação comprovada | Ato averbado e legível na matrícula atualizada | Consolidação exigida e não comprovada | `PENDENTE` | Impede `BUY` | RULE-DEC-001 |
| MC-119 | Mora e notificação comprovadas ou suficientemente evidenciadas | Cadeia documental suficiente para o caso concreto | Irregularidade material comprovada | `PENDENTE` | `BLOCK` quando irregular | RULE-DEC-001 |
| MC-120 | Intimações legalmente exigíveis verificadas | Todas as intimações aplicáveis verificadas | Ausência comprovada de intimação exigível | `PENDENTE` | `BLOCK` | RULE-DEC-001 |
| MC-121 | Edital e cronologia coerentes | Sem conflito material entre edital, matrícula e datas | Conflito material | `PENDENTE` | `BLOCK` | RULE-DEC-001 |
| MC-122 | Processos sem impacto material ou com impacto mitigado | Impacto classificado como nenhum ou mitigado com evidência | Impacto material sem mitigação | `PENDENTE` | `BLOCK` | RULE-DEC-001 |
| MC-123 | Nenhum indício material de nulidade sem tratamento | Todo indício tratado e registrado | Indício material sem tratamento | `PENDENTE` | `RISCO_JURIDICO`/`BLOCK` | RULE-DEC-001 |
| MC-124 | Ocupação e locação tratadas econômica e juridicamente | Custo, prazo e efeitos registrados | Tratamento ausente | `PENDENTE` | Impede `BUY` | RULE-DEC-001 |
| MC-125 | Item crítico inconclusivo resulta em PENDENTE ou BLOCK | Nenhum item crítico inconclusivo liberado como `BUY` | `BUY` emitido com item crítico inconclusivo | — | Invariante de SAFE-003 | RULE-DEC-001 |

## A.15 Resultado da análise (MC-126 a MC-136)

| ID | Verificação | Aprovado quando | Reprovado quando | Ausente ⇒ | Efeito | Regra |
|----|-------------|-----------------|------------------|-----------|--------|-------|
| MC-126 | Tese de investimento escrita em uma frase | Frase registrada | Tese ausente | Não registrada | Análise incompleta | RULE-DEC-002 |
| MC-127 | Principais evidências | Lista com proveniência registrada | Evidências ausentes | Não registradas | Análise incompleta | RULE-DEC-002 |
| MC-128 | Principais riscos | Lista com categoria e severidade | Riscos ausentes | Não registrados | Análise incompleta | RULE-DEC-002 |
| MC-129 | Pendências | Lista com impacto, responsável e prazo | Pendências ausentes | Não registradas | Análise incompleta | RULE-DEC-002 |
| MC-130 | Condições para compra | Condições objetivas registradas | `BUY_IF` sem condição objetiva | Não registradas | Bloqueia `BUY_IF` | RULE-DEC-002 |
| MC-131 | Preço máximo de compra | Preço máximo por estratégia registrado | Preço máximo ausente | Não registrado | Impede disciplina de lance | RULE-DEC-002 |
| MC-132 | Cenário conservador | Resultado do cenário registrado | Cenário ausente | Não registrado | Impede avaliação de robustez | RULE-DEC-002 |
| MC-133 | Cenário base | Resultado do cenário registrado | Cenário ausente | Não registrado | Impede decisão | RULE-DEC-002 |
| MC-134 | Cenário estressado | Resultado do cenário registrado | Cenário ausente | Não registrado | Impede avaliação de proteção | RULE-DEC-002 |
| MC-135 | Próxima ação definida | Ação registrada | Ação ausente | Não registrada | Análise incompleta | RULE-DEC-002 |
| MC-136 | Data da análise e versão das regras registradas | Data, versão de regras e de parâmetros registradas | Versões ausentes | Não registradas | Análise não reproduzível | RULE-DEC-002 |

---

# Anexo B — Verificações Complementares de Arrematação (normativo, 27 itens)

Origem: material de estudo de domínio. As conclusões do material **não** são tratadas
como regras jurídicas universais; cada item é ponto de investigação validado contra
legislação, jurisprudência, edital, matrícula e evidências do caso concreto.

Os identificadores `B-01` a `B-27` são os identificadores normativos deste anexo (`D17`).
A coluna **ID de origem** preserva a rastreabilidade até o material de estudo. Sem
identificador próprio, o teste de cobertura de catálogo exigido pelo projeto técnico não é
escrevível.

| ID | ID de origem | Pergunta de verificação | Aprovado quando | Reprovado quando | Ausente ⇒ | Efeito | Regra |
|----|--------------|-------------------------|-----------------|------------------|-----------|--------|-------|
| B-01 | JUR-CHK-001 | A intimação para purgar a mora foi pessoal? | Intimação pessoal comprovada | Intimação comprovadamente irregular | `PENDENTE` | P0 `PENDENTE`; `BLOCK` se irregular | RULE-JUR-004 |
| B-02 | JUR-CHK-002 | Não sendo pessoal, houve intimação por edital? | Intimação por edital comprovada | Ausência comprovada de intimação pessoal e de edital | `PENDENTE` | `BLOCK` quando comprovadamente ausente e exigível | RULE-JUR-004 |
| B-03 | JUR-CHK-003 | Houve notificação das datas dos dois leilões do art. 27 da Lei nº 9.514/97? | Notificação comprovada | Ausência comprovada de notificação exigível | `PENDENTE` | `BLOCK` quando comprovadamente ausente | RULE-JUR-005 |
| B-04 | JUR-CHK-004 | O contrato com alienação fiduciária está mais de 80% quitado? | Percentual apurado e registrado | — | `PENDENTE` | Sinal de investigação; risco `alto`; nunca `BLOCK` isolado | RULE-JUR-010 |
| B-05 | JUR-CHK-005 | O bem residencial de pessoa física foi dado em garantia de dívida de terceiro? | Situação apurada e registrada | Estrutura confirmada com risco não mitigável | `PENDENTE` | `PENDENTE` ou `BLOCK` conforme evidência | RULE-JUR-009 |
| B-06 | JUR-CHK-006 | No segundo leilão o imóvel é oferecido por menos de 50% da avaliação? | Percentual apurado e norma validada | — | `PENDENTE` | Alerta jurídico; reduz confiança; nunca `BLOCK` isolado | RULE-JUR-011 |
| B-07 | JUR-CHK-007 | Há ação questionando o leilão ou o procedimento antes do certame? | Pesquisa realizada e resultado registrado | Ação com efeito sobre o certame | `PENDENTE` | `BLOCK` quando há efeito | RULE-JUR-007 |
| B-08 | JUR-CHK-008 | Os leilões negativos do art. 27 estão averbados na matrícula? | Situação registrada entre averbado, em tratamento, não se aplica ou desconhecido | Impossibilidade material de regularização | `desconhecido` ⇒ `PENDENTE` | `em_tratamento` ⇒ pendência registral com custo e prazo no TCO | RULE-JUR-012 |
| B-09 | JUR-CHK-009 | O contrato de alienação fiduciária está registrado e a consolidação averbada em nome do credor fiduciário? | Ambos os atos localizados na matrícula | Ato exigido ausente ou inconsistente | `PENDENTE` | `PENDENTE` ou `BLOCK` conforme modalidade | RULE-JUR-013 |
| B-10 | JUR-CHK-010 | Os direitos do **devedor fiduciante** foram penhorados ou tornados indisponíveis? | Constrição verificada e classificada | Constrição impeditiva vigente | `PENDENTE` | `BLOCK` quando impeditiva | RULE-JUR-008 |
| B-11 | JUR-CHK-011 | Há terceiro ocupando? Houve compra e venda ou cessão de posição contratual do **devedor fiduciante**? | Origem da posse apurada | Posse de terceiro com risco relevante não mitigável | `PENDENTE` | Risco de posse `alto`; não presumir nulidade | RULE-OCC-002 |
| B-12 | JUR-CHK-012 | Há terceiro ocupando com locação? O contrato está registrado na matrícula? | Situação registral da locação apurada | Cláusula de vigência averbada e ignorada | `PENDENTE` | Restringe posse e prazo de saída | RULE-LOC-001 |
| B-13 | EDIT-CHK-013 | O edital foi lido integralmente? | Leitura integral registrada com versão e fingerprint | Decisão tomada sem leitura integral | `PENDENTE` | Impede `BUY` | RULE-ED-001 |
| B-14 | EDIT-CHK-014 | O vendedor se responsabiliza pela evicção de direito? | Cláusula localizada com item e página | Edital obtido e comprovadamente sem cláusula ⇒ `REPROVADO` e `BLOCK` | `PENDENTE` jurídico que impede `BUY` | Hard stop de lance nos dois casos (`D4`) | RULE-ED-002 |
| B-15 | EDIT-CHK-015 | A responsabilidade por IPTU e condomínio anteriores está clara no edital? | Responsabilidade determinada | Responsabilidade indeterminável | `PENDENTE` + contingência | Entra no TCO | RULE-ED-003 |
| B-16 | EDIT-CHK-016 | A vaga de garagem possui matrícula própria? | Situação registral da vaga apurada | Vaga autônoma não abrangida pela oferta | `PENDENTE` | `PENDENTE` ou `BLOCK` registral | RULE-ED-004 |
| B-17 | FIN-CHK-017 | O imóvel é muito ilíquido mesmo com desconto? | Liquidez estimada ≥ `liquidez_min` da estratégia | Liquidez abaixo do mínimo sem compensação | `indefinida` | Exige margem `LIQ-011` ou exceção | RULE-LIQ-001 |
| B-18 | FIN-CHK-018 | O condomínio é elevado em relação ao imóvel e ao padrão regional? | Comparação registrada e dentro do parâmetro | Condomínio elevado sem compensação de yield | `PENDENTE` | Penalidade econômica e de liquidez | RULE-FIN-005 |
| B-19 | FIN-CHK-019 | Há comparáveis suficientes de venda e aluguel? | Quantidade ≥ `VAL-011` | Quantidade < `VAL-001` | Valuation `INCONCLUSIVO` | Reduz confiança; impede `BUY` | RULE-MKT-001 |
| B-20 | FIN-CHK-020 | A região tem segurança, serviços e acesso adequados? | Dimensões avaliadas com fonte | Classe de localização `E` | `PENDENTE` | Alimenta score e liquidez | RULE-LOC-003 |
| B-21 | FIN-CHK-021 | Serão necessárias grandes obras para tornar o imóvel mais líquido? | Nível de reforma e faixa de custo registrados | Reforma nível 4 sem orçamento | `PENDENTE` alta + contingência | Entra no TCO e na liquidez | RULE-FIN-006 |
| B-22 | FIN-CHK-022 | O retorno anualizado esperado supera `GLB-011`? | `roi_anualizado` ≥ `GLB-011` | `roi_anualizado` < `GLB-011` | Não calculável | `DO_NOT_BUY` pela economia | RULE-FIN-004 |
| B-23 | FIN-CHK-023 | O prazo entre o pagamento da arrematação e o recebimento da venda é maior ou igual a 24 meses? | Prazo estimado < `LIQ-009` | Prazo ≥ `LIQ-009` | `indefinida` | `DO_NOT_BUY` para a estratégia | RULE-LIQ-003 |
| B-24 | LOG-CHK-024 | O imóvel está distante da região onde o investidor atua? | Distância dentro de `LOC-007` | Distância acima do limite sem compensação | `PENDENTE` | Penaliza `esforco_operacional` do Investor Fit | RULE-STR-002 |
| B-25 | LOG-CHK-025 | O imóvel precisa de grandes obras de manutenção ou reforma? | Nível de reforma dentro de `INV-008` | Nível acima da tolerância do investidor | `PENDENTE` | `BUY_IF` ou `DO_NOT_BUY` | RULE-FIN-006 |
| B-26 | LOG-CHK-026 | É possível vender sem corretor? Há condomínio com portaria? | Situação registrada | — | `PENDENTE` | Ajusta custo de saída e liquidez | RULE-LIQ-001 |
| B-27 | LOG-CHK-027 | O investidor se sente confortável em adquirir imóvel ocupado por família? | Conforto declarado ≥ `INV-017` | Conforto abaixo de `INV-017` | `PENDENTE` | `MONITOR` ou `DO_NOT_BUY` pelo critério pessoal | RULE-STR-001 |

---

# Anexo C — Due Diligence Individual, Hard Stops e Disciplina de Lance (normativo)

Origem: método de análise individual usado em operações reais, auditado e absorvido. As
tabelas abaixo são normativas e autocontidas: `C.1` traz os 71 critérios de due diligence,
`C.2` as 9 verificações de evicção, `C.3` os 9 hard stops, `C.4` os 12 itens pré-lance, `C.5`
os dados do certame e do leiloeiro, `C.6` a disciplina de lance e `C.7` os 12 itens da
revalidação final do dia do lance.

## C.1 Checklist de Due Diligence — 71 critérios

Cada critério recebe resultado `OK`, `ATENCAO` ou `REPROVAR`, com nota quando
aplicável, evidência, fonte, data da consulta, link ou documento e observações.

**Identificadores normativos** `[CANÔNICO]` (`D17`): os critérios deste anexo são
identificados por `C-01` a `C-71`, em que o número do identificador é o número do critério
nas tabelas abaixo com dois dígitos — o critério 1 é `C-01`, o critério 49 é `C-49` e o
critério 71 é `C-71`. Os identificadores existem para que a cobertura do catálogo seja
verificável por teste.

`REPROVAR` exige **evidência de irregularidade**; a simples falta de informação resulta em
`ATENCAO` com pendência registrada (`P-E`, `D49`).

**Bloco Registral e Jurídico (1–24)**

| # | Critério | # | Critério |
|---|----------|---|----------|
| 1 | Matrícula identificada | 13 | Ações envolvendo o imóvel |
| 2 | Matrícula atualizada | 14 | Ações contra o vendedor ou o procedimento |
| 3 | Cadeia dominial | 15 | Processos do proprietário anterior |
| 4 | Venda fiduciária | 16 | Evicção |
| 5 | Consolidação | 17 | Dependência de advogado |
| 6 | Constituição em mora | 18 | Edital completo |
| 7 | Purgação da mora | 19 | Responsabilidade por débitos |
| 8 | Intimação | 20 | Ocupação |
| 9 | Penhora | 21 | Desocupação |
| 10 | Indisponibilidade ou arresto | 22 | Financiamento anterior |
| 11 | Hipoteca e outros ônus | 23 | Percentual financiado |
| 12 | Usufruto e direitos de terceiros | 24 | Adimplemento substancial |

**Bloco Localização e Mercado (25–40)**

| # | Critério | # | Critério |
|---|----------|---|----------|
| 25 | Bairro e localização | 33 | Preço por metro quadrado |
| 26 | Segurança | 34 | Aluguel provável |
| 27 | Infraestrutura | 35 | Yield bruto |
| 28 | Liquidez regional | 36 | Tempo de venda |
| 29 | Liquidez para aluguel | 37 | Oferta e demanda |
| 30 | Valorização | 38 | Avaliação da fonte |
| 31 | Valor de mercado independente | 39 | Lance mínimo |
| 32 | Comparáveis de venda | 40 | Desconto |

**Bloco Financeiro (41–57)**

| # | Critério | # | Critério |
|---|----------|---|----------|
| 41 | Comissão do leiloeiro | 50 | Venda líquida |
| 42 | ITBI | 51 | Lucro líquido |
| 43 | Registro e documentação | 52 | ROI líquido |
| 44 | Condomínio | 53 | Margem líquida |
| 45 | IPTU e tributos | 54 | Preço máximo por ROI |
| 46 | Reforma | 55 | Cenário conservador |
| 47 | Corretagem de venda | 56 | Cenário base |
| 48 | IR sobre ganho de capital | 57 | Cenário otimista |
| 49 | Custo total da operação | | |

**Bloco Físico (58–64)**

| # | Critério | # | Critério |
|---|----------|---|----------|
| 58 | Estado do imóvel | 62 | Cozinha e banheiro |
| 59 | Instalação elétrica | 63 | Portas e janelas |
| 60 | Hidráulica | 64 | Áreas comuns |
| 61 | Pisos e pintura | | |

**Bloco Contexto Humano e Disciplina (65–71)**

| # | Critério | # | Critério |
|---|----------|---|----------|
| 65 | Contexto humano | 69 | Disciplina de lance |
| 66 | Tempo de posse e residência | 70 | Score final |
| 67 | Índice de Conforto Pessoal | 71 | Situação |
| 68 | Liquidez versus margem | | |

**Regra de agregação do bloco** `[CANÔNICO]`: o índice de segurança jurídica do
painel executivo é 0 quando existe pelo menos um critério `REPROVAR`; é 60 quando
existe pelo menos um `ATENCAO` e nenhum `REPROVAR`; e é 100 quando todos os
critérios aplicáveis são `OK`.

## C.2 Evicção de direito — hard stop (E01 a E09)

| ID | Verificação | Aprovado quando | Reprovado quando | Ausente ⇒ |
|----|-------------|-----------------|------------------|-----------|
| E01 | Existe cláusula expressa de garantia contra evicção no edital | Cláusula localizada | Edital obtido e comprovadamente sem cláusula ⇒ `REPROVAR` e `BLOCK` | `PENDENTE` (edital não obtido ou cláusula não verificada) |
| E02 | Item e página do edital que contêm a garantia | Referência exata registrada | Referência não localizável | `PENDENTE` |
| E03 | A redação cobre perda do imóvel por direito de terceiro | Cobertura confirmada na redação | Redação lida e comprovadamente não cobre a hipótese ⇒ `REPROVAR` | `PENDENTE` |
| E04 | Existem exclusões, ressalvas ou limitações relevantes | Ausência de limitação relevante, ou limitação registrada e precificada | Limitação que esvazia a garantia | `PENDENTE` |
| E05 | Existem ações reais ou reipersecutórias ou direitos de terceiros | Pesquisa realizada sem achado material | Direito de terceiro material identificado | `PENDENTE` |
| E06 | A cadeia dominial apresenta risco residual | Cadeia analisada sem risco residual material | Risco residual material | `PENDENTE` |
| E07 | A garantia é compatível com a modalidade de venda | Compatibilidade confirmada | Garantia incompatível com a modalidade | `PENDENTE` |
| E08 | Trecho do edital comprobatório registrado | Trecho transcrito com fonte e data | Trecho não registrado | `PENDENTE` |
| E09 | Conclusão de evicção | Conclusão `OK` | Conclusão `REPROVAR` | `ATENCAO` |

**Regra de hard stop** `[CANÔNICO]` (`D4`) — os dois casos são distintos e nenhum deles
libera o lance:

1. IF o edital foi obtido AND comprovadamente não contém cláusula de garantia contra
   evicção, THEN THE Gate_Juridico SHALL retornar `BLOCK`, THE Motor_de_Decisao SHALL
   emitir `BLOCK` AND THE Radar SHALL impedir a liberação de lance. Este é o caso de
   **evidência de ausência**.
2. IF o edital não foi obtido, OR a cláusula não foi verificada, THEN THE Gate_Juridico
   SHALL retornar `PENDENTE` jurídico, THE Motor_de_Decisao SHALL impedir a decisão `BUY`
   AND THE Radar SHALL impedir a liberação de lance. Este é o caso de **ausência de
   evidência**.

A formulação anterior desta spec admitia "no máximo `BUY_IF`" nos dois casos, o que
convertia a ausência comprovada de garantia em decisão condicional favorável.

## C.3 Hard stops de lance (9 condições)

| ID | Condição | Resultado |
|----|----------|-----------|
| HS-01 | Edital vigente não confirmado | `REPROVAR` |
| HS-02 | Data, hora ou plataforma divergentes sem confirmação | `REPROVAR` ou pausa até confirmação |
| HS-03 | Garantia contra evicção não atendida | `REPROVAR` |
| HS-04 | Matrícula ou situação jurídica com dúvida material | `REPROVAR` |
| HS-05 | Débitos ou ocupação sem estimativa confiável | `REPROVAR` ou pausa |
| HS-06 | Custo total acima do orçamento definido | `REPROVAR` |
| HS-07 | Lance necessário acima do lance máximo autorizado | `NAO_ENTRAR` |
| HS-08 | Condições de pagamento ou comissão não compreendidas | `NAO_ENTRAR` |
| HS-09 | A aceitação do risco depende de parecer jurídico e o parecer não está registrado como evidência | `REPROVAR` |

`HS-09` **não** é condicionado a `INV-018` (`D5`). O hard stop dispara sempre que a
aceitação do risco depender de parecer jurídico e o parecer não estiver registrado. Antes da
consolidação, bastava configurar `INV-018 = nao` para desligar a proteção.

## C.4 Checklist pré-lance — revalidação obrigatória (12 itens)

| # | Item | Condição de liberação |
|---|------|-----------------------|
| PL-01 | Edital vigente conferido | `SIM` |
| PL-02 | Matrícula e documentação rechecadas | `SIM` |
| PL-03 | Valor mínimo atualizado | `SIM` |
| PL-04 | Comissão confirmada | `SIM` |
| PL-05 | Regra de condomínio e IPTU confirmada | `SIM` |
| PL-06 | Ocupação reavaliada | `SIM` |
| PL-07 | Mercado e comparáveis ainda válidos | `SIM` |
| PL-08 | Custo total recalculado | `SIM` |
| PL-09 | Lance máximo definido | `SIM` |
| PL-10 | Recursos disponíveis para lance mais custos | `SIM` |
| PL-11 | Leiloeiro e plataforma conferidos | `SIM` |
| PL-12 | Sem alteração material desde a análise | `SIM` |

**Regra de liberação** `[CANÔNICO]`: THE Radar SHALL emitir `PODE_DAR_LANCE` apenas
quando os 12 itens `PL-01` a `PL-12` estiverem `SIM`, nenhum hard stop `HS-01` a
`HS-09` estiver acionado, o lance máximo autorizado e o lance máximo absoluto
estiverem definidos, e o lance atual for menor ou igual ao lance máximo absoluto. Em
qualquer outra combinação, THE Radar SHALL emitir `NAO_DAR_LANCE`.

## C.5 Dados do certame e do leiloeiro

| Campo | Obrigatoriedade | Observação |
|-------|-----------------|------------|
| Nome do leiloeiro | Obrigatório | Conferir no edital vigente |
| Registro ou matrícula na Junta Comercial | Obrigatório | Conferir em fonte oficial |
| CPF ou CNPJ | Quando disponível | Conferir em fonte oficial |
| Empresa ou marca | Obrigatório | Conferir no edital |
| Site ou plataforma | Obrigatório | Conferir domínio oficial |
| E-mail oficial | Obrigatório | Abster-se de usar contato não confirmado |
| Telefone oficial | Obrigatório | Abster-se de usar contato não confirmado |
| Comissão e forma de pagamento | Obrigatório | Conferir no edital vigente |
| Comissão fora do lance | Obrigatório | Percentual confirmado no edital; **somar no custo total de aquisição**, nunca embutir no lance |
| Dados bancários para pagamento | Somente após orientação oficial | Abster-se de confiar em mensagem isolada |
| Número do edital | Obrigatório | Conferir versão vigente |
| Item do imóvel | Obrigatório | Deve coincidir com o imóvel analisado |
| Data e hora da sessão | Obrigatório | Confrontar portal e edital |
| Plataforma da sessão | Obrigatório | Conferir acesso no dia |
| Valor mínimo | Obrigatório | Atualizar a cada nova publicação |
| Forma de pagamento admitida | Obrigatório | Conferir regra vigente |

**Histórico do leiloeiro — seis verificações** `[CANÔNICO]` (`D50`). Antes da consolidação
este item era uma única linha "recomendado", o que o tornava inverificável.

| ID | Verificação | Aprovado quando |
|----|-------------|-----------------|
| HL-01 | Registro oficial na Junta Comercial | Registro localizado em fonte oficial e vigente |
| HL-02 | Site oficial | Domínio confirmado no edital ou em fonte oficial |
| HL-03 | Experiência com a instituição vendedora | Certames anteriores identificados |
| HL-04 | Reclamações relevantes | Pesquisa realizada com resultado registrado |
| HL-05 | Histórico de divergências | Pesquisa realizada com resultado registrado |
| HL-06 | Plataforma utilizada | Plataforma do edital igual à do portal e acessível |

**Requisito derivado:** THE Radar SHALL registrar cada divergência documental em um
registro com data, fonte A, informação A, fonte B, informação B e impacto na decisão,
conforme a entidade Divergência de `R74.6`.

## C.7 Revalidação final do dia do lance (12 itens)

Esta verificação é **distinta** do checklist pré-lance `C.4`: ela ocorre no dia do certame e
inclui quatro itens que não têm equivalente em `C.4` (`D50`).

| ID | Item | Condição de liberação | Equivalente em C.4 |
|----|------|-----------------------|--------------------|
| RL-01 | Edital vigente conferido | `SIM` | `PL-01` |
| RL-02 | Data e horário confirmados no portal oficial e junto ao leiloeiro | `SIM` | — (amplia `PL-11`) |
| RL-03 | Leiloeiro do portal igual ao leiloeiro do edital e à plataforma | `SIM` | `PL-11` |
| RL-04 | Valor mínimo atualizado | `SIM` | `PL-03` |
| RL-05 | Matrícula e documentação rechecadas | `SIM` | `PL-02` |
| RL-06 | Débitos, condomínio e IPTU rechecados | `SIM` | `PL-05` |
| RL-07 | Ocupação rechecada | `SIM` | `PL-06` |
| RL-08 | **Condições de pagamento confirmadas** | `SIM` | — sem equivalente |
| RL-09 | **Evicção documentalmente confirmada** | `SIM` | — sem equivalente |
| RL-10 | **Nenhuma divergência pendente** | `SIM` | — sem equivalente |
| RL-11 | Lance máximo definido e respeitado | `SIM` | `PL-09` |
| RL-12 | **Reserva de contingência disponível** | `SIM` | — sem equivalente |

**Regra de liberação final** `[CANÔNICO]`: THE Radar SHALL emitir `LIBERADO_PARA_LANCE`
somente quando os doze itens `RL-01` a `RL-12` estiverem `SIM`, os doze itens `PL-01` a
`PL-12` estiverem `SIM`, nenhum hard stop `HS-01` a `HS-09` estiver acionado, e o lance
atual for menor ou igual ao lance máximo absoluto.

## C.6 Disciplina de lance

| Campo | Regra |
|-------|-------|
| Lance máximo autorizado | Nunca ultrapassar |
| Lance máximo absoluto | Teto final, mesmo sob disputa; definido antes da sessão |
| Lance atual | Atualizado durante a disputa |
| Situação | `LIBERADO` somente após o checklist pré-lance |
| Motivo para sair da disputa | Preço acima do teto ou qualquer hard stop; sair sem exceção |

---

# Anexo D — Matriz Canônica de Regras (55 regras, normativo)

As 45 primeiras regras são o catálogo canônico consolidado. As dez últimas,
`RULE-RSK-001` a `RULE-RSK-010`, incorporam as regras de bloqueio de risco que existiam na
documentação de origem e não estavam representadas aqui (`D19`). Total: **55 regras**.

| ID | Regra | Domínio | Condição ou gatilho | Evidência mínima | Resultado | Prioridade | Afeta score |
|----|-------|---------|---------------------|------------------|-----------|------------|-------------|
| RULE-ID-001 | Identidade e captura | Identidade | A oferta precisa ser identificável e rastreável antes de qualquer análise | Fonte, instituição ou leiloeiro, identificador, matrícula, comarca, endereço, área e captura original | Sem identidade confiável ⇒ `PENDENTE`; conflito material ⇒ `BLOCK` | GATE | Não |
| RULE-ID-002 | Matrícula atualizada e titularidade | Registral | A matrícula atual deve permitir confirmar titularidade e atos relevantes | Certidão atualizada, proprietário, atos e averbações relevantes | Ausente ou desatualizada ⇒ `PENDENTE`; conflito material ⇒ `BLOCK` | GATE | Não |
| RULE-JUR-001 | Alienação fiduciária e credor | Jurídico | Identificar contrato e credor fiduciário e a relação com a propriedade | Matrícula, contrato, documentos do credor | Inconsistência ⇒ risco jurídico e `PENDENTE` | GATE | Não |
| RULE-JUR-002 | Consolidação da propriedade | Jurídico | Confirmar a consolidação quando exigida para o procedimento | Matrícula atual, ato ou averbação e texto do ato | Não comprovada ⇒ `BLOCK` ou `PENDENTE` conforme modalidade e fase | BLOCK | Não |
| RULE-JUR-003 | Constituição em mora | Jurídico | Confirmar a constituição em mora e a cadeia documental | Documento de constituição, certidão, notificações | Ausência ou irregularidade material ⇒ risco jurídico crítico | BLOCK | Não |
| RULE-JUR-004 | Intimação para purgação da mora | Jurídico | Verificar modalidade, destinatário, endereço, data, recebimento ou recusa e eventual edital subsidiário | Prova de intimação, aviso de recebimento ou certidão, edital | Inconclusivo ⇒ `PENDENTE`; irregularidade material ⇒ `BLOCK` | BLOCK | Não |
| RULE-JUR-005 | Intimações relativas aos leilões | Jurídico | Verificar comunicações legalmente exigíveis sobre as datas dos leilões | Comprovantes, certidões, documentos do procedimento | Ausência de evidência ⇒ `PENDENTE`; irregularidade material ⇒ `BLOCK` | BLOCK | Não |
| RULE-JUR-006 | Cronologia jurídica do procedimento | Jurídico | A sequência mora, consolidação e leilão deve ser coerente | Matrícula, edital, notificações, datas | Conflito material ⇒ `BLOCK` ou `PENDENTE` | BLOCK | Não |
| RULE-JUR-007 | Processos judiciais e liminares | Jurídico | Avaliar objeto, fase, decisões e impacto; a existência isolada não bloqueia | Tribunais, processos, decisões, tutelas | Impacto material sem mitigação ⇒ `BLOCK`; demais ⇒ risco ou `PENDENTE` | BLOCK | Não |
| RULE-JUR-008 | Penhora e indisponibilidade de direitos | Jurídico | Identificar constrições atuais e verificar se impedem a transferência | Matrícula, ordens de indisponibilidade, processos | Constrição impeditiva ⇒ `BLOCK`; baixa comprovada ⇒ normal | BLOCK | Não |
| RULE-JUR-009 | Garantia de dívida de terceiro | Jurídico | Detectar imóvel residencial em garantia de dívida de terceiro | Contrato, matrícula, partes, jurisprudência vigente | Risco contextual ⇒ `PENDENTE` ou `BLOCK` conforme evidência | BLOCK | Não |
| RULE-JUR-010 | Percentual de quitação do financiamento | Jurídico | Registrar percentual quitado como sinal de investigação | Contrato, saldo, documentos | Acima de 0,80 ⇒ revisão jurídica; resultado depende do caso | RISK | Não |
| RULE-JUR-011 | Preço do segundo leilão abaixo de 50% da avaliação | Jurídico e Econômico | Detectar preço inferior ao parâmetro e exigir validação da modalidade e da norma | Edital, avaliação, preço do segundo leilão, legislação | Alerta jurídico; nunca bloqueio isolado pelo percentual | ALERT | Afeta confiança |
| RULE-JUR-012 | Averbação de leilões negativos | Registral | Tratar situação `em tratamento` como pendência registral | Matrícula atual, exigências cartorárias, edital | `em_tratamento` ⇒ `PENDENTE`; impossibilidade material ⇒ `BLOCK` potencial | GATE | Reduz confiança; custo no TCO |
| RULE-JUR-013 | Contrato de alienação fiduciária registrado e consolidação averbada | Registral | Confirmar atos registrais necessários e sua coerência com o leilão | Matrícula atual | Ausente ou inconsistente ⇒ `PENDENTE` ou `BLOCK` conforme modalidade | BLOCK | Não |
| RULE-OCC-001 | Situação de ocupação | Ocupação | Determinar desocupado, ocupado pelo devedor, ocupado por terceiro, ocupado por inquilino ou desconhecido | Vistoria, anúncio, informações da instituição, condomínio | Desconhecido ⇒ `PENDENTE`; ocupado ⇒ risco de posse e custo | RISK | Afeta TCO, prazo e liquidez |
| RULE-OCC-002 | Terceiro e cessão de posição contratual | Ocupação | Investigar contrato, origem da posse e efeitos perante o adquirente | Contrato, matrícula, evidências de posse | Risco relevante ⇒ `PENDENTE` ou risco; nunca presumir nulidade | RISK | Sim |
| RULE-LOC-001 | Locação e registro | Locação | Verificar contrato, prazo, valor, garantia, cláusula de vigência e registro | Contrato, matrícula, documentos | Efeito relevante ⇒ `PENDENTE` ou risco | RISK | Sim |
| RULE-LOC-002 | Locação versus garantia fiduciária | Locação | Comparar data e condições da locação com a garantia | Contrato de garantia, contrato de locação, matrícula | Conflito ⇒ análise jurídica específica | RISK | Sim |
| RULE-LOC-003 | Qualidade da localização | Localização | Avaliar segurança, serviços, comércio, transporte, acesso e atratividade da microárea | Dados geográficos, mercado, fontes locais | Alimenta score e liquidez; nunca bloqueio por indicador isolado | SCORE | Sim |
| RULE-ED-001 | Leitura integral do edital | Edital | O edital é fonte primária das condições da operação | Documento oficial, versão, fingerprint | Sem edital ⇒ `PENDENTE`; conflito crítico ⇒ `BLOCK` | GATE | Não |
| RULE-ED-002 | Responsabilidade por evicção | Edital e Jurídico | Extrair a cláusula de evicção e registrar a responsabilidade assumida | Edital e cláusula, com item e página | Cláusula desfavorável ⇒ elevar risco e contingência; nunca inferir proteção | RISK | Sim |
| RULE-ED-003 | IPTU, condomínio e demais débitos | Custos | Identificar o responsável por cada encargo e criar contingência para desconhecidos | Edital, prefeitura, condomínio, concessionárias | Responsabilidade desconhecida ⇒ contingência e `PENDENTE` | COST | Sim |
| RULE-ED-004 | Vaga de garagem e matrícula | Registral | Confirmar se a vaga integra a unidade ou possui matrícula autônoma | Matrículas, edital, convenção | Inconsistência ⇒ `PENDENTE` ou `BLOCK` registral | GATE | Não |
| RULE-MKT-001 | Comparáveis de venda | Mercado | Construir amostra relevante priorizando mesmo condomínio e microárea | Anúncios, transações, endereço, área, padrão, data | Poucos comparáveis ⇒ confiança menor; nunca inventar valor | DATA | Sim |
| RULE-MKT-002 | Comparáveis de aluguel | Mercado | Usar aluguéis comparáveis para validar renda e demanda | Anúncios, contratos, condomínio, tipologia | Amostra pequena ⇒ confiança menor | DATA | Sim |
| RULE-MKT-003 | Valuation em faixa | Valuation | Produzir conservador, base, otimista e venda rápida; separar avaliação da fonte do valor de mercado | Comparáveis, metodologia, outliers | Sem robustez ⇒ valuation inconclusivo ou `PENDENTE` | DATA | Sim |
| RULE-MKT-004 | Outliers e qualidade dos comparáveis | Valuation | Excluir ou ajustar outliers e registrar a metodologia | Base de comparáveis | Amostra inconsistente ⇒ reduzir confiança | DATA | Sim |
| RULE-FIN-001 | Custo econômico total | Economia | Somar aquisição, comissão, tributos, registro, débitos, reforma, regularização, desocupação, carrying, financiamento, saída e contingência | Edital, certidões, estimativas, orçamentos, parâmetros | TCO incompleto ⇒ não fechar preço máximo definitivo | GATE | Não |
| RULE-FIN-002 | Desconto líquido | Economia | Calcular `1 − TCO ÷ valor de mercado` | TCO e valuation | Valuation pouco confiável ⇒ desconto com confiança menor | SCORE | Sim |
| RULE-FIN-003 | Margem de segurança | Economia | Calcular a margem entre valor de mercado e TCO e testar cenários | Valuation, TCO, cenários | Margem insuficiente ⇒ não atende à estratégia | SCORE | Sim |
| RULE-FIN-004 | Preço máximo por estratégia | Economia | Derivar preço máximo respeitando custos, retorno mínimo, risco e estratégia | Parâmetros da estratégia, TCO, valuation | Preço ofertado acima do máximo ⇒ `DO_NOT_BUY` econômico | GATE | Não |
| RULE-FIN-005 | Condomínio elevado | Economia e Liquidez | Comparar o condomínio com o valor do imóvel e com similares e incorporar carrying | Boleto ou declaração, comparáveis | Elevado ⇒ penalidade econômica e de liquidez | SCORE | Sim |
| RULE-FIN-006 | Reforma e regularização | Economia | Estimar custo, prazo, contingência e efeito sobre liquidez e valor | Vistoria, orçamentos, tipologia | Incerteza ⇒ contingência e confiança menor | COST | Sim |
| RULE-LIQ-001 | Liquidez de venda | Liquidez | Estimar demanda, concorrência, preço e prazo de venda | Comparáveis, oferta, histórico | Baixa liquidez exige margem maior e pode reprovar a estratégia | SCORE | Sim |
| RULE-LIQ-002 | Liquidez de aluguel | Liquidez | Estimar demanda, aluguel, vacância e tempo para locar | Comparáveis, anúncios, mercado local | Baixa demanda reduz aderência à renda | SCORE | Sim |
| RULE-LIQ-003 | Prazo de carregamento | Liquidez | Modelar tempo até venda ou locação e o impacto financeiro | Cenários, carrying, estratégia | Prazo acima do máximo ⇒ `DO_NOT_BUY` para a estratégia | GATE | Não |
| RULE-STR-001 | Aderência à estratégia | Estratégia | Comparar imóvel e tese com a estratégia ativa | Perfil, estratégia, parâmetros | Incompatível ⇒ `DO_NOT_BUY` ou monitorar conforme configuração | GATE | Não |
| RULE-STR-002 | Capital e concentração | Carteira | Verificar ticket, capital disponível e concentração por região e tipo | Carteira, caixa, parâmetros | Excesso de concentração ⇒ penalidade ou bloqueio configurado | SCORE | Sim |
| RULE-SCR-001 | Opportunity Score | Score | Calcular somente após os gates críticos, com componentes versionados | Desconto líquido, margem, liquidez, localização, risco, renda, valorização, qualidade | Score baixo ⇒ menor prioridade; score alto nunca supera `BLOCK` | SCORE | Não |
| RULE-SCR-002 | Investor Fit e confiança | Score e Confiança | Ajustar a oportunidade pela aderência ao investidor e pela confiança dos dados | Estratégia, carteira, qualidade, evidências | Confiança baixa limita a decisão e pode gerar `PENDENTE` | GATE | Sim |
| RULE-DEC-001 | Precedência de decisão | Governança e Decisão | Aplicar a precedência canônica de camadas | Todos os resultados anteriores | `BLOCK` sempre prevalece; desconhecido crítico impede `BUY` | DECISION | Não |
| RULE-DEC-002 | Explicabilidade | Decisão | Toda decisão deve apontar tese, evidências, riscos, pendências, condições e próxima ação | Resultado das regras e evidências | Sem justificativa rastreável ⇒ análise incompleta | GOV | Não |
| RULE-GOV-001 | Versionamento e reprodutibilidade | Governança | Registrar versão de regras, parâmetros, fontes, data e evidências usadas | Metadados da análise | Sem versão ⇒ análise não reproduzível | GOV | Não |
| RULE-MON-001 | Monitoramento e reavaliação | Monitoramento | Recalcular quando preço, status, valuation, risco, evidência, regra ou estratégia mudar | Eventos e histórico | Mudança material ⇒ reanálise | MONITOR | Não |
| RULE-RSK-001 | Impedimento jurídico crítico confirmado | Risco | Impedimento jurídico com impacto crítico comprovado | Documento registral, decisão judicial, edital | `BLOCK` | BLOCK | Não |
| RULE-RSK-002 | Titularidade incompatível sem solução | Risco | Titularidade da matrícula incompatível com a oferta e sem caminho de saneamento | Matrícula, edital, documentos do credor | `BLOCK` | BLOCK | Não |
| RULE-RSK-003 | Restrição de aquisição incompatível | Risco | Restrição legal, contratual ou editalícia que impeça o investidor de adquirir | Edital, norma aplicável, perfil do investidor | `BLOCK` | BLOCK | Não |
| RULE-RSK-004 | Passivo crítico sem limite conhecido | Risco | Passivo de impacto crítico cuja magnitude não é determinável | Certidões, boletos, declarações de credores | Sem limite conhecido ⇒ `PENDENTE` crítico; impossibilidade material de limitar ⇒ `BLOCK` | BLOCK | Não |
| RULE-RSK-005 | Ocupação com impacto crítico sem estratégia de desocupação | Risco | Ocupação de impacto crítico sem estratégia registrada, ou posse litigiosa com evidência de litígio | Vistoria, contrato, processos, evidências de posse | `BLOCK` na camada 0 (`D2`) | BLOCK | Não |
| RULE-RSK-006 | Identidade documental conflitante | Risco | Identificadores documentais em conflito material | Matrícula, edital, cadastro da fonte | `PENDENTE` até a resolução | GATE | Não |
| RULE-RSK-007 | Valuation inconclusivo para decisão de alto risco | Risco | Valuation `INCONCLUSIVO` combinado com risco `alto` | Amostra de comparáveis, confiança do valuation | `PENDENTE` | GATE | Sim |
| RULE-RSK-008 | Reforma estrutural desconhecida | Risco | Condição estrutural do imóvel desconhecida | Vistoria, laudo, orçamento | `PENDENTE` de prioridade `alta` mais contingência (`D6`) | RISK | Sim |
| RULE-RSK-009 | Regra eliminatória do investidor | Risco | Regra eliminatória expressa do investidor acionada | Perfil do investidor, parâmetros vigentes | `BLOCK` (`D3`) | BLOCK | Não |
| RULE-RSK-010 | Risco aceito por exceção formal | Risco | Risco não crítico aceito por exceção autorizada dentro de alçada e prazo | Registro de exceção com justificativa, evidência, limite e prazo | Prossegue condicionado | GOV | Sim |

`RULE-RSK-005` e `RULE-RSK-009` produzem `BLOCK`, não `DO_NOT_BUY`. O motivo é operacional:
`BLOCK` sai do ranking e `DO_NOT_BUY` permanece nele, e uma regra eliminatória do investidor
não deve continuar competindo pelo capital e pela atenção (`D3`).

---

# Anexo E — Testes de Regressão Obrigatórios

| ID | Cenário | Resultado esperado |
|----|---------|--------------------|
| REG-001 | Consolidação não comprovada | Não permitir `BUY`; `PENDENTE` ou `BLOCK` conforme modalidade |
| REG-002 | Consolidação comprovada com texto do ato mencionando intimação regular | Reconhecer evidência positiva sem declarar risco zero |
| REG-003 | Averbação de leilões negativos `em tratamento` | Pendência registral com custo e prazo no TCO; sem `BLOCK` automático |
| REG-004 | Processo judicial sem impacto material | Não bloquear apenas pela existência |
| REG-005 | Processo com liminar que atinge o leilão | `BLOCK` até resolução ou mitigação |
| REG-006 | Imóvel ocupado | Separar posse de validade jurídica; modelar custo e prazo |
| REG-007 | Poucos comparáveis | Reduzir confiança; não emitir valuation preciso |
| REG-008 | Opportunity Score 92 com `BLOCK` jurídico | Resultado final `BLOCK` |
| REG-009 | Avaliação da fonte acima dos comparáveis | Recalcular valuation de forma independente |
| REG-010 | TCO com componente crítico desconhecido | Não fechar preço máximo definitivo |
| REG-011 | Preço do segundo leilão abaixo de 50% da avaliação | Emitir alerta e validar norma; sem `BLOCK` automático |
| REG-012 | Investidor não aceita imóvel ocupado | Estratégia incompatível ⇒ `DO_NOT_BUY` ou `MONITOR` conforme configuração |
| REG-013 | Garantia contra evicção não confirmada no edital | Impedir liberação de lance |
| REG-014 | Divergência entre data do portal e data do edital | `PENDENTE` e hard stop de lance até confirmação |
| REG-015 | Custo econômico total acima do limite por operação do investidor | `BLOCK` operacional por capital |
| REG-016 | Capital livre após a operação abaixo da reserva mínima | `BLOCK` operacional por reserva |
| REG-017 | Opportunity Score alto com Investor Fit abaixo do mínimo | Não priorizar; `DO_NOT_BUY` ou prioridade reduzida |
| REG-018 | Backtest recebendo dado posterior à data da decisão | Rejeitar o dado e registrar a rejeição |
| REG-019 | Valor monetário ou área com ponto como separador decimal, por exemplo `"47.76"` e `"191651.31"` | Interpretar como 47,76 e 191.651,31; nunca multiplicar por 100 (ver `D.1.3`) |
| REG-020 | Percentual fracionário `"2.5%"` e percentual inteiro `1` significando um por cento | Retornar 0,025 e 0,01; a unidade deve vir declarada na entrada (ver `D.1.4`) |
| REG-021 | Score 89,5 e confiança 89,5 | Classificar como `Excelente` e aplicar fator 0,95; nenhuma lacuna entre faixas em todo o domínio `[0, 100]` (ver `D.1.5`) |
| REG-022 | `legal_status` recebido com valor fora do enum, incluindo `"ok"` minúsculo e string vazia | Falhar explicitamente; nunca tratar como liberado (ver `D.2.7`) |
| REG-023 | Chamada de análise sem informar o resultado do gate jurídico | Assumir `PENDENTE` e elegibilidade falsa; nunca `OK` (ver `D.2.5`) |
| REG-024 | Verificação jurídica com resultado `IRREGULAR` | Evidência registrada com estado e confiança compatíveis com prova de irregularidade, não com confiança zero (ver `D.2.8`) |
| REG-025 | Verificação jurídica `NOT_APPLICABLE` | Estado distinto de `UNKNOWN`; não contar como lacuna de cobertura |
| REG-026 | Mesma matrícula apresentada em dois imóveis distintos | Rejeitar no nível de integridade de dados (ver `D.9.1`) |
| REG-027 | Mesmo payload de captura reprocessado duas vezes | Uma única captura registrada; nenhuma análise duplicada (ver `D.9.2`) |
| REG-028 | Aplicação do schema e do seed duas vezes seguidas | Execução idempotente, sem erro e sem duplicar linhas (ver `D.9.11`) |
| REG-029 | `market_value` igual a zero ou negativo na API | Resposta 422 com a causa; nunca 500 (ver `D.10.7`) |
| REG-030 | Captura de fonte diferente de CAIXA | Normalizador correspondente à fonte; falhar se não houver (ver `D.6.11`) |
| REG-031 | Ocupação com impacto crítico e sem estratégia de desocupação; e posse litigiosa com evidência de litígio | `BLOCK` pela camada 0 nos dois casos (`D2`) |
| REG-032 | Edital obtido e comprovadamente sem cláusula de evicção; e edital não obtido | `BLOCK` no primeiro caso e `PENDENTE` no segundo; lance não liberado em nenhum dos dois (`D4`) |
| REG-033 | Teto conservador do método com IR igual a zero — entrada completa e obrigatória para reprodução: `V = 300.000`, `c_v = 0,06`, `F = 23.000`, `c_c = 0,05`, `r = 0,25`, `t = 0` e `c_itbi = 0` | Teto conservador `259.000 ÷ 1,30 =` R$ 199.230,77 **excede** o preço máximo exato `253.250 ÷ 1,3125 =` R$ 192.952,38, diferença de R$ 6.278,39. Com `c_itbi = 0,02` o preço máximo exato cai para `253.250 ÷ (1,07 × 1,25) = 253.250 ÷ 1,3375 =` R$ 189.345,79 e a diferença sobe para R$ 9.884,98: o ITBI **agrava** a falsidade da propriedade removida. O teto conservador é informativo e o teto decisório é `mínimo(exato; ajustado ao risco)` (`D28`) |
| REG-034 | Pendência resolvida | Confiança, Opportunity Score, Investor Fit e ranking recalculados (`MON-011`, `D39`) |
| REG-035 | Risco de severidade `critico` com evidência `ESTIMATED` | `BLOCK` registrado como bloqueio por risco crítico presumido, com condição objetiva de desbloqueio (`D20`) |

---

# Anexo F — Golden Cases (casos de prova)

## F.1 Item 227 — Apartamento, caso de prova econômico

**Procedência dos dados.** As entradas de `F.1` vêm de uma planilha de análise individual
real, e **não** da documentação de negócio. A documentação apresenta exemplos com outro
conjunto de números; os dois não se reconciliam e não devem ser misturados. Este Golden Case
é oráculo **desta spec**: onde a planilha divergir das regras aqui escritas, prevalecem as
regras, e a planilha permanece registrada como valor de origem.

### F.1.1 Entradas

| Campo | Valor | Origem |
|-------|-------|--------|
| Edital e item | Edital `0031/0326-CPVE/RE`, item `227` | planilha |
| Lance mínimo (preço) | R$ 191.651,31 | planilha |
| Comissão do leiloeiro (`CUS-002`) | 5% | planilha |
| ITBI (`CUS-003`) | 2% | planilha |
| Registro e documentação (`CUS-004`) | R$ 3.000,00 | planilha |
| Condomínio e débitos (`CUS-005`) | R$ 5.000,00 | planilha |
| Tributos e débitos (`CUS-006`) | R$ 0,00 | planilha |
| Reforma (`CUS-007`) | R$ 10.000,00 | planilha |
| Custo jurídico potencial (`CUS-014`) | R$ 0,00 **declarado** pelo analista | planilha |
| Probabilidade jurídica (`CUS-015`) | 0,00 **declarada** pelo analista | planilha |
| Corretagem de venda (`CUS-012`) | 6% | planilha |
| IR sobre ganho de capital (`CUS-013`) | 15% | planilha |
| Preço de venda de referência | R$ 300.000,00 | planilha |
| Valor de mercado conservador | R$ 270.000,00 | planilha |
| **Valor de mercado provável** | **R$ 290.000,00** | planilha |
| Aluguel mensal bruto | R$ 1.900,00 | planilha |
| Condomínio mensal | R$ 510,00 | planilha |
| IPTU mensal | R$ 25,00 | planilha |
| Seguro e taxas mensais | R$ 0,00 | planilha |
| Manutenção mensal | R$ 100,00 | planilha |
| Vacância (`REN-004`) | 5% ⇒ R$ 95,00 | planilha |
| Prazo base até a saída | **90 dias (3 meses)** | declarado por esta spec |
| Carrying mensal (`CUS-016`) | **R$ 635,00** = 510 + 25 + 0 + 100 | derivado das entradas |
| ROI alvo da estratégia revenda | 25% | planilha |
| Custos fixos `F` para preço máximo | R$ 23.000,00 | planilha |
| Score de localização | 85 | planilha |
| Score de liquidez | 80 | planilha |
| Tempo provável de venda | 60 a 90 dias | planilha |
| Índice de Conforto Pessoal | 85 | planilha |
| Data e hora da sessão | 15/09/2026 10:00 no edital; 29/09/2026 10:00 no portal — **divergência registrada** | planilha |

`CUS-014` e `CUS-015` são zero por **declaração explícita do analista**, o que `R26.10`
admite como evidência de que o componente é efetivamente nulo. Não é ausência de informação.
Caso não fossem declarados, o estado seria `UNKNOWN` com contingência e pendência (`D13`).

A inadimplência (`REN-005`) **não** foi declarada. Ela é, portanto, `UNKNOWN`: gera
contingência e pendência, e o aluguel líquido publicado abaixo é provisório **por cima**.
`REN-012` está `[PENDENTE-DECISÃO]`, logo o imposto sobre aluguel não é aplicado e o yield
líquido também é provisório por cima. As duas pendências só pioram o resultado.

### F.1.2 Custo econômico total — planilha e spec

O custo total de aquisição da planilha permanece registrado como valor de origem:

```
223.066,9017  = 191.651,31 + 9.582,5655 + 3.833,0262 + 3.000 + 5.000 + 0 + 10.000
228.066,9017  = 223.066,9017 + 5.000,00   (reserva fixa usada pela planilha)
```

A reserva de R$ 5.000,00 corresponde a `5.000 ÷ 223.066,9017 = 2,2415%` da base, e não aos
5% que `CUS-011` exige. Aplicando a spec:

```
reserva conforme CUS-011 = 223.066,9017 × 0,05 = 11.153,345085
subtotal de aquisição     = 223.066,9017 + 11.153,345085 = 234.220,246785
carrying (CUS-016 × prazo) = 635,00 × 3 = 1.905,00
TCO econômico (R26.1)      = 234.220,246785 + 1.905,00 = 236.125,246785
```

| Métrica | Valor |
|---------|-------|
| Custo total de aquisição da planilha | R$ 228.066,9017 |
| Reserva conforme `CUS-011` | R$ 11.153,345085 |
| Carrying de 3 meses a R$ 635,00 | R$ 1.905,00 |
| **TCO econômico conforme `R26.1`** | **R$ 236.125,246785** |

O TCO **não** inclui corretagem de venda nem IR sobre ganho de capital: pela `R26.1.1` eles
pertencem exclusivamente à perna de venda. Também não inclui o custo de oportunidade do
capital, pela `R26.1.2`.

### F.1.3 Desconto líquido — base correta

`R27.3` calcula o desconto líquido sobre o **valor de mercado provável**, R$ 290.000,00:

```
desconto_liquido (TCO da spec)     = 1 − 236.125,246785 ÷ 290.000 = 0,1857750 → 18,5775%
desconto_liquido (TCO da planilha) = 1 − 228.066,9017   ÷ 290.000 = 0,2135624 → 21,3562%
```

Os 23,98% publicados na versão anterior desta spec estavam **errados**: foram calculados
sobre R$ 300.000,00, que é o preço de venda de referência, não o valor de mercado provável
(`1 − 228.066,9017 ÷ 300.000 = 0,2397770`). O erro inflava o desconto em 2,62 pontos
percentuais.

### F.1.4 Resultado econômico recalculado

Todas as linhas usam o TCO da spec, R$ 236.125,246785.

| Métrica | Fórmula | Valor |
|---------|---------|-------|
| Margem absoluta (`R27.4`) | `290.000 − 236.125,246785` | R$ 53.874,753215 |
| Margem percentual (`R27.5`) | `53.874,753215 ÷ 290.000` | 0,1857750 → 18,5775% |
| Corretagem de venda | `300.000 × 0,06` | R$ 18.000,00 |
| Base de IR (`R27.10`) | `máx(0; 300.000 − 18.000 − 0 − 236.125,246785)` | R$ 45.874,753215 |
| IR sobre ganho (`CUS-013`) | `45.874,753215 × 0,15` | R$ 6.881,21298225 |
| Venda líquida (`R27.9`) | `300.000 − 18.000 − 0 − 6.881,21298225` | R$ 275.118,78701775 |
| Lucro líquido (`R27.11`) | `275.118,78701775 − 236.125,246785` | R$ 38.993,54023275 |
| ROI líquido (`R27.12`) | `38.993,54023275 ÷ 236.125,246785` | 0,1651392 → 16,5139% |
| Margem líquida (`R27.13`) | `38.993,54023275 ÷ 300.000` | 0,1299785 → 12,9978% |
| ROI anualizado (`R30.3.1`) | `(1 + 0,1651392)^(12 ÷ 3) − 1` | 0,8429404 → 84,2940% |
| Break-even de saída (`R27.14`) | `236.125,246785 ÷ (1 − 0,06)` | R$ 251.197,07105 |
| Distância do break-even ao preço atual (`R33.7`) | `(251.197,07105 − 191.651,31) ÷ 191.651,31` | 0,3107 → 31,07%; acima de 0,05, não aciona `MONITOR` |

Renda:

| Métrica | Fórmula | Valor |
|---------|---------|-------|
| Aluguel líquido (`R27.7`) | `máx(0; 1.900 − 510 − 25 − 100 − 0 − 95 − 0 − 0)` | R$ 1.170,00 |
| Base de IR sobre aluguel (`R27.7.1`) | `máx(0; 1.900 − 510 − 25 − 100 − 0)` | R$ 1.265,00 |
| Imposto sobre aluguel | `1.265,00 × REN-012` | não aplicado — `REN-012` pendente |
| Yield bruto mensal (`R27.6`) | `1.900 ÷ 236.125,246785` | 0,0080466 → 0,8047% |
| Yield líquido mensal (`R27.8`) | `1.170 ÷ 236.125,246785` | 0,0049550 → 0,4955% |
| Yield líquido anual (`R27.8`) | `0,0049550 × 12` | 0,0594600 → 5,9460% |
| Renda líquida anual | `1.170 × 12` | R$ 14.040,00 |

### F.1.5 Preço máximo e teto decisório

Entradas: `V = 300.000`, `c_v = 0,06`, `t = 0,15`, `F = 23.000`, `c_c = 0,05`,
`c_itbi = 0,02`, `r = 0,25`.

```
V(1−c_v)            = 300.000 × 0,94        = 282.000
V(1−c_v)(1−t)       = 282.000 × 0,85        = 239.700
(1 + r − t)         = 1 + 0,25 − 0,15       = 1,10
F(1 + r − t)        = 23.000 × 1,10         = 25.300
numerador           = 239.700 − 25.300      = 214.400
(1 + c_c + c_itbi)  = 1 + 0,05 + 0,02       = 1,07
denominador         = 1,07 × 1,10           = 1,177
preço_maximo        = 214.400 ÷ 1,177       = 182.158,0289
```

**Preço máximo por ROI alvo = R$ 182.158,03.**

Verificação da propriedade inversa de `R28.3` — o ROI recalculado com esse preço deve ser
exatamente 25%:

```
TCO            = 182.158,0289 × 1,07 + 23.000 = 194.909,0909 + 23.000 = 217.909,0909
V(1−c_v)       = 282.000
base de IR     = 282.000 − 217.909,0909      = 64.090,9091
IR             = 64.090,9091 × 0,15          = 9.613,6364
venda líquida  = 282.000 − 9.613,6364        = 272.386,3636
lucro líquido  = 272.386,3636 − 217.909,0909 = 54.477,2727
ROI            = 54.477,2727 ÷ 217.909,0909  = 0,250000  ✓  (erro < 1e-6)
```

O valor anterior desta spec, R$ 185.627,71, **omitia o ITBI** da derivação, embora o ITBI
seja proporcional ao preço. Incluí-lo reduz o teto em R$ 3.469,68 (`D27`).

| Referência | Valor | Rótulo correto |
|------------|-------|----------------|
| Preço máximo por ROI alvo de 25% (`R28.2`) | **R$ 182.158,03** | teto decisório econômico |
| Forma fechada conservadora do método (`R28.4`) | **R$ 168.374,76** | **teto conservador do método — referência informativa** |
| Preço máximo ajustado ao risco (`R28.9`) | provisório | dependente das pendências de inadimplência e ocupação |
| Teto decisório (`R28.4.2`) | `mínimo(182.158,03; ajustado)` | ≤ R$ 182.158,03 |

O valor de R$ 168.374,76 **nunca** deve ser rotulado como "preço máximo por ROI alvo": ele é
o resultado de uma álgebra diferente, que trata a base de IR sem o custo total de aquisição,
e por isso não satisfaz a definição de `R28.2`.

### F.1.6 Vereditos

| Estratégia | Indicador determinante | Threshold `STR` | Resultado | Camada determinante |
|------------|------------------------|-----------------|-----------|---------------------|
| revenda | desconto líquido = **18,5775%** | 25% | `DO_NOT_BUY` | 4 — economia |
| renda | yield líquido mensal = **0,4955%** | 0,80% | `DO_NOT_BUY` | 5 — estratégia |

As duas reprovações se mantêm e ficam **mais folgadas** do que na versão anterior:

- revenda: a folga de reprovação passa de `25% − 23,98% = 1,02` para
  `25% − 18,5775% = 6,4225` pontos percentuais;
- renda: a folga passa de `0,80% − 0,513% = 0,287` para
  `0,80% − 0,4955% = 0,3045` pontos percentuais.

Reforços independentes da economia:

- o preço máximo por ROI alvo, R$ 182.158,03, é **inferior** ao lance mínimo de
  R$ 191.651,31 em R$ 9.493,28; o teto conservador informativo também é inferior;
- a liquidez de 80 satisfaz `liquidez_min` de 75 para revenda e de 70 para renda, logo a
  camada 7 não é a determinante;
- a divergência de data entre portal e edital aciona `PENDENTE` e hard stop de lance
  (`RL-02`, `RL-10`, `REG-014`): mesmo que a economia melhorasse, o lance não seria liberado.

Ambas as reprovações são **econômicas**, não jurídicas.

Este é o caso que sustenta o piso de yield sobre o líquido: com o piso aplicado ao yield
**bruto** (0,8047% contra 0,80%) a estratégia de renda seria aprovada em um imóvel cujo
aluguel líquido é 61,58% do bruto (`1.170 ÷ 1.900`). Aplicar o piso ao líquido é o que
impede essa aprovação (`D31`, SAFE-016).

**Comparáveis registrados**

| Fonte | Empreendimento | Área m² | Quartos | Vagas | Preço | Preço/m² | Aluguel | Condomínio | Data |
|-------|----------------|---------|---------|-------|-------|----------|---------|------------|------|
| Portal A | Residencial Piazza San Pietro | 47,00 | 2 | 1 | R$ 320.000 | R$ 6.808,51 | R$ 1.700 | R$ 510 | 14/09/2026 |
| Portal B | Residencial Piazza San Pietro | 47,76 | 2 | 1 | R$ 300.000 | R$ 6.281,41 | R$ 1.700 | R$ 510 | 14/09/2026 |
| Fonte vendedora | Unidade em análise | 47,76 | 3 | 1 | R$ 191.651,31 | R$ 4.012,80 | R$ 1.900 | R$ 510 | 14/09/2026 |

## F.2 Reserva dos Pinhais

| Campo | Valor |
|-------|-------|
| Situação registral | Consolidação antiga |
| Matrícula | Certidão antiga em relação à data da análise |
| Leilões anteriores | Existentes |
| Averbação dos leilões negativos | `em tratamento` |

**Resultado esperado:** pendência registral, e não nulidade automática. Exigir matrícula
atualizada. Incorporar custo, prazo e documentação da regularização ao custo econômico
total. Cobre `REG-003`.

## F.3 Residencial Milano

| Campo | Valor |
|-------|-------|
| Identificador do imóvel | `855553513794-2` |
| Matrícula | `71502` |
| Avaliação da fonte | R$ 230.000,00 |
| Valor mínimo do segundo leilão | R$ 138.000,00 |
| Data da consolidação | 31/07/2026 |
| Data de emissão da matrícula | 03/08/2026 |
| Averbação dos leilões negativos | `nao_se_aplica` |
| Decisão de referência | `BUY_IF` com pendências |
| Confiança de referência | aproximadamente 78 |

**Resultado esperado:** cadeia registral recente é evidência forte, porém não comprova
que todas as notificações estão regulares nem substitui a verificação de processos,
ocupação, condomínio e tributos. Cobre `REG-002`. O valor mínimo do segundo leilão
corresponde a 60% da avaliação, logo `RULE-JUR-011` não é acionada.

## F.4 Conjunto Residencial Ouro Verde

| Campo | Valor |
|-------|-------|
| Ato registral | Consolidação com menção a intimação regular e ausência de purgação da mora |
| Localização da evidência | Averbação `AV-13` da matrícula |
| Gravames | Penhora histórica posteriormente levantada |
| Avaliação da fonte | R$ 285.000,00 |

**Resultado esperado:** ler o texto do ato registral é superior a apenas detectar o
evento. Gravame histórico baixado não é ônus atual. O valuation deve ser independente
da avaliação da fonte. Cobre `REG-002` e `REG-009`.

---

# Correctness Properties

Propriedades executáveis destinadas a teste baseado em propriedades. Cada propriedade
declara o gerador de entradas, a invariante e os requisitos cobertos. Propriedades que
dependem de serviços externos não estão nesta seção: consultas a cartório, tribunais,
concessionárias e portais são verificadas por testes de integração com um a três
exemplos representativos e por dublês nos testes de propriedade.

## P1 — Preservação e identidade da captura

| ID | Propriedade | Gerador | Requisitos |
|----|-------------|---------|-----------|
| P1.1 | O fingerprint da captura é invariante à ordem das chaves do payload | payloads aninhados com permutação de chaves | 2.2 |
| P1.2 | O fingerprint é determinístico: duas execuções sobre o mesmo payload produzem o mesmo valor | payloads arbitrários | 2.2 |
| P1.3 | Payloads com conteúdo diferente produzem fingerprints diferentes | pares de payloads distintos | 2.2 |
| P1.4 | Registrar a mesma captura `n` vezes resulta em exatamente um registro persistido (idempotência) | captura e `n` em 1 a 10 | 2.3 |
| P1.5 | Para qualquer sequência de operações, nenhuma captura previamente registrada é alterada ou removida | sequências de capturas e correções | 2.4, 2.5 |

## P2 — Normalização sem invenção de dados

| ID | Propriedade | Gerador | Requisitos |
|----|-------------|---------|-----------|
| P2.1 | Todo campo ausente no payload resulta em `UNKNOWN` na oferta normalizada, nunca em zero, string vazia ou valor padrão | payloads com subconjuntos aleatórios de campos | 3.2 |
| P2.2 | Round-trip de valores monetários: `parse(format(v)) == v` para valores em BRL com duas casas | decimais de 0 a 10^9 | 3.4 |
| P2.3 | Round-trip de áreas: `parse(format(a)) == a` para áreas com duas casas | decimais de 0,01 a 10^5 | 3.4 |
| P2.4 | Round-trip de percentuais: `parse(format(p)) == p` | frações de 0 a 1 | 3.4 |
| P2.5 | Round-trip de datas e datas com hora no formato brasileiro | datas de 1900 a 2100 | 3.4 |
| P2.6 | Normalizar duas vezes a mesma captura produz o mesmo resultado (idempotência) | capturas arbitrárias | 3.1, 3.11 |
| P2.7 | A lista de campos ausentes retornada é exatamente o conjunto de campos relevantes com valor `UNKNOWN` | capturas com lacunas aleatórias | 3.9 |
| P2.8 | O valor de avaliação da fonte nunca é atribuído ao campo de valor de mercado | capturas com avaliação presente | 3.10 |
| P2.9 | O tipo de área nunca é inferido quando a fonte não o declara | capturas com rótulos de área ambíguos | 3.5 |
| P2.10 | Invariância de magnitude na interpretação numérica: para o mesmo número apresentado em qualquer notação aceita — pt-BR `"1.234,56"`, sem separador de milhar `"1234,56"` e com ponto decimal `"1234.56"` — o valor interpretado é o mesmo | números de 0,01 a 10^9 renderizados nas três notações | 3.4.1 |
| P2.11 | Percentual sempre normalizado: o resultado está em `[0, 1]` ou é `UNKNOWN`, e a unidade declarada na entrada é respeitada, inclusive para alíquotas fracionárias e para o caso de um por cento | percentuais de 0 a 100 com uma e duas casas decimais, em notação de fração e de porcentagem | 3.4.2, 3.4.3 |
| P2.12 | Entrada não interpretável resulta em `UNKNOWN`, nunca em zero | strings arbitrárias, incluindo vazia, apenas símbolos e texto livre | 3.2, 3.4.4 |
| P2.13 | Precedência de vacância: qualquer texto que contenha termo de desocupação resulta em desocupado, mesmo quando o termo contém "ocupado" como subcadeia | textos com termos de ocupação e vacância combinados | 3.8 |

## P3 — Identidade e deduplicação

| ID | Propriedade | Gerador | Requisitos |
|----|-------------|---------|-----------|
| P3.1 | A resolução de identidade é total: retorna exatamente um nível de `I0` a `I4` | ofertas normalizadas arbitrárias | 7.1 |
| P3.2 | Monotonicidade: acrescentar um identificador mais forte nunca reduz o nível de identidade | pares de ofertas em relação de subconjunto de evidências | 7.2 a 7.6 |
| P3.3 | Invariância ao preço: alterar apenas preço, avaliação ou desconto não altera o nível de identidade | ofertas com preço variado | 7.7 |
| P3.4 | Invariância ao preço na deduplicação: alterar apenas preço não altera o veredito de `is_same_property` | pares de ofertas com preço variado | 9.5 |
| P3.5 | Matrícula é decisiva: matrículas iguais implicam veredito verdadeiro e matrículas distintas implicam veredito falso, para qualquer combinação dos demais campos | pares de ofertas com matrícula controlada | 9.1 |
| P3.6 | Simetria: `is_same_property(a, b)` é igual a `is_same_property(b, a)` | pares arbitrários | 9.1 a 9.6 |
| P3.7 | Reflexividade: `is_same_property(a, a)` nunca retorna falso | ofertas arbitrárias | 9.1 a 9.6 |
| P3.8 | Idempotência da associação: associar a mesma captura ao mesmo imóvel `n` vezes produz um único vínculo | captura, imóvel e `n` em 1 a 10 | 9.7 |
| P3.9 | Unidades distintas no mesmo condomínio nunca são fundidas | pares no mesmo condomínio com unidades diferentes | 9.11 |
| P3.10 | Evidência insuficiente resulta em veredito indefinido, nunca em verdadeiro ou falso | pares com evidência fraca | 9.6 |
| P3.11 | Desfazer uma associação preserva o registro histórico da associação anterior | sequências de associação e correção | 9.9 |

## P4 — Gate jurídico determinístico

| ID | Propriedade | Gerador | Requisitos |
|----|-------------|---------|-----------|
| P4.1 | Determinismo: a mesma entrada de verificações produz sempre o mesmo `legal_status` | conjuntos de resultados de verificação | 12.5, 12.6 |
| P4.2 | Confluência: a ordem de avaliação das verificações não altera o `legal_status` | permutações do conjunto de verificações | 12.1, 12.5 |
| P4.3 | Precedência interna: existindo ao menos uma verificação `IRREGULAR`, o resultado é `BLOCK`, independentemente das demais | conjuntos com pelo menos um `IRREGULAR` | 12.6, 13.4 |
| P4.4 | Ausência de evidência nunca produz `OK`: existindo ao menos uma verificação obrigatória `UNKNOWN` e nenhuma `IRREGULAR`, o resultado é `PENDENTE` | conjuntos com pelo menos um `UNKNOWN` | 12.6, 20.7 |
| P4.5 | Toda verificação avaliada gera exatamente uma evidência registrada, inclusive as `UNKNOWN` | conjuntos arbitrários | 20.1, 20.7 |
| P4.6 | Cobertura total: toda análise avalia e registra resultado para todos os itens aplicáveis do Anexo A | análises geradas com combinações de dados disponíveis | 36.5 |
| P4.7 | Ocupação nunca altera o `legal_status` | conjuntos de verificações com estado de ocupação variado | 18.2, 18.8 |
| P4.8 | Processo judicial sem impacto material classificado nunca produz `BLOCK` | processos com impacto `nenhum` | 16.6 |

## P5 — Camada de evidência

| ID | Propriedade | Gerador | Requisitos |
|----|-------------|---------|-----------|
| P5.1 | Nenhuma evidência é aceita sem fonte identificada | evidências com campos opcionais nulos | 20.3 |
| P5.2 | Nenhuma transição leva um fato de `UNKNOWN` a `CONFIRMED` sem o registro de nova evidência de suporte | sequências de operações sobre um fato | 20.4 |
| P5.3 | Monotonicidade do repositório: a quantidade de evidências registradas nunca diminui | sequências arbitrárias de escrita | 20.5, 20.6 |
| P5.4 | Registrar evidências contraditórias preserva todas e marca o fato como conflitante | pares de evidências contraditórias | 20.5 |
| P5.5 | Todo valor apresentado possui exatamente um estado de informação atribuído | conjuntos de fatos consolidados | 10.2 |

## P6 — Cálculos econômicos

| ID | Propriedade | Gerador | Requisitos |
|----|-------------|---------|-----------|
| P6.1 | Conservação de valor: o custo econômico total é exatamente a soma dos componentes | componentes de custo não negativos | 26.1, 26.11 |
| P6.2 | Monotonicidade do TCO: aumentar qualquer componente nunca reduz o total | componentes e incremento positivo | 26.1 |
| P6.3 | Monotonicidade do desconto líquido: aumentar qualquer componente de custo nunca aumenta o desconto líquido | custos, incremento e valor de mercado positivo | 27.3 |
| P6.4 | Monotonicidade da margem: aumentar qualquer componente de custo nunca aumenta a margem absoluta nem a margem percentual | custos, incremento e valor de mercado positivo | 27.4, 27.5 |
| P6.5 | Identidade metamórfica: `desconto_liquido` é igual a `margem_percentual` quando ambos usam o mesmo TCO e o mesmo valor de mercado | TCO e valor de mercado positivos | 27.3, 27.5 |
| P6.6 | Consistência entre yields: `yield_bruto_anual` é igual a `yield_bruto_mensal × 12` e `yield_liquido_anual` é igual a `yield_liquido_mensal × 12` | aluguéis e TCO positivos | 27.6, 27.8 |
| P6.7 | O yield líquido nunca excede o yield bruto para custos recorrentes não negativos | aluguel, custos recorrentes e TCO positivos | 27.7, 27.8 |
| P6.8 | Monotonicidade do yield: aumentar o TCO nunca aumenta o yield, e aumentar o aluguel nunca reduz o yield | aluguel, TCO e incrementos positivos | 27.6, 27.8 |
| P6.9 | A base de IR nunca é negativa | preços de venda, custos e TCO arbitrários | 27.10 |
| P6.10 | Condição de erro: valor de mercado menor ou igual a zero resulta em sinalização de erro em todas as métricas dependentes | valores de mercado não positivos | 27.16 |
| P6.11 | Determinismo: duas execuções com as mesmas entradas produzem exatamente os mesmos resultados em todas as métricas | entradas arbitrárias | 27.17 |
| P6.12 | O break-even de saída, usado como preço de venda, produz lucro líquido igual a zero dentro da tolerância de arredondamento | TCO e custos de saída positivos | 27.14 |

## P7 — Preço máximo

| ID | Propriedade | Gerador | Requisitos |
|----|-------------|---------|-----------|
| P7.1 | Propriedade inversa: usar o preço máximo como preço de aquisição produz ROI líquido igual ao ROI alvo, dentro de tolerância de 10^-6 | valor de venda, custos fixos, percentuais e ROI alvo válidos | 28.2 |
| P7.2 | Monotonicidade decrescente no ROI alvo: aumentar o ROI alvo nunca aumenta o preço máximo | ROI alvo crescente | 28.2 |
| P7.3 | Monotonicidade decrescente nos custos fixos: aumentar os custos fixos nunca aumenta o preço máximo | custos fixos crescentes | 28.2 |
| P7.4 | Monotonicidade crescente no valor de saída: aumentar o valor de venda nunca reduz o preço máximo | valor de venda crescente | 28.2 |
| P7.5 | O preço máximo nunca é negativo | entradas arbitrárias válidas | 28.2 |
| P7.6 | O preço máximo ajustado ao risco nunca excede o preço máximo econômico | custos de risco e margens adicionais não negativos | 28.9 |
| P7.7 | Implicação de decisão: preço de oferta acima do preço máximo ajustado resulta em `DO_NOT_BUY` para a estratégia | preços e preços máximos arbitrários | 28.13, 33.2 |
| P7.8 | O preço-alvo nunca excede o preço máximo | folgas não negativas | 28.12 |
| P7.9 | Liquidez indefinida impede a emissão de preço máximo definitivo | estados de liquidez variados | 28.11 |
| P7.10 | O teto decisório nunca excede o preço máximo exato nem o preço máximo ajustado ao risco: `teto_decisorio == min(exato, ajustado)` | entradas válidas com ROI alvo positivo e custos de risco não negativos | 28.4.2 |
| P7.11 | O preço máximo é monotônico decrescente no ITBI: aumentar `c_itbi` nunca aumenta o preço máximo | alíquotas de ITBI crescentes | 28.2, 28.2.1 |
| P7.12 | Contraexemplo verificado, mantido como exemplo dirigido e **não** como propriedade: com a entrada completa `V = 300.000`, `c_v = 0,06`, `F = 23.000`, `c_c = 0,05`, `r = 0,25`, `t = 0` e `c_itbi = 0`, o teto conservador do método (`259.000 ÷ 1,30 =` R$ 199.230,77) excede o preço máximo exato (`253.250 ÷ 1,3125 =` R$ 192.952,38). Com `c_itbi = 0,02` o exato cai para `253.250 ÷ 1,3375 =` R$ 189.345,79 e a diferença sobe de R$ 6.278,39 para R$ 9.884,98, ou seja, o ITBI agrava a falsidade. A propriedade "conservador ≤ exato" é falsa e foi removida | exemplo fixo com as sete entradas declaradas, incluindo `c_itbi = 0` | 28.4.1 |

## P8 — Cenários e risco

| ID | Propriedade | Gerador | Requisitos |
|----|-------------|---------|-----------|
| P8.1 | Ordenação de cenários: a margem no cenário otimista é maior ou igual à do base, que é maior ou igual à do conservador, que é maior ou igual à do estressado | conjuntos coerentes de premissas por cenário | 32.1 a 32.4 |
| P8.2 | Se a tese sobrevive ao cenário estressado, então sobrevive a todos os cenários | premissas arbitrárias | 32.6 |
| P8.3 | A classificação de robustez é total e consistente com os resultados dos cenários | resultados de cenários arbitrários | 32.6 |
| P8.4 | A severidade do risco é total sobre o produto de probabilidade e impacto | pares probabilidade e impacto | 34.3, 34.4 |
| P8.5 | Monotonicidade da severidade: aumentar a probabilidade ou o impacto nunca reduz a severidade | pares com incremento | 34.4 |
| P8.6 | Risco de severidade `critico` sempre produz `BLOCK`, **para qualquer estado de evidência** e independentemente das demais dimensões | riscos com severidade `critico` e estado de evidência variado, métricas arbitrárias | 34.5, 12.3 |
| P8.8 | `BLOCK` por risco crítico com evidência `ESTIMATED` ou `INFERRED` sempre acompanha condição objetiva de desbloqueio registrada | riscos críticos presumidos | 34.5.1 |
| P8.7 | Categoria não investigada resulta em risco `UNKNOWN`, nunca em `baixo` | conjuntos com categorias omitidas | 34.9 |

## P9 — Liquidez

| ID | Propriedade | Gerador | Requisitos |
|----|-------------|---------|-----------|
| P9.1 | A categoria de liquidez é uma função total e monotônica não decrescente do score, com exatamente sete faixas contínuas e sem lacuna sobre `[0, 100]`, incluindo valores fracionários junto a cada fronteira | reais em `[0, 100]`, incluindo 39,5 · 49,5 · 59,5 · 69,5 · 79,5 · 89,5 | 40.2 |
| P9.2 | O score de liquidez permanece na faixa de 0 a 100 para qualquer combinação de componentes | componentes de 0 a 100 | 40.1, 40.3 |
| P9.3 | Monotonicidade: melhorar qualquer componente com peso positivo nunca reduz o score de liquidez | componentes e incremento | 40.3 |
| P9.4 | Liquidez abaixo do mínimo da estratégia nunca resulta em `BUY` sem exceção registrada | scores e estratégias arbitrárias | 40.7 |
| P9.5 | Aumentar o prazo estimado nunca reduz a margem adicional exigida | prazos crescentes | 41.4, 30.7 |

## P10 — Score, Fit e ranking

| ID | Propriedade | Gerador | Requisitos |
|----|-------------|---------|-----------|
| P10.1 | Todo conjunto de pesos vigente soma exatamente 1,00 dentro de tolerância de 10^-9 | conjuntos de pesos da configuração | 49.5 |
| P10.2 | O Opportunity Score permanece na faixa de 0 a 100 para qualquer combinação de fatores | fatores de 0 a 100 | 49.1, 49.2 |
| P10.3 | Monotonicidade: melhorar um fator com peso positivo nunca reduz o Opportunity Score | fatores e incremento | 49.2 |
| P10.4 | A soma das contribuições registradas por fator é igual ao Opportunity Score | fatores arbitrários | 49.7 |
| P10.5 | O Investor Fit Score permanece na faixa de 0 a 100 | componentes de 0 a 100 | 51.1 |
| P10.6 | O Investor Fit nunca converte `BLOCK` em `BUY` | decisões com `BLOCK` e Fit variado | 51.4, 12.3 |
| P10.7 | O score de prioridade é monotônico não decrescente em cada fator multiplicativo | fatores em 0 a 1 | 52.1, 52.2 |
| P10.8 | O ranking é uma ordem total: a relação de precedência é antissimétrica, transitiva e total | conjuntos de oportunidades | 52.4 |
| P10.9 | Confluência do ranking: permutar a ordem de entrada não altera a ordem de saída | permutações do mesmo conjunto | 52.4 |
| P10.10 | Consistência do ranking: se o score de prioridade de A é maior que o de B, então A precede B, salvo aplicação registrada de critério de desempate | pares de oportunidades | 52.4 |
| P10.11 | Determinismo do desempate: entradas com scores iguais produzem sempre a mesma ordem | conjuntos com empates | 52.4 |
| P10.12 | Exclusão de bloqueados: nenhuma oportunidade com decisão `BLOCK` aparece no ranking operacional | conjuntos com bloqueados | 52.3 |
| P10.13 | Idempotência do ranking: recalcular o ranking sobre o mesmo estado produz a mesma ordem | estados arbitrários | 52.4 |
| P10.14 | Cobertura total das faixas de score: para qualquer valor real em `[0, 100]`, a classificação retorna exatamente uma faixa, e faixas adjacentes não deixam lacuna nem se sobrepõem | reais em `[0, 100]`, incluindo os limites e valores fracionários junto a cada fronteira | 49.6 |
| P10.15 | Cobertura total do fator de confiança: para qualquer valor real em `[0, 100]`, o fator retornado é o da faixa correta, e o fator é monotônico não decrescente na confiança | reais em `[0, 100]`, incluindo fronteiras fracionárias | 50.3, 50.4 |
| P10.16 | Totalidade do enum de status jurídico: qualquer valor fora do conjunto `OK`, `PENDENTE`, `BLOCK` é rejeitado na fronteira, e nenhum valor desconhecido é interpretado como liberado | strings arbitrárias, incluindo variações de caixa dos valores válidos | 12.5, 12.6 |
| P10.17 | Os sete pesos do Investor Fit somam exatamente 1,00 dentro de 10^-9, e nenhum componente de qualidade econômica participa do Fit | conjunto de pesos vigente | 51.1, 51.1.1 |
| P10.18 | Cada uma das cinco colunas de pesos por estratégia soma exatamente 1,00 dentro de 10^-9 **e inclui** `qualidade_oportunidade` com peso estritamente positivo | conjuntos de pesos por estratégia | 49.5, 49.2 |
| P10.19 | O score de prioridade é o produto de exatamente cinco fatores, e concentração influencia o resultado por exatamente um caminho: zerar o componente `diversificacao` do Fit elimina toda a sensibilidade do score de prioridade à concentração | carteiras com concentração variada | 52.1, 52.1.1, 47.4.1 |
| P10.20 | A escala de urgência e a escala de atratividade combinada não compartilham rótulos: nenhum valor pertence às duas | valores das duas escalas | 52.6, 52.6.1 |

## P11 — Motor de decisão

| ID | Propriedade | Gerador | Requisitos |
|----|-------------|---------|-----------|
| P11.1 | Totalidade: para qualquer entrada, exatamente um dos cinco estados de decisão é emitido | entradas de decisão arbitrárias | 53.5 |
| P11.2 | Não compensação de `BLOCK`: para qualquer combinação de score, desconto, margem, yield, liquidez, Fit e eficiência de capital, existindo `BLOCK` a decisão é `BLOCK` | entradas com `legal_status` igual a `BLOCK` ou risco crítico confirmado | 12.3, 53.4 |
| P11.3 | A camada determinante reportada é a de menor índice entre as camadas que eliminam a oportunidade | entradas com múltiplas falhas simultâneas | 53.1 a 53.3 |
| P11.4 | Nenhuma camada posterior altera o resultado de uma camada anterior eliminatória | entradas com falhas em camadas distintas | 53.4 |
| P11.5 | `legal_status` igual a `PENDENTE` nunca resulta em `BUY` | entradas com `PENDENTE` e métricas favoráveis | 12.8 |
| P11.6 | Confiança abaixo de `GLB-003` nunca resulta em `BUY` | confianças de 0 a 100 | 50.6 |
| P11.7 | Pendência de prioridade crítica em aberto nunca resulta em `BUY` nem em `DO_NOT_BUY` | conjuntos de pendências | 37.3 |
| P11.8 | `BUY_IF` sempre acompanha ao menos uma condição objetiva registrada | entradas que produzem `BUY_IF` | 53.7 |
| P11.9 | `MONITOR` sempre acompanha ao menos um gatilho de reentrada registrado | entradas que produzem `MONITOR` | 53.8 |
| P11.10 | Monotonicidade da decisão na confiança: aumentar a confiança, mantendo o restante, nunca piora a decisão na ordem `BLOCK` < `DO_NOT_BUY` < `MONITOR` < `BUY_IF` < `BUY` | confianças crescentes | 55.1 a 55.9 |
| P11.11 | Monotonicidade da decisão no desconto líquido: aumentar o desconto líquido, mantendo o restante, nunca piora a decisão | descontos crescentes | 33.3 |
| P11.12 | Determinismo: a mesma entrada de decisão produz sempre a mesma decisão e a mesma camada determinante | entradas arbitrárias | 53.1 |
| P11.13 | Exceção não contorna bloqueio: para qualquer exceção registrada, existindo `BLOCK` jurídico ou risco crítico confirmado, a decisão permanece `BLOCK` | exceções e entradas com bloqueio | 63.4 |
| P11.14 | Rastreabilidade: toda decisão persistida referencia ao menos uma evidência e ao menos uma versão de regra | decisões geradas arbitrariamente | 56.8, 61.4 |
| P11.15 | Totalidade da matriz de score × confiança: para qualquer par de score e confiança em `[0, 100]²`, a matriz retorna exatamente uma ação, sem lacuna e sem sobreposição entre as 15 células | pares reais em `[0, 100]²`, incluindo fronteiras fracionárias 59,5 · 69,5 · 79,5 · 89,5 e 59,5 · 74,5 | 55.1 a 55.16 |
| P11.16 | Onze camadas: a camada determinante reportada pertence sempre ao intervalo de 0 a 10, e a decisão final nunca é reportada como camada | entradas com falhas em camadas distintas | 53.1, 53.1.1 |
| P11.17 | Ausência de evidência nunca produz resultado favorável: para qualquer verificação com estado `UNKNOWN`, o resultado é `PENDENTE` ou mais restritivo, nunca `REPROVADO` nem liberação | conjuntos de verificações com `UNKNOWN` | `P-E`, 36.3.1, 36.3.2 |
| P11.18 | Evidência de ausência produz o efeito da regra: cláusula de evicção comprovadamente inexistente no edital obtido resulta em `BLOCK`, e cláusula não verificada resulta em `PENDENTE`; os dois casos são distinguíveis no registro | estados de evicção variados | 15.9, 15.9.1, 15.9.2 |
| P11.19 | Precedência de escopo: para qualquer par de escopos, o mais específico prevalece, exceto quando o menos específico impõe bloqueio crítico ou restrição legal ou documental | hierarquias de parâmetros com conflitos gerados | 54.10, 54.10.1 |

## P12 — Orquestração

| ID | Propriedade | Gerador | Requisitos |
|----|-------------|---------|-----------|
| P12.1 | O traço de fases executadas é sempre uma subsequência da ordem canônica de fases | estados iniciais arbitrários | 70.1, 70.5 |
| P12.2 | Curto-circuito jurídico: com `BLOCK` no gate, as fases de enriquecimento, valuation, custo, liquidez, estratégia e score não aparecem no traço | estados com `BLOCK` | 70.2, 12.2 |
| P12.3 | Curto-circuito de identidade: com identidade inferior a `I2`, as fases posteriores à identificação até a decisão não aparecem no traço | estados com identidade fraca | 70.3, 7.9 |
| P12.4 | Determinismo do pipeline: o mesmo estado inicial produz o mesmo traço e o mesmo resultado | estados arbitrários | 70.1 |
| P12.5 | Equivalência de execução: a execução orquestrada e a execução sequencial de referência produzem o mesmo resultado (teste baseado em modelo) | estados arbitrários | 70.1, 70.6 |

## P13 — Monitoramento e governança

| ID | Propriedade | Gerador | Requisitos |
|----|-------------|---------|-----------|
| P13.1 | Limiar de materialidade: mudança de magnitude inferior ao limiar não dispara reavaliação; mudança igual ou superior dispara | magnitudes em torno do limiar, incluindo o valor exato | 57.2, 57.3 |
| P13.2 | Versionamento monotônico: as versões de análise por oportunidade são estritamente crescentes e sem lacunas | sequências de análises | 61.1 |
| P13.3 | Imutabilidade: após persistir uma nova análise, todas as anteriores permanecem byte a byte inalteradas | sequências de análises | 61.2 |
| P13.4 | Reprodutibilidade: reexecutar uma análise histórica com as mesmas versões de regras, parâmetros e dados produz a mesma decisão | análises históricas arbitrárias | 61.4, 62.8 |
| P13.5 | Vigência temporal: uma análise com data `D` utiliza exclusivamente versões de regra e de parâmetro vigentes em `D` | datas e conjuntos de versões | 62.8 |
| P13.6 | Antiviés temporal: nenhum dado com data posterior à data da decisão entra no conjunto usado pelo backtest | conjuntos de dados com datas variadas | 60.4, 60.5 |
| P13.7 | Trilha append-only: a quantidade de eventos de auditoria é monotônica não decrescente e nenhum evento registrado é alterado | sequências de operações | 64.1, 64.3 |
| P13.8 | Resolução de parâmetro: o escopo mais específico com versão vigente é sempre o aplicado, e o escopo aplicado é sempre registrado | hierarquias de parâmetros arbitrárias | 62.10 |
| P13.9 | Expiração de exceção: após a data de validade, a regra padrão é restaurada e a reavaliação é disparada | exceções com prazos variados | 63.5 |
| P13.10 | Idempotência da reavaliação: reavaliar duas vezes sem mudança de entrada produz o mesmo resultado e não cria nova versão | estados arbitrários | 57.6, 61.1 |

## P14 — Disciplina de lance

| ID | Propriedade | Gerador | Requisitos |
|----|-------------|---------|-----------|
| P14.1 | `PODE_DAR_LANCE` é emitido se e somente se os 12 itens pré-lance são `SIM`, nenhum hard stop está acionado, os tetos estão definidos e o lance atual não excede o teto absoluto | combinações booleanas dos 12 itens e 9 hard stops | C.4 |
| P14.2 | Qualquer hard stop acionado resulta em `NAO_DAR_LANCE`, independentemente do checklist | combinações com ao menos um hard stop | C.3, C.4 |
| P14.3 | Lance atual acima do teto absoluto resulta em `NAO_DAR_LANCE` | pares de lance e teto | C.4, C.6 |
| P14.4 | Garantia contra evicção não confirmada impede a liberação de lance, tanto no caso de ausência comprovada quanto no caso de não verificação | estados de evicção variados | C.2, 82.4 |
| P14.5 | `LIBERADO_PARA_LANCE` é emitido se e somente se os doze itens `PL-01` a `PL-12` e os doze itens `RL-01` a `RL-12` são `SIM`, nenhum hard stop está acionado e o lance atual não excede o teto absoluto | combinações booleanas dos 24 itens e dos 9 hard stops | C.7, 82.6 |
| P14.6 | Divergência documental pendente resulta em `NAO_DAR_LANCE`, independentemente do restante do checklist | divergências e checklists arbitrários | 82.10 |
| P14.7 | A comissão do leiloeiro nunca é subtraída do lance: para qualquer lance, o custo total de aquisição é estritamente maior que o lance quando a comissão é positiva | lances e percentuais de comissão positivos | 82.7 |

## P16 — Escopo, dicionário e priorização

| ID | Propriedade | Gerador | Requisitos |
|----|-------------|---------|-----------|
| P16.1 | Cobertura de catálogo: todo item `MC-001` a `MC-136`, `B-01` a `B-27` e `C-01` a `C-71` possui exatamente um resultado registrado por análise, ou é explicitamente `nao_aplicavel` | análises geradas com combinações de dados disponíveis | 36.5, `D17` |
| P16.2 | Cobertura de prioridade: todo requisito de 1 a 83 possui exatamente uma classificação entre `P0`, `P1`, `P2` e `fora do MVP` | conjunto de requisitos | 75.5 |
| P16.3 | Parâmetro `[PENDENTE-DECISÃO]` nunca é aplicado: o requisito dependente é reportado como NÃO AVALIADO, nunca como satisfeito | parâmetros pendentes e análises arbitrárias | `D54`, 74.11 |
| P16.4 | Toda regra aplicada depende apenas de entidades e campos declarados no dicionário; regra que dependa de estrutura ausente é rejeitada | conjuntos de regras e dicionários parciais | 74.11 |
| P16.5 | Os pontos mínimos de intervenção humana não são removíveis: para qualquer configuração, os sete pontos de `R83.5` permanecem exigidos | configurações arbitrárias | 83.5, 83.6 |
| P16.6 | Texto-fonte e paráfrase permanecem distinguíveis em todo segmento recuperado | documentos arbitrários | 72.3.1, 72.3.2 |

## P15 — Ingestão de conhecimento

| ID | Propriedade | Gerador | Requisitos |
|----|-------------|---------|-----------|
| P15.1 | Todo segmento indexado possui identificador, tipo e metadados obrigatórios preenchidos | documentos arbitrários | 72.3, 72.4 |
| P15.2 | Nenhuma regra jurídica indexada é aceita sem fonte e proveniência | segmentos de regra arbitrários | 72.5 |
| P15.3 | Reingerir o mesmo documento não duplica segmentos (idempotência por fingerprint) | documentos e repetições | 72.1 |
| P15.4 | Todo item recuperado da memória histórica é marcado como hipótese, nunca como evidência atual | consultas arbitrárias | 72.9 |

---

# Diagnóstico Técnico — Revisão do Estado Atual

Revisão realizada por inspeção direta de `src/radar/`, `db/schema.sql`, `spec/`,
`tests/`, `pyproject.toml` e da spec parcial `.kiro/specs/pipeline-captura-identidade-gate-juridico/`.
Cada achado cita o artefato inspecionado. Nenhum código foi alterado.

## D.1 Defeitos de cálculo (verificados numericamente)

**D.1.1 — `max_price_by_target_roi` não satisfaz a própria definição. Severidade: crítica.**

`src/radar/engines/calculation.py`, função `max_price_by_target_roi`. O docstring afirma
resolver o preço tal que o ROI líquido resultante seja igual ao ROI alvo. Com as entradas
do Golden Case do item 227 — valor de venda R$ 300.000, custos fixos R$ 23.000, comissão
de compra 5%, corretagem de venda 6%, IR 15% e ROI alvo 25% — os três valores divergem:

| Origem | Preço máximo | ROI líquido efetivo |
|--------|--------------|---------------------|
| Implementação atual | R$ 163.352,38 | ≈ 38,6% |
| Forma fechada conservadora do método de referência | R$ 168.374,76 | ≈ 34,97% |
| Solução exata sem ITBI no coeficiente proporcional | R$ 185.627,71 | 25,00% sobre um TCO que subestima o ITBI |
| **Solução exata de `R28.2`, com ITBI** | **R$ 182.158,03** | **25,00%** |

A quarta linha é a correta e é a única que satisfaz `R28.2` e a propriedade `P7.1`. A
terceira linha constava da versão anterior desta spec e omitia o ITBI do coeficiente
proporcional ao preço, embora o ITBI seja proporcional ao preço (`D27`). A derivação completa
e a verificação inversa estão em `F.1.5`.

Causa raiz: o código calcula `total_cost = venda_liquida ÷ (1 + ROI)` tratando a venda
líquida como independente do custo total, e depois divide por `(1 + comissão)`. A base de
IR usada é `venda − custos_fixos`, ignorando o custo total de aquisição, que é a base
efetivamente usada em `Requirement 27.10` e na própria planilha. A forma fechada da planilha
comete a mesma simplificação na base de IR, mas com álgebra diferente, e por isso também
não retorna o ROI alvo. O resultado prático é um teto de preço 12% abaixo do correto,
o que produz falsos negativos econômicos: oportunidades viáveis são reprovadas.

Observação relevante: a documentação e o `README.md` afirmam que os cálculos estão
"validados contra os números reais da planilha Método Jabes". A validação cobre o TCO
(R$ 228.066,90, confirmado), mas **não** cobre o preço máximo. O teste
`tests/test_calculation.py::test_max_price_by_target_roi_below_current_bid` assere apenas
`max_price < 191_651.31`, o que passa com qualquer um dos três valores acima e por isso
não detecta o defeito. A propriedade `P7.1` deste documento detecta.

**D.1.2 — TCO incompleto em relação a `RULE-FIN-001`. Severidade: alta.**

`CostBreakdown` em `src/radar/domain/models.py` e a tabela `costs` em `db/schema.sql`
contêm dez componentes: `preco`, `comissao_leiloeiro`, `itbi`, `registro_documentacao`,
`condominio_debitos`, `tributos_debitos`, `reforma`, `reserva_imprevistos`,
`custo_juridico_esperado` e `carrying`. Faltam **três** componentes que `R26.1` exige:
`regularizacao`, `desocupacao` e `custo_financeiro`. O `CostBreakdown` passa, portanto, de
dez para **treze** componentes.

`custo_saida_corretagem` e `ir_ganho_capital` **não** entram no `CostBreakdown`: por `R26.1.1`
eles pertencem exclusivamente à perna de venda. A versão anterior desta spec os incluía no
TCO e os subtraía novamente em `R27.9` e `R27.11`, o que contava os custos de saída duas
vezes — no caso de prova `F.1` a dupla contagem valia 7,69 pontos percentuais de ROI — e
tornava a definição do IR circular, já que `R27.10` define a base do IR subtraindo o TCO
(`D26`). Consequência do defeito remanescente: o desconto líquido e a margem são
superestimados em operações com imóvel ocupado, com pendência registral ou financiadas.
Afeta `MC-082`, `MC-083` e `MC-085`.

**D.1.3 — `parse_money` corrompe decimal com ponto por fator de 100. Severidade: crítica.**

`src/radar/capture/parsing.py`. A expressão `_MONEY_RE = r"-?[\d.]+(?:,\d+)?"` captura o
ponto como separador de milhar e a função executa `replace(".", "")` incondicionalmente.
Verificado em execução:

| Entrada | Retorno | Esperado |
|---------|---------|----------|
| `"R$ 191.651,31"` | `191651.31` | correto |
| `"47.76"` | `4776.0` | `47.76` |
| `parse_area("47.76")` | `4776.0` | `47.76` |

Qualquer fonte que entregue JSON, CSV ou API com ponto decimal — o caso normal fora de
texto renderizado em pt-BR — produz valor cem vezes maior. Em `min_bid` contamina o TCO,
o desconto líquido e o preço máximo; em `area_m2` contamina o preço por metro quadrado e
toda a seleção de comparáveis. Os 22 testes atuais não cobrem esse formato, e as
propriedades de round-trip `P2.2` a `P2.4` também não o alcançam, porque partem de um
formatador pt-BR. A propriedade que detecta é `P2.10`, de invariância de magnitude entre
notações.

**D.1.4 — `parse_percent` erra percentual fracionário e o caso de 1%. Severidade: alta.**

Mesmo arquivo. `parse_percent` delega a `parse_money` e por isso herda o defeito acima;
além disso usa a heurística `valor > 1` para decidir se divide por 100. Verificado:

| Entrada | Retorno | Esperado |
|---------|---------|----------|
| `"5%"` | `0.05` | correto |
| `"2.5%"` | `0.25` | `0.025` |
| `1` (um por cento) | `1.0` | `0.01` |

Em `comissao_leiloeiro_pct` e `itbi_pct` isso é erro direto de custo. A heurística é
aceitável para percentuais inteiros, mas não para alíquotas fracionárias, que existem no
domínio (ITBI municipal, corretagem negociada). O contrato correto é exigir a unidade na
entrada, não inferi-la.

**D.1.5 — `classify_score` e `confidence_factor` têm lacunas para valores não inteiros. Severidade: alta.**

`src/radar/domain/parameters.py`. `ScoreBand.contains` e `CONFIDENCE_TIERS` usam limites
inteiros fechados (`lo <= x <= hi`), o que deixa o intervalo aberto entre `hi` de uma faixa
e `lo` da seguinte. Verificado:

| Chamada | Retorno | Esperado |
|---------|---------|----------|
| `classify_score(89.5)` | `🔴 Fraca` | `🟢 Excelente` |
| `confidence_factor(89.5)` | `0.60` | `0.95` |
| `confidence_factor(74.5)` | `0.60` | `0.88` |

O erro é de pior caso, não de arredondamento: um score de 89,5 cai na última banda e uma
confiança de 89,5 recebe o menor fator possível, com impacto de até 0,35 no multiplicador
de `Requirement 52`. `classify_score` é usado em produção na explicação gerada por
`analysis_service._explain`. As faixas devem ser definidas por limite inferior com
comparação `>=` em ordem decrescente, cobrindo todo o domínio contínuo `[0, 100]`.
As propriedades `P10.14` e `P10.15` detectam.

**D.1.6 — desconto líquido e margem percentual são a mesma expressão. Severidade: média (de especificação).**

`net_discount(tco, vm) = 1 − tco/vm` e `margin_pct(tco, vm) = (vm − tco)/vm` são
algebricamente idênticos, e a Especificação Canônica §9 os define assim. Consequência
em `engines/decision.py`: a condição
`net_discount >= desconto_liquido_min AND margin_pct >= margem_min` colapsa em
`>= max(dois)`, de modo que `margem_min` **nunca** é restrição ativa — revenda 0,20 sob
0,25; renda 0,15 sob 0,15; MCMV 0,15 sob 0,20. O teste
`tests/test_calculation.py::test_net_discount_and_margin` confirma ambos com o mesmo valor
0,2398 sem sinalizar a redundância. A coluna `margem_min` da tabela `STR` é, hoje,
decorativa. Resolução exigida: `Requirement 27.4` diferencia margem de segurança, que deve
ser medida contra o **valor conservador** e não contra o valor base, tornando as duas
condições independentes. Enquanto isso não for implementado, `margem_min` não deve ser
apresentada como critério ativo.

## D.2 Defeitos do motor de decisão

**D.2.1 — Camada de score nunca é avaliada. Severidade: alta.**

`src/radar/engines/decision.py` recebe `opportunity_score` em `DecisionInput` e nunca o
utiliza. Não existe verificação de score mínimo por estratégia, de Investor Fit, de
capital ou de concentração. A camada 8 da precedência canônica (`Requirement 53.1`) nunca
é a camada determinante, e `DecisionLayer.SCORE` nunca aparece em `deciding_layer`.
`MC-110` a `MC-114` não são atendidos. Confirmado por leitura: `analysis_service.analyze()`
fixa `opportunity_score=None`, e `confidence_factor`, `OPPORTUNITY_WEIGHTS` e
`INVESTOR_FIT_WEIGHTS` estão definidos em `domain/parameters.py` sem nenhum chamador.

**D.2.2 — `has_critical_block` fixado em `False`. Severidade: alta.**

`src/radar/orchestration/graph.py`, nó `node_decision`, passa `has_critical_block=False`
literalmente. A camada 0 da precedência nunca dispara pela orquestração, mesmo quando o
`Motor_de_Risco` registra risco de severidade `critico`. Viola `Requirement 34.5` e `P8.6`.

**D.2.3 — Liquidez avaliada com dois limiares inconsistentes. Severidade: média.**

Em `decision.py`, a verificação de liquidez compara com `th.liquidez_min` da estratégia e
apenas acrescenta um motivo, sem eliminar. Já a camada final compara com a constante global
`MIN_LIQUIDITY_FOR_BUY = 60`. Para a estratégia `terreno`, cujo mínimo passa a ser 50, uma
liquidez de 55 passa pela verificação de estratégia e é bloqueada no final pelo limiar
global, contrariando `Requirement 40.7` e o threshold declarado para a estratégia. A
liquidez passa a ser a **camada 7**, própria, com o limiar da estratégia e o piso global
`LIQ-001` resolvidos pela hierarquia de escopo.

**D.2.4 — Rótulo de camada incorreto. Severidade: baixa.**

Em `decision.py`, a ausência de estratégia e a impossibilidade de calcular a economia
retornam `DecisionLayer.STRATEGY` e `DecisionLayer.DATA_CONFIDENCE`, enquanto o comentário
do bloco indica "Camada 4 — Economia". A camada determinante reportada não corresponde à
verificação executada, o que quebra `P11.3` e a auditabilidade exigida por `MC-116`.

**D.2.5 — Defaults inseguros no serviço de análise. Severidade: crítica.**

`src/radar/services/analysis_service.py`, `AnalysisRequest`, define
`legal_status: str = "OK"` e `is_eligible: bool = True`. Uma chamada que não informe o
resultado do gate jurídico produz uma análise com validade jurídica aprovada. Isso viola
diretamente SAFE-003: a ausência de informação é convertida em regularidade. O default
correto é `PENDENTE` para o status jurídico e `False` para a elegibilidade.

**D.2.6 — Heurística de confiança não versionada e sem origem normativa. Severidade: alta.**

`graph.py`, `node_decision`, calcula a confiança como `identidade + 10` quando o gate é
`OK`, `identidade × 0,7` quando `PENDENTE` e `identidade × 0,5` nos demais casos. Esses
coeficientes não constam de nenhum documento de negócio nem de `parameters.py`, não
possuem versão e não são reproduzíveis. A confiança consolidada deveria derivar das
dimensões `CONF-001` a `CONF-005` conforme `Requirement 50`, que não estão implementadas.

**D.2.7 — `legal_status` é string livre e qualquer valor inesperado é tratado como liberado. Severidade: crítica.**

O status jurídico é `str` em `AnalysisContract` (`domain/models.py`), `DecisionInput`
(`engines/decision.py`), `AnalysisRequest` e `DecisionRequest`
(`services/analysis_service.py`, `api/main.py`), comparado por literal em quatro arquivos.
Em `decide()` a camada 0 testa apenas `== "BLOCK"` e `== "PENDENTE"`; **qualquer** outro
valor segue como se fosse `OK`. Isso inclui `"ok"` em minúsculas, `"block"` em minúsculas,
string vazia, `"Bloqueado"` e qualquer erro de digitação em chamada de API. O tipo
`legal_status` existe no banco (`db/schema.sql`) como enum de três valores, mas não há enum
Python correspondente. Combinado com o default `legal_status = "OK"` de `D.2.5`, existem
dois caminhos independentes pelos quais a ausência ou a corrupção da informação jurídica
se converte em liberação — exatamente o que SAFE-001 e SAFE-003 proíbem. A correção é um
enum fechado, validado na fronteira, com falha explícita em valor desconhecido. A
propriedade `P10.16` e o teste `REG-022` cobrem este ponto.

**D.2.8 — semântica de evidência invertida no gate jurídico. Severidade: alta.**

`src/radar/pipeline/legal_gate.py`, em `evaluate_legal_gate`:
`confidence = 95.0 if outcome is CheckOutcome.CONFIRMED else 0.0`. Uma irregularidade
**comprovada** (`IRREGULAR`) — a evidência mais decisiva que o gate produz, pois determina
`BLOCK` — é registrada com confiança `0.0` e estado `OBSERVED`. Um auditor lendo a trilha
concluiria que o bloqueio se apoia em evidência sem confiança. Além disso,
`_OUTCOME_TO_EVIDENCE_STATE[NOT_APPLICABLE] = EvidenceState.UNKNOWN` funde "não se aplica"
com "não sei", o que viola `Requirement 20.4` e impede distinguir cobertura completa de
lacuna. Por fim, `GateCheck.blocks_buy_if_unknown` é sempre `True` e só reflete em
`Pending.blocks_buy`, sem efeito na agregação de status.

## D.3 Lacunas de implementação (capacidades P0 ausentes)

| Capacidade | Situação | Requisito não atendido |
|-----------|----------|------------------------|
| Motor de valuation, seleção e ajuste de comparáveis | ausente | 21, 22, 23, 24 |
| Motor de liquidez e estimativa de prazo de saída | ausente | 40, 41 |
| Cálculo do Opportunity Score | ausente; `analysis_service` grava `opportunity_score=None` | 49 |
| Cálculo do Investor Fit Score | ausente | 51 |
| Motor de ranking e explicação da posição | ausente | 52 |
| Motor de cenários e sensibilidade | ausente (tabela `scenarios` existe, sem produtor) | 32 |
| Preço máximo por estratégia além de revenda | ausente | 28.5 a 28.8 |
| Gestor de portfólio, capital, reserva e concentração | ausente (tabela `investors` existe, sem posições) | 46, 47, 48 |
| Monitor, materialidade e reavaliação | ausente | 57, 58 |
| Gestor de alertas | ausente (tabela `alerts` existe, sem produtor) | 59 |
| Motor de backtest e registro de resultado real | ausente | 60 |
| Execução de regras a partir de `rules` e `rule_versions` | ausente; tabelas criadas e não lidas | 62, 65 |
| Resolução hierárquica de parâmetros | ausente; valores fixos em `domain/parameters.py` | 62.10, 62.11 |
| Registro de exceções e overrides | ausente; sem entidade nem tabela | 63 |
| Trilha de auditoria de mudanças | parcial; `analysis_events` existe, sem registro de ator e valor anterior | 64 |
| Esteira de ingestão documental e RAG | ausente em `src/`; apenas `scripts/db_smoke_vector.py` | 72 |
| Ferramentas MCP | ausentes | 71.10 |
| Persistência da oferta normalizada | ausente; `NormalizedListing` não é gravado | 3.11 |
| Confiança por dimensão | ausente; `analyses.confidence` é escalar único | 50.1 |

## D.4 Divergências entre documentação e esquema de dados

| # | Achado | Artefato | Requisito afetado |
|---|--------|----------|-------------------|
| D.4.1 | `properties` contém apenas `id` e `created_at`. Não há perfil consolidado do imóvel (tipo, área com tipo, quartos, vagas, endereço, bairro, município, UF, CEP, condomínio, bloco, unidade). | `db/schema.sql` | 8.1, 10.1 |
| D.4.2 | Não existem os campos `condominio`, `torre`, `bloco`, `unidade` e `vaga` em `NormalizedListing`, embora a chave conceitual de identidade os exija. | `src/radar/capture/schemas.py` | 8.1, 8.2 |
| D.4.3 | `area_m2` agrega "área privativa" e "área total" no mesmo campo, perdendo o tipo de área. A comparação de preço por metro quadrado fica sujeita a erro sistemático. | `src/radar/capture/caixa.py`, `FIELD_ALIASES` | 3.5, 21.11, 21.12 |
| D.4.4 | `leiloes_negativos_averbados` é booleano, incapaz de representar o estado `em_tratamento` exigido pelo Golden Case Reserva dos Pinhais e por `RULE-JUR-012`. | `src/radar/capture/schemas.py` | 13.13, REG-003 |
| D.4.5 | `missing_fields()` considera oito campos e omite `tipo_imovel`, `bairro`, `quartos` e `vagas`, que são obrigatórios nos gates `G1` e no dicionário mínimo. | `src/radar/capture/schemas.py` | 4.2 |
| D.4.6 | Não há mapeamento do status da oferta para estados padronizados; apenas `situacao_texto` livre. | `src/radar/capture/caixa.py` | 3.7 |
| D.4.7 | Não existe entidade nem coluna para o ciclo de vida da captura (`Captured` a `Error`) nem para o ciclo de vida do imóvel (`Candidate` a `Closed`). | `db/schema.sql` | Jornada Macro |
| D.4.8 | `comparables` não possui classe de qualidade, ajustes aplicados, tipo de área nem indicação de anúncio versus transação. | `db/schema.sql` | 21.2, 21.3, 21.5, 21.10 |
| D.4.9 | `risks` não possui probabilidade, impacto, exposição, mitigação nem prazo. A matriz de severidade não é reconstituível. | `db/schema.sql` | 34.2, 34.3, 34.10 |
| D.4.10 | `pendings` possui apenas `item`, `reason` e `blocks_buy`. Faltam prioridade, responsável, prazo, condição de liberação e evidência de encerramento. | `db/schema.sql` | 37.1, 37.2 |
| D.4.11 | `analyses.rule_version` é uma única string. Não há vínculo entre a decisão e o conjunto de `rule_versions` efetivamente aplicadas. | `db/schema.sql` | 61.4, 64.1 |
| D.4.12 | Os thresholds por estratégia existem em dois lugares independentes: seed da tabela `strategies` e constante `STRATEGY_THRESHOLDS` em `domain/parameters.py`. Nada garante a convergência entre os dois. | `db/schema.sql`, `src/radar/domain/parameters.py` | 62.10 |
| D.4.13 | Não há registro de divergências documentais (fonte A, informação A, fonte B, informação B, impacto), exigido pelo Anexo C.5 e pela divergência real de data do Golden Case item 227. | `db/schema.sql` | 6.1, 15.7 |
| D.4.14 | Não há entidade para posições do portfólio do investidor, o que torna as regras de concentração incalculáveis. | `db/schema.sql` | 47.5 |
| D.4.15 | Não há entidade para resultado real pós-aquisição, necessária ao backtest. | `db/schema.sql` | 60.1 |

## D.5 Gate jurídico incompleto

`src/radar/pipeline/legal_gate.py` implementa sete verificações (`GATE-JUR-001` a
`GATE-JUR-007`). `Requirement 12.9` exige **19**: treze `RULE-JUR-001` a `RULE-JUR-013`,
quatro `RULE-ED-001` a `RULE-ED-004`, e duas `RULE-ID-001` e `RULE-ID-002`. As verificações
de ocupação e de locação ficam na camada 6 de risco e não integram o gate (`R12.10`).
Verificações ausentes, todas com efeito potencial de `BLOCK` ou de hard stop:

| Regra ausente | Verificação | Consequência |
|---------------|-------------|--------------|
| `RULE-ED-002` | Responsabilidade por evicção (E01 a E09) | Hard stop de lance do Método Jabes não implementado |
| `RULE-JUR-008` | Penhora e indisponibilidade de direitos | Constrição impeditiva não detectada |
| `RULE-JUR-009` | Garantia de dívida de terceiro | Sinal de nulidade não detectado |
| `RULE-JUR-010` | Percentual de quitação acima de 80% | Sinal de investigação não registrado |
| `RULE-JUR-011` | Segundo leilão abaixo de 50% da avaliação | Alerta jurídico não emitido |
| `RULE-JUR-012` | Averbação de leilões negativos | Pendência registral e custo não modelados |
| `RULE-ED-003` | Responsabilidade por IPTU e condomínio | Contingência obrigatória não criada |
| `RULE-ED-004` | Vaga de garagem com matrícula autônoma | Risco registral não detectado |

Ausentes também, porém na **camada 6 de risco** e não no gate: `RULE-LOC-001` e
`RULE-LOC-002` (locação e cláusula de vigência, com efeito sobre posse e prazo) e
`RULE-OCC-001` e `RULE-OCC-002` (situação de ocupação e cessão de posição contratual, com
efeito sobre custo, prazo e, nos casos de `R18.2.1` e `R18.2.2`, `BLOCK` na camada 0).

Além disso, `LegalGateResult.blocks_buy` retorna verdadeiro para `BLOCK` e para
`PENDENTE`, o que é correto, porém a orquestração usa apenas `legal_status == "BLOCK"`
para o curto-circuito, de modo que `PENDENTE` prossegue pelo pipeline sem que o efeito
de `blocks_buy` seja consumido em nenhum ponto.

## D.6 Inconsistências internas entre spec e código

| # | Achado |
|---|--------|
| D.6.1 | `IdentityResult.is_reliable` exige nível maior ou igual a `I3`, mas a orquestração usa `identity.level >= 2` para elegibilidade e `< 2` para curto-circuito. A propriedade `is_reliable` não é consumida em nenhum ponto do fluxo: é código morto com um limiar divergente do especificado. |
| D.6.2 | A spec absorvida definia que matrícula com contexto registral resulta em `I4` e matrícula sem contexto resulta em no máximo `I3`, enquanto a fonte de captura define `I3` como "confirmado por identificador forte" e `I4` como "documental". A implementação segue a spec absorvida. `Requirement 7` consolida a definição, mantém a compatibilidade com a implementação e, por `D35`, amplia `I4` para qualquer documentação registral e acrescenta o requisito de unidade de `Requirement 8`. |
| D.6.3 | A fase `DEDUPLICATED` é declarada na máquina de estados e não existe nó de deduplicação no grafo de `orchestration/graph.py`: a fase nunca é atingida em execução. O mesmo vale agora para `QUALIFIED` e `CONSOLIDATED`, acrescentadas por `D47`. |
| D.6.4 | A precedência de decisão aparecia com cinco contagens divergentes nas fontes (8, 10, 10 com liquidez antes de risco, 8 e 12). Resolvido em `D1`: **onze camadas, numeradas 0 a 10**, conforme o adendo de versão do documento de decisão. O enum `DecisionLayer` de `domain/enums.py` tem nove valores e **deve ser ampliado** para onze, acrescentando camadas próprias de risco, liquidez, capital e concentração, e ranking. Além do enum, faltam no código os conteúdos das camadas 0, 2, 6, 7, 8, 9 e 10 (ver D.2.1 e D.2.2). |
| D.6.5 | O enum `strategy` do banco e `Strategy` do domínio possuem cinco valores, enquanto três fontes tratavam `apartamento`, `casa_sobrado` e `um_dormitorio` também como estratégias. `Requirement 44.2` classifica-os como perfis de ativo e exige um novo campo de perfil; por `D42`, o enum de estratégia passa a **seis** valores com a inclusão de `customizada`, e o enum de perfil de ativo passa a nove valores. |
| D.6.6 | `README.md` declara 18 testes e o `tasks.md` da spec parcial repete o número; a execução real de `python -m pytest -q` retorna **22 passaram** em 5 arquivos (`test_analysis_service.py`, `test_api.py`, `test_calculation.py`, `test_capture_caixa.py`, `test_decision.py`). Não existem testes para `pipeline/legal_gate.py`, `pipeline/identity.py`, `orchestration/graph.py`, `db/*` nem `domain/parameters.py` — justamente os módulos onde estão `D.1.3` a `D.1.5` e `D.2.8`. A suíte verde protege as partes já corretas e não alcança nenhum dos seis defeitos numéricos verificados. |
| D.6.7 | `tasks.md` da spec parcial afirma que o código "nunca foi executado" e que é preciso "garantir que importa sem exigir LangGraph". Verificado: `langgraph` está instalado, `build_graph()` compila e retorna `CompiledStateGraph`, e a suíte passa. O `tasks.md` precisa ser reescrito a partir do estado real; o ramo `except ImportError` de `run_analysis` é hoje inalcançável e portanto nunca exercitado. |
| D.6.8 | `mypy` está configurado com `strict = true` em `pyproject.toml`, porém nem `mypy` nem `ruff` estão instalados no ambiente (`python -m ruff check .` retorna "No module named ruff"). Nenhuma das duas verificações jamais rodou, o que explica a convivência de `# type: ignore` em `decision.py`, `graph.py` e `db/models.py` com a exigência de tipagem estrita. |
| D.6.9 | Código definido e sem nenhum chamador: `parameters.confidence_factor`, `OPPORTUNITY_WEIGHTS`, `INVESTOR_FIT_WEIGHTS`, `EXCEPTIONAL_DISCOUNT`, `TICKET_MIN`, `TICKET_MAX`, `enums.ConfidenceBand`, `identity.EVIDENCE_WEIGHT`, `identity.is_same_property`, `IdentityResult.is_reliable`, `LegalGateResult.blocks_buy`, `calculation.market_discount`, `calculation.gross_annual_yield`. São os parâmetros e as funções que sustentariam as camadas 2, 5 e 6 da precedência: estão escritos e desligados. |
| D.6.10 | `langchain` e `langchain-openai` são dependências declaradas em `pyproject.toml` e não são importadas em nenhum arquivo de `src/`. `config.Settings.llm_provider`, `llm_model` e `openai_api_key` não são lidos por nenhum módulo. A camada de IA da arquitetura (§7, §8, §12) está declarada e ausente. |
| D.6.11 | `node_normalize` em `orchestration/graph.py` chama `normalize_caixa` incondicionalmente, ignorando `RawCapture.source_type`. Qualquer fonte é normalizada como se fosse CAIXA, o que contraria `Requirement 1.1` e a premissa multi-fonte do produto. |

## D.7 Riscos técnicos

| # | Risco | Impacto | Mitigação recomendada |
|---|-------|---------|-----------------------|
| D.7.1 | Duas fontes de verdade para parâmetros: constantes Python e seed do banco. | Divergência silenciosa entre o que o motor usa e o que o banco declara; análises não reproduzíveis. | Eleger o banco como fonte, carregar via `Gestor_de_Parametros` com versão e vigência, e manter as constantes apenas como valores de arranque. |
| D.7.2 | Parâmetros embutidos no código impedem o versionamento exigido por `RULE-GOV-001`. | Nenhuma análise é reproduzível após alteração de parâmetro. | Implementar resolução hierárquica com `effective_from` e `effective_to`. |
| D.7.3 | Ausência de `hypothesis` ou biblioteca equivalente em `pyproject.toml`. | As propriedades deste documento não podem ser executadas. | Adicionar a dependência ao grupo `dev` em versão fixada. |
| D.7.4 | Índice `ivfflat` criado com `lists = 100` sobre tabela vazia. | Recall degradado da busca semântica enquanto o volume for baixo, e parâmetro inadequado quando o volume crescer. | Recriar o índice após a carga inicial, com `lists` proporcional ao volume. |
| D.7.5 | `CREATE EXTENSION vector` exige privilégio elevado. | Falha de provisionamento em ambiente gerenciado. | Já há convergência tardia em `scripts/db_setup.py`; manter o núcleo transacional independente de pgvector. |
| D.7.6 | `AnalysisContract` declara `model_config = {"frozen": False}` com o comentário de que se torna imutável após a persistência, sem mecanismo que garanta isso. | Snapshot pode ser alterado em memória após a persistência. | Congelar o contrato na fronteira de persistência ou usar um tipo distinto para o snapshot. |
| D.7.7 | Especificações normativas vivendo fora desta spec, duplicando a fonte de verdade. | Divergência silenciosa entre artefatos normativos. | **Resolvido por `D51`**: este documento é a fonte única; os demais artefatos normativos foram absorvidos e deixam de ser referenciados. |
| D.7.8 | `api/main.py` expõe `/analysis/run` sem autenticação nem autorização. | Endpoint de análise acessível por qualquer cliente que alcance a porta. Em ambiente local o impacto é limitado; em rede compartilhada, não. | Definir autenticação antes de qualquer exposição além de `localhost`. |
| D.7.9 | A orquestração cai silenciosamente para execução sequencial quando o LangGraph não está disponível (`except ImportError`). | Duas implementações do fluxo podem divergir sem sinalização. | Registrar o modo de execução na trilha de auditoria e cobrir a equivalência pela propriedade `P12.5`. |
| D.7.10 | Não há tratamento de frescor de dados em nenhum módulo. | Decisões tomadas com preço, edital ou matrícula vencidos. | Implementar `FRESH` e `CONF-008` no `Monitor`. |

## D.8 Relação com a spec `pipeline-captura-identidade-gate-juridico`

A spec `pipeline-captura-identidade-gate-juridico` é **integralmente absorvida** por este
documento e **não é mais fonte de trabalho** (`D55`). Este documento é um superconjunto:
mantém todos os nove requisitos daquela spec e os amplia. A lista abaixo enumera os pontos em
que este documento a **altera**; onde não há alteração, a formulação é mantida.

**Compatível e mantido:** preservação da captura, normalização sem invenção de dados,
níveis de identidade I0 a I4, deduplicação por força de evidência, gate jurídico como
camada P0, ocupação como risco de posse, evidência com proveniência, orquestração com
curto-circuito e persistência como snapshot imutável.

**Divergências apontadas, a serem conciliadas:**

| # | Divergência | Resolução adotada aqui |
|---|-------------|------------------------|
| 1 | A spec parcial não exige o tipo de área na normalização. | `Requirement 3.5` passa a exigir. |
| 2 | A spec parcial não exige unidade, bloco, torre e condomínio na chave de identidade. | `Requirement 8` passa a exigir. |
| 3 | A spec parcial define sete verificações no gate jurídico ("no mínimo"). | `Requirement 12.9` fixa o catálogo em **19 verificações**: treze `RULE-JUR-*`, quatro `RULE-ED-*` e duas `RULE-ID-*`. |
| 4 | A spec parcial não trata o estado `em_tratamento` da averbação de leilões negativos. | `Requirement 13.13` define os quatro estados. |
| 5 | A spec parcial declara fora de escopo a consulta a cartório e tribunais. | Este documento mantém a coleta fora de escopo e especifica o contrato de entrada dessas verificações. |
| 6 | A spec parcial não menciona a garantia contra evicção. | `Requirement 15.8` a `15.9.2` e o Anexo C.2 passam a exigir, com a distinção entre ausência comprovada e não verificação. |
| 7 | A spec parcial trata ocupação em cinco estados e nunca bloqueante. | `Requirement 18.1` define sete estados e `18.2.1` e `18.2.2` definem os dois casos de `BLOCK`. |
| 8 | A spec parcial não define a camada de decisão. | `Requirement 53.1` define onze camadas e a posição do gate jurídico como camada 1, subordinada aos bloqueios críticos da camada 0. |
| 9 | A spec parcial não define identificadores de checklist. | Os Anexos A, B e C passam a ter `MC-*`, `B-01` a `B-27` e `C-01` a `C-71`. |
| 10 | A spec parcial não exige `CONSOLIDATED` nem `QUALIFIED` no pipeline. | `Requirement 70.1` e a tabela de fases passam a exigir as duas. |

## D.9 Integridade do banco de dados

Achados obtidos por leitura de `db/schema.sql` e `src/radar/db/`. **Esta lista é normativa**:
o modelo físico deve declarar cada item abaixo. Por `D51`, a exigência de integridade vive
aqui e não em artefato externo.

| # | Achado | Consequência | Correção exigida |
|---|--------|--------------|------------------|
| D.9.1 | `property_identifiers` tem `UNIQUE (property_id, id_type, value)`, o que permite **a mesma matrícula vinculada a dois `properties` distintos**. | Contraria diretamente `Requirement 9.2`: matrícula é evidência decisiva de identidade. Dois imóveis com a mesma matrícula é o falso negativo de deduplicação, e o falso positivo inverso fica igualmente possível. | Índice único parcial sobre `(id_type, value)` para `id_type = 'matricula'`, e coluna de origem (`source_id` ou `document_id`) no identificador. |
| D.9.2 | Nenhum código insere em `captures`, apesar da tabela existir com `UNIQUE (source_id, hash)`. `RawCapture.fingerprint` é calculado e nunca persistido. | A idempotência de captura existe no schema e não existe em execução. Reprocessar o mesmo payload cria nova análise sem deduplicar. Viola `Requirement 2.4`. | Implementar `save_capture` idempotente por `(source_id, fingerprint)`. |
| D.9.3 | `documents` tem `UNIQUE (hash)` global. | O mesmo edital coletado por duas fontes distintas colide, e a segunda coleta falha em vez de registrar a segunda proveniência. | `UNIQUE (source_id, hash)`, preservando a origem de cada cópia. |
| D.9.4 | `opportunities` não tem restrição de unicidade sobre `(source_id, external_ref)`. | Nada impede duplicar a mesma oferta do mesmo edital, o que distorce ranking e estatísticas. | `UNIQUE (source_id, external_ref)` quando `external_ref` não é nulo. |
| D.9.5 | Apenas `evidences` e `analysis_events` possuem índice em `analysis_id`. `risks`, `pendings`, `facts`, `comparables`, `valuations` e `scenarios` não possuem. | Varredura completa ao montar a ficha da oportunidade. | Índice em `analysis_id` em todas as tabelas filhas de `analyses`. |
| D.9.6 | `analyses.liquidity_score` é `SMALLINT` **sem** `CHECK (… BETWEEN 0 AND 100)`, ao contrário de `identity_confidence`, `opportunity_score`, `investor_fit` e `confidence`. `analyses.version` não tem `CHECK (version > 0)`. | Escala violável sem erro. | Acrescentar os `CHECK` correspondentes. |
| D.9.7 | `db/repository.py::save_analysis` converte os escores com `int(...)`, truncando. | Uma confiança de 74,6 é gravada como 74 e cruza o limiar `GLB-003` de 75. O snapshot deixa de reproduzir a decisão tomada em memória, violando `Requirement 61.2`. | Persistir `NUMERIC(5,2)` ou arredondar de forma declarada e documentada no parâmetro. |
| D.9.8 | A imutabilidade do snapshot é apenas documental. Não há trigger, regra nem revogação de privilégio impedindo `UPDATE` ou `DELETE` em `analyses`, `evidences` e `captures`; e o encadeamento `ON DELETE CASCADE` de `properties → opportunities → analyses` permite apagar todo o histórico com um único `DELETE`. `AnalysisContract.model_config` declara `{"frozen": False}` com comentário afirmando o contrário. | `Requirement 61.1` e `Requirement 64.4` não são executáveis. | Trigger de bloqueio de `UPDATE`/`DELETE` nas tabelas de snapshot, e restrição do cascade a um procedimento explícito de limpeza de dados de teste. |
| D.9.9 | O ORM em `src/radar/db/models.py` mapeia 10 das 24 tabelas. Sem mapeamento: `captures`, `facts`, `valuations`, `scenarios`, `comparables`, `risks`, `pendings`, `analysis_events`, `rules`, `rule_versions`, `parameters`, `strategies`, `investors`, `alerts`. `Analysis` não tem relação para `risks` nem `pendings`. | As 14 tabelas restantes são schema morto. A trilha de evidência é modelada e nunca gravada: `analysis_service.analyze()` monta o `AnalysisContract` sem `legal_evidence`, `risks` e `pending`, então `analyze_and_persist` grava análises com zero evidências. | Completar o ORM e ligar a produção do gate jurídico à persistência. |
| D.9.10 | A última linha de `db/models.py` é `CheckConstraint("confidence BETWEEN 0 AND 100", name="ck_analysis_confidence")` no escopo do módulo, fora de qualquer `__table_args__`. | Não gera DDL nem validação. Dá falsa aparência de paridade com o schema. | Mover para `Analysis.__table_args__` ou remover. |
| D.9.11 | Não existem migrações. O único caminho é `db/schema.sql` aplicado por `scripts/db_setup.py`, que divide comandos por `;` e tolera erros por lista de SQLSTATE. O `INSERT INTO strategies` final **não é idempotente**: a segunda execução gera `23505 unique_violation`, que não está na lista tolerada, e o script termina com código 2. `--drop` executa `DROP SCHEMA … CASCADE` sem confirmação. | O setup só funciona do zero. Evolução de schema sem histórico. | Adotar ferramenta de migração, tornar o seed idempotente (`ON CONFLICT DO UPDATE`) e exigir confirmação no `--drop`. |

## D.10 Configuração, segredos e operação

| # | Achado | Impacto | Correção exigida |
|---|--------|---------|------------------|
| D.10.1 | `config.Settings.openai_api_key` é `str` e não `SecretStr`. | A chave aparece em `repr(settings)`, em log de exceção e em despejo de estado. | Tipo secreto com redação automática. |
| D.10.2 | `database_url` traz credencial default embutida (`radar:radar`) e `docker-compose.yml` publica a porta 5432 no host com `POSTGRES_PASSWORD: radar` em claro. | Banco alcançável da rede local com senha conhecida. | Não publicar a porta por default; senha por variável de ambiente sem valor default. |
| D.10.3 | Quando `RADAR_DB_HOST_ADDR` está definido, a conexão usa `sslmode=require`, que criptografa **sem validar certificado nem nome do servidor** — o próprio `scripts/db_check.py` documenta isso. | Tráfego cifrado, porém sujeito a interposição. Inaceitável contra banco gerenciado em produção. | `sslmode=verify-full` com CA explícita antes de qualquer uso fora de `localhost`. |
| D.10.4 | `scripts/db_setup.py` e `scripts/db_check.py` reimplementam um leitor de `.env` próprio (`load_env`) que **ignora variáveis de ambiente reais**. | Se a credencial vier do ambiente e não do arquivo, os scripts falham com "RADAR_DATABASE_URL não definida". Impede uso em integração contínua e em gerenciador de segredos. | Usar `pydantic-settings` como única via de configuração. |
| D.10.5 | `db/session.py` cria `create_engine` em tempo de import. | Qualquer import de `radar.db.*` passa a exigir configuração válida, inclusive em teste unitário. Sem `pool_size`, `pool_timeout` nem política de retry. | Fábrica preguiçosa de engine e sessão. |
| D.10.6 | `api/main.py` registra `/health`, `/analysis/decision` e `/analysis/run` sem autenticação, CORS nem limite de taxa. | Já registrado em `D.7.8`. Reforço: o endpoint executa cálculo e persistência, não é somente leitura. | Autenticação antes de qualquer exposição além de `localhost`. |
| D.10.7 | `AnalyzeRequest.market_value` é `float` sem `gt=0`. `POST /analysis/run` com `market_value = 0` atinge `calculation.net_discount`, que levanta `ValueError`, e não há manipulador de exceção em `main.py`: resposta 500. | Entrada válida pelo schema derruba a requisição. | Validação no schema e manipulador de erro que retorne 422 com a causa. |
| D.10.8 | `AnalyzeRequest` omite `tributos`, `custo_juridico_potencial`, `prob_juridica` e `carrying`, que existem em `AnalysisRequest` e na Canônica §9. | Pela API esses custos entram como zero, o que é precisamente a conversão de desconhecido em zero proibida por SAFE-003 e por `Requirement 26.7`. | Expor todos os componentes do TCO e marcar ausência como desconhecido, não como zero. |

## D.11 Fonte única normativa

**Declaração** `[CANÔNICO]` (`D51`). Este documento é o único artefato normativo do produto.
A documentação de negócio de origem, o material extraído dela e as especificações canônicas
internas anteriores foram auditados, consolidados e absorvidos, e **deixam de ser
referenciados**. Todo valor, regra, item de checklist, fórmula e caso de prova está escrito
aqui. Nenhum requisito deste documento depende de arquivo externo.

Regras decorrentes:

| Regra | Efeito |
|-------|--------|
| Nenhum requisito novo entra no produto sem passar por este documento | Impede que regra saia de material de origem direto para código. |
| Nenhuma justificativa é feita por indireção | Onde havia "conforme a especificação canônica §N", a justificativa está reescrita no próprio texto. |
| A seção **Decisões de Consolidação** é a memória de auditoria | `D1` a `D55` registram conflito, lados, decisão e motivo de cada resolução. |
| O modelo físico de dados é normatizado por `D.9` | A lista de integridade de `D.9` é exigência desta spec, não de artefato externo. |
| O material de origem é arquivo histórico | Preservado fora do fluxo de trabalho, sem valor normativo. |

A pendência anterior `PEND-FONTE-UNICA`, que previa consolidar artefatos, é substituída por
esta declaração e considerada encerrada.

**Situação dos artefatos**

| Artefato | Situação | Observação |
|----------|----------|------------|
| Este `requirements.md` | **Fonte única normativa** | Versionado e commitado. Nenhum requisito novo entra no produto sem passar por aqui. |
| Documentação de negócio de origem e material extraído | **Absorvidos** | Sem valor normativo. Preservados apenas como arquivo histórico, fora do fluxo de trabalho. |
| Especificações canônicas internas anteriores | **Absorvidas** | Conteúdo replicado e reconciliado aqui: a precedência de decisão, a máquina de estados e as exigências de integridade do modelo físico. Deixam de ser citadas por qualquer requisito. |
| Exigências de integridade do modelo físico | **Internalizadas em `D.9`** | `D.9` é a lista normativa. O modelo físico deve declarar cada item. |
| `.kiro/specs/pipeline-captura-identidade-gate-juridico/` | **Absorvida** | Ver `D.8` e `D55`: integralmente coberta por este documento; deixa de ser fonte de trabalho. |
| Docstrings e cabeçalhos de código que citam especificações externas | **A reescrever** | Devem passar a citar requisitos deste documento pelo número. |

**Fechamento do ciclo parâmetro ↔ código ↔ banco.** As constantes de threshold por
estratégia no código, o seed da tabela de estratégias no banco e a tabela `STR` deste
documento repetem os mesmos registros sem nada garantindo convergência — e `margem_min`,
`liquidez_min`, `ticket_max` e `desconto_liquido_min` acabaram de mudar aqui.
`Requirement 62.10` exige um único ponto de verdade, com o seed gerado a partir dele e um
teste comparando as três representações. A tabela `STR` desta spec é esse ponto de verdade.

---

# Decisões de Consolidação

Esta seção é a **memória de auditoria** da consolidação. Cada decisão registra o conflito
encontrado, os lados em disputa, a decisão adotada e o motivo. Depois que o material de
origem sai do fluxo de trabalho, é aqui que se entende por que cada valor é o que é.

Os princípios que governaram as decisões são `P-A` a `P-E`, declarados na Introdução.

## D1 — Precedência de decisão: onze camadas

**Conflito.** O número e a ordem das camadas de decisão divergia em **cinco** formulações.

| Fonte | Camadas | Particularidade |
|-------|---------|-----------------|
| Documento de decisão, corpo v1.0 §3 | 8 | Sem gate jurídico; risco diluído |
| **Adendo v1.1 do mesmo documento** | **11** | Bloqueio → validade jurídica → elegibilidade → dados → economia → estratégia → risco → liquidez → score → capital → ranking |
| Documento de ranking §3 | 10 | Sem camada de validade jurídica própria |
| Documento de estratégias §5 | 10 | Liquidez antes de risco |
| Matriz canônica §8 | 8 | Numerada P0 a P7 |
| Base de conhecimento §04 | 12 | Desdobra a ação final |

**Decisão.** Onze camadas, numeradas 0 a 10, conforme o adendo v1.1: `0` bloqueios críticos;
`1` validade jurídica; `2` elegibilidade; `3` dados e confiança; `4` economia, com a robustez
de cenário como sub-verificação; `5` estratégia; `6` risco; `7` liquidez; `8` score;
`9` capital e concentração; `10` ranking. A decisão final é a **saída**, não uma camada.
Risco, liquidez, capital e ranking voltam a ser camadas próprias. A camada determinante
reportada é sempre a de menor índice entre as eliminatórias. Atualizados `R53` integralmente,
o enum `DecisionLayer` citado em `D.6.4` e toda referência a "nove camadas".

**Motivo.** `P-B`: o adendo prevalece sobre o corpo. Além disso, tratar risco, liquidez e
capital como sub-verificações de outras camadas tornava a camada determinante ambígua — o
mesmo caso podia ser reportado como reprovado por "estratégia" ou por "score" conforme o
caminho de código, o que quebra a auditabilidade exigida por `MC-116`.

## D2 — Ocupação pode bloquear

**Conflito.** A spec tratava ocupação como risco alto que nunca bloqueia; a fonte de risco
prevê `BLOCK` para ocupação com impacto crítico sem estratégia de desocupação e classifica
posse litigiosa como alto ou crítico conforme evidências.

**Lados.** "Ocupação nunca é nulidade" (correto) versus "ocupação nunca bloqueia" (incorreto).
São afirmações diferentes que a spec havia fundido.

**Decisão.** Sete estados de ocupação, com o acréscimo de `posse_litigiosa` e
`livre_nao_confirmado`. Ocupação com impacto crítico e sem estratégia de desocupação, ou
posse litigiosa com evidência de litígio, resulta em severidade `critico` e `BLOCK` na
camada 0 (`RULE-RSK-005`). Ocupação desconhecida resulta em `PENDENTE` de prioridade `alta`,
não `critica`, mais contingência, permitindo a continuidade da análise. Corrigidos `R18`,
o efeito de `MC-044`, o efeito de `MC-045` e o parâmetro `RISK-002`.

**Motivo.** `P-A` para o bloqueio: um imóvel que não pode ser desocupado não é oportunidade,
e a ausência de estratégia não deve ser compensada por desconto. `R18.3` para a prioridade:
a própria spec exige que a análise econômica continue, o que é incompatível com pendência
crítica.

## D3 — Regra eliminatória do investidor produz BLOCK

**Conflito.** A fonte de risco classifica a regra eliminatória do investidor como `BLOCK`; a
matriz canônica a mapeia para `DO_NOT_BUY`.

**Decisão.** `BLOCK`. Corrigidos `R39.4.2` e o efeito de `MC-107`.

**Motivo.** `P-A` com consequência operacional: `BLOCK` sai do ranking e `DO_NOT_BUY`
permanece nele. Uma oportunidade que o investidor declarou inaceitável não deve continuar
competindo por capital e atenção.

## D4 — Evicção: dois casos distintos

**Conflito.** A spec tratava "garantia de evicção não confirmada" como um caso único com
resultado "no máximo `BUY_IF`".

**Decisão.** Dois casos. Se o edital foi obtido e comprovadamente **não contém** cláusula de
garantia contra evicção — evidência de ausência — o resultado é `BLOCK`. Se o edital não foi
obtido ou a cláusula não foi verificada — ausência de evidência — o resultado é `PENDENTE`
jurídico que impede `BUY`. Nos dois casos o lance não é liberado. Corrigidos `R15.9` a
`R15.9.2`, o Anexo C.2 e `B-14`; eliminado o "no máximo `BUY_IF`".

**Motivo.** `P-E`. O "no máximo `BUY_IF`" convertia a ausência comprovada de garantia em
decisão condicional favorável, que é exatamente o resultado que a garantia existe para
evitar.

## D5 — Hard stop de parecer jurídico não é configurável

**Conflito.** `HS-09` era condicionado a `INV-018 = nao`, isto é, bastava configurar o
parâmetro para desligar o hard stop.

**Decisão.** Removida a condicionante. O hard stop dispara sempre que a aceitação do risco
depender de parecer jurídico e o parecer não estiver registrado como evidência. `INV-018`
passa a significar "o investidor exige parecer jurídico registrado para aceitar risco
jurídico relevante", com default `sim`, e não condiciona o hard stop. Corrigidos `HS-09`,
`R39.4` e `R39.4.1`.

**Motivo.** `P-A`. Uma proteção que pode ser desligada por configuração não é proteção. O
hard stop de origem é pessoal e absoluto: "necessidade de advogado para aceitar o risco ⇒
reprovar".

## D6 — Reforma estrutural desconhecida gera pendência

**Conflito.** A spec tratava condição estrutural desconhecida apenas como contingência de
custo; a fonte de risco a classifica como `PENDENTE` (`RULE-RSK-008`).

**Decisão.** `PENDENTE` de prioridade `alta` **mais** contingência. Corrigidos `MC-081` e
`R38.5.1`.

**Motivo.** `P-A`. Contingência sozinha permite que a análise avance até `BUY` com um risco
estrutural não investigado; a pendência força a investigação.

## D7 — Liquidez mínima

**Conflito.** Cinco valores: piso global 60 na spec anterior; `LIQ-001` igual a 70 no
catálogo de parâmetros; 70 para renda, 75 para revenda e 70 para MCMV nos exemplos de
configuração.

**Decisão.** `LIQ-001` = 70 e `GLB-006` = 70. Tabela `STR.liquidez_min`: revenda 75, renda 70,
mcmv 70, valorizacao 60, terreno 50. Os dois últimos são `[DEFAULT-DERIVADO]`: a hierarquia
relativa anterior era `valorizacao = renda − 10` e `terreno = renda − 20`, que aplicada aos
três valores documentados produz 60 e 50. **Revogada** a resolução anterior `CONF-LIQ`, que
fixava o piso em 60 contra os documentos.

**Motivo.** `P-D`: a numeração e os valores do catálogo de parâmetros são canônicos. A
resolução anterior escolhia o valor mais permissivo sem fonte que o sustentasse.

## D8 — Sete faixas de liquidez

**Conflito.** Quatro faixas na spec anterior, com limiar de exceção formal em 40; sete faixas
por dezena na fonte de liquidez.

**Decisão.** Sete faixas, total e sem lacuna: 90–100 `muito_alta`; 80–89 `alta`; 70–79 `boa`;
60–69 `media`; 50–59 `baixa`; 40–49 `muito_baixa`; 0–39 `iliquida`. Score abaixo de **50**
resulta em `MONITOR` ou `DO_NOT_BUY` e exige exceção formal para qualquer compra. Atualizados
`R40.2`, `R40.8`, o enum `LiquidityCategory` e a propriedade `P9.1`.

**Motivo.** `P-D` e `P-A`. Com quatro faixas, a faixa `baixa` cobria 40 a 59 e o limiar de
exceção em 40 deixava 40–49 passar sem exceção, embora essa seja a segunda pior faixa da
escala de origem.

## D9 — Margem mínima

**Conflito.** Quatro valores: 15% no catálogo de parâmetros e nos exemplos de renda e MCMV;
18% na fonte de governança; 20% no manual de regras e no documento de negócio; 25% na fonte
de due diligence.

**Decisão.** `GLB-002` = 0,15. `STR.margem_min`: revenda 0,20, renda 0,15, valorizacao 0,15,
mcmv 0,15, terreno 0,20. Os valores 20% e 25% permanecem disponíveis como defaults de perfil
mais restritivos, admitidos pela hierarquia de escopo.

**Motivo.** `P-D` para o piso global. `P-C` para a coexistência: um perfil mais exigente é
escopo mais específico e prevalece; o piso global não pode ser mais permissivo que o valor
documentado.

## D10 — Desconto líquido mínimo

**Conflito.** Cinco valores divergentes: `PRI-005` igual a 10% no catálogo; 15% no desconto
sobre mercado; 20% no exemplo de revenda; 25% no manual de regras; 30% na fonte de due
diligence. A resolução anterior omitia os 30%.

**Decisão.** `PRI-005` = 0,15 como piso global. `STR.desconto_liquido_min`: revenda 0,25,
mcmv 0,20, terreno 0,20, renda 0,15, valorizacao 0,15.

**Motivo.** `P-A`. O piso de 10% era o valor mais permissivo do conjunto e nenhuma estratégia
o usava; elevá-lo a 15% alinha o piso ao menor valor efetivamente aplicado. Os 25% e 30%
permanecem como defaults de perfil.

## D11 — Matriz score × confiança completa

**Conflito.** A spec cobria nove das quinze células e a fonte de decisão era internamente
contraditória sobre a faixa 50–59: uma seção dizia "somente se a estratégia aceitar" e outra
dizia `DO NOT BUY`.

**Decisão.** As 15 células publicadas em `R55`, usando as faixas de `CONF-007`. A célula
60–69 com confiança baixa é `DO_NOT_BUY`. Para a faixa 50–59, a coluna "ação típica" de
`SCORE-003` passa a "baixa prioridade; só avança com exceção autorizada" e `R55.7` permanece
emitindo `DO_NOT_BUY` para score abaixo de 60.

**Motivo.** A contradição da fonte se resolve pela aritmética: o score mínimo por estratégia
vai de 65 a 75, logo **nenhuma** estratégia aceita 50–59 pela regra normal. As duas
afirmações da fonte descrevem a mesma coisa: reprovado, salvo exceção.

## D12 — Escala nomeada de confiança

**Conflito.** Três fontes usam seis níveis nomeados; a spec usava faixas numéricas e uma
faixa `insuficiente` que não existe em nenhuma fonte.

**Decisão.** Os seis níveis acrescentados em `CONF-010`, com as faixas e fatores de
`CONF-007`: `muito_alta` 90–100 fator 1,00; `alta` 75–89 fator 0,95; `media` 60–74 fator
0,88; `baixa` 40–59 fator 0,75; `muito_baixa` 0–39 fator 0,60; `inconclusiva` quando dimensão
crítica é ausente ou conflitante. Confiança `inconclusiva` resulta em `PENDENTE` ou `BLOCK`,
não apenas em abster-se de recomendar. Corrigidos `R50.5`, `R55.9` e toda referência a
"faixa insuficiente", termo eliminado.

**Motivo.** `P-A`. "Abster-se de recomendar" deixa a oportunidade em estado indefinido; a
fonte exige resultado explícito. O rótulo `insuficiente` era invenção e criava uma sexta
faixa numérica sem limites declarados.

## D13 — Custo desconhecido nunca é zero

**Conflito.** `REN-005` inadimplência, `CUS-014` custo jurídico potencial e `CUS-015`
probabilidade jurídica tinham default 0, contrariando a regra explícita da própria fonte de
parâmetros — "nunca assumir custo zero apenas porque não foi encontrado" — e o princípio
SAFE-005 desta spec.

**Decisão.** Os três passam a `(obrigatório investigar)` com estado `UNKNOWN`, contingência e
pendência, igual a `CUS-005` e `CUS-006`. `CUS-013` permanece 0,15 `[DEFAULT]` com a
simplificação declarada em `PEND-IR`. `REN-012` passa a `[PENDENTE-DECISÃO]` sem default
numérico; enquanto pendente, o yield líquido é emitido como provisório.

**Motivo.** `P-A` e SAFE-005. Default zero é indistinguível de "verifiquei e é zero", e a
diferença muda a decisão.

## D14 — Custo de oportunidade não é retorno exigido

**Conflito.** `GLB-007` acumulava duas funções: preço do tempo do capital, usada no carrying,
e retorno mínimo exigido, usada como limiar de aprovação. Com isso o retorno exigido era
cobrado duas vezes — uma como custo e outra como limiar.

**Decisão.** Desdobrado. `GLB-007` `custo_oportunidade_capital_aa`, usada no carrying de
`R30.3`; `GLB-011` `retorno_minimo_exigido_aa` = Selic + 15 p.p., usada em `R33.9`. Definida
a anualização que faltava: `roi_anualizado = (1 + roi_liquido)^(12 ÷ prazo em meses) − 1`,
comparável com `GLB-011`. Além disso, o componente de custo de oportunidade de `CUS-016` é
excluído do TCO usado em desconto, margem e ROI (`R26.1.2`).

**Motivo.** Sem a separação, uma operação de três meses com ROI de 16,5% era comparada com
uma taxa anual, o que é incomparável; e o custo do capital entrava no denominador do próprio
ROI que deveria superá-lo.

## D15 — Restauração da numeração de parâmetros

**Conflito.** A spec havia renumerado silenciosamente as faixas `VAL`, `CMP`, `LOC` e `ALT`,
perdido dois parâmetros e apontado referências cruzadas para os IDs errados — em especial
`R21.4`, que restringia comparáveis apontando raio e janela para parâmetros que passaram a
significar outra coisa.

**Decisão.** Numeração do catálogo de parâmetros restaurada, com dois parâmetros
reintroduzidos: `VAL-008` margem conservadora, que faltava e sem a qual o valor
`conservador` de `R23` não tinha derivação; e `CMP-008` estado de conservação como ajuste
obrigatório, que é a variável que mais separa imóvel de leilão de imóvel anunciado. Os
parâmetros que a spec havia inserido nesses IDs receberam IDs novos no fim da faixa
(`VAL-011`, `CMP-011` a `CMP-014`). `LOC-011` volta a `perfil_socioeconomico_aceitavel`
(informativo) e o desconto adicional de classe C passa a `LOC-013`. `ALT-010` volta a
"reavaliação por evento material" e "pendência vencida" passa a `ALT-016`. Publicada a tabela
de equivalência ID antigo → ID novo. Corrigidas todas as referências cruzadas.

**Motivo.** `P-D`. Renumeração silenciosa faz com que uma referência a `VAL-004` signifique
coisas diferentes em documentos diferentes, e foi exatamente o que produziu o defeito de
`R21.4`.

**Correção a esta decisão, registrada.** A formulação original desta decisão atribuía
`VAL-010` ao critério de outlier. O catálogo de parâmetros define `VAL-010` como "diferença
máxima entre fontes" e `CMP-010` como "outlier"; a formulação original atribuía outlier a
dois IDs. Por `P-D`, prevalece o catálogo: `VAL-010` é `diferenca_maxima_entre_fontes_pct` e
`CMP-010` é `outlier`.

## D16 — O gate jurídico tem 19 verificações

**Conflito.** A spec citava **três** contagens divergentes para o mesmo conjunto (21 em uma
seção, 21 em outra, e uma lista incompatível na matriz de rastreabilidade) e apoiava parte da
contagem na família `RULE-REG-001` a `RULE-REG-004`.

**Decisão.** A família `RULE-REG-*` **não existe em nenhuma fonte** e foi removida: a matriz
canônica tem 45 regras e nenhuma com prefixo `REG`. O conjunto do gate passa a 13
`RULE-JUR-*` + 4 `RULE-ED-*` + `RULE-ID-001` + `RULE-ID-002` = **19 verificações**.
`RULE-OCC-001`, `RULE-OCC-002`, `RULE-LOC-001` e `RULE-LOC-002` ficam na camada 6 de risco e
não integram o gate. Corrigidas as três contagens e acrescentado o crosswalk explícito
`GATE-JUR-001` a `GATE-JUR-006` → regras canônicas em `R12`.

**Motivo.** Verificação direta: as regras citadas não existem. Ocupação e locação são risco
de posse e de economia, não validade do procedimento — colocá-las no gate contradiz SAFE-013.

## D17 — Identificadores de checklist

**Conflito.** Os Anexos B e C.1 não tinham identificadores próprios, o que torna o teste de
cobertura de catálogo exigido pelo projeto técnico inescrevível.

**Decisão.** Anexo B passa a `B-01` a `B-27`, com coluna do ID de origem preservada. Anexo
C.1 passa a `C-01` a `C-71`, em que o número do identificador é o número do critério.

**Motivo.** Cobertura de catálogo é propriedade verificável (`P16.1`) e propriedade
verificável exige identificador estável.

## D18 — Remapeamentos da matriz canônica

**Conflito.** O mapeamento de checks para regras canônicas tinha quatro erros internos.

**Decisão.** Quatro correções declaradas:

| Check | Mapeamento da fonte | Mapeamento correto | Motivo |
|-------|---------------------|--------------------|--------|
| `MC-025` | `RULE-JUR-004` | `RULE-JUR-005` | O check trata das intimações dos **leilões**; `RULE-JUR-004` é purgação da mora |
| `MC-026` | `RULE-JUR-004` | `RULE-JUR-005` | Mesma razão |
| `MC-048` | `RULE-OCC-001` | `RULE-OCC-002` | Posse de **terceiro** é o objeto de `RULE-OCC-002` |
| `MC-049` | `RULE-OCC-001` | `RULE-LOC-001` | Ocupação por **inquilino** é locação |

**Motivo.** O próprio critério de agrupamento da fonte, declarado na seção de mapeamento,
exige essas atribuições. O mapeamento publicado se contradizia.

## D19 — Regras de bloqueio de risco incorporadas

**Conflito.** Dez regras de bloqueio de risco existiam na fonte de risco e não tinham
representação no catálogo canônico desta spec.

**Decisão.** Incorporadas ao Anexo D como `RULE-RSK-001` a `RULE-RSK-010`, com os efeitos da
fonte, incluindo os `BLOCK` de `D2` e `D3`, "passivo crítico sem limite conhecido ⇒
`PENDENTE` ou `BLOCK`" e "restrição de aquisição incompatível ⇒ `BLOCK`". O Anexo D passa a
ter **55 regras**.

**Motivo.** Regra que não está no catálogo não é executada nem auditada. Quatro delas
produzem `BLOCK` e estavam fora.

## D20 — Risco crítico bloqueia independentemente da evidência

**Conflito.** A fonte de risco é internamente contraditória: uma seção declara `BLOCK`
incondicional para severidade crítica; outra condiciona o bloqueio a confiança alta. A spec
seguia a segunda, exigindo evidência `CONFIRMED`.

**Decisão.** `BLOCK` quando a severidade é `critico`, independentemente do estado da
evidência. Com evidência `ESTIMATED` ou `INFERRED`, o bloqueio é registrado como "bloqueio
por risco crítico presumido" com condição objetiva de desbloqueio: confirmar ou afastar o
risco. Corrigidos `R34.5` a `R34.5.2` e a propriedade `P8.6`.

**Motivo.** `P-A` pelo lado seguro, sem travar irreversivelmente. Exigir `CONFIRMED` para
bloquear significa que um risco crítico apenas estimado libera a compra — o oposto da
função do bloqueio. A condição de desbloqueio evita o efeito contrário, de bloqueio
permanente por suspeita.

## D21 — Investor Fit com sete componentes

**Conflito.** A fonte de portfólio lista oito componentes de aderência, entre eles "qualidade
econômica"; a spec usava quatro, sem liquidez, horizonte nem esforço operacional.

**Decisão.** Sete componentes, com os pesos renormalizados: `aderencia_estrategia` 0,27;
`aderencia_risco` 0,20; `liquidez_vs_necessidade` 0,13; `aderencia_capital` 0,13;
`diversificacao` 0,13; `esforco_operacional` 0,07; `horizonte` 0,07. Soma 1,00. O componente
"qualidade econômica" foi **excluído**. Corrigidos `R51.1` e `SCORE-006`.

**Motivo.** Qualidade econômica é o Opportunity Score; incluí-la no Fit violaria a separação
obrigatória entre os dois scores, declarada pela própria fonte. Os três componentes ausentes
são justamente os que distinguem "boa oportunidade" de "boa oportunidade para este
investidor".

## D22 — `qualidade_oportunidade` nos pesos por estratégia

**Conflito.** O fator constava dos pesos mestres e não das cinco colunas de override. Como
cada coluna já somava 1,00 sem ele, seu peso efetivo por estratégia era **zero**,
contrariando `R49.2` e `R60.2`, que o exigem como componente.

**Decisão.** Incluído nas cinco colunas com peso 0,05, e os demais pesos reduzidos
proporcionalmente para manter soma exata de 1,00 por coluna. Verificado: as cinco colunas
somam 1,00.

**Motivo.** Um fator exigido por requisito com peso efetivo zero é requisito não atendido, e
a propriedade `P10.18` passa a detectar.

## D23 — Score composto com cinco fatores

**Conflito.** A fonte de ranking define cinco fatores; a spec usava quatro, com "capital e
concentração" fundidos em um só.

**Decisão.** Cinco fatores: `Opportunity Score × fator de confiança × fator de Investor Fit ×
ajuste de capital × ajuste de portfólio`. O ajuste de portfólio cobre o bônus de equilíbrio
de estratégias e a penalização por capital imobilizado. **Concentração e diversificação ficam
só no componente `diversificacao` do Investor Fit**, para não contar duas vezes; a escolha
está registrada em `SCORE-008` e em `R47.4.1`. Corrigido `R52.1`.

**Motivo.** Fundir capital e concentração em um fator impedia distinguir "não cabe no meu
capital" de "concentra demais a carteira", que exigem ações diferentes. A escolha de manter
concentração em um único caminho é registrada porque, sem esse registro, uma leitura futura
a reintroduziria nos dois lugares e penalizaria a mesma característica duas vezes.

## D24 — Escalas de prioridade

**Conflito.** Duas escalas com rótulos concorrentes: `P0` a `P4` mais `BLOCK` para urgência, e
`P1` a `P5` para atratividade combinada. O mesmo rótulo `P1` significava coisas diferentes.

**Decisão.** `P0` a `P4` mais `BLOCK` é a escala canônica de **urgência**. A escala de
atratividade combinada com aderência e capital é renomeada para `A1` a `A5` e mapeada para a
matriz final de priorização. `P0` ganha o terceiro disparador da fonte: **oportunidade
excepcional**. Registrado em `SCORE-009` e `R52.6`.

**Motivo.** Rótulos colidentes tornam qualquer relatório ambíguo. A renomeação preserva as
duas escalas, que medem coisas distintas e independentes.

## D25 — Precedência de escopo

**Conflito.** `R54.10` determinava que a regra global prevalece sobre a regra de estratégia,
contradizendo `R44.9`, a hierarquia de escopo declarada no catálogo de parâmetros e duas
fontes que afirmam o contrário.

**Decisão.** O escopo mais específico prevalece, exceto quando o menos específico impõe
bloqueio crítico ou restrição legal ou documental. Corrigidos `R54.10` e `R54.10.1`.
Registrado como **superado** o trecho da fonte de decisão que afirmava "regra global vence".

**Motivo.** `P-C`. A formulação anterior tornava toda a hierarquia de escopo inútil: se o
global sempre vence, parametrizar por estratégia não tem efeito.

## D26 — Escopo do custo econômico total

**Conflito.** `R26.1` incluía "custos de saída conforme a estratégia" no TCO, enquanto
`R27.9` e `R27.11` os subtraíam novamente na perna de venda.

**Decisão.** O TCO é o custo de **adquirir e transformar até a saída** e **não** inclui custos
de saída nem IR sobre ganho de capital. Removido "custos de saída conforme a estratégia" de
`R26.1`; os custos de saída ficam exclusivamente em `R27.9`. O `CostBreakdown` passa de
quinze para **treze** componentes. Corrigida toda referência a "quinze componentes".

**Motivo.** Dois defeitos concretos. Primeiro, dupla contagem: no caso de prova `F.1` ela
valia **7,69 pontos percentuais** de ROI. Segundo, definição circular do IR: `R27.10` define a
base do IR subtraindo o TCO; com o IR dentro do TCO, ele dependeria de si mesmo. A leitura é
consistente com a própria fonte de economia, que exclui os custos de saída do capital
empregado antes da venda, e com a fonte de valuation.

## D27 — Preço máximo por ROI alvo inclui o ITBI

**Conflito.** A derivação do preço máximo usava apenas a comissão de compra no coeficiente
proporcional ao preço, omitindo o ITBI, que também é proporcional ao preço.

**Decisão.** `TCO = P(1 + c_c + c_itbi) + F`, logo
`preço_maximo = (V(1−c_v)(1−t) − F(1+r−t)) ÷ ((1 + c_c + c_itbi)(1+r−t))`. Com as entradas de
`F.1` o resultado é **R$ 182.158,03**, e não R$ 185.627,71. A verificação inversa está
publicada em `F.1.5`: o ROI recalculado com esse preço é exatamente 25%, com erro inferior a
1e-6. Corrigidos `R28.2`, `R28.2.1` e `R28.3`, e acrescentada em `R28.2.2` a generalização
para reserva proporcional.

**Motivo.** Aritmética: omitir um custo proporcional ao preço superestima o teto em
R$ 3.469,68 no caso de prova, o que é um falso positivo econômico.

## D28 — O teto conservador do método não é limite superior

**Conflito.** A spec afirmava, como propriedade `P7.10`, que o teto conservador do método de
referência nunca excede o preço máximo exato.

**Decisão.** A propriedade é **falsa** e foi removida. Contraexemplo verificado, com IR igual
a zero — caso previsto por `CUS-013` e por `PEND-IR`.

**Entrada completa do contraexemplo** (obrigatória para reprodução do teste dirigido):
`V = 300.000`, `c_v = 0,06`, `F = 23.000`, `c_c = 0,05`, `r = 0,25`, `t = 0` e **`c_itbi = 0`**.
A declaração de `c_itbi = 0` é indispensável: `R28.2.1` inclui o ITBI no coeficiente
proporcional ao preço, logo sem essa entrada os números publicados não se reproduzem.

- Preço máximo exato (`R28.2`): `(300.000 × 0,94 − 23.000 × 1,25) ÷ (1,05 × 1,25)
  = 253.250 ÷ 1,3125 = 192.952,38`.
- Teto conservador (`R28.4`): `(282.000 − 23.000) ÷ (1 + 0,05 + 0,25) = 259.000 ÷ 1,30
  = 199.230,77`.
- Diferença: `199.230,77 − 192.952,38 = 6.278,39`.

Com `c_itbi = 0,02`, o preço máximo exato cai para `253.250 ÷ (1,07 × 1,25) = 253.250 ÷ 1,3375
= 189.345,79`, enquanto o teto conservador permanece em R$ 199.230,77 porque a forma fechada
conservadora do método não contempla o ITBI. A diferença sobe de R$ 6.278,39 para
R$ 9.884,98: a falsidade da propriedade removida **se agrava** com o ITBI, não se atenua.

O teto conservador passa a **referência informativa**, e o
teto decisório é definido como `mínimo(preço máximo exato; preço máximo ajustado ao risco)`.
Corrigidos `R28.4` a `R28.4.2`, `P7.10` e acrescentado `REG-033`.

**Motivo.** Aritmética. A derivação das duas formas difere no tratamento da base do IR; com
`t = 0` a forma conservadora perde o termo que a mantinha abaixo da exata. Manter a
propriedade produziria um teste que falha em entrada legítima.

## D29 — Golden Case F.1 republicado

**Conflito.** Quatro problemas simultâneos no caso de prova: o TCO publicado era o da
planilha, que não obedece a `CUS-011`; o desconto líquido era calculado sobre o preço de venda
e não sobre o valor de mercado provável; o teto conservador do método estava rotulado como
"preço máximo por ROI alvo"; e os demais números não eram coerentes com o TCO da spec.

**Decisão.** Republicado em `F.1` com as contas mostradas.

(a) O TCO de aquisição da planilha, R$ 228.066,9017, permanece como valor de origem, mas o
Golden Case é oráculo **desta spec**, então o TCO econômico conforme `R26.1` também é
publicado: reserva de imprevistos a 5% da base (a planilha usou R$ 5.000, que é **2,2415%**) e
carrying do prazo base, declarado explicitamente como **90 dias** com `CUS-016` de
**R$ 635,00/mês**. Resultado: **R$ 236.125,246785**.

(b) Desconto líquido calculado sobre o valor de mercado **provável** de R$ 290.000 conforme
`R27.3`: **18,5775%** com o TCO da spec e **21,3562%** com o TCO da planilha. Os 23,98%
publicados antes estavam errados — usavam R$ 300.000 como base, inflando o desconto em 2,62
pontos percentuais.

(c) Preço máximo por ROI alvo **R$ 182.158,03** conforme `D27`, e **R$ 168.374,76** rotulado
corretamente como teto conservador do método, nunca como preço máximo por ROI alvo.

(d) ROI, margem, yields, base de IR e venda líquida recalculados com o TCO da spec, cada
número publicado com a fórmula que o produz: ROI líquido 16,5139%; ROI anualizado 84,2940%;
margem líquida 12,9978%; margem percentual 18,5775%; base de IR R$ 45.874,753215; venda
líquida R$ 275.118,78701775; yield bruto mensal 0,8047%; yield líquido mensal 0,4955%; yield
líquido anual 5,9460%; break-even de saída R$ 251.197,07105.

Os dois vereditos `DO_NOT_BUY` se mantêm e ficam **mais folgados**, confirmado
aritmeticamente: a folga de revenda passa de 1,02 para 6,4225 pontos percentuais e a de renda
passa de 0,287 para 0,3045 pontos percentuais.

Registrado também que os dados de entrada de `F.1` vêm da planilha e **não** dos documentos de
negócio, e que a documentação apresenta exemplos com outro conjunto de números que não se
reconcilia com este.

**Motivo.** Um Golden Case que publica números inconsistentes com as próprias regras da spec
não é oráculo: é ruído. As duas reprovações ficarem mais folgadas confirma que as correções
não mudaram o veredito, apenas a margem com que ele é alcançado.

## D30 — Faixas de confiança do valuation sem lacuna

**Conflito.** As faixas de `R22` deixavam a faixa 60–74 **inalcançável**, e `VAL-002` era uma
faixa "7 a 10", o que torna ambígua a comparação "quantidade ≥ `VAL-002`".

**Decisão.** Cinco faixas contínuas: 90–100 com amostra ideal de classe `A`/`B`; 75–89 com
amostra ideal de classe `A` a `C`; **60–74** com amostra que atende `VAL-001` mas não a faixa
ideal, ou amostra ideal de qualidade média; 40–59 com amostra fraca; 0–39 com evidência
isolada. `VAL-011 comparaveis_ideais` definido como limiar único igual a **7**.

**Motivo.** Uma faixa inalcançável significa que nenhuma amostra intermediária recebia
confiança média, e o salto de 89 para 59 mudava o fator de confiança de 0,95 para 0,75 sem
estado intermediário. Registrado que uma das fontes admite "3 a 5 como base inicial
razoável", faixa que a resolução anterior descartou e que agora é coberta pela faixa 40–59.

## D31 — Yield: piso sobre o líquido

**Conflito.** Duas fontes fixam o piso de 0,80% mensal sobre o yield **bruto**; a
especificação canônica interna anterior o fixava sobre o **líquido**.

**Decisão.** Mantido o piso decisório sobre o yield **líquido** (`REN-009` = 0,0080), agora com
a justificativa escrita na própria spec: no caso de prova `F.1` o bruto é 0,8047% e o líquido
é 0,4955%; aplicar o piso ao bruto aprovaria um imóvel cujo aluguel líquido é **61,58%** do
bruto. `REN-002` bruto permanece informativo, com nota explícita de que perdeu efeito
decisório. Definida a base do IR sobre aluguel que faltava:
`máx(0; aluguel − condomínio não recuperável − IPTU não recuperável − manutenção − seguro e taxas) × REN-012`.
Acrescentados `seguro e taxas` e `inadimplência` ao `aluguel_liquido` de `R27.7` e restaurado
o piso em zero.

**Motivo.** `P-A` e SAFE-016. Aplicar o piso ao bruto transforma custos recorrentes não
deduzidos em melhora da tese.

## D32 — Carrying completo

**Conflito.** `CUS-016` listava quatro componentes; `R30.2` listava a lista completa de seis.
O parâmetro contradizia o requisito.

**Decisão.** `CUS-016` passa a condomínio + IPTU e taxas + seguro e manutenção + custo
financeiro + despesas operacionais + custo de oportunidade do capital (`GLB-007`), alinhando
com `R30.2`. Registrado em `R26.1.2` que o componente de custo de oportunidade é usado apenas
nas métricas de custo do tempo e de eficiência de capital, e excluído do TCO usado em
desconto, margem e ROI.

**Motivo.** Alinhamento com a fonte de economia. A exclusão do custo de oportunidade do TCO
decisório segue a mesma lógica de `D26` e `D14`: não cobrar o retorno exigido duas vezes.

## D33 — Break-even comparado ao preço atual

**Conflito.** `R33.7` comparava o break-even de saída com o valor de mercado conservador; a
fonte de economia o compara com o **preço atual**.

**Decisão.** `R33.7` passa a comparar com o preço atual e `R33.7.1` declara a unidade do
limiar como fração do preço atual.

**Motivo.** `P-D` e coerência. O break-even responde "a partir de que preço de venda eu não
perco", e a referência de risco é quanto eu vou pagar, não quanto o mercado vale no cenário
pessimista.

## D34 — Entidades ausentes do dicionário

**Conflito.** Regras da spec dependiam de entidades e campos que o dicionário não declarava:
`R10.1` exige histórico de preços e `R10.3` exige versões do perfil, sem estrutura para
nenhum dos dois; regras de localização, due diligence e score não tinham entidade própria.

**Decisão.** `R74` acrescenta como entidades próprias Localização, Due Diligence, Score com
composição, Versão do Perfil Consolidado, Histórico de Preços, Divergência, Posição de
Portfólio e Resultado Real. Acrescentados os campos `banheiros` e `complemento` de endereço.
O perfil consolidado passa a ter os grupos Condominial, Ocupacional e Qualidade (`R10.8` a
`R10.11`). `R74.11` determina que regra dependente de estrutura ausente é rejeitada e o
requisito é reportado como NÃO AVALIADO.

**Motivo.** Regra que depende de estrutura inexistente é regra não executável, e a spec a
declarava como se fosse.

## D35 — Identidade: lacuna de cobertura e grau dos sinais

**Conflito.** Endereço completo **com** unidade, sem matrícula e sem identificador oficial,
ficava sem nível atribuído, embora a fonte de captura atribua força **alta** a esse sinal. E
`I4` exigia matrícula, embora a fonte diga "confirmada por documentação". Preço, avaliação da
fonte e desconto eram descritos como força **nula**, o que é incorreto.

**Decisão.** `I3` passa a cobrir o caso de endereço completo com unidade sem matrícula e sem
identificador oficial. `I4` passa a admitir qualquer documentação registral que identifique o
imóvel. Acrescentado `imagem_semelhante` como sinal complementar de força `media`. Preço,
avaliação da fonte e desconto passam a força `baixa`, porém **proibidos** como sinal isolado
de identidade e **proibidos** para deduplicação — mantém o efeito prático e corrige o grau.
Acrescentadas as dimensões de deduplicação que faltavam: descrição semelhante (peso `fraco`),
área próxima (peso `medio`), quartos iguais (peso `medio`) e vagas iguais (peso `fraco`).

**Motivo.** A lacuna deixava sem nível o caso mais comum em portais imobiliários. Sobre o
grau: força nula é afirmação factualmente errada — o preço carrega alguma informação — e a
correção preserva a proibição, que é o que importa para a decisão.

## D36 — Escopo e priorização do MVP

**Conflito.** A spec não tinha domínio de escopo e priorização, e nenhum requisito tinha
prioridade atribuída, o que torna a ordem de implementação não derivável.

**Decisão.** Domínio novo, com `R75`: 23 capacidades `P0` (as 22 da fonte mais a validade
jurídica do adendo v1.1), nove `P1`, oito `P2`, nove itens fora do MVP, e a regra de controle
de escopo em seis categorias. Cada requisito desta spec passa a ter prioridade em coluna
própria do Índice de Requisitos e da Matriz de Rastreabilidade.

**Motivo.** Sem prioridade por requisito, a ordem de construção depende de interpretação, e
uma spec de 83 requisitos não é implementável em bloco.

## D37 — Telas e capacidades sem requisito

**Conflito.** Capacidades declaradas `P0` na fonte não tinham nenhum critério de aceitação:
Análise Profunda (`P0-18` e tela `P0`), Cenários como espaço de teste de premissas, e
Configurações do Investidor. O radar também havia perdido as oito visões pré-definidas.

**Decisão.** Criados `R76` Análise Profunda, com tese, argumentos a favor, argumentos contra,
contrapontos e as **oito** perguntas da fonte; `R77` Cenários como espaço de teste de
premissas; e `R78` Configurações do Investidor com os **doze** grupos da fonte. Devolvidas ao
radar as oito visões pré-definidas em `R66.4.1`: Top, por estratégia, por região, novidades,
queda de preço, score crescente, monitoramento e bloqueadas. Acrescentados "radar diário" e
"risco por severidade" aos relatórios de `R69.1`.

**Motivo.** Capacidade `P0` sem critério de aceitação não é implementável nem testável.

## D38 — Interface de programação

**Conflito.** Seis capacidades apresentadas na interface não tinham contrato de programação
correspondente.

**Decisão.** `R79` exige cobertura para visão geral, ações do card (salvar, monitorar, criar
alerta), linha do tempo, comparação de 2 a 5, visão de monitoramento e as **oito** decisões do
investidor, com autenticação obrigatória e rejeição explícita de valor fora de domínio.

**Motivo.** Interface que depende de comportamento não especificado é interface que divergirá
da especificação sem aviso.

## D39 — Monitoramento e alertas

**Conflito.** O gatilho mais comum da due diligence — pendência resolvida — estava ausente,
assim como os seis sinais de mercado obrigatórios, o gatilho de recomparação da carteira por
oportunidade excepcional, três alertas de ranking e o objeto de monitoramento com estados.

**Decisão.** Acrescentados: `MON-011` pendência resolvida ⇒ recalcular confiança, score e
ranking; `MON-012` a `MON-016`, os seis sinais de mercado com impacto mapeado; `MON-017` nova
oportunidade excepcional ⇒ recomparar a carteira automaticamente; `ALT-017` subiu 20 posições,
`ALT-018` saiu do Top 10 e `ALT-019` passou a `BLOCK`; e o objeto de monitoramento com dez
estados em `R57.10.1`.

**Motivo.** Sem `MON-011`, resolver uma pendência não devolvia a oportunidade ao ranking, o
que torna a due diligence um beco sem saída. Os demais itens constavam das fontes.

## D40 — Governança

**Conflito.** `R65.1` exigia "evidência suficiente" sem critério; faltavam indicadores de
falso positivo e falso negativo, a população do falso negativo, o controle de sobreajuste, o
nível de mudança para faixa de classificação e identificadores de parâmetro na seção SCORE.

**Decisão.** Acrescentados: a hierarquia de qualidade de evidência em cinco níveis (`forte`,
`boa`, `moderada`, `fraca`, `ausente`) em `R65.1.1`; os indicadores de falso positivo e falso
negativo em `R80`; a coorte de rejeitadas e ignoradas e o controle de sobreajuste em `R60.3.1`
a `R60.3.4`; "mudança de faixa de classificação" como nível `alto` exigindo backtest e
aprovação em `R62.4.1`; e identificadores `SCORE-001` a `SCORE-009` para a seção SCORE.

**Exceção sobre bloqueio crítico.** **Mantida** a proibição absoluta desta spec, registrada
como **endurecimento deliberado**: a fonte de governança admitia superar bloqueio crítico
"com autorização adequada", e esta spec não admite em nenhuma hipótese (`R63.4.1`).

**Motivo.** "Evidência suficiente" sem critério é cláusula de escape. Falso negativo sem
população definida é indicador incalculável. E uma autorização capaz de superar bloqueio
crítico anularia SAFE-002 por via administrativa.

## D41 — Capital e portfólio

**Conflito.** Faltavam reserva percentual do patrimônio líquido, esforço operacional e meta de
renda no perfil, alocação-alvo por estratégia, três das cinco métricas de eficiência, faixas
de ação por posição no ranking e ordem de desempate parametrizável. E `INV-002` de R$ 250 mil
convivia com tickets por estratégia de R$ 300 mil e R$ 400 mil sem regra de precedência.

**Decisão.** Acrescentados `INV-019` reserva percentual, `INV-020` esforço operacional,
`INV-021` meta de renda, e o grupo `PORT-001` a `PORT-008` com alocação-alvo, desvio máximo,
limites de concentração, limite de capital imobilizado, bônus de equilíbrio, penalidade de
capital imobilizado, faixas de ação por posição e ordem de desempate por estratégia. As cinco
métricas de eficiência em `R46.8`, incluindo renda por capital, margem por capital e renda
líquida por risco. Ticket por estratégia: renda R$ 300 mil e revenda R$ 400 mil; `INV-002` de
R$ 250 mil passa a **default do perfil**, com a estratégia prevalecendo por `D25`.

**Motivo.** Sem alocação-alvo não há como medir desvio nem aplicar o bônus de equilíbrio de
`SCORE-008`. Sem faixas de ação, o ranking não se converte em trabalho.

## D42 — Critérios por estratégia e perfil de ativo

**Conflito.** A fonte de portfólio exige critérios que a spec não avaliava, e vários critérios
eram descritos sem parâmetro correspondente.

**Decisão.** Completados: apartamento ganha preço por m², dormitórios, financiabilidade,
demanda de locação e demanda de venda; casa e sobrado ganham ticket, público familiar,
financiabilidade e uso alternativo; MCMV ganha custo de reforma e potencial de revenda;
terreno ganha ticket e capital imobilizado. Renda ganha reforma máxima, prazo máximo de
estabilização e concentração máxima por região **como parâmetros da estratégia**; valorização
ganha horizonte mínimo e tolerância a capital imobilizado; revenda ganha custo máximo de
reforma e capital máximo por operação. Perfis de ativo passam a incluir `terreno`, `rural`,
`outros` e `desconhecido`, mantendo `galpao`, que tem origem em `TIP-001`. Acrescentada a
sexta estratégia `customizada`, parametrizável pelo investidor, exigida por `P0-12`.

**Motivo.** Critério sem parâmetro não é avaliável. E a estratégia configurável é capacidade
`P0` declarada.

## D43 — Compensações condicionais

**Conflito.** `R45.10` exigia "margem adicional" quando a liquidez está abaixo do mínimo, sem
número; `LIQ-010` é compensação por **prazo**, não por liquidez, e estava sendo usado como se
cobrisse os dois casos.

**Decisão.** Acrescentado `LIQ-011 margem_minima_liquidez_baixa` = 0,30. `R45.10` e `R45.10.1`
passam a aplicar `LIQ-010` e `LIQ-011` cumulativamente, porque compensam fatores distintos.
Acrescentado também, em `R45.11`, "imóvel atípico exige comparáveis de qualidade superior".

**Motivo.** Exigência sem número não é verificável, e reutilizar a compensação de prazo para
cobrir iliquidez subcompensa o caso mais grave.

## D44 — Score econômico como indicador informativo

**Conflito.** A resolução anterior arrolava a fonte de economia como **concordante** com os
pesos mestres do Opportunity Score. É leitura errada: aquela fonte define um score econômico
próprio, de sete componentes e pesos diferentes.

**Decisão.** Incorporado como `SCORE-005`, indicador informativo `score_economico` com os sete
componentes da fonte — desconto 25, margem 25, ROI 15, liquidez 10, prazo 10, risco econômico
10, complexidade 5 — **sem efeito decisório**. Corrigida a resolução anterior.

**Motivo.** Tratar dois modelos distintos como um só apagava um deles e dava falsa impressão
de convergência entre fontes.

## D45 — Colisão de namespace entre catálogos

**Conflito.** Dois catálogos de parâmetros usam os **mesmos IDs para parâmetros diferentes** em
dez ou mais casos.

**Decisão.** A numeração do catálogo de parâmetros (Documento 8) é canônica (`P-D`). A tabela
abaixo existe para que nenhuma leitura futura reintroduza o erro.

| ID | Significado canônico (catálogo de parâmetros) | Significado no catálogo de estratégias |
|----|------------------------------------------------|----------------------------------------|
| `REN-002` | Yield bruto mensal mínimo | Vacância |
| `VAL-003` | Raio máximo de comparáveis | Critério de outlier |
| `VAL-004` | Janela temporal de comparáveis | Faixa conservadora de valor |
| `CUS-002` | Comissão do leiloeiro | Reforma |
| `CUS-003` | ITBI | Custo de saída |
| `PRI-002` | Preço máximo | Desconto mínimo |
| `LOC-003` | Bairro prioritário | Zona condicional |
| `LIQ-002` | Prazo máximo de venda | Liquidez de venda |
| `CONF-001` | Confiança do preço | Dados incompletos |
| `TIP-003` | Quartos mínimos | Perfil de um dormitório |

**Motivo.** Sem a tabela, qualquer citação futura de `CUS-002` é ambígua, e a ambiguidade
troca comissão de leiloeiro por custo de reforma.

## D46 — Terminologia jurídica

**Conflito.** O material de origem escreve "devedor fiduciário" em dois checks e na matriz
canônica.

**Decisão.** Usar **devedor fiduciante** em toda a spec, com nota no glossário e nos itens
`B-10` e `B-11`.

**Motivo.** Está errado: na alienação fiduciária o devedor é o **fiduciante** e o credor é o
**fiduciário**. Propagar o erro produz busca documental e redação de pareceres incorretas.

## D47 — Pipeline e enriquecimento

**Conflito.** Duas fases existiam como componentes e não como marco persistido: qualificação
(gate `G1`) e consolidação de perfil. E o enriquecimento progressivo tinha dependência
circular: os níveis dependiam do score, que só existe no passo 12, enquanto o enriquecimento é
o passo 5.

**Decisão.** Acrescentadas `QUALIFIED` e `CONSOLIDATED` a `PipelinePhase` e à ordem obrigatória
de `R70.1`, que passa a ter 20 etapas e 16 fases persistidas. O enriquecimento passa a depender
do **potencial preliminar** em faixas qualitativas — `descartavel`, `baixo`, `medio`, `alto`,
`excepcional` — e não do score (`R5.2` a `R5.7`).

**Motivo.** Fase que não é registrada não é verificável pelo traço de execução. E a dependência
circular tornava `R5` inexecutável na ordem declarada por `R70.1`.

## D48 — Frescor da matrícula

**Conflito.** A fonte de parâmetros declara, para matrícula e documentação registral,
"até mudança ou evidência nova" — a única linha explicitamente **não temporal** da tabela. A
spec a havia reescrito como 30 dias de validade.

**Decisão.** "Até mudança ou evidência nova", com **revalidação obrigatória antes da decisão de
compra** e alerta de revalidação aos 30 dias (`ALT-020`). Corrigidos `R13.3` a `R13.3.2` e a
tabela FRESH.

**Motivo.** `P-D`. Prazo fixo tem dois defeitos opostos: aos 29 dias trata como atual uma
certidão que pode ter sido superada por averbação no dia seguinte à emissão, e aos 31 dias
invalida uma certidão que continua correta. A revalidação antes da compra resolve os dois.

## D49 — Ausência de evidência nos itens de checklist

**Conflito.** A coluna "Ausente ⇒" do Anexo A usava oito valores ad hoc e atribuía `REPROVADO`
a itens em que a informação apenas faltava.

**Decisão.** `P-E` aplicado. `REPROVADO` fica reservado para evidência de irregularidade.
`MC-007` (captura preservada) e `MC-069` (contingência para valores desconhecidos) passam de
`REPROVADO` para `PENDENTE` crítico. `MC-045` (ocupação desconhecida) passa de `PENDENTE`
crítico para `PENDENTE` **alta**, alinhando com `R18.3` e `RULE-OCC-001`. A coluna passa a usar
exclusivamente o vocabulário de `R36.3` mais os estados de pendência e de decisão desta spec.

**Motivo.** `REPROVADO` por falta de informação confunde "não verifiquei" com "verifiquei e
está irregular", e as duas situações exigem ações opostas: investigar versus abandonar.

## D50 — Disciplina de lance com requisito numerado

**Conflito.** Os hard stops, os itens pré-lance, as verificações de evicção e a revalidação
final do dia do lance existiam apenas como tabelas de anexo, sem requisito numerado e sem
nenhuma linha na Matriz de Rastreabilidade para `C.3` a `C.6`.

**Decisão.** Criado `R82`, que numera os 9 hard stops, os 12 itens pré-lance, as 9 verificações
de evicção e a revalidação final. Acrescentados os 12 itens da revalidação final como `RL-01`
a `RL-12` no novo Anexo C.7, incluindo os **quatro sem equivalente** em `C.4`: condições de
pagamento confirmadas, evicção documentalmente confirmada, nenhuma divergência pendente e
reserva de contingência disponível. Restaurado o campo "comissão fora do lance, somar no custo
total" em `C.5` e desdobrado "histórico do leiloeiro" nas seis verificações `HL-01` a `HL-06`.

**Motivo.** A disciplina de lance é a última barreira antes de um compromisso irreversível, e
era a única parte da spec sem requisito nem rastreabilidade.

## D51 — Fonte única

**Conflito.** Quatro camadas normativas sobrepostas, com o artefato que se declarava fonte
única dependendo por indireção das outras três.

**Decisão.** Esta spec é o único artefato normativo. A documentação de origem, o material
extraído dela e as especificações canônicas internas anteriores deixam de ser referenciados.
Todo valor, regra, item e caso de prova está escrito aqui. A pendência `PEND-FONTE-UNICA` é
substituída por essa declaração, em `D.11`. Removida da spec toda frase do tipo "conforme a
especificação canônica §N" e reescrita a justificativa no próprio texto — em particular a de
`D31`, que agora traz o cálculo do caso 227 inline.

**Motivo.** Uma spec que se declara autocontida e cita arquivos externos para justificar
decisões não é autocontida. Quando os arquivos saírem, a justificativa desaparece.

## D52 — Fronteira da IA

**Conflito.** A arquitetura de origem é internamente contraditória: em várias seções e em um
registro de decisão arquitetural declara determinismo e proíbe que agentes decidam; em outra
seção atribui a agentes `AG-00` a `AG-12` o valuation, o TCO e a decisão.

**Decisão.** Mantido o determinismo — ele é fiel à maior parte da arquitetura e à base de
conhecimento, e **não** é endurecimento desta spec. Registrado que os agentes que apareciam
encarregados de valuation, TCO e decisão são mapeados para funções **sem poder de decisão nem
de criação de evidência**; prevalece a leitura restritiva. Definida a fronteira do agente de
extração: ele extrai e localiza evidência propondo uma proposta de evidência com localização
documental exata, promovida a evidência por **ato humano registrado** ou por **regra
determinística declarada** (`R83.1` a `R83.4`). Enumerados os **sete** pontos mínimos de
intervenção humana em `R83.5`, com `R83.6` proibindo configuração que os remova.

**Motivo.** `P-A` para a contradição interna. Sobre os pontos de intervenção: a spec anterior
dizia "pontos de decisão configurados" sem lista, o que permite configurar **zero** pontos e
esvaziar a supervisão.

## D53 — Taxonomia de conhecimento

**Conflito.** A arquitetura define oito tipos de segmento; a base de conhecimento exige mais.
Com oito, os próprios princípios SAFE, as exceções e o catálogo de parâmetros não são
indexáveis como o que são.

**Decisão.** Adotados **quinze** tipos: os oito originais (`REGRA`, `DEFINICAO`, `FORMULA`,
`CHECKLIST`, `EVIDENCIA`, `CASO`, `ANALISE`, `MANUAL`) acrescidos de `PARAMETER`, `EXCEPTION`,
`DECISION`, `GOVERNANCE`, `EVIDENCE_GUIDE`, `STRATEGY` e `SAFETY`. Acrescentados aos metadados
obrigatórios `checklist_id`, `case_id` e `created_at`, e a separação entre `source_text` e
`paraphrase` (`R72.3.1`, `R72.3.2`).

**Correção de contagem.** A formulação original desta decisão e de `R72.2` dizia "doze tipos"
enquanto enumerava quinze nomes. A contagem correta é **quinze**: oito originais mais sete
acrescentados. O numeral "doze" era **defeito de redação, não decisão** — o conjunto adotado é
o superconjunto de quinze, e reduzi-lo a doze exigiria escolher três tipos para remover, o que
nenhuma fonte sustenta. `R72.2.1` já atribui uso explícito a sete dos quinze tipos.

**Motivo.** O conjunto de quinze é superconjunto do de oito, logo adotá-lo não perde nada. A
separação entre texto-fonte e paráfrase é o que impede que os dois coexistam
indistinguíveis — exatamente o risco que `R71.7` tenta evitar.

## D54 — Pendências que permanecem

**Conflito.** A spec misturava pendências de decisão de negócio com pendências de calibração e
com valores interpolados apresentados como derivados.

**Decisão.** Permanecem `[PENDENTE-DECISÃO]` apenas os itens que nenhuma fonte fixa: cidades e
regiões do piloto; perfis habilitados; `PRI-008` preço por m² máximo; `LOC-009` valorização
histórica mínima; `LOC-010` yield regional mínimo; `LIQ-005` compradores potenciais mínimos;
`REN-012` IR sobre aluguel; metodologia do score de liquidez; e calibração de pesos e fatores.

**Regra de comportamento na ausência**, aplicável a cada um deles: enquanto não decidido, o
parâmetro **não é aplicado** e o requisito dependente é reportado como **NÃO AVALIADO**, nunca
como satisfeito (`R74.11`, `P16.3`).

Registrado que `CUS-017` N2 = 0,15 é **interpolação** entre as sensibilidades documentadas de
+10% e +25%, e que `CUS-018` e `CUS-019` iguais a 0,10 são **derivações sem sensibilidade
documentada**; os três passam a `[PENDENTE-CALIBRAÇÃO]`.

**Motivo.** `P-A` e `P-E`. Parâmetro não decidido tratado como satisfeito é a forma mais
silenciosa de converter ausência de decisão em resultado favorável. E valor interpolado
apresentado como derivado esconde que não há fonte para ele.

## D55 — Spec duplicada

**Conflito.** A spec `pipeline-captura-identidade-gate-juridico` reenunciava regras desta spec,
com formulações mais fracas em dez pontos.

**Decisão.** Aquela spec é **integralmente absorvida** por esta e **não é mais fonte de
trabalho**. Os dez pontos em que esta a altera estão enumerados em `D.8`.

**Motivo.** Duas specs enunciando a mesma regra com formulações diferentes produzem
implementações diferentes, e a mais fraca tende a prevalecer porque é a que já está no código.

---

## Decisões anteriores preservadas

As resoluções abaixo foram verificadas na auditoria e **permanecem válidas**. Onde uma decisão
`D1` a `D55` as altera, a coluna de resolução registra a substituição.

| ID | Conflito | Fontes divergentes | Resolução |
|----|----------|--------------------|-----------|
| CONF-VERSAO-15 | Matriz mestra de regras de decisão | Corpo v1.0 sem gate jurídico; adendo v1.1 com o gate de validade jurídica e onze camadas | **MANTIDA por `P-B` e detalhada por `D1`.** O adendo prevalece: o gate de validade jurídica é a **camada 1**, subordinada apenas aos bloqueios críticos da camada 0. |
| CONF-VERSAO-19 | Risco e due diligence | Corpo v1.0 sem etapa P0; adendo v1.1 com validade da consolidação e notificações | **MANTIDA por `P-B`.** `DD-0` inclui a triagem de validade do procedimento. |
| CONF-VERSAO-26 | Plano do MVP | Corpo v1.0 sem validade jurídica no fluxo; adendo v1.1 insere a etapa entre perfil e comparáveis | **MANTIDA por `P-B` e detalhada por `D36`.** A validade jurídica é a capacidade `P0-23`. |
| CONF-PRECEDENCIA | Número de camadas de decisão | Cinco contagens divergentes: 8, 10, 10 com liquidez antes de risco, 8 e 12 | **SUBSTITUÍDA por `D1`: onze camadas, numeradas 0 a 10.** A resolução anterior fixava nove camadas e absorvia risco, liquidez, capital e ranking como sub-verificações, o que tornava a camada determinante ambígua. |
| CONF-SCORE-BANDAS | Faixas de classificação do score | Manual de regras: 5 faixas com verde em 80–89 · quatro outras fontes: 6 faixas com verde em 70–79 | **MANTIDA e corrigida por `D11`.** Seis faixas em `SCORE-003`; o ranking usa o valor numérico, não a cor. A ação típica da faixa 50–59 foi corrigida para "baixa prioridade; só avança com exceção autorizada". |
| CONF-SCORE-PESOS | Pesos do score | Manual de regras: pesos por estratégia · cinco outras fontes: pesos mestres únicos | **MANTIDA e corrigida por `D22`.** Pesos mestres (`SCORE-001`) como default e overrides por estratégia (`SCORE-002`) parametrizáveis, ambos versionados; `D22` acrescenta `qualidade_oportunidade` às cinco colunas, que antes o omitiam e lhe davam peso efetivo zero. |
| CONF-SCORE-MODELO | Modelo de agregação do score | Planilha de referência: média simples de cinco pilares (segurança jurídica, localização, liquidez, financeiro, contexto humano) · quatro outras fontes: soma ponderada de oito fatores | **MANTIDA.** A soma ponderada de oito fatores é o Opportunity Score canônico para ranking. O score de cinco pilares é preservado como indicador executivo informativo, e o pilar de contexto humano é incorporado como `INV-017` com efeito decisório próprio (`R39.3`). Por `D44`, o score econômico de sete componentes também passa a existir como indicador informativo `SCORE-005`, distinto dos dois anteriores. |
| CONF-CONFIANCA | Escalas de confiança | Faixas 90–100, 75–89, 60–74, 40–59, 0–39 · classes A a E e U · rótulos de Muito alta a Inconclusiva · faixas com fator multiplicativo | **MANTIDA e completada por `D12`.** A escala numérica 0–100 com fator multiplicativo (`CONF-007`) é canônica; os seis níveis nomeados são sua face qualitativa (`CONF-010`), não uma escala paralela. As classes A–E e U são preservadas como classificação de qualidade da fonte (`Requirement 1.5`), dimensão distinta da confiança consolidada. |
| CONF-LIQ | Liquidez mínima | Piso 60 na spec anterior · `LIQ-001` igual a 70 no catálogo · renda 70, revenda 75, MCMV 70 nos exemplos · faixas por dezena na fonte de liquidez | **REVOGADA e SUBSTITUÍDA por `D7` e `D8`**: `LIQ-001` e `GLB-006` iguais a 70; sete faixas por dezena; limiar de exceção formal em 50. A resolução anterior fixava 60 contra os documentos. |
| CONF-YIELD | Base do yield mínimo | Duas fontes fixam 0,80% mensal sobre o yield **bruto** · a especificação canônica interna anterior fixava sobre o **líquido** | **MANTIDA e detalhada por `D31`**: o piso decisório é 0,0080 sobre o yield **LÍQUIDO**, com a justificativa aritmética reescrita inline em `REN-009` e em `F.1.6`. `REN-002` permanece indicador informativo de yield bruto, sem efeito decisório. Marcado `[PENDENTE-CALIBRAÇÃO]`: um piso líquido de 0,80% ao mês equivale a 9,6% ao ano sobre o capital total e pode ser restritivo demais para o segmento. |
| CONF-DESCONTO | Sobrecarga do termo desconto | Três fontes usavam "desconto" para quatro grandezas diferentes, incluindo `PRI-003`, `PRI-004` e `PRI-005` | **MANTIDA.** Quatro definições distintas e nomeadas: desconto da fonte, desconto de mercado, desconto líquido e margem de segurança (`R27.1` a `R27.5`). Somente o desconto líquido é decisório. |
| CONF-DESCONTO-MIN | Desconto líquido mínimo | Cinco valores: 10%, 15%, 20%, 25% e 30% | **SUBSTITUÍDA por `D10`**: `PRI-005` igual a **0,15** como piso global, com os thresholds por estratégia prevalecendo quando mais restritivos. A resolução anterior fixava 0,10 e omitia os 30% de uma das fontes. |
| CONF-ESTRATEGIAS | O que é estratégia | Três fontes tratam apartamento, casa/sobrado e um dormitório como estratégias · o enum do código reconhece cinco estratégias | **MANTIDA e ampliada por `D42`**: estratégias de investimento e perfis de ativo são dimensões separadas (`R44.1`, `R44.2`), e as estratégias passam a **seis** com a inclusão de `customizada`, exigida por `P0-12`. |
| CONF-ESTADOS | Vocabulários de estado | Cinco vocabulários divergentes: 16 estados de negócio, estados em inglês, ciclos separados de captura e de imóvel, ciclo simplificado e outro conjunto de 16 estados | **MANTIDA e ampliada por `D47`.** Duas dimensões ortogonais: fase do pipeline (`PipelinePhase`, **16** valores após `D47`) e estado de decisão (`DecisionState`, 6 valores), mais dois ciclos de vida auxiliares para captura e imóvel. Todos declarados na Jornada Macro. |
| CONF-IDENTIDADE | Rótulos dos níveis de identidade | Fonte de captura: I0 desconhecido, I1 candidato, I2 provável, I3 confirmado, I4 documental · spec absorvida: I0 indefinida, I1 fraca, I2 provável, I3 forte, I4 plena | **MANTIDA e ampliada por `D35`.** Os rótulos da fonte de captura são adotados em `R7.1`, preservando a semântica da spec absorvida e a numeração da implementação; `D35` fecha a lacuna de `I3` e amplia `I4`. |
| CONF-PRECO-MAXIMO | Fórmula do preço máximo por ROI alvo | Forma fechada da planilha: R$ 168.374,76 · definição "ROI resultante igual ao ROI alvo" · implementação atual: R$ 163.352,38 | **MANTIDA na direção e CORRIGIDA por `D27` e `D28`.** A definição prevalece sobre a forma fechada, e o resultado correto é **R$ 182.158,03**, com o ITBI no coeficiente proporcional; o valor anterior de R$ 185.627,71 omitia o ITBI. A forma fechada da planilha passa a **referência informativa**, não a teto adicional garantido (`D28`). A propriedade `P7.1` é o oráculo. |
| CONF-IR | Tributação do ganho de capital | Planilha de referência: 15% linear · demais fontes: não especificam | **MANTIDA.** `CUS-013` igual a 0,15 como `[DEFAULT]` e simplificação declarada. Registrado em `PEND-IR`: modelar isenções e alíquotas progressivas de pessoa física. O IR sobre aluguel passa a `REN-012` `[PENDENTE-DECISÃO]` sem default numérico (`D13`). |
| CONF-CONTINGENCIA | Percentuais de contingência | Faixas qualitativas (menor, média, maior, muito maior) · sensibilidades de +10%, +25% e +50% | **CORRIGIDA por `D54`**: `CUS-017` é derivado das sensibilidades, porém o valor N2 = 0,15 é **interpolação** e `CUS-018` e `CUS-019` são derivações **sem sensibilidade documentada**; os três passam a `[PENDENTE-CALIBRAÇÃO]`. |
| CONF-FRESCOR | Prazos de frescor | Duas fontes declaram apenas sensibilidade qualitativa; uma delas declara matrícula como "até mudança ou evidência nova" | **MANTIDA e corrigida por `D48`.** Tabela FRESH com prazos numéricos `[DEFAULT-DERIVADO]` das classes qualitativas, **exceto** matrícula e documentação registral, que permanece não temporal com revalidação obrigatória antes da compra. |
| CONF-COMPARAVEIS | Quantidade mínima de comparáveis | `VAL-001` igual a 5 · material complementar: 7 a 10 · uma fonte admite 3 a 5 como base inicial razoável | **MANTIDA e corrigida por `D30`**: `VAL-001` igual a 5 como mínimo e `VAL-011` igual a **7** como limiar único do patamar ideal, não faixa. A base de 3 a 5 é coberta pela faixa de confiança 40–59. |
| CONF-CENARIOS | Conjunto de cenários | Duas fontes: conservador, base, otimista e venda rápida · duas outras: conservador, base, otimista e estressado | **MANTIDA.** Dois conjuntos com finalidades distintas: quatro referências de **valor** (`R23.1`) e quatro cenários **econômicos** (`R32.1`). Venda rápida é referência de valor; estressado é cenário econômico. |
| CONF-DECISAO-ROTULOS | Rótulos de decisão | Duas fontes em português (COMPRAR, COMPRAR SE, MONITORAR, NÃO COMPRAR, BLOQUEAR) · quatro em inglês (BUY, BUY IF, MONITOR, DO NOT BUY, BLOCK) · planilha de referência: vereditos A a E · documento de negócio: seis classificações com emoji | **MANTIDA.** Enum canônico em cinco estados, com mapeamento declarado para os vereditos A a E e para as classificações de exibição. |
| CONF-RISCO-MATRIZ | Matriz de severidade | Uma seção da fonte de risco lista cinco níveis incluindo informacional; outra define matriz 3 × 4 com quatro níveis | **MANTIDA.** Quatro níveis de severidade (`baixo`, `medio`, `alto`, `critico`) derivados da matriz de probabilidade × impacto. O nível informacional é tratado como registro sem severidade. |
| CONF-ESCOPO-JURIDICO | Automação jurídica | Documento de negócio: automação jurídica completa fora do foco · adendo do plano de MVP: validade jurídica como capacidade P0 | **MANTIDA — sem contradição, e assim registrado:** o Radar avalia a validade do procedimento com base em evidência documental fornecida, e não substitui parecer jurídico nem automatiza a coleta em cartórios e tribunais. |

## Pendências que permanecem

Permanecem apenas as pendências que **nenhuma fonte fixa** (`D54`). Para cada uma está
declarada a **regra de comportamento na ausência**: enquanto não decidida, o parâmetro não é
aplicado e o requisito dependente é reportado como **NÃO AVALIADO**, nunca como satisfeito.

### Pendências de decisão de negócio `[PENDENTE-DECISÃO]`

| ID | Pendência | Parâmetro | Comportamento enquanto pendente |
|----|-----------|-----------|---------------------------------|
| PEND-CIDADES | Cidades e regiões do piloto | `LOC-001` | Nenhuma restrição de cidade é aplicada; `R11` reporta a classe de localização como NÃO AVALIADA quando depender de lista vazia |
| PEND-PERFIS | Perfis de investimento habilitados | `INV-007`, estratégias ativas | Nenhuma estratégia é presumida ativa; `R44.3` reporta NÃO AVALIADO na ausência de estratégia ativa |
| PEND-REGIOES | Listas de regiões prioritárias, condicionais e bloqueadas | `LOC-003` a `LOC-006` | Sem lista, toda localização é classe `B`; `LOC-013` não é aplicado e `R11.4` é reportado como NÃO AVALIADO |
| PEND-PRECO-M2 | Preço por metro quadrado máximo absoluto | `PRI-008` | O limite não é aplicado; o critério de elegibilidade por preço por m² é reportado como NÃO AVALIADO |
| PEND-VALORIZACAO | Valorização histórica mínima regional e yield regional mínimo | `LOC-009`, `LOC-010` | Nenhum dos dois é aplicado; os critérios dependentes de `R45.3` são reportados como NÃO AVALIADOS |
| PEND-COMPRADORES | Quantidade mínima de compradores potenciais | `LIQ-005` | O limite não é aplicado; o componente de demanda de `R40.4` é reportado como NÃO AVALIADO |
| PEND-IR-ALUGUEL | Alíquota de IR sobre aluguel | `REN-012` | O imposto não é aplicado; o yield líquido é emitido como **provisório** e nunca como confirmado (`R27.7.2`) |
| PEND-LIQ-MODELO | Metodologia de cálculo do score de liquidez a partir de dados observáveis | `R40.3` | O score de liquidez é emitido como `indefinida` quando a metodologia não é aplicável aos dados disponíveis (`R40.6`) |

### Pendências de calibração `[PENDENTE-CALIBRAÇÃO]`

| ID | Pendência | Parâmetro | Comportamento enquanto pendente |
|----|-----------|-----------|---------------------------------|
| PEND-CALIBRACAO | Calibrar pesos do score, fatores de confiança e prazos de frescor após 10 a 20 análises reais | `SCORE-001`, `SCORE-002`, `SCORE-006`, `CONF-007`, FRESH | Os valores de fábrica são aplicados e marcados como não calibrados na explicação da decisão |
| PEND-CONTINGENCIA | `CUS-017` N2 = 0,15 é **interpolação** entre as sensibilidades de +10% e +25%; `CUS-018` e `CUS-019` iguais a 0,10 são **derivações sem sensibilidade documentada** | `CUS-017`, `CUS-018`, `CUS-019` | Os valores são aplicados e marcados como não calibrados; a contingência resultante é apresentada como faixa, não como número exato |
| PEND-YIELD | Reavaliar o piso de yield líquido mensal de 0,0080 após 10 a 20 análises reais. O piso equivale a 9,6% ao ano sobre o capital total e reprova o caso de prova `F.1` na estratégia de renda; é preciso confirmar se o patamar é alcançável no segmento e na faixa de ticket alvo, ou se o valor correto está entre 0,0050 e 0,0080 | `REN-009`, `STR` | O piso de 0,0080 é aplicado; a reprovação por yield é registrada com a marcação de piso não calibrado |

### Pendências de modelagem declaradas

| ID | Pendência | Observação |
|----|-----------|------------|
| PEND-IR | Modelar isenções e alíquotas progressivas de IR sobre ganho de capital de pessoa física | `CUS-013` igual a 0,15 permanece como simplificação `[DEFAULT]` declarada; o resultado é apresentado como estimativa tributária, não como apuração |

---

# Índice de Requisitos e Prioridade

Índice completo dos 83 requisitos com a capacidade do MVP a que cada um serve e a prioridade
atribuída conforme `R75.5` e `D36`. Esta é a tabela que torna a ordem de implementação
derivável do documento.

| Req. | Título | Capacidade | Prioridade |
|------|--------|-----------|------------|
| 1 | Gestão de fontes independentes | `P0-01` | P0 |
| 2 | Preservação da captura original | `P0-01` | P0 |
| 3 | Normalização sem invenção de dados | `P0-02` | P0 |
| 4 | Dados mínimos e gates de dados | `P0-02` | P0 |
| 5 | Enriquecimento progressivo | `P1` — mais automações | P1 |
| 6 | Conflitos entre fontes | `P0-05` | P0 |
| 7 | Resolução de identidade do imóvel | `P0-03` | P0 |
| 8 | Chave conceitual de identidade | `P0-03` | P0 |
| 9 | Deduplicação por força de evidência | `P0-04` | P0 |
| 10 | Perfil consolidado do imóvel | `P0-05` | P0 |
| 11 | Classificação de localização | `P0-05` | P0 |
| 12 | Precedência absoluta do gate jurídico | `P0-23` | P0 |
| 13 | Verificações registrais e de titularidade | `P0-23` | P0 |
| 14 | Constituição em mora e intimações | `P0-23` | P0 |
| 15 | Edital, cronologia e coerência do certame | `P0-23` | P0 |
| 16 | Processos judiciais e risco de nulidade | `P0-23` | P0 |
| 17 | Sinais jurídicos de investigação obrigatória | `P0-23` | P0 |
| 18 | Ocupação e posse como risco econômico | `P0-10` | P0 |
| 19 | Locação e efeitos perante o adquirente | `P0-10` | P0 |
| 20 | Evidência jurídica com proveniência obrigatória | `P0-19` | P0 |
| 21 | Seleção e qualificação de comparáveis | `P0-06` | P0 |
| 22 | Quantidade de comparáveis e confiança do valuation | `P0-07` | P0 |
| 23 | Faixas de valor e cenários de valuation | `P0-07` | P0 |
| 24 | Métodos de valuation por tipo de ativo | `P0-07` | P0 |
| 25 | Gatilhos de revaluation | `P0-22` | P0 |
| 26 | Custo econômico total | `P0-08` | P0 |
| 27 | Métricas econômicas determinísticas | `P0-09` | P0 |
| 28 | Preço máximo por estratégia | `P0-08` | P0 |
| 29 | Reforma, contingência e regularização | `P0-08` | P0 |
| 30 | Capital imobilizado e custo do tempo | `P0-08` | P0 |
| 31 | Financiamento | `P1` — comparação avançada | P1 |
| 32 | Cenários e sensibilidade | `P0-09` | P0 |
| 33 | Regras de decisão econômica | `P0-13` | P0 |
| 34 | Classificação de risco | `P0-10` | P0 |
| 35 | Risco versus incerteza | `P0-10` | P0 |
| 36 | Fases da Due Diligence | `P0-19` | P0 |
| 37 | Pendências | `P0-19` | P0 |
| 38 | Visita física | `P0-19` | P0 |
| 39 | Contexto humano e conforto pessoal | `P0-20` | P0 |
| 40 | Score de liquidez | `P0-11` | P0 |
| 41 | Preço e prazo de saída | `P0-11` | P0 |
| 42 | Estratégias de saída e operações híbridas | `P1` — mais estratégias | P1 |
| 43 | Monitoramento de liquidez | `P1` — monitoramento sofisticado | P1 |
| 44 | Estratégias simultâneas e aderência | `P0-12` | P0 |
| 45 | Critérios por estratégia | `P0-12` | P0 |
| 46 | Capital, reserva e limite por operação | `P0-15` | P0 |
| 47 | Concentração e diversificação | `P0-15` | P0 |
| 48 | Simulação de alocação antes da decisão | `P1` — comparação avançada de portfólio | P1 |
| 49 | Opportunity Score | `P0-14` | P0 |
| 50 | Confiança consolidada | `P0-14` | P0 |
| 51 | Investor Fit Score | `P0-15` | P0 |
| 52 | Score composto e ranking | `P0-16` | P0 |
| 53 | Precedência canônica de decisão | `P0-20` | P0 |
| 54 | Tipos de regra e resolução de conflitos | `P0-13` | P0 |
| 55 | Matriz de ação por score e confiança | `P0-20` | P0 |
| 56 | Explicabilidade obrigatória | `P0-17` | P0 |
| 57 | Monitoramento contínuo e materialidade | `P0-22` | P0 |
| 58 | Reentrada e abandono de tese | `P0-22` | P0 |
| 59 | Alertas acionáveis | `P1` — alertas avançados | P1 |
| 60 | Resultado real, backtest e aprendizado | `P1` — backtest ampliado | P1 |
| 61 | Snapshot imutável da análise | `P0-21` | P0 |
| 62 | Versionamento de regras e parâmetros | `P0-13` | P0 |
| 63 | Exceções auditáveis | `P0-13` | P0 |
| 64 | Trilha de auditoria | `P0-21` | P0 |
| 65 | Controle de qualidade das regras | `P1` — governança avançada | P1 |
| 66 | Navegação e visões do Radar | `P0-16` | P0 |
| 67 | Ficha da oportunidade | `P0-17` | P0 |
| 68 | Comparação, rejeição e monitoramento na interface | `P0-20` | P0 |
| 69 | Relatórios de negócio | `P1` — relatórios avançados | P1 |
| 70 | Orquestração com ordem obrigatória | `P0-13` | P0 |
| 71 | Guarda-corpos dos componentes de IA | `P0-17` | P0 |
| 72 | Ingestão de conhecimento e memória | `P2` — inteligência de documentos | P2 |
| 73 | Testes de invariantes e Golden Cases | `P0-13` | P0 |
| 74 | Entidades e campos obrigatórios do dicionário | `P0-05` | P0 |
| 75 | Escopo, priorização e controle de escopo | `P0-13` | P0 |
| 76 | Análise profunda | `P0-18` | P0 |
| 77 | Cenários como espaço de teste de premissas | `P0-09` | P0 |
| 78 | Configurações do investidor | `P0-12` | P0 |
| 79 | Interface de programação | `P0-16` | P0 |
| 80 | Qualidade de evidência e indicadores de aprendizado | `P1` — backtest ampliado | P1 |
| 81 | Alocação, eficiência de capital e faixas de ação | `P1` — comparação avançada de portfólio | P1 |
| 82 | Disciplina de lance e revalidação final | `P0-20` | P0 |
| 83 | Fronteira dos componentes de IA e intervenção humana | `P0-17` | P0 |

Contagem: **69 requisitos `P0`**, **13 requisitos `P1`**, **1 requisito `P2`**, nenhum fora do
MVP. Nenhum requisito desta spec é fora de escopo, porque os itens fora do MVP estão listados
em `R75.4` como exclusões e não como requisitos.

---

# Matriz de Rastreabilidade

| Domínio | Requisitos | Prioridade predominante | Regras canônicas | Checklist | Propriedades |
|---------|-----------|-------------------------|------------------|-----------|--------------|
| A — Fontes, Captura, Normalização | 1 a 6 | P0 (5 de 6) | RULE-ID-001 | MC-001 a MC-007 | P1, P2 |
| B — Identidade e Deduplicação | 7 a 11 | P0 | RULE-ID-001, RULE-ID-002, RULE-LOC-003, RULE-RSK-006 | MC-001 a MC-006, MC-008 a MC-016 | P3 |
| C — Gate Jurídico (camada 1) — **19 verificações** | 12 a 20 | P0 | RULE-JUR-001 a RULE-JUR-013, RULE-ED-001 a RULE-ED-004, RULE-ID-001, RULE-ID-002 | MC-008 a MC-043, MC-118 a MC-125, `B-01` a `B-16`, Anexo C.2 | P4, P5 |
| D — Mercado e Valuation | 21 a 25 | P0 | RULE-MKT-001 a RULE-MKT-004, RULE-RSK-007 | MC-070 a MC-076, `B-19` | P2.8, P6 |
| E — Economia e Rentabilidade | 26 a 33 | P0 (7 de 8) | RULE-FIN-001 a RULE-FIN-006, RULE-ED-003, RULE-RSK-004 | MC-064 a MC-069, MC-077 a MC-090, `B-15`, `B-18`, `B-22` | P6, P7, P8.1 a P8.3 |
| F — Risco e Due Diligence | 34 a 39 | P0 | RULE-OCC-001, RULE-OCC-002, RULE-LOC-001, RULE-LOC-002, RULE-JUR-007 a RULE-JUR-011, RULE-RSK-001 a RULE-RSK-010 | MC-035 a MC-063, `C-01` a `C-71`, `B-04` a `B-12` | P8.4 a P8.8 |
| G — Liquidez e Saída | 40 a 43 | P0 (2 de 4) | RULE-LIQ-001 a RULE-LIQ-003, RULE-FIN-005 | MC-091 a MC-098, `B-17`, `B-23`, `B-26` | P9 |
| H — Estratégias e Portfólio | 44 a 48 | P0 (4 de 5) | RULE-STR-001, RULE-STR-002, RULE-RSK-003, RULE-RSK-009 | MC-099 a MC-109, `B-24`, `B-27` | P10.5, P10.6, P10.17 |
| I — Score, Ranking, Decisão | 49 a 56 | P0 | RULE-SCR-001, RULE-SCR-002, RULE-DEC-001, RULE-DEC-002 | MC-110 a MC-117 | P10, P11 |
| J — Monitoramento e Aprendizado | 57 a 60 | P0 (2 de 4) | RULE-MON-001 | MC-136 | P13.1, P13.6 |
| K — Governança e Auditoria | 61 a 65 | P0 (4 de 5) | RULE-GOV-001, RULE-DEC-002, RULE-RSK-010 | MC-136 | P13 |
| L — Interface do Investidor | 66 a 69 | P0 (3 de 4) | RULE-DEC-002 | MC-115, MC-126 a MC-135 | exemplos dirigidos |
| M — Orquestração e Arquitetura de IA | 70 a 73 | P0 (3 de 4) | RULE-DEC-001, RULE-GOV-001 | Anexo E | P12, P15 |
| N — Dicionário, Escopo e Priorização | 74 a 83 | P0 (7 de 10) | RULE-GOV-001, RULE-ED-002, RULE-RSK-009 | `B-13`, `B-14`, Anexo C.2 a C.7 | P14, P16 |

**Disciplina de lance — rastreabilidade dos anexos `C.2` a `C.7`** (`D50`). Antes da
consolidação, nenhuma linha da matriz cobria esses anexos.

| Anexo | Conteúdo | Requisito | Propriedades |
|-------|----------|-----------|--------------|
| C.2 | 9 verificações de evicção `E01` a `E09` | `R82.4`, `R15.9` a `R15.9.2` | P14.4, P11.18 |
| C.3 | 9 hard stops `HS-01` a `HS-09` | `R82.1`, `R82.2` | P14.2 |
| C.4 | 12 itens pré-lance `PL-01` a `PL-12` | `R82.3` | P14.1 |
| C.5 | Dados do certame, comissão fora do lance e 6 verificações de histórico do leiloeiro `HL-01` a `HL-06` | `R82.7`, `R82.8`, `R82.9` | P14.6, P14.7 |
| C.6 | Disciplina de lance e tetos | `R82.6` | P14.3 |
| C.7 | 12 itens da revalidação final `RL-01` a `RL-12` | `R82.5`, `R82.6` | P14.5 |

## Definition of Done funcional

Uma capacidade é considerada funcionalmente pronta quando possui: requisito identificado
neste documento; módulo responsável; caso de uso quando aplicável; regras canônicas
associadas; parâmetros identificados com escopo e versão; fluxo ou tela definidos quando
houver interação; eventos relevantes definidos; critérios de aceitação testáveis; itens de
checklist mapeados; propriedades de correção associadas; tratamento de exceções; impacto
no histórico definido; e prioridade de release atribuída.

---

# Fora de Escopo Declarado

Para evitar ambiguidade na implementação, os itens abaixo estão explicitamente fora do
escopo deste documento.

| Item | Observação |
|------|------------|
| Coleta automatizada de fontes (varredura de portais, download de editais) | O payload bruto é entrada. O coletor será especificado separadamente. |
| Consulta automatizada a cartórios, tribunais, prefeituras e concessionárias | Os resultados dessas verificações são entradas do Gate_Juridico, vindas de documento ou de registro manual. |
| Execução automática de lance ou de arremate | Risco excessivo. O Radar apoia a disciplina de lance, sem executá-la. |
| Parecer jurídico, laudo de engenharia e contabilidade do imóvel | O Radar não substitui profissionais habilitados. |
| Garantia de valorização, liquidez ou rentabilidade | O Radar estima e explica; não garante resultado. |
| Automação integral da due diligence | A due diligence é assistida, com evidência e pendências registradas. |
| Aprendizado estatístico avançado e predição por modelos treinados | Depende de histórico real. Entra como evolução após o backtest. |
| Gestão patrimonial completa e contabilidade | Fora da tese central. |
| Marketplace e recursos colaborativos | Fora da tese central. |
| Aplicativo móvel completo | Não necessário para provar o valor do produto. |
| Operação em múltiplas instituições no MVP | A primeira fonte é a CAIXA; o modelo já nasce multi-fonte. |
| Definição da arquitetura de produção em nuvem | Local-first no MVP; produção apenas quando houver necessidade demonstrada. |
