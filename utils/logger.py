import os
import logging
import json
from datetime import datetime


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        # Include extra fields if present
        if hasattr(record, "extra_data"):
            log_record.update(record.extra_data)

        return json.dumps(log_record)


def get_logger(name="app"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    #  Prevent duplicate handlers
    if logger.handlers:
        return logger

    #  Create logs directory (CRITICAL FIX)
    os.makedirs("logs", exist_ok=True)

    formatter = JsonFormatter()

    # File handler
    file_handler = logging.FileHandler("logs/app.json")
    file_handler.setFormatter(formatter)

    # Console handler (for CI visibility)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger