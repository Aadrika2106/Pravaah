import pickle
import pandas as pd
import numpy as np

def predict_wqi(features_dict):
    """Predict Water Quality Index"""
    try:
        with open('models/wqi/random_forest_wqi.pkl', 'rb') as f:
            model = pickle.load(f)
        
        feature_order = [
            'temperature', 'ph', 'dissolved_oxygen', 'conductivity',
            'turbidity', 'tds', 'bod', 'cod', 'nitrate', 'phosphate',
            'fecal_coliform', 'total_coliform', 'chloride', 'fluoride',
            'hardness', 'alkalinity'
        ]
        
        feature_values = [features_dict.get(f, 0) for f in feature_order]
        df = pd.DataFrame([feature_values], columns=feature_order)
        
        wqi_score = float(model.predict(df)[0])
        wqi_score = np.clip(wqi_score, 0, 100)
        
        if wqi_score < 25:
            classification = 'Excellent'
        elif wqi_score < 50:
            classification = 'Good'
        elif wqi_score < 75:
            classification = 'Fair'
        else:
            classification = 'Poor'
        
        return {
            'wqi_score': wqi_score,
            'classification': classification
        }
    
    except Exception as e:
        # Fallback calculation
        wqi = 50.0
        return {
            'wqi_score': wqi,
            'classification': 'Good',
            'error': str(e)
        }