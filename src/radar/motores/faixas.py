"""Classificação por faixa contínua — o ponto único de correção de `D.1.5`.

O defeito `D.1.5` nasceu de faixas escritas como intervalos fechados de inteiros
(`if 80 <= v <= 89`): `89,5` não pertencia a faixa alguma, e a classificação deixava de
ser uma função total. A correção é um classificador **único**, por **limite inferior**,
com comparação `>=` e avaliação em **ordem decrescente** de limite: a primeira faixa
satisfeita vence. Assim a cobertura sobre `[0, 100]` é total *por construção* — não
existe valor sem faixa, inteiro ou fracionário, e faixas adjacentes não se sobrepõem.

Toda faixa do produto passa por aqui: liquidez (`R40.2`), escore (`R49.6`, `SCORE-003`),
fator de confiança (`CONF-007`, `R50.3`, `R50.4`), nível nomeado de confiança
(`CONF-010`), aderência (`R44.4`), impacto de prazo (`R41.3`) e margem adicional por
prazo (`LIQ-010`). Cada motor declara a **tabela** da sua faixa com `construir_faixas` e
consulta com `classificar_por_faixa`; nenhum deles reimplementa a comparação. Um único
ponto de correção para `D.1.5` e um único ponto de verificação para `P9.1`, `P10.14`,
`P10.15` e `P11.15`.

Duas regras sustentam a totalidade e ambas falham alto, nunca em silêncio:

- **Domínio fechado.** Valor fora de `[0, 100]` é erro explícito. Nunca é saturado para o
  limite mais próximo: saturar transformaria dado corrompido em classe plausível.
- **Tabela defeituosa falha na declaração.** Ordem inconsistente, limites sobrepostos ou
  ausência de cobertura do limite inferior são defeito da tabela. `construir_faixas`
  rejeita no import do módulo que declara a tabela, antes de qualquer consulta.

Camada de núcleo (`R119.1`): função pura, sem entrada e saída de dados.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Final

__all__ = [
    "LIMITE_INFERIOR_DA_ESCALA",
    "LIMITE_SUPERIOR_DA_ESCALA",
    "TabelaDeFaixas",
    "classificar_por_faixa",
    "construir_faixas",
]

LIMITE_INFERIOR_DA_ESCALA: Final[Decimal] = Decimal(0)
"""Limite inferior do domínio das escalas de 0 a 100 (`R40.1`, `R49.1`, `R50.1`)."""

LIMITE_SUPERIOR_DA_ESCALA: Final[Decimal] = Decimal(100)
"""Limite superior do domínio das escalas de 0 a 100 (`R40.1`, `R49.1`, `R50.1`)."""


type TabelaDeFaixas[T] = tuple[tuple[Decimal, T], ...]
"""Tabela de faixas validada: pares `(limite inferior, classe)` em ordem decrescente.

Construída exclusivamente por `construir_faixas`, que é quem garante ordem estrita,
ausência de sobreposição e cobertura de todo o domínio.
"""


def _rejeitar_float(valor: object, campo: str) -> None:
    """`float` não atravessa a fronteira do núcleo: o caminho numérico é `Decimal`."""
    if isinstance(valor, float):
        raise TypeError(f"{campo} não aceita float; use Decimal")


def _exigir_decimal_finito(valor: object, campo: str) -> Decimal:
    """Garante `Decimal` finito. `NaN` não é comparável e não classifica nada."""
    _rejeitar_float(valor, campo)
    if not isinstance(valor, Decimal):
        raise TypeError(f"{campo} exige Decimal (recebido {type(valor).__name__})")
    if not valor.is_finite():
        raise ValueError(f"{campo} exige valor finito (recebido {valor})")
    return valor


def _exigir_na_escala(valor: Decimal, campo: str) -> None:
    """Domínio fechado em `[0, 100]`: fora dele é erro, nunca saturação silenciosa."""
    if not LIMITE_INFERIOR_DA_ESCALA <= valor <= LIMITE_SUPERIOR_DA_ESCALA:
        raise ValueError(
            f"{campo} fora da escala {LIMITE_INFERIOR_DA_ESCALA}-"
            f"{LIMITE_SUPERIOR_DA_ESCALA}: {valor}"
        )


def construir_faixas[T](*faixas: tuple[Decimal, T]) -> TabelaDeFaixas[T]:
    """Valida e congela uma tabela de faixas por limite inferior.

    Recebe os pares `(limite inferior, classe)` em ordem **decrescente** de limite e
    rejeita, na construção, toda tabela que não possa classificar `[0, 100]` inteiro:

    - tabela vazia, que não classificaria valor algum;
    - limite que não seja `Decimal` finito dentro de `[0, 100]`;
    - limites que não sejam **estritamente** decrescentes — o que cobre ao mesmo tempo a
      ordem inconsistente e a sobreposição de faixas, porque limite repetido ou fora de
      ordem torna a classe de um valor dependente da posição na sequência;
    - último limite diferente de `0`, que deixaria um trecho inicial do domínio sem
      faixa.

    Chamada no corpo do módulo que declara a tabela, a validação acontece no import: uma
    tabela defeituosa nunca chega à consulta.
    """
    if not faixas:
        raise ValueError("tabela de faixas vazia não classifica valor algum")

    for indice, (limite, _) in enumerate(faixas):
        campo = f"limite inferior da faixa de índice {indice}"
        _exigir_na_escala(_exigir_decimal_finito(limite, campo), campo)

    for indice in range(len(faixas) - 1):
        limite_atual = faixas[indice][0]
        limite_seguinte = faixas[indice + 1][0]
        if limite_atual <= limite_seguinte:
            raise ValueError(
                "faixas exigem limites inferiores estritamente decrescentes; "
                f"índice {indice} tem {limite_atual} e índice {indice + 1} tem "
                f"{limite_seguinte}"
            )

    ultimo_limite = faixas[-1][0]
    if ultimo_limite != LIMITE_INFERIOR_DA_ESCALA:
        raise ValueError(
            "a última faixa deve ter limite inferior igual a "
            f"{LIMITE_INFERIOR_DA_ESCALA} para cobrir todo o domínio; "
            f"recebido {ultimo_limite}"
        )

    return tuple(faixas)


def classificar_por_faixa[T](valor: Decimal, faixas: TabelaDeFaixas[T]) -> T:
    """Classificação por faixa contínua. Total sobre `[0, 100]`.

    `faixas` vem ordenado por limite inferior **decrescente** e a comparação é `>=`: a
    primeira faixa satisfeita vence. Assim a cobertura é total por construção — não
    existe valor sem faixa, e faixas adjacentes não se sobrepõem. No limite exato o valor
    pertence à faixa superior, que é o que `P9.1`, `P10.14` e `P10.15` verificam junto a
    cada fronteira, e o que faz `89,5` classificar na faixa de `80` em vez de ficar sem
    classe (`D.1.5`).

    Substitui todo teste de faixa escrito como `if 80 <= v <= 89`, que deixava `89,5` sem
    classe. Usado por liquidez (`R40.2`), escore (`SCORE-003`, `R49.6`), fator de
    confiança (`CONF-007`, `R50.3`, `R50.4`), nível nomeado de confiança (`CONF-010`),
    aderência (`R44.4`), impacto de prazo (`R41.3`) e margem adicional por prazo
    (`LIQ-010`).

    Valor fora de `[0, 100]`, `float` ou `Decimal` não finito falha explicitamente:
    escala corrompida não vira classe plausível. A tabela é revalidada aqui com o mesmo
    critério de `construir_faixas`, para que a totalidade não dependa de o chamador ter
    passado pela construção — a tabela canônica passa, e uma tabela improvisada com
    lacuna falha em vez de devolver classe errada.
    """
    _exigir_na_escala(_exigir_decimal_finito(valor, "valor"), "valor")
    tabela = construir_faixas(*faixas)

    for limite, classe in tabela:
        if valor >= limite:
            return classe

    raise AssertionError(  # pragma: no cover - impedido por construir_faixas
        f"tabela validada não classificou {valor}: cobertura de [0, 100] violada"
    )
