"""`MT-16` — nove estados por tela.

**O que verifica** (`R122.1`, `R122.10`, `REG-054`, `D101`): cada `DeclaracaoDeTela` declara os
**nove** valores de `EstadoDeTela` — carregando, esqueleto, vazio, erro, repetição, parcial, dado
obsoleto, confirmação e sucesso. A tela é **dado**, não convenção de implementação, e é isso que
permite reprovar tela sem estado vazio.

**Como falha**: tela com estado ausente, **nomeando a tela e o estado** (`REG-054`).

**Estado hoje**: falha por conteúdo ausente. Os nove estados existem em `EstadoDeTela` e são
conferidos aqui contra a enumeração de `R122.1`; `DeclaracaoDeTela` e o catálogo de telas não
existem, e nenhum dos nove destinos de navegação de `R123.1` tem estado declarado.
"""

from __future__ import annotations

import re
from collections.abc import Iterable

from testes.meta.apoio import (
    falhar_por_conteudo_ausente,
    itens_enumerados,
    modulo_opcional,
    secao,
    simbolo_opcional,
    texto_do_requirements,
)

TITULO_DE_R122 = "### Requirement 122: Estados obrigatórios de tela"
TITULO_DE_R123 = "### Requirement 123: Navegação e ordem de leitura da análise"

MODULO_DOS_ENUMS = "radar.nucleo.enumeracoes_de_infraestrutura"
ENUM_DOS_ESTADOS = "EstadoDeTela"
MODULO_DA_APRESENTACAO = "radar.apresentacao.telas"
SIMBOLO_DA_DECLARACAO = "DeclaracaoDeTela"
SIMBOLO_DO_CATALOGO = "TELAS_DECLARADAS"

TOTAL_DE_ESTADOS = 9
TOTAL_DE_DESTINOS = 9


def _criterio(titulo: str, numero: int, codigo: str) -> str:
    trecho = secao(texto_do_requirements(), titulo, nivel="### ")
    criterio = re.search(rf"^{numero}\. (.+)$", trecho, re.MULTILINE)
    assert criterio is not None, f"MT-16 — critério `{codigo}` não encontrado no requirements"
    return criterio.group(1)


def _estados_de_r122() -> list[str]:
    return itens_enumerados(_criterio(TITULO_DE_R122, 1, "R122.1"), apos="estados: ")


def _destinos_de_r123() -> list[str]:
    return itens_enumerados(_criterio(TITULO_DE_R123, 1, "R123.1"), apos="destinos: ")


def _estados_implementados() -> list[str]:
    modulo = modulo_opcional(MODULO_DOS_ENUMS)
    assert modulo is not None, f"MT-16 — módulo de enums ausente: `{MODULO_DOS_ENUMS}`"
    enum = getattr(modulo, ENUM_DOS_ESTADOS, None)
    assert enum is not None, (
        f"MT-16 — `{ENUM_DOS_ESTADOS}` ausente de `{MODULO_DOS_ENUMS}`; sem ele não há estado a "
        "exigir de cada tela"
    )
    assert isinstance(enum, Iterable), f"MT-16 — `{ENUM_DOS_ESTADOS}` não é enumerável"
    return [str(valor.value) for valor in enum]


def test_mt_16_os_nove_estados_de_tela_estao_declarados_e_implementados() -> None:
    do_requirements = _estados_de_r122()
    assert len(do_requirements) == TOTAL_DE_ESTADOS, (
        f"MT-16 — `R122.1` declara exatamente {TOTAL_DE_ESTADOS} estados; "
        f"enumerados {len(do_requirements)}: {do_requirements}"
    )

    implementados = _estados_implementados()
    assert len(implementados) == TOTAL_DE_ESTADOS, (
        f"MT-16 — `{ENUM_DOS_ESTADOS}` tem {TOTAL_DE_ESTADOS} valores; "
        f"encontrados {len(implementados)}: {implementados}"
    )


def test_mt_16_cada_tela_declarada_traz_os_nove_estados() -> None:
    estados = _estados_implementados()
    declaracao = simbolo_opcional(MODULO_DA_APRESENTACAO, SIMBOLO_DA_DECLARACAO)
    catalogo = simbolo_opcional(MODULO_DA_APRESENTACAO, SIMBOLO_DO_CATALOGO)

    if declaracao is None or catalogo is None:
        destinos = _destinos_de_r123()
        assert len(destinos) == TOTAL_DE_DESTINOS, (
            f"MT-16 — `R123.1` declara {TOTAL_DE_DESTINOS} destinos de navegação; "
            f"enumerados {len(destinos)}"
        )
        falhar_por_conteudo_ausente(
            codigo="MT-16",
            verifica=f"cada `{SIMBOLO_DA_DECLARACAO}` declara os {TOTAL_DE_ESTADOS} valores de "
            f"`{ENUM_DOS_ESTADOS}`",
            falta=f"`{SIMBOLO_DA_DECLARACAO}` e `{SIMBOLO_DO_CATALOGO}` em "
            f"`{MODULO_DA_APRESENTACAO}`",
            requisitos="R122.1, R122.10",
            orfaos=[f"{destino}: nenhum dos {TOTAL_DE_ESTADOS} estados" for destino in destinos],
            rotulo_dos_orfaos="tela(s) sem estado declarado",
            observacoes=[
                f"Os {TOTAL_DE_ESTADOS} estados exigidos são: {', '.join(estados)}.",
                "Tela que dependa de dado remoto e não declare o estado vazio é reprovada por "
                "`REG-054`.",
            ],
        )

    assert isinstance(catalogo, Iterable), (
        f"MT-16 — `{SIMBOLO_DO_CATALOGO}` é declarado como coleção de telas; "
        f"encontrado {type(catalogo).__name__}"
    )
    sem_estado: list[str] = []
    for tela in catalogo:
        declarados = {str(estado) for estado in getattr(tela, "estados", ())}
        nome = str(getattr(tela, "nome", tela))
        sem_estado.extend(f"{nome}: {estado}" for estado in estados if estado not in declarados)
    assert not sem_estado, (
        f"MT-16 — tela com estado ausente, nomeando a tela e o estado (`REG-054`): {sem_estado}"
    )
