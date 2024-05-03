"""
HonkaiStarRailScrapePathAndElement class uses Selenium to scrape data related to character paths, rarities, and elements
from the https://www.prydwen.gg/star-rail/ website.

It allows users to input URLs manually or automatically and saves the collected data to an Excel file.
"""

#    Copyright 2024 Sakan Nirattisaykul
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import os
import bs4
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from requests import Response
from loguru import logger

from .scrape_stats import HonkaiStarRailScrapeStats, create_dir


class HonkaiStarRailScrapePathAndElement(HonkaiStarRailScrapeStats):
    def __init__(self, auto=False, urls=None):
        """
        :param urls: List of URLs entered by the user.
                    Required if auto is False.
                    Default is None.
        :param auto: If True, the script automatically gets URLs, if not, the user needs to manually enter URLs.
                    Default is False.
        """
        super().__init__(auto, urls)
        self.data = {"Character": [], "Path": [], "Rarity": [], "Element": []}

    def _clean_data(
            self,
            path_elements: bs4.ResultSet,
            rarity_elements: bs4.Tag,
            char_elements: bs4.ResultSet) -> None:
        """
        Clean data scrpaed from path_elements, rarity_elements, and char_elements.
        :param path_elements: Web elements contain Path data.
        :param rarity_elements: Web elements contain Rarity data.
        :param char_elements: Web elements contain Character data.
        :return: None
        """
        logger.info('Cleaning data from path_elements, rarity_elements, and char_elements...')

        logger.info('Clean data from path_elements')
        try:
            for element in path_elements:
                self.data['Path'].append(element.text.replace('Path of ', ''))
        except AttributeError as e:
            logger.error(e)
            logger.error('AttributeError')
        except Exception as e:
            logger.error(e)
            logger.error('Unexpected error')

        logger.info('Clean data from rarity_elements')
        try:
            for element in rarity_elements:
                if element.text == '5' or element.text == '4':
                    self.data['Rarity'].append(element.text)
        except AttributeError as e:
            logger.error(e)
            logger.error('AttributeError')
        except Exception as e:
            logger.error(e)
            logger.error('Unexpected error')

        logger.info('Clean data from char_elements')
        try:
            for element in char_elements:
                if element.text in ['Lightning', 'Wind', 'Physical', 'Fire', 'Ice', 'Quantum', 'Imaginary']:
                    self.data['Element'].append(element.text)
        except AttributeError as e:
            logger.error(e)
            logger.error('AttributeError')
        except Exception as e:
            logger.error(e)
            logger.error('Unexpected error')

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
                    class_=["Lightning", "Wind", "Fire", "Ice", "Quantum", "Imaginary", "Physical"]
                )

                char_name: str = self._extract_char_name(url)

                logger.info('Append data to the dictionary')
                self.data['Character'].append(char_name)

                self._clean_data(path_elements, rarity_elements, char_elements)
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
        create_dir(output_directory)

        # Define the file path
        output_name = os.path.join(output_directory, "hsr_paths_rarities_elements.xlsx")

        # Save the DataFrame to an Excel file
        try:
            df.to_excel(output_name, index=False)
        except Exception as e:
            logger.error(e)
            logger.error('Unexpected error')

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

        logger.info('Create a DataFrame from a dictionary, self.data')
        df = None
        try:
            df = pd.DataFrame(self.data)
        except KeyError as e:
            logger.error(e)
            logger.error('KeyError')
        except ValueError as e:
            logger.error(e)
            logger.error('ValueError')
        except Exception as e:
            logger.error(e)
            logger.error('Unexpected error')

        self._save_to_data_dir(df)


if __name__ == '__main__':
    pass
