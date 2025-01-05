from flask import Blueprint, render_template, request, jsonify
from formulas.statistics_formulas import *
from config import logger
from configurations.tool_config.statistics.basic_statistical_analysis_config import BASIC_STATISTICAL_ANALYSIS_TOOL_CONFIG

# Blueprints for the three sub-categories
descriptive_statistics_routes = Blueprint("descriptive_statistics_routes", __name__)
inferential_statistics_routes = Blueprint("inferential_statistics_routes", __name__)
probability_tools_routes = Blueprint("probability_tools_routes", __name__)

TOOL_FUNCTIONS = {
    # Descriptive Statistics
    "mean": calculate_mean,
    "median": calculate_median,
    "mode": calculate_mode,
    "range": calculate_range,
    "iqr": calculate_iqr,
    "skewness": calculate_skewness,
    "kurtosis": calculate_kurtosis,

    # Inferential Statistics
    "t_test": t_test,
    "z_test": z_test,
    "chi_square_test": chi_square_test,
    "confidence_intervals": calculate_confidence_intervals,
    "anova": anova,

    # Probability Tools
    "pdf_cdf": calculate_pdf_cdf,
    "z_score": calculate_z_score,
}

# Common route handler
def handle_statistical_tool_request(tool_key, sub_category_key):
    tool_config = BASIC_STATISTICAL_ANALYSIS_TOOL_CONFIG.get(sub_category_key, {}).get("tools", {}).get(tool_key)

    if not tool_config:
        logger.warning(f"Tool not found: {tool_key} in {sub_category_key}")
        return "Tool not found", 404

    if request.method == "POST":
        data = request.json
        try:
            # Parse inputs
            params = {
                input["id"]: float(data[input["id"]]) 
                if input["type"] == "number" else data[input["id"]]
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

# Routes for Descriptive Statistics
@descriptive_statistics_routes.route("/tools/statistical-analysis/basic-statistical-analysis/<tool_key>", methods=["GET", "POST"])
def handle_descriptive_tool(tool_key):
    return handle_statistical_tool_request(tool_key, "descriptive_statistics")

# Routes for Inferential Statistics
@inferential_statistics_routes.route("/tools/statistical-analysis/inferential/<tool_key>", methods=["GET", "POST"])
def handle_inferential_tool(tool_key):
    return handle_statistical_tool_request(tool_key, "inferential_statistics")

# Routes for Probability Tools
@probability_tools_routes.route("/tools/statistical-analysis/probability/<tool_key>", methods=["GET", "POST"])
def handle_probability_tool(tool_key):
    return handle_statistical_tool_request(tool_key, "probability_tools")
