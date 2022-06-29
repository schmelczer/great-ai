from typing import Optional

from pydantic import BaseModel

from ..logger import get_logger

logger = get_logger("parallel_map")


class ParallelMapConfiguration(BaseModel):
    concurrency: int
    chunk_count: Optional[int]
    chunk_length: int
    input_length: Optional[int]
    serialized_map_function: bytes

    def pretty_print(self, prefix="  ⚙️ "):
        logger.info(f"{prefix} concurrency: {self.concurrency}")
        logger.info(f"{prefix} chunk length: {self.chunk_length}")
        logger.info(
            f"{prefix} chunk count: {self.chunk_count if self.chunk_count else 'unknown'}"
        )
        logger.info(
            f"{prefix} function size: {len(self.serialized_map_function) / 1024:.0f} kB"
        )
