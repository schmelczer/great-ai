"""Shared local paths and small datasets for the documentation notebooks."""

import json
import os
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "docs/tutorial/data"
SURVEY_DIR = ROOT / "docs/surveys"
FULL_RUN = os.environ.get("GREAT_AI_NOTEBOOK_FULL") == "1"


def setup_notebook(workflow: str) -> Path:
    """Keep related notebooks' models and traces together, outside source files."""
    from great_ai import ParallelTinyDbDriver, configure
    from great_ai.large_file import LargeFileLocal

    base = Path(os.environ.get("GREAT_AI_NOTEBOOK_WORKDIR", ROOT / ".cache/notebooks"))
    suffix = "-full" if FULL_RUN else ""
    work_dir = (base / (workflow + suffix)).resolve()
    work_dir.mkdir(parents=True, exist_ok=True)
    LargeFileLocal.cache_path = work_dir / "models-cache"
    ParallelTinyDbDriver.path_to_db = work_dir / "tracing_database.json"
    configure(
        large_file_implementation=LargeFileLocal,
        tracing_database_factory=ParallelTinyDbDriver,
        disable_se4ml_banner=True,
        seed=42,
    )
    print(f"Notebook artifacts: {work_dir}")
    return work_dir


def mag_lines(path: Path, per_label: Optional[int] = None) -> List[str]:
    """Read the bundled MAG data, optionally limiting each class for a quick run."""
    counts: Counter = Counter()
    lines = []
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            label = json.loads(line)["label"]
            if per_label is None or counts[label] < per_label:
                counts[label] += 1
                lines.append(line)
    return lines


def demo_annotations() -> List[dict]:
    """Synthetic annotations for exercising the pipeline, not measuring quality."""
    annotations: List[Dict[str, int]] = [{}, {}]
    for index, topic in enumerate(
        ["protein", "cancer", "solar", "quantum", "neural", "genome"]
    ):
        for sample in range(10):
            positive = sample % 2
            sentence = (
                f"Our {topic} method improves prediction accuracy in experiment {sample}."
                if positive
                else f"The {topic} dataset contains observations from experiment {sample}."
            )
            annotations[0][sentence] = positive
            annotations[1][sentence] = (
                1 - positive if (index * 10 + sample) % 11 == 0 else positive
            )
    return annotations
