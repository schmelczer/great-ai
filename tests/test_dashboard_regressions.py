from typing import Any

import pandas as pd
import pytest
from great_ai.deploy.routes.dashboard.create_dash_app import get_dimension_descriptor
from great_ai.deploy.routes.dashboard.get_filter_from_datatable import (
    get_filter_from_datatable,
)


@pytest.mark.parametrize(
    "expression, operator, value",
    [
        ('{value} contains "a=b"', "contains", "a=b"),
        ("{value} eq 7", "=", 7),
        ("{value} ge 2.5", ">=", 2.5),
        ('{value} contains ""', "contains", ""),
        (r"{value} contains 'it\'s > 2'", "contains", "it's > 2"),
    ],
)
def test_dashboard_filter_grammar(expression: str, operator: str, value: Any) -> None:
    result = get_filter_from_datatable(expression)
    assert result is not None
    assert result.property == "value"
    assert result.operator == operator
    assert result.value == value


@pytest.mark.parametrize(
    "expression", ["{value} > ", '{value} contains "unfinished', "invalid"]
)
def test_incomplete_filters_are_ignored(expression: str) -> None:
    assert get_filter_from_datatable(expression) is None


def test_long_category_labels_keep_distinct_coordinates() -> None:
    prefix = "a" * 40
    dimension = get_dimension_descriptor(
        pd.DataFrame({"category": [prefix + "1", prefix + "2"]}), "category"
    )
    assert dimension["values"] == [0, 1]
    assert dimension["tickvals"] == [0, 1]
    assert dimension["ticktext"] == [prefix, prefix]
