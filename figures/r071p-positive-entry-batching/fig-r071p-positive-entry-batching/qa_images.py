#!/usr/bin/env python3
"""Build final-size color and true-grayscale QA previews."""

from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
TARGET = (1780, 1180)  # 178 mm by 118 mm at 254 dpi.


def main() -> None:
    with Image.open(ROOT / "figure.png") as source:
        color = source.convert("RGB").resize(TARGET, Image.Resampling.LANCZOS)
    color.save(ROOT / "qa-original.png", dpi=(254, 254), optimize=True)
    gray = color.convert("L")
    gray.save(ROOT / "qa-grayscale.png", dpi=(254, 254), optimize=True)


if __name__ == "__main__":
    main()

