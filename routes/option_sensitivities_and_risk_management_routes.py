from flask import Blueprint, render_template, request, jsonify
from config import (
    logger,
    parse_input_data,
    extract_values,
    convert_numpy_types,
    result_tuple_into_dict,
)
from configurations.tool_config.options.option_sensitivities_and_risk_management_tool_config import (
    GREEKS_TOOL_CONFIG,
)
from formulas.options_formulas import *
from graph_generation.get_graph import GRAPH_FUNCTIONS
import markdown

# Blueprint for Greeks
greeks_routes = Blueprint("greeks_routes", __name__)

#  Tool Functions
TOOL_FUNCTIONS = {
    "greeks-visualizer": plot_greeks_sensitivity_formula,
    # "delta-hedging-simulator": simulate_delta_hedging,
    # "greeks-sensitivity-explorer": explore_greeks_sensitivity,
}


#  Generic Request Handler
def handle_greeks_tool_request(tool_key, sub_category_key):
    logger.info(f"Handling request for tool: {tool_key} in {sub_category_key}")
    tool_config = GREEKS_TOOL_CONFIG.get(tool_key)

    if not tool_config:
        logger.warning(f"Tool not found: {tool_key} in {sub_category_key}")
        return "Tool not found", 404

    if request.method == "POST":
        try:
            #  Parse input parameters
            column_names, params = parse_input_data(request, tool_config)
            logger.info(f"Parsed parameters: {params}")

            #  Call the corresponding calculation function
            calculation_function = TOOL_FUNCTIONS.get(tool_key)
            if not calculation_function:
                logger.error(f"No calculation logic for tool: {tool_key}")
                return "Calculation logic not implemented", 500

            logger.info(f"Calling calculation function for {tool_key}")
            result = calculation_function(**params)
            logger.info(f"Calculation result: {result}")

            #  Generate Graphs (if applicable)
            graphs_output = {}
            if tool_key in GRAPH_FUNCTIONS:
                logger.info(f"Generating graphs for tool: {tool_key}")
                result_graph = extract_values(result)
                graph_input = params | result_graph
                graphs = []
                n_graphs = len(GRAPH_FUNCTIONS[tool_key])
                for i in range(n_graphs):
                    graph_function = GRAPH_FUNCTIONS[tool_key][i + 1]
                    graph = graph_function(graph_input)
                    graphs.append(graph)
                graphs_output = {
                    f"graph_{i + 1}": graph for i, graph in enumerate(graphs)
                }

            #  Combine result and graphs
            final_result = result_tuple_into_dict(result) | graphs_output

            logger.info(f"Final result: {final_result}")
            return jsonify(convert_numpy_types(final_result))

        except Exception as e:
            logger.error(f"Error processing tool {tool_key}: {e}")
            return jsonify({"error": str(e)}), 400

    #  Markdown notes if available
    if tool_config.get("note"):
        tool_config["note"] = markdown.markdown(tool_config["note"])
        return render_template("base_tool.html", tool=tool_config)

    #  Render the tool page
    return render_template("base_tool.html", tool=tool_config)


#  Routes
@greeks_routes.route("/tools/options/greeks/<tool_key>", methods=["GET", "POST"])
def handle_greeks_tool(tool_key):
    return handle_greeks_tool_request(tool_key, "greeks")
