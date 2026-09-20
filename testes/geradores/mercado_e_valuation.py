"""Geradores de mercado e valuation das propriedades `P18` (`R21` a `R25`, `VAL-*`, `CMP-*`).

O que este módulo acrescenta ao módulo de mercado e economia é a **amostra** como objeto de
primeira classe: conjunto de comparáveis com quantidade, dispersão e outliers controlados, e o par
raio × janela nos limites exatos de `VAL-003` e `VAL-004`.

Quantidade de comparáveis é gerada em torno de `VAL-001` (5) e `VAL-011` (7), porque é aí que a
confiança do valuation muda de patamar; gerar só amostras grandes esconderia o caso em que o
método deveria recuar.

Camada de infraestrutura de teste: nenhuma entrada e saída de dados.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Final

from hypothesis import strategies as st

from radar.nucleo.enumeracoes import (
    ClasseDeComparavel,
    MetodoDeValuation,
    PerfilDeAtivo,
)
from testes.geradores.escalas import escala_de_zero_a_cem
from testes.geradores.mercado_e_economia import Comparavel, comparavel

__all__ = [
    "IDADE_MAXIMA_DO_ANUNCIO_EM_MESES",
    "JANELA_TEMPORAL_MAXIMA_EM_MESES",
    "QUANTIDADE_IDEAL_DE_COMPARAVEIS",
    "QUANTIDADE_MINIMA_DE_COMPARAVEIS",
    "RAIO_MAXIMO_EM_KM",
    "PremissasDeValuation",
    "RaioEJanela",
    "conjunto_de_comparaveis",
    "premissas_de_valuation",
    "raio_e_janela",
    "tipo_de_ativo",
]

QUANTIDADE_MINIMA_DE_COMPARAVEIS: Final[int] = 5
"""`VAL-001`. Abaixo disso o valuation reduz confiança e abre pendência."""

QUANTIDADE_IDEAL_DE_COMPARAVEIS: Final[int] = 7
"""`VAL-011`. Limiar único, não faixa (`D30`)."""

RAIO_MAXIMO_EM_KM: Final[Decimal] = Decimal("1.0")
"""`VAL-003` e `CMP-003`, alinhados entre si."""

JANELA_TEMPORAL_MAXIMA_EM_MESES: Final[int] = 12
"""`VAL-004`."""

IDADE_MAXIMA_DO_ANUNCIO_EM_MESES: Final[int] = 12
"""`CMP-011`. Além de 6 meses o peso cai 50% por `CMP-013`."""


def conjunto_de_comparaveis() -> st.SearchStrategy[tuple[Comparavel, ...]]:
    """Amostra de comparáveis de 0 a 12, com as quantidades de fronteira sempre presentes.

    As quantidades injetadas são 0, 1, 4, 5, 6, 7 e 8: em volta de `VAL-001` e de `VAL-011`. É a
    vizinhança desses dois números que separa valuation confiável de valuation que deveria recuar,
    e uma amostragem puramente uniforme visitaria pouco os casos pequenos.
    """
    quantidades = st.one_of(
        st.sampled_from((0, 1, 4, 5, 6, 7, 8)),
        st.integers(min_value=0, max_value=12),
    )
    return quantidades.flatmap(
        lambda quantidade: st.lists(
            comparavel(),
            min_size=quantidade,
            max_size=quantidade,
        ).map(tuple)
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class PremissasDeValuation:
    """Premissas de um valuation: método, perfil, pesos e margem conservadora (`R23`, `R24`)."""

    metodo: MetodoDeValuation
    perfil_de_ativo: PerfilDeAtivo
    classe_minima_aceita: ClasseDeComparavel
    priorizar_mesmo_condominio: bool
    peso_de_mesmo_condominio: Decimal
    margem_conservadora: Decimal
    confianca_exigida: Decimal


def premissas_de_valuation() -> st.SearchStrategy[PremissasDeValuation]:
    """Premissas com `VAL-006` (2,0×), `VAL-008` (0,10) e `VAL-009` (70) nas fronteiras.

    `VAL-008` é o parâmetro reintroduzido por `D15` — a fração subtraída do valor base para obter
    o conservador. Sem ele, a distinção de referência de `D.1.6` não tem número.
    """
    return st.builds(
        PremissasDeValuation,
        metodo=st.sampled_from(MetodoDeValuation),
        perfil_de_ativo=st.sampled_from(PerfilDeAtivo),
        classe_minima_aceita=st.sampled_from(ClasseDeComparavel),
        priorizar_mesmo_condominio=st.booleans(),
        peso_de_mesmo_condominio=st.sampled_from(
            (Decimal("1.0"), Decimal("2.0"), Decimal("2.5"))
        ),
        margem_conservadora=st.sampled_from(
            (Decimal("0.05"), Decimal("0.10"), Decimal("0.15"))
        ),
        confianca_exigida=escala_de_zero_a_cem(),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class RaioEJanela:
    """Par raio × janela da seleção de comparáveis (`VAL-003`, `VAL-004`)."""

    raio_em_km: Decimal
    janela_em_meses: int


def raio_e_janela() -> st.SearchStrategy[RaioEJanela]:
    """Raio e janela nos limites exatos e imediatamente além deles.

    No limite exato o comparável **está** dentro do raio e da janela: a comparação é `<=`. Por isso
    1,0 km e 12 meses entram de propósito, ao lado de 1,1 km e 13 meses, que estão fora.
    """
    return st.builds(
        RaioEJanela,
        raio_em_km=st.sampled_from(
            (
                Decimal("0.0"),
                Decimal("0.5"),
                RAIO_MAXIMO_EM_KM,
                Decimal("1.1"),
                Decimal("2.0"),
            )
        ),
        janela_em_meses=st.sampled_from(
            (0, 6, JANELA_TEMPORAL_MAXIMA_EM_MESES, JANELA_TEMPORAL_MAXIMA_EM_MESES + 1, 24)
        ),
    )


def tipo_de_ativo() -> st.SearchStrategy[PerfilDeAtivo]:
    """Perfil de ativo nos nove valores, `DESCONHECIDO` incluído.

    Perfil de ativo **não** é estratégia (`D.6.5`): são dois enums, e o método de valuation por
    tipo de ativo (`R24`) despacha por este, não por aquele.
    """
    return st.sampled_from(PerfilDeAtivo)
