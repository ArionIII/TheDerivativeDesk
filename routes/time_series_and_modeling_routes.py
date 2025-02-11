from flask import Blueprint, render_template, request, jsonify
from formulas.statistics_formulas import *
from config import logger, parse_csv_and_xlsx, extract_values, get_data_source, parse_array, convert_numpy_types, process_uploaded_files_with_target, parse_input_data, reassign_params_if_header
from configurations.tool_config.statistics.time_series_and_modeling_tool_config import TIME_SERIES_AND_MODELING_TOOL_CONFIG
from graph_generation.get_graph import GRAPH_FUNCTIONS

# Blueprint for Time Series and Modeling
time_series_and_modeling_routes = Blueprint("time_series_and_modeling_routes", __name__)

TOOL_FUNCTIONS = ({
    # Time Series and Modeling
    "moving-averages": calculate_moving_averages,
    "exponential-smoothing": calculate_exponential_smoothing,
    "autocorrelation": calculate_autocorrelation,
    "transition-matrices": calculate_transition_matrices,
    "random-walk-simulation": simulate_random_walk,
    "AR-MA-ARMA-previsions": forecast_series,
    "log-returns-calculator": compute_log_returns_csv_xlsx,
})


def handle_time_series_and_modeling_tool_request(tool_key, sub_category_key):
    logger.info(f"Handling request for tool: {tool_key} in {sub_category_key}")
    tool_config = TIME_SERIES_AND_MODELING_TOOL_CONFIG.get(tool_key)

    if not tool_config:
        logger.warning(f"Tool not found: {tool_key} in {sub_category_key}")
        return "Tool not found", 404

    if request.method == "POST":
        try:
            column_names, params = parse_input_data(request, tool_config)
            logger.warning(column_names)
            if column_names:
                params, column_names = reassign_params_if_header(tool_config, params, column_names)
            logger.warning("Params were parsed")
            logger.error(params)
            logger.error(column_names)
            # Call the corresponding calculation function
            calculation_function = TOOL_FUNCTIONS.get(tool_key)
            if not calculation_function:
                logger.error(f"No calculation logic for tool: {tool_key}")
                return "Calculation logic not implemented", 500
            
            logger.error("Moment before result")
            result = calculation_function(**params)
            logger.warning("Result")
            logger.warning(result)

            final_result = result

            # Plotting the graphs if needed
            graphs_output = {}
            if tool_key in GRAPH_FUNCTIONS:
                result_graph = extract_values(result)
                graph_input = params | result_graph
                logger.warning(f"Graph inputs: {graph_input}")
                logger.info(f"Generating graphs for tool: {tool_key}")
                n_graphs = len(GRAPH_FUNCTIONS[tool_key])
                logger.warning(f"Number of graphs: {n_graphs}")
                graphs = []
                for i in range(n_graphs):
                    graph_function = GRAPH_FUNCTIONS[tool_key][i+1]
                    logger.info(f"Graph function: {graph_function}")
                    graph = graph_function(graph_input)
                    graphs.append(graph)
                graphs_output = {f'graph_{i+1}': graph for i, graph in enumerate(graphs)}
                logger.info(f"Graphs: {graphs}")
                final_result = result | graphs_output

            # Execute the function and return results
            
            logger.warning("final_result")
            logger.warning(final_result)
            return jsonify(convert_numpy_types(final_result))

        except Exception as e:
            logger.error(f"Error processing tool {tool_key}: {e}")
            return jsonify({"error": str(e)}), 400

    # Render the tool page
    return render_template("base_tool.html", tool=tool_config)


# Routes for Time Series and Modeling
@time_series_and_modeling_routes.route("/tools/time-series-analysis/<tool_key>", methods=["GET", "POST"])
def handle_time_series_tool(tool_key):
    return handle_time_series_and_modeling_tool_request(tool_key, "time_series_and_modeling")

@time_series_and_modeling_routes.route("/tools/markov-chains-and-random-walks/<tool_key>", methods=["GET", "POST"])
def handle_modeling_tool(tool_key):
    return handle_time_series_and_modeling_tool_request(tool_key, "time_series_and_modeling")
