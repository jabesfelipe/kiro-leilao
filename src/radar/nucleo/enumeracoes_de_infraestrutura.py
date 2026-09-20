"""Os 7 enums de infraestrutura e de plataforma dos Domínios P a T.

Nenhum deles participa de cálculo de negócio, de escore, de decisão ou de precedência: são
vocabulários de execução, de captura, de erro, de trabalho assíncrono e de apresentação. Vivem
em módulo separado dos 60 enums de negócio exatamente para que essa fronteira seja visível —
contá-los junto foi o que permitiu, no passado, que detalhe de aquisição vazasse para o
domínio.

As contagens são igualmente contrato e são verificadas por `MT-09` junto com as dos enums de
negócio. Os nomes seguem a tabela de correspondência de rótulos normativos (`D72`) e as
correspondências obrigatórias de `D103`; `ENDPOINT` é o identificador declarado pelo próprio
projeto para a estratégia de captura correspondente.

Camada de núcleo: sem import externo, sem entrada e saída de dados.
"""

from __future__ import annotations

from enum import StrEnum

__all__ = [
    "CategoriaDeErro",
    "EstadoDaOfertaNaFonte",
    "EstadoDeTela",
    "EstrategiaDeCaptura",
    "NaturezaDaInformacao",
    "SituacaoDeExecucaoDoRadar",
    "SituacaoDeTrabalhoAssincrono",
]


class SituacaoDeExecucaoDoRadar(StrEnum):
    """As 6 situações de uma Execução do Radar (`R106.4`)."""

    EM_EXECUCAO = "EM_EXECUCAO"
    CONCLUIDA = "CONCLUIDA"
    CONCLUIDA_COM_ERRO = "CONCLUIDA_COM_ERRO"
    PARCIAL = "PARCIAL"
    INTERROMPIDA = "INTERROMPIDA"
    FALHA = "FALHA"


class EstadoDaOfertaNaFonte(StrEnum):
    """Os 6 estados da oferta na fonte (`R108.2`).

    Toda oferta capturada recebe exatamente um (`P20.11`).
    """

    NOVA = "NOVA"
    ATUALIZADA = "ATUALIZADA"
    SEM_ALTERACAO = "SEM_ALTERACAO"
    REMOVIDA_DA_FONTE = "REMOVIDA_DA_FONTE"
    INVALIDA = "INVALIDA"
    INCONCLUSIVA = "INCONCLUSIVA"


class EstrategiaDeCaptura(StrEnum):
    """As 4 estratégias de captura (`R106.1`, `R107.4` a `R107.11`, `D94`).

    É **invisível ao domínio**: aparece na Execução do Radar e na captura, e em nenhuma entidade
    de negócio, regra, parâmetro de negócio ou motor (`R85.3`, `R106.8`, `P20.4`). Payload igual
    obtido por estratégias diferentes produz resultado idêntico (`P17.20`).
    """

    PAGINA_PUBLICA = "PAGINA_PUBLICA"
    ENDPOINT = "ENDPOINT"
    ARQUIVO = "ARQUIVO"
    VARREDURA = "VARREDURA"


class CategoriaDeErro(StrEnum):
    """As 15 categorias do catálogo único de erro (`R114.2`, `D100`).

    Três famílias: entrada e contrato; evidência e governança; capacidade e infraestrutura.
    Catálogo paralelo é defeito, não alternativa (`R114.5`); erro não catalogado é apresentado
    como falha interna com identificador de correlação e abre pendência de catalogação
    (`R114.7`).
    """

    ERRO_DE_VALIDACAO = "ERRO_DE_VALIDACAO"
    NAO_ENCONTRADO = "NAO_ENCONTRADO"
    CONFLITO = "CONFLITO"
    NAO_AUTENTICADO = "NAO_AUTENTICADO"
    NAO_AUTORIZADO = "NAO_AUTORIZADO"
    DOCUMENTO_INVALIDO = "DOCUMENTO_INVALIDO"
    ERRO_DE_PROCESSAMENTO_DE_DOCUMENTO = "ERRO_DE_PROCESSAMENTO_DE_DOCUMENTO"
    FONTE_INDISPONIVEL = "FONTE_INDISPONIVEL"
    FONTE_ALTERADA = "FONTE_ALTERADA"
    ERRO_DE_EXECUCAO_DO_RADAR = "ERRO_DE_EXECUCAO_DO_RADAR"
    ERRO_DE_PROVEDOR_DE_IA = "ERRO_DE_PROVEDOR_DE_IA"
    TEMPO_EXCEDIDO_DE_IA = "TEMPO_EXCEDIDO_DE_IA"
    ERRO_DE_RECUPERACAO = "ERRO_DE_RECUPERACAO"
    ERRO_DE_ANALISE = "ERRO_DE_ANALISE"
    ERRO_DE_REGRA_DE_NEGOCIO = "ERRO_DE_REGRA_DE_NEGOCIO"


class SituacaoDeTrabalhoAssincrono(StrEnum):
    """As 6 situações de trabalho assíncrono (`R115.4`).

    A situação nunca regride de concluída para em execução (`P21.12`).
    """

    ENFILEIRADO = "ENFILEIRADO"
    EM_EXECUCAO = "EM_EXECUCAO"
    CONCLUIDO = "CONCLUIDO"
    CONCLUIDO_COM_ERRO = "CONCLUIDO_COM_ERRO"
    INTERROMPIDO = "INTERROMPIDO"
    FALHA = "FALHA"


class EstadoDeTela(StrEnum):
    """Os 9 estados de tela (`R122.1`).

    Toda tela e todo componente que dependa de dado remoto declara os nove (`MT-16`, `P22.1`).
    `DADO_OBSOLETO` é o dado obsoleto de `R122.6`, e `ESQUELETO` é o esqueleto de `D103`.
    """

    CARREGANDO = "CARREGANDO"
    ESQUELETO = "ESQUELETO"
    VAZIO = "VAZIO"
    ERRO = "ERRO"
    REPETICAO = "REPETICAO"
    PARCIAL = "PARCIAL"
    DADO_OBSOLETO = "DADO_OBSOLETO"
    CONFIRMACAO = "CONFIRMACAO"
    SUCESSO = "SUCESSO"


class NaturezaDaInformacao(StrEnum):
    """As 4 naturezas da informação apresentada (`R101.5`, `R123.4`).

    `R101.5` declara três naturezas da informação produzida e `R123.4` acrescenta `PENDENTE`
    como a quarta natureza apresentável. Nenhum item acumula mais de uma (`P19.11`, `P22.5`).
    """

    FATO_DO_DOCUMENTO = "FATO_DO_DOCUMENTO"
    INTERPRETACAO_DA_IA = "INTERPRETACAO_DA_IA"
    RESULTADO_DETERMINISTICO = "RESULTADO_DETERMINISTICO"
    PENDENTE = "PENDENTE"
