"""Orquestração da análise via LangGraph.

Fluxo (arquitetura §6 / Máquina de Estados §4):

    START -> normalizar -> identidade -> validade_juridica
          ├─ BLOCK/identidade insuficiente ──────────────┐
          └─ continuar -> economia -> decisao -> explicacao -> END

O estado compartilhado é a única comunicação entre nós. Regras de negócio e
cálculos ficam nos motores determinísticos — o grafo apenas orquestra.
"""

from __future__ import annotations

from typing import Any, TypedDict

from radar.capture.caixa import normalize_caixa
from radar.capture.schemas import NormalizedListing, RawCapture
from radar.domain.enums import DecisionState, PipelinePhase, Strategy
from radar.domain.models import Pending, Risk
from radar.engines import calculation as calc
from radar.engines.decision import DecisionInput, DecisionResult, decide
from radar.pipeline.identity import IdentityResult, resolve_identity
from radar.pipeline.legal_gate import LegalGateInput, LegalGateResult, evaluate_legal_gate


class AnalysisState(TypedDict, total=False):
    """Estado compartilhado do grafo."""

    # entrada
    capture: RawCapture
    strategy: Strategy
    legal_input: LegalGateInput
    market_value: float | None
    cost_overrides: dict[str, float]
    liquidity_score: float
    survives_conservative: bool
    rent_month: float | None
    rent_costs: dict[str, float]

    # produzidos pelos nós
    listing: NormalizedListing
    identity: IdentityResult
    legal: LegalGateResult
    phase: PipelinePhase
    economic_cost: float | None
    net_discount: float | None
    margin_pct: float | None
    net_monthly_yield: float | None
    confidence: float
    decision_result: DecisionResult
    decision: str
    pendings: list[Pending]
    risks: list[Risk]
    reasons: list[str]
    explanation: str


# ---------------------------------------------------------------- nós


def node_normalize(state: AnalysisState) -> AnalysisState:
    """Captura -> NormalizedListing (original preservado no RawCapture)."""
    state["listing"] = normalize_caixa(state["capture"])
    state["phase"] = PipelinePhase.NORMALIZED
    return state


def node_identity(state: AnalysisState) -> AnalysisState:
    """Resolve identidade do imóvel (níveis I0–I4)."""
    state["identity"] = resolve_identity(state["listing"])
    state["phase"] = PipelinePhase.IDENTIFIED
    return state


def node_legal_gate(state: AnalysisState) -> AnalysisState:
    """Camada P0: validade jurídica do leilão."""
    legal = evaluate_legal_gate(state.get("legal_input") or LegalGateInput())
    state["legal"] = legal
    state["pendings"] = list(legal.pendings)
    state["risks"] = list(legal.risks)
    state["phase"] = PipelinePhase.LEGAL_VALIDATED
    return state


def node_economics(state: AnalysisState) -> AnalysisState:
    """Custo econômico total, desconto líquido e margem (determinístico)."""
    listing = state["listing"]
    price = listing.min_bid
    market_value = state.get("market_value")
    if price is None or not market_value:
        state["phase"] = PipelinePhase.COSTED
        return state

    ov = state.get("cost_overrides") or {}
    cost = calc.build_cost(
        price,
        commission_pct=ov.get("commission_pct", listing.comissao_leiloeiro_pct or 0.05),
        itbi_pct=ov.get("itbi_pct", 0.02),
        registro=ov.get("registro", 0.0),
        condominio=ov.get("condominio", 0.0),
        tributos=ov.get("tributos", 0.0),
        reforma=ov.get("reforma", 0.0),
        reserva=ov.get("reserva", 0.0),
        custo_juridico_potencial=ov.get("custo_juridico_potencial", 0.0),
        prob_juridica=ov.get("prob_juridica", 0.0),
        carrying=ov.get("carrying", 0.0),
    )
    tco = cost.total
    state["economic_cost"] = tco
    state["net_discount"] = calc.net_discount(tco, market_value)
    state["margin_pct"] = calc.margin_pct(tco, market_value)

    rent = state.get("rent_month")
    if rent:
        rc = state.get("rent_costs") or {}
        state["net_monthly_yield"] = calc.net_monthly_yield(
            rent,
            rc.get("condo", 0.0),
            rc.get("iptu", 0.0),
            rc.get("maintenance", 0.0),
            rc.get("vacancy", 0.0),
            tco,
        )
    state["phase"] = PipelinePhase.COSTED
    return state


def node_decision(state: AnalysisState) -> AnalysisState:
    """Decision Engine: aplica a precedência canônica (camadas 0..8)."""
    identity = state.get("identity")
    legal = state.get("legal")

    # confiança combina identidade e evidência jurídica
    confidence = state.get("confidence")
    if confidence is None:
        base = identity.confidence if identity else 0.0
        if legal and legal.legal_status == "OK":
            confidence = min(100.0, base + 10.0)
        elif legal and legal.legal_status == "PENDENTE":
            confidence = base * 0.7
        else:
            confidence = base * 0.5
        state["confidence"] = confidence

    result = decide(
        DecisionInput(
            legal_status=legal.legal_status if legal else "PENDENTE",
            has_critical_block=False,
            is_eligible=bool(identity and identity.level >= 2),
            confidence=confidence,
            net_discount=state.get("net_discount"),
            margin_pct=state.get("margin_pct"),
            liquidity_score=state.get("liquidity_score", 0.0),
            strategy=state.get("strategy"),
            opportunity_score=None,
            survives_conservative=state.get("survives_conservative", True),
            net_monthly_yield=state.get("net_monthly_yield"),
        )
    )
    state["decision_result"] = result
    state["decision"] = result.decision.value
    state["phase"] = PipelinePhase.DECIDED
    return state


def node_explain(state: AnalysisState) -> AnalysisState:
    """Explicabilidade: junta razões da identidade, do gate e da decisão."""
    parts: list[str] = []
    identity = state.get("identity")
    legal = state.get("legal")
    result = state.get("decision_result")

    if result:
        parts.append(
            f"Decisão: {result.decision.value} "
            f"(veredito Jabes {result.decision.veredito_jabes}); "
            f"camada decisória: {result.deciding_layer.name}."
        )
    if identity:
        parts.append(f"Identidade: {identity.level.name} (confiança {identity.confidence:.0f}).")
    if legal:
        parts.extend(legal.reasons)
    if state.get("net_discount") is not None:
        parts.append(f"Desconto líquido: {state['net_discount']:.1%}.")
    if result:
        parts.extend(result.reasons)

    state["reasons"] = parts
    state["explanation"] = " ".join(parts)
    return state


# ------------------------------------------------------------ roteamento


def route_after_legal(state: AnalysisState) -> str:
    """BLOCK jurídico ou identidade insuficiente curto-circuitam para a decisão."""
    legal = state.get("legal")
    identity = state.get("identity")
    if (legal and legal.legal_status == "BLOCK") or (identity and identity.level < 2):
        return "decisao"
    return "economia"


# ------------------------------------------------------------ montagem


def build_graph() -> Any:
    """Compila o grafo LangGraph com os nós do pipeline."""
    from langgraph.graph import END, START, StateGraph

    g: StateGraph = StateGraph(AnalysisState)
    g.add_node("normalizar", node_normalize)
    g.add_node("identidade", node_identity)
    g.add_node("validade_juridica", node_legal_gate)
    g.add_node("economia", node_economics)
    g.add_node("decisao", node_decision)
    g.add_node("explicacao", node_explain)

    g.add_edge(START, "normalizar")
    g.add_edge("normalizar", "identidade")
    g.add_edge("identidade", "validade_juridica")
    g.add_conditional_edges(
        "validade_juridica",
        route_after_legal,
        {"economia": "economia", "decisao": "decisao"},
    )
    g.add_edge("economia", "decisao")
    g.add_edge("decisao", "explicacao")
    g.add_edge("explicacao", END)
    return g.compile()


def run_analysis(state: AnalysisState) -> AnalysisState:
    """Executa o pipeline. Usa LangGraph; cai para execução direta se indisponível."""
    try:
        graph = build_graph()
    except ImportError:
        return _run_sequential(state)
    return graph.invoke(state)  # type: ignore[no-any-return]


def _run_sequential(state: AnalysisState) -> AnalysisState:
    """Mesma sequência do grafo, sem dependência do LangGraph."""
    state = node_normalize(state)
    state = node_identity(state)
    state = node_legal_gate(state)
    if route_after_legal(state) == "economia":
        state = node_economics(state)
    state = node_decision(state)
    return node_explain(state)


__all__ = [
    "AnalysisState",
    "build_graph",
    "run_analysis",
    "route_after_legal",
    "DecisionState",
]
