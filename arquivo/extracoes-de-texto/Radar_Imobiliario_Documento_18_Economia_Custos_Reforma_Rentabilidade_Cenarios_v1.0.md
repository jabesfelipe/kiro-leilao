# Radar_Imobiliario_Documento_18_Economia_Custos_Reforma_Rentabilidade_Cenarios_v1.0

🏠 RADAR IMOBILIÁRIO
Documento 18
Economia da Operação, Custos, Reforma, Rentabilidade e Cenários
Especificação Funcional de Negócio | Versão 1.0
PREÇO → CUSTO TOTAL → REFORMA → RENDA/SAÍDA → MARGEM → RETORNO → DECISÃO

# 1. Objetivo

Detalhar a economia da operação depois do valuation, transformando o valor de mercado em uma análise completa de investimento. O documento cobre aquisição, custos, reforma, carregamento, aluguel, revenda, rentabilidade, margem, cenários, sensibilidade e preço máximo.
- Evitar decisões baseadas somente no desconto de entrada.
- Calcular custo econômico total por estratégia.
- Separar retorno bruto de retorno líquido.
- Modelar cenários e sensibilidade.
- Permitir que o investidor defina sua margem mínima e retorno exigido.
- Manter premissas explícitas e auditáveis.

# 2. Princípio Econômico Central

Uma operação só é boa quando a diferença entre valor econômico provável e custo total, ajustada por risco, tempo e retorno exigido, é suficiente para compensar o capital empregado.

| Conceito | Pergunta |
|---|---|
| Entrada | Quanto vou pagar? |
| Custos | Quanto realmente vou gastar? |
| Capital | Quanto ficará imobilizado e por quanto tempo? |
| Saída | Por quanto consigo vender/alugar? |
| Margem | Quanto sobra após todos os custos? |
| Retorno | Quanto ganho sobre o capital? |
| Risco | O que pode reduzir ou eliminar o ganho? |
| Estratégia | Essa relação faz sentido para meu objetivo? |


# 3. Custo Econômico Total

O custo econômico deve representar o capital necessário para transformar a aquisição em um ativo pronto para a estratégia.

| Grupo | Componentes |
|---|---|
| Aquisição | Preço/lance, sinal, custos diretamente vinculados |
| Transação | Comissão, ITBI, registro, escritura/documentação |
| Passivos | Condomínio, IPTU e demais débitos conforme responsabilidade |
| Regularização | Documentação, obras ou adequações necessárias |
| Reforma | Materiais, mão de obra, projeto e contingência |
| Carregamento | Condomínio, impostos, manutenção, seguros e outros |
| Financiamento | Juros, tarifas e custos financeiros |
| Saída | Corretagem, impostos/custos de venda e preparação |
| Contingência | Reserva para incertezas |

Regra: cada componente deve ser identificado como confirmado, estimado, calculado ou desconhecido.

# 4. Custos Conhecidos x Desconhecidos


| Situação | Tratamento |
|---|---|
| Confirmado | Incluir no custo. |
| Estimado | Incluir com premissa e faixa. |
| Desconhecido de baixo impacto | Registrar; pode permanecer pendente. |
| Desconhecido de alto impacto | Criar contingência ou impedir decisão. |
| Desconhecido crítico | Não permitir BUY até resolução. |


# 5. Reforma — Níveis 0 a 4


| Nível | Descrição | Tratamento econômico |
|---|---|---|
| 0 | Sem reforma relevante | Custo mínimo |
| 1 | Cosmética | Pintura, limpeza, pequenos reparos |
| 2 | Leve/média | Pisos, elétrica/hidráulica pontual, cozinha/banheiro |
| 3 | Relevante | Reforma ampla, vários ambientes |
| 4 | Pesada | Reforma estrutural/complexa; alta incerteza |

- O nível deve ser uma estimativa até existir evidência física/orçamento.
- O orçamento deve possuir faixa mínima/base/máxima quando houver incerteza.
- Quanto maior a reforma, maior deve ser a contingência.

# 6. Contingência de Reforma

A contingência protege contra erro de orçamento e descoberta de problemas.

| Situação | Contingência conceitual |
|---|---|
| Orçamento confirmado + imóvel vistoriado | Menor |
| Orçamento preliminar | Média |
| Sem visita | Maior |
| Imóvel ocupado | Maior |
| Reforma nível 3/4 | Maior |
| Problemas estruturais suspeitos | Muito maior / pendente |

Percentuais exatos devem ser parametrizados pelo investidor e calibrados com resultados reais.

# 7. Capital Imobilizado

O Radar deve considerar não apenas o custo total, mas quanto capital ficará imobilizado e por quanto tempo.

| Indicador | Uso |
|---|---|
| Capital inicial | Capital necessário para aquisição. |
| Capital total | Aquisição + reforma + custos. |
| Capital máximo | Limite configurado pelo investidor. |
| Prazo de imobilização | Tempo até aluguel ou venda. |
| Custo de oportunidade | Retorno que o capital poderia gerar em alternativa. |
| Capital exposto | Capital sujeito ao risco da operação. |


# 8. Custo de Carregamento

- Condomínio.
- IPTU e taxas.
- Seguro/manutenção quando aplicável.
- Financiamento.
- Despesas operacionais.
- Custo de oportunidade do capital.
- Tempo esperado até locação/venda.
O custo de carregamento deve ser modelado por mês e por cenário.

# 9. Estratégia de Renda


| Indicador | Cálculo/uso |
|---|---|
| Aluguel bruto | Aluguel mensal esperado |
| Vacância | Meses/percentual sem renda |
| Receita efetiva | Aluguel ajustado por vacância |
| Custos recorrentes | Condomínio, impostos, manutenção etc. |
| Renda líquida | Receita efetiva − custos |
| Yield bruto | Aluguel / custo econômico |
| Yield líquido | Renda líquida / capital total |
| Payback | Tempo para recuperar capital via renda, quando aplicável |


# 10. Yield

O yield deve ser sempre associado à base utilizada.

| Métrica | Fórmula conceitual |
|---|---|
| Yield bruto mensal | aluguel mensal / custo econômico |
| Yield bruto anual | yield mensal × 12 |
| Yield líquido mensal | renda líquida mensal / capital total |
| Yield líquido anual | yield líquido mensal × 12 |

Exemplo: aluguel de R$ 2.200 e custo econômico de R$ 220.000 → yield bruto mensal de 1,0%.

# 11. Estratégia de Revenda

A análise de revenda deve partir de um valor de saída conservador, e não do melhor preço imaginável.

| Componente | Exemplo |
|---|---|
| Preço de aquisição | R$ 191.651 |
| Custos de aquisição | R$ 10.000 |
| Reforma | R$ 20.000 |
| Carregamento | R$ 8.000 |
| Capital total antes da venda | R$ 229.651 |
| Venda conservadora | R$ 285.000 |
| Custos de venda | R$ 15.000 |
| Resultado antes de impostos/ajustes | R$ 40.349 |


# 12. Margem de Operação


| Métrica | Fórmula |
|---|---|
| Margem absoluta | receita líquida de saída − capital total |
| Margem sobre valor de mercado | (valor − custo econômico) / valor |
| Retorno sobre capital | lucro líquido / capital total |
| ROI | ganho líquido / capital investido |
| Margem de segurança | valor conservador − custo econômico |

O Radar deve evitar confundir margem sobre valor do imóvel com retorno sobre o capital.

# 13. Estratégia de Valorização

- Definir horizonte de investimento.
- Projetar valorização de forma conservadora.
- Considerar renda durante o período.
- Considerar custos de carregamento.
- Aplicar desconto/risco à valorização futura.
- Comparar com alternativas de investimento.

# 14. Valor Presente e Custo de Oportunidade

Quando o horizonte for relevante, o Radar pode comparar o resultado esperado com o retorno mínimo exigido pelo investidor.

| Conceito | Aplicação |
|---|---|
| Retorno mínimo | Taxa mínima exigida. |
| Custo de oportunidade | Retorno alternativo do capital. |
| Valor temporal | R$ hoje não equivale a R$ no futuro. |
| Prazo | Quanto tempo o capital ficará exposto. |
| TIR/IRR | Pode ser usada em operações com fluxos múltiplos. |
| VPL/NPV | Pode apoiar decisões com horizonte definido. |

TIR e VPL são métricas complementares; não substituem análise de risco, liquidez e qualidade dos dados.

# 15. Financiamento


| Item | Tratamento |
|---|---|
| Entrada | Capital próprio. |
| Parcelas | Fluxo futuro. |
| Juros | Custo econômico. |
| Seguros/tarifas | Custos financeiros. |
| Prazo | Impacta capital e risco. |
| Amortização | Afeta saldo devedor. |
| Venda antecipada | Simular quitação. |
| Custo de oportunidade | Comparar capital próprio e financiado. |

A análise deve permitir comparar compra à vista, financiada e cenários híbridos quando aplicável.

# 16. Preço Máximo Econômico

O preço máximo deve ser calculado antes da decisão final, incorporando custos, retorno/margem exigida e risco.

| Estratégia | Estrutura |
|---|---|
| Revenda | Preço máximo = saída conservadora − custos de saída − reforma − carregamento − lucro/margem exigida |
| Renda | Preço máximo = renda líquida / yield mínimo, ajustado por custos e capital adicional |
| Valorização | Preço máximo = valor futuro ajustado ao retorno exigido − custos |
| MCMV | Preço máximo = valor compatível com demanda − custos − margem |
| Terreno | Preço máximo = valor econômico do potencial − custos de desenvolvimento − margem |


# 17. Três Preços Importantes


| Preço | Significado |
|---|---|
| Preço de oferta | O que o vendedor pede. |
| Preço máximo | O limite racional de entrada. |
| Preço-alvo | Preço desejado para comprar com folga superior ao mínimo. |

A existência de preço máximo permite que o Radar monitore oportunidades mesmo quando ainda não estão baratas o suficiente.

# 18. Cenários Econômicos


| Cenário | Aquisição | Reforma | Saída | Prazo |
|---|---|---|---|---|
| Otimista | Baixa | Baixa | Alta | Curto |
| Base | Esperada | Esperada | Base | Esperado |
| Conservador | Esperada | Alta | Baixa | Longo |
| Estressado | Alta | Muito alta | Muito baixa | Muito longo |

- Cada cenário deve gerar custo, margem e retorno.
- A tese deve ser avaliada pela robustez, não apenas pelo cenário base.

# 19. Sensibilidade

A sensibilidade mostra quais variáveis podem destruir a tese.

| Variável | Faixas a testar |
|---|---|
| Preço de saída | −5%, −10%, −15% |
| Reforma | +10%, +25%, +50% |
| Prazo | +3, +6, +12 meses |
| Aluguel | −5%, −10%, −15% |
| Vacância | +3, +6 meses |
| Custos | +10%, +20% |
| Preço de aquisição | cenários de lance/negociação |

Os intervalos são ilustrativos e devem ser parametrizados conforme o mercado e a estratégia.

# 20. Ponto de Equilíbrio

O Radar deve conseguir responder qual é o preço de saída mínimo para não perder dinheiro e qual é o preço máximo de entrada para manter a margem exigida.

| Pergunta | Saída |
|---|---|
| Qual venda mínima cobre todos os custos? | Break-even de saída |
| Qual compra máxima mantém a margem? | Preço máximo |
| Quanto pode subir a reforma? | Limite de reforma |
| Quanto pode cair o aluguel? | Yield mínimo atingido |
| Quanto pode aumentar o prazo? | Prazo máximo |


# 21. Robustez da Operação


| Robustez | Critério |
|---|---|
| Muito alta | Funciona no conservador com boa margem. |
| Alta | Funciona no conservador com margem menor. |
| Média | Funciona no base, mas é sensível. |
| Baixa | Só funciona próximo do otimista. |
| Especulativa | Depende de várias premissas favoráveis. |
| Inviável | Não funciona no base/conservador. |


# 22. Comparação com Alternativas

A oportunidade deve competir contra o custo de oportunidade do capital.

| Alternativa | Comparar |
|---|---|
| FII | renda, liquidez, risco, esforço |
| Ações | retorno esperado, volatilidade, liquidez |
| Tesouro | retorno, risco, liquidez e simplicidade |
| Imóvel para renda | yield, valorização, custos e trabalho |
| Imóvel para revenda | ROI, prazo, risco e capital |
| Outra oportunidade imobiliária | margem, liquidez, risco e preço máximo |


# 23. Custo de Esforço

O Radar deve reconhecer que operações complexas consomem tempo e atenção.
- Due diligence intensa.
- Desocupação.
- Reforma.
- Regularização.
- Negociação.
- Gestão de obra.
- Venda/locação.
Quando duas oportunidades possuem retorno semelhante, menor complexidade pode ser vantagem estratégica.

# 24. Score Econômico


| Componente | Peso ilustrativo |
|---|---|
| Desconto líquido | 25% |
| Margem de segurança | 25% |
| ROI/retorno | 15% |
| Liquidez | 10% |
| Prazo | 10% |
| Risco econômico | 10% |
| Complexidade | 5% |

Os pesos são ilustrativos e devem ser configuráveis por estratégia. Este score econômico alimenta o score geral do Radar.

# 25. Exemplo Integrado

Exemplo: imóvel por R$ 191.651,31, valor conservador de R$ 285 mil, custo econômico inicial de R$ 220 mil e venda com custos adicionais. O Radar deve testar se a margem permanece positiva após reforma maior, venda mais barata e prazo maior. Se a tese continuar positiva, a oportunidade é robusta; se depender do valor otimista, deve ser classificada como sensível/especulativa.

| Teste | Resultado conceitual |
|---|---|
| Base | Margem positiva |
| Reforma +25% | Margem reduzida |
| Saída −10% | Testa robustez |
| Prazo +6 meses | Aumenta carregamento |
| Todas as pressões juntas | Cenário estressado |
| Conclusão | Robustez determina força da recomendação |


# 26. Regras de Decisão Econômica


| ID | Regra | Resultado |
|---|---|---|
| ECO18-001 | Custo econômico > valor conservador | DO NOT BUY / BLOCK conforme risco |
| ECO18-002 | Preço > preço máximo | DO NOT BUY |
| ECO18-003 | Margem abaixo do mínimo | DO NOT BUY/BUY IF |
| ECO18-004 | Reforma acima do limite | BUY IF/DO NOT BUY |
| ECO18-005 | Yield abaixo do piso | Não aderente à renda |
| ECO18-006 | Operação só funciona no otimista | Especulativa |
| ECO18-007 | Break-even muito próximo do preço atual | MONITOR |
| ECO18-008 | Cenário conservador ainda robusto | Favorecer BUY |
| ECO18-009 | Custo crítico desconhecido | PENDENTE |
| ECO18-010 | Retorno abaixo do mínimo exigido | DO NOT BUY |


# 27. Alertas Econômicos

- Preço atingiu preço-alvo.
- Preço atingiu preço máximo.
- Desconto líquido ultrapassou gatilho.
- Valuation aumentou/reduziu.
- Reforma estimada aumentou.
- Yield caiu abaixo do piso.
- Margem caiu abaixo do mínimo.
- Custo de carregamento mudou.
- Cenário conservador deixou de ser viável.
- Nova oportunidade apresenta retorno superior.

# 28. Reavaliação Econômica


| Evento | Recalcular |
|---|---|
| Mudança | Recalcular |
| Preço | Custo, desconto, margem, preço máximo |
| Reforma | Custo, ROI, margem |
| Aluguel | Yield e estratégia de renda |
| Mercado | Valuation e saída |
| Prazo | Carregamento e retorno |
| Risco | Margem requerida e decisão |
| Financiamento | Fluxo e retorno |


# 29. Critérios de Dados para Decisão

- Preço atual.
- Valuation com confiança.
- Custos de aquisição.
- Reforma.
- Carregamento.
- Custos de saída.
- Valor de saída.
- Prazo.
- Retorno mínimo.
- Margem mínima.
- Cenário conservador.
- Riscos relevantes.

# 30. O que NÃO Fazer

- Não considerar somente o preço do leilão.
- Não chamar desconto bruto de lucro.
- Não ignorar comissão, impostos ou documentação.
- Não considerar reforma como custo zero quando desconhecida.
- Não usar aluguel bruto como se fosse renda líquida.
- Não projetar venda pelo melhor anúncio encontrado.
- Não ignorar o tempo do capital.
- Não comparar ROI de operações com prazos muito diferentes sem ajuste.
- Não usar cenário otimista como base de decisão.
- Não tratar preço máximo como preço obrigatório de compra.

# 31. MVP Econômico

- Custo de aquisição.
- Comissão e documentação.
- Estimativa de débitos relevantes.
- Reforma nível 0–4.
- Contingência.
- Custo econômico total.
- Valuation conservador/base.
- Desconto líquido.
- Margem.
- Aluguel e yield quando aplicável.
- Custo de carregamento básico.
- Preço máximo por estratégia.
- Cenário conservador.
- Break-even.
- Decisão econômica explicável.

# 32. Critérios de Aceite

- CA-D18 — O custo econômico total pode ser calculado por operação.
- CA-D18 — Custos conhecidos e desconhecidos são diferenciados.
- CA-D18 — Reforma possui níveis e cenários.
- CA-D18 — Contingência é parametrizável.
- CA-D18 — O Radar calcula yield bruto e líquido quando os dados permitem.
- CA-D18 — ROI e margem são diferenciados.
- CA-D18 — O tempo de capital é considerado.
- CA-D18 — Preço máximo pode ser calculado por estratégia.
- CA-D18 — Cenários otimista, base, conservador e estressado são suportados.
- CA-D18 — É possível executar análise de sensibilidade.
- CA-D18 — O break-even pode ser identificado.
- CA-D18 — Operações complexas podem receber impacto de esforço/risco.
- CA-D18 — Alternativas de investimento podem ser usadas como referência de custo de oportunidade.
- CA-D18 — Uma oportunidade pode ser BUY mesmo sem ser a de maior desconto, se tiver melhor relação risco/retorno.
- CA-D18 — Uma oportunidade pode ser rejeitada mesmo com grande desconto se a economia não for robusta.

# 33. Relação com os Documentos Anteriores


| Documento | Papel |
|---|---|
| 17 — Valuation | Define valor de mercado e preço máximo inicial. |
| 18 — Economia | Transforma valuation em operação completa. |
| 15 — Decisão | Usa resultado econômico para decidir. |
| 3/8 — Estratégias/Parâmetros | Define pesos, limites e objetivos. |
| 4 — Due Diligence | Valida premissas e riscos. |
| 7 — Workflow | Reage às mudanças econômicas. |
| 14/16 — Dados | Fornecem evidências e histórico. |


# 34. Próximo Documento

Recomendação: Documento 19 — Risco, Due Diligence, Ocupação, Jurídico e Matriz de Impacto. O objetivo será aprofundar como riscos jurídicos, ocupação, dívidas, documentação, condição física e incertezas alteram margem, confiança, preço máximo e decisão.
