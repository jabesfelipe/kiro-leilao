"""Repositório de análise — persiste o AnalysisContract como snapshot imutável.

Fecha o ciclo domínio -> banco. Regras:
- Cada análise é uma nova versão (monotônica por oportunidade); nunca sobrescreve.
- A decisão é gravada em `decisions`; os componentes de custo em `costs`.
- Evidências são append-only (contradições coexistem).
"""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from radar.domain.enums import DecisionState
from radar.domain.models import AnalysisContract, CostBreakdown
from radar.engines.decision import DecisionResult

from .models import Analysis, Cost, Decision, EvidenceRow, Opportunity


def next_version(session: Session, opportunity_id: uuid.UUID) -> int:
    """Próxima versão de análise para a oportunidade (1 se for a primeira)."""
    stmt = (
        select(Analysis.version)
        .where(Analysis.opportunity_id == opportunity_id)
        .order_by(Analysis.version.desc())
        .limit(1)
    )
    current = session.execute(stmt).scalar_one_or_none()
    return (current or 0) + 1


def current_analysis(session: Session, opportunity_id: uuid.UUID) -> Analysis | None:
    """Retorna a análise de maior versão (a 'atual')."""
    stmt = (
        select(Analysis)
        .where(Analysis.opportunity_id == opportunity_id)
        .order_by(Analysis.version.desc())
        .limit(1)
    )
    return session.execute(stmt).scalar_one_or_none()


def save_analysis(
    session: Session,
    opportunity_id: uuid.UUID,
    contract: AnalysisContract,
    *,
    cost: CostBreakdown | None = None,
    decision: DecisionResult | None = None,
) -> Analysis:
    """Persiste o contrato canônico como novo snapshot de análise.

    Não faz commit (responsabilidade da sessão/`get_session`).
    """
    version = next_version(session, opportunity_id)

    row = Analysis(
        opportunity_id=opportunity_id,
        version=version,
        analysis_date=contract.analysis_date,
        phase=contract.phase,
        identity_confidence=int(contract.identity_confidence),
        legal_status=contract.legal_status,
        occupancy_status=contract.occupancy_status,
        market_value=contract.market_value,
        economic_cost=contract.economic_cost,
        net_discount=contract.net_discount,
        margin=contract.margin,
        liquidity_score=int(contract.liquidity_score) if contract.liquidity_score is not None else None,
        strategy=contract.strategy,
        opportunity_score=int(contract.opportunity_score) if contract.opportunity_score is not None else None,
        investor_fit=int(contract.investor_fit) if contract.investor_fit is not None else None,
        confidence=int(contract.confidence),
        decision=contract.decision,
        explanation=contract.explanation,
        rule_version=contract.rule_version,
    )
    session.add(row)
    session.flush()  # garante row.id

    # evidências (append-only)
    for ev in contract.legal_evidence:
        session.add(
            EvidenceRow(
                analysis_id=row.id,
                source_id=None,
                document_id=None,
                location=ev.location,
                fact=ev.fact,
                value=str(ev.value) if ev.value is not None else None,
                state=ev.state,
                confidence=int(ev.confidence),
                observed_at=ev.observed_at,
                extracted_at=ev.extracted_at,
                created_by=ev.created_by,
                rule_refs=ev.rule_refs,
            )
        )

    if cost is not None:
        session.add(
            Cost(
                analysis_id=row.id,
                preco=cost.preco,
                comissao_leiloeiro=cost.comissao_leiloeiro,
                itbi=cost.itbi,
                registro_documentacao=cost.registro_documentacao,
                condominio_debitos=cost.condominio_debitos,
                tributos_debitos=cost.tributos_debitos,
                reforma=cost.reforma,
                reserva_imprevistos=cost.reserva_imprevistos,
                custo_juridico_esperado=cost.custo_juridico_esperado,
                carrying=cost.carrying,
            )
        )

    if decision is not None:
        session.add(
            Decision(
                analysis_id=row.id,
                decision=decision.decision,
                deciding_layer=decision.deciding_layer.name,
                reasons=decision.reasons,
            )
        )

    return row


def create_opportunity(
    session: Session,
    property_id: uuid.UUID,
    *,
    source_id: uuid.UUID | None = None,
    external_ref: str | None = None,
    min_bid: float | None = None,
) -> Opportunity:
    opp = Opportunity(
        property_id=property_id,
        source_id=source_id,
        external_ref=external_ref,
        min_bid=min_bid,
    )
    session.add(opp)
    session.flush()
    return opp


__all__ = [
    "next_version",
    "current_analysis",
    "save_analysis",
    "create_opportunity",
    "DecisionState",
]
