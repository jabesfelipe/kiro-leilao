"""Testes do Calculation Engine — fórmulas canônicas (Canônica §9)."""

from __future__ import annotations

import pytest

from radar.engines import calculation as calc


def test_net_discount_and_margin():
    market = 300_000.0
    tco = 228_066.90
    nd = calc.net_discount(tco, market)
    mp = calc.margin_pct(tco, market)
    assert nd == pytest.approx(0.2398, abs=1e-3)
    assert mp == pytest.approx(0.2398, abs=1e-3)


def test_build_cost_matches_metodo_jabes_item_227():
    # Dados reais da planilha Método Jabes (aba 04 - Financeiro)
    cost = calc.build_cost(
        preco=191_651.31,
        commission_pct=0.05,
        itbi_pct=0.02,
        registro=3_000.0,
        condominio=5_000.0,
        reforma=10_000.0,
        reserva=5_000.0,
    )
    # Planilha: CUSTO TOTAL AQUISIÇÃO = 228.066,9017
    assert cost.total == pytest.approx(228_066.90, abs=1.0)


def test_yields():
    tco = 228_066.90
    assert calc.gross_monthly_yield(1_900.0, tco) == pytest.approx(0.00833, abs=1e-4)
    net = calc.net_monthly_yield(1_900.0, 510.0, 25.0, 100.0, 95.0, tco)
    assert net == pytest.approx(0.00513, abs=1e-4)


def test_max_price_by_target_roi_below_current_bid():
    # ROI alvo 25% deve produzir teto abaixo do lance mínimo (191.651) -> não compensa
    max_price = calc.max_price_by_target_roi(
        market_value=300_000.0,
        fixed_costs=23_000.0,
        commission_pct=0.05,
        sale_commission_pct=0.06,
        income_tax_pct=0.15,
        target_roi=0.25,
    )
    assert max_price < 191_651.31
