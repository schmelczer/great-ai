from great_ai import ClassificationOutput, MultiLabelClassificationOutput, Trace


def test_output_models_hash_nested_mutable_fields_by_value() -> None:
    first = MultiLabelClassificationOutput(
        labels=[
            ClassificationOutput(
                label="a", confidence=0.5, explanation={"tokens": ["a", "b"]}
            )
        ]
    )
    second = first.model_copy(deep=True)
    assert hash(first) == hash(second)
    assert len({first, second}) == 1


def test_trace_hash_supports_its_dictionary_and_list_fields() -> None:
    trace: Trace = Trace(
        trace_id="id",
        created="2026-01-01",
        original_execution_time_ms=0,
        logged_values={"x": [1, 2]},
        models=[],
        tags=["online"],
    )
    assert hash(trace) == hash(trace.model_copy(deep=True))
