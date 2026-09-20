"""Geradores da infraestrutura de IA — `P19` (`R98` a `R105`).

**Provedor de modelo e provedor de embedding entram nas propriedades apenas por dublê.** Cem
iterações contra provedor real custariam dinheiro e tornariam a suíte não determinística; o
provedor real é exercitado por integração com um a três exemplos e pela suíte de avaliação de IA
(`R105.8`). Os dublês daqui não abrem rede, não consomem crédito e não exigem chave: é isso que
sustenta a promessa de que as 262 propriedades rodam sem banco, sem rede e sem provedor.

**O que os dublês assumem sobre os contratos.** `ProvedorDeModeloDeLinguagem` e
`ProvedorDeEmbedding` serão declarados em `src/radar/nucleo/contratos/` pela tarefa 2.4 e ainda não
existem no disco. Para que o dublê os satisfaça quando aterrissarem, e sem importar módulo
inexistente, duas escolhas deliberadas:

1. os **nomes e a aridade** dos métodos são exatamente os do design — `completar`,
   `produzir_saida_estruturada`, `declarar_capacidade`, `gerar_representacao_vetorial`,
   `declarar_identidade`;
2. os parâmetros são anotados de forma **mais larga** que o contrato (`object`,
   `Mapping[str, object]`) e o retorno como `Any`. Parâmetro mais largo satisfaz contravariância
   e retorno `Any` é compatível com qualquer tipo de retorno declarado — de modo que nenhuma
   anotação daqui precisa mudar quando os tipos reais existirem.

Os dublês **registram toda chamada**, porque `R98.11` exige exatamente um registro por chamada e
`P19.3` verifica isso. Sem o registro no dublê, a propriedade não teria o que observar.

Camada de infraestrutura de teste: nenhuma entrada e saída de dados, nenhuma rede.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any, Final
from uuid import UUID

from hypothesis import strategies as st

from radar.nucleo.enumeracoes_de_infraestrutura import (
    CategoriaDeErro,
    NaturezaDaInformacao,
    SituacaoDeTrabalhoAssincrono,
)
from testes.geradores.escalas import FUSO_DE_BRASILIA, data_hora_br, escala_de_zero_a_cem

__all__ = [
    "ETAPAS_DO_WORKFLOW_DE_IA",
    "METADADOS_OBRIGATORIOS_DO_SEGMENTO",
    "PONTOS_DE_INTERVENCAO_HUMANA",
    "CapacidadeDubladaDeModelo",
    "DublaDeProvedorDeEmbedding",
    "DublaDeProvedorDeModeloDeLinguagem",
    "ErroDeProvedorDublado",
    "EstadoDeWorkflow",
    "GrafoDeImportacoes",
    "IdentidadeDubladaDeEmbedding",
    "InvocacaoDeFerramenta",
    "PontoDeInterrupcao",
    "PromptVersionado",
    "RegistroDeChamadaDublada",
    "RepresentacaoVetorialDublada",
    "RespostaDubladaDeModelo",
    "SaidaEstruturada",
    "SegmentoComMetadados",
    "dubla_de_provedor_de_embedding",
    "dubla_de_provedor_de_modelo",
    "estado_de_workflow",
    "grafo_de_importacoes",
    "invocacao_de_ferramenta",
    "ponto_de_interrupcao",
    "prompt_versionado",
    "saida_estruturada",
    "segmento_com_metadados",
]

METADADOS_OBRIGATORIOS_DO_SEGMENTO: Final[tuple[str, ...]] = (
    "documento",
    "versao_do_documento",
    "imovel",
    "oportunidade",
    "pagina",
    "trecho",
    "tipo",
    "data",
    "origem",
    "hash",
    "provedor_e_modelo_do_embedding",
    "versao_do_embedding",
    "versao_da_segmentacao",
)
"""Os treze metadados mínimos por segmento (`R101.2`, `P19.10`). A contagem é contrato."""

ETAPAS_DO_WORKFLOW_DE_IA: Final[tuple[str, ...]] = (
    "extracao",
    "limpeza",
    "segmentacao",
    "atribuicao_de_metadados",
    "geracao_de_representacao_vetorial",
    "indexacao",
    "busca",
    "reordenacao",
    "montagem_de_contexto",
    "entrega_ao_componente_de_linguagem",
    "persistencia",
)
"""As onze etapas do workflow de IA (`R103.1`), na ordem. Cada uma tem ponto de retomada."""

PONTOS_DE_INTERVENCAO_HUMANA: Final[tuple[str, ...]] = (
    "promocao_de_evidencia",
    "aceite_de_risco",
    "autorizacao_de_excecao",
    "revisao_de_extracao",
    "aprovacao_de_configuracao_de_checklist",
    "confirmacao_de_lance",
    "encerramento_de_pendencia",
)
"""Os sete pontos de intervenção humana registrada (`R103`). Intervenção sem registro é defeito."""

_CATEGORIAS_DE_FALHA_DE_IA: Final[tuple[CategoriaDeErro, ...]] = (
    CategoriaDeErro.ERRO_DE_PROVEDOR_DE_IA,
    CategoriaDeErro.TEMPO_EXCEDIDO_DE_IA,
    CategoriaDeErro.ERRO_DE_RECUPERACAO,
)

# Data fixa e consciente de fuso para a representação vetorial do dublê: o dublê é determinístico,
# e um relógio real tornaria dois vetores iguais em valor mas diferentes em registro.
_GERADO_EM: Final[datetime] = datetime(2024, 1, 1, 12, 0, 0, tzinfo=FUSO_DE_BRASILIA)


# --------------------------------------------------------------------------------------
# Dados de ida e volta dos dublês
# --------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True, kw_only=True)
class PromptVersionado:
    """Prompt com versão registrada (`R100`). Prompt sem versão não é reproduzível."""

    identificador: str
    versao: str
    tarefa: str
    texto: str


def prompt_versionado() -> st.SearchStrategy[PromptVersionado]:
    """Prompt versionado, com versões distintas do mesmo identificador no espaço de geração.

    Mudar a versão do prompt **não** altera interpretação já persistida (`P19.8`): gerar mais de
    uma versão do mesmo prompt é o que torna a imutabilidade verificável.
    """
    return st.builds(
        PromptVersionado,
        identificador=st.sampled_from(
            ("extracao-de-matricula", "classificacao-de-documento", "analise-de-edital")
        ),
        versao=st.sampled_from(("1.0.0", "1.1.0", "2.0.0")),
        tarefa=st.sampled_from(("classificacao", "extracao", "analise")),
        texto=st.text(min_size=1, max_size=120),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class CapacidadeDubladaDeModelo:
    """Capacidade declarada pelo dublê, com os oito atributos do design (`R98.1`).

    O chamador decide o que pedir a partir daqui, em lugar de descobrir por erro em produção.
    `limite_de_tokens_de_entrada` respeita `IA-005` (32.000).
    """

    provedor: str
    modelo: str
    versao: str
    limite_de_tokens_de_entrada: int
    suporta_saida_estruturada: bool
    suporta_ferramentas: bool
    custo_por_mil_tokens_de_entrada: Decimal
    custo_por_mil_tokens_de_saida: Decimal


@dataclass(frozen=True, slots=True, kw_only=True)
class IdentidadeDubladaDeEmbedding:
    """Provedor, modelo, dimensões e versão (`R98.2`, `R100.3`).

    A dimensão é atributo da representação vetorial, nunca do documento (`R102.6`).
    """

    provedor: str
    modelo: str
    dimensoes: int
    versao: str


@dataclass(frozen=True, slots=True, kw_only=True)
class RespostaDubladaDeModelo:
    """Resposta do dublê: texto, contagem de tokens e a marca de truncamento de `R99.9`."""

    texto: str
    tokens_de_entrada: int
    tokens_de_saida: int
    truncada: bool


@dataclass(frozen=True, slots=True, kw_only=True)
class SaidaEstruturada:
    """Saída estruturada com a natureza declarada e a citação que a sustenta (`R101.5`).

    `conforme_o_esquema=False` é o caso que a fronteira anti-alucinação tem de rejeitar: saída que
    não satisfaz o esquema declarado não vira interpretação (`R105.6`).
    """

    campos: Mapping[str, str]
    conforme_o_esquema: bool
    natureza: NaturezaDaInformacao
    citacao_resolvivel: bool


def saida_estruturada() -> st.SearchStrategy[SaidaEstruturada]:
    """Saída estruturada, incluindo a não conforme e a de citação não resolvível.

    Trecho sem citação resolvível é descartado do contexto e não apoia interpretação (`R101.4`);
    nenhum item acumula mais de uma natureza (`P19.11`), e por isso a natureza é um enum, não um
    conjunto.
    """
    return st.builds(
        SaidaEstruturada,
        campos=st.dictionaries(
            keys=st.sampled_from(("proprietario", "area", "gravame", "data_do_ato")),
            values=st.text(min_size=0, max_size=40),
            min_size=0,
            max_size=4,
        ),
        conforme_o_esquema=st.booleans(),
        natureza=st.sampled_from(NaturezaDaInformacao),
        citacao_resolvivel=st.booleans(),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class RepresentacaoVetorialDublada:
    """Representação vetorial devolvida pelo dublê, com identidade e dimensão próprias."""

    vetor: tuple[Decimal, ...]
    identidade: IdentidadeDubladaDeEmbedding
    gerada_em: datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class RegistroDeChamadaDublada:
    """Registro de uma chamada ao dublê — o análogo de `RegistroDeChamadaAProvedor`.

    Existe porque `R98.11` exige **exatamente um** registro por chamada e `P19.3` o verifica. O
    dublê acumula os registros em ordem; a propriedade conta.
    """

    tarefa: str
    provedor: str
    modelo: str
    versao: str
    tokens_de_entrada: int
    tokens_de_saida: int
    truncada: bool


# N818 pede sufixo `Error`; o projeto nomeia erros com o prefixo `Erro` em português (`D72`,
# `D103`), como `ErroDoRadar` e `ErroDeValidacaoDeDominio`. O idioma prevalece sobre a convenção
# da ferramenta.
class ErroDeProvedorDublado(RuntimeError):  # noqa: N818
    """Falha simulada de provedor, sempre com categoria do catálogo único de erro (`R114.2`).

    Indisponibilidade ou excesso de `IA-006` registra erro catalogado, mantém a execução retomável
    e **não** produz interpretação (`R98.10`, `R103.6`). O dublê levanta este erro para que a
    propriedade veja o caminho de falha sem depender de rede instável.
    """

    def __init__(self, categoria: CategoriaDeErro) -> None:
        super().__init__(f"falha simulada de provedor: {categoria}")
        self.categoria = categoria


@dataclass(slots=True, kw_only=True)
class DublaDeProvedorDeModeloDeLinguagem:
    """Dublê do contrato `ProvedorDeModeloDeLinguagem` — sem rede, sem crédito, sem chave.

    Satisfaz o contrato pelos nomes e pela aridade dos três métodos do design. Os parâmetros são
    anotados como `object` e o retorno como `Any` de propósito: parâmetro mais largo satisfaz a
    contravariância do `Protocol` e retorno `Any` é compatível com o tipo de retorno declarado,
    de modo que nada aqui muda quando `radar.nucleo.contratos` aterrissar.
    """

    capacidade: CapacidadeDubladaDeModelo
    resposta: RespostaDubladaDeModelo
    saida: SaidaEstruturada
    falha: CategoriaDeErro | None = None
    chamadas: list[RegistroDeChamadaDublada] = field(default_factory=list)

    def _registrar(self, tarefa: str) -> None:
        self.chamadas.append(
            RegistroDeChamadaDublada(
                tarefa=tarefa,
                provedor=self.capacidade.provedor,
                modelo=self.capacidade.modelo,
                versao=self.capacidade.versao,
                tokens_de_entrada=self.resposta.tokens_de_entrada,
                tokens_de_saida=self.resposta.tokens_de_saida,
                truncada=self.resposta.truncada,
            )
        )

    def completar(
        self,
        prompt: object,
        entrada: Mapping[str, object],
        orcamento: object,
    ) -> Any:
        """Completa texto. Registra a chamada **antes** de decidir se falha."""
        del prompt, entrada, orcamento
        self._registrar("completar")
        if self.falha is not None:
            raise ErroDeProvedorDublado(self.falha)
        return self.resposta

    def produzir_saida_estruturada(
        self,
        prompt: object,
        entrada: Mapping[str, object],
        esquema: object,
        orcamento: object,
    ) -> Any:
        """Produz saída estruturada. A conformidade com o esquema é dada, não presumida."""
        del prompt, entrada, esquema, orcamento
        self._registrar("produzir_saida_estruturada")
        if self.falha is not None:
            raise ErroDeProvedorDublado(self.falha)
        return self.saida

    def declarar_capacidade(self) -> Any:
        """Capacidade declarada. Consultar capacidade não é chamada a provedor: não registra."""
        return self.capacidade


@dataclass(slots=True, kw_only=True)
class DublaDeProvedorDeEmbedding:
    """Dublê do contrato `ProvedorDeEmbedding` — determinístico e sem rede.

    O vetor é derivado do hash do segmento, e não sorteado a cada chamada: o mesmo segmento produz
    o mesmo vetor. Sem determinismo, a propriedade de reconstrução do índice (`P19.12`) não teria
    como distinguir mudança de resultado de ruído do dublê.
    """

    identidade: IdentidadeDubladaDeEmbedding
    falha: CategoriaDeErro | None = None
    chamadas: list[RegistroDeChamadaDublada] = field(default_factory=list)

    def gerar_representacao_vetorial(self, segmento: object) -> Any:
        """Gera representação vetorial determinística a partir do texto do segmento."""
        self.chamadas.append(
            RegistroDeChamadaDublada(
                tarefa="gerar_representacao_vetorial",
                provedor=self.identidade.provedor,
                modelo=self.identidade.modelo,
                versao=self.identidade.versao,
                tokens_de_entrada=0,
                tokens_de_saida=0,
                truncada=False,
            )
        )
        if self.falha is not None:
            raise ErroDeProvedorDublado(self.falha)
        digesto = hashlib.sha256(repr(segmento).encode("utf-8")).digest()
        vetor = tuple(
            Decimal(digesto[posicao % len(digesto)]) / Decimal(256)
            for posicao in range(self.identidade.dimensoes)
        )
        return RepresentacaoVetorialDublada(
            vetor=vetor,
            identidade=self.identidade,
            gerada_em=_GERADO_EM,
        )

    def declarar_identidade(self) -> Any:
        """Provedor, modelo, dimensões e versão. Consulta de identidade não é chamada."""
        return self.identidade


def dubla_de_provedor_de_modelo() -> st.SearchStrategy[DublaDeProvedorDeModeloDeLinguagem]:
    """Dublê de provedor de modelo, incluindo o que falha com erro catalogado.

    Metade do espaço tem `falha=None` e metade tem uma categoria de erro do catálogo único: a
    propriedade que exige execução retomável e ausência de interpretação em falha precisa dos dois
    caminhos.
    """
    return st.builds(
        DublaDeProvedorDeModeloDeLinguagem,
        capacidade=st.builds(
            CapacidadeDubladaDeModelo,
            provedor=st.sampled_from(("dublê-openai", "dublê-local")),
            modelo=st.sampled_from(("modelo-economico", "modelo-de-maior-capacidade")),
            versao=st.sampled_from(("1.0.0", "2.0.0")),
            limite_de_tokens_de_entrada=st.sampled_from((8_000, 32_000)),
            suporta_saida_estruturada=st.booleans(),
            suporta_ferramentas=st.booleans(),
            custo_por_mil_tokens_de_entrada=st.sampled_from(
                (Decimal("0.0000"), Decimal("0.0150"))
            ),
            custo_por_mil_tokens_de_saida=st.sampled_from(
                (Decimal("0.0000"), Decimal("0.0600"))
            ),
        ),
        resposta=st.builds(
            RespostaDubladaDeModelo,
            texto=st.text(min_size=0, max_size=200),
            tokens_de_entrada=st.integers(min_value=0, max_value=32_000),
            tokens_de_saida=st.integers(min_value=0, max_value=4_000),
            truncada=st.booleans(),
        ),
        saida=saida_estruturada(),
        falha=st.one_of(st.none(), st.sampled_from(_CATEGORIAS_DE_FALHA_DE_IA)),
    )


def dubla_de_provedor_de_embedding() -> st.SearchStrategy[DublaDeProvedorDeEmbedding]:
    """Dublê de provedor de embedding, com dimensão variável e falha catalogada opcional.

    A dimensão varia de propósito: trocar de modelo muda a dimensão, e a migração de representação
    vetorial (`R102.4`) é justamente o que exige que a dimensão pertença à representação e não ao
    documento.
    """
    return st.builds(
        DublaDeProvedorDeEmbedding,
        identidade=st.builds(
            IdentidadeDubladaDeEmbedding,
            provedor=st.sampled_from(("dublê-openai", "dublê-local")),
            modelo=st.sampled_from(("embedding-pequeno", "embedding-grande")),
            dimensoes=st.sampled_from((4, 8, 16)),
            versao=st.sampled_from(("1.0.0", "2.0.0")),
        ),
        falha=st.one_of(st.none(), st.sampled_from(_CATEGORIAS_DE_FALHA_DE_IA)),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class SegmentoComMetadados:
    """Segmento com os treze metadados obrigatórios de `R101.2`."""

    texto: str
    hash_do_segmento: str
    metadados: Mapping[str, str]


def segmento_com_metadados() -> st.SearchStrategy[SegmentoComMetadados]:
    """Segmento com os treze metadados **sempre** presentes, alguns possivelmente em branco.

    Chave sempre presente e valor possivelmente vazio é deliberado: é o que separa a propriedade
    "os treze estão preenchidos" (`P19.10`) da propriedade "os treze existem". Se o gerador nunca
    produzisse valor vazio, a primeira passaria por acidente.
    """
    return st.builds(
        SegmentoComMetadados,
        texto=st.text(min_size=1, max_size=200),
        hash_do_segmento=st.text(alphabet="0123456789abcdef", min_size=64, max_size=64),
        metadados=st.fixed_dictionaries(
            dict.fromkeys(METADADOS_OBRIGATORIOS_DO_SEGMENTO, st.text(min_size=0, max_size=30))
        ),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class EstadoDeWorkflow:
    """Estado explícito de um workflow de IA, com ponto de retomada por etapa (`R103`)."""

    execucao: UUID
    etapa_atual: str
    etapas_concluidas: tuple[str, ...]
    tentativas: int
    situacao: SituacaoDeTrabalhoAssincrono
    versao_do_grafo: str
    chave_de_idempotencia: str


def estado_de_workflow() -> st.SearchStrategy[EstadoDeWorkflow]:
    """Estado de workflow com prefixo coerente de etapas concluídas.

    As etapas concluídas são sempre um **prefixo** da ordem canônica: workflow que tivesse
    concluído a indexação sem ter segmentado não é um estado alcançável, e gerá-lo produziria
    contraexemplos que só provam que o gerador está errado.
    """
    return st.builds(
        _estado_de_workflow_coerente,
        execucao=st.uuids(),
        quantidade_concluida=st.integers(min_value=0, max_value=len(ETAPAS_DO_WORKFLOW_DE_IA)),
        tentativas=st.integers(min_value=0, max_value=3),
        situacao=st.sampled_from(SituacaoDeTrabalhoAssincrono),
        versao_do_grafo=st.sampled_from(("1.0.0", "1.1.0")),
        chave_de_idempotencia=st.text(min_size=1, max_size=32),
    )


def _estado_de_workflow_coerente(
    *,
    execucao: UUID,
    quantidade_concluida: int,
    tentativas: int,
    situacao: SituacaoDeTrabalhoAssincrono,
    versao_do_grafo: str,
    chave_de_idempotencia: str,
) -> EstadoDeWorkflow:
    concluidas = ETAPAS_DO_WORKFLOW_DE_IA[:quantidade_concluida]
    restantes = ETAPAS_DO_WORKFLOW_DE_IA[quantidade_concluida:]
    etapa_atual = restantes[0] if restantes else ETAPAS_DO_WORKFLOW_DE_IA[-1]
    return EstadoDeWorkflow(
        execucao=execucao,
        etapa_atual=etapa_atual,
        etapas_concluidas=concluidas,
        tentativas=tentativas,
        situacao=situacao,
        versao_do_grafo=versao_do_grafo,
        chave_de_idempotencia=chave_de_idempotencia,
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class PontoDeInterrupcao:
    """Ponto de intervenção humana registrada, com autor e decisão (`R103`)."""

    ponto: str
    autor: str
    decidido_em: datetime
    decisao_registrada: bool


def ponto_de_interrupcao() -> st.SearchStrategy[PontoDeInterrupcao]:
    """Ponto de interrupção nos sete pontos declarados, com e sem decisão registrada."""
    return st.builds(
        PontoDeInterrupcao,
        ponto=st.sampled_from(PONTOS_DE_INTERVENCAO_HUMANA),
        autor=st.text(min_size=1, max_size=30),
        decidido_em=data_hora_br(),
        decisao_registrada=st.booleans(),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class InvocacaoDeFerramenta:
    """Invocação de ferramenta pelo servidor de ferramentas (`R104`, `R105`).

    `de_escrita` separa os dois catálogos: toda escrita exige autorização, validação de esquema,
    idempotência e auditoria, e a leitura não.
    """

    ferramenta: str
    de_escrita: bool
    autorizada: bool
    esquema_satisfeito: bool
    chave_de_idempotencia: str
    confianca_da_saida: Decimal


def invocacao_de_ferramenta() -> st.SearchStrategy[InvocacaoDeFerramenta]:
    """Invocação de ferramenta, de leitura e de escrita, autorizada e não autorizada."""
    return st.builds(
        InvocacaoDeFerramenta,
        ferramenta=st.sampled_from(
            ("consultar_evidencia", "registrar_pendencia", "obter_documento", "gravar_analise")
        ),
        de_escrita=st.booleans(),
        autorizada=st.booleans(),
        esquema_satisfeito=st.booleans(),
        chave_de_idempotencia=st.text(min_size=1, max_size=32),
        confianca_da_saida=escala_de_zero_a_cem(),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class GrafoDeImportacoes:
    """Grafo de importação entre as três camadas de `R119` (`MT-10`).

    As arestas são pares `(origem, destino)` de camada. Importação do núcleo para adaptador ou
    para infraestrutura é a aresta proibida, e o gerador a produz de propósito: `MT-10` existe
    para recusá-la, não para supô-la ausente.
    """

    arestas: tuple[tuple[str, str], ...]


def grafo_de_importacoes() -> st.SearchStrategy[GrafoDeImportacoes]:
    """Grafo de importações entre `nucleo`, `adaptadores` e `infraestrutura`."""
    camadas = ("nucleo", "adaptadores", "infraestrutura")
    aresta = st.tuples(st.sampled_from(camadas), st.sampled_from(camadas))
    return st.builds(
        GrafoDeImportacoes,
        arestas=st.lists(aresta, min_size=0, max_size=9, unique=True).map(tuple),
    )
