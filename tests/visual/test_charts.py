"""Tests for chart creation functionality."""

import pytest
from unittest.mock import patch, MagicMock

from hsrws.visual.charts import create_advanced_charts, save_figure


@pytest.fixture
def mock_plt():
    """Mock matplotlib.pyplot for testing."""
    with patch("hsrws.visual.charts.plt") as mock_plt:
        # Configure mock figure
        mock_fig = MagicMock()
        mock_plt.subplots.return_value = (mock_fig, MagicMock())
        yield mock_plt


@pytest.fixture
def mock_sns():
    """Mock seaborn for testing."""
    with patch("hsrws.visual.charts.sns") as mock_sns:
        yield mock_sns


@pytest.fixture
def mock_data_utils():
    """Mock all data_utils functions."""
    with (
        patch("hsrws.visual.charts.get_latest_patch") as mock_latest_patch,
        patch("hsrws.visual.charts.get_element_path_heatmap_data") as mock_heatmap_data,
        patch(
            "hsrws.visual.charts.get_rarity_element_distribution_data"
        ) as mock_rarity_data,
        patch(
            "hsrws.visual.charts.get_version_release_timeline_data"
        ) as mock_timeline_data,
        patch(
            "hsrws.visual.charts.get_element_balance_evolution_data"
        ) as mock_evolution_data,
        patch(
            "hsrws.visual.charts.get_path_rarity_distribution_data"
        ) as mock_path_data,
    ):
        # Configure mock returns
        import pandas as pd

        mock_latest_patch.return_value = "Patch (1.6)"
        mock_heatmap_data.return_value = pd.DataFrame(
            {"Element": ["Fire"], "Destruction": [2], "Hunt": [1]}
        )
        mock_rarity_data.return_value = pd.DataFrame(
            {"Rarity": [5], "Element": ["Fire"], "Count": [2]}
        )
        mock_timeline_data.return_value = pd.DataFrame(
            {"Version": ["1.0"], "New_Characters": [5], "Cumulative_Total": [5]}
        )
        mock_evolution_data.return_value = pd.DataFrame(
            {"Version": ["1.0"], "Fire": [1], "Ice": [1]}
        )
        mock_path_data.return_value = pd.DataFrame(
            {"Path": ["Hunt"], "5-star": [2], "4-star": [1]}
        )

        yield {
            "latest_patch": mock_latest_patch,
            "heatmap_data": mock_heatmap_data,
            "rarity_data": mock_rarity_data,
            "timeline_data": mock_timeline_data,
            "evolution_data": mock_evolution_data,
            "path_data": mock_path_data,
        }


@pytest.fixture
def mock_plotting():
    """Mock all plotting functions."""
    with (
        patch("hsrws.visual.charts.plot_element_path_heatmap") as mock_heatmap_plot,
        patch(
            "hsrws.visual.charts.plot_rarity_element_distribution"
        ) as mock_rarity_plot,
        patch(
            "hsrws.visual.charts.plot_version_release_timeline"
        ) as mock_timeline_plot,
        patch(
            "hsrws.visual.charts.plot_element_balance_evolution"
        ) as mock_evolution_plot,
        patch("hsrws.visual.charts.plot_path_rarity_distribution") as mock_path_plot,
    ):
        # Configure mock returns
        mock_fig = MagicMock()
        mock_heatmap_plot.return_value = mock_fig
        mock_rarity_plot.return_value = mock_fig
        mock_timeline_plot.return_value = mock_fig
        mock_evolution_plot.return_value = mock_fig
        mock_path_plot.return_value = mock_fig

        yield {
            "heatmap_plot": mock_heatmap_plot,
            "rarity_plot": mock_rarity_plot,
            "timeline_plot": mock_timeline_plot,
            "evolution_plot": mock_evolution_plot,
            "path_plot": mock_path_plot,
        }


@pytest.mark.visual
def test_save_figure(mock_plt):
    """Test saving a figure to file."""
    # Setup
    mock_fig = MagicMock()
    dpi = 300

    # Create a mock image object with the necessary properties
    mock_image = MagicMock()
    mock_image.size = (100, 150)  # Width and height attributes

    # Create a mock square image
    mock_square_img = MagicMock()

    with (
        patch("os.makedirs") as mock_makedirs,
        patch("PIL.Image.open", return_value=mock_image),
        patch("PIL.Image.new", return_value=mock_square_img),
    ):
        # Execute
        save_figure(mock_fig, "test_figure.png", dpi)

        # Verify
        mock_makedirs.assert_called_once()
        mock_fig.savefig.assert_called_once()
        mock_plt.close.assert_called_once_with(mock_fig)
        mock_square_img.paste.assert_called_once()
        mock_square_img.save.assert_called_once()


@pytest.mark.visual
def test_create_advanced_charts(mock_plt, mock_sns, mock_data_utils, mock_plotting):
    """Test creating all advanced charts."""
    # Setup
    with (
        patch("os.makedirs"),
        patch("hsrws.visual.charts.save_figure") as mock_save_figure,
    ):
        # Execute
        create_advanced_charts()

        # Verify all data functions were called
        for mock_func in mock_data_utils.values():
            assert mock_func.called

        # Verify all plotting functions were called
        for mock_plot in mock_plotting.values():
            assert mock_plot.called

        # Verify figures were saved
        assert mock_save_figure.call_count == 5
