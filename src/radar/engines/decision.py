"""Decision Engine — aplica a precedência canônica de decisão.

Fonte de verdade: Canônica §1 e §2. Determinístico.
Regra inviolável: score NUNCA compensa uma camada de bloqueio.
"BLOCK jurídico não pode ser superado por desconto, score ou rentabilidade."
"""

from __future__ import annotations

from dataclasses import dataclass, field

from radar.domain.enums import DecisionLayer, DecisionState, Strategy
from radar.domain.parameters import (
    MIN_CONFIDENCE_FOR_BUY,
    MIN_LIQUIDITY_FOR_BUY,
    STRATEGY_THRESHOLDS,
)


@dataclass
class DecisionInput:
    """Entradas já calculadas/confirmadas pelos motores anteriores."""

    legal_status: str  # "OK" | "PENDENTE" | "BLOCK"
    has_critical_block: bool
    is_eligible: bool
    confidence: float  # 0-100
    net_discount: float | None  # fração 0-1
    margin_pct: float | None  # fração 0-1
    liquidity_score: float | None  # 0-100
    strategy: Strategy | None
    opportunity_score: float | None  # 0-100
    survives_conservative: bool
    net_monthly_yield: float | None = None  # fração 0-1


@dataclass
class DecisionResult:
    decision: DecisionState
    deciding_layer: DecisionLayer
    reasons: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, object]:
        return {
            "decision": self.decision.value,
            "deciding_layer": self.deciding_layer.name,
            "reasons": self.reasons,
        }


def decide(inp: DecisionInput) -> DecisionResult:
    """Aplica as camadas 0..8 em ordem. A primeira que elimina define a saída."""
    reasons: list[str] = []

    # Camada 0 — Validade jurídica do leilão (gate P0)
    if inp.legal_status == "BLOCK":
        return DecisionResult(
            DecisionState.BLOCK, DecisionLayer.LEGAL_VALIDITY,
            ["Validade jurídica do leilão: BLOCK (procedimento não executável)."],
        )
    if inp.legal_status == "PENDENTE":
        reasons.append("Validade jurídica PENDENTE: exige evidência antes de liberar BUY.")

    # Camada 1 — Bloqueios críticos
    if inp.has_critical_block:
        return DecisionResult(
            DecisionState.BLOCK, DecisionLayer.CRITICAL_BLOCKS,
            ["Bloqueio crítico confirmado (risco jurídico/registral)."],
        )

    # Camada 2 — Elegibilidade
    if not inp.is_eligible:
        return DecisionResult(
            DecisionState.DO_NOT_BUY, DecisionLayer.ELIGIBILITY,
            ["Não atende critérios mínimos de elegibilidade."],
        )

    # Camada 3 — Dados / Confiança
    if inp.confidence < MIN_CONFIDENCE_FOR_BUY:
        reasons.append(
            f"Confiança {inp.confidence:.0f} < mínimo {MIN_CONFIDENCE_FOR_BUY}: não liberar BUY."
        )
        # confiança baixa não bloqueia, mas rebaixa para MONITOR mais adiante

    # Camada 4 — Economia
    if inp.strategy is None:
        return DecisionResult(
            DecisionState.DO_NOT_BUY, DecisionLayer.STRATEGY,
            ["Estratégia não definida."],
        )
    th = STRATEGY_THRESHOLDS[inp.strategy]
    if inp.net_discount is None or inp.margin_pct is None:
        return DecisionResult(
            DecisionState.MONITOR, DecisionLayer.DATA_CONFIDENCE,
            reasons + ["Economia não calculável (dados insuficientes)."],
        )
    econ_ok = inp.net_discount >= th.desconto_liquido_min and inp.margin_pct >= th.margem_min
    if not econ_ok:
        return DecisionResult(
            DecisionState.DO_NOT_BUY, DecisionLayer.ECONOMICS,
            reasons + [
                f"Economia insuficiente: desconto líquido {inp.net_discount:.1%} "
                f"(mín {th.desconto_liquido_min:.0%}), margem {inp.margin_pct:.1%} "
                f"(mín {th.margem_min:.0%})."
            ],
        )

    # Camada 5 — Estratégia (yield para renda/MCMV, liquidez)
    if th.yield_liquido_mensal_min is not None:
        if inp.net_monthly_yield is None or inp.net_monthly_yield < th.yield_liquido_mensal_min:
            return DecisionResult(
                DecisionState.DO_NOT_BUY, DecisionLayer.STRATEGY,
                reasons + [
                    f"Yield líquido mensal abaixo do mínimo {th.yield_liquido_mensal_min:.2%} "
                    f"para estratégia {inp.strategy.value}."
                ],
            )
    liq = inp.liquidity_score if inp.liquidity_score is not None else 0
    if liq < th.liquidez_min:
        reasons.append(
            f"Liquidez {liq:.0f} abaixo do mínimo {th.liquidez_min} para {inp.strategy.value}."
        )

    # Camada 7 — Robustez / Cenário conservador
    if not inp.survives_conservative:
        return DecisionResult(
            DecisionState.BUY_IF, DecisionLayer.SCENARIO,
            reasons + ["Tese não sobrevive ao cenário conservador: só sob condição/teto."],
        )

    # Camada 8 — Ação final
    blockers_for_buy = (
        inp.confidence < MIN_CONFIDENCE_FOR_BUY
        or liq < MIN_LIQUIDITY_FOR_BUY
        or inp.legal_status == "PENDENTE"
    )
    if blockers_for_buy:
        return DecisionResult(
            DecisionState.MONITOR, DecisionLayer.ACTION,
            reasons + ["Boa oportunidade, mas há pendências que impedem BUY imediato."],
        )

    return DecisionResult(
        DecisionState.BUY, DecisionLayer.ACTION,
        reasons + ["Todas as camadas atendidas: liberar dentro do teto de preço."],
    )
