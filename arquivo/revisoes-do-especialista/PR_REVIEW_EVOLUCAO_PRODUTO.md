# PR Review — Fechamento Final da Especificação para Implementação Completa

## Objetivo

Esta revisão consolida o fechamento arquitetural do Radar Imobiliário antes do início da implementação completa.

A especificação deve permanecer como **fonte única de verdade**. O objetivo agora não é reduzir escopo, criar um MVP técnico simplificado ou deixar decisões importantes para depois. O objetivo é fechar os contratos arquiteturais, funcionais e operacionais necessários para que o Kiro possa implementar o produto inteiro de forma coerente.

Princípio central:

> **A IA interpreta. A evidência sustenta. O domínio calcula. O motor decide. A interface explica.**

---

## 1. Escopo de implementação

A implementação deve contemplar o produto completo definido na spec:

- backend;
- persistência;
- domínio determinístico;
- análise manual;
- Radar automático;
- captura e conectores de fontes;
- documentos;
- OCR/extracão;
- evidências;
- RAG;
- LLM;
- LangChain;
- LangGraph;
- Agents;
- MCP;
- checklists;
- reanálise;
- versionamento;
- auditoria;
- observabilidade;
- frontend React;
- UX desktop e mobile;
- notificações e monitoramento;
- testes;
- segurança;
- arquitetura preparada para SaaS futuro.

Não criar uma implementação artificialmente reduzida que invalide a arquitetura final.

A implementação deve, entretanto, respeitar a ordem de dependências técnicas para evitar retrabalho.

---

## 2. Produto e fluxo principal

O produto deve fechar o ciclo:

```
DESCOBRIR
 → SELECIONAR
 → DOCUMENTAR
 → ANALISAR
 → COMPLEMENTAR
 → REANALISAR
 → COMPARAR
 → DECIDIR
```

Duas portas de entrada:

### Análise manual

```
Usuário
 → Imóvel/Oportunidade
 → Documentos
 → Evidências
 → Análise
 → Decisão
```

### Radar automático

```
Fonte
 → Captura
 → Normalização
 → Identificação
 → Deduplicação
 → Filtros
 → Checklist
 → Candidato
 → Análise profunda quando aplicável
```

As duas entradas devem convergir para o mesmo domínio e para o mesmo motor determinístico de análise/decisão.

O Radar é **descoberta**, não um segundo motor de decisão.

---

## 3. Arquitetura geral

Arquitetura de referência:

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND REACT                   │
│ Dashboard · Radar · Imóveis · Análises · Docs      │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│                         API                         │
│ Auth · CRUD · Análise · Radar · Documentos          │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│                    APPLICATION                      │
│ Use Cases · Orquestração · Jobs · Eventos          │
└───────────────┬──────────────────────┬──────────────┘
                │                      │
                ▼                      ▼
┌────────────────────────┐  ┌─────────────────────────┐
│      DOMÍNIO           │  │      IA / ORQUESTRAÇÃO  │
│ Regras · TCO · Jurídico│  │ LangGraph · RAG · Agent │
│ Valuation · Decisão    │  │ LLM · MCP               │
└────────────┬───────────┘  └────────────┬────────────┘
             │                           │
             └──────────────┬────────────┘
                            ▼
┌─────────────────────────────────────────────────────┐
│                   PERSISTÊNCIA                      │
│ PostgreSQL · documentos · vetores · auditoria      │
└─────────────────────────────────────────────────────┘
```

A IA não deve possuir autoridade para substituir as regras determinísticas do domínio.

---

## 4. Domínio determinístico

O domínio é a camada de maior autoridade para resultados de negócio.

Devem permanecer determinísticos:

- TCO;
- valuation final;
- preço máximo;
- preço-alvo;
- break-even;
- margem;
- desconto líquido;
- yield bruto;
- yield líquido;
- ROI;
- liquidez;
- score;
- Investor Fit;
- regras jurídicas;
- gates;
- hard stops;
- decisão final.

A LLM pode interpretar, estruturar, localizar evidências e sugerir ações, mas não pode alterar arbitrariamente um resultado determinístico.

---

## 5. Radar automático

O Radar deve ser robusto o suficiente para execução recorrente.

Fluxo:

```
EXECUÇÃO RADAR
 → carregar conectores ativos
 → capturar fonte
 → preservar captura bruta
 → validar captura
 → normalizar
 → identificar imóvel/oportunidade
 → deduplicar
 → enriquecer quando necessário
 → aplicar filtros
 → aplicar checklist
 → gerar candidatos
 → priorizar enriquecimento/análise
```

A execução deve ser idempotente e auditável.

Cada execução deve possuir:

- id;
- início;
- término;
- fonte;
- conector;
- estratégia;
- versão;
- quantidade capturada;
- quantidade nova;
- quantidade atualizada;
- quantidade descartada;
- quantidade candidata;
- erros;
- alertas;
- status.

---

## 6. Framework de aquisição

A aquisição deve ser abstraída em dois níveis:

```
Radar Engine
    │
    ├── Source Connector
    │
    └── Capture Strategy
         ├── WEB
         ├── API
         ├── FILE
         └── CRAWLER
```

Exemplo:

- CaixaConnector;
- BancoDoBrasilConnector;
- SantanderConnector;
- ItauConnector.

O domínio nunca deve possuir `if caixa`, `if banco_do_brasil` ou regras semelhantes espalhadas pelo código.

O conector conhece a fonte.

A estratégia conhece como capturar.

O domínio conhece imóveis e oportunidades.

---

## 7. Crawling e resiliência

O crawler deve suportar:

- timeout;
- retry com backoff;
- rate limiting;
- paginação;
- checkpoint;
- retomada;
- falha parcial;
- captura incremental;
- alteração de HTML;
- alteração de endpoint;
- resposta vazia;
- resposta inválida;
- conteúdo duplicado;
- indisponibilidade temporária;
- circuit breaker quando aplicável.

O crawler não deve depender de seletores frágeis sem validação.

Toda captura deve validar:

- estrutura esperada;
- quantidade mínima plausível;
- presença de campos essenciais;
- hash;
- timestamp;
- fonte.

Uma mudança inesperada da fonte deve produzir erro observável, não corromper silenciosamente o domínio.

---

## 8. Captura incremental

O Radar não deve baixar e reprocessar indiscriminadamente tudo a cada execução.

Suportar:

- hash de payload;
- hash de documento;
- identificador externo;
- URL canônica;
- matrícula;
- chave composta de oportunidade;
- data de atualização da fonte.

A captura deve distinguir:

- NOVA;
- ATUALIZADA;
- SEM_ALTERACAO;
- REMOVIDA_DA_FONTE;
- INVALIDA;
- INCONCLUSIVA.

Remoção da fonte não deve apagar o histórico interno.

---

## 9. Idempotência

Operações críticas devem ser idempotentes.

Exemplos:

- captura;
- importação de documento;
- criação de oportunidade a partir de fonte;
- indexação vetorial;
- execução de análise;
- processamento de evento;
- geração de candidato.

Utilizar constraints, hashes e chaves naturais quando aplicável.

Retry nunca deve produzir duplicação silenciosa.

---

## 10. Agendamento

O Radar deve possuir modelo de execução agendada, mesmo que inicialmente executado localmente.

Configurações:

- frequência;
- fonte;
- janela;
- horário;
- ativo/inativo;
- estratégia;
- checklist;
- filtros;
- limite de páginas;
- limite de itens;
- política de retry.

A arquitetura deve permitir posteriormente:

- cron local;
- scheduler cloud;
- EventBridge;
- worker assíncrono.

Não acoplar o domínio ao mecanismo de agendamento.

---

## 11. Multi-banco / multi-fonte

A arquitetura deve permitir adicionar novas fontes sem reescrever o domínio.

Contrato mínimo de um conector:

```
SourceConnector
 ├── identificar_fonte
 ├── validar_configuracao
 ├── capturar
 ├── listar_oportunidades
 ├── obter_detalhes
 ├── obter_documentos
 ├── normalizar
 └── informar_capacidades
```

Cada fonte pode possuir capacidades diferentes.

O sistema deve registrar essas capacidades em vez de assumir que todas as fontes possuem os mesmos dados.

---

## 12. Multi-tenant readiness

Mesmo que a primeira versão seja single-user/local, entidades sensíveis devem possuir estrutura que não impeça SaaS futuro.

Considerar:

- `tenant_id`;
- `user_id`;
- ownership;
- permissões;
- auditoria;
- isolamento lógico;
- configuração por tenant.

Não é necessário implementar billing agora, mas não criar modelo que torne multi-tenant inviável.

---

## 13. Perfil do investidor

O perfil do investidor deve ser explícito e versionável.

Exemplos:

- estratégia;
- ticket máximo;
- região;
- tipo de imóvel;
- tolerância a risco;
- objetivo de renda;
- objetivo de revenda;
- prazo;
- necessidade de liquidez;
- limite de financiamento;
- preferência de ocupação/desocupação.

Investor Fit deve ser calculado deterministicamente a partir do perfil versionado.

O perfil não pode ultrapassar hard stops jurídicos.

---

## 14. LLM Provider

Criar abstração de provedor:

```
LLMProvider
EmbeddingProvider
```

Primeira implementação pode utilizar OpenAI.

A arquitetura deve permitir futuramente:

- Anthropic;
- Gemini;
- AWS Bedrock;
- modelos locais;
- outros provedores.

Não espalhar chamadas diretas ao SDK do provedor pelo domínio.

---

## 15. ChatGPT Plus × API

A implementação deve considerar explicitamente:

- ChatGPT Plus é o produto de uso do ChatGPT;
- OpenAI API possui faturamento separado;
- assinatura Plus não deve ser tratada como crédito automático para chamadas da API.

O backend deve usar uma credencial de API própria, com configuração por ambiente.

Exemplo conceitual:

```
OPENAI_API_KEY
OPENAI_MODEL
OPENAI_EMBEDDING_MODEL
```

Nunca versionar secrets.

---

## 16. Controle de custo da IA

A arquitetura deve possuir mecanismos para evitar custo desnecessário:

- cache de respostas quando semanticamente seguro;
- cache de embeddings;
- deduplicação de documentos;
- chunking controlado;
- limite de tokens;
- modelos diferentes por tarefa;
- processamento assíncrono;
- reprocessamento somente quando necessário;
- budget por execução;
- métricas de tokens;
- métricas de custo;
- versionamento de prompts.

Uma mudança de prompt/modelo deve permitir identificar qual versão produziu uma interpretação.

---

## 17. LangChain

LangChain deve ser usado como infraestrutura de integração/orquestração de componentes de IA, não como substituto do domínio.

Responsabilidades possíveis:

- loaders;
- splitters;
- embeddings;
- retrievers;
- structured output;
- tools;
- integrações com LLM.

O domínio não deve depender diretamente de objetos específicos de LangChain quando um contrato próprio for suficiente.

---

## 18. LangGraph

LangGraph deve representar workflows de IA com estado explícito.

Exemplo:

```
START
 ↓
CARREGAR_DOCUMENTOS
 ↓
EXTRAIR_TEXTO
 ↓
CLASSIFICAR_DOCUMENTOS
 ↓
EXTRAIR_EVIDENCIAS
 ↓
VALIDAR_EVIDENCIAS
 ↓
RECUPERAR_CONTEXTO_RAG
 ↓
ANALISAR_PENDENCIAS
 ↓
GERAR_PROPOSTA_DE_ANALISE
 ↓
VALIDAR_CONTRA_DOMINIO
 ↓
EXECUTAR_MOTOR_DETERMINISTICO
 ↓
GERAR_EXPLICACAO
 ↓
END
```

O estado deve registrar:

- correlation id;
- analysis id;
- execution id;
- versões;
- documentos;
- evidências;
- mensagens;
- erros;
- checkpoints;
- resultado intermediário;
- status.

---

## 19. Resiliência do LangGraph

O workflow deve suportar:

- retry por nó;
- timeout;
- checkpoint;
- resume;
- execução parcial;
- idempotência;
- falha de ferramenta;
- falha do LLM;
- fallback;
- human-in-the-loop.

Uma falha no nó de RAG não deve necessariamente invalidar todo o processo se a etapa puder ser retomada.

---

## 20. Human-in-the-loop

Deve existir possibilidade de intervenção humana quando:

- documento possui baixa qualidade;
- evidência é ambígua;
- há conflito entre fontes;
- processo judicial exige interpretação;
- extração possui baixa confiança;
- LLM não consegue estruturar o dado;
- regra de negócio exige confirmação.

O usuário deve conseguir:

- aceitar;
- corrigir;
- rejeitar;
- adicionar evidência;
- marcar pendência;
- solicitar reanálise.

Toda intervenção deve gerar auditoria.

---

## 21. Agents

Agents devem ser **bounded agents**, com escopo e ferramentas explícitos.

Exemplos:

### Agente documental
Extrai e localiza evidências.

### Agente jurídico
Organiza informações jurídicas e aponta lacunas, sem declarar regularidade sem evidência suficiente.

### Agente de mercado
Busca e organiza comparáveis.

### Agente de diligência
Identifica pendências.

### Agente de análise
Orquestra chamadas aos demais componentes.

Nenhum agente possui autoridade para ignorar hard stops.

---

## 22. MCP

MCP deve ser tratado como camada de ferramentas/contexto, não como autoridade de decisão.

Separar:

### Read tools
- consultar documento;
- buscar evidência;
- consultar imóvel;
- consultar processo;
- consultar comparáveis;
- consultar parâmetros.

### Write tools
- criar evidência;
- atualizar análise;
- registrar revisão;
- criar pendência;
- disparar reanálise.

Operações de escrita devem exigir:

- autorização;
- validação;
- auditoria;
- idempotência.

---

## 23. RAG

RAG deve possuir pipeline explícito:

```
Documento
 → extração
 → limpeza
 → chunking
 → metadata
 → embedding
 → vector store
 → retrieval
 → reranking quando aplicável
 → contexto
 → LLM
```

Metadata mínima:

- documento;
- versão;
- imóvel;
- oportunidade;
- página;
- trecho;
- tipo;
- data;
- origem;
- hash;
- versão do embedding;
- versão do chunking.

---

## 24. Citações e proveniência do RAG

Toda resposta de IA que dependa de documento deve poder apontar:

- documento;
- versão;
- página;
- trecho;
- evidência;
- origem.

A interface deve permitir abrir a evidência original.

O sistema deve distinguir:

```
FATO DO DOCUMENTO
INTERPRETAÇÃO DA IA
RESULTADO DETERMINÍSTICO
```

Não apresentar interpretação da IA como se fosse fato documental.

---

## 25. Vector Store separado da verdade transacional

O vector store não é fonte de verdade do domínio.

A verdade transacional permanece em persistência relacional/documental apropriada.

O vector store pode ser reconstruído.

Deve existir possibilidade de:

- reindexar;
- trocar provider;
- trocar modelo;
- alterar chunking;
- invalidar embeddings;
- executar migração.

---

## 26. Knowledge Base

Separar claramente:

### Conhecimento do domínio
- regras;
- conceitos;
- legislação/configuração;
- critérios;
- procedimentos.

### Dados do imóvel
- matrícula;
- edital;
- IPTU;
- condomínio;
- processos;
- fotos;
- laudos.

### Histórico
- análises anteriores;
- decisões;
- alterações;
- capturas.

Cada categoria deve possuir política de atualização e validade temporal própria.

---

## 27. Contexto temporal

A arquitetura deve ser temporalmente consciente.

Exemplos:

- edital da data X;
- matrícula emitida em Y;
- débito consultado em Z;
- preço capturado em T;
- comparável observado em determinada data.

Não utilizar automaticamente uma evidência antiga como se fosse atual.

Uma análise deve registrar a data de corte das informações utilizadas.

---

## 28. Document processing

Pipeline:

```
UPLOAD
 ↓
VALIDAÇÃO
 ↓
HASH
 ↓
ARMAZENAMENTO ORIGINAL
 ↓
OCR/EXTRAÇÃO
 ↓
NORMALIZAÇÃO
 ↓
CLASSIFICAÇÃO
 ↓
CHUNKING
 ↓
INDEXAÇÃO
 ↓
EXTRAÇÃO DE EVIDÊNCIAS
 ↓
VALIDAÇÃO
```

O arquivo original nunca é substituído.

Falhas de OCR/extracão devem ser explícitas.

---

## 29. Segurança

Implementar desde o início:

- gestão segura de secrets;
- autenticação;
- autorização;
- ownership;
- validação de upload;
- limite de tamanho;
- tipos MIME;
- sanitização;
- proteção contra path traversal;
- logs sem secrets;
- criptografia quando aplicável;
- controle de acesso aos documentos;
- auditoria.

Nunca enviar documento sensível para LLM sem política explícita de processamento.

---

## 30. Observabilidade

Toda execução importante deve possuir:

- correlation id;
- trace id;
- execution id;
- logs estruturados;
- métricas;
- duração;
- status;
- erro;
- retries;
- custo de IA;
- tokens;
- fonte;
- versão.

Monitorar especialmente:

- captura;
- crawler;
- documentos;
- OCR;
- embeddings;
- RAG;
- LangGraph;
- Agents;
- MCP;
- análise;
- notificações.

---

## 31. Auditoria

Registrar:

- quem;
- quando;
- o quê;
- valor anterior;
- valor novo;
- motivo;
- origem;
- versão.

Eventos automáticos devem ser distinguíveis de alterações manuais.

Análises e capturas devem possuir histórico imutável.

---

## 32. Notificações

Arquitetar eventos para suportar posteriormente:

- nova oportunidade;
- oportunidade atualizada;
- preço alterado;
- documento novo;
- pendência resolvida;
- risco alterado;
- decisão alterada;
- oportunidade removida da fonte;
- execução do Radar concluída;
- erro de captura.

Primeiramente pode existir notificação local/in-app, mas o contrato deve permitir email, WhatsApp, push ou outros canais futuramente.

---

## 33. Watch / monitoramento de oportunidades

Uma oportunidade pode ser marcada para acompanhamento.

O sistema deve permitir:

- acompanhar preço;
- acompanhar rodada;
- acompanhar disponibilidade;
- acompanhar documentos;
- acompanhar riscos;
- acompanhar processos;
- acompanhar mudança de decisão.

Alteração relevante deve gerar evento e permitir reanálise.

---

## 34. Backtest temporalmente seguro

Qualquer backtest deve utilizar apenas informações disponíveis na data simulada.

Não permitir:

- usar preço futuro;
- usar documento posterior;
- usar comparável conhecido somente depois;
- usar resultado da própria operação para prever a decisão.

Registrar:

- data de corte;
- versão do motor;
- versão das regras;
- fontes disponíveis;
- dados utilizados.

---

## 35. API

A API deve ser versionável e consistente.

Contratos conceituais:

```
POST/GET /imoveis
GET      /imoveis/{id}

POST/GET /oportunidades
GET      /oportunidades/{id}

POST/GET /documentos
GET      /documentos/{id}
GET      /documentos/{id}/download

POST/GET /analises
GET      /analises/{id}
POST     /analises/{id}/reanalisar
GET      /analises/{id}/comparar/{versao}

POST/GET /evidencias

GET      /radar/oportunidades
POST     /radar/executar

GET/POST /checklists
PUT      /checklists/{id}
POST     /checklists/{id}/versionar

GET/PUT  /configuracoes
```

Contratos reais devem definir:

- request;
- response;
- erros;
- paginação;
- filtros;
- ordenação;
- idempotency key quando necessário;
- versionamento;
- autorização.

---

## 36. Catálogo de erros

Não retornar mensagens técnicas diretamente ao usuário.

Categorias:

- VALIDATION_ERROR;
- NOT_FOUND;
- CONFLICT;
- UNAUTHORIZED;
- FORBIDDEN;
- DOCUMENT_INVALID;
- DOCUMENT_PROCESSING_ERROR;
- SOURCE_UNAVAILABLE;
- SOURCE_CHANGED;
- RADAR_EXECUTION_ERROR;
- AI_PROVIDER_ERROR;
- AI_TIMEOUT;
- RAG_ERROR;
- ANALYSIS_ERROR;
- BUSINESS_RULE_ERROR.

Cada erro deve possuir:

- código;
- mensagem amigável;
- contexto;
- correlation id;
- detalhes seguros.

---

## 37. Performance

Evitar processamento síncrono pesado no request HTTP.

Processamentos candidatos a assíncronos:

- OCR;
- embeddings;
- RAG;
- análise profunda;
- crawler;
- download de grandes documentos;
- reanálise;
- indexação.

A interface deve mostrar progresso/status.

---

## 38. Frontend — estados obrigatórios

Toda tela relevante deve possuir:

- loading;
- skeleton quando apropriado;
- empty state;
- error state;
- retry;
- partial state;
- stale data indicator;
- confirmation;
- success feedback.

Nunca deixar tela vazia sem explicar o estado.

---

## 39. Frontend — navegação

Estrutura sugerida:

```
Dashboard
 ├── Radar
 ├── Imóveis
 ├── Oportunidades
 ├── Análises
 ├── Pendências
 ├── Documentos
 ├── Monitoramento
 └── Configurações
```

A jornada principal deve exigir poucos passos para chegar de oportunidade até análise.

---

## 40. UX de análise

A tela de análise deve começar pelo que importa:

1. decisão;
2. justificativa;
3. bloqueios;
4. pendências;
5. indicadores financeiros;
6. riscos;
7. evidências;
8. detalhes técnicos.

A interface deve deixar claro:

- o que é fato;
- o que é inferência;
- o que é cálculo;
- o que está pendente.

---

## 41. UX mobile

O produto deve ser responsivo desde o início.

No mobile:

- cards;
- accordions;
- sticky decision summary;
- filtros em drawer;
- documentos em lista;
- evidências em navegação simplificada;
- ações principais acessíveis com uma mão.

Tabelas complexas devem possuir representação responsiva.

Upload de documentos deve funcionar em mobile.

---

## 42. Design system

Criar design system consistente para:

- cores semânticas;
- tipografia;
- espaçamento;
- cards;
- badges;
- status;
- tabelas;
- formulários;
- dialogs;
- alerts;
- gráficos;
- skeletons.

Cores de decisão devem ser semânticas, não apenas decorativas.

---

## 43. Acessibilidade

Implementar:

- navegação por teclado;
- labels;
- foco visível;
- contraste;
- textos alternativos;
- aria quando necessário;
- mensagens de erro associadas ao campo;
- não depender somente de cor para comunicar estado.

---

## 44. Comercialização futura

Preparar abstrações para futuro SaaS:

- tenant;
- usuário;
- plano;
- limites;
- consumo de IA;
- armazenamento;
- auditoria;
- billing;
- feature flags.

Não implementar billing agora se não for necessário, mas evitar acoplamento que impeça sua inclusão.

---

## 45. Configuração por ambiente

Separar:

- desenvolvimento;
- teste;
- produção.

Configurações devem incluir:

- banco;
- storage;
- LLM;
- embeddings;
- vector store;
- crawler;
- scheduler;
- notificações;
- limites;
- feature flags.

Nunca hardcode credentials ou URLs sensíveis.

---

## 46. Testes

Cobertura deve incluir:

### Domínio
- unitários;
- property-based quando aplicável;
- golden cases.

### Integração
- banco;
- documentos;
- storage;
- vector store;
- conectores.

### API
- contratos;
- autorização;
- erros.

### Radar
- captura;
- deduplicação;
- incremental;
- idempotência;
- falhas.

### Frontend
- componentes;
- fluxos críticos;
- estados.

---

## 47. Testes de IA

Criar avaliação específica para IA:

- extração correta;
- citação correta;
- não alucinação;
- preservação de UNKNOWN;
- consistência de structured output;
- recuperação RAG;
- classificação;
- regressão de prompts;
- regressão de modelos.

Golden cases devem conter documentos reais/sintéticos representativos e resultados esperados.

---

## 48. Anti-hallucination

Regras obrigatórias:

- não inventar evidência;
- não inventar valor;
- não inventar número de processo;
- não inventar cláusula;
- não inventar data;
- não converter ausência em confirmação;
- não omitir contradição relevante.

Quando não houver evidência:

```
UNKNOWN / PENDING
```

e não uma resposta afirmativa.

---

## 49. Motor final de decisão

A decisão deve seguir os gates e hard stops já definidos na spec.

Regra fundamental:

```
BLOCK jurídico
    > score
    > desconto
    > yield
    > margem
    > preferência do investidor
```

Nenhum indicador financeiro pode superar bloqueio jurídico.

Nenhum agente pode alterar essa precedência.

---

## 50. Explainability

Toda decisão deve responder:

- quais evidências foram usadas;
- quais regras foram aplicadas;
- quais cálculos foram executados;
- quais pendências permaneceram;
- quais riscos influenciaram;
- qual versão do motor foi utilizada;
- qual versão do checklist;
- qual versão dos documentos;
- qual versão do modelo/prompt quando IA participou.

---

## 51. Reprodutibilidade

Uma análise deve poder ser reproduzida com:

- documentos;
- evidências;
- parâmetros;
- checklist;
- versão do domínio;
- versão do motor;
- versão do prompt;
- versão do modelo;
- versão do embedding;
- data de corte.

A reprodução histórica não deve depender do estado atual mutável.

---

## 52. Versionamento do engine

Registrar versão do motor determinístico.

Exemplo:

```
ENGINE_VERSION = 1.0.0
```

Mudanças de regra que alterem decisão devem gerar nova versão.

O histórico deve continuar interpretável.

---

## 53. Domain events

Considerar eventos internos como:

- ImovelCriado;
- OportunidadeCapturada;
- DocumentoAdicionado;
- DocumentoProcessado;
- EvidenciaCriada;
- AnaliseExecutada;
- AnaliseReanalisada;
- RiscoAlterado;
- DecisaoAlterada;
- RadarExecutado;
- CandidatoCriado.

Eventos não devem criar acoplamento excessivo. Usar somente onde houver benefício real.

---

## 54. Local-first

A primeira execução deve ser possível localmente e com baixo/no custo de infraestrutura.

A arquitetura deve permitir evolução posterior para cloud.

Separar:

```
CORE
 ↕
ADAPTERS
 ↕
INFRA
```

Exemplos de adapters:

- storage local / S3;
- PostgreSQL local / RDS;
- scheduler local / EventBridge;
- LLM API / Bedrock / local model.

---

## 55. IA local × API

A abstração de provider deve permitir decidir por tarefa.

Exemplo:

- OCR local;
- embeddings API;
- LLM API;
- modelo local para classificação barata;
- modelo maior para análise complexa.

Não assumir que toda tarefa deve utilizar o mesmo modelo.

---

## 56. Embedding Provider

Criar:

```
EmbeddingProvider
```

Registrar:

- provider;
- model;
- dimensions;
- version;
- timestamp.

Documentos e chunks devem identificar qual embedding foi utilizado.

---

## 57. Migração de embeddings

A arquitetura deve permitir reindexação sem perda do documento original.

Fluxo:

```
OLD EMBEDDING
 → RE-EMBED
 → VALIDATE
 → NEW INDEX
 → SWITCH
 → RETAIN/REMOVE OLD INDEX
```

Não acoplar o documento à dimensão fixa de um único modelo.

---

## 58. Fechamento arquitetural

Antes de iniciar implementação, validar as seguintes perguntas:

1. O domínio funciona sem LLM?
2. O domínio funciona sem RAG?
3. A decisão final é determinística?
4. UNKNOWN permanece UNKNOWN?
5. BLOCK nunca é superado por score?
6. Toda evidência possui origem?
7. Documentos originais são preservados?
8. Documentos possuem versão?
9. Análises são snapshots?
10. Reanálise gera nova versão?
11. O Radar é somente descoberta?
12. Radar e análise manual usam o mesmo domínio?
13. Capturas são idempotentes?
14. Existe captura incremental?
15. O payload bruto é preservado?
16. Existe connector abstraction?
17. O conector é separado da estratégia de captura?
18. É possível adicionar outro banco sem alterar o domínio?
19. O crawler suporta retry e falha parcial?
20. Existe checkpoint/resume para workflows?
21. LangGraph possui estado explícito?
22. Agents possuem ferramentas limitadas?
23. MCP possui separação read/write?
24. Escritas via MCP são auditáveis?
25. RAG possui metadata suficiente para citação?
26. Vector store pode ser reconstruído?
27. Embeddings possuem versão?
28. Existe controle de custo de IA?
29. LLM provider é abstraído?
30. A API é versionável?
31. Erros são catalogados?
32. A UI possui loading/empty/error states?
33. O mobile está contemplado?
34. A análise mostra evidência e explicação?
35. Existe auditoria?
36. Existe versionamento do engine?
37. Existe data de corte temporal?
38. Backtest evita leakage?
39. Existe observabilidade?
40. O sistema pode evoluir para SaaS?

Se alguma resposta for “não”, a spec ainda não está fechada.

---

## 59. Ordem de implementação

A ordem de implementação deve respeitar dependências:

1. fundação do projeto;
2. domínio determinístico;
3. persistência;
4. documentos e evidências;
5. análise manual ponta a ponta;
6. versionamento e reanálise;
7. API;
8. frontend;
9. IA documental;
10. RAG;
11. LangGraph;
12. Agents/MCP;
13. connector framework;
14. conector CAIXA;
15. Radar automático;
16. checklists parametrizáveis;
17. monitoramento/notificações;
18. observabilidade;
19. hardening;
20. Golden Cases e validação final.

**Não começar pelo crawler.**

O primeiro marco funcional continua sendo a análise manual real de um imóvel CAIXA, mas a arquitetura final deve estar refletida desde o início.

---

## 60. Diretriz final para o Kiro

Atualizar **somente os artefatos normativos já existentes**, especialmente:

- `.kiro/specs/**/requirements.md`;
- `.kiro/specs/**/design.md`;
- `.kiro/specs/**/tasks.md`.

Não criar uma segunda fonte de verdade.

Preservar as decisões já tomadas D1-D89 e consolidar os novos fechamentos desta revisão sem duplicar requisitos ou entidades.

Garantir que:

- requirements expressem comportamento e critérios;
- design expresse arquitetura e contratos;
- tasks expressem implementação e dependências;
- testes reflitam requirements;
- nenhuma decisão importante fique implícita.

Depois da consolidação:

1. validar consistência entre requirements/design/tasks;
2. validar que não existem requisitos contraditórios;
3. validar que não existem entidades duplicadas;
4. validar cobertura de implementação;
5. validar os 40 itens de fechamento;
6. congelar a spec;
7. iniciar implementação.

A partir desse ponto, mudanças de arquitetura devem ser tratadas como mudança explícita de decisão, com impacto documentado.

---

## Princípio arquitetural definitivo

> **A IA interpreta.**
>
> **A evidência sustenta.**
>
> **O domínio calcula.**
>
> **O motor decide.**
>
> **A interface explica.**
