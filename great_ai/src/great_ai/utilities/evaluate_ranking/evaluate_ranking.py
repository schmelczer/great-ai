from pathlib import Path
from typing import Dict, List, Optional, Union

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve

from ..unique import unique
from .draw_f1_iso_lines import draw_f1_iso_lines


def evaluate_ranking(
    expected: List[Union[str, float]],
    actual_scores: List[float],
    target_recall: float,
    title: Optional[str] = "",
    disable_interpolation: bool = False,
    axes: Optional[plt.Axes] = None,
    output_svg: Optional[Path] = None,
    reverse_order: bool = False,
    plot: bool = True,
) -> Dict[Union[str, float], float]:
    assert 0 <= target_recall <= 1

    if plot and axes is None:
        fig = plt.figure(figsize=(20, 10))
        fig.patch.set_facecolor("white")
        ax = plt.axes()
    else:
        ax = axes

    classes = sorted(unique(expected), reverse=reverse_order)
    str_classes = [str(c) for c in classes]

    with matplotlib.rc_context({"font.size": 20}):
        if plot:
            ax.set_xmargin(0)

            draw_f1_iso_lines(axes=ax)

        results: Dict[Union[str, float], float] = {}
        for i in range(len(classes) - 1):
            binarized_expected = [
                (v < classes[i]) if reverse_order else (v > classes[i])
                for v in expected
            ]
            precision, recall, _ = precision_recall_curve(
                binarized_expected, actual_scores
            )

            if not disable_interpolation:
                for j in range(1, len(precision)):
                    precision[j] = max(precision[j - 1], precision[j])

            closest_recall_index = np.argmin(np.abs(recall - target_recall))
            precision_at_closest_recall = precision[closest_recall_index]
            average_precision = average_precision_score(
                binarized_expected, actual_scores
            )
            results[classes[i]] = precision_at_closest_recall

            if plot:
                ax.plot(
                    recall,
                    precision,
                    label=f"{'|'.join(str_classes[:i + 1])} ↔ {'|'.join(str_classes[i+1:])} (P@{target_recall:.2f}={precision_at_closest_recall:.2f}, AP={average_precision:.2f})",
                )

        if plot:
            ax.legend(loc="upper right")
            ax.axvline(x=target_recall, linestyle="--", color="#55c6bb", linewidth=2.0)

            if title is None:
                title = "Ranking evaluation"

            ax.set_title(f'{title} ({" < ".join(str_classes)})', pad=20)

            ax.set_xlabel("Recall")
            ax.set_ylabel("Precision")

            ax.set_xticks([target_recall] + sorted(ax.get_xticks()))

        if plot and output_svg is None:
            if axes is None:
                plt.show()
        elif output_svg:
            plt.savefig(output_svg, format="svg")

    return results
