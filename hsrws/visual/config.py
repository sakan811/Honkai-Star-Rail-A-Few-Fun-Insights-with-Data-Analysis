"""Configuration for chart visualization."""

from dataclasses import dataclass
from typing import Dict, Tuple, Any


@dataclass
class ChartConfig:
    """
    Configuration for charts.

    Attributes:
        figure_size: Default size of the figure (width, height) with 1:1 ratio.
        dpi: Dots per inch for the output image.
        font_scale: Global scaling factor for all font sizes.
        base_fontsize: Base font size from which all other sizes are calculated.
        title_fontsize: Font size for the chart title.
        label_fontsize: Font size for category labels.
        tick_fontsize: Font size for tick labels.
        legend_fontsize: Font size for legend text.
        annotation_fontsize: Font size for annotations.
        tight_layout: Whether to use tight layout.
        bbox_inches: Bounding box in inches for saving.
        chart_sizes: Dictionary of chart-specific sizes, all with 1:1 ratio.
        colormaps: Dictionary of chart-specific colormaps.
        default_titles: Dictionary of default titles for each chart type.
        grid_settings: Dictionary of default grid settings.
        legend_settings: Dictionary of default legend settings.
        annotation_settings: Dictionary of default annotation settings.
        marker_settings: Dictionary of default marker settings.
    """

    # Default chart dimensions with 1:1 ratio
    figure_size: Tuple[int, int] = (10, 10)
    dpi: int = 300

    # Font scaling mechanism
    font_scale: float = 1.0
    base_fontsize: int = 16

    # Text sizes (now derived from base_fontsize and font_scale)
    title_fontsize: int = None
    label_fontsize: int = None
    tick_fontsize: int = None
    legend_fontsize: int = None
    annotation_fontsize: int = None

    # Output configuration
    tight_layout: bool = True
    bbox_inches: str = "tight"
    
    # Chart-specific sizes (all with 1:1 ratio)
    chart_sizes: Dict[str, Tuple[int, int]] = None
    
    # Chart-specific colormaps
    colormaps: Dict[str, str] = None
    
    # Default titles for each chart type
    default_titles: Dict[str, str] = None
    
    # Grid settings for different chart types
    grid_settings: Dict[str, Dict[str, Any]] = None
    
    # Legend settings for different chart types
    legend_settings: Dict[str, Dict[str, Any]] = None
    
    # Annotation settings
    annotation_settings: Dict[str, Dict[str, Any]] = None
    
    # Marker settings
    marker_settings: Dict[str, Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize configuration dictionaries and font sizes if not provided."""
        # Set font sizes based on base_fontsize and font_scale if not explicitly provided
        if self.title_fontsize is None:
            self.title_fontsize = int(self.base_fontsize * 1.5 * self.font_scale)
        if self.label_fontsize is None:
            self.label_fontsize = int(self.base_fontsize * 1.3 * self.font_scale)
        if self.tick_fontsize is None:
            self.tick_fontsize = int(self.base_fontsize * 1.1 * self.font_scale)
        if self.legend_fontsize is None:
            self.legend_fontsize = int(self.base_fontsize * 1.1 * self.font_scale)
        if self.annotation_fontsize is None:
            self.annotation_fontsize = int(self.base_fontsize * 1.0 * self.font_scale)
            
        # Initialize other dictionaries
        if self.chart_sizes is None:
            self.chart_sizes = {
                "heatmap": (10, 10),
                "bar": (10, 10),
                "timeline": (10, 10),
                "area": (10, 10),
                "grouped_bar": (10, 10)
            }
            
        if self.colormaps is None:
            self.colormaps = {
                "heatmap": "viridis",
                "bar": "tab10",
                "timeline": "tab10",
                "area": "tab10",
                "grouped_bar": "Paired"
            }
            
        if self.default_titles is None:
            self.default_titles = {
                "heatmap": "Character Distribution by Element and Path",
                "bar": "Character Rarity Distribution with Element Breakdown",
                "timeline": "Character Introduction Rate by Version",
                "area": "Elemental Balance Evolution Across Versions",
                "grouped_bar": "Character Path Distribution by Rarity"
            }
            
        if self.grid_settings is None:
            self.grid_settings = {
                "timeline": {"visible": True, "linestyle": "--", "alpha": 0.7},
                "area": {"visible": True, "linestyle": "--", "alpha": 0.7},
                "grouped_bar": {"visible": True, "axis": "y", "linestyle": "--", "alpha": 0.7}
            }
            
        if self.legend_settings is None:
            self.legend_settings = {
                "bar": {"title": "Element", "bbox_to_anchor": (1.05, 1), "loc": "upper left"},
                "area": {"title": "Element", "bbox_to_anchor": (1.05, 1), "loc": "upper left"},
                "grouped_bar": {"title": "Rarity", "bbox_to_anchor": (1.05, 1), "loc": "upper left"}
            }
            
        if self.annotation_settings is None:
            self.annotation_settings = {
                "timeline": {
                    "textcoords": "offset points",
                    "xytext": (0, 10),
                    "ha": "center",
                    "fontsize_offset": 0  # No offset needed anymore as we use annotation_fontsize
                },
                "grouped_bar": {
                    "fmt": "%.0f",
                    "padding": 3
                },
                "heatmap": {
                    "fmt": ".0f"
                }
            }
            
        if self.marker_settings is None:
            self.marker_settings = {
                "timeline": {
                    "primary": {"marker": "o", "markersize": 10, "linewidth": 2},
                    "secondary": {"marker": "s", "linestyle": "--", "color": "darkred", "alpha": 0.7, "markersize": 8}
                }
            }
    
    def set_font_scale(self, scale: float) -> None:
        """
        Set a new font scale and recalculate all font sizes.
        
        Args:
            scale: New scale factor for fonts
        """
        self.font_scale = scale
        # Recalculate all font sizes
        self.title_fontsize = int(self.base_fontsize * 1.5 * self.font_scale)
        self.label_fontsize = int(self.base_fontsize * 1.3 * self.font_scale)
        self.tick_fontsize = int(self.base_fontsize * 1.1 * self.font_scale)
        self.legend_fontsize = int(self.base_fontsize * 1.1 * self.font_scale)
        self.annotation_fontsize = int(self.base_fontsize * 1.0 * self.font_scale)
        
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
        
    def get_marker_settings(self, chart_type: str, marker_type: str = "primary") -> Dict[str, Any]:
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
