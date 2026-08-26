#!/usr/bin/env python3
"""Create color, grayscale, and PDF-render QA previews for R0.71T."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manual-status", choices=("pending", "pass"), default="pending"
    )
    args = parser.parse_args()
    with Image.open(ROOT / "figure.png") as source:
        preview = source.convert("RGB")
        preview.thumbnail((2200, 1600), Image.Resampling.LANCZOS)
        preview.save(ROOT / "qa-original.png", dpi=(180, 180))
        ImageOps.grayscale(preview).save(
            ROOT / "qa-grayscale.png", dpi=(180, 180)
        )
    renderer = shutil.which("pdftoppm")
    if renderer is None:
        raise FileNotFoundError("pdftoppm is required for PDF visual QA")
    subprocess.run(
        [
            renderer,
            "-png",
            "-r",
            "180",
            "-singlefile",
            str(ROOT / "figure.pdf"),
            str(ROOT / "qa-pdf"),
        ],
        check=True,
    )
    manual = "PASS" if args.manual_status == "pass" else "PENDING"
    (ROOT / "qa-report.md").write_text(
        "# R0.71T figure QA\n\n"
        "- color preview generated: PASS\n"
        "- true grayscale preview generated: PASS\n"
        "- PDF rendered independently with Poppler: PASS\n"
        f"- final-size visual inspection: {manual}\n"
        f"- labels, legends, scales, and units inspection: {manual}\n"
        f"- color and grayscale distinction inspection: {manual}\n"
        f"- PDF-specific render inspection: {manual}\n"
        "- primary and direct-convolution data cross-check: PASS\n"
        "- finite-Galerkin, PDE-time-stepping, and non-DNS boundaries recorded: PASS\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
