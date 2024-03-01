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


def prompt_user() -> list[str]:
    """
    Prompt the user whether they want to manually enter URLs or want the script to automatically get the URLs.
    :return: List of URLs
    """
    logging.info('Prompting the user...')
    print('Automatically get urls: press 1')
    print('Manually enter urls: press 2')

    while True:
        print('Enter number: ')
        user_input: str = input()
        logging.debug(f'{user_input = }')

        if user_input == '1':
            return get_urls_auto.get_urls_auto()

        elif user_input == '2':
            return web_scrap.enter_input()
        else:
            logging.warning('Invalid input. Please enter 1 or 2.')


def main() -> None:
    user_input_list: list[str] = prompt_user()
    logging.debug(f'{user_input_list = }')

    for url in user_input_list:
        character_name: str = web_scrap.extract_char_name(url)
        logging.debug(f'{character_name = }')

        first_output_path = f"hsr/{character_name}.xlsx"
        second_output_path = f"hsr/hsr_updated/{character_name}.xlsx"

        web_scrap.scrape(url, character_name, first_output_path, second_output_path)


if __name__ == '__main__':
    main()
