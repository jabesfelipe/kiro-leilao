"""Configuração de teste que vale para toda a suíte.

Único conteúdo: registrar os quatro perfis de execução do `hypothesis` e carregar o
perfil pedido pelo ambiente. Fica na raiz, e não em `testes/conftest.py`, para valer
também para o que estiver fora de `testes/` enquanto os módulos legados em inglês não
forem reescritos (tarefa 4.1).

As marcas `db`, `fonte_externa` e `provedor_de_modelo` são assunto de `testes/conftest.py`
na tarefa 1.8 e não são declaradas aqui.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ_DO_PROJETO = Path(__file__).resolve().parent

if str(RAIZ_DO_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_DO_PROJETO))

from testes.perfis_de_execucao import registrar_e_carregar  # noqa: E402

PERFIL_ATIVO = registrar_e_carregar()
