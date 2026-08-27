#!/usr/bin/env python3
"""Create final-size, grayscale, and PDF-raster QA surfaces."""

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
    size = (round(source.width * scale), round(source.height * scale))
    final = source.resize(size, Image.Resampling.LANCZOS)
    final.save(ROOT / "qa-final-size.png", dpi=(qa_dpi, qa_dpi))
    final.convert("L").save(ROOT / "qa-grayscale.png", dpi=(qa_dpi, qa_dpi))
    pdftoppm = shutil.which("pdftoppm")
    if pdftoppm is None:
        raise RuntimeError("pdftoppm is required for PDF QA")
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
    pdf = Image.open(ROOT / "qa-pdf.png").convert("RGB")
    if pdf.size != size:
        pdf = pdf.resize(size, Image.Resampling.LANCZOS)
    pdf.save(ROOT / "qa-pdf.png", dpi=(qa_dpi, qa_dpi))
    print(f"QA surfaces: {size[0]}x{size[1]} at {qa_dpi} dpi")


if __name__ == "__main__":
    main()
