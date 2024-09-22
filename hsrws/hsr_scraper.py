import json
import os

import aiohttp
import pandas as pd
from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseModel, Field

load_dotenv()


async def get_payload(page_num: int) -> dict:
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


def get_headers() -> dict:
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


class Scraper(BaseModel):
    """
    Scraper class.
    Contain functions related to scraping data.

    Attributes:
        page_num (int): Page number of the page that contains data.
        char_data_dict (dict): Dictionary to store character data.
    """

    page_num: int = Field(0, ge=0)
    char_data_dict: dict[str, list[Any]] = {
        'Character': [],
        'Path': [],
        'Element': [],
        'Rarity': [],
        'ATK Lvl 80': [],
        'DEF Lvl 80': [],
        'HP Lvl 80': [],
        'SPD Lvl 80': []
    }

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
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload_data) as response:
                    if not response.status == 200:
                        logger.error(f"Error: Received status code {response.status}")
                        return pd.DataFrame(self.char_data_dict)

                    hsr_data = await response.json()

                    char_list: list[dict] = hsr_data['data']['list']

                    if not char_list:
                        logger.warning(f'Character list from page {self.page_num} is empty. Stop web-scraping process')
                        return pd.DataFrame(self.char_data_dict)

                    for char in char_list:
                        await self._scrape_character_data(char)

    async def _scrape_character_data(self, character_data: dict) -> None:
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

            try:
                char_stats = character_data['display_field']

                if char_stats == {}:
                    self.char_data_dict['ATK Lvl 80'].append(0)
                    self.char_data_dict['DEF Lvl 80'].append(0)
                    self.char_data_dict['HP Lvl 80'].append(0)
                    self.char_data_dict['SPD Lvl 80'].append(0)
                else:
                    char_stats_lvl_80_json_str = character_data['display_field']['attr_level_80']
                    char_stats_lvl_80 = json.loads(char_stats_lvl_80_json_str)
                    self.char_data_dict['ATK Lvl 80'].append(int(char_stats_lvl_80['base_atk']))
                    self.char_data_dict['DEF Lvl 80'].append(int(char_stats_lvl_80['base_def']))
                    self.char_data_dict['HP Lvl 80'].append(int(char_stats_lvl_80['base_hp']))
                    self.char_data_dict['SPD Lvl 80'].append(int(char_stats_lvl_80['base_speed']))
            except KeyError as e:
                logger.error(f"Stats of Character name {e} is not found. Append stats as zero.")
                raise KeyError

    async def _append_char_type_data(self, character_data: dict) -> None:
        """
        Appends character type data, e.g., Path, Element, and Rarity
        :param character_data: Dictionary that represents each character data.
        :return: None
        """
        logger.debug('Adding character type data...')

        try:
            path: list = character_data['filter_values']['character_paths']['values']
            element: list = character_data['filter_values']['character_combat_type']['values']
            rarity: list = character_data['filter_values']['character_rarity']['values']
        except KeyError:
            logger.error(f'No character type data found for {character_data["name"]}', exc_info=True)
            raise KeyError

        try:
            self.char_data_dict['Path'].append(path[0])
            self.char_data_dict['Element'].append(element[0])
            self.char_data_dict['Rarity'].append(rarity[0])
        except IndexError:
            logger.error(f'No character type data found for {character_data["name"]}', exc_info=True)
            raise IndexError


if __name__ == '__main__':
    pass
