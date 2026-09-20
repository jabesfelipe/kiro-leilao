# Radar_Imobiliario_Documento_12_Matriz_Completa_de_Requisitos_Regras_Casos_de_Uso_e_Criterios_de_Aceite_v1.0

🎯
RADAR IMOBILIÁRIO
Documento 12 — Matriz Completa de Requisitos, Regras,
Casos de Uso e Critérios de Aceite
Versão 1.0 | Matriz de Rastreabilidade Funcional

# 1. Objetivo

Consolidar a documentação de negócio do Radar Imobiliário em uma matriz única de rastreabilidade. O documento conecta requisito, módulo, caso de uso, regra, parâmetro, tela, evento, saída e critério de aceite.

# 2. Finalidade

- Evitar lacunas entre visão de negócio e implementação futura.
- Permitir rastrear de onde cada funcionalidade surgiu.
- Permitir validar se cada regra possui parâmetro e comportamento definido.
- Facilitar priorização de MVP e releases posteriores.
- Permitir testes funcionais baseados em critérios objetivos.
- Preservar a decisão de negócio independentemente da tecnologia escolhida.

# 3. Modelo de Rastreabilidade

A cadeia de rastreabilidade é:
OBJETIVO → REQUISITO → MÓDULO → CASO DE USO → REGRA → PARÂMETRO → TELA → EVENTO → SAÍDA → CRITÉRIO DE ACEITE
Nenhum requisito crítico deve ficar sem módulo, regra quando aplicável e critério de aceite.

# 4. Legenda


| Código | Significado |
|---|---|
| RF | Requisito funcional |
| RN | Regra de negócio |
| UC | Caso de uso |
| PRM | Parâmetro |
| TEL | Tela/experiência |
| EVT | Evento |
| ALT | Alerta |
| CA | Critério de aceite |
| P0 | MVP / obrigatório |
| P1 | Alta prioridade posterior |
| P2 | Evolução |


# 5. Matriz Macro de Módulos


| Módulo | RF | UC | Tela | Prioridade |
|---|---|---|---|---|
| MOD-01 Fontes | RF-031 | UC-004 | TEL-01/Config | P0 |
| MOD-02 Captura | RF-032/033 | UC-004 | TEL-02 | P0 |
| MOD-03 Normalização | RF-034/037 | UC-005 | TEL-02/03 | P0 |
| MOD-04 Deduplicação | RF-035 | UC-005 | TEL-03 | P0 |
| MOD-05 Perfil | RF-036/037 | UC-005 | TEL-03 | P0 |
| MOD-06 Localização | RF-038 | UC-003 | TEL-03/Config | P0 |
| MOD-07 Mercado | RF-039 | UC-007 | TEL-04 | P0 |
| MOD-08 Valuation | RF-040/041 | UC-007 | TEL-04 | P0 |
| MOD-09 Economia | RF-042/043 | UC-008 | TEL-05/06 | P0 |
| MOD-10 Estratégias | RF-044 | UC-002 | TEL-07 | P0 |
| MOD-11 Regras | RF-045/046 | UC-006 | TEL-08/Config | P0 |
| MOD-12 Score | RF-047 | UC-009 | TEL-02/03/07 | P0 |
| MOD-13 Radar | RF-048 | UC-010 | TEL-02 | P0 |
| MOD-14 Análise | RF-049 | UC-011 | TEL-09 | P0 |
| MOD-15 Due Diligence | RF-050 | UC-012 | TEL-10 | P0 |
| MOD-16 Workflow | RF-051 | UC-013 | TEL-09/10 | P0 |
| MOD-17 Alertas | RF-052 | UC-015 | TEL-11 | P1 |
| MOD-18 Monitoramento | RF-053 | UC-014/016 | TEL-12 | P1 |
| MOD-19 Histórico | RF-054 | UC-017 | TEL-12/13 | P0 |
| MOD-20 Relatórios | RF-055 | — | TEL-14 | P1 |
| MOD-21 Backtest | RF-056 | UC-018 | TEL-15 | P2 |
| MOD-22 Governança | RF-057/058 | UC-018 | TEL-16 | P0 |


# 6. Matriz Principal de Requisitos


| ID | Domínio | Requisito | Módulo | UC | Tela | Aceite | Prioridade |
|---|---|---|---|---|---|---|---|
| RF-031 | Fontes | Cadastrar/ativar/desativar fontes | MOD-01 | UC-004 | Configuração | CA-001 | P0 |
| RF-032 | Captura | Preservar snapshot original | MOD-02 | UC-004 | TEL-02 | CA-002 | P0 |
| RF-033 | Captura | Registrar data/hora/status | MOD-02 | UC-004 | TEL-02 | CA-003 | P0 |
| RF-034 | Normalização | Padronizar campos | MOD-03 | UC-005 | TEL-03 | CA-004 | P0 |
| RF-035 | Deduplicação | Detectar/consolidar duplicidades | MOD-04 | UC-005 | TEL-03 | CA-005 | P0 |
| RF-036 | Imóvel | Manter identificação física/documental | MOD-05 | UC-005 | TEL-03 | CA-006 | P0 |
| RF-037 | Perfil | Preservar desconhecidos | MOD-05 | UC-005 | TEL-03 | CA-007 | P0 |
| RF-038 | Localização | Classificar localização | MOD-06 | UC-003 | Config/TEL-03 | CA-008 | P0 |
| RF-039 | Mercado | Registrar comparáveis | MOD-07 | UC-007 | TEL-04 | CA-009 | P0 |
| RF-040 | Valuation | Calcular cenários de valor | MOD-08 | UC-007 | TEL-04 | CA-010 | P0 |
| RF-041 | Valuation | Informar confiança | MOD-08 | UC-007 | TEL-04 | CA-011 | P0 |
| RF-042 | Economia | Calcular custo total | MOD-09 | UC-008 | TEL-05 | CA-012 | P0 |
| RF-043 | Economia | Calcular desconto/margem/retorno | MOD-09 | UC-008 | TEL-05/06 | CA-013 | P0 |
| RF-044 | Estratégia | Aplicar múltiplas estratégias | MOD-10 | UC-002 | TEL-07 | CA-014 | P0 |
| RF-045 | Regras | Aplicar regras | MOD-11 | UC-006 | TEL-08 | CA-015 | P0 |
| RF-046 | Regras | Explicar impacto das regras | MOD-11 | UC-006 | TEL-08 | CA-016 | P0 |
| RF-047 | Score | Calcular score por estratégia | MOD-12 | UC-009 | TEL-02/03 | CA-017 | P0 |
| RF-048 | Ranking | Ordenar oportunidades | MOD-13 | UC-010 | TEL-02 | CA-018 | P0 |
| RF-049 | Análise | Registrar tese e contrapontos | MOD-14 | UC-011 | TEL-09 | CA-019 | P0 |
| RF-050 | Due Diligence | Controlar checklist/evidências | MOD-15 | UC-012 | TEL-10 | CA-020 | P0 |
| RF-051 | Workflow | Controlar estados | MOD-16 | UC-013 | TEL-09/10 | CA-021 | P0 |
| RF-052 | Alertas | Gerar alertas por evento | MOD-17 | UC-015 | TEL-11 | CA-022 | P1 |
| RF-053 | Monitoramento | Reprocessar mudanças | MOD-18 | UC-016 | TEL-12 | CA-023 | P1 |
| RF-054 | Histórico | Preservar evolução | MOD-19 | UC-017 | TEL-13 | CA-024 | P0 |
| RF-055 | Relatórios | Gerar visões consolidadas | MOD-20 | — | TEL-14 | CA-025 | P1 |
| RF-056 | Backtest | Comparar configurações | MOD-21 | UC-018 | TEL-15 | CA-026 | P2 |
| RF-057 | Governança | Versionar parâmetros/regras | MOD-22 | UC-018 | TEL-16 | CA-027 | P0 |
| RF-058 | Governança | Registrar exceções | MOD-22 | UC-018 | TEL-16 | CA-028 | P0 |


# 7. Matriz de Regras de Negócio


| ID | Regra | Domínio | Tela |
|---|---|---|---|
| RN-001 | Preço é dado; valor de mercado é estimativa. | VAL/CUS | TEL-04/05 |
| RN-002 | Desconto nominal não é suficiente. | ECON | TEL-05 |
| RN-003 | Custo desconhecido não é custo zero. | ECON | TEL-05 |
| RN-004 | Risco crítico bloqueia. | RISK | TEL-08/09 |
| RN-005 | Score não supera bloqueio. | SCORE | TEL-03 |
| RN-006 | Estratégias podem gerar scores diferentes. | STR | TEL-07 |
| RN-007 | Confiança reduz força da recomendação. | CONF | TEL-03/08 |
| RN-008 | Dados desconhecidos permanecem desconhecidos. | DATA | TEL-03 |
| RN-009 | Exceções exigem justificativa. | EXC | TEL-16 |
| RN-010 | Histórico não é sobrescrito. | HIST | TEL-13 |
| RN-011 | Mudança material provoca reavaliação. | MON | TEL-12 |
| RN-012 | Valuation precisa de evidências. | VAL | TEL-04 |
| RN-013 | Liquidez faz parte da oportunidade. | LIQ | TEL-03/05 |
| RN-014 | Mesma oportunidade pode ser boa para uma estratégia e ruim para outra. | STR | TEL-07 |
| RN-015 | Recomendação deve ser explicável. | EXPL | TEL-08 |


# 8. Matriz de Parâmetros Críticos


| ID | Parâmetro | Escopo | Requisito | Onde configurar |
|---|---|---|---|---|
| PRI-001 | Preço máximo | Investidor | RF-048 | Config |
| PRI-003 | Desconto mínimo | Investidor/Estratégia | RF-045 | Config |
| PRI-005 | Desconto líquido mínimo | Estratégia | RF-043 | Config |
| CUS-007 | Reforma | Economia | RF-042 | TEL-05 |
| VAL-001 | Mínimo de comparáveis | Valuation | RF-040 | TEL-04 |
| VAL-009 | Confiança mínima valuation | Valuation | RF-041 | Config |
| REN-002 | Yield mínimo | Renda | RF-043 | Config |
| LIQ-001 | Liquidez mínima | Estratégia | RF-048 | Config |
| RISK-001 | Risco jurídico crítico | Global | RF-045 | Config |
| CONF-006 | Dados mínimos para score | Global | RF-047 | Config |
| CONF-007 | Fator de confiança | Global | RF-047 | Config |
| SCORE-001 | Score mínimo | Estratégia | RF-047/048 | Config |
| LOC-003 | Bairro prioritário | Investidor | RF-038 | Config |
| LOC-005 | Bairro condicional | Investidor | RF-038 | Config |
| TIP-001 | Tipos aceitos | Investidor | RF-036 | Config |
| INV-002 | Ticket máximo | Investidor | RF-048 | Config |


# 9. Matriz de Casos de Uso


| ID | Caso de uso | Domínio | Entrada | Saída |
|---|---|---|---|---|
| UC-001 | Configurar perfil | INV | PRM | Perfil salvo e vigente. |
| UC-002 | Configurar estratégia | INV/STR | PRM | Estratégia ativa. |
| UC-003 | Configurar localização | INV/LOC | PRM | Mapa/regra de localização. |
| UC-004 | Receber oportunidade | CAP | Fonte | Captura preservada. |
| UC-005 | Consolidar imóvel | CAP/DEDUP | Property | Imóvel único + capturas. |
| UC-006 | Qualificar | RULE | Regras | Qualified/Rejected/Blocked. |
| UC-007 | Valorar | MARKET/VAL | Comparáveis | Valuation + confiança. |
| UC-008 | Calcular economia | ECON | Custos | Tese econômica. |
| UC-009 | Pontuar | SCORE | Estratégia | Score + explicação. |
| UC-010 | Consultar ranking | RADAR | Filtros | Lista ordenada. |
| UC-011 | Analisar | ANALYSIS | Tese | Análise registrada. |
| UC-012 | Due diligence | DD | Evidências | Pendências/validações. |
| UC-013 | Decidir | WORKFLOW | Regras | Decisão registrada. |
| UC-014 | Monitorar | MON | Gatilhos | Tese ativa. |
| UC-015 | Receber alerta | ALERT | Evento | Alerta acionável. |
| UC-016 | Reavaliar | MON/VAL | Mudança | Novo score/valuation. |
| UC-017 | Consultar histórico | HISTORY | Eventos | Timeline. |
| UC-018 | Calibrar | BACKTEST | Histórico | Configuração avaliada. |


# 10. Matriz de Eventos e Reprocessamento


| Evento | Descrição | Origem | Ação funcional |
|---|---|---|---|
| EVT-001 | Nova captura | Captura | Normalizar/qualificar |
| EVT-002 | Preço alterado | Captura | Recalcular economia/score |
| EVT-003 | Status alterado | Captura | Reavaliar workflow |
| EVT-004 | Novo comparável | Mercado | Reavaliar valuation |
| EVT-005 | Valuation alterado | Valuation | Recalcular economia/score |
| EVT-006 | Novo risco | Risco | Recalcular risco/score |
| EVT-007 | Risco resolvido | Risco | Reavaliar |
| EVT-008 | Nova evidência | DD | Atualizar confiança |
| EVT-009 | Pendência vencida | DD | Gerar alerta |
| EVT-010 | Score alterado | Score | Verificar limiares |
| EVT-011 | Classificação alterada | Score | Gerar alerta se configurado |
| EVT-012 | Regra alterada | Governança | Reprocessar conforme vigência |
| EVT-013 | Estratégia alterada | Estratégia | Recalcular fit/score |
| EVT-014 | Condição atingida | Workflow | Sugerir ação |
| EVT-015 | Decisão registrada | Workflow | Atualizar histórico |


# 11. Matriz de Alertas


| ID | Alerta | Origem | Prioridade |
|---|---|---|---|
| ALT-001 | Nova oportunidade relevante | Radar | Alta |
| ALT-002 | Queda de preço acima do limite | Economia | Alta |
| ALT-003 | Score cruzou limiar | Score | Média/Alta |
| ALT-004 | Valuation mudou materialmente | Mercado | Média/Alta |
| ALT-005 | Novo risco crítico | Risco | Crítica |
| ALT-006 | Risco resolvido | Risco | Média |
| ALT-007 | Condição de compra atingida | Workflow | Alta |
| ALT-008 | Oportunidade/evidência vencendo | Freshness | Média |
| ALT-009 | Status de venda/leilão alterado | Captura | Média |
| ALT-010 | Pendência vencida | DD | Média |


# 12. Matriz de Critérios de Aceite


| ID | Critério | Requisito |
|---|---|---|
| CA-001 | Fonte pode ser identificada e administrada. | RF-031 |
| CA-002 | Snapshot original nunca é perdido. | RF-032 |
| CA-003 | Captura possui data/hora/status. | RF-033 |
| CA-004 | Dados são normalizados sem apagar origem. | RF-034 |
| CA-005 | Duplicidades podem ser detectadas e consolidadas. | RF-035 |
| CA-006 | Imóvel possui identidade consolidada. | RF-036 |
| CA-007 | Campo desconhecido permanece explicitamente desconhecido. | RF-037 |
| CA-008 | Localização segue configuração vigente. | RF-038 |
| CA-009 | Comparáveis possuem origem/data/qualidade. | RF-039 |
| CA-010 | Valuation produz cenários e evidências. | RF-040 |
| CA-011 | Valuation informa confiança. | RF-041 |
| CA-012 | Custo total considera custos conhecidos e incertezas. | RF-042 |
| CA-013 | Desconto/margem/yield podem ser recalculados. | RF-043 |
| CA-014 | Uma oportunidade pode ter múltiplas estratégias. | RF-044 |
| CA-015 | Regras hard/soft/conditional são distinguíveis. | RF-045 |
| CA-016 | Sistema explica regras que afetaram a decisão. | RF-046 |
| CA-017 | Score é específico por estratégia. | RF-047 |
| CA-018 | Ranking respeita filtros e estratégia. | RF-048 |
| CA-019 | Análise registra tese e contrapontos. | RF-049 |
| CA-020 | Due diligence controla evidências e pendências. | RF-050 |
| CA-021 | Workflow impede transições inválidas. | RF-051 |
| CA-022 | Alertas são gerados conforme configuração. | RF-052 |
| CA-023 | Mudança material provoca reavaliação. | RF-053 |
| CA-024 | Histórico preserva evolução. | RF-054 |
| CA-025 | Relatórios refletem dados vigentes e históricos. | RF-055 |
| CA-026 | Backtest compara versões/configurações. | RF-056 |
| CA-027 | Regras/parâmetros possuem versão e vigência. | RF-057 |
| CA-028 | Exceções têm justificativa e rastreabilidade. | RF-058 |


# 13. Matriz de Cenários Negativos


| ID | Cenário | Situação enganosa | Resposta esperada |
|---|---|---|---|
| N-001 | Risco jurídico crítico | Score alto | Bloquear |
| N-002 | Custo desconhecido relevante | Preço atrativo | Reduzir confiança / pendência |
| N-003 | Poucos comparáveis | Valuation desejado | Baixar confiança |
| N-004 | Valuation muito divergente | Múltiplas fontes | Investigar |
| N-005 | Yield alto + baixa liquidez | Boa renda | Penalizar/condicionar |
| N-006 | Desconto alto + reforma alta | Preço baixo | Recalcular custo total |
| N-007 | Bairro fora da preferência | Score alto | Aplicar regra de localização |
| N-008 | Dados antigos | Score alto | Revalidar |
| N-009 | Exceção sem evidência | Regra bloqueia | Não permitir |
| N-010 | Mudança material pós-análise | Decisão anterior | Reabrir/reavaliar |


# 14. Matriz de Priorização do MVP


| Prioridade | Escopo | Objetivo |
|---|---|---|
| P0 | Captura + normalização + deduplicação | Ter dados confiáveis. |
| P0 | Perfil + localização | Conhecer o ativo. |
| P0 | Mercado + valuation | Saber quanto vale. |
| P0 | Economia | Saber quanto custa de verdade. |
| P0 | Estratégia + regras + score | Saber se é oportunidade. |
| P0 | Radar + ficha | Permitir descoberta. |
| P0 | Análise + DD + decisão | Fechar ciclo de decisão. |
| P0 | Histórico + governança | Preservar inteligência. |
| P1 | Alertas + monitoramento | Acompanhar mudanças. |
| P1 | Relatórios + comparador | Aumentar produtividade. |
| P2 | Backtest avançado | Otimizar o modelo. |


# 15. Matriz de Rastreabilidade da Decisão

Toda recomendação final deve conseguir responder à cadeia abaixo:

| Pergunta | Evidência |
|---|---|
| O que foi capturado? | Fonte + snapshot |
| Que imóvel é esse? | Identidade consolidada |
| Quanto vale? | Valuation + comparáveis |
| Quanto custa? | Custos + cenários |
| Por que é oportunidade? | Desconto + margem + estratégia |
| Quais riscos? | Riscos + evidências |
| Quanto confiamos? | Confiança + qualidade dos dados |
| O que falta? | Pendências |
| O que o Radar recomenda? | Classificação + score + ação |
| Qual versão decidiu? | Regra/score/parâmetros |


# 16. Definition of Done Funcional

Uma funcionalidade é considerada funcionalmente pronta quando:
- Possui requisito identificado.
- Possui módulo responsável.
- Possui caso de uso quando aplicável.
- Possui regras de negócio definidas.
- Possui parâmetros identificados.
- Possui tela/fluxo definido quando houver interação.
- Possui eventos relevantes definidos.
- Possui critérios de aceite testáveis.
- Possui tratamento de exceções.
- Possui impacto no histórico quando aplicável.
- Está vinculada a uma prioridade/release.

# 17. Governança da Matriz

- A matriz deve evoluir junto com o produto.
- Novos requisitos recebem novos identificadores.
- Requisitos alterados preservam histórico de versão.
- Uma mudança de regra deve indicar quais requisitos e telas foram afetados.
- Um parâmetro removido não deve apagar o histórico das análises que o utilizaram.
- Critérios de aceite devem ser atualizados quando o comportamento de negócio mudar.

# 18. O que o Documento 12 Fecha

Este documento consolida os Documentos 0–11 em uma visão rastreável. A partir dele, o Radar possui uma linha clara entre visão de negócio, regras, parâmetros, funcionalidades, experiência, eventos e validação.

# 19. Próximo Documento Recomendado

Documento 13 — Backlog Funcional e Roadmap do Produto. A próxima etapa será transformar a matriz em épicos, features, histórias, prioridades, dependências e releases, mantendo a linguagem de negócio e deixando a arquitetura técnica para uma etapa posterior.
