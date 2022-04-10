from typing import Any, Callable

import uvicorn
from fastapi import FastAPI, status
from uvicorn.config import LOGGING_CONFIG

from ..tracing import TracingContext
from ..views import Trace
from .create_fastapi_app import create_fastapi_app


def serve(
    function: Callable[..., Any],
    disable_docs: bool = False,
    disable_metrics: bool = False,
    configure: Callable[[FastAPI], None] = lambda _: None,
) -> None:
    app = create_fastapi_app(
        function.__name__, disable_docs=disable_docs, disable_metrics=disable_metrics
    )

    @app.post("/score", status_code=status.HTTP_200_OK, response_model=Trace)
    def process(input: Any) -> Trace:
        with TracingContext() as t:
            result = function(input)
            output = t.log_output(result)
        return output

    configure(app)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5050,
        log_config={
            **LOGGING_CONFIG,
            "formatters": {
                "default": {
                    "()": "good_ai.logger.CustomFormatter",
                    "fmt": "%(asctime)s | %(levelname)8s | %(message)s",
                },
                "access": {
                    "()": "good_ai.logger.CustomFormatter",
                    "fmt": "%(asctime)s | %(levelname)8s | %(message)s",  # noqa: E501
                },
            },
        },
    )
