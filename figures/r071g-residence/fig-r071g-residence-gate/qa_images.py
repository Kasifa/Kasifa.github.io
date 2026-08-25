#!/usr/bin/env python3
"""Create print-size original and grayscale QA images for visual inspection."""

from pathlib import Path

from PIL import Image, ImageOps


source = Image.open(Path("figure.png")).convert("RGB")
preview_width = 1780
preview_height = round(source.height * preview_width / source.width)
preview = source.resize((preview_width, preview_height), Image.Resampling.LANCZOS)
preview.save("qa-original.png", dpi=(254, 254))
ImageOps.grayscale(preview).convert("RGB").save(
    "qa-grayscale.png", dpi=(254, 254)
)
