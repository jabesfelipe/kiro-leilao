"""Enums canônicos do domínio.

Fonte de verdade: spec/00_ESPECIFICACAO_CANONICA.md e spec/01_MAQUINA_DE_ESTADOS.md.
Nenhum valor aqui deve divergir dessas especificações.
"""

from __future__ import annotations

from enum import Enum


class DecisionState(str, Enum):
    """Saídas de decisão canônicas (Canônica §2)."""

    BUY = "BUY"
    BUY_IF = "BUY_IF"
    MONITOR = "MONITOR"
    DO_NOT_BUY = "DO_NOT_BUY"
    BLOCK = "BLOCK"
    PENDING = "PENDING"  # antes de DECIDED

    @property
    def veredito_jabes(self) -> str:
        """Veredito A–E equivalente do Método Jabes."""
        return {
            DecisionState.BUY: "A",
            DecisionState.BUY_IF: "B/D",
            DecisionState.MONITOR: "C",
            DecisionState.DO_NOT_BUY: "E",
            DecisionState.BLOCK: "E",
            DecisionState.PENDING: "-",
        }[self]


class EvidenceState(str, Enum):
    """Estados de evidência canônicos (Canônica §3)."""

    OBSERVED = "OBSERVED"
    CONFIRMED = "CONFIRMED"
    CALCULATED = "CALCULATED"
    ESTIMATED = "ESTIMATED"
    INFERRED = "INFERRED"
    UNKNOWN = "UNKNOWN"


class DecisionLayer(int, Enum):
    """Camadas de precedência de decisão (Canônica §1).

    Uma camada só é avaliada se a anterior não eliminou a oportunidade.
    """

    LEGAL_VALIDITY = 0
    CRITICAL_BLOCKS = 1
    ELIGIBILITY = 2
    DATA_CONFIDENCE = 3
    ECONOMICS = 4
    STRATEGY = 5
    SCORE = 6
    SCENARIO = 7
    ACTION = 8


class PipelinePhase(int, Enum):
    """Fases do pipeline de processamento (Máquina de Estados §2)."""

    CAPTURED = 1
    NORMALIZED = 2
    IDENTIFIED = 3
    DEDUPLICATED = 4
    LEGAL_VALIDATED = 5
    ENRICHED = 6
    VALUATED = 7
    COSTED = 8
    SCORED = 9
    RANKED = 10
    IN_ANALYSIS = 11
    DECIDED = 12
    MONITORED = 13
    CLOSED = 14


class Strategy(str, Enum):
    """Estratégias do investidor (Canônica §8)."""

    REVENDA = "revenda"
    RENDA = "renda"
    VALORIZACAO = "valorizacao"
    MCMV = "mcmv"
    TERRENO = "terreno"


class ConfidenceBand(str, Enum):
    """Bandas de confiança (Canônica §5)."""

    MUITO_ALTA = "muito_alta"
    ALTA = "alta"
    BOA = "boa"
    FRACA = "fraca"
    INSUFICIENTE = "insuficiente"
