# Arquivo — material de origem absorvido

A especificação está **congelada**. A partir deste ponto existe **uma única fonte de verdade**:

- `.kiro/specs/radar-imobiliario-especificacao-completa/requirements.md` — fonte normativa de **negócio**
- `.kiro/specs/radar-imobiliario-especificacao-completa/design.md` — fonte normativa de **engenharia**
- `.kiro/specs/radar-imobiliario-especificacao-completa/tasks.md` — plano de execução

Tudo que está nesta pasta foi **auditado, consolidado e absorvido** por esses três documentos e
está preservado apenas como memória histórica. **Nada aqui é fonte de trabalho.** Divergência
entre qualquer arquivo desta pasta e a spec resolve-se sempre a favor da spec.

## Conteúdo

| Pasta | O que é |
|-------|---------|
| `documentos-de-negocio/` | Os 34 documentos de negócio e arquitetura, o Checklist Mestre, a Matriz Canônica de Regras, a Matriz Mestra de Regras de Decisão, a Base de Conhecimento de IA, a Arquitetura Técnica de IA e a planilha do Método Jabes |
| `especificacoes-anteriores/` | As especificações canônicas internas anteriores (especificação canônica, máquina de estados, modelo de dados) |
| `extracoes-de-texto/` | Texto extraído dos documentos, usado durante a consolidação |
| `revisoes-do-especialista/` | As revisões de produto e de arquitetura que originaram as decisões `D56` a `D104` |

## Por que ficam aqui, e não apagados

A seção **Decisões de Consolidação** (`D1` a `D104`) do `requirements.md` é a memória de auditoria
da absorção: registra cada conflito encontrado, os lados em disputa, a decisão adotada e o motivo.
Esta pasta é o lastro documental dessa trilha — consultável em auditoria, nunca em implementação.

## Regra de uso

Nenhum artefato de código, teste, migração ou documentação pode referenciar esta pasta como fonte.
Mudança de arquitetura depois do congelamento é **mudança explícita de decisão numerada**, com
conflito, resolução e impacto registrados no `requirements.md` (`R126.44`, `R126.45`).
