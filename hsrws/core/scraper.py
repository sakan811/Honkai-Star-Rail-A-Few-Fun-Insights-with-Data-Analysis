"""Core scraper functionality."""

import json
import os
from typing import Any

import aiohttp
import pandas as pd
from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseModel, Field

from hsrws.utils.payload import get_payload, get_headers, default_char_data_dict

load_dotenv()


class Scraper(BaseModel):
    """
    Scraper class for HSR character data.
    
    Attributes:
        page_num: Page number of the page that contains data.
        char_data_dict: Dictionary to store character data.
    """

    page_num: int = Field(0, ge=0)
    char_data_dict: dict[str, list[Any]] = Field(default_factory=default_char_data_dict)

    async def scrape_hsr_data(self, url: str, headers: dict) -> pd.DataFrame:
        """
        Scrapes HSR character data from JSON response.
        
        Args:
            url: URL for the API.
            headers: Headers for the request.
        
        Returns:
            Dataframe containing scraped character data.
        """
        logger.info("Scraping HSR data...")

        while True:
            self.page_num += 1
            payload_data = await get_payload(page_num=self.page_num)

            logger.info(f"Scraping data of page {self.page_num}")
            char_list = await self._fetch_character_list(url, headers, payload_data)

            if not char_list:
                logger.info("Finished scraping.")
                break

            # Import here to avoid circular import
            from hsrws.core.character import process_character_list
            await process_character_list(self, char_list)

        return pd.DataFrame(self.char_data_dict)

    @staticmethod
    async def _fetch_character_list(
        url: str, headers: dict, payload_data: dict
    ) -> list[dict]:
        """
        Fetches the character list from the API.
        
        Args:
            url: URL for the API.
            headers: Headers for the request.
            payload_data: Payload data for the request.
        
        Returns:
            List of characters.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, headers=headers, json=payload_data
            ) as response:
                if response.status != 200:
                    logger.error(f"Error: Received status code {response.status}")
                    return []

                hsr_data = await response.json()
                return hsr_data["data"]["list"] 