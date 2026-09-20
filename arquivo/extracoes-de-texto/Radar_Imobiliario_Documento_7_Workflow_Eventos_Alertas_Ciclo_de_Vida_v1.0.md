# Radar_Imobiliario_Documento_7_Workflow_Eventos_Alertas_Ciclo_de_Vida_v1.0

Radar Imobiliário
Documento 7 — Workflow de Negócio, Estados, Eventos, Alertas e Ciclo de Vida | v1.0
Documento de negócio — comportamento funcional, transições e acompanhamento.
Princípio: uma oportunidade não nasce pronta nem morre na primeira decisão. Ela evolui conforme preço, evidências, risco, mercado e estratégia mudam.

# 1. Objetivo

Definir o ciclo de vida completo de uma oportunidade, seus estados, eventos, gatilhos, transições, decisões, alertas e regras de reavaliação. O objetivo é garantir que o Radar saiba não apenas classificar imóveis, mas também conduzi-los ao longo do tempo.
- Controlar estados.
- Definir quem/qual processo pode provocar transições.
- Definir eventos relevantes.
- Definir gatilhos de reavaliação.
- Definir alertas e prioridades.
- Preservar histórico.
- Permitir retorno de uma oportunidade ao Radar.
- Evitar decisões irreversíveis sem justificativa.

# 2. Princípio do ciclo de vida

O imóvel é permanente; a oportunidade é dinâmica. O mesmo imóvel pode ser ruim hoje, excelente amanhã e novamente ruim depois. A mudança de preço, mercado, risco ou estratégia deve poder alterar sua classificação.
O histórico nunca deve ser apagado para representar o estado atual.

# 3. Macrofluxo

CAPTURADO → NORMALIZADO → QUALIFICADO → ENRIQUECIDO → VALORADO → PONTUADO → RANKEADO → EM ANÁLISE → DUE DILIGENCE → DECISÃO → MONITORAMENTO → REAVALIAÇÃO
Em qualquer ponto relevante pode ocorrer BLOQUEIO, REPROVAÇÃO, PENDÊNCIA ou RETORNO AO RADAR.

# 4. Estados principais


| Estado | Significado | Saída típica |
|---|---|---|
| Capturado | encontrado em uma fonte | normalização |
| Normalizado | dados padronizados | deduplicação |
| Qualificado | passou filtros mínimos | enriquecimento |
| Enriquecido | possui dados adicionais | valuation |
| Valorado | valor econômico estimado | score |
| Pontuado | score calculado | ranking |
| Rankeado | prioridade definida | análise |
| Em análise | investigação iniciada | Due Diligence |
| Pendente | há questão bloqueadora | retorno à análise |
| Monitorando | ainda sem decisão final | reavaliação |
| Aprovado | tese validada | compra/monitoramento |
| Compra condicional | aguarda condição objetiva | aprovação/reprovação |
| Reprovado | tese não sustentada | encerramento/monitoramento opcional |
| Bloqueado | regra crítica impede avanço | reavaliação quando condição mudar |
| Adquirido | investimento realizado | pós-investimento |
| Encerrado | não há interesse ativo | histórico |


# 5. Transições


| Origem | Evento/condição | Destino |
|---|---|---|
| Capturado | dados mínimos disponíveis | Normalizado |
| Normalizado | identidade consolidada | Qualificado |
| Qualificado | passa filtros | Enriquecido |
| Enriquecido | valuation disponível | Valorado |
| Valorado | regras/score executados | Pontuado |
| Pontuado | entra em faixa de prioridade | Rankeado |
| Rankeado | investigação iniciada | Em análise |
| Em análise | pendência relevante | Pendente |
| Pendente | pendência resolvida | Em análise |
| Em análise | due diligence aberta | Due Diligence |
| Due Diligence | tese validada | Aprovado |
| Due Diligence | condição pendente | Compra condicional |
| Due Diligence | tese destruída | Reprovado |
| Qualquer estado | risco crítico | Bloqueado |
| Monitorando | gatilho relevante | Reavaliação |
| Reavaliação | nova tese válida | Rankeado/Em análise |
| Aprovado | aquisição concluída | Adquirido |
| Qualquer estado ativo | perda de interesse | Encerrado |


# 6. Eventos de negócio

Evento é algo que aconteceu e pode provocar uma reação.

| Código | Evento | Exemplo |
|---|---|---|
| EVT-001 | Nova captura | novo imóvel encontrado |
| EVT-002 | Preço alterado | preço caiu |
| EVT-003 | Status alterado | imóvel saiu/entrou em oferta |
| EVT-004 | Novo comparável | mercado ganhou evidência |
| EVT-005 | Valuation alterado | faixa de mercado mudou |
| EVT-006 | Novo risco | processo/restrição identificado |
| EVT-007 | Risco resolvido | pendência jurídica esclarecida |
| EVT-008 | Nova evidência | documento recebido |
| EVT-009 | Pendência vencida | prazo ultrapassado |
| EVT-010 | Score alterado | pontuação mudou |
| EVT-011 | Classificação alterada | Interessante → Excelente |
| EVT-012 | Regra alterada | parâmetro atualizado |
| EVT-013 | Estratégia alterada | usuário ativou Renda |
| EVT-014 | Condição atingida | preço-alvo alcançado |
| EVT-015 | Decisão registrada | comprar/monitorar/etc. |


# 7. Gatilhos

Gatilho é uma condição que determina que um evento deve provocar uma ação.

| Gatilho | Ação |
|---|---|
| Queda de preço ≥ limite | recalcular economia/score |
| Desconto líquido ≥ limite | elevar prioridade |
| Score sobe de faixa | gerar alerta |
| Novo risco alto/crítico | reavaliar e possivelmente bloquear |
| Valuation cai | recalcular margem |
| Aluguel muda significativamente | recalcular yield |
| Nova captura do mesmo imóvel | atualizar oportunidade |
| Condição de compra atingida | alertar |
| Pendência resolvida | reprocessar análise |
| Regra/parametrização alterada | reavaliar conforme vigência |


# 8. Tipos de alerta


| Tipo | Prioridade | Exemplo |
|---|---|---|
| Crítico | 🔴 | risco impeditivo |
| Urgente | 🔥 | preço-alvo atingido |
| Alto | 🟠 | score entrou em faixa excelente |
| Médio | 🟡 | novo comparável relevante |
| Baixo | 🔵 | alteração pequena |
| Informativo | ⚪ | evento sem ação imediata |


# 9. Alertas econômicos

- Preço caiu.
- Desconto aumentou.
- Margem aumentou.
- Margem caiu.
- Custo estimado aumentou.
- Yield aumentou/caiu.
- Preço-alvo foi atingido.
- Cenário conservador deixou de ser positivo.
- Oportunidade passou a cumprir uma estratégia antes não atendida.

# 10. Alertas de risco

- Novo processo relevante.
- Nova restrição.
- Ocupação identificada.
- Dívida relevante descoberta.
- Reforma estimada aumentou.
- Liquidez caiu.
- Dado crítico ficou desatualizado.
- Confiança caiu abaixo do limite.

# 11. Alertas de oportunidade

- Entrou no Radar.
- Subiu no ranking.
- Score ultrapassou limite.
- Passou a ser aderente a estratégia prioritária.
- Preço entrou na faixa desejada.
- Margem atingiu mínimo.
- Due Diligence pode ser iniciada.
- Pendência crítica foi resolvida.

# 12. Alertas negativos

- Saiu da faixa de preço.
- Score caiu.
- Valuation caiu.
- Margem ficou negativa.
- Risco aumentou.
- Liquidez piorou.
- Oportunidade deixou de ser elegível.
- Condição de aprovação deixou de existir.

# 13. Reavaliação

Reavaliação é obrigatória quando uma mudança material pode alterar a decisão.

| Mudança | Reavaliar |
|---|---|
| Preço | sim |
| Status | sim |
| Valuation | sim |
| Comparáveis relevantes | sim |
| Aluguel | sim, para renda |
| Condomínio | sim, para economia/renda |
| Risco | sim |
| Ocupação | sim |
| Regra/Parâmetro | sim, conforme vigência |
| Mudança pequena sem impacto | não necessariamente |


# 14. Regras de reprocessamento

- Preservar análise anterior.
- Criar nova fotografia da análise.
- Identificar o que mudou.
- Recalcular indicadores afetados.
- Reaplicar regras vigentes.
- Recalcular score.
- Comparar classificação anterior e nova.
- Registrar motivo da mudança.

# 15. Máquina de decisão conceitual

A lógica de negócio pode ser representada assim:
BLOQUEIO? → sim: BLOQUEADO. não → ELEGÍVEL? → não: NÃO PRIORIZAR. sim → ECONOMIA POSITIVA? → não: REPROVAR/MONITORAR. sim → ESTRATÉGIA ADERENTE? → não: MONITORAR. sim → SCORE/CONFIANÇA → RANKING → DUE DILIGENCE → DECISÃO.

# 16. Regras de bloqueio

- Risco jurídico crítico.
- Restrição impeditiva conhecida.
- Impossibilidade de identificar o imóvel.
- Dados essenciais contraditórios sem possibilidade de resolução.
- Condição de aquisição incompatível com a estratégia.
- Outra regra crítica explicitamente configurada.
Bloqueio deve ter motivo, data e condição de desbloqueio quando possível.

# 17. Compra condicional

É usada quando a tese é forte, mas uma condição objetiva precisa ser confirmada.

| Condição | Exemplo |
|---|---|
| Preço | comprar se preço ≤ teto |
| Documento | comprar após confirmação |
| Dívida | comprar se custo final ≤ limite |
| Visita | comprar se reforma ≤ orçamento |
| Jurídico | comprar após resolução/parecer |
| Liquidez | comprar se cenário conservador permanecer positivo |


# 18. Monitoramento

Monitorar não significa abandonar. Significa manter a oportunidade viva sem gastar esforço máximo de Due Diligence.
- Acompanhar preço.
- Acompanhar status.
- Acompanhar score.
- Acompanhar valuation.
- Acompanhar riscos.
- Acompanhar gatilhos personalizados.
- Reabrir análise quando a tese melhorar.

# 19. Encerramento

Uma oportunidade pode ser encerrada por perda de interesse, venda do imóvel, impossibilidade definitiva, tese destruída ou decisão do investidor.
- Registrar motivo.
- Registrar data.
- Preservar histórico.
- Permitir reabertura quando regra permitir.
- Não apagar evidências.

# 20. SLA conceitual

O Radar deve permitir prioridades de tratamento, sem amarrar a tecnologia.

| Prioridade | Tratamento de negócio |
|---|---|
| Crítica | ação imediata |
| Urgente | análise no mesmo ciclo |
| Alta | prioridade próxima |
| Média | fila normal |
| Baixa | monitoramento |


# 21. Responsabilidades


| Papel | Responsabilidade |
|---|---|
| Radar | descobrir e priorizar |
| Investidor | definir estratégia e decisão |
| Analista | validar evidências quando aplicável |
| Especialista jurídico | interpretar questões jurídicas quando necessário |
| Especialista físico | avaliar aspectos construtivos quando necessário |

O produto apoia a decisão; não substitui profissionais especializados em questões que exigem avaliação profissional.

# 22. Histórico de eventos

Cada evento relevante deve permitir reconstruir o fluxo: quando ocorreu, qual estado existia, qual condição foi detectada, qual ação foi tomada e qual resultado ocorreu.

# 23. Histórico de estados


| Informação | Exemplo |
|---|---|
| Estado anterior | Monitorando |
| Evento | preço caiu 8% |
| Novo estado | Reavaliando |
| Resultado | score 82 |
| Nova classificação | Excelente |
| Ação | abrir Due Diligence |


# 24. Preferências de alerta

O investidor deve poder controlar quais eventos considera importantes.
- Ativar/desativar tipos de alerta.
- Definir prioridade mínima.
- Definir estratégias observadas.
- Definir regiões observadas.
- Definir preço-alvo.
- Definir score mínimo.
- Definir margem mínima.
- Definir eventos de risco.
- Definir frequência desejada de resumo.

# 25. Evitar fadiga de alertas

- Agrupar eventos semelhantes.
- Não alertar repetidamente sem mudança material.
- Permitir silenciar uma oportunidade.
- Permitir definir limiar mínimo.
- Elevar prioridade apenas quando houver mudança relevante.
- Mostrar resumo do que mudou.

# 26. Exemplo de ciclo

Dia 1: imóvel capturado por R$ 220 mil. Dia 2: valuation conservador R$ 300 mil e score 68. Dia 10: preço cai para R$ 195 mil; score sobe para 78 e gera alerta. Dia 11: novo comparável confirma mercado; score 82. Dia 12: Due Diligence identifica pendência condominial; estado vira Compra Condicional. Dia 15: dívida confirmada aumenta custo e reduz margem; score 74. Dia 18: condição é resolvida; score volta a 80. Decisão: comprar.

# 27. Ciclo pós-compra

Quando adquirido, o imóvel deixa de ser uma oportunidade de aquisição, mas passa a gerar histórico de investimento.
- Preço efetivamente pago.
- Custos reais.
- Reforma real.
- Tempo até locação/venda.
- Aluguel real.
- Preço de venda real.
- Retorno realizado.
- Diferença entre estimativa e resultado.
Esses dados alimentam o aprendizado e o backtest.

# 28. Métricas do workflow


| Métrica | Objetivo |
|---|---|
| Tempo Capturado → Qualificado | velocidade de triagem |
| Tempo Qualificado → Análise | priorização |
| Tempo Due Diligence | eficiência investigativa |
| Taxa de pendências resolvidas | qualidade operacional |
| Taxa de aprovação | qualidade do filtro |
| Taxa de reprovação | capacidade de eliminar risco |
| Alertas acionáveis | qualidade dos gatilhos |
| Falso alerta | reduzir ruído |
| Conversão em aquisição | valor do Radar |


# 29. Princípios finais

- Toda transição precisa de motivo.
- Toda decisão importante precisa de evidência.
- Mudança material exige reavaliação.
- Histórico não é apagado.
- Bloqueio prevalece sobre score.
- Monitoramento mantém a tese viva.
- Condição deve ser objetiva.
- Alertas devem gerar ação ou informação útil.
- O Radar deve aprender com o resultado real.

# 30. Próximo documento

Documento 8 — Catálogo Completo de Parâmetros, Regras e Configurações do Investidor.
Esse documento deve ser o grande inventário configurável do produto: localização, tipos, preços, descontos, margens, custos, liquidez, risco, valuation, estratégias, score, alertas, workflow, exceções e parâmetros específicos por perfil. A ideia é chegar ao ponto em que praticamente nenhuma decisão de negócio relevante esteja hard-coded.
