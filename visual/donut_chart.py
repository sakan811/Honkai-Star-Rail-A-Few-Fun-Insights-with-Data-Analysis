import os
from loguru import logger
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sqlalchemy import create_engine, text
from dataclasses import dataclass

DB_PATH = "hsr.db"

# Create visual directory if it doesn't exist
os.makedirs("visual", exist_ok=True)
os.makedirs("visual/visual_img", exist_ok=True)

# Set seaborn style
sns.set_theme(style="whitegrid")


@dataclass
class ChartConfig:
    """Configuration for donut charts."""
    # Chart dimensions
    figure_size: tuple = (10, 10)
    dpi: int = 150
    
    # Donut properties
    donut_width: float = 0.5
    donut_hole_radius: float = 0.4
    
    # Text sizes
    title_fontsize: int = 14
    title_pad: int = 20
    center_text_fontsize: int = 20
    label_fontsize: int = 10
    pct_fontsize: int = 8
    count_fontsize: int = 8
    
    # Color maps
    path_cmap: str = "Blues"
    element_cmap: str = "Spectral"
    rarity_cmap: str = "Reds"
    
    # Positioning
    pct_distance: float = 0.85
    
    # Output configuration
    tight_layout: bool = True
    bbox_inches: str = 'tight'


def fetch_data(query):
    """Fetch data from the database using the provided query with SQLAlchemy."""
    engine = create_engine(f"sqlite:///{DB_PATH}")
    with engine.connect() as conn:
        return pd.read_sql_query(text(query), conn)


def get_latest_patch():
    """Get the latest patch version from the database."""
    query = """
    SELECT MAX(Version) as latest_version
    FROM HsrCharacters
    """
    result = fetch_data(query)
    return result.iloc[0]['latest_version']


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
    
    # Query for Path distribution
    path_query = """
    SELECT Path as category, COUNT(*) as count
    FROM HsrCharacters
    GROUP BY Path
    ORDER BY count DESC
    """

    # Query for Element distribution
    element_query = """
    SELECT Element as category, COUNT(*) as count
    FROM HsrCharacters
    GROUP BY Element
    ORDER BY count DESC
    """

    # Query for Rarity distribution
    rarity_query = """
    SELECT Rarity as category, COUNT(*) as count
    FROM HsrCharacters
    GROUP BY Rarity
    ORDER BY count DESC
    """

    # Fetch all data
    path_data = fetch_data(path_query)
    element_data = fetch_data(element_query)
    rarity_data = fetch_data(rarity_query)

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
