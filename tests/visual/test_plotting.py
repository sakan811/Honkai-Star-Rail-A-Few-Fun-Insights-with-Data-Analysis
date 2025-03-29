"""Tests for visualization plotting functions."""

import pytest
from unittest.mock import patch, MagicMock

from hsrws.visual.plotting import (
    plot_character_stats,
    plot_element_distribution,
    plot_path_distribution,
)


@pytest.fixture
def mock_plt():
    """Mock matplotlib.pyplot for testing."""
    with patch("hsrws.visual.plotting.plt") as mock_plt:
        # Configure mock figure and axes
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_plt.subplots.return_value = (mock_fig, mock_ax)
        yield mock_plt


@pytest.mark.visual
def test_plot_character_stats(sample_character_df, mock_plt):
    """Test plotting character stats."""
    # Call the function under test
    plot_character_stats(sample_character_df, "ATK Lvl 80")

    # Verify plot was created
    mock_plt.subplots.assert_called_once()
    mock_ax = mock_plt.subplots.return_value[1]

    # Check that bar plot was called
    mock_ax.bar.assert_called_once()

    # Check that labels were set
    mock_ax.set_xlabel.assert_called_once()
    mock_ax.set_ylabel.assert_called_once()
    mock_ax.set_title.assert_called_once()

    # Check that figure was shown or saved
    assert mock_plt.tight_layout.called
    assert mock_plt.show.called or mock_plt.savefig.called


@pytest.mark.visual
def test_plot_element_distribution(sample_character_df, mock_plt):
    """Test plotting element distribution."""
    # Call the function under test
    plot_element_distribution(sample_character_df)

    # Verify plot was created
    mock_plt.subplots.assert_called_once()
    mock_ax = mock_plt.subplots.return_value[1]

    # Check that pie chart was called
    mock_ax.pie.assert_called_once()

    # Check that title was set
    mock_ax.set_title.assert_called_once()

    # Check that figure was shown or saved
    assert mock_plt.tight_layout.called
    assert mock_plt.show.called or mock_plt.savefig.called


@pytest.mark.visual
def test_plot_path_distribution(sample_character_df, mock_plt):
    """Test plotting path distribution."""
    # Call the function under test
    plot_path_distribution(sample_character_df)

    # Verify plot was created
    mock_plt.subplots.assert_called_once()
    mock_ax = mock_plt.subplots.return_value[1]

    # Check that countplot or another plot function was called
    assert mock_ax.pie.called or mock_ax.bar.called

    # Check that title was set
    mock_ax.set_title.assert_called_once()

    # Check that figure was shown or saved
    assert mock_plt.tight_layout.called
    assert mock_plt.show.called or mock_plt.savefig.called
