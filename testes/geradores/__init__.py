"""Geradores compartilhados das 262 propriedades, um módulo por domínio (`R73.1`, `R73.2`).

Compartilhar gerador é o que impede que duas propriedades sobre a mesma entidade divirjam na
noção de entrada válida. Aqui não há teste: há **infraestrutura de teste**. Cada módulo declara
os geradores do seu domínio, todos nomeados em português (`D72`, `D103`), e nenhum deles abre
conexão de banco, chamada de rede ou acesso a provedor — as 262 propriedades rodam sem banco,
sem rede e sem provedor.

| Módulo | Domínio |
|--------|---------|
| `escalas` | escalas e escalares, mais os valores de fronteira obrigatórios |
| `captura_e_identidade` | captura, normalização e identidade |
| `juridico_e_evidencia` | gate jurídico, evidência e pendência |
| `mercado_e_economia` | comparável, valuation, custo e economia |
| `risco_liquidez_e_escore` | risco, liquidez, escore e portfólio |
| `decisao_e_lance` | decisão e checklist de lance |
| `governanca` | parâmetros, exceções e base de conhecimento |
| `dominio_o` | documento, versão, checklist, débito, processo, conector e porta |
| `mercado_e_valuation` | conjunto de comparáveis e premissas (`P18`) |
| `infraestrutura_de_ia` | dublês de provedor, prompt, segmento e workflow (`P19`) |
| `aquisicao_resiliente` | execução do Radar, estratégia de captura e idempotência (`P20`) |
| `plataforma` | segredo, arquivo hostil, paginação, multi-titular e evento (`P21`) |
| `experiencia` | tela, resposta, viewport, componente e formulário (`P22`) |

Este pacote reexporta **apenas** `escalas`, porque é o módulo de que todo o resto depende e é onde
vivem os valores de fronteira obrigatórios: eles entram nas estratégias **deliberadamente**, por
`sampled_from`, e ficam publicados como constantes para quem preferir `@example`. Os geradores de
domínio são importados do seu próprio módulo — `from testes.geradores.dominio_o import documento` —
para que a propriedade declare de qual domínio vem a entrada que usa.
"""

from __future__ import annotations

from testes.geradores.escalas import (
    CADEIAS_DE_PERCENTUAL_DE_FRONTEIRA,
    CADEIAS_DECIMAIS_DE_FRONTEIRA,
    FUSO_DE_BRASILIA,
    IDENTIFICADORES_DE_MATERIALIDADE,
    LIMIARES_DE_DECISAO,
    LIMIARES_DE_ESTRATEGIA,
    LIMIARES_NUMERICOS_DE_MATERIALIDADE,
    LIMIARES_QUALITATIVOS_DE_MATERIALIDADE,
    UM_COM_UNIDADE_PORCENTO,
    VALORES_FRACIONARIOS_DE_FRONTEIRA,
    AreaDeclarada,
    LimiaresDeEstrategia,
    PercentualDeclarado,
    area,
    data_hora_br,
    dinheiro,
    escala_de_zero_a_cem,
    informado,
    percentual,
    texto_de_dinheiro,
    texto_de_percentual,
)

__all__ = [
    "CADEIAS_DECIMAIS_DE_FRONTEIRA",
    "CADEIAS_DE_PERCENTUAL_DE_FRONTEIRA",
    "FUSO_DE_BRASILIA",
    "IDENTIFICADORES_DE_MATERIALIDADE",
    "LIMIARES_DE_DECISAO",
    "LIMIARES_DE_ESTRATEGIA",
    "LIMIARES_NUMERICOS_DE_MATERIALIDADE",
    "LIMIARES_QUALITATIVOS_DE_MATERIALIDADE",
    "UM_COM_UNIDADE_PORCENTO",
    "VALORES_FRACIONARIOS_DE_FRONTEIRA",
    "AreaDeclarada",
    "LimiaresDeEstrategia",
    "PercentualDeclarado",
    "area",
    "data_hora_br",
    "dinheiro",
    "escala_de_zero_a_cem",
    "informado",
    "percentual",
    "texto_de_dinheiro",
    "texto_de_percentual",
]
