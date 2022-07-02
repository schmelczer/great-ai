from typing import Optional

from pydantic import BaseModel

from ..logger import get_logger

logger = get_logger("parallel_map")


class ParallelMapConfiguration(BaseModel):
    concurrency: int
    chunk_count: Optional[int]
    chunk_size: int
    input_length: Optional[int]
    serialized_map_function: bytes
    function_name: str
