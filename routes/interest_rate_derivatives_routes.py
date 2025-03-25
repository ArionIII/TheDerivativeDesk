from flask import Blueprint, render_template, request, jsonify
from config import (
    logger,
    parse_input_data,
    extract_values,
    convert_numpy_types,
    result_tuple_into_dict,
)
from configurations.tool_config.interest_rates.interest_rate_derivatives_tool_config import (
    INTEREST_RATE_DERIVATIVES_TOOL_CONFIG,
)
from formulas.interest_rates_formulas import *
from graph_generation.get_graph import GRAPH_FUNCTIONS
import markdown

# Blueprint for New Interest Rate Tools
interest_rate_derivatives_routes = Blueprint(
    "interest_rate_derivatives_routes", __name__
)

# Tool Functions
NEW_TOOL_FUNCTIONS = {
    "payoff-of-fra": payoff_of_fra,
    "valuation-of-fra": calculate_valuation_of_fra,
    "forward-rate-calculation": calculate_forward_rate_curve,
    "fra-break-even-rate": calculate_fra_break_even_rate,
    "hedging-with-fra": calculate_hedging_strategy_analysis,
    "calculate-interest-rate-swap-cash-flows": calculate_interest_rate_swap_cash_flows,
    "calculate-interest-rate-swap-valuation": calculate_interest_rate_swap_valuation,
    "calculate-pricing-interest-rate-futures": calculate_pricing_interest_rate_futures,
    "calculate-swap-spread-analysis": calculate_swap_spread_analysis,
    "calculate-swaption-valuation": calculate_swaption_valuation,
    "calculate-basis-swap-analysis": calculate_basis_swap_analysis,
    "calculate-interest-rate-swap-delta-hedging": calculate_interest_rate_swap_delta_hedging,
}


# Generic Request Handler for New Interest Rate Tools
def handle_new_interest_rate_tool_request(tool_key, sub_category_key):
    logger.info(f"Handling request for tool: {tool_key} in {sub_category_key}")
    tool_config = INTEREST_RATE_DERIVATIVES_TOOL_CONFIG.get(tool_key)

    if not tool_config:
        logger.warning(f"Tool not found: {tool_key} in {sub_category_key}")
        return "Tool not found", 404

    if request.method == "POST":
        try:
            # Parse input parameters
            column_names, params = parse_input_data(request, tool_config)
            logger.warning("Params were parsed successfully.")

            # Call the corresponding calculation function
            calculation_function = NEW_TOOL_FUNCTIONS.get(tool_key)
            if not calculation_function:
                logger.error(f"No calculation logic found for tool: {tool_key}")
                return "Calculation logic not implemented", 500

            logger.info("Executing calculation function...")
            result = calculation_function(**params)
            logger.warning("Calculation function executed successfully.")

            # Initialize the final result dictionary
            final_result = result
            logger.info("final result")
            logger.info(final_result)

            # Plotting the graphs if needed
            graphs_output = {}
            if tool_key in GRAPH_FUNCTIONS:
                logger.warning("Tool requires graphs.")
                result_graph = extract_values(result)
                graph_input = (
                    params | result_graph
                )  # Combine input and computed results

                logger.warning(f"Graph input parameters: {graph_input}")
                logger.info(f"Generating graphs for tool: {tool_key}")

                n_graphs = len(GRAPH_FUNCTIONS[tool_key])
                logger.warning(f"Number of graphs to generate: {n_graphs}")

                graphs = []
                for i in range(n_graphs):
                    logger.error("Starting graph generation...")
                    graph_function = GRAPH_FUNCTIONS[tool_key][
                        i + 1
                    ]  # Retrieve correct graph function
                    logger.info(f"Using graph function: {graph_function}")

                    graph = graph_function(graph_input)
                    graphs.append(graph)

                graphs_output = {
                    f"graph_{i + 1}": graph for i, graph in enumerate(graphs)
                }
                logger.info(f"Graphs successfully generated: {graphs}")

            # Convert results into a dictionary format
            result = result_tuple_into_dict(result)
            final_result = result | graphs_output  # Merge result and graphs

            logger.warning(f"Final result: {final_result}")
            return jsonify(convert_numpy_types(final_result))

        except Exception as e:
            logger.error(f"Error processing tool {tool_key}: {e}")
            return jsonify({"error": str(e)}), 400

    # Render the tool page if it's a GET request
    if tool_config.get("note"):
        tool_config["note"] = markdown.markdown(tool_config["note"])
        return render_template("base_tool.html", tool=tool_config)

    return render_template("base_tool.html", tool=tool_config)


# Routes
@interest_rate_derivatives_routes.route(
    "/tools/forward-rate-agreements/<tool_key>", methods=["GET", "POST"]
)
def handle_new_interest_rate_tool(tool_key):
    return handle_new_interest_rate_tool_request(tool_key, "new-interest-rate-tools")


@interest_rate_derivatives_routes.route(
    "/tools/swaps-and-interest-rate-derivatives/<tool_key>", methods=["GET", "POST"]
)
def handle_new_swap_analysis_tool(tool_key):
    return handle_new_interest_rate_tool_request(tool_key, "new-swap-analysis")
