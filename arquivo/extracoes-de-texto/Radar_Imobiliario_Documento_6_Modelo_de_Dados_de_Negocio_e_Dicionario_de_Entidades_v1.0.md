# Radar_Imobiliario_Documento_6_Modelo_de_Dados_de_Negocio_e_Dicionario_de_Entidades_v1.0

Radar Imobiliário
Documento 6 — Modelo de Dados de Negócio e Dicionário de Entidades | v1.0
Documento de negócio — sem definição de banco, APIs ou arquitetura.
Princípio: não confundir o imóvel físico com a oportunidade comercial. O mesmo imóvel pode aparecer em várias fontes, ter várias capturas, várias análises e várias decisões.

# 1. Objetivo

Criar um vocabulário único do domínio para que negócio, produto e tecnologia tenham a mesma interpretação sobre os conceitos que formam o Radar.

# 2. Mapa conceitual

FONTE → CAPTURA → IMÓVEL → OPORTUNIDADE → ENRIQUECIMENTO → VALUATION → ECONOMIA → ESTRATÉGIA → REGRAS → SCORE → ANÁLISE → DUE DILIGENCE → DECISÃO → MONITORAMENTO → HISTÓRICO

# 3. Entidades principais


| Entidade | Definição |
|---|---|
| Fonte | origem da informação |
| Captura | fotografia do que a fonte informou em determinado momento |
| Imóvel | ativo físico/documental |
| Oportunidade | tese econômica sobre o imóvel |
| Perfil do imóvel | características consolidadas |
| Localização | contexto geográfico e de mercado |
| Comparável | evidência utilizada no valuation |
| Valuation | estimativa de valor de mercado |
| Custo | componente do custo econômico |
| Cenário | conjunto de premissas econômicas |
| Estratégia | objetivo de investimento |
| Regra | critério de negócio |
| Parâmetro | valor configurável usado por regra |
| Score | pontuação de priorização |
| Risco | ameaça à tese |
| Evidência | informação que sustenta uma conclusão |
| Pendência | questão ainda não resolvida |
| Análise | fotografia da tese em uma data |
| Due Diligence | processo de investigação profunda |
| Decisão | resultado da análise |
| Alerta | evento que exige atenção |
| Histórico | evolução temporal dos conceitos |


# 4. Fonte

Representa quem originou a informação. Deve possuir nome, tipo, abrangência, status, periodicidade, identificador e confiabilidade.

# 5. Captura

É uma fotografia do que uma fonte mostrou em determinado momento. Deve preservar dados originais, data, identificador externo, preço, status e alterações observadas.

# 6. Imóvel

Representa o bem físico/documental e concentra atributos relativamente estáveis.
- Endereço.
- Matrícula.
- Cartório/comarca.
- Unidade/bloco/torre.
- Áreas.
- Tipo.
- Quartos.
- Banheiros.
- Vagas.
- Condomínio/empreendimento.

# 7. Oportunidade

Representa a tese econômica aplicada a um imóvel. Um mesmo imóvel pode ter diferentes oportunidades ao longo do tempo, conforme preço, modalidade, estratégia e contexto.

# 8. Perfil consolidado


| Grupo | Exemplos |
|---|---|
| Identidade | matrícula, unidade, condomínio |
| Localização | endereço, bairro, cidade, classe |
| Físico | área, quartos, banheiros, vagas |
| Comercial | preço, avaliação, status |
| Condominial | condomínio, obras, extraordinárias |
| Ocupacional | ocupação, posse, locação |
| Qualidade | estado, padrão, reforma |


# 9. Localização

Não é apenas endereço. É o contexto de mercado que pode conter classificação A–E, demanda, liquidez, infraestrutura, restrições e preferências do investidor.

# 10. Comparável

Propriedade usada como evidência para estimar valor. Deve registrar origem, data, preço, características, qualidade, aderência e ajustes.

# 11. Valuation

Resultado de uma avaliação de mercado em determinado momento.

| Elemento | Conteúdo |
|---|---|
| Conservador | valor prudente |
| Base | valor mais provável |
| Otimista | valor em cenário favorável |
| Venda rápida | valor de saída acelerada quando aplicável |
| Método | metodologia utilizada |
| Comparáveis | evidências usadas |
| Confiança | qualidade da conclusão |


# 12. Custo

Cada componente do custo econômico deve ser separado e classificado como confirmado, estimado, contingente ou desconhecido.
- Aquisição.
- Comissão.
- Tributos.
- Registro/documentação.
- Dívidas atribuíveis.
- Condomínio.
- Reforma.
- Contingência.
- Carregamento.
- Financiamento quando aplicável.
- Venda quando aplicável.

# 13. Cenário

Conjunto de premissas usado para testar a robustez da oportunidade.

| Cenário | Uso |
|---|---|
| Otimista | melhor execução/mercado |
| Base | premissas mais prováveis |
| Conservador | custos maiores e/ou receita menor |
| Estressado | combinação adversa |


# 14. Estratégia

Define o objetivo econômico da análise.
- Renda.
- Revenda/Flip.
- Valorização.
- MCMV/baixa renda.
- Terreno.
- Apartamento.
- Casa/sobrado.
- 1 dormitório.

# 15. Regra e parâmetro

Regra é o critério; parâmetro é o valor que permite configurá-lo.

| Regra | Parâmetro exemplo |
|---|---|
| Yield mínimo | 0,80% ao mês |
| Margem mínima | 25% |
| Preço máximo | R$ X |
| Classe de localização | A/B/C |
| Liquidez mínima | Média |
| Confiança mínima | Média |
| Score mínimo | 70 |
| Desconto mínimo | 30% |


# 16. Score

Deve guardar score bruto, componentes, pesos, bônus, penalizações, confiança, score final, estratégia e versão das regras utilizadas.

# 17. Risco


| Categoria | Exemplos |
|---|---|
| Jurídico | processos, penhoras, indisponibilidade |
| Documental | divergências, documentos faltantes |
| Ocupacional | posse, ocupação, desocupação |
| Físico | reforma, estrutura, instalações |
| Financeiro | custos incertos, margem insuficiente |
| Mercado | baixa liquidez, comparáveis fracos |
| Localização | fatores que afetam demanda |
| Execução | prazo e complexidade |


# 18. Evidência

Qualquer informação capaz de sustentar uma conclusão. Deve registrar origem, data, referência, confiabilidade e qual conclusão suporta.

# 19. Pendência

Questão ainda não resolvida. Deve possuir descrição, prioridade, status, evidência necessária, impacto e condição de encerramento.

# 20. Análise

Fotografia da avaliação do imóvel em uma data. Deve guardar estratégia, parâmetros, valuation, custos, riscos, score, confiança, pendências e conclusão.

# 21. Due Diligence

Processo de validação documental, jurídica, financeira, física e de mercado. Deve controlar escopo, evidências, pendências, resultado e decisão.

# 22. Decisão


| Resultado | Significado |
|---|---|
| COMPRAR | tese validada |
| COMPRAR SE | condição objetiva pendente |
| MONITORAR | tese interessante sem decisão final |
| NÃO COMPRAR | economia/risco incompatível |
| BLOQUEAR | regra crítica violada |


# 23. Alerta

Evento relevante: queda de preço, mudança de status, aumento de score, novo risco, mudança de valuation, retorno à elegibilidade ou outro gatilho configurado.

# 24. Histórico

Permite responder: o que sabíamos, quais regras estavam vigentes e por que a decisão foi tomada naquela data? Deve preservar alterações relevantes sem apagar o passado.

# 25. Relacionamentos essenciais


| Relação | Regra de negócio |
|---|---|
| Fonte → Captura | uma fonte gera várias capturas |
| Captura → Imóvel | captura identifica ou atualiza imóvel |
| Imóvel → Oportunidade | um imóvel pode ter várias teses ao longo do tempo |
| Oportunidade → Análise | uma oportunidade pode ser reavaliada |
| Análise → Valuation | usa uma avaliação vigente |
| Análise → Custo | possui composição econômica |
| Análise → Estratégia | pode avaliar múltiplas estratégias |
| Estratégia → Regra | possui regras/pesos específicos |
| Regra → Parâmetro | usa valores configuráveis |
| Análise → Score | produz pontuação |
| Análise → Risco | riscos influenciam decisão |
| Due Diligence → Evidência | evidências sustentam verificações |
| Due Diligence → Pendência | controla o que falta |
| Due Diligence → Decisão | gera resultado |
| Oportunidade → Alerta | mudanças geram atenção |
| Todos → Histórico | preservam evolução relevante |


# 26. Tipos de informação


| Tipo | Significado |
|---|---|
| Observado | veio diretamente da fonte |
| Confirmado | validado por evidência |
| Calculado | resulta de fórmula |
| Estimado | inferido por metodologia |
| Inferido | deduzido por regra |
| Desconhecido | ainda não disponível |


# 27. Integridade do domínio

- Captura nunca apaga o dado original anterior.
- Oportunidade nunca perde histórico de decisões.
- Análise identifica estratégia e contexto.
- Score possui confiança.
- Desconhecido permanece explicitamente desconhecido.
- Regra alterada identifica sua versão.
- Exceção é rastreável.
- Decisão possui justificativa e evidências.

# 28. Dicionário resumido


| Entidade | Atributos essenciais |
|---|---|
| Fonte | nome, tipo, status, abrangência, confiabilidade |
| Captura | data, identificador externo, preço, status, dados originais |
| Imóvel | identidade, endereço, matrícula, tipo, áreas, quartos, vagas |
| Oportunidade | tese, status, estratégia, preço-alvo, prioridade |
| Localização | endereço, região, classe, demanda, liquidez |
| Comparável | origem, data, preço, características, qualidade |
| Valuation | valores por cenário, método, comparáveis, confiança |
| Custo | tipo, valor, status, fonte, cenário |
| Estratégia | objetivo, parâmetros, pesos |
| Regra | código, condição, tipo, severidade, vigência |
| Parâmetro | nome, valor, unidade, escopo, vigência |
| Score | bruto, componentes, confiança, final, classificação |
| Risco | categoria, severidade, probabilidade, impacto, status |
| Evidência | origem, data, referência, confiabilidade |
| Pendência | descrição, prioridade, status, encerramento |
| Análise | data, estratégia, valuation, economia, risco, score |
| Due Diligence | escopo, status, pendências, evidências, resultado |
| Decisão | tipo, data, justificativa, condições |
| Alerta | evento, prioridade, data, status |
| Histórico | objeto, versão, data, alteração, motivo |


# 29. Regra de separação

Preço não é oportunidade. Score não é decisão. Valuation não é verdade absoluta. Evidência não é interpretação. O domínio deve preservar essas diferenças.

# 30. Próximo documento

Documento 7 — Workflow de Negócio, Estados, Eventos, Alertas e Ciclo de Vida. Ele detalhará transições, gatilhos, responsabilidades, reavaliações, SLAs conceituais e notificações.
