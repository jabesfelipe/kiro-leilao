"""Regras canônicas do Radar Imobiliário, expressas como dados versionados.

Camada de núcleo (`R119.1`, `radar/regras/**` em `camadas.PACOTES_DO_NUCLEO`): a regra é
declaração avaliável, nunca ramificação escondida em serviço. Nenhum módulo deste pacote executa
entrada e saída de dados nem importa cliente de modelo de linguagem, de embedding, de
armazenamento externo, de agendamento ou de orquestração de IA (`R119.3`, `MT-10`).
"""
