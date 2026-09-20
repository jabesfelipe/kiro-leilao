# Radar_Imobiliario_Documento_20_Liquidez_Demanda_Locacao_Venda_Saida_v1.0

🏠 RADAR IMOBILIÁRIO
Documento 20
Liquidez, Demanda, Locação, Venda e Estratégias de Saída
Especificação Funcional de Negócio | Versão 1.0
COMPRAR → MANTER → ALUGAR/VENDER → REALIZAR VALOR → RECUPERAR CAPITAL

# 1. Objetivo

Definir como o Radar deve analisar liquidez, demanda, locação, venda e estratégias de saída. A análise deve responder não apenas se um imóvel é barato, mas se existe demanda suficiente para transformar o investimento em renda ou caixa dentro do prazo esperado.
- Estimar liquidez de venda e locação.
- Identificar público-alvo.
- Estimar prazo de saída.
- Definir preço de saída em diferentes cenários.
- Incorporar liquidez ao score, margem e preço máximo.
- Permitir estratégias diferentes de saída.

# 2. Princípio Central

Liquidez é parte do valor econômico. Um imóvel pode ter grande desconto e ainda ser uma oportunidade ruim se permanecer muito tempo sem comprador ou locatário.

| Pergunta | Impacto |
|---|---|
| Existe demanda? | Define possibilidade de saída. |
| Quem compra/aluga? | Define público-alvo. |
| Por quanto? | Define preço de saída. |
| Em quanto tempo? | Define capital imobilizado. |
| Quão sensível é o preço? | Define margem necessária. |
| Há alternativas melhores? | Define oportunidade relativa. |


# 3. Liquidez de Venda x Liquidez de Locação


| Dimensão | Venda | Locação |
|---|---|---|
| Demanda | Compradores | Locatários |
| Preço | Valor de saída | Aluguel |
| Prazo | Tempo até venda | Tempo até ocupação |
| Concorrência | Imóveis à venda | Imóveis para locação |
| Ticket | Impacta financiamento/capital | Impacta capacidade de pagamento |
| Perfil | Investidor/morador | Morador/empresa |
| Estratégia | Revenda/valorização | Renda |


# 4. Indicadores de Liquidez


| Indicador | Descrição |
|---|---|
| Tempo estimado de venda | Prazo esperado para realizar a saída. |
| Tempo estimado de locação | Prazo esperado até ocupação. |
| Demanda relativa | Força da procura no segmento. |
| Oferta concorrente | Quantidade de alternativas disponíveis. |
| Absorção | Velocidade com que estoque é consumido. |
| Desconto necessário | Redução necessária para acelerar a saída. |
| Ticket relativo | Preço comparado ao mercado local. |
| Financiabilidade | Facilidade de financiamento do público. |
| Liquidez histórica | Evidências de vendas/locações anteriores. |


# 5. Score de Liquidez


| Faixa | Interpretação | Tratamento |
|---|---|---|
| 90–100 | Muito líquida | Prioridade |
| 80–89 | Alta | Favorável |
| 70–79 | Boa | Aceitável |
| 60–69 | Média | Atenção |
| 50–59 | Baixa | Margem maior |
| <50 | Muito baixa | MONITOR/DO NOT BUY |
| Indefinida | Dados insuficientes | PENDENTE |

As faixas são ilustrativas e devem ser parametrizadas por mercado e estratégia.

# 6. Fatores de Demanda

- Localização.
- Faixa de preço.
- Tipo e tamanho do imóvel.
- Quantidade de dormitórios.
- Vagas.
- Padrão e conservação.
- Condomínio.
- Financiabilidade.
- Infraestrutura e serviços.
- Perfil do público local.
- Oferta concorrente.

# 7. Público-Alvo


| Segmento | Perguntas |
|---|---|
| Morador | O imóvel atende família/indivíduo local? |
| Investidor | O yield e a liquidez atraem investidores? |
| Primeiro imóvel | Ticket e financiamento são compatíveis? |
| MCMV/baixa renda | Existe demanda e capacidade de financiamento? |
| Alto padrão | Existe público suficiente para o ticket? |
| Comercial | Há empresas/usuários para o espaço? |
| Terreno | Quem compraria e para qual finalidade? |


# 8. Demanda por Faixa de Preço

O mesmo bairro pode apresentar liquidez completamente diferente por faixa de ticket. O Radar deve analisar o imóvel dentro do seu submercado.

| Faixa | Exemplo de análise |
|---|---|
| Baixo ticket | Volume de demanda, financiamento, renda. |
| Ticket médio | Oferta concorrente e público predominante. |
| Ticket alto | Profundidade de compradores e tempo de saída. |
| Ticket muito alto | Mercado mais restrito e maior sensibilidade. |


# 9. Concorrência

- Quantidade de imóveis similares disponíveis.
- Faixa de preços.
- Tempo de anúncio, quando disponível.
- Condição dos concorrentes.
- Diferenças de localização.
- Diferença entre preço e qualidade.
- Existência de imóveis com melhor relação preço/benefício.
Um imóvel não deve ser avaliado isoladamente; deve competir com as alternativas que o comprador/locatário encontrará.

# 10. Preço de Saída


| Cenário | Uso |
|---|---|
| Otimista | Potencial máximo; não deve sustentar sozinho a decisão. |
| Base | Preço mais provável. |
| Conservador | Preço prudente para testar margem. |
| Venda rápida | Preço necessário para acelerar liquidez. |

Preço de saída deve ser compatível com comparáveis e público-alvo, não simplesmente com o valor de mercado estimado.

# 11. Tempo de Saída


| Fator | Efeito |
|---|---|
| Alta demanda | Reduz prazo. |
| Baixa concorrência | Reduz prazo. |
| Preço competitivo | Reduz prazo. |
| Preço alto | Aumenta prazo. |
| Imóvel específico | Aumenta prazo. |
| Reforma incompleta | Pode aumentar prazo. |
| Documentação problemática | Aumenta prazo. |
| Ocupação | Pode aumentar significativamente. |


# 12. Custo do Tempo

Cada mês adicional pode gerar condomínio, impostos, manutenção, financiamento e custo de oportunidade.

| Prazo | Impacto |
|---|---|
| 0–3 meses | Baixo carregamento |
| 3–6 meses | Moderado |
| 6–12 meses | Alto |
| >12 meses | Muito alto; exigir margem adicional |

As faixas são exemplos e devem ser configuráveis.

# 13. Estratégia de Renda


| Indicador | Pergunta |
|---|---|
| Aluguel | Quanto o mercado paga? |
| Vacância | Quanto tempo pode ficar vazio? |
| Renda líquida | Quanto sobra após custos? |
| Yield | Retorno mensal/anual sobre capital. |
| Liquidez | Quão fácil é encontrar locatário? |
| Reajuste | Potencial de atualização da renda. |
| Saída | O imóvel continua vendável? |


# 14. Estratégia de Revenda

- Preço de saída conservador.
- Tempo de venda.
- Custo de corretagem/venda.
- Custo de carregamento.
- Reforma e preparação.
- Margem mínima.
- Preço máximo de entrada.
- Sensibilidade a desconto na venda.

# 15. Estratégia de Valorização

- Horizonte.
- Tendência local.
- Infraestrutura.
- Demanda futura.
- Oferta futura.
- Liquidez esperada.
- Renda durante a espera.
- Custo de capital.

# 16. Estratégia Híbrida

O Radar deve permitir estratégias como comprar → reformar → alugar → vender posteriormente, ou comprar → alugar enquanto aguarda valorização.

| Estratégia | Exemplo |
|---|---|
| Renda + valorização | Alugar enquanto aguarda valorização. |
| Renda + revenda | Gerar renda temporária e vender. |
| Revenda + valorização | Comprar desconto e aguardar janela. |
| MCMV + renda | Comprar para locação dentro do segmento. |
| Terreno + desenvolvimento | Comprar, regularizar/desenvolver e vender. |


# 17. Liquidez e Preço Máximo

Baixa liquidez deve reduzir o preço máximo aceitável, porque aumenta prazo, risco e custo de capital.

| Liquidez | Preço máximo |
|---|---|
| Muito alta | Pode suportar preço maior dentro da margem. |
| Alta | Preço normal da estratégia. |
| Média | Exigir margem adicional. |
| Baixa | Desconto adicional necessário. |
| Muito baixa | Somente exceção formal. |
| Indefinida | Não calcular preço máximo definitivo. |


# 18. Liquidez e Margem

Uma margem de 15% em uma operação que pode levar 18 meses é economicamente diferente de 15% em uma operação que pode sair em 3 meses.

| Prazo | Tratamento |
|---|---|
| Curto | Margem padrão. |
| Médio | Margem adicional. |
| Longo | Margem significativamente maior. |
| Incerto | Cenário conservador + contingência. |


# 19. Liquidez e Risco de Capital

- Quanto mais tempo o capital ficar imobilizado, maior a exposição.
- Operações financiadas são mais sensíveis ao prazo.
- Operações de reforma são sensíveis a atrasos.
- O custo de oportunidade aumenta com o prazo.
- O Radar deve comparar retorno ajustado pelo tempo.

# 20. Break-even de Saída

O Radar deve calcular o menor preço de venda necessário para cobrir todo o capital empregado.

| Componente | Exemplo |
|---|---|
| Capital investido | Compra + custos + reforma |
| Carregamento | Custo mensal × prazo |
| Venda | Corretagem e custos |
| Break-even | Preço que zera o resultado |


# 21. Preço de Saída por Estratégia


| Estratégia | Referência |
|---|---|
| Revenda | Comparáveis + condição pós-reforma. |
| Renda | Aluguel de mercado + liquidez. |
| Valorização | Projeção prudente + horizonte. |
| MCMV | Capacidade do público + financiamento. |
| Terreno | Mercado + potencial de uso. |


# 22. Liquidez em MCMV / Baixa Renda

Liquidez deve ser analisada pela demanda e capacidade financeira do público, não por preconceito sobre o perfil socioeconômico.
- Disponibilidade de financiamento.
- Ticket compatível.
- Oferta concorrente.
- Demanda local.
- Aluguel relativo à renda.
- Tempo de absorção.
- Qualidade e localização dentro do segmento.

# 23. Liquidez de 1 Dormitório

- Demanda de estudantes/profissionais quando existente.
- Proximidade de emprego, transporte e serviços.
- Condomínio.
- Preço de entrada.
- Aluguel e yield.
- Oferta concorrente.
- Facilidade de revenda.

# 24. Liquidez de Casas e Sobrados

- Ticket.
- Área do terreno.
- Conservação.
- Localização.
- Vagas.
- Segurança/percepção local.
- Potencial de reforma.
- Público familiar.
- Financiabilidade.

# 25. Liquidez de Terrenos

- Zoneamento.
- Potencial construtivo.
- Infraestrutura.
- Dimensões.
- Topografia.
- Demanda de construtores/compradores.
- Tempo de desenvolvimento.
- Número de compradores potenciais.

# 26. Matriz de Liquidez x Estratégia


| Liquidez | Renda | Revenda | Valorização | Terreno |
|---|---|---|---|---|
| Muito alta | Excelente | Excelente | Boa | Boa |
| Alta | Excelente | Muito boa | Boa | Boa |
| Média | Boa | Boa | Boa | Média |
| Baixa | Cautela | Cautela | Pode aceitar | Cautela |
| Muito baixa | Somente exceção | Geralmente evitar | Somente tese forte | Somente tese forte |


# 27. Cenários de Saída


| Cenário | Saída | Prazo | Interpretação |
|---|---|---|---|
| S-01 | Preço alto | Curto | Otimista |
| S-02 | Preço base | Prazo esperado | Base |
| S-03 | Preço menor | Prazo maior | Conservador |
| S-04 | Venda rápida | Preço reduzido | Stress de liquidez |
| S-05 | Sem saída no prazo | Muito longo | Reavaliar tese |


# 28. Monitoramento de Liquidez

- Mudança na quantidade de concorrentes.
- Mudança nos preços concorrentes.
- Mudança no aluguel.
- Mudança na demanda.
- Tempo de anúncio.
- Mudança no financiamento.
- Mudança no ticket do segmento.
- Mudança de infraestrutura/localização.

# 29. Alertas de Liquidez


| Evento | Alerta |
|---|---|
| Liquidez sobe acima do gatilho | Oportunidade fortalecida |
| Liquidez cai | Reavaliar score |
| Preço de concorrentes cai | Reavaliar saída |
| Aluguel cai | Reavaliar renda |
| Prazo esperado aumenta | Recalcular carregamento |
| Demanda aumenta | Reavaliar valorização |
| Imóvel fica muito tempo sem interessados | Alerta negativo |


# 30. Score de Saída


| Componente | Peso ilustrativo |
|---|---|
| Demanda | 25% |
| Preço competitivo | 20% |
| Liquidez histórica/estimada | 20% |
| Ticket/financiabilidade | 15% |
| Concorrência | 10% |
| Condição do imóvel | 5% |
| Documentação/operacional | 5% |

Pesos são ilustrativos e devem ser configuráveis.

# 31. Exemplo Integrado

Um imóvel pode apresentar valuation de R$ 300 mil, custo econômico de R$ 220 mil e desconto líquido de 26,7%, mas possuir liquidez apenas 55/100 e prazo estimado de 12 meses. O Radar deve exigir margem maior e pode classificar a operação como MONITOR ou BUY IF. Outro imóvel com desconto de 20%, liquidez 90/100 e prazo de 3 meses pode ter melhor relação risco/retorno.

| Imóvel | Desconto | Liquidez | Prazo | Leitura |
|---|---|---|---|---|
| A | 26,7% | 55 | 12 meses | Alto desconto, alta exposição |
| B | 20% | 90 | 3 meses | Menor desconto, maior liquidez |
| Conclusão |  |  |  | B pode ser melhor oportunidade relativa |


# 32. Regras de Negócio


| ID | Regra | Resultado |
|---|---|---|
| LIQ20-001 | Liquidez abaixo do mínimo da estratégia | Reduz score/DO NOT BUY |
| LIQ20-002 | Prazo acima do máximo | BUY IF/DO NOT BUY |
| LIQ20-003 | Venda rápida exige desconto adicional | Recalcular saída |
| LIQ20-004 | Demanda insuficiente | MONITOR/DO NOT BUY |
| LIQ20-005 | Concorrente claramente superior | Reduz prioridade |
| LIQ20-006 | Aluguel abaixo do mínimo | Não aderente à renda |
| LIQ20-007 | Liquidez indefinida | Reduz confiança |
| LIQ20-008 | Mercado melhora materialmente | Reavaliar |
| LIQ20-009 | Mercado piora materialmente | Reavaliar |
| LIQ20-010 | Preço de saída não cobre capital | DO NOT BUY |


# 33. Critérios de Aceite

- CA-D20 — O Radar diferencia liquidez de venda e de locação.
- CA-D20 — Demanda é analisada por segmento e público-alvo.
- CA-D20 — Preço de saída possui cenários.
- CA-D20 — Prazo de saída influencia custo de carregamento.
- CA-D20 — Liquidez influencia score.
- CA-D20 — Liquidez influencia margem exigida.
- CA-D20 — Liquidez influencia preço máximo.
- CA-D20 — É possível modelar venda rápida.
- CA-D20 — É possível modelar estratégia de renda.
- CA-D20 — É possível modelar estratégias híbridas.
- CA-D20 — MCMV/baixa renda não é excluído automaticamente.
- CA-D20 — Terrenos possuem critérios específicos.
- CA-D20 — Casas, sobrados e apartamentos possuem fatores próprios.
- CA-D20 — Eventos de mercado podem disparar reavaliação.
- CA-D20 — O Radar consegue comparar oportunidades de diferentes descontos pela relação risco/retorno.

# 34. Relação com os Documentos


| Documento | Relação |
|---|---|
| 17 — Valuation | Fornece valor de mercado e valor de saída. |
| 18 — Economia | Transforma prazo e saída em retorno. |
| 19 — Risco | Incorpora risco de liquidez e ocupação. |
| 15 — Decisão | Usa liquidez para BUY/BUY IF/MONITOR. |
| 8 — Parâmetros | Define mínimos, prazos e pesos. |
| 7 — Workflow | Gera eventos e alertas. |
| 14 — Dados | Fornece fontes de mercado. |
| 16 — Captura | Mantém histórico de ofertas e concorrência. |


# 35. Próximo Documento

Recomendação: Documento 21 — Estratégias do Investidor, Perfil, Portfólio e Alocação de Capital. O foco será conectar as oportunidades encontradas ao capital disponível, concentração, limite por operação, diversificação, renda passiva, revenda, valorização e prioridades do investidor.
