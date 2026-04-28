import logging
import os
import json
from datetime import datetime


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)


def get_logger(name="app"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate logs
    if logger.handlers:
        return logger

    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    formatter = JsonFormatter()

    # File handler
    file_handler = logging.FileHandler("logs/app.json")
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
    




