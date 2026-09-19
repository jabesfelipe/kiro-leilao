# PR Review — Evolução da Spec para Produto Completo do Radar Imobiliário

## Objetivo

Evoluir o Radar Imobiliário de um motor de regras/análise para um produto completo, mantendo a especificação como fonte única de verdade e separando descoberta, evidência, análise determinística e decisão.

## Escopo do MVP

O MVP é exclusivamente **leilão extrajudicial de imóveis**, inicialmente da CAIXA.

Fora do MVP:
- venda direta;
- leilão judicial;
- execução judicial;
- arrematação judicial;
- execução automática de lance.

A arquitetura deve permanecer extensível para futuras modalidades e fontes.

## Duas portas de entrada

### 1. Análise manual

Fluxo:

```
Usuário → Imóvel/Oportunidade → Documentos → Evidências → Análise → Decisão
```

O usuário pode cadastrar a oportunidade, enviar edital, matrícula, IPTU, condomínio, processos e outras evidências, executar a análise e posteriormente complementar informações.

### 2. Radar automático

Fluxo:

```
CAIXA → Captura → Normalização → Identificação → Deduplicação
→ Filtros → Checklist → Candidato → Analisar
```

O Radar é uma camada de descoberta. Ele não possui um segundo motor de decisão.

As duas entradas convergem para o mesmo motor determinístico de análise.

## Modelo conceitual

```
IMÓVEL
 ├── OPORTUNIDADE
 │    ├── CAPTURA 1
 │    ├── CAPTURA 2
 │    └── CAPTURA N
 ├── DOCUMENTOS
 ├── EVIDÊNCIAS
 └── ANÁLISES
      ├── V1
      ├── V2
      └── VN
```

Uma nova captura não cria automaticamente um novo imóvel.

## Source Connector

A aquisição deve ser abstraída por um contrato de fonte.

Primeira implementação:
- CAIXA.

Futuras:
- Banco do Brasil;
- Santander;
- Itaú;
- outras fontes.

A estratégia de aquisição pode ser página, endpoint, arquivo, API ou crawler, desde que permaneça desacoplada do domínio.

## Preservação da captura

Toda captura automática deve preservar:
- payload bruto;
- fonte/URL;
- data e hora;
- hash;
- documentos;
- edital;
- anexos;
- imagens quando aplicável;
- versão da captura.

Isso permite responder: **“O que a fonte informou quando esta oportunidade foi capturada?”**

## Documentos como entidades de primeira classe

O arquivo original é permanente e nunca deve ser substituído pela extração.

Metadados:
- tipo;
- nome original;
- extensão;
- MIME;
- tamanho;
- hash;
- origem;
- data/hora;
- usuário;
- imóvel;
- oportunidade;
- análise;
- versão;
- texto extraído;
- páginas;
- chunks;
- embeddings quando aplicável.

Tipos iniciais:
`MATRICULA`, `EDITAL`, `IPTU`, `CONDOMINIO`, `PROCESSO_JUDICIAL`, `LAUDO`, `FOTOS`, `ORCAMENTO_REFORMA`, `OUTRO`.

## Versionamento

Documentos possuem versões.

Análises são snapshots imutáveis.

Cada execução registra:
- versão da análise;
- data/hora;
- evidências consideradas;
- parâmetros;
- checklist;
- resultados;
- decisão;
- justificativa.

Uma nova evidência material gera nova análise.

A interface deve permitir comparar V1 × V2, identificando:
- nova evidência;
- valor alterado;
- risco alterado;
- pendência resolvida;
- decisão alterada;
- motivo da alteração.

## Evidências manuais

Entrada manual é evidência explícita com:
- tipo;
- conteúdo;
- origem;
- data;
- autor;
- confiança;
- validade;
- referência;
- observação.

Origem `USER` não recebe automaticamente a mesma confiança de fonte oficial.

## Processos judiciais e débitos

O MVP não depende de integração automática com Jusbrasil.

Processos podem ser importados manualmente por:
- PDF;
- captura;
- número do processo;
- decisão;
- andamento;
- observação.

Débitos possuem modelo explícito e alimentam o TCO:
- IPTU;
- condomínio;
- demais encargos futuros.

Cada débito deve registrar valor, período, fonte, data da consulta, documento e status.

## Fast Radar × Deep Analysis

### Fast Radar

```
Captura
 → Normalização
 → Identificação
 → Deduplicação
 → Filtros
 → Checklist
 → Candidato
```

Pode avaliar rapidamente:
- localização;
- preço;
- rodada;
- desconto;
- tipo;
- área;
- quartos;
- ticket;
- disponibilidade de dados.

### Deep Analysis

```
Documentos
 → Evidências
 → Jurídico
 → Valuation
 → Comparáveis
 → TCO
 → Reforma
 → Desocupação
 → Liquidez
 → Risco
 → Yield
 → Estratégia
 → Score
 → Decisão
```

A análise profunda não deve ser executada indiscriminadamente para toda oportunidade capturada.

## Checklist parametrizável

Checklist é configuração, não regra hardcoded.

Deve suportar:
- banco;
- estado;
- cidade;
- tipo de imóvel;
- estratégia;
- oportunidade.

Cada checklist possui:
- versão;
- regras;
- filtros;
- pesos;
- severidade;
- ordem;
- condição;
- ação.

Cada execução registra o checklist e sua versão.

## Frontend React

React é o frontend oficial.

A interface deve ser 100% em português.

Mínimo:
- Dashboard;
- Nova Análise;
- pesquisa de imóveis;
- Radar;
- análise detalhada;
- documentos;
- evidências;
- pendências;
- reanálise;
- comparação de versões;
- checklists;
- parâmetros;
- download de documentos.

A tela de análise deve mostrar:
- decisão;
- justificativa;
- confiança;
- Opportunity Score;
- Investor Fit Score;
- preço;
- valor de mercado;
- TCO;
- desconto líquido;
- margem;
- preço máximo;
- preço-alvo;
- break-even;
- aluguel;
- yield bruto;
- yield líquido;
- liquidez;
- riscos;
- pendências;
- evidências.

## Viabilidade financeira

A planilha de viabilidade passa a ser uma visão financeira oficial do produto.

TCO:

```
aquisição
+ comissão
+ ITBI
+ registro
+ débitos
+ reforma
+ desocupação
+ regularização
+ contingências
+ custos financeiros
```

Cada componente deve ser decomponível e rastreável à evidência que o originou.

Os motores determinísticos calculam:
- TCO;
- valor de mercado;
- margem;
- desconto líquido;
- preço máximo;
- preço-alvo;
- break-even;
- yield;
- ROI;
- prazo;
- liquidez.

## IA, RAG, LangGraph, Agents e MCP

Arquitetura conceitual:

```
React
 ↓
API
 ↓
Orquestrador
 ↓
LangGraph
 ↓
RAG / Agents / MCP
 ↓
Extração e interpretação
 ↓
Evidências estruturadas
 ↓
Motores determinísticos
 ↓
Decisão
```

Responsabilidades:

**LLM/Agents**
- interpretar documentos;
- extrair informações;
- classificar trechos;
- localizar evidências;
- resumir;
- sugerir pendências;
- orquestrar etapas.

**RAG**
- recuperar conhecimento;
- recuperar documentos e trechos relevantes;
- fornecer contexto.

**Motores determinísticos**
- TCO;
- valuation final;
- preço máximo;
- score;
- yield;
- margem;
- regras jurídicas;
- decisão.

RAG não é a verdade transacional.

LLM/Agent não pode transformar `UNKNOWN` em `CONFIRMED` sem nova evidência.

## Princípios de segurança do domínio

- Desconto nunca compensa invalidade jurídica.
- Score nunca supera `BLOCK`.
- Ausência de evidência significa `UNKNOWN/PENDING`.
- Custo desconhecido nunca é zero.
- Risco desconhecido nunca é zero.
- Contradições devem ser preservadas.
- Evidência histórica é contexto, não prova atual.
- Avaliação CAIXA é informacional, não automaticamente valor de mercado.
- Ocupação representa risco de posse/econômico e não é automaticamente invalidade.
- Existência de processo judicial não é automaticamente `BLOCK`.
- Yield bruto não é yield líquido.
- Toda conclusão deve possuir proveniência.

## Auditoria

Toda alteração manual registra:
- quem;
- quando;
- valor anterior;
- novo valor;
- motivo.

Capturas automáticas são imutáveis.

Evidências possuem proveniência.

Análises são versionadas.

Regras, checklists e parâmetros são versionados.

## Arquitetura de documentação

Estrutura recomendada:

```
architecture/
  backend/
    README.md
    architecture.md
    components.md
    data-flow.md
    api.md
    persistence.md
    ai.md
    rag.md
    langgraph.md
    agents.md
    mcp.md
    document-processing.md
    source-connectors.md
    radar.md
    security.md
    observability.md
```

Esses documentos são derivados da spec e não substituem a fonte normativa.

## Ordem de implementação

1. Domínio determinístico.
2. Persistência.
3. Documentos e evidências.
4. Análise manual ponta a ponta.
5. Reanálise e versionamento.
6. API.
7. Frontend.
8. Conector CAIXA.
9. Radar automático.
10. Checklists parametrizáveis.
11. Auditoria e Golden Cases.

**Não começar pelo crawler.**

## Prova de fogo do MVP

O sistema precisa permitir:

1. criar imóvel;
2. cadastrar oportunidade CAIXA;
3. enviar edital;
4. enviar matrícula;
5. informar IPTU;
6. informar condomínio;
7. adicionar processos;
8. executar análise;
9. visualizar decisão;
10. visualizar TCO;
11. visualizar valuation;
12. visualizar riscos;
13. visualizar pendências;
14. baixar documentos;
15. adicionar nova evidência;
16. reanalisar;
17. comparar V1 × V2;
18. revisitar o imóvel posteriormente.

Depois:

```
Radar CAIXA
 → Captura
 → Checklist
 → Candidato
 → ANALISAR
 → mesmo motor de análise
```

## Critério de sucesso

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

com:
- rastreabilidade;
- versionamento;
- explicabilidade;
- auditoria;
- reprodutibilidade;
- preservação de desconhecidos;
- histórico completo.

## Decisões adicionadas

- D56 — MVP exclusivamente leilão extrajudicial.
- D57 — duas entradas: análise manual e Radar automático.
- D58 — CAIXA é o primeiro Source Connector.
- D59 — Connector desacoplado da estratégia de captura.
- D60 — documento original preservado.
- D61 — documento versionado.
- D62 — análise é snapshot imutável.
- D63 — reanálise cria nova versão.
- D64 — entrada manual é evidência com proveniência.
- D65 — processo judicial pode ser importado manualmente.
- D66 — débitos podem ser informados manualmente.
- D67 — checklist parametrizável e versionado.
- D68 — checklist suporta banco/localização/estratégia.
- D69 — Fast Radar separado de Deep Analysis.
- D70 — React é frontend oficial.
- D71 — interface em português.
- D72 — novos componentes de código e banco em português.
- D73 — arquitetura backend documentada separadamente.
- D74 — RAG é recuperação, não verdade transacional.
- D75 — LLM/Agent não substitui motor determinístico.
- D76 — captura preserva payload bruto.
- D77 — resultado financeiro reproduz a planilha de viabilidade.
- D78 — documentos capturados são baixáveis.
- D79 — histórico de análises é navegável/comparável.
- D80 — Radar e análise manual convergem para o mesmo motor.

## Diretriz final

**Primeiro fechar a spec. Depois implementar.**

O primeiro grande marco funcional é a análise manual real de um imóvel CAIXA, do upload dos documentos até a decisão apresentada no frontend, incluindo complementação de evidências e reanálise. Somente depois o Radar automático deve ser priorizado.
