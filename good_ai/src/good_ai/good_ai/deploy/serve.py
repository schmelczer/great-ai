from typing import Any, Callable

import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import RedirectResponse

from good_ai.good_ai.deploy.create_fastapi_app import create_fastapi_app

from ..context import get_context
from ..metrics import create_dash_app
from ..tracing import TracingContext
from ..views import Trace


def serve(
    function: Callable[..., Any],
    disable_docs: bool = False,
    disable_metrics: bool = False,
    configure: Callable[[FastAPI], None] = lambda _: None,
) -> None:
    app = create_fastapi_app(function.__name__, disable_docs=disable_docs)

    if not disable_metrics:
        dash_app = create_dash_app(function.__name__)
        app.mount(get_context().metrics_path, WSGIMiddleware(dash_app))

        @app.get("/", include_in_schema=False)
        def redirect_to_entrypoint() -> RedirectResponse:
            return RedirectResponse("/metrics")

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
            "version": 1,
            "disable_existing_loggers": False,
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
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
                "access": {
                    "formatter": "access",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "uvicorn": {"handlers": ["default"], "level": "INFO"},
                "uvicorn.error": {"level": "INFO"},
                "uvicorn.access": {
                    "handlers": ["access"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        },
    )
