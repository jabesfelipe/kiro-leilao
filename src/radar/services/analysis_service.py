"""Serviço de análise — orquestra motores, contrato e persistência.

Fecha o ciclo: entradas -> Calculation Engine -> Decision Engine -> AnalysisContract
-> (opcional) persistência como snapshot imutável.

Determinístico: não depende de LLM. Os nós que dependem de LLM/RAG/tools (captura,
mercado, extração de documentos) alimentam as entradas deste serviço, mas não
substituem regras nem cálculos (arquitetura §2).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime

from radar.domain.enums import PipelinePhase, Strategy
from radar.domain.models import AnalysisContract, CostBreakdown
from radar.domain.parameters import (
    PARAMETERS_VERSION,
    classify_score,
    liquidity_category,
)
from radar.engines import calculation as calc
from radar.engines.decision import DecisionInput, DecisionResult, decide


@dataclass
class AnalysisRequest:
    """Entradas já coletadas/confirmadas pelos nós anteriores do pipeline."""

    property_id: str
    strategy: Strategy
    price: float
    market_value: float
    # custos
    commission_pct: float = 0.05
    itbi_pct: float = 0.02
    registro: float = 0.0
    condominio: float = 0.0
    tributos: float = 0.0
    reforma: float = 0.0
    reserva: float = 0.0
    custo_juridico_potencial: float = 0.0
    prob_juridica: float = 0.0
    carrying: float = 0.0
    # renda (opcional)
    rent_month: float | None = None
    condo_month: float = 0.0
    iptu_month: float = 0.0
    maintenance_month: float = 0.0
    vacancy_month: float = 0.0
    # sinais das camadas anteriores
    legal_status: str = "OK"
    has_critical_block: bool = False
    is_eligible: bool = True
    confidence: float = 0.0
    liquidity_score: float = 0.0
    identity_confidence: float = 0.0
    survives_conservative: bool = True
    occupancy_status: str | None = None


@dataclass
class AnalysisOutput:
    contract: AnalysisContract
    cost: CostBreakdown
    decision: DecisionResult


def _explain(contract: AnalysisContract, decision: DecisionResult) -> str:
    band = (
        classify_score(contract.opportunity_score)
        if contract.opportunity_score is not None
        else None
    )
    parts: list[str] = [
        f"Decisão: {decision.decision.value} "
        f"(veredito Método Jabes {decision.decision.veredito_jabes}), "
        f"determinada na camada {decision.deciding_layer.name}."
    ]
    if contract.net_discount is not None:
        parts.append(f"Desconto líquido: {contract.net_discount:.1%}.")
    if contract.margin is not None and contract.market_value:
        parts.append(f"Margem: R$ {contract.margin:,.0f}.")
    if contract.liquidity_score is not None:
        parts.append(
            f"Liquidez: {contract.liquidity_score:.0f} ({liquidity_category(contract.liquidity_score)})."
        )
    if band is not None:
        parts.append(f"Score: {contract.opportunity_score:.0f} {band.emoji} {band.label}.")
    parts.extend(decision.reasons)
    return " ".join(parts)


def analyze(req: AnalysisRequest) -> AnalysisOutput:
    """Executa a análise determinística de ponta a ponta."""
    # 1. Calculation Engine
    cost = calc.build_cost(
        req.price,
        commission_pct=req.commission_pct,
        itbi_pct=req.itbi_pct,
        registro=req.registro,
        condominio=req.condominio,
        tributos=req.tributos,
        reforma=req.reforma,
        reserva=req.reserva,
        custo_juridico_potencial=req.custo_juridico_potencial,
        prob_juridica=req.prob_juridica,
        carrying=req.carrying,
    )
    tco = cost.total
    net_disc = calc.net_discount(tco, req.market_value)
    margin_abs = calc.margin(tco, req.market_value)
    margin_p = calc.margin_pct(tco, req.market_value)
    net_yield = None
    if req.rent_month is not None:
        net_yield = calc.net_monthly_yield(
            req.rent_month,
            req.condo_month,
            req.iptu_month,
            req.maintenance_month,
            req.vacancy_month,
            tco,
        )

    # 2. Decision Engine (precedência canônica)
    decision = decide(
        DecisionInput(
            legal_status=req.legal_status,
            has_critical_block=req.has_critical_block,
            is_eligible=req.is_eligible,
            confidence=req.confidence,
            net_discount=net_disc,
            margin_pct=margin_p,
            liquidity_score=req.liquidity_score,
            strategy=req.strategy,
            opportunity_score=None,
            survives_conservative=req.survives_conservative,
            net_monthly_yield=net_yield,
        )
    )

    # 3. Contrato canônico (snapshot)
    contract = AnalysisContract(
        property_id=req.property_id,
        analysis_date=datetime.now(),
        identity_confidence=req.identity_confidence,
        legal_status=req.legal_status,
        occupancy_status=req.occupancy_status,
        market_value=req.market_value,
        economic_cost=tco,
        net_discount=round(net_disc, 4),
        margin=round(margin_abs, 2),
        liquidity_score=req.liquidity_score,
        strategy=req.strategy,
        opportunity_score=None,
        confidence=req.confidence,
        phase=PipelinePhase.DECIDED,
        decision=decision.decision,
        rule_version=PARAMETERS_VERSION,
    )
    contract.explanation = _explain(contract, decision)
    contract.next_actions = decision.reasons

    return AnalysisOutput(contract=contract, cost=cost, decision=decision)


def analyze_and_persist(req: AnalysisRequest, opportunity_id: uuid.UUID) -> AnalysisOutput:
    """Executa a análise e persiste como novo snapshot (requer banco)."""
    from radar.db import repository
    from radar.db.session import get_session

    out = analyze(req)
    with get_session() as session:
        repository.save_analysis(
            session,
            opportunity_id,
            out.contract,
            cost=out.cost,
            decision=out.decision,
        )
    return out
