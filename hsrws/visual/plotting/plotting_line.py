"""Area chart plotting functions for HSR visualization."""

from typing import Optional
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
from loguru import logger
import seaborn as sns
from unittest.mock import patch, MagicMock
import pytest

from hsrws.visual.data_utils import get_element_colors, get_path_colors


def plot_element_balance_evolution(
    df: pd.DataFrame, patch_version: Optional[str] = None
) -> Figure:
    """
    Plot elemental balance evolution across versions as an area chart.
    Shows the cumulative sum of characters for each element across versions.

    Args:
        df: DataFrame with Version, Element, and count columns from ORM query
             or already pivoted with Version and element columns.
        patch_version: Optional patch version to include in title.

    Returns:
        Matplotlib figure object.
    """
    logger.debug("Plotting elemental balance evolution area chart...")

    # Get element-specific colors instead of using tab10
    element_colors = get_element_colors()

    fig, ax = plt.subplots()
    sns.lineplot(
        data=df,
        x="Version",
        y="count",
        hue="Element",
        palette=element_colors,
        linewidth=2.5,
    )

    # Place legend outside the plot area to the right
    ax.legend(title="Element", bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.set_xlabel("Version")
    ax.set_ylabel("Cumulative Character Count")

    title = "Honkai: Star Rail Elemental Balance Evolution Across Versions"
    if patch_version:
        title += f" - {patch_version}"

    ax.set_title(title)

    # Adjust layout to make room for the legend
    plt.tight_layout()

    return fig


def plot_path_balance_evolution(
    df: pd.DataFrame, patch_version: Optional[str] = None
) -> Figure:
    """
    Plot path balance evolution across versions as a line chart.
    Shows the cumulative sum of characters for each path across versions.

    Args:
        df: DataFrame with Version, Path, and count columns from ORM query
             or already pivoted with Version and path columns.
        patch_version: Optional patch version to include in title.

    Returns:
        Matplotlib figure object.
    """
    logger.debug("Plotting path balance evolution line chart...")

    # Get path-specific colors
    path_colors = get_path_colors()

    fig, ax = plt.subplots()
    sns.lineplot(
        data=df,
        x="Version",
        y="count",
        hue="Path",
        palette=path_colors,
        linewidth=2.5,
    )

    # Place legend outside the plot area to the right
    ax.legend(title="Path", bbox_to_anchor=(1.05, 1), loc="upper left")
    ax.set_xlabel("Version")
    ax.set_ylabel("Cumulative Character Count")

    title = "Honkai: Star Rail Path Balance Evolution Across Versions"
    if patch_version:
        title += f" - {patch_version}"

    ax.set_title(title)

    # Adjust layout to make room for the legend
    plt.tight_layout()

    return fig


@pytest.mark.visual
def test_plot_path_balance_evolution():
    """Test plotting path balance evolution."""
    # Create test data with the correct columns
    df = pd.DataFrame(
        [
            {"Version": "1.0", "Path": "Hunt", "count": 1},
            {"Version": "1.0", "Path": "Harmony", "count": 1},
            {"Version": "1.1", "Path": "Hunt", "count": 2},
            {"Version": "1.1", "Path": "Harmony", "count": 2},
        ]
    )

    # Patch the seaborn lineplot and pyplot
    with patch("seaborn.lineplot") as mock_lineplot:
        # Setup matplotlib mock
        with (
            patch("matplotlib.pyplot.subplots") as mock_subplots,
            patch("matplotlib.pyplot.tight_layout") as mock_tight_layout,
        ):
            mock_fig = MagicMock()
            mock_ax = MagicMock()
            mock_subplots.return_value = (mock_fig, mock_ax)

            # Execute the function
            from hsrws.visual.plotting.plotting_line import plot_path_balance_evolution

            result = plot_path_balance_evolution(df, "Patch (1.6)")

            # Verify
            mock_lineplot.assert_called_once()
            # Verify legend placement
            mock_ax.legend.assert_called_once_with(
                title="Path", bbox_to_anchor=(1.05, 1), loc="upper left"
            )
            # Verify tight_layout is called
            mock_tight_layout.assert_called_once()
            assert result is mock_fig


@pytest.mark.visual
def test_plot_element_balance_evolution():
    """Test plotting element balance evolution."""
    # Create test data with the correct columns
    df = pd.DataFrame(
        [
            {"Version": "1.0", "Element": "Fire", "count": 1},
            {"Version": "1.0", "Element": "Ice", "count": 1},
            {"Version": "1.1", "Element": "Fire", "count": 2},
            {"Version": "1.1", "Element": "Ice", "count": 2},
        ]
    )

    # Patch the seaborn lineplot and pyplot
    with patch("seaborn.lineplot") as mock_lineplot:
        # Setup matplotlib mock
        with (
            patch("matplotlib.pyplot.subplots") as mock_subplots,
            patch("matplotlib.pyplot.tight_layout") as mock_tight_layout,
        ):
            mock_fig = MagicMock()
            mock_ax = MagicMock()
            mock_subplots.return_value = (mock_fig, mock_ax)

            # Execute the function
            from hsrws.visual.plotting.plotting_line import (
                plot_element_balance_evolution,
            )

            result = plot_element_balance_evolution(df, "Patch (1.6)")

            # Verify
            mock_lineplot.assert_called_once()
            # Verify legend placement
            mock_ax.legend.assert_called_once_with(
                title="Element", bbox_to_anchor=(1.05, 1), loc="upper left"
            )
            # Verify tight_layout is called
            mock_tight_layout.assert_called_once()
            assert result is mock_fig
