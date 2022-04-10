import logging

from .colors import BLUE, BOLD_RED, GREY, RED, RESET, YELLOW


class CustomFormatter(logging.Formatter):
    def __init__(self, fmt: str):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: GREY + self.fmt + RESET,
            logging.INFO: BLUE + self.fmt + RESET,
            logging.WARNING: YELLOW + self.fmt + RESET,
            logging.ERROR: RED + self.fmt + RESET,
            logging.CRITICAL: BOLD_RED + self.fmt + RESET,
        }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
