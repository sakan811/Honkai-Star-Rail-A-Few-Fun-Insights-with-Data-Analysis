"""Core chart configuration class."""

from dataclasses import dataclass, field
from typing import Dict, Tuple, Any, Optional

from hsrws.visual.config.config_chart_settings import (
    get_default_colormaps,
    get_default_titles,
    get_default_grid_settings,
    get_default_legend_settings,
    get_default_annotation_settings,
    get_default_marker_settings,
)
from hsrws.visual.config.config_chart_sizes import (
    get_default_font_scale_by_chart,
    get_default_chart_sizes,
)


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
    figure_size: Tuple[float, float] = (10, 10)
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
    font_scale_by_chart: Dict[str, Dict[str, float]] = field(
        default_factory=get_default_font_scale_by_chart
    )

    # Title wrap settings
    wrap_title: bool = True

    # Output configuration
    tight_layout: bool = True
    bbox_inches: str = "tight"

    # Auto-rotate labels to prevent overlap
    auto_rotate_labels: bool = True

    # Chart-specific configurations with aspect ratios optimized for Instagram
    chart_sizes: Dict[str, Tuple[float, float]] = field(
        default_factory=get_default_chart_sizes
    )
    colormaps: Dict[str, str] = field(default_factory=get_default_colormaps)
    default_titles: Dict[str, str] = field(default_factory=get_default_titles)
    grid_settings: Dict[str, Dict[str, Any]] = field(
        default_factory=get_default_grid_settings
    )
    legend_settings: Dict[str, Dict[str, Any]] = field(
        default_factory=get_default_legend_settings
    )
    annotation_settings: Dict[str, Dict[str, Any]] = field(
        default_factory=get_default_annotation_settings
    )
    marker_settings: Dict[str, Dict[str, Any]] = field(
        default_factory=get_default_marker_settings
    )

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
