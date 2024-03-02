"""
The main script to run a web scraping of the https://www.prydwen.gg/star-rail/ website.
This script ask users to choose how they want to scrap from the website.
"""
import logging

from codes import web_scrap
from codes import get_urls_auto

logging.basicConfig(
    filename='main.log',
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(name)s | %(filename)s | %(funcName)s | %(lineno)d | %(message)s',
    filemode='w'
)

selenium_logger = logging.getLogger('selenium')
selenium_logger.setLevel(logging.INFO)

# Create a StreamHandler for console output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

# Add the console handler to the root logger
root_logger = logging.getLogger()
root_logger.addHandler(console_handler)


def check_auto_param(auto: bool) -> list[str]:
    """
    Check if the user has parsed \'auto\' parameter as True.
    :param auto: If True, the script automatically get URLs, if not, the user need to manually enter URLs.
                Default is False.
    :return: List of URLs
    """
    logging.info('Checking if the user has parsed \'auto\' parameter as True...')
    if auto is True:
        logging.info(f'{auto = }. Automatically get URLs')
        return get_urls_auto.get_urls_auto()
    elif auto is False:
        logging.info(f'{auto = }. Manually enter URLs')
        return web_scrap.enter_input()


def main(auto: bool = False) -> None:
    """
    Main function to start all processes related to web scraping of the website.
    :param auto: If True, the script automatically get URLs, if not, the user need to manually enter URLs.
                Default is False.
    :return: None
    """
    user_input_list: list[str] = check_auto_param(auto)
    logging.debug(f'{user_input_list = }')

    for url in user_input_list:
        character_name: str = web_scrap.extract_char_name(url)
        logging.debug(f'{character_name = }')

        first_output_path = f"hsr/{character_name}.xlsx"
        second_output_path = f"hsr/hsr_updated/{character_name}.xlsx"

        web_scrap.scrape(url, character_name, first_output_path, second_output_path)


if __name__ == '__main__':
    main()
