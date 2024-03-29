"""
HonkaiStarRailScrapePathAndElement class uses Selenium to scrape data related to character paths, rarities, and elements
from the https://www.prydwen.gg/star-rail/ website.

It allows users to input URLs manually or automatically and saves the collected data to an Excel file.
"""
import os
import bs4
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from requests import Response
from loguru import logger

from .web_scrap import WebScrape as ws
from .scrape_stats import HonkaiStarRailScrapeStats


class HonkaiStarRailScrapePathAndElement(HonkaiStarRailScrapeStats):
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
        logger.info('Scraping Path, Element, and Rarity data...')
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
                logger.error(f"Failed to retrieve the webpage. Status code: {response.status_code}")

        except Exception as e:
            logger.error(f"An error occurred: {e}")

    @staticmethod
    def _save_to_data_dir(df: DataFrame) -> None:
        """
        Save the dataframe to the specified directory.
        :param df: Pandas DataFrame
        :return: None
        """
        logger.info("Saving dataframe to the given directory...")
        # Define the output directory
        output_directory = "data"

        # Ensure the directory exists, create it if it doesn't
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Define the file path
        output_name = os.path.join(output_directory, "hsr_paths_rarities_elements.xlsx")

        # Save the DataFrame to an Excel file
        df.to_excel(output_name, index=False)

    def hsr_scrape(self) -> None:
        """
        Function to start all processes related to web-scraping Path, Elements, and Rarity from the website.
        :return: None
        """
        logger.info("Starting Path, Elements, and Rarity web-scraping process...")
        user_input_list = []
        if self.auto is True:
            user_input_list: list[str] = self._check_auto_param()
        elif self.auto is False:
            user_input_list = self.urls

        for url in user_input_list:
            self._scrape_paths_elements_rarities(url)

        # Create a DataFrame
        df = pd.DataFrame(self.data)

        self._save_to_data_dir(df)


if __name__ == '__main__':
    pass
