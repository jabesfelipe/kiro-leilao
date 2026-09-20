"""Escalas e escalares, com os valores de fronteira obrigatórios injetados deliberadamente.

Este módulo é a base de todos os outros: quem precisa de dinheiro, área, percentual, data e hora
ou de um `Informado[T]` vem buscar aqui, e ao fazê-lo herda **os valores de fronteira
obrigatórios** do design sem ter de repeti-los.

Os valores de fronteira não são amostra: entram por `sampled_from` dentro de `one_of`, de modo
que toda execução de 100 iterações os visita. Também ficam publicados como constantes, para quem
preferir fixá-los com `@example` no próprio teste.

| Grupo de fronteira | Constante | Defeito que caça |
|--------------------|-----------|------------------|
| 89,5 · 79,5 · 74,5 · 69,5 · 59,5 · 49,5 · 39,5 | `VALORES_FRACIONARIOS_DE_FRONTEIRA` | `D.1.5` |
| `"47.76"` · `"191651.31"` | `CADEIAS_DECIMAIS_DE_FRONTEIRA` | `D.1.3` |
| `"2,5%"` · `"2.5%"` | `CADEIAS_DE_PERCENTUAL_DE_FRONTEIRA` | `D.1.4` |
| 1 com unidade `PORCENTO` | `UM_COM_UNIDADE_PORCENTO` | `D.1.4` |
| limiar exato de `MON-001` a `MON-017` | `LIMIARES_NUMERICOS_DE_MATERIALIDADE` | `P13.1` |
| limiar qualitativo de `MON-*` | `LIMIARES_QUALITATIVOS_DE_MATERIALIDADE` | `P13.1` |
| limiar exato de `STR` | `LIMIARES_DE_ESTRATEGIA` | decisão no limiar exato |
| limiar exato de decisão | `LIMIARES_DE_DECISAO` | decisão no limiar exato |

Camada de infraestrutura de teste: nenhuma entrada e saída de dados, nenhuma rede, nenhum banco.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from types import MappingProxyType
from typing import Final

from hypothesis import strategies as st

from radar.nucleo.enumeracoes import (
    EstadoDaInformacao,
    Estrategia,
    QualidadeDaEvidencia,
    TipoDeArea,
    UnidadeDePercentual,
)
from radar.nucleo.informado import DESCONHECIDO, Informado

__all__ = [
    "CADEIAS_DECIMAIS_DE_FRONTEIRA",
    "CADEIAS_DE_PERCENTUAL_DE_FRONTEIRA",
    "FONTES_SINTETICAS",
    "FUSO_DE_BRASILIA",
    "IDENTIFICADORES_DE_MATERIALIDADE",
    "LIMIARES_DE_DECISAO",
    "LIMIARES_DE_ESTRATEGIA",
    "LIMIARES_NUMERICOS_DE_MATERIALIDADE",
    "LIMIARES_QUALITATIVOS_DE_MATERIALIDADE",
    "UM_COM_UNIDADE_PORCENTO",
    "VALORES_DE_FRONTEIRA_DA_ESCALA",
    "VALORES_FRACIONARIOS_DE_FRONTEIRA",
    "AreaDeclarada",
    "LimiaresDeEstrategia",
    "PercentualDeclarado",
    "area",
    "data_hora_br",
    "dinheiro",
    "escala_de_zero_a_cem",
    "fonte_declarada",
    "informado",
    "percentual",
    "texto_de_dinheiro",
    "texto_de_percentual",
]

# Fuso de Brasília como deslocamento fixo de −3 h. O Brasil não observa horário de verão desde
# 2019, e o deslocamento fixo evita depender da base de fusos do sistema operacional — o que
# tornaria a suíte dependente de ambiente sem ganho algum de fidelidade de domínio.
FUSO_DE_BRASILIA: Final[timezone] = timezone(timedelta(hours=-3))


# --------------------------------------------------------------------------------------
# Valores de fronteira obrigatórios (design, seção *Valores de fronteira obrigatórios*)
# --------------------------------------------------------------------------------------

VALORES_FRACIONARIOS_DE_FRONTEIRA: Final[tuple[Decimal, ...]] = (
    Decimal("89.5"),  # fronteira 89/90: Excelente e fator 0,95 (`REG-021`)
    Decimal("79.5"),  # fronteira 79/80
    Decimal("74.5"),  # fronteira 74/75, a que decide `GLB-003`
    Decimal("69.5"),  # fronteira 69/70
    Decimal("59.5"),  # fronteira 59/60
    Decimal("49.5"),  # fronteira 49/50, limiar de exceção formal de `R40.8`
    Decimal("39.5"),  # fronteira 39/40
)
"""Os sete fracionários que `D.1.5` deixava sem faixa. Nenhum deles é inteiro por acidente."""

CADEIAS_DECIMAIS_DE_FRONTEIRA: Final[tuple[str, ...]] = ("47.76", "191651.31")
"""Ponto decimal com duas casas: `"47.76"` é 47,76 e nunca 4.776 (`REG-019`, `D.1.3`)."""

CADEIAS_DE_PERCENTUAL_DE_FRONTEIRA: Final[tuple[str, ...]] = ("2,5%", "2.5%")
"""Alíquota fracionária nas duas grafias; ambas resultam em 0,025 (`REG-020`, `D.1.4`)."""

UM_COM_UNIDADE_PORCENTO: Final[tuple[Decimal, UnidadeDePercentual]] = (
    Decimal(1),
    UnidadeDePercentual.PORCENTO,
)
"""Um por cento: resulta em 0,01, não em 1,00. A unidade é obrigatória na entrada (`R3.4.2`)."""

IDENTIFICADORES_DE_MATERIALIDADE: Final[tuple[str, ...]] = tuple(
    f"MON-{numero:03d}" for numero in range(1, 18)
)
"""Os dezessete gatilhos de materialidade, `MON-001` a `MON-017`. A contagem é contrato."""

LIMIARES_NUMERICOS_DE_MATERIALIDADE: Final[Mapping[str, Decimal]] = MappingProxyType(
    {
        "MON-001": Decimal("0.05"),  # mudança de preço
        "MON-005": Decimal("0.05"),  # mudança de aluguel
        "MON-009": Decimal("0.10"),  # mudança de capital disponível
        "MON-010": Decimal(10),  # mudança de liquidez, em pontos da escala 0–100
        "MON-012": Decimal("0.20"),  # oferta concorrente aumenta
        "MON-013": Decimal("0.05"),  # preços de venda da região caem
        "MON-014": Decimal("0.05"),  # aluguéis da região sobem
    }
)
"""Limiar **exato** de cada gatilho numérico. A comparação é `>=`: no limiar, dispara (`P13.1`)."""

LIMIARES_QUALITATIVOS_DE_MATERIALIDADE: Final[Mapping[str, str]] = MappingProxyType(
    {
        "MON-002": "qualquer",
        "MON-003": "qualidade ≥ C e dentro do raio/janela",
        "MON-004": "qualquer",
        "MON-006": "qualquer",
        "MON-007": "qualquer",
        "MON-008": "prazo FRESH excedido",
        "MON-011": "qualquer",
        "MON-015": "qualquer mudança material de taxa, prazo ou elegibilidade",
        "MON-016": "qualquer",
        "MON-017": "PRI-007 satisfeito e sem BLOCK",
    }
)
"""Gatilhos cujo limiar declarado **não** é número. `qualquer` dispara em toda mudança."""


@dataclass(frozen=True, slots=True, kw_only=True)
class LimiaresDeEstrategia:
    """Uma linha da tabela `STR` — thresholds por estratégia `[CANÔNICO]`.

    `None` significa a célula `—` da tabela: a estratégia **não declara** o limiar. É distinto
    de limiar zero, e tratá-los como iguais seria converter ausência em exigência nula.
    """

    desconto_liquido_minimo: Decimal
    margem_minima: Decimal
    yield_liquido_mensal_minimo: Decimal | None
    liquidez_minima: Decimal
    prazo_de_saida_maximo_em_dias: int | None
    ticket_maximo: Decimal


LIMIARES_DE_ESTRATEGIA: Final[Mapping[Estrategia, LimiaresDeEstrategia]] = MappingProxyType(
    {
        Estrategia.REVENDA: LimiaresDeEstrategia(
            desconto_liquido_minimo=Decimal("0.25"),
            margem_minima=Decimal("0.20"),
            yield_liquido_mensal_minimo=None,
            liquidez_minima=Decimal(75),
            prazo_de_saida_maximo_em_dias=180,
            ticket_maximo=Decimal(400_000),
        ),
        Estrategia.RENDA: LimiaresDeEstrategia(
            desconto_liquido_minimo=Decimal("0.15"),
            margem_minima=Decimal("0.15"),
            yield_liquido_mensal_minimo=Decimal("0.0080"),
            liquidez_minima=Decimal(70),
            prazo_de_saida_maximo_em_dias=None,
            ticket_maximo=Decimal(300_000),
        ),
        Estrategia.VALORIZACAO: LimiaresDeEstrategia(
            desconto_liquido_minimo=Decimal("0.15"),
            margem_minima=Decimal("0.15"),
            yield_liquido_mensal_minimo=None,
            liquidez_minima=Decimal(60),
            prazo_de_saida_maximo_em_dias=None,
            ticket_maximo=Decimal(250_000),  # `INV-002`
        ),
        Estrategia.MCMV: LimiaresDeEstrategia(
            desconto_liquido_minimo=Decimal("0.20"),
            margem_minima=Decimal("0.15"),
            yield_liquido_mensal_minimo=Decimal("0.0080"),
            liquidez_minima=Decimal(70),
            prazo_de_saida_maximo_em_dias=180,
            ticket_maximo=Decimal(250_000),  # `INV-002`
        ),
        Estrategia.TERRENO: LimiaresDeEstrategia(
            desconto_liquido_minimo=Decimal("0.20"),
            margem_minima=Decimal("0.20"),
            yield_liquido_mensal_minimo=None,
            liquidez_minima=Decimal(50),
            prazo_de_saida_maximo_em_dias=365,
            ticket_maximo=Decimal(250_000),  # `INV-002`
        ),
    }
)
"""Limiar **exato** de `STR` por estratégia. `CUSTOMIZADA` é ausente porque a tabela a declara
inteiramente `configurável`: ela não tem valor de fábrica a injetar."""

LIMIARES_DE_DECISAO: Final[Mapping[str, Decimal]] = MappingProxyType(
    {
        "GLB-003": Decimal(75),  # confiança mínima para COMPRAR
        "GLB-004": Decimal(60),  # score mínimo global
        "GLB-006": Decimal(70),  # liquidez mínima global
        "LIQ-011": Decimal("0.30"),  # margem mínima com liquidez baixa
        "VAL-009": Decimal(70),  # confiança mínima de valuation
        "SCORE-004:revenda": Decimal(75),
        "SCORE-004:renda": Decimal(70),
        "SCORE-004:mcmv": Decimal(65),
        "SCORE-004:valorizacao": Decimal(65),
        "SCORE-004:terreno": Decimal(65),
        "SCORE-007": Decimal(60),  # mínimo de aderência do investidor (Investor Fit)
        "PRI-007": Decimal("0.30"),  # desconto excepcional, gatilho de `MON-017`
    }
)
"""Limiares de decisão em que a satisfação é `>=`: no limiar exato, **satisfaz**.

`GLB-011` não aparece porque seu default é derivado (`Selic + 15 p.p.`) e não tem valor exato de
fábrica: fixar um número aqui seria inventar parâmetro.
"""

_INTEIROS_DE_FRONTEIRA_DA_ESCALA: Final[tuple[int, ...]] = (
    0, 39, 40, 49, 50, 59, 60, 69, 70, 74, 75, 79, 80, 89, 90, 100,
)

VALORES_DE_FRONTEIRA_DA_ESCALA: Final[tuple[Decimal, ...]] = (
    *VALORES_FRACIONARIOS_DE_FRONTEIRA,
    *(Decimal(inteiro) for inteiro in _INTEIROS_DE_FRONTEIRA_DA_ESCALA),
    LIMIARES_NUMERICOS_DE_MATERIALIDADE["MON-010"],
    *(limiares.liquidez_minima for limiares in LIMIARES_DE_ESTRATEGIA.values()),
    *(
        LIMIARES_DE_DECISAO[identificador]
        for identificador in (
            "GLB-003",
            "GLB-004",
            "GLB-006",
            "VAL-009",
            "SCORE-004:revenda",
            "SCORE-004:renda",
            "SCORE-004:mcmv",
            "SCORE-004:valorizacao",
            "SCORE-004:terreno",
            "SCORE-007",
        )
    ),
)
"""Tudo que vive na escala `[0, 100]` e tem de ser visitado: fracionários de `D.1.5`, inteiros de
cada fronteira de faixa, `MON-010`, a liquidez mínima de cada estratégia e os limiares de
decisão medidos em pontos."""

VALORES_DE_FRONTEIRA_FRACIONARIOS_DE_PERCENTUAL: Final[tuple[Decimal, ...]] = (
    # `MON-010` fica de fora: seus 10 são **pontos** da escala 0–100, não fração. Ele entra em
    # `VALORES_DE_FRONTEIRA_DA_ESCALA`, que é onde o limiar de liquidez é comparado.
    *(
        limiar
        for identificador, limiar in LIMIARES_NUMERICOS_DE_MATERIALIDADE.items()
        if identificador != "MON-010"
    ),
    *(limiares.desconto_liquido_minimo for limiares in LIMIARES_DE_ESTRATEGIA.values()),
    *(limiares.margem_minima for limiares in LIMIARES_DE_ESTRATEGIA.values()),
    *(
        limiares.yield_liquido_mensal_minimo
        for limiares in LIMIARES_DE_ESTRATEGIA.values()
        if limiares.yield_liquido_mensal_minimo is not None
    ),
    LIMIARES_DE_DECISAO["LIQ-011"],
    LIMIARES_DE_DECISAO["PRI-007"],
)
"""Limiares expressos como fração e injetados em `percentual()` com unidade `FRACAO`."""

FONTES_SINTETICAS: Final[tuple[str, ...]] = (
    "edital",
    "matricula",
    "iptu",
    "cartorio",
    "anuncio-de-mercado",
    "informado-pelo-usuario",
)
"""Fontes sintéticas. Nenhuma string em branco: ausência de fonte se declara com `Desconhecido`."""


# --------------------------------------------------------------------------------------
# Geradores
# --------------------------------------------------------------------------------------


def fonte_declarada() -> st.SearchStrategy[str]:
    """Nome de fonte não vazio — `Informado` rejeita fonte em branco por construção."""
    return st.sampled_from(FONTES_SINTETICAS)


def escala_de_zero_a_cem() -> st.SearchStrategy[Decimal]:
    """Escala `[0, 100]` de escore, confiança, liquidez e aderência (`R40.1`, `R49.1`, `R50.1`).

    Amostragem contínua **mais** os valores de fronteira obrigatórios. É este gerador que leva
    89,5 e os seis irmãos a toda propriedade de faixa, e é por isso que `D.1.5` não volta.
    """
    return st.one_of(
        st.sampled_from(VALORES_DE_FRONTEIRA_DA_ESCALA),
        st.decimals(
            min_value=Decimal(0),
            max_value=Decimal(100),
            places=2,
            allow_nan=False,
            allow_infinity=False,
        ),
    )


def dinheiro() -> st.SearchStrategy[Decimal]:
    """Valor monetário em `Decimal` com duas casas. `float` não atravessa o núcleo.

    Injeta 47,76 e 191.651,31 como números, que são os mesmos valores das cadeias de `D.1.3`:
    a propriedade que interpreta a cadeia e a que calcula sobre o número veem a mesma fronteira.
    """
    return st.one_of(
        st.sampled_from(tuple(Decimal(cadeia) for cadeia in CADEIAS_DECIMAIS_DE_FRONTEIRA)),
        st.decimals(
            min_value=Decimal("0.01"),
            max_value=Decimal("5000000.00"),
            places=2,
            allow_nan=False,
            allow_infinity=False,
        ),
    )


def texto_de_dinheiro() -> st.SearchStrategy[str]:
    """Cadeia monetária como ela chega da fonte, para a interpretação de `R3.4.1`.

    Inclui `"47.76"` e `"191651.31"` — ponto decimal com duas casas, que `D.1.3` lia como
    separador de milhar — ao lado das grafias `pt_br` e simples que precisam conviver.
    """
    return st.one_of(
        st.sampled_from(CADEIAS_DECIMAIS_DE_FRONTEIRA),
        st.sampled_from(("1.234,56", "1234,56", "1,234.56", "1234.56", "191.651,31", "47,76")),
    )


def texto_de_percentual() -> st.SearchStrategy[str]:
    """Cadeia de percentual, com `"2,5%"` e `"2.5%"` sempre presentes (`REG-020`, `D.1.4`)."""
    return st.one_of(
        st.sampled_from(CADEIAS_DE_PERCENTUAL_DE_FRONTEIRA),
        st.sampled_from(("1%", "0,025", "0.025", "15%", "2,50%", "100%")),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class PercentualDeclarado:
    """Percentual com a unidade declarada: sem unidade, alíquota fracionária é lida errado."""

    valor: Decimal
    unidade: UnidadeDePercentual


def percentual() -> st.SearchStrategy[PercentualDeclarado]:
    """Percentual com unidade obrigatória (`R3.4.2`, `R3.4.3`).

    Injeta `1` com unidade `PORCENTO` — que vale 0,01 e não 1,00 —, `2,5` com `PORCENTO` e todo
    limiar fracionário de `MON-*`, de `STR`, de `LIQ-011` e de `PRI-007` com unidade `FRACAO`.
    """
    fronteiras = (
        PercentualDeclarado(valor=UM_COM_UNIDADE_PORCENTO[0], unidade=UM_COM_UNIDADE_PORCENTO[1]),
        PercentualDeclarado(valor=Decimal("2.5"), unidade=UnidadeDePercentual.PORCENTO),
        *(
            PercentualDeclarado(valor=limiar, unidade=UnidadeDePercentual.FRACAO)
            for limiar in VALORES_DE_FRONTEIRA_FRACIONARIOS_DE_PERCENTUAL
        ),
    )
    amostrado = st.builds(
        PercentualDeclarado,
        valor=st.decimals(
            min_value=Decimal(0),
            max_value=Decimal(1),
            places=4,
            allow_nan=False,
            allow_infinity=False,
        ),
        unidade=st.just(UnidadeDePercentual.FRACAO),
    )
    return st.one_of(st.sampled_from(fronteiras), amostrado)


@dataclass(frozen=True, slots=True, kw_only=True)
class AreaDeclarada:
    """Área com o tipo declarado (`R3.5`, `R21.11`).

    Área de tipo desconhecido **não** é área privativa por omissão: `TipoDeArea.DESCONHECIDO` é
    um valor gerado de propósito, para que as propriedades vejam o caso.
    """

    valor: Decimal
    tipo: TipoDeArea


def area() -> st.SearchStrategy[AreaDeclarada]:
    """Área em metros quadrados, sempre com tipo declarado."""
    return st.builds(
        AreaDeclarada,
        valor=st.decimals(
            min_value=Decimal("1.00"),
            max_value=Decimal("100000.00"),
            places=2,
            allow_nan=False,
            allow_infinity=False,
        ),
        tipo=st.sampled_from(TipoDeArea),
    )


# Limites naive exigidos por `st.datetimes`, que recebe fronteiras sem fuso e aplica o fuso pela
# estratégia de `timezones`. O resultado gerado é sempre consciente de fuso.
_INICIO_DA_JANELA: Final[datetime] = datetime(2020, 1, 1, 0, 0, 0)  # noqa: DTZ001
_FIM_DA_JANELA: Final[datetime] = datetime(2030, 12, 31, 23, 59, 59)  # noqa: DTZ001


def data_hora_br() -> st.SearchStrategy[datetime]:
    """Data e hora consciente de fuso, no fuso de Brasília. Data sem fuso é defeito de domínio."""
    return st.datetimes(
        min_value=_INICIO_DA_JANELA,
        max_value=_FIM_DA_JANELA,
        timezones=st.just(FUSO_DE_BRASILIA),
    )


_ESTADOS_COM_VALOR: Final[tuple[EstadoDaInformacao, ...]] = tuple(
    estado for estado in EstadoDaInformacao if estado is not EstadoDaInformacao.DESCONHECIDO
)

_QUALIDADES_COM_VALOR: Final[tuple[QualidadeDaEvidencia, ...]] = tuple(
    qualidade
    for qualidade in QualidadeDaEvidencia
    if qualidade is not QualidadeDaEvidencia.AUSENTE
)


def _com_valor[T](
    *,
    valor: T,
    estado_da_informacao: EstadoDaInformacao,
    fonte: str,
    data_de_observacao: datetime,
    confianca: Decimal,
    qualidade_da_evidencia: QualidadeDaEvidencia,
) -> Informado[T]:
    return Informado(
        valor=valor,
        estado_da_informacao=estado_da_informacao,
        fonte=fonte,
        data_de_observacao=data_de_observacao,
        confianca=confianca,
        qualidade_da_evidencia=qualidade_da_evidencia,
    )


def _sem_valor[T](*, fonte: str, data_de_observacao: datetime) -> Informado[T]:
    return Informado(
        valor=DESCONHECIDO,
        estado_da_informacao=EstadoDaInformacao.DESCONHECIDO,
        fonte=fonte,
        data_de_observacao=data_de_observacao,
        confianca=DESCONHECIDO,
        qualidade_da_evidencia=QualidadeDaEvidencia.AUSENTE,
    )


def informado[T](
    valores: st.SearchStrategy[T],
    *,
    permitir_desconhecido: bool = True,
) -> st.SearchStrategy[Informado[T]]:
    """`Informado[T]` válido, com ou sem valor — a ausência é gerada, não evitada.

    Gerar `DESCONHECIDO` é o ponto do gerador: é ele que expõe as propriedades que confundem
    ausência com zero (`SAFE-003`, `SAFE-005`). Quem precisa de valor presente por pré-condição
    pede `permitir_desconhecido=False`, e a exclusão fica declarada na chamada.
    """
    conhecido: st.SearchStrategy[Informado[T]] = st.builds(
        _com_valor,
        valor=valores,
        estado_da_informacao=st.sampled_from(_ESTADOS_COM_VALOR),
        fonte=fonte_declarada(),
        data_de_observacao=data_hora_br(),
        confianca=escala_de_zero_a_cem(),
        qualidade_da_evidencia=st.sampled_from(_QUALIDADES_COM_VALOR),
    )
    if not permitir_desconhecido:
        return conhecido
    ausente: st.SearchStrategy[Informado[T]] = st.builds(
        _sem_valor,
        fonte=fonte_declarada(),
        data_de_observacao=data_hora_br(),
    )
    return st.one_of(conhecido, ausente)
