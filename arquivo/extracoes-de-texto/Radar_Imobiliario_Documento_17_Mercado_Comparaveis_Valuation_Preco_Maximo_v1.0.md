# Radar_Imobiliario_Documento_17_Mercado_Comparaveis_Valuation_Preco_Maximo_v1.0

🏠 RADAR IMOBILIÁRIO
Documento 17
Mercado, Comparáveis, Valuation e Preço Máximo de Compra
Especificação Funcional de Negócio | Versão 1.0
IMÓVEL → MERCADO → VALOR → CUSTO → MARGEM → PREÇO MÁXIMO → OPORTUNIDADE

# 1. Objetivo

Definir como o Radar deve transformar o imóvel consolidado e as evidências de mercado em uma estimativa de valor, faixa de valor, confiança, cenários econômicos e preço máximo de compra por estratégia.
- Separar preço anunciado de valor de mercado.
- Definir critérios para seleção e qualidade dos comparáveis.
- Calcular desconto líquido e margem após custos.
- Determinar preço máximo aceitável para cada estratégia.
- Permitir que o mesmo imóvel tenha preços máximos diferentes conforme a estratégia.
- Preservar incerteza quando a evidência de mercado for insuficiente.

# 2. Princípio Central

O Radar não deve perguntar apenas 'qual é o valor deste imóvel?'. Deve responder quatro perguntas:
- Quanto o mercado provavelmente pagaria?
- Quanto custa economicamente adquirir e colocar o imóvel em condição de saída?
- Quanto de margem de segurança é necessário?
- Qual é o maior preço que ainda torna a operação interessante para esta estratégia?
O valor de mercado é uma estimativa. O preço máximo de compra é uma decisão estratégica derivada dessa estimativa.

# 3. Conceitos


| Conceito | Definição |
|---|---|
| Preço de oferta | Preço/lance informado pela fonte. |
| Valor de mercado | Estimativa do valor provável em condições normais. |
| Valor de venda rápida | Valor estimado para uma saída mais rápida. |
| Custo econômico total | Preço de aquisição + custos + reforma + contingências relevantes. |
| Desconto bruto | Diferença entre preço de oferta e valor de mercado. |
| Desconto líquido | Diferença entre custo econômico e valor de mercado. |
| Margem | Valor de mercado − custo econômico. |
| Margem de segurança | Proteção contra erro de valuation e imprevistos. |
| Preço máximo | Maior preço de aquisição compatível com a estratégia. |
| Confiança | Qualidade da evidência que sustenta o valuation. |
| Oportunidade relativa | Atratividade comparada a alternativas disponíveis. |


# 4. Hierarquia de Evidências de Mercado


| Nível | Evidência | Peso conceitual |
|---|---|---|
| A | Transações efetivamente realizadas e comparáveis | Muito alto |
| B | Múltiplas ofertas muito semelhantes e atuais | Alto |
| C | Ofertas semelhantes com ajustes | Médio |
| D | Estimativas indiretas / poucos comparáveis | Baixo |
| E | Analogia fraca ou dados antigos | Muito baixo |
| U | Sem evidência suficiente | Inconclusivo |

O Radar deve diferenciar preço pedido de preço efetivamente transacionado. Quando não houver dados de transação, a análise pode utilizar anúncios, mas deve reduzir a confiança.

# 5. Seleção de Comparáveis


| Critério | Prioridade |
|---|---|
| Mesmo condomínio/empreendimento | Muito alta |
| Mesma unidade/padrão | Muito alta |
| Mesma microregião | Alta |
| Tipo de imóvel semelhante | Alta |
| Área semelhante | Alta |
| Quartos/vagas semelhantes | Alta |
| Padrão construtivo semelhante | Alta |
| Condição semelhante | Alta |
| Data recente | Alta |
| Mesmo público-alvo | Alta |

- Comparável ruim não deve ser incluído apenas para aumentar o tamanho da amostra.
- Qualidade deve prevalecer sobre quantidade.
- Comparáveis incompatíveis devem ser excluídos ou explicitamente ajustados.

# 6. Quantidade de Comparáveis


| Situação | Tratamento |
|---|---|
| Muitos comparáveis de alta qualidade | Maior confiança; usar distribuição. |
| Quantidade razoável | Usar mediana e faixa. |
| Poucos comparáveis | Faixa mais ampla e confiança reduzida. |
| Um único comparável | Somente como evidência, não como verdade. |
| Nenhum comparável | Valuation inconclusivo ou baseado em método alternativo. |


# 7. Ajustes dos Comparáveis


| Diferença | Tratamento |
|---|---|
| Área | Ajustar preço total/preço por m² conforme segmento. |
| Quartos | Ajustar conforme impacto observado no mercado. |
| Vagas | Ajustar quando material. |
| Padrão | Separar baixo, médio, alto padrão. |
| Conservação | Separar reformado, original e deteriorado. |
| Condomínio | Considerar impacto na atratividade. |
| Andar/elevador | Ajustar quando relevante. |
| Localização | Considerar microdiferenças. |
| Data | Atualizar quando mercado mudou. |
| Características especiais | Tratar individualmente. |


# 8. Mesmo Condomínio

Comparáveis do mesmo condomínio possuem valor especial porque reduzem diferenças de localização e estrutura.
- Priorizar mesma torre/bloco quando possível.
- Comparar unidades de áreas e características próximas.
- Considerar diferenças de andar, posição, vaga e reforma.
- Não assumir que toda unidade do condomínio possui o mesmo valor por m².
- Usar o histórico de ofertas do próprio empreendimento quando disponível.

# 9. Preço por m²

Preço por m² é indicador auxiliar, não substituto do valuation.
- Usar área correta para o tipo de imóvel.
- Não comparar áreas privativas e totais sem ajuste.
- Separar segmentos muito diferentes.
- Analisar distribuição, mediana e dispersão.
- Investigar outliers.
O preço total e as características do imóvel continuam relevantes; dois imóveis com o mesmo preço/m² podem possuir liquidez e valor econômico diferentes.

# 10. Outliers


| Situação | Tratamento |
|---|---|
| Preço muito acima da amostra | Investigar; pode ser imóvel premium. |
| Preço muito abaixo | Investigar; pode conter problema ou oportunidade. |
| Anúncio antigo | Reduzir peso. |
| Imóvel claramente diferente | Excluir. |
| Erro evidente | Não usar como comparável. |
| Outlier recorrente | Investigar se representa submercado real. |


# 11. Métodos de Valuation


| Método | Aplicação |
|---|---|
| Comparativo | Principal para apartamentos/casas quando há amostra. |
| Preço/m² ajustado | Auxiliar para segmentos homogêneos. |
| Mesmo condomínio | Muito relevante em apartamentos. |
| Renda | Relevante quando imóvel é essencialmente de investimento. |
| Residual/potencial | Mais aplicável a terrenos e imóveis com potencial específico. |
| Analogia de mercado | Quando dados são escassos, com menor confiança. |
| Híbrido | Combinação de métodos quando necessário. |


# 12. Faixas de Valor

O valuation deve evitar uma falsa precisão. Sempre que possível, entregar:

| Saída | Objetivo |
|---|---|
| Conservador | Protege contra superestimação. |
| Base | Melhor estimativa central. |
| Otimista | Potencial superior, sem ser referência principal. |
| Venda rápida | Referência de liquidez/saída. |
| Confiança | Indica qualidade da estimativa. |


# 13. Exemplo de Valuation

Suponha comparáveis ajustados entre R$ 285 mil e R$ 315 mil, com mediana de R$ 300 mil. O Radar pode produzir valor base de R$ 300 mil, conservador de R$ 285 mil e otimista de R$ 315 mil, desde que a dispersão e a qualidade da amostra sustentem essas faixas.

| Cenário | Valor ilustrativo | Uso |
|---|---|---|
| Conservador | R$ 285.000 | Stress / margem |
| Base | R$ 300.000 | Decisão principal |
| Otimista | R$ 315.000 | Potencial, não garantia |
| Venda rápida | Ex.: R$ 270.000–285.000 | Teste de liquidez |


# 14. Valuation por Estratégia

O valor de mercado pode ser comum, mas o valor econômico para o investidor muda conforme a estratégia.

| Estratégia | Referência principal |
|---|---|
| Renda | Valor compatível com aluguel e yield. |
| Revenda | Valor de saída após reforma e custos. |
| Valorização | Valor atual + potencial futuro, descontado por risco/horizonte. |
| MCMV/baixa renda | Valor dentro da demanda e capacidade de financiamento do público. |
| Terreno | Valor de uso/potencial e mercado local. |


# 15. Custo Econômico Total

O preço de aquisição nunca deve ser usado sozinho na decisão.

| Componente | Exemplo |
|---|---|
| Preço de compra/lance | R$ 191.651 |
| Comissão | Valor aplicável |
| ITBI/registro/documentação | Estimativa |
| Condomínio/IPTU/débitos | Valor confirmado/estimado |
| Reforma | Orçamento/cenário |
| Regularização | Quando aplicável |
| Financiamento | Quando aplicável |
| Carregamento | Tempo até saída |
| Contingência | Margem parametrizada |

Custo econômico = soma dos componentes aplicáveis, mantendo desconhecidos explicitamente identificados.

# 16. Desconto Bruto x Desconto Líquido


| Métrica | Fórmula |
|---|---|
| Desconto bruto | 1 − (preço de aquisição / valor de mercado) |
| Desconto líquido | 1 − (custo econômico total / valor de mercado) |

Exemplo: valor de mercado R$ 300 mil e preço de aquisição R$ 191.651 → desconto bruto ≈ 36,1%. Se o custo econômico total for R$ 220 mil → desconto líquido ≈ 26,7%.

# 17. Margem de Segurança

Margem de segurança deve proteger contra erros de valuation, custos inesperados, tempo de saída e variações de mercado.

| Fator | Como afeta a margem exigida |
|---|---|
| Baixa confiança no valuation | Aumenta |
| Alta reforma | Aumenta |
| Baixa liquidez | Aumenta |
| Risco jurídico/posse | Aumenta |
| Mercado volátil | Aumenta |
| Dados robustos | Pode reduzir |
| Saída rápida e líquida | Pode reduzir |
| Múltiplas estratégias aderentes | Pode aumentar atratividade, sem eliminar risco |


# 18. Preço Máximo de Compra

O preço máximo deve ser calculado de trás para frente: parte-se do valor econômico de saída e descontam-se custos, margem e retorno exigido.

| Estratégia | Estrutura conceitual |
|---|---|
| Revenda | Preço máximo = valor de saída − custos de venda − reforma − carregamento − margem mínima |
| Renda | Preço máximo = aluguel compatível / yield mínimo − custos de aquisição/adequações |
| Valorização | Preço máximo = valor esperado ajustado ao risco − custos − margem requerida |
| MCMV | Preço máximo = valor compatível com demanda/financiamento − custos − margem |
| Terreno | Preço máximo = valor econômico do potencial − desenvolvimento − custos − margem |

O cálculo exato deve ser parametrizável e pode incorporar financiamento, prazo e impostos conforme a estratégia.

# 19. Preço Máximo e Preço Atual


| Situação | Interpretação |
|---|---|
| Preço atual muito abaixo do máximo | Grande folga; oportunidade forte. |
| Preço atual próximo do máximo | Pouca margem; monitorar. |
| Preço atual acima do máximo | Não comprar pela estratégia. |
| Preço máximo muda após nova informação | Recalcular oportunidade. |
| Preço máximo diferente por estratégia | Esperado e desejável. |


# 20. Oportunidade Relativa

Uma oportunidade não deve ser avaliada apenas contra um valor absoluto. Deve ser comparada com outras oportunidades disponíveis.
- Margem em relação ao risco.
- Desconto líquido em relação ao mercado.
- Liquidez.
- Confiança.
- Tempo e esforço para aquisição.
- Retorno potencial.
- Alternativas com melhor relação risco/retorno.
O melhor imóvel do Radar é o melhor dentro das alternativas elegíveis, não necessariamente o mais barato.

# 21. Cenários Econômicos


| Cenário | Premissas |
|---|---|
| Otimista | Saída próxima ao topo da faixa; custos controlados. |
| Base | Premissas mais prováveis. |
| Conservador | Valor menor + custos maiores + saída mais lenta. |
| Estressado | Valor de saída baixo + custos altos + prazo elevado. |

- BUY deve normalmente sobreviver ao cenário conservador conforme a estratégia.
- Se só funcionar no otimista, classificar como especulativa.
- Se nem o cenário base for viável, não recomendar compra.

# 22. Liquidez no Valuation

Valor de mercado e valor de venda rápida são diferentes. O Radar deve estimar ambos quando houver evidência.

| Situação | Efeito |
|---|---|
| Mercado muito líquido | Venda rápida próxima ao valor base. |
| Mercado normal | Desconto moderado para saída rápida. |
| Mercado pouco líquido | Desconto maior e prazo maior. |
| Imóvel muito específico | Faixa ampla e confiança menor. |


# 23. Valuation de Terrenos

- Zoneamento e uso permitido.
- Infraestrutura disponível.
- Dimensões e topografia.
- Potencial construtivo.
- Demanda por lotes na região.
- Comparáveis de terrenos similares.
- Custos para desenvolvimento/regularização.
- Prazo provável de saída.
Terreno não deve ser valorizado apenas por preço/m² de terrenos vizinhos sem considerar potencial e restrições.

# 24. Valuation de Casas e Sobrados

- Área do terreno.
- Área construída.
- Padrão e conservação.
- Vagas.
- Localização/microregião.
- Potencial de reforma/ampliação.
- Liquidez do perfil.
- Comparáveis efetivamente semelhantes.

# 25. Valuation de Apartamentos

- Área privativa.
- Condomínio.
- Vagas.
- Andar/elevador.
- Posição e insolação quando relevantes.
- Padrão do condomínio.
- Estado da unidade.
- Comparáveis do mesmo empreendimento.

# 26. Valuation MCMV / Baixa Renda

O valuation deve considerar a dinâmica específica desse mercado.
- Ticket compatível com público-alvo.
- Demanda real.
- Financiamento disponível.
- Aluguel praticado.
- Liquidez.
- Condição do imóvel.
- Comparáveis do mesmo segmento.
A classificação socioeconômica do público não deve ser usada como proxy automático de risco ou baixa qualidade.

# 27. Confiança do Valuation


| Confiança | Características |
|---|---|
| Muito alta | Comparáveis numerosos, atuais, homogêneos e/ou transações confirmadas. |
| Alta | Boa amostra com pequenos ajustes. |
| Média | Amostra razoável, alguma incerteza. |
| Baixa | Poucos comparáveis ou diferenças relevantes. |
| Muito baixa | Evidência fraca/indireta. |
| Inconclusiva | Não há base suficiente. |


# 28. Gatilhos de Revaluation

- Nova captura de preço.
- Mudança material no status.
- Novo comparável relevante.
- Alteração do aluguel.
- Nova informação física.
- Novo risco.
- Mudança relevante de mercado.
- Mudança de estratégia.
- Passagem de tempo além da validade configurada.

# 29. Cenários de Erro


| Erro | Proteção |
|---|---|
| Valuation superestimado | Cenário conservador + margem. |
| Comparável ruim | Qualificação de comparáveis. |
| Custo esquecido | Checklist de custo econômico. |
| Reforma subestimada | Níveis de reforma + contingência. |
| Saída otimista | Valor de venda rápida. |
| Mercado mudou | Frescor + revaluation. |
| Dado conflitante | Redução de confiança + pendência. |


# 30. Exemplo Completo

Exemplo ilustrativo: imóvel ofertado por R$ 191.651,31; valuation base R$ 300.000; custo econômico estimado R$ 220.000; margem R$ 80.000; desconto líquido ≈ 26,7%. Se o preço máximo de compra para uma estratégia de revenda for R$ 205.000 e para renda for R$ 230.000, o mesmo imóvel pode ser mais aderente à renda do que à revenda.

| Indicador | Resultado ilustrativo |
|---|---|
| Oferta | R$ 191.651 |
| Valor base | R$ 300.000 |
| Custo econômico | R$ 220.000 |
| Desconto líquido | 26,7% |
| Margem | R$ 80.000 |
| Preço máximo — revenda | R$ 205.000 |
| Preço máximo — renda | R$ 230.000 |
| Situação | Dentro dos dois limites; priorização depende de score/risco/liquidez |


# 31. Matriz de Decisão Econômica


| Condição | Resultado |
|---|---|
| Custo ≤ preço máximo + margem robusta | Favorecer |
| Custo próximo do máximo | Monitorar |
| Custo > máximo | DO NOT BUY na estratégia |
| Valuation inconclusivo | PENDENTE |
| Risco crítico | BLOCK |
| Valuation alto, mas confiança baixa | BUY IF/MONITOR |
| Boa economia + alta liquidez + alta confiança | Prioridade máxima |


# 32. Dados Obrigatórios para Valuation

- Imóvel identificado com confiança suficiente.
- Localização.
- Tipo.
- Área e tipo da área.
- Características relevantes.
- Comparáveis ou método alternativo explicitado.
- Data dos dados de mercado.
- Faixa de valor.
- Confiança.
- Premissas.
- Custos relevantes para preço máximo.

# 33. Critérios de Aceite

- CA-D17 — O Radar diferencia preço de oferta e valor de mercado.
- CA-D17 — Comparáveis possuem qualidade e relevância avaliadas.
- CA-D17 — Preço anunciado não é tratado como preço transacionado.
- CA-D17 — Valuation pode produzir faixa e não apenas valor pontual.
- CA-D17 — Confiança acompanha o valuation.
- CA-D17 — Custos econômicos são considerados antes de medir oportunidade.
- CA-D17 — Desconto líquido é calculável.
- CA-D17 — Margem de segurança é parametrizável.
- CA-D17 — Preço máximo pode ser calculado por estratégia.
- CA-D17 — O mesmo imóvel pode possuir preços máximos diferentes por estratégia.
- CA-D17 — Valuation pode ser refeito após eventos materiais.
- CA-D17 — Cenários conservador, base, otimista e estressado podem ser comparados.
- CA-D17 — Dados insuficientes não geram falsa precisão.
- CA-D17 — Liquidez influencia valor de saída e margem.
- CA-D17 — Terrenos, casas, sobrados, apartamentos e MCMV podem ter métodos específicos.
- CA-D17 — A decisão econômica pode ser explicada por comparáveis, premissas e custos.

# 34. Relação com o Radar

O Documento 17 transforma o imóvel consolidado do Documento 16 em uma unidade econômica comparável. A saída alimenta diretamente os módulos de Economia, Estratégia, Score, Ranking, Alertas e Due Diligence.

| Entrada | Saída |
|---|---|
| Imóvel identificado | Perfil de mercado |
| Comparáveis | Valuation |
| Custos | Custo econômico |
| Estratégia | Preço máximo |
| Risco/confiança | Margem requerida |
| Preço atual | Desconto líquido |
| Mercado | Oportunidade relativa |


# 35. Próximo Documento

Recomendação: Documento 18 — Economia da Operação, Custos, Reforma, Rentabilidade, Margem e Cenários. O foco será aprofundar a matemática econômica depois do valuation: custo total, reforma, carregamento, aluguel, yield, revenda, retorno, sensibilidade e preço máximo.
