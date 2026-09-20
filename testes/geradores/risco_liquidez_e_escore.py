"""Geradores de risco, liquidez, escore e portfólio (`R34` a `R52`, `SCORE-*`).

Todos os fatores vivem na escala `[0, 100]` e vêm de `escala_de_zero_a_cem()`: é por esse caminho
que 89,5 · 79,5 · 74,5 · 69,5 · 59,5 · 49,5 · 39,5 chegam a toda propriedade de faixa de escore,
de liquidez e de fator de confiança. Sem isso, `D.1.5` voltaria pela porta de trás.

`conjunto_de_pesos()` gera pesos que somam exatamente 1,00, porque é isso que `SCORE-001` e
`SCORE-002` declaram; conjunto que não fecha é entrada inválida, não caso de teste.

Camada de infraestrutura de teste: nenhuma entrada e saída de dados.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from typing import Final

from hypothesis import strategies as st

from radar.nucleo.enumeracoes import (
    CategoriaDeRisco,
    Estrategia,
    Impacto,
    Mitigacao,
    Probabilidade,
    QualidadeDaEvidencia,
    Severidade,
)
from testes.geradores.escalas import escala_de_zero_a_cem

__all__ = [
    "FATORES_DE_LIQUIDEZ",
    "FATORES_DO_ESCORE_DE_OPORTUNIDADE",
    "FATORES_DO_INVESTOR_FIT",
    "EstadoDePortfolio",
    "RegistroDeRisco",
    "conjunto_de_pesos",
    "estado_de_portfolio",
    "fatores_de_escore",
    "fatores_de_liquidez",
    "registro_de_risco",
]

FATORES_DO_ESCORE_DE_OPORTUNIDADE: Final[tuple[str, ...]] = (
    "desconto_liquido",
    "margem_seguranca",
    "liquidez",
    "localizacao",
    "risco",
    "yield_renda",
    "valorizacao",
    "qualidade_oportunidade",
)
"""Os oito fatores de `SCORE-001`. `qualidade_oportunidade` está presente de propósito: era o
fator cujo peso efetivo por estratégia era zero antes de `D22`."""

FATORES_DO_INVESTOR_FIT: Final[tuple[str, ...]] = (
    "aderencia_estrategia",
    "aderencia_risco",
    "liquidez_vs_necessidade",
    "aderencia_capital",
    "diversificacao",
    "esforco_operacional",
    "horizonte",
)
"""Os sete pesos de aderência de `SCORE-006`. `qualidade economica` foi excluída: ela é o
Opportunity Score, e incluí-la no Fit misturaria os dois escores (`D21`)."""

FATORES_DE_LIQUIDEZ: Final[tuple[str, ...]] = (
    "demanda_regional",
    "publico_alvo",
    "tempo_de_anuncio",
    "concorrencia",
    "financiabilidade",
    "faixa_de_ticket",
)
"""Fatores que alimentam o escore de liquidez de `R40`."""


@dataclass(frozen=True, slots=True, kw_only=True)
class RegistroDeRisco:
    """Risco registrado com probabilidade, impacto, severidade e mitigação (`R34`).

    A severidade é gerada junto com o par probabilidade × impacto para que a propriedade possa
    confrontar a matriz em lugar de reimplementá-la. Risco de severidade `critico` com evidência
    `ESTIMADO` é o caso de `REG-035`: bloqueio por risco crítico presumido, com condição objetiva
    de desbloqueio — e o gerador o produz.
    """

    categoria: CategoriaDeRisco
    probabilidade: Probabilidade
    impacto: Impacto
    severidade: Severidade
    qualidade_da_evidencia: QualidadeDaEvidencia
    mitigacao: Mitigacao
    condicao_de_desbloqueio: str


def registro_de_risco() -> st.SearchStrategy[RegistroDeRisco]:
    """Registro de risco em todas as combinações das dez categorias."""
    return st.builds(
        RegistroDeRisco,
        categoria=st.sampled_from(CategoriaDeRisco),
        probabilidade=st.sampled_from(Probabilidade),
        impacto=st.sampled_from(Impacto),
        severidade=st.sampled_from(Severidade),
        qualidade_da_evidencia=st.sampled_from(QualidadeDaEvidencia),
        mitigacao=st.sampled_from(Mitigacao),
        condicao_de_desbloqueio=st.text(min_size=1, max_size=60),
    )


def fatores_de_liquidez() -> st.SearchStrategy[Mapping[str, Decimal]]:
    """Fatores de liquidez, todos na escala `[0, 100]` com os valores de fronteira injetados."""
    return st.fixed_dictionaries(
        {nome: escala_de_zero_a_cem() for nome in FATORES_DE_LIQUIDEZ}
    )


def fatores_de_escore() -> st.SearchStrategy[Mapping[str, Decimal]]:
    """Os oito fatores do Opportunity Score, na escala `[0, 100]`.

    Cada fator visita 89,5 e os seis irmãos: a faixa do escore (`SCORE-003`) é classificada por
    limite inferior, e é no fracionário que a versão anterior deixava valor sem classe.
    """
    return st.fixed_dictionaries(
        {nome: escala_de_zero_a_cem() for nome in FATORES_DO_ESCORE_DE_OPORTUNIDADE}
    )


def _pesos_normalizados(nomes: tuple[str, ...], brutos: tuple[int, ...]) -> Mapping[str, Decimal]:
    """Distribui 1,00 entre os nomes, com o resto no último — a soma fecha exatamente."""
    total = sum(brutos)
    pesos: dict[str, Decimal] = {}
    acumulado = Decimal(0)
    for nome, bruto in zip(nomes[:-1], brutos[:-1], strict=True):
        peso = (Decimal(bruto) / Decimal(total)).quantize(Decimal("0.01"))
        pesos[nome] = peso
        acumulado += peso
    pesos[nomes[-1]] = Decimal("1.00") - acumulado
    return pesos


def conjunto_de_pesos(
    nomes: tuple[str, ...] = FATORES_DO_ESCORE_DE_OPORTUNIDADE,
) -> st.SearchStrategy[Mapping[str, Decimal]]:
    """Conjunto de pesos que soma exatamente 1,00 (`SCORE-001`, `SCORE-002`, `SCORE-006`).

    A normalização é feita no gerador porque a soma unitária é pré-condição do cálculo, não coisa
    a descobrir por contraexemplo. O último peso absorve o resto do arredondamento, de modo que a
    soma é exata em `Decimal` e não aproximada.
    """
    return st.builds(
        _pesos_normalizados,
        nomes=st.just(nomes),
        brutos=st.lists(
            st.integers(min_value=1, max_value=40),
            min_size=len(nomes),
            max_size=len(nomes),
        ).map(tuple),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class EstadoDePortfolio:
    """Estado da carteira para capital e concentração (`R47`, `R48`, `INV-*`, `PORT-001`)."""

    capital_disponivel: Decimal
    reserva_minima: Decimal
    patrimonio_liquido: Decimal
    concentracao_por_regiao: Decimal
    concentracao_por_tipo: Decimal
    estrategias_ativas: tuple[Estrategia, ...]
    quantidade_de_ativos: int


def estado_de_portfolio() -> st.SearchStrategy[EstadoDePortfolio]:
    """Estado de portfólio com os defaults de `INV-001`, `INV-005` e `INV-019` nas fronteiras.

    A reserva mínima aplicável é o **maior** valor entre `INV-005` absoluto e
    `INV-019 × patrimônio líquido`; gerar os dois separadamente é o que permite verificar que o
    maior prevalece.
    """
    return st.builds(
        EstadoDePortfolio,
        capital_disponivel=st.sampled_from(
            (Decimal(0), Decimal(50_000), Decimal(250_000), Decimal(300_000))
        ),
        reserva_minima=st.sampled_from((Decimal(0), Decimal(50_000))),
        patrimonio_liquido=st.sampled_from(
            (Decimal(0), Decimal(500_000), Decimal(1_000_000))
        ),
        concentracao_por_regiao=st.sampled_from(
            (Decimal("0.00"), Decimal("0.40"), Decimal("0.41"), Decimal("1.00"))
        ),
        concentracao_por_tipo=st.sampled_from(
            (Decimal("0.00"), Decimal("0.15"), Decimal("0.25"), Decimal("1.00"))
        ),
        estrategias_ativas=st.lists(
            st.sampled_from(Estrategia),
            min_size=0,
            max_size=6,
            unique=True,
        ).map(tuple),
        quantidade_de_ativos=st.integers(min_value=0, max_value=20),
    )
