# Radar_Imobiliario_Base_de_Conhecimento_IA_v1.2_COMPLETA

RADAR IMOBILIÁRIO
BASE DE CONHECIMENTO FUNCIONAL E DE DECISÃO PARA IA
Versão 1.0 — consolidação canônica para uso humano e futura indexação em base vetorial/RAG.
Princípios: “Preço é o dado. Oportunidade é a análise.” | “Não procure imóveis baratos. Deixe o Radar encontrar imóveis que estejam realmente baratos.”

# Objetivo

Este documento consolida a lógica funcional do Radar: identificar e consolidar imóveis, estimar mercado, calcular custo econômico, avaliar validade jurídica, risco, liquidez e estratégia, pontuar, ranquear, explicar, conduzir due diligence, decidir e monitorar.
- Fato observado, fato confirmado, cálculo, estimativa, inferência e desconhecido devem ser separados.
- Ausência de informação nunca deve virar zero ou uma suposição silenciosa.
- Score, desconto ou retorno nunca superam um BLOCK jurídico.
- Toda conclusão deve apontar evidências, pendências, impacto e condições.
- Regras, pesos e parâmetros usados em cada decisão devem ser versionados.

# 01 — DEFINIÇÃO DO PRODUTO

O Radar Imobiliário é uma plataforma de inteligência de oportunidades que captura informações imobiliárias, identifica e consolida imóveis, estima valor de mercado, calcula custo econômico, avalia risco e liquidez, aplica estratégias e regras do investidor, ranqueia oportunidades, explica suas conclusões, conduz análise profunda, registra decisões, monitora mudanças e aprende com resultados.

## O que não é

- Não é apenas agregador de anúncios.
- Não é apenas sistema de leilões.
- Não é ranking de imóveis baratos.
- Não é calculadora de desconto.
- Não substitui due diligence jurídica.
Unidade central: a oportunidade economicamente fundamentada e continuamente monitorada, não o anúncio.

# 02 — ONTOLOGIA


| Entidade | Definição |
|---|---|
| Source | Origem da informação. |
| Capture | Snapshot original de uma fonte em um momento. |
| Property | Ativo físico/documental identificado. |
| Opportunity | Tese econômica sobre uma Property. |
| Profile | Características consolidadas. |
| Location | Contexto geográfico/mercadológico. |
| Comparable | Evidência de mercado. |
| Valuation | Estimativa de valor por método/cenário/confiança. |
| Cost | Custo econômico da operação. |
| Scenario | Premissas econômicas. |
| Strategy | Objetivo do investimento. |
| Rule | Critério decisório parametrizado. |
| Parameter | Valor configurável. |
| Score | Atratividade/prioridade. |
| Fit | Compatibilidade com investidor. |
| Risk | Ameaça/incerteza com impacto. |
| Evidence | Fonte/documento que sustenta afirmação. |
| Pending | Questão não resolvida. |
| Analysis | Tese em uma data. |
| Due Diligence | Investigação profunda. |
| Decision | Resultado formal. |
| Alert | Evento que exige atenção. |
| History | Evolução temporal. |


## Tipos de informação


| Tipo | Uso |
|---|---|
| OBSERVED | Capturado diretamente. |
| CONFIRMED | Validado por evidência. |
| CALCULATED | Derivado matematicamente. |
| ESTIMATED | Estimado com evidências. |
| INFERRED | Inferido, não observado diretamente. |
| UNKNOWN | Não conhecido. |


# 03 — FLUXO PONTA A PONTA

FONTES → CAPTURA → NORMALIZAÇÃO → IDENTIFICAÇÃO → DEDUPLICAÇÃO → CONSOLIDAÇÃO → QUALIFICAÇÃO → PERFIL → VALIDADE JURÍDICA → COMPARÁVEIS → VALUATION → CUSTO → RISCO → LIQUIDEZ → ESTRATÉGIA → REGRAS → SCORE → FIT → RANKING → EXPLICAÇÃO → ANÁLISE → DUE DILIGENCE → DECISÃO → HISTÓRICO → MONITORAMENTO → RESULTADO → APRENDIZADO
Estados: Captured, Normalized, Qualified, Enriched, Valuated, Scored, Ranked, In Analysis, Pending, Monitoring, Approved, Conditional Purchase, Rejected, Blocked, Acquired, Closed.

# 04 — PRECEDÊNCIA DE DECISÃO

BLOCKING → VALIDADE JURÍDICA → ELIGIBILIDADE → DADOS/CONFIANÇA → ECONOMIA → ESTRATÉGIA → RISCO → LIQUIDEZ → SCORE → CAPITAL → RANKING → AÇÃO

| Camada | Pergunta |
|---|---|
| Blocking | Existe impedimento crítico? |
| Validade | A aquisição/procedimento é juridicamente executável? |
| Elegibilidade | Atende filtros mínimos? |
| Dados | Há evidência suficiente? |
| Economia | Há margem/retorno adequado? |
| Estratégia | Serve ao objetivo? |
| Risco | Riscos aceitáveis/mitigáveis? |
| Liquidez | Há demanda e saída plausível? |
| Score | Qual atratividade? |
| Capital | Compete pelo capital? |
| Ranking | Qual prioridade? |
| Ação | Qual próximo estado? |


| Decisão | Regra |
|---|---|
| BUY | Gates críticos satisfeitos. |
| BUY IF | Boa tese condicionada a pendências explicitáveis. |
| MONITOR | Ainda não comprar; acompanhar gatilhos. |
| DO NOT BUY | Não atende à tese. |
| BLOCK | Impedimento crítico confirmado/não sanável. |


# 05 — IDENTIFICAÇÃO E DEDUPLICAÇÃO


| Nível | Significado |
|---|---|
| I0 | Desconhecido |
| I1 | Candidato |
| I2 | Provável |
| I3 | Confirmado |
| I4 | Documental |

Preço sozinho nunca deduplica. Priorizar matrícula, unidade, bloco, endereço, inscrição, área e identificadores de fonte. Ambiguidade permanece explícita.
Muitas fontes → muitas captures → uma property → várias oportunidades/análises ao longo do tempo.

# 06 — QUALIDADE E CONFIANÇA


| Dimensão | Pergunta |
|---|---|
| Completeness | Quanto falta? |
| Atualidade | Ainda é válido? |
| Consistency | Fontes divergem? |
| Precision | Qual precisão? |
| Source | Qual qualidade da fonte? |
| Confirmation | Há confirmação? |
| Relevance | Afeta decisão? |
| Traceability | Volta à evidência? |


| Confiança | Fator ilustrativo |
|---|---|
| Muito alta | 1,00 |
| Alta | 0,95 |
| Média | 0,88 |
| Baixa | 0,75 |
| Muito baixa | 0,60 |
| Inconclusiva | Não recomendar sem resolver ponto crítico |

Fatores são calibráveis e devem ser versionados.

# 07 — MERCADO E LOCALIZAÇÃO

Localização é configurável. Não classificar automaticamente baixa renda/MCMV como ruim. Avaliar micro-localização, demanda, infraestrutura, acesso, oferta, público, preço relativo, financiabilidade e liquidez.
Classes A/B/C/D/E podem existir, mas nunca devem ser hardcoded por bairro.

# 08 — VALUATION E COMPARÁVEIS

Hierarquia recomendada: transações comparáveis > comparáveis muito próximos e recentes > mesmo condomínio > micro-localização > referências amplas. Avaliação da CAIXA é referência, não valor de mercado automático.
- Preferir mesmo condomínio.
- Comparar tipologia, área, quartos, vagas e estado físico.
- Ajustar piso/posição quando relevante.
- Separar anúncio de transação.
- Tratar outliers.
- Produzir cenários conservador/base/otimista e venda rápida.

| Métrica | Fórmula |
|---|---|
| Desconto de mercado | 1 − aquisição / valor de mercado |
| Desconto líquido | 1 − custo econômico total / valor de mercado |
| Margem | valor de mercado − custo econômico total |
| Margem % | (valor de mercado − custo econômico total) / valor de mercado |
| Preço/m² | valor / área considerada |
| Yield mensal bruto | aluguel / custo econômico total |
| Yield anual bruto | yield mensal × 12 |


# 09 — ECONOMIA E PREÇO MÁXIMO

Custo Econômico Total = aquisição + comissão + ITBI/tributos de aquisição + registro/cartório + passivos assumidos + regularização + reforma + desocupação + carrying + financiamento + custos de saída + contingência.

| Reforma | Descrição |
|---|---|
| 0 | Nenhuma relevante |
| 1 | Cosmética |
| 2 | Leve/moderada |
| 3 | Significativa |
| 4 | Pesada/estrutural |

Preço máximo é específico da estratégia. Para revenda, deriva do valor de saída conservador menos custos, margem mínima e contingência. Para renda, respeita yield mínimo e despesas.
Desconto não é lucro.

# 10 — GATE JURÍDICO P0

O anúncio da CAIXA não prova sozinho a regularidade de toda a cadeia. A análise deve verificar matrícula, consolidação, mora, notificações/intimações, edital, leilões, averbações, ônus e processos.

| ID | Verificação | Tratamento |
|---|---|---|
| JUR-001 | Matrícula atualizada | Exigir atualização quando material |
| JUR-002 | Alienação fiduciária/credor | Conferir cadeia |
| JUR-003 | Consolidação em favor da CAIXA | Evidência registral |
| JUR-004 | Constituição em mora | Ato, data, destinatário, evidência |
| JUR-005 | Notificação/intimação aplicável | Analisar caso concreto |
| JUR-006 | Texto do ato de consolidação | Capturar declaração de intimação regular quando houver |
| JUR-007 | Edital e cronologia | Mora → consolidação → leilões coerentes |
| JUR-008 | Leilões negativos/averbação | Verificar aplicabilidade/status |
| JUR-009 | Ônus/indisponibilidades | Investigar situação atual |
| JUR-010 | Processos | Objeto, fase, decisão e impacto |
| JUR-011 | Ocupação/locação | Separar validade de posse |
| JUR-012 | Transferibilidade futura | Regularização antes da saída |
| JUR-013 | Averbação de negativos | Pendência não é nulidade automática |

Classificação: REGULAR_COMPROVADO / PENDENTE / RISCO_JURIDICO / BLOCK / INCONCLUSIVO.
Consolidação registrada comprova o ato registral na data correspondente, mas não substitui verificação de fatos posteriores.
Indício de nulidade não deve ser tratado como nulidade confirmada. Processo, ocupação ou averbação pendente não são, isoladamente, sinônimos de nulidade.

# 11 — OCUPAÇÃO E LOCAÇÃO


| Situação | Tratamento |
|---|---|
| Desocupado confirmado | Registrar evidência |
| Devedor ocupa | Risco de posse |
| Terceiro ocupa | Identificar natureza |
| Inquilino | Investigar contrato e efeitos |
| Desconhecido | UNKNOWN + reduzir confiança |

- Contrato e datas.
- Aluguel e garantia.
- Cláusula de vigência.
- Registro/averbação quando aplicável.
- Relação temporal com garantia fiduciária.
- Impacto sobre posse, prazo e rentabilidade.
Inquilino não é sinônimo de nulidade. Prazo legal não é prazo operacional garantido.

# 12 — LIQUIDEZ E SAÍDA

Liquidez é capacidade de converter o ativo em caixa dentro de preço e prazo aceitáveis.
- Demanda de venda e locação.
- Oferta concorrente.
- Absorção.
- Ticket.
- Financiabilidade.
- Elasticidade de preço.
- Micro-localização.
- Venda rápida.
- Prazo máximo de carregamento.
Liquidez afeta custo de carregamento e preço máximo.

# 13 — ESTRATÉGIAS


| Estratégia | Foco |
|---|---|
| Renda | Yield, aluguel, vacância, despesas |
| Revenda | Desconto líquido, reforma, saída |
| Valorização | Localização, horizonte, tendência |
| MCMV | Ticket, demanda, financiamento |
| Terreno | Uso, zoneamento, localização |
| Apartamento | Ticket, condomínio, demanda |
| Casa/sobrado | Terreno, reforma, liquidez |
| 1 dormitório | Demanda, ticket, locação |

Estratégia e tipo de imóvel são dimensões diferentes.

# 14 — REGRAS E PARÂMETROS


| Prefixo | Domínio |
|---|---|
| GLB | Globais |
| INV | Investidor |
| LOC | Localização |
| TIP | Tipo |
| PRI | Preço |
| CUS | Custos |
| VAL | Valuation |
| CMP | Comparáveis |
| REN | Renda |
| LIQ | Liquidez |
| RISK | Risco |
| CONF | Confiança |
| JUR | Jurídico |
| RANK | Ranking |
| GOV | Governança |
| MON | Monitoramento |


| Exemplo de configuração | Valor ilustrativo |
|---|---|
| Ticket renda | ≤ R$300k |
| Yield alvo | ≥1,0%/mês |
| Yield mínimo | ≥0,8%/mês |
| Liquidez renda | ≥70 |
| Reforma renda | ≤ nível 2 |
| Score renda | ≥70 |
| Ticket revenda | ≤R$400k |
| Desconto líquido revenda | ≥20% |
| Margem pós-reforma | ≥15% |
| Saída | ≤180 dias |
| Liquidez revenda | ≥75 |
| Score revenda | ≥75 |
| Risco crítico | BLOCK |
| Confiança mínima | ≥75% |

Valores acima são configuração ilustrativa do perfil documentado, não regra universal.

# 15 — OPPORTUNITY SCORE


| Componente | Peso ilustrativo |
|---|---|
| Desconto líquido | 25% |
| Margem de segurança | 20% |
| Liquidez | 15% |
| Localização | 15% |
| Risco | 10% |
| Yield | 5% |
| Valorização | 5% |
| Qualidade | 5% |

Score = soma ponderada dos componentes normalizados. Pesos são versionados.

| Faixa | Classificação |
|---|---|
| 90–100 | Exceptional |
| 80–89 | Excellent |
| 70–79 | Very good |
| 60–69 | Interesting |
| 50–59 | Speculative |
| <50 | Weak |
| BLOCK | Eliminado |


# 16 — INVESTOR FIT

Investor Fit mede aderência ao objetivo, estratégia, capital, liquidez e carteira.
Conceito: Score Final = Opportunity Score × aderência × confiança × ajuste de capital/carteira.
- Estratégia.
- Ticket.
- Capital disponível.
- Concentração geográfica/tipo/estratégia.
- Risco acumulado.
- Liquidez necessária.
- Competição com outras oportunidades.
Opportunity good ≠ opportunity good for this investor.

# 17 — RANKING

Ranking pode ser absoluto, por estratégia, relativo ao mercado, temporal, estratégico ou de carteira.
- Desempate: margem robusta, confiança, risco, liquidez, aderência, capital imobilizado e urgência.
- Ranking é dinâmico e muda com preço, valuation, risco, liquidez, estratégia ou capital.

# 18 — EXPLAINABILITY

Toda saída deve responder: por que entrou; valor de mercado; custo total; desconto líquido; estratégia; riscos; pendências; evidências; o que pode invalidar a tese; preço máximo; próxima ação.
Formato: TESE → EVIDÊNCIAS → ECONOMIA → RISCOS → PENDÊNCIAS → ESTRATÉGIA → SCORE/FIT → CONDIÇÕES → DECISÃO → PRÓXIMA AÇÃO.

# 19 — DUE DILIGENCE


| Bloco | Mínimo |
|---|---|
| Identificação | Matrícula, unidade, endereço, inscrição, áreas |
| Registro | Titularidade, fiduciária, consolidação, ônus |
| Procedimento | Mora, notificações, intimações, edital, leilões |
| Judicial | Processos, pedidos, decisões, liminares, impacto |
| Condomínio | Saldo, ações, obras |
| Tributos | IPTU e encargos |
| Ocupação | Quem ocupa, contrato, posse |
| Físico | Visita, reforma, defeitos |
| Mercado | Comparáveis, aluguel, venda |
| Economia | Custo, cenários, preço máximo |
| Decisão | BUY/BUY IF/MONITOR/DO NOT BUY/BLOCK |

Pendência deve ter criticidade, evidência esperada, impacto, prazo e condição de resolução.

# 20 — MONITORAMENTO


| Evento | Reação |
|---|---|
| Preço mudou | Recalcular economia/score |
| Valuation mudou | Reavaliar margem |
| Novo comparável | Atualizar valuation se material |
| Novo risco | Reavaliar |
| Risco resolvido | Recalcular confiança |
| Liquidez mudou | Atualizar prazo/carrying |
| Aluguel mudou | Recalcular yield |
| Estratégia mudou | Recalcular fit |
| Capital mudou | Recalcular prioridade |
| Regra mudou | Registrar versão/impacto |

Alertas: critical/high/medium/low/informational. Evitar fadiga.

# 21 — GOVERNANÇA E AUDITORIA

- Versionar regras, parâmetros, pesos, estratégias e evidências.
- Registrar vigência.
- Preservar análise original.
- Registrar exceções.
- Manter trilha de auditoria.
- Permitir reconstruir uma decisão histórica.
- Registrar fonte e timestamp.
- Não sobrescrever histórico.
Regra de ouro: anos depois, o sistema deve conseguir explicar por que uma propriedade foi classificada daquela forma naquela data.

# 22 — BACKTEST E APRENDIZADO


| Métrica | Uso |
|---|---|
| Precision | Qualidade das recomendações positivas |
| Recall | Cobertura das oportunidades boas |
| False Positive | Recomendação que falhou |
| False Negative | Boa oportunidade descartada |
| Erro valuation | Previsto vs realizado |
| Erro aluguel | Estimado vs realizado |
| Erro prazo | Estimado vs realizado |
| Retorno | Previsto vs realizado |

Nunca usar informação futura para justificar decisão passada. Pesos devem ser calibrados com dados suficientes.

# 23 — CHECKLIST MESTRE

☐ Identificação: fonte, imóvel, matrícula, comarca, inscrição, endereço, áreas.
☐ Matrícula atualizada: titularidade, fiduciária, averbações, ônus.
☐ Consolidação: data, ato, CAIXA, texto do ato.
☐ Mora/notificações: devedor, ato, datas, meio, evidência, intimações aplicáveis.
☐ Leilão: edital, 1º/2º, cronologia, resultados, averbação de negativos.
☐ Processos: objeto, fase, liminares, decisões, impacto.
☐ Ocupação: situação, ocupante, evidência, desocupação.
☐ Locação: contrato, prazo, aluguel, garantia, cláusula de vigência, registro/averbação, efeitos.
☐ Condomínio: saldo, ações, obras.
☐ Tributos: IPTU e demais.
☐ Mercado: comparáveis, mesmo condomínio, preço/m², cenários.
☐ Economia: aquisição, comissão, impostos, cartório, dívidas, reforma, desocupação, carrying, saída, contingência.
☐ Liquidez: demanda, oferta, absorção, ticket, financiamento, saída.
☐ Estratégia: objetivo, ticket, yield/margem, horizonte, capital.
☐ Score/Fit: componentes, pesos, confiança, aderência, capital/carteira.
☐ Decisão: estado, evidências, pendências, condições e próxima ação.
☐ Monitoramento: gatilhos e data de reavaliação.
REGRA DE OURO: DESCONTO NÃO COMPENSA NULIDADE. SCORE NÃO SUPERA BLOCK. AUSÊNCIA DE EVIDÊNCIA NÃO É REGULARIDADE.

# 24 — CONTRATO DE SAÍDA DA IA


| Campo | Conteúdo |
|---|---|
| property_id | Identidade consolidada |
| identity_confidence | I0–I4 |
| legal_status | Regular/Pendente/Risco/Block/Inconclusivo |
| legal_evidence | Evidências |
| occupancy_status | Situação + evidência |
| market_value | Cenários + confiança |
| economic_cost | Composição |
| net_discount | Cálculo |
| margin | Cálculo |
| liquidity_score | 0–100 + evidência |
| strategy | Estratégia |
| opportunity_score | 0–100 + versão |
| investor_fit | 0–100 + versão |
| confidence | Fator/nível + motivos |
| risks | Riscos/severidade |
| pending | Pendências |
| decision | BUY/BUY IF/MONITOR/DO NOT BUY/BLOCK |
| explanation | Justificativa |
| next_actions | Próximas ações |
| rule_version | Versão |
| analysis_date | Data/hora |

Formato recomendado: RESUMO → GATES → MERCADO → ECONOMIA → RISCO → LIQUIDEZ → ESTRATÉGIA → SCORE/FIT → PENDÊNCIAS → DECISÃO → CONDIÇÕES → PRÓXIMA AÇÃO.

# 25 — CASOS DE PROVA DE FOGO


## Reserva dos Pinhais

Caso com consolidação antiga, matrícula fornecida antiga para a análise atual, leilões anteriores e “Averbação dos leilões negativos: Em tratamento”. Regra aprendida: pendência registral não é nulidade automática, mas exige custo/prazo/documentação; matrícula atualizada é necessária.

## Residencial Milano

Caso com consolidação em 31/07/2026, matrícula emitida em 03/08/2026 e “Averbação dos leilões negativos: Não se aplica”. Regra aprendida: cadeia registral recente é evidência forte, mas ainda exige processos, ocupação, condomínio, tributos e análise de notificações.

## Conjunto Residencial Ouro Verde

Caso em que o ato registral de consolidação registra intimação regular e ausência de purgação da mora; houve penhora histórica posteriormente levantada. Regra aprendida: ler o texto do ato é superior a apenas detectar o evento; gravame histórico cancelado não é ônus atual; valuation deve ser independente da avaliação CAIXA.
Lição: procurar primeiro o que pode invalidar ou destruir economicamente a oportunidade; depois analisar o desconto.

# 26 — INVARIANTES DE SEGURANÇA PARA IA

SAFE-001 — A IA não declara regularidade jurídica sem evidência suficiente.
SAFE-002 — Não declara nulidade apenas por processo, ocupação ou averbação pendente.
SAFE-003 — Não inventa custos, dívidas, aluguel, ocupação ou situação registral.
SAFE-004 — UNKNOWN permanece UNKNOWN.
SAFE-005 — Matrícula desatualizada deve ser explicitamente sinalizada.
SAFE-006 — Consolidação registrada não prova ausência de fatos posteriores.
SAFE-007 — O texto do ato registral deve ser considerado quando disponível.
SAFE-008 — Notificação é analisada conforme requisito aplicável ao caso concreto.
SAFE-009 — Inquilino não é sinônimo de nulidade.
SAFE-010 — Averbação de leilões negativos não é sinônimo de nulidade.
SAFE-011 — Processo não é sinônimo de nulidade.
SAFE-012 — Score alto nunca supera BLOCK.
SAFE-013 — Desconto alto nunca prova oportunidade.
SAFE-014 — Avaliação CAIXA não é automaticamente valor de mercado.
SAFE-015 — Preço anunciado não é preço transacionado.
SAFE-016 — Yield bruto não é yield líquido.
SAFE-017 — Custo de compra não é custo econômico total.
SAFE-018 — Prazo legal não é prazo operacional garantido.
SAFE-019 — Decisão precisa de evidências e condições.
SAFE-020 — Dados críticos ausentes reduzem confiança.
SAFE-021 — Mudança material dispara reavaliação.
SAFE-022 — Histórico nunca é apagado.
SAFE-023 — Regra/peso possui versão e vigência.
SAFE-024 — Informação futura não pode contaminar decisão histórica.
SAFE-025 — Conflito entre fontes deve ser registrado, não resolvido silenciosamente.

# 27 — PREPARAÇÃO PARA RAG / BASE VETORIAL

O documento é a fonte canônica. Para RAG, quebrar em chunks semanticamente autocontidos e preservar metadados.

| Metadado | Exemplo |
|---|---|
| document_id | RADAR-KB |
| section_id | JUR-10 |
| topic | validade jurídica |
| rule_id | JUR-003 |
| strategy | renda/revenda |
| version | 1.0 |
| effective_from | data |
| priority | P0 |
| entity_type | Property/Opportunity |
| jurisdiction | Brasil/PR |
| confidence | alta |

Tipos de chunk: DEFINITION, RULE, FORMULA, PARAMETER, CHECKLIST, EXCEPTION, CASE, DECISION, GOVERNANCE, EVIDENCE_GUIDE, STRATEGY, SAFETY.
Para recuperação precisa, preferir chunks pequenos, completos e com IDs estáveis. Não depender de um único chunk para contexto crítico.

# 28 — INTENÇÕES DA FUTURA IA


| Intenção | Recuperar |
|---|---|
| Analisar imóvel | Property + Market + Valuation + Cost + Risk + Strategy + Score + DD |
| Verificar nulidade | Matrícula + consolidação + mora + notificações + edital + leilões + processos |
| Verificar inquilino | Ocupação + contrato + datas + registro/averbação + efeitos |
| Calcular desconto | Preço + valuation + custo |
| Calcular renda | Aluguel + custo + despesas + vacância |
| Preço máximo | Saída + custos + margem + risco + estratégia |
| Comparar imóveis | Opportunity + Fit + Confidence + Capital + Portfolio |
| Explicar decisão | Evidence + Rules + Parameters + Calculations + Pending |
| Reavaliar | Estado atual + evento + análise anterior + versão |
| Auditar | Análise + evidências + regras + parâmetros + timestamps |


# 29 — DEFINIÇÃO FINAL

O Radar procura oportunidades imobiliárias reais, combinando valor de mercado, custo econômico, validade jurídica, risco, liquidez, estratégia, confiança, capital e saída. O objetivo não é dizer apenas “está barato”, mas explicar “por que é uma oportunidade, para qual estratégia, sob quais condições, com quais riscos, por qual preço máximo e o que precisa ser verificado”.
A decisão ideal permanece explicável mesmo depois que o resultado real aparece.

# 30 — FECHAMENTO

Esta documentação consolida a base funcional e decisória do Radar para a próxima etapa de construção e, posteriormente, para a camada de conhecimento consultada pela IA.
Próxima fase: CONSTRUIR → TESTAR COM IMÓVEIS REAIS → MEDIR → CORRIGIR → APRENDER → EVOLUIR.

# 27 Perguntas Adicionais — Checklist de Arrematação

Fonte de origem: imagens anexadas pelo usuário, do livro “O Guia Completo de Leilão de Imóveis”. Tratamento no Radar: os itens entram como conhecimento de domínio e pontos de investigação; as conclusões do livro não são tratadas como regras jurídicas universais. O Radar deve validar cada caso com legislação, jurisprudência, edital, matrícula e evidências.

| ID | Pergunta | Categoria | Tratamento no Radar |
|---|---|---|---|
| JUR-CHK-001 | A intimação para purgar a mora foi pessoal? | Extrajudicial / Jurídico | Gate jurídico/registral, pendência, risco ou bloqueio conforme evidência. |
| JUR-CHK-002 | Se a intimação não foi pessoal, ela foi realizada por edital? | Extrajudicial / Jurídico | Gate jurídico/registral, pendência, risco ou bloqueio conforme evidência. |
| JUR-CHK-003 | Houve envio de notificação para a data dos dois leilões do art. 27 da Lei nº 9.514/97? | Extrajudicial / Jurídico | Gate jurídico/registral, pendência, risco ou bloqueio conforme evidência. |
| JUR-CHK-004 | O contrato de financiamento com alienação fiduciária em garantia está mais de 80% quitado? | Extrajudicial / Jurídico | Gate jurídico/registral, pendência, risco ou bloqueio conforme evidência. |
| JUR-CHK-005 | O bem residencial de pessoa física foi dado em garantia de dívida de terceiro? | Extrajudicial / Jurídico | Gate jurídico/registral, pendência, risco ou bloqueio conforme evidência. |
| JUR-CHK-006 | No segundo leilão, o imóvel está sendo oferecido por menos de 50% do valor de avaliação? | Extrajudicial / Jurídico | Gate jurídico/registral, pendência, risco ou bloqueio conforme evidência. |
| JUR-CHK-007 | Há alguma ação questionando o leilão ou o procedimento de execução extrajudicial antes da data da concorrência? | Extrajudicial / Jurídico | Gate jurídico/registral, pendência, risco ou bloqueio conforme evidência. |
| JUR-CHK-008 | Os leilões negativos do art. 27 da Lei nº 9.514/97 estão averbados na matrícula? | Extrajudicial / Registral | Gate jurídico/registral, pendência, risco ou bloqueio conforme evidência. |
| JUR-CHK-009 | Houve registro do contrato de alienação fiduciária na matrícula e averbação da consolidação da propriedade em nome do credor fiduciário? | Extrajudicial / Registral | Gate jurídico/registral, pendência, risco ou bloqueio conforme evidência. |
| JUR-CHK-010 | Os direitos do devedor fiduciário foram penhorados ou tornados indisponíveis? | Extrajudicial / Jurídico | Gate jurídico/registral, pendência, risco ou bloqueio conforme evidência. |
| JUR-CHK-011 | Há terceiro ocupando o imóvel? Houve contrato de compra e venda entre o devedor fiduciário e terceiro (cessão de posição contratual)? | Extrajudicial / Ocupação | Gate jurídico/registral, pendência, risco ou bloqueio conforme evidência. |
| JUR-CHK-012 | Há terceiro ocupando o imóvel com contrato de locação? O contrato está registrado na matrícula? | Extrajudicial / Locação | Gate jurídico/registral, pendência, risco ou bloqueio conforme evidência. |
| EDIT-CHK-013 | O edital do leilão foi lido integralmente? | Edital / Documental | Validação documental, jurídica ou de custo; depende do texto do edital. |
| EDIT-CHK-014 | O banco se responsabiliza pela evicção de direito? | Edital / Jurídico | Validação documental, jurídica ou de custo; depende do texto do edital. |
| EDIT-CHK-015 | As responsabilidades sobre valores em atraso de IPTU e condomínio até a data do leilão estão claramente definidas no edital? | Edital / Custos | Validação documental, jurídica ou de custo; depende do texto do edital. |
| EDIT-CHK-016 | A vaga de garagem associada ao apartamento possui número de matrícula próprio? | Edital / Registral | Validação documental, jurídica ou de custo; depende do texto do edital. |
| FIN-CHK-017 | O imóvel é muito ilíquido, mesmo considerando eventual desconto na compra? | Financeiro / Liquidez | Variável econômica/mercado que pode afetar score, margem, liquidez ou confiança. |
| FIN-CHK-018 | A taxa de condomínio é superior a 1% ou 1,5% ao ano em relação ao valor do imóvel ou superior à de imóveis semelhantes na região? | Financeiro / Condomínio | Variável econômica/mercado que pode afetar score, margem, liquidez ou confiança. |
| FIN-CHK-019 | É possível encontrar imóveis similares à venda e para aluguel na região? Foi possível formar uma base de pelo menos 7 a 10 comparáveis? | Financeiro / Mercado | Variável econômica/mercado que pode afetar score, margem, liquidez ou confiança. |
| FIN-CHK-020 | A região é segura e possui serviços, comércio, transporte e facilidade de acesso? | Financeiro / Localização | Variável econômica/mercado que pode afetar score, margem, liquidez ou confiança. |
| FIN-CHK-021 | O imóvel precisará de grandes obras de manutenção/reforma para se tornar mais líquido? | Financeiro / Reforma | Variável econômica/mercado que pode afetar score, margem, liquidez ou confiança. |
| FIN-CHK-022 | A taxa de retorno esperada está acima de Selic + 15% ao ano? | Financeiro / Retorno | Variável econômica/mercado que pode afetar score, margem, liquidez ou confiança. |
| FIN-CHK-023 | O prazo estimado entre o pagamento da arrematação e o recebimento do valor total da venda é maior ou igual a dois anos? | Financeiro / Prazo | Variável econômica/mercado que pode afetar score, margem, liquidez ou confiança. |
| LOG-CHK-024 | O imóvel está localizado em cidade ou Estado distante do local onde o investidor mora? | Logística / Administração | Variável operacional/estratégica; deve ser parametrizável por investidor. |
| LOG-CHK-025 | O imóvel precisará de grandes obras de manutenção/reforma? | Logística / Administração | Variável operacional/estratégica; deve ser parametrizável por investidor. |
| LOG-CHK-026 | É possível vender sem corretor? O imóvel está em condomínio com portaria? | Logística / Venda | Variável operacional/estratégica; deve ser parametrizável por investidor. |
| LOG-CHK-027 | O investidor se sente confortável em adquirir imóvel ocupado por uma família? | Investidor / Ocupação / Estratégia | Variável operacional/estratégica; deve ser parametrizável por investidor. |


## Modelo de execução desses 27 itens

- Cada item deve gerar um resultado estruturado: SIM, NÃO, DESCONHECIDO, NÃO APLICÁVEL ou INCONCLUSIVO.
- O Radar deve registrar a evidência que sustenta o resultado e sua fonte.
- Ausência de evidência não deve ser interpretada como regularidade; normalmente reduz a confiança e cria pendência.
- Questões jurídicas críticas são avaliadas antes de score e ranking e podem gerar BLOCK.
- Questões financeiras, de liquidez e logística alimentam economia, score, estratégia e/ou confiança conforme configuração.
- Limites como 50%, 80%, 7–10 comparáveis, Selic + 15% e 2 anos ficam registrados como parâmetros de referência e devem ser configuráveis e versionados.
- O conteúdo deve permanecer rastreável à fonte original e ser atualizado quando legislação, jurisprudência ou política do Radar mudar.

## Regra de segurança jurídica

As perguntas e orientações extraídas das imagens são uma fonte de conhecimento para investigação. O Radar não deve apresentar a conclusão do livro como garantia jurídica. Em temas de nulidade, intimação, consolidação, alienação fiduciária, ocupação, locação, evicção e registro, o agente deve cruzar evidências do caso com a legislação e jurisprudência vigentes e explicitar incertezas.

# Versão 1.2 — Consolidação Completa para Base Vetorial / RAG

Objetivo desta versão: transformar a base do Radar em uma fonte de conhecimento mais adequada para recuperação semântica, raciocínio por agentes, execução de checklist, explicabilidade, avaliação e auditoria.

## 1. Contagem atual dos checklists

Considerando o Checklist Mestre do Radar como a consolidação funcional e somando as 27 perguntas adicionais extraídas das imagens anexadas pelo usuário, temos atualmente:

| Conjunto | Quantidade | Observação |
|---|---|---|
| Checklist Mestre do Radar | 136 | Itens/checks consolidados nas 15 áreas do checklist mestre. |
| Checklist adicional das imagens do livro | 27 | Perguntas adicionais, preservadas com origem própria. |
| TOTAL BRUTO | 163 | Quantidade de checks/perguntas catalogados antes da deduplicação semântica. |

Importante: 163 é a contagem bruta. Existem sobreposições semânticas entre os dois conjuntos (por exemplo: reforma, ocupação, locação, consolidação, leilões negativos, comparáveis e liquidez). Para a IA, não devemos tratar cada repetição como uma regra independente. A próxima etapa de normalização deve criar uma Regra Canônica única, mantendo as perguntas originais como evidências/fontes de origem.

## 2. Estrutura recomendada: pergunta ≠ regra ≠ evidência ≠ decisão

- Pergunta de checklist: o que precisa ser verificado.
- Fato observado: o que foi encontrado no documento/fonte.
- Evidência: documento, trecho, registro, URL, processo, matrícula, anúncio ou cálculo que sustenta o fato.
- Regra canônica: como o Radar interpreta o fato.
- Impacto: jurídico, econômico, liquidez, estratégia, logística ou confiança.
- Decisão: BUY, BUY IF, MONITOR, DO NOT BUY ou BLOCK.
- Explicação: por que a decisão ocorreu e quais condições ainda precisam ser resolvidas.

## 3. Checklist Mestre completo — 136 checks


### 1. IDENTIFICAÇÃO

- ☐ Fonte / banco / leiloeiro identificados
- ☐ Número do imóvel / identificação da oferta
- ☐ Matrícula(s) identificada(s)
- ☐ Comarca / cartório identificados
- ☐ Endereço completo conferido
- ☐ Área / unidade / vagas / características conferidas
- ☐ Captura original preservada

### 2. MATRÍCULA E TITULARIDADE

- ☐ Matrícula atualizada obtida
- ☐ Proprietário atual conferido
- ☐ Alienação fiduciária identificada
- ☐ Credor fiduciário identificado
- ☐ Averbações relevantes analisadas
- ☐ Consolidação da propriedade em nome da CAIXA comprovada, quando aplicável
- ☐ Data da consolidação registrada
- ☐ Ato/averbação registral identificado
- ☐ Inconsistências de titularidade inexistentes ou tratadas

### 3. CONSTITUIÇÃO EM MORA / NOTIFICAÇÕES

- ☐ Devedor/fiduciante identificado
- ☐ Constituição em mora localizada
- ☐ Notificação para purgação da mora verificada
- ☐ Data da notificação registrada
- ☐ Meio/endereço/destinatário conferidos
- ☐ Prazo legal aplicável conferido
- ☐ Evidência documental disponível
- ☐ Eventual devolução/recusa/ausência de recebimento analisada
- ☐ Intimações legalmente exigíveis relacionadas ao leilão verificadas
- ☐ Datas e destinatários conferidos

### 4. EDITAL E CRONOLOGIA DO LEILÃO

- ☐ Edital oficial obtido
- ☐ 1º leilão identificado
- ☐ 2º leilão identificado, quando aplicável
- ☐ Datas e horários conferidos
- ☐ Resultado dos leilões conhecido
- ☐ Cronologia: mora → consolidação → leilão coerente
- ☐ Matrícula e edital sem conflito material
- ☐ Regras específicas do edital analisadas

### 5. PROCESSOS JUDICIAIS / RISCO DE NULIDADE

- ☐ Pesquisa judicial realizada
- ☐ Processos envolvendo devedor analisados
- ☐ Processos envolvendo imóvel/matrícula analisados
- ☐ Ações anulatórias/sustação de leilão pesquisadas
- ☐ Liminares/tutelas identificadas
- ☐ Decisões relevantes analisadas
- ☐ Fase atual registrada
- ☐ Impacto sobre validade do leilão classificado
- ☐ Processo não tratado como BLOCK automático apenas por existir

### 6. OCUPAÇÃO

- ☐ Situação de ocupação conhecida
- ☐ Desocupado confirmado / ocupado / desconhecido
- ☐ Ocupante identificado, quando possível
- ☐ Proprietário/devedor ocupa?
- ☐ Terceiro ocupa?
- ☐ Inquilino ocupa?
- ☐ Evidência da ocupação registrada
- ☐ Custo/prazo de desocupação estimado
- ☐ Risco de posse separado do risco de nulidade

### 7. LOCAÇÃO / INQUILINO

- ☐ Existe contrato de locação?
- ☐ Contrato obtido?
- ☐ Data de início e término
- ☐ Valor do aluguel
- ☐ Garantia
- ☐ Cláusula de vigência
- ☐ Registro/averbação na matrícula, quando aplicável
- ☐ Data do contrato comparada à garantia fiduciária
- ☐ Efeitos jurídicos da locação avaliados
- ☐ Impacto em posse, prazo e rentabilidade calculado
- ☐ Não presumir nulidade do leilão apenas pela existência de inquilino

### 8. DÍVIDAS E ENCARGOS

- ☐ Condomínio
- ☐ IPTU
- ☐ Água/luz/outros encargos
- ☐ Débitos informados pela CAIXA
- ☐ Responsabilidade por cada débito identificada
- ☐ Contingência criada para valores desconhecidos

### 9. MERCADO / VALUATION

- ☐ Comparáveis suficientes
- ☐ Preferência por mesmo condomínio quando possível
- ☐ Preço/m² comparado
- ☐ Conservador/base/otimista
- ☐ Valor de venda rápida
- ☐ Confiança do valuation
- ☐ Anomalias/outliers tratados

### 10. ECONOMIA DA OPERAÇÃO

- ☐ Preço de aquisição
- ☐ ITBI/registro/escritura aplicáveis
- ☐ Comissão do leiloeiro
- ☐ Débitos/contingências
- ☐ Reforma
- ☐ Regularização
- ☐ Custo de desocupação
- ☐ Carrying cost
- ☐ Financiamento, se houver
- ☐ Custos de saída
- ☐ Custo econômico total
- ☐ Desconto líquido
- ☐ Margem de segurança
- ☐ Preço máximo por estratégia

### 11. LIQUIDEZ / SAÍDA

- ☐ Demanda de locação
- ☐ Demanda de venda
- ☐ Oferta concorrente
- ☐ Tempo estimado para alugar
- ☐ Tempo estimado para vender
- ☐ Preço de saída conservador
- ☐ Prazo máximo de carregamento
- ☐ Risco de liquidez

### 12. ESTRATÉGIA DO INVESTIDOR

- ☐ Renda
- ☐ Revenda
- ☐ Valorização
- ☐ MCMV/baixa renda
- ☐ Terreno
- ☐ Apartamento
- ☐ Casa/sobrado
- ☐ 1 dormitório
- ☐ Estratégia efetivamente compatível
- ☐ Capital disponível
- ☐ Concentração de carteira avaliada

### 13. SCORE E DECISÃO

- ☐ Opportunity Score calculado
- ☐ Investor Fit calculado
- ☐ Confiança calculada
- ☐ Ajuste por capital/carteira
- ☐ Ranking calculado
- ☐ Explicação do score registrada
- ☐ BUY / BUY IF / MONITOR / DO NOT BUY / BLOCK
- ☐ Toda decisão possui evidências e justificativa

### 14. GATE FINAL DE VALIDADE JURÍDICA

- ☐ CONSOLIDAÇÃO COMPROVADA
- ☐ MORA/NOTIFICAÇÃO COMPROVADAS OU SUFICIENTEMENTE EVIDENCIADAS
- ☐ INTIMAÇÕES LEGALMENTE EXIGÍVEIS VERIFICADAS
- ☐ EDITAL E CRONOLOGIA COERENTES
- ☐ PROCESSOS SEM IMPACTO MATERIAL OU IMPACTO MITIGADO
- ☐ Nenhum indício material de nulidade sem tratamento
- ☐ Ocupação/locação economicamente e juridicamente tratadas
- ☐ Se qualquer item crítico estiver inconclusivo: PENDENTE/BLOCK, não BUY

### 15. RESULTADO DA ANÁLISE

- ☐ Tese de investimento escrita em uma frase
- ☐ Principais evidências
- ☐ Principais riscos
- ☐ Pendências
- ☐ Condições para compra
- ☐ Preço máximo de compra
- ☐ Cenário conservador
- ☐ Cenário base
- ☐ Cenário estressado
- ☐ Próxima ação definida
- ☐ Data da análise e versão das regras registradas
Total conferido nesta seção: 136 checks.

## 4. Checklist adicional das imagens — 27 perguntas


| ID | Pergunta | Categoria | Tratamento |
|---|---|---|---|
| JUR-CHK-001 | A intimação para purgar a mora foi pessoal? | Extrajudicial / Jurídico | Gate jurídico/registral; pode gerar pendência, risco ou BLOCK conforme evidência. |
| JUR-CHK-002 | Se a intimação não foi pessoal, ela foi realizada por edital? | Extrajudicial / Jurídico | Gate jurídico/registral; pode gerar pendência, risco ou BLOCK conforme evidência. |
| JUR-CHK-003 | Houve envio de notificação para a data dos dois leilões do art. 27 da Lei nº 9.514/97? | Extrajudicial / Jurídico | Gate jurídico/registral; pode gerar pendência, risco ou BLOCK conforme evidência. |
| JUR-CHK-004 | O contrato de financiamento com alienação fiduciária em garantia está mais de 80% quitado? | Extrajudicial / Jurídico | Gate jurídico/registral; pode gerar pendência, risco ou BLOCK conforme evidência. |
| JUR-CHK-005 | O bem residencial de pessoa física foi dado em garantia de dívida de terceiro? | Extrajudicial / Jurídico | Gate jurídico/registral; pode gerar pendência, risco ou BLOCK conforme evidência. |
| JUR-CHK-006 | No segundo leilão, o imóvel está sendo oferecido por menos de 50% do valor de avaliação? | Extrajudicial / Jurídico | Gate jurídico/registral; pode gerar pendência, risco ou BLOCK conforme evidência. |
| JUR-CHK-007 | Há alguma ação questionando o leilão ou o procedimento de execução extrajudicial antes da data da concorrência? | Extrajudicial / Jurídico | Gate jurídico/registral; pode gerar pendência, risco ou BLOCK conforme evidência. |
| JUR-CHK-008 | Os leilões negativos do art. 27 da Lei nº 9.514/97 estão averbados na matrícula? | Extrajudicial / Registral | Gate jurídico/registral; pode gerar pendência, risco ou BLOCK conforme evidência. |
| JUR-CHK-009 | Houve registro do contrato de alienação fiduciária na matrícula e averbação da consolidação da propriedade em nome do credor fiduciário? | Extrajudicial / Registral | Gate jurídico/registral; pode gerar pendência, risco ou BLOCK conforme evidência. |
| JUR-CHK-010 | Os direitos do devedor fiduciário foram penhorados ou tornados indisponíveis? | Extrajudicial / Jurídico | Gate jurídico/registral; pode gerar pendência, risco ou BLOCK conforme evidência. |
| JUR-CHK-011 | Há terceiro ocupando o imóvel? Houve contrato de compra e venda entre o devedor fiduciário e terceiro (cessão de posição contratual)? | Extrajudicial / Ocupação | Gate jurídico/registral; pode gerar pendência, risco ou BLOCK conforme evidência. |
| JUR-CHK-012 | Há terceiro ocupando o imóvel com contrato de locação? O contrato está registrado na matrícula? | Extrajudicial / Locação | Gate jurídico/registral; pode gerar pendência, risco ou BLOCK conforme evidência. |
| EDIT-CHK-013 | O edital do leilão foi lido integralmente? | Edital / Documental | Validação documental/jurídica/custo; depende do edital e documentos. |
| EDIT-CHK-014 | O banco se responsabiliza pela evicção de direito? | Edital / Jurídico | Validação documental/jurídica/custo; depende do edital e documentos. |
| EDIT-CHK-015 | As responsabilidades sobre valores em atraso de IPTU e condomínio até a data do leilão estão claramente definidas no edital? | Edital / Custos | Validação documental/jurídica/custo; depende do edital e documentos. |
| EDIT-CHK-016 | A vaga de garagem associada ao apartamento possui número de matrícula próprio? | Edital / Registral | Validação documental/jurídica/custo; depende do edital e documentos. |
| FIN-CHK-017 | O imóvel é muito ilíquido, mesmo considerando eventual desconto na compra? | Financeiro / Liquidez | Impacta economia, liquidez, valuation, score ou confiança. |
| FIN-CHK-018 | A taxa de condomínio é superior a 1% ou 1,5% ao ano em relação ao valor do imóvel ou superior à de imóveis semelhantes na região? | Financeiro / Condomínio | Impacta economia, liquidez, valuation, score ou confiança. |
| FIN-CHK-019 | É possível encontrar imóveis similares à venda e para aluguel na região? Foi possível formar uma base de pelo menos 7 a 10 comparáveis? | Financeiro / Mercado | Impacta economia, liquidez, valuation, score ou confiança. |
| FIN-CHK-020 | A região é segura e possui serviços, comércio, transporte e facilidade de acesso? | Financeiro / Localização | Impacta economia, liquidez, valuation, score ou confiança. |
| FIN-CHK-021 | O imóvel precisará de grandes obras de manutenção/reforma para se tornar mais líquido? | Financeiro / Reforma | Impacta economia, liquidez, valuation, score ou confiança. |
| FIN-CHK-022 | A taxa de retorno esperada está acima de Selic + 15% ao ano? | Financeiro / Retorno | Impacta economia, liquidez, valuation, score ou confiança. |
| FIN-CHK-023 | O prazo estimado entre o pagamento da arrematação e o recebimento do valor total da venda é maior ou igual a dois anos? | Financeiro / Prazo | Impacta economia, liquidez, valuation, score ou confiança. |
| LOG-CHK-024 | O imóvel está localizado em cidade ou Estado distante do local onde o investidor mora? | Logística / Administração | Impacta logística, estratégia e aderência do investidor. |
| LOG-CHK-025 | O imóvel precisará de grandes obras de manutenção/reforma? | Logística / Administração | Impacta logística, estratégia e aderência do investidor. |
| LOG-CHK-026 | É possível vender sem corretor? O imóvel está em condomínio com portaria? | Logística / Venda | Impacta logística, estratégia e aderência do investidor. |
| LOG-CHK-027 | O investidor se sente confortável em adquirir imóvel ocupado por uma família? | Investidor / Ocupação / Estratégia | Impacta logística, estratégia e aderência do investidor. |


## 5. Provas de fogo — casos reais para avaliação da futura IA

As provas de fogo não são exemplos decorativos. Elas devem funcionar como casos de avaliação (golden cases) para testar se o agente recupera as regras corretas, não confunde ausência de evidência com regularidade, respeita BLOCK, calcula economia e explica a decisão.

### Caso A — COND RESERVA DOS PINHAIS

Entradas do caso:
- Valor de avaliação: R$ 201.100,00.
- Valor mínimo informado: R$ 105.430,40.
- Apartamento de 38,68 m², 1 vaga.
- Identificação informada: 878770253318-5.
- Matrícula informada: 76.036, 2º Registro de Imóveis de São José dos Pinhais.
- Edital informado: 0031/0326-CPVE/RE; item 228; abertura em 29/09/2026.
- Campo do anúncio: “Averbação dos leilões negativos: Em tratamento”.
- Matrícula fornecida anteriormente indicava consolidação em nome da CAIXA em 2022.
Evidências relevantes:
- Existência de ato de consolidação na matrícula fornecida.
- Indicação expressa de averbação dos leilões negativos em tratamento.
- Preço mínimo muito inferior à avaliação informada.
Achados da análise:
- Consolidação em nome da CAIXA aparece comprovada na documentação anterior, porém a matrícula precisa ser atualizada para a análise de 2026.
- Averbação de leilões negativos em tratamento deve ser classificada como pendência registral, não como nulidade automática.
- O preço cria potencial econômico, mas não elimina pendências jurídicas/registrárias.
- Situação de ocupação/identidade do ocupante ainda precisa ser fechada.
Condições que poderiam invalidar a tese:
- Ausência de consolidação válida na matrícula atual.
- Problema material de intimação/notificação identificado.
- Impossibilidade relevante de regularizar a averbação pendente.
- Custos de condomínio, IPTU, reforma ou desocupação que destruam a margem.
Decisão preliminar esperada: BUY IF / PENDING
Confiança: Intermediária; aumentar somente após matrícula atualizada, situação registral atual, ocupação e custos serem confirmados.
Comportamento esperado da IA: A IA deve explicar que o desconto é atraente, mas que a pendência registral e a falta de confirmação atual impedem uma conclusão definitiva. Não deve emitir BLOCK apenas pelo texto “em tratamento”.

### Caso B — RESIDENCIAL MILANO

Entradas do caso:
- Valor de avaliação: R$ 230.000,00.
- 1º leilão: R$ 230.000,00; 2º leilão: R$ 138.000,00.
- Apartamento de 46,97 m², 2 dormitórios, 1 vaga.
- Identificação informada: 855553513794-2.
- Matrícula informada: 71.502, 2º Registro de Imóveis de São José dos Pinhais.
- Edital informado: 0047/0226-CPA/RE; item 234; 1º leilão 08/10/2026; 2º leilão 15/10/2026.
- Campo do anúncio: “Averbação dos leilões negativos: Não se aplica”.
- Matrícula emitida em 03/08/2026; consolidação em nome da CAIXA em 31/07/2026.
Evidências relevantes:
- Matrícula recente.
- Consolidação registrada antes do leilão.
- Indicação de que a averbação de leilões negativos não se aplica.
- Comparáveis do mesmo condomínio/região utilizados na análise anterior.
Achados da análise:
- A cadeia registral parece recente e coerente com o leilão informado.
- A matrícula, isoladamente, não comprova todos os detalhes de notificações que possam ser necessários.
- Condomínio e tributos precisam entrar no custo econômico conforme responsabilidade definida no edital e situação real.
- Ocupação permanece como variável a confirmar.
- Em R$ 138 mil, a tese tende a depender fortemente de margem de revenda e custos totais.
Condições que poderiam invalidar a tese:
- Processo ou decisão judicial com impacto material.
- Ônus atual não considerado.
- Débitos/reforma/desocupação que reduzam a margem abaixo do mínimo da estratégia.
- Valuation superestimado.
Decisão preliminar esperada: BUY IF / PENDING
Confiança: Aproximadamente 78% na análise preliminar anterior, sujeita à confirmação das evidências.
Comportamento esperado da IA: A IA deve separar “consolidação comprovada” de “todas as notificações comprovadas”, calcular o custo econômico total e comparar a tese de renda e revenda sem assumir automaticamente que a avaliação CAIXA é o valor de mercado.

### Caso C — CONJUNTO RESIDENCIAL OURO VERDE

Entradas do caso:
- Valor de avaliação: R$ 285.000,00.
- 1º leilão: R$ 285.000,00; 2º leilão: R$ 171.000,00.
- Apartamento de 51,44 m², 3 dormitórios.
- Identificação informada: 855551826803-1.
- Matrícula informada: 70.081, 8º Registro de Imóveis de Curitiba.
- Edital informado: 0049/0226-CPA/RE; item 259; 1º leilão 20/10/2026; 2º leilão 26/10/2026.
- Campo do anúncio: “Averbação dos leilões negativos: Não se aplica”.
- Matrícula emitida em 31/07/2026.
- AV-13/70.081, datada de 28/07/2026, registra a consolidação em nome da CAIXA.
- O texto do próprio ato de consolidação informa que o devedor foi regularmente notificado e não purgou a mora.
- Constava histórico antigo de penhora/ônus condominial, posteriormente levantado em 2005.
Evidências relevantes:
- AV-13/70.081: consolidação em nome da CAIXA.
- Texto do ato registral com referência à notificação regular e ausência de purgação da mora.
- Histórico registral indicando baixa do ônus antigo.
- Comparáveis do mesmo endereço/condomínio.
- Referência de aluguel próxima a R$ 2.000/mês e condomínio próximo de R$ 500/mês na análise anterior.
Achados da análise:
- O texto do ato de consolidação é uma evidência mais forte do que simplesmente encontrar a palavra “consolidação”.
- O ônus histórico baixado não deve ser tratado como ônus atual.
- A avaliação CAIXA de R$ 285 mil pareceu agressiva diante dos comparáveis utilizados; o valuation precisa ser independente.
- Estimativa de mercado anterior: conservador ~R$ 200 mil; base ~R$ 215–225 mil; otimista ~R$ 235 mil.
- Comissão de 5% sobre R$ 171 mil: R$ 179.550 antes dos demais custos.
- A tese de renda parecia mais robusta que a tese de flip, mas isso depende do custo total e da ocupação.
Condições que poderiam invalidar a tese:
- Qualquer inconsistência atual na consolidação ou notificação.
- Débitos/encargos que reduzam materialmente a margem.
- Reforma relevante não precificada.
- Mercado efetivo muito abaixo do valuation base.
- Problema de ocupação que altere significativamente prazo/custo.
Decisão preliminar esperada: BUY IF / PENDING
Confiança: Boa na parte registral preliminar; econômica ainda dependente de valuation, custos, ocupação e liquidez.
Comportamento esperado da IA: A IA deve reconhecer a evidência positiva do AV-13, mas não extrapolar para uma garantia absoluta. Deve descontar o valuation agressivo e usar comparáveis independentes.

## 6. Matriz de avaliação das provas de fogo


| Teste | Reserva dos Pinhais | Milano | Ouro Verde | O que a IA precisa demonstrar |
|---|---|---|---|---|
| Consolidação | Encontrada, mas matrícula precisa ser atualizada | Recente e registrada | AV-13 + texto do ato | Não confundir anúncio com prova registral. |
| Notificação | Ainda requer fechamento documental | Não totalmente comprovada só pela matrícula | Ato registral menciona notificação regular | Separar evidência forte de evidência ausente. |
| Leilões negativos | Em tratamento | Não se aplica | Não se aplica | Não criar BLOCK automático para “em tratamento”. |
| Ônus históricos | A confirmar na matrícula atual | A confirmar | Ônus antigo foi levantado | Distinguir histórico cancelado de ônus vigente. |
| Valuation | Necessita amostra/custos | Comparáveis suportam análise | Avaliação CAIXA parece agressiva | Valuation independente e faixa conservadora/base/otimista. |
| Ocupação | Desconhecida | Desconhecida | Impacta prazo/custo | Ocupado não significa nulidade. |
| Economia | Potencial forte | Potencial de revenda | Renda parece relevante | Calcular custo econômico total antes da decisão. |


## 7. Casos de teste que a futura IA deve passar


| ID | Cenário | Comportamento esperado |
|---|---|---|
| TF-01 | Consolidação não encontrada | Não localizar consolidação válida na matrícula atual |


## 7. Casos de teste que a futura IA deve passar


| ID | Cenário | Comportamento esperado |
|---|---|---|
| TF-01 | Consolidação não encontrada | Não localizar consolidação válida na matrícula atual → não permitir BUY; classificar como PENDENTE ou BLOCK conforme gravidade/evidência. |
| TF-02 | Consolidação + texto de notificação | Ato registral menciona notificação regular e mora não purgada → reconhecer evidência positiva e aumentar confiança jurídica sem declarar risco zero. |
| TF-03 | Leilões negativos em tratamento | Anúncio informa “Em tratamento” → gerar pendência registral; não transformar automaticamente em nulidade. |
| TF-04 | Processo judicial existente | Há processo relacionado ao devedor/imóvel → analisar objeto, fase e decisões; existência isolada não é BLOCK. |
| TF-05 | Imóvel ocupado | Ocupante é terceiro → separar risco de posse do risco de validade do leilão. |
| TF-06 | Poucos comparáveis | Menos de 7–10 comparáveis confiáveis → reduzir confiança do valuation; não inventar valor de mercado. |
| TF-07 | Avaliação CAIXA acima do mercado | Comparáveis indicam valor menor → usar valuation independente e reduzir margem/score. |
| TF-08 | Score alto com BLOCK jurídico | Economia excelente, mas gate jurídico bloqueado → BLOCK prevalece sobre score. |
| TF-09 | Ausência de evidência | Documento necessário indisponível → retornar UNKNOWN/PENDING/INCONCLUSIVO; nunca assumir regularidade. |
| TF-10 | Reforma pesada | Reforma aumenta liquidez, mas consome margem → incluir custo, prazo, contingência e impacto no preço máximo. |


## 8. Modelo canônico de um item de checklist para o RAG

Cada item deve poder ser armazenado como uma unidade recuperável e, quando necessário, ligado a uma regra canônica.
{
  "checklist_id": "JUR-CHK-003",
  "source_type": "CHECKLIST_SOURCE",
  "source_name": "O Guia Completo de Leilão de Imóveis",
  "domain": "EXTRAJUDICIAL",
  "category": "JURIDICO",
  "question": "...",
  "expected_evidence": [
    "documento de intimação",
    "comprovante de envio/recebimento",
    "matrícula",
    "documentação do procedimento"
  ],
  "possible_results": [
    "SIM",
    "NAO",
    "DESCONHECIDO",
    "NAO_APLICAVEL",
    "INCONCLUSIVO"
  ],
  "impact_types": [
    "LEGAL_RISK",
    "CONFIDENCE"
  ],
  "blocking": "CONDITIONAL",
  "canonical_rule_id": null,
  "source_version": "BOOK_REFERENCE",
  "needs_current_legal_validation": true
}

## 9. Modelo canônico de uma prova de fogo

Para avaliação automática do agente, cada caso deve possuir: entrada factual, documentos/evidências disponíveis, perguntas relevantes, regras que deveriam ser recuperadas, cálculos esperados, riscos esperados, pendências esperadas, decisão esperada, confiança esperada e fatos que invalidariam a tese.

## 10. Regra de ouro para a Base Vetorial

- O RAG recupera conhecimento; ele não substitui o motor determinístico.
- A IA deve registrar qual evidência sustentou cada fato relevante.
- Regra jurídica crítica tem prioridade maior que score econômico.
- Score não supera BLOCK.
- Desconto não compensa nulidade.
- Ausência de evidência não é regularidade.
- Avaliação CAIXA não deve ser tratada automaticamente como valor de mercado.
- Ocupação não deve ser confundida com nulidade.
- Processo judicial existente não deve ser tratado como BLOCK automático.
- “Averbação dos leilões negativos: Em tratamento” é uma pendência registral que exige análise, não um bloqueio universal.
- Parâmetros históricos do checklist devem permanecer versionados e configuráveis.
- Toda decisão precisa ser reproduzível: dados + evidências + regras + parâmetros + versão + data.

## 11. Estratégia de chunking para o futuro Vector DB

- Um chunk por definição importante.
- Um chunk por regra canônica.
- Um chunk por fórmula.
- Um chunk por checklist/pergunta quando a pergunta possuir significado próprio.
- Um chunk por exceção.
- Um chunk por prova de fogo.
- Um chunk por decisão e racional de caso.
- Não duplicar conteúdo apenas porque aparece em vários documentos; usar IDs e relações entre chunks.
- Metadados mínimos: document_id, section_id, chunk_id, topic, rule_id, checklist_id, strategy, source_type, version, effective_from, effective_to, priority, entity_type, jurisdiction, confidence, case_id.
- Manter source_text/paraphrase e provenance separados para permitir auditoria.

## 12. Próxima normalização recomendada

Antes de implementar agentes, transformar os 163 checks brutos em uma matriz de regras canônicas. Exemplo: os checks de consolidação, leilões negativos, ocupação, locação, comparáveis, reforma e liquidez podem possuir múltiplas perguntas de origem, mas uma única regra canônica com vários gatilhos e evidências.
- CHECKLIST → REGRA CANÔNICA
- REGRA → EVIDÊNCIA NECESSÁRIA
- EVIDÊNCIA → FONTE
- FONTE → CONFIANÇA
- REGRA → IMPACTO
- IMPACTO → SCORE / GATE / BLOCK
- REGRA → EXPLICAÇÃO
- REGRA → CASOS DE TESTE
Estado da base nesta versão: 163 checks brutos catalogados, 27 perguntas com origem explícita nas imagens anexadas, Checklist Mestre de 136 checks incorporado, e três provas de fogo estruturadas como casos de avaliação. A próxima versão deve priorizar a deduplicação e a criação dos IDs das regras canônicas antes da implementação do RAG/MCP.
