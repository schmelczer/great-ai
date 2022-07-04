from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes


def draw_f1_iso_lines(
    resolution: int = 1000,
    min: float = 0.2,
    max: float = 0.8,
    steps: int = 4,
    axes: Optional[Axes] = None,
) -> None:
    if axes is None:
        axes = plt.axes()

    for f_score in np.linspace(min, max, num=steps):
        x = np.linspace(f_score / (2 - f_score), 1, num=resolution)
        y = f_score * x / (2 * x - f_score)

        axes.plot(x[y >= 0], y[y >= 0], color="gray", alpha=0.2)

        axes.annotate(
            f"f1={f_score:0.1f}",
            backgroundcolor="w",
            xy=(0.9, y[int(resolution * 0.9)] + 0.02),
        )
