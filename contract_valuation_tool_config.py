CONTRACT_VALUATION_TOOL_CONFIG = {
    "value_forward_contracts": {
        "title": "Value of Forward Contracts",
        "description": (
            "Compute the value of forward contracts for long and short positions "
            "based on the market price, forward price, and contract size."
        ),
        "url": "/tools/value-forward-contracts/value_forward_contracts",
        "inputs": [
            {"label": "Market Price (Sₜ)", "id": "market_price", "type": "number", "placeholder": "e.g., 1500", "step": "any"},
            {"label": "Forward Price (F₀)", "id": "forward_price", "type": "number", "placeholder": "e.g., 1400", "step": "any"},
            {"label": "Contract Size (Q)", "id": "contract_size", "type": "number", "placeholder": "e.g., 100", "step": "any"},
            {
                "label": "Position Type (Long/Short)", 
                "id": "position_type", 
                "type": "toggle", 
                "placeholder": "Select Long or Short Position", 
                "options": ["Long", "Short"], 
                "default": "Long",
                "optional": True
            }
        ],
        "outputs": ["Value "],
        "visualization": False,
        "keywords": [
            "forward contracts", "contract valuation", "long position", "short position",
            "market price", "forward price", "contract size", "financial derivatives",
            "valuation tools", "risk management"
        ],
    },
}
