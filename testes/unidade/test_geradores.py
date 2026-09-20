"""Sanidade dos geradores compartilhados: os valores de fronteira existem e tudo constrói.

Não são testes de propriedade e não substituem nenhuma das 262. São a verificação mínima de que a
infraestrutura de teste funciona: que os valores de fronteira obrigatórios do design estão
declarados com o valor **exato**, que cada gerador produz ao menos um valor sem levantar erro, e
que os dublês de provedor funcionam sem rede, sem crédito e sem chave.

O que estes testes protegem é específico: um gerador que levanta erro na construção só apareceria
quando a primeira propriedade que o usa fosse escrita, e um limiar digitado errado passaria
silenciosamente — a propriedade continuaria verde verificando a fronteira errada.
"""

from __future__ import annotations

from collections.abc import Callable
from decimal import Decimal

import pytest
from hypothesis import Phase, find, settings
from hypothesis import strategies as st

from radar.nucleo.enumeracoes import (
    Estrategia,
    QualidadeDaEvidencia,
    UnidadeDePercentual,
)
from radar.nucleo.enumeracoes_de_infraestrutura import CategoriaDeErro, NaturezaDaInformacao
from testes.geradores import aquisicao_resiliente as aquisicao
from testes.geradores import captura_e_identidade as captura
from testes.geradores import decisao_e_lance as decisao
from testes.geradores import dominio_o, escalas, experiencia, governanca, plataforma
from testes.geradores import infraestrutura_de_ia as ia
from testes.geradores import juridico_e_evidencia as juridico
from testes.geradores import mercado_e_economia as economia
from testes.geradores import mercado_e_valuation as valuation
from testes.geradores import risco_liquidez_e_escore as risco

# Busca curta e sem banco de exemplos: estes testes provam que o gerador **constrói**, não que uma
# propriedade vale. Gravar seus achados no banco de exemplos o poluiria com entradas que não são
# contraexemplo de propriedade alguma.
BUSCA_DE_SANIDADE = settings(
    max_examples=20,
    deadline=None,
    database=None,
    phases=(Phase.generate,),
)


def _primeiro[T](
    estrategia: st.SearchStrategy[T],
    condicao: Callable[[T], bool] = lambda _: True,
) -> T:
    """Primeiro valor da estratégia que satisfaz a condição, com busca curta."""
    return find(estrategia, condicao, settings=BUSCA_DE_SANIDADE)


# --------------------------------------------------------------------------------------
# Valores de fronteira obrigatórios
# --------------------------------------------------------------------------------------


def test_os_sete_fracionarios_de_d_1_5_estao_declarados() -> None:
    esperados = (
        Decimal("89.5"),
        Decimal("79.5"),
        Decimal("74.5"),
        Decimal("69.5"),
        Decimal("59.5"),
        Decimal("49.5"),
        Decimal("39.5"),
    )
    assert esperados == escalas.VALORES_FRACIONARIOS_DE_FRONTEIRA


def test_os_fracionarios_entram_na_escala_de_zero_a_cem() -> None:
    for fracionario in escalas.VALORES_FRACIONARIOS_DE_FRONTEIRA:
        assert fracionario in escalas.VALORES_DE_FRONTEIRA_DA_ESCALA


def test_as_cadeias_de_interpretacao_numerica_estao_declaradas() -> None:
    assert escalas.CADEIAS_DECIMAIS_DE_FRONTEIRA == ("47.76", "191651.31")
    assert escalas.CADEIAS_DE_PERCENTUAL_DE_FRONTEIRA == ("2,5%", "2.5%")


def test_um_com_unidade_porcento_esta_declarado() -> None:
    esperado = (Decimal(1), UnidadeDePercentual.PORCENTO)
    assert esperado == escalas.UM_COM_UNIDADE_PORCENTO


def test_os_dezessete_limiares_de_materialidade_estao_cobertos() -> None:
    numericos = set(escalas.LIMIARES_NUMERICOS_DE_MATERIALIDADE)
    qualitativos = set(escalas.LIMIARES_QUALITATIVOS_DE_MATERIALIDADE)
    assert len(escalas.IDENTIFICADORES_DE_MATERIALIDADE) == 17
    assert numericos.isdisjoint(qualitativos)
    assert numericos | qualitativos == set(escalas.IDENTIFICADORES_DE_MATERIALIDADE)


def test_os_limiares_numericos_de_materialidade_sao_os_do_catalogo() -> None:
    esperados = {
        "MON-001": Decimal("0.05"),
        "MON-005": Decimal("0.05"),
        "MON-009": Decimal("0.10"),
        "MON-010": Decimal(10),
        "MON-012": Decimal("0.20"),
        "MON-013": Decimal("0.05"),
        "MON-014": Decimal("0.05"),
    }
    assert esperados == escalas.LIMIARES_NUMERICOS_DE_MATERIALIDADE


def test_os_limiares_de_estrategia_sao_os_da_tabela_str() -> None:
    revenda = escalas.LIMIARES_DE_ESTRATEGIA[Estrategia.REVENDA]
    assert revenda.desconto_liquido_minimo == Decimal("0.25")
    assert revenda.margem_minima == Decimal("0.20")
    assert revenda.yield_liquido_mensal_minimo is None
    assert revenda.liquidez_minima == Decimal(75)
    assert revenda.prazo_de_saida_maximo_em_dias == 180
    assert revenda.ticket_maximo == Decimal(400_000)

    renda = escalas.LIMIARES_DE_ESTRATEGIA[Estrategia.RENDA]
    assert renda.yield_liquido_mensal_minimo == Decimal("0.0080")
    assert renda.liquidez_minima == Decimal(70)

    terreno = escalas.LIMIARES_DE_ESTRATEGIA[Estrategia.TERRENO]
    assert terreno.liquidez_minima == Decimal(50)
    assert terreno.prazo_de_saida_maximo_em_dias == 365

    # `customizada` é inteiramente configurável: não tem valor de fábrica a injetar.
    assert Estrategia.CUSTOMIZADA not in escalas.LIMIARES_DE_ESTRATEGIA


def test_a_liquidez_minima_de_cada_estrategia_entra_na_escala() -> None:
    for limiares in escalas.LIMIARES_DE_ESTRATEGIA.values():
        assert limiares.liquidez_minima in escalas.VALORES_DE_FRONTEIRA_DA_ESCALA


def test_os_limiares_de_decisao_em_pontos_entram_na_escala() -> None:
    for identificador in ("GLB-003", "GLB-004", "GLB-006", "VAL-009", "SCORE-007"):
        assert escalas.LIMIARES_DE_DECISAO[identificador] in (
            escalas.VALORES_DE_FRONTEIRA_DA_ESCALA
        )


def test_os_limiares_fracionarios_entram_no_gerador_de_percentual() -> None:
    esperados = {
        Decimal("0.05"),
        Decimal("0.10"),
        Decimal("0.15"),
        Decimal("0.20"),
        Decimal("0.25"),
        Decimal("0.30"),
        Decimal("0.0080"),
    }
    assert esperados <= set(escalas.VALORES_DE_FRONTEIRA_FRACIONARIOS_DE_PERCENTUAL)


def test_a_versao_inicial_de_documento_e_de_analise_e_um() -> None:
    assert dominio_o.PRIMEIRA_VERSAO == 1


def test_o_par_de_versoes_identicas_e_alcancavel() -> None:
    par = _primeiro(dominio_o.par_de_versoes_de_analise(), lambda versoes: versoes[0] == versoes[1])
    assert par[0] == par[1]


def test_o_documento_com_hash_divergente_e_alcancavel() -> None:
    divergente = _primeiro(dominio_o.documento(), lambda registro: registro.integridade_violada)
    assert divergente.hash_registrado != divergente.hash_calculado_no_download


def test_o_nome_de_arquivo_hostil_cobre_os_cinco_grupos() -> None:
    hostis = plataforma.NOMES_DE_ARQUIVO_HOSTIS
    assert any(nome.startswith("../") for nome in hostis)
    assert any(nome.startswith("/") or ":\\" in nome for nome in hostis)
    assert any("\\" in nome and "/" in nome for nome in hostis)
    assert any(not nome.isascii() for nome in hostis)
    assert "" in hostis


# --------------------------------------------------------------------------------------
# Construção de cada gerador
# --------------------------------------------------------------------------------------

GERADORES: tuple[tuple[str, Callable[[], st.SearchStrategy[object]]], ...] = (
    ("escalas.escala_de_zero_a_cem", escalas.escala_de_zero_a_cem),
    ("escalas.dinheiro", escalas.dinheiro),
    ("escalas.area", escalas.area),
    ("escalas.percentual", escalas.percentual),
    ("escalas.data_hora_br", escalas.data_hora_br),
    ("escalas.texto_de_dinheiro", escalas.texto_de_dinheiro),
    ("escalas.texto_de_percentual", escalas.texto_de_percentual),
    ("captura.payload_bruto", captura.payload_bruto),
    ("captura.oferta_normalizada", captura.oferta_normalizada),
    ("captura.sinais_de_identidade", captura.sinais_de_identidade),
    ("captura.vinculo_de_imovel", captura.vinculo_de_imovel),
    ("juridico.resultados_de_verificacao", juridico.resultados_de_verificacao),
    ("juridico.registro_de_evidencia", juridico.registro_de_evidencia),
    ("juridico.proposta_de_evidencia", juridico.proposta_de_evidencia),
    ("juridico.conjunto_de_pendencias", juridico.conjunto_de_pendencias),
    ("economia.comparavel", economia.comparavel),
    ("economia.entradas_de_valuation", economia.entradas_de_valuation),
    ("economia.composicao_de_custo", economia.composicao_de_custo),
    ("economia.entradas_economicas", economia.entradas_economicas),
    ("economia.entradas_de_preco_maximo", economia.entradas_de_preco_maximo),
    ("economia.premissas_de_cenario", economia.premissas_de_cenario),
    ("risco.registro_de_risco", risco.registro_de_risco),
    ("risco.fatores_de_liquidez", risco.fatores_de_liquidez),
    ("risco.fatores_de_escore", risco.fatores_de_escore),
    ("risco.conjunto_de_pesos", risco.conjunto_de_pesos),
    ("risco.estado_de_portfolio", risco.estado_de_portfolio),
    ("decisao.entrada_de_decisao", decisao.entrada_de_decisao),
    ("decisao.checklist_de_lance", decisao.checklist_de_lance),
    ("governanca.hierarquia_de_parametros", governanca.hierarquia_de_parametros),
    ("governanca.registro_de_excecao", governanca.registro_de_excecao),
    ("governanca.segmento_de_conhecimento", governanca.segmento_de_conhecimento),
    ("dominio_o.documento", dominio_o.documento),
    ("dominio_o.versao_de_documento", dominio_o.versao_de_documento),
    ("dominio_o.par_de_versoes_de_analise", dominio_o.par_de_versoes_de_analise),
    ("dominio_o.configuracao_de_checklist", dominio_o.configuracao_de_checklist),
    ("dominio_o.conjunto_de_debitos", dominio_o.conjunto_de_debitos),
    ("dominio_o.processo_judicial", dominio_o.processo_judicial),
    ("dominio_o.payload_de_conector", dominio_o.payload_de_conector),
    ("dominio_o.porta_de_entrada", dominio_o.porta_de_entrada),
    ("dominio_o.candidato_do_radar", dominio_o.candidato_do_radar),
    ("valuation.conjunto_de_comparaveis", valuation.conjunto_de_comparaveis),
    ("valuation.premissas_de_valuation", valuation.premissas_de_valuation),
    ("valuation.raio_e_janela", valuation.raio_e_janela),
    ("valuation.tipo_de_ativo", valuation.tipo_de_ativo),
    ("ia.dubla_de_provedor_de_modelo", ia.dubla_de_provedor_de_modelo),
    ("ia.dubla_de_provedor_de_embedding", ia.dubla_de_provedor_de_embedding),
    ("ia.prompt_versionado", ia.prompt_versionado),
    ("ia.segmento_com_metadados", ia.segmento_com_metadados),
    ("ia.saida_estruturada", ia.saida_estruturada),
    ("ia.estado_de_workflow", ia.estado_de_workflow),
    ("ia.ponto_de_interrupcao", ia.ponto_de_interrupcao),
    ("ia.invocacao_de_ferramenta", ia.invocacao_de_ferramenta),
    ("ia.grafo_de_importacoes", ia.grafo_de_importacoes),
    ("aquisicao.execucao_do_radar", aquisicao.execucao_do_radar),
    ("aquisicao.payload_por_estrategia", aquisicao.payload_por_estrategia),
    ("aquisicao.captura_invalida", aquisicao.captura_invalida),
    ("aquisicao.sequencia_de_falhas", aquisicao.sequencia_de_falhas),
    (
        "aquisicao.par_de_capturas_da_mesma_oferta",
        aquisicao.par_de_capturas_da_mesma_oferta,
    ),
    ("aquisicao.chave_de_idempotencia", aquisicao.chave_de_idempotencia),
    ("aquisicao.capacidades_declaradas", aquisicao.capacidades_declaradas),
    ("plataforma.segredo_sintetico", plataforma.segredo_sintetico),
    ("plataforma.nome_de_arquivo_hostil", plataforma.nome_de_arquivo_hostil),
    ("plataforma.combinacao_de_sinalizadores", plataforma.combinacao_de_sinalizadores),
    ("plataforma.combinacao_de_adaptadores", plataforma.combinacao_de_adaptadores),
    ("plataforma.colecao_paginavel", plataforma.colecao_paginavel),
    ("plataforma.base_multi_titular", plataforma.base_multi_titular),
    (
        "plataforma.evidencia_em_torno_da_data_de_corte",
        plataforma.evidencia_em_torno_da_data_de_corte,
    ),
    ("plataforma.sequencia_de_eventos", plataforma.sequencia_de_eventos),
    ("experiencia.declaracao_de_tela", experiencia.declaracao_de_tela),
    ("experiencia.classe_de_resposta", experiencia.classe_de_resposta),
    ("experiencia.largura_de_viewport", experiencia.largura_de_viewport),
    ("experiencia.arvore_de_componentes", experiencia.arvore_de_componentes),
    ("experiencia.formulario_declarado", experiencia.formulario_declarado),
)


@pytest.mark.parametrize(
    ("nome", "gerador"),
    GERADORES,
    ids=[nome for nome, _ in GERADORES],
)
def test_cada_gerador_produz_ao_menos_um_valor(
    nome: str,
    gerador: Callable[[], st.SearchStrategy[object]],
) -> None:
    """Todo gerador declarado constrói e produz valor.

    Erro de construção falha aqui, e não na primeira propriedade que usar o gerador.
    """
    del nome
    _primeiro(gerador())


def test_informado_produz_valor_conhecido_e_desconhecido() -> None:
    conhecido = _primeiro(
        escalas.informado(escalas.dinheiro()),
        lambda registro: not registro.esta_desconhecido,
    )
    assert conhecido.qualidade_da_evidencia is not QualidadeDaEvidencia.AUSENTE
    assert isinstance(conhecido.exigir_valor(), Decimal)

    ausente = _primeiro(
        escalas.informado(escalas.dinheiro()),
        lambda registro: registro.esta_desconhecido,
    )
    assert ausente.qualidade_da_evidencia is QualidadeDaEvidencia.AUSENTE
    with pytest.raises(ValueError, match="DESCONHECIDO"):
        ausente.exigir_valor()


def test_informado_sem_desconhecido_nunca_produz_ausencia() -> None:
    presente = _primeiro(escalas.informado(escalas.dinheiro(), permitir_desconhecido=False))
    assert not presente.esta_desconhecido


def test_composicao_de_custo_tem_os_treze_componentes() -> None:
    assert len(economia.COMPONENTES_DO_CUSTO_ECONOMICO_TOTAL) == 13
    composicao = _primeiro(economia.composicao_de_custo())
    for componente in economia.COMPONENTES_DO_CUSTO_ECONOMICO_TOTAL:
        assert hasattr(composicao, componente)


def test_o_gate_juridico_tem_dezenove_verificacoes() -> None:
    assert len(juridico.CODIGOS_DE_VERIFICACAO_JURIDICA) == 19
    resultados = _primeiro(juridico.resultados_de_verificacao())
    assert set(resultados) == set(juridico.CODIGOS_DE_VERIFICACAO_JURIDICA)


def test_o_segmento_tem_os_treze_metadados_obrigatorios() -> None:
    assert len(ia.METADADOS_OBRIGATORIOS_DO_SEGMENTO) == 13
    segmento = _primeiro(ia.segmento_com_metadados())
    assert set(segmento.metadados) == set(ia.METADADOS_OBRIGATORIOS_DO_SEGMENTO)


def test_os_pesos_somam_exatamente_um() -> None:
    pesos = _primeiro(risco.conjunto_de_pesos())
    assert sum(pesos.values()) == Decimal("1.00")


# --------------------------------------------------------------------------------------
# Dublês de provedor: sem rede, sem crédito, sem chave
# --------------------------------------------------------------------------------------


def _dubla_de_modelo(*, falha: CategoriaDeErro | None) -> ia.DublaDeProvedorDeModeloDeLinguagem:
    return ia.DublaDeProvedorDeModeloDeLinguagem(
        capacidade=ia.CapacidadeDubladaDeModelo(
            provedor="dublê-local",
            modelo="modelo-economico",
            versao="1.0.0",
            limite_de_tokens_de_entrada=32_000,
            suporta_saida_estruturada=True,
            suporta_ferramentas=False,
            custo_por_mil_tokens_de_entrada=Decimal("0.0000"),
            custo_por_mil_tokens_de_saida=Decimal("0.0000"),
        ),
        resposta=ia.RespostaDubladaDeModelo(
            texto="texto",
            tokens_de_entrada=10,
            tokens_de_saida=5,
            truncada=False,
        ),
        saida=ia.SaidaEstruturada(
            campos={"proprietario": "ACME"},
            conforme_o_esquema=True,
            natureza=NaturezaDaInformacao.INTERPRETACAO_DA_IA,
            citacao_resolvivel=True,
        ),
        falha=falha,
    )


def test_a_dubla_de_modelo_registra_exatamente_uma_chamada_por_invocacao() -> None:
    dubla = _dubla_de_modelo(falha=None)
    dubla.completar(object(), {}, object())
    dubla.produzir_saida_estruturada(object(), {}, object(), object())
    dubla.declarar_capacidade()
    assert [registro.tarefa for registro in dubla.chamadas] == [
        "completar",
        "produzir_saida_estruturada",
    ]


def test_a_dubla_de_modelo_falha_com_erro_catalogado_e_registra_a_chamada() -> None:
    dubla = _dubla_de_modelo(falha=CategoriaDeErro.TEMPO_EXCEDIDO_DE_IA)
    with pytest.raises(ia.ErroDeProvedorDublado) as capturado:
        dubla.completar(object(), {}, object())
    assert capturado.value.categoria is CategoriaDeErro.TEMPO_EXCEDIDO_DE_IA
    assert len(dubla.chamadas) == 1


def test_a_dubla_de_embedding_e_determinista_e_respeita_a_dimensao() -> None:
    identidade = ia.IdentidadeDubladaDeEmbedding(
        provedor="dublê-local",
        modelo="embedding-pequeno",
        dimensoes=8,
        versao="1.0.0",
    )
    primeira = ia.DublaDeProvedorDeEmbedding(identidade=identidade)
    segunda = ia.DublaDeProvedorDeEmbedding(identidade=identidade)
    vetor_a = primeira.gerar_representacao_vetorial("segmento")
    vetor_b = segunda.gerar_representacao_vetorial("segmento")
    assert vetor_a.vetor == vetor_b.vetor
    assert len(vetor_a.vetor) == identidade.dimensoes
    assert vetor_a.gerada_em.tzinfo is not None
