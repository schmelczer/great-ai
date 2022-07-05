from great_ai import GreatAI


def test_process_batch() -> None:
    @GreatAI.create(return_raw_result=True)
    def f(x):
        return x + 2

    assert f.process_batch([3, 9, 34]) == [5, 11, 36]
