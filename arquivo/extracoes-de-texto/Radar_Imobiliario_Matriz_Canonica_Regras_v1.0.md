# Radar_Imobiliario_Matriz_Canonica_Regras_v1.0

RADAR IMOBILIÁRIO — MATRIZ CANÔNICA DE REGRAS
Versão 1.0 — Normalização dos 163 checks para RAG, agentes e motor determinístico
Objetivo: converter o checklist bruto em regras canônicas, mantendo rastreabilidade das perguntas de origem. A matriz é uma ponte entre a Base de Conhecimento e a futura camada de execução.

# 1. Inventário

- 136 checks do Checklist Mestre do Radar.
- 27 perguntas adicionais provenientes das imagens anexadas do livro “O Guia Completo de Leilão de Imóveis”.
- Total bruto: 163 checks/perguntas.
- Regras canônicas propostas nesta versão: 45.
- Uma regra canônica pode receber várias perguntas de checklist. Isso evita duplicação e permite atualização centralizada.

# 2. Princípios de normalização

- Checklist pergunta o que verificar; regra define como interpretar.
- Evidência sustenta o fato; sem evidência suficiente o resultado pode ser DESCONHECIDO/PENDENTE/INCONCLUSIVO.
- BLOCK jurídico prevalece sobre desconto, score, liquidez e estratégia.
- Ocupação é risco de posse/economia, não nulidade automática.
- Processo judicial existente não é BLOCK automático; o objeto, fase e decisões precisam ser analisados.
- “Averbação dos leilões negativos: Em tratamento” é pendência registral, não nulidade automática.
- Avaliação CAIXA é referência; valuation deve usar metodologia e comparáveis independentes.
- Parâmetros históricos do checklist permanecem versionados e configuráveis.
- Toda regra precisa ser explicável e auditável.

# 3. Catálogo de regras canônicas


| ID | Regra | Domínio | Condição/Gatilho | Evidência mínima | Resultado/ação | Prioridade | Score | Observação |
|---|---|---|---|---|---|---|---|---|
| RULE-ID-001 | Identidade e captura | Identidade | A oferta precisa ser identificável e rastreável antes de qualquer análise. | Fonte, banco/leiloeiro, ID, matrícula, comarca, endereço, área e captura original. | Sem identidade confiável → PENDENTE; conflito material → BLOCK. | GATE | Não pontuar até resolver. |  |
| RULE-ID-002 | Matrícula atualizada e titularidade | Registral | A matrícula atual deve permitir confirmar titularidade e atos relevantes. | Certidão atualizada, proprietário, AV/R/atos relevantes. | Ausente/desatualizada → PENDENTE; conflito material → BLOCK. | GATE | Não. |  |
| RULE-JUR-001 | Alienação fiduciária e credor | Jurídico | Identificar contrato/credor fiduciário e sua relação com a propriedade. | Matrícula, contrato, documentos do credor. | Inconsistência → risco jurídico/PENDENTE; impossibilidade de confirmar → não concluir compra. | GATE | Não. |  |
| RULE-JUR-002 | Consolidação da propriedade | Jurídico | Confirmar a consolidação da propriedade em nome do credor quando exigida para o procedimento analisado. | Matrícula atual, ato/averbação e texto do ato. | Não comprovada → BLOCK/PENDENTE conforme modalidade e fase. | BLOCK | Não. |  |
| RULE-JUR-003 | Constituição em mora | Jurídico | Confirmar constituição em mora e a cadeia documental correspondente. | Documento de constituição, certidão, notificações. | Ausência/irregularidade material → risco jurídico crítico. | BLOCK | Não. |  |
| RULE-JUR-004 | Intimação para purgação da mora | Jurídico | Verificar modalidade, destinatário, endereço, data, recebimento/recusa e eventual edital subsidiário. | Prova de intimação, AR/certidão, edital, documentos do procedimento. | Inconclusivo → PENDENTE; irregularidade material → BLOCK potencial. | BLOCK | Não. |  |
| RULE-JUR-005 | Intimações relativas aos leilões | Jurídico | Verificar comunicações legalmente exigíveis sobre as datas dos leilões aplicáveis. | Comprovantes, certidões, documentos do procedimento. | Ausência de evidência → PENDENTE; irregularidade material → BLOCK. | BLOCK | Não. |  |
| RULE-JUR-006 | Cronologia jurídica do procedimento | Jurídico | A sequência mora → consolidação → leilão deve ser coerente com a modalidade e os documentos. | Matrícula, edital, notificações, datas. | Conflito material → BLOCK/PENDENTE. | BLOCK | Não. |  |
| RULE-JUR-007 | Processos judiciais e liminares | Jurídico | Pesquisar processos e avaliar objeto, fase, decisões e impacto; existência isolada não bloqueia. | Tribunais, processos, decisões, tutelas. | Impacto material sem mitigação → BLOCK; demais → RISCO/PENDENTE. | BLOCK | Não. |  |
| RULE-JUR-008 | Penhora/indisponibilidade de direitos | Jurídico | Identificar constrições atuais e verificar se impedem ou complicam a transferência. | Matrícula, CNIB/ordens quando acessíveis, processos. | Constrição impeditiva → BLOCK; baixa/levantamento comprovado → normal. | BLOCK | Não. |  |
| RULE-JUR-009 | Garantia de dívida de terceiro | Jurídico | Detectar estrutura em que imóvel residencial garante dívida de terceiro e direcionar para análise jurídica específica. | Contrato, matrícula, partes, jurisprudência vigente. | Risco jurídico contextual → PENDENTE/BLOCK conforme evidência. | BLOCK | Não. |  |
| RULE-JUR-010 | Percentual de quitação do financiamento | Jurídico | Registrar percentual quitado como sinal de investigação, nunca como regra isolada de nulidade. | Contrato, saldo, documentos. | Acima do parâmetro → revisão jurídica; resultado depende do caso. | RISK | Não. |  |
| RULE-JUR-011 | Preço do segundo leilão e parâmetro de 50% | Jurídico/Econômico | Detectar preço inferior ao parâmetro histórico do checklist e exigir validação jurídica da modalidade e norma vigente. | Edital, avaliação, preço do segundo leilão, legislação/jurisprudência. | Alerta jurídico; não bloquear só pela porcentagem. | ALERT | Pode afetar confiança. |  |
| RULE-JUR-012 | Averbação de leilões negativos | Registral | Tratar “em tratamento” como pendência registral e investigar capacidade de regularização. | Matrícula atual, exigências cartorárias, edital, documentos. | Em tratamento → PENDENTE; impossibilidade material → BLOCK potencial. | GATE | Reduz confiança; custo entra no TCO. |  |
| RULE-JUR-013 | Contrato AF registrado e consolidação averbada | Registral | Confirmar atos registrais necessários e sua coerência com o leilão. | Matrícula atual. | Ausente/inconsistente → PENDENTE/BLOCK conforme modalidade. | BLOCK | Não. |  |
| RULE-OCC-001 | Situação de ocupação | Ocupação | Determinar desocupado, ocupado pelo devedor, ocupado por terceiro ou desconhecido. | Vistoria, anúncio, informações do banco, condomínio, evidências. | Desconhecido → PENDENTE; ocupado → risco de posse/custo, não nulidade automática. | RISK | Afeta TCO, prazo e liquidez. |  |
| RULE-OCC-002 | Terceiro e cessão de posição contratual | Ocupação | Investigar contrato, origem da posse e efeitos perante o adquirente. | Contrato, matrícula, evidências de posse. | Risco relevante → PENDENTE/RISK; não presumir nulidade. | RISK | Sim. |  |
| RULE-LOC-001 | Locação e registro | Locação | Verificar contrato, prazo, valor, garantia, cláusula de vigência e registro quando aplicável. | Contrato, matrícula, documentos. | Efeito jurídico/operacional relevante → PENDENTE/RISK. | RISK | Sim. |  |
| RULE-LOC-002 | Locação versus garantia fiduciária | Locação | Comparar data e condições da locação com a garantia e avaliar efeitos jurídicos. | Contrato AF, contrato de locação, matrícula. | Conflito → análise jurídica específica. | RISK | Sim. |  |
| RULE-ED-001 | Leitura integral do edital | Edital | O edital é fonte primária das condições da operação e deve ser analisado integralmente. | PDF oficial, versão, hash/captura. | Sem edital → PENDENTE; conflito crítico → BLOCK. | GATE | Não. |  |
| RULE-ED-002 | Responsabilidade por evicção | Edital/Jurídico | Extrair a cláusula de evicção e registrar exatamente a responsabilidade assumida. | Edital/cláusula. | Cláusula desfavorável → aumentar risco e contingência; não inferir proteção. | RISK | Sim. |  |
| RULE-ED-003 | IPTU, condomínio e demais débitos | Custos | Identificar responsável por cada encargo e criar contingência para desconhecidos. | Edital, prefeitura, condomínio, concessionárias. | Responsabilidade desconhecida → contingência/PENDENTE. | COST | Sim. |  |
| RULE-ED-004 | Vaga de garagem e matrícula | Registral | Confirmar se vaga é parte da unidade ou possui matrícula autônoma e se está abrangida. | Matrículas, edital, convenção. | Inconsistência → PENDENTE/BLOCK registral. | GATE | Não. |  |
| RULE-MKT-001 | Comparáveis de venda | Mercado | Construir amostra de comparáveis relevantes, priorizando mesmo condomínio/microárea. | Anúncios, transações quando disponíveis, endereço, área, padrão, data. | Poucos comparáveis → confiança menor; nunca inventar valor. | DATA | Sim. |  |
| RULE-MKT-002 | Comparáveis de aluguel | Mercado | Usar aluguéis comparáveis para validar renda e demanda. | Anúncios, contratos/dados disponíveis, condomínio, tipologia. | Pouca amostra → confiança menor. | DATA | Sim. |  |
| RULE-MKT-003 | Valuation em faixa | Valuation | Produzir conservador/base/otimista e venda rápida; separar avaliação bancária de valor de mercado. | Comparáveis, metodologia, outliers. | Sem robustez → valuation inconclusivo/PENDENTE. | DATA | Sim. |  |
| RULE-MKT-004 | Outliers e qualidade dos comparáveis | Valuation | Excluir/ajustar outliers e registrar metodologia. | Base de comparáveis. | Amostra inconsistente → reduzir confiança. | DATA | Sim. |  |
| RULE-LOC-003 | Qualidade da localização | Localização | Avaliar segurança, serviços, comércio, transporte, acesso e atratividade da microárea. | Dados geográficos, mercado, fontes locais. | Resultado alimenta score/liquidez; não bloquear apenas por um indicador isolado. | SCORE | Sim. |  |
| RULE-FIN-001 | Custo econômico total | Economia | Somar aquisição, comissão, impostos/registro, débitos, reforma, regularização, desocupação, carrying, financiamento, saída e contingência aplicáveis. | Edital, certidões, estimativas, orçamentos, parâmetros. | TCO incompleto → não fechar preço máximo. | GATE | Não. |  |
| RULE-FIN-002 | Desconto líquido | Economia | Calcular 1 - TCO/valor de mercado. | TCO e valuation. | Se valuation pouco confiável, desconto recebe confiança menor. | SCORE | Sim. |  |
| RULE-FIN-003 | Margem de segurança | Economia | Calcular margem entre valor de mercado e TCO e testar cenários. | Valuation, TCO, cenários. | Margem insuficiente → não atende estratégia. | SCORE | Sim. |  |
| RULE-FIN-004 | Preço máximo por estratégia | Economia | Derivar preço máximo respeitando custos, retorno mínimo, risco e estratégia. | Parâmetros da estratégia, TCO, valuation. | Preço ofertado > máximo → DO NOT BUY/BLOCK econômico. | GATE | Não. |  |
| RULE-FIN-005 | Condomínio elevado | Economia/Liquidez | Comparar condomínio com valor do imóvel e imóveis similares e incorporar carrying cost. | Boleto/declaração, comparáveis. | Elevado → penalidade econômica/liquidez; parâmetro configurável. | SCORE | Sim. |  |
| RULE-FIN-006 | Reforma e regularização | Economia | Estimar custo, prazo, contingência e efeito sobre liquidez/valor. | Vistoria, orçamentos, tipologia. | Incerteza → contingência e confiança menor. | COST | Sim. |  |
| RULE-LIQ-001 | Liquidez de venda | Liquidez | Estimar demanda, concorrência, preço e prazo de venda. | Comparáveis, oferta, histórico quando disponível. | Baixa liquidez exige margem maior e pode reprovar estratégia. | SCORE | Sim. |  |
| RULE-LIQ-002 | Liquidez de aluguel | Liquidez | Estimar demanda, aluguel, vacancy e tempo para locar. | Comparáveis, anúncios, mercado local. | Baixa demanda reduz aderência à estratégia de renda. | SCORE | Sim. |  |
| RULE-LIQ-003 | Prazo de carregamento | Liquidez | Modelar tempo até venda/locação e impacto financeiro. | Cenários, carrying, estratégia. | Prazo acima do máximo → DO NOT BUY para a estratégia. | GATE | Não. |  |
| RULE-STR-001 | Aderência à estratégia | Estratégia | Comparar imóvel e tese com estratégia ativa do investidor. | Perfil, estratégia, parâmetros. | Incompatível → DO NOT BUY/monitorar conforme configuração. | GATE | Não. |  |
| RULE-STR-002 | Capital e concentração | Carteira | Verificar ticket, capital disponível e concentração por região/tipo. | Carteira, caixa, parâmetros. | Excesso de concentração → penalidade ou bloqueio configurado. | SCORE | Sim. |  |
| RULE-SCR-001 | Opportunity Score | Score | Calcular score somente após gates críticos e com componentes configurados/versionados. | Desconto líquido, margem, liquidez, localização, risco, renda, valorização, qualidade. | Score baixo → menor prioridade; score alto não supera BLOCK. | SCORE | Não. |  |
| RULE-SCR-002 | Investor Fit e confiança | Score/Confiança | Ajustar oportunidade pela aderência do investidor e confiança dos dados. | Estratégia, carteira, qualidade, evidências. | Confiança baixa limita decisão e pode gerar PENDENTE. | GATE | Sim. |  |
| RULE-DEC-001 | Precedência de decisão | Governança/Decisão | Aplicar precedência: bloqueio jurídico → elegibilidade → qualidade/confiança → economia → estratégia → score → cenário → ação. | Todos os resultados anteriores. | BLOCK sempre prevalece sobre score; desconhecido crítico impede BUY. | DECISION | Não. |  |
| RULE-DEC-002 | Explicabilidade | Decisão | Toda decisão deve apontar tese, evidências, riscos, pendências, condições e próxima ação. | Resultado de regras e evidências. | Sem justificativa rastreável → análise incompleta. | GOV | Não. |  |
| RULE-GOV-001 | Versionamento e reprodutibilidade | Governança | Registrar versão de regras, parâmetros, fontes, data e evidências usadas. | Metadados da análise. | Sem versão → análise não reproduzível. | GOV | Não. |  |
| RULE-MON-001 | Monitoramento e reavaliação | Monitoramento | Recalcular quando preço, status, valuation, risco, evidência, regra ou estratégia mudar. | Eventos e histórico. | Mudança material → reanálise automática. | MONITOR | Não. |  |


# 4. Mapeamento dos 136 checks do Checklist Mestre


| ID origem | Seção | Check | Regra canônica |
|---|---|---|---|
| MC-001 | IDENTIFICAÇÃO | Fonte / banco / leiloeiro identificados | RULE-ID-001 |
| MC-002 | IDENTIFICAÇÃO | Número do imóvel / identificação da oferta | RULE-ID-001 |
| MC-003 | IDENTIFICAÇÃO | Matrícula(s) identificada(s) | RULE-ID-001 |
| MC-004 | IDENTIFICAÇÃO | Comarca / cartório identificados | RULE-ID-001 |
| MC-005 | IDENTIFICAÇÃO | Endereço completo conferido | RULE-ID-001 |
| MC-006 | IDENTIFICAÇÃO | Área / unidade / vagas / características conferidas | RULE-ID-001 |
| MC-007 | IDENTIFICAÇÃO | Captura original preservada | RULE-ID-001 |
| MC-008 | MATRÍCULA E TITULARIDADE | Matrícula atualizada obtida | RULE-ID-002 |
| MC-009 | MATRÍCULA E TITULARIDADE | Proprietário atual conferido | RULE-ID-002 |
| MC-010 | MATRÍCULA E TITULARIDADE | Alienação fiduciária identificada | RULE-JUR-001 |
| MC-011 | MATRÍCULA E TITULARIDADE | Credor fiduciário identificado | RULE-JUR-001 |
| MC-012 | MATRÍCULA E TITULARIDADE | Averbações relevantes analisadas | RULE-JUR-013 |
| MC-013 | MATRÍCULA E TITULARIDADE | Consolidação da propriedade em nome da CAIXA comprovada, quando aplicável | RULE-JUR-002 |
| MC-014 | MATRÍCULA E TITULARIDADE | Data da consolidação registrada | RULE-JUR-013 |
| MC-015 | MATRÍCULA E TITULARIDADE | Ato/averbação registral identificado | RULE-JUR-013 |
| MC-016 | MATRÍCULA E TITULARIDADE | Inconsistências de titularidade inexistentes ou tratadas | RULE-ID-002 |
| MC-017 | CONSTITUIÇÃO EM MORA / NOTIFICAÇÕES | Devedor/fiduciante identificado | RULE-JUR-004 |
| MC-018 | CONSTITUIÇÃO EM MORA / NOTIFICAÇÕES | Constituição em mora localizada | RULE-JUR-003 |
| MC-019 | CONSTITUIÇÃO EM MORA / NOTIFICAÇÕES | Notificação para purgação da mora verificada | RULE-JUR-004 |
| MC-020 | CONSTITUIÇÃO EM MORA / NOTIFICAÇÕES | Data da notificação registrada | RULE-JUR-004 |
| MC-021 | CONSTITUIÇÃO EM MORA / NOTIFICAÇÕES | Meio/endereço/destinatário conferidos | RULE-JUR-004 |
| MC-022 | CONSTITUIÇÃO EM MORA / NOTIFICAÇÕES | Prazo legal aplicável conferido | RULE-JUR-004 |
| MC-023 | CONSTITUIÇÃO EM MORA / NOTIFICAÇÕES | Evidência documental disponível | RULE-JUR-004 |
| MC-024 | CONSTITUIÇÃO EM MORA / NOTIFICAÇÕES | Eventual devolução/recusa/ausência de recebimento analisada | RULE-JUR-004 |
| MC-025 | CONSTITUIÇÃO EM MORA / NOTIFICAÇÕES | Intimações legalmente exigíveis relacionadas ao leilão verificadas | RULE-JUR-004 |
| MC-026 | CONSTITUIÇÃO EM MORA / NOTIFICAÇÕES | Datas e destinatários conferidos | RULE-JUR-004 |
| MC-027 | EDITAL E CRONOLOGIA DO LEILÃO | Edital oficial obtido | RULE-ED-001 |
| MC-028 | EDITAL E CRONOLOGIA DO LEILÃO | 1º leilão identificado | RULE-ED-001 |
| MC-029 | EDITAL E CRONOLOGIA DO LEILÃO | 2º leilão identificado, quando aplicável | RULE-ED-001 |
| MC-030 | EDITAL E CRONOLOGIA DO LEILÃO | Datas e horários conferidos | RULE-ED-001 |
| MC-031 | EDITAL E CRONOLOGIA DO LEILÃO | Resultado dos leilões conhecido | RULE-ED-001 |
| MC-032 | EDITAL E CRONOLOGIA DO LEILÃO | Cronologia: mora → consolidação → leilão coerente | RULE-JUR-006 |
| MC-033 | EDITAL E CRONOLOGIA DO LEILÃO | Matrícula e edital sem conflito material | RULE-ED-001 |
| MC-034 | EDITAL E CRONOLOGIA DO LEILÃO | Regras específicas do edital analisadas | RULE-ED-001 |
| MC-035 | PROCESSOS JUDICIAIS / RISCO DE NULIDADE | Pesquisa judicial realizada | RULE-JUR-007 |
| MC-036 | PROCESSOS JUDICIAIS / RISCO DE NULIDADE | Processos envolvendo devedor analisados | RULE-JUR-007 |
| MC-037 | PROCESSOS JUDICIAIS / RISCO DE NULIDADE | Processos envolvendo imóvel/matrícula analisados | RULE-JUR-007 |
| MC-038 | PROCESSOS JUDICIAIS / RISCO DE NULIDADE | Ações anulatórias/sustação de leilão pesquisadas | RULE-JUR-007 |
| MC-039 | PROCESSOS JUDICIAIS / RISCO DE NULIDADE | Liminares/tutelas identificadas | RULE-JUR-007 |
| MC-040 | PROCESSOS JUDICIAIS / RISCO DE NULIDADE | Decisões relevantes analisadas | RULE-JUR-007 |
| MC-041 | PROCESSOS JUDICIAIS / RISCO DE NULIDADE | Fase atual registrada | RULE-JUR-007 |
| MC-042 | PROCESSOS JUDICIAIS / RISCO DE NULIDADE | Impacto sobre validade do leilão classificado | RULE-JUR-007 |
| MC-043 | PROCESSOS JUDICIAIS / RISCO DE NULIDADE | Processo não tratado como BLOCK automático apenas por existir | RULE-JUR-007 |
| MC-044 | OCUPAÇÃO | Situação de ocupação conhecida | RULE-OCC-001 |
| MC-045 | OCUPAÇÃO | Desocupado confirmado / ocupado / desconhecido | RULE-OCC-001 |
| MC-046 | OCUPAÇÃO | Ocupante identificado, quando possível | RULE-OCC-001 |
| MC-047 | OCUPAÇÃO | Proprietário/devedor ocupa? | RULE-OCC-001 |
| MC-048 | OCUPAÇÃO | Terceiro ocupa? | RULE-OCC-001 |
| MC-049 | OCUPAÇÃO | Inquilino ocupa? | RULE-OCC-001 |
| MC-050 | OCUPAÇÃO | Evidência da ocupação registrada | RULE-OCC-001 |
| MC-051 | OCUPAÇÃO | Custo/prazo de desocupação estimado | RULE-OCC-001 |
| MC-052 | OCUPAÇÃO | Risco de posse separado do risco de nulidade | RULE-OCC-002 |
| MC-053 | LOCAÇÃO / INQUILINO | Existe contrato de locação? | RULE-LOC-001 |
| MC-054 | LOCAÇÃO / INQUILINO | Contrato obtido? | RULE-LOC-002 |
| MC-055 | LOCAÇÃO / INQUILINO | Data de início e término | RULE-LOC-002 |
| MC-056 | LOCAÇÃO / INQUILINO | Valor do aluguel | RULE-LOC-002 |
| MC-057 | LOCAÇÃO / INQUILINO | Garantia | RULE-LOC-002 |
| MC-058 | LOCAÇÃO / INQUILINO | Cláusula de vigência | RULE-LOC-002 |
| MC-059 | LOCAÇÃO / INQUILINO | Registro/averbação na matrícula, quando aplicável | RULE-LOC-002 |
| MC-060 | LOCAÇÃO / INQUILINO | Data do contrato comparada à garantia fiduciária | RULE-LOC-002 |
| MC-061 | LOCAÇÃO / INQUILINO | Efeitos jurídicos da locação avaliados | RULE-LOC-001 |
| MC-062 | LOCAÇÃO / INQUILINO | Impacto em posse, prazo e rentabilidade calculado | RULE-LOC-002 |
| MC-063 | LOCAÇÃO / INQUILINO | Não presumir nulidade do leilão apenas pela existência de inquilino | RULE-LOC-002 |
| MC-064 | DÍVIDAS E ENCARGOS | Condomínio | RULE-ED-003 |
| MC-065 | DÍVIDAS E ENCARGOS | IPTU | RULE-ED-003 |
| MC-066 | DÍVIDAS E ENCARGOS | Água/luz/outros encargos | RULE-ED-003 |
| MC-067 | DÍVIDAS E ENCARGOS | Débitos informados pela CAIXA | RULE-ED-003 |
| MC-068 | DÍVIDAS E ENCARGOS | Responsabilidade por cada débito identificada | RULE-ED-003 |
| MC-069 | DÍVIDAS E ENCARGOS | Contingência criada para valores desconhecidos | RULE-ED-003 |
| MC-070 | MERCADO / VALUATION | Comparáveis suficientes | RULE-MKT-001 |
| MC-071 | MERCADO / VALUATION | Preferência por mesmo condomínio quando possível | RULE-MKT-001 |
| MC-072 | MERCADO / VALUATION | Preço/m² comparado | RULE-MKT-001 |
| MC-073 | MERCADO / VALUATION | Conservador/base/otimista | RULE-MKT-003 |
| MC-074 | MERCADO / VALUATION | Valor de venda rápida | RULE-MKT-003 |
| MC-075 | MERCADO / VALUATION | Confiança do valuation | RULE-MKT-003 |
| MC-076 | MERCADO / VALUATION | Anomalias/outliers tratados | RULE-MKT-004 |
| MC-077 | ECONOMIA DA OPERAÇÃO | Preço de aquisição | RULE-FIN-001 |
| MC-078 | ECONOMIA DA OPERAÇÃO | ITBI/registro/escritura aplicáveis | RULE-FIN-001 |
| MC-079 | ECONOMIA DA OPERAÇÃO | Comissão do leiloeiro | RULE-FIN-001 |
| MC-080 | ECONOMIA DA OPERAÇÃO | Débitos/contingências | RULE-FIN-001 |
| MC-081 | ECONOMIA DA OPERAÇÃO | Reforma | RULE-FIN-006 |
| MC-082 | ECONOMIA DA OPERAÇÃO | Regularização | RULE-FIN-006 |
| MC-083 | ECONOMIA DA OPERAÇÃO | Custo de desocupação | RULE-FIN-006 |
| MC-084 | ECONOMIA DA OPERAÇÃO | Carrying cost | RULE-FIN-001 |
| MC-085 | ECONOMIA DA OPERAÇÃO | Financiamento, se houver | RULE-FIN-001 |
| MC-086 | ECONOMIA DA OPERAÇÃO | Custos de saída | RULE-FIN-001 |
| MC-087 | ECONOMIA DA OPERAÇÃO | Custo econômico total | RULE-FIN-001 |
| MC-088 | ECONOMIA DA OPERAÇÃO | Desconto líquido | RULE-FIN-002 |
| MC-089 | ECONOMIA DA OPERAÇÃO | Margem de segurança | RULE-FIN-003 |
| MC-090 | ECONOMIA DA OPERAÇÃO | Preço máximo por estratégia | RULE-FIN-004 |
| MC-091 | LIQUIDEZ / SAÍDA | Demanda de locação | RULE-LIQ-002 |
| MC-092 | LIQUIDEZ / SAÍDA | Demanda de venda | RULE-LIQ-001 |
| MC-093 | LIQUIDEZ / SAÍDA | Oferta concorrente | RULE-LIQ-001 |
| MC-094 | LIQUIDEZ / SAÍDA | Tempo estimado para alugar | RULE-LIQ-001 |
| MC-095 | LIQUIDEZ / SAÍDA | Tempo estimado para vender | RULE-LIQ-001 |
| MC-096 | LIQUIDEZ / SAÍDA | Preço de saída conservador | RULE-LIQ-001 |
| MC-097 | LIQUIDEZ / SAÍDA | Prazo máximo de carregamento | RULE-LIQ-003 |
| MC-098 | LIQUIDEZ / SAÍDA | Risco de liquidez | RULE-LIQ-001 |
| MC-099 | ESTRATÉGIA DO INVESTIDOR | Renda | RULE-STR-001 |
| MC-100 | ESTRATÉGIA DO INVESTIDOR | Revenda | RULE-STR-001 |
| MC-101 | ESTRATÉGIA DO INVESTIDOR | Valorização | RULE-STR-001 |
| MC-102 | ESTRATÉGIA DO INVESTIDOR | MCMV/baixa renda | RULE-STR-001 |
| MC-103 | ESTRATÉGIA DO INVESTIDOR | Terreno | RULE-STR-001 |
| MC-104 | ESTRATÉGIA DO INVESTIDOR | Apartamento | RULE-STR-001 |
| MC-105 | ESTRATÉGIA DO INVESTIDOR | Casa/sobrado | RULE-STR-001 |
| MC-106 | ESTRATÉGIA DO INVESTIDOR | 1 dormitório | RULE-STR-001 |
| MC-107 | ESTRATÉGIA DO INVESTIDOR | Estratégia efetivamente compatível | RULE-STR-001 |
| MC-108 | ESTRATÉGIA DO INVESTIDOR | Capital disponível | RULE-STR-002 |
| MC-109 | ESTRATÉGIA DO INVESTIDOR | Concentração de carteira avaliada | RULE-STR-002 |
| MC-110 | SCORE E DECISÃO | Opportunity Score calculado | RULE-SCR-001 |
| MC-111 | SCORE E DECISÃO | Investor Fit calculado | RULE-SCR-002 |
| MC-112 | SCORE E DECISÃO | Confiança calculada | RULE-SCR-002 |
| MC-113 | SCORE E DECISÃO | Ajuste por capital/carteira | RULE-SCR-002 |
| MC-114 | SCORE E DECISÃO | Ranking calculado | RULE-DEC-001 |
| MC-115 | SCORE E DECISÃO | Explicação do score registrada | RULE-DEC-002 |
| MC-116 | SCORE E DECISÃO | BUY / BUY IF / MONITOR / DO NOT BUY / BLOCK | RULE-DEC-001 |
| MC-117 | SCORE E DECISÃO | Toda decisão possui evidências e justificativa | RULE-DEC-002 |
| MC-118 | GATE FINAL DE VALIDADE JURÍDICA | CONSOLIDAÇÃO COMPROVADA | RULE-DEC-001 |
| MC-119 | GATE FINAL DE VALIDADE JURÍDICA | MORA/NOTIFICAÇÃO COMPROVADAS OU SUFICIENTEMENTE EVIDENCIADAS | RULE-DEC-001 |
| MC-120 | GATE FINAL DE VALIDADE JURÍDICA | INTIMAÇÕES LEGALMENTE EXIGÍVEIS VERIFICADAS | RULE-DEC-001 |
| MC-121 | GATE FINAL DE VALIDADE JURÍDICA | EDITAL E CRONOLOGIA COERENTES | RULE-DEC-001 |
| MC-122 | GATE FINAL DE VALIDADE JURÍDICA | PROCESSOS SEM IMPACTO MATERIAL OU IMPACTO MITIGADO | RULE-DEC-001 |
| MC-123 | GATE FINAL DE VALIDADE JURÍDICA | Nenhum indício material de nulidade sem tratamento | RULE-DEC-001 |
| MC-124 | GATE FINAL DE VALIDADE JURÍDICA | Ocupação/locação economicamente e juridicamente tratadas | RULE-DEC-001 |
| MC-125 | GATE FINAL DE VALIDADE JURÍDICA | Se qualquer item crítico estiver inconclusivo: PENDENTE/BLOCK, não BUY | RULE-DEC-001 |
| MC-126 | RESULTADO DA ANÁLISE | Tese de investimento escrita em uma frase | RULE-DEC-002 |
| MC-127 | RESULTADO DA ANÁLISE | Principais evidências | RULE-DEC-002 |
| MC-128 | RESULTADO DA ANÁLISE | Principais riscos | RULE-DEC-002 |
| MC-129 | RESULTADO DA ANÁLISE | Pendências | RULE-DEC-002 |
| MC-130 | RESULTADO DA ANÁLISE | Condições para compra | RULE-DEC-002 |
| MC-131 | RESULTADO DA ANÁLISE | Preço máximo de compra | RULE-DEC-002 |
| MC-132 | RESULTADO DA ANÁLISE | Cenário conservador | RULE-DEC-002 |
| MC-133 | RESULTADO DA ANÁLISE | Cenário base | RULE-DEC-002 |
| MC-134 | RESULTADO DA ANÁLISE | Cenário estressado | RULE-DEC-002 |
| MC-135 | RESULTADO DA ANÁLISE | Próxima ação definida | RULE-DEC-002 |
| MC-136 | RESULTADO DA ANÁLISE | Data da análise e versão das regras registradas | RULE-DEC-002 |


# 5. Mapeamento dos 27 checks adicionais das imagens


| ID origem | Domínio | Pergunta | Regra canônica |
|---|---|---|---|
| JUR-CHK-001 | JURÍDICO | Intimação para purgar a mora foi pessoal? | RULE-JUR-004 |
| JUR-CHK-002 | JURÍDICO | Se não foi pessoal, houve intimação por edital? | RULE-JUR-004 |
| JUR-CHK-003 | JURÍDICO | Houve notificação para a data dos dois leilões do art. 27 da Lei nº 9.514/97? | RULE-JUR-005 |
| JUR-CHK-004 | JURÍDICO | Contrato de financiamento com alienação fiduciária está mais de 80% quitado? | RULE-JUR-010 |
| JUR-CHK-005 | JURÍDICO | Bem residencial de pessoa física foi dado em garantia de dívida de terceiro? | RULE-JUR-009 |
| JUR-CHK-006 | JURÍDICO | No segundo leilão, o imóvel é oferecido por menos de 50% da avaliação? | RULE-JUR-011 |
| JUR-CHK-007 | JURÍDICO | Há ação questionando o leilão/procedimento antes da concorrência? | RULE-JUR-007 |
| JUR-CHK-008 | REGISTRAL | Leilões negativos do art. 27 estão averbados na matrícula? | RULE-JUR-012 |
| JUR-CHK-009 | REGISTRAL | Contrato de alienação fiduciária está registrado e consolidação averbada em nome do credor? | RULE-JUR-013 |
| JUR-CHK-010 | JURÍDICO | Direitos do devedor fiduciário foram penhorados/indisponibilizados? | RULE-JUR-008 |
| JUR-CHK-011 | OCUPAÇÃO | Há terceiro ocupando? Houve compra e venda/cessão de posição contratual? | RULE-OCC-002 |
| JUR-CHK-012 | LOCAÇÃO | Há terceiro ocupando com locação? O contrato está registrado na matrícula? | RULE-LOC-001 |
| EDIT-CHK-013 | EDITAL | Edital foi lido integralmente? | RULE-ED-001 |
| EDIT-CHK-014 | EDITAL | Banco se responsabiliza pela evicção de direito? | RULE-ED-002 |
| EDIT-CHK-015 | EDITAL | Responsabilidade por IPTU e condomínio anteriores está clara no edital? | RULE-ED-003 |
| EDIT-CHK-016 | REGISTRAL | Vaga de garagem possui matrícula própria? | RULE-ED-004 |
| FIN-CHK-017 | LIQUIDEZ | Imóvel é muito ilíquido mesmo com desconto? | RULE-LIQ-001 |
| FIN-CHK-018 | CONDOMÍNIO | Condomínio é elevado em relação ao imóvel/padrão regional? | RULE-FIN-005 |
| FIN-CHK-019 | MERCADO | Há comparáveis suficientes de venda e aluguel (idealmente 7–10)? | RULE-MKT-001 |
| FIN-CHK-020 | LOCALIZAÇÃO | Região tem segurança, serviços e acesso adequados? | RULE-LOC-003 |
| FIN-CHK-021 | REFORMA | Grandes obras são necessárias para melhorar liquidez? | RULE-FIN-006 |
| FIN-CHK-022 | RETORNO | Retorno esperado supera Selic + 15% ao ano? | RULE-FIN-004 |
| FIN-CHK-023 | PRAZO | Prazo entre pagamento e recebimento da venda é >= 2 anos? | RULE-LIQ-003 |
| LOG-CHK-024 | LOGÍSTICA | Imóvel está distante da região onde o investidor mora? | RULE-STR-002 |
| LOG-CHK-025 | LOGÍSTICA | Imóvel precisa de grandes obras de manutenção/reforma? | RULE-FIN-006 |
| LOG-CHK-026 | VENDA | É possível vender sem corretor? Há condomínio com portaria? | RULE-LIQ-001 |
| LOG-CHK-027 | INVESTIDOR | Investidor se sente confortável em adquirir imóvel ocupado por família? | RULE-STR-001 |


# 6. Contrato de execução de uma regra

{
  "rule_id": "RULE-JUR-004",
  "name": "Intimação para purgação da mora",
  "domain": "JURIDICO",
  "priority": "BLOCK",
  "inputs": ["dados_do_imovel", "documentos", "matricula", "processos"],
  "required_evidence": ["prova_de_intimacao", "destinatario", "data", "modalidade"],
  "possible_results": ["CONFIRMADO", "NAO_CONFIRMADO", "DESCONHECIDO", "INCONCLUSIVO"],
  "impact": ["LEGAL_RISK", "CONFIDENCE"],
  "blocking": "CONDITIONAL",
  "score_effect": "NONE_DIRECT",
  "explanation_required": true,
  "source_checklist_ids": ["JUR-CHK-001", "JUR-CHK-002"],
  "version": "1.0"
}

# 7. Pipeline de execução

- CAPTURA → NORMALIZAÇÃO → IDENTIDADE → EVIDÊNCIAS
- → GATES JURÍDICOS → EDITAL/CRONOLOGIA → OCUPAÇÃO/LOCAÇÃO
- → DÉBITOS → VALUATION → CUSTO ECONÔMICO TOTAL
- → LIQUIDEZ → ESTRATÉGIA → SCORE → CENÁRIOS
- → DECISÃO → EXPLICAÇÃO → ALERTA/MONITORAMENTO

# 8. Precedência formal

A ordem abaixo deve ser implementada como regra de orquestração e não apenas como orientação textual:
- P0 — Bloqueios jurídicos/registrários críticos.
- P1 — Elegibilidade e identidade do ativo.
- P2 — Qualidade dos dados e confiança.
- P3 — Economia e custo total.
- P4 — Estratégia e perfil do investidor.
- P5 — Opportunity Score / Investor Fit.
- P6 — Cenários e sensibilidade.
- P7 — Ação: BUY / BUY IF / MONITOR / DO NOT BUY / BLOCK.

# 9. Provas de fogo — critérios de avaliação

- Reserva dos Pinhais: reconhecer consolidação anterior, exigir matrícula atualizada, tratar “averbação dos leilões negativos: em tratamento” como pendência e não como BLOCK automático.
- Residencial Milano: reconhecer consolidação recente, mas não inferir que todas as notificações estão comprovadas apenas pela matrícula; recalcular economia e valuation.
- Ouro Verde: reconhecer AV-13 e o texto do ato que menciona notificação regular; distinguir ônus histórico baixado de ônus atual; não aceitar automaticamente a avaliação de R$ 285 mil como valor de mercado.
Uma resposta da IA somente passa no teste quando identifica evidências, incertezas, regras aplicáveis, cálculos relevantes e decisão coerente com a precedência. Não basta produzir um texto plausível.

# 10. Testes mínimos de regressão


| ID | Cenário | Resultado esperado |
|---|---|---|
| REG-001 | Sem consolidação comprovada | Não permitir BUY; PENDENTE/BLOCK conforme modalidade. |
| REG-002 | Consolidação + texto de notificação regular | Reconhecer evidência positiva, sem declarar risco zero. |
| REG-003 | Averbação de leilões negativos em tratamento | PENDENTE registral; investigar regularização. |
| REG-004 | Processo judicial sem impacto material | Não bloquear apenas pela existência. |
| REG-005 | Processo com liminar que atinge o leilão | BLOCK até resolução/mitigação. |
| REG-006 | Imóvel ocupado | Separar posse de validade jurídica; modelar custo/prazo. |
| REG-007 | Poucos comparáveis | Reduzir confiança; não inventar valuation. |
| REG-008 | Score 92 + BLOCK jurídico | Resultado final BLOCK. |
| REG-009 | Avaliação CAIXA acima dos comparáveis | Recalcular valuation independente. |
| REG-010 | TCO desconhecido | Não fechar preço máximo definitivo. |
| REG-011 | Preço abaixo de 50% da avaliação | Gerar alerta; validar norma e modalidade, sem BLOCK automático. |
| REG-012 | Investidor não aceita imóvel ocupado | Estratégia incompatível → DO NOT BUY/MONITOR conforme configuração. |


# 11. RAG versus motor determinístico


| Componente | Responsabilidade | Não deve fazer |
|---|---|---|
| RAG / Vector DB | Recuperar definições, regras, checklist, exceções, casos, evidências e documentação. | Executar sozinho cálculos críticos ou decidir ignorando precedência. |
| LLM / Agente | Interpretar documentos, selecionar regras, formular perguntas, explicar achados e coordenar ferramentas. | Inventar evidências, preencher lacunas como fatos ou superar BLOCK. |
| Rule Engine | Executar condições determinísticas, precedência e classificação. | Interpretar documentos complexos sem evidência estruturada. |
| Calculation Engine | TCO, desconto, margem, yield, preço máximo, cenários. | Escolher estratégia sem parâmetros. |
| Evidence Store | Guardar fonte, trecho, documento, data, confiança e provenance. | Tratar ausência como prova de regularidade. |
| Evaluation / Golden Cases | Medir se o agente reproduz os resultados esperados. | Ser substituído por avaliação subjetiva. |


# 12. Metadados recomendados para cada regra/chunk

rule_id, checklist_id, document_id, section_id, topic, domain, source_type, source_name, source_version, effective_from, effective_to, priority, jurisdiction, entity_type, strategy, evidence_type, confidence_required, blocking, score_effect, formula_id, case_id, parent_rule_id, supersedes_rule_id.

# 13. Critério de qualidade antes de colocar no Vector DB

- Nenhum item crítico sem ID.
- Nenhuma regra jurídica crítica sem fonte/proveniência.
- Nenhuma regra com condição ambígua sem campo de interpretação.
- Nenhuma decisão sem evidência.
- Nenhum parâmetro histórico tratado como universal.
- Nenhum score capaz de ultrapassar BLOCK.
- Todos os Golden Cases devem ter resultado esperado e fatos invalidadores.
- Toda alteração de regra deve gerar nova versão e preservar a anterior para auditoria.

# 14. Próximo passo técnico

Com esta matriz, a próxima etapa é transformar cada RULE-* em objetos versionados e construir o contrato entre Agente → RAG → ferramentas/MCP → Rule Engine → Calculation Engine → Evidence Store → Decision Engine. A implementação deve começar pelos gates jurídicos, TCO/valuation e provas de fogo, antes de expandir para todos os módulos.
