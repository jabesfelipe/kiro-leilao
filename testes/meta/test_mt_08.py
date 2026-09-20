"""`MT-08` — soma de pesos.

**O que verifica** (`R40.3`, `R49.5`, `R51.1`, `D101`): `SCORE-001`, as **cinco colunas** de
`SCORE-002`, os **sete** componentes de `SCORE-006` e os **sete** pesos de `R40.3` somam
**1,00**; `SCORE-005` soma **100**. A verificação vale para os cinco conjuntos da especificação e
para as constantes Python que os realizam — `PESOS_DE_OPORTUNIDADE`, `PESOS_POR_ESTRATEGIA`,
`PESOS_DE_ADERENCIA`, `PESOS_DO_ESCORE_ECONOMICO` e `PESOS_DE_LIQUIDEZ`.

**Como falha**: qualquer conjunto fora da soma, nomeando o conjunto e a soma encontrada; ou
conjunto sem constante correspondente na implementação.

**Estado hoje**: falha por conteúdo ausente. Os cinco conjuntos da especificação somam o
declarado e isso é conferido aqui em aritmética exata — `Decimal`, nunca ponto flutuante —; as
constantes Python ainda não existem.
"""

from __future__ import annotations

import re
from decimal import Decimal

from testes.meta.apoio import (
    falhar_por_conteudo_ausente,
    simbolo_opcional,
    tabela_apos,
    texto_do_requirements,
)

MARCADOR_DE_SCORE_001 = "**`SCORE-001` — Pesos mestres do Opportunity Score**"
MARCADOR_DE_SCORE_002 = "**`SCORE-002` — Pesos por estratégia (overrides)**"
MARCADOR_DE_SCORE_005 = "**`SCORE-005` — Score econômico (indicador informativo)**"
MARCADOR_DE_SCORE_006 = "**`SCORE-006` — Pesos do Investor Fit Score**"

COLUNAS_DE_SCORE_002 = ("revenda", "renda", "valorizacao", "mcmv", "terreno")

UM = Decimal("1.00")
CEM = Decimal("100")

#: Conjunto de pesos → constante Python declarada pelo design e o módulo que a hospeda.
CONSTANTES_ESPERADAS: dict[str, tuple[str, str]] = {
    "SCORE-001": ("radar.motores.escore", "PESOS_DE_OPORTUNIDADE"),
    "SCORE-002": ("radar.motores.escore", "PESOS_POR_ESTRATEGIA"),
    "SCORE-005": ("radar.motores.escore", "PESOS_DO_ESCORE_ECONOMICO"),
    "SCORE-006": ("radar.motores.escore", "PESOS_DE_ADERENCIA"),
    "R40.3": ("radar.motores.liquidez", "PESOS_DE_LIQUIDEZ"),
}


def _coluna_de_pesos(marcador: str, coluna: int) -> list[Decimal]:
    """Pesos de uma coluna da tabela, descartando a linha de total."""
    pesos: list[Decimal] = []
    for celulas in tabela_apos(texto_do_requirements(), marcador):
        if not celulas[0].startswith("`"):
            continue
        pesos.append(Decimal(celulas[coluna].replace(",", ".")))
    return pesos


def _pesos_de_liquidez() -> list[Decimal]:
    """Os sete pesos de `R40.3`, declarados em prosa no critério de aceitação."""
    criterio = re.search(
        r"^3\. THE Motor_de_Liquidez SHALL compor o score de liquidez(.+)$",
        texto_do_requirements(),
        re.MULTILINE,
    )
    assert criterio is not None, "MT-08 — critério `R40.3` não encontrado no requirements"
    return [
        Decimal(valor.replace(",", "."))
        for valor in re.findall(r"peso (\d,\d+)", criterio.group(1))
    ]


def _conjuntos_da_especificacao() -> dict[str, tuple[list[Decimal], Decimal, int]]:
    """Conjunto → (pesos, soma esperada, quantidade esperada de componentes)."""
    conjuntos: dict[str, tuple[list[Decimal], Decimal, int]] = {
        "SCORE-001": (_coluna_de_pesos(MARCADOR_DE_SCORE_001, 1), UM, 8),
        "SCORE-005": (_coluna_de_pesos(MARCADOR_DE_SCORE_005, 1), CEM, 7),
        "SCORE-006": (_coluna_de_pesos(MARCADOR_DE_SCORE_006, 1), UM, 7),
        "R40.3": (_pesos_de_liquidez(), UM, 7),
    }
    for indice, estrategia in enumerate(COLUNAS_DE_SCORE_002, start=1):
        conjuntos[f"SCORE-002/{estrategia}"] = (
            _coluna_de_pesos(MARCADOR_DE_SCORE_002, indice),
            UM,
            8,
        )
    return conjuntos


def test_mt_08_os_conjuntos_de_pesos_da_especificacao_fecham_a_soma() -> None:
    fora_da_soma: list[str] = []
    contagem_errada: list[str] = []
    for nome, (pesos, soma_esperada, quantidade) in _conjuntos_da_especificacao().items():
        if sum(pesos) != soma_esperada:
            fora_da_soma.append(f"{nome} soma {sum(pesos)}, esperado {soma_esperada}")
        if len(pesos) != quantidade:
            contagem_errada.append(f"{nome} tem {len(pesos)} componentes, esperado {quantidade}")

    assert not fora_da_soma, f"MT-08 — conjunto de pesos fora da soma: {fora_da_soma}"
    assert not contagem_errada, (
        f"MT-08 — conjunto de pesos com componentes a mais ou a menos: {contagem_errada}"
    )


def test_mt_08_todo_conjunto_de_pesos_tem_constante_na_implementacao() -> None:
    ausentes = [
        f"{conjunto} → `{simbolo}` em `{modulo}`"
        for conjunto, (modulo, simbolo) in CONSTANTES_ESPERADAS.items()
        if simbolo_opcional(modulo, simbolo) is None
    ]
    if ausentes:
        falhar_por_conteudo_ausente(
            codigo="MT-08",
            verifica="`SCORE-001`, as cinco colunas de `SCORE-002`, os sete de `SCORE-006` e os "
            "sete de `R40.3` somam 1,00; `SCORE-005` soma 100",
            falta="as constantes Python de pesos que realizam os conjuntos da especificação",
            requisitos="R40.3, R49.5, R51.1, R73.10",
            orfaos=ausentes,
            rotulo_dos_orfaos="conjunto(s) de pesos sem constante correspondente",
            observacoes=[
                "Os conjuntos da especificação já fecham a soma; o que falta é a representação "
                "executável sobre a qual a soma passa a ser verificada a cada mudança.",
            ],
        )
