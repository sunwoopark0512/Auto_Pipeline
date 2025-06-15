"""Graphic Generator Module."""

import cairo
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple


class GraphicType(Enum):
    """그래픽 유형."""

    CHART = "chart"
    ICON = "icon"
    BADGE = "badge"


@dataclass
class GraphicConfig:
    """그래픽 설정."""

    width: int
    height: int
    background_color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    line_color: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    line_width: float = 2.0
    font_size: float = 14.0
    font_family: str = "Arial"


class GraphicGenerator:
    """그래픽 생성기."""

    def __init__(self, output_dir: Path) -> None:
        """Initialize the graphic generator.

        Args:
            output_dir: Output directory for generated graphics
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_surface(self, config: GraphicConfig) -> cairo.Surface:
        """Create a new Cairo surface."""
        surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            config.width,
            config.height,
        )
        context = cairo.Context(surface)
        context.set_source_rgb(*config.background_color)
        context.paint()
        context.set_source_rgb(*config.line_color)
        context.set_line_width(config.line_width)
        return surface

    def create_chart(
        self,
        data: List[float],
        config: GraphicConfig,
        title: Optional[str] = None,
    ) -> Path:
        """Create a line chart."""
        if not data:
            raise ValueError("Data cannot be empty")

        surface = self.create_surface(config)
        context = cairo.Context(surface)

        padding = 40
        chart_width = config.width - 2 * padding
        chart_height = config.height - 2 * padding

        if title:
            context.set_font_size(config.font_size)
            context.select_font_face(
                config.font_family,
                cairo.FONT_SLANT_NORMAL,
                cairo.FONT_WEIGHT_BOLD,
            )
            context.move_to(padding, padding - 10)
            context.show_text(title)

        max_value = max(data)
        min_value = min(data)
        value_range = max_value - min_value or 1.0

        context.move_to(
            padding,
            config.height - padding - (data[0] - min_value) * chart_height / value_range,
        )
        for i, value in enumerate(data):
            x = padding + i * chart_width / (len(data) - 1)
            y = config.height - padding - (value - min_value) * chart_height / value_range
            context.line_to(x, y)
        context.stroke()

        output_path = self.output_dir / f"chart_{len(data)}.png"
        surface.write_to_png(str(output_path))
        return output_path

    def create_badge(
        self,
        text: str,
        config: GraphicConfig,
        style: str = "flat",
    ) -> Path:
        """Create a badge."""
        surface = self.create_surface(config)
        context = cairo.Context(surface)

        context.set_font_size(config.font_size)
        context.select_font_face(
            config.font_family,
            cairo.FONT_SLANT_NORMAL,
            cairo.FONT_WEIGHT_NORMAL,
        )

        extents = context.text_extents(text)
        text_x = (config.width - extents.width) / 2
        text_y = (config.height + extents.height) / 2

        if style == "rounded":
            context.arc(
                config.height / 2,
                config.height / 2,
                config.height / 2,
                0,
                2 * 3.14159,
            )
            context.arc(
                config.width - config.height / 2,
                config.height / 2,
                config.height / 2,
                0,
                2 * 3.14159,
            )
            context.rectangle(
                config.height / 2,
                0,
                config.width - config.height,
                config.height,
            )
            context.fill()
        else:
            context.rectangle(0, 0, config.width, config.height)
            context.fill()

        context.set_source_rgb(*config.line_color)
        context.move_to(text_x, text_y)
        context.show_text(text)

        output_path = self.output_dir / f"badge_{text.lower()}.png"
        surface.write_to_png(str(output_path))
        return output_path
