"""
This script performs web scraping of HSR character stats from the https://www.prydwen.gg/star-rail/ website.
"""

import re
from urllib.parse import urlparse
import pandas as pd
from selenium.common import TimeoutException, NoSuchElementException
import calculate_hsr as cal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import get_urls_auto as get_urls


def click_drop_down(driver, first_dropdown_xpath):
    try:
        first_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, first_dropdown_xpath)))
        first_dropdown.click()
    except TimeoutException:
        print("The first dropdown was not found within the specified timeout. Moving on.")


def click_level(driver, level):
    level_xpath = f'//*[text()="{level}"]'
    # Attempt to click the element with a maximum number of retries
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            # Wait for the element to be present
            level_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, level_xpath)))
            level_element.click()
            # Break the loop if click is successful
            break
        except Exception as e:
            # If an exception occurs, scroll down and try again
            driver.execute_script("window.scrollBy(0, 100);")
            retries += 1
    else:
        print(f"Failed to click the element after {max_retries} retries.")


def extract_all_visible_text(driver, store, level, level_result_xpath, first_dropdown_xpath):
    # Find and extract all visible text in the specified path
    level_result_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, level_result_xpath)))

    level_text = str(level_result_element.text)  # Convert to string

    level_is_correct = check_level(level_text, level)

    if level_is_correct:
        store.append(level_text)
    else:
        click_drop_down(driver, first_dropdown_xpath)


def check_level(level_result_text, level):
    # Use regular expression to find the current level in the lines
    current_level_match = re.search(r'Level \d+', level_result_text)

    # Check if a match is found
    if current_level_match:
        # Extract the matched level
        current_level = current_level_match.group()

        # Compare the extracted level with the provided level
        if current_level != level:
            return False  # Return False if the levels do not match
        else:
            return True  # Return True if the levels match
    else:
        return False  # Return False if no match is found


def create_excel(stats_list, output_name):
    # Create a dictionary to store the data
    data = {"Level": [], "HP": [], "ATK": [], "DEF": [], "Speed": []}

    # Iterate through the list and populate the dictionary
    for stat_str in stats_list:
        lines = stat_str.split('\n')
        current_level = int(lines[0].split()[1])

        # Create a dictionary for the current level
        level_data = {"Level": current_level, "HP": None, "ATK": None, "DEF": None, "Speed": None}

        for i in range(1, len(lines), 2):
            stat, value = lines[i], int(lines[i + 1])
            level_data[stat] = value

        # Append the level data to the main data dictionary
        for key, value in level_data.items():
            data[key].append(value)

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame to an Excel file
    df.to_excel(output_name, index=False)


def extract_char_name(url):
    # Split the URL using '/'
    url_parts = url.split('/')

    # Take the last element as the character name
    char_name = url_parts[-1]

    return char_name


def check_cookie(driver):
    # Check if the cookie consent dialog is present
    cookie_dialog_xpath = '//*[@id="qc-cmp2-ui"]'

    try:
        cookie_dialog = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, cookie_dialog_xpath)))

        # If the cookie consent dialog is present, click on the specified element
        if cookie_dialog.is_displayed():
            agree_button_xpath = '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]/span'
            agree_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, agree_button_xpath)))
            agree_button.click()

    except TimeoutException:
        # Handle the case where the dialog is not present or not displayed within the timeout
        print("Cookie consent dialog not found or not displayed. Moving on.")

    except NoSuchElementException:
        # Handle the case where the agree button is not found
        print("Agree button not found. Moving on.")


def check_if_path_exist(driver, first_dropdown_xpath, hsr_name):
    try:
        first_dropdown = driver.find_element(By.XPATH, first_dropdown_xpath)
        return True
    except Exception:
        print(f'{hsr_name}: first_dropdown_xpath not found')
        return False


def scrape(url):
    # Extract the character name from the URL
    hsr_name = extract_char_name(url)
    output_name = f"hsr/{hsr_name}.xlsx"

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

        create_excel(store, output_name)

        # Close the browser window
        driver.quit()

        # Call the main function from 'calculate_hsr.py'
        cal.main(output_name, hsr_name)
    else:
        driver.quit()


def enter_input():
    user_input_list = []

    while True:
        user_input = input('Enter URL (press 1 to finish): ')

        if not user_input.strip():  # Check if the input is empty after stripping whitespaces
            print('You entered nothing. Please enter a valid URL or press 1 to finish.')
            continue

        if user_input == '1':
            break

        if user_input.isdigit() and user_input != '1':
            print('Please enter a valid URL or press 1 to finish.')
            continue

        if not isinstance(user_input, str):
            print('Please enter a valid URL or press 1 to finish.')
            continue

        # Additional check to ensure the user enters a valid URL
        try:
            parsed_url = urlparse(user_input)
            if not (parsed_url.scheme and parsed_url.netloc):
                raise ValueError("Invalid URL")
        except ValueError:
            print('Invalid URL. Please enter a valid URL or press 1 to finish.')
            continue

        user_input_list.append(user_input)

    return user_input_list


def main():
    print('Automatically get urls: press 1')
    print('Manually get urls: press 2')

    while True:
        user_input = input('Enter number: ')

        if user_input == '1':
            user_input_list = get_urls.get_urls_auto()
            break
        elif user_input == '2':
            user_input_list = enter_input()
            break
        else:
            print('Invalid input. Please enter 1 or 2.')

    for url in user_input_list:
        scrape(url)


if __name__ == '__main__':
    main()
