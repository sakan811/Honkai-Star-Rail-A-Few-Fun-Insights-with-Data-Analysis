"""Plotting functions for HSR data visualization."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from loguru import logger

from hsrws.visual.config import ChartConfig


def _setup_chart_basics(fig, ax, config, chart_type, title, patch_version=None, x_label=None, y_label=None):
    """
    Set up basic chart properties with appropriate aspect ratio based on chart type.
    
    Args:
        fig: Matplotlib figure object
        ax: Matplotlib axis object
        config: ChartConfig object
        chart_type: Type of chart for retrieving specific settings
        title: Chart title
        patch_version: Optional patch version to append to title
        x_label: Label for x-axis
        y_label: Label for y-axis
        
    Returns:
        None (modifies the axis object in-place)
    """
    # Get chart size to calculate aspect ratio
    chart_size = config.get_size(chart_type)
    aspect_ratio = chart_size[0] / chart_size[1] if chart_size[1] != 0 else 1
    
    # Set aspect ratio based on chart type
    # For square charts (1:1 ratio), force box_aspect
    if abs(aspect_ratio - 1) < 0.1:  # If the ratio is approximately 1:1
        ax.set_box_aspect(1)
    
    # Set title with optional patch version
    if patch_version:
        title = f"{title} - {patch_version}"
    
    # Apply title wrapping if enabled
    if hasattr(config, 'wrap_text'):
        title = config.wrap_text(title)
    
    ax.set_title(title, fontsize=config.get_font_size('title', chart_type), pad=15)
    
    # Set axis labels if provided
    if x_label:
        ax.set_xlabel(x_label, fontsize=config.get_font_size('label', chart_type), labelpad=10)
    if y_label:
        ax.set_ylabel(y_label, fontsize=config.get_font_size('label', chart_type), labelpad=10)
    
    # Set tick label font sizes
    ax.tick_params(axis='both', which='major', labelsize=config.get_font_size('tick', chart_type))
    
    # Rotate x-axis labels to prevent overlap if auto_rotate_labels is enabled
    if config.auto_rotate_labels:
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")


def plot_element_path_heatmap(df: pd.DataFrame, config: ChartConfig = None, patch_version: str = None) -> plt.Figure:
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
            "size": config.get_font_size('annotation', 'heatmap'),
            "fontweight": annotation_settings.get("fontweight", "normal")
        }
    )
    
    # Set up chart basics for square display
    title = config.get_title("heatmap")
    _setup_chart_basics(
        fig, ax, config, "heatmap", title, patch_version,
        x_label="Path", y_label="Element"
    )
    
    # Horizontal y-axis labels for better readability
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    
    if config.tight_layout:
        plt.tight_layout()
    else:
        plt.subplots_adjust(left=0.15, right=0.9, bottom=0.15, top=0.9)
    
    return fig


def plot_rarity_element_distribution(df: pd.DataFrame, config: ChartConfig = None, patch_version: str = None) -> plt.Figure:
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
    pivot_df = df.pivot_table(index="Rarity", columns="Element", values="count", fill_value=0)
    
    # Create figure and axis with landscape ratio
    fig, ax = plt.subplots(figsize=config.get_size("bar"))
    
    # Create stacked bar chart
    pivot_df.plot(kind="bar", stacked=True, ax=ax, colormap=config.get_colormap("bar"))
    
    # Set up chart basics
    title = config.get_title("bar")
    _setup_chart_basics(
        fig, ax, config, "bar", title, patch_version,
        x_label="Rarity", y_label="Character Count"
    )
    
    # Configure legend
    config.configure_legend(ax, "bar")
    
    if config.tight_layout:
        plt.tight_layout()
    else:
        # Adjust for landscape ratio
        plt.subplots_adjust(bottom=0.15, left=0.1, right=0.9)
        
    return fig


def plot_version_release_timeline(df: pd.DataFrame, config: ChartConfig = None, patch_version: str = None) -> plt.Figure:
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
        linewidth=primary_marker.get("linewidth", 2)
    )
    
    # Add data points annotation
    annotation_settings = config.get_annotation_settings("timeline")
    for x, y in zip(df["Version"], df["character_count"]):
        fontsize = config.get_font_size('annotation', 'timeline')
        if annotation_settings.get("fontsize_offset", 0) > 0:
            fontsize += annotation_settings.get("fontsize_offset")
        
        ax.annotate(
            f"{y:.0f}",
            (x, y), 
            textcoords=annotation_settings.get("textcoords", "offset points"),
            xytext=annotation_settings.get("xytext", (0, 15)), 
            ha=annotation_settings.get("ha", "center"),
            fontsize=fontsize,
            fontweight=annotation_settings.get("fontweight", "bold")
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
        markersize=secondary_marker.get("markersize", 6)
    )
    ax2.set_ylabel("Cumulative Character Count", 
                  fontsize=config.get_font_size('label', 'timeline'), 
                  color=secondary_marker.get("color", "darkred"))
    
    # Set up chart basics - landscape ratio is optimal for timelines
    title = config.get_title("timeline")
    _setup_chart_basics(
        fig, ax, config, "timeline", title, patch_version,
        x_label="Version", y_label="New Characters Per Version"
    )
    
    # Set x-axis ticks to show all versions
    ax.set_xticks(df["Version"])
    
    ax2.tick_params(axis='y', which='major', labelsize=config.get_font_size('tick', 'timeline'))
    
    # Add grid for better readability
    config.configure_grid(ax, "timeline")
    
    if config.tight_layout:
        plt.tight_layout()
    else:
        # Adjust for landscape ratio
        plt.subplots_adjust(bottom=0.2, left=0.1, right=0.9)
    return fig


def plot_element_balance_evolution(df: pd.DataFrame, config: ChartConfig = None, patch_version: str = None) -> plt.Figure:
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
        alpha=0.7  # Add transparency to make layers more visible
    )
    
    # Set up chart basics for landscape display
    title = config.get_title("area")
    _setup_chart_basics(
        fig, ax, config, "area", title, patch_version,
        x_label="Version", y_label="Character Count"
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


def plot_path_rarity_distribution(df: pd.DataFrame, config: ChartConfig = None, patch_version: str = None) -> plt.Figure:
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
    pivot_df = df.pivot_table(index="Path", columns="Rarity", values="count", fill_value=0)
    
    # Create figure and axis with portrait ratio (4:5)
    fig, ax = plt.subplots(figsize=config.get_size("grouped_bar"))
    
    # Create grouped bar chart
    pivot_df.plot(kind="bar", ax=ax, colormap=config.get_colormap("grouped_bar"))
    
    # Set up chart basics for portrait display
    title = config.get_title("grouped_bar")
    _setup_chart_basics(
        fig, ax, config, "grouped_bar", title, patch_version,
        x_label="Path", y_label="Character Count"
    )
    
    # Configure legend for top right position (override the default settings)
    legend = ax.legend(title="Rarity", loc="upper right")
    
    # Apply chart-specific font sizes for legend
    legend.get_title().set_fontsize(config.get_font_size('legend', 'grouped_bar'))
    for text in legend.get_texts():
        text.set_fontsize(config.get_font_size('legend', 'grouped_bar'))
    
    # Add data value annotations
    annotation_settings = config.get_annotation_settings("grouped_bar")
    for container in ax.containers:
        labels = ax.bar_label(
            container, 
            fmt=annotation_settings.get("fmt", "%.0f"),
            padding=annotation_settings.get("padding", 5),
            fontsize=config.get_font_size('annotation', 'grouped_bar'),
            fontweight=annotation_settings.get("fontweight", "normal")
        )
    
    # Add grid for better readability in vertical layout
    config.configure_grid(ax, "grouped_bar")
    
    if config.tight_layout:
        plt.tight_layout()
    else:
        # Adjust for portrait ratio
        plt.subplots_adjust(bottom=0.2, top=0.9)
    
    return fig
