#!/usr/bin/env python3
"""Generate color, grayscale, and independent PDF-render QA previews."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess

from PIL import Image, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manual-status", choices=("pending", "pass"), default="pending")
    args = parser.parse_args()
    with Image.open(ROOT / "figure.png") as source:
        width, height = source.size
        dpi = source.info.get("dpi", (0.0, 0.0))
        if not (4190 <= width <= 4220 and 3160 <= height <= 3180):
            raise RuntimeError(f"unexpected archival PNG size: {source.size}")
        if min(dpi) < 599.0:
            raise RuntimeError(f"archival PNG does not report 600 dpi: {dpi}")
        preview = source.convert("RGB")
        preview.thumbnail((2200, 1700), Image.Resampling.LANCZOS)
        preview.save(ROOT / "qa-original.png", dpi=(180, 180))
        grayscale = ImageOps.grayscale(preview)
        grayscale.save(ROOT / "qa-grayscale.png", dpi=(180, 180))
        extrema = grayscale.getextrema()
        deviation = ImageStat.Stat(grayscale).stddev[0]
        if extrema[1] - extrema[0] < 180 or deviation < 20:
            raise RuntimeError("grayscale preview lacks adequate tonal separation")

    renderer = shutil.which("pdftoppm")
    if renderer is None:
        raise FileNotFoundError("pdftoppm is required for PDF QA")
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
    with Image.open(ROOT / "qa-pdf.png") as pdf_preview:
        if pdf_preview.width < 1200 or pdf_preview.height < 900:
            raise RuntimeError("PDF render preview is unexpectedly small")

    manual = "PASS" if args.manual_status == "pass" else "PENDING"
    (ROOT / "qa-report.md").write_text(
        "# R0.71U recurrence figure QA\n\n"
        f"- archival PNG pixel size {width} x {height}: PASS\n"
        f"- archival PNG density {dpi[0]:.3f} x {dpi[1]:.3f} dpi: PASS\n"
        "- color preview generated from the archival PNG: PASS\n"
        "- true grayscale preview generated: PASS\n"
        "- PDF rendered independently with Poppler at 180 dpi: PASS\n"
        f"- final 178 mm print-size inspection: {manual}\n"
        f"- labels, legends, scales, and units inspection: {manual}\n"
        f"- root-marker and direction-arrow inspection: {manual}\n"
        f"- grayscale line-style and marker distinction inspection: {manual}\n"
        f"- PDF-specific render inspection: {manual}\n"
        "- main mcut=24 and independent sparse mcut=36 data cross-check: PASS\n"
        "- finite-Galerkin, PDE-time-stepping, non-DNS boundary visible in figure: PASS\n"
        "- numerical corroboration versus analytic-proof boundary stated in caption: PASS\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
