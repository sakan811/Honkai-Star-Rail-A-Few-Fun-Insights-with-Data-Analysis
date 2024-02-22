"""
For creating Excel files.
"""

import pandas as pd


def create_excel(stats_list: list, output_name: str) -> None:
    """
    Create an Excel file from a list of stats.
    """

    # Create a list of dictionaries to store the data
    level_data = []

    # Iterate through the list and populate the list of dictionaries
    for stat_str in stats_list:
        lines: str = stat_str.split('\n')
        current_level: int = int(lines[0].split()[1])

        # Create a dictionary for the current level
        level_dict = {"Level": current_level, "HP": None, "ATK": None, "DEF": None, "Speed": None}

        # Store the result of split() in a variable
        stat_names: str = lines[1::2]
        stat_values: str = lines[2::2]

        for stat_name, stat_value in zip(stat_names, stat_values):
            level_dict[stat_name]: dict[str, int] = int(stat_value)

        # Append the level dictionary to the list of dictionaries
        level_data.append(level_dict)

    # Create a DataFrame
    df = pd.DataFrame(level_data)

    # Save the DataFrame to an Excel file
    df.to_excel(output_name, index=False)


if __name__ == '__main__':
    pass
