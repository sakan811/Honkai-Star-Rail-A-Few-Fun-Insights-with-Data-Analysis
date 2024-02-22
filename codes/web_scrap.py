"""
This script performs web scraping of HSR character stats from the https://www.prydwen.gg/star-rail/ website.
"""
import os
import re
from selenium.common import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from validators import url as validate_url

import calculate_hsr
import create_excel

script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)


def click_drop_down(driver, first_dropdown_xpath: str) -> None:
    """

    :param driver: WebDriver instance
    :param first_dropdown_xpath: str
    :return: None
    """
    try:
        first_dropdown = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, first_dropdown_xpath)))
        first_dropdown_location = first_dropdown.location
        script = f"window.scrollTo({first_dropdown_location['x']}, {first_dropdown_location['y'] - 200});"
        driver.execute_script(script)
        first_dropdown.click()
    except TimeoutException:
        print("The first dropdown was not found within the specified timeout. Moving on.")


def click_level(driver, level: str) -> None:
    """

    :param driver: WebDriver instance
    :param level: str
    :return: None
    """
    level_xpath = f'//*[text()="{level}"]'
    # Attempt to click the element with a maximum number of retries
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            # Wait for the element to be present
            level_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, level_xpath)))
            level_element.click()
            # Break the loop if click is successful
            break
        except Exception as e:
            # If an exception occurs, scroll down and try again
            driver.execute_script("window.scrollBy(0, 100);")
            retries += 1
    else:
        print(f"Failed to click the element after {max_retries} retries.")


def extract_all_visible_text(driver, store: list, level: str, level_result_xpath: str,
                             first_dropdown_xpath: str) -> None:
    """

    :param driver: WebDriver instance
    :param store: list
    :param level: str
    :param level_result_xpath: str
    :param first_dropdown_xpath: str
    :return: None
    """
    # Find and extract all visible text in the specified path
    level_result_element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, level_result_xpath)))

    level_text: str = str(level_result_element.text)  # Convert to string

    level_is_correct: bool = check_level(level_text, level)

    if level_is_correct:
        store.append(level_text)
    else:
        click_drop_down(driver, first_dropdown_xpath)


def check_level(level_result_text: str, level: str) -> bool:
    # Use regular expression to find the current level in the lines
    current_level_match = re.search(r'Level \d+', level_result_text)

    # Check if a match is found
    if current_level_match:
        # Extract the matched level
        current_level: str = current_level_match.group()

        # Compare the extracted level with the provided level
        if current_level != level:
            return False  # Return False if the levels do not match
        else:
            return True  # Return True if the levels match
    else:
        return False  # Return False if no match is found


def extract_char_name(url: str) -> str:
    # Split the URL using '/'
    url_parts: list[str] = url.split('/')

    # Take the last element as the character name
    char_name: str = url_parts[-1]

    return char_name


def check_cookie(driver) -> None:
    """
    Check if the cookie consent dialog is present and handle it accordingly.

    Args:
        driver: The WebDriver instance.
    """
    # Check if the cookie consent dialog is present
    cookie_dialog_xpath = '//*[@id="qc-cmp2-ui"]'

    try:
        cookie_dialog = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, cookie_dialog_xpath)))

        # If the cookie consent dialog is present, click on the specified element
        if cookie_dialog.is_displayed():
            agree_button_xpath = '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]/span'
            agree_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, agree_button_xpath)))
            agree_button.click()

    except TimeoutException:
        # Handle the case where the dialog is not present or not displayed within the timeout
        logging.error("Cookie consent dialog not found or not displayed. Moving on.")

    except NoSuchElementException:
        # Handle the case where the agree button is not found
        logging.error("Agree button not found. Moving on.")


def check_if_path_exist(driver, first_dropdown_xpath: str, hsr_name: str) -> bool:
    """

    :param driver: WebDriver
    :param first_dropdown_xpath: str
    :param hsr_name: str
    :return: bool
    """
    try:
        driver.find_element(By.XPATH, first_dropdown_xpath)
        return True
    except Exception:
        print(f'{hsr_name}: first_dropdown_xpath not found')
        return False


def scrape(url: str) -> None:
    # Extract the character name from the URL
    hsr_name: str = extract_char_name(url)
    output_name = f"/hsr/{hsr_name}.xlsx"

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()

    # Maximize the browser window to full-screen
    driver.maximize_window()

    # Open the webpage
    driver.get(url)

    check_cookie(driver)

    first_dropdown_xpath = '//*[@id="gatsby-focus-wrapper"]/div/div[2]/div[2]/div[6]/div[11]/div[1]/div/div[1]/div'

    path_exist = check_if_path_exist(driver, first_dropdown_xpath, hsr_name)

    if path_exist:

        level_result_xpath = '//*[@id="gatsby-focus-wrapper"]/div/div[2]/div[2]/div[6]/div[12]/div[1]/div'

        store = []
        levels = ["Level 1", "Level 20", "Level 30", "Level 40", "Level 50", "Level 60", "Level 70", "Level 80"]

        for level in levels:
            click_drop_down(driver, first_dropdown_xpath)
            click_level(driver, level)
            extract_all_visible_text(driver, store, level, level_result_xpath, first_dropdown_xpath)

        create_excel.create_excel(store, output_name)

        # Close the browser window
        driver.quit()

        # Call the main function from 'calculate_hsr.py'
        calculate_hsr.main(output_name, hsr_name)
    else:
        driver.quit()


def enter_input() -> list[str]:
    """
    Prompts the user to enter URLs and returns a list of valid URLs.
    The user can enter '1' to finish entering URLs.
    """
    user_input_list = []

    while True:
        user_input: str = input('Enter URL (press 1 to finish): ')

        if not user_input.strip():  # Check if the input is empty after stripping whitespaces
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
