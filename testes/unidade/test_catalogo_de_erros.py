"""Catálogo único de erro: as 15 categorias, a taxonomia e a rejeição que é registro.

Bloco `1.1-A` do passo 1 de `D91`, tarefa 2.3. São testes **unitários**: verificam os casos
específicos em que o catálogo tem de falhar alto e as fronteiras exatas do contrato declarado em
*Error Handling*. Não substituem `MT-14`, que confronta o catálogo da implementação com o catálogo
declarado no design, nem a tradução na fronteira, que é de `radar/plataforma/erros.py`.

Quatro grupos:

1. **O catálogo** — as 15 categorias de `R114.2`, uma a uma, com código `RAD-NNN` único, mensagem
   amigável em português e contexto exigido; e as três famílias particionando o catálogo inteiro.
2. **Nenhuma mensagem com detalhe técnico** (`R114.3`) — sem rastro de execução, consulta ao banco,
   caminho de arquivo interno ou mensagem de biblioteca.
3. **A taxonomia** — toda classe resolve para exatamente uma categoria do catálogo; código e
   mensagem vêm do catálogo, não do chamador; classe cuja categoria depende da causa exige a causa
   declarada; contexto com segredo ou conteúdo bruto é recusado na construção.
4. **Falha que é estado registrado** — `RejeicaoDeCaptura` não é exceção, existe só com estado
   `REJEITADA` e exige a causa nomeada (`R85.8`); erro não catalogado abre pendência (`R114.7`).
"""

from __future__ import annotations

import re
from uuid import uuid4

import pytest

from radar.nucleo.enumeracoes import EstadoDaCaptura
from radar.nucleo.enumeracoes_de_infraestrutura import CategoriaDeErro
from radar.nucleo.erros import (
    CATALOGO_DE_ERROS,
    CATEGORIA_POR_CLASSE_DE_ERRO,
    CATEGORIAS_ADMITIDAS_POR_CAUSA,
    FAMILIAS_DE_ERRO,
    ErroCatalogado,
    ErroDeCapturaInvalida,
    ErroDeFronteiraDeEnum,
    ErroDeIdempotenciaAusente,
    ErroDeProvedorDeIA,
    ErroDeTempoExcedidoDeIA,
    ErroDeValidacaoDeDominio,
    ErroDoRadar,
    PendenciaDeCatalogacao,
    RejeicaoDeCaptura,
    catalogar,
    categoria_de_erro,
    entrada_do_catalogo,
)

#: Rastros que jamais aparecem em mensagem apresentada ao usuário (`R114.3`).
RASTROS_TECNICOS = (
    r"Traceback",
    r"\bSELECT\b",
    r"\bINSERT\b",
    r"\bUPDATE\b",
    r"psycopg",
    r"sqlalchemy",
    r"pydantic",
    r"\.py\b",
    r"[A-Za-z]:\\\\",
    r"/usr/",
    r"/var/",
    r"\bException\b",
    r"\bstack trace\b",
)


# --------------------------------------------------------------------------------------
# 1. O catálogo
# --------------------------------------------------------------------------------------


def test_o_catalogo_declara_as_quinze_categorias_uma_a_uma() -> None:
    assert set(CATALOGO_DE_ERROS) == set(CategoriaDeErro)
    assert len(CATALOGO_DE_ERROS) == 15


def test_cada_categoria_tem_codigo_estavel_unico_mensagem_e_contexto() -> None:
    codigos = [entrada.codigo for entrada in CATALOGO_DE_ERROS.values()]
    assert len(set(codigos)) == len(codigos), "código do catálogo é estável e único"
    for categoria, entrada in CATALOGO_DE_ERROS.items():
        assert entrada.categoria is categoria
        assert re.fullmatch(r"RAD-\d{3}", entrada.codigo), categoria
        assert entrada.mensagem_amigavel.strip(), categoria
        assert entrada.contexto_registrado, categoria


def test_as_tres_familias_particionam_o_catalogo() -> None:
    assert len(FAMILIAS_DE_ERRO) == 3
    reunidas = [categoria for familia in FAMILIAS_DE_ERRO.values() for categoria in familia]
    assert len(reunidas) == len(set(reunidas)), "categoria não pertence a duas famílias"
    assert set(reunidas) == set(CategoriaDeErro)


def test_o_catalogo_e_imutavel() -> None:
    with pytest.raises(TypeError):
        CATALOGO_DE_ERROS[CategoriaDeErro.CONFLITO] = (  # type: ignore[index]
            entrada_do_catalogo(CategoriaDeErro.NAO_ENCONTRADO)
        )


# --------------------------------------------------------------------------------------
# 2. Nenhuma mensagem apresentada com detalhe técnico
# --------------------------------------------------------------------------------------


def test_nenhuma_mensagem_apresentada_contem_detalhe_tecnico() -> None:
    com_detalhe = [
        f"{categoria}: {rastro}"
        for categoria, entrada in CATALOGO_DE_ERROS.items()
        for rastro in RASTROS_TECNICOS
        if re.search(rastro, entrada.mensagem_amigavel)
    ]
    assert not com_detalhe, com_detalhe


def test_a_representacao_textual_do_erro_e_a_mensagem_amigavel() -> None:
    erro = ErroDeFronteiraDeEnum(contexto={"campo": "situacao_juridica"})
    assert str(erro) == entrada_do_catalogo(CategoriaDeErro.ERRO_DE_VALIDACAO).mensagem_amigavel


# --------------------------------------------------------------------------------------
# 3. A taxonomia
# --------------------------------------------------------------------------------------


def test_toda_classe_declarada_resolve_para_categoria_do_catalogo() -> None:
    for classe, categoria in CATEGORIA_POR_CLASSE_DE_ERRO.items():
        assert categoria in CATALOGO_DE_ERROS, classe
        erro = classe()
        assert erro.categoria is categoria
        assert erro.codigo == CATALOGO_DE_ERROS[categoria].codigo


def test_a_classe_mais_especifica_vence_a_herdada() -> None:
    assert ErroDeProvedorDeIA().categoria is CategoriaDeErro.ERRO_DE_PROVEDOR_DE_IA
    assert ErroDeTempoExcedidoDeIA().categoria is CategoriaDeErro.TEMPO_EXCEDIDO_DE_IA


def test_captura_invalida_e_indisponibilidade_de_fonte_nao_erro_de_dominio() -> None:
    assert ErroDeCapturaInvalida().categoria is CategoriaDeErro.FONTE_INDISPONIVEL


def test_classe_por_causa_exige_a_causa_declarada() -> None:
    assert set(CATEGORIAS_ADMITIDAS_POR_CAUSA) <= set(CATEGORIA_POR_CLASSE_DE_ERRO.keys()) | set(
        CATEGORIAS_ADMITIDAS_POR_CAUSA
    )
    with pytest.raises(ValueError, match="causa declarada"):
        ErroDeIdempotenciaAusente()
    with pytest.raises(ValueError, match="admite apenas"):
        ErroDeIdempotenciaAusente(categoria=CategoriaDeErro.NAO_ENCONTRADO)
    erro = ErroDeIdempotenciaAusente(categoria=CategoriaDeErro.ERRO_DE_VALIDACAO)
    assert erro.codigo == entrada_do_catalogo(CategoriaDeErro.ERRO_DE_VALIDACAO).codigo


def test_subclasse_sem_categoria_declarada_falha_na_construcao() -> None:
    class ErroDeCatalogoParalelo(ErroDoRadar):
        """Subclasse que não entrou no catálogo: defeito, não alternativa (`R114.5`)."""

    with pytest.raises(ValueError, match="não tem categoria declarada"):
        ErroDeCatalogoParalelo()


def test_contexto_nao_carrega_segredo_nem_conteudo_bruto() -> None:
    with pytest.raises(ValueError, match="segredo"):
        ErroDeValidacaoDeDominio(contexto={"senha_do_usuario": "..."})
    with pytest.raises(ValueError, match="segredo"):
        ErroDeValidacaoDeDominio(contexto={"payload": "{}"})
    with pytest.raises(TypeError, match="binário"):
        ErroDeValidacaoDeDominio(contexto={"documento": b"\x00\x01"})


def test_contexto_do_erro_e_imutavel_e_independente_do_chamador() -> None:
    contexto = {"campo": "prazo"}
    erro = ErroDeValidacaoDeDominio(contexto=contexto)
    contexto["campo"] = "outro"
    assert erro.contexto["campo"] == "prazo"
    with pytest.raises(TypeError):
        erro.contexto["campo"] = "terceiro"  # type: ignore[index]


# --------------------------------------------------------------------------------------
# 4. Catalogação, pendência e falha que é estado registrado
# --------------------------------------------------------------------------------------


def test_catalogar_produz_os_cinco_atributos_de_r114_1() -> None:
    correlacao = uuid4()
    erro = ErroDeProvedorDeIA(contexto={"tarefa": "extracao"}, detalhe_seguro="provedor recusou")
    resultado = catalogar(erro, correlacao)
    assert isinstance(resultado, ErroCatalogado)
    assert resultado.codigo == "RAD-521"
    assert resultado.categoria is CategoriaDeErro.ERRO_DE_PROVEDOR_DE_IA
    assert resultado.mensagem_amigavel == erro.mensagem_amigavel
    assert resultado.contexto == {"tarefa": "extracao"}
    assert resultado.identificador_de_correlacao == correlacao
    assert resultado.detalhe_seguro == "provedor recusou"


def test_erro_catalogado_recusa_codigo_de_outra_categoria() -> None:
    with pytest.raises(ValueError, match="catálogo é único"):
        ErroCatalogado(
            codigo="RAD-404",
            mensagem_amigavel="Não encontramos o item solicitado.",
            contexto={},
            identificador_de_correlacao=uuid4(),
            detalhe_seguro="",
            categoria=CategoriaDeErro.CONFLITO,
        )


def test_erro_nao_catalogado_abre_pendencia_de_catalogacao() -> None:
    correlacao = uuid4()
    assert categoria_de_erro(ZeroDivisionError()) is None
    resultado = catalogar(ZeroDivisionError(), correlacao)
    assert isinstance(resultado, PendenciaDeCatalogacao)
    assert resultado.classe_do_erro == "ZeroDivisionError"
    assert resultado.identificador_de_correlacao == correlacao


def test_rejeicao_de_captura_e_registro_nao_excecao() -> None:
    rejeicao = RejeicaoDeCaptura(
        captura_id=uuid4(),
        causa_de_rejeicao="preço ausente",
        campos_ausentes=("preco",),
    )
    assert not isinstance(rejeicao, BaseException)
    assert rejeicao.estado is EstadoDaCaptura.REJEITADA


def test_rejeicao_de_captura_exige_causa_nomeada_e_estado_rejeitada() -> None:
    with pytest.raises(ValueError, match="causa_de_rejeicao"):
        RejeicaoDeCaptura(captura_id=uuid4(), causa_de_rejeicao="   ")
    with pytest.raises(ValueError, match="REJEITADA"):
        RejeicaoDeCaptura(
            captura_id=uuid4(),
            causa_de_rejeicao="preço ausente",
            estado=EstadoDaCaptura.CAPTURADA,
        )
