from flask import Blueprint, render_template, request, jsonify
from config import logger, parse_inputs
from configurations.tool_config.statistics.simulation_and_bayesian_analysis_config import (
    SIMULATION_AND_BAYESIAN_ANALYSIS_TOOL_CONFIG,
)
from formulas.statistics_formulas import *

# Blueprint for Time Series and Modeling
simulation_and_bayesian_analysis_routes = Blueprint(
    "simulation_and_bayesian_analysis_routes", __name__
)

TOOL_FUNCTIONS = {
    "monte-carlo": perform_monte_carlo_simulations,
    "bayesian-updating": perform_bayesian_updating,
}


def handle_simulation_and_bayesian_analysis_tool_request(tool_key, sub_category_key):
    logger.info(f"Handling request for tool: {tool_key} in {sub_category_key}")
    tool_config = SIMULATION_AND_BAYESIAN_ANALYSIS_TOOL_CONFIG.get(tool_key)

    if not tool_config:
        logger.warning(f"Tool not found: {tool_key} in {sub_category_key}")
        return "Tool not found", 404

    if request.method == "POST":
        try:
            data_source = (
                request.form
                if request.content_type.startswith("multipart/form-data")
                else request.json
            )
            params = parse_inputs(data_source, tool_config["inputs"])
            calculation_function = TOOL_FUNCTIONS.get(tool_key)
            if not calculation_function:
                return "Calculation logic not implemented", 500
            result = calculation_function(**params)
            return jsonify(result)
        except Exception as e:
            logger.error(f"Error processing tool {tool_key}: {e}")
            return jsonify({"error": str(e)}), 400

    return render_template("base_tool.html", tool=tool_config)


@simulation_and_bayesian_analysis_routes.route(
    "/tools/monte-carlo-simulations/<tool_key>", methods=["GET", "POST"]
)
def handle_monte_carlo_simulation_tool(tool_key):
    return handle_simulation_and_bayesian_analysis_tool_request(
        tool_key, "simulation_and_bayesian_analysis"
    )


@simulation_and_bayesian_analysis_routes.route(
    "/tools/bayesian-analysis/<tool_key>", methods=["GET", "POST"]
)
def handle_bayesian_analysis_tool(tool_key):
    return handle_simulation_and_bayesian_analysis_tool_request(
        tool_key, "simulation_and_bayesian_analysis"
    )
