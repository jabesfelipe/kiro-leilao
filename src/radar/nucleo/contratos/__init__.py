"""Os oito contratos declarados pelo núcleo (`R119.1`, `R119.2`).

O núcleo declara o contrato, o adaptador o implementa, e o núcleo nunca conhece o adaptador. A
direção das dependências é única, e **o grafo de importação proibida é o contrato** (`R119.3`,
`R98.5`): nada aqui importa cliente de modelo de linguagem, biblioteca de orquestração de IA,
cliente de embedding, cliente de armazenamento externo ou cliente de agendamento. `MT-10` percorre
o fechamento transitivo de imports e falha com o caminho completo do import proibido; `P19.2`
verifica o mesmo fechamento como propriedade.

| Contrato | Implementações da primeira versão | Requisito |
|----------|-----------------------------------|-----------|
| `ProvedorDeModeloDeLinguagem` | OpenAI (`IA-001`); modelo local (`P1`) | `R98.1`, `R98.8` |
| `ProvedorDeEmbedding` | OpenAI (`IA-002`) | `R98.2` |
| `IndiceVetorial` | pgvector | `R102.1`, `R102.9` |
| `ArmazenamentoDeArquivo` | disco local; S3 | `R119.2`, `R86.2` |
| `Agendador` | cron local; agendador de nuvem; processo assíncrono | `R110.3`, `R110.4` |
| `CanalDeNotificacao` | local (`PLT-013`); canal externo (`P1`) | `R121.2`, `R121.3` |
| `ConectorDeFonte` | CAIXA | `R85.1`, `R85.4` |
| `EstrategiaDeCaptura` | página pública; endpoint; arquivo; varredura | `R107.4`, `D94` |

`EstrategiaDeCaptura` exportado por este pacote é o **contrato**. O **enum** homônimo de quatro
valores vive em `radar.nucleo.enumeracoes_de_infraestrutura` e não é reexportado aqui: os dois
mantêm o nome único de `D103`, e a desambiguação é o caminho do módulo.

Trocar qualquer adaptador declarado não altera o resultado determinístico: para as mesmas
evidências, os mesmos parâmetros e as mesmas versões, o resultado é idêntico em qualquer combinação
(`R119.4`, `R119.6`, `R98.9`).
"""

from __future__ import annotations

from radar.nucleo.contratos.agendador import Agendador
from radar.nucleo.contratos.armazenamento_de_arquivo import ArmazenamentoDeArquivo
from radar.nucleo.contratos.canal_de_notificacao import CanalDeNotificacao
from radar.nucleo.contratos.conector_de_fonte import ConectorDeFonte
from radar.nucleo.contratos.estrategia_de_captura import EstrategiaDeCaptura
from radar.nucleo.contratos.indice_vetorial import IndiceVetorial
from radar.nucleo.contratos.provedor_de_embedding import ProvedorDeEmbedding
from radar.nucleo.contratos.provedor_de_modelo_de_linguagem import ProvedorDeModeloDeLinguagem

__all__ = [
    "Agendador",
    "ArmazenamentoDeArquivo",
    "CanalDeNotificacao",
    "ConectorDeFonte",
    "EstrategiaDeCaptura",
    "IndiceVetorial",
    "ProvedorDeEmbedding",
    "ProvedorDeModeloDeLinguagem",
]
