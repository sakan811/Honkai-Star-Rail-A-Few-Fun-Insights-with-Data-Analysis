#    Copyright 2024 Sakan Nirattisaykul
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import json

import aiohttp
from loguru import logger


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
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://wiki.hoyolab.com',
        'Referer': 'https://wiki.hoyolab.com/',
        'X-Rpc-Language': 'en-us',
        'X-Rpc-Wiki_app': 'hsr'
    }


async def scrape_hsr_data(url: str, headers: dict, char_data_dict: dict) -> None:
    """
    Scrapes HSR data from JSON response.
    :param url: URL.
    :param headers: Headers.
    :param char_data_dict: Character data dictionary to append scraped data.
    :return: None
    """
    logger.info("Scraping HSR data...")
    async with aiohttp.ClientSession() as session:
        page_num = 0
        while True:
            page_num += 1
            payload_data = await get_payload(page_num=page_num)

            logger.info(f"Scraping data of page {page_num}")
            async with session.post(url, headers=headers, json=payload_data) as response:
                if response.status == 200:
                    hsr_data = await response.json()

                    char_list = hsr_data['data']['list']

                    if char_list:
                        for char in char_list:
                            char_data_dict['Character'].append(char['name'])

                            char_stats = char['display_field']

                            char_data_dict['Path'].append(char['filter_values']['character_paths']['values'][0])
                            char_data_dict['Element'].append(char['filter_values']['character_combat_type']['values'][0])
                            char_data_dict['Rarity'].append(char['filter_values']['character_rarity']['values'][0])

                            if char_stats == {}:
                                char_data_dict['ATK Lvl 80'].append(0)
                                char_data_dict['DEF Lvl 80'].append(0)
                                char_data_dict['HP Lvl 80'].append(0)
                                char_data_dict['SPD Lvl 80'].append(0)
                            else:
                                char_stats_lvl_80_json_str = char['display_field']['attr_level_80']
                                char_stats_lvl_80 = json.loads(char_stats_lvl_80_json_str)
                                char_data_dict['ATK Lvl 80'].append(int(char_stats_lvl_80['base_atk']))
                                char_data_dict['DEF Lvl 80'].append(int(char_stats_lvl_80['base_def']))
                                char_data_dict['HP Lvl 80'].append(int(char_stats_lvl_80['base_hp']))
                                char_data_dict['SPD Lvl 80'].append(int(char_stats_lvl_80['base_speed']))
                    else:
                        logger.warning(f'Character list from page {page_num} is empty. Stop web-scraping process')
                        break
                else:
                    logger.error(f"Error: Received status code {response.status}")
                    break


if __name__ == '__main__':
    pass
