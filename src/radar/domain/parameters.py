"""Parâmetros canônicos versionados.

Fonte de verdade: spec/00_ESPECIFICACAO_CANONICA.md.
Valores marcados [DEFAULT]/[PENDENTE-CALIBRAÇÃO] devem ser recalibrados após
10–20 análises reais (regra de evolução do Método Jabes).
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from radar.domain.enums import Strategy

PARAMETERS_VERSION = "1.0.0"


class ScoreBand(BaseModel):
    lo: int
    hi: int
    emoji: str
    label: str

    def contains(self, score: float) -> bool:
        return self.lo <= score <= self.hi


# Canônica §4 — bandas do opportunity score (escala única)
SCORE_BANDS: list[ScoreBand] = [
    ScoreBand(lo=90, hi=100, emoji="🔥", label="Excepcional"),
    ScoreBand(lo=80, hi=89, emoji="🟢", label="Excelente"),
    ScoreBand(lo=70, hi=79, emoji="🟡", label="Muito boa"),
    ScoreBand(lo=60, hi=69, emoji="🟠", label="Interessante"),
    ScoreBand(lo=50, hi=59, emoji="⚪", label="Especulativa"),
    ScoreBand(lo=0, hi=49, emoji="🔴", label="Fraca"),
]


def classify_score(score: float) -> ScoreBand:
    for band in SCORE_BANDS:
        if band.contains(score):
            return band
    return SCORE_BANDS[-1]


# Canônica §4.1 — pesos do opportunity score [DEFAULT]
OPPORTUNITY_WEIGHTS: dict[str, float] = {
    "desconto_liquido": 0.25,
    "margem_seguranca": 0.20,
    "liquidez": 0.15,
    "localizacao": 0.15,
    "risco": 0.10,
    "yield_renda": 0.05,
    "valorizacao": 0.05,
    "qualidade": 0.05,
}


# Canônica §5 — fator de confiança (faixa -> fator)
class ConfidenceTier(BaseModel):
    lo: int
    hi: int
    label: str
    factor: float


CONFIDENCE_TIERS: list[ConfidenceTier] = [
    ConfidenceTier(lo=90, hi=100, label="Muito alta", factor=1.00),
    ConfidenceTier(lo=75, hi=89, label="Alta", factor=0.95),
    ConfidenceTier(lo=60, hi=74, label="Boa", factor=0.88),
    ConfidenceTier(lo=40, hi=59, label="Fraca", factor=0.75),
    ConfidenceTier(lo=0, hi=39, label="Insuficiente", factor=0.60),
]

MIN_CONFIDENCE_FOR_BUY = 75  # [DEFAULT]


def confidence_factor(confidence: float) -> float:
    for tier in CONFIDENCE_TIERS:
        if tier.lo <= confidence <= tier.hi:
            return tier.factor
    return CONFIDENCE_TIERS[-1].factor


# Canônica §6 — liquidez (score 0-100 é canônico; categoria é derivada)
def liquidity_category(score: float) -> str:
    if score >= 80:
        return "Alta"
    if score >= 60:
        return "Média"
    if score >= 40:
        return "Baixa"
    return "Muito baixa"


MIN_LIQUIDITY_FOR_BUY = 60  # [DEFAULT]


# Canônica §7 — pesos do investor fit [DEFAULT]
INVESTOR_FIT_WEIGHTS: dict[str, float] = {
    "aderencia_estrategia": 0.35,
    "aderencia_capital": 0.30,
    "concentracao": 0.20,
    "aderencia_risco": 0.15,
}


# Canônica §8 — thresholds por estratégia [DEFAULT]
class StrategyThresholds(BaseModel):
    desconto_liquido_min: float = Field(description="fração 0-1")
    margem_min: float = Field(description="fração 0-1")
    yield_liquido_mensal_min: float | None = Field(default=None, description="fração 0-1")
    liquidez_min: int


STRATEGY_THRESHOLDS: dict[Strategy, StrategyThresholds] = {
    Strategy.REVENDA: StrategyThresholds(
        desconto_liquido_min=0.25, margem_min=0.20, liquidez_min=60
    ),
    Strategy.RENDA: StrategyThresholds(
        desconto_liquido_min=0.15, margem_min=0.10, yield_liquido_mensal_min=0.008, liquidez_min=60
    ),
    Strategy.VALORIZACAO: StrategyThresholds(
        desconto_liquido_min=0.15, margem_min=0.15, liquidez_min=50
    ),
    Strategy.MCMV: StrategyThresholds(
        desconto_liquido_min=0.20, margem_min=0.15, yield_liquido_mensal_min=0.008, liquidez_min=60
    ),
    Strategy.TERRENO: StrategyThresholds(
        desconto_liquido_min=0.20, margem_min=0.20, liquidez_min=40
    ),
}

EXCEPTIONAL_DISCOUNT = 0.30  # [DEFAULT] aciona exceção auditável
TICKET_MIN = 150_000.0  # [DEFAULT]
TICKET_MAX = 250_000.0  # [DEFAULT]
