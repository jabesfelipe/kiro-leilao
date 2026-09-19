# Requirements Document

Pipeline de Entrada: Captura, Identidade e Gate Jurídico

## Introduction

Esta spec cobre a fatia de entrada do pipeline de análise do Radar Imobiliário: da
captura de uma oferta na fonte (CAIXA, no MVP) até a liberação (ou bloqueio) da
análise pelo gate de validade jurídica.

É a fatia mais crítica do produto porque determina **se uma oportunidade pode sequer
ser analisada economicamente**. A documentação de negócio v1.1 introduziu o gate de
validade jurídica como camada P0 justamente para impedir o padrão perigoso
"imóvel da CAIXA + desconto alto = comprar", que ignora nulidade de procedimento.

### Escopo

Incluído:
- Captura preservada e normalização de ofertas da CAIXA
- Resolução de identidade do imóvel (níveis I0–I4) e deduplicação
- Gate de validade jurídica (camada 0 da precedência canônica)
- Orquestração dessas etapas com curto-circuito em caso de bloqueio
- Registro de evidências, pendências e riscos com proveniência

Não incluído (fatias seguintes):
- Valuation, comparáveis de mercado e Opportunity Score
- Investor Fit, ranking e monitoramento
- Coleta automatizada (scraping) da fonte — aqui o payload cru é insumo de entrada

### Referências normativas

Documentos que prevalecem em caso de dúvida:
- `spec/00_ESPECIFICACAO_CANONICA.md` — precedência, estados de evidência, thresholds
- `spec/01_MAQUINA_DE_ESTADOS.md` — fases do pipeline e estados de decisão
- `spec/02_MODELO_DE_DADOS.md` — entidades e proveniência

---

## Glossary

| Termo | Significado |
|-------|-------------|
| Captura | Snapshot bruto e imutável do que a fonte informou, com hash e data |
| Oferta normalizada | Visão estruturada da captura; campo ausente é UNKNOWN, nunca zero |
| Identidade | Grau de certeza sobre qual imóvel físico a oferta representa (I0–I4) |
| Gate P0 | Camada 0: validade jurídica do procedimento de leilão |
| BLOCK | Impedimento não compensável por desconto, score ou rentabilidade |
| PENDENTE | Falta evidência; não libera BUY, mas não é reprovação definitiva |
| Matrícula | Registro do imóvel no cartório; evidência decisiva de identidade |
| Consolidação | Averbação da propriedade em nome do credor fiduciário |
| Purgação da mora | Oportunidade legal do devedor de quitar a dívida e reverter o processo |

---

## Requirements

### Requisito 1 — Preservação da captura original

**User story:** Como analista, quero que o dado original da fonte seja preservado
intacto, para que qualquer conclusão seja auditável até a origem.

#### Critérios de aceitação

1. WHEN uma oferta é capturada de uma fonte THE SYSTEM SHALL armazenar o payload
   bruto sem alteração, junto com tipo de fonte, nome da fonte e data/hora da captura.
2. WHEN uma captura é registrada THE SYSTEM SHALL calcular um fingerprint estável do
   conteúdo, independente da ordem das chaves do payload.
3. IF duas capturas da mesma fonte possuem o mesmo fingerprint THEN THE SYSTEM SHALL
   tratá-las como a mesma captura e não duplicar o registro.
4. THE SYSTEM SHALL NOT sobrescrever ou apagar uma captura já registrada.

### Requisito 2 — Normalização sem invenção de dados

**User story:** Como analista, quero que campos ausentes na fonte permaneçam
explicitamente desconhecidos, para não confundir ausência de informação com
informação favorável.

#### Critérios de aceitação

1. WHEN uma captura da CAIXA é normalizada THE SYSTEM SHALL extrair identificação,
   localização, dados físicos, dados do certame e situação de ocupação.
2. IF um campo não está presente ou não é interpretável THEN THE SYSTEM SHALL
   registrá-lo como desconhecido (UNKNOWN) e NOT atribuir zero, vazio ou valor default.
3. WHEN valores monetários, áreas, percentuais e datas vêm em formato brasileiro
   THE SYSTEM SHALL interpretá-los corretamente (ex.: "R$ 191.651,31", "47,76 m²",
   "5%", "15/09/2026 10:00").
4. WHEN a fonte indica situação de ocupação THE SYSTEM SHALL distinguir "ocupado" de
   "desocupado" sem ambiguidade de substring.
5. WHEN a normalização termina THE SYSTEM SHALL disponibilizar a lista de campos
   relevantes ausentes, para alimentar pendências.
6. THE SYSTEM SHALL tratar o valor de avaliação informado pela fonte como referência
   informativa, NOT como valor de mercado para decisão.

### Requisito 3 — Resolução de identidade do imóvel

**User story:** Como analista, quero saber o quão certo estou de qual imóvel estou
analisando, porque analisar o imóvel errado invalida todo o resto.

#### Critérios de aceitação

1. WHEN uma oferta normalizada é avaliada THE SYSTEM SHALL classificar a identidade
   em um de cinco níveis: I0 (indefinida), I1 (fraca), I2 (provável), I3 (forte) ou
   I4 (plena).
2. WHERE existe matrícula acompanhada de contexto registral (comarca ou cartório)
   THE SYSTEM SHALL classificar a identidade como I4.
3. WHERE existe matrícula sem contexto registral, OR identificador da fonte com
   endereço completo, THE SYSTEM SHALL classificar a identidade como no máximo I3.
4. WHEN a identidade é resolvida THE SYSTEM SHALL registrar os identificadores
   encontrados com sua confiança relativa.
5. IF a identidade é inferior a I2 THEN THE SYSTEM SHALL impedir a progressão para a
   etapa econômica.
6. IF não há matrícula THEN THE SYSTEM SHALL registrar pendência exigindo certidão
   antes de qualquer liberação de compra.

### Requisito 4 — Deduplicação por força de evidência

**User story:** Como analista, quero que ofertas do mesmo imóvel sejam reconhecidas
como uma só, sem unir imóveis distintos por coincidência.

#### Critérios de aceitação

1. WHEN duas ofertas possuem matrícula THE SYSTEM SHALL usar a matrícula como
   evidência decisiva: iguais são o mesmo imóvel, distintas são imóveis diferentes.
2. WHERE não há matrícula mas há o mesmo identificador da fonte THE SYSTEM SHALL
   tratar como o mesmo imóvel por evidência forte.
3. WHERE há apenas endereço igual THE SYSTEM SHALL exigir compatibilidade de área
   para afirmar identidade, AND retornar indefinido quando a área divergir ou faltar.
4. THE SYSTEM SHALL NOT usar preço, valor de avaliação ou desconto como evidência de
   identidade, em nenhuma circunstância.
5. IF as evidências são insuficientes THEN THE SYSTEM SHALL retornar resultado
   indefinido em vez de adivinhar.

### Requisito 5 — Gate de validade jurídica (camada P0)

**User story:** Como investidor, quero que o sistema bloqueie oportunidades
juridicamente inexecutáveis antes de me mostrar qualquer desconto atraente.

#### Critérios de aceitação

1. WHEN uma análise é executada THE SYSTEM SHALL avaliar o gate de validade jurídica
   ANTES de calcular valuation, desconto, margem ou score.
2. THE SYSTEM SHALL avaliar, no mínimo: consolidação da propriedade, atualização e
   consistência da matrícula, constituição em mora, intimação para purgação da mora,
   coerência cronológica (mora → consolidação → leilão), impacto de processos
   judiciais na validade, e divergências nos dados do certame.
3. IF qualquer verificação apresenta irregularidade material comprovada THEN THE
   SYSTEM SHALL retornar BLOCK.
4. IF qualquer verificação obrigatória está sem evidência THEN THE SYSTEM SHALL
   retornar PENDENTE, AND registrar pendência explicando que ausência de evidência
   não constitui regularidade.
5. WHEN todas as verificações estão comprovadas documentalmente THE SYSTEM SHALL
   retornar OK.
6. THE SYSTEM SHALL NOT permitir que score, desconto, margem, liquidez ou
   rentabilidade convertam um BLOCK em liberação de compra.
7. WHEN o resultado é BLOCK THE SYSTEM SHALL registrar risco de categoria jurídica
   com severidade crítica.

### Requisito 6 — Ocupação como risco de posse

**User story:** Como investidor, quero que ocupação seja tratada como custo e risco
de posse, não como impedimento jurídico, para não descartar boas oportunidades.

#### Critérios de aceitação

1. IF o imóvel está ocupado THEN THE SYSTEM SHALL registrar risco de posse de
   severidade alta AND NOT tratar a ocupação como nulidade do procedimento.
2. IF a situação de ocupação é desconhecida THEN THE SYSTEM SHALL registrar pendência
   para estimativa de custo e prazo de desocupação, sem bloquear a análise.
3. WHEN o imóvel está comprovadamente desocupado THE SYSTEM SHALL NOT registrar risco
   de posse.

### Requisito 7 — Evidência com proveniência obrigatória

**User story:** Como auditor, quero rastrear cada conclusão até o documento que a
sustenta, para poder defender ou revisar a decisão depois.

#### Critérios de aceitação

1. WHEN uma verificação jurídica é registrada THE SYSTEM SHALL gravar evidência com
   identificação da regra, fonte, localização da prova, estado da evidência,
   confiança, autor do registro e data de extração.
2. THE SYSTEM SHALL classificar cada evidência em exatamente um estado: OBSERVED,
   CONFIRMED, CALCULATED, ESTIMATED, INFERRED ou UNKNOWN.
3. THE SYSTEM SHALL NOT permitir que um componente automatizado crie evidência
   inexistente ou promova UNKNOWN para CONFIRMED sem nova prova.
4. WHEN evidências contraditórias existem THE SYSTEM SHALL preservar ambas em vez de
   sobrescrever.

### Requisito 8 — Orquestração com ordem obrigatória e curto-circuito

**User story:** Como responsável técnico, quero que a ordem das etapas seja garantida
pela orquestração, para que nenhuma análise pule o gate jurídico.

#### Critérios de aceitação

1. THE SYSTEM SHALL executar as etapas na ordem: normalização → identidade →
   validade jurídica → economia → decisão → explicação.
2. IF o gate jurídico retorna BLOCK THEN THE SYSTEM SHALL desviar diretamente para a
   decisão, sem executar a etapa econômica.
3. IF a identidade é inferior a I2 THEN THE SYSTEM SHALL desviar diretamente para a
   decisão.
4. WHEN cada etapa conclui THE SYSTEM SHALL atualizar a fase do pipeline conforme a
   máquina de estados canônica.
5. WHEN a análise termina THE SYSTEM SHALL produzir explicação consolidando
   identidade, resultado do gate jurídico, indicadores econômicos disponíveis e a
   camada que determinou a decisão.

### Requisito 9 — Persistência como snapshot imutável

**User story:** Como investidor, quero manter o histórico de como cada oportunidade
foi avaliada ao longo do tempo, sem perder as avaliações anteriores.

#### Critérios de aceitação

1. WHEN uma análise é persistida THE SYSTEM SHALL criar uma nova versão, com
   numeração crescente por oportunidade.
2. THE SYSTEM SHALL NOT sobrescrever análises anteriores da mesma oportunidade.
3. WHEN uma análise é persistida THE SYSTEM SHALL gravar as evidências, pendências,
   riscos, custos e a decisão vinculados àquela versão.
4. WHEN uma análise é persistida THE SYSTEM SHALL registrar a versão de regras e
   parâmetros vigente, para permitir reprodução futura.
5. WHEN uma nova análise da mesma oportunidade é executada THE SYSTEM SHALL poder
   consultar as versões anteriores como contexto, AND NOT tratá-las como evidência
   atual.

---

## Fora de escopo declarado

Para evitar ambiguidade na implementação:

- Coleta automatizada da CAIXA (scraping, download de editais) — o payload cru é
  entrada; a spec não define o coletor.
- Consulta automática a cartório, tribunais ou órgãos de débito — os resultados das
  verificações jurídicas são entradas do gate, vindas de documento ou input manual.
- Cálculo de valuation, score e ranking.
- Interface de usuário.
