"""Testes de captura/normalização da Caixa e dos parsers pt-BR."""

from __future__ import annotations

from datetime import datetime

from radar.capture.caixa import normalize_caixa
from radar.capture.parsing import (
    parse_area,
    parse_money,
    parse_occupancy,
    parse_percent,
)
from radar.capture.schemas import RawCapture

# payload cru como aparece numa listagem da Caixa (item 227 do edital 0031/0326)
PAYLOAD_227 = {
    "Número do imóvel": "855553513794-2",
    "Matrícula": "71502",
    "Endereço": "Rua Exemplo, 100, apto 42",
    "Cidade": "Ribeirão Preto",
    "UF": "SP",
    "Tipo de imóvel": "Apartamento",
    "Área privativa": "47,76 m²",
    "Quartos": "3",
    "Vagas": "1",
    "Edital": "0031/0326-CPVE/RE",
    "Item": "227",
    "Data do leilão": "15/09/2026 10:00",
    "Valor mínimo": "R$ 191.651,31",
    "Valor de avaliação": "R$ 313.000,00",
    "Comissão do leiloeiro": "5%",
    "Leiloeiro": "Nasar Leilões",
    "Situação": "Desocupado",
    "Formas de pagamento": "Recursos próprios / FGTS; sem financiamento",
}


def _capture(payload: dict) -> RawCapture:
    return RawCapture(
        source_type="caixa",
        source_name="Portal Caixa",
        payload=payload,
        captured_at=datetime(2026, 9, 14, 10, 0),
    )


def test_parsers_ptbr():
    assert parse_money("R$ 191.651,31") == 191651.31
    assert parse_money(191651.31) == 191651.31
    assert parse_money("") is None
    assert parse_area("47,76 m²") == 47.76
    assert parse_percent("5%") == 0.05
    assert parse_percent(5) == 0.05
    assert parse_percent(0.05) == 0.05
    # "desocupado" não pode ser lido como "ocupado" (substring)
    assert parse_occupancy("Desocupado") is False
    assert parse_occupancy("Ocupado") is True
    assert parse_occupancy("") is None


def test_normalize_item_227():
    listing = normalize_caixa(_capture(PAYLOAD_227))
    assert listing.source_ref == "855553513794-2"
    assert listing.matricula == "71502"
    assert listing.min_bid == 191651.31
    assert listing.avaliacao_fonte == 313000.00
    assert listing.area_m2 == 47.76
    assert listing.quartos == 3
    assert listing.comissao_leiloeiro_pct == 0.05
    assert listing.ocupado is False
    assert listing.auction_date == datetime(2026, 9, 15, 10, 0)
    assert listing.item == "227"


def test_campos_ausentes_ficam_unknown():
    """Campo ausente é None (UNKNOWN), nunca zero."""
    listing = normalize_caixa(_capture({"Cidade": "Campinas"}))
    assert listing.min_bid is None
    assert listing.area_m2 is None
    assert listing.matricula is None
    assert "matricula" in listing.missing_fields()
    assert "min_bid" in listing.missing_fields()


def test_fingerprint_estavel():
    a = _capture(PAYLOAD_227).fingerprint
    b = _capture(dict(reversed(list(PAYLOAD_227.items())))).fingerprint
    assert a == b  # ordem das chaves não altera o hash
