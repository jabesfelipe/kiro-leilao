# Implementation Plan: Radar Imobiliário — Especificação Completa

## Overview

Este plano converte o `design.md` desta spec em passos incrementais de código Python 3.12,
PostgreSQL 16 com pgvector, FastAPI, LangGraph e React. Cada sub-tarefa referencia os critérios de
aceitação do `requirements.md` que a originam. Os dois documentos são as **únicas** fontes de
trabalho: nenhuma tarefa deste plano depende de ler qualquer outro arquivo, e **os dezesseis
artefatos de `architecture/backend/` são derivados e não normativos** (`D86`) — nenhuma tarefa os
toma como fonte.

**Contagens que governam este plano, e que são contrato:**

| Grandeza | Valor |
|----------|-------|
| Requisitos | **126**, `R1` a `R126` |
| Prioridade | **112 `P0`**, **13 `P1`**, **1 `P2`** (`D102`) |
| Requisitos `P1` | `R5`, `R31`, `R42`, `R43`, `R48`, `R59`, `R60`, `R65`, `R69`, `R80`, `R81`, `R117`, `R121` |
| Requisito `P2` | `R72` |
| Propriedades de correção | **262**, em **22 famílias** `P1` a `P22`, numeradas de 1 a 262 |
| Meta-testes | **16**, `MT-01` a `MT-16` |
| Testes de regressão | **60**, `REG-001` a `REG-060`, um por linha do Anexo E |
| Golden Cases | **4**, dos Anexos E e F |
| Componentes | **49** |
| Entidades de negócio | **63** · entidades de infraestrutura e de plataforma: **15** |
| Enums de negócio | **60** · enums de infraestrutura: **7** |
| Itens de integridade | **24** |
| Passos da ordem de construção | **20** (`D91`, que substitui `D88`) |
| Camadas de decisão | **11** · verificações do gate jurídico: **19** · componentes de custo: **13** |
| Regras canônicas | **55** · itens de checklist: **234** · pesos de aderência: **7** |
| Fases persistidas | **16** · etapas do pipeline de `R70.1`: **20** |

Nenhum número de negócio muda: R$ 182.158,03, R$ 236.125,246785, 18,5775%, 16,5139%, 84,2940% e
R$ 251.197,07105 permanecem exatamente como estão.

**Ordem de construção e prioridade de requisito são dimensões distintas.** Um requisito `P0`
construído no passo 18 continua `P0`: a observabilidade (`R111`), o endurecimento de segurança
(`R112`) e os checklists parametrizáveis por escopo (`R92`) são `P0` e são construídos tarde porque
dependem do motor único e do catálogo estabilizado, não porque sejam menos exigidos. Prioridade
responde "o MVP existe sem isto?"; ordem de construção responde "o que precisa estar pronto
antes?". Nenhuma das duas se deduz da outra.

**O preparo estrutural é exceção deliberada a essa distinção, e vem no começo.** Identificador de
correlação, identificador de titular, versão do motor, data de corte, catálogo de erros, contratos
de provedor e separação entre núcleo, adaptadores e infraestrutura entram nos passos 1 a 3,
**antes** de as 63 entidades de negócio estarem gravadas. O motivo é aritmético, não estético:
retroajustá-los depois é **migração**, não ajuste (`D96`, `R118.9`).

**As duas invariantes preservadas.** O **primeiro marco funcional** é a análise manual real de um
imóvel da CAIXA, do documento até a decisão apresentada na interface, incluindo complementação de
evidência e reanálise — e ele fecha ao fim do **passo 8**, não do passo 5, porque exige interface de
programação e interface do investidor. E **a construção não começa pelo coletor**: framework de
conector, conector CAIXA e Radar são deliberadamente posteriores (passos 13 a 15).

**Convenção de idioma (`D72` e `D103`).** Todo identificador de implementação é escrito em
português, exatamente como o `design.md` o nomeia, e a tabela de correspondências obrigatórias de
`D103` é normativa — sinônimo novo para termo já nomeado é defeito de redação, não variação de
estilo. A renomeação **é trabalho de implementação**: alcança `src/radar/**`, `db/schema.sql`,
`scripts/**` e `tests/**`. Ela entra como renomeação de **módulos no passo 2**, **esquema por
migração versionada no passo 3**, nomes de recurso, campo e valor de domínio no **contrato de
programação no passo 7**, e **interface integralmente em português no passo 8**; `MT-11` está na
barreira de integração, junto com `ruff` e `mypy --strict`, **desde o passo 1**. As exceções em
inglês são apenas nomes de tecnologia externa — LangChain, LangGraph, MCP, RAG, OCR, React,
FastAPI, PostgreSQL, pgvector, S3, OpenAI, Bedrock e cron — e os códigos estáveis, que **não** são
renomeados (`RULE-*`, `MC-*`, `B-*`, `C-*`, `REG-*`, `MT-*`, `CUS-*`, `GLB-*`, `INV-*`, `LOC-*`,
`TIP-*`, `PRI-*`, `VAL-*`, `CMP-*`, `REN-*`, `LIQ-*`, `RISK-*`, `CONF-*`, `FRESH`, `SCORE-*`,
`STR`, `PORT-*`, `EXC-*`, `ALT-*`, `MON-*`, `IA-*`, `AQ-*`, `PLT-*`, `HS-*`, `PL-*`, `RL-*`,
`HL-*`, `E01` a `E09`, gates `G0` a `G7` e `G1-P`, níveis `I0` a `I4`, `SAFE-*`, `P-A` a `P-E`,
`D*`, `R*`, `P*`). A coluna `tenant_id` permanece com esse nome porque é o identificador declarado
literalmente em `R118.1`; o termo de negócio correspondente é **titular**.

**Base existente.** O produto já tem fatia vertical em `src/radar/**` com **22 testes passando**, o
esquema em `db/schema.sql`, utilitários em `scripts/**`, testes em `tests/**` e configuração em
`pyproject.toml` (comprimento de linha 100, alvo `py312`, modo estrito). Os módulos atuais estão em
inglês e são renomeados nas primeiras tarefas, mantendo os 22 testes verdes.

**Convenção de teste de propriedade.** Cada uma das **262** propriedades tem **exatamente um**
teste, em arquivo próprio `testes/propriedades/test_propriedade_NNN.py`, com a etiqueta
`Feature: radar-imobiliario-especificacao-completa, Property {n}: {texto}` e no mínimo **100
iterações**. Arquivo por propriedade é o que torna essas tarefas independentes e paralelizáveis.
`P7.12` **não** é propriedade: é contraexemplo dirigido de entradas fixas (`REG-033`).

## Tasks

- [x] 1. Passo 1 de `D91` · bloco `1.1` — Fundação de tipos e infraestrutura de teste

  - [x] 1.1 Implementar o valor com estado de informação
    - Criar `src/radar/nucleo/informado.py` com `Informado[T]` congelado — valor, estado da informação, fonte, data de observação, confiança e qualidade da evidência — e o sentinela explícito `Desconhecido`
    - Nenhum campo de domínio recebe default permissivo: ausência é `Desconhecido`, nunca zero, string vazia ou valor neutro
    - Declarar a métrica provisória que carrega o motivo da provisoriedade, usada quando componente de custo é `DESCONHECIDO` de impacto alto ou crítico
    - _Requisitos: 3.2, 10.2, 26.7, 26.10, 26.12_

  - [x] 1.2 Declarar os 60 enums de negócio e os 7 enums de infraestrutura
    - Criar `src/radar/nucleo/enumeracoes.py` com os **60 enums de negócio** e as contagens que são contrato: `FaseDoPipeline` 16, `EstadoDeDecisao` 6, `CamadaDeDecisao` 11, `Estrategia` 6, `PerfilDeAtivo` 9, `EstadoDeOcupacao` 7, `CategoriaDeLiquidez` 7, `NivelDeConfianca` 6, `EstadoDaInformacao` 6, `QualidadeDaEvidencia` 5, `OrigemDeEvidencia` 5, `TipoDeSegmentoDeConhecimento` 15, `ClasseDeUrgencia` 6, `ClasseDeAtratividade` 5, `SituacaoJuridica` 3, `ResultadoP0` 5, `ResultadoDeVerificacao` 5, `NivelDeIdentidade` 5, `ForcaDeSinal` 6, `VeredictoDeIdentidade` 3, `ClasseDeLocalizacao` 5, `ClasseDeComparavel` 6, `TipoDeArea` 5, `MetodoDeValuation` 7, `CategoriaDeRisco` 10, `Probabilidade` 3, `Impacto` 4, `Severidade` 4, `Mitigacao` 6, `FaseDeDiligencia` 8, `ResultadoDeItemDeChecklist` 6, `PrioridadeDePendencia` 4, `TipoDeCenario` 4, `Robustez` 6, `NivelDeReforma` 5, `EstadoDeMonitoramento` 10, `Materialidade` 5, `TipoDeRegra` 6, `GrupoDePerfil` 9, `GateDeDados` 8, `PotencialPreliminar` 5, `PublicoAlvo` 7, `EstadoDaCaptura` 10, `EstadoDoImovel` 8, `ClasseDeConfiabilidadeDeFonte` 6, `SituacaoDeGovernanca` 6, `FormatoNumerico` 3, `UnidadeDePercentual` 2, `EstadoDeAverbacaoDeLeilaoNegativo` 4, `ResultadoDeEviccao` 3, `ImpactoDeProcesso` 4, `TipoDeDocumento` 9, `OrigemDeDocumento` 3, `TipoDeDebito` 4, `SituacaoDeDebito` 5, `ResponsabilidadePeloDebito` 3, `SituacaoDeProcesso` 5, `PortaDeEntrada` 2, `ResultadoDeTriagem` 2 e `CategoriaDeDiferenca` 5
    - Criar `src/radar/nucleo/enumeracoes_de_infraestrutura.py` com os **7 enums de infraestrutura**: `SituacaoDeExecucaoDoRadar` 6, `EstadoDaOfertaNaFonte` 6, `EstrategiaDeCaptura` 4, `CategoriaDeErro` 15, `SituacaoDeTrabalhoAssincrono` 6, `EstadoDeTela` 9 e `NaturezaDaInformacao` 4
    - Aplicar a tabela de correspondência de rótulos normativos de `D72` e as correspondências obrigatórias de `D103`, um para um; sinônimo novo para termo já nomeado é defeito
    - _Requisitos: 53.1, 53.5, 56.5, 62.4, 86.4, 91.2, 91.4, 93.3, 101.5, 106.4, 108.2, 114.2, 115.4, 122.1_

  - [x] 1.3 Implementar a classificação por faixa única
    - Criar `src/radar/motores/faixas.py` com `classificar_por_faixa`, por limite inferior, comparação `>=` e avaliação em ordem decrescente, total sobre `[0, 100]` e sem lacuna para valores não inteiros
    - Toda faixa do produto — escore, confiança, liquidez, materialidade — passa a usar esta função única, corrigindo `D.1.5`
    - _Requisitos: 40.2, 49.6, 50.3, 50.4_

  - [x] 1.4 Configurar a infraestrutura de teste de propriedade
    - Fixar `hypothesis` com pino exato em `pyproject.toml`, ao lado de `pytest`, `pytest-cov`, `ruff` e `mypy` já configurados (linha 100, alvo `py312`, modo estrito)
    - Declarar os perfis `dev` (100), `ci` (500), `noturno` (5.000) e `regressao` (banco de exemplos persistido), com `deadline` desativado apenas onde houver justificativa no próprio teste
    - Criar `testes/propriedades/` com **um arquivo por propriedade**, `test_propriedade_NNN.py`, e a etiqueta obrigatória `Feature: radar-imobiliario-especificacao-completa, Property {n}: {texto}` em cada teste
    - _Requisitos: 73.1, 73.2, 73.7_

  - [x] 1.5 Criar os geradores compartilhados
    - Criar `testes/geradores/`, um módulo por domínio, todos nomeados em português: escalas e escalares (`dinheiro`, `area`, `percentual`, `data_hora_br`, `informado`); captura e identidade; jurídico e evidência; mercado e economia; risco, liquidez e escore; decisão e lance; governança; Domínio O; mercado e valuation; infraestrutura de IA; aquisição resiliente; plataforma; experiência
    - Injetar em cada gerador de escala os valores de fronteira obrigatórios: 89,5 · 79,5 · 74,5 · 69,5 · 59,5 · 49,5 · 39,5, `"47.76"`, `"191651.31"`, `"2,5%"`, `"2.5%"`, 1 com unidade `PORCENTO`, o valor exato de cada limiar de `MON-001` a `MON-017` e de `STR`, versão 1 de documento e de análise, par de versões idênticas e documento com hash divergente
    - Provedor de modelo e provedor de embedding entram nas propriedades **apenas** por dublê: `dubla_de_provedor_de_modelo()` e `dubla_de_provedor_de_embedding()`; `nome_de_arquivo_hostil()` injeta travessia relativa, caminho absoluto, separadores mistos, unicode e nome vazio
    - _Requisitos: 73.1, 73.2_

  - [x] 1.6 Criar o esqueleto dos dezesseis meta-testes
    - Criar `testes/meta/test_mt_01.py` a `test_mt_10.py` e `test_mt_12.py` a `test_mt_16.py`, executáveis e falhando por conteúdo ausente, nunca por erro de importação
    - Cada esqueleto declara o que verifica e a condição de falha: rastreabilidade das 262 propriedades, um teste por propriedade, cobertura de checklist em qualquer versão, 55 regras, disciplina de lance, prioridade dos 126 requisitos com 112/13/1, ponto único de verdade de `STR`, soma de pesos, contagem de enums, isolamento do núcleo, quarenta perguntas de fechamento, titular em toda entidade, catálogo de erros, identificador de correlação e nove estados por tela
    - _Requisitos: 73.1, 73.3, 73.10_

  - [x] 1.7 Implementar `MT-11` — convenção de idioma na barreira de integração
    - Criar `testes/meta/test_mt_11.py` percorrendo a árvore sintática dos módulos Python de `src/radar/**` e de `scripts/**` e o esquema de `db/schema.sql`: módulos, pacotes, classes, funções, parâmetros, tabelas, colunas, índices, enums e valores de enum têm de estar em português
    - Falhar **apontando o identificador, o arquivo e a linha**; o dicionário de exceções é dado versionado e acrescentar entrada a ele é mudança revisável, não escape silencioso
    - Colocar `MT-11` na mesma barreira de integração que `ruff` e `mypy --strict`, **desde o passo 1**, e cobrir também as correspondências obrigatórias de `D103`
    - _Requisitos: 94.2, 97.3_

  - [x] 1.8 Declarar as três marcas de dependência externa, desabilitadas por default
    - Registrar em `testes/conftest.py` as marcas `@pytest.mark.db`, `@pytest.mark.fonte_externa` e `@pytest.mark.provedor_de_modelo`, com `--strict-markers` e `addopts` que as desabilita por default, habilitadas explicitamente na integração contínua
    - A consequência é verificável: as 262 propriedades rodam sem banco, sem rede e sem crédito de provedor
    - _Requisitos: 73.2, 73.7_

  - [x]* 1.9 Escrever testes unitários da fundação de tipos
    - Criar `testes/unidade/test_fundacao_de_tipos.py` cobrindo `Informado[T]` e `Desconhecido` na fronteira, a totalidade de `classificar_por_faixa` nos limites inteiros e fracionários, e as contagens declaradas de cada enum
    - _Requisitos: 3.2, 26.7, 49.6_

- [ ] 2. Passo 1 de `D91` · bloco `1.1-A` — Preparo estrutural

  - [x] 2.1 Implementar o identificador de correlação
    - Criar `src/radar/nucleo/correlacao.py` com `IdentificadorDeCorrelacao` gerado na borda de entrada e propagado por todo o caminho de execução, como valor imutável do núcleo
    - Exceção deliberada de ordem: entra no passo 1 porque é **coluna em toda entidade**, e acrescentá-lo depois das 61 tabelas gravadas é migração (`D96`)
    - _Requisitos: 111.1, 111.3_

  - [x] 2.2 Implementar a versão do motor e a data de corte
    - Criar `src/radar/nucleo/versao_do_motor.py` com `VersaoDoMotor` e `DataDeCorte` como valores registrados em toda execução relevante
    - Nenhuma evidência com data de observação posterior à `DataDeCorte` é admitida na versão de análise que a declara
    - _Requisitos: 120.1, 120.2, 120.4_

  - [x] 2.3 Declarar o catálogo de erros com as quinze categorias
    - Criar `src/radar/nucleo/erros.py` (componente 44, catálogo) com `ErroDoRadar` como raiz, carregando código estável, mensagem amigável em português e contexto estruturado sem segredo e sem payload íntegro de terceiro
    - Declarar as três famílias: entrada e contrato; evidência e governança; capacidade e infraestrutura — com as **15 categorias** de `CategoriaDeErro` mapeadas uma a uma
    - Declarar `RejeicaoDeCaptura` como **resultado registrado, não exceção**: payload reprovado em `G0` vira captura com estado `REJEITADA` e causa nomeada, sem criar oportunidade
    - _Requisitos: 114.1, 114.2, 114.5, 114.7, 114.9_

  - [x] 2.4 Declarar os contratos de provedor no núcleo
    - Criar `src/radar/nucleo/contratos/provedor_de_modelo_de_linguagem.py` e `src/radar/nucleo/contratos/provedor_de_embedding.py` como `Protocol` — componente 28, lado do núcleo
    - Declarar no mesmo diretório os contratos `IndiceVetorial`, `ArmazenamentoDeArquivo`, `Agendador`, `CanalDeNotificacao`, `ConectorDeFonte` e `EstrategiaDeCaptura`
    - _Requisitos: 98.1, 98.2, 98.5_

  - [x] 2.5 Declarar as três camadas e o grafo de importação proibida
    - Criar a estrutura `src/radar/nucleo/**`, `src/radar/adaptadores/**` e `src/radar/plataforma/**`, com `radar/motores/**`, `radar/pipeline/**`, `radar/regras/**` e `radar/radar/**` pertencendo ao núcleo
    - Declarar em `src/radar/nucleo/camadas.py` o grafo de importação proibida: o fechamento transitivo do núcleo não contém cliente de modelo de linguagem, biblioteca de orquestração de IA, cliente de embedding, cliente de armazenamento externo nem cliente de agendamento
    - _Requisitos: 119.1, 119.2, 119.3_

  - [ ] 2.6 Implementar `MT-10` — isolamento do núcleo
    - Criar `testes/meta/test_mt_10.py` percorrendo a árvore de imports a partir de cada módulo do núcleo e falhando com o **caminho completo** do import proibido
    - _Requisitos: 71.1, 71.2, 98.5, 119.3_

  - [ ] 2.7 Implementar o Gestor de Configuração que falha fechada
    - Criar `src/radar/plataforma/configuracao.py` (componente 43): configuração por ambiente, sem segredo em código, com **falha de inicialização** quando configuração obrigatória está ausente
    - Declarar os sinalizadores de recurso, que não alteram precedência, princípio inviolável nem parada absoluta, e cuja desabilitação preserva o determinismo registrando a capacidade como não executada
    - _Requisitos: 113.1, 113.2, 113.5, 113.6, 113.7, 113.8_

  - [ ] 2.8 Implementar a tradução do catálogo de erros na fronteira
    - Criar `src/radar/plataforma/erros.py` com a tradução do catálogo: código, mensagem amigável em português e mapeamento por categoria, sem rastro de execução, consulta ao banco, caminho interno ou mensagem de biblioteca
    - _Requisitos: 114.3, 114.6, 114.8, 114.9_

  - [ ] 2.9 Implementar `MT-14` — catálogo de erros completo e sem detalhe técnico
    - Criar `testes/meta/test_mt_14.py`: cada uma das **15** categorias de `R114.2` tem código, mensagem amigável em português e mapeamento declarados, e nenhuma mensagem apresentada ao usuário contém detalhe técnico
    - Falha **nomeando** a categoria sem código, sem mensagem ou sem mapeamento, e a mensagem com rastro de execução
    - _Requisitos: 114.2, 114.9_

  - [ ] 2.10 Registrar os adaptadores aplicados por execução
    - Criar `src/radar/nucleo/adaptadores_aplicados.py`: cada execução registra a combinação de adaptadores usada, e a primeira execução completa é local — armazenamento local, banco local, agendamento local
    - Troca de adaptador declarado não altera o resultado determinístico para as mesmas evidências, parâmetros e versões
    - _Requisitos: 119.4, 119.5, 119.6, 119.7_

  - [ ]* 2.11 Escrever teste de propriedade para isolamento do núcleo
    - **Property 188: Isolamento do núcleo (`P19.2`)**
    - **Validates: Requirements 98.5, 119.3**
    - Arquivo `testes/propriedades/test_propriedade_188.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 188: Isolamento do núcleo`, mínimo de 100 iterações

  - [ ]* 2.12 Escrever teste de propriedade para configuração ausente impede inicialização
    - **Property 234: Configuração ausente impede inicialização (`P21.8`)**
    - **Validates: Requirements 113.5**
    - Arquivo `testes/propriedades/test_propriedade_234.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 234: Configuração ausente impede inicialização`, mínimo de 100 iterações

  - [ ]* 2.13 Escrever teste de propriedade para totalidade do catálogo de erros
    - **Property 236: Totalidade do catálogo de erros (`P21.10`)**
    - **Validates: Requirements 114.2, 114.3, 114.7**
    - Arquivo `testes/propriedades/test_propriedade_236.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 236: Totalidade do catálogo de erros`, mínimo de 100 iterações

  - [ ]* 2.14 Escrever teste de propriedade para invariância de adaptador
    - **Property 245: Invariância de adaptador (`P21.19`)**
    - **Validates: Requirements 119.4, 119.6**
    - Arquivo `testes/propriedades/test_propriedade_245.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 245: Invariância de adaptador`, mínimo de 100 iterações

  - [ ]* 2.15 Escrever teste de propriedade para versão do motor sempre registrada
    - **Property 246: Versão do motor sempre registrada (`P21.20`)**
    - **Validates: Requirements 120.1**
    - Arquivo `testes/propriedades/test_propriedade_246.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 246: Versão do motor sempre registrada`, mínimo de 100 iterações

  - [ ]* 2.16 Escrever testes unitários do preparo estrutural
    - Criar `testes/unidade/test_preparo_estrutural.py` cobrindo a falha fechada da configuração ausente, a totalidade do mapeamento de `CategoriaDeErro` e a propagação do identificador de correlação
    - _Requisitos: 113.5, 114.2, 111.1_

- [ ] 3. Checkpoint — fecha o passo 1 de `D91`
  - Executar a suíte inteira, `ruff`, `mypy --strict` e `MT-11`
  - Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 4. Passo 2 de `D91` · bloco `1.2` — Correções numéricas verificadas e renomeação dos módulos

  - [ ] 4.1 Renomear os módulos de domínio e motores para português (`D72`)
    - Renomear em `src/radar/**`: `capture` → `captura` (`parsing` → `interpretacao`, `schemas` → `esquemas`), `domain` → `dominio` e `nucleo`, `engines` → `motores` (`calculation` → `calculo`, `decision` → `decisao`), `pipeline/identity` → `pipeline/identidade`, `pipeline/legal_gate` → `pipeline/gate_juridico`, `orchestration/graph` → `orquestracao/grafo`, `services/analysis_service` → `servicos/servico_de_analise`, `db/{models,repository,session}` → `db/{modelos,repositorio,sessao}`, `config` → `configuracao`, e `tests/` → `testes/`
    - Renomear classes, funções, parâmetros e variáveis internas conforme a tabela de correspondência de `D72` e `D103`; manter os **22 testes existentes verdes**, ajustando apenas nomes e imports
    - A renomeação do esquema **não** entra aqui: ela é migração versionada do passo 3
    - _Requisitos: 94.2, 97.3_

  - [ ] 4.2 Corrigir a interpretação numérica
    - Reescrever `src/radar/captura/interpretacao.py`: `interpretar_decimal` sem nenhuma heurística de magnitude — `"47.76"` é 47,76 e nunca 4.776 —, e `interpretar_percentual` com `UnidadeDePercentual` obrigatória na entrada
    - Entrada não interpretável ou ambígua resulta em `DESCONHECIDO`, nunca em valor adivinhado; corrige `D.1.3` e `D.1.4`
    - _Requisitos: 3.2, 3.4, 3.4.1, 3.4.2, 3.4.3, 3.4.4_

  - [ ] 4.3 Fixar `Decimal` em todo o caminho monetário
    - Criar `src/radar/nucleo/escalas.py` com os tipos de dinheiro, área e percentual sobre `Decimal`, e a regra de arredondamento declarada como parâmetro versionado, nunca implícita na conversão de tipo
    - Nenhum `float` atravessa a fronteira: isso passa a ser erro de tipo sob `mypy --strict`, não convenção
    - _Requisitos: 26.1, 27.17_

  - [ ] 4.4 Implementar as métricas de tempo e o `roi_anualizado`
    - Criar `src/radar/motores/tempo.py` com `roi_anualizado`, custo do tempo e eficiência de capital, sem tocar o custo econômico total
    - O custo de oportunidade do capital de `CUS-016` entra apenas aqui, e **não** no custo econômico total
    - _Requisitos: 26.1.2, 30.2, 30.3, 30.3.1, 30.3.2_

  - [ ]* 4.5 Escrever teste de propriedade para round-trip monetário
    - **Property 7: Round-trip monetário (`P2.2`)**
    - **Validates: Requirements 3.4**
    - Arquivo `testes/propriedades/test_propriedade_007.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 7: Round-trip monetário`, mínimo de 100 iterações

  - [ ]* 4.6 Escrever teste de propriedade para round-trip de área
    - **Property 8: Round-trip de área (`P2.3`)**
    - **Validates: Requirements 3.4**
    - Arquivo `testes/propriedades/test_propriedade_008.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 8: Round-trip de área`, mínimo de 100 iterações

  - [ ]* 4.7 Escrever teste de propriedade para round-trip de percentual
    - **Property 9: Round-trip de percentual (`P2.4`)**
    - **Validates: Requirements 3.4**
    - Arquivo `testes/propriedades/test_propriedade_009.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 9: Round-trip de percentual`, mínimo de 100 iterações

  - [ ]* 4.8 Escrever teste de propriedade para round-trip de data e data com hora
    - **Property 10: Round-trip de data e data com hora (`P2.5`)**
    - **Validates: Requirements 3.4**
    - Arquivo `testes/propriedades/test_propriedade_010.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 10: Round-trip de data e data com hora`, mínimo de 100 iterações

  - [ ]* 4.9 Escrever teste de propriedade para invariância de magnitude na interpretação numérica
    - **Property 15: Invariância de magnitude na interpretação numérica (`P2.10`)**
    - **Validates: Requirements 3.4.1**
    - Arquivo `testes/propriedades/test_propriedade_015.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 15: Invariância de magnitude na interpretação numérica`, mínimo de 100 iterações

  - [ ]* 4.10 Escrever teste de propriedade para percentual normalizado com unidade respeitada
    - **Property 16: Percentual normalizado com unidade respeitada (`P2.11`)**
    - **Validates: Requirements 3.4.2, 3.4.3**
    - Arquivo `testes/propriedades/test_propriedade_016.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 16: Percentual normalizado com unidade respeitada`, mínimo de 100 iterações

  - [ ]* 4.11 Escrever teste de propriedade para entrada não interpretável resulta em DESCONHECIDO
    - **Property 17: Entrada não interpretável resulta em DESCONHECIDO (`P2.12`)**
    - **Validates: Requirements 3.2, 3.4.4**
    - Arquivo `testes/propriedades/test_propriedade_017.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 17: Entrada não interpretável resulta em DESCONHECIDO`, mínimo de 100 iterações

  - [ ]* 4.12 Escrever testes dirigidos de interpretação numérica
    - Criar `testes/dirigidos/test_interpretacao_numerica.py` com `"47.76"`, `"191651.31"`, `"2,5%"`, `"2.5%"` e 1 com unidade `PORCENTO`, cobrindo `REG-019` e `REG-020`
    - _Requisitos: 3.4.1, 3.4.2, 3.4.3_

- [ ] 5. Passo 2 de `D91` · bloco `1.3` — Captura, identidade, perfil e localização

  - [ ] 5.1 Implementar o Capturador
    - Criar `src/radar/captura/servico_de_captura.py` (componente 1) com impressão digital canônica invariante à ordem das chaves, determinística e distinguindo conteúdos distintos
    - Registro idempotente por `(fonte, hash)` e append-only: corrigir cria registro novo, nunca altera o anterior
    - _Requisitos: 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 2.5, 85.6_

  - [ ] 5.2 Implementar o Normalizador com despacho por tipo de fonte
    - Criar `src/radar/captura/normalizadores/base.py` e `src/radar/captura/normalizadores/caixa.py` (componente 2): despacho por tipo de fonte com falha explícita quando não há normalizador, corrigindo `D.6.11`
    - Campo ausente resulta em `DESCONHECIDO`; lista de ausências exata; tipo de área nunca inferido; avaliação da fonte em campo próprio, sem nenhum caminho para `valor_de_mercado`; precedência de vacância sobre ocupação
    - Preservar o **valor original de cada campo** ao lado do valor normalizado
    - _Requisitos: 3.1, 3.2, 3.3, 3.5, 3.8, 3.9, 3.10, 3.11, 74.9, 74.10_

  - [ ] 5.3 Implementar o Gate de dados e o Qualificador
    - Criar `src/radar/pipeline/qualificacao.py` (componente 3) com os gates `G0` a `G7` declarativos e o gate `G1` de qualificação
    - Payload reprovado em `G0` não cria oportunidade: produz captura rejeitada com a verificação não satisfeita nomeada
    - _Requisitos: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8_

  - [ ] 5.4 Implementar o Resolvedor de Identidade
    - Criar `src/radar/pipeline/identidade.py` (componente 4, parte): níveis `I0` a `I4`, chave conceitual, força de sinal monotônica e identidade invariante ao preço
    - A resolução é **total**: nenhuma entrada fica sem nível atribuído
    - _Requisitos: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.9, 8.1, 8.2, 8.3, 8.4_

  - [ ] 5.5 Implementar o Deduplicador
    - Criar `src/radar/pipeline/deduplicacao.py` (componente 4, parte): veredicto de três valores, matrícula decisiva, simetria e reflexividade, vínculo idempotente, desvínculo que preserva histórico
    - Veredicto `MESMO` vincula a captura ao imóvel existente e **não** cria imóvel novo; unidades distintas nunca são fundidas; evidência insuficiente resulta em veredicto indeterminado
    - _Requisitos: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.9, 9.11, 84.11, 84.12, 84.13_

  - [ ] 5.6 Implementar o Consolidador de Perfil
    - Criar `src/radar/pipeline/perfil.py` (componente 5, parte): perfil vigente nos **nove** grupos, com estado de informação e fonte por campo, e versões de perfil numeradas sem sobrescrita
    - _Requisitos: 10.1, 10.2, 10.4, 10.5, 10.6, 10.8, 74.4_

  - [ ] 5.7 Implementar o histórico de observações de preço
    - Criar `src/radar/pipeline/precos.py`: valor, moeda, data de observação, fonte, tipo de preço e variação em relação à observação anterior, alimentando `ALT-002` e `MON-001`
    - Venda direta subsiste aqui apenas como **tipo de preço observado**
    - _Requisitos: 10.7, 74.5_

  - [ ] 5.8 Implementar o registro de divergências entre fontes
    - Criar `src/radar/pipeline/divergencias.py`: fonte A, informação A, fonte B, informação B, dimensão afetada, materialidade, impacto na decisão e situação, permanecendo aberta até confirmação oficial
    - _Requisitos: 6.1, 6.2, 6.3, 6.4, 6.5, 74.6_

  - [ ] 5.9 Implementar o Classificador de Localização
    - Criar `src/radar/pipeline/localizacao.py` (componente 5, parte): classes A–E, perfil de demanda, liquidez regional e faixa de preço predominante como entidade própria, com histórico
    - _Requisitos: 11.1, 11.2, 11.3, 74.1_

  - [ ]* 5.10 Escrever teste de propriedade para impressão digital invariante à ordem das chaves
    - **Property 1: Impressão digital invariante à ordem das chaves (`P1.1`)**
    - **Validates: Requirements 2.2**
    - Arquivo `testes/propriedades/test_propriedade_001.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 1: Impressão digital invariante à ordem das chaves`, mínimo de 100 iterações

  - [ ]* 5.11 Escrever teste de propriedade para impressão digital determinística
    - **Property 2: Impressão digital determinística (`P1.2`)**
    - **Validates: Requirements 2.2**
    - Arquivo `testes/propriedades/test_propriedade_002.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 2: Impressão digital determinística`, mínimo de 100 iterações

  - [ ]* 5.12 Escrever teste de propriedade para impressão digital distingue conteúdos distintos
    - **Property 3: Impressão digital distingue conteúdos distintos (`P1.3`)**
    - **Validates: Requirements 2.2**
    - Arquivo `testes/propriedades/test_propriedade_003.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 3: Impressão digital distingue conteúdos distintos`, mínimo de 100 iterações

  - [ ]* 5.13 Escrever teste de propriedade para idempotência do registro de captura
    - **Property 4: Idempotência do registro de captura (`P1.4`)**
    - **Validates: Requirements 2.3**
    - Arquivo `testes/propriedades/test_propriedade_004.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 4: Idempotência do registro de captura`, mínimo de 100 iterações

  - [ ]* 5.14 Escrever teste de propriedade para captura é append-only
    - **Property 5: Captura é append-only (`P1.5`)**
    - **Validates: Requirements 2.4, 2.5**
    - Arquivo `testes/propriedades/test_propriedade_005.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 5: Captura é append-only`, mínimo de 100 iterações

  - [ ]* 5.15 Escrever teste de propriedade para campo ausente resulta em DESCONHECIDO
    - **Property 6: Campo ausente resulta em DESCONHECIDO (`P2.1`)**
    - **Validates: Requirements 3.2**
    - Arquivo `testes/propriedades/test_propriedade_006.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 6: Campo ausente resulta em DESCONHECIDO`, mínimo de 100 iterações

  - [ ]* 5.16 Escrever teste de propriedade para idempotência da normalização
    - **Property 11: Idempotência da normalização (`P2.6`)**
    - **Validates: Requirements 3.1, 3.11**
    - Arquivo `testes/propriedades/test_propriedade_011.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 11: Idempotência da normalização`, mínimo de 100 iterações

  - [ ]* 5.17 Escrever teste de propriedade para lista de ausências é exata
    - **Property 12: Lista de ausências é exata (`P2.7`)**
    - **Validates: Requirements 3.9**
    - Arquivo `testes/propriedades/test_propriedade_012.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 12: Lista de ausências é exata`, mínimo de 100 iterações

  - [ ]* 5.18 Escrever teste de propriedade para avaliação da fonte nunca vira valor de mercado
    - **Property 13: Avaliação da fonte nunca vira valor de mercado (`P2.8`)**
    - **Validates: Requirements 3.10**
    - Arquivo `testes/propriedades/test_propriedade_013.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 13: Avaliação da fonte nunca vira valor de mercado`, mínimo de 100 iterações

  - [ ]* 5.19 Escrever teste de propriedade para tipo de área nunca é inferido
    - **Property 14: Tipo de área nunca é inferido (`P2.9`)**
    - **Validates: Requirements 3.5**
    - Arquivo `testes/propriedades/test_propriedade_014.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 14: Tipo de área nunca é inferido`, mínimo de 100 iterações

  - [ ]* 5.20 Escrever teste de propriedade para precedência de vacância sobre ocupação
    - **Property 18: Precedência de vacância sobre ocupação (`P2.13`)**
    - **Validates: Requirements 3.8**
    - Arquivo `testes/propriedades/test_propriedade_018.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 18: Precedência de vacância sobre ocupação`, mínimo de 100 iterações

  - [ ]* 5.21 Escrever teste de propriedade para resolução de identidade é total
    - **Property 19: Resolução de identidade é total (`P3.1`)**
    - **Validates: Requirements 7.1**
    - Arquivo `testes/propriedades/test_propriedade_019.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 19: Resolução de identidade é total`, mínimo de 100 iterações

  - [ ]* 5.22 Escrever teste de propriedade para monotonicidade na força dos sinais
    - **Property 20: Monotonicidade na força dos sinais (`P3.2`)**
    - **Validates: Requirements 7.2, 7.3, 7.4, 7.5, 7.6**
    - Arquivo `testes/propriedades/test_propriedade_020.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 20: Monotonicidade na força dos sinais`, mínimo de 100 iterações

  - [ ]* 5.23 Escrever teste de propriedade para identidade é invariante ao preço
    - **Property 21: Identidade é invariante ao preço (`P3.3`)**
    - **Validates: Requirements 7.7**
    - Arquivo `testes/propriedades/test_propriedade_021.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 21: Identidade é invariante ao preço`, mínimo de 100 iterações

  - [ ]* 5.24 Escrever teste de propriedade para deduplicação é invariante ao preço
    - **Property 22: Deduplicação é invariante ao preço (`P3.4`)**
    - **Validates: Requirements 9.5**
    - Arquivo `testes/propriedades/test_propriedade_022.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 22: Deduplicação é invariante ao preço`, mínimo de 100 iterações

  - [ ]* 5.25 Escrever teste de propriedade para matrícula é decisiva
    - **Property 23: Matrícula é decisiva (`P3.5`)**
    - **Validates: Requirements 9.1**
    - Arquivo `testes/propriedades/test_propriedade_023.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 23: Matrícula é decisiva`, mínimo de 100 iterações

  - [ ]* 5.26 Escrever teste de propriedade para simetria do veredicto
    - **Property 24: Simetria do veredicto (`P3.6`)**
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5, 9.6**
    - Arquivo `testes/propriedades/test_propriedade_024.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 24: Simetria do veredicto`, mínimo de 100 iterações

  - [ ]* 5.27 Escrever teste de propriedade para reflexividade do veredicto
    - **Property 25: Reflexividade do veredicto (`P3.7`)**
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5, 9.6**
    - Arquivo `testes/propriedades/test_propriedade_025.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 25: Reflexividade do veredicto`, mínimo de 100 iterações

  - [ ]* 5.28 Escrever teste de propriedade para idempotência do vínculo
    - **Property 26: Idempotência do vínculo (`P3.8`)**
    - **Validates: Requirements 9.7**
    - Arquivo `testes/propriedades/test_propriedade_026.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 26: Idempotência do vínculo`, mínimo de 100 iterações

  - [ ]* 5.29 Escrever teste de propriedade para unidades distintas nunca são fundidas
    - **Property 27: Unidades distintas nunca são fundidas (`P3.9`)**
    - **Validates: Requirements 9.11**
    - Arquivo `testes/propriedades/test_propriedade_027.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 27: Unidades distintas nunca são fundidas`, mínimo de 100 iterações

  - [ ]* 5.30 Escrever teste de propriedade para evidência insuficiente resulta em veredicto indeterminado
    - **Property 28: Evidência insuficiente resulta em veredicto indeterminado (`P3.10`)**
    - **Validates: Requirements 9.6**
    - Arquivo `testes/propriedades/test_propriedade_028.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 28: Evidência insuficiente resulta em veredicto indeterminado`, mínimo de 100 iterações

  - [ ]* 5.31 Escrever teste de propriedade para desvincular preserva histórico
    - **Property 29: Desvincular preserva histórico (`P3.11`)**
    - **Validates: Requirements 9.9**
    - Arquivo `testes/propriedades/test_propriedade_029.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 29: Desvincular preserva histórico`, mínimo de 100 iterações

  - [ ]* 5.32 Escrever teste de propriedade para nova captura não cria imóvel novo
    - **Property 150: Nova captura não cria imóvel novo (`P17.1`)**
    - **Validates: Requirements 84.12, 9.1**
    - Arquivo `testes/propriedades/test_propriedade_150.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 150: Nova captura não cria imóvel novo`, mínimo de 100 iterações

  - [ ]* 5.33 Escrever testes unitários de captura, identidade e perfil
    - Criar `testes/unidade/test_captura_identidade_perfil.py` cobrindo os ramos de despacho por fonte, os cinco níveis de identidade e as transições de veredicto
    - _Requisitos: 3.1, 7.1, 9.6_

- [ ] 6. Passo 2 de `D91` · bloco `1.4` — Gate jurídico de 19 verificações e Camada de Evidência

  - [ ] 6.1 Implementar o Gate Jurídico com as 19 verificações declarativas
    - Criar `src/radar/pipeline/gate_juridico.py` (componente 6): de 7 para **19** verificações declarativas, determinístico e confluente, com `SituacaoJuridica` fechada validada na fronteira
    - Ausência de evidência **nunca** produz `REGULAR`; irregularidade implica `BLOQUEIO`; corrige `D.5`, `D.2.5` e `D.2.7`
    - _Requisitos: 12.1, 12.2, 12.3, 12.5, 12.6, 12.8_

  - [ ] 6.2 Declarar as regras jurídicas como dados
    - Criar `src/radar/regras/juridicas/catalogo.py` com as regras jurídicas do Anexo D declaradas como dados enumeráveis em tempo de execução, cada uma com fonte e proveniência exigidas
    - Cobrir os códigos estáveis `E01` a `E09` e as verificações complementares do Anexo B
    - _Requisitos: 13.1, 13.4, 13.13, 14.1, 15.9, 15.9.1, 15.9.2, 17.1, 19.1_

  - [ ] 6.3 Implementar `ResultadoDeVerificacao` com `NAO_APLICAVEL` distinto de `DESCONHECIDO`
    - Criar `src/radar/pipeline/verificacoes.py`: uma evidência por verificação avaliada, `NAO_APLICAVEL` com justificativa não nula, e confiança expressando **qualidade da prova**, corrigindo `D.2.8`
    - _Requisitos: 20.4, 36.3, 36.3.1, 36.3.2_

  - [ ] 6.4 Mover ocupação e locação para risco econômico
    - Criar `src/radar/pipeline/ocupacao.py`: os sete estados de ocupação saem do gate jurídico e vão para a camada 6, exceto os dois casos de `BLOQUEAR` da camada 0
    - Ocupação **nunca** altera a situação jurídica
    - _Requisitos: 18.1, 18.2, 18.2.1, 18.2.2, 18.8_

  - [ ] 6.5 Implementar a classificação de impacto do processo judicial
    - Criar `src/radar/pipeline/impacto_processual.py`: quatro níveis de impacto, e somente `material_impeditivo` sem mitigação produz `BLOQUEAR`
    - Processo sem impacto material **nunca** bloqueia
    - _Requisitos: 16.3, 16.6_

  - [ ] 6.6 Implementar a Camada de Evidência append-only
    - Criar `src/radar/evidencia/repositorio.py` (componente 7): proveniência obrigatória, rejeição de evidência sem fonte, monotonicidade do repositório, contradições preservadas e marcadas como conflitantes
    - `transitar_fato` exige identificador de evidência de suporte: `DESCONHECIDO` não vira `CONFIRMADO` sem prova
    - _Requisitos: 20.1, 20.2, 20.3, 20.4, 20.5, 20.6, 20.7_

  - [ ] 6.7 Implementar a fronteira da IA e as propostas de evidência
    - Criar `src/radar/evidencia/propostas.py`: `PropostaDeEvidencia` é tipo e tabela distintos de evidência, e a promoção exige ato humano registrado ou regra determinística declarada
    - _Requisitos: 83.1, 83.2, 83.3_

  - [ ]* 6.8 Escrever teste de propriedade para determinismo do gate jurídico
    - **Property 30: Determinismo do gate jurídico (`P4.1`)**
    - **Validates: Requirements 12.5, 12.6**
    - Arquivo `testes/propriedades/test_propriedade_030.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 30: Determinismo do gate jurídico`, mínimo de 100 iterações

  - [ ]* 6.9 Escrever teste de propriedade para confluência do gate jurídico
    - **Property 31: Confluência do gate jurídico (`P4.2`)**
    - **Validates: Requirements 12.1, 12.5**
    - Arquivo `testes/propriedades/test_propriedade_031.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 31: Confluência do gate jurídico`, mínimo de 100 iterações

  - [ ]* 6.10 Escrever teste de propriedade para irregularidade implica BLOQUEIO
    - **Property 32: Irregularidade implica BLOQUEIO (`P4.3`)**
    - **Validates: Requirements 12.6, 13.4**
    - Arquivo `testes/propriedades/test_propriedade_032.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 32: Irregularidade implica BLOQUEIO`, mínimo de 100 iterações

  - [ ]* 6.11 Escrever teste de propriedade para ausência de evidência nunca produz REGULAR
    - **Property 33: Ausência de evidência nunca produz REGULAR (`P4.4`)**
    - **Validates: Requirements 12.6, 20.7**
    - Arquivo `testes/propriedades/test_propriedade_033.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 33: Ausência de evidência nunca produz REGULAR`, mínimo de 100 iterações

  - [ ]* 6.12 Escrever teste de propriedade para uma evidência por verificação avaliada
    - **Property 34: Uma evidência por verificação avaliada (`P4.5`)**
    - **Validates: Requirements 20.1, 20.7**
    - Arquivo `testes/propriedades/test_propriedade_034.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 34: Uma evidência por verificação avaliada`, mínimo de 100 iterações

  - [ ]* 6.13 Escrever teste de propriedade para cobertura total do Anexo A
    - **Property 35: Cobertura total do Anexo A (`P4.6`)**
    - **Validates: Requirements 36.5**
    - Arquivo `testes/propriedades/test_propriedade_035.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 35: Cobertura total do Anexo A`, mínimo de 100 iterações

  - [ ]* 6.14 Escrever teste de propriedade para ocupação nunca altera a situação jurídica
    - **Property 36: Ocupação nunca altera a situação jurídica (`P4.7`)**
    - **Validates: Requirements 18.2, 18.8**
    - Arquivo `testes/propriedades/test_propriedade_036.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 36: Ocupação nunca altera a situação jurídica`, mínimo de 100 iterações

  - [ ]* 6.15 Escrever teste de propriedade para processo sem impacto material nunca bloqueia
    - **Property 37: Processo sem impacto material nunca bloqueia (`P4.8`)**
    - **Validates: Requirements 16.6**
    - Arquivo `testes/propriedades/test_propriedade_037.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 37: Processo sem impacto material nunca bloqueia`, mínimo de 100 iterações

  - [ ]* 6.16 Escrever teste de propriedade para evidência sem fonte é rejeitada
    - **Property 38: Evidência sem fonte é rejeitada (`P5.1`)**
    - **Validates: Requirements 20.3**
    - Arquivo `testes/propriedades/test_propriedade_038.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 38: Evidência sem fonte é rejeitada`, mínimo de 100 iterações

  - [ ]* 6.17 Escrever teste de propriedade para dESCONHECIDO não vira CONFIRMADO sem suporte
    - **Property 39: DESCONHECIDO não vira CONFIRMADO sem suporte (`P5.2`)**
    - **Validates: Requirements 20.4**
    - Arquivo `testes/propriedades/test_propriedade_039.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 39: DESCONHECIDO não vira CONFIRMADO sem suporte`, mínimo de 100 iterações

  - [ ]* 6.18 Escrever teste de propriedade para monotonicidade do repositório de evidências
    - **Property 40: Monotonicidade do repositório de evidências (`P5.3`)**
    - **Validates: Requirements 20.5, 20.6**
    - Arquivo `testes/propriedades/test_propriedade_040.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 40: Monotonicidade do repositório de evidências`, mínimo de 100 iterações

  - [ ]* 6.19 Escrever teste de propriedade para contradições são preservadas
    - **Property 41: Contradições são preservadas (`P5.4`)**
    - **Validates: Requirements 20.5**
    - Arquivo `testes/propriedades/test_propriedade_041.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 41: Contradições são preservadas`, mínimo de 100 iterações

  - [ ]* 6.20 Escrever teste de propriedade para todo valor tem exatamente um estado de informação
    - **Property 42: Todo valor tem exatamente um estado de informação (`P5.5`)**
    - **Validates: Requirements 10.2**
    - Arquivo `testes/propriedades/test_propriedade_042.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 42: Todo valor tem exatamente um estado de informação`, mínimo de 100 iterações

  - [ ]* 6.21 Escrever testes dirigidos de cobertura do Anexo A no gate jurídico
    - Criar `testes/dirigidos/test_gate_juridico.py` cobrindo os ramos de `EM_TRATAMENTO`, os dois casos de evicção e `NAO_APLICAVEL` distinto de `DESCONHECIDO` (`REG-025`)
    - _Requisitos: 13.13, 15.9, 20.4_

- [ ] 7. Passo 2 de `D91` · bloco `1.5` — Mercado, comparáveis e valuation

  - [ ] 7.1 Implementar o Motor de Comparáveis
    - Criar `src/radar/motores/comparaveis.py` (componente 8, parte): seleção determinística e confluente, classes A–E e U, tipo de área respeitado, descarte de outliers por `CMP-012`
    - Candidato reprovado não influencia o resultado; comparável fora da janela nunca é atual
    - _Requisitos: 21.1, 21.2, 21.3, 21.8, 21.10, 21.11, 21.12_

  - [ ] 7.2 Implementar o Motor de Valuation
    - Criar `src/radar/motores/valuation.py` (componente 8, parte): quantidade mínima de comparáveis, faixas de confiança totais, as quatro referências de valor ordenadas e a contenção do valor provável
    - Ausência de comparável qualificado resulta em `DESCONHECIDO`; a avaliação da fonte permanece independente
    - _Requisitos: 22.1, 22.2, 22.3, 22.4, 22.4.1, 23.1, 23.2, 23.4_

  - [ ] 7.3 Implementar os métodos de valuation por tipo de ativo
    - Criar `src/radar/motores/metodos_de_valuation.py`: os **sete** métodos, com totalidade por tipo de ativo e falha explícita quando o tipo é desconhecido
    - _Requisitos: 24.1, 24.2, 24.3, 24.4, 24.5_

  - [ ] 7.4 Implementar os gatilhos de revaluation
    - Criar `src/radar/motores/revaluation.py`: o limiar dispara no valor **exato**, com comparação `>=`
    - _Requisitos: 25.1, 25.2_

  - [ ]* 7.5 Escrever teste de propriedade para determinismo da seleção de comparáveis
    - **Property 172: Determinismo da seleção de comparáveis (`P18.1`)**
    - **Validates: Requirements 21.1**
    - Arquivo `testes/propriedades/test_propriedade_172.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 172: Determinismo da seleção de comparáveis`, mínimo de 100 iterações

  - [ ]* 7.6 Escrever teste de propriedade para confluência da seleção de comparáveis
    - **Property 173: Confluência da seleção de comparáveis (`P18.2`)**
    - **Validates: Requirements 21.1, 22.1**
    - Arquivo `testes/propriedades/test_propriedade_173.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 173: Confluência da seleção de comparáveis`, mínimo de 100 iterações

  - [ ]* 7.7 Escrever teste de propriedade para monotonicidade do raio e da janela
    - **Property 174: Monotonicidade do raio e da janela (`P18.3`)**
    - **Validates: Requirements 21.2**
    - Arquivo `testes/propriedades/test_propriedade_174.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 174: Monotonicidade do raio e da janela`, mínimo de 100 iterações

  - [ ]* 7.8 Escrever teste de propriedade para monotonicidade da confiança do valuation
    - **Property 175: Monotonicidade da confiança do valuation (`P18.4`)**
    - **Validates: Requirements 22.1, 22.2**
    - Arquivo `testes/propriedades/test_propriedade_175.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 175: Monotonicidade da confiança do valuation`, mínimo de 100 iterações

  - [ ]* 7.9 Escrever teste de propriedade para cobertura total das faixas de confiança do valuation
    - **Property 176: Cobertura total das faixas de confiança do valuation (`P18.5`)**
    - **Validates: Requirements 22.2**
    - Arquivo `testes/propriedades/test_propriedade_176.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 176: Cobertura total das faixas de confiança do valuation`, mínimo de 100 iterações

  - [ ]* 7.10 Escrever teste de propriedade para quantidade insuficiente nunca produz precisão
    - **Property 177: Quantidade insuficiente nunca produz precisão (`P18.6`)**
    - **Validates: Requirements 22.3**
    - Arquivo `testes/propriedades/test_propriedade_177.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 177: Quantidade insuficiente nunca produz precisão`, mínimo de 100 iterações

  - [ ]* 7.11 Escrever teste de propriedade para ordenação das referências de valor
    - **Property 178: Ordenação das referências de valor (`P18.7`)**
    - **Validates: Requirements 23.1**
    - Arquivo `testes/propriedades/test_propriedade_178.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 178: Ordenação das referências de valor`, mínimo de 100 iterações

  - [ ]* 7.12 Escrever teste de propriedade para contenção do valor provável
    - **Property 179: Contenção do valor provável (`P18.8`)**
    - **Validates: Requirements 23.1, 23.2**
    - Arquivo `testes/propriedades/test_propriedade_179.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 179: Contenção do valor provável`, mínimo de 100 iterações

  - [ ]* 7.13 Escrever teste de propriedade para independência da avaliação da fonte
    - **Property 180: Independência da avaliação da fonte (`P18.9`)**
    - **Validates: Requirements 21.8, 3.10**
    - Arquivo `testes/propriedades/test_propriedade_180.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 180: Independência da avaliação da fonte`, mínimo de 100 iterações

  - [ ]* 7.14 Escrever teste de propriedade para totalidade do método de valuation por tipo de ativo
    - **Property 181: Totalidade do método de valuation por tipo de ativo (`P18.10`)**
    - **Validates: Requirements 24.1**
    - Arquivo `testes/propriedades/test_propriedade_181.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 181: Totalidade do método de valuation por tipo de ativo`, mínimo de 100 iterações

  - [ ]* 7.15 Escrever teste de propriedade para idempotência do valuation
    - **Property 182: Idempotência do valuation (`P18.11`)**
    - **Validates: Requirements 22.1**
    - Arquivo `testes/propriedades/test_propriedade_182.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 182: Idempotência do valuation`, mínimo de 100 iterações

  - [ ]* 7.16 Escrever teste de propriedade para candidato reprovado não influencia o resultado
    - **Property 183: Candidato reprovado não influencia o resultado (`P18.12`)**
    - **Validates: Requirements 21.3**
    - Arquivo `testes/propriedades/test_propriedade_183.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 183: Candidato reprovado não influencia o resultado`, mínimo de 100 iterações

  - [ ]* 7.17 Escrever teste de propriedade para limiar de revaluation dispara no valor exato
    - **Property 184: Limiar de revaluation dispara no valor exato (`P18.13`)**
    - **Validates: Requirements 25.1, 25.2**
    - Arquivo `testes/propriedades/test_propriedade_184.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 184: Limiar de revaluation dispara no valor exato`, mínimo de 100 iterações

  - [ ]* 7.18 Escrever teste de propriedade para comparável fora da janela nunca é atual
    - **Property 185: Comparável fora da janela nunca é atual (`P18.14`)**
    - **Validates: Requirements 21.2**
    - Arquivo `testes/propriedades/test_propriedade_185.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 185: Comparável fora da janela nunca é atual`, mínimo de 100 iterações

  - [ ]* 7.19 Escrever teste de propriedade para ausência de comparável qualificado resulta em DESCONHECIDO
    - **Property 186: Ausência de comparável qualificado resulta em DESCONHECIDO (`P18.15`)**
    - **Validates: Requirements 22.4**
    - Arquivo `testes/propriedades/test_propriedade_186.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 186: Ausência de comparável qualificado resulta em DESCONHECIDO`, mínimo de 100 iterações

  - [ ]* 7.20 Escrever testes dirigidos de seleção de comparáveis e método por tipo
    - Criar `testes/dirigidos/test_comparaveis_e_metodos.py` cobrindo os ramos de `R21` e a escolha de método por tipo de ativo de `R24`
    - _Requisitos: 21.1, 24.1_

- [ ] 8. Passo 2 de `D91` · bloco `1.6` — Economia, preço máximo e cenários

  - [ ] 8.1 Implementar o custo econômico total de treze componentes
    - Reescrever `src/radar/motores/calculo.py` (componente 9): `ComposicaoDeCusto` com os **13** componentes, cada um `Informado[Decimal]` com fonte e evidência de origem, conservando valor na soma
    - Custos de saída e imposto de renda sobre ganho de capital ficam **fora** do custo econômico total, e o custo de oportunidade do capital também: corrige `D.1.2` e a dupla contagem
    - Componente `DESCONHECIDO` propaga contingência e marca o preço máximo como provisório; valor zero só com evidência de não aplicabilidade
    - _Requisitos: 26.1, 26.1.1, 26.1.2, 26.2, 26.3, 26.4, 26.5, 26.6, 26.7, 26.8, 26.9, 26.11, 26.12_

  - [ ] 8.2 Implementar as métricas econômicas determinísticas
    - Criar `src/radar/motores/metricas.py`: desconto líquido contra o valor **base** e margem de segurança contra o valor **conservador**, corrigindo `D.1.6`
    - Yields mensal e anual consistentes, yield líquido nunca acima do bruto, base de imposto nunca negativa, break-even que zera o lucro líquido, e rejeição explícita quando o valor de mercado provável é não positivo
    - Todos os cálculos são função pura, sem entrada e saída de dados e sem dependência de modelo de linguagem
    - _Requisitos: 27.1, 27.3, 27.4, 27.5, 27.6, 27.7, 27.7.1, 27.8, 27.9, 27.10, 27.11, 27.12, 27.14, 27.16, 27.17_

  - [ ] 8.3 Implementar o preço máximo e o teto decisório
    - Criar `src/radar/motores/preco_maximo.py` (componente 10): forma fechada de `R28.2` **com ITBI** no coeficiente proporcional e verificação inversa como pré-condição de aceite, corrigindo `D.1.1`
    - Ajustado ao risco nunca excede o econômico; preço-alvo nunca excede o preço máximo; liquidez indefinida impede teto definitivo; teto decisório é o **mínimo** dos dois; oferta acima do teto implica `NAO_COMPRAR`
    - A forma fechada conservadora permanece como referência **informativa**
    - _Requisitos: 28.2, 28.2.1, 28.2.2, 28.3, 28.4, 28.4.1, 28.4.2, 28.9, 28.11, 28.12, 28.13_

  - [ ] 8.4 Implementar reforma, contingências e capital imobilizado
    - Criar `src/radar/motores/reforma.py` (componente 11): os cinco níveis de reforma, contingências, capital imobilizado e prazo, sem default numérico para `CUS-014`, `CUS-015` e `REN-005`
    - _Requisitos: 29.1, 29.2, 29.3, 30.1, 30.2_

  - [ ] 8.5 Implementar cenários, robustez e regras de decisão econômica
    - Criar `src/radar/motores/cenarios.py` (componente 12): os quatro cenários ordenados, classificação de robustez total, e sobreviver ao estressado implicando sobreviver a todos
    - Aplicar as regras econômicas de `R33`, incluindo a distância do break-even ao preço atual
    - _Requisitos: 32.1, 32.2, 32.3, 32.4, 32.6, 33.2, 33.3, 33.7_

  - [ ]* 8.6 Escrever teste de propriedade para conservação de valor no custo econômico total
    - **Property 43: Conservação de valor no custo econômico total (`P6.1`)**
    - **Validates: Requirements 26.1, 26.11**
    - Arquivo `testes/propriedades/test_propriedade_043.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 43: Conservação de valor no custo econômico total`, mínimo de 100 iterações

  - [ ]* 8.7 Escrever teste de propriedade para monotonicidade do custo econômico total
    - **Property 44: Monotonicidade do custo econômico total (`P6.2`)**
    - **Validates: Requirements 26.1**
    - Arquivo `testes/propriedades/test_propriedade_044.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 44: Monotonicidade do custo econômico total`, mínimo de 100 iterações

  - [ ]* 8.8 Escrever teste de propriedade para monotonicidade do desconto líquido
    - **Property 45: Monotonicidade do desconto líquido (`P6.3`)**
    - **Validates: Requirements 27.3**
    - Arquivo `testes/propriedades/test_propriedade_045.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 45: Monotonicidade do desconto líquido`, mínimo de 100 iterações

  - [ ]* 8.9 Escrever teste de propriedade para monotonicidade da margem
    - **Property 46: Monotonicidade da margem (`P6.4`)**
    - **Validates: Requirements 27.4, 27.5**
    - Arquivo `testes/propriedades/test_propriedade_046.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 46: Monotonicidade da margem`, mínimo de 100 iterações

  - [ ]* 8.10 Escrever teste de propriedade para identidade metamórfica desconto-margem
    - **Property 47: Identidade metamórfica desconto-margem (`P6.5`)**
    - **Validates: Requirements 27.3, 27.5**
    - Arquivo `testes/propriedades/test_propriedade_047.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 47: Identidade metamórfica desconto-margem`, mínimo de 100 iterações

  - [ ]* 8.11 Escrever teste de propriedade para consistência entre yields mensal e anual
    - **Property 48: Consistência entre yields mensal e anual (`P6.6`)**
    - **Validates: Requirements 27.6, 27.8**
    - Arquivo `testes/propriedades/test_propriedade_048.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 48: Consistência entre yields mensal e anual`, mínimo de 100 iterações

  - [ ]* 8.12 Escrever teste de propriedade para yield líquido nunca excede o bruto
    - **Property 49: Yield líquido nunca excede o bruto (`P6.7`)**
    - **Validates: Requirements 27.7, 27.8**
    - Arquivo `testes/propriedades/test_propriedade_049.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 49: Yield líquido nunca excede o bruto`, mínimo de 100 iterações

  - [ ]* 8.13 Escrever teste de propriedade para monotonicidade do yield
    - **Property 50: Monotonicidade do yield (`P6.8`)**
    - **Validates: Requirements 27.6, 27.8**
    - Arquivo `testes/propriedades/test_propriedade_050.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 50: Monotonicidade do yield`, mínimo de 100 iterações

  - [ ]* 8.14 Escrever teste de propriedade para base do imposto nunca é negativa
    - **Property 51: Base do imposto nunca é negativa (`P6.9`)**
    - **Validates: Requirements 27.10**
    - Arquivo `testes/propriedades/test_propriedade_051.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 51: Base do imposto nunca é negativa`, mínimo de 100 iterações

  - [ ]* 8.15 Escrever teste de propriedade para valor de mercado não positivo sinaliza erro
    - **Property 52: Valor de mercado não positivo sinaliza erro (`P6.10`)**
    - **Validates: Requirements 27.16**
    - Arquivo `testes/propriedades/test_propriedade_052.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 52: Valor de mercado não positivo sinaliza erro`, mínimo de 100 iterações

  - [ ]* 8.16 Escrever teste de propriedade para determinismo das métricas econômicas
    - **Property 53: Determinismo das métricas econômicas (`P6.11`)**
    - **Validates: Requirements 27.17**
    - Arquivo `testes/propriedades/test_propriedade_053.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 53: Determinismo das métricas econômicas`, mínimo de 100 iterações

  - [ ]* 8.17 Escrever teste de propriedade para break-even zera o lucro líquido
    - **Property 54: Break-even zera o lucro líquido (`P6.12`)**
    - **Validates: Requirements 27.14**
    - Arquivo `testes/propriedades/test_propriedade_054.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 54: Break-even zera o lucro líquido`, mínimo de 100 iterações

  - [ ]* 8.18 Escrever teste de propriedade para propriedade inversa do preço máximo
    - **Property 55: Propriedade inversa do preço máximo (`P7.1`)**
    - **Validates: Requirements 28.2, 28.3**
    - Arquivo `testes/propriedades/test_propriedade_055.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 55: Propriedade inversa do preço máximo`, mínimo de 100 iterações

  - [ ]* 8.19 Escrever teste de propriedade para monotonicidade decrescente no ROI alvo
    - **Property 56: Monotonicidade decrescente no ROI alvo (`P7.2`)**
    - **Validates: Requirements 28.2**
    - Arquivo `testes/propriedades/test_propriedade_056.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 56: Monotonicidade decrescente no ROI alvo`, mínimo de 100 iterações

  - [ ]* 8.20 Escrever teste de propriedade para monotonicidade decrescente nos custos fixos
    - **Property 57: Monotonicidade decrescente nos custos fixos (`P7.3`)**
    - **Validates: Requirements 28.2**
    - Arquivo `testes/propriedades/test_propriedade_057.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 57: Monotonicidade decrescente nos custos fixos`, mínimo de 100 iterações

  - [ ]* 8.21 Escrever teste de propriedade para monotonicidade crescente no valor de saída
    - **Property 58: Monotonicidade crescente no valor de saída (`P7.4`)**
    - **Validates: Requirements 28.2**
    - Arquivo `testes/propriedades/test_propriedade_058.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 58: Monotonicidade crescente no valor de saída`, mínimo de 100 iterações

  - [ ]* 8.22 Escrever teste de propriedade para preço máximo nunca é negativo
    - **Property 59: Preço máximo nunca é negativo (`P7.5`)**
    - **Validates: Requirements 28.2**
    - Arquivo `testes/propriedades/test_propriedade_059.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 59: Preço máximo nunca é negativo`, mínimo de 100 iterações

  - [ ]* 8.23 Escrever teste de propriedade para ajustado ao risco nunca excede o econômico
    - **Property 60: Ajustado ao risco nunca excede o econômico (`P7.6`)**
    - **Validates: Requirements 28.9**
    - Arquivo `testes/propriedades/test_propriedade_060.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 60: Ajustado ao risco nunca excede o econômico`, mínimo de 100 iterações

  - [ ]* 8.24 Escrever teste de propriedade para oferta acima do teto implica NAO_COMPRAR
    - **Property 61: Oferta acima do teto implica NAO_COMPRAR (`P7.7`)**
    - **Validates: Requirements 28.13, 33.2**
    - Arquivo `testes/propriedades/test_propriedade_061.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 61: Oferta acima do teto implica NAO_COMPRAR`, mínimo de 100 iterações

  - [ ]* 8.25 Escrever teste de propriedade para preço-alvo nunca excede o preço máximo
    - **Property 62: Preço-alvo nunca excede o preço máximo (`P7.8`)**
    - **Validates: Requirements 28.12**
    - Arquivo `testes/propriedades/test_propriedade_062.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 62: Preço-alvo nunca excede o preço máximo`, mínimo de 100 iterações

  - [ ]* 8.26 Escrever teste de propriedade para liquidez indefinida impede teto definitivo
    - **Property 63: Liquidez indefinida impede teto definitivo (`P7.9`)**
    - **Validates: Requirements 28.11**
    - Arquivo `testes/propriedades/test_propriedade_063.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 63: Liquidez indefinida impede teto definitivo`, mínimo de 100 iterações

  - [ ]* 8.27 Escrever teste de propriedade para teto decisório é o mínimo dos dois
    - **Property 64: Teto decisório é o mínimo dos dois (`P7.10`)**
    - **Validates: Requirements 28.4.2**
    - Arquivo `testes/propriedades/test_propriedade_064.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 64: Teto decisório é o mínimo dos dois`, mínimo de 100 iterações

  - [ ]* 8.28 Escrever teste de propriedade para monotonicidade decrescente no ITBI
    - **Property 65: Monotonicidade decrescente no ITBI (`P7.11`)**
    - **Validates: Requirements 28.2, 28.2.1**
    - Arquivo `testes/propriedades/test_propriedade_065.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 65: Monotonicidade decrescente no ITBI`, mínimo de 100 iterações

  - [ ]* 8.29 Escrever teste de propriedade para ordenação de cenários
    - **Property 66: Ordenação de cenários (`P8.1`)**
    - **Validates: Requirements 32.1, 32.2, 32.3, 32.4**
    - Arquivo `testes/propriedades/test_propriedade_066.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 66: Ordenação de cenários`, mínimo de 100 iterações

  - [ ]* 8.30 Escrever teste de propriedade para sobreviver ao estressado implica sobreviver a todos
    - **Property 67: Sobreviver ao estressado implica sobreviver a todos (`P8.2`)**
    - **Validates: Requirements 32.6**
    - Arquivo `testes/propriedades/test_propriedade_067.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 67: Sobreviver ao estressado implica sobreviver a todos`, mínimo de 100 iterações

  - [ ]* 8.31 Escrever teste de propriedade para classificação de robustez é total e consistente
    - **Property 68: Classificação de robustez é total e consistente (`P8.3`)**
    - **Validates: Requirements 32.6**
    - Arquivo `testes/propriedades/test_propriedade_068.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 68: Classificação de robustez é total e consistente`, mínimo de 100 iterações

  - [ ]* 8.32 Escrever testes dirigidos das fórmulas econômicas
    - Criar `testes/dirigidos/test_formulas_economicas.py` com o contraexemplo do teto conservador e as fronteiras de yield e de break-even
    - _Requisitos: 27.14, 28.4.1_

- [ ] 9. Passo 2 de `D91` · bloco `1.7` — Risco, liquidez, estratégia, portfólio e escore

  - [ ] 9.1 Implementar o Motor de Risco
    - Criar `src/radar/motores/risco.py` (componente 13): matriz de severidade total sobre probabilidade e impacto, monotônica; risco crítico sempre bloqueia pela camada 0
    - Bloqueio presumido traz **condição objetiva de desbloqueio**; categoria não investigada resulta em `DESCONHECIDO`; risco e incerteza são dimensões distintas
    - _Requisitos: 34.1, 34.3, 34.4, 34.5, 34.5.1, 34.5.2, 34.9, 34.10, 35.1_

  - [ ] 9.2 Implementar o Motor de Liquidez
    - Criar `src/radar/motores/liquidez.py` (componente 15): **sete** faixas contínuas e sem lacuna, escore na escala, monotônico, e margem adicional monotônica no prazo
    - Liquidez abaixo do mínimo nunca resulta em `COMPRAR`; o limiar é resolvido pelo Gestor de Parâmetros, corrigindo `D.2.3`
    - _Requisitos: 40.1, 40.2, 40.3, 40.7, 40.8, 41.4_

  - [ ] 9.3 Implementar o Motor de Estratégia
    - Criar `src/radar/motores/estrategia.py` (componente 16, parte): `Estrategia` com **6** valores e `PerfilDeAtivo` com **9**, corrigindo `D.6.5`; critérios por estratégia e limites vigentes registrados por avaliação
    - _Requisitos: 44.1, 44.2, 44.3, 44.10, 45.1, 46.1_

  - [ ] 9.4 Implementar o Gestor de Portfólio
    - Criar `src/radar/motores/portfolio.py` (componente 16, parte): capital, reserva percentual e concentração entrando por **um único caminho** no escore de prioridade
    - _Requisitos: 47.1, 47.4, 47.4.1, 47.5_

  - [ ] 9.5 Implementar o Motor de Escore e a confiança consolidada
    - Criar `src/radar/motores/escore.py` (componente 17, parte): `EscoreDeOportunidade` na escala, monotônico, com contribuições que somam o escore e todo conjunto de pesos somando 1,00
    - Confiança consolidada derivada de `CONF-001` a `CONF-005` e **versionada**, retirando a heurística do grafo e corrigindo `D.2.6`
    - `EscoreDeAderencia` com os **sete** pesos, sem qualidade econômica, e sem nenhum caminho que converta `BLOQUEAR` em `COMPRAR`
    - _Requisitos: 49.1, 49.2, 49.5, 49.6, 49.7, 50.1, 50.2, 50.3, 50.4, 50.6, 51.1, 51.1.1, 51.4_

  - [ ] 9.6 Implementar o Motor de Ranqueamento
    - Criar `src/radar/motores/ranqueamento.py` (componente 17, parte): ordem total, confluente, idempotente, consistente com o escore, com desempate determinístico
    - Bloqueados não aparecem no ranqueamento; escalas de urgência `P0`–`P4` e de atratividade `A1`–`A5` permanecem disjuntas
    - _Requisitos: 52.1, 52.1.1, 52.3, 52.4, 52.6, 52.6.1_

  - [ ] 9.7 Implementar `MT-08` — soma de pesos
    - Criar `testes/meta/test_mt_08.py`: `SCORE-001`, as cinco colunas de `SCORE-002`, os sete de `SCORE-006` e os sete de `R40.3` somam 1,00; `SCORE-005` soma 100
    - _Requisitos: 40.3, 49.5, 51.1_

  - [ ]* 9.8 Escrever teste de propriedade para severidade é total sobre probabilidade e impacto
    - **Property 69: Severidade é total sobre probabilidade e impacto (`P8.4`)**
    - **Validates: Requirements 34.3, 34.4**
    - Arquivo `testes/propriedades/test_propriedade_069.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 69: Severidade é total sobre probabilidade e impacto`, mínimo de 100 iterações

  - [ ]* 9.9 Escrever teste de propriedade para monotonicidade da severidade
    - **Property 70: Monotonicidade da severidade (`P8.5`)**
    - **Validates: Requirements 34.4**
    - Arquivo `testes/propriedades/test_propriedade_070.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 70: Monotonicidade da severidade`, mínimo de 100 iterações

  - [ ]* 9.10 Escrever teste de propriedade para risco crítico sempre bloqueia
    - **Property 71: Risco crítico sempre bloqueia (`P8.6`)**
    - **Validates: Requirements 34.5, 34.5.2, 12.3**
    - Arquivo `testes/propriedades/test_propriedade_071.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 71: Risco crítico sempre bloqueia`, mínimo de 100 iterações

  - [ ]* 9.11 Escrever teste de propriedade para categoria não investigada resulta em DESCONHECIDO
    - **Property 72: Categoria não investigada resulta em DESCONHECIDO (`P8.7`)**
    - **Validates: Requirements 34.9**
    - Arquivo `testes/propriedades/test_propriedade_072.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 72: Categoria não investigada resulta em DESCONHECIDO`, mínimo de 100 iterações

  - [ ]* 9.12 Escrever teste de propriedade para bloqueio presumido traz condição de desbloqueio
    - **Property 73: Bloqueio presumido traz condição de desbloqueio (`P8.8`)**
    - **Validates: Requirements 34.5.1**
    - Arquivo `testes/propriedades/test_propriedade_073.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 73: Bloqueio presumido traz condição de desbloqueio`, mínimo de 100 iterações

  - [ ]* 9.13 Escrever teste de propriedade para sete faixas de liquidez contínuas e sem lacuna
    - **Property 74: Sete faixas de liquidez contínuas e sem lacuna (`P9.1`)**
    - **Validates: Requirements 40.2**
    - Arquivo `testes/propriedades/test_propriedade_074.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 74: Sete faixas de liquidez contínuas e sem lacuna`, mínimo de 100 iterações

  - [ ]* 9.14 Escrever teste de propriedade para escore de liquidez permanece na escala
    - **Property 75: Escore de liquidez permanece na escala (`P9.2`)**
    - **Validates: Requirements 40.1, 40.3**
    - Arquivo `testes/propriedades/test_propriedade_075.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 75: Escore de liquidez permanece na escala`, mínimo de 100 iterações

  - [ ]* 9.15 Escrever teste de propriedade para monotonicidade do escore de liquidez
    - **Property 76: Monotonicidade do escore de liquidez (`P9.3`)**
    - **Validates: Requirements 40.3**
    - Arquivo `testes/propriedades/test_propriedade_076.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 76: Monotonicidade do escore de liquidez`, mínimo de 100 iterações

  - [ ]* 9.16 Escrever teste de propriedade para liquidez abaixo do mínimo nunca resulta em COMPRAR
    - **Property 77: Liquidez abaixo do mínimo nunca resulta em COMPRAR (`P9.4`)**
    - **Validates: Requirements 40.7**
    - Arquivo `testes/propriedades/test_propriedade_077.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 77: Liquidez abaixo do mínimo nunca resulta em COMPRAR`, mínimo de 100 iterações

  - [ ]* 9.17 Escrever teste de propriedade para margem adicional monotônica no prazo
    - **Property 78: Margem adicional monotônica no prazo (`P9.5`)**
    - **Validates: Requirements 41.4, 30.7**
    - Arquivo `testes/propriedades/test_propriedade_078.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 78: Margem adicional monotônica no prazo`, mínimo de 100 iterações

  - [ ]* 9.18 Escrever teste de propriedade para todo conjunto de pesos soma 1,00
    - **Property 79: Todo conjunto de pesos soma 1,00 (`P10.1`)**
    - **Validates: Requirements 49.5**
    - Arquivo `testes/propriedades/test_propriedade_079.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 79: Todo conjunto de pesos soma 1,00`, mínimo de 100 iterações

  - [ ]* 9.19 Escrever teste de propriedade para escoreDeOportunidade permanece na escala
    - **Property 80: EscoreDeOportunidade permanece na escala (`P10.2`)**
    - **Validates: Requirements 49.1, 49.2**
    - Arquivo `testes/propriedades/test_propriedade_080.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 80: EscoreDeOportunidade permanece na escala`, mínimo de 100 iterações

  - [ ]* 9.20 Escrever teste de propriedade para monotonicidade do EscoreDeOportunidade
    - **Property 81: Monotonicidade do EscoreDeOportunidade (`P10.3`)**
    - **Validates: Requirements 49.2**
    - Arquivo `testes/propriedades/test_propriedade_081.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 81: Monotonicidade do EscoreDeOportunidade`, mínimo de 100 iterações

  - [ ]* 9.21 Escrever teste de propriedade para contribuições somam o escore
    - **Property 82: Contribuições somam o escore (`P10.4`)**
    - **Validates: Requirements 49.7**
    - Arquivo `testes/propriedades/test_propriedade_082.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 82: Contribuições somam o escore`, mínimo de 100 iterações

  - [ ]* 9.22 Escrever teste de propriedade para escoreDeAderencia permanece na escala
    - **Property 83: EscoreDeAderencia permanece na escala (`P10.5`)**
    - **Validates: Requirements 51.1**
    - Arquivo `testes/propriedades/test_propriedade_083.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 83: EscoreDeAderencia permanece na escala`, mínimo de 100 iterações

  - [ ]* 9.23 Escrever teste de propriedade para escoreDeAderencia nunca converte BLOQUEAR em COMPRAR
    - **Property 84: EscoreDeAderencia nunca converte BLOQUEAR em COMPRAR (`P10.6`)**
    - **Validates: Requirements 51.4, 12.3**
    - Arquivo `testes/propriedades/test_propriedade_084.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 84: EscoreDeAderencia nunca converte BLOQUEAR em COMPRAR`, mínimo de 100 iterações

  - [ ]* 9.24 Escrever teste de propriedade para monotonicidade do escore de prioridade
    - **Property 85: Monotonicidade do escore de prioridade (`P10.7`)**
    - **Validates: Requirements 52.1, 52.2**
    - Arquivo `testes/propriedades/test_propriedade_085.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 85: Monotonicidade do escore de prioridade`, mínimo de 100 iterações

  - [ ]* 9.25 Escrever teste de propriedade para ranqueamento é ordem total
    - **Property 86: Ranqueamento é ordem total (`P10.8`)**
    - **Validates: Requirements 52.4**
    - Arquivo `testes/propriedades/test_propriedade_086.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 86: Ranqueamento é ordem total`, mínimo de 100 iterações

  - [ ]* 9.26 Escrever teste de propriedade para confluência do ranqueamento
    - **Property 87: Confluência do ranqueamento (`P10.9`)**
    - **Validates: Requirements 52.4**
    - Arquivo `testes/propriedades/test_propriedade_087.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 87: Confluência do ranqueamento`, mínimo de 100 iterações

  - [ ]* 9.27 Escrever teste de propriedade para consistência do ranqueamento com o escore
    - **Property 88: Consistência do ranqueamento com o escore (`P10.10`)**
    - **Validates: Requirements 52.4**
    - Arquivo `testes/propriedades/test_propriedade_088.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 88: Consistência do ranqueamento com o escore`, mínimo de 100 iterações

  - [ ]* 9.28 Escrever teste de propriedade para determinismo do desempate
    - **Property 89: Determinismo do desempate (`P10.11`)**
    - **Validates: Requirements 52.4**
    - Arquivo `testes/propriedades/test_propriedade_089.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 89: Determinismo do desempate`, mínimo de 100 iterações

  - [ ]* 9.29 Escrever teste de propriedade para bloqueados não aparecem no ranqueamento
    - **Property 90: Bloqueados não aparecem no ranqueamento (`P10.12`)**
    - **Validates: Requirements 52.3**
    - Arquivo `testes/propriedades/test_propriedade_090.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 90: Bloqueados não aparecem no ranqueamento`, mínimo de 100 iterações

  - [ ]* 9.30 Escrever teste de propriedade para idempotência do ranqueamento
    - **Property 91: Idempotência do ranqueamento (`P10.13`)**
    - **Validates: Requirements 52.4**
    - Arquivo `testes/propriedades/test_propriedade_091.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 91: Idempotência do ranqueamento`, mínimo de 100 iterações

  - [ ]* 9.31 Escrever teste de propriedade para cobertura total das faixas de escore
    - **Property 92: Cobertura total das faixas de escore (`P10.14`)**
    - **Validates: Requirements 49.6**
    - Arquivo `testes/propriedades/test_propriedade_092.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 92: Cobertura total das faixas de escore`, mínimo de 100 iterações

  - [ ]* 9.32 Escrever teste de propriedade para cobertura total do fator de confiança
    - **Property 93: Cobertura total do fator de confiança (`P10.15`)**
    - **Validates: Requirements 50.3, 50.4**
    - Arquivo `testes/propriedades/test_propriedade_093.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 93: Cobertura total do fator de confiança`, mínimo de 100 iterações

  - [ ]* 9.33 Escrever teste de propriedade para enum de situação jurídica é total e fechado
    - **Property 94: Enum de situação jurídica é total e fechado (`P10.16`)**
    - **Validates: Requirements 12.5, 12.6**
    - Arquivo `testes/propriedades/test_propriedade_094.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 94: Enum de situação jurídica é total e fechado`, mínimo de 100 iterações

  - [ ]* 9.34 Escrever teste de propriedade para sete pesos de aderência, sem qualidade econômica
    - **Property 95: Sete pesos de aderência, sem qualidade econômica (`P10.17`)**
    - **Validates: Requirements 51.1, 51.1.1**
    - Arquivo `testes/propriedades/test_propriedade_095.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 95: Sete pesos de aderência, sem qualidade econômica`, mínimo de 100 iterações

  - [ ]* 9.35 Escrever teste de propriedade para colunas por estratégia somam 1,00 com qualidade positiva
    - **Property 96: Colunas por estratégia somam 1,00 com qualidade positiva (`P10.18`)**
    - **Validates: Requirements 49.5, 49.2**
    - Arquivo `testes/propriedades/test_propriedade_096.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 96: Colunas por estratégia somam 1,00 com qualidade positiva`, mínimo de 100 iterações

  - [ ]* 9.36 Escrever teste de propriedade para concentração entra por um único caminho
    - **Property 97: Concentração entra por um único caminho (`P10.19`)**
    - **Validates: Requirements 52.1, 52.1.1, 47.4.1**
    - Arquivo `testes/propriedades/test_propriedade_097.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 97: Concentração entra por um único caminho`, mínimo de 100 iterações

  - [ ]* 9.37 Escrever teste de propriedade para escalas de urgência e atratividade são disjuntas
    - **Property 98: Escalas de urgência e atratividade são disjuntas (`P10.20`)**
    - **Validates: Requirements 52.6, 52.6.1**
    - Arquivo `testes/propriedades/test_propriedade_098.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 98: Escalas de urgência e atratividade são disjuntas`, mínimo de 100 iterações

  - [ ]* 9.38 Escrever testes dirigidos de risco, liquidez e escore
    - Criar `testes/dirigidos/test_risco_liquidez_escore.py` cobrindo as fronteiras 89,5 · 79,5 · 74,5 · 69,5 · 59,5 · 49,5 · 39,5 e o bloqueio por risco crítico presumido
    - _Requisitos: 34.5.2, 40.2, 49.6_

- [ ] 10. Passo 2 de `D91` · bloco `1.8` — Decisão de onze camadas e explicabilidade

  - [ ] 10.1 Implementar o Motor de Decisão com as onze camadas
    - Reescrever `src/radar/motores/decisao.py` (componente 18, parte): `CamadaDeDecisao` com **11** valores, camadas 8, 9 e 10 com conteúdo, camada determinante sempre a de **menor índice** entre as eliminatórias
    - `EntradaDeDecisao` **sem nenhum default**; `BLOQUEAR` não é compensável; camada posterior não anula camada anterior; `PENDENTE` e confiança insuficiente nunca resultam em `COMPRAR`
    - `COMPRAR_SE` sempre traz condição objetiva e `MONITORAR` sempre traz gatilho de reentrada; corrige `D.2.1`, `D.2.2`, `D.2.4`, `D.2.5` e `D.6.4`
    - _Requisitos: 53.1, 53.1.1, 53.2, 53.3, 53.4, 53.5, 53.7, 53.8_

  - [ ] 10.2 Declarar o catálogo das 55 regras canônicas como dados
    - Criar `src/radar/regras/catalogo.py` com as **55** regras do Anexo D declaradas como dados enumeráveis, com os **seis** tipos de regra e a precedência de escopo `Global → Investidor → Estratégia → Localização → Tipo → Oportunidade → Exceção`
    - O escopo mais específico prevalece, **exceto** quando o menos específico impõe bloqueio crítico ou restrição legal ou documental
    - _Requisitos: 54.1, 54.2, 54.10, 54.10.1_

  - [ ] 10.3 Implementar a matriz de ação de escore × confiança
    - Criar `src/radar/motores/matriz_de_acao.py`: matriz **total**, monotônica na confiança, com `BLOQUEAR` em qualquer camada prevalecendo e confiança `inconclusiva` resultando em `PENDENTE` ou `BLOQUEAR` conforme a criticidade
    - _Requisitos: 55.1, 55.8, 55.9, 55.10, 55.16_

  - [ ] 10.4 Extrair o Motor de Explicabilidade
    - Criar `src/radar/motores/explicabilidade.py` a partir de `servico_de_analise._explicar`: explicação simétrica entre aprovação e rejeição, com os elementos obrigatórios de `R56.1` e `R56.2` e rastreabilidade completa da decisão
    - _Requisitos: 56.1, 56.2, 56.5, 56.8_

  - [ ] 10.5 Implementar `MT-04` — cobertura das 55 regras
    - Criar `testes/meta/test_mt_04.py`: todo `RULE-*` do Anexo D está em `CATALOGO_DE_REGRAS`, sem regra ausente nem sobrando
    - _Requisitos: 54.1, 73.4_

  - [ ]* 10.6 Escrever teste de propriedade para totalidade da decisão
    - **Property 99: Totalidade da decisão (`P11.1`)**
    - **Validates: Requirements 53.5**
    - Arquivo `testes/propriedades/test_propriedade_099.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 99: Totalidade da decisão`, mínimo de 100 iterações

  - [ ]* 10.7 Escrever teste de propriedade para bLOQUEAR não é compensável
    - **Property 100: BLOQUEAR não é compensável (`P11.2`)**
    - **Validates: Requirements 12.3, 53.4**
    - Arquivo `testes/propriedades/test_propriedade_100.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 100: BLOQUEAR não é compensável`, mínimo de 100 iterações

  - [ ]* 10.8 Escrever teste de propriedade para camada determinante é a de menor índice
    - **Property 101: Camada determinante é a de menor índice (`P11.3`)**
    - **Validates: Requirements 53.1, 53.2, 53.3**
    - Arquivo `testes/propriedades/test_propriedade_101.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 101: Camada determinante é a de menor índice`, mínimo de 100 iterações

  - [ ]* 10.9 Escrever teste de propriedade para camada posterior não anula camada anterior
    - **Property 102: Camada posterior não anula camada anterior (`P11.4`)**
    - **Validates: Requirements 53.4**
    - Arquivo `testes/propriedades/test_propriedade_102.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 102: Camada posterior não anula camada anterior`, mínimo de 100 iterações

  - [ ]* 10.10 Escrever teste de propriedade para pENDENTE nunca resulta em COMPRAR
    - **Property 103: PENDENTE nunca resulta em COMPRAR (`P11.5`)**
    - **Validates: Requirements 12.8**
    - Arquivo `testes/propriedades/test_propriedade_103.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 103: PENDENTE nunca resulta em COMPRAR`, mínimo de 100 iterações

  - [ ]* 10.11 Escrever teste de propriedade para confiança insuficiente nunca resulta em COMPRAR
    - **Property 104: Confiança insuficiente nunca resulta em COMPRAR (`P11.6`)**
    - **Validates: Requirements 50.6**
    - Arquivo `testes/propriedades/test_propriedade_104.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 104: Confiança insuficiente nunca resulta em COMPRAR`, mínimo de 100 iterações

  - [ ]* 10.12 Escrever teste de propriedade para pendência crítica restringe a decisão
    - **Property 105: Pendência crítica restringe a decisão (`P11.7`)**
    - **Validates: Requirements 37.3**
    - Arquivo `testes/propriedades/test_propriedade_105.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 105: Pendência crítica restringe a decisão`, mínimo de 100 iterações

  - [ ]* 10.13 Escrever teste de propriedade para cOMPRAR_SE sempre traz condição objetiva
    - **Property 106: COMPRAR_SE sempre traz condição objetiva (`P11.8`)**
    - **Validates: Requirements 53.7**
    - Arquivo `testes/propriedades/test_propriedade_106.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 106: COMPRAR_SE sempre traz condição objetiva`, mínimo de 100 iterações

  - [ ]* 10.14 Escrever teste de propriedade para mONITORAR sempre traz gatilho de reentrada
    - **Property 107: MONITORAR sempre traz gatilho de reentrada (`P11.9`)**
    - **Validates: Requirements 53.8**
    - Arquivo `testes/propriedades/test_propriedade_107.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 107: MONITORAR sempre traz gatilho de reentrada`, mínimo de 100 iterações

  - [ ]* 10.15 Escrever teste de propriedade para monotonicidade da decisão na confiança
    - **Property 108: Monotonicidade da decisão na confiança (`P11.10`)**
    - **Validates: Requirements 55.1, 55.2, 55.3, 55.4, 55.5, 55.6, 55.7, 55.8, 55.9**
    - Arquivo `testes/propriedades/test_propriedade_108.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 108: Monotonicidade da decisão na confiança`, mínimo de 100 iterações

  - [ ]* 10.16 Escrever teste de propriedade para monotonicidade da decisão no desconto líquido
    - **Property 109: Monotonicidade da decisão no desconto líquido (`P11.11`)**
    - **Validates: Requirements 33.3**
    - Arquivo `testes/propriedades/test_propriedade_109.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 109: Monotonicidade da decisão no desconto líquido`, mínimo de 100 iterações

  - [ ]* 10.17 Escrever teste de propriedade para determinismo da decisão e da camada
    - **Property 110: Determinismo da decisão e da camada (`P11.12`)**
    - **Validates: Requirements 53.1**
    - Arquivo `testes/propriedades/test_propriedade_110.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 110: Determinismo da decisão e da camada`, mínimo de 100 iterações

  - [ ]* 10.18 Escrever teste de propriedade para exceção não contorna bloqueio
    - **Property 111: Exceção não contorna bloqueio (`P11.13`)**
    - **Validates: Requirements 63.4, 63.4.1**
    - Arquivo `testes/propriedades/test_propriedade_111.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 111: Exceção não contorna bloqueio`, mínimo de 100 iterações

  - [ ]* 10.19 Escrever teste de propriedade para rastreabilidade da decisão
    - **Property 112: Rastreabilidade da decisão (`P11.14`)**
    - **Validates: Requirements 56.8, 61.4**
    - Arquivo `testes/propriedades/test_propriedade_112.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 112: Rastreabilidade da decisão`, mínimo de 100 iterações

  - [ ]* 10.20 Escrever teste de propriedade para totalidade da matriz de escore × confiança
    - **Property 113: Totalidade da matriz de escore × confiança (`P11.15`)**
    - **Validates: Requirements 55.1, 55.10, 55.11, 55.12, 55.13, 55.14, 55.15, 55.16**
    - Arquivo `testes/propriedades/test_propriedade_113.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 113: Totalidade da matriz de escore × confiança`, mínimo de 100 iterações

  - [ ]* 10.21 Escrever teste de propriedade para onze camadas e a decisão não é camada
    - **Property 114: Onze camadas e a decisão não é camada (`P11.16`)**
    - **Validates: Requirements 53.1, 53.1.1**
    - Arquivo `testes/propriedades/test_propriedade_114.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 114: Onze camadas e a decisão não é camada`, mínimo de 100 iterações

  - [ ]* 10.22 Escrever teste de propriedade para ausência de evidência nunca produz resultado favorável
    - **Property 115: Ausência de evidência nunca produz resultado favorável (`P11.17`)**
    - **Validates: Requirements 36.3.1, 36.3.2**
    - Arquivo `testes/propriedades/test_propriedade_115.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 115: Ausência de evidência nunca produz resultado favorável`, mínimo de 100 iterações

  - [ ]* 10.23 Escrever teste de propriedade para evidência de ausência produz o efeito da regra
    - **Property 116: Evidência de ausência produz o efeito da regra (`P11.18`)**
    - **Validates: Requirements 15.9, 15.9.1, 15.9.2**
    - Arquivo `testes/propriedades/test_propriedade_116.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 116: Evidência de ausência produz o efeito da regra`, mínimo de 100 iterações

  - [ ]* 10.24 Escrever teste de propriedade para precedência de escopo
    - **Property 117: Precedência de escopo (`P11.19`)**
    - **Validates: Requirements 54.10, 54.10.1**
    - Arquivo `testes/propriedades/test_propriedade_117.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 117: Precedência de escopo`, mínimo de 100 iterações

  - [ ]* 10.25 Escrever testes de instantâneo da explicabilidade
    - Criar `testes/instantaneo/test_explicabilidade.py` verificando a **presença** de cada elemento obrigatório, não a redação
    - _Requisitos: 56.1, 56.2_

- [ ] 11. Passo 2 de `D91` · bloco `1.9` — Diligência, análise profunda e disciplina de lance

  - [ ] 11.1 Implementar o Gestor de Due Diligence
    - Criar `src/radar/diligencia/gestor.py` (componente 14): as **oito** fases `DD-0` a `DD-7`, pendências com item, motivo, impacto, responsável, prazo, condição objetiva de liberação e prioridade
    - Pendência crítica restringe a decisão; resolução preserva o registro
    - _Requisitos: 36.1, 36.2, 36.3, 36.4, 37.1, 37.2, 37.3_

  - [ ] 11.2 Declarar os 234 itens da versão 1 do checklist padrão como dados
    - Criar `src/radar/diligencia/catalogo.py` com `MC-001` a `MC-136`, `B-01` a `B-27` e `C-01` a `C-71` — 136 + 27 + 71 = **234** —, cada item com filtro de aplicabilidade, peso, severidade, ordem, condição de aprovação e de reprovação, resultado na ausência, prioridade na ausência, criticidade e fase
    - _Requisitos: 36.5, 92.2_

  - [ ] 11.3 Implementar visita física e contexto humano
    - Criar `src/radar/diligencia/visita.py`: registro de visita, contexto humano do ocupante e as consequências declaradas, sem transformar ausência de visita em regularidade
    - _Requisitos: 38.1, 38.5, 38.5.1, 39.1, 39.4_

  - [ ] 11.4 Implementar a Análise Profunda
    - Criar `src/radar/motores/analise_profunda.py` (componente 18, parte): tese, argumentos a favor e contra, contrapontos e as **oito** respostas obrigatórias, versionada sem sobrescrita
    - Cenários derivados são marcados como hipótese, com autor, data e motivo
    - _Requisitos: 76.1, 76.2, 77.2, 77.5_

  - [ ] 11.5 Implementar a disciplina de lance
    - Criar `src/radar/motores/disciplina_de_lance.py` (componente 19): `HS-01` a `HS-09`, `PL-01` a `PL-12`, `E01` a `E09`, `RL-01` a `RL-12` e `HL-01` a `HL-06` declarados como dados
    - Liberação pré-lance **bicondicional**; parada absoluta acionada, lance acima do teto absoluto, evicção não confirmada e divergência pendente impedem o lance; comissão nunca é subtraída do lance
    - _Requisitos: 82.1, 82.2, 82.3, 82.4, 82.5, 82.6, 82.7, 82.9, 82.10_

  - [ ] 11.6 Implementar `MT-05` — cobertura da disciplina de lance
    - Criar `testes/meta/test_mt_05.py`: `HS-01..09`, `PL-01..12`, `E01..09`, `RL-01..12` e `HL-01..06` declarados, falhando por item ausente
    - _Requisitos: 73.5, 82.1_

  - [ ]* 11.7 Escrever teste de propriedade para liberação pré-lance é bicondicional
    - **Property 133: Liberação pré-lance é bicondicional (`P14.1`)**
    - **Validates: Requirements 82.3, 82.6**
    - Arquivo `testes/propriedades/test_propriedade_133.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 133: Liberação pré-lance é bicondicional`, mínimo de 100 iterações

  - [ ]* 11.8 Escrever teste de propriedade para parada absoluta acionada impede o lance
    - **Property 134: Parada absoluta acionada impede o lance (`P14.2`)**
    - **Validates: Requirements 82.1, 82.2**
    - Arquivo `testes/propriedades/test_propriedade_134.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 134: Parada absoluta acionada impede o lance`, mínimo de 100 iterações

  - [ ]* 11.9 Escrever teste de propriedade para lance acima do teto absoluto impede o lance
    - **Property 135: Lance acima do teto absoluto impede o lance (`P14.3`)**
    - **Validates: Requirements 82.6**
    - Arquivo `testes/propriedades/test_propriedade_135.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 135: Lance acima do teto absoluto impede o lance`, mínimo de 100 iterações

  - [ ]* 11.10 Escrever teste de propriedade para evicção não confirmada impede o lance
    - **Property 136: Evicção não confirmada impede o lance (`P14.4`)**
    - **Validates: Requirements 82.4, 15.9, 15.9.1**
    - Arquivo `testes/propriedades/test_propriedade_136.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 136: Evicção não confirmada impede o lance`, mínimo de 100 iterações

  - [ ]* 11.11 Escrever teste de propriedade para liberação final exige as duas listas
    - **Property 137: Liberação final exige as duas listas (`P14.5`)**
    - **Validates: Requirements 82.5, 82.6**
    - Arquivo `testes/propriedades/test_propriedade_137.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 137: Liberação final exige as duas listas`, mínimo de 100 iterações

  - [ ]* 11.12 Escrever teste de propriedade para divergência pendente impede o lance
    - **Property 138: Divergência pendente impede o lance (`P14.6`)**
    - **Validates: Requirements 82.9, 82.10**
    - Arquivo `testes/propriedades/test_propriedade_138.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 138: Divergência pendente impede o lance`, mínimo de 100 iterações

  - [ ]* 11.13 Escrever teste de propriedade para comissão nunca é subtraída do lance
    - **Property 139: Comissão nunca é subtraída do lance (`P14.7`)**
    - **Validates: Requirements 82.7**
    - Arquivo `testes/propriedades/test_propriedade_139.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 139: Comissão nunca é subtraída do lance`, mínimo de 100 iterações

  - [ ]* 11.14 Escrever testes dirigidos de registro de visita e de pendências
    - Criar `testes/dirigidos/test_diligencia.py` cobrindo os ramos de `R38` e o recálculo por pendência resolvida
    - _Requisitos: 37.3, 38.1_

- [ ] 12. Passo 2 de `D91` · bloco `1.10` — Orquestração e fronteiras

  - [ ] 12.1 Implementar o Orquestrador com as vinte etapas e as dezesseis fases
    - Reescrever `src/radar/orquestracao/grafo.py` (componente 20, parte): as **20 etapas** de `R70.1` na ordem canônica, com as **16 fases** persistidas, incluindo deduplicação, qualificação e consolidação, corrigindo `D.6.3`
    - Curto-circuito jurídico e de identidade; traço persistido como subsequência da ordem canônica; determinismo do pipeline
    - Remover **toda** regra do grafo: a heurística de confiança e o bloqueio crítico vão para os motores
    - _Requisitos: 70.1, 70.1.1, 70.2, 70.3, 70.5, 70.6, 70.9_

  - [ ] 12.2 Implementar os guarda-corpos da IA
    - Criar `src/radar/nucleo/guarda_corpos.py`: motores determinísticos são funções puras, sem entrada e saída de dados e sem dependência de modelo de linguagem, com a fronteira declarada e verificável
    - _Requisitos: 71.1, 71.2, 71.3_

  - [ ] 12.3 Implementar os pontos mínimos de supervisão humana
    - Criar `src/radar/governanca/supervisao.py`: os **sete** pontos mínimos declarados como dados e **não removíveis** por configuração, com ator, papel, data, objeto afetado e justificativa
    - _Requisitos: 83.5, 83.6, 83.7_

  - [ ] 12.4 Implementar as configurações do investidor
    - Criar `src/radar/governanca/investidor.py` com `INV-001` a `INV-021`, incluindo reserva percentual, esforço operacional aceitável e meta de renda
    - _Requisitos: 46.6.1, 78.1, 78.2_

  - [ ] 12.5 Implementar o controle de escopo
    - Criar `src/radar/governanca/escopo.py`: o que está fora de escopo declarado não é executado silenciosamente, e a cobertura de prioridade dos requisitos é apurável
    - _Requisitos: 75.1, 75.2, 75.5_

  - [ ] 12.6 Implementar a execução sequencial de referência
    - Criar `src/radar/orquestracao/referencia.py`: implementação sequencial independente usada como oráculo de equivalência do grafo
    - _Requisitos: 70.1, 70.6_

  - [ ]* 12.7 Escrever teste de propriedade para traço é subsequência da ordem canônica
    - **Property 118: Traço é subsequência da ordem canônica (`P12.1`)**
    - **Validates: Requirements 70.1, 70.5**
    - Arquivo `testes/propriedades/test_propriedade_118.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 118: Traço é subsequência da ordem canônica`, mínimo de 100 iterações

  - [ ]* 12.8 Escrever teste de propriedade para curto-circuito jurídico
    - **Property 119: Curto-circuito jurídico (`P12.2`)**
    - **Validates: Requirements 70.2, 12.2**
    - Arquivo `testes/propriedades/test_propriedade_119.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 119: Curto-circuito jurídico`, mínimo de 100 iterações

  - [ ]* 12.9 Escrever teste de propriedade para curto-circuito de identidade
    - **Property 120: Curto-circuito de identidade (`P12.3`)**
    - **Validates: Requirements 70.3, 7.9**
    - Arquivo `testes/propriedades/test_propriedade_120.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 120: Curto-circuito de identidade`, mínimo de 100 iterações

  - [ ]* 12.10 Escrever teste de propriedade para determinismo do pipeline
    - **Property 121: Determinismo do pipeline (`P12.4`)**
    - **Validates: Requirements 70.1**
    - Arquivo `testes/propriedades/test_propriedade_121.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 121: Determinismo do pipeline`, mínimo de 100 iterações

  - [ ]* 12.11 Escrever teste de propriedade para equivalência com a execução sequencial de referência
    - **Property 122: Equivalência com a execução sequencial de referência (`P12.5`)**
    - **Validates: Requirements 70.1, 70.6**
    - Arquivo `testes/propriedades/test_propriedade_122.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 122: Equivalência com a execução sequencial de referência`, mínimo de 100 iterações

  - [ ]* 12.12 Escrever teste de propriedade para pontos mínimos de supervisão não são removíveis
    - **Property 148: Pontos mínimos de supervisão não são removíveis (`P16.5`)**
    - **Validates: Requirements 83.5, 83.6**
    - Arquivo `testes/propriedades/test_propriedade_148.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 148: Pontos mínimos de supervisão não são removíveis`, mínimo de 100 iterações

  - [ ]* 12.13 Escrever testes de integração do pipeline determinístico
    - Criar `testes/integracao/test_pipeline_deterministico.py` percorrendo as vinte etapas sobre dados sintéticos, sem banco
    - _Requisitos: 70.1, 70.5_

- [ ] 13. Checkpoint — fecha o passo 2 de `D91`
  - Executar a suíte inteira, `ruff`, `mypy --strict` e `MT-11`
  - Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 14. Passo 3 de `D91` — Persistência: modelo físico, integridade e titular

  - [ ] 14.1 Criar a migração dos enums do esquema
    - Criar `db/migracoes/001_enumeracoes.sql` declarando como tipos do banco os **60 enums de negócio** e os **7 enums de infraestrutura**, todos em português e com exatamente as contagens fixadas em *Data Models*
    - Alterar qualquer contagem passa a ser mudança de nível `alto` ou `critico`, revisável
    - _Requisitos: 53.5, 56.5, 62.4_

  - [ ] 14.2 Criar a migração das onze entidades de aquisição, fonte, captura e documentos
    - Criar `db/migracoes/002_aquisicao_e_documentos.sql` com `fontes`, `conectores`, `capturas`, `ofertas_normalizadas`, `documentos`, `versoes_de_documento`, `extracoes_de_documento`, `segmentos_de_documento`, `propostas_de_evidencia`, `debitos` e `processos_judiciais`
    - _Requisitos: 1.1, 2.1, 72.1, 83.2, 85.10, 86.1, 86.9, 87.1, 90.1, 91.1_

  - [ ] 14.3 Criar a migração das dez entidades de imóvel, identidade, perfil e processo
    - Criar `db/migracoes/003_imovel_e_identidade.sql` com `andamentos_processuais`, `imoveis`, `identificadores_de_imovel`, `vinculos_de_imovel`, `localizacoes`, `perfis_de_imovel`, `versoes_de_perfil`, `observacoes_de_preco`, `divergencias` e `portas_de_entrada` — esta última com `CHECK` que impede uma terceira porta
    - _Requisitos: 9.1, 10.2, 11.1, 74.1, 74.4, 74.5, 74.6, 84.1, 90.8_

  - [ ] 14.4 Criar a migração das vinte e sete entidades de oportunidade, triagem, análise e comparação
    - Criar `db/migracoes/004_analise_e_comparacao.sql` com `oportunidades`, `candidatos_do_radar`, `resultados_de_triagem`, `analises`, `analises_documentos`, `diferencas_de_comparacao`, `evidencias`, `fatos`, `custos`, `valuations`, `comparaveis`, `cenarios`, `riscos`, `pendencias`, `diligencias`, `checklists`, `versoes_de_checklist`, `itens_de_checklist`, `execucoes_de_checklist`, `resultados_de_item_de_checklist`, `dimensoes_de_confianca`, `avaliacoes_de_estrategia`, `escores`, `aplicacoes_de_regra`, `posicoes_no_ranking`, `analises_profundas`, `verificacoes_de_lance`, `decisoes` e `eventos_de_analise`
    - `resultados_de_triagem` **não possui** coluna de decisão, escore, valuation nem custo: a abstenção é estrutural
    - _Requisitos: 53.1, 61.1, 61.7, 67.12, 74.2, 74.3, 76.1, 82.1, 87.4, 88.1, 92.1, 92.4, 93.10_

  - [ ] 14.5 Criar a migração das treze entidades de portfólio, resultado, governança e monitoramento
    - Criar `db/migracoes/005_governanca_e_monitoramento.sql` com `investidores`, `posicoes_de_portfolio`, `resultados_reais`, `regras`, `versoes_de_regra`, `parametros`, `estrategias`, `excecoes`, `objetos_de_monitoramento`, `alertas`, `eventos_de_auditoria`, `intervencoes_humanas` e `falhas_de_integridade`
    - _Requisitos: 54.1, 57.10, 62.1, 63.1, 64.1, 74.7, 74.8, 78.1, 83.5, 86.8_

  - [ ] 14.6 Criar a migração das quinze entidades de infraestrutura e de plataforma
    - Criar `db/migracoes/006_infraestrutura.sql` com `execucoes_do_radar`, `trabalhos_assincronos`, `prompts_versionados`, `colecoes_do_indice_vetorial`, `representacoes_vetoriais`, `configuracoes_de_agendamento`, `capacidades_declaradas_de_fonte`, `sinalizadores_de_recurso`, `erros_catalogados`, `notificacoes`, `acompanhamentos`, `politicas_de_processamento_de_documento`, `chaves_de_idempotencia`, `registros_de_chamada_a_provedor` e `eventos_de_dominio`
    - Estas quinze **não** integram o dicionário de `R74`: a contagem de 63 entidades de negócio permanece inalterada
    - _Requisitos: 98.11, 100.1, 102.6, 102.9, 106.1, 109.1, 110.2, 110.6, 112.10, 113.6, 114.1, 115.3, 117.2, 121.2, 121.6_

  - [ ] 14.7 Criar a migração de titular e usuário responsável em toda entidade de negócio
    - Criar `db/migracoes/007_titular.sql` com `tenant_id UUID NOT NULL` e `usuario_responsavel_id UUID NOT NULL` nas **63** tabelas de entidade de negócio, com chave estrangeira, índice por `tenant_id` e índice composto `(tenant_id, <chave de acesso>)`
    - Declarar a política de isolamento no banco: consulta sem o predicado de titular é rejeitada informando a causa, sem retornar dado; operação de titular único registra o titular padrão do ambiente e mantém a verificação ativa
    - _Requisitos: 118.1, 118.2, 118.3, 118.5, 118.6, 118.7, 118.9, 118.10_

  - [ ] 14.8 Criar a migração dos itens de integridade 1 a 12
    - Criar `db/migracoes/008_integridade_1_12.sql`: índice único **parcial** de matrícula; unicidade de documento por vínculo e hash; `UNIQUE (fonte_id, referencia_externa)` em `oportunidades`; índice por `analise_id` em todas as filhas; `CHECK` de escala 0–100 e `CHECK (versao > 0)`; escores em `NUMERIC(5,2)`; gatilhos que rejeitam `UPDATE` e `DELETE`; `ON DELETE CASCADE` restrito a rotina nomeada; migrações versionadas com seed idempotente; contrato congelado na fronteira e ORM de todas as tabelas; índice vetorial recriado após a carga; contiguidade de versão de documento por gatilho
    - _Requisitos: 9.1, 61.2, 86.9, 87.1, 92.4, 102.1_

  - [ ] 14.9 Criar a migração dos itens de integridade 13 a 24
    - Criar `db/migracoes/009_integridade_13_24.sql`: imutabilidade do arquivo original; unicidade de execução de checklist por análise; append-only nas novas tabelas de snapshot; independência das duas dimensões de versão; unicidade de execução do Radar por fonte, janela e agendamento; append-only nas tabelas de infraestrutura; contiguidade de versão de prompt; unicidade de segmento e de representação vetorial; unicidade de chave de idempotência com validade; índice por `tenant_id`; restrição que impede consulta sem titular; `CHECK` que impede evidência posterior à data de corte
    - _Requisitos: 86.2, 86.6, 86.8, 100.4, 106.7, 109.2, 109.3, 118.2, 120.4, 120.5_

  - [ ] 14.10 Implementar o ORM de todas as tabelas com contrato congelado
    - Reescrever `src/radar/db/modelos.py` e `src/radar/db/repositorio.py`: o ORM cobre **todas** as tabelas, o tipo que atravessa a fronteira é imutável, e o repositório **exige** o identificador do titular na assinatura
    - Nenhuma conversão truncante na fronteira: escore 74,6 permanece 74,6
    - _Requisitos: 61.2, 74.1, 118.5_

  - [ ] 14.11 Implementar o Gestor de Parâmetros com hierarquia de escopo e vigência
    - Criar `src/radar/governanca/parametros.py` (componente 20, parte): resolução pela hierarquia de escopo com vigência temporal, e parâmetro `[PENDENTE-DECISÃO]` marcado e **não aplicável**
    - O banco passa a ser fonte única: as constantes Python ficam apenas como valores de arranque que geram o seed
    - _Requisitos: 62.8, 62.10, 62.11, 74.11_

  - [ ] 14.12 Gerar o seed a partir de `STR` e dos catálogos
    - Criar `scripts/gerar_seed.py` que **gera** o seed de `estrategias`, dos pesos de `SCORE-001`, `SCORE-002`, `SCORE-005` e `SCORE-006`, dos limiares de `MON-001` a `MON-017`, dos parâmetros `PORT-001` a `PORT-008` e dos **234** itens da versão 1 do checklist padrão, de forma idempotente (`ON CONFLICT DO UPDATE`)
    - Renomear `scripts/db_setup.py`, `scripts/db_check.py`, `scripts/db_cleanup.py`, `scripts/db_smoke.py` e `scripts/db_smoke_vector.py` para português e exigir confirmação em `--drop`
    - _Requisitos: 62.10, 92.2_

  - [ ] 14.13 Implementar `MT-07` — ponto único de verdade
    - Criar `testes/meta/test_mt_07.py` comparando as **três** representações — tabela `STR` do requirements, constantes Python e seed do banco — e falhando à primeira divergência
    - _Requisitos: 62.10, 73.7_

  - [ ] 14.14 Implementar `MT-09` — contagem de enums
    - Criar `testes/meta/test_mt_09.py`: cada um dos 60 enums de negócio e dos 7 de infraestrutura tem exatamente a quantidade de valores fixada em *Data Models*
    - _Requisitos: 62.4, 73.3_

  - [ ] 14.15 Implementar `MT-13` — titular em toda entidade de negócio
    - Criar `testes/meta/test_mt_13.py` percorrendo as **63** entidades do dicionário e falhando **nomeando a entidade** que não declara `tenant_id` e `usuario_responsavel_id` com índice por `tenant_id`
    - _Requisitos: 118.1, 118.10_

  - [ ] 14.16 Renomear o esquema existente por migração versionada (`D72`)
    - Criar `db/migracoes/010_renomeacao_d72.sql` renomeando tabelas, colunas, índices, restrições e enums de `db/schema.sql` para português — **por migração**, nunca por reescrita manual do esquema
    - `MT-11` passa a cobrir o esquema renomeado na mesma barreira de `ruff` e `mypy --strict`
    - _Requisitos: 94.2, 97.3_

  - [ ]* 14.17 Escrever teste de propriedade para vigência temporal das versões
    - **Property 127: Vigência temporal das versões (`P13.5`)**
    - **Validates: Requirements 62.8**
    - Arquivo `testes/propriedades/test_propriedade_127.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 127: Vigência temporal das versões`, mínimo de 100 iterações

  - [ ]* 14.18 Escrever teste de propriedade para resolução de parâmetro pelo escopo mais específico
    - **Property 130: Resolução de parâmetro pelo escopo mais específico (`P13.8`)**
    - **Validates: Requirements 62.10**
    - Arquivo `testes/propriedades/test_propriedade_130.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 130: Resolução de parâmetro pelo escopo mais específico`, mínimo de 100 iterações

  - [ ]* 14.19 Escrever teste de propriedade para parâmetro pendente de decisão nunca é aplicado
    - **Property 146: Parâmetro pendente de decisão nunca é aplicado (`P16.3`)**
    - **Validates: Requirements 74.11**
    - Arquivo `testes/propriedades/test_propriedade_146.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 146: Parâmetro pendente de decisão nunca é aplicado`, mínimo de 100 iterações

  - [ ]* 14.20 Escrever teste de propriedade para regra depende só do dicionário declarado
    - **Property 147: Regra depende só do dicionário declarado (`P16.4`)**
    - **Validates: Requirements 74.11**
    - Arquivo `testes/propriedades/test_propriedade_147.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 147: Regra depende só do dicionário declarado`, mínimo de 100 iterações

  - [ ]* 14.21 Escrever teste de propriedade para isolamento por titular
    - **Property 243: Isolamento por titular (`P21.17`)**
    - **Validates: Requirements 118.2, 118.5**
    - Arquivo `testes/propriedades/test_propriedade_243.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 243: Isolamento por titular`, mínimo de 100 iterações

  - [ ]* 14.22 Escrever teste de propriedade para presença do titular em toda entidade de negócio
    - **Property 244: Presença do titular em toda entidade de negócio (`P21.18`)**
    - **Validates: Requirements 118.1, 118.7**
    - Arquivo `testes/propriedades/test_propriedade_244.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 244: Presença do titular em toda entidade de negócio`, mínimo de 100 iterações

  - [ ]* 14.23 Escrever a integração de banco marcada com a lista de integridade
    - Criar `testes/integracao/test_integridade_do_banco.py` com `@pytest.mark.db`, cobrindo os **24** itens: índice único parcial de matrícula, idempotência de captura, idempotência de esquema e seed, gatilhos append-only, `CHECK` de escala e de versão, preservação de escala em `NUMERIC(5,2)`, unicidade de `documentos`, contiguidade de `versoes_de_documento`, execução única de checklist e rejeição de consulta sem titular
    - _Requisitos: 74.1, 118.2_

- [ ] 15. Checkpoint — fecha o passo 3 de `D91`
  - Executar a suíte inteira, `ruff`, `mypy --strict`, `MT-11` e, a partir daqui, os testes marcados com `@pytest.mark.db`
  - Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 16. Passo 4 de `D91` — Documentos e evidências

  - [ ] 16.1 Implementar o Gestor de Documentos
    - Criar `src/radar/documentos/gestor.py` (componente 22): documento como entidade de primeira classe vinculável a imóvel, oportunidade e análise, com os **nove** tipos, as **três** origens, hash do arquivo e idempotência por vínculo e hash
    - O arquivo original é permanente e nunca é substituído em razão da extração
    - _Requisitos: 86.1, 86.2, 86.3, 86.4, 86.5, 86.6, 86.9, 86.10_

  - [ ] 16.2 Implementar as versões de documento
    - Criar `src/radar/documentos/versoes.py`: numeração crescente e **sem lacuna** a partir de 1, com motivo da nova versão, autor, data e origem
    - Nova versão que contradiz evidência vigente preserva ambas e marca o fato como conflitante
    - _Requisitos: 87.1, 87.2, 87.5_

  - [ ] 16.3 Implementar a extração derivada
    - Criar `src/radar/documentos/extracao.py`: texto, páginas e segmentos como conteúdo **derivado** vinculado à versão de documento, regravável sem alterar o hash do original
    - _Requisitos: 86.6, 86.11_

  - [ ] 16.4 Implementar a verificação de integridade com pendência crítica
    - Criar `src/radar/documentos/integridade.py`: o download entrega o arquivo íntegro e recalcula o hash; divergência registra falha de integridade, abre pendência crítica e **impede** o uso do conteúdo extraído como evidência
    - _Requisitos: 86.7, 86.8_

  - [ ] 16.5 Implementar a evidência de origem manual
    - Criar `src/radar/evidencia/manual.py` (componente 26, parte): origem `USUARIO` com classe no máximo `C indicado` sem documento, sem herdar confiança de fonte oficial, e a verificação jurídica permanecendo `DESCONHECIDO` com pendência
    - _Requisitos: 89.1, 89.2, 89.3, 89.5_

  - [ ] 16.6 Implementar o registro de processo judicial e andamentos
    - Criar `src/radar/processos/registro.py` (componente 26, parte): número, órgão julgador, partes, tipo, situação, data da consulta, documento vinculado e impacto classificado; andamentos append-only
    - Impacto é `DESCONHECIDO` quando não há decisão nem andamento
    - _Requisitos: 90.1, 90.5, 90.8_

  - [ ] 16.7 Implementar o débito como entidade que compõe `CUS-005` e `CUS-006`
    - Criar `src/radar/debitos/registro.py` (componente 26, parte): os quatro tipos, valor com estado de informação, período, fonte, data da consulta, documento, as cinco situações e a responsabilidade atribuída pelo edital com cláusula e página
    - Os componentes `CUS-005` e `CUS-006` do custo econômico total passam a ser **compostos** a partir desses registros; tipo exigido e não investigado permanece `DESCONHECIDO`, nunca zero
    - _Requisitos: 91.1, 91.2, 91.3, 91.4, 91.5, 91.6, 91.7_

  - [ ]* 16.8 Escrever teste de propriedade para imutabilidade do arquivo original
    - **Property 151: Imutabilidade do arquivo original (`P17.2`)**
    - **Validates: Requirements 86.2, 86.6**
    - Arquivo `testes/propriedades/test_propriedade_151.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 151: Imutabilidade do arquivo original`, mínimo de 100 iterações

  - [ ]* 16.9 Escrever teste de propriedade para round-trip de download
    - **Property 152: Round-trip de download (`P17.3`)**
    - **Validates: Requirements 86.7, 86.8**
    - Arquivo `testes/propriedades/test_propriedade_152.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 152: Round-trip de download`, mínimo de 100 iterações

  - [ ]* 16.10 Escrever teste de propriedade para idempotência do registro de documento
    - **Property 153: Idempotência do registro de documento (`P17.4`)**
    - **Validates: Requirements 86.9**
    - Arquivo `testes/propriedades/test_propriedade_153.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 153: Idempotência do registro de documento`, mínimo de 100 iterações

  - [ ]* 16.11 Escrever teste de propriedade para evidência USUARIO não herda confiança de fonte oficial
    - **Property 155: Evidência USUARIO não herda confiança de fonte oficial (`P17.6`)**
    - **Validates: Requirements 89.3, 89.5**
    - Arquivo `testes/propriedades/test_propriedade_155.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 155: Evidência USUARIO não herda confiança de fonte oficial`, mínimo de 100 iterações

  - [ ]* 16.12 Escrever teste de propriedade para versionamento de documento é crescente e sem lacuna
    - **Property 156: Versionamento de documento é crescente e sem lacuna (`P17.7`)**
    - **Validates: Requirements 87.1, 87.2**
    - Arquivo `testes/propriedades/test_propriedade_156.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 156: Versionamento de documento é crescente e sem lacuna`, mínimo de 100 iterações

  - [ ]* 16.13 Escrever teste de propriedade para conservação do débito no custo
    - **Property 167: Conservação do débito no custo (`P17.18`)**
    - **Validates: Requirements 91.3, 91.6, 26.1**
    - Arquivo `testes/propriedades/test_propriedade_167.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 167: Conservação do débito no custo`, mínimo de 100 iterações

  - [ ]* 16.14 Escrever teste de propriedade para débito não investigado nunca vale zero
    - **Property 168: Débito não investigado nunca vale zero (`P17.19`)**
    - **Validates: Requirements 91.5, 26.10**
    - Arquivo `testes/propriedades/test_propriedade_168.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 168: Débito não investigado nunca vale zero`, mínimo de 100 iterações

  - [ ]* 16.15 Escrever a integração marcada de documentos e evidências
    - Criar `testes/integracao/test_documentos_e_evidencias.py` com `@pytest.mark.db`, cobrindo round-trip de download byte a byte, contiguidade de versões e composição de `CUS-005` a partir de débitos registrados
    - _Requisitos: 86.7, 87.1, 91.3_

- [ ] 17. Checkpoint — fecha o passo 4 de `D91`
  - Executar a suíte inteira, `ruff`, `mypy --strict`, `MT-11` e os testes marcados com `@pytest.mark.db`
  - Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 18. Passo 5 de `D91` — Análise manual ponta a ponta pela primeira porta

  - [ ] 18.1 Implementar a porta de análise manual
    - Criar `src/radar/servicos/porta_manual.py`: criação de imóvel com identificação mínima de `G0`, cadastro da oportunidade da CAIXA, e a porta registrada apenas como **proveniência**
    - `porta_de_entrada` não é lida por nenhuma camada de decisão
    - _Requisitos: 84.1, 84.2, 84.3, 84.4, 84.9, 84.10_

  - [ ] 18.2 Implementar o envio de edital e matrícula pela porta manual
    - Criar `src/radar/servicos/envio_de_documentos.py`: envio do usuário com tipo declarado, registro de IPTU, condomínio e processos como entradas manuais com contrato definido
    - _Requisitos: 86.5, 89.1, 91.1, 95.1_

  - [ ] 18.3 Executar a análise sobre evidência real
    - Reescrever `src/radar/servicos/servico_de_analise.py`: execução da análise sobre evidência real de documento, produzindo decisão, custo econômico total decomposto, valuation, riscos e pendências
    - O gate jurídico passa a operar sobre evidência real, e não sobre entrada sintética
    - _Requisitos: 95.1, 95.2, 95.5_

  - [ ] 18.4 Implementar a visão financeira oficial
    - Criar `src/radar/apresentacao/visao_financeira.py`: as catorze grandezas e os **treze** componentes decompostos, reproduzindo a **estrutura** e a rastreabilidade da planilha de referência, e **não** a aritmética onde ela foi verificadamente corrigida
    - Cada componente é navegável até a evidência que o originou; a forma fechada conservadora permanece informativa
    - _Requisitos: 96.1, 96.2, 96.3, 96.4, 96.5, 96.6_

  - [ ]* 18.5 Escrever a integração dos passos 1 a 13 do ciclo de prova pela porta manual
    - Criar `testes/integracao/test_porta_manual.py` com `@pytest.mark.db`, percorrendo do passo 1 (criar imóvel) ao passo 13 do ciclo de `R95`, com o requisito que sustenta cada passo declarado no próprio caso
    - _Requisitos: 95.1, 95.2, 95.6_

- [ ] 19. Checkpoint — fecha o passo 5 de `D91`
  - Executar a suíte inteira, `ruff`, `mypy --strict`, `MT-11` e os testes marcados com `@pytest.mark.db`
  - Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 20. Passo 6 de `D91` — Versionamento e reanálise

  - [ ] 20.1 Implementar a nova versão de análise sem sobrescrita
    - Criar `src/radar/versionamento/analises.py`: numeração monotônica e sem lacunas a partir de 1, análises anteriores imutáveis, consulta histórica retornando tipo distinto porque histórico é **hipótese**
    - A decisão histórica é reproduzível a partir das versões registradas de regra, parâmetros e checklist
    - _Requisitos: 61.1, 61.2, 61.3, 61.4, 61.5_

  - [ ] 20.2 Implementar o Comparador de Versões
    - Criar `src/radar/versionamento/comparador.py` (componente 23): as **cinco** categorias de diferença, comparação vazia se e somente se as versões são idênticas, simetria e neutralidade
    - `decisao_alterada` exige motivo não nulo, com evidências, valores, pendências e versões de regra e de parâmetro responsáveis
    - _Requisitos: 88.1, 88.4, 88.5, 88.6, 88.7, 88.9_

  - [ ] 20.3 Implementar a reexecução que não versiona
    - Criar `src/radar/versionamento/reexecucao.py`: reexecução sem mudança de entrada **não** cria versão nova e é registrada na trilha de auditoria
    - _Requisitos: 64.1, 88.10_

  - [ ] 20.4 Garantir a independência das duas dimensões de versão
    - Criar `src/radar/versionamento/dimensoes.py`: versão de documento e versão de análise são sequências separadas, e nenhuma deriva da outra — sem restrição, gatilho, sequência ou coluna calculada que as relacione
    - _Requisitos: 61.1, 87.3_

  - [ ] 20.5 Implementar a data de corte por versão de análise
    - Criar `src/radar/versionamento/data_de_corte.py` (componente 47): `VersaoDoMotor` e `DataDeCorte` registradas por versão; evidência com data de observação posterior é recusada **naquela versão**, a recusa é registrada e a evidência permanece disponível para nova versão
    - A reprodução usa apenas versões registradas
    - _Requisitos: 120.1, 120.4, 120.5, 120.7, 120.10_

  - [ ]* 20.6 Escrever teste de propriedade para versionamento monotônico e sem lacunas
    - **Property 124: Versionamento monotônico e sem lacunas (`P13.2`)**
    - **Validates: Requirements 61.1**
    - Arquivo `testes/propriedades/test_propriedade_124.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 124: Versionamento monotônico e sem lacunas`, mínimo de 100 iterações

  - [ ]* 20.7 Escrever teste de propriedade para imutabilidade das análises anteriores
    - **Property 125: Imutabilidade das análises anteriores (`P13.3`)**
    - **Validates: Requirements 61.2**
    - Arquivo `testes/propriedades/test_propriedade_125.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 125: Imutabilidade das análises anteriores`, mínimo de 100 iterações

  - [ ]* 20.8 Escrever teste de propriedade para reprodutibilidade da decisão histórica
    - **Property 126: Reprodutibilidade da decisão histórica (`P13.4`)**
    - **Validates: Requirements 61.4, 62.8**
    - Arquivo `testes/propriedades/test_propriedade_126.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 126: Reprodutibilidade da decisão histórica`, mínimo de 100 iterações

  - [ ]* 20.9 Escrever teste de propriedade para independência das dimensões de versão
    - **Property 157: Independência das dimensões de versão (`P17.8`)**
    - **Validates: Requirements 87.3, 61.1**
    - Arquivo `testes/propriedades/test_propriedade_157.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 157: Independência das dimensões de versão`, mínimo de 100 iterações

  - [ ]* 20.10 Escrever teste de propriedade para comparação vazia se e somente se idênticas
    - **Property 158: Comparação vazia se e somente se idênticas (`P17.9`)**
    - **Validates: Requirements 88.7**
    - Arquivo `testes/propriedades/test_propriedade_158.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 158: Comparação vazia se e somente se idênticas`, mínimo de 100 iterações

  - [ ]* 20.11 Escrever teste de propriedade para simetria e neutralidade da comparação
    - **Property 159: Simetria e neutralidade da comparação (`P17.10`)**
    - **Validates: Requirements 88.4, 88.9**
    - Arquivo `testes/propriedades/test_propriedade_159.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 159: Simetria e neutralidade da comparação`, mínimo de 100 iterações

  - [ ]* 20.12 Escrever teste de propriedade para decisão alterada sempre tem motivo
    - **Property 160: Decisão alterada sempre tem motivo (`P17.11`)**
    - **Validates: Requirements 88.6**
    - Arquivo `testes/propriedades/test_propriedade_160.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 160: Decisão alterada sempre tem motivo`, mínimo de 100 iterações

  - [ ]* 20.13 Escrever teste de propriedade para totalidade da classificação de diferenças
    - **Property 161: Totalidade da classificação de diferenças (`P17.12`)**
    - **Validates: Requirements 88.5**
    - Arquivo `testes/propriedades/test_propriedade_161.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 161: Totalidade da classificação de diferenças`, mínimo de 100 iterações

  - [ ]* 20.14 Escrever teste de propriedade para reexecução sem mudança não versiona
    - **Property 170: Reexecução sem mudança não versiona (`P17.21`)**
    - **Validates: Requirements 88.10, 61.1, 64.1**
    - Arquivo `testes/propriedades/test_propriedade_170.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 170: Reexecução sem mudança não versiona`, mínimo de 100 iterações

  - [ ]* 20.15 Escrever teste de propriedade para data de corte nunca admite evidência posterior
    - **Property 247: Data de corte nunca admite evidência posterior (`P21.21`)**
    - **Validates: Requirements 120.4, 120.5**
    - Arquivo `testes/propriedades/test_propriedade_247.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 247: Data de corte nunca admite evidência posterior`, mínimo de 100 iterações

  - [ ]* 20.16 Escrever teste de propriedade para reprodução usa apenas versões registradas
    - **Property 248: Reprodução usa apenas versões registradas (`P21.22`)**
    - **Validates: Requirements 120.7, 120.10**
    - Arquivo `testes/propriedades/test_propriedade_248.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 248: Reprodução usa apenas versões registradas`, mínimo de 100 iterações

  - [ ]* 20.17 Escrever a integração dos passos 14 a 18 do ciclo de prova
    - Criar `testes/integracao/test_reanalise.py` com `@pytest.mark.db`, cobrindo complementação de evidência, reanálise, comparação e preservação de todas as versões produzidas
    - _Requisitos: 95.1, 95.7_

- [ ] 21. Checkpoint — fecha o passo 6 de `D91`
  - Executar a suíte inteira, `ruff`, `mypy --strict`, `MT-11` e os testes marcados com `@pytest.mark.db`
  - Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 22. Passo 7 de `D91` — Interface de programação

  - [ ] 22.1 Implementar o contrato de programação versionável
    - Criar `src/radar/api/versionamento.py` (componente 46, parte): versão declarada no contrato, compatibilidade retroativa e depreciação registrada
    - _Requisitos: 116.1, 116.2, 116.5_

  - [ ] 22.2 Implementar as famílias de recursos e as operações expostas
    - Criar `src/radar/api/rotas/` com as famílias de recursos de `R97.1` e as operações de `R97.2`, cada operação registrando a execução na trilha de auditoria
    - _Requisitos: 97.1, 97.2, 97.6_

  - [ ] 22.3 Implementar paginação e chave de idempotência por operação
    - Criar `src/radar/api/paginacao.py`: paginação sem perda e sem repetição, limite de página respeitado, e chave de idempotência declarada por operação
    - _Requisitos: 109.1, 116.3, 116.4_

  - [ ] 22.4 Implementar autenticação e autorização em toda operação exposta
    - Criar `src/radar/api/autorizacao.py`: posse do recurso mais titular do ator mais papel exercido, em **toda** operação exposta
    - _Requisitos: 112.1, 112.2, 118.3_

  - [ ] 22.5 Traduzir o catálogo de erros na fronteira
    - Criar `src/radar/api/erros.py`: `422` em lugar de `500` na violação de contrato, referência inexistente rejeitada **com recurso e causa**, e nenhuma mensagem com detalhe técnico
    - _Requisitos: 79.9, 114.3, 114.6_

  - [ ] 22.6 Expor o contrato completo dos treze componentes do custo
    - Criar `src/radar/api/esquemas/custo.py`: os **13** componentes decompostos, cada um com valor, estado, fonte e evidência de origem, mais o total
    - _Requisitos: 96.1, 96.7, 96.8_

  - [ ] 22.7 Garantir que nenhuma rota altere captura, evidência ou versão persistida
    - Criar `src/radar/api/invariantes.py` com a verificação executável de que nenhuma operação exposta escreve em tabela append-only
    - _Requisitos: 79.1, 79.2, 97.7_

  - [ ] 22.8 Renomear recursos, campos e valores de domínio no contrato (`D72`)
    - Criar `src/radar/api/nomes.py` com o mapa único de nomes de recurso, campo e valor de domínio em português, verificado por `MT-11`
    - _Requisitos: 97.3_

  - [ ]* 22.9 Escrever teste de propriedade para paginação sem perda e sem repetição
    - **Property 239: Paginação sem perda e sem repetição (`P21.13`)**
    - **Validates: Requirements 116.3**
    - Arquivo `testes/propriedades/test_propriedade_239.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 239: Paginação sem perda e sem repetição`, mínimo de 100 iterações

  - [ ]* 22.10 Escrever teste de propriedade para limite de página respeitado
    - **Property 240: Limite de página respeitado (`P21.14`)**
    - **Validates: Requirements 116.4**
    - Arquivo `testes/propriedades/test_propriedade_240.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 240: Limite de página respeitado`, mínimo de 100 iterações

  - [ ]* 22.11 Escrever os testes de contrato da interface de programação
    - Criar `testes/contrato/test_interface_de_programacao.py` cobrindo `422` em lugar de `500` (`REG-029`), paginação e idempotência declarada
    - _Requisitos: 97.1, 116.3_

- [ ] 23. Passo 8 de `D91` — Interface do investidor

  - [ ] 23.1 Implementar o `DesignSystem`
    - Criar `frontend/src/design-system/index.ts` (componente 49, parte): catálogo visual **fechado**, com contraste de `PLT-010` calculável sobre o catálogo
    - Estado nunca depende só de cor: há representação textual ou de forma além dela
    - _Requisitos: 125.1, 125.2, 125.3, 125.9_

  - [ ] 23.2 Declarar os nove estados de tela
    - Criar `frontend/src/design-system/estados-de-tela.ts`: `EstadoDeTela` com os **nove** valores — carregando, esqueleto, vazio, erro, repetição, parcial, dado obsoleto, confirmação e sucesso — declarados por tela como **dado**, não como convenção
    - Cada classe de resposta corresponde a exatamente um estado apresentado
    - _Requisitos: 122.1, 122.2, 122.3, 122.4, 122.5, 122.6, 122.9, 122.10_

  - [ ] 23.3 Implementar painel, nova análise e ficha da oportunidade
    - Criar `frontend/src/paginas/painel.tsx`, `nova-analise.tsx` e `ficha-da-oportunidade.tsx`, integralmente em português
    - _Requisitos: 66.1, 66.2, 67.1, 67.4, 94.1, 94.2_

  - [ ] 23.4 Implementar documentos, evidências, pendências, comparação e parâmetros
    - Criar `frontend/src/paginas/documentos.tsx`, `evidencias.tsx`, `pendencias.tsx`, `comparacao.tsx` e `parametros.tsx`, com a linha do tempo dos eventos de análise
    - _Requisitos: 66.4, 67.12, 68.1, 88.1, 94.3_

  - [ ] 23.5 Implementar a visão financeira navegável até a evidência
    - Criar `frontend/src/paginas/visao-financeira.tsx`: cada um dos treze componentes navegável até a evidência de origem
    - _Requisitos: 96.2, 96.8_

  - [ ] 23.6 Implementar a navegação e a ordem canônica de leitura
    - Criar `frontend/src/navegacao/mapa.ts`: os nove destinos, distância máxima de **dois** passos, ordem canônica dos oito blocos da análise e natureza única por informação
    - _Requisitos: 123.1, 123.2, 123.3, 123.4_

  - [ ] 23.7 Implementar a responsividade em tela estreita
    - Criar `frontend/src/design-system/responsividade.ts`: decisão, bloqueios, pendências e explicação preservados em toda largura declarada, e alternativa responsiva para **toda** tabela
    - _Requisitos: 124.1, 124.3, 124.7_

  - [ ] 23.8 Implementar a acessibilidade automatizável
    - Criar `frontend/src/design-system/acessibilidade.ts`: rótulo associado a campo, mensagem de erro associada ao campo, alcançabilidade por teclado com ordem de foco declarada e foco visível
    - _Requisitos: 125.4, 125.5, 125.6_

  - [ ] 23.9 Declarar as verificações manuais de acessibilidade como registro verificável
    - Criar `testes/acessibilidade/registro_manual.py` com o catálogo executável das verificações **não automatizáveis** — leitura por leitor de tela, navegação por voz, uso com ampliador, contraste em condição real e uso com uma das mãos —, cada uma com roteiro declarado e resultado registrado
    - O registro **falha** se qualquer verificação manual for reportada como satisfeita por inferência a partir da declaração: o verde da suíte não é lido como acessibilidade comprovada
    - _Requisitos: 124.4, 125.7, 125.10_

  - [ ] 23.10 Implementar `MT-16` — nove estados por tela
    - Criar `testes/meta/test_mt_16.py`: cada `DeclaracaoDeTela` declara os nove valores de `EstadoDeTela`, falhando ao **nomear a tela e o estado ausente** (`REG-054`)
    - _Requisitos: 122.1, 122.10_

  - [ ]* 23.11 Escrever teste de propriedade para totalidade dos estados de tela
    - **Property 251: Totalidade dos estados de tela (`P22.1`)**
    - **Validates: Requirements 122.1, 122.9**
    - Arquivo `testes/propriedades/test_propriedade_251.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 251: Totalidade dos estados de tela`, mínimo de 100 iterações

  - [ ]* 23.12 Escrever teste de propriedade para estado corresponde à resposta
    - **Property 252: Estado corresponde à resposta (`P22.2`)**
    - **Validates: Requirements 122.2, 122.3, 122.4, 122.5, 122.6**
    - Arquivo `testes/propriedades/test_propriedade_252.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 252: Estado corresponde à resposta`, mínimo de 100 iterações

  - [ ]* 23.13 Escrever teste de propriedade para ordem de leitura da análise
    - **Property 253: Ordem de leitura da análise (`P22.3`)**
    - **Validates: Requirements 123.3**
    - Arquivo `testes/propriedades/test_propriedade_253.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 253: Ordem de leitura da análise`, mínimo de 100 iterações

  - [ ]* 23.14 Escrever teste de propriedade para distância de navegação
    - **Property 254: Distância de navegação (`P22.4`)**
    - **Validates: Requirements 123.2**
    - Arquivo `testes/propriedades/test_propriedade_254.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 254: Distância de navegação`, mínimo de 100 iterações

  - [ ]* 23.15 Escrever teste de propriedade para natureza única por informação
    - **Property 255: Natureza única por informação (`P22.5`)**
    - **Validates: Requirements 123.4**
    - Arquivo `testes/propriedades/test_propriedade_255.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 255: Natureza única por informação`, mínimo de 100 iterações

  - [ ]* 23.16 Escrever teste de propriedade para preservação em tela estreita
    - **Property 256: Preservação em tela estreita (`P22.6`)**
    - **Validates: Requirements 124.1, 124.7**
    - Arquivo `testes/propriedades/test_propriedade_256.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 256: Preservação em tela estreita`, mínimo de 100 iterações

  - [ ]* 23.17 Escrever teste de propriedade para tabela sempre tem alternativa responsiva
    - **Property 257: Tabela sempre tem alternativa responsiva (`P22.7`)**
    - **Validates: Requirements 124.3**
    - Arquivo `testes/propriedades/test_propriedade_257.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 257: Tabela sempre tem alternativa responsiva`, mínimo de 100 iterações

  - [ ]* 23.18 Escrever teste de propriedade para catálogo visual fechado
    - **Property 258: Catálogo visual fechado (`P22.8`)**
    - **Validates: Requirements 125.1, 125.3**
    - Arquivo `testes/propriedades/test_propriedade_258.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 258: Catálogo visual fechado`, mínimo de 100 iterações

  - [ ]* 23.19 Escrever teste de propriedade para estado nunca depende só de cor
    - **Property 259: Estado nunca depende só de cor (`P22.9`)**
    - **Validates: Requirements 125.9**
    - Arquivo `testes/propriedades/test_propriedade_259.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 259: Estado nunca depende só de cor`, mínimo de 100 iterações

  - [ ]* 23.20 Escrever teste de propriedade para acessibilidade de formulário
    - **Property 260: Acessibilidade de formulário (`P22.10`)**
    - **Validates: Requirements 125.5**
    - Arquivo `testes/propriedades/test_propriedade_260.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 260: Acessibilidade de formulário`, mínimo de 100 iterações

  - [ ]* 23.21 Escrever teste de propriedade para operação por teclado
    - **Property 261: Operação por teclado (`P22.11`)**
    - **Validates: Requirements 125.4**
    - Arquivo `testes/propriedades/test_propriedade_261.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 261: Operação por teclado`, mínimo de 100 iterações

  - [ ]* 23.22 Escrever os testes de renderização e de acessibilidade automatizada
    - Criar `frontend/src/__testes__/acessibilidade.test.tsx` cobrindo rótulo associado, foco visível e alternativa responsiva de tabela
    - _Requisitos: 124.3, 125.4, 125.5_

- [ ] 24. Checkpoint — fecha o passo 8 de `D91` · **primeiro marco funcional**
  - Este é o primeiro marco funcional de `D91`: análise manual real de um imóvel da CAIXA, do documento à **decisão apresentada na interface**, incluindo complementação de evidência e reanálise
  - Executar a suíte inteira, `ruff`, `mypy --strict`, `MT-11` e os testes marcados com `@pytest.mark.db`
  - Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 25. Passo 9 de `D91` — IA documental

  - [ ] 25.1 Implementar os adaptadores de provedor de modelo e de embedding
    - Criar `src/radar/adaptadores/modelo_de_linguagem/openai.py`, `.../local.py` e `src/radar/adaptadores/embedding/openai.py` (componente 28, lado do adaptador), implementando os contratos declarados no núcleo
    - Troca de provedor ou de modelo **não altera** o resultado determinístico para as mesmas evidências e versões
    - _Requisitos: 98.1, 98.2, 98.3, 98.8, 98.9_

  - [ ] 25.2 Implementar o registro de chamada a provedor
    - Criar `src/radar/ia/registro_de_chamada.py`: identificador de correlação, tarefa, provedor, modelo, versão, tokens de entrada e de saída, duração, custo estimado e truncamento, append-only
    - _Requisitos: 98.11_

  - [ ] 25.3 Implementar o Gestor de Custo de IA
    - Criar `src/radar/ia/custo.py` (componente 29): `OrcamentoDeExecucaoDeIA` de `IA-003` e `IA-004`, com interrupção registrada e execução marcada como parcial quando o orçamento é atingido
    - Orçamento **nunca** é excedido em silêncio: a interrupção registra orçamento, consumo e identificador de correlação
    - _Requisitos: 99.1, 99.2, 99.3, 99.4_

  - [ ] 25.4 Implementar o cache de resposta e de representação vetorial
    - Criar `src/radar/ia/cache.py`: cache idempotente de resposta e de representação vetorial, com reprocessamento mínimo quando nada mudou
    - _Requisitos: 99.5, 99.7, 99.12_

  - [ ] 25.5 Implementar o prompt versionado e o registro de versões de IA
    - Criar `src/radar/ia/prompts.py` (componente 30): `prompt_id`, versão contígua a partir de 1, conteúdo, tarefa, autor, data, motivo e diferença em relação à versão anterior
    - Interpretação registrada é **imutável** e sempre rastreável até a versão de prompt e de modelo que a produziu
    - _Requisitos: 100.1, 100.2, 100.4, 100.5, 100.6, 100.9, 100.10_

  - [ ] 25.6 Implementar a extração e o OCR com falha explícita e conteúdo parcial
    - Criar `src/radar/ia/extracao.py`: falha de extração é declarada, conteúdo parcial é marcado como parcial, e campo ausente no documento permanece `DESCONHECIDO`
    - _Requisitos: 101.8, 105.2, 105.5_

  - [ ] 25.7 Implementar as regras anti-alucinação na fronteira da saída estruturada
    - Criar `src/radar/ia/saida_estruturada.py`: nenhuma afirmação sem trecho de origem, esquema de saída **total**, e ausência de evidência que nunca vira afirmação
    - _Requisitos: 105.1, 105.3, 105.6, 105.7_

  - [ ]* 25.8 Escrever teste de propriedade para invariância de provedor
    - **Property 187: Invariância de provedor (`P19.1`)**
    - **Validates: Requirements 98.9, 98.5**
    - Arquivo `testes/propriedades/test_propriedade_187.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 187: Invariância de provedor`, mínimo de 100 iterações

  - [ ]* 25.9 Escrever teste de propriedade para registro completo de chamada a provedor
    - **Property 189: Registro completo de chamada a provedor (`P19.3`)**
    - **Validates: Requirements 98.11**
    - Arquivo `testes/propriedades/test_propriedade_189.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 189: Registro completo de chamada a provedor`, mínimo de 100 iterações

  - [ ]* 25.10 Escrever teste de propriedade para orçamento nunca é excedido em silêncio
    - **Property 190: Orçamento nunca é excedido em silêncio (`P19.4`)**
    - **Validates: Requirements 99.2, 99.3, 99.4**
    - Arquivo `testes/propriedades/test_propriedade_190.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 190: Orçamento nunca é excedido em silêncio`, mínimo de 100 iterações

  - [ ]* 25.11 Escrever teste de propriedade para idempotência do cache de resposta
    - **Property 191: Idempotência do cache de resposta (`P19.5`)**
    - **Validates: Requirements 99.5**
    - Arquivo `testes/propriedades/test_propriedade_191.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 191: Idempotência do cache de resposta`, mínimo de 100 iterações

  - [ ]* 25.12 Escrever teste de propriedade para reprocessamento mínimo
    - **Property 192: Reprocessamento mínimo (`P19.6`)**
    - **Validates: Requirements 99.7, 99.12**
    - Arquivo `testes/propriedades/test_propriedade_192.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 192: Reprocessamento mínimo`, mínimo de 100 iterações

  - [ ]* 25.13 Escrever teste de propriedade para rastreabilidade de versão da interpretação
    - **Property 193: Rastreabilidade de versão da interpretação (`P19.7`)**
    - **Validates: Requirements 100.2, 100.6**
    - Arquivo `testes/propriedades/test_propriedade_193.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 193: Rastreabilidade de versão da interpretação`, mínimo de 100 iterações

  - [ ]* 25.14 Escrever teste de propriedade para imutabilidade da interpretação registrada
    - **Property 194: Imutabilidade da interpretação registrada (`P19.8`)**
    - **Validates: Requirements 100.5, 100.9, 100.10**
    - Arquivo `testes/propriedades/test_propriedade_194.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 194: Imutabilidade da interpretação registrada`, mínimo de 100 iterações

  - [ ]* 25.15 Escrever a integração marcada de provedor de modelo
    - Criar `testes/integracao/test_provedor_de_modelo.py` com `@pytest.mark.provedor_de_modelo` e **um a três** exemplos representativos; nas propriedades, apenas dublê
    - _Requisitos: 98.3, 105.9_

- [ ] 26. Passo 10 de `D91` — Recuperação

  - [ ] 26.1 Implementar o Motor de Recuperação com o pipeline de dez etapas
    - Criar `src/radar/conhecimento/recuperacao.py` (componente 31): extração, limpeza, segmentação, atribuição de metadados, geração de representação vetorial, indexação, busca, reordenação, montagem de contexto até `IA-010` trechos e entrega
    - O que a recuperação entrega é **apoio à interpretação** — nunca evidência, valor de cálculo ou verdade transacional
    - _Requisitos: 101.1, 101.9, 101.11_

  - [ ] 26.2 Implementar a segmentação com os treze metadados obrigatórios
    - Criar `src/radar/conhecimento/segmentacao.py`: os **treze** metadados por segmento, com `UNIQUE (extracao_id, indice_do_segmento)` tornando a reingestão idempotente
    - _Requisitos: 101.2_

  - [ ] 26.3 Implementar a citação resolvível
    - Criar `src/radar/conhecimento/citacao.py`: toda citação resolve documento, versão, página e trecho; trecho sem citação resolvível é **descartado** do contexto e a ocorrência é registrada
    - _Requisitos: 101.3, 101.4_

  - [ ] 26.4 Implementar `NaturezaDaInformacao` e as três coleções
    - Criar `src/radar/conhecimento/colecoes.py`: conhecimento normativo, dados do imóvel e histórico, cada coleção com política de atualização e validade própria da tabela `FRESH`
    - As naturezas da informação permanecem separadas: fato do documento, interpretação da IA, resultado determinístico e pendente
    - _Requisitos: 101.5, 101.6, 101.10_

  - [ ] 26.5 Implementar o Índice Vetorial reconstruível
    - Criar `src/radar/adaptadores/indice_vetorial/pgvector.py` (componente 32): artefato **derivado e reconstruível**, com coleções versionadas e índice criado depois da ingestão
    - Reconstrução com o mesmo modelo e a mesma segmentação **não altera** decisão, camada determinante, resultados determinísticos, versões de análise nem evidências
    - _Requisitos: 102.1, 102.2, 102.7, 102.9_

  - [ ] 26.6 Implementar a migração de representação vetorial
    - Criar `src/radar/adaptadores/indice_vetorial/migracao.py`: o vetor vive em `representacoes_vetoriais` com dimensão própria, permitindo conviver mais de um provedor sobre o mesmo segmento sem tocar o arquivo original
    - _Requisitos: 102.3, 102.5, 102.6_

  - [ ] 26.7 Implementar a degradação declarada com índice indisponível
    - Criar `src/radar/conhecimento/degradacao.py`: índice indisponível executa a análise sem a etapa de recuperação, marca a etapa como não executada e **não contamina** o resultado determinístico
    - _Requisitos: 102.8_

  - [ ]* 26.8 Escrever teste de propriedade para citação sempre resolvível
    - **Property 195: Citação sempre resolvível (`P19.9`)**
    - **Validates: Requirements 101.3, 101.4**
    - Arquivo `testes/propriedades/test_propriedade_195.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 195: Citação sempre resolvível`, mínimo de 100 iterações

  - [ ]* 26.9 Escrever teste de propriedade para metadados mínimos do segmento
    - **Property 196: Metadados mínimos do segmento (`P19.10`)**
    - **Validates: Requirements 101.2**
    - Arquivo `testes/propriedades/test_propriedade_196.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 196: Metadados mínimos do segmento`, mínimo de 100 iterações

  - [ ]* 26.10 Escrever teste de propriedade para separação de naturezas da informação
    - **Property 197: Separação de naturezas da informação (`P19.11`)**
    - **Validates: Requirements 101.5, 101.6**
    - Arquivo `testes/propriedades/test_propriedade_197.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 197: Separação de naturezas da informação`, mínimo de 100 iterações

  - [ ]* 26.11 Escrever teste de propriedade para reconstrução do índice não altera resultado
    - **Property 198: Reconstrução do índice não altera resultado (`P19.12`)**
    - **Validates: Requirements 102.7**
    - Arquivo `testes/propriedades/test_propriedade_198.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 198: Reconstrução do índice não altera resultado`, mínimo de 100 iterações

  - [ ]* 26.12 Escrever teste de propriedade para reindexação preserva o arquivo original
    - **Property 199: Reindexação preserva o arquivo original (`P19.13`)**
    - **Validates: Requirements 102.3, 102.6, 86.2**
    - Arquivo `testes/propriedades/test_propriedade_199.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 199: Reindexação preserva o arquivo original`, mínimo de 100 iterações

  - [ ]* 26.13 Escrever teste de propriedade para degradação sem contaminação
    - **Property 200: Degradação sem contaminação (`P19.14`)**
    - **Validates: Requirements 102.8**
    - Arquivo `testes/propriedades/test_propriedade_200.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 200: Degradação sem contaminação`, mínimo de 100 iterações

  - [ ]* 26.14 Escrever a integração marcada de recuperação
    - Criar `testes/integracao/test_recuperacao.py` com `@pytest.mark.db` e `@pytest.mark.provedor_de_modelo`, cobrindo reconstrução de índice e preservação do original (`REG-050`)
    - _Requisitos: 102.3, 102.7_

- [ ] 27. Checkpoint — fecha o passo 10 de `D91`
  - Executar a suíte inteira, `ruff`, `mypy --strict`, `MT-11` e os testes marcados com `@pytest.mark.db`
  - Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 28. Passo 11 de `D91` — Orquestração de workflow de IA

  - [ ] 28.1 Implementar o Orquestrador de Workflow de IA
    - Criar `src/radar/ia/workflow.py` (componente 33, LangGraph): as **onze** etapas na ordem obrigatória, de carregar documentos a produzir explicação
    - O workflow **não altera** a ordem obrigatória do pipeline de `R70.1` nem a precedência de decisão de `R53`
    - _Requisitos: 103.1, 103.2, 103.14_

  - [ ] 28.2 Implementar o estado explícito e o ponto de retomada por etapa
    - Criar `src/radar/ia/estado_do_workflow.py`: cada etapa concluída registra o ponto de retomada, e retomar produz o **mesmo** resultado da execução contínua com as mesmas entradas e versões
    - _Requisitos: 103.3, 103.4, 103.5, 103.6_

  - [ ] 28.3 Implementar limite de tempo, tentativas e execução parcial retomável
    - Criar `src/radar/ia/limites_do_workflow.py`: falha da recuperação registra limitação declarada e o workflow prossegue; se a etapa do motor determinístico não conclui, **nenhuma decisão é emitida** e a análise fica registrada como incompleta
    - _Requisitos: 103.7, 103.8, 103.11_

  - [ ] 28.4 Implementar os sete pontos de intervenção humana registrada
    - Criar `src/radar/ia/intervencao_humana.py`: saída não estruturada após `IA-007` tentativas e validação de evidência candidata escalam para ato humano registrado, com ator, papel, data e justificativa
    - _Requisitos: 83.5, 103.9, 103.10_

  - [ ] 28.5 Implementar a idempotência da execução e a versão do grafo
    - Criar `src/radar/ia/idempotencia_do_workflow.py`: mesma chave de idempotência produz exatamente um efeito persistido, e a versão do grafo é registrada em cada execução
    - _Requisitos: 103.12, 103.13_

  - [ ]* 28.6 Escrever teste de propriedade para retomada equivalente do workflow
    - **Property 201: Retomada equivalente do workflow (`P19.15`)**
    - **Validates: Requirements 103.5, 103.6**
    - Arquivo `testes/propriedades/test_propriedade_201.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 201: Retomada equivalente do workflow`, mínimo de 100 iterações

  - [ ]* 28.7 Escrever teste de propriedade para idempotência da execução do workflow
    - **Property 202: Idempotência da execução do workflow (`P19.16`)**
    - **Validates: Requirements 103.12, 109.3**
    - Arquivo `testes/propriedades/test_propriedade_202.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 202: Idempotência da execução do workflow`, mínimo de 100 iterações

  - [ ]* 28.8 Escrever a integração de retomada do workflow
    - Criar `testes/integracao/test_retomada_do_workflow.py` com `@pytest.mark.provedor_de_modelo`, cobrindo interrupção após a extração e retomada equivalente (`REG-056`)
    - _Requisitos: 103.4, 103.5_

- [ ] 29. Passo 12 de `D91` — Agentes, ferramentas de contexto e avaliação de IA

  - [ ] 29.1 Implementar os cinco agentes limitados
    - Criar `src/radar/ia/agentes/` (componente 34, parte) com os **cinco** `AgenteLimitado`, cada um com escopo e ferramentas declarados
    - Nenhum agente supera parada absoluta nem cria evidência: agente produz `PropostaDeEvidencia`
    - _Requisitos: 104.1, 104.2, 104.3, 104.4_

  - [ ] 29.2 Implementar o Servidor de Ferramentas com catálogos separados
    - Criar `src/radar/ia/ferramentas/leitura.py` e `src/radar/ia/ferramentas/escrita.py` (componente 34, parte, MCP): catálogos **separados** de leitura e de escrita
    - _Requisitos: 104.5, 104.6, 104.7, 104.8_

  - [ ] 29.3 Implementar a política de escrita por ferramenta
    - Criar `src/radar/ia/ferramentas/politica_de_escrita.py`: autorização, validação de esquema, idempotência e auditoria em **toda** escrita; invocação sem autorização é recusada sem efeito e com a causa informada
    - _Requisitos: 104.9, 104.10, 104.11, 104.12_

  - [ ] 29.4 Implementar o Avaliador de IA
    - Criar `src/radar/ia/avaliacao.py` (componente 35): cada execução registra, por caso, documento, resultado esperado, resultado obtido, versão do prompt e versão do modelo
    - _Requisitos: 105.8, 105.9, 105.12, 105.13_

  - [ ] 29.5 Implementar a suíte de avaliação de IA com as nove verificações, separada da suíte de propriedades
    - Criar `testes/avaliacao_de_ia/` com **diretório e barreira próprios**, casos-ouro de documento e as **nove** verificações: correção da extração, correção da citação, ausência de alucinação, preservação de `DESCONHECIDO`, consistência da saída estruturada, qualidade da recuperação, correção da classificação, regressão de prompt e regressão de modelo
    - A suíte de avaliação **não substitui** a suíte de propriedades e não é contada entre as 262 propriedades: mudança de versão de prompt ou de modelo executa a suíte e registra a comparação, e regressão em qualquer caso-ouro impede a promoção sem aceitação explícita
    - _Requisitos: 105.8, 105.10, 105.11, 105.13_

  - [ ]* 29.6 Escrever teste de propriedade para escrita por ferramenta é idempotente e auditada
    - **Property 203: Escrita por ferramenta é idempotente e auditada (`P19.17`)**
    - **Validates: Requirements 104.9, 104.11**
    - Arquivo `testes/propriedades/test_propriedade_203.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 203: Escrita por ferramenta é idempotente e auditada`, mínimo de 100 iterações

  - [ ]* 29.7 Escrever teste de propriedade para autorização é necessária na escrita por ferramenta
    - **Property 204: Autorização é necessária na escrita por ferramenta (`P19.18`)**
    - **Validates: Requirements 104.10**
    - Arquivo `testes/propriedades/test_propriedade_204.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 204: Autorização é necessária na escrita por ferramenta`, mínimo de 100 iterações

  - [ ]* 29.8 Escrever teste de propriedade para preservação de DESCONHECIDO na extração por IA
    - **Property 205: Preservação de DESCONHECIDO na extração por IA (`P19.19`)**
    - **Validates: Requirements 105.2, 105.5**
    - Arquivo `testes/propriedades/test_propriedade_205.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 205: Preservação de DESCONHECIDO na extração por IA`, mínimo de 100 iterações

  - [ ]* 29.9 Escrever teste de propriedade para ausência de evidência nunca vira afirmação
    - **Property 206: Ausência de evidência nunca vira afirmação (`P19.20`)**
    - **Validates: Requirements 105.1, 105.2, 105.3**
    - Arquivo `testes/propriedades/test_propriedade_206.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 206: Ausência de evidência nunca vira afirmação`, mínimo de 100 iterações

  - [ ]* 29.10 Escrever teste de propriedade para totalidade do esquema de saída estruturada
    - **Property 207: Totalidade do esquema de saída estruturada (`P19.21`)**
    - **Validates: Requirements 105.6, 105.7**
    - Arquivo `testes/propriedades/test_propriedade_207.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 207: Totalidade do esquema de saída estruturada`, mínimo de 100 iterações

  - [ ]* 29.11 Escrever teste de propriedade para nenhum agente supera parada absoluta
    - **Property 208: Nenhum agente supera parada absoluta (`P19.22`)**
    - **Validates: Requirements 104.3, 53.4**
    - Arquivo `testes/propriedades/test_propriedade_208.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 208: Nenhum agente supera parada absoluta`, mínimo de 100 iterações

  - [ ]* 29.12 Escrever a regressão marcada de prompt e de modelo
    - Criar `testes/avaliacao_de_ia/test_regressao_de_versao.py` com `@pytest.mark.provedor_de_modelo`, cobrindo `REG-051`
    - _Requisitos: 105.10, 105.11_

- [ ] 30. Checkpoint — fecha o passo 12 de `D91`
  - Executar a suíte inteira, `ruff`, `mypy --strict`, `MT-11` e os testes marcados com `@pytest.mark.db`
  - Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 31. Passo 13 de `D91` — Framework de conector

  - [ ] 31.1 Implementar o contrato único de Conector de Fonte
    - Criar `src/radar/conectores/contrato.py` (componente 21): listar ofertas, obter detalhe, obter documentos e declarar cobertura, e nada além disso
    - A estratégia de aquisição é detalhe de infraestrutura e **não é exposta** a entidades, regras, parâmetros ou motores; nova fonte exige implementar o contrato e cadastrar a fonte, e nada mais
    - _Requisitos: 85.1, 85.2, 85.3, 85.5, 85.7, 85.8_

  - [ ] 31.2 Implementar `EstrategiaDeCaptura` como adaptador com os quatro valores
    - Criar `src/radar/adaptadores/captura/pagina_publica.py`, `endpoint.py`, `arquivo.py` e `varredura.py` (componente 37, parte)
    - A estratégia aparece apenas na Execução do Radar e na captura: payload igual obtido por estratégias diferentes produz resultado idêntico
    - _Requisitos: 106.1, 106.8, 107.4_

  - [ ] 31.3 Implementar o Validador de Captura com as seis verificações
    - Criar `src/radar/captura/validacao.py` (componente 37, parte): validação **total**, com a verificação não satisfeita nomeada, erro `FONTE_ALTERADA` registrado, payload bruto preservado e **nada** propagado ao domínio
    - Resposta vazia é resultado inválido por quantidade implausível e **nunca** remove oferta conhecida; conteúdo não interpretável mantém a última captura válida vigente
    - _Requisitos: 107.1, 107.2, 107.3, 107.8, 107.9_

  - [ ] 31.4 Implementar a resiliência do conector
    - Criar `src/radar/conectores/resiliencia.py`: limite de tempo, retry, limite de taxa, paginação, ponto de retomada e **disjuntor** monotônico nas falhas, com abertura registrada e retomada apenas após o intervalo configurado
    - _Requisitos: 107.4, 107.5, 107.6, 107.7, 107.10_

  - [ ] 31.5 Implementar as capacidades declaradas por fonte
    - Criar `src/radar/conectores/capacidades.py` (componente 40, parte): as dez capacidades declaradas por fonte, com data da última declaração
    - _Requisitos: 110.6, 110.7_

  - [ ]* 31.6 Escrever teste de propriedade para desacoplamento do conector
    - **Property 169: Desacoplamento do conector (`P17.20`)**
    - **Validates: Requirements 85.3, 85.5**
    - Arquivo `testes/propriedades/test_propriedade_169.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 169: Desacoplamento do conector`, mínimo de 100 iterações

  - [ ]* 31.7 Escrever teste de propriedade para totalidade da validação de captura
    - **Property 213: Totalidade da validação de captura (`P20.5`)**
    - **Validates: Requirements 107.1, 107.2**
    - Arquivo `testes/propriedades/test_propriedade_213.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 213: Totalidade da validação de captura`, mínimo de 100 iterações

  - [ ]* 31.8 Escrever teste de propriedade para mudança de estrutura da fonte é observável
    - **Property 214: Mudança de estrutura da fonte é observável (`P20.6`)**
    - **Validates: Requirements 107.3**
    - Arquivo `testes/propriedades/test_propriedade_214.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 214: Mudança de estrutura da fonte é observável`, mínimo de 100 iterações

  - [ ]* 31.9 Escrever teste de propriedade para resposta vazia nunca remove oferta
    - **Property 215: Resposta vazia nunca remove oferta (`P20.7`)**
    - **Validates: Requirements 107.8**
    - Arquivo `testes/propriedades/test_propriedade_215.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 215: Resposta vazia nunca remove oferta`, mínimo de 100 iterações

  - [ ]* 31.10 Escrever teste de propriedade para retomada da captura
    - **Property 216: Retomada da captura (`P20.8`)**
    - **Validates: Requirements 107.5, 107.6**
    - Arquivo `testes/propriedades/test_propriedade_216.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 216: Retomada da captura`, mínimo de 100 iterações

  - [ ]* 31.11 Escrever teste de propriedade para disjuntor monotônico nas falhas
    - **Property 217: Disjuntor monotônico nas falhas (`P20.9`)**
    - **Validates: Requirements 107.7**
    - Arquivo `testes/propriedades/test_propriedade_217.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 217: Disjuntor monotônico nas falhas`, mínimo de 100 iterações

  - [ ]* 31.12 Escrever teste de propriedade para limite de taxa respeitado
    - **Property 218: Limite de taxa respeitado (`P20.10`)**
    - **Validates: Requirements 107.4**
    - Arquivo `testes/propriedades/test_propriedade_218.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 218: Limite de taxa respeitado`, mínimo de 100 iterações

  - [ ]* 31.13 Escrever a integração marcada de fonte externa
    - Criar `testes/integracao/test_fonte_externa.py` com `@pytest.mark.fonte_externa` e um a três exemplos, cobrindo estrutura alterada, resposta vazia, conteúdo inválido e disjuntor (`REG-045` a `REG-047`, `REG-060`)
    - _Requisitos: 107.3, 107.7, 107.8_

- [ ] 32. Passo 14 de `D91` — Conector CAIXA como primeira implementação do contrato

  - [ ] 32.1 Implementar o conector da CAIXA
    - Criar `src/radar/conectores/caixa.py` como **primeira** implementação do contrato, com `conector_id`, versão e cobertura declarada — modalidades, UFs, cidades, tipos, campos entregues e não entregues
    - _Requisitos: 1.1, 1.2, 1.3, 85.4_

  - [ ] 32.2 Implementar o registro de captura imutável com identificador e versão do conector
    - Criar `src/radar/captura/registro_de_captura.py`: `conector_id`, `conector_versao` e versão da captura gravados em cada snapshot bruto
    - _Requisitos: 2.1, 85.6, 85.10_

  - [ ] 32.3 Implementar a captura rejeitada em `G0`
    - Criar `src/radar/captura/rejeicao.py`: payload reprovado em `G0` é registrado como captura `REJEITADA` com causa nomeada, **sem** criar oportunidade
    - _Requisitos: 2.6, 2.7, 4.1_

  - [ ] 32.4 Implementar a falha de obtenção que preserva a última captura válida
    - Criar `src/radar/conectores/falha_de_obtencao.py`: falha registra causa e a última captura válida permanece vigente
    - _Requisitos: 85.9, 107.9_

  - [ ] 32.5 Implementar a entrega dos arquivos ao Gestor de Documentos
    - Criar `src/radar/conectores/entrega_de_documentos.py`: os arquivos obtidos são entregues com **tipo declarado** e origem `CAPTURA_AUTOMATICA`
    - _Requisitos: 85.7, 86.4, 86.5_

  - [ ]* 32.6 Escrever a integração marcada do conector CAIXA
    - Criar `testes/integracao/test_conector_caixa.py` com `@pytest.mark.fonte_externa`, cobrindo cobertura declarada, obtenção de documentos e falha que preserva a última captura válida
    - _Requisitos: 85.4, 85.9_

- [ ] 33. Checkpoint — fecha o passo 14 de `D91`
  - Executar a suíte inteira, `ruff`, `mypy --strict`, `MT-11` e os testes marcados com `@pytest.mark.db`
  - Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 34. Passo 15 de `D91` — Radar automático pela segunda porta

  - [ ] 34.1 Implementar a porta do Radar automático
    - Criar `src/radar/radar/porta_automatica.py`: porta 2 de `R84`, convergindo para o **mesmo** estado, o mesmo pipeline, o mesmo catálogo de regras, os mesmos parâmetros e o mesmo `Motor_de_Decisao`
    - A porta é **proveniência**, nunca parâmetro de decisão
    - _Requisitos: 84.1, 84.5, 84.8, 84.9, 84.10_

  - [ ] 34.2 Implementar a Triagem Rápida como prefixo das fases 1 a 5
    - Criar `src/radar/pipeline/triagem.py` (componente 24): prefixo do **mesmo** pipeline, sem normalizador próprio, sem identidade própria e sem checklist próprio de decisão
    - A triagem **nunca** decide: não calcula valuation, custo econômico total, escore nem decisão, e não emite nenhum valor de `EstadoDeDecisao`
    - _Requisitos: 93.1, 93.2, 93.3, 93.4, 93.8, 93.11_

  - [ ] 34.3 Implementar o gate de promoção `G1-P` e a promoção manual
    - Criar `src/radar/pipeline/promocao.py`: o gate `G1-P` é **necessário** para a análise profunda; reprovar não é decisão de investimento e a oportunidade permanece disponível para reavaliação
    - Promoção manual registra autor, data e motivo como intervenção humana
    - _Requisitos: 93.5, 93.6, 93.7, 93.9, 93.10_

  - [ ] 34.4 Implementar o Motor do Radar e a Execução do Radar
    - Criar `src/radar/radar/motor.py` (componente 36): ciclo de **doze** etapas e Execução do Radar auditável de **quinze** campos, com as seis situações de `SituacaoDeExecucaoDoRadar`
    - A Execução do Radar **não decide**: nenhum `EstadoDeDecisao`, escore, valuation nem custo; uma execução por ciclo disparado
    - _Requisitos: 106.1, 106.2, 106.3, 106.4, 106.5, 106.6, 106.7, 106.8_

  - [ ] 34.5 Implementar a classificação incremental da oferta na fonte
    - Criar `src/radar/radar/classificacao_incremental.py` (componente 38): os **seis** estados de `EstadoDaOfertaNaFonte`, classificação total e captura incremental idempotente
    - Comparação inconclusiva **nunca** cria oferta nova; remoção na fonte registra `REMOVIDA_DA_FONTE` com data e hora e **não apaga** histórico
    - _Requisitos: 108.1, 108.2, 108.3, 108.5, 108.6, 108.7, 108.9_

  - [ ] 34.6 Implementar a chave de idempotência e as nove operações críticas
    - Criar `src/radar/plataforma/idempotencia.py` (componente 39): as **nove** operações críticas com garantia **de armazenamento**, não de disciplina do chamador
    - Repetição dentro da validade retorna o resultado da primeira execução; repetição após falha parcial completa o efeito faltante sem duplicar o já persistido
    - _Requisitos: 109.1, 109.2, 109.3, 109.4, 109.7_

  - [ ] 34.7 Implementar o Agendador configurável
    - Criar `src/radar/adaptadores/agendamento/local.py` e `nuvem.py` (componente 40, parte): os **dez** atributos de agendamento por fonte, exclusão mútua de execuções em curso para a mesma fonte, e alteração restrita ao Operador de Plataforma e registrada na trilha
    - _Requisitos: 110.1, 110.2, 110.3, 110.4, 110.5, 110.9, 110.10_

  - [ ]* 34.8 Escrever teste de propriedade para invariância de porta de entrada
    - **Property 154: Invariância de porta de entrada (`P17.5`)**
    - **Validates: Requirements 84.9, 93.8**
    - Arquivo `testes/propriedades/test_propriedade_154.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 154: Invariância de porta de entrada`, mínimo de 100 iterações

  - [ ]* 34.9 Escrever teste de propriedade para a triagem rápida nunca decide
    - **Property 162: A triagem rápida nunca decide (`P17.13`)**
    - **Validates: Requirements 93.2, 93.4**
    - Arquivo `testes/propriedades/test_propriedade_162.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 162: A triagem rápida nunca decide`, mínimo de 100 iterações

  - [ ]* 34.10 Escrever teste de propriedade para gate de promoção é necessário
    - **Property 163: Gate de promoção é necessário (`P17.14`)**
    - **Validates: Requirements 93.5, 93.6, 93.7**
    - Arquivo `testes/propriedades/test_propriedade_163.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 163: Gate de promoção é necessário`, mínimo de 100 iterações

  - [ ]* 34.11 Escrever teste de propriedade para a triagem é prefixo do mesmo pipeline
    - **Property 164: A triagem é prefixo do mesmo pipeline (`P17.15`)**
    - **Validates: Requirements 93.1, 93.8, 70.1**
    - Arquivo `testes/propriedades/test_propriedade_164.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 164: A triagem é prefixo do mesmo pipeline`, mínimo de 100 iterações

  - [ ]* 34.12 Escrever teste de propriedade para conservação das quantidades da execução
    - **Property 209: Conservação das quantidades da execução (`P20.1`)**
    - **Validates: Requirements 106.5, 108.2**
    - Arquivo `testes/propriedades/test_propriedade_209.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 209: Conservação das quantidades da execução`, mínimo de 100 iterações

  - [ ]* 34.13 Escrever teste de propriedade para uma execução por ciclo
    - **Property 210: Uma execução por ciclo (`P20.2`)**
    - **Validates: Requirements 106.7, 109.2**
    - Arquivo `testes/propriedades/test_propriedade_210.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 210: Uma execução por ciclo`, mínimo de 100 iterações

  - [ ]* 34.14 Escrever teste de propriedade para a execução do Radar nunca decide
    - **Property 211: A execução do Radar nunca decide (`P20.3`)**
    - **Validates: Requirements 106.6, 93.2**
    - Arquivo `testes/propriedades/test_propriedade_211.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 211: A execução do Radar nunca decide`, mínimo de 100 iterações

  - [ ]* 34.15 Escrever teste de propriedade para estratégia de captura invisível ao domínio
    - **Property 212: Estratégia de captura invisível ao domínio (`P20.4`)**
    - **Validates: Requirements 106.8, 85.3**
    - Arquivo `testes/propriedades/test_propriedade_212.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 212: Estratégia de captura invisível ao domínio`, mínimo de 100 iterações

  - [ ]* 34.16 Escrever teste de propriedade para totalidade da classificação incremental
    - **Property 219: Totalidade da classificação incremental (`P20.11`)**
    - **Validates: Requirements 108.2**
    - Arquivo `testes/propriedades/test_propriedade_219.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 219: Totalidade da classificação incremental`, mínimo de 100 iterações

  - [ ]* 34.17 Escrever teste de propriedade para idempotência da captura incremental
    - **Property 220: Idempotência da captura incremental (`P20.12`)**
    - **Validates: Requirements 108.3, 2.3**
    - Arquivo `testes/propriedades/test_propriedade_220.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 220: Idempotência da captura incremental`, mínimo de 100 iterações

  - [ ]* 34.18 Escrever teste de propriedade para remoção na fonte não apaga histórico
    - **Property 221: Remoção na fonte não apaga histórico (`P20.13`)**
    - **Validates: Requirements 108.5, 108.9**
    - Arquivo `testes/propriedades/test_propriedade_221.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 221: Remoção na fonte não apaga histórico`, mínimo de 100 iterações

  - [ ]* 34.19 Escrever teste de propriedade para comparação inconclusiva nunca cria oferta nova
    - **Property 222: Comparação inconclusiva nunca cria oferta nova (`P20.14`)**
    - **Validates: Requirements 108.7**
    - Arquivo `testes/propriedades/test_propriedade_222.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 222: Comparação inconclusiva nunca cria oferta nova`, mínimo de 100 iterações

  - [ ]* 34.20 Escrever teste de propriedade para idempotência das nove operações críticas
    - **Property 223: Idempotência das nove operações críticas (`P20.15`)**
    - **Validates: Requirements 109.1, 109.3**
    - Arquivo `testes/propriedades/test_propriedade_223.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 223: Idempotência das nove operações críticas`, mínimo de 100 iterações

  - [ ]* 34.21 Escrever teste de propriedade para retry completa sem duplicar
    - **Property 224: Retry completa sem duplicar (`P20.16`)**
    - **Validates: Requirements 109.4**
    - Arquivo `testes/propriedades/test_propriedade_224.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 224: Retry completa sem duplicar`, mínimo de 100 iterações

  - [ ]* 34.22 Escrever teste de propriedade para exclusão mútua de execuções
    - **Property 225: Exclusão mútua de execuções (`P20.17`)**
    - **Validates: Requirements 110.5**
    - Arquivo `testes/propriedades/test_propriedade_225.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 225: Exclusão mútua de execuções`, mínimo de 100 iterações

  - [ ]* 34.23 Escrever a integração da invariância entre as duas portas
    - Criar `testes/integracao/test_duas_portas.py` com `@pytest.mark.db`: mesma oportunidade pelas duas portas, mesmas evidências e mesmos parâmetros produzem mesma decisão, mesma camada determinante e mesma explicação (`REG-039`)
    - _Requisitos: 84.9, 93.8_

- [ ] 35. Checkpoint — fecha o passo 15 de `D91`
  - Executar a suíte inteira, `ruff`, `mypy --strict`, `MT-11` e os testes marcados com `@pytest.mark.db`
  - Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 36. Passo 16 de `D91` — Checklists parametrizáveis por escopo

  - [ ] 36.1 Implementar o Gestor de Checklist
    - Criar `src/radar/diligencia/checklist.py` (componente 25): catálogo de checklists **versionado**, com escopo por instituição, localização, tipo e estratégia, e a versão 1 do padrão contendo os **234** itens
    - _Requisitos: 92.1, 92.2, 92.3, 92.8, 92.9_

  - [ ] 36.2 Implementar os dois limites invioláveis validados na carga
    - Criar `src/radar/diligencia/limites_de_configuracao.py`: nenhuma configuração remove, desativa ou torna não aplicável item crítico da versão 1, e nenhuma torna o resultado na ausência de evidência mais favorável do que o devido na versão 1
    - Violação é rejeitada com `ErroDeConfiguracaoDeChecklist` (`REG-040`)
    - _Requisitos: 92.5, 92.6_

  - [ ] 36.3 Implementar a execução única por análise com cobertura apurada
    - Criar `src/radar/diligencia/execucao.py`: exatamente **uma** execução por análise, cobertura apurada e versão aplicada registrada, com cobertura verificável em **qualquer** versão configurada
    - _Requisitos: 92.4, 92.7, 92.10, 92.11_

  - [ ] 36.4 Implementar a pendência por documento exigido e por capacidade não declarada
    - Criar `src/radar/diligencia/pendencias_de_capacidade.py`: documento exigido e ausente abre pendência, e capacidade de fonte exigida por item de checklist e não declarada também
    - _Requisitos: 36.6, 37.4, 110.8_

  - [ ] 36.5 Implementar `MT-03` — cobertura de catálogo em qualquer versão
    - Criar `testes/meta/test_mt_03.py`: para toda `VersaoDeChecklist` ativa, todo item aplicável ao escopo resolvido tem resultado registrado; e a versão 1 declara `MC-001` a `MC-136`, `B-01` a `B-27` e `C-01` a `C-71` — 136 + 27 + 71 = **234**
    - _Requisitos: 73.3, 92.7_

  - [ ]* 36.6 Escrever teste de propriedade para cobertura total do catálogo de checklists em qualquer versão
    - **Property 144: Cobertura total do catálogo de checklists em qualquer versão (`P16.1`)**
    - **Validates: Requirements 36.5, 92.7**
    - Arquivo `testes/propriedades/test_propriedade_144.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 144: Cobertura total do catálogo de checklists em qualquer versão`, mínimo de 100 iterações

  - [ ]* 36.7 Escrever teste de propriedade para parametrização não enfraquece o checklist
    - **Property 165: Parametrização não enfraquece o checklist (`P17.16`)**
    - **Validates: Requirements 92.5, 92.6**
    - Arquivo `testes/propriedades/test_propriedade_165.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 165: Parametrização não enfraquece o checklist`, mínimo de 100 iterações

  - [ ]* 36.8 Escrever teste de propriedade para registro do checklist aplicado
    - **Property 166: Registro do checklist aplicado (`P17.17`)**
    - **Validates: Requirements 92.4, 92.10**
    - Arquivo `testes/propriedades/test_propriedade_166.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 166: Registro do checklist aplicado`, mínimo de 100 iterações

  - [ ]* 36.9 Escrever teste de propriedade para capacidade ausente gera pendência
    - **Property 226: Capacidade ausente gera pendência (`P20.18`)**
    - **Validates: Requirements 110.7, 110.8**
    - Arquivo `testes/propriedades/test_propriedade_226.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 226: Capacidade ausente gera pendência`, mínimo de 100 iterações

  - [ ]* 36.10 Escrever a integração marcada de checklist
    - Criar `testes/integracao/test_checklist.py` com `@pytest.mark.db`, cobrindo execução única por análise e resultado por item aplicável
    - _Requisitos: 92.4, 92.7_

- [ ] 37. Passo 17 de `D91` — Monitoramento e notificações

  - [ ] 37.1 Implementar o Monitor e a materialidade
    - Criar `src/radar/monitoramento/monitor.py` (componente 20, parte): monitoramento contínuo com os limiares de `MON-001` a `MON-017` comparados com `>=` — no limiar **exato**, dispara
    - Reavaliação é idempotente: reavaliar sem mudança de entrada não altera o estado
    - _Requisitos: 57.1, 57.2, 57.3, 57.6_

  - [ ] 37.2 Implementar reentrada e abandono de tese
    - Criar `src/radar/monitoramento/tese.py`: os **dez** estados de `EstadoDeMonitoramento`, com gatilho de reentrada, gatilho de abandono e histórico de transições
    - _Requisitos: 57.10, 57.10.1, 57.10.2_

  - [ ] 37.3 Implementar o Gestor de Alertas
    - Criar `src/radar/monitoramento/alertas.py`: o catálogo `ALT-001` a `ALT-020`, com impacto quantificado, consequência na tese, próxima ação, prioridade, agrupamento e silenciamento
    - _Requisitos: 58.1, 58.2, 58.3_

  - [ ] 37.4 Implementar o Gestor de Notificações com contrato único de canal
    - Criar `src/radar/monitoramento/notificacoes.py` (componente 48, parte) e `src/radar/adaptadores/notificacao/local.py`: **uma** notificação local por evento do catálogo, append-only
    - _Requisitos: 121.1, 121.2, 121.3, 121.9_

  - [ ] 37.5 Implementar o Gestor de Acompanhamento com os sete eixos
    - Criar `src/radar/monitoramento/acompanhamento.py` (componente 48, parte): os **sete** eixos, condição de encerramento e histórico preservado; acompanhamento dispara reavaliação
    - _Requisitos: 121.6, 121.7, 121.8_

  - [ ] 37.6 Implementar os eventos de domínio para os onze fatos
    - Criar `src/radar/plataforma/eventos.py` (componente 46, parte): os **onze** tipos, append-only, idempotentes por `(tipo, entidade_afetada, versao)` e com identificador do titular
    - Evento **não decide**: nenhuma decisão é emitida a partir do processamento de evento
    - _Requisitos: 117.1, 117.2, 117.3, 117.4_

  - [ ]* 37.7 Escrever teste de propriedade para limiar de materialidade dispara no valor exato
    - **Property 123: Limiar de materialidade dispara no valor exato (`P13.1`)**
    - **Validates: Requirements 57.2, 57.3**
    - Arquivo `testes/propriedades/test_propriedade_123.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 123: Limiar de materialidade dispara no valor exato`, mínimo de 100 iterações

  - [ ]* 37.8 Escrever teste de propriedade para idempotência da reavaliação
    - **Property 132: Idempotência da reavaliação (`P13.10`)**
    - **Validates: Requirements 57.6, 61.1**
    - Arquivo `testes/propriedades/test_propriedade_132.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 132: Idempotência da reavaliação`, mínimo de 100 iterações

  - [ ]* 37.9 Escrever teste de propriedade para idempotência do processamento de evento
    - **Property 241: Idempotência do processamento de evento (`P21.15`)**
    - **Validates: Requirements 117.3, 109.1**
    - Arquivo `testes/propriedades/test_propriedade_241.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 241: Idempotência do processamento de evento`, mínimo de 100 iterações

  - [ ]* 37.10 Escrever teste de propriedade para evento não decide
    - **Property 242: Evento não decide (`P21.16`)**
    - **Validates: Requirements 117.4**
    - Arquivo `testes/propriedades/test_propriedade_242.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 242: Evento não decide`, mínimo de 100 iterações

  - [ ]* 37.11 Escrever teste de propriedade para notificação por evento
    - **Property 249: Notificação por evento (`P21.23`)**
    - **Validates: Requirements 121.1, 121.9**
    - Arquivo `testes/propriedades/test_propriedade_249.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 249: Notificação por evento`, mínimo de 100 iterações

  - [ ]* 37.12 Escrever teste de propriedade para acompanhamento dispara reavaliação
    - **Property 250: Acompanhamento dispara reavaliação (`P21.24`)**
    - **Validates: Requirements 121.6, 121.7**
    - Arquivo `testes/propriedades/test_propriedade_250.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 250: Acompanhamento dispara reavaliação`, mínimo de 100 iterações

  - [ ]* 37.13 Escrever a integração de monitoramento e notificação
    - Criar `testes/integracao/test_monitoramento.py` com `@pytest.mark.db`, cobrindo disparo no limiar exato e notificação local por evento
    - _Requisitos: 57.2, 121.1_

- [ ] 38. Checkpoint — fecha o passo 17 de `D91`
  - Executar a suíte inteira, `ruff`, `mypy --strict`, `MT-11` e os testes marcados com `@pytest.mark.db`
  - Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 39. Passo 18 de `D91` — Observabilidade

  - [ ] 39.1 Implementar o Gestor de Observabilidade
    - Criar `src/radar/plataforma/observabilidade.py` (componente 41): identificador de correlação propagado, os **treze** atributos por execução relevante, log estruturado consultável por campo e retenção de `PLT-008`
    - **Nenhum segredo em log**: chave, credencial e token não aparecem em nenhum registro
    - _Requisitos: 111.1, 111.2, 111.3, 111.4, 111.5, 111.8, 111.9_

  - [ ] 39.2 Implementar a distinção entre evento automático e alteração manual
    - Criar `src/radar/plataforma/procedencia_de_evento.py`: todo erro é correlacionável, e evento automático e alteração manual são distinguíveis no registro
    - _Requisitos: 111.6, 111.7_

  - [ ] 39.3 Implementar `MT-15` — identificador de correlação em toda execução relevante
    - Criar `testes/meta/test_mt_15.py`: cada uma das treze espécies de execução relevante registra identificador de correlação e os treze atributos, falhando **nomeando a execução** sem identificador
    - _Requisitos: 111.3, 111.10_

  - [ ]* 39.4 Escrever teste de propriedade para identificador de correlação total
    - **Property 227: Identificador de correlação total (`P21.1`)**
    - **Validates: Requirements 111.1, 111.3**
    - Arquivo `testes/propriedades/test_propriedade_227.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 227: Identificador de correlação total`, mínimo de 100 iterações

  - [ ]* 39.5 Escrever teste de propriedade para log sem segredo
    - **Property 228: Log sem segredo (`P21.2`)**
    - **Validates: Requirements 111.5**
    - Arquivo `testes/propriedades/test_propriedade_228.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 228: Log sem segredo`, mínimo de 100 iterações

  - [ ]* 39.6 Escrever teste de propriedade para erro sempre correlacionável
    - **Property 229: Erro sempre correlacionável (`P21.3`)**
    - **Validates: Requirements 111.6, 111.7, 114.3**
    - Arquivo `testes/propriedades/test_propriedade_229.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 229: Erro sempre correlacionável`, mínimo de 100 iterações

  - [ ]* 39.7 Escrever a integração de observabilidade
    - Criar `testes/integracao/test_observabilidade.py` com `@pytest.mark.db`, cobrindo propagação do identificador de correlação de ponta a ponta e ausência de segredo em log
    - _Requisitos: 111.1, 111.5_

- [ ] 40. Passo 19 de `D91` — Endurecimento de segurança e desempenho

  - [ ] 40.1 Implementar o Gestor de Segurança
    - Criar `src/radar/plataforma/seguranca.py` (componente 42): autenticação, e autorização por **posse do recurso, titular do ator e papel exercido** em toda operação exposta
    - _Requisitos: 112.1, 112.2, 112.3_

  - [ ] 40.2 Implementar as quatro verificações de upload e a gravação por hash
    - Criar `src/radar/plataforma/upload.py`: extensão, tipo MIME, tamanho e nome do arquivo verificados; gravação por **hash**, nunca pelo nome enviado
    - Nome com travessia de caminho ou caminho absoluto é recusado com a causa informada, a tentativa é registrada e **nenhum** arquivo é gravado (`REG-053`)
    - _Requisitos: 112.4, 112.5, 112.6, 112.7, 112.8_

  - [ ] 40.3 Implementar a política de envio de documento a provedor
    - Criar `src/radar/plataforma/politica_de_provedor.py`: sem política registrada para a classe do documento e o provedor, o envio é recusado, a recusa é registrada com identificador de correlação, uma pendência é aberta e **nenhum** conteúdo é transmitido (`REG-052`)
    - _Requisitos: 112.10, 112.11, 112.12_

  - [ ] 40.4 Implementar o Executor Assíncrono
    - Criar `src/radar/plataforma/execucao_assincrona.py` (componente 45): os **oito** processamentos fora da requisição, com as seis situações de `SituacaoDeTrabalhoAssincrono`, progresso e `UNIQUE (tipo, chave_de_idempotencia)`
    - A situação do trabalho é total e monotônica
    - _Requisitos: 115.1, 115.2, 115.3, 115.4, 115.8_

  - [ ] 40.5 Implementar a conversão de operação síncrona que excede `PLT-009`
    - Criar `src/radar/plataforma/conversao_assincrona.py`: operação que excede o limite é convertida em trabalho assíncrono, com identificador devolvido ao chamador
    - _Requisitos: 115.6, 115.7_

  - [ ] 40.6 Concluir a configuração por ambiente e os sinalizadores de recurso
    - Criar `src/radar/plataforma/sinalizadores.py`: sinalizador por nome e ambiente, com autor e data da última alteração; nenhum sinalizador altera decisão, precedência, princípio inviolável ou parada absoluta
    - _Requisitos: 113.3, 113.4, 113.7, 113.8, 113.9_

  - [ ]* 40.7 Escrever teste de propriedade para upload sem travessia de caminho
    - **Property 230: Upload sem travessia de caminho (`P21.4`)**
    - **Validates: Requirements 112.5, 112.6**
    - Arquivo `testes/propriedades/test_propriedade_230.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 230: Upload sem travessia de caminho`, mínimo de 100 iterações

  - [ ]* 40.8 Escrever teste de propriedade para validação de upload é total
    - **Property 231: Validação de upload é total (`P21.5`)**
    - **Validates: Requirements 112.4, 112.7**
    - Arquivo `testes/propriedades/test_propriedade_231.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 231: Validação de upload é total`, mínimo de 100 iterações

  - [ ]* 40.9 Escrever teste de propriedade para política obrigatória antes do envio ao provedor
    - **Property 232: Política obrigatória antes do envio ao provedor (`P21.6`)**
    - **Validates: Requirements 112.10, 112.11**
    - Arquivo `testes/propriedades/test_propriedade_232.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 232: Política obrigatória antes do envio ao provedor`, mínimo de 100 iterações

  - [ ]* 40.10 Escrever teste de propriedade para autorização é necessária em toda operação exposta
    - **Property 233: Autorização é necessária em toda operação exposta (`P21.7`)**
    - **Validates: Requirements 112.1, 112.2**
    - Arquivo `testes/propriedades/test_propriedade_233.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 233: Autorização é necessária em toda operação exposta`, mínimo de 100 iterações

  - [ ]* 40.11 Escrever teste de propriedade para sinalizador de recurso não altera decisão
    - **Property 235: Sinalizador de recurso não altera decisão (`P21.9`)**
    - **Validates: Requirements 113.7, 113.8**
    - Arquivo `testes/propriedades/test_propriedade_235.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 235: Sinalizador de recurso não altera decisão`, mínimo de 100 iterações

  - [ ]* 40.12 Escrever teste de propriedade para conversão para assíncrono
    - **Property 237: Conversão para assíncrono (`P21.11`)**
    - **Validates: Requirements 115.6, 115.7**
    - Arquivo `testes/propriedades/test_propriedade_237.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 237: Conversão para assíncrono`, mínimo de 100 iterações

  - [ ]* 40.13 Escrever teste de propriedade para totalidade e monotonicidade da situação do trabalho
    - **Property 238: Totalidade e monotonicidade da situação do trabalho (`P21.12`)**
    - **Validates: Requirements 115.4**
    - Arquivo `testes/propriedades/test_propriedade_238.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 238: Totalidade e monotonicidade da situação do trabalho`, mínimo de 100 iterações

  - [ ]* 40.14 Escrever a integração de segurança e de desempenho
    - Criar `testes/integracao/test_seguranca.py` com `@pytest.mark.db`, cobrindo upload hostil, recusa de envio sem política e conversão para assíncrono
    - _Requisitos: 112.5, 112.11, 115.6_

- [ ] 41. Checkpoint — fecha o passo 19 de `D91`
  - Executar a suíte inteira, `ruff`, `mypy --strict`, `MT-11` e os testes marcados com `@pytest.mark.db`
  - Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 42. Passo 20 de `D91` — Golden Cases, regressão, validação final e portão de congelamento

  - [ ] 42.1 Implementar a trilha de auditoria append-only dos 22 tipos de evento
    - Criar `src/radar/governanca/auditoria.py` (componente 20, parte): os **22** tipos de evento com data, ator, papel, objeto, valor anterior, valor novo, motivo e identificador do titular, sem `UPDATE` nem `DELETE`
    - Registrar também a reexecução sem versionamento e as operações do contrato de programação
    - _Requisitos: 64.1, 64.2, 64.3, 64.4_

  - [ ] 42.2 Implementar as exceções auditáveis
    - Criar `src/radar/governanca/excecoes.py`: `EXC-001` a `EXC-009` com valor normal, valor excepcional, risco aceito, justificativa, evidência, alçada, prazo e impacto no escore
    - Exceção sobre bloqueio crítico é **rejeitada**; expiração da exceção **restaura** a regra
    - _Requisitos: 63.1, 63.4, 63.4.1, 63.5_

  - [ ] 42.3 Implementar as invariantes de `R73` e o controle de escopo de `R75`
    - Criar `src/radar/governanca/invariantes.py`: as invariantes declaradas como verificações executáveis, com a lista de fatos que invalidariam cada resultado publicado
    - _Requisitos: 73.1, 73.6, 73.9, 75.3, 75.5_

  - [ ] 42.4 Implementar `MT-01` — rastreabilidade das 262 propriedades
    - Criar `testes/meta/test_mt_01.py`: o conjunto de identificadores `P1.1` a `P22.12` do requirements é igual ao conjunto dos identificadores de origem das **262** propriedades do design, com a única exceção declarada de `P7.12`, e todo requisito citado em `Validates` existe no intervalo de 1 a **126**
    - _Requisitos: 73.1, 73.10_

  - [ ] 42.5 Implementar `MT-02` — um teste por propriedade
    - Criar `testes/meta/test_mt_02.py`: cada uma das **262** propriedades tem exatamente **um** teste com a etiqueta `Property {n}`, falhando por propriedade sem teste ou por dois testes para a mesma
    - _Requisitos: 73.2, 73.10_

  - [ ] 42.6 Implementar `MT-06` — cobertura de prioridade dos 126 requisitos
    - Criar `testes/meta/test_mt_06.py`: os **126** requisitos têm exatamente uma prioridade, com as contagens **112 `P0`**, **13 `P1`** e **1 `P2`**, e o resumo do Índice de Requisitos coincidindo com a tabulação linha a linha
    - _Requisitos: 73.10, 75.5_

  - [ ] 42.7 Implementar `MT-12` — cobertura das quarenta perguntas de fechamento
    - Criar `testes/meta/test_mt_12.py`: cada um dos critérios `R126.1` a `R126.40` possui requisito numerado que o satisfaça, e todo identificador citado existe; falha **nomeando a pergunta órfã**
    - _Requisitos: 126.41, 126.42_

  - [ ] 42.8 Implementar o Golden Case `F.1` — oráculo econômico
    - Criar `testes/golden/test_golden_f1.py` com tolerância declarada e os números publicados, que **não mudam**: reserva R$ 11.153,345085; carregamento R$ 1.905,00; **custo econômico total R$ 236.125,246785**; desconto líquido 0,1857750 → **18,5775%**; margem absoluta R$ 53.874,753215; base de imposto na venda R$ 45.874,753215; venda líquida R$ 275.118,78701775; lucro líquido R$ 38.993,54023275; ROI líquido 0,1651392 → **16,5139%**; ROI anualizado 0,8429404 → **84,2940%**; break-even de saída **R$ 251.197,07105**; distância do break-even 0,3107 sem acionar `MONITORAR`; aluguel líquido R$ 1.170,00; base de imposto sobre aluguel R$ 1.265,00; yield bruto mensal 0,0080466; yield líquido mensal 0,0049550; **preço máximo por ROI alvo R$ 182.158,03**; verificação inversa 0,250000 com erro < 10⁻⁶; teto conservador informativo R$ 168.374,76; veredito revenda `NAO_COMPRAR` na camada 4 e veredito renda `NAO_COMPRAR` na camada 5
    - Os mesmos números são o oráculo da visão financeira oficial: os **treze** componentes decompostos somam exatamente o custo econômico total publicado, e cada componente é navegável até a evidência
    - Declarar a lista de fatos que invalidariam o resultado
    - _Requisitos: 26.1, 27.3, 27.12, 28.2, 30.3.1, 65.6, 73.1_

  - [ ] 42.9 Implementar o Golden Case `F.2`
    - Criar `testes/golden/test_golden_f2.py`: averbação `EM_TRATAMENTO` como pendência registral **sem** `BLOQUEIO` (`REG-003`), com a lista de fatos que invalidariam o resultado
    - _Requisitos: 12.6, 13.13, 65.6_

  - [ ] 42.10 Implementar o Golden Case `F.3`
    - Criar `testes/golden/test_golden_f3.py`: cadeia registral recente como evidência forte que **não** comprova regularidade das notificações (`REG-002`), com o segundo leilão a 60% da avaliação **não** acionando `RULE-JUR-011`
    - _Requisitos: 13.1, 14.1, 65.6_

  - [ ] 42.11 Implementar o Golden Case `F.4`
    - Criar `testes/golden/test_golden_f4.py`: leitura do texto do ato registral, gravame histórico baixado e valuation independente da avaliação da fonte (`REG-002`, `REG-009`)
    - _Requisitos: 3.10, 12.1, 21.8, 65.6_

  - [ ] 42.12 Implementar os testes de regressão `REG-001` a `REG-012`
    - Criar `testes/regressao/test_reg_001_a_012.py`, **um teste por linha** do Anexo E, nomeado pelo identificador
    - _Requisitos: 73.8_

  - [ ] 42.13 Implementar os testes de regressão `REG-013` a `REG-024`
    - Criar `testes/regressao/test_reg_013_a_024.py`, um teste por linha do Anexo E
    - _Requisitos: 73.8_

  - [ ] 42.14 Implementar os testes de regressão `REG-025` a `REG-036`
    - Criar `testes/regressao/test_reg_025_a_036.py`, um teste por linha do Anexo E, incluindo `NAO_APLICAVEL` distinto de `DESCONHECIDO`, matrícula duplicada, reprocessamento de captura, idempotência de esquema e `422` em lugar de `500`
    - _Requisitos: 73.8_

  - [ ] 42.15 Implementar os testes de regressão `REG-037` a `REG-048`
    - Criar `testes/regressao/test_reg_037_a_048.py`, um teste por linha do Anexo E, cobrindo os cenários do Domínio O e o início dos Domínios P a T
    - _Requisitos: 73.8_

  - [ ] 42.16 Implementar os testes de regressão `REG-049` a `REG-060`
    - Criar `testes/regressao/test_reg_049_a_060.py`, um teste por linha do Anexo E, fechando os cenários dos Domínios P a T
    - _Requisitos: 73.8_

  - [ ] 42.17 Implementar o ciclo de prova do MVP como teste de integração único de dezoito passos, nas duas portas
    - Criar `testes/integracao/test_ciclo_de_prova.py` com `@pytest.mark.db`: **um único** teste percorrendo os **dezoito** passos na ordem, do passo 1 (criar imóvel) ao passo 18 (revisitar o imóvel posteriormente), sobre banco real e documentos reais
    - Fechar o ciclo `DESCOBRIR` → `SELECIONAR` → `DOCUMENTAR` → `ANALISAR` → `COMPLEMENTAR` → `REANALISAR` → `COMPARAR` → `DECIDIR` nas **duas** portas de entrada, executando os passos 3 a 18 a partir de candidato promovido sem alteração de motor, regra ou parâmetro
    - Verificar os sete atributos de `R95.5` e a preservação de todas as versões de análise, documentos, versões de documento e evidências; passo não executável faz o teste falhar **identificando o passo e o requisito**, sem resultado parcial
    - _Requisitos: 95.1, 95.2, 95.3, 95.4, 95.5, 95.6, 95.7_

  - [ ] 42.18 Implementar o portão de congelamento de `R126`
    - Criar `testes/congelamento/test_portao_de_congelamento.py`: as **quarenta** perguntas de fechamento respondidas por requisito numerado, com `MT-06`, `MT-12` e a suíte de regressão completa como sequência de validação
    - Registrar o congelamento com data, versão do documento e as contagens de requisitos, decisões, propriedades e testes de regressão; depois dele, mudança de arquitetura exige decisão numerada com conflito, resolução e impacto documentados, e mudança sem decisão registrada **não é admitida**
    - _Requisitos: 126.41, 126.42, 126.43, 126.44, 126.45, 126.46_

  - [ ]* 42.19 Escrever teste de propriedade para trilha de auditoria é append-only
    - **Property 129: Trilha de auditoria é append-only (`P13.7`)**
    - **Validates: Requirements 64.1, 64.3**
    - Arquivo `testes/propriedades/test_propriedade_129.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 129: Trilha de auditoria é append-only`, mínimo de 100 iterações

  - [ ]* 42.20 Escrever teste de propriedade para expiração de exceção restaura a regra
    - **Property 131: Expiração de exceção restaura a regra (`P13.9`)**
    - **Validates: Requirements 63.5**
    - Arquivo `testes/propriedades/test_propriedade_131.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 131: Expiração de exceção restaura a regra`, mínimo de 100 iterações

  - [ ]* 42.21 Escrever teste de propriedade para cobertura de prioridade dos requisitos
    - **Property 145: Cobertura de prioridade dos requisitos (`P16.2`)**
    - **Validates: Requirements 75.5**
    - Arquivo `testes/propriedades/test_propriedade_145.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 145: Cobertura de prioridade dos requisitos`, mínimo de 100 iterações

  - [ ]* 42.22 Escrever teste de propriedade para cobertura dos dezoito passos do ciclo de prova
    - **Property 171: Cobertura dos dezoito passos do ciclo de prova (`P17.22`)**
    - **Validates: Requirements 95.1, 95.2, 95.6**
    - Arquivo `testes/propriedades/test_propriedade_171.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 171: Cobertura dos dezoito passos do ciclo de prova`, mínimo de 100 iterações

  - [ ]* 42.23 Escrever teste de propriedade para fechamento total
    - **Property 262: Fechamento total (`P22.12`)**
    - **Validates: Requirements 126.41, 126.42**
    - Arquivo `testes/propriedades/test_propriedade_262.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 262: Fechamento total`, mínimo de 100 iterações

  - [ ]* 42.24 Escrever a execução consolidada da suíte de regressão marcada
    - Criar `testes/regressao/test_suite_completa.py` habilitando `@pytest.mark.db`, `@pytest.mark.fonte_externa` e `@pytest.mark.provedor_de_modelo` e reexecutando os **60** testes com os perfis `ci` e `regressao`
    - _Requisitos: 73.8, 73.10_

- [ ] 43. Checkpoint — fecha o passo 20 de `D91`
  - Executar a suíte inteira, `ruff`, `mypy --strict`, os **16 meta-testes**, as **262 propriedades**, os **60 testes de regressão**, os **4 Golden Cases**, a suíte de avaliação de IA e os testes marcados com `@pytest.mark.db`, `@pytest.mark.fonte_externa` e `@pytest.mark.provedor_de_modelo`
  - Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 44. Requisitos `P1` — os treze, depois de todos os `P0`

  - [ ] 44.1 Implementar o enriquecimento progressivo (`R5`)
    - Criar `src/radar/pipeline/enriquecimento.py`: profundidade derivada do **potencial preliminar** em cinco faixas qualitativas e da posição no ranqueamento, nunca do `EscoreDeOportunidade` — derivar dele criaria dependência circular
    - _Requisitos: 5.1, 5.2, 5.7_

  - [ ] 44.2 Implementar o financiamento (`R31`)
    - Criar `src/radar/motores/financiamento.py`: custo financeiro como componente do custo econômico total, com prazo e taxa declarados
    - _Requisitos: 31.1, 31.2, 31.3_

  - [ ] 44.3 Implementar estratégias de saída e operações híbridas (`R42`, `R43`)
    - Criar `src/radar/motores/saida.py`: estratégias de saída, operações híbridas e monitoramento de liquidez
    - _Requisitos: 42.1, 42.2, 43.1, 43.2_

  - [ ] 44.4 Implementar a simulação de alocação antes da decisão (`R48`)
    - Criar `src/radar/motores/alocacao.py`: simulação de alocação do portfólio antes da decisão, sem alterar a precedência de decisão
    - _Requisitos: 48.1, 48.2, 48.3_

  - [ ] 44.5 Implementar os alertas acionáveis (`R59`)
    - Criar `src/radar/monitoramento/alertas_acionaveis.py`: próxima ação objetiva por alerta, com impacto quantificado
    - _Requisitos: 59.1, 59.2, 59.3_

  - [ ] 44.6 Implementar resultado real e backtest com coortes (`R60`)
    - Criar `src/radar/backtest/motor.py`: os nove campos de resultado real, coortes e controle de sobreajuste, com o acesso a dados filtrado pela data da decisão — antiviés temporal de `SAFE-015`
    - _Requisitos: 60.1, 60.3, 60.3.1, 60.4, 60.5_

  - [ ] 44.7 Implementar o controle de qualidade das regras e a qualidade de evidência (`R65`)
    - Criar `src/radar/governanca/qualidade.py`: `QualidadeDaEvidencia` aplicada, indicadores de aprendizado e a lista de fatos que invalidariam cada resultado publicado
    - _Requisitos: 65.1, 65.1.1, 65.6_

  - [ ] 44.8 Implementar os relatórios de negócio (`R69`)
    - Criar `src/radar/apresentacao/relatorios.py`, verificados por instantâneo de **estrutura**, não de redação
    - _Requisitos: 69.1, 69.2, 69.3_

  - [ ] 44.9 Implementar alocação, eficiência de capital e faixas de ação (`R80`, `R81`)
    - Criar `src/radar/motores/eficiencia_de_capital.py`: eficiência de capital e as faixas de ação de `PORT-007`
    - _Requisitos: 80.1, 80.2, 81.1, 81.2_

  - [ ] 44.10 Implementar o evento de domínio como mecanismo de desacoplamento (`R117.5`)
    - Criar `src/radar/plataforma/eventos_desacoplados.py`: uso de evento como substituto de chamada direta **onde a ordem não é exigida**, preservando a idempotência e a abstenção de decisão
    - _Requisitos: 117.5, 117.6_

  - [ ] 44.11 Implementar a notificação por canal externo (`R121.4`)
    - Criar `src/radar/adaptadores/notificacao/externo.py`: entrega por canal externo sobre o mesmo contrato `CanalDeNotificacao`, sem alterar o catálogo de eventos nem a notificação local
    - _Requisitos: 121.4, 121.5_

  - [ ]* 44.12 Escrever teste de propriedade para antiviés temporal no backtest
    - **Property 128: Antiviés temporal no backtest (`P13.6`)**
    - **Validates: Requirements 60.4, 60.5**
    - Arquivo `testes/propriedades/test_propriedade_128.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 128: Antiviés temporal no backtest`, mínimo de 100 iterações

  - [ ]* 44.13 Escrever os testes dos requisitos `P1`
    - Criar `testes/integracao/test_requisitos_p1.py` com `@pytest.mark.db`, reexecutando os 60 testes de regressão e os 16 meta-testes como pré-condição de entrada
    - _Requisitos: 60.1, 65.1, 121.4_

- [ ] 45. Requisito `P2` — esteira de conhecimento e RAG (`R72`)

  - [ ] 45.1 Implementar a ingestão da base de conhecimento
    - Criar `src/radar/conhecimento/ingestao.py`: os **quinze** tipos de `TipoDeSegmentoDeConhecimento`, com `texto_fonte` e `parafrase` **separados** e os vinte metadados obrigatórios por segmento
    - Reingestão é idempotente por `(extracao_id, indice_do_segmento)`
    - _Requisitos: 72.1, 72.2, 72.3, 72.3.1, 72.3.2, 72.4_

  - [ ] 45.2 Implementar o conhecimento normativo com fonte e proveniência
    - Criar `src/radar/conhecimento/normativo.py`: regra jurídica exige fonte e proveniência declaradas, e texto-fonte e paráfrase permanecem distinguíveis
    - _Requisitos: 72.5, 72.6_

  - [ ] 45.3 Implementar as três camadas de memória
    - Criar `src/radar/conhecimento/memoria.py`: memória histórica é **sempre hipótese** e nunca atravessa a fronteira como regra vigente
    - _Requisitos: 72.7, 72.8, 72.9_

  - [ ] 45.4 Reconstruir o índice vetorial após a carga
    - Criar `scripts/reconstruir_indice_vetorial.py`: o índice é criado ou reconstruído **depois** da ingestão, com `lists` dimensionado pelo volume real
    - _Requisitos: 72.1, 102.2_

  - [ ]* 45.5 Escrever teste de propriedade para metadados obrigatórios em todo segmento
    - **Property 140: Metadados obrigatórios em todo segmento (`P15.1`)**
    - **Validates: Requirements 72.3, 72.4**
    - Arquivo `testes/propriedades/test_propriedade_140.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 140: Metadados obrigatórios em todo segmento`, mínimo de 100 iterações

  - [ ]* 45.6 Escrever teste de propriedade para regra jurídica exige fonte e proveniência
    - **Property 141: Regra jurídica exige fonte e proveniência (`P15.2`)**
    - **Validates: Requirements 72.5**
    - Arquivo `testes/propriedades/test_propriedade_141.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 141: Regra jurídica exige fonte e proveniência`, mínimo de 100 iterações

  - [ ]* 45.7 Escrever teste de propriedade para idempotência da reingestão
    - **Property 142: Idempotência da reingestão (`P15.3`)**
    - **Validates: Requirements 72.1**
    - Arquivo `testes/propriedades/test_propriedade_142.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 142: Idempotência da reingestão`, mínimo de 100 iterações

  - [ ]* 45.8 Escrever teste de propriedade para memória histórica é sempre hipótese
    - **Property 143: Memória histórica é sempre hipótese (`P15.4`)**
    - **Validates: Requirements 72.9**
    - Arquivo `testes/propriedades/test_propriedade_143.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 143: Memória histórica é sempre hipótese`, mínimo de 100 iterações

  - [ ]* 45.9 Escrever teste de propriedade para texto-fonte e paráfrase permanecem distinguíveis
    - **Property 149: Texto-fonte e paráfrase permanecem distinguíveis (`P16.6`)**
    - **Validates: Requirements 72.3.1, 72.3.2**
    - Arquivo `testes/propriedades/test_propriedade_149.py`, etiqueta `Feature: radar-imobiliario-especificacao-completa, Property 149: Texto-fonte e paráfrase permanecem distinguíveis`, mínimo de 100 iterações

  - [ ]* 45.10 Escrever a integração da esteira de conhecimento
    - Criar `testes/integracao/test_esteira_de_conhecimento.py` com `@pytest.mark.db`, cobrindo idempotência da reingestão e separação entre texto-fonte e paráfrase
    - _Requisitos: 72.1, 72.3.1_

- [ ] 46. Checkpoint final — barreira completa
  - Executar **tudo**: a suíte inteira, `ruff`, `mypy --strict`, `MT-11`, os **16 meta-testes** `MT-01` a `MT-16`, as **262 propriedades** com o perfil `ci`, os **60 testes de regressão** `REG-001` a `REG-060`, os **4 Golden Cases** dos Anexos E e F, a suíte de avaliação de IA com as nove verificações, os testes marcados com `@pytest.mark.db`, `@pytest.mark.fonte_externa` e `@pytest.mark.provedor_de_modelo`, o ciclo de prova de `R95` nas **duas portas** e o **portão de congelamento** de `R126`
  - Registrar as verificações manuais de acessibilidade com o resultado declarado; nenhuma delas é reportada como satisfeita por inferência
  - Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

## Notes

- Sub-tarefas marcadas com `*` são **de teste** e podem ser adiadas sem bloquear a construção.
  **Nenhuma tarefa de topo é opcional.** As verificações que são contrato do produto — os 16
  meta-testes, os 60 testes de regressão, os 4 Golden Cases, o ciclo de prova de `R95`, a suíte de
  avaliação de IA e o portão de congelamento de `R126` — **não** são marcadas com `*`: elas são o
  entregável do passo 20, não teste adiável.
- Cada uma das **262 propriedades** tem **exatamente uma** tarefa de teste, em **arquivo próprio**
  `testes/propriedades/test_propriedade_NNN.py`, com a etiqueta
  `Feature: radar-imobiliario-especificacao-completa, Property {n}: {texto}` e no mínimo 100
  iterações. É o arquivo por propriedade que torna essas tarefas independentes e paralelizáveis, e
  é `MT-02` que verifica a correspondência de um para um.
- `P7.12` **não** é propriedade: é **contraexemplo dirigido** de entradas fixas, com os dois números
  publicados e a diferença verificada, e é a única exceção declarada de `MT-01`. Ele entra como
  teste dirigido no bloco `1.6`, não como tarefa de propriedade.
- **Correspondência entre as tarefas de topo e os vinte passos de `D91`:** passo 1 → tarefas 1 e 2
  (blocos `1.1` e `1.1-A`); passo 2 → tarefas 4 a 12 (blocos `1.2` a `1.10`); passo 3 → 14;
  passo 4 → 16; passo 5 → 18; passo 6 → 20; passo 7 → 22; passo 8 → 23; passo 9 → 25;
  passo 10 → 26; passo 11 → 28; passo 12 → 29; passo 13 → 31; passo 14 → 32; passo 15 → 34;
  passo 16 → 36; passo 17 → 37; passo 18 → 39; passo 19 → 40; passo 20 → 42. As tarefas 44 e 45
  são os **13 requisitos `P1`** e o **único `P2`**, que vêm depois de todos os `P0` e reexecutam a
  barreira integralmente. As demais tarefas de topo são **checkpoints**.
- **Ordem de construção e prioridade de requisito são dimensões distintas.** Um `P0` construído no
  passo 18 continua `P0`. O **preparo estrutural** é exceção deliberada e vem nos passos 1 a 3,
  porque retroajustá-lo depois das 63 entidades gravadas é migração (`D96`, `R118.9`).
- **O primeiro marco funcional fecha no checkpoint da tarefa 24, ao fim do passo 8**: análise manual
  real de um imóvel da CAIXA, do documento à decisão apresentada na interface. E **a construção não
  começa pelo coletor**: framework de conector, conector CAIXA e Radar são os passos 13 a 15.
- **A renomeação de `D72` acontece em quatro lugares:** módulos de domínio e motores na tarefa 4.1
  (passo 2); esquema por **migração versionada** na tarefa 14.16 (passo 3); nomes de recurso, campo
  e valor de domínio no contrato de programação na tarefa 22.8 (passo 7); e interface integralmente
  em português na tarefa 23 (passo 8). `MT-11` entra na barreira de integração na tarefa 1.7,
  **desde o passo 1**, e cobre também as correspondências obrigatórias de `D103`.
- **O que cada checkpoint executa.** Todo checkpoint executa a suíte inteira, `ruff`,
  `mypy --strict` e `MT-11`; a partir do checkpoint que fecha o passo 3 — quando a persistência
  existe — executa também os testes marcados com `@pytest.mark.db`. O checkpoint que fecha o passo
  20 acrescenta os 16 meta-testes, as 262 propriedades, os 60 testes de regressão, os 4 Golden
  Cases, a suíte de avaliação de IA e as três marcas de dependência externa. O **checkpoint final**
  executa tudo isso mais o ciclo de prova de `R95` nas duas portas e o portão de congelamento de
  `R126`.
- **As três marcas de dependência externa** — `@pytest.mark.db`, `@pytest.mark.fonte_externa` e
  `@pytest.mark.provedor_de_modelo` — são declaradas na tarefa 1.8 e ficam **desabilitadas por
  default**. A consequência é verificável: as 262 propriedades rodam em qualquer máquina, sem banco,
  sem rede e sem crédito de provedor. Provedor de modelo e de embedding entram nas propriedades
  apenas por dublê.
- **Acessibilidade tem duas metades distintas.** O que é automatizável é verificado por propriedade
  sobre declaração e renderização (`P22.1` a `P22.11`) e pelo contraste calculável do
  `DesignSystem`. O que **não** é automatizável — leitura por leitor de tela, navegação por voz, uso
  com ampliador, percepção de contraste em condição real e uso com uma das mãos — é declarado na
  tarefa 23.9 como registro executável com roteiro próprio, e **nenhuma dessas verificações é
  reportada como satisfeita por inferência**: o verde da suíte não é lido como acessibilidade
  comprovada.
- **A suíte de avaliação de IA é separada da suíte de propriedades** e uma não substitui a outra. Ela
  vive em `testes/avaliacao_de_ia/`, com barreira própria e as nove verificações de `R105.8`, e não
  é contada entre as 262 propriedades.
- **Os artefatos de arquitetura derivados não são fonte de nenhuma tarefa.** Nenhuma tarefa deste
  plano depende de ler `architecture/**` ou qualquer outro documento fora desta spec: o
  `requirements.md` é a única fonte normativa de negócio e o `design.md` é a única fonte normativa
  de engenharia.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8"] },
    { "id": 1, "tasks": ["1.9"] },
    { "id": 2, "tasks": ["2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9", "2.10"] },
    { "id": 3, "tasks": ["2.11", "2.12", "2.13", "2.14", "2.15", "2.16"] },
    { "id": 4, "tasks": ["3"] },
    { "id": 5, "tasks": ["4.1", "4.2", "4.3", "4.4"] },
    { "id": 6, "tasks": ["4.5", "4.6", "4.7", "4.8", "4.9", "4.10", "4.11", "4.12"] },
    { "id": 7, "tasks": ["5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7", "5.8", "5.9"] },
    { "id": 8, "tasks": ["5.10", "5.11", "5.12", "5.13", "5.14", "5.15", "5.16", "5.17", "5.18", "5.19", "5.20", "5.21", "5.22", "5.23", "5.24", "5.25", "5.26", "5.27", "5.28", "5.29", "5.30", "5.31", "5.32", "5.33"] },
    { "id": 9, "tasks": ["6.1", "6.2", "6.3", "6.4", "6.5", "6.6", "6.7"] },
    { "id": 10, "tasks": ["6.8", "6.9", "6.10", "6.11", "6.12", "6.13", "6.14", "6.15", "6.16", "6.17", "6.18", "6.19", "6.20", "6.21"] },
    { "id": 11, "tasks": ["7.1", "7.2", "7.3", "7.4"] },
    { "id": 12, "tasks": ["7.5", "7.6", "7.7", "7.8", "7.9", "7.10", "7.11", "7.12", "7.13", "7.14", "7.15", "7.16", "7.17", "7.18", "7.19", "7.20"] },
    { "id": 13, "tasks": ["8.1", "8.2", "8.3", "8.4", "8.5"] },
    { "id": 14, "tasks": ["8.6", "8.7", "8.8", "8.9", "8.10", "8.11", "8.12", "8.13", "8.14", "8.15", "8.16", "8.17", "8.18", "8.19", "8.20", "8.21", "8.22", "8.23", "8.24", "8.25", "8.26", "8.27", "8.28", "8.29", "8.30", "8.31", "8.32"] },
    { "id": 15, "tasks": ["9.1", "9.2", "9.3", "9.4", "9.5", "9.6", "9.7"] },
    { "id": 16, "tasks": ["9.8", "9.9", "9.10", "9.11", "9.12", "9.13", "9.14", "9.15", "9.16", "9.17", "9.18", "9.19", "9.20", "9.21", "9.22", "9.23", "9.24", "9.25", "9.26", "9.27", "9.28", "9.29", "9.30", "9.31", "9.32", "9.33", "9.34", "9.35", "9.36", "9.37", "9.38"] },
    { "id": 17, "tasks": ["10.1", "10.2", "10.3", "10.4", "10.5"] },
    { "id": 18, "tasks": ["10.6", "10.7", "10.8", "10.9", "10.10", "10.11", "10.12", "10.13", "10.14", "10.15", "10.16", "10.17", "10.18", "10.19", "10.20", "10.21", "10.22", "10.23", "10.24", "10.25"] },
    { "id": 19, "tasks": ["11.1", "11.2", "11.3", "11.4", "11.5", "11.6"] },
    { "id": 20, "tasks": ["11.7", "11.8", "11.9", "11.10", "11.11", "11.12", "11.13", "11.14"] },
    { "id": 21, "tasks": ["12.1", "12.2", "12.3", "12.4", "12.5", "12.6"] },
    { "id": 22, "tasks": ["12.7", "12.8", "12.9", "12.10", "12.11", "12.12", "12.13"] },
    { "id": 23, "tasks": ["13"] },
    { "id": 24, "tasks": ["14.1", "14.2", "14.3", "14.4", "14.5", "14.6", "14.7", "14.8", "14.9", "14.10", "14.11", "14.12", "14.13", "14.14", "14.15", "14.16"] },
    { "id": 25, "tasks": ["14.17", "14.18", "14.19", "14.20", "14.21", "14.22", "14.23"] },
    { "id": 26, "tasks": ["15"] },
    { "id": 27, "tasks": ["16.1", "16.2", "16.3", "16.4", "16.5", "16.6", "16.7"] },
    { "id": 28, "tasks": ["16.8", "16.9", "16.10", "16.11", "16.12", "16.13", "16.14", "16.15"] },
    { "id": 29, "tasks": ["17"] },
    { "id": 30, "tasks": ["18.1", "18.2", "18.3", "18.4"] },
    { "id": 31, "tasks": ["18.5"] },
    { "id": 32, "tasks": ["19"] },
    { "id": 33, "tasks": ["20.1", "20.2", "20.3", "20.4", "20.5"] },
    { "id": 34, "tasks": ["20.6", "20.7", "20.8", "20.9", "20.10", "20.11", "20.12", "20.13", "20.14", "20.15", "20.16", "20.17"] },
    { "id": 35, "tasks": ["21"] },
    { "id": 36, "tasks": ["22.1", "22.2", "22.3", "22.4", "22.5", "22.6", "22.7", "22.8"] },
    { "id": 37, "tasks": ["22.9", "22.10", "22.11"] },
    { "id": 38, "tasks": ["23.1", "23.2", "23.3", "23.4", "23.5", "23.6", "23.7", "23.8", "23.9", "23.10"] },
    { "id": 39, "tasks": ["23.11", "23.12", "23.13", "23.14", "23.15", "23.16", "23.17", "23.18", "23.19", "23.20", "23.21", "23.22"] },
    { "id": 40, "tasks": ["24"] },
    { "id": 41, "tasks": ["25.1", "25.2", "25.3", "25.4", "25.5", "25.6", "25.7"] },
    { "id": 42, "tasks": ["25.8", "25.9", "25.10", "25.11", "25.12", "25.13", "25.14", "25.15"] },
    { "id": 43, "tasks": ["26.1", "26.2", "26.3", "26.4", "26.5", "26.6", "26.7"] },
    { "id": 44, "tasks": ["26.8", "26.9", "26.10", "26.11", "26.12", "26.13", "26.14"] },
    { "id": 45, "tasks": ["27"] },
    { "id": 46, "tasks": ["28.1", "28.2", "28.3", "28.4", "28.5"] },
    { "id": 47, "tasks": ["28.6", "28.7", "28.8"] },
    { "id": 48, "tasks": ["29.1", "29.2", "29.3", "29.4", "29.5"] },
    { "id": 49, "tasks": ["29.6", "29.7", "29.8", "29.9", "29.10", "29.11", "29.12"] },
    { "id": 50, "tasks": ["30"] },
    { "id": 51, "tasks": ["31.1", "31.2", "31.3", "31.4", "31.5"] },
    { "id": 52, "tasks": ["31.6", "31.7", "31.8", "31.9", "31.10", "31.11", "31.12", "31.13"] },
    { "id": 53, "tasks": ["32.1", "32.2", "32.3", "32.4", "32.5"] },
    { "id": 54, "tasks": ["32.6"] },
    { "id": 55, "tasks": ["33"] },
    { "id": 56, "tasks": ["34.1", "34.2", "34.3", "34.4", "34.5", "34.6", "34.7"] },
    { "id": 57, "tasks": ["34.8", "34.9", "34.10", "34.11", "34.12", "34.13", "34.14", "34.15", "34.16", "34.17", "34.18", "34.19", "34.20", "34.21", "34.22", "34.23"] },
    { "id": 58, "tasks": ["35"] },
    { "id": 59, "tasks": ["36.1", "36.2", "36.3", "36.4", "36.5"] },
    { "id": 60, "tasks": ["36.6", "36.7", "36.8", "36.9", "36.10"] },
    { "id": 61, "tasks": ["37.1", "37.2", "37.3", "37.4", "37.5", "37.6"] },
    { "id": 62, "tasks": ["37.7", "37.8", "37.9", "37.10", "37.11", "37.12", "37.13"] },
    { "id": 63, "tasks": ["38"] },
    { "id": 64, "tasks": ["39.1", "39.2", "39.3"] },
    { "id": 65, "tasks": ["39.4", "39.5", "39.6", "39.7"] },
    { "id": 66, "tasks": ["40.1", "40.2", "40.3", "40.4", "40.5", "40.6"] },
    { "id": 67, "tasks": ["40.7", "40.8", "40.9", "40.10", "40.11", "40.12", "40.13", "40.14"] },
    { "id": 68, "tasks": ["41"] },
    { "id": 69, "tasks": ["42.1", "42.2", "42.3", "42.4", "42.5", "42.6", "42.7", "42.8", "42.9", "42.10", "42.11", "42.12", "42.13", "42.14", "42.15", "42.16", "42.17", "42.18"] },
    { "id": 70, "tasks": ["42.19", "42.20", "42.21", "42.22", "42.23", "42.24"] },
    { "id": 71, "tasks": ["43"] },
    { "id": 72, "tasks": ["44.1", "44.2", "44.3", "44.4", "44.5", "44.6", "44.7", "44.8", "44.9", "44.10", "44.11"] },
    { "id": 73, "tasks": ["44.12", "44.13"] },
    { "id": 74, "tasks": ["45.1", "45.2", "45.3", "45.4"] },
    { "id": 75, "tasks": ["45.5", "45.6", "45.7", "45.8", "45.9", "45.10"] },
    { "id": 76, "tasks": ["46"] }
  ]
}
```
