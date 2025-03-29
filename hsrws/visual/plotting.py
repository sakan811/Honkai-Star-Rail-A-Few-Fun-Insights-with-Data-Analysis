"""Plotting functions for HSR data visualization."""

import matplotlib.pyplot as plt
import pandas as pd
from loguru import logger


def plot_character_stats(df: pd.DataFrame, stat_column: str) -> None:
    """
    Plot character stats as a bar chart.

    Args:
        df: DataFrame containing character data.
        stat_column: Column name of the stat to plot.
    """
    logger.debug(f"Plotting character stats for {stat_column}...")
    fig, ax = plt.subplots(figsize=(12, 8))

    # Sort by the stat value for better visualization
    sorted_df = df.sort_values(by=stat_column, ascending=False)

    # Create bar chart
    ax.bar(sorted_df["Character"], sorted_df[stat_column])

    # Set labels and title
    ax.set_xlabel("Character")
    ax.set_ylabel(stat_column)
    ax.set_title(f"Character {stat_column} Comparison")

    # Rotate x-labels for better readability
    plt.xticks(rotation=90)

    plt.tight_layout()
    plt.show()


def plot_element_distribution(df: pd.DataFrame) -> None:
    """
    Plot element distribution as a pie chart.

    Args:
        df: DataFrame containing character data.
    """
    logger.debug("Plotting element distribution...")
    fig, ax = plt.subplots(figsize=(10, 10))

    # Count elements
    element_counts = df["Element"].value_counts()

    # Create pie chart
    ax.pie(
        element_counts,
        labels=element_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        shadow=True,
    )

    ax.set_title("Character Element Distribution")
    plt.tight_layout()
    plt.show()


def plot_path_distribution(df: pd.DataFrame) -> None:
    """
    Plot path distribution as a pie chart.

    Args:
        df: DataFrame containing character data.
    """
    logger.debug("Plotting path distribution...")
    fig, ax = plt.subplots(figsize=(10, 10))

    # Count paths
    path_counts = df["Path"].value_counts()

    # Create pie chart
    ax.pie(
        path_counts,
        labels=path_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        shadow=True,
    )

    ax.set_title("Character Path Distribution")
    plt.tight_layout()
    plt.show()
