try:
    import en_core_web_lg
except ImportError:
    import subprocess

    print("Spacy model en_core_web_lg not found locally, downloading...")

    subprocess.call(
        [
            "pip",
            "install",
            "https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.2.0/en_core_web_lg-3.2.0-py3-none-any.whl",
        ]
    )
    import en_core_web_lg

from .external.negspacy import negation  # noqa: F401 it's important to import this

nlp = en_core_web_lg.load()

nlp.add_pipe("negex")
