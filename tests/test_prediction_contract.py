from typing import List

import pytest
from fastapi.testclient import TestClient
from great_ai import GreatAI, parameter
from pydantic import BaseModel


class Score(BaseModel):
    label: str
    confidence: float


@pytest.mark.parametrize("is_async", [False, True])
def test_custom_validation_returns_client_error_but_prediction_failures_do_not(
    isolated_context: None, is_async: bool
) -> None:
    @parameter("value", validate=lambda value: value > 0)
    def predict(value: int) -> int:
        if value == 7:
            raise ValueError("prediction failed")
        return value

    @parameter("value", validate=lambda value: value > 0)
    async def predict_async(value: int) -> int:
        return predict(value)

    service = GreatAI.create(predict_async if is_async else predict)
    with TestClient(service.app) as client:
        rejected = client.post("/predict", json={"value": -1})
        assert rejected.status_code == 422
        assert "did not pass validation" in rejected.json()["detail"]
        assert client.post("/predict", json={"value": "wrong"}).status_code == 422
        assert client.post("/predict", json={"value": 7}).status_code == 500
        valid = client.post("/predict", json={"value": 1})
        assert valid.status_code == 200
        assert valid.json()["output"] == 1


@pytest.mark.parametrize("is_async", [False, True])
def test_openapi_preserves_typed_nested_prediction_outputs(
    isolated_context: None, is_async: bool
) -> None:
    def predict(text: str) -> List[Score]:
        return [Score(label=text, confidence=0.75)]

    async def predict_async(text: str) -> List[Score]:
        return predict(text)

    service = GreatAI.create(predict_async if is_async else predict)
    with TestClient(service.app) as client:
        schema = client.get("/openapi.json").json()
        response_ref = schema["paths"]["/predict"]["post"]["responses"]["200"][
            "content"
        ]["application/json"]["schema"]["$ref"].split("/")[-1]
        output = schema["components"]["schemas"][response_ref]["properties"]["output"][
            "anyOf"
        ][0]
        assert output == {
            "items": {"$ref": "#/components/schemas/Score"},
            "type": "array",
        }
        assert (
            schema["components"]["schemas"]["Score"]["properties"]["confidence"]["type"]
            == "number"
        )
        response = client.post("/predict", json={"text": "cat"})
        assert response.status_code == 200
        assert response.json()["output"] == [{"label": "cat", "confidence": 0.75}]


def test_http_rejects_outputs_that_violate_the_return_annotation(
    isolated_context: None,
) -> None:
    @GreatAI.create
    def predict(value: int) -> int:
        return "invalid"  # type: ignore[return-value]

    with TestClient(predict.app, raise_server_exceptions=False) as client:
        assert client.post("/predict", json={"value": 1}).status_code == 500
