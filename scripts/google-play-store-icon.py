"""
Generate an icon for the Google Play Store.

Create fastlane/metadata/android/en-US/images/icon.png using pyproject.toml .tool.flet.product
"""

import io
from pathlib import Path

from PIL import Image
from resvg_py import svg_to_bytes

import project


def generate_icon(path: Path,
                  text: str,
                  color: str,
                  background=None,
                  width=512,
                  height=512,
                  mode="RGBA",
                  max_bytes=1024 * 1024,
                  ):
    font_scale = 65 / 100
    font_x = 50 / 100
    font_y = 55 / 100

    font_family = "Georgia"
    font_em_h = 1.23
    font_em_v = 1.423

    font_size = font_scale * font_em_h * width
    x = f"{font_x:.2%}"
    y = height - ((height - (font_size * 1 / font_em_v)) / 2) * (.5 + font_y)

    svg_string = f"""\
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
            {f'<rect width="{width}" height="{height}" rx="30%" fill="{background}" />' if background else ''}
            <text x="{x}" y="{y}" text-anchor="middle"
                  font-family="{font_family}"
                  font-weight="bold"
                  font-size="{font_size}"
                  fill="{color}">{text}
            </text>
        </svg>
        """

    # Render vector SVG to raster PNG bytes
    png_bytes = svg_to_bytes(svg_string=svg_string)

    # Load into Pillow for color space and 32-bit RGBA handling
    image = Image.open(io.BytesIO(png_bytes))

    # Ensure 32-bit RGBA format (8 bits per channel: Red, Green, Blue, Alpha)
    assert image.mode == mode
    assert image.size == (width, height)

    for compress_level in range(9, -1, -1):
        image.save(
            path,
            format=Image.registered_extensions()[path.suffix],
            optimize=True,
            compress_level=compress_level
        )
        if path.stat().st_size <= max_bytes:
            return
    raise ValueError()


if __name__ == '__main__':
    text = project.product[0]
    generate_icon(project.root / "fastlane/metadata/android/en-US/images/icon.png", text, color="#455a64")
