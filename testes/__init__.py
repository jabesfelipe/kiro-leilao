"""Suíte de testes do Radar Imobiliário.

Subdiretórios previstos pela estratégia de teste do design:

- `propriedades/` — um arquivo por propriedade, `test_propriedade_NNN.py`, 1 a 262;
- `geradores/`    — geradores compartilhados do `hypothesis`, um módulo por domínio;
- `meta/`         — meta-testes `MT-01` a `MT-16`;
- `unidade/`      — testes por exemplo e Golden Cases.

Os perfis de execução do `hypothesis` ficam em `perfis_de_execucao.py` e são
registrados pelo `conftest.py` da raiz do repositório, valendo para toda a suíte.
"""
