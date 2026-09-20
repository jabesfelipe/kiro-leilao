"""Versão do motor e data de corte — o par que torna o histórico interpretável (`R120`).

Duas perguntas de auditoria: **qual motor** produziu esta decisão e **até que data** a evidência
foi admitida. `VersaoDoMotor` (`R120.1`, `PLT-003`) e `DataDeCorte` (`R120.4`) respondem cada uma
delas, e ambas são tipo de **primeira classe**, nunca texto solto: é o que permite registrá-las em
cada análise, cada decisão e cada resultado calculado (`P21.20`) e compará-las sem interpretar
cadeia em cada ponto de uso.

A data de corte não é rótulo informativo: ela **recusa** evidência. Nenhuma evidência com data de
observação posterior à data de corte é admitida na versão de análise que a declara (`R120.5`,
`P21.21`, `REG-058`), e a recusa vive aqui, em `DataDeCorte.admite` e
`exigir_evidencia_admissivel`, como função pura verificável — não como comentário a ser lembrado
por quem escreve o próximo motor. É a mesma disciplina do antiviés temporal de `SAFE-015`:
informação futura não avalia decisão passada. A evidência recusada **não** desaparece; ela
permanece disponível para uma nova versão de análise, com nova data de corte (`REG-058`).

O limite é **fechado**: evidência observada **na** data de corte é admitida, posterior não. É a
diferença entre "até" e "antes de", e é o caso que uma amostragem de datas quase nunca visitaria.

Data e hora circula sempre consciente de fuso — data ingênua é defeito de domínio, rejeitado na
entrada. A data de corte é uma data de calendário, e um instante só pertence a um dia depois de
declarado o fuso em que o calendário é lido: `FUSO_DE_BRASILIA` é esse fuso, declarado uma vez, em
lugar de ficar implícito no fuso da máquina que executa a análise.

Camada de núcleo (`R119.1`): função pura, sem entrada e saída de dados.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Final

from radar.nucleo.informado import Desconhecido

__all__ = [
    "FUSO_DE_BRASILIA",
    "VERSAO_DO_MOTOR_CANONICA",
    "DataDeCorte",
    "VersaoDoMotor",
    "exigir_evidencia_admissivel",
    "exigir_publicacao_de_nova_versao",
]

FUSO_DE_BRASILIA: Final[timezone] = timezone(timedelta(hours=-3))
"""Fuso em que a data de corte é lida como dia de calendário.

Deslocamento fixo de −3 h: o Brasil não observa horário de verão desde 2019, e o deslocamento
fixo evita que a admissibilidade de uma evidência dependa da base de fusos do sistema operacional
que executa a análise. O fuso é declarado porque um instante só pertence a um dia **depois** de
escolhido o calendário em que se lê o dia.
"""


def _exigir_inteiro_nao_negativo(valor: object, campo: str) -> int:
    """Componente de versão é inteiro não negativo. `bool` e `float` não são versão."""
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TypeError(f"{campo} exige int não negativo (recebido {type(valor).__name__})")
    if valor < 0:
        raise ValueError(f"{campo} exige int não negativo (recebido {valor})")
    return valor


def _exigir_data_e_hora_com_fuso(valor: datetime, campo: str) -> datetime:
    """Rejeita data e hora ingênua: sem fuso não existe instante, e sem instante não há corte."""
    if valor.tzinfo is None or valor.tzinfo.utcoffset(valor) is None:
        raise ValueError(
            f"{campo} exige data e hora consciente de fuso; data ingênua não determina instante"
        )
    return valor


@dataclass(frozen=True, slots=True, order=True)
class VersaoDoMotor:
    """Versão do motor determinístico que produziu um resultado (`R120.1`, `PLT-003`).

    Tipo de primeira classe, não texto solto (`D103`): a ordem entre versões é a ordem semântica
    — maior, depois menor, depois correção —, e é ela que `exigir_publicacao_de_nova_versao`
    verifica. Registrada em cada análise, cada decisão e cada resultado calculado (`P21.20`), de
    modo que o histórico produzido por versões anteriores permaneça interpretável (`R120.3`).
    """

    maior: int
    menor: int
    correcao: int

    def __post_init__(self) -> None:
        _exigir_inteiro_nao_negativo(self.maior, "maior")
        _exigir_inteiro_nao_negativo(self.menor, "menor")
        _exigir_inteiro_nao_negativo(self.correcao, "correcao")

    def __str__(self) -> str:
        """Forma canônica `maior.menor.correcao`, para registro e apresentação (`R120.3`)."""
        return f"{self.maior}.{self.menor}.{self.correcao}"

    @classmethod
    def a_partir_do_texto(cls, texto: str) -> VersaoDoMotor:
        """Converte a versão semântica de `PLT-003` na fronteira, uma vez, e falha alto.

        A conversão de cadeia existe **só** aqui: configuração e persistência entregam texto, e é
        nesta fronteira que ele deixa de ser texto. Cadeia sem os três componentes, com componente
        não numérico ou com sinal é defeito de configuração, não versão aproximada.
        """
        partes = texto.strip().split(".")
        if len(partes) != 3:
            raise ValueError(
                f"versão do motor exige três componentes maior.menor.correcao (recebido {texto!r})"
            )
        if not all(parte.isdigit() for parte in partes):
            raise ValueError(
                f"componente de versão do motor exige apenas dígitos (recebido {texto!r})"
            )
        maior, menor, correcao = (int(parte) for parte in partes)
        return cls(maior=maior, menor=menor, correcao=correcao)


VERSAO_DO_MOTOR_CANONICA: Final[VersaoDoMotor] = VersaoDoMotor(maior=1, menor=0, correcao=0)
"""Versão canônica de `PLT-003`: 1.0.0. Valor `[CANÔNICO]`, não default configurável."""


@dataclass(frozen=True, slots=True, order=True)
class DataDeCorte:
    """Data até a qual a evidência foi admitida em uma análise (`R120.4`).

    Tipo de primeira classe (`D103`). O valor é uma data de **calendário**: o corte é um dia
    inteiro, lido no fuso de `FUSO_DE_BRASILIA`, e não um instante — dizer "corte em 10 de março"
    é admitir tudo que foi observado naquele dia, a qualquer hora.

    `datetime` é subclasse de `date` e seria aceito em silêncio, com semântica diferente da
    declarada; por isso é rejeitado na construção.
    """

    valor: date

    def __post_init__(self) -> None:
        if isinstance(self.valor, datetime):
            raise TypeError(
                "data de corte é data de calendário, não instante; passe date, não datetime"
            )
        if not isinstance(self.valor, date):
            raise TypeError(f"data de corte exige date (recebido {type(self.valor).__name__})")

    def __str__(self) -> str:
        """Forma ISO `AAAA-MM-DD`, para registro por análise (`R120.4`)."""
        return self.valor.isoformat()

    def admite(self, data_de_observacao: datetime | Desconhecido) -> bool:
        """Verdadeiro quando a evidência entra nesta versão de análise (`R120.5`).

        O limite é fechado: observação **na** data de corte é admitida, posterior não. O instante
        é convertido para `FUSO_DE_BRASILIA` antes de virar dia de calendário, de modo que a
        admissibilidade não dependa do fuso em que o instante foi registrado.

        Evidência sem data de observação **não** é admitida: toda evidência registra a data em que
        foi observada (`R120.8`), e ausência de data não demonstra anterioridade ao corte. Tratar a
        ausência como anterioridade seria deixar informação futura entrar por omissão
        (`SAFE-015`). Ela permanece disponível para uma nova versão de análise, uma vez estabelecida
        a data (`REG-058`).
        """
        if isinstance(data_de_observacao, Desconhecido):
            return False
        instante = _exigir_data_e_hora_com_fuso(data_de_observacao, "data_de_observacao")
        return instante.astimezone(FUSO_DE_BRASILIA).date() <= self.valor


def exigir_evidencia_admissivel(
    data_de_corte: DataDeCorte,
    data_de_observacao: datetime | Desconhecido,
) -> None:
    """Recusa, com a causa nomeada, a evidência que não entra nesta versão (`R120.5`, `REG-058`).

    O predicado é `DataDeCorte.admite`; esta função é o caminho de quem precisa **falhar** em vez
    de escolher, para que nenhuma evidência posterior ao corte atravesse por descuido de quem
    esqueceu de testar o retorno.
    """
    if data_de_corte.admite(data_de_observacao):
        return
    if isinstance(data_de_observacao, Desconhecido):
        raise ValueError(
            f"evidência sem data de observação não é admitida na análise de corte "
            f"{data_de_corte}: a anterioridade ao corte não é demonstrável (R120.5, R120.8)"
        )
    observada_em = data_de_observacao.astimezone(FUSO_DE_BRASILIA).date()
    raise ValueError(
        f"evidência observada em {observada_em.isoformat()} é posterior à data de corte "
        f"{data_de_corte} e não é admitida nesta versão de análise (R120.5); ela permanece "
        "disponível para nova versão com nova data de corte"
    )


def exigir_publicacao_de_nova_versao(
    anterior: VersaoDoMotor,
    nova: VersaoDoMotor,
    *,
    decisao_alterada: bool,
) -> None:
    """Regra que altera a decisão de alguma entrada exige versão nova e maior (`R120.2`).

    A verificação é da ordem semântica, não da igualdade: republicar a mesma versão, ou retroceder,
    deixaria duas decisões diferentes atribuídas ao mesmo motor — e o histórico de `R120.3` deixaria
    de ser interpretável. Mudança que não altera decisão alguma não exige nova versão, e por isso
    `decisao_alterada` é declarada pelo chamador em vez de inferida.
    """
    if not decisao_alterada:
        return
    if nova <= anterior:
        raise ValueError(
            f"mudança de regra que altera decisão exige publicar versão do motor maior que "
            f"{anterior} (recebido {nova}); mesma versão com decisão diferente torna o histórico "
            "não interpretável (R120.2, R120.3)"
        )
