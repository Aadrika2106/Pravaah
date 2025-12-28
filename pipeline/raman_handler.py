import pandas as pd
import os

CSV_PATH = "../data/raman_dataset/raman_merged_labeled.csv"

def run_raman():
    if not os.path.exists(CSV_PATH):
        return {"error": "Raman dataset not found"}

    df = pd.read_csv(CSV_PATH)

    # Use the 'class' column as the detected material/polymer category
    materials = df["class"].dropna().unique().tolist()

    return {
        "status": "Raman data processed",
        "total_samples": len(df),
        "unique_classes_found": len(materials),
        "detected_material_classes": materials[:10]  # show first 10 for clean output
    }
