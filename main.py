"""
The main script to run a web scraping of the https://www.prydwen.gg/star-rail/ website.
This script ask users to choose how they want to scrap from the website.
"""
from loguru import logger

from codes import web_scrap
from codes import get_urls_auto

logger.add('main.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w')


class Main:
    def __init__(self, auto=False, urls=None):
        """

        :param urls: List of URLs entered by the user. Default is None.
        :param auto: If True, the script automatically gets URLs, if not, the user need to manually enter URLs.
                    Default is False.
        """
        self.auto = auto
        self.urls = urls
        self.user_input_list = []

    def check_auto_param(self) -> list[str]:
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

    def main(self) -> None:
        """
        Main function to start all processes related to web scraping of the website.
        :return: None
        """
        logger.info('Starting main function...')
        user_input_list = self.check_auto_param()
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


if __name__ == '__main__':
    url = ['https://www.prydwen.gg/star-rail/characters/gallagher']
    main = Main(urls=url)
    main.main()
