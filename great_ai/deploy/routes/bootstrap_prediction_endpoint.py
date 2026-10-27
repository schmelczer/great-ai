import inspect
from typing import Any, Awaitable, Callable, Type, Union, cast

from fastapi import APIRouter, FastAPI, HTTPException, status
from pydantic import BaseModel, create_model

from ...helper import get_function_metadata_store
from ...helper.get_function_type_hints import get_function_type_hints
from ...views import Trace


def bootstrap_prediction_endpoint(
    app: FastAPI, func: Callable[..., Union[Trace, Awaitable[Trace]]]
) -> None:
    router = APIRouter(
        tags=["predictions"],
    )

    schema = _get_schema(func)
    positional_names = [
        p.name
        for p in inspect.signature(func).parameters.values()
        if p.kind == p.POSITIONAL_ONLY and p.name in schema.model_fields
    ]

    @router.post("/predict", status_code=status.HTTP_200_OK, response_model=Trace)
    async def predict(input_value: schema) -> Trace:  # type: ignore
        try:
            # model_dump() recursively converts nested models to dictionaries,
            # losing the validated argument types expected by the function.
            arguments = {
                name: getattr(input_value, name) for name in schema.model_fields
            }
            positional = [arguments.pop(name) for name in positional_names]
            if inspect.iscoroutinefunction(func):
                return await cast(Callable[..., Awaitable[Trace]], func)(
                    *positional, **arguments
                )
            return cast(Callable[..., Trace], func)(*positional, **arguments)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"The following exception has occurred: {type(e).__name__}: {e}",
            )

    app.include_router(router)


def _get_schema(func: Callable) -> Type[BaseModel]:
    signature = inspect.signature(func)
    type_hints = get_function_type_hints(func)
    parameters = {
        p.name: (
            type_hints.get(p.name, Any),
            p.default if p.default != inspect._empty else ...,
        )
        for p in signature.parameters.values()
        if p.name in get_function_metadata_store(func).input_parameter_names
    }

    schema: Type[BaseModel] = create_model("InputModel", **parameters)  # type: ignore
    return schema
