"""Verifica a consequência das três marcas de dependência externa (`R73.2`, `R73.7`).

Três afirmações, verificadas por execução real do `pytest` em subprocesso, não por leitura de
configuração: as três marcas **estão declaradas** (marca não declarada é erro), estão
**desabilitadas por default** e a **habilitação explícita funciona** — tanto por `-m` na linha
de comando quanto pela variável `MARCAS_HABILITADAS` da integração contínua.

A suíte efêmera vive dentro de `testes/` para que `testes/conftest.py` valha sobre ela, e é
removida ao fim de cada caso. A coleta (`--collect-only`) é suficiente: a desseleção por marca
acontece na coleta, e a declaração da marca é exigida na importação do módulo.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tomllib
from collections.abc import Iterator
from pathlib import Path

import pytest

from testes.conftest import (
    EXPRESSAO_DESABILITADA_POR_DEFAULT,
    MARCAS_DE_DEPENDENCIA_EXTERNA,
    NOME_DA_VARIAVEL_DE_HABILITACAO,
    NOMES_DAS_MARCAS,
    expressao_de_selecao,
    marcas_habilitadas,
)

RAIZ_DO_PROJETO = Path(__file__).resolve().parents[2]

MODULO_MARCADO = '''"""Suíte efêmera: um teste sem marca e um por marca de dependência externa."""

import pytest


def test_sem_marca() -> None:
    assert True


@pytest.mark.db
def test_com_marca_db() -> None:
    assert True


@pytest.mark.fonte_externa
def test_com_marca_fonte_externa() -> None:
    assert True


@pytest.mark.provedor_de_modelo
def test_com_marca_provedor_de_modelo() -> None:
    assert True
'''

MODULO_COM_MARCA_NAO_DECLARADA = '''"""Suíte efêmera com marca fora das três declaradas."""

import pytest


@pytest.mark.dependencia_nao_declarada
def test_com_marca_inexistente() -> None:
    assert True
'''


@pytest.fixture
def suite_efemera() -> Iterator[Path]:
    """Diretório descartável sob `testes/`, com os dois módulos de verificação."""
    destino = RAIZ_DO_PROJETO / "testes" / f"_marcas_em_verificacao_{os.getpid()}"
    shutil.rmtree(destino, ignore_errors=True)
    destino.mkdir()
    try:
        (destino / "test_marcado.py").write_text(MODULO_MARCADO, encoding="utf-8")
        (destino / "test_nao_declarada.py").write_text(
            MODULO_COM_MARCA_NAO_DECLARADA, encoding="utf-8"
        )
        yield destino
    finally:
        shutil.rmtree(destino, ignore_errors=True)


def _coletar(
    arquivo: Path, *argumentos: str, ambiente: dict[str, str] | None = None
) -> tuple[int, str]:
    """Roda a coleta do `pytest` como a linha de comando roda, e devolve código e saída."""
    variaveis = dict(os.environ)
    variaveis.pop(NOME_DA_VARIAVEL_DE_HABILITACAO, None)
    variaveis.update(ambiente or {})
    processo = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "--collect-only",
            "-p",
            "no:cacheprovider",
            str(arquivo),
            *argumentos,
        ],
        cwd=RAIZ_DO_PROJETO,
        capture_output=True,
        text=True,
        env=variaveis,
        check=False,
    )
    return processo.returncode, processo.stdout + processo.stderr


def _selecionados(saida: str) -> set[str]:
    """Nomes de teste que sobreviveram à desseleção por marca."""
    return {
        linha.rsplit("::", 1)[1].strip()
        for linha in saida.splitlines()
        if "::" in linha and linha.strip().startswith("testes/")
    }


def test_as_tres_marcas_de_dependencia_externa_estao_declaradas() -> None:
    assert NOMES_DAS_MARCAS == ("db", "fonte_externa", "provedor_de_modelo")
    assert len(MARCAS_DE_DEPENDENCIA_EXTERNA) == 3
    for marca in MARCAS_DE_DEPENDENCIA_EXTERNA:
        assert marca.descricao.startswith(f"{marca.nome}: exige ")


def test_o_pyproject_liga_strict_markers_e_desabilita_as_tres_por_default() -> None:
    with (RAIZ_DO_PROJETO / "pyproject.toml").open("rb") as arquivo:
        configuracao = tomllib.load(arquivo)
    addopts: list[str] = configuracao["tool"]["pytest"]["ini_options"]["addopts"]
    assert "--strict-markers" in addopts
    assert "-m" in addopts
    assert EXPRESSAO_DESABILITADA_POR_DEFAULT in addopts


def test_marca_nao_declarada_e_erro_e_nao_aviso(suite_efemera: Path) -> None:
    codigo, saida = _coletar(suite_efemera / "test_nao_declarada.py")
    assert codigo != 0, saida
    assert "dependencia_nao_declarada" in saida


def test_por_default_nenhuma_das_tres_marcas_e_selecionada(suite_efemera: Path) -> None:
    codigo, saida = _coletar(suite_efemera / "test_marcado.py")
    assert codigo == 0, saida
    assert _selecionados(saida) == {"test_sem_marca"}


def test_a_linha_de_comando_habilita_a_marca_pedida(suite_efemera: Path) -> None:
    codigo, saida = _coletar(suite_efemera / "test_marcado.py", "-m", "db")
    assert codigo == 0, saida
    assert _selecionados(saida) == {"test_com_marca_db"}


def test_a_variavel_de_ambiente_habilita_as_marcas_da_integracao_continua(
    suite_efemera: Path,
) -> None:
    codigo, saida = _coletar(
        suite_efemera / "test_marcado.py",
        ambiente={NOME_DA_VARIAVEL_DE_HABILITACAO: "fonte_externa"},
    )
    assert codigo == 0, saida
    assert _selecionados(saida) == {"test_sem_marca", "test_com_marca_fonte_externa"}

    codigo, saida = _coletar(
        suite_efemera / "test_marcado.py",
        ambiente={NOME_DA_VARIAVEL_DE_HABILITACAO: ",".join(NOMES_DAS_MARCAS)},
    )
    assert codigo == 0, saida
    assert _selecionados(saida) == {
        "test_sem_marca",
        "test_com_marca_db",
        "test_com_marca_fonte_externa",
        "test_com_marca_provedor_de_modelo",
    }


def test_a_expressao_de_selecao_reflete_a_habilitacao_pedida() -> None:
    assert expressao_de_selecao({}) == EXPRESSAO_DESABILITADA_POR_DEFAULT
    assert expressao_de_selecao({NOME_DA_VARIAVEL_DE_HABILITACAO: "db"}) == (
        "not fonte_externa and not provedor_de_modelo"
    )
    assert expressao_de_selecao({NOME_DA_VARIAVEL_DE_HABILITACAO: ",".join(NOMES_DAS_MARCAS)}) == ""


def test_marca_habilitada_fora_das_tres_falha_fechado(suite_efemera: Path) -> None:
    with pytest.raises(ValueError, match="Marca de dependência externa desconhecida"):
        marcas_habilitadas({NOME_DA_VARIAVEL_DE_HABILITACAO: "rede"})

    codigo, saida = _coletar(
        suite_efemera / "test_marcado.py",
        ambiente={NOME_DA_VARIAVEL_DE_HABILITACAO: "rede"},
    )
    assert codigo != 0
    assert "INTERNALERROR" not in saida
    assert "Marca de dependência externa desconhecida" in saida
