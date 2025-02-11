import csv
from io import StringIO
from flask import Blueprint, render_template, request, jsonify
from formulas.statistics_formulas import *
from config import logger, parse_csv_and_xlsx, parse_inputs, extract_values, get_data_source, parse_array, convert_numpy_types
from configurations.tool_config.statistics.basic_statistical_analysis_tool_config import BASIC_STATISTICAL_ANALYSIS_TOOL_CONFIG
from graph_generation.get_graph import GRAPH_FUNCTIONS
from werkzeug.datastructures import FileStorage

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
            logger.info(request.content_type)
            data_source = get_data_source(request)
            logger.info("Received data:")
            logger.info('data source')
            logger.info(data_source)

            # params = parse_inputs(data_source, tool_config["inputs"])

            
            # Sur ce module on a qu'un binaire entre 1 file OU 1 form/json, mais faudra complexifier + tard
            if "json" in data_source and data_source["json"]:
                logger.info("Processing JSON data")
                params = data_source["json"]  
            if "form" in data_source and data_source["form"]:
                parsed_values = []
                logger.info("Processing form data")
                values = data_source["form"].values()
                logger.info(values)
                keys = data_source["form"].keys()
                logger.info(keys)
                for value in values :
                    parsed_values.append(parse_array(value))
                # dataset_value = data_source["form"]["dataset"] 
                params = {k:v for k,v in zip(keys, parsed_values)}
            if "files" in data_source and data_source["files"]:
                csv_value = data_source["files"].get('csv_file')
                if isinstance(csv_value, FileStorage) and csv_value.filename:  # Vérifier si le fichier a un nom valide
                    logger.info(f"Fichier détecté : {csv_value.filename}")
                    logger.info(csv_value)
                    params = {"dataset" : parse_csv_and_xlsx(csv_value)}
            else:
                logger.info("Aucun fichier valide détecté, passage à la suite.") 
            
            logger.error(params)
            # Call the corresponding calculation function
            calculation_function = TOOL_FUNCTIONS.get(tool_key)
            if not calculation_function:
                logger.error(f"No calculation logic for tool: {tool_key}")
                return "Calculation logic not implemented", 500
            logger.error('moment before result')
            result = calculation_function(**params)
            logger.warning("result")
            logger.warning(result)

            #Plotting the graphs if needed
            graphs_output = {}
            if tool_key in GRAPH_FUNCTIONS:
                result_graph = extract_values(result)
                graph_input = params | result_graph
                logger.info(f'graph inputs : {graph_input}')
                logger.info(f"Generating graphs for tool: {tool_key}")
                n_graphs = len(GRAPH_FUNCTIONS[tool_key])
                logger.info(f"Number of graphs: {n_graphs}")
                graphs = []
                for i in range(n_graphs):
                    graph_function = GRAPH_FUNCTIONS[tool_key][i+1]
                    logger.info(f"Graph function: {graph_function}")
                    graph = graph_function(graph_input)
                    graphs.append(graph)
                graphs_output = {f'graph_{i+1}': graph for i, graph in enumerate(graphs)}
                logger.info(f"Graphs: {graphs}")

            # Execute the function and return results
            final_result = result | graphs_output
            logger.info(final_result)
            return jsonify(convert_numpy_types(final_result))

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
