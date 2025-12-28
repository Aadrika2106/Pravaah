import joblib
import pandas as pd

MODEL_PATH = "../model/wqi_forecast_model.pkl"

def run_forecast(days):
    model = joblib.load(MODEL_PATH)
    df = model.make_future_dataframe(periods=days)
    forecast = model.predict(df)

    csv_path = f"forecast_next_{days}_days.csv"
    forecast[["ds","yhat","yhat_lower","yhat_upper"]].to_csv(csv_path, index=False)
    
    return {"csv_saved": csv_path}
