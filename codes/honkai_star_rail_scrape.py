"""
HonkaiStarRailScrape class takes care of the web scraping process of the https://www.prydwen.gg/star-rail/ website.
"""
from loguru import logger

from . import web_scrap
from . import get_urls_auto


class HonkaiStarRailScrape:
    def __init__(self, auto=False, urls=None):
        """
        :param urls: List of URLs entered by the user. Default is None.
        :param auto: If True, the script automatically gets URLs, if not, the user need to manually enter URLs.
                    Default is False.
        """
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
            return get_urls_auto.get_urls_auto()
        elif self.auto is False:
            logger.info(f'{self.auto = }. User manually entered URLs')
            return self.urls

    def hsr_scrape(self) -> None:
        """
        Main function to start all processes related to web scraping of the website.
        :return: None
        """
        logger.info('Starting main function...')
        user_input_list = self._check_auto_param()
        logger.debug(f'{user_input_list = }')

        try:
            for url in user_input_list:
                character_name: str = web_scrap.extract_char_name(url)
                logger.debug(f'{character_name = }')

                first_output_path = f"hsr/{character_name}.xlsx"
                second_output_path = f"hsr/hsr_updated/{character_name}.xlsx"

                web_scrap.scrape(url, character_name, first_output_path, second_output_path)
        except Exception as e:
            logger.error(f'Error: {e}')
