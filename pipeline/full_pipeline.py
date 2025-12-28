from models.yolo.infer import predict_image_with_viz
from models.raman.infer import predict_polymer
from models.wqi.predict import predict_wqi
from models.forecast.forecast import forecast_wqi
from models.pinn.predict_do import predict_dissolved_oxygen
from models.digital_twin.simulate import run_digital_twin_simulation

def run_pipeline(image, raman_vec, features):
    yolo = predict_image_with_viz(image)
    raman = predict_polymer(raman_vec)
    wqi = predict_wqi(features)
    forecast = forecast_wqi(wqi["wqi_score"])
    pinn = predict_dissolved_oxygen(features)
    twin = run_digital_twin_simulation({
        "pollution_load": yolo["count"] * 10,
        "cleanup_frequency": 0.3,
        "regulation_strictness": 0.6
    }, 30)

    return {
        "yolo": yolo,
        "raman": raman,
        "wqi": wqi,
        "forecast": forecast,
        "pinn": pinn,
        "twin": twin
    }
