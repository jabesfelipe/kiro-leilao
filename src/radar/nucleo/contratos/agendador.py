"""Contrato do agendador — componente 40 (`R110`).

Cron local, agendador de nuvem ou processo assíncrono mantêm a mesma configuração e o mesmo
registro de Execução do Radar (`R110.4`). O domínio não é acoplado ao mecanismo de agendamento: o
disparo é operação do `Motor_do_Radar` (`R110.3`).

Camada de núcleo: declaração pura, sem import de cliente de agendamento (`R119.3`, `MT-10`).
"""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from radar.nucleo.contratos.tipos_dos_contratos import (
    Coincidencia,
    ConfiguracaoDeAgendamento,
    ExecucaoDoRadar,
)

__all__ = ["Agendador"]


class Agendador(Protocol):
    """Contrato de agendamento e de disparo (`R110`). Duas operações.

    Pré-condição: a configuração de agendamento está ativa e resolvida, com os dez atributos de
    `R110.2`.

    Pós-condição: execução agendada que coincide com execução em curso da mesma fonte **não
    inicia**, e a coincidência é registrada (`R110.5`, `P20.17`) — é o que o segundo membro do
    retorno de `disparar` declara na assinatura, em lugar de deixá-lo implícito num valor nulo.

    Proibição: alteração de agendamento e de limites operacionais é restrita ao papel Operador de
    Plataforma, que não altera regra, parâmetro de negócio, evidência, análise nem decisão
    (`R110.9`), e vai para a trilha de auditoria (`R110.10`).
    """

    def agendar(self, configuracao: ConfiguracaoDeAgendamento) -> None:
        """Registra o agendamento da fonte conforme `AQ-001` e `AQ-002` (`R110.2`)."""
        ...

    def disparar(self, fonte_id: UUID) -> ExecucaoDoRadar | Coincidencia:
        """Dispara o ciclo da fonte, ou registra a coincidência sem iniciar (`R110.5`)."""
        ...
