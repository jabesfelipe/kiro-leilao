# Radar_Imobiliario_Documento_15_Matriz_Mestra_de_Regras_de_Decisao_v1.1

🏠 RADAR IMOBILIÁRIO
Documento 15
Matriz Mestra de Regras de Decisão e Cenários de Negócio
Especificação de Negócio | Versão 1.0
DADOS → REGRAS → SCORE → CONFIANÇA → ESTRATÉGIA → ALERTA → DECISÃO

# 1. Objetivo

Consolidar a lógica de decisão do Radar Imobiliário em uma matriz única, capaz de transformar dados enriquecidos em classificação, prioridade, alertas e decisão de investimento. O documento conecta os princípios dos Documentos 1 a 14 e cria uma referência operacional para os cenários de negócio.
- Define como regras eliminatórias, regras condicionais, score e confiança convivem.
- Define as saídas BUY, BUY IF, MONITOR, DO NOT BUY e BLOCK.
- Permite avaliar o mesmo imóvel por diferentes estratégias.
- Não define tecnologia ou arquitetura.

# 2. Princípio Central da Decisão

O Radar não pergunta apenas 'quanto está barato?'. Ele pergunta: 'quanto vale, quanto custa adquirir e transformar, quais riscos existem, quão líquida é a saída e quão bem esta oportunidade atende à estratégia?'

| Conceito | Significado |
|---|---|
| Preço | O que está sendo pedido/lance. |
| Valor | Estimativa de mercado em determinado cenário. |
| Custo econômico | Preço + custos conhecidos/estimados + contingências relevantes. |
| Desconto líquido | Diferença entre custo econômico e valor de mercado. |
| Margem de segurança | Proteção econômica contra erros e imprevistos. |
| Score | Atratividade relativa. |
| Confiança | Qualidade da evidência que sustenta a análise. |
| Risco | Fatores que podem destruir ou reduzir a tese. |
| Estratégia | Objetivo do investidor. |
| Decisão | Ação recomendada após todas as dimensões. |


# 3. Ordem de Precedência

A ordem evita que um score alto esconda um problema grave.

| Prioridade | Camada | Função |
|---|---|---|
| 1 | Bloqueios críticos | Elimina a oportunidade. |
| 2 | Elegibilidade | Verifica se o imóvel atende aos critérios mínimos. |
| 3 | Dados/Confiança | Determina se há evidência suficiente. |
| 4 | Economia | Testa custo, desconto e margem. |
| 5 | Estratégia | Verifica aderência ao objetivo. |
| 6 | Score | Prioriza oportunidades elegíveis. |
| 7 | Cenário | Testa robustez da tese. |
| 8 | Ação | Define BUY, BUY IF, MONITOR, DO NOT BUY ou BLOCK. |


# 4. Tipos de Regra


| Tipo | Descrição | Exemplo |
|---|---|---|
| Hard Rule | Eliminatória; não é compensada pelo score. | Risco jurídico crítico confirmado. |
| Soft Rule | Afeta score/prioridade. | Liquidez abaixo do ideal. |
| Conditional Rule | Permite avançar somente sob condição. | Comprar se dívida for quitada. |
| Informational Rule | Gera informação/alerta, sem eliminar. | Preço caiu 8%. |
| Strategy Rule | Válida para determinada estratégia. | Yield mínimo para renda. |
| Exception Rule | Exceção explicitamente autorizada. | Investidor aceita liquidez menor por desconto excepcional. |


# 5. Matriz Mestra de Decisão


| Etapa | Pergunta | Saída |
|---|---|---|
| Elegibilidade | Pode ser analisado? | SIM / NÃO |
| Dados | Há informação suficiente? | CONFIRMADO / PENDENTE |
| Mercado | Qual é o valor provável? | Faixa + confiança |
| Economia | Há margem após custos? | POSITIVA / NEGATIVA |
| Risco | Existe bloqueio? | OK / BLOCK |
| Estratégia | Atende ao objetivo? | ADERENTE / NÃO |
| Score | Quão atrativa é? | 0–100 |
| Robustez | Funciona em cenário conservador? | SIM / NÃO |
| Decisão | Qual ação tomar? | BUY / BUY IF / MONITOR / DO NOT BUY / BLOCK |


# 6. Regras de Elegibilidade


| ID | Regra | Tipo | Resultado |
|---|---|---|---|
| DEC-001 | Localização proibida conforme configuração | Hard | BLOCK |
| DEC-002 | Tipo de imóvel proibido pela estratégia | Hard | BLOCK |
| DEC-003 | Preço acima do limite configurado | Hard/Strategy | BLOCK |
| DEC-004 | Imóvel sem identificação mínima | Hard | PENDENTE/BLOCK |
| DEC-005 | Fonte/condição da oferta não confiável | Conditional | PENDENTE |
| DEC-006 | Dados críticos ausentes | Conditional | PENDENTE |
| DEC-007 | Imóvel atende ao perfil configurado | Soft | Prossegue |
| DEC-008 | Imóvel atende a múltiplas estratégias | Informational | Priorizar análise |


# 7. Regras Econômicas


| ID | Regra | Exemplo de tratamento |
|---|---|---|
| ECO-001 | Calcular custo econômico total | Preço + comissão + tributos + reforma + demais custos |
| ECO-002 | Calcular desconto líquido | 1 − custo econômico / valor de mercado |
| ECO-003 | Calcular margem | valor de mercado − custo econômico |
| ECO-004 | Exigir margem mínima | Abaixo do parâmetro → reduzir score ou eliminar |
| ECO-005 | Custo desconhecido relevante | Criar contingência ou impedir decisão |
| ECO-006 | Testar cenário conservador | Se margem desaparecer → BUY não permitido |
| ECO-007 | Reforma relevante | Incorporar cenário e prazo |
| ECO-008 | Financiamento | Incorporar custo financeiro quando aplicável |


# 8. Regras de Valuation


| Situação | Tratamento |
|---|---|
| Muitos comparáveis de boa qualidade | Maior confiança. |
| Poucos comparáveis | Faixa mais ampla e confiança menor. |
| Comparáveis de segmentos diferentes | Não misturar sem ajustes. |
| Apenas preço anunciado | Usar como evidência, não como preço realizado. |
| Avaliação oficial superior ao mercado | Investigar antes de assumir desconto. |
| Imóvel único | Usar múltiplas evidências e cenário conservador. |
| Conflito material entre fontes | Pendente + redução de confiança. |


# 9. Regras de Confiança


| Confiança | Interpretação | Efeito |
|---|---|---|
| Muito alta | Evidência robusta e atual | Recomendação normal |
| Alta | Boa evidência | Pequena cautela |
| Média | Evidência razoável | Score/recomendação com ressalva |
| Baixa | Muitas estimativas ou lacunas | Priorizar investigação |
| Muito baixa | Tese pouco sustentada | Não recomendar compra |
| Inconclusiva | Dado crítico ausente/conflitante | Pendente ou BLOCK |

A confiança não substitui uma regra eliminatória. Um risco crítico continua sendo bloqueador mesmo com dados altamente confiáveis.

# 10. Score — Estrutura Mestra


| Componente | Peso ilustrativo |
|---|---|
| Desconto líquido | 25% |
| Margem de segurança | 20% |
| Liquidez | 15% |
| Localização | 15% |
| Risco | 10% |
| Yield | 5% |
| Valorização | 5% |
| Qualidade da oportunidade | 5% |
| Total | 100% |

Os pesos são parametrizáveis. A matriz não estabelece pesos universais; eles devem ser calibrados por estratégia e histórico.

# 11. Faixas de Classificação


| Score | Classificação | Ação típica |
|---|---|---|
| 90–100 | Excepcional | Prioridade máxima |
| 80–89 | Excelente | Análise rápida |
| 70–79 | Muito boa | Priorizar |
| 60–69 | Interessante | Monitorar/analisar |
| 50–59 | Especulativa | Somente se estratégia aceitar |
| <50 | Fraca | Baixa prioridade |
| Bloqueado | Eliminada | Não recomendar |


# 12. Estratégia: Renda


| Critério | Regra ilustrativa | Decisão |
|---|---|---|
| Yield | ≥ alvo | Favorece |
| Yield mínimo | ≥ piso configurado | Abaixo → não aderente |
| Vacância | Baixa/média | Score |
| Condomínio | Compatível com aluguel | Score |
| Liquidez locatícia | ≥ mínimo | Score/Hard conforme configuração |
| Reforma | ≤ limite | Score/Conditional |
| Saída | Viável | Obrigatório para robustez |

Exemplo: um apartamento barato com yield alto, mas baixa liquidez de locação, pode ser apenas MONITOR e não BUY.

# 13. Estratégia: Revenda


| Critério | Regra ilustrativa |
|---|---|
| Desconto líquido | ≥ mínimo |
| Margem após reforma | ≥ mínimo |
| Liquidez | ≥ mínimo |
| Prazo de saída | ≤ limite |
| Custo de carregamento | Incluído |
| Preço de saída | Conservador/base |
| Risco documental | Sem bloqueio crítico |


# 14. Estratégia: Valorização


| Critério | Peso esperado |
|---|---|
| Localização | Muito alto |
| Infraestrutura futura | Alto |
| Tendência de mercado | Alto |
| Preço relativo | Alto |
| Horizonte | Parametrizável |
| Renda durante espera | Desejável |
| Liquidez | Importante |


# 15. Estratégia: MCMV / Baixa Renda

A estratégia deve ser tratada como segmento de demanda, não como sinônimo de baixa qualidade.
- Avaliar demanda efetiva.
- Avaliar financiamento e ticket.
- Avaliar aluguel e liquidez.
- Avaliar padrão e localização dentro do segmento.
- Não excluir automaticamente pelo perfil econômico.
- Aplicar as mesmas exigências de evidência, risco e economia.

# 16. Estratégias: Terreno, Casa, Sobrado e 1 Dormitório


| Tipo | Critérios adicionais |
|---|---|
| Terreno | zoneamento, uso, infraestrutura, potencial, liquidez |
| Casa/sobrado | terreno, conservação, reforma, manutenção, demanda |
| 1 dormitório | demanda locatícia, ticket, aluguel, liquidez |
| Apartamento | condomínio, padrão, vagas, comparáveis do empreendimento |


# 17. Regras de Risco e Bloqueio


| Risco | Nível | Tratamento |
|---|---|---|
| Impedimento jurídico crítico confirmado | Crítico | BLOCK |
| Titularidade incompatível | Crítico | BLOCK |
| Condição de venda inviabilizadora | Crítico | BLOCK |
| Ocupação com impacto relevante e sem estratégia | Alto | BUY IF/MONITOR/BLOCK |
| Dívida material desconhecida | Alto | PENDENTE |
| Reforma muito incerta | Médio/Alto | Cenário + contingência |
| Baixa liquidez | Médio | Reduz score |
| Poucos comparáveis | Médio | Reduz confiança |
| Dado antigo | Baixo/Médio | Reenriquecer |


# 18. Cenários de Negócio


| Cenário | Descrição | Resultado esperado |
|---|---|---|
| C-01 | Grande desconto + boa liquidez + baixo risco | BUY |
| C-02 | Grande desconto + risco documental pendente | BUY IF / PENDENTE |
| C-03 | Preço baixo + valuation incerto | MONITOR |
| C-04 | Yield excelente + baixa liquidez | MONITOR/BUY IF |
| C-05 | Desconto moderado + excelente localização | Pode ser BUY por valorização |
| C-06 | Desconto alto + reforma elevada | Recalcular economia |
| C-07 | Ótimo score + risco crítico | BLOCK |
| C-08 | Dados insuficientes + preço excepcional | Investigar, não comprar automaticamente |
| C-09 | Imóvel fora da estratégia atual | DO NOT BUY |
| C-10 | Oportunidade melhora após queda de preço | Reavaliar e alertar |


# 19. Cenários Negativos


| Situação | Ação |
|---|---|
| Valor de mercado revisado para baixo | Recalcular desconto/margem/score |
| Custo de reforma aumenta | Recalcular custo econômico |
| Novo processo relevante | Reavaliar risco |
| Imóvel fica ocupado | Reavaliar prazo/custo |
| Aluguel esperado cai | Recalcular yield |
| Liquidez piora | Reduzir score |
| Preço sobe | Recalcular oportunidade |
| Fonte remove anúncio | Registrar mudança; verificar status |
| Comparáveis desaparecem | Reduzir confiança |
| Regra do investidor muda | Reprocessar aderência |


# 20. Decisão BUY

BUY representa uma recomendação positiva após as condições mínimas serem atendidas.

| Condição | Necessário |
|---|---|
| Sem bloqueio crítico | Sim |
| Dados críticos | Confirmados ou suficientemente sustentados |
| Economia | Margem positiva e adequada |
| Estratégia | Aderente |
| Score | Acima do mínimo |
| Confiança | Acima do mínimo |
| Cenário conservador | Tese ainda aceitável |
| Pendências críticas | Nenhuma |


# 21. Decisão BUY IF

BUY IF é uma recomendação condicional. A oportunidade é boa, mas existe uma condição objetiva que precisa ser resolvida.
- Comprar se determinada dívida estiver dentro do limite.
- Comprar se a ocupação for resolvida em determinada condição.
- Comprar se a reforma ficar dentro do orçamento.
- Comprar se o preço/lance atingir determinado teto.
- Comprar após confirmação documental específica.
Toda condição deve ser objetiva, verificável e ter impacto conhecido na tese.

# 22. Decisão MONITOR

- Tese potencialmente interessante, mas ainda não madura.
- Preço ainda não atingiu o gatilho.
- Dados insuficientes, mas sem sinal de bloqueio.
- Mercado ou liquidez precisam ser acompanhados.
- A oportunidade pode melhorar com mudança de preço/status.
MONITOR não significa rejeição. Significa manter a tese viva e definir o evento que pode fazê-la avançar.

# 23. Decisão DO NOT BUY

- Não há aderência a nenhuma estratégia ativa.
- Economia insuficiente.
- Liquidez incompatível.
- Margem abaixo do mínimo sem compensação.
- Tese depende de premissas improváveis.
- Há alternativa claramente superior.
DO NOT BUY é diferente de BLOCK: a primeira é uma decisão econômica/estratégica; a segunda é uma impossibilidade ou risco impeditivo.

# 24. Decisão BLOCK

BLOCK encerra a possibilidade de recomendação enquanto o bloqueio existir.
- Risco jurídico crítico.
- Impedimento documental crítico.
- Condição de venda incompatível.
- Regra eliminatória expressa do investidor.
- Inconsistência crítica que inviabiliza análise.
Um score elevado nunca supera um BLOCK.

# 25. Exceções


| Exceção | Tratamento |
|---|---|
| Investidor aceita ticket maior | Registrar autorização e estratégia |
| Liquidez abaixo do mínimo | Só permitir se regra de exceção estiver ativa |
| Yield abaixo do alvo | Pode ser compensado por valorização, se configurado |
| Risco conhecido aceito | Registrar justificativa e limite |
| Comparáveis insuficientes | Aceitar somente com confiança mínima e cenário conservador |
| Reforma elevada | Permitir se margem compensar e orçamento for validável |


# 26. Conflitos entre Regras


| Conflito | Precedência |
|---|---|
| BLOCK x Score alto | BLOCK vence |
| Hard x Soft | Hard vence |
| Estratégia x regra global | Regra global vence, salvo exceção autorizada |
| Dado confirmado x estimado | Confirmado tem prioridade |
| Regra nova x regra antiga | Versão vigente vence; histórico preservado |
| Preço atual x preço antigo | Atual para decisão; antigo para histórico |


# 27. Alertas Derivados da Matriz


| Evento | Alerta |
|---|---|
| Score cruza 70 | Nova oportunidade relevante |
| Score cruza 80 | Oportunidade excelente |
| Preço cai além do gatilho | Reavaliar |
| Valuation sobe | Reavaliar margem |
| Novo risco | Alerta de risco |
| Risco resolvido | Oportunidade liberada |
| Pendência crítica resolvida | Pode avançar |
| Condição BUY IF atendida | Ação necessária |
| Mudança de estratégia | Reprocessar universo |
| Mudança material de regra | Recalcular oportunidades afetadas |


# 28. Matriz de Ação por Score × Confiança


| Score | Confiança alta | Confiança média | Confiança baixa |
|---|---|---|---|
| 90–100 | BUY se sem bloqueio | BUY IF / investigar | MONITOR |
| 80–89 | BUY / BUY IF | BUY IF | MONITOR |
| 70–79 | BUY IF / BUY | MONITOR/BUY IF | MONITOR |
| 60–69 | MONITOR/BUY IF | MONITOR | DO NOT BUY |
| <60 | DO NOT BUY | DO NOT BUY | DO NOT BUY |
| Qualquer score + BLOCK | BLOCK | BLOCK | BLOCK |


# 29. Matriz de Robustez por Cenário


| Resultado | Interpretação |
|---|---|
| Tese funciona no conservador | Robusta |
| Tese funciona no base, mas não no conservador | Sensível |
| Tese só funciona no otimista | Especulativa |
| Tese não funciona em nenhum cenário | Rejeitar |
| Cenário conservador depende de dado desconhecido | Pendente |


# 30. Exemplo Completo de Decisão

Exemplo ilustrativo: apartamento capturado por R$ 191.651,31, valor de mercado estimado em R$ 300.000. Após comissão, documentação, reforma e contingência, custo econômico estimado em R$ 220.000. Desconto líquido aproximado de 26,7%. Yield estimado de 1,0% a.m., liquidez 78/100, risco médio e confiança alta.

| Dimensão | Resultado |
|---|---|
| Elegibilidade | SIM |
| Valuation | R$ 300 mil — confiança alta |
| Custo econômico | R$ 220 mil |
| Margem | R$ 80 mil |
| Desconto líquido | 26,7% |
| Yield | 1,0% a.m. |
| Liquidez | 78 |
| Risco | Médio |
| Score | Ex.: 84 |
| Estratégia renda | Aderente |
| Estratégia revenda | Aderente |
| Decisão | BUY IF se pendência crítica estiver resolvida |

O exemplo não constitui recomendação de compra de imóvel específico. Serve para demonstrar a lógica da matriz.

# 31. Regra de Ouro: Preço de Entrada

O Radar deve calcular o preço máximo aceitável para cada estratégia, e não apenas dizer se o preço atual é barato.

| Estratégia | Preço máximo deve considerar |
|---|---|
| Renda | yield mínimo + custos + risco + liquidez |
| Revenda | valor de saída − reforma − custos − margem mínima − carregamento |
| Valorização | valor relativo + horizonte + risco + margem |
| MCMV | ticket + demanda + financiamento + yield + liquidez |
| Terreno | potencial de uso + custos + prazo + liquidez |

Assim, o mesmo imóvel pode ter preço máximo de compra diferente para cada estratégia.

# 32. Reprocessamento

- Alteração de preço.
- Alteração de status.
- Nova avaliação.
- Novo comparável material.
- Mudança de aluguel.
- Novo risco/evidência.
- Mudança de regra ou parâmetro.
- Mudança de estratégia.
- Mudança relevante no custo de reforma.
Eventos materiais devem disparar nova avaliação econômica e, quando necessário, novo score.

# 33. Governança e Versionamento


| Item | Regra |
|---|---|
| Regra | Possui identificador e versão |
| Parâmetro | Possui valor, vigência e contexto |
| Exceção | Possui justificativa |
| Score | Registra pesos utilizados |
| Decisão | Registra data, versão e justificativa |
| Histórico | Nunca apagar decisão anterior |
| Backtest | Avalia impacto de mudanças antes de torná-las definitivas |


# 34. Critérios de Aceite

- CA-D15 — O Radar diferencia bloqueio de baixa pontuação.
- CA-D15 — Uma oportunidade pode ser avaliada por múltiplas estratégias.
- CA-D15 — Score não supera regra eliminatória.
- CA-D15 — Confiança é independente do score.
- CA-D15 — Dados ausentes podem gerar pendência.
- CA-D15 — BUY possui condições objetivas.
- CA-D15 — BUY IF possui condição verificável.
- CA-D15 — MONITOR possui gatilho de evolução.
- CA-D15 — DO NOT BUY possui justificativa econômica/estratégica.
- CA-D15 — BLOCK possui motivo impeditivo.
- CA-D15 — Preço máximo pode ser calculado por estratégia.
- CA-D15 — Alterações materiais provocam reavaliação.
- CA-D15 — Exceções são rastreáveis.
- CA-D15 — Decisões anteriores permanecem no histórico.
- CA-D15 — Os pesos e limites podem ser parametrizados.
- CA-D15 — A matriz permite backtest e calibração futura.

# 35. O que este Documento Fecha

Com os Documentos 1 a 15, o Radar passa a ter uma espinha dorsal completa de negócio:

| Bloco | Documento |
|---|---|
| Regras | 1 |
| Valuation | 2 |
| Estratégias e score | 3 |
| Due Diligence | 4 |
| Requisitos funcionais | 5 |
| Modelo de dados de negócio | 6 |
| Workflow e ciclo de vida | 7 |
| Parâmetros | 8 |
| Módulos e casos de uso | 9 |
| Especificação detalhada | 10 |
| Telas e experiência | 11 |
| Rastreabilidade | 12 |
| Backlog e roadmap | 13 |
| Dados, fontes e enriquecimento | 14 |
| Decisão e cenários | 15 |


# 36. Próximo Documento

Recomendação: Documento 16 — Especificação Funcional da Captura, Normalização, Deduplicação e Identificação de Imóveis. O objetivo será detalhar como uma oportunidade nasce no Radar, como diferentes fontes são consolidadas em um mesmo imóvel, como mudanças são identificadas e como o histórico é preservado — ainda exclusivamente sob a ótica de negócio.
ADENDO v1.1 — GATE DE VALIDADE JURÍDICA DO PROCEDIMENTO
Objetivo: impedir que uma oportunidade seja considerada BUY apenas porque o anúncio é da CAIXA ou apresenta grande desconto. A regularidade do procedimento deve ser comprovada ou explicitamente classificada como pendência/risco.
Nova precedência: BLOCKING > VALIDADE JURÍDICA > ELIGIBILIDADE > DADOS/CONFIANÇA > ECONOMIA > ESTRATÉGIA > RISCO > LIQUIDEZ > SCORE > CAPITAL > RANKING.
GATE-JUR-001 — Consolidação: verificar matrícula atualizada, titularidade da CAIXA quando aplicável, data do ato e evidência registral. Consolidação não comprovada: PENDENTE/BLOCK conforme criticidade.
GATE-JUR-002 — Constituição em mora: verificar devedor, ato de constituição em mora, notificação, endereço/meio, prazo e evidência disponível.
GATE-JUR-003 — Intimações do procedimento: verificar as intimações legalmente exigíveis para o caso concreto, especialmente aquelas relacionadas ao leilão, datas e comprovação.
GATE-JUR-004 — Edital e sequência: confrontar matrícula, edital e cronologia de mora, consolidação e leilões. Inconsistência material gera PENDENTE ou BLOCK.
GATE-JUR-005 — Processos: existência de processo não gera BLOCK automático. O Radar deve avaliar objeto, fase, pedido, decisão, efeito sobre o imóvel/procedimento e evidências.
GATE-JUR-006 — Ocupação/locação: não confundir risco de posse/desocupação com nulidade automática. Ocupação desconhecida reduz confiança e exige investigação; locação deve ser analisada quanto à existência, datas, registro/averbação e efeitos jurídicos aplicáveis.
Regra de segurança: score, desconto, liquidez ou retorno nunca podem superar um BLOCK jurídico.
Estados jurídicos mínimos: REGULAR_COMPROVADO, PENDENTE, RISCO_JURIDICO, BLOCK, INCONCLUSIVO.
