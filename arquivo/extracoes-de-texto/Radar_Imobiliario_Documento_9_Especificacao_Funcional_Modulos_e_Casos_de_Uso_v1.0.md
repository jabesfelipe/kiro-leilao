# Radar_Imobiliario_Documento_9_Especificacao_Funcional_Modulos_e_Casos_de_Uso_v1.0

🎯
RADAR IMOBILIÁRIO
Documento 9 — Especificação Funcional dos Módulos e Casos de Uso
Versão 1.0 | Documento de Negócio

# 1. Objetivo

Transformar os documentos de negócio anteriores em uma especificação funcional concreta, descrevendo módulos, funcionalidades, atores, entradas, saídas, regras, estados, alertas e critérios de aceite. Este documento permanece deliberadamente independente de tecnologia e arquitetura.

# 2. Princípio do Produto

O Radar deve reduzir o trabalho de encontrar, comparar, analisar e acompanhar oportunidades imobiliárias, aumentando a qualidade da decisão sem substituir o julgamento do investidor.
Frase central: “Não procure imóveis baratos. Deixe o Radar encontrar imóveis que estejam realmente baratos.”

# 3. Atores


| Ator | Responsabilidade |
|---|---|
| Investidor | Define preferências, acompanha oportunidades e toma decisões. |
| Analista | Investiga dados, valida evidências e conduz due diligence. |
| Gestor | Define estratégias, regras, pesos e governança. |
| Fonte | Origina oportunidades e informações. |
| Radar | Executa qualificação, enriquecimento, valuation, score, ranking e monitoramento. |


# 4. Macro Jornada Funcional

FONTES → CAPTURA → NORMALIZAÇÃO → DEDUPLICAÇÃO → PERFIL → ENRIQUECIMENTO → VALUATION → ECONOMIA → ESTRATÉGIAS → REGRAS → SCORE → RANKING → ANÁLISE → DUE DILIGENCE → DECISÃO → MONITORAMENTO → HISTÓRICO → BACKTEST

# 5. Módulos Funcionais


| ID | Módulo | Função |
|---|---|---|
| MOD-01 | Fontes | Cadastrar e administrar origens de oportunidades e dados. |
| MOD-02 | Captura | Registrar cada ocorrência/snapshot recebida de uma fonte. |
| MOD-03 | Normalização | Padronizar dados de diferentes origens. |
| MOD-04 | Deduplicação | Identificar ocorrências do mesmo imóvel/oportunidade. |
| MOD-05 | Perfil do imóvel | Consolidar características físicas e documentais. |
| MOD-06 | Localização | Avaliar contexto geográfico e mercadológico. |
| MOD-07 | Mercado | Pesquisar e administrar evidências de mercado. |
| MOD-08 | Valuation | Estimar valor de mercado e confiança. |
| MOD-09 | Economia | Calcular custo total, margem, desconto e cenários. |
| MOD-10 | Estratégias | Definir objetivos e critérios por estratégia. |
| MOD-11 | Regras | Aplicar hard, soft e condicionais. |
| MOD-12 | Score | Priorizar oportunidades. |
| MOD-13 | Ranking/Radar | Exibir oportunidades priorizadas. |
| MOD-14 | Análise profunda | Permitir investigação estruturada. |
| MOD-15 | Due Diligence | Controlar evidências, pendências e validações. |
| MOD-16 | Workflow | Controlar estados e transições. |
| MOD-17 | Alertas | Comunicar eventos relevantes. |
| MOD-18 | Monitoramento | Reavaliar oportunidades após mudanças. |
| MOD-19 | Histórico | Preservar evolução de dados e decisões. |
| MOD-20 | Relatórios | Produzir visão executiva e analítica. |
| MOD-21 | Backtest | Avaliar regras, pesos e resultados históricos. |
| MOD-22 | Governança | Controlar parâmetros, versões e auditoria. |


# 6. Requisitos Funcionais por Módulo


| ID | Módulo | Requisito |
|---|---|---|
| RF-031 | Fontes | Permitir cadastrar, ativar, desativar e classificar fontes. |
| RF-032 | Captura | Preservar o conteúdo original recebido. |
| RF-033 | Captura | Registrar data/hora e status da captura. |
| RF-034 | Normalização | Converter diferentes formatos para um perfil comum. |
| RF-035 | Deduplicação | Detectar possíveis duplicidades e consolidar ocorrências. |
| RF-036 | Imóvel | Manter identificação física/documental do imóvel. |
| RF-037 | Perfil | Permitir dados desconhecidos sem preenchê-los artificialmente. |
| RF-038 | Localização | Classificar localização conforme parâmetros vigentes. |
| RF-039 | Mercado | Registrar comparáveis e sua qualidade. |
| RF-040 | Valuation | Calcular valor conservador, base e otimista. |
| RF-041 | Valuation | Informar confiança da estimativa. |
| RF-042 | Economia | Calcular custo econômico total. |
| RF-043 | Economia | Calcular desconto, margem e retorno. |
| RF-044 | Estratégia | Permitir múltiplas estratégias para o mesmo imóvel. |
| RF-045 | Regras | Aplicar regras globais e específicas. |
| RF-046 | Regras | Explicar regras que eliminaram ou penalizaram. |
| RF-047 | Score | Calcular score por estratégia. |
| RF-048 | Ranking | Ordenar oportunidades por relevância. |
| RF-049 | Análise | Permitir registrar tese e contrapontos. |
| RF-050 | Due Diligence | Controlar checklist, evidências e pendências. |
| RF-051 | Workflow | Controlar estados e transições. |
| RF-052 | Alertas | Gerar alertas por eventos configurados. |
| RF-053 | Monitoramento | Reprocessar quando houver mudança material. |
| RF-054 | Histórico | Preservar versões das análises. |
| RF-055 | Relatórios | Gerar visão resumida e detalhada. |
| RF-056 | Backtest | Comparar resultados das configurações. |
| RF-057 | Governança | Versionar regras e parâmetros. |
| RF-058 | Governança | Registrar justificativa de exceções. |


# 7. Casos de Uso Principais


| ID | Caso de uso | Ator | Resultado |
|---|---|---|---|
| UC-001 | Configurar perfil | Investidor | Define capital, ticket, risco, liquidez e objetivos. |
| UC-002 | Configurar estratégia | Gestor/Investidor | Define critérios e pesos. |
| UC-003 | Cadastrar localização | Investidor | Define regiões prioritárias, aceitáveis e bloqueadas. |
| UC-004 | Receber oportunidade | Radar | Registra nova captura. |
| UC-005 | Consolidar imóvel | Radar | Relaciona capturas ao imóvel. |
| UC-006 | Qualificar oportunidade | Radar | Aplica regras de elegibilidade. |
| UC-007 | Valorar imóvel | Radar | Estima valor de mercado. |
| UC-008 | Calcular tese econômica | Radar | Calcula custo, margem, yield e cenários. |
| UC-009 | Pontuar oportunidade | Radar | Calcula score e confiança. |
| UC-010 | Consultar ranking | Investidor | Visualiza melhores oportunidades. |
| UC-011 | Analisar oportunidade | Investidor/Analista | Investiga tese e riscos. |
| UC-012 | Executar due diligence | Analista | Valida documentação, dívidas, ocupação e físico. |
| UC-013 | Tomar decisão | Investidor | Compra, compra condicional, monitora ou rejeita. |
| UC-014 | Acompanhar oportunidade | Investidor | Mantém tese em monitoramento. |
| UC-015 | Receber alerta | Investidor | Recebe evento acionável. |
| UC-016 | Reavaliar oportunidade | Radar | Atualiza valuation/economia/score. |
| UC-017 | Consultar histórico | Investidor/Analista | Compara evolução temporal. |
| UC-018 | Calibrar regras | Gestor | Executa backtest e ajusta parâmetros. |


# 8. Tela Conceitual da Oportunidade

A ficha da oportunidade deve responder rapidamente: O que é? Por que é interessante? Quanto vale? Quanto custa de verdade? Qual o risco? Para qual estratégia serve? O que falta confirmar? O que faria a tese deixar de ser válida?

| Bloco | Informações |
|---|---|
| Identificação | Imóvel, fonte, captura, localização, status |
| Preço | Preço atual, histórico, avaliação da fonte |
| Mercado | Valor estimado, comparáveis, confiança |
| Economia | Custo total, desconto líquido, margem |
| Renda | Aluguel, yield, vacância, cenário |
| Liquidez | Score, prazo estimado, demanda |
| Risco | Categorias, severidade, pendências |
| Estratégias | Fit e score por estratégia |
| Decisão | Status, tese, recomendação |
| Evidências | Documentos, fontes e confirmações |
| Histórico | Alterações e decisões |


# 9. Fluxo de Qualificação

1. Capturar → 2. Normalizar → 3. Identificar imóvel → 4. Deduplicar → 5. Validar dados mínimos → 6. Aplicar bloqueios → 7. Valorar → 8. Calcular custo econômico → 9. Avaliar estratégias → 10. Pontuar → 11. Classificar → 12. Alertar/rankear.
Se houver bloqueio crítico, a oportunidade pode ser interrompida antes das etapas posteriores. Se faltar informação importante, o Radar deve indicar pendência e reduzir a confiança.

# 10. Fluxo de Análise Profunda

SELECIONAR → FORMULAR TESE → VALIDAR MERCADO → VALIDAR CUSTOS → VALIDAR DOCUMENTAÇÃO → VALIDAR OCUPAÇÃO → VALIDAR FÍSICO → TESTAR CENÁRIOS → REAVALIAR SCORE → DECIDIR

| Resultado | Significado |
|---|---|
| BUY | Tese validada e risco aceitável. |
| BUY IF | Compra condicionada a requisitos objetivos. |
| MONITOR | Tese interessante, mas ainda não pronta. |
| DO NOT BUY | Tese não atende aos critérios. |
| BLOCK | Risco crítico ou impeditivo. |


# 11. Critérios de Aceite Essenciais


| ID | Critério de aceite |
|---|---|
| CA-001 | Uma oportunidade nova deve manter sua captura original. |
| CA-002 | O mesmo imóvel pode ter várias capturas sem criar ativos duplicados. |
| CA-003 | Preço não pode ser tratado como valor de mercado automaticamente. |
| CA-004 | Valuation deve possuir evidências e confiança. |
| CA-005 | Custo desconhecido não pode virar zero silenciosamente. |
| CA-006 | Uma mesma oportunidade pode ter scores diferentes por estratégia. |
| CA-007 | Bloqueio crítico sempre prevalece sobre score. |
| CA-008 | Toda recomendação deve ser explicável. |
| CA-009 | Alterações materiais devem gerar reavaliação. |
| CA-010 | Histórico de preço, score, regras e decisão deve ser preservado. |
| CA-011 | Exceções precisam de justificativa e rastreabilidade. |
| CA-012 | Dados vencidos devem afetar confiança ou disparar revalidação. |


# 12. Regras de Negócio Transversais

- Imóvel é permanente; oportunidade é dinâmica.
- Preço é dado; valor de mercado é estimativa.
- Desconto nominal não é suficiente: analisar desconto líquido.
- Score prioriza; não substitui bloqueios.
- Risco e confiança são dimensões distintas.
- Dados desconhecidos devem permanecer explicitamente desconhecidos.
- Uma oportunidade pode ser boa para uma estratégia e ruim para outra.
- Histórico nunca deve ser apagado por atualização.
- Reavaliação deve ocorrer diante de eventos materiais.
- Cada decisão precisa registrar justificativa e evidências.

# 13. Jornada do Investidor


| Etapa | Pergunta do usuário | Resposta do Radar |
|---|---|---|
| Descoberta | O que apareceu de novo? | Novas oportunidades qualificadas. |
| Triagem | Vale olhar? | Score, confiança e explicação. |
| Comparação | Qual é melhor? | Ranking por estratégia. |
| Investigação | Por que é boa? | Tese + evidências + riscos. |
| Validação | É realmente boa? | Due diligence + cenários. |
| Decisão | Compro? | BUY / BUY IF / MONITOR / DO NOT BUY. |
| Acompanhamento | Mudou algo? | Alertas e reavaliação. |
| Aprendizado | Acertamos? | Histórico e backtest. |


# 14. Relatórios Funcionais

- Radar diário de novas oportunidades.
- Ranking por estratégia.
- Ranking por localização.
- Mapa de oportunidades por faixa de score.
- Lista de oportunidades bloqueadas e respectivos motivos.
- Análises em andamento e pendências.
- Alertas críticos.
- Histórico de preço e score.
- Desempenho de oportunidades adquiridas.
- Relatório de calibração das regras.

# 15. Indicadores de Produto


| Indicador | Objetivo |
|---|---|
| Oportunidades capturadas | Medir cobertura. |
| Oportunidades qualificadas | Medir qualidade da triagem. |
| Taxa de falso positivo | Medir precisão. |
| Tempo até análise | Medir produtividade. |
| Tempo até decisão | Medir eficiência. |
| Precisão do valuation | Medir qualidade econômica. |
| Precisão do ranking | Medir qualidade do score. |
| Taxa de alertas úteis | Medir qualidade da comunicação. |
| Retorno realizado | Medir resultado econômico. |
| Taxa de oportunidades bloqueadas | Medir efetividade de proteção. |


# 16. Escopo Inicial Recomendado

Para uma primeira entrega funcional, o Radar deve priorizar o ciclo completo de uma oportunidade, mesmo que com poucas fontes:
- Captura de oportunidades da Caixa.
- Cadastro/configuração do investidor.
- Normalização e identificação do imóvel.
- Valuation básico com comparáveis.
- Cálculo do custo econômico total.
- Aplicação de regras.
- Score por estratégia.
- Ranking.
- Ficha completa da oportunidade.
- Workflow de análise.
- Due diligence estruturada.
- Alertas de mudanças materiais.
- Histórico.
O objetivo do MVP não é cobrir todas as fontes, mas provar o ciclo de decisão de ponta a ponta.

# 17. Fora do Escopo deste Documento

- Arquitetura de software.
- Escolha de linguagem/framework.
- Banco de dados.
- Cloud/infrastructure.
- Mensageria.
- APIs técnicas.
- Detalhes de implementação.

# 18. Próximo Passo

Documento 10 — Especificação Funcional Detalhada dos Módulos, com fluxos, estados, entradas, saídas, regras, exceções e critérios de aceite por funcionalidade. Esse documento será a ponte entre o desenho de negócio e uma futura especificação técnica.
