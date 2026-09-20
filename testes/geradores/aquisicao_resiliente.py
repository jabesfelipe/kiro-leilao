"""Geradores da aquisição resiliente — `P20` (`R106` a `R110`).

Três casos que a arquitetura anterior não conseguia exercitar e que aqui são geráveis:

- `captura_invalida()` produz a resposta com **lista vazia** e o conteúdo **não interpretável**.
  Nenhum dos dois pode classificar oferta conhecida como removida da fonte, e nenhum dos dois pode
  descartar a última captura válida (`R107.8`, `R107.9`, `AQ-010`, `REG-046`, `REG-047`);
- `sequencia_de_falhas()` produz duas ausências válidas consecutivas, que é a condição exata de
  `REMOVIDA_DA_FONTE` (`R108.5`, `REG-048`);
- `par_de_capturas_da_mesma_oferta()` produz a mesma oferta com preço alterado, que não pode criar
  imóvel novo (`R84.12`, `REG-036`).

`payload_por_estrategia()` fixa o **mesmo** payload sob estratégias diferentes: é o gerador de
`P17.20`, e sem a igualdade do payload a propriedade não diria nada.

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

from radar.nucleo.enumeracoes_de_infraestrutura import (
    CategoriaDeErro,
    EstadoDaOfertaNaFonte,
    EstrategiaDeCaptura,
    SituacaoDeExecucaoDoRadar,
)
from testes.geradores.escalas import data_hora_br, dinheiro

__all__ = [
    "CAPACIDADES_DO_CONECTOR",
    "EXECUCOES_PARA_REMOCAO_DA_FONTE",
    "CapturaDeOferta",
    "CapturaInvalida",
    "ExecucaoDoRadar",
    "PayloadPorEstrategia",
    "capacidades_declaradas",
    "captura_invalida",
    "chave_de_idempotencia",
    "execucao_do_radar",
    "par_de_capturas_da_mesma_oferta",
    "payload_por_estrategia",
    "sequencia_de_falhas",
]

CAPACIDADES_DO_CONECTOR: Final[tuple[str, ...]] = (
    "listar_ofertas",
    "obter_detalhe",
    "obter_documentos",
    "declarar_cobertura",
)
"""As quatro operações do contrato `ConectorDeFonte` (`R85.1`).

Uma nova fonte exige implementar o contrato e cadastrar a fonte, e nada mais (`R85.5`): cobertura
declarada parcialmente é caso legítimo, e o gerador a produz.
"""

EXECUCOES_PARA_REMOCAO_DA_FONTE: Final[int] = 2
"""Duas execuções **válidas** consecutivas sem a oferta ⇒ `REMOVIDA_DA_FONTE` (`R108.5`).

Execução inválida não conta. É a distinção que `REG-046` e `REG-048` cobrem juntos.
"""


@dataclass(frozen=True, slots=True, kw_only=True)
class ExecucaoDoRadar:
    """Execução do Radar auditável, com estratégia, contagens e situação (`R106.4`)."""

    identificador: UUID
    fonte: str
    estrategia: EstrategiaDeCaptura
    situacao: SituacaoDeExecucaoDoRadar
    ofertas_listadas: int
    capturas_persistidas: int
    rejeicoes: int
    iniciada_em: datetime
    chave_de_idempotencia: str


def execucao_do_radar() -> st.SearchStrategy[ExecucaoDoRadar]:
    """Execução do Radar nas seis situações, incluindo `PARCIAL` e `INTERROMPIDA`.

    `ofertas_listadas = 0` é gerado de propósito: lista vazia é resultado implausível, e a execução
    que a recebe não pode concluir como `CONCLUIDA` limpa nem marcar ofertas como removidas.
    """
    return st.builds(
        ExecucaoDoRadar,
        identificador=st.uuids(),
        fonte=st.sampled_from(("caixa", "banco-do-brasil", "leiloeiro-oficial")),
        estrategia=st.sampled_from(EstrategiaDeCaptura),
        situacao=st.sampled_from(SituacaoDeExecucaoDoRadar),
        ofertas_listadas=st.one_of(st.just(0), st.integers(min_value=1, max_value=500)),
        capturas_persistidas=st.integers(min_value=0, max_value=500),
        rejeicoes=st.integers(min_value=0, max_value=50),
        iniciada_em=data_hora_br(),
        chave_de_idempotencia=st.text(min_size=1, max_size=32),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class PayloadPorEstrategia:
    """O **mesmo** payload sob duas estratégias de captura diferentes (`P17.20`).

    A estratégia é invisível ao domínio (`R85.3`, `R106.8`, `P20.4`); este tipo existe para que a
    propriedade possa fixar o payload e variar só a estratégia.
    """

    conteudo: Mapping[str, str]
    primeira_estrategia: EstrategiaDeCaptura
    segunda_estrategia: EstrategiaDeCaptura


def payload_por_estrategia() -> st.SearchStrategy[PayloadPorEstrategia]:
    """Payload fixo com par de estratégias distintas."""
    return st.builds(
        PayloadPorEstrategia,
        conteudo=st.fixed_dictionaries(
            {
                "identificador": st.text(min_size=1, max_size=16),
                "preco": st.sampled_from(("47.76", "191651.31", "250000,00")),
                "matricula": st.from_regex(r"\A[0-9]{4,8}\Z", fullmatch=True),
            }
        ),
        primeira_estrategia=st.sampled_from(EstrategiaDeCaptura),
        segunda_estrategia=st.sampled_from(EstrategiaDeCaptura),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class CapturaInvalida:
    """Captura que a fonte devolveu de forma inválida — e o motivo exato (`R107.8`, `R107.9`).

    `payload_bruto_preservado` é sempre verdadeiro por construção: o payload é preservado inclusive
    no caminho de rejeição (`R85.6`, `R85.8`). Gerá-lo como falso seria gerar um estado que o
    sistema não tem permissão de alcançar.
    """

    motivo: CategoriaDeErro
    quantidade_devolvida: int
    conteudo_interpretavel: bool
    payload_bruto_preservado: bool
    ultima_captura_valida_mantida: bool


def captura_invalida() -> st.SearchStrategy[CapturaInvalida]:
    """Captura inválida, com lista vazia e conteúdo não interpretável entre os casos gerados."""
    return st.builds(
        CapturaInvalida,
        motivo=st.sampled_from(
            (
                CategoriaDeErro.FONTE_ALTERADA,
                CategoriaDeErro.FONTE_INDISPONIVEL,
                CategoriaDeErro.DOCUMENTO_INVALIDO,
                CategoriaDeErro.ERRO_DE_EXECUCAO_DO_RADAR,
            )
        ),
        quantidade_devolvida=st.one_of(st.just(0), st.integers(min_value=1, max_value=10)),
        conteudo_interpretavel=st.booleans(),
        payload_bruto_preservado=st.just(True),
        ultima_captura_valida_mantida=st.just(True),
    )


def sequencia_de_falhas() -> st.SearchStrategy[tuple[bool, ...]]:
    """Sequência de execuções, `True` quando a oferta esteve presente e válida na fonte.

    Duas ausências consecutivas em execuções **válidas** é a condição de `REMOVIDA_DA_FONTE`. A
    sequência é gerada com 2 a 6 execuções, o que garante que a condição de duas seja alcançável e
    que o caso de uma única ausência — que **não** basta — também apareça.
    """
    return st.lists(st.booleans(), min_size=2, max_size=6).map(tuple)


@dataclass(frozen=True, slots=True, kw_only=True)
class CapturaDeOferta:
    """Uma captura da mesma oferta, com preço e estado na fonte (`R108.2`)."""

    identificador_na_fonte: str
    fonte: str
    preco: Decimal
    estado_na_fonte: EstadoDaOfertaNaFonte
    capturada_em: datetime


def par_de_capturas_da_mesma_oferta() -> st.SearchStrategy[
    tuple[CapturaDeOferta, CapturaDeOferta]
]:
    """Duas capturas da **mesma** oferta, com preço possivelmente alterado.

    Identificador na fonte e fonte são idênticos nas duas por construção: é o que faz a segunda
    captura ser *da mesma oferta*. Nenhuma das duas pode criar imóvel novo (`REG-036`), e o
    histórico de preços tem de registrar a variação.
    """
    return st.builds(
        _par_da_mesma_oferta,
        identificador_na_fonte=st.text(min_size=1, max_size=16),
        fonte=st.sampled_from(("caixa", "banco-do-brasil")),
        primeiro_preco=dinheiro(),
        segundo_preco=dinheiro(),
        primeiro_estado=st.sampled_from(EstadoDaOfertaNaFonte),
        segundo_estado=st.sampled_from(EstadoDaOfertaNaFonte),
        capturada_em=data_hora_br(),
    )


def _par_da_mesma_oferta(
    *,
    identificador_na_fonte: str,
    fonte: str,
    primeiro_preco: Decimal,
    segundo_preco: Decimal,
    primeiro_estado: EstadoDaOfertaNaFonte,
    segundo_estado: EstadoDaOfertaNaFonte,
    capturada_em: datetime,
) -> tuple[CapturaDeOferta, CapturaDeOferta]:
    primeira = CapturaDeOferta(
        identificador_na_fonte=identificador_na_fonte,
        fonte=fonte,
        preco=primeiro_preco,
        estado_na_fonte=primeiro_estado,
        capturada_em=capturada_em,
    )
    segunda = CapturaDeOferta(
        identificador_na_fonte=identificador_na_fonte,
        fonte=fonte,
        preco=segundo_preco,
        estado_na_fonte=segundo_estado,
        capturada_em=capturada_em,
    )
    return (primeira, segunda)


def chave_de_idempotencia() -> st.SearchStrategy[str]:
    """Chave de idempotência, com repetição garantida no espaço de geração.

    O conjunto de chaves é pequeno de propósito: idempotência só é verificável quando a **mesma**
    chave reaparece. Chaves uniformemente aleatórias praticamente nunca colidiriam, e a propriedade
    de "exatamente um efeito persistido" (`R109.3`, `REG-049`) passaria sem nunca ser exercitada.
    """
    return st.sampled_from(("chave-a", "chave-b", "chave-c", "chave-d"))


def capacidades_declaradas() -> st.SearchStrategy[tuple[str, ...]]:
    """Cobertura declarada por um conector, de uma a quatro operações.

    Cobertura parcial é legítima e precisa ser declarada: chamar operação não coberta é erro
    explícito, não resultado vazio (`R85.1`, `R85.4`).
    """
    return st.lists(
        st.sampled_from(CAPACIDADES_DO_CONECTOR),
        min_size=1,
        max_size=len(CAPACIDADES_DO_CONECTOR),
        unique=True,
    ).map(tuple)
