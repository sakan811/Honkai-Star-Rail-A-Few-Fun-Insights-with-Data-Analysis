"""
This script automatically extracts character URLs from the https://www.prydwen.gg/star-rail/ website.
and prints the list of URLs.

"""
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from . import web_scrap


def get_urls_auto() -> list[str]:
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
    web_scrap.check_cookie(driver)

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
