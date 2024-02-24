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
from validators import url as validate_url

from codes.calculate_hsr import calculate_hsr
from codes.create_excel import create_excel


def click_drop_down(driver: WebDriver, first_dropdown_xpath: str) -> None:
    """
    Finds and clicks on the specified dropdown element on a web page.
    :param driver: The WebDriver instance used to interact with the web page.
    :param first_dropdown_xpath: The XPath of the dropdown element to be clicked.
    :return: None
    """
    try:
        # Waiting for the dropdown element to be clickable
        first_dropdown: WebElement = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, first_dropdown_xpath)))

        first_dropdown_location: dict = first_dropdown.location

        script = f"window.scrollTo({first_dropdown_location['x']}, {first_dropdown_location['y'] - 200});"

        driver.execute_script(script)

        first_dropdown.click()
    except TimeoutException:
        print("The first dropdown was not found within the specified timeout. Moving on.")


def click_level(driver: WebDriver, level: str) -> None:
    """
    Clicks on the specified level in the dropdown on a web page.
    :param driver: The WebDriver instance used to interact with the web page.
    :param level: The text of the level to be clicked in the dropdown.
    :return: None
    """
    level_xpath = f'//*[text()="{level}"]'

    # Attempt to click the element with a maximum number of retries
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            # Wait for the element to be present
            level_element: WebElement = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, level_xpath)))
            level_element.click()

            # Break the loop if click is successful
            break
        except Exception as e:
            # If an exception occurs, scroll down and try again
            driver.execute_script("window.scrollBy(0, 100);")
            retries += 1
    else:
        print(f"Failed to click the element after {max_retries} retries.")


def extract_all_visible_text(
        driver: WebDriver,
        store: list,
        level: str,
        level_result_xpath: str,
        first_dropdown_xpath: str) -> None:
    """
    Extracts all visible text in the specified path and stores it in a list.
    :param driver: The WebDriver instance used to interact with the web page.
    :param store: The list to store the extracted text.
    :param level: The expected level text to validate against the extracted text.
    :param level_result_xpath: The XPath of the element containing the text to be extracted.
    :param first_dropdown_xpath: The XPath of the dropdown element to click if the level is not correct.
    :return: None
    """
    # Find and extract all visible text in the specified path
    level_result_element: WebElement = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, level_result_xpath))
    )

    level_text: str = level_result_element.text

    level_is_correct: bool = check_level(level_text, level)

    if level_is_correct:
        store.append(level_text)
    else:
        click_drop_down(driver, first_dropdown_xpath)


def check_level(level_result_text: str, level: str) -> bool:
    """
    Checks if the extracted level matches the expected level.
    :param level_result_text: The text containing the extracted level information.
    :param level: The expected level text to validate against the extracted level.
    :return: True if the extracted level matches the expected level, False otherwise.
    """
    # Use regular expression to find the current level in the lines
    current_level_match: re.Match[str] = re.search(r'Level \d+', level_result_text)

    # Check if a match is found
    if current_level_match:
        # Extract the matched level
        current_level: str = current_level_match.group()

        # Compare the extracted level with the provided level
        if current_level != level:
            return False
        else:
            return True
    else:
        return False  # Return False if no match is found


def extract_char_name(url: str) -> str:
    """
    Extracts the name of the character from the given URL.
    :param url: The URL containing the character name.
    :return: The name of the character extracted from the URL.
    """
    # Split the URL using '/'
    url_parts: list[str] = url.split('/')

    # Take the last element as the character name
    char_name: str = url_parts[-1]

    return char_name


def check_cookie(driver: WebDriver) -> None:
    """
    Checks for the presence of a cookie consent dialog and accepts it if found.
    :param driver: The WebDriver instance used to interact with the web page.
    :return: None
    """
    cookie_dialog_xpath = '//*[@id="qc-cmp2-ui"]'

    try:
        # Wait for the cookie consent dialog to be visible
        cookie_dialog: WebElement = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, cookie_dialog_xpath))
        )

        # If the cookie consent dialog is present, click on the specified element
        if cookie_dialog.is_displayed():
            agree_button_xpath = '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]/span'
            agree_button: WebElement = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, agree_button_xpath)))
            agree_button.click()

    except TimeoutException:
        # Handle the case where the dialog is not present or not displayed within the timeout
        logging.error("Cookie consent dialog not found or not displayed. Moving on.")

    except NoSuchElementException:
        # Handle the case where the agree button is not found
        logging.error("Agree button not found. Moving on.")


def check_if_path_exist(driver: WebDriver, first_dropdown_xpath: str, character_name: str) -> bool:
    """
    Checks if the specified XPath exists on the webpage.
    :param driver: The WebDriver instance used to interact with the web page.
    :param first_dropdown_xpath: The XPath to be checked for existence.
    :param character_name: A character name.
    :return: True if the XPath exists, False otherwise.
    """
    try:
        driver.find_element(By.XPATH, first_dropdown_xpath)
        return True
    except Exception:
        print(f'{character_name}: first_dropdown_xpath not found')
        return False


def scrape(url: str, character_name: str, first_output_path: str, second_output_path: str) -> None:
    """
    Scrapes data from a webpage and performs further processing.
    :param url: The URL of the webpage to scrape.
    :param character_name: A character name.
    :param first_output_path: The file path for the first Excel output set.
    :param second_output_path: The file path for the second Excel output set.
    :return: None
    """
    driver = webdriver.Chrome()

    driver.maximize_window()

    driver.get(url)

    check_cookie(driver)

    first_dropdown_xpath = '//*[@id="gatsby-focus-wrapper"]/div/div[2]/div[2]/div[7]/div[11]/div[1]/div/div[1]/div'

    path_exist: bool = check_if_path_exist(driver, first_dropdown_xpath, character_name)

    if path_exist:

        level_result_xpath = '//*[@id="gatsby-focus-wrapper"]/div/div[2]/div[2]/div[7]/div[12]/div[1]/div'

        store = []
        levels = ["Level 1", "Level 20", "Level 30", "Level 40", "Level 50", "Level 60", "Level 70", "Level 80"]

        for level in levels:
            click_drop_down(driver, first_dropdown_xpath)
            click_level(driver, level)
            extract_all_visible_text(driver, store, level, level_result_xpath, first_dropdown_xpath)

        create_excel.create_excel(store, first_output_path)

        driver.quit()

        calculate_hsr.save_to_excel(first_output_path, second_output_path)
    else:
        driver.quit()


def enter_input() -> list[str]:
    """
    Prompts the user to enter URLs and returns a list of valid URLs.
    The user can enter '1' to finish entering URLs.
    :return: A list of valid URLs entered by the user.
    """
    user_input_list = []

    while True:
        user_input: str = input('Enter URL (press 1 to finish): ')

        # Check if the input is empty after stripping whitespaces
        if not user_input.strip():
            print('You entered nothing. Please enter a valid URL or press 1 to finish.')
            continue

        if user_input == '1':
            break

        # Additional check to ensure the user enters a valid URL
        if not validate_url(user_input):
            print('Invalid URL. Please enter a valid URL or press 1 to finish.')
            continue

        user_input_list.append(user_input)

    return user_input_list


if __name__ == '__main__':
    pass
