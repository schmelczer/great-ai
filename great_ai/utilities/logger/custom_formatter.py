import logging
from typing import Any

from .colors import BLUE, BOLD_RED, GREY, RED, RESET, YELLOW


class CustomFormatter(logging.Formatter):
    def __init__(self, fmt: str, *args: Any, **kwargs: Any):
        self._log_format = fmt
        self._date_format = "%Y-%m-%d %H:%M:%S"

        self._color_mapping = {
            logging.DEBUG: GREY + fmt + RESET,
            logging.INFO: BLUE + fmt + RESET,
            logging.WARNING: YELLOW + fmt + RESET,
            logging.ERROR: RED + fmt + RESET,
            logging.CRITICAL: BOLD_RED + fmt + RESET,
        }

    def format(self, record: logging.LogRecord) -> str:
        log_format = self._color_mapping.get(record.levelno)
        formatter = logging.Formatter(log_format, self._date_format)
        return formatter.format(record)
