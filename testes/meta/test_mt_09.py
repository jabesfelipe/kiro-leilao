"""`MT-09` — contagem de enums.

**O que verifica** (`R62.4`, `R73.3`, `D101`): cada um dos **60 enums de negócio** e dos **7 enums
de infraestrutura** declarados em *Data Models* do design tem, na implementação, exatamente a
quantidade de valores ali fixada. As contagens são contrato: alterar qualquer uma delas é mudança
de nível `alto` ou `critico` por `R62.4`.

**Como falha**: valor acrescentado ou removido sem revisão, nomeando o enum, a quantidade
declarada e a encontrada; enum declarado no design e ausente da implementação, nomeando o enum; ou
enum na implementação sem declaração no design.

Este meta-teste verifica **conteúdo já entregue** — `src/radar/nucleo/enumeracoes.py` e
`src/radar/nucleo/enumeracoes_de_infraestrutura.py` — e por isso **passa** hoje. É o portão contra
o próximo valor acrescentado em silêncio.
"""

from __future__ import annotations

import re
from enum import EnumMeta

from testes.meta.apoio import modulo_opcional, secao, texto_do_design

TITULO_DOS_ENUMS_DE_NEGOCIO = "### Enumerações"
TITULO_DOS_ENUMS_DE_INFRAESTRUTURA = "#### Enums de infraestrutura — 7 enums"

MODULO_DE_NEGOCIO = "radar.nucleo.enumeracoes"
MODULO_DE_INFRAESTRUTURA = "radar.nucleo.enumeracoes_de_infraestrutura"

TOTAL_DE_ENUMS_DE_NEGOCIO = 60
TOTAL_DE_ENUMS_DE_INFRAESTRUTURA = 7


def _declaracoes(trecho: str, coluna_dos_valores: int) -> dict[str, int]:
    """Enum → quantidade de valores, lida das tabelas de *Data Models*.

    A linha combinada `Probabilidade / Impacto / Severidade` com `3 / 4 / 4` é tratada pelo
    emparelhamento posicional entre os nomes e as contagens em negrito da mesma linha.
    """
    declaracoes: dict[str, int] = {}
    for linha in trecho.splitlines():
        if not linha.startswith("| `"):
            continue
        celulas = [celula.strip() for celula in linha.strip().strip("|").split("|")]
        nomes = re.findall(r"`([A-Za-z][A-Za-z0-9_]*)`", celulas[0])
        contagens = re.findall(r"\*\*(\d+)\*\*", celulas[coluna_dos_valores])
        assert len(nomes) == len(contagens), (
            f"MT-09 — linha de *Data Models* com {len(nomes)} enum(s) e {len(contagens)} "
            f"contagem(ns) em negrito, o que torna a contagem ambígua: {linha[:120]}"
        )
        declaracoes.update(
            {nome: int(contagem) for nome, contagem in zip(nomes, contagens, strict=True)}
        )
    return declaracoes


def _declaracoes_de_negocio() -> dict[str, int]:
    trecho = secao(texto_do_design(), TITULO_DOS_ENUMS_DE_NEGOCIO, nivel="#### ")
    return _declaracoes(trecho, coluna_dos_valores=2)


def _declaracoes_de_infraestrutura() -> dict[str, int]:
    trecho = secao(texto_do_design(), TITULO_DOS_ENUMS_DE_INFRAESTRUTURA, nivel="### ")
    return _declaracoes(trecho, coluna_dos_valores=1)


def _enums_implementados(nome_do_modulo: str) -> dict[str, int]:
    """Enum → quantidade de valores, lida do módulo da implementação."""
    modulo = modulo_opcional(nome_do_modulo)
    assert modulo is not None, (
        f"MT-09 — módulo de enums ausente: `{nome_do_modulo}`. As contagens de *Data Models* "
        "não têm o que verificar."
    )
    implementados: dict[str, int] = {}
    for nome in dir(modulo):
        valor = getattr(modulo, nome)
        if isinstance(valor, EnumMeta) and valor.__module__ == nome_do_modulo:
            implementados[nome] = len(list(valor))
    return implementados


def _conferir(declaradas: dict[str, int], implementadas: dict[str, int], grupo: str) -> None:
    ausentes = sorted(set(declaradas) - set(implementadas))
    assert not ausentes, (
        f"MT-09 — enum de {grupo} declarado em *Data Models* e não implementado: {ausentes}"
    )

    sobrando = sorted(set(implementadas) - set(declaradas))
    assert not sobrando, (
        f"MT-09 — enum de {grupo} implementado e não declarado em *Data Models*: {sobrando}"
    )

    divergentes = [
        f"{nome}: declarado {declaradas[nome]}, implementado {implementadas[nome]}"
        for nome in sorted(declaradas)
        if declaradas[nome] != implementadas[nome]
    ]
    assert not divergentes, (
        f"MT-09 — contagem de valores divergente em enum de {grupo}, o que é mudança de nível "
        f"`alto` ou `critico` por `R62.4`: {divergentes}"
    )


def test_mt_09_os_60_enums_de_negocio_tem_a_contagem_declarada() -> None:
    declaradas = _declaracoes_de_negocio()
    assert len(declaradas) == TOTAL_DE_ENUMS_DE_NEGOCIO, (
        f"MT-09 — *Data Models* declara {TOTAL_DE_ENUMS_DE_NEGOCIO} enums de negócio; "
        f"tabulados {len(declaradas)}"
    )
    _conferir(declaradas, _enums_implementados(MODULO_DE_NEGOCIO), "negócio")


def test_mt_09_os_7_enums_de_infraestrutura_tem_a_contagem_declarada() -> None:
    declaradas = _declaracoes_de_infraestrutura()
    assert len(declaradas) == TOTAL_DE_ENUMS_DE_INFRAESTRUTURA, (
        f"MT-09 — *Data Models* declara {TOTAL_DE_ENUMS_DE_INFRAESTRUTURA} enums de "
        f"infraestrutura; tabulados {len(declaradas)}"
    )
    _conferir(declaradas, _enums_implementados(MODULO_DE_INFRAESTRUTURA), "infraestrutura")


def test_mt_09_negocio_e_infraestrutura_permanecem_contados_separadamente() -> None:
    de_negocio = set(_declaracoes_de_negocio())
    de_infraestrutura = set(_declaracoes_de_infraestrutura())
    intersecao = sorted(de_negocio & de_infraestrutura)
    assert not intersecao, (
        "MT-09 — enum contado nos dois grupos. A fronteira entre negócio e infraestrutura é "
        f"contrato (`D96`): {intersecao}"
    )
