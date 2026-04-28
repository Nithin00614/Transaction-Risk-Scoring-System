from fastapi.testclient import TestClient

from inference.app import app

client = TestClient(app)


def test_health():
    response = client.get("/")
    assert response.status_code == 200


def test_score():
    payload = {
        "amount": 100,
        "account_age_days": 200,
        "past_txn_count_24h": 5,
        "hour_of_day": 14,
        "merchant_risk_score": 0.2,
    }
    response = client.post("/score", json=payload)
    assert response.status_code == 200
    assert "risk_score" in response.json()
