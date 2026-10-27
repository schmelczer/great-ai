import sys
from types import ModuleType

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


def test_positional_only_inputs_keep_their_bindings(isolated_context: None) -> None:
    @GreatAI.create
    def predict(first: str, /, second: int = 7) -> str:
        return first * second

    trace = predict("a", 2)
    assert trace.output == "aa"
    assert trace.logged_values["arg:first:value"] == "a"
    assert trace.logged_values["arg:second:value"] == 2
    with TestClient(predict.app) as client:
        response = client.post("/predict", json={"first": "b", "second": 3})
        assert response.status_code == 200
        assert response.json()["output"] == "bbb"


def test_postponed_model_annotations_resolve_in_their_module(
    isolated_context: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = ModuleType("great_ai_test_annotations")
    monkeypatch.setitem(sys.modules, module.__name__, module)
    exec(
        "from __future__ import annotations\n"
        "from pydantic import BaseModel\n"
        "class Payload(BaseModel):\n    value: int\n"
        "def predict(data: Payload) -> int:\n    return data.value\n",
        module.__dict__,
    )
    service = GreatAI.create(module.predict)
    with pytest.raises(TypeError):
        service("wrong")
    with TestClient(service.app) as client:
        response = client.post("/predict", json={"data": {"value": 7}})
        assert response.status_code == 200
        assert response.json()["output"] == 7
        assert client.get("/openapi.json").status_code == 200
