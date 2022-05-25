#!/usr/bin/env python3
import re
from importlib import import_module
from sys import argv
import uvicorn
from uvicorn.config import LOGGING_CONFIG

from .great_ai.exceptions import MissingArgumentError
from .great_ai.context import get_context



def main():
    if len(argv) < 2:
        raise MissingArgumentError(f"Provide a filename such as: {argv[0]} my_app.py")

    module_name = re.sub(r"\.py\b", "", argv[1])
    
    base = module_name.split(":")[0]

    import_module(base)
    get_context().logger.info("Starting server")

    if ":" not in module_name:
        module_name += ":app"
        get_context().logger.warning(
            'Service name (name of variable) is assumed to be "app",'
            + ' such as: `app = create_service(predict_domain)`'
        )

    uvicorn.run(
        module_name,
        host="0.0.0.0",
        port=6060,
        timeout_keep_alive=600,
        workers=1,
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
        get_context().logger.error(e)
    except KeyboardInterrupt:
        exit()
