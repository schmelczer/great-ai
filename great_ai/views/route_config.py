from pydantic import BaseModel


class RouteConfig(BaseModel):
    prediction_endpoint_enabled: bool = True
    docs_endpoints_enabled: bool = True
    dashboard_enabled: bool = True
    feedback_endpoints_enabled: bool = True
    trace_endpoints_enabled: bool = True
    meta_endpoints_enabled: bool = True
