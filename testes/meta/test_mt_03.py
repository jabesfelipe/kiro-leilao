"""`MT-03` — cobertura de catálogo de checklist em qualquer versão configurada.

**O que verifica** (`R73.3`, `R92.7`, `D83`, `D101`): a **versão 1 do checklist padrão** declara
`MC-001` a `MC-136` (Anexo A), `B-01` a `B-27` (Anexo B) e `C-01` a `C-71` (Anexo C.1) —
136 + 27 + 71 = **234** itens; e, para toda `VersaoDeChecklist` ativa, todo item aplicável ao
escopo resolvido tem resultado registrado.

**Como falha**: item ausente do catálogo, nomeando o identificador; ou versão configurada com
item aplicável sem resultado registrado, nomeando a versão e o item.

**Estado hoje**: falha por conteúdo ausente. Os 234 identificadores existem nos anexos e são
conferidos aqui; o catálogo da implementação — `CHECKLIST_PADRAO_VERSAO_1` em
`radar/diligencia/catalogo.py` — e o seed de `itens_de_checklist` gerado a partir dos anexos
ainda não existem, e é isso que a falha nomeia.
"""

from __future__ import annotations

import re

from testes.meta.apoio import (
    caminho_ausente,
    falhar_por_conteudo_ausente,
    identificadores,
    secao,
    simbolo_opcional,
    texto_do_requirements,
)

TITULO_DO_ANEXO_A = "## Anexo A — Checklist Mestre de Análise de Leilão (normativo, 136 itens)"
TITULO_DO_ANEXO_B = "## Anexo B — Verificações Complementares de Arrematação (normativo, 27 itens)"
TITULO_DO_ANEXO_C = (
    "## Anexo C — Due Diligence Individual, Hard Stops e Disciplina de Lance (normativo)"
)
TITULO_DE_C1 = "### C.1 Checklist de Due Diligence — 71 critérios"

TOTAL_DE_ITENS = 234
MODULO_DO_CATALOGO = "radar.diligencia.catalogo"
SIMBOLO_DO_CATALOGO = "CHECKLIST_PADRAO_VERSAO_1"
SEED_DO_CATALOGO = "db/seeds/itens_de_checklist.sql"


def _itens_do_anexo_a() -> list[str]:
    return identificadores(secao(texto_do_requirements(), TITULO_DO_ANEXO_A), r"MC-\d{3}")


def _itens_do_anexo_b() -> list[str]:
    return identificadores(secao(texto_do_requirements(), TITULO_DO_ANEXO_B), r"B-\d{2}")


def _criterios_de_c1() -> list[int]:
    """Números dos critérios de due diligence das tabelas de duas colunas de `C.1`."""
    anexo_c = secao(texto_do_requirements(), TITULO_DO_ANEXO_C)
    trecho = secao(anexo_c, TITULO_DE_C1, nivel="### ")
    numeros: set[int] = set()
    for linha in trecho.splitlines():
        if not linha.startswith("|"):
            continue
        for celula in linha.strip().strip("|").split("|"):
            if re.fullmatch(r"\d{1,2}", celula.strip()):
                numeros.add(int(celula.strip()))
    return sorted(numeros)


def test_mt_03_a_versao_1_declara_os_234_itens() -> None:
    do_anexo_a = _itens_do_anexo_a()
    do_anexo_b = _itens_do_anexo_b()
    criterios = _criterios_de_c1()

    esperados_a = [f"MC-{numero:03d}" for numero in range(1, 137)]
    esperados_b = [f"B-{numero:02d}" for numero in range(1, 28)]

    assert do_anexo_a == esperados_a, (
        "MT-03 — o Anexo A declara `MC-001` a `MC-136`, sem lacuna. "
        f"Faltando: {sorted(set(esperados_a) - set(do_anexo_a))}; "
        f"sobrando: {sorted(set(do_anexo_a) - set(esperados_a))}"
    )
    assert do_anexo_b == esperados_b, (
        "MT-03 — o Anexo B declara `B-01` a `B-27`, sem lacuna. "
        f"Faltando: {sorted(set(esperados_b) - set(do_anexo_b))}; "
        f"sobrando: {sorted(set(do_anexo_b) - set(esperados_b))}"
    )
    assert criterios == list(range(1, 72)), (
        "MT-03 — o Anexo C.1 declara 71 critérios, numerados de 1 a 71, que originam `C-01` a "
        f"`C-71` (`D17`). Encontrados {len(criterios)}: "
        f"faltando {sorted(set(range(1, 72)) - set(criterios))}"
    )

    total = len(do_anexo_a) + len(do_anexo_b) + len(criterios)
    assert total == TOTAL_DE_ITENS, (
        f"MT-03 — 136 + 27 + 71 = {TOTAL_DE_ITENS} itens na versão 1 do checklist padrão; "
        f"a soma dos anexos deu {total}"
    )


def test_mt_03_todo_item_do_catalogo_tem_entrada_na_implementacao() -> None:
    itens = [
        *_itens_do_anexo_a(),
        *_itens_do_anexo_b(),
        *[f"C-{numero:02d}" for numero in _criterios_de_c1()],
    ]
    catalogo = simbolo_opcional(MODULO_DO_CATALOGO, SIMBOLO_DO_CATALOGO)
    seed_ausente = caminho_ausente(SEED_DO_CATALOGO)

    if catalogo is None or seed_ausente:
        falhar_por_conteudo_ausente(
            codigo="MT-03",
            verifica="cobertura de catálogo de checklist em qualquer versão configurada",
            falta=f"`{SIMBOLO_DO_CATALOGO}` em `{MODULO_DO_CATALOGO}`"
            + (f" e o seed `{SEED_DO_CATALOGO}`" if seed_ausente else ""),
            requisitos="R73.3, R92.2, R92.7",
            orfaos=itens,
            rotulo_dos_orfaos="item(ns) do catálogo sem entrada na implementação",
            observacoes=[
                "A segunda metade da verificação — para toda `VersaoDeChecklist` ativa, todo "
                "item aplicável ao escopo resolvido tem resultado registrado — depende de "
                "`resolver_checklist` e de `execucoes_de_checklist`, que também não existem.",
            ],
        )
