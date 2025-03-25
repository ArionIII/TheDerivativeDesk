from flask import Blueprint, render_template, request, jsonify
from config import logger
from formulas.chap_3 import *
from formulas.chap_5 import *
from configurations.tool_config.futures_forwards.contract_valuation_tool_config import CONTRACT_VALUATION_TOOL_CONFIG

# Blueprints for valuation tools
value_forward_routes = Blueprint("value_forward_routes", __name__)
delivery_timing_decision_routes = Blueprint("delivery_timing_decision_routes", __name__)

TOOL_FUNCTIONS = {
    # Valuation tools
    "value_forward_contracts": calculate_forward_contract_value,
    "delivery_timing_decision": delivery_timing_decision,
}

# Route for Value Forward Contracts
@value_forward_routes.route("/tools/value-forward-contracts/<tool_key>", methods=["GET", "POST"])
def handle_value_forward_contracts(tool_key):
    tool_config = CONTRACT_VALUATION_TOOL_CONFIG.get(tool_key)
    if not tool_config:
        logger.warning(f"Tool not found: {tool_key}")
        return "Tool not found", 404

    if request.method == "POST":
        data = request.form
        try:
            # Parse inputs from the request
            forward_price = float(data.get("forward_price", 0))
            delivery_price = float(data.get("delivery_price", 0))
            risk_free_rate = float(data.get("risk_free_rate", 0))
            time_to_maturity = float(data.get("time_to_maturity", 0))
            long_position = (True if (data.get("position_type") == 'Long') else False)

            # Validate required inputs
            if any(value is None for value in [forward_price, delivery_price, risk_free_rate, time_to_maturity]):
                raise ValueError("All required inputs must be provided.")

            # Perform calculation
            calculation_function = TOOL_FUNCTIONS.get(tool_key)
            if not calculation_function:
                logger.error(f"No calculation logic for tool: {tool_key}")
                return "Calculation logic not implemented", 500

            result = calculation_function(
                forward_price, delivery_price, risk_free_rate, time_to_maturity, long_position
            )

            logger.info(f"Calculation successful for tool: {tool_key}, result: {result}")
            return jsonify(result)

        except Exception as e:
            logger.error(f"Error processing tool {tool_key}: {e}")
            return jsonify({"error": str(e)}), 400

    return render_template("base_tool.html", tool=tool_config)

# Route for Delivery Timing Decision
@delivery_timing_decision_routes.route("/tools/delivery-timing-decision/<tool_key>", methods=["GET", "POST"])
def handle_delivery_timing_decision(tool_key):
    tool_config = CONTRACT_VALUATION_TOOL_CONFIG.get(tool_key)
    if not tool_config:
        logger.warning(f"Tool not found: {tool_key}")
        return "Tool not found", 404

    if request.method == "POST":
        data = request.form
        try:
            # Parse inputs
            cost_of_carry = float(data.get("cost_of_carry", 0))
            convenience_yield = float(data.get("convenience_yield", 0))

            # Validate required inputs
            if any(value is None for value in [cost_of_carry, convenience_yield]):
                raise ValueError("All required inputs must be provided.")

            # Perform calculation
            calculation_function = TOOL_FUNCTIONS.get(tool_key)
            if not calculation_function:
                logger.error(f"No calculation logic for tool: {tool_key}")
                return "Calculation logic not implemented", 500

            result = calculation_function(cost_of_carry, convenience_yield)

            logger.info(f"Calculation successful for tool: {tool_key}, result: {result}")
            return jsonify(result)

        except Exception as e:
            logger.error(f"Error processing tool {tool_key}: {e}")
            return jsonify({"error": str(e)}), 400

    return render_template("base_tool.html", tool=tool_config)
