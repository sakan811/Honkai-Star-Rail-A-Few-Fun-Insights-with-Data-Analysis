"""Configuration for chart visualization."""

from dataclasses import dataclass, field
from typing import Dict, Tuple, Any, Optional


@dataclass
class ChartConfig:
    """
    Configuration for charts.

    Attributes:
        figure_size: Default size of the figure (width, height) with 1:1 ratio.
        dpi: Dots per inch for the output image.
        font_scale: Global scaling factor for all font sizes.
        base_fontsize: Base font size from which all other sizes are calculated.
        tight_layout: Whether to use tight layout.
        bbox_inches: Bounding box in inches for saving.
        auto_rotate_labels: Whether to auto-rotate labels to prevent overlap.
        font_scale_by_chart: Dictionary with per-chart font scaling factors.
    """
    # Default chart dimensions with 1:1 ratio (square for Instagram)
    figure_size: Tuple[int, int] = (10, 10)
    dpi: int = 300

    # Font configuration
    font_scale: float = 1.2
    base_fontsize: int = 16
    
    # Font sizes are calculated dynamically in __post_init__
    title_fontsize: Optional[int] = None
    label_fontsize: Optional[int] = None
    tick_fontsize: Optional[int] = None
    legend_fontsize: Optional[int] = None
    annotation_fontsize: Optional[int] = None
    
    # Maximum title width in characters before wrapping
    title_wrap_length: int = 30
    
    # Chart-specific font scaling factors
    font_scale_by_chart: Dict[str, Dict[str, float]] = field(default_factory=lambda: {
        "heatmap": {
            "title": 1.1,     # Square format - increased title size
            "label": 1.05,    # Larger labels
            "tick": 1.0,      # Larger ticks to enhance readability
            "annotation": 1.0, # Increased annotations for dense heatmap cells
            "legend": 1.0    # Larger legend size
        },
        "bar": {
            "title": 0.8,     # Landscape format - larger title
            "label": 0.8,     # Larger label size
            "tick": 0.8,      # Larger ticks for horizontal layout
            "annotation": 0.8, # Larger annotation size
            "legend": 0.8    # Larger legend size
        },
        "timeline": {
            "title": 0.8,     # Landscape format - larger title
            "label": 0.8,     # Larger label size
            "tick": 0.8,     # Larger ticks for dense timeline
            "annotation": 0.8, # Larger annotations for potential overlap
            "legend": 0.8     # Larger legend size
        },
        "area": {
            "title": 0.8,     # Landscape format - larger title
            "label": 0.8,     # Larger label size
            "tick": 0.8,     # Larger ticks for version numbers
            "annotation": 0.8, # Larger annotation size
            "legend": 0.8     # Larger legend size
        },
        "grouped_bar": {
            "title": 1.0,     # Portrait format - larger title
            "label": 1.0,    # Larger labels for readability
            "tick": 1.0,     # Larger ticks for grouped bars
            "annotation": 1.0, # Larger annotations to avoid overlap
            "legend": 1.0    # Larger legend size
        }
    })
    
    # Title wrap settings
    wrap_title: bool = True

    # Output configuration
    tight_layout: bool = True
    bbox_inches: str = "tight"
    
    # Auto-rotate labels to prevent overlap
    auto_rotate_labels: bool = True
    
    # Chart-specific configurations with aspect ratios optimized for Instagram
    # Square ratio (1:1) - Default for Instagram feed: 1080px x 1080px
    # Landscape ratio (1.91:1) - Landscape for Instagram: 1080px x 566px
    # Portrait ratio (4:5) - Vertical for Instagram: 1080px x 1350px
    chart_sizes: Dict[str, Tuple[int, int]] = field(default_factory=lambda: {
        # Heatmap - Square format (1:1) is ideal for heatmaps to maintain cell symmetry
        "heatmap": (10, 10),  # 1:1 ratio
        
        # Bar chart - Landscape format (1.91:1) works better for horizontal bars
        "bar": (10, 5.24),  # Close to 1.91:1 ratio
        
        # Timeline - Landscape format (1.91:1) works well for time series
        "timeline": (10, 5.24),  # Close to 1.91:1 ratio
        
        # Area chart - Landscape format (1.91:1) works well for evolution visualization
        "area": (10, 5.24),  # Close to 1.91:1 ratio
        
        # Grouped bar - Portrait format (4:5) works well for vertical comparisons
        "grouped_bar": (8, 10)  # Close to 4:5 ratio
    })
    
    colormaps: Dict[str, str] = field(default_factory=lambda: {
        "heatmap": "viridis",
        "bar": "tab10",
        "timeline": "tab10",
        "area": "tab10",
        "grouped_bar": "Paired"
    })
    
    default_titles: Dict[str, str] = field(default_factory=lambda: {
        "heatmap": "Honkai: Star Rail Character Distribution by Element and Path",
        "bar": "Honkai: Star Rail Character Rarity Distribution with Element Breakdown",
        "timeline": "Honkai: Star Rail Character Introduction Rate by Version",
        "area": "Honkai: Star Rail Elemental Balance Evolution Across Versions",
        "grouped_bar": "Honkai: Star Rail Character Path Distribution by Rarity"
    })
    
    grid_settings: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "timeline": {"visible": True, "linestyle": "--", "alpha": 0.7},
        "area": {"visible": True, "linestyle": "--", "alpha": 0.7},
        "grouped_bar": {"visible": True, "axis": "y", "linestyle": "--", "alpha": 0.7}
    })
    
    legend_settings: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        # For landscape charts (bar, timeline, area), position legend on the right side
        "bar": {"title": "Element", "bbox_to_anchor": (1.15, 0.5), "loc": "center left"},
        "area": {"title": "Element", "bbox_to_anchor": (1.15, 0.5), "loc": "center left"},
        "timeline": {"title": "Data Type", "bbox_to_anchor": (1.15, 0.5), "loc": "center left"},
        # For portrait chart (grouped_bar), position legend at the top
        "grouped_bar": {"title": "Rarity", "bbox_to_anchor": (0.5, 1.15), "loc": "lower center"}
    })
    
    annotation_settings: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "timeline": {
            "textcoords": "offset points",
            "xytext": (0, 15),  # Increased vertical offset
            "ha": "center",
            "fontsize_offset": 2  # Add additional size increase
        },
        "grouped_bar": {
            "fmt": "%.0f",
            "padding": 5,
            "fontweight": "bold"  # Make annotations bold
        },
        "heatmap": {
            "fmt": ".0f",
            "fontweight": "bold"  # Make annotations bold
        }
    })
    
    marker_settings: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "timeline": {
            "primary": {"marker": "o", "markersize": 8, "linewidth": 2},
            "secondary": {"marker": "s", "linestyle": "--", "color": "darkred", "alpha": 0.7, "markersize": 6}
        }
    })
    
    def __post_init__(self):
        """Calculate font sizes based on base_fontsize and font_scale."""
        self._calculate_font_sizes()
    
    def _calculate_font_sizes(self) -> None:
        """Calculate all font sizes based on base_fontsize and font_scale."""
        if self.title_fontsize is None:
            self.title_fontsize = int(self.base_fontsize * 1.4 * self.font_scale)
        if self.label_fontsize is None:
            self.label_fontsize = int(self.base_fontsize * 1.2 * self.font_scale)
        if self.tick_fontsize is None:
            self.tick_fontsize = int(self.base_fontsize * 1.0 * self.font_scale)
        if self.legend_fontsize is None:
            self.legend_fontsize = int(self.base_fontsize * 1.0 * self.font_scale)
        if self.annotation_fontsize is None:
            self.annotation_fontsize = int(self.base_fontsize * 0.9 * self.font_scale)
    
    def set_font_scale(self, scale: float) -> None:
        """
        Set a new font scale and recalculate all font sizes.
        
        Args:
            scale: New scale factor for fonts
        """
        self.font_scale = scale
        self._calculate_font_sizes()
    
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
        if size_type == 'title':
            base_size = self.title_fontsize
        elif size_type == 'label':
            base_size = self.label_fontsize
        elif size_type == 'tick':
            base_size = self.tick_fontsize
        elif size_type == 'annotation':
            base_size = self.annotation_fontsize
        elif size_type == 'legend':
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
    
    def configure_legend(self, ax, chart_type: str):
        """
        Configure the legend for a chart based on settings.
        
        Args:
            ax: Matplotlib axis to configure legend for
            chart_type: Type of chart to get legend settings for
            
        Returns:
            The legend object
        """
        legend_settings = self.get_legend_settings(chart_type)
        legend = ax.legend(
            title=legend_settings.get("title", ""),
            bbox_to_anchor=legend_settings.get("bbox_to_anchor", (1.15, 1)),
            loc=legend_settings.get("loc", "upper left")
        )
        
        # Apply chart-specific font sizes for legend
        legend.get_title().set_fontsize(self.get_font_size('legend', chart_type))
        
        for text in legend.get_texts():
            text.set_fontsize(self.get_font_size('legend', chart_type))
        
        return legend
        
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

    def configure_grid(self, ax, chart_type: str):
        """
        Configure the grid for a chart based on settings.
        
        Args:
            ax: Matplotlib axis to configure grid for
            chart_type: Type of chart to get grid settings for
        """
        grid_settings = self.get_grid_settings(chart_type)
        if grid_settings.get("visible", False):
            axis = grid_settings.get("axis", "both")
            ax.grid(
                True,
                axis=axis,
                linestyle=grid_settings.get("linestyle", "--"),
                alpha=grid_settings.get("alpha", 0.7)
            )

    def wrap_text(self, text: str, max_width: int = None) -> str:
        """
        Wrap text to a maximum width.
        
        Args:
            text: Text to wrap
            max_width: Maximum width in characters, uses title_wrap_length if None
            
        Returns:
            Wrapped text with newlines
        """
        if not self.wrap_title:
            return text
            
        if max_width is None:
            max_width = self.title_wrap_length
            
        # Simple wrapping logic
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + len(current_line) <= max_width:
                current_line.append(word)
                current_length += len(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
                
        if current_line:
            lines.append(' '.join(current_line))
            
        return '\n'.join(lines)
