"""
The main script to run a web scraping of the https://www.prydwen.gg/star-rail/ website.
This script ask users to choose how they want to scrap from the website.
"""

from codes import web_scrap
from codes import get_urls_auto


def main() -> None:
    print('Automatically get urls: press 1')
    print('Manually enter urls: press 2')

    while True:
        user_input: str = input('Enter number: ')

        if user_input == '1':
            user_input_list: list[str] = get_urls_auto.get_urls_auto()
            break
        elif user_input == '2':
            user_input_list: list[str] = web_scrap.enter_input()
            break
        else:
            print('Invalid input. Please enter 1 or 2.')

    for url in user_input_list:
        # Extract the character name from the URL
        hsr_name: str = web_scrap.extract_char_name(url)

        first_output_path = f"hsr/{hsr_name}.xlsx"
        second_output_path = f"hsr/hsr_updated/{hsr_name}.xlsx"

        web_scrap.scrape(url, hsr_name, first_output_path, second_output_path)


if __name__ == '__main__':
    main()
