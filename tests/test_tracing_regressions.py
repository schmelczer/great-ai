import pytest
from great_ai import GreatAI, log_metric
from great_ai.tracing import TracingContext


@pytest.mark.parametrize("fail", [False, True])
def test_nested_predictions_restore_outer_trace(
    isolated_context: None, fail: bool
) -> None:
    @GreatAI.create
    def inner(value: int) -> int:
        if fail:
            raise ValueError("inner failed")
        return value

    @GreatAI.create
    def outer(value: int) -> int:
        try:
            inner(value)
        except ValueError:
            pass
        log_metric("after_inner", 7, disable_logging=True)
        return value

    trace = outer(1)
    assert trace.logged_values["metric:outer:after_inner"] == 7
    assert TracingContext.get_current_tracing_context() is None
