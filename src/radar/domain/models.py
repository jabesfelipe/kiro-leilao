"""Modelos de domínio (contratos Pydantic).

Contrato canônico da análise: arquitetura de IA §16.
Evidence Layer: arquitetura de IA §11 + Canônica §3.
"""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field

from radar.domain.enums import DecisionState, EvidenceState, PipelinePhase, Strategy


class Evidence(BaseModel):
    """Uma evidência com proveniência obrigatória (Evidence Layer)."""

    evidence_id: str
    source_id: str
    source_type: str
    document_id: str | None = None
    location: str | None = Field(default=None, description="ex.: AV-13 da matrícula, item 18.1 do edital")
    fact: str
    value: str | float | bool | None = None
    state: EvidenceState
    confidence: float = Field(ge=0, le=100)
    observed_at: date | None = None
    extracted_at: datetime | None = None
    created_by: str = Field(description="agente/tool que registrou; nunca 'inventa' evidência")
    rule_refs: list[str] = Field(default_factory=list)


class CostBreakdown(BaseModel):
    """Componentes do custo econômico total (Canônica §9)."""

    preco: float
    comissao_leiloeiro: float = 0.0
    itbi: float = 0.0
    registro_documentacao: float = 0.0
    condominio_debitos: float = 0.0
    tributos_debitos: float = 0.0
    reforma: float = 0.0
    reserva_imprevistos: float = 0.0
    custo_juridico_esperado: float = 0.0
    carrying: float = 0.0

    @property
    def total(self) -> float:
        return (
            self.preco
            + self.comissao_leiloeiro
            + self.itbi
            + self.registro_documentacao
            + self.condominio_debitos
            + self.tributos_debitos
            + self.reforma
            + self.reserva_imprevistos
            + self.custo_juridico_esperado
            + self.carrying
        )


class Risk(BaseModel):
    category: str
    description: str
    severity: str = Field(description="baixo|medio|alto|critico")
    state: EvidenceState


class Pending(BaseModel):
    item: str
    reason: str
    blocks_buy: bool = False


class AnalysisContract(BaseModel):
    """Contrato canônico da análise (arquitetura §16). Snapshot imutável."""

    property_id: str
    analysis_version: int = 1
    analysis_date: datetime

    identity_confidence: float = Field(ge=0, le=100)
    legal_status: str = Field(description="OK|PENDENTE|BLOCK")
    legal_evidence: list[Evidence] = Field(default_factory=list)
    occupancy_status: str | None = None

    market_value: float | None = None
    economic_cost: float | None = None
    net_discount: float | None = None
    margin: float | None = None
    liquidity_score: float | None = None

    strategy: Strategy | None = None
    opportunity_score: float | None = Field(default=None, ge=0, le=100)
    investor_fit: float | None = Field(default=None, ge=0, le=100)
    confidence: float = Field(ge=0, le=100)

    risks: list[Risk] = Field(default_factory=list)
    pending: list[Pending] = Field(default_factory=list)

    phase: PipelinePhase = PipelinePhase.CAPTURED
    decision: DecisionState = DecisionState.PENDING
    explanation: str = ""
    next_actions: list[str] = Field(default_factory=list)

    rule_version: str = "1.0.0"

    model_config = {"frozen": False}  # torna-se imutável após persistir (snapshot)
