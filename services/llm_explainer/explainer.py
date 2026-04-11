import os
import httpx
from rag import search_similar_incidents


OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")


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

        return data.get("response", "").strip()

    except Exception:
        return "Unable to generate explanation at this time."