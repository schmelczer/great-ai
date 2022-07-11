import logging
from typing import Dict

from .custom_formatter import CustomFormatter

loggers: Dict[str, logging.Logger] = {}


def get_logger(
    name: str, level: int = logging.INFO, disable_colors: bool = False
) -> logging.Logger:
    """Return a customised logger used throughout the GreatAI codebase.

    Uses colors, and only prints timestamps when not running inside notebook.
    """

    if name not in loggers:
        logger = logging.getLogger(name)
        logger.setLevel(level)

        try:
            get_ipython()  # type: ignore
            log_format = "%(message)s"
        except NameError:
            # will fail outside of a notebook https://ipython.org/
            log_format = "%(asctime)s | %(levelname)8s | %(message)s"

        stdout_handler = logging.StreamHandler()
        stdout_handler.setLevel(level)
        if not disable_colors:
            stdout_handler.setFormatter(CustomFormatter(log_format))

        logger.addHandler(stdout_handler)
        loggers[name] = logger

    return loggers[name]
