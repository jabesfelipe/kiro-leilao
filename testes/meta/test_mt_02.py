"""`MT-02` — um teste por propriedade.

**O que verifica** (`R73.2`, `R73.10`, `D101`): cada uma das **262** propriedades numeradas no
design tem **exatamente um** teste em `testes/propriedades/` com a etiqueta `Property {n}`.

**Como falha**: propriedade sem teste, nomeando o número e o identificador de origem; ou duas
etiquetas para a mesma propriedade, nomeando os arquivos que a reivindicam.

**Estado hoje**: falha por conteúdo ausente. `testes/propriedades/` existe como pacote e está
vazio de testes — as 262 propriedades entram uma a uma, por família, ao longo dos passos de
`D91`. Enquanto isso, este meta-teste é o inventário do que falta.
"""

from __future__ import annotations

import re
from collections import defaultdict

from testes.meta.apoio import (
    RAIZ_DO_PROJETO,
    falhar_por_conteudo_ausente,
    secao,
    texto_do_design,
)

DIRETORIO_DAS_PROPRIEDADES = RAIZ_DO_PROJETO / "testes" / "propriedades"
TOTAL_DE_PROPRIEDADES = 262
ETIQUETA = re.compile(r"\bProperty\s+(\d+)\b")


def _propriedades_declaradas() -> dict[int, str]:
    """Número da propriedade → identificador de origem, conforme o design."""
    secao_de_propriedades = secao(texto_do_design(), "## Correctness Properties")
    titulos = re.findall(r"^###\s+Property\s+(\d+):\s*(.+)$", secao_de_propriedades, re.MULTILINE)
    declaradas: dict[int, str] = {}
    for numero, titulo in titulos:
        origem = re.search(r"\(`(P\d+\.\d+)`\)\s*$", titulo.strip())
        declaradas[int(numero)] = origem.group(1) if origem else "sem origem declarada"
    return declaradas


def _etiquetas_encontradas() -> dict[int, list[str]]:
    """Número da propriedade → arquivos que declaram a etiqueta `Property {n}`."""
    encontradas: dict[int, list[str]] = defaultdict(list)
    if not DIRETORIO_DAS_PROPRIEDADES.is_dir():
        return encontradas
    for arquivo in sorted(DIRETORIO_DAS_PROPRIEDADES.rglob("*.py")):
        conteudo = arquivo.read_text(encoding="utf-8")
        relativo = arquivo.relative_to(RAIZ_DO_PROJETO).as_posix()
        for numero in {int(n) for n in ETIQUETA.findall(conteudo)}:
            encontradas[numero].append(relativo)
    return encontradas


def test_mt_02_cada_propriedade_tem_exatamente_um_teste() -> None:
    declaradas = _propriedades_declaradas()
    assert len(declaradas) == TOTAL_DE_PROPRIEDADES, (
        f"MT-02 — o design declara {TOTAL_DE_PROPRIEDADES} propriedades; "
        f"encontradas {len(declaradas)}"
    )

    encontradas = _etiquetas_encontradas()

    duplicadas = [
        f"Property {numero} em {', '.join(arquivos)}"
        for numero, arquivos in sorted(encontradas.items())
        if len(arquivos) > 1
    ]
    assert not duplicadas, (
        "MT-02 — duas ou mais etiquetas para a mesma propriedade. A correspondência é um para "
        f"um: {'; '.join(duplicadas)}"
    )

    etiquetas_sem_propriedade = sorted(set(encontradas) - set(declaradas))
    assert not etiquetas_sem_propriedade, (
        "MT-02 — etiqueta `Property {n}` sem propriedade correspondente no design: "
        f"{etiquetas_sem_propriedade}"
    )

    sem_teste = [
        f"Property {numero} ({declaradas[numero]})"
        for numero in sorted(declaradas)
        if numero not in encontradas
    ]
    if sem_teste:
        falhar_por_conteudo_ausente(
            codigo="MT-02",
            verifica="cada uma das 262 propriedades tem exatamente um teste "
            "com a etiqueta `Property {n}`",
            falta=f"testes de propriedade em {DIRETORIO_DAS_PROPRIEDADES.name}/ "
            "(um arquivo por propriedade, `test_propriedade_NNN.py`)",
            requisitos="R73.2, R73.10",
            orfaos=sem_teste,
            rotulo_dos_orfaos="propriedade(s) sem teste",
        )
