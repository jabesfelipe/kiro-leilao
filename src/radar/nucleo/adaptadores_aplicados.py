"""Os adaptadores aplicados em cada execução, e a combinação local da primeira (`R119.4` a `R119.7`).

`R119.7` exige que **cada** execução registre os adaptadores aplicados. O registro só é útil se for
**total**: uma execução declara uma implementação para cada um dos 9 adaptadores de `R119.2`, e o
adaptador que não participou é declarado `NAO_APLICADO` em lugar de ser omitido do registro. Omissão
e ausência são indistinguíveis depois do fato — ao reproduzir uma análise, "não havia índice
vetorial" e "esqueceram de registrar o índice vetorial" levariam à mesma linha em branco, e é isso
que `CombinacaoDeAdaptadores` recusa na construção, nomeando o adaptador omitido.

A lista dos adaptadores e as implementações admissíveis de cada um **não** são redeclaradas aqui:
vêm de `ADAPTADORES_DECLARADOS` (`camadas.py`), ponto único de `R119.2`. Registrar uma implementação
que o adaptador não declara é defeito de configuração, não variação, e falha alto.

**A primeira execução completa é local** (`R119.5`): `COMBINACAO_LOCAL_DA_PRIMEIRA_EXECUCAO` declara
esse conjunto como valor nomeado — armazenamento em disco local, PostgreSQL local, cron local —, de
modo que "roda local" seja um valor verificável e não uma afirmação de documento. Nuvem é escolha
posterior, por troca de adaptador, não reescrita (`D93`, `R119.8`).

**A troca de adaptador declarado não altera o resultado** (`R119.4`, `R119.6`): `substituir` é a
operação de troca — devolve outra combinação e não toca em nada do núcleo —, `adaptadores_divergentes`
nomeia em que adaptadores duas execuções diferem, e `exigir_invariancia_de_adaptador` é a forma
verificável da invariância: mesma entrada determinística, resultados diferentes, e a falha nomeia os
adaptadores trocados. A verificação sobre o espaço inteiro de combinações é `P21.19`, em tarefa
própria; o que existe aqui é a estrutura que a torna verificável.

Camada de núcleo (`R119.1`): valores imutáveis e funções puras, sem entrada e saída de dados e sem
cliente externo (`R119.3`, `MT-10`). O núcleo registra **qual** adaptador foi aplicado; jamais o
importa.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final

from radar.nucleo.camadas import ADAPTADORES_DECLARADOS
from radar.nucleo.correlacao import IdentificadorDeCorrelacao
from radar.nucleo.versao_do_motor import VersaoDoMotor

__all__ = [
    "COMBINACAO_LOCAL_DA_PRIMEIRA_EXECUCAO",
    "IMPLEMENTACOES_POR_ADAPTADOR",
    "NAO_APLICADO",
    "NOMES_DOS_ADAPTADORES_DECLARADOS",
    "TEXTO_DE_NAO_APLICADO",
    "AdaptadorAplicado",
    "CombinacaoDeAdaptadores",
    "ExecucaoRegistrada",
    "ImplementacaoAplicada",
    "NaoAplicado",
    "adaptadores_divergentes",
    "exigir_invariancia_de_adaptador",
]

#: Texto sob o qual a ausência declarada é registrada e apresentada (`R119.7`).
TEXTO_DE_NAO_APLICADO: Final[str] = "NAO_APLICADO"


@dataclass(frozen=True, slots=True)
class NaoAplicado:
    """Ausência **declarada** de implementação para um adaptador nesta execução (`R119.7`).

    É valor de primeira classe, e não `None`: aparece na união de tipo para que a ausência seja
    visível na assinatura e verificável por tipo, do mesmo modo que `Desconhecido` no domínio
    econômico. Declarar que o índice vetorial não participou é informação de reprodução — omiti-lo
    do registro não é.
    """

    def __str__(self) -> str:
        return TEXTO_DE_NAO_APLICADO


NAO_APLICADO: Final[NaoAplicado] = NaoAplicado()

type ImplementacaoAplicada = str | NaoAplicado
"""Implementação aplicada a um adaptador: o nome declarado em `R119.2`, ou a ausência declarada."""

#: Os 9 nomes de `R119.2`, na ordem em que `ADAPTADORES_DECLARADOS` os declara. A ordem é o que
#: torna a combinação comparável termo a termo, sem depender de ordenação de mapa.
NOMES_DOS_ADAPTADORES_DECLARADOS: Final[tuple[str, ...]] = tuple(
    adaptador.nome for adaptador in ADAPTADORES_DECLARADOS
)

#: Adaptador → implementações que ele declara (`R119.2`). Derivado, nunca redigitado: divergência
#: entre esta tabela e `camadas.py` seria defeito, e por isso não existe segunda lista.
IMPLEMENTACOES_POR_ADAPTADOR: Final[Mapping[str, tuple[str, ...]]] = MappingProxyType(
    {adaptador.nome: adaptador.implementacoes for adaptador in ADAPTADORES_DECLARADOS}
)


def _exigir_adaptador_declarado(adaptador: str) -> None:
    """Adaptador fora de `R119.2` não é registrável: o registro é da combinação declarada."""
    if adaptador not in IMPLEMENTACOES_POR_ADAPTADOR:
        raise ValueError(
            f"adaptador {adaptador!r} não é declarado por R119.2; os declarados são "
            f"{', '.join(NOMES_DOS_ADAPTADORES_DECLARADOS)}"
        )


def _exigir_implementacao_declarada(adaptador: str, implementacao: ImplementacaoAplicada) -> None:
    """Implementação registrada é uma das declaradas para aquele adaptador, ou a ausência."""
    if isinstance(implementacao, NaoAplicado):
        return
    if not isinstance(implementacao, str):
        raise TypeError(
            f"implementação de {adaptador!r} exige str ou NAO_APLICADO "
            f"(recebido {type(implementacao).__name__})"
        )
    if not implementacao.strip():
        raise ValueError(
            f"implementação de {adaptador!r} em branco não declara ausência; use NAO_APLICADO"
        )
    declaradas = IMPLEMENTACOES_POR_ADAPTADOR[adaptador]
    if implementacao not in declaradas:
        raise ValueError(
            f"implementação {implementacao!r} não é declarada para o adaptador {adaptador!r}; "
            f"as declaradas são {', '.join(declaradas)}"
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class AdaptadorAplicado:
    """Um adaptador de `R119.2` e a implementação que esta execução lhe aplicou (`R119.7`)."""

    adaptador: str
    implementacao: ImplementacaoAplicada

    def __post_init__(self) -> None:
        _exigir_adaptador_declarado(self.adaptador)
        _exigir_implementacao_declarada(self.adaptador, self.implementacao)

    @property
    def foi_aplicado(self) -> bool:
        """Falso quando a execução declarou que o adaptador não participou."""
        return not isinstance(self.implementacao, NaoAplicado)

    def __str__(self) -> str:
        return f"{self.adaptador}={self.implementacao}"


@dataclass(frozen=True, slots=True)
class CombinacaoDeAdaptadores:
    """A combinação **total** de adaptadores aplicados por uma execução (`R119.7`).

    Total significa os 9 adaptadores de `R119.2`, na ordem declarada, cada um exatamente uma vez:
    adaptador omitido, repetido ou fora de ordem é recusado na construção, com o nome do adaptador
    na mensagem. `a_partir_do_mapa` é o caminho ergonômico — ordena pela ordem declarada e cobra a
    totalidade —, e é ele que o chamador usa.

    Congelada e comparável por valor: é o que permite a `P21.19` gerar pares de combinações
    distintas e comparar resultados sem interpretar texto.
    """

    itens: tuple[AdaptadorAplicado, ...]

    def __post_init__(self) -> None:
        registrados = tuple(item.adaptador for item in self.itens)
        if registrados == NOMES_DOS_ADAPTADORES_DECLARADOS:
            return
        conjunto = set(registrados)
        omitidos = tuple(
            nome for nome in NOMES_DOS_ADAPTADORES_DECLARADOS if nome not in conjunto
        )
        if omitidos:
            raise ValueError(
                "combinação de adaptadores é total: a ausência é declarada com NAO_APLICADO, "
                f"nunca omitida (omitidos: {', '.join(omitidos)})"
            )
        if len(conjunto) != len(registrados):
            repetidos = tuple(
                nome for nome in NOMES_DOS_ADAPTADORES_DECLARADOS if registrados.count(nome) > 1
            )
            raise ValueError(
                f"adaptador registrado mais de uma vez na combinação: {', '.join(repetidos)}"
            )
        raise ValueError(
            "combinação de adaptadores segue a ordem declarada em R119.2; "
            "use CombinacaoDeAdaptadores.a_partir_do_mapa para ordenar"
        )

    @classmethod
    def a_partir_do_mapa(
        cls, implementacao_por_adaptador: Mapping[str, ImplementacaoAplicada]
    ) -> CombinacaoDeAdaptadores:
        """Constrói a combinação a partir do mapa adaptador → implementação, na ordem declarada.

        Nada é preenchido por default: o mapa incompleto **falha**, nomeando o adaptador omitido,
        porque supor `NAO_APLICADO` por omissão seria exatamente a omissão silenciosa que `R119.7`
        impede.
        """
        for adaptador in implementacao_por_adaptador:
            _exigir_adaptador_declarado(adaptador)
        faltando = tuple(
            nome
            for nome in NOMES_DOS_ADAPTADORES_DECLARADOS
            if nome not in implementacao_por_adaptador
        )
        if faltando:
            raise ValueError(
                "combinação de adaptadores é total: declare a implementação ou NAO_APLICADO para "
                f"cada adaptador de R119.2 (faltando: {', '.join(faltando)})"
            )
        return cls(
            itens=tuple(
                AdaptadorAplicado(
                    adaptador=nome, implementacao=implementacao_por_adaptador[nome]
                )
                for nome in NOMES_DOS_ADAPTADORES_DECLARADOS
            )
        )

    @property
    def implementacao_por_adaptador(self) -> Mapping[str, ImplementacaoAplicada]:
        """A combinação como mapa somente leitura, para consulta por nome de adaptador."""
        return MappingProxyType({item.adaptador: item.implementacao for item in self.itens})

    def implementacao_de(self, adaptador: str) -> ImplementacaoAplicada:
        """Implementação aplicada ao adaptador. Adaptador fora de `R119.2` falha alto."""
        _exigir_adaptador_declarado(adaptador)
        return self.implementacao_por_adaptador[adaptador]

    def substituir(
        self, adaptador: str, implementacao: ImplementacaoAplicada
    ) -> CombinacaoDeAdaptadores:
        """A troca de adaptador de `R119.4`: outra combinação, sem alteração alguma do núcleo.

        Devolve valor novo em lugar de mutar — trocar adaptador no meio de uma execução tornaria o
        registro de `R119.7` ambíguo sobre qual combinação produziu o resultado.
        """
        _exigir_adaptador_declarado(adaptador)
        return CombinacaoDeAdaptadores.a_partir_do_mapa(
            {**self.implementacao_por_adaptador, adaptador: implementacao}
        )

    def como_mapa_de_texto(self) -> Mapping[str, str]:
        """Forma textual do registro por execução (`R119.7`), com a ausência visível como texto."""
        return MappingProxyType({item.adaptador: str(item.implementacao) for item in self.itens})


#: A combinação da **primeira execução completa**, inteiramente local (`R119.5`): arquivo em disco
#: local, banco PostgreSQL local, agendamento por cron local. A fonte e a estratégia de captura
#: acompanham porque sem elas não há execução completa, e o canal de notificação local fecha o
#: ciclo (`R121.4`).
#:
#: Modelo de linguagem, embedding e índice vetorial são declarados `NAO_APLICADO`, não omitidos: o
#: domínio determinístico executa sem componente de linguagem (`R71.1`, `R119.3`) e sem a etapa de
#: recuperação (`R102.8`), e nenhum dos três é recurso local. Habilitá-los é escolha adicional de
#: configuração por ambiente (`R113.2`), e a troca não altera o resultado determinístico (`R119.6`).
COMBINACAO_LOCAL_DA_PRIMEIRA_EXECUCAO: Final[CombinacaoDeAdaptadores] = (
    CombinacaoDeAdaptadores.a_partir_do_mapa(
        {
            "Armazenamento de arquivo": "disco local",
            "Banco de dados": "PostgreSQL local",
            "Agendamento": "cron local",
            "Modelo de linguagem": NAO_APLICADO,
            "Embedding": NAO_APLICADO,
            "Índice vetorial": NAO_APLICADO,
            "Estratégia de captura": "página pública",
            "Canal de notificação": "local",
            "Conector de fonte": "CAIXA",
        }
    )
)


@dataclass(frozen=True, slots=True, kw_only=True)
class ExecucaoRegistrada:
    """O que uma execução registra sobre si para que a reprodução seja possível (`R119.7`).

    Três elementos, e nenhum deles com default: a correlação que liga todos os registros daquela
    execução (`R111.1`), a versão do motor que produziu o resultado (`R120.1`) e a combinação de
    adaptadores aplicada. `chave_da_entrada_deterministica` é a identidade daquilo de que o
    resultado **pode** depender — evidências, parâmetros resolvidos e versões (`R120.6`) —, e é ela
    que separa duas execuções comparáveis de duas execuções simplesmente diferentes.
    """

    correlacao: IdentificadorDeCorrelacao
    versao_do_motor: VersaoDoMotor
    adaptadores_aplicados: CombinacaoDeAdaptadores
    chave_da_entrada_deterministica: str

    def __post_init__(self) -> None:
        if not self.chave_da_entrada_deterministica.strip():
            raise ValueError(
                "chave_da_entrada_deterministica em branco não identifica entrada: declare as "
                "evidências, os parâmetros e as versões que produziram o resultado (R120.6)"
            )

    @property
    def mesma_entrada_e_versoes_que_comparaveis(self) -> tuple[str, str]:
        """Par que duas execuções têm de compartilhar para que `R119.6` se aplique a elas."""
        return (self.chave_da_entrada_deterministica, str(self.versao_do_motor))


def adaptadores_divergentes(
    primeira: CombinacaoDeAdaptadores, segunda: CombinacaoDeAdaptadores
) -> tuple[str, ...]:
    """Adaptadores em que duas combinações aplicaram implementações diferentes, na ordem declarada.

    Função pura e total: combinações iguais devolvem tupla vazia, e a ausência declarada participa
    da comparação como qualquer outra implementação — trocar `pgvector` por `NAO_APLICADO` é troca
    de adaptador, e aparece aqui.
    """
    de_primeira = primeira.implementacao_por_adaptador
    de_segunda = segunda.implementacao_por_adaptador
    return tuple(
        nome
        for nome in NOMES_DOS_ADAPTADORES_DECLARADOS
        if de_primeira[nome] != de_segunda[nome]
    )


def exigir_invariancia_de_adaptador(
    primeira: ExecucaoRegistrada,
    segunda: ExecucaoRegistrada,
    *,
    resultado_da_primeira: object,
    resultado_da_segunda: object,
) -> None:
    """Mesma entrada e mesmas versões exigem o mesmo resultado determinístico (`R119.6`).

    Duas recusas distintas, e a distinção é o que dá valor à verificação:

    - Entradas ou versões diferentes: a comparação **não é aplicável**, e dizer que passou seria
      afirmar invariância sem tê-la observado. Falha nomeando a divergência de entrada.
    - Mesma entrada e resultados diferentes: é a violação de `R119.6`, e a falha nomeia os
      adaptadores trocados — a informação de que quem investiga precisa.

    É a forma executável da propriedade `P21.19`, que a exercita sobre pares de combinações
    geradas.
    """
    if primeira.mesma_entrada_e_versoes_que_comparaveis != segunda.mesma_entrada_e_versoes_que_comparaveis:
        raise ValueError(
            "invariância de adaptador compara execuções com as mesmas evidências, os mesmos "
            "parâmetros e as mesmas versões (R119.6); recebidas entradas distintas: "
            f"{primeira.mesma_entrada_e_versoes_que_comparaveis} e "
            f"{segunda.mesma_entrada_e_versoes_que_comparaveis}"
        )
    if resultado_da_primeira == resultado_da_segunda:
        return
    divergentes = adaptadores_divergentes(
        primeira.adaptadores_aplicados, segunda.adaptadores_aplicados
    )
    trocados = ", ".join(divergentes) if divergentes else "nenhum"
    raise ValueError(
        "troca de adaptador declarado alterou o resultado determinístico para as mesmas "
        f"evidências, parâmetros e versões (R119.6); adaptadores trocados: {trocados}"
    )
