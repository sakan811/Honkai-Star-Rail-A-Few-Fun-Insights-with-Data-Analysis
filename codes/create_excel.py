"""
For creating an Excel file and add data from the stats list into the file.
"""
import logging

import pandas as pd


def create_excel(stats_list: list, output_excel_file_path: str) -> None:
    """
    Create an Excel file and add data from the stats list into the file
    :param stats_list: A list that contains stats of the characters.
    :param output_excel_file_path: The desired path to save Excel files.
    :return: None
    """

    # Create a list of dictionaries to store the data
    level_data = []

    try:
        logging.info(f'Iterate through the \'stats_list\' and populate the list of dictionaries')
        for stat_str in stats_list:
            lines: str = stat_str.split('\n')
            logging.debug(f'{lines = }')
            current_level: int = int(lines[0].split()[1])
            logging.debug(f'{current_level = }')

            logging.info(f'Create a dictionary for the {current_level = }')
            level_dict = {"Level": current_level, "HP": None, "ATK": None, "DEF": None, "Speed": None}

            logging.info(f'Store the result of split() in a variable')
            stat_names: str = lines[1::2]
            logging.debug(f'{stat_names = }')
            stat_values: str = lines[2::2]
            logging.debug(f'{stat_values = }')

            logging.info(f'Zip {stat_names = } and {stat_values = } and loop through them '
                         f'to map them as key, value of the dictionary.')
            try:
                for stat_name, stat_value in zip(stat_names, stat_values):
                    level_dict[stat_name]: dict[str, int] = int(stat_value)
                    logging.debug(f'{level_dict[stat_name] = }: {stat_values = }')
            except Exception as e:
                logging.error(f'Error mapping \'stat_names\' and \'stat_values\' to dictionary: {e}')

            logging.info(f'Append the {level_dict = } to the list of dictionaries')
            level_data.append(level_dict)
    except Exception as e:
        logging.error(f'Error iterating through the \'stats_list\' and populate the list of dictionaries:'
                      f'{e}')

    logging.info(f'Create a DataFrame of \'level_data\'')
    df = pd.DataFrame(level_data)

    logging.info(f'Save the DataFrame to Excel at the {output_excel_file_path = }')
    df.to_excel(output_excel_file_path, index=False)


if __name__ == '__main__':
    pass
