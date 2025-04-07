"""Area chart plotting functions for HSR visualization."""

from typing import Optional
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
from loguru import logger
import seaborn as sns

from hsrws.visual.data_utils import get_element_colors, get_path_colors


def plot_element_balance_evolution(
    df: pd.DataFrame, patch_version: Optional[str] = None
) -> Figure:
    """
    Plot elemental balance evolution across versions as an area chart.
    Shows the cumulative sum of characters for each element across versions.

    Args:
        df: DataFrame with Version, Element, and count columns from ORM query
             or already pivoted with Version and element columns.
        patch_version: Optional patch version to include in title.

    Returns:
        Matplotlib figure object.
    """
    logger.debug("Plotting elemental balance evolution area chart...")

    # Get element-specific colors instead of using tab10
    element_colors = get_element_colors()

    fig, ax = plt.subplots()
    sns.lineplot(
        data=df,
        x="Version",
        y="count",
        hue="Element",
        palette=element_colors,
        linewidth=2.5,
    )

    # Place legend outside the plot area to the right
    ax.legend(title="Element", bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.set_xlabel("Version")
    ax.set_ylabel("Cumulative Character Count")

    title = "Honkai: Star Rail Elemental Balance Evolution Across Versions"
    if patch_version:
        title += f" - {patch_version}"

    ax.set_title(title)
    
    # Adjust layout to make room for the legend
    plt.tight_layout()

    return fig


def plot_path_balance_evolution(
    df: pd.DataFrame, patch_version: Optional[str] = None
) -> Figure:
    """
    Plot path balance evolution across versions as a line chart.
    Shows the cumulative sum of characters for each path across versions.

    Args:
        df: DataFrame with Version, Path, and count columns from ORM query
             or already pivoted with Version and path columns.
        patch_version: Optional patch version to include in title.

    Returns:
        Matplotlib figure object.
    """
    logger.debug("Plotting path balance evolution line chart...")

    # Get path-specific colors
    path_colors = get_path_colors()

    fig, ax = plt.subplots()
    sns.lineplot(
        data=df,
        x="Version",
        y="count",
        hue="Path",
        palette=path_colors,
        linewidth=2.5,
    )

    # Place legend outside the plot area to the right
    ax.legend(title="Path", bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.set_xlabel("Version")
    ax.set_ylabel("Cumulative Character Count")

    title = "Honkai: Star Rail Path Balance Evolution Across Versions"
    if patch_version:
        title += f" - {patch_version}"

    ax.set_title(title)
    
    # Adjust layout to make room for the legend
    plt.tight_layout()

    return fig
