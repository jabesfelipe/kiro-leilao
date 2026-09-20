"""Geradores de gate jurídico, evidência e pendência (`R12` a `R20`, `R37`, `R89`).

Três coisas o módulo existe para tornar geráveis, porque sem elas as propriedades do gate viram
inspeção manual: o conjunto **completo** das dezenove verificações, a distinção entre
`DESCONHECIDO` e `NAO_APLICAVEL`, e a diferença entre **evidência** registrada e **proposta** de
evidência produzida por componente automatizado.

Nenhum componente automatizado cria evidência (`SAFE-009`): `proposta_de_evidencia()` gera
proposta, e proposta não tem caminho implícito para virar registro.

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
    EstadoDaInformacao,
    EstadoDeAverbacaoDeLeilaoNegativo,
    OrigemDeEvidencia,
    PrioridadeDePendencia,
    QualidadeDaEvidencia,
    ResultadoDeEviccao,
    ResultadoDeVerificacao,
    ResultadoP0,
    SituacaoJuridica,
)
from testes.geradores.escalas import data_hora_br, escala_de_zero_a_cem

__all__ = [
    "CODIGOS_DE_VERIFICACAO_JURIDICA",
    "Pendencia",
    "PropostaDeEvidencia",
    "RegistroDeEvidencia",
    "avaliacao_de_eviccao",
    "conjunto_de_pendencias",
    "estado_de_averbacao",
    "proposta_de_evidencia",
    "registro_de_evidencia",
    "resultado_p0",
    "resultados_de_verificacao",
    "situacao_juridica",
]

CODIGOS_DE_VERIFICACAO_JURIDICA: Final[tuple[str, ...]] = (
    *(f"RULE-JUR-{numero:03d}" for numero in range(1, 14)),
    *(f"RULE-ED-{numero:03d}" for numero in range(1, 5)),
    *(f"RULE-ID-{numero:03d}" for numero in range(1, 3)),
)
"""As dezenove verificações do gate: treze `RULE-JUR-*`, quatro `RULE-ED-*`, duas `RULE-ID-*`.

A contagem é contrato de `R12.9`. `RULE-OCC-*` e `RULE-LOC-*` **não** estão aqui: saíram do gate
para a camada 6 de risco (`R12.10`), e `RULE-REG-*` não existe em fonte alguma (`D.5`).
"""


def resultados_de_verificacao() -> st.SearchStrategy[Mapping[str, ResultadoDeVerificacao]]:
    """Resultado de **cada uma** das dezenove verificações — cobertura total, sempre.

    Gerar o conjunto completo é o que permite às propriedades exigir cobertura sem lacuna: se uma
    verificação pudesse faltar do dicionário, ausência de chave e `DESCONHECIDO` se confundiriam,
    que é precisamente o que `D.2.8` e `REG-025` proíbem.
    """
    return st.fixed_dictionaries(
        {
            codigo: st.sampled_from(ResultadoDeVerificacao)
            for codigo in CODIGOS_DE_VERIFICACAO_JURIDICA
        }
    )


def situacao_juridica() -> st.SearchStrategy[SituacaoJuridica]:
    """Situação jurídica fechada em três valores. Valor fora do domínio é erro, não `REGULAR`."""
    return st.sampled_from(SituacaoJuridica)


def estado_de_averbacao() -> st.SearchStrategy[EstadoDeAverbacaoDeLeilaoNegativo]:
    """Averbação de leilão negativo. `EM_TRATAMENTO` é pendência registral, não `BLOQUEIO`."""
    return st.sampled_from(EstadoDeAverbacaoDeLeilaoNegativo)


def avaliacao_de_eviccao() -> st.SearchStrategy[ResultadoDeEviccao]:
    """Evicção nos três resultados: cláusula ausente comprovada e não verificada são distintas."""
    return st.sampled_from(ResultadoDeEviccao)


@dataclass(frozen=True, slots=True, kw_only=True)
class RegistroDeEvidencia:
    """Evidência registrada, com proveniência obrigatória (`R20`, `R65.1`, `R89.2`).

    Não existe evidência sem fonte (`R73.2`): `fonte` e `origem` são campos obrigatórios, e a
    localização documental acompanha toda evidência extraída de documento.
    """

    identificador: UUID
    fato: str
    origem: OrigemDeEvidencia
    fonte: str
    estado_da_informacao: EstadoDaInformacao
    qualidade: QualidadeDaEvidencia
    confianca: Decimal
    localizacao_documental: str
    observado_em: datetime


def registro_de_evidencia() -> st.SearchStrategy[RegistroDeEvidencia]:
    """Evidência registrada e válida, inclusive a de irregularidade comprovada.

    Irregularidade comprovada é a evidência mais decisiva que o gate produz e vem com estado
    `CONFIRMADO` e confiança alta — a confiança expressa a qualidade da prova, não a conveniência
    do resultado (`D.2.8`).
    """
    return st.builds(
        RegistroDeEvidencia,
        identificador=st.uuids(),
        fato=st.text(min_size=1, max_size=60),
        origem=st.sampled_from(OrigemDeEvidencia),
        fonte=st.text(min_size=1, max_size=40),
        estado_da_informacao=st.sampled_from(EstadoDaInformacao),
        qualidade=st.sampled_from(QualidadeDaEvidencia),
        confianca=escala_de_zero_a_cem(),
        localizacao_documental=st.text(min_size=1, max_size=40),
        observado_em=data_hora_br(),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class PropostaDeEvidencia:
    """Proposta produzida por componente automatizado (`SAFE-009`, `R20.9`).

    Proposta **não** é evidência. A promoção exige ato humano registrado ou regra determinística
    declarada, e o identificador do responsável não tem default.
    """

    identificador: UUID
    fato_proposto: str
    componente_de_origem: str
    confianca_declarada: Decimal
    localizacao_documental: str
    proposta_em: datetime


def proposta_de_evidencia() -> st.SearchStrategy[PropostaDeEvidencia]:
    """Proposta de evidência sem nenhum campo de promoção — a promoção é ato externo."""
    return st.builds(
        PropostaDeEvidencia,
        identificador=st.uuids(),
        fato_proposto=st.text(min_size=1, max_size=60),
        componente_de_origem=st.sampled_from(
            ("extrator-de-texto", "agente-de-analise", "classificador-de-documento")
        ),
        confianca_declarada=escala_de_zero_a_cem(),
        localizacao_documental=st.text(min_size=1, max_size=40),
        proposta_em=data_hora_br(),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class Pendencia:
    """Pendência aberta, com prioridade e condição objetiva de encerramento (`R37`)."""

    identificador: UUID
    descricao: str
    prioridade: PrioridadeDePendencia
    verificacao_de_origem: str
    condicao_de_encerramento: str
    resolvida: bool


def conjunto_de_pendencias() -> st.SearchStrategy[tuple[Pendencia, ...]]:
    """Conjunto de pendências, possivelmente vazio, com identificadores distintos.

    O conjunto vazio é gerado de propósito: resolver a última pendência é o gatilho `MON-011`, e
    a propriedade que verifica o recálculo precisa ver a transição de não vazio para vazio.
    """
    pendencia = st.builds(
        Pendencia,
        identificador=st.uuids(),
        descricao=st.text(min_size=1, max_size=60),
        prioridade=st.sampled_from(PrioridadeDePendencia),
        verificacao_de_origem=st.sampled_from(CODIGOS_DE_VERIFICACAO_JURIDICA),
        condicao_de_encerramento=st.text(min_size=1, max_size=60),
        resolvida=st.booleans(),
    )
    return st.lists(
        pendencia,
        min_size=0,
        max_size=6,
        unique_by=lambda registro: registro.identificador,
    ).map(tuple)


def resultado_p0() -> st.SearchStrategy[ResultadoP0]:
    """Resultado do gate `P0` nos cinco valores. `INCONCLUSIVO` não é `REGULAR_COMPROVADO`."""
    return st.sampled_from(ResultadoP0)
