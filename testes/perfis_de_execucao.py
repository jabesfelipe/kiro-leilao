"""Perfis de execução do `hypothesis`, conforme a estratégia de teste do design.

| Perfil      | `max_examples`   | Uso                                             |
|-------------|------------------|-------------------------------------------------|
| `dev`       | 100              | laço local, execução rápida (padrão)            |
| `ci`        | 500              | integração contínua em cada mudança             |
| `noturno`   | 5.000            | busca profunda, com banco de exemplos persistido|
| `regressao` | banco de exemplos| reexecuta todo contraexemplo já encontrado      |

O perfil ativo vem da variável de ambiente `PERFIL_HYPOTHESIS` e o padrão é `dev`.
Nome desconhecido **não** cai em silêncio para o padrão: falha fechada, com a lista
dos perfis válidos na mensagem.

`deadline` é declarado explicitamente e **igual** nos quatro perfis. Desativá-lo é
decisão de um teste específico, com justificativa escrita nele
(`@settings(deadline=None)  # motivo`), nunca decisão de perfil.
"""

from __future__ import annotations

import os
from datetime import timedelta
from pathlib import Path

from hypothesis import Phase, settings
from hypothesis.database import DirectoryBasedExampleDatabase

RAIZ_DO_PROJETO = Path(__file__).resolve().parents[1]

# Banco de exemplos persistido e versionável: o contraexemplo encontrado numa máquina
# vira regressão permanente para todas as outras.
DIRETORIO_DO_BANCO_DE_EXEMPLOS = RAIZ_DO_PROJETO / "testes" / "banco_de_exemplos"

NOME_DA_VARIAVEL_DE_AMBIENTE = "PERFIL_HYPOTHESIS"
PERFIL_PADRAO = "dev"

#: Mínimo de 100 iterações por propriedade no perfil padrão.
ITERACOES_POR_PERFIL: dict[str, int] = {
    "dev": 100,
    "ci": 500,
    "noturno": 5_000,
    "regressao": 100,
}

PERFIS = tuple(ITERACOES_POR_PERFIL)

PRAZO_POR_EXEMPLO = timedelta(milliseconds=200)


def _banco_de_exemplos() -> DirectoryBasedExampleDatabase:
    DIRETORIO_DO_BANCO_DE_EXEMPLOS.mkdir(parents=True, exist_ok=True)
    return DirectoryBasedExampleDatabase(str(DIRETORIO_DO_BANCO_DE_EXEMPLOS))


def registrar_perfis() -> None:
    """Registra os quatro perfis. Idempotente: registrar de novo sobrescreve igual."""
    banco = _banco_de_exemplos()

    settings.register_profile(
        "dev",
        max_examples=ITERACOES_POR_PERFIL["dev"],
        deadline=PRAZO_POR_EXEMPLO,
        database=banco,
        print_blob=True,
    )
    settings.register_profile(
        "ci",
        max_examples=ITERACOES_POR_PERFIL["ci"],
        deadline=PRAZO_POR_EXEMPLO,
        database=banco,
        print_blob=True,
    )
    settings.register_profile(
        "noturno",
        max_examples=ITERACOES_POR_PERFIL["noturno"],
        deadline=PRAZO_POR_EXEMPLO,
        database=banco,
        print_blob=True,
    )
    # Sem a fase de geração: roda o que está no banco de exemplos e os `@example`
    # explícitos, e só isso. É a releitura barata de todo contraexemplo já conhecido.
    settings.register_profile(
        "regressao",
        max_examples=ITERACOES_POR_PERFIL["regressao"],
        deadline=PRAZO_POR_EXEMPLO,
        database=banco,
        print_blob=True,
        phases=(Phase.explicit, Phase.reuse),
    )


def perfil_pedido(ambiente: dict[str, str] | None = None) -> str:
    """Nome do perfil pedido pelo ambiente, com `dev` como padrão."""
    variaveis = os.environ if ambiente is None else ambiente
    return variaveis.get(NOME_DA_VARIAVEL_DE_AMBIENTE, PERFIL_PADRAO).strip() or PERFIL_PADRAO


def carregar_perfil(nome: str) -> str:
    """Carrega o perfil informado. Nome fora da lista é erro, não é fallback."""
    if nome not in ITERACOES_POR_PERFIL:
        validos = ", ".join(PERFIS)
        raise ValueError(
            f"Perfil de hypothesis desconhecido: {nome!r}. "
            f"Defina {NOME_DA_VARIAVEL_DE_AMBIENTE} com um destes: {validos}."
        )
    settings.load_profile(nome)
    return nome


def registrar_e_carregar(ambiente: dict[str, str] | None = None) -> str:
    """Registra os quatro perfis e carrega o pedido pelo ambiente."""
    registrar_perfis()
    return carregar_perfil(perfil_pedido(ambiente))


__all__ = [
    "DIRETORIO_DO_BANCO_DE_EXEMPLOS",
    "ITERACOES_POR_PERFIL",
    "NOME_DA_VARIAVEL_DE_AMBIENTE",
    "PERFIL_PADRAO",
    "PERFIS",
    "PRAZO_POR_EXEMPLO",
    "carregar_perfil",
    "perfil_pedido",
    "registrar_e_carregar",
    "registrar_perfis",
]
