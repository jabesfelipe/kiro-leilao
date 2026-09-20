"""Contrato da estratégia de captura — componente 37 (`R107.4` a `R107.11`, `D94`).

**Homonímia deliberada, e resolvida por módulo.** `EstrategiaDeCaptura` nomeia duas coisas em
`D103`, e as duas mantêm esse nome único:

- o **enum** de quatro valores, em `radar.nucleo.enumeracoes_de_infraestrutura` — o *valor* que a
  Execução do Radar e a captura registram (`R106.1`, `R106.8`);
- o **contrato** declarado aqui — o *adaptador* que obtém a página, com página pública, endpoint,
  arquivo e varredura como implementações (`R107.4`, `R119.2`).

Nenhum dos dois é renomeado, porque sinônimo para termo já nomeado é defeito de redação e `MT-11`
falha nele. A desambiguação é o caminho do módulo: quem precisa do valor importa de
`enumeracoes_de_infraestrutura`; quem precisa do contrato importa de `radar.nucleo.contratos`.
Este módulo **não** importa o enum e **não** o redeclara. A ponte entre os dois é o atributo
`valor`, cujos quatro literais — exatamente os declarados pelo design para este `Protocol` —
correspondem um a um aos quatro valores do enum.

A estratégia **continua invisível ao domínio**: aparece apenas na Execução do Radar e na captura, e
nenhuma entidade de negócio, regra, parâmetro de negócio ou motor a conhece (`R85.3`, `R106.8`,
`P20.4`). Payload igual obtido por estratégias diferentes produz resultado idêntico (`P17.20`).

Camada de núcleo: declaração pura, sem cliente de rede e sem entrada e saída de dados (`MT-10`).
"""

from __future__ import annotations

from typing import Literal, Protocol

from radar.nucleo.contratos.tipos_dos_contratos import (
    CursorDeCaptura,
    PaginaDeCaptura,
    PontoDeRetomada,
)

__all__ = ["EstrategiaDeCaptura"]


class EstrategiaDeCaptura(Protocol):
    """Contrato do **adaptador** de captura, com quatro valores (`R107.4` a `R107.11`, `D94`).

    Aplica limite de tempo `AQ-004`, política de retry `AQ-005`, limite de taxa `AQ-003`, paginação
    com limite `AQ-006` e limite de itens `AQ-007` (`P20.10`). Registra ponto de retomada a cada
    `AQ-012` e retoma do último ponto registrado (`R107.5`, `P20.8`).

    Disjuntor: `AQ-008` falhas consecutivas abrem o disjuntor, interrompem as chamadas àquela
    fonte, registram a abertura com data, hora e causa, e a retomada só ocorre após `AQ-009`
    (`R107.7`, `P20.9`, `REG-060`).

    Pós-condição: cada campo essencial obtido é validado contra a estrutura declarada da fonte;
    **nenhuma** dependência de seletor de página sem validação (`R107.11`). Mudança de estrutura
    além de `AQ-011` registra o erro catalogado `FONTE_ALTERADA`, notifica conforme `R121.1` e
    **não** registra a mudança como ausência de oferta (`R107.3`, `P20.6`, `REG-045`).
    """

    valor: Literal["pagina_publica", "endpoint", "arquivo", "varredura"]

    def obter_pagina(self, cursor: CursorDeCaptura) -> PaginaDeCaptura:
        """Obtém uma página da fonte a partir do cursor, sob os limites de `AQ`."""
        ...

    def ponto_de_retomada(self) -> PontoDeRetomada:
        """Último ponto de retomada registrado (`R107.5`)."""
        ...
