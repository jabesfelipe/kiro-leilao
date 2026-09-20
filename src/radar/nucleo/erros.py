"""Catálogo único de erro do produto e a taxonomia de exceções do Radar (`R114`, `D100`).

Componente 44 — Gestor de Erros, lado do núcleo. Aqui vive o **catálogo**: as 15 categorias de
`R114.2`, cada uma com o código estável `RAD-*`, a mensagem amigável em português e o contexto que
tem de ser registrado, exatamente como declarados na seção *Error Handling* do design. Este é o
**único** catálogo de erro do produto: catálogo paralelo é defeito, não alternativa (`R114.5`,
`D100`). As exigências anteriores — `R79.9` (valor fora de domínio informando campo e causa) e
`R97.5` (referência inexistente informando recurso e causa) — permanecem válidas e passam a ser
casos dele.

Três regras governam o módulo, e são as mesmas que governam o domínio:

1. **Nenhuma falha produz resultado favorável.** Um erro de entrada não vira zero, uma exceção não
   vira `REGULAR`, uma indisponibilidade não vira "verificado" e uma ausência de oferta não vira
   evidência de que a oferta não existe.
2. **Nenhuma mensagem apresentada ao usuário contém detalhe técnico** (`R114.3`): sem rastro de
   execução, sem consulta ao banco de dados, sem caminho de arquivo interno e sem mensagem de
   biblioteca. As mensagens deste módulo são as do catálogo, e nada mais.
3. **O contexto nunca inclui segredo nem payload íntegro de terceiro.** A construção que tenta
   carregá-los é rejeitada aqui, na raiz, não na fronteira.

A correspondência entre classe de exceção e categoria é **declarada como dado**
(`CATEGORIA_POR_CLASSE_DE_ERRO`), nunca deduzida por convenção de nome. Cinco classes têm a
categoria determinada **pela causa declarada** e não pela classe (`CATEGORIAS_ADMITIDAS_POR_CAUSA`):
para elas a categoria é obrigatória na construção.

O que **não** está aqui: o mapeamento para estado HTTP, a apresentação ao usuário e o registro da
ocorrência. São tradução na fronteira e vivem em `radar/plataforma/erros.py` — o núcleo não conhece
protocolo de transporte.

Camada de núcleo: valores imutáveis e funções puras, sem entrada e saída de dados, sem import de
cliente externo.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final, Literal
from uuid import UUID

from radar.nucleo.enumeracoes import EstadoDaCaptura
from radar.nucleo.enumeracoes_de_infraestrutura import CategoriaDeErro

__all__ = [
    "CATALOGO_DE_ERROS",
    "CATEGORIAS_ADMITIDAS_POR_CAUSA",
    "CATEGORIA_POR_CLASSE_DE_ERRO",
    "CHAVES_PROIBIDAS_NO_CONTEXTO",
    "FAMILIAS_DE_ERRO",
    "FAMILIA_DE_CAPACIDADE_E_INFRAESTRUTURA",
    "FAMILIA_DE_ENTRADA_E_CONTRATO",
    "FAMILIA_DE_EVIDENCIA_E_GOVERNANCA",
    "EntradaDoCatalogoDeErros",
    "ErroCatalogado",
    "ErroDeAutorizacaoDeFerramenta",
    "ErroDeCapturaInvalida",
    "ErroDeConfiguracaoAusente",
    "ErroDeConfiguracaoDeChecklist",
    "ErroDeConfiguracaoDeSupervisao",
    "ErroDeConsultaSemTitular",
    "ErroDeDisjuntorAberto",
    "ErroDeEntidadeAusenteNoDicionario",
    "ErroDeEntradaAmbigua",
    "ErroDeEvidenciaPosteriorADataDeCorte",
    "ErroDeEvidenciaSemFonte",
    "ErroDeExcecaoSobreBloqueio",
    "ErroDeExecucaoDoRadar",
    "ErroDeFonteAlterada",
    "ErroDeFonteIndisponivel",
    "ErroDeFronteiraDeEnum",
    "ErroDeIdempotenciaAusente",
    "ErroDeIntegridadeDeDocumento",
    "ErroDeNormalizadorNaoEncontrado",
    "ErroDeObtencaoDoConector",
    "ErroDeOperacaoNaoPermitida",
    "ErroDeOrcamentoDeIAAtingido",
    "ErroDeParametroPendenteDeDecisao",
    "ErroDeParametroSemVigencia",
    "ErroDePoliticaDeProcessamentoAusente",
    "ErroDePreCondicao",
    "ErroDePromocaoDeEvidencia",
    "ErroDeProvedorDeIA",
    "ErroDeRecuperacao",
    "ErroDeReferenciaInexistente",
    "ErroDeTempoExcedidoDeIA",
    "ErroDeUploadInvalido",
    "ErroDeValidacaoDeDominio",
    "ErroDeViolacaoDeImutabilidade",
    "ErroDoRadar",
    "FamiliaDeErro",
    "PendenciaDeCatalogacao",
    "RejeicaoDeCaptura",
    "catalogar",
    "categoria_de_erro",
    "entrada_do_catalogo",
]


# --------------------------------------------------------------------------------------
# As três famílias
# --------------------------------------------------------------------------------------

type FamiliaDeErro = Literal[
    "entrada e contrato", "evidência e governança", "capacidade e infraestrutura"
]

#: Família 1 — culpa do chamador: entrada inválida, referência inexistente, sessão ausente,
#: permissão ausente e arquivo inaceitável. Nada aqui degrada resultado de domínio.
FAMILIA_DE_ENTRADA_E_CONTRATO: Final[FamiliaDeErro] = "entrada e contrato"

#: Família 2 — violação de invariante e de governança: conflito de estado, leitura parcial de
#: documento, análise que não conclui e regra do produto contrariada. Sempre com registro na
#: trilha de auditoria.
FAMILIA_DE_EVIDENCIA_E_GOVERNANCA: Final[FamiliaDeErro] = "evidência e governança"

#: Família 3 — indisponibilidade de capacidade: fonte, execução do Radar, provedor de IA,
#: tempo excedido e recuperação. Indisponibilidade **não** degrada o resultado determinístico.
FAMILIA_DE_CAPACIDADE_E_INFRAESTRUTURA: Final[FamiliaDeErro] = "capacidade e infraestrutura"


@dataclass(frozen=True, slots=True, kw_only=True)
class EntradaDoCatalogoDeErros:
    """Uma linha do catálogo: categoria, código estável, mensagem amigável e contexto exigido.

    A mensagem é a que o usuário lê: diz o que aconteceu, o que fazer e nada mais (`R114.3`).
    `contexto_registrado` nomeia o que a ocorrência tem de registrar — é exigência de conteúdo,
    não texto apresentado.
    """

    categoria: CategoriaDeErro
    codigo: str
    mensagem_amigavel: str
    contexto_registrado: tuple[str, ...]
    familia: FamiliaDeErro

    def __post_init__(self) -> None:
        if not self.codigo.startswith("RAD-"):
            raise ValueError(
                f"código do catálogo tem de ser estável na forma RAD-NNN: {self.codigo!r}"
            )
        if not self.mensagem_amigavel.strip():
            raise ValueError(
                f"categoria {self.categoria} sem mensagem amigável; toda categoria tem uma "
                "(`R114.1`, `R114.9`)"
            )
        if not self.contexto_registrado:
            raise ValueError(f"categoria {self.categoria} sem contexto registrado (`R114.1`)")


def _catalogo() -> Mapping[CategoriaDeErro, EntradaDoCatalogoDeErros]:
    """As 15 categorias de `R114.2`, uma a uma, como declaradas em *Error Handling*."""
    entradas = (
        EntradaDoCatalogoDeErros(
            categoria=CategoriaDeErro.ERRO_DE_VALIDACAO,
            codigo="RAD-400",
            mensagem_amigavel=(
                "Um dos valores informados não é válido. Confira o campo indicado e tente "
                "novamente."
            ),
            contexto_registrado=("campo", "valor recusado", "regra de validação"),
            familia=FAMILIA_DE_ENTRADA_E_CONTRATO,
        ),
        EntradaDoCatalogoDeErros(
            categoria=CategoriaDeErro.NAO_ENCONTRADO,
            codigo="RAD-404",
            mensagem_amigavel="Não encontramos o item solicitado.",
            contexto_registrado=("recurso", "identificador procurado"),
            familia=FAMILIA_DE_ENTRADA_E_CONTRATO,
        ),
        EntradaDoCatalogoDeErros(
            categoria=CategoriaDeErro.CONFLITO,
            codigo="RAD-409",
            mensagem_amigavel="Esta operação conflita com o estado atual do registro.",
            contexto_registrado=("recurso", "estado atual", "estado exigido"),
            familia=FAMILIA_DE_EVIDENCIA_E_GOVERNANCA,
        ),
        EntradaDoCatalogoDeErros(
            categoria=CategoriaDeErro.NAO_AUTENTICADO,
            codigo="RAD-401",
            mensagem_amigavel="Sua sessão não está ativa. Entre novamente para continuar.",
            contexto_registrado=("operação", "ausência de credencial"),
            familia=FAMILIA_DE_ENTRADA_E_CONTRATO,
        ),
        EntradaDoCatalogoDeErros(
            categoria=CategoriaDeErro.NAO_AUTORIZADO,
            codigo="RAD-403",
            mensagem_amigavel="Você não tem permissão para esta operação.",
            contexto_registrado=("ator", "papel", "recurso", "titular"),
            familia=FAMILIA_DE_ENTRADA_E_CONTRATO,
        ),
        EntradaDoCatalogoDeErros(
            categoria=CategoriaDeErro.DOCUMENTO_INVALIDO,
            codigo="RAD-415",
            mensagem_amigavel="Este arquivo não pode ser aceito. Verifique o tipo e o tamanho.",
            contexto_registrado=(
                "verificação não satisfeita de R112.4",
                "tipo MIME",
                "tamanho",
            ),
            familia=FAMILIA_DE_ENTRADA_E_CONTRATO,
        ),
        EntradaDoCatalogoDeErros(
            categoria=CategoriaDeErro.ERRO_DE_PROCESSAMENTO_DE_DOCUMENTO,
            codigo="RAD-422",
            mensagem_amigavel=(
                "Não conseguimos ler todo o conteúdo deste documento. O arquivo original está "
                "preservado e a leitura ficou registrada como parcial."
            ),
            contexto_registrado=("documento", "versão", "etapa", "páginas não lidas"),
            familia=FAMILIA_DE_EVIDENCIA_E_GOVERNANCA,
        ),
        EntradaDoCatalogoDeErros(
            categoria=CategoriaDeErro.FONTE_INDISPONIVEL,
            codigo="RAD-503",
            mensagem_amigavel=(
                "A fonte de origem não respondeu agora. Os dados anteriores continuam válidos."
            ),
            contexto_registrado=("fonte", "conector", "causa", "disjuntor"),
            familia=FAMILIA_DE_CAPACIDADE_E_INFRAESTRUTURA,
        ),
        EntradaDoCatalogoDeErros(
            categoria=CategoriaDeErro.FONTE_ALTERADA,
            codigo="RAD-512",
            mensagem_amigavel=(
                "A fonte mudou de formato. A captura foi recusada para não corromper os dados, "
                "e a equipe foi notificada."
            ),
            contexto_registrado=(
                "fonte",
                "campos essenciais ausentes",
                "comparação com a última captura válida",
            ),
            familia=FAMILIA_DE_CAPACIDADE_E_INFRAESTRUTURA,
        ),
        EntradaDoCatalogoDeErros(
            categoria=CategoriaDeErro.ERRO_DE_EXECUCAO_DO_RADAR,
            codigo="RAD-513",
            mensagem_amigavel=(
                "A varredura não concluiu. O que já foi capturado está preservado e pode ser "
                "retomado."
            ),
            contexto_registrado=(
                "execução",
                "fonte",
                "ponto de retomada",
                "páginas não obtidas",
            ),
            familia=FAMILIA_DE_CAPACIDADE_E_INFRAESTRUTURA,
        ),
        EntradaDoCatalogoDeErros(
            categoria=CategoriaDeErro.ERRO_DE_PROVEDOR_DE_IA,
            codigo="RAD-521",
            mensagem_amigavel=(
                "A leitura assistida não está disponível agora. A análise determinística não é "
                "afetada."
            ),
            contexto_registrado=("tarefa", "provedor", "modelo", "causa"),
            familia=FAMILIA_DE_CAPACIDADE_E_INFRAESTRUTURA,
        ),
        EntradaDoCatalogoDeErros(
            categoria=CategoriaDeErro.TEMPO_EXCEDIDO_DE_IA,
            codigo="RAD-522",
            mensagem_amigavel=(
                "A leitura assistida demorou mais do que o previsto e foi interrompida."
            ),
            contexto_registrado=("etapa", "limite IA-006", "tentativas"),
            familia=FAMILIA_DE_CAPACIDADE_E_INFRAESTRUTURA,
        ),
        EntradaDoCatalogoDeErros(
            categoria=CategoriaDeErro.ERRO_DE_RECUPERACAO,
            codigo="RAD-523",
            mensagem_amigavel=(
                "Não foi possível consultar os documentos indexados. A análise segue sem essa "
                "etapa, e isso está registrado."
            ),
            contexto_registrado=("coleção", "consulta", "versão do embedding"),
            familia=FAMILIA_DE_CAPACIDADE_E_INFRAESTRUTURA,
        ),
        EntradaDoCatalogoDeErros(
            categoria=CategoriaDeErro.ERRO_DE_ANALISE,
            codigo="RAD-531",
            mensagem_amigavel=(
                "A análise não concluiu. Nenhuma decisão foi emitida e a execução está "
                "registrada como incompleta."
            ),
            contexto_registrado=("análise", "etapa", "causa", "pendência aberta"),
            familia=FAMILIA_DE_EVIDENCIA_E_GOVERNANCA,
        ),
        EntradaDoCatalogoDeErros(
            categoria=CategoriaDeErro.ERRO_DE_REGRA_DE_NEGOCIO,
            codigo="RAD-540",
            mensagem_amigavel=(
                "Esta operação contraria uma regra do produto. O motivo está descrito abaixo."
            ),
            contexto_registrado=("regra", "versão da regra", "motivo objetivo"),
            familia=FAMILIA_DE_EVIDENCIA_E_GOVERNANCA,
        ),
    )
    catalogo = {entrada.categoria: entrada for entrada in entradas}
    if len(catalogo) != len(CategoriaDeErro):
        faltantes = sorted(set(CategoriaDeErro) - set(catalogo))
        raise ValueError(
            f"o catálogo tem de declarar as {len(CategoriaDeErro)} categorias de `R114.2`, uma a "
            f"uma; sem entrada: {faltantes}"
        )
    return MappingProxyType(catalogo)


#: Catálogo único do produto: categoria → código, mensagem amigável e contexto exigido.
CATALOGO_DE_ERROS: Final[Mapping[CategoriaDeErro, EntradaDoCatalogoDeErros]] = _catalogo()

#: Família → as categorias que a compõem. A soma das três é o catálogo inteiro.
FAMILIAS_DE_ERRO: Final[Mapping[FamiliaDeErro, tuple[CategoriaDeErro, ...]]] = MappingProxyType(
    {
        familia: tuple(
            categoria
            for categoria, entrada in CATALOGO_DE_ERROS.items()
            if entrada.familia == familia
        )
        for familia in (
            FAMILIA_DE_ENTRADA_E_CONTRATO,
            FAMILIA_DE_EVIDENCIA_E_GOVERNANCA,
            FAMILIA_DE_CAPACIDADE_E_INFRAESTRUTURA,
        )
    }
)


def entrada_do_catalogo(categoria: CategoriaDeErro) -> EntradaDoCatalogoDeErros:
    """A linha do catálogo da categoria. Categoria sem linha é defeito, não caso de uso."""
    return CATALOGO_DE_ERROS[categoria]


# --------------------------------------------------------------------------------------
# A raiz da taxonomia
# --------------------------------------------------------------------------------------

#: Trecho de chave que jamais entra no contexto de um erro. O contexto explica **o que** falhou;
#: segredo e payload íntegro de terceiro não explicam nada e ampliam o dano de um vazamento.
CHAVES_PROIBIDAS_NO_CONTEXTO: Final[frozenset[str]] = frozenset(
    {
        "senha",
        "segredo",
        "token",
        "credencial",
        "autorizacao",
        "chave_de_api",
        "chave_privada",
        "payload",
        "corpo_da_resposta",
    }
)


def _validar_contexto(contexto: Mapping[str, object]) -> None:
    """Rejeita segredo e payload íntegro de terceiro antes de o erro existir."""
    for chave, valor in contexto.items():
        comparavel = chave.strip().lower()
        proibida = next(
            (trecho for trecho in sorted(CHAVES_PROIBIDAS_NO_CONTEXTO) if trecho in comparavel),
            None,
        )
        if proibida is not None:
            raise ValueError(
                f"contexto de erro não carrega segredo nem payload íntegro de terceiro; "
                f"chave {chave!r} contém {proibida!r}"
            )
        if isinstance(valor, bytes | bytearray | memoryview):
            raise TypeError(
                f"contexto de erro é estruturado, não conteúdo bruto; chave {chave!r} recebeu "
                "dado binário"
            )


def _resolver_pela_classe(
    classe: type[ErroDoRadar],
) -> tuple[CategoriaDeErro | None, tuple[CategoriaDeErro, ...] | None]:
    """Categoria declarada para a classe, ou as categorias admitidas conforme a causa."""
    for base in classe.__mro__:
        categoria = CATEGORIA_POR_CLASSE_DE_ERRO.get(base)
        if categoria is not None:
            return categoria, None
        admitidas = CATEGORIAS_ADMITIDAS_POR_CAUSA.get(base)
        if admitidas is not None:
            return None, admitidas
    return None, None


# N818 pede sufixo `Error`; o projeto nomeia erros com o prefixo `Erro` em português (`D72`,
# `D103`). O idioma prevalece sobre a convenção da ferramenta, e `MT-11` é quem julga o nome.
class ErroDoRadar(Exception):  # noqa: N818
    """Raiz da taxonomia. Carrega código estável, mensagem de negócio e contexto estruturado.

    O código e a mensagem **não** são escritos pelo chamador: vêm do catálogo único, pela
    categoria (`R114.5`, `D100`). A categoria vem da correspondência declarada em
    `CATEGORIA_POR_CLASSE_DE_ERRO`, ou da causa declarada na construção quando a classe está em
    `CATEGORIAS_ADMITIDAS_POR_CAUSA`. Subclasse fora das duas é defeito e falha na construção:
    catálogo paralelo não tem porta de entrada aqui.

    `str(erro)` é a mensagem amigável, e só ela. O contexto nunca inclui segredo nem payload
    íntegro de terceiros, e o detalhe técnico não mora aqui: vai para o log estruturado,
    associado ao identificador de correlação (`R114.4`).
    """

    categoria: CategoriaDeErro
    codigo: str
    mensagem_amigavel: str
    contexto: Mapping[str, object]
    detalhe_seguro: str

    def __init__(
        self,
        *,
        contexto: Mapping[str, object] | None = None,
        detalhe_seguro: str = "",
        categoria: CategoriaDeErro | None = None,
    ) -> None:
        declarada, admitidas = _resolver_pela_classe(type(self))
        nome = type(self).__name__
        if admitidas is not None:
            if categoria is None:
                raise ValueError(
                    f"`{nome}` tem a categoria determinada pela causa declarada; informe uma "
                    f"entre {[item.value for item in admitidas]}"
                )
            if categoria not in admitidas:
                raise ValueError(
                    f"`{nome}` admite apenas {[item.value for item in admitidas]} conforme a "
                    f"causa declarada; recebida {categoria.value}"
                )
        elif categoria is None:
            if declarada is None:
                raise ValueError(
                    f"`{nome}` não tem categoria declarada em `CATEGORIA_POR_CLASSE_DE_ERRO`; "
                    "erro sem categoria do catálogo único é defeito (`R114.5`, `D100`)"
                )
            categoria = declarada

        contexto_efetivo: Mapping[str, object] = {} if contexto is None else dict(contexto)
        _validar_contexto(contexto_efetivo)

        entrada = CATALOGO_DE_ERROS[categoria]
        self.categoria = categoria
        self.codigo = entrada.codigo
        self.mensagem_amigavel = entrada.mensagem_amigavel
        self.contexto = MappingProxyType(dict(contexto_efetivo))
        self.detalhe_seguro = detalhe_seguro
        super().__init__(entrada.mensagem_amigavel)


# --------------------------------------------------------------------------------------
# Família 1 — entrada e contrato
# --------------------------------------------------------------------------------------


class ErroDeValidacaoDeDominio(ErroDoRadar):
    """Valor fora de domínio. Nomeia o campo e a causa (`R79.9`)."""


class ErroDeFronteiraDeEnum(ErroDeValidacaoDeDominio):
    """Valor fora do enum na fronteira.

    `situacao_juridica` igual a "ok" minúsculo ou string vazia falha aqui, e **nunca** é tratado
    como liberado (`D.2.7`, `REG-022`, `P10.16`).
    """


class ErroDePreCondicao(ErroDeValidacaoDeDominio):
    """Pré-condição algébrica violada.

    Valor de mercado ≤ 0 (`R27.16`), prazo ≤ 0 (`R30.3.2`), `1 + r − t ≤ 0` (`R28.2`) e
    comparação fora de duas a cinco oportunidades (`R79.5`).
    """


class ErroDeEntradaAmbigua(ErroDeValidacaoDeDominio):
    """Entrada numericamente ambígua.

    Resulta em `DESCONHECIDO` no domínio, e em erro de entrada apenas quando o chamador exigiu
    valor (`R3.4.4`).
    """


class ErroDeReferenciaInexistente(ErroDeValidacaoDeDominio):
    """Requisição que referencia imóvel, oportunidade, documento, análise ou checklist inexistente.

    Informa o **recurso** e a **causa**, e nunca cria o recurso de forma implícita para atender à
    requisição (`R97.5`).
    """


# --------------------------------------------------------------------------------------
# Família 2 — evidência e governança
# --------------------------------------------------------------------------------------


class ErroDeEvidenciaSemFonte(ErroDoRadar):
    """Evidência sem fonte identificada (`R20.3`)."""


class ErroDePromocaoDeEvidencia(ErroDoRadar):
    """Tentativa de levar fato de `DESCONHECIDO` a `CONFIRMADO` sem evidência de suporte.

    `R20.4`, `SAFE-009`.
    """


class ErroDeViolacaoDeImutabilidade(ErroDoRadar):
    """Tentativa de alterar registro imutável.

    Snapshot, evidência, captura, documento, versão de documento, decisão ou trilha (`R20.5`,
    `R61.2`, `R64.3`, `R86.2`, `R87.1`). Espelha o gatilho do banco na camada de aplicação: a
    garantia é dupla, não delegada.
    """


class ErroDeOperacaoNaoPermitida(ErroDoRadar):
    """Tentativa de alterar captura, evidência ou versão de análise por operação exposta.

    A ausência da rota é a primeira barreira; esta exceção é a segunda, para o caso de chamada
    interna indevida (`R97.7`).
    """


class ErroDeParametroSemVigencia(ErroDoRadar):
    """Parâmetro sem versão vigente na data (`R62.11`)."""


class ErroDeParametroPendenteDeDecisao(ErroDoRadar):
    """Uso de parâmetro `[PENDENTE-DECISÃO]`.

    O requisito dependente é reportado como NÃO AVALIADO; o cálculo não prossegue com valor
    inventado (`R74.11`, `P16.3`).
    """


class ErroDeExcecaoSobreBloqueio(ErroDoRadar):
    """Exceção que tentaria contornar bloqueio jurídico ou risco crítico (`R63.4`, `R63.4.1`)."""


class ErroDeEntidadeAusenteNoDicionario(ErroDoRadar):
    """Regra que depende de entidade ou campo ausente do dicionário.

    A regra é rejeitada e o requisito é reportado como NÃO AVALIADO (`R74.11`).
    """


class ErroDeConfiguracaoDeChecklist(ErroDoRadar):
    """Configuração de checklist que enfraquece a versão 1.

    Remove, desativa ou torna não aplicável item **crítico** (`R92.5`), torna o resultado na
    ausência de evidência mais favorável do que o devido (`R92.6`) ou altera a precedência
    canônica de decisão de `R53` (`R92.11`). Nomeia o `item_id` e o motivo. A validação é na
    **carga** da configuração, não na execução: configuração inválida nunca chega a reger uma
    análise (`P17.16`, `REG-040`).
    """


class ErroDeIntegridadeDeDocumento(ErroDoRadar):
    """Hash recalculado do arquivo original difere do hash registrado.

    Registra falha de integridade, abre pendência de prioridade **crítica** e **impede**
    apresentar o conteúdo extraído como evidência enquanto a falha estiver aberta (`R86.8`). O
    arquivo não é substituído, corrigido nem removido: a divergência é fato registrado, e a
    extração derivada perde o status de prova, não o registro.
    """


# --------------------------------------------------------------------------------------
# Família 3 — capacidade e infraestrutura
# --------------------------------------------------------------------------------------


class ErroDeNormalizadorNaoEncontrado(ErroDoRadar):
    """Fonte sem normalizador registrado.

    Falha explícita, nunca despacho para o normalizador da CAIXA (`D.6.11`, `REG-030`).
    """


class ErroDeConfiguracaoDeSupervisao(ErroDoRadar):
    """Configuração que removeria ponto mínimo de intervenção humana (`R83.6`)."""


class ErroDeFonteIndisponivel(ErroDoRadar):
    """Fonte externa indisponível.

    Produz `DESCONHECIDO` com pendência, nunca ausência de risco (`SAFE-003`).
    """


class ErroDeObtencaoDoConector(ErroDeFonteIndisponivel):
    """Falha do `Conector_de_Fonte` na obtenção.

    Registra fonte, data, hora e causa, **preserva a última captura válida** e nunca registra
    ausência de oferta como evidência de inexistência da oferta (`R85.9`). A oferta não listada
    permanece `DESCONHECIDA`; nenhuma oportunidade é encerrada por silêncio da fonte.
    """


# --------------------------------------------------------------------------------------
# Os Domínios P a T, distribuídos pelas mesmas três famílias
# --------------------------------------------------------------------------------------
# Nenhuma falha de plataforma, de IA ou de aquisição produz resultado favorável, e nenhuma delas
# degrada o resultado determinístico. Cada classe abaixo cai em uma das três famílias pela
# categoria que a correspondência declarada lhe atribui.


class ErroDeProvedorDeIA(ErroDoRadar):
    """Falha de provedor de modelo de linguagem ou de embedding.

    Registra erro catalogado, mantém a execução retomável e **abstém-se** de emitir interpretação
    sem resposta do provedor (`R98.10`, `R103.6`).
    """


class ErroDeTempoExcedidoDeIA(ErroDeProvedorDeIA):
    """Limite de tempo `IA-006` excedido na etapa.

    Conta como tentativa; esgotadas as `IA-007` tentativas, a etapa vai para intervenção humana
    (`R103.3`, `R103.9`, `R105.7`).
    """


class ErroDeRecuperacao(ErroDoRadar):
    """Falha da etapa de recuperação.

    O workflow prossegue nas etapas que não dependem dela e a ausência do contexto recuperado é
    registrada como limitação declarada da execução (`R103.7`). Com o índice indisponível, o
    resultado determinístico **não muda** (`R102.8`, `P19.14`).
    """


class ErroDeOrcamentoDeIAAtingido(ErroDoRadar):
    """Orçamento de execução de IA atingido.

    Interrompe as chamadas, registra orçamento, consumo apurado e identificador de correlação,
    marca a execução como parcial e registra pendência. A interrupção é apresentada na interface e
    na trilha: nenhuma interrupção por custo permanece implícita (`R99.3`, `R99.4`, `P19.4`,
    `REG-055`).
    """


class ErroDeFonteAlterada(ErroDoRadar):
    """Estrutura da fonte difere da última captura válida além de `AQ-011`.

    Preserva o payload bruto, rejeita a captura nomeando a verificação não satisfeita, notifica por
    `R121.1` e **abstém-se** de registrar a mudança como ausência de oferta (`R107.2`, `R107.3`,
    `P20.6`, `REG-045`).
    """


class ErroDeCapturaInvalida(ErroDoRadar):
    """Captura que não satisfaz uma das seis verificações de `R107.1`.

    Estado `REJEITADA`, payload preservado, nada propagado ao domínio. Resposta vazia é inválida
    por quantidade implausível e **nunca** classifica oferta conhecida como removida da fonte
    (`R107.8`, `REG-046`).
    """


class ErroDeDisjuntorAberto(ErroDeFonteIndisponivel):
    """`AQ-008` falhas consecutivas abriram o disjuntor daquela fonte.

    Nenhuma nova chamada antes de `AQ-009`; a abertura fica registrada com data, hora e causa
    (`R107.7`, `P20.9`, `REG-060`).
    """


class ErroDeExecucaoDoRadar(ErroDoRadar):
    """Falha do ciclo do Radar.

    Preserva as capturas já registradas, registra o ponto de retomada e mantém a execução
    retomável (`R106.10`, `R107.5`).
    """


class ErroDeIdempotenciaAusente(ErroDeValidacaoDeDominio):
    """Operação crítica recebida sem chave de idempotência e sem chave natural derivável.

    Rejeitada informando a causa (`R109.6`).
    """


class ErroDeAutorizacaoDeFerramenta(ErroDoRadar):
    """Ferramenta de escrita invocada sem autorização, com entrada inválida ou sem idempotência.

    Rejeita informando a causa e **não produz efeito** (`R104.10`, `P19.18`, `REG-057`).
    """


class ErroDeUploadInvalido(ErroDeValidacaoDeDominio):
    """Upload que não satisfaz uma das quatro verificações de `R112.4`.

    Nome com travessia de caminho ou caminho absoluto é recusado, a tentativa é registrada com
    identificador de correlação e **nada é gravado** (`R112.5`, `R112.7`, `P21.4`, `REG-053`).
    """


class ErroDePoliticaDeProcessamentoAusente(ErroDoRadar):
    """Documento submetido a provedor sem política de processamento registrada para a sua classe.

    Recusa o envio, registra a recusa com identificador de correlação e abre pendência: nenhum
    conteúdo é transmitido (`R112.11`, `IA-014`, `P21.6`, `REG-052`).
    """


class ErroDeConfiguracaoAusente(ErroDoRadar):
    """Configuração obrigatória do ambiente ausente.

    **Impede a inicialização** do componente dependente e abstém-se de aplicar valor implícito
    (`R113.5`, `P21.8`).
    """


class ErroDeConsultaSemTitular(ErroDoRadar):
    """Consulta a entidade de negócio sem o identificador do titular.

    Rejeitada informando a causa, sem retornar dado (`R118.5`, `P21.17`, `REG-059`).
    """


class ErroDeEvidenciaPosteriorADataDeCorte(ErroDoRadar):
    """Evidência com data de observação posterior à data de corte da versão de análise.

    Recusada naquela versão, com a recusa registrada; a evidência permanece disponível para nova
    versão (`R120.4`, `R120.5`, `P21.21`, `REG-058`).
    """


# --------------------------------------------------------------------------------------
# A correspondência classe → categoria, declarada como dado
# --------------------------------------------------------------------------------------
# Declarada, não deduzida por convenção de nome: é o que permite renomear uma classe sem mudar a
# categoria apresentada, e mudar a categoria apresentada sem renomear classe alguma.

CATEGORIA_POR_CLASSE_DE_ERRO: Final[Mapping[type[ErroDoRadar], CategoriaDeErro]] = (
    MappingProxyType(
        {
            ErroDeValidacaoDeDominio: CategoriaDeErro.ERRO_DE_VALIDACAO,
            ErroDeFronteiraDeEnum: CategoriaDeErro.ERRO_DE_VALIDACAO,
            ErroDePreCondicao: CategoriaDeErro.ERRO_DE_VALIDACAO,
            ErroDeEntradaAmbigua: CategoriaDeErro.ERRO_DE_VALIDACAO,
            ErroDeReferenciaInexistente: CategoriaDeErro.NAO_ENCONTRADO,
            ErroDePromocaoDeEvidencia: CategoriaDeErro.CONFLITO,
            ErroDeViolacaoDeImutabilidade: CategoriaDeErro.CONFLITO,
            ErroDeParametroSemVigencia: CategoriaDeErro.CONFLITO,
            ErroDeParametroPendenteDeDecisao: CategoriaDeErro.CONFLITO,
            ErroDeExcecaoSobreBloqueio: CategoriaDeErro.CONFLITO,
            ErroDeEntidadeAusenteNoDicionario: CategoriaDeErro.CONFLITO,
            ErroDeOperacaoNaoPermitida: CategoriaDeErro.CONFLITO,
            ErroDeIntegridadeDeDocumento: CategoriaDeErro.DOCUMENTO_INVALIDO,
            ErroDeUploadInvalido: CategoriaDeErro.DOCUMENTO_INVALIDO,
            ErroDeFonteIndisponivel: CategoriaDeErro.FONTE_INDISPONIVEL,
            ErroDeObtencaoDoConector: CategoriaDeErro.FONTE_INDISPONIVEL,
            ErroDeDisjuntorAberto: CategoriaDeErro.FONTE_INDISPONIVEL,
            ErroDeCapturaInvalida: CategoriaDeErro.FONTE_INDISPONIVEL,
            ErroDeFonteAlterada: CategoriaDeErro.FONTE_ALTERADA,
            ErroDeExecucaoDoRadar: CategoriaDeErro.ERRO_DE_EXECUCAO_DO_RADAR,
            ErroDeProvedorDeIA: CategoriaDeErro.ERRO_DE_PROVEDOR_DE_IA,
            ErroDeOrcamentoDeIAAtingido: CategoriaDeErro.ERRO_DE_PROVEDOR_DE_IA,
            ErroDeTempoExcedidoDeIA: CategoriaDeErro.TEMPO_EXCEDIDO_DE_IA,
            ErroDeRecuperacao: CategoriaDeErro.ERRO_DE_RECUPERACAO,
            ErroDeConsultaSemTitular: CategoriaDeErro.NAO_AUTORIZADO,
            ErroDeAutorizacaoDeFerramenta: CategoriaDeErro.NAO_AUTORIZADO,
            ErroDeConfiguracaoAusente: CategoriaDeErro.ERRO_DE_REGRA_DE_NEGOCIO,
            ErroDePoliticaDeProcessamentoAusente: CategoriaDeErro.ERRO_DE_REGRA_DE_NEGOCIO,
            ErroDeEvidenciaPosteriorADataDeCorte: CategoriaDeErro.ERRO_DE_REGRA_DE_NEGOCIO,
        }
    )
)

_POR_CAUSA: Final[tuple[CategoriaDeErro, ...]] = (
    CategoriaDeErro.ERRO_DE_REGRA_DE_NEGOCIO,
    CategoriaDeErro.ERRO_DE_VALIDACAO,
)

#: Classes cuja categoria é `ERRO_DE_REGRA_DE_NEGOCIO` **ou** `ERRO_DE_VALIDACAO` conforme a causa
#: declarada. Para elas a categoria é obrigatória na construção: a causa é do chamador, não do
#: nome da classe.
CATEGORIAS_ADMITIDAS_POR_CAUSA: Final[
    Mapping[type[ErroDoRadar], tuple[CategoriaDeErro, ...]]
] = MappingProxyType(
    {
        ErroDeEvidenciaSemFonte: _POR_CAUSA,
        ErroDeConfiguracaoDeChecklist: _POR_CAUSA,
        ErroDeConfiguracaoDeSupervisao: _POR_CAUSA,
        ErroDeNormalizadorNaoEncontrado: _POR_CAUSA,
        ErroDeIdempotenciaAusente: _POR_CAUSA,
    }
)


def categoria_de_erro(erro: BaseException) -> CategoriaDeErro | None:
    """A categoria do erro, ou `None` quando ele **não** está catalogado (`R114.7`).

    `None` não é silêncio: é o que obriga a fronteira a apresentar falha interna com identificador
    de correlação e a abrir pendência de catalogação. Nenhuma ausência de categoria vira sucesso.
    """
    if isinstance(erro, ErroDoRadar):
        return erro.categoria
    return None


# --------------------------------------------------------------------------------------
# O erro catalogado e a pendência de catalogação
# --------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True, kw_only=True)
class ErroCatalogado:
    """Os **cinco** atributos de `R114.1`, mais a categoria que os determina.

    Código, mensagem amigável, contexto, identificador de correlação e detalhe seguro. O detalhe
    seguro é o que pode ser mostrado sem expor execução; o detalhe técnico fica no log estruturado,
    associado ao mesmo identificador (`R114.4`).
    """

    codigo: str
    mensagem_amigavel: str
    contexto: Mapping[str, object]
    identificador_de_correlacao: UUID
    detalhe_seguro: str
    categoria: CategoriaDeErro

    def __post_init__(self) -> None:
        if self.codigo != CATALOGO_DE_ERROS[self.categoria].codigo:
            raise ValueError(
                f"código {self.codigo!r} não é o da categoria {self.categoria}; o catálogo é "
                "único (`R114.5`, `D100`)"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class PendenciaDeCatalogacao:
    """Erro não catalogado: pendência aberta, nunca silêncio (`R114.7`).

    Nomeia a classe do erro para que a catalogação seja possível, e o identificador de correlação
    para que o detalhe técnico do log estruturado seja alcançável. A classe é registrada como
    **nome**, não como objeto: a pendência é registro, não referência viva de execução.
    """

    classe_do_erro: str
    identificador_de_correlacao: UUID

    def __post_init__(self) -> None:
        if not self.classe_do_erro.strip():
            raise ValueError("pendência de catalogação exige a classe do erro nomeada")


def catalogar(
    erro: BaseException,
    identificador_de_correlacao: UUID,
    *,
    detalhe_seguro: str = "",
) -> ErroCatalogado | PendenciaDeCatalogacao:
    """Classifica o erro em **exatamente uma** das 15 categorias, ou abre pendência (`P21.10`).

    Função pura: não apresenta, não registra e não traduz para protocolo. A apresentação e o
    registro são da fronteira (`R114.3`, `R114.8`); o resultado aqui é o valor que ela usa. Erro
    não catalogado devolve `PendenciaDeCatalogacao`, e é por isso que o caminho de ausência de
    categoria não tem como terminar em silêncio.
    """
    categoria = categoria_de_erro(erro)
    if categoria is None:
        return PendenciaDeCatalogacao(
            classe_do_erro=type(erro).__name__,
            identificador_de_correlacao=identificador_de_correlacao,
        )
    entrada = CATALOGO_DE_ERROS[categoria]
    contexto: Mapping[str, object] = erro.contexto if isinstance(erro, ErroDoRadar) else {}
    detalhe = detalhe_seguro
    if not detalhe and isinstance(erro, ErroDoRadar):
        detalhe = erro.detalhe_seguro
    return ErroCatalogado(
        codigo=entrada.codigo,
        mensagem_amigavel=entrada.mensagem_amigavel,
        contexto=contexto,
        identificador_de_correlacao=identificador_de_correlacao,
        detalhe_seguro=detalhe,
        categoria=categoria,
    )


# --------------------------------------------------------------------------------------
# Falha que é estado registrado, não exceção
# --------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True, kw_only=True)
class RejeicaoDeCaptura:
    """Resultado de captura reprovada no gate `G0` de `R4.1`. **Não é exceção: é registro.**

    O payload reprovado em `G0` vira captura com estado `REJEITADA` e a causa nomeada, e **não**
    cria oportunidade (`R85.8`). A captura rejeitada permanece: é o que permite auditar a cobertura
    real do conector e distinguir "a fonte não entregou preço" de "não havia oferta". O payload
    bruto é preservado de forma imutável antes de qualquer avaliação, inclusive neste caminho
    (`R85.6`, `R85.10`).

    O estado é `REJEITADA` por construção — rejeição que chegasse aqui com outro estado seria a
    própria falha que esta classe existe para impedir.
    """

    captura_id: UUID
    causa_de_rejeicao: str
    campos_ausentes: tuple[str, ...] = ()
    estado: EstadoDaCaptura = EstadoDaCaptura.REJEITADA

    def __post_init__(self) -> None:
        if self.estado is not EstadoDaCaptura.REJEITADA:
            raise ValueError(
                f"RejeicaoDeCaptura só existe com estado REJEITADA (recebido {self.estado}); "
                "reprovar em `G0` não cria oportunidade e não apaga a captura"
            )
        if not self.causa_de_rejeicao.strip():
            raise ValueError(
                "causa_de_rejeicao é obrigatória: a rejeição nomeia o campo ausente ou inválido "
                "(`R85.8`)"
            )
