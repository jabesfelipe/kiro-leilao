"""Valor com estado de informação e o sentinela explícito de ausência.

Nenhum número circula sozinho no domínio econômico e documental: circula como
`Informado[T]` — valor, estado da informação, fonte, data de observação, confiança e
qualidade da evidência (`R3.2`, `R10.2`, `R26.7`).

Ausência de informação é representada pelo sentinela `Desconhecido`, nunca por zero,
string vazia ou qualquer outro valor neutro: nenhum campo de domínio recebe default
permissivo (`R26.10`, SAFE-003, SAFE-005). Ausência de evidência não é regularidade e é
distinta de evidência de ausência (SAFE-017); `DESCONHECIDO` permanece `DESCONHECIDO`
enquanto não houver nova evidência (SAFE-004), e este módulo não oferece caminho de
promoção automática.

`MetricaProvisoria[T]` carrega o motivo da provisoriedade junto com o número, para que
decidir sobre número provisório exija que a provisoriedade viaje junto — o caso de
componente de custo `DESCONHECIDO` de impacto alto ou crítico (`R26.12`).

Camada de núcleo: funções puras, sem entrada e saída de dados.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Final, cast

from radar.nucleo.enumeracoes import EstadoDaInformacao, Impacto, QualidadeDaEvidencia

__all__ = [
    "CONFIANCA_MAXIMA",
    "CONFIANCA_MINIMA",
    "DESCONHECIDO",
    "Desconhecido",
    "Informado",
    "MetricaProvisoria",
    "MotivoDeProvisoriedade",
]

CONFIANCA_MINIMA: Final[Decimal] = Decimal(0)
CONFIANCA_MAXIMA: Final[Decimal] = Decimal(100)


@dataclass(frozen=True, slots=True)
class Desconhecido:
    """Sentinela explícito de ausência de informação (`R3.2`, SAFE-003).

    É um valor de domínio, não um marcador de conveniência: aparece nas uniões de tipo
    (`Decimal | Desconhecido`) para que a ausência seja visível na assinatura e
    verificável por tipo. Não define valor de verdade próprio, para que
    `if valor:` não possa confundir ausência com zero.
    """


DESCONHECIDO: Final[Desconhecido] = Desconhecido()


def _exigir_texto_informado(valor: str | Desconhecido, campo: str) -> None:
    """Rejeita texto em branco: ausência se declara com `Desconhecido`, não com ``''``."""
    if isinstance(valor, Desconhecido):
        return
    if not valor.strip():
        raise ValueError(
            f"{campo} em branco não representa ausência de informação; use Desconhecido"
        )


def _rejeitar_float(valor: object, campo: str) -> None:
    """`float` não atravessa a fronteira do núcleo: o caminho monetário é `Decimal`."""
    if isinstance(valor, float):
        raise TypeError(f"{campo} não aceita float; use Decimal")


@dataclass(frozen=True, slots=True, kw_only=True)
class Informado[T]:
    """Valor acompanhado do seu estado de informação e da sua proveniência.

    Nenhum campo tem default: a ausência é declarada, campo por campo, com
    `Desconhecido` (`R26.10`, SAFE-005). O estado `DESCONHECIDO` e a ausência de valor
    são a mesma coisa, e a construção que os separa é rejeitada — é o que impede que um
    custo desconhecido circule como zero.
    """

    valor: T | Desconhecido
    estado_da_informacao: EstadoDaInformacao
    fonte: str | Desconhecido
    data_de_observacao: datetime | Desconhecido
    confianca: Decimal | Desconhecido
    qualidade_da_evidencia: QualidadeDaEvidencia

    def __post_init__(self) -> None:
        _rejeitar_float(self.valor, "valor")
        _rejeitar_float(self.confianca, "confianca")
        _exigir_texto_informado(self.fonte, "fonte")
        self._validar_coerencia_do_estado()
        self._validar_confianca()

    def _validar_coerencia_do_estado(self) -> None:
        sem_valor = isinstance(self.valor, Desconhecido)
        sem_confianca = isinstance(self.confianca, Desconhecido)
        desconhecido = self.estado_da_informacao is EstadoDaInformacao.DESCONHECIDO
        if sem_valor and not desconhecido:
            raise ValueError(
                "valor ausente exige estado_da_informacao DESCONHECIDO "
                f"(recebido {self.estado_da_informacao})"
            )
        if desconhecido and not sem_valor:
            raise ValueError(
                "estado_da_informacao DESCONHECIDO exige valor ausente (Desconhecido)"
            )
        if not desconhecido:
            return
        if self.qualidade_da_evidencia is not QualidadeDaEvidencia.AUSENTE:
            raise ValueError(
                "estado_da_informacao DESCONHECIDO exige qualidade_da_evidencia AUSENTE "
                f"(recebido {self.qualidade_da_evidencia})"
            )
        if not sem_confianca:
            raise ValueError(
                "estado_da_informacao DESCONHECIDO exige confianca ausente (Desconhecido)"
            )

    def _validar_confianca(self) -> None:
        if isinstance(self.confianca, Desconhecido):
            return
        if not CONFIANCA_MINIMA <= self.confianca <= CONFIANCA_MAXIMA:
            raise ValueError(
                f"confianca fora da escala {CONFIANCA_MINIMA}-{CONFIANCA_MAXIMA}: "
                f"{self.confianca}"
            )

    @property
    def esta_desconhecido(self) -> bool:
        """Verdadeiro quando não há valor — e, por construção, o estado é `DESCONHECIDO`."""
        return isinstance(self.valor, Desconhecido)

    def exigir_valor(self) -> T:
        """Devolve o valor ou falha. Nunca devolve zero nem valor neutro (SAFE-005)."""
        if self.esta_desconhecido:
            raise ValueError(
                "valor DESCONHECIDO não tem substituto numérico; resolva a pendência"
            )
        return cast("T", self.valor)

    @classmethod
    def desconhecido(
        cls,
        *,
        fonte: str | Desconhecido = DESCONHECIDO,
        data_de_observacao: datetime | Desconhecido = DESCONHECIDO,
    ) -> Informado[T]:
        """Ausência de informação, com a proveniência que houver.

        Os defaults são o próprio sentinela: declaram ausência, e não valor neutro. A
        fonte é informável porque saber **quem** deixou de informar é proveniência
        (`R10.4`), e a data de observação porque a ausência também é observada numa data.
        """
        return cls(
            valor=DESCONHECIDO,
            estado_da_informacao=EstadoDaInformacao.DESCONHECIDO,
            fonte=fonte,
            data_de_observacao=data_de_observacao,
            confianca=DESCONHECIDO,
            qualidade_da_evidencia=QualidadeDaEvidencia.AUSENTE,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class MotivoDeProvisoriedade:
    """Por que uma métrica é provisória, com a pendência determinante nomeada.

    `R26.12`: componente de custo `DESCONHECIDO` de impacto alto ou crítico marca o
    preço máximo como provisório e exige registrar de qual pendência depende o valor
    definitivo. O impacto é `Desconhecido` quando ainda não foi estimado — nunca `baixo`
    por omissão.
    """

    componente: str
    estado_da_informacao: EstadoDaInformacao
    impacto: Impacto | Desconhecido
    pendencia_determinante: str

    def __post_init__(self) -> None:
        if not self.componente.strip():
            raise ValueError("componente é obrigatório no motivo da provisoriedade")
        if not self.pendencia_determinante.strip():
            raise ValueError(
                "pendencia_determinante é obrigatória: o valor definitivo depende da "
                "resolução de uma pendência nomeada"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class MetricaProvisoria[T]:
    """Métrica cujo caráter provisório viaja junto com o número.

    Os motivos não têm default: uma métrica só é definitiva quando alguém declara que
    nada a torna provisória. Métrica sem valor é necessariamente provisória — dizer que
    um número inexistente é definitivo seria tratar ausência como resultado.
    """

    valor: Informado[T]
    motivos_da_provisoriedade: tuple[MotivoDeProvisoriedade, ...]

    def __post_init__(self) -> None:
        if self.valor.esta_desconhecido and not self.motivos_da_provisoriedade:
            raise ValueError(
                "métrica sem valor exige ao menos um motivo de provisoriedade"
            )

    @property
    def esta_provisoria(self) -> bool:
        """Verdadeiro quando há ao menos um motivo de provisoriedade registrado."""
        return bool(self.motivos_da_provisoriedade)
