# Centralized configuration for all tools in "Option Greeks"
GREEKS_TOOL_CONFIG = {
    ## GREEKS VISUALIZER ##
    "greeks-visualizer": {
        "title": "Greeks Visualizer",
        "description": "Dynamically adjust parameters and observe the behavior of Delta, Gamma, Theta and Vega in real-time.",
        "url": "/tools/options/greeks/greeks-visualizer",
        "inputs": [
            {"label": "Option Type", "id": "option_type", "type": "select", "options": ["CALL", "PUT"]},
            {"label": "Underlying Price (S₀)", "id": "underlying_price", "type": "range", "placeholder": "100", "range": [0,1000], "step": 1},
            {"label": "Strike Price (K)", "id": "strike_price", "type": "range", "placeholder": "100", "range": [0,1000], "step": 1},
            {"label": "Time to Maturity (T)", "id": "time_to_maturity", "type": "range", "placeholder": "0.5", "range": [0,20], "step": 0.1},
            {"label": "Risk-Free Rate (r)", "id": "risk_free_rate", "type": "range", "placeholder": "0.05", "range": [0,1], "step": 0.01},   
            {"label": "Volatility (σ)", "id": "volatility", "type": "range", "placeholder": "0.2", "range": [0,1], "step": 0.01},
            {"label": "Dividend Yield (q)", "id": "dividend_yield", "type": "range", "placeholder": "0.03", "optional": True, "range": [0,1], "step": 0.01}, 
            {"label": "Position Type", "id": "position_type", "type": "select", "options": ["LONG", "SHORT"]}
        ],
        "outputs": ["Delta", "Gamma", "Theta", "Vega", "Rho"],
        "is_live": True,
        "keywords": [
            "greeks", "sensitivity", "delta", "gamma", "theta", "vega", "rho", "visualizer"
        ],
    },

    ## DELTA HEDGING SIMULATOR ##
    # "delta-hedging-simulator": {
    #     "title": "Delta Hedging Simulator",
    #     "description": "Simulate a delta-hedging strategy by adjusting the underlying position dynamically.",
    #     "url": "/tools/options/greeks/delta-hedging-simulator",
    #     "inputs": [
    #         {"label": "Option Type", "id": "option_type", "type": "select", "options": ["CALL", "PUT"]},
    #         {"label": "Underlying Price (S₀)", "id": "underlying_price", "type": "number", "placeholder": "100"},
    #         {"label": "Strike Price (K)", "id": "strike_price", "type": "number", "placeholder": "100"},
    #         {"label": "Time to Maturity (T)", "id": "time_to_maturity", "type": "number", "placeholder": "0.5"},
    #         {"label": "Risk-Free Rate (r)", "id": "risk_free_rate", "type": "number", "placeholder": "0.05"},
    #         {"label": "Volatility (σ)", "id": "volatility", "type": "number", "placeholder": "0.2"},
    #         {"label": "Dividend Yield (q)", "id": "dividend_yield", "type": "number", "placeholder": "0.03", "optional": True},
    #         {"label": "Delta Target", "id": "delta_target", "type": "number", "placeholder": "0.5"},
    #         {"label": "Position Type", "id": "position_type", "type": "select", "options": ["LONG", "SHORT"]}
    #     ],
    #     "outputs": ["Hedging Strategy P&L", "Adjusted Delta"],
    #     "visualization": True,
    #     "graphs": [
    #         {"name": "Delta Hedging Strategy"},
    #         {"name": "Adjusted Delta Curve"}
    #     ],
    #     "keywords": [
    #         "delta hedging", "dynamic hedging", "gamma", "portfolio", "volatility"
    #     ],
    # },

    # ## GREEKS SENSITIVITY EXPLORER ##
    # "greeks-sensitivity-explorer": {
    #     "title": "Greeks Sensitivity Explorer",
    #     "description": "Explore how Greeks evolve based on changes in multiple market parameters.",
    #     "url": "/tools/options/greeks/sensitivity-explorer",
    #     "inputs": [
    #         {"label": "Option Type", "id": "option_type", "type": "select", "options": ["CALL", "PUT"]},
    #         {"label": "Underlying Price (S₀)", "id": "underlying_price", "type": "number", "placeholder": "100"},
    #         {"label": "Strike Price (K)", "id": "strike_price", "type": "number", "placeholder": "100"},
    #         {"label": "Time to Maturity (T)", "id": "time_to_maturity", "type": "number", "placeholder": "0.5"},
    #         {"label": "Risk-Free Rate (r)", "id": "risk_free_rate", "type": "number", "placeholder": "0.05"},
    #         {"label": "Volatility (σ)", "id": "volatility", "type": "number", "placeholder": "0.2"},
    #         {"label": "Dividend Yield (q)", "id": "dividend_yield", "type": "number", "placeholder": "0.03", "optional": True},
    #         {"label": "Sensitivity Parameter 1", "id": "sensitivity_param_1", "type": "select", "options": ["underlying_price", "strike_price", "time_to_maturity", "volatility", "risk_free_rate"]},
    #         {"label": "Sensitivity Parameter 2", "id": "sensitivity_param_2", "type": "select", "options": ["underlying_price", "strike_price", "time_to_maturity", "volatility", "risk_free_rate"]}
    #     ],
    #     "outputs": ["Greeks Sensitivity Surface"],
    #     "visualization": True,
    #     "graphs": [
    #         {"name": "Greeks Sensitivity Heatmap"},
    #         {"name": "Greeks Sensitivity 3D Surface"}
    #     ],
    #     "keywords": [
    #         "sensitivity", "greeks", "volatility", "delta", "gamma", "theta", "vega", "rho"
    #     ],
    # }
    #RM ICI
}
