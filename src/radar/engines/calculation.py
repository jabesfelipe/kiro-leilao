"""Calculation Engine — cálculos determinísticos.

Fonte de verdade: Canônica §9. Nenhum cálculo aqui depende de LLM.
"O LLM não substitui cálculos financeiros" (arquitetura §2).
"""

from __future__ import annotations

from radar.domain.models import CostBreakdown


def market_discount(preco: float, market_value: float) -> float:
    """Desconto sobre valor de mercado = 1 - (preco / valor de mercado)."""
    if market_value <= 0:
        raise ValueError("market_value deve ser > 0")
    return 1 - (preco / market_value)


def net_discount(tco: float, market_value: float) -> float:
    """Desconto líquido = 1 - (custo econômico total / valor de mercado). Decisório."""
    if market_value <= 0:
        raise ValueError("market_value deve ser > 0")
    return 1 - (tco / market_value)


def margin(tco: float, market_value: float) -> float:
    """Margem absoluta = valor de mercado - TCO."""
    return market_value - tco


def margin_pct(tco: float, market_value: float) -> float:
    """Margem % = (valor de mercado - TCO) / valor de mercado."""
    if market_value <= 0:
        raise ValueError("market_value deve ser > 0")
    return (market_value - tco) / market_value


def gross_monthly_yield(rent_month: float, tco: float) -> float:
    """Yield mensal bruto = aluguel mensal / TCO."""
    if tco <= 0:
        raise ValueError("tco deve ser > 0")
    return rent_month / tco


def gross_annual_yield(rent_month: float, tco: float) -> float:
    return gross_monthly_yield(rent_month, tco) * 12


def net_monthly_yield(
    rent_month: float,
    condo: float,
    iptu: float,
    maintenance: float,
    vacancy: float,
    tco: float,
) -> float:
    """Yield líquido mensal = (aluguel - custos recorrentes) / TCO."""
    if tco <= 0:
        raise ValueError("tco deve ser > 0")
    net_rent = rent_month - condo - iptu - maintenance - vacancy
    return net_rent / tco


def max_price_by_target_roi(
    market_value: float,
    fixed_costs: float,
    commission_pct: float,
    sale_commission_pct: float,
    income_tax_pct: float,
    target_roi: float,
) -> float:
    """Preço máximo por ROI alvo (backward), Canônica §9 / Método Jabes.

    Resolve o preço tal que o ROI líquido resultante == target_roi.

    ROI = lucro_liquido / custo_total_aquisicao
    venda_liquida = market_value * (1 - sale_commission_pct)
                    - income_tax sobre o ganho
    Simplificação PF flat de IR (marcada como pendência na Canônica §9).

    custo_total = preco * (1 + commission_pct) + fixed_costs
    Resolve-se preco para que:
        (venda_liquida - custo_total) / custo_total = target_roi
    => custo_total = venda_liquida / (1 + target_roi)
    => preco = (custo_total - fixed_costs) / (1 + commission_pct)
    """
    if commission_pct < 0 or target_roi < -1:
        raise ValueError("parâmetros inválidos")
    sale_net_before_tax = market_value * (1 - sale_commission_pct)
    # IR incide sobre o ganho aproximado (venda liquida - custo). Como custo depende
    # do preço, usamos aproximação sobre a base venda para manter determinismo simples.
    sale_net = sale_net_before_tax - (income_tax_pct * max(0.0, sale_net_before_tax - fixed_costs))
    total_cost = sale_net / (1 + target_roi)
    price = (total_cost - fixed_costs) / (1 + commission_pct)
    return max(0.0, price)


def build_cost(
    preco: float,
    *,
    commission_pct: float = 0.05,
    itbi_pct: float = 0.02,
    registro: float = 0.0,
    condominio: float = 0.0,
    tributos: float = 0.0,
    reforma: float = 0.0,
    reserva: float = 0.0,
    custo_juridico_potencial: float = 0.0,
    prob_juridica: float = 0.0,
    carrying: float = 0.0,
) -> CostBreakdown:
    """Monta o CostBreakdown aplicando percentuais sobre o preço."""
    return CostBreakdown(
        preco=preco,
        comissao_leiloeiro=preco * commission_pct,
        itbi=preco * itbi_pct,
        registro_documentacao=registro,
        condominio_debitos=condominio,
        tributos_debitos=tributos,
        reforma=reforma,
        reserva_imprevistos=reserva,
        custo_juridico_esperado=custo_juridico_potencial * prob_juridica,
        carrying=carrying,
    )
