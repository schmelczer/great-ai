from typing import Any, Callable

import uvicorn
from fastapi import status
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import RedirectResponse
from typing_extensions import Never

from good_ai.good_ai.deploy.create_fastapi_app import create_fastapi_app

from ..context import get_context
from ..metrics import create_dash_app
from ..tracing import TracingContext
from ..views import Trace


def serve(
    function: Callable[..., Any],
    disable_docs: bool = False,
    disable_metrics: bool = False,
) -> Never:
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
            t.log_input(input)
            result = function(input)
            output = t.log_output(result)
        return output

    uvicorn.run(app, host="0.0.0.0", port=5050)
