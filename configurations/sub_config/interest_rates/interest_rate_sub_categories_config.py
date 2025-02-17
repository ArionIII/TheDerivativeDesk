from flask import Blueprint, render_template

tool_category_interest_rates_routes = Blueprint("tool_category_interest_rates_routes", __name__)

INTEREST_RATES_TOOL_CATEGORIES = {
    # Basic Interest Rate Analysis
    "basic-interest-rates-analysis": {
        "title": "Basic Interest Rate Analysis",
        "description": "Perform fundamental interest rate calculations, including rate conversions, bond pricing, and basic sensitivity analysis.",
        "parent_category": "interest-rates",
        "tools": [
            {"title": "Continuous Compounding to m-Compounding Rate", "description": "Convert m-compounding rates to continuous compounding rates.", "url": "/tools/basic-interest-rates-analysis/continuous-compounding-rate"},
            {"title": "m-Compounding to Continuous Rate", "description": "Convert m-compounding rates to continuous compounding rates.", "url": "/tools/basic-interest-rates-analysis/m-to-continuous-compounding-rate"},
            {"title": "Bond Pricing", "description": "Calculate the price of bonds based on market rates.", "url": "/tools/basic-interest-rates-analysis/bond-pricing"},
            {"title": "Duration and Convexity", "description": "Compute Macaulay, Modified Duration for bonds & Convexity.", "url": "/tools/basic-interest-rates-analysis/duration-and-convexity"},
        ],
    },
    # Term Structure Construction
    "term-structure-construction": {
        "title": "Term Structure Construction",
        "description": "Construct term structures of interest rates using various market instruments.",
        "parent_category": "interest-rates",
        "tools": [
            # {"title": "Zero Rate Curve", "description": "Determine zero rates from market data.", "url": "/tools/term-structure-construction/zero-rate-curve"},
            {"title": "Determining Zero Rates & Zero-Curve", "description": "Compute zero rates from bond prices.", "url": "/tools/basic-interest-rates-analysis/determining-zero-rates"},
            {"title": "Extend Zero-Rate Curve with Swap Rates", "description": "Extend the Zero-Rate curve using swap rates.", "url": "/tools/term-structure-construction/extending-libor-curve-with-swap-rates"},
            {"title": "Extend Zero-Rate Curve with FRA", "description": "Extend the Zero-Rate curve using forward rate agreements (FRA).", "url": "/tools/term-structure-construction/extending-zero-curve-with-fra"},
        ],
    },
    # Forward Rate Agreements (FRA)
    "forward-rate-agreements": {
        "title": "Forward Rate Agreements (FRA)",
        "description": "Analyze and value forward rate agreements.",
        "parent_category": "interest-rates",
        "tools": [
            {"title": "Payoff of FRA", "description": "Calculate the payoff of a forward rate agreement.", "url": "/tools/forward-rate-agreements/payoff-of-fra"},
            {"title": "Valuation of FRA", "description": "Evaluate the value of forward rate agreements.", "url": "/tools/forward-rate-agreements/valuation-of-fra"},
            {"title": "Forward Rate Calculation", "description": "Calculate forward rates from spot rates or zero rates.", "url": "/tools/forward-rate-agreements/forward-rate-calculation"},
            {"title": "FRA Break-Even Rate", "description": "Determine the break-even interest rate for an FRA.", "url": "/tools/forward-rate-agreements/fra-break-even-rate"},
            {"title": "Hedging with FRA", "description": "Analyze hedging strategies using forward rate agreements to manage interest rate risks.", "url": "/tools/forward-rate-agreements/hedging-with-fra"},
        ],
    },
    # Interest Rate Derivatives
    "swaps-and-interest-rate-derivatives": {
        "title": "Interest Rate Derivatives",
        "description": "Explore interest rate derivatives including swaps, futures, and swaptions.",
        "parent_category": "interest-rates",
        "tools": [
            {"title": "Interest Rate Swap Cash Flows", "description": "Calculate the cash flows of fixed-for-floating interest rate swaps.", "url": "/tools/swaps-and-interest-rate-derivatives/interest-rate-swap-cash-flows"},
            {"title": "Interest Rate Swap Valuation", "description": "Compute the present value of interest rate swaps using market curves.", "url": "/tools/swaps-and-interest-rate-derivatives/interest-rate-swap-valuation"},
            {"title": "Pricing Interest Rate Futures", "description": "Price interest rate futures such as Eurodollar futures based on market interest rates.", "url": "/tools/swaps-and-interest-rate-derivatives/pricing-interest-rate-futures"},
            {"title": "Swap Spread Analysis", "description": "Analyze the spread between swap rates and government yields.", "url": "/tools/swaps-and-interest-rate-derivatives/swap-spread-analysis"},
            {"title": "Swaption Valuation", "description": "Value options on interest rate swaps using Black’s model.", "url": "/tools/swaps-and-interest-rate-derivatives/swaption-valuation"},
            {"title": "Basis Swap Analysis", "description": "Evaluate basis swaps where both legs are floating rates with different benchmarks.", "url": "/tools/swaps-and-interest-rate-derivatives/basis-swap-analysis"},
            {"title": "Interest Rate Swap Delta Hedging", "description": "Analyze hedging strategies for interest rate swaps.", "url": "/tools/swaps-and-interest-rate-derivatives/interest-rate-swap-delta-hedging"},
        ],
    },
}


@tool_category_interest_rates_routes.route("/tools/interest-rates/<category_key>")
def render_interest_rates_tool_category(category_key):
    category = INTEREST_RATES_TOOL_CATEGORIES.get(category_key)
    if not category:
        return "Category not found", 404
    return render_template("tool_category.html", category=category)
