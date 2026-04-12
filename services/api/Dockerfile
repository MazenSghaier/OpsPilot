FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc && rm -rf /var/lib/apt/lists/*

COPY api/requirements.txt .

# Install lightweight packages first (cached separately)
RUN pip install --no-cache-dir --timeout=300 \
    fastapi uvicorn[standard] httpx pydantic \
    python-dotenv redis prometheus-fastapi-instrumentator \
    supabase reportlab

# Install heavy ML packages separately
RUN pip install --no-cache-dir --timeout=300 \
    scikit-learn numpy pandas \
    sentence-transformers \
    prophet

COPY api/          .
COPY anomaly_detector/ ./anomaly_detector/
COPY llm_explainer/    ./llm_explainer/

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]