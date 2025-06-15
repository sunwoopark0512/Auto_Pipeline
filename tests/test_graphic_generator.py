"""Graphic Generator Tests."""

from pathlib import Path
import pytest

from graphic_generator import GraphicGenerator, GraphicConfig


@pytest.fixture
def temp_dir(tmp_path):
    """Temporary directory for test outputs."""
    return tmp_path


@pytest.fixture
def generator(temp_dir):
    """Graphic generator instance."""
    return GraphicGenerator(temp_dir)


@pytest.fixture
def config():
    """Basic graphic configuration."""
    return GraphicConfig(
        width=400,
        height=300,
        background_color=(1.0, 1.0, 1.0),
        line_color=(0.0, 0.0, 0.0),
        line_width=2.0,
        font_size=14.0,
    )


def test_create_chart(generator, config):
    """Test chart creation."""
    data = [1.0, 2.0, 1.5, 3.0, 2.5]
    output_path = generator.create_chart(data, config, "Test Chart")
    
    assert output_path.exists()
    assert output_path.suffix == ".png"


def test_create_chart_empty_data(generator, config):
    """Test chart creation with empty data."""
    with pytest.raises(ValueError):
        generator.create_chart([], config)


def test_create_badge(generator, config):
    """Test badge creation."""
    text = "Test Badge"
    output_path = generator.create_badge(text, config)
    
    assert output_path.exists()
    assert output_path.suffix == ".png"


def test_create_badge_rounded(generator, config):
    """Test rounded badge creation."""
    text = "Rounded Badge"
    output_path = generator.create_badge(text, config, style="rounded")
    
    assert output_path.exists()
    assert output_path.suffix == ".png"


def test_output_directory_creation(temp_dir):
    """Test output directory creation."""
    output_dir = temp_dir / "graphics"
    generator = GraphicGenerator(output_dir)
    assert output_dir.exists()
    assert output_dir.is_dir()
