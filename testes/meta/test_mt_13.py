"""`MT-13` — titular em toda entidade de negócio.

**O que verifica** (`R118.1`, `R118.10`, `D96`, `D101`): cada entidade de negócio do dicionário
declara `tenant_id` e `usuario_responsavel_id`, com índice por `tenant_id`. Não é campo opcional
acrescentado por conveniência: é a condição para que abrir o produto a outros investidores **não
exija migração** das entidades já gravadas (`R118.9`).

**Como falha**: entidade sem os dois identificadores, **nomeada pela falha**; ou entidade com os
campos e sem índice por `tenant_id`, também nomeada.

**Estado hoje**: falha por conteúdo ausente. O dicionário do design é lido aqui, bloco a bloco, e
o esquema `db/schema.sql` é percorrido de fato: nenhuma das entidades de negócio tem tabela com os
dois identificadores. As entidades de infraestrutura e de plataforma **não** entram nesta
verificação (`D96`).
"""

from __future__ import annotations

import re

from testes.meta.apoio import (
    RAIZ_DO_PROJETO,
    falhar_por_conteudo_ausente,
    secao,
    tabela_apos,
    texto_do_design,
)

TITULO_DO_DICIONARIO = "### Dicionário de entidades"
ESQUEMA = "db/schema.sql"
TOTAL_DECLARADO = 63
COLUNAS_DE_TITULAR = ("tenant_id", "usuario_responsavel_id")


def _blocos_do_dicionario() -> list[tuple[str, int]]:
    """Blocos do dicionário: (título, quantidade declarada no próprio título)."""
    trecho = secao(texto_do_design(), TITULO_DO_DICIONARIO, nivel="### ")
    return [
        (titulo, int(quantidade))
        for titulo, quantidade in re.findall(
            r"^\*\*(.+?) — (\d+) entidades\*\*$", trecho, re.MULTILINE
        )
    ]


def _entidades_do_dicionario() -> dict[str, str]:
    """Entidade de negócio → bloco do dicionário que a declara."""
    trecho = secao(texto_do_design(), TITULO_DO_DICIONARIO, nivel="### ")
    entidades: dict[str, str] = {}
    for titulo, quantidade in _blocos_do_dicionario():
        marcador = f"**{titulo} — {quantidade} entidades**"
        for celulas in tabela_apos(trecho, marcador):
            nome = celulas[0]
            if nome.startswith("`") and nome.endswith("`"):
                entidades[nome.strip("`")] = titulo
    return entidades


def _tabelas_do_esquema() -> dict[str, str]:
    """Tabela → corpo do `CREATE TABLE`, conforme o esquema versionado."""
    caminho = RAIZ_DO_PROJETO / ESQUEMA
    if not caminho.is_file():
        return {}
    conteudo = caminho.read_text(encoding="utf-8")
    return dict(
        re.findall(r"CREATE TABLE\s+(?:IF NOT EXISTS\s+)?(\w+)\s*\((.*?)\n\);", conteudo, re.DOTALL)
    )


def test_mt_13_o_dicionario_tabula_as_entidades_de_cada_bloco() -> None:
    blocos = _blocos_do_dicionario()
    assert blocos, "MT-13 — dicionário de entidades sem blocos declarados no design"

    trecho = secao(texto_do_design(), TITULO_DO_DICIONARIO, nivel="### ")
    divergentes: list[str] = []
    for titulo, quantidade in blocos:
        marcador = f"**{titulo} — {quantidade} entidades**"
        tabuladas = [
            celulas[0] for celulas in tabela_apos(trecho, marcador) if celulas[0].startswith("`")
        ]
        if len(tabuladas) != quantidade:
            divergentes.append(
                f"{titulo}: título declara {quantidade}, tabela traz {len(tabuladas)}"
            )

    assert not divergentes, (
        "MT-13 — bloco do dicionário com contagem em desacordo com a tabulação. Prevalece a "
        f"tabulação (`D89`), e o título é que deve ser corrigido: {divergentes}"
    )


def test_mt_13_toda_entidade_de_negocio_declara_titular_e_usuario_responsavel() -> None:
    entidades = _entidades_do_dicionario()
    tabelas = _tabelas_do_esquema()
    tabuladas = len(entidades)

    sem_titular: list[str] = []
    sem_indice: list[str] = []
    for entidade, bloco in sorted(entidades.items()):
        corpo = tabelas.get(entidade)
        if corpo is None or any(coluna not in corpo for coluna in COLUNAS_DE_TITULAR):
            sem_titular.append(f"{entidade} ({bloco})")
        elif not re.search(rf"CREATE INDEX[^;]+ON {entidade} \(tenant_id", corpo):
            sem_indice.append(entidade)

    if sem_titular:
        falhar_por_conteudo_ausente(
            codigo="MT-13",
            verifica="cada entidade de negócio do dicionário declara `tenant_id` e "
            "`usuario_responsavel_id`, com índice por `tenant_id`",
            falta=f"as entidades de negócio no esquema `{ESQUEMA}` com os dois identificadores "
            "de titular",
            requisitos="R118.1, R118.10",
            orfaos=sem_titular,
            rotulo_dos_orfaos="entidade(s) de negócio sem os dois identificadores",
            observacoes=[
                f"O dicionário do design declara {TOTAL_DECLARADO} entidades de negócio e "
                f"tabula {tabuladas}. Enquanto a divergência não for resolvida, a tabulação é o "
                "que este meta-teste percorre (`D89`).",
                "As 15 entidades de infraestrutura e de plataforma estão fora desta "
                "verificação por `D96`.",
            ],
        )

    assert not sem_indice, (
        f"MT-13 — entidade de negócio com os dois identificadores e sem índice por `tenant_id`, "
        f"o que torna o isolamento por titular uma varredura: {sem_indice}"
    )
