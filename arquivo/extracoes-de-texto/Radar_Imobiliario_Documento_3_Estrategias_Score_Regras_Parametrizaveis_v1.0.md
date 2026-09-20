# Radar_Imobiliario_Documento_3_Estrategias_Score_Regras_Parametrizaveis_v1.0

Radar Imobiliário
Documento 3 — Estratégias, Score e Catálogo de Regras Parametrizáveis | v1.0
Documento de negócio. Foco exclusivo em decisões, critérios, regras, parâmetros, pontuação e comportamento esperado do Radar. Arquitetura e tecnologia ficam fora deste documento.
Princípio central: preço é o dado; oportunidade é a análise.

# 1. Objetivo do documento

Este documento transforma os princípios dos Documentos 1 e 2 em um modelo operacional de decisão. Ele define como o Radar interpreta uma oportunidade, aplica regras, calcula score, adapta a análise à estratégia do investidor e determina o que deve ser priorizado, monitorado ou descartado.
O objetivo não é criar uma fórmula única que diga se um imóvel é bom. O objetivo é criar um sistema de decisão configurável, no qual a mesma propriedade possa receber classificações diferentes conforme a estratégia escolhida.
- Separar critérios eliminatórios de critérios de pontuação.
- Permitir estratégias independentes e simultâneas.
- Evitar que preço baixo compense risco crítico.
- Permitir regras condicionais e exceções controladas.
- Produzir uma explicação objetiva para cada classificação.
- Permitir calibração futura por histórico e backtest.
- Manter as regras independentes da fonte de origem, permitindo expansão para outros bancos e portais.

# 2. Conceito de estratégia

Estratégia é a intenção econômica usada para avaliar uma oportunidade. Ela define o que importa mais, quais riscos são aceitáveis, quais indicadores recebem maior peso e quais condições são obrigatórias.

| Estratégia | Objetivo principal | Indicadores prioritários |
|---|---|---|
| Renda | Gerar renda recorrente com segurança | yield, aluguel provável, vacância, condomínio, liquidez, risco |
| Revenda / Flip | Comprar abaixo do mercado e vender com margem | desconto líquido, margem, reforma, prazo, liquidez, custos de saída |
| Valorização | Capturar crescimento de valor ao longo do tempo | localização, preço/m², infraestrutura, oferta/demanda, tendência |
| MCMV / Baixa renda | Explorar demanda popular com ticket e liquidez adequados | ticket, demanda, aluguel, financiamento, liquidez, localização |
| Terreno | Explorar potencial construtivo ou valorização | zoneamento, área, testada, topografia, infraestrutura, preço/m² |
| Apartamento | Avaliar unidades residenciais em condomínio | condomínio, vaga, elevador, andar, área, aluguel, liquidez |
| Casa / Sobrado | Avaliar imóveis horizontais | terreno, área construída, reforma, localização, garagem, liquidez |
| 1 dormitório | Explorar demanda específica e alta liquidez potencial | ticket, aluguel, demanda, localização, condomínio, revenda |


# 3. Modelo de avaliação em camadas

A análise deve ocorrer em camadas. Uma camada posterior não deve mascarar uma falha crítica anterior.

| Camada | Pergunta | Resultado |
|---|---|---|
| 1. Elegibilidade | O imóvel pode entrar no Radar? | elegível / bloqueado |
| 2. Qualidade dos dados | Os dados são suficientes e confiáveis? | confiança |
| 3. Mercado | Está barato frente ao mercado? | valuation e desconto |
| 4. Economia | Existe margem depois de todos os custos? | margem e retorno |
| 5. Liquidez | É vendável/alugável dentro do prazo esperado? | liquidez |
| 6. Risco | Há riscos que inviabilizam ou reduzem a tese? | risco |
| 7. Estratégia | É aderente à estratégia selecionada? | aderência |
| 8. Score | Qual a força relativa da oportunidade? | pontuação |
| 9. Ação | O que fazer agora? | monitorar / analisar / priorizar / descartar |


# 4. Hard Rules x Soft Rules

Hard Rules são condições obrigatórias. Se uma delas for violada, o imóvel pode ser bloqueado independentemente do score. Soft Rules influenciam a pontuação, mas não necessariamente eliminam a oportunidade.

| Tipo | Comportamento | Exemplo |
|---|---|---|
| Hard | Elimina ou coloca em análise condicionada | zona bloqueada |
| Hard | Impede recomendação | risco jurídico crítico |
| Soft | Reduz ou aumenta score | condomínio alto |
| Soft | Aumenta prioridade | desconto líquido elevado |
| Condicional | Exige compensação | zona C aceita com margem adicional |
| Informacional | Não decide sozinha | número de quartos |
| Confiança | Reduz força da conclusão | poucos comparáveis |


# 5. Hierarquia e precedência das regras

A precedência evita que uma regra de score anule uma condição de segurança.
- 1º — Bloqueios e restrições críticas.
- 2º — Regras legais/documentais eliminatórias.
- 3º — Regras de elegibilidade da estratégia.
- 4º — Regras condicionais e requisitos mínimos.
- 5º — Regras econômicas.
- 6º — Regras de liquidez.
- 7º — Regras de risco.
- 8º — Pontuação dos fatores.
- 9º — Ajuste por confiança.
- 10º — Ranking e desempate.
Regra fundamental: risco crítico não pode ser compensado por pontos positivos de preço, aluguel ou valorização.

# 6. Arquitetura conceitual do score

O score deve representar a atratividade relativa da oportunidade, e não substituir a análise econômica.
Modelo conceitual: Score Final = Score Bruto × Fator de Confiança × Ajustes Estratégicos, respeitando previamente todas as Hard Rules.

| Componente | Faixa ilustrativa | Peso exemplo |
|---|---|---|
| Desconto líquido | 0–100 | 25% |
| Margem de segurança | 0–100 | 20% |
| Liquidez | 0–100 | 15% |
| Localização | 0–100 | 15% |
| Risco | 0–100 | 10% |
| Renda / yield | 0–100 | 5% |
| Valorização | 0–100 | 5% |
| Qualidade da oportunidade | 0–100 | 5% |

Os pesos acima são referência inicial de negócio e devem ser calibrados por backtest. Cada estratégia deve possuir pesos próprios.

# 7. Faixas de classificação


| Score Final | Classificação | Ação sugerida |
|---|---|---|
| 90–100 | 🔥 Excepcional | Prioridade máxima; análise imediata |
| 80–89 | 🟢 Excelente | Priorizar due diligence |
| 70–79 | 🟢 Muito boa | Analisar em seguida |
| 60–69 | 🟡 Interessante | Monitorar/analisar conforme estratégia |
| 50–59 | 🟠 Especulativa | Somente com tese clara |
| <50 | 🔴 Fraca | Baixa prioridade |
| Bloqueada | ⛔ Eliminada | Não recomendar enquanto condição persistir |


# 8. Fator de confiança

Confiança mede a qualidade da conclusão, não o risco do imóvel. Um imóvel pode parecer excelente, mas ter baixa confiança porque existem poucos comparáveis ou dados incompletos.

| Confiança | Fator ilustrativo | Interpretação |
|---|---|---|
| Muito alta | 1,00 | dados fortes e consistentes |
| Alta | 0,95 | boa evidência, pequenas lacunas |
| Média | 0,88 | evidência razoável |
| Baixa | 0,75 | lacunas relevantes |
| Muito baixa | 0,60 | conclusão frágil; exige validação |
| Inconclusiva | não recomendar | dados insuficientes para decisão |

Esses fatores são parâmetros calibráveis, não valores definitivos.

# 9. Estratégia — Renda

A estratégia de renda procura imóveis que possam gerar fluxo recorrente com risco controlado.

| Regra | Parâmetro inicial | Tipo |
|---|---|---|
| Yield bruto mínimo | 0,80% ao mês | Hard/Soft configurável |
| Condomínio sobre aluguel | limite configurável | Soft |
| Vacância esperada | limite configurável | Soft |
| Demanda locatícia | mínima média | Hard |
| Liquidez | mínima média | Hard |
| Risco jurídico | sem risco crítico | Hard |
| Preço total | compatível com aluguel | Hard/Soft |
| Margem de segurança | mínima configurável | Soft |

O yield deve utilizar o custo econômico total, não apenas o lance/preço de aquisição.

# 10. Estratégia — Revenda / Flip

O foco é capturar desconto real, executar melhorias com previsibilidade e vender em prazo compatível.

| Indicador | Regra de negócio |
|---|---|
| Desconto líquido | deve superar o mínimo da estratégia |
| Margem líquida | deve cobrir custos + margem de segurança |
| Reforma | não pode consumir a tese econômica |
| Liquidez | preferencialmente média/alta |
| Prazo de saída | deve ser compatível com o cenário |
| Preço de venda estressado | deve manter margem aceitável |
| Risco jurídico | sem impeditivo crítico |

O Radar deve calcular cenário base e cenário estressado. Uma oportunidade que só funciona no cenário otimista não deve ser classificada como excelente.

# 11. Estratégia — Valorização

Busca ativos cuja tese dependa principalmente de crescimento futuro de valor.
- Localização recebe peso elevado.
- Preço por m² deve ser comparado ao segmento correto.
- Infraestrutura e transformação urbana podem aumentar a tese.
- Oferta concorrente deve ser considerada.
- Tempo de permanência deve ser explicitamente parametrizado.
- Valorização passada nunca deve ser tratada como garantia de valorização futura.

# 12. Estratégia — MCMV / Baixa renda

A estratégia deve tratar mercado popular como um segmento econômico, não como sinônimo de baixa qualidade.
- Não bloquear automaticamente por perfil de renda.
- Avaliar demanda efetiva do bairro e do produto.
- Considerar ticket e capacidade de absorção do mercado.
- Medir liquidez de venda e aluguel separadamente.
- Considerar acesso a financiamento como fator de demanda.
- Aplicar filtros específicos de localização e segurança definidos pelo usuário.
- Exigir margem adicional quando a liquidez for baixa.
- Separar preço baixo de oportunidade: ticket baixo não garante retorno.

# 13. Estratégia — Terrenos

Terrenos exigem regras diferentes porque o valor depende fortemente do potencial de uso.

| Fator | Perguntas-chave |
|---|---|
| Zoneamento | O que pode ser construído? |
| Potencial construtivo | Qual o aproveitamento permitido? |
| Testada | É adequada ao uso pretendido? |
| Topografia | Há custo extraordinário? |
| Formato | A geometria limita o projeto? |
| Infraestrutura | Há água, esgoto, energia e acesso? |
| Preço/m² | Está barato frente a terrenos comparáveis? |
| Demanda | Existe comprador para esse tipo de terreno? |


# 14. Estratégia — Apartamentos

- Condomínio deve ser incorporado ao custo e ao cálculo de renda.
- Vaga deve ser valorizada conforme o mercado local.
- Andar, elevador, posição e incidência solar podem ser diferenciais.
- Unidades pequenas não devem ser automaticamente descartadas.
- Comparáveis devem priorizar o mesmo condomínio quando possível.
- Reforma deve ser estimada por nível de intervenção.

# 15. Estratégia — Casa / Sobrado

- Separar valor do terreno e valor da construção sempre que possível.
- Avaliar necessidade de reforma.
- Considerar garagem, testada e área externa.
- Verificar liquidez específica da rua/bairro.
- Casas podem ter grande desconto aparente e ainda assim baixa liquidez.
- Imóveis muito personalizados devem receber desconto de liquidez quando aplicável.

# 16. Localização como regra configurável


| Classe | Descrição | Comportamento exemplo |
|---|---|---|
| A | prioritária | aceitar com requisitos normais |
| B | boa | aceitar; pequeno desconto adicional pode ser exigido |
| C | condicional | exigir margem/score mínimo maior |
| D | restrita | somente exceções configuradas |
| E | bloqueada | não recomendar |

As classes não devem ser gravadas como verdade absoluta. Devem resultar de parâmetros configuráveis, listas de áreas, indicadores de liquidez, segurança, infraestrutura, demanda e decisões do investidor.

# 17. Regras de desconto


| Regra | Fórmula / conceito | Uso |
|---|---|---|
| Desconto de aquisição | 1 − preço / valor de mercado | mede desconto nominal |
| Desconto líquido | 1 − custo econômico total / valor de mercado | mede desconto real |
| Margem | valor de mercado − custo total | mede ganho potencial |
| Margem % | margem / valor de mercado | compara oportunidades |
| Desconto estressado | 1 − custo estressado / valor estressado | teste de segurança |


# 18. Regras de custo

- Incluir preço/lance.
- Incluir comissão aplicável.
- Incluir ITBI quando aplicável.
- Incluir registro/escritura quando aplicável.
- Incluir condomínio e tributos conforme responsabilidade e cenário.
- Incluir regularização/documentação quando aplicável.
- Incluir reforma.
- Incluir custo financeiro quando a estratégia exigir.
- Incluir custo de carregamento.
- Incluir custo de venda na estratégia de revenda.
- Incluir margem para imprevistos.
O Radar deve trabalhar com custo econômico total e também manter os componentes separados para explicar a tese.

# 19. Regras de liquidez


| Nível | Interpretação | Impacto |
|---|---|---|
| Muito alta | mercado amplo e giro rápido | forte bônus |
| Alta | boa demanda | bônus |
| Média | mercado funcional | neutro/leve bônus |
| Baixa | venda pode demorar | penalização |
| Muito baixa | saída difícil | forte penalização ou bloqueio |

Liquidez deve ser específica para venda e aluguel. Um imóvel pode ser muito líquido para aluguel e ruim para revenda, ou vice-versa.

# 20. Regras de risco

- Risco crítico: pode bloquear a oportunidade.
- Risco alto: exige margem adicional e validação.
- Risco médio: penaliza score.
- Risco baixo: pequeno impacto.
- Risco desconhecido: não deve ser tratado como baixo; reduz confiança.
Risco deve ser decomposto em jurídico, documental, ocupacional, físico, financeiro, localização, liquidez e execução.

# 21. Regras condicionais

As regras condicionais permitem que o Radar capture oportunidades fora do perfil normal sem perder disciplina.

| Condição | Compensação exemplo |
|---|---|
| Localização C | exigir desconto líquido ≥ 35% |
| Liquidez baixa | exigir margem ≥ 30% |
| Poucos comparáveis | reduzir confiança e exigir margem adicional |
| Reforma alta | exigir cenário estressado positivo |
| Condomínio elevado | exigir yield superior ao mínimo |
| Imóvel atípico | exigir comparáveis de qualidade superior |
| Dados incompletos | permitir monitoramento, mas não prioridade máxima |


# 22. Catálogo de regras parametrizáveis


| Código | Regra | Tipo | Objetivo |
|---|---|---|---|
| LOC-001 | Localização bloqueada | Hard | bloquear áreas explicitamente proibidas |
| LOC-002 | Localização prioritária | Soft | bônus de score |
| LOC-003 | Zona condicional | Conditional | exigir margem adicional |
| LOC-004 | Distância de polo | Soft | pontuar proximidade de demanda |
| LOC-005 | Liquidez local | Soft/Hard | definir mínimo por estratégia |
| TIP-001 | Tipo permitido | Hard | filtrar tipos |
| TIP-002 | Tipo prioritário | Soft | aumentar score |
| TIP-003 | 1 dormitório | Soft | avaliar sem preconceito de tipo |
| PRI-001 | Preço máximo | Hard | limitar ticket |
| PRI-002 | Desconto mínimo | Hard/Soft | definir entrada econômica |
| VAL-001 | Comparáveis mínimos | Confidence | definir evidência mínima |
| VAL-002 | Mesmo condomínio | Soft | priorizar comparáveis |
| VAL-003 | Outlier | Quality | excluir ou reduzir peso |
| VAL-004 | Faixa conservadora | Hard/Soft | usar cenário prudente |
| CUS-001 | Custo total | Hard | incluir componentes aplicáveis |
| CUS-002 | Reforma | Soft/Hard | limitar impacto |
| CUS-003 | Custo de saída | Soft | aplicar em revenda |
| MARG-001 | Margem mínima | Hard | proteger tese |
| MARG-002 | Margem adicional por risco | Conditional | exigir compensação |
| LIQ-001 | Liquidez mínima | Hard | impedir baixa liquidez |
| LIQ-002 | Liquidez venda | Soft | pontuar saída |
| LIQ-003 | Liquidez aluguel | Soft | pontuar locação |
| REN-001 | Yield mínimo | Hard/Soft | estratégia renda |
| REN-002 | Vacância | Soft | penalizar risco de renda |
| REN-003 | Condomínio/aluguel | Soft | avaliar eficiência |
| RISK-001 | Risco jurídico crítico | Hard | bloquear |
| RISK-002 | Risco ocupacional | Soft/Hard | ajustar tese |
| RISK-003 | Risco físico | Soft/Hard | ajustar custo |
| CONF-001 | Dados incompletos | Confidence | reduzir confiança |
| CONF-002 | Dados antigos | Confidence | reduzir confiança |
| STR-001 | Aderência à estratégia | Hard | filtrar |
| STR-002 | Peso por estratégia | Soft | alterar score |
| STR-003 | Regra específica | Override | sobrepor regra global |
| SCORE-001 | Score mínimo | Hard | definir entrada no ranking |
| SCORE-002 | Faixa excepcional | Soft | prioridade máxima |
| ALERT-001 | Entrada no radar | Informational | gerar evento |
| ALERT-002 | Melhora de score | Informational | alertar mudança |
| ALERT-003 | Queda de preço | Informational | recalcular |
| ALERT-004 | Mudança de status | Informational | reavaliar |
| HIST-001 | Reavaliação periódica | Governance | manter análise atual |
| HIST-002 | Mudança de regra | Governance | recalcular histórico conforme política |


# 23. Modelo de parametrização

Todo parâmetro relevante deve possuir, conceitualmente: nome, descrição, valor, unidade, tipo, estratégia, escopo geográfico, vigência, prioridade, condição, origem e justificativa.

| Dimensão | Exemplos |
|---|---|
| Global | idade do dado, fator de confiança |
| Estratégia | yield mínimo, margem mínima, score mínimo |
| Localização | classes A–E, áreas bloqueadas |
| Tipo | apartamento, casa, terreno, sobrado |
| Faixa de preço | mínimo/máximo |
| Economia | desconto, margem, custos |
| Liquidez | nível mínimo |
| Risco | limites por categoria |
| Valuation | comparáveis, conservador/base/otimista |
| Monitoramento | frequência de reavaliação, gatilhos |
| Alertas | eventos e prioridades |


# 24. Exceções

Exceção não deve significar apagar uma regra. Deve significar criar uma condição explícita que permita ultrapassá-la.
- Cada exceção deve ter motivo.
- Deve indicar quais regras ela substitui.
- Deve possuir validade quando aplicável.
- Deve ser auditável.
- Não pode ultrapassar bloqueios críticos de segurança/jurídico sem regra explícita de governança.
- Deve aparecer na explicação final da oportunidade.

# 25. Explicabilidade da decisão

Toda oportunidade relevante deve responder, de forma legível:
- Por que entrou no Radar?
- Qual é a estratégia em que ela funciona melhor?
- Quanto está abaixo do mercado?
- Qual é o custo econômico total estimado?
- Qual é a margem?
- Quais são os principais pontos positivos?
- Quais são os principais riscos?
- O que ainda precisa ser confirmado?
- Qual regra aumentou ou reduziu o score?
- Por que ela ficou acima ou abaixo de outras oportunidades?

# 26. Exemplo de análise


| Indicador | Exemplo |
|---|---|
| Preço de aquisição | R$ 190.000 |
| Valor de mercado conservador | R$ 300.000 |
| Custos adicionais | R$ 35.000 |
| Custo econômico total | R$ 225.000 |
| Desconto líquido | 25,0% |
| Margem econômica | R$ 75.000 |
| Margem % | 25,0% |
| Aluguel estimado | R$ 2.100 |
| Yield bruto | 0,93% a.m. |
| Liquidez | Alta |
| Risco | Médio |
| Confiança | Alta |
| Estratégia mais aderente | Renda + Revenda |

O exemplo mostra por que o preço de aquisição sozinho não determina a oportunidade.

# 27. Ranking

O ranking deve combinar score, confiança, estratégia e urgência.

| Critério de desempate | Prioridade |
|---|---|
| Hard Rules | primeiro |
| Score final | 1 |
| Confiança | 2 |
| Margem % | 3 |
| Liquidez | 4 |
| Risco | 5 |
| Atualidade dos dados | 6 |
| Potencial de múltiplas estratégias | 7 |

Uma oportunidade com score alto e baixa confiança não deve necessariamente superar uma oportunidade ligeiramente inferior, mas muito mais comprovada.

# 28. Monitoramento e reavaliação

O imóvel não deve ser tratado como fotografia. Ele é uma oportunidade viva.
- Preço pode mudar.
- Status pode mudar.
- Comparáveis podem mudar.
- Aluguel de mercado pode mudar.
- Condomínio ou dívida podem ser atualizados.
- Novas informações jurídicas podem surgir.
- Uma oportunidade descartada pode voltar ao Radar se uma variável crítica mudar.
O Radar deve registrar o motivo de cada mudança de classificação.

# 29. Gatilhos de reavaliação


| Gatilho | Ação |
|---|---|
| Queda de preço | recalcular oportunidade |
| Mudança de avaliação | recalcular desconto |
| Novo comparável relevante | recalcular valuation |
| Mudança de status | reavaliar elegibilidade |
| Mudança de localização/classificação | recalcular score |
| Nova informação de risco | reavaliar risco |
| Alteração de estratégia | recalcular aderência |
| Mudança de parâmetros | reprocessar conforme vigência |


# 30. Backtest e calibração

Nenhum peso ou limite deve ser considerado definitivo antes de ser confrontado com histórico.
- Guardar oportunidades capturadas.
- Registrar score e regras aplicadas na época.
- Registrar decisão do investidor.
- Registrar desfecho quando conhecido.
- Comparar score previsto com resultado observado.
- Identificar regras que geram muitos falsos positivos.
- Identificar regras que eliminam boas oportunidades.
- Calibrar pesos, limites e fatores de confiança.

# 31. KPIs do Radar


| KPI | Objetivo |
|---|---|
| Oportunidades capturadas | medir cobertura |
| Oportunidades qualificadas | medir qualidade do filtro |
| Taxa de falso positivo | medir precisão |
| Taxa de falso negativo | medir oportunidades perdidas |
| Precisão do valuation | medir qualidade de mercado |
| Precisão do yield estimado | medir qualidade da tese de renda |
| Tempo até decisão | medir eficiência |
| Conversão em aquisição | medir valor real do Radar |
| Retorno por estratégia | medir desempenho |
| Performance por regra | identificar regras boas/ruins |


# 32. Governança das regras

- Regras devem possuir versão.
- Alterações devem possuir justificativa.
- Parâmetros devem ter vigência.
- Alterações críticas devem ser comparáveis entre versões.
- O histórico não deve ser silenciosamente reescrito.
- Deve ser possível saber qual configuração produziu cada score.
- Novas regras devem poder ser testadas antes de se tornarem oficiais.

# 33. Princípios finais

- Preço baixo não é oportunidade automaticamente.
- Desconto nominal não é desconto econômico.
- Mercado deve ser segmentado; comparar imóveis errados distorce a tese.
- Risco desconhecido não é risco baixo.
- Baixa renda não significa baixa qualidade.
- Tipo de imóvel não deve ser preconceituosamente eliminado.
- Liquidez importa tanto quanto margem.
- Uma estratégia pode transformar um imóvel mediano em uma boa oportunidade — ou o contrário.
- Hard Rule protege contra erros graves; Score serve para priorização.
- Confiança protege contra excesso de certeza.
- Exceções devem ser explícitas e auditáveis.
- Cada oportunidade deve explicar por que merece atenção.

# 34. Próximo documento recomendado

Documento 4 — Processo de Análise Profunda e Due Diligence do Imóvel.
Esse próximo documento deve detalhar o que acontece depois que o Radar identifica uma oportunidade: validação documental, matrícula, ocupação, condomínio, IPTU, situação jurídica, edital, dívidas, reforma, visita, confirmação de comparáveis, validação de aluguel, cenários de compra, critérios de aprovação/reprovação e checklist completo antes da decisão de aquisição.
Assim, a sequência de negócio fica: Documento 1 — Regras → Documento 2 — Valuation → Documento 3 — Estratégias/Score → Documento 4 — Due Diligence → posteriormente Requisitos Funcionais do sistema.
