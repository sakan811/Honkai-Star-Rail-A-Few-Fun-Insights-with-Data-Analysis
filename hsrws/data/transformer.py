"""Data transformation functions for HSR data."""

import re

import pandas as pd
from loguru import logger

from hsrws.utils.version import get_version_dict


def transform_char_name(char_name: str) -> str:
    """
    Transforms character name to a standard format.

    Args:
        char_name: Character name.

    Returns:
        Transformed character name.
    """
    logger.debug("Transforming character name...")

    # Define the non-breaking space character
    nbsp: str = "\u00a0"

    # Remove "(Coming Soon)"
    cleaned_char_name: str = char_name.replace(" (Coming Soon)", "")
    # Replace non-breaking spaces with regular spaces
    cleaned_char_name: str = cleaned_char_name.replace(nbsp, " ")
    # Remove symbols like '.', '•', and ':'
    cleaned_char_name: str = re.sub(r"[.•:]", "", cleaned_char_name)
    # Replace spaces with hyphens
    cleaned_char_name: str = cleaned_char_name.replace(" ", "-").lower()
    # Replace multiple hyphens with a single hyphen
    cleaned_char_name: str = re.sub(r"-+", "-", cleaned_char_name)
    # Ensure no name ends with a hyphen
    cleaned_char_name: str = cleaned_char_name.rstrip("-")
    return cleaned_char_name


def clean_path_name(path_name: str) -> str:
    """
    Cleans Path name by removing 'The ' prefix.

    Args:
        path_name: Path name.

    Returns:
        Cleaned Path name.
    """
    logger.debug("Cleaning Path name...")
    return path_name.replace("The ", "")


def add_char_version(df: pd.DataFrame) -> None:
    """
    Adds characters' version to dataframe.

    Args:
        df: Character Dataframe.
    """
    logger.debug("Adding character version...")
    version_and_character_dict: dict[int, list[str]] = get_version_dict()
    df["Version"] = df["Character"].apply(
        lambda character: next(
            (
                version
                for version, characters in version_and_character_dict.items()
                if character in characters
            ),
            1.0,
        )
    )
