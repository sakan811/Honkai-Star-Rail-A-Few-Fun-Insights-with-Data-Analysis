from codes import web_scrap
from codes import get_urls_auto


def main():
    print('Automatically get urls: press 1')
    print('Manually get urls: press 2')

    while True:
        user_input = input('Enter number: ')

        if user_input == '1':
            user_input_list = get_urls_auto.get_urls_auto()
            break
        elif user_input == '2':
            user_input_list = web_scrap.enter_input()
            break
        else:
            print('Invalid input. Please enter 1 or 2.')

    for url in user_input_list:
        web_scrap.scrape(url)


if __name__ == '__main__':
    main()
