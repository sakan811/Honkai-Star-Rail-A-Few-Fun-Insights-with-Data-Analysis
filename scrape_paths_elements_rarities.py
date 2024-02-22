"""
This script uses Selenium to scrape data related to character paths, rarities, and elements
from the https://www.prydwen.gg/star-rail/ website.

It allows users to input URLs manually or automatically and saves the collected data to an Excel file.
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup

from codes import web_scrap as ws
from codes import get_urls_auto as get_urls


def scrape_paths_elements_rarities(url, data):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find elements based on class names
            path_elements = soup.find_all(class_=["Nihility", "Hunt", "Abundance", "Destruction", "Erudition", "Harmony", "Preservation"])
            rarity_elements = soup.find(class_=["rarity-5", "rarity-4"])
            char_elements = soup.find_all(class_=["Lightning", "Wind", "Fire", "Ice", "Quantum", "Imaginary", "Physical"])

            char_name = ws.extract_char_name(url)

            # Append data to the dictionary
            data['Character'].append(char_name)

            for element in path_elements:
                data['Path'].append(element.text.replace('Path of ', ''))
            for element in rarity_elements:
                if element.text == '5' or element.text == '4':
                    data['Rarity'].append(element.text)
            for element in char_elements:
                if element.text in ['Lightning', 'Wind', 'Physical', 'Fire', 'Ice', 'Quantum', 'Imaginary']:
                    data['Element'].append(element.text)
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)

    except Exception as e:
        print("An error occurred:", str(e))


def main():
    print('Automatically get urls: press 1')
    print('Manually get urls: press 2')

    while True:
        user_input = input('Enter number: ')

        if user_input == '1':
            user_input_list = get_urls.get_urls_auto()
            break
        elif user_input == '2':
            user_input_list = ws.enter_input()
            break
        else:
            print('Invalid input. Please enter 1 or 2.')

    data = {"Character": [], "Path": [], "Rarity": [], "Element": []}

    for url in user_input_list:
        scrape_paths_elements_rarities(url, data)

    # Create a DataFrame
    df = pd.DataFrame(data)

    output_name = f"hsr_paths_rarities_elements.xlsx"

    # Save the DataFrame to an Excel file
    df.to_excel(output_name, index=False)


if __name__ == '__main__':
    main()
