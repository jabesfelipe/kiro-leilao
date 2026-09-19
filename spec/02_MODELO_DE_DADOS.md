# Radar Imobiliário — Modelo de Dados

Versão 1.0 · Detalhamento das entidades da arquitetura §19 (PostgreSQL + pgvector)

Consolida o dicionário de entidades (Doc 6), a Evidence Layer (arquitetura §11),
o contrato canônico da análise (§16) e a máquina de estados (spec 01). É a fonte de
verdade para o schema SQL (`db/schema.sql`) e para os modelos SQLAlchemy.

---

## 1. Princípios de modelagem (não violar)

1. **Imóvel ≠ Oportunidade.** O imóvel físico é permanente; a oportunidade é
   dinâmica e pode reaparecer em vários leilões.
2. **Nada é destrutivo.** Captura original preservada; correção gera nova versão.
3. **Análise é snapshot imutável.** Uma nova análise cria nova versão; as anteriores
   não são sobrescritas.
4. **Toda evidência tem proveniência.** Fonte, documento, localização, estado e data.
5. **Fato ≠ interpretação.** O estado da evidência (OBSERVED/CONFIRMED/CALCULATED/
   ESTIMATED/INFERRED/UNKNOWN) é sempre explícito.
6. **Regras e parâmetros são versionados.** Cada análise referencia a versão vigente.
7. **Conhecimento (RAG) é separado dos dados transacionais.** Embeddings em pgvector;
   verdade estruturada em tabelas relacionais.

---

## 2. Mapa de entidades

```
FONTE ─┬─< CAPTURA >─┬─ IMÓVEL ─┬─< OPORTUNIDADE >─┬─< ANÁLISE (v1..vN) >
       │             │          │                  │        │
       │             │          ├─ property_ids    │        ├─< EVIDÊNCIA
       │             │          └─ comparáveis      │        ├─< FATO
       │             │                              │        ├─< CUSTO
       └─ DOCUMENTO ─┴─< DOCUMENT_CHUNK (pgvector)  │        ├─< VALUATION
                                                     │        ├─< CENÁRIO
                                                     │        ├─< RISCO
                                                     │        ├─< PENDÊNCIA
                                                     │        ├─ DECISÃO
                                                     │        └─< ANALYSIS_EVENT
                                                     └─< ALERTA

REGRA ─< RULE_VERSION        PARÂMETRO (hierárquico + versionado)
ESTRATÉGIA                   INVESTIDOR / PERFIL
```

---

## 3. Entidades (dicionário)

### 3.1 Fonte e captura

| Entidade | Descrição | Chaves/Notas |
|----------|-----------|--------------|
| `sources` | Origem dos dados (Caixa, leiloeiro, portal, cartório). | `source_type`, confiabilidade |
| `captures` | Snapshot bruto de uma coleta (preservado, imutável). | `hash`, `captured_at`, JSON cru |
| `documents` | Documento anexado (edital, matrícula, laudo). | `hash`, `mime`, origem |
| `document_chunks` | Pedaços do documento para RAG. | **embedding em pgvector** |

### 3.2 Imóvel e oportunidade

| Entidade | Descrição | Chaves/Notas |
|----------|-----------|--------------|
| `properties` | Imóvel físico único. | identidade via `property_identifiers` |
| `property_identifiers` | Identificadores do imóvel (matrícula, ID Caixa, endereço). | `type`, `value`, `confidence` |
| `opportunities` | Oferta comercial de um imóvel num leilão/momento. | FK `property_id`, estado |
| `comparables` | Comparáveis de mercado usados no valuation. | FK `analysis_id` |

### 3.3 Análise (snapshot imutável) e resultados

| Entidade | Descrição | Chaves/Notas |
|----------|-----------|--------------|
| `analyses` | Snapshot da análise (contrato canônico §16). | `version`, `analysis_date`, imutável |
| `evidences` | Evidências com proveniência (Evidence Layer). | `state`, `confidence`, `rule_refs` |
| `facts` | Fatos derivados/consolidados a partir de evidências. | `information_type` |
| `costs` | Componentes do custo econômico total. | 1:1 com análise |
| `valuations` | Valor de mercado por cenário + confiança. | conservador/base/otimista/rápida |
| `scenarios` | Cenários de tese (robustez). | conservador/base/otimista/estressado |
| `risks` | Riscos identificados. | `category`, `severity`, `state` |
| `pendings` | Pendências (podem bloquear BUY). | `blocks_buy` |
| `decisions` | Decisão final da análise. | `decision`, `deciding_layer` |
| `analysis_events` | Timeline de eventos/alterações da análise. | append-only |

### 3.4 Regras, parâmetros e estratégia

| Entidade | Descrição | Chaves/Notas |
|----------|-----------|--------------|
| `rules` | Regra canônica (RULE-JUR-002 etc.). | `code`, `domain`, `priority` |
| `rule_versions` | Versão vigente de uma regra. | `effective_from/to`, `approved_by` |
| `parameters` | Parâmetro configurável hierárquico. | `scope`, `key`, `value`, versão |
| `strategies` | Estratégia (renda, revenda, valorização, MCMV, terreno). | thresholds |
| `investors` | Investidor/perfil (capital, reservas, tolerância a risco). | portfólio |

### 3.5 Monitoramento

| Entidade | Descrição | Chaves/Notas |
|----------|-----------|--------------|
| `alerts` | Alerta acionável (impacto + próxima ação). | `priority`, `opportunity_id` |

---

## 4. Relacionamentos (cardinalidades)

- `sources` 1—N `captures` · `captures` N—1 `properties`
- `properties` 1—N `property_identifiers` · 1—N `opportunities`
- `opportunities` 1—N `analyses` (versões) · 1—N `alerts`
- `analyses` 1—N `evidences`, `facts`, `risks`, `pendings`, `comparables`,
  `scenarios`, `analysis_events`
- `analyses` 1—1 `costs`, `decisions`
- `analyses` 1—N `valuations` (uma por cenário)
- `documents` 1—N `document_chunks` · `documents` N—1 `sources`
- `rules` 1—N `rule_versions`
- `analyses` N—N `rule_versions` (via `rule_refs` nas evidências/decisão)

---

## 5. Decisões de modelagem

1. **`analyses.version`** é monotônica por `opportunity_id`. A "análise atual" é a de
   maior versão. Snapshots antigos permanecem consultáveis (regra 3).
   As FKs de exclusão em cadeia são `ON DELETE CASCADE` ao longo de
   `properties → opportunities → analyses → (evidences/costs/decisions/...)`, para
   que remover um imóvel/oportunidade de teste não deixe órfãos.
2. **Identidade do imóvel** não depende de uma única chave: `property_identifiers`
   guarda múltiplos identificadores com `confidence`. Matrícula é o mais forte;
   preço nunca prova identidade (Doc 16).
3. **Evidência é append-only**; contradições coexistem (não se apaga a anterior).
4. **`costs` embute o breakdown** do `CostBreakdown` (Canônica §9) em colunas, para
   auditoria; `total` é coluna gerada.
5. **Embeddings** ficam só em `document_chunks.embedding` (pgvector); nenhuma tabela
   transacional depende de vetor para funcionar.
6. **Parâmetros e regras versionados**: `analyses.rule_version` e
   `analyses.parameters_version` fixam o que valia na data da análise
   (reprodutibilidade, Doc 24).
7. **Enums do banco** espelham exatamente os enums de `src/radar/domain/enums.py`.
