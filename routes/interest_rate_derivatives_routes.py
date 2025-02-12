from flask import Blueprint, render_template, request, jsonify
from config import logger, parse_inputs
from configurations.tool_config.interest_rates.interest_rate_derivatives_tool_config import INTEREST_RATE_DERIVATIVES_TOOL_CONFIG
from formulas.interest_rates_formulas import *  

# Blueprint for New Interest Rate Tools
interest_rate_derivatives_routes = Blueprint("interest_rate_derivatives_routes", __name__)

# Tool Functions
NEW_TOOL_FUNCTIONS = {
    "payoff-of-fra": calculate_payoff_of_fra,
    "calculate-valuation-of-fra": calculate_valuation_of_fra,
    "forward-rate-calculation": calculate_forward_rate,
    "fra-break-even-rate": calculate_fra_break_even_rate,
    "calculate-interest-rate-swap-cash-flows": calculate_interest_rate_swap_cash_flows,
    "calculate-interest-rate-swap-valuation": calculate_interest_rate_swap_valuation,
    "calculate-pricing-interest-rate-futures": calculate_pricing_interest_rate_futures,
    "calculate-swap-spread-analysis": calculate_swap_spread_analysis,
    "calculate-swaption-valuation": calculate_swaption_valuation,
    "calculate-basis-swap-analysis": calculate_basis_swap_analysis,
    "calculate-interest-rate-swap-delta-hedging": calculate_interest_rate_swap_delta_hedging,
}

# Generic Request Handler
def handle_new_interest_rate_tool_request(tool_key, sub_category_key):
    logger.info(f"Handling request for tool: {tool_key} in {sub_category_key}")
    tool_config = INTEREST_RATE_DERIVATIVES_TOOL_CONFIG.get(tool_key)

    if not tool_config:
        logger.warning(f"Tool not found: {tool_key} in {sub_category_key}")
        return "Tool not found", 404

    if request.method == "POST":
        try:
            data_source = request.form if request.content_type.startswith("multipart/form-data") else request.json
            params = parse_inputs(data_source, tool_config["inputs"])
            if tool_key not in NEW_TOOL_FUNCTIONS:
                logger.error(f'{tool_key} not in tool functions list : {NEW_TOOL_FUNCTIONS}')
            calculation_function = NEW_TOOL_FUNCTIONS.get(tool_key)
            if not calculation_function:
                return "Calculation logic not implemented", 500
            result = calculation_function(**params)
            logger.info("result :", result)
            return jsonify(result)
        except Exception as e:
            logger.error(f"Error processing tool {tool_key}: {e}")
            return jsonify({"error": str(e)}), 400

    return render_template("base_tool.html", tool=tool_config)

# Routes
@interest_rate_derivatives_routes.route("/tools/forward-rate-agreements/<tool_key>", methods=["GET", "POST"])
def handle_new_interest_rate_tool(tool_key):
    return handle_new_interest_rate_tool_request(tool_key, "new-interest-rate-tools")

@interest_rate_derivatives_routes.route("/tools/swaps-and-interest-rate-derivatives/<tool_key>", methods=["GET", "POST"])
def handle_new_swap_analysis_tool(tool_key):
    return handle_new_interest_rate_tool_request(tool_key, "new-swap-analysis")
