"""
This script automatically extracts character URLs from the https://www.prydwen.gg/star-rail/ website,
And prints the list of URLs.
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

from loguru import logger
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from .web_scrap import WebScrape


class GetUrlAuto(WebScrape):
    def __init__(self):
        super().__init__()
        self.website_url = 'https://www.prydwen.gg/star-rail/characters/'
        self.character_page_class_name = 'employees-container'
        self.character_urls_xpath = './/a[@href]'

    def find_character_page(self, driver: WebDriver) -> WebElement:
        """
        Finds the character page by its Class Name and returns its WebElement.
        :param driver: Chrome WebDriver instance
        :return: Character page WebElement
        """
        logger.info(f'Finding the Web element at {self.character_page_class_name = }...')
        try:
            character_page: WebElement = driver.find_element(By.CLASS_NAME, self.character_page_class_name)
        except NoSuchElementException as e:
            logger.error(e)
            logger.error(f'{self.character_page_class_name} not found')
        else:
            logger.info(f'{self.character_page_class_name} found successfully.')
            return character_page

    def find_character_urls(self, character_page: WebElement) -> list[WebElement]:
        """
        Finds each character URL within the character page by their Xpath and returns their WebElements as a List.
        :param character_page: Character page WebElement
        :return: List of character URL WebElement
        """
        logger.info(f'Finding the Web elements at {self.character_urls_xpath = }...')
        try:
            character_url_elements: list[WebElement] = character_page.find_elements(By.XPATH, self.character_urls_xpath)
        except NoSuchElementException as e:
            logger.error(e)
            logger.error(f'{self.character_urls_xpath} not found')
        else:
            logger.info(f'{self.character_urls_xpath} found successfully.')
            logger.debug(f'{character_url_elements = }')
            return character_url_elements

    def get_urls_auto(self) -> list[str]:
        """
        Automatically extracts the character URLs from the website.
        :return: A list of extracted character URLs.
        """
        logger.info('Auto-getting URLs...')

        url_lists = []

        logger.info('Set --disable-images and --headless option for Chrome')
        chrome_options = Options()
        chrome_options.add_argument('--disable-images')  # Disable loading images for faster page loading
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without GUI) for better performance

        logger.info('Open the web browser.')
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(self.website_url)

        logger.info('Check cookies')
        self._check_cookie(driver)

        character_page = self.find_character_page(driver)
        character_url_elements = self.find_character_urls(character_page)

        logger.info('Extract the href attribute value from each URL element and append it to the URL list')
        for character_url in character_url_elements:
            href_value: str = character_url.get_attribute('href')
            logger.debug(f'{href_value = }')

            logger.info(f'Add {href_value = } to the {url_lists = }')
            url_lists.append(href_value)

        logger.info('Close the browser.')
        driver.quit()

        return url_lists


if __name__ == '__main__':
    pass
