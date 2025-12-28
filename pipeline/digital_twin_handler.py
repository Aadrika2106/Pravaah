def run_digital_twin(microplastic_level):
    effect = microplastic_level * 0.15
    return {
        "simulation": f"DO drops approx {round(effect,2)}% under microplastic stress"
    }
