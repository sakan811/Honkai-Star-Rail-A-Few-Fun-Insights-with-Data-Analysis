"""
This script performs web scraping of HSR character stats from the https://www.prydwen.gg/star-rail/ website.
"""
import re
from selenium.common import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

from codes import calculate_hsr
from codes import create_excel


def click_drop_down(driver: WebDriver, first_dropdown_xpath: str) -> None:
    """
    Finds and clicks on the specified dropdown element on a web page.
    :param driver: The WebDriver instance used to interact with the web page.
    :param first_dropdown_xpath: The XPath of the dropdown element to be clicked.
    :return: None
    """
    logging.info('Clicking drop down...')
    try:
        logging.info('Waiting for the dropdown element to be clickable')
        first_dropdown: WebElement = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, first_dropdown_xpath)))

        first_dropdown_location: dict = first_dropdown.location
        logging.debug(f'{first_dropdown_location =}')

        script = f"window.scrollTo({first_dropdown_location['x']}, {first_dropdown_location['y'] - 200});"
        logging.debug(f'{script = }')

        logging.info('Execute the script')
        driver.execute_script(script)

        logging.info('Clicks the element.')
        first_dropdown.click()
    except TimeoutException:
        logging.error("TimeoutException. The first dropdown was not found within the specified timeout. Moving on.")


def click_level(driver: WebDriver, level: str) -> None:
    """
    Clicks on the specified level in the dropdown on a web page.
    :param driver: The WebDriver instance used to interact with the web page.
    :param level: The text of the level to be clicked in the dropdown.
    :return: None
    """
    logging.info('Clicking level...')

    level_xpath = f'//*[text()="{level}"]'
    logging.debug(f'{level_xpath = }')

    logging.info('Attempt to click the element with a maximum number of retries')
    max_retries = 3
    logging.debug(f'{max_retries = }')
    retries = 0
    logging.debug(f'{retries = }')

    while retries < max_retries:
        try:
            logging.info('Wait for the element to be present')
            level_element: WebElement = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, level_xpath)))
            logging.info('Click at the Web element.')
            level_element.click()

            logging.info('Success. Break the loop.')
            break
        except Exception as e:
            logging.error('Clicking unsuccessfully. Scroll down and try again')
            driver.execute_script("window.scrollBy(0, 100);")
            logging.info('Execute Script ("window.scrollBy(0, 100);")')
            retries += 1
            logging.debug(f'{retries = }')
    else:
        logging.error(f"Failed to click the element after {max_retries} retries.")


def extract_all_visible_text(
        driver: WebDriver,
        stat_list: list,
        level: str,
        level_result_xpath: str,
        first_dropdown_xpath: str) -> None:
    """
    Extracts all visible text in the specified path and stores it in a list.
    :param driver: The WebDriver instance used to interact with the web page.
    :param stat_list: The stat list for storing characters' stats.
    :param level: The expected level text to validate against the extracted text.
    :param level_result_xpath: The XPath of the element containing the text to be extracted.
    :param first_dropdown_xpath: The XPath of the dropdown element to click if the level is not correct.
    :return: None
    """
    logging.info('Extracting all visible text...')

    logging.info('Find and extract all visible text in the specified path')
    level_result_element: WebElement = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, level_result_xpath))
    )

    level_text: str = level_result_element.text
    logging.debug(f'{level_text = }')

    level_is_correct: bool = check_level(level_text, level)
    logging.debug(f'{level_is_correct = }')

    if level_is_correct:
        stat_list.append(level_text)
        logging.info(f'Add {level_text} to the \'stat_list\' list')
    else:
        logging.info(f'Click at the dropdown at {first_dropdown_xpath}')
        click_drop_down(driver, first_dropdown_xpath)


def check_level(level_result_text: str, level: str) -> bool:
    """
    Checks if the extracted level matches the expected level.
    :param level_result_text: The text containing the extracted level information.
    :param level: The expected level text to validate against the extracted level.
    :return: True if the extracted level matches the expected level, False otherwise.
    """
    logging.info('Checking level...')

    logging.info('Use regular expression to create Match')
    current_level_match: re.Match[str] = re.search(r'Level \d+', level_result_text)
    logging.debug(f'{current_level_match = }')

    logging.info('Check if the script is scraping data from the expected level')
    if current_level_match:
        # Extract the matched level
        current_level: str = current_level_match.group()
        logging.debug(f'{current_level = }')

        logging.info('Compare the extracted level with the expected level')
        if current_level != level:
            logging.info('The level not matched. Return False')
            return False
        else:
            logging.info('The level matched. Return True')
            return True
    else:
        logging.info('No match is found. Return False')
        return False


def extract_char_name(url: str) -> str:
    """
    Extracts the name of the character from the given URL.
    :param url: The URL containing the character name.
    :return: The name of the character extracted from the URL.
    """
    logging.info(f'Extracting the character name from the {url = }...')

    # Split the URL using '/'
    url_parts: list[str] = url.split('/')
    logging.debug(f'{url_parts = }')

    # Take the last element as the character name
    char_name: str = url_parts[-1]
    logging.debug(f'{char_name = }')

    return char_name


def check_cookie(driver: WebDriver) -> None:
    """
    Checks for the presence of a cookie consent dialog and accepts it if found.
    :param driver: The WebDriver instance used to interact with the web page.
    :return: None
    """
    logging.info('Checking cookies...')

    cookie_dialog_xpath = '//*[@id="qc-cmp2-ui"]'
    logging.debug(f'{cookie_dialog_xpath = }')

    try:
        logging.info('Wait for the cookie consent dialog to be visible')
        cookie_dialog: WebElement = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, cookie_dialog_xpath))
        )

        logging.info('If the cookie consent dialog is present, click on the specified element')
        if cookie_dialog.is_displayed():
            agree_button_xpath = '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]/span'
            logging.debug(f'{agree_button_xpath = }')
            logging.info('Wait for the Agree button to appear.')
            agree_button: WebElement = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, agree_button_xpath)))
            logging.info('Click at the Agree button.')
            agree_button.click()

    except TimeoutException:
        logging.error("TimeoutException. Cookie consent dialog not found or not displayed. Moving on.")

    except NoSuchElementException:
        logging.error("NoSuchElementException. Agree button not found. Moving on.")


def check_if_path_exist(driver: WebDriver, first_dropdown_xpath: str, character_name: str) -> bool:
    """
    Checks if the specified XPath exists on the webpage.
    :param driver: The WebDriver instance used to interact with the web page.
    :param first_dropdown_xpath: The XPath to be checked for existence.
    :param character_name: A character name.
    :return: True if the XPath exists, False otherwise.
    """
    logging.info('Checking if path exists...')
    try:
        logging.info(f'Find the Web Element by the {first_dropdown_xpath}')
        driver.find_element(By.XPATH, first_dropdown_xpath)
        logging.info('Success. Return True')
        return True
    except Exception:
        logging.error(f'{character_name}: first_dropdown_xpath not found')
        return False


def click_at_each_level(driver: WebDriver,
                        levels: list[str],
                        stat_data_at_given_level_xpath: str,
                        first_dropdown_xpath: str,
                        stat_list: list[str]) -> None:
    """
    Clicking at each Level dropdown
    :param driver: Selenium Web Driver
    :param levels: Level list
    :param stat_data_at_given_level_xpath: Character stats at given Level XPath
    :param first_dropdown_xpath: Dropdown XPath
    :param stat_list: Stat list
    :return: None
    """
    logging.info('Clicking at rach Level...')
    for level in levels:
        logging.info(f'Click at the dropdown at {stat_data_at_given_level_xpath}')
        click_drop_down(driver, first_dropdown_xpath)
        logging.info(f'Click at the {level}')
        click_level(driver, level)
        logging.info(f'Extract all visible texts of {level = } '
                     f'from {stat_data_at_given_level_xpath = } from {first_dropdown_xpath = }')
        extract_all_visible_text(driver, stat_list, level, stat_data_at_given_level_xpath, first_dropdown_xpath)


def scrape_each_level(driver: WebDriver,
                      first_dropdown_xpath: str,
                      first_output_path: str,
                      second_output_path: str) -> None:
    """
    Scrape character stats data at each Level.
    :param driver: Selenium Web Driver
    :param first_dropdown_xpath: Level Dropdown XPath
    :param first_output_path: First Excel Output Path
    :param second_output_path: Second Excel Output Path
    :return: None
    """
    logging.info('Scraping each level...')

    stat_data_at_given_level_xpath = '//*[@id="gatsby-focus-wrapper"]/div/div[2]/div[2]/div[7]/div[12]/div[1]/div'
    logging.debug(f'{stat_data_at_given_level_xpath = }')

    stat_list = []
    levels = ["Level 1", "Level 20", "Level 30", "Level 40", "Level 50", "Level 60", "Level 70", "Level 80"]

    click_at_each_level(driver, levels, stat_data_at_given_level_xpath, first_dropdown_xpath, stat_list)

    logging.info(f'Create an Excel from the \'stat_list\' and save to the {first_output_path = }')
    create_excel.create_excel(stat_list, first_output_path)

    logging.info('Close the browser')
    driver.quit()

    logging.info(f'Add additional columns to each Excel from {first_output_path = } '
                 f'and save them to {second_output_path = }')
    calculate_hsr.save_to_excel(first_output_path, second_output_path)


def scrape(url: str, character_name: str, first_output_path: str, second_output_path: str) -> None:
    """
    Scrapes data from a webpage and performs further processing.
    :param url: The URL of the webpage to scrape.
    :param character_name: A character name.
    :param first_output_path: The file path for the first Excel output set.
    :param second_output_path: The file path for the second Excel output set.
    :return: None
    """
    logging.info(f'Web scraping is starting...'
                 f'Scrap from {url = } of {character_name = }')

    logging.info('Open the browser.')
    driver = webdriver.Chrome()

    driver.maximize_window()

    logging.info('Get the URL')
    driver.get(url)

    logging.info('Check cookies')
    check_cookie(driver)

    first_dropdown_xpath = '//*[@id="gatsby-focus-wrapper"]/div/div[2]/div[2]/div[7]/div[11]/div[1]/div/div[1]/div'
    logging.debug(f'{first_dropdown_xpath = }')

    logging.info('Check if the path exists')
    path_exist: bool = check_if_path_exist(driver, first_dropdown_xpath, character_name)
    logging.debug(f'{path_exist = }')

    if path_exist:
        scrape_each_level(driver, first_dropdown_xpath, first_output_path, second_output_path)
    else:
        logging.info(f'{path_exist = }. Close the browser')
        driver.quit()





if __name__ == '__main__':
    pass
