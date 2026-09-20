"""Geradores de plataforma — `P21` (`R111` a `R121`).

O gerador central deste módulo é `nome_de_arquivo_hostil()`. Ele sustenta `P21.4`, e sem os casos
hostis **explícitos** não prova nada: travessia relativa, caminho absoluto, separadores mistos,
unicode e nome vazio. Texto aleatório praticamente nunca produziria `../../etc/passwd`, e a
propriedade de upload seguro passaria por sorte.

`segredo_sintetico()` gera segredo que **nunca** pode aparecer em representação, em log ou em
resposta de erro (`D.10.1`). O valor é sintético e reconhecível, de modo que a propriedade possa
procurar por ele na saída em lugar de conferir a ausência de um padrão vago.

`evidencia_em_torno_da_data_de_corte()` gera evidência antes, exatamente na, e depois da data de
corte: a data de corte é por versão de análise (`R120.4`), e o caso do limite exato é o que
distingue "até" de "antes de".

Camada de infraestrutura de teste: nenhuma entrada e saída de dados.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Final
from uuid import UUID

from hypothesis import strategies as st

from radar.nucleo.enumeracoes_de_infraestrutura import (
    CategoriaDeErro,
    SituacaoDeTrabalhoAssincrono,
)
from testes.geradores.escalas import data_hora_br

__all__ = [
    "NOMES_DE_ARQUIVO_HOSTIS",
    "SINALIZADORES_DE_PLATAFORMA",
    "BaseMultiTitular",
    "ColecaoPaginavel",
    "EventoDePlataforma",
    "EvidenciaEmTornoDaDataDeCorte",
    "SegredoSintetico",
    "base_multi_titular",
    "colecao_paginavel",
    "combinacao_de_adaptadores",
    "combinacao_de_sinalizadores",
    "evidencia_em_torno_da_data_de_corte",
    "nome_de_arquivo_hostil",
    "segredo_sintetico",
    "sequencia_de_eventos",
]

NOMES_DE_ARQUIVO_HOSTIS: Final[tuple[str, ...]] = (
    # Travessia relativa
    "../segredo.env",
    "../../etc/passwd",
    "documentos/../../.ssh/id_rsa",
    # Caminho absoluto
    "/etc/passwd",
    "C:\\Windows\\System32\\config\\SAM",
    # Separadores mistos
    "pasta\\subpasta/arquivo.pdf",
    "..\\../matricula.pdf",
    # Unicode
    "matrícula-ação-português.pdf",
    "\u202earquivo.fdp",
    "документ.pdf",
    # Nome vazio e quase vazio
    "",
    " ",
    ".",
    "..",
)
"""Os cinco grupos hostis exigidos pelo design para `P21.4`.

Cada grupo está presente de propósito, e nenhum é fruto de amostragem: travessia relativa, caminho
absoluto, separadores mistos, unicode (inclusive a marca de sobrescrita da direita para a esquerda,
que disfarça extensão) e nome vazio.
"""

SINALIZADORES_DE_PLATAFORMA: Final[tuple[str, ...]] = (
    "radar_automatico",
    "ia_documental",
    "recuperacao_vetorial",
    "multi_titular",
    "agendamento",
)
"""Sinalizadores de funcionalidade. Combinação é gerada, não enumerada à mão."""


def nome_de_arquivo_hostil() -> st.SearchStrategy[str]:
    """Nome de arquivo hostil, com os cinco grupos obrigatórios sempre no espaço de geração.

    Este é o gerador de `P21.4`. A amostragem aleatória de texto entra como complemento, nunca como
    substituto: é o caso nomeado que prova que o upload rejeita, e não o texto improvável.
    """
    return st.one_of(
        st.sampled_from(NOMES_DE_ARQUIVO_HOSTIS),
        st.text(min_size=0, max_size=40),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class SegredoSintetico:
    """Segredo sintético, com o valor que **não** pode aparecer em lugar algum (`D.10.1`).

    `valor` é reconhecível de propósito: a propriedade procura a cadeia exata na representação, no
    log e no corpo do erro. Procurar por um padrão genérico aceitaria redação parcial como sucesso.
    """

    nome: str
    valor: str


def segredo_sintetico() -> st.SearchStrategy[SegredoSintetico]:
    """Segredo sintético com nome de variável de ambiente plausível."""
    return st.builds(
        SegredoSintetico,
        nome=st.sampled_from(
            ("CHAVE_DO_PROVEDOR_DE_IA", "URL_DO_BANCO", "SENHA_DO_BANCO", "TOKEN_DE_ACESSO")
        ),
        valor=st.sampled_from(
            (
                "valor-sintetico-que-nunca-deve-vazar-0001",
                "valor-sintetico-que-nunca-deve-vazar-0002",
            )
        ),
    )


def combinacao_de_sinalizadores() -> st.SearchStrategy[frozenset[str]]:
    """Subconjunto dos sinalizadores de funcionalidade, incluindo o conjunto vazio.

    O conjunto vazio é o perfil mínimo e tem de arrancar: funcionalidade desligada é configuração
    válida, não caminho não suportado.
    """
    return st.sets(st.sampled_from(SINALIZADORES_DE_PLATAFORMA), min_size=0, max_size=5).map(
        frozenset
    )


def combinacao_de_adaptadores() -> st.SearchStrategy[frozenset[str]]:
    """Subconjunto dos adaptadores substituíveis das três camadas de `R119.2`.

    Trocar adaptador não altera resultado determinístico: gerar combinações é o que permite
    verificar isso sem instanciar nenhum adaptador real.
    """
    adaptadores = (
        "armazenamento_de_arquivo",
        "repositorio_transacional",
        "agendador",
        "canal_de_notificacao",
        "indice_vetorial",
        "provedor_de_modelo_de_linguagem",
        "provedor_de_embedding",
        "conector_de_fonte",
    )
    return st.sets(st.sampled_from(adaptadores), min_size=0, max_size=len(adaptadores)).map(
        frozenset
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class ColecaoPaginavel:
    """Coleção paginável, com total, tamanho de página e cursor (`R116`, `R97`).

    `tamanho_de_pagina` inclui 0 e 1 porque são as fronteiras que quebram paginação escrita com
    divisão ingênua, e `total` inclui 0 porque coleção vazia é resposta válida, não erro.
    """

    total: int
    tamanho_de_pagina: int
    pagina: int


def colecao_paginavel() -> st.SearchStrategy[ColecaoPaginavel]:
    """Coleção paginável com as fronteiras de total e de tamanho de página."""
    return st.builds(
        ColecaoPaginavel,
        total=st.one_of(st.sampled_from((0, 1, 2, 100)), st.integers(min_value=0, max_value=1_000)),
        tamanho_de_pagina=st.sampled_from((1, 10, 20, 100)),
        pagina=st.integers(min_value=1, max_value=20),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseMultiTitular:
    """Registro com titular e responsável, para o preparo multi-titular (`R118`).

    `tenant_id` e `usuario_responsavel_id` existem em toda entidade de negócio; gerar dois titulares
    distintos é o que permite verificar o isolamento sem banco.
    """

    titular: UUID
    usuario_responsavel: UUID
    titular_da_consulta: UUID


def base_multi_titular() -> st.SearchStrategy[BaseMultiTitular]:
    """Par titular do registro × titular da consulta, coincidindo em metade do espaço."""
    return st.builds(
        _base_multi_titular_coerente,
        titular=st.sampled_from(_TITULARES),
        usuario_responsavel=st.uuids(),
        mesma_titularidade=st.booleans(),
        outro_titular=st.sampled_from(_TITULARES),
    )


_TITULARES: Final[tuple[UUID, ...]] = (
    UUID("00000000-0000-4000-8000-000000000001"),
    UUID("00000000-0000-4000-8000-000000000002"),
    UUID("00000000-0000-4000-8000-000000000003"),
)


def _base_multi_titular_coerente(
    *,
    titular: UUID,
    usuario_responsavel: UUID,
    mesma_titularidade: bool,
    outro_titular: UUID,
) -> BaseMultiTitular:
    return BaseMultiTitular(
        titular=titular,
        usuario_responsavel=usuario_responsavel,
        titular_da_consulta=titular if mesma_titularidade else outro_titular,
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class EvidenciaEmTornoDaDataDeCorte:
    """Evidência posicionada em relação à data de corte da versão de análise (`R120.4`)."""

    data_de_corte: datetime
    observada_em: datetime
    deslocamento_em_dias: int


def evidencia_em_torno_da_data_de_corte() -> st.SearchStrategy[EvidenciaEmTornoDaDataDeCorte]:
    """Evidência antes, exatamente na, e depois da data de corte.

    O deslocamento zero é obrigatório: é ele que distingue "até a data de corte" de "antes da data
    de corte", e é o caso que uma amostragem contínua de datas quase nunca produziria.
    """
    return st.builds(
        _evidencia_em_torno_do_corte,
        data_de_corte=data_hora_br(),
        deslocamento_em_dias=st.sampled_from((-30, -1, 0, 1, 30)),
    )


def _evidencia_em_torno_do_corte(
    *,
    data_de_corte: datetime,
    deslocamento_em_dias: int,
) -> EvidenciaEmTornoDaDataDeCorte:
    return EvidenciaEmTornoDaDataDeCorte(
        data_de_corte=data_de_corte,
        observada_em=data_de_corte + timedelta(days=deslocamento_em_dias),
        deslocamento_em_dias=deslocamento_em_dias,
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class EventoDePlataforma:
    """Evento de plataforma, com situação de trabalho assíncrono e categoria de erro opcional."""

    nome: str
    ocorrido_em: datetime
    situacao: SituacaoDeTrabalhoAssincrono
    categoria_de_erro: CategoriaDeErro | None
    identificador_de_correlacao: UUID


def sequencia_de_eventos() -> st.SearchStrategy[tuple[EventoDePlataforma, ...]]:
    """Sequência de eventos em ordem cronológica não decrescente.

    A ordem é construída, não sorteada, porque a situação de um trabalho assíncrono nunca regride
    de concluída para em execução (`P21.12`) — e uma sequência fora de ordem testaria o gerador em
    lugar do sistema.
    """
    evento = st.builds(
        EventoDePlataforma,
        nome=st.sampled_from(
            ("captura_registrada", "analise_concluida", "pendencia_aberta", "alerta_emitido")
        ),
        ocorrido_em=data_hora_br(),
        situacao=st.sampled_from(SituacaoDeTrabalhoAssincrono),
        categoria_de_erro=st.one_of(st.none(), st.sampled_from(CategoriaDeErro)),
        identificador_de_correlacao=st.uuids(),
    )
    return st.lists(evento, min_size=0, max_size=8).map(
        lambda eventos: tuple(sorted(eventos, key=lambda registro: registro.ocorrido_em))
    )
