"""Utility methods for chart configuration."""

from typing import Dict, Any


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