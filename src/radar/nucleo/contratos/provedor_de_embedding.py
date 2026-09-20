"""Contrato único de geração de representação vetorial — componente 28 (`R98.2`).

O nome é `ProvedorDeEmbedding`, e é o **único** (`D103`, `R98.2`): `EmbeddingProvider`,
`ProvedorDeVetores` e `ProvedorDeRepresentacaoVetorial` são sinônimos proibidos, e `MT-11` falha
neles. `embedding` permanece em inglês por decisão declarada do dicionário de idioma, justamente
porque o identificador canônico é este.

Camada de núcleo: declaração pura, sem implementação, sem entrada e saída de dados e sem import de
cliente de embedding (`R98.5`, `R119.3`, `MT-10`).
"""

from __future__ import annotations

from typing import Protocol

from radar.nucleo.contratos.tipos_dos_contratos import (
    IdentidadeDeEmbedding,
    RepresentacaoVetorial,
    SegmentoDeDocumento,
)

__all__ = ["ProvedorDeEmbedding"]


class ProvedorDeEmbedding(Protocol):
    """Contrato **único** de geração de representação vetorial (`R98.2`). Duas operações.

    Pré-condição: o segmento existe, tem hash calculado e os treze metadados de `R101.2`.

    Pós-condição: a representação vetorial registra provedor, modelo, dimensões, versão e data da
    geração (`R100.3`); o cache de `IA-012` é consultado antes de gerar (`R99.6`).

    A dimensão é atributo da representação vetorial, **nunca** do documento (`R102.6`): é o que
    permite migrar de modelo sem reescrever o documento (`R102.4`).
    """

    def gerar_representacao_vetorial(
        self, segmento: SegmentoDeDocumento
    ) -> RepresentacaoVetorial:
        """Gera a representação vetorial de um segmento já segmentado e com metadados."""
        ...

    def declarar_identidade(self) -> IdentidadeDeEmbedding:
        """Provedor, modelo, dimensões e versão (`R98.2`, `R100.3`)."""
        ...
