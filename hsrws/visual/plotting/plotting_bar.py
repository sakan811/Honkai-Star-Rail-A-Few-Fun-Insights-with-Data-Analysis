"""Bar chart plotting functions for HSR visualization."""

from typing import Optional
from matplotlib.figure import Figure
import pandas as pd
import seaborn as sns
from loguru import logger

from hsrws.visual.config.config_chart_settings import get_default_titles
from hsrws.visual.data_utils import get_rarity_colors


def plot_rarity_element_distribution(
    df: pd.DataFrame, patch_version: Optional[str] = None
) -> Figure:
    """
    Plot character element distribution with rarity breakdown as a grouped bar chart.

    Args:
        df: DataFrame containing rarity, element, and count columns.
        patch_version: Optional patch version to include in title.

    Returns:
        Matplotlib figure object.
    """
    logger.debug("Plotting element-rarity grouped bar chart...")

    # Create catplot with seaborn (include legend by default)
    g = sns.catplot(
        data=df,
        x="Element",
        y="count",
        hue="Rarity",
        kind="bar",
        palette=get_rarity_colors(),
        legend_out=False,  # Keep legend inside the plot
    )
    
    fig = g.figure
    ax = g.ax
    
    ax.legend(title="Rarity")
    ax.set_xlabel("Element")
    ax.set_ylabel("Character Count")
    
    # Set up chart basics
    titles = get_default_titles() 
    title = titles.get("grouped_bar", "Honkai: Star Rail Character Path Distribution by Rarity")
    
    if patch_version:
        title += f" - {patch_version}"
        
    ax.set_title(title)
    
    return fig


def plot_path_rarity_distribution(
    df: pd.DataFrame, patch_version: Optional[str] = None
) -> Figure:
    """
    Plot character path-rarity distribution as a grouped bar chart.

    Args:
        df: DataFrame containing path, rarity, and count columns.
        patch_version: Optional patch version to include in title.

    Returns:
        Matplotlib figure object.
    """
    logger.debug("Plotting path-rarity grouped bar chart...")
    
    # Create catplot with seaborn (include legend by default)
    g = sns.catplot(
        data=df,
        x="Path",
        y="count",
        hue="Rarity",
        kind="bar",
        palette=get_rarity_colors(),
        legend_out=False,  # Keep legend inside the plot
    )
    
    fig = g.figure
    ax = g.ax
        
    title = "Honkai: Star Rail Character Path Distribution by Rarity" + f" - {patch_version}"
    
    ax.set_title(title)
    ax.set_xlabel("Path")
    ax.set_ylabel("Character Count")
    ax.legend(title="Rarity")
    
    return fig
