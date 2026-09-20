"""`MT-06` — cobertura de prioridade dos 126 requisitos.

**O que verifica** (`R73.10`, `R75.5`, `D89`, `D102`): os **126** requisitos têm exatamente uma
prioridade atribuída no Índice de Requisitos, com as contagens **112 `P0`**, **13 `P1`** e
**1 `P2`**; os treze `P1` são exatamente `R5`, `R31`, `R42`, `R43`, `R48`, `R59`, `R60`, `R65`,
`R69`, `R80`, `R81`, `R117` e `R121`, e o único `P2` é `R72`; e o resumo declarado ao fim do
índice coincide com a tabulação linha a linha — onde divergirem, prevalece a tabulação (`D89`).

**Como falha**: requisito sem prioridade, nomeando o número; requisito com duas linhas no índice;
contagem divergente; ou resumo em desacordo com a tabulação.

Este meta-teste tem sujeito **inteiramente na especificação** e **passa** hoje. Ele entra na
sequência de validação anterior ao congelamento junto com `MT-12` e a suíte de regressão (`D104`).
"""

from __future__ import annotations

import re
from collections import Counter

from testes.meta.apoio import amostra, secao, texto_do_requirements

TITULO_DO_INDICE = "## Índice de Requisitos e Prioridade"
TOTAL_DE_REQUISITOS = 126
CONTAGEM_DECLARADA = {"P0": 112, "P1": 13, "P2": 1}
REQUISITOS_P1 = (5, 31, 42, 43, 48, 59, 60, 65, 69, 80, 81, 117, 121)
REQUISITO_P2 = 72


def _prioridade_por_requisito() -> list[tuple[int, str]]:
    """Pares (número do requisito, prioridade) tabulados linha a linha no índice."""
    indice = secao(texto_do_requirements(), TITULO_DO_INDICE)
    linhas = re.findall(r"^\|\s*(\d{1,3})\s*\|[^|]*\|[^|]*\|\s*(P\d)\s*\|", indice, re.MULTILINE)
    return [(int(numero), prioridade) for numero, prioridade in linhas]


def test_mt_06_todo_requisito_tem_exatamente_uma_prioridade() -> None:
    tabulacao = _prioridade_por_requisito()
    vezes = Counter(numero for numero, _ in tabulacao)

    repetidos = sorted(numero for numero, quantidade in vezes.items() if quantidade > 1)
    assert not repetidos, (
        f"MT-06 — requisito com mais de uma linha no Índice de Requisitos: {repetidos}"
    )

    sem_prioridade = sorted(set(range(1, TOTAL_DE_REQUISITOS + 1)) - set(vezes))
    assert not sem_prioridade, (
        f"MT-06 — requisito sem prioridade atribuída no Índice de Requisitos: "
        f"{amostra([f'R{numero}' for numero in sem_prioridade])}"
    )

    fora_do_intervalo = sorted(numero for numero in vezes if numero > TOTAL_DE_REQUISITOS)
    assert not fora_do_intervalo, (
        f"MT-06 — linha do índice fora do intervalo de 1 a {TOTAL_DE_REQUISITOS}: "
        f"{fora_do_intervalo}"
    )


def test_mt_06_as_contagens_por_prioridade_batem_com_a_tabulacao() -> None:
    tabulacao = _prioridade_por_requisito()
    apuradas = Counter(prioridade for _, prioridade in tabulacao)

    assert dict(apuradas) == CONTAGEM_DECLARADA, (
        f"MT-06 — contagem divergente. Declarado {CONTAGEM_DECLARADA}, "
        f"tabulado {dict(apuradas)}"
    )

    p1 = tuple(sorted(numero for numero, prioridade in tabulacao if prioridade == "P1"))
    p2 = tuple(sorted(numero for numero, prioridade in tabulacao if prioridade == "P2"))
    assert p1 == REQUISITOS_P1, (
        f"MT-06 — os treze requisitos `P1` são {REQUISITOS_P1}; tabulados {p1}"
    )
    assert p2 == (REQUISITO_P2,), (
        f"MT-06 — o único requisito `P2` é R{REQUISITO_P2}; tabulados {p2}"
    )


def test_mt_06_o_resumo_declarado_coincide_com_a_tabulacao() -> None:
    indice = secao(texto_do_requirements(), TITULO_DO_INDICE)
    resumo = re.search(
        r"Contagem:\s*\*\*(\d+)\s+requisitos?\s+`P0`\*\*,\s*\*\*(\d+)\s+requisitos?\s+`P1`\*\*,"
        r"\s*\*\*(\d+)\s+requisitos?\s+`P2`\*\*",
        indice,
    )
    assert resumo is not None, (
        "MT-06 — o Índice de Requisitos declara o resumo de contagem por prioridade; "
        "resumo não encontrado"
    )

    declarado = {
        "P0": int(resumo.group(1)),
        "P1": int(resumo.group(2)),
        "P2": int(resumo.group(3)),
    }
    apurado = dict(Counter(prioridade for _, prioridade in _prioridade_por_requisito()))
    assert declarado == apurado, (
        f"MT-06 — resumo em desacordo com a tabulação. Resumo {declarado}, tabulação {apurado}. "
        "Prevalece a tabulação (`D89`), e o resumo é que deve ser corrigido."
    )
    assert declarado == CONTAGEM_DECLARADA, (
        f"MT-06 — resumo em desacordo com as contagens de `D102`: {declarado}"
    )
