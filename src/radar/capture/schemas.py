"""Contratos de captura e normalização.

Princípios (Doc 16 / arquitetura §8):
- A captura original é PRESERVADA e imutável (hash + payload cru).
- Normalização não descarta o original; produz uma visão estruturada.
- Campo ausente é UNKNOWN, nunca zero nem "regular".
"""

from __future__ import annotations

import hashlib
import json
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field


class RawCapture(BaseModel):
    """Payload cru de uma fonte, preservado como veio."""

    source_type: str = Field(description="caixa | leiloeiro | portal | cartorio")
    source_name: str
    payload: dict[str, Any]
    captured_at: datetime

    @property
    def fingerprint(self) -> str:
        """Hash estável do conteúdo (dedup de captura)."""
        blob = json.dumps(self.payload, sort_keys=True, ensure_ascii=False, default=str)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()


class NormalizedListing(BaseModel):
    """Visão normalizada de uma oferta. Campos desconhecidos ficam None (UNKNOWN)."""

    # identificação
    source_ref: str | None = Field(default=None, description="ID do imóvel na fonte")
    matricula: str | None = None
    comarca: str | None = None
    cartorio: str | None = None

    # localização e físico
    endereco: str | None = None
    cidade: str | None = None
    uf: str | None = None
    bairro: str | None = None
    cep: str | None = None
    tipo_imovel: str | None = None
    area_m2: float | None = None
    quartos: int | None = None
    vagas: int | None = None

    # leilão / comercial
    edital: str | None = None
    item: str | None = None
    modalidade: str | None = None
    auction_date: datetime | None = None
    min_bid: float | None = None
    avaliacao_fonte: float | None = None
    comissao_leiloeiro_pct: float | None = None
    forma_pagamento: str | None = None
    leiloeiro: str | None = None

    # situação
    ocupado: bool | None = None
    situacao_texto: str | None = None

    # jurídico (indícios vindos da fonte; evidência real vem de documentos)
    consolidacao_averbada: bool | None = None
    consolidacao_data: date | None = None
    leiloes_negativos_averbados: bool | None = None

    # rastreabilidade
    observed_at: date | None = None
    links: list[str] = Field(default_factory=list)

    def missing_fields(self) -> list[str]:
        """Campos relevantes ausentes (viram UNKNOWN/PENDENTE adiante)."""
        relevant = [
            "matricula",
            "endereco",
            "cidade",
            "uf",
            "area_m2",
            "min_bid",
            "edital",
            "auction_date",
        ]
        return [f for f in relevant if getattr(self, f) is None]
