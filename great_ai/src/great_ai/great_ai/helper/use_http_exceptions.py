from functools import wraps
from typing import Any, Callable, Dict, List

from fastapi import HTTPException, status


def use_http_exceptions(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"The following exception has occurred: {type(e).__name__}: {e}",
            )

    return wrapper
