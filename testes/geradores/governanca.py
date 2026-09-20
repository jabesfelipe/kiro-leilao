"""Geradores de governança: parâmetros, exceções e base de conhecimento (`R61`, `R62`, `R72`).

A hierarquia de parâmetros é gerada com os **sete** escopos de resolução e com vigência temporal,
porque é aí que vivem os dois defeitos que a arquitetura anterior tinha: parâmetro sem vigência
que resolvia de todo modo (`R62.11`) e escopo mais específico contornando bloqueio crítico.

`registro_de_excecao()` gera a exceção autorizada — e gera também a tentativa de exceção **sobre
bloqueio**, que tem de ser recusada. Exceção que contorna bloqueio jurídico ou risco crítico não é
exceção, é defeito.

Camada de infraestrutura de teste: nenhuma entrada e saída de dados.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Final

from hypothesis import strategies as st

from radar.nucleo.enumeracoes import (
    SituacaoDeGovernanca,
    TipoDeSegmentoDeConhecimento,
)
from radar.nucleo.informado import DESCONHECIDO, Desconhecido
from testes.geradores.escalas import data_hora_br, escala_de_zero_a_cem

__all__ = [
    "ESCOPOS_DE_RESOLUCAO",
    "IDENTIFICADORES_DE_PARAMETRO",
    "HierarquiaDeParametros",
    "NivelDeEscopo",
    "RegistroDeExcecao",
    "SegmentoDeConhecimento",
    "ValorDeParametro",
    "hierarquia_de_parametros",
    "registro_de_excecao",
    "segmento_de_conhecimento",
]

ESCOPOS_DE_RESOLUCAO: Final[tuple[str, ...]] = (
    "global",
    "perfil_do_investidor",
    "estrategia",
    "localizacao",
    "tipo_de_imovel",
    "oportunidade",
    "excecao_autorizada",
)
"""A hierarquia de escopo `[CANÔNICO]`, do menos para o mais específico.

O mais específico prevalece, **exceto** quando o menos específico impõe bloqueio crítico ou
restrição legal ou documental. Gerar os sete em ordem é o que permite verificar a exceção.
"""

IDENTIFICADORES_DE_PARAMETRO: Final[tuple[str, ...]] = (
    "GLB-003",
    "GLB-004",
    "GLB-006",
    "LIQ-011",
    "VAL-009",
    "PRI-007",
    "SCORE-004",
    "SCORE-007",
    "MON-001",
    "MON-010",
    "MON-017",
)
"""Parâmetros do catálogo normativo cujos limiares as propriedades de decisão consultam."""

NivelDeEscopo = str
"""Um dos sete escopos de `ESCOPOS_DE_RESOLUCAO`."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ValorDeParametro:
    """Valor de parâmetro em um escopo, com vigência declarada (`R62.10`, `R62.11`).

    `vigente_de` pode ser `Desconhecido`: é o parâmetro sem vigência, que **não** resolve. Gerar
    esse caso é o ponto — a alternativa seria descobrir em produção que ele resolvia.
    """

    identificador: str
    escopo: NivelDeEscopo
    valor: Decimal
    versao: str
    vigente_de: datetime | Desconhecido
    situacao: SituacaoDeGovernanca


@dataclass(frozen=True, slots=True, kw_only=True)
class HierarquiaDeParametros:
    """Os valores declarados de um mesmo parâmetro nos escopos em que ele aparece."""

    identificador: str
    valores_por_escopo: tuple[ValorDeParametro, ...]
    bloqueio_critico_no_escopo_global: bool


def hierarquia_de_parametros() -> st.SearchStrategy[HierarquiaDeParametros]:
    """Hierarquia de um parâmetro, com de um a sete escopos declarados e vigência opcional."""
    return st.builds(
        _hierarquia_coerente,
        identificador=st.sampled_from(IDENTIFICADORES_DE_PARAMETRO),
        escopos=st.lists(
            st.sampled_from(ESCOPOS_DE_RESOLUCAO),
            min_size=1,
            max_size=len(ESCOPOS_DE_RESOLUCAO),
            unique=True,
        ).map(tuple),
        valores=st.lists(escala_de_zero_a_cem(), min_size=7, max_size=7).map(tuple),
        vigencias=st.lists(
            st.one_of(st.just(DESCONHECIDO), data_hora_br()),
            min_size=7,
            max_size=7,
        ).map(tuple),
        situacao=st.sampled_from(SituacaoDeGovernanca),
        bloqueio_critico_no_escopo_global=st.booleans(),
    )


def _hierarquia_coerente(
    *,
    identificador: str,
    escopos: tuple[str, ...],
    valores: tuple[Decimal, ...],
    vigencias: tuple[datetime | Desconhecido, ...],
    situacao: SituacaoDeGovernanca,
    bloqueio_critico_no_escopo_global: bool,
) -> HierarquiaDeParametros:
    declarados = tuple(
        ValorDeParametro(
            identificador=identificador,
            escopo=escopo,
            valor=valores[indice],
            versao=f"1.{indice}.0",
            vigente_de=vigencias[indice],
            situacao=situacao,
        )
        for indice, escopo in enumerate(escopos)
    )
    return HierarquiaDeParametros(
        identificador=identificador,
        valores_por_escopo=declarados,
        bloqueio_critico_no_escopo_global=bloqueio_critico_no_escopo_global,
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class RegistroDeExcecao:
    """Exceção autorizada, com autor, motivo, validade e alvo (`R63`, `EXC-*`).

    `alvo_e_bloqueio_juridico` e `alvo_e_risco_critico` existem para gerar a tentativa proibida:
    exceção **não** contorna bloqueio jurídico nem risco crítico, e a recusa tem de ser verificada
    e não presumida.
    """

    identificador: str
    parametro_alvo: str
    autor: str
    motivo: str
    autorizada_em: datetime
    valida_ate: datetime | Desconhecido
    alvo_e_bloqueio_juridico: bool
    alvo_e_risco_critico: bool


def registro_de_excecao() -> st.SearchStrategy[RegistroDeExcecao]:
    """Exceção autorizada, incluindo as que tentam alcançar bloqueio e risco crítico."""
    return st.builds(
        RegistroDeExcecao,
        identificador=st.from_regex(r"\AEXC-[0-9]{3}\Z", fullmatch=True),
        parametro_alvo=st.sampled_from(IDENTIFICADORES_DE_PARAMETRO),
        autor=st.text(min_size=1, max_size=30),
        motivo=st.text(min_size=1, max_size=60),
        autorizada_em=data_hora_br(),
        valida_ate=st.one_of(st.just(DESCONHECIDO), data_hora_br()),
        alvo_e_bloqueio_juridico=st.booleans(),
        alvo_e_risco_critico=st.booleans(),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class SegmentoDeConhecimento:
    """Segmento da Base de Conhecimento, com tipo e versão (`R72.2`)."""

    identificador: str
    tipo: TipoDeSegmentoDeConhecimento
    texto: str
    versao: str
    situacao: SituacaoDeGovernanca
    e_hipotese: bool


def segmento_de_conhecimento() -> st.SearchStrategy[SegmentoDeConhecimento]:
    """Segmento de conhecimento nos quinze tipos, com a marca de hipótese.

    `e_hipotese` é obrigatório porque item recuperado da memória histórica é hipótese, nunca
    evidência atual (`R72.9`, `SAFE-011`): o histórico não se converte em fato atual.
    """
    return st.builds(
        SegmentoDeConhecimento,
        identificador=st.text(min_size=1, max_size=20),
        tipo=st.sampled_from(TipoDeSegmentoDeConhecimento),
        texto=st.text(min_size=1, max_size=200),
        versao=st.sampled_from(("1.0.0", "1.1.0", "2.0.0")),
        situacao=st.sampled_from(SituacaoDeGovernanca),
        e_hipotese=st.booleans(),
    )
