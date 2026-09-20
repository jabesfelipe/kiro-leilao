"""Tipos de fronteira citados pelos oito contratos, declarados como apelidos opacos.

As assinaturas dos contratos de `R119.2` citam tipos que **pertencem a outros componentes**:
`PromptVersionado` é de `R100`, `OrcamentoDeExecucaoDeIA` é de `R99`, `OfertaBruta` e
`CoberturaDaFonte` são de `R85`, `ColecaoDoIndiceVetorial` é de `R102.9`, `ExecucaoDoRadar` é de
`R106.1`, `Notificacao` é de `R121.2`, e assim por diante. Nenhum deles é declarado por esta
tarefa, e declará-los aqui criaria um segundo dono para o mesmo tipo — exatamente o defeito que
`D103` proíbe no plano dos nomes.

Enquanto o componente proprietário não aterrissa, cada tipo entra aqui como **apelido opaco**:
um `NewType` nominal sobre `object`, sem campo e sem operação. A escolha tem três consequências
deliberadas:

1. **A assinatura do contrato fica declarada e verificável agora.** O nome do tipo, a posição do
   parâmetro e a aridade do método são o que a tarefa exige, e nenhum deles depende da forma
   interna do tipo: o corpo de um `Protocol` é `...`.
2. **Distinção nominal preservada.** `NewType` mantém `PromptVersionado` e `EsquemaDeclarado`
   tipos distintos entre si, de modo que trocar um pelo outro na chamada é erro de tipo — o que
   não aconteceria com um apelido para `object`.
3. **A substituição é uma linha.** Quando o componente proprietário declarar o tipo de fato, a
   entrada sai daqui e o contrato passa a importá-lo do módulo dono, sem mudar assinatura.

Camada de núcleo: apenas declaração de tipo, sem implementação, sem import externo e sem entrada
e saída de dados.
"""

from __future__ import annotations

from typing import NewType

__all__ = [
    "ArquivoDeOferta",
    "CapacidadeDeModelo",
    "CoberturaDaFonte",
    "Coincidencia",
    "ColecaoDoIndiceVetorial",
    "ConfiguracaoDeAgendamento",
    "CursorDeCaptura",
    "EsquemaDeclarado",
    "ExecucaoDoRadar",
    "FiltroDeBusca",
    "IdentidadeDeEmbedding",
    "NomeDeColecao",
    "Notificacao",
    "OfertaBruta",
    "OrcamentoDeExecucaoDeIA",
    "PaginaDeCaptura",
    "PontoDeRetomada",
    "PromptVersionado",
    "ReferenciaDeOferta",
    "RepresentacaoVetorial",
    "RespostaDeModelo",
    "SaidaEstruturada",
    "SegmentoDeDocumento",
    "TrechoRecuperado",
]

# --- Componente 28 · provedores de modelo e de embedding (`R98`) -----------------------------

CapacidadeDeModelo = NewType("CapacidadeDeModelo", object)
"""Capacidades declaradas do modelo (`R98.1`): provedor, modelo, versão, limite de tokens de
entrada de `IA-005`, suporte a saída estruturada, suporte a ferramentas e os dois custos por mil
tokens."""

IdentidadeDeEmbedding = NewType("IdentidadeDeEmbedding", object)
"""Provedor, modelo, dimensões e versão do embedding (`R98.2`, `R100.3`). A dimensão é atributo
da representação vetorial, nunca do documento (`R102.6`)."""

RespostaDeModelo = NewType("RespostaDeModelo", object)
"""Resposta de completar texto, com tokens apurados e a marca de truncamento de `R99.9`."""

SaidaEstruturada = NewType("SaidaEstruturada", object)
"""Saída que satisfaz o esquema declarado, ou é rejeitada (`R105.6`)."""

EsquemaDeclarado = NewType("EsquemaDeclarado", object)
"""Esquema que a saída estruturada tem de satisfazer (`R98.1`, `R105.6`)."""

PromptVersionado = NewType("PromptVersionado", object)
"""Prompt com versão registrada (`R100`). Prompt sem versão não é reproduzível."""

OrcamentoDeExecucaoDeIA = NewType("OrcamentoDeExecucaoDeIA", object)
"""Orçamento por execução, em tokens (`IA-003`) e em moeda (`IA-004`) — `R99.2`."""

SegmentoDeDocumento = NewType("SegmentoDeDocumento", object)
"""Segmento com hash calculado e os treze metadados de `R101.2`."""

RepresentacaoVetorial = NewType("RepresentacaoVetorial", object)
"""Representação vetorial com provedor, modelo, dimensões, versão e data (`R100.3`)."""

# --- Componente 32 · índice vetorial (`R102`) ------------------------------------------------

NomeDeColecao = NewType("NomeDeColecao", object)
"""Nome de uma das três coleções de `R101.10`: conhecimento normativo, dados do imóvel e
histórico."""

TrechoRecuperado = NewType("TrechoRecuperado", object)
"""Trecho devolvido pela busca, com a citação que o torna resolvível (`R101.4`)."""

ColecaoDoIndiceVetorial = NewType("ColecaoDoIndiceVetorial", object)
"""Coleção com provedor, modelo, dimensões, versão, configuração de segmentação e data de
construção (`R102.9`)."""

# --- Componente 21 · conector de fonte (`R85`) -----------------------------------------------

FiltroDeBusca = NewType("FiltroDeBusca", object)
"""Filtro aplicado à listagem de ofertas da fonte (`R85.1`)."""

ReferenciaDeOferta = NewType("ReferenciaDeOferta", object)
"""Referência devolvida pela listagem e aceita pelas operações de detalhe (`R85.1`)."""

OfertaBruta = NewType("OfertaBruta", object)
"""Payload bruto, referência de origem, data e hora, hash, documentos, imagens e versão da
captura (`R85.2`)."""

ArquivoDeOferta = NewType("ArquivoDeOferta", object)
"""Arquivo entregue pela fonte, com o tipo declarado conforme `R86.4` (`R85.7`)."""

CoberturaDaFonte = NewType("CoberturaDaFonte", object)
"""Modalidades, estados, cidades, tipos de imóvel, campos entregues e campos não entregues
(`R85.1`)."""

# --- Componente 37 · estratégia de captura (`R107`) ------------------------------------------

CursorDeCaptura = NewType("CursorDeCaptura", object)
"""Posição da paginação de `AQ-006`, com o limite de itens de `AQ-007`."""

PaginaDeCaptura = NewType("PaginaDeCaptura", object)
"""Página obtida da fonte, já sujeita ao limite de tempo de `AQ-004`."""

PontoDeRetomada = NewType("PontoDeRetomada", object)
"""Ponto registrado a cada `AQ-012`, de onde a retomada parte (`R107.5`)."""

# --- Componente 40 · agendador (`R110`) e componente 48 · notificação (`R121`) ---------------

ConfiguracaoDeAgendamento = NewType("ConfiguracaoDeAgendamento", object)
"""Os dez atributos de agendamento por fonte (`R110.2`)."""

ExecucaoDoRadar = NewType("ExecucaoDoRadar", object)
"""Execução do Radar com os quinze campos de `R106.1`."""

Coincidencia = NewType("Coincidencia", object)
"""Registro de execução agendada que coincide com execução em curso da mesma fonte e por isso
**não** inicia (`R110.5`)."""

Notificacao = NewType("Notificacao", object)
"""Destinatário, assunto, conteúdo, prioridade, data e situação de entrega (`R121.2`)."""
