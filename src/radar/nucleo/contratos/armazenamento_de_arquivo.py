"""Contrato de armazenamento de arquivo (`R119.2`, `R86.2`).

O design declara este contrato na tabela de adaptadores de `R119.2` e no diagrama das três camadas
— com disco local e S3 como implementações da primeira versão —, mas **não** declara a sua
assinatura em nenhum bloco de código. As duas operações abaixo são as que os requisitos citados
exigem, e nada além delas:

- `R86.2` exige preservar o arquivo original de forma **permanente e imutável**, abstendo-se de
  substituí-lo, sobrescrevê-lo ou removê-lo em razão da extração. Por isso **não** existe operação
  de remoção nem de sobrescrita neste contrato: a ausência é o que torna a proibição estrutural em
  lugar de disciplina do chamador.
- `R86.7` e `R86.8` exigem entregar o arquivo original **íntegro**, com hash igual ao registrado.
  Por isso a leitura devolve os bytes exatos, sem transformação — o *round-trip* byte a byte de
  `P17.3` vale para binário e para arquivo de zero byte.

A referência é declarada pelo chamador, não devolvida pelo armazenamento: se a localização fosse
gerada pelo adaptador, trocar disco local por S3 mudaria a referência registrada no domínio, e a
troca de adaptador deixaria de ser invisível ao núcleo (`R119.4`, `R119.6`).

Camada de núcleo: declaração pura, sem import de cliente de armazenamento externo (`R119.3`,
`MT-10`).
"""

from __future__ import annotations

from typing import Protocol

__all__ = ["ArmazenamentoDeArquivo"]


class ArmazenamentoDeArquivo(Protocol):
    """Contrato de guarda do arquivo original (`R119.2`, `R86.2`). Duas operações.

    Pré-condição: a referência é declarada pelo chamador e é estável ao longo da vida do
    documento.

    Pós-condição: o conteúdo gravado é recuperável byte a byte, com hash igual ao registrado
    (`R86.7`, `R86.8`, `P17.3`).

    Proibição: substituir, sobrescrever ou remover o arquivo original em razão da extração
    (`R86.2`). Hash recalculado diferente do registrado é falha de integridade com pendência
    crítica, nunca degradação silenciosa (`R86.8`).
    """

    def gravar(self, referencia: str, conteudo: bytes) -> None:
        """Grava o conteúdo sob a referência declarada, de forma permanente e imutável."""
        ...

    def ler(self, referencia: str) -> bytes:
        """Devolve os bytes exatos do que foi gravado, sem transformação."""
        ...
