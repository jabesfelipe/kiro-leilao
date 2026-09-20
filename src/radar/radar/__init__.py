"""Motor do Radar: a execução recorrente de aquisição, em sua parte determinística (`R106`).

Camada de núcleo (`R119.1`, `radar/radar/**` em `camadas.PACOTES_DO_NUCLEO`): decide o que
capturar, em que ordem e com que idempotência, sem conhecer a estratégia concreta que busca o
dado — esta é adaptador (`R107.4`, `D94`). Nenhum módulo deste pacote importa cliente de modelo de
linguagem, de embedding, de armazenamento externo, de agendamento ou de orquestração de IA
(`R119.3`, `MT-10`).
"""
