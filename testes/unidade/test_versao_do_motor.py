"""Versão do motor e data de corte na fronteira (`R120.1`, `R120.2`, `R120.4`, `R120.5`).

Bloco `1.1-A` do passo 1 de `D91`. Teste **unitário**: o que está em jogo é o **limite exato** da
data de corte, que é o caso que distingue "até a data de corte" de "antes da data de corte" —
evidência observada **na** data é admitida, posterior não. Nenhuma propriedade do design é
substituída aqui; `P21.21` continua sendo a verificação sobre o espaço inteiro de datas.

Junto com o limite, os casos em que o par tem de falhar alto em lugar de aceitar em silêncio: data
e hora ingênua, `datetime` no lugar de data de calendário, e versão republicada sem avanço depois
de a decisão mudar (`R120.2`).
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, date, datetime, timedelta, timezone

import pytest

from radar.nucleo.informado import DESCONHECIDO
from radar.nucleo.versao_do_motor import (
    FUSO_DE_BRASILIA,
    VERSAO_DO_MOTOR_CANONICA,
    DataDeCorte,
    VersaoDoMotor,
    exigir_evidencia_admissivel,
    exigir_publicacao_de_nova_versao,
)

CORTE = DataDeCorte(valor=date(2025, 3, 10))


def _instante(dia: int, hora: int = 12, *, fuso: timezone = FUSO_DE_BRASILIA) -> datetime:
    return datetime(2025, 3, dia, hora, tzinfo=fuso)


# --------------------------------------------------------------------------------------
# O limite exato da data de corte (`R120.5`)
# --------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "observada_em",
    [
        _instante(9),
        _instante(10, 0),  # primeiro instante do dia do corte
        _instante(10, 23),  # último instante do dia do corte
    ],
)
def test_evidencia_ate_a_data_de_corte_e_admitida(observada_em: datetime) -> None:
    """O corte é um dia inteiro: `10` admite tudo observado em `10`, a qualquer hora."""
    assert CORTE.admite(observada_em)
    exigir_evidencia_admissivel(CORTE, observada_em)


@pytest.mark.parametrize("observada_em", [_instante(11, 0), _instante(11), _instante(30)])
def test_evidencia_posterior_a_data_de_corte_nao_e_admitida(observada_em: datetime) -> None:
    """Informação posterior ao corte não entra nesta versão de análise (`SAFE-015`)."""
    assert not CORTE.admite(observada_em)
    with pytest.raises(ValueError, match="posterior à data de corte"):
        exigir_evidencia_admissivel(CORTE, observada_em)


def test_o_dia_do_corte_e_lido_no_fuso_declarado() -> None:
    """Meia-noite de 11 em UTC é ainda o dia 10 em Brasília, e é o dia 10 que decide."""
    meia_noite_em_utc = datetime(2025, 3, 11, 0, 30, tzinfo=UTC)
    assert meia_noite_em_utc.astimezone(FUSO_DE_BRASILIA).date() == date(2025, 3, 10)
    assert CORTE.admite(meia_noite_em_utc)


def test_evidencia_sem_data_de_observacao_nao_e_admitida() -> None:
    """Ausência de data não demonstra anterioridade ao corte (`R120.8`, `SAFE-015`)."""
    assert not CORTE.admite(DESCONHECIDO)
    with pytest.raises(ValueError, match="sem data de observação"):
        exigir_evidencia_admissivel(CORTE, DESCONHECIDO)


def test_data_e_hora_ingenua_e_recusada() -> None:
    """Data sem fuso não determina instante, e instante é o que o corte compara."""
    ingenua = datetime(2025, 3, 10, 12)  # noqa: DTZ001 — o defeito é o objeto do teste
    with pytest.raises(ValueError, match="consciente de fuso"):
        CORTE.admite(ingenua)


def test_data_de_corte_recusa_instante_no_lugar_de_data_de_calendario() -> None:
    """`datetime` é subclasse de `date` e passaria em silêncio com outra semântica."""
    with pytest.raises(TypeError, match="data de calendário"):
        DataDeCorte(valor=datetime(2025, 3, 10, tzinfo=FUSO_DE_BRASILIA))


# --------------------------------------------------------------------------------------
# Versão do motor (`R120.1`, `R120.2`)
# --------------------------------------------------------------------------------------


def test_a_versao_canonica_de_plt_003_e_1_0_0() -> None:
    assert VersaoDoMotor(maior=1, menor=0, correcao=0) == VERSAO_DO_MOTOR_CANONICA
    assert str(VERSAO_DO_MOTOR_CANONICA) == "1.0.0"
    assert VersaoDoMotor.a_partir_do_texto("1.0.0") == VERSAO_DO_MOTOR_CANONICA


@pytest.mark.parametrize("texto", ["1.0", "1.0.0.1", "1.0.x", "v1.0.0", "-1.0.0", ""])
def test_texto_que_nao_e_versao_semantica_falha(texto: str) -> None:
    with pytest.raises(ValueError, match=r"versão do motor|componente de versão"):
        VersaoDoMotor.a_partir_do_texto(texto)


def test_a_ordem_entre_versoes_e_semantica() -> None:
    assert VersaoDoMotor(maior=1, menor=0, correcao=0) < VersaoDoMotor(maior=1, menor=0, correcao=1)
    assert VersaoDoMotor(maior=1, menor=9, correcao=9) < VersaoDoMotor(maior=2, menor=0, correcao=0)


def test_decisao_alterada_exige_versao_maior() -> None:
    """`R120.2`: republicar a mesma versão deixaria duas decisões no mesmo motor."""
    anterior = VERSAO_DO_MOTOR_CANONICA
    exigir_publicacao_de_nova_versao(
        anterior, VersaoDoMotor(maior=1, menor=1, correcao=0), decisao_alterada=True
    )
    with pytest.raises(ValueError, match="exige publicar versão do motor maior"):
        exigir_publicacao_de_nova_versao(anterior, anterior, decisao_alterada=True)
    with pytest.raises(ValueError, match="exige publicar versão do motor maior"):
        exigir_publicacao_de_nova_versao(
            anterior, VersaoDoMotor(maior=0, menor=9, correcao=9), decisao_alterada=True
        )


def test_mudanca_que_nao_altera_decisao_nao_exige_nova_versao() -> None:
    anterior = VERSAO_DO_MOTOR_CANONICA
    exigir_publicacao_de_nova_versao(anterior, anterior, decisao_alterada=False)


@pytest.mark.parametrize("componente", ["maior", "menor", "correcao"])
def test_componente_de_versao_negativo_falha(componente: str) -> None:
    componentes = {"maior": 1, "menor": 0, "correcao": 0} | {componente: -1}
    with pytest.raises(ValueError, match="int não negativo"):
        VersaoDoMotor(**componentes)


def test_a_data_de_corte_e_a_versao_sao_congeladas() -> None:
    """Valor registrado não é alterado depois do registro (`R120.1`, `R120.4`)."""
    with pytest.raises(FrozenInstanceError):
        CORTE.valor = date(2025, 3, 11)  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        VERSAO_DO_MOTOR_CANONICA.maior = 2  # type: ignore[misc]


def test_o_deslocamento_do_fuso_declarado_e_de_tres_horas_a_menos() -> None:
    assert FUSO_DE_BRASILIA.utcoffset(None) == timedelta(hours=-3)
