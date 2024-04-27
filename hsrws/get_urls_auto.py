"""
This script automatically extracts character URLs from the https://www.prydwen.gg/star-rail/ website.
and prints the list of URLs.

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
"""
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from .web_scrap import WebScrape


class GetUrlAuto(WebScrape):
    def __init__(self):
        super().__init__()

    def get_urls_auto(self) -> list[str]:
        """
        Automatically extracts the character URLs from the website.
        :return: A list of extracted character URLs.
        """
        logger.info('Auto-getting URLs...')

        url_lists = []
        url = 'https://www.prydwen.gg/star-rail/characters'

        logger.info('Open the web browser.')
        driver = webdriver.Chrome()

        logger.info(f'Get the {url = }')
        driver.get(url)

        logger.info('Check cookies')
        self._check_cookie(driver)

        parent_xpath = '//*[@id="gatsby-focus-wrapper"]/div/div[2]/div[2]/div[6]'
        logger.debug(f'{parent_xpath = }')

        logger.info(f'Find the Web element at {parent_xpath = }')
        parent_element: WebElement = driver.find_element(By.XPATH, parent_xpath)

        urls_xpath = './/a[@href]'
        logger.debug(f'{urls_xpath = }')

        url_elements: list[WebElement] = parent_element.find_elements(By.XPATH, urls_xpath)
        logger.debug(f'{url_elements = }')

        logger.info('Extract the href attribute value from each URL element and append it to the URL list')
        for url_element in url_elements:
            href_value: str = url_element.get_attribute('href')
            logger.debug(f'{href_value = }')
            logger.info(f'Add {href_value = } to the {url_lists = }')
            url_lists.append(href_value)

        logger.info('Close the browser.')
        driver.quit()

        return url_lists


if __name__ == '__main__':
    pass
