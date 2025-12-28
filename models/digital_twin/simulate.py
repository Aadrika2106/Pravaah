import pickle
import numpy as np

def run_digital_twin_simulation(scenario_params, duration_days=30):
    """
    Run Digital Twin environmental simulation
    """
    try:
        # Load simulator
        with open('models/digital_twin/twin_simulator.pkl', 'rb') as f:
            simulator = pickle.load(f)
        
        # Extract parameters
        pollution_load = scenario_params.get('pollution_load', 100)
        cleanup_frequency = scenario_params.get('cleanup_frequency', 0.2)
        regulation_strictness = scenario_params.get('regulation_strictness', 0.5)
        
        # Run simulation through model
        results = simulator.simulate(
            days=duration_days,
            pollution=pollution_load,
            cleanup=cleanup_frequency,
            regulations=regulation_strictness
        )
        
        return results
    
    except Exception as e:
        # Fallback: Rule-based simulation
        pollution_load = scenario_params.get('pollution_load', 100)
        cleanup_frequency = scenario_params.get('cleanup_frequency', 0.2)
        regulation_strictness = scenario_params.get('regulation_strictness', 0.5)
        
        time_steps = duration_days
        
        # Initialize arrays
        microplastic_conc = []
        wqi_values = []
        do_values = []
        ecosystem_health = []
        
        # Simulation loop
        current_pollution = pollution_load
        
        for day in range(time_steps):
            # Daily pollution accumulation
            daily_pollution = pollution_load * (1 - regulation_strictness * 0.5)
            daily_pollution += np.random.normal(0, 10)
            
            # Cleanup effect
            if day % max(1, int(1 / (cleanup_frequency + 0.01))) == 0:
                daily_pollution *= 0.6  # Cleanup removes 40%
            
            # Update pollution
            current_pollution = max(0, current_pollution * 0.95 + daily_pollution * 0.05)
            
            # Calculate dependent variables
            mp_conc = current_pollution
            wqi = max(0, 100 - (mp_conc / 5))
            do = max(0, 8.5 - (mp_conc / 50))
            health = (wqi * 0.6 + do * 4)
            
            # Store results
            microplastic_conc.append(mp_conc)
            wqi_values.append(wqi)
            do_values.append(do)
            ecosystem_health.append(health)
        
        # Calculate summary
        summary = {
            'avg_microplastic_conc': float(np.mean(microplastic_conc)),
            'avg_wqi': float(np.mean(wqi_values)),
            'avg_do': float(np.mean(do_values)),
            'ecosystem_health_score': float(np.mean(ecosystem_health)),
            'critical_days': sum(1 for w in wqi_values if w < 50),
            'recommendation': _get_recommendation(np.mean(wqi_values))
        }
        
        return {
            'time_series': {
                'microplastic_concentration': microplastic_conc,
                'wqi': wqi_values,
                'dissolved_oxygen': do_values,
                'ecosystem_health': ecosystem_health
            },
            'summary': summary,
            'simulation_days': duration_days,
            'warning': 'Using fallback simulation',
            'error': str(e)
        }

def _get_recommendation(avg_wqi):
    """Generate recommendations based on WQI"""
    if avg_wqi > 75:
        return 'Maintain current practices. Water quality is good.'
    elif avg_wqi > 50:
        return 'Increase monitoring frequency. Consider preventive measures.'
    else:
        return 'Urgent intervention required. Implement strict pollution controls immediately.'