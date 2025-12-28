import pickle
import numpy as np

def predict_polymer(raman_spectrum):
    """Predict polymer type"""
    try:
        with open('models/raman/raman_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        if isinstance(raman_spectrum, list):
            raman_spectrum = np.array(raman_spectrum)
        
        if len(raman_spectrum.shape) == 1:
            raman_spectrum = raman_spectrum.reshape(1, -1)
        
        prediction = model.predict(raman_spectrum)
        probabilities = model.predict_proba(raman_spectrum)
        
        polymer_classes = {0: 'PET', 1: 'PE', 2: 'PP', 3: 'PS', 4: 'PVC'}
        
        polymer = polymer_classes.get(int(prediction[0]), 'Unknown')
        confidence = float(np.max(probabilities[0]))
        
        prob_dict = {
            polymer_classes[i]: float(probabilities[0][i])
            for i in range(len(probabilities[0]))
        }
        
        return {
            'polymer': polymer,
            'confidence': confidence,
            'probabilities': prob_dict
        }
    
    except Exception as e:
        return {'polymer': 'Unknown', 'confidence': 0.0, 'error': str(e)}