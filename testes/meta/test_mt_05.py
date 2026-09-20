"""`MT-05` — cobertura da disciplina de lance.

**O que verifica** (`R73.5`, `R82.1`, `D101`): os **48** itens da disciplina de lance do Anexo C
estão declarados — os nove hard stops `HS-01` a `HS-09` (`C.3`), os doze itens pré-lance `PL-01`
a `PL-12` (`C.4`), as nove verificações de evicção `E01` a `E09` (`C.2`), os doze itens da
revalidação final `RL-01` a `RL-12` (`C.7`) e as seis verificações de histórico do leiloeiro
`HL-01` a `HL-06` (`C.5`).

**Como falha**: item ausente, nomeando o identificador e a tabela de origem.

**Estado hoje**: falha por conteúdo ausente. Os 48 identificadores existem no Anexo C e são
conferidos aqui, grupo por grupo; o motor de disciplina de lance —
`radar/motores/disciplina_de_lance.py`, com o catálogo das verificações — ainda não existe.
"""

from __future__ import annotations

from testes.meta.apoio import (
    falhar_por_conteudo_ausente,
    identificadores,
    secao,
    simbolo_opcional,
    texto_do_requirements,
)

TITULO_DO_ANEXO_C = (
    "## Anexo C — Due Diligence Individual, Hard Stops e Disciplina de Lance (normativo)"
)

#: Grupo → (padrão do identificador, quantidade declarada, tabela de origem).
GRUPOS: dict[str, tuple[str, int, str]] = {
    "HS": (r"HS-\d{2}", 9, "C.3 hard stops de lance"),
    "PL": (r"PL-\d{2}", 12, "C.4 checklist pré-lance"),
    "E": (r"E\d{2}", 9, "C.2 verificações de evicção"),
    "RL": (r"RL-\d{2}", 12, "C.7 revalidação final do dia do lance"),
    "HL": (r"HL-\d{2}", 6, "C.5 histórico do leiloeiro"),
}

TOTAL_DE_ITENS = 48
MODULO_DA_DISCIPLINA = "radar.motores.disciplina_de_lance"
SIMBOLO_DA_DISCIPLINA = "CATALOGO_DE_VERIFICACOES_DE_LANCE"


def _itens_por_grupo() -> dict[str, list[str]]:
    anexo_c = secao(texto_do_requirements(), TITULO_DO_ANEXO_C)
    return {grupo: identificadores(anexo_c, padrao) for grupo, (padrao, _, _) in GRUPOS.items()}


def test_mt_05_o_anexo_c_declara_os_48_itens_da_disciplina_de_lance() -> None:
    encontrados = _itens_por_grupo()
    faltando: list[str] = []
    for grupo, (_, quantidade, tabela) in GRUPOS.items():
        separador = "" if grupo == "E" else "-"
        esperados = [f"{grupo}{separador}{numero:02d}" for numero in range(1, quantidade + 1)]
        ausentes = [item for item in esperados if item not in encontrados[grupo]]
        faltando.extend(f"{item} ({tabela})" for item in ausentes)
    assert not faltando, f"MT-05 — item da disciplina de lance ausente do Anexo C: {faltando}"

    total = sum(len(itens) for itens in encontrados.values())
    assert total == TOTAL_DE_ITENS, (
        f"MT-05 — a disciplina de lance tem {TOTAL_DE_ITENS} itens declarados "
        f"(9 + 12 + 9 + 12 + 6); encontrados {total}"
    )


def test_mt_05_toda_verificacao_de_lance_esta_declarada_na_implementacao() -> None:
    encontrados = _itens_por_grupo()
    itens = [
        f"{item} ({GRUPOS[grupo][2]})" for grupo, lista in encontrados.items() for item in lista
    ]
    catalogo = simbolo_opcional(MODULO_DA_DISCIPLINA, SIMBOLO_DA_DISCIPLINA)

    if catalogo is None:
        falhar_por_conteudo_ausente(
            codigo="MT-05",
            verifica="`HS-01..09`, `PL-01..12`, `E01..09`, `RL-01..12` e `HL-01..06` declarados",
            falta=f"`{SIMBOLO_DA_DISCIPLINA}` em `{MODULO_DA_DISCIPLINA}`",
            requisitos="R73.5, R82.1",
            orfaos=sorted(itens),
            rotulo_dos_orfaos="item(ns) da disciplina de lance sem declaração na implementação",
            observacoes=[
                "A liberação de lance depende dos 48 itens: `PODE_DAR_LANCE` exige os doze "
                "`PL`, nenhum `HS` acionado e o teto respeitado; `LIBERADO_PARA_LANCE` exige "
                "também os doze `RL`.",
            ],
        )
