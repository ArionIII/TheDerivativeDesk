INTEREST_RATE_FUNDAMENTALS_TOOL_CONFIG = {
    "continuous-compounding-rate": {
        "title": "Continuous Compounding Rate",
        "description": "Convert m-compounding rate to continuous compounding rate.",
        "url": "/tools/basic-interest-rates-analysis/continuous-compounding-rate",
        "inputs": [
            {"label": "Rate (m-compounding)", "id": "rate_m", "type": "number", "placeholder": "e.g., 0.05", "optional": False},
            {"label": "Compounding Frequency (m)", "id": "frequency_m", "type": "number", "placeholder": "e.g., 4", "optional": False},
        ],
        "outputs": ["Rate (Continuous Compounding)"],
    },
    "m-to-continuous-compounding-rate": {
    "title": "Continuous to m-Compounding Rate",
    "description": "Convert continuous compounding rate to m-compounding rate.",
    "url": "/tools/basic-interest-rates-analysis/m-to-continuous-compounding-rate",
    "inputs": [
        {"label": "Rate (Continuous Compounding)", "id": "rate_c", "type": "number", "placeholder": "e.g., 0.05", "optional": False},
        {"label": "Compounding Frequency (m)", "id": "frequency_m", "type": "number", "placeholder": "e.g., 4", "optional": False},
    ],
    "outputs": ["Rate (m-Compounding)"],
},
    "zero-rate-curve": {
    "title": "Zero Rate Curve Construction",
    "description": "Construct zero rate curves using market instruments.",
    "url": "/tools/basic-interest-rates-analysis/zero-rate-curve",
    "inputs": [
        {
            "label": "Input Rates (comma-separated)", 
            "id": "input_rates", 
            "type": "array", 
            "placeholder": "e.g., [0.02, 0.025, 0.03]", 
            "optional": False
        },
        {
            "label": "Rate Type (e.g., FRA, Swap)", 
            "id": "rate_type", 
            "type": "select", 
            "placeholder": "Select Rate Type (FRA or Swap)", 
            "options": ["FRA", "Swap"], 
            "default": "FRA", 
            "optional": False
        },
        {
            "label": "Maturities (comma-separated)", 
            "id": "maturities", 
            "type": "array", 
            "placeholder": "e.g., [0.5, 1, 1.5]", 
            "optional": False
        },
        {
            "label": "Space Between Payments (Years)", 
            "id": "space_between_payments", 
            "type": "number", 
            "placeholder": "e.g., 0.5 (Semi-annual)", 
            "optional": True
        }
    ],
    "outputs": ["Zero Rate Curve"]
},
    "bond-pricing": {
        "title": "Bond Pricing",
        "description": "Calculate the price of a bond given its characteristics.",
        "url": "/tools/basic-interest-rates-analysis/bond-pricing",
        "inputs": [
            {"label": "Face Value", "id": "face_value", "type": "number", "placeholder": "e.g., 1000", "optional": False},
            {"label": "Coupon Rate (%)", "id": "coupon_rate", "type": "number", "placeholder": "e.g., 5", "optional": False},
            {"label": "Maturity (Years)", "id": "maturity", "type": "number", "placeholder": "e.g., 10", "optional": False},
            {"label": "Market Rate (%)", "id": "market_rate", "type": "number", "placeholder": "e.g., 4", "optional": False},
        ],
        "outputs": ["Bond Price"],
    },
    "determining-zero-rates": {
    "title": "Determining Zero Rates",
    "description": "Calculate zero rates from coupon bond prices.",
    "url": "/tools/basic-interest-rates-analysis/determining-zero-rates",
    "inputs": [
        {
            "label": "Bond Prices (comma-separated)", 
            "id": "bond_prices", 
            "type": "array", 
            "placeholder": "e.g., [980, 970, 960]", 
            "optional": False
        },
        {
            "label": "Face Values (comma-separated)", 
            "id": "face_values", 
            "type": "array", 
            "placeholder": "e.g., [1000, 1000, 1000]", 
            "optional": False
        },
        {
            "label": "Maturities (Years)", 
            "id": "maturities", 
            "type": "array", 
            "placeholder": "e.g., [1, 2, 3]", 
            "optional": False
        },

    ],
    "outputs": ["Zero Rates"]
},
    "extending-libor-curve-with-swap-rates": {
        "title": "Extend LIBOR Curve with Swap Rates",
        "description": "Use swap rates to extend the LIBOR curve.",
        "url": "/tools/interest-rates/extending-libor-curve-with-swap-rates",
        "inputs": [
            {"label": "Initial LIBOR Rates (comma-separated)", "id": "libor_rates", "type": "array", "placeholder": "e.g., [0.01, 0.015]", "optional": False},
            {"label": "Swap Rates (comma-separated)", "id": "swap_rates", "type": "array", "placeholder": "e.g., [0.02, 0.025, 0.03]", "optional": False},
            {"label": "Maturities (Years)", "id": "maturities", "type": "array", "placeholder": "e.g., [1, 2, 3]", "optional": False},
        ],
        "outputs": ["Extended LIBOR Curve"],
    },
    "extending-libor-curve-with-fra": {
        "title": "Extend LIBOR Curve with FRA",
        "description": "Use FRA rates to extend the LIBOR curve.",
        "url": "/tools/interest-rates/extending-libor-curve-with-fra",
        "inputs": [
            {"label": "Initial LIBOR Rates (comma-separated)", "id": "libor_rates", "type": "array", "placeholder": "e.g., [0.01, 0.015]", "optional": False},
            {"label": "FRA Rates (comma-separated)", "id": "fra_rates", "type": "array", "placeholder": "e.g., [0.02, 0.022, 0.024]", "optional": False},
            {"label": "Maturities (Years)", "id": "maturities", "type": "array", "placeholder": "e.g., [1, 2, 3]", "optional": False},
        ],
        "outputs": ["Extended LIBOR Curve"],
    },
    "payoff-of-fra": {
        "title": "Payoff of FRA",
        "description": "Calculate the payoff of a Forward Rate Agreement (FRA).",
        "url": "/tools/interest-rates/payoff-of-fra",
        "inputs": [
            {"label": "Contract Rate", "id": "contract_rate", "type": "number", "placeholder": "e.g., 0.02", "optional": False},
            {"label": "Settlement Rate", "id": "settlement_rate", "type": "number", "placeholder": "e.g., 0.025", "optional": False},
            {"label": "Notional Value", "id": "notional_value", "type": "number", "placeholder": "e.g., 1000000", "optional": False},
            {"label": "Time (Years)", "id": "time", "type": "number", "placeholder": "e.g., 0.5", "optional": False},
        ],
        "outputs": ["FRA Payoff"],
    },
    "duration-and-convexity": {
        "title": "Duration and Convexity",
        "description": "Calculate the duration and convexity of a bond.",
        "url": "/tools/basic-interest-rate-analysis/duration-and-convexity",
        "inputs": [
            {"label": "Bond Cash Flows (comma-separated)", "id": "cash_flows", "type": "array", "placeholder": "e.g., [50, 50, 1050]", "optional": False},
            {"label": "Discount Rates (comma-separated)", "id": "discount_rates", "type": "array", "placeholder": "e.g., [0.03, 0.035, 0.04]", "optional": False},
            {"label": "Time Periods (Years)", "id": "time_periods", "type": "array", "placeholder": "e.g., [1, 2, 3]", "optional": False},
        ],
        "outputs": ["Duration", "Convexity"],
    },
}
