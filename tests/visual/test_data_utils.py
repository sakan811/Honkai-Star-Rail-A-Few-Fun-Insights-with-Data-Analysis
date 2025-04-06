"""Tests for the data utility functions."""

import pandas as pd
import pytest
from unittest.mock import patch, MagicMock, PropertyMock

from hsrws.visual.data_utils import (
    fetch_data_orm,
    get_latest_patch,
    get_element_path_heatmap_data,
    get_rarity_element_distribution_data,
    get_version_release_timeline_data,
    get_element_balance_evolution_data,
    get_path_rarity_distribution_data,
    get_element_colors,
    get_path_colors,
    get_rarity_colors,
)


@pytest.fixture
def mock_session():
    """Create a mock database session."""
    with patch("hsrws.visual.data_utils.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_execute = MagicMock()
        mock_session.execute.return_value = mock_execute
        mock_get_session.return_value.__enter__.return_value = mock_session
        yield mock_session


@pytest.fixture
def mock_execute_result():
    """Create a mock execution result."""
    mock_result = MagicMock()
    mock_result.all.return_value = [("1.6",)]

    # Properly mock column names as a property
    columns_property = PropertyMock()
    columns_property.keys.return_value = ["latest_version"]
    type(mock_result).columns = columns_property

    return mock_result


@pytest.mark.visual
def test_fetch_data_orm(mock_session):
    """Test fetch_data_orm function."""
    # Setup
    mock_result = MagicMock()
    mock_result.all.return_value = [("Fire", 5), ("Ice", 3)]
    mock_session.execute.return_value = mock_result

    # Create a mock stmt with column names
    mock_stmt = MagicMock()
    # Mock the columns property
    columns_property = PropertyMock()
    columns_property.keys.return_value = ["element", "count"]
    type(mock_stmt).columns = columns_property

    # Execute
    result = fetch_data_orm(mock_stmt)

    # Verify
    assert isinstance(result, pd.DataFrame)
    assert mock_session.execute.called
    assert len(result) == 2  # Two rows from our mock data


@pytest.mark.visual
def test_get_latest_patch(mock_session, mock_execute_result):
    """Test get_latest_patch function."""
    # Setup
    mock_session.execute.return_value.all.return_value = [(1.6,)]
    columns_property = PropertyMock()
    columns_property.keys.return_value = ["latest_version"]
    type(mock_session.execute.return_value).columns = columns_property

    # Execute
    with patch("hsrws.visual.data_utils.get_latest_patch_stmt"):
        result = get_latest_patch()

    # Verify
    assert result == "Patch (1.6)"


@pytest.mark.visual
def test_get_element_path_heatmap_data(mock_session, mock_execute_result):
    """Test get_element_path_heatmap_data function."""
    # Execute
    with patch("hsrws.visual.data_utils.get_element_path_heatmap_stmt"):
        with patch("hsrws.visual.data_utils.fetch_data_orm") as mock_fetch:
            mock_fetch.return_value = pd.DataFrame(
                {"Element": ["Fire"], "Path": ["Destruction"], "Count": [2]}
            )
            result = get_element_path_heatmap_data()

    # Verify
    assert isinstance(result, pd.DataFrame)
    mock_fetch.assert_called_once()


@pytest.mark.visual
def test_get_rarity_element_distribution_data(mock_session, mock_execute_result):
    """Test get_rarity_element_distribution_data function."""
    # Execute
    with patch("hsrws.visual.data_utils.get_rarity_element_distribution_stmt"):
        with patch("hsrws.visual.data_utils.fetch_data_orm") as mock_fetch:
            mock_fetch.return_value = pd.DataFrame(
                {"Rarity": ["5"], "Element": ["Fire"], "Count": [2]}
            )
            result = get_rarity_element_distribution_data()

    # Verify
    assert isinstance(result, pd.DataFrame)
    mock_fetch.assert_called_once()


@pytest.mark.visual
def test_get_version_release_timeline_data(mock_session, mock_execute_result):
    """Test get_version_release_timeline_data function."""
    # Execute
    with patch("hsrws.visual.data_utils.get_version_release_timeline_stmt"):
        with patch("hsrws.visual.data_utils.fetch_data_orm") as mock_fetch:
            mock_fetch.return_value = pd.DataFrame(
                {"Version": ["1.0"], "New_Characters": [5]}
            )
            result = get_version_release_timeline_data()

    # Verify
    assert isinstance(result, pd.DataFrame)
    mock_fetch.assert_called_once()


@pytest.mark.visual
def test_get_element_balance_evolution_data(mock_session, mock_execute_result):
    """Test get_element_balance_evolution_data function."""
    # Execute
    with patch("hsrws.visual.data_utils.get_version_element_evolution_stmt"):
        with patch("hsrws.visual.data_utils.fetch_data_orm") as mock_fetch:
            mock_fetch.return_value = pd.DataFrame(
                {"Version": ["1.0"], "Fire": [1], "Ice": [1]}
            )
            result = get_element_balance_evolution_data()

    # Verify
    assert isinstance(result, pd.DataFrame)
    mock_fetch.assert_called_once()


@pytest.mark.visual
def test_get_path_rarity_distribution_data(mock_session, mock_execute_result):
    """Test get_path_rarity_distribution_data function."""
    # Execute
    with patch("hsrws.visual.data_utils.get_path_rarity_distribution_stmt"):
        with patch("hsrws.visual.data_utils.fetch_data_orm") as mock_fetch:
            mock_fetch.return_value = pd.DataFrame(
                {"Path": ["Destruction"], "Rarity": ["5"], "Count": [2]}
            )
            result = get_path_rarity_distribution_data()

    # Verify
    assert isinstance(result, pd.DataFrame)
    mock_fetch.assert_called_once()


@pytest.mark.visual
def test_get_element_colors():
    """Test get_element_colors function."""
    result = get_element_colors()
    assert isinstance(result, dict)
    assert "Fire" in result
    assert result["Fire"] == "red"


@pytest.mark.visual
def test_get_path_colors():
    """Test get_path_colors function."""
    result = get_path_colors()
    assert isinstance(result, dict)
    assert "Destruction" in result
    assert result["Destruction"] == "grey"


@pytest.mark.visual
def test_get_rarity_colors():
    """Test get_rarity_colors function."""
    result = get_rarity_colors()
    assert isinstance(result, dict)
    assert "4" in result
    assert result["4"] == "gold"
