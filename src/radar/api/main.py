"""API FastAPI do Radar Imobiliário (esqueleto).

Expõe um endpoint para submeter uma análise já com os dados calculados,
retornando a decisão do Decision Engine determinístico.
"""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from radar.domain.enums import Strategy
from radar.engines.decision import DecisionInput, decide
from radar.services.analysis_service import AnalysisRequest, analyze

app = FastAPI(title="Radar Imobiliário", version="0.1.0")


class DecisionRequest(BaseModel):
    legal_status: str = Field(default="OK", description="OK|PENDENTE|BLOCK")
    has_critical_block: bool = False
    is_eligible: bool = True
    confidence: float = Field(ge=0, le=100)
    net_discount: float | None = None
    margin_pct: float | None = None
    liquidity_score: float | None = None
    strategy: Strategy | None = None
    opportunity_score: float | None = None
    survives_conservative: bool = True
    net_monthly_yield: float | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analysis/decision")
def analysis_decision(req: DecisionRequest) -> dict[str, object]:
    result = decide(
        DecisionInput(
            legal_status=req.legal_status,
            has_critical_block=req.has_critical_block,
            is_eligible=req.is_eligible,
            confidence=req.confidence,
            net_discount=req.net_discount,
            margin_pct=req.margin_pct,
            liquidity_score=req.liquidity_score,
            strategy=req.strategy,
            opportunity_score=req.opportunity_score,
            survives_conservative=req.survives_conservative,
            net_monthly_yield=req.net_monthly_yield,
        )
    )
    return result.as_dict()


class AnalyzeRequest(BaseModel):
    property_id: str
    strategy: Strategy
    price: float
    market_value: float
    commission_pct: float = 0.05
    itbi_pct: float = 0.02
    registro: float = 0.0
    condominio: float = 0.0
    reforma: float = 0.0
    reserva: float = 0.0
    rent_month: float | None = None
    condo_month: float = 0.0
    iptu_month: float = 0.0
    maintenance_month: float = 0.0
    vacancy_month: float = 0.0
    legal_status: str = "OK"
    has_critical_block: bool = False
    is_eligible: bool = True
    confidence: float = Field(default=0, ge=0, le=100)
    liquidity_score: float = Field(default=0, ge=0, le=100)
    identity_confidence: float = Field(default=0, ge=0, le=100)
    survives_conservative: bool = True
    occupancy_status: str | None = None


@app.post("/analysis/run")
def analysis_run(req: AnalyzeRequest) -> dict[str, object]:
    """Executa a análise determinística de ponta a ponta e devolve o contrato."""
    out = analyze(AnalysisRequest(**req.model_dump()))
    return {
        "decision": out.decision.decision.value,
        "deciding_layer": out.decision.deciding_layer.name,
        "veredito_jabes": out.decision.decision.veredito_jabes,
        "economic_cost": out.cost.total,
        "net_discount": out.contract.net_discount,
        "margin": out.contract.margin,
        "explanation": out.contract.explanation,
    }
