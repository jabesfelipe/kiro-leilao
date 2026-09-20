# Radar Imobiliário

Plataforma de inteligência para leilões de imóveis. Transforma dados de
oportunidades (início: Caixa) em decisão de investimento explicável e auditável,
seguindo o Método Jabes e a arquitetura de IA (LangChain, LangGraph, RAG, MCP).

> Princípio central: **preço não é oportunidade**. A decisão vem de valor de
> mercado − custo econômico total − risco, com o preço máximo definido por risco,
> mercado e custo — nunca pela disputa.

## Documentos de especificação

A especificação está **congelada**. A fonte única de verdade é a spec
`radar-imobiliario-especificacao-completa`, em `.kiro/specs/`, composta de três documentos:

- **requirements.md** — fonte normativa de **negócio**: princípios invioláveis, glossário,
  os **126 requisitos** (`R1`–`R126`) com critérios de aceitação, as **104 decisões** de
  consolidação, o catálogo de 55 regras, os parâmetros e limiares, os 234 itens de checklist,
  os 4 Golden Cases e os 60 testes de regressão.
- **design.md** — fonte normativa de **engenharia**: arquitetura em núcleo, adaptadores e
  infraestrutura, os 49 componentes com assinaturas, o modelo físico de dados completo e as
  **262 propriedades** de correção executáveis, em 22 famílias.
- **tasks.md** — plano de execução: 46 tarefas de topo, 523 folhas executáveis e grafo de
  77 ondas, com 15 checkpoints como barreira de qualidade.

A spec é **autocontida**: nenhum artefato depende de leitura de documento fora dela. Todo o
material de origem — os 34 documentos de negócio, o Checklist Mestre, as matrizes de regras, a
Base de Conhecimento de IA, a planilha do Método Jabes, as especificações internas anteriores e
as revisões de arquitetura — foi auditado, absorvido e arquivado em `arquivo/`, que é memória
histórica e **não é fonte de trabalho**. Onde houver divergência, a spec prevalece.

O produto é **integralmente em português** (`D72`, `D103`), inclusive os identificadores de
implementação: módulos, tipos, funções, variáveis, tabelas, colunas e enums. Os módulos atuais
em inglês são renomeados pelas primeiras tarefas do plano. O meta-teste `MT-11` impede a
reintrodução de identificador em inglês.

O código deve refletir exatamente a spec, citando requisitos pelo número.

## Estrutura

```
src/radar/
  domain/          # enums, parâmetros e modelos canônicos (fonte de verdade em código)
    enums.py       # DecisionState, EvidenceState, DecisionLayer, PipelinePhase, Strategy
    parameters.py  # bandas de score, pesos, thresholds por estratégia [DEFAULT]
    models.py      # Evidence, CostBreakdown, AnalysisContract (contrato canônico §16)
  engines/         # motores DETERMINÍSTICOS (independentes do LLM)
    calculation.py # fórmulas: desconto líquido, margem, yield, preço máximo por ROI
    decision.py    # precedência canônica (camadas 0..8); BLOCK nunca é compensado
  orchestration/
    graph.py       # esqueleto do grafo LangGraph (fluxo da arquitetura §6)
  services/
    analysis_service.py  # orquestra motores + contrato + persistência (ponta a ponta)
  db/
    models.py      # modelos ORM (SQLAlchemy 2.0) espelhando db/schema.sql
    repository.py  # persiste AnalysisContract como snapshot; grava decisão/custo
    session.py     # engine + sessão
  api/
    main.py        # FastAPI: /health, /analysis/decision, /analysis/run
  config.py        # settings (LLM/banco desacoplados por env)
db/
  schema.sql       # schema PostgreSQL + pgvector (24 tabelas, enums, seed)
tests/             # 18 testes; Golden Cases (Método Jabes item 227, BLOCK jurídico)
```

## Modelo de dados

A especificação do modelo físico está na seção *Data Models* do `design.md` da spec.
O schema físico está em `db/schema.sql` e os modelos ORM em `src/radar/db/models.py`.
Embeddings ficam em `document_chunks.embedding` (pgvector, dim 1536); a verdade
estruturada e o histórico ficam nas tabelas relacionais.

## Princípios de arquitetura (não violar)

- O LLM **não** substitui regras determinísticas nem cálculos financeiros.
- Nenhum agente cria evidência nem transforma `UNKNOWN` em `CONFIRMED`.
- `BLOCK` jurídico não é superado por desconto, score ou rentabilidade.
- Ausência de evidência não é regularidade (`UNKNOWN`/`PENDENTE`).
- Toda análise é um snapshot imutável; histórico é contexto, não verdade atual.

## Rodando

```bash
python -m pip install -e ".[dev]"
python -m pytest                                    # roda os testes (inclui Golden Cases)
uvicorn radar.api.main:app --reload --app-dir src   # sobe a API
```

### Banco de dados (Postgres 16 + pgvector via Docker)

Ambiente local, idêntico em qualquer máquina. Configuração via `.env`
(copie de `.env.example`).

```bash
# 1) sobe o container e habilita a extensão pgvector (rodar no WSL)
bash scripts/wsl_db_up.sh

# 2) aplica o schema (idempotente) e valida
python scripts/db_check.py         # conexão + pgvector + schema
python scripts/db_setup.py         # cria schema poc_ia, 24 tabelas e seed
python scripts/db_setup.py --drop  # recria do zero

# 3) smoke tests
python scripts/db_smoke.py         # ciclo transacional: persiste o Golden Case item 227
python scripts/db_smoke_vector.py  # pgvector: grava embeddings e valida ranking
python scripts/db_cleanup.py       # remove dados de smoke test
```

Notas:
- Objetos ficam no schema `poc_ia` (configurável em `RADAR_DB_SCHEMA`).
- O usuário `radar` é superuser no container, então `CREATE EXTENSION vector`
  funciona. Em **RDS** isso exige `rds_superuser`; sem ele o `db_setup.py` cria
  tudo menos a coluna `embedding` e converge depois (adiciona a coluna e o índice
  quando a extensão existir). O núcleo transacional não depende de pgvector.
- **Docker via snap (WSL)**: o snap não cria o grupo `docker` nem expõe `/snap/bin`
  em shells não-login. Se der "permission denied" no socket:
  `sudo addgroup --system docker && sudo adduser $USER docker && sudo snap disable docker && sudo snap enable docker`,
  depois `wsl --shutdown`. O snap também é confinado e não faz bind mount de
  `/mnt/c`, por isso o schema é aplicado via `db_setup.py` em vez de initdb.
- **Banco remoto em VPC privada**: se o hostname não resolver por DNS público mas
  o IP privado for alcançável (VPN), defina `RADAR_DB_HOST_ADDR=<ip>` no `.env`.

## Estado atual (MVP — fatia vertical)

Implementado e testado ponta a ponta (18 testes):
- Enums, parâmetros e modelos canônicos (fonte de verdade em código).
- **Calculation Engine** — fórmulas determinísticas, validadas contra os números
  reais da planilha Método Jabes (item 227: TCO R$ 228.066,90).
- **Decision Engine** — precedência canônica completa (camadas 0..8); BLOCK nunca
  compensado por score.
- **Analysis Service** — orquestra cálculo → decisão → contrato → explicação.
- **Persistência** — schema PostgreSQL+pgvector, ORM e repositório que grava cada
  análise como snapshot imutável versionado.
- **API** — `/analysis/run` executa a análise ponta a ponta.

Pendente (esqueleto): nós do grafo LangGraph que dependem de LLM/RAG/tools MCP
(captura Caixa, extração de documentos, comparáveis de mercado). Eles alimentam as
entradas do Analysis Service, mas não substituem regras nem cálculos (arquitetura §2).

A recomendação da análise permanece: começar por **uma oportunidade real da Caixa**
percorrendo Fonte → Validade Jurídica → Valuation → Economia → Decisão.
