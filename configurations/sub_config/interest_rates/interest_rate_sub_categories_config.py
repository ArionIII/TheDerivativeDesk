from flask import Blueprint, render_template

tool_category_interest_rates_routes = Blueprint("tool_category_interest_rates_routes", __name__)

INTEREST_RATES_TOOL_CATEGORIES = {
    # Basic Interest Rate Analysis
    "basic-interest-rate-analysis": {
        "title": "Basic Interest Rate Analysis",
        "description": "Perform fundamental interest rate calculations, including rate conversions, bond pricing, and basic sensitivity analysis.",
        "parent_category": "interest-rates",
        "tools": [
            {"title": "Continuous Compounding Rate", "description": "Convert m-compounding rates to continuous compounding rates.", "url": "/tools/interest-rates/continuous-compounding-rate"},
            {"title": "Bond Pricing", "description": "Calculate the price of bonds based on market rates.", "url": "/tools/interest-rates/bond-pricing"},
            {"title": "Determining Zero Rates", "description": "Compute zero rates from bond prices.", "url": "/tools/interest-rates/determining-zero-rates"},
            {"title": "Duration", "description": "Compute Macaulay and Modified Duration for bonds.", "url": "/tools/interest-rates/duration"},
            {"title": "Convexity", "description": "Analyze convexity as a measure of interest rate risk.", "url": "/tools/interest-rates/convexity"},
        ],
    },
    # Term Structure Construction
    "term-structure-construction": {
        "title": "Term Structure Construction",
        "description": "Construct term structures of interest rates using various market instruments.",
        "parent_category": "interest-rates",
        "tools": [
            {"title": "Zero Rate Curve", "description": "Determine zero rates from market data.", "url": "/tools/interest-rates/zero-rate-curve"},
            {"title": "Extend LIBOR Curve with Swap Rates", "description": "Extend the LIBOR curve using swap rates.", "url": "/tools/interest-rates/extending-libor-curve-with-swap-rates"},
            {"title": "Extend LIBOR Curve with FRA", "description": "Extend the LIBOR curve using forward rate agreements (FRA).", "url": "/tools/interest-rates/extending-libor-curve-with-fra"},
        ],
    },
    # Forward Rate Agreements (FRA)
    "forward-rate-agreements": {
        "title": "Forward Rate Agreements (FRA)",
        "description": "Analyze and value forward rate agreements.",
        "parent_category": "interest-rates",
        "tools": [
            {"title": "Payoff of FRA", "description": "Calculate the payoff of a forward rate agreement.", "url": "/tools/interest-rates/payoff-of-fra"},
            {"title": "Valuation of FRA", "description": "Evaluate the value of forward rate agreements.", "url": "/tools/interest-rates/valuation-of-fra"},
        ],
    },
    # Repo Market Analysis
    "repo-market": {
        "title": "Repo Market Analysis",
        "description": "Study repurchase agreements and their implications in the fixed income market.",
        "parent_category": "interest-rates",
        "tools": [
            {"title": "Repo Market Analysis", "description": "Analyze the terms and conditions of repurchase agreements.", "url": "/tools/interest-rates/repo-market"},
        ],
    },
}

@tool_category_interest_rates_routes.route("/tools/interest-rates/<category_key>")
def render_interest_rates_tool_category(category_key):
    category = INTEREST_RATES_TOOL_CATEGORIES.get(category_key)
    if not category:
        return "Category not found", 404
    return render_template("tool_category.html", category=category)
