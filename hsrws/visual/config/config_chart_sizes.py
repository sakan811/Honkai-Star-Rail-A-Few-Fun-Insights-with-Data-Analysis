"""Size and scaling settings for charts."""

from typing import Dict, Tuple, Any


def get_default_font_scale_by_chart() -> Dict[str, Dict[str, float]]:
    """Get default font scale factors for each chart type."""
    return {
        "heatmap": {
            "title": 1.1,  # Square format - increased title size
            "label": 1.05,  # Larger labels
            "tick": 1.0,  # Larger ticks to enhance readability
            "annotation": 1.0,  # Increased annotations for dense heatmap cells
            "legend": 1.0,  # Larger legend size
        },
        "bar": {
            "title": 0.8,  # Landscape format - larger title
            "label": 0.8,  # Larger label size
            "tick": 0.8,  # Larger ticks for horizontal layout
            "annotation": 0.8,  # Larger annotation size
            "legend": 0.8,  # Larger legend size
        },
        "timeline": {
            "title": 0.8,  # Landscape format - larger title
            "label": 0.8,  # Larger label size
            "tick": 0.8,  # Larger ticks for dense timeline
            "annotation": 0.8,  # Larger annotations for potential overlap
            "legend": 0.8,  # Larger legend size
        },
        "area": {
            "title": 0.8,  # Landscape format - larger title
            "label": 0.8,  # Larger label size
            "tick": 0.8,  # Larger ticks for version numbers
            "annotation": 0.8,  # Larger annotation size
            "legend": 0.8,  # Larger legend size
        },
        "grouped_bar": {
            "title": 1.0,  # Portrait format - larger title
            "label": 1.0,  # Larger labels for readability
            "tick": 1.0,  # Larger ticks for grouped bars
            "annotation": 1.0,  # Larger annotations to avoid overlap
            "legend": 1.0,  # Larger legend size
        },
    }


def get_default_chart_sizes() -> Dict[str, Tuple[int, int]]:
    """
    Get default chart sizes optimized for Instagram.

    Square ratio (1:1) - Default for Instagram feed: 1080px x 1080px
    Landscape ratio (1.91:1) - Landscape for Instagram: 1080px x 566px
    Portrait ratio (4:5) - Vertical for Instagram: 1080px x 1350px
    """
    return {
        # Heatmap - Square format (1:1) is ideal for heatmaps to maintain cell symmetry
        "heatmap": (10, 10),  # 1:1 ratio
        # Bar chart - Landscape format (1.91:1) works better for horizontal bars
        "bar": (10, 5.24),  # Close to 1.91:1 ratio
        # Timeline - Landscape format (1.91:1) works well for time series
        "timeline": (10, 5.24),  # Close to 1.91:1 ratio
        # Area chart - Landscape format (1.91:1) works well for evolution visualization
        "area": (10, 5.24),  # Close to 1.91:1 ratio
        # Grouped bar - Portrait format (4:5) works well for vertical comparisons
        "grouped_bar": (8, 10),  # Close to 4:5 ratio
    } 