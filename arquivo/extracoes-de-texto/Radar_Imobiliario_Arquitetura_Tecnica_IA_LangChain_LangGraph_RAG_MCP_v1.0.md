# Radar_Imobiliario_Arquitetura_Tecnica_IA_LangChain_LangGraph_RAG_MCP_v1.0

RADAR IMOBILIÁRIO
Arquitetura Técnica de IA — LangChain, LangGraph, RAG, MCP e Memória Histórica
Versão 1.0 • Base oficial da documentação técnica de arquitetura • 17/09/2026
Status: APROVADA PARA IMPLEMENTAÇÃO

# 1. Objetivo

Consolidar as decisões técnicas e arquiteturais para transformar o Radar Imobiliário em uma plataforma de inteligência imobiliária orientada por IA. A documentação funcional anterior continua sendo a fonte de verdade para regras de negócio, critérios, checklist e estratégias; este documento traduz essas decisões para uma arquitetura executável.

# 2. Princípios arquiteturais

- Identificar oportunidades reais ajustadas por mercado, custos, risco, liquidez e estratégia — não apenas imóveis baratos.
- Separar fatos, evidências, conhecimento, inferências, cálculos e decisões.
- LLM não substitui regras determinísticas nem cálculos financeiros.
- Nenhum agente cria evidência ou transforma UNKNOWN em CONFIRMED.
- BLOCK jurídico não pode ser superado por desconto, score ou rentabilidade.
- Toda conclusão relevante é rastreável às evidências e regras utilizadas.
- Histórico de análises é reutilizável como contexto, mas não vira verdade atual automaticamente.
- Arquitetura local-first no MVP, com evolução posterior.
- Modular monolith inicialmente; distribuir componentes somente com justificativa.
- Tudo relevante deve ser parametrizado e versionado.

# 3. Stack decidida


| Camada | Decisão | Motivo |
|---|---|---|
| Linguagem | Python 3.12+ | Ecossistema de IA, RAG, documentos, avaliação e agentes. |
| Agentes/integrações | LangChain | Modelos, prompts, retrievers, tools e ecossistema. |
| Orquestração | LangGraph | Estado, branches, ciclos, checkpoints e human-in-the-loop. |
| LLM | OpenAI API | Primeiro provedor, desacoplado por configuração. |
| Banco | PostgreSQL | Fonte estruturada de verdade e histórico. |
| Vetorial | pgvector | Busca semântica sem adicionar infraestrutura no MVP. |
| API | FastAPI | API Python tipada e simples. |
| Contratos | Pydantic | Contratos explícitos entre componentes. |
| Documentos | PyMuPDF + OCR quando necessário | Extração e preservação de origem. |
| Tools | MCP | Capacidades controladas para os agentes. |
| Testes | pytest + Golden Cases + regressão | Confiabilidade. |
| Infra | Docker/local-first | Custo inicial próximo de zero. |


# 4. Visão de alto nível

USUÁRIO
  ↓
LANGGRAPH / ORQUESTRADOR
  ↓
┌──────────────┬───────────────┬──────────────┐
│ RAG          │ MEMÓRIA       │ MCP / TOOLS  │
│ conhecimento │ histórico     │ dados/fontes │
└──────┬───────┴───────┬───────┴───────┬──────┘
       └───────────────┼───────────────┘
                       ↓
              AGENTES ESPECIALISTAS
                       ↓
                 EVIDENCE LAYER
                       ↓
                  RULE ENGINE
                       ↓
               CALCULATION ENGINE
                       ↓
                 DECISION ENGINE
                       ↓
                EXPLAINABILITY
                       ↓
               PERSISTÊNCIA
                  ↙          ↘
            PostgreSQL     pgvector

# 5. Responsabilidade dos componentes


| Componente | Faz | Não faz |
|---|---|---|
| LangGraph | Orquestra workflow e estado | Substituir regras de negócio. |
| LangChain | Integra LLM, prompts, retrievers e tools | Ser fonte de verdade do domínio. |
| RAG | Recupera conhecimento | Decidir sozinho ou provar fato atual. |
| Agentes | Interpretam e investigam | Inventar evidência ou superar BLOCK. |
| MCP/Tools | Executam capacidades controladas | Decidir sem contrato. |
| Evidence Layer | Guarda proveniência | Inferir fatos. |
| Rule Engine | Executa regras determinísticas | Interpretar livremente documentos. |
| Calculation Engine | Executa cálculos | Tomar decisão jurídica. |
| Decision Engine | Aplica precedência | Inventar dados. |
| PostgreSQL | Dados estruturados e histórico | Substituir busca semântica. |
| pgvector | Busca semântica | Ser banco transacional. |


# 6. LangGraph

LangGraph será o núcleo de orquestração. A análise será um grafo com estado, nós, condicionais, possibilidade de investigação adicional, bloqueios, pendências e reanálises.
START
 → carregar_imovel
 → carregar_contexto
 → identidade
 → evidências_juridicas
      ├─ BLOCK → decisão
      └─ continuar
 → edital
 → ocupação
 → mercado
 → economia
 → liquidez
 → estratégia
 → regras
 → decisão
 → explicação
 → persistência
 → memória
 → END
O estado compartilhado é a comunicação entre agentes; não haverá uma cadeia descontrolada de agentes conversando por texto.

# 7. Agentes


| ID | Agente | Responsabilidade |
|---|---|---|
| AG-00 | Orquestrador | Coordenar análise. |
| AG-01 | Captura & Identidade | Normalizar e identificar imóvel. |
| AG-02 | Documentos | Extrair/classificar/localizar evidências. |
| AG-03 | Jurídico | Analisar cadeia registral e requisitos. |
| AG-04 | Edital | Ler edital e obrigações. |
| AG-05 | Mercado & Valuation | Comparáveis e valor de mercado. |
| AG-06 | Ocupação & Locação | Ocupação, terceiros e contratos. |
| AG-07 | Economia | TCO, margem, retorno e cenários. |
| AG-08 | Liquidez | Demanda, venda e aluguel. |
| AG-09 | Estratégia | Fit com estratégia e capital. |
| AG-10 | Decisão | Consolidar regras e decisão. |
| AG-11 | Explicabilidade | Justificativa rastreável. |
| AG-12 | Monitoramento | Mudanças e reanálise. |

No MVP, os agentes são módulos Python dentro de um modular monolith, não 13 microserviços.

# 8. RAG e ingestão documental

DOCUMENTO
 → hash/fingerprint
 → catálogo/fonte
 → extração/OCR
 → limpeza
 → classificação
 → chunking semântico
 → metadata
 → embedding
 → PostgreSQL + pgvector
Todo documento novo passa pela mesma pipeline. Não será considerado conhecimento apenas por estar em uma pasta.

## 8.1 Tipos de conhecimento


| Tipo | Exemplo | Tratamento |
|---|---|---|
| REGRA | RULE-JUR-002 | Versionada e prioritária. |
| DEFINIÇÃO | Conceito jurídico | Conhecimento. |
| FÓRMULA | Net discount | Execução preferencial no Calculation Engine. |
| CHECKLIST | JUR-CHK-009 | Mapeado para regra canônica. |
| EVIDÊNCIA | AV-13 da matrícula | Estruturada + referência documental. |
| CASO | Ouro Verde | Memória histórica, não verdade atual. |
| ANÁLISE | Milano — 17/09/2026 | Histórico + contexto semântico. |
| MANUAL/LIVRO | Material de estudo | Conhecimento contextual. |


## 8.2 Metadata

document_id
section_id
chunk_id
tipo
dominio
topic
rule_id
strategy
source_type
source_id
version
effective_from
effective_to
priority
entity_type
jurisdiction
confidence
created_at

# 9. Base de conhecimento

A base receberá os documentos funcionais já produzidos, a Base de Conhecimento IA v1.2, a Matriz Canônica de 45 regras, o checklist de 163 checks, os casos de prova e novos materiais.
- Leis e jurisprudência
- Editais e documentos CAIXA
- Matrículas e certidões
- Laudos e avaliações
- Comparáveis e mercado
- Manuais e livros autorizados
- Novas análises e casos históricos
- Documentos futuros adicionados pelo usuário

# 10. Memória híbrida

Teremos três camadas.

| Memória | Onde | Finalidade |
|---|---|---|
| Conhecimento | pgvector + PostgreSQL | Regras, leis, manuais, conceitos e casos. |
| Histórico | PostgreSQL | Cada análise, decisão, alteração e evento. |
| Contexto do imóvel | PostgreSQL + pgvector | Histórico específico e casos semelhantes. |

Cada análise será um snapshot imutável. Uma nova análise cria nova versão; análises anteriores não são sobrescritas.
IMÓVEL
 ├─ análise v1 → BUY IF
 ├─ análise v2 → MONITOR
 ├─ análise v3 → BUY IF
 └─ análise v4 → BLOCK
Na próxima análise, o sistema recupera análises anteriores, decisões, pendências, evidências recentes, alterações e casos semelhantes. Histórico é contexto/hipótese, não evidência atual.

# 11. Evidence Layer

Evidencia:
 evidence_id
 source_id
 source_type
 document_id
 location
 fact
 value
 information_type
 identity_level
 confidence
 observed_at
 extracted_at
 created_by
 rule_refs

| Tipo | Significado |
|---|---|
| OBSERVED | Observado explicitamente. |
| CONFIRMED | Confirmado por evidência suficiente. |
| CALCULATED | Derivado por cálculo. |
| ESTIMATED | Estimativa. |
| INFERRED | Inferência. |
| UNKNOWN | Não conhecido. |

- Agente nunca cria evidência.
- UNKNOWN não vira CONFIRMED sem nova evidência.
- Inferência é marcada como inferência.
- Toda evidência possui origem.
- Contradições são preservadas.
- Evidência atual não é substituída por memória histórica.

# 12. MCP / Tools


| Tool | Função |
|---|---|
| tool.property.get | Obter imóvel e identificadores. |
| tool.source.capture | Capturar fonte. |
| tool.document.extract | Extrair documento. |
| tool.registry.lookup | Consultar registro/matrícula. |
| tool.court.search | Pesquisar processos. |
| tool.auction.get | Obter leilão/editais. |
| tool.market.search | Buscar comparáveis. |
| tool.location.analyze | Analisar localização. |
| tool.debt.lookup | Consultar débitos. |
| tool.valuation.calculate | Executar valuation. |
| tool.economics.calculate | Executar TCO/cenários. |
| tool.rules.evaluate | Executar regras. |
| tool.decision.evaluate | Aplicar decisão. |
| tool.evidence.store | Persistir evidência. |


# 13. Rule Engine

As 163 verificações funcionais são normalizadas nas regras canônicas já definidas. O motor é independente do prompt do LLM.
P0 bloqueios jurídicos/registrários
P1 identidade/eligibilidade
P2 qualidade/confiança
P3 economia
P4 estratégia
P5 score/Investor Fit
P6 cenários
P7 ação
BLOCK jurídico não pode ser compensado por score, desconto ou yield.

# 14. Calculation Engine

Cálculos críticos serão determinísticos.
Desconto de mercado = 1 - preço / valor de mercado

Custo econômico total =
aquisição + comissão + tributos/custos + débitos
+ regularização + reforma + carrying
+ financiamento + saída + contingência

Desconto líquido = 1 - TCO / valor de mercado
Margem = valor de mercado - TCO
Margem % = (valor de mercado - TCO) / valor de mercado
Yield mensal bruto = aluguel mensal / TCO
Yield anual bruto = yield mensal × 12

# 15. Decision Engine

BLOCK
BUY
BUY_IF
MONITOR
DO_NOT_BUY
A decisão aponta para evidências, regras, cálculos, estratégia, versão e pendências.

# 16. Contrato canônico da análise

{
  property_id,
  identity_confidence,
  legal_status,
  legal_evidence,
  occupancy_status,
  market_value,
  economic_cost,
  net_discount,
  margin,
  liquidity_score,
  strategy,
  opportunity_score,
  investor_fit,
  confidence,
  risks,
  pending,
  decision,
  explanation,
  next_actions,
  rule_version,
  analysis_date
}

# 17. Score e confiança

Opportunity Score mede oportunidade; confidence mede qualidade/solidez da informação. Os dois permanecem separados.

| Componente | Peso ilustrativo |
|---|---|
| Desconto líquido | 25% |
| Margem de segurança | 20% |
| Liquidez | 15% |
| Localização | 15% |
| Risco | 10% |
| Renda/Yield | 5% |
| Apreciação | 5% |
| Qualidade da oportunidade | 5% |


# 18. Estratégias

Estratégias são configurações: renda, revenda, valorização, MCMV/baixa renda, terreno, apartamento, casa/sobrado e 1 quarto. O mesmo imóvel pode gerar decisões diferentes conforme a estratégia.

# 19. Modelo de dados

PostgreSQL
 ├─ properties
 ├─ property_identifiers
 ├─ sources
 ├─ documents
 ├─ document_chunks
 ├─ evidences
 ├─ facts
 ├─ analyses
 ├─ analysis_events
 ├─ decisions
 ├─ risks
 ├─ pendings
 ├─ comparables
 ├─ valuations
 ├─ costs
 ├─ scenarios
 ├─ strategies
 ├─ rules
 ├─ rule_versions
 ├─ parameters
 └─ alerts

pgvector
 └─ embeddings / chunks / memória semântica

# 20. Fluxo completo

USUÁRIO
 ↓
LangGraph
 ↓
identificar imóvel
 ↓
dados atuais + histórico + evidências
 ↓
RAG
 ↓
Jurídico → Edital → Ocupação → Mercado
 ↓
Economia → Liquidez → Estratégia
 ↓
Rule Engine → Calculation Engine → Decision Engine
 ↓
Explainability
 ↓
salvar análise + timeline
 ↓
indexar resumo para memória semântica
 ↓
resultado

# 21. Caso de prova — Residencial Milano


| Campo | Valor |
|---|---|
| Property ID | 855553513794-2 |
| Matrícula | 71502 |
| Avaliação | R$ 230.000 |
| 2º leilão | R$ 138.000 |
| Consolidação | 31/07/2026 |
| Matrícula emitida | 03/08/2026 |
| Leilões negativos | Não se aplica |
| Referência funcional | BUY IF / PENDING |
| Confiança referência | ~78% |

O Golden Case deve validar que consolidação confirmada não implica automaticamente que todas as notificações estejam comprovadas. Ocupação e débitos dependem de evidência.

# 22. Casos Golden adicionais

Reserva dos Pinhais: validar consolidação, matrícula desatualizada frente à data da análise e averbação de leilões negativos em tratamento, sem BLOCK automático.
Ouro Verde: validar leitura do ato de consolidação com menção à regularidade da intimação, distinguir gravame histórico cancelado de gravame atual e não aceitar avaliação CAIXA automaticamente como valor de mercado.

# 23. Evaluation


| Teste | Objetivo |
|---|---|
| Golden Case | Garantir comportamento em casos conhecidos. |
| Regression | Detectar mudanças indesejadas. |
| Evidence invariant | Impedir evidência inventada. |
| UNKNOWN invariant | Impedir confirmação sem prova. |
| BLOCK invariant | Impedir score de superar bloqueio. |
| Traceability | Decisão ligada a evidências/regras. |
| Temporal consistency | Histórico não vira fato atual. |
| Calculation tests | Garantir cálculos determinísticos. |


# 24. Observabilidade

analysis_run_id
property_id
graph_version
agent
node
model
prompt_version
tool
input_hash
output_hash
latency
tokens
retrievals
evidence_ids
rule_ids
errors
decision
created_at

# 25. Reprodutibilidade

Cada análise registra versão do grafo, modelo, prompt, regras, parâmetros, conhecimento/evidências utilizados, estratégia, data e resultado.
ANÁLISE
 ├─ graph_version
 ├─ model_version
 ├─ prompt_version
 ├─ rule_version
 ├─ parameter_version
 ├─ knowledge_snapshot
 └─ evidence_snapshot

# 26. Segurança contra alucinação

- Não afirmar consulta a fonte não consultada.
- Não preencher lacunas jurídicas com suposição.
- Não ocultar conflitos entre fontes.
- Não usar score para ultrapassar BLOCK.
- Ausência de informação não significa regularidade.
- Informar pendências que podem invalidar a tese.
- Separar fato, inferência, estimativa e cálculo.
- Indicar dependência de legislação/jurisprudência vigente.

# 27. Estrutura do projeto

radar-ai/
├─ app/
│  ├─ agents/
│  ├─ rag/
│  ├─ mcp/
│  ├─ rules/
│  ├─ calculations/
│  ├─ evidence/
│  ├─ decision/
│  ├─ models/
│  ├─ schemas/
│  └─ api/
├─ data/{raw,processed,evidence,knowledge}
├─ evaluation/{golden_cases,regression}
├─ tests/
├─ docker/
├─ scripts/
├─ pyproject.toml
├─ docker-compose.yml
└─ README.md

# 28. Roadmap técnico

- Fase 1 — Fundação: Python, Docker, PostgreSQL, pgvector, Pydantic.
- Fase 2 — Domínio: entidades, evidências, regras, cálculos e decisão.
- Fase 3 — RAG: ingestão, chunking, embeddings e retrieval.
- Fase 4 — LangChain: LLM, prompts, retrievers e tools.
- Fase 5 — LangGraph: state, nodes, branches e checkpoints.
- Fase 6 — MCP: ferramentas controladas.
- Fase 7 — Agentes especialistas.
- Fase 8 — Memória histórica e timeline.
- Fase 9 — Evaluation e regressão.
- Fase 10 — FastAPI/UI.
- Fase 11 — Produção/cloud somente quando houver necessidade.

# 29. ADRs iniciais

- ADR-001 — Python para a camada de IA.
- ADR-002 — LangChain + LangGraph.
- ADR-003 — PostgreSQL + pgvector.
- ADR-004 — Memória híbrida: histórico estruturado + memória semântica.
- ADR-005 — Modular monolith no MVP.
- ADR-006 — LLM não decide regra crítica sozinho; regras e cálculos permanecem determinísticos.

# 30. Checklist de prontidão

- ☐ Python + Docker
- ☐ PostgreSQL + pgvector
- ☐ Pydantic schemas
- ☐ Evidence / Fact / Analysis
- ☐ Rule Engine
- ☐ Calculation Engine
- ☐ Decision Engine
- ☐ Pipeline documental
- ☐ Embeddings + Retriever
- ☐ LangChain
- ☐ LangGraph State
- ☐ MCP inicial
- ☐ Golden Cases
- ☐ Persistência de análise
- ☐ Timeline
- ☐ Memória semântica
- ☐ Testes de invariantes
- ☐ Observabilidade

# 31. Definição oficial

O Radar Imobiliário será uma plataforma de inteligência imobiliária com arquitetura híbrida de IA e software determinístico. LangGraph coordena agentes e workflows; LangChain fornece componentes de LLM, recuperação e ferramentas; RAG fornece conhecimento contextual; MCP fornece capacidades controladas; PostgreSQL armazena a verdade estruturada e o histórico; pgvector fornece memória semântica; Evidence Layer garante rastreabilidade; Rule Engine e Calculation Engine garantem determinismo; Decision Engine aplica precedência; e Human-in-the-loop atua como mecanismo de segurança.
A arquitetura aceita ingestão contínua de documentos e transforma análises concluídas em histórico reutilizável, mantendo separação entre conhecimento normativo, evidência atual e experiência histórica.
Esta versão é a base oficial da documentação técnica de arquitetura. Alterações estruturais relevantes devem ser registradas por ADR.
