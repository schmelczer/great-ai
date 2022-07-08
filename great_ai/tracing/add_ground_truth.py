from datetime import datetime
from math import ceil
from random import shuffle
from typing import Any, Iterable, List, TypeVar, cast
from uuid import uuid4

from ..constants import (
    GROUND_TRUTH_TAG_NAME,
    TEST_SPLIT_TAG_NAME,
    TRAIN_SPLIT_TAG_NAME,
    VALIDATION_SPLIT_TAG_NAME,
)
from ..context import get_context
from ..views import Trace

T = TypeVar("T")


def add_ground_truth(
    inputs: Iterable[Any],
    expected_outputs: Iterable[T],
    *,
    tags: List[str] = [],
    train_split_ratio: float = 1,
    test_split_ratio: float = 0,
    validation_split_ratio: float = 0
) -> None:
    get_context()  # this resets the seed

    inputs = list(inputs)
    expected_outputs = list(expected_outputs)
    assert len(inputs) == len(
        expected_outputs
    ), "The length of the inputs and expected_outputs must be equal"

    sum_ratio = train_split_ratio + test_split_ratio + validation_split_ratio
    assert sum_ratio > 0, "The sum of the split ratios must be a positive number"

    train_split_ratio /= sum_ratio
    test_split_ratio /= sum_ratio
    validation_split_ratio /= sum_ratio

    values = list(zip(inputs, expected_outputs))
    shuffle(values)

    split_tags = (
        [TRAIN_SPLIT_TAG_NAME] * ceil(train_split_ratio * len(inputs))
        + [TEST_SPLIT_TAG_NAME] * ceil(test_split_ratio * len(inputs))
        + [VALIDATION_SPLIT_TAG_NAME] * ceil(validation_split_ratio * len(inputs))
    )
    shuffle(split_tags)

    created = datetime.utcnow().isoformat()
    traces = [
        cast(
            Trace[T],
            Trace(  # avoid ValueError: "Trace" object has no field "__orig_class__"
                trace_id=str(uuid4()),
                created=created,
                original_execution_time_ms=0,
                logged_values=X if isinstance(X, dict) else {"input": X},
                models=[],
                output=y,
                feedback=y,
                exception=None,
                tags=[GROUND_TRUTH_TAG_NAME, split_tag, *tags],
            ),
        )
        for ((X, y), split_tag) in zip(values, split_tags)
    ]

    get_context().tracing_database.save_batch(traces)
