#!/usr/bin/env python3
"""Create original-color and grayscale print-size QA previews."""

from pathlib import Path

from PIL import Image, ImageOps


with Image.open(Path("figure.png")) as source_image:
    source = source_image.convert("RGB")
preview_width = 1780
preview_height = round(source.height * preview_width / source.width)
preview = source.resize((preview_width, preview_height), Image.Resampling.LANCZOS)
preview.save("qa-original.png", dpi=(254, 254))
ImageOps.grayscale(preview).convert("RGB").save("qa-grayscale.png", dpi=(254, 254))
