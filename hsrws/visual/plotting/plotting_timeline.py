"""Timeline plotting functions for HSR visualization."""

import matplotlib.pyplot as plt
import pandas as pd
from loguru import logger

from hsrws.visual.config import ChartConfig
from hsrws.visual.plotting.plotting_base import _setup_chart_basics


def plot_version_release_timeline(
    df: pd.DataFrame, config: ChartConfig = None, patch_version: str = None
) -> plt.Figure:
    """
    Plot version release timeline showing character introduction rate.

    Args:
        df: DataFrame containing version and character_count columns.
        config: Optional chart configuration. If not provided, a default is used.
        patch_version: Optional patch version to include in title.

    Returns:
        Matplotlib figure object.
    """
    logger.debug("Plotting version release timeline...")

    # Use provided config or create default
    if config is None:
        config = ChartConfig()

    # Create figure and axis with landscape aspect ratio
    fig, ax = plt.subplots(figsize=config.get_size("timeline"))

    # Get marker settings
    primary_marker = config.get_marker_settings("timeline", "primary")
    secondary_marker = config.get_marker_settings("timeline", "secondary")

    # Create timeline plot
    ax.plot(
        df["Version"],
        df["character_count"],
        marker=primary_marker.get("marker", "o"),
        markersize=primary_marker.get("markersize", 8),
        linewidth=primary_marker.get("linewidth", 2),
    )

    # Add data points annotation
    annotation_settings = config.get_annotation_settings("timeline")
    for x, y in zip(df["Version"], df["character_count"]):
        fontsize = config.get_font_size("annotation", "timeline")
        if annotation_settings.get("fontsize_offset", 0) > 0:
            fontsize += annotation_settings.get("fontsize_offset")

        ax.annotate(
            f"{y:.0f}",
            (x, y),
            textcoords=annotation_settings.get("textcoords", "offset points"),
            xytext=annotation_settings.get("xytext", (0, 15)),
            ha=annotation_settings.get("ha", "center"),
            fontsize=fontsize,
            fontweight=annotation_settings.get("fontweight", "bold"),
        )

    # Calculate cumulative sum for additional information
    df["cumulative_count"] = df["character_count"].cumsum()
    ax2 = ax.twinx()
    ax2.plot(
        df["Version"],
        df["cumulative_count"],
        marker=secondary_marker.get("marker", "s"),
        linestyle=secondary_marker.get("linestyle", "--"),
        color=secondary_marker.get("color", "darkred"),
        alpha=secondary_marker.get("alpha", 0.7),
        markersize=secondary_marker.get("markersize", 6),
    )
    ax2.set_ylabel(
        "Cumulative Character Count",
        fontsize=config.get_font_size("label", "timeline"),
        color=secondary_marker.get("color", "darkred"),
    )

    # Set up chart basics - landscape ratio is optimal for timelines
    title = config.get_title("timeline")
    _setup_chart_basics(
        fig,
        ax,
        config,
        "timeline",
        title,
        patch_version,
        x_label="Version",
        y_label="New Characters Per Version",
    )

    # Set x-axis ticks to show all versions
    ax.set_xticks(df["Version"])

    ax2.tick_params(
        axis="y", which="major", labelsize=config.get_font_size("tick", "timeline")
    )

    # Add grid for better readability
    config.configure_grid(ax, "timeline")

    if config.tight_layout:
        plt.tight_layout()
    else:
        # Adjust for landscape ratio
        plt.subplots_adjust(bottom=0.2, left=0.1, right=0.9)
    return fig
