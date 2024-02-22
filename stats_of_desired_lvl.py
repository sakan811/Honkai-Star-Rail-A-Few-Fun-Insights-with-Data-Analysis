"""
This script processes Excel files in a specified directory, extracts all stats from the desired character's level,
and combines the extracted data into a new Excel file.
"""

import os
import pandas as pd


def process_excel_files(input_directory: str, output_file: str, desired_level: int) -> None:
    # Create an empty DataFrame to store the extracted data
    processed_data = pd.DataFrame()

    # Iterate through each file in the specified directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".xlsx"):
            # Extract the file name (without extension)
            char_name: str = os.path.splitext(filename)[0]

            # Load the Excel file into a DataFrame
            file_path: str = os.path.join(input_directory, filename)
            df = pd.read_excel(file_path)

            # Use boolean indexing to extract data from the row with the desired level
            row_with_desired_level = df[df['Level'] == desired_level]

            # Extract the data from the specified columns in the found row
            hp_data = row_with_desired_level['HP'].values[0] if not row_with_desired_level.empty else None
            def_data = row_with_desired_level['DEF'].values[0] if not row_with_desired_level.empty else None
            atk_data = row_with_desired_level['ATK'].values[0] if not row_with_desired_level.empty else None
            spd_data = row_with_desired_level['Speed'].values[0] if not row_with_desired_level.empty else None
            # Create a new DataFrame with the extracted data and file name
            file_data = pd.DataFrame({
                'Character': [char_name],
                f'HP (Level {desired_level})': [hp_data],
                f'DEF (Level {desired_level})': [def_data],
                f'ATK (Level {desired_level})': [atk_data],
                f'Speed (Level {desired_level})': [spd_data],
            })

            # Append the new DataFrame to the processed_data DataFrame
            processed_data = pd.concat([processed_data, file_data], ignore_index=True)

    # Save the processed data to a new Excel file
    processed_data.to_excel(output_file, index=False)


def main() -> None:
    desired_level = 20
    input_directory = 'hsr/hsr_updated'
    output_file = f'stats_as_lvl_{desired_level}_data.xlsx'
    process_excel_files(input_directory, output_file, desired_level)


if __name__ == '__main__':
    main()