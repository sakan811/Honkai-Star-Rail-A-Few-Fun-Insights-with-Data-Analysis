"""Base plotting utilities for HSR visualization."""

import matplotlib.pyplot as plt


def _setup_chart_basics(fig, ax, config, chart_type, title, patch_version=None, x_label=None, y_label=None):
    """
    Set up basic chart properties with appropriate aspect ratio based on chart type.
    
    Args:
        fig: Matplotlib figure object
        ax: Matplotlib axis object
        config: ChartConfig object
        chart_type: Type of chart for retrieving specific settings
        title: Chart title
        patch_version: Optional patch version to append to title
        x_label: Label for x-axis
        y_label: Label for y-axis
        
    Returns:
        None (modifies the axis object in-place)
    """
    # Get chart size to calculate aspect ratio
    chart_size = config.get_size(chart_type)
    aspect_ratio = chart_size[0] / chart_size[1] if chart_size[1] != 0 else 1
    
    # Set aspect ratio based on chart type
    # For square charts (1:1 ratio), force box_aspect
    if abs(aspect_ratio - 1) < 0.1:  # If the ratio is approximately 1:1
        ax.set_box_aspect(1)
    
    # Set title with optional patch version
    if patch_version:
        title = f"{title} - {patch_version}"
    
    # Apply title wrapping if enabled
    if hasattr(config, 'wrap_text'):
        title = config.wrap_text(title)
    
    ax.set_title(title, fontsize=config.get_font_size('title', chart_type), pad=15)
    
    # Set axis labels if provided
    if x_label:
        ax.set_xlabel(x_label, fontsize=config.get_font_size('label', chart_type), labelpad=10)
    if y_label:
        ax.set_ylabel(y_label, fontsize=config.get_font_size('label', chart_type), labelpad=10)
    
    # Set tick label font sizes
    ax.tick_params(axis='both', which='major', labelsize=config.get_font_size('tick', chart_type))
    
    # Rotate x-axis labels to prevent overlap if auto_rotate_labels is enabled
    if config.auto_rotate_labels:
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor") 