import pytest
from fastapi.testclient import TestClient

from great_ai import GreatAI


def test_keyword_only_inputs_are_validated_and_exposed(isolated_context: None) -> None:
    @GreatAI.create
    def predict(*, value: int) -> int:
        return value

    trace = predict(value=7)
    assert trace.output == 7
    assert trace.logged_values["arg:value:value"] == 7
    with pytest.raises(TypeError):
        predict(value="wrong")
    with TestClient(predict.app) as client:
        assert client.post("/predict", json={"value": 8}).json()["output"] == 8
        assert client.post("/predict", json={"value": "wrong"}).status_code == 422
