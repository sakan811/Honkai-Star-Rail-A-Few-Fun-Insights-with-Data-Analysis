"""Tests for the main scraper entrypoint functionality."""

import pytest
import pandas as pd
from unittest.mock import patch

from main import main


@pytest.mark.asyncio
async def test_main_scraper_integration():
    """Test the main function that runs the scraper."""
    # Use the fixture for sample data
    mock_df = pd.DataFrame(
        {
            "Character": ["Test Character"],
            "Path": ["Test Path"],
            "Element": ["Test Element"],
            "Rarity": [5],
            "ATK Lvl 80": [100],
            "DEF Lvl 80": [200],
            "HP Lvl 80": [1000],
            "SPD Lvl 80": [100],
        }
    )

    # Mock the asyncio.run function
    with patch("asyncio.run", return_value=mock_df):
        char_data_df = main()

        # Verify expected dataframe structure and properties
        assert isinstance(char_data_df, pd.DataFrame)
        assert char_data_df.shape[1] == 9  # Added Version column makes it 9
        assert not char_data_df.empty
        assert "Version" in char_data_df.columns


if __name__ == "__main__":
    pytest.main()
