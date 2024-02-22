"""
This script adds growth-related stat columns to an Excel file for each HSR character.

The script functionality:
1. Reads an input Excel file.
2. Calculates growth values for Attack (ATK), Defense (DEF), HP, and Speed columns.
3. Saves the modified DataFrame to a new Excel file in the 'hsr_updated' directory.
"""

import pandas as pd


def calculate(df) -> None:
    """

    :param df: DataFrame instance
    :return: None
    """
    # Add a new column for Attack (ATK) growth with NaN values
    df["ATK Growth"] = [0] + [(df["ATK"].iloc[i] - df["ATK"].iloc[i - 1]) for i in range(1, len(df))]

    # Add a new column for Attack (ATK) growth percentage with NaN values
    df["ATK Growth %"] = [0] + [((df["ATK"].iloc[i] - df["ATK"].iloc[i - 1]) / df["ATK"].iloc[i - 1]) for i in range(1, len(df))]

    # Add a new column for Defense (DEF) growth with NaN values
    df["DEF Growth"] = [0] + [(df["DEF"].iloc[i] - df["DEF"].iloc[i - 1]) for i in range(1, len(df))]

    # Add a new column for Defense (DEF) growth percentage with NaN values
    df["DEF Growth %"] = [0] + [((df["DEF"].iloc[i] - df["DEF"].iloc[i - 1]) / df["DEF"].iloc[i - 1]) for i in range(1, len(df))]

    # Add a new column for HP growth with NaN values
    df["HP Growth"] = [0] + [(df["HP"].iloc[i] - df["HP"].iloc[i - 1]) for i in range(1, len(df))]

    # Add a new column for HP growth percentage with NaN values
    df["HP Growth %"] = [0] + [((df["HP"].iloc[i] - df["HP"].iloc[i - 1]) / df["HP"].iloc[i - 1]) for i in range(1, len(df))]

    # Add a new column for Speed growth with NaN values
    df["Speed Growth"] = [0] + [(df["Speed"].iloc[i] - df["Speed"].iloc[i - 1]) for i in range(1, len(df))]

    # Add a new column for Speed growth percentage with NaN values
    df["Speed Growth %"] = [0] + [((df["Speed"].iloc[i] - df["Speed"].iloc[i - 1]) / df["Speed"].iloc[i - 1]) for i in range(1, len(df))]


def main(file_path: str, hsr_name: str) -> None:
    df = pd.read_excel(file_path)

    calculate(df)

    # Save the modified DataFrame to a new Excel file in the 'hsr_updated' directory
    df.to_excel(f"/hsr/hsr_updated/{hsr_name}.xlsx", index=False)


if __name__ == '__main__':
    pass
