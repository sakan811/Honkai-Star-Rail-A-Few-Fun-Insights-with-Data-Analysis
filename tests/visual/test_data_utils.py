"""Tests for data utility functions."""

import pytest
from unittest.mock import patch, MagicMock, PropertyMock
import pandas as pd

from hsrws.visual.data_utils import (
    fetch_data_orm,
    fetch_view_data,
    get_latest_patch,
    get_element_path_heatmap_data,
    get_rarity_element_distribution_data,
    get_version_release_timeline_data,
    get_element_balance_evolution_data,
    get_path_rarity_distribution_data,
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
def test_fetch_data_orm():
    """Test fetch_data_orm function."""
    # Setup
    mock_stmt = MagicMock()
    mock_result = MagicMock()
    mock_result.all.return_value = [("1.6",)]

    # Use dict-style mock for columns attribute with a mock keys method
    columns_mock = MagicMock()
    keys_mock = MagicMock()
    keys_mock.return_value = ["latest_version"]
    columns_mock.keys = keys_mock
    mock_stmt.columns = columns_mock

    with patch("hsrws.visual.data_utils.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Execute
        result = fetch_data_orm(mock_stmt)

    # Verify
    assert isinstance(result, pd.DataFrame)


@pytest.mark.visual
def test_fetch_view_data():
    """Test fetch_view_data function."""
    # Setup
    mock_mapping1 = MagicMock()
    mock_mapping1._mapping = {"element": "Fire", "count": 5}
    mock_mapping2 = MagicMock()
    mock_mapping2._mapping = {"element": "Ice", "count": 3}

    # Create a proper mock result with returns_rows attribute
    mock_result = MagicMock()
    type(mock_result).returns_rows = PropertyMock(return_value=True)
    mock_result.__iter__.return_value = [mock_mapping1, mock_mapping2]

    with (
        patch("hsrws.visual.data_utils.get_session") as mock_get_session,
        patch("hsrws.visual.data_utils.text") as mock_text,
    ):
        mock_session = MagicMock()
        mock_session.execute.return_value = mock_result
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Execute
        result = fetch_view_data("TestView")

    # Verify
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2  # Two rows from our mock data


@pytest.mark.visual
def test_get_latest_patch():
    """Test get_latest_patch function."""
    mock_df = pd.DataFrame({"latest_version": ["1.6"]})

    with (
        patch("hsrws.visual.data_utils.get_latest_patch_stmt") as mock_stmt,
        patch("hsrws.visual.data_utils.fetch_data_orm") as mock_fetch,
    ):
        mock_fetch.return_value = mock_df
        result = get_latest_patch()

    # Verify
    assert result == "Patch (1.6)"


@pytest.mark.visual
def test_get_element_path_heatmap_data(mock_session, mock_execute_result):
    """Test get_element_path_heatmap_data function."""
    # Execute
    with patch("hsrws.visual.data_utils.get_element_path_heatmap_stmt") as mock_stmt:
        with patch("hsrws.visual.data_utils.fetch_data_orm") as mock_fetch:
            mock_fetch.return_value = pd.DataFrame(
                {"Element": ["Fire"], "Path": ["Hunt"], "Count": [2]}
            )
            result = get_element_path_heatmap_data()

    # Verify
    assert isinstance(result, pd.DataFrame)
    mock_fetch.assert_called_once()


@pytest.mark.visual
def test_get_rarity_element_distribution_data(mock_session, mock_execute_result):
    """Test get_rarity_element_distribution_data function."""
    # Execute
    with patch(
        "hsrws.visual.data_utils.get_rarity_element_distribution_stmt"
    ) as mock_stmt:
        with patch("hsrws.visual.data_utils.fetch_data_orm") as mock_fetch:
            mock_fetch.return_value = pd.DataFrame(
                {"Rarity": [5], "Element": ["Fire"], "Count": [2]}
            )
            result = get_rarity_element_distribution_data()

    # Verify
    assert isinstance(result, pd.DataFrame)
    mock_fetch.assert_called_once()


@pytest.mark.visual
def test_get_version_release_timeline_data(mock_session, mock_execute_result):
    """Test get_version_release_timeline_data function."""
    # Execute
    with patch(
        "hsrws.visual.data_utils.get_version_release_timeline_stmt"
    ) as mock_stmt:
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
    with patch("hsrws.visual.data_utils.fetch_view_data") as mock_fetch_view:
        mock_fetch_view.return_value = pd.DataFrame(
            {"Version": ["1.0"], "Fire": [1], "Ice": [1]}
        )
        result = get_element_balance_evolution_data()

    # Verify
    assert isinstance(result, pd.DataFrame)
    mock_fetch_view.assert_called_once_with("ElementCharacterCountByVersion")


@pytest.mark.visual
def test_get_element_balance_evolution_data_fallback(mock_session, mock_execute_result):
    """Test get_element_balance_evolution_data function with fallback."""
    # Execute
    with patch("hsrws.visual.data_utils.fetch_view_data") as mock_fetch_view:
        mock_fetch_view.side_effect = Exception("View not found")
        with patch(
            "hsrws.visual.data_utils.get_version_element_evolution_stmt"
        ) as mock_stmt:
            with patch("hsrws.visual.data_utils.fetch_data_orm") as mock_fetch:
                mock_fetch.return_value = pd.DataFrame(
                    {"Version": ["1.0"], "Fire": [1], "Ice": [1]}
                )
                result = get_element_balance_evolution_data()

    # Verify
    assert isinstance(result, pd.DataFrame)
    mock_fetch_view.assert_called_once()
    mock_fetch.assert_called_once()


@pytest.mark.visual
def test_get_path_rarity_distribution_data(mock_session, mock_execute_result):
    """Test get_path_rarity_distribution_data function."""
    # Execute
    with patch(
        "hsrws.visual.data_utils.get_path_rarity_distribution_stmt"
    ) as mock_stmt:
        with patch("hsrws.visual.data_utils.fetch_data_orm") as mock_fetch:
            mock_fetch.return_value = pd.DataFrame(
                {"Path": ["Hunt"], "5-star": [2], "4-star": [1]}
            )
            result = get_path_rarity_distribution_data()

    # Verify
    assert isinstance(result, pd.DataFrame)
    mock_fetch.assert_called_once()
