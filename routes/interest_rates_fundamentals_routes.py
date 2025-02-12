from flask import Blueprint, render_template, request, jsonify
from config import logger, parse_inputs
from configurations.tool_config.interest_rates.interest_rate_fundamentals_tool_config import INTEREST_RATE_FUNDAMENTALS_TOOL_CONFIG
from formulas.interest_rates_formulas import *  
# Blueprint for Interest Rate Fundamentals
interest_rate_fundamentals_routes = Blueprint("interest_rate_fundamentals_routes", __name__)

# Tool Functions
TOOL_FUNCTIONS = {
    "continuous-compounding-rate": continuous_compounding_rate,
    "m-to-continuous-compounding-rate": m_compounding_rate,
    "zero-rate-curve": zero_rate_curve,
    "bond-pricing": bond_pricing,
    "determining-zero-rates": determining_zero_rates,
    "extending-libor-curve-with-swap-rates": extending_libor_curve_with_swap_rates,
    "extending-zero-curve-with-fra": extending_zero_curve_with_fra,
    "payoff-of-fra": payoff_of_fra,
    "duration-and-convexity": duration_and_convexity,
}

# Generic Request Handler
def handle_interest_rate_tool_request(tool_key, sub_category_key):
    logger.info(f"Handling request for tool: {tool_key} in {sub_category_key}")
    tool_config = INTEREST_RATE_FUNDAMENTALS_TOOL_CONFIG.get(tool_key)

    if not tool_config:
        logger.warning(f"Tool not found: {tool_key} in {sub_category_key}")
        return "Tool not found", 404

    if request.method == "POST":
        try:
            data_source = request.form if request.content_type.startswith("multipart/form-data") else request.json
            params = parse_inputs(data_source, tool_config["inputs"])
            logger.warning(params)
            if tool_key not in TOOL_FUNCTIONS:
                logger.error(f'{tool_key} not in tool functions list : {TOOL_FUNCTIONS}')
            calculation_function = TOOL_FUNCTIONS.get(tool_key)
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
@interest_rate_fundamentals_routes.route("/tools/basic-interest-rates-analysis/<tool_key>", methods=["GET", "POST"])
def handle_basic_interest_rate_analysis_tool(tool_key):
    return handle_interest_rate_tool_request(tool_key, "basic-interest-rate-analysis")

@interest_rate_fundamentals_routes.route("/tools/term-structure-construction/<tool_key>", methods=["GET", "POST"])
def handle_term_structure_construction_tool(tool_key):
    return handle_interest_rate_tool_request(tool_key, "term-structure-construction")
