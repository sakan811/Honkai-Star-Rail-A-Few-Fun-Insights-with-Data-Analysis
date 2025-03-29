"""Plotting functions for HSR data visualization."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from loguru import logger

from hsrws.visual.config import ChartConfig


def plot_element_path_heatmap(df: pd.DataFrame, config: ChartConfig = None, patch_version: str = None) -> plt.Figure:
    """
    Plot character distribution by element and path as a heatmap.

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
    
    # Pivot the dataframe for heatmap format
    pivot_df = df.pivot_table(index="Element", columns="Path", values="count", fill_value=0)
    
    # Create figure and axis with square aspect ratio
    fig, ax = plt.subplots(figsize=config.get_size("heatmap"))
    
    # Force square aspect ratio
    ax.set_aspect('equal')
    
    # Get annotation settings
    annotation_settings = config.get_annotation_settings("heatmap")
    
    # Create heatmap
    sns.heatmap(
        pivot_df, 
        annot=True, 
        fmt=annotation_settings.get("fmt", ".0f"),
        cmap=config.get_colormap("heatmap"), 
        linewidths=0.5, 
        ax=ax,
        cbar_kws={
            "label": "Character Count", 
            "pad": 0.02  # Add some padding between the colorbar and the plot
        },
        annot_kws={"fontsize": config.annotation_fontsize}
    )
    
    # Adjust colorbar label font size
    cbar = ax.collections[0].colorbar
    cbar.ax.set_ylabel("Character Count", fontsize=config.label_fontsize)
    
    # Set title and labels
    title = config.get_title("heatmap")
    if patch_version:
        title = f"{title} - {patch_version}"
    ax.set_title(title, fontsize=config.title_fontsize, pad=20)  # Add padding to title
    ax.set_xlabel("Path", fontsize=config.label_fontsize, labelpad=15)  # Add padding to x-label
    ax.set_ylabel("Element", fontsize=config.label_fontsize, labelpad=15)  # Add padding to y-label
    
    # Set tick label font sizes and rotation
    ax.tick_params(axis='both', which='major', labelsize=config.tick_fontsize, pad=8)  # Add padding to tick labels
    # Rotate y-axis labels to horizontal for better readability and prevent overlapping
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    # Rotate x-axis labels for better fit if needed
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    if config.tight_layout:
        plt.tight_layout()
    else:
        # Only use subplot adjustments if tight_layout is disabled
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
    
    # Create figure and axis with 1:1 ratio
    fig, ax = plt.subplots(figsize=config.get_size("bar"))
    
    # Create stacked bar chart
    pivot_df.plot(kind="bar", stacked=True, ax=ax, colormap=config.get_colormap("bar"))
    
    # Set title and labels
    title = config.get_title("bar")
    if patch_version:
        title = f"{title} - {patch_version}"
    ax.set_title(title, fontsize=config.title_fontsize)
    ax.set_xlabel("Rarity", fontsize=config.label_fontsize)
    ax.set_ylabel("Character Count", fontsize=config.label_fontsize)
    
    # Set tick label font sizes
    ax.tick_params(axis='both', which='major', labelsize=config.tick_fontsize)
    
    # Configure legend
    legend_settings = config.get_legend_settings("bar")
    legend = ax.legend(
        title=legend_settings.get("title", "Element"),
        bbox_to_anchor=legend_settings.get("bbox_to_anchor", (1.05, 1)),
        loc=legend_settings.get("loc", "upper left")
    )
    legend.get_title().set_fontsize(config.legend_fontsize)
    for text in legend.get_texts():
        text.set_fontsize(config.legend_fontsize)
    
    if config.tight_layout:
        plt.tight_layout()
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
    
    # Create figure and axis with wider width for better label spacing
    fig, ax = plt.subplots(figsize=config.get_size("timeline"))
    
    # Get marker settings
    primary_marker = config.get_marker_settings("timeline", "primary")
    secondary_marker = config.get_marker_settings("timeline", "secondary")
    
    # Create timeline plot
    ax.plot(
        df["Version"], 
        df["character_count"], 
        marker=primary_marker.get("marker", "o"),
        markersize=primary_marker.get("markersize", 10),
        linewidth=primary_marker.get("linewidth", 2)
    )
    
    # Add data points annotation
    annotation_settings = config.get_annotation_settings("timeline")
    for x, y in zip(df["Version"], df["character_count"]):
        ax.annotate(
            f"{y:.0f}",  # Use .0f format to handle potential float values
            (x, y), 
            textcoords=annotation_settings.get("textcoords", "offset points"),
            xytext=annotation_settings.get("xytext", (0, 10)), 
            ha=annotation_settings.get("ha", "center"),
            fontsize=config.annotation_fontsize
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
        markersize=secondary_marker.get("markersize", 8)
    )
    ax2.set_ylabel("Cumulative Character Count", fontsize=config.label_fontsize, color=secondary_marker.get("color", "darkred"))
    
    # Set title and labels
    title = config.get_title("timeline")
    if patch_version:
        title = f"{title} - {patch_version}"
    ax.set_title(title, fontsize=config.title_fontsize)
    ax.set_xlabel("Version", fontsize=config.label_fontsize)
    ax.set_ylabel("New Characters Per Version", fontsize=config.label_fontsize)
    
    # Set x-axis ticks to show all versions
    ax.set_xticks(df["Version"])
    
    # Set tick label font sizes and rotate x labels to avoid overlap
    ax.tick_params(axis='both', which='major', labelsize=config.tick_fontsize)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    ax2.tick_params(axis='y', which='major', labelsize=config.tick_fontsize)
    
    # Add grid for better readability
    grid_settings = config.get_grid_settings("timeline")
    if grid_settings.get("visible", True):
        ax.grid(
            True, 
            linestyle=grid_settings.get("linestyle", "--"), 
            alpha=grid_settings.get("alpha", 0.7)
        )
    
    if config.tight_layout:
        plt.tight_layout()
    else:
        # Add extra bottom margin to prevent x-label cropping
        plt.subplots_adjust(bottom=0.15)
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
    
    # Create figure and axis with 1:1 ratio
    fig, ax = plt.subplots(figsize=config.get_size("area"))
    
    # Melt the DataFrame for area chart (convert from wide to long format)
    elements = ["Fire", "Ice", "Lightning", "Wind", "Physical", "Quantum", "Imaginary"]
    melted_df = pd.melt(
        df, 
        id_vars=["Version"], 
        value_vars=elements,
        var_name="Element", 
        value_name="Count"
    )
    
    # Create a pivot table for the area chart
    pivot_df = melted_df.pivot(index="Version", columns="Element", values="Count")
    
    # Plot area chart
    pivot_df.plot.area(ax=ax, alpha=0.7, colormap=config.get_colormap("area"))
    
    # Set title and labels
    title = config.get_title("area")
    if patch_version:
        title = f"{title} - {patch_version}"
    ax.set_title(title, fontsize=config.title_fontsize)
    ax.set_xlabel("Version", fontsize=config.label_fontsize)
    ax.set_ylabel("Cumulative Character Count", fontsize=config.label_fontsize)
    
    # Set tick label font sizes
    ax.tick_params(axis='both', which='major', labelsize=config.tick_fontsize)
    
    # Configure legend
    legend_settings = config.get_legend_settings("area")
    legend = ax.legend(
        title=legend_settings.get("title", "Element"),
        bbox_to_anchor=legend_settings.get("bbox_to_anchor", (1.05, 1)),
        loc=legend_settings.get("loc", "upper left")
    )
    legend.get_title().set_fontsize(config.legend_fontsize)
    for text in legend.get_texts():
        text.set_fontsize(config.legend_fontsize)
    
    # Add grid for better readability
    grid_settings = config.get_grid_settings("area")
    if grid_settings.get("visible", True):
        ax.grid(
            True, 
            linestyle=grid_settings.get("linestyle", "--"), 
            alpha=grid_settings.get("alpha", 0.7)
        )
    
    if config.tight_layout:
        plt.tight_layout()
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
    
    # Create figure and axis with 1:1 ratio
    fig, ax = plt.subplots(figsize=config.get_size("grouped_bar"))
    
    # Create grouped bar chart
    pivot_df.plot(kind="bar", ax=ax, colormap=config.get_colormap("grouped_bar"))
    
    # Set title and labels
    title = config.get_title("grouped_bar")
    if patch_version:
        title = f"{title} - {patch_version}"
    ax.set_title(title, fontsize=config.title_fontsize)
    ax.set_xlabel("Path", fontsize=config.label_fontsize)
    ax.set_ylabel("Character Count", fontsize=config.label_fontsize)
    
    # Set tick label font sizes
    ax.tick_params(axis='both', which='major', labelsize=config.tick_fontsize)
    
    # Configure legend
    legend_settings = config.get_legend_settings("grouped_bar")
    legend = ax.legend(
        title=legend_settings.get("title", "Rarity"),
        bbox_to_anchor=legend_settings.get("bbox_to_anchor", (1.05, 1)),
        loc=legend_settings.get("loc", "upper left")
    )
    legend.get_title().set_fontsize(config.legend_fontsize)
    for text in legend.get_texts():
        text.set_fontsize(config.legend_fontsize)
    
    # Add data value annotations
    annotation_settings = config.get_annotation_settings("grouped_bar")
    for container in ax.containers:
        ax.bar_label(
            container, 
            fmt=annotation_settings.get("fmt", "%.0f"),
            padding=annotation_settings.get("padding", 3),
            fontsize=config.annotation_fontsize
        )
    
    # Add grid for better readability
    grid_settings = config.get_grid_settings("grouped_bar")
    if grid_settings.get("visible", True):
        ax.grid(
            True, 
            axis=grid_settings.get("axis", "y"),
            linestyle=grid_settings.get("linestyle", "--"), 
            alpha=grid_settings.get("alpha", 0.7)
        )
    
    if config.tight_layout:
        plt.tight_layout()
    return fig
