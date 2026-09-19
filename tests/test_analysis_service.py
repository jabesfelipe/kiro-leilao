"""Testes do serviço de análise — ciclo determinístico ponta a ponta.

Golden Case principal: item 227 do Método Jabes (dados reais da planilha).
"""

from __future__ import annotations

from radar.domain.enums import DecisionState, Strategy
from radar.services.analysis_service import AnalysisRequest, analyze


def test_golden_case_item_227_end_to_end():
    # Dados reais: lance 191.651,31; mercado provável ~300k; custos da planilha.
    req = AnalysisRequest(
        property_id="855553-227",
        strategy=Strategy.REVENDA,
        price=191_651.31,
        market_value=300_000.0,
        registro=3_000.0,
        condominio=5_000.0,
        reforma=10_000.0,
        reserva=5_000.0,
        legal_status="OK",
        confidence=90.0,
        liquidity_score=80.0,
        identity_confidence=90.0,
    )
    out = analyze(req)

    # Custo total confere com a planilha (228.066,90)
    assert abs(out.cost.total - 228_066.90) < 1.0
    # Preço acima do teto -> economia insuficiente para revenda -> DO_NOT_BUY
    assert out.decision.decision is DecisionState.DO_NOT_BUY
    assert "DO_NOT_BUY" in out.contract.explanation
    assert out.contract.economic_cost is not None


def test_bom_negocio_vira_buy():
    req = AnalysisRequest(
        property_id="teste-buy",
        strategy=Strategy.REVENDA,
        price=150_000.0,
        market_value=300_000.0,
        reforma=10_000.0,
        legal_status="OK",
        confidence=90.0,
        liquidity_score=85.0,
        identity_confidence=95.0,
        survives_conservative=True,
    )
    out = analyze(req)
    assert out.decision.decision is DecisionState.BUY
    # desconto líquido bem acima de 25%
    assert out.contract.net_discount is not None and out.contract.net_discount > 0.25


def test_block_juridico_impede_buy_mesmo_com_economia_otima():
    req = AnalysisRequest(
        property_id="teste-block",
        strategy=Strategy.REVENDA,
        price=120_000.0,
        market_value=300_000.0,
        legal_status="BLOCK",
        confidence=95.0,
        liquidity_score=90.0,
        identity_confidence=95.0,
    )
    out = analyze(req)
    assert out.decision.decision is DecisionState.BLOCK
    assert out.decision.deciding_layer.name == "LEGAL_VALIDITY"


def test_renda_com_yield_bom_vira_buy():
    # Preço tal que o yield líquido (aluguel líq ~1170/mês) fique acima de 0,8%.
    req = AnalysisRequest(
        property_id="teste-renda",
        strategy=Strategy.RENDA,
        price=125_000.0,
        market_value=250_000.0,
        rent_month=1_900.0,
        condo_month=510.0,
        iptu_month=25.0,
        maintenance_month=100.0,
        vacancy_month=95.0,
        legal_status="OK",
        confidence=90.0,
        liquidity_score=80.0,
        identity_confidence=90.0,
    )
    out = analyze(req)
    # yield líquido mensal ~1170 / ~136k ≈ 0,86% > 0,8%; desconto e margem atendem renda
    assert out.contract.net_discount is not None and out.contract.net_discount >= 0.15
    assert out.decision.decision in (DecisionState.BUY, DecisionState.BUY_IF)
