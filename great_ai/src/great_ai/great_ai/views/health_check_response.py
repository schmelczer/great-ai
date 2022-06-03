from pydantic import BaseModel

from .cache_statistics import CacheStatistics


class HealthCheckResponse(BaseModel):
    is_healthy: bool
    cache_statistics: CacheStatistics
