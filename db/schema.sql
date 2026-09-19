-- Radar Imobiliário — Schema PostgreSQL + pgvector
-- Fonte de verdade: spec/02_MODELO_DE_DADOS.md
-- Enums espelham src/radar/domain/enums.py. Dimensão de embedding: 1536 (text-embedding-3-small).
--
-- Portável: roda no RDS provisório e no Postgres local. Objetos ficam no schema poc_ia.
-- Se preferir outro schema, ajuste RADAR_DB_SCHEMA e rode via scripts/db_setup.py.

CREATE SCHEMA IF NOT EXISTS poc_ia;
SET search_path TO poc_ia, public;

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;  -- gen_random_uuid()

-- ---------------------------------------------------------------------------
-- Tipos enumerados (espelham os enums do domínio)
-- ---------------------------------------------------------------------------
CREATE TYPE decision_state AS ENUM
    ('BUY', 'BUY_IF', 'MONITOR', 'DO_NOT_BUY', 'BLOCK', 'PENDING');

CREATE TYPE evidence_state AS ENUM
    ('OBSERVED', 'CONFIRMED', 'CALCULATED', 'ESTIMATED', 'INFERRED', 'UNKNOWN');

CREATE TYPE pipeline_phase AS ENUM
    ('CAPTURED', 'NORMALIZED', 'IDENTIFIED', 'DEDUPLICATED', 'LEGAL_VALIDATED',
     'ENRICHED', 'VALUATED', 'COSTED', 'SCORED', 'RANKED', 'IN_ANALYSIS',
     'DECIDED', 'MONITORED', 'CLOSED');

CREATE TYPE strategy AS ENUM
    ('revenda', 'renda', 'valorizacao', 'mcmv', 'terreno');

CREATE TYPE legal_status AS ENUM ('OK', 'PENDENTE', 'BLOCK');

CREATE TYPE risk_severity AS ENUM ('baixo', 'medio', 'alto', 'critico');

CREATE TYPE scenario_kind AS ENUM ('conservador', 'base', 'otimista', 'estressado', 'venda_rapida');

-- ---------------------------------------------------------------------------
-- Fonte, captura, documentos, RAG
-- ---------------------------------------------------------------------------
CREATE TABLE sources (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_type   TEXT NOT NULL,                 -- caixa | leiloeiro | portal | cartorio
    name          TEXT NOT NULL,
    url           TEXT,
    reliability   SMALLINT CHECK (reliability BETWEEN 0 AND 100),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE properties (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE property_identifiers (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id   UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    id_type       TEXT NOT NULL,                 -- matricula | id_caixa | endereco | cnib
    value         TEXT NOT NULL,
    confidence    SMALLINT CHECK (confidence BETWEEN 0 AND 100),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (property_id, id_type, value)
);
CREATE INDEX idx_prop_ident_lookup ON property_identifiers (id_type, value);

CREATE TABLE captures (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id     UUID NOT NULL REFERENCES sources(id),
    property_id   UUID REFERENCES properties(id),  -- pode ser nulo até deduplicação
    hash          TEXT NOT NULL,                   -- fingerprint do conteúdo bruto
    raw           JSONB NOT NULL,                  -- payload cru preservado (imutável)
    captured_at   TIMESTAMPTZ NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source_id, hash)
);

CREATE TABLE documents (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id     UUID REFERENCES sources(id),
    property_id   UUID REFERENCES properties(id),
    doc_type      TEXT NOT NULL,                   -- edital | matricula | laudo | certidao
    mime          TEXT,
    hash          TEXT NOT NULL,
    uri           TEXT,                            -- caminho/local do arquivo
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (hash)
);

CREATE TABLE document_chunks (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id   UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index   INT NOT NULL,
    content       TEXT NOT NULL,
    -- metadata do RAG (arquitetura §8.2)
    tipo          TEXT,        -- REGRA | DEFINICAO | FORMULA | CHECKLIST | EVIDENCIA | CASO | ANALISE | MANUAL
    dominio       TEXT,
    topic         TEXT,
    rule_id       TEXT,
    priority      SMALLINT,
    effective_from DATE,
    effective_to   DATE,
    confidence    SMALLINT,
    embedding     VECTOR(1536),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (document_id, chunk_index)
);
-- busca semântica (IVFFlat; ajustar lists conforme volume)
CREATE INDEX idx_chunks_embedding ON document_chunks
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- ---------------------------------------------------------------------------
-- Oportunidade e análise (snapshot imutável)
-- ---------------------------------------------------------------------------
CREATE TABLE opportunities (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id   UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    source_id     UUID REFERENCES sources(id),
    external_ref  TEXT,                            -- ex.: item 227 / edital 0031/0326
    auction_date  TIMESTAMPTZ,
    min_bid       NUMERIC(14,2),
    current_phase pipeline_phase NOT NULL DEFAULT 'CAPTURED',
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_opp_property ON opportunities (property_id);

CREATE TABLE analyses (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_id      UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    version             INT NOT NULL,
    analysis_date       TIMESTAMPTZ NOT NULL DEFAULT now(),
    phase               pipeline_phase NOT NULL DEFAULT 'CAPTURED',

    identity_confidence SMALLINT CHECK (identity_confidence BETWEEN 0 AND 100),
    legal_status        legal_status NOT NULL DEFAULT 'PENDENTE',
    occupancy_status    TEXT,

    market_value        NUMERIC(14,2),
    economic_cost       NUMERIC(14,2),
    net_discount        NUMERIC(6,4),              -- fração 0-1
    margin              NUMERIC(14,2),
    liquidity_score     SMALLINT,

    strategy            strategy,
    opportunity_score   SMALLINT CHECK (opportunity_score BETWEEN 0 AND 100),
    investor_fit        SMALLINT CHECK (investor_fit BETWEEN 0 AND 100),
    confidence          SMALLINT NOT NULL CHECK (confidence BETWEEN 0 AND 100),

    decision            decision_state NOT NULL DEFAULT 'PENDING',
    explanation         TEXT,

    rule_version        TEXT NOT NULL DEFAULT '1.0.0',
    parameters_version  TEXT NOT NULL DEFAULT '1.0.0',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (opportunity_id, version)
);
CREATE INDEX idx_analyses_opp ON analyses (opportunity_id, version DESC);

CREATE TABLE evidences (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id   UUID NOT NULL REFERENCES analyses(id) ON DELETE CASCADE,
    source_id     UUID REFERENCES sources(id),
    document_id   UUID REFERENCES documents(id),
    location      TEXT,                            -- ex.: AV-13 da matrícula, item 18.1
    fact          TEXT NOT NULL,
    value         TEXT,
    state         evidence_state NOT NULL,
    confidence    SMALLINT CHECK (confidence BETWEEN 0 AND 100),
    observed_at   DATE,
    extracted_at  TIMESTAMPTZ,
    created_by    TEXT NOT NULL,                   -- agente/tool; nunca "inventa"
    rule_refs     TEXT[] NOT NULL DEFAULT '{}',
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_evidences_analysis ON evidences (analysis_id);

CREATE TABLE facts (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id       UUID NOT NULL REFERENCES analyses(id) ON DELETE CASCADE,
    key               TEXT NOT NULL,
    value             TEXT,
    information_type  evidence_state NOT NULL,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE costs (
    analysis_id            UUID PRIMARY KEY REFERENCES analyses(id) ON DELETE CASCADE,
    preco                  NUMERIC(14,2) NOT NULL,
    comissao_leiloeiro     NUMERIC(14,2) NOT NULL DEFAULT 0,
    itbi                   NUMERIC(14,2) NOT NULL DEFAULT 0,
    registro_documentacao  NUMERIC(14,2) NOT NULL DEFAULT 0,
    condominio_debitos     NUMERIC(14,2) NOT NULL DEFAULT 0,
    tributos_debitos       NUMERIC(14,2) NOT NULL DEFAULT 0,
    reforma                NUMERIC(14,2) NOT NULL DEFAULT 0,
    reserva_imprevistos    NUMERIC(14,2) NOT NULL DEFAULT 0,
    custo_juridico_esperado NUMERIC(14,2) NOT NULL DEFAULT 0,
    carrying               NUMERIC(14,2) NOT NULL DEFAULT 0,
    total                  NUMERIC(14,2) GENERATED ALWAYS AS (
        preco + comissao_leiloeiro + itbi + registro_documentacao
        + condominio_debitos + tributos_debitos + reforma
        + reserva_imprevistos + custo_juridico_esperado + carrying
    ) STORED
);

CREATE TABLE valuations (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id   UUID NOT NULL REFERENCES analyses(id) ON DELETE CASCADE,
    kind          scenario_kind NOT NULL,
    value         NUMERIC(14,2) NOT NULL,
    confidence    SMALLINT CHECK (confidence BETWEEN 0 AND 100),
    method        TEXT,
    UNIQUE (analysis_id, kind)
);

CREATE TABLE scenarios (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id   UUID NOT NULL REFERENCES analyses(id) ON DELETE CASCADE,
    kind          scenario_kind NOT NULL,
    roi           NUMERIC(6,4),
    margin        NUMERIC(14,2),
    survives      BOOLEAN NOT NULL DEFAULT false,
    notes         TEXT,
    UNIQUE (analysis_id, kind)
);

CREATE TABLE comparables (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id   UUID NOT NULL REFERENCES analyses(id) ON DELETE CASCADE,
    source        TEXT,
    address       TEXT,
    area_m2       NUMERIC(8,2),
    price         NUMERIC(14,2),
    price_m2      NUMERIC(12,2),
    rent          NUMERIC(12,2),
    observed_at   DATE,
    link          TEXT
);

CREATE TABLE risks (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id   UUID NOT NULL REFERENCES analyses(id) ON DELETE CASCADE,
    category      TEXT NOT NULL,
    description   TEXT,
    severity      risk_severity NOT NULL,
    state         evidence_state NOT NULL
);

CREATE TABLE pendings (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id   UUID NOT NULL REFERENCES analyses(id) ON DELETE CASCADE,
    item          TEXT NOT NULL,
    reason        TEXT,
    blocks_buy    BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE decisions (
    analysis_id     UUID PRIMARY KEY REFERENCES analyses(id) ON DELETE CASCADE,
    decision        decision_state NOT NULL,
    deciding_layer  TEXT NOT NULL,                 -- nome do DecisionLayer
    reasons         TEXT[] NOT NULL DEFAULT '{}',
    decided_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE analysis_events (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id   UUID NOT NULL REFERENCES analyses(id) ON DELETE CASCADE,
    event_type    TEXT NOT NULL,
    payload       JSONB,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_events_analysis ON analysis_events (analysis_id, created_at);

-- ---------------------------------------------------------------------------
-- Regras, versões, parâmetros, estratégias, investidor
-- ---------------------------------------------------------------------------
CREATE TABLE rules (
    code          TEXT PRIMARY KEY,               -- RULE-JUR-002, RULE-ID-001...
    name          TEXT NOT NULL,
    domain        TEXT NOT NULL,                   -- Juridico | Registral | Economico...
    priority      TEXT NOT NULL,                  -- P0..P7 / GATE / BLOCK
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE rule_versions (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_code      TEXT NOT NULL REFERENCES rules(code) ON DELETE CASCADE,
    version        TEXT NOT NULL,
    definition     JSONB NOT NULL,                 -- condição/gatilho/evidência/ação
    effective_from DATE NOT NULL,
    effective_to   DATE,
    approved_by    TEXT,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (rule_code, version)
);

CREATE TABLE parameters (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scope          TEXT NOT NULL,                  -- global | investidor | estrategia | local | tipo | excecao
    scope_ref      TEXT,                           -- id do escopo (ex.: estrategia=renda)
    key            TEXT NOT NULL,                  -- ex.: desconto_liquido_min
    value          JSONB NOT NULL,
    version        TEXT NOT NULL DEFAULT '1.0.0',
    effective_from DATE NOT NULL DEFAULT CURRENT_DATE,
    effective_to   DATE,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (scope, scope_ref, key, version)
);

CREATE TABLE strategies (
    code                    strategy PRIMARY KEY,
    desconto_liquido_min    NUMERIC(5,4) NOT NULL,
    margem_min              NUMERIC(5,4) NOT NULL,
    yield_liquido_mensal_min NUMERIC(6,5),
    liquidez_min            SMALLINT NOT NULL
);

CREATE TABLE investors (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name           TEXT NOT NULL,
    capital_total  NUMERIC(16,2),
    reserve_min    NUMERIC(16,2),
    risk_tolerance TEXT,                            -- baixo | medio | alto
    max_per_deal   NUMERIC(16,2),
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE alerts (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_id UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
    priority       TEXT NOT NULL,                  -- critico | alto | medio | baixo | info
    message        TEXT NOT NULL,
    next_action    TEXT,
    resolved       BOOLEAN NOT NULL DEFAULT false,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_alerts_opp ON alerts (opportunity_id, resolved);

-- ---------------------------------------------------------------------------
-- Seed dos thresholds canônicos por estratégia (Canônica §8)
-- ---------------------------------------------------------------------------
INSERT INTO strategies (code, desconto_liquido_min, margem_min, yield_liquido_mensal_min, liquidez_min) VALUES
    ('revenda',     0.25, 0.20, NULL,   60),
    ('renda',       0.15, 0.10, 0.008,  60),
    ('valorizacao', 0.15, 0.15, NULL,   50),
    ('mcmv',        0.20, 0.15, 0.008,  60),
    ('terreno',     0.20, 0.20, NULL,   40);
