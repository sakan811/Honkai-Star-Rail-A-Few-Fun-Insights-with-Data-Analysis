"""Tests for visualization plotting functions."""

import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import matplotlib

matplotlib.use("Agg")  # Use non-interactive backend to avoid tkinter issues

from hsrws.visual.plotting import (
    plot_element_path_heatmap,
    plot_rarity_element_distribution,
    plot_version_release_timeline,
    plot_element_balance_evolution,
    plot_path_rarity_distribution,
)
from hsrws.visual.config import ChartConfig


@pytest.fixture
def mock_plt():
    """Mock matplotlib.pyplot for testing."""
    with patch("matplotlib.pyplot") as mock_plt:
        # Configure mock figure and axes
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_plt.subplots.return_value = (mock_fig, mock_ax)
        yield mock_plt


@pytest.fixture
def mock_sns():
    """Mock seaborn for testing."""
    with patch("seaborn.heatmap") as mock_heatmap:
        yield mock_heatmap


@pytest.fixture
def sample_config():
    """Return a sample ChartConfig for testing."""
    return ChartConfig()


@pytest.fixture
def element_path_data():
    """Return sample data for element-path heatmap."""
    return pd.DataFrame(
        {
            "Element": [
                "Fire",
                "Ice",
                "Lightning",
                "Wind",
                "Quantum",
                "Imaginary",
                "Physical",
            ],
            "Path": [
                "Destruction",
                "Hunt",
                "Erudition",
                "Harmony",
                "Nihility",
                "Preservation",
                "Abundance",
            ],
            "count": [2, 1, 1, 0, 1, 0, 1],
        }
    )


@pytest.fixture
def rarity_element_data():
    """Return sample data for rarity-element distribution."""
    return pd.DataFrame(
        {
            "Rarity": [5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4],
            "Element": [
                "Fire",
                "Ice",
                "Lightning",
                "Wind",
                "Quantum",
                "Imaginary",
                "Physical",
                "Fire",
                "Ice",
                "Lightning",
                "Wind",
                "Quantum",
                "Imaginary",
                "Physical",
            ],
            "count": [3, 2, 2, 2, 3, 2, 1, 2, 3, 3, 2, 1, 2, 2],
        }
    )


@pytest.fixture
def version_timeline_data():
    """Return sample data for version release timeline."""
    return pd.DataFrame(
        {
            "Version": ["1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "2.0"],
            "character_count": [5, 2, 2, 2, 2, 2, 3],
            "cumulative_count": [5, 7, 9, 11, 13, 15, 18],
        }
    )


@pytest.fixture
def element_evolution_data():
    """Return sample data for element balance evolution."""
    return pd.DataFrame(
        {
            "Version": ["1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "2.0"],
            "Fire": [1, 1, 1, 2, 3, 3, 4],
            "Ice": [1, 2, 2, 2, 3, 3, 4],
            "Lightning": [1, 1, 2, 2, 2, 3, 3],
            "Wind": [1, 1, 1, 2, 2, 2, 2],
            "Quantum": [0, 1, 1, 1, 1, 2, 2],
            "Imaginary": [0, 0, 1, 1, 1, 1, 2],
            "Physical": [1, 1, 1, 1, 1, 1, 1],
        }
    )


@pytest.fixture
def path_rarity_data():
    """Return sample data for path-rarity distribution."""
    return pd.DataFrame(
        {
            "Path": [
                "Destruction",
                "Hunt",
                "Erudition",
                "Harmony",
                "Nihility",
                "Preservation",
                "Abundance",
            ],
            "Rarity": [
                "5-star",
                "5-star",
                "5-star",
                "5-star",
                "5-star",
                "5-star",
                "5-star",
                "4-star",
                "4-star",
                "4-star",
                "4-star",
                "4-star",
                "4-star",
                "4-star",
            ],
            "count": [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        }
    )


@pytest.mark.visual
def test_plot_element_path_heatmap():
    """Test plotting element-path heatmap."""
    # Create test data properly aligned with what the function expects
    df = pd.DataFrame(
        [
            {"Element": "Fire", "Path": "Destruction", "count": 2},
            {"Element": "Ice", "Path": "Hunt", "count": 1},
            {"Element": "Lightning", "Path": "Erudition", "count": 1},
        ]
    )

    config = ChartConfig()

    # Patch both Pandas pivot and seaborn heatmap
    with (
        patch("pandas.DataFrame.pivot") as mock_pivot,
        patch("matplotlib.pyplot.figure") as mock_figure,
        patch("seaborn.heatmap") as mock_heatmap,
    ):
        # Create mock objects for figure and axes
        mock_fig = MagicMock()
        mock_ax = MagicMock()

        # Setup pivot mock
        mock_pivot_result = pd.DataFrame()
        mock_pivot.return_value = mock_pivot_result

        # Setup figure mock
        mock_figure.return_value = mock_fig
        mock_fig.add_subplot.return_value = mock_ax

        # Execute
        result = plot_element_path_heatmap(df, config, "Patch (1.6)")

        # Verify basics
        assert mock_pivot.called
        assert mock_heatmap.called
        assert result is not None


@pytest.mark.visual
def test_plot_rarity_element_distribution():
    """Test plotting rarity-element distribution."""
    # Create test data
    df = pd.DataFrame(
        [
            {"Rarity": 5, "Element": "Fire", "count": 3},
            {"Rarity": 5, "Element": "Ice", "count": 2},
            {"Rarity": 4, "Element": "Fire", "count": 2},
            {"Rarity": 4, "Element": "Ice", "count": 3},
        ]
    )

    config = ChartConfig()

    # Skip the actual plotting by patching critical methods
    with (
        patch("hsrws.visual.plotting.plotting_bar.plt") as mock_plt,
        patch("pandas.DataFrame.pivot_table") as mock_pivot_table,
    ):
        # Setup pivot mock to return a dataframe
        pivot_df = pd.DataFrame({"Fire": [3, 2], "Ice": [2, 3]})
        pivot_df.index = [5, 4]  # Rarity values
        mock_pivot_table.return_value = pivot_df

        # Setup matplotlib figure mock
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_plt.subplots.return_value = (mock_fig, mock_ax)

        # Add plot method to pivot_df
        pivot_df.plot = MagicMock()

        # Execute the function
        result = plot_rarity_element_distribution(df, config, "Patch (1.6)")

        # Verify pivot_table was called and a figure is returned
        assert mock_pivot_table.called
        assert result is not None


@pytest.mark.visual
def test_plot_version_release_timeline():
    """Test plotting version release timeline."""
    # Create test data
    df = pd.DataFrame(
        [
            {"Version": "1.0", "character_count": 5, "cumulative_count": 5},
            {"Version": "1.1", "character_count": 2, "cumulative_count": 7},
        ]
    )

    config = ChartConfig()

    with patch("hsrws.visual.plotting.plotting_timeline.plt") as mock_plt:
        # Setup matplotlib mock
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_plt.subplots.return_value = (mock_fig, mock_ax)

        # Execute
        result = plot_version_release_timeline(df, config, "Patch (1.6)")

        # Verify
        assert mock_plt.subplots.called
        assert result is not None


@pytest.mark.visual
def test_plot_element_balance_evolution():
    """Test plotting element balance evolution."""
    # Create test data
    df = pd.DataFrame(
        [
            {"Version": "1.0", "Fire": 1, "Ice": 1},
            {"Version": "1.1", "Fire": 2, "Ice": 2},
        ]
    )

    config = ChartConfig()

    with (
        patch("hsrws.visual.plotting.plotting_area.plt") as mock_plt,
        patch("pandas.DataFrame.set_index") as mock_set_index,
    ):
        # Setup set_index mock to return a dataframe with plot method
        indexed_df = pd.DataFrame({"Fire": [1, 2], "Ice": [1, 2]})
        indexed_df.index = ["1.0", "1.1"]  # Version values
        mock_set_index.return_value = indexed_df

        # Setup matplotlib mock
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_plt.subplots.return_value = (mock_fig, mock_ax)

        # Add plot method to indexed_df
        indexed_df.plot = MagicMock()

        # Execute
        result = plot_element_balance_evolution(df, config, "Patch (1.6)")

        # Verify
        assert mock_set_index.called
        assert mock_plt.subplots.called
        assert result is not None


@pytest.mark.visual
def test_plot_path_rarity_distribution():
    """Test plotting path-rarity distribution."""
    # Create test data
    df = pd.DataFrame(
        [
            {"Path": "Destruction", "Rarity": "5-star", "count": 2},
            {"Path": "Destruction", "Rarity": "4-star", "count": 1},
            {"Path": "Hunt", "Rarity": "5-star", "count": 1},
            {"Path": "Hunt", "Rarity": "4-star", "count": 2},
        ]
    )

    config = ChartConfig()

    with (
        patch("hsrws.visual.plotting.plotting_bar.plt") as mock_plt,
        patch("pandas.DataFrame.pivot_table") as mock_pivot_table,
    ):
        # Setup pivot mock to return a dataframe with plot method
        pivot_df = pd.DataFrame({"5-star": [2, 1], "4-star": [1, 2]})
        pivot_df.index = ["Destruction", "Hunt"]  # Path values
        mock_pivot_table.return_value = pivot_df

        # Setup matplotlib mock
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_plt.subplots.return_value = (mock_fig, mock_ax)

        # Add plot method to pivot_df
        pivot_df.plot = MagicMock()

        # Execute
        result = plot_path_rarity_distribution(df, config, "Patch (1.6)")

        # Verify
        assert mock_pivot_table.called
        assert mock_plt.subplots.called
        assert result is not None
