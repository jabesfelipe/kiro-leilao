# Radar_Imobiliario_Documento_13_Backlog_Funcional_e_Roadmap_do_Produto_v1.0

🎯
RADAR IMOBILIÁRIO
Documento 13 — Backlog Funcional e Roadmap do Produto
Versão 1.0 | Planejamento Funcional

# 1. Objetivo

Transformar a especificação funcional do Radar Imobiliário em um backlog organizado por épicos, funcionalidades, prioridades, dependências e releases. O foco permanece no negócio e na entrega de valor; tecnologia e arquitetura ficam fora deste documento.

# 2. Estratégia de Construção

O Radar deve ser construído de forma incremental, mas cada incremento importante deve aproximar o produto do ciclo completo de decisão.
- Primeiro provar o ciclo econômico: encontrar → valorar → calcular → classificar.
- Depois aumentar qualidade: mercado, risco, due diligence e histórico.
- Depois aumentar cobertura: novas fontes e estratégias.
- Depois aumentar inteligência: monitoramento, backtest e calibração.
- Evitar construir um grande catálogo de imóveis sem capacidade de análise.

# 3. Épicos do Produto


| ID | Épico | Objetivo |
|---|---|---|
| EP-01 | Fundação do Radar | Fontes, captura e identidade do imóvel. |
| EP-02 | Qualificação | Normalização, deduplicação e elegibilidade. |
| EP-03 | Inteligência de Mercado | Localização, comparáveis, aluguel e liquidez. |
| EP-04 | Valuation | Estimativa de valor e confiança. |
| EP-05 | Economia | Custo total, margem, desconto e cenários. |
| EP-06 | Estratégias | Perfis e objetivos de investimento. |
| EP-07 | Regras e Score | Elegibilidade, score e classificação. |
| EP-08 | Radar e Descoberta | Ranking, filtros e comparação. |
| EP-09 | Análise e Due Diligence | Investigação e validação. |
| EP-10 | Decisão e Workflow | Aprovação, rejeição e monitoramento. |
| EP-11 | Alertas e Monitoramento | Mudanças e reavaliações. |
| EP-12 | Histórico e Governança | Versionamento e auditoria. |
| EP-13 | Relatórios | Visões gerenciais. |
| EP-14 | Backtest e Aprendizado | Calibração do modelo. |
| EP-15 | Expansão de Fontes | Outros bancos e provedores. |


# 4. Priorização


| Prioridade | Significado |
|---|---|
| P0 | Essencial para provar a proposta de valor. |
| P1 | Importante para operação eficiente. |
| P2 | Evolução/otimização. |
| P3 | Futuro/experimental. |

Critério de priorização: valor para decisão × impacto econômico × dependência × risco de construção × capacidade de validação.

# 5. Release 0 — Fundação e Prova da Tese

Objetivo: colocar uma oportunidade real no Radar e chegar até uma classificação econômica explicável.

| ID | Feature | Prioridade | Dependência |
|---|---|---|---|
| F-001 | Cadastro de fontes | P0 | — |
| F-002 | Captura de oportunidade | P0 | F-001 |
| F-003 | Preservação do snapshot | P0 | F-002 |
| F-004 | Normalização | P0 | F-002 |
| F-005 | Identificação/consolidação do imóvel | P0 | F-004 |
| F-006 | Perfil do imóvel | P0 | F-005 |
| F-007 | Localização básica | P0 | F-006 |
| F-008 | Comparáveis básicos | P0 | F-007 |
| F-009 | Valuation base | P0 | F-008 |
| F-010 | Custo econômico total | P0 | F-009 |
| F-011 | Desconto líquido e margem | P0 | F-010 |
| F-012 | Estratégia inicial | P0 | F-011 |
| F-013 | Regras essenciais | P0 | F-012 |
| F-014 | Score inicial | P0 | F-013 |
| F-015 | Radar/Raking | P0 | F-014 |
| F-016 | Ficha da oportunidade | P0 | F-015 |
| F-017 | Explicabilidade | P0 | F-016 |


# 6. Release 1 — Análise Profunda

Objetivo: transformar oportunidades interessantes em teses de investimento investigáveis.

| ID | Feature | Prioridade | Dependência |
|---|---|---|---|
| F-018 | Análise estruturada | P0 | F-016 |
| F-019 | Checklist de due diligence | P0 | F-018 |
| F-020 | Evidências | P0 | F-019 |
| F-021 | Pendências | P0 | F-019 |
| F-022 | Riscos | P0 | F-020 |
| F-023 | Cenários econômico-financeiros | P0 | F-010 |
| F-024 | Decisão BUY/BUY IF/MONITOR/DO NOT BUY/BLOCK | P0 | F-019 |
| F-025 | Workflow de estados | P0 | F-024 |
| F-026 | Histórico de decisões | P0 | F-025 |


# 7. Release 2 — Radar Operacional


| ID | Feature | Prioridade | Dependência |
|---|---|---|---|
| F-027 | Filtros avançados | P0 | F-015 |
| F-028 | Ordenação configurável | P0 | F-015 |
| F-029 | Comparador de oportunidades | P1 | F-016 |
| F-030 | Favoritos | P1 | F-016 |
| F-031 | Monitoramento | P1 | F-025 |
| F-032 | Alertas | P1 | F-031 |
| F-033 | Histórico visual | P1 | F-026 |
| F-034 | Dashboard | P1 | F-027 |


# 8. Release 3 — Inteligência e Parametrização


| ID | Feature | Prioridade | Dependência |
|---|---|---|---|
| F-035 | Perfil completo do investidor | P0 | F-012 |
| F-036 | Configuração de localização | P0 | F-035 |
| F-037 | Configuração por tipo de imóvel | P0 | F-035 |
| F-038 | Configuração de ticket/preço | P0 | F-035 |
| F-039 | Configuração de custos | P0 | F-035 |
| F-040 | Configuração de valuation | P0 | F-009 |
| F-041 | Configuração de yield | P0 | F-035 |
| F-042 | Configuração de liquidez | P0 | F-035 |
| F-043 | Configuração de risco | P0 | F-035 |
| F-044 | Pesos do score | P0 | F-014 |
| F-045 | Regras hard/soft/conditional | P0 | F-013 |
| F-046 | Exceções parametrizadas | P1 | F-045 |
| F-047 | Versionamento | P0 | F-045 |


# 9. Release 4 — Monitoramento Inteligente


| ID | Feature | Prioridade | Dependência |
|---|---|---|---|
| F-048 | Detecção de mudança de preço | P1 | F-002 |
| F-049 | Detecção de mudança de status | P1 | F-002 |
| F-050 | Atualização de comparáveis | P1 | F-008 |
| F-051 | Revaluation | P1 | F-009 |
| F-052 | Re-score | P1 | F-014 |
| F-053 | Alertas por limiar | P1 | F-032 |
| F-054 | Reabertura de tese | P1 | F-031 |
| F-055 | Controle de freshness | P1 | F-047 |


# 10. Release 5 — Escala de Fontes e Estratégias


| ID | Feature | Prioridade | Dependência |
|---|---|---|---|
| F-056 | Nova fonte bancária | P1 | EP-15 |
| F-057 | Leiloeiros adicionais | P1 | EP-15 |
| F-058 | Portais/mercado | P1 | EP-15 |
| F-059 | Entrada manual | P1 | EP-15 |
| F-060 | Estratégia de renda | P0 | F-035 |
| F-061 | Estratégia de revenda | P0 | F-035 |
| F-062 | Estratégia de valorização | P1 | F-035 |
| F-063 | Estratégia MCMV/baixa renda | P1 | F-035 |
| F-064 | Estratégia terreno | P1 | F-035 |
| F-065 | Estratégias específicas por tipo | P1 | F-035 |


# 11. Release 6 — Backtest e Aprendizado


| ID | Feature | Prioridade | Objetivo |
|---|---|---|---|
| F-066 | Base histórica de oportunidades | P2 | Criar amostra. |
| F-067 | Backtest de regras | P2 | Avaliar critérios. |
| F-068 | Backtest de score | P2 | Avaliar pesos. |
| F-069 | Erro de valuation | P2 | Calibrar valuation. |
| F-070 | Erro de aluguel | P2 | Calibrar renda. |
| F-071 | Falsos positivos/negativos | P2 | Medir precisão. |
| F-072 | Calibração de thresholds | P2 | Ajustar limites. |
| F-073 | Comparação de versões | P2 | Escolher configurações melhores. |


# 12. User Stories Essenciais


| ID | User Story |
|---|---|
| US-001 | Como investidor, quero configurar meu ticket máximo para não receber oportunidades fora da minha capacidade. |
| US-002 | Como investidor, quero definir bairros prioritários para concentrar o Radar onde tenho interesse. |
| US-003 | Como investidor, quero aceitar tipos diferentes de imóveis conforme estratégia. |
| US-004 | Como investidor, quero saber quanto o imóvel realmente vale no mercado. |
| US-005 | Como investidor, quero saber o custo total antes de considerar o desconto. |
| US-006 | Como investidor, quero saber a margem líquida da oportunidade. |
| US-007 | Como investidor, quero comparar o imóvel com imóveis semelhantes. |
| US-008 | Como investidor, quero entender a confiança do valuation. |
| US-009 | Como investidor, quero saber quais riscos podem destruir a tese. |
| US-010 | Como investidor, quero receber um score por estratégia. |
| US-011 | Como investidor, quero saber por que o Radar recomendou o imóvel. |
| US-012 | Como investidor, quero comparar várias oportunidades. |
| US-013 | Como investidor, quero acompanhar uma oportunidade mesmo sem comprar agora. |
| US-014 | Como investidor, quero ser avisado quando o preço cair. |
| US-015 | Como investidor, quero registrar minha decisão e motivo. |
| US-016 | Como investidor, quero consultar o histórico para entender o que mudou. |
| US-017 | Como analista, quero controlar pendências de due diligence. |
| US-018 | Como gestor, quero alterar regras sem apagar o passado. |


# 13. Backlog de Regras de Negócio


| ID | Regra | Prioridade | Release |
|---|---|---|---|
| BR-001 | Bloquear risco jurídico crítico | P0 | R0 |
| BR-002 | Calcular desconto líquido | P0 | R0 |
| BR-003 | Calcular custo total | P0 | R0 |
| BR-004 | Valuation com confiança | P0 | R0 |
| BR-005 | Score por estratégia | P0 | R0 |
| BR-006 | Explicar score | P0 | R0 |
| BR-007 | Permitir desconhecido | P0 | R0 |
| BR-008 | Preservar histórico | P0 | R1 |
| BR-009 | Reavaliar mudança material | P1 | R4 |
| BR-010 | Exceções justificadas | P1 | R3 |
| BR-011 | Versionar parâmetros | P0 | R3 |
| BR-012 | Backtest antes de calibrar oficialmente | P2 | R6 |


# 14. Dependências Funcionais Críticas


| Dependência | Por quê |
|---|---|
| Identidade do imóvel | Sem ela, capturas não podem ser consolidadas. |
| Comparáveis | Sem evidência, valuation perde confiança. |
| Custos | Sem custo total, desconto pode ser enganoso. |
| Estratégia | Sem estratégia, score não tem contexto. |
| Regras | Sem elegibilidade, ranking pode priorizar risco. |
| Histórico | Sem histórico, o produto não aprende nem audita. |
| Evidências | Sem evidência, explicabilidade fica fraca. |


# 15. Roadmap Conceitual

FASE 1 — PROVAR A TESE
Capturar → Valorar → Calcular → Classificar → Mostrar
FASE 2 — PROVAR A DECISÃO
Analisar → Due Diligence → Decidir → Registrar
FASE 3 — PROVAR A OPERAÇÃO
Monitorar → Alertar → Reavaliar → Histórico
FASE 4 — PROVAR A INTELIGÊNCIA
Backtest → Calibrar → Melhorar
FASE 5 — ESCALAR
Novas fontes → Novas estratégias → Novas regiões

# 16. Métricas de Sucesso por Fase


| Fase | Métrica principal |
|---|---|
| F1 | Percentual de oportunidades corretamente qualificadas. |
| F2 | Percentual de decisões sustentadas por evidências. |
| F3 | Taxa de alertas úteis e tempo de reação. |
| F4 | Precisão do ranking/valuation e redução de falsos positivos. |
| F5 | Cobertura de fontes/regiões sem perda de qualidade. |


# 17. Definition of Ready

- Objetivo de negócio conhecido.
- Regra de negócio identificada.
- Parâmetros envolvidos definidos.
- Dependências conhecidas.
- Critérios de aceite definidos.
- Exceções relevantes mapeadas.
- Impacto no histórico conhecido.

# 18. Definition of Done

- Funcionalidade atende aos critérios de aceite.
- Fluxo normal e exceções foram considerados.
- Regras aplicáveis estão identificadas.
- Histórico/auditoria foram considerados.
- Explicabilidade foi definida quando houver decisão automática.
- Impacto em outras funcionalidades foi avaliado.
- Documentação funcional foi atualizada.

# 19. Riscos do Roadmap


| Risco | Mitigação |
|---|---|
| Construir catálogo antes de inteligência | Priorizar ciclo econômico completo. |
| Score parecer preciso sem validação | Usar confiança e backtest. |
| Excesso de regras | Governança e versionamento. |
| Alertas demais | Critérios de relevância e anti-fadiga. |
| Dependência de uma fonte | Modelo multi-fonte. |
| Valuation fraco | Qualidade/quantidade de comparáveis. |
| Dados faltantes | Pendências e confiança, não zero. |
| Escopo crescer indefinidamente | Roadmap por valor entregue. |


# 20. MVP — Definição Executiva

O MVP do Radar está pronto para ser considerado quando conseguir pegar uma oportunidade real, consolidá-la, estimar seu valor de mercado, calcular seu custo econômico, avaliar uma estratégia, aplicar regras, gerar score, explicar a classificação e permitir que o investidor registre uma decisão.
Esse é o mínimo que prova a tese do produto.

# 21. Resultado Esperado do Produto

O Radar deve evoluir de uma ferramenta de descoberta para um sistema de inteligência de oportunidades imobiliárias:
“Ele encontra. Ele compara. Ele calcula. Ele explica. Ele acompanha. E aprende com o resultado.”

# 22. Próximo Documento Recomendado

Documento 14 — Especificação Funcional dos Dados, Fontes e Enriquecimento. O próximo passo é detalhar exatamente quais informações o Radar precisa para executar sua inteligência: dados mínimos, dados desejáveis, fontes, evidências, qualidade, frequência de atualização, confiabilidade e impacto na análise — ainda sem definir tecnologia.
