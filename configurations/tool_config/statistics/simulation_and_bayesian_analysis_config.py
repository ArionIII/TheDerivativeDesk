SIMULATION_AND_BAYESIAN_ANALYSIS_TOOL_CONFIG = {
    "monte-carlo": {
        "title": "Monte Carlo Simulations",
        "description": "Perform Monte Carlo simulations to estimate outcomes.",
        "url": "/tools/monte-carlo-simulations/monte-carlo",
        "inputs": [
            {
                "label": "Number of Simulations",
                "id": "num_simulations",
                "type": "number",
                "placeholder": "1000",
                "optional": False,
            },
            {
                "label": "Random Seed (optional)",
                "id": "random_seed",
                "type": "number",
                "placeholder": "42",
                "optional": True,
            },
        ],
        "outputs": ["CSV File with Simulation Results"],
    },
    "bayesian-updating": {
        "title": "Bayesian Updating",
        "description": "Update beliefs using Bayesian probabilities.",
        "url": "/tools/bayesian-analysis/bayesian-updating",
        "inputs": [
            {
                "label": "Prior Probability",
                "id": "prior",
                "type": "number",
                "placeholder": "0.6",
                "optional": False,
            },
            {
                "label": "Likelihood",
                "id": "likelihood",
                "type": "number",
                "placeholder": "0.8",
                "optional": False,
            },
            {
                "label": "Evidence Probability",
                "id": "evidence",
                "type": "number",
                "placeholder": "0.7",
                "optional": False,
            },
        ],
        "outputs": ["Updated Probability"],
    },
}
