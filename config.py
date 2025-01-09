# colored_logger.py
import logging
import os
import csv
from io import StringIO

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

def parse_csv(file):
    """
    Parse CSV file content into a list of numbers.
    Expects a single column or comma-separated values.
    """
    try:
        file_content = file.read().decode('utf-8')  # Decode file content
        reader = csv.reader(StringIO(file_content))
        values = []
        for row in reader:
            # Assume single-column or comma-separated values
            values.extend(float(x.strip()) for x in row if x.strip())
        return values
    except Exception as e:
        logger.error(f"Error parsing CSV: {e}")
        raise ValueError("Invalid CSV content")
    
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
                        params[input_id] = parse_csv(file_data)
                elif input_type == "array":
                    logger.info("Processing array input")
                    params[input_id] = parse_array(raw_value)
                elif input_type == "number":
                    logger.info("Processing number input")
                    params[input_id] = float(raw_value)
                else:
                    params[input_id] = raw_value
            elif not optional:
                raise ValueError(f"Missing required input: {input_id}")

    return params