# Radar_Imobiliario_Documento_26_MVP_Plano_Construcao_Versao_1_Final_Funcional_v1.1

🏠 RADAR IMOBILIÁRIO
Documento 26
Especificação Funcional do MVP e Plano de Construção da Primeira Versão
FECHAMENTO DA FASE FUNCIONAL | Versão 1.0
DO DADO À DECISÃO — PRIMEIRA VERSÃO OPERACIONAL

# 1. Objetivo

Este documento fecha a especificação funcional inicial do Radar Imobiliário e define, de forma objetiva, o que precisa existir na primeira versão operacional, o que fica deliberadamente fora, qual fluxo mínimo comprova o valor do produto e quais critérios determinam que o MVP está realmente pronto.
O foco é encerrar a fase de descoberta funcional. A partir deste documento, novas necessidades devem ser tratadas como evolução, não como motivo para reabrir indefinidamente o escopo-base.

# 2. Decisão de Produto

O MVP NÃO será um portal imobiliário completo. Também não será apenas um coletor de anúncios. O MVP será uma máquina funcional de descoberta, análise e priorização de oportunidades imobiliárias.

| MVP precisa provar | MVP não precisa provar |
|---|---|
| Encontrar uma oportunidade real | Cobrir todos os bancos |
| Consolidar o imóvel | Ter todos os tipos de imóvel |
| Estimar valor de mercado | Ter todos os mercados |
| Calcular custo econômico | Automatizar toda Due Diligence |
| Avaliar risco/liquidez | Ter todos os canais de alerta |
| Aplicar estratégia | Ter todos os modelos de score |
| Ranquear | Ter aprendizado avançado |
| Explicar | Ter operação em escala |
| Registrar decisão | Ter arquitetura técnica definitiva |


# 3. Hipótese que o MVP Deve Validar

Se o Radar conseguir transformar uma oferta real em uma oportunidade economicamente fundamentada, explicar por que ela é interessante, mostrar riscos e pendências, comparar com alternativas e permitir uma decisão rastreável, então existe valor real no produto.

| Hipótese | Métrica de prova |
|---|---|
| Encontramos oportunidades reais | Oportunidades qualificadas |
| Valuation melhora a decisão | Diferença entre preço e valor |
| Custo econômico evita falsas oportunidades | Desconto líquido/margem |
| Risco evita erros | Riscos identificados antes da decisão |
| Ranking economiza tempo | Tempo até encontrar Top 3 |
| Explicabilidade gera confiança | Decisões justificadas |
| Histórico gera aprendizado | Previsto × realizado |


# 4. Usuário Principal do MVP

Investidor/analista que procura imóveis com desconto real e quer decidir onde concentrar tempo e capital.
- Configura preferências.
- Recebe oportunidades.
- Analisa rapidamente.
- Aprofunda as melhores.
- Registra decisão.
- Acompanha mudanças.

# 5. Escopo P0 — Obrigatório


| ID | Capacidade | Obrigatório |
|---|---|---|
| P0-01 | Fonte e captura | Sim |
| P0-02 | Normalização | Sim |
| P0-03 | Identificação do imóvel | Sim |
| P0-04 | Deduplicação básica | Sim |
| P0-05 | Perfil consolidado | Sim |
| P0-06 | Comparáveis | Sim |
| P0-07 | Valuation | Sim |
| P0-08 | Custo econômico total | Sim |
| P0-09 | Desconto/margem | Sim |
| P0-10 | Risco básico | Sim |
| P0-11 | Liquidez básica | Sim |
| P0-12 | Estratégia | Sim |
| P0-13 | Regras | Sim |
| P0-14 | Opportunity Score | Sim |
| P0-15 | Investor Fit | Sim |
| P0-16 | Ranking | Sim |
| P0-17 | Explicabilidade | Sim |
| P0-18 | Análise profunda | Sim |
| P0-19 | Pendências/evidências | Sim |
| P0-20 | Decisão | Sim |
| P0-21 | Histórico | Sim |
| P0-22 | Monitoramento básico | Sim |


# 6. Fonte Inicial

A primeira fonte operacional pode ser a Caixa, mantendo o modelo funcional preparado para expansão posterior.
- A fonte deve possuir identidade própria.
- Cada captura deve preservar o conteúdo original.
- Uma mesma oportunidade pode aparecer em capturas diferentes.
- Nova fonte deve entrar sem mudar a lógica central do Radar.

# 7. Escopo P1 — Depois do MVP


| Capacidade | Prioridade |
|---|---|
| Novas fontes/bancos | P1 |
| Mais automações de enriquecimento | P1 |
| Alertas avançados | P1 |
| Monitoramento mais sofisticado | P1 |
| Mais estratégias | P1 |
| Backtest ampliado | P1 |
| Modelos de liquidez mais sofisticados | P1 |
| Comparação avançada de portfólio | P1 |
| Relatórios avançados | P1 |


# 8. Escopo P2 — Evolução

- Aprendizado estatístico avançado.
- Predições mais sofisticadas.
- Expansão ampla de mercados.
- Modelos específicos por submercado.
- Automação de Due Diligence.
- Inteligência avançada de documentos.
- Novos canais de comunicação.
- Recursos colaborativos.

# 9. Fora do MVP


| Item | Motivo |
|---|---|
| Todos os bancos | Validação primeiro |
| Todos os portais | Complexidade desnecessária |
| Aplicativo completo | Não necessário para provar valor |
| Automação jurídica completa | DD inicial pode ser assistida |
| Machine Learning avançado | Precisa de histórico |
| Execução automática de compra | Risco excessivo |
| Gestão patrimonial completa | Escopo posterior |
| Marketplace | Fora da tese central |
| Arquitetura técnica definitiva | Após validação funcional |


# 10. Fluxo Ponta a Ponta do MVP

FONTE → CAPTURA → NORMALIZAÇÃO → IDENTIFICAÇÃO → DEDUPLICAÇÃO → QUALIFICAÇÃO → PERFIL → COMPARÁVEIS → VALUATION → CUSTO → RISCO → LIQUIDEZ → ESTRATÉGIA → REGRAS → SCORE → FIT → RANKING → EXPLICAÇÃO → ANÁLISE → DD → DECISÃO → HISTÓRICO → MONITORAMENTO

# 11. Fluxo 1 — Descoberta

- Receber captura.
- Preservar dados originais.
- Normalizar campos.
- Identificar imóvel.
- Verificar duplicidade.
- Consolidar perfil.
- Aplicar elegibilidade.
- Criar oportunidade quando houver tese potencial.

# 12. Fluxo 2 — Valuation

- Selecionar comparáveis.
- Avaliar qualidade dos comparáveis.
- Ajustar diferenças relevantes.
- Calcular faixa de valor.
- Definir cenário conservador/base/otimista.
- Calcular confiança.
- Determinar preço máximo por estratégia.

# 13. Fluxo 3 — Economia

- Preço de aquisição.
- Custos de aquisição.
- Dívidas/responsabilidades quando aplicáveis.
- Regularização.
- Reforma.
- Contingência.
- Carregamento.
- Financiamento.
- Saída.
- Calcular custo econômico.
- Calcular desconto líquido.
- Calcular margem.
- Calcular retorno/yield conforme estratégia.

# 14. Fluxo 4 — Risco e Liquidez


| Risco | Liquidez |
|---|---|
| Matrícula | Demanda |
| Ocupação | Oferta |
| Jurídico | Concorrência |
| Débitos | Ticket |
| Físico | Financiabilidade |
| Execução | Prazo de saída |
| Incerteza | Preço de saída |


# 15. Fluxo 5 — Estratégia e Score

O MVP deve permitir pelo menos:
- Renda.
- Revenda.
- Valorização.
- MCMV/baixa renda.
- Terreno.
- Estratégia configurável.
O Opportunity Score e o Investor Fit devem permanecer separados.

# 16. Fluxo 6 — Ranking

O ranking deve combinar:
- Qualidade econômica.
- Aderência.
- Confiança.
- Risco.
- Liquidez.
- Capital.
- Concentração.
Resultado: uma fila priorizada de oportunidades, não uma lista genérica.

# 17. Fluxo 7 — Análise Profunda


| Etapa | Resultado |
|---|---|
| Identificação | Imóvel confirmado |
| Documentação | Situação conhecida |
| Ocupação | Situação conhecida |
| Jurídico | Riscos identificados |
| Condomínio/IPTU | Custos conhecidos |
| Físico | Reforma estimada |
| Mercado | Preço validado |
| Economia | Cenários |
| Pendências | Lista objetiva |
| Decisão | BUY/BUY IF/MONITOR/DO NOT BUY/BLOCK |


# 18. Fluxo 8 — Decisão


| Decisão | Significado |
|---|---|
| BUY | Comprar |
| BUY IF | Comprar se condição objetiva for satisfeita |
| MONITOR | Manter tese viva |
| DO NOT BUY | Não comprar por razão econômica/estratégica |
| BLOCK | Impedimento crítico |


# 19. Explicabilidade Obrigatória

Toda oportunidade recomendada deve responder:
- Por que apareceu?
- Por que está barata?
- Quanto vale?
- Quanto realmente custa?
- Qual é o desconto líquido?
- Qual é a margem?
- Qual é o risco?
- Qual é a liquidez?
- Para qual estratégia serve?
- Por que é adequada ao investidor?
- O que ainda precisa ser confirmado?
- O que faria a tese deixar de ser válida?

# 20. Tela/Visão Mínima do MVP


| Visão | Conteúdo |
|---|---|
| Dashboard | Resumo e Top oportunidades |
| Radar | Lista/ranking filtrável |
| Oportunidade | Ficha completa |
| Mercado | Comparáveis/valuation |
| Economia | Custos/margem/cenários |
| Risco/DD | Riscos/evidências/pendências |
| Decisão | Resultado e justificativa |
| Histórico | Linha do tempo |
| Configuração | Perfil/estratégias/regras |


# 21. Dados Mínimos por Oportunidade


| Grupo | Campos essenciais |
|---|---|
| Identidade | Endereço, matrícula quando disponível, fonte |
| Oferta | Preço, status, data |
| Perfil | Tipo, área, dormitórios, vagas |
| Mercado | Comparáveis, valor estimado |
| Economia | Custos, custo total, margem |
| Risco | Riscos/pêndencias |
| Liquidez | Demanda, prazo estimado |
| Estratégia | Estratégias aderentes |
| Score | Opportunity Score |
| Fit | Investor Fit |
| Confiança | Nível |
| Decisão | Status + justificativa |


# 22. Regras Mínimas do MVP


| ID | Regra |
|---|---|
| MVP-001 | BLOCK sempre prevalece. |
| MVP-002 | Desconhecido reduz confiança. |
| MVP-003 | Preço sozinho não define oportunidade. |
| MVP-004 | Desconto deve considerar custo econômico. |
| MVP-005 | Valuation deve possuir confiança. |
| MVP-006 | Liquidez influencia decisão. |
| MVP-007 | Risco crítico pode bloquear. |
| MVP-008 | Estratégia altera critérios. |
| MVP-009 | Fit é separado do Opportunity Score. |
| MVP-010 | Ranking deve ser explicável. |
| MVP-011 | Decisão deve preservar evidências. |
| MVP-012 | Histórico não deve ser sobrescrito. |
| MVP-013 | BUY IF exige condição objetiva. |
| MVP-014 | MONITOR exige gatilho de reentrada. |
| MVP-015 | Regra/parâmetro relevante possui versão. |


# 23. Critérios de Pronto — MVP

- CA-MVP — Uma oportunidade real pode entrar no Radar.
- CA-MVP — O Radar preserva a captura original.
- CA-MVP — O imóvel pode ser identificado e consolidado.
- CA-MVP — Duplicidades podem ser tratadas.
- CA-MVP — Existem comparáveis.
- CA-MVP — Existe valuation com confiança.
- CA-MVP — O custo econômico total pode ser calculado.
- CA-MVP — Desconto líquido e margem são calculados.
- CA-MVP — Risco pode ser registrado.
- CA-MVP — Liquidez pode ser avaliada.
- CA-MVP — Estratégia pode ser selecionada.
- CA-MVP — Regras podem eliminar oportunidades.
- CA-MVP — Opportunity Score é calculado.
- CA-MVP — Investor Fit é calculado.
- CA-MVP — Oportunidades são ranqueadas.
- CA-MVP — O ranking é explicável.
- CA-MVP — É possível abrir análise profunda.
- CA-MVP — É possível registrar pendências e evidências.
- CA-MVP — É possível registrar decisão.
- CA-MVP — É possível acompanhar histórico.
- CA-MVP — Uma oportunidade pode voltar ao ranking após mudança.
- CA-MVP — Uma operação completa pode ser reconstruída depois.

# 24. Definition of Done Funcional


| Condição | Obrigatória |
|---|---|
| Fluxo ponta a ponta funcionando | Sim |
| Dados reais | Sim |
| Resultado econômico | Sim |
| Valuation | Sim |
| Risco | Sim |
| Liquidez | Sim |
| Estratégia | Sim |
| Ranking | Sim |
| Explicabilidade | Sim |
| Decisão | Sim |
| Histórico | Sim |
| Teste de cenário negativo | Sim |
| Auditoria básica | Sim |


# 25. Cenários de Aceite Positivos


| Cenário | Resultado esperado |
|---|---|
| Grande desconto + boa liquidez + baixo risco | Alta prioridade |
| Desconto médio + excelente liquidez + Fit alto | Pode superar desconto maior |
| Preço baixo + custo alto | Não classificar como grande oportunidade |
| Boa margem + risco crítico | BLOCK |
| Boa oportunidade + dados insuficientes | Confiança reduzida |
| Preço caiu materialmente | Ranking recalculado |
| Pendência resolvida | Reavaliar |
| Estratégia alterada | Fit recalculado |


# 26. Cenários Negativos Obrigatórios


| Cenário | Comportamento |
|---|---|
| Duplicidade falsa | Não consolidar irreversivelmente |
| Mesmo imóvel em duas fontes | Uma identidade, múltiplas capturas |
| Sem comparáveis | Reduzir confiança |
| Custo de reforma desconhecido | Não assumir zero |
| Risco jurídico crítico | BLOCK |
| Preço abaixo do mercado, mas baixa liquidez | Exigir margem/monitorar |
| Score alto + Fit baixo | Não priorizar |
| Capital indisponível | BLOCK operacional |
| Informação futura em backtest | Não utilizar |
| Regra alterada | Nova versão |


# 27. Plano de Construção Funcional


| Fase | Objetivo | Saída |
|---|---|---|
| F0 | Preparação | Perfil + parâmetros + fonte |
| F1 | Descoberta | Captura → imóvel |
| F2 | Inteligência | Comparáveis → valuation |
| F3 | Economia | Custo → margem |
| F4 | Decisão | Risco + liquidez + estratégia + score |
| F5 | Ranking | Fila priorizada |
| F6 | Análise | DD + decisão |
| F7 | Ciclo | Histórico + monitoramento |


# 28. Ordem de Construção Recomendada

- Começar com um único mercado e uma única fonte.
- Conseguir capturar uma oportunidade real.
- Consolidar corretamente o imóvel.
- Calcular valuation.
- Calcular custo econômico.
- Aplicar regras.
- Calcular score e Fit.
- Criar ranking.
- Explicar a oportunidade.
- Executar análise profunda.
- Registrar decisão.
- Reavaliar após mudança.
Só depois expandir cobertura.

# 29. Estratégia de Validação


| Etapa | Pergunta |
|---|---|
| Semana/iteração inicial | Conseguimos encontrar algo realmente interessante? |
| Valuation | Nossa estimativa é defensável? |
| Economia | Os custos evitam falsos descontos? |
| Ranking | As melhores aparecem primeiro? |
| DD | Encontramos riscos relevantes? |
| Decisão | O usuário consegue decidir mais rápido? |
| Resultado | As previsões se confirmam? |


# 30. Métricas do MVP


| Indicador | Objetivo |
|---|---|
| Oportunidades capturadas | Cobertura |
| Oportunidades qualificadas | Qualidade |
| Top 10 úteis | Precisão prática |
| Tempo até Top 3 | Eficiência |
| Falsos positivos | Reduzir |
| Falsos negativos | Reduzir |
| Erro de valuation | Calibrar |
| Erro de custo | Calibrar |
| Erro de prazo | Calibrar |
| Decisões justificadas | 100% |
| Decisões reproduzíveis | 100% |


# 31. O que significa “Fechar” o Produto Funcional

Fechar a fase funcional NÃO significa afirmar que o produto nunca mais mudará. Significa que existe agora uma definição suficientemente completa para construir, testar, medir e aprender sem continuar reinventando o conceito.

| Agora | Depois |
|---|---|
| Construir | Evoluir |
| Testar hipótese | Calibrar |
| Medir resultado | Aprender |
| Corrigir defeitos | Criar novas versões |
| Preservar regras | Propor melhorias |


# 32. Regra de Controle de Escopo

Qualquer nova ideia deve ser classificada como:

| Categoria | Tratamento |
|---|---|
| P0 obrigatório | Entra no MVP |
| P1 importante | Backlog pós-MVP |
| P2 evolução | Roadmap |
| Experimento | Testar separadamente |
| Fora da tese | Não entra |
| Mudança estrutural | Revisar impacto antes de alterar base |

Isso evita que o projeto fique indefinidamente aberto.

# 33. Checklist Executivo Final

- ✓ Temos uma definição clara de oportunidade.
- ✓ Temos uma definição clara de imóvel.
- ✓ Temos valuation.
- ✓ Temos custo econômico.
- ✓ Temos risco.
- ✓ Temos liquidez.
- ✓ Temos estratégias.
- ✓ Temos regras parametrizáveis.
- ✓ Temos score.
- ✓ Temos Investor Fit.
- ✓ Temos ranking.
- ✓ Temos explicabilidade.
- ✓ Temos Due Diligence.
- ✓ Temos decisões.
- ✓ Temos monitoramento.
- ✓ Temos histórico.
- ✓ Temos governança.
- ✓ Temos backtest.
- ✓ Temos aprendizado.
- ✓ Temos MVP definido.
- ✓ Temos critérios de aceite.
- ✓ Temos ordem de construção.
- ✓ Temos controle de escopo.

# 34. Mapa Final dos 26 Documentos


| Bloco | Documentos | O que foi fechado |
|---|---|---|
| Fundamentos | 1–4 | Negócio, regras, valuation, DD |
| Requisitos | 5–7 | Requisitos, dados, workflow |
| Parametrização | 8–10 | Parâmetros, módulos, especificação |
| Experiência | 11–13 | Telas, rastreabilidade, roadmap |
| Dados/Decisão | 14–18 | Dados, regras, captura, valuation, economia |
| Risco/Saída | 19–20 | Risco, DD, liquidez, saída |
| Investidor/Ranking | 21–22 | Portfólio, capital, ranking |
| Ciclo/Conhecimento | 23–24 | Monitoramento, aprendizado, governança |
| Consolidação | 25 | Mapa funcional completo |
| Execução | 26 | MVP e fechamento funcional |


# 35. Definição Final do Produto

O Radar Imobiliário é uma plataforma de inteligência de oportunidades que captura informações imobiliárias, identifica e consolida imóveis, estima valor de mercado, calcula custo econômico, avalia risco e liquidez, aplica estratégias e regras do investidor, ranqueia oportunidades, explica suas conclusões, conduz análise profunda, registra decisões, monitora mudanças e aprende com os resultados.
Não procure imóveis baratos. Deixe o Radar encontrar imóveis que estejam realmente baratos.
Preço é o dado. Oportunidade é a análise.

# 36. Fechamento da Fase Funcional

Com este Documento 26, a especificação funcional-base do Radar está fechada. Os documentos 1 a 26 formam um conjunto coerente de referência para construção e validação.
A partir daqui, o projeto deve sair do ciclo de “definir o que é” e entrar no ciclo de “construir → testar → medir → aprender → evoluir”.
Novas descobertas de negócio continuam permitidas, mas devem entrar como evolução versionada, preservando a base já definida.

# 37. Próxima Fase

A próxima fase deixa de ser uma nova rodada de documentos conceituais. É a execução: transformar este escopo funcional fechado em backlog de implementação, priorização de entregas, protótipo/primeiro fluxo real, testes com oportunidades reais e validação da hipótese de produto.
O primeiro objetivo operacional deve ser simples: pegar uma oportunidade imobiliária real e fazê-la percorrer o Radar inteiro, do dado bruto até uma decisão explicável.
ADENDO v1.1 — NOVO GATE P0: VALIDADE JURÍDICA DO LEILÃO/ATIVO
A validade jurídica do procedimento passa a ser capacidade P0 do MVP.
Fluxo MVP atualizado: FONTE → CAPTURA → NORMALIZAÇÃO → IDENTIFICAÇÃO → DEDUPLICAÇÃO → QUALIFICAÇÃO → PERFIL → VALIDADE JURÍDICA → COMPARÁVEIS → VALUATION → CUSTO → RISCO → LIQUIDEZ → ESTRATÉGIA → REGRAS → SCORE → FIT → RANKING → EXPLICAÇÃO → ANÁLISE → DD → DECISÃO → HISTÓRICO → MONITORAMENTO.
O MVP deve ser capaz de detectar e classificar: consolidação não comprovada; inconsistência de matrícula; ausência/insuficiência de evidência de notificação/intimação; inconsistências entre edital e matrícula; processos com potencial impacto sobre a validade; ocupação/locação relevante.
Critério de aceite: nenhuma oportunidade com BLOCK jurídico pode aparecer como BUY, independentemente do score.
Critério de aceite: ausência de evidência deve reduzir confiança e gerar PENDENTE/INCONCLUSIVO, nunca ser tratada como regularidade.
