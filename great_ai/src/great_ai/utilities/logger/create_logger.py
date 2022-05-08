import logging

from .custom_formatter import CustomFormatter


def create_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    fmt = "%(asctime)s | %(levelname)8s | %(message)s"

    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(CustomFormatter(fmt))

    logger.addHandler(stdout_handler)

    return logger
