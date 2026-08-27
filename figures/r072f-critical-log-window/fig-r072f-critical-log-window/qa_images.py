#!/usr/bin/env python3
"""Create final-size color, grayscale, and PDF-raster QA surfaces."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess

from PIL import Image


ROOT = Path(__file__).resolve().parent


def main() -> None:
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    qa_dpi = int(config["figure"]["qaDpi"])
    source = Image.open(ROOT / "figure.png").convert("RGB")
    source_dpi = float(source.info.get("dpi", (600.0, 600.0))[0])
    scale = qa_dpi / source_dpi
    size = (
        max(1, round(source.width * scale)),
        max(1, round(source.height * scale)),
    )
    final_size = source.resize(size, Image.Resampling.LANCZOS)
    final_size.save(ROOT / "qa-final-size.png", dpi=(qa_dpi, qa_dpi))
    final_size.convert("L").save(ROOT / "qa-grayscale.png", dpi=(qa_dpi, qa_dpi))

    pdftoppm = shutil.which("pdftoppm")
    if pdftoppm is None:
        raise RuntimeError("pdftoppm not found")
    subprocess.run(
        [
            pdftoppm,
            "-png",
            "-singlefile",
            "-r",
            str(qa_dpi),
            str(ROOT / "figure.pdf"),
            str(ROOT / "qa-pdf"),
        ],
        check=True,
    )
    pdf_image = Image.open(ROOT / "qa-pdf.png").convert("RGB")
    if pdf_image.size != size:
        pdf_image = pdf_image.resize(size, Image.Resampling.LANCZOS)
    pdf_image.save(ROOT / "qa-pdf.png", dpi=(qa_dpi, qa_dpi))
    print(f"QA surfaces written at {qa_dpi} dpi: {size[0]}x{size[1]}")


if __name__ == "__main__":
    main()
