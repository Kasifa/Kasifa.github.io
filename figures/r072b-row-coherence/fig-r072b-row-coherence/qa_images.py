#!/usr/bin/env python3
"""Create final-size color, grayscale, and PDF-render QA surfaces."""

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
    resized = source.resize(size, Image.Resampling.LANCZOS)
    resized.save(ROOT / "qa-original.png", dpi=(qa_dpi, qa_dpi))
    resized.convert("L").save(ROOT / "qa-grayscale.png", dpi=(qa_dpi, qa_dpi))

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
    print(f"QA surfaces written at {qa_dpi} dpi: {size[0]}x{size[1]}")


if __name__ == "__main__":
    main()
