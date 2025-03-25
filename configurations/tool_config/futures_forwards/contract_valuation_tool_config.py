CONTRACT_VALUATION_TOOL_CONFIG = {
    "value_forward_contracts": {
        "title": "Value of Forward Contracts",
        "description": (
            "Compute the value of forward contracts for long and short positions "
            "based on the market price, forward price, and contract size."
        ),
        "url": "/tools/value-forward-contracts/value_forward_contracts",
        "inputs": [
            {
                "label": "Forward Price (F₀)",
                "id": "forward_price",
                "type": "number",
                "placeholder": "1400",
                "step": "any",
            },
            {
                "label": "Delivery Price (K)",
                "id": "delivery_price",
                "type": "number",
                "placeholder": "1350",
                "step": "any",
            },
            {
                "label": "Risk-Free Rate (r)",
                "id": "risk_free_rate",
                "type": "number",
                "placeholder": "0.05",
                "step": "any",
            },
            {
                "label": "Time to Maturity (T)",
                "id": "time_to_maturity",
                "type": "number",
                "placeholder": "1",
                "step": "any",
            },
            {
                "label": "Position Type (Long/Short)",
                "id": "position_type",
                "type": "select",
                "placeholder": "Select Long or Short Position",
                "options": ["Long", "Short"],
                "default": "Long",
                "optional": False,
            },
        ],
        "outputs": ["Value "],
        "visualization": False,
        "keywords": [
            "forward contracts",
            "contract valuation",
            "long position",
            "short position",
            "market price",
            "forward price",
            "contract size",
            "financial derivatives",
            "valuation tools",
            "risk management",
        ],
    },
    "delivery_timing_decision": {
        "title": "Delivery Timing Decision",
        "description": (
            "Determine whether to deliver a futures contract as soon as possible or as late as possible, "
            "based on the cost of carry and convenience yield."
        ),
        "url": "/tools/delivery-timing-decision/delivery_timing_decision",
        "inputs": [
            {
                "label": "Cost of Carry (c)",
                "id": "cost_of_carry",
                "type": "number",
                "placeholder": "0.03",
                "step": "any",
                "optional": False,
            },
            {
                "label": "Convenience Yield (y)",
                "id": "convenience_yield",
                "type": "number",
                "placeholder": "0.02",
                "step": "any",
                "optional": False,
            },
        ],
        "outputs": ["Delivery Timing Decision"],
        "visualization": False,
        "keywords": [
            "delivery timing",
            "cost of carry",
            "convenience yield",
            "futures contracts",
            "risk management",
            "financial derivatives",
            "optimal delivery",
            "timing strategies",
        ],
    },
}
