"""Configuration for chart visualization."""

from dataclasses import dataclass


@dataclass
class ChartConfig:
    """
    Configuration for donut charts.
    
    Attributes:
        figure_size: Size of the figure (width, height).
        dpi: Dots per inch for the output image.
        donut_width: Width of the donut ring.
        donut_hole_radius: Radius of the donut hole.
        title_fontsize: Font size for the chart title.
        title_pad: Padding for the chart title.
        center_text_fontsize: Font size for the text in the center of the donut.
        label_fontsize: Font size for category labels.
        pct_fontsize: Font size for percentage labels.
        count_fontsize: Font size for count labels.
        path_cmap: Color map for Path charts.
        element_cmap: Color map for Element charts.
        rarity_cmap: Color map for Rarity charts.
        pct_distance: Distance of percentage labels from the center.
        tight_layout: Whether to use tight layout.
        bbox_inches: Bounding box in inches for saving.
    """
    # Chart dimensions
    figure_size: tuple = (10, 10)
    dpi: int = 300
    
    # Donut properties
    donut_width: float = 0.5
    donut_hole_radius: float = 0.4
    
    # Text sizes
    title_fontsize: int = 20
    title_pad: int = 20
    center_text_fontsize: int = 20
    label_fontsize: int = 20
    pct_fontsize: int = 15
    count_fontsize: int = 15
    
    # Color maps
    path_cmap: str = "Blues"
    element_cmap: str = "Spectral"
    rarity_cmap: str = "Reds"
    
    # Positioning
    pct_distance: float = 0.85
    
    # Output configuration
    tight_layout: bool = True
    bbox_inches: str = 'tight' 