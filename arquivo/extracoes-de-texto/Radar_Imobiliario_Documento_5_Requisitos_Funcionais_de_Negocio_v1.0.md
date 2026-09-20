# Radar_Imobiliario_Documento_5_Requisitos_Funcionais_de_Negocio_v1.0

Radar Imobiliário
Documento 5 — Requisitos Funcionais de Negócio e Jornada Completa | v1.0
Documento de negócio — produto, módulos, funcionalidades, estados, decisões e fluxos.
Princípio: o Radar não é uma base de imóveis. É um sistema de descoberta, avaliação, priorização e acompanhamento de oportunidades.

# 1. Objetivo

Transformar os quatro documentos anteriores em uma visão funcional única do produto. Este documento descreve o que o Radar deve fazer do ponto de vista do negócio, sem definir arquitetura, linguagem, banco de dados ou infraestrutura.
- Definir a jornada completa do imóvel.
- Definir os módulos funcionais.
- Definir responsabilidades de cada módulo.
- Definir entradas, saídas e decisões.
- Definir estados e transições.
- Definir cadastros e parâmetros.
- Definir alertas, histórico e rastreabilidade.
- Preparar a base para os requisitos técnicos posteriores.

# 2. Visão do produto

O Radar recebe oportunidades de múltiplas fontes, normaliza os dados, identifica duplicidades, enriquece o imóvel, calcula valor de mercado, aplica regras e estratégias, calcula score, classifica oportunidades e conduz a análise até uma decisão.
A unidade central do produto é a Oportunidade Imobiliária, que representa um imóvel acompanhado ao longo do tempo e não apenas um registro capturado de uma fonte.

# 3. Jornada macro


| Etapa | Pergunta de negócio | Saída |
|---|---|---|
| 1. Captura | o que apareceu no mercado? | oportunidade bruta |
| 2. Normalização | é o mesmo imóvel e quais são seus dados padronizados? | imóvel identificado |
| 3. Qualificação | pode entrar no Radar? | elegível/bloqueado |
| 4. Enriquecimento | o que sabemos sobre ele? | perfil enriquecido |
| 5. Valuation | quanto vale de forma realista? | faixas de valor |
| 6. Economia | quanto realmente custa? | custo e margem |
| 7. Estratégia | para qual estratégia serve? | aderência |
| 8. Score | quão boa é a oportunidade? | score/classificação |
| 9. Ranking | quais merecem atenção primeiro? | prioridade |
| 10. Due Diligence | a tese é verdadeira? | aprovada/condicional/reprovada |
| 11. Decisão | o que fazer? | comprar/monitorar/não comprar |
| 12. Monitoramento | o que mudou? | reavaliação/alerta |
| 13. Aprendizado | o Radar acertou? | histórico/backtest |


# 4. Conceito de Oportunidade

Uma oportunidade deve possuir identidade própria e histórico. Capturas sucessivas do mesmo imóvel não devem criar oportunidades independentes; devem alimentar a mesma linha de acompanhamento, salvo quando a regra de negócio determinar que se trata de uma nova oportunidade comercial.
- Imóvel = identidade física/documental.
- Captura = ocorrência em uma fonte.
- Oportunidade = tese econômica sobre aquele imóvel.
- Análise = fotografia da tese em determinado momento.
- Decisão = resultado de uma análise.

# 5. Módulos funcionais


| Módulo | Responsabilidade |
|---|---|
| 1. Fontes | gerenciar origens dos imóveis |
| 2. Captura | receber novas oportunidades |
| 3. Normalização | padronizar dados |
| 4. Deduplicação | identificar o mesmo imóvel |
| 5. Perfil do imóvel | consolidar características |
| 6. Localização | classificar e parametrizar áreas |
| 7. Mercado | comparáveis e valuation |
| 8. Economia | custos, margem e cenários |
| 9. Estratégias | configurar teses de investimento |
| 10. Regras | executar critérios |
| 11. Score | pontuar oportunidades |
| 12. Ranking | priorizar |
| 13. Due Diligence | investigar profundamente |
| 14. Workflow | controlar estados e decisões |
| 15. Alertas | notificar mudanças |
| 16. Monitoramento | acompanhar ciclo de vida |
| 17. Histórico | preservar evolução |
| 18. Relatórios | permitir análise gerencial |
| 19. Backtest | avaliar qualidade das regras |
| 20. Governança | versionar parâmetros e decisões |


# 6. Módulo de Fontes

Deve permitir cadastrar fontes sem alterar o conceito central do Radar.
- Nome da fonte.
- Tipo de fonte.
- Abrangência geográfica.
- Periodicidade esperada.
- Status ativo/inativo.
- Regras específicas da fonte.
- Campos disponíveis.
- Confiabilidade histórica.
- Data da última captura.
A Caixa deve ser a primeira fonte, mas nenhuma regra estrutural deve depender exclusivamente dela.

# 7. Captura

- Registrar cada imóvel encontrado.
- Registrar data/hora da captura.
- Preservar dados originais.
- Registrar preço e status observados.
- Registrar identificador da fonte.
- Detectar alteração de preço/status.
- Evitar perda do histórico anterior.
- Encaminhar novos registros para qualificação.
O dado original deve ser preservado para permitir auditoria e comparação futura.

# 8. Normalização

A normalização transforma formatos diferentes em uma linguagem comum do Radar.
- Endereço.
- CEP.
- Bairro.
- Cidade.
- Estado.
- Tipo de imóvel.
- Áreas.
- Quartos.
- Banheiros.
- Vagas.
- Preço.
- Avaliação.
- Condomínio.
- Status.
- Matrícula.
- Identificadores.
Quando um campo não puder ser normalizado com segurança, o sistema deve preservar o valor original e marcar a inconsistência.

# 9. Deduplicação

O Radar deve identificar quando duas ou mais fontes estão descrevendo o mesmo imóvel.

| Evidência | Força |
|---|---|
| Matrícula igual | muito alta |
| Identificador oficial igual | muito alta |
| Endereço + unidade | alta |
| Endereço + características | média |
| Similaridade parcial | baixa; requer validação |

Deduplicação incorreta é um risco grave: duplicar oportunidades distorce ranking, cobertura e estatísticas.

# 10. Perfil consolidado do imóvel

O perfil deve separar dado observado, dado calculado, dado estimado e dado confirmado.

| Tipo de dado | Exemplo |
|---|---|
| Observado | preço informado pela fonte |
| Confirmado | informação documental validada |
| Calculado | desconto líquido |
| Estimado | aluguel provável |
| Inferido | segmento de mercado provável |
| Desconhecido | dado ainda não disponível |


# 11. Qualificação inicial

Antes de gastar esforço de investigação, o Radar deve aplicar filtros mínimos.
- Localização elegível.
- Tipo permitido.
- Faixa de preço.
- Fonte válida.
- Dados mínimos.
- Ausência de bloqueio conhecido.
- Compatibilidade com pelo menos uma estratégia, quando configurado.
O imóvel pode ser mantido em monitoramento mesmo sem cumprir critérios de prioridade, desde que não exista bloqueio definitivo.

# 12. Enriquecimento

O enriquecimento agrega informações que não estavam na captura inicial.
- Comparáveis.
- Preço/m².
- Aluguel.
- Condomínio.
- IPTU.
- Localização.
- Liquidez.
- Risco.
- Matrícula.
- Processos.
- Ocupação.
- Reforma.
- Infraestrutura.
- Histórico de preços.
Cada informação enriquecida deve possuir origem, data e nível de confiança.

# 13. Valuation


| Entrada | Processamento | Saída |
|---|---|---|
| Características | comparáveis adequados | faixa de mercado |
| Localização | segmentação | ajuste local |
| Estado | ajustes | valor conservador/base/otimista |
| Histórico | tendência/anomalias | confiança |
| Aluguel | relação preço/renda | checagem econômica |

O valuation não deve ser um único número sem contexto. O Radar precisa mostrar faixa e confiança.

# 14. Módulo econômico

Deve calcular a economia completa da operação.
- Preço de aquisição.
- Comissão.
- Tributos.
- Registro/documentação.
- Dívidas atribuíveis.
- Condomínio.
- Reforma.
- Contingência.
- Custo de carregamento.
- Custo financeiro quando aplicável.
- Custo de venda.
- Custo econômico total.
- Margem.
- Margem %.
- Yield.
- Retorno sobre capital.

# 15. Estratégias

Uma oportunidade pode ser avaliada simultaneamente em várias estratégias.

| Estratégia | Pergunta principal |
|---|---|
| Renda | gera fluxo adequado ao risco? |
| Revenda | há margem após custos e prazo? |
| Valorização | há tese de crescimento sustentável? |
| MCMV/baixa renda | há demanda e liquidez no segmento? |
| Terreno | há potencial econômico de uso? |
| Apartamento | as características favorecem liquidez/renda? |
| Casa/sobrado | terreno + construção + localização fazem sentido? |
| 1 dormitório | há demanda suficiente para o produto? |


# 16. Regras

O módulo de regras deve permitir critérios globais, específicos de estratégia, localização e tipo de imóvel.
- Ativar/desativar.
- Definir prioridade.
- Definir condição.
- Definir parâmetro.
- Definir vigência.
- Definir escopo.
- Definir severidade.
- Definir exceção.
- Registrar justificativa.
- Versionar alteração.

# 17. Score

O Score deve ser consequência das regras e dos indicadores, não um número arbitrário.
- Score bruto.
- Pontuação por dimensão.
- Pesos por estratégia.
- Penalizações.
- Bônus.
- Fator de confiança.
- Score final.
- Classificação.
- Explicação das contribuições.

# 18. Ranking

O ranking deve responder: quais oportunidades merecem meu tempo agora?

| Prioridade | Critério |
|---|---|
| 1 | não bloqueada |
| 2 | score final |
| 3 | confiança |
| 4 | margem |
| 5 | liquidez |
| 6 | risco |
| 7 | atualidade |
| 8 | aderência a múltiplas estratégias |


# 19. Tela conceitual da oportunidade

A visão de negócio de uma oportunidade deve apresentar, em uma única leitura:
- Identificação e localização.
- Preço atual.
- Valor de mercado.
- Desconto líquido.
- Custo econômico total.
- Margem.
- Yield quando aplicável.
- Score por estratégia.
- Classificação.
- Risco.
- Confiança.
- Principais motivos positivos.
- Principais alertas.
- Pendências.
- Próxima ação.

# 20. Workflow de Due Diligence


| Fase | Objetivo |
|---|---|
| Preparação | definir escopo |
| Documental | validar documentos |
| Jurídica | investigar riscos |
| Financeira | confirmar custos |
| Mercado | validar valuation/aluguel |
| Física | validar estado/reforma |
| Estratégica | confirmar tese |
| Decisão | aprovar/reprovar/condicionar |


# 21. Pendências

Toda pendência deve ser explícita e possuir prioridade.

| Prioridade | Comportamento |
|---|---|
| Crítica | impede decisão |
| Alta | impede aprovação normal |
| Média | reduz confiança |
| Baixa | não impede decisão |


# 22. Decisão


| Decisão | Significado |
|---|---|
| COMPRAR | tese validada |
| COMPRAR SE | condição objetiva pendente |
| MONITORAR | tese interessante, timing/dados insuficientes |
| NÃO COMPRAR | economia ou risco incompatível |
| BLOQUEAR | regra crítica violada |


# 23. Monitoramento

O imóvel continua sendo acompanhado depois de uma decisão de monitoramento ou mesmo depois de uma aprovação, enquanto houver interesse.
- Preço.
- Status.
- Avaliação.
- Comparáveis.
- Aluguel.
- Condomínio.
- Riscos.
- Processos.
- Score.
- Classificação.
- Mudanças de estratégia.
- Mudanças de parâmetros.

# 24. Alertas


| Evento | Prioridade sugerida |
|---|---|
| Preço caiu significativamente | alta |
| Score subiu | alta |
| Entrou em faixa excepcional | alta |
| Mudança de status | alta |
| Novo risco | crítica/alta |
| Novo comparável relevante | média |
| Mudança de valuation | média |
| Oportunidade voltou a ser elegível | alta |
| Parâmetro alterado | informativa |


# 25. Ciclo de vida

O ciclo de vida deve ser histórico e não destrutivo.

| Estado | Pode avançar para |
|---|---|
| Capturado | Qualificado/Bloqueado |
| Qualificado | Em análise/Monitorando |
| Em análise | Pendente/Aprovado/Reprovado |
| Pendente | Em análise/Bloqueado |
| Aprovado | Comprado/Monitorando |
| Monitorando | Em análise/Reprovado |
| Comprado | Pós-investimento |


# 26. Histórico

- Histórico de preço.
- Histórico de status.
- Histórico de valuation.
- Histórico de score.
- Histórico de regras.
- Histórico de parâmetros.
- Histórico de decisões.
- Histórico de alertas.
- Histórico de evidências.
- Histórico de custo estimado.
O histórico deve permitir reconstruir por que uma oportunidade foi classificada de determinada maneira em uma data passada.

# 27. Cadastro de parâmetros


| Grupo | Exemplos |
|---|---|
| Localização | classes, áreas prioritárias/bloqueadas |
| Preço | mínimos/máximos |
| Mercado | comparáveis e confiança |
| Economia | margens e custos |
| Renda | yield e vacância |
| Liquidez | níveis mínimos |
| Risco | limites |
| Score | pesos e faixas |
| Estratégia | regras específicas |
| Alertas | gatilhos |
| Workflow | prazos/status |


# 28. Gestão de preferências do investidor

O usuário deve poder expressar sua tese de investimento sem transformar preferências pessoais em código rígido.
- Estratégias ativas.
- Regiões desejadas.
- Regiões condicionais.
- Regiões bloqueadas.
- Tipos aceitos.
- Tipos prioritários.
- Ticket mínimo/máximo.
- Margem mínima.
- Yield mínimo.
- Liquidez mínima.
- Nível de risco aceitável.
- Peso das estratégias.
- Preferências de prazo.

# 29. Busca e filtros

- Localização.
- Preço.
- Desconto.
- Valor de mercado.
- Margem.
- Score.
- Estratégia.
- Liquidez.
- Risco.
- Confiança.
- Tipo.
- Quartos.
- Área.
- Vagas.
- Condomínio.
- Status.
- Data de captura.
- Mudanças recentes.
Filtros não devem destruir a oportunidade: um filtro de visualização é diferente de uma regra eliminatória.

# 30. Comparação de oportunidades

Deve ser possível comparar imóveis lado a lado usando critérios econômicos e estratégicos.

| Critério | Comparação |
|---|---|
| Preço | menor/maior |
| Valor de mercado | faixa |
| Desconto líquido | % |
| Margem | R$/% |
| Yield | % a.m./a.a. |
| Liquidez | nível |
| Risco | nível |
| Confiança | nível |
| Score | por estratégia |
| Pendências | quantidade/severidade |


# 31. Relatórios de negócio

- Melhores oportunidades.
- Oportunidades por estratégia.
- Oportunidades por região.
- Mudanças de preço.
- Oportunidades bloqueadas e motivos.
- Pendências da Due Diligence.
- Evolução do score.
- Performance das regras.
- Histórico de decisões.
- Resultado por estratégia.
- Taxa de conversão em aquisição.

# 32. Regras de explicabilidade

Nenhuma classificação relevante deve aparecer sem justificativa.
Exemplo: 'Excelente para Renda porque yield estimado de X%, liquidez alta e custo total Y; perdeu pontos por condomínio; confiança alta; pendência: confirmar débito condominial.'
A explicação deve permitir ao investidor discordar do Radar e identificar exatamente qual premissa precisa ser alterada.

# 33. Reprocessamento

Mudanças relevantes devem poder reprocessar a oportunidade sem perder o resultado anterior.
- Nova captura.
- Novo preço.
- Novo valuation.
- Novo comparável.
- Novo risco.
- Novo parâmetro.
- Nova estratégia.
- Conclusão da pendência.
- Mudança de status.

# 34. Multi-fonte

O produto deve nascer com o conceito de fonte independente.
- Caixa como primeira fonte.
- Possibilidade de outras instituições.
- Portais imobiliários.
- Leiloeiros.
- Fontes de mercado.
- Fontes de dados públicos.
- Dados fornecidos manualmente pelo usuário.
A fonte pode mudar; a lógica de oportunidade deve permanecer.

# 35. Requisitos funcionais consolidados


| ID | Requisito | Prioridade |
|---|---|---|
| RF-001 | Capturar imóveis de fontes configuradas. | Obrigatório |
| RF-002 | Preservar o dado original. | Obrigatório |
| RF-003 | Normalizar atributos. | Obrigatório |
| RF-004 | Identificar duplicidades. | Obrigatório |
| RF-005 | Criar perfil consolidado. | Obrigatório |
| RF-006 | Classificar localização. | Obrigatório |
| RF-007 | Enriquecer dados. | Obrigatório |
| RF-008 | Calcular valuation. | Obrigatório |
| RF-009 | Calcular custo econômico. | Obrigatório |
| RF-010 | Calcular margem. | Obrigatório |
| RF-011 | Calcular yield. | Obrigatório |
| RF-012 | Aplicar regras. | Obrigatório |
| RF-013 | Aplicar estratégias. | Obrigatório |
| RF-014 | Calcular score. | Obrigatório |
| RF-015 | Calcular confiança. | Obrigatório |
| RF-016 | Classificar oportunidade. | Obrigatório |
| RF-017 | Ordenar ranking. | Obrigatório |
| RF-018 | Abrir Due Diligence. | Obrigatório |
| RF-019 | Controlar pendências. | Obrigatório |
| RF-020 | Registrar evidências. | Obrigatório |
| RF-021 | Registrar decisão. | Obrigatório |
| RF-022 | Monitorar mudanças. | Obrigatório |
| RF-023 | Gerar alertas. | Obrigatório |
| RF-024 | Preservar histórico. | Obrigatório |
| RF-025 | Permitir parametrização. | Obrigatório |
| RF-026 | Versionar regras. | Obrigatório |
| RF-027 | Comparar oportunidades. | Obrigatório |
| RF-028 | Gerar relatórios. | Obrigatório |
| RF-029 | Executar backtest. | Obrigatório |
| RF-030 | Explicar decisões. | Obrigatório |


# 36. Requisitos não funcionais de negócio

- Rastreabilidade: toda decisão deve ser reconstruível.
- Auditabilidade: alterações de regras e parâmetros devem ser identificáveis.
- Transparência: dados estimados devem ser distinguidos de confirmados.
- Consistência: a mesma configuração deve produzir resultado reproduzível.
- Flexibilidade: parâmetros devem poder mudar sem redefinir o domínio.
- Histórico: mudanças não devem apagar o passado.
- Prudência: incerteza deve reduzir confiança.
- Explicabilidade: cada classificação deve possuir justificativa.

# 37. O que NÃO faz parte do Radar

- O Radar não substitui advogado.
- O Radar não substitui engenheiro/arquiteto em avaliação física.
- O Radar não garante valorização.
- O Radar não garante liquidez.
- O Radar não garante rentabilidade.
- O Radar não autoriza compra automaticamente.
- O Radar não deve esconder incertezas.
Ele é um sistema de apoio à decisão, não um substituto da diligência profissional.

# 38. Exemplo de jornada completa

Imóvel capturado por uma fonte → identificado e normalizado → mesma matrícula encontrada em outra fonte → registros consolidados → localização classificada como B → valuation conservador de R$ 300 mil → custo econômico estimado de R$ 225 mil → desconto líquido de 25% → yield estimado de 0,93% a.m. → score alto para Renda e médio para Flip → Due Diligence aberta → identificado débito ainda não confirmado → oportunidade fica 'Comprar se' → confirmação do débito atualiza custo → score é recalculado → decisão final.
O exemplo demonstra que o Radar deve ser um processo vivo, e não uma classificação definitiva na captura.

# 39. Critério de sucesso do produto

O Radar terá sucesso se conseguir reduzir o tempo gasto procurando imóveis e aumentar a qualidade das oportunidades efetivamente investigadas, mantendo baixo índice de falsos positivos e permitindo explicar por que cada oportunidade foi priorizada.

| Objetivo | Métrica |
|---|---|
| Descoberta | volume de oportunidades relevantes |
| Qualificação | taxa que passa filtros |
| Precisão | falsos positivos/negativos |
| Valuation | erro entre estimado e observado |
| Decisão | tempo até aprovação/reprovação |
| Investimento | taxa de conversão |
| Retorno | resultado por estratégia |
| Aprendizado | melhoria após backtest |


# 40. Arquitetura de negócio consolidada

Sem entrar em tecnologia, o domínio funcional agora pode ser visualizado como:
FONTES → CAPTURA → NORMALIZAÇÃO → DEDUPLICAÇÃO → PERFIL → ENRIQUECIMENTO → VALUATION → ECONOMIA → ESTRATÉGIAS → REGRAS → SCORE → RANKING → DUE DILIGENCE → DECISÃO → MONITORAMENTO → HISTÓRICO → BACKTEST
Essa cadeia representa o coração do Radar.

# 41. Próximo documento

Documento 6 — Modelo de Dados de Negócio e Dicionário de Entidades.
O próximo passo recomendado é definir, ainda sem tecnologia, as entidades do domínio e seus relacionamentos: Imóvel, Captura, Fonte, Oportunidade, Estratégia, Regra, Parâmetro, Avaliação, Comparável, Custo, Risco, Evidência, Pendência, Análise, Score, Alerta, Decisão, Histórico e demais conceitos.
Depois do Documento 6, teremos uma base muito madura para transformar o negócio em especificação técnica.
