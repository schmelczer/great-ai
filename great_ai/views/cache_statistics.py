from pydantic import BaseModel


class CacheStatistics(BaseModel):
    hits: int
    misses: int
    size: int
    max_size: int
