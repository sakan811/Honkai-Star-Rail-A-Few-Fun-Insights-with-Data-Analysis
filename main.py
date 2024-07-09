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
import asyncio
import sys

import pandas as pd
from loguru import logger

from hsrws.data_transformer import transform_char_name, add_char_version, clean_path_name
from hsrws.hsr_scraper import get_headers, scrape_hsr_data
from hsrws.sqlite_pipeline import load_to_sqlite

logger.configure(handlers=[{"sink": sys.stderr, "level": "INFO"}])
logger.add('main.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w', level="INFO")


def main() -> pd.DataFrame:
    """
    Main function to start the web-scraping process.
    :return: Pandas Dataframe.
    """
    url = 'https://sg-wiki-api.hoyolab.com/hoyowiki/hsr/wapi/get_entry_page_list'
    headers = get_headers()

    char_data_dict = {
        'Character': [],
        'Path': [],
        'Element': [],
        'Rarity': [],
        'ATK Lvl 80': [],
        'DEF Lvl 80': [],
        'HP Lvl 80': [],
        'SPD Lvl 80': []
    }

    asyncio.run(scrape_hsr_data(url, headers, char_data_dict))

    char_data_df = pd.DataFrame(char_data_dict)

    char_data_df['Character'] = char_data_df['Character'].apply(transform_char_name)
    char_data_df['Path'] = char_data_df['Path'].apply(clean_path_name)

    add_char_version(char_data_df)

    return char_data_df


if __name__ == '__main__':
    char_data_df = main()
    load_to_sqlite(char_data_df)
