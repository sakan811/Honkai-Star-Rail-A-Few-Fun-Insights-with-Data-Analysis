"""Tests for scrape_hsr_data method in Scraper class."""

import unittest
from unittest.mock import patch, AsyncMock

import pandas as pd
import pytest

from hsrws.core.scraper import Scraper


class TestScrapeHsrData(unittest.TestCase):
    """Unit test cases for scrape_hsr_data method in the Scraper class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.scraper = Scraper()
        self.url = "https://test.url"
        self.headers = {"User-Agent": "test"}
    
    @pytest.fixture(autouse=True)
    def _patch_event_loop(self, event_loop):
        """Provide an event loop for each test."""
        self.loop = event_loop
        
    @pytest.mark.asyncio
    async def test_scrape_hsr_data_single_page(self):
        """Test scraping process with a single page of data."""
        # Create mock character data
        mock_character_list = [
            {
                "name": "Character1",
                "filter_values": {
                    "path": {"values": ["The Hunt"]},
                    "element": {"values": ["Fire"]},
                    "rarity": {"values": [5]},
                },
            },
            {
                "name": "Character2",
                "filter_values": {
                    "path": {"values": ["The Harmony"]},
                    "element": {"values": ["Ice"]},
                    "rarity": {"values": [4]},
                },
            },
        ]
        
        # Mock empty list for second page to end the loop
        mock_empty_list = []
        
        # Mock the _fetch_character_list method
        with patch.object(
            self.scraper, 
            '_fetch_character_list', 
            new_callable=AsyncMock
        ) as mock_fetch:
            mock_fetch.side_effect = [mock_character_list, mock_empty_list]
            
            # Mock process_character_list function
            with patch('hsrws.core.character.process_character_list', new_callable=AsyncMock) as mock_process:
                # Define behavior: populate the character dictionary when process_character_list is called
                async def side_effect(scraper_instance, char_list):
                    for char in char_list:
                        scraper_instance.char_data_dict["Character"].append(char["name"])
                        scraper_instance.char_data_dict["Path"].append("The Hunt" if char["name"] == "Character1" else "The Harmony")
                        scraper_instance.char_data_dict["Element"].append("Fire" if char["name"] == "Character1" else "Ice")
                        scraper_instance.char_data_dict["Rarity"].append(5 if char["name"] == "Character1" else 4)
                        scraper_instance.char_data_dict["ATK Lvl 80"].append(100)
                        scraper_instance.char_data_dict["DEF Lvl 80"].append(200)
                        scraper_instance.char_data_dict["HP Lvl 80"].append(1000)
                        scraper_instance.char_data_dict["SPD Lvl 80"].append(100)
                
                mock_process.side_effect = side_effect
                
                # Call the method
                result_df = await self.scraper.scrape_hsr_data(self.url, self.headers)
                
                # Verify the results
                self.assertIsInstance(result_df, pd.DataFrame)
                self.assertEqual(mock_fetch.call_count, 2)
                self.assertEqual(len(result_df), 2)
                self.assertEqual(list(result_df["Character"]), ["Character1", "Character2"])
                self.assertEqual(list(result_df["Path"]), ["The Hunt", "The Harmony"])
                self.assertEqual(list(result_df["Element"]), ["Fire", "Ice"])
                self.assertEqual(list(result_df["Rarity"]), [5, 4])

    @pytest.mark.asyncio
    async def test_scrape_hsr_data_no_results(self):
        """Test scraping process when no results are returned."""
        # Mock empty list for first page
        mock_empty_list = []
        
        # Mock the _fetch_character_list method
        with patch.object(
            self.scraper, 
            '_fetch_character_list', 
            new_callable=AsyncMock
        ) as mock_fetch:
            mock_fetch.return_value = mock_empty_list
            
            # Call the method
            result_df = await self.scraper.scrape_hsr_data(self.url, self.headers)
            
            # Verify the results
            self.assertIsInstance(result_df, pd.DataFrame)
            self.assertEqual(mock_fetch.call_count, 1)
            self.assertTrue(result_df.empty)

    @pytest.mark.asyncio
    async def test_scrape_hsr_data_multiple_pages(self):
        """Test successful scraping with multiple pages."""
        mock_char_list = [{"name": "Char1"}, {"name": "Char2"}]
        mock_df = pd.DataFrame({"name": ["Char1", "Char2"]})

        with (
            patch(
                "hsrws.utils.payload.get_payload", new_callable=AsyncMock
            ) as mock_get_payload,
            patch.object(
                self.scraper, "_fetch_character_list", new_callable=AsyncMock
            ) as mock_fetch,
            patch(
                "hsrws.core.character.process_character_list", new_callable=AsyncMock
            ) as mock_process,
        ):
            mock_get_payload.return_value = {"some": "payload"}
            mock_fetch.side_effect = [mock_char_list, mock_char_list, []]
            self.scraper.char_data_dict = {"name": ["Char1", "Char2"]}

            result = await self.scraper.scrape_hsr_data(self.url, self.headers)

            self.assertIsInstance(result, pd.DataFrame)
            pd.testing.assert_frame_equal(result, mock_df)
            self.assertEqual(mock_get_payload.call_count, 3)
            self.assertEqual(mock_fetch.call_count, 3)
            self.assertEqual(mock_process.call_count, 2)

    @pytest.mark.asyncio
    async def test_scrape_hsr_data_empty_first_page(self):
        """Test when first page is empty."""
        with (
            patch(
                "hsrws.utils.payload.get_payload", new_callable=AsyncMock
            ) as mock_get_payload,
            patch.object(
                self.scraper, "_fetch_character_list", new_callable=AsyncMock
            ) as mock_fetch,
            patch(
                "hsrws.core.character.process_character_list", new_callable=AsyncMock
            ) as mock_process,
        ):
            mock_get_payload.return_value = {"some": "payload"}
            mock_fetch.return_value = []
            self.scraper.char_data_dict = {}

            result = await self.scraper.scrape_hsr_data(self.url, self.headers)

            self.assertIsInstance(result, pd.DataFrame)
            self.assertTrue(result.empty)
            self.assertEqual(mock_get_payload.call_count, 1)
            self.assertEqual(mock_fetch.call_count, 1)
            self.assertEqual(mock_process.call_count, 0)

    @pytest.mark.asyncio
    async def test_scrape_hsr_data_exception(self):
        """Test exception handling."""
        with (
            patch(
                "hsrws.utils.payload.get_payload", new_callable=AsyncMock
            ) as mock_get_payload,
            patch.object(
                self.scraper, "_fetch_character_list", new_callable=AsyncMock
            ) as mock_fetch,
            patch(
                "hsrws.core.character.process_character_list", new_callable=AsyncMock
            ) as mock_process,
        ):
            mock_get_payload.side_effect = Exception("Test error")

            with self.assertRaises(Exception):
                await self.scraper.scrape_hsr_data(self.url, self.headers)

            self.assertEqual(mock_get_payload.call_count, 1)
            self.assertEqual(mock_fetch.call_count, 0)
            self.assertEqual(mock_process.call_count, 0)

    @pytest.mark.asyncio
    async def test_scrape_hsr_data_logging(self):
        """Test logging during the scraping process."""
        mock_char_list = [{"name": "Char1"}]

        with (
            patch(
                "hsrws.utils.payload.get_payload", new_callable=AsyncMock
            ) as mock_get_payload,
            patch.object(
                self.scraper, "_fetch_character_list", new_callable=AsyncMock
            ) as mock_fetch,
            patch("hsrws.core.character.process_character_list", new_callable=AsyncMock),
            patch("loguru.logger.info") as mock_logger,
        ):
            mock_get_payload.return_value = {"some": "payload"}
            mock_fetch.side_effect = [mock_char_list, []]
            self.scraper.char_data_dict = {"name": ["Char1"]}

            await self.scraper.scrape_hsr_data(self.url, self.headers)
            
            # Verify logging calls
            mock_logger.assert_any_call("Scraping HSR data...")
            mock_logger.assert_any_call("Scraping data of page 1")
            mock_logger.assert_any_call("Scraping data of page 2")
            mock_logger.assert_any_call("Finished scraping.")
