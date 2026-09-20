# Radar_Imobiliario_Documento_10_Especificacao_Funcional_Detalhada_dos_Modulos_v1.0

🎯
RADAR IMOBILIÁRIO
Documento 10 — Especificação Funcional Detalhada dos Módulos
Versão 1.0 | Documento de Negócio

# 1. Objetivo

Detalhar funcionalmente os módulos definidos no Documento 9, estabelecendo responsabilidades, fluxos, entradas, saídas, regras, exceções, estados e critérios de aceite. O documento continua independente de tecnologia.

# 2. Princípio

O Radar deve transformar dados dispersos em uma decisão de investimento explicável. O sistema não deve apenas mostrar imóveis: deve demonstrar por que uma oportunidade merece atenção, quais riscos existem e o que ainda precisa ser confirmado.

# 3. Arquitetura Funcional do Produto

A visão funcional é organizada em cinco grandes blocos:

| Bloco | Módulos | Objetivo |
|---|---|---|
| Entrada | 01–04 | Capturar, preservar, normalizar e consolidar informações. |
| Inteligência | 05–12 | Entender imóvel, mercado, economia, estratégia, regras e score. |
| Decisão | 13–16 | Rankear, analisar, executar due diligence e decidir. |
| Acompanhamento | 17–19 | Alertar, monitorar e preservar histórico. |
| Gestão | 20–22 | Relatórios, backtest e governança. |


# 4. Padrão Funcional de Cada Módulo

Todo módulo deve ser descrito por: objetivo → atores → entradas → processamento de negócio → saídas → regras → exceções → eventos → critérios de aceite.
A sequência abaixo é a especificação funcional de referência.

| ID | Módulo | Responsabilidade |
|---|---|---|
| MOD-01 | Fontes | Administrar origens de dados. |
| MOD-02 | Captura | Registrar snapshots das oportunidades. |
| MOD-03 | Normalização | Padronizar informações. |
| MOD-04 | Deduplicação | Consolidar ocorrências do mesmo imóvel. |
| MOD-05 | Perfil do Imóvel | Consolidar características do ativo. |
| MOD-06 | Localização | Classificar contexto territorial. |
| MOD-07 | Mercado | Construir evidências de mercado. |
| MOD-08 | Valuation | Estimar valor de mercado. |
| MOD-09 | Economia | Calcular tese econômica. |
| MOD-10 | Estratégias | Avaliar aderência a objetivos. |
| MOD-11 | Regras | Aplicar critérios configurados. |
| MOD-12 | Score | Priorizar oportunidades. |
| MOD-13 | Radar/Ranking | Apresentar oportunidades. |
| MOD-14 | Análise Profunda | Investigar tese. |
| MOD-15 | Due Diligence | Validar riscos e evidências. |
| MOD-16 | Workflow/Decisão | Controlar estados e decisões. |
| MOD-17 | Alertas | Notificar eventos relevantes. |
| MOD-18 | Monitoramento | Reavaliar teses vivas. |
| MOD-19 | Histórico | Preservar evolução. |
| MOD-20 | Relatórios | Consolidar informações. |
| MOD-21 | Backtest | Calibrar regras e score. |
| MOD-22 | Governança | Controlar configurações e auditoria. |


# 5. MOD-01 — Fontes

Objetivo: controlar as origens das informações.

| Função | Descrição |
|---|---|
| Cadastrar fonte | Nome, tipo, origem, abrangência e status. |
| Classificar fonte | Banco, leiloeiro, portal, órgão público, mercado, manual etc. |
| Ativar/desativar | Permitir controle operacional. |
| Avaliar qualidade | Registrar confiabilidade histórica. |
| Acompanhar cobertura | Identificar regiões/tipos atendidos. |

Critério de aceite: nenhuma captura deve perder a identificação da fonte original.

# 6. MOD-02 — Captura

Objetivo: registrar exatamente o que foi observado em determinado momento.

| Entrada | Saída |
|---|---|
| Identificação da fonte | Captura identificada |
| Data/hora | Timestamp da observação |
| Dados originais | Snapshot preservado |
| Referência da oportunidade | Vínculo com ocorrência |

Regra: uma nova captura não sobrescreve a anterior.
Eventos: nova captura, alteração de preço, alteração de status, remoção da fonte.

# 7. MOD-03 — Normalização

Objetivo: converter diferentes formatos para uma linguagem comum de negócio.
- Padronizar preço e moeda.
- Padronizar área e unidades.
- Padronizar quartos/vagas.
- Padronizar endereço e localização.
- Padronizar status.
- Classificar campos como observado, confirmado, calculado, estimado, inferido ou desconhecido.
Critério de aceite: o dado original continua recuperável após normalização.

# 8. MOD-04 — Deduplicação

Objetivo: impedir que várias capturas do mesmo imóvel sejam tratadas como imóveis distintos.

| Nível | Exemplos |
|---|---|
| Identidade forte | Matrícula/documento identificador. |
| Identidade provável | Endereço + unidade + características. |
| Similaridade | Endereço aproximado + área + quartos + vaga. |
| Indefinido | Possível duplicidade que exige confirmação. |

A deduplicação deve permitir consolidar capturas sem apagar nenhuma delas.

# 9. MOD-05 — Perfil do Imóvel

Objetivo: formar a visão consolidada do ativo.

| Grupo | Dados |
|---|---|
| Identificação | Tipo, matrícula, unidade, origem |
| Físico | Área, quartos, banheiros, vagas |
| Edificação | Condomínio, idade, padrão |
| Condição | Novo, usado, reforma necessária |
| Posse | Livre, ocupado, desconhecido |
| Comercial | Preço, avaliação, status |
| Localização | Cidade, bairro, endereço, contexto |

Regra: o perfil consolidado pode evoluir; cada alteração relevante deve ser historicamente rastreável.

# 10. MOD-06 — Localização

Objetivo: interpretar a localização segundo configuração e contexto de mercado.
- Classificar cidade/bairro/região.
- Aplicar zonas prioritárias, aceitáveis, condicionais e bloqueadas.
- Avaliar liquidez regional.
- Avaliar demanda de compra e aluguel.
- Aplicar parâmetros específicos da estratégia.
A classificação territorial não deve ser universal: deve respeitar o perfil e a estratégia do investidor.

# 11. MOD-07 — Mercado

Objetivo: construir evidência sobre preço, aluguel, liquidez e comportamento local.

| Função | Resultado |
|---|---|
| Comparáveis | Conjunto de evidências qualificadas. |
| Preço/m² | Indicador relativo. |
| Aluguel | Faixa de aluguel provável. |
| Liquidez | Estimativa de facilidade de saída. |
| Histórico | Evolução dos indicadores. |
| Anomalias | Outliers para investigação. |


# 12. MOD-08 — Valuation

Objetivo: estimar o valor de mercado do imóvel com cenários e confiança.

| Saída | Descrição |
|---|---|
| Conservador | Estimativa prudente. |
| Base | Tese central. |
| Otimista | Cenário favorável. |
| Venda rápida | Valor provável sob necessidade de liquidez. |
| Confiança | Qualidade da evidência. |

Regra central: valor da fonte não é automaticamente valor de mercado.
Critério de aceite: valuation deve indicar evidências, data e confiança.

# 13. MOD-09 — Economia

Objetivo: transformar preço e valuation em uma tese econômica realista.

| Cálculo | Definição |
|---|---|
| Custo total | Preço + aquisição + dívidas + reforma + regularização + financeiro + demais custos. |
| Desconto líquido | 1 − custo total / valor de mercado. |
| Margem | Valor de mercado − custo total. |
| Margem % | Margem / valor de mercado. |
| Yield bruto | Aluguel mensal / custo total. |
| Cenários | Conservador, base, otimista e estressado. |

Regra: custo desconhecido deve gerar incerteza, faixa ou pendência; nunca custo zero silencioso.

# 14. MOD-10 — Estratégias

Objetivo: avaliar o mesmo imóvel sob diferentes teses.

| Estratégia | Pergunta principal |
|---|---|
| Renda | Quanto posso gerar de renda e com qual risco? |
| Revenda | Existe margem líquida suficiente para sair? |
| Valorização | Existe potencial de valorização ajustado ao risco? |
| MCMV/Baixa renda | Existe demanda, liquidez e economia compatíveis? |
| Terreno | Existe potencial de uso e valorização? |
| Apartamento | A unidade apresenta liquidez, renda e preço adequados? |
| Casa/Sobrado | Terreno, localização, reforma e saída fazem sentido? |
| 1 dormitório | Demanda e yield compensam o ticket? |


# 15. MOD-11 — Regras

Objetivo: aplicar o catálogo de regras configuráveis.

| Tipo | Resultado |
|---|---|
| Hard | Elimina/bloqueia. |
| Soft | Penaliza score. |
| Conditional | Cria condição para aprovação. |
| Informational | Gera alerta sem eliminar. |
| Exception | Permite desvio controlado. |

Critério de aceite: o Radar deve conseguir explicar cada regra que influenciou a oportunidade.

# 16. MOD-12 — Score

Objetivo: ordenar oportunidades sobreviventes às regras.
Componentes possíveis: desconto líquido, margem, liquidez, localização, risco, yield, valorização, qualidade da oportunidade e confiança.
Score deve ser calculado por estratégia. Um imóvel pode ter score 85 em renda e 62 em revenda.
Regra: bloqueio crítico prevalece sobre qualquer score.

# 17. MOD-13 — Radar e Ranking

Objetivo: permitir descoberta rápida das melhores oportunidades.

| Visão | Uso |
|---|---|
| Top oportunidades | Prioridade geral. |
| Por estratégia | Melhores para cada tese. |
| Por região | Comparação territorial. |
| Novidades | Entradas recentes. |
| Queda de preço | Mudanças relevantes. |
| Score crescente | Oportunidades que melhoraram. |
| Monitoramento | Teses ainda vivas. |
| Bloqueadas | Controle de rejeições. |

Cada card/ficha deve mostrar: preço, valuation, custo total, desconto líquido, score, confiança, risco e principal motivo da classificação.

# 18. MOD-14 — Análise Profunda

Objetivo: sair da triagem automática para uma análise estruturada.

| Etapa | Pergunta |
|---|---|
| Tese | Por que isso é uma oportunidade? |
| Mercado | O valor estimado é defensável? |
| Economia | A margem continua boa após custos? |
| Liquidez | Consigo sair quando precisar? |
| Risco | O que pode destruir a tese? |
| Pendências | O que ainda não sabemos? |
| Cenários | A tese sobrevive ao cenário estressado? |
| Conclusão | Comprar, condicionar, monitorar ou rejeitar? |


# 19. MOD-15 — Due Diligence

Objetivo: validar fatos críticos antes da decisão.
- Matrícula e titularidade.
- Ônus e restrições.
- Processos relevantes.
- Condomínio e débitos.
- IPTU e tributos.
- Ocupação/posse.
- Condições da venda.
- Estado físico/reforma.
- Validação de mercado.
- Documentação/evidências.
Cada item deve possuir status: Não iniciado, Em análise, Confirmado, Não confirmado, Dispensado ou Bloqueado.

# 20. MOD-16 — Workflow e Decisão

Fluxo de referência: Captured → Normalized → Qualified → Enriched → Valuated → Scored → Ranked → In Analysis → Pending/Due Diligence → Approved / Conditional Purchase / Rejected / Blocked → Acquired → Closed.
Decisões:

| Decisão | Condição conceitual |
|---|---|
| BUY | Tese validada. |
| BUY IF | Condições objetivas pendentes. |
| MONITOR | Interessante, mas ainda insuficiente. |
| DO NOT BUY | Tese não compensa. |
| BLOCK | Impedimento crítico. |


# 21. MOD-17 — Alertas

Alertas devem ser acionáveis.

| Evento | Prioridade sugerida |
|---|---|
| Risco crítico novo | Crítica |
| Condição de compra atingida | Alta |
| Grande queda de preço | Alta |
| Mudança relevante de valuation | Alta |
| Score cruzou limiar | Média/Alta |
| Novo comparável relevante | Média |
| Mudança de status | Média |
| Pendência vencida | Média |
| Atualização sem impacto material | Informativa |


# 22. MOD-18 — Monitoramento

Uma oportunidade em monitoramento continua viva, mas não necessariamente em análise profunda.
- Preço mudou.
- Status mudou.
- Novo comparável apareceu.
- Aluguel mudou.
- Novo risco surgiu ou foi resolvido.
- Regra/estratégia mudou.
- Evidência perdeu validade.
Qualquer evento material pode disparar revaluation e novo score.

# 23. MOD-19 — Histórico

Deve preservar evolução de preço, valuation, score, classificação, regras, riscos, evidências, decisões, alertas e parâmetros utilizados.
Regra: histórico é parte da inteligência do produto, não apenas auditoria.

# 24. MOD-20 — Relatórios


| Relatório | Conteúdo |
|---|---|
| Radar diário | Novas e melhores oportunidades. |
| Ranking | Top por estratégia. |
| Análise | Oportunidades em investigação. |
| Due diligence | Pendências e evidências. |
| Risco | Riscos por severidade. |
| Performance | Resultados realizados. |
| Histórico | Evolução temporal. |
| Regras | Impacto das configurações. |


# 25. MOD-21 — Backtest

Objetivo: verificar se regras e pesos produzem resultados coerentes antes de tratá-los como definitivos.
- Testar configurações antigas sobre oportunidades históricas.
- Medir falsos positivos e negativos.
- Comparar valuation previsto e resultado observado.
- Comparar ranking e retorno real.
- Testar pesos alternativos.
- Registrar versão da configuração vencedora.

# 26. MOD-22 — Governança


| Controle | Obrigatoriedade |
|---|---|
| Versão de regra | Obrigatório |
| Versão de score | Obrigatório |
| Vigência | Obrigatório |
| Justificativa de mudança | Obrigatório |
| Exceção | Justificativa + evidência |
| Auditoria | Histórico preservado |
| Configuração experimental | Separada da oficial |


# 27. Fluxo Completo — Caso de Uso Principal

CENÁRIO: o Radar encontra um apartamento anunciado por valor inferior ao esperado.
1. A fonte gera uma captura.
2. O Radar preserva o snapshot.
3. Normaliza os dados.
4. Identifica/consolida o imóvel.
5. Verifica elegibilidade.
6. Enriquece localização e mercado.
7. Busca comparáveis.
8. Calcula valuation e confiança.
9. Calcula custo econômico total.
10. Calcula desconto líquido e margem.
11. Avalia aluguel e liquidez.
12. Aplica estratégias.
13. Aplica hard/soft/conditional rules.
14. Calcula score.
15. Classifica e rankeia.
16. Gera explicação.
17. Se relevante, cria análise profunda.
18. Executa due diligence.
19. Registra decisão.
20. Mantém monitoramento e histórico.

# 28. Exemplo de Explicabilidade

“Oportunidade classificada como EXCELENTE para Renda.”

| Fator | Resultado |
|---|---|
| Preço de aquisição | R$ 190 mil |
| Valor de mercado base | R$ 260 mil |
| Custo econômico total | R$ 207 mil |
| Desconto líquido | 20,4% |
| Yield bruto | 0,92% a.m. |
| Liquidez | 78/100 |
| Risco | Baixo/Médio |
| Confiança | Alta |
| Score | 84 |
| Pendência | Confirmar condomínio |

Conclusão: interessante pela margem e liquidez; confirmação do condomínio é necessária antes da decisão final.

# 29. Exemplo de Bloqueio

Mesmo que um imóvel apresente 35% de desconto e score preliminar alto, um risco jurídico classificado como crítico deve gerar BLOCKED. O sistema deve explicar: regra responsável, evidência, data e condição para eventual desbloqueio.

# 30. Critérios de Aceite Globais

- Cada oportunidade deve ser rastreável até sua fonte e captura.
- Cada cálculo relevante deve possuir origem, data e premissas.
- Cada score deve indicar estratégia e versão.
- Cada bloqueio deve possuir motivo.
- Cada recomendação deve possuir explicação.
- Cada dado desconhecido deve permanecer desconhecido.
- Cada mudança material deve poder provocar reavaliação.
- Cada decisão deve preservar sua história.
- Cada exceção deve ser justificável.
- Os parâmetros devem poder mudar sem reescrever o passado.

# 31. MVP Funcional Recomendado

O MVP deve provar o ciclo completo, não necessariamente todos os recursos avançados.

| Prioridade | Escopo |
|---|---|
| Essencial | Captura → consolidação → valuation → economia → regras → score → ranking → análise → decisão. |
| Essencial | Configuração de investidor e estratégias. |
| Essencial | Ficha da oportunidade. |
| Essencial | Histórico de preço/score. |
| Essencial | Alertas de eventos materiais. |
| Essencial | Due diligence estruturada. |
| Posterior | Múltiplas fontes. |
| Posterior | Backtest avançado. |
| Posterior | Modelos mais sofisticados de liquidez/valorização. |
| Posterior | Automação de canais de comunicação. |


# 32. O que este Documento Fecha

Com os Documentos 0–10, o Radar possui: visão de negócio, regras, valuation, estratégias, due diligence, requisitos, modelo de dados de negócio, workflow, parâmetros, casos de uso e detalhamento funcional dos módulos.

# 33. Próximo Documento Recomendado

Documento 11 — Especificação Funcional das Telas, Navegação e Experiência do Investidor. O objetivo será desenhar, ainda sem tecnologia, o que o usuário vê, quais ações executa, quais filtros utiliza e como percorre o Radar desde a descoberta até a decisão.
