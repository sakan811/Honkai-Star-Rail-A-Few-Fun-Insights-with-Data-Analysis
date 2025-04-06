"""Payload utilities for API interactions."""

import os
from typing import Any

from loguru import logger


async def get_payload(page_num: int) -> dict[str, Any]:
    """
    Gets payload with specified page number.

    Args:
        page_num: Page number.

    Returns:
        Dictionary with payload data.
    """
    logger.info(f"Getting payload for page {page_num}...")
    return {
        "filters": [],
        "menu_id": "104",
        "page_num": page_num,
        "page_size": 30,
        "use_es": True,
    }


def get_headers() -> dict[str, Any]:
    """
    Gets headers for API requests.

    Returns:
        Headers as Dictionary.
    """
    logger.info("Getting headers...")
    return {
        "Origin": "https://wiki.hoyolab.com",
        "Referer": "https://wiki.hoyolab.com/",
        "User-Agent": os.getenv("USER_AGENT"),
        "X-Rpc-Language": "en-us",
        "X-Rpc-Wiki_app": "hsr",
    }


def default_char_data_dict() -> dict[str, list[Any]]:
    """
    Creates a default character data dictionary with empty lists.

    Returns:
        Dictionary with empty lists for each character attribute.
    """
    return {
        "Character": [],
        "Path": [],
        "Element": [],
        "Rarity": [],
        "ATK Lvl 80": [],
        "DEF Lvl 80": [],
        "HP Lvl 80": [],
        "SPD Lvl 80": [],
    }


def get_first_value(
    data: dict[str, Any], *keys: str, default: Any = None
) -> str | int | None:
    """
    Retrieves the first value from a nested dictionary structure.

    Searches for the first non-empty value in the 'values' list of the specified
    keys in the given data dictionary.

    Args:
        data: The dictionary to search in
        keys: Variable number of keys to search for
        default: Value to return if no value is found, defaults to None

    Returns:
        The first non-empty value found, or the default value

    Raises:
        KeyError: If a specified key exists in data but doesn't have a 'values' key
    """
    for key in keys:
        if key in data:
            values = data[key]["values"]
            if values:
                return values[0]
    return default
