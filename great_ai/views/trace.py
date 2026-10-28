from pprint import pformat
from typing import Any, Dict, Generic, List, Literal, Optional, TypeVar, cast

from pydantic import (
    ConfigDict,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    TypeAdapter,
    field_serializer,
)
from pydantic_core import PydanticSerializationError

from ..helper.numpy_to_python import numpy_to_python
from .hashable_base_model import HashableBaseModel
from .model import Model

T = TypeVar("T")
_json_value = TypeAdapter(Any)


class Trace(HashableBaseModel, Generic[T]):
    """Universal structure for storing prediction traces and training data.

    Attributes:
        trace_id: UUID4 identifier for uniquely referring to a trace.
        created: Timestamp of its (original) construction.
        original_execution_time_ms: Wall-time elapsed while its generating
            TracingContext was alive.
        logged_values: Values persisted through using `@parameter` or `log_metric()`.
        models: Marks left by each encountered `@use_model` decorated function.
        exception: Exception description if any was encountered.
        output: Return value of the function wrapped by GreatAI.
        feedback: Feedback obtained using the REST API of `add_ground_truth`.
        tags: Tags used for filtering traces. Contains the name of the original
            function, value of `ENVIRONMENT`, its split if has any, and either
            `ground_truth` or `online` depending on the origin of the Trace.
    """

    trace_id: str
    created: str
    original_execution_time_ms: float
    logged_values: Dict[str, Any]
    models: List[Model]
    exception: Optional[str] = None
    output: Optional[T] = None
    feedback: Any = None
    tags: List[str]

    model_config = ConfigDict(extra="ignore")

    @field_serializer(
        "output", "logged_values", "feedback", mode="wrap", when_used="json"
    )
    def serialize_numpy_values(  # type: ignore[no-untyped-def]
        self,
        value: Any,
        handler: SerializerFunctionWrapHandler,
        info: SerializationInfo,
    ):
        # An explicit return annotation would replace the generic output's JSON
        # schema. Keep its declared type while providing a fallback for NumPy.
        try:
            return handler(value)
        except PydanticSerializationError:
            return _json_value.dump_python(
                value,
                mode="json",
                include=cast(Any, info.include),
                exclude=cast(Any, info.exclude),
                by_alias=info.by_alias,
                exclude_unset=info.exclude_unset,
                exclude_defaults=info.exclude_defaults,
                exclude_none=info.exclude_none,
                round_trip=info.round_trip,
                serialize_as_any=info.serialize_as_any,
                context=info.context,
                fallback=numpy_to_python,
            )

    @property
    def input(self) -> Any:
        """Original input value, or a name-to-value mapping for multiple arguments.

        Online traces omit metrics and derived argument metadata. Arguments marked
        ``disable_logging=True`` are omitted, so their values cannot be recovered.
        """
        if "online" in self.tags and "ground_truth" not in self.tags:
            arguments = {
                key[len("arg:") : -len(":value")]: value
                for key, value in self.logged_values.items()
                if key.startswith("arg:") and key.endswith(":value")
            }
            if len(arguments) == 1:
                return next(iter(arguments.values()))
            return arguments
        return (
            self.logged_values["input"]
            if list(self.logged_values.keys()) == ["input"]
            else self.logged_values
        )

    @property
    def models_flat(self) -> str:
        return ", ".join(f"{m.key}:{m.version}" for m in self.models)

    @property
    def output_flat(self) -> str:
        return pformat(self.output, indent=2, compact=True)

    @property
    def exception_flat(self) -> str:
        return (
            "null"
            if self.exception is None
            else pformat(self.exception, indent=2, compact=True)
        )

    @property
    def feedback_flat(self) -> str:
        return (
            "null"
            if self.feedback is None
            else pformat(self.feedback, indent=2, compact=True)
        )

    @property
    def tags_flat(self) -> str:
        return ",\n".join(self.tags)

    def to_flat_dict(
        self,
        include_original: bool = True,
        *,
        mode: Literal["python", "json"] = "python",
    ) -> Dict[str, Any]:
        serialized = self.model_dump(mode=mode)
        reserved = set(type(self).model_fields) | {"_id"}
        return {
            **(
                serialized
                if include_original
                else {
                    "trace_id": self.trace_id,
                    "created": self.created,
                    "original_execution_time_ms": self.original_execution_time_ms,
                }
            ),
            **{
                k: (
                    v
                    if (isinstance(v, float) or isinstance(v, int))
                    else pformat(v, indent=2, compact=True)
                )
                for k, v in serialized["logged_values"].items()
                if k not in reserved
            },
            "models_flat": self.models_flat,
            "exception_flat": self.exception_flat,
            "output_flat": self.output_flat,
            "feedback_flat": self.feedback_flat,
            "tags_flat": self.tags_flat,
        }

    def __repr__(self) -> str:
        formatted = pformat(self.model_dump(), indent=2, compact=True).replace(
            "{ ", "{", 1
        )
        return f"Trace[{type(self.output).__name__}]({formatted})"
