import json
import os
import httpx
from rag import search_similar_incidents
import redis.asyncio as aioredis
from detector import AnomalyDetector

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")

SEVERITY_COLORS = {
    "critical": "#FF0000",
    "high":     "#FF6600",
    "medium":   "#FFA500",
    "low":      "#36A64F",
}

async def explain_anomaly(service, metrics, score, log_snippet) -> str:
    try:

        query = f"{service} cpu={metrics['cpu']} memory={metrics['memory']} error_rate={metrics['error_rate']} latency={metrics['latency_p99']} {log_snippet}"
        similar = await search_similar_incidents(query, limit=3)

        # Extract readable text from results
        similar_texts = []
        for item in similar:
            text = item.get("summary") or str(item)
            similar_texts.append(text)

        if not similar_texts:
            similar_texts = ["No similar incidents found"]

       
        prompt = f"""
You are an expert DevOps engineer specializing in incident response and root cause analysis.

SERVICE: {service}
ANOMALY SCORE: {score}

METRICS:
cpu={metrics['cpu']}%
memory={metrics['memory']}%
error_rate={metrics['error_rate']}
latency={metrics['latency_p99']}ms

LOG SNIPPET:
{log_snippet}

SIMILAR PAST INCIDENTS:
1. {similar_texts[0] if len(similar_texts) > 0 else ""}
2. {similar_texts[1] if len(similar_texts) > 1 else ""}
3. {similar_texts[2] if len(similar_texts) > 2 else ""}

Respond with:
1. LIKELY CAUSE
2. IMMEDIATE ACTION (max 3 bullets)
3. CONFIDENCE: low/medium/high
""".strip()

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": "llama3.2",
                    "prompt": prompt,
                    "stream": False
                }
            )

        data = response.json()
        explanation = data.get("response", "").strip()

        severity = AnomalyDetector.get_severity(score)
        await _store_alert(service, metrics, score, severity, explanation)
        await _send_slack_alert(service, metrics, score, severity, explanation)

        return explanation

    except Exception:
        return "Unable to generate explanation at this time."
    
async def _store_alert(service, metrics, score, severity, explanation):
    redis = aioredis.from_url(os.getenv("REDIS_URL", "redis://redis:6379"))
    try:
        alert = {
            "service": service,
            "anomaly_score": round(score, 4),
            "severity": severity,
            "metrics": metrics,
            "explanation": explanation,
        }
        await redis.xadd("opspilot:alerts", {"data": json.dumps(alert)})
    finally:
        await redis.aclose()

async def _send_slack_alert(service, metrics, score, severity, explanation):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        return  # Slack not configured, skip silently

    color = SEVERITY_COLORS.get(severity, "#808080")

    blocks = {
        "attachments": [
            {
                "color": color,
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"🚨 OpsPilot Alert — {severity.upper()} — {service}"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*Service:*\n{service}"},
                            {"type": "mrkdwn", "text": f"*Severity:*\n{severity.upper()}"},
                            {"type": "mrkdwn", "text": f"*Anomaly Score:*\n{round(score, 4)}"},
                            {"type": "mrkdwn", "text": f"*CPU:*\n{metrics.get('cpu')}%"},
                            {"type": "mrkdwn", "text": f"*Memory:*\n{metrics.get('memory')}%"},
                            {"type": "mrkdwn", "text": f"*Error Rate:*\n{metrics.get('error_rate')}"},
                            {"type": "mrkdwn", "text": f"*p99 Latency:*\n{metrics.get('latency_p99')}ms"},
                        ]
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*🤖 AI Analysis:*\n```{explanation[:2900]}```"
                        }
                    }
                ]
            }
        ]
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(webhook_url, json=blocks)
    except Exception as e:
        print(f"Slack alert failed: {e}")