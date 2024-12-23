from flask import Blueprint, render_template, request, jsonify
from chap_3 import *
from chap_5 import *
from config import logger
from contract_valuation_tool_config import CONTRACT_VALUATION_TOOL_CONFIG

# Blueprints for forwards and futures
value_forward_routes = Blueprint("value_forward_routes", __name__)

TOOL_FUNCTIONS = {
    # Valuation tools
    "value_forward_contracts": calculate_forward_contract_value,
}



@value_forward_routes.route("/tools/value-forward-contracts/<tool_key>", methods=["GET", "POST"])
def handle_value_forward_contract_tool(tool_key):
    tool_config = CONTRACT_VALUATION_TOOL_CONFIG.get(tool_key)

    if not tool_config:
        logger.warning(f"Tool not found: {tool_key}")
        return "Tool not found", 404

    if request.method == "POST":
        data = request.json
        try:
            # Parse inputs
            params = {
                input["id"]: float(data[input["id"]])
                for input in tool_config["inputs"]
                if not input.get("optional") or data.get(input["id"])
            }

            # Default long_position to True if not provided
            long_position = data.get("long_position", "true").lower() == "true"

            # Add long_position to params
            params["long_position"] = long_position

            # Execute calculation function
            calculation_function = TOOL_FUNCTIONS.get(tool_key)
            if not calculation_function:
                logger.error(f"No calculation logic for tool: {tool_key}")
                return "Calculation logic not implemented", 500

            result = calculation_function(**params)
            return jsonify(result)

        except Exception as e:
            logger.error(f"Error processing tool {tool_key}: {e}")
            return jsonify({"error": str(e)}), 400

    # Render the tool page
    return render_template("base_tool.html", tool=tool_config)