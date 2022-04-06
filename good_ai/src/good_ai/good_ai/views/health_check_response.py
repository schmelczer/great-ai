from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    is_healthy: bool
