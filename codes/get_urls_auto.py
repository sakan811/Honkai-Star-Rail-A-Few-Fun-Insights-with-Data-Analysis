"""
This script automatically extracts character URLs from the https://www.prydwen.gg/star-rail/ website.
and prints the list of URLs.

"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import web_scrap as ws


def get_urls_auto():
    url_lists = []
    url = 'https://www.prydwen.gg/star-rail/characters'
    driver = webdriver.Chrome()

    driver.get(url)

    ws.check_cookie(driver)

    parent_xpath = '//*[@id="gatsby-focus-wrapper"]/div/div[2]/div[2]/div[6]'
    parent_element = driver.find_element(By.XPATH, parent_xpath)
    urls_xpath = './/a[@href]'
    url_elements = parent_element.find_elements(By.XPATH, urls_xpath)

    for url_element in url_elements:
        href_value = url_element.get_attribute('href')
        url_lists.append(href_value)

    driver.quit()

    return url_lists


if __name__ == '__main__':
    url_list = get_urls_auto()
    print(url_list)
