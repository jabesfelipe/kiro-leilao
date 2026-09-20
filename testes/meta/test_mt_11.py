"""`MT-11` — convenção de idioma na barreira de integração.

**O que verifica** (`D72`, `D103`, `R94.2`, `R97.3`): os identificadores de implementação de
`src/radar/**`, de `scripts/**` e de `db/schema.sql` — módulos, pacotes, classes, funções,
métodos, parâmetros, atributos, constantes, tabelas, colunas, índices, enums e valores de enum —
estão em **português**. As declarações Python são colhidas da **árvore sintática** (`ast`), nunca
por semelhança de texto: o que entra na verificação é declaração de fato, com a linha que o
compilador atribui a ela. O esquema é percorrido instrução a instrução, com a linha preservada.

Cobre também as **correspondências obrigatórias de `D103`**: `ProvedorDeModeloDeLinguagem`,
`ProvedorDeEmbedding`, `EstrategiaDeCaptura`, `VersaoDoMotor`, `DataDeCorte`,
`IdentificadorDeCorrelacao` e `OrcamentoDeExecucaoDeIA` têm **um** nome no projeto. Sinônimo novo
para termo já nomeado é defeito de redação, não variação de estilo.

**Como falha**: nomeando o **identificador**, o **arquivo** e a **linha** de cada achado, com o
termo em inglês encontrado e o identificador em português que o substitui, mais a contagem por
arquivo. O dicionário de exceções vive em `testes/meta/dicionario_de_idioma.toml` — **dado
versionado**, não lista embutida aqui. Acrescentar entrada a ele aparece no diff, tem motivo
declarado e passa por revisão: não existe escape silencioso. Este teste também verifica que a
classe `[tecnologia]` do dicionário não ultrapassa a lista **fechada** de `D72` e `D103`, o que
impede inflar a exceção disfarçando-a de nome de tecnologia.

**Estado hoje**: falha, e a falha é o ponto. Os módulos legados em inglês continuam em
`src/radar/**` — `capture/`, `domain/`, `engines/`, `orchestration/`, `pipeline/legal_gate.py`,
`services/analysis_service.py`, `db/{models,repository,session}.py`, `config.py` —, `scripts/**`
tem identificadores em inglês e `db/schema.sql` nomeia tabelas, colunas, índices e enums em
inglês. `MT-11` é o portão que a renomeação da tarefa 4.1 tem de fazer passar, e entra na barreira
de integração junto com `ruff` e `mypy --strict` **desde o passo 1** de `D91`.
"""

from __future__ import annotations

import ast
import re
import tomllib
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Final

import pytest

from testes.meta.apoio import RAIZ_DO_PROJETO, amostra

CAMINHO_DO_DICIONARIO: Final[Path] = Path(__file__).with_name("dicionario_de_idioma.toml")
DIRETORIOS_DE_PYTHON: Final[tuple[str, ...]] = ("src/radar", "scripts")
ESQUEMA: Final[str] = "db/schema.sql"
REQUISITOS: Final[str] = "R94.2, R97.3"

#: Lista **fechada** de tecnologia e biblioteca externa admitida em inglês: é a declarada na
#: *Convenção de idioma* do design (`D72`) mais as exceções de `D103`. Vive aqui, e não no
#: dicionário, porque é norma da especificação: o dicionário é verificado contra ela.
TECNOLOGIA_DE_D72: Final[frozenset[str]] = frozenset(
    {
        "FastAPI",
        "LangGraph",
        "LangChain",
        "SQLAlchemy",
        "pgvector",
        "PostgreSQL",
        "hypothesis",
        "pytest",
        "ruff",
        "mypy",
        "pydantic",
        "React",
        "Decimal",
        "IntEnum",
        "StrEnum",
        "Protocol",
        "UUID",
        "MCP",
        "RAG",
        "OCR",
        "S3",
        "OpenAI",
        "Bedrock",
        "cron",
    }
)


@dataclass(frozen=True, slots=True)
class Correspondencia:
    """Termo de `D103` com nome único no projeto e os sinônimos que o defeituariam."""

    identificador: str
    requisito: str
    sinonimos: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DicionarioDeIdioma:
    """Conteúdo de `dicionario_de_idioma.toml`, validado campo a campo na leitura."""

    termos_em_ingles: dict[str, str]
    tecnologia: tuple[str, ...]
    reservadas: tuple[str, ...]
    contrato: tuple[tuple[str, str], ...]
    codigos_estaveis: tuple[re.Pattern[str], ...]
    correspondencias: tuple[Correspondencia, ...]

    @property
    def dispensas_de_identificador(self) -> frozenset[str]:
        """Exceções comparadas com o identificador inteiro, na forma normalizada."""
        return frozenset(
            _normalizar(termo)
            for termo in (
                *self.tecnologia,
                *(termo for termo, _ in self.contrato),
                *(item.identificador for item in self.correspondencias),
            )
        )

    @property
    def dispensas_de_termo(self) -> frozenset[str]:
        """Exceções comparadas termo a termo do identificador."""
        return self.dispensas_de_identificador | frozenset(
            _normalizar(termo) for termo in self.reservadas
        )


@dataclass(frozen=True, slots=True)
class Declaracao:
    """Identificador declarado, com o arquivo e a linha em que a declaração está."""

    arquivo: str
    linha: int
    especie: str
    identificador: str


@dataclass(frozen=True, slots=True)
class Achado:
    """Termo em inglês encontrado num identificador declarado."""

    declaracao: Declaracao
    termo: str
    equivalente: str

    def __str__(self) -> str:
        return (
            f"{self.declaracao.arquivo}:{self.declaracao.linha} "
            f"{self.declaracao.especie} `{self.declaracao.identificador}` — "
            f"`{self.termo}` está em inglês; em português: `{self.equivalente}`"
        )


def _normalizar(identificador: str) -> str:
    """Forma comparável: sem separadores e sem caixa. `Tenant_Id` e `tenantid` coincidem."""
    return re.sub(r"[^0-9a-z]", "", identificador.lower())


def _exigir_tabela(dados: dict[str, object], chave: str) -> dict[str, object]:
    valor = dados.get(chave)
    if not isinstance(valor, dict):
        pytest.fail(f"MT-11 — `{CAMINHO_DO_DICIONARIO.name}` sem a tabela `[{chave}]`.")
    return valor


def _exigir_textos(dados: dict[str, object], chave: str, contexto: str) -> tuple[str, ...]:
    valor = dados.get(chave)
    if not isinstance(valor, list) or not all(isinstance(item, str) for item in valor):
        pytest.fail(f"MT-11 — `{contexto}.{chave}` deve ser uma lista de textos.")
    return tuple(str(item) for item in valor)


def _exigir_texto(dados: dict[str, object], chave: str, contexto: str) -> str:
    valor = dados.get(chave)
    if not isinstance(valor, str) or not valor.strip():
        pytest.fail(f"MT-11 — `{contexto}.{chave}` deve ser um texto não vazio.")
    return valor


def _exigir_tabelas(dados: dict[str, object], chave: str) -> tuple[dict[str, object], ...]:
    valor = dados.get(chave)
    if not isinstance(valor, list) or not all(isinstance(item, dict) for item in valor):
        pytest.fail(f"MT-11 — `{CAMINHO_DO_DICIONARIO.name}` sem as entradas `[[{chave}]]`.")
    return tuple(item for item in valor if isinstance(item, dict))


@cache
def dicionario() -> DicionarioDeIdioma:
    """Lê o dicionário versionado. Ausência é falha com o caminho procurado."""
    if not CAMINHO_DO_DICIONARIO.is_file():
        pytest.fail(
            f"MT-11 — dicionário de exceções ausente: {CAMINHO_DO_DICIONARIO}. As exceções são "
            "dado versionado em arquivo próprio, não lista embutida no teste."
        )
    with CAMINHO_DO_DICIONARIO.open("rb") as arquivo:
        bruto: dict[str, object] = tomllib.load(arquivo)

    termos: dict[str, str] = {}
    for termo, equivalente in _exigir_tabela(bruto, "termos_em_ingles").items():
        if not isinstance(equivalente, str) or not equivalente.strip():
            pytest.fail(f"MT-11 — `termos_em_ingles.{termo}` deve declarar o termo em português.")
        termos[termo.lower()] = equivalente

    padroes: list[re.Pattern[str]] = []
    for padrao in _exigir_textos(_exigir_tabela(bruto, "codigos_estaveis"), "padroes", "codigos"):
        try:
            padroes.append(re.compile(padrao))
        except re.error as erro:
            pytest.fail(f"MT-11 — padrão de código estável inválido {padrao!r}: {erro}")

    correspondencias = tuple(
        Correspondencia(
            identificador=_exigir_texto(entrada, "identificador", "correspondencias_obrigatorias"),
            requisito=_exigir_texto(entrada, "requisito", "correspondencias_obrigatorias"),
            sinonimos=_exigir_textos(entrada, "sinonimos", "correspondencias_obrigatorias"),
        )
        for entrada in _exigir_tabelas(bruto, "correspondencias_obrigatorias")
    )

    return DicionarioDeIdioma(
        termos_em_ingles=termos,
        tecnologia=_exigir_textos(_exigir_tabela(bruto, "tecnologia"), "termos", "tecnologia"),
        reservadas=_exigir_textos(_exigir_tabela(bruto, "reservadas"), "termos", "reservadas"),
        contrato=tuple(
            (
                _exigir_texto(entrada, "termo", "contrato"),
                _exigir_texto(entrada, "motivo", "contrato"),
            )
            for entrada in _exigir_tabelas(bruto, "contrato")
        ),
        codigos_estaveis=tuple(padroes),
        correspondencias=correspondencias,
    )


_FRONTEIRA_DE_CAIXA: Final[re.Pattern[str]] = re.compile(
    r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])"
)
_SEPARADOR: Final[re.Pattern[str]] = re.compile(r"[^0-9A-Za-z]+")


def _termos(identificador: str) -> tuple[str, ...]:
    """Termos de um identificador: separa por `_`, por `-` e por fronteira de caixa.

    `LLMProvider` → `llm`, `provider`. `legal_status` → `legal`, `status`. `area_m2` → `area`,
    `m2`. A separação é estrutural, não semântica: o julgamento de idioma é do dicionário.
    """
    palavras: list[str] = []
    for parte in _SEPARADOR.split(identificador):
        palavras.extend(pedaco.lower() for pedaco in _FRONTEIRA_DE_CAIXA.split(parte) if pedaco)
    return tuple(palavras)


def _radicais(termo: str) -> tuple[str, ...]:
    """O termo e os radicais do seu plural em inglês (`-s`, `-es`, `-ies`, `-ses`).

    `sources` → `source`; `analyses` → `analysis`; `properties` → `property`. É o que permite
    julgar `CREATE TABLE properties` sem exigir uma entrada de dicionário para cada plural.
    """
    candidatos = [termo]
    if termo.endswith("ies") and len(termo) > 4:
        candidatos.append(f"{termo[:-3]}y")
    if termo.endswith("ses") and len(termo) > 4:
        candidatos.append(f"{termo[:-3]}sis")
    if termo.endswith("es") and len(termo) > 3:
        candidatos.append(termo[:-2])
    if termo.endswith("s") and len(termo) > 2:
        candidatos.append(termo[:-1])
    return tuple(candidatos)


def _achados_de(declaracao: Declaracao, dic: DicionarioDeIdioma) -> Iterator[Achado]:
    """Termos em inglês do identificador, já descontadas as exceções permitidas."""
    identificador = declaracao.identificador
    if identificador.startswith("__") and identificador.endswith("__"):
        return
    if _normalizar(identificador) in dic.dispensas_de_identificador:
        return
    if any(padrao.fullmatch(identificador) for padrao in dic.codigos_estaveis):
        return

    dispensas = dic.dispensas_de_termo
    for termo in _termos(identificador):
        if termo in dispensas:
            continue
        for radical in _radicais(termo):
            equivalente = dic.termos_em_ingles.get(radical)
            if equivalente is not None:
                yield Achado(declaracao=declaracao, termo=termo, equivalente=equivalente)
                break


def _arquivos_de_python() -> list[Path]:
    arquivos: list[Path] = []
    for diretorio in DIRETORIOS_DE_PYTHON:
        arquivos.extend(sorted((RAIZ_DO_PROJETO / diretorio).rglob("*.py")))
    return arquivos


def _relativo(arquivo: Path) -> str:
    return arquivo.relative_to(RAIZ_DO_PROJETO).as_posix()


def _nomes_do_alvo(alvo: ast.expr) -> Iterator[str]:
    """Nomes declarados por um alvo de atribuição, inclusive em tupla."""
    if isinstance(alvo, ast.Name):
        yield alvo.id
    elif isinstance(alvo, ast.Tuple | ast.List):
        for item in alvo.elts:
            yield from _nomes_do_alvo(item)


def _parametros(
    arquivo: str, funcao: ast.FunctionDef | ast.AsyncFunctionDef
) -> Iterator[Declaracao]:
    argumentos = funcao.args
    todos = [
        *argumentos.posonlyargs,
        *argumentos.args,
        *argumentos.kwonlyargs,
        *(item for item in (argumentos.vararg, argumentos.kwarg) if item is not None),
    ]
    for argumento in todos:
        yield Declaracao(arquivo, argumento.lineno, "parâmetro", argumento.arg)


def _e_enum(classe: ast.ClassDef) -> bool:
    """Classe de enumeração: alguma base se chama `Enum`, `IntEnum`, `StrEnum` ou similar."""
    nomes = [base.id for base in classe.bases if isinstance(base, ast.Name)]
    nomes += [base.attr for base in classe.bases if isinstance(base, ast.Attribute)]
    return any(nome.endswith("Enum") for nome in nomes)


def _declaracoes_do_corpo(
    arquivo: str, corpo: list[ast.stmt], *, escopo_de_enum: bool, escopo_de_classe: bool
) -> Iterator[Declaracao]:
    """Declarações de um corpo de módulo ou de classe, sem descer em corpo de função.

    Variável local não é identificador de barreira de integração: o que atravessa a fronteira é
    o nome público — módulo, classe, função, parâmetro, atributo, constante e valor de enum.
    """
    for no in corpo:
        if isinstance(no, ast.ClassDef):
            enum = _e_enum(no)
            yield Declaracao(arquivo, no.lineno, "enum" if enum else "classe", no.name)
            yield from _declaracoes_do_corpo(
                arquivo, no.body, escopo_de_enum=enum, escopo_de_classe=True
            )
        elif isinstance(no, ast.FunctionDef | ast.AsyncFunctionDef):
            especie = "método" if escopo_de_classe else "função"
            yield Declaracao(arquivo, no.lineno, especie, no.name)
            yield from _parametros(arquivo, no)
        elif isinstance(no, ast.Assign | ast.AnnAssign):
            if escopo_de_enum:
                especie = "valor de enum"
            elif escopo_de_classe:
                especie = "atributo"
            else:
                especie = "constante"
            alvos = no.targets if isinstance(no, ast.Assign) else [no.target]
            for alvo in alvos:
                for nome in _nomes_do_alvo(alvo):
                    yield Declaracao(arquivo, no.lineno, especie, nome)
        elif isinstance(no, ast.TypeAlias) and isinstance(no.name, ast.Name):
            yield Declaracao(arquivo, no.lineno, "apelido de tipo", no.name.id)
        elif isinstance(no, ast.If | ast.For | ast.While):
            yield from _declaracoes_do_corpo(
                arquivo, [*no.body, *no.orelse], escopo_de_enum=escopo_de_enum,
                escopo_de_classe=escopo_de_classe,
            )
        elif isinstance(no, ast.With):
            yield from _declaracoes_do_corpo(
                arquivo, no.body, escopo_de_enum=escopo_de_enum,
                escopo_de_classe=escopo_de_classe,
            )
        elif isinstance(no, ast.Try):
            aninhados = [*no.body, *no.orelse, *no.finalbody]
            for manipulador in no.handlers:
                aninhados.extend(manipulador.body)
            yield from _declaracoes_do_corpo(
                arquivo, aninhados, escopo_de_enum=escopo_de_enum,
                escopo_de_classe=escopo_de_classe,
            )


def _declaracoes_de_python() -> Iterator[Declaracao]:
    """Módulos, pacotes e tudo que a árvore sintática declara em `src/radar/**` e `scripts/**`."""
    for arquivo in _arquivos_de_python():
        relativo = _relativo(arquivo)
        if arquivo.stem == "__init__":
            yield Declaracao(relativo, 1, "pacote", arquivo.parent.name)
        else:
            yield Declaracao(relativo, 1, "módulo", arquivo.stem)
        arvore = ast.parse(arquivo.read_text(encoding="utf-8"), filename=str(arquivo))
        yield from _declaracoes_do_corpo(
            relativo, arvore.body, escopo_de_enum=False, escopo_de_classe=False
        )


_CRIAR_TABELA: Final[re.Pattern[str]] = re.compile(
    r"^\s*CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([\w.]+)", re.IGNORECASE
)
_CRIAR_INDICE: Final[re.Pattern[str]] = re.compile(
    r"^\s*CREATE\s+(?:UNIQUE\s+)?INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?([\w.]+)", re.IGNORECASE
)
_CRIAR_ENUM: Final[re.Pattern[str]] = re.compile(
    r"^\s*CREATE\s+TYPE\s+([\w.]+)\s+AS\s+ENUM", re.IGNORECASE
)
_COLUNA: Final[re.Pattern[str]] = re.compile(r"^\s{2,}(\w+)\s")
_VALOR_DE_ENUM: Final[re.Pattern[str]] = re.compile(r"'([^']+)'")

#: Primeira palavra de uma linha do corpo de `CREATE TABLE` que declara restrição, não coluna.
_RESTRICOES: Final[frozenset[str]] = frozenset(
    {"unique", "primary", "check", "constraint", "foreign", "exclude", "references", "like"}
)


def _declaracoes_do_esquema() -> Iterator[Declaracao]:
    """Tabelas, colunas, índices, enums e valores de enum de `db/schema.sql`, com a linha.

    O esquema não tem árvore sintática de Python a percorrer; a varredura é por instrução, com
    a linha preservada, e distingue corpo de tabela de declaração de restrição para não tomar
    `UNIQUE (...)` por nome de coluna.
    """
    caminho = RAIZ_DO_PROJETO / ESQUEMA
    if not caminho.is_file():
        return
    relativo = _relativo(caminho)
    dentro_da_tabela = False
    enum_em_aberto: str | None = None
    for numero, linha in enumerate(caminho.read_text(encoding="utf-8").splitlines(), start=1):
        if enum_em_aberto is not None:
            for valor in _VALOR_DE_ENUM.findall(linha):
                yield Declaracao(relativo, numero, "valor de enum", valor)
            if ";" in linha:
                enum_em_aberto = None
            continue

        enum = _CRIAR_ENUM.match(linha)
        if enum is not None:
            yield Declaracao(relativo, numero, "enum", enum.group(1))
            enum_em_aberto = enum.group(1)
            for valor in _VALOR_DE_ENUM.findall(linha):
                yield Declaracao(relativo, numero, "valor de enum", valor)
            if ";" in linha.split("ENUM", 1)[1]:
                enum_em_aberto = None
            continue

        tabela = _CRIAR_TABELA.match(linha)
        if tabela is not None:
            yield Declaracao(relativo, numero, "tabela", tabela.group(1))
            dentro_da_tabela = True
            continue

        indice = _CRIAR_INDICE.match(linha)
        if indice is not None:
            yield Declaracao(relativo, numero, "índice", indice.group(1))
            continue

        if dentro_da_tabela:
            if linha.startswith(")"):
                dentro_da_tabela = False
                continue
            coluna = _COLUNA.match(linha)
            if coluna is not None and coluna.group(1).lower() not in _RESTRICOES:
                yield Declaracao(relativo, numero, "coluna", coluna.group(1))


def declaracoes() -> list[Declaracao]:
    """Todas as declarações de implementação sob a convenção de idioma, sem repetição."""
    vistas: set[tuple[str, int, str, str]] = set()
    resultado: list[Declaracao] = []
    for declaracao in (*_declaracoes_de_python(), *_declaracoes_do_esquema()):
        chave = (
            declaracao.arquivo,
            declaracao.linha,
            declaracao.especie,
            declaracao.identificador,
        )
        if chave not in vistas:
            vistas.add(chave)
            resultado.append(declaracao)
    return resultado


def _mensagem(achados: list[Achado]) -> str:
    por_arquivo: dict[str, int] = {}
    for achado in achados:
        arquivo = achado.declaracao.arquivo
        por_arquivo[arquivo] = por_arquivo.get(arquivo, 0) + 1
    ordenados = sorted(por_arquivo.items(), key=lambda item: (-item[1], item[0]))
    return "\n".join(
        [
            f"MT-11 — identificador em inglês fora das exceções permitidas (`D72`, {REQUISITOS}).",
            f"{len(achados)} achado(s) em {len(por_arquivo)} arquivo(s):",
            *(f"  {arquivo}: {quantidade}" for arquivo, quantidade in ordenados),
            "Identificador, arquivo e linha de cada achado:",
            *(f"  {achado}" for achado in achados),
            f"As exceções permitidas são dado versionado em `{_relativo(CAMINHO_DO_DICIONARIO)}`; "
            "acrescentar entrada a ele é mudança revisável, não escape silencioso.",
        ]
    )


def test_mt_11_a_barreira_cobre_os_tres_alvos_da_convencao_de_idioma() -> None:
    """A falha de `MT-11` tem de ser por conteúdo em inglês, nunca por coleta vazia."""
    ausentes = [
        alvo
        for alvo in (*DIRETORIOS_DE_PYTHON, ESQUEMA)
        if not (RAIZ_DO_PROJETO / alvo).exists()
    ]
    assert not ausentes, (
        f"MT-11 — alvo da convenção de idioma ausente do repositório: {ausentes}. `D72` aplica-se "
        "a `src/radar/**`, a `scripts/**` e a `db/schema.sql`."
    )

    coletadas = declaracoes()
    arquivos = {declaracao.arquivo for declaracao in coletadas}
    sem_declaracao = [
        alvo
        for alvo in (*DIRETORIOS_DE_PYTHON, ESQUEMA)
        if not any(arquivo.startswith(alvo) for arquivo in arquivos)
    ]
    assert not sem_declaracao, (
        f"MT-11 — nenhuma declaração colhida de {sem_declaracao}: a varredura não pode passar por "
        "coleta vazia."
    )


def test_mt_11_o_dicionario_de_excecoes_declara_apenas_as_classes_permitidas() -> None:
    """Exceção fora das três classes de `D72` é inflar a lista, e é isto que falha aqui."""
    dic = dicionario()
    permitida = {_normalizar(termo) for termo in TECNOLOGIA_DE_D72}
    excedentes = sorted(
        termo for termo in dic.tecnologia if _normalizar(termo) not in permitida
    )
    assert not excedentes, (
        "MT-11 — `[tecnologia]` do dicionário ultrapassa a lista fechada de `D72` e `D103`: "
        f"{excedentes}. Nome que não é de tecnologia externa não entra por esta porta."
    )

    sem_motivo = [termo for termo, motivo in dic.contrato if not motivo.strip()]
    assert not sem_motivo, (
        f"MT-11 — exceção de contrato sem motivo declarado: {sem_motivo}. O motivo é o que a "
        "revisão julga."
    )

    mal_formados = sorted(
        termo
        for termo in dic.termos_em_ingles
        if termo != _normalizar(termo) or not termo.isascii()
    )
    assert not mal_formados, (
        f"MT-11 — termo do vocabulário em inglês fora da forma comparável: {mal_formados}."
    )

    assert dic.termos_em_ingles, "MT-11 — vocabulário em inglês vazio não julga identificador."
    assert dic.correspondencias, "MT-11 — correspondências obrigatórias de `D103` ausentes."


def test_mt_11_os_identificadores_de_implementacao_estao_em_portugues() -> None:
    dic = dicionario()
    achados = [
        achado
        for declaracao in declaracoes()
        for achado in _achados_de(declaracao, dic)
    ]
    if achados:
        pytest.fail(_mensagem(achados))


def test_mt_11_as_correspondencias_obrigatorias_de_d103_tem_nome_unico() -> None:
    """Sinônimo de termo já nomeado por `D103` é defeito de redação, não variação de estilo."""
    dic = dicionario()
    proibidos = {
        _normalizar(sinonimo): item
        for item in dic.correspondencias
        for sinonimo in item.sinonimos
    }
    violacoes = [
        f"{declaracao.arquivo}:{declaracao.linha} {declaracao.especie} "
        f"`{declaracao.identificador}` — sinônimo de "
        f"`{proibidos[_normalizar(declaracao.identificador)].identificador}` "
        f"({proibidos[_normalizar(declaracao.identificador)].requisito})"
        for declaracao in declaracoes()
        if _normalizar(declaracao.identificador) in proibidos
    ]
    assert not violacoes, (
        "MT-11 — sinônimo de termo já nomeado pelas correspondências obrigatórias de `D103`. "
        f"Cada termo tem **um** nome no projeto: {amostra(violacoes)}"
    )
