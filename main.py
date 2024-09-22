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
from typing import Any

import pandas as pd
from loguru import logger

from hsrws.data_transformer import transform_char_name, add_char_version, clean_path_name
from hsrws.hsr_scraper import get_headers, Scraper
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
    url: str = 'https://sg-wiki-api.hoyolab.com/hoyowiki/hsr/wapi/get_entry_page_list'
    headers: dict[str, Any] = get_headers()

    scraper: Scraper = Scraper()
    character_data_dataframe: pd.DataFrame = asyncio.run(scraper.scrape_hsr_data(url, headers))

    character_data_dataframe['Character'] = character_data_dataframe['Character'].apply(transform_char_name)
    character_data_dataframe['Path'] = character_data_dataframe['Path'].apply(clean_path_name)

    add_char_version(character_data_dataframe)

    return character_data_dataframe


if __name__ == '__main__':
    char_data_df = main()
    load_to_sqlite(char_data_df)
