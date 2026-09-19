"""Testes do Decision Engine — precedência canônica (Canônica §1).

Inclui Golden Cases derivados do Método Jabes e do caso Milano.
"""

from __future__ import annotations

from radar.domain.enums import DecisionLayer, DecisionState, Strategy
from radar.engines.decision import DecisionInput, decide


def _base(**over) -> DecisionInput:
    args = dict(
        legal_status="OK",
        has_critical_block=False,
        is_eligible=True,
        confidence=90.0,
        net_discount=0.30,
        margin_pct=0.25,
        liquidity_score=80.0,
        strategy=Strategy.REVENDA,
        opportunity_score=85.0,
        survives_conservative=True,
        net_monthly_yield=None,
    )
    args.update(over)
    return DecisionInput(**args)  # type: ignore[arg-type]


def test_block_juridico_supera_score_alto():
    # Regra inviolável: BLOCK jurídico não é compensado por score.
    r = decide(_base(legal_status="BLOCK", opportunity_score=99.0))
    assert r.decision is DecisionState.BLOCK
    assert r.deciding_layer is DecisionLayer.LEGAL_VALIDITY


def test_critical_block_bloqueia():
    r = decide(_base(has_critical_block=True))
    assert r.decision is DecisionState.BLOCK
    assert r.deciding_layer is DecisionLayer.CRITICAL_BLOCKS


def test_golden_case_item_227_preco_acima_do_teto():
    # Método Jabes item 227: bom imóvel, mas economia insuficiente (veredito E econômico).
    # desconto líquido ~24% < mínimo 25% para revenda.
    r = decide(_base(net_discount=0.2398, margin_pct=0.2398))
    assert r.decision is DecisionState.DO_NOT_BUY
    assert r.deciding_layer is DecisionLayer.ECONOMICS


def test_caso_bom_mas_pendente_vira_monitor():
    r = decide(_base(legal_status="PENDENTE"))
    assert r.decision is DecisionState.MONITOR
    assert r.deciding_layer is DecisionLayer.ACTION


def test_buy_quando_tudo_atende():
    r = decide(_base())
    assert r.decision is DecisionState.BUY
    assert r.deciding_layer is DecisionLayer.ACTION


def test_nao_sobrevive_conservador_vira_buy_if():
    r = decide(_base(survives_conservative=False))
    assert r.decision is DecisionState.BUY_IF
    assert r.deciding_layer is DecisionLayer.SCENARIO


def test_renda_reprova_por_yield_baixo():
    r = decide(
        _base(
            strategy=Strategy.RENDA,
            net_discount=0.20,
            margin_pct=0.15,
            net_monthly_yield=0.005,  # abaixo de 0,8%
        )
    )
    assert r.decision is DecisionState.DO_NOT_BUY
    assert r.deciding_layer is DecisionLayer.STRATEGY
