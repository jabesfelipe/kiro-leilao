# Radar Imobiliário — Máquina de Estados da Oportunidade

> **Este documento foi absorvido e não é mais fonte de verdade.**

As duas dimensões ortogonais que este arquivo introduziu — fase do pipeline e estado
de decisão — continuam valendo, agora declaradas na spec
`radar-imobiliario-especificacao-completa`, em `.kiro/specs/`:

| Assunto | Onde está agora |
|---------|-----------------|
| Fases do pipeline e transições | `requirements.md` da spec |
| Estados de decisão e as camadas que os produzem | `requirements.md` da spec |
| Estados de monitoramento, reentrada e abandono | `requirements.md` da spec |
| Enumerações fechadas com contagem declarada (`PipelinePhase`, `DecisionState`, `DecisionLayer`, `MonitoringState`) | `design.md` da spec, seção *Data Models* |
| Orquestração das etapas e curto-circuitos | `design.md` da spec |

A spec é autocontida: não depende deste arquivo, dos documentos em `docs/`, nem de
`.kiro/_extracted/`. Onde houver divergência, **a spec prevalece**.

O conteúdo anterior está preservado no histórico do git.
