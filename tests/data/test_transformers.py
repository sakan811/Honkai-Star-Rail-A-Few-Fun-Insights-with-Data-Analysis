"""Test module for the data transformers."""

import pandas as pd
from unittest.mock import patch
from hsrws.data.transformer import (
    add_char_version,
    clean_path_name,
    transform_char_name,
)


def test_transform_char_name():
    """Test that character names are properly transformed."""
    test_cases = [
        ("Firefly", "firefly"),
        ("March 7th", "march-7th"),
        ("Jingliu (The Hunt)", "jingliu-(the-hunt)"),
        ("Kafka (Nihility)", "kafka-(nihility)"),
        ("Blade (Destruction)", "blade-(destruction)"),
    ]

    for input_name, expected_output in test_cases:
        assert transform_char_name(input_name) == expected_output


def test_clean_path_name():
    """Test that path names are properly cleaned."""
    test_cases = [
        ("The Hunt", "Hunt"),
        ("Nihility", "Nihility"),
        ("Destruction", "Destruction"),
        ("The Abundance", "Abundance"),
        ("Preservation", "Preservation"),
        ("The Erudition", "Erudition"),
        ("Harmony", "Harmony"),
    ]

    for input_path, expected_output in test_cases:
        assert clean_path_name(input_path) == expected_output


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
        add_char_version(df)

    # Verify results
    assert "Version" in df.columns
    assert df.loc[df["Character"] == "Harry Potter", "Version"].iloc[0] == 1.0
    assert df.loc[df["Character"] == "Hermione Granger", "Version"].iloc[0] == 1.0
    assert df.loc[df["Character"] == "Spider-Man", "Version"].iloc[0] == 2.0
    assert df.loc[df["Character"] == "Iron Man", "Version"].iloc[0] == 2.0
