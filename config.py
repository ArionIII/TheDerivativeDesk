# colored_logger.py
import logging

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
