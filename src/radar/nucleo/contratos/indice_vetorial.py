"""Contrato do índice vetorial — componente 32 (`R102`).

O índice vetorial é **artefato derivado e reconstruível**, nunca fonte de verdade do domínio
(`R102.1`). A verdade transacional vive em persistência relacional (`R102.10`), e o arquivo
original, a extração e os segmentos vivem em persistência independente do índice (`R102.2`).

Camada de núcleo: declaração pura, sem implementação e sem import de cliente de índice — a
implementação da primeira versão é pgvector, do lado dos adaptadores (`R119.2`, `MT-10`).
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from radar.nucleo.contratos.tipos_dos_contratos import (
    ColecaoDoIndiceVetorial,
    NomeDeColecao,
    RepresentacaoVetorial,
    TrechoRecuperado,
)

__all__ = ["IndiceVetorial"]


class IndiceVetorial(Protocol):
    """Contrato de indexação, busca e reconstrução (`R102`). Quatro operações.

    Pré-condição: o arquivo original está preservado e íntegro (`R86.2`); a coleção de destino
    está declarada.

    Pós-condição: reindexar a partir do arquivo original **não altera** conteúdo nem hash do
    original (`R102.3`, `P19.13`); reconstruir com o mesmo modelo e a mesma segmentação preserva
    decisão, camada determinante, resultados determinísticos, versões de análise e evidências
    (`R102.7`, `P19.12`, `REG-050`).

    Índice indisponível executa a análise **sem** a etapa de recuperação, marca a etapa como não
    executada, registra pendência quando o checklist aplicável a exigia e **não altera por isso o
    resultado determinístico** (`R102.8`, `P19.14`).
    """

    def indexar(
        self, representacoes: Sequence[RepresentacaoVetorial], colecao: NomeDeColecao
    ) -> None:
        """Indexa representações vetoriais numa das três coleções de `R101.10`."""
        ...

    def buscar(
        self, vetor: Sequence[float], colecao: NomeDeColecao, limite: int
    ) -> Sequence[TrechoRecuperado]:
        """Busca por similaridade, com limite explícito de trechos (`IA-010`)."""
        ...

    def reconstruir(self, colecao: NomeDeColecao) -> ColecaoDoIndiceVetorial:
        """Reconstrói a coleção a partir dos segmentos preservados (`R102.1`, `R102.7`)."""
        ...

    def declarar_colecao(self, colecao: NomeDeColecao) -> ColecaoDoIndiceVetorial:
        """Provedor, modelo, dimensões, versão, segmentação e data de construção (`R102.9`).

        Sem esses atributos, reindexar é adivinhação.
        """
        ...
