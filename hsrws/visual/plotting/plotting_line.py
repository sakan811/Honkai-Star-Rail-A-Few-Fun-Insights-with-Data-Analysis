"""Area chart plotting functions for HSR visualization."""

from typing import Optional
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
from loguru import logger
import seaborn as sns

from hsrws.visual.config.config_chart_settings import get_default_titles
from hsrws.visual.data_utils import get_element_colors


def plot_element_balance_evolution(
    df: pd.DataFrame, patch_version: Optional[str] = None
) -> Figure:
    """
    Plot elemental balance evolution across versions as an area chart.
    Shows the cumulative sum of characters for each element across versions.

    Args:
        df: DataFrame with Version, Element, and count columns from ORM query
             or already pivoted with Version and element columns.
        config: Optional chart configuration. If not provided, a default is used.
        patch_version: Optional patch version to include in title.

    Returns:
        Matplotlib figure object.
    """
    logger.debug("Plotting elemental balance evolution area chart...")

    # Get element-specific colors instead of using tab10
    element_colors = get_element_colors()
    
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x="Version", y="count", hue="Element", palette=element_colors, linewidth=2.5)

    ax.legend(title="Element")
    ax.set_xlabel("Version")
    ax.set_ylabel("Cumulative Character Count")
    
    titles = get_default_titles()
    title = titles["line"] + f" - {patch_version}"
    
    ax.set_title(title)
    
    return fig
