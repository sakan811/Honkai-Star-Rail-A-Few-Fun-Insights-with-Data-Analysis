"""
This script uses Selenium to scrape data related to character paths, rarities, and elements
from the https://www.prydwen.gg/star-rail/ website.

It allows users to input URLs manually or automatically and saves the collected data to an Excel file.
"""
import bs4
import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests import Response

from codes import web_scrap as ws
from codes.honkai_star_rail_scrape import HonkaiStarRailScrape


class HonkaiStarRailScrapePathAndElement(HonkaiStarRailScrape):
    def __init__(self, auto=False, urls=None):
        """
        :param urls: List of URLs entered by the user.
                    Required if auto is False.
                    Default is None.
        :param auto: If True, the script automatically get URLs, if not, the user need to manually enter URLs.
                    Default is False.
        """
        super().__init__(auto, urls)
        self.data = {"Character": [], "Path": [], "Rarity": [], "Element": []}

    def _scrape_paths_elements_rarities(self, url: str) -> None:
        """
        Scrape Path, Element, and Rarity data from the URL.
        :param url: Character's URL.
        :return: None
        """
        try:
            # Send an HTTP GET request to the URL
            response: Response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find elements based on class names
                path_elements: bs4.ResultSet = soup.find_all(
                    class_=["Nihility", "Hunt", "Abundance", "Destruction", "Erudition", "Harmony", "Preservation"]
                )
                rarity_elements: bs4.Tag | bs4.NavigableString = soup.find(class_=["rarity-5", "rarity-4"])
                char_elements: bs4.ResultSet = soup.find_all(
                    class_=["Lightning", "Wind", "Fire", "Ice", "Quantum", "Imaginary", "Physical"])

                char_name: str = ws.extract_char_name(url)

                # Append data to the dictionary
                self.data['Character'].append(char_name)

                for element in path_elements:
                    self.data['Path'].append(element.text.replace('Path of ', ''))
                for element in rarity_elements:
                    if element.text == '5' or element.text == '4':
                        self.data['Rarity'].append(element.text)
                for element in char_elements:
                    if element.text in ['Lightning', 'Wind', 'Physical', 'Fire', 'Ice', 'Quantum', 'Imaginary']:
                        self.data['Element'].append(element.text)
            else:
                print("Failed to retrieve the webpage. Status code:", response.status_code)

        except Exception as e:
            print("An error occurred:", str(e))

    def hsr_scrape(self) -> None:
        """
        Main function to start all processes related to web scraping of the website.
        :return: None
        """
        user_input_list = []
        if self.auto is True:
            user_input_list: list[str] = self._check_auto_param()
        elif self.auto is False:
            user_input_list = self.urls

        for url in user_input_list:
            self._scrape_paths_elements_rarities(url)

        # Create a DataFrame
        df = pd.DataFrame(self.data)

        output_name = f"data/hsr_paths_rarities_elements.xlsx"

        # Save the DataFrame to an Excel file
        df.to_excel(output_name, index=False)


if __name__ == '__main__':
    url = ['https://www.prydwen.gg/star-rail/characters/gallagher']
    main = HonkaiStarRailScrapePathAndElement(urls=url)
    main.hsr_scrape()
