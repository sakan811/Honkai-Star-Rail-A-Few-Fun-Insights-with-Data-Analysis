"""Bar chart plotting functions for HSR visualization."""

import matplotlib.pyplot as plt
import pandas as pd
from loguru import logger

from hsrws.visual.config import ChartConfig
from hsrws.visual.plotting.plotting_base import _setup_chart_basics
from hsrws.visual.data_utils import get_rarity_colors


def plot_rarity_element_distribution(
    df: pd.DataFrame, config: ChartConfig = None, patch_version: str = None
) -> plt.Figure:
    """
    Plot character element distribution with rarity breakdown as a grouped bar chart.

    Args:
        df: DataFrame containing rarity, element, and count columns.
        config: Optional chart configuration. If not provided, a default is used.
        patch_version: Optional patch version to include in title.

    Returns:
        Matplotlib figure object.
    """
    logger.debug("Plotting element-rarity grouped bar chart...")

    # Use provided config or create default
    if config is None:
        config = ChartConfig()

    # Pivot the dataframe for grouped bar format (Element on X-axis)
    pivot_df = df.pivot_table(
        index="Element", columns="Rarity", values="count", fill_value=0
    )

    # Get rarity-specific colors
    rarity_colors = get_rarity_colors()

    # Create figure and axis with portrait ratio (4:5)
    fig, ax = plt.subplots(figsize=config.get_size("grouped_bar"))

    # Create grouped bar chart with rarity-specific colors
    pivot_df.plot(kind="bar", ax=ax, color=rarity_colors)

    # Set up chart basics for portrait display
    title = config.get_title("grouped_bar")
    _setup_chart_basics(
        fig,
        ax,
        config,
        "grouped_bar",
        title,
        patch_version,
        x_label="Element",
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

    # Get rarity-specific colors
    rarity_colors = get_rarity_colors()

    # Create figure and axis with portrait ratio (4:5)
    fig, ax = plt.subplots(figsize=config.get_size("grouped_bar"))

    # Create grouped bar chart with rarity-specific colors
    pivot_df.plot(kind="bar", ax=ax, color=rarity_colors)

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
