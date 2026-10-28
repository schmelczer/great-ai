from typing import Any

import numpy as np
from pydantic_core import PydanticSerializationError


def numpy_to_python(value: Any) -> Any:
    """Convert NumPy values encountered by Pydantic's JSON serializer."""
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.generic):
        converted = value.item()
        if not isinstance(converted, type(value)):
            return converted
    raise PydanticSerializationError(
        f"Unable to serialize {type(value).__name__}; convert it to a JSON-compatible "
        "Python value before returning or logging it."
    )
