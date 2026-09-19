# Radar Imobiliário

Plataforma de inteligência para leilões de imóveis. Transforma dados de
oportunidades (início: Caixa) em decisão de investimento explicável e auditável,
seguindo o Método Jabes e a arquitetura de IA (LangChain, LangGraph, RAG, MCP).

> Princípio central: **preço não é oportunidade**. A decisão vem de valor de
> mercado − custo econômico total − risco, com o preço máximo definido por risco,
> mercado e custo — nunca pela disputa.

## Documentos de especificação

A fonte única de verdade vive em `spec/`:

- `spec/00_ESPECIFICACAO_CANONICA.md` — reconcilia os conflitos da documentação v1.1
  (bandas de score, thresholds, escalas de confiança/liquidez, Investor Fit, fórmulas).
- `spec/01_MAQUINA_DE_ESTADOS.md` — máquina de estados única (fase de pipeline ×
  estado de decisão), resolvendo os três vocabulários de estado divergentes.

O código em `src/radar/domain` deve refletir exatamente essas specs.

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

Especificação em `spec/02_MODELO_DE_DADOS.md` (22+ entidades da arquitetura §19).
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
