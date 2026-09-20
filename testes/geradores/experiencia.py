"""Geradores de experiência do investidor — `P22` (`R122` a `R125`).

`declaracao_de_tela()` gera a declaração dos **nove** estados de tela, e gera também a declaração
**incompleta**: `MT-16` e `P22.1` existem para recusar a tela que dependa de dado remoto e não
declare os nove. Um gerador que sempre produzisse a declaração completa tornaria as duas
verificações vazias.

`largura_de_viewport()` inclui as larguras estreitas de propósito — responsividade em tela estreita
é requisito, não cortesia.

Camada de infraestrutura de teste: nenhuma entrada e saída de dados.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from hypothesis import strategies as st

from radar.nucleo.enumeracoes_de_infraestrutura import EstadoDeTela, NaturezaDaInformacao

__all__ = [
    "DESTINOS_DE_NAVEGACAO",
    "LARGURAS_DE_FRONTEIRA",
    "ArvoreDeComponentes",
    "ClasseDeResposta",
    "DeclaracaoDeTela",
    "FormularioDeclarado",
    "arvore_de_componentes",
    "classe_de_resposta",
    "declaracao_de_tela",
    "formulario_declarado",
    "largura_de_viewport",
]

DESTINOS_DE_NAVEGACAO: Final[tuple[str, ...]] = (
    "painel",
    "nova_analise",
    "ficha_da_oportunidade",
    "documentos",
    "evidencias",
    "pendencias",
    "comparacao_de_versoes",
    "parametros",
    "visao_financeira",
)
"""Os nove destinos de navegação da interface do investidor (`R122`, `R94`)."""

LARGURAS_DE_FRONTEIRA: Final[tuple[int, ...]] = (320, 360, 768, 1024, 1280, 1920)
"""Larguras de viewport de fronteira. 320 é a tela estreita que a responsividade tem de atender."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeclaracaoDeTela:
    """Declaração dos estados de uma tela que depende de dado remoto (`R122.1`).

    `estados_declarados` pode ser incompleto de propósito: é o caso que `MT-16` recusa. `completa`
    diz se os nove estão presentes, para que a propriedade não precise recontar.
    """

    destino: str
    depende_de_dado_remoto: bool
    estados_declarados: frozenset[EstadoDeTela]

    @property
    def completa(self) -> bool:
        """Verdadeiro quando os nove estados de tela estão declarados."""
        return self.estados_declarados == frozenset(EstadoDeTela)


def declaracao_de_tela() -> st.SearchStrategy[DeclaracaoDeTela]:
    """Declaração de tela, completa em parte do espaço e incompleta no resto."""
    completa = st.just(frozenset(EstadoDeTela))
    incompleta = st.sets(st.sampled_from(EstadoDeTela), min_size=0, max_size=8).map(frozenset)
    return st.builds(
        DeclaracaoDeTela,
        destino=st.sampled_from(DESTINOS_DE_NAVEGACAO),
        depende_de_dado_remoto=st.booleans(),
        estados_declarados=st.one_of(completa, incompleta),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class ClasseDeResposta:
    """Classe de resposta apresentada ao investidor, com a natureza da informação (`R123.4`).

    Nenhum item acumula mais de uma natureza (`P22.5`): a natureza é um enum, não um conjunto, e
    `PENDENTE` é a quarta natureza apresentável — não a ausência de natureza.
    """

    natureza: NaturezaDaInformacao
    estado_de_tela: EstadoDeTela
    tem_citacao: bool


def classe_de_resposta() -> st.SearchStrategy[ClasseDeResposta]:
    """Classe de resposta em todas as combinações de natureza e estado de tela."""
    return st.builds(
        ClasseDeResposta,
        natureza=st.sampled_from(NaturezaDaInformacao),
        estado_de_tela=st.sampled_from(EstadoDeTela),
        tem_citacao=st.booleans(),
    )


def largura_de_viewport() -> st.SearchStrategy[int]:
    """Largura de viewport em pixels, com as larguras de fronteira sempre presentes."""
    return st.one_of(
        st.sampled_from(LARGURAS_DE_FRONTEIRA),
        st.integers(min_value=280, max_value=2560),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class ArvoreDeComponentes:
    """Árvore de componentes de uma tela, achatada em pares pai × filho.

    O nó raiz aparece como filho de `None` representado por cadeia vazia; a árvore pode ser vazia,
    que é o caso da tela sem componente remoto.
    """

    componentes: tuple[str, ...]
    arestas: tuple[tuple[str, str], ...]
    componentes_com_dado_remoto: frozenset[str]


def arvore_de_componentes() -> st.SearchStrategy[ArvoreDeComponentes]:
    """Árvore de componentes com subconjunto declarado de componentes que buscam dado remoto."""
    nomes = ("raiz", "cabecalho", "lista", "item", "rodape", "formulario")
    return st.builds(
        _arvore_coerente,
        quantidade=st.integers(min_value=1, max_value=len(nomes)),
        nomes=st.just(nomes),
        com_dado_remoto=st.sets(st.sampled_from(nomes), min_size=0, max_size=len(nomes)).map(
            frozenset
        ),
    )


def _arvore_coerente(
    *,
    quantidade: int,
    nomes: tuple[str, ...],
    com_dado_remoto: frozenset[str],
) -> ArvoreDeComponentes:
    componentes = nomes[:quantidade]
    arestas = tuple(
        (componentes[indice - 1], componentes[indice]) for indice in range(1, len(componentes))
    )
    return ArvoreDeComponentes(
        componentes=componentes,
        arestas=arestas,
        componentes_com_dado_remoto=frozenset(com_dado_remoto & set(componentes)),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class FormularioDeclarado:
    """Formulário com rótulo, obrigatoriedade e mensagem de erro por campo (`R125`).

    `rotulo_associado` e `mensagem_de_erro_declarada` são separados porque acessibilidade exige os
    dois: campo obrigatório sem rótulo associado e erro sem mensagem legível são defeitos distintos.
    """

    campos: tuple[str, ...]
    obrigatorios: frozenset[str]
    rotulo_associado: frozenset[str]
    mensagem_de_erro_declarada: frozenset[str]


def formulario_declarado() -> st.SearchStrategy[FormularioDeclarado]:
    """Formulário declarado, com campos sem rótulo e sem mensagem entre os casos gerados."""
    campos = (
        "preco_lance",
        "valor_de_mercado",
        "matricula",
        "estrategia",
        "observacoes",
    )
    subconjunto = st.sets(st.sampled_from(campos), min_size=0, max_size=len(campos)).map(frozenset)
    return st.builds(
        FormularioDeclarado,
        campos=st.just(campos),
        obrigatorios=subconjunto,
        rotulo_associado=subconjunto,
        mensagem_de_erro_declarada=subconjunto,
    )
