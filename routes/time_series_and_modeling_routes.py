from flask import Blueprint, render_template, request, jsonify
from formulas.statistics_formulas import *
from config import logger, parse_csv_and_xlsx, parse_inputs
from configurations.tool_config.statistics.time_series_and_modeling_tool_config import TIME_SERIES_AND_MODELING_TOOL_CONFIG

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
            # Détecter si la requête est multipart/form-data (avec fichiers) ou JSON
            is_multipart = request.content_type.startswith("multipart/form-data")

            # Récupérer les fichiers (s'il y en a)
            files = request.files.to_dict()

            # Récupérer les autres paramètres
            if is_multipart:
                other_params = request.form.to_dict()  # Récupère les inputs classiques (ex: texte, nombres)
            else:
                other_params = request.get_json() or {}  # Récupère les données JSON

            # Fusionner fichiers et autres paramètres en un seul dictionnaire
            data_source = {**other_params, **files}

            logger.info("Received data (merged files and inputs):")
            logger.info(data_source)

            # Parser les inputs en fonction de la config de l'outil
            params = parse_inputs(data_source, tool_config["inputs"])
            logger.info("Parsed parameters:")
            logger.info(params)

            # Si un CSV est présent, on le renomme en "dataset" sans supprimer les autres paramètres
            if "csv_file" in params:
                logger.info("Processing CSV file")
                params["dataset"] = params.pop("csv_file")

            # Appel de la fonction de calcul
            calculation_function = TOOL_FUNCTIONS.get(tool_key)
            if not calculation_function:
                logger.error(f"No calculation logic for tool: {tool_key}")
                return "Calculation logic not implemented", 500

            # Exécuter la fonction et retourner les résultats
            result = calculation_function(**params)
            logger.warning(f"Result: {result}")
            return jsonify(result)

        except Exception as e:
            logger.error(f"Error processing tool {tool_key}: {e}")
            return jsonify({"error": str(e)}), 400

    # Rendu de la page de l'outil
    return render_template("base_tool.html", tool=tool_config)

# Routes for Time Series and Modeling
@time_series_and_modeling_routes.route("/tools/time-series-analysis/<tool_key>", methods=["GET", "POST"])
def handle_time_series_tool(tool_key):
    return handle_time_series_and_modeling_tool_request(tool_key, "time_series_and_modeling")

@time_series_and_modeling_routes.route("/tools/markov-chains-and-random-walks/<tool_key>", methods=["GET", "POST"])
def handle_modeling_tool(tool_key):
    return handle_time_series_and_modeling_tool_request(tool_key, "time_series_and_modeling")
