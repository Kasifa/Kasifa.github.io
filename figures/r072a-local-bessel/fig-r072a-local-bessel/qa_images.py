#!/usr/bin/env python3
"""Create final-size, grayscale, and PDF-render QA images for R0.72A-1."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from zoneinfo import ZoneInfo

from PIL import Image


ROOT = Path(__file__).resolve().parent
TIMEZONE = ZoneInfo("Asia/Shanghai")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    figure_config = config["figure"]
    qa_dpi = int(figure_config["qaDpi"])
    width = round(float(figure_config["widthMillimetres"]) / 25.4 * qa_dpi)
    height = round(float(figure_config["heightMillimetres"]) / 25.4 * qa_dpi)

    with Image.open(ROOT / "figure.png") as image:
        original = image.convert("RGB").resize((width, height), Image.Resampling.LANCZOS)
        original.save(ROOT / "qa-original.png", dpi=(qa_dpi, qa_dpi))
        original.convert("L").save(ROOT / "qa-grayscale.png", dpi=(qa_dpi, qa_dpi))

    pdftoppm = shutil.which("pdftoppm")
    if pdftoppm is None:
        raise FileNotFoundError("pdftoppm is required for PDF QA")
    with tempfile.TemporaryDirectory(prefix="r072a-pdfqa-") as temp_dir:
        stem = Path(temp_dir) / "page"
        subprocess.run(
            [pdftoppm, "-png", "-r", str(qa_dpi), "-singlefile", str(ROOT / "figure.pdf"), str(stem)],
            check=True,
            capture_output=True,
        )
        with Image.open(stem.with_suffix(".png")) as pdf_image:
            pdf_image.convert("RGB").save(ROOT / "qa-pdf.png", dpi=(qa_dpi, qa_dpi))

    report = f"""# R0.72A-1 visual QA

Generated: {datetime.now(TIMEZONE).isoformat(timespec='seconds')}

- final-size color inspection: PENDING
- grayscale distinction inspection: PENDING
- PDF render inspection: PENDING
- title, subtitle, labels, legends, and footer clipping: PENDING
- interpretation and claim-boundary review: PENDING

The final reviewer must inspect `qa-original.png`, `qa-grayscale.png`, and
`qa-pdf.png` before replacing PENDING with PASS and recording any revision.
"""
    (ROOT / "qa-report.md").write_text(report, encoding="utf-8")
    print(json.dumps({"status": "qa-images-created", "pixels": [width, height], "dpi": qa_dpi}, indent=2))


if __name__ == "__main__":
    main()
