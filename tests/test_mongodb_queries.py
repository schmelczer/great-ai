from datetime import datetime, timedelta, timezone
from typing import Any, Iterator, Tuple
from unittest.mock import MagicMock, patch

import pytest

from great_ai import MongoDbDriver


@pytest.fixture
def mongo() -> Iterator[Tuple[MongoDbDriver, Any]]:
    driver = MongoDbDriver.__new__(MongoDbDriver)
    driver.mongo_connection_string = "mongodb://test"
    driver.mongo_database = "test"
    with patch("great_ai.persistence.mongodb_driver.MongoClient") as factory:
        client = factory.__getitem__.return_value.return_value.__enter__.return_value
        collection = client.__getitem__.return_value.traces
        collection.count_documents.return_value = 3
        collection.find.return_value.__enter__.return_value = []
        yield driver, collection


def test_mongo_date_bounds_match_stored_iso_strings(
    mongo: Tuple[MongoDbDriver, Any],
) -> None:
    driver, collection = mongo
    since = datetime(2026, 1, 1, 1, tzinfo=timezone(timedelta(hours=1)))
    until = datetime(2026, 1, 2)
    driver.query(since=since, until=until)
    predicates = collection.find.call_args.kwargs["filter"]["$and"]
    assert {"created": {"$gte": "2026-01-01T00:00:00"}} in predicates
    assert {"created": {"$lte": "2026-01-02T00:00:00"}} in predicates


def test_zero_take_preserves_count_without_fetching(
    mongo: Tuple[MongoDbDriver, Any],
) -> None:
    driver, collection = mongo
    assert driver.query(take=0) == ([], 3)
    collection.find.assert_not_called()


def test_empty_batch_is_a_noop(mongo: Tuple[MongoDbDriver, Any]) -> None:
    driver, collection = mongo
    assert driver.save_batch([]) == []
    collection.insert_many.assert_not_called()
