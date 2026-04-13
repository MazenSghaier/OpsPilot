from datetime import datetime

from fastapi import APIRouter
import redis.asyncio as aioredis
import os
import json

from predictor.predictor import MetricPredictor

router = APIRouter()

async def store_metric_history(service: str, value: float, metric: str):
    redis = aioredis.from_url(os.getenv("REDIS_URL", "redis://redis:6379"))
    entry = json.dumps({
        "timestamp": datetime.utcnow().isoformat(),
        "value": value
    })
    try:
        # store as a Redis list, keep last 100 readings per service+metric
        key = f"history:{service}:{metric}"
        await redis.rpush(key, entry)
        await redis.ltrim(key, -100, -1)  # keep only last 100
    finally:
        await redis.aclose()

@router.get("/api/predict/{service}")
async def predict(service: str):
    redis = aioredis.from_url(os.getenv("REDIS_URL", "redis://redis:6379"))

    try:
        key = f"history:{service}:cpu"

        # 🔹 1. Read Redis list
        items = await redis.lrange(key, 0, -1)

        # 🔹 2. Deserialize JSON → dict
        history = [json.loads(item.decode("utf-8")) for item in items]

    finally:
        await redis.aclose()

    # 🔴 3. Handle insufficient data (IMPORTANT)
    if len(history) < 2:
        return {
            "predicted_value": None,
            "upper_bound": None,
            "lower_bound": None,
            "will_breach": False,
            "threshold": 90.0,
            "minutes_ahead": 45,
            "message": "Not enough data to make prediction"
        }

    predictor = MetricPredictor()
    predictor.fit(history)

    result = predictor.forecast(periods=3, threshold=90.0)

    return result