# Implementation Plan: Radar Imobiliário — Especificação Completa

## Overview

Este plano converte o `design.md` desta spec em passos incrementais de código Python 3.12,
PostgreSQL 16 com pgvector, FastAPI, LangGraph e React. Cada tarefa referencia os critérios de
aceitação do `requirements.md` que a originam. Os dois documentos são as **únicas** fontes de
trabalho: nada aqui depende de leitura de outro arquivo, e os artefatos derivados são não
normativos (`D86`).

**Contagens que governam este plano**, todas lidas do `requirements.md` e do `design.md`:

- **97 requisitos**, `R1` a `R97`, com **85 `P0`**, **11 `P1`** e **1 `P2`** (`D89`);
- **171 propriedades** de correção, numeradas de 1 a 171, em dezessete famílias;
- **11 meta-testes**, `MT-01` a `MT-11`;
- **44 testes de regressão**, `REG-001` a `REG-044`, um teste por linha do Anexo E;
- **4 Golden Cases** dos Anexos E e F;
- **13 etapas** de implementação: as **11 etapas de construção de `D88`**, que realizam os 85
  requisitos `P0`, mais a **etapa 12** com os 11 requisitos `P1` e a **etapa 13** com o único
  `P2` (`R72`);
- **61 entidades** no modelo físico, **dezesseis** itens de integridade, **60 enums**, **55**
  regras canônicas, **234** itens de checklist como versão 1, **11 camadas** de decisão,
  **19 verificações** no gate jurídico, **13 componentes** de custo, **16 fases** de pipeline e
  **20 etapas** de orquestração.

**Ordem de construção e prioridade de requisito são dimensões distintas.** Um requisito `P0`
construído no passo 10 continua `P0`: os checklists parametrizáveis (`R92`) e o Radar automático
(`R93`) são `P0` e são construídos tarde porque dependem do motor único e do catálogo
estabilizado, não porque sejam menos exigidos. Prioridade responde "o MVP existe sem isto?";
ordem de construção responde "o que precisa estar pronto antes?". Nenhuma se deduz da outra.

A **etapa 1** (domínio determinístico) é grande e é a única com ordenação interna publicada, em dez
blocos (`1.1` a `1.10`). Ela aparece aqui dividida nas tarefas de topo 1 a 15, preservando a ordem
dos blocos. As etapas 2 a 13 seguem nas tarefas 16 a 32. O **primeiro marco funcional de `D88`**
— análise manual real, do envio dos documentos até a decisão apresentada na interface — fecha ao
fim da **etapa 7**, não da etapa 4, porque exige interface de programação e interface do
investidor; o checkpoint da tarefa 23 é esse marco.

**Convenção de idioma (`D72`).** Todo identificador de implementação é escrito em português,
exatamente como o `design.md` o nomeia. A renomeação **é trabalho de implementação, não convenção
documental**: alcança `src/radar/**`, `db/schema.sql`, `scripts/**` e `tests/**`, entra na etapa 1
como renomeação de módulos, na etapa 2 como migração versionada de tabelas, colunas, índices,
restrições e enums, na etapa 6 como nomes de recurso, campo e valor de domínio, e na etapa 7 como
interface integralmente em português. `MT-11` impede a reintrodução de identificador em inglês.
Exceções permitidas apenas para tecnologia e biblioteca externa (`FastAPI`, `LangGraph`,
`SQLAlchemy`, `pgvector`, `hypothesis`, `pytest`, `ruff`, `mypy`, `React`, `Decimal`, `pydantic`) e
para os códigos estáveis, que **não** são renomeados (`RULE-*`, `MC-*`, `B-*`, `C-*`, `REG-*`,
`MT-*`, `CUS-*`, `GLB-*`, `INV-*`, `LOC-*`, `TIP-*`, `PRI-*`, `VAL-*`, `CMP-*`, `REN-*`, `LIQ-*`,
`RISK-*`, `CONF-*`, `FRESH`, `SCORE-*`, `STR`, `PORT-*`, `EXC-*`, `ALT-*`, `MON-*`, `HS-*`,
`PL-*`, `RL-*`, `HL-*`, `E01` a `E09`, gates `G0` a `G7` e `G1-P`, níveis `I0` a `I4`, `SAFE-*`,
`P-A` a `P-E`, `D*`, `R*`, `P*`).

**Base existente.** O produto já tem fatia vertical em `src/radar/**` com **22 testes passando**,
o esquema em `db/schema.sql`, utilitários em `scripts/**`, testes em `tests/**` e configuração em
`pyproject.toml` (comprimento de linha 100, alvo `py312`, modo estrito). Os módulos atuais estão em
inglês (`capture/`, `domain/`, `engines/`, `orchestration/`, `pipeline/`, `services/`, `db/`) e são
renomeados nas primeiras tarefas.

**Convenção de teste de propriedade.** Cada uma das 171 propriedades tem **exatamente um** teste,
em arquivo próprio `testes/propriedades/test_propriedade_NNN.py`, com a etiqueta
`Feature: radar-imobiliario-especificacao-completa, Property {n}: {texto}` e no mínimo 100
iterações. Arquivo por propriedade é o que torna as tarefas de teste independentes entre si.
`P7.12` **não** é propriedade: é contraexemplo verificado e entra como teste dirigido de entradas
fixas (`REG-033`).

## Tasks

- [ ] 1. Fundação de tipos, taxonomia de erro e infraestrutura de teste (bloco 1.1)

  - [ ] 1.1 Criar o valor com estado de informação
    - Criar `src/radar/dominio/informado.py` com `Informado[T]` congelado — valor, estado da informação, fonte, data de observação, confiança e qualidade da evidência — e o sentinela explícito `Desconhecido`
    - Declarar a métrica provisória que carrega o motivo da provisoriedade, usada quando componente de custo é `DESCONHECIDO` de impacto alto ou crítico
    - Nenhum campo de domínio tem default permissivo: ausência é `Desconhecido`, nunca zero, string vazia ou valor neutro
    - _Requisitos: 3.2, 10.2, 26.7, 26.10, 26.12_

  - [ ] 1.2 Declarar os 60 enums fechados com as contagens do modelo de dados
    - Criar `src/radar/dominio/enumeracoes.py` com todos os enums nomeados em português e com as contagens que são parte do contrato: `FaseDoPipeline` 16, `EstadoDeDecisao` 6, `CamadaDeDecisao` 11, `Estrategia` 6, `PerfilDeAtivo` 9, `EstadoDeOcupacao` 7, `CategoriaDeLiquidez` 7, `NivelDeConfianca` 6, `EstadoDaInformacao` 6, `QualidadeDaEvidencia` 5, `OrigemDeEvidencia` 5, `TipoDeSegmentoDeConhecimento` 15, `ClasseDeUrgencia` 6, `ClasseDeAtratividade` 5, `SituacaoJuridica` 3, `ResultadoDeVerificacao` 5, `ResultadoP0` 5, `FormatoNumerico` 3, `UnidadeDePercentual` 2, `TipoDeDocumento` 9, `OrigemDeDocumento` 3, `TipoDeDebito` 4, `SituacaoDeDebito` 5, `ResponsabilidadePeloDebito` 3, `SituacaoDeProcesso` 5, `ImpactoDeProcesso` 4, `ResultadoDeEviccao` 3, `EstadoDeAverbacaoDeLeilaoNegativo` 4, `PortaDeEntrada` 2, `ResultadoDeTriagem` 2, `CategoriaDeDiferenca` 5, `EstadoDeMonitoramento` 10, `ClasseDeConfiabilidadeDeFonte` 6, `SituacaoDeGovernanca` 6 e os demais declarados na seção de enumerações
    - Aplicar a tabela de correspondência de rótulos normativos: cada rótulo do `requirements.md` tem um identificador de implementação em português, um para um
    - _Requisitos: 18.1, 40.2, 44.1, 44.2, 53.1, 53.5, 56.5, 62.4, 72.2, 84.1, 88.5, 91.2, 91.4, 93.3_

  - [ ] 1.3 Implementar a classificação por faixa única
    - Criar `src/radar/motores/faixas.py` com `classificar_por_faixa`, por limite inferior, comparação `>=` e avaliação em ordem decrescente, total sobre `[0, 100]` e sem lacuna para valores não inteiros
    - Toda faixa do produto — escore, confiança, liquidez, materialidade — passa a usar esta função única
    - _Requisitos: 40.2, 49.6, 50.3, 50.4_

  - [ ] 1.4 Criar a taxonomia de erro em português
    - Criar `src/radar/erros.py` com `ErroDoRadar` como raiz, carregando código estável, mensagem de negócio e contexto estruturado sem segredo nem payload íntegro de terceiro
    - Família 1, entrada e contrato: `ErroDeValidacaoDeDominio`, `ErroDeFronteiraDeEnum`, `ErroDePreCondicao`, `ErroDeEntradaAmbigua`, `ErroDeReferenciaInexistente`
    - Família 2, evidência e governança: `ErroDeEvidenciaSemFonte`, `ErroDePromocaoDeEvidencia`, `ErroDeViolacaoDeImutabilidade`, `ErroDeOperacaoNaoPermitida`, `ErroDeParametroSemVigencia`, `ErroDeParametroPendenteDeDecisao`, `ErroDeExcecaoSobreBloqueio`, `ErroDeEntidadeAusenteNoDicionario`, `ErroDeConfiguracaoDeChecklist`, `ErroDeIntegridadeDeDocumento`
    - Família 3, capacidade e infraestrutura: `ErroDeNormalizadorNaoEncontrado`, `ErroDeConfiguracaoDeSupervisao`, `ErroDeFonteIndisponivel`, `ErroDeObtencaoDoConector`
    - Declarar `RejeicaoDeCaptura` como **resultado registrado, não exceção**: payload reprovado no gate `G0` vira captura com estado `REJEITADA` e causa nomeada, sem criar oportunidade
    - _Requisitos: 20.3, 20.4, 62.11, 63.4, 74.11, 79.9, 83.6, 86.8, 92.5, 92.6_

  - [ ] 1.5 Renomear os módulos de domínio e motores existentes para português
    - Renomear os pacotes e módulos de `src/radar/**`: `capture` → `captura` (`parsing` → `interpretacao`, `caixa`, `schemas` → `esquemas`), `domain` → `dominio` (`enums` → `enumeracoes`, `models` → `modelos`, `parameters` → `parametros`), `engines` → `motores` (`calculation` → `calculo`, `decision` → `decisao`), `pipeline/identity` → `pipeline/identidade`, `pipeline/legal_gate` → `pipeline/gate_juridico`, `orchestration/graph` → `orquestracao/grafo`, `services/analysis_service` → `servicos/servico_de_analise`, `db/{models,repository,session}` → `db/{modelos,repositorio,sessao}`, `config` → `configuracao`
    - Renomear classes, funções, parâmetros e variáveis internas conforme a tabela de correspondência; renomear `tests/` para `testes/`
    - Manter os 22 testes existentes verdes ao fim da renomeação, ajustando apenas nomes e imports
    - _Requisitos: 94.2, 97.3_

  - [ ] 1.6 Configurar a infraestrutura de teste de propriedade
    - Fixar `hypothesis` com pino exato em `pyproject.toml`, ao lado de `pytest`, `pytest-cov`, `ruff` e `mypy`
    - Declarar os perfis `dev` (100), `ci` (500), `noturno` (5.000) e `regressao` (banco de exemplos persistido), com `deadline` desativado apenas com justificativa no próprio teste
    - Criar os geradores compartilhados em `testes/geradores/`, um módulo por domínio, nomeados em português: `dinheiro`, `area`, `percentual`, `data_hora_br`, `informado`, `payload_bruto`, `oferta_normalizada`, `sinais_de_identidade`, `vinculo_de_imovel`, `resultados_de_verificacao`, `registro_de_evidencia`, `proposta_de_evidencia`, `conjunto_de_pendencias`, `comparavel`, `entradas_de_valuation`, `composicao_de_custo`, `entradas_economicas`, `entradas_de_preco_maximo`, `premissas_de_cenario`, `registro_de_risco`, `fatores_de_liquidez`, `fatores_de_escore`, `conjunto_de_pesos`, `estado_de_portfolio`, `entrada_de_decisao`, `checklist_de_lance`, `hierarquia_de_parametros`, `registro_de_excecao`, `segmento_de_conhecimento`, `documento`, `versao_de_documento`, `par_de_versoes_de_analise`, `configuracao_de_checklist`, `conjunto_de_debitos`, `processo_judicial`, `payload_de_conector`, `porta_de_entrada`, `candidato_do_radar`
    - Injetar em cada gerador de escala os valores de fronteira obrigatórios: 89,5 · 79,5 · 74,5 · 69,5 · 59,5 · 49,5 · 39,5, `"47.76"`, `"191651.31"`, `"2,5%"`, `"2.5%"`, 1 com unidade `PORCENTO`, o valor exato de cada limiar de materialidade e de decisão, versão 1 de documento e de análise, par de versões idênticas e documento com hash divergente
    - Criar `testes/propriedades/` com um arquivo por propriedade e a etiqueta obrigatória no comentário de cada teste
    - _Requisitos: 73.1, 73.2, 73.7_

  - [ ] 1.7 Criar o esqueleto dos onze meta-testes
    - Criar `testes/meta/` com `MT-01` a `MT-11` executáveis e falhando por conteúdo ausente, não por erro de importação: rastreabilidade de propriedades, um teste por propriedade, cobertura de checklist em qualquer versão, cobertura das 55 regras, cobertura da disciplina de lance, cobertura de prioridade dos 97 requisitos com as contagens 85/11/1, ponto único de verdade da tabela `STR`, soma de pesos, contagem dos 60 enums, isolamento da IA e convenção de idioma
    - _Requisitos: 73.1, 73.3, 73.8, 75.5_

  - [ ] 1.8 Implementar `MT-11` completo — verificação da convenção de idioma
    - Implementar o meta-teste que percorre a árvore sintática dos módulos Python de `src/radar/**` e de `scripts/**` e o esquema de `db/schema.sql`, comparando módulos, pacotes, classes, funções, parâmetros, tabelas, colunas, índices, enums e valores de enum contra um dicionário de exceções versionado
    - Falhar **apontando o identificador, o arquivo e a linha**; acrescentar entrada ao dicionário de exceções é mudança revisável, não escape silencioso
    - Colocar `MT-11` na mesma barreira de integração que `ruff` e `mypy --strict`
    - _Requisitos: 94.2, 97.3_

  - [ ]* 1.9 Escrever testes unitários da fundação
    - Cobrir `Informado[T]` e `Desconhecido` na fronteira, a totalidade de `classificar_por_faixa` nos limites inteiros e fracionários, e a hierarquia de exceções com seus códigos estáveis
    - _Requisitos: 3.2, 26.7, 49.6, 79.9_

- [ ] 2. Correções numéricas verificadas (bloco 1.2)

  - [ ] 2.1 Reescrever a interpretação decimal sem heurística de magnitude
    - Reescrever `src/radar/captura/interpretacao.py` com `FormatoNumerico` (`pt_br`, `simples`, `auto`) e `interpretar_decimal(bruto, formato) -> Informado[Decimal]`
    - Em `auto`: vírgula presente é separador decimal; ponto único seguido de uma ou duas casas é decimal; ponto único seguido de exatamente três dígitos com grupo curto à esquerda é **ambíguo** e resulta em `Desconhecido`; múltiplos pontos são separador de milhar
    - Nenhuma multiplicação por 100 e nenhuma inferência por magnitude: entrada não interpretável nunca vira zero
    - _Requisitos: 3.4, 3.4.1, 3.4.4_

  - [ ]* 2.2 Escrever teste de propriedade para o round-trip monetário
    - **Property 7: Round-trip monetário (`P2.2`)**
    - **Validates: Requirements 3.4**

  - [ ]* 2.3 Escrever teste de propriedade para a invariância de magnitude
    - **Property 15: Invariância de magnitude na interpretação numérica (`P2.10`)**
    - **Validates: Requirements 3.4.1**

  - [ ]* 2.4 Escrever teste de propriedade para entrada não interpretável
    - **Property 17: Entrada não interpretável resulta em DESCONHECIDO (`P2.12`)**
    - **Validates: Requirements 3.2, 3.4.4**

  - [ ]* 2.5 Escrever teste de propriedade para o round-trip de área
    - **Property 8: Round-trip de área (`P2.3`)**
    - **Validates: Requirements 3.4**

  - [ ] 2.6 Reescrever a interpretação de percentual com unidade obrigatória
    - Implementar `interpretar_percentual(bruto, unidade)` com `UnidadeDePercentual` (`fracao`, `porcento`) exigida na entrada, resultado em `[0, 1]` ou `Desconhecido`
    - Alíquota fracionária (`"2,5%"` e `"2.5%"`) resulta em 0,025; `1` com unidade `PORCENTO` resulta em 0,01
    - _Requisitos: 3.4.2, 3.4.3, 3.4.4_

  - [ ]* 2.7 Escrever teste de propriedade para o round-trip de percentual
    - **Property 9: Round-trip de percentual (`P2.4`)**
    - **Validates: Requirements 3.4**

  - [ ]* 2.8 Escrever teste de propriedade para a unidade de percentual
    - **Property 16: Percentual normalizado com unidade respeitada (`P2.11`)**
    - **Validates: Requirements 3.4.2, 3.4.3**

  - [ ] 2.9 Implementar a interpretação de data e data com hora no formato brasileiro
    - Implementar `interpretar_data_hora_br(bruto) -> Informado[datetime]`, com data sem hora e data com hora, e ausência resultando em `Desconhecido`
    - _Requisitos: 3.4_

  - [ ]* 2.10 Escrever teste de propriedade para o round-trip de data
    - **Property 10: Round-trip de data e data com hora (`P2.5`)**
    - **Validates: Requirements 3.4**

  - [ ] 2.11 Levar `Decimal` a todo o caminho monetário e corrigir o retorno anualizado
    - Substituir `float` por `Decimal` em todo o caminho monetário e percentual de `src/radar/motores/**` e `src/radar/captura/**`, de modo que `float` atravessando a fronteira seja erro de tipo sob `mypy --strict`
    - Implementar `roi_anualizado(roi, meses)` com a composição correta e pré-condição que rejeita prazo não positivo
    - _Requisitos: 27.17, 30.3, 30.3.1, 30.3.2_

  - [ ]* 2.12 Escrever teste dirigido das fronteiras de interpretação numérica
    - Entradas fixas `"47.76"`, `"191651.31"`, `"1.234,56"`, `"1234,56"`, `"1234.56"`, `"2,5%"`, `"2.5%"` e `1` com unidade `PORCENTO`, com os valores esperados declarados
    - _Requisitos: 3.4, 3.4.1, 3.4.2, 3.4.3_

- [ ] 3. Checkpoint — fundação de tipos e correções numéricas
  - Executar a suíte inteira, `ruff` e `mypy --strict`; confirmar que os 22 testes existentes seguem verdes após a renomeação e a troca para `Decimal`, e que `MT-11` já falha diante de identificador em inglês introduzido de propósito. Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 4. Captura, identidade, deduplicação, perfil e localização (bloco 1.3)

  - [ ] 4.1 Criar o registro de fontes
    - Criar `src/radar/captura/registro_de_fontes.py` com `RegistroDeFontes.cadastrar`, `confiabilidade` e `desativar`: fonte como entidade própria com tipo, nome, URL, abrangência geográfica, periodicidade esperada, campos disponíveis, confiabilidade de 0 a 100, situação e data da última captura
    - Declarar os oito tipos de fonte e a confiabilidade por categoria de dado nas classes A, B, C, D, E e U; entrada do analista é marcada como interpretação com autor registrado
    - Desativar preserva as capturas já registradas e interrompe novas capturas
    - _Requisitos: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

  - [ ] 4.2 Implementar a impressão digital e o serviço de captura idempotente
    - Criar `src/radar/captura/servico_de_captura.py` com `impressao_digital(payload)` invariante à ordem das chaves e `ServicoDeCaptura.registrar`, `substituir` e `rejeitar`
    - Preservar o payload bruto sem alteração, com tipo e nome da fonte, identificador da publicação, referência e data e hora da captura; registrar preço e situação exatamente como informados pela fonte, além das versões normalizadas
    - Idempotência garantida pelo banco por `(fonte_id, hash)`; correção cria registro novo e nunca altera o anterior; `rejeitar` grava `RejeicaoDeCaptura` com a causa e **não** cria oportunidade
    - _Requisitos: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7_

  - [ ]* 4.3 Escrever teste de propriedade para a invariância de ordem das chaves
    - **Property 1: Impressão digital invariante à ordem das chaves (`P1.1`)**
    - **Validates: Requirements 2.2**

  - [ ]* 4.4 Escrever teste de propriedade para o determinismo da impressão digital
    - **Property 2: Impressão digital determinística (`P1.2`)**
    - **Validates: Requirements 2.2**

  - [ ]* 4.5 Escrever teste de propriedade para a distinção de conteúdos
    - **Property 3: Impressão digital distingue conteúdos distintos (`P1.3`)**
    - **Validates: Requirements 2.2**

  - [ ]* 4.6 Escrever teste de propriedade para a idempotência do registro de captura
    - **Property 4: Idempotência do registro de captura (`P1.4`)**
    - **Validates: Requirements 2.3**

  - [ ]* 4.7 Escrever teste de propriedade para o caráter append-only da captura
    - **Property 5: Captura é append-only (`P1.5`)**
    - **Validates: Requirements 2.4, 2.5**

  - [ ] 4.8 Reescrever o normalizador com despacho por tipo de fonte
    - Declarar o protocolo `Normalizador` e o mapa `NORMALIZADORES` em `src/radar/captura/normalizadores/base.py`, com a implementação da CAIXA em `caixa.py`; fonte sem normalizador registrado levanta `ErroDeNormalizadorNaoEncontrado`, nunca despacha para o normalizador da CAIXA
    - Extrair identificação, localização com `complemento`, características físicas com `banheiros`, dados do certame, condições comerciais e situação de ocupação; preservar o valor original de cada campo
    - Campo ausente é `Desconhecido` explícito; produzir a lista exata de campos ausentes; nunca inferir tipo de área; nunca atribuir a avaliação da fonte ao valor de mercado; precedência de vacância sobre ocupação na interpretação textual
    - Persistir a oferta normalizada vinculada à captura, de modo que a normalização vigente na data da análise seja reproduzível
    - _Requisitos: 3.1, 3.2, 3.3, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 74.9, 74.10_

  - [ ]* 4.9 Escrever teste de propriedade para campo ausente
    - **Property 6: Campo ausente resulta em DESCONHECIDO (`P2.1`)**
    - **Validates: Requirements 3.2**

  - [ ]* 4.10 Escrever teste de propriedade para a idempotência da normalização
    - **Property 11: Idempotência da normalização (`P2.6`)**
    - **Validates: Requirements 3.1, 3.11**

  - [ ]* 4.11 Escrever teste de propriedade para a lista de ausências
    - **Property 12: Lista de ausências é exata (`P2.7`)**
    - **Validates: Requirements 3.9**

  - [ ]* 4.12 Escrever teste de propriedade para a avaliação da fonte
    - **Property 13: Avaliação da fonte nunca vira valor de mercado (`P2.8`)**
    - **Validates: Requirements 3.10**

  - [ ]* 4.13 Escrever teste de propriedade para o tipo de área
    - **Property 14: Tipo de área nunca é inferido (`P2.9`)**
    - **Validates: Requirements 3.5**

  - [ ]* 4.14 Escrever teste de propriedade para a precedência de vacância
    - **Property 18: Precedência de vacância sobre ocupação (`P2.13`)**
    - **Validates: Requirements 3.8**

  - [ ] 4.15 Implementar os gates de dados e o qualificador `G1`
    - Criar `src/radar/pipeline/qualificacao.py` com `GateDeDados` (`G0` a `G7`), `AvaliacaoDeGates` e `avaliar_gates_de_dados`, devolvendo o primeiro gate não satisfeito e exatamente qual informação falta
    - Classificar o impacto de cada ausência em baixo, médio, alto ou crítico e reduzir a confiança da dimensão correspondente; materializar a fase `QUALIFICADO`
    - _Requisitos: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 4.10_

  - [ ] 4.16 Implementar a resolução de identidade e a chave conceitual
    - Criar `src/radar/pipeline/identidade.py` com `NivelDeIdentidade` (`I0` a `I4`), `ForcaDeSinal`, `SinalDeIdentidade`, `FORCA_DO_SINAL`, `resolver_identidade` e `chave_conceitual`
    - Declarar `PROIBIDOS_PARA_IDENTIDADE` com preço, avaliação da fonte e desconto, de modo que identidade seja invariante a preço por construção
    - Endereço conhecido com unidade desconhecida limita a identidade a `I2` e abre pendência; conflito material entre identificadores resulta em `PENDENTE`
    - _Requisitos: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.10, 7.11, 7.12, 8.1, 8.2, 8.3, 8.4_

  - [ ]* 4.17 Escrever teste de propriedade para a totalidade da resolução de identidade
    - **Property 19: Resolução de identidade é total (`P3.1`)**
    - **Validates: Requirements 7.1**

  - [ ]* 4.18 Escrever teste de propriedade para a monotonicidade dos sinais
    - **Property 20: Monotonicidade na força dos sinais (`P3.2`)**
    - **Validates: Requirements 7.2, 7.3, 7.4, 7.5, 7.6**

  - [ ]* 4.19 Escrever teste de propriedade para a invariância da identidade ao preço
    - **Property 21: Identidade é invariante ao preço (`P3.3`)**
    - **Validates: Requirements 7.7**

  - [ ] 4.20 Implementar a deduplicação e o vinculador de imóveis
    - Criar `src/radar/pipeline/deduplicacao.py` com `VeredictoDeIdentidade` de três valores (`mesmo`, `diferente`, `indeterminado`), `SINAIS_COMPLEMENTARES` e `e_o_mesmo_imovel`, simétrico e reflexivo, com matrícula como evidência decisiva
    - Criar `VinculadorDeImoveis` com `vincular` idempotente por `(captura_id, imovel_id)`, `desvincular` que preserva o histórico do vínculo anterior e `revincular_republicada` que tenta associar oferta encerrada e republicada ao imóvel histórico antes de criar novo
    - Unidades distintas do mesmo condomínio nunca são fundidas; evidência insuficiente resulta em `indeterminado`
    - _Requisitos: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 9.10, 9.11, 9.12_

  - [ ]* 4.21 Escrever teste de propriedade para a invariância da deduplicação ao preço
    - **Property 22: Deduplicação é invariante ao preço (`P3.4`)**
    - **Validates: Requirements 9.5**

  - [ ]* 4.22 Escrever teste de propriedade para a matrícula como evidência decisiva
    - **Property 23: Matrícula é decisiva (`P3.5`)**
    - **Validates: Requirements 9.1**

  - [ ]* 4.23 Escrever teste de propriedade para a simetria do veredicto
    - **Property 24: Simetria do veredicto (`P3.6`)**
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5, 9.6**

  - [ ]* 4.24 Escrever teste de propriedade para a reflexividade do veredicto
    - **Property 25: Reflexividade do veredicto (`P3.7`)**
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5, 9.6**

  - [ ]* 4.25 Escrever teste de propriedade para a idempotência do vínculo
    - **Property 26: Idempotência do vínculo (`P3.8`)**
    - **Validates: Requirements 9.7**

  - [ ]* 4.26 Escrever teste de propriedade para unidades distintas
    - **Property 27: Unidades distintas nunca são fundidas (`P3.9`)**
    - **Validates: Requirements 9.11**

  - [ ]* 4.27 Escrever teste de propriedade para evidência insuficiente
    - **Property 28: Evidência insuficiente resulta em veredicto indeterminado (`P3.10`)**
    - **Validates: Requirements 9.6**

  - [ ]* 4.28 Escrever teste de propriedade para a preservação do histórico de vínculo
    - **Property 29: Desvincular preserva histórico (`P3.11`)**
    - **Validates: Requirements 9.9**

  - [ ] 4.29 Consolidar o perfil do imóvel nos nove grupos
    - Criar `src/radar/pipeline/perfil.py` com `GrupoDePerfil` e `consolidar_perfil`: cada campo recebe exatamente um estado de informação e registra a fonte que o sustentou; inferência marca `INFERIDO` e registra a premissa
    - Versionar o perfil com numeração crescente, data, autor, campos alterados e motivo, sem sobrescrita; registrar o grupo Qualidade com estado de conservação, nível de reforma estimado, padrão construtivo e idade aparente
    - Registrar o histórico de preços observados com valor, moeda, data, fonte, tipo de preço e variação em relação à observação anterior; materializar a fase `CONSOLIDADO`
    - _Requisitos: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9, 10.10, 10.11, 74.4, 74.5_

  - [ ]* 4.30 Escrever teste de propriedade para o estado de informação único
    - **Property 42: Todo valor tem exatamente um estado de informação (`P5.5`)**
    - **Validates: Requirements 10.2**

  - [ ] 4.31 Registrar as divergências entre fontes
    - Implementar `classificar_divergencia` gravando data, fonte A, informação A, fonte B, informação B, dimensão afetada, materialidade, impacto na decisão e situação; a divergência permanece aberta até confirmação oficial e nunca é resolvida por escolha silenciosa
    - _Requisitos: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 74.6_

  - [ ] 4.32 Classificar a localização em classes A–E
    - Criar `src/radar/pipeline/localizacao.py` com `ClasseDeLocalizacao` e `classificar_localizacao`, parametrizado e sem presumir que região de menor renda é ruim; persistir a localização como entidade com região, classe, perfil de demanda, liquidez regional e faixa de preço predominante
    - _Requisitos: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7, 11.8, 74.1_

- [ ] 5. Gate jurídico de 19 verificações e camada de evidência (bloco 1.4)

  - [ ] 5.1 Declarar as dezenove verificações jurídicas como dados
    - Ampliar `src/radar/pipeline/gate_juridico.py` e criar `src/radar/regras/juridicas/` com `VERIFICACOES_JURIDICAS` contendo exatamente 19 entradas: `RULE-JUR-001` a `RULE-JUR-013`, `RULE-ED-001` a `RULE-ED-004`, `RULE-ID-001` e `RULE-ID-002`
    - Declarar `ResultadoDeVerificacao` com cinco valores, mantendo `NAO_APLICAVEL` distinto de `DESCONHECIDO`, `ResultadoP0` com cinco valores, `SituacaoJuridica` fechada em `REGULAR`, `PENDENTE` e `BLOQUEIO`, e o mapa `P0_PARA_SITUACAO_JURIDICA`
    - Implementar `avaliar_gate_juridico` determinístico e confluente: qualquer `IRREGULAR` produz `BLOQUEIO`; verificação obrigatória `DESCONHECIDO` sem irregularidade produz `PENDENTE`, nunca `REGULAR`; cada verificação avaliada gera exatamente uma evidência registrada, inclusive as `DESCONHECIDO`
    - Validar `situacao_juridica` na fronteira com falha explícita: nenhuma string fora do enum é interpretada como liberada
    - _Requisitos: 12.1, 12.2, 12.4, 12.5, 12.6, 12.7, 12.9, 12.10, 12.11_

  - [ ]* 5.2 Escrever teste de propriedade para o determinismo do gate jurídico
    - **Property 30: Determinismo do gate jurídico (`P4.1`)**
    - **Validates: Requirements 12.5, 12.6**

  - [ ]* 5.3 Escrever teste de propriedade para a confluência do gate jurídico
    - **Property 31: Confluência do gate jurídico (`P4.2`)**
    - **Validates: Requirements 12.1, 12.5**

  - [ ]* 5.4 Escrever teste de propriedade para irregularidade
    - **Property 32: Irregularidade implica BLOQUEIO (`P4.3`)**
    - **Validates: Requirements 12.6, 13.4**

  - [ ]* 5.5 Escrever teste de propriedade para ausência de evidência no gate
    - **Property 33: Ausência de evidência nunca produz REGULAR (`P4.4`)**
    - **Validates: Requirements 12.6, 20.7**

  - [ ]* 5.6 Escrever teste de propriedade para a evidência por verificação
    - **Property 34: Uma evidência por verificação avaliada (`P4.5`)**
    - **Validates: Requirements 20.1, 20.7**

  - [ ]* 5.7 Escrever teste de propriedade para o enum fechado de situação jurídica
    - **Property 94: Enum de situação jurídica é total e fechado (`P10.16`)**
    - **Validates: Requirements 12.5, 12.6**

  - [ ] 5.8 Implementar as verificações registrais e de titularidade
    - Implementar `verificar_registro` sobre a matrícula, com cadeia dominial, consolidação da propriedade registrada com ato, data e **texto integral**, ônus reais, penhora e indisponibilidade, e `EstadoDeAverbacaoDeLeilaoNegativo` com quatro valores, inclusive `EM_TRATAMENTO`
    - Vaga com matrícula autônoma e abrangência indeterminada resulta em `PENDENTE` para a verificação registral da vaga; o texto do ato registral prevalece sobre a simples detecção do evento
    - _Requisitos: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6, 13.7, 13.8, 13.9, 13.10, 13.11, 13.12, 13.13, 13.14_

  - [ ] 5.9 Implementar a verificação de mora e intimações
    - Avaliar constituição em mora, intimação para purgação da mora — pessoal ou por edital —, prazo legal e purgação, sem presumir exigência nem dispensa, conforme a modalidade do procedimento e o caso concreto
    - _Requisitos: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7, 14.8, 14.9, 14.10_

  - [ ] 5.10 Implementar a verificação do edital, cronologia e coerência do certame
    - Confrontar edital e matrícula, verificar cronologia das praças, valor mínimo de primeira e segunda praça, responsabilidades, prazos e regras específicas que alterem custo, prazo, posse ou obrigações do arrematante
    - Implementar `verificar_divergencia_portal_edital` entre o retrato da oferta no portal e o edital, registrando divergência como pendência
    - _Requisitos: 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7, 15.8, 15.10, 15.11, 15.12, 15.13_

  - [ ] 5.11 Implementar a verificação de evicção
    - Implementar `verificar_eviccao` com `ResultadoDeEviccao` de três valores, distinguindo cláusula **comprovadamente inexistente** no edital obtido, que resulta em `BLOQUEIO`, de cláusula **não verificada**, que resulta em `PENDENTE`; os dois casos permanecem distinguíveis no registro
    - _Requisitos: 15.9, 15.9.1, 15.9.2_

  - [ ]* 5.12 Escrever teste de propriedade para a evidência de ausência
    - **Property 116: Evidência de ausência produz o efeito da regra (`P11.18`)**
    - **Validates: Requirements 15.9, 15.9.1, 15.9.2**

  - [ ] 5.13 Classificar o impacto de processo judicial
    - Implementar `classificar_processo` com `ImpactoDeProcesso` em quatro níveis; existência isolada de processo não é bloqueio automático e só impacto material impeditivo sem mitigação produz `BLOQUEIO`; decisão liminar que atinge o leilão bloqueia até resolução ou mitigação comprovada
    - _Requisitos: 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 16.8_

  - [ ]* 5.14 Escrever teste de propriedade para processo sem impacto material
    - **Property 37: Processo sem impacto material nunca bloqueia (`P4.8`)**
    - **Validates: Requirements 16.6**

  - [ ] 5.15 Implementar os sinais jurídicos de investigação obrigatória
    - Implementar `sinais_juridicos` registrando cada sinal como evidência com proveniência, estado e localização documental, sem convertê-lo em bloqueio automático
    - _Requisitos: 17.1, 17.2, 17.3, 17.4, 17.5_

  - [ ] 5.16 Tratar ocupação e locação como risco econômico
    - Implementar `avaliar_ocupacao` com `EstadoDeOcupacao` de **sete** valores, mantendo o risco de posse como categoria distinta do risco de nulidade; ocupação sai do gate jurídico e vai para a camada 6, exceto os dois casos de bloqueio crítico da camada 0
    - Avaliar locação vigente, cláusula de vigência averbada e o impacto da locação sobre posse, prazo de saída e rentabilidade, registrado no cenário econômico
    - _Requisitos: 18.1, 18.2, 18.2.1, 18.2.2, 18.3, 18.4, 18.5, 18.6, 18.7, 18.8, 19.1, 19.2, 19.3, 19.4, 19.5, 19.6_

  - [ ]* 5.17 Escrever teste de propriedade para a neutralidade da ocupação no gate
    - **Property 36: Ocupação nunca altera a situação jurídica (`P4.7`)**
    - **Validates: Requirements 18.2, 18.8**

  - [ ] 5.18 Criar a camada de evidência append-only com proveniência obrigatória
    - Criar `src/radar/evidencia/repositorio.py` com `RepositorioDeEvidencias.acrescentar`, `promover`, `transitar_fato` e `fatos`, gravando regra, fonte, origem, documento, versão do documento, localização exata, fato, valor, estado, confiança, qualidade, autor, data de observação, data de extração e validade
    - Rejeitar evidência sem fonte identificada; nunca atualizar nem remover; preservar evidências contraditórias e marcar o fato como conflitante; `transitar_fato` para `CONFIRMADO` exige identificador de evidência de suporte
    - Criar `src/radar/evidencia/propostas.py` com `PropostaDeEvidencia` como tipo **distinto** de evidência, promovível apenas por ato humano registrado ou regra determinística declarada
    - _Requisitos: 20.1, 20.2, 20.3, 20.4, 20.5, 20.6, 20.7_

  - [ ]* 5.19 Escrever teste de propriedade para evidência sem fonte
    - **Property 38: Evidência sem fonte é rejeitada (`P5.1`)**
    - **Validates: Requirements 20.3**

  - [ ]* 5.20 Escrever teste de propriedade para a promoção de fato
    - **Property 39: DESCONHECIDO não vira CONFIRMADO sem suporte (`P5.2`)**
    - **Validates: Requirements 20.4**

  - [ ]* 5.21 Escrever teste de propriedade para a monotonicidade do repositório
    - **Property 40: Monotonicidade do repositório de evidências (`P5.3`)**
    - **Validates: Requirements 20.5, 20.6**

  - [ ]* 5.22 Escrever teste de propriedade para a preservação de contradições
    - **Property 41: Contradições são preservadas (`P5.4`)**
    - **Validates: Requirements 20.5**

  - [ ]* 5.23 Escrever teste de propriedade para a cobertura do Anexo A
    - **Property 35: Cobertura total do Anexo A (`P4.6`)**
    - **Validates: Requirements 36.5**

- [ ] 6. Checkpoint — gate jurídico e camada de evidência
  - Executar a suíte inteira, `ruff` e `mypy --strict`; confirmar que nenhuma ausência de informação jurídica produz liberação, que `NAO_APLICAVEL` e `DESCONHECIDO` permanecem distinguíveis e que a ocupação não altera a situação jurídica. Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 7. Mercado, comparáveis e valuation (bloco 1.5)

  - [ ] 7.1 Selecionar e qualificar comparáveis
    - Criar `src/radar/motores/comparaveis.py` com `ClasseDeComparavel` (A–E e U), `TipoDeArea` e `selecionar_comparaveis` na ordem de prioridade canônica — transações realizadas; ofertas muito semelhantes e recentes no mesmo condomínio; mesma microárea; mesmo bairro; regiões próximas —, restrita aos limites de raio e janela salvo exceção registrada
    - Distinguir preço anunciado de transacionado em todo registro e cálculo, com amostra só de anunciados reduzindo a confiança; excluir erro evidente e segmento incompatível com motivo
    - Identificar outliers por critério declarado (`CMP-012`) e registrar, para cada um, a decisão de excluir ou ajustar com justificativa; outlier repetido abre pendência de hipótese de submercado distinto
    - _Requisitos: 21.1, 21.2, 21.3, 21.4, 21.5, 21.6, 21.7_

  - [ ] 7.2 Aplicar ajustes e preço por metro quadrado
    - Implementar `aplicar_ajustes` e `preco_por_m2`, com o tipo de área explícito nas duas pontas; tipo de área desconhecido no imóvel ou no comparável abre pendência e reduz a confiança do valuation
    - _Requisitos: 21.8, 21.9, 21.10, 21.11, 21.12_

  - [ ] 7.3 Calcular a confiança do valuation pela amostra
    - Implementar `confianca_do_valuation` a partir da quantidade, da qualidade e da dispersão dos comparáveis, com o limiar único de comparáveis ideais (`VAL-011`); registrar metodologia aplicada, amostra utilizada, ajustes realizados e premissas assumidas
    - _Requisitos: 22.1, 22.2, 22.3, 22.4, 22.5, 22.6, 22.7, 22.8_

  - [ ] 7.4 Emitir as quatro faixas de valor
    - Criar `src/radar/motores/valuation.py` com `avaliar_valor` produzindo conservador, base, otimista e venda rápida, cada um com confiança e método próprios
    - A avaliação da fonte permanece em campo próprio, informativa, sem nenhum caminho de atribuição ao valor de mercado; avaliação da fonte acima do valor otimista da amostra registra divergência como evidência e abre pendência
    - _Requisitos: 23.1, 23.2, 23.3, 23.4, 23.5, 23.6, 23.7, 23.8_

  - [ ] 7.5 Implementar os métodos de valuation por tipo de ativo
    - Implementar `MetodoDeValuation` com o método adequado a terreno, casa, apartamento e demais perfis, registrando qual método foi aplicado em cada referência de valor emitida
    - _Requisitos: 24.1, 24.2, 24.3, 24.4, 24.5, 24.6, 24.7, 24.8_

  - [ ] 7.6 Implementar os gatilhos de revaluation
    - Implementar os gatilhos que reestimam o valor quando o mercado, a amostra ou a evidência mudam, sem que nova evidência de preço implique necessariamente recalcular o valor de mercado
    - _Requisitos: 25.1, 25.2, 25.3, 25.4, 25.5_

  - [ ]* 7.7 Escrever testes dirigidos de comparáveis e métodos de valuation
    - Cobrir os ramos de seleção de comparáveis, o tratamento de outliers, a amostra só de anunciados e a escolha de método por tipo de ativo, com exemplos fixos e resultado esperado declarado
    - _Requisitos: 21.1, 21.6, 22.3, 24.2, 24.3, 24.4, 24.5_

- [ ] 8. Economia, preço máximo e cenários (bloco 1.6)

  - [ ] 8.1 Reconstruir o custo econômico total com treze componentes
    - Reescrever `ComposicaoDeCusto` em `src/radar/motores/calculo.py` com exatamente treze componentes, cada um `Informado[Decimal]`, e `total` como soma exata dos treze
    - Manter **fora** do custo econômico total os custos de saída e o imposto sobre ganho, e o custo de oportunidade do capital; componente `DESCONHECIDO` propaga contingência e marca o preço máximo como provisório, nunca vale zero
    - _Requisitos: 26.1, 26.1.1, 26.1.2, 26.2, 26.3, 26.4, 26.5, 26.7, 26.8, 26.9, 26.10, 26.11, 26.12_

  - [ ]* 8.2 Escrever teste de propriedade para a conservação de valor no custo
    - **Property 43: Conservação de valor no custo econômico total (`P6.1`)**
    - **Validates: Requirements 26.1, 26.11**

  - [ ]* 8.3 Escrever teste de propriedade para a monotonicidade do custo
    - **Property 44: Monotonicidade do custo econômico total (`P6.2`)**
    - **Validates: Requirements 26.1**

  - [ ] 8.4 Implementar o modelo de carregamento
    - Implementar `ModeloDeCarregamento` com `mensal_decisorio` e `mensal_pleno`, distinguindo o custo do tempo que entra no custo econômico total do que é apenas informativo
    - _Requisitos: 26.6, 30.1, 30.2, 30.3_

  - [ ] 8.5 Implementar desconto líquido e margem de segurança com bases distintas
    - Implementar `desconto_liquido` contra o valor **base** e `margem_de_seguranca_pct` contra o valor **conservador**, corrigindo a igualdade indevida entre as duas métricas
    - Valor de mercado menor ou igual a zero levanta `ErroDePreCondicao` e todas as métricas dependentes sinalizam erro
    - _Requisitos: 27.1, 27.2, 27.3, 27.4, 27.5, 27.16_

  - [ ]* 8.6 Escrever teste de propriedade para a monotonicidade do desconto líquido
    - **Property 45: Monotonicidade do desconto líquido (`P6.3`)**
    - **Validates: Requirements 27.3**

  - [ ]* 8.7 Escrever teste de propriedade para a monotonicidade da margem
    - **Property 46: Monotonicidade da margem (`P6.4`)**
    - **Validates: Requirements 27.4, 27.5**

  - [ ]* 8.8 Escrever teste de propriedade para a identidade desconto-margem
    - **Property 47: Identidade metamórfica desconto-margem (`P6.5`)**
    - **Validates: Requirements 27.3, 27.5**

  - [ ] 8.9 Implementar aluguel líquido, imposto e yields
    - Implementar `aluguel_liquido`, `base_de_ir_do_aluguel`, `ir_sobre_aluguel` e `yield_liquido_mensal`, com o piso decisório de renda incidindo sobre o **líquido** e o yield bruto permanecendo informativo
    - _Requisitos: 27.6, 27.7, 27.7.1, 27.8_

  - [ ]* 8.10 Escrever teste de propriedade para a consistência entre yields
    - **Property 48: Consistência entre yields mensal e anual (`P6.6`)**
    - **Validates: Requirements 27.6, 27.8**

  - [ ]* 8.11 Escrever teste de propriedade para a relação entre yield líquido e bruto
    - **Property 49: Yield líquido nunca excede o bruto (`P6.7`)**
    - **Validates: Requirements 27.7, 27.8**

  - [ ]* 8.12 Escrever teste de propriedade para a monotonicidade do yield
    - **Property 50: Monotonicidade do yield (`P6.8`)**
    - **Validates: Requirements 27.6, 27.8**

  - [ ] 8.13 Implementar venda líquida, base de imposto, lucro e retorno
    - Implementar venda líquida, base de imposto de renda na venda que nunca é negativa, lucro líquido, retorno líquido e retorno anualizado, todos determinísticos e sem entrada e saída de dados
    - _Requisitos: 27.9, 27.10, 27.11, 27.12, 27.13, 27.15, 27.17_

  - [ ]* 8.14 Escrever teste de propriedade para a base do imposto
    - **Property 51: Base do imposto nunca é negativa (`P6.9`)**
    - **Validates: Requirements 27.10**

  - [ ]* 8.15 Escrever teste de propriedade para valor de mercado não positivo
    - **Property 52: Valor de mercado não positivo sinaliza erro (`P6.10`)**
    - **Validates: Requirements 27.16**

  - [ ]* 8.16 Escrever teste de propriedade para o determinismo das métricas
    - **Property 53: Determinismo das métricas econômicas (`P6.11`)**
    - **Validates: Requirements 27.17**

  - [ ] 8.17 Implementar o break-even de saída
    - Implementar `break_even_de_saida` a partir do custo econômico total e do percentual de custo de venda, e a distância do break-even ao preço atual
    - _Requisitos: 27.14_

  - [ ]* 8.18 Escrever teste de propriedade para o break-even
    - **Property 54: Break-even zera o lucro líquido (`P6.12`)**
    - **Validates: Requirements 27.14**

  - [ ] 8.19 Implementar a forma fechada do preço máximo com ITBI
    - Implementar `EntradasDePrecoMaximo` e `preco_maximo_por_roi_alvo` com o ITBI no coeficiente proporcional, e a pré-condição algébrica `1 + r − t > 0` que levanta `ErroDePreCondicao` em lugar de devolver valor
    - Implementar a **verificação inversa** como pré-condição de aceite: usar o preço máximo como preço de aquisição reproduz o retorno alvo dentro de 10⁻⁶
    - Implementar `preco_maximo_com_reserva_proporcional` para o caso da reserva proporcional ao custo
    - _Requisitos: 28.1, 28.2, 28.2.1, 28.3_

  - [ ]* 8.20 Escrever teste de propriedade para a propriedade inversa do preço máximo
    - **Property 55: Propriedade inversa do preço máximo (`P7.1`)**
    - **Validates: Requirements 28.2, 28.3**

  - [ ]* 8.21 Escrever teste de propriedade para a monotonicidade no retorno alvo
    - **Property 56: Monotonicidade decrescente no ROI alvo (`P7.2`)**
    - **Validates: Requirements 28.2**

  - [ ]* 8.22 Escrever teste de propriedade para a monotonicidade nos custos fixos
    - **Property 57: Monotonicidade decrescente nos custos fixos (`P7.3`)**
    - **Validates: Requirements 28.2**

  - [ ]* 8.23 Escrever teste de propriedade para a monotonicidade no valor de saída
    - **Property 58: Monotonicidade crescente no valor de saída (`P7.4`)**
    - **Validates: Requirements 28.2**

  - [ ]* 8.24 Escrever teste de propriedade para o sinal do preço máximo
    - **Property 59: Preço máximo nunca é negativo (`P7.5`)**
    - **Validates: Requirements 28.2**

  - [ ]* 8.25 Escrever teste de propriedade para a monotonicidade no ITBI
    - **Property 65: Monotonicidade decrescente no ITBI (`P7.11`)**
    - **Validates: Requirements 28.2, 28.2.1**

  - [ ] 8.26 Implementar o teto conservador informativo e o teto decisório
    - Implementar `preco_maximo_conservador_do_metodo` rotulado como **referência informativa**, nunca como teto decisório, e `teto_decisorio` como o mínimo entre o preço máximo exato e o ajustado ao risco
    - _Requisitos: 28.4, 28.4.1, 28.4.2_

  - [ ]* 8.27 Escrever teste de propriedade para o teto decisório
    - **Property 64: Teto decisório é o mínimo dos dois (`P7.10`)**
    - **Validates: Requirements 28.4.2**

  - [ ]* 8.28 Escrever teste dirigido do contraexemplo do teto conservador
    - Entradas fixas com valor de saída 300.000, custo de venda 0,06, custos fixos 23.000, custo de aquisição 0,05, retorno alvo 0,25, imposto 0 e ITBI 0; conservador 199.230,77 e exato 192.952,38, com a diferença de R$ 6.278,39 verificada (`REG-033`). É contraexemplo, não propriedade
    - _Requisitos: 28.4, 28.4.1_

  - [ ] 8.29 Implementar o preço máximo ajustado ao risco e o preço-alvo
    - Implementar `preco_maximo_ajustado_ao_risco`, que nunca excede o econômico, e `preco_alvo`, que nunca excede o preço máximo para folga não negativa
    - _Requisitos: 28.9, 28.10, 28.12_

  - [ ]* 8.30 Escrever teste de propriedade para o teto ajustado ao risco
    - **Property 60: Ajustado ao risco nunca excede o econômico (`P7.6`)**
    - **Validates: Requirements 28.9**

  - [ ]* 8.31 Escrever teste de propriedade para o preço-alvo
    - **Property 62: Preço-alvo nunca excede o preço máximo (`P7.8`)**
    - **Validates: Requirements 28.12**

  - [ ] 8.32 Implementar os demais tetos por estratégia
    - Implementar `preco_maximo_por_yield_liquido`, `preco_maximo_por_valor_futuro`, `preco_maximo_por_publico_alvo` e `preco_maximo_por_potencial_de_uso`, cada um com a estratégia e as premissas declaradas
    - _Requisitos: 28.5, 28.6, 28.7, 28.8_

  - [ ] 8.33 Tratar liquidez indefinida e oferta acima do teto
    - Não emitir preço máximo definitivo quando a liquidez está indefinida, e emitir `NAO_COMPRAR` para a estratégia quando a oferta está acima do teto ajustado, com a pendência determinante nomeada
    - _Requisitos: 28.11, 28.13, 28.14, 28.15, 28.16, 33.2_

  - [ ]* 8.34 Escrever teste de propriedade para liquidez indefinida
    - **Property 63: Liquidez indefinida impede teto definitivo (`P7.9`)**
    - **Validates: Requirements 28.11**

  - [ ]* 8.35 Escrever teste de propriedade para oferta acima do teto
    - **Property 61: Oferta acima do teto implica NAO_COMPRAR (`P7.7`)**
    - **Validates: Requirements 28.13, 33.2**

  - [ ] 8.36 Implementar reforma, contingência e regularização
    - Criar `src/radar/motores/reforma.py` com `NivelDeReforma`, `EstimativaEmFaixa`, `custo_de_reforma` e `suspeita_estrutural`: orçamento desconhecido permanece em faixa com estado de informação, nunca vira número único; suspeita estrutural abre diligência e não é tratada como custo zero
    - _Requisitos: 29.1, 29.2, 29.3, 29.4, 29.5, 29.6, 29.7, 29.8, 29.9, 29.10, 29.11_

  - [ ] 8.37 Implementar capital imobilizado e custo do tempo
    - Implementar `metricas_de_capital` com capital imobilizado, prazo, custo do tempo e retorno anualizado comparado ao retorno mínimo exigido, sem cobrar o retorno exigido duas vezes
    - _Requisitos: 30.4, 30.5, 30.6, 30.7, 30.8, 30.9_

  - [ ] 8.38 Construir os quatro cenários e a grade de sensibilidade
    - Criar `src/radar/motores/cenarios.py` com `TipoDeCenario`, `Robustez`, `GRADE_DE_SENSIBILIDADE` e `construir_cenarios` produzindo otimista, base, conservador e estressado, cada um com custo econômico total, margem, retorno e prazo próprios
    - Classificar a robustez de forma total e consistente com os resultados; tese que sobrevive ao estressado sobrevive a todos
    - _Requisitos: 32.1, 32.2, 32.3, 32.4, 32.5, 32.6, 32.7, 32.8, 32.9, 32.10, 32.11_

  - [ ]* 8.39 Escrever teste de propriedade para a ordenação de cenários
    - **Property 66: Ordenação de cenários (`P8.1`)**
    - **Validates: Requirements 32.1, 32.2, 32.3, 32.4**

  - [ ]* 8.40 Escrever teste de propriedade para a sobrevivência ao estressado
    - **Property 67: Sobreviver ao estressado implica sobreviver a todos (`P8.2`)**
    - **Validates: Requirements 32.6**

  - [ ]* 8.41 Escrever teste de propriedade para a classificação de robustez
    - **Property 68: Classificação de robustez é total e consistente (`P8.3`)**
    - **Validates: Requirements 32.6**

  - [ ] 8.42 Implementar as regras de decisão econômica e os limites de break-even
    - Implementar `avaliar_regras_economicas` e `limites_de_break_even`, com os pisos de desconto líquido, margem, yield líquido e retorno por estratégia, e a distância do break-even que aciona `MONITORAR`
    - _Requisitos: 33.1, 33.3, 33.4, 33.5, 33.6, 33.7, 33.7.1, 33.8, 33.9, 33.10_

  - [ ] 8.43 Compor os componentes de débito do custo econômico total
    - Implementar `compor_componentes_de_debito` alimentando `CUS-005` e `CUS-006` a partir dos débitos registrados um a um; tipo exigido pelo checklist e não investigado permanece `DESCONHECIDO`, nunca zero
    - _Requisitos: 91.3, 91.5, 91.6, 26.1_

  - [ ] 8.44 Implementar as fórmulas da visão financeira oficial
    - Implementar `visao_financeira_oficial` com as catorze grandezas e a decomposição em treze componentes, reproduzindo a **estrutura** e a **rastreabilidade** da planilha de viabilidade de referência, e não a sua aritmética onde ela foi verificadamente corrigida
    - _Requisitos: 96.2, 96.3, 96.4, 96.5_

- [ ] 9. Checkpoint — economia, preço máximo e cenários
  - Executar a suíte inteira, `ruff` e `mypy --strict`; confirmar que o preço máximo satisfaz a própria definição na verificação inversa, que o custo econômico total tem treze componentes sem dupla contagem e que nenhum componente desconhecido é tratado como zero. Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 10. Risco, liquidez, estratégia, portfólio, escore e ranqueamento (bloco 1.7)

  - [ ] 10.1 Declarar a matriz de severidade e o registro de risco
    - Criar `src/radar/motores/risco.py` com `CategoriaDeRisco`, `Probabilidade`, `Impacto`, `Severidade`, `MATRIZ_DE_SEVERIDADE` declarada como dado sobre as doze combinações, `Mitigacao` e `RegistroDeRisco` com categoria, probabilidade, impacto, exposição de capital, incerteza, mitigabilidade, prazo potencial, estado de informação, severidade e mitigação
    - Severidade e confiança são dimensões independentes; a estratégia de mitigação `aceitar` exige exceção registrada com justificativa, evidência, limite e prazo
    - _Requisitos: 34.1, 34.2, 34.3, 34.4, 34.6, 34.7, 34.8, 34.10, 34.11_

  - [ ]* 10.2 Escrever teste de propriedade para a totalidade da severidade
    - **Property 69: Severidade é total sobre probabilidade e impacto (`P8.4`)**
    - **Validates: Requirements 34.3, 34.4**

  - [ ]* 10.3 Escrever teste de propriedade para a monotonicidade da severidade
    - **Property 70: Monotonicidade da severidade (`P8.5`)**
    - **Validates: Requirements 34.4**

  - [ ] 10.4 Implementar o bloqueio por risco crítico e a categoria não investigada
    - Implementar `bloqueio_critico`, que produz bloqueio para qualquer estado de informação, e a condição objetiva de desbloqueio obrigatória quando a evidência é `ESTIMADO` ou `INFERIDO`
    - Implementar `nao_investigada`, que devolve risco `DESCONHECIDO` para categoria não investigada, nunca `baixo`
    - _Requisitos: 34.5, 34.5.1, 34.5.2, 34.9, 12.3_

  - [ ]* 10.5 Escrever teste de propriedade para o bloqueio por risco crítico
    - **Property 71: Risco crítico sempre bloqueia (`P8.6`)**
    - **Validates: Requirements 34.5, 34.5.2, 12.3**

  - [ ]* 10.6 Escrever teste de propriedade para categoria não investigada
    - **Property 72: Categoria não investigada resulta em DESCONHECIDO (`P8.7`)**
    - **Validates: Requirements 34.9**

  - [ ]* 10.7 Escrever teste de propriedade para o bloqueio presumido
    - **Property 73: Bloqueio presumido traz condição de desbloqueio (`P8.8`)**
    - **Validates: Requirements 34.5.1**

  - [ ] 10.8 Separar risco de incerteza
    - Implementar `margem_exigida` por severidade e nível de confiança e `efeito_da_incerteza`, que converte dado desconhecido em restrição de decisão em lugar de risco baixo
    - _Requisitos: 35.1, 35.2, 35.3, 35.4, 35.5, 35.6_

  - [ ] 10.9 Implementar as sete faixas de liquidez e o escore de liquidez
    - Criar `src/radar/motores/liquidez.py` com `CategoriaDeLiquidez`, `FAIXAS_DE_LIQUIDEZ` com exatamente **sete** faixas contínuas e sem lacuna, `PESOS_DE_LIQUIDEZ` somando 1,00 e `escores_de_liquidez` para venda e locação
    - Usar `classificar_por_faixa` como função única de faixa, de modo que 39,5 · 49,5 · 59,5 · 69,5 · 79,5 · 89,5 tenham categoria definida
    - _Requisitos: 40.1, 40.2, 40.3, 40.4, 40.5, 40.6, 40.9, 40.10, 40.11_

  - [ ]* 10.10 Escrever teste de propriedade para as sete faixas de liquidez
    - **Property 74: Sete faixas de liquidez contínuas e sem lacuna (`P9.1`)**
    - **Validates: Requirements 40.2**

  - [ ]* 10.11 Escrever teste de propriedade para a escala do escore de liquidez
    - **Property 75: Escore de liquidez permanece na escala (`P9.2`)**
    - **Validates: Requirements 40.1, 40.3**

  - [ ]* 10.12 Escrever teste de propriedade para a monotonicidade do escore de liquidez
    - **Property 76: Monotonicidade do escore de liquidez (`P9.3`)**
    - **Validates: Requirements 40.3**

  - [ ] 10.13 Implementar a decisão por liquidez
    - Implementar `decisao_por_liquidez` com o limiar da estratégia resolvido pelo Gestor de Parâmetros e a exceção formal exigida abaixo do limiar de `R40.8`
    - _Requisitos: 40.7, 40.8_

  - [ ]* 10.14 Escrever teste de propriedade para liquidez abaixo do mínimo
    - **Property 77: Liquidez abaixo do mínimo nunca resulta em COMPRAR (`P9.4`)**
    - **Validates: Requirements 40.7**

  - [ ] 10.15 Implementar preço e prazo de saída
    - Implementar `margem_adicional_por_prazo`, `margem_exigida_com_liquidez` e `precos_de_saida` por público-alvo, com a margem adicional monotônica no prazo estimado
    - _Requisitos: 41.1, 41.2, 41.3, 41.4, 41.5, 41.6, 41.7, 41.8, 30.7_

  - [ ]* 10.16 Escrever teste de propriedade para a margem adicional por prazo
    - **Property 78: Margem adicional monotônica no prazo (`P9.5`)**
    - **Validates: Requirements 41.4, 30.7**

  - [ ] 10.17 Separar estratégia de perfil de ativo
    - Criar `src/radar/motores/estrategia.py` com `Estrategia` de **seis** valores, incluindo `customizada`, e `PerfilDeAtivo` de **nove** valores, incluindo `desconhecido`, que não herda critérios de nenhum perfil, abre pendência de classificação e reduz a confiança
    - Declarar `LimitesDaEstrategia` **gerado** a partir da tabela `STR`, `PARAMETROS_PROPRIOS_DA_ESTRATEGIA` e `resolver_ticket_maximo`, em que o ticket da estratégia prevalece sobre o do perfil do investidor quando declarado
    - Implementar `avaliar_estrategias` com aderência, critérios atendidos, critérios não atendidos, parâmetros aplicados, limites vigentes e veredicto por estratégia avaliada
    - _Requisitos: 44.1, 44.2, 44.3, 44.4, 44.5, 44.6, 44.7, 44.8, 44.9, 44.10, 45.1, 45.2, 45.3, 45.4, 45.5, 45.6, 45.7, 45.8, 45.9, 45.10, 45.11, 45.12, 45.13, 45.14, 45.15, 45.16, 45.17, 45.18_

  - [ ] 10.18 Implementar capital, reserva e limite por operação
    - Criar `src/radar/motores/portfolio.py` com `VisaoDeCapital`, `reserva_aplicavel` resolvendo reserva absoluta e percentual, `limite_por_operacao` e `eficiencia_de_capital`
    - _Requisitos: 46.1, 46.2, 46.3, 46.4, 46.5, 46.6, 46.6.1, 46.7, 46.8, 46.9_

  - [ ] 10.19 Implementar concentração e diversificação
    - Implementar `concentracao` sobre as posições de portfólio, com os limites de concentração e o desvio em relação à alocação-alvo, e a exigência de que a concentração entre na decisão por um único caminho
    - _Requisitos: 47.1, 47.2, 47.3, 47.4, 47.4.1, 47.5, 47.6_

  - [ ] 10.20 Implementar o escore de oportunidade
    - Criar `src/radar/motores/escore.py` com `PESOS_DE_OPORTUNIDADE` somando 1,00, `PESOS_POR_ESTRATEGIA` com as cinco colunas somando 1,00 e `qualidade_oportunidade` estritamente positiva em todas, e `escore_de_oportunidade`
    - Rejeitar conjunto de pesos cuja soma difira de 1,00 **na carga da configuração**; registrar a contribuição individual de cada fator, cuja soma é igual ao escore, a versão dos pesos e qual conjunto foi aplicado
    - Dados mínimos ausentes fazem o motor **abster-se** de emitir escore e registrar escore indefinido; nunca emitir zero
    - _Requisitos: 49.1, 49.2, 49.3, 49.4, 49.5, 49.6, 49.7, 49.8, 49.9_

  - [ ]* 10.21 Escrever teste de propriedade para a soma dos pesos
    - **Property 79: Todo conjunto de pesos soma 1,00 (`P10.1`)**
    - **Validates: Requirements 49.5**

  - [ ]* 10.22 Escrever teste de propriedade para a escala do escore de oportunidade
    - **Property 80: EscoreDeOportunidade permanece na escala (`P10.2`)**
    - **Validates: Requirements 49.1, 49.2**

  - [ ]* 10.23 Escrever teste de propriedade para a monotonicidade do escore de oportunidade
    - **Property 81: Monotonicidade do EscoreDeOportunidade (`P10.3`)**
    - **Validates: Requirements 49.2**

  - [ ]* 10.24 Escrever teste de propriedade para as contribuições por fator
    - **Property 82: Contribuições somam o escore (`P10.4`)**
    - **Validates: Requirements 49.7**

  - [ ]* 10.25 Escrever teste de propriedade para as faixas de escore
    - **Property 92: Cobertura total das faixas de escore (`P10.14`)**
    - **Validates: Requirements 49.6**

  - [ ]* 10.26 Escrever teste de propriedade para as colunas de pesos por estratégia
    - **Property 96: Colunas por estratégia somam 1,00 com qualidade positiva (`P10.18`)**
    - **Validates: Requirements 49.5, 49.2**

  - [ ] 10.27 Implementar a confiança consolidada versionada
    - Implementar `confianca_consolidada` a partir de `CONF-001` a `CONF-005`, determinística, versionada e reproduzível, e `FAIXAS_DO_FATOR_DE_CONFIANCA` com cinco faixas contínuas e monotônicas não decrescentes
    - Dimensão obrigatória desconhecida ou conflitante resulta em `inconclusiva`, que é estado e não faixa numérica; a confiança nunca é usada para contornar camada de bloqueio
    - _Requisitos: 50.1, 50.2, 50.3, 50.4, 50.5, 50.5.1, 50.6, 50.7_

  - [ ]* 10.28 Escrever teste de propriedade para o fator de confiança
    - **Property 93: Cobertura total do fator de confiança (`P10.15`)**
    - **Validates: Requirements 50.3, 50.4**

  - [ ] 10.29 Implementar o escore de aderência com sete componentes
    - Declarar `PESOS_DE_ADERENCIA` com exatamente sete componentes e os pesos 0,27 · 0,20 · 0,13 · 0,13 · 0,13 · 0,07 · 0,07, somando 1,00, e implementar o `EscoreDeAderencia`
    - Nenhum componente de qualidade econômica participa do escore de aderência; a aderência nunca converte bloqueio em compra
    - _Requisitos: 51.1, 51.1.1, 51.2, 51.3, 51.4, 51.5, 51.6, 12.3_

  - [ ]* 10.30 Escrever teste de propriedade para a escala do escore de aderência
    - **Property 83: EscoreDeAderencia permanece na escala (`P10.5`)**
    - **Validates: Requirements 51.1**

  - [ ]* 10.31 Escrever teste de propriedade para a aderência diante de bloqueio
    - **Property 84: EscoreDeAderencia nunca converte BLOQUEAR em COMPRAR (`P10.6`)**
    - **Validates: Requirements 51.4, 12.3**

  - [ ]* 10.32 Escrever teste de propriedade para os sete pesos de aderência
    - **Property 95: Sete pesos de aderência, sem qualidade econômica (`P10.17`)**
    - **Validates: Requirements 51.1, 51.1.1**

  - [ ] 10.33 Implementar o escore de prioridade com cinco fatores
    - Implementar `escore_de_prioridade` como produto de exatamente **cinco** fatores, cada um normalizado em `[0, 1]`, com o ajuste de portfólio composto apenas do bônus e da penalidade declarados
    - Declarar `PESOS_DO_ESCORE_ECONOMICO` somando 100 como indicador auxiliar, sem efeito decisório
    - _Requisitos: 52.1, 52.1.1, 52.2_

  - [ ]* 10.34 Escrever teste de propriedade para a monotonicidade do escore de prioridade
    - **Property 85: Monotonicidade do escore de prioridade (`P10.7`)**
    - **Validates: Requirements 52.1, 52.2**

  - [ ]* 10.35 Escrever teste de propriedade para o caminho único da concentração
    - **Property 97: Concentração entra por um único caminho (`P10.19`)**
    - **Validates: Requirements 52.1, 52.1.1, 47.4.1**

  - [ ] 10.36 Implementar o ranqueamento determinístico
    - Criar `src/radar/motores/ranqueamento.py` com `ranquear` e `ORDEM_DE_DESEMPATE` de oito critérios, produzindo ordem total, antissimétrica, transitiva, confluente e idempotente
    - Excluir do ranqueamento operacional toda oportunidade com decisão de bloqueio; registrar versão dos pesos e das regras com data e hora e preservar o histórico de posições
    - Identificar as oportunidades que competem pelo mesmo capital e destacar o conjunto não dominado
    - _Requisitos: 52.3, 52.4, 52.4.1, 52.5, 52.7, 52.8, 52.9, 52.11, 52.12_

  - [ ]* 10.37 Escrever teste de propriedade para a ordem total do ranqueamento
    - **Property 86: Ranqueamento é ordem total (`P10.8`)**
    - **Validates: Requirements 52.4**

  - [ ]* 10.38 Escrever teste de propriedade para a confluência do ranqueamento
    - **Property 87: Confluência do ranqueamento (`P10.9`)**
    - **Validates: Requirements 52.4**

  - [ ]* 10.39 Escrever teste de propriedade para a consistência com o escore
    - **Property 88: Consistência do ranqueamento com o escore (`P10.10`)**
    - **Validates: Requirements 52.4**

  - [ ]* 10.40 Escrever teste de propriedade para o determinismo do desempate
    - **Property 89: Determinismo do desempate (`P10.11`)**
    - **Validates: Requirements 52.4**

  - [ ]* 10.41 Escrever teste de propriedade para a exclusão dos bloqueados
    - **Property 90: Bloqueados não aparecem no ranqueamento (`P10.12`)**
    - **Validates: Requirements 52.3**

  - [ ]* 10.42 Escrever teste de propriedade para a idempotência do ranqueamento
    - **Property 91: Idempotência do ranqueamento (`P10.13`)**
    - **Validates: Requirements 52.4**

  - [ ] 10.43 Implementar urgência, atratividade e explicação de posição
    - Declarar `ClasseDeUrgencia` com `P0` a `P4` mais bloqueio e `ClasseDeAtratividade` com `A1` a `A5`, sem nenhum rótulo compartilhado entre as duas escalas, e implementar `explicar_posicao` com as seis respostas obrigatórias
    - _Requisitos: 52.6, 52.6.1, 52.10_

  - [ ]* 10.44 Escrever teste de propriedade para as escalas disjuntas
    - **Property 98: Escalas de urgência e atratividade são disjuntas (`P10.20`)**
    - **Validates: Requirements 52.6, 52.6.1**

- [ ] 11. Decisão de onze camadas, catálogo de regras e explicabilidade (bloco 1.8)

  - [ ] 11.1 Redefinir a entrada da decisão sem nenhum default
    - Reescrever `EntradaDeDecisao` em `src/radar/motores/decisao.py` com todos os campos obrigatórios e **nenhum** default: bloqueios críticos, situação jurídica, identidade, elegibilidade, confiança consolidada, confiança do valuation, pendências, métricas econômicas, robustez, avaliação de estratégia, riscos, liquidez, escore de oportunidade, escore de aderência, veredicto de capital, posição no ranqueamento e exceções
    - Declarar `CamadaDeDecisao` com **onze** valores, de 0 a 10, e manter a decisão final como **saída**, nunca como camada
    - _Requisitos: 53.1, 53.1.1, 12.8_

  - [ ]* 11.2 Escrever teste de propriedade para as onze camadas
    - **Property 114: Onze camadas e a decisão não é camada (`P11.16`)**
    - **Validates: Requirements 53.1, 53.1.1**

  - [ ]* 11.3 Escrever teste de propriedade para situação jurídica pendente
    - **Property 103: PENDENTE nunca resulta em COMPRAR (`P11.5`)**
    - **Validates: Requirements 12.8**

  - [ ] 11.4 Implementar a função de decisão com curto-circuito por camada
    - Implementar `decidir` como função pura que avalia as camadas em ordem, emite exatamente um dos estados de decisão, reporta a camada determinante como a de **menor índice** entre as eliminatórias e impede que camada posterior altere resultado de camada anterior
    - _Requisitos: 53.1, 53.2, 53.3, 53.4, 53.5, 53.6_

  - [ ]* 11.5 Escrever teste de propriedade para a totalidade da decisão
    - **Property 99: Totalidade da decisão (`P11.1`)**
    - **Validates: Requirements 53.5**

  - [ ]* 11.6 Escrever teste de propriedade para a incompensabilidade do bloqueio
    - **Property 100: BLOQUEAR não é compensável (`P11.2`)**
    - **Validates: Requirements 12.3, 53.4**

  - [ ]* 11.7 Escrever teste de propriedade para a camada determinante
    - **Property 101: Camada determinante é a de menor índice (`P11.3`)**
    - **Validates: Requirements 53.1, 53.2, 53.3**

  - [ ]* 11.8 Escrever teste de propriedade para a precedência entre camadas
    - **Property 102: Camada posterior não anula camada anterior (`P11.4`)**
    - **Validates: Requirements 53.4**

  - [ ]* 11.9 Escrever teste de propriedade para o determinismo da decisão
    - **Property 110: Determinismo da decisão e da camada (`P11.12`)**
    - **Validates: Requirements 53.1**

  - [ ] 11.10 Dar conteúdo às camadas 0 a 3
    - Implementar a camada 0 alimentada pelo Motor de Risco — risco crítico, ocupação crítica sem estratégia, posse litigiosa, regra eliminatória e reserva mínima —, a camada 1 com o gate jurídico de 19 verificações, a camada 2 de elegibilidade com identidade mínima `I2`, localização, tipo e ticket, e a camada 3 de dados e confiança com o mínimo de confiança para compra e as pendências abertas
    - Pendência de prioridade crítica aberta restringe a decisão: nunca `COMPRAR` nem `NAO_COMPRAR`
    - _Requisitos: 12.3, 37.3, 50.6, 53.1_

  - [ ]* 11.11 Escrever teste de propriedade para confiança insuficiente
    - **Property 104: Confiança insuficiente nunca resulta em COMPRAR (`P11.6`)**
    - **Validates: Requirements 50.6**

  - [ ]* 11.12 Escrever teste de propriedade para pendência crítica
    - **Property 105: Pendência crítica restringe a decisão (`P11.7`)**
    - **Validates: Requirements 37.3**

  - [ ] 11.13 Dar conteúdo às camadas 4 a 7
    - Implementar a camada 4 de economia, com a robustez do conservador como **sub-verificação**, a camada 5 de estratégia, a camada 6 de risco recebendo as regras de ocupação e de localização, e a camada 7 de liquidez com o limiar próprio resolvido pelo Gestor de Parâmetros
    - _Requisitos: 53.1, 53.1.6, 33.3, 40.7_

  - [ ]* 11.14 Escrever teste de propriedade para a monotonicidade no desconto líquido
    - **Property 109: Monotonicidade da decisão no desconto líquido (`P11.11`)**
    - **Validates: Requirements 33.3**

  - [ ] 11.15 Dar conteúdo às camadas 8 a 10 e à matriz de ação
    - Implementar a camada 8 de escore, a camada 9 de capital e concentração e a camada 10 de ranqueamento, e declarar `MATRIZ_DE_ACAO` com as **15 células** do produto de faixas de escore por faixas de confiança, total e sem sobreposição
    - _Requisitos: 55.1, 55.10, 55.11, 55.12, 55.13, 55.14, 55.15, 55.16_

  - [ ]* 11.16 Escrever teste de propriedade para a totalidade da matriz
    - **Property 113: Totalidade da matriz de escore × confiança (`P11.15`)**
    - **Validates: Requirements 55.1, 55.10, 55.11, 55.12, 55.13, 55.14, 55.15, 55.16**

  - [ ] 11.17 Exigir condição objetiva e gatilho de reentrada
    - Garantir que todo `COMPRAR_SE` traga ao menos uma condição objetiva registrada e todo `MONITORAR` traga ao menos um gatilho de reentrada registrado
    - _Requisitos: 53.7, 53.8, 53.9, 53.10, 53.11_

  - [ ]* 11.18 Escrever teste de propriedade para a condição objetiva
    - **Property 106: COMPRAR_SE sempre traz condição objetiva (`P11.8`)**
    - **Validates: Requirements 53.7**

  - [ ]* 11.19 Escrever teste de propriedade para o gatilho de reentrada
    - **Property 107: MONITORAR sempre traz gatilho de reentrada (`P11.9`)**
    - **Validates: Requirements 53.8**

  - [ ] 11.20 Implementar a monotonicidade da decisão na confiança
    - Garantir que aumento de confiança, mantido o restante, nunca piore a decisão na ordem bloquear, não comprar, monitorar, comprar sob condição e comprar
    - _Requisitos: 55.1, 55.2, 55.3, 55.4, 55.5, 55.6, 55.7, 55.8, 55.9_

  - [ ]* 11.21 Escrever teste de propriedade para a monotonicidade na confiança
    - **Property 108: Monotonicidade da decisão na confiança (`P11.10`)**
    - **Validates: Requirements 55.1, 55.2, 55.3, 55.4, 55.5, 55.6, 55.7, 55.8, 55.9**

  - [ ] 11.22 Declarar o catálogo das 55 regras e a resolução de conflitos
    - Criar `src/radar/regras/catalogo.py` com `CATALOGO_DE_REGRAS` contendo as **55** regras canônicas, `TipoDeRegra` com regra dura, branda, condicional, informativa e de exceção, `PRECEDENCIA_DE_CONFLITO` e `resolver_conflito_de_escopo`
    - O escopo mais específico prevalece, **exceto** quando o menos específico impõe bloqueio crítico ou restrição legal ou documental
    - _Requisitos: 54.1, 54.2, 54.3, 54.4, 54.5, 54.6, 54.7, 54.8, 54.9, 54.10, 54.10.1, 54.11_

  - [ ]* 11.23 Escrever teste de propriedade para a precedência de escopo
    - **Property 117: Precedência de escopo (`P11.19`)**
    - **Validates: Requirements 54.10, 54.10.1**

  - [ ] 11.24 Impedir que exceção contorne bloqueio
    - Implementar a validação que levanta `ErroDeExcecaoSobreBloqueio` quando uma exceção tentaria contornar bloqueio jurídico ou risco crítico confirmado
    - _Requisitos: 63.4, 63.4.1_

  - [ ]* 11.25 Escrever teste de propriedade para exceção sobre bloqueio
    - **Property 111: Exceção não contorna bloqueio (`P11.13`)**
    - **Validates: Requirements 63.4, 63.4.1**

  - [ ] 11.26 Extrair a explicabilidade para motor próprio
    - Criar `src/radar/motores/explicabilidade.py` com `explicar`, produzindo os elementos obrigatórios da justificativa — camada determinante, regras aplicadas com versão, evidências, valores, pendências e o que mudaria a decisão — com simetria entre aprovação e rejeição
    - Toda decisão persistida referencia ao menos uma evidência e ao menos uma versão de regra
    - _Requisitos: 56.1, 56.2, 56.3, 56.4, 56.5, 56.6, 56.7, 56.8, 56.9, 61.4_

  - [ ]* 11.27 Escrever teste de propriedade para a rastreabilidade da decisão
    - **Property 112: Rastreabilidade da decisão (`P11.14`)**
    - **Validates: Requirements 56.8, 61.4**

- [ ] 12. Checkpoint — motor de decisão
  - Executar a suíte inteira, `ruff` e `mypy --strict`; confirmar que as onze camadas têm conteúdo, que a camada determinante é a de menor índice entre as eliminatórias e que nenhuma combinação de escore, desconto, margem, yield, liquidez, aderência ou eficiência de capital supera um bloqueio. Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 13. Diligência, análise profunda e disciplina de lance (bloco 1.9)

  - [ ] 13.1 Declarar os 234 itens de checklist como dados
    - Criar `src/radar/diligencia/catalogo.py` com `ItemDeChecklist` e `CHECKLIST_PADRAO_VERSAO_1` declarando os **234** itens dos Anexos A, B e C.1 — `MC-001` a `MC-136`, `B-01` a `B-27` e `C-01` a `C-71` —, cada um com código de regra, filtro de aplicabilidade, peso, severidade, ordem, condição de aprovação, condição de reprovação, resultado na ausência, prioridade na ausência, criticidade e fase
    - Declarar `FaseDeDiligencia` e a ordem obrigatória das fases; os itens são enumeráveis em tempo de execução, para que a cobertura seja verificável
    - _Requisitos: 36.1, 36.2, 36.4, 36.5, 36.6, 36.7_

  - [ ] 13.2 Implementar o resultado por item e a ausência de evidência
    - Implementar `ResultadoDeItemDeChecklist` com os seis resultados possíveis, mantendo ausência de evidência e evidência de ausência como resultados **distintos**, e `nao_aplicavel` exigindo justificativa
    - Ausência de evidência produz pendência ou resultado mais restritivo, nunca reprovação por irregularidade nem liberação
    - _Requisitos: 36.3, 36.3.1, 36.3.2_

  - [ ]* 13.3 Escrever teste de propriedade para ausência de evidência no checklist
    - **Property 115: Ausência de evidência nunca produz resultado favorável (`P11.17`)**
    - **Validates: Requirements 36.3.1, 36.3.2**

  - [ ] 13.4 Implementar o gestor de pendências
    - Criar `src/radar/diligencia/pendencias.py` com `PrioridadeDePendencia`, `GestorDePendencias.abrir` e `.resolver` — que preserva o registro — e `efeito_das_pendencias_na_decisao`
    - Pendência resolvida dispara o recálculo de confiança, escore de oportunidade, escore de aderência e ranqueamento pelo gatilho `MON-011`
    - _Requisitos: 37.1, 37.2, 37.3, 37.4, 37.5, 37.6, 37.7, 37.8, 37.9_

  - [ ] 13.5 Implementar o registro de visita física
    - Implementar `registrar_visita`, que converte o relatório de visita em evidências com proveniência, localização e data de observação, sem promover fato desconhecido
    - _Requisitos: 38.1, 38.2, 38.3, 38.4, 38.5, 38.6_

  - [ ] 13.6 Implementar o contexto humano e o conforto pessoal
    - Implementar `contexto_humano`, que produz veredicto sobre esforço operacional, conforto e restrições do investidor, sem alterar nenhuma camada eliminatória
    - _Requisitos: 39.1, 39.2, 39.3, 39.4, 39.5, 39.6_

  - [ ] 13.7 Implementar a análise profunda com as oito respostas obrigatórias
    - Criar `src/radar/motores/analise_profunda.py` com `PERGUNTAS_DA_ANALISE_PROFUNDA`, `AnaliseProfunda` — tese, argumentos a favor, argumentos contra, contrapontos e as **oito** respostas — e `gate_da_analise_profunda`, versionada sem sobrescrita
    - _Requisitos: 76.1, 76.2, 76.3, 76.4, 76.5, 76.6, 76.7, 76.8_

  - [ ] 13.8 Implementar cenários derivados como hipótese
    - Implementar `derivar_cenario`, que marca o cenário derivado como hipótese com autor, data e motivo, sem convertê-lo em evidência nem em cenário canônico
    - _Requisitos: 77.1, 77.2, 77.3, 77.4, 77.5, 77.6_

  - [ ] 13.9 Declarar as paradas absolutas e as listas de verificação de lance
    - Criar `src/radar/motores/disciplina_de_lance.py` com `PARADAS_ABSOLUTAS` (`HS-01` a `HS-09`), `VERIFICACOES_PRE_LANCE` (`PL-01` a `PL-12`), `VERIFICACOES_DE_EVICCAO` (`E01` a `E09`), `REVALIDACAO_FINAL` (`RL-01` a `RL-12`) e `HISTORICO_DO_LEILOEIRO` (`HL-01` a `HL-06`), todas declaradas como dados
    - _Requisitos: 82.1, 82.2, 82.3, 82.4, 82.5_

  - [ ]* 13.10 Escrever teste de propriedade para a liberação pré-lance
    - **Property 133: Liberação pré-lance é bicondicional (`P14.1`)**
    - **Validates: Requirements 82.3, 82.6**

  - [ ]* 13.11 Escrever teste de propriedade para parada absoluta acionada
    - **Property 134: Parada absoluta acionada impede o lance (`P14.2`)**
    - **Validates: Requirements 82.1, 82.2**

  - [ ]* 13.12 Escrever teste de propriedade para a liberação final
    - **Property 137: Liberação final exige as duas listas (`P14.5`)**
    - **Validates: Requirements 82.5, 82.6**

  - [ ] 13.13 Implementar a liberação de lance e o custo total de aquisição
    - Implementar `DisciplinaDeLance`, `liberacao_de_lance` e `custo_total_de_aquisicao`, em que a comissão do leiloeiro **soma** ao lance e nunca é subtraída; lance acima do teto absoluto e divergência documental pendente impedem o lance
    - Evicção não confirmada impede o lance tanto na ausência comprovada quanto na não verificação; a liberação é ato registrado com autor, papel e data
    - _Requisitos: 82.6, 82.7, 82.8, 82.9, 82.10, 15.9, 15.9.1_

  - [ ]* 13.14 Escrever teste de propriedade para lance acima do teto
    - **Property 135: Lance acima do teto absoluto impede o lance (`P14.3`)**
    - **Validates: Requirements 82.6**

  - [ ]* 13.15 Escrever teste de propriedade para evicção não confirmada no lance
    - **Property 136: Evicção não confirmada impede o lance (`P14.4`)**
    - **Validates: Requirements 82.4, 15.9, 15.9.1**

  - [ ]* 13.16 Escrever teste de propriedade para divergência pendente
    - **Property 138: Divergência pendente impede o lance (`P14.6`)**
    - **Validates: Requirements 82.9, 82.10**

  - [ ]* 13.17 Escrever teste de propriedade para a comissão do leiloeiro
    - **Property 139: Comissão nunca é subtraída do lance (`P14.7`)**
    - **Validates: Requirements 82.7**

- [ ] 14. Orquestração, fronteiras da IA, supervisão e controle de escopo (bloco 1.10)

  - [ ] 14.1 Reconstruir o grafo com as vinte etapas
    - Reescrever `src/radar/orquestracao/grafo.py` com `ETAPAS` contendo as **vinte** etapas na ordem canônica — normalização, identidade, deduplicação, qualificação, consolidação de perfil, validade jurídica, enriquecimento, mercado e valuation, economia, risco, liquidez, estratégia, regras, escore, aderência do investidor, ranqueamento, decisão, explicação, persistência e memória — e `construir_grafo`
    - Incluir `deduplicacao`, `qualificacao` e `consolidacao_de_perfil` como etapas reais, tornando alcançáveis as fases `DEDUPLICADO`, `QUALIFICADO` e `CONSOLIDADO`; não executar a validade jurídica antes delas
    - Propagar o estado compartilhado como único meio de comunicação entre etapas, atualizar a fase, persistir o traço e registrar a versão do grafo em cada execução
    - _Requisitos: 70.1, 70.1.1, 70.5, 70.6, 70.7, 70.8, 70.9_

  - [ ]* 14.2 Escrever teste de propriedade para o traço de fases
    - **Property 118: Traço é subsequência da ordem canônica (`P12.1`)**
    - **Validates: Requirements 70.1, 70.5**

  - [ ]* 14.3 Escrever teste de propriedade para o determinismo do pipeline
    - **Property 121: Determinismo do pipeline (`P12.4`)**
    - **Validates: Requirements 70.1**

  - [ ]* 14.4 Escrever teste de propriedade para a equivalência com a execução sequencial
    - **Property 122: Equivalência com a execução sequencial de referência (`P12.5`)**
    - **Validates: Requirements 70.1, 70.6**

  - [ ] 14.5 Implementar os curto-circuitos do pipeline
    - Implementar o desvio por bloqueio jurídico, que não executa mercado, economia, liquidez, estratégia e escore, o desvio por identidade inferior a `I2` e o desvio por bloqueio crítico confirmado em qualquer etapa
    - O curto-circuito é verificável pela **ausência** das fases posteriores no traço
    - _Requisitos: 70.2, 70.3, 70.4, 12.2, 7.9_

  - [ ]* 14.6 Escrever teste de propriedade para o curto-circuito jurídico
    - **Property 119: Curto-circuito jurídico (`P12.2`)**
    - **Validates: Requirements 70.2, 12.2**

  - [ ]* 14.7 Escrever teste de propriedade para o curto-circuito de identidade
    - **Property 120: Curto-circuito de identidade (`P12.3`)**
    - **Validates: Requirements 70.3, 7.9**

  - [ ] 14.8 Remover toda regra de negócio do grafo
    - Mover a heurística de confiança não versionada para o Motor de Escore e o bloqueio crítico para o Motor de Risco; o grafo passa a apenas sequenciar etapas, sem nenhuma decisão própria
    - _Requisitos: 70.6, 50.4, 34.5_

  - [ ] 14.9 Implementar os guarda-corpos dos componentes de IA
    - Garantir que nenhum módulo de `src/radar/motores/**` e `src/radar/pipeline/**` importe, direta ou transitivamente, cliente de modelo de linguagem, e completar `MT-10` para falhar com o caminho completo do import proibido
    - Agentes produzem apenas proposta de evidência; nenhum componente automatizado cria evidência nem promove desconhecido para confirmado
    - _Requisitos: 71.1, 71.2, 71.3, 71.4, 71.5, 71.6, 71.7, 71.8, 71.9, 71.10_

  - [ ] 14.10 Implementar os pontos mínimos de supervisão humana
    - Declarar `PONTOS_HUMANOS_OBRIGATORIOS` com os **sete** pontos mínimos, `validar_configuracao_de_supervisao`, que rejeita configuração que removeria qualquer um deles, e `registrar_intervencao_humana` com ator, papel, data, objeto afetado e justificativa
    - _Requisitos: 83.1, 83.2, 83.3, 83.4, 83.5, 83.6, 83.7_

  - [ ]* 14.11 Escrever teste de propriedade para os pontos de supervisão
    - **Property 148: Pontos mínimos de supervisão não são removíveis (`P16.5`)**
    - **Validates: Requirements 83.5, 83.6**

  - [ ] 14.12 Implementar as configurações do investidor
    - Criar `src/radar/governanca/configuracoes_do_investidor.py` com os doze grupos de configuração, cada valor identificado pelo código de parâmetro do catálogo, com escopo e versão; configuração que reduza bloqueio crítico é rejeitada
    - _Requisitos: 78.1, 78.2, 78.3, 78.4, 78.5, 78.6, 78.7_

  - [ ] 14.13 Implementar o controle de escopo e prioridade
    - Declarar a tabulação de prioridade dos **97** requisitos, com exatamente uma classificação entre `P0`, `P1`, `P2` e fora do MVP para cada um, e o controle que recusa expansão de escopo sem revisão
    - _Requisitos: 75.1, 75.2, 75.3, 75.4, 75.5, 75.6, 75.7_

  - [ ]* 14.14 Escrever teste de propriedade para a cobertura de prioridade
    - **Property 145: Cobertura de prioridade dos requisitos (`P16.2`)**
    - **Validates: Requirements 75.5**

  - [ ] 14.15 Declarar a estrutura de invariantes e Golden Cases
    - Criar `testes/invariantes/` e `testes/golden/` com a estrutura dos testes de invariante e dos quatro Golden Cases, cada caso declarando a **lista de fatos que invalidariam o resultado**; a implementação dos oráculos numéricos fecha na etapa 11
    - _Requisitos: 73.1, 73.2, 73.3, 73.4, 73.5, 73.6, 73.8_

- [ ] 15. Checkpoint — fim da etapa 1, domínio determinístico completo
  - Executar a suíte inteira, `ruff`, `mypy --strict` e `MT-11`; confirmar que os dez blocos da etapa 1 estão fechados, que nenhuma regra vive no grafo, que os motores não importam camada de IA e que as 145 propriedades da etapa 1 estão verdes. Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 16. Etapa 2 — Persistência das 61 entidades, integridade e governança de parâmetros

  - [ ] 16.1 Declarar o modelo físico das 61 entidades
    - Reescrever `db/schema.sql` por migração versionada com as **61** entidades do dicionário, todas nomeadas em português: aquisição, fonte, captura e documentos (11); imóvel, identidade, perfil e processo (10); oportunidade, triagem, análise e comparação (27); portfólio, resultado, governança e monitoramento (13)
    - Declarar as cardinalidades publicadas e os **60** enums do banco espelhando exatamente os enums de domínio
    - _Requisitos: 74.1, 74.2, 74.3, 74.4, 74.5, 74.6, 74.7, 74.8, 74.9, 74.10_

  - [ ] 16.2 Migrar para português o esquema existente
    - Criar a migração versionada que renomeia tabelas, colunas, índices, restrições e enums do esquema atual para português, sem reescrita manual do esquema e sem perda de dado
    - Renomear em conjunto os utilitários de `scripts/**` e os modelos de `src/radar/db/modelos.py`
    - _Requisitos: 94.2, 97.3_

  - [ ] 16.3 Declarar os itens de integridade 1 a 5
    - Índice único **parcial** de matrícula em `identificadores_de_imovel` para `tipo = 'matricula'`, com coluna de origem; unicidade de `documentos` por vínculo e hash do arquivo; unicidade de `oportunidades` por fonte e referência externa quando não nula; índice por `analise_id` em **todas** as tabelas filhas de `analises`; `CHECK` de escala 0–100 em toda coluna de escala e `CHECK (versao > 0)` em `analises`
    - _Requisitos: 9.1, 61.1, 86.9, 74.3_

  - [ ] 16.4 Declarar os itens de integridade 6 a 11
    - Escores em `NUMERIC(5,2)` sem truncamento, com arredondamento declarado como parâmetro versionado; gatilhos que rejeitam `UPDATE` e `DELETE` em `analises`, `evidencias`, `capturas`, `decisoes` e `eventos_de_analise`; `ON DELETE CASCADE` restrito a rotina nomeada de limpeza com confirmação; migrações versionadas com seed idempotente e remoção de schema exigindo confirmação; contrato congelado na fronteira de persistência com ORM cobrindo **todas** as tabelas; índice vetorial criado ou reconstruído após a carga inicial
    - _Requisitos: 61.2, 61.7, 64.3, 62.8_

  - [ ] 16.5 Declarar os itens de integridade 12 a 16 das entidades do Domínio O
    - Versão de documento estritamente crescente e sem lacuna, com `UNIQUE (documento_id, versao)`, `CHECK (versao >= 1)` e gatilho de contiguidade; imutabilidade do arquivo original com gatilhos e restrição sobre hash e URI; unicidade de execução de checklist por análise e de resultado por item; append-only em `versoes_de_documento`, `resultados_de_triagem`, `execucoes_de_checklist`, `resultados_de_item_de_checklist`, `andamentos_processuais`, `diferencas_de_comparacao`, `analises_documentos` e `intervencoes_humanas`; nenhuma restrição, gatilho, sequência ou coluna calculada relacionando versão de documento a versão de análise
    - _Requisitos: 86.2, 87.1, 87.3, 92.4, 92.7_

  - [ ] 16.6 Mapear todas as tabelas no ORM e nos repositórios
    - Reescrever `src/radar/db/modelos.py` e `src/radar/db/repositorio.py` cobrindo as 61 entidades, com a trilha de evidência efetivamente gravada — nenhuma análise é persistida com zero evidências — e as restrições declaradas dentro da declaração de tabela, de modo que gerem DDL
    - _Requisitos: 20.1, 61.7, 74.3_

  - [ ] 16.7 Implementar o versionamento append-only das análises
    - Persistir o snapshot da análise como tipo congelado, com versões estritamente crescentes e sem lacunas por oportunidade, e todas as anteriores inalteradas byte a byte após a persistência de uma nova
    - _Requisitos: 61.1, 61.2, 61.3, 61.7_

  - [ ]* 16.8 Escrever teste de propriedade para o versionamento de análises
    - **Property 124: Versionamento monotônico e sem lacunas (`P13.2`)**
    - **Validates: Requirements 61.1**

  - [ ]* 16.9 Escrever teste de propriedade para a imutabilidade das análises
    - **Property 125: Imutabilidade das análises anteriores (`P13.3`)**
    - **Validates: Requirements 61.2**

  - [ ] 16.10 Implementar a reprodutibilidade e a vigência temporal
    - Registrar em cada análise as versões de regra, de parâmetros e de checklist vigentes na data, e implementar a reexecução histórica que produz a mesma decisão com as mesmas versões e os mesmos dados
    - _Requisitos: 61.4, 61.5, 61.6, 62.8, 62.9_

  - [ ]* 16.11 Escrever teste de propriedade para a reprodutibilidade histórica
    - **Property 126: Reprodutibilidade da decisão histórica (`P13.4`)**
    - **Validates: Requirements 61.4, 62.8**

  - [ ]* 16.12 Escrever teste de propriedade para a vigência temporal
    - **Property 127: Vigência temporal das versões (`P13.5`)**
    - **Validates: Requirements 62.8**

  - [ ] 16.13 Implementar o gestor de parâmetros com hierarquia e vigência
    - Criar `src/radar/governanca/parametros.py` com `ORDEM_DE_ESCOPO` — global, investidor, estratégia, localização, tipo, oportunidade e exceção — e `resolver_parametro`, que aplica o escopo mais específico com versão vigente e **registra** o escopo aplicado
    - Parâmetro sem versão vigente na data levanta `ErroDeParametroSemVigencia`; o banco passa a ser a fonte única de parâmetros
    - _Requisitos: 62.1, 62.2, 62.3, 62.4, 62.5, 62.6, 62.7, 62.10, 62.11, 62.12_

  - [ ]* 16.14 Escrever teste de propriedade para a resolução de parâmetro
    - **Property 130: Resolução de parâmetro pelo escopo mais específico (`P13.8`)**
    - **Validates: Requirements 62.10**

  - [ ] 16.15 Gerar o seed a partir da tabela `STR` e fechar `MT-07`
    - Gerar o seed de `estrategias` e dos pesos a partir da tabela `STR` e dos conjuntos de pesos, mantendo as constantes Python apenas como valores de arranque que alimentam o gerador, e completar `MT-07` comparando as três representações
    - Gerar também o seed de `itens_de_checklist` a partir dos Anexos A, B e C.1, com os 234 itens, e comparar catálogo, seed e banco em `MT-03`
    - _Requisitos: 62.10, 92.2_

  - [ ] 16.16 Implementar a trilha de auditoria append-only
    - Persistir os **22** tipos de evento de auditoria com data, ator, papel, objeto, valor anterior, valor novo e motivo, sem `UPDATE` nem `DELETE`, e o registro de execução
    - _Requisitos: 64.1, 64.2, 64.3, 64.4, 64.5_

  - [ ]* 16.17 Escrever teste de propriedade para a trilha de auditoria
    - **Property 129: Trilha de auditoria é append-only (`P13.7`)**
    - **Validates: Requirements 64.1, 64.3**

  - [ ] 16.18 Tratar parâmetro pendente de decisão e dicionário incompleto
    - Marcar parâmetro pendente de decisão como não aplicável, reportando o requisito dependente como não avaliado, e rejeitar regra que dependa de entidade ou campo ausente do dicionário
    - _Requisitos: 74.11_

  - [ ]* 16.19 Escrever teste de propriedade para parâmetro pendente de decisão
    - **Property 146: Parâmetro pendente de decisão nunca é aplicado (`P16.3`)**
    - **Validates: Requirements 74.11**

  - [ ]* 16.20 Escrever teste de propriedade para a dependência do dicionário
    - **Property 147: Regra depende só do dicionário declarado (`P16.4`)**
    - **Validates: Requirements 74.11**

  - [ ]* 16.21 Escrever testes de integração de banco
    - Marcar com `@pytest.mark.db`, desabilitados por default, executados contra PostgreSQL com pgvector; cobrir índice único parcial de matrícula, idempotência de captura, idempotência de esquema e seed, rejeição de `UPDATE` e `DELETE` nas tabelas append-only, `CHECK` de escala e de versão, preservação de escala em `NUMERIC(5,2)`, unicidade de documento por vínculo e hash, contiguidade de versões de documento e execução única de checklist por análise
    - _Requisitos: 9.1, 61.1, 61.2, 64.3, 86.9, 87.1, 92.4_

- [ ] 17. Checkpoint — persistência e governança de parâmetros
  - Executar a suíte inteira, `ruff`, `mypy --strict`, `MT-07` e `MT-11`, mais os testes marcados de banco; confirmar que o esquema está integralmente em português, que as dezesseis exigências de integridade estão declaradas e que nenhuma tabela mapeada deixou de ser gravada. Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 18. Etapa 3 — Documentos, evidências manuais, processos judiciais e débitos

  - [ ] 18.1 Implementar o gestor de documentos
    - Criar `src/radar/documentos/gestor.py` com `MetadadosDeDocumento`, `TipoDeDocumento` de nove valores, `OrigemDeDocumento` de três valores e `GestorDeDocumentos.registrar`, gravando nome original, extensão, tipo MIME, tamanho, hash do arquivo, origem, data e hora, usuário responsável e versão vigente
    - O documento é entidade própria vinculável a imóvel, oportunidade e análise; registrar o mesmo arquivo no mesmo vínculo é idempotente
    - _Requisitos: 86.1, 86.3, 86.4, 86.5, 86.9_

  - [ ]* 18.2 Escrever teste de propriedade para a idempotência do registro de documento
    - **Property 153: Idempotência do registro de documento (`P17.4`)**
    - **Validates: Requirements 86.9**

  - [ ] 18.3 Preservar o arquivo original e derivar a extração
    - Criar `src/radar/documentos/extracao.py` com `extrair`, gravando texto, páginas, segmentos e representação vetorial como conteúdo **derivado** em tabela própria, sem nunca alterar o arquivo original nem o seu hash
    - _Requisitos: 86.2, 86.6_

  - [ ]* 18.4 Escrever teste de propriedade para a imutabilidade do arquivo original
    - **Property 151: Imutabilidade do arquivo original (`P17.2`)**
    - **Validates: Requirements 86.2, 86.6**

  - [ ] 18.5 Implementar o download com verificação de integridade
    - Criar `src/radar/documentos/integridade.py` e `GestorDeDocumentos.baixar`, que entrega o arquivo íntegro, recalcula o hash e compara com o registrado
    - Divergência levanta `ErroDeIntegridadeDeDocumento`, insere registro em `falhas_de_integridade`, abre pendência de prioridade **crítica** e **impede** apresentar o conteúdo extraído como evidência enquanto a falha estiver aberta; o arquivo não é substituído, corrigido nem removido
    - _Requisitos: 86.7, 86.8_

  - [ ]* 18.6 Escrever teste de propriedade para o round-trip de download
    - **Property 152: Round-trip de download (`P17.3`)**
    - **Validates: Requirements 86.7, 86.8**

  - [ ] 18.7 Implementar o versionamento de documento
    - Implementar `registrar_nova_versao` e `obter_versao` com numeração estritamente crescente e sem lacuna por documento, preservando toda versão anterior, e registrando hash, URI, tamanho, páginas, autor, data, origem e motivo da nova versão
    - Nova versão que contradiz evidência vigente preserva as duas evidências e marca o fato como conflitante
    - _Requisitos: 87.1, 87.2, 87.5, 87.6, 87.7, 87.8_

  - [ ]* 18.8 Escrever teste de propriedade para o versionamento de documento
    - **Property 156: Versionamento de documento é crescente e sem lacuna (`P17.7`)**
    - **Validates: Requirements 87.1, 87.2**

  - [ ] 18.9 Exigir versão de documento na evidência derivada
    - Rejeitar registro de evidência derivada de documento sem a versão do documento e a localização exata; ausência do documento **nunca** é tratada como conformidade
    - _Requisitos: 86.10, 86.11_

  - [ ] 18.10 Implementar a evidência de origem manual
    - Criar `src/radar/evidencia/manual.py` com `registrar_evidencia_manual` e `restricao_do_gate_por_evidencia_manual`: origem `USUARIO` sem documento de suporte nunca recebe classe `A` nem `B`, e nenhuma verificação obrigatória do gate jurídico passa a `REGULAR` por essa evidência
    - A evidência manual é identificada como tal em toda apresentação e em toda explicação
    - _Requisitos: 89.1, 89.2, 89.3, 89.4, 89.5, 89.6, 89.7, 89.8, 89.9_

  - [ ]* 18.11 Escrever teste de propriedade para a evidência de origem USUARIO
    - **Property 155: Evidência USUARIO não herda confiança de fonte oficial (`P17.6`)**
    - **Validates: Requirements 89.3, 89.5**

  - [ ] 18.12 Implementar a importação manual de processo judicial
    - Criar `src/radar/processos/registro.py` com `SituacaoDeProcesso`, `ProcessoJudicial` e `importar_processo`, gravando número, órgão julgador, partes, tipo, situação, data da consulta, documento vinculado, observação e impacto classificado, mais os andamentos com data, descrição, documento de suporte e espécie de ato
    - Impacto permanece `DESCONHECIDO` quando não há decisão nem andamento que o sustente
    - _Requisitos: 90.1, 90.2, 90.3, 90.4, 90.5, 90.6, 90.7, 90.8_

  - [ ] 18.13 Implementar o débito como entidade explícita
    - Criar `src/radar/debitos/registro.py` com `TipoDeDebito`, `SituacaoDeDebito`, `ResponsabilidadePeloDebito` e `Debito`, gravando valor com estado de informação, período de referência, fonte, data da consulta, documento vinculado, situação e responsabilidade atribuída pelo edital com cláusula e página
    - Ligar os débitos registrados à composição de `CUS-005` e `CUS-006`, de modo que acrescentar débito nunca reduza o custo econômico total
    - _Requisitos: 91.1, 91.2, 91.3, 91.4, 91.5, 91.6, 91.7, 91.8, 91.9, 91.10_

  - [ ]* 18.14 Escrever teste de propriedade para a conservação do débito no custo
    - **Property 167: Conservação do débito no custo (`P17.18`)**
    - **Validates: Requirements 91.3, 91.6, 26.1**

  - [ ]* 18.15 Escrever teste de propriedade para débito não investigado
    - **Property 168: Débito não investigado nunca vale zero (`P17.19`)**
    - **Validates: Requirements 91.5, 26.10**

- [ ] 19. Etapa 4 — Análise manual ponta a ponta pela porta 1

  - [ ] 19.1 Implementar a criação de imóvel com identificação mínima
    - Implementar o caso de uso de criação de imóvel pelo usuário, exigindo a identificação mínima do gate `G0` e recusando criação sem ela, com autor e data registrados
    - _Requisitos: 84.1, 84.2_

  - [ ] 19.2 Implementar o cadastro da oportunidade vinculada ao imóvel
    - Implementar o cadastro da oportunidade da CAIXA sobre imóvel novo ou existente, com referência externa, data do certame, lance mínimo, praça e modalidade, e a porta de entrada registrada como proveniência
    - Quando a deduplicação conclui identidade verdadeira, vincular ao imóvel existente **sem criar imóvel novo**; identidade indeterminada registra candidata a vínculo mais pendência e não cria imóvel definitivo
    - _Requisitos: 84.3, 84.10, 84.11, 84.12, 84.13_

  - [ ]* 19.3 Escrever teste de propriedade para a não criação de imóvel novo
    - **Property 150: Nova captura não cria imóvel novo (`P17.1`)**
    - **Validates: Requirements 84.12, 9.1**

  - [ ] 19.4 Implementar o envio de documentos e o registro de evidências no mesmo fluxo
    - Encadear envio de edital e matrícula, registro de IPTU, condomínio e processos, e registro de evidências manuais no mesmo fluxo de criação da análise
    - _Requisitos: 84.4, 84.6, 84.7_

  - [ ] 19.5 Executar a análise sobre evidência real
    - Executar o pipeline completo sobre a oportunidade criada manualmente, produzindo decisão, custo econômico total decomposto, valuation, riscos e pendências, com o mesmo motor determinístico das duas portas
    - _Requisitos: 84.5, 84.8, 84.9_

  - [ ] 19.6 Produzir a visão financeira oficial decomposta
    - Produzir a decomposição em treze componentes, cada um com valor, estado de informação, fonte e evidência de origem, e as catorze grandezas da visão financeira oficial; componente sem evidência de origem é classificado como estimado ou desconhecido e abre pendência
    - _Requisitos: 96.1, 96.2, 96.6, 96.7_

  - [ ] 19.7 Cobrir os passos 1 a 13 do ciclo de prova
    - Implementar e verificar os passos 1 a 13 do ciclo de prova do MVP — criar imóvel, cadastrar oportunidade, enviar edital, enviar matrícula, informar IPTU, informar condomínio, adicionar processos, executar análise, visualizar decisão, custo econômico total, valuation, riscos e pendências — cada um com o requisito que o sustenta declarado no próprio caso
    - _Requisitos: 95.1, 95.2, 95.5_

- [ ] 20. Etapa 5 — Reanálise, versionamento e comparação de versões

  - [ ] 20.1 Implementar a reanálise sem sobrescrita
    - Implementar a execução de nova análise sobre a mesma oportunidade, criando nova versão e preservando todas as anteriores, com data, autor e motivo
    - _Requisitos: 88.1, 88.2, 88.3_

  - [ ] 20.2 Garantir a independência entre as duas dimensões de versão
    - Manter as numerações de versão de documento e de versão de análise como sequências separadas, sem que uma derive da outra, e registrar em cada análise a lista de documentos considerados com suas versões
    - _Requisitos: 87.3, 87.4, 61.1_

  - [ ]* 20.3 Escrever teste de propriedade para a independência das dimensões de versão
    - **Property 157: Independência das dimensões de versão (`P17.8`)**
    - **Validates: Requirements 87.3, 61.1**

  - [ ] 20.4 Implementar o comparador de versões com as cinco categorias
    - Criar `src/radar/versionamento/comparador.py` com `CategoriaDeDiferenca` de cinco valores, `Diferenca` e `comparar_versoes`, simétrico e neutro — comparar não altera nenhuma das versões —, com conjunto de diferenças vazio exatamente quando evidências, parâmetros, versões de regra e resultados coincidem
    - _Requisitos: 88.4, 88.5, 88.7, 88.9_

  - [ ]* 20.5 Escrever teste de propriedade para a comparação vazia
    - **Property 158: Comparação vazia se e somente se idênticas (`P17.9`)**
    - **Validates: Requirements 88.7**

  - [ ]* 20.6 Escrever teste de propriedade para a simetria da comparação
    - **Property 159: Simetria e neutralidade da comparação (`P17.10`)**
    - **Validates: Requirements 88.4, 88.9**

  - [ ]* 20.7 Escrever teste de propriedade para a totalidade da classificação de diferenças
    - **Property 161: Totalidade da classificação de diferenças (`P17.12`)**
    - **Validates: Requirements 88.5**

  - [ ] 20.8 Exigir motivo em decisão alterada
    - Implementar `MotivoDaAlteracao` obrigatório quando a categoria é decisão alterada, com ao menos uma evidência, valor, pendência ou versão de regra responsável, garantido também por `CHECK` no banco
    - _Requisitos: 88.6_

  - [ ]* 20.9 Escrever teste de propriedade para o motivo da decisão alterada
    - **Property 160: Decisão alterada sempre tem motivo (`P17.11`)**
    - **Validates: Requirements 88.6**

  - [ ] 20.10 Implementar a reexecução que não versiona
    - Implementar `reexecutar_analise`, que não cria nova versão quando as entradas não mudaram e registra a reexecução na trilha de auditoria
    - _Requisitos: 88.10, 61.1, 64.1_

  - [ ]* 20.11 Escrever teste de propriedade para a reexecução sem mudança
    - **Property 170: Reexecução sem mudança não versiona (`P17.21`)**
    - **Validates: Requirements 88.10, 61.1, 64.1**

  - [ ] 20.12 Servir o histórico navegável de versões
    - Produzir o histórico de versões com data, autor, motivo, decisão e camada determinante de cada versão, consultável por par de versões
    - _Requisitos: 88.8_

  - [ ] 20.13 Cobrir os passos 14 a 18 do ciclo de prova
    - Implementar e verificar os passos 14 a 18 — baixar documentos, adicionar nova evidência, reanalisar, comparar `V1` × `V2` e revisitar o imóvel posteriormente —, preservando ao fim todas as versões de análise, documentos, versões de documento e evidências produzidas
    - _Requisitos: 95.1, 95.2, 95.7_

- [ ] 21. Etapa 6 — Interface de programação autenticada

  - [ ] 21.1 Declarar as famílias de recursos em português
    - Ampliar `src/radar/api/**` com as famílias de recursos de produto: imóveis, oportunidades, documentos por oportunidade, evidências, débitos, processos, análises, comparação de análises, candidatos do Radar, triagem, checklists, configurações, visão geral, ações, linha do tempo, comparação de oportunidades, monitoramento e decisão do investidor
    - Recursos, campos e valores de domínio nomeados em português
    - _Requisitos: 97.1, 97.3_

  - [ ] 21.2 Implementar as operações de produto
    - Implementar criar e consultar imóvel, criar oportunidade e vincular a imóvel existente, enviar e baixar documento e registrar nova versão, registrar evidência manual, registrar débito e processo, executar análise e reanalisar, listar e consultar versões e comparar duas versões
    - _Requisitos: 97.2_

  - [ ] 21.3 Exigir autenticação e autorização em toda operação exposta
    - Implementar autenticação e autorização antes de qualquer execução de cálculo ou persistência: requisição sem credencial responde 401 e requisição autenticada sem autorização responde 403; nenhuma operação exposta fica acessível sem credencial, inclusive a de análise, que executa cálculo **e** escrita
    - _Requisitos: 79.8, 97.4_

  - [ ] 21.4 Traduzir a taxonomia de erro na fronteira
    - Declarar `MAPA_DE_ESTADO_HTTP` e `tratar_erro_do_radar`: corpo com código, mensagem, campo e orientação, sem rastreamento de pilha, consulta, caminho de arquivo nem valor de configuração; entrada inválida responde 422, referência inexistente responde 404 nomeando recurso e causa, violação de invariante responde 409 ou 405 e indisponibilidade responde 503 **sem** degradar o resultado do domínio
    - Corrigir o caso em que valor de mercado igual a zero atravessava o esquema e derrubava a requisição com 500, aplicando também a restrição no próprio esquema de entrada
    - _Requisitos: 79.9, 97.5, 27.16_

  - [ ] 21.5 Registrar toda operação exposta na trilha de auditoria
    - Registrar o que foi requisitado, por quem, quando, com que papel e o resultado, inclusive as respostas de erro e as recusas
    - _Requisitos: 79.10, 97.6, 64.1_

  - [ ] 21.6 Impedir rotas que alterem registro imutável
    - Não expor nenhuma operação que altere captura registrada, evidência registrada ou versão de análise já persistida; chamada interna indevida levanta `ErroDeOperacaoNaoPermitida`
    - _Requisitos: 97.7_

  - [ ] 21.7 Completar o contrato de entrada da análise
    - Expor em `EntradaDeAnalise` **todos** os treze componentes do custo econômico total, inclusive tributos, custo jurídico potencial, probabilidade jurídica e carregamento; ausência é representada como desconhecida no corpo da requisição, nunca por omissão com default numérico
    - _Requisitos: 26.7, 26.10, 96.7_

  - [ ] 21.8 Tornar a configuração fechada por default
    - Adotar `pydantic-settings` como via única de configuração, com segredo em tipo redigido; remover o leitor de `.env` reimplementado em `scripts/**` que ignorava variáveis de ambiente reais; exigir `sslmode=verify-full` com autoridade certificadora explícita fora de `localhost`; não publicar a porta do banco por default; fábrica preguiçosa de engine e sessão com tamanho de pool, tempo limite e política de repetição; CORS restritivo e limite de taxa antes de qualquer exposição além de `localhost`
    - Ausência de segredo, de autoridade certificadora ou de URL de banco impede o arranque com mensagem clara, em lugar de arrancar em modo permissivo
    - _Requisitos: 79.8, 79.9_

  - [ ] 21.9 Servir as visões e ações do investidor
    - Implementar o painel consolidado, as ações de salvar, monitorar e alertar com ator, papel, data e motivo, a linha do tempo dos doze eventos em ordem cronológica, a comparação de duas a cinco oportunidades — fora da faixa rejeita com a causa —, a visão de monitoramento e as oito decisões do investidor
    - _Requisitos: 79.1, 79.2, 79.3, 79.4, 79.5, 79.6, 79.7_

  - [ ] 21.10 Renomear para português o contrato existente
    - Renomear recursos, campos e valores de domínio do contrato atual para português, mantendo a correspondência com os rótulos normativos declarada em um único ponto
    - _Requisitos: 97.3_

  - [ ]* 21.11 Escrever testes de contrato
    - Cobrir os códigos de estado por família de erro, a recusa de referência inexistente com recurso e causa, a ausência de rota que altere registro imutável, a exigência de credencial em toda operação e o contrato completo dos treze componentes de custo
    - _Requisitos: 79.8, 79.9, 97.4, 97.5, 97.7_

- [ ] 22. Etapa 7 — Interface do investidor em React e em português

  - [ ] 22.1 Criar a estrutura da interface
    - Criar `frontend/src/**` em React, organizado por páginas, serviços, hooks, tipos, rotas e layouts, consumindo exclusivamente o contrato de programação
    - _Requisitos: 94.1_

  - [ ] 22.2 Implementar as doze capacidades mínimas
    - Implementar painel de visão geral, nova análise em fluxo único, pesquisa de imóveis, Radar de candidatos, ficha detalhada, documentos, evidências, pendências, reanálise, comparação de versões, checklists e parâmetros
    - _Requisitos: 94.3, 94.6_

  - [ ] 22.3 Apresentar a ficha com as vinte grandezas e o estado de informação
    - Apresentar cada uma das vinte grandezas da ficha com o estado de informação correspondente, sem nunca exibir valor desconhecido como zero
    - _Requisitos: 94.4, 94.5, 66.11_

  - [ ] 22.4 Implementar documentos, versões e download
    - Listar documentos por tipo, exibir versões e permitir o download de todo documento registrado, sinalizando falha de integridade aberta quando houver
    - _Requisitos: 94.7, 86.7, 86.8_

  - [ ] 22.5 Implementar a comparação de versões na interface
    - Apresentar o histórico navegável com data, autor, motivo, decisão e camada determinante, e as diferenças classificadas nas cinco categorias
    - _Requisitos: 94.8, 88.8_

  - [ ] 22.6 Apresentar checklists e parâmetros
    - Apresentar escopo resolvido, versão aplicada e resultado por item do checklist, e o identificador do catálogo, o escopo aplicado, a versão e o valor vigente de cada parâmetro
    - _Requisitos: 94.9, 94.10, 78.6_

  - [ ] 22.7 Apresentar a visão financeira oficial navegável
    - Apresentar os treze componentes do custo econômico total e as catorze grandezas, cada componente navegável até a evidência que o originou, com a forma fechada conservadora rotulada como referência informativa
    - _Requisitos: 96.8, 96.5, 96.1_

  - [ ] 22.8 Garantir a interface integralmente em português
    - Traduzir todo texto, rótulo, mensagem e relatório para português; texto de origem externa em outro idioma é **preservado como evidência** e apresentado com rótulo e interpretação em português
    - _Requisitos: 94.2, 94.11_

  - [ ] 22.9 Implementar as visões do Radar e a navegação
    - Implementar as oito visões pré-definidas como parametrizações da mesma consulta, com as bloqueadas apresentando camada determinante e motivo impeditivo e permanecendo **fora** do ranqueamento operacional; filtro de visualização é separado de regra eliminatória e nunca elimina oportunidade
    - _Requisitos: 66.1, 66.2, 66.3, 66.4, 66.5, 66.6, 66.7, 66.8, 66.9, 66.10, 66.12_

  - [ ] 22.10 Implementar a ficha da oportunidade e as ações de comparação
    - Implementar as seções da ficha da oportunidade, a linha do tempo dos doze eventos, e as ações de comparar, rejeitar e monitorar com motivo registrado
    - _Requisitos: 67.1, 67.2, 67.3, 67.4, 67.5, 67.6, 67.7, 67.8, 67.9, 67.10, 67.11, 67.12, 68.1, 68.2, 68.3, 68.4, 68.5, 68.6, 68.7_

  - [ ]* 22.11 Escrever testes de componente e de instantâneo
    - Verificar a presença de cada elemento obrigatório da explicabilidade e da visão financeira por instantâneo de **estrutura**, não de redação, e a apresentação do estado de informação em cada grandeza
    - _Requisitos: 56.1, 56.2, 94.4, 96.2_

- [ ] 23. Checkpoint — primeiro marco funcional de `D88`, ao fim da etapa 7
  - Executar a suíte inteira, `ruff`, `mypy --strict`, `MT-11` e os testes marcados de banco; confirmar que a análise manual de um imóvel real da CAIXA fecha do envio dos documentos até a decisão apresentada na interface, com complementação de evidência e reanálise, e que os passos 1 a 18 do ciclo de prova já são executáveis pela porta manual. Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 24. Etapa 8 — Contrato de conector de fonte e conector CAIXA

  - [ ] 24.1 Declarar o contrato único do conector
    - Criar `src/radar/conectores/contrato.py` com o protocolo `ConectorDeFonte` — `listar_ofertas`, `obter_detalhe`, `obter_documentos` e `declarar_cobertura` —, `CoberturaDaFonte` com modalidades, unidades federativas, cidades, tipos e campos entregues e não entregues, `OfertaBruta` e `ReferenciaDeOferta`
    - A estratégia de aquisição é rótulo interno de infraestrutura e **não** é exposta a entidade, regra, parâmetro ou motor
    - _Requisitos: 85.1, 85.2, 85.3, 85.4_

  - [ ] 24.2 Implementar o conector da CAIXA
    - Criar `src/radar/conectores/caixa.py` com `ConectorCaixa` implementando o contrato, de modo que uma nova fonte exija apenas implementar o contrato e cadastrar a fonte
    - _Requisitos: 85.5, 1.1, 1.2, 1.3_

  - [ ] 24.3 Implementar a aquisição e a captura com identificador do conector
    - Implementar `executar_aquisicao` e `registrar_captura`, preservando o payload bruto de forma imutável **antes** de qualquer avaliação e registrando o identificador e a versão do conector em cada captura
    - _Requisitos: 85.6, 85.10, 2.1, 2.2, 2.3_

  - [ ] 24.4 Registrar como captura rejeitada o payload reprovado no gate `G0`
    - Gravar `RejeicaoDeCaptura` com estado rejeitado, causa nomeada e campos ausentes, **sem** criar oportunidade e **sem** apagar a captura, de modo que a cobertura real do conector seja auditável e "a fonte não entregou preço" permaneça distinguível de "não havia oferta"
    - _Requisitos: 85.8, 4.1_

  - [ ] 24.5 Tratar a falha de obtenção sem inventar ausência
    - Implementar `ErroDeObtencaoDoConector` registrando fonte, data, hora e causa na última falha do conector, preservando a última captura válida; oferta não listada permanece desconhecida e nenhuma oportunidade é encerrada por silêncio da fonte
    - _Requisitos: 85.9_

  - [ ] 24.6 Entregar os arquivos ao gestor de documentos
    - Encaminhar os arquivos obtidos ao `GestorDeDocumentos` com o tipo de documento declarado e a origem de captura automática, sem que o conector conheça a extração
    - _Requisitos: 85.7, 86.1, 86.5_

  - [ ]* 24.7 Escrever teste de propriedade para o desacoplamento do conector
    - **Property 169: Desacoplamento do conector (`P17.20`)**
    - **Validates: Requirements 85.3, 85.5**

  - [ ]* 24.8 Escrever testes de integração de fonte externa
    - Um a três exemplos representativos com dublê nos testes de propriedade, cobrindo cobertura declarada, obtenção de documentos e falha de obtenção que preserva a última captura válida
    - _Requisitos: 85.2, 85.7, 85.9_

- [ ] 25. Etapa 9 — Radar automático, triagem rápida e gate de promoção

  - [ ] 25.1 Implementar a triagem rápida como prefixo do pipeline
    - Criar `src/radar/pipeline/triagem.py` com `ResultadoDeTriagem` de dois valores, `CriterioDeTriagem`, `AvaliacaoDeTriagem` e `triar`, executando as fases 1 a 5 do **mesmo** pipeline com os dados já disponíveis e registrando versão dos filtros, critério determinante e resultado de cada critério avaliado
    - _Requisitos: 93.1, 93.3, 93.9, 93.10_

  - [ ]* 25.2 Escrever teste de propriedade para a triagem como prefixo
    - **Property 164: A triagem é prefixo do mesmo pipeline (`P17.15`)**
    - **Validates: Requirements 93.1, 93.8, 70.1**

  - [ ] 25.3 Garantir a abstenção estrutural da triagem
    - Garantir que a triagem não produza valuation, custo econômico total, escore de oportunidade, escore de aderência nem estado de decisão, e que a tabela de resultados de triagem não tenha coluna para nenhum deles
    - _Requisitos: 93.2, 93.4_

  - [ ]* 25.4 Escrever teste de propriedade para a abstenção da triagem
    - **Property 162: A triagem rápida nunca decide (`P17.13`)**
    - **Validates: Requirements 93.2, 93.4**

  - [ ] 25.5 Implementar o gate de promoção `G1-P`
    - Declarar `CRITERIOS_DE_PROMOCAO` como dado e implementar `avaliar_gate_de_promocao` conjuntivo, que nomeia o primeiro critério não satisfeito; análise profunda só executa com `G1-P` satisfeito ou promoção manual registrada
    - Reprovar na promoção **não** é decisão de investimento: a oportunidade permanece disponível para reavaliação
    - _Requisitos: 93.5, 93.6_

  - [ ]* 25.6 Escrever teste de propriedade para a necessidade do gate de promoção
    - **Property 163: Gate de promoção é necessário (`P17.14`)**
    - **Validates: Requirements 93.5, 93.6, 93.7**

  - [ ] 25.7 Implementar a promoção manual registrada
    - Implementar `promover_manualmente` com autor, data e motivo, registrada como intervenção humana
    - _Requisitos: 93.7, 83.5_

  - [ ] 25.8 Listar candidatos por potencial preliminar
    - Implementar `listar_candidatos` ordenado por potencial preliminar, **sem** escore de oportunidade, com o resultado da triagem vigente e a situação de promoção
    - _Requisitos: 93.10, 93.11_

  - [ ] 25.9 Fechar a convergência das duas portas
    - Garantir que a oportunidade vinda do Radar atravesse o mesmo pipeline, o mesmo catálogo de regras, os mesmos parâmetros resolvidos e o mesmo motor de decisão da porta manual, executando os passos 3 a 18 do ciclo a partir do candidato promovido, sem alteração de motor, de regra ou de parâmetro
    - _Requisitos: 84.8, 84.9, 93.8, 95.3, 95.4_

  - [ ]* 25.10 Escrever teste de propriedade para a invariância de porta de entrada
    - **Property 154: Invariância de porta de entrada (`P17.5`)**
    - **Validates: Requirements 84.9, 93.8**

- [ ] 26. Etapa 10 — Checklists parametrizáveis por escopo e versionados

  - [ ] 26.1 Implementar o catálogo de checklists versionado
    - Criar `src/radar/diligencia/checklist.py` com `VersaoDeChecklist`, `ItemDeChecklist` e `CHECKLIST_PADRAO_VERSAO_1` registrada como **versão 1** com os 234 itens; toda configuração deriva dela
    - Persistir checklists, versões e itens com escopo declarado, autor, data, motivo, diferença em relação à versão anterior e situação de governança
    - _Requisitos: 92.1, 92.2, 92.3_

  - [ ] 26.2 Resolver o escopo e fixar a versão na execução
    - Implementar `resolver_checklist` por instituição, localização, tipo e estratégia, e `executar_checklist`, que fixa a versão aplicada, registra o escopo resolvido, o ator, a data, a cobertura apurada e o resultado item a item, com exatamente **uma** execução por análise
    - Reproduzir a análise com a versão registrada produz o mesmo resultado
    - _Requisitos: 92.4, 92.9, 92.10_

  - [ ]* 26.3 Escrever teste de propriedade para o registro do checklist aplicado
    - **Property 166: Registro do checklist aplicado (`P17.17`)**
    - **Validates: Requirements 92.4, 92.10**

  - [ ] 26.4 Validar os dois limites invioláveis na carga
    - Implementar `validar_configuracao_de_checklist`, que levanta `ErroDeConfiguracaoDeChecklist` nomeando o item recusado quando a configuração remove, desativa ou torna não aplicável item **crítico** da versão 1, quando torna o resultado na ausência de evidência mais favorável do que o devido na versão 1, ou quando altera a precedência canônica de decisão
    - A validação é na **carga** da configuração, não na execução: configuração inválida nunca chega a reger uma análise
    - _Requisitos: 92.5, 92.6, 92.11_

  - [ ]* 26.5 Escrever teste de propriedade para a parametrização que não enfraquece
    - **Property 165: Parametrização não enfraquece o checklist (`P17.16`)**
    - **Validates: Requirements 92.5, 92.6**

  - [ ] 26.6 Apurar a cobertura em qualquer versão configurada
    - Apurar, para toda versão configurada, que todo item aplicável ao escopo resolvido tem exatamente um resultado registrado, ou é explicitamente não aplicável com justificativa
    - _Requisitos: 92.7, 36.5_

  - [ ]* 26.7 Escrever teste de propriedade para a cobertura do catálogo em qualquer versão
    - **Property 144: Cobertura total do catálogo de checklists em qualquer versão (`P16.1`)**
    - **Validates: Requirements 36.5, 92.7**

  - [ ] 26.8 Implementar o versionamento de checklist com governança
    - Implementar `versionar_checklist`, que cria nova versão com autor, data, motivo e diferença, sem alterar versões anteriores nem execuções já registradas
    - _Requisitos: 92.8_

  - [ ] 26.9 Abrir pendência por documento exigido e ausente
    - Abrir pendência com prioridade correspondente quando o checklist exige documento que não foi registrado, sem jamais tratar a ausência do documento como conformidade
    - _Requisitos: 37.1, 37.2, 86.11, 92.7_

- [ ] 27. Checkpoint — conector, Radar automático e checklists parametrizáveis
  - Executar a suíte inteira, `ruff`, `mypy --strict`, `MT-03`, `MT-11` e os testes marcados de banco e de fonte externa; confirmar que a triagem não emite nenhum estado de decisão, que as duas portas produzem decisão, camada determinante e explicação idênticas, e que nenhuma configuração de checklist enfraquece a versão 1. Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 28. Etapa 11 — Auditoria, monitoramento, Golden Cases, regressão e meta-testes

  - [ ] 28.1 Implementar o monitoramento contínuo e a materialidade
    - Criar `src/radar/monitoramento/monitor.py` com `Materialidade`, `LIMIARES_DE_MATERIALIDADE` declarando `MON-001` a `MON-017` como dados — inclusive os seis sinais de mercado obrigatórios e a nova oportunidade excepcional que dispara a recomparação da carteira — e `ao_detectar_mudanca`
    - A comparação com o limiar é por `>=`: no valor exato do limiar, **dispara**
    - _Requisitos: 57.1, 57.2, 57.3, 57.3.1, 57.3.2, 57.4, 57.5, 57.7, 57.8, 57.9_

  - [ ]* 28.2 Escrever teste de propriedade para o limiar de materialidade
    - **Property 123: Limiar de materialidade dispara no valor exato (`P13.1`)**
    - **Validates: Requirements 57.2, 57.3**

  - [ ] 28.3 Implementar os dez estados de monitoramento, a reentrada e o abandono
    - Declarar `EstadoDeMonitoramento` com os **dez** estados e implementar a reentrada por gatilho material, o abandono de tese com motivo e a reabertura, com histórico de transições preservado
    - Reavaliar duas vezes sem mudança de entrada produz o mesmo resultado e **não** cria nova versão
    - _Requisitos: 57.6, 57.10, 57.10.1, 57.10.2, 57.11, 58.1, 58.2, 58.3, 58.4, 58.5, 58.6, 58.7, 58.8_

  - [ ]* 28.4 Escrever teste de propriedade para a idempotência da reavaliação
    - **Property 132: Idempotência da reavaliação (`P13.10`)**
    - **Validates: Requirements 57.6, 61.1**

  - [ ] 28.5 Implementar as exceções auditáveis
    - Criar `src/radar/governanca/excecoes.py` com os campos obrigatórios `EXC-001` a `EXC-009` — regra excepcionada, valor normal, valor excepcional, risco aceito, justificativa, evidência, alçada, prazo e impacto no escore —, a rejeição de exceção sobre bloqueio crítico e a expiração que restaura a regra padrão e dispara a reavaliação
    - _Requisitos: 63.1, 63.2, 63.3, 63.4, 63.4.1, 63.5, 63.6, 63.7_

  - [ ]* 28.6 Escrever teste de propriedade para a expiração de exceção
    - **Property 131: Expiração de exceção restaura a regra (`P13.9`)**
    - **Validates: Requirements 63.5**

  - [ ] 28.7 Completar a trilha de auditoria e a governança de versões
    - Completar `src/radar/governanca/{auditoria,versoes,qualidade}.py` com os 22 tipos de evento, o registro de execução, o versionamento de regra com aprovador e vigência, e a situação de governança em seis valores
    - _Requisitos: 64.1, 64.2, 64.3, 64.4, 64.5, 62.1, 62.2_

  - [ ] 28.8 Implementar o Golden Case `F.1` com os números publicados
    - Verificar, com tolerância declarada: reserva R$ 11.153,345085; carregamento de três meses a R$ 635,00 igual a R$ 1.905,00; **custo econômico total R$ 236.125,246785**; desconto líquido 0,1857750, ou **18,5775%**, sobre R$ 290.000; margem absoluta R$ 53.874,753215; base de imposto de renda na venda R$ 45.874,753215; venda líquida R$ 275.118,78701775; lucro líquido R$ 38.993,54023275; **retorno líquido 0,1651392, ou 16,5139%**; **retorno anualizado 0,8429404, ou 84,2940%**; **break-even de saída R$ 251.197,07105**; distância do break-even 0,3107, que não aciona monitorar; aluguel líquido R$ 1.170,00; base de imposto sobre aluguel R$ 1.265,00; yield bruto mensal 0,0080466; yield líquido mensal 0,0049550; **preço máximo por retorno alvo R$ 182.158,03**; **verificação inversa fechando em 0,250000 com erro inferior a 10⁻⁶**; teto conservador informativo R$ 168.374,76; veredito revenda `NAO_COMPRAR` na camada 4 e veredito renda `NAO_COMPRAR` na camada 5
    - Declarar a lista de fatos que invalidariam o resultado
    - _Requisitos: 73.1, 73.3, 26.1, 27.3, 27.12, 28.2, 28.3, 30.3.1_

  - [ ] 28.9 Implementar os Golden Cases `F.2`, `F.3` e `F.4`
    - `F.2`: averbação de leilão negativo em tratamento como pendência registral, **sem** bloqueio; `F.3`: cadeia registral recente como evidência forte que não comprova regularidade das notificações, com o segundo leilão a 60% da avaliação, que **não** aciona a regra de preço vil; `F.4`: leitura do texto do ato registral, gravame histórico baixado e valuation independente da avaliação da fonte
    - Cada caso declara a lista de fatos que invalidariam o resultado
    - _Requisitos: 73.1, 73.3, 13.13, 14.1, 23.7_

  - [ ] 28.10 Escrever os testes de regressão `REG-001` a `REG-012`
    - Um teste por linha do Anexo E, nomeado pelo identificador, com o cenário e a verificação declarados no próprio caso
    - _Requisitos: 73.4, 73.5_

  - [ ] 28.11 Escrever os testes de regressão `REG-013` a `REG-024`
    - Um teste por linha, nomeado pelo identificador; inclui a interpretação de `"47.76"` e de `"2.5%"`, o enum fora de domínio recusado na fronteira e a fronteira 89/90 do fator de confiança
    - _Requisitos: 73.4, 73.5, 3.4.1, 3.4.2, 12.5_

  - [ ] 28.12 Escrever os testes de regressão `REG-025` a `REG-035`
    - Um teste por linha, nomeado pelo identificador; inclui matrícula duplicada, reprocessamento de captura, idempotência do esquema e do seed, resposta 422 em lugar de 500, normalizador por tipo de fonte, os dois casos de bloqueio da camada 0, os dois casos de evicção, o contraexemplo do teto conservador, o recálculo por pendência resolvida e o bloqueio por risco crítico presumido
    - _Requisitos: 73.4, 73.5, 9.1, 27.16, 34.5.1, 37.9_

  - [ ] 28.13 Escrever os testes de regressão `REG-036` a `REG-044` do Domínio O
    - `REG-036`: nova captura da mesma oferta com preço alterado vincula ao imóvel existente, **nenhum** imóvel novo criado, histórico de preços atualizado; `REG-037`: extração sobre documento já registrado preserva o original, o hash e o download byte a byte; `REG-038`: evidência de matrícula informada manualmente sem documento fica com classe no máximo indicada e a verificação jurídica permanece desconhecida com pendência; `REG-039`: mesma oportunidade pelas duas portas produz mesma decisão, mesma camada e mesma explicação; `REG-040`: configuração que remove item crítico e configuração que torna a ausência favorável são recusadas, com a cobertura dos 234 itens mantida; `REG-041`: nova evidência material altera a decisão entre versões e a categoria de decisão alterada traz motivo, evidências, valores e versões de regra; `REG-042`: débito de condomínio informado manualmente com responsabilidade do adquirente integra `CUS-005` e aparece no custo decomposto; `REG-043`: candidato reprovado em `G1-P` não executa análise profunda, registra o critério não satisfeito e não emite nenhum estado de decisão; `REG-044`: nova versão de documento contradizendo evidência vigente preserva ambas, marca o fato como conflitante e mantém as versões sem lacuna
    - _Requisitos: 84.12, 86.2, 86.7, 87.1, 87.5, 88.5, 88.6, 89.3, 91.3, 92.5, 92.6, 92.7, 93.4, 93.6_

  - [ ] 28.14 Completar os onze meta-testes
    - `MT-01` rastreabilidade das 171 propriedades com a única exceção declarada de `P7.12`; `MT-02` exatamente um teste por propriedade; `MT-03` cobertura de checklist em qualquer versão e os 234 itens da versão 1; `MT-04` as 55 regras no catálogo; `MT-05` cobertura da disciplina de lance; `MT-06` prioridade dos 97 requisitos com as contagens 85, 11 e 1 e o resumo em acordo com a tabulação; `MT-07` ponto único de verdade entre tabela, constantes e banco; `MT-08` soma de pesos; `MT-09` contagem dos 60 enums; `MT-10` isolamento da IA; `MT-11` convenção de idioma
    - _Requisitos: 73.1, 73.2, 73.3, 73.6, 73.7, 73.8, 75.5, 92.7_

  - [ ] 28.15 Implementar o ciclo de prova do MVP como teste de integração ponta a ponta
    - Um **único** teste que percorre os **dezoito** passos na ordem, do passo 1 ao passo 18, sobre banco real e documentos reais, declarando no próprio caso o requisito que sustenta cada passo
    - Fechar o ciclo descobrir, selecionar, documentar, analisar, complementar, reanalisar, comparar e decidir nas **duas** portas de entrada, executando os passos 3 a 18 a partir de candidato promovido sem alteração de motor, de regra ou de parâmetro
    - Verificar os sete atributos exigidos — rastreabilidade, versionamento, explicabilidade, auditoria, reprodutibilidade, preservação de desconhecidos e histórico completo — e preservar, ao fim, todas as versões de análise, documentos, versões de documento e evidências
    - Passo não executável faz o teste falhar identificando o passo e o requisito não satisfeitos, e o MVP é reportado como incompleto, nunca como parcialmente pronto
    - _Requisitos: 95.1, 95.2, 95.3, 95.4, 95.5, 95.6, 95.7_

  - [ ]* 28.16 Escrever teste de propriedade para a cobertura dos dezoito passos
    - **Property 171: Cobertura dos dezoito passos do ciclo de prova (`P17.22`)**
    - **Validates: Requirements 95.1, 95.2, 95.6**

- [ ] 29. Checkpoint — barreira completa de `D88`, ao fim da etapa 11
  - Executar a suíte inteira, `ruff`, `mypy --strict`, os onze meta-testes, os 44 testes de regressão, os quatro Golden Cases e o ciclo de prova nas duas portas; nenhum requisito `P1` ou `P2` entra sem que tudo isso esteja verde. Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 30. Etapa 12 — Os onze requisitos `P1`

  - [ ] 30.1 Implementar o enriquecimento progressivo
    - Implementar `PotencialPreliminar`, `potencial_preliminar` e `profundidade_de_enriquecimento`, derivando a profundidade de investigação das cinco faixas qualitativas de potencial e da posição no ranqueamento, nunca do escore de oportunidade, e registrando origem, data de obtenção e confiança de cada informação enriquecida
    - _Requisitos: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8_

  - [ ] 30.2 Implementar o financiamento
    - Implementar `modelo_de_financiamento` com condições, entrada, parcela, prazo e efeito no capital imobilizado e no retorno, respeitando os limites do perfil do investidor
    - _Requisitos: 31.1, 31.2, 31.3, 31.4, 31.5, 31.6_

  - [ ] 30.3 Implementar estratégias de saída e operações híbridas
    - Implementar `fluxo_de_estrategia_hibrida` com as etapas encadeadas e o resultado consolidado, e as estratégias de saída por público-alvo
    - _Requisitos: 42.1, 42.2, 42.3, 42.4_

  - [ ] 30.4 Implementar o monitoramento de liquidez
    - Monitorar a liquidez ao longo do tempo e disparar reavaliação quando a liquidez estimada muda materialmente
    - _Requisitos: 43.1, 43.2, 43.3, 43.4_

  - [ ] 30.5 Implementar a simulação de alocação antes da decisão
    - Implementar `simular_alocacao`, que projeta o efeito da candidata sobre capital, reserva, concentração e eficiência de capital antes de decidir
    - _Requisitos: 48.1, 48.2, 48.3, 48.4, 48.5_

  - [ ] 30.6 Implementar os alertas acionáveis
    - Criar `src/radar/monitoramento/alertas.py` com `CATALOGO_DE_ALERTAS` (`ALT-001` a `ALT-020`) e `emitir_alerta` com evento, impacto quantificado, consequência na tese, próxima ação, prioridade, agrupamento de alertas relacionados e silenciamento
    - _Requisitos: 59.1, 59.2, 59.3, 59.4, 59.5, 59.6, 59.7, 59.8, 59.9, 59.10_

  - [ ] 30.7 Implementar resultado real e backtest com antiviés temporal
    - Persistir os nove campos do resultado real e implementar `executar_backtest` com coortes, controle de sobreajuste e filtro de corte pela data da decisão, de modo que nenhum dado posterior entre no conjunto usado
    - _Requisitos: 60.1, 60.2, 60.3, 60.3.1, 60.4, 60.5, 60.6, 60.7, 60.8, 60.9, 60.10, 60.11_

  - [ ]* 30.8 Escrever teste de propriedade para o antiviés temporal
    - **Property 128: Antiviés temporal no backtest (`P13.6`)**
    - **Validates: Requirements 60.4, 60.5**

  - [ ] 30.9 Implementar o controle de qualidade das regras
    - Implementar os indicadores de qualidade de regra, a qualidade da evidência em cinco níveis e a revisão de regra com histórico
    - _Requisitos: 65.1, 65.1.1, 65.1.2, 65.1.3, 65.2, 65.3, 65.4, 65.5, 65.6_

  - [ ] 30.10 Implementar os relatórios de negócio
    - Implementar os relatórios de negócio com os elementos obrigatórios e a estrutura verificada por instantâneo, sempre em português
    - _Requisitos: 69.1, 69.2, 69.3, 69.4_

  - [ ] 30.11 Implementar os indicadores de aprendizado
    - Implementar os indicadores de aprendizado e a evolução da qualidade de evidência ao longo das análises
    - _Requisitos: 80.1, 80.2, 80.3, 80.4, 80.5_

  - [ ] 30.12 Implementar alocação, eficiência de capital e faixas de ação
    - Implementar `FAIXAS_DE_ACAO_POR_POSICAO` e as faixas de ação por posição no ranqueamento, com alocação-alvo e eficiência de capital
    - _Requisitos: 81.1, 81.2, 81.3, 81.4, 81.5_

- [ ] 31. Etapa 13 — O requisito `P2`: esteira de conhecimento e recuperação

  - [ ] 31.1 Implementar o segmento de conhecimento com os quinze tipos
    - Criar `src/radar/conhecimento/ingestao.py` com `SegmentoDeConhecimento`, `TipoDeSegmentoDeConhecimento` com **15** valores, os vinte metadados obrigatórios e `texto_fonte` e `parafrase` em campos **separados**
    - _Requisitos: 72.2, 72.3, 72.3.1, 72.3.2, 72.4_

  - [ ]* 31.2 Escrever teste de propriedade para os metadados obrigatórios
    - **Property 140: Metadados obrigatórios em todo segmento (`P15.1`)**
    - **Validates: Requirements 72.3, 72.4**

  - [ ]* 31.3 Escrever teste de propriedade para texto-fonte e paráfrase
    - **Property 149: Texto-fonte e paráfrase permanecem distinguíveis (`P16.6`)**
    - **Validates: Requirements 72.3.1, 72.3.2**

  - [ ] 31.4 Implementar a indexação idempotente
    - Implementar `indexar` com unicidade por extração e índice do segmento, de modo que reingerir o mesmo documento não duplique segmentos
    - _Requisitos: 72.1, 72.6_

  - [ ]* 31.5 Escrever teste de propriedade para a idempotência da reingestão
    - **Property 142: Idempotência da reingestão (`P15.3`)**
    - **Validates: Requirements 72.1**

  - [ ] 31.6 Exigir fonte e proveniência em segmento de regra jurídica
    - Rejeitar a indexação de segmento de regra jurídica sem fonte e proveniência
    - _Requisitos: 72.5_

  - [ ]* 31.7 Escrever teste de propriedade para a proveniência de regra jurídica
    - **Property 141: Regra jurídica exige fonte e proveniência (`P15.2`)**
    - **Validates: Requirements 72.5**

  - [ ] 31.8 Implementar as três camadas de memória
    - Criar `src/radar/conhecimento/recuperacao.py` com as três camadas de memória e a recuperação que marca todo item da memória histórica como **hipótese**, nunca como evidência atual
    - _Requisitos: 72.7, 72.8, 72.9_

  - [ ]* 31.9 Escrever teste de propriedade para a memória histórica
    - **Property 143: Memória histórica é sempre hipótese (`P15.4`)**
    - **Validates: Requirements 72.9**

  - [ ] 31.10 Reconstruir o índice vetorial após a carga
    - Criar ou reconstruir o índice vetorial depois da ingestão, com o dimensionamento pelo volume real, de modo que nenhum índice seja construído sobre tabela vazia
    - _Requisitos: 72.6_

- [ ] 32. Checkpoint final — suíte completa nas treze etapas
  - Executar a suíte inteira, `ruff`, `mypy --strict`, os onze meta-testes, as 171 propriedades, os 44 testes de regressão, os quatro Golden Cases, os testes marcados de banco e de fonte externa, e o ciclo de prova do MVP nas duas portas de entrada. Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

## Notes

- Tarefas marcadas com `*` são de teste e podem ser adiadas para acelerar o MVP; nenhuma tarefa de topo é opcional.
- Cada uma das **171** propriedades tem **exatamente uma** tarefa de teste, em arquivo próprio `testes/propriedades/test_propriedade_NNN.py`. Arquivo por propriedade é o que torna essas tarefas independentes entre si e paralelizáveis.
- `P7.12` não aparece como tarefa de propriedade: é contraexemplo verificado e entra como teste dirigido de entradas fixas na tarefa 8.28 (`REG-033`).
- As 13 etapas do plano preservam a ordem publicada: tarefas 1 a 15 cobrem os dez blocos da etapa 1 na ordem `1.1` a `1.10`; tarefas 16 a 29 cobrem as etapas 2 a 11 de `D88`; tarefas 30 e 31 cobrem as etapas 12 (`P1`) e 13 (`P2`).
- Ordem de construção e prioridade de requisito não se deduzem uma da outra: `R92` e `R93` são `P0` construídos nas tarefas 25 e 26.
- O primeiro marco funcional de `D88` fecha no checkpoint da tarefa 23, ao fim da etapa 7.
- A renomeação de `D72` é implementação: módulos na tarefa 1.5, esquema por migração versionada na tarefa 16.2, contrato de programação na tarefa 21.10 e interface na tarefa 22.8, com `MT-11` na barreira de integração desde a tarefa 1.8.
- Todo checkpoint executa a suíte inteira, `ruff` e `mypy --strict`; do checkpoint 17 em diante, também os testes marcados de banco.
- Os artefatos de arquitetura derivados são **não normativos**: nenhuma tarefa os toma como fonte, e produzi-los, se for o caso, é trabalho derivado desta spec.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.3", "1.4"] },
    { "id": 1, "tasks": ["1.5"] },
    { "id": 2, "tasks": ["1.6"] },
    { "id": 3, "tasks": ["1.7"] },
    { "id": 4, "tasks": ["1.8"] },
    { "id": 5, "tasks": ["1.9"] },
    { "id": 6, "tasks": ["2.1"] },
    { "id": 7, "tasks": ["2.6"] },
    { "id": 8, "tasks": ["2.9"] },
    { "id": 9, "tasks": ["2.11"] },
    { "id": 10, "tasks": ["2.2", "2.3", "2.4", "2.5", "2.7", "2.8", "2.10", "2.12"] },
    { "id": 11, "tasks": ["3"] },
    { "id": 12, "tasks": ["4.1", "4.2"] },
    { "id": 13, "tasks": ["4.8"] },
    { "id": 14, "tasks": ["4.15"] },
    { "id": 15, "tasks": ["4.16"] },
    { "id": 16, "tasks": ["4.20"] },
    { "id": 17, "tasks": ["4.29"] },
    { "id": 18, "tasks": ["4.31"] },
    { "id": 19, "tasks": ["4.32"] },
    { "id": 20, "tasks": ["4.3", "4.4", "4.5", "4.6", "4.7", "4.9", "4.10", "4.11", "4.12", "4.13", "4.14", "4.17", "4.18", "4.19", "4.21", "4.22", "4.23", "4.24", "4.25", "4.26", "4.27", "4.28", "4.30"] },
    { "id": 21, "tasks": ["5.1"] },
    { "id": 22, "tasks": ["5.8"] },
    { "id": 23, "tasks": ["5.9"] },
    { "id": 24, "tasks": ["5.10"] },
    { "id": 25, "tasks": ["5.11"] },
    { "id": 26, "tasks": ["5.13"] },
    { "id": 27, "tasks": ["5.15"] },
    { "id": 28, "tasks": ["5.16"] },
    { "id": 29, "tasks": ["5.18"] },
    { "id": 30, "tasks": ["5.2", "5.3", "5.4", "5.5", "5.6", "5.7", "5.12", "5.14", "5.17", "5.19", "5.20", "5.21", "5.22", "5.23"] },
    { "id": 31, "tasks": ["6"] },
    { "id": 32, "tasks": ["7.1"] },
    { "id": 33, "tasks": ["7.2"] },
    { "id": 34, "tasks": ["7.3"] },
    { "id": 35, "tasks": ["7.4"] },
    { "id": 36, "tasks": ["7.5"] },
    { "id": 37, "tasks": ["7.6"] },
    { "id": 38, "tasks": ["7.7"] },
    { "id": 39, "tasks": ["8.1"] },
    { "id": 40, "tasks": ["8.4"] },
    { "id": 41, "tasks": ["8.5"] },
    { "id": 42, "tasks": ["8.9"] },
    { "id": 43, "tasks": ["8.13"] },
    { "id": 44, "tasks": ["8.17"] },
    { "id": 45, "tasks": ["8.19"] },
    { "id": 46, "tasks": ["8.26"] },
    { "id": 47, "tasks": ["8.29"] },
    { "id": 48, "tasks": ["8.32"] },
    { "id": 49, "tasks": ["8.33"] },
    { "id": 50, "tasks": ["8.36"] },
    { "id": 51, "tasks": ["8.37"] },
    { "id": 52, "tasks": ["8.38"] },
    { "id": 53, "tasks": ["8.42"] },
    { "id": 54, "tasks": ["8.43"] },
    { "id": 55, "tasks": ["8.44"] },
    { "id": 56, "tasks": ["8.2", "8.3", "8.6", "8.7", "8.8", "8.10", "8.11", "8.12", "8.14", "8.15", "8.16", "8.18", "8.20", "8.21", "8.22", "8.23", "8.24", "8.25", "8.27", "8.28", "8.30", "8.31", "8.34", "8.35", "8.39", "8.40", "8.41"] },
    { "id": 57, "tasks": ["9"] },
    { "id": 58, "tasks": ["10.1"] },
    { "id": 59, "tasks": ["10.4"] },
    { "id": 60, "tasks": ["10.8"] },
    { "id": 61, "tasks": ["10.9"] },
    { "id": 62, "tasks": ["10.13"] },
    { "id": 63, "tasks": ["10.15"] },
    { "id": 64, "tasks": ["10.17"] },
    { "id": 65, "tasks": ["10.18"] },
    { "id": 66, "tasks": ["10.19"] },
    { "id": 67, "tasks": ["10.20"] },
    { "id": 68, "tasks": ["10.27"] },
    { "id": 69, "tasks": ["10.29"] },
    { "id": 70, "tasks": ["10.33"] },
    { "id": 71, "tasks": ["10.36"] },
    { "id": 72, "tasks": ["10.43"] },
    { "id": 73, "tasks": ["10.2", "10.3", "10.5", "10.6", "10.7", "10.10", "10.11", "10.12", "10.14", "10.16", "10.21", "10.22", "10.23", "10.24", "10.25", "10.26", "10.28", "10.30", "10.31", "10.32", "10.34", "10.35", "10.37", "10.38", "10.39", "10.40", "10.41", "10.42", "10.44"] },
    { "id": 74, "tasks": ["11.1"] },
    { "id": 75, "tasks": ["11.4"] },
    { "id": 76, "tasks": ["11.10"] },
    { "id": 77, "tasks": ["11.13"] },
    { "id": 78, "tasks": ["11.15"] },
    { "id": 79, "tasks": ["11.17"] },
    { "id": 80, "tasks": ["11.20"] },
    { "id": 81, "tasks": ["11.22"] },
    { "id": 82, "tasks": ["11.24"] },
    { "id": 83, "tasks": ["11.26"] },
    { "id": 84, "tasks": ["11.2", "11.3", "11.5", "11.6", "11.7", "11.8", "11.9", "11.11", "11.12", "11.14", "11.16", "11.18", "11.19", "11.21", "11.23", "11.25", "11.27"] },
    { "id": 85, "tasks": ["12"] },
    { "id": 86, "tasks": ["13.1"] },
    { "id": 87, "tasks": ["13.2"] },
    { "id": 88, "tasks": ["13.4"] },
    { "id": 89, "tasks": ["13.5"] },
    { "id": 90, "tasks": ["13.6"] },
    { "id": 91, "tasks": ["13.7"] },
    { "id": 92, "tasks": ["13.8"] },
    { "id": 93, "tasks": ["13.9"] },
    { "id": 94, "tasks": ["13.13"] },
    { "id": 95, "tasks": ["13.3", "13.10", "13.11", "13.12", "13.14", "13.15", "13.16", "13.17"] },
    { "id": 96, "tasks": ["14.1"] },
    { "id": 97, "tasks": ["14.5"] },
    { "id": 98, "tasks": ["14.8"] },
    { "id": 99, "tasks": ["14.9"] },
    { "id": 100, "tasks": ["14.10"] },
    { "id": 101, "tasks": ["14.12"] },
    { "id": 102, "tasks": ["14.13"] },
    { "id": 103, "tasks": ["14.15"] },
    { "id": 104, "tasks": ["14.2", "14.3", "14.4", "14.6", "14.7", "14.11", "14.14"] },
    { "id": 105, "tasks": ["15"] },
    { "id": 106, "tasks": ["16.1"] },
    { "id": 107, "tasks": ["16.2"] },
    { "id": 108, "tasks": ["16.3"] },
    { "id": 109, "tasks": ["16.4"] },
    { "id": 110, "tasks": ["16.5"] },
    { "id": 111, "tasks": ["16.6"] },
    { "id": 112, "tasks": ["16.7"] },
    { "id": 113, "tasks": ["16.10"] },
    { "id": 114, "tasks": ["16.13"] },
    { "id": 115, "tasks": ["16.15"] },
    { "id": 116, "tasks": ["16.16"] },
    { "id": 117, "tasks": ["16.18"] },
    { "id": 118, "tasks": ["16.8", "16.9", "16.11", "16.12", "16.14", "16.17", "16.19", "16.20", "16.21"] },
    { "id": 119, "tasks": ["17"] },
    { "id": 120, "tasks": ["18.1"] },
    { "id": 121, "tasks": ["18.3"] },
    { "id": 122, "tasks": ["18.5"] },
    { "id": 123, "tasks": ["18.7"] },
    { "id": 124, "tasks": ["18.9"] },
    { "id": 125, "tasks": ["18.10"] },
    { "id": 126, "tasks": ["18.12"] },
    { "id": 127, "tasks": ["18.13"] },
    { "id": 128, "tasks": ["18.2", "18.4", "18.6", "18.8", "18.11", "18.14", "18.15"] },
    { "id": 129, "tasks": ["19.1"] },
    { "id": 130, "tasks": ["19.2"] },
    { "id": 131, "tasks": ["19.4"] },
    { "id": 132, "tasks": ["19.5"] },
    { "id": 133, "tasks": ["19.6"] },
    { "id": 134, "tasks": ["19.7"] },
    { "id": 135, "tasks": ["19.3"] },
    { "id": 136, "tasks": ["20.1"] },
    { "id": 137, "tasks": ["20.2"] },
    { "id": 138, "tasks": ["20.4"] },
    { "id": 139, "tasks": ["20.8"] },
    { "id": 140, "tasks": ["20.10"] },
    { "id": 141, "tasks": ["20.12"] },
    { "id": 142, "tasks": ["20.13"] },
    { "id": 143, "tasks": ["20.3", "20.5", "20.6", "20.7", "20.9", "20.11"] },
    { "id": 144, "tasks": ["21.1"] },
    { "id": 145, "tasks": ["21.2"] },
    { "id": 146, "tasks": ["21.3"] },
    { "id": 147, "tasks": ["21.4"] },
    { "id": 148, "tasks": ["21.5"] },
    { "id": 149, "tasks": ["21.6"] },
    { "id": 150, "tasks": ["21.7"] },
    { "id": 151, "tasks": ["21.8"] },
    { "id": 152, "tasks": ["21.9"] },
    { "id": 153, "tasks": ["21.10"] },
    { "id": 154, "tasks": ["21.11"] },
    { "id": 155, "tasks": ["22.1"] },
    { "id": 156, "tasks": ["22.2"] },
    { "id": 157, "tasks": ["22.3"] },
    { "id": 158, "tasks": ["22.4"] },
    { "id": 159, "tasks": ["22.5"] },
    { "id": 160, "tasks": ["22.6"] },
    { "id": 161, "tasks": ["22.7"] },
    { "id": 162, "tasks": ["22.8"] },
    { "id": 163, "tasks": ["22.9"] },
    { "id": 164, "tasks": ["22.10"] },
    { "id": 165, "tasks": ["22.11"] },
    { "id": 166, "tasks": ["23"] },
    { "id": 167, "tasks": ["24.1"] },
    { "id": 168, "tasks": ["24.2"] },
    { "id": 169, "tasks": ["24.3"] },
    { "id": 170, "tasks": ["24.4"] },
    { "id": 171, "tasks": ["24.5"] },
    { "id": 172, "tasks": ["24.6"] },
    { "id": 173, "tasks": ["24.7", "24.8"] },
    { "id": 174, "tasks": ["25.1"] },
    { "id": 175, "tasks": ["25.3"] },
    { "id": 176, "tasks": ["25.5"] },
    { "id": 177, "tasks": ["25.7"] },
    { "id": 178, "tasks": ["25.8"] },
    { "id": 179, "tasks": ["25.9"] },
    { "id": 180, "tasks": ["25.2", "25.4", "25.6", "25.10"] },
    { "id": 181, "tasks": ["26.1"] },
    { "id": 182, "tasks": ["26.2"] },
    { "id": 183, "tasks": ["26.4"] },
    { "id": 184, "tasks": ["26.6"] },
    { "id": 185, "tasks": ["26.8"] },
    { "id": 186, "tasks": ["26.9"] },
    { "id": 187, "tasks": ["26.3", "26.5", "26.7"] },
    { "id": 188, "tasks": ["27"] },
    { "id": 189, "tasks": ["28.1"] },
    { "id": 190, "tasks": ["28.3"] },
    { "id": 191, "tasks": ["28.5"] },
    { "id": 192, "tasks": ["28.7"] },
    { "id": 193, "tasks": ["28.8"] },
    { "id": 194, "tasks": ["28.9"] },
    { "id": 195, "tasks": ["28.10"] },
    { "id": 196, "tasks": ["28.11"] },
    { "id": 197, "tasks": ["28.12"] },
    { "id": 198, "tasks": ["28.13"] },
    { "id": 199, "tasks": ["28.14"] },
    { "id": 200, "tasks": ["28.15"] },
    { "id": 201, "tasks": ["28.2", "28.4", "28.6", "28.16"] },
    { "id": 202, "tasks": ["29"] },
    { "id": 203, "tasks": ["30.1"] },
    { "id": 204, "tasks": ["30.2"] },
    { "id": 205, "tasks": ["30.3"] },
    { "id": 206, "tasks": ["30.4"] },
    { "id": 207, "tasks": ["30.5"] },
    { "id": 208, "tasks": ["30.6"] },
    { "id": 209, "tasks": ["30.7"] },
    { "id": 210, "tasks": ["30.9"] },
    { "id": 211, "tasks": ["30.10"] },
    { "id": 212, "tasks": ["30.11"] },
    { "id": 213, "tasks": ["30.12"] },
    { "id": 214, "tasks": ["30.8"] },
    { "id": 215, "tasks": ["31.1"] },
    { "id": 216, "tasks": ["31.4"] },
    { "id": 217, "tasks": ["31.6"] },
    { "id": 218, "tasks": ["31.8"] },
    { "id": 219, "tasks": ["31.10"] },
    { "id": 220, "tasks": ["31.2", "31.3", "31.5", "31.7", "31.9"] },
    { "id": 221, "tasks": ["32"] }
  ]
}
```
