"""Utility classes for generating simple charts and badges."""

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Tuple

import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont


@dataclass
class GraphicConfig:
    """Configuration for a graphic element."""

    width: int
    height: int
    background_color: Tuple[float, float, float]
    line_color: Tuple[float, float, float] | None = None
    line_width: float | None = None
    font_size: float = 12.0


def _ensure_dir(directory: Path) -> None:
    """Create directory if it does not exist."""

    directory.mkdir(parents=True, exist_ok=True)


class GraphicGenerator:
    """Generate simple graphics to disk."""

    def __init__(self, output_dir: Path) -> None:
        """Initialize the generator with an output directory."""

        self.output_dir = output_dir
        _ensure_dir(self.output_dir)

    def create_chart(
        self, data: Iterable[float], config: GraphicConfig, title: str
    ) -> Path:
        """Create a simple line chart and return the saved path."""
        fig, ax = plt.subplots(
            figsize=(config.width / 100, config.height / 100), dpi=100
        )
        ax.plot(
            list(data),
            color=config.line_color or "blue",
            linewidth=config.line_width or 2,
        )
        ax.set_title(title)
        fig.patch.set_facecolor(config.background_color)
        ax.set_facecolor(config.background_color)
        output_path = self.output_dir / f"{title.replace(' ', '_')}.png"
        plt.tight_layout()
        fig.savefig(output_path)
        plt.close(fig)
        return output_path

    def create_badge(
        self, text: str, config: GraphicConfig, style: str = "rounded"
    ) -> Path:
        """Create a badge image and return the saved path."""
        img = Image.new(
            "RGB",
            (config.width, config.height),
            tuple(int(c * 255) for c in config.background_color),
        )
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", int(config.font_size))
        except (OSError, IOError):
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        text_x = (config.width - text_w) / 2
        text_y = (config.height - text_h) / 2
        draw.text(
            (text_x, text_y),
            text,
            fill=tuple(int(c * 255) for c in (config.line_color or (1, 1, 1))),
            font=font,
        )
        if style == "rounded":
            mask = Image.new("L", (config.width, config.height), 0)
            ImageDraw.Draw(mask).rounded_rectangle(
                [(0, 0), (config.width, config.height)], 5, fill=255
            )
            rounded = Image.new(
                "RGB",
                (config.width, config.height),
                tuple(int(c * 255) for c in config.background_color),
            )
            rounded.paste(img, (0, 0), mask)
            img = rounded
        output_path = self.output_dir / f"{text.replace(' ', '_')}_badge.png"
        img.save(output_path)
        return output_path
