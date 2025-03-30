"""Tests for chart configuration."""

import pytest
from hsrws.visual.config import ChartConfig


@pytest.fixture
def default_config():
    """Return a default ChartConfig instance."""
    return ChartConfig()


def test_chart_config_initialization():
    """Test ChartConfig initialization with default values."""
    config = ChartConfig()
    
    # Test default values
    assert config.figure_size == (10, 10)
    assert config.dpi == 300
    assert config.font_scale == 1.2
    assert config.base_fontsize == 16
    assert config.tight_layout is True
    assert config.bbox_inches == "tight"
    assert config.auto_rotate_labels is True


def test_font_size_calculation(default_config):
    """Test that font sizes are calculated correctly."""
    # Test calculated font sizes
    assert default_config.title_fontsize == int(default_config.base_fontsize * 1.4 * default_config.font_scale)
    assert default_config.label_fontsize == int(default_config.base_fontsize * 1.2 * default_config.font_scale)
    assert default_config.tick_fontsize == int(default_config.base_fontsize * 1.0 * default_config.font_scale)
    assert default_config.legend_fontsize == int(default_config.base_fontsize * 1.0 * default_config.font_scale)
    assert default_config.annotation_fontsize == int(default_config.base_fontsize * 0.9 * default_config.font_scale)


def test_set_font_scale():
    """Test setting font scale."""
    # Create a fresh config for this test
    config = ChartConfig()
    original_scale = config.font_scale
    
    # Change to a different scale
    new_scale = original_scale + 0.5
    config.set_font_scale(new_scale)
    
    # Check that font scale was updated
    assert config.font_scale == new_scale
    assert config.font_scale != original_scale


def test_get_font_size_for_chart_type(default_config):
    """Test getting font size for specific chart type."""
    # Test for heatmap chart type
    title_size_heatmap = default_config.get_font_size("title", "heatmap")
    title_size_timeline = default_config.get_font_size("title", "timeline")
    
    # Heatmap has a scale factor of 1.1, timeline has 0.8
    assert title_size_heatmap != title_size_timeline


def test_get_size_for_chart_type(default_config):
    """Test getting size for specific chart type."""
    # Test size for different chart types
    heatmap_size = default_config.get_size("heatmap")
    bar_size = default_config.get_size("bar")
    
    # Heatmap is square (1:1), bar is landscape (1.91:1)
    assert heatmap_size == (10, 10)
    assert bar_size != heatmap_size
    assert bar_size[0] / bar_size[1] > 1  # Width > height for landscape


def test_get_colormap(default_config):
    """Test getting colormap for chart type."""
    heatmap_cmap = default_config.get_colormap("heatmap")
    bar_cmap = default_config.get_colormap("bar")
    
    assert heatmap_cmap == "viridis"
    assert bar_cmap == "tab10"
    assert heatmap_cmap != bar_cmap


def test_get_title(default_config):
    """Test getting default title for chart type."""
    heatmap_title = default_config.get_title("heatmap")
    
    assert "Element" in heatmap_title
    assert "Path" in heatmap_title


def test_wrap_text(default_config):
    """Test text wrapping functionality."""
    long_text = "This is a very long title that should be wrapped to multiple lines for better readability"
    wrapped_text = default_config.wrap_text(long_text)
    
    # Check that text was wrapped (contains newlines)
    assert "\n" in wrapped_text
    
    # Disable wrapping and test again
    default_config.wrap_title = False
    unwrapped_text = default_config.wrap_text(long_text)
    assert "\n" not in unwrapped_text
    assert unwrapped_text == long_text 