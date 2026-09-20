# Radar_Imobiliario_Documento_8_Catalogo_Completo_de_Parametros_Regras_e_Configuracoes_v1.0

🎯
RADAR IMOBILIÁRIO
Documento 8 — Catálogo Completo de Parâmetros,
Regras e Configurações do Investidor
Versão 1.0  |  Documento de Negócio
“Preço é o dado. Oportunidade é a análise.”

# 1. Objetivo

Este documento define o catálogo de parâmetros, regras e configurações que governam o comportamento do Radar Imobiliário. O objetivo é garantir que critérios de investimento não fiquem implícitos ou fixos, mas possam ser configurados, versionados, combinados, auditados e recalibrados.
Princípio central: o Radar deve ser flexível para diferentes investidores, estratégias, regiões e momentos de mercado.

# 2. Filosofia de Parametrização

- Tudo que representa uma preferência ou critério de decisão deve ser potencialmente parametrizável.
- Parâmetros globais definem o padrão; exceções podem ser aplicadas por estratégia, localização ou tipo de imóvel.
- Regra eliminatória protege contra erros graves; score organiza as oportunidades restantes.
- Ausência de informação não deve ser confundida com ausência de risco.
- Toda alteração relevante deve possuir versão, vigência e histórico.
- Uma configuração deve ser explicável: o sistema deve conseguir dizer quais parâmetros influenciaram a decisão.
- O mesmo imóvel pode receber avaliações diferentes conforme a estratégia ativa.

# 3. Hierarquia de Configuração


| Nível | Finalidade | Exemplo |
|---|---|---|
| Global | Padrão do Radar | Margem mínima geral |
| Perfil do investidor | Preferências pessoais | Ticket máximo |
| Estratégia | Objetivo de investimento | Yield mínimo para renda |
| Localização | Contexto regional | Priorizar bairro |
| Tipo de imóvel | Características do ativo | Aceitar/recusar terreno |
| Exceção | Tratamento específico | Condomínio X com regra própria |
| Análise | Ajuste pontual justificado | Custo de reforma confirmado |

Precedência sugerida: Global → Perfil → Estratégia → Localização/Tipo → Exceção → ajuste de análise, sempre preservando rastreabilidade.

# 4. Parâmetros Globais


| ID | Parâmetro | Unidade/Tipo | Objetivo |
|---|---|---|---|
| GLB-001 | Moeda | BRL | Padrão monetário |
| GLB-002 | Margem mínima de segurança | % | Proteção econômica mínima |
| GLB-003 | Confiança mínima | % | Nível mínimo de qualidade dos dados |
| GLB-004 | Score mínimo | 0–100 | Entrada no ranking |
| GLB-005 | Nível de risco máximo | Baixo/Médio/Alto | Limite geral |
| GLB-006 | Liquidez mínima | 0–100 | Facilidade de saída |
| GLB-007 | Custo de oportunidade | % a.a. | Referência financeira |
| GLB-008 | Horizonte de investimento | meses/anos | Prazo esperado |
| GLB-009 | Tolerância a exceções | Baixa/Média/Alta | Flexibilidade |
| GLB-010 | Data de validade da análise | dias | Freshness da tese |


# 5. Perfil do Investidor

O perfil traduz o que o investidor aceita, busca e evita. Não é apenas tolerância a risco: inclui capital, prazo, estratégia e preferências.

| ID | Parâmetro | Exemplos |
|---|---|---|
| INV-001 | Capital disponível | R$ 300 mil |
| INV-002 | Ticket máximo | R$ 250 mil |
| INV-003 | Entrada máxima | R$ 100 mil |
| INV-004 | Parcela máxima | R$ 3 mil/mês |
| INV-005 | Reserva mínima | R$ 50 mil |
| INV-006 | Horizonte | Curto/Médio/Longo |
| INV-007 | Objetivo | Renda/Revenda/Valorização |
| INV-008 | Tolerância a reforma | 0–4 |
| INV-009 | Tolerância a risco | Baixa/Média/Alta |
| INV-010 | Aceita ocupação | Sim/Não/Condicional |
| INV-011 | Aceita financiamento | Sim/Não |
| INV-012 | Aceita consórcio | Sim/Não |
| INV-013 | Prioridade de liquidez | Baixa/Média/Alta |
| INV-014 | Prioridade de renda | Baixa/Média/Alta |


# 6. Parâmetros de Localização

A localização deve ser parametrizada em múltiplos níveis, permitindo que o investidor priorize regiões sem transformar um bairro em regra universal.

| ID | Parâmetro | Exemplo |
|---|---|---|
| LOC-001 | Cidade permitida | Curitiba |
| LOC-002 | Cidade bloqueada | Cidade X |
| LOC-003 | Bairro prioritário | Portão |
| LOC-004 | Bairro aceitável | Novo Mundo |
| LOC-005 | Bairro condicional | Bairro X |
| LOC-006 | Zona de exclusão | Área definida pelo investidor |
| LOC-007 | Distância de referência | até 2 km de ponto |
| LOC-008 | Liquidez mínima regional | 70/100 |
| LOC-009 | Valorização histórica mínima | X% a.a. |
| LOC-010 | Yield regional mínimo | X% |
| LOC-011 | Perfil socioeconômico aceitável | parametrizado |
| LOC-012 | Restrição de risco local | parametrizada |

Importante: o Radar não deve usar “tipo de público” como sinônimo de “boa” ou “má” localização. A avaliação deve considerar liquidez, preço, demanda, infraestrutura, risco e estratégia.

# 7. Parâmetros por Tipo de Imóvel


| ID | Parâmetro | Exemplos |
|---|---|---|
| TIP-001 | Tipos aceitos | Apartamento, casa, sobrado, terreno |
| TIP-002 | Tipos bloqueados | Configurável |
| TIP-003 | Quartos mínimos | 1, 2, 3... |
| TIP-004 | Quartos máximos | Configurável |
| TIP-005 | Área mínima | m² |
| TIP-006 | Área máxima | m² |
| TIP-007 | Vagas mínimas | 0, 1, 2... |
| TIP-008 | Condomínio máximo | R$ |
| TIP-009 | Aceita MCMV/baixa renda | Sim/Não/Condicional |
| TIP-010 | Aceita reforma | Sim/Não/Condicional |
| TIP-011 | Aceita terreno | Sim/Não |
| TIP-012 | Aceita imóvel ocupado | Sim/Não/Condicional |


# 8. Preço, Ticket e Desconto

O preço de entrada é apenas um componente. O Radar deve diferenciar preço anunciado, preço de aquisição e custo econômico total.

| ID | Parâmetro | Exemplo |
|---|---|---|
| PRI-001 | Preço mínimo | R$ 80 mil |
| PRI-002 | Preço máximo | R$ 400 mil |
| PRI-003 | Desconto mínimo sobre avaliação | 20% |
| PRI-004 | Desconto mínimo sobre mercado | 15% |
| PRI-005 | Desconto líquido mínimo | 10% |
| PRI-006 | Faixa de ticket prioritária | R$ 150–250 mil |
| PRI-007 | Desconto excepcional | ≥30% |
| PRI-008 | Preço por m² máximo | R$ X/m² |
| PRI-009 | Preço por m² relativo à região | ≤ X% da mediana |


# 9. Parâmetros de Custo Econômico

O Radar deve trabalhar com custo total provável, e não apenas com o lance ou preço de compra.

| ID | Custo | Tratamento |
|---|---|---|
| CUS-001 | Preço/lance | Obrigatório quando conhecido |
| CUS-002 | Comissão | Percentual ou valor |
| CUS-003 | ITBI | Estimado/confirmado |
| CUS-004 | Registro/escritura | Estimado/confirmado |
| CUS-005 | Condomínio pendente | Estimado/confirmado |
| CUS-006 | IPTU/débitos | Estimado/confirmado |
| CUS-007 | Reforma | Faixa por cenário |
| CUS-008 | Desocupação | Faixa por cenário |
| CUS-009 | Regularização | Faixa por cenário |
| CUS-010 | Financiamento/custo financeiro | Cenário |
| CUS-011 | Reserva para imprevistos | Percentual |
| CUS-012 | Custo de venda | Percentual |

Regra: custo desconhecido deve permanecer como desconhecido ou ser representado por faixa/risco. Nunca assumir custo zero apenas porque não foi encontrado.

# 10. Parâmetros de Valuation


| ID | Parâmetro | Exemplo |
|---|---|---|
| VAL-001 | Mínimo de comparáveis | 5 |
| VAL-002 | Priorizar mesmo condomínio | Sim |
| VAL-003 | Raio máximo de comparáveis | 1 km |
| VAL-004 | Janela temporal | 12 meses |
| VAL-005 | Peso de comparáveis recentes | Configurável |
| VAL-006 | Peso de mesmo condomínio | Alto |
| VAL-007 | Desconto de venda rápida | 5–15% |
| VAL-008 | Margem conservadora | Configurável |
| VAL-009 | Confiança mínima de valuation | 70% |
| VAL-010 | Diferença máxima entre fontes | Configurável |

O valuation deve produzir pelo menos três referências: conservadora, base e otimista, sempre acompanhadas da confiança.

# 11. Parâmetros de Comparáveis


| ID | Critério | Configuração |
|---|---|---|
| CMP-001 | Mesmo condomínio | Prioridade máxima |
| CMP-002 | Mesmo bairro | Prioridade alta |
| CMP-003 | Distância | Configurável |
| CMP-004 | Área semelhante | Faixa configurável |
| CMP-005 | Quartos semelhantes | Sim/Não |
| CMP-006 | Vagas semelhantes | Sim/Não |
| CMP-007 | Padrão construtivo | Baixo/Médio/Alto |
| CMP-008 | Estado de conservação | Ajustar |
| CMP-009 | Anúncio muito antigo | Penalizar |
| CMP-010 | Outlier | Excluir/penalizar |


# 12. Renda, Aluguel e Yield


| ID | Parâmetro | Exemplo |
|---|---|---|
| REN-001 | Aluguel mensal estimado | R$ |
| REN-002 | Yield bruto mínimo | 0,8% / mês |
| REN-003 | Yield alvo | 1,0% / mês |
| REN-004 | Vacância | % |
| REN-005 | Inadimplência | % |
| REN-006 | Condomínio não recuperável | R$ |
| REN-007 | IPTU não recuperável | R$ |
| REN-008 | Manutenção | % |
| REN-009 | Yield líquido mínimo | % |
| REN-010 | Prazo máximo para alugar | dias |
| REN-011 | Aluguel conservador/base/otimista | Cenários |


# 13. Parâmetros de Liquidez


| ID | Parâmetro | Exemplo |
|---|---|---|
| LIQ-001 | Score mínimo de liquidez | 70 |
| LIQ-002 | Prazo máximo de venda | 180 dias |
| LIQ-003 | Prazo alvo de venda | 90 dias |
| LIQ-004 | Desconto máximo para saída | 10% |
| LIQ-005 | Quantidade mínima de compradores potenciais | Configurável |
| LIQ-006 | Demanda de aluguel | Baixa/Média/Alta |
| LIQ-007 | Liquidez por bairro | Score regional |
| LIQ-008 | Liquidez por ticket | Score por faixa |


# 14. Parâmetros de Risco


| ID | Risco | Tratamento |
|---|---|---|
| RISK-001 | Risco jurídico crítico | Bloqueio |
| RISK-002 | Ocupação | Peso/condição |
| RISK-003 | Débitos incertos | Penalidade/faixa |
| RISK-004 | Matrícula inconsistente | Bloqueio/pêndencia |
| RISK-005 | Processo relevante | Investigação |
| RISK-006 | Reforma elevada | Penalidade |
| RISK-007 | Baixa liquidez | Penalidade/bloqueio |
| RISK-008 | Dados insuficientes | Redução de confiança |
| RISK-009 | Risco de desocupação | Cenário |
| RISK-010 | Risco de revenda | Penalidade |

A severidade do risco e o nível de confiança devem ser tratados separadamente.

# 15. Parâmetros de Confiança e Qualidade dos Dados


| ID | Parâmetro | Exemplo |
|---|---|---|
| CONF-001 | Confiança do preço | Alta/Média/Baixa |
| CONF-002 | Confiança do valuation | Alta/Média/Baixa |
| CONF-003 | Confiança do aluguel | Alta/Média/Baixa |
| CONF-004 | Confiança dos custos | Alta/Média/Baixa |
| CONF-005 | Confiança jurídica | Alta/Média/Baixa |
| CONF-006 | Dados mínimos para score | Configurável |
| CONF-007 | Fator de confiança | 1,00 / 0,95 / 0,88... |
| CONF-008 | Prazo de validade da evidência | dias |

Exemplo de fator ilustrativo: muito alta 1,00; alta 0,95; média 0,88; baixa 0,75; muito baixa 0,60. Valores devem ser calibrados por backtest.

# 16. Parâmetros por Estratégia


| Estratégia | Parâmetros prioritários |
|---|---|
| Renda | Yield, aluguel, vacância, liquidez de locação, condomínio, estabilidade da demanda |
| Revenda/Flip | Desconto líquido, reforma, margem, prazo de venda, custo de saída |
| Valorização | Localização, tendência regional, infraestrutura, escassez, horizonte |
| MCMV/Baixa renda | Ticket, demanda, financiamento, aluguel, liquidez, risco |
| Terreno | Potencial construtivo, localização, uso, liquidez, documentação |
| Apartamento | Condomínio, vaga, padrão, liquidez, aluguel, comparáveis |
| Casa/Sobrado | Terreno, conservação, localização, segurança, liquidez, reforma |
| 1 dormitório | Demanda, ticket, aluguel, liquidez, público-alvo |


# 17. Pesos e Limiares do Score

O score não substitui regras eliminatórias. Ele organiza as oportunidades que sobreviveram às regras.

| Componente | Peso ilustrativo |
|---|---|
| Desconto líquido | 25% |
| Margem de segurança | 20% |
| Liquidez | 15% |
| Localização | 15% |
| Risco | 10% |
| Renda/Yield | 5% |
| Valorização | 5% |
| Qualidade da oportunidade | 5% |

Faixas ilustrativas: 90–100 Excepcional; 80–89 Excelente; 70–79 Muito boa; 60–69 Interessante; 50–59 Especulativa; <50 Fraca. Esses limites são calibráveis.

# 18. Regras Eliminatórias, Suaves e Condicionais


| Tipo | Comportamento | Exemplo |
|---|---|---|
| Hard Rule | Elimina ou bloqueia | Risco jurídico crítico |
| Soft Rule | Reduz score | Liquidez abaixo do alvo |
| Conditional | Aceita sob condição | Comprar somente se dívida ≤ X |
| Informational | Não decide | Dados incompletos, mas alerta |
| Override | Exceção justificada | Bairro normalmente bloqueado |

Uma exceção nunca deve apagar a regra original. Deve registrar quem/qual configuração permitiu a exceção, motivo e validade.

# 19. Parâmetros de Exceção


| ID | Parâmetro | Objetivo |
|---|---|---|
| EXC-001 | Regra excepcional | Permitir caso específico |
| EXC-002 | Prazo de validade | Evitar exceção permanente |
| EXC-003 | Justificativa obrigatória | Explicabilidade |
| EXC-004 | Evidência obrigatória | Base factual |
| EXC-005 | Alçada de aprovação | Controle |
| EXC-006 | Impacto no score | Transparência |
| EXC-007 | Reavaliação automática | Retorno à regra padrão |


# 20. Parâmetros de Alertas


| ID | Evento | Exemplo |
|---|---|---|
| ALT-001 | Nova oportunidade | Entrou no radar |
| ALT-002 | Preço caiu | Queda ≥ 10% |
| ALT-003 | Score subiu | Passou de 69 para 80 |
| ALT-004 | Valuation subiu | Nova evidência |
| ALT-005 | Risco novo | Processo/dívida |
| ALT-006 | Risco resolvido | Pendência encerrada |
| ALT-007 | Regra atendida | Condição de compra atingida |
| ALT-008 | Oportunidade expirando | Fonte/condição antiga |
| ALT-009 | Mudança de status | Leilão/status alterado |
| ALT-010 | Reavaliação | Evento material |

Cada alerta deve possuir prioridade, condição, canal, frequência máxima e regra anti-fadiga.

# 21. Parâmetros de Workflow


| Parâmetro | Valores possíveis |
|---|---|
| Estado inicial | Captured |
| Qualificação | Qualified / Rejected / Blocked |
| Análise | In Analysis / Pending |
| Acompanhamento | Monitoring |
| Decisão | Approved / Conditional / Rejected |
| Aquisição | Acquired |
| Encerramento | Closed |

Estados e transições devem ser configuráveis dentro de limites de governança, sem permitir que uma configuração elimine rastreabilidade.

# 22. Monitoramento e Reavaliação


| ID | Gatilho | Ação |
|---|---|---|
| MON-001 | Mudança de preço | Recalcular economia |
| MON-002 | Mudança de status | Reavaliar oportunidade |
| MON-003 | Novo comparável relevante | Atualizar valuation |
| MON-004 | Novo risco | Recalcular risco |
| MON-005 | Mudança de aluguel | Atualizar yield |
| MON-006 | Mudança de estratégia | Recalcular score |
| MON-007 | Regra alterada | Reprocessar elegibilidade |
| MON-008 | Evidência vencida | Reduzir confiança |


# 23. Frescor dos Dados

Cada família de informação pode ter prazo de validade diferente. O Radar deve evitar tratar dados antigos como se fossem atuais.

| Informação | Freshness sugerido |
|---|---|
| Preço/status da oportunidade | Muito curto |
| Leilão/data | Muito curto |
| Comparáveis | Curto/Médio |
| Aluguel | Curto/Médio |
| Valuation | Médio |
| Infraestrutura/localização | Longo, salvo mudança material |
| Matrícula/documentação | Até mudança/evidência nova |


# 24. Conflitos e Precedência

Quando duas configurações conflitarem, a decisão deve seguir uma hierarquia explícita. Exemplo: uma regra global pode bloquear uma localização, mas uma estratégia pode permitir exceção somente se uma condição adicional for satisfeita.

| Prioridade | Regra |
|---|---|
| 1 | Bloqueio jurídico/risco crítico |
| 2 | Restrição legal ou documental |
| 3 | Regra explícita de exclusão |
| 4 | Regra condicional |
| 5 | Preferência da estratégia |
| 6 | Preferência do tipo de imóvel |
| 7 | Score e ranking |

O Radar nunca deve usar um score alto para “vencer” um bloqueio crítico.

# 25. Governança, Versionamento e Auditoria

- Toda configuração deve possuir identificador, versão, data de início, data de fim quando aplicável e status.
- Mudanças de pesos ou regras devem registrar motivo.
- O histórico de análises deve preservar qual versão das regras foi utilizada.
- Resultados anteriores não devem ser reescritos silenciosamente.
- Exceções devem possuir justificativa e evidência.
- Configurações experimentais devem ser separadas das configurações oficiais.

# 26. Exemplo de Configuração — Investidor de Renda


| Parâmetro | Configuração ilustrativa |
|---|---|
| Ticket máximo | R$ 300 mil |
| Yield alvo | ≥ 1,0% a.m. |
| Yield mínimo aceitável | ≥ 0,8% a.m. |
| Liquidez | ≥ 70/100 |
| Reforma | Até nível 2 |
| Risco jurídico crítico | Bloquear |
| Ocupação | Condicional |
| Margem de segurança | ≥ 15% |
| Confiança mínima | ≥ 75% |
| Score mínimo | ≥ 70 |


# 27. Exemplo de Configuração — Revenda


| Parâmetro | Configuração ilustrativa |
|---|---|
| Ticket máximo | R$ 400 mil |
| Desconto líquido | ≥ 20% |
| Margem após reforma | ≥ 15% |
| Prazo de saída | ≤ 180 dias |
| Custo de venda | Parametrizado |
| Reforma | Até nível 3 |
| Liquidez | ≥ 75/100 |
| Risco | Baixo/Médio |
| Score mínimo | ≥ 75 |


# 28. Exemplo de Configuração — MCMV / Baixa Renda


| Parâmetro | Configuração ilustrativa |
|---|---|
| Tipo | Apartamento/casa |
| Ticket | Faixa parametrizada |
| Demanda | ≥ média |
| Financiabilidade | Preferencial |
| Yield | Peso médio/alto |
| Liquidez | ≥ 70/100 |
| Localização | Aceitável, sem zona de exclusão |
| Condomínio | Limite proporcional ao aluguel |
| Risco | Baixo/Médio |
| Score mínimo | ≥ 65 |


# 29. O que NÃO deve ficar fixo

- Bairros considerados bons ou ruins.
- Tipos de imóvel considerados bons ou ruins.
- Percentuais de desconto considerados automaticamente excelentes.
- Yield mínimo universal.
- Ticket máximo universal.
- Pesos do score sem versão.
- Custos assumidos como zero quando não conhecidos.
- Uma única estratégia de investimento.
- Uma única fonte de imóveis.
- Uma única forma de aquisição.

# 30. Catálogo Consolidado de Parâmetros


| Grupo | Domínio | Qtd./Modelo |
|---|---|---|
| GLB | Globais | 10 |
| INV | Investidor | 14 |
| LOC | Localização | 12 |
| TIP | Tipo de imóvel | 12 |
| PRI | Preço/ticket | 9 |
| CUS | Custos | 12 |
| VAL | Valuation | 10 |
| CMP | Comparáveis | 10 |
| REN | Renda/yield | 11 |
| LIQ | Liquidez | 8 |
| RISK | Risco | 10 |
| CONF | Confiança | 8 |
| STR | Estratégia | variável |
| SCORE | Score | variável |
| EXC | Exceções | 7 |
| ALT | Alertas | 10 |
| MON | Monitoramento | 8 |


# 31. Ciclo de Vida da Configuração

CONFIGURAR → VALIDAR → PUBLICAR → APLICAR → MONITORAR → CALIBRAR → VERSIONAR → SUBSTITUIR
Uma configuração nova não deve alterar retroativamente análises históricas. Ela passa a valer a partir de sua vigência.

# 32. Calibração e Backtest

Os valores deste documento são pontos de partida. O Radar deve aprender com o histórico: oportunidades encontradas, oportunidades rejeitadas, decisões de compra, preço efetivo de saída, aluguel realizado, prazo de venda, custos reais e riscos materializados.

| Métrica | Pergunta |
|---|---|
| Precisão do ranking | As melhores posições realmente eram melhores? |
| Falsos positivos | Quantas oportunidades pareciam boas e não eram? |
| Falsos negativos | Quantas boas oportunidades foram descartadas? |
| Erro de valuation | Quanto o valor estimado divergiu do realizado? |
| Erro de aluguel | Quanto o aluguel previsto divergiu do realizado? |
| Erro de custo | Quanto o custo previsto divergiu do real? |
| Liquidez | O prazo previsto foi compatível com a saída? |
| Retorno real | A tese entregou o retorno esperado? |


# 33. Matriz Final de Decisão


| Elegibilidade | Risco | Confiança | Score | Resultado |
|---|---|---|---|---|
| Bloqueada | Qualquer | Qualquer | Qualquer | BLOCKED |
| Aprovada | Crítico | Qualquer | Qualquer | BLOCKED |
| Aprovada | Aceitável | Baixa | Alto | MONITORAR / CONFIRMAR |
| Aprovada | Aceitável | Alta | ≥ mínimo | OPORTUNIDADE |
| Aprovada | Aceitável | Alta | Muito alto | PRIORIDADE |
| Condicional | Controlável | Alta/Média | ≥ mínimo | BUY IF |


# 34. Princípios Finais

- O Radar deve encontrar oportunidades, não simplesmente imóveis baratos.
- Parâmetros devem ser configuráveis e versionados.
- Estratégia muda a interpretação do mesmo imóvel.
- Hard rules protegem; score prioriza.
- Risco e confiança são dimensões diferentes.
- Dados desconhecidos devem permanecer explicitamente desconhecidos.
- Toda decisão deve ser explicável.
- Toda oportunidade deve ter histórico.
- Exceções devem ser temporárias, justificadas e auditáveis.
- O sistema deve ser capaz de evoluir sem reescrever suas premissas históricas.

# 35. Próximo Documento Recomendado

Documento 9 — Especificação Funcional dos Módulos e Casos de Uso. A partir deste catálogo, o próximo passo é transformar os conceitos em módulos funcionais, telas/fluxos de negócio, ações do usuário, entradas, saídas, regras aplicadas e critérios de aceite — ainda sem entrar em arquitetura ou tecnologia.
