"""Testes da API FastAPI (endpoints de decisão e análise)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from radar.api.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_analysis_run_item_227_do_not_buy():
    payload = {
        "property_id": "855553-227",
        "strategy": "revenda",
        "price": 191651.31,
        "market_value": 300000.0,
        "registro": 3000.0,
        "condominio": 5000.0,
        "reforma": 10000.0,
        "reserva": 5000.0,
        "legal_status": "OK",
        "confidence": 90,
        "liquidity_score": 80,
        "identity_confidence": 90,
    }
    r = client.post("/analysis/run", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["decision"] == "DO_NOT_BUY"
    assert abs(body["economic_cost"] - 228066.90) < 1.0


def test_analysis_decision_block_wins():
    payload = {
        "legal_status": "BLOCK",
        "confidence": 99,
        "opportunity_score": 99,
        "strategy": "revenda",
    }
    r = client.post("/analysis/decision", json=payload)
    assert r.status_code == 200
    assert r.json()["decision"] == "BLOCK"
