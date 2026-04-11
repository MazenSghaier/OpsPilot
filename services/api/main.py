from fastapi import FastAPI
import os
import httpx
from pydantic import BaseModel, Field
from typing import Optional
from contextlib import asynccontextmanager

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: load the model here
    yield
    # shutdown: cleanup here

app = FastAPI(lifespan=lifespan)

class MetricsPayload(BaseModel):
    service: str
    cpu: float = Field(ge=0, le=100)
    memory: float = Field(ge=0, le=100)
    error_rate: float = Field(ge=0)
    latency_p99: float = Field(ge=0)
    log_snippet: Optional[str] = None

@app.get("/")
async def root():
    return {"service": "OpsPilot", "status": "running"}


@app.get("/api/health")
async def health_check():
    # Read from environment variable with fallback
    base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(f"{base_url}/api/tags")

        if response.status_code == 200:
            ollama_status = "reachable"
        else:
            ollama_status = "unreachable"

    except Exception:
        ollama_status = "unreachable"

    return {
        "status": "ok",
        "ollama": ollama_status
    }

@app.post("/api/ingest")
async def ingest_metrics(payload: MetricsPayload):
    return {
        "received": True,
        "service": payload.service,
        "message": "ok"
    }
