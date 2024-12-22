from flask import Blueprint, render_template, request, jsonify
from futures_forwards_tool_config import FUTURES_FORWARDS_TOOL_CONFIG
from chap_3 import *
from chap_5 import *
from config import logger

# Blueprints for forwards and futures
forwards_routes = Blueprint("forwards_routes", __name__, url_prefix="/tools/futures-forwards/forward-pricing")
futures_routes = Blueprint("futures_routes", __name__, url_prefix="/tools/futures-forwards/futures-pricing")

# Map tool names to corresponding functions
TOOL_FUNCTIONS = {
    # Forward-pricing tools
    "forward_pricing_no_income": calculate_forward_price_no_income,
    "forward_pricing_with_income": calculate_forward_price_with_income,
    "forward_pricing_with_yield": calculate_forward_price_with_yield,
    "forward_pricing_foreign_currency": calculate_forward_price_foreign_currency,
    
    # Futures-pricing tools
    "futures_pricing_stock_index": calculate_futures_price_stock_index,
    "futures_pricing_with_storage": calculate_futures_price_with_storage,
    "futures_pricing_proportional_costs_yield": calculate_futures_price_with_proportional_costs_and_yield,
    "futures_pricing_nonproportional_costs_yield": calculate_futures_price_with_non_proportional_costs_and_yield,
    "futures_pricing_cost_of_carry": calculate_futures_price_cost_of_carry,
    "futures_pricing_cost_of_carry_yield": calculate_futures_price_cost_of_carry_with_convenience_yield,
}

def handle_tool_request(tool_name):
    # Get the tool configuration
    tool_config = FUTURES_FORWARDS_TOOL_CONFIG.get(tool_name)
    if not tool_config:
        logger.warning(f"Tool not found: {tool_name}")
        return "Tool not found", 404

    if request.method == "POST":
        # Handle POST request
        data = request.json
        try:
            # Map input field IDs to their values
            params = {input["id"]: float(data[input["id"]]) for input in tool_config["inputs"]}
            logger.info(params)
            # Find the corresponding function and execute
            calculation_function = TOOL_FUNCTIONS.get(tool_name)
            logger.info(calculation_function)
            if not calculation_function:
                logger.error(f"No calculation logic for tool: {tool_name}")
                return "Calculation logic not implemented", 500

            # Calculate the result
            result = calculation_function(**params)
            logger.info(f"Calculation successful for tool: {tool_name}, result: {result}")

            return jsonify({"result": result})

        except Exception as e:
            logger.error(f"Error in tool {tool_name}: {e}")
            return jsonify({"error": str(e)}), 400

    # Render the tool page with its configuration
    return render_template("base_tool.html", tool=tool_config)

@forwards_routes.route("/<tool_name>", methods=["GET", "POST"])
def handle_forward_tool(tool_name):
    logger.info(f"Handling forward-pricing tool: {tool_name}")
    return handle_tool_request(tool_name)

@futures_routes.route("/<tool_name>", methods=["GET", "POST"])
def handle_futures_tool(tool_name):
    logger.info(f"Handling futures-pricing tool: {tool_name}")
    return handle_tool_request(tool_name)
