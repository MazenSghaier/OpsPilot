from prophet import Prophet
import pandas as pd


class MetricPredictor:

    def __init__(self):
        self.model = None

    def fit(self, history: list[dict]) -> None:
        # Convert list of dicts → DataFrame
        df = pd.DataFrame(history)

        # Rename columns to match Prophet requirements
        df = df.rename(columns={
            "timestamp": "ds",
            "value": "y"
        })

        # Ensure datetime format
        df["ds"] = pd.to_datetime(df["ds"])

        # Initialize and fit the model
        self.model = Prophet()
        self.model.fit(df)

    def forecast(self, periods: int = 3, threshold: float = 90.0) -> dict:
        if self.model is None:
            raise ValueError("Model is not fitted yet. Call fit() first.")

        # Create future dataframe (each period = 15 minutes)
        future = self.model.make_future_dataframe(periods=periods, freq="15min")

        # Predict
        forecast = self.model.predict(future)

        # Get the last prediction (furthest in the future)
        last_row = forecast.iloc[-1]

        predicted_value = float(last_row["yhat"])
        upper_bound = float(last_row["yhat_upper"])
        lower_bound = float(last_row["yhat_lower"])

        # Check if it will breach threshold
        will_breach = upper_bound > threshold

        return {
            "predicted_value": predicted_value,
            "upper_bound": upper_bound,
            "lower_bound": lower_bound,
            "will_breach": will_breach,
            "threshold": threshold,
            "minutes_ahead": periods * 15,
        }