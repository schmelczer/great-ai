from typing import List

from pydantic import BaseModel


class FunctionMetadata(BaseModel):
    input_parameter_names: List[str] = []
    model_parameter_names: List[str] = []
    is_finalised: bool = False
