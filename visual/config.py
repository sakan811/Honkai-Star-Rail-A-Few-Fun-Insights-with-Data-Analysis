from dataclasses import dataclass


@dataclass
class ChartConfig:
    """Configuration for donut charts."""
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