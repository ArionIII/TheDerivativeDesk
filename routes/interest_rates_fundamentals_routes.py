from flask import Blueprint, render_template, request, jsonify
from config import logger, parse_inputs, parse_input_data, extract_values, convert_numpy_types, result_tuple_into_dict
from configurations.tool_config.interest_rates.interest_rate_fundamentals_tool_config import INTEREST_RATE_FUNDAMENTALS_TOOL_CONFIG
from formulas.interest_rates_formulas import *  
from graph_generation.get_graph import GRAPH_FUNCTIONS
import markdown
# Blueprint for Interest Rate Fundamentals
interest_rate_fundamentals_routes = Blueprint("interest_rate_fundamentals_routes", __name__)

# Tool Functions
TOOL_FUNCTIONS = {
    "continuous-compounding-rate": continuous_compounding_rate,
    "m-to-continuous-compounding-rate": m_compounding_rate,
    "zero-rate-curve": zero_rate_curve,
    "bond-pricing": bond_pricing,
    "determining-zero-rates": determining_zero_rates,
    "extending-libor-curve-with-swap-rates": extending_libor_curve_with_swap_rates,
    "extending-zero-curve-with-fra": extending_zero_curve_with_fra,
    "payoff-of-fra": payoff_of_fra,
    "duration-and-convexity": duration_and_convexity,
}

# Generic Request Handler
def handle_interest_rate_tool_request(tool_key, sub_category_key):
    logger.info(f"Handling request for tool: {tool_key} in {sub_category_key}")
    tool_config = INTEREST_RATE_FUNDAMENTALS_TOOL_CONFIG.get(tool_key)

    if not tool_config:
        logger.warning(f"Tool not found: {tool_key} in {sub_category_key}")
        return "Tool not found", 404

    if request.method == "POST":
        try:
            # Parse input parameters
            column_names, params = parse_input_data(request, tool_config)
            logger.warning("params were parsed")

            # Call the corresponding calculation function
            calculation_function = TOOL_FUNCTIONS.get(tool_key)
            if not calculation_function:
                logger.error(f"No calculation logic for tool: {tool_key}")
                return "Calculation logic not implemented", 500
            logger.error('moment before result')
            result = calculation_function(**params)
            logger.warning("result")
            logger.warning(result)
            final_result = result
            # Plotting the graphs if needed
            graphs_output = {}
            if tool_key in GRAPH_FUNCTIONS:
                logger.warning('TOOL KEY IN GRAPH FUNCTIONS')
                result_graph = extract_values(result)
                graph_input = params | result_graph
                logger.warning(f'graph inputs : {graph_input}')
                logger.info(f"Generating graphs for tool: {tool_key}")
                n_graphs = len(GRAPH_FUNCTIONS[tool_key])
                logger.warning(f"Number of graphs: {n_graphs}")
                graphs = []
                for i in range(n_graphs):
                    logger.error("ENTERING GRAPH PLOTTING")
                    graph_function = GRAPH_FUNCTIONS[tool_key][i+1]
                    logger.info(f"Graph function: {graph_function}")
                    graph = graph_function(graph_input)
                    graphs.append(graph)
                graphs_output = {f'graph_{i+1}': graph for i, graph in enumerate(graphs)}
                logger.info(f"Graphs: {graphs}")

                logger.error(result)
                logger.error(graphs_output)
            result = result_tuple_into_dict(result)
            final_result = result | graphs_output

            # Execute the function and return results
            logger.warning(final_result)
            return jsonify(convert_numpy_types(final_result))

        except Exception as e:
            logger.error(f"Error processing tool {tool_key}: {e}")
            return jsonify({"error": str(e)}), 400

    if tool_config.get("note"):
        tool_config['note'] = markdown.markdown(tool_config['note'])
        return render_template("base_tool.html", tool=tool_config)
    # Render the tool page
    return render_template("base_tool.html", tool=tool_config)


# Routes
@interest_rate_fundamentals_routes.route("/tools/basic-interest-rates-analysis/<tool_key>", methods=["GET", "POST"])
def handle_basic_interest_rate_analysis_tool(tool_key):
    return handle_interest_rate_tool_request(tool_key, "basic-interest-rate-analysis")

@interest_rate_fundamentals_routes.route("/tools/term-structure-construction/<tool_key>", methods=["GET", "POST"])
def handle_term_structure_construction_tool(tool_key):
    return handle_interest_rate_tool_request(tool_key, "term-structure-construction")
