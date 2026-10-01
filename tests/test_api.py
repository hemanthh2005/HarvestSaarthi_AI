"""
HarvestSaarthi AI - API Integration Tests
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"


def test_crops_endpoint():
    response = client.get("/api/crops")
    assert response.status_code == 200
    data = response.json()
    assert "Tomato" in data["data"]


def test_markets_endpoint():
    response = client.get("/api/markets")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) > 0


def test_decision_endpoint():
    payload = {
        "crop": "Tomato",
        "quantity_kg": 2000,
        "farmer_location": "Hassan",
        "crop_grade": "Grade A",
        "has_cold_storage": False,
        "has_transport": True,
        "preferred_selling_radius_km": 150,
        "urgency": "HIGH",
        "language": "en"
    }
    response = client.post("/api/decision", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "recommendation_title" in data["data"]
    assert data["data"]["expected_net_realization"] > 0


def test_demo_endpoint():
    response = client.get("/api/demo/tomato")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["demo_id"] == "tomato"


def test_what_if_endpoint():
    payload = {
        "situation": {
            "crop": "Tomato",
            "quantity_kg": 2000,
            "farmer_location": "Hassan"
        },
        "override_quantity_kg": 5000,
        "override_cold_storage": True
    }
    response = client.post("/api/what-if", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
