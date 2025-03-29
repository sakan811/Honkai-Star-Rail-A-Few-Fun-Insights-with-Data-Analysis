"""Chart creation functionality."""

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from loguru import logger

from hsrws.visual.config import ChartConfig
from hsrws.visual.data_utils import (
    get_latest_patch,
    get_path_distribution,
    get_element_distribution,
    get_rarity_distribution
)
from hsrws.visual.donut import create_donut_chart


def create_chart(data, title, cmap, filename, config):
    """
    Creates and saves a donut chart.
    
    Args:
        data: DataFrame with 'category' and 'count' columns.
        title: Chart title.
        cmap: Color map to use.
        filename: Output filename.
        config: Chart configuration object.
    """
    # Ensure visualization directories exist
    os.makedirs("visual", exist_ok=True)
    os.makedirs("visual/visual_img", exist_ok=True)
    
    fig, ax = plt.subplots(figsize=config.figure_size)
    create_donut_chart(ax, data, title, cmap, config)
    
    if config.tight_layout:
        plt.tight_layout()
    
    plt.savefig(
        os.path.join("visual", "visual_img", filename), 
        bbox_inches=config.bbox_inches, 
        dpi=config.dpi
    )
    plt.close()


def create_all_charts():
    """Creates all the donut charts for character distributions."""
    # Set seaborn style
    sns.set_theme(style="whitegrid")
    
    # Initialize chart configuration
    config = ChartConfig()
    
    # Get the latest patch version
    latest_patch = get_latest_patch()
    patch_info = f"(Latest Patch: {latest_patch})"
    
    # Fetch data using data utility functions
    path_data = get_path_distribution()
    element_data = get_element_distribution()
    rarity_data = get_rarity_distribution()

    # Create individual donut charts
    create_chart(
        path_data,
        f"Honkai Star Rail: Character Distribution by Path {patch_info}",
        config.path_cmap,
        "path_distribution.png",
        config
    )
    
    create_chart(
        element_data,
        f"Honkai Star Rail: Character Distribution by Element {patch_info}",
        config.element_cmap,
        "element_distribution.png",
        config
    )
    
    create_chart(
        rarity_data,
        f"Honkai Star Rail: Character Distribution by Rarity {patch_info}",
        config.rarity_cmap,
        "rarity_distribution.png",
        config
    )

    logger.info(f"Donut charts have been created in the 'visual/visual_img' directory for patch {latest_patch}.") 