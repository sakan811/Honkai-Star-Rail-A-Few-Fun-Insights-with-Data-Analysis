import json
import os
from typing import Any

import aiohttp
import pandas as pd
from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseModel, Field

load_dotenv()


async def get_payload(page_num: int) -> dict[str, Any]:
    """
    Gets payload with specified page number.
    :param page_num: Page number.
    :return: Dictionary.
    """
    logger.info(f"Getting payload for page {page_num}...")
    return {
        "filters": [],
        "menu_id": "104",
        "page_num": page_num,
        "page_size": 30,
        "use_es": True
    }


def get_headers() -> dict[str, Any]:
    """
    Gets headers.
    :return: Headers as Dictionary.
    """
    logger.info("Getting headers...")
    return {
        'Origin': 'https://wiki.hoyolab.com',
        'Referer': 'https://wiki.hoyolab.com/',
        'User-Agent': os.getenv('USER_AGENT'),
        'X-Rpc-Language': 'en-us',
        'X-Rpc-Wiki_app': 'hsr'
    }


def default_char_data_dict() -> dict[str, list[Any]]:
    return {
        'Character': [],
        'Path': [],
        'Element': [],
        'Rarity': [],
        'ATK Lvl 80': [],
        'DEF Lvl 80': [],
        'HP Lvl 80': [],
        'SPD Lvl 80': []
    }


def get_first_value(data: dict[str, Any], *keys: str, default=None) -> str | int | None:
    """
    Retrieves the first value from a nested dictionary structure.

    Searches for the first non-empty value in the 'values' list of the specified
    keys in the given data dictionary.

    Returns the first found value or the default.

    :param data: The dictionary to search in
    :param keys: Variable number of keys to search for
    :param default: Value to return if no value is found, defaults to None
    :returns: The first non-empty value found, or the default value
    :raises KeyError: If a specified key exists in data but doesn't have a 'values' key
    """
    for key in keys:
        if key in data:
            values = data[key]['values']
            if values:
                return values[0]
    return default


class Scraper(BaseModel):
    """
    Scraper class.
    Contain functions related to scraping data.

    Attributes:
        page_num (int): Page number of the page that contains data.
        char_data_dict (dict): Dictionary to store character data.
    """

    page_num: int = Field(0, ge=0)
    char_data_dict: dict[str, list[Any]] = Field(default_factory=default_char_data_dict)

    async def scrape_hsr_data(self, url: str, headers: dict) -> pd.DataFrame:
        """
        Scrapes HSR data from JSON response.
        :param url: URL.
        :param headers: Headers.
        :return: Dataframe containing scraped data.
        """
        logger.info("Scraping HSR data...")

        while True:
            self.page_num += 1
            payload_data = await get_payload(page_num=self.page_num)

            logger.info(f"Scraping data of page {self.page_num}")
            char_list = await self._fetch_character_list(url, headers, payload_data)

            if not char_list:
                logger.info(f'Finished scraping.')
                break

            await self._process_character_list(char_list)

        return pd.DataFrame(self.char_data_dict)

    @staticmethod
    async def _fetch_character_list(url: str, headers: dict, payload_data: dict) -> list[dict]:
        """
        Fetches the character list from the API.
        :param url: URL.
        :param headers: Headers.
        :param payload_data: Payload data for the request.
        :return: List of characters.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload_data) as response:
                if response.status != 200:
                    logger.error(f"Error: Received status code {response.status}")
                    return []

                hsr_data = await response.json()
                return hsr_data['data']['list']

    async def _process_character_list(self, char_list: list[dict]) -> None:
        """
        Processes the character list.
        :param char_list: List of characters.
        :return: None
        """
        for char in char_list:
            await self._scrape_character_data(char)

    async def _scrape_character_data(self, character_data: dict[str, Any]) -> None:
        """
        Scrapes character data from JSON response.
        :param character_data: Dictionary that represents each character data.
        :return: None
        """
        try:
            character_name = character_data['name']
        except KeyError as e:
            logger.error(f"Character name {e} is not found.")
            raise KeyError
        else:
            self.char_data_dict['Character'].append(character_name)
            await self._append_char_type_data(character_data)
            self._append_char_stats(character_data)

    def _append_char_stats(self, character_data: dict[str, Any]) -> None:
        """
        Appends character stats to the character data dictionary.
        :param character_data: Dictionary that represents each character data.
        :return: None
        """
        try:
            char_stats = character_data['display_field']
            if not char_stats:
                self._append_stats()
            else:
                char_stats_lvl_80_json_str = char_stats['attr_level_80']
                char_stats_lvl_80: dict[str, Any] = json.loads(char_stats_lvl_80_json_str)
                self._append_stats(char_stats_lvl_80)
        except KeyError as e:
            logger.error(f"Stats of Character name {e} is not found. Append stats as zero.")
            self._append_stats()

    def _append_stats(self, char_stats_lvl_80: dict[str, Any] = None) -> None:
        """
        Appends stats to the character data dictionary.
        :param char_stats_lvl_80: Character stats at level 80.
        :return: None
        """
        if char_stats_lvl_80:
            try:
                base_atk_lvl_80 = int(char_stats_lvl_80['base_atk'])
                self.char_data_dict['ATK Lvl 80'].append(base_atk_lvl_80)
            except KeyError as e:
                logger.error(f"KeyError: {e}. Appending 'base_atk_lvl_80' as zero.")
                self.char_data_dict['ATK Lvl 80'].append(0)

            try:
                base_def_lvl_80 = int(char_stats_lvl_80['base_def'])
                self.char_data_dict['DEF Lvl 80'].append(base_def_lvl_80)
            except KeyError as e:
                logger.error(f"KeyError: {e}. Appending 'base_def_lvl_80' as zero.")
                self.char_data_dict['DEF Lvl 80'].append(0)

            try:
                base_hp_lvl_80 = int(char_stats_lvl_80['base_hp'])
                self.char_data_dict['HP Lvl 80'].append(base_hp_lvl_80)
            except KeyError as e:
                logger.error(f"KeyError: {e}. Appending 'base_hp_lvl_80' as zero.")
                self.char_data_dict['HP Lvl 80'].append(0)

            try:
                base_speed_lvl_80 = int(char_stats_lvl_80['base_speed'])
                self.char_data_dict['SPD Lvl 80'].append(base_speed_lvl_80)
            except KeyError as e:
                logger.error(f"KeyError: {e}. Appending 'base_speed_lvl_80' as zero.")
                self.char_data_dict['SPD Lvl 80'].append(0)
        else:
            self.char_data_dict['ATK Lvl 80'].append(0)
            self.char_data_dict['DEF Lvl 80'].append(0)
            self.char_data_dict['HP Lvl 80'].append(0)
            self.char_data_dict['SPD Lvl 80'].append(0)

    async def _append_char_type_data(self, character_data: dict) -> None:
        """
        Appends character type data, e.g., Path, Element, and Rarity
        :param character_data: Dictionary that represents each character data.
        :return: None
        """
        logger.debug('Adding character type data...')

        try:
            character_filter_values = character_data.get('filter_values', {})

            path = get_first_value(character_filter_values, 'character_paths')
            element = get_first_value(character_filter_values, 'character_combat_type')
            rarity = get_first_value(character_filter_values, 'character_rarity')

            self.char_data_dict['Path'].append(path or 'Unknown')
            self.char_data_dict['Element'].append(element or 'Unknown')
            self.char_data_dict['Rarity'].append(rarity or 'Unknown')

        except Exception as e:
            logger.error(f'Error processing character data for {character_data.get("name", "Unknown")}: {str(e)}',
                         exc_info=True)
            raise IndexError


if __name__ == '__main__':
    pass
