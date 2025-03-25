import requests
import itertools
import json
from flask import Blueprint, request, jsonify
import csv 
import os
import random
import string

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
from configurations.tool_config.options.options_pricing_tool_config import OPTION_PRICING_TOOL_CONFIG

# -----------------------------------------------------------------------------
# 1) RÉUNIR TOUTES LES CONFIGURATIONS DE TOOLS
# -----------------------------------------------------------------------------

ALL_TOOLS = FUTURES_FORWARDS_TOOL_CONFIG | HEDGING_TOOL_CONFIG | CONTRACT_VALUATION_TOOL_CONFIG | INTEREST_RATE_DERIVATIVES_TOOL_CONFIG | INTEREST_RATE_FUNDAMENTALS_TOOL_CONFIG | BASIC_STATISTICAL_ANALYSIS_TOOL_CONFIG | LINEAR_ALGEBRA_AND_ADVANCED_CALCULATION_TOOL_CONFIG | SIMULATION_AND_BAYESIAN_ANALYSIS_TOOL_CONFIG | TIME_SERIES_AND_MODELING_TOOL_CONFIG | OPTION_PRICING_TOOL_CONFIG  
BASE_URL = "http://localhost:10000"

# Créer le Blueprint Flask
test_bp = Blueprint('test', __name__)

# -----------------------------------------------------------------------------
# GÉNÉRATION DES INPUTS POUR CHAQUE TOOL
# -----------------------------------------------------------------------------

def generate_input_payloads(tool_config):
    input_defs = tool_config.get("inputs", [])
    input_ids = []
    input_values_list = []

    for inp in input_defs:
        # 👉 Si l'input contient "data_target", on le saute (car optionnel + remplace une autre valeur)
        if inp.get("data_target"):
            logger.info(f"Skipping input '{inp['id']}' because it's a file upload input")
            continue

        input_ids.append(inp["id"])

        if inp["type"] == "select":
            options = inp.get("options", [])
            input_values_list.append(options)

        elif inp["type"] == "number":
            placeholder = inp.get("placeholder", None)
            if placeholder is not None:
                try:
                    step = inp.get("step", None)
                    if step == "any":
                        placeholder = float(placeholder.replace("(", "").replace(")", "").split()[0])
                except:
                    pass
                input_values_list.append([placeholder])
            else:
                input_values_list.append([None])

        elif inp["type"] == "array":
            placeholder = inp.get("placeholder", None)
            if placeholder:
                input_values_list.append([[placeholder]])
            else:
                input_values_list.append([[0]])

        else:
            input_values_list.append([None])

    # Produit cartésien des inputs → toutes les combinaisons possibles
    all_combos = list(itertools.product(*input_values_list))

    payloads = []
    for combo in all_combos:
        payload = {}
        for idx, val in enumerate(combo):
            payload[input_ids[idx]] = val
        
        # 👉 Supprimer les inputs de type "file" car ils sont facultatifs
        for inp in input_defs:
            if inp.get("type") == "file" and inp.get("id") in payload:
                del payload[inp.get("id")]
        
        payloads.append(payload)

    return payloads


# -----------------------------------------------------------------------------
# TEST DES TOOLS (APPEL API)
# -----------------------------------------------------------------------------

def test_tool(tool_key, tool_config):
    url_endpoint = tool_config.get("url")
    if not url_endpoint:
        return [{
            "tool": tool_key,
            "input_payload": None,
            "status_code": None,
            "passed": False,
            "error": f"No URL for tool {tool_key}"
        }]

    full_url = BASE_URL + url_endpoint
    payloads = generate_input_payloads(tool_config)
    expected_result = tool_config.get("base_inputs_result", None)

    results = []

    for payload in payloads:
        try:
            resp = requests.post(full_url, json=payload, timeout=10)
            status_code = resp.status_code
            
            #  Si le statut est 200 => Success
            if 200 <= status_code < 300:
                if expected_result is not None:
                    actual_result = resp.json()
                    if actual_result == expected_result:
                        test_passed = True
                        error_msg = None
                    else:
                        test_passed = False
                        error_msg = f"Output mismatch: Expected {expected_result}, got {actual_result}"
                else:
                    test_passed = True
                    error_msg = None

            #  Si le statut est ≥ 400 => Échec + Capture de l'erreur détaillée
            else:
                test_passed = False

                # 👉 Si la réponse est JSON :
                try:
                    error_detail = resp.json().get("error", resp.json().get("message", ""))
                except:
                    # 👉 Si ce n'est pas JSON → texte brut
                    error_detail = resp.text
                
                error_msg = f"HTTP Error {status_code}: {error_detail}"

            results.append({
                "tool": tool_key,
                "input_payload": payload,
                "status_code": status_code,
                "passed": test_passed,
                "error": error_msg
            })

        except Exception as e:
            results.append({
                "tool": tool_key,
                "input_payload": payload,
                "status_code": None,
                "passed": False,
                "error": str(e)
            })

    return results

# -----------------------------------------------------------------------------
# ROUTE FLASK
# -----------------------------------------------------------------------------

# Crée un dossier de sortie s'il n'existe pas
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

@test_bp.route('/test-tools', methods=['POST'])
def run_tests():
    try:
        data = request.get_json()
        tool_key = data.get('tool_key')
        all_results = []
        done = 0
        total_length = len(ALL_TOOLS.items())

        if tool_key:
            if tool_key in ALL_TOOLS:
                tool_results = test_tool(tool_key, ALL_TOOLS[tool_key])
                all_results.extend(tool_results)
            else:
                return jsonify({"error": f"Tool '{tool_key}' not found"}), 404
        else:
            for tool_key, tool_cfg in ALL_TOOLS.items():
                # logger.warning(f"Testing tool: {tool_key}")
                tool_results = test_tool(tool_key, tool_cfg)
                # logger.info(f"Done {done + 1}/{total_length}")
                all_results.extend(tool_results)
                done += 1

        # Rapport final
        total_tests = len(all_results)
        passed_tests = sum(1 for r in all_results if r["passed"])
        failed_tests = total_tests - passed_tests

        report = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "details": all_results
        }

        #  Écriture du fichier CSV propre
        csv_file = os.path.join(OUTPUT_DIR, generate_unique_filename_csv())
        write_csv_report(all_results, csv_file)

        logger.info(f" Test report saved to {csv_file}")

        return jsonify(report), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------------------------------------
# FONCTION POUR CRÉER LE FICHIER CSV
# -----------------------------------------------------------------------------


def generate_unique_filename_csv(prefix="test_report"):
    """Génère un nom de fichier unique avec un identifiant aléatoire."""
    random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"{prefix}_{random_suffix}.csv"

def write_csv_report(results, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        #  En-tête des colonnes
        writer.writerow([
            "Tool Name",
            "Input Payload",
            "Status Code",
            "Passed",
            "Error"
        ])

        for result in results:
            tool_name = result.get("tool", "")
            input_payload = json.dumps(result.get("input_payload", {}), indent=None)
            status_code = result.get("status_code", "")
            passed = "" if result.get("passed") else ""
            error = result.get("error", "")

            writer.writerow([
                tool_name,
                input_payload,
                status_code,
                passed,
                error
            ])