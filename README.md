# OpsPilot — AI-Powered Incident Intelligence

OpsPilot watches your infrastructure logs and metrics, detects anomalies with ML,
and explains them in plain English using a locally-running LLM (Ollama + Llama 3.2).
No paid AI API required. Vector search powered by Supabase (free tier).

## Stack

| Layer | Tool |
|---|---|
| LLM | Ollama (llama3.2) — runs locally in Docker |
| Vector store | Supabase pgvector (free hosted tier) |
| Anomaly detection | scikit-learn Isolation Forest |
| Time-series | Facebook Prophet |
| Message queue | Redis Streams |
| API | FastAPI |
| Observability | Prometheus + Grafana |
| Runtime | Docker Desktop (Windows) |

## Prerequisites

- Docker Desktop for Windows (with WSL2 backend enabled)
- Python 3.11+ (for running scripts outside Docker)
- A free Supabase account → https://supabase.com

## Quick Start

### 1. Clone and configure

```bash
git clone https://github.com/yourname/opspilot.git
cd opspilot
cp .env.example .env
```

Edit `.env` and fill in your Supabase credentials (see below).

### 2. Set up Supabase

1. Create a free project at https://supabase.com
2. Go to **SQL Editor** and run:

```sql
create extension if not exists vector;

create table if not exists incidents (
  id bigserial primary key,
  summary text,
  service text,
  severity text,
  embedding vector(384),
  created_at timestamptz default now()
);

create index on incidents using ivfflat (embedding vector_cosine_ops);
```

3. Copy your **Project URL** and **anon key** into `.env`

### 3. Pull the Ollama model

```bash
docker compose run --rm ollama ollama pull llama3.2
```

This downloads ~2GB once and caches it in a Docker volume.

### 4. Start the stack

```bash
docker compose up --build
```

Services start at:
- API → http://localhost:8000
- Grafana → http://localhost:3000 (admin / admin)
- Prometheus → http://localhost:9090
- Ollama → http://localhost:11434

### 5. Seed sample data

```bash
docker compose exec api python /app/scripts/seed_vector_store.py
docker compose exec api python /app/scripts/generate_training_data.py
```

### 6. Trigger a test anomaly

```bash
curl -X POST http://localhost:8000/api/ingest \
  -H "Content-Type: application/json" \
  -d '{"service":"checkout","cpu":98.5,"memory":91.2,"error_rate":0.34,"latency_p99":4200}'
```

Check `http://localhost:8000/api/alerts` for the AI-generated explanation.

## Project Structure

```
opspilot/
├── services/
│   ├── ingestion/        # Metrics/log collector (pushes to Redis Streams)
│   ├── anomaly_detector/ # Isolation Forest model
│   ├── predictor/        # Prophet time-series forecasting
│   ├── llm_explainer/    # Ollama + RAG pipeline
│   └── api/              # FastAPI — main entry point
├── data/
│   ├── runbooks/         # Markdown runbooks (auto-embedded into Supabase)
│   └── sample_logs/      # Synthetic logs for dev/testing
├── scripts/              # Seed + data generation utilities
├── infra/                # Terraform for Azure (optional cloud deploy)
├── .github/workflows/    # CI pipeline
└── docker-compose.yml
```

## Environment Variables

See `.env.example` for all variables with descriptions.

## Running Tests

```bash
docker compose exec api pytest tests/ -v
```
