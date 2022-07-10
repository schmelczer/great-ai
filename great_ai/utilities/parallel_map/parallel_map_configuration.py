from typing import Optional

from pydantic import BaseModel

from ..logger.get_logger import get_logger

logger = get_logger("parallel_map")


class ParallelMapConfiguration(BaseModel):
    concurrency: int
    chunk_count: Optional[int]
    chunk_size: int
    input_length: Optional[int]
    function_name: str
