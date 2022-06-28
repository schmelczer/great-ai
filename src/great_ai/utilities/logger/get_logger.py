import logging
from typing import Dict

from .custom_formatter import CustomFormatter

loggers: Dict[str, logging.Logger] = {}


def get_logger(
    name: str, level: int = logging.INFO, disable_colors: bool = False
) -> logging.Logger:
    if name not in loggers:
        logger = logging.getLogger(name)
        logger.setLevel(level)

        fmt = "%(asctime)s | %(levelname)8s | %(message)s"

        stdout_handler = logging.StreamHandler()
        stdout_handler.setLevel(level)
        if not disable_colors:
            stdout_handler.setFormatter(CustomFormatter(fmt))

        logger.addHandler(stdout_handler)
        loggers[name] = logger

    return loggers[name]
