# Radar_Imobiliario_Documento_16_Captura_Normalizacao_Deduplicacao_Identificacao_v1.0

🏠 RADAR IMOBILIÁRIO
Documento 16
Captura, Normalização, Deduplicação e Identificação de Imóveis
Especificação Funcional de Negócio | Versão 1.0
Muitas fontes → muitas capturas → um imóvel → várias oportunidades ao longo do tempo

# 1. Objetivo

Definir como o Radar recebe informações de diferentes fontes, preserva a captura original, normaliza os dados, identifica o imóvel físico/documental, detecta duplicidades e consolida diferentes anúncios/capturas sem perder histórico.
- Separar claramente Fonte, Captura, Imóvel e Oportunidade.
- Evitar que o mesmo imóvel apareça várias vezes como oportunidades independentes.
- Permitir que uma nova captura altere o estado da oportunidade sem apagar o passado.
- Permitir expansão para novas fontes sem mudar o conceito de negócio.
- Não definir tecnologia, arquitetura ou implementação.

# 2. Conceitos Fundamentais


| Conceito | Definição | Exemplo |
|---|---|---|
| Fonte | Origem da informação. | Caixa, leiloeiro, portal, documento público. |
| Captura | Fotografia do que uma fonte informou em determinado momento. | Oferta por R$ 200 mil em 14/09. |
| Imóvel | Ativo físico/documental identificado. | Apartamento unidade 302. |
| Oportunidade | Tese econômica associada ao imóvel em determinado contexto. | Comprar abaixo do valor de mercado. |
| Análise | Avaliação da oportunidade em um momento. | Valuation + risco + estratégia. |
| Decisão | Resultado da análise. | BUY IF. |
| Histórico | Evolução temporal de todos os elementos. | Preço caiu, risco mudou, score mudou. |


# 3. Princípio de Identidade

O Radar deve tratar a identidade do imóvel como algo mais estável que a oferta. Uma oferta pode desaparecer, mudar de preço ou trocar de modalidade sem que o imóvel deixe de existir.

| Situação | Tratamento |
|---|---|
| Mesma unidade em duas fontes | Uma entidade Imóvel, duas Capturas. |
| Mesma unidade em datas diferentes | Uma entidade Imóvel, várias Capturas históricas. |
| Preço alterado | Nova versão/captura, não novo imóvel. |
| Anúncio retirado e republicado | Tentar associar ao imóvel existente. |
| Mesmo condomínio, unidades diferentes | Imóveis distintos. |
| Mesmo endereço, apartamentos diferentes | Imóveis distintos. |
| Oferta sem identificação suficiente | Criar candidato, não assumir identidade definitiva. |


# 4. Fluxo Funcional

O fluxo recomendado é:
FONTE → CAPTURA ORIGINAL → NORMALIZAÇÃO → IDENTIFICAÇÃO → DEDUPLICAÇÃO → CONSOLIDAÇÃO → QUALIFICAÇÃO → ENRIQUECIMENTO → OPORTUNIDADE

| Etapa | Responsabilidade |
|---|---|
| Captura | Preservar exatamente o que foi encontrado. |
| Normalização | Padronizar formatos sem alterar o significado. |
| Identificação | Determinar qual imóvel está sendo representado. |
| Deduplicação | Verificar se já existe o mesmo imóvel. |
| Consolidação | Reunir informações complementares das fontes. |
| Qualificação | Decidir se merece processamento adicional. |
| Enriquecimento | Adicionar mercado, custos, risco etc. |
| Oportunidade | Avaliar economicamente. |


# 5. Captura Original


| Dado | Regra |
|---|---|
| Fonte | Sempre obrigatório. |
| Data/hora | Sempre obrigatório. |
| Identificador da fonte | Preservar quando existir. |
| URL/referência da publicação | Preservar quando disponível. |
| Preço | Guardar valor original e normalizado. |
| Status | Guardar valor original e normalizado. |
| Texto/descrição | Preservar informação relevante. |
| Imagens/documentos | Preservar referência quando disponíveis. |
| Condição da oferta | Registrar modalidade e condições conhecidas. |

A captura original é evidência histórica. Correções posteriores não devem sobrescrever silenciosamente o conteúdo capturado.

# 6. Normalização

Normalizar significa tornar dados comparáveis, não inventar dados.

| Campo | Normalização |
|---|---|
| Endereço | Padronizar abreviações, logradouro, número, complemento e CEP. |
| Município | Padronizar nome. |
| Bairro | Padronizar grafia e relacionamentos conhecidos. |
| Área | Separar valor e tipo de área. |
| Preço | Converter para representação monetária consistente. |
| Quartos | Normalizar quantidade. |
| Vagas | Normalizar quantidade e tipo quando conhecido. |
| Tipo | Mapear para taxonomia do Radar. |
| Status | Mapear para estados padronizados. |
| Data | Padronizar formato sem perder a original. |
| Texto | Preservar original; normalizado é adicional. |


# 7. Taxonomia de Tipos de Imóvel


| Grupo | Exemplos |
|---|---|
| Apartamento | 1 dormitório, 2 dormitórios, 3 dormitórios etc. |
| Casa | Casa térrea, geminada etc. |
| Sobrado | Sobrado residencial. |
| Terreno | Lote, terreno urbano etc. |
| Comercial | Sala, loja, conjunto. |
| Rural | Chácara, sítio etc., se habilitado. |
| Outros | Tipos não classificados. |
| Desconhecido | Ainda não identificado. |

A taxonomia deve ser extensível e parametrizável. Tipo desconhecido não deve ser convertido automaticamente em um tipo provável sem evidência.

# 8. Identificação do Imóvel

A identificação deve usar múltiplos sinais, com prioridade para identificadores fortes.

| Sinal | Força |
|---|---|
| Matrícula + unidade | Muito alta |
| Identificador oficial do imóvel | Muito alta |
| Endereço completo + unidade | Alta |
| Condomínio + unidade + área | Alta |
| Endereço + características compatíveis | Média |
| Título/descrição semelhante | Média/baixa |
| Preço semelhante | Baixa |
| Imagem semelhante | Complementar |

Preço nunca deve ser usado sozinho para afirmar que duas ofertas representam o mesmo imóvel.

# 9. Chave Conceitual de Identidade

O Radar deve construir uma identidade composta conforme os dados disponíveis, por exemplo:
- Município + logradouro + número + unidade.
- Condomínio + bloco + unidade.
- Matrícula.
- Identificador oficial.
- Combinação de endereço + área + quartos + vaga quando identificadores fortes não estiverem disponíveis.
A chave exata é uma decisão de negócio dependente do nível de identificação disponível; o sistema deve trabalhar também com identidade provável e identidade pendente.

# 10. Níveis de Identidade


| Nível | Descrição | Uso |
|---|---|---|
| I0 — Desconhecido | Não há sinais suficientes. | Não consolidar. |
| I1 — Candidato | Há indícios, mas insuficientes. | Acompanhar. |
| I2 — Provável | Múltiplos sinais compatíveis. | Pode consolidar com cautela. |
| I3 — Confirmado | Identificador forte ou evidência robusta. | Consolidação normal. |
| I4 — Documental | Identidade confirmada por documentação. | Máxima confiança. |


# 11. Deduplicação

Deduplicação responde: 'esta nova captura representa um imóvel que já conhecemos?'

| Caso | Resultado |
|---|---|
| Correspondência exata | Associar ao imóvel existente. |
| Correspondência forte | Associar e registrar evidências. |
| Correspondência provável | Solicitar/gerar validação. |
| Possível duplicidade | Não fundir automaticamente. |
| Sem correspondência | Criar novo imóvel. |
| Conflito de identidade | Manter separados até resolução. |


# 12. Matriz de Evidências para Deduplicação


| Sinal | Exemplo de peso conceitual |
|---|---|
| Matrícula igual | Decisivo |
| Identificador oficial igual | Decisivo |
| Unidade + condomínio iguais | Muito forte |
| Endereço completo igual | Forte |
| Área próxima | Médio |
| Quartos/vagas iguais | Médio |
| Descrição semelhante | Fraco/médio |
| Preço semelhante | Fraco |
| Imagem semelhante | Complementar |
| Mesma fonte + mesmo identificador | Muito forte |

Pesos e limiares devem ser parametrizáveis e calibrados com casos reais. Uma correspondência de baixa confiança não deve gerar fusão irreversível.

# 13. Fusão x Associação

O Radar deve diferenciar consolidar informação de apagar diferenças entre fontes.

| Ação | Quando |
|---|---|
| Associar captura ao imóvel | Quando a identidade é suficientemente confiável. |
| Manter ambas as informações | Quando fontes trazem valores diferentes. |
| Escolher valor vigente | Somente para a decisão atual, preservando histórico. |
| Criar pendência | Quando a divergência for material. |
| Fusão definitiva | Somente com evidência suficiente. |
| Desfazer associação | Quando nova evidência mostrar erro, preservando histórico da decisão anterior. |


# 14. Conflitos entre Fontes


| Conflito | Tratamento |
|---|---|
| Preço diferente | Registrar ambos; identificar data/condição. |
| Área diferente | Investigar tipo de área e fonte. |
| Quartos diferentes | Registrar divergência. |
| Status diferente | Priorizar informação mais atual/adequada e gerar evento. |
| Ocupação divergente | Pendência crítica até confirmação. |
| Matrícula divergente | Não fundir automaticamente. |
| Endereço divergente | Investigar se é variação de cadastro ou outro imóvel. |


# 15. Consolidação do Perfil

Depois da identificação, o Radar cria um perfil consolidado sem destruir os dados originais.

| Perfil consolidado | Fonte de suporte |
|---|---|
| Endereço normalizado | Capturas + fontes de referência |
| Características | Fonte mais confiável + confirmações |
| Preço atual | Captura vigente |
| Histórico de preços | Todas as capturas |
| Status atual | Última evidência válida |
| Matrícula | Documento/evidência documental |
| Área | Fonte mais confiável + tipo da área |
| Imagens | Histórico das capturas |
| Confiança | Qualidade e concordância das fontes |


# 16. Capturas e Oportunidades

Uma captura não é automaticamente uma oportunidade. A oportunidade nasce quando existe uma tese econômica potencial após qualificação.

| Situação | Resultado |
|---|---|
| Oferta nova, preço normal | Captura + baixa prioridade |
| Oferta nova, grande desconto aparente | Captura + oportunidade potencial |
| Preço cai | Nova captura + reavaliação da oportunidade |
| Preço sobe | Nova captura + possível redução de score |
| Oferta desaparece | Histórico + mudança de status |
| Mesmo imóvel em outro leiloeiro | Nova captura associada ao mesmo imóvel; avaliar nova oportunidade/oferta |
| Mesmo imóvel com outra estratégia | Uma mesma base de imóvel pode gerar análises estratégicas distintas |


# 17. Ciclo de Vida da Captura


| Estado | Descrição |
|---|---|
| Captured | Recebida da fonte. |
| Normalized | Dados padronizados. |
| Identified | Imóvel identificado. |
| Matched | Associada a imóvel existente. |
| Qualified | Passou pelos critérios mínimos. |
| Enriched | Recebeu dados adicionais. |
| Expired | Informação deixou de ser vigente. |
| Superseded | Substituída por captura mais nova. |
| Rejected | Captura inválida/irrelevante. |
| Error | Problema de qualidade que exige correção. |


# 18. Ciclo de Vida do Imóvel


| Estado | Significado |
|---|---|
| Candidate | Identidade ainda não confirmada. |
| Active | Imóvel identificado e relevante. |
| Monitoring | Acompanhado por interesse. |
| Opportunity | Possui tese econômica relevante. |
| Acquired | Adquirido pelo investidor. |
| Sold | Saída realizada. |
| Inactive | Sem oferta/atividade conhecida. |
| Closed | Ciclo encerrado. |


# 19. Regras de Atualização

- Nova captura nunca apaga a captura anterior.
- Alteração material de preço deve gerar evento.
- Alteração material de status deve gerar evento.
- Mudança de identidade deve ser auditável.
- Nova evidência pode elevar ou reduzir confiança.
- Uma captura mais nova não torna automaticamente a anterior 'errada'; ela apenas pode deixar de ser vigente.
- Mudanças materiais devem reavaliar oportunidade, score e alertas.

# 20. Regras de Reprocessamento


| Evento | Reprocessamento |
|---|---|
| Novo preço | Economia + score + ranking |
| Novo status | Elegibilidade + workflow |
| Nova matrícula | Identidade + risco |
| Nova área | Valuation + comparáveis |
| Novo comparável | Valuation + score |
| Novo aluguel | Yield + estratégia |
| Novo risco | Risco + decisão |
| Mudança de regra | Todas as oportunidades afetadas |
| Nova estratégia | Reavaliar aderência |
| Nova fonte | Deduplicação/consolidação |


# 21. Casos de Uso


| ID | Caso de uso | Resultado |
|---|---|---|
| UC-016-01 | Capturar nova oferta | Criar snapshot. |
| UC-016-02 | Normalizar captura | Padronizar dados. |
| UC-016-03 | Identificar imóvel | Determinar candidato/existente. |
| UC-016-04 | Detectar duplicidade | Associar ou separar. |
| UC-016-05 | Consolidar perfil | Atualizar visão vigente. |
| UC-016-06 | Registrar conflito | Criar pendência/evidência. |
| UC-016-07 | Atualizar oportunidade | Recalcular após mudança. |
| UC-016-08 | Desassociar captura | Corrigir vínculo preservando histórico. |
| UC-016-09 | Encerrar oferta | Marcar captura/status como encerrado. |
| UC-016-10 | Reativar acompanhamento | Nova captura pode reabrir análise. |


# 22. Cenários de Deduplicação


| Cenário | Decisão |
|---|---|
| Apto 302 aparece em Caixa e leiloeiro | Mesmo imóvel, fontes distintas. |
| Apto 302 aparece duas vezes na Caixa | Uma identidade, múltiplas capturas. |
| Apto 302 e Apto 303 no mesmo prédio | Imóveis distintos. |
| Mesmo endereço sem unidade | Candidato; não fundir sem evidência. |
| Matrícula igual e endereço divergente | Investigar antes de consolidar. |
| Preço igual, endereços diferentes | Não deduplicar. |
| Descrição igual, unidades diferentes | Não deduplicar automaticamente. |
| Oferta encerrada e republicada | Tentar associar ao imóvel histórico. |


# 23. Falsos Positivos e Falsos Negativos

Deduplicação é uma decisão com dois erros possíveis:

| Erro | Impacto |
|---|---|
| Falso positivo | Fundir imóveis diferentes; pode contaminar valuation, risco e decisão. |
| Falso negativo | Criar dois registros para o mesmo imóvel; pode duplicar oportunidade e gerar ruído. |
| Princípio | Em casos ambíguos, preservar separação e solicitar evidência é preferível a uma fusão irreversível. |


# 24. Qualidade e Confiança da Identidade


| Identidade | Efeito |
|---|---|
| Confirmada | Pode participar normalmente do Radar. |
| Provável | Pode ser analisada, mas com confiança reduzida. |
| Candidata | Pode permanecer em monitoramento. |
| Conflitante | Não permitir decisão econômica definitiva. |
| Desconhecida | Apenas captura/triagem. |


# 25. Explainability da Consolidação

Quando o Radar associa uma captura a um imóvel, deve conseguir explicar o motivo.
- Quais sinais coincidiram.
- Quais fontes foram comparadas.
- Quais sinais divergiram.
- Qual nível de confiança foi atribuído.
- Se houve validação manual.
- Se a associação foi posteriormente corrigida.

# 26. Exemplo Completo

A Caixa publica um apartamento por R$ 191.651,31. Um leiloeiro também publica a unidade por valor diferente. As duas capturas possuem o mesmo condomínio, unidade e matrícula. O Radar deve criar duas Capturas associadas ao mesmo Imóvel. O preço atual deve ser determinado conforme a oferta vigente, mas os preços anteriores permanecem no histórico. O valuation e a análise econômica devem utilizar a condição específica da oferta escolhida.

| Objeto | Resultado |
|---|---|
| Fonte 1 | Caixa |
| Fonte 2 | Leiloeiro |
| Capturas | 2 |
| Imóvel | 1 |
| Histórico | Preservado |
| Oportunidade | Avaliada conforme oferta/estratégia |
| Conflitos | Registrados |
| Confiança de identidade | Muito alta, se matrícula confirmada |


# 27. Critérios para Criar Novo Imóvel

- Não existe correspondência suficientemente confiável.
- Identificadores indicam ativo distinto.
- Unidade diferente.
- Matrícula diferente.
- Endereço e características incompatíveis.
- Conflito não resolvido impede fusão.
Criar um novo imóvel é reversível no sentido de poder posteriormente ser associado/corrigido, mas o histórico da mudança deve permanecer.

# 28. Critérios para Reabrir uma Oportunidade

- Preço retorna ao patamar de interesse.
- Novo desconto supera gatilho.
- Novo comparável melhora valuation.
- Risco anteriormente impeditivo é resolvido.
- Condição de venda muda.
- Nova estratégia passa a aceitar o imóvel.
- Dados anteriormente desconhecidos são confirmados.

# 29. O que NÃO Fazer

- Não tratar cada anúncio como um imóvel diferente.
- Não apagar histórico quando o preço muda.
- Não fundir somente porque preço e endereço parecem iguais.
- Não escolher silenciosamente entre fontes conflitantes.
- Não usar descrição textual como prova definitiva.
- Não transformar dado ausente em zero.
- Não recalcular toda a história como se a informação atual sempre tivesse existido.
- Não permitir que uma deduplicação errada contamine valuation, risco e score sem rastreabilidade.

# 30. Dados Mínimos para o MVP

- Fonte e data/hora da captura.
- Identificador da publicação, quando houver.
- Preço e status.
- Endereço/localização.
- Tipo e características básicas.
- Sinais de identidade.
- Nível de confiança da identidade.
- Vínculo com imóvel existente ou criação de candidato.
- Histórico de alterações.
- Conflitos e pendências.
- Reprocessamento após alterações materiais.

# 31. Critérios de Aceite

- CA-D16 — Uma mesma unidade publicada em várias fontes pode ser consolidada em um único imóvel.
- CA-D16 — Cada publicação/captura mantém seu histórico próprio.
- CA-D16 — Alterações de preço não criam novos imóveis.
- CA-D16 — Imóveis diferentes no mesmo condomínio não são fundidos.
- CA-D16 — Identidade forte tem prioridade sobre similaridade textual.
- CA-D16 — Casos ambíguos podem permanecer como candidatos.
- CA-D16 — Conflitos de fontes são registrados e explicáveis.
- CA-D16 — A consolidação possui nível de confiança.
- CA-D16 — Uma nova captura pode alterar a visão vigente sem apagar o passado.
- CA-D16 — Eventos materiais podem disparar reprocessamento econômico.
- CA-D16 — Uma captura encerrada não apaga o imóvel.
- CA-D16 — Uma oportunidade pode nascer, desaparecer e reaparecer ao longo do ciclo de vida.
- CA-D16 — Correções de associação são auditáveis.
- CA-D16 — Dados originais permanecem preservados.
- CA-D16 — Novas fontes podem ser incorporadas ao modelo conceitual.

# 32. Relação com os Documentos Anteriores


| Documento | Relação com o D16 |
|---|---|
| 5 — Requisitos | Define a jornada funcional. |
| 6 — Modelo de Dados | Define Fonte, Captura, Imóvel e Oportunidade. |
| 7 — Workflow | Define estados e eventos. |
| 8 — Parâmetros | Define critérios configuráveis. |
| 9/10 — Módulos | Define funcionalidades. |
| 11 — UX | Define como o investidor visualizará o resultado. |
| 12 — Rastreabilidade | Garante ligação entre requisito e comportamento. |
| 13 — Roadmap | Prioriza captura/qualificação. |
| 14 — Dados e Fontes | Define qualidade, origem e enriquecimento. |
| 15 — Decisão | Usa os dados consolidados para decidir. |


# 33. Próximo Documento

Recomendação: Documento 17 — Especificação Funcional de Mercado, Comparáveis, Valuation e Cálculo do Preço Máximo de Compra. O foco será transformar o imóvel consolidado em valor de mercado confiável, cenários, margem, preço máximo e oportunidade relativa por estratégia.
