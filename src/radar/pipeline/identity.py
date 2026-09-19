"""Identidade e deduplicação do imóvel (Doc 16).

Níveis I0–I4 e pesos de evidência. Regras invioláveis:
- Matrícula é evidência DECISIVA de identidade.
- Preço NUNCA prova identidade (pode coincidir entre imóveis distintos).
- Sem identidade confiável -> PENDENTE; conflito material -> BLOCK (RULE-ID-001).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum

from radar.capture.schemas import NormalizedListing


class IdentityLevel(IntEnum):
    """Força da identificação do imóvel."""

    I0_INDEFINIDA = 0
    I1_FRACA = 1
    I2_PROVAVEL = 2
    I3_FORTE = 3
    I4_PLENA = 4

    @property
    def confidence(self) -> float:
        """Confiança (0-100) associada ao nível."""
        return {0: 0.0, 1: 35.0, 2: 60.0, 3: 85.0, 4: 95.0}[int(self)]


# pesos de evidência para deduplicação (Doc 16)
EVIDENCE_WEIGHT = {
    "matricula": "DECISIVO",
    "source_ref": "FORTE",
    "endereco_area": "PROVAVEL",
    "preco": "NUNCA",  # preço nunca prova identidade
}


@dataclass
class PropertyIdentifier:
    id_type: str
    value: str
    confidence: float


@dataclass
class IdentityResult:
    level: IdentityLevel
    confidence: float
    identifiers: list[PropertyIdentifier] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def is_reliable(self) -> bool:
        """Identidade suficiente para prosseguir a análise."""
        return self.level >= IdentityLevel.I3_FORTE and not self.conflicts


def resolve_identity(listing: NormalizedListing) -> IdentityResult:
    """Determina o nível de identidade a partir do que foi capturado."""
    identifiers: list[PropertyIdentifier] = []
    notes: list[str] = []

    has_matricula = bool(listing.matricula)
    has_source_ref = bool(listing.source_ref)
    has_address = bool(listing.endereco and listing.cidade and listing.uf)
    has_area = listing.area_m2 is not None
    has_registry_ctx = bool(listing.comarca or listing.cartorio)

    if has_matricula:
        identifiers.append(PropertyIdentifier("matricula", str(listing.matricula), 95.0))
    if has_source_ref:
        identifiers.append(PropertyIdentifier("id_caixa", str(listing.source_ref), 85.0))
    if has_address:
        addr = f"{listing.endereco}, {listing.cidade}/{listing.uf}"
        identifiers.append(PropertyIdentifier("endereco", addr, 60.0))

    # nível de identidade
    if has_matricula and has_registry_ctx:
        level = IdentityLevel.I4_PLENA
    elif has_matricula or (has_source_ref and has_address):
        level = IdentityLevel.I3_FORTE
    elif has_address and has_area:
        level = IdentityLevel.I2_PROVAVEL
    elif has_address or has_source_ref:
        level = IdentityLevel.I1_FRACA
    else:
        level = IdentityLevel.I0_INDEFINIDA

    if has_matricula and not has_registry_ctx:
        notes.append("Matrícula presente sem comarca/cartório: confirmar origem registral.")
    if not has_matricula:
        notes.append("Sem matrícula: identidade não é plena; exigir certidão para BUY.")

    return IdentityResult(
        level=level,
        confidence=level.confidence,
        identifiers=identifiers,
        notes=notes,
    )


def is_same_property(a: NormalizedListing, b: NormalizedListing) -> tuple[bool | None, str]:
    """Decide se duas ofertas são o mesmo imóvel.

    Retorna (veredito, motivo). `None` = indefinido (não afirmar).
    Preço igual NUNCA é usado como prova.
    """
    if a.matricula and b.matricula:
        if _norm(a.matricula) == _norm(b.matricula):
            return True, "Matrícula idêntica (evidência decisiva)."
        return False, "Matrículas distintas (evidência decisiva de imóveis diferentes)."

    if a.source_ref and b.source_ref and _norm(a.source_ref) == _norm(b.source_ref):
        return True, "Mesmo identificador da fonte (evidência forte)."

    same_addr = (
        a.endereco
        and b.endereco
        and _norm(a.endereco) == _norm(b.endereco)
        and _norm(a.cidade or "") == _norm(b.cidade or "")
    )
    if same_addr:
        if a.area_m2 and b.area_m2 and abs(a.area_m2 - b.area_m2) <= 1.0:
            return True, "Endereço e área compatíveis (evidência provável)."
        return None, "Endereço igual, área divergente/ausente: indefinido."

    return None, "Evidências insuficientes para afirmar identidade."


def _norm(s: str) -> str:
    return " ".join(str(s).strip().lower().split())
