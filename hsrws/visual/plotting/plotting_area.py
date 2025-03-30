"""Area chart plotting functions for HSR visualization."""

import matplotlib.pyplot as plt
import pandas as pd
from loguru import logger

from hsrws.visual.config import ChartConfig
from hsrws.visual.plotting.plotting_base import _setup_chart_basics


def plot_element_balance_evolution(
    df: pd.DataFrame, config: ChartConfig = None, patch_version: str = None
) -> plt.Figure:
    """
    Plot elemental balance evolution across versions as an area chart.

    Args:
        df: DataFrame from ElementCharacterCountByVersion view.
        config: Optional chart configuration. If not provided, a default is used.
        patch_version: Optional patch version to include in title.

    Returns:
        Matplotlib figure object.
    """
    logger.debug("Plotting elemental balance evolution area chart...")

    # Use provided config or create default
    if config is None:
        config = ChartConfig()

    # Create figure and axis with landscape ratio for evolutionary data
    fig, ax = plt.subplots(figsize=config.get_size("area"))

    # Create area chart
    df.set_index("Version").plot(
        kind="area",
        stacked=True,
        ax=ax,
        colormap=config.get_colormap("area"),
        alpha=0.7,  # Add transparency to make layers more visible
    )

    # Set up chart basics for landscape display
    title = config.get_title("area")
    _setup_chart_basics(
        fig,
        ax,
        config,
        "area",
        title,
        patch_version,
        x_label="Version",
        y_label="Character Count",
    )

    # Configure legend - for landscape charts, position legend to save horizontal space
    config.configure_legend(ax, "area")

    # Add grid for better readability
    config.configure_grid(ax, "area")

    if config.tight_layout:
        plt.tight_layout()
    else:
        # Adjust for landscape ratio
        plt.subplots_adjust(bottom=0.2, left=0.1, right=0.9)

    return fig
