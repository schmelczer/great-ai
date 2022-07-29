from typing import List

from typing_extensions import Literal  # <= Python 3.7

Operator = Literal[">=", "<=", "<", ">", "!=", "=", "contains"]

operators: List[Operator] = [">=", "<=", "<", ">", "!=", "=", "contains"]
