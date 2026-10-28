from typing import Any, Dict, Optional
from unittest.mock import patch

import numpy as np
import pytest
from fastapi.testclient import TestClient
from great_ai import GreatAI, log_metric
from great_ai.context import get_context
from great_ai.persistence.mongodb_driver import MongoDbDriver
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict, Field


class ArraySubclass(np.ndarray):
    pass


@pytest.mark.asyncio
@pytest.mark.parametrize("is_async", [False, True])
@pytest.mark.parametrize("cache_size", [0, 8])
async def test_numpy_arrays_work_with_and_without_caching(
    isolated_context: None, is_async: bool, cache_size: int
) -> None:
    get_context().prediction_cache_size = cache_size
    calls = 0

    def predict(values: np.ndarray) -> np.ndarray:
        nonlocal calls
        calls += 1
        log_metric("mean", np.float32(values.mean()))
        return values * 2

    async def predict_async(values: np.ndarray) -> np.ndarray:
        return predict(values)

    service: Any = GreatAI.create(predict_async if is_async else predict)
    original = np.array([1, 2], dtype=np.int64)
    first = service(original)
    if is_async:
        first = await first
    original[0] = 9
    first.output[0] = 99
    second = service(np.array([1, 2], dtype=np.int64))
    if is_async:
        second = await second
    np.testing.assert_array_equal(second.output, [2, 4])
    assert second.output.dtype == np.int64
    assert calls == (1 if cache_size else 2)
    stored = get_context().tracing_database.get(second.trace_id)
    assert stored is not None
    assert stored.output == [2, 4]
    assert stored.input == [1, 2]
    assert stored.logged_values["metric:predict:mean"] == 1.5


def test_numpy_cache_keys_preserve_shape_dtype_and_object_values(
    isolated_context: None,
) -> None:
    calls = 0

    @GreatAI.create
    def predict(values: np.ndarray) -> str:
        nonlocal calls
        calls += 1
        return str(values.shape) + str(values.dtype)

    for values in (
        np.array([1, 2], dtype=np.int32),
        np.array([1, 2], dtype=np.int64),
        np.array([1, 2], dtype=np.int64).view(ArraySubclass),
        np.array([[1, 2]], dtype=np.int64),
        np.array([{"x": [1]}], dtype=object),
    ):
        first = predict(values)
        assert predict(values.copy()).trace_id == first.trace_id
    assert calls == 5


def test_http_numpy_arrays_have_schemas_and_round_trip_through_storage(
    isolated_context: None,
) -> None:
    @GreatAI.create
    def predict(values: Optional[NDArray[np.float64]]) -> list[np.ndarray]:
        assert isinstance(values, np.ndarray)
        log_metric(
            "nested",
            {"maximum": np.int64(values.max()), "flags": np.array([True, False])},
        )
        return [values * 2]

    with TestClient(predict.app) as client:
        response = client.post("/predict", json={"values": [1, 2]})
        assert response.status_code == 200
        trace = response.json()
        assert trace["output"] == [[2, 4]]
        assert trace["logged_values"]["metric:predict:nested"] == {
            "maximum": 2,
            "flags": [True, False],
        }
        trace_url = f"/traces/{trace['trace_id']}"
        assert client.get(trace_url).json() == trace
        assert client.post("/traces", json={}).json() == [trace]
        assert client.post("/predict", json={"values": "wrong"}).status_code == 422
        schema = client.get("/openapi.json").json()
        assert (
            schema["components"]["schemas"]["InputModel"]["properties"]["values"][
                "anyOf"
            ][0]["type"]
            == "array"
        )
        response_ref = schema["paths"]["/predict"]["post"]["responses"]["200"][
            "content"
        ]["application/json"]["schema"]["$ref"].split("/")[-1]
        output = schema["components"]["schemas"][response_ref]["properties"]["output"][
            "anyOf"
        ][0]
        assert output["type"] == output["items"]["type"] == "array"


def test_numpy_scalar_annotations_are_preserved_in_python_and_openapi(
    isolated_context: None,
) -> None:
    @GreatAI.create
    def predict(value: np.int64) -> np.float32:
        assert isinstance(value, np.int64)
        return np.float32(value / 2)

    assert isinstance(predict(np.int64(3)).output, np.float32)
    with TestClient(predict.app) as client:
        response = client.post("/predict", json={"value": 3})
        assert response.status_code == 200
        assert response.json()["output"] == 1.5
        schema = client.get("/openapi.json").json()
        assert (
            schema["components"]["schemas"]["InputModel"]["properties"]["value"]["type"]
            == "integer"
        )
        response_ref = schema["paths"]["/predict"]["post"]["responses"]["200"][
            "content"
        ]["application/json"]["schema"]["$ref"].split("/")[-1]
        assert (
            schema["components"]["schemas"][response_ref]["properties"]["output"][
                "anyOf"
            ][0]["type"]
            == "number"
        )


def test_mongodb_serializes_numpy_values_for_insert_batch_and_update(
    isolated_context: None,
) -> None:
    @GreatAI.create
    def predict(values: np.ndarray) -> Dict[str, Any]:
        return {"values": values, "count": np.int64(values.size)}

    trace = predict(np.array([1, 2]))
    driver = MongoDbDriver.__new__(MongoDbDriver)
    driver.mongo_connection_string = "mongodb://127.0.0.1:1"
    driver.mongo_database = "test"
    with patch("great_ai.persistence.mongodb_driver.MongoClient") as factory:
        collection = (
            factory.__getitem__.return_value.return_value.__enter__.return_value[
                "test"
            ].traces
        )
        driver.save(trace)
        driver.save_batch([trace])
        driver.update(trace.trace_id, trace)
    inserted = collection.insert_one.call_args.args[0]
    assert inserted["output"] == {"values": [1, 2], "count": 2}
    assert inserted["logged_values"]["arg:values:value"] == [1, 2]
    assert collection.insert_many.call_args.args[0] == [inserted]
    assert collection.replace_one.call_args.args[1] == inserted


def test_numpy_serialization_preserves_exclusions_and_model_aliases(
    isolated_context: None,
) -> None:
    class Result(BaseModel):
        values: Any = Field(alias="array")
        secret: str = "private"
        model_config = ConfigDict(populate_by_name=True)

    @GreatAI.create
    def predict(value: int) -> Result:
        return Result(array=np.array([value]), secret="private")

    trace = predict(1)
    dumped = trace.model_dump(mode="json", exclude={"output": {"secret"}})
    assert dumped["output"] == {"values": [1]}
    aliased = trace.model_dump(
        mode="json", by_alias=True, exclude={"output": {"secret"}}
    )
    assert aliased["output"] == {"array": [1]}
