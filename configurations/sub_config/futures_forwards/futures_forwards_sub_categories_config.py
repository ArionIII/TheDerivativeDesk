from flask import Blueprint, render_template

tool_category_future_forwards_routes = Blueprint("tool_category_future_forwards_routes", __name__)

FUTURES_FORWARDS_TOOL_CATEGORIES = {
    # Futures Pricing Tools
    "futures-pricing": {
        "title": "Futures Pricing Tools",
        "description": "Select a futures pricing tool based on the type of asset or scenario you are analyzing.",
        "parent_category":"futures-forwards",
        "tools": [
            {
                "title": "Stock Index with Dividend Yield",
                "description": "Calculate the futures price of a stock index considering dividend yield.",
                "url": "/tools/futures-forwards/futures-pricing/futures_pricing_stock_index",
            },
            {
                "title": "Commodity with Storage Costs",
                "description": "Determine the futures price of a commodity with fixed storage costs.",
                "url": "/tools/futures-forwards/futures-pricing/futures_pricing_with_storage",
            },
            {
                "title": "Commodity with Proportional Storage Costs and Convenience Yield",
                "description": "Evaluate the futures price of a commodity with proportional storage costs and convenience yield.",
                "url": "/tools/futures-forwards/futures-pricing/futures_pricing_proportional_costs_yield",
            },
            {
                "title": "Commodity with Non-Proportional Storage Costs and Convenience Yield",
                "description": "Compute the futures price of a commodity with fixed storage costs and convenience yield.",
                "url": "/tools/futures-forwards/futures-pricing/futures_pricing_nonproportional_costs_yield",
            },
            {
                "title": "Investment Asset (Cost of Carry)",
                "description": "Calculate the futures price of an investment asset using cost of carry.",
                "url": "/tools/futures-forwards/futures-pricing/futures_pricing_cost_of_carry",
            },
            {
                "title": "Consumption Asset (Cost of Carry with Convenience Yield)",
                "description": "Determine the futures price of a consumption asset using cost of carry and convenience yield.",
                "url": "/tools/futures-forwards/futures-pricing/futures_pricing_cost_of_carry_yield",
            },
        ],
    },
    # Forward Pricing Tools
    "forward-pricing": {
        "title": "Forward Pricing Tools",
        "description": "Select a forward pricing tool based on the type of asset or scenario you are analyzing.",
        "parent_category":"futures-forwards",
        "tools": [
            {
                "title": "Investment Asset without Income",
                "description": "Calculate the forward price of an investment asset with no income during its life.",
                "url": "/tools/futures-forwards/forward-pricing/forward_pricing_no_income",
            },
            {
                "title": "Investment Asset with Known Income",
                "description": "Calculate the forward price of an investment asset with known income.",
                "url": "/tools/futures-forwards/forward-pricing/forward_pricing_with_income",
            },
            {
                "title": "Investment Asset with Known Yield",
                "description": "Calculate the forward price of an investment asset with known yield.",
                "url": "/tools/futures-forwards/forward-pricing/forward_pricing_with_yield",
            },
            {
                "title": "Foreign Currency (Interest Rate Parity)",
                "description": "Calculate the forward price of a foreign currency using interest rate parity.",
                "url": "/tools/futures-forwards/forward-pricing/forward_pricing_foreign_currency",
            },
        ],
    },
    # Hedging Tools
    "hedging-basics": {
        "title": "Hedging Strategies",
        "description": "Explore tools for optimizing hedge strategies, including minimum variance, tailing adjustments, and optimal contract calculations.",
        "parent_category":"futures-forwards",
        "tools": [
            {
                "title": "Optimal Futures & Tailing the Hedge",
                "description": (
                    "Compute the optimal number of futures contracts or adjust for tailing the hedge "
                    "with optional asset and futures value parameters."
                ),
                "url": "/tools/hedging-basics/optimal_number_of_futures_contracts_tailing_the_hedge",
            },
            {
                "title": "Minimum Variance Hedge Ratio",
                "description": "Calculate the minimum variance hedge ratio using standard deviations of spot and futures prices, and their correlation.",
                "url": "/tools/hedging-basics/minimum_variance_hedge_ratio",
            },
        ],
    },
    "equity-hedging": {
        "title": "Equity Hedging Tools",
        "description": "Discover tools for managing equity portfolio risk, including beta adjustments and portfolio hedging using futures.",
        "parent_category": "futures-forwards",
        "tools": [
            {
                "title": "Hedge Equity Portfolio",
                "description": "Compute the hedge for an equity portfolio using futures contracts based on beta and portfolio value.",
                "url": "/tools/equity-hedging/hedge_equity_portfolio",
            },
            {
                "title": "Change Portfolio Beta",
                "description": "Calculate the optimal hedge to adjust an equity portfolio beta to a target level.",
                "url": "/tools/equity-hedging/change_beta_portfolio",
            },
        ],
    },
    # Valuation Tools
    "forward-contract-value": {
    "title": "Value of Forward Contracts",
    "description": "Evaluate the value of forward contracts for both long and short positions based on market price, forward price, and contract size.",
    "parent_category": "futures-forwards",
    "tools": [
        {
            "title": "Value of Forward Contracts",
            "description": (
                "Calculate the value of forward contracts for both long and short positions "
                "using the market price, forward price, and contract size."
            ),
            "url": "/tools/value-forward-contracts/value_forward_contracts",
        },
    ],
},
    "delivery-timing": {
        "title": "Delivery Timing Tools",
        "description": "Evaluate the optimal delivery timing for futures contracts based on cost of carry and convenience yield.",
        "parent_category": "futures-forwards",
        "tools": [
            {
                "title": "Delivery Timing Decision",
                "description": "Determine whether to deliver a futures contract as soon as possible or as late as possible, based on cost of carry and convenience yield.",
                "url": "/tools/delivery-timing-decision/delivery_timing_decision",
            }
        ]
    }
}


@tool_category_future_forwards_routes.route("/tools/futures-forwards/<category_key>")
def render_tool_category(category_key):
    category = FUTURES_FORWARDS_TOOL_CATEGORIES.get(category_key)
    if not category:
        return "Category not found", 404
    return render_template("tool_category.html", category=category)