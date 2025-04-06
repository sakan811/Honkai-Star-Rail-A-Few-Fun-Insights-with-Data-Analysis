"""Tests for scrape_hsr_data method in Scraper class."""

from unittest.mock import patch, Mock

import pandas as pd
import pytest

from hsrws.core.scraper import Scraper

# Add this decorator to mark the module for pytest-asyncio
pytestmark = pytest.mark.asyncio


class TestScrapeHsrData:
    """Unit test cases for scrape_hsr_data method in the Scraper class."""

    @pytest.fixture
    def setup_test_data(self):
        """Set up test data for tests."""
        # Character data that will be consistently used
        mock_character_list_page1 = [
            {
                "name": "Character1",
                "filter_values": {
                    "character_paths": {"values": ["The Hunt"]},
                    "character_combat_type": {"values": ["Fire"]},
                    "character_rarity": {"values": ["5-Star"]},
                },
            },
            {
                "name": "Character2",
                "filter_values": {
                    "character_paths": {"values": ["The Harmony"]},
                    "character_combat_type": {"values": ["Ice"]},
                    "character_rarity": {"values": ["4-Star"]},
                },
            },
        ]

        mock_character_list_page2 = [
            {
                "name": "Character3",
                "filter_values": {
                    "character_paths": {"values": ["The Nihility"]},
                    "character_combat_type": {"values": ["Lightning"]},
                    "character_rarity": {"values": ["5-Star"]},
                },
            },
        ]

        # Empty list to signal end of pages
        mock_empty_list = []

        return {
            "page1": mock_character_list_page1,
            "page2": mock_character_list_page2,
            "empty": mock_empty_list,
        }

    @pytest.fixture
    def setup_scraper(self):
        """Set up a scraper instance for each test."""
        scraper = Scraper()
        # Reset char_data_dict to ensure test isolation
        scraper.char_data_dict = {
            "Character": [],
            "Path": [],
            "Element": [],
            "Rarity": [],
            "ATK Lvl 80": [],
            "DEF Lvl 80": [],
            "HP Lvl 80": [],
            "SPD Lvl 80": [],
        }
        # Set up common test values
        url = "https://test.url"
        headers = {"User-Agent": "test"}

        return scraper, url, headers

    # Define a predictable process_character_list mock behavior
    @staticmethod
    async def mock_process_character_list(scraper, char_list):
        """Mock implementation of process_character_list for testing."""
        for char in char_list:
            name = char["name"]
            # Extract path, element and rarity with predictable logic
            path = char["filter_values"]["character_paths"]["values"][0].replace(
                "The ", ""
            )
            element = char["filter_values"]["character_combat_type"]["values"][0]
            rarity = char["filter_values"]["character_rarity"]["values"][0].split("-")[
                0
            ]

            # Add data to scraper dict
            scraper.char_data_dict["Character"].append(name)
            scraper.char_data_dict["Path"].append(path)
            scraper.char_data_dict["Element"].append(element)
            scraper.char_data_dict["Rarity"].append(rarity)
            scraper.char_data_dict["ATK Lvl 80"].append(100)
            scraper.char_data_dict["DEF Lvl 80"].append(200)
            scraper.char_data_dict["HP Lvl 80"].append(1000)
            scraper.char_data_dict["SPD Lvl 80"].append(100)

    @pytest.mark.asyncio
    async def test_scrape_hsr_data_single_page(self, setup_scraper, setup_test_data):
        """Test scraping process with a single page of data."""
        scraper, url, headers = setup_scraper
        test_data = setup_test_data

        # Set up mocks with consistent, deterministic behavior
        with (
            patch("hsrws.utils.payload.get_payload", return_value={"page": 1}),
            patch.object(
                scraper,
                "_fetch_character_list",
                side_effect=[test_data["page1"], test_data["empty"]],
            ),
            patch(
                "hsrws.core.character.process_character_list",
                side_effect=self.mock_process_character_list,
            ),
        ):
            # Call the method
            result_df = await scraper.scrape_hsr_data(url, headers)

            # Verify results deterministically
            assert isinstance(result_df, pd.DataFrame)
            assert len(result_df) == 2
            assert list(result_df["Character"]) == ["Character1", "Character2"]
            assert list(result_df["Path"]) == ["Hunt", "Harmony"]
            assert list(result_df["Element"]) == ["Fire", "Ice"]
            assert list(result_df["Rarity"]) == ["5", "4"]

    @pytest.mark.asyncio
    async def test_scrape_hsr_data_no_results(self, setup_scraper):
        """Test scraping process when no results are returned."""
        scraper, url, headers = setup_scraper

        # Directly mock with return_value instead of side_effect for more predictable behavior
        with (
            patch("hsrws.utils.payload.get_payload", return_value={"page": 1}),
            patch.object(scraper, "_fetch_character_list", return_value=[]),
        ):
            # Call the method
            result_df = await scraper.scrape_hsr_data(url, headers)

            # Verify the results
            assert isinstance(result_df, pd.DataFrame)
            assert result_df.empty

    @pytest.mark.asyncio
    async def test_scrape_hsr_data_multiple_pages(self, setup_scraper, setup_test_data):
        """Test successful scraping with multiple pages."""
        scraper, url, headers = setup_scraper
        test_data = setup_test_data

        # Simple, predictable mocks
        with (
            patch("hsrws.utils.payload.get_payload", return_value={"page": 1}),
            patch.object(
                scraper,
                "_fetch_character_list",
                side_effect=[
                    test_data["page1"],
                    test_data["page2"],
                    test_data["empty"],
                ],
            ),
            patch(
                "hsrws.core.character.process_character_list",
                side_effect=self.mock_process_character_list,
            ),
        ):
            # Execute test
            result = await scraper.scrape_hsr_data(url, headers)

            # Deterministic assertions
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 3
            assert list(result["Character"]) == [
                "Character1",
                "Character2",
                "Character3",
            ]
            assert list(result["Path"]) == ["Hunt", "Harmony", "Nihility"]
            assert list(result["Element"]) == ["Fire", "Ice", "Lightning"]
            assert list(result["Rarity"]) == ["5", "4", "5"]

    @pytest.mark.asyncio
    async def test_scrape_hsr_data_exception(self, setup_scraper):
        """Test exception handling."""
        scraper, url, headers = setup_scraper

        # Use a more comprehensive patching approach to isolate the test
        # We need to patch both get_payload and _fetch_character_list to ensure
        # the test doesn't try to make any real network calls
        with patch(
            "hsrws.core.scraper.get_payload", side_effect=Exception("Test error")
        ) as mock_payload:
            # Wrap in pytest.raises to capture the exception
            with pytest.raises(Exception) as excinfo:
                await scraper.scrape_hsr_data(url, headers)

            # Verify payload function was called
            assert mock_payload.called
            # Make sure we got the expected exception
            assert "Test error" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_scrape_hsr_data_logging(self, setup_scraper, setup_test_data):
        """Test logging during the scraping process."""
        scraper, url, headers = setup_scraper
        test_data = setup_test_data

        # Mock logger with a simple Mock object rather than complex AsyncMock
        mock_logger = Mock()

        with (
            patch("hsrws.utils.payload.get_payload", return_value={"page": 1}),
            patch.object(
                scraper,
                "_fetch_character_list",
                side_effect=[test_data["page1"], test_data["empty"]],
            ),
            patch(
                "hsrws.core.character.process_character_list",
                side_effect=self.mock_process_character_list,
            ),
            patch("loguru.logger.info", mock_logger),
        ):
            # Execute test
            await scraper.scrape_hsr_data(url, headers)

            # Verify logging in a deterministic way
            mock_logger.assert_any_call("Scraping HSR data...")
            mock_logger.assert_any_call("Scraping data of page 1")
            mock_logger.assert_any_call("Scraping data of page 2")
            mock_logger.assert_any_call("Finished scraping.")
