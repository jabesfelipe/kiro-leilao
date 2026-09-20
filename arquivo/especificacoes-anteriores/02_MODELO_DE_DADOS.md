# Radar Imobiliário — Modelo de Dados

> **Este documento foi absorvido e não é mais fonte de verdade.**

O modelo físico passou para a seção **Data Models** do `design.md` da spec
`radar-imobiliario-especificacao-completa`, em `.kiro/specs/`. Essa seção é hoje a
única fonte de `db/schema.sql` e dos modelos SQLAlchemy em `src/radar/db/`.

| Assunto | Onde está agora |
|---------|-----------------|
| Dicionário de entidades e colunas | `design.md` da spec, seção *Data Models* |
| Enumerações do banco, espelhando as de domínio, com contagem declarada | `design.md` da spec, seção *Data Models* |
| Itens de integridade (índices únicos, verificações de escala, gatilhos append-only, migrações e seed) | `design.md` da spec, seção *Data Models* |
| Camada de evidências, proveniência e estado do fato | `requirements.md` e `design.md` da spec |
| Separação entre conhecimento vetorial e verdade estruturada | `requirements.md` e `design.md` da spec |

Os princípios de modelagem que este arquivo enunciou — imóvel ≠ oportunidade, nada é
destrutivo, análise é snapshot imutável, toda evidência tem proveniência, fato ≠
interpretação, regras e parâmetros versionados, conhecimento separado do
transacional — continuam valendo e estão declarados na spec como princípios
invioláveis, com propriedades de correção executáveis que os verificam.

A spec é autocontida: não depende deste arquivo, dos documentos em `docs/`, nem de
`.kiro/_extracted/`. Onde houver divergência, **a spec prevalece**.

O conteúdo anterior está preservado no histórico do git.
