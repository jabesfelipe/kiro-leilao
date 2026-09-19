"""Gate de Validade Jurídica do leilão — camada P0 (Canônica §1).

Origem: adendo v1.1 dos Docs 15/19/26. É a barreira que impede "CAIXA + desconto = BUY".

Regras invioláveis:
- Ausência de evidência NÃO é regularidade -> UNKNOWN -> PENDENTE.
- Irregularidade material comprovada -> BLOCK (não compensável por score/desconto).
- Consolidação não comprovada -> não liberar BUY.
- Ocupação é risco de posse/economia, NÃO nulidade automática.
- Processo existente não é BLOCK automático: exige objeto/fase/impacto.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from radar.domain.enums import EvidenceState
from radar.domain.models import Evidence, Pending, Risk


class CheckOutcome(str, Enum):
    """Resultado de uma verificação jurídica."""

    CONFIRMED = "CONFIRMED"      # comprovado documentalmente
    IRREGULAR = "IRREGULAR"      # irregularidade material comprovada -> BLOCK
    UNKNOWN = "UNKNOWN"          # sem evidência -> PENDENTE
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True)
class GateCheck:
    code: str
    description: str
    blocks_buy_if_unknown: bool = True


# Catálogo dos gates P0 (GATE-JUR-001..007)
GATE_CHECKS: tuple[GateCheck, ...] = (
    GateCheck("GATE-JUR-001", "Consolidação da propriedade comprovada na matrícula"),
    GateCheck("GATE-JUR-002", "Matrícula atualizada e consistente com o edital"),
    GateCheck("GATE-JUR-003", "Constituição em mora comprovada"),
    GateCheck("GATE-JUR-004", "Intimação/notificação para purgação da mora comprovada"),
    GateCheck("GATE-JUR-005", "Cronologia coerente: mora -> consolidação -> leilão"),
    GateCheck("GATE-JUR-006", "Processos judiciais sem impacto na validade do leilão"),
    GateCheck(
        "GATE-JUR-007",
        "Dados do certame sem divergência (data/hora/plataforma/valor)",
        blocks_buy_if_unknown=True,
    ),
)

CHECKS_BY_CODE = {c.code: c for c in GATE_CHECKS}


@dataclass
class LegalGateInput:
    """Resultados das verificações, vindos de documentos/tools.

    Chave = código do gate; valor = (resultado, onde está a prova).
    O que não for informado é tratado como UNKNOWN (nunca como regular).
    """

    outcomes: dict[str, tuple[CheckOutcome, str | None]] = field(default_factory=dict)
    ocupado: bool | None = None
    source_id: str = "manual"
    created_by: str = "AG-03:juridico"

    def outcome(self, code: str) -> tuple[CheckOutcome, str | None]:
        return self.outcomes.get(code, (CheckOutcome.UNKNOWN, None))


@dataclass
class LegalGateResult:
    legal_status: str  # "OK" | "PENDENTE" | "BLOCK"
    evidences: list[Evidence] = field(default_factory=list)
    pendings: list[Pending] = field(default_factory=list)
    risks: list[Risk] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)

    @property
    def blocks_buy(self) -> bool:
        return self.legal_status in ("BLOCK", "PENDENTE")


_OUTCOME_TO_EVIDENCE_STATE = {
    CheckOutcome.CONFIRMED: EvidenceState.CONFIRMED,
    CheckOutcome.IRREGULAR: EvidenceState.OBSERVED,
    CheckOutcome.UNKNOWN: EvidenceState.UNKNOWN,
    CheckOutcome.NOT_APPLICABLE: EvidenceState.UNKNOWN,
}


def evaluate_legal_gate(inp: LegalGateInput) -> LegalGateResult:
    """Avalia a camada 0. BLOCK vence; senão UNKNOWN vira PENDENTE; senão OK."""
    evidences: list[Evidence] = []
    pendings: list[Pending] = []
    risks: list[Risk] = []
    reasons: list[str] = []

    has_block = False
    has_unknown = False

    for check in GATE_CHECKS:
        outcome, location = inp.outcome(check.code)

        evidences.append(
            Evidence(
                evidence_id=check.code,
                source_id=inp.source_id,
                source_type="documento",
                location=location,
                fact=check.description,
                value=outcome.value,
                state=_OUTCOME_TO_EVIDENCE_STATE[outcome],
                confidence=95.0 if outcome is CheckOutcome.CONFIRMED else 0.0,
                extracted_at=datetime.now(),
                created_by=inp.created_by,
                rule_refs=[check.code],
            )
        )

        if outcome is CheckOutcome.IRREGULAR:
            has_block = True
            reasons.append(f"{check.code}: irregularidade material comprovada — {check.description}.")
            risks.append(
                Risk(
                    category="juridico",
                    description=f"{check.code}: {check.description}",
                    severity="critico",
                    state=EvidenceState.OBSERVED,
                )
            )
        elif outcome is CheckOutcome.UNKNOWN:
            has_unknown = True
            pendings.append(
                Pending(
                    item=check.code,
                    reason=f"Sem evidência: {check.description}. Ausência não é regularidade.",
                    blocks_buy=check.blocks_buy_if_unknown,
                )
            )

    # ocupação: risco de posse, nunca nulidade
    if inp.ocupado is True:
        risks.append(
            Risk(
                category="posse",
                description="Imóvel ocupado: risco de posse/custo de desocupação.",
                severity="alto",
                state=EvidenceState.OBSERVED,
            )
        )
        reasons.append("Ocupação registrada: tratar como risco de posse/economia, não nulidade.")
    elif inp.ocupado is None:
        pendings.append(
            Pending(
                item="OCUPACAO",
                reason="Situação de ocupação desconhecida: estimar custo/prazo de desocupação.",
                blocks_buy=False,
            )
        )

    if has_block:
        status = "BLOCK"
        reasons.insert(0, "Validade jurídica: BLOCK (procedimento não executável).")
    elif has_unknown:
        status = "PENDENTE"
        reasons.insert(
            0,
            "Validade jurídica: PENDENTE — evidências faltantes impedem liberar BUY.",
        )
    else:
        status = "OK"
        reasons.insert(0, "Validade jurídica: OK — todos os gates comprovados documentalmente.")

    return LegalGateResult(
        legal_status=status,
        evidences=evidences,
        pendings=pendings,
        risks=risks,
        reasons=reasons,
    )
