"""Testes de propriedade — um arquivo por propriedade.

Convenção obrigatória, verificada por `MT-02`:

- nome do arquivo: `test_propriedade_NNN.py`, com `NNN` na faixa de 001 a 262 e a
  numeração do design como chave; um arquivo por propriedade, sem exceção — é isso
  que torna as 262 tarefas de propriedade independentes e paralelizáveis;
- etiqueta em cada teste, no formato exato:

      Feature: radar-imobiliario-especificacao-completa, Property {n}: {texto}

- mínimo de 100 iterações por propriedade (`max_examples=100` no perfil `dev`, que é
  o padrão);
- `deadline` desativado apenas onde a operação é legitimamente lenta, com a
  justificativa escrita no próprio teste — nunca nos perfis.

O diretório nasce sem testes de propósito: cada uma das 262 propriedades é tarefa
própria e traz o seu único arquivo.
"""
