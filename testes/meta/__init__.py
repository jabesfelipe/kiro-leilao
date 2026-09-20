"""Meta-testes `MT-01` a `MT-16` (`R73.10`, `D101`).

Um meta-teste não exercita comportamento: ele confronta **declaração contra declaração** e
falha nomeando o elemento órfão — a propriedade sem teste, o item de checklist sem cobertura,
a regra sem implementação, a pergunta de fechamento sem requisito, a entidade sem titular, a
categoria de erro sem código, a tela sem estado. É o que os torna baratos e é o que os torna
eficazes (`D101`).

Um arquivo por meta-teste, `test_mt_01.py` a `test_mt_16.py`. `MT-11` — convenção de idioma —
é o único que percorre a árvore sintática do código e vive na mesma barreira de integração que
`ruff` e `mypy --strict` desde o passo 1 de `D91`.

Dois grupos, pela natureza do que verificam:

- **Sujeito inteiramente na especificação** — `MT-01` (rastreabilidade das 262 propriedades),
  `MT-06` (prioridade dos 126 requisitos) e `MT-12` (as quarenta perguntas de fechamento) —,
  mais `MT-09`, cujo sujeito são os enums já entregues. Estes verificam conteúdo existente e
  **passam** hoje;
- **Sujeito na implementação** — os demais. Enquanto o artefato verificado não existe, o
  meta-teste **falha nomeando exatamente o que falta** e o requisito que o exige. A falha é o
  portão: ela cai no dia em que o conteúdo entra.

Nenhum deles falha por erro de importação ou de coleta: a leitura da especificação e a sondagem
dos módulos acontecem dentro do teste, nunca no corpo do módulo, e módulo ausente é resultado
`None` tratado, não exceção.
"""
