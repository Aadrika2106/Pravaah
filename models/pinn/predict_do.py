import pickle
import torch
import numpy as np

def predict_dissolved_oxygen(environmental_params, time_steps=72):
    """
    Predict Dissolved Oxygen using PINN
    """
    try:
        # Load PINN model
        model = torch.load('models/pinn/pinn_do.pth')
        
        # Extract parameters
        temp = environmental_params.get('temperature', 25.0)
        ph = environmental_params.get('ph', 7.0)
        flow = environmental_params.get('flow_rate', 1000.0)
        turbidity = environmental_params.get('turbidity', 25.0)
        
        # Time array (hours)
        t = np.arange(time_steps)
        
        # Create input features
        inputs = []
        for time_hour in t:
            inputs.append([
                time_hour / 24,  # Normalized time (days)
                temp,
                ph,
                flow,
                turbidity
            ])
        
        X = np.array(inputs)
        
        # Predict
        if isinstance(model, torch.nn.Module):
            model.eval()
            with torch.no_grad():
                X_tensor = torch.FloatTensor(X)
                predictions = model(X_tensor).numpy().flatten()
        else:
            predictions = model.predict(X)
        
        # Apply physics constraints (DO: 0-15 mg/L)
        predictions = np.clip(predictions, 0, 15)
        
        # Find critical hours (DO < 4.0)
        critical_hours = [int(i) for i, do in enumerate(predictions) if do < 4.0]
        
        return {
            'time_hours': t.tolist(),
            'do_predictions': predictions.tolist(),
            'mean_do': float(predictions.mean()),
            'min_do': float(predictions.min()),
            'max_do': float(predictions.max()),
            'critical_hours': critical_hours
        }
    
    except Exception as e:
        # Fallback: Physics-based simulation
        t = np.arange(time_steps)
        
        # Simple DO model based on temperature
        temp = environmental_params.get('temperature', 25.0)
        base_do = 8.5 - (temp - 20) * 0.2  # Temperature effect
        
        # Add daily variation
        daily_cycle = 0.5 * np.sin(2 * np.pi * t / 24)
        noise = np.random.normal(0, 0.2, time_steps)
        
        predictions = base_do + daily_cycle + noise
        predictions = np.clip(predictions, 0, 15)
        
        critical_hours = [int(i) for i, do in enumerate(predictions) if do < 4.0]
        
        return {
            'time_hours': t.tolist(),
            'do_predictions': predictions.tolist(),
            'mean_do': float(predictions.mean()),
            'min_do': float(predictions.min()),
            'max_do': float(predictions.max()),
            'critical_hours': critical_hours,
            'warning': 'Using fallback physics model',
            'error': str(e)
        }
