from datetime import datetime
from math import ceil
from random import shuffle
from typing import Any, Iterable, List, TypeVar, Union, cast
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
    tags: Union[List[str], str] = [],
    train_split_ratio: float = 1,
    test_split_ratio: float = 0,
    validation_split_ratio: float = 0,
) -> None:
    """Add training data (with optional train-test splitting).

    Add and tag data-points, wrap them into traces. The `inputs` are available via the
    `.input` property, while `expected_outputs` under both the `.output` and `.feedback`
    properties.

    All generated traces are tagged with `ground_truth` by default. Additional tags can
    be also provided. Using the `split_ratio` arguments, tags can be given randomly with
    a user-defined distribution. Only the ratio of the splits matter, they don't have to
    add up to 1.

    Examples:
        >>> add_ground_truth(
        ...    [1, 2, 3],
        ...    ['odd', 'even', 'odd'],
        ...    tags='my_tag',
        ...    train_split_ratio=1,
        ...    test_split_ratio=1,
        ...    validation_split_ratio=0.5,
        ... )

        >>> add_ground_truth(
        ...    [1, 2],
        ...    ['odd', 'even', 'odd'],
        ...    tags='my_tag',
        ...    train_split_ratio=1,
        ...    test_split_ratio=1,
        ...    validation_split_ratio=0.5,
        ... )
        Traceback (most recent call last):
            ...
        AssertionError: The length of the inputs and expected_outputs must be equal

    Args:
        inputs: The inputs. (X in scikit-learn)
        expected_outputs: The ground-truth values corresponding to the inputs. (y in
            scikit-learn)
        tags: A single tag or a list of tags to append to each generated trace's tags.
        train_split_ratio: The probability-weight of giving each trace the `train` tag.
        test_split_ratio: The probability-weight of giving each trace the `test` tag.
        validation_split_ratio: The probability-weight of giving each trace the
            `validation` tag.
    """

    inputs = list(inputs)
    expected_outputs = list(expected_outputs)
    assert len(inputs) == len(
        expected_outputs
    ), "The length of the inputs and expected_outputs must be equal"

    tags = tags if isinstance(tags, list) else [tags]

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
