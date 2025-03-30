"""Default chart settings for visualization module."""

from typing import Dict, Tuple, Any


def get_default_colormaps() -> Dict[str, str]:
    """Get default colormaps for each chart type."""
    return {
        "heatmap": "viridis",
        "bar": "tab10",
        "timeline": "tab10",
        "area": "tab10",
        "grouped_bar": "Paired",
    }


def get_default_titles() -> Dict[str, str]:
    """Get default titles for each chart type."""
    return {
        "heatmap": "Honkai: Star Rail Character Distribution by Element and Path",
        "bar": "Honkai: Star Rail Character Rarity Distribution with Element Breakdown",
        "timeline": "Honkai: Star Rail Character Introduction Rate by Version",
        "area": "Honkai: Star Rail Elemental Balance Evolution Across Versions",
        "grouped_bar": "Honkai: Star Rail Character Path Distribution by Rarity",
    }


def get_default_grid_settings() -> Dict[str, Dict[str, Any]]:
    """Get default grid settings for each chart type."""
    return {
        "timeline": {"visible": True, "linestyle": "--", "alpha": 0.7},
        "area": {"visible": True, "linestyle": "--", "alpha": 0.7},
        "grouped_bar": {"visible": True, "axis": "y", "linestyle": "--", "alpha": 0.7},
    }


def get_default_legend_settings() -> Dict[str, Dict[str, Any]]:
    """Get default legend settings for each chart type."""
    return {
        # For landscape charts (bar, timeline, area), position legend on the right side
        "bar": {
            "title": "Element",
            "bbox_to_anchor": (1.15, 0.5),
            "loc": "center left",
        },
        "area": {
            "title": "Element",
            "bbox_to_anchor": (1.15, 0.5),
            "loc": "center left",
        },
        "timeline": {
            "title": "Data Type",
            "bbox_to_anchor": (1.15, 0.5),
            "loc": "center left",
        },
        # For portrait chart (grouped_bar), position legend at the top
        "grouped_bar": {
            "title": "Rarity",
            "bbox_to_anchor": (0.5, 1.15),
            "loc": "lower center",
        },
    }


def get_default_annotation_settings() -> Dict[str, Dict[str, Any]]:
    """Get default annotation settings for each chart type."""
    return {
        "timeline": {
            "textcoords": "offset points",
            "xytext": (0, 15),  # Increased vertical offset
            "ha": "center",
            "fontsize_offset": 2,  # Add additional size increase
        },
        "grouped_bar": {
            "fmt": "%.0f",
            "padding": 5,
            "fontweight": "bold",  # Make annotations bold
        },
        "heatmap": {
            "fmt": ".0f",
            "fontweight": "bold",  # Make annotations bold
        },
    }


def get_default_marker_settings() -> Dict[str, Dict[str, Any]]:
    """Get default marker settings for each chart type."""
    return {
        "timeline": {
            "primary": {"marker": "o", "markersize": 8, "linewidth": 2},
            "secondary": {
                "marker": "s",
                "linestyle": "--",
                "color": "darkred",
                "alpha": 0.7,
                "markersize": 6,
            },
        }
    }
