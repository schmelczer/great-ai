from typing import Any, Callable

import uvicorn
from fastapi import status
from typing_extensions import Never

from good_ai.good_ai.deploy.create_fastapi_app import create_fastapi_app

from ..set_default_config import set_default_config_if_uninitialized
from ..tracing import TracingContext
from ..views import Trace


def serve(
    function: Callable[..., Any],
) -> Never:
    set_default_config_if_uninitialized()

    app = create_fastapi_app(function.__name__)

    @app.post("/score", status_code=status.HTTP_200_OK, response_model=Trace)
    def process(input: Any) -> Trace:
        with TracingContext() as t:
            t.log_input(input)
            result = function(input)
            output = t.log_output(result)
        return output

    uvicorn.run(app, host="0.0.0.0", port=5050)
