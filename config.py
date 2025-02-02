# colored_logger.py
import logging
import os
import csv
from io import StringIO
from flask import Blueprint, render_template, request, jsonify
import pandas as pd

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

        if file_extension == ".csv":
            # Lire le contenu du fichier CSV
            file_content = file.read().decode('utf-8')

            # Détecter automatiquement le séparateur
            first_line = file_content.split("\n")[0]
            separator = "," if "," in first_line else ";" if ";" in first_line else "\t"
            logger.info(f"Detected separator: {separator}")

            # Charger le fichier avec pandas
            df = pd.read_csv(StringIO(file_content), sep=separator, header=None)

        elif file_extension in [".xls", ".xlsx"]:
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

        # Remplacer les virgules par des points pour conversion correcte
        df = df.applymap(lambda x: x.replace(",", ".") if isinstance(x, str) else x)
        df = df.astype(float)

        # Si une seule colonne, retourner une liste de nombres
        if df.shape[1] == 1:
            return df.iloc[:, 0].dropna().tolist()

        # Si plusieurs colonnes, retourner un dictionnaire {nom_colonne: liste de valeurs}
        return {col: df[col].dropna().tolist() for col in df.columns}

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
    if isinstance(raw_value, list):
        return raw_value
    if "[" in raw_value and "]" in raw_value:
        # Parse nested lists
        try:
            return [
                [float(x.strip()) for x in inner_list.strip("[]").split(",") if x.strip()]
                for inner_list in raw_value.strip("[]").split("],[")
            ]
        except ValueError as e:
            logger.error(f"Error parsing nested array: {raw_value}, Error: {e}")
            raise ValueError(f"Invalid format for nested array input: {raw_value}")
    else:
        # Parse flat lists
        return [float(x.strip()) for x in raw_value.strip("[]").split(",") if x.strip()]


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
                        params[input_id] = parse_csv_and_xlsx(file_data)
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
    Extrait uniquement les valeurs numériques du dictionnaire sans la display_value.
    """
    return {key: value[1] for key, value in results.items()}
