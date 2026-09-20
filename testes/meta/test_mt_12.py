"""`MT-12` — cobertura das quarenta perguntas de fechamento.

**O que verifica** (`R126.41`, `R126.42`, `P22.12`, `D101`): cada um dos critérios `R126.1` a
`R126.40` — as quarenta perguntas de fechamento arquitetural — possui **requisito numerado** que o
satisfaça, e todo identificador citado existe: requisito no intervalo de 1 a 126, com o critério
existente naquele requisito, e princípio inviolável `SAFE-*` declarado.

**Como falha**: pergunta órfã, nomeada pela falha; ou identificador citado inexistente, nomeando a
pergunta e o identificador.

`MT-12` é o único meta-teste cuja falha significa que a **especificação não está fechada**
(`R126.42`), e por isso entra na sequência de validação anterior ao congelamento junto com `MT-06`
e a suíte de regressão (`D104`). Tem sujeito inteiramente na especificação e **passa** hoje.
"""

from __future__ import annotations

import re

from testes.meta.apoio import (
    amostra,
    criterios_por_requisito,
    secao,
    texto_do_requirements,
)

TITULO_DE_R126 = "### Requirement 126: Portão de congelamento arquitetural"
TITULO_DOS_INVIOLAVEIS = "### Princípios invioláveis (regras de segurança do domínio)"
TOTAL_DE_PERGUNTAS = 40
TOTAL_DE_REQUISITOS = 126


def _perguntas_de_fechamento() -> dict[int, str]:
    """Critérios numerados de `R126`, na ordem em que o requisito os declara."""
    trecho = secao(texto_do_requirements(), TITULO_DE_R126, nivel="---")
    perguntas: dict[int, str] = {}
    for linha in trecho.splitlines():
        item = re.match(r"^(\d+)\.\s+(.*)$", linha)
        if item:
            perguntas[int(item.group(1))] = item.group(2)
    return perguntas


def _principios_inviolaveis() -> set[str]:
    trecho = secao(texto_do_requirements(), TITULO_DOS_INVIOLAVEIS, nivel="### ")
    return set(re.findall(r"\|\s*(SAFE-\d{3})\s*\|", trecho))


def test_mt_12_as_quarenta_perguntas_de_fechamento_estao_declaradas() -> None:
    perguntas = _perguntas_de_fechamento()
    ausentes = [numero for numero in range(1, TOTAL_DE_PERGUNTAS + 1) if numero not in perguntas]
    assert not ausentes, (
        f"MT-12 — pergunta de fechamento ausente de `R126`: "
        f"{[f'R126.{numero}' for numero in ausentes]}"
    )


def test_mt_12_cada_pergunta_possui_requisito_numerado_que_a_satisfaz() -> None:
    perguntas = _perguntas_de_fechamento()
    orfas = [
        f"R126.{numero}: {perguntas.get(numero, '(ausente)')[:90]}"
        for numero in range(1, TOTAL_DE_PERGUNTAS + 1)
        if not re.search(r"`R\d+\.\d+`", perguntas.get(numero, ""))
    ]
    assert not orfas, (
        "MT-12 — pergunta de fechamento sem requisito numerado que a satisfaça. A especificação "
        f"**não está fechada** (`R126.42`):\n{chr(10).join(orfas)}"
    )


def test_mt_12_todo_identificador_citado_nas_perguntas_existe() -> None:
    perguntas = _perguntas_de_fechamento()
    criterios = criterios_por_requisito(texto_do_requirements())
    inviolaveis = _principios_inviolaveis()

    inexistentes: list[str] = []
    for numero in range(1, TOTAL_DE_PERGUNTAS + 1):
        texto = perguntas.get(numero, "")
        for requisito, criterio in re.findall(r"`R(\d+)\.(\d+)`", texto):
            if not 1 <= int(requisito) <= TOTAL_DE_REQUISITOS:
                inexistentes.append(f"R126.{numero} cita R{requisito}.{criterio} (fora de 1 a 126)")
            elif int(criterio) not in criterios.get(int(requisito), set()):
                inexistentes.append(
                    f"R126.{numero} cita R{requisito}.{criterio} (critério inexistente)"
                )
        for principio in re.findall(r"`(SAFE-\d{3})`", texto):
            if principio not in inviolaveis:
                inexistentes.append(f"R126.{numero} cita {principio} (princípio não declarado)")

    assert not inexistentes, (
        f"MT-12 — identificador citado por pergunta de fechamento e inexistente: "
        f"{amostra(inexistentes)}"
    )
