"""Adaptadores: as implementações dos contratos declarados no núcleo (`R119.2`).

Camada de adaptadores (`R119.1`): aqui, e só aqui, vive o cliente de provedor de modelo de
linguagem, de embedding, de índice vetorial, de armazenamento externo e de agendamento
(`R98.5`). Cada adaptador implementa **um** contrato do núcleo, e a troca de qualquer um deles
não altera o núcleo (`R119.4`) nem o resultado determinístico (`R119.6`).

A direção é única: o adaptador importa o núcleo; o núcleo nunca importa o adaptador (`R119.3`).
Os 9 adaptadores declarados estão em `radar.nucleo.camadas.ADAPTADORES_DECLARADOS`.
"""
