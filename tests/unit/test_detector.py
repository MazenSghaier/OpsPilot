import asyncio
import sys
import pytest

sys.path.insert(0, "/app/anomaly_detector")
from detector import AnomalyDetector


@pytest.fixture(scope="module")
def trained_detector():
    detector = AnomalyDetector()
    asyncio.run(detector.load_or_train())
    return detector


def test_predict_returns_correct_types(trained_detector):
    is_anomaly, score = trained_detector.predict([35, 50, 0.01, 200])
    assert isinstance(is_anomaly, bool)
    assert isinstance(score, float)


def test_normal_metrics_not_anomaly(trained_detector):
    is_anomaly, _ = trained_detector.predict([35, 50, 0.01, 200])
    assert is_anomaly is False


def test_extreme_metrics_are_anomaly(trained_detector):
    is_anomaly, _ = trained_detector.predict([99, 98, 0.45, 9000])
    assert is_anomaly is True


def test_get_severity_critical():
    assert AnomalyDetector.get_severity(-0.40) == "critical"


def test_get_severity_high():
    assert AnomalyDetector.get_severity(-0.25) == "high"


def test_get_severity_medium():
    assert AnomalyDetector.get_severity(-0.15) == "medium"


def test_get_severity_low():
    assert AnomalyDetector.get_severity(-0.05) == "low"


def test_model_not_loaded_raises():
    detector = AnomalyDetector()
    with pytest.raises(RuntimeError):
        detector.predict([35, 50, 0.01, 200])