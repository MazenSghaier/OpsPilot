# OpsPilot — AI-Powered Incident Intelligence

> Detect infrastructure anomalies with ML, explain them in plain English with a local LLM, and receive proactive alerts — all running free, locally, in Docker.

OpsPilot watches your infrastructure metrics in real time, detects anomalies using Isolation Forest, and uses a locally-running Llama 3.2 model (via Ollama) to generate plain-English incident reports with root cause analysis and remediation steps. No paid AI API. No cloud vendor lock-in.

---

## How it works

```
Ingestion worker → POST /api/ingest → Isolation Forest
                                             │
                                    anomaly detected?
                                             │ yes
                                    RAG: search Supabase for similar past incidents
                                             │
                                    Ollama (llama3.2) generates explanation
                                             │
                          ┌──────────────────┼──────────────────┐
                       Redis Stream       Slack alert       PDF report
                       (alert history)   (webhook)         (on demand)
```

---

## Stack

| Layer | Tool | Notes |
|---|---|---|
| LLM | Ollama + Llama 3.2 | Runs locally in Docker — free, no API key |
| Anomaly detection | scikit-learn Isolation Forest | Trained on synthetic baseline at startup |
| Vector store / RAG | Supabase pgvector | Free hosted tier |
| Embeddings | sentence-transformers `all-MiniLM-L6-v2` | Runs locally, 384 dimensions |
| Time-series forecasting | Facebook Prophet | Predicts metric trajectory (future work) |
| Message queue | Redis Streams | Alert history, async pipeline |
| API | FastAPI | REST API with automatic `/docs` |
| Observability | Prometheus + Grafana | Real request metrics via instrumentator |
| Alerting | Slack Incoming Webhooks | Optional, color-coded by severity |
| Reports | ReportLab PDF | Professional incident report on demand |
| Runtime | Docker Desktop (Windows) | WSL2 backend |

---

## Prerequisites

- **Docker Desktop for Windows** with WSL2 backend enabled
- **A free Supabase account** → https://supabase.com
- **8GB+ RAM** recommended — Llama 3.2 uses ~4GB on CPU

---

## Quick Start

### 1. Clone and configure

```bash
git clone https://github.com/yourname/opspilot.git
cd opspilot
cp .env.example .env
```

Edit `.env` and fill in your Supabase credentials.

---

### 2. Set up Supabase

1. Create a free project at https://supabase.com
2. Go to **SQL Editor** and run:

```sql
-- Enable vector extension
create extension if not exists vector;

-- Incidents table
create table if not exists incidents (
  id         bigserial primary key,
  summary    text,
  service    text,
  severity   text,
  embedding  vector(384),
  created_at timestamptz default now()
);

-- Vector similarity index
create index on incidents using ivfflat (embedding vector_cosine_ops);

-- Similarity search function used by RAG
create or replace function match_incidents(
  query_embedding vector(384),
  match_threshold float,
  match_count     int
)
returns table (
  id         bigint,
  summary    text,
  service    text,
  severity   text,
  similarity float
)
language sql stable as $$
  select
    id, summary, service, severity,
    1 - (embedding <=> query_embedding) as similarity
  from incidents
  where 1 - (embedding <=> query_embedding) > match_threshold
  order by similarity desc
  limit match_count;
$$;
```

3. Go to **Settings → API** and copy your **Project URL** and **anon key** into `.env`

---

### 3. Start the stack

```bash
docker compose up --build
```

First build takes 5–10 minutes (downloading ML dependencies). Subsequent starts are fast.

Services available at:

| Service | URL | Credentials |
|---|---|---|
| OpsPilot API | http://localhost:8000 | — |
| API docs (Swagger) | http://localhost:8000/docs | — |
| Grafana | http://localhost:3000 | admin / admin |
| Prometheus | http://localhost:9090 | — |
| Ollama | http://localhost:11434 | — |

---

### 4. Pull the Llama model

```bash
docker compose exec ollama ollama pull llama3.2
```

Downloads ~2GB once, cached in a Docker volume. Takes 3–5 minutes depending on connection speed.

---

### 5. Verify everything is running

```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "ok",
  "ollama": "reachable"
}
```

---

### 6. Trigger a test anomaly

The ingestion worker sends metrics automatically every 15 seconds (~8% are injected anomalies). To trigger one manually:

```bash
curl -X POST http://localhost:8000/api/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "service": "checkout",
    "cpu": 98.5,
    "memory": 94.1,
    "error_rate": 0.38,
    "latency_p99": 7800,
    "log_snippet": "ERROR connection pool exhausted after 3 retries"
  }'
```

Response (immediate):
```json
{
  "received": true,
  "service": "checkout",
  "anomaly_detected": true,
  "anomaly_score": -0.4021,
  "severity": "critical",
  "message": "Anomaly detected!"
}
```

---

### 7. View AI-generated alerts

Wait 30–120 seconds for Ollama to generate the explanation (CPU inference), then:

```bash
curl http://localhost:8000/api/alerts
```

Each alert contains the service, severity, metrics snapshot, and a plain-English explanation from Llama 3.2 including likely cause, immediate actions, and confidence level.

---

### 8. Generate a PDF incident report

```bash
curl http://localhost:8000/api/reports/latest --output report.pdf
```

Opens as a professional dark-themed PDF with executive summary, severity breakdown table, per-incident metrics, and AI analysis.

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Service status |
| `GET` | `/api/health` | Health check — Ollama reachability |
| `POST` | `/api/ingest` | Submit a metrics snapshot for analysis |
| `GET` | `/api/alerts` | Retrieve recent AI-generated alerts |
| `GET` | `/api/reports/latest` | Download PDF incident report |
| `GET` | `/metrics` | Prometheus metrics scrape endpoint |
| `GET` | `/docs` | Interactive Swagger UI |

### `POST /api/ingest` payload

```json
{
  "service":     "checkout",
  "cpu":         98.5,
  "memory":      94.1,
  "error_rate":  0.38,
  "latency_p99": 7800.0,
  "log_snippet": "optional — recent log lines for LLM context"
}
```

---

## Severity Levels

| Score range | Severity | Action |
|---|---|---|
| above -0.10 | 🟢 low | Monitor and log |
| -0.10 to -0.20 | 🟡 medium | Review within 4 hours |
| -0.20 to -0.35 | 🟠 high | Investigate within 1 hour |
| below -0.35 | 🔴 critical | Immediate action required |

Score is the raw Isolation Forest anomaly score — more negative means more anomalous.

---

## Slack Alerts (optional)

1. Create a Slack app at https://api.slack.com/apps
2. Enable **Incoming Webhooks** → Add to Workspace
3. Copy the webhook URL into `.env`:

```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx/yyy/zzz
```

Restart the stack. Alerts will appear automatically in your Slack channel, color-coded by severity, with the full AI analysis attached.

---

## Project Structure

```
opspilot/
├── services/
│   ├── api/
│   │   ├── main.py               # FastAPI app + lifespan
│   │   ├── routers/
│   │   │   ├── alerts.py         # GET /api/alerts — reads Redis Stream
│   │   │   └── reports.py        # GET /api/reports/latest — PDF generator
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── anomaly_detector/
│   │   └── detector.py           # Isolation Forest — predict() + get_severity()
│   │
│   ├── llm_explainer/
│   │   ├── explainer.py          # Ollama call + Redis storage + Slack webhook
│   │   └── rag.py                # Supabase pgvector semantic search
│   │
│   ├── ingestion/
│   │   ├── worker.py             # Synthetic metrics generator → POST /api/ingest
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── predictor/                # Prophet time-series (future)
│       ├── Dockerfile
│       └── requirements.txt
│
├── infra/
│   ├── prometheus.yml            # Scrape config
│   └── grafana/provisioning/     # Auto-provision Prometheus datasource
│
├── data/
│   ├── runbooks/                 # Markdown runbooks (embed into Supabase)
│   └── sample_logs/              # Synthetic logs for dev/testing
│
├── scripts/                      # Seed utilities
├── tests/                        # pytest unit + integration tests
├── .github/workflows/            # CI pipeline
├── .env.example                  # All environment variables documented
└── docker-compose.yml
```

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SUPABASE_URL` | Yes | Your Supabase project URL |
| `SUPABASE_KEY` | Yes | Your Supabase anon key |
| `OLLAMA_BASE_URL` | No | Default: `http://ollama:11434` |
| `OLLAMA_MODEL` | No | Default: `llama3.2` |
| `REDIS_URL` | No | Default: `redis://redis:6379` |
| `SLACK_WEBHOOK_URL` | No | Slack alerts (leave blank to disable) |
| `ANOMALY_CONTAMINATION` | No | Default: `0.05` (5% expected anomaly rate) |

See `.env.example` for the full list with descriptions.

---

## Running Tests

```bash
docker compose exec api pytest tests/ -v
```

---

## Roadmap

- [ ] Predictor service — Prophet forecasting with proactive alerts
- [ ] Feedback endpoint — `POST /api/alerts/{id}/feedback` for model improvement
- [ ] Grafana dashboard — anomaly score overlay provisioned automatically
- [ ] Azure deployment — Terraform + AKS + Azure OpenAI swap-in
- [ ] GitHub Actions CI — lint, test, build, push to GHCR on merge

---

## Built with

- [FastAPI](https://fastapi.tiangolo.com)
- [Ollama](https://ollama.com)
- [scikit-learn](https://scikit-learn.org)
- [Supabase](https://supabase.com)
- [sentence-transformers](https://www.sbert.net)
- [Grafana](https://grafana.com)
- [ReportLab](https://www.reportlab.com)
