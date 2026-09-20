"""Identificador de correlação na fronteira: atribuição na borda e propagação sem troca.

Bloco `1.1-A` do passo 1 de `D91`. Testes **unitários**: verificam os casos em que o valor tem
de falhar alto — identificador nulo, texto em branco, texto fora da forma de `UUID`, tentativa
de mutação — e o comportamento que `R111.1` exige do caminho de execução: recebeu correlação,
mantém a mesma; não recebeu, está na borda e atribui.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from uuid import UUID, uuid4

import pytest

from radar.nucleo.correlacao import (
    NOME_DO_CAMPO_DE_CORRELACAO,
    IdentificadorDeCorrelacao,
    propagar,
)


def test_novo_atribui_identificador_distinto_em_cada_execucao() -> None:
    primeiro = IdentificadorDeCorrelacao.novo()
    segundo = IdentificadorDeCorrelacao.novo()
    assert primeiro != segundo
    assert isinstance(primeiro.valor, UUID)


def test_o_valor_e_congelado() -> None:
    correlacao = IdentificadorDeCorrelacao.novo()
    with pytest.raises(FrozenInstanceError):
        correlacao.valor = uuid4()  # type: ignore[misc]


def test_a_igualdade_e_a_do_valor() -> None:
    valor = uuid4()
    assert IdentificadorDeCorrelacao(valor=valor) == IdentificadorDeCorrelacao(valor=valor)


def test_identificador_nulo_e_recusado() -> None:
    with pytest.raises(ValueError, match="nulo"):
        IdentificadorDeCorrelacao(valor=UUID(int=0))


def test_valor_fora_de_uuid_e_recusado() -> None:
    with pytest.raises(TypeError, match="UUID"):
        IdentificadorDeCorrelacao(valor="7d0a9e2e")  # type: ignore[arg-type]


@pytest.mark.parametrize("texto", ["", "   ", "correlacao-1", "7d0a9e2e"])
def test_de_texto_recusa_correlacao_ilegivel(texto: str) -> None:
    with pytest.raises(ValueError):
        IdentificadorDeCorrelacao.de_texto(texto)


def test_de_texto_preserva_a_correlacao_recebida_de_fora_do_processo() -> None:
    origem = IdentificadorDeCorrelacao.novo()
    assert IdentificadorDeCorrelacao.de_texto(f"  {origem.texto}  ") == origem
    assert str(origem) == origem.texto


def test_propagar_mantem_a_correlacao_recebida() -> None:
    origem = IdentificadorDeCorrelacao.novo()
    assert propagar(origem) is origem


def test_propagar_atribui_quando_a_execucao_nasce_na_borda() -> None:
    atribuido = propagar(None)
    assert atribuido.valor != UUID(int=0)


def test_o_nome_do_campo_de_correlacao_e_o_da_coluna_e_do_log() -> None:
    assert NOME_DO_CAMPO_DE_CORRELACAO == "identificador_de_correlacao"
