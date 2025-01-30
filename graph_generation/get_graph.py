from flask import Flask, request, send_file
from graph_generation.graph_generator import generate_coefficients_graph, generate_observed_vs_predicted_graph

app = Flask(__name__)

# Dictionnaire qui mappe chaque outil à ses fonctions graphiques
GRAPH_FUNCTIONS = {
    "multiple-regression": {
        1: generate_coefficients_graph,
        2: generate_observed_vs_predicted_graph
    },
    # 🔹 Ajouter ici d'autres outils avec leurs graphiques 🔹
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