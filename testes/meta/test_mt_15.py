"""`MT-15` — identificador de correlação em toda execução relevante.

**O que verifica** (`R111.2`, `R111.3`, `R111.10`, `D101`): cada uma das **treze** espécies de
execução relevante de `R111.3` registra identificador de correlação e os **treze** atributos de
`R111.2` — identificador de correlação, identificador de rastro, identificador da execução, log
estruturado, métricas, duração, situação, erro quando houver, quantidade de repetições, custo de
IA, tokens, fonte e versões aplicadas.

**Como falha**: execução relevante sem identificador, **nomeada pela falha**; ou execução com
identificador e sem um dos treze atributos, nomeando a execução e o atributo.

**Estado hoje**: falha por conteúdo ausente. As treze espécies e os treze atributos são lidos do
requirements e conferidos aqui; `EXECUCOES_RELEVANTES` e o registro de execução em
`radar/plataforma/observabilidade.py` ainda não existem.
"""

from __future__ import annotations

import re
import unicodedata

from testes.meta.apoio import (
    falhar_por_conteudo_ausente,
    itens_enumerados,
    secao,
    simbolo_opcional,
    texto_do_requirements,
)

TITULO_DE_R111 = "### Requirement 111: Observabilidade e identificador de correlação"
TOTAL_DE_ESPECIES = 13
TOTAL_DE_ATRIBUTOS = 13

MODULO_DA_OBSERVABILIDADE = "radar.plataforma.observabilidade"
SIMBOLO_DAS_EXECUCOES = "EXECUCOES_RELEVANTES"


def _identificador(termo: str) -> str:
    """Forma comparável entre a prosa do requirements e o identificador da implementação."""
    sem_acento = unicodedata.normalize("NFKD", termo).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "_", sem_acento.lower()).strip("_")


def _criterio(numero: int) -> str:
    trecho = secao(texto_do_requirements(), TITULO_DE_R111, nivel="### ")
    criterio = re.search(rf"^{numero}\. (.+)$", trecho, re.MULTILINE)
    assert criterio is not None, f"MT-15 — critério `R111.{numero}` não encontrado no requirements"
    return criterio.group(1)


def _atributos_de_execucao() -> list[str]:
    return itens_enumerados(_criterio(2), apos="atributos: ")


def _especies_de_execucao_relevante() -> list[str]:
    return itens_enumerados(_criterio(3), apos="no mínimo: ")


def test_mt_15_o_requirements_declara_treze_especies_e_treze_atributos() -> None:
    especies = _especies_de_execucao_relevante()
    atributos = _atributos_de_execucao()
    assert len(especies) == TOTAL_DE_ESPECIES, (
        f"MT-15 — `R111.3` declara {TOTAL_DE_ESPECIES} espécies de execução relevante; "
        f"enumeradas {len(especies)}: {especies}"
    )
    assert len(atributos) == TOTAL_DE_ATRIBUTOS, (
        f"MT-15 — `R111.2` declara {TOTAL_DE_ATRIBUTOS} atributos por execução; "
        f"enumerados {len(atributos)}: {atributos}"
    )
    assert "identificador de correlação" in atributos, (
        "MT-15 — o identificador de correlação é o primeiro dos treze atributos de `R111.2` e "
        f"não está entre os enumerados: {atributos}"
    )


def test_mt_15_toda_execucao_relevante_registra_identificador_de_correlacao() -> None:
    especies = _especies_de_execucao_relevante()
    execucoes = simbolo_opcional(MODULO_DA_OBSERVABILIDADE, SIMBOLO_DAS_EXECUCOES)

    if execucoes is None:
        falhar_por_conteudo_ausente(
            codigo="MT-15",
            verifica="cada uma das treze espécies de execução relevante de `R111.3` registra "
            "identificador de correlação e os treze atributos de `R111.2`",
            falta=f"`{SIMBOLO_DAS_EXECUCOES}` em `{MODULO_DA_OBSERVABILIDADE}`",
            requisitos="R111.1, R111.2, R111.3, R111.10",
            orfaos=especies,
            rotulo_dos_orfaos="execução(ões) relevante(s) sem registro de identificador de "
            "correlação",
            observacoes=[
                "O identificador de correlação é o que liga a falha apresentada ao usuário "
                "(`R111.7`, `R114.3`) ao registro técnico no log estruturado (`R114.4`).",
            ],
        )

    assert isinstance(execucoes, tuple | list), (
        f"MT-15 — `{SIMBOLO_DAS_EXECUCOES}` é declarado como sequência de espécies de execução; "
        f"encontrado {type(execucoes).__name__}"
    )
    declaradas = {_identificador(str(item)) for item in execucoes}
    ausentes = [especie for especie in especies if _identificador(especie) not in declaradas]
    assert not ausentes, (
        f"MT-15 — espécie de execução relevante de `R111.3` sem correspondente em "
        f"`{SIMBOLO_DAS_EXECUCOES}`: {ausentes}"
    )
