from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image

def classify_microplastic_type(width, height):
    """Classify based on aspect ratio"""
    aspect_ratio = max(width, height) / (min(width, height) + 1e-6)
    area = width * height
    
    if aspect_ratio >= 3.5:
        return "fiber"
    elif area <= 1500:
        return "pellet"
    else:
        return "fragment"

COLOR_MAP = {
    "fiber": (255, 0, 0),     # Blue
    "fragment": (0, 255, 255), # Yellow
    "pellet": (0, 255, 0)      # Green
}

def predict_image_with_viz(uploaded_file, conf_threshold=0.50, user_level="Public"):
    """YOLO detection with visualization"""
    try:
        # Load model
        try:
            model = YOLO('models/yolo/best.pt')
        except:
            try:
                model = YOLO('runs/detect/train4/weights/best.pt')
            except:
                return {'error': 'Model not found'}
        
        # Read image
        image = Image.open(uploaded_file).convert("RGB")
        img_np = np.array(image)
        img_draw = img_np.copy()
        
        # Run inference
        results = model(img_np, conf=conf_threshold)[0]
        
        # Process detections
        type_counts = {"fiber": 0, "fragment": 0, "pellet": 0}
        confidences = []
        detections_list = []
        
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            
            width = x2 - x1
            height = y2 - y1
            
            mp_type = classify_microplastic_type(width, height)
            type_counts[mp_type] += 1
            confidences.append(conf)
            
            color = COLOR_MAP[mp_type]
            
            # Draw box
            cv2.rectangle(img_draw, (x1, y1), (x2, y2), color, 2)
            
            # Add label
            label = f"{mp_type.upper()} {conf:.2f}"
            cv2.putText(img_draw, label, (x1, y1 - 8),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            detections_list.append({
                "Type": mp_type.title(),
                "Confidence": round(conf, 3),
                "Width(px)": width,
                "Height(px)": height
            })
        
        count = len(results.boxes)
        avg_confidence = np.mean(confidences) if confidences else 0.0
        
        # Convert BGR to RGB
        img_draw_rgb = cv2.cvtColor(img_draw, cv2.COLOR_BGR2RGB)
        
        return {
            'count': count,
            'avg_confidence': avg_confidence,
            'particle_types': {k: v for k, v in type_counts.items() if v > 0},
            'annotated_image': img_draw_rgb,
            'detections_table': detections_list,
            'individual_confidences': confidences
        }
    
    except Exception as e:
        return {'error': str(e), 'count': 0, 'avg_confidence': 0.0}