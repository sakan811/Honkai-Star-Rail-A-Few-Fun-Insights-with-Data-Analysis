"""Heatmap plotting functions for HSR visualization."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from loguru import logger

from hsrws.visual.config import ChartConfig
from hsrws.visual.plotting.plotting_base import _setup_chart_basics


def plot_element_path_heatmap(
    df: pd.DataFrame, config: ChartConfig = None, patch_version: str = None
) -> plt.Figure:
    """
    Plot a heatmap of element vs path distribution.

    Args:
        df: DataFrame containing element, path, and count columns.
        config: Optional chart configuration. If not provided, a default is used.
        patch_version: Optional patch version to include in title.

    Returns:
        Matplotlib figure object.
    """
    logger.debug("Plotting element-path heatmap...")

    # Use provided config or create default
    if config is None:
        config = ChartConfig()

    # Create figure and axis with square ratio for symmetric heatmap cells
    fig, ax = plt.subplots(figsize=config.get_size("heatmap"))

    # Pivot the dataframe to create heatmap format
    pivot_df = df.pivot(index="Element", columns="Path", values="count")

    # Fill NaN values with 0 instead of leaving blank
    pivot_df = pivot_df.fillna(0)

    # Get annotation settings
    annotation_settings = config.get_annotation_settings("heatmap")

    # Create heatmap with cell annotations
    sns.heatmap(
        pivot_df,
        annot=True,
        fmt=annotation_settings.get("fmt", ".0f"),
        cmap=config.get_colormap("heatmap"),
        linewidths=0.5,
        ax=ax,
        annot_kws={
            "size": config.get_font_size("annotation", "heatmap"),
            "fontweight": annotation_settings.get("fontweight", "normal"),
        },
    )

    # Set up chart basics for square display
    title = config.get_title("heatmap")
    _setup_chart_basics(
        fig,
        ax,
        config,
        "heatmap",
        title,
        patch_version,
        x_label="Path",
        y_label="Element",
    )

    # Horizontal y-axis labels for better readability
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

    if config.tight_layout:
        plt.tight_layout()
    else:
        plt.subplots_adjust(left=0.15, right=0.9, bottom=0.15, top=0.9)

    return fig
