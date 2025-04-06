"""Heatmap plotting functions for HSR visualization."""

from typing import Optional
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from loguru import logger

from hsrws.visual.config import ChartConfig
from hsrws.visual.config.config_chart_settings import get_default_titles


def plot_element_path_heatmap(
    df: pd.DataFrame, config: Optional[ChartConfig] = None, patch_version: Optional[str] = None
) -> Figure:
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

    # Pivot the dataframe to create heatmap format
    pivot_df = df.pivot(index="Element", columns="Path", values="count")

    # Fill NaN values with 0 instead of leaving blank
    pivot_df = pivot_df.fillna(0)

    fig, ax = plt.subplots()
    
    # Create heatmap with cell annotations
    sns.heatmap(
        pivot_df,
        annot=True,
        fmt=".0f",
        cmap="viridis",
        linewidths=0.5,
        ax=ax,
    )

    ax.set_xlabel("Path")
    ax.set_ylabel("Element")
    
    # Horizontal y-axis labels for better readability
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    
    titles = get_default_titles()
    title = titles["heatmap"]  + f" - {patch_version}"
    
    ax.set_title(title)
    
    return fig
