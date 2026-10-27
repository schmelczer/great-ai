from great_ai import ParallelTinyDbDriver, configure
from great_ai.context import get_context
from great_ai.large_file import LargeFileLocal


def test_explicit_custom_backends_are_preserved(isolated_context: None) -> None:
    class CustomDatabase(ParallelTinyDbDriver):
        pass

    class CustomStorage(LargeFileLocal):
        pass

    configure(
        tracing_database_factory=CustomDatabase,
        large_file_implementation=CustomStorage,
        disable_se4ml_banner=True,
    )
    assert isinstance(get_context().tracing_database, CustomDatabase)
    assert get_context().large_file_implementation is CustomStorage
