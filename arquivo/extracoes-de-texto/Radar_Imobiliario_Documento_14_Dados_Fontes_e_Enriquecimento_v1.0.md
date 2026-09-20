# Radar_Imobiliario_Documento_14_Dados_Fontes_e_Enriquecimento_v1.0

🏠 RADAR IMOBILIÁRIO
Documento 14
Dados, Fontes e Enriquecimento
Especificação de Negócio | Versão 1.0
Princípio central: o Radar não deve apenas coletar imóveis; deve transformar dados dispersos em evidências suficientes para avaliar uma oportunidade.

# 1. Objetivo

Definir, em nível de negócio, quais dados o Radar precisa conhecer, de onde esses dados podem vir, como devem ser avaliados, quando precisam ser atualizados e como o enriquecimento transforma uma captura inicial em uma oportunidade analisável.
- Este documento não define arquitetura, tecnologia, banco de dados ou APIs.
- O foco é a qualidade da informação necessária para tomar decisões de investimento.
- A origem e a qualidade de cada informação devem ser rastreáveis.

# 2. Filosofia de Dados

O Radar deve trabalhar com a ideia de que informação tem valor diferente conforme sua origem, confirmação, atualidade e impacto na decisão.

| Princípio | Aplicação |
|---|---|
| Dado não é decisão | Preço, metragem ou avaliação são fatos/entradas; oportunidade é uma conclusão. |
| Fonte importa | Uma informação oficial ou documental pode ter peso diferente de um anúncio. |
| Evidência importa | Toda conclusão relevante deve poder ser sustentada por evidência. |
| Desconhecido permanece desconhecido | Ausência de informação não deve ser convertida em risco zero ou custo zero. |
| Tempo importa | Preço, aluguel, disponibilidade e condições podem mudar. |
| Conflito deve ser explicitado | Fontes divergentes devem gerar pendência, não uma escolha silenciosa. |
| Histórico é preservado | Mudanças relevantes devem permanecer registradas. |
| Confiança acompanha o dado | Quanto menor a qualidade/certeza, menor a confiança na conclusão. |


# 3. Categorias de Dados


| Categoria | Exemplos | Impacto |
|---|---|---|
| Identificação | matrícula, número do imóvel, endereço, unidade | Muito alto |
| Oferta/captura | preço, modalidade, status, datas | Muito alto |
| Localização | bairro, CEP, região, infraestrutura, contexto | Alto |
| Características | área, quartos, vagas, padrão, condomínio | Alto |
| Mercado | comparáveis, preço/m², transações, anúncios | Muito alto |
| Valuation | valor estimado, faixas, confiança | Muito alto |
| Economia | custos, reforma, dívidas, impostos, comissão | Muito alto |
| Renda | aluguel, vacância, yield | Alto |
| Liquidez | tempo de venda, demanda, ticket, absorção | Alto |
| Jurídico/documental | ocupação, processos, matrícula, ônus | Crítico |
| Físico | conservação, reforma, visita, fotos | Alto |
| Estratégia | objetivo, restrições, aderência | Muito alto |
| Decisão | análise, pendências, aprovação/reprovação | Crítico |


# 4. Dados Mínimos Viáveis

Um imóvel só deve entrar no Radar como oportunidade analisável quando possuir um conjunto mínimo de informações. A ausência de dados não necessariamente elimina o imóvel, mas pode impedir sua classificação ou reduzir sua confiança.

| Bloco | Mínimo necessário | Gate |
|---|---|---|
| Identificação | endereço ou identificador suficientemente confiável | Obrigatório |
| Preço | preço atual e condição da oferta | Obrigatório |
| Tipo | apartamento, casa, terreno etc. | Obrigatório |
| Localização | bairro/região/município | Obrigatório |
| Área | área conhecida ou sinalizada como desconhecida | Obrigatório |
| Fonte | origem e data da captura | Obrigatório |
| Modalidade/status | venda, leilão, ocupado etc., quando aplicável | Obrigatório |
| Valuation inicial | estimativa ou indicação de insuficiência | Obrigatório para ranking econômico |
| Custo econômico | componentes conhecidos + desconhecidos explicitados | Obrigatório para decisão |
| Estratégia | ao menos uma estratégia candidata | Obrigatório para recomendação |
| Confiança | nível de confiança dos dados/conclusões | Obrigatório |
| Risco crítico | checagem preliminar de bloqueios conhecidos | Obrigatório antes de recomendação |


# 5. Dados Desejáveis e Enriquecimento


| Estágio | Objetivo | Exemplos |
|---|---|---|
| Nível 0 — Captura | registrar a oferta original | preço, endereço, fonte, data, status |
| Nível 1 — Normalização | tornar os dados comparáveis | tipo, área, bairro, valores padronizados |
| Nível 2 — Identificação | confirmar o ativo | matrícula, unidade, condomínio, identificadores |
| Nível 3 — Mercado | entender valor e demanda | comparáveis, preço/m², aluguel |
| Nível 4 — Econômico | calcular tese | custos, reforma, margem, yield |
| Nível 5 — Risco | testar fragilidades | ocupação, dívidas, processos, documentação |
| Nível 6 — Estratégia | avaliar aderência | renda, revenda, valorização, MCMV, terreno |
| Nível 7 — Due Diligence | validar antes da decisão | evidências documentais, visita, pendências |
| Nível 8 — Pós-decisão | aprender com o resultado | compra, venda, aluguel, custos e resultado real |


# 6. Tipos de Fontes


| Fonte | Papel | Confiabilidade típica | Observação |
|---|---|---|---|
| Caixa / instituição vendedora | oferta, condições, avaliação, modalidade | Alta para dados da própria oferta | Não substitui valuation de mercado |
| Leiloeiro / edital | regras, datas, condições, documentação da venda | Alta para o certame | Ler condições específicas |
| Portais imobiliários | oferta e comparáveis | Média | Preço anunciado não é necessariamente preço transacionado |
| Registros/documentos públicos | matrícula, ônus, processos, tributos | Alta quando oficiais e atuais | Exigir contexto e data |
| Condomínio/administração | taxas, débitos, características | Alta quando confirmada | Pode exigir confirmação formal |
| Pesquisa de mercado | preço, aluguel, demanda | Média a alta | Qualidade depende da amostra |
| Visita/fotos | condição física e ocupação | Alta para o observado | Sempre registrar data e limitações |
| Informação manual do analista | hipóteses, observações | Variável | Deve ser identificada como interpretação |


# 7. Hierarquia de Confiabilidade

A hierarquia abaixo é orientativa e deve ser ajustada conforme o tipo de dado.

| Nível | Descrição | Uso |
|---|---|---|
| A — Confirmado | documento oficial, evidência direta ou múltiplas confirmações | Pode sustentar decisão |
| B — Forte | fonte confiável e atual, sem confirmação independente | Pode sustentar análise |
| C — Indicado | fonte razoável, mas ainda não confirmada | Usar com ressalva |
| D — Estimado | inferência/cálculo com premissas | Não tratar como fato |
| E — Incerto | informação fraca, antiga ou conflitante | Reduz confiança |
| U — Desconhecido | não há informação suficiente | Gerar pendência |


# 8. Captura e Snapshot

Toda captura deve representar o que a fonte informava naquele momento. O Radar deve preservar a fotografia original antes de normalizar ou enriquecer.
- Data e hora da captura.
- Fonte e identificação da publicação.
- Preço e condições naquele momento.
- Status/modalidade.
- Texto ou informações relevantes da oferta.
- Dados originais que possam ser necessários para auditoria.
- Posteriores correções não devem apagar o valor originalmente capturado.

# 9. Identificação do Imóvel


| Dado | Importância | Regra de negócio |
|---|---|---|
| Endereço | Crítica | Normalizar e validar sempre que possível. |
| Matrícula | Crítica | Usar como forte identificador documental. |
| Unidade/apto | Alta | Separar empreendimento de unidade. |
| Condomínio | Alta | Identificar empreendimento quando possível. |
| CEP | Média/Alta | Apoiar normalização geográfica. |
| Identificador da fonte | Alta | Preservar para rastreabilidade. |
| Área | Alta | Registrar tipo de área quando conhecido. |


# 10. Dados de Localização

Localização deve ser analisada como contexto de mercado, não apenas como endereço.
- Município, bairro, região e microregião.
- Infraestrutura, transporte, comércio, serviços e atratividade.
- Perfil de demanda e liquidez.
- Faixa de preço predominante.
- Relação com regiões de referência.
- Características negativas relevantes quando comprovadas.
- Classificação de localização deve ser parametrizável e nunca universal.
Importante: perfil econômico de uma região não deve ser usado isoladamente para excluir oportunidades. A estratégia deve considerar demanda, liquidez, preço, financiamento, aluguel e risco.

# 11. Mercado e Comparáveis


| Dado | Obrigatório? | Critério |
|---|---|---|
| Preço do comparável | Sim para uso | Registrar valor e data |
| Localização | Sim | Priorizar proximidade e contexto equivalente |
| Área | Sim quando disponível | Comparar corretamente |
| Tipo/padrão | Sim | Evitar misturar segmentos incompatíveis |
| Quartos/vagas | Desejável/alto | Ajustar diferenças relevantes |
| Condição | Desejável | Separar reformado, original e novo |
| Status da oferta | Desejável | Anunciado não equivale a vendido |
| Fonte | Sim | Rastreabilidade |
| Data | Sim | Evitar comparável obsoleto |


# 12. Valuation

O valuation deve produzir valor estimado, faixa de valor, cenário e confiança. A avaliação da fonte da oferta é referência, não verdade absoluta de mercado.

| Saída | Descrição |
|---|---|
| Valor conservador | estimativa prudente |
| Valor base | estimativa mais provável |
| Valor otimista | potencial superior, usado com cautela |
| Valor de venda rápida | referência para liquidez/saída |
| Confiança | qualidade da evidência |
| Justificativa | comparáveis e ajustes utilizados |


# 13. Dados de Aluguel e Yield

- Aluguel mensal potencial.
- Condomínio e custos recorrentes relevantes.
- Vacância esperada.
- Liquidez de locação.
- Faixa de aluguel dos comparáveis.
- Yield bruto e, quando possível, yield líquido.
Yield nunca deve ser analisado isoladamente. Um yield elevado pode esconder baixa liquidez, reforma, risco ou dificuldade de saída.

# 14. Custos, Dívidas e Custo Econômico


| Componente | Exemplos | Tratamento |
|---|---|---|
| Aquisição | preço/lance | Obrigatório |
| Comissão | leiloeiro/intermediação | Adicionar quando aplicável |
| Tributos/documentação | ITBI, registro etc. | Estimar e atualizar |
| Condomínio | cotas e débitos | Confirmar responsabilidade |
| IPTU/taxas | débitos e encargos | Investigar |
| Reforma | material + mão de obra | Cenários 0–4 |
| Regularização | documentos/obras | Adicionar quando identificada |
| Financiamento | juros/custos | Considerar quando estratégia exigir |
| Custo de carregamento | tempo até venda/locação | Usar em cenários |
| Contingência | margem prudencial | Parametrizável |

Regra: custo desconhecido não deve ser tratado como R$ 0. Deve permanecer como desconhecido, estimado ou contingenciado.

# 15. Dados Jurídicos e Documentais

- Matrícula e titularidade.
- Ônus, averbações e restrições.
- Ocupação/posse.
- Processos relevantes.
- Condições específicas da venda.
- Débitos e responsabilidades.
- Situação de regularização.
- Evidência e data de consulta.
Riscos críticos podem bloquear a oportunidade independentemente do score.

# 16. Dados Físicos e Visita


| Informação | Exemplo |
|---|---|
| Conservação | novo, bom, regular, ruim |
| Reforma | nível 0 a 4 |
| Estrutura | aparente/confirmada/desconhecida |
| Instalações | elétrica, hidráulica etc. |
| Ocupação | livre, ocupado, desconhecido |
| Fotos | fonte e data |
| Visita | data, responsável, observações |
| Limitações | áreas não acessadas, informações não verificadas |


# 17. Liquidez

Liquidez é uma variável de negócio própria. O Radar deve estimar a facilidade de locação ou venda, e não inferi-la apenas do desconto.
- Tempo esperado de saída.
- Quantidade/qualidade de demanda.
- Ticket em relação ao mercado local.
- Oferta concorrente.
- Facilidade de financiamento, quando aplicável.
- Adequação do imóvel ao público-alvo.
- Histórico de absorção, quando disponível.

# 18. Risco


| Grupo | Exemplos | Efeito |
|---|---|---|
| Jurídico | processos, restrições, documentação | Pode bloquear |
| Posse | ocupação, resistência, desocupação | Aumenta custo/prazo |
| Financeiro | custos desconhecidos, reforma alta | Reduz margem |
| Mercado | baixa demanda, baixa liquidez | Reduz score |
| Valuation | poucos comparáveis | Reduz confiança |
| Operacional | complexidade de aquisição | Aumenta esforço |
| Estratégico | fora do objetivo | Pode eliminar |


# 19. Dados da Estratégia

O mesmo imóvel deve poder ser avaliado por estratégias diferentes.

| Estratégia | Dados especialmente relevantes |
|---|---|
| Renda | aluguel, yield, vacância, condomínio, liquidez |
| Revenda | desconto líquido, margem, reforma, tempo de saída |
| Valorização | localização, tendência, infraestrutura, horizonte |
| MCMV/baixa renda | demanda, financiamento, ticket, aluguel, liquidez |
| Terreno | uso, zoneamento, demanda, infraestrutura, potencial |
| Casa/sobrado | terreno, conservação, demanda, liquidez, custo de manutenção |
| 1 dormitório | demanda locatícia, ticket, aluguel, liquidez |


# 20. Evidências

Toda informação relevante deve poder ser classificada como evidência observada, confirmada, calculada, estimada, inferida ou desconhecida.

| Tipo | Exemplo | Pode sustentar decisão? |
|---|---|---|
| Observada | foto mostra estado aparente | Sim, com limitação |
| Confirmada | documento oficial atual | Sim |
| Calculada | yield calculado com dados confirmados | Sim, conforme premissas |
| Estimada | reforma estimada por faixa | Sim em cenário |
| Inferida | demanda inferida de sinais de mercado | Com cautela |
| Desconhecida | ocupação não verificada | Não como fato |


# 21. Qualidade dos Dados


| Dimensão | Pergunta |
|---|---|
| Completude | Temos os dados necessários? |
| Atualidade | O dado ainda representa o mercado/oferta? |
| Consistência | Os dados não se contradizem? |
| Precisão | O valor é suficientemente exato para a decisão? |
| Fonte | Quem informou? |
| Confirmação | Existe evidência independente? |
| Relevância | O dado realmente impacta a tese? |
| Rastreabilidade | Conseguimos voltar à origem? |


# 22. Frescor dos Dados

A validade temporal deve ser parametrizável por categoria. Não existe um único prazo de validade para todos os dados.

| Dado | Exemplo de sensibilidade temporal |
|---|---|
| Preço da oferta | Muito alta |
| Status da oferta | Muito alta |
| Aluguel | Alta |
| Comparáveis | Alta |
| Condições de venda | Muito alta |
| Matrícula/documentação | Alta |
| Localização estrutural | Baixa |
| Infraestrutura | Média |
| Estimativa de reforma | Média/alta |
| Score | Deve ser reavaliado após mudanças materiais |


# 23. Dados Ausentes ou Desconhecidos

- Identificar exatamente qual informação está ausente.
- Classificar o impacto da ausência: baixo, médio, alto ou crítico.
- Reduzir confiança quando apropriado.
- Criar pendência quando houver ação de investigação.
- Impedir decisão definitiva quando o dado ausente for crítico.
- Nunca preencher silenciosamente com zero ou com uma hipótese tratada como fato.

# 24. Conflitos entre Fontes


| Situação | Tratamento |
|---|---|
| Pequena diferença | Registrar e usar regra de prioridade/tolerância |
| Diferença material | Investigar antes de decisão |
| Fonte oficial x anúncio | Priorizar fonte adequada ao tipo de dado |
| Dados antigos x atuais | Priorizar atualidade, preservando histórico |
| Informação incompatível | Marcar conflito e reduzir confiança |
| Sem forma de resolver | Manter desconhecido e impedir falsa precisão |


# 25. Linhagem da Informação

Para cada dado relevante, o Radar deve ser capaz de responder: de onde veio, quando foi obtido, como foi transformado, quem confirmou, qual regra utilizou e em quais decisões impactou.

| Elemento | Exemplo |
|---|---|
| Origem | Caixa, edital, portal, documento, visita |
| Momento | data/hora da captura/consulta |
| Valor original | dado como encontrado |
| Valor normalizado | forma padronizada |
| Transformação | cálculo/ajuste realizado |
| Evidência | documento/foto/registro |
| Confiança | A–E/U |
| Impacto | qual regra ou score foi afetado |


# 26. Enriquecimento Progressivo

O Radar deve evitar gastar o mesmo esforço em todos os imóveis. O enriquecimento deve ser proporcional ao potencial da oportunidade.

| Faixa | Tratamento |
|---|---|
| Baixo potencial | captura + qualificação mínima |
| Potencial moderado | mercado + economia básica |
| Alto potencial | valuation robusto + custos + risco |
| Finalistas | due diligence profunda |
| Compra | validação final e documentação |
| Pós-compra | dados reais para aprendizado |


# 27. Gates de Dados


| Gate | Condição |
|---|---|
| G0 — Captura | fonte + identificação mínima + preço/status |
| G1 — Qualificação | localização + tipo + dados mínimos |
| G2 — Mercado | evidência suficiente para estimar valor ou declarar insuficiência |
| G3 — Economia | custo econômico + margem/desconto |
| G4 — Estratégia | aderência a pelo menos uma estratégia |
| G5 — Risco | sem bloqueio crítico conhecido |
| G6 — Recomendação | score + confiança + explicação |
| G7 — Compra | due diligence e pendências críticas resolvidas |


# 28. Impacto dos Dados no Score e na Confiança

O score mede atratividade; a confiança mede quão confiável é a análise. São dimensões diferentes.

| Situação | Score | Confiança | Resultado |
|---|---|---|---|
| Excelente oportunidade com dados robustos | Alto | Alta | Priorizar |
| Excelente preço, poucos comparáveis | Alto | Baixa | Investigar antes de concluir |
| Preço mediano, dados robustos | Médio | Alta | Pode monitorar |
| Preço baixo, risco crítico desconhecido | Alto potencial | Muito baixa | Não recomendar ainda |
| Dado crítico ausente | Indefinido | Baixa | Pendente/bloqueado conforme regra |

A confiança pode ajustar a força da recomendação, mas não deve mascarar uma regra de bloqueio.

# 29. Dicionário Resumido de Dados


| Campo de negócio | Tipo | Exemplo |
|---|---|---|
| Preço da oferta | Observado | R$ 191.651,31 |
| Valor de mercado | Estimado | R$ 300.000 |
| Custo econômico total | Calculado/estimado | R$ 220.000 |
| Desconto líquido | Calculado | 26,7% |
| Margem | Calculado | R$ 80.000 |
| Aluguel | Estimado/observado | R$ 2.200/mês |
| Yield | Calculado | 1,00% a.m. |
| Liquidez | Estimado/calculado | 78/100 |
| Risco | Classificado | Médio |
| Confiança | Classificado | Alta |
| Score | Calculado | 84 |
| Estratégia | Configurado | Renda + Revenda |
| Decisão | Resultado | BUY IF |


# 30. Matriz de Fontes — Exemplo Inicial


| Fonte | Dados principais | Confiança alvo | Uso |
|---|---|---|---|
| Caixa | preço, avaliação, modalidade, condições | Alta | Captura e oferta |
| Edital/leiloeiro | regras, datas, ocupação/condições quando informadas | Alta | Due diligence |
| Portais | comparáveis, aluguel, concorrência | Média | Mercado |
| Documentos públicos | matrícula, processos, tributos | Alta | Risco |
| Condomínio | taxas/débitos | Alta | Custos |
| Visita | estado físico/ocupação observada | Alta | Reforma/risco |
| Analista | hipóteses e interpretações | Variável | Análise |

Esta matriz é inicial. Novas fontes devem poder ser adicionadas sem alterar o conceito do Radar.

# 31. Escopo de Dados do MVP

- Captura original da oferta.
- Identificação e localização.
- Preço, modalidade e status.
- Características básicas.
- Avaliação/valuation inicial.
- Comparáveis essenciais.
- Custo econômico estimado.
- Desconto líquido e margem.
- Aluguel/yield quando aplicável.
- Liquidez estimada.
- Risco preliminar.
- Confiança.
- Estratégia.
- Score e explicação.
- Histórico de alterações.
O MVP deve provar que dados diferentes podem ser transformados em uma decisão de investimento explicável. Não deve tentar enriquecer profundamente todo o universo capturado.

# 32. Governança dos Dados


| Regra | Obrigação |
|---|---|
| Fonte | Toda informação relevante deve possuir origem. |
| Data | Dados sensíveis ao tempo devem possuir data. |
| Histórico | Mudanças relevantes devem ser preservadas. |
| Correção | Correções devem manter rastreabilidade. |
| Regra | Alterações de critérios devem ser versionadas. |
| Confiança | Toda análise deve indicar confiança. |
| Conflito | Divergências devem gerar tratamento explícito. |
| Desconhecido | Não preencher ausência como fato. |
| Decisão | Toda decisão deve possuir justificativa. |
| Aprendizado | Resultados reais devem alimentar calibração/backtest. |


# 33. Critérios de Aceite do Documento

- CA-D14 — É possível identificar quais dados são necessários para cada etapa do Radar.
- CA-D14 — Cada dado relevante possui origem, qualidade e tratamento de ausência definidos.
- CA-D14 — O Radar preserva a captura original antes do enriquecimento.
- CA-D14 — Dados desconhecidos não são convertidos em risco ou custo zero.
- CA-D14 — Fontes podem ser adicionadas sem mudar o modelo conceitual.
- CA-D14 — Comparáveis possuem critérios mínimos de qualidade.
- CA-D14 — Valuation possui confiança e cenários.
- CA-D14 — Custos podem ser observados, estimados ou desconhecidos.
- CA-D14 — Riscos críticos podem impedir recomendação independentemente do score.
- CA-D14 — O enriquecimento é progressivo e proporcional ao potencial.
- CA-D14 — Todas as conclusões relevantes podem ser explicadas por dados/evidências.
- CA-D14 — Dados históricos permanecem disponíveis para auditoria e backtest.

# 34. Princípios Finais

- Dados são matéria-prima; oportunidade é uma interpretação econômica.
- A qualidade da fonte é parte da qualidade da análise.
- Preço é captura; valor é estimativa; oportunidade é tese.
- Desconto sem custo e risco é uma métrica incompleta.
- Desconhecido não significa seguro.
- Score sem confiança pode produzir falsa precisão.
- Quanto mais perto da compra, maior deve ser o nível de evidência.
- O Radar deve preservar o passado para aprender com o resultado.
- Novas fontes e novos tipos de imóvel devem ser extensíveis.
- O objetivo não é coletar o máximo de dados, mas coletar os dados certos para tomar melhores decisões.

# 35. Próximo Documento

Recomendação: Documento 15 — Matriz Mestra de Regras de Decisão e Cenários de Negócio. O objetivo será consolidar, em uma única visão operacional, como os dados enriquecidos atravessam regras eliminatórias, score, confiança, estratégia, alertas e decisão, incluindo cenários positivos, negativos, exceções e conflitos.
