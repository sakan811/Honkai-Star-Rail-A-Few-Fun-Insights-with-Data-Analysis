import pytest
from unittest.mock import Mock, call
from hsrws.sqlite_pipeline import create_views, get_element_char_count_by_ver, get_path_char_count_by_ver, \
    get_rarity_char_count_by_ver


def test_create_views_executes_all_queries():
    # Arrange
    mock_conn = Mock()

    # Act
    create_views(mock_conn)

    # Assert
    assert mock_conn.execute.call_count == 3
    mock_conn.execute.assert_has_calls([
        call(get_element_char_count_by_ver()),
        call(get_path_char_count_by_ver()),
        call(get_rarity_char_count_by_ver())
    ])


def test_create_views_handles_execution_error():
    # Arrange
    mock_conn = Mock()
    mock_conn.execute.side_effect = Exception("Database error")

    # Act & Assert
    with pytest.raises(Exception):
        create_views(mock_conn)