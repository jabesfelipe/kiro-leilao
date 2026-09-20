"""Identificador de correlação: o fio que liga uma execução inteira.

`R111.1` — toda execução relevante nasce com um identificador de correlação atribuído e o
propaga a **todos** os registros daquela execução; `R111.3` enumera as treze espécies de
execução relevante que o exigem, da captura ao envio de notificação. O nome canônico é
`IdentificadorDeCorrelacao` (`D103`), e é o **único** nome do termo no projeto: `MT-11`
reprova sinônimo.

Ele entra no passo 1 de `D91` por decisão de ordem, não por conveniência: é **coluna em toda
entidade**, e acrescentá-lo depois das entidades gravadas é migração, não ajuste (`D96`).

Camada de núcleo: valor imutável e congelado, sem entrada e saída de dados e sem cliente
externo (`R119.3`, `MT-10`). A geração de um identificador novo acontece na **borda de
entrada** — uma única vez por execução, em `novo` —, e o caminho de execução daí em diante
apenas **propaga** o valor recebido, com `propagar`. Nenhum ponto interno inventa um
identificador próprio: identificador trocado no meio do caminho quebra a correlação que
`R111.6` e `R111.7` exigem na hora do erro.

Ausência de correlação não é representada por valor neutro: o identificador nulo — `UUID` com
todos os dígitos em zero — é recusado na construção, para que "sem correlação" nunca circule
disfarçado de correlação (SAFE-003).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final
from uuid import UUID, uuid4

__all__ = [
    "NOME_DO_CAMPO_DE_CORRELACAO",
    "IdentificadorDeCorrelacao",
    "propagar",
]

#: Nome do campo sob o qual a correlação é registrada no log estruturado consultável por campo
#: (`R111.2`, `R111.4`) e na coluna presente em toda entidade (`D96`). Vive aqui para que exista
#: um único lugar onde o nome pode estar errado.
NOME_DO_CAMPO_DE_CORRELACAO: Final[str] = "identificador_de_correlacao"

_IDENTIFICADOR_NULO: Final[UUID] = UUID(int=0)


@dataclass(frozen=True, slots=True)
class IdentificadorDeCorrelacao:
    """Valor que liga todos os registros de uma mesma execução: requisição, log, métrica e erro.

    Congelado e sem comportamento de mutação: o identificador atravessa o caminho de execução
    inteiro sem ser recalculado. A igualdade é a do valor, de modo que dois registros da mesma
    execução se reconhecem como tal.
    """

    valor: UUID

    def __post_init__(self) -> None:
        if not isinstance(self.valor, UUID):
            raise TypeError(
                "identificador de correlação exige UUID; "
                f"recebido {type(self.valor).__name__}"
            )
        if self.valor == _IDENTIFICADOR_NULO:
            raise ValueError(
                "identificador de correlação nulo não representa ausência de correlação; "
                "atribua um identificador na borda de entrada"
            )

    @classmethod
    def novo(cls) -> IdentificadorDeCorrelacao:
        """Atribui um identificador novo. Chamado **uma vez por execução**, na borda de entrada.

        É o único ponto não determinístico do módulo, e está isolado neste construtor de
        propósito: o restante do caminho de execução usa `propagar`, nunca este método.
        """
        return cls(valor=uuid4())

    @classmethod
    def de_texto(cls, texto: str) -> IdentificadorDeCorrelacao:
        """Interpreta a correlação recebida de fora do processo — cabeçalho, mensagem, registro.

        Texto em branco ou fora da forma de `UUID` é recusado: correlação ilegível não é
        substituída silenciosamente por uma nova, porque isso romperia a ligação com a
        execução de origem.
        """
        if not texto.strip():
            raise ValueError(
                "identificador de correlação em branco não é correlação; "
                "propague o identificador da execução de origem"
            )
        try:
            return cls(valor=UUID(texto.strip()))
        except ValueError as erro:
            raise ValueError(
                f"identificador de correlação fora da forma de UUID: {texto!r}"
            ) from erro

    @property
    def texto(self) -> str:
        """Forma canônica para log estruturado, resposta de erro e coluna persistida."""
        return str(self.valor)

    def __str__(self) -> str:
        return self.texto


def propagar(
    correlacao: IdentificadorDeCorrelacao | None,
) -> IdentificadorDeCorrelacao:
    """Reaproveita a correlação recebida; atribui uma nova só quando a execução nasce aqui.

    É a operação que o caminho de execução usa: recebeu correlação, mantém a mesma; não
    recebeu, está na borda de entrada e atribui (`R111.1`). Assim, uma execução aninhada
    permanece ligada à execução que a disparou em lugar de abrir um fio novo.
    """
    if correlacao is None:
        return IdentificadorDeCorrelacao.novo()
    return correlacao
