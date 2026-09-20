"""As três camadas declaradas e o grafo de importação proibida (`R119.1` a `R119.3`).

Este módulo é **declaração**, não mecanismo: as três camadas de `R119.1`, os 9 adaptadores de
`R119.2` e o conjunto de clientes externos proibidos no núcleo por `R119.3` existem aqui como
**dado consultável em tempo de execução**, para que a verificação seja mecânica e não uma
convenção lembrada de memória. `MT-10` percorre a árvore de imports de `src/radar/**` e falha com
o caminho completo do import proibido; `P19.2` verifica o mesmo fechamento transitivo como
propriedade. Os pacotes do núcleo e as espécies de cliente externo declarados aqui são os mesmos
que aqueles verificadores usam — divergência entre as duas listas é defeito, não variação.

A direção das dependências é única e é o contrato: o núcleo declara o contrato, o adaptador o
implementa, e o núcleo **nunca** conhece o adaptador. A infraestrutura — banco, armazenamento,
agendador, provedores, índice vetorial — vive fora do processo e é resolvida por configuração de
ambiente (`R113.2`); nenhum módulo do projeto pertence a ela, e é por isso que sua tupla de
pacotes é vazia.

Camada de núcleo: declaração pura, sem entrada e saída de dados, sem import de cliente externo.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Final

__all__ = [
    "ADAPTADORES_DECLARADOS",
    "CLIENTES_EXTERNOS_PROIBIDOS_NO_NUCLEO",
    "DEPENDENCIA_PERMITIDA_ENTRE_CAMADAS",
    "PACOTES_DO_NUCLEO",
    "PACOTES_POR_CAMADA",
    "AdaptadorDeclarado",
    "Camada",
    "EspecieDeClienteExterno",
    "camada_do_modulo",
    "dependencia_permitida",
    "especie_de_cliente_externo",
]


class Camada(StrEnum):
    """As 3 camadas declaradas da implementação (`R119.1`).

    `NUCLEO` é o domínio determinístico, as regras, os motores, os catálogos como dados e os
    contratos. `ADAPTADORES` são as implementações dos contratos. `INFRAESTRUTURA` são os
    recursos externos, que não são código deste processo.
    """

    NUCLEO = "NUCLEO"
    ADAPTADORES = "ADAPTADORES"
    INFRAESTRUTURA = "INFRAESTRUTURA"


class EspecieDeClienteExterno(StrEnum):
    """As 5 espécies de cliente que o núcleo não importa, direta ou transitivamente (`R119.3`).

    `R98.5` restringe a chamada a provedor aos adaptadores; estas são as espécies cuja mera
    presença no fechamento transitivo do núcleo é violação.
    """

    MODELO_DE_LINGUAGEM = "MODELO_DE_LINGUAGEM"
    ORQUESTRACAO_DE_IA = "ORQUESTRACAO_DE_IA"
    EMBEDDING = "EMBEDDING"
    ARMAZENAMENTO_EXTERNO = "ARMAZENAMENTO_EXTERNO"
    AGENDAMENTO = "AGENDAMENTO"


#: Camada → pacotes que lhe pertencem, em caminho relativo a `src/` (`R119.1`).
#: `INFRAESTRUTURA` é deliberadamente vazia: recurso externo não é pacote deste projeto.
PACOTES_POR_CAMADA: Final[Mapping[Camada, tuple[str, ...]]] = MappingProxyType(
    {
        Camada.NUCLEO: (
            "radar/nucleo",
            "radar/motores",
            "radar/pipeline",
            "radar/regras",
            "radar/radar",
        ),
        Camada.ADAPTADORES: (
            "radar/adaptadores",
            "radar/ia",
            "radar/plataforma",
            "radar/conectores",
        ),
        Camada.INFRAESTRUTURA: (),
    }
)

#: Os 5 pacotes do núcleo, na mesma ordem em que `MT-10` os verifica.
PACOTES_DO_NUCLEO: Final[tuple[str, ...]] = PACOTES_POR_CAMADA[Camada.NUCLEO]

#: Pacote raiz proibido no núcleo → espécie de cliente externo que ele representa (`R119.3`).
#: A chave é a **raiz** do nome importado: `langchain_core.messages` casa por `langchain_core`.
CLIENTES_EXTERNOS_PROIBIDOS_NO_NUCLEO: Final[Mapping[str, EspecieDeClienteExterno]] = (
    MappingProxyType(
        {
            "anthropic": EspecieDeClienteExterno.MODELO_DE_LINGUAGEM,
            "apscheduler": EspecieDeClienteExterno.AGENDAMENTO,
            "boto3": EspecieDeClienteExterno.ARMAZENAMENTO_EXTERNO,
            "botocore": EspecieDeClienteExterno.ARMAZENAMENTO_EXTERNO,
            "celery": EspecieDeClienteExterno.AGENDAMENTO,
            "croniter": EspecieDeClienteExterno.AGENDAMENTO,
            "langchain": EspecieDeClienteExterno.MODELO_DE_LINGUAGEM,
            "langchain_community": EspecieDeClienteExterno.MODELO_DE_LINGUAGEM,
            "langchain_core": EspecieDeClienteExterno.MODELO_DE_LINGUAGEM,
            "langchain_openai": EspecieDeClienteExterno.MODELO_DE_LINGUAGEM,
            "langgraph": EspecieDeClienteExterno.ORQUESTRACAO_DE_IA,
            "openai": EspecieDeClienteExterno.MODELO_DE_LINGUAGEM,
            "s3transfer": EspecieDeClienteExterno.ARMAZENAMENTO_EXTERNO,
            "sentence_transformers": EspecieDeClienteExterno.EMBEDDING,
            "tiktoken": EspecieDeClienteExterno.MODELO_DE_LINGUAGEM,
        }
    )
)

#: Camada → camadas que ela pode importar. O núcleo importa apenas o núcleo, e é essa linha
#: que proíbe o núcleo de conhecer o adaptador (`R119.3`). A infraestrutura não importa nada
#: porque não é código: é recurso externo alcançado pelo adaptador.
DEPENDENCIA_PERMITIDA_ENTRE_CAMADAS: Final[Mapping[Camada, frozenset[Camada]]] = MappingProxyType(
    {
        Camada.NUCLEO: frozenset({Camada.NUCLEO}),
        Camada.ADAPTADORES: frozenset({Camada.NUCLEO, Camada.ADAPTADORES}),
        Camada.INFRAESTRUTURA: frozenset(),
    }
)


@dataclass(frozen=True, slots=True)
class AdaptadorDeclarado:
    """Um adaptador declarado por `R119.2`: implementa **um** contrato do núcleo.

    Se a substituição de uma implementação exige tocar o núcleo, o contrato está errado
    (`R119.4`). A troca não altera o resultado determinístico (`R119.6`, `P21.19`), e cada
    execução registra os adaptadores aplicados (`R119.7`).
    """

    nome: str
    contrato: str
    implementacoes: tuple[str, ...]
    requisitos: tuple[str, ...]


#: Os 9 adaptadores declarados por `R119.2`, cada um com o contrato do núcleo que implementa.
ADAPTADORES_DECLARADOS: Final[tuple[AdaptadorDeclarado, ...]] = (
    AdaptadorDeclarado(
        nome="Armazenamento de arquivo",
        contrato="ArmazenamentoDeArquivo",
        implementacoes=("disco local", "S3"),
        requisitos=("R119.2", "R86.2"),
    ),
    AdaptadorDeclarado(
        nome="Banco de dados",
        contrato="RepositorioTransacional",
        implementacoes=("PostgreSQL local", "PostgreSQL gerenciado"),
        requisitos=("R119.2", "R74"),
    ),
    AdaptadorDeclarado(
        nome="Agendamento",
        contrato="Agendador",
        implementacoes=("cron local", "agendador de nuvem", "processo assíncrono"),
        requisitos=("R110.3", "R110.4"),
    ),
    AdaptadorDeclarado(
        nome="Modelo de linguagem",
        contrato="ProvedorDeModeloDeLinguagem",
        implementacoes=("OpenAI", "modelo local"),
        requisitos=("R98.1", "R98.3", "R98.8"),
    ),
    AdaptadorDeclarado(
        nome="Embedding",
        contrato="ProvedorDeEmbedding",
        implementacoes=("OpenAI",),
        requisitos=("R98.2", "R98.3"),
    ),
    AdaptadorDeclarado(
        nome="Índice vetorial",
        contrato="IndiceVetorial",
        implementacoes=("pgvector",),
        requisitos=("R102.1", "R102.9"),
    ),
    AdaptadorDeclarado(
        nome="Estratégia de captura",
        contrato="EstrategiaDeCaptura",
        implementacoes=("página pública", "endpoint", "arquivo", "varredura"),
        requisitos=("R107.4", "D94"),
    ),
    AdaptadorDeclarado(
        nome="Canal de notificação",
        contrato="CanalDeNotificacao",
        implementacoes=("local", "canal externo"),
        requisitos=("R121.2", "R121.3"),
    ),
    AdaptadorDeclarado(
        nome="Conector de fonte",
        contrato="ConectorDeFonte",
        implementacoes=("CAIXA",),
        requisitos=("R85.1", "R85.4"),
    ),
)


def camada_do_modulo(modulo: str) -> Camada | None:
    """Camada a que o módulo pertence, ou `None` quando nenhum pacote declarado o contém.

    Aceita nome importável (`radar.nucleo.camadas`) e caminho (`radar/nucleo/camadas.py`).
    """
    normalizado = modulo.removesuffix(".py").replace("\\", "/").replace("/", ".").strip(".")
    for camada, pacotes in PACOTES_POR_CAMADA.items():
        for pacote in pacotes:
            prefixo = pacote.replace("/", ".")
            if normalizado == prefixo or normalizado.startswith(f"{prefixo}."):
                return camada
    return None


def especie_de_cliente_externo(modulo_importado: str) -> EspecieDeClienteExterno | None:
    """Espécie de cliente externo do módulo importado, ou `None` quando ele não é um.

    A classificação é pela raiz do nome: `boto3.session` é armazenamento externo.
    """
    raiz = modulo_importado.split(".")[0]
    return CLIENTES_EXTERNOS_PROIBIDOS_NO_NUCLEO.get(raiz)


def dependencia_permitida(origem: Camada, destino: Camada) -> bool:
    """Se a camada de origem pode importar a camada de destino (`R119.3`)."""
    return destino in DEPENDENCIA_PERMITIDA_ENTRE_CAMADAS[origem]
