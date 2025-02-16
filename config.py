# colored_logger.py
import logging
import os
import csv
from io import StringIO
from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import json
import numpy as np
from werkzeug.datastructures import FileStorage
import ipdb


class LogColors:
    DEBUG = "\033[94m"  # Blue
    INFO = "\033[92m"   # Green
    WARNING = "\033[93m"  # Yellow
    ERROR = "\033[91m"   # Red
    CRITICAL = "\033[95m"  # Magenta
    RESET = "\033[0m"   # Reset to default color

class ColoredFormatter(logging.Formatter):
    def __init__(self, fmt):
        super().__init__()
        self.FORMATS = {
            logging.DEBUG: f"{LogColors.DEBUG}DEBUG: %(message)s{LogColors.RESET}",
            logging.INFO: f"{LogColors.INFO}INFO: %(message)s{LogColors.RESET}",
            logging.WARNING: f"{LogColors.WARNING}WARNING: %(message)s{LogColors.RESET}",
            logging.ERROR: f"{LogColors.ERROR}ERROR: %(message)s{LogColors.RESET}",
            logging.CRITICAL: f"{LogColors.CRITICAL}CRITICAL: %(message)s{LogColors.RESET}",
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, "%(message)s")
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def get_colored_logger(name="ColoredLogger"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(ColoredFormatter("%(levelname)s: %(message)s"))
    logger.addHandler(ch)
    return logger

logger = get_colored_logger("AppLogger")

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key")
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/TheDerivativeDesk")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your_jwt_secret_key")


def parse_csv_and_xlsx(file):
    """
    Parse CSV or XLSX file content into a list of numbers (if single column)
    or into a dictionary of lists (if multiple columns).

    Automatically detects:
    - The file type (CSV or XLSX).
    - The separator (",", ";", or tab "\t") for CSV files.
    - Whether to skip the header by checking if the first row contains strings.

    Parameters:
    - file: The uploaded file.

    Returns:
    - List of floats if it's a single-column file.
    - Dictionary {column_name: list of floats} if multiple columns.
    """
    try:
        # Déterminer le format du fichier
        filename = file.filename.lower()
        file_extension = os.path.splitext(filename)[1]  # Récupérer l'extension du fichier
        logger.warning(filename)
        if file_extension == ".csv":
            logger.info("Loading CSV file")
            # Lire le contenu du fichier CSV
            file_content = file.read().decode('utf-8')

            # Détecter automatiquement le séparateur
            first_line = file_content.split("\n")[0]
            separator = "," if "," in first_line else ";" if ";" in first_line else "\t"
            logger.info(f"Detected separator: {separator}")

            # Charger le fichier avec pandas
            df = pd.read_csv(StringIO(file_content), sep=separator, header=None)

        elif file_extension in [".xls", ".xlsx"]:
            logger.info("Loading XLSX file")
            # Charger le fichier XLSX avec pandas
            df = pd.read_excel(file, header=None, engine="openpyxl")

        else:
            raise ValueError("Unsupported file format. Only CSV and XLSX are allowed.")
        # Vérifier si la première ligne contient des strings (header) ou seulement des nombres
        first_row = df.iloc[0].astype(str)  # Convertir en string pour test
        contains_strings = any(not value.replace(".", "", 1).isdigit() for value in first_row)
        logger.info(f"Contains strings: {contains_strings}")

        # Si la première ligne contient des strings, on la considère comme un header et on la saute
        if contains_strings:
            if file_extension == ".csv":
                df = pd.read_csv(StringIO(file_content), sep=separator, header=0)
            elif file_extension in [".xls", ".xlsx"]:
                df = pd.read_excel(file, header=0, engine="openpyxl")

        logger.info(f"Loaded Data:\n{df}")
        ##############################
        # Remplacer les virgules par des points pour conversion correcte
        df = df.applymap(lambda x: x.replace(",", ".") if isinstance(x, str) else x)
        df = df.astype(float)

        # Si une seule colonne, retourner une liste de nombres
        if df.shape[1] == 1:
            return ([], df.iloc[:, 0].dropna().tolist())

        # Si plusieurs colonnes, retourner un dictionnaire {nom_colonne: liste de valeurs}
        logger.warning('multiple columns')
        return (df.columns.tolist(), [df[col].dropna().tolist() for col in df.columns])

    except Exception as e:
        logger.error(f"Error parsing file: {e}")
        raise ValueError("Invalid file content")


def parse_array(raw_value):
    """
    Parse an array input, supporting nested arrays or flat arrays.

    Args:
        raw_value: Raw input value (string or list).

    Returns:
        Parsed array.
    """
    logger.info('entering parse_array function')
    logger.info(raw_value)

    # Cas ou c'est un nombre
    if isinstance(raw_value, str):
        try:
            floating_str = float(raw_value)
            return floating_str
        except ValueError:
            pass

    # 🔹 Cas d'un texte normal (ex: "One-Sample", "Test Type")
    if isinstance(raw_value, str) and not any(char in raw_value for char in "[],"):
        logger.info("Recognized as a standard string, returning as is.")
        return raw_value  # Ex: "One-Sample"

    # 🔹 Vérification si c'est un JSON valide (ex: "[1,2,3]" ou "[[1,2],[3,4]]")
    try:
        parsed_json = json.loads(raw_value)  # Essayer de charger en JSON
        if isinstance(parsed_json, list):
            if all(isinstance(sublist, list) for sublist in parsed_json):  # Cas [[1,2],[3,4]]
                logger.info("Recognized as a JSON-style list of lists, converting to nested float lists.")
                return [[float(x) for x in sublist] for sublist in parsed_json]
            else:  # Cas [1,2,3]
                logger.info("Recognized as a JSON-style simple list, converting to float list.")
                return [float(x) for x in parsed_json]
    except json.JSONDecodeError:
        logger.info("Not a JSON list, checking further.")

    # 🔹 Cas où la valeur est une simple liste sous forme de string (ex: "1,2,3")
    if "," in raw_value:
        logger.info("Recognized as a CSV-style list, converting to float list.")
        return [float(x.strip()) for x in raw_value.split(",") if x.strip()]
    
    # Cas ou c'est juste une simple liste
    if isinstance(raw_value, list):
        logger.info("Processing list input")
        return raw_value
   
    return raw_value

def parse_inputs(data_source, inputs_config):
    """
    Parse and validate the inputs based on the provided configuration.

    Args:
        data_source: Request data (form or JSON).
        inputs_config: List of input configurations.

    Returns:
        A dictionary of parsed parameters.
    """
    params = {}
    for input_field in inputs_config:
        input_id = input_field["id"]
        input_type = input_field["type"]
        optional = input_field.get("optional", False)
        if input_id in data_source:
            raw_value = data_source[input_id]
            logger.info(f"Parsing input {input_id}: {raw_value}")
            if raw_value:
                if input_type == "file":
                    logger.info("Processing file input")
                    # Handle CSV file upload
                    file_data = request.files[input_id] if request.files else None
                    if file_data:
                        column_names, params[input_id] = parse_csv_and_xlsx(file_data)
                elif input_type == "array":
                    logger.info("Processing array input")
                    params[input_id] = parse_array(raw_value)
                    logger.info('processed array input')
                elif input_type == "number":
                    logger.info("Processing number input")
                    params[input_id] = float(raw_value)
                else:
                    params[input_id] = raw_value
            elif not optional:
                raise ValueError(f"Missing required input: {input_id}")
    return params

# Pour extraire les valeurs du result sans prendre en compte la display_value
def extract_values(results):
    """
    Extrait uniquement les valeurs numériques du dictionnaire, ou lit les valeurs depuis un fichier CSV si nécessaire.

    - Si `results` est un dictionnaire, retourne `{clé: valeur numérique}`.
    - Si `results` est un tuple contenant un fichier CSV, lit les données du CSV et retourne un dictionnaire.

    Retourne :
    - Un dictionnaire `{clé: valeurs}` où les clés sont les colonnes ou indices si pas de header.
    """
    logger.info("Extracting numerical values from the results")
    logger.warning(results)

    # Cas où results est un tuple contenant des chemins de fichiers
    if isinstance(results, tuple):
        csv_path = None
        
        # Trouver le fichier CSV dans le tuple
        for file in results:
            if file.endswith(".csv"):
                csv_path = file
                break
        
        if csv_path is None:
            raise ValueError("No CSV file found in results")

        logger.info(f"Loading data from CSV file: {csv_path}")

        # Lire le fichier CSV avec Pandas
        df = pd.read_csv(csv_path)

        # Vérifier si le CSV a un header (contient des noms de colonnes ou juste des valeurs)
        if df.columns.str.contains("Unnamed").all():
            logger.info("CSV file has no header, using column indices as keys")
            data_dict = {i: df.iloc[:, i].tolist() for i in range(df.shape[1])}
        else:
            logger.info("CSV file has headers, using column names as keys")
            data_dict = {col: df[col].tolist() for col in df.columns}
        logger.error(data_dict)
        return data_dict

    # Cas où results est un dictionnaire normal
    elif isinstance(results, dict):
        logger.error({key: value[1] for key, value in results.items()})
        return {key: value[1] for key, value in results.items()}
    
    else:
        raise TypeError("Unsupported format for results")




def get_data_source(request):
    """Détecte la source des données envoyées (JSON, form-data ou fichier)"""
    if request.content_type.startswith("multipart/form-data"):
        logger.info("📂 Requête multipart/form-data détectée")

        # Récupérer les fichiers
        files_data = request.files if request.files else {}

        # Récupérer les champs textes envoyés dans le form-data
        form_data = request.form.to_dict()  # Convertir en dict pour éviter ImmutableMultiDict

        # Vérifier si un JSON est encodé dans un champ texte
        json_data = {}
        if "json_data" in form_data:
            try:
                json_data = json.loads(form_data["json_data"])
            except json.JSONDecodeError:
                logger.error("Erreur de parsing du JSON dans form-data")

        return {"files": files_data, "json": json_data, "form": form_data}

    elif request.is_json:
        logger.info("Requête JSON détectée")
        return {"files": None, "json": request.json, "form": {}}

    else:
        logger.warning("Type de requête inconnu")
        return {"files": None, "json": {}, "form": {}}

def convert_numpy_types(obj):
    """Convertit les types NumPy en types standards pour éviter les erreurs JSON."""
    if isinstance(obj, np.integer):  # Vérifie si c'est un int NumPy (ex: int32, int64)
        return int(obj)  # Convertit en int standard
    elif isinstance(obj, np.floating):  # Vérifie si c'est un float NumPy
        return float(obj)  # Convertit en float standard
    elif isinstance(obj, dict):  # Vérifie si c'est un dictionnaire et convertit récursivement
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):  # Vérifie si c'est une liste et convertit récursivement
        return [convert_numpy_types(item) for item in obj]
    return obj  # Sinon, renvoie l'objet inchangé


def process_uploaded_files_with_target(data_source, tool_config):
    """
    Gère les fichiers uploadés et remplace leur ID par leur `data_target`.

    Args:
        data_source (dict): Données reçues contenant les fichiers.
        tool_config (list): Configuration des inputs, contenant `id` et `data_target`.

    Returns:
        dict: Un dictionnaire avec `data_target` comme clé et le contenu du fichier en valeur.
    """
    parsed_datasets = {}
    column_names = []

    # Vérifier si des fichiers sont présents
    if "files" in data_source and data_source["files"]:
        logger.warning("📂 Processing uploaded files...")

        for file_key, file_obj in data_source["files"].items():
            if isinstance(file_obj, FileStorage) and file_obj.filename:
                logger.info(f"📌 Détection du fichier : {file_obj.filename}")

                # Trouver `data_target` correspondant à l'ID du fichier
                target_name = next(
                (item["data_target"] for item in tool_config["inputs"] if item["id"] == file_key),
                file_key  # Valeur par défaut si non trouvé
            )
                # Parser le fichier CSV/XLSX
                try:
                    column_names, parsed_data = parse_csv_and_xlsx(file_obj)
                    logger.warning(f"✅ Fichier {file_obj.filename} chargé avec succès.")
                    parsed_datasets[target_name] = parsed_data
                    logger.warning(f"✅ Fichier {file_obj.filename} chargé sous `{target_name}` avec succès.")
                except Exception as e:
                    logger.error(f"❌ Erreur lors du traitement de {file_obj.filename} : {e}")
    logger.warning(f"✅ Parsed datasets: {parsed_datasets}")
    return column_names, parsed_datasets


def parse_input_data(request, tool_config):
    data_source = get_data_source(request)
    parsed_data = {}

    logger.warning("📥 Processing input data...")
    column_names = []
    
    # 🔹 1️⃣ Parsing des fichiers (prioritaires)
    if "files" in data_source and data_source["files"]:
        logger.warning("📂 Processing uploaded files...")
        column_names, parsed_files = process_uploaded_files_with_target(data_source, tool_config)
        logger.warning(f"✅ Parsed files: {parsed_files}")
        
        # Priorité aux fichiers : on écrase les valeurs existantes
        parsed_data.update(parsed_files)
        logger.error('parsed data 1')
        logger.error(parsed_data)

    # 🔹 2️⃣ Parsing du JSON
    if "json" in data_source and data_source["json"]:
        for key, value in data_source["json"].items():
            # Ajouter seulement si l'input n'a pas déjà été remplacé par un fichier
            if key not in parsed_data:
                parsed_data[key] = value
        logger.error('parsed data 2', parsed_data)

    # 🔹 3️⃣ Parsing du formulaire (`form`)
    if "form" in data_source and data_source["form"]:
        parsed_values = [parse_array(value) for value in data_source["form"].values()]
        parsed_form_data = {k: v for k, v in zip(data_source["form"].keys(), parsed_values)}

        for key, value in parsed_form_data.items():
            # Ajouter seulement si l'input n'a pas déjà été remplacé par un fichier
            if key not in parsed_data:
                parsed_data[key] = value

        logger.error('parsed data 3')
        logger.error(parsed_data)

    logger.info(f"✅ Parsed data: {parsed_data}")
    return column_names, parsed_data

def reassign_params_if_header(tool_config, params, column_names):
    """
    Réassigne les paramètres et les noms de colonnes si un fichier CSV a été fourni 
    et que son id dans tool_config contient "header": True.

    Args:
        tool_config (dict): Configuration de l'outil.
        params (dict): Données parsées des inputs de l'utilisateur.
        column_names (list): Liste des noms de colonnes issues du fichier CSV.

    Returns:
        tuple: (params mis à jour, column_names mis à jour)
    """
    for input_config in tool_config.get("inputs", []):
        data_target = input_config.get("data_target")
        
        if data_target and input_config.get("header") == True:
            # Vérifier si ce data_target est bien dans params
            if data_target in params and isinstance(params[data_target], list):
                data_values = params[data_target]  # Liste des listes
                
                if len(column_names) == 1:
                    # Si une seule colonne, on garde une liste plate
                    params[data_target] = data_values[0]  # On prend la première liste (colonne unique)
                else:
                    # Si plusieurs colonnes, transformer en dictionnaire {nom_colonne: liste de valeurs}
                    params[data_target] = {
                        col_name: data_values[i] for i, col_name in enumerate(column_names)
                    }

                break  # Une seule mise à jour suffit

    return params, column_names

