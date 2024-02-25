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


def main() -> None:
    logging.info('Prompt the user.')
    print('Automatically get urls: press 1')
    print('Manually enter urls: press 2')

    while True:
        print('Enter number: ')
        user_input: str = input()
        logging.debug(f'{user_input = }')

        if user_input == '1':
            user_input_list: list[str] = get_urls_auto.get_urls_auto()
            logging.debug(user_input_list)
            break
        elif user_input == '2':
            user_input_list: list[str] = web_scrap.enter_input()
            logging.debug(user_input_list)
            break
        else:
            logging.warning('Invalid input. Please enter 1 or 2.')

    for url in user_input_list:
        logging.info(f'Extract the character name from the {url = }')
        character_name: str = web_scrap.extract_char_name(url)
        logging.debug(character_name)

        first_output_path = f"hsr/{character_name}.xlsx"
        second_output_path = f"hsr/hsr_updated/{character_name}.xlsx"

        logging.info(f'Web scraping is starting.'
                     f'Scrap from {url = } of {character_name = }')
        web_scrap.scrape(url, character_name, first_output_path, second_output_path)


if __name__ == '__main__':
    main()
