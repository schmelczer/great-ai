from typing import Dict, Tuple

from great_ai import GreatAI


def test_nested_tuple_inputs_can_be_cached(isolated_context: None) -> None:
    calls = 0

    @GreatAI.create
    def predict(value: Tuple[Dict[str, int]]) -> int:
        nonlocal calls
        calls += 1
        return value[0]["x"]

    assert predict(({"x": 7},)).output == 7
    assert predict(({"x": 7},)).output == 7
    assert calls == 1
