import json
import os
import redis.asyncio as aioredis
from fastapi import APIRouter

router = APIRouter()

def _get_redis():
    return aioredis.from_url(os.getenv("REDIS_URL", "redis://redis:6379"))

@router.get("/api/alerts")
async def get_alerts(limit: int = 20):
    redis = _get_redis()
    try:
        entries = await redis.xrevrange("opspilot:alerts", count=limit)
        alerts = []
        for msg_id, fields in entries:
            try:
                alert = json.loads(fields[b"data"])
                alert["id"] = msg_id.decode()
                alerts.append(alert)
            except Exception:
                continue
        return {"alerts": alerts, "count": len(alerts)}
    finally:
        await redis.aclose()