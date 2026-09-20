"""Verifica a infraestrutura de teste de propriedade: os quatro perfis de execução."""

from __future__ import annotations

import pytest
from hypothesis import Phase, settings

from testes.perfis_de_execucao import (
    ITERACOES_POR_PERFIL,
    PERFIL_PADRAO,
    carregar_perfil,
    perfil_pedido,
    registrar_perfis,
)


def test_os_quatro_perfis_estao_registrados_com_as_iteracoes_do_design() -> None:
    registrar_perfis()
    assert set(ITERACOES_POR_PERFIL) == {"dev", "ci", "noturno", "regressao"}
    assert settings.get_profile("dev").max_examples == 100
    assert settings.get_profile("ci").max_examples == 500
    assert settings.get_profile("noturno").max_examples == 5_000


def test_o_perfil_padrao_e_dev_e_garante_o_minimo_de_cem_iteracoes() -> None:
    assert perfil_pedido({}) == PERFIL_PADRAO == "dev"
    assert settings.get_profile("dev").max_examples >= 100


def test_o_perfil_de_regressao_nao_gera_casos_novos() -> None:
    registrar_perfis()
    fases = settings.get_profile("regressao").phases
    assert Phase.reuse in fases
    assert Phase.explicit in fases
    assert Phase.generate not in fases


def test_deadline_nao_e_desativado_por_perfil() -> None:
    registrar_perfis()
    for nome in ITERACOES_POR_PERFIL:
        assert settings.get_profile(nome).deadline is not None


def test_perfil_desconhecido_falha_fechado() -> None:
    registrar_perfis()
    with pytest.raises(ValueError, match="Perfil de hypothesis desconhecido"):
        carregar_perfil("producao")
