from typing import Literal, Union

from ..core import function_registry
from .use_model_plugin import UseModelPlugin


def use_model(
    key: str, version: Union[int, Literal["latest"]] = None, return_path: bool = False
):
    assert isinstance(version, int) or version == "latest"

    def inner(f):
        function_registry.add_plugin(
            f,
            UseModelPlugin(
                f,
                key=key,
                version=version if isinstance(version, int) else None,
                return_path=return_path,
            ),
        )
        return f

    return inner
