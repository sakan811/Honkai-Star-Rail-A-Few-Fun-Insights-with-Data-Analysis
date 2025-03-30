"""Character data processing logic."""

import json
from typing import Any, Optional

from loguru import logger

from hsrws.core.scraper import Scraper
from hsrws.utils.payload import get_first_value


async def process_character_list(scraper: Scraper, char_list: list[dict]) -> None:
    """
    Processes the character list.

    Args:
        scraper: Scraper instance to use for processing.
        char_list: List of characters to process.
    """
    for char in char_list:
        await scrape_character_data(scraper, char)


async def scrape_character_data(
    scraper: Scraper, character_data: dict[str, Any]
) -> None:
    """
    Scrapes character data from JSON response.

    Args:
        scraper: Scraper instance to use for processing.
        character_data: Dictionary that represents each character data.

    Raises:
        KeyError: If character name is not found.
    """
    try:
        character_name = character_data["name"]
    except KeyError as e:
        logger.error(f"Character name {e} is not found.")
        raise KeyError
    else:
        scraper.char_data_dict["Character"].append(character_name)
        await append_char_type_data(scraper, character_data)
        append_char_stats(scraper, character_data)


def append_char_stats(scraper: Scraper, character_data: dict[str, Any]) -> None:
    """
    Appends character stats to the character data dictionary.

    Args:
        scraper: Scraper instance to use for processing.
        character_data: Dictionary that represents each character data.
    """
    try:
        char_stats = character_data["display_field"]
        if not char_stats:
            append_stats(scraper)
        else:
            char_stats_lvl_80_json_str = char_stats["attr_level_80"]
            char_stats_lvl_80: dict[str, Any] = json.loads(char_stats_lvl_80_json_str)
            append_stats(scraper, char_stats_lvl_80)
    except KeyError as e:
        logger.error(f"Stats of Character name {e} is not found. Append stats as zero.")
        append_stats(scraper)


def append_stats(
    scraper: Scraper, char_stats_lvl_80: Optional[dict[str, Any]] = None
) -> None:
    """
    Appends stats to the character data dictionary.

    Args:
        scraper: Scraper instance to use for processing.
        char_stats_lvl_80: Character stats at level 80.
    """
    if char_stats_lvl_80:
        try:
            base_atk_lvl_80 = int(char_stats_lvl_80["base_atk"])
            scraper.char_data_dict["ATK Lvl 80"].append(base_atk_lvl_80)
        except KeyError as e:
            logger.error(f"KeyError: {e}. Appending 'base_atk_lvl_80' as zero.")
            scraper.char_data_dict["ATK Lvl 80"].append(0)

        try:
            base_def_lvl_80 = int(char_stats_lvl_80["base_def"])
            scraper.char_data_dict["DEF Lvl 80"].append(base_def_lvl_80)
        except KeyError as e:
            logger.error(f"KeyError: {e}. Appending 'base_def_lvl_80' as zero.")
            scraper.char_data_dict["DEF Lvl 80"].append(0)

        try:
            base_hp_lvl_80 = int(char_stats_lvl_80["base_hp"])
            scraper.char_data_dict["HP Lvl 80"].append(base_hp_lvl_80)
        except KeyError as e:
            logger.error(f"KeyError: {e}. Appending 'base_hp_lvl_80' as zero.")
            scraper.char_data_dict["HP Lvl 80"].append(0)

        try:
            base_speed_lvl_80 = int(char_stats_lvl_80["base_speed"])
            scraper.char_data_dict["SPD Lvl 80"].append(base_speed_lvl_80)
        except KeyError as e:
            logger.error(f"KeyError: {e}. Appending 'base_speed_lvl_80' as zero.")
            scraper.char_data_dict["SPD Lvl 80"].append(0)
    else:
        scraper.char_data_dict["ATK Lvl 80"].append(0)
        scraper.char_data_dict["DEF Lvl 80"].append(0)
        scraper.char_data_dict["HP Lvl 80"].append(0)
        scraper.char_data_dict["SPD Lvl 80"].append(0)


async def append_char_type_data(
    scraper: Scraper, character_data: dict[str, Any]
) -> None:
    """
    Appends character type data to the character data dictionary.

    Args:
        scraper: Scraper instance to use for processing.
        character_data: Dictionary that represents each character data.
    """
    try:
        filter_values = character_data.get("filter_values", {})

        # Extract path from character_paths
        path = get_first_value(filter_values, "character_paths", default="Unknown")

        # Extract element from character_combat_type
        element = get_first_value(
            filter_values, "character_combat_type", default="Unknown"
        )

        # Extract rarity from character_rarity
        rarity = get_first_value(filter_values, "character_rarity", default="Unknown")

        # Remove "The " prefix from path if present
        if isinstance(path, str) and path.startswith("The "):
            path = path[4:]

        # Remove "-Star" suffix from rarity if present
        if isinstance(rarity, str) and rarity.endswith("-Star"):
            rarity = rarity.split("-")[0]

        scraper.char_data_dict["Path"].append(path)
        scraper.char_data_dict["Element"].append(element)
        scraper.char_data_dict["Rarity"].append(rarity)
    except KeyError as e:
        logger.error(
            f"KeyError: {e}. Appending all path, element, and rarity as 'Unknown'."
        )
        scraper.char_data_dict["Path"].append("Unknown")
        scraper.char_data_dict["Element"].append("Unknown")
        scraper.char_data_dict["Rarity"].append("Unknown")
