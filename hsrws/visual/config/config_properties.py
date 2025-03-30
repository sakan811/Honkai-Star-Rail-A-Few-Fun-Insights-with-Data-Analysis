"""Property getter methods for chart configuration."""

from typing import Dict, Tuple, Any


def get_font_size(self, size_type: str, chart_type: str) -> int:
    """
    Get the font size for a specific chart type, applying chart-specific scaling.

    Args:
        size_type: Type of font size ('title', 'label', 'tick', 'annotation', 'legend')
        chart_type: Type of chart to get font size for

    Returns:
        Integer with calculated font size
    """
    # Get base font size
    if size_type == "title":
        base_size = self.title_fontsize
    elif size_type == "label":
        base_size = self.label_fontsize
    elif size_type == "tick":
        base_size = self.tick_fontsize
    elif size_type == "annotation":
        base_size = self.annotation_fontsize
    elif size_type == "legend":
        base_size = self.legend_fontsize
    else:
        return self.base_fontsize  # Default fallback

    # Apply chart-specific scaling if available
    chart_scales = self.font_scale_by_chart.get(chart_type, {})
    scale_factor = chart_scales.get(size_type, 1.0)

    return int(base_size * scale_factor)


def get_size(self, chart_type: str) -> Tuple[int, int]:
    """
    Get the figure size for a specific chart type.

    Args:
        chart_type: Type of chart to get size for.

    Returns:
        Tuple with figure dimensions (width, height).
    """
    return self.chart_sizes.get(chart_type, self.figure_size)


def get_colormap(self, chart_type: str) -> str:
    """
    Get the colormap for a specific chart type.

    Args:
        chart_type: Type of chart to get colormap for.

    Returns:
        String with colormap name.
    """
    return self.colormaps.get(chart_type, "viridis")


def get_title(self, chart_type: str) -> str:
    """
    Get the default title for a specific chart type.

    Args:
        chart_type: Type of chart to get title for.

    Returns:
        String with default title.
    """
    return self.default_titles.get(chart_type, "")


def get_grid_settings(self, chart_type: str) -> Dict[str, Any]:
    """
    Get the grid settings for a specific chart type.

    Args:
        chart_type: Type of chart to get grid settings for.

    Returns:
        Dictionary with grid settings.
    """
    return self.grid_settings.get(chart_type, {"visible": False})


def get_legend_settings(self, chart_type: str) -> Dict[str, Any]:
    """
    Get the legend settings for a specific chart type.

    Args:
        chart_type: Type of chart to get legend settings for.

    Returns:
        Dictionary with legend settings.
    """
    return self.legend_settings.get(chart_type, {})


def get_annotation_settings(self, chart_type: str) -> Dict[str, Any]:
    """
    Get the annotation settings for a specific chart type.

    Args:
        chart_type: Type of chart to get annotation settings for.

    Returns:
        Dictionary with annotation settings.
    """
    return self.annotation_settings.get(chart_type, {})


def get_marker_settings(
    self, chart_type: str, marker_type: str = "primary"
) -> Dict[str, Any]:
    """
    Get the marker settings for a specific chart type.

    Args:
        chart_type: Type of chart to get marker settings for.
        marker_type: Type of marker (primary or secondary).

    Returns:
        Dictionary with marker settings.
    """
    chart_markers = self.marker_settings.get(chart_type, {})
    return chart_markers.get(marker_type, {})
