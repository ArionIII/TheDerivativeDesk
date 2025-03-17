from flask import Blueprint, render_template, request, jsonify
from config import logger
from configurations.tool_config.futures_forwards.futures_forwards_pricing_tool_config import FUTURES_FORWARDS_TOOL_CONFIG
from configurations.tool_config.futures_forwards.hedging_tool_config import HEDGING_TOOL_CONFIG
from configurations.tool_config.futures_forwards.contract_valuation_tool_config import CONTRACT_VALUATION_TOOL_CONFIG
from configurations.tool_config.interest_rates.interest_rate_derivatives_tool_config import INTEREST_RATE_DERIVATIVES_TOOL_CONFIG
from configurations.tool_config.interest_rates.interest_rate_fundamentals_tool_config import INTEREST_RATE_FUNDAMENTALS_TOOL_CONFIG
from configurations.tool_config.statistics.basic_statistical_analysis_tool_config import BASIC_STATISTICAL_ANALYSIS_TOOL_CONFIG
from configurations.tool_config.statistics.linear_algebra_and_advanced_calculations_tool_config import LINEAR_ALGEBRA_AND_ADVANCED_CALCULATION_TOOL_CONFIG
from configurations.tool_config.statistics.simulation_and_bayesian_analysis_config import SIMULATION_AND_BAYESIAN_ANALYSIS_TOOL_CONFIG
from configurations.tool_config.statistics.time_series_and_modeling_tool_config import TIME_SERIES_AND_MODELING_TOOL_CONFIG 
from configurations.tool_config.options.option_sensitivities_and_risk_management_tool_config import GREEKS_TOOL_CONFIG
from configurations.tool_config.options.options_pricing_tool_config import OPTION_PRICING_TOOL_CONFIG


ALL_TOOLS = FUTURES_FORWARDS_TOOL_CONFIG | HEDGING_TOOL_CONFIG | CONTRACT_VALUATION_TOOL_CONFIG | INTEREST_RATE_DERIVATIVES_TOOL_CONFIG | INTEREST_RATE_FUNDAMENTALS_TOOL_CONFIG | BASIC_STATISTICAL_ANALYSIS_TOOL_CONFIG | LINEAR_ALGEBRA_AND_ADVANCED_CALCULATION_TOOL_CONFIG | SIMULATION_AND_BAYESIAN_ANALYSIS_TOOL_CONFIG | TIME_SERIES_AND_MODELING_TOOL_CONFIG | OPTION_PRICING_TOOL_CONFIG | GREEKS_TOOL_CONFIG  


search_routes = Blueprint("search", __name__)

@search_routes.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").strip().lower()
    
    if not query:
        return render_template("search.html", results=[])

    query_tokens = query.split()  # Sépare la requête en mots-clés
    results = []

    for tool_key, tool in ALL_TOOLS.items():
        score = 0

        # Normalisation des titres, descriptions et autres champs
        title = tool["title"].lower()
        description = tool["description"].lower()
        outputs = [output.lower() for output in tool.get("outputs", [])]
        graphs = [graph["name"].lower() for graph in tool.get("graphs", [])]
        inputs = [inp["label"].lower() for inp in tool.get("inputs", [])]

        title_tokens = title.split()
        description_tokens = description.split()
        output_tokens = [token for output in outputs for token in output.split()]
        graph_tokens = [token for graph in graphs for token in graph.split()]
        input_tokens = [token for inp in inputs for token in inp.split()]

        # Exact match scoring
        if query == title:
            score += 200
        if query == description:
            score += 100
        if query in outputs:
            score += 80
        if query in graphs:
            score += 80
        if query in inputs:
            score += 30

        # Token matching scoring
        for token in query_tokens:
            if token in title_tokens:
                score += 30
            if token in description_tokens:
                score += 20
            if token in output_tokens:
                score += 15
            if token in graph_tokens:
                score += 15
            if token in input_tokens:
                score += 5

        # Ajouter le résultat si score > 0
        if score > 0:
            results.append({
                "name": tool["title"],
                "url": tool['url'],
                "description": tool["description"],
                "score": score
            })

    # Tri des résultats : 
    # 1. D'abord par score (décroissant)
    # 2. Si égalité, on priorise l'exact match sur le titre
    results = sorted(results, key=lambda x: (-x["score"], x["name"] != query))

    return render_template("search.html", results=results, query=query)


@search_routes.route("/suggest", methods=["GET"])
def suggest():
    logger.info("Handling suggestion request")
    query = request.args.get("q", "").strip().lower()

    if not query:
        return jsonify([])

    query_tokens = query.split()
    suggestions = []

    for tool_key, tool in ALL_TOOLS.items():
        score = 0

        # Normalisation des titres, descriptions et autres champs
        title = tool["title"].lower()
        description = tool["description"].lower()
        outputs = [output.lower() for output in tool.get("outputs", [])]
        graphs = [graph["name"].lower() for graph in tool.get("graphs", [])]
        inputs = [inp["label"].lower() for inp in tool.get("inputs", [])]

        title_tokens = title.split()
        description_tokens = description.split()
        output_tokens = [token for output in outputs for token in output.split()]
        graph_tokens = [token for graph in graphs for token in graph.split()]
        input_tokens = [token for inp in inputs for token in inp.split()]

        # Exact match scoring
        if query == title:
            score += 100
        if query == description:
            score += 70
        if query in outputs:
            score += 50
        if query in graphs:
            score += 50
        if query in inputs:
            score += 20

        # Token matching scoring
        for token in query_tokens:
            if token in title_tokens:
                score += 20
            if token in description_tokens:
                score += 15
            if token in output_tokens:
                score += 10
            if token in graph_tokens:
                score += 10
            if token in input_tokens:
                score += 5

        # Match partiel (progressivité) : On vérifie si la requête est un préfixe d'un mot dans les données
        if any(title_word.startswith(query) for title_word in title_tokens):
            score += 50
        if any(desc_word.startswith(query) for desc_word in description_tokens):
            score += 30
        if any(output_word.startswith(query) for output_word in output_tokens):
            score += 20
        if any(graph_word.startswith(query) for graph_word in graph_tokens):
            score += 20
        if any(input_word.startswith(query) for input_word in input_tokens):
            score += 10

        # Ajouter le résultat si score > 0
        if score > 0:
            suggestions.append({
                "name": tool["title"],
                "url": tool["url"],
                "description": tool["description"],
                "score": score
            })

    # Trier les suggestions par score (décroissant) et ensuite par ordre alphabétique en cas d'égalité
    suggestions = sorted(suggestions, key=lambda x: (-x["score"], x["name"]))

    logger.info(f"Returning {len(suggestions)} suggestions")
    logger.info(suggestions)
    
    return jsonify(suggestions)

