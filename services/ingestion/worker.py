import asyncio
import random
import httpx
import os

API_URL = os.getenv("API_URL", "http://api:8000")
SERVICES = ["checkout", "auth", "inventory", "payments", "notifications"]

def normal_metrics(service):
    return {
        "service": service,
        "cpu":         round(random.gauss(35, 10), 2),
        "memory":      round(random.gauss(50, 12), 2),
        "error_rate":  round(random.betavariate(1, 60), 4),
        "latency_p99": round(random.gauss(200, 50), 1),
    }

def anomalous_metrics(service):
    base = normal_metrics(service)
    kind = random.choice(["cpu", "memory", "errors", "latency"])
    if kind == "cpu":      base["cpu"] = round(random.uniform(88, 99), 2)
    if kind == "memory":   base["memory"] = round(random.uniform(88, 99), 2)
    if kind == "errors":   base["error_rate"] = round(random.uniform(0.2, 0.45), 4)
    if kind == "latency":  base["latency_p99"] = round(random.uniform(3000, 8000), 1)
    base["log_snippet"] = f"ERROR [{service}] connection pool exhausted"
    return base

async def run():
    print(f"Ingestion worker started → {API_URL}")
    async with httpx.AsyncClient(timeout=10) as client:
        while True:
            service = random.choice(SERVICES)
            # inject anomaly ~8% of the time so alerts appear quickly
            payload = anomalous_metrics(service) if random.random() < 0.08 else normal_metrics(service)
            try:
                r = await client.post(f"{API_URL}/api/ingest", json=payload)
                data = r.json()
                flag = "🚨" if data.get("anomaly_detected") else "✅"
                print(f"{flag} [{service}] score={data.get('anomaly_score')}")
            except Exception as e:
                print(f"failed: {e}")
            await asyncio.sleep(15)

if __name__ == "__main__":
    asyncio.run(run())