"""Remove os dados de smoke test do banco (properties/opportunities/analyses de teste).

Uso: python scripts/db_cleanup.py
Apaga apenas oportunidades cujo external_ref contém 'item 227' e cascata.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sqlalchemy import text

from radar.db.session import get_session


def main() -> int:
    # DELETE direto: o ON DELETE CASCADE do banco remove analyses/costs/decisions.
    with get_session() as session:
        # coleta as properties dessas oportunidades antes de apagar
        prop_ids = [
            r[0]
            for r in session.execute(
                text(
                    "SELECT property_id FROM opportunities "
                    "WHERE external_ref LIKE '%item 227%'"
                )
            ).all()
        ]
        res = session.execute(
            text("DELETE FROM opportunities WHERE external_ref LIKE '%item 227%'")
        )
        n = res.rowcount
        # remove properties que ficaram sem oportunidades
        for pid in prop_ids:
            session.execute(
                text(
                    "DELETE FROM properties p WHERE p.id = :pid "
                    "AND NOT EXISTS (SELECT 1 FROM opportunities o WHERE o.property_id = p.id)"
                ),
                {"pid": pid},
            )
    print(f"Removidas {n} oportunidades de teste e propriedades órfãs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
