# Radar_Imobiliario_Documento_25_Arquitetura_Funcional_Mapa_Consolidado_Produto_v1.0

🏠 RADAR IMOBILIÁRIO
Documento 25
Arquitetura Funcional do Produto e Mapa Consolidado de Módulos, Fluxos e Capacidades
Visão Consolidada de Negócio | Versão 1.0

# 1. Objetivo

Consolidar os 24 documentos anteriores em uma visão única do produto, mostrando como módulos, dados, regras, decisões, pessoas, estados e ciclos se conectam. Este documento continua sendo funcional: não define tecnologia, infraestrutura, banco de dados ou arquitetura técnica.
- Mostrar o Radar de ponta a ponta.
- Consolidar capacidades do produto.
- Eliminar ambiguidades entre módulos.
- Definir entradas e saídas de cada macrocapacidade.
- Mostrar dependências de negócio.
- Estabelecer o mapa funcional que servirá de referência para as próximas especificações.

# 2. O que é o Radar

O Radar é um sistema de inteligência de oportunidades imobiliárias. Ele transforma múltiplas fontes e informações fragmentadas em oportunidades analisadas, ranqueadas, explicáveis e acompanhadas ao longo do tempo.
Não é um simples catálogo de imóveis, um portal de anúncios ou um sistema exclusivamente de leilões.

| Camada | Pergunta |
|---|---|
| Descoberta | O que apareceu? |
| Identificação | É o mesmo imóvel? |
| Qualificação | Pode ser uma oportunidade? |
| Mercado | Quanto vale? |
| Economia | Quanto realmente custa? |
| Estratégia | Para que serve? |
| Risco | O que pode dar errado? |
| Liquidez | Como sai/aluga? |
| Score | Quão boa é? |
| Fit | É boa para este investidor? |
| Ranking | Qual merece atenção primeiro? |
| Due Diligence | É realmente viável? |
| Decisão | Comprar, condicionar, monitorar ou rejeitar? |
| Monitoramento | O que mudou? |
| Aprendizado | O que aprendemos? |


# 3. Princípios Mestres

- Preço é o dado. Oportunidade é a análise.
- Não procure imóveis baratos. Deixe o Radar encontrar imóveis realmente baratos.
- Desconto não é lucro.
- Score não supera BLOCK.
- Desconhecido não significa seguro.
- Imóvel é permanente; oportunidade é dinâmica.
- Muitos registros podem representar um único imóvel.
- Uma oportunidade pode ser boa para uma estratégia e ruim para outra.
- Liquidez é parte do valor econômico.
- Capital e tempo também têm custo.
- Todo resultado relevante precisa ser explicável.
- Histórico nunca deve ser apagado.
- Aprendizado deve melhorar decisões sem destruir governança.

# 4. Mapa Funcional de Alto Nível

FONTES → CAPTURA → NORMALIZAÇÃO → IDENTIFICAÇÃO → DEDUPLICAÇÃO → CONSOLIDAÇÃO → QUALIFICAÇÃO → ENRIQUECIMENTO → VALUATION → ECONOMIA → RISCO → LIQUIDEZ → ESTRATÉGIAS → REGRAS → SCORE → FIT → RANKING → ANÁLISE → DUE DILIGENCE → DECISÃO → MONITORAMENTO → RESULTADO → APRENDIZADO
Esse fluxo é conceitual e pode possuir ciclos, retornos e reprocessamentos.

# 5. Macrocapacidades


| ID | Capacidade | Objetivo |
|---|---|---|
| CAP-01 | Fontes | Conhecer origens de informação. |
| CAP-02 | Captura | Preservar o que a fonte informou. |
| CAP-03 | Identificação | Reconhecer o imóvel. |
| CAP-04 | Deduplicação | Consolidar múltiplas referências. |
| CAP-05 | Perfil | Formar visão consolidada. |
| CAP-06 | Mercado | Entender contexto local. |
| CAP-07 | Comparáveis | Obter evidências de preço. |
| CAP-08 | Valuation | Estimar valor. |
| CAP-09 | Economia | Calcular custo e retorno. |
| CAP-10 | Risco | Avaliar ameaças. |
| CAP-11 | Liquidez | Avaliar demanda e saída. |
| CAP-12 | Estratégias | Definir objetivos. |
| CAP-13 | Regras | Aplicar critérios. |
| CAP-14 | Score | Medir qualidade. |
| CAP-15 | Fit | Medir aderência. |
| CAP-16 | Ranking | Priorizar. |
| CAP-17 | Análise | Investigar oportunidade. |
| CAP-18 | Due Diligence | Validar realidade. |
| CAP-19 | Decisão | Registrar resultado. |
| CAP-20 | Monitoramento | Acompanhar mudanças. |
| CAP-21 | Alertas | Chamar atenção para eventos. |
| CAP-22 | Histórico | Preservar evolução. |
| CAP-23 | Backtest | Validar regras. |
| CAP-24 | Governança | Controlar mudanças. |
| CAP-25 | Aprendizado | Transformar resultado em conhecimento. |


# 6. Módulos Funcionais Consolidados


| Módulo | Entrada principal | Saída principal |
|---|---|---|
| Fontes | Origem externa/manual | Fonte cadastrada |
| Captura | Conteúdo da fonte | Snapshot |
| Normalização | Dados brutos | Dados padronizados |
| Identificação | Atributos do imóvel | Identidade |
| Deduplicação | Registros candidatos | Relação/consolidação |
| Perfil | Dados consolidados | Perfil do imóvel |
| Localização | Endereço/geografia | Contexto local |
| Mercado | Dados locais | Submercado |
| Comparáveis | Imóveis semelhantes | Evidências |
| Valuation | Comparáveis + contexto | Valor estimado |
| Economia | Preço + custos | Resultado econômico |
| Risco | Fatos + evidências | Matriz de risco |
| Liquidez | Demanda + oferta | Score de liquidez |
| Estratégia | Objetivo do investidor | Critérios |
| Regras | Parâmetros | Elegibilidade |
| Score | Indicadores | Opportunity Score |
| Fit | Investidor + oportunidade | Investor Fit |
| Ranking | Scores + contexto | Prioridade |
| Análise | Oportunidade | Tese |
| DD | Tese + evidências | Validação |
| Decisão | Resultado da DD | BUY/BUY IF/MONITOR/etc. |
| Monitoramento | Eventos | Reavaliação |
| Alertas | Mudanças | Ação |
| Histórico | Eventos | Linha do tempo |
| Backtest | Histórico | Calibração |
| Governança | Mudanças | Versões/auditoria |
| Aprendizado | Resultados | Conhecimento |


# 7. Entidades de Negócio


| Entidade | Papel |
|---|---|
| Fonte | Origem |
| Captura | Snapshot |
| Imóvel | Ativo físico/documental |
| Oportunidade | Tese econômica |
| Perfil | Características consolidadas |
| Localização | Contexto geográfico |
| Comparável | Evidência de mercado |
| Valuation | Estimativa de valor |
| Custo | Componente econômico |
| Cenário | Premissas |
| Estratégia | Objetivo |
| Regra | Critério |
| Parâmetro | Valor configurável |
| Score | Prioridade |
| Risco | Ameaça |
| Evidência | Suporte |
| Pendência | Questão não resolvida |
| Análise | Avaliação temporal |
| Due Diligence | Validação profunda |
| Decisão | Resultado |
| Alerta | Evento de atenção |
| Histórico | Evolução |


# 8. Relações Fundamentais

FONTE → CAPTURA → IMÓVEL → OPORTUNIDADE
OPORTUNIDADE → PERFIL + LOCALIZAÇÃO + COMPARÁVEIS + VALUATION + CUSTOS + RISCOS + LIQUIDEZ + ESTRATÉGIAS + SCORE + FIT
OPORTUNIDADE → ANÁLISE → DUE DILIGENCE → DECISÃO
OPORTUNIDADE → MONITORAMENTO → HISTÓRICO → APRENDIZADO

# 9. Separação Fundamental: Imóvel x Oportunidade


| Imóvel | Oportunidade |
|---|---|
| Existe independentemente do Radar | Surge a partir de uma tese |
| Identidade relativamente estável | Pode mudar |
| Tem matrícula/endereço/características | Tem preço, estratégia, score |
| Pode aparecer em várias fontes | Pode existir em vários momentos |
| Histórico próprio | Histórico de análises/decisões |


# 10. Jornada Completa do Investidor

- Configurar perfil e estratégias.
- Definir capital e limites.
- Receber/consultar oportunidades.
- Filtrar e qualificar.
- Visualizar valuation e economia.
- Entender risco e liquidez.
- Comparar e ranquear.
- Abrir análise profunda.
- Executar Due Diligence.
- Tomar decisão.
- Registrar aquisição/rejeição.
- Monitorar.
- Comparar previsto x realizado.
- Alimentar aprendizado.

# 11. Jornada da Oportunidade

CAPTURADA → NORMALIZADA → IDENTIFICADA → CONSOLIDADA → QUALIFICADA → ENRIQUECIDA → VALUADA → ECONÔMICA → RANQUEADA → EM ANÁLISE → DD → APROVADA / BUY IF / MONITOR / REJEITADA / BLOCK → ADQUIRIDA → RESULTADO → APRENDIZADO

# 12. Estados Principais


| Estado | Significado |
|---|---|
| Captured | Foi encontrada. |
| Normalized | Dados padronizados. |
| Qualified | Passou elegibilidade. |
| Enriched | Recebeu informações adicionais. |
| Valuated | Possui valuation. |
| Scored | Possui score. |
| Ranked | Está priorizada. |
| In Analysis | Análise profunda. |
| Pending | Há pendências. |
| Monitoring | Tese viva sem decisão final. |
| Approved | Aprovada. |
| Conditional Purchase | Aprovada sob condição. |
| Rejected | Rejeitada. |
| Blocked | Impedimento crítico. |
| Acquired | Adquirida. |
| Closed | Ciclo encerrado. |


# 13. Camadas de Decisão


| Camada | Pergunta | Pode bloquear? |
|---|---|---|
| Bloqueio | Existe impedimento crítico? | Sim |
| Elegibilidade | Atende critérios mínimos? | Sim |
| Dados | Há confiança suficiente? | Pode impedir recomendação |
| Economia | Existe margem? | Sim, por regra |
| Risco | Risco aceitável? | Sim |
| Estratégia | É aderente? | Sim |
| Liquidez | Existe saída/renda? | Pode impedir |
| Score | Quão boa é? | Não supera bloqueios |
| Fit | Serve ao investidor? | Pode reduzir prioridade |
| Ranking | Qual vem primeiro? | Não |


# 14. Motor Econômico

VALOR DE MERCADO → CUSTO ECONÔMICO TOTAL → DESCONTO LÍQUIDO → MARGEM → RETORNO → PREÇO MÁXIMO → CENÁRIOS
- Compra.
- Custos de aquisição.
- Dívidas/responsabilidades quando aplicáveis.
- Regularização.
- Reforma.
- Carregamento.
- Financiamento.
- Saída.
- Contingência.

# 15. Motor de Risco

RISCO = PROBABILIDADE × IMPACTO × EXPOSIÇÃO × INCERTEZA, considerando mitigação e tempo.
- Jurídico.
- Matrícula.
- Ocupação.
- Débitos.
- Físico.
- Mercado.
- Liquidez.
- Execução.
Risco crítico confirmado → BLOCK. Risco crítico desconhecido → PENDENTE/BLOCK conforme regra.

# 16. Motor de Liquidez

DEMANDA → OFERTA → CONCORRÊNCIA → PREÇO → PRAZO → LIQUIDEZ → CUSTO DO TEMPO → SAÍDA
- Venda.
- Locação.
- Ticket.
- Financiabilidade.
- Público-alvo.
- Absorção.
- Preço de venda rápida.

# 17. Motor de Estratégia


| Estratégia | Principal objetivo |
|---|---|
| Renda | Maximizar renda ajustada ao risco. |
| Revenda | Maximizar margem e velocidade. |
| Valorização | Maximizar valorização ajustada. |
| MCMV | Capturar demanda e eficiência do segmento. |
| Terreno | Explorar preço/potencial/saída. |
| Híbrida | Combinar renda, valorização e saída. |


# 18. Motor de Score

Opportunity Score mede a qualidade da oportunidade.
Investor Fit Score mede a aderência ao investidor.
Confiança mede a força das evidências.
Score Final/Ranking combina essas dimensões sem eliminar precedência das regras.

# 19. Motor de Ranking

RANKING = QUALIDADE + FIT + CONFIANÇA + CAPITAL + PORTFÓLIO + URGÊNCIA
- Ranking absoluto.
- Ranking relativo.
- Ranking por estratégia.
- Ranking por capital.
- Ranking por urgência.
- Comparação entre oportunidades concorrentes.

# 20. Motor de Due Diligence


| Área | Validação |
|---|---|
| Identidade | Matrícula/registro |
| Titularidade | Propriedade |
| Ocupação | Posse/ocupante |
| Condomínio | Débitos/regras |
| Tributos | IPTU |
| Jurídico | Processos |
| Fonte | Condições de venda |
| Físico | Estado/reforma |
| Mercado | Comparáveis |
| Renda | Aluguel |
| Economia | Cenários |
| Decisão | BUY/BUY IF/MONITOR/etc. |


# 21. Monitoramento

A oportunidade não termina na análise.

| Mudança | Reação |
|---|---|
| Preço | Recalcular economia |
| Valuation | Recalcular margem |
| Risco | Reavaliar DD |
| Liquidez | Recalcular saída |
| Aluguel | Recalcular renda |
| Capital | Recalcular Fit |
| Estratégia | Recalcular aderência |
| Concorrência | Reavaliar mercado |


# 22. Alertas


| Tipo | Exemplo |
|---|---|
| Oportunidade | Preço caiu e entrou no Top 3. |
| Risco | Novo risco crítico. |
| Economia | Margem caiu abaixo do mínimo. |
| Liquidez | Prazo estimado aumentou. |
| Estratégia | Oportunidade deixou de ser aderente. |
| Capital | Reserva ficou abaixo do mínimo. |
| Governança | Regra relevante alterada. |
| Aprendizado | Regra apresenta alto falso positivo. |


# 23. Governança e Auditoria

Toda decisão relevante deve ser reconstruível.
- Dados utilizados.
- Fontes.
- Evidências.
- Regras.
- Parâmetros.
- Pesos.
- Score.
- Fit.
- Exceções.
- Justificativa.
- Data/hora.

# 24. Ciclo de Aprendizado

PREVISÃO → DECISÃO → RESULTADO REAL → ERRO/ACERTO → BACKTEST → CALIBRAÇÃO → NOVA VERSÃO
O aprendizado deve melhorar a qualidade sem permitir que informações futuras contaminem decisões passadas.

# 25. Mapa de Dependências


| Capacidade | Depende principalmente de |
|---|---|
| Valuation | Perfil + mercado + comparáveis |
| Economia | Valuation + custos |
| Risco | Dados + evidências |
| Liquidez | Mercado + demanda |
| Estratégia | Investidor |
| Score | Economia + risco + liquidez + localização |
| Fit | Investidor + oportunidade |
| Ranking | Score + Fit + confiança + capital |
| DD | Oportunidade + riscos + pendências |
| Decisão | DD + economia + estratégia |
| Monitoramento | Histórico + eventos |
| Aprendizado | Resultados + histórico + decisões |


# 26. Matriz de Capacidades x Documentos


| Tema | Documentos principais |
|---|---|
| Regras | 1, 3, 8, 15 |
| Valuation | 2, 17 |
| Economia | 18 |
| Risco/DD | 4, 19 |
| Liquidez | 20 |
| Investidor | 21 |
| Ranking | 22 |
| Monitoramento | 23 |
| Governança | 24 |
| Produto/Módulos | 5, 9, 10, 11, 12, 13, 16 |
| Dados | 6, 14 |
| Fluxo | 7 |
| Consolidação | 25 |


# 27. Capacidade de Expansão

O produto deve conseguir adicionar novas fontes, bancos, leiloeiros, tipos de imóvel e estratégias sem reconstruir a lógica central.
- Nova fonte → nova captura.
- Novo tipo → nova parametrização.
- Nova estratégia → novo perfil de regras.
- Novo mercado → novos parâmetros de contexto.
- Nova evidência → novo enriquecimento.
- Nova regra → nova versão.

# 28. O que NÃO faz parte desta Arquitetura Funcional

- Tecnologia específica.
- Cloud/provedor.
- Banco de dados físico.
- Linguagem de programação.
- Framework.
- APIs técnicas.
- Filas/mensageria.
- Infraestrutura.
Esses assuntos podem ser tratados posteriormente, depois de estabilizada a visão funcional.

# 29. MVP Funcional Consolidado

O MVP precisa provar o ciclo completo, não apenas disponibilizar uma tela de imóveis.

| Obrigatório | Resultado |
|---|---|
| Fonte/Captura | Oportunidade real capturada |
| Identificação | Imóvel consolidado |
| Valuation | Valor de mercado |
| Economia | Custo e margem |
| Risco | Principais riscos |
| Liquidez | Saída/renda |
| Estratégia | Aderência |
| Regras | Elegibilidade |
| Score | Qualidade |
| Fit | Aderência ao investidor |
| Ranking | Prioridade |
| Explicabilidade | Por que é oportunidade |
| Análise | Tese |
| Decisão | Resultado |
| Histórico | Memória |


# 30. Exemplo de Ponta a Ponta

Uma captura identifica um apartamento de 3 dormitórios anunciado por R$ 191.651. O Radar consolida fontes, encontra comparáveis, estima valor de mercado, calcula custo econômico, margem, yield, liquidez e riscos. A oportunidade recebe score, Fit e confiança. Entra no ranking. A análise profunda identifica uma pendência documental. A decisão passa para BUY IF. Após a resolução, a oportunidade retorna ao ranking e pode ser aprovada. O resultado real posteriormente alimenta o aprendizado.

| Etapa | Saída |
|---|---|
| Captura | Preço original |
| Valuation | Valor estimado |
| Economia | Margem |
| Risco | Pendência |
| Liquidez | Score |
| Score/Fit | Prioridade |
| DD | Condição |
| Decisão | BUY IF |
| Monitoramento | Condição resolvida |
| Aquisição | Resultado real |
| Aprendizado | Calibração |


# 31. Critérios de Aceite

- CA-D25 — Existe uma visão funcional única do produto.
- CA-D25 — Todos os módulos principais possuem propósito definido.
- CA-D25 — As entidades principais estão diferenciadas.
- CA-D25 — O fluxo ponta a ponta está definido.
- CA-D25 — Imóvel e oportunidade estão separados.
- CA-D25 — Score e Fit estão separados.
- CA-D25 — Regras precedem score.
- CA-D25 — Valuation e preço máximo estão conectados.
- CA-D25 — Economia considera custo total.
- CA-D25 — Risco influencia decisão.
- CA-D25 — Liquidez influencia economia e ranking.
- CA-D25 — Capital influencia prioridade.
- CA-D25 — Due Diligence valida a tese.
- CA-D25 — Monitoramento reabre/recalcula oportunidades.
- CA-D25 — Alertas possuem ação.
- CA-D25 — Histórico preserva decisões.
- CA-D25 — Governança controla versões.
- CA-D25 — Aprendizado usa resultados reais.
- CA-D25 — O MVP prova uma oportunidade real de ponta a ponta.
- CA-D25 — Arquitetura técnica não foi antecipada.

# 32. Visão Executiva Final

O Radar Imobiliário é, funcionalmente, uma máquina de transformar informação imobiliária em decisão de investimento.
FONTES → INFORMAÇÃO → IMÓVEL → OPORTUNIDADE → EVIDÊNCIA → VALUATION → ECONOMIA → RISCO → LIQUIDEZ → ESTRATÉGIA → SCORE → FIT → RANKING → DUE DILIGENCE → DECISÃO → MONITORAMENTO → RESULTADO → APRENDIZADO
A unidade central do produto não é o anúncio. É a oportunidade economicamente fundamentada e continuamente acompanhada.

# 33. Próximo Documento

Recomendação: Documento 26 — Especificação Funcional do MVP e Plano de Construção da Primeira Versão. Com o mapa mestre consolidado, o próximo passo é definir exatamente o que entra na primeira versão operacional, o que fica fora, quais fluxos precisam funcionar de ponta a ponta e quais entregas comprovam valor real.
