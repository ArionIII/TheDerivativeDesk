from flask import Blueprint, render_template, request, jsonify
from config import logger, parse_inputs
from formulas.statistics_formulas import *
from configurations.tool_config.statistics.linear_algebra_and_advanced_calculations_tool_config import (
    LINEAR_ALGEBRA_AND_ADVANCED_CALCULATION_TOOL_CONFIG,
)

# Blueprints
linear_algebra_and_advanced_calculations_routes = Blueprint(
    "linear_algebra_and_advanced_calculations_routes", __name__
)

# Tool Functions
TOOL_FUNCTIONS = {
    "matrix-multiplication": calculate_matrix_multiplication,
    "inverse-matrices": calculate_inverse_matrix,
    "singular-value-decomposition": perform_svd,
    "principal-component-analysis": perform_pca,
    "eigenvalues-eigenvectors": calculate_eigenvalues_eigenvectors,
}


# Generic Request Handler
def handle_tool_request(tool_key, sub_category_key):
    logger.info(f"Handling request for tool: {tool_key} in {sub_category_key}")
    tool_config = LINEAR_ALGEBRA_AND_ADVANCED_CALCULATION_TOOL_CONFIG.get(tool_key)

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


# Routes
@linear_algebra_and_advanced_calculations_routes.route(
    "/tools/linear-algebra-tools/<tool_key>", methods=["GET", "POST"]
)
def handle_linear_algebra_tool(tool_key):
    return handle_tool_request(tool_key, "linera_algebra")


@linear_algebra_and_advanced_calculations_routes.route(
    "/tools/advanced-calculations/<tool_key>", methods=["GET", "POST"]
)
def handle_advanced_calculation_tool(tool_key):
    return handle_tool_request(tool_key, "advanced_calculations")
