from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI DevOps CI/CD demo"}


def test_version() -> None:
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data


def test_metrics() -> None:
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_request" in response.text
