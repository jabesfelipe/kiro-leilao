"""`MT-04` — cobertura das 55 regras do Anexo D.

**O que verifica** (`R54.1`, `R73.4`, `D101`): todo `RULE-*` do Anexo D — Matriz Canônica de
Regras, **55** regras — está declarado em `CATALOGO_DE_REGRAS`, e o catálogo não tem regra que o
anexo não declare.

**Como falha**: regra ausente do catálogo ou sobrando nele, nomeando o código em cada caso.

**Estado hoje**: falha por conteúdo ausente. As 55 regras existem no anexo e são conferidas aqui,
inclusive a contagem e a ausência de lacuna por família; `CATALOGO_DE_REGRAS`, declarado pelo
design em `radar/regras/catalogo.py`, ainda não existe.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping

from testes.meta.apoio import (
    falhar_por_conteudo_ausente,
    identificadores,
    secao,
    simbolo_opcional,
    texto_do_requirements,
)

TITULO_DO_ANEXO_D = "## Anexo D — Matriz Canônica de Regras (55 regras, normativo)"
TOTAL_DE_REGRAS = 55
MODULO_DO_CATALOGO = "radar.regras.catalogo"
SIMBOLO_DO_CATALOGO = "CATALOGO_DE_REGRAS"


def _regras_do_anexo_d() -> list[str]:
    return identificadores(secao(texto_do_requirements(), TITULO_DO_ANEXO_D), r"RULE-[A-Z]+-\d{3}")


def test_mt_04_o_anexo_d_declara_55_regras_sem_repeticao_nem_lacuna() -> None:
    regras = _regras_do_anexo_d()
    repetidas = sorted({codigo for codigo, vezes in Counter(regras).items() if vezes > 1})
    assert not repetidas, f"MT-04 — regra repetida no Anexo D: {repetidas}"
    assert len(regras) == TOTAL_DE_REGRAS, (
        f"MT-04 — o Anexo D declara {TOTAL_DE_REGRAS} regras; encontradas {len(regras)}"
    )

    por_familia: dict[str, list[int]] = {}
    for codigo in regras:
        familia, numero = codigo.rsplit("-", 1)
        por_familia.setdefault(familia, []).append(int(numero))
    com_lacuna = {
        familia: numeros
        for familia, numeros in por_familia.items()
        if sorted(numeros) != list(range(1, len(numeros) + 1))
    }
    assert not com_lacuna, (
        f"MT-04 — numeração descontínua dentro da família de regras: {com_lacuna}"
    )


def test_mt_04_toda_regra_do_anexo_d_esta_no_catalogo() -> None:
    regras = _regras_do_anexo_d()
    catalogo = simbolo_opcional(MODULO_DO_CATALOGO, SIMBOLO_DO_CATALOGO)

    if catalogo is None:
        falhar_por_conteudo_ausente(
            codigo="MT-04",
            verifica=f"as {TOTAL_DE_REGRAS} regras do Anexo D estão em `{SIMBOLO_DO_CATALOGO}`",
            falta=f"`{SIMBOLO_DO_CATALOGO}` em `{MODULO_DO_CATALOGO}`",
            requisitos="R54.1, R73.4",
            orfaos=regras,
            rotulo_dos_orfaos="regra(s) do Anexo D sem declaração no catálogo",
        )

    assert isinstance(catalogo, Mapping), (
        f"MT-04 — `{SIMBOLO_DO_CATALOGO}` é declarado como mapa de código de regra para "
        f"especificação; encontrado {type(catalogo).__name__}"
    )
    codigos_do_catalogo = {str(codigo) for codigo in catalogo}
    ausentes = sorted(set(regras) - codigos_do_catalogo)
    sobrando = sorted(codigos_do_catalogo - set(regras))
    assert not ausentes and not sobrando, (
        f"MT-04 — regra ausente do catálogo: {ausentes}; regra sobrando no catálogo: {sobrando}"
    )
