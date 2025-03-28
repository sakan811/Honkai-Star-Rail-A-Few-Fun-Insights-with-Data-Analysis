import os
from loguru import logger
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sqlalchemy import create_engine, text

DB_PATH = "hsr.db"

# Create visual directory if it doesn't exist
os.makedirs("visual", exist_ok=True)
os.makedirs("visual/visual_img", exist_ok=True)

# Set seaborn style
sns.set_theme(style="whitegrid")


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


def create_donut_chart(ax, data, title, cmap="viridis"):
    """Create a donut chart on the given axes."""
    # Create a pie chart with a hole in the middle (donut chart)
    wedges, texts, autotexts = ax.pie(
        data["count"],
        labels=data["category"],
        autopct="%1.1f%%",
        textprops={"fontsize": 10},
        wedgeprops={"width": 0.5, "edgecolor": "w"},
        pctdistance=0.85,
        colors=sns.color_palette(cmap, len(data)),
    )

    # Style the chart
    plt.setp(autotexts, size=8, weight="bold")
    plt.setp(texts, size=10)

    # Add a circle at the center to create the donut hole
    centre_circle = plt.Circle((0, 0), 0.4, fc="white")
    ax.add_patch(centre_circle)

    # Add total count in the center
    total = data["count"].sum()
    ax.text(
        0,
        0,
        f"Total\n{total}",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=20,
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
            fontsize=8,
            fontweight="bold",
        )

    # Add title
    ax.set_title(title, fontsize=14, pad=20)


def main():
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
    # Path distribution
    fig, ax = plt.subplots(figsize=(10, 10))
    create_donut_chart(
        ax,
        path_data,
        f"Honkai Star Rail: Character Distribution by Path {patch_info}",
        "Blues",
    )
    plt.tight_layout()
    plt.savefig(os.path.join("visual", "visual_img", "path_distribution.png"), bbox_inches='tight', dpi=150)
    plt.close()

    # Element distribution
    fig, ax = plt.subplots(figsize=(10, 10))
    create_donut_chart(
        ax,
        element_data,
        f"Honkai Star Rail: Character Distribution by Element {patch_info}",
        "Spectral",
    )
    plt.tight_layout()
    plt.savefig(os.path.join("visual", "visual_img", "element_distribution.png"), bbox_inches='tight', dpi=150)
    plt.close()

    # Rarity distribution
    fig, ax = plt.subplots(figsize=(10, 10))
    create_donut_chart(
        ax,
        rarity_data,
        f"Honkai Star Rail: Character Distribution by Rarity {patch_info}",
        "Reds",
    )
    plt.tight_layout()
    plt.savefig(os.path.join("visual", "visual_img", "rarity_distribution.png"), bbox_inches='tight', dpi=150)
    plt.close()

    logger.info(f"Donut charts have been created in the 'visual/visual_img' directory for patch {latest_patch}.")


if __name__ == "__main__":
    main()
