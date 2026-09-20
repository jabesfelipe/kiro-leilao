"""Apoio comum aos meta-testes: leitura da especificação e sondagem da implementação.

Ler a especificação em tempo de teste é legítimo e é a razão de existir dos meta-testes: eles
existem exatamente para confrontar código e especificação. Os dois arquivos normativos são
`requirements.md` e `design.md`, localizados por caminho **relativo à raiz do repositório**,
derivada deste arquivo e não do diretório de trabalho de quem invoca o `pytest`.

Duas regras estruturam este módulo:

1. **Nada é lido na importação.** Toda leitura e toda sondagem acontecem dentro da função,
   chamada pelo teste. Arquivo ausente vira falha com mensagem, nunca erro de coleta.
2. **Módulo ausente não é exceção.** `modulo_opcional` devolve `None` para módulo inexistente,
   e é isso que permite a um meta-teste falhar por *conteúdo ausente* em lugar de falhar por
   `ModuleNotFoundError`.
"""

from __future__ import annotations

import importlib
import re
from collections.abc import Iterable, Sequence
from functools import cache
from pathlib import Path
from types import ModuleType
from typing import NoReturn

import pytest

#: Raiz do repositório: `testes/meta/apoio.py` → dois níveis acima.
RAIZ_DO_PROJETO = Path(__file__).resolve().parents[2]

NOME_DA_SPEC = "radar-imobiliario-especificacao-completa"
DIRETORIO_DA_SPEC = RAIZ_DO_PROJETO / ".kiro" / "specs" / NOME_DA_SPEC
CAMINHO_DO_REQUIREMENTS = DIRETORIO_DA_SPEC / "requirements.md"
CAMINHO_DO_DESIGN = DIRETORIO_DA_SPEC / "design.md"


@cache
def texto_do_requirements() -> str:
    """Conteúdo de `requirements.md`. Ausência é falha com o caminho procurado."""
    return _ler(CAMINHO_DO_REQUIREMENTS)


@cache
def texto_do_design() -> str:
    """Conteúdo de `design.md`. Ausência é falha com o caminho procurado."""
    return _ler(CAMINHO_DO_DESIGN)


def _ler(caminho: Path) -> str:
    if not caminho.is_file():
        pytest.fail(
            f"Fonte normativa ausente: {caminho}. "
            f"Os meta-testes confrontam código e especificação e exigem os dois arquivos da "
            f"spec `{NOME_DA_SPEC}` no repositório."
        )
    return caminho.read_text(encoding="utf-8")


def secao(texto: str, titulo: str, nivel: str = "## ") -> str:
    """Trecho entre o `titulo` exato e o próximo cabeçalho de `nivel`.

    O título é comparado por igualdade da linha inteira: seção renomeada falha aqui, com o
    título procurado na mensagem, em lugar de devolver trecho vazio em silêncio.
    """
    linhas = texto.splitlines()
    inicio: int | None = None
    for indice, linha in enumerate(linhas):
        if linha.strip() == titulo:
            inicio = indice + 1
            break
    if inicio is None:
        pytest.fail(f"Seção não encontrada na especificação: {titulo!r}.")
    fim = len(linhas)
    for indice in range(inicio, len(linhas)):
        if linhas[indice].startswith(nivel):
            fim = indice
            break
    return "\n".join(linhas[inicio:fim])


def tabela_apos(texto: str, marcador: str) -> list[list[str]]:
    """Primeira tabela markdown que vem depois de `marcador`, célula a célula.

    A linha de separação (`|---|`) é descartada; a primeira linha devolvida é o cabeçalho. A
    varredura para na primeira linha que não pertence à tabela, o que impede capturar a tabela
    seguinte.
    """
    if marcador not in texto:
        pytest.fail(f"Marcador não encontrado na especificação: {marcador!r}.")
    linhas = texto[texto.index(marcador) :].splitlines()[1:]
    tabela: list[list[str]] = []
    dentro = False
    for linha in linhas:
        if linha.startswith("|"):
            dentro = True
            if re.fullmatch(r"\|[\s\-:|]+", linha):
                continue
            tabela.append([celula.strip() for celula in linha.strip().strip("|").split("|")])
        elif dentro:
            break
    return tabela


def identificadores(texto: str, padrao: str) -> list[str]:
    """Identificadores na primeira coluna das linhas de tabela que casam com `padrao`."""
    return re.findall(rf"^\|\s*(?:`)?({padrao})(?:`)?\s*\|", texto, re.MULTILINE)


def criterios_por_requisito(texto_do_requisitos: str) -> dict[int, set[int]]:
    """Mapa requisito → números dos critérios de aceitação declarados nele."""
    mapa: dict[int, set[int]] = {}
    atual: int | None = None
    for linha in texto_do_requisitos.splitlines():
        cabecalho = re.match(r"^###\s+Requirement\s+(\d+):", linha)
        if cabecalho:
            atual = int(cabecalho.group(1))
            mapa.setdefault(atual, set())
            continue
        if atual is None:
            continue
        item = re.match(r"^(\d+)\.\s+\S", linha)
        if item:
            mapa[atual].add(int(item.group(1)))
    return mapa


def itens_enumerados(linha: str, apos: str) -> list[str]:
    """Itens de uma enumeração em prosa separada por ponto e vírgula, depois de `apos`.

    Forma usada pelos critérios de aceitação: `... treze atributos: a; b; c; e d.` O `e` final
    e a pontuação de encerramento são removidos.
    """
    if apos not in linha:
        pytest.fail(f"Enumeração não encontrada: esperava {apos!r} em {linha[:80]!r}.")
    corpo = linha.split(apos, 1)[1]
    itens: list[str] = []
    for parte in corpo.split(";"):
        item = re.sub(r"^\s*e\s+", "", parte.strip()).strip(" .")
        if item:
            itens.append(item)
    return itens


def modulo_opcional(nome: str) -> ModuleType | None:
    """Importa `nome` e devolve `None` quando o módulo ainda não existe.

    Só `ModuleNotFoundError` do próprio módulo procurado é tratada como ausência. Erro de
    sintaxe, import quebrado ou dependência faltante **propaga**: silenciá-los transformaria
    defeito de código em conteúdo ausente.
    """
    try:
        return importlib.import_module(nome)
    except ModuleNotFoundError as erro:
        if erro.name is not None and (nome == erro.name or nome.startswith(f"{erro.name}.")):
            return None
        raise


def simbolo_opcional(nome_do_modulo: str, nome_do_simbolo: str) -> object | None:
    """Símbolo do módulo, ou `None` quando o módulo ou o símbolo ainda não existem."""
    modulo = modulo_opcional(nome_do_modulo)
    if modulo is None:
        return None
    valor: object | None = getattr(modulo, nome_do_simbolo, None)
    return valor


def caminho_ausente(*relativos: str) -> list[str]:
    """Quais dos caminhos relativos à raiz do repositório ainda não existem."""
    return [relativo for relativo in relativos if not (RAIZ_DO_PROJETO / relativo).exists()]


def amostra(itens: Iterable[str], limite: int = 12) -> str:
    """Enumeração legível dos órfãos: os primeiros `limite`, e a contagem do resto."""
    lista = list(itens)
    if len(lista) <= limite:
        return ", ".join(lista)
    return f"{', '.join(lista[:limite])} … (+{len(lista) - limite})"


def falhar_por_conteudo_ausente(
    codigo: str,
    verifica: str,
    falta: str,
    requisitos: str,
    orfaos: Sequence[str] = (),
    rotulo_dos_orfaos: str = "elemento(s) órfão(s)",
    observacoes: Sequence[str] = (),
) -> NoReturn:
    """Falha padronizada de meta-teste: nomeia o que falta, o requisito e os órfãos.

    A mensagem é o produto do meta-teste. Ela existe para que a revisão saiba, sem abrir o
    design, qual conteúdo está faltando e qual requisito o exige.
    """
    linhas = [
        f"{codigo} — {verifica}",
        f"Conteúdo ausente: {falta}",
        f"Exigido por: {requisitos}",
    ]
    if orfaos:
        linhas.append(f"{len(orfaos)} {rotulo_dos_orfaos}: {amostra(orfaos)}")
    linhas.extend(observacoes)
    pytest.fail("\n".join(linhas))


__all__ = [
    "CAMINHO_DO_DESIGN",
    "CAMINHO_DO_REQUIREMENTS",
    "DIRETORIO_DA_SPEC",
    "NOME_DA_SPEC",
    "RAIZ_DO_PROJETO",
    "amostra",
    "caminho_ausente",
    "criterios_por_requisito",
    "falhar_por_conteudo_ausente",
    "identificadores",
    "itens_enumerados",
    "modulo_opcional",
    "secao",
    "simbolo_opcional",
    "tabela_apos",
    "texto_do_design",
    "texto_do_requirements",
]
