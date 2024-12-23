HEDGING_TOOL_CONFIG = {
    "optimal_number_of_futures_contracts_tailing_the_hedge": {
        "title": "Hedging Strategies: Optimal Futures & Tailing the Hedge",
        "description": (
            "Compute the optimal number of futures contracts or adjust for tailing the hedge "
            "with optional asset and futures value parameters."
        ),
        "url": "/tools/hedging/hedging_tool",
        "inputs": [
            {"label": "Asset Quantity", "id": "asset_quantity", "type": "number", "placeholder": "e.g., 1000", "step": "any"},
            {"label": "Futures Quantity", "id": "futures_quantity", "type": "number", "placeholder": "e.g., 50", "step": "any"},
            {"label": "Hedge Ratio", "id": "hedge_ratio", "type": "number", "placeholder": "e.g., 0.9", "step": "any"},
            {"label": "Asset Value (optional)", "id": "asset_value", "type": "number", "placeholder": "e.g., 100000", "step": "any", "optional": True},
            {"label": "Futures Value (optional)", "id": "futures_value", "type": "number", "placeholder": "e.g., 95000", "step": "any", "optional": True}
        ],
        "outputs": ["Optimal Number of Futures Contracts", "Hedge Adjustment Value"],
        "visualization": False,
        "keywords": [
            "hedging", "futures contracts", "hedge ratio", "tailing the hedge",
            "asset quantity", "futures quantity", "asset value", "futures value",
            "optimal hedge", "financial derivatives"
        ],
    }, 
    "minimum_variance_hedge_ratio"   : {
    "title": "Minimum Variance Hedge Ratio",
    "description": "Calculate the minimum variance hedge ratio using standard deviations of spot and futures prices, and their correlation.",
    "url": "/tools/hedging/minimum_variance_hedge_ratio",
    "inputs": [
        {"label": "Standard Deviation of Spot Changes (σₛ)", "id": "std_change_spot", "type": "number", "placeholder": "e.g., 0.05", "step": "any"},
        {"label": "Standard Deviation of Futures Changes (σₓ)", "id": "std_change_futures", "type": "number", "placeholder": "e.g., 0.04", "step": "any"},
        {"label": "Correlation Coefficient (ρ)", "id": "correlation", "type": "number", "placeholder": "e.g., 0.8", "step": "any"}
    ],
    "outputs": ["Minimum Variance Hedge Ratio (h*)"],
    "visualization": False,
    "keywords": [
        "hedging", "minimum variance hedge", "hedge ratio", "correlation coefficient",
        "spot standard deviation", "futures standard deviation", "financial derivatives",
        "hedging strategies", "variance minimization", "risk management"
    ],
},
 "hedge_equity_portfolio": {
        "title": "Hedge Equity Portfolio",
        "description": "Compute the hedge for an equity portfolio using futures.",
        "url": "/tools/hedging/equity/hedge_equity_portfolio",
        "inputs": [
            {"label": "Beta (β)", "id": "beta", "type": "number", "placeholder": "e.g., 1.2", "step": "any"},
            {"label": "Asset Value ($)", "id": "asset_value", "type": "number", "placeholder": "e.g., 1000000", "step": "any"},
            {"label": "Futures Value ($)", "id": "futures_value", "type": "number", "placeholder": "e.g., 200000", "step": "any"},
        ],
        "outputs": ["Optimal Number of Futures Contracts"],
        "visualization": False,
        "keywords": [
            "equity hedging", "portfolio hedge", "hedging strategies",
            "equity futures", "portfolio beta", "financial derivatives",
            "risk management", "hedging tools", "optimal hedge"
        ],
    },
    "change_beta_portfolio": {
        "title": "Change Portfolio Beta",
        "description": "Compute the hedge to change the beta of an equity portfolio to a target level.",
        "url": "/tools/hedging/equity/change_beta_portfolio",
        "inputs": [
            {"label": "Target Beta (βₜ)", "id": "target_beta", "type": "number", "placeholder": "e.g., 0.8", "step": "any"},
            {"label": "Current Beta (βₒ)", "id": "current_beta", "type": "number", "placeholder": "e.g., 1.2", "step": "any"},
            {"label": "Asset Value ($)", "id": "asset_value", "type": "number", "placeholder": "e.g., 1000000", "step": "any"},
            {"label": "Futures Value ($)", "id": "futures_value", "type": "number", "placeholder": "e.g., 200000", "step": "any"},
        ],
        "outputs": ["Optimal Number of Futures Contracts"],
        "visualization": False,
        "keywords": [
            "change portfolio beta", "target beta", "hedging strategies",
            "equity portfolio", "futures hedge", "portfolio risk",
            "financial derivatives", "portfolio adjustment", "hedging tools"
        ],
    }}
