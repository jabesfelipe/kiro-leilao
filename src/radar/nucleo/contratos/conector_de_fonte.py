"""Contrato único de aquisição de ofertas — componente 21 (`R85.1`).

O conector é o único ponto do produto que sabe **como** a oferta é obtida. Nada abaixo dele sabe.
A estratégia de aquisição — página pública, endpoint, arquivo, interface de programação de terceiro
ou varredura — é detalhe de implementação deste `Protocol` e **não é exposta** a entidades, regras,
parâmetros ou motores do domínio (`R85.3`).

Incorporar uma fonte nova exige implementar este contrato e cadastrar a fonte conforme `R1.1`, e
**nada mais**: nenhuma alteração de entidade, regra, parâmetro, motor ou esquema de dados
(`R85.5`). A CAIXA é a **primeira** implementação (`R85.4`), do lado dos adaptadores.

Camada de núcleo: declaração pura, sem cliente de rede e sem entrada e saída de dados (`MT-10`).
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Protocol

from radar.nucleo.contratos.tipos_dos_contratos import (
    ArquivoDeOferta,
    CoberturaDaFonte,
    FiltroDeBusca,
    OfertaBruta,
    ReferenciaDeOferta,
)

__all__ = ["ConectorDeFonte"]


class ConectorDeFonte(Protocol):
    """Contrato **único** de aquisição (`R85.1`). Quatro operações, e nada mais.

    Pré-condição: a fonte está cadastrada conforme `R1.1` e o conector declara identificador e
    versão — cada captura registra os dois (`R85.10`).

    Pós-condição: o payload bruto é preservado de forma imutável, com hash e versão da captura
    (`R85.6`, `R2.1` a `R2.4`); edital, matrícula, anexos e imagens são entregues ao
    `Gestor_de_Documentos` com o tipo declarado conforme `R86.4` (`R85.7`).

    Proibição: falha de obtenção registra fonte, data, hora e causa, preserva a última captura
    válida e **abstém-se** de registrar ausência de oferta como evidência de inexistência da oferta
    (`R85.9`, `SAFE-003`). Não conseguir listar não é o mesmo que a oferta ter saído do ar.
    """

    conector_id: str
    conector_versao: str

    def listar_ofertas(self, filtro: FiltroDeBusca) -> Iterator[ReferenciaDeOferta]:
        """Lista as referências de oferta que satisfazem o filtro."""
        ...

    def obter_detalhe(self, ref: ReferenciaDeOferta) -> OfertaBruta:
        """Entrega payload bruto, referência de origem, data e hora, hash, documentos, imagens e
        versão da captura (`R85.2`)."""
        ...

    def obter_documentos(self, ref: ReferenciaDeOferta) -> Sequence[ArquivoDeOferta]:
        """Entrega os arquivos da oferta, cada um com o tipo declarado (`R85.7`, `R86.4`)."""
        ...

    def declarar_cobertura(self) -> CoberturaDaFonte:
        """Declara o que a fonte cobre e o que não cobre (`R85.1`).

        É o que permite ao Radar saber o que a fonte não entrega sem tentar e falhar, e é a base
        das capacidades declaradas de `R110.6` e `R110.11`.
        """
        ...
