#!/usr/bin/env python3
"""Create original and grayscale print-size QA previews."""

from pathlib import Path

from PIL import Image, ImageOps


with Image.open(Path("figure.png")) as image:
    source = image.convert("RGB")
width = 1780
height = round(source.height * width / source.width)
preview = source.resize((width, height), Image.Resampling.LANCZOS)
preview.save("qa-original.png", dpi=(254, 254))
ImageOps.grayscale(preview).convert("RGB").save("qa-grayscale.png", dpi=(254, 254))
