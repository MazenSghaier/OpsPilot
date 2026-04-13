import sys
import pytest

sys.path.insert(0, "/app/predictor")
from predictor import MetricPredictor

from datetime import datetime, timedelta


def _make_history(n=20, base=40.0):
    """Generate n synthetic metric readings."""
    now = datetime.utcnow()
    return [
        {
            "timestamp": (now - timedelta(minutes=(n - i) * 15)).isoformat(),
            "value": base + i * 0.5,
        }
        for i in range(n)
    ]


def test_fit_does_not_raise():
    p = MetricPredictor()
    p.fit(_make_history())


def test_forecast_returns_expected_keys():
    p = MetricPredictor()
    p.fit(_make_history())
    result = p.forecast(periods=3, threshold=90.0)
    for key in ["predicted_value", "upper_bound", "lower_bound",
                "will_breach", "threshold", "minutes_ahead"]:
        assert key in result


def test_forecast_minutes_ahead():
    p = MetricPredictor()
    p.fit(_make_history())
    result = p.forecast(periods=4)
    assert result["minutes_ahead"] == 60


def test_forecast_will_breach_true():
    """Rising metric heading above threshold should trigger breach."""
    p = MetricPredictor()
    p.fit(_make_history(n=20, base=85.0))  # starts at 85, rises
    result = p.forecast(periods=3, threshold=88.0)
    assert result["will_breach"] is True


def test_forecast_will_breach_false():
    """Stable low metric should not breach a high threshold."""
    p = MetricPredictor()
    p.fit(_make_history(n=20, base=20.0))
    result = p.forecast(periods=3, threshold=90.0)
    assert result["will_breach"] is False


def test_forecast_before_fit_raises():
    p = MetricPredictor()
    with pytest.raises(ValueError):
        p.forecast()