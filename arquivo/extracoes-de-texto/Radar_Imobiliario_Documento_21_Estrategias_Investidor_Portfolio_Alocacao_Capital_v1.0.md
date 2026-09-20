# Radar_Imobiliario_Documento_21_Estrategias_Investidor_Portfolio_Alocacao_Capital_v1.0

🏠 RADAR IMOBILIÁRIO
Documento 21
Estratégias do Investidor, Perfil, Portfólio e Alocação de Capital
Especificação Funcional de Negócio | Versão 1.0

# 1. Objetivo

Definir como o Radar transforma o perfil, os objetivos e o capital disponível do investidor em estratégias de busca, filtros, pesos, limites, prioridades e decisões de alocação.
- Representar diferentes perfis e objetivos de investimento.
- Permitir múltiplas estratégias simultâneas.
- Definir capital disponível e capital máximo por operação.
- Controlar concentração por localização, tipo e estratégia.
- Priorizar oportunidades compatíveis com o momento do investidor.
- Separar oportunidade boa de oportunidade adequada ao investidor.
- Permitir simulação de alocação antes da compra.

# 2. Princípio Central

Uma oportunidade pode ser excelente no mercado e ainda assim ser inadequada para determinado investidor. O Radar deve responder duas perguntas separadamente:

| Pergunta | Resultado |
|---|---|
| Essa oportunidade é boa? | Qualidade econômica do ativo. |
| Essa oportunidade é boa para mim? | Aderência ao capital, estratégia, risco e objetivos. |

O objetivo não é maximizar a quantidade de imóveis aprovados, mas maximizar a qualidade do capital alocado.

# 3. Perfil do Investidor


| Dimensão | Exemplos |
|---|---|
| Objetivo | Renda, revenda, valorização, preservação, combinação |
| Horizonte | Curto, médio, longo |
| Risco | Conservador, moderado, arrojado |
| Liquidez desejada | Alta, média, baixa |
| Capital disponível | Valor total disponível para imóveis |
| Capital por operação | Limite absoluto e percentual |
| Renda desejada | Meta mensal/anual |
| Esforço operacional | Baixo, médio, alto |
| Financiamento | Não utilizar, opcional, prioritário |
| Diversificação | Limites por região/tipo/estratégia |


# 4. Objetivos de Investimento


| Objetivo | Indicadores principais |
|---|---|
| Renda passiva | Yield, vacância, liquidez, renda líquida |
| Revenda | Desconto líquido, margem, prazo, liquidez |
| Valorização | Potencial, horizonte, risco, liquidez |
| Preservação | Risco, localização, liquidez, qualidade |
| Construção patrimonial | Diversificação, retorno, risco |
| Oportunidade especial | Margem excepcional + risco controlável |


# 5. Estratégias Simultâneas

O investidor pode manter várias estratégias ativas. Exemplo:

| Estratégia | Alocação ilustrativa | Prioridade |
|---|---|---|
| Renda | 40% | Alta |
| Revenda | 30% | Alta |
| Valorização | 20% | Média |
| Oportunidades especiais | 10% | Baixa |

Os percentuais são exemplos e devem ser configuráveis.

# 6. Capital Disponível

O Radar deve diferenciar patrimônio total, capital líquido disponível e capital efetivamente disponível para novas aquisições.

| Conceito | Definição |
|---|---|
| Patrimônio total | Todos os ativos do investidor. |
| Capital líquido | Recursos que podem ser mobilizados. |
| Reserva | Capital que não deve ser utilizado. |
| Capital imobiliário | Valor reservado para imóveis. |
| Capital disponível agora | Valor efetivamente aplicável. |
| Capital comprometido | Recursos já alocados em operações. |
| Capital livre | Saldo após compromissos. |


# 7. Reserva de Segurança

O Radar nunca deve assumir que 100% do capital disponível pode ser investido. Deve existir uma reserva configurável.
- Reserva mínima absoluta.
- Reserva percentual do patrimônio líquido.
- Reserva para custos inesperados.
- Reserva para reformas.
- Reserva para vacância/carregamento.
- Reserva para contingências jurídicas.
Uma oportunidade que consome a reserva pode ser bloqueada mesmo sendo economicamente atrativa.

# 8. Limite por Operação


| Regra | Exemplo |
|---|---|
| Valor máximo absoluto | R$ 250 mil |
| Percentual máximo do capital | 25% |
| Percentual máximo do patrimônio | 15% |
| Capital total comprometido | Até limite definido |
| Exceção | Permitida somente com justificativa |

O Radar deve avaliar o limite mais restritivo quando múltiplas regras forem aplicáveis.

# 9. Concentração


| Dimensão | Controle |
|---|---|
| Localização | Máximo por cidade/bairro/região |
| Tipo | Máximo em apartamentos/casas/terrenos |
| Estratégia | Máximo em renda/revenda/valorização |
| Faixa de ticket | Máximo por faixa |
| Fonte | Evitar dependência excessiva de uma origem |
| Risco | Limite de exposição a operações complexas |


# 10. Capital Livre x Capital Comprometido

Uma oportunidade não deve ser analisada isoladamente quando o investidor já possui várias operações em andamento.

| Situação | Tratamento |
|---|---|
| Capital livre alto | Maior capacidade de aquisição. |
| Capital livre baixo | Priorizar oportunidades excepcionais. |
| Várias reformas | Reduzir novas aquisições operacionais. |
| Alta concentração | Priorizar diversificação. |
| Reserva abaixo do mínimo | Bloquear novas operações. |


# 11. Orçamento Econômico da Operação

O limite do investidor deve considerar o custo econômico total, e não apenas o lance/preço de aquisição.

| Componente | Considerar no limite |
|---|---|
| Compra | Sim |
| Comissão | Sim |
| Impostos/taxas | Sim |
| Dívidas/responsabilidades | Quando aplicáveis |
| Regularização | Sim |
| Reforma | Sim |
| Contingência | Sim |
| Carregamento | Sim |
| Financiamento | Sim |
| Venda/saída | Conforme estratégia |


# 12. Aderência à Estratégia

Cada oportunidade deve receber uma nota de aderência à estratégia ativa.

| Aderência | Interpretação |
|---|---|
| 90–100 | Totalmente alinhada |
| 80–89 | Muito alinhada |
| 70–79 | Alinhada |
| 60–69 | Parcial |
| 50–59 | Especulativa |
| <50 | Fora da estratégia |


# 13. Oportunidade de Mercado x Oportunidade para o Investidor


| Caso | Conclusão |
|---|---|
| Excelente + aderente | Prioridade máxima |
| Excelente + não aderente | Monitorar ou ignorar |
| Boa + aderente | Priorizar conforme capital |
| Boa + concentração excessiva | Reduzir prioridade |
| Fraca + aderente | Não comprar |
| Excepcional + limite excedido | Exigir exceção formal |


# 14. Score do Investidor


| Componente | Peso ilustrativo |
|---|---|
| Qualidade econômica | 25% |
| Aderência à estratégia | 20% |
| Risco | 15% |
| Liquidez | 10% |
| Capital necessário | 10% |
| Diversificação | 10% |
| Esforço operacional | 5% |
| Horizonte | 5% |

O peso deve ser configurável por perfil. O score do investidor complementa, mas não substitui, o score da oportunidade.

# 15. Score Duplo

O Radar deve manter dois conceitos:

| Score | Pergunta |
|---|---|
| Opportunity Score | Quão boa é a oportunidade? |
| Investor Fit Score | Quão adequada é ao investidor? |

Uma oportunidade somente deve ocupar posições prioritárias quando apresentar boa qualidade e boa aderência.

# 16. Score Composto

Modelo conceitual:
Score Final = Opportunity Score × fator de aderência × fator de confiança × fator de capital/concentração
Os fatores são parametrizáveis. Regras de bloqueio continuam superiores ao score.

# 17. Estratégia de Renda

- Meta de yield.
- Meta de renda líquida.
- Vacância máxima.
- Liquidez mínima.
- Ticket máximo.
- Reforma máxima.
- Prazo máximo de estabilização.
- Perfil de imóvel preferido.
- Concentração máxima por região.

# 18. Estratégia de Revenda

- Desconto líquido mínimo.
- Margem mínima.
- Prazo máximo de saída.
- Liquidez mínima.
- Custo máximo de reforma.
- Capital máximo por operação.
- Preço máximo de compra.
- Concentração máxima.

# 19. Estratégia de Valorização

- Horizonte mínimo.
- Potencial de valorização.
- Infraestrutura esperada.
- Qualidade da localização.
- Liquidez futura.
- Renda durante a espera.
- Custo de oportunidade.
- Tolerância a capital imobilizado.

# 20. Estratégia MCMV / Baixa Renda

- Ticket compatível com público.
- Demanda local.
- Financiabilidade.
- Aluguel relativo à renda.
- Liquidez.
- Condição do imóvel.
- Custo de reforma.
- Potencial de revenda.
O perfil socioeconômico do público não deve ser usado como exclusão automática. A análise deve ser econômica, de demanda, liquidez e risco.

# 21. Estratégia para Terrenos

- Uso permitido.
- Potencial construtivo.
- Ticket.
- Demanda de compradores.
- Prazo de saída.
- Infraestrutura.
- Topografia.
- Capital imobilizado.
- Risco de desenvolvimento.

# 22. Estratégia para Apartamentos

- Condomínio.
- Liquidez.
- Preço/m².
- Vagas.
- Dormitórios.
- Demanda de locação.
- Demanda de venda.
- Financiabilidade.

# 23. Estratégia para Casas e Sobrados

- Terreno.
- Conservação.
- Ticket.
- Público familiar.
- Liquidez.
- Potencial de reforma.
- Financiabilidade.
- Uso alternativo.

# 24. Portfólio Atual

O Radar deve representar o portfólio existente para que novas oportunidades sejam avaliadas no contexto do patrimônio.

| Dimensão | Exemplos |
|---|---|
| Ativo | Imóvel/participação |
| Valor investido | Capital histórico |
| Valor atual | Estimativa atual |
| Renda | Aluguel líquido |
| Estratégia | Renda/revenda/valorização |
| Liquidez | Alta/média/baixa |
| Risco | Baixo/médio/alto |
| Localização | Cidade/região |
| Status | Ativo, venda, reforma etc. |


# 25. Diversificação

Diversificação não significa possuir muitos imóveis. Significa evitar que um único fator comprometa grande parte do capital.
- Diversificação geográfica.
- Diversificação por tipo.
- Diversificação por estratégia.
- Diversificação por prazo.
- Diversificação por perfil de demanda.
- Diversificação de risco.

# 26. Priorização de Oportunidades


| Prioridade | Condição |
|---|---|
| P1 | Excelente oportunidade + alta aderência + capital disponível |
| P2 | Boa oportunidade + alta aderência |
| P3 | Boa oportunidade + aderência parcial |
| P4 | Interessante, mas capital/concentração limitante |
| P5 | Monitoramento |
| Bloqueada | Regra crítica ou capital indisponível |


# 27. Alocação de Capital

Antes de aprovar uma compra, o Radar deve responder quanto capital será consumido e qual será a posição do portfólio após a operação.

| Pergunta | Saída |
|---|---|
| Quanto custa a operação? | Capital necessário |
| Quanto ficará livre? | Capital residual |
| Qual percentual do portfólio? | Concentração |
| Qual estratégia aumenta? | Exposição estratégica |
| Qual risco aumenta? | Exposição de risco |
| Qual renda potencial? | Impacto na renda |
| Qual liquidez do portfólio? | Liquidez consolidada |


# 28. Simulação Antes da Compra

- Selecionar oportunidade.
- Calcular custo econômico total.
- Reservar capital necessário.
- Simular concentração.
- Simular renda/retorno.
- Simular cenário conservador.
- Verificar reserva remanescente.
- Comparar com outras oportunidades.
- Emitir recomendação.

# 29. Comparação entre Oportunidades


| Oportunidade | Retorno | Risco | Liquidez | Capital | Fit |
|---|---|---|---|---|---|
| A | Alto | Médio | Alta | Médio | Alto |
| B | Muito alto | Alto | Baixa | Alto | Médio |
| C | Bom | Baixo | Alta | Baixo | Muito alto |

A oportunidade C pode ser priorizada mesmo com retorno absoluto inferior, se melhorar a eficiência e a diversificação do portfólio.

# 30. Eficiência do Capital

O Radar deve avaliar quanto retorno, renda ou margem é gerado por unidade de capital e por unidade de tempo.

| Métrica | Uso |
|---|---|
| Retorno / capital | Eficiência do capital |
| Renda / capital | Eficiência de renda |
| Margem / capital | Eficiência da operação |
| Margem / mês | Eficiência temporal |
| Renda líquida / risco | Qualidade ajustada ao risco |


# 31. Capital Imobilizado

- Capital preso por longo prazo reduz capacidade de aproveitar novas oportunidades.
- Operações em reforma consomem capacidade operacional.
- Imóveis de baixa liquidez exigem maior margem.
- O Radar deve penalizar excesso de capital imobilizado.

# 32. Custo de Oportunidade

Uma compra deve ser comparada às alternativas disponíveis. O capital utilizado em uma oportunidade deixa de estar disponível para outra.

| Situação | Tratamento |
|---|---|
| Poucas oportunidades | Pode aceitar margem menor, se aderente. |
| Muitas oportunidades excelentes | Exigir maior seletividade. |
| Capital escasso | Priorizar melhor retorno ajustado. |
| Capital abundante | Aumentar diversificação, sem abandonar prudência. |


# 33. Limites e Exceções

O investidor pode criar exceções, mas elas devem ser explícitas, justificadas e auditáveis.

| Exceção | Exemplo |
|---|---|
| EXC-21-01 | Exceder ticket por oportunidade excepcional |
| EXC-21-02 | Exceder concentração regional |
| EXC-21-03 | Aceitar liquidez menor por margem excepcional |
| EXC-21-04 | Aceitar reforma maior por desconto extraordinário |
| EXC-21-05 | Usar financiamento fora da preferência padrão |


# 34. Regras de Negócio


| ID | Regra | Resultado |
|---|---|---|
| INV21-001 | Capital livre abaixo da reserva mínima | BLOQUEAR novas compras |
| INV21-002 | Custo total excede limite por operação | BLOQUEAR/EXCEÇÃO |
| INV21-003 | Concentração excede limite | Reduzir prioridade |
| INV21-004 | Fit abaixo do mínimo | DO NOT BUY |
| INV21-005 | Capital imobilizado excede limite | Reduzir prioridade |
| INV21-006 | Oportunidade melhora diversificação | Aumentar prioridade |
| INV21-007 | Score alto, mas estratégia incompatível | Não priorizar |
| INV21-008 | Exceção sem justificativa | Não permitir |
| INV21-009 | Reserva comprometida após compra | BLOQUEAR |
| INV21-010 | Oportunidade excepcional supera limite | Permitir somente exceção formal |


# 35. Alertas do Investidor


| Evento | Alerta |
|---|---|
| Capital disponível cai | Recalcular prioridades |
| Concentração aumenta | Alerta de portfólio |
| Nova oportunidade excepcional | Prioridade máxima |
| Estratégia alterada | Reprocessar oportunidades |
| Meta de renda muda | Recalcular ranking |
| Reserva abaixo do mínimo | Bloquear aquisições |
| Ativo adquirido | Atualizar portfólio |
| Venda concluída | Liberar capital |


# 36. Ciclo do Capital

CAPITAL LIVRE → OPORTUNIDADE → AQUISIÇÃO → CAPITAL IMOBILIZADO → RENDA/VALORIZAÇÃO/REFORMA → SAÍDA → CAPITAL LIBERADO → NOVA OPORTUNIDADE
O Radar deve enxergar esse ciclo e não apenas a etapa de aquisição.

# 37. Cenário Integrado

Imagine duas oportunidades: A possui maior desconto, mas exige R$ 250 mil, baixa liquidez e concentração em uma região já representada no portfólio. B possui desconto menor, exige R$ 150 mil, alta liquidez e diversifica a localização. O Radar deve conseguir demonstrar que B pode ter maior prioridade para aquele investidor.

| Fator | A | B |
|---|---|---|
| Desconto | 30% | 22% |
| Capital | R$ 250 mil | R$ 150 mil |
| Liquidez | 55 | 90 |
| Concentração | Alta | Baixa |
| Fit | 65 | 92 |
| Prioridade | Menor | Maior |


# 38. Matriz Final de Decisão


| Qualidade | Fit | Capital | Resultado |
|---|---|---|---|
| Alta | Alta | Disponível | PRIORIDADE |
| Alta | Alta | Limitado | MONITOR/COMPARAR |
| Alta | Baixa | Disponível | MONITOR |
| Média | Alta | Disponível | AVALIAR |
| Baixa | Alta | Disponível | DO NOT BUY |
| Qualquer | Qualquer | Indisponível | BLOCK |
| Qualquer | Qualquer | Reserva comprometida | BLOCK |


# 39. Critérios de Aceite

- CA-D21 — O investidor possui objetivos configuráveis.
- CA-D21 — É possível manter múltiplas estratégias.
- CA-D21 — Capital disponível é separado de reserva.
- CA-D21 — O custo econômico total é considerado.
- CA-D21 — Existe limite por operação.
- CA-D21 — Existe controle de concentração.
- CA-D21 — O Radar calcula Investor Fit Score.
- CA-D21 — O Opportunity Score permanece separado.
- CA-D21 — O score composto considera aderência e confiança.
- CA-D21 — Exceções são justificadas e auditáveis.
- CA-D21 — O portfólio existente influencia novas decisões.
- CA-D21 — O capital imobilizado é considerado.
- CA-D21 — O custo de oportunidade é considerado.
- CA-D21 — É possível simular a compra antes da decisão.
- CA-D21 — Novas compras podem ser bloqueadas por falta de capital.
- CA-D21 — Uma oportunidade excepcional pode exigir exceção formal.
- CA-D21 — O sistema prioriza eficiência do capital, não quantidade de aquisições.

# 40. Relação com os Documentos


| Documento | Relação |
|---|---|
| 15 — Decisão | Define resultado e precedência. |
| 18 — Economia | Fornece custo, retorno e cenários. |
| 19 — Risco | Fornece risco e impacto. |
| 20 — Liquidez | Fornece demanda e saída. |
| 8 — Parâmetros | Permite configurar perfil e limites. |
| 7 — Workflow | Controla ciclo da oportunidade. |
| 12 — Traceabilidade | Relaciona regras, parâmetros e decisões. |
| 13 — Roadmap | Orienta implementação funcional. |


# 41. Próximo Documento

Recomendação: Documento 22 — Ranking, Priorização, Comparação e Motor de Decisão do Radar. O foco será transformar todas as dimensões anteriores em uma fila inteligente de oportunidades: o que aparece primeiro, por quê, o que mudou, quais oportunidades competem pelo mesmo capital e qual deve ser analisada antes.
