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
    plot_path_rarity_distribution,
)


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

        # Execute - remove config parameter
        result = plot_element_path_heatmap(df, "Patch (1.6)")

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

    # Patch seaborn catplot directly instead of plt
    with patch("seaborn.catplot") as mock_catplot:
        # Setup the mock return value
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_g = MagicMock()
        mock_g.figure = mock_fig
        mock_g.ax = mock_ax
        mock_catplot.return_value = mock_g

        # Execute the function
        result = plot_rarity_element_distribution(df, "Patch (1.6)")

        # Verify
        mock_catplot.assert_called_once()
        assert result is mock_fig


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

    # More comprehensive patching
    with (
        patch("hsrws.visual.plotting.plotting_timeline.plt") as mock_plt,
        patch("hsrws.visual.plotting.plotting_timeline.sns.lineplot") as mock_lineplot,
    ):
        # Setup matplotlib mock
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_plt.subplots.return_value = (mock_fig, mock_ax)

        # Execute
        result = plot_version_release_timeline(df, "Patch (1.6)")

        # Assert
        assert mock_plt.subplots.called
        assert mock_lineplot.called
        assert isinstance(result, MagicMock)  # Since we mocked Figure


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

    # Patch the seaborn lineplot directly
    with patch("seaborn.lineplot") as mock_lineplot:
        # Setup matplotlib mock
        with patch("matplotlib.pyplot.subplots") as mock_subplots:
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
            assert result is mock_fig


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

    # Patch seaborn catplot directly instead of plt
    with patch("seaborn.catplot") as mock_catplot:
        # Setup the mock return value
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_g = MagicMock()
        mock_g.figure = mock_fig
        mock_g.ax = mock_ax
        mock_catplot.return_value = mock_g

        # Execute the function
        result = plot_path_rarity_distribution(df, "Patch (1.6)")

        # Verify
        mock_catplot.assert_called_once()
        assert result is mock_fig
