import torch
import torch.nn as nn
import pandas as pd
import joblib

MODEL = "../model/pinn_wqi.pth"
BASE = "../model/river_pinn_base.pkl"

# Load base model to ensure feature order
base_model = joblib.load(BASE)
REQUIRED = base_model.feature_names_in_.tolist()

# 🧠 EXACT ARCHITECTURE FROM YOUR TRAINED MODEL (confirmed by error logs)
class PINN(nn.Module):
    def __init__(self, input_dim):
        super(PINN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)   # 9 -> 64
        self.fc2 = nn.Linear(64, 32)          # 64 -> 32
        self.out = nn.Linear(32, 1)           # 32 -> 1

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.out(x)

def run_pinn(data: dict):
    """Run PINN prediction with sensor data or WQI features"""
    
    df = pd.DataFrame([data])
    df = df.reindex(columns=REQUIRED, fill_value=0)
    x = torch.tensor(df.values, dtype=torch.float32)

    model = PINN(input_dim=len(REQUIRED))
    model.load_state_dict(torch.load(MODEL, map_location="cpu"), strict=True)
    model.eval()

    with torch.no_grad():
        pred = float(model(x))

    return {
        "PINN_DO_Prediction": round(pred, 2),
        "Impact": "Pollution likely" if pred < 6 else "Safe oxygen range"
    }
