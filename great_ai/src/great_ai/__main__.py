#!/usr/bin/env python3
import re
from importlib import import_module
from sys import argv

import uvicorn
from uvicorn.config import LOGGING_CONFIG

from great_ai.great_ai.context import get_context

if __name__ == "__main__":
    if len(argv) < 2:
        raise ValueError(f"Provide a filename such as: {argv[0]} my_app.py")

    module_name = re.sub(r"\.py\b", "", argv[1])
    if ":" not in module_name:
        module_name += ":app"

    base = module_name.split(":")[0]
    module = import_module(base)
    get_context().logger.info("Starting server")

    uvicorn.run(
        module_name,
        host="0.0.0.0",
        port=6060,
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
