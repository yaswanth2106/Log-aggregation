from fastapi.testclient import TestClient
from app.main import app
from app import models

client = TestClient(app)


def test_create_log():
    response = client.post(
        "/logs",
        json={
            "service_name": "test-service",
            "level": "INFO",
            "message": "test log",
            "timestamp": "2026-02-28T18:00:00"
        },
    )

    assert response.status_code == 200


def test_get_logs():
    response = client.get("/logs?service=auth&level=ERROR&page=2&limit=10")
    assert response.status_code == 200