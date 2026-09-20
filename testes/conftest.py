"""Marcas de dependência externa: declaração única, desabilitadas por default.

Três dependências externas exigem marcação, porque a suíte precisa rodar completa sem
nenhuma delas (`D91` passo 1, `R73.2`, `R73.7`):

| Marca                | Dependência                             | Na propriedade                |
|----------------------|-----------------------------------------|-------------------------------|
| `db`                 | PostgreSQL com pgvector                 | repositório em memória        |
| `fonte_externa`      | portal vendedor, leiloeiro, mercado     | `payload_de_conector()`       |
| `provedor_de_modelo` | modelo de linguagem e de embedding      | `dubla_de_provedor_*()`       |

**Aqui é o ponto único de declaração.** `pyproject.toml` não repete a lista: ele só liga
`--strict-markers` — marca não declarada é **erro**, não aviso — e o `addopts` com a
expressão que desabilita as três por default. Este módulo registra cada marca no
`pytest_configure` e recalcula a expressão de seleção conforme a habilitação explícita.

**Default: desabilitado.** `python -m pytest` puro não toca banco, não abre rede e não
consome crédito de provedor. A consequência é a exigida pelo design: as 262 propriedades
rodam em qualquer máquina.

**Habilitação explícita**, nas duas formas, para a integração contínua escolher:

1. Linha de comando — `-m` posterior ao `addopts` vence o default:

       python -m pytest -m db
       python -m pytest -m "db or fonte_externa"

2. Variável de ambiente `MARCAS_HABILITADAS`, lista separada por vírgula. Habilita as
   marcas pedidas **sem** desabilitar o resto da suíte, que é o que a integração contínua
   quer — rodar tudo, inclusive o marcado:

       MARCAS_HABILITADAS=db python -m pytest
       MARCAS_HABILITADAS=db,fonte_externa,provedor_de_modelo python -m pytest

   No PowerShell, `$env:MARCAS_HABILITADAS = "db"` antes da chamada.

Nome fora da lista das três **não** cai em silêncio: falha fechada, com os nomes válidos na
mensagem. A variável só age sobre a expressão default; `-m` na linha de comando tem
precedência e é preservado como escrito.

Os perfis do `hypothesis` são registrados pelo `conftest.py` da raiz e não são assunto deste
módulo.
"""

from __future__ import annotations

import os
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Final

import pytest


@dataclass(frozen=True, slots=True)
class MarcaDeDependenciaExterna:
    """Uma marca, a dependência que ela carrega e o dublê que a substitui na propriedade."""

    nome: str
    dependencia: str
    dubla_na_propriedade: str

    @property
    def descricao(self) -> str:
        """Linha no formato que o `pytest` espera em `markers`: `nome: descrição`."""
        return (
            f"{self.nome}: exige {self.dependencia}; desabilitada por default, "
            f"habilitada explicitamente na integração contínua; "
            f"na propriedade, {self.dubla_na_propriedade}"
        )


#: As três, e apenas as três. Lista fechada: dependência externa nova entra por decisão
#: explícita, com a linha desta tabela preenchida.
MARCAS_DE_DEPENDENCIA_EXTERNA: Final[tuple[MarcaDeDependenciaExterna, ...]] = (
    MarcaDeDependenciaExterna(
        nome="db",
        dependencia="PostgreSQL com pgvector",
        dubla_na_propriedade="repositório em memória ou a função pura",
    ),
    MarcaDeDependenciaExterna(
        nome="fonte_externa",
        dependencia="portal da instituição vendedora, leiloeiro ou portal de mercado",
        dubla_na_propriedade="payload_de_conector() e payload_por_estrategia()",
    ),
    MarcaDeDependenciaExterna(
        nome="provedor_de_modelo",
        dependencia="provedor de modelo de linguagem e de embedding",
        dubla_na_propriedade="dubla_de_provedor_de_modelo() e dubla_de_provedor_de_embedding()",
    ),
)

NOMES_DAS_MARCAS: Final[tuple[str, ...]] = tuple(
    marca.nome for marca in MARCAS_DE_DEPENDENCIA_EXTERNA
)

NOME_DA_VARIAVEL_DE_HABILITACAO: Final[str] = "MARCAS_HABILITADAS"

SEPARADOR_DA_LISTA: Final[str] = ","


def expressao_que_desabilita(nomes: Iterable[str]) -> str:
    """Expressão `-m` que remove da seleção cada nome informado."""
    return " and ".join(f"not {nome}" for nome in nomes)


#: Exatamente o que `pyproject.toml` declara em `addopts`. Reconhecer esta expressão é como
#: este módulo distingue "ninguém pediu nada" de "-m escrito à mão na linha de comando".
EXPRESSAO_DESABILITADA_POR_DEFAULT: Final[str] = expressao_que_desabilita(NOMES_DAS_MARCAS)


def marcas_habilitadas(ambiente: Mapping[str, str] | None = None) -> frozenset[str]:
    """Marcas pedidas por `MARCAS_HABILITADAS`. Nome fora das três é erro, não é silêncio."""
    variaveis = os.environ if ambiente is None else ambiente
    bruto = variaveis.get(NOME_DA_VARIAVEL_DE_HABILITACAO, "")
    pedidas = [parte.strip() for parte in bruto.split(SEPARADOR_DA_LISTA) if parte.strip()]
    desconhecidas = [nome for nome in pedidas if nome not in NOMES_DAS_MARCAS]
    if desconhecidas:
        validas = ", ".join(NOMES_DAS_MARCAS)
        raise ValueError(
            f"Marca de dependência externa desconhecida: {desconhecidas}. "
            f"Defina {NOME_DA_VARIAVEL_DE_HABILITACAO} com uma lista destas: {validas}."
        )
    return frozenset(pedidas)


def expressao_de_selecao(ambiente: Mapping[str, str] | None = None) -> str:
    """Expressão `-m` em vigor: desabilita toda marca que o ambiente não habilitou."""
    habilitadas = marcas_habilitadas(ambiente)
    return expressao_que_desabilita(nome for nome in NOMES_DAS_MARCAS if nome not in habilitadas)


def pytest_configure(config: pytest.Config) -> None:
    """Declara as três marcas e aplica a habilitação explícita sobre a expressão default."""
    for marca in MARCAS_DE_DEPENDENCIA_EXTERNA:
        config.addinivalue_line("markers", marca.descricao)

    escrita_na_linha_de_comando = str(config.option.markexpr or "").strip()
    if escrita_na_linha_de_comando not in {"", EXPRESSAO_DESABILITADA_POR_DEFAULT}:
        return

    try:
        config.option.markexpr = expressao_de_selecao()
    except ValueError as erro:
        # Erro de uso, não defeito interno: a mensagem sai limpa, sem rastreio de pilha.
        raise pytest.UsageError(str(erro)) from erro


__all__ = [
    "EXPRESSAO_DESABILITADA_POR_DEFAULT",
    "MARCAS_DE_DEPENDENCIA_EXTERNA",
    "NOMES_DAS_MARCAS",
    "NOME_DA_VARIAVEL_DE_HABILITACAO",
    "MarcaDeDependenciaExterna",
    "expressao_de_selecao",
    "expressao_que_desabilita",
    "marcas_habilitadas",
]
