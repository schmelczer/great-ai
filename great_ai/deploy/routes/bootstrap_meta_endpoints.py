from typing import Any

from fastapi import APIRouter, FastAPI, status

from ...views import ApiMetadata, CacheStatistics, HealthCheckResponse


def bootstrap_meta_endpoints(app: FastAPI, func: Any, metadata: ApiMetadata) -> None:
    router = APIRouter(
        tags=["meta"],
    )

    @router.get("/health", status_code=status.HTTP_200_OK)
    def check_health() -> HealthCheckResponse:
        hits, misses, maxsize, cache_size = func.cache_info()
        cache_statistics = CacheStatistics(
            hits=hits, misses=misses, size=cache_size, max_size=maxsize
        )

        return HealthCheckResponse(is_healthy=True, cache_statistics=cache_statistics)

    @router.get("/version", response_model=ApiMetadata, status_code=status.HTTP_200_OK)
    def get_version() -> ApiMetadata:
        return metadata

    app.include_router(router)
