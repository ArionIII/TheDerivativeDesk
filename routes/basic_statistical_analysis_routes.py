import csv
from io import StringIO
from flask import Blueprint, render_template, request, jsonify
from formulas.statistics_formulas import *
from config import logger, parse_csv
from configurations.tool_config.statistics.basic_statistical_analysis_tool_config import BASIC_STATISTICAL_ANALYSIS_TOOL_CONFIG

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
    "comprehensive-basic-analysis": perform_comprehensive_analysis,

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
    logger.info(f"Handling request for tool: {tool_key} in {sub_category_key}")
    tool_config = BASIC_STATISTICAL_ANALYSIS_TOOL_CONFIG.get(tool_key)

    if not tool_config:
        logger.warning(f"Tool not found: {tool_key} in {sub_category_key}")
        return "Tool not found", 404

    if request.method == "POST":
        try:
            params = {}
            # Handle multipart/form-data for file uploads
            if request.content_type.startswith("multipart/form-data"):
                for input_field in tool_config["inputs"]:
                    input_id = input_field["id"]
                    input_type = input_field["type"]

                    if input_type == "file" and input_id in request.files:
                        # Handle CSV file upload
                        csv_file = request.files[input_id]
                        params[input_id] = parse_csv(csv_file)
                    elif input_type == "array" and input_id in request.form:
                        # Handle array from form input
                        raw_array = request.form[input_id]
                        params[input_id] = [
                            float(x.strip()) for x in raw_array.strip("[]").split(",") if x.strip()
                        ]
                    elif input_type == "number" and input_id in request.form:
                        params[input_id] = float(request.form[input_id])
                    elif input_id in request.form:
                        params[input_id] = request.form[input_id]
                    elif not input_field.get("optional"):
                        raise ValueError(f"Missing required input: {input_id}")
            else:
                # Handle application/json for non-file uploads
                data = request.json
                for input_field in tool_config["inputs"]:
                    input_id = input_field["id"]
                    input_type = input_field["type"]

                    if input_id in data:
                        if input_type == "number":
                            params[input_id] = float(data[input_id])
                        elif input_type == "array":
                            if isinstance(data[input_id], list):
                                params[input_id] = data[input_id]
                            elif isinstance(data[input_id], str):
                                clean_data = data[input_id].strip("[]")
                                params[input_id] = [
                                    float(x) for x in clean_data.split(",") if x.strip()
                                ]
                            else:
                                raise ValueError(f"Invalid format for array input: {input_id}")
                        else:
                            params[input_id] = data[input_id]
                    elif not input_field.get("optional"):
                        raise ValueError(f"Missing required input: {input_id}")
            logger.info(params)
            if params.get("csv_file"):
                # ATT : Particulier au traitement statistique
                params= {"dataset": params["csv_file"]}
            else:
                del params["csv_file"]

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
@descriptive_statistics_routes.route("/tools/descriptive-analysis/<tool_key>", methods=["GET", "POST"])
def handle_descriptive_tool(tool_key):
    return handle_statistical_tool_request(tool_key, "descriptive_statistics")

# Routes for Inferential Statistics
@inferential_statistics_routes.route("/tools/inferential-statistics/<tool_key>", methods=["GET", "POST"])
def handle_inferential_tool(tool_key):
    return handle_statistical_tool_request(tool_key, "inferential_statistics")

# Routes for Probability Tools
@probability_tools_routes.route("/tools/probability-tools/<tool_key>", methods=["GET", "POST"])
def handle_probability_tool(tool_key):
    return handle_statistical_tool_request(tool_key, "probability_tools")
