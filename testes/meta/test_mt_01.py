"""`MT-01` — rastreabilidade das 262 propriedades.

**O que verifica** (`R73.1`, `R73.10`, `D101`): o conjunto de identificadores `P1.1` a `P22.12`
da seção *Correctness Properties* do `requirements.md` é **igual** ao conjunto dos
identificadores de origem das **262** propriedades da seção *Correctness Properties* do
`design.md`, com a **única exceção declarada** de `P7.12` — que é contraexemplo verificado e não
propriedade; e todo requisito citado em `Validates` existe no intervalo de 1 a **126**.

**Como falha**: propriedade acrescentada ou removida de um só lado, nomeando o identificador
órfão de cada lado; propriedade do design sem identificador de origem no título; numeração fora
de 1 a 262; ou citação de requisito inexistente, nomeando a citação.

Este meta-teste tem sujeito **inteiramente na especificação**: o conteúdo que ele confronta
existe hoje, e por isso ele **passa** — e passa a valer como portão contra a próxima propriedade
acrescentada de um lado só.
"""

from __future__ import annotations

import re

from testes.meta.apoio import amostra, secao, texto_do_design, texto_do_requirements

TITULO_DA_SECAO = "## Correctness Properties"
EXCECAO_DECLARADA = "P7.12"
TOTAL_DE_PROPRIEDADES = 262
TOTAL_DE_REQUISITOS = 126


def _identificadores_do_requirements() -> list[str]:
    """Identificadores `Pf.n` das tabelas das 22 famílias do requirements."""
    secao_de_propriedades = secao(texto_do_requirements(), TITULO_DA_SECAO)
    return re.findall(r"^\|\s*(P\d+\.\d+)\s*\|", secao_de_propriedades, re.MULTILINE)


def _propriedades_do_design() -> list[tuple[int, str, str]]:
    """Trincas (número, título, identificador de origem) das propriedades do design."""
    secao_de_propriedades = secao(texto_do_design(), TITULO_DA_SECAO)
    titulos = re.findall(r"^###\s+Property\s+(\d+):\s*(.+)$", secao_de_propriedades, re.MULTILINE)
    propriedades: list[tuple[int, str, str]] = []
    for numero, titulo in titulos:
        origem = re.search(r"\(`(P\d+\.\d+)`\)\s*$", titulo.strip())
        propriedades.append((int(numero), titulo.strip(), origem.group(1) if origem else ""))
    return propriedades


def test_mt_01_toda_propriedade_do_design_declara_identificador_de_origem() -> None:
    propriedades = _propriedades_do_design()
    sem_origem = [
        f"Property {numero}: {titulo}"
        for numero, titulo, origem in propriedades
        if not origem
    ]
    assert not sem_origem, (
        "MT-01 — propriedade do design sem identificador de origem entre parênteses no título, "
        f"o que torna a rastreabilidade não mecânica: {amostra(sem_origem)}"
    )


def test_mt_01_numeracao_das_propriedades_do_design_e_contigua() -> None:
    numeros = [numero for numero, _, _ in _propriedades_do_design()]
    esperados = list(range(1, TOTAL_DE_PROPRIEDADES + 1))
    assert numeros == esperados, (
        f"MT-01 — o design declara {TOTAL_DE_PROPRIEDADES} propriedades numeradas de 1 a "
        f"{TOTAL_DE_PROPRIEDADES}, sem lacuna e em ordem; encontradas {len(numeros)}, "
        f"faltando {amostra([str(n) for n in sorted(set(esperados) - set(numeros))])}, "
        f"sobrando {amostra([str(n) for n in sorted(set(numeros) - set(esperados))])}"
    )


def test_mt_01_conjuntos_de_identificadores_coincidem() -> None:
    do_requirements = _identificadores_do_requirements()
    do_design = [origem for _, _, origem in _propriedades_do_design() if origem]

    repetidos_no_requirements = sorted({i for i in do_requirements if do_requirements.count(i) > 1})
    repetidos_no_design = sorted({i for i in do_design if do_design.count(i) > 1})
    assert not repetidos_no_requirements, (
        f"MT-01 — identificador repetido no requirements: {amostra(repetidos_no_requirements)}"
    )
    assert not repetidos_no_design, (
        f"MT-01 — identificador de origem repetido no design: {amostra(repetidos_no_design)}"
    )

    conjunto_do_requirements = set(do_requirements) - {EXCECAO_DECLARADA}
    conjunto_do_design = set(do_design)

    so_no_requirements = sorted(conjunto_do_requirements - conjunto_do_design)
    so_no_design = sorted(conjunto_do_design - conjunto_do_requirements)
    assert not so_no_requirements and not so_no_design, (
        "MT-01 — propriedade acrescentada ou removida de um lado só.\n"
        f"Sem propriedade correspondente no design: {amostra(so_no_requirements)}\n"
        f"Sem origem no requirements: {amostra(so_no_design)}\n"
        f"A única exceção declarada é {EXCECAO_DECLARADA}, que é contraexemplo e não propriedade."
    )

    assert len(conjunto_do_design) == TOTAL_DE_PROPRIEDADES, (
        f"MT-01 — o total declarado é {TOTAL_DE_PROPRIEDADES} propriedades executáveis; "
        f"o design declara {len(conjunto_do_design)}"
    )


def test_mt_01_requisitos_citados_em_validates_existem() -> None:
    secao_de_propriedades = secao(texto_do_design(), TITULO_DA_SECAO)
    blocos = re.findall(
        r"^\*\*Validates:\s*Requirements?\s*([^*]+)\*\*", secao_de_propriedades, re.MULTILINE
    )
    assert len(blocos) == TOTAL_DE_PROPRIEDADES, (
        f"MT-01 — cada uma das {TOTAL_DE_PROPRIEDADES} propriedades declara um bloco "
        f"`Validates: Requirements`; encontrados {len(blocos)}"
    )

    fora_do_intervalo: list[str] = []
    for bloco in blocos:
        for citacao in re.findall(r"\d+(?:\.\d+)*", bloco):
            requisito = int(citacao.split(".")[0])
            if not 1 <= requisito <= TOTAL_DE_REQUISITOS:
                fora_do_intervalo.append(citacao)
    assert not fora_do_intervalo, (
        f"MT-01 — requisito citado em `Validates` fora do intervalo de 1 a {TOTAL_DE_REQUISITOS}, "
        "o que aponta para critério que só existia em rascunho: "
        f"{amostra(sorted(fora_do_intervalo))}"
    )
