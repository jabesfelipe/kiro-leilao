# Radar_Imobiliario_Documento_de_Negocio_v1.0

🛰️ RADAR IMOBILIÁRIO
DOCUMENTO DE NEGÓCIO — VISÃO, PROCESSOS E REGRAS DE NEGÓCIO
Foco inicial: imóveis da Caixa Econômica Federal
Evolução planejada: múltiplas instituições e fontes
Versão 1.0 — Documento-base do Business

# 1. Sumário Executivo

O Radar Imobiliário é um negócio de inteligência e descoberta de oportunidades imobiliárias. 
Seu propósito é monitorar imóveis disponíveis no mercado, inicialmente provenientes da Caixa Econômica Federal, 
e identificar aqueles que apresentam uma combinação atraente de preço, valor de mercado, liquidez, localização, 
potencial de renda, valorização, custos e riscos.

O Radar não deve ser confundido com um simples catálogo de imóveis baratos. Seu principal ativo é o processo de 
transformar grande volume de ofertas em poucas oportunidades priorizadas, explicadas e comparáveis.

O princípio central é: um imóvel somente é uma oportunidade quando o preço de aquisição, ajustado pelos custos e riscos, 
produz uma margem suficientemente interessante em relação ao valor econômico provável do imóvel e à estratégia escolhida.

## 1.1 Objetivos do negócio

- Encontrar oportunidades antes que o usuário precise procurá-las manualmente.
- Separar desconto aparente de desconto econômico real.
- Permitir estratégias diferentes: renda, revenda, valorização, MCMV/baixa renda, terrenos, casas, apartamentos e outras.
- Evitar que preço baixo isoladamente seja interpretado como oportunidade.
- Dar transparência sobre por que um imóvel foi priorizado, penalizado ou descartado.
- Manter regras e preferências parametrizáveis, sem depender de decisões fixas.
- Construir uma base histórica para comparar preço, comportamento e qualidade das oportunidades ao longo do tempo.
- Começar pela Caixa, mas preservar o conceito de fonte independente para incorporar outros bancos futuramente.

# 2. Escopo de Negócio


| Dentro do escopo | Fora do foco inicial |
|---|---|
| Descoberta de imóveis | Execução da compra |
| Comparação com mercado | Financiamento operacional |
| Classificação de oportunidade | Gestão de obra |
| Avaliação de liquidez | Administração de locação |
| Análise econômica preliminar | Contabilidade do imóvel |
| Monitoramento de preço/status | Tecnologia/arquitetura neste documento |
| Alertas e acompanhamento | Operação de outros bancos no MVP |
| Estratégias configuráveis | Automação jurídica completa no Radar |


# 3. Conceito de Core Business

O Core Business do Radar é o ciclo de decisão: CAPTURAR → ENTENDER → COMPARAR → FILTRAR → VALORAR → 
MEDIR RISCO → PONTUAR → PRIORIZAR → MONITORAR → ENVIAR PARA ANÁLISE.

A fonte do imóvel é secundária. Caixa é apenas a primeira origem. O produto precisa possuir um conceito único de 
“imóvel” e um conceito único de “oportunidade”, independentemente de onde o imóvel foi encontrado.

## 3.1 Definição de oportunidade

Uma oportunidade é um imóvel que, para uma determinada estratégia, apresenta evidências suficientes de que seu 
custo econômico de aquisição está abaixo de seu valor de mercado ajustado, mantendo nível de risco e liquidez 
compatíveis com os parâmetros da estratégia.
Fórmula conceitual:
Oportunidade = Valor econômico provável − Custo econômico total − Ajuste de risco

# 4. Princípios de Negócio


| Princípio | Regra |
|---|---|
| Preço baixo não basta | Todo imóvel deve ser comparado com uma referência de mercado. |
| Desconto da fonte não é verdade absoluta | O desconto divulgado pela Caixa é um indicador, não a conclusão. |
| Tudo deve ser parametrizável | Preferências e critérios devem poder ser alterados sem redefinir o produto. |
| Tipo não define qualidade | 1 quarto, terreno, casa ou MCMV podem ser excelentes ou ruins dependendo do contexto. |
| Liquidez importa | Uma grande margem sem capacidade razoável de saída pode ser uma falsa oportunidade. |
| Risco reduz atratividade | Quanto maior o risco, maior deve ser a compensação econômica exigida. |
| Explicabilidade | Toda classificação deve possuir motivo compreensível. |
| Histórico é parte do negócio | Preço e status devem ser acompanhados no tempo. |
| Confiança importa | Estimativas com poucos dados devem ter menor grau de confiança. |
| Radar antes da análise profunda | O Radar prioriza; a due diligence decide. |


# 5. Jornada Completa do Negócio

- Definir estratégias e preferências do usuário.
- Capturar imóveis da Caixa.
- Validar se o registro é utilizável.
- Normalizar as informações.
- Identificar possíveis duplicidades.
- Registrar preço e histórico.
- Enriquecer o contexto do imóvel.
- Determinar referências de mercado.
- Estimar valor de mercado e confiança.
- Estimar custos econômicos.
- Avaliar liquidez.
- Avaliar localização.
- Avaliar riscos conhecidos.
- Aplicar regras eliminatórias.
- Aplicar regras de pontuação.
- Calcular score por estratégia.
- Classificar a oportunidade.
- Explicar os fatores positivos e negativos.
- Monitorar alterações.
- Notificar quando houver evento relevante.
- Encaminhar oportunidades selecionadas para análise aprofundada.

# 6. Cadastro e Perfil do Imóvel

O Radar deve manter uma visão de negócio do imóvel, independente da fonte.

| Grupo | Informações de negócio |
|---|---|
| Identificação | Identificador, matrícula quando disponível, identificador da fonte, modalidade, situação |
| Localização | Cidade, bairro, endereço, CEP, região e contexto geográfico |
| Características | Tipo, área, quartos, banheiros, vagas, terreno, padrão e demais atributos |
| Preço | Preço atual, preço anterior, avaliação, valor mínimo e datas |
| Mercado | Valor estimado, faixa, preço/m², comparáveis e confiança |
| Renda | Aluguel estimado, despesas e yield |
| Custos | Aquisição, tributos, registros, condomínio, reforma, desocupação e demais custos |
| Risco | Ocupação, documentação, jurídico, condomínio, localização, mercado e outros |
| Histórico | Mudanças de preço, status, avaliação, score e decisões do usuário |


# 7. Fontes de Oportunidades

A Caixa será a fonte inicial. Entretanto, o negócio deve tratar a origem como um atributo do imóvel, e não como parte 
do conceito central. Isso permitirá adicionar outros bancos e fontes sem alterar as regras fundamentais.

| Fase | Fontes |
|---|---|
| Inicial | Caixa Econômica Federal |
| Expansão 1 | Outros bancos com imóveis retomados ou em venda |
| Expansão 2 | Leiloeiros e canais especializados |
| Expansão 3 | Mercado aberto e portais imobiliários |
| Futuro | Parceiros, imobiliárias e novas fontes |


# 8. Estratégias de Investimento

O mesmo imóvel pode ser oportunidade para uma estratégia e não ser oportunidade para outra.

| Estratégia | Objetivo | Principais critérios |
|---|---|---|
| Renda | Gerar renda recorrente | Aluguel, yield, despesas, demanda e liquidez |
| Revenda | Comprar abaixo do mercado e vender | Desconto real, margem, liquidez, reforma e demanda |
| Valorização | Capturar crescimento futuro | Localização, infraestrutura, tendência e preço/m² |
| MCMV / baixa renda | Explorar mercado de alto volume e ticket acessível | Preço, demanda, enquadramento, aluguel e liquidez |
| Terreno | Explorar valor do terreno/potencial construtivo | Zoneamento, área, preço/m², uso e potencial |
| Casa / Sobrado | Renda ou revenda residencial | Terreno, construção, reforma, preço/m² e demanda |


# 9. Parâmetros de Localização

- Localizações prioritárias.
- Localizações aceitáveis.
- Localizações condicionais.
- Localizações bloqueadas.
- Cidades e bairros.
- CEP ou regiões.
- Raio ou área geográfica.
- Infraestrutura desejada.
- Proximidade de transporte e serviços.
- Indicadores de demanda.
- Indicadores de liquidez.
- Condições específicas por estratégia.
Importante: “não atuar em determinada região” deve ser uma preferência configurável. O sistema não deve assumir 
automaticamente que toda região de menor renda é ruim. A análise deve distinguir baixa renda, baixa qualidade, baixa 
liquidez e risco, pois são conceitos diferentes.

# 10. Tipos de Imóvel

- Apartamento
- Casa
- Sobrado
- Terreno/lote
- Sala/conjunto comercial
- Loja
- Galpão
- Outros
Nenhum tipo deve ser universalmente excluído. Critérios específicos podem existir por estratégia. Por exemplo, 
um apartamento de 1 quarto pode ter alta atratividade em uma região com forte demanda de locação, enquanto pode ter 
baixa atratividade em outra região.

# 11. Conceito de Desconto


| Indicador | Definição de negócio |
|---|---|
| Desconto da fonte | Diferença entre o preço divulgado e o valor de referência divulgado pela fonte. |
| Desconto de mercado | Diferença entre o preço de aquisição e o valor estimado de mercado. |
| Desconto líquido | Diferença entre custo econômico total e valor estimado de mercado. |
| Margem de segurança | Quanto valor econômico permanece depois de considerar o custo total. |
| Desconto efetivo | Desconto que continua existindo após custos e ajustes relevantes. |

O desconto de mercado e a margem após custos devem ter prioridade sobre o desconto promocional divulgado pela origem.

# 12. Valor de Mercado

O Radar deve estimar o valor econômico provável do imóvel a partir de referências comparáveis. O valor deve ser 
tratado como estimativa, não como verdade absoluta.
- Priorizar comparáveis realmente semelhantes.
- Dar maior peso a imóveis do mesmo condomínio quando existirem.
- Considerar proximidade geográfica.
- Considerar área, quartos, vagas, padrão e estado.
- Separar preço anunciado de preço efetivamente observado quando houver dados confiáveis.
- Informar intervalo de valor, não apenas um número.
- Informar nível de confiança.
- Reduzir confiança quando houver poucos comparáveis ou comparáveis fracos.

# 13. Confiança da Avaliação


| Nível | Interpretação |
|---|---|
| Muito alta | Muitos comparáveis relevantes e grande semelhança. |
| Alta | Boa quantidade e qualidade de comparáveis. |
| Média | Dados suficientes, porém com diferenças relevantes. |
| Baixa | Poucos comparáveis ou mercado pouco transparente. |
| Insuficiente | Não há evidência suficiente para recomendar pela margem de mercado. |


# 14. Custo Econômico Total

O Radar deve buscar aproximar o custo real da oportunidade, e não somente o preço anunciado.
- Preço de aquisição.
- Comissão, quando aplicável.
- ITBI.
- Registro e documentação.
- Condomínio e eventuais atrasos relevantes.
- IPTU e eventuais débitos relevantes.
- Reforma.
- Desocupação, quando aplicável.
- Custos jurídicos.
- Custos financeiros.
- Reserva para imprevistos.
- Outros custos parametrizados.

# 15. Liquidez

Liquidez representa a capacidade de transformar o imóvel em dinheiro dentro de um prazo e faixa de preço razoáveis. 
Ela deve ser analisada de forma contextual.
- Quantidade de imóveis concorrentes.
- Quantidade de compradores potenciais.
- Histórico de tempo de exposição, quando disponível.
- Faixa de preço.
- Localização.
- Tipo e características.
- Demanda de aluguel.
- Facilidade de financiamento.
- Diferença entre preço pedido e preço de mercado.
Classificação: 🟢 Alta | 🟡 Média | 🟠 Baixa | 🔴 Muito baixa.

# 16. Risco


| Categoria | Pergunta de negócio |
|---|---|
| Localização | Existe fator local que prejudique demanda, segurança, valorização ou saída? |
| Ocupação | Existe dificuldade ou incerteza relevante para posse/uso? |
| Documentação | Existem lacunas ou restrições relevantes? |
| Jurídico | Existem processos ou riscos que alterem a decisão? |
| Condomínio | Existem custos, dívidas ou problemas relevantes? |
| Reforma | O custo ou incerteza pode destruir a margem? |
| Mercado | A avaliação de mercado é confiável? |
| Liquidez | Há compradores suficientes para a estratégia? |

O Radar deve distinguir “risco desconhecido” de “risco baixo”. Ausência de informação não significa ausência de risco.

# 17. Hard Rules e Soft Rules

As regras devem ser divididas em dois grupos.

## 17.1 Hard Rules

Falhas eliminam ou bloqueiam a recomendação.
- Região explicitamente bloqueada.
- Tipo não permitido para determinada estratégia.
- Preço acima do limite da estratégia.
- Risco crítico.
- Dados mínimos ausentes para uma estratégia que exija esses dados.
- Outra condição explicitamente definida como eliminatória.

## 17.2 Soft Rules

Afetam o score, mas não necessariamente eliminam.
- Liquidez média.
- Condomínio acima do ideal.
- Reforma moderada.
- Desconto abaixo do alvo, mas ainda aceitável.
- Valorização incerta.
- Poucos comparáveis.

# 18. Motor de Score

O score deve ser relativo à estratégia.

| Dimensão | Exemplo de avaliação |
|---|---|
| Desconto real | Quanto abaixo do valor de mercado o custo total está. |
| Margem | Quanto sobra após custos. |
| Liquidez | Facilidade esperada de saída. |
| Localização | Aderência à região desejada. |
| Renda | Qualidade do retorno de aluguel. |
| Valorização | Potencial de crescimento. |
| Risco | Risco total identificado. |
| Confiança | Qualidade das evidências usadas. |

Os pesos devem ser configuráveis por estratégia. O score deve ser acompanhado de explicação.

# 19. Exemplo de Estratégia — Revenda


| Parâmetro | Exemplo |
|---|---|
| Desconto real mínimo | 25% |
| Liquidez mínima | Média |
| Margem mínima | 20% |
| Risco máximo | Médio |
| Reforma máxima | Definida pelo usuário |
| Localização | Regiões prioritárias ou condicionais |
| Confiança mínima | Definida pelo usuário |

Os números acima são exemplos iniciais de parametrização, não regras definitivas do negócio.

# 20. Exemplo de Estratégia — Renda


| Parâmetro | Exemplo |
|---|---|
| Yield mínimo | Configurável |
| Liquidez mínima | Média |
| Condomínio | Limite configurável |
| Aluguel | Estimativa com confiança mínima |
| Localização | Demanda de locação relevante |
| Risco | Máximo configurável |


# 21. Exemplo de Estratégia — MCMV / Baixa Renda

O objetivo não é simplesmente procurar imóveis baratos. A estratégia deve identificar imóveis acessíveis com 
mercado consumidor relevante e capacidade de geração de retorno.
- Faixa de preço configurável.
- Demanda local.
- Liquidez.
- Aluguel compatível.
- Facilidade de revenda.
- Infraestrutura.
- Condição do imóvel.
- Margem após custos.

# 22. Exemplo de Estratégia — Terrenos

- Preço por m² comparável.
- Área.
- Frente.
- Profundidade.
- Topografia.
- Infraestrutura.
- Zoneamento.
- Uso permitido.
- Potencial construtivo.
- Possibilidade de desenvolvimento.
- Liquidez.

# 23. Classificação Final


| Classificação | Significado |
|---|---|
| 🔥 Excelente oportunidade | Atende fortemente à estratégia e apresenta margem/riscos favoráveis. |
| 🟢 Boa oportunidade | Atende à estratégia com pontos de atenção controláveis. |
| 🟡 Monitorar | Pode se tornar interessante com queda de preço ou melhora de dados. |
| 🟠 Oportunidade condicional | Somente faz sentido sob determinadas condições. |
| 🔴 Rejeitada | Não atende às regras ou possui risco/margem incompatível. |
| ⚪ Inconclusiva | Dados insuficientes para uma conclusão confiável. |


# 24. Monitoramento

O Radar não termina após a primeira avaliação. O imóvel permanece em ciclo de acompanhamento.

| Evento | Ação de negócio |
|---|---|
| Novo imóvel | Avaliar e classificar. |
| Queda de preço | Recalcular oportunidade. |
| Aumento de preço | Recalcular e eventualmente retirar prioridade. |
| Mudança de status | Reavaliar elegibilidade. |
| Novos comparáveis | Recalcular valor de mercado. |
| Mudança de aluguel | Recalcular estratégia de renda. |
| Mudança de risco | Recalcular score. |
| Entrada em leilão/nova praça | Gerar evento relevante. |


# 25. Alertas

- Nova oportunidade acima do score configurado.
- Desconto real atingiu o mínimo.
- Preço caiu significativamente.
- Score aumentou.
- Imóvel entrou em nova modalidade/praça.
- Valor de mercado foi atualizado.
- Liquidez mudou.
- Uma oportunidade anteriormente rejeitada passou a atender à estratégia.

# 26. Explicabilidade

Toda oportunidade deverá responder: “Por que devo olhar para este imóvel?”
Exemplo:
- 31% abaixo do valor de mercado estimado.
- Liquidez alta.
- Região prioritária.
- Condomínio compatível.
- Margem estimada de R$ 72 mil após custos.
- Yield estimado de 0,80% ao mês.
- Ponto de atenção: reforma estimada em R$ 25 mil.
- Confiança da avaliação: alta.

# 27. Histórico e Ciclo de Vida


| Estado | Descrição |
|---|---|
| Capturado | Imóvel encontrado na fonte. |
| Validado | Dados mínimos confirmados. |
| Avaliado | Mercado/custos/riscos preliminares calculados. |
| Interessante | Atende parcialmente aos critérios. |
| Oportunidade | Atende aos critérios da estratégia. |
| Monitorando | Usuário decidiu acompanhar. |
| Análise profunda | Entrou no processo de due diligence. |
| Descartado | Não interessa ou falhou nas regras. |
| Adquirido | Usuário realizou aquisição. |
| Encerrado | Saiu do mercado ou não está mais disponível. |


# 28. Decisão do Usuário

O sistema deve separar a classificação automática da decisão humana.
- Interessado.
- Não interessado.
- Monitorar.
- Analisar.
- Descartar.
- Favorito.
- Já analisado.
- Adquirido.
A decisão do usuário deve gerar histórico e, futuramente, poderá ser utilizada para melhorar recomendações.

# 29. Regras de Negócio Transversais

- Um imóvel pode participar de várias estratégias simultaneamente.
- Um imóvel pode ser oportunidade para uma estratégia e rejeitado para outra.
- Uma fonte não determina a qualidade da oportunidade.
- O valor de avaliação da fonte não deve ser tratado automaticamente como valor de mercado.
- Uma estimativa de mercado sem confiança suficiente não deve sustentar uma recomendação forte.
- Desconto deve ser analisado depois dos custos sempre que os dados permitirem.
- Risco desconhecido não deve ser classificado automaticamente como risco baixo.
- Localização deve poder ser configurada por cidade, bairro, região ou área.
- Filtros podem ser globais ou específicos de uma estratégia.
- Alterações de regras devem gerar nova versão e permitir rastrear a decisão.
- Regras eliminatórias têm precedência sobre score.
- Score não elimina a necessidade de análise profunda.
- Dados históricos devem preservar as condições existentes no momento da avaliação.
- O Radar deve explicar tanto recomendações quanto rejeições.
- Novas fontes devem aderir ao mesmo modelo conceitual de oportunidade.

# 30. Exemplo Completo de Avaliação


| Item | Valor |
|---|---|
| Tipo | Apartamento, 3 quartos |
| Preço Caixa | R$ 191.651 |
| Avaliação Caixa | R$ 313.000 |
| Desconto da fonte | 38,77% |
| Mercado estimado | R$ 285.000 |
| Custos adicionais estimados | R$ 28.000 |
| Custo econômico total | R$ 219.651 |
| Desconto líquido vs mercado | 22,93% |
| Margem estimada | R$ 65.349 |
| Liquidez | Alta |
| Confiança valuation | Alta |
| Score hipotético | 87/100 |
| Classificação | 🟢 Boa oportunidade |

Este exemplo é apenas ilustrativo. Os valores de mercado, custos e score reais somente devem ser calculados após 
a coleta e validação das evidências necessárias.

# 31. Exemplo de Falsa Oportunidade


| Item | Valor |
|---|---|
| Avaliação da fonte | R$ 350.000 |
| Preço | R$ 175.000 |
| Desconto divulgado | 50% |
| Mercado real estimado | R$ 205.000 |
| Custos adicionais | R$ 25.000 |
| Custo total | R$ 200.000 |
| Margem | R$ 5.000 |
| Liquidez | Baixa |
| Conclusão | 🔴 Não é oportunidade apesar do desconto de 50% |

Este é exatamente o tipo de falso positivo que o Radar deve eliminar.

# 32. Indicadores de Sucesso do Negócio


| KPI | O que mede |
|---|---|
| Oportunidades relevantes/mês | Capacidade de descoberta. |
| Taxa de falso positivo | Qualidade do Radar. |
| Taxa de oportunidades analisadas | Qualidade da priorização. |
| Margem média das oportunidades | Qualidade econômica. |
| Desconto real médio | Atratividade. |
| Tempo entre captura e alerta | Velocidade do Radar. |
| % de oportunidades com alta confiança | Qualidade dos dados. |
| Oportunidades que chegaram à aquisição | Conversão de descoberta em resultado. |
| Resultado realizado | Validação final do negócio. |


# 33. Evolução para Outros Bancos

Quando novas instituições forem incorporadas, o processo de negócio não deve ser duplicado. A instituição passa a 
ser apenas uma origem adicional de imóveis.
Exemplo conceitual:

| Origem | Mesmo processo |
|---|---|
| Caixa | Captura → avaliação → regras → score → alerta |
| Banco B | Captura → avaliação → regras → score → alerta |
| Banco C | Captura → avaliação → regras → score → alerta |
| Leiloeiro | Captura → avaliação → regras → score → alerta |

A vantagem competitiva permanece no Radar, não na fonte.

# 34. Roadmap de Negócio


| Fase | Entrega de negócio |
|---|---|
| Fase 0 | Definição das regras e estratégias. |
| Fase 1 | Radar Caixa com classificação básica. |
| Fase 2 | Valor de mercado e comparáveis. |
| Fase 3 | Custos, liquidez, risco e score. |
| Fase 4 | Monitoramento e alertas. |
| Fase 5 | Análise aprofundada / due diligence. |
| Fase 6 | Novos bancos. |
| Fase 7 | Mercado aberto. |
| Fase 8 | IA para valuation, liquidez e descoberta de anomalias. |


# 35. Decisões de Negócio Ainda Pendentes

- Definir quais cidades serão prioritárias no primeiro piloto.
- Definir os perfis de investimento que serão habilitados no MVP.
- Definir os limites iniciais de risco por estratégia.
- Definir a metodologia de classificação de liquidez.
- Definir a metodologia de valuation e seus níveis de confiança.
- Definir quais custos entram obrigatoriamente no custo econômico.
- Definir os limites mínimos de desconto/margem.
- Definir política para dados insuficientes.
- Definir quais regiões serão bloqueadas, condicionais ou prioritárias.
- Definir quais eventos geram alerta.
- Definir o conjunto mínimo de dados para uma oportunidade ser recomendada.

# 36. Documento 1 — Próxima Especificação

O próximo documento deverá transformar esta visão em um verdadeiro Manual de Regras do Radar. Ele deverá detalhar 
as fórmulas, faixas, pesos, precedências, exemplos e cenários de cada decisão.
- Modelo matemático de valor de mercado.
- Seleção e peso de comparáveis.
- Cálculo de desconto real.
- Cálculo de custo econômico.
- Cálculo de margem de segurança.
- Cálculo de yield.
- Modelo de liquidez.
- Modelo de risco.
- Modelo de confiança.
- Score por estratégia.
- Hard rules.
- Soft rules.
- Regras de localização.
- Regras MCMV/baixa renda.
- Regras para terrenos.
- Regras para apartamentos de 1, 2, 3+ quartos.
- Regras para casas e sobrados.
- Regras de monitoramento.
- Regras de alertas.
- Exemplos completos de decisão.

# 37. Conclusão

O Radar deve ser concebido como o núcleo do negócio imobiliário: uma máquina de descoberta e priorização de 
oportunidades. A Caixa é apenas o ponto de partida.

O diferencial não será possuir uma lista maior de imóveis, mas possuir um processo melhor para responder, de forma 
consistente e explicável:

1. O imóvel está barato em relação ao mercado?
2. Depois dos custos, ainda existe margem?
3. Existe liquidez suficiente?
4. A localização é compatível com a estratégia?
5. O risco é aceitável?
6. Os dados possuem confiança suficiente?
7. A oportunidade é melhor que as alternativas disponíveis?
8. Vale a pena gastar tempo com uma análise profunda?

Se o Radar responder essas perguntas bem, o produto terá valor independentemente da fonte dos imóveis.

O objetivo final é sair de “procurar imóveis” para “receber as melhores oportunidades já filtradas e justificadas”.
