"""`MT-14` — catálogo de erros completo e sem detalhe técnico.

**O que verifica** (`R114.2`, `R114.9`, `D100`, `D101`): cada uma das **15** categorias de
`R114.2` tem código, mensagem amigável em português e mapeamento declarados; e nenhuma mensagem
apresentada ao usuário contém rastro de execução, consulta ao banco de dados, caminho de arquivo
interno ou mensagem de biblioteca.

**Como falha**: categoria sem código, sem mensagem ou sem mapeamento, nomeando a categoria; ou
mensagem com detalhe técnico, nomeando a mensagem e o rastro encontrado.

**Estado hoje**: falha por conteúdo ausente. O catálogo declarado em *Error Handling* é conferido
de fato — as 15 categorias, os códigos `RAD-*`, o estado HTTP e a ausência de detalhe técnico nas
mensagens —; o catálogo da implementação, `CATALOGO_DE_ERROS` em `radar/plataforma/erros.py`,
ainda não existe.
"""

from __future__ import annotations

import re

from testes.meta.apoio import (
    falhar_por_conteudo_ausente,
    secao,
    simbolo_opcional,
    tabela_apos,
    texto_do_design,
    texto_do_requirements,
)

TITULO_DE_R114 = "### Requirement 114: Catálogo de erros apresentáveis"
MARCADOR_DO_CATALOGO = "### Catálogo de erros apresentáveis — 15 categorias (`R114`)"
TOTAL_DE_CATEGORIAS = 15

MODULO_DOS_ERROS = "radar.plataforma.erros"
SIMBOLO_DO_CATALOGO = "CATALOGO_DE_ERROS"

#: Rastros que jamais aparecem em mensagem apresentada ao usuário (`R114.3`).
RASTROS_TECNICOS = (
    r"Traceback",
    r"\bSELECT\b",
    r"\bINSERT\b",
    r"\bUPDATE\b",
    r"psycopg",
    r"sqlalchemy",
    r"pydantic",
    r"\.py\b",
    r"[A-Za-z]:\\\\",
    r"/usr/",
    r"/var/",
    r"\bException\b",
    r"\bstack trace\b",
)


def _categorias_de_r114() -> list[str]:
    """As 15 categorias declaradas pelo critério 2 de `R114`."""
    trecho = secao(texto_do_requirements(), TITULO_DE_R114, nivel="### ")
    criterio = re.search(r"^2\. .*?categorias:\s*(.+)$", trecho, re.MULTILINE)
    assert criterio is not None, "MT-14 — critério `R114.2` não encontrado no requirements"
    return re.findall(r"`([A-Z_]+)`", criterio.group(1))


def _catalogo_declarado() -> dict[str, tuple[str, str, str]]:
    """Categoria → (código, mensagem amigável, estado HTTP), conforme *Error Handling*."""
    declarado: dict[str, tuple[str, str, str]] = {}
    for celulas in tabela_apos(texto_do_design(), MARCADOR_DO_CATALOGO):
        if not celulas[0].startswith("`"):
            continue
        categoria = celulas[0].strip("`")
        declarado[categoria] = (celulas[1].strip("`"), celulas[2], celulas[4].strip("`"))
    return declarado


def test_mt_14_as_15_categorias_tem_codigo_mensagem_e_mapeamento_declarados() -> None:
    categorias = _categorias_de_r114()
    assert len(categorias) == TOTAL_DE_CATEGORIAS, (
        f"MT-14 — `R114.2` declara {TOTAL_DE_CATEGORIAS} categorias; encontradas {len(categorias)}"
    )

    declarado = _catalogo_declarado()
    sem_linha = [categoria for categoria in categorias if categoria not in declarado]
    assert not sem_linha, f"MT-14 — categoria de `R114.2` sem linha no catálogo: {sem_linha}"

    incompletas = [
        f"{categoria}: código={codigo!r}, mensagem={bool(mensagem)}, HTTP={http!r}"
        for categoria, (codigo, mensagem, http) in declarado.items()
        if not re.fullmatch(r"RAD-\d{3}", codigo)
        or not mensagem
        or not re.fullmatch(r"\d{3}", http)
    ]
    assert not incompletas, (
        f"MT-14 — categoria sem código `RAD-*`, sem mensagem amigável ou sem mapeamento de estado "
        f"HTTP: {incompletas}"
    )

    sobrando = sorted(set(declarado) - set(categorias))
    assert not sobrando, (
        f"MT-14 — categoria no catálogo e fora de `R114.2`. Catálogo paralelo é defeito, não "
        f"alternativa (`R114.5`, `D100`): {sobrando}"
    )


def test_mt_14_nenhuma_mensagem_apresentada_contem_detalhe_tecnico() -> None:
    com_detalhe: list[str] = []
    for categoria, (_, mensagem, _) in _catalogo_declarado().items():
        for rastro in RASTROS_TECNICOS:
            if re.search(rastro, mensagem):
                com_detalhe.append(f"{categoria}: rastro {rastro!r} em {mensagem[:60]!r}")
    assert not com_detalhe, (
        "MT-14 — mensagem apresentada ao usuário com rastro de execução, consulta ao banco, "
        f"caminho interno ou mensagem de biblioteca (`R114.3`): {com_detalhe}"
    )


def test_mt_14_o_catalogo_da_implementacao_declara_as_15_categorias() -> None:
    categorias = _categorias_de_r114()
    catalogo = simbolo_opcional(MODULO_DOS_ERROS, SIMBOLO_DO_CATALOGO)

    if catalogo is None:
        falhar_por_conteudo_ausente(
            codigo="MT-14",
            verifica="cada uma das 15 categorias de `R114.2` tem código, mensagem amigável em "
            "português e mapeamento declarados",
            falta=f"`{SIMBOLO_DO_CATALOGO}` em `{MODULO_DOS_ERROS}`",
            requisitos="R114.1, R114.2, R114.9",
            orfaos=categorias,
            rotulo_dos_orfaos="categoria(s) de erro sem código, mensagem e mapeamento na "
            "implementação",
            observacoes=[
                "O catálogo declarado em *Error Handling* está completo e sem detalhe técnico; "
                "o que falta é o catálogo executável, que é o único do produto (`R114.5`).",
            ],
        )
