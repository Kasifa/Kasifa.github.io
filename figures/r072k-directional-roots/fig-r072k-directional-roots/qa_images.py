#!/usr/bin/env python3
"""Create final-size, grayscale, and PDF-raster QA surfaces for R0.72K."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess

from PIL import Image


ROOT = Path(__file__).resolve().parent


def expected_pixels(config: dict[str, object], dpi: int) -> tuple[int, int]:
    figure = config["figure"]
    assert isinstance(figure, dict)
    return (
        round(float(figure["widthMillimetres"]) / 25.4 * dpi),
        round(float(figure["heightMillimetres"]) / 25.4 * dpi),
    )


def main() -> None:
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    qa_dpi = int(config["figure"]["qaDpi"])
    size = expected_pixels(config, qa_dpi)

    png_path = ROOT / "figure.png"
    pdf_path = ROOT / "figure.pdf"
    if not png_path.is_file() or not pdf_path.is_file():
        raise FileNotFoundError("figure.png and figure.pdf must be built first")

    with Image.open(png_path) as source_image:
        source = source_image.convert("RGB")
    final = source.resize(size, Image.Resampling.LANCZOS)
    final.save(ROOT / "qa-final-size.png", dpi=(qa_dpi, qa_dpi))
    final.convert("L").save(
        ROOT / "qa-grayscale.png", dpi=(qa_dpi, qa_dpi)
    )

    pdftoppm = shutil.which("pdftoppm")
    if pdftoppm is None:
        raise RuntimeError("pdftoppm is required for PDF-raster QA")
    subprocess.run(
        [
            pdftoppm,
            "-png",
            "-f",
            "1",
            "-l",
            "1",
            "-singlefile",
            "-r",
            str(qa_dpi),
            str(pdf_path),
            str(ROOT / "qa-pdf"),
        ],
        check=True,
    )
    with Image.open(ROOT / "qa-pdf.png") as pdf_image:
        pdf_raster = pdf_image.convert("RGB")
    if pdf_raster.size != size:
        pdf_raster = pdf_raster.resize(size, Image.Resampling.LANCZOS)
    pdf_raster.save(ROOT / "qa-pdf.png", dpi=(qa_dpi, qa_dpi))

    print(
        f"R0.72K QA surfaces: {size[0]}x{size[1]} px at {qa_dpi} dpi"
    )


if __name__ == "__main__":
    main()
