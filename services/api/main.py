import os
import sys
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from typing import Optional

import httpx
from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel, Field

sys.path.insert(0, "/app/anomaly_detector")
from detector import AnomalyDetector

sys.path.insert(0, "/app/llm_explainer")
from explainer import explain_anomaly

from routers.alerts import router as alerts_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting OpsPilot...")
    detector = AnomalyDetector()
    await detector.load_or_train()
    app.state.detector = detector
    print("Anomaly detector ready")
    yield
    print("Shutting down OpsPilot")


app = FastAPI(
    title="OpsPilot",
    description="AI-Powered Incident Intelligence",
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(alerts_router)
# Add Prometheus instrumentation (collects metrics on all endpoints)
Instrumentator().instrument(app).expose(app)

class MetricsPayload(BaseModel):
    service:     str
    cpu:         float = Field(ge=0, le=100)
    memory:      float = Field(ge=0, le=100)
    error_rate:  float = Field(ge=0, le=1)
    latency_p99: float = Field(ge=0)
    log_snippet: Optional[str] = None


@app.get("/")
async def root():
    return {"service": "OpsPilot", "status": "running"}


@app.get("/api/health")
async def health_check():
    base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(f"{base_url}/api/tags")
        ollama_status = "reachable" if response.status_code == 200 else "unreachable"
    except Exception:
        ollama_status = "unreachable"
    return {"status": "ok", "ollama": ollama_status}


@app.post("/api/ingest")
async def ingest_metrics(payload: MetricsPayload, request: Request, background_tasks: BackgroundTasks):
    detector = request.app.state.detector
    features = [payload.cpu, payload.memory, payload.error_rate, payload.latency_p99]
    is_anomaly, score = detector.predict(features)
    severity = AnomalyDetector.get_severity(score)
    if is_anomaly:
        background_tasks.add_task(
            explain_anomaly,          # the function
            payload.service,          # arg 1: service
            payload.dict(),           # arg 2: metrics dict
            score,                    # arg 3: anomaly score
            payload.log_snippet or "" # arg 4: log snippet
        )
    return {
        "received": True,
        "service": payload.service,
        "anomaly_detected": is_anomaly,
        "anomaly_score": round(score, 4),
        "severity": severity,            # ← add this
        "message": "Anomaly detected!" if is_anomaly else "All clear",
    }