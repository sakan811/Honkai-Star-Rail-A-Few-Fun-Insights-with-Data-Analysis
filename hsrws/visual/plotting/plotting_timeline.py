"""Timeline plotting functions for HSR visualization."""

from typing import Optional
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
from loguru import logger
import seaborn as sns

from hsrws.visual.config import ChartConfig
from hsrws.visual.config.config_chart_settings import get_default_titles


def plot_version_release_timeline(
    df: pd.DataFrame, patch_version: Optional[str] = None
) -> Figure:
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

    fig, ax = plt.subplots()
    
    # Primary line for new characters per version
    sns.lineplot(data=df, x="Version", y="character_count", 
                marker="o", markersize=8, linewidth=2.5)

    # Add data annotations
    for x, y in zip(df["Version"], df["character_count"]):
        ax.annotate(
            f"{y:.0f}",
            (x, y),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontweight="bold",
        )

    # Calculate cumulative sum for additional information
    df["cumulative_count"] = df["character_count"].cumsum()
    
    # Secondary line for cumulative count
    ax2 = ax.twinx()
    sns.lineplot(data=df, x="Version", y="cumulative_count", 
                ax=ax2, color="darkred", linestyle="--", 
                marker="s", markersize=6, alpha=0.7)
                
    ax.set_xlabel("Version")
    ax.set_ylabel("New Characters Per Version")
    ax2.set_ylabel("Cumulative Character Count", color="darkred")
    
    # Show all versions as ticks but only label some to avoid crowding
    ax.set_xticks(df["Version"])
    
    # Show labels for approximately 1/3 of the versions
    n_versions = len(df["Version"])
    step = max(1, n_versions // 3)
    labels = [str(v) if i % step == 0 else "" for i, v in enumerate(df["Version"])]
    ax.set_xticklabels(labels)
    
    titles = get_default_titles()
    title = titles["timeline"]  + f" - {patch_version}"
    
    ax.set_title(title)
    
    return fig
