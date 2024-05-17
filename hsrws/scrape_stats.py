"""
HonkaiStarRailScrapeStats class set up the web-scraping process of the https://www.prydwen.gg/star-rail/ website.
To scrape characters' stats data from the website.
"""
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

import os
from concurrent.futures import ThreadPoolExecutor

from loguru import logger

from .web_scrap import WebScrape
from .get_urls_auto import GetUrlAuto


def create_dir(output_dir: str) -> None:
    """
    Create the output directory.
    :param output_dir: Output directory.
    :return: None
    """
    logger.info(f'Creating {output_dir = } directory if not exist...')
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    except PermissionError as e:
        logger.error(e)
        logger.error('Permission denied.')
    except FileExistsError as e:
        logger.error(e)
        logger.error('File already exists.')
    except OSError as e:
        logger.error(e)
        logger.error('Operation failed.')
    except Exception as e:
        logger.error(e)
        logger.error('Unexpected error.')
    else:
        logger.info(f'Created {output_dir = } successfully')


class HonkaiStarRailScrapeStats(WebScrape):
    def __init__(self, auto: bool = False, urls: list[str] = None):
        """
        :param urls: List of URLs entered by the user. Default is None.
        :param auto: If True, the script automatically gets URLs, if not, the user need to manually enter URLs.
                    Default is False.
        """
        super().__init__()
        self.auto = auto
        self.urls = urls
        self.user_input_list = []

    def _check_auto_param(self) -> list[str]:
        """
        Check if the user has parsed \'auto\' parameter as True.
        :return: List of URLs
        """
        logger.info('Checking if the user has parsed \'auto\' parameter as True...')
        try:
            if self.auto is True:
                logger.info(f'{self.auto = }. Automatically get URLs')
                return GetUrlAuto().get_urls_auto()
            elif self.auto is False:
                logger.info(f'{self.auto = }. User manually entered URLs')
                return self.urls
        except Exception as e:
            logger.error(e)
            logger.error('Unexpected error.')

    def hsr_scrape(self) -> None:
        """
        Function to start all processes related to web-scraping characters' stats from the website.

        Use ThreadPoolExecutor to parallelize the web-scraping process.
        :return: None
        """
        logger.info('Starting main function...')
        url_lists = self._check_auto_param()
        logger.debug(f'{url_lists = }')

        logger.info('Define the number of threads to use')
        num_threads = 4
        logger.debug(f'{num_threads = }')

        logger.info('Create a ThreadPoolExecutor to manage threads')
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for url in url_lists:
                character_name: str = self._extract_char_name(url)
                logger.debug(f'{character_name = }')

                first_output_dir = 'hsr'
                create_dir(first_output_dir)

                first_output_path = f"hsr/{character_name}.xlsx"

                second_output_dir = 'hsr/hsr_updated'
                create_dir(second_output_dir)

                second_output_path = f"hsr/hsr_updated/{character_name}.xlsx"

                logger.info('Submit the scrape task to the executor')
                future = executor.submit(self.scrape, url, character_name, first_output_path, second_output_path)

                logger.info('Append task to the \'futures\' list')
                futures.append(future)

            logger.info('Wait for all futures to complete')
            for future in futures:
                try:
                    # Re-raise any exceptions caught during the execution of the scrape method
                    future.result()
                except Exception as e:
                    logger.error(f'Error during scraping: {e}')


if __name__ == '__main__':
    pass
