from datetime import datetime
from typing import Any, Dict, List
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from great_ai import GreatAI, Trace
from great_ai.helper.freeze_arguments import freeze
from great_ai.persistence.mongodb_driver import MongoDbDriver
from pydantic import BaseModel, Field, field_validator
from pymongo import MongoClient
from pymongo.synchronous.collection import Collection


class Item(BaseModel):
    value: int = Field(alias="number")

    @field_validator("value")
    @classmethod
    def increment(cls, value: int) -> int:
        return value + 1


class Payload(BaseModel):
    item: Item
    others: List[Item]


def test_freezing_preserves_validated_models() -> None:
    original = Payload(item=Item(number=1), others=[Item(number=2)])
    frozen = freeze(original)
    assert isinstance(frozen, Payload)
    assert isinstance(frozen.item, Item)
    assert frozen.item.value == 2
    assert frozen.others[0].value == 3
    assert frozen.model_dump() == original.model_dump()
    assert hash(frozen) == hash(freeze(original))
    assert type(original) is Payload


@pytest.mark.parametrize("is_async", [False, True])
def test_http_preserves_nested_models(isolated_context: None, is_async: bool) -> None:
    def predict(data: Payload) -> int:
        assert isinstance(data.item, Item)
        assert all(isinstance(item, Item) for item in data.others)
        return data.item.value + sum(item.value for item in data.others)

    async def predict_async(data: Payload) -> int:
        return predict(data)

    service = GreatAI.create(predict_async if is_async else predict)
    with TestClient(service.app) as client:
        response = client.post(
            "/predict",
            json={"data": {"item": {"number": 1}, "others": [{"number": 2}]}},
        )
        assert response.status_code == 200
        assert response.json()["output"] == 5


@pytest.mark.asyncio
async def test_batch_after_async_prediction(isolated_context: None) -> None:
    @GreatAI.create
    async def predict(value: int) -> int:
        return value + 1

    assert (await predict(1)).output == 2
    assert [trace.output for trace in predict.process_batch([1, 2], concurrency=1)] == [
        2,
        3,
    ]
    assert (await predict(1)).output == 2


def test_flattening_preserves_reserved_trace_fields() -> None:
    trace = Trace(
        trace_id="actual-id",
        created=datetime(2026, 1, 1).isoformat(),
        original_execution_time_ms=0,
        models=[],
        tags=["online"],
        output="prediction",
        logged_values={
            "trace_id": "input-id",
            "created": "input-created",
            "output": 123,
            "tags": ["input"],
            "models": "input",
            "_id": "input-id",
            "feature": 5,
        },
    )
    flat = trace.to_flat_dict()
    for name, value in trace.model_dump().items():
        assert flat[name] == value
    assert "_id" not in flat
    assert flat["feature"] == 5
    assert Trace.model_validate(flat) == trace


def test_mongo_update_uses_valid_replacement() -> None:
    trace: Trace = Trace(
        trace_id="id",
        created="2026-01-01",
        original_execution_time_ms=0,
        logged_values={},
        models=[],
        tags=[],
        feedback="correct",
    )
    driver = MongoDbDriver.__new__(MongoDbDriver)
    driver.mongo_connection_string = "mongodb://127.0.0.1:1"
    driver.mongo_database = "test"
    client: MongoClient[Dict[str, Any]] = MongoClient(
        driver.mongo_connection_string, connect=False
    )
    with (
        patch("great_ai.persistence.mongodb_driver.MongoClient") as factory,
        patch.object(
            Collection, "_update_retryable", return_value={"n": 1, "nModified": 1}
        ) as update,
    ):
        factory.__getitem__.return_value.return_value = client
        driver.update("id", trace)
    assert update.call_args.args[0] == {"_id": "id"}
    document = update.call_args.args[1]
    assert document["_id"] == "id"
    assert Trace.model_validate(document) == trace
