import joblib
import pandas as pd
from difflib import get_close_matches

MODEL_PATH = "../model/river_wqi_model.pkl"
model = joblib.load(MODEL_PATH)

REQUIRED = [
    "Temperature","Dissolved Oxygen","pH",
    "Bio-Chemical Oxygen Demand (mg/L)",
    "Faecal Streptococci (MPN/ 100 mL)",
    "Nitrate (mg/ L)",
    "Faecal Coliform (MPN/ 100 mL)",
    "Total Coliform (MPN/ 100 mL)",
    "Conductivity (mho/ Cm)"
]

def format_input(data):
    df = pd.DataFrame([data])
    formatted = {}
    cols = df.columns.tolist()
    for req in REQUIRED:
        match = get_close_matches(req, cols, n=1, cutoff=0.3)
        formatted[req] = df[match[0]].values[0] if match else 0
    return pd.DataFrame([formatted])

def classify_wqi(value):
    if value < 25: return "Excellent"
    if value < 50: return "Good"
    if value < 75: return "Medium"
    if value < 100: return "Poor"
    return "Very Poor"

def run_water_quality(data):
    df = format_input(data)
    raw_pred = model.predict(df)[0]

    # 🎯 CASE 1 → MODEL RETURNS STRING LIKE "Excellent"
    if isinstance(raw_pred, str):
        return {
            "Predicted_WQI": raw_pred,
            "Quality_Status": raw_pred
        }
    
    # 🎯 CASE 2 → MODEL RETURNS A NUMBER
    raw_pred = float(raw_pred)
    return {
        "Predicted_WQI": round(raw_pred, 2),
        "Quality_Status": classify_wqi(raw_pred)
    }
