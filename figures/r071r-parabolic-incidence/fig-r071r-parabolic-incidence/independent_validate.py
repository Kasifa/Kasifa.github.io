#!/usr/bin/env python3
"""Independent asset and CSV validation for the R0.71R figure."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.data.parent
    rows = list(csv.DictReader(args.data.open(encoding="utf-8")))
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(label: str, condition: bool, detail: object) -> None:
        if not condition:
            raise AssertionError(label)
        checks.append({"label": label, "passed": True, "detail": detail})

    check("metadata row count", len(rows) == metadata["rows"], len(rows))
    check("PDF one page", len(PdfReader(str(root / "figure.pdf")).pages) == 1, 1)
    svg = (root / "figure.svg").read_text(encoding="utf-8")
    for token in ("Critical scaling", "genuine NSE initial jet", "Degree-zero entry", "Bounded source"):
        check(f"SVG contains {token}", token in svg, token)
    with Image.open(root / "figure.png") as image:
        check("PNG sufficiently large", image.width >= 3500 and image.height >= 2400, [image.width, image.height])
        dpi = image.info.get("dpi", (0, 0))
        check("PNG 600 dpi", min(dpi) > 590, dpi)
    result = {"status": "passed", "checkCount": len(checks), "method": "standalone CSV/PDF/SVG/PNG inspection using csv, Pillow, and pypdf", "checks": checks}
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
