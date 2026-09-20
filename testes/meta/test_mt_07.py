"""`MT-07` — ponto único de verdade da tabela `STR`.

**O que verifica** (`R62.10`, `R73.7`, `D101`): as **três** representações dos limiares por
estratégia coincidem — a tabela `STR` do `requirements.md`, as constantes Python e o seed do
banco. O seed é **gerado** a partir da tabela, nunca escrito à mão, e as constantes Python
subsistem apenas como valores de arranque que alimentam o gerador.

**Como falha**: qualquer divergência entre as três representações, nomeando a estratégia, o
limiar e os valores encontrados em cada representação.

**Estado hoje**: falha por conteúdo ausente. A tabela `STR` existe e é conferida aqui — seis
estratégias e seis limiares —, e as outras duas representações não existem. Este é o defeito
registrado no design: o mesmo limiar vivia em três lugares sem nada garantindo convergência.
"""

from __future__ import annotations

from testes.meta.apoio import (
    caminho_ausente,
    falhar_por_conteudo_ausente,
    simbolo_opcional,
    tabela_apos,
    texto_do_requirements,
)

MARCADOR_DA_TABELA = "### STR — Thresholds por Estratégia"
ESTRATEGIAS = ("revenda", "renda", "valorizacao", "mcmv", "terreno", "customizada")
LIMIARES = (
    "desconto_liquido_min",
    "margem_min",
    "yield_liquido_mensal_min",
    "liquidez_min",
    "prazo_saida_max",
    "ticket_max",
)

MODULO_DAS_CONSTANTES = "radar.motores.estrategia"
SIMBOLO_DAS_CONSTANTES = "LimitesDaEstrategia"
SEED_DO_BANCO = "db/seeds/estrategias.sql"


def _tabela_str() -> list[list[str]]:
    return tabela_apos(texto_do_requirements(), MARCADOR_DA_TABELA)


def test_mt_07_a_tabela_str_declara_seis_estrategias_e_seis_limiares() -> None:
    tabela = _tabela_str()
    cabecalho = [celula.strip("`") for celula in tabela[0]]
    linhas = tabela[1:]

    assert cabecalho[1:] == list(LIMIARES), (
        f"MT-07 — os seis limiares da tabela `STR` são {LIMIARES}; cabeçalho encontrado: "
        f"{cabecalho[1:]}"
    )
    estrategias = tuple(linha[0].strip("`") for linha in linhas)
    assert estrategias == ESTRATEGIAS, (
        f"MT-07 — a tabela `STR` declara as estratégias {ESTRATEGIAS}; encontradas {estrategias}"
    )
    sem_todas_as_colunas = [
        linha[0] for linha in linhas if len(linha) != len(LIMIARES) + 1 or any(not c for c in linha)
    ]
    assert not sem_todas_as_colunas, (
        f"MT-07 — estratégia com limiar em branco na tabela `STR`: {sem_todas_as_colunas}"
    )


def test_mt_07_as_tres_representacoes_de_str_coincidem() -> None:
    constantes = simbolo_opcional(MODULO_DAS_CONSTANTES, SIMBOLO_DAS_CONSTANTES)
    seed_ausente = caminho_ausente(SEED_DO_BANCO)

    representacoes_ausentes: list[str] = []
    if constantes is None:
        representacoes_ausentes.append(
            f"constantes Python (`{SIMBOLO_DAS_CONSTANTES}` em `{MODULO_DAS_CONSTANTES}`)"
        )
    if seed_ausente:
        representacoes_ausentes.append(f"seed do banco (`{SEED_DO_BANCO}`, gerado a partir de STR)")

    if representacoes_ausentes:
        orfaos = [
            f"{estrategia}.{limiar}" for estrategia in ESTRATEGIAS for limiar in LIMIARES
        ]
        falhar_por_conteudo_ausente(
            codigo="MT-07",
            verifica="tabela `STR` do requirements, constantes Python e seed do banco coincidem",
            falta=" e ".join(representacoes_ausentes),
            requisitos="R62.10, R73.7",
            orfaos=orfaos,
            rotulo_dos_orfaos="limiar(es) de estratégia sem as três representações",
            observacoes=[
                "Enquanto duas das três representações não existem, não há o que comparar: a "
                "tabela do documento é a única fonte, e é ela que gera as outras duas.",
            ],
        )
