import logging

from .colors import BLUE, BOLD_RED, GREY, RED, RESET, YELLOW


class CustomFormatter(logging.Formatter):
    def __init__(self, fmt: str):
        super().__init__()
        self._fmt = fmt
        self._color_mapping = {
            logging.DEBUG: GREY + self._fmt + RESET,
            logging.INFO: BLUE + self._fmt + RESET,
            logging.WARNING: YELLOW + self._fmt + RESET,
            logging.ERROR: RED + self._fmt + RESET,
            logging.CRITICAL: BOLD_RED + self._fmt + RESET,
        }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self._color_mapping.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
