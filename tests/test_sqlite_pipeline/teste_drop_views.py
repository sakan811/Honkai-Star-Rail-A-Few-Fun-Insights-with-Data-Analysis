import pytest
from unittest.mock import Mock, call
from hsrws.sqlite_pipeline import drop_views


def test_drop_views_executes_all_queries():
    # Arrange
    mock_conn = Mock()

    # Act
    drop_views(mock_conn)

    # Assert
    assert mock_conn.execute.call_count == 3
    mock_conn.execute.assert_has_calls([
        call("DROP VIEW IF EXISTS ElementCharacterCountByVersion"),
        call("DROP VIEW IF EXISTS PathCharacterCountByVersion"),
        call("DROP VIEW IF EXISTS RarityCharacterCountByVersion")
    ])


def test_drop_views_handles_execution_error():
    # Arrange
    mock_conn = Mock()
    mock_conn.execute.side_effect = Exception("Database error")

    # Act & Assert
    with pytest.raises(Exception):
        drop_views(mock_conn)