# Radar_Imobiliario_Documento_22_Ranking_Priorizacao_Comparacao_Motor_Decisao_v1.0

🏠 RADAR IMOBILIÁRIO
Documento 22
Ranking, Priorização, Comparação e Motor de Decisão
Especificação Funcional de Negócio | Versão 1.0

# 1. Objetivo

Definir como o Radar transforma dados, valuation, economia, liquidez, risco, estratégia, perfil do investidor e confiança em uma ordem inteligente de prioridade.
- O que deve aparecer primeiro.
- Por que uma oportunidade está acima de outra.
- Quais fatores elevaram ou reduziram a posição.
- Quais oportunidades competem pelo mesmo capital.
- Quando o ranking deve ser recalculado.
- Como bloquear oportunidades sem depender do score.
- Como explicar a decisão de forma auditável.

# 2. Princípio Central

O ranking não procura simplesmente o imóvel mais barato nem o maior desconto. Ele procura a oportunidade que apresenta a melhor combinação entre retorno potencial, segurança, liquidez, aderência ao investidor, eficiência de capital e confiança dos dados.

| Não é | É |
|---|---|
| Maior desconto | Melhor oportunidade ajustada |
| Menor preço | Melhor relação valor/custo |
| Maior score isolado | Score + regras + confiança + contexto |
| Lista estática | Fila dinâmica |
| Decisão automática cega | Decisão explicável e auditável |


# 3. Hierarquia de Decisão


| Ordem | Camada | Função |
|---|---|---|
| 1 | Bloqueios | Elimina impedimentos críticos. |
| 2 | Elegibilidade | Verifica se pode participar. |
| 3 | Qualidade dos dados | Determina confiança. |
| 4 | Economia | Avalia custo, margem e retorno. |
| 5 | Estratégia | Verifica aderência. |
| 6 | Risco | Ajusta exigência. |
| 7 | Liquidez | Avalia saída/renda. |
| 8 | Score | Prioriza. |
| 9 | Capital | Avalia capacidade de execução. |
| 10 | Ranking | Ordena oportunidades. |

Uma camada superior não pode ser anulada por uma inferior. Em especial: score não supera BLOCK.

# 4. Conceitos de Ranking


| Conceito | Definição |
|---|---|
| Score | Nota de qualidade da oportunidade. |
| Fit | Aderência ao investidor. |
| Confiança | Qualidade das evidências. |
| Prioridade | Urgência/importância de análise. |
| Ranking | Ordem relativa entre oportunidades. |
| Status | Estado operacional da oportunidade. |
| Competição de capital | Conjunto de oportunidades que disputam os mesmos recursos. |


# 5. Opportunity Score


| Componente | Peso ilustrativo |
|---|---|
| Desconto líquido | 25% |
| Margem de segurança | 20% |
| Liquidez | 15% |
| Localização | 15% |
| Risco | 10% |
| Yield | 5% |
| Valorização | 5% |
| Qualidade da oportunidade | 5% |

Os pesos são exemplos e devem ser parametrizáveis por estratégia.

# 6. Investor Fit Score


| Componente | Pergunta |
|---|---|
| Estratégia | A oportunidade atende ao objetivo? |
| Capital | Cabe no orçamento? |
| Liquidez | É compatível com a necessidade de saída? |
| Risco | Está dentro da tolerância? |
| Concentração | Melhora ou piora o portfólio? |
| Horizonte | O prazo é compatível? |
| Esforço | A operação cabe na capacidade operacional? |


# 7. Confiança

A mesma oportunidade pode ter score alto com dados fracos. Por isso, confiança deve atuar como fator de prudência.

| Confiança | Fator ilustrativo |
|---|---|
| Muito alta | 1,00 |
| Alta | 0,95 |
| Média | 0,88 |
| Baixa | 0,75 |
| Muito baixa | 0,60 |
| Inconclusiva | Não recomendar |

Esses fatores são ilustrativos e devem ser calibrados com dados históricos.

# 8. Score Composto

Modelo conceitual:
Score de Prioridade = Opportunity Score × Investor Fit × Confiança × Ajuste de Capital × Ajuste de Portfólio
Os ajustes podem ser normalizados para evitar distorções. O score não elimina regras de bloqueio.

# 9. Ajuste de Capital


| Situação | Efeito |
|---|---|
| Capital amplamente disponível | Sem penalização relevante. |
| Capital limitado | Priorizar eficiência de capital. |
| Capital quase comprometido | Priorizar oportunidades excepcionais. |
| Reserva ameaçada | Bloquear. |
| Custo total excede limite | Bloquear ou exigir exceção. |


# 10. Ajuste de Portfólio

- Bônus para diversificação desejada.
- Penalização para concentração excessiva.
- Penalização para duplicação de risco.
- Bônus para equilíbrio de estratégias.
- Penalização para excesso de capital imobilizado.
- Ajuste conforme objetivos atuais do investidor.

# 11. Ranking Absoluto x Ranking Relativo


| Tipo | Uso |
|---|---|
| Absoluto | Compara oportunidade com critérios mínimos. |
| Relativo | Compara oportunidades entre si. |
| Estratégico | Compara dentro de uma estratégia. |
| Portfólio | Compara considerando capital já investido. |
| Temporal | Compara prioridade no momento atual. |

Uma oportunidade pode ter score absoluto alto, mas perder posição para outra oportunidade ainda melhor.

# 12. Ranking por Estratégia


| Estratégia | Prioridade típica |
|---|---|
| Renda | Yield + liquidez + risco + estabilidade |
| Revenda | Desconto + margem + prazo + liquidez |
| Valorização | Potencial + localização + horizonte |
| MCMV | Demanda + financiamento + ticket + liquidez |
| Terreno | Preço + potencial + demanda + prazo |
| Oportunidade especial | Margem excepcional + risco controlável |


# 13. Ranking por Perfil de Imóvel

- Apartamento: condomínio, preço/m², liquidez, aluguel.
- 1 dormitório: demanda específica, localização e ticket.
- Casa/sobrado: terreno, conservação, família, ticket.
- Terreno: zoneamento, potencial, infraestrutura e saída.
- MCMV: financiamento, demanda e capacidade de pagamento.

# 14. Comparação Lado a Lado


| Fator | A | B | C |
|---|---|---|---|
| Opportunity Score | 91 | 84 | 88 |
| Fit | 72 | 95 | 86 |
| Confiança | 95% | 90% | 98% |
| Liquidez | 60 | 90 | 78 |
| Capital | R$ 250k | R$ 150k | R$ 190k |
| Prioridade | 2 | 1 | 3 |

A maior nota econômica não precisa ser a primeira colocada quando aderência, liquidez ou capital tornam outra oportunidade superior.

# 15. Explicabilidade do Ranking

Toda posição deve ser explicável em linguagem de negócio.

| Pergunta | Exemplo de resposta |
|---|---|
| Por que está alta? | Margem alta, boa liquidez e forte aderência. |
| Por que não está em 1º? | Capital elevado e concentração regional. |
| O que faria subir? | Redução do preço em R$ 15 mil. |
| O que faria cair? | Nova pendência jurídica. |
| Qual é o risco principal? | Prazo de saída. |
| Qual condição falta? | Confirmar custo de reforma. |


# 16. Ranking Dinâmico

O ranking deve mudar quando ocorrer evento material.
- Preço mudou.
- Valuation mudou.
- Novo comparável surgiu.
- Liquidez mudou.
- Aluguel mudou.
- Risco surgiu ou foi resolvido.
- Pendência foi resolvida.
- Estratégia do investidor mudou.
- Capital disponível mudou.
- Outra oportunidade foi adquirida.

# 17. Gatilhos de Reclassificação


| Evento | Ação |
|---|---|
| Preço - material | Recalcular economia e ranking |
| Preço + material | Recalcular |
| Valuation mudou | Recalcular |
| Novo risco crítico | BLOCK |
| Liquidez caiu | Recalcular |
| Score cruzou faixa | Gerar alerta |
| Capital ficou indisponível | Recalcular |
| Estratégia mudou | Reprocessar aderência |
| Nova oportunidade excepcional | Comparar carteira |


# 18. Ranking por Urgência


| Prioridade | Situação |
|---|---|
| P0 | Janela curta / evento crítico / oportunidade excepcional |
| P1 | Excelente e pronta para análise |
| P2 | Muito boa, sem urgência |
| P3 | Interessante, requer enriquecimento |
| P4 | Monitoramento |
| BLOCK | Não elegível ou risco crítico |


# 19. Urgência x Atratividade

Atratividade e urgência são dimensões diferentes.

| Atratividade | Urgência | Tratamento |
|---|---|---|
| Alta | Alta | Analisar imediatamente |
| Alta | Baixa | Priorizar |
| Baixa | Alta | Investigar motivo da urgência |
| Baixa | Baixa | Monitorar/ignorar |


# 20. Competição pelo Mesmo Capital

O Radar deve identificar quando várias oportunidades competem pelo mesmo orçamento.

| Capital | Oportunidade A | Oportunidade B |
|---|---|---|
| Necessário | R$ 200k | R$ 180k |
| Retorno | Alto | Muito alto |
| Risco | Médio | Baixo |
| Liquidez | Média | Alta |
| Fit | 80 | 94 |
| Escolha | — | Prioridade |


# 21. Fronteira de Oportunidades

Quando existem muitas oportunidades, o Radar deve destacar aquelas que oferecem combinações não dominadas de retorno, risco, liquidez e capital.
- Mais retorno com risco semelhante.
- Mesmo retorno com menor capital.
- Mesmo capital com maior liquidez.
- Menor risco com retorno equivalente.
Essas oportunidades formam um conjunto prioritário para análise.

# 22. Score x Confiança


| Score | Confiança | Interpretação |
|---|---|---|
| 95 | 95% | Prioridade máxima |
| 95 | 60% | Grande potencial, mas precisa evidência |
| 75 | 98% | Boa oportunidade comprovada |
| 75 | 60% | Baixa prioridade |
| 55 | 98% | Fraca, mesmo com boa evidência |
| 95 | Inconclusiva | Não recomendar |


# 23. Score x Liquidez


| Score | Liquidez | Tratamento |
|---|---|---|
| Alto | Alta | Excelente candidata |
| Alto | Média | Análise aprofundada |
| Alto | Baixa | Exigir margem |
| Médio | Alta | Pode superar oportunidade mais arriscada |
| Baixo | Alta | Não basta liquidez |
| Qualquer | Muito baixa | Somente tese excepcional |


# 24. Score x Capital

O ranking deve privilegiar eficiência quando o capital é escasso.

| Oportunidade | Capital | Score | Eficiência ilustrativa |
|---|---|---|---|
| A | R$ 100k | 80 | Alta |
| B | R$ 250k | 90 | Média |
| C | R$ 150k | 88 | Alta |

B pode ser melhor em score absoluto, mas A ou C podem gerar melhor uso do capital disponível.

# 25. Ranking por Janela de Decisão


| Janela | Objetivo |
|---|---|
| Agora | Oportunidades prontas para decisão. |
| Próximos dias | Oportunidades com DD em andamento. |
| Próximas semanas | Monitoramento ativo. |
| Longo prazo | Teses de valorização. |


# 26. Regras de Desempate

- Maior aderência à estratégia.
- Maior confiança.
- Maior margem de segurança.
- Maior liquidez.
- Menor risco.
- Menor capital necessário.
- Melhor diversificação.
- Maior urgência, quando aplicável.
A ordem deve ser parametrizável por estratégia.

# 27. Decisão sobre o Ranking


| Posição | Ação |
|---|---|
| Top 1–3 | Análise prioritária |
| Top 4–10 | Fila ativa |
| Top 11–30 | Monitoramento qualificado |
| Demais | Monitoramento passivo/arquivamento |
| BLOCK | Fora do ranking operacional |


# 28. Ranking e Workflow

O ranking não substitui o workflow. Ele orienta onde investir atenção.
CAPTURADO → QUALIFICADO → VALUADO → SCORE → RANKING → ANÁLISE → DD → DECISÃO
- Uma oportunidade pode subir sem estar pronta para compra.
- Uma oportunidade no topo pode ficar PENDENTE.
- Uma oportunidade aprovada sai da fila de descoberta e entra no ciclo de aquisição.
- Uma oportunidade rejeitada pode retornar se os fatos mudarem.

# 29. Ranking e Alertas


| Mudança | Alerta |
|---|---|
| Entrou no Top 10 | Nova oportunidade prioritária |
| Subiu 20 posições | Melhora material |
| Caiu 20 posições | Deterioração material |
| Virou Top 3 | Ação recomendada |
| Saiu do Top 10 | Reavaliar atenção |
| Virou BLOCK | Alerta crítico |


# 30. Ranking e Explainability

Cada posição deve possuir um resumo executivo:
- Classificação atual.
- Score.
- Fit.
- Confiança.
- Principal vantagem.
- Principal risco.
- Principal pendência.
- Condição para subir.
- Condição para cair.
- Ação recomendada.

# 31. Reprocessamento

Sempre que um dado material mudar, o Radar deve reprocessar apenas as camadas afetadas e refletir a mudança no ranking.

| Mudança | Camadas |
|---|---|
| Preço | Economia → Score → Ranking |
| Valuation | Economia → Score → Ranking |
| Risco | Risco → Score → Ranking |
| Estratégia | Fit → Score → Ranking |
| Capital | Portfólio → Fit/Capital → Ranking |
| Liquidez | Saída → Score → Ranking |


# 32. Auditoria do Ranking

- Versão dos pesos.
- Versão das regras.
- Dados usados.
- Timestamp da classificação.
- Score anterior e atual.
- Motivo da mudança.
- Exceções aplicadas.
- Decisão humana, quando houver.

# 33. Cenário Completo

Uma oportunidade capturada por R$ 190 mil possui valuation base de R$ 300 mil. Após custos, seu custo econômico é R$ 220 mil. Possui desconto líquido de 26,7%, liquidez 72, risco médio e confiança 91%. O Opportunity Score é 84 e o Fit do investidor é 94. Outra oportunidade possui score 90, mas Fit 65, liquidez 50 e exige R$ 280 mil. O motor deve colocar a primeira acima da segunda.

| Dimensão | Opção A | Opção B |
|---|---|---|
| Opportunity Score | 84 | 90 |
| Fit | 94 | 65 |
| Confiança | 91% | 88% |
| Liquidez | 72 | 50 |
| Capital | R$ 220k | R$ 280k |
| Resultado | Prioridade 1 | Prioridade 2 |


# 34. Regras de Negócio


| ID | Regra | Resultado |
|---|---|---|
| RANK22-001 | BLOCK elimina do ranking operacional | Não priorizar |
| RANK22-002 | Score não supera bloqueio | Manter BLOCK |
| RANK22-003 | Fit abaixo do mínimo | Reduzir/DO NOT BUY |
| RANK22-004 | Confiança insuficiente | Reduzir prioridade |
| RANK22-005 | Capital indisponível | BLOCK operacional |
| RANK22-006 | Nova informação material | Recalcular |
| RANK22-007 | Nova oportunidade excepcional | Recomparar |
| RANK22-008 | Concentração excessiva | Penalizar prioridade |
| RANK22-009 | Liquidez baixa | Exigir margem adicional |
| RANK22-010 | Ranking deve ser explicável | Obrigatório |
| RANK22-011 | Pesos devem possuir versão | Obrigatório |
| RANK22-012 | Empates seguem critérios configurados | Desempatar |


# 35. Critérios de Aceite

- CA-D22 — O ranking diferencia qualidade da oportunidade e aderência ao investidor.
- CA-D22 — Bloqueios removem oportunidades do ranking operacional.
- CA-D22 — Score não supera regras críticas.
- CA-D22 — Confiança influencia prioridade.
- CA-D22 — Capital disponível influencia prioridade.
- CA-D22 — Concentração influencia prioridade.
- CA-D22 — Liquidez influencia prioridade.
- CA-D22 — O ranking pode ser segmentado por estratégia.
- CA-D22 — O ranking pode ser absoluto ou relativo.
- CA-D22 — O usuário consegue comparar oportunidades lado a lado.
- CA-D22 — Cada posição possui explicação.
- CA-D22 — Existem gatilhos de reclassificação.
- CA-D22 — Eventos materiais recalculam o ranking.
- CA-D22 — O ranking possui histórico.
- CA-D22 — Pesos e regras possuem versão.
- CA-D22 — É possível identificar oportunidades que competem pelo mesmo capital.
- CA-D22 — O Radar destaca oportunidades não dominadas.
- CA-D22 — Existe separação entre atratividade e urgência.
- CA-D22 — O ranking orienta atenção sem substituir a Due Diligence.
- CA-D22 — A decisão final continua auditável.

# 36. Relação com os Documentos


| Documento | Relação |
|---|---|
| 15 — Decisão | Fornece matriz e precedência. |
| 17 — Valuation | Fornece valor e preço máximo. |
| 18 — Economia | Fornece margem e retorno. |
| 19 — Risco | Fornece risco e mitigação. |
| 20 — Liquidez | Fornece demanda e saída. |
| 21 — Investidor | Fornece Fit, capital e portfólio. |
| 8 — Parâmetros | Fornece pesos e limites. |
| 7 — Workflow | Recebe eventos e mudanças. |
| 12 — Traceabilidade | Mantém vínculo entre regras e decisão. |


# 37. Próximo Documento

Recomendação: Documento 23 — Monitoramento, Reavaliação, Alertas Inteligentes e Aprendizado Contínuo. O foco será fazer o Radar continuar trabalhando depois da primeira análise: detectar mudanças, reavaliar oportunidades, alertar somente o que importa e aprender com decisões e resultados reais.
