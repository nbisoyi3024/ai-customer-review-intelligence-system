from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Customer Review Intelligence API"
    }


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok"
    }


def test_analyze_empty_review():
    response = client.post(
        "/analyze",
        json={"review": ""}
    )

    assert response.status_code != 200

