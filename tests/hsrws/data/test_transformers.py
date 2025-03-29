"""Tests for the data transformation functions."""

import pandas as pd
from unittest.mock import patch

from hsrws.data.transformers import add_version, clean_path_name, transform_char_name


def test_add_version():
    """Test adding version information to characters."""
    # Create test dataframe
    df = pd.DataFrame({"Character": ["Kafka", "Blade", "Dr. Ratio", "Robin"]})

    # Mock version dictionary
    mock_version_dict = {1.0: ["Kafka", "Blade"], 2.0: ["Dr. Ratio", "Robin"]}

    # Patch the version dictionary function
    with patch(
        "hsrws.data.transformers.get_version_dict", return_value=mock_version_dict
    ):
        # Call the function under test
        result_df = add_version(df)

    # Verify results
    assert "Version" in result_df.columns
    assert result_df.loc[result_df["Character"] == "Kafka", "Version"].iloc[0] == 1.0
    assert result_df.loc[result_df["Character"] == "Blade", "Version"].iloc[0] == 1.0
    assert (
        result_df.loc[result_df["Character"] == "Dr. Ratio", "Version"].iloc[0] == 2.0
    )
    assert result_df.loc[result_df["Character"] == "Robin", "Version"].iloc[0] == 2.0


def test_clean_path_name():
    """Test cleaning path names in the dataframe."""
    # Create test dataframe
    df = pd.DataFrame(
        {"Path": ["The Hunt", "the abundance", "THE HARMONY", "Destruction"]}
    )

    # Call the function under test
    result_df = clean_path_name(df)

    # Verify results
    assert all(result_df["Path"] == ["Hunt", "Abundance", "Harmony", "Destruction"])


def test_transform_char_name():
    """Test transforming character names in the dataframe."""
    # Create test dataframe
    df = pd.DataFrame(
        {
            "Character": [
                "Trailblazer (Fire)",
                "Trailblazer (Physical)",
                "Dr. Ratio",
                "Kafka",
            ]
        }
    )

    # Call the function under test
    result_df = transform_char_name(df)

    # Verify results
    assert "Character" in result_df.columns
    assert "Trailblazer Fire" in result_df["Character"].values
    assert "Trailblazer Physical" in result_df["Character"].values
    assert "Dr. Ratio" in result_df["Character"].values
    assert "Kafka" in result_df["Character"].values
