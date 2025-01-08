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
    "t-test": t_test,
    "z-test": z_test,
    "chi-square": chi_square_test,
    "confidence-intervals": calculate_confidence_intervals,
    "anova": anova,
    "simple-regression": simple_regression,
    "multiple-regression": multiple_regression,
    "p-value": calculate_p_value,

    # Probability Tools
    "pdf": calculate_pdf,
    "cdf": calculate_cdf,
    "z-score": calculate_z_score,
    "binomial-distribution": calculate_binomial,
    "poisson-distribution": calculate_poisson,
    "normal-distribution": calculate_normal_distribution,
    "t-distribution": calculate_t_distribution,
}


def handle_statistical_tool_request(tool_key, sub_category_key):
    logger.info(f"Handling request for tool: {tool_key} in {sub_category_key}")
    tool_config = BASIC_STATISTICAL_ANALYSIS_TOOL_CONFIG.get(tool_key)

    if not tool_config:
        logger.warning(f"Tool not found: {tool_key} in {sub_category_key}")
        return "Tool not found", 404

    if request.method == "POST":
        try:
            # Determine source of data: form or JSON
            data_source = request.form if request.content_type.startswith("multipart/form-data") else request.json
            logger.info("Received data:")
            logger.info(data_source)

            params = parse_inputs(data_source, tool_config["inputs"])
            logger.info("Parsed parameters:")
            logger.info(params)

            if "csv_file" in params:
                logger.info("Processing CSV file")
                params = {"dataset": params["csv_file"]}

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


def parse_inputs(data_source, inputs_config):
    """
    Parse and validate the inputs based on the provided configuration.

    Args:
        data_source: Request data (form or JSON).
        inputs_config: List of input configurations.

    Returns:
        A dictionary of parsed parameters.
    """
    params = {}
    for input_field in inputs_config:
        input_id = input_field["id"]
        input_type = input_field["type"]
        optional = input_field.get("optional", False)

        if input_id in data_source:
            raw_value = data_source[input_id]
            logger.info(f"Parsing input {input_id}: {raw_value}")
            if raw_value:
                if input_type == "file":
                    logger.info("Processing file input")
                    # Handle CSV file upload
                    file_data = request.files[input_id] if request.files else None
                    if file_data:
                        params[input_id] = parse_csv(file_data)
                elif input_type == "array":
                    logger.info("Processing array input")
                    params[input_id] = parse_array(raw_value)
                elif input_type == "number":
                    logger.info("Processing number input")
                    params[input_id] = float(raw_value)
                else:
                    params[input_id] = raw_value
            elif not optional:
                raise ValueError(f"Missing required input: {input_id}")

    return params


def parse_array(raw_value):
    """
    Parse an array input, supporting nested arrays or flat arrays.

    Args:
        raw_value: Raw input value (string or list).

    Returns:
        Parsed array.
    """
    if isinstance(raw_value, list):
        return raw_value
    if "[" in raw_value and "]" in raw_value:
        # Parse nested lists
        try:
            return [
                [float(x.strip()) for x in inner_list.strip("[]").split(",") if x.strip()]
                for inner_list in raw_value.strip("[]").split("],[")
            ]
        except ValueError as e:
            logger.error(f"Error parsing nested array: {raw_value}, Error: {e}")
            raise ValueError(f"Invalid format for nested array input: {raw_value}")
    else:
        # Parse flat lists
        return [float(x.strip()) for x in raw_value.strip("[]").split(",") if x.strip()]


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
