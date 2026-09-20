"""Contrato único de canal de notificação — componente 48 (`R121.2`, `R121.3`).

O design declara este contrato na tabela de adaptadores de `R119.2` e no diagrama das três camadas
— com o canal local de `PLT-013` e o canal externo `P1` como implementações —, e declara o **dado**
que atravessa a fronteira em `Notificacao` (`R121.2`: destinatário, assunto, conteúdo, prioridade,
data e situação de entrega). A assinatura do canal em si não aparece em bloco de código, e a
operação declarada abaixo é a de `R121.3`: **entregar** a notificação por aquele canal, usando o
mesmo contrato.

A separação de verbos é deliberada e não é sinônimo: o `Gestor_de_Notificacoes` **publica** a
notificação (`R121.1`, componente 48, núcleo) e o canal **entrega** — a situação de entrega de
`R121.2` é justamente o que o canal resolve e o gestor registra.

Camada de núcleo: declaração pura, sem import de cliente de canal externo (`R119.3`, `MT-10`).
"""

from __future__ import annotations

from typing import Protocol

from radar.nucleo.contratos.tipos_dos_contratos import Notificacao

__all__ = ["CanalDeNotificacao"]


class CanalDeNotificacao(Protocol):
    """Contrato **único** de canal (`R121.2`). Uma operação.

    Pré-condição: a notificação existe com destinatário, assunto, conteúdo, prioridade e data, e
    corresponde a um dos dez eventos de `R121.1`.

    Pós-condição: cada notificação emitida é registrada com evento, canal, destinatário, data e
    situação de entrega (`R121.9`, `P21.23`).

    Proibição: a prioridade e o controle de fadiga de alerta são os de `R59`; catálogo de alerta
    paralelo é defeito, não alternativa (`R121.5`). Canal externo habilitado em `PLT-013` usa **o
    mesmo** contrato (`R121.3`), e a entrega externa é capacidade `P1`, com a notificação local
    como comportamento da primeira versão (`R121.4`).
    """

    def entregar(self, notificacao: Notificacao) -> None:
        """Entrega a notificação pelo canal, que registra a situação de entrega."""
        ...
