"""
For creating an Excel file and add data from the stats list into the file.

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
import pandas as pd


def create_excel(stats_list: list, output_excel_file_path: str) -> None:
    """
    Create an Excel file and add data from the stats list into the file
    :param stats_list: A list that contains stats of the characters.
    :param output_excel_file_path: The desired path to save Excel files.
    :return: None
    """
    logger.info('Creating Excel...')

    # Create a list of dictionaries to store the data
    level_data = []

    try:
        logger.info(f'Iterate through the \'stats_list\' and populate the list of dictionaries')
        for stat_str in stats_list:
            lines: str = stat_str.split('\n')
            logger.debug(f'{lines = }')
            current_level: int = int(lines[0].split()[1])
            logger.debug(f'{current_level = }')

            logger.info(f'Create a dictionary for the {current_level = }')
            level_dict = {"Level": current_level, "HP": None, "ATK": None, "DEF": None, "Speed": None}

            logger.info(f'Store the result of split() in a variable')
            stat_names: str = lines[1::2]
            logger.debug(f'{stat_names = }')
            stat_values: str = lines[2::2]
            logger.debug(f'{stat_values = }')

            logger.info(f'Zip {stat_names = } and {stat_values = } and loop through them '
                        f'to map them as key, value of the dictionary.')
            try:
                for stat_name, stat_value in zip(stat_names, stat_values):
                    level_dict[stat_name]: dict[str, int] = int(stat_value)
                    logger.debug(f'{stat_name = }: {stat_value = }')
            except Exception as e:
                logger.error(f'Error mapping \'stat_names\' and \'stat_values\' to dictionary: {e}')

            logger.info(f'Append the {level_dict = } to the list of dictionaries')
            level_data.append(level_dict)
    except Exception as e:
        logger.error(f'Error iterating through the \'stats_list\' and populate the list of dictionaries:'
                     f'{e}')

    logger.info(f'Create a DataFrame of \'level_data\'')
    df = pd.DataFrame(level_data)

    logger.info(f'Save the DataFrame to Excel at the {output_excel_file_path = }')
    df.to_excel(output_excel_file_path, index=False)


if __name__ == '__main__':
    pass
