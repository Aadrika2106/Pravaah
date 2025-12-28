from ultralytics import YOLO
import os

MODEL_PATH = "../yolov8n.pt"
model = YOLO(MODEL_PATH)

def run_yolo(image_path):
    if not os.path.exists(image_path):
        return {"status": "error", "msg": "Image not found", "path": image_path}

    results = model(image_path)
    boxes = results[0].boxes

    count = len(boxes)
    confs = [float(b.conf) for b in boxes]
    avg_conf = round(sum(confs)/len(confs), 3) if confs else 0

    return {
        "microplastic_count": count,
        "avg_confidence": avg_conf,
        "details": [{"cls": int(b.cls), "conf": float(b.conf)} for b in boxes]
    }
