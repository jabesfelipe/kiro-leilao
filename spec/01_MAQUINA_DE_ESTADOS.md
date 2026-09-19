# Radar Imobiliário — Máquina de Estados Única da Oportunidade

Versão 1.0 · Reconciliação dos vocabulários de estado dos Docs 5, 7, 8, 10 e 25

Resolve a coexistência de três vocabulários de estado que misturavam fases de
pipeline com estados de negócio. Aqui há **duas dimensões ortogonais**:

1. **Fase do pipeline** (onde a oportunidade está no processamento) — determinística.
2. **Estado de decisão** (qual o veredito atual) — resultado do motor de decisão.

Uma oportunidade tem sempre uma fase e (a partir da decisão) um estado de decisão.

---

## 1. Princípio

> O imóvel é permanente; a oportunidade é dinâmica. Nada é destrutivo: cada mudança
> material gera um novo *snapshot* de análise (versão), preservando o histórico.

---

## 2. Fases do pipeline (enum `PipelinePhase`)

Sequência determinística de processamento. Cada fase produz evidências/cálculos.

| Ordem | Fase | Produz |
|-------|------|--------|
| 1 | `CAPTURED` | captura original preservada (fonte, hash, data) |
| 2 | `NORMALIZED` | dados normalizados |
| 3 | `IDENTIFIED` | identidade do imóvel (matrícula, endereço) |
| 4 | `DEDUPLICATED` | vínculo a imóvel único |
| 5 | `LEGAL_VALIDATED` | validade jurídica do leilão (gate P0) |
| 6 | `ENRICHED` | comparáveis, localização, contexto |
| 7 | `VALUATED` | valor de mercado + confiança |
| 8 | `COSTED` | custo econômico total |
| 9 | `SCORED` | opportunity score + investor fit |
| 10 | `RANKED` | posição no radar |
| 11 | `IN_ANALYSIS` | due diligence em curso |
| 12 | `DECIDED` | decisão registrada |
| 13 | `MONITORED` | acompanhamento contínuo |
| 14 | `CLOSED` | encerrada (arrematada, perdida, expirada) |

---

## 3. Estados de decisão (enum `DecisionState`)

Espelham as saídas canônicas (Especificação Canônica §2). Só existem a partir da
fase `DECIDED`.

```
BUY · BUY_IF · MONITOR · DO_NOT_BUY · BLOCK
```

Antes de `DECIDED`, o estado de decisão é `PENDING` (indefinido).

---

## 4. Transições de fase válidas

```
CAPTURED → NORMALIZED → IDENTIFIED → DEDUPLICATED → LEGAL_VALIDATED
    → ENRICHED → VALUATED → COSTED → SCORED → RANKED → IN_ANALYSIS
    → DECIDED → MONITORED → CLOSED

Atalhos de bloqueio (curto-circuito):
    LEGAL_VALIDATED --(BLOCK jurídico)--> DECIDED[BLOCK]
    IDENTIFIED      --(sem identidade)--> DECIDED[PENDING/DO_NOT_BUY]
    qualquer fase   --(mudança material)--> reabre análise (nova versão)

Reentrada:
    MONITORED --(gatilho: preço caiu / nova evidência)--> IN_ANALYSIS (nova versão)
    DECIDED[BUY_IF] --(condição satisfeita)--> IN_ANALYSIS → DECIDED
```

Regras:
- `LEGAL_VALIDATED` é obrigatório antes de `VALUATED`. Não se valora o que pode ser
  juridicamente nulo (adendo v1.1).
- Qualquer BLOCK jurídico leva direto a `DECIDED[BLOCK]`, sem passar por score.
- Reavaliação nunca sobrescreve: cria nova versão de análise (snapshot imutável).

---

## 5. Versionamento de análise (snapshots)

```
IMÓVEL
 └─ OPORTUNIDADE
     ├─ análise v1 → DECIDED[BUY_IF]   (2026-09-15)
     ├─ análise v2 → DECIDED[MONITOR]  (2026-09-20)
     └─ análise v3 → DECIDED[BLOCK]    (2026-09-29)
```

- Cada análise registra: fase final, estado de decisão, evidências usadas, regras
  aplicadas (com versão), cálculos, pendências, explicação e data.
- A análise atual é a de maior versão; as anteriores permanecem consultáveis.
- Histórico é contexto para a próxima análise, **não** vira verdade atual.

---

## 6. Mapa de reconciliação (de-para)

| Vocabulário antigo | Origem | Mapeado para |
|--------------------|--------|--------------|
| Captured/Qualified/Enriched/Valuated/Scored/Ranked | Doc 8/10 (inglês) | `PipelinePhase` |
| Normalizado/Valorado/Pontuado/Rankeado | Doc 7 (fases) | `PipelinePhase` |
| Aprovado/Bloqueado/Condicional/Rejeitado | Doc 7/8 (negócio) | `DecisionState` |
| BUY/BUY IF/MONITOR/DO NOT BUY/BLOCK | Doc 15/25/26 | `DecisionState` |
| Veredito A/B/C/D/E | Método Jabes | `DecisionState` (ver Canônica §2) |
