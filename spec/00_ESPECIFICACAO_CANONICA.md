# Radar Imobiliário — Especificação Canônica (Fonte Única de Verdade)

Versão 1.0 · Base de reconciliação da documentação v1.1

Este documento resolve os conflitos identificados na análise dos 31 documentos de
negócio. Onde houver divergência entre documentos, **este documento prevalece**.
O código-fonte deve referenciar apenas os valores e definições daqui.

> Convenção de status de valor: `[CANÔNICO]` = decidido; `[DEFAULT]` = valor
> inicial parametrizável, sujeito a calibração; `[PENDENTE-CALIBRAÇÃO]` = precisa
> de histórico real para fixar.

---

## 1. Precedência de decisão (camada mestra)

Ordem única e definitiva. Uma camada só é avaliada se a anterior não eliminou a
oportunidade. Score **nunca** compensa uma camada de bloqueio.

| Nº | Camada | Função | Saída possível |
|----|--------|--------|----------------|
| 0 | **Validade jurídica do leilão** | Procedimento é juridicamente executável? | BLOCK / PENDENTE / OK |
| 1 | **Bloqueios críticos** | Risco jurídico/registral confirmado | BLOCK |
| 2 | **Elegibilidade** | Atende critérios mínimos (localização, tipo, ticket) | DO_NOT_BUY / OK |
| 3 | **Dados / Confiança** | Há evidência suficiente? | PENDENTE / OK |
| 4 | **Economia** | Há margem após custos? | DO_NOT_BUY / OK |
| 5 | **Estratégia** | Aderente ao objetivo do investidor? | DO_NOT_BUY / OK |
| 6 | **Score** | Quão atrativa é (0–100)? | ranking |
| 7 | **Cenário / Robustez** | Sobrevive ao cenário conservador? | BUY_IF / OK |
| 8 | **Ação** | Decisão final | BUY / BUY_IF / MONITOR / DO_NOT_BUY / BLOCK |

> Reconciliação: unifica as "8 camadas" do Doc 15 §3, os "11 níveis" do adendo v1.1
> e a "hierarquia de 10 camadas" do Doc 22. A validade jurídica é a camada 0 (P0).

---

## 2. Saídas de decisão (enum canônico)

| Código | Significado | Veredito Método Jabes equivalente |
|--------|-------------|-----------------------------------|
| `BUY` | Arrematar dentro do teto | A |
| `BUY_IF` | Arrematar sob condição/teto definido | B / D |
| `MONITOR` | Interessante, diligência incompleta | C |
| `DO_NOT_BUY` | Preço/estratégia não compensa | E (econômico) |
| `BLOCK` | Impedimento jurídico/crítico, não participar | E (jurídico) |

---

## 3. Estados de evidência (enum canônico)

Unifica Evidence Layer da arquitetura de IA com os tipos de informação dos Docs 5/6/24.

| Estado | Significado | Pode virar CONFIRMED? |
|--------|-------------|-----------------------|
| `OBSERVED` | Observado explicitamente numa fonte | — |
| `CONFIRMED` | Confirmado por evidência suficiente | — |
| `CALCULATED` | Derivado por cálculo determinístico | — |
| `ESTIMATED` | Estimativa com método declarado | Só com nova evidência |
| `INFERRED` | Inferência marcada como tal | Só com nova evidência |
| `UNKNOWN` | Não conhecido | Só com nova evidência |

Regras invioláveis:
- Nenhum agente cria evidência.
- `UNKNOWN` nunca vira `CONFIRMED` sem nova evidência.
- Ausência de documento **não** é regularidade → resultado `UNKNOWN`/`PENDENTE`.
- Custo/risco desconhecido **nunca** é tratado como zero.
- Contradições são preservadas, não sobrescritas.
- Memória histórica é contexto/hipótese, não evidência atual.

---

## 4. Score de oportunidade — bandas canônicas

Resolve o conflito entre Doc 1 (uma escala) e Docs 3/8 (outra escala). **Escala única:**

| Faixa | Classe | Rótulo |
|-------|--------|--------|
| 90–100 | 🔥 | Excepcional |
| 80–89 | 🟢 | Excelente |
| 70–79 | 🟡 | Muito boa |
| 60–69 | 🟠 | Interessante |
| 50–59 | ⚪ | Especulativa |
| < 50 | 🔴 | Fraca |

> Reconciliação: adota 6 faixas com granularidade fina. As bandas do Doc 1
> (80–89 verde) e dos Docs 3/8 (70–79 verde) são fundidas nesta escala única.
> Ranking usa o valor numérico (0–100), não a cor.

### 4.1 Pesos do Opportunity Score `[DEFAULT]`

Um único conjunto de pesos, aplicável ao score mestre. Substitui os pesos
divergentes dos Docs 15 e 18.

| Fator | Peso |
|-------|------|
| Desconto líquido | 25% |
| Margem de segurança | 20% |
| Liquidez | 15% |
| Localização | 15% |
| Risco | 10% |
| Yield / Renda | 5% |
| Valorização | 5% |
| Qualidade da oportunidade | 5% |
| **Total** | **100%** |

`[PENDENTE-CALIBRAÇÃO]` — recalibrar após 10–20 análises reais (regra de evolução
do Método Jabes).

### 4.2 Composição final

```
Score Final = Opportunity Score (0–100)
            × Fator de Confiança
            × Ajuste Estratégico (Investor Fit)
            × Ajuste de Capital / Concentração
```

- **Opportunity Score** mede a atratividade da oportunidade (§4.1).
- **Fator de Confiança** (§6) pondera pela qualidade da evidência.
- **Investor Fit** (§7) mede aderência ao investidor.
- Cálculo é determinístico (Calculation Engine), não decisão do LLM.

---

## 5. Fator de confiança — escala canônica

Unifica os três vocabulários encontrados (A–U; Muito alta→Inconclusiva;
Alta/Média/Baixa) numa escala única com fator multiplicativo.

| Faixa (0–100) | Rótulo | Fator | Ação típica |
|---------------|--------|-------|-------------|
| 90–100 | Muito alta | 1.00 | Decisão plena |
| 75–89 | Alta | 0.95 | Decisão com nota |
| 60–74 | Boa | 0.88 | Decisão com ressalva |
| 40–59 | Fraca | 0.75 | Tende a MONITOR/BUY_IF |
| 0–39 | Insuficiente | 0.60 | Não recomendar / PENDENTE |

Confiança mínima para BUY: `75` `[DEFAULT]`.

---

## 6. Liquidez — escala canônica

Resolve as duas escalas não reconciliadas (categórica vs 0–100). **A escala numérica
0–100 é canônica**; a categórica é derivada dela.

| Score (0–100) | Categoria derivada |
|---------------|--------------------|
| 80–100 | Alta |
| 60–79 | Média |
| 40–59 | Baixa |
| < 40 | Muito baixa |

Liquidez mínima para BUY: `60` (Média) `[DEFAULT]`.

---

## 7. Investor Fit — definição formal

Conceito usado no Checklist v1.1, Doc 21 e MVP, mas nunca definido. Definição canônica:

> **Investor Fit Score (0–100)**: mede quão bem uma oportunidade — já considerada boa
> em si (Opportunity Score) — atende ao perfil, estratégia, capital e restrições de
> concentração de um investidor específico.

Componentes `[DEFAULT]`:

| Componente | Peso | Fonte |
|------------|------|-------|
| Aderência à estratégia (renda/revenda/valorização/MCMV/terreno) | 35% | perfil × imóvel |
| Aderência de capital (ticket dentro da faixa e da reserva) | 30% | orçamento total, não só o lance |
| Concentração (geografia/tipo/estratégia/fonte) | 20% | portfólio atual |
| Aderência de risco (tolerância do investidor) | 15% | perfil de risco |

Regras:
- Investor Fit **não** pode transformar um `BLOCK` em `BUY`.
- Estouro de capital/reserva → `BLOCK` por capital (regra mais restritiva vence).
- O mesmo imóvel pode ter Fit diferente para investidores/estratégias diferentes.

---

## 8. Thresholds canônicos por estratégia `[DEFAULT]`

Resolve o "desconto mínimo" sobrecarregado (5 significados). **Definições fixas:**

- **Desconto sobre avaliação da fonte** = 1 − (preço / avaliação da fonte). *Informativo, nunca decisório.*
- **Desconto sobre valor de mercado** = 1 − (preço / valor de mercado provável).
- **Desconto líquido** = 1 − (custo econômico total / valor de mercado provável). *Este é o decisório.*
- **Margem de segurança** = (valor de mercado − custo econômico total) / valor de mercado.

| Estratégia | Desconto líquido mín. | Margem mín. | Yield líq. mín. (mês) | Liquidez mín. |
|------------|----------------------|-------------|-----------------------|---------------|
| Revenda | 25% | 20% | — | 60 |
| Renda | 15% | 10% | 0,80% | 60 |
| Valorização | 15% | 15% | — | 50 |
| MCMV | 20% | 15% | 0,80% | 60 |
| Terreno | 20% | 20% | — | 40 |

Desconto excepcional (aciona exceção auditável): `≥ 30%` `[DEFAULT]`.
Ticket padrão: `R$ 150.000 – R$ 250.000` `[DEFAULT]`.

---

## 9. Custo econômico total (fórmula canônica)

Determinística, executada pelo Calculation Engine. Baseada no financeiro do Método Jabes.

```
Custo econômico total (TCO aquisição) =
    lance/preço
  + comissão do leiloeiro (% sobre o preço)
  + ITBI (% sobre o preço)
  + registro/documentação
  + condomínio/débitos
  + tributos/débitos
  + reforma
  + reserva/imprevistos
  + custo jurídico esperado (custo potencial × probabilidade)
  + carrying (custo do tempo até a saída)
```

Fórmulas derivadas (todas determinísticas):

```
Desconto de mercado   = 1 − (preço / valor de mercado)
Desconto líquido      = 1 − (TCO / valor de mercado)
Margem                = valor de mercado − TCO
Margem %              = (valor de mercado − TCO) / valor de mercado
Yield mensal bruto    = aluguel mensal / TCO
Yield anual bruto     = yield mensal bruto × 12
Yield líquido mensal  = (aluguel − condomínio − IPTU − manutenção − vacância) / TCO
Preço máximo (por ROI alvo, backward) =
    resolve preço tal que ROI líquido resultante = ROI alvo da estratégia
```

Regra de ouro (Método Jabes): **o preço máximo é definido por risco, mercado e custo
total — nunca pela disputa.**

> `[PENDENTE]` IR sobre ganho de capital: modelar isenções e alíquotas progressivas
> de PF (o exemplo do Método Jabes usa 15% flat, que é simplificação).
