class MetricPredictor:

    def fit(self, history: list[dict]) -> None:
        # history = [{"timestamp": "...", "value": 35.2}, ...]
        # convert to Prophet DataFrame
        # fit the model
        pass

    def forecast(self, periods: int = 3) -> dict:
        # predict next N steps (each step = 15 minutes)
        # return predicted value, upper bound, lower bound
        # return whether upper bound crosses danger threshold
        pass