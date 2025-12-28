import os
from yolo_handler import run_yolo
from raman_handler import run_raman
from water_quality_handler import run_water_quality
from forecast_handler import run_forecast
from pinn_handler import run_pinn
from digital_twin_handler import run_digital_twin

print("\n🚀 MICROPLASTIC PIPELINE STARTED...\n")

# ================= YOLO =================
img = input("📸 Enter YOLO image path: ").strip()
yolo_output = run_yolo(img)
print("\nYOLO →", yolo_output)

# ================= RAMAN =================
raman_output = run_raman()
print("\nRaman →", raman_output)

# ================= WATER QUALITY =========
sensor_data = {
    "Temperature": 27,
    "Dissolved Oxygen": 7.2,
    "pH": 7.3,
    "Bio-Chemical Oxygen Demand (mg/L)": 3.5,
    "Faecal Streptococci (MPN/ 100 mL)": 50,
    "Nitrate (mg/ L)": 2.3,      # ⚠️ space doesn't matter
    "Faecal Coliform (MPN/ 100 mL)": 90,
    "Total Coliform (MPN/ 100 mL)": 120,
    "Conductivity (mho/ Cm)": 112
}
wq_output = run_water_quality(sensor_data)
print("\nWater Quality →", wq_output)

# ================= FORECAST ===============
forecast_output = run_forecast(60)  # 60 days
print("\nForecast → CSV generated for future prediction\n")

# ================= PINN ====================
pinn_output = run_pinn(sensor_data)
print("\nPINN Prediction →", pinn_output)

# ================= DIGITAL TWIN ============
twin_output = run_digital_twin(25)
print("\nDigital Twin →", twin_output)


print("\n\n🎉🎉🎉 PIPELINE COMPLETED SUCCESSFULLY 🎉🎉🎉\n")
