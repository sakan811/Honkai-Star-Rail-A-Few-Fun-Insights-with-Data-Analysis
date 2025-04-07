"""Tests for character version addition functionality."""

import pandas as pd
from unittest.mock import patch
from hsrws.data.transformer import add_char_version


def test_add_char_version():
    """Test adding version information to characters based on their release version."""
    # Create test dataframe
    df = pd.DataFrame(
        {"Character": ["Harry Potter", "Hermione Granger", "Spider-Man", "Iron Man"]}
    )

    # Mock version dictionary
    mock_version_dict = {2.0: ["Spider-Man", "Iron Man"]}

    # Apply the version mapping
    with patch(
        "hsrws.data.transformer.get_version_dict", return_value=mock_version_dict
    ):
        # Call the actual function instead of reimplementing it
        add_char_version(df)

    # Verify results
    assert "Version" in df.columns
    assert df.loc[df["Character"] == "Harry Potter", "Version"].iloc[0] == 1.0
    assert df.loc[df["Character"] == "Hermione Granger", "Version"].iloc[0] == 1.0
    assert df.loc[df["Character"] == "Spider-Man", "Version"].iloc[0] == 2.0
    assert df.loc[df["Character"] == "Iron Man", "Version"].iloc[0] == 2.0
