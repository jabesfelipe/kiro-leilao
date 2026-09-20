"""Fundação de tipos na fronteira: `Informado[T]`, `classificar_por_faixa` e os enums.

Bloco `1.1` do passo 1 de `D91`. São testes **unitários**, não de propriedade: verificam os
casos específicos em que a fundação tem de falhar alto e as fronteiras exatas em que ela tem de
classificar, e não substituem nenhuma das propriedades do design.

Três grupos, um por peça da fundação:

1. `Informado[T]` e `Desconhecido` na fronteira — coerência entre valor ausente e estado,
   `float` recusado, fonte em branco recusada, escala da confiança e `exigir_valor` que falha
   em lugar de devolver zero. Caça a ausência lida como zero (`R3.2`, `R26.7`, SAFE-003,
   SAFE-005).
2. `classificar_por_faixa` — totalidade sobre `[0, 100]` nos limites inteiros **e**
   fracionários, e recusa de toda tabela defeituosa. Caça `D.1.5`, o 89,5 sem faixa (`R49.6`).
3. Enumerações — a contagem que cada um dos 60 + 7 enums declara na própria docstring, e a
   ausência de valor duplicado. Caça o valor acrescentado em silêncio (`R62.4`).

O terceiro grupo **não** duplica `MT-09`: lá a contagem do design é confrontada com a
implementação; aqui é a contagem que cada enum **declara no próprio contrato** que é confrontada
com os seus valores. Um enum cuja docstring diz "as 6 situações" e lista sete é incoerente
consigo mesmo antes de ser incoerente com o design.

Os valores de fronteira vêm dos geradores compartilhados (`testes/geradores/escalas.py`): os
sete fracionários de `D.1.5` não são redigitados aqui, para que exista um único lugar onde eles
podem estar errados.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import MISSING, FrozenInstanceError, fields
from datetime import datetime
from decimal import Decimal
from enum import Enum
from types import ModuleType
from typing import Any, Final, cast

import pytest
from hypothesis import Phase, find, settings
from hypothesis import strategies as st

from radar.motores.faixas import (
    LIMITE_INFERIOR_DA_ESCALA,
    LIMITE_SUPERIOR_DA_ESCALA,
    TabelaDeFaixas,
    classificar_por_faixa,
    construir_faixas,
)
from radar.nucleo import enumeracoes, enumeracoes_de_infraestrutura
from radar.nucleo.enumeracoes import EstadoDaInformacao, Impacto, QualidadeDaEvidencia
from radar.nucleo.informado import (
    CONFIANCA_MAXIMA,
    CONFIANCA_MINIMA,
    DESCONHECIDO,
    Desconhecido,
    Informado,
    MetricaProvisoria,
    MotivoDeProvisoriedade,
)
from testes.geradores import escalas

# Busca curta e sem banco de exemplos: o que se verifica aqui é que o gerador compartilhado
# entrega um `Informado` coerente, não uma propriedade. Gravar os achados no banco de exemplos o
# poluiria com entradas que não são contraexemplo de propriedade alguma.
BUSCA_DE_FRONTEIRA: Final[settings] = settings(
    max_examples=50,
    deadline=None,
    database=None,
    phases=(Phase.generate,),
)

DATA_DE_OBSERVACAO: Final[datetime] = datetime(
    2026, 9, 15, 10, 0, tzinfo=escalas.FUSO_DE_BRASILIA
)


def _primeiro[T](
    estrategia: st.SearchStrategy[T],
    condicao: Callable[[T], bool] = lambda _: True,
) -> T:
    """Primeiro valor da estratégia que satisfaz a condição, com busca curta."""
    return find(estrategia, condicao, settings=BUSCA_DE_FRONTEIRA)


# --------------------------------------------------------------------------------------
# `Informado[T]` e `Desconhecido` na fronteira
# --------------------------------------------------------------------------------------

NOMES_DOS_CAMPOS_DE_INFORMADO: Final[tuple[str, ...]] = tuple(
    campo.name for campo in fields(Informado)
)


def _campos_com_valor() -> dict[str, Any]:
    """Construção válida com valor presente, para ser desfigurada campo a campo."""
    return {
        "valor": Decimal("191651.31"),
        "estado_da_informacao": EstadoDaInformacao.CONFIRMADO,
        "fonte": "edital",
        "data_de_observacao": DATA_DE_OBSERVACAO,
        "confianca": Decimal(80),
        "qualidade_da_evidencia": QualidadeDaEvidencia.FORTE,
    }


def _campos_sem_valor() -> dict[str, Any]:
    """Construção válida de ausência declarada, para ser desfigurada campo a campo."""
    return {
        "valor": DESCONHECIDO,
        "estado_da_informacao": EstadoDaInformacao.DESCONHECIDO,
        "fonte": "edital",
        "data_de_observacao": DATA_DE_OBSERVACAO,
        "confianca": DESCONHECIDO,
        "qualidade_da_evidencia": QualidadeDaEvidencia.AUSENTE,
    }


def _informado_bruto(**campos: Any) -> Informado[Decimal]:
    """Constrói sem a proteção do verificador de tipos.

    A fronteira que interessa é a de **execução**: `float` e campo omitido chegam de código que
    não passou por verificação estática, e é aí que a validação tem de falhar.
    """
    return Informado(**campos)


def test_o_sentinela_de_ausencia_e_um_valor_de_dominio() -> None:
    assert isinstance(DESCONHECIDO, Desconhecido)
    assert Desconhecido() == DESCONHECIDO


def test_a_ausencia_nao_e_falsa_como_o_zero() -> None:
    # `Desconhecido` não define valor de verdade próprio: `if valor:` não pode confundir
    # ausência de informação com zero, que **é** falso.
    assert bool(DESCONHECIDO) is True
    assert bool(Decimal(0)) is False


def test_informado_exige_palavra_chave_em_todo_campo() -> None:
    construtor = cast("Callable[..., object]", Informado)
    with pytest.raises(TypeError):
        construtor(
            Decimal("191651.31"),
            EstadoDaInformacao.CONFIRMADO,
            "edital",
            DATA_DE_OBSERVACAO,
            Decimal(80),
            QualidadeDaEvidencia.FORTE,
        )


def test_nenhum_campo_de_informado_tem_default() -> None:
    com_default = [
        campo.name
        for campo in fields(Informado)
        if campo.default is not MISSING or campo.default_factory is not MISSING
    ]
    assert not com_default, (
        "ausência se declara campo a campo com Desconhecido; default permissivo em "
        f"Informado viola SAFE-005: {com_default}"
    )


def test_informado_recusa_campo_omitido() -> None:
    for nome in NOMES_DOS_CAMPOS_DE_INFORMADO:
        campos = _campos_com_valor()
        del campos[nome]
        with pytest.raises(TypeError, match=nome):
            _informado_bruto(**campos)


def test_informado_e_congelado() -> None:
    informado = _informado_bruto(**_campos_com_valor())
    # O nome do campo vem de variável de propósito: a atribuição direta é recusada pelo
    # verificador de tipos, e o que se verifica aqui é a recusa em **execução**.
    campo = "valor"
    with pytest.raises(FrozenInstanceError):
        setattr(informado, campo, Decimal(1))


def test_valor_ausente_exige_estado_desconhecido() -> None:
    campos = _campos_sem_valor()
    campos["estado_da_informacao"] = EstadoDaInformacao.ESTIMADO
    with pytest.raises(ValueError, match="valor ausente exige"):
        _informado_bruto(**campos)


def test_estado_desconhecido_exige_valor_ausente() -> None:
    campos = _campos_com_valor()
    campos["estado_da_informacao"] = EstadoDaInformacao.DESCONHECIDO
    with pytest.raises(ValueError, match="exige valor ausente"):
        _informado_bruto(**campos)


def test_estado_desconhecido_exige_qualidade_ausente() -> None:
    campos = _campos_sem_valor()
    campos["qualidade_da_evidencia"] = QualidadeDaEvidencia.FRACA
    with pytest.raises(ValueError, match="qualidade_da_evidencia AUSENTE"):
        _informado_bruto(**campos)


def test_estado_desconhecido_exige_confianca_ausente() -> None:
    campos = _campos_sem_valor()
    campos["confianca"] = Decimal(10)
    with pytest.raises(ValueError, match="confianca ausente"):
        _informado_bruto(**campos)


def test_float_nao_atravessa_a_fronteira_do_informado() -> None:
    com_valor_float = _campos_com_valor()
    com_valor_float["valor"] = 191651.31
    with pytest.raises(TypeError, match="valor não aceita float"):
        _informado_bruto(**com_valor_float)

    com_confianca_float = _campos_com_valor()
    com_confianca_float["confianca"] = 80.0
    with pytest.raises(TypeError, match="confianca não aceita float"):
        _informado_bruto(**com_confianca_float)


def test_fonte_em_branco_nao_representa_ausencia() -> None:
    for em_branco in ("", "   ", "\t\n"):
        campos = _campos_com_valor()
        campos["fonte"] = em_branco
        with pytest.raises(ValueError, match="fonte em branco"):
            _informado_bruto(**campos)

    campos = _campos_com_valor()
    campos["fonte"] = DESCONHECIDO
    assert isinstance(_informado_bruto(**campos).fonte, Desconhecido)


def test_a_confianca_vive_na_escala_de_zero_a_cem() -> None:
    assert Decimal(0) == CONFIANCA_MINIMA
    assert Decimal(100) == CONFIANCA_MAXIMA

    aceitos = (CONFIANCA_MINIMA, CONFIANCA_MAXIMA, *escalas.VALORES_FRACIONARIOS_DE_FRONTEIRA)
    for confianca in aceitos:
        campos = _campos_com_valor()
        campos["confianca"] = confianca
        assert _informado_bruto(**campos).confianca == confianca

    for fora_da_escala in (Decimal("-0.01"), Decimal("100.01")):
        campos = _campos_com_valor()
        campos["confianca"] = fora_da_escala
        with pytest.raises(ValueError, match="confianca fora da escala"):
            _informado_bruto(**campos)


def test_exigir_valor_falha_em_lugar_de_devolver_zero() -> None:
    ausente = _informado_bruto(**_campos_sem_valor())
    assert ausente.esta_desconhecido is True
    with pytest.raises(ValueError, match="não tem substituto numérico"):
        ausente.exigir_valor()

    presente = _informado_bruto(**_campos_com_valor())
    assert presente.esta_desconhecido is False
    assert presente.exigir_valor() == Decimal("191651.31")


def test_informado_desconhecido_declara_ausencia_em_todo_campo() -> None:
    ausente: Informado[Decimal] = Informado.desconhecido()
    assert isinstance(ausente.valor, Desconhecido)
    assert isinstance(ausente.fonte, Desconhecido)
    assert isinstance(ausente.data_de_observacao, Desconhecido)
    assert isinstance(ausente.confianca, Desconhecido)
    assert ausente.estado_da_informacao is EstadoDaInformacao.DESCONHECIDO
    assert ausente.qualidade_da_evidencia is QualidadeDaEvidencia.AUSENTE
    assert ausente.esta_desconhecido is True


def test_informado_desconhecido_preserva_a_proveniencia_que_houver() -> None:
    ausente: Informado[Decimal] = Informado.desconhecido(
        fonte="edital", data_de_observacao=DATA_DE_OBSERVACAO
    )
    assert ausente.fonte == "edital"
    assert ausente.data_de_observacao == DATA_DE_OBSERVACAO
    assert ausente.esta_desconhecido is True


def test_o_gerador_compartilhado_produz_informado_com_valor_coerente() -> None:
    informado = _primeiro(escalas.informado(escalas.dinheiro(), permitir_desconhecido=False))
    assert informado.esta_desconhecido is False
    assert informado.exigir_valor() == informado.valor
    assert informado.estado_da_informacao is not EstadoDaInformacao.DESCONHECIDO
    assert isinstance(informado.confianca, Decimal)
    assert CONFIANCA_MINIMA <= informado.confianca <= CONFIANCA_MAXIMA


def test_o_gerador_compartilhado_produz_ausencia_declarada() -> None:
    ausente = _primeiro(
        escalas.informado(escalas.dinheiro()),
        lambda gerado: gerado.esta_desconhecido,
    )
    assert ausente.estado_da_informacao is EstadoDaInformacao.DESCONHECIDO
    assert ausente.qualidade_da_evidencia is QualidadeDaEvidencia.AUSENTE
    assert isinstance(ausente.confianca, Desconhecido)
    with pytest.raises(ValueError, match="não tem substituto numérico"):
        ausente.exigir_valor()


def test_o_motivo_de_provisoriedade_exige_componente_e_pendencia_nomeados() -> None:
    with pytest.raises(ValueError, match="componente é obrigatório"):
        MotivoDeProvisoriedade(
            componente="   ",
            estado_da_informacao=EstadoDaInformacao.DESCONHECIDO,
            impacto=Impacto.ALTO,
            pendencia_determinante="obter certidão de débitos de condomínio",
        )

    with pytest.raises(ValueError, match="pendencia_determinante é obrigatória"):
        MotivoDeProvisoriedade(
            componente="debitos_de_condominio",
            estado_da_informacao=EstadoDaInformacao.DESCONHECIDO,
            impacto=Impacto.ALTO,
            pendencia_determinante="",
        )


def test_o_impacto_nao_estimado_e_desconhecido_e_nunca_baixo_por_omissao() -> None:
    motivo = MotivoDeProvisoriedade(
        componente="debitos_de_condominio",
        estado_da_informacao=EstadoDaInformacao.DESCONHECIDO,
        impacto=DESCONHECIDO,
        pendencia_determinante="obter certidão de débitos de condomínio",
    )
    assert isinstance(motivo.impacto, Desconhecido)


def _motivo() -> MotivoDeProvisoriedade:
    return MotivoDeProvisoriedade(
        componente="debitos_de_condominio",
        estado_da_informacao=EstadoDaInformacao.DESCONHECIDO,
        impacto=Impacto.CRITICO,
        pendencia_determinante="obter certidão de débitos de condomínio",
    )


def test_metrica_sem_valor_exige_ao_menos_um_motivo_de_provisoriedade() -> None:
    ausente: Informado[Decimal] = Informado.desconhecido()
    with pytest.raises(ValueError, match="ao menos um motivo de provisoriedade"):
        MetricaProvisoria(valor=ausente, motivos_da_provisoriedade=())

    provisoria = MetricaProvisoria(valor=ausente, motivos_da_provisoriedade=(_motivo(),))
    assert provisoria.esta_provisoria is True


def test_metrica_com_valor_e_sem_motivo_e_definitiva() -> None:
    presente = _informado_bruto(**_campos_com_valor())
    definitiva = MetricaProvisoria(valor=presente, motivos_da_provisoriedade=())
    assert definitiva.esta_provisoria is False
    assert definitiva.valor.exigir_valor() == Decimal("191651.31")


# --------------------------------------------------------------------------------------
# `classificar_por_faixa`: totalidade sobre `[0, 100]`
# --------------------------------------------------------------------------------------

LIMITES_DE_FRONTEIRA: Final[tuple[Decimal, ...]] = (
    Decimal(90),
    Decimal(80),
    Decimal(75),
    Decimal(70),
    Decimal(60),
    Decimal(50),
    Decimal(40),
    Decimal(0),
)
"""Os limites inteiros que os sete fracionários de `D.1.5` cercam, em ordem decrescente.

Os rótulos são locais a este teste: o que se verifica é o **classificador**, não a tabela de
nenhum motor. Cada fracionário de `escalas.VALORES_FRACIONARIOS_DE_FRONTEIRA` fica entre dois
destes limites, que é exatamente onde `D.1.5` abria lacuna.
"""


def _rotulo(limite: Decimal) -> str:
    return f"faixa_de_{limite}"


TABELA_DE_FRONTEIRA: Final[TabelaDeFaixas[str]] = construir_faixas(
    *((limite, _rotulo(limite)) for limite in LIMITES_DE_FRONTEIRA)
)

ROTULOS: Final[frozenset[str]] = frozenset(_rotulo(limite) for limite in LIMITES_DE_FRONTEIRA)


def _classificar_bruto(valor: object) -> str:
    """Classifica sem a proteção do verificador de tipos, para exercitar `float` e `int`."""
    classe: str = classificar_por_faixa(cast("Decimal", valor), TABELA_DE_FRONTEIRA)
    return classe


def test_a_escala_declarada_vai_de_zero_a_cem() -> None:
    assert Decimal(0) == LIMITE_INFERIOR_DA_ESCALA
    assert Decimal(100) == LIMITE_SUPERIOR_DA_ESCALA


def test_todo_inteiro_da_escala_recebe_faixa() -> None:
    for inteiro in range(101):
        assert classificar_por_faixa(Decimal(inteiro), TABELA_DE_FRONTEIRA) in ROTULOS


def test_todo_meio_ponto_da_escala_recebe_faixa() -> None:
    # A totalidade que `D.1.5` violava não é a dos inteiros: é a dos fracionários entre eles.
    for inteiro in range(100):
        fracionario = Decimal(inteiro) + Decimal("0.5")
        assert classificar_por_faixa(fracionario, TABELA_DE_FRONTEIRA) in ROTULOS


def test_os_sete_fracionarios_de_d_1_5_caem_na_faixa_imediatamente_inferior() -> None:
    esperado = {
        Decimal("89.5"): _rotulo(Decimal(80)),
        Decimal("79.5"): _rotulo(Decimal(75)),
        Decimal("74.5"): _rotulo(Decimal(70)),
        Decimal("69.5"): _rotulo(Decimal(60)),
        Decimal("59.5"): _rotulo(Decimal(50)),
        Decimal("49.5"): _rotulo(Decimal(40)),
        Decimal("39.5"): _rotulo(Decimal(0)),
    }
    assert set(esperado) == set(escalas.VALORES_FRACIONARIOS_DE_FRONTEIRA), (
        "os sete fracionários obrigatórios são os declarados em testes/geradores/escalas.py; "
        "divergir deles é verificar a fronteira errada"
    )
    for fracionario, rotulo in esperado.items():
        assert classificar_por_faixa(fracionario, TABELA_DE_FRONTEIRA) == rotulo


def test_no_limite_exato_o_valor_pertence_a_faixa_superior() -> None:
    for indice, limite in enumerate(LIMITES_DE_FRONTEIRA):
        assert classificar_por_faixa(limite, TABELA_DE_FRONTEIRA) == _rotulo(limite)
        if limite == LIMITE_INFERIOR_DA_ESCALA:
            continue
        abaixo = limite - Decimal("0.01")
        seguinte = LIMITES_DE_FRONTEIRA[indice + 1]
        assert classificar_por_faixa(abaixo, TABELA_DE_FRONTEIRA) == _rotulo(seguinte)


def test_os_extremos_da_escala_recebem_faixa() -> None:
    assert classificar_por_faixa(LIMITE_INFERIOR_DA_ESCALA, TABELA_DE_FRONTEIRA) == _rotulo(
        Decimal(0)
    )
    assert classificar_por_faixa(LIMITE_SUPERIOR_DA_ESCALA, TABELA_DE_FRONTEIRA) == _rotulo(
        Decimal(90)
    )


def test_valor_fora_da_escala_falha_em_lugar_de_saturar() -> None:
    for fora in (Decimal("-0.01"), Decimal("100.01"), Decimal(-1), Decimal(101)):
        with pytest.raises(ValueError, match="valor fora da escala"):
            classificar_por_faixa(fora, TABELA_DE_FRONTEIRA)


def test_float_nao_atravessa_o_classificador() -> None:
    with pytest.raises(TypeError, match="valor não aceita float"):
        _classificar_bruto(89.5)


def test_valor_que_nao_e_decimal_nao_classifica() -> None:
    with pytest.raises(TypeError, match="valor exige Decimal"):
        _classificar_bruto(90)


def test_decimal_nao_finito_nao_classifica() -> None:
    for nao_finito in (Decimal("NaN"), Decimal("Infinity"), Decimal("-Infinity")):
        with pytest.raises(ValueError, match="valor exige valor finito"):
            classificar_por_faixa(nao_finito, TABELA_DE_FRONTEIRA)


def test_tabela_vazia_nao_classifica_valor_algum() -> None:
    with pytest.raises(ValueError, match="tabela de faixas vazia"):
        construir_faixas()


def test_os_limites_precisam_ser_estritamente_decrescentes() -> None:
    for limites in ((Decimal(80), Decimal(80), Decimal(0)), (Decimal(40), Decimal(80), Decimal(0))):
        with pytest.raises(ValueError, match="estritamente decrescentes"):
            construir_faixas(*((limite, _rotulo(limite)) for limite in limites))


def test_a_ultima_faixa_precisa_comecar_no_limite_inferior_da_escala() -> None:
    with pytest.raises(ValueError, match="última faixa"):
        construir_faixas((Decimal(90), "alta"), (Decimal(40), "baixa"))


def test_limite_fora_da_escala_e_recusado_na_construcao() -> None:
    for limite in (Decimal(101), Decimal(-1)):
        with pytest.raises(ValueError, match="limite inferior da faixa de índice"):
            construir_faixas((limite, "alta"), (Decimal(0), "baixa"))


def test_limite_float_e_recusado_na_construcao() -> None:
    with pytest.raises(TypeError, match="não aceita float"):
        construir_faixas((cast("Decimal", 90.0), "alta"), (Decimal(0), "baixa"))


def test_o_classificador_revalida_a_tabela_improvisada() -> None:
    # Tabela que não passou por `construir_faixas` e deixa `[0, 40)` sem faixa: falha em vez de
    # devolver a classe errada, mesmo para um valor que a primeira faixa satisfaria.
    com_lacuna = cast("TabelaDeFaixas[str]", ((Decimal(90), "alta"), (Decimal(40), "baixa")))
    with pytest.raises(ValueError, match="última faixa"):
        classificar_por_faixa(Decimal(95), com_lacuna)


# --------------------------------------------------------------------------------------
# Enumerações: a contagem que cada enum declara é a que ele tem
# --------------------------------------------------------------------------------------

TOTAL_DE_ENUMS_DE_NEGOCIO: Final[int] = 60
TOTAL_DE_ENUMS_DE_INFRAESTRUTURA: Final[int] = 7

PADRAO_DA_CONTAGEM_DECLARADA: Final[re.Pattern[str]] = re.compile(r"^(?:As|Os)\s+(\d+)\s")
"""A primeira linha da docstring de cada enum abre com `As N …` ou `Os N …`. `N` é o contrato."""


def _enums_do_modulo(modulo: ModuleType) -> dict[str, type[Enum]]:
    """Enums declarados **no próprio módulo**: `StrEnum` importado não conta."""
    return {
        nome: valor
        for nome, valor in vars(modulo).items()
        if isinstance(valor, type)
        and issubclass(valor, Enum)
        and valor.__module__ == modulo.__name__
    }


def _contagem_declarada(nome: str, enumeracao: type[Enum]) -> int:
    documentacao = (enumeracao.__doc__ or "").strip()
    encontrado = PADRAO_DA_CONTAGEM_DECLARADA.match(documentacao)
    assert encontrado is not None, (
        f"{nome} não declara a quantidade de valores na primeira linha da docstring; a contagem "
        "é contrato por `R62.4` e precisa estar escrita para ser verificável"
    )
    return int(encontrado.group(1))


def _divergencias_de_contagem(modulo: ModuleType) -> list[str]:
    return [
        f"{nome}: declarado {_contagem_declarada(nome, enumeracao)}, "
        f"implementado {len(list(enumeracao))}"
        for nome, enumeracao in sorted(_enums_do_modulo(modulo).items())
        if _contagem_declarada(nome, enumeracao) != len(list(enumeracao))
    ]


def test_os_sessenta_enums_de_negocio_estao_declarados() -> None:
    assert len(_enums_do_modulo(enumeracoes)) == TOTAL_DE_ENUMS_DE_NEGOCIO


def test_os_sete_enums_de_infraestrutura_estao_declarados() -> None:
    assert len(_enums_do_modulo(enumeracoes_de_infraestrutura)) == TOTAL_DE_ENUMS_DE_INFRAESTRUTURA


def test_cada_enum_de_negocio_tem_a_contagem_que_declara() -> None:
    divergentes = _divergencias_de_contagem(enumeracoes)
    assert not divergentes, (
        f"enum de negócio incoerente com a contagem da própria docstring: {divergentes}"
    )


def test_cada_enum_de_infraestrutura_tem_a_contagem_que_declara() -> None:
    divergentes = _divergencias_de_contagem(enumeracoes_de_infraestrutura)
    assert not divergentes, (
        f"enum de infraestrutura incoerente com a contagem da própria docstring: {divergentes}"
    )


def test_nenhum_enum_tem_valor_duplicado() -> None:
    duplicados: list[str] = []
    for modulo in (enumeracoes, enumeracoes_de_infraestrutura):
        for nome, enumeracao in sorted(_enums_do_modulo(modulo).items()):
            membros = list(enumeracao)
            if len(enumeracao.__members__) != len(membros):
                duplicados.append(f"{nome}: apelido de membro repetido")
            if len({membro.value for membro in membros}) != len(membros):
                duplicados.append(f"{nome}: valor repetido entre membros")
    assert not duplicados, (
        "valor duplicado torna a contagem declarada ilusória, porque o apelido não aparece na "
        f"iteração: {duplicados}"
    )


def test_o_todo_de_cada_enum_e_alcancavel_pelo_proprio_valor() -> None:
    # Reconstruir cada membro a partir do seu valor é o que a persistência e a auditoria fazem:
    # se o valor não volta ao membro, a contagem declarada não descreve o que se grava.
    for modulo in (enumeracoes, enumeracoes_de_infraestrutura):
        for nome, enumeracao in sorted(_enums_do_modulo(modulo).items()):
            for membro in enumeracao:
                assert enumeracao(membro.value) is membro, f"{nome}.{membro.name}"
