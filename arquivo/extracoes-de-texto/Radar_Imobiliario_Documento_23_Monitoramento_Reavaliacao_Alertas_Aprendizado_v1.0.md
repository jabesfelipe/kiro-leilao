# Radar_Imobiliario_Documento_23_Monitoramento_Reavaliacao_Alertas_Aprendizado_v1.0

🏠 RADAR IMOBILIÁRIO
Documento 23
Monitoramento, Reavaliação, Alertas Inteligentes e Aprendizado Contínuo
Especificação Funcional de Negócio | Versão 1.0

# 1. Objetivo

Definir como o Radar acompanha oportunidades ao longo do tempo, detecta mudanças relevantes, reavalia teses, gera alertas acionáveis e utiliza resultados reais para melhorar regras, pesos e decisões futuras.
- Manter oportunidades vivas após a primeira análise.
- Detectar mudanças materiais.
- Evitar reanálises desnecessárias.
- Gerar alertas somente quando houver ação possível.
- Preservar histórico de decisões.
- Comparar previsão com resultado real.
- Aprender com acertos, erros e rejeições.

# 2. Princípio Central

Oportunidade imobiliária é dinâmica. Preço, concorrência, aluguel, valuation, risco, documentação, liquidez e estratégia podem mudar. O Radar deve acompanhar a tese, e não apenas armazenar um retrato.

| Modelo antigo | Modelo do Radar |
|---|---|
| Análise pontual | Análise contínua |
| Lista de imóveis | Tes es monitoradas |
| Alerta por qualquer mudança | Alerta por materialidade |
| Score fixo | Score recalculável |
| Decisão final | Decisão revisável |
| Histórico descartado | Histórico preservado |
| Sem aprendizado | Backtest e calibração |


# 3. Ciclo Contínuo

CAPTURA → ANÁLISE → RANKING → MONITORAMENTO → MUDANÇA → REAVALIAÇÃO → NOVA DECISÃO → RESULTADO REAL → APRENDIZADO → NOVA CALIBRAÇÃO
Esse ciclo conecta descoberta, análise, decisão e aprendizado.

# 4. O que Monitorar


| Dimensão | Exemplos |
|---|---|
| Preço | Preço de venda/lance, redução, aumento |
| Valuation | Mudança no valor estimado |
| Comparáveis | Novos anúncios, vendas e preços |
| Aluguel | Preço e oferta de locação |
| Liquidez | Tempo de anúncio, concorrência, demanda |
| Risco | Processos, ocupação, documentos, dívidas |
| Físico | Reforma, condição, visita |
| Estratégia | Mudança de objetivo do investidor |
| Capital | Capital livre e comprometido |
| Portfólio | Concentração e exposição |


# 5. Materialidade

Nem toda mudança deve provocar reprocessamento completo. O Radar deve classificar eventos por impacto.

| Nível | Exemplo | Ação |
|---|---|---|
| Crítico | Novo risco impeditivo | BLOCK imediato |
| Alto | Grande queda de preço | Reavaliar completo |
| Médio | Novo comparável relevante | Recalcular valuation |
| Baixo | Pequena alteração | Registrar |
| Informativo | Mudança sem impacto | Histórico |


# 6. Gatilhos de Reavaliação


| Gatilho | Reavaliação |
|---|---|
| Preço mudou acima do limite | Economia + score + ranking |
| Valuation mudou materialmente | Economia + score |
| Novo risco crítico | Risco + decisão |
| Liquidez caiu significativamente | Saída + score |
| Aluguel mudou materialmente | Renda + score |
| Novo comparável relevante | Valuation |
| Pendência resolvida | Confiança + score |
| Estratégia mudou | Fit + ranking |
| Capital disponível mudou | Portfólio + ranking |


# 7. Reavaliação Parcial x Completa


| Tipo | Quando |
|---|---|
| Parcial | Mudança restrita a uma dimensão. |
| Econômica | Preço, custo, aluguel ou valuation. |
| Risco | Documento, ocupação, processo ou dívida. |
| Estratégica | Mudança de perfil/objetivo. |
| Completa | Mudança material em múltiplas dimensões. |

O histórico deve registrar quais dimensões foram reprocessadas.

# 8. Alertas Inteligentes

Um alerta deve ser acionável. Não basta informar que algo mudou; deve explicar o impacto e sugerir a próxima ação.

| Alerta ruim | Alerta bom |
|---|---|
| Preço mudou. | Preço caiu 8%; margem aumentou e oportunidade subiu 14 posições. |
| Novo anúncio. | Novo comparável reduz valuation base em R$ 12 mil. |
| Mudança de status. | Oportunidade perdeu elegibilidade. |
| Risco detectado. | Novo processo pode elevar custo/prazo; DD necessária. |


# 9. Prioridade dos Alertas


| Prioridade | Uso |
|---|---|
| P0 — Crítico | Ação imediata |
| P1 — Urgente | Analisar rapidamente |
| P2 — Alto | Entrar na fila ativa |
| P3 — Médio | Acompanhar |
| P4 — Baixo | Histórico/consulta |
| Informativo | Sem ação |


# 10. Redução de Fadiga

- Agrupar mudanças relacionadas.
- Evitar alertar duas vezes o mesmo fato.
- Aplicar limiar de materialidade.
- Respeitar preferências do investidor.
- Silenciar alertas sem ação.
- Escalar somente quando a situação piorar.
- Mostrar resumo diário/agrupado quando apropriado.

# 11. Alertas de Oportunidade


| Evento | Mensagem de negócio |
|---|---|
| Preço caiu | Margem melhorou. |
| Valuation subiu | Desconto aumentou. |
| Liquidez melhorou | Prazo de saída estimado caiu. |
| Risco resolvido | Confiança aumentou. |
| Pendência resolvida | Pode avançar para DD/decisão. |
| Entrou no Top 3 | Prioridade máxima. |


# 12. Alertas Negativos


| Evento | Consequência |
|---|---|
| Preço subiu | Margem diminuiu. |
| Valuation caiu | Desconto líquido diminuiu. |
| Aluguel caiu | Yield diminuiu. |
| Concorrência aumentou | Liquidez pode cair. |
| Novo risco | Reavaliar. |
| Prazo aumentou | Custo de capital aumenta. |
| Reserva comprometida | Compra pode ser bloqueada. |


# 13. Monitoramento por Estado


| Estado | Monitoramento |
|---|---|
| Captured | Mudanças na fonte |
| Qualified | Elegibilidade |
| Ranked | Score e posição |
| In Analysis | Dados críticos |
| Pending | Pendências |
| Monitoring | Gatilhos definidos |
| Approved | Condições de compra |
| Conditional Purchase | Condições específicas |
| Acquired | Resultado real |
| Closed | Aprendizado histórico |


# 14. Monitoramento de Oportunidade

Toda oportunidade em MONITORING deve possuir:
- Motivo do monitoramento.
- Tese atual.
- Gatilho de reentrada.
- Gatilho de abandono.
- Preço-alvo.
- Score mínimo.
- Liquidez mínima.
- Pendências relevantes.
- Data da próxima revisão, quando aplicável.

# 15. Monitoramento de BUY IF

Uma oportunidade condicional deve possuir condições objetivas.

| Condição | Exemplo |
|---|---|
| Preço | Comprar se ≤ R$ 185 mil |
| Documento | Comprar após regularização confirmada |
| Reforma | Comprar se orçamento ≤ R$ 35 mil |
| Risco | Comprar após resolução de pendência |
| Liquidez | Comprar se comparáveis confirmarem demanda |


# 16. Reentrada no Ranking

Oportunidades rejeitadas ou monitoradas podem retornar ao ranking se a tese mudar.

| Evento | Resultado |
|---|---|
| Preço cai | Reavaliar |
| Risco é resolvido | Reavaliar |
| Liquidez melhora | Reavaliar |
| Valuation aumenta | Reavaliar |
| Nova estratégia | Reavaliar Fit |
| Mercado muda | Reavaliar |


# 17. Abandono da Tese

- Margem desapareceu.
- Preço máximo foi ultrapassado.
- Risco tornou-se inaceitável.
- Liquidez ficou abaixo do mínimo.
- Tese de demanda deixou de existir.
- Custo de reforma inviabilizou a operação.
- Capital ficou indisponível.
- Outra oportunidade tornou-se claramente superior.

# 18. Resultado Real

Após aquisição, o Radar deve comparar previsão e realidade.

| Previsto | Real |
|---|---|
| Preço de compra | Preço efetivamente pago |
| Reforma | Custo real |
| Prazo de reforma | Prazo real |
| Aluguel | Aluguel realizado |
| Vacância | Vacância real |
| Venda | Preço efetivo |
| Prazo de saída | Prazo real |
| Retorno | Retorno realizado |


# 19. Aprendizado

O Radar deve descobrir onde suas estimativas erram.

| Erro | Pergunta |
|---|---|
| Valuation | Estimamos acima/abaixo? |
| Reforma | Orçamento foi realista? |
| Aluguel | Estimativa foi correta? |
| Liquidez | Prazo foi subestimado? |
| Risco | Algum risco foi ignorado? |
| Score | O ranking antecipou o resultado? |


# 20. Backtest

- Reproduzir decisões com dados históricos.
- Verificar quais oportunidades realmente performaram.
- Comparar aprovadas, rejeitadas e ignoradas.
- Testar diferentes pesos.
- Testar limites de score.
- Medir falsos positivos.
- Medir falsos negativos.

# 21. Métricas de Aprendizado


| Métrica | Objetivo |
|---|---|
| Precisão de oportunidades | Quantas classificadas como boas foram boas. |
| Recall | Quantas boas oportunidades foram encontradas. |
| Falso positivo | Boa classificação que não se confirmou. |
| Falso negativo | Oportunidade perdida. |
| Erro de valuation | Diferença estimado × realizado. |
| Erro de prazo | Diferença previsto × realizado. |
| Erro de aluguel | Diferença previsto × realizado. |
| Retorno previsto × real | Calibração econômica. |


# 22. Calibração de Regras

Pesos e limites não devem ser tratados como verdades permanentes.
- Testar versão atual.
- Comparar com versões anteriores.
- Medir impacto.
- Evitar overfitting.
- Manter explicabilidade.
- Aprovar alterações antes de produção operacional.
- Preservar histórico de versões.

# 23. Aprendizado sem Automatismo Cego

O Radar pode aprender com dados, mas não deve alterar sozinho uma regra crítica sem governança. O aprendizado serve para sugerir calibração; decisões de negócio devem permanecer auditáveis.

| Pode sugerir | Não deve fazer sozinho |
|---|---|
| Ajuste de peso | Liberar risco crítico |
| Novo limiar | Ignorar bloqueio |
| Novo comparável | Alterar responsabilidade jurídica |
| Correção de estimativa | Comprar automaticamente |


# 24. Evolução do Score

Exemplo: após centenas de operações, pode-se descobrir que liquidez estava subponderada. O Radar pode propor aumentar seu peso, testar o impacto histórico e somente então publicar uma nova versão.

| Versão | Liquidez | Resultado histórico |
|---|---|---|
| v1 | 15% | Base |
| v2 | 20% | Teste |
| v3 | 20% | Aprovada, se comprovada |


# 25. Controle de Mudança


| Mudança | Registro obrigatório |
|---|---|
| Peso | Valor anterior, novo, motivo |
| Regra | Versão e justificativa |
| Parâmetro | Antes/depois |
| Estratégia | Impacto esperado |
| Score | Recalibração |
| Bloqueio | Aprovação e evidência |


# 26. Alertas de Aprendizado

- Regra apresenta alto falso positivo.
- Valuation sistematicamente superestima mercado.
- Prazo de venda é subestimado.
- Reforma ultrapassa estimativa.
- Uma classe de imóveis apresenta desempenho superior.
- Uma localização apresenta liquidez maior/menor que o esperado.

# 27. Monitoramento de Mercado


| Sinal | Possível impacto |
|---|---|
| Oferta aumenta | Liquidez ↓ |
| Preços caem | Valuation/saída ↓ |
| Aluguéis sobem | Yield ↑ |
| Financiamento melhora | Demanda ↑ |
| Financiamento piora | Demanda ↓ |
| Infraestrutura melhora | Valorização ↑ |
| Nova concorrência forte | Saída ↓ |


# 28. Reavaliação da Tese

A tese deve ser reescrita quando houver mudança material, não apenas o score.

| Antes | Depois |
|---|---|
| Comprar por desconto | Comprar por desconto + liquidez |
| Renda estimada | Renda confirmada |
| Risco desconhecido | Risco confirmado |
| Valuation R$ 300k | Valuation R$ 285k |
| BUY | BUY IF/MONITOR |


# 29. Histórico de Decisões

- Data.
- Status.
- Score.
- Fit.
- Confiança.
- Valuation.
- Custo.
- Risco.
- Liquidez.
- Motivo.
- Evidências.
- Regra/versão aplicada.

# 30. Alertas e Ação Recomendada


| Situação | Ação |
|---|---|
| Oportunidade subiu muito | Analisar agora |
| Margem caiu | Revisar preço máximo |
| Risco aumentou | Abrir DD |
| Pendência resolveu | Retomar análise |
| Capital liberou | Reordenar ranking |
| Tese perdeu força | Reduzir prioridade |
| Tese inválida | Encerrar monitoramento |


# 31. Regras de Negócio


| ID | Regra | Resultado |
|---|---|---|
| MON23-001 | Mudança crítica de risco | BLOCK/reavaliar |
| MON23-002 | Mudança material de preço | Recalcular |
| MON23-003 | Valuation materialmente alterado | Recalcular |
| MON23-004 | Liquidez abaixo do mínimo | Reavaliar |
| MON23-005 | Pendência resolvida | Reavaliar |
| MON23-006 | Estratégia alterada | Recalcular Fit |
| MON23-007 | Capital alterado | Recalcular prioridade |
| MON23-008 | Alerta deve ser acionável | Obrigatório |
| MON23-009 | Mudanças relacionadas devem ser agrupadas | Evitar fadiga |
| MON23-010 | Decisões antigas não podem ser sobrescritas | Preservar histórico |
| MON23-011 | Regra crítica não pode ser alterada sem governança | Bloquear mudança |
| MON23-012 | Resultado real deve alimentar backtest | Aprendizado |


# 32. Critérios de Aceite

- CA-D23 — O Radar monitora oportunidades após a análise inicial.
- CA-D23 — Existe materialidade configurável.
- CA-D23 — Eventos críticos podem bloquear imediatamente.
- CA-D23 — Eventos relevantes provocam reavaliação.
- CA-D23 — Reavaliações podem ser parciais ou completas.
- CA-D23 — Alertas possuem prioridade.
- CA-D23 — Alertas apresentam impacto e ação recomendada.
- CA-D23 — Existe mecanismo para evitar fadiga de alertas.
- CA-D23 — BUY IF possui gatilhos objetivos.
- CA-D23 — MONITORING possui gatilhos de reentrada.
- CA-D23 — É possível abandonar uma tese com motivo.
- CA-D23 — Resultados reais podem ser registrados.
- CA-D23 — Previsto e realizado podem ser comparados.
- CA-D23 — Existe backtest.
- CA-D23 — Existe medição de falsos positivos e negativos.
- CA-D23 — Pesos e regras podem ser calibrados.
- CA-D23 — Alterações de regras possuem versão e justificativa.
- CA-D23 — O aprendizado não elimina governança.
- CA-D23 — O histórico de decisões é preservado.
- CA-D23 — O Radar pode melhorar com resultados reais sem perder explicabilidade.

# 33. Relação com os Documentos


| Documento | Relação |
|---|---|
| 7 — Workflow | Fornece estados e eventos. |
| 8 — Parâmetros | Fornece gatilhos e limites. |
| 14 — Dados | Fornece qualidade e histórico. |
| 15 — Decisão | Define consequências. |
| 18 — Economia | Fornece métricas previstas/realizadas. |
| 19 — Risco | Fornece gatilhos críticos. |
| 20 — Liquidez | Fornece sinais de demanda/saída. |
| 21 — Investidor | Fornece capital e estratégia. |
| 22 — Ranking | Recebe as reavaliações e mudanças. |
| 23 | Fecha o ciclo de aprendizado. |


# 34. Visão Consolidada do Radar

O Radar passa a operar como um ciclo contínuo:
DESCOBRIR → ENTENDER → VALORIZAR → CALCULAR → FILTRAR → PONTUAR → RANQUEAR → ANALISAR → VALIDAR → DECIDIR → MONITORAR → MEDIR → APRENDER → MELHORAR
A grande diferença é que o sistema não termina na decisão. Cada operação gera conhecimento para melhorar as próximas decisões.

# 35. Próximo Documento

Recomendação: Documento 24 — Governança, Auditoria, Versionamento e Gestão do Conhecimento do Radar. O foco será consolidar quem pode alterar regras, como decisões são auditadas, como versões de parâmetros são controladas, como evidências são preservadas e como o conhecimento acumulado do Radar se torna patrimônio do produto.
