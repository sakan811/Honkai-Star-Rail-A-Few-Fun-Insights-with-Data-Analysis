import os
from loguru import logger
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from config import ChartConfig
from data_utils import (
    get_latest_patch,
    get_path_distribution,
    get_element_distribution,
    get_rarity_distribution
)

# Create visual directory if it doesn't exist
os.makedirs("visual", exist_ok=True)
os.makedirs("visual/visual_img", exist_ok=True)

# Set seaborn style
sns.set_theme(style="whitegrid")


def create_donut_chart(ax, data, title, cmap, config):
    """Create a donut chart on the given axes using the provided configuration."""
    # Create a pie chart with a hole in the middle (donut chart)
    wedges, texts, autotexts = ax.pie(
        data["count"],
        labels=data["category"],
        autopct="%1.1f%%",
        textprops={"fontsize": config.label_fontsize},
        wedgeprops={"width": config.donut_width, "edgecolor": "w"},
        pctdistance=config.pct_distance,
        colors=sns.color_palette(cmap, len(data)),
    )

    # Style the chart
    plt.setp(autotexts, size=config.pct_fontsize, weight="bold")
    plt.setp(texts, size=config.label_fontsize)

    # Add a circle at the center to create the donut hole
    centre_circle = plt.Circle((0, 0), config.donut_hole_radius, fc="white")
    ax.add_patch(centre_circle)

    # Add total count in the center
    total = data["count"].sum()
    ax.text(
        0,
        0,
        f"Total\n{total}",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=config.center_text_fontsize,
        fontweight="bold",
    )

    # Add data labels for each slice
    for i, (wedge, category, count) in enumerate(
        zip(wedges, data["category"], data["count"])
    ):
        ang = (wedge.theta2 - wedge.theta1) / 2.0 + wedge.theta1
        x = 0.75 * 0.5 * np.cos(np.deg2rad(ang))
        y = 0.75 * 0.5 * np.sin(np.deg2rad(ang))
        ax.annotate(
            f"{count}",
            xy=(x, y),
            xytext=(0, 0),
            textcoords="offset points",
            ha="center",
            va="center",
            fontsize=config.count_fontsize,
            fontweight="bold",
        )

    # Add title
    ax.set_title(title, fontsize=config.title_fontsize, pad=config.title_pad)


def create_chart(data, title, cmap, filename, config):
    """Create and save a donut chart based on the provided configuration."""
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


def main():
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


if __name__ == "__main__":
    main()
