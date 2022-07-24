from pathlib import Path
from typing import Dict, List, Optional, TypeVar

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import average_precision_score

from ..unique import unique
from .draw_f1_iso_lines import draw_f1_iso_lines

T = TypeVar("T", str, float)


def evaluate_ranking(
    expected: List[T],
    actual_scores: List[float],
    target_recall: float,
    title: Optional[str] = "",
    disable_interpolation: bool = False,
    axes: Optional[plt.Axes] = None,
    output_svg: Optional[Path] = None,
    reverse_order: bool = False,
    plot: bool = True,
) -> Dict[T, float]:
    """Render the Precision-Recall curve of a ranking.

    And improved version of scikit-learn's [PR-curve](https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html#sphx-glr-auto-examples-model-selection-plot-precision-recall-py)

    Args:
        expected: Expected ordering of the elements
            (rank if it's an integer, alphabetical if a string)
        actual_scores: Actual ranking scores (need not be on the same scale as
            `expected`)
        title: Title of the plot.
        disable_interpolation: Do not interpolate.
        axes: Matplotlib axes for plotting inside a subplot.
        output_svg: If specified, save the chart as an svg to the given Path.
        reverse_order: Reverse the ranking specified by `expected`.
        plot: Display a plot on the screen.

    Returns:
        Precision values at given recall.
    """

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

        results: Dict[T, float] = {}
        for i in range(len(classes) - 1):
            binarized_expected = [
                (v < classes[i]) if reverse_order else (v > classes[i])
                for v in expected
            ]

            sorted_expected_actual = sorted(
                zip(binarized_expected, actual_scores), key=lambda v: v[1], reverse=True
            )
            precision = []
            recall = []
            correct = 0
            for all, (e, score) in enumerate(sorted_expected_actual, start=1):
                correct += int(e)
                precision.append(correct / all)
                recall.append(all / len(sorted_expected_actual))

            if not disable_interpolation:
                for j in range(len(precision) - 2, -1, -1):
                    precision[j] = max(precision[j], precision[j + 1])

            closest_recall_index = np.argmin(np.abs(np.array(recall) - target_recall))
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
