import inspect
from typing import Any, Awaitable, Callable, Type, Union, cast

from fastapi import APIRouter, FastAPI, HTTPException, status
from pydantic import BaseModel, create_model

from ...helper import get_function_metadata_store
from ...views import Trace


def bootstrap_prediction_endpoint(
    app: FastAPI, func: Callable[..., Union[Trace, Awaitable[Trace]]]
) -> None:
    router = APIRouter(
        tags=["predictions"],
    )

    schema = _get_schema(func)

    @router.post("/predict", status_code=status.HTTP_200_OK, response_model=Trace)
    async def predict(input_value: schema) -> Trace:  # type: ignore
        try:
            if inspect.iscoroutinefunction(func):
                return await cast(Callable[..., Awaitable[Trace]], func)(
                    **cast(BaseModel, input_value).dict()
                )
            return cast(Callable[..., Trace], func)(
                **cast(BaseModel, input_value).dict()
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"The following exception has occurred: {type(e).__name__}: {e}",
            )

    app.include_router(router)


def _get_schema(func: Callable) -> Type[BaseModel]:
    signature = inspect.signature(func)
    parameters = {
        p.name: (
            p.annotation if p.annotation != inspect._empty else Any,
            p.default if p.default != inspect._empty else ...,
        )
        for p in signature.parameters.values()
        if p.name in get_function_metadata_store(func).input_parameter_names
    }

    schema: Type[BaseModel] = create_model("InputModel", **parameters)  # type: ignore
    return schema
