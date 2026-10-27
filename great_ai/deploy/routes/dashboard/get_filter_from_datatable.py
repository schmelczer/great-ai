import re
from typing import Optional, Union, cast

from ....views import Filter
from ....views.operators import Operator

_expression = re.compile(
    r"\s*\{([^}]+)\}\s*(>=|<=|!=|=|>|<|contains\b|ge\b|le\b|lt\b|gt\b|ne\b|eq\b)\s*(.*?)\s*",
    re.DOTALL,
)
_aliases = {"ge": ">=", "le": "<=", "lt": "<", "gt": ">", "ne": "!=", "eq": "="}


def get_filter_from_datatable(description: str) -> Optional[Filter]:
    match = _expression.fullmatch(description)
    if match is None:
        return None
    name, token, raw = match.groups()
    if not raw:
        return None
    if raw[0] in ("'", '"', "`"):
        if len(raw) < 2 or raw[-1] != raw[0]:
            return None
        value: Union[str, float] = re.sub(r"\\([\\'\"`])", r"\1", raw[1:-1])
    else:
        try:
            value = float(raw)
        except ValueError:
            value = raw
    return Filter(
        property=name, operator=cast(Operator, _aliases.get(token, token)), value=value
    )
