"""
This script adds growth-related stat columns to an Excel file for each HSR character.

The script functionality:
1. Reads an input Excel file.
2. Calculates growth values for Attack (ATK), Defense (DEF), HP, and Speed columns.
3. Saves the modified DataFrame to a new Excel file in the 'hsr_updated' directory.
"""
from loguru import logger

import pandas as pd
from pandas import DataFrame


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

def save_to_excel(input_excel_file_path: str, output_path: str) -> None:
    """
    Save the processed file to Excel to the specified directory.
    :param input_excel_file_path: The file path of the input Excel file.
    :param output_path: The file path where the modified Excel data will be saved.
    :return:
    """

    def calculate(df: DataFrame) -> None:
        """
        Calculates growth values for Attack (ATK), Defense (DEF), HP, and Speed columns.
        :param df: The DataFrame containing the data.
        :return: None
        """
        logger.info('Calculating additional columns...')

        # Add a new column for Attack (ATK) growth with NaN values
        df["ATK Growth"] = [0] + [(df["ATK"].iloc[i] - df["ATK"].iloc[i - 1]) for i in range(1, len(df))]

        # Add a new column for Attack (ATK) growth percentage with NaN values
        df["ATK Growth %"] = [0] + [((df["ATK"].iloc[i] - df["ATK"].iloc[i - 1]) / df["ATK"].iloc[i - 1]) for i in
                                    range(1, len(df))]

        # Add a new column for Defense (DEF) growth with NaN values
        df["DEF Growth"] = [0] + [(df["DEF"].iloc[i] - df["DEF"].iloc[i - 1]) for i in range(1, len(df))]

        # Add a new column for Defense (DEF) growth percentage with NaN values
        df["DEF Growth %"] = [0] + [((df["DEF"].iloc[i] - df["DEF"].iloc[i - 1]) / df["DEF"].iloc[i - 1]) for i in
                                    range(1, len(df))]

        # Add a new column for HP growth with NaN values
        df["HP Growth"] = [0] + [(df["HP"].iloc[i] - df["HP"].iloc[i - 1]) for i in range(1, len(df))]

        # Add a new column for HP growth percentage with NaN values
        df["HP Growth %"] = [0] + [((df["HP"].iloc[i] - df["HP"].iloc[i - 1]) / df["HP"].iloc[i - 1]) for i in
                                   range(1, len(df))]

        # Add a new column for Speed growth with NaN values
        df["Speed Growth"] = [0] + [(df["Speed"].iloc[i] - df["Speed"].iloc[i - 1]) for i in range(1, len(df))]

        # Add a new column for Speed growth percentage with NaN values
        df["Speed Growth %"] = [0] + [((df["Speed"].iloc[i] - df["Speed"].iloc[i - 1]) / df["Speed"].iloc[i - 1]) for i
                                      in
                                      range(1, len(df))]

    logger.info('Saving to Excel...')

    logger.info(f'Read the Excel from {input_excel_file_path = }')
    df = pd.read_excel(input_excel_file_path)

    logger.info('Calculates growth values for Attack (ATK), Defense (DEF), HP, and Speed columns.'
                'Add them as additional columns.')
    calculate(df)

    logger.info(f'Save the processed Excel to {output_path = }')
    df.to_excel(output_path, index=False)


if __name__ == '__main__':
    pass
