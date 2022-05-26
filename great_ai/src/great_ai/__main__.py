#!/usr/bin/env python3

import re
from importlib import import_module

import uvicorn
from uvicorn.config import LOGGING_CONFIG

from .great_ai.context import get_context
from .great_ai.exceptions import MissingArgumentError
from .parse_arguments import parse_arguments
from .utilities.logger import create_logger

logger = create_logger("GreatAI-Server")


def main() -> None:
    args = parse_arguments()

    file_name = re.sub(r"\.py$", "", args.file_name)
    function_name = args.function_name

    module = import_module(file_name)

    if not function_name:
        logger.warning(f"Argument function_name not provided, trying to guess it")

        if not function_name and "app" in module.__dict__:
            function_name = "app"

        if not function_name and file_name in module.__dict__:
            function_name = file_name

        if function_name:
            logger.warning(f"Found `{function_name}` as the value of function_name")
        else:
            raise MissingArgumentError("Argument function_name could not be guessed")

    app_name = f"{file_name}:{function_name}"
    logger.info(f"Starting uvicorn server with app={app_name}")

    uvicorn.run(
        app_name,
        host=args.host,
        port=args.port,
        timeout_keep_alive=args.timeout_keep_alive,
        workers=args.workers,
        reload=not get_context().is_production,
        log_config={
            **LOGGING_CONFIG,
            "formatters": {
                "default": {
                    "()": "great_ai.logger.CustomFormatter",
                    "fmt": "%(asctime)s | %(levelname)8s | %(message)s",
                },
                "access": {
                    "()": "great_ai.logger.CustomFormatter",
                    "fmt": "%(asctime)s | %(levelname)8s | %(message)s",  # noqa: E501
                },
            },
        },
    )


if __name__ == "__main__":
    try:
        main()
    except (MissingArgumentError, ModuleNotFoundError) as e:
        logger.error(e)
    except KeyboardInterrupt:
        exit()
