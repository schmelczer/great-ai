from functools import wraps
from typing import Any, Callable, Dict, List, TypeVar, cast

from fastapi import HTTPException, status

F = TypeVar("F", bound=Callable[..., Any])


def use_http_exceptions(func: F) -> F:
    @wraps(func)
    def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"The following exception has occurred: {type(e).__name__}: {e}",
            )

    return cast(F, wrapper)
