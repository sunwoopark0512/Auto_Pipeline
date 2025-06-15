"""Tests for the :mod:`graphic_generator` package."""

from pathlib import Path

from graphic_generator import GraphicConfig, GraphicGenerator


def test_create_chart(tmp_path: Path) -> None:
    """Ensure a chart image is created."""

    generator = GraphicGenerator(tmp_path)
    config = GraphicConfig(width=400, height=200, background_color=(1, 1, 1))
    data = [0, 1, 2, 3]
    chart_path = generator.create_chart(data, config, "Test Chart")
    assert chart_path.exists()


def test_create_badge(tmp_path: Path) -> None:
    """Ensure a badge image is created."""

    generator = GraphicGenerator(tmp_path)
    config = GraphicConfig(width=100, height=20, background_color=(1, 0, 0))
    badge_path = generator.create_badge("OK", config)
    assert badge_path.exists()
