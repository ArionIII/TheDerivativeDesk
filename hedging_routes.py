from flask import Blueprint, render_template, request, jsonify
from chap_3 import *
from chap_5 import *
from config import logger
from hedging_tool_config import HEDGING_TOOL_CONFIG

# Blueprints for forwards and futures
hedging_basics_routes = Blueprint("hedging_routes", __name__)

TOOL_FUNCTIONS = {
    # Hedging tools
    "dollar_value_of_hedge": compute_dollar_value_of_hedge,
    "tailing_the_hedge_adjustment": compute_tailing_the_hedge_adjustment,
    "optimal_number_futures_contract": compute_optimal_number_futures_contract,
    "minimum_variance_hedge_ratio": compute_minimum_variance_hedge_ratio,
}

@hedging_basics_routes.route("/tools/hedging/<tool_key>", methods=["GET", "POST"])
def handle_hedging_tool(tool_key):
    tool_config = HEDGING_TOOL_CONFIG.get(tool_key)

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
            
            # Call the corresponding calculation function
            calculation_function = TOOL_FUNCTIONS.get(tool_key)
            if not calculation_function:
                logger.error(f"No calculation logic for tool: {tool_key}")
                return "Calculation logic not implemented", 500
            
            # Execute the function and return results
            result = calculation_function(**params)
            return jsonify({"result": result})
        
        except Exception as e:
            logger.error(f"Error processing tool {tool_key}: {e}")
            return jsonify({"error": str(e)}), 400

    # Render the tool page
    return render_template("base_tool.html", tool=tool_config)