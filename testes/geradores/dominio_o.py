"""Geradores do Domínio O — documento, versão, checklist, débito, processo e porta (`R84` a `R96`).

Sem estes geradores, `P17.1` a `P17.22` viram inspeção manual. Três deles carregam valor de
fronteira obrigatório e por isso merecem leitura atenta:

- `versao_de_documento()` e `par_de_versoes_de_analise()` começam na versão **1** e são contíguas,
  sem lacuna (`R87.1`, `P17.7`, `P13.2`);
- `par_de_versoes_de_analise()` produz, deliberadamente, o **par idêntico**: a comparação é vazia
  se e somente se as versões são idênticas (`P17.9`);
- `documento()` produz o caso de **hash divergente** do registrado, que é falha de integridade com
  pendência crítica e impedimento de uso do conteúdo extraído (`R86.7`, `R86.8`).

Camada de infraestrutura de teste: nenhuma entrada e saída de dados.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Final
from uuid import UUID

from hypothesis import strategies as st

from radar.nucleo.enumeracoes import (
    CategoriaDeDiferenca,
    EstadoDeDecisao,
    OrigemDeDocumento,
    PortaDeEntrada,
    PotencialPreliminar,
    ResponsabilidadePeloDebito,
    ResultadoDeItemDeChecklist,
    ResultadoDeTriagem,
    SituacaoDeDebito,
    SituacaoDeProcesso,
    TipoDeDebito,
    TipoDeDocumento,
)
from radar.nucleo.enumeracoes_de_infraestrutura import EstrategiaDeCaptura
from radar.nucleo.informado import DESCONHECIDO, Desconhecido, Informado
from testes.geradores.escalas import (
    data_hora_br,
    dinheiro,
    escala_de_zero_a_cem,
    informado,
)

__all__ = [
    "ITENS_CRITICOS_DO_CHECKLIST",
    "PRIMEIRA_VERSAO",
    "QUANTIDADE_DE_ITENS_DO_CHECKLIST",
    "CandidatoDoRadar",
    "ConfiguracaoDeChecklist",
    "Debito",
    "Documento",
    "PayloadDeConector",
    "ProcessoJudicial",
    "VersaoDeAnalise",
    "VersaoDeDocumento",
    "candidato_do_radar",
    "categoria_de_diferenca",
    "configuracao_de_checklist",
    "conjunto_de_debitos",
    "documento",
    "par_de_versoes_de_analise",
    "payload_de_conector",
    "porta_de_entrada",
    "processo_judicial",
    "versao_de_documento",
]

PRIMEIRA_VERSAO: Final[int] = 1
"""Versão inicial de documento e de análise. A contiguidade começa em 1, não em 0 (`R87.1`)."""

QUANTIDADE_DE_ITENS_DO_CHECKLIST: Final[int] = 234
"""Os 234 itens do Checklist Mestre. A cobertura é contrato (`R92.7`, `P16.1`)."""

ITENS_CRITICOS_DO_CHECKLIST: Final[tuple[str, ...]] = (
    "MC-001",
    "MC-032",
    "MC-107",
    "MC-108",
    "B-22",
    "C-01",
)
"""Amostra de itens críticos. Configuração que tenta removê-los da versão 1 é rejeitada com
`ErroDeConfiguracaoDeChecklist` (`R92.5`, `REG-040`)."""

_HASH_HEXADECIMAL = st.text(alphabet="0123456789abcdef", min_size=64, max_size=64)


@dataclass(frozen=True, slots=True, kw_only=True)
class Documento:
    """Documento com arquivo original imutável e hash registrado (`R86.2`, `R86.6`).

    `hash_calculado_no_download` é gerado **independente** de `hash_registrado`: quando divergem,
    é falha de integridade com pendência crítica, e o conteúdo extraído não pode ser usado como
    evidência (`R86.7`, `R86.8`).
    """

    identificador: UUID
    tipo: TipoDeDocumento
    origem: OrigemDeDocumento
    nome_do_arquivo: str
    hash_registrado: str
    hash_calculado_no_download: str
    registrado_em: datetime
    texto_extraido: str | Desconhecido

    @property
    def integridade_violada(self) -> bool:
        """Verdadeiro quando o hash do download divergiu do registrado."""
        return self.hash_registrado != self.hash_calculado_no_download


def documento() -> st.SearchStrategy[Documento]:
    """Documento nos nove tipos, com o caso de hash divergente sempre no espaço de geração.

    O hash íntegro é o caso comum e o divergente é injetado explicitamente: gerar dois hashes
    aleatórios de 64 caracteres praticamente nunca produziria coincidência, e a propriedade de
    round-trip de download (`P17.3`) nunca veria o caminho feliz.
    """
    return st.builds(
        _documento_com_integridade,
        identificador=st.uuids(),
        tipo=st.sampled_from(TipoDeDocumento),
        origem=st.sampled_from(OrigemDeDocumento),
        nome_do_arquivo=st.sampled_from(("matricula.pdf", "edital.pdf", "iptu.pdf")),
        hash_registrado=_HASH_HEXADECIMAL,
        hash_divergente=_HASH_HEXADECIMAL,
        integro=st.booleans(),
        registrado_em=data_hora_br(),
        texto_extraido=st.one_of(st.just(DESCONHECIDO), st.text(min_size=1, max_size=120)),
    )


def _documento_com_integridade(
    *,
    identificador: UUID,
    tipo: TipoDeDocumento,
    origem: OrigemDeDocumento,
    nome_do_arquivo: str,
    hash_registrado: str,
    hash_divergente: str,
    integro: bool,
    registrado_em: datetime,
    texto_extraido: str | Desconhecido,
) -> Documento:
    calculado = hash_registrado if integro else f"{hash_divergente[:63]}f"
    return Documento(
        identificador=identificador,
        tipo=tipo,
        origem=origem,
        nome_do_arquivo=nome_do_arquivo,
        hash_registrado=hash_registrado,
        hash_calculado_no_download=calculado,
        registrado_em=registrado_em,
        texto_extraido=texto_extraido,
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class VersaoDeDocumento:
    """Versão de documento, numerada sem lacuna a partir de 1 (`R87.1`)."""

    identificador_do_documento: UUID
    numero: int
    hash_do_conteudo: str
    registrada_em: datetime
    contradiz_evidencia_vigente: bool


def versao_de_documento() -> st.SearchStrategy[tuple[VersaoDeDocumento, ...]]:
    """Sequência contígua de versões de documento, começando **sempre** na versão 1.

    A contiguidade é gerada em lugar de sorteada: numeração com lacuna é defeito de persistência
    e é verificada por restrição de banco, não por propriedade sobre entrada inventada.
    """
    return st.builds(
        _sequencia_de_versoes_de_documento,
        identificador_do_documento=st.uuids(),
        quantidade=st.integers(min_value=1, max_value=5),
        hashes=st.lists(_HASH_HEXADECIMAL, min_size=5, max_size=5).map(tuple),
        registrada_em=data_hora_br(),
        contradicoes=st.lists(st.booleans(), min_size=5, max_size=5).map(tuple),
    )


def _sequencia_de_versoes_de_documento(
    *,
    identificador_do_documento: UUID,
    quantidade: int,
    hashes: tuple[str, ...],
    registrada_em: datetime,
    contradicoes: tuple[bool, ...],
) -> tuple[VersaoDeDocumento, ...]:
    return tuple(
        VersaoDeDocumento(
            identificador_do_documento=identificador_do_documento,
            numero=PRIMEIRA_VERSAO + indice,
            hash_do_conteudo=hashes[indice],
            registrada_em=registrada_em,
            contradiz_evidencia_vigente=contradicoes[indice],
        )
        for indice in range(quantidade)
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class VersaoDeAnalise:
    """Versão de análise: append-only, com decisão, camada e evidências da vez (`R61`, `R88`)."""

    numero: int
    decisao: EstadoDeDecisao
    escore_de_oportunidade: Decimal
    confianca_consolidada: Decimal
    evidencias: tuple[UUID, ...]
    versao_das_regras: str
    analisada_em: datetime


def par_de_versoes_de_analise() -> st.SearchStrategy[tuple[VersaoDeAnalise, VersaoDeAnalise]]:
    """Par de versões de análise `V1` e `V2`, contíguo a partir de 1.

    Metade do espaço é o par **idêntico**, e isso é deliberado: a comparação é vazia se e somente
    se as versões são idênticas (`P17.9`). Um gerador que só produzisse pares distintos provaria
    apenas a metade fácil da bicondicional.
    """
    return st.builds(
        _par_de_versoes,
        decisao_v1=st.sampled_from(EstadoDeDecisao),
        decisao_v2=st.sampled_from(EstadoDeDecisao),
        escore_v1=escala_de_zero_a_cem(),
        escore_v2=escala_de_zero_a_cem(),
        confianca_v1=escala_de_zero_a_cem(),
        confianca_v2=escala_de_zero_a_cem(),
        evidencias_v1=st.lists(st.uuids(), min_size=0, max_size=4, unique=True).map(tuple),
        evidencias_v2=st.lists(st.uuids(), min_size=0, max_size=4, unique=True).map(tuple),
        versao_das_regras=st.sampled_from(("1.0.0", "1.1.0")),
        analisada_em=data_hora_br(),
        identicas=st.booleans(),
    )


def _par_de_versoes(
    *,
    decisao_v1: EstadoDeDecisao,
    decisao_v2: EstadoDeDecisao,
    escore_v1: Decimal,
    escore_v2: Decimal,
    confianca_v1: Decimal,
    confianca_v2: Decimal,
    evidencias_v1: tuple[UUID, ...],
    evidencias_v2: tuple[UUID, ...],
    versao_das_regras: str,
    analisada_em: datetime,
    identicas: bool,
) -> tuple[VersaoDeAnalise, VersaoDeAnalise]:
    primeira = VersaoDeAnalise(
        numero=PRIMEIRA_VERSAO,
        decisao=decisao_v1,
        escore_de_oportunidade=escore_v1,
        confianca_consolidada=confianca_v1,
        evidencias=evidencias_v1,
        versao_das_regras=versao_das_regras,
        analisada_em=analisada_em,
    )
    if identicas:
        return (primeira, primeira)
    segunda = VersaoDeAnalise(
        numero=PRIMEIRA_VERSAO + 1,
        decisao=decisao_v2,
        escore_de_oportunidade=escore_v2,
        confianca_consolidada=confianca_v2,
        evidencias=evidencias_v2,
        versao_das_regras=versao_das_regras,
        analisada_em=analisada_em,
    )
    return (primeira, segunda)


def categoria_de_diferenca() -> st.SearchStrategy[CategoriaDeDiferenca]:
    """As cinco categorias de diferença. `decisao_alterada` exige motivo (`R88.5`, `R88.6`)."""
    return st.sampled_from(CategoriaDeDiferenca)


@dataclass(frozen=True, slots=True, kw_only=True)
class ConfiguracaoDeChecklist:
    """Configuração de uma versão do Checklist Mestre (`R92`).

    `itens_removidos` e `ausencia_tratada_como_favoravel` existem para gerar as duas configurações
    que **têm** de ser rejeitadas (`REG-040`): remover item crítico da versão 1, e tornar a
    ausência de evidência favorável.
    """

    versao: int
    quantidade_de_itens: int
    itens_removidos: tuple[str, ...]
    ausencia_tratada_como_favoravel: bool
    resultado_por_item: Mapping[str, ResultadoDeItemDeChecklist]


def configuracao_de_checklist() -> st.SearchStrategy[ConfiguracaoDeChecklist]:
    """Configuração de checklist, com a versão 1 e as duas configurações proibidas."""
    return st.builds(
        ConfiguracaoDeChecklist,
        versao=st.integers(min_value=PRIMEIRA_VERSAO, max_value=3),
        quantidade_de_itens=st.just(QUANTIDADE_DE_ITENS_DO_CHECKLIST),
        itens_removidos=st.lists(
            st.sampled_from(ITENS_CRITICOS_DO_CHECKLIST),
            min_size=0,
            max_size=3,
            unique=True,
        ).map(tuple),
        ausencia_tratada_como_favoravel=st.booleans(),
        resultado_por_item=st.fixed_dictionaries(
            dict.fromkeys(
                ITENS_CRITICOS_DO_CHECKLIST,
                st.sampled_from(ResultadoDeItemDeChecklist),
            )
        ),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class Debito:
    """Débito como entidade, não estimativa (`R91.1`, `R91.2`).

    Valor `DESCONHECIDO` é o caso central: tipo exigido pelo checklist e não investigado permanece
    `DESCONHECIDO`, nunca zero (`R91.5`).
    """

    tipo: TipoDeDebito
    valor: Informado[Decimal]
    situacao: SituacaoDeDebito
    responsabilidade: ResponsabilidadePeloDebito
    consultado_em: datetime | Desconhecido
    documento_de_origem: UUID | Desconhecido


def conjunto_de_debitos() -> st.SearchStrategy[tuple[Debito, ...]]:
    """Conjunto de débitos que compõe `CUS-005` e `CUS-006`, possivelmente vazio."""
    debito = st.builds(
        Debito,
        tipo=st.sampled_from(TipoDeDebito),
        valor=informado(dinheiro()),
        situacao=st.sampled_from(SituacaoDeDebito),
        responsabilidade=st.sampled_from(ResponsabilidadePeloDebito),
        consultado_em=st.one_of(st.just(DESCONHECIDO), data_hora_br()),
        documento_de_origem=st.one_of(st.just(DESCONHECIDO), st.uuids()),
    )
    return st.lists(debito, min_size=0, max_size=6).map(tuple)


@dataclass(frozen=True, slots=True, kw_only=True)
class ProcessoJudicial:
    """Processo judicial com situação, objeto e impacto declarados (`R90.1`)."""

    numero: str
    situacao: SituacaoDeProcesso
    objeto: str
    impacto_declarado: str
    ultima_movimentacao_em: datetime | Desconhecido


def processo_judicial() -> st.SearchStrategy[ProcessoJudicial]:
    """Processo judicial nas cinco situações, incluindo `DESCONHECIDA`."""
    return st.builds(
        ProcessoJudicial,
        numero=st.from_regex(r"\A[0-9]{7}-[0-9]{2}\Z", fullmatch=True),
        situacao=st.sampled_from(SituacaoDeProcesso),
        objeto=st.text(min_size=1, max_size=60),
        impacto_declarado=st.sampled_from(
            ("nenhum", "potencial", "material_mitigavel", "material_impeditivo")
        ),
        ultima_movimentacao_em=st.one_of(st.just(DESCONHECIDO), data_hora_br()),
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class PayloadDeConector:
    """Payload de conector com a estratégia de captura que o obteve (`R85.1`, `R106.1`).

    A estratégia é invisível ao domínio (`R85.3`, `P20.4`). Ela aparece aqui porque `P17.20` exige
    que payload **igual** obtido por estratégias **diferentes** produza resultado idêntico — e
    isso só é verificável se a estratégia puder variar com o payload fixo.
    """

    estrategia: EstrategiaDeCaptura
    fonte: str
    conteudo: Mapping[str, str]
    cobertura_declarada: tuple[str, ...]


def payload_de_conector() -> st.SearchStrategy[PayloadDeConector]:
    """Payload de conector, com as quatro estratégias de captura."""
    return st.builds(
        PayloadDeConector,
        estrategia=st.sampled_from(EstrategiaDeCaptura),
        fonte=st.sampled_from(("caixa", "banco-do-brasil", "leiloeiro-oficial")),
        conteudo=st.fixed_dictionaries(
            {
                "identificador": st.text(min_size=1, max_size=16),
                "preco": st.sampled_from(("47.76", "191651.31", "250000,00")),
            }
        ),
        cobertura_declarada=st.lists(
            st.sampled_from(("listar_ofertas", "obter_detalhe", "obter_documentos")),
            min_size=1,
            max_size=3,
            unique=True,
        ).map(tuple),
    )


def porta_de_entrada() -> st.SearchStrategy[PortaDeEntrada]:
    """As duas portas de entrada. A porta é proveniência, nunca parâmetro de decisão (`R84.9`)."""
    return st.sampled_from(PortaDeEntrada)


@dataclass(frozen=True, slots=True, kw_only=True)
class CandidatoDoRadar:
    """Candidato da triagem rápida, antes do gate de promoção `G1-P` (`R93`).

    A triagem decide quem segue, nunca o que vale: não emite `EstadoDeDecisao` (`R93.2`), e por
    isso este tipo não tem campo de veredito.
    """

    identificador: UUID
    resultado_da_triagem: ResultadoDeTriagem
    potencial_preliminar: PotencialPreliminar
    promovido: bool
    criterio_nao_satisfeito: str | Desconhecido


def candidato_do_radar() -> st.SearchStrategy[CandidatoDoRadar]:
    """Candidato do Radar, incluindo o reprovado em `G1-P` com o critério nomeado (`REG-043`)."""
    return st.builds(
        CandidatoDoRadar,
        identificador=st.uuids(),
        resultado_da_triagem=st.sampled_from(ResultadoDeTriagem),
        potencial_preliminar=st.sampled_from(PotencialPreliminar),
        promovido=st.booleans(),
        criterio_nao_satisfeito=st.one_of(
            st.just(DESCONHECIDO),
            st.sampled_from(("PRI-001", "PRI-002", "LOC-002", "TIP-002")),
        ),
    )
