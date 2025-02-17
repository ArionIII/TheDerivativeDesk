from flask import Flask, request, send_file
from graph_generation.graph_generator import *

app = Flask(__name__)

# Dictionnaire qui mappe chaque outil à ses fonctions graphiques
GRAPH_FUNCTIONS = {
    "multiple-regression": {
        1: generate_coefficients_graph,
        2: generate_observed_vs_predicted_graph
    },
    "determining-zero-rates": {
        1: generate_zero_rates_curve,
        2: generate_zero_rates_vs_bond_prices,
    },
    "duration-and-convexity": {
        1:generate_duration_contribution_graph,
        2:generate_cash_flow_discounting_graph,
    },
    "extending-libor-curve-with-swap-rates": {
        1:generate_extended_zero_rate_curve_graph_fixed,
    },
    "extending-zero-curve-with-fra": {
        1:generate_extended_zero_rate_curve_graph_fra,
    },
    "payoff-of-fra": {
        1:generate_fra_payoff_evolution_graph,
        2:generate_fra_fixed_vs_floating_rates_graph,
    },
    "forward-rate-calculation": {
        1:generate_forward_rate_curve,
        2:generate_spot_vs_forward_comparison,
    },
    "valuation-of-fra": {
        1:plot_fra_payoff,
        2:plot_fra_fixed_vs_forward
    },
    # "fra-break-even-rate": {
    #     1:plot_fra_break_even_vs_forward,
    #     2:plot_fra_break_even_vs_maturity,
    # }
}

@app.route("/api/get-graph")
def get_graph():
    tool = request.args.get("tool")
    graph_id = int(request.args.get("graph_id", 1))

    # Vérifier si l'outil a des graphiques définis
    if tool in GRAPH_FUNCTIONS and graph_id in GRAPH_FUNCTIONS[tool]:
        return GRAPH_FUNCTIONS[tool][graph_id]()  # Exécute la bonne fonction
    else:
        return "Graph not found", 404