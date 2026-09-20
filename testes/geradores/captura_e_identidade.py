"""Geradores de captura, normalização e identidade (`R1` a `R11`, `R84` a `R85`).

O payload bruto é gerado como ele chega da fonte — **texto**, inclusive as cadeias de fronteira
de `D.1.3` e `D.1.4` — porque é exatamente na travessia de texto para número que os defeitos de
interpretação vivem. A oferta normalizada já é domínio: preço e área são `Informado`, e matrícula
ausente é `Desconhecido`, nunca cadeia vazia.

Camada de infraestrutura de teste: nenhuma entrada e saída de dados.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Final
from uuid import UUID

from hypothesis import strategies as st

from radar.nucleo.enumeracoes import (
    EstadoDaCaptura,
    ForcaDeSinal,
    NivelDeIdentidade,
    PortaDeEntrada,
    VeredictoDeIdentidade,
)
from radar.nucleo.informado import DESCONHECIDO, Desconhecido, Informado
from testes.geradores.escalas import (
    AreaDeclarada,
    area,
    data_hora_br,
    dinheiro,
    escala_de_zero_a_cem,
    informado,
    texto_de_dinheiro,
    texto_de_percentual,
)

__all__ = [
    "FONTES_DE_CAPTURA",
    "OfertaNormalizada",
    "PayloadBruto",
    "SinaisDeIdentidade",
    "VinculoDeImovel",
    "matricula",
    "oferta_normalizada",
    "payload_bruto",
    "sinais_de_identidade",
    "vinculo_de_imovel",
]

FONTES_DE_CAPTURA: Final[tuple[str, ...]] = (
    "caixa",
    "banco-do-brasil",
    "leiloeiro-oficial",
    "prefeitura",
    "arquivo-enviado",
)
"""Tipos de fonte distintos. O normalizador despacha por tipo de fonte e falha se não houver
normalizador registrado (`D.6.11`, `REG-030`); gerar mais de uma fonte é o que torna isso visível.
"""


@dataclass(frozen=True, slots=True, kw_only=True)
class PayloadBruto:
    """Payload preservado de forma imutável antes de qualquer avaliação (`R85.6`, `R85.8`).

    `campos` é texto puro: é assim que a fonte entrega, e é onde `"47.76"` e `"2,5%"` precisam
    aparecer para que a interpretação seja exercitada de verdade.
    """

    fonte: str
    identificador_na_fonte: str
    campos: Mapping[str, str]
    obtido_em: datetime
    hash_do_conteudo: str


def payload_bruto() -> st.SearchStrategy[PayloadBruto]:
    """Payload bruto com as cadeias numéricas de fronteira sempre no espaço de geração."""
    campos = st.fixed_dictionaries(
        {
            "preco": texto_de_dinheiro(),
            "avaliacao": texto_de_dinheiro(),
            "aliquota_itbi": texto_de_percentual(),
            "area": texto_de_dinheiro(),
        }
    )
    return st.builds(
        PayloadBruto,
        fonte=st.sampled_from(FONTES_DE_CAPTURA),
        identificador_na_fonte=st.text(min_size=1, max_size=24),
        campos=campos,
        obtido_em=data_hora_br(),
        hash_do_conteudo=st.text(alphabet="0123456789abcdef", min_size=64, max_size=64),
    )


def matricula() -> st.SearchStrategy[str | Desconhecido]:
    """Número de matrícula, ou `Desconhecido`. Matrícula ausente não é cadeia vazia (`R13.2`)."""
    return st.one_of(
        st.just(DESCONHECIDO),
        st.from_regex(r"\A[0-9]{4,8}\Z", fullmatch=True),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class OfertaNormalizada:
    """Oferta já interpretada, com estado de informação por campo (`R2`, `R3`)."""

    fonte: str
    identificador_na_fonte: str
    preco: Informado[Decimal]
    avaliacao_da_fonte: Informado[Decimal]
    area_declarada: AreaDeclarada
    matricula: str | Desconhecido
    municipio: str
    estado_da_captura: EstadoDaCaptura
    porta_de_entrada: PortaDeEntrada


def oferta_normalizada() -> st.SearchStrategy[OfertaNormalizada]:
    """Oferta normalizada válida, incluindo os casos em que o preço é `DESCONHECIDO`.

    A avaliação da fonte é campo próprio e **nunca** se converte em valor de mercado
    (`SAFE-012`): gerá-la separada do preço é o que permite verificar isso.
    """
    return st.builds(
        OfertaNormalizada,
        fonte=st.sampled_from(FONTES_DE_CAPTURA),
        identificador_na_fonte=st.text(min_size=1, max_size=24),
        preco=informado(dinheiro()),
        avaliacao_da_fonte=informado(dinheiro()),
        area_declarada=area(),
        matricula=matricula(),
        municipio=st.sampled_from(("São Paulo", "Campinas", "Curitiba", "Recife")),
        estado_da_captura=st.sampled_from(EstadoDaCaptura),
        porta_de_entrada=st.sampled_from(PortaDeEntrada),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class SinaisDeIdentidade:
    """Sinais de identificação com a força declarada de cada um (`R7.1`, `R7.6`).

    O nível resultante é gerado junto para que as propriedades possam confrontar sinal e nível
    em lugar de recalcular a regra dentro do teste.
    """

    matricula: str | Desconhecido
    inscricao_imobiliaria: str | Desconhecido
    endereco_normalizado: str | Desconhecido
    identificador_na_fonte: str
    forca_predominante: ForcaDeSinal
    nivel: NivelDeIdentidade


def sinais_de_identidade() -> st.SearchStrategy[SinaisDeIdentidade]:
    """Sinais de identidade, com ausência de sinal representada por `Desconhecido`."""
    texto_ou_desconhecido = st.one_of(st.just(DESCONHECIDO), st.text(min_size=1, max_size=40))
    return st.builds(
        SinaisDeIdentidade,
        matricula=matricula(),
        inscricao_imobiliaria=texto_ou_desconhecido,
        endereco_normalizado=texto_ou_desconhecido,
        identificador_na_fonte=st.text(min_size=1, max_size=24),
        forca_predominante=st.sampled_from(ForcaDeSinal),
        nivel=st.sampled_from(NivelDeIdentidade),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class VinculoDeImovel:
    """Vínculo entre captura e imóvel, com o veredicto de três valores (`R9.6`).

    `INDETERMINADO` é um veredicto, não uma falha: nova captura da mesma oferta não pode criar
    imóvel novo (`REG-036`), e não pode fundir dois imóveis sob dúvida.
    """

    identificador_do_imovel: UUID
    nivel_de_identidade: NivelDeIdentidade
    veredicto: VeredictoDeIdentidade
    confianca_do_vinculo: Decimal
    justificativa: str


def vinculo_de_imovel() -> st.SearchStrategy[VinculoDeImovel]:
    """Vínculo de imóvel com confiança na escala de fronteira `[0, 100]`."""
    return st.builds(
        VinculoDeImovel,
        identificador_do_imovel=st.uuids(),
        nivel_de_identidade=st.sampled_from(NivelDeIdentidade),
        veredicto=st.sampled_from(VeredictoDeIdentidade),
        confianca_do_vinculo=escala_de_zero_a_cem(),
        justificativa=st.text(min_size=1, max_size=80),
    )
