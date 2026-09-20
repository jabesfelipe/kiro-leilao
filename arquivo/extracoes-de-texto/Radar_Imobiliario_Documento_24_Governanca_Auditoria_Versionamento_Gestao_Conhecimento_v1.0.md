# Radar_Imobiliario_Documento_24_Governanca_Auditoria_Versionamento_Gestao_Conhecimento_v1.0

🏠 RADAR IMOBILIÁRIO
Documento 24
Governança, Auditoria, Versionamento e Gestão do Conhecimento
Especificação Funcional de Negócio | Versão 1.0

# 1. Objetivo

Definir a governança do Radar: quem pode alterar regras e parâmetros, como versões são controladas, como decisões são auditadas, como evidências são preservadas e como o conhecimento acumulado permanece íntegro ao longo do tempo.
- Preservar a história das decisões.
- Permitir reconstruir qualquer decisão passada.
- Controlar mudanças de regras e parâmetros.
- Separar dado original de interpretação.
- Controlar exceções.
- Manter rastreabilidade de evidências.
- Transformar resultados em conhecimento reutilizável.

# 2. Princípio Central

O Radar deve conseguir responder, anos depois, a pergunta: “Por que esta oportunidade foi classificada dessa forma naquela data?”

| Deve ser possível saber | Exemplo |
|---|---|
| Qual dado foi usado | Preço capturado em determinada data |
| Qual valuation | R$ 300 mil, cenário base |
| Quais custos | Custo econômico estimado |
| Quais riscos | Risco jurídico médio |
| Quais regras | Versão das regras vigente |
| Quais pesos | Versão do score |
| Qual estratégia | Renda |
| Qual decisão | BUY IF |
| Qual evidência | Documento/comparável/registro |
| Quem decidiu | Investidor/analista |
| Quando | Data e hora |


# 3. Princípios de Governança

- Histórico não deve ser apagado.
- Correção deve gerar nova versão, não reescrever o passado.
- Regras críticas possuem controle maior.
- Exceções são explícitas.
- Dados observados são separados de estimativas.
- Decisões devem possuir justificativa.
- Alterações relevantes devem possuir motivo.
- Conhecimento derivado deve manter origem.
- Score deve ser reproduzível.
- Automação não elimina responsabilidade.

# 4. Objetos Governados


| Objeto | Controle |
|---|---|
| Fonte | Identidade e confiabilidade |
| Captura | Snapshot original |
| Imóvel | Identidade |
| Valuation | Versão e evidências |
| Custo | Premissas |
| Risco | Severidade e evidências |
| Regra | Versão e vigência |
| Parâmetro | Valor e vigência |
| Estratégia | Versão |
| Score | Fórmula/pesos |
| Decisão | Justificativa |
| Exceção | Autorização |
| Alerta | Gatilho e tratamento |


# 5. Papéis de Governança


| Papel | Responsabilidade |
|---|---|
| Investidor | Define objetivos, limites e decisão final. |
| Analista | Executa análise e registra evidências. |
| Gestor | Aprova mudanças relevantes de negócio. |
| Curador de regras | Mantém catálogo e coerência. |
| Auditor | Verifica rastreabilidade e integridade. |
| Radar | Calcula, registra e apresenta resultados. |

Os papéis são conceituais e podem ser acumulados por uma mesma pessoa em operação individual.

# 6. Níveis de Mudança


| Nível | Exemplo | Governança |
|---|---|---|
| Baixo | Texto, descrição, classificação informativa | Registro |
| Médio | Parâmetro operacional | Revisão |
| Alto | Peso de score | Aprovação |
| Crítico | Regra de bloqueio | Aprovação formal + histórico |


# 7. Versionamento

Toda mudança que possa alterar uma decisão deve gerar uma nova versão.

| Objeto | Exemplo |
|---|---|
| Regra | RISK-001 v1.2 |
| Parâmetro | LIQ-MIN v2.0 |
| Estratégia | RENDA v1.4 |
| Score | SCORE-RENDA v3.1 |
| Valuation | VAL-2026-09-01 |
| Decisão | DEC-2026-09-14 |


# 8. Vigência


| Campo | Função |
|---|---|
| Data de criação | Quando surgiu |
| Data de vigência | Quando passou a valer |
| Data de encerramento | Quando deixou de valer |
| Status | Rascunho/ativo/retirado |
| Motivo | Por que mudou |
| Aprovador | Quem autorizou |


# 9. Reprodutibilidade

Uma decisão histórica deve ser reproduzível com a mesma versão de regras, parâmetros e dados disponíveis na época.
- Não usar automaticamente valores atuais para reconstruir decisão antiga.
- Preservar snapshots relevantes.
- Preservar versões das regras.
- Preservar versão do score.
- Preservar evidências.

# 10. Auditoria da Decisão


| Elemento | Obrigatório |
|---|---|
| Opportunity ID | Sim |
| Data/hora | Sim |
| Status | Sim |
| Score | Sim |
| Fit | Sim |
| Confiança | Sim |
| Valuation | Sim |
| Custo | Sim |
| Risco | Sim |
| Liquidez | Sim |
| Estratégia | Sim |
| Regras aplicadas | Sim |
| Exceções | Quando houver |
| Justificativa | Sim |
| Evidências | Sim |


# 11. Separação entre Fato e Interpretação


| Tipo | Exemplo |
|---|---|
| Observado | Preço informado na fonte |
| Confirmado | Informação validada documentalmente |
| Calculado | Desconto calculado |
| Estimado | Custo de reforma estimado |
| Inferido | Liquidez inferida por evidências |
| Desconhecido | Informação ainda não confirmada |

O Radar nunca deve transformar uma inferência em fato sem evidência.

# 12. Evidência

Toda conclusão relevante deve possuir evidência suficiente para sustentar a afirmação.

| Qualidade | Tratamento |
|---|---|
| Forte | Pode sustentar decisão |
| Boa | Sustenta com ressalvas |
| Moderada | Exige confirmação |
| Fraca | Reduz confiança |
| Ausente | Permanece desconhecido |


# 13. Trilha de Auditoria

A trilha deve registrar eventos importantes:
- Captura criada.
- Imóvel identificado.
- Fontes associadas.
- Duplicidade resolvida.
- Valuation alterado.
- Risco criado/resolvido.
- Regra aplicada.
- Score alterado.
- Ranking alterado.
- Alerta emitido.
- Decisão registrada.
- Exceção criada.
- Parâmetro alterado.
- Resultado real registrado.

# 14. Exceções

Exceção não significa ignorar a regra. Significa permitir conscientemente uma condição fora do padrão.

| Exceção | Registro |
|---|---|
| Motivo | Obrigatório |
| Regra afetada | Obrigatório |
| Valor normal | Obrigatório |
| Valor excepcional | Obrigatório |
| Risco aceito | Obrigatório |
| Validade | Obrigatório |
| Responsável | Obrigatório |
| Evidência | Quando aplicável |


# 15. Regras de Exceção

- Exceção não pode ocultar BLOCK crítico sem autorização adequada.
- Exceção deve possuir prazo/escopo.
- Exceção deve aparecer na explicabilidade.
- Exceção deve influenciar auditoria.
- Exceções recorrentes devem provocar revisão da regra.

# 16. Conflito entre Regras


| Conflito | Precedência |
|---|---|
| BLOCK × score | BLOCK |
| Elegibilidade × score | Elegibilidade |
| Risco crítico × oportunidade | Risco crítico |
| Estratégia × score | Estratégia |
| Parâmetro específico × global | Mais específico |
| Exceção válida × regra padrão | Exceção dentro do escopo |


# 17. Hierarquia de Parâmetros

Global → Investidor → Estratégia → Localização → Tipo de imóvel → Oportunidade → Exceção
Quanto mais específico o contexto, maior a prioridade, desde que respeitados bloqueios superiores.

# 18. Governança do Score


| Mudança | Tratamento |
|---|---|
| Peso menor | Registro |
| Peso relevante | Revisão |
| Mudança de fórmula | Aprovação |
| Novo componente | Backtest |
| Mudança de classificação | Backtest + aprovação |
| Mudança que afeta BLOCK | Governança crítica |


# 19. Gestão do Conhecimento

O Radar deve acumular conhecimento estruturado, não apenas dados.

| Conhecimento | Exemplo |
|---|---|
| Mercado | Faixa de preço com maior liquidez |
| Tipo | 1 dormitório com alta demanda em determinada região |
| Reforma | Estimativas historicamente subestimadas |
| Risco | Tipo de pendência com maior impacto |
| Liquidez | Tempo real de saída por segmento |
| Valuation | Erro médio por tipo/local |
| Estratégia | Estratégia com melhor desempenho |


# 20. Base de Decisões

Cada decisão deve poder alimentar uma base histórica para responder:
- Quais critérios geram melhores oportunidades?
- Quais critérios geram falsos positivos?
- Quais imóveis foram rejeitados e depois se mostraram bons?
- Quais riscos foram subestimados?
- Quais bairros/tipos tiveram melhor desempenho?
- Quais estratégias tiveram melhor retorno ajustado ao risco?

# 21. Conhecimento por Mercado


| Dimensão | Exemplo |
|---|---|
| Cidade | Curitiba |
| Região | Bairro/submercado |
| Tipo | Apartamento |
| Ticket | R$ 150–250 mil |
| Estratégia | Renda |
| Liquidez | Alta |
| Yield | Faixa observada |
| Risco | Perfil histórico |

O conhecimento deve ser contextualizado; uma regra boa em um submercado pode não ser boa em outro.

# 22. Auditoria de Dados

- Fonte original preservada.
- Data da captura preservada.
- Transformações rastreáveis.
- Conflitos entre fontes registrados.
- Correções não apagam original.
- Estimativas possuem premissas.
- Dados desconhecidos continuam desconhecidos.

# 23. Auditoria de Decisões


| Pergunta | Resposta esperada |
|---|---|
| Por que aprovou? | Margem + estratégia + risco + evidências |
| Por que rejeitou? | Regra/margem/risco/fit |
| Por que score mudou? | Evento material |
| Por que ranking mudou? | Comparação atualizada |
| Por que regra mudou? | Backtest/mercado/estratégia |
| Quem autorizou? | Responsável registrado |


# 24. Auditoria de Mudanças


| Antes | Depois | Motivo |
|---|---|---|
| Yield mínimo 1,0% | 0,8% | Mudança de estratégia |
| Score mínimo 70 | 75 | Maior seletividade |
| Liquidez mínima 70 | 75 | Capital mais restrito |
| Margem mínima 15% | 18% | Aumento de risco |

Exemplos ilustrativos.

# 25. Governança do Aprendizado

Resultados históricos podem propor mudanças, mas toda alteração relevante deve ser testada antes de virar regra vigente.
- Identificar padrão.
- Medir evidência.
- Propor mudança.
- Executar backtest.
- Comparar versão atual × proposta.
- Avaliar efeitos colaterais.
- Aprovar.
- Publicar nova versão.
- Monitorar resultado.

# 26. Controle de Qualidade das Regras


| Teste | Objetivo |
|---|---|
| Coerência | Regra não contradiz outra. |
| Cobertura | Cenários relevantes atendidos. |
| Borda | Limites funcionam corretamente. |
| Histórico | Decisões antigas continuam reproduzíveis. |
| Backtest | Melhora comprovada. |
| Explicabilidade | Resultado compreensível. |


# 27. Gestão de Conhecimento Negativo

O Radar também deve registrar o que NÃO funcionou.
- Bairros com liquidez superestimada.
- Tipos de imóvel com reforma problemática.
- Estimativas de aluguel excessivamente otimistas.
- Riscos recorrentes.
- Estratégias que falharam.
- Regras que produziram falsos positivos.

# 28. Governança do Ciclo de Vida


| Estado | Governança |
|---|---|
| Rascunho | Pode ser editado. |
| Em revisão | Aguardando validação. |
| Aprovado | Pronto para vigência. |
| Ativo | Aplicado às novas análises. |
| Retirado | Não usado em novas decisões. |
| Histórico | Preservado para auditoria. |


# 29. Segurança da Decisão

O objetivo da governança é impedir que uma mudança posterior reescreva a história ou torne uma decisão impossível de explicar.
- Não sobrescrever decisões.
- Não apagar evidências.
- Não substituir versão antiga.
- Não esconder exceções.
- Não tratar resultado posterior como se fosse conhecido na data original.

# 30. Antiviés Temporal

Ao avaliar uma decisão passada, o Radar deve utilizar somente informações que estavam disponíveis naquele momento. Informações futuras não podem contaminar o backtest.
Exemplo: não usar o preço de venda realizado em 2027 para avaliar se a decisão tomada em 2026 era racional com as informações disponíveis em 2026.

# 31. Governança do Investidor


| Elemento | Controle |
|---|---|
| Objetivos | Versionados |
| Estratégias | Versionadas |
| Limites | Versionados |
| Reserva | Versionada |
| Preferências | Versionadas |
| Exceções | Auditadas |
| Decisões | Preservadas |


# 32. Indicadores de Governança


| Indicador | Objetivo |
|---|---|
| Decisões reproduzíveis | Medir rastreabilidade |
| Regras com versão | 100% |
| Decisões com justificativa | 100% |
| Decisões com evidência | Meta alta |
| Exceções justificadas | 100% |
| Mudanças auditáveis | 100% |
| Dados sem origem | Minimizar |
| Falsos positivos | Reduzir |
| Falsos negativos | Reduzir |


# 33. Regras de Negócio


| ID | Regra | Resultado |
|---|---|---|
| GOV24-001 | Mudança material gera nova versão | Obrigatório |
| GOV24-002 | Histórico não pode ser sobrescrito | Obrigatório |
| GOV24-003 | Decisão deve ser reproduzível | Obrigatório |
| GOV24-004 | Regra crítica exige governança | Aprovação |
| GOV24-005 | Exceção exige justificativa | Obrigatório |
| GOV24-006 | Evidência relevante deve ser preservada | Obrigatório |
| GOV24-007 | Dados futuros não entram em decisões passadas | Bloquear |
| GOV24-008 | Regra recorridamente excepcionada deve ser revisada | Reavaliar |
| GOV24-009 | Mudança de score deve possuir versão | Obrigatório |
| GOV24-010 | Aprendizado deve ser testado antes de vigência | Obrigatório |
| GOV24-011 | Fato e inferência não podem ser confundidos | Obrigatório |
| GOV24-012 | Conhecimento negativo deve ser preservado | Obrigatório |


# 34. Critérios de Aceite

- CA-D24 — É possível reconstruir uma decisão histórica.
- CA-D24 — Dados originais permanecem preservados.
- CA-D24 — Regras possuem versões e vigência.
- CA-D24 — Parâmetros possuem histórico.
- CA-D24 — Score possui versão.
- CA-D24 — Exceções são rastreáveis.
- CA-D24 — Decisões possuem justificativa.
- CA-D24 — Evidências possuem origem.
- CA-D24 — Fatos são separados de estimativas e inferências.
- CA-D24 — Conflitos de regras possuem precedência definida.
- CA-D24 — O conhecimento histórico é reutilizável.
- CA-D24 — Resultados reais podem gerar aprendizado.
- CA-D24 — Backtests evitam uso de informação futura.
- CA-D24 — Mudanças críticas possuem aprovação.
- CA-D24 — Regras recorridamente excepcionadas podem ser revistas.
- CA-D24 — É possível auditar por que uma oportunidade subiu ou caiu no ranking.
- CA-D24 — É possível identificar quem realizou/aprovou mudanças.
- CA-D24 — O Radar mantém conhecimento positivo e negativo.

# 35. Relação com os Documentos


| Documento | Relação |
|---|---|
| 6 — Modelo de Dados | Define conceitos que precisam de governança. |
| 8 — Parâmetros | Define catálogo configurável. |
| 12 — Traceabilidade | Define vínculos entre requisitos e decisões. |
| 15 — Decisão | Define precedência. |
| 22 — Ranking | Define priorização. |
| 23 — Aprendizado | Define evolução e backtest. |
| 24 | Consolida governança e memória do produto. |


# 36. Visão Final de Governança

DADO → EVIDÊNCIA → INTERPRETAÇÃO → REGRA → SCORE → RANKING → DECISÃO → RESULTADO → APRENDIZADO → NOVA REGRA
Cada etapa deve ser rastreável. O conhecimento acumulado passa a ser um ativo central do Radar.

# 37. Próximo Documento

Recomendação: Documento 25 — Arquitetura Funcional do Produto e Mapa Consolidado de Módulos, Fluxos e Capacidades de Negócio. A partir daqui, os documentos já cobrem regras, dados, valuation, economia, risco, liquidez, investidor, ranking, monitoramento e governança; o próximo passo pode consolidar tudo em uma visão única do produto antes de entrar em especificações de implementação.
