"""Geradores de decisão e de disciplina de lance (`R53` a `R56`, `R60`).

A entrada de decisão traz as onze camadas como dados: gerar a camada determinante ao lado do
veredito é o que permite verificar que ela é a de **menor** índice entre as eliminatórias
(`R53.1`, `D.2.4`) e que nenhum escore alto supera `BLOQUEAR` (`SAFE-001`, `R73.4`).

O checklist de lance gera o caso de parada absoluta: divergência entre portal e edital, evicção
não verificada, revalidação registral pendente. São os casos em que o lance **não** é liberado, e
sem eles o checklist não prova nada.

Camada de infraestrutura de teste: nenhuma entrada e saída de dados.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal

from hypothesis import strategies as st

from radar.nucleo.enumeracoes import (
    CamadaDeDecisao,
    ClasseDeAtratividade,
    ClasseDeUrgencia,
    EstadoDeDecisao,
    Estrategia,
    NivelDeConfianca,
    ResultadoDeItemDeChecklist,
    Severidade,
    SituacaoJuridica,
)
from testes.geradores.escalas import escala_de_zero_a_cem

__all__ = [
    "VERIFICACOES_DE_LANCE",
    "ChecklistDeLance",
    "EntradaDeDecisao",
    "checklist_de_lance",
    "entrada_de_decisao",
]

VERIFICACOES_DE_LANCE: tuple[str, ...] = (
    "RL-01",
    "RL-02",
    "RL-03",
    "RL-04",
    "RL-05",
    "RL-06",
    "RL-07",
    "RL-08",
    "RL-09",
    "RL-10",
)
"""As verificações de liberação de lance (`RL-*`). `RL-02` e `RL-10` são a parada absoluta por
divergência entre portal e edital (`REG-014`)."""


@dataclass(frozen=True, slots=True, kw_only=True)
class EntradaDeDecisao:
    """Entrada completa do motor de decisão — nenhuma camada fica implícita.

    `situacao_juridica` e `severidade_maxima_de_risco` entram separadas do escore de propósito:
    é a separação que torna verificável que escore, desconto, margem, yield, liquidez e Investor
    Fit não superam um `BLOQUEAR` (`R73.4`).
    """

    situacao_juridica: SituacaoJuridica
    severidade_maxima_de_risco: Severidade
    escore_de_oportunidade: Decimal
    investor_fit: Decimal
    confianca_consolidada: Decimal
    confianca_do_valuation: Decimal
    escore_de_liquidez: Decimal
    desconto_liquido: Decimal
    margem_de_seguranca: Decimal
    estrategia: Estrategia
    nivel_de_confianca: NivelDeConfianca
    pendencias_abertas: int
    reserva_minima_preservada: bool
    veredito_esperado: EstadoDeDecisao
    camada_determinante: CamadaDeDecisao
    urgencia: ClasseDeUrgencia
    atratividade: ClasseDeAtratividade


def entrada_de_decisao() -> st.SearchStrategy[EntradaDeDecisao]:
    """Entrada de decisão sobre todo o espaço de vereditos e camadas.

    Os escores vêm de `escala_de_zero_a_cem()`, de modo que a decisão é exercitada exatamente em
    `GLB-003` = 75, `GLB-004` = 60, `GLB-006` = 70, `VAL-009` = 70, no mínimo de aderência
    `SCORE-007` = 60 e nos fracionários vizinhos de cada um. No limiar exato, a decisão é a
    satisfação, não a reprovação.
    """
    escala = escala_de_zero_a_cem()
    fracao = st.decimals(
        min_value=Decimal(0),
        max_value=Decimal(1),
        places=4,
        allow_nan=False,
        allow_infinity=False,
    )
    return st.builds(
        EntradaDeDecisao,
        situacao_juridica=st.sampled_from(SituacaoJuridica),
        severidade_maxima_de_risco=st.sampled_from(Severidade),
        escore_de_oportunidade=escala,
        investor_fit=escala,
        confianca_consolidada=escala,
        confianca_do_valuation=escala,
        escore_de_liquidez=escala,
        desconto_liquido=fracao,
        margem_de_seguranca=fracao,
        estrategia=st.sampled_from(Estrategia),
        nivel_de_confianca=st.sampled_from(NivelDeConfianca),
        pendencias_abertas=st.integers(min_value=0, max_value=8),
        reserva_minima_preservada=st.booleans(),
        veredito_esperado=st.sampled_from(EstadoDeDecisao),
        camada_determinante=st.sampled_from(CamadaDeDecisao),
        urgencia=st.sampled_from(ClasseDeUrgencia),
        atratividade=st.sampled_from(ClasseDeAtratividade),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class ChecklistDeLance:
    """Checklist de liberação de lance, com o resultado de cada verificação `RL-*` (`R60`)."""

    verificacoes: Mapping[str, ResultadoDeItemDeChecklist]
    divergencia_entre_portal_e_edital: bool
    eviccao_verificada: bool
    revalidacao_registral_realizada: bool
    limite_de_lance: Decimal


def checklist_de_lance() -> st.SearchStrategy[ChecklistDeLance]:
    """Checklist de lance com todas as verificações presentes e as três paradas absolutas.

    Cobertura total das verificações é deliberada: verificação ausente do dicionário e
    verificação `DESCONHECIDO` não podem se confundir, e `DESCONHECIDO` nunca é favorável.
    """
    return st.builds(
        ChecklistDeLance,
        verificacoes=st.fixed_dictionaries(
            dict.fromkeys(
                VERIFICACOES_DE_LANCE,
                st.sampled_from(ResultadoDeItemDeChecklist),
            )
        ),
        divergencia_entre_portal_e_edital=st.booleans(),
        eviccao_verificada=st.booleans(),
        revalidacao_registral_realizada=st.booleans(),
        limite_de_lance=st.sampled_from(
            (Decimal(0), Decimal(150_000), Decimal(182_158), Decimal(250_000))
        ),
    )
