"""Bar chart plotting functions for HSR visualization."""

import matplotlib.pyplot as plt
import pandas as pd
from loguru import logger

from hsrws.visual.config import ChartConfig
from hsrws.visual.plotting.plotting_base import _setup_chart_basics


def plot_rarity_element_distribution(
    df: pd.DataFrame, config: ChartConfig = None, patch_version: str = None
) -> plt.Figure:
    """
    Plot character rarity distribution with element breakdown as a stacked bar chart.

    Args:
        df: DataFrame containing rarity, element, and count columns.
        config: Optional chart configuration. If not provided, a default is used.
        patch_version: Optional patch version to include in title.

    Returns:
        Matplotlib figure object.
    """
    logger.debug("Plotting rarity-element stacked bar chart...")

    # Use provided config or create default
    if config is None:
        config = ChartConfig()

    # Pivot the dataframe for stacked bar format
    pivot_df = df.pivot_table(
        index="Rarity", columns="Element", values="count", fill_value=0
    )

    # Create figure and axis with landscape ratio
    fig, ax = plt.subplots(figsize=config.get_size("bar"))

    # Create stacked bar chart
    pivot_df.plot(kind="bar", stacked=True, ax=ax, colormap=config.get_colormap("bar"))

    # Set up chart basics
    title = config.get_title("bar")
    _setup_chart_basics(
        fig,
        ax,
        config,
        "bar",
        title,
        patch_version,
        x_label="Rarity",
        y_label="Character Count",
    )

    # Configure legend
    config.configure_legend(ax, "bar")

    if config.tight_layout:
        plt.tight_layout()
    else:
        # Adjust for landscape ratio
        plt.subplots_adjust(bottom=0.15, left=0.1, right=0.9)

    return fig


def plot_path_rarity_distribution(
    df: pd.DataFrame, config: ChartConfig = None, patch_version: str = None
) -> plt.Figure:
    """
    Plot character path-rarity distribution as a grouped bar chart.

    Args:
        df: DataFrame containing path, rarity, and count columns.
        config: Optional chart configuration. If not provided, a default is used.
        patch_version: Optional patch version to include in title.

    Returns:
        Matplotlib figure object.
    """
    logger.debug("Plotting path-rarity grouped bar chart...")

    # Use provided config or create default
    if config is None:
        config = ChartConfig()

    # Pivot the dataframe for grouped bar format
    pivot_df = df.pivot_table(
        index="Path", columns="Rarity", values="count", fill_value=0
    )

    # Create figure and axis with portrait ratio (4:5)
    fig, ax = plt.subplots(figsize=config.get_size("grouped_bar"))

    # Create grouped bar chart
    pivot_df.plot(kind="bar", ax=ax, colormap=config.get_colormap("grouped_bar"))

    # Set up chart basics for portrait display
    title = config.get_title("grouped_bar")
    _setup_chart_basics(
        fig,
        ax,
        config,
        "grouped_bar",
        title,
        patch_version,
        x_label="Path",
        y_label="Character Count",
    )

    # Configure legend for top right position (override the default settings)
    legend = ax.legend(title="Rarity", loc="upper right")

    # Apply chart-specific font sizes for legend
    legend.get_title().set_fontsize(config.get_font_size("legend", "grouped_bar"))
    for text in legend.get_texts():
        text.set_fontsize(config.get_font_size("legend", "grouped_bar"))

    # Add data value annotations
    annotation_settings = config.get_annotation_settings("grouped_bar")
    for container in ax.containers:
        ax.bar_label(
            container,
            fmt=annotation_settings.get("fmt", "%.0f"),
            padding=annotation_settings.get("padding", 5),
            fontsize=config.get_font_size("annotation", "grouped_bar"),
            fontweight=annotation_settings.get("fontweight", "normal"),
        )

    # Add grid for better readability in vertical layout
    config.configure_grid(ax, "grouped_bar")

    if config.tight_layout:
        plt.tight_layout()
    else:
        # Adjust for portrait ratio
        plt.subplots_adjust(bottom=0.2, top=0.9)

    return fig
