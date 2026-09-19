# Implementation Plan: Radar Imobiliário — Especificação Completa

## Overview

Este plano converte o `design.md` desta spec em passos incrementais de código Python 3.12
sobre a fatia vertical já existente: `src/radar/**` (captura CAIXA, normalização, identidade,
gate jurídico parcial, motor de cálculo, motor de decisão, persistência e API, com 22 testes
passando em `tests/`), `db/schema.sql`, `scripts/**` e `pyproject.toml`. Persistência em
PostgreSQL 16 com pgvector, orquestração em LangGraph, API em FastAPI, testes de propriedade
com `hypothesis`, qualidade estática com `ruff` e `mypy --strict`.

A ordem das tarefas de topo é a da seção **Ordem de implementação recomendada** do design, nas
suas 15 etapas, e a regra de priorização é inviolável: **todas as tarefas que realizam
requisitos `P1` e `P2` vêm depois de todas as que realizam `P0`**. O único requisito `P2`
(`R72`, esteira de conhecimento e RAG) é a última etapa funcional, antes apenas dos Golden
Cases e das meta-verificações.

Uma observação sobre cobertura: a tabela de etapas do design não nomeia `R21` a `R25`
(mercado, comparáveis e valuation), embora sejam `P0` e sejam pré-requisito direto do desconto
líquido, da margem e do preço máximo. Eles são implementados na **cabeça da etapa 5**, antes
do custo econômico total, que os consome.

As **149 propriedades** da seção *Correctness Properties* do design têm, cada uma, exatamente
uma tarefa de teste de propriedade, posicionada logo depois da tarefa de implementação que a
torna verificável. As tarefas de teste são opcionais (`*`) e referenciam a propriedade pelo
número e pelo título exato do design.

Os documentos em `docs/`, `.kiro/_extracted/` e `spec/` não são fonte de trabalho: o
`requirements.md` é a única fonte normativa de negócio e o `design.md` é a única fonte
normativa de engenharia, incluindo o modelo físico de dados.

## Tasks

- [ ] 1. Fundação de tipos e infraestrutura de teste
  - [ ] 1.1 Criar o valor com estado de informação
    - Criar `src/radar/domain/informed.py` com `Informed[T]` congelado (valor, estado, fonte, data de observação, confiança, qualidade da evidência), o sentinela `Unknown` e `ProvisionalMetric[T]` carregando o motivo da provisoriedade
    - `value=None` com estado `UNKNOWN` é distinto de `value=0` com estado `CONFIRMED`; não existe construtor que produza zero a partir de ausência
    - _Requisitos: 3.2, 10.2, 26.7, 26.10, 27.8_

  - [ ] 1.2 Fechar os enums de domínio com as contagens de *Data Models*
    - Ampliar `src/radar/domain/enums.py` com todos os enums da tabela de enumerações do design e as contagens declaradas: `PipelinePhase` 16, `DecisionState` 6, `DecisionLayer` 11 (0 a 10), `Strategy` 6 com `customizada`, `AssetProfile` 9 com `desconhecido`, `OccupancyState` 7, `LiquidityCategory` 7, `ConfidenceLevel` 6, `EvidenceState` 6, `EvidenceQuality` 5, `UrgencyClass` 6, `AttractivenessClass` 5, `LegalStatus` 3, `P0Result` 5, `CheckOutcome` 5 com `NOT_APPLICABLE`, `IdentityLevel` 5, `SignalStrength` 6, `MatchVerdict` 3, `LocationClass` 5, `ComparableClass` 6, `AreaKind` 5, `ValuationMethod` 7, `RiskCategory` 10, `Probability` 3, `Impact` 4, `Severity` 4, `Mitigation` 6, `DDPhase` 8, `ChecklistOutcome` 6, `PendingPriority` 4, `ScenarioKind` 4, `Robustness` 6, `RenovationLevel` 5, `MonitoringState` 10, `Materiality` 5, `RuleType` 6, `ProfileGroup` 9, `DataGate` 8, `PreliminaryPotential` 5, `TargetPublic` 7, `CaptureState` 10, `PropertyState` 8, `SourceReliabilityClass` 6, `GovernanceStatus` 6, `KnowledgeSegmentType` 15
    - Substituir `legal_status: str` por `LegalStatus` em todos os módulos que o consomem
    - _Requisitos: 7.1, 9.6, 11.1, 12.5, 12.6, 18.1, 32.1, 32.6, 34.1, 34.3, 34.4, 36.1, 36.3, 37.2, 40.2, 44.1, 44.2, 52.6, 52.6.1, 53.1, 53.5, 54.1, 57.2, 57.10.1, 72.2_

  - [ ] 1.3 Criar a taxonomia de erros e o validador de fronteira
    - Criar `src/radar/domain/errors.py` com `RadarError` e as três famílias do design: entrada e contrato (`DomainValidationError`, `EnumBoundaryError`, `PreconditionError`, `AmbiguousInputError`); evidência e governança (`EvidenceSourceMissingError`, `EvidencePromotionError`, `ImmutabilityViolationError`, `ParameterNotInForceError`, `PendingDecisionParameterError`, `ExceptionOverBlockError`, `MissingDictionaryEntityError`); capacidade e infraestrutura (`NormalizerNotFoundError`, `SupervisionConfigError`, `UpstreamUnavailableError`)
    - Criar `src/radar/domain/boundary.py` com `parse_enum` que levanta `EnumBoundaryError` para valor fora do conjunto, inclusive variação de caixa e string vazia, e nunca devolve um default permissivo
    - _Requisitos: 12.5, 12.6, 79.9_

  - [ ]* 1.4 Escrever teste de propriedade para o enum de status jurídico
    - **Property 94: Enum de status jurídico é total e fechado (`P10.16`)**
    - **Validates: Requirements 12.5, 12.6**

  - [ ] 1.5 Implementar a classificação por faixa contínua
    - Criar `src/radar/domain/bands.py` com `classify_by_band(value, bands)`, faixas ordenadas por limite inferior decrescente e comparação `>=`, rejeitando na construção qualquer sequência que não cubra o limite inferior do domínio
    - Este é o ponto único de correção da lacuna de faixas e o ponto único de verificação de liquidez, score, fator de confiança, nível nomeado de confiança, aderência, impacto de prazo e margem adicional por prazo
    - _Requisitos: 40.2, 41.3, 44.4, 49.6, 50.3, 50.4_

  - [ ] 1.6 Montar a infraestrutura de teste de propriedade
    - Fixar `hypothesis` com pino exato em `pyproject.toml`, ao lado de `pytest`, `pytest-cov`, `ruff` e `mypy`
    - Criar os quatro perfis de execução: `dev` com 100 exemplos, `ci` com 500, `nightly` com 5.000 e banco de exemplos persistido, e `regression` reexecutando todo contraexemplo já encontrado
    - Criar `tests/generators/` com os geradores compartilhados: `money`, `area`, `percent`, `br_datetime`, `raw_payload`, `normalized_listing`, `identity_signals`, `check_results`, `cost_breakdown`, `economic_inputs`, `max_price_inputs`, `scenario_premises`, `risk_record`, `liquidity_factors`, `score_factors`, `weight_set`, `decision_input`, `pending_set`, `portfolio_state`, `bid_checklist`, `knowledge_segment`, `parameter_hierarchy`
    - Injetar os valores de fronteira obrigatórios em todo gerador de escala: 89,5 · 79,5 · 74,5 · 69,5 · 59,5 · 49,5 · 39,5 · `"47.76"` · `"191651.31"` · `"2,5%"` · `"2.5%"` · `1` com unidade de porcentagem · e o valor exato de cada limiar de materialidade, de estratégia e de confiança
    - Adotar a etiqueta `Feature: radar-imobiliario-especificacao-completa, Property {n}: {texto}` como comentário obrigatório de cada teste de propriedade
    - _Requisitos: 73.1, 73.7_

  - [ ] 1.7 Criar o esqueleto dos dez meta-testes
    - Criar `tests/meta/` com `MT-01` a `MT-10` executáveis e falhando por ausência de alvo, não por erro de importação: rastreabilidade de propriedades, um teste por propriedade, cobertura de checklists, cobertura de regras, cobertura de disciplina de lance, cobertura de prioridade, ponto único de verdade dos thresholds, soma de pesos, contagem de enums e isolamento da camada de IA
    - `MT-09` já verifica as contagens declaradas na tarefa 1.2; `MT-02` já conhece a numeração de 1 a 149
    - _Requisitos: 73.2, 73.3, 73.4, 73.5, 73.6, 73.8, 75.5_

- [ ] 2. Correções numéricas verificadas
  - [ ] 2.1 Reescrever a interpretação numérica sem heurística de magnitude
    - Reescrever `src/radar/capture/parsing.py` com `NumberFormat` (`PT_BR`, `PLAIN`, `AUTO`) e `parse_decimal(raw, fmt) -> Informed[Decimal]` aplicando as quatro regras de `AUTO` em ordem: vírgula presente é decimal; ponto único seguido de 1 ou 2 dígitos é decimal; ponto único seguido de exatamente 3 dígitos com grupo curto à esquerda é ambíguo e resulta em `UNKNOWN`; múltiplos pontos são milhar
    - Nenhuma decisão por magnitude e nenhum retorno zero para entrada não interpretável
    - _Requisitos: 3.2, 3.4, 3.4.1, 3.4.4_

  - [ ]* 2.2 Escrever teste de propriedade para invariância de magnitude
    - **Property 15: Invariância de magnitude na interpretação numérica (`P2.10`)**
    - **Validates: Requirements 3.4.1**

  - [ ]* 2.3 Escrever teste de propriedade para entrada não interpretável
    - **Property 17: Entrada não interpretável resulta em UNKNOWN (`P2.12`)**
    - **Validates: Requirements 3.2, 3.4.4**

  - [ ] 2.4 Exigir a unidade na interpretação de percentual
    - Implementar `PercentUnit` (`FRACTION`, `PERCENT`) e `parse_percent(raw, unit) -> Informed[Decimal]` com a unidade obrigatória no contrato, sem heurística de magnitude; o sufixo `%` presente no texto deve concordar com a unidade declarada, e a discordância é erro de entrada
    - _Requisitos: 3.4.2, 3.4.3_

  - [ ]* 2.5 Escrever teste de propriedade para percentual com unidade
    - **Property 16: Percentual normalizado com unidade respeitada (`P2.11`)**
    - **Validates: Requirements 3.4.2, 3.4.3**

  - [ ] 2.6 Implementar data brasileira e formatadores canônicos
    - Implementar `parse_datetime_br` para `dd/mm/aaaa` e `dd/mm/aaaa hh:mm`, e os formatadores canônicos de moeda, área, percentual e data que fecham o ciclo com os interpretadores
    - _Requisitos: 3.4_

  - [ ]* 2.7 Escrever teste de propriedade para o ciclo monetário
    - **Property 7: Round-trip monetário (`P2.2`)**
    - **Validates: Requirements 3.4**

  - [ ]* 2.8 Escrever teste de propriedade para o ciclo de área
    - **Property 8: Round-trip de área (`P2.3`)**
    - **Validates: Requirements 3.4**

  - [ ]* 2.9 Escrever teste de propriedade para o ciclo de percentual
    - **Property 9: Round-trip de percentual (`P2.4`)**
    - **Validates: Requirements 3.4**

  - [ ]* 2.10 Escrever teste de propriedade para o ciclo de data
    - **Property 10: Round-trip de data e data com hora (`P2.5`)**
    - **Validates: Requirements 3.4**

  - [ ] 2.11 Trocar `float` por `Decimal` em todo o caminho monetário
    - Converter `src/radar/engines/calculation.py`, `src/radar/domain/models.py` e os esquemas de `src/radar/api/main.py` para `Decimal`, sem nenhum `float` atravessando a fronteira
    - _Requisitos: 26.11, 27.17_

  - [ ] 2.12 Corrigir o retorno anualizado e suas pré-condições
    - Implementar `annualized_roi(roi, months) = (1 + roi)^(12 ÷ meses) − 1` em `calculation.py`; prazo menor ou igual a zero levanta erro de dado de entrada, nunca devolve infinito nem zero
    - Este é o valor comparável com o retorno mínimo exigido; o ROI do período não é
    - _Requisitos: 30.3, 30.3.1, 30.3.2_

  - [ ] 2.13 Migrar as faixas existentes para o classificador único
    - Substituir todo teste de faixa escrito como intervalo fechado de inteiros por `classify_by_band`, incluindo as faixas de score e os níveis de confiança hoje em `src/radar/domain/parameters.py`
    - _Requisitos: 49.6, 50.3, 50.4_

- [ ] 3. Checkpoint — fundação e correções numéricas
  - Executar a suíte inteira, `ruff` e `mypy --strict`; garantir que os 22 testes existentes continuam passando após a troca para `Decimal`. Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 4. Captura idempotente e normalização por fonte
  - [ ] 4.1 Criar o registro de fontes
    - Criar `src/radar/capture/sources.py` com `SourceRegistry`: fonte como entidade própria com tipo, nome, URL, abrangência, periodicidade, campos disponíveis, confiabilidade 0–100, situação e data da última captura; oito tipos de fonte aceitos; confiabilidade por categoria de dado nas classes A, B, C, D, E e U; entrada manual do analista marcada como interpretação com autor registrado; desativação preserva as capturas e interrompe novas
    - _Requisitos: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

  - [ ] 4.2 Implementar o fingerprint canônico da captura
    - Implementar `fingerprint(payload)` com SHA-256 sobre serialização canônica: chaves ordenadas, separadores fixos e unicode em NFC
    - _Requisitos: 2.1, 2.2_

  - [ ]* 4.3 Escrever teste de propriedade para invariância à ordem das chaves
    - **Property 1: Fingerprint invariante à ordem das chaves (`P1.1`)**
    - **Validates: Requirements 2.2**

  - [ ]* 4.4 Escrever teste de propriedade para determinismo do fingerprint
    - **Property 2: Fingerprint determinístico (`P1.2`)**
    - **Validates: Requirements 2.2**

  - [ ]* 4.5 Escrever teste de propriedade para distinção de conteúdos
    - **Property 3: Fingerprint distingue conteúdos distintos (`P1.3`)**
    - **Validates: Requirements 2.2**

  - [ ] 4.6 Persistir a captura de forma idempotente
    - Criar `src/radar/capture/capture_service.py` com `CaptureService.record` usando `INSERT ... ON CONFLICT (source_id, hash) DO NOTHING RETURNING` seguido de leitura, de modo que a idempotência seja do banco; `supersede` cria nova captura e move a anterior para `Superseded`, que permanece consultável; preço e status são gravados exatamente como informados, ao lado das versões normalizadas, com as referências a imagens e documentos e a data de observação
    - Hoje o fingerprint é calculado e descartado e nenhum código insere em `captures`
    - _Requisitos: 2.3, 2.4, 2.5, 2.6, 2.7_

  - [ ]* 4.7 Escrever teste de propriedade para idempotência do registro
    - **Property 4: Idempotência do registro de captura (`P1.4`)**
    - **Validates: Requirements 2.3**

  - [ ]* 4.8 Escrever teste de propriedade para captura append-only
    - **Property 5: Captura é append-only (`P1.5`)**
    - **Validates: Requirements 2.4, 2.5**

  - [ ] 4.9 Despachar o normalizador por tipo de fonte
    - Criar `src/radar/capture/normalizers/base.py` com o protocolo `Normalizer` e o registro `NORMALIZERS`, mover o normalizador atual para `normalizers/caixa.py` e fazer `normalize(capture)` despachar por `capture.source_type`, levantando `NormalizerNotFoundError` para fonte sem normalizador registrado
    - Hoje o nó de normalização chama o normalizador da CAIXA incondicionalmente
    - _Requisitos: 1.1, 3.1, 3.6, 3.7_

  - [ ] 4.10 Normalizar sem inventar dado
    - Estruturar `NormalizedListing` com identificação, localização, características físicas, dados do certame, condições comerciais e ocupação; campo ausente é `UNKNOWN` explícito; o valor original de cada campo é preservado; o tipo de área é registrado e nunca inferido; a avaliação da fonte tem campo próprio sem nenhum caminho para o valor de mercado; a lista de campos ausentes é emitida; a oferta normalizada é persistida vinculada à captura de origem
    - Acrescentar `banheiros` à caracterização física e `complemento` ao endereço, distinto de logradouro, número e unidade
    - _Requisitos: 3.1, 3.2, 3.3, 3.5, 3.9, 3.10, 3.11, 74.9, 74.10_

  - [ ] 4.11 Corrigir a distinção ocupado/desocupado
    - Substituir a verificação por subcadeia por tokenização e léxico ordenado em que os termos de vacância têm precedência sobre os de ocupação
    - _Requisitos: 3.8_

  - [ ]* 4.12 Escrever teste de propriedade para campo ausente
    - **Property 6: Campo ausente resulta em UNKNOWN (`P2.1`)**
    - **Validates: Requirements 3.2**

  - [ ]* 4.13 Escrever teste de propriedade para idempotência da normalização
    - **Property 11: Idempotência da normalização (`P2.6`)**
    - **Validates: Requirements 3.1, 3.11**

  - [ ]* 4.14 Escrever teste de propriedade para a lista de ausências
    - **Property 12: Lista de ausências é exata (`P2.7`)**
    - **Validates: Requirements 3.9**

  - [ ]* 4.15 Escrever teste de propriedade para a avaliação da fonte
    - **Property 13: Avaliação da fonte nunca vira valor de mercado (`P2.8`)**
    - **Validates: Requirements 3.10**

  - [ ]* 4.16 Escrever teste de propriedade para o tipo de área
    - **Property 14: Tipo de área nunca é inferido (`P2.9`)**
    - **Validates: Requirements 3.5**

  - [ ]* 4.17 Escrever teste de propriedade para precedência de vacância
    - **Property 18: Precedência de vacância sobre ocupação (`P2.13`)**
    - **Validates: Requirements 3.8**

- [ ] 5. Gates de dados, identidade e deduplicação
  - [ ] 5.1 Implementar os oito gates de dados e a qualificação
    - Criar `src/radar/pipeline/qualification.py` com `evaluate_data_gates` avaliando `G0` a `G7` em ordem e devolvendo o primeiro gate não satisfeito mais exatamente qual informação falta, com o impacto de cada ausência classificado em baixo, medio, alto ou critico e a redução da confiança da dimensão correspondente
    - O gate `G1` materializa a fase `QUALIFIED`, que hoje não existe em execução
    - _Requisitos: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 4.10_

  - [ ] 5.2 Ampliar o resolvedor de identidade para I0 a I4
    - Ampliar `src/radar/pipeline/identity.py` com `IdentitySignal`, a ordem decrescente de força dos sinais e o conjunto proibido para identidade (preço, avaliação da fonte, desconto); resolver exatamente um nível de `I0` a `I4` de forma monotônica na força dos sinais; imagem semelhante é sinal complementar, nunca isolado; cada identificador é registrado com confiança; conflito material de identificadores resulta em `PENDENTE`
    - Consolidar o limiar de elegibilidade `I2` em um único lugar, `meets_eligibility_threshold`, eliminando a divergência entre o `>= I3` não consumido e o `>= I2` da orquestração
    - _Requisitos: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.12_

  - [ ]* 5.3 Escrever teste de propriedade para totalidade da identidade
    - **Property 19: Resolução de identidade é total (`P3.1`)**
    - **Validates: Requirements 7.1**

  - [ ]* 5.4 Escrever teste de propriedade para monotonicidade dos sinais
    - **Property 20: Monotonicidade na força dos sinais (`P3.2`)**
    - **Validates: Requirements 7.2, 7.3, 7.4, 7.5, 7.6**

  - [ ]* 5.5 Escrever teste de propriedade para invariância ao preço
    - **Property 21: Identidade é invariante ao preço (`P3.3`)**
    - **Validates: Requirements 7.7**

  - [ ] 5.6 Implementar a chave conceitual de identidade
    - Implementar `conceptual_key` com a primeira combinação disponível na ordem canônica: matrícula; identificador oficial da fonte; município com logradouro, número e unidade; condomínio com bloco e unidade. Sem identificador forte, usar endereço, área, quartos e vagas e marcar o resultado como provável. Endereço conhecido com unidade desconhecida limita a identidade a `I2` e abre pendência de identificação da unidade
    - _Requisitos: 8.1, 8.2, 8.3, 8.4_

  - [ ] 5.7 Criar o deduplicador com veredito de três valores
    - Criar `src/radar/pipeline/dedup.py` com `MatchVerdict` (`same`, `different`, `undetermined`) e `is_same_property` simétrica e reflexiva: matrícula é decisiva; evidência insuficiente devolve `undetermined`; unidades distintas do mesmo condomínio devolvem `different`; preço, avaliação e desconto são sinais inválidos; elevar `undetermined` a provável exige dois sinais complementares de peso medio, e sinais fracos nunca elevam o veredito
    - _Requisitos: 9.1, 9.2, 9.3, 9.4, 9.5, 9.5.1, 9.5.2, 9.6, 9.11_

  - [ ]* 5.8 Escrever teste de propriedade para invariância ao preço na deduplicação
    - **Property 22: Deduplicação é invariante ao preço (`P3.4`)**
    - **Validates: Requirements 9.5**

  - [ ]* 5.9 Escrever teste de propriedade para o caráter decisivo da matrícula
    - **Property 23: Matrícula é decisiva (`P3.5`)**
    - **Validates: Requirements 9.1**

  - [ ]* 5.10 Escrever teste de propriedade para simetria do veredito
    - **Property 24: Simetria do veredito (`P3.6`)**
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5, 9.6**

  - [ ]* 5.11 Escrever teste de propriedade para reflexividade do veredito
    - **Property 25: Reflexividade do veredito (`P3.7`)**
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5, 9.6**

  - [ ]* 5.12 Escrever teste de propriedade para unidades distintas
    - **Property 27: Unidades distintas nunca são fundidas (`P3.9`)**
    - **Validates: Requirements 9.11**

  - [ ]* 5.13 Escrever teste de propriedade para evidência insuficiente
    - **Property 28: Evidência insuficiente resulta em veredito indefinido (`P3.10`)**
    - **Validates: Requirements 9.6**

  - [ ] 5.14 Implementar o vínculo captura ↔ imóvel
    - Implementar `PropertyLinker` com `link` idempotente por par de captura e imóvel, fusão definitiva apenas com evidência decisiva ou muito forte, vínculo reversível com solicitação de validação para correspondência provável, registro de sinais coincidentes e divergentes, fontes comparadas, confiança e validação manual; `unlink` preserva o histórico e o motivo; `rematch_republished` tenta o imóvel histórico antes de criar um novo
    - _Requisitos: 9.7, 9.8, 9.9, 9.10, 9.12_

  - [ ]* 5.15 Escrever teste de propriedade para idempotência da associação
    - **Property 26: Idempotência da associação (`P3.8`)**
    - **Validates: Requirements 9.7**

  - [ ]* 5.16 Escrever teste de propriedade para preservação do histórico de associação
    - **Property 29: Desfazer associação preserva histórico (`P3.11`)**
    - **Validates: Requirements 9.9**

- [ ] 6. Perfil consolidado, divergências e localização
  - [ ] 6.1 Consolidar o perfil do imóvel em nove grupos
    - Criar `src/radar/pipeline/profile.py` com `consolidate_profile`: cada campo recebe exatamente um estado de informação e registra a fonte que o sustentou; inferência marca `INFERRED` e registra a premissa; o perfil é versionado com numeração crescente, data, autor, campos alterados e motivo, sem sobrescrita; os nove grupos incluem Condominial, Ocupacional e Qualidade com estado de conservação, nível de reforma estimado, padrão construtivo e idade aparente
    - _Requisitos: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.8, 10.9, 10.10, 10.11, 74.4_

  - [ ]* 6.2 Escrever teste de propriedade para o estado de informação
    - **Property 42: Todo valor tem exatamente um estado de informação (`P5.5`)**
    - **Validates: Requirements 10.2**

  - [ ] 6.3 Registrar o histórico de preços como entidade própria
    - Emitir observações de preço com valor, moeda, data de observação, fonte, tipo de preço e variação em relação à observação anterior, alimentando os gatilhos de mudança de preço
    - _Requisitos: 10.7, 74.5_

  - [ ] 6.4 Classificar e preservar divergências entre fontes
    - Implementar `classify_divergence` e a entidade Divergência com data, fonte A, informação A, fonte B, informação B, dimensão afetada, materialidade e impacto na decisão: divergência de valor de mercado acima do limiar é material, gera pendência e reduz a confiança; ocupação divergente gera pendência crítica; status divergente adota o mais recente como vigente, preserva o anterior e emite evento de mudança; divergência entre fonte oficial e anúncio registra o critério de priorização aplicado; matrícula divergente mantém registros separados como conflito de identidade
    - _Requisitos: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 74.6_

  - [ ] 6.5 Classificar a localização como entidade própria
    - Criar `src/radar/pipeline/location.py` com `classify_location` devolvendo exatamente uma classe de A a E, derivada apenas dos parâmetros de localização vigentes, sem nome de bairro embutido no produto; avaliar segurança, serviços, comércio, transporte, acesso, infraestrutura, perfil de demanda, faixa de preço predominante e liquidez regional como dimensões independentes; manter o perfil socioeconômico como dimensão informativa, separada de liquidez, risco e qualidade; um único indicador desfavorável reduz a dimensão e mantém a oportunidade elegível
    - Persistir Localização com endereço, região, classe, perfil de demanda, liquidez regional e faixa de preço predominante
    - _Requisitos: 11.1, 11.2, 11.6, 11.7, 11.8, 74.1_

- [ ] 7. Camada de evidência append-only e fronteira da IA
  - [ ] 7.1 Criar o repositório de evidências
    - Criar `src/radar/evidence/store.py` com `EvidenceStore.append` gravando regra, fonte, documento, localização exata, fato, valor, estado, confiança, qualidade da evidência, autor, data de observação e data de extração; rejeitar evidência sem fonte identificada; nunca atualizar nem remover; fatos com evidências contraditórias vêm marcados como conflitantes com todas as evidências preservadas
    - _Requisitos: 20.1, 20.2, 20.3, 20.5, 20.6, 65.1.1, 65.1.3_

  - [ ]* 7.2 Escrever teste de propriedade para evidência sem fonte
    - **Property 38: Evidência sem fonte é rejeitada (`P5.1`)**
    - **Validates: Requirements 20.3**

  - [ ]* 7.3 Escrever teste de propriedade para monotonicidade do repositório
    - **Property 40: Monotonicidade do repositório de evidências (`P5.3`)**
    - **Validates: Requirements 20.5, 20.6**

  - [ ]* 7.4 Escrever teste de propriedade para preservação de contradições
    - **Property 41: Contradições são preservadas (`P5.4`)**
    - **Validates: Requirements 20.5**

  - [ ] 7.5 Controlar a transição de estado dos fatos
    - Implementar `transition_fact` exigindo identificador de evidência de suporte para levar um fato de `UNKNOWN` a `CONFIRMED`, levantando `EvidencePromotionError` em qualquer outro caminho
    - _Requisitos: 20.4_

  - [ ]* 7.6 Escrever teste de propriedade para promoção de estado
    - **Property 39: UNKNOWN não vira CONFIRMED sem suporte (`P5.2`)**
    - **Validates: Requirements 20.4**

  - [ ] 7.7 Separar proposta de evidência de evidência
    - Criar `src/radar/evidence/proposals.py` com `EvidenceProposal` (fato afirmado, documento, localização exata, confiança da extração, produtor) como único artefato que um agente produz, e `promote` admitindo exatamente dois caminhos: ato humano registrado ou regra determinística explicitamente declarada
    - _Requisitos: 20.4, 71.5, 71.6, 83.1, 83.2, 83.3_

- [ ] 8. Gate jurídico — 19 verificações declarativas
  - [ ] 8.1 Declarar as dezenove verificações como dados
    - Ampliar `src/radar/pipeline/legal_gate.py` e criar `src/radar/rules/legal/` com `LEGAL_CHECKS` contendo exatamente 19 entradas: `RULE-JUR-001` a `RULE-JUR-013`, `RULE-ED-001` a `RULE-ED-004` e `RULE-ID-001` e `RULE-ID-002`
    - Cada `LegalCheckSpec` traz código da regra, itens de checklist vinculados, obrigatoriedade, resultado devido em `UNKNOWN` (nunca regular comprovado), resultado devido em `IRREGULAR`, evidências exigidas e qualidade mínima de evidência
    - Registrar o crosswalk `GATE-JUR-001` a `GATE-JUR-006` para as regras canônicas e mover `RULE-OCC-001`, `RULE-OCC-002`, `RULE-LOC-001` e `RULE-LOC-002` para a camada 6 de risco; a família `RULE-REG-*` não existe e não é declarada
    - _Requisitos: 12.4, 12.5, 12.6, 12.9, 12.10, 12.11_

  - [ ] 8.2 Agregar o resultado do gate de forma determinística e confluente
    - Implementar `evaluate_legal_gate` com a precedência: qualquer `IRREGULAR` produz `BLOCK`; senão qualquer obrigatória `UNKNOWN` produz `PENDENTE`; senão `RISCO_JURIDICO` havendo sinal; senão `REGULAR_COMPROVADO`. Mapear `P0Result` para `LegalStatus` de forma total
    - Emitir exatamente uma evidência por verificação avaliada, inclusive `UNKNOWN`; corrigir a confiança da evidência, que hoje é alta apenas quando o resultado é favorável: irregularidade comprovada é evidência decisiva e recebe estado `CONFIRMED` com confiança alta
    - Manter `NOT_APPLICABLE` distinto de `UNKNOWN`, e passar a consumir o efeito bloqueante do resultado, hoje calculado e ignorado
    - _Requisitos: 12.1, 12.5, 12.6, 20.1, 20.7_

  - [ ]* 8.3 Escrever teste de propriedade para determinismo do gate
    - **Property 30: Determinismo do gate jurídico (`P4.1`)**
    - **Validates: Requirements 12.5, 12.6**

  - [ ]* 8.4 Escrever teste de propriedade para confluência do gate
    - **Property 31: Confluência do gate jurídico (`P4.2`)**
    - **Validates: Requirements 12.1, 12.5**

  - [ ]* 8.5 Escrever teste de propriedade para irregularidade
    - **Property 32: Irregularidade implica BLOCK (`P4.3`)**
    - **Validates: Requirements 12.6, 13.4**

  - [ ]* 8.6 Escrever teste de propriedade para ausência de evidência
    - **Property 33: Ausência de evidência nunca produz OK (`P4.4`)**
    - **Validates: Requirements 12.6, 20.7**

  - [ ]* 8.7 Escrever teste de propriedade para evidência por verificação
    - **Property 34: Uma evidência por verificação avaliada (`P4.5`)**
    - **Validates: Requirements 20.1, 20.7**

  - [ ] 8.8 Implementar as verificações registrais e de titularidade
    - Implementar `check_registry` cobrindo `RULE-ID-002`, `RULE-JUR-012` e `RULE-JUR-013`: matrícula ausente produz `PENDENTE` com pendência de certidão; validade da certidão até mudança registral, com revalidação obrigatória antes da compra e pendência crítica que impede `BUY` quando não realizada; conflito material de titularidade produz `BLOCK`; a consolidação registra ato, data e **texto integral**, e as declarações sobre intimação e purgação são extraídas como evidência com localização exata; consolidação comprovada comprova o ato na data e mantém desconhecidos os fatos posteriores; gravame histórico baixado é distinguido de gravame atual; constrição vigente que impeça a transferência produz `BLOCK`
    - Implementar `NegativeAuctionRecordState` com os quatro estados e tratar averbação `em_tratamento` como pendência registral com custo e prazo no custo econômico total, sem bloqueio por esta situação; vaga com matrícula autônoma e abrangência indeterminada produz `PENDENTE`
    - _Requisitos: 13.2, 13.3, 13.3.2, 13.4, 13.6, 13.8, 13.9, 13.10, 13.11, 13.12, 13.13, 13.14_

  - [ ] 8.9 Verificar mora, intimações e cronologia
    - Implementar as verificações de constituição em mora e de intimações avaliando a exigibilidade conforme a modalidade e o caso concreto, sem presumir exigência nem dispensa; verificar a cronologia mora → consolidação → leilão como ordenação de datas conhecidas, com data ausente produzindo `PENDENTE` e nunca coerência presumida
    - _Requisitos: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7, 14.8, 14.9, 14.10, 15.4_

  - [ ] 8.10 Verificar o edital e a coerência do certame
    - Implementar a leitura do edital confrontada com a matrícula, o registro das cláusulas que alteram custo, prazo, posse ou obrigações do arrematante, e `check_portal_edital_divergence`, que emite `PENDENTE` com as duas informações e suas origens registradas quando divergem data, horário, plataforma, leiloeiro ou valor mínimo
    - _Requisitos: 15.1, 15.2, 15.3, 15.5, 15.6, 15.7, 15.11, 15.12, 15.13_

  - [ ] 8.11 Distinguir os dois casos de evicção
    - Implementar `check_eviction` com `EvictionOutcome` de três valores: cláusula confirmada; cláusula comprovadamente ausente no edital obtido, que produz `BLOCK` e impede o lance; cláusula não verificada, que produz `PENDENTE`, impede `BUY` e impede o lance. Os dois casos são distinguíveis no registro e na explicação. Registrar item e página, e as limitações e ressalvas uma a uma, elevando risco e contingência. Avaliar `E01` a `E09`
    - _Requisitos: 15.8, 15.9, 15.9.1, 15.9.2, 15.10_

  - [ ]* 8.12 Escrever teste de propriedade para evidência de ausência
    - **Property 116: Evidência de ausência produz o efeito da regra (`P11.18`)**
    - **Validates: Requirements 15.9, 15.9.1, 15.9.2**

  - [ ] 8.13 Classificar processos judiciais pelo impacto
    - Implementar `ProcessImpact` com quatro níveis e `classify_process`: impedimento material sem mitigação comprovada produz `BLOCK`; potencial e material mitigável produzem risco jurídico com condição de mitigação; a existência isolada de processo nunca produz `BLOCK`; liminar que atinge o leilão produz `BLOCK` até resolução ou mitigação
    - _Requisitos: 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 16.8_

  - [ ]* 8.14 Escrever teste de propriedade para processo sem impacto material
    - **Property 37: Processo sem impacto material nunca bloqueia (`P4.8`)**
    - **Validates: Requirements 16.6**

  - [ ] 8.15 Implementar os sinais jurídicos de investigação obrigatória
    - Implementar `legal_signals` cobrindo `RULE-JUR-009` a `RULE-JUR-011`: quitação elevada registra sinal e risco alto sem bloqueio isolado; bem residencial em garantia de dívida de terceiro produz `PENDENTE` ou `BLOCK` conforme a evidência; segundo leilão abaixo da metade da avaliação emite alerta, exige validação da modalidade e reduz a confiança jurídica sem bloqueio isolado; constrição sobre os direitos do devedor fiduciante produz `BLOCK` quando impeditiva; cada sinal é evidência com proveniência, estado e localização documental
    - _Requisitos: 17.1, 17.2, 17.3, 17.4, 17.5_

  - [ ] 8.16 Tratar ocupação como risco, com os dois casos de camada 0
    - Implementar `OccupancyState` com os sete estados e `assess_occupancy`: ocupado produz risco de posse de severidade alto e nunca é tratado como nulidade do procedimento; impacto crítico sem estratégia de desocupação e posse litigiosa com evidência de litígio produzem severidade crítica e bloqueio pela camada 0; livre não confirmado reduz a confiança e abre pendência de confirmação, sem tratar o imóvel como desocupado comprovado; desconhecido abre pendência de prioridade alta, nunca crítica, com contingência de desocupação e continuidade da análise; desocupado comprovado não registra risco de posse; o risco de posse é categoria distinta do risco de nulidade em todo registro
    - _Requisitos: 18.1, 18.2, 18.2.1, 18.2.2, 18.2.3, 18.3, 18.3.1, 18.4, 18.8_

  - [ ]* 8.17 Escrever teste de propriedade para independência da ocupação
    - **Property 36: Ocupação nunca altera o status jurídico (`P4.7`)**
    - **Validates: Requirements 18.2, 18.8**

  - [ ] 8.18 Avaliar locação e efeitos perante o adquirente
    - Implementar as verificações de locação: existência de contrato, cláusula de vigência averbada na matrícula, prazo e efeitos perante o adquirente, sem presumir nulidade pela existência de inquilino, e calcular o impacto da locação sobre posse, prazo de saída e rentabilidade para o cenário econômico
    - _Requisitos: 19.1, 19.2, 19.3, 19.4, 19.5, 19.6_

  - [ ] 8.19 Declarar o Anexo A e as verificações complementares como dados
    - Declarar `MC-001` a `MC-136` e `B-01` a `B-27` como catálogo enumerável ligado às verificações do gate, cada item com fase, criticidade, regra de origem, condição de aprovação, condição de reprovação e o resultado devido na ausência de evidência
    - _Requisitos: 12.11, 36.5_

  - [ ]* 8.20 Escrever teste de propriedade para cobertura do Anexo A
    - **Property 35: Cobertura total do Anexo A (`P4.6`)**
    - **Validates: Requirements 36.5**

- [ ] 9. Checkpoint — gate jurídico e camada de evidência
  - Executar a suíte inteira, `ruff` e `mypy --strict`; confirmar que nenhuma ausência de informação jurídica produz liberação e que o efeito bloqueante do gate é consumido pela orquestração e pelo motor de decisão. Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 10. Mercado, comparáveis e valuation
  - [ ] 10.1 Selecionar e qualificar comparáveis
    - Criar `src/radar/engines/comparables.py` com `select_comparables` na ordem de prioridade canônica (transações realizadas; ofertas muito semelhantes e recentes no mesmo condomínio; mesma microárea; mesmo bairro; regiões próximas), restrito aos limites de raio e janela salvo exceção registrada; distinguir preço anunciado de transacionado em todo registro e cálculo, com amostra só de anunciados reduzindo a confiança; excluir erro evidente e segmento incompatível com motivo; identificar outliers por um critério declarado e registrar, para cada um, a decisão de excluir ou ajustar com justificativa; outlier repetido registra hipótese de submercado distinto como pendência; idade do anúncio acima do limite exclui e, entre a metade e o limite, aplica a penalidade declarada
    - _Requisitos: 21.1, 21.4, 21.5, 21.6, 21.7, 21.8, 21.9, 21.10.2_

  - [ ] 10.2 Aplicar ajustes e comparar áreas do mesmo tipo
    - Implementar `apply_adjustments` com ajustes explícitos e registrados para área, quartos, vagas, padrão construtivo, estado de conservação, andar, posição, condomínio, localização e data, sendo o ajuste por estado de conservação obrigatório e o estado desconhecido de qualquer lado gerando pendência e redução de confiança; implementar `price_per_m2` que só compara áreas do mesmo tipo e resulta em pendência quando o tipo é desconhecido em qualquer dos lados
    - _Requisitos: 21.10, 21.10.1, 21.11, 21.12_

  - [ ] 10.3 Calcular a confiança do valuation em faixas contínuas
    - Implementar `valuation_confidence` com as faixas do requisito por `classify_by_band`, monotônica não decrescente na quantidade e na qualidade dos comparáveis, considerando também atualidade, semelhança e dispersão; amostra sem comparável aproveitável resulta em inconclusivo com pendência de mercado; registrar metodologia, amostra, ajustes e premissas
    - _Requisitos: 22.1, 22.2, 22.3, 22.4, 22.4.1, 22.5, 22.7, 22.8_

  - [ ] 10.4 Emitir as faixas de valor e os métodos por tipo de ativo
    - Criar `src/radar/engines/valuation.py` com `valuate` emitindo conservador, base, otimista e venda rápida, cada um com confiança e método registrado; base é a mediana da amostra ajustada, conservador é o base menos o desconto declarado e venda rápida é o conservador menos o desconto de aceleração; o conservador é a referência dos testes de robustez e o base é a referência da decisão principal, e o otimista nunca é referência única; aplicar os métodos por tipo de ativo, sem exigir yield de aluguel para terreno, e manter a classificação socioeconômica do público como informativa
    - A avaliação da fonte permanece em campo próprio e nunca alimenta o valor de mercado; quando supera o valor otimista da amostra, gera evidência de divergência e pendência
    - _Requisitos: 23.1, 23.2, 23.2.1, 23.3, 23.4, 23.5, 23.6, 23.7, 23.8, 24.1, 24.2, 24.3, 24.4, 24.5, 24.6, 24.7, 24.8_

  - [ ] 10.5 Emitir os gatilhos de revaluation
    - Emitir para o Monitor os gatilhos de reestimativa: novo comparável de classe A a C dentro do raio e da janela; frescor de valuation excedido; variação material do aluguel; informação física relevante alterada. Mudança de estratégia ativa recalcula o preço máximo sem necessariamente recalcular o valor de mercado
    - _Requisitos: 25.1, 25.2, 25.3, 25.4, 25.5_

  - [ ]* 10.6 Escrever testes dirigidos de comparáveis e valuation
    - Cobrir por exemplo os ramos de seleção de comparáveis e de método por tipo de ativo, que não têm propriedade universal associada
    - _Requisitos: 21.1, 24.2, 24.3, 24.4, 24.5_

- [ ] 11. Custo econômico total e métricas econômicas
  - [ ] 11.1 Reconstruir o custo econômico total com treze componentes
    - Reescrever `CostBreakdown` em `src/radar/engines/calculation.py` com exatamente treze componentes, cada um `Informed[Decimal]`: preço, comissão do leiloeiro, ITBI e tributos de aquisição, registro e documentação, débitos de condomínio, débitos de tributos, regularização, reforma, desocupação, reserva para imprevistos, custo jurídico esperado, carrying e custo financeiro
    - O total é a soma exata dos treze e o estado do total é o pior estado entre os componentes; cada componente permanece individualmente consultável; desconhecido nunca é zero
    - **Fora do total**: corretagem de venda e imposto sobre ganho de capital, que pertencem à perna de venda, e o custo de oportunidade do capital, já cobrado pelo retorno mínimo exigido
    - _Requisitos: 26.1, 26.1.1, 26.1.2, 26.2, 26.3, 26.4, 26.5, 26.6, 26.7, 26.8, 26.10, 26.11_

  - [ ]* 11.2 Escrever teste de propriedade para conservação de valor no total
    - **Property 43: Conservação de valor no TCO (`P6.1`)**
    - **Validates: Requirements 26.1, 26.11**

  - [ ]* 11.3 Escrever teste de propriedade para monotonicidade do total
    - **Property 44: Monotonicidade do TCO (`P6.2`)**
    - **Validates: Requirements 26.1**

  - [ ] 11.4 Separar as referências de desconto líquido e de margem
    - Implementar `net_discount` sobre o valor de mercado **base** e `safety_margin_pct` com a mesma fórmula, reservando o valor **conservador** para o teste de robustez; registrar o desconto da fonte e o desconto de mercado como informativos
    - _Requisitos: 27.1, 27.2, 27.3, 27.4, 27.5_

  - [ ]* 11.5 Escrever teste de propriedade para monotonicidade do desconto líquido
    - **Property 45: Monotonicidade do desconto líquido (`P6.3`)**
    - **Validates: Requirements 27.3**

  - [ ]* 11.6 Escrever teste de propriedade para monotonicidade da margem
    - **Property 46: Monotonicidade da margem (`P6.4`)**
    - **Validates: Requirements 27.4, 27.5**

  - [ ]* 11.7 Escrever teste de propriedade para a identidade desconto-margem
    - **Property 47: Identidade metamórfica desconto-margem (`P6.5`)**
    - **Validates: Requirements 27.3, 27.5**

  - [ ] 11.8 Calcular renda, base de imposto sobre aluguel e yields
    - Implementar `rent_net` com piso em zero, subtraindo condomínio e IPTU não recuperáveis, manutenção, seguro e taxas, vacância, inadimplência e imposto; `rent_tax_base` sem deduzir vacância nem inadimplência; `rent_income_tax` devolvendo desconhecido enquanto a alíquota estiver pendente de decisão; `net_yield_monthly` devolvendo `ProvisionalMetric` com o motivo da provisoriedade, porque o piso decisório de renda incide sobre o líquido
    - _Requisitos: 27.6, 27.7, 27.7.1, 27.7.2, 27.8_

  - [ ]* 11.9 Escrever teste de propriedade para consistência entre yields
    - **Property 48: Consistência entre yields mensal e anual (`P6.6`)**
    - **Validates: Requirements 27.6, 27.8**

  - [ ]* 11.10 Escrever teste de propriedade para yield líquido e bruto
    - **Property 49: Yield líquido nunca excede o bruto (`P6.7`)**
    - **Validates: Requirements 27.7, 27.8**

  - [ ]* 11.11 Escrever teste de propriedade para monotonicidade do yield
    - **Property 50: Monotonicidade do yield (`P6.8`)**
    - **Validates: Requirements 27.6, 27.8**

  - [ ] 11.12 Calcular a perna de venda e o retorno
    - Implementar venda líquida, base de imposto sobre ganho de capital com piso em zero, lucro líquido, ROI líquido e margem líquida, com a corretagem e o imposto aparecendo apenas aqui e nunca no custo econômico total
    - _Requisitos: 27.9, 27.10, 27.11, 27.12, 27.13_

  - [ ]* 11.13 Escrever teste de propriedade para a base de imposto
    - **Property 51: Base de IR nunca é negativa (`P6.9`)**
    - **Validates: Requirements 27.10**

  - [ ] 11.14 Calcular o ponto de equilíbrio de saída
    - Implementar `break_even_exit` como o preço de venda que zera o lucro líquido, com ganho nulo implicando base de imposto zero
    - _Requisitos: 27.14, 27.15_

  - [ ]* 11.15 Escrever teste de propriedade para o ponto de equilíbrio
    - **Property 54: Break-even zera o lucro líquido (`P6.12`)**
    - **Validates: Requirements 27.14**

  - [ ] 11.16 Declarar as pré-condições e o determinismo dos cálculos
    - Rejeitar valor de mercado menor ou igual a zero com erro de dado de entrada em todas as métricas dependentes, e garantir que todo cálculo deste motor é função pura sem dependência de modelo de linguagem
    - _Requisitos: 27.16, 27.17_

  - [ ]* 11.17 Escrever teste de propriedade para valor de mercado não positivo
    - **Property 52: Valor de mercado não positivo sinaliza erro (`P6.10`)**
    - **Validates: Requirements 27.16**

  - [ ]* 11.18 Escrever teste de propriedade para determinismo das métricas
    - **Property 53: Determinismo das métricas econômicas (`P6.11`)**
    - **Validates: Requirements 27.17**

  - [ ] 11.19 Modelar carrying, capital imobilizado e custo do tempo
    - Implementar `CarryingModel` com as seis parcelas mensais e os dois totalizadores: o decisório com cinco parcelas, que entra no custo econômico total, e o pleno com seis, usado apenas no custo do tempo e na eficiência de capital; implementar `capital_metrics` com capital inicial, capital total, prazo de imobilização, capital exposto, margem por mês e retorno por capital; prazo acima do limite classifica como não aderente e alerta; aumento de prazo recalcula carregamento e margem exigida; valor presente líquido e taxa interna de retorno são complementares e não substituem risco, liquidez e confiança
    - _Requisitos: 30.1, 30.2, 30.3, 30.4, 30.5, 30.6, 30.7, 30.8, 30.9_

  - [ ] 11.20 Modelar reforma, contingências e regularização
    - Implementar `RenovationLevel` de 0 a 4, `RangeEstimate` com mínimo, base e máximo, e `renovation_cost` aplicando de forma cumulativa a contingência por nível, o acréscimo por ausência de vistoria e o acréscimo por imóvel ocupado; separar reforma necessária de desejável, incluindo apenas a necessária no cenário base, e na estratégia de renda considerar como necessário o mínimo para locação; manter regularização como componente distinto; suspeita estrutural sem confirmação abre pendência crítica e impede `BUY`, e condição estrutural desconhecida exige pendência de prioridade alta **mais** contingência
    - _Requisitos: 29.1, 29.2, 29.3, 29.4, 29.5, 29.6, 29.7, 29.8, 29.9, 29.10, 29.11_

- [ ] 12. Preço máximo, teto decisório e demais tetos por estratégia
  - [ ] 12.1 Implementar a forma fechada do preço máximo com ITBI
    - Implementar `MaxPriceInputs` e `max_price_by_target_roi` conforme a derivação do design, com o ITBI no coeficiente proporcional, e a pré-condição algébrica que levanta erro em lugar de devolver valor
    - Este é o defeito central: o teto anterior, usado como preço, não reproduzia o ROI alvo, e a versão anterior omitia o ITBI apesar de ele ser proporcional ao preço
    - _Requisitos: 28.1, 28.2, 28.2.1_

  - [ ]* 12.2 Escrever teste de propriedade para a inversa do preço máximo
    - **Property 55: Propriedade inversa do preço máximo (`P7.1`)**
    - **Validates: Requirements 28.2, 28.3**

  - [ ]* 12.3 Escrever teste de propriedade para monotonicidade no ROI alvo
    - **Property 56: Monotonicidade decrescente no ROI alvo (`P7.2`)**
    - **Validates: Requirements 28.2**

  - [ ]* 12.4 Escrever teste de propriedade para monotonicidade nos custos fixos
    - **Property 57: Monotonicidade decrescente nos custos fixos (`P7.3`)**
    - **Validates: Requirements 28.2**

  - [ ]* 12.5 Escrever teste de propriedade para monotonicidade no valor de saída
    - **Property 58: Monotonicidade crescente no valor de saída (`P7.4`)**
    - **Validates: Requirements 28.2**

  - [ ]* 12.6 Escrever teste de propriedade para não negatividade do teto
    - **Property 59: Preço máximo nunca é negativo (`P7.5`)**
    - **Validates: Requirements 28.2**

  - [ ]* 12.7 Escrever teste de propriedade para monotonicidade no ITBI
    - **Property 65: Monotonicidade decrescente no ITBI (`P7.11`)**
    - **Validates: Requirements 28.2, 28.2.1**

  - [ ] 12.8 Implementar a variante com reserva proporcional
    - Implementar `max_price_with_proportional_reserve`, em que a reserva incide sobre o custo de aquisição e altera o coeficiente proporcional e os custos fixos, coexistindo com a variante de reserva fixa orçada
    - _Requisitos: 28.2.2_

  - [ ] 12.9 Implementar o teto conservador informativo e o teto decisório
    - Implementar `max_price_jabes_conservative` rotulado como referência informativa, nunca como preço máximo por ROI alvo, e `decision_ceiling` como o mínimo entre o teto exato e o ajustado ao risco, único valor que a disciplina de lance consome
    - _Requisitos: 28.4, 28.4.1, 28.4.2_

  - [ ]* 12.10 Escrever teste de propriedade para o teto decisório
    - **Property 64: Teto decisório é o mínimo dos dois (`P7.10`)**
    - **Validates: Requirements 28.4.2**

  - [ ] 12.11 Implementar os tetos das demais estratégias
    - Implementar o teto por yield líquido mínimo, o teto por valor futuro projetado, o teto por capacidade do público-alvo e o teto por potencial de uso de terreno, e garantir que o mesmo imóvel tenha tetos distintos por estratégia
    - _Requisitos: 28.5, 28.6, 28.7, 28.8, 28.15_

  - [ ] 12.12 Ajustar o teto ao risco e à liquidez
    - Implementar `risk_adjusted_max_price` subtraindo custo de risco esperado, contingência e margem adicional, com a margem adicional por prazo aplicada quando a liquidez fica abaixo do mínimo da estratégia; liquidez indefinida não produz teto definitivo; componente de custo desconhecido de impacto alto ou crítico marca o teto como provisório com a pendência determinante nomeada
    - _Requisitos: 26.12, 28.9, 28.10, 28.11_

  - [ ]* 12.13 Escrever teste de propriedade para o teto ajustado ao risco
    - **Property 60: Ajustado ao risco nunca excede o econômico (`P7.6`)**
    - **Validates: Requirements 28.9**

  - [ ]* 12.14 Escrever teste de propriedade para liquidez indefinida
    - **Property 63: Liquidez indefinida impede teto definitivo (`P7.9`)**
    - **Validates: Requirements 28.11**

  - [ ] 12.15 Implementar o preço-alvo e a apresentação como limite
    - Implementar `target_price` com folga sobre o teto, nunca excedendo-o, e apresentar o preço máximo como limite, jamais como preço recomendado de compra
    - _Requisitos: 28.12, 28.16_

  - [ ]* 12.16 Escrever teste de propriedade para o preço-alvo
    - **Property 62: Preço-alvo nunca excede o preço máximo (`P7.8`)**
    - **Validates: Requirements 28.12**

  - [ ] 12.17 Aplicar o teto contra a oferta
    - Comparar o preço de oferta com o teto ajustado e emitir reprovação econômica para a estratégia quando excedido, registrando o teto aplicado
    - _Requisitos: 28.13, 28.14, 33.2_

  - [ ]* 12.18 Escrever teste de propriedade para oferta acima do teto
    - **Property 61: Oferta acima do teto implica DO_NOT_BUY (`P7.7`)**
    - **Validates: Requirements 28.13, 33.2**

- [ ] 13. Cenários, robustez e regras de decisão econômica
  - [ ] 13.1 Construir os quatro cenários e a grade de sensibilidade
    - Criar `src/radar/engines/scenarios.py` com `build_scenarios` produzindo otimista, base, conservador e estressado, cada um com TCO, margem, ROI líquido e prazo próprios, e a grade de sensibilidade de preço de saída, reforma, prazo, aluguel, vacância e custos; a construção é monotônica por projeto
    - _Requisitos: 32.1, 32.2, 32.3, 32.4, 32.5_

  - [ ]* 13.2 Escrever teste de propriedade para ordenação de cenários
    - **Property 66: Ordenação de cenários (`P8.1`)**
    - **Validates: Requirements 32.1, 32.2, 32.3, 32.4**

  - [ ] 13.3 Classificar a robustez em seis níveis
    - Implementar `Robustness` com seis níveis e a classificação como sub-verificação da camada de economia: tese que não sobrevive ao conservador produz no máximo condição objetiva; tese inviável no base é reprovada; conservador dependente de dado desconhecido produz monitoramento ou condição com a pendência determinante nomeada
    - _Requisitos: 32.6, 32.7, 32.8, 32.9, 32.10_

  - [ ]* 13.4 Escrever teste de propriedade para sobrevivência ao estressado
    - **Property 67: Sobreviver ao estressado implica sobreviver a todos (`P8.2`)**
    - **Validates: Requirements 32.6**

  - [ ]* 13.5 Escrever teste de propriedade para classificação de robustez
    - **Property 68: Classificação de robustez é total e consistente (`P8.3`)**
    - **Validates: Requirements 32.6**

  - [ ] 13.6 Calcular os cinco limites do ponto de equilíbrio
    - Implementar `break_even_limits`: preço de venda mínimo que cobre todos os custos; preço de compra máximo que mantém a margem exigida; aumento máximo suportado de reforma; queda máxima suportada de aluguel; aumento máximo suportado de prazo
    - _Requisitos: 32.11_

  - [ ] 13.7 Avaliar as regras de decisão econômica
    - Implementar `evaluate_economic_rules` registrando, para cada veredito, a métrica avaliada, o valor apurado, o limite aplicado e o parâmetro de origem do limite; custo acima do valor conservador reprova ou bloqueia conforme a severidade do risco associado; desconto líquido abaixo do mínimo da estratégia reprova pela camada de economia; margem abaixo do mínimo reprova ou condiciona conforme exista condição objetiva de melhoria; a distância do ponto de equilíbrio é medida contra o **preço atual** e comparada com o limiar declarado; o retorno comparado com o hurdle é o **anualizado**; conservador robusto eleva o componente de qualidade da oportunidade no score
    - _Requisitos: 33.1, 33.3, 33.4, 33.5, 33.6, 33.7, 33.7.1, 33.8, 33.9, 33.10_

- [ ] 14. Motor de Risco e Motor de Liquidez
  - [ ] 14.1 Declarar a matriz de severidade e o registro de risco
    - Criar `src/radar/engines/risk.py` com `RiskRecord` (categoria, probabilidade, impacto, exposição de capital, incerteza, mitigabilidade, prazo potencial, estado de evidência, severidade, mitigação), as dez categorias, e `SEVERITY_MATRIX` declarada como dado com as doze células do produto de três probabilidades por quatro impactos; severidade e confiança são dimensões independentes; as seis estratégias de mitigação são fechadas e `aceitar` exige exceção registrada com justificativa, evidência, limite e prazo
    - _Requisitos: 34.1, 34.2, 34.3, 34.4, 34.8, 34.10, 34.11_

  - [ ]* 14.2 Escrever teste de propriedade para totalidade da severidade
    - **Property 69: Severidade é total sobre probabilidade e impacto (`P8.4`)**
    - **Validates: Requirements 34.3, 34.4**

  - [ ]* 14.3 Escrever teste de propriedade para monotonicidade da severidade
    - **Property 70: Monotonicidade da severidade (`P8.5`)**
    - **Validates: Requirements 34.4**

  - [ ] 14.4 Implementar o bloqueio por risco crítico
    - Implementar `critical_block` produzindo bloqueio para severidade crítica **independentemente do estado da evidência**, e rotulando o registro como bloqueio por risco crítico presumido, com a condição objetiva de desbloqueio, quando a severidade decorre de evidência estimada ou inferida; alimentar a camada 0 do motor de decisão, hoje literalmente falsa no grafo; registrar risco jurídico de severidade crítica quando o gate jurídico bloqueia
    - _Requisitos: 12.3, 12.4, 34.5, 34.5.1, 34.5.2_

  - [ ]* 14.5 Escrever teste de propriedade para bloqueio por risco crítico
    - **Property 71: Risco crítico sempre bloqueia (`P8.6`)**
    - **Validates: Requirements 34.5, 34.5.2, 12.3**

  - [ ]* 14.6 Escrever teste de propriedade para bloqueio presumido
    - **Property 73: Bloqueio presumido traz condição de desbloqueio (`P8.8`)**
    - **Validates: Requirements 34.5.1**

  - [ ] 14.7 Tratar categoria não investigada como desconhecida
    - Implementar `uninvestigated` de modo que categoria não investigada seja risco de estado desconhecido, nunca baixo, e garantir que não exista construtor capaz de produzir severidade baixa sem probabilidade e impacto informados; registrar a exposição de capital e o prazo potencial por categoria
    - _Requisitos: 34.6, 34.7, 34.9_

  - [ ]* 14.8 Escrever teste de propriedade para categoria não investigada
    - **Property 72: Categoria não investigada resulta em UNKNOWN (`P8.7`)**
    - **Validates: Requirements 34.9**

  - [ ] 14.9 Separar risco de incerteza
    - Implementar `required_margin` crescente com risco e incerteza, com risco crítico não admitindo margem compensatória, e `uncertainty_effect` traduzindo o impacto do desconhecido em restrição de decisão: impacto baixo permite decidir com pendência baixa; impacto alto condiciona ou monitora; impacto crítico impede `BUY`; risco conhecido e quantificável entra no custo como custo esperado; conhecido e não quantificável eleva a margem exigida e condiciona a decisão
    - _Requisitos: 35.1, 35.2, 35.3, 35.4, 35.5, 35.6_

  - [ ] 14.10 Calcular os escores de liquidez de venda e de locação
    - Criar `src/radar/engines/liquidity.py` com `liquidity_scores` produzindo dois escores independentes de 0 a 100 a partir dos sete pesos que somam 1,00, `LIQUIDITY_BANDS` com as **sete** faixas contínuas e sem lacuna sobre todo o domínio, e os sete públicos-alvo; avaliar o imóvel dentro do seu submercado de ticket, sem generalizar a liquidez do bairro; registrar quantidade e características da oferta concorrente; dados insuficientes produzem liquidez indefinida com confiança reduzida e pendência, nunca um número de conveniência
    - _Requisitos: 40.1, 40.2, 40.3, 40.6, 40.9, 40.10, 40.11_

  - [ ]* 14.11 Escrever teste de propriedade para as sete faixas de liquidez
    - **Property 74: Sete faixas de liquidez contínuas e sem lacuna (`P9.1`)**
    - **Validates: Requirements 40.2**

  - [ ]* 14.12 Escrever teste de propriedade para a escala do score de liquidez
    - **Property 75: Score de liquidez permanece na escala (`P9.2`)**
    - **Validates: Requirements 40.1, 40.3**

  - [ ]* 14.13 Escrever teste de propriedade para monotonicidade da liquidez
    - **Property 76: Monotonicidade do score de liquidez (`P9.3`)**
    - **Validates: Requirements 40.3**

  - [ ] 14.14 Implementar os dois limiares distintos de liquidez
    - Implementar `liquidity_decision` com o limiar da estratégia, que é preferência calibrável, e o piso do produto, que exige exceção formal para qualquer decisão de compra; os dois coexistem e são registrados separadamente
    - _Requisitos: 40.7, 40.8_

  - [ ]* 14.15 Escrever teste de propriedade para liquidez abaixo do mínimo
    - **Property 77: Liquidez abaixo do mínimo nunca resulta em BUY (`P9.4`)**
    - **Validates: Requirements 40.7**

  - [ ] 14.16 Tornar cumulativas as compensações de prazo e de iliquidez
    - Implementar `additional_margin_by_term` por faixa contínua de prazo e `required_margin_with_liquidity` somando a compensação de iliquidez à compensação de prazo, porque as duas cobrem coisas distintas
    - _Requisitos: 30.7, 41.4, 45.10, 45.10.1_

  - [ ]* 14.17 Escrever teste de propriedade para margem adicional por prazo
    - **Property 78: Margem adicional monotônica no prazo (`P9.5`)**
    - **Validates: Requirements 41.4, 30.7**

  - [ ] 14.18 Estimar preços e prazos de saída
    - Implementar `exit_prices` com otimista, base, conservador e venda rápida derivados dos comparáveis e do público-alvo, nunca igualados automaticamente ao valor de mercado estimado; classificar o impacto do prazo estimado; prazo acima do limite condiciona ou reprova; preço conservador que não cobre o capital total empregado reprova; venda rápida recalcula margem e ROI; registrar o desconto necessário para acelerar a saída e compará-lo com o limite declarado
    - _Requisitos: 41.1, 41.2, 41.3, 41.5, 41.6, 41.7, 41.8_

- [ ] 15. Estratégia, portfólio, score, confiança e ranking
  - [ ] 15.1 Separar estratégia de perfil de ativo
    - Criar `src/radar/engines/strategy.py` com `Strategy` de **seis** valores, incluindo `customizada`, e `AssetProfile` de **nove** valores, incluindo `desconhecido`, que não herda critérios de nenhum perfil e registra pendência de classificação com redução de confiança; declarar `StrategyThresholds` a partir da tabela de thresholds por estratégia e `STRATEGY_OWN_PARAMETERS` com os parâmetros próprios de cada estratégia; implementar `resolve_ticket_max`, em que o ticket da estratégia prevalece sobre o ticket do perfil do investidor quando declarado
    - _Requisitos: 44.1, 44.1.1, 44.2, 44.2.1, 44.9, 45.12, 45.13, 45.14, 45.15, 45.16_

  - [ ] 15.2 Avaliar todas as estratégias ativas
    - Implementar `evaluate_strategies` emitindo um resultado por estratégia ativa, com aderência de 0 a 100 classificada por faixa contínua nas seis faixas e reprovação da estratégia abaixo do piso; a mesma oportunidade pode resultar em decisões diferentes por estratégia, e aderência a mais de uma é fator informativo de priorização; registrar critérios atendidos, critérios não atendidos e parâmetros aplicados; nenhum tipo de imóvel nem segmento socioeconômico é excluído automaticamente; imóvel atípico eleva o requisito mínimo de classe de comparável e registra a atipicidade como fator de liquidez
    - _Requisitos: 44.3, 44.4, 44.5, 44.6, 44.7, 44.8, 44.10, 45.1, 45.2, 45.3, 45.4, 45.5, 45.6, 45.7, 45.8, 45.9, 45.11, 45.17, 45.18_

  - [ ] 15.3 Implementar capital, reserva e limite por operação
    - Criar `src/radar/engines/portfolio.py` com `CapitalView` de sete grandezas distintas; `applicable_reserve` como o **maior** valor entre a reserva absoluta e a reserva percentual do patrimônio líquido, com capital livre abaixo dela produzindo bloqueio operacional por reserva; `operation_limit` avaliado contra o **custo econômico total**, aplicando o mais restritivo entre ticket, percentual do capital por operação e percentual do patrimônio por operação, com bloqueio operacional por capital quando excedido salvo exceção formal registrada; considerar as reservas específicas de custos inesperados, reforma, vacância, carregamento e contingências jurídicas
    - _Requisitos: 46.1, 46.2, 46.3, 46.4, 46.5, 46.5.1, 46.6, 46.6.1, 46.7, 46.9_

  - [ ] 15.4 Calcular as cinco métricas de eficiência de capital
    - Implementar `capital_efficiency` com eficiência de capital, eficiência temporal, renda por capital, margem por capital e renda líquida por risco, apresentadas por operação
    - _Requisitos: 46.8_

  - [ ] 15.5 Calcular concentração e diversificação por um único caminho
    - Implementar `concentration` com os limites por localização, tipo, estratégia, faixa de ticket, fonte e nível de risco, mantendo a alocação-alvo por estratégia, calculando o desvio da carteira e comparando-o com o limite de desvio; concentração excedida reduz a prioridade e penaliza o componente de diversificação do Investor Fit, e melhora da diversificação eleva o mesmo componente; concentração e diversificação entram no resultado **apenas** por esse componente, e o ajuste de portfólio do score composto cobre somente o bônus de equilíbrio e a penalização por capital imobilizado
    - _Requisitos: 47.1, 47.1.1, 47.2, 47.3, 47.4, 47.4.1, 47.5, 47.6_

  - [ ] 15.6 Implementar o Opportunity Score e os conjuntos de pesos
    - Criar `src/radar/engines/scoring.py` e `src/radar/engines/bands.py` com os pesos mestres somando 1,00, as **cinco** colunas de pesos por estratégia, cada uma somando 1,00 e com o componente de qualidade da oportunidade em peso estritamente positivo, e o score econômico auxiliar de sete componentes em base 100 sem efeito decisório; calcular o Opportunity Score apenas após a aprovação das camadas eliminatórias, rejeitar na carga da configuração qualquer conjunto cuja soma difira de 1,00, registrar a contribuição individual de cada fator e a versão dos pesos aplicada, e abster-se de emitir score quando faltam os dados mínimos, registrando score indefinido em lugar de zero
    - Classificar o score nas faixas nomeadas por `classify_by_band`
    - _Requisitos: 49.1, 49.2, 49.3, 49.4, 49.5, 49.6, 49.7, 49.8, 49.9_

  - [ ]* 15.7 Escrever teste de propriedade para a soma dos pesos
    - **Property 79: Todo conjunto de pesos soma 1,00 (`P10.1`)**
    - **Validates: Requirements 49.5**

  - [ ]* 15.8 Escrever teste de propriedade para a escala do Opportunity Score
    - **Property 80: Opportunity Score permanece na escala (`P10.2`)**
    - **Validates: Requirements 49.1, 49.2**

  - [ ]* 15.9 Escrever teste de propriedade para monotonicidade do Opportunity Score
    - **Property 81: Monotonicidade do Opportunity Score (`P10.3`)**
    - **Validates: Requirements 49.2**

  - [ ]* 15.10 Escrever teste de propriedade para a soma das contribuições
    - **Property 82: Contribuições somam o score (`P10.4`)**
    - **Validates: Requirements 49.7**

  - [ ]* 15.11 Escrever teste de propriedade para as faixas de score
    - **Property 92: Cobertura total das faixas de score (`P10.14`)**
    - **Validates: Requirements 49.6**

  - [ ]* 15.12 Escrever teste de propriedade para as colunas por estratégia
    - **Property 96: Colunas por estratégia somam 1,00 com qualidade positiva (`P10.18`)**
    - **Validates: Requirements 49.5, 49.2**

  - [ ] 15.13 Consolidar a confiança fora do grafo
    - Implementar `consolidated_confidence` a partir das cinco dimensões declaradas, determinística, versionada e reproduzível, com o fator de confiança em faixas contínuas e monotônicas e o nível nomeado saindo dos seis rótulos fechados; dimensão obrigatória desconhecida ou conflitante produz estado inconclusivo, que não é faixa numérica; a confiança é dimensão independente do score e do risco e nunca contorna camada de bloqueio
    - Remover do grafo de orquestração a heurística de confiança não versionada
    - _Requisitos: 50.1, 50.2, 50.3, 50.4, 50.5, 50.5.1, 50.7_

  - [ ]* 15.14 Escrever teste de propriedade para o fator de confiança
    - **Property 93: Cobertura total do fator de confiança (`P10.15`)**
    - **Validates: Requirements 50.3, 50.4**

  - [ ] 15.15 Implementar o Investor Fit com sete componentes
    - Implementar o Investor Fit com exatamente sete componentes e os pesos 0,27 de aderência à estratégia, 0,20 de aderência ao risco, 0,13 de liquidez versus necessidade, 0,13 de aderência ao capital, 0,13 de diversificação, 0,07 de esforço operacional e 0,07 de horizonte, somando 1,00 e **sem nenhum componente de qualidade econômica**; manter o Fit separado do Opportunity Score, permitir valores distintos por investidor e por estratégia, e garantir que o Fit nunca converte bloqueio em compra
    - _Requisitos: 51.1, 51.1.1, 51.2, 51.3, 51.4, 51.5, 51.6_

  - [ ]* 15.16 Escrever teste de propriedade para a escala do Investor Fit
    - **Property 83: Investor Fit permanece na escala (`P10.5`)**
    - **Validates: Requirements 51.1**

  - [ ]* 15.17 Escrever teste de propriedade para o Fit diante de bloqueio
    - **Property 84: Investor Fit nunca converte BLOCK em BUY (`P10.6`)**
    - **Validates: Requirements 51.4, 12.3**

  - [ ]* 15.18 Escrever teste de propriedade para os sete pesos do Fit
    - **Property 95: Sete pesos do Fit, sem qualidade econômica (`P10.17`)**
    - **Validates: Requirements 51.1, 51.1.1**

  - [ ] 15.19 Implementar o score de prioridade com cinco fatores
    - Implementar `priority_score` como produto de exatamente cinco fatores — Opportunity Score, fator de confiança, fator de Investor Fit, ajuste de capital e ajuste de portfólio — com cada fator multiplicativo normalizado em `[0, 1]`, e o ajuste de portfólio composto apenas do bônus de equilíbrio e da penalidade por capital imobilizado
    - _Requisitos: 52.1, 52.1.1, 52.2_

  - [ ]* 15.20 Escrever teste de propriedade para monotonicidade do score de prioridade
    - **Property 85: Monotonicidade do score de prioridade (`P10.7`)**
    - **Validates: Requirements 52.1, 52.2**

  - [ ]* 15.21 Escrever teste de propriedade para o caminho único da concentração
    - **Property 97: Concentração entra por um único caminho (`P10.19`)**
    - **Validates: Requirements 52.1, 52.1.1, 47.4.1**

  - [ ] 15.22 Implementar o ranking, o desempate e as escalas
    - Criar `src/radar/engines/ranking.py` com `rank` excluindo do ranking operacional toda oportunidade bloqueada, produzindo ordem total, antissimétrica, transitiva, confluente e idempotente, com desempate determinístico pelos oito critérios na ordem canônica ou pela ordem própria da estratégia quando declarada, registrando qual foi aplicada; suportar ordenação absoluta, relativa, por estratégia, por portfólio e por janela temporal; classificar a urgência em `P0` a `P4` mais bloqueado, com os três disparadores de `P0`, e a atratividade combinada em `A1` a `A5`, mantendo as duas escalas nominalmente disjuntas; aplicar as faixas de ação por posição; registrar versão dos pesos e das regras com data e hora e preservar o histórico de posições
    - _Requisitos: 52.3, 52.4, 52.4.1, 52.5, 52.6, 52.6.1, 52.6.2, 52.11, 52.12_

  - [ ]* 15.23 Escrever teste de propriedade para ordem total do ranking
    - **Property 86: Ranking é ordem total (`P10.8`)**
    - **Validates: Requirements 52.4**

  - [ ]* 15.24 Escrever teste de propriedade para confluência do ranking
    - **Property 87: Confluência do ranking (`P10.9`)**
    - **Validates: Requirements 52.4**

  - [ ]* 15.25 Escrever teste de propriedade para consistência com o score
    - **Property 88: Consistência do ranking com o score (`P10.10`)**
    - **Validates: Requirements 52.4**

  - [ ]* 15.26 Escrever teste de propriedade para determinismo do desempate
    - **Property 89: Determinismo do desempate (`P10.11`)**
    - **Validates: Requirements 52.4**

  - [ ]* 15.27 Escrever teste de propriedade para exclusão de bloqueados
    - **Property 90: Bloqueados não aparecem no ranking (`P10.12`)**
    - **Validates: Requirements 52.3**

  - [ ]* 15.28 Escrever teste de propriedade para idempotência do ranking
    - **Property 91: Idempotência do ranking (`P10.13`)**
    - **Validates: Requirements 52.4**

  - [ ]* 15.29 Escrever teste de propriedade para disjunção das escalas
    - **Property 98: Escalas de urgência e atratividade são disjuntas (`P10.20`)**
    - **Validates: Requirements 52.6, 52.6.1**

  - [ ] 15.30 Explicar a posição no ranking
    - Implementar `explain_position` com as seis respostas obrigatórias — razão da posição, razão de não estar em primeiro, o que a faria subir, o que a faria cair, risco principal e pendência principal — além da identificação das oportunidades que competem pelo mesmo capital e do destaque do conjunto não dominado em retorno, risco, liquidez e capital
    - _Requisitos: 52.7, 52.8, 52.9, 52.10_

- [ ] 16. Motor de Decisão, catálogo de regras e explicabilidade
  - [ ] 16.1 Redefinir a entrada da decisão sem nenhum default
    - Reescrever `DecisionInput` em `src/radar/engines/decision.py` com todos os campos obrigatórios: bloqueios críticos, status jurídico, identidade, elegibilidade, confiança consolidada, confiança do valuation, pendências, métricas econômicas, robustez, avaliação de estratégia, riscos, liquidez, score, Investor Fit, veredito de capital, posição no ranking e exceções
    - Omitir o resultado do gate jurídico passa a ser erro de tipo; a fronteira da interface assume pendente e elegibilidade falsa, nunca liberado
    - Declarar `DecisionLayer` com os **onze** valores de 0 a 10
    - _Requisitos: 53.1, 53.1.1, 53.6_

  - [ ] 16.2 Dar conteúdo às onze camadas
    - Declarar cada camada como dado, com a verificação que executa e a saída em falha: camada 0 bloqueios críticos, incluindo risco crítico, ocupação de impacto crítico sem estratégia de desocupação, posse litigiosa com evidência de litígio, regra eliminatória expressa do investidor e comprometimento da reserva mínima aplicável; camada 1 validade jurídica com as 19 verificações; camada 2 elegibilidade com identidade mínima, localização, tipo e ticket; camada 3 dados e confiança com os limiares de confiança consolidada e de valuation e as pendências abertas; camada 4 economia com desconto líquido, margem, preço máximo, retorno anualizado contra o hurdle e a sub-verificação de robustez do conservador; camada 5 estratégia com aderência, yield líquido mínimo, prazo e critérios próprios; camada 6 risco com severidades alto e medio e as regras de ocupação e de localização; camada 7 liquidez com o limiar da estratégia, o piso do produto e as compensações; camada 8 score com o piso de score e a matriz; camada 9 capital e concentração com Investor Fit mínimo e os limites de capital e de concentração; camada 10 ranking com posição e faixas de ação
    - _Requisitos: 53.1.2, 53.1.3, 53.1.4, 53.1.5, 53.1.6, 53.1.7, 53.1.8, 53.1.9, 53.1.10, 53.1.11, 53.1.12_

  - [ ] 16.3 Avaliar as camadas com curto-circuito e camada determinante correta
    - Implementar `decide` avaliando as camadas em ordem e parando na primeira eliminatória, sem que nenhuma camada posterior altere o resultado de uma anterior; quando várias camadas eliminariam, a determinante reportada é a de **menor índice**, e o rótulo corresponde à verificação efetivamente executada; emitir exatamente um dos cinco estados finais, com a decisão sendo a saída e nunca uma camada; distinguir reprovação econômica de impedimento
    - _Requisitos: 53.2, 53.3, 53.4, 53.5, 53.7, 53.8, 53.9, 53.10, 53.11_

  - [ ]* 16.4 Escrever teste de propriedade para totalidade da decisão
    - **Property 99: Totalidade da decisão (`P11.1`)**
    - **Validates: Requirements 53.5**

  - [ ]* 16.5 Escrever teste de propriedade para incompensabilidade do bloqueio
    - **Property 100: BLOCK não é compensável (`P11.2`)**
    - **Validates: Requirements 12.3, 53.4**

  - [ ]* 16.6 Escrever teste de propriedade para a camada determinante
    - **Property 101: Camada determinante é a de menor índice (`P11.3`)**
    - **Validates: Requirements 53.1, 53.2, 53.3**

  - [ ]* 16.7 Escrever teste de propriedade para precedência entre camadas
    - **Property 102: Camada posterior não anula camada anterior (`P11.4`)**
    - **Validates: Requirements 53.4**

  - [ ]* 16.8 Escrever teste de propriedade para determinismo da decisão
    - **Property 110: Determinismo da decisão e da camada (`P11.12`)**
    - **Validates: Requirements 53.1**

  - [ ]* 16.9 Escrever teste de propriedade para as onze camadas
    - **Property 114: Onze camadas e a decisão não é camada (`P11.16`)**
    - **Validates: Requirements 53.1, 53.1.1**

  - [ ] 16.10 Declarar a matriz de ação de quinze células
    - Declarar `ACTION_MATRIX` com as **cinco** faixas de score por **três** faixas de confiança, totalizando quinze células, com os dois eixos classificados por faixa contínua; bloqueio em qualquer camada produz bloqueio independentemente de score e confiança; confiança inconclusiva produz pendente ou bloqueio conforme a criticidade da dimensão; a matriz é o limite superior da decisão na camada 8, e as camadas anteriores podem sempre ser mais restritivas
    - _Requisitos: 55.1, 55.8, 55.9, 55.10, 55.11, 55.12, 55.13, 55.14, 55.15, 55.16_

  - [ ]* 16.11 Escrever teste de propriedade para a totalidade da matriz
    - **Property 113: Totalidade da matriz de score × confiança (`P11.15`)**
    - **Validates: Requirements 55.1, 55.10, 55.11, 55.12, 55.13, 55.14, 55.15, 55.16**

  - [ ]* 16.12 Escrever teste de propriedade para monotonicidade na confiança
    - **Property 108: Monotonicidade da decisão na confiança (`P11.10`)**
    - **Validates: Requirements 55.1, 55.2, 55.3, 55.4, 55.5, 55.6, 55.7, 55.8, 55.9**

  - [ ] 16.13 Aplicar as restrições de status jurídico, confiança e pendências
    - Implementar as restrições da camada 1 e da camada 3: status pendente impede `BUY` e permite no máximo condição ou monitoramento; risco jurídico emite condição, monitoramento ou bloqueio conforme o impacto e a possibilidade de saneamento; confiança abaixo do mínimo impede `BUY`; pendência crítica aberta restringe a decisão a pendente, monitoramento ou bloqueio; pendência alta impede `BUY` e permite condição; pendência média reduz a confiança consolidada; pendência baixa permite decidir com a pendência na explicação
    - _Requisitos: 12.7, 12.8, 37.3, 37.4, 37.5, 37.6, 50.6_

  - [ ]* 16.14 Escrever teste de propriedade para status pendente
    - **Property 103: PENDENTE nunca resulta em BUY (`P11.5`)**
    - **Validates: Requirements 12.8**

  - [ ]* 16.15 Escrever teste de propriedade para confiança insuficiente
    - **Property 104: Confiança insuficiente nunca resulta em BUY (`P11.6`)**
    - **Validates: Requirements 50.6**

  - [ ]* 16.16 Escrever teste de propriedade para pendência crítica
    - **Property 105: Pendência crítica restringe a decisão (`P11.7`)**
    - **Validates: Requirements 37.3**

  - [ ]* 16.17 Escrever teste de propriedade para monotonicidade no desconto líquido
    - **Property 109: Monotonicidade da decisão no desconto líquido (`P11.11`)**
    - **Validates: Requirements 33.3**

  - [ ] 16.18 Declarar o catálogo das cinquenta e cinco regras
    - Criar `src/radar/rules/catalog.py` com `RULE_CATALOG` contendo as **55** regras canônicas: `RULE-ID-001` a `RULE-ID-002`, `RULE-JUR-001` a `RULE-JUR-013`, `RULE-OCC-001` a `RULE-OCC-002`, `RULE-LOC-001` a `RULE-LOC-003`, `RULE-ED-001` a `RULE-ED-004`, `RULE-MKT-001` a `RULE-MKT-004`, `RULE-FIN-001` a `RULE-FIN-006`, `RULE-LIQ-001` a `RULE-LIQ-003`, `RULE-STR-001` a `RULE-STR-002`, `RULE-SCR-001` a `RULE-SCR-002`, `RULE-DEC-001` a `RULE-DEC-002`, `RULE-GOV-001`, `RULE-MON-001` e `RULE-RSK-001` a `RULE-RSK-010`
    - Cada especificação traz domínio, condição ou gatilho, evidência mínima, resultado, prioridade, tipo entre os seis e se afeta o score; ligar `RULE-RSK-005` e `RULE-RSK-009` à camada 0 com resultado de bloqueio, e `RULE-RSK-008` à exigência de pendência mais contingência; declarar a precedência de conflitos nos seis níveis, com score e ranking abaixo de todos
    - _Requisitos: 54.1, 54.2, 54.3, 54.4, 54.5, 54.6, 54.7, 54.8, 54.9, 54.11_

  - [ ] 16.19 Resolver conflito pelo escopo mais específico
    - Implementar `resolve_scope_conflict` em que o escopo **mais específico prevalece**, exceto quando o menos específico impõe bloqueio crítico ou restrição legal ou documental, para todo par da hierarquia global, investidor, estratégia, localização, tipo, oportunidade e exceção
    - _Requisitos: 54.10, 54.10.1_

  - [ ]* 16.20 Escrever teste de propriedade para precedência de escopo
    - **Property 117: Precedência de escopo (`P11.19`)**
    - **Validates: Requirements 54.10, 54.10.1**

  - [ ] 16.21 Impedir que exceção contorne bloqueio
    - Implementar a verificação que rejeita, no motor de decisão, qualquer exceção que tentaria contornar bloqueio jurídico ou risco crítico confirmado, sem exceção por alçada
    - _Requisitos: 63.4, 63.4.1_

  - [ ]* 16.22 Escrever teste de propriedade para exceção sobre bloqueio
    - **Property 111: Exceção não contorna bloqueio (`P11.13`)**
    - **Validates: Requirements 63.4, 63.4.1**

  - [ ] 16.23 Extrair e completar a explicabilidade
    - Criar `src/radar/engines/explain.py` extraindo a explicação hoje embutida no serviço de análise, com os **onze** elementos obrigatórios e as **doze** perguntas respondidas para cada oportunidade recomendada; informar a camada determinante e a regra que a determinou, a contribuição de cada fator e as penalidades, e identificar cada valor como observado, confirmado, calculado, estimado, inferido ou desconhecido; apresentar cada exceção autorizada que influenciou o resultado, em linguagem de negócio; explicar rejeições e bloqueios com o **mesmo** nível de detalhe das recomendações; explicação sem vínculo a evidências e regras registradas classifica a análise como incompleta e impede o registro de decisão de compra
    - _Requisitos: 56.1, 56.2, 56.3, 56.4, 56.5, 56.6, 56.7, 56.8, 56.9_

  - [ ]* 16.24 Escrever teste de propriedade para condição objetiva
    - **Property 106: BUY_IF sempre traz condição objetiva (`P11.8`)**
    - **Validates: Requirements 53.7**

  - [ ]* 16.25 Escrever teste de propriedade para gatilho de reentrada
    - **Property 107: MONITOR sempre traz gatilho de reentrada (`P11.9`)**
    - **Validates: Requirements 53.8**

  - [ ]* 16.26 Escrever teste de propriedade para rastreabilidade da decisão
    - **Property 112: Rastreabilidade da decisão (`P11.14`)**
    - **Validates: Requirements 56.8, 61.4**

- [ ] 17. Checkpoint — motor de decisão
  - Executar a suíte inteira, `ruff` e `mypy --strict`; confirmar que as onze camadas têm conteúdo, que a camada determinante é a de menor índice e que nenhuma combinação de score, desconto, margem, yield, liquidez, Investor Fit ou eficiência de capital supera um bloqueio. Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 18. Due diligence, análise profunda e disciplina de lance
  - [ ] 18.1 Declarar os 234 itens de checklist como dados
    - Criar `src/radar/dd/catalog.py` com `CHECKLIST_CATALOG` contendo exatamente **234** itens: `MC-001` a `MC-136`, `B-01` a `B-27` e `C-01` a `C-71`, integrando o catálogo do Anexo A já declarado no gate jurídico; cada item traz fase, criticidade, regra de origem, condição de aprovação, condição de reprovação e o resultado devido na ausência de evidência; declarar as oito fases de `DD-0` a `DD-7`, com `DD-0` executando antes de tudo
    - _Requisitos: 36.1, 36.2, 36.5_

  - [ ]* 18.2 Escrever teste de propriedade para cobertura do catálogo
    - **Property 144: Cobertura total do catálogo de checklists (`P16.1`)**
    - **Validates: Requirements 36.5**

  - [ ] 18.3 Avaliar o checklist com vocabulário fechado
    - Criar `src/radar/dd/manager.py` com `evaluate_checklist` atribuindo a cada item aplicável exatamente um dos seis resultados; item crítico sem evidência é desconhecido, nunca aprovado; o vocabulário é fechado, sem rótulo fora dos seis mais os estados de pendência e de decisão; reprovado fica reservado a evidência de irregularidade, e falta de informação é desconhecido mais pendência de prioridade proporcional ao impacto; a profundidade deriva de score, valor da operação, risco, estratégia e custo de investigação; bloqueio óbvio em `DD-0` encerra as fases subsequentes e encaminha à decisão
    - _Requisitos: 36.3, 36.3.1, 36.3.2, 36.4, 36.6, 36.7_

  - [ ]* 18.4 Escrever teste de propriedade para ausência de evidência no checklist
    - **Property 115: Ausência de evidência nunca produz resultado favorável (`P11.17`)**
    - **Validates: Requirements 36.3.1, 36.3.2**

  - [ ] 18.5 Gerenciar pendências com condição de encerramento
    - Implementar `PendingManager` exigindo item, motivo, impacto, responsável, prazo, condição objetiva de liberação e a evidência que a encerrará, com as quatro prioridades; a resolução grava evidência de encerramento, data e autor, preserva o registro como histórico e dispara o gatilho de pendência resolvida, que recalcula confiança consolidada, Opportunity Score, Investor Fit e ranking; prazo vencido emite o alerta correspondente
    - _Requisitos: 37.1, 37.2, 37.7, 37.8, 37.9_

  - [ ] 18.6 Registrar a visita física
    - Implementar `record_visit` com data, responsável, fotos com data, observações, **áreas não acessadas** e os treze itens de estado observado; toda observação de visita é observada, nunca confirmada, e fica registrado que observação visual não constitui laudo técnico; visita não realizada aplica o acréscimo de contingência e abre pendência de vistoria de prioridade alta; estratégia e risco que exijam visita impedem `BUY` sem registro de visita
    - _Requisitos: 38.1, 38.2, 38.3, 38.4, 38.5, 38.5.1, 38.6_

  - [ ] 18.7 Implementar o contexto humano e o hard stop de parecer
    - Implementar `human_context` com o Índice de Conforto Pessoal de 0 a 100, emitindo no máximo monitoramento quando abaixo do mínimo, com o critério pessoal nomeado; aceitação de risco relevante que dependa de parecer jurídico sem o parecer registrado como evidência produz bloqueio e impede o lance, **independentemente do parâmetro de exigência do investidor**; regra eliminatória expressa do investidor produz bloqueio, não reprovação econômica, porque bloqueio sai do ranking; apresentar o contexto humano como dimensão declarada, separada das técnicas, sem inferir característica pessoal sem fonte identificada
    - _Requisitos: 39.1, 39.2, 39.3, 39.4, 39.4.1, 39.4.2, 39.5, 39.6_

  - [ ] 18.8 Implementar a análise profunda com as oito perguntas
    - Criar `src/radar/engines/deep_analysis.py` com `DeepAnalysis` exigindo a tese em uma frase, argumentos a favor vinculados a evidência ou métrica, argumentos contra vinculados a evidência, risco ou pendência, um contraponto para cada argumento contra **ou** o registro explícito de que não existe, e resposta registrada para as **oito** perguntas obrigatórias; qualquer pergunta sem resposta impede `BUY` e classifica a análise profunda como incompleta; os argumentos e contrapontos entram na explicação da decisão; cada versão é preservada sem sobrescrita
    - _Requisitos: 76.1, 76.2, 76.3, 76.4, 76.5, 76.6, 76.7, 76.8_

  - [ ] 18.9 Implementar cenários derivados como hipótese
    - Implementar `derive_scenario` criando cenário derivado identificado, preservando o de origem e registrando quais premissas mudaram, com autor, data e motivo; recalcular custo total, desconto líquido, margem, ROI líquido, retorno anualizado, yield líquido, prazo e robustez, e responder à pergunta de robustez para cada cenário; todo cenário derivado é tipo distinto, marcado como hipótese, e não pode ser base de decisão sem registro explícito de adoção
    - _Requisitos: 77.1, 77.2, 77.3, 77.4, 77.5, 77.6_

  - [ ] 18.10 Declarar os catálogos da disciplina de lance
    - Criar `src/radar/engines/bidding.py` com `HARD_STOPS` de nove condições, `PRE_BID_CHECKS` com os doze itens `PL-01` a `PL-12`, `EVICTION_CHECKS` com as nove verificações `E01` a `E09`, `FINAL_REVALIDATION` com os doze itens `RL-01` a `RL-12` e `AUCTIONEER_HISTORY` com as seis verificações `HL-01` a `HL-06`
    - A revalidação final é lista **distinta** do checklist pré-lance e mantém os quatro itens sem equivalente: condições de pagamento confirmadas, evicção documentalmente confirmada, nenhuma divergência pendente e reserva de contingência disponível
    - _Requisitos: 82.1, 82.2, 82.3, 82.4, 82.5, 82.8_

  - [ ] 18.11 Implementar a liberação conjuntiva do lance
    - Implementar `BidDiscipline` com os três tetos, sendo o absoluto definido antes da sessão, `acquisition_total` somando a comissão do leiloeiro ao custo de aquisição e nunca subtraindo-a do lance, e `bid_release` emitindo liberação **se e somente se** os doze itens pré-lance e os doze itens de revalidação estão satisfeitos, nenhum dos nove hard stops está acionado, os dois tetos estão definidos e o lance atual não excede o teto absoluto; divergência documental aberta impede o lance independentemente do restante do checklist, e permanece aberta até confirmação em fonte oficial
    - _Requisitos: 82.6, 82.7, 82.9, 82.10_

  - [ ]* 18.12 Escrever teste de propriedade para a liberação pré-lance
    - **Property 133: Liberação pré-lance é bicondicional (`P14.1`)**
    - **Validates: Requirements 82.3, 82.6**

  - [ ]* 18.13 Escrever teste de propriedade para hard stop acionado
    - **Property 134: Hard stop acionado impede o lance (`P14.2`)**
    - **Validates: Requirements 82.1, 82.2**

  - [ ]* 18.14 Escrever teste de propriedade para lance acima do teto
    - **Property 135: Lance acima do teto absoluto impede o lance (`P14.3`)**
    - **Validates: Requirements 82.6**

  - [ ]* 18.15 Escrever teste de propriedade para evicção não confirmada
    - **Property 136: Evicção não confirmada impede o lance (`P14.4`)**
    - **Validates: Requirements 82.4, 15.9, 15.9.1**

  - [ ]* 18.16 Escrever teste de propriedade para a liberação final
    - **Property 137: Liberação final exige as duas listas (`P14.5`)**
    - **Validates: Requirements 82.5, 82.6**

  - [ ]* 18.17 Escrever teste de propriedade para divergência pendente
    - **Property 138: Divergência pendente impede o lance (`P14.6`)**
    - **Validates: Requirements 82.9, 82.10**

  - [ ]* 18.18 Escrever teste de propriedade para a comissão do leiloeiro
    - **Property 139: Comissão nunca é subtraída do lance (`P14.7`)**
    - **Validates: Requirements 82.7**

- [ ] 19. Persistência, modelo físico e Gestor de Parâmetros
  - [ ] 19.1 Reescrever o esquema físico conforme *Data Models*
    - Reescrever `db/schema.sql` com todas as entidades do dicionário do design, os enums do banco espelhando os de domínio com as contagens declaradas, e as cardinalidades publicadas: fonte, captura, oferta normalizada, documento, segmento de conhecimento, proposta de evidência, imóvel, identificador, vínculo, localização, perfil, versão do perfil, histórico de preços, divergência, oportunidade, análise, evidência, fato, custo, valuation, comparável, cenário, risco, pendência, due diligence, resultado de checklist, dimensão de confiança, avaliação de estratégia, score, aplicação de regra, posição no ranking, análise profunda, verificação de lance, decisão, evento de análise, investidor, posição de portfólio, resultado real, regra, versão de regra, parâmetro, estratégia, exceção, objeto de monitoramento, alerta, trilha de auditoria e intervenção humana
    - A tabela de custos tem os treze componentes com valor, estado e origem, e **não** tem colunas de corretagem de venda, de imposto sobre ganho de capital nem de custo de oportunidade do capital
    - _Requisitos: 61.3, 61.7, 74.1, 74.2, 74.3, 74.4, 74.5, 74.6, 74.7, 74.8_

  - [ ] 19.2 Declarar os onze itens de integridade
    - Declarar no esquema: índice único **parcial** de matrícula em identificadores, com coluna de origem; unicidade de documento por fonte e hash, em lugar de hash global; unicidade de oportunidade por fonte e referência externa quando não nula; índice por análise em **todas** as tabelas filhas; verificação de escala de 0 a 100 em toda coluna de escala, incluindo a de liquidez, e verificação de versão positiva na análise; escores em `NUMERIC(5,2)` sem truncamento por conversão a inteiro; gatilhos que rejeitam atualização e remoção em análises, evidências, capturas, decisões e eventos de análise; cascade restrito a rotina nomeada de limpeza de dados de teste, fora do caminho de aplicação; migrações versionadas com seed idempotente e remoção exigindo confirmação; contrato congelado na fronteira de persistência com o mapeamento objeto-relacional cobrindo todas as tabelas; índice vetorial criado ou reconstruído depois da carga, com dimensionamento pelo volume real
    - _Requisitos: 9.1, 61.1, 61.2, 61.6, 64.3_

  - [ ] 19.3 Cobrir todas as tabelas no mapeamento objeto-relacional
    - Ampliar `src/radar/db/models.py` e `src/radar/db/repository.py` para todas as tabelas, congelar o contrato que atravessa a fronteira de persistência, remover ou mover para os argumentos de tabela as restrições declaradas fora deles, e passar a gravar a trilha de evidências, hoje modelada e nunca persistida
    - _Requisitos: 61.2, 61.3_

  - [ ] 19.4 Criar migrações versionadas e seed gerado
    - Criar migrações versionadas em `db/` com runner em `scripts/`, seed idempotente por atualização em conflito, e **geração** do seed de estratégias a partir da tabela de thresholds por estratégia, que é o ponto único de verdade; manter as constantes Python apenas como valores de arranque que alimentam o gerador; aplicar o mesmo tratamento aos pesos de score, aos limiares de materialidade e aos parâmetros de portfólio
    - _Requisitos: 62.1, 62.8, 62.10_

  - [ ]* 19.5 Escrever teste de propriedade para versionamento das análises
    - **Property 124: Versionamento monotônico e sem lacunas (`P13.2`)**
    - **Validates: Requirements 61.1**

  - [ ]* 19.6 Escrever teste de propriedade para imutabilidade das análises
    - **Property 125: Imutabilidade das análises anteriores (`P13.3`)**
    - **Validates: Requirements 61.2**

  - [ ]* 19.7 Escrever teste de propriedade para reprodutibilidade da decisão
    - **Property 126: Reprodutibilidade da decisão histórica (`P13.4`)**
    - **Validates: Requirements 61.4, 62.8**

  - [ ] 19.8 Implementar o Gestor de Parâmetros
    - Criar `src/radar/governance/parameters.py` com `resolve_parameter` percorrendo a hierarquia do escopo mais específico ao menos específico e devolvendo o primeiro valor com versão vigente na data, registrando qual escopo forneceu o valor aplicado, com a exceção do bloqueio crítico ou da restrição legal ou documental imposta por escopo menos específico; rejeitar parâmetro sem versão vigente em lugar de cair em constante de código; versionar alteração com nível de mudança e preservar o histórico das análises que usaram parâmetro removido
    - _Requisitos: 62.2, 62.4, 62.10, 62.11, 62.12_

  - [ ]* 19.9 Escrever teste de propriedade para vigência temporal
    - **Property 127: Vigência temporal das versões (`P13.5`)**
    - **Validates: Requirements 62.8**

  - [ ]* 19.10 Escrever teste de propriedade para resolução por escopo
    - **Property 130: Resolução de parâmetro pelo escopo mais específico (`P13.8`)**
    - **Validates: Requirements 62.10**

  - [ ] 19.11 Bloquear o uso de parâmetro pendente de decisão
    - Implementar a rejeição do uso de parâmetro marcado como pendente de decisão, reportando o requisito dependente como NÃO AVALIADO e nunca como satisfeito, para todos os parâmetros nesse estado
    - _Requisitos: 74.11_

  - [ ]* 19.12 Escrever teste de propriedade para parâmetro pendente
    - **Property 146: Parâmetro pendente de decisão nunca é aplicado (`P16.3`)**
    - **Validates: Requirements 74.11**

  - [ ] 19.13 Rejeitar regra que dependa de estrutura ausente
    - Implementar a verificação que rejeita a aplicação de qualquer regra que dependa de entidade ou campo ausente do dicionário, reportando o requisito dependente como NÃO AVALIADO
    - _Requisitos: 74.11_

  - [ ]* 19.14 Escrever teste de propriedade para dependência do dicionário
    - **Property 147: Regra depende só do dicionário declarado (`P16.4`)**
    - **Validates: Requirements 74.11**

- [ ] 20. Orquestração
  - [ ] 20.1 Completar o grafo com as vinte etapas
    - Reescrever `src/radar/orchestration/graph.py` com os **vinte** nós na ordem canônica — normalização, identidade, deduplicação, qualificação, consolidação de perfil, validade jurídica, enriquecimento, mercado e valuation, economia, risco, liquidez, estratégia, regras, score, Investor Fit, ranking, decisão, explicação, persistência e memória — acrescentando os três nós hoje ausentes, que tornam alcançáveis as fases de deduplicação, qualificação e consolidação; atualizar a fase a cada etapa entre as **dezesseis** fases persistidas; usar o estado compartilhado como único meio de comunicação entre etapas; proibir executar a validade jurídica antes da qualificação e da consolidação
    - _Requisitos: 70.1, 70.1.1, 70.5, 70.6_

  - [ ] 20.2 Implementar os curto-circuitos e o traço persistido
    - Implementar o desvio para a decisão em bloqueio jurídico, sem executar mercado, economia, liquidez, estratégia e score; em identidade abaixo do mínimo; e em bloqueio crítico confirmado em qualquer etapa; persistir o snapshot e registrar o traço executado em eventos de análise, além da versão do grafo em cada execução
    - _Requisitos: 70.2, 70.3, 70.4, 70.8, 70.9_

  - [ ] 20.3 Remover toda regra de negócio do grafo
    - Retirar do grafo a heurística de confiança não versionada, que passa ao Motor de Score, e o indicador de bloqueio crítico literalmente falso, que passa a ser alimentado pelo Motor de Risco; o grafo apenas sequencia, propaga estado, atualiza fase e registra traço
    - _Requisitos: 34.5, 50.4, 70.6_

  - [ ]* 20.4 Escrever teste de propriedade para o traço do pipeline
    - **Property 118: Traço é subsequência da ordem canônica (`P12.1`)**
    - **Validates: Requirements 70.1, 70.5**

  - [ ]* 20.5 Escrever teste de propriedade para o curto-circuito jurídico
    - **Property 119: Curto-circuito jurídico (`P12.2`)**
    - **Validates: Requirements 70.2, 12.2**

  - [ ]* 20.6 Escrever teste de propriedade para o curto-circuito de identidade
    - **Property 120: Curto-circuito de identidade (`P12.3`)**
    - **Validates: Requirements 70.3, 7.9**

  - [ ]* 20.7 Escrever teste de propriedade para determinismo do pipeline
    - **Property 121: Determinismo do pipeline (`P12.4`)**
    - **Validates: Requirements 70.1**

  - [ ]* 20.8 Escrever teste de propriedade para equivalência com a execução sequencial
    - **Property 122: Equivalência com a execução sequencial de referência (`P12.5`)**
    - **Validates: Requirements 70.1, 70.6**

  - [ ] 20.9 Exigir as intervenções humanas mínimas no grafo
    - Fazer o grafo exigir os pontos mínimos de intervenção humana antes das etapas que dependem deles, admitindo pontos adicionais configurados
    - _Requisitos: 70.7, 83.5_

- [ ] 21. Checkpoint — persistência e orquestração
  - Executar a suíte inteira, incluindo os testes marcados de banco contra PostgreSQL com pgvector, mais `ruff` e `mypy --strict`; confirmar que o esquema e o seed são idempotentes em duas execuções seguidas e que as fases de deduplicação, qualificação e consolidação aparecem no traço. Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

- [ ] 22. Interface de programação e configuração segura
  - [ ] 22.1 Autenticar e autorizar todas as operações expostas
    - Implementar autenticação e autorização em `src/radar/api/main.py` antes de qualquer cálculo ou persistência, respondendo sem credencial e sem autorização com os códigos próprios, e registrar cada operação exposta na trilha de auditoria
    - _Requisitos: 79.8, 79.10_

  - [ ] 22.2 Implementar os endpoints do contrato
    - Implementar visão geral com oportunidades novas, melhores por estratégia, mudanças relevantes, alertas críticos, análises pendentes, teses em monitoramento e indicadores consolidados; ações de salvar, monitorar e criar alerta registrando ator, papel, data e motivo; linha do tempo com os doze eventos em ordem cronológica e a versão de análise; comparação de duas a cinco oportunidades, rejeitando fora da faixa com a causa explicitada; listagem de monitoramento com motivo, condição de entrada, estado do objeto, score atual, última atualização, próximo gatilho e alertas relacionados; e registro das **oito** decisões do investidor
    - _Requisitos: 79.1, 79.2, 79.3, 79.4, 79.5, 79.6, 79.7_

  - [ ] 22.3 Traduzir a taxonomia de erro na fronteira
    - Implementar o manipulador global que mapeia cada erro de domínio para o código próprio — entrada e contrato, violação de invariante e indisponibilidade — informando código, mensagem, campo e sugestão, sem rastreamento de pilha, consulta, caminho de arquivo nem valor de configuração no corpo; o rastreamento vai para o log estruturado correlacionado por identificador de requisição; valor de mercado não positivo passa a responder com erro de entrada, nunca com falha de execução
    - _Requisitos: 79.9_

  - [ ] 22.4 Completar o contrato de custo na entrada
    - Expor no corpo da requisição de análise **todos** os treze componentes do custo econômico total, incluindo tributos, custo jurídico potencial, probabilidade jurídica e carrying, hoje omitidos e entrando como zero; ausência é representada como desconhecida, nunca por omissão com default numérico
    - _Requisitos: 26.1, 26.7, 26.10_

  - [ ] 22.5 Endurecer a configuração
    - Adotar `pydantic-settings` como via única de configuração, removendo os leitores de arquivo de ambiente reimplementados em `scripts/`, que ignoram variáveis de ambiente reais; segredo como tipo redigido, sem nenhum default de credencial, com ausência levantando erro na carga; validação completa de certificado e nome do servidor fora do ambiente local; porta do banco não publicada por default no `docker-compose.yml`; fábrica preguiçosa de engine e de sessão com limites de pool, tempo de espera e política de retry, de modo que importar os módulos de banco deixe de exigir configuração válida em teste unitário; CORS restritivo e limite de taxa antes de qualquer exposição além do ambiente local
    - _Requisitos: 79.8_

  - [ ] 22.6 Implementar as visões do radar e a ficha da oportunidade
    - Implementar as **oito** visões pré-definidas como parametrizações da mesma consulta — top oportunidades, por estratégia, por região, novidades, queda de preço, score crescente, em monitoramento e bloqueadas com motivo —, apresentando na visão de bloqueadas a camada determinante e o motivo impeditivo e mantendo-as fora do ranking operacional; implementar a ficha com o aprofundamento progressivo do resumo para o detalhe e do detalhe para a evidência original, a comparação com os indicadores exigidos e o registro histórico das decisões do investidor; manter filtro de visualização separado de regra eliminatória, sem que filtro elimine oportunidade
    - _Requisitos: 66.4.1, 66.4.2, 66.12, 67.1, 67.2, 67.3, 67.4, 67.12, 68.1, 68.6, 68.7_

- [ ] 23. Monitoramento, governança e conclusão dos requisitos `P0`
  - [ ] 23.1 Declarar os limiares de materialidade
    - Criar `src/radar/monitoring/monitor.py` com `MATERIALITY_THRESHOLDS` declarando `MON-001` a `MON-017` como dados, incluindo o gatilho de pendência resolvida, os seis sinais de mercado obrigatórios e o gatilho de nova oportunidade excepcional que dispara a recomparação da carteira; a comparação com o limiar usa `>=`, de modo que a mudança de magnitude exatamente igual ao limiar **dispara**
    - _Requisitos: 57.1, 57.2, 57.3, 57.3.1, 57.3.2_

  - [ ] 23.2 Implementar a reavaliação por materialidade
    - Implementar `on_change` classificando a materialidade em cinco níveis e aplicando a ação devida: crítico reavalia imediatamente e bloqueia quando o gatilho é risco impeditivo; alto reavalia por completo; médio reavalia parcialmente as dimensões afetadas; baixo e informativo apenas registram no histórico; reprocessar somente as camadas afetadas, propagar o efeito ao score e ao ranking e registrar quais dimensões foram reprocessadas e por quê
    - _Requisitos: 57.4, 57.5, 57.6, 57.7, 57.8, 57.9_

  - [ ]* 23.3 Escrever teste de propriedade para o limiar de materialidade
    - **Property 123: Limiar de materialidade dispara no valor exato (`P13.1`)**
    - **Validates: Requirements 57.2, 57.3**

  - [ ] 23.4 Implementar o objeto de monitoramento, a reentrada e o abandono
    - Implementar `MonitoringState` com os **dez** estados e o objeto de monitoramento com motivo, tese atual, gatilho de reentrada, gatilho de abandono, preço-alvo, score mínimo, liquidez mínima, pendências relevantes, próxima revisão e histórico de transições; acompanhar cada condição objetiva registrada em decisão condicional e alertar quando satisfeita; disparar reentrada por queda de preço ao patamar de interesse, risco impeditivo resolvido com evidência, liquidez acima do mínimo, valuation materialmente maior, nova estratégia que passa a aceitar o imóvel e dado antes desconhecido confirmado; exigir motivo de uma lista fechada de oito para abandono, preservando o histórico completo e permitindo reabertura
    - _Requisitos: 57.10, 57.10.1, 57.10.2, 57.11, 58.1, 58.2, 58.3, 58.4, 58.5, 58.6, 58.7, 58.8_

  - [ ]* 23.5 Escrever teste de propriedade para idempotência da reavaliação
    - **Property 132: Idempotência da reavaliação (`P13.10`)**
    - **Validates: Requirements 57.6, 61.1**

  - [ ] 23.6 Implementar a trilha de auditoria
    - Criar `src/radar/governance/audit.py` registrando os **22** tipos de evento com data, ator, papel, objeto, valor anterior, valor novo e motivo, sem exclusão nem alteração, incluindo o registro de execução, e mantendo os **sete** indicadores de governança: decisões reproduzíveis, regras com versão, decisões com justificativa, decisões com evidência, exceções justificadas, mudanças auditáveis e dados sem origem
    - _Requisitos: 64.1, 64.2, 64.3, 64.4, 64.5_

  - [ ]* 23.7 Escrever teste de propriedade para a trilha append-only
    - **Property 129: Trilha de auditoria é append-only (`P13.7`)**
    - **Validates: Requirements 64.1, 64.3**

  - [ ] 23.8 Implementar as exceções auditáveis
    - Criar `src/radar/governance/exceptions.py` exigindo os campos obrigatórios da exceção — regra excepcionada, valor normal, valor excepcional, risco aceito, justificativa, evidência, alçada, prazo e impacto no score —, restaurando a regra padrão após a data de validade e disparando a reavaliação, e registrando recomendação de revisão quando a mesma regra é excepcionada de forma recorrente acima do limiar configurado
    - _Requisitos: 63.1, 63.2, 63.3, 63.5, 63.6, 63.7_

  - [ ]* 23.9 Escrever teste de propriedade para expiração de exceção
    - **Property 131: Expiração de exceção restaura a regra (`P13.9`)**
    - **Validates: Requirements 63.5**

  - [ ] 23.10 Congelar os sete pontos mínimos de supervisão humana
    - Declarar o conjunto congelado dos **sete** pontos mínimos — promover evidência jurídica a confirmada, aceitar risco de severidade alto, criar exceção, aprovar mudança de nível alto ou crítico, confirmar divergência documental, liberar lance e registrar decisão de compra —, rejeitar configuração que remova qualquer um deles e registrar cada intervenção com ator, papel, data, objeto afetado e justificativa
    - _Requisitos: 83.1, 83.2, 83.3, 83.4, 83.5, 83.6, 83.7_

  - [ ]* 23.11 Escrever teste de propriedade para os pontos de supervisão
    - **Property 148: Pontos mínimos de supervisão não são removíveis (`P16.5`)**
    - **Validates: Requirements 83.5, 83.6**

  - [ ] 23.12 Aplicar os guarda-corpos dos componentes de IA
    - Garantir que nenhum cálculo determinístico e nenhuma decisão dependem de modelo de linguagem, que o agente apenas interpreta e propõe, que cada ferramenta invocada é registrada com entradas, saídas e resultado na trilha, e ligar o meta-teste de isolamento para falhar com o caminho completo de qualquer import proibido a partir dos pacotes de motores e de pipeline
    - _Requisitos: 71.1, 71.2, 71.3, 71.4, 71.7, 71.8, 71.9, 71.10_

  - [ ] 23.13 Declarar a priorização dos 83 requisitos como dado
    - Declarar o índice de prioridade com exatamente uma classificação por requisito de 1 a 83 e as contagens de 69 `P0`, 13 `P1` e 1 `P2`, nenhum fora do MVP; declarar as 23 capacidades `P0`, as nove `P1`, as oito `P2` e os nove itens fora da primeira versão; implementar a classificação de nova necessidade nas seis categorias de controle de escopo e a exigência de registro de impacto para mudança estrutural
    - _Requisitos: 75.1, 75.2, 75.3, 75.4, 75.5, 75.6, 75.7_

  - [ ]* 23.14 Escrever teste de propriedade para a cobertura de prioridade
    - **Property 145: Cobertura de prioridade dos requisitos (`P16.2`)**
    - **Validates: Requirements 75.5**

  - [ ] 23.15 Implementar as configurações do investidor
    - Implementar os **doze** grupos de configuração — capital, ticket, estratégias, localização, tipos de imóvel, desconto, margem, yield, liquidez, risco, reforma e alertas —, incluindo os parâmetros de reserva percentual do patrimônio líquido, esforço operacional aceitável e meta de renda mensal; exibir para cada configuração o identificador do parâmetro do catálogo e o escopo em que o valor se aplica; a alteração cria nova versão com valor anterior, valor novo, autor e data e dispara o reprocessamento pelos gatilhos correspondentes; rejeitar configuração que contorne bloqueio jurídico ou risco crítico
    - _Requisitos: 78.1, 78.2, 78.3, 78.4, 78.5, 78.6, 78.7_

- [ ] 24. Requisitos `P1`
  - [ ] 24.1 Implementar o enriquecimento progressivo
    - Implementar `preliminary_potential` com as cinco faixas qualitativas derivadas do desconto sobre o valor de referência da fonte, do enquadramento no escopo de localização e tipo e do enquadramento no ticket — **sem depender de score**, para não criar ciclo com o valuation — e `enrichment_depth` mapeando as faixas para os níveis de 0 a 8, com o topo do ranking incluindo o nível mais profundo; registrar origem, data de obtenção e nível de confiança de cada informação enriquecida
    - _Requisitos: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8_

  - [ ] 24.2 Modelar financiamento
    - Implementar entrada, parcelas, juros, seguros, tarifas, prazo, amortização e saldo devedor, com juros e custos financeiros entrando no custo total pelo componente financeiro; simular quitação antecipada; comparar retorno sobre capital próprio entre à vista, financiado e híbrido; parcela acima do limite do investidor classifica a operação como não aderente ao capital; forma de pagamento da fonte que exclui financiamento restringe os cenários modelados
    - _Requisitos: 31.1, 31.2, 31.3, 31.4, 31.5, 31.6_

  - [ ] 24.3 Modelar estratégias de saída híbridas
    - Implementar os fluxos de comprar-reformar-alugar-vender, comprar-alugar-aguardar-valorização e comprar-regularizar-desenvolver-vender, com custos, receitas e prazos por etapa, retorno total somando a renda do período ao resultado da saída final e liquidez exigida avaliada em cada etapa
    - _Requisitos: 42.1, 42.2, 42.3, 42.4_

  - [ ] 24.4 Monitorar a liquidez
    - Acompanhar concorrentes e seus preços, aluguel de mercado, demanda, tempo de anúncio, condições de financiamento, ticket do segmento e infraestrutura, e disparar, na variação material, o recálculo de score, de margem exigida e de **preço máximo**
    - _Requisitos: 43.1, 43.2, 43.3_

  - [ ] 24.5 Simular alocação e consolidar eficiência de capital
    - Implementar `simulate_allocation` com capital necessário, capital residual, percentual do portfólio, exposição estratégica resultante, exposição de risco resultante, impacto na renda e liquidez consolidada da carteira, executando também no cenário conservador, comparando com as oportunidades que competem pelo mesmo capital, emitindo recomendação de alocação justificada e confrontando o retorno com as alternativas de custo de oportunidade configuradas; consolidar as métricas de eficiência para a carteira, aplicar as faixas de ação por posição e registrar a recomendação de rebalanceamento quando o desvio de alocação é excedido
    - _Requisitos: 48.1, 48.2, 48.3, 48.4, 48.5, 81.1, 81.2, 81.3, 81.4, 81.5_

  - [ ] 24.6 Implementar o catálogo de alertas
    - Criar `src/radar/monitoring/alerts.py` com `ALERT_CATALOG` de `ALT-001` a `ALT-020`, incluindo os três alertas de ranking e os alertas de prazo de pendência vencido e de reserva comprometida; cada alerta informa evento, impacto quantificado, consequência na tese e próxima ação, com prioridade atribuída; agrupar alertas relacionados da mesma oportunidade, não repetir alerta para o mesmo fato sem mudança material, respeitar a frequência máxima diária por oportunidade, elevar prioridade somente quando a situação subjacente piora e permitir silenciar uma oportunidade sem encerrar o monitoramento
    - _Requisitos: 59.1, 59.2, 59.3, 59.3.1, 59.4, 59.5, 59.6, 59.7, 59.8, 59.9, 59.10_

  - [ ] 24.7 Implementar resultado real e backtest com corte temporal
    - Criar `src/radar/backtest/engine.py` registrando o resultado real com preço pago, custos reais, custo e prazo reais de reforma, aluguel realizado, vacância real, preço de venda efetivo, prazo real de saída e retorno realizado; reproduzir o estado com as versões vigentes na data e passar todo acesso a dados por um filtro de corte pela data da decisão, rejeitando e registrando o dado posterior; medir precisão, recall, taxa de falso positivo, taxa de falso negativo e os erros de valuation, prazo, aluguel e custo; construir a coorte de rejeitadas e ignoradas com o resultado observado de cada uma, reportando NÃO AVALIADO para coorte vazia em lugar de zero; separar amostra de calibração de amostra de verificação, registrar o desempenho em ambas antes de propor calibração e rejeitar a proposta quando o desempenho na calibração excede o da verificação além do limiar, registrando o indício de sobreajuste; nenhuma regra crítica é alterada automaticamente
    - _Requisitos: 60.1, 60.2, 60.3, 60.3.1, 60.3.2, 60.3.3, 60.3.4, 60.4, 60.5, 60.6, 60.7_

  - [ ]* 24.8 Escrever teste de propriedade para o antiviés temporal
    - **Property 128: Antiviés temporal no backtest (`P13.6`)**
    - **Validates: Requirements 60.4, 60.5**

  - [ ] 24.9 Publicar os indicadores de aprendizado
    - Publicar falso positivo e falso negativo em conjunto, apresentar em qualquer proposta de calibração o efeito simultâneo sobre ambos com a troca aceita registrada, e classificar a qualidade da evidência de cada verificação publicando a distribuição por domínio
    - _Requisitos: 80.1, 80.2, 80.3, 80.4, 80.5_

  - [ ] 24.10 Implementar o controle de qualidade das regras
    - Criar `src/radar/governance/quality.py` verificando coerência e cobertura antes da publicação, com os cinco níveis de qualidade de evidência, a exigência de qualidade mínima para regra jurídica crítica, o registro da qualidade por verificação, e a lista de fatos que invalidariam o resultado exigida de cada caso de prova
    - _Requisitos: 65.1, 65.1.1, 65.1.2, 65.1.3, 65.2, 65.3, 65.4, 65.5, 65.6_

  - [ ] 24.11 Implementar os relatórios de negócio
    - Implementar as visões consolidadas de desempenho do processo previstas no requisito, a partir das entidades já persistidas, sem recálculo fora dos motores
    - _Requisitos: 69.1, 69.2, 69.3, 69.4, 69.5, 69.6_

- [ ] 25. Requisito `P2` — esteira de conhecimento e RAG
  - [ ] 25.1 Implementar a esteira obrigatória de ingestão
    - Criar `src/radar/knowledge/ingest.py` com a esteira completa: fingerprint, catalogação da fonte, extração, limpeza, classificação, segmentação semântica, metadados, representação vetorial e persistência, idempotente por fingerprint de modo que reingerir o mesmo documento não duplique segmentos
    - _Requisitos: 72.1_

  - [ ] 25.2 Declarar os quinze tipos de segmento e separar texto-fonte de paráfrase
    - Declarar `KnowledgeSegmentType` com os **quinze** valores — regra, definição, fórmula, checklist, evidência, caso, análise, manual, parâmetro, exceção, decisão, governança, guia de evidência, estratégia e segurança — e os **vinte** metadados obrigatórios, com `source_text` e `paraphrase` como campos distintos e rotulados; rejeitar indexação de segmento com os dois fundidos no mesmo campo e de item crítico sem identificador
    - _Requisitos: 72.2, 72.3, 72.3.1, 72.3.2, 72.4_

  - [ ]* 25.3 Escrever teste de propriedade para metadados obrigatórios
    - **Property 140: Metadados obrigatórios em todo segmento (`P15.1`)**
    - **Validates: Requirements 72.3, 72.4**

  - [ ]* 25.4 Escrever teste de propriedade para texto-fonte e paráfrase
    - **Property 149: Texto-fonte e paráfrase permanecem distinguíveis (`P16.6`)**
    - **Validates: Requirements 72.3.1, 72.3.2**

  - [ ]* 25.5 Escrever teste de propriedade para idempotência da reingestão
    - **Property 142: Idempotência da reingestão (`P15.3`)**
    - **Validates: Requirements 72.1**

  - [ ] 25.6 Rejeitar indexação sem proveniência
    - Rejeitar a indexação de segmento de regra jurídica crítica sem fonte e proveniência, e de parâmetro histórico sem a marcação de que não é universal
    - _Requisitos: 72.5, 72.6_

  - [ ]* 25.7 Escrever teste de propriedade para regra jurídica sem proveniência
    - **Property 141: Regra jurídica exige fonte e proveniência (`P15.2`)**
    - **Validates: Requirements 72.5**

  - [ ] 25.8 Separar as três camadas de memória
    - Criar `src/radar/knowledge/retrieve.py` com as três camadas separadas — conhecimento normativo, histórico estruturado e contexto do imóvel — e marcar **todo** item recuperado da memória histórica como hipótese, nunca como evidência atual, informando na recuperação qual parte é texto-fonte e qual é paráfrase
    - _Requisitos: 72.7, 72.8, 72.9_

  - [ ]* 25.9 Escrever teste de propriedade para a memória histórica
    - **Property 143: Memória histórica é sempre hipótese (`P15.4`)**
    - **Validates: Requirements 72.9**

  - [ ] 25.10 Reconstruir o índice vetorial após a carga
    - Criar a rotina em `scripts/` que cria ou reconstrói o índice vetorial depois da ingestão, com o dimensionamento pelo volume real, em lugar de construí-lo sobre tabela vazia
    - _Requisitos: 72.1_

- [ ] 26. Golden Cases, testes de regressão e meta-verificações
  - [ ] 26.1 Escrever o Golden Case `F.1` como oráculo econômico
    - Criar `tests/golden/test_f1.py` com as entradas publicadas (lance mínimo R$ 191.651,31; comissão 5%; ITBI 2%; registro R$ 3.000,00; condomínio e débitos R$ 5.000,00; tributos R$ 0,00; reforma R$ 10.000,00; custo jurídico R$ 0,00 e probabilidade 0,00 **declarados**; corretagem 6%; IR 15%; preço de venda de referência R$ 300.000,00; valor de mercado provável R$ 290.000,00; aluguel R$ 1.900,00; condomínio R$ 510,00; IPTU R$ 25,00; manutenção R$ 100,00; vacância R$ 95,00; prazo 3 meses; carrying mensal R$ 635,00; ROI alvo 25%; custos fixos R$ 23.000,00) e os valores esperados:
      reserva R$ 11.153,345085 · carrying R$ 1.905,00 · **TCO econômico R$ 236.125,246785** · **desconto líquido 0,1857750 → 18,5775%** · margem absoluta R$ 53.874,753215 · base de IR na venda R$ 45.874,753215 · venda líquida R$ 275.118,78701775 · lucro líquido R$ 38.993,54023275 · **ROI líquido 0,1651392 → 16,5139%** · **ROI anualizado 0,8429404 → 84,2940%** · break-even R$ 251.197,07105 · distância do break-even 0,3107, que não aciona monitoramento · aluguel líquido R$ 1.170,00 · base de IR sobre aluguel R$ 1.265,00 · yield bruto mensal 0,0080466 · yield líquido mensal 0,0049550 · **preço máximo por ROI alvo R$ 182.158,03** · **verificação inversa do ROI igual a 0,250000 com erro menor que 10^-6** · teto conservador informativo R$ 168.374,76 · veredito de revenda reprovado pela camada 4 · veredito de renda reprovado pela camada 5
    - Registrar a lista de fatos que invalidariam o resultado, sem a qual o caso vira número mágico
    - _Requisitos: 73.1, 73.7_

  - [ ] 26.2 Escrever os Golden Cases `F.2`, `F.3` e `F.4`
    - `F.2` com averbação de leilões negativos em tratamento, resultando em pendência registral com custo, prazo e documentação no custo econômico total, sem bloqueio automático; `F.3` com consolidação em 31/07/2026, matrícula emitida em 03/08/2026, avaliação da fonte R$ 230.000,00 e valor mínimo do segundo leilão R$ 138.000,00 — 60% da avaliação, que **não** aciona a regra do segundo leilão —, decisão de referência condicional com confiança aproximada de 78; `F.4` com leitura do texto do ato registral na averbação indicada, gravame histórico baixado distinguido de gravame atual e valuation independente da avaliação da fonte de R$ 285.000,00
    - Cada caso declara a lista de fatos que invalidariam o resultado
    - _Requisitos: 73.1, 73.7_

  - [ ] 26.3 Escrever os testes de regressão `REG-001` a `REG-018`
    - Um teste por linha, nomeado pelo identificador, em `tests/regression/`: consolidação não comprovada; consolidação comprovada com texto do ato; averbação em tratamento; processo sem impacto material; liminar sobre o leilão; imóvel ocupado; poucos comparáveis; score alto com bloqueio jurídico; avaliação da fonte acima dos comparáveis; custo com componente crítico desconhecido; segundo leilão abaixo da metade da avaliação; investidor que não aceita ocupação; garantia contra evicção não confirmada; divergência entre data do portal e data do edital; custo acima do limite por operação; capital livre abaixo da reserva mínima; score alto com Investor Fit abaixo do mínimo; backtest recebendo dado posterior à decisão
    - _Requisitos: 73.8_

  - [ ] 26.4 Escrever os testes de regressão `REG-019` a `REG-035`
    - Ponto como separador decimal em `"47.76"` e `"191651.31"`, interpretados como 47,76 e 191.651,31; percentual `"2.5%"` e `1` com unidade de porcentagem, resultando em 0,025 e 0,01; score e confiança 89,5 classificados como excelente com fator 0,95 e sem lacuna em todo o domínio; status jurídico fora do enum, inclusive minúsculo e vazio, falhando explicitamente; chamada sem o resultado do gate assumindo pendente e elegibilidade falsa; verificação irregular com evidência de confiança compatível; verificação não aplicável distinta de desconhecida; mesma matrícula em dois imóveis rejeitada na integridade; captura reprocessada gerando um único registro; esquema e seed idempotentes em duas execuções; valor de mercado não positivo respondendo com erro de entrada; captura de fonte diferente exigindo normalizador próprio; os dois casos de bloqueio pela camada 0; os dois casos de evicção com lance não liberado em nenhum; o contraexemplo do teto conservador com as entradas completas — teto conservador R$ 199.230,77 excedendo o preço máximo exato R$ 192.952,38 com diferença de R$ 6.278,39, e com ITBI de 2% o exato caindo a R$ 189.345,79 com diferença de R$ 9.884,98; pendência resolvida recalculando confiança, score, Investor Fit e ranking; risco crítico com evidência estimada bloqueando como presumido com condição objetiva de desbloqueio
    - _Requisitos: 73.8_

  - [ ] 26.5 Completar os meta-testes `MT-01` a `MT-05`
    - Rastreabilidade dos identificadores de propriedade entre requirements e design, com a única exceção declarada do contraexemplo; exatamente um teste por propriedade para a numeração de 1 a 149; cobertura dos 234 itens de checklist; cobertura das 55 regras do catálogo; cobertura dos itens de disciplina de lance — nove hard stops, doze pré-lance, nove de evicção, doze de revalidação final e seis de histórico do leiloeiro
    - _Requisitos: 73.2, 73.3, 73.5, 73.8_

  - [ ] 26.6 Completar os meta-testes `MT-06` a `MT-10`
    - Cobertura de prioridade com as contagens de 69 `P0`, 13 `P1` e 1 `P2`; ponto único de verdade comparando a tabela de thresholds, as constantes Python e o seed do banco; soma de pesos dos conjuntos mestre, por estratégia, do Investor Fit e de liquidez em 1,00, e do score econômico em 100; contagem de valores de cada enum conforme *Data Models*; isolamento da camada de IA percorrendo a árvore de imports a partir de cada módulo de motores e de pipeline e falhando com o caminho completo do import proibido
    - _Requisitos: 71.1, 71.2, 75.5_

  - [ ] 26.7 Escrever os testes de invariante dos princípios invioláveis
    - Testes dedicados para: nenhuma evidência criada sem fonte; desconhecido não se transforma em confirmado sem nova evidência; score, desconto, margem, yield, liquidez e Investor Fit não superam um bloqueio; toda decisão vinculada a evidências e regras registradas; histórico não convertido em fato atual
    - _Requisitos: 73.2, 73.3, 73.4, 73.5, 73.6_

- [ ] 27. Checkpoint final
  - Executar a suíte inteira nos perfis `dev` e `ci`, incluindo os testes marcados de banco, mais `ruff` e `mypy --strict`; confirmar as 149 propriedades com um teste cada, os 35 testes de regressão, os quatro Golden Cases e os dez meta-testes verdes. Assegurar que todos os testes passam, e perguntar ao usuário se surgirem dúvidas.

## Notes

- Sub-tarefas marcadas com `*` são opcionais e podem ser adiadas para um MVP mais rápido; as tarefas de implementação não são opcionais.
- Cada uma das **149** propriedades do design tem exatamente uma sub-tarefa de teste, com o número e o título da propriedade e a lista de critérios que ela valida.
- Toda tarefa de implementação referencia critérios de aceitação da numeração atual de `R1` a `R83`.
- A ordem das tarefas de topo é a das 15 etapas do design, e nenhuma tarefa de requisito `P1` ou `P2` antecede uma tarefa de requisito `P0`.
- Os checkpoints verificam a suíte inteira, `ruff` e `mypy --strict`, que são condição de merge.
- `requirements.md` e `design.md` são as únicas fontes: nenhuma tarefa depende de documento externo à spec.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.5", "1.6"] },
    { "id": 1, "tasks": ["1.3", "1.7"] },
    { "id": 2, "tasks": ["1.4"] },
    { "id": 3, "tasks": ["2.1"] },
    { "id": 4, "tasks": ["2.2", "2.3"] },
    { "id": 5, "tasks": ["2.4"] },
    { "id": 6, "tasks": ["2.5"] },
    { "id": 7, "tasks": ["2.6"] },
    { "id": 8, "tasks": ["2.7", "2.8", "2.9", "2.10"] },
    { "id": 9, "tasks": ["2.11"] },
    { "id": 10, "tasks": ["2.12"] },
    { "id": 11, "tasks": ["2.13"] },
    { "id": 12, "tasks": ["4.1", "4.2"] },
    { "id": 13, "tasks": ["4.3", "4.4", "4.5"] },
    { "id": 14, "tasks": ["4.6"] },
    { "id": 15, "tasks": ["4.7", "4.8"] },
    { "id": 16, "tasks": ["4.9"] },
    { "id": 17, "tasks": ["4.10"] },
    { "id": 18, "tasks": ["4.11"] },
    { "id": 19, "tasks": ["4.12", "4.13", "4.14", "4.15", "4.16", "4.17"] },
    { "id": 20, "tasks": ["5.1"] },
    { "id": 21, "tasks": ["5.2"] },
    { "id": 22, "tasks": ["5.3", "5.4", "5.5"] },
    { "id": 23, "tasks": ["5.6"] },
    { "id": 24, "tasks": ["5.7"] },
    { "id": 25, "tasks": ["5.8", "5.9", "5.10", "5.11", "5.12", "5.13", "5.14"] },
    { "id": 26, "tasks": ["5.15", "5.16"] },
    { "id": 27, "tasks": ["6.1"] },
    { "id": 28, "tasks": ["6.2", "6.3"] },
    { "id": 29, "tasks": ["6.4", "6.5"] },
    { "id": 30, "tasks": ["7.1"] },
    { "id": 31, "tasks": ["7.2", "7.3", "7.4"] },
    { "id": 32, "tasks": ["7.5"] },
    { "id": 33, "tasks": ["7.6", "7.7"] },
    { "id": 34, "tasks": ["8.1"] },
    { "id": 35, "tasks": ["8.2"] },
    { "id": 36, "tasks": ["8.3", "8.4", "8.5", "8.6", "8.7"] },
    { "id": 37, "tasks": ["8.8", "8.9", "8.10"] },
    { "id": 38, "tasks": ["8.11", "8.13", "8.15", "8.16", "8.18"] },
    { "id": 39, "tasks": ["8.12", "8.14", "8.17"] },
    { "id": 40, "tasks": ["8.19"] },
    { "id": 41, "tasks": ["8.20"] },
    { "id": 42, "tasks": ["10.1"] },
    { "id": 43, "tasks": ["10.2"] },
    { "id": 44, "tasks": ["10.3"] },
    { "id": 45, "tasks": ["10.4"] },
    { "id": 46, "tasks": ["10.5", "10.6"] },
    { "id": 47, "tasks": ["11.1"] },
    { "id": 48, "tasks": ["11.2", "11.3"] },
    { "id": 49, "tasks": ["11.4"] },
    { "id": 50, "tasks": ["11.5", "11.6", "11.7"] },
    { "id": 51, "tasks": ["11.8"] },
    { "id": 52, "tasks": ["11.9", "11.10", "11.11"] },
    { "id": 53, "tasks": ["11.12"] },
    { "id": 54, "tasks": ["11.13"] },
    { "id": 55, "tasks": ["11.14"] },
    { "id": 56, "tasks": ["11.15"] },
    { "id": 57, "tasks": ["11.16"] },
    { "id": 58, "tasks": ["11.17", "11.18"] },
    { "id": 59, "tasks": ["11.19"] },
    { "id": 60, "tasks": ["11.20"] },
    { "id": 61, "tasks": ["12.1"] },
    { "id": 62, "tasks": ["12.2", "12.3", "12.4", "12.5", "12.6", "12.7"] },
    { "id": 63, "tasks": ["12.8"] },
    { "id": 64, "tasks": ["12.9"] },
    { "id": 65, "tasks": ["12.10"] },
    { "id": 66, "tasks": ["12.11"] },
    { "id": 67, "tasks": ["12.12"] },
    { "id": 68, "tasks": ["12.13", "12.14"] },
    { "id": 69, "tasks": ["12.15"] },
    { "id": 70, "tasks": ["12.16"] },
    { "id": 71, "tasks": ["12.17"] },
    { "id": 72, "tasks": ["12.18"] },
    { "id": 73, "tasks": ["13.1"] },
    { "id": 74, "tasks": ["13.2"] },
    { "id": 75, "tasks": ["13.3"] },
    { "id": 76, "tasks": ["13.4", "13.5"] },
    { "id": 77, "tasks": ["13.6"] },
    { "id": 78, "tasks": ["13.7"] },
    { "id": 79, "tasks": ["14.1", "14.10"] },
    { "id": 80, "tasks": ["14.2", "14.3", "14.11", "14.12", "14.13"] },
    { "id": 81, "tasks": ["14.4", "14.14"] },
    { "id": 82, "tasks": ["14.5", "14.6", "14.15"] },
    { "id": 83, "tasks": ["14.7", "14.16"] },
    { "id": 84, "tasks": ["14.8", "14.17"] },
    { "id": 85, "tasks": ["14.9", "14.18"] },
    { "id": 86, "tasks": ["15.1", "15.3", "15.6"] },
    { "id": 87, "tasks": ["15.2", "15.4", "15.7", "15.8", "15.9", "15.10", "15.11", "15.12"] },
    { "id": 88, "tasks": ["15.5", "15.13"] },
    { "id": 89, "tasks": ["15.14"] },
    { "id": 90, "tasks": ["15.15"] },
    { "id": 91, "tasks": ["15.16", "15.17", "15.18"] },
    { "id": 92, "tasks": ["15.19"] },
    { "id": 93, "tasks": ["15.20", "15.21"] },
    { "id": 94, "tasks": ["15.22"] },
    { "id": 95, "tasks": ["15.23", "15.24", "15.25", "15.26", "15.27", "15.28", "15.29"] },
    { "id": 96, "tasks": ["15.30"] },
    { "id": 97, "tasks": ["16.1"] },
    { "id": 98, "tasks": ["16.2"] },
    { "id": 99, "tasks": ["16.3"] },
    { "id": 100, "tasks": ["16.4", "16.5", "16.6", "16.7", "16.8", "16.9"] },
    { "id": 101, "tasks": ["16.10"] },
    { "id": 102, "tasks": ["16.11", "16.12"] },
    { "id": 103, "tasks": ["16.13"] },
    { "id": 104, "tasks": ["16.14", "16.15", "16.16", "16.17"] },
    { "id": 105, "tasks": ["16.18"] },
    { "id": 106, "tasks": ["16.19"] },
    { "id": 107, "tasks": ["16.20"] },
    { "id": 108, "tasks": ["16.21"] },
    { "id": 109, "tasks": ["16.22"] },
    { "id": 110, "tasks": ["16.23"] },
    { "id": 111, "tasks": ["16.24", "16.25", "16.26"] },
    { "id": 112, "tasks": ["18.1"] },
    { "id": 113, "tasks": ["18.2"] },
    { "id": 114, "tasks": ["18.3"] },
    { "id": 115, "tasks": ["18.4"] },
    { "id": 116, "tasks": ["18.5", "18.6", "18.7", "18.8", "18.9", "18.10"] },
    { "id": 117, "tasks": ["18.11"] },
    { "id": 118, "tasks": ["18.12", "18.13", "18.14", "18.15", "18.16", "18.17", "18.18"] },
    { "id": 119, "tasks": ["19.1"] },
    { "id": 120, "tasks": ["19.2"] },
    { "id": 121, "tasks": ["19.3"] },
    { "id": 122, "tasks": ["19.4"] },
    { "id": 123, "tasks": ["19.5", "19.6", "19.7"] },
    { "id": 124, "tasks": ["19.8"] },
    { "id": 125, "tasks": ["19.9", "19.10"] },
    { "id": 126, "tasks": ["19.11"] },
    { "id": 127, "tasks": ["19.12"] },
    { "id": 128, "tasks": ["19.13"] },
    { "id": 129, "tasks": ["19.14"] },
    { "id": 130, "tasks": ["20.1"] },
    { "id": 131, "tasks": ["20.2"] },
    { "id": 132, "tasks": ["20.3"] },
    { "id": 133, "tasks": ["20.4", "20.5", "20.6", "20.7", "20.8"] },
    { "id": 134, "tasks": ["20.9"] },
    { "id": 135, "tasks": ["22.1"] },
    { "id": 136, "tasks": ["22.2"] },
    { "id": 137, "tasks": ["22.3"] },
    { "id": 138, "tasks": ["22.4"] },
    { "id": 139, "tasks": ["22.5"] },
    { "id": 140, "tasks": ["22.6"] },
    { "id": 141, "tasks": ["23.1"] },
    { "id": 142, "tasks": ["23.2"] },
    { "id": 143, "tasks": ["23.3"] },
    { "id": 144, "tasks": ["23.4"] },
    { "id": 145, "tasks": ["23.5"] },
    { "id": 146, "tasks": ["23.6", "23.8", "23.10", "23.13", "23.15"] },
    { "id": 147, "tasks": ["23.7", "23.9", "23.11", "23.14"] },
    { "id": 148, "tasks": ["23.12"] },
    { "id": 149, "tasks": ["24.1", "24.2", "24.3", "24.4", "24.5", "24.6", "24.7", "24.10", "24.11"] },
    { "id": 150, "tasks": ["24.8", "24.9"] },
    { "id": 151, "tasks": ["25.1"] },
    { "id": 152, "tasks": ["25.2"] },
    { "id": 153, "tasks": ["25.3", "25.4", "25.5"] },
    { "id": 154, "tasks": ["25.6"] },
    { "id": 155, "tasks": ["25.7"] },
    { "id": 156, "tasks": ["25.8", "25.10"] },
    { "id": 157, "tasks": ["25.9"] },
    { "id": 158, "tasks": ["26.1", "26.2", "26.3", "26.4", "26.7"] },
    { "id": 159, "tasks": ["26.5", "26.6"] }
  ]
}
```


# Consolidação de Produto — Implementação

## Ordem oficial do produto
- [ ] Domínio determinístico completo
- [ ] Persistência e versionamento
- [ ] Documentos originais + processamento + evidências
- [ ] Análise manual ponta a ponta
- [ ] Reanálise e comparação V1×VN
- [ ] API
- [ ] Frontend React em português
- [ ] Conector CAIXA
- [ ] Radar automático
- [ ] Checklists parametrizáveis/versionados
- [ ] Auditoria + Golden Cases + regressão

## Critério de passagem para Radar
O fluxo manual deve estar funcional antes do Radar automático. O Radar somente descobre candidatos; a decisão deve ocorrer no motor compartilhado.

## Critério de aceite do MVP
Criar imóvel → cadastrar oportunidade CAIXA → anexar edital/matrícula → complementar evidências → executar análise → visualizar decisão/TCO/valuation/riscos/pendências → adicionar evidência → reanalisar → comparar versões.
