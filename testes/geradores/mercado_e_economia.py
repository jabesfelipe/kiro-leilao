"""Geradores de mercado, valuation, custo e economia (`R21` a `R33`, `R96`).

A `ComposicaoDeCusto` gerada aqui tem os **treze** componentes de `R26.1`, cada um como
`Informado[Decimal]` e cada um podendo vir `DESCONHECIDO`. É essa possibilidade que dá sentido às
propriedades de conservação e de provisoriedade: se o gerador nunca produzisse componente
desconhecido, a conversão de desconhecido em zero (`SAFE-005`, `D.10.8`) passaria sem ser vista.

As entradas de preço máximo incluem a combinação exata de `REG-033`, que é o contraexemplo do teto
conservador. Ela entra como valor de fronteira, não como caso aleatório improvável.

Camada de infraestrutura de teste: nenhuma entrada e saída de dados.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Final

from hypothesis import strategies as st

from radar.nucleo.enumeracoes import (
    ClasseDeComparavel,
    MetodoDeValuation,
    NivelDeReforma,
    PerfilDeAtivo,
    TipoDeCenario,
)
from radar.nucleo.informado import Informado
from testes.geradores.escalas import (
    AreaDeclarada,
    area,
    data_hora_br,
    dinheiro,
    escala_de_zero_a_cem,
    informado,
)

__all__ = [
    "COMPONENTES_DO_CUSTO_ECONOMICO_TOTAL",
    "ENTRADAS_DE_PRECO_MAXIMO_DE_REG_033",
    "Comparavel",
    "ComposicaoDeCusto",
    "EntradasDePrecoMaximo",
    "EntradasDeValuation",
    "EntradasEconomicas",
    "PremissasDeCenario",
    "comparavel",
    "composicao_de_custo",
    "entradas_de_preco_maximo",
    "entradas_de_valuation",
    "entradas_economicas",
    "premissas_de_cenario",
]

COMPONENTES_DO_CUSTO_ECONOMICO_TOTAL: Final[tuple[str, ...]] = (
    "preco",
    "comissao_do_leiloeiro",
    "itbi_e_tributos_de_aquisicao",
    "registro_e_documentacao",
    "debitos_de_condominio",
    "debitos_tributarios",
    "regularizacao",
    "reforma",
    "desocupacao",
    "reserva_para_imprevistos",
    "custo_juridico_esperado",
    "carregamento",
    "custo_financeiro",
)
"""Os treze componentes de `R26.1`, na ordem do design. A contagem é contrato.

Corretagem de venda e imposto de renda sobre ganho de capital **não** estão aqui: pertencem à
perna de venda (`R26.1.1`). O custo de oportunidade do capital também não: o retorno exigido já é
cobrado pelo limiar `GLB-011` (`R26.1.2`).
"""


@dataclass(frozen=True, slots=True, kw_only=True)
class Comparavel:
    """Comparável de mercado com classe, distância e idade do anúncio (`R21`, `CMP-*`)."""

    identificador: str
    classe: ClasseDeComparavel
    preco: Decimal
    area_declarada: AreaDeclarada
    distancia_em_km: Decimal
    idade_do_anuncio_em_meses: int
    mesmo_condominio: bool
    observado_em: datetime


def comparavel() -> st.SearchStrategy[Comparavel]:
    """Comparável válido, incluindo classe `U` e os limites de `CMP-003` e `CMP-011`.

    Distância e idade são geradas **além** dos limites (1,0 km e 12 meses) de propósito: seleção
    que aceitasse comparável fora do raio ou fora da janela é defeito, e o gerador precisa
    oferecer o caso para que a propriedade o recuse.
    """
    return st.builds(
        Comparavel,
        identificador=st.text(min_size=1, max_size=16),
        classe=st.sampled_from(ClasseDeComparavel),
        preco=dinheiro(),
        area_declarada=area(),
        distancia_em_km=st.one_of(
            st.sampled_from((Decimal("0.0"), Decimal("1.0"), Decimal("1.1"), Decimal("2.0"))),
            st.decimals(min_value=Decimal(0), max_value=Decimal(5), places=2, allow_nan=False),
        ),
        idade_do_anuncio_em_meses=st.one_of(
            st.sampled_from((0, 6, 12, 13, 24)),
            st.integers(min_value=0, max_value=36),
        ),
        mesmo_condominio=st.booleans(),
        observado_em=data_hora_br(),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class EntradasDeValuation:
    """Entradas de um valuation: amostra, método, perfil e confiança (`R23`, `R24`)."""

    comparaveis: tuple[Comparavel, ...]
    metodo: MetodoDeValuation
    perfil_de_ativo: PerfilDeAtivo
    confianca: Decimal
    avaliacao_da_fonte: Informado[Decimal]


def entradas_de_valuation() -> st.SearchStrategy[EntradasDeValuation]:
    """Entradas de valuation com amostra de 0 a 9 comparáveis.

    A amostra vazia e a amostra abaixo de `VAL-001` (5) são geradas: valuation sem comparável
    suficiente tem de reduzir confiança e abrir pendência, não produzir número confiante.
    """
    return st.builds(
        EntradasDeValuation,
        comparaveis=st.lists(comparavel(), min_size=0, max_size=9).map(tuple),
        metodo=st.sampled_from(MetodoDeValuation),
        perfil_de_ativo=st.sampled_from(PerfilDeAtivo),
        confianca=escala_de_zero_a_cem(),
        avaliacao_da_fonte=informado(dinheiro()),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class ComposicaoDeCusto:
    """Os treze componentes de `R26.1`, cada um individualmente consultável (`R26.11`).

    Nenhum componente tem default numérico. `DESCONHECIDO` propaga contingência e marca o preço
    máximo como provisório; nunca vale zero (`R26.10`, `SAFE-005`).
    """

    preco: Informado[Decimal]
    comissao_do_leiloeiro: Informado[Decimal]
    itbi_e_tributos_de_aquisicao: Informado[Decimal]
    registro_e_documentacao: Informado[Decimal]
    debitos_de_condominio: Informado[Decimal]
    debitos_tributarios: Informado[Decimal]
    regularizacao: Informado[Decimal]
    reforma: Informado[Decimal]
    desocupacao: Informado[Decimal]
    reserva_para_imprevistos: Informado[Decimal]
    custo_juridico_esperado: Informado[Decimal]
    carregamento: Informado[Decimal]
    custo_financeiro: Informado[Decimal]


def composicao_de_custo(
    *,
    permitir_desconhecido: bool = True,
) -> st.SearchStrategy[ComposicaoDeCusto]:
    """Composição de custo com os treze componentes.

    `permitir_desconhecido=False` é a porta para as propriedades de conservação de valor, que
    exigem os treze presentes para somar. Excluir a ausência é decisão declarada na chamada, não
    default silencioso do gerador.
    """
    componente = informado(dinheiro(), permitir_desconhecido=permitir_desconhecido)
    return st.builds(
        ComposicaoDeCusto,
        **dict.fromkeys(COMPONENTES_DO_CUSTO_ECONOMICO_TOTAL, componente),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class EntradasEconomicas:
    """Entradas das métricas de `R27`: custo, mercado, aluguel, prazo e alíquotas."""

    custo_economico_total: Decimal
    valor_de_mercado_base: Decimal
    valor_de_mercado_conservador: Decimal
    aluguel_bruto_mensal: Informado[Decimal]
    prazo_em_meses: int
    custo_de_venda_percentual: Decimal
    ir_ganho_de_capital_percentual: Decimal


def entradas_economicas() -> st.SearchStrategy[EntradasEconomicas]:
    """Entradas econômicas coerentes: o valor conservador nunca supera o valor base.

    Gerar o par sem essa restrição produziria contraexemplos que provam apenas que o gerador está
    errado — a distinção de `D.1.6` é de referência, e a ordem entre as duas referências é parte
    da definição das faixas de valor (`R23.5`).
    """
    return st.builds(
        _entradas_economicas_coerentes,
        custo=dinheiro(),
        mercado_base=dinheiro(),
        reducao_conservadora=st.decimals(
            min_value=Decimal("0.00"),
            max_value=Decimal("0.30"),
            places=2,
            allow_nan=False,
        ),
        aluguel=informado(dinheiro()),
        prazo_em_meses=st.sampled_from((0, 3, 6, 12, 24, 36)),
        custo_de_venda_percentual=st.sampled_from((Decimal("0.00"), Decimal("0.06"))),
        ir_ganho_de_capital_percentual=st.sampled_from((Decimal("0.00"), Decimal("0.15"))),
    )


def _entradas_economicas_coerentes(
    *,
    custo: Decimal,
    mercado_base: Decimal,
    reducao_conservadora: Decimal,
    aluguel: Informado[Decimal],
    prazo_em_meses: int,
    custo_de_venda_percentual: Decimal,
    ir_ganho_de_capital_percentual: Decimal,
) -> EntradasEconomicas:
    return EntradasEconomicas(
        custo_economico_total=custo,
        valor_de_mercado_base=mercado_base,
        valor_de_mercado_conservador=mercado_base * (Decimal(1) - reducao_conservadora),
        aluguel_bruto_mensal=aluguel,
        prazo_em_meses=prazo_em_meses,
        custo_de_venda_percentual=custo_de_venda_percentual,
        ir_ganho_de_capital_percentual=ir_ganho_de_capital_percentual,
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class EntradasDePrecoMaximo:
    """Entradas da forma fechada do preço máximo por ROI alvo (`R28.2`, `R28.2.1`)."""

    valor_de_mercado: Decimal
    custo_de_venda_percentual: Decimal
    custos_fixos: Decimal
    comissao_percentual: Decimal
    roi_alvo: Decimal
    ir_percentual: Decimal
    itbi_percentual: Decimal


ENTRADAS_DE_PRECO_MAXIMO_DE_REG_033: Final[EntradasDePrecoMaximo] = EntradasDePrecoMaximo(
    valor_de_mercado=Decimal(300_000),
    custo_de_venda_percentual=Decimal("0.06"),
    custos_fixos=Decimal(23_000),
    comissao_percentual=Decimal("0.05"),
    roi_alvo=Decimal("0.25"),
    ir_percentual=Decimal(0),
    itbi_percentual=Decimal(0),
)
"""A entrada completa e obrigatória de `REG-033`: o contraexemplo do teto conservador.

Com ela o teto conservador de R$ 199.230,77 **excede** o preço máximo exato de R$ 192.952,38. É
por isso que o teto conservador é informativo e o teto decisório é o mínimo entre o exato e o
ajustado ao risco (`D28`).
"""


def entradas_de_preco_maximo() -> st.SearchStrategy[EntradasDePrecoMaximo]:
    """Entradas do preço máximo, com a combinação de `REG-033` sempre no espaço de geração."""
    amostrado = st.builds(
        EntradasDePrecoMaximo,
        valor_de_mercado=dinheiro(),
        custo_de_venda_percentual=st.sampled_from((Decimal("0.00"), Decimal("0.06"))),
        custos_fixos=dinheiro(),
        comissao_percentual=st.sampled_from((Decimal("0.00"), Decimal("0.05"))),
        roi_alvo=st.sampled_from((Decimal("0.15"), Decimal("0.25"), Decimal("0.30"))),
        ir_percentual=st.sampled_from((Decimal("0.00"), Decimal("0.15"))),
        itbi_percentual=st.sampled_from((Decimal("0.00"), Decimal("0.02"))),
    )
    return st.one_of(st.just(ENTRADAS_DE_PRECO_MAXIMO_DE_REG_033), amostrado)


@dataclass(frozen=True, slots=True, kw_only=True)
class PremissasDeCenario:
    """Premissas de um dos quatro cenários de `R32.1`."""

    tipo: TipoDeCenario
    fator_sobre_o_valor_de_mercado: Decimal
    prazo_em_meses: int
    nivel_de_reforma: NivelDeReforma
    contingencia_percentual: Decimal


def premissas_de_cenario() -> st.SearchStrategy[PremissasDeCenario]:
    """Premissas de cenário com as contingências exatas de `CUS-017` por nível de reforma."""
    contingencias = (
        Decimal("0.00"),
        Decimal("0.10"),
        Decimal("0.15"),
        Decimal("0.25"),
        Decimal("0.50"),
    )
    return st.builds(
        PremissasDeCenario,
        tipo=st.sampled_from(TipoDeCenario),
        fator_sobre_o_valor_de_mercado=st.sampled_from(
            (Decimal("0.80"), Decimal("0.90"), Decimal("1.00"), Decimal("1.10"))
        ),
        prazo_em_meses=st.sampled_from((0, 3, 6, 12, 24, 36)),
        nivel_de_reforma=st.sampled_from(NivelDeReforma),
        contingencia_percentual=st.sampled_from(contingencias),
    )
