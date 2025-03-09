# Centralized configuration for all tools in "Option Pricing Techniques"
OPTION_PRICING_TOOL_CONFIG = {
    ## BINOMIAL TREES ##
    "binomial-dividend": {
    "title": "Binomial Trees: Dividend Adjustment",
    "description": "Price American or European options using a binomial tree approach adjusted for continuous dividends.",
    "url": "/tools/options/option-pricing/binomial-dividend",
    "inputs": [
        {"label": "Option Type", "id": "option_type", "type": "select", "options": ["CALL", "PUT"]},
        {"label": "Style", "id": "option_style", "type": "select", "options": ["American", "European"]},
        {"label": "Underlying Price (S₀)", "id": "underlying_price", "type": "number", "placeholder": "100"},
        {"label": "Strike Price (K)", "id": "strike_price", "type": "number", "placeholder": "100"},
        {"label": "Time to Maturity (T)", "id": "time_to_maturity", "type": "number", "placeholder": "1"},
        {"label": "Risk-Free Rate (r)", "id": "risk_free_rate", "type": "number", "placeholder": "0.05"},
        {"label": "Volatility (σ)", "id": "volatility", "type": "number", "placeholder": "0.2"},
        {"label": "Number of Steps (n)", "id": "steps", "type": "number", "placeholder": "30"},
        {"label": "Dividend Yield (q)", "id": "dividend_yield", "type": "number", "placeholder": "0.03", "optional":True},
    ],
    "outputs": ["Option Price"],
    "visualization": True,
    "graphs": [
        {"name": "Binomial Tree with Dividend"},
        {"name": "Payoff Diagram with Dividend"}
    ],
    "keywords": [
        "binomial trees", "american options", "european options", "option pricing", 
        "dividend adjustment", "financial derivatives", "volatility"
    ]
},

    ## BLACK-SCHOLES ##
    "black-scholes-option": {
        "title": "Black-Scholes: Options",
        "description": "Price European-style options using the Black-Scholes formula.",
        "url": "/tools/options/option-pricing/black-scholes-option",
        "inputs": [
            {"label": "Option Type", "id": "option_type", "type": "select", "options": ["CALL", "PUT"]},
            {"label": "Underlying Price (S₀)", "id": "underlying_price", "type": "number", "placeholder": "100"},
            {"label": "Strike Price (K)", "id": "strike_price", "type": "number", "placeholder": "100"},
            {"label": "Time to Maturity (T)", "id": "time_to_maturity", "type": "number", "placeholder": "1"},
            {"label": "Risk-Free Rate (r)", "id": "risk_free_rate", "type": "number", "placeholder": "0.05"},
            {"label": "Volatility (σ)", "id": "volatility", "type": "number", "placeholder": "0.2"}
        ],
        "outputs": ["Option Price"],
        "visualization": True,
        "graphs": [
            {"name": "Payoff Curve"},
            {"name": "Greeks Sensitivity"}
        ],
        "keywords": [
            "black scholes", "call option", "put option", "option pricing", "financial derivatives"
        ]
    },

    "black-scholes-implied-volatility": {
        "title": "Black-Scholes: Implied Volatility",
        "description": "Calculate the implied volatility of an option using the Black-Scholes model.",
        "url": "/tools/options/option-pricing/black-scholes-implied-volatility",
        "inputs": [
    {"label": "Option Type", "id": "option_type", "type": "select", "options": ["CALL", "PUT"]},
    {"label": "Underlying Price (S₀)", "id": "underlying_price", "type": "number", "placeholder": "100"},
    {"label": "Strike Price (K)", "id": "strike_price", "type": "number", "placeholder": "100"},
    {"label": "Market Option Price", "id": "option_price", "type": "number", "placeholder": "10.5"},
    {"label": "Time to Maturity (T years)", "id": "time_to_maturity", "type": "number", "placeholder": "1"},
    {"label": "Risk-Free Rate (r)", "id": "risk_free_rate", "type": "number", "placeholder": "0.05"}
],

        "outputs": ["Implied Volatility"],
        "keywords": ["black scholes", "implied volatility", "option pricing", "financial derivatives"]
    },

    "american-vs-european-spread": {
        "title": "American vs European Option Spread",
        "description": "Compare the prices of American and European options with the same parameters.",
        "url": "/tools/options/option-pricing/american-vs-european-spread",
        "inputs": [
            {"label": "Option Type", "id": "option_type", "type": "select", "options": ["CALL", "PUT"]},
            {"label": "Underlying Price (S₀)", "id": "underlying_price", "type": "number"},
            {"label": "Strike Price (K)", "id": "strike_price", "type": "number"},
            {"label": "Time to Maturity (T)", "id": "time_to_maturity", "type": "number"},
            {"label": "Risk-Free Rate (r)", "id": "risk_free_rate", "type": "number"},
            {"label": "Volatility (σ)", "id": "volatility", "type": "number"},
            {"label": "Dividend Yield (q)", "id": "dividend_yield", "type": "number", "placeholder": "0.03", "optional":True},
        ],
        "outputs": ["Spread Value"],
        "visualization": True,
        "graphs": [
            {"name": "Spread vs Time"}
        ],
        "keywords": ["american options", "european options", "spread", "option pricing"]
    },

    ## MONTE CARLO ##
    "monte-carlo-option": {
    "title": "Monte Carlo: Options",
    "description": "Use Monte Carlo simulation to price Asian or European options.",
    "url": "/tools/options/option-pricing/monte-carlo-option",
    "inputs": [
        {"label": "Option Type", "id": "option_type", "type": "select", "options": ["CALL", "PUT"]},
        {"label": "Option Style", "id": "option_style", "type": "select", "options": ["Asian", "European"]},
        {"label": "Underlying Price (S₀)", "id": "underlying_price", "type": "number", "placeholder": "100"},
        {"label": "Strike Price (K)", "id": "strike_price", "type": "number", "placeholder": "100"},
        {"label": "Risk-Free Rate (r)", "id": "risk_free_rate", "type": "number", "placeholder": "0.05"},
        {"label": "Volatility (σ)", "id": "volatility", "type": "number", "placeholder": "0.2"},
        {"label": "Number of Simulations/Paths", "id": "num_simulations", "type": "number", "placeholder": "10000"}
    ],
    "outputs": ["Option Price"],
    "visualization": True,
    "graphs": [
        {"name": "Simulation Results Histogram"},
        {"name": "Convergence Plot"}
    ],
    "keywords": [
        "monte carlo", "asian options", "european options", "simulation", 
        "financial derivatives", "volatility", "option pricing"
    ]
},

    # "monte-carlo-path-dependent": {
    #     "title": "Monte Carlo: Path Dependent Options",
    #     "description": "Use Monte Carlo simulation to price path-dependent options.",
    #     "url": "/tools/options/option-pricing/monte-carlo-path-dependent",
    #     "inputs": [
    #         {"label": "Number of Paths", "id": "num_paths", "type": "number"}
    #     ],
    #     "outputs": ["Path Dependent Option Price"],
    #     "visualization": True,
    #     "graphs": [
    #         {"name": "Path Dependent Payoff"}
    #     ],
    #     "keywords": ["monte carlo", "path dependent", "option pricing", "simulation"]
    # }
}
