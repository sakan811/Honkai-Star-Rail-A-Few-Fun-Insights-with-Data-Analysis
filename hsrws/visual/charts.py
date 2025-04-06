"""Chart creation functionality."""

import os
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import seaborn as sns
from loguru import logger
import io
from PIL import Image

from hsrws.visual.config import ChartConfig
from hsrws.visual.data_utils import (
    get_latest_patch,
    get_element_path_heatmap_data,
    get_rarity_element_distribution_data,
    get_version_release_timeline_data,
    get_element_balance_evolution_data,
    get_path_rarity_distribution_data,
)
from hsrws.visual.plotting import (
    plot_element_path_heatmap,
    plot_rarity_element_distribution,
    plot_version_release_timeline,
    plot_element_balance_evolution,
    plot_path_rarity_distribution,
)


def save_figure(fig: Figure, filename: str, config: ChartConfig):
    """
    Saves a matplotlib figure to file with a 1:1 aspect ratio.

    Args:
        fig: Matplotlib figure to save.
        filename: Output filename.
        config: Chart configuration object.
    """
    # Ensure visualization directories exist
    os.makedirs("hsrws/visual/visual_img", exist_ok=True)

    # Save original figure to a BytesIO buffer
    buf = io.BytesIO()
    fig.savefig( # type: ignore
        buf,
        format="png",
        bbox_inches=config.bbox_inches,
        dpi=config.dpi,
        facecolor="white",
    )
    buf.seek(0)

    # Open the image with PIL
    img = Image.open(buf)

    # Get dimensions
    width, height = img.size
    max_dim = max(width, height)

    # Create a square white image
    square_img = Image.new("RGBA", (max_dim, max_dim), (255, 255, 255, 255))

    # Calculate position to center the original image
    paste_x = (max_dim - width) // 2
    paste_y = (max_dim - height) // 2

    # Paste the original image onto the square canvas
    square_img.paste(img, (paste_x, paste_y))

    # Save the square image
    output_path = os.path.join("hsrws", "visual", "visual_img", filename)
    square_img.save(output_path)

    # Close the figure
    plt.close(fig)


def create_advanced_charts():
    """Creates all the advanced charts for character insights."""
    # Set seaborn style
    sns.set_theme(style="whitegrid")

    # Initialize chart configuration with 1:1 ratio
    config = ChartConfig()

    # Get the latest patch version
    latest_patch = get_latest_patch()

    # Create element-path heatmap
    element_path_data = get_element_path_heatmap_data()
    element_path_fig = plot_element_path_heatmap(
        element_path_data, config, latest_patch
    )
    save_figure(element_path_fig, "element_path_heatmap.png", config)

    # Create rarity-element stacked bar chart
    rarity_element_data = get_rarity_element_distribution_data()
    rarity_element_fig = plot_rarity_element_distribution(
        rarity_element_data, config, latest_patch
    )
    save_figure(rarity_element_fig, "rarity_element_distribution.png", config)

    # Create version release timeline
    version_release_data = get_version_release_timeline_data()
    version_release_fig = plot_version_release_timeline(
        version_release_data, config, latest_patch
    )
    save_figure(version_release_fig, "version_release_timeline.png", config)

    # Create elemental balance evolution area chart
    element_evolution_data = get_element_balance_evolution_data()
    element_evolution_fig = plot_element_balance_evolution(
        element_evolution_data, config, latest_patch
    )
    save_figure(element_evolution_fig, "element_balance_evolution.png", config)

    # Create path-rarity grouped bar chart
    path_rarity_data = get_path_rarity_distribution_data()
    path_rarity_fig = plot_path_rarity_distribution(
        path_rarity_data, config, latest_patch
    )
    save_figure(path_rarity_fig, "path_rarity_distribution.png", config)

    logger.info(
        f"Advanced insight charts have been created in the 'hsrws/visual/visual_img' directory for {latest_patch}."
    )
