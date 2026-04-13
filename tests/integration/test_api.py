import sys
import asyncio
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient

sys.path.insert(0, "/app/anomaly_detector")
sys.path.insert(0, "/app/llm_explainer")

# Mock heavy dependencies before importing app
with patch("sentence_transformers.SentenceTransformer"), \
     patch("explainer.search_similar_incidents", new_callable=AsyncMock):
    from main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


# ── Root ─────────────────────────────────────────────────────────────────────
def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["service"] == "OpsPilot"


# ── Health ────────────────────────────────────────────────────────────────────
def test_health_returns_ok(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "ollama" in data


# ── Ingest — validation ───────────────────────────────────────────────────────
def test_ingest_invalid_cpu_rejected(client):
    """CPU above 100 must return 422."""
    r = client.post("/api/ingest", json={
        "service": "checkout",
        "cpu": 150,           # invalid
        "memory": 50,
        "error_rate": 0.01,
        "latency_p99": 200,
    })
    assert r.status_code == 422


def test_ingest_missing_field_rejected(client):
    """Missing required field must return 422."""
    r = client.post("/api/ingest", json={
        "service": "checkout",
        "cpu": 35,
        # memory missing
        "error_rate": 0.01,
        "latency_p99": 200,
    })
    assert r.status_code == 422


# ── Ingest — normal metrics ───────────────────────────────────────────────────
def test_ingest_normal_metrics(client):
    r = client.post("/api/ingest", json={
        "service": "checkout",
        "cpu": 35,
        "memory": 50,
        "error_rate": 0.01,
        "latency_p99": 200,
    })
    assert r.status_code == 200
    data = r.json()
    assert data["received"] is True
    assert data["anomaly_detected"] is False
    assert "anomaly_score" in data
    assert "severity" in data


# ── Ingest — anomaly ──────────────────────────────────────────────────────────
def test_ingest_anomaly_detected(client):
    r = client.post("/api/ingest", json={
        "service": "checkout",
        "cpu": 99,
        "memory": 98,
        "error_rate": 0.45,
        "latency_p99": 9000,
    })
    assert r.status_code == 200
    data = r.json()
    assert data["anomaly_detected"] is True
    assert data["severity"] in ["high", "critical"]


# ── Ingest — response shape ───────────────────────────────────────────────────
def test_ingest_response_has_all_fields(client):
    r = client.post("/api/ingest", json={
        "service": "auth",
        "cpu": 40,
        "memory": 55,
        "error_rate": 0.02,
        "latency_p99": 300,
    })
    data = r.json()
    for field in ["received", "service", "anomaly_detected",
                  "anomaly_score", "severity", "message"]:
        assert field in data


# ── Predict — not enough data ─────────────────────────────────────────────────
def test_predict_insufficient_data(client):
    """Fresh service with no history should return graceful message."""
    with patch("routers.predict.aioredis") as mock_redis:
        mock_client = AsyncMock()
        mock_client.lrange = AsyncMock(return_value=[])
        mock_client.aclose = AsyncMock()
        mock_redis.from_url.return_value = mock_client

        r = client.get("/api/predict/nonexistent-service")
        assert r.status_code == 200
        assert r.json()["will_breach"] is False
        assert "message" in r.json()


# ── Alerts ────────────────────────────────────────────────────────────────────
def test_alerts_returns_list(client):
    """Alerts endpoint should always return a list even when Redis is empty."""
    with patch("routers.alerts.aioredis") as mock_redis:
        mock_client = AsyncMock()
        mock_client.xrevrange = AsyncMock(return_value=[])
        mock_client.aclose = AsyncMock()
        mock_redis.from_url.return_value = mock_client

        r = client.get("/api/alerts")
        assert r.status_code == 200
        data = r.json()
        assert "alerts" in data
        assert isinstance(data["alerts"], list)