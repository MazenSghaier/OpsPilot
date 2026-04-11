import os
import pickle
from pathlib import Path

import numpy as np
from sklearn.ensemble import IsolationForest

MODEL_PATH = Path(os.getenv("MODEL_PATH", "/app/models/isolation_forest.pkl"))
CONTAMINATION = float(os.getenv("ANOMALY_CONTAMINATION", "0.05"))


def _generate_training_data(n: int = 2000) -> np.ndarray:
    rng = np.random.default_rng(42)

    cpu        = rng.normal(loc=35,  scale=12, size=n).clip(1, 80)
    memory     = rng.normal(loc=50,  scale=15, size=n).clip(5, 85)
    error_rate = rng.beta(a=1, b=50,           size=n)        # mostly near 0
    latency    = rng.normal(loc=200, scale=60, size=n).clip(10, 500)

    return np.column_stack([cpu, memory, error_rate, latency])


class AnomalyDetector:

    def __init__(self):
        self._model: IsolationForest | None = None

    async def load_or_train(self):
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

        if MODEL_PATH.exists():
            with open(MODEL_PATH, "rb") as f:
                self._model = pickle.load(f)
            print(f"Loaded model from {MODEL_PATH}")
        else:
            await self._train()

    async def _train(self):
        print("Training Isolation Forest...")
        X = _generate_training_data()

        self._model = IsolationForest(
            n_estimators=200,
            contamination=CONTAMINATION,
            random_state=42,
            n_jobs=-1,
        )
        self._model.fit(X)

        with open(MODEL_PATH, "wb") as f:
            pickle.dump(self._model, f)
        print(f"Model trained and saved to {MODEL_PATH}")

    def predict(self, features: list[float]) -> tuple[bool, float]:
        if self._model is None:
            raise RuntimeError("Model not loaded. Call load_or_train() first.")

        X = np.array(features).reshape(1, -1)

        label = self._model.predict(X)[0]        # returns 1 or -1
        score = self._model.score_samples(X)[0]  # returns a float

        is_anomaly = bool(label == -1)
        return is_anomaly, float(score)
    
    @staticmethod
    def get_severity(score: float) -> str:
        if score < -0.35:
            return "critical"
        elif score < -0.2:
            return "high"
        elif score < -0.1:
            return "medium"
        else:
            return "low"
