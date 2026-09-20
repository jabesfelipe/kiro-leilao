"""Contrato único de acesso a modelo de linguagem — componente 28, lado do núcleo (`R98.1`).

Um contrato, e nada mais, separa o produto de qualquer fornecedor de modelo. Trocar de fornecedor
é implementar este `Protocol` e registrar a configuração do ambiente: **nenhuma alteração de
entidade de negócio, de regra, de parâmetro de negócio, de motor determinístico ou de esquema de
dados de negócio** (`R98.4`).

O nome é `ProvedorDeModeloDeLinguagem`, e é o **único** (`D103`, `R98.1`): `LLMProvider`,
`ProvedorLLM`, `ProvedorDeModelo` e as demais variantes são defeito de redação, e `MT-11` falha
nelas nomeando arquivo e linha.

Camada de núcleo: declaração pura. Sem implementação, sem entrada e saída de dados, sem import de
cliente de provedor, de biblioteca de orquestração de IA, de armazenamento ou de agendamento —
`MT-10` percorre o fechamento transitivo de imports e falha com o caminho completo do import
proibido (`R98.5`, `R119.3`).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol

from radar.nucleo.contratos.tipos_dos_contratos import (
    CapacidadeDeModelo,
    EsquemaDeclarado,
    OrcamentoDeExecucaoDeIA,
    PromptVersionado,
    RespostaDeModelo,
    SaidaEstruturada,
)

__all__ = ["ProvedorDeModeloDeLinguagem"]


class ProvedorDeModeloDeLinguagem(Protocol):
    """Contrato **único** de acesso a modelo de linguagem (`R98.1`). Três operações, e nada mais.

    Pré-condição: a chamada parte de um adaptador de `R119.2`, nunca do núcleo nem de um motor
    determinístico (`R98.5`); a tarefa tem provedor e modelo resolvidos por `IA-015` (`R98.6`); a
    entrada não excede `IA-005` tokens (`R99.9`).

    Pós-condição: existe exatamente um `RegistroDeChamadaAProvedor` persistido por chamada, com
    os onze atributos de `R98.11`; a saída estruturada satisfaz o esquema declarado ou é
    rejeitada (`R105.6`); nenhuma interpretação é emitida sem resposta do provedor (`R98.10`).

    Objeto de biblioteca externa não atravessa esta fronteira: LangChain e LangGraph são
    infraestrutura de integração e de orquestração, e não aparecem em assinatura de domínio
    (`R98.7`).

    Indisponibilidade ou excesso de `IA-006` registra erro catalogado conforme `R114.2`, mantém a
    execução retomável conforme `R103.6` e **não** produz interpretação (`R98.10`).

    Modelo local aplica **o mesmo** contrato e registra o provedor como local (`R98.8`); a
    primeira versão usa OpenAI (`IA-001`, `R98.3`). Para as mesmas evidências, os mesmos
    parâmetros e as mesmas versões de regra, o resultado determinístico é idêntico em qualquer
    provedor ou modelo (`R98.9`, `P19.1`).
    """

    def completar(
        self,
        prompt: PromptVersionado,
        entrada: Mapping[str, object],
        orcamento: OrcamentoDeExecucaoDeIA,
    ) -> RespostaDeModelo:
        """Completa texto a partir de um prompt versionado, dentro do orçamento da execução."""
        ...

    def produzir_saida_estruturada(
        self,
        prompt: PromptVersionado,
        entrada: Mapping[str, object],
        esquema: EsquemaDeclarado,
        orcamento: OrcamentoDeExecucaoDeIA,
    ) -> SaidaEstruturada:
        """Produz saída conforme o esquema declarado. Saída não conforme é rejeitada, nunca
        aproveitada em parte (`R105.6`)."""
        ...

    def declarar_capacidade(self) -> CapacidadeDeModelo:
        """Capacidades do modelo (`R98.1`). O chamador decide o que pedir a partir daqui, em
        lugar de descobrir por erro em produção."""
        ...
