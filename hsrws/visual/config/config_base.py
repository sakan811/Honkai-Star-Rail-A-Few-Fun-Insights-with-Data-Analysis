"""Base configuration for chart visualization."""

from hsrws.visual.config.config_core import ChartConfig
from hsrws.visual.config.config_methods import (
    configure_legend,
    configure_grid,
    wrap_text,
)
from hsrws.visual.config.config_properties import (
    get_font_size,
    get_size,
    get_colormap,
    get_title,
    get_grid_settings,
    get_legend_settings,
    get_annotation_settings,
    get_marker_settings,
)

# Add config methods to ChartConfig class
ChartConfig.get_font_size = get_font_size
ChartConfig.get_size = get_size
ChartConfig.get_colormap = get_colormap
ChartConfig.get_title = get_title
ChartConfig.get_grid_settings = get_grid_settings
ChartConfig.get_legend_settings = get_legend_settings
ChartConfig.get_annotation_settings = get_annotation_settings
ChartConfig.get_marker_settings = get_marker_settings

# Import methods from config_methods module
ChartConfig.configure_legend = configure_legend
ChartConfig.configure_grid = configure_grid
ChartConfig.wrap_text = wrap_text
