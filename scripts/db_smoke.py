"""Smoke test de escrita: persiste uma análise real (item 227) no banco.

Cria property + opportunity, roda o Analysis Service e grava o snapshot.
Depois lê de volta e imprime a decisão persistida. Requer conexão ao banco.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from radar.db import repository
from radar.db.models import Analysis, Decision, Property
from radar.db.session import get_session
from radar.domain.enums import Strategy
from radar.services.analysis_service import AnalysisRequest, analyze


def main() -> int:
    req = AnalysisRequest(
        property_id="855553-227",
        strategy=Strategy.REVENDA,
        price=191_651.31,
        market_value=300_000.0,
        registro=3_000.0,
        condominio=5_000.0,
        reforma=10_000.0,
        reserva=5_000.0,
        legal_status="OK",
        confidence=90.0,
        liquidity_score=80.0,
        identity_confidence=90.0,
    )
    out = analyze(req)

    with get_session() as session:
        prop = Property()
        session.add(prop)
        session.flush()
        opp = repository.create_opportunity(
            session, prop.id, external_ref="edital 0031/0326 item 227", min_bid=191_651.31
        )
        row = repository.save_analysis(
            session, opp.id, out.contract, cost=out.cost, decision=out.decision
        )
        analysis_id = row.id
        opp_id = opp.id

    # lê de volta numa nova sessão
    with get_session() as session:
        saved = session.get(Analysis, analysis_id)
        dec = session.get(Decision, analysis_id)
        print("=== análise persistida ===")
        print(f"opportunity_id : {opp_id}")
        print(f"analysis_id    : {analysis_id}  (versão {saved.version})")
        print(f"decision       : {saved.decision.value}")
        print(f"economic_cost  : {saved.economic_cost}")
        print(f"net_discount   : {saved.net_discount}")
        print(f"deciding_layer : {dec.deciding_layer}")
        print(f"reasons        : {dec.reasons}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
