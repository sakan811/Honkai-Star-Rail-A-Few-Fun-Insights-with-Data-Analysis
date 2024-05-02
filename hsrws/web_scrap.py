"""
WebScrape contains methods related to web-scraping the desired data,
from the https://www.prydwen.gg/star-rail/ website.

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
import time

from loguru import logger
from selenium.common import TimeoutException, NoSuchElementException, WebDriverException
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import calculate_hsr
from . import create_excel


class WebScrape:
    def __init__(self):
        logger.info('Initialzing all desired elements\'s Xpath and Level list...')

        self.levels = ["Level 1", "Level 20", "Level 30", "Level 40", "Level 50", "Level 60", "Level 70", "Level 80"]
        self.stat_data_at_given_level_xpath = '//*[@id="gatsby-focus-wrapper"]/div/div[2]/div[2]/div[7]/div[12]/div[1]/div'
        self.level_dropdown_xpath = '//*[@id="gatsby-focus-wrapper"]/div/div[2]/div[2]/div[7]/div[11]/div[1]/div/div[1]/div'
        self.cookie_dialog_xpath = '//*[@id="qc-cmp2-ui"]'
        self.cookie_agree_button_xpath = '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]/span'

    @staticmethod
    def _extract_all_visible_text(
            driver: WebDriver,
            stat_list: list,
            stat_data_at_given_level_xpath: str) -> None:
        """
        Extracts all visible text in the specified path and stores it in a list.
        :param stat_data_at_given_level_xpath: Character stats at given Level XPath
        :param driver: The WebDriver instance used to interact with the web page.
        :param stat_list: The stat list for storing characters' stats.
        :return: None
        """
        logger.info('Extracting all visible text...')
        time.sleep(0.5)
        try:
            logger.info('Wait for the stat element to be visible')
            stats = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, stat_data_at_given_level_xpath))
            )
            stat_list.append(stats.text)
        except TimeoutException as e:
            logger.error(e)
            logger.error('TimeoutException')
        except NoSuchElementException as e:
            logger.error(e)
            logger.error('NoSuchElementException')
        except WebDriverException as e:
            logger.error(e)
            logger.error('WebDriverException')
        except Exception as e:
            logger.error(e)
            logger.error('Unexpected exception')
        else:
            logger.info('The stat element is visible')

    @staticmethod
    def _extract_char_name(url: str) -> str:
        """
        Extracts the name of the character from the given URL.
        :param url: The URL containing the character name.
        :return: The name of the character extracted from the URL.
        """
        logger.info(f'Extracting the character name from the {url = }...')

        # Split the URL using '/'
        url_parts: list[str] = url.split('/')
        logger.debug(f'{url_parts = }')

        # Take the last element as the character name
        char_name: str = url_parts[-1]
        logger.debug(f'{char_name = }')

        return char_name

    def _check_cookie(self, driver: WebDriver) -> None:
        """
        Checks for the presence of a cookie consent dialog and accepts it if found.
        :param driver: The WebDriver instance used to interact with the web page.
        :return: None
        """
        logger.info('Checking cookies...')

        try:
            logger.info('Wait for the cookie consent dialog to be visible')
            cookie_dialog: WebElement = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, self.cookie_dialog_xpath))
            )

            logger.info('If the cookie consent dialog is present, click on the specified element')
            if cookie_dialog.is_displayed():
                logger.info('Wait for the Agree button to appear.')
                agree_button: WebElement = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, self.cookie_agree_button_xpath)))

                logger.info('Click at the Agree button.')
                agree_button.click()
        except TimeoutException as e:
            logger.error(e)
            logger.error("TimeoutException. Cookie consent dialog not found or not displayed. Moving on.")
        except NoSuchElementException as e:
            logger.error(e)
            logger.error("NoSuchElementException. Agree button not found. Moving on.")
        else:
            logger.info('Cookie consent dialog is closed successfully.')

    def _check_if_path_exist(self, driver: WebDriver, character_name: str) -> bool:
        """
        Checks if the Level dropdown XPath exists on the webpage.
        :param driver: The WebDriver instance used to interact with the web page.
        :param character_name: A character name.
        :return: True if the XPath exists, False otherwise.
        """
        logger.info('Checking if path exists...')
        try:
            logger.info(f'Find the Web Element by the {self.level_dropdown_xpath}')
            driver.find_element(By.XPATH, self.level_dropdown_xpath)
            logger.info('Success. Return True')
            return True
        except NoSuchElementException as e:
            logger.error(e)
            logger.error(f'{character_name}: level_dropdown_xpath not found')
            return False
        except Exception as e:
            logger.error(f'An unexpected error occurred: {e}')
            return False

    def _click_at_each_level(self,
                             driver: WebDriver,
                             first_dropdown_xpath: str,
                             stat_list: list[str]) -> None:
        """
        Clicking at each Level dropdown
        :param driver: Selenium Web Driver
        :param first_dropdown_xpath: Dropdown XPath
        :param stat_list: Stat list
        :return: None
        """
        logger.info('Clicking at each Level...')
        element = None
        for level in self.levels:
            try:
                logger.info('Find the dropdown element')
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                    By.XPATH, first_dropdown_xpath))
                )
                time.sleep(0.5)
            except TimeoutException as e:
                logger.error(e)
                logger.error("TimeoutException")
            except NoSuchElementException as e:
                logger.error(e)
                logger.error("NoSuchElementException")
            except Exception as e:
                logger.error(e)
                logger.error("Unexpected error occurred")
            else:
                logger.info('Found the dropdown element successfully.')

            try:
                logger.info('Scroll down into view of the element')
                driver.execute_script("arguments[0].scrollIntoView(true);", element)

                y = -200
                logger.info(f'Scroll down y = {y}')
                driver.execute_script(f"window.scrollBy(0, {y});")

                logger.info('Click on the dropdown element')
                element.click()
                time.sleep(0.5)
            except NoSuchElementException as e:
                logger.error(e)
                logger.error("NoSuchElementException")
            except Exception as e:
                logger.error(e)
                logger.error("Unexpected error occurred")
            else:
                logger.info('Clicked at the dropdown element successfully.')

            try:
                logger.info('Find the dropdown option corresponding to the current level and click on it')
                option_xpath = f"//*[text()='{level}']"

                if level == 'Level 60' or level == 'Level 70' or level == 'Level 80':
                    y = 100
                    logger.info('Level 60, 70, and 80 are not in the view')
                    logger.info(f'Scroll up y = {y}')
                    driver.execute_script(f"window.scrollBy(0, {y});")

                option_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, option_xpath))
                )

                option_element.click()

                self._extract_all_visible_text(driver, stat_list, self.stat_data_at_given_level_xpath)
            except NoSuchElementException as e:
                logger.error(e)
                logger.error(f"Error clicking dropdown option for {level}: NoSuchElementException")
            except Exception as e:
                logger.error(e)
                logger.error("Unexpected error occurred")

    def _scrape_each_level(self,
                           driver: WebDriver,
                           first_output_path: str,
                           second_output_path: str) -> None:
        """
        Scrape character stats data at each Level.
        :param driver: Selenium Web Driver
        :param first_output_path: First Excel Output Path
        :param second_output_path: Second Excel Output Path
        :return: None
        """
        logger.info('Scraping each level...')

        stat_list = []

        self._click_at_each_level(driver, self.level_dropdown_xpath, stat_list)

        logger.info(f'Create an Excel from the \'stat_list\' and save to the {first_output_path = }')
        create_excel.create_excel(stat_list, first_output_path)

        logger.info('Close the browser')
        driver.quit()

        logger.info(f'Add additional columns to each Excel from {first_output_path = } '
                    f'and save them to {second_output_path = }')
        calculate_hsr.save_to_excel(first_output_path, second_output_path)

    def scrape(self, url: str, character_name: str, first_output_path: str, second_output_path: str) -> None:
        """
        Scrapes data from a webpage and performs further processing.
        :param url: The URL of the webpage to scrape.
        :param character_name: A character name.
        :param first_output_path: The file path for the first Excel output set.
        :param second_output_path: The file path for the second Excel output set.
        :return: None
        """
        logger.info(f'Web scraping is starting...'
                    f'Scrap from {url = } of {character_name = }')

        logger.info('Open the browser.')
        driver = webdriver.Chrome()

        driver.maximize_window()

        logger.info('Get the URL')
        driver.get(url)

        logger.info('Check cookies')
        self._check_cookie(driver)

        logger.info('Check if the Level dropdown Xpath exists')
        path_exist: bool = self._check_if_path_exist(driver, character_name)
        logger.debug(f'{path_exist = }')

        if path_exist:
            self._scrape_each_level(driver, first_output_path, second_output_path)
        else:
            logger.info(f'{path_exist = }. Close the browser')
            driver.quit()


if __name__ == '__main__':
    pass
