"""`MT-10` — isolamento do núcleo.

**O que verifica** (`R71.1`, `R71.2`, `R98.5`, `R119.3`, `D101`): nenhum módulo do núcleo —
`radar/nucleo/**`, `radar/motores/**`, `radar/pipeline/**`, `radar/regras/**`, `radar/radar/**` —
importa, direta ou **transitivamente**, cliente de modelo de linguagem (`langchain*`, `langgraph`,
`openai` ou equivalente), cliente de embedding, cliente de armazenamento externo (`boto3` ou
equivalente) ou cliente de agendamento. A direção das dependências é única: o núcleo declara o
contrato, o adaptador o implementa, e o núcleo nunca conhece o adaptador.

**Como falha**: import proibido introduzido, com o **caminho completo** do módulo do núcleo até o
cliente externo; ou pacote do núcleo ausente, nomeando o pacote.

**Estado hoje**: a varredura transitiva dos pacotes já existentes — `radar/nucleo`,
`radar/motores`, `radar/pipeline` — não encontra import proibido, e é executada de fato. A falha é
por conteúdo ausente: `radar/regras/**` e `radar/radar/**`, que são núcleo por `D101`, ainda não
existem.
"""

from __future__ import annotations

import ast
from pathlib import Path

from testes.meta.apoio import RAIZ_DO_PROJETO, falhar_por_conteudo_ausente

DIRETORIO_DO_CODIGO = RAIZ_DO_PROJETO / "src"

PACOTES_DO_NUCLEO = (
    "radar/nucleo",
    "radar/motores",
    "radar/pipeline",
    "radar/regras",
    "radar/radar",
)

#: Pacote raiz proibido → espécie de cliente externo que ele representa.
CLIENTES_EXTERNOS: dict[str, str] = {
    "langchain": "cliente de modelo de linguagem",
    "langchain_openai": "cliente de modelo de linguagem",
    "langchain_core": "cliente de modelo de linguagem",
    "langchain_community": "cliente de modelo de linguagem",
    "langgraph": "biblioteca de orquestração de IA",
    "openai": "cliente de modelo de linguagem",
    "anthropic": "cliente de modelo de linguagem",
    "tiktoken": "cliente de modelo de linguagem",
    "sentence_transformers": "cliente de embedding",
    "boto3": "cliente de armazenamento externo",
    "botocore": "cliente de armazenamento externo",
    "s3transfer": "cliente de armazenamento externo",
    "apscheduler": "cliente de agendamento",
    "celery": "cliente de agendamento",
    "croniter": "cliente de agendamento",
}


def _modulos_do_projeto() -> dict[str, Path]:
    """Nome de módulo importável → arquivo, para tudo que vive em `src/radar/**`."""
    modulos: dict[str, Path] = {}
    for arquivo in sorted(DIRETORIO_DO_CODIGO.rglob("*.py")):
        partes = arquivo.relative_to(DIRETORIO_DO_CODIGO).with_suffix("").parts
        if partes[-1] == "__init__":
            partes = partes[:-1]
        modulos[".".join(partes)] = arquivo
    return modulos


def _importados_por(arquivo: Path) -> list[str]:
    """Módulos importados pelo arquivo, em qualquer profundidade da árvore sintática."""
    arvore = ast.parse(arquivo.read_text(encoding="utf-8"), filename=str(arquivo))
    importados: list[str] = []
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            importados.extend(alias.name for alias in no.names)
        elif isinstance(no, ast.ImportFrom) and no.level == 0 and no.module:
            importados.append(no.module)
    return importados


def _caminho_proibido(
    modulo: str, modulos: dict[str, Path], visitados: set[str]
) -> list[str] | None:
    """Caminho de imports do módulo até um cliente externo, ou `None` quando não há."""
    if modulo in visitados:
        return None
    visitados.add(modulo)
    for importado in _importados_por(modulos[modulo]):
        raiz = importado.split(".")[0]
        if raiz in CLIENTES_EXTERNOS:
            return [modulo, f"{importado} ({CLIENTES_EXTERNOS[raiz]})"]
        alvo = importado if importado in modulos else None
        if alvo is None and importado.rsplit(".", 1)[0] in modulos:
            # `from radar.nucleo.enumeracoes import X` resolvido para o módulo que o contém.
            alvo = importado.rsplit(".", 1)[0]
        if alvo is not None:
            continuacao = _caminho_proibido(alvo, modulos, visitados)
            if continuacao is not None:
                return [modulo, *continuacao]
    return None


def _modulos_do_nucleo(modulos: dict[str, Path]) -> list[str]:
    prefixos = tuple(pacote.replace("/", ".") + "." for pacote in PACOTES_DO_NUCLEO)
    return sorted(nome for nome in modulos if nome.startswith(prefixos))


def test_mt_10_nenhum_modulo_do_nucleo_importa_cliente_externo() -> None:
    modulos = _modulos_do_projeto()
    violacoes: list[str] = []
    for modulo in _modulos_do_nucleo(modulos):
        caminho = _caminho_proibido(modulo, modulos, set())
        if caminho is not None:
            violacoes.append(" → ".join(caminho))
    assert not violacoes, (
        "MT-10 — import proibido no núcleo, com o caminho completo. O núcleo declara o "
        "contrato e nunca conhece o adaptador (`R119.3`):\n" + "\n".join(violacoes)
    )


def test_mt_10_os_cinco_pacotes_do_nucleo_existem() -> None:
    ausentes = [
        pacote for pacote in PACOTES_DO_NUCLEO if not (DIRETORIO_DO_CODIGO / pacote).is_dir()
    ]
    if ausentes:
        falhar_por_conteudo_ausente(
            codigo="MT-10",
            verifica="isolamento do núcleo: nenhum módulo de `radar/nucleo/**`, "
            "`radar/motores/**`, `radar/pipeline/**`, `radar/regras/**` e `radar/radar/**` "
            "importa cliente externo",
            falta="pacote(s) do núcleo em `src/`",
            requisitos="R71.1, R71.2, R98.5, R119.3",
            orfaos=ausentes,
            rotulo_dos_orfaos="pacote(s) do núcleo sem módulo a verificar",
            observacoes=[
                "A varredura transitiva dos pacotes já existentes foi executada e não "
                "encontrou import proibido.",
            ],
        )
