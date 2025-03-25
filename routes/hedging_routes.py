from flask import Blueprint, render_template, request, jsonify
from formulas.chap_3 import *
from formulas.chap_5 import *
from config import logger
from configurations.tool_config.futures_forwards.hedging_tool_config import (
    HEDGING_TOOL_CONFIG,
)

# Blueprints for forwards and futures
hedging_basics_routes = Blueprint("hedging_basics_routes", __name__)
equity_hedging_routes = Blueprint("equity_hedging_routes", __name__)

TOOL_FUNCTIONS = {
    # Basics Hedging tools
    "dollar_value_of_hedge": compute_dollar_value_of_hedge,
    "tailing_the_hedge_adjustment": compute_tailing_the_hedge_adjustment,
    "optimal_number_futures_contract": compute_optimal_number_futures_contract,
    "minimum_variance_hedge_ratio": compute_minimum_variance_hedge_ratio,
    "optimal_number_of_futures_contracts_tailing_the_hedge": compute_optimal_number_of_futures_contracts_tailing_the_hedge,
    # New equity hedging tools
    "hedge_equity_portfolio": compute_hedge_equity_portfolio,
    "change_beta_portfolio": compute_change_beta_portfolio,
}


# Route for Basics Hedging Tools
@hedging_basics_routes.route(
    "/tools/hedging-basics/<tool_key>", methods=["GET", "POST"]
)
def handle_basics_hedging_tool(tool_key):
    tool_config = HEDGING_TOOL_CONFIG.get(tool_key)

    if not tool_config:
        logger.warning(f"Tool not found: {tool_key}")
        return "Tool not found", 404
    logger.info(request)
    if request.method == "POST":
        logger.info(request)
        data = request.form
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
            return jsonify(result)

        except Exception as e:
            logger.error(f"Error processing tool {tool_key}: {e}")
            return jsonify({"error": str(e)}), 400

    # Render the tool page
    return render_template("base_tool.html", tool=tool_config)


# Route for Equity Hedging Tools
@equity_hedging_routes.route(
    "/tools/equity-hedging/<tool_key>", methods=["GET", "POST"]
)
def handle_equity_hedging_tool(tool_key):
    tool_config = HEDGING_TOOL_CONFIG.get(tool_key)

    if not tool_config:
        logger.warning(f"Tool not found: {tool_key}")
        return "Tool not found", 404

    if request.method == "POST":
        data = request.form
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
            return jsonify(result)

        except Exception as e:
            logger.error(f"Error processing tool {tool_key}: {e}")
            return jsonify({"error": str(e)}), 400

    # Render the tool page
    return render_template("base_tool.html", tool=tool_config)
