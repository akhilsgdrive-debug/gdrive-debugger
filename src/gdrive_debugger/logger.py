"""Structured logging for gdrive-debugger."""

import json
import logging
from datetime import datetime
from pathlib import Path

from rich.logging import RichHandler

LOG_DIR = Path.home() / ".config" / "gdrive-debugger" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "gdrive-debugger.log"


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


def get_logger(name: str = "gdrive-debugger") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # JSON file handler (structured logs)
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)

    # Pretty Rich console handler
    console_handler = RichHandler(rich_tracebacks=True, show_time=False)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    return logger


def log_api_call(logger, method: str, **kwargs):
    """Log Google Drive API calls."""
    logger.info(f"API Call: {method}", extra={"extra": kwargs})