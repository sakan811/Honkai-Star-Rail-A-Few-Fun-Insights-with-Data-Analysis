"""
HonkaiStarRailScrapeStats class set up the web-scraping process of the https://www.prydwen.gg/star-rail/ website.
To scrape characters' stats data from the website.

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
"""
from loguru import logger

from .web_scrap import WebScrape
from .get_urls_auto import GetUrlAuto


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
        if self.auto is True:
            logger.info(f'{self.auto = }. Automatically get URLs')
            return GetUrlAuto().get_urls_auto()
        elif self.auto is False:
            logger.info(f'{self.auto = }. User manually entered URLs')
            return self.urls

    def hsr_scrape(self) -> None:
        """
        Function to start all processes related to web-scraping characters' stats from the website.
        :return: None
        """
        logger.info('Starting main function...')
        user_input_list = self._check_auto_param()
        logger.debug(f'{user_input_list = }')

        try:
            for url in user_input_list:
                character_name: str = self._extract_char_name(url)
                logger.debug(f'{character_name = }')

                first_output_path = f"hsr/{character_name}.xlsx"
                second_output_path = f"hsr/hsr_updated/{character_name}.xlsx"

                self.scrape(url, character_name, first_output_path, second_output_path)
        except Exception as e:
            logger.error(f'Error: {e}')


if __name__ == '__main__':
    pass
