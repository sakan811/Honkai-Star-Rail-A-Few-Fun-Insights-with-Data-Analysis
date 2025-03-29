"""Donut chart creation module."""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def create_donut_chart(ax, data, title, cmap, config):
    """
    Creates a donut chart on the given axes.

    Args:
        ax: Matplotlib axes object.
        data: DataFrame with 'category' and 'count' columns.
        title: Chart title.
        cmap: Color map to use.
        config: Chart configuration object.
    """
    # Create a pie chart with a hole in the middle (donut chart)
    wedges, texts, autotexts = ax.pie(
        data["count"],
        labels=data["category"],
        autopct="%1.1f%%",
        textprops={"fontsize": config.label_fontsize},
        wedgeprops={"width": config.donut_width, "edgecolor": "w"},
        pctdistance=config.pct_distance,
        colors=sns.color_palette(cmap, len(data)),
    )

    # Style the chart
    plt.setp(autotexts, size=config.pct_fontsize, weight="bold")
    plt.setp(texts, size=config.label_fontsize)

    # Add a circle at the center to create the donut hole
    centre_circle = plt.Circle((0, 0), config.donut_hole_radius, fc="white")
    ax.add_patch(centre_circle)

    # Add total count in the center
    total = data["count"].sum()
    ax.text(
        0,
        0,
        f"Total\n{total}",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=config.center_text_fontsize,
        fontweight="bold",
    )

    # Add data labels for each slice
    for i, (wedge, category, count) in enumerate(
        zip(wedges, data["category"], data["count"])
    ):
        ang = (wedge.theta2 - wedge.theta1) / 2.0 + wedge.theta1
        x = 0.75 * 0.5 * np.cos(np.deg2rad(ang))
        y = 0.75 * 0.5 * np.sin(np.deg2rad(ang))
        ax.annotate(
            f"{count}",
            xy=(x, y),
            xytext=(0, 0),
            textcoords="offset points",
            ha="center",
            va="center",
            fontsize=config.count_fontsize,
            fontweight="bold",
        )

    # Add title
    ax.set_title(title, fontsize=config.title_fontsize, pad=config.title_pad)
