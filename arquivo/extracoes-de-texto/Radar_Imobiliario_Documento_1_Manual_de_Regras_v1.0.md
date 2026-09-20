# Radar_Imobiliario_Documento_1_Manual_de_Regras_v1.0

📐 DOCUMENTO 1 — MANUAL DE REGRAS DO RADAR
Modelo de oportunidade, valuation, liquidez, risco, score e decisão
Foco inicial: Caixa Econômica Federal • Estratégias configuráveis • Versão 1.0

# 1. Objetivo deste documento

Transformar a visão do Radar em regras de negócio operacionais. O documento define como avaliar um imóvel, quais evidências considerar, quando rejeitar, quando monitorar e quando priorizar. Valores numéricos apresentados como exemplos são pontos de partida e devem ser calibrados por dados reais e backtest.

# 2. Princípio central

O Radar não procura simplesmente imóveis baratos. Procura imóveis cujo custo econômico total seja suficientemente inferior ao valor econômico provável, com liquidez, risco, confiança e aderência à estratégia compatíveis.

# 3. Definição de oportunidade

Oportunidade é um imóvel que satisfaz requisitos mínimos de elegibilidade e, para pelo menos uma estratégia, apresenta vantagem econômica suficiente, liquidez compatível, risco aceitável e evidência com confiança adequada.

# 4. Camadas de decisão


| Camada | Pergunta | Saída |
|---|---|---|
| Elegibilidade | Pode participar da estratégia? | Sim/Não |
| Dados | Há informação suficiente? | Confiança |
| Mercado | Quanto vale? | Valor + faixa |
| Economia | Depois dos custos, sobra margem? | Margem |
| Liquidez | Existe saída razoável? | Classe |
| Risco | O que pode destruir a tese? | Risco |
| Estratégia | Para qual objetivo serve? | Perfil |
| Score | Quão forte é? | 0–100 |
| Ação | O que fazer? | Priorizar/monitorar/rejeitar |


# 5. Glossário


| Termo | Regra de negócio |
|---|---|
| Preço de aquisição | Valor necessário para adquirir conforme a oferta. |
| Avaliação da fonte | Valor informado pela Caixa ou outra origem. |
| Valor de mercado | Estimativa prudente do valor em condições normais. |
| Custo econômico total | Preço mais custos necessários e reservas relevantes. |
| Desconto de mercado | Diferença entre preço e valor de mercado. |
| Desconto líquido | Diferença entre custo total e valor de mercado. |
| Margem de segurança | Folga entre valor de mercado e custo total. |
| Liquidez | Facilidade e velocidade esperadas de saída. |
| Confiança | Qualidade das evidências usadas. |
| Hard rule | Regra eliminatória. |
| Soft rule | Regra que altera score. |
| Score | Nota relativa à estratégia. |


# 6. Hierarquia das regras

- Hard rules são avaliadas antes do score.
- Regras específicas da estratégia prevalecem sobre regras genéricas.
- Dados conflitantes reduzem confiança.
- Risco crítico não pode ser mascarado por score alto.
- Quando não houver evidência suficiente, usar 'inconclusivo', não inventar certeza.

# 7. Elegibilidade


| Critério | Comportamento |
|---|---|
| Fonte habilitada | Aceitar. |
| Tipo permitido | Verificar estratégia. |
| Localização | Aplicar prioridade/bloqueio. |
| Faixa de preço | Aplicar limite. |
| Dados mínimos | Exigir o necessário. |
| Risco crítico | Bloquear se configurado. |
| Conflito de estratégia | Rejeitar apenas naquela estratégia. |


# 8. Localização

Localização é um atributo parametrizável e contextual. O sistema deve permitir cidade, bairro, CEP, microregião, raio e áreas bloqueadas.

| Classe | Significado |
|---|---|
| A — Prioritária | Região desejada. |
| B — Boa | Adequada. |
| C — Condicional | Aceitar com compensação econômica. |
| D — Indesejada | Baixa aderência. |
| E — Bloqueada | Hard rule. |

Não se deve confundir baixa renda com baixa qualidade, baixa liquidez ou alto risco. A estratégia MCMV/baixa renda deve ser tratada com regras próprias.

# 9. Tipos de imóvel

- Apartamento
- Casa
- Sobrado
- Terreno/lote
- Sala/conjunto comercial
- Loja
- Galpão
- Outros
Nenhum tipo é universalmente ruim. Apartamento de 1 quarto, terreno ou imóvel MCMV podem ser excelentes quando o contexto econômico justificar.

# 10. Valor de mercado

O valuation deve estimar quanto o imóvel provavelmente valeria em condições normais, usando evidências comparáveis e ajustes. A avaliação da Caixa é referência auxiliar, não verdade absoluta.

## 10.1 Hierarquia de comparáveis


| Prioridade | Evidência |
|---|---|
| 1 | Mesmo condomínio e características muito semelhantes. |
| 2 | Mesmo condomínio com diferenças ajustáveis. |
| 3 | Mesma microregião. |
| 4 | Mesmo bairro. |
| 5 | Regiões próximas comparáveis. |
| 6 | Modelos amplos quando faltarem dados. |


## 10.2 Critérios de comparação

- distância geográfica
- tipo
- área
- quartos
- suítes
- banheiros
- vagas
- padrão
- idade
- estado
- condomínio
- características relevantes
Comparáveis claramente fora do padrão devem ser excluídos ou fortemente penalizados.

# 11. Faixa de valor

Sempre que possível, o Radar deve produzir cenário conservador, base e otimista.

| Cenário | Exemplo |
|---|---|
| Conservador | R$ 295.000 |
| Base | R$ 315.000 |
| Otimista | R$ 335.000 |

A recomendação econômica deve ser resistente ao cenário otimista; idealmente deve funcionar com premissas conservadoras.

# 12. Confiança do valuation


| Confiança | Interpretação | Uso |
|---|---|---|
| 90–100 | Evidência muito forte | Pode sustentar prioridade. |
| 75–89 | Boa evidência | Recomendação forte. |
| 60–74 | Razoável | Monitorar/analisar. |
| 40–59 | Fraca | Evitar conclusão forte. |
| 0–39 | Insuficiente | Inconclusiva. |

A confiança deve considerar quantidade, qualidade, atualidade e semelhança dos comparáveis.

# 13. Descontos


| Indicador | Fórmula conceitual |
|---|---|
| Desconto da fonte | 1 − preço ÷ avaliação da fonte |
| Desconto de mercado | 1 − preço ÷ valor de mercado |
| Desconto líquido | 1 − custo total ÷ valor de mercado |
| Margem % | (valor de mercado − custo total) ÷ valor de mercado |

O desconto líquido e a margem são mais importantes para a decisão econômica que o desconto promocional da fonte.

# 14. Custo econômico total

Deve representar o capital necessário para colocar o imóvel em condição de uso, locação ou venda, conforme a estratégia.
- preço de aquisição
- ITBI
- registro/documentação
- comissão
- condomínio relevante
- IPTU relevante
- reforma
- desocupação
- custos jurídicos
- custos financeiros
- reserva para imprevistos
- outros custos parametrizados

# 15. Reforma


| Nível | Exemplos |
|---|---|
| Nenhuma | Pronto ou sem necessidade identificada. |
| Leve | Pintura e pequenos reparos. |
| Média | Cozinha/banheiros e instalações parciais. |
| Pesada | Reforma ampla/estrutural. |
| Incerta | Escopo desconhecido; aplicar reserva adicional. |

A reforma deve ser uma faixa de custo quando houver incerteza, e não uma falsa precisão.

# 16. Margem de segurança

Margem = Valor de mercado − Custo econômico total
Quanto menor a confiança do valuation ou maior o risco, maior deve ser a margem exigida.

# 17. Liquidez


| Classe | Descrição |
|---|---|
| Alta | Mercado amplo e boa saída esperada. |
| Média | Demanda existente, mas maior prazo/negociação. |
| Baixa | Poucos compradores ou características pouco procuradas. |
| Muito baixa | Saída difícil ou dependente de grande desconto. |

- localização
- faixa de preço
- tipo
- área
- quartos/vagas
- condomínio
- financiabilidade
- concorrência
- demanda de aluguel
- histórico de exposição
Liquidez é contextual à estratégia: pode ser suficiente para renda e insuficiente para flip, por exemplo.

# 18. Risco


| Dimensão | Exemplos |
|---|---|
| Localização | Fatores que prejudicam demanda/saída. |
| Ocupação | Incerteza de posse/uso. |
| Documentação | Pendências/restrições. |
| Jurídico | Processos ou situações relevantes. |
| Condomínio | Débitos, obras ou custos extraordinários. |
| Reforma | Incerteza de custo. |
| Mercado | Poucos comparáveis/dispersão. |
| Liquidez | Mercado estreito. |

Risco desconhecido não é risco baixo. Deve ser registrado como desconhecido e reduzir a confiança.

# 19. Hard Rules


| Condição | Resultado |
|---|---|
| Localização bloqueada | Rejeitar estratégia. |
| Risco crítico eliminatório | Rejeitar. |
| Preço fora da faixa | Rejeitar. |
| Dados mínimos ausentes | Inconclusiva/rejeitar conforme estratégia. |
| Liquidez abaixo do mínimo | Rejeitar quando requisito. |
| Margem abaixo do mínimo absoluto | Rejeitar. |
| Tipo incompatível | Rejeitar somente naquela estratégia. |


# 20. Soft Rules


| Condição | Efeito |
|---|---|
| Liquidez média | Reduz score. |
| Condomínio alto | Reduz retorno. |
| Reforma média | Reduz margem. |
| Poucos comparáveis | Reduz confiança. |
| Localização condicional | Reduz score/exige prêmio. |
| Desconto abaixo do alvo | Reduz score. |
| Valorização incerta | Reduz componente de valorização. |


# 21. Score por estratégia

Score de 0 a 100. Cada estratégia terá pesos próprios.

| Componente | Revenda — exemplo | Renda — exemplo |
|---|---|---|
| Desconto real | 30% | 15% |
| Margem | 20% | 15% |
| Liquidez | 20% | 20% |
| Localização | 15% | 20% |
| Renda | 0% | 20% |
| Valorização | 10% | 5% |
| Risco | 5% | 5% |

Pesos são ilustrativos e devem ser calibrados. A soma de cada estratégia deve ser 100%.

# 22. Confiança e score

Score ajustado = Score bruto × fator de confiança

| Confiança | Fator ilustrativo |
|---|---|
| Muito alta | 1,00 |
| Alta | 0,95 |
| Média | 0,88 |
| Baixa | 0,75 |
| Muito baixa | 0,60 ou inconclusiva |

Os fatores são provisórios e devem ser validados por backtest.

# 23. Classificação


| Score | Classe | Ação |
|---|---|---|
| 90–100 | 🔥 Excelente | Prioridade máxima |
| 80–89 | 🟢 Forte | Analisar rapidamente |
| 70–79 | 🟡 Interessante | Monitorar/analisar |
| 60–69 | 🟠 Condicional | Somente com tese específica |
| <60 | 🔴 Fraca | Não priorizar |

Limites podem variar por estratégia.

# 24. Estratégia — Renda


| Parâmetro | Regra de negócio |
|---|---|
| Objetivo | Renda recorrente. |
| Yield | Mínimo configurável. |
| Liquidez | >= média, salvo exceção. |
| Demanda de locação | Mínimo configurável. |
| Condomínio | Limite configurável. |
| Risco | Máximo configurável. |
| Tipos | Apartamento/casa/sobrado e outros conforme perfil. |

Yield bruto mensal = aluguel mensal ÷ custo econômico total

# 25. Estratégia — Revenda


| Parâmetro | Regra ilustrativa |
|---|---|
| Objetivo | Comprar abaixo do mercado para vender. |
| Desconto líquido alvo | >= 25% |
| Margem mínima | >= 20% |
| Liquidez | >= média |
| Risco | <= médio |
| Localização | A/B; C somente com prêmio |
| Reforma | Dentro de limite configurável |


# 26. Estratégia — MCMV / baixa renda

A estratégia deve procurar demanda ampla e ticket acessível, não simplesmente o menor preço.
- faixa de preço
- demanda
- liquidez
- aluguel
- facilidade de revenda
- infraestrutura
- condição
- margem
- risco
É permitido aceitar desconto menor que em um flip se a combinação de demanda, liquidez e renda produzir tese superior.

# 27. Estratégia — Terrenos

- preço/m²
- área
- frente
- profundidade
- topografia
- infraestrutura
- zoneamento
- uso permitido
- potencial construtivo
- possibilidade de desenvolvimento
- liquidez
Yield de aluguel não é requisito quando não fizer sentido para a natureza do ativo.

# 28. Estratégia — Casas e sobrados

- terreno
- área construída
- padrão
- vagas
- estado
- reforma
- localização
- preço/m²
- liquidez
- demanda
- aluguel quando aplicável

# 29. Estratégia — apartamento de 1 quarto

Não existe rejeição automática. Avaliar demanda, localização, ticket, aluguel, liquidez, condomínio e público comprador.

# 30. Oportunidade relativa

O Radar deve comparar a oportunidade com as demais oportunidades disponíveis. Um imóvel pode perder prioridade porque surgiu outro melhor, mesmo sem piorar.

# 31. Explicabilidade

Toda classificação deve apresentar: pontos positivos, pontos de atenção, riscos, confiança e próxima ação.
- “31% abaixo do mercado”
- “liquidez alta”
- “região prioritária”
- “margem de R$ 72 mil”
- “reforma estimada em R$ 25 mil”
- “confiança alta”

# 32. Ciclo de vida

- Capturado
- Validado
- Avaliado
- Interessante
- Oportunidade
- Monitorando
- Análise profunda
- Aprovado
- Descartado
- Adquirido
- Encerrado
O usuário pode interromper o fluxo a qualquer momento. O imóvel permanece no histórico.

# 33. Monitoramento


| Evento | Ação |
|---|---|
| Novo imóvel | Avaliar. |
| Queda de preço | Recalcular. |
| Aumento de preço | Recalcular. |
| Mudança de status | Reavaliar elegibilidade. |
| Novos comparáveis | Recalcular valuation. |
| Mudança de aluguel | Recalcular renda. |
| Novo risco | Recalcular score. |
| Nova praça | Gerar evento relevante. |


# 34. Alertas

- nova oportunidade
- desconto atingiu alvo
- queda relevante de preço
- score ultrapassou limite
- score aumentou
- nova praça/modalidade
- valuation melhorou
- liquidez melhorou
- risco relevante detectado
- imóvel saiu do mercado

# 35. Insuficiência de dados


| Situação | Resultado |
|---|---|
| Poucos comparáveis | Valuation inconclusivo ou baixa confiança. |
| Sem aluguel | Não inventar yield. |
| Localização incompleta | Reduzir confiança/bloquear estratégia. |
| Custos críticos desconhecidos | Reserva ou não recomendar. |
| Risco não investigado | Marcar desconhecido. |
| Dados contraditórios | Registrar inconsistência. |


# 36. Atualidade dos dados

Dados voláteis devem ser revalidados com maior frequência.

| Dado | Prioridade de atualização |
|---|---|
| Preço/status | Muito alta |
| Oferta | Muito alta |
| Aluguel | Alta |
| Comparáveis | Alta |
| Liquidez | Média/alta |
| Características | Baixa salvo correção |
| Risco/documentação | Sempre que houver evidência nova |


# 37. Versionamento

Cada avaliação deve guardar a estratégia, versão, regras, dados, valuation, confiança, score e data. Isso permite reproduzir por que um imóvel foi considerado oportunidade.

# 38. Conflitos de regras

- Hard rule vence score.
- Regra específica vence regra genérica.
- Versão ativa mais recente prevalece.
- Dados conflitantes reduzem confiança.
- Risco crítico não pode ser compensado por pontos.
- Incerteza deve gerar condição ou inconclusão.

# 39. Cenários de negócio


| Cenário | Resultado esperado |
|---|---|
| 50% de desconto Caixa, mercado só 15% abaixo | 🔴 Falsa oportunidade |
| 25% abaixo do mercado, alta liquidez, risco baixo | 🟢 Forte oportunidade |
| MCMV, desconto moderado, demanda e yield fortes | 🟢 Pode ser excelente |
| Terreno sem yield, mas zoneamento/potencial muito fortes | 🟢 Avaliar como terreno |
| 1 quarto em mercado de locação forte | 🟢 Pode ser oportunidade |
| 45% abaixo, liquidez muito baixa e valuation incerto | 🔴 Não priorizar |


# 40. Regra de prudência econômica

Uma oportunidade forte deve ser resistente a cenários conservadores. Quanto maior a incerteza, maior deve ser a margem exigida. O Radar deve evitar teses que dependam de venda perfeita, valorização extraordinária ou custo de reforma irrealisticamente baixo.

# 41. Backtest

O backtest é obrigatório antes de considerar pesos e limites definitivos.
- Reproduzir o estado histórico.
- Usar somente dados disponíveis naquela data.
- Calcular valuation.
- Aplicar regras.
- Calcular score.
- Registrar classificação.
- Comparar com resultado posterior.
- Medir falsos positivos/negativos.
- Calibrar novamente.
O objetivo é validar o processo, não apenas fazer o score parecer coerente.

# 42. KPIs das regras


| Indicador | Objetivo |
|---|---|
| Precisão | % de oportunidades sinalizadas que se sustentam. |
| Falso positivo | Sinalizações que não se confirmam. |
| Falso negativo | Boas oportunidades não detectadas. |
| Margem média | Qualidade econômica. |
| Confiança média | Qualidade das evidências. |
| Tempo até alerta | Velocidade. |
| Conversão para análise | Qualidade da priorização. |
| Conversão para aquisição | Valor efetivo gerado. |


# 43. Regras que devem ser evitadas

- usar somente desconto Caixa
- usar um único preço/m² como verdade
- tratar bairro inteiro como homogêneo
- assumir que baixa renda é ruim
- assumir que alto padrão é bom
- eliminar 1 quarto automaticamente
- exigir yield de terreno
- tratar informação ausente como risco baixo
- deixar score esconder risco crítico
- usar dados antigos como atuais
- apresentar estimativa como certeza

# 44. Saída padrão da avaliação


| Campo | Exemplo |
|---|---|
| Classificação | 🔥 Excelente oportunidade |
| Estratégia | Revenda |
| Preço | R$ 220.000 |
| Mercado conservador | R$ 300.000 |
| Custo total | R$ 240.000 |
| Desconto líquido | 20% |
| Margem | R$ 60.000 |
| Liquidez | Alta |
| Risco | Baixo |
| Confiança | Alta |
| Score bruto | 93 |
| Score ajustado | 90 |
| Ponto positivo | Margem + liquidez |
| Atenção | Reforma |
| Próxima ação | Análise aprofundada |


# 45. Matriz final de decisão


| Economia | Liquidez | Risco | Confiança | Decisão |
|---|---|---|---|---|
| Excelente | Alta | Baixo | Alta | 🔥 Prioridade máxima |
| Boa | Alta | Baixo/Médio | Alta | 🟢 Priorizar |
| Boa | Média | Médio | Média | 🟡 Analisar |
| Excelente | Baixa | Médio | Baixa | 🟠 Condicional |
| Excelente | Muito baixa | Alto | Baixa | 🔴 Evitar |
| Fraca | Alta | Baixo | Alta | 🟡 Monitorar |
| Fraca | Baixa | Qualquer | Qualquer | 🔴 Rejeitar |
| Desconhecida | Qualquer | Desconhecido | Baixa | ⚪ Inconclusiva |


# 46. Governança

- revisar regras periodicamente
- registrar alterações
- comparar desempenho antes/depois
- evitar mudanças simultâneas sem controle
- executar backtest para mudanças estruturais
- identificar regras causadoras de falsos positivos
- recalibrar pesos com evidências reais

# 47. Próximo documento

Documento 2 — Modelo de Valuation e Mercado. Deve aprofundar seleção e ponderação de comparáveis, ajustes de área/quartos/vagas/padrão/localização, preço/m², outliers, faixa conservadora/base/otimista, confiança, mercados com poucos dados, atualização temporal e exemplos completos.

# 48. Conclusão

O Manual estabelece o Radar como uma máquina de decisão orientada a evidências. A oportunidade não nasce do desconto anunciado;
nasce da combinação entre preço, valor econômico, custo total, margem, liquidez, localização, risco, confiança e estratégia.

A Caixa é apenas a primeira fonte. O mesmo conjunto de princípios deve funcionar para outros bancos e fontes futuras.

O próximo grande desafio de negócio é o valuation: descobrir de maneira consistente quanto o imóvel realmente vale. Essa será a
base para quase todas as demais decisões do Radar.
