# Radar_Imobiliario_Documento_11_Telas_Navegacao_e_Experiencia_do_Investidor_v1.0

🎯
RADAR IMOBILIÁRIO
Documento 11 — Telas, Navegação e Experiência do Investidor
Versão 1.0 | Documento de Negócio

# 1. Objetivo

Definir a experiência funcional do investidor no Radar Imobiliário: telas, navegação, filtros, informações apresentadas, ações disponíveis e caminhos de decisão. O objetivo é tornar a análise rápida para triagem e profunda quando uma oportunidade merece investigação.

# 2. Princípios de UX do Radar

- O usuário deve entender rapidamente por que uma oportunidade apareceu.
- Preço nunca deve aparecer isolado de valuation e custo econômico.
- Score deve vir acompanhado de explicação.
- Risco e confiança devem estar visíveis.
- O sistema deve diferenciar fato, estimativa, cálculo e informação desconhecida.
- A tela deve permitir sair da visão resumida para a evidência original.
- Ações importantes devem ser simples: analisar, monitorar, rejeitar, aprovar e configurar.
- O usuário deve conseguir comparar oportunidades sem abrir dezenas de páginas.
- Alertas devem levar diretamente ao contexto que motivou o alerta.
- A experiência deve respeitar a estratégia ativa do investidor.

# 3. Arquitetura de Navegação Funcional

Navegação principal recomendada:

| Área | Função |
|---|---|
| 🏠 Visão Geral | Resumo do Radar e prioridades. |
| 📡 Radar | Lista principal de oportunidades. |
| ⭐ Minhas Oportunidades | Itens salvos/favoritos. |
| 🔎 Análises | Oportunidades em investigação. |
| 📋 Due Diligence | Pendências e validações. |
| 🔔 Alertas | Eventos que exigem atenção. |
| 📊 Mercado | Comparáveis, aluguel e valuation. |
| 📈 Estratégias | Configuração e performance. |
| ⚙️ Configurações | Parâmetros e regras. |
| 📜 Histórico | Evolução das oportunidades. |
| 📑 Relatórios | Visões consolidadas. |
| 🧪 Backtest | Calibração e aprendizado. |


# 4. Tela 01 — Dashboard / Visão Geral

Objetivo: responder em poucos segundos “o que merece minha atenção hoje?”.

| Componente | Conteúdo |
|---|---|
| Oportunidades novas | Quantidade e principais entradas. |
| Top oportunidades | Melhores scores por estratégia. |
| Mudanças relevantes | Quedas de preço, valuation, riscos. |
| Alertas críticos | Itens que exigem ação. |
| Análises pendentes | Due diligence e pendências. |
| Monitoramento | Teses que mudaram. |
| Indicadores | Oportunidades, margem média, yield, liquidez. |

Ação principal: clicar em uma oportunidade e entrar diretamente na ficha.

# 5. Tela 02 — Radar de Oportunidades

É a tela central do produto.
Filtros recomendados:

| Grupo | Filtros |
|---|---|
| Estratégia | Renda, revenda, valorização, MCMV, terreno etc. |
| Localização | Cidade, bairro, região, prioridade. |
| Tipo | Apartamento, casa, sobrado, terreno, 1 dormitório etc. |
| Preço | Mínimo/máximo. |
| Desconto | Nominal, mercado e líquido. |
| Margem | Mínima desejada. |
| Yield | Mínimo/alvo. |
| Liquidez | Mínima. |
| Score | Faixa. |
| Risco | Máximo aceitável. |
| Confiança | Mínima. |
| Status | Novo, análise, monitoramento, aprovado etc. |
| Fonte | Caixa, leiloeiro, portal etc. |

Ordenações: melhor score, maior margem, maior desconto líquido, maior yield, maior liquidez, maior confiança, mais recente e maior melhoria.

# 6. Card da Oportunidade

O card deve permitir uma decisão preliminar sem abrir a ficha.

| Campo | Exemplo |
|---|---|
| Tipo/local | Apartamento • Portão |
| Preço | R$ 190 mil |
| Mercado base | R$ 260 mil |
| Custo total | R$ 207 mil |
| Desconto líquido | 20,4% |
| Margem | R$ 53 mil |
| Yield | 0,92% a.m. |
| Liquidez | 78/100 |
| Score | 84 |
| Confiança | Alta |
| Risco | Baixo/Médio |
| Estratégia | Renda |
| Motivo | Margem + liquidez + preço abaixo do mercado |

Ações rápidas: ⭐ salvar, 🔍 analisar, 👁 monitorar, ❌ rejeitar, 🔔 criar alerta.

# 7. Tela 03 — Ficha Completa da Oportunidade

A ficha é o centro da decisão. Deve possuir visão resumida no topo e detalhes organizados por abas/blocos.

| Bloco | Objetivo |
|---|---|
| Resumo executivo | Decisão em poucos segundos. |
| Imóvel | Características e identificação. |
| Preço e histórico | Evolução das capturas. |
| Mercado | Comparáveis e valuation. |
| Economia | Custos, margem e cenários. |
| Estratégias | Score e aderência. |
| Riscos | Riscos e severidade. |
| Pendências | O que falta confirmar. |
| Evidências | Fontes/documentos. |
| Due Diligence | Checklist. |
| Timeline | Eventos e decisões. |
| Decisão | BUY / BUY IF / MONITOR etc. |


# 8. Cabeçalho da Ficha

O cabeçalho deve apresentar a síntese:

| Elemento | Informação |
|---|---|
| Classificação | Excepcional / Excelente / Muito boa / Interessante etc. |
| Score | Score da estratégia ativa. |
| Confiança | Nível de confiança. |
| Preço | Preço atual. |
| Valor de mercado | Faixa e valor base. |
| Custo econômico | Estimativa total. |
| Margem | R$ e %. |
| Risco | Nível atual. |
| Status | Estado do workflow. |
| Recomendação | Ação sugerida. |

A recomendação deve ser acompanhada de uma frase explicativa, não apenas de uma cor ou número.

# 9. Tela 04 — Mercado e Comparáveis

Objetivo: permitir que o investidor entenda de onde veio o valuation.

| Elemento | Descrição |
|---|---|
| Comparáveis | Lista de imóveis semelhantes. |
| Distância | Relação geográfica. |
| Preço/m² | Comparação. |
| Área | Comparação. |
| Quartos/vagas | Ajustes. |
| Condição | Novo/usado/reformado. |
| Fonte | Origem da evidência. |
| Data | Atualidade. |
| Qualidade | A–E. |
| Ajustes | Motivo de diferença. |

Deve existir acesso à evidência original sempre que disponível.

# 10. Tela 05 — Economia da Oportunidade

Objetivo: mostrar se a tese permanece boa depois de todos os custos.

| Bloco | Conteúdo |
|---|---|
| Aquisição | Preço/lance + comissão. |
| Tributos/documentos | ITBI, registro, escritura etc. |
| Débitos | Condomínio, IPTU e outros. |
| Reforma | Faixa por cenário. |
| Regularização | Custos estimados. |
| Financeiro | Financiamento/custo de capital. |
| Saída | Custo de venda. |
| Total | Custo econômico total. |
| Mercado | Valor conservador/base/otimista. |
| Resultado | Margem e desconto líquido. |

O usuário deve conseguir alterar premissas em um cenário sem destruir o cenário original.

# 11. Tela 06 — Cenários

Cada oportunidade deve poder ser testada em cenários:

| Cenário | Exemplos |
|---|---|
| Otimista | Preço alto de saída, reforma baixa, venda rápida. |
| Base | Premissas centrais. |
| Conservador | Preço de saída menor, custos maiores. |
| Estressado | Venda lenta, reforma alta, aluguel menor, custos adicionais. |

A pergunta principal: “A tese ainda funciona se as premissas piorarem?”

# 12. Tela 07 — Estratégias

O investidor escolhe uma estratégia ativa ou compara múltiplas estratégias.

| Informação | Exibição |
|---|---|
| Estratégia | Nome e objetivo. |
| Fit | Aderência do imóvel. |
| Score | 0–100. |
| Pontos fortes | Fatores positivos. |
| Pontos fracos | Fatores negativos. |
| Condições | Requisitos para aprovação. |
| Recomendação | Ação por estratégia. |

Exemplo: o mesmo apartamento pode ser “Excelente para Renda” e apenas “Interessante para Revenda”.

# 13. Tela 08 — Explicabilidade

A tela deve responder “por que o Radar chegou a esta conclusão?”.

| Pergunta | Resposta esperada |
|---|---|
| Por que entrou? | Quais regras de entrada foram atendidas. |
| Por que pontuou alto? | Componentes do score. |
| Por que perdeu pontos? | Penalidades e fatores negativos. |
| Qual o risco? | Risco + evidência. |
| Qual a incerteza? | Dados faltantes e confiança. |
| O que precisa confirmar? | Pendências. |
| O que invalidaria? | Condições que derrubariam a tese. |

A explicação deve ser legível para uma pessoa, sem exigir conhecimento técnico.

# 14. Tela 09 — Análise Profunda

Área para registrar a tese e confrontá-la com fatos.

| Seção | Conteúdo |
|---|---|
| Tese | Por que comprar? |
| Argumentos a favor | Evidências positivas. |
| Argumentos contra | Riscos/contrapontos. |
| Mercado | Valuation validado? |
| Economia | Margem validada? |
| Liquidez | Saída plausível? |
| Documentação | O que foi confirmado? |
| Físico | Estado/reforma. |
| Pendências | O que falta. |
| Conclusão | BUY / BUY IF / MONITOR / DO NOT BUY / BLOCK. |


# 15. Tela 10 — Due Diligence

Checklist visual com progresso.

| Grupo | Itens |
|---|---|
| Documental | Matrícula, titularidade, ônus. |
| Jurídico | Processos, restrições, riscos. |
| Financeiro | Condomínio, IPTU, débitos. |
| Posse | Ocupação, desocupação. |
| Venda | Edital/condições/origem. |
| Físico | Visita, reforma, conservação. |
| Mercado | Comparáveis e aluguel. |
| Evidências | Documentos e fontes. |

Cada pendência deve ter responsável, prioridade, prazo, evidência e impacto na decisão.

# 16. Tela 11 — Alertas


| Tipo | Ação ao clicar |
|---|---|
| Nova oportunidade | Abrir ficha. |
| Preço caiu | Abrir histórico + economia. |
| Score aumentou | Abrir fatores da mudança. |
| Valuation mudou | Abrir comparáveis. |
| Risco novo | Abrir risco/evidência. |
| Condição atendida | Abrir condição de compra. |
| Pendência vencida | Abrir due diligence. |
| Status alterado | Abrir timeline. |

Evitar alertas sem ação. Preferir poucos alertas relevantes.

# 17. Tela 12 — Histórico / Timeline

Linha do tempo da oportunidade:
- Captura inicial.
- Alterações de preço.
- Alterações de status.
- Novos comparáveis.
- Alterações de valuation.
- Alterações de score.
- Novos riscos.
- Pendências resolvidas.
- Decisões.
- Reavaliações.
O usuário deve conseguir responder: “como essa oportunidade chegou até aqui?”

# 18. Tela 13 — Configurações do Investidor

Área onde o usuário define seu perfil.

| Grupo | Configurações |
|---|---|
| Capital | Disponível, reserva, entrada. |
| Ticket | Mínimo/máximo. |
| Estratégias | Ativas e prioridades. |
| Localização | Prioritária, aceitável, condicional, bloqueada. |
| Tipos | Aceitos/bloqueados. |
| Desconto | Mínimos e alvos. |
| Margem | Mínima e alvo. |
| Yield | Mínimo e alvo. |
| Liquidez | Mínima. |
| Risco | Máximo. |
| Reforma | Tolerância. |
| Alertas | Eventos e prioridades. |


# 19. Tela 14 — Comparador de Oportunidades

Permitir selecionar 2–5 oportunidades e comparar lado a lado.

| Indicador | Oportunidade A | Oportunidade B | Oportunidade C |
|---|---|---|---|
| Preço | — | — | — |
| Valor mercado | — | — | — |
| Custo total | — | — | — |
| Desconto líquido | — | — | — |
| Margem | — | — | — |
| Yield | — | — | — |
| Liquidez | — | — | — |
| Risco | — | — | — |
| Confiança | — | — | — |
| Score | — | — | — |
| Pendências | — | — | — |
| Estratégia | — | — | — |


# 20. Tela 15 — Rejeitar / Bloquear

A rejeição deve ser rápida, mas estruturada.

| Motivo | Exemplos |
|---|---|
| Preço | Sem margem. |
| Mercado | Valuation insuficiente. |
| Liquidez | Saída ruim. |
| Localização | Fora da estratégia. |
| Risco | Risco elevado. |
| Documentação | Impedimento. |
| Reforma | Custo inviável. |
| Estratégia | Baixo fit. |
| Dados | Confiança insuficiente. |
| Outro | Motivo livre obrigatório. |

Rejeitar não significa apagar. A oportunidade permanece no histórico e pode voltar ao Radar se as condições mudarem.

# 21. Tela 16 — Monitoramento

Mostra oportunidades que o investidor decidiu acompanhar.

| Informação | Ação |
|---|---|
| Motivo do monitoramento | Entender por que está acompanhando. |
| Condição de entrada | Ex.: preço ≤ X. |
| Score atual | Situação. |
| Última atualização | Freshness. |
| Próximo gatilho | O que pode mudar. |
| Alertas | Eventos relevantes. |


# 22. Navegação por Estratégia

O investidor deve poder escolher uma estratégia e ver o Radar reinterpretado.
Exemplo: selecionar “Renda” altera filtros prioritários, score, ranking, explicação e indicadores exibidos; não altera os dados fundamentais do imóvel.

# 23. Fluxo Principal do Usuário

1. Abre o Dashboard.
2. Vê novas oportunidades e alertas.
3. Entra no Radar.
4. Escolhe estratégia.
5. Filtra região/ticket/tipo.
6. Compara cards.
7. Abre uma oportunidade.
8. Entende preço, valuation, custo e score.
9. Consulta explicabilidade.
10. Verifica riscos e pendências.
11. Abre análise profunda.
12. Executa due diligence.
13. Decide BUY / BUY IF / MONITOR / DO NOT BUY / BLOCK.
14. Mantém monitoramento.
15. Recebe alertas de mudanças.

# 24. Princípios de Interface para Decisão

- Não esconder risco em telas secundárias.
- Não mostrar desconto sem mostrar base de comparação.
- Não mostrar valuation sem confiança.
- Não mostrar score sem explicar composição.
- Não misturar fato com estimativa sem identificação.
- Não exigir que o investidor calcule manualmente o custo total.
- Não exigir abertura de várias telas para entender a tese.
- Permitir aprofundamento progressivo: resumo → detalhe → evidência.
- Manter ações de decisão sempre disponíveis.
- Preservar contexto da estratégia selecionada.

# 25. Critérios de Aceite de UX

- O usuário consegue identificar as melhores oportunidades em uma única visão.
- É possível filtrar por localização, estratégia, tipo, preço, desconto, margem, yield, liquidez, risco e confiança.
- Cada oportunidade mostra preço, valuation, custo total, margem, score e risco.
- O usuário consegue entender por que uma oportunidade foi classificada.
- É possível comparar oportunidades.
- É possível salvar, rejeitar e monitorar.
- É possível iniciar análise profunda a partir do Radar.
- Due diligence mostra claramente pendências e impacto.
- Alertas levam diretamente ao motivo do alerta.
- Histórico permite entender a evolução da oportunidade.
- Configurações alteram o comportamento futuro sem apagar o histórico.

# 26. MVP de Experiência


| Prioridade | Telas |
|---|---|
| P0 | Dashboard |
| P0 | Radar |
| P0 | Ficha da oportunidade |
| P0 | Economia |
| P0 | Valuation/mercado |
| P0 | Estratégia + score |
| P0 | Explicabilidade |
| P0 | Análise |
| P0 | Due Diligence |
| P0 | Decisão |
| P1 | Alertas |
| P1 | Histórico |
| P1 | Comparador |
| P1 | Configurações avançadas |
| P2 | Relatórios avançados |
| P2 | Backtest visual |


# 27. O que este Documento Fecha

Com este documento, o Radar passa a ter uma definição funcional de como o investidor navega, descobre, compara, investiga, decide e acompanha oportunidades. A experiência foi desenhada para refletir as regras e conceitos dos Documentos 0–10.

# 28. Próximo Documento Recomendado

Documento 12 — Matriz Completa de Requisitos, Regras, Casos de Uso e Critérios de Aceite. O objetivo será consolidar tudo em uma matriz rastreável, ligando requisito → módulo → regra → parâmetro → tela → evento → saída → critério de aceite. Essa matriz será a base definitiva para implementação posterior.
