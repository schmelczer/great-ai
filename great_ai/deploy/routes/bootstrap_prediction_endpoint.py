import inspect
from types import UnionType
from typing import (
    Annotated,
    Any,
    Awaitable,
    Callable,
    Type,
    Union,
    cast,
    get_args,
    get_origin,
)

import numpy as np
from fastapi import APIRouter, FastAPI, HTTPException, status
from numpy.typing import NDArray
from pydantic import (
    AfterValidator,
    BaseModel,
    PlainSerializer,
    PlainValidator,
    WithJsonSchema,
    create_model,
)

from ...errors import ArgumentValidationError
from ...helper import get_function_metadata_store
from ...helper.get_function_type_hints import get_function_type_hints
from ...helper.numpy_to_python import numpy_to_python
from ...views import Trace


def bootstrap_prediction_endpoint(
    app: FastAPI, func: Callable[..., Union[Trace, Awaitable[Trace]]]
) -> None:
    router = APIRouter(
        tags=["predictions"],
    )

    schema = _get_schema(func)
    return_type = _get_api_type(get_function_type_hints(func).get("return", Any))
    response_model = Trace[return_type]  # type: ignore[valid-type]
    positional_names = [
        p.name
        for p in inspect.signature(func).parameters.values()
        if p.kind == p.POSITIONAL_ONLY and p.name in schema.model_fields
    ]

    @router.post(
        "/predict", status_code=status.HTTP_200_OK, response_model=response_model
    )
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
        except ArgumentValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=str(e),
            ) from e
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
            _get_api_type(type_hints.get(p.name, Any)),
            p.default if p.default != inspect._empty else ...,
        )
        for p in signature.parameters.values()
        if p.name in get_function_metadata_store(func).input_parameter_names
    }

    schema: Type[BaseModel] = create_model("InputModel", **parameters)  # type: ignore
    return schema


def _validate_numpy_array(value: Any) -> np.ndarray:
    if not isinstance(value, (list, np.ndarray)):
        raise ValueError("Expected an array (a JSON list or NumPy ndarray)")
    return np.asarray(value)


_NumpyArray = Annotated[
    np.ndarray,
    PlainValidator(_validate_numpy_array),
    PlainSerializer(lambda value: value.tolist(), when_used="json"),
    WithJsonSchema({"type": "array", "items": {}}),
]


def _get_api_type(annotation: Any) -> Any:
    """Represent NumPy arrays as JSON arrays without losing other annotations."""
    origin = get_origin(annotation)
    if annotation in (np.ndarray, NDArray) or origin in (np.ndarray, NDArray):
        return _NumpyArray
    if isinstance(annotation, type) and issubclass(annotation, np.generic):
        scalar_types = (
            (np.bool_, bool),
            (np.integer, int),
            (np.floating, float),
            (np.complexfloating, complex),
            (np.str_, str),
            (np.bytes_, bytes),
        )
        for numpy_type, python_type in scalar_types:
            if issubclass(annotation, numpy_type):
                return Annotated[
                    python_type,
                    AfterValidator(annotation),
                    PlainSerializer(
                        numpy_to_python, return_type=python_type, when_used="json"
                    ),
                ]
    arguments = get_args(annotation)
    if origin is Annotated:
        return Annotated[_get_api_type(arguments[0]), *arguments[1:]]
    converted = tuple(_get_api_type(argument) for argument in arguments)
    if all(old is new for old, new in zip(arguments, converted)):
        return annotation
    if origin in (Union, UnionType):
        return Union[converted]
    if hasattr(annotation, "copy_with"):
        return annotation.copy_with(converted)
    return origin[converted]
