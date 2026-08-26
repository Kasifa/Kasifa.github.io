#!/usr/bin/env python3
"""Independent CSV and asset validation for the R0.71S journal figure."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
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
    check("all four panels", {row["panel"] for row in rows} == {"A", "B", "C", "D"}, sorted({row["panel"] for row in rows}))

    a_rows = [row for row in rows if row["panel"] == "A"]
    a_error = 0.0
    for row in a_rows:
        k = float(row["x"])
        expected = 8.0 * k**2 if row["series"] == "critical H^-1 packet cost" else 8.0
        a_error = max(a_error, abs(float(row["y"]) / expected - 1.0))
    check("box packet scaling reconstructed", a_error < 2e-14, a_error)

    b_rows = [row for row in rows if row["panel"] == "B"]
    b_error = 0.0
    for overlap in sorted({int(float(row["x"])) for row in b_rows}):
        indices = np.arange(64, dtype=np.float64)
        gram = np.maximum(
            0.0,
            1.0 - np.abs(indices[:, None] - indices[None, :]) / overlap,
        )
        reconstructed = float(np.linalg.eigvalsh(gram)[-1])
        recorded = next(
            float(row["y"]) for row in b_rows
            if int(float(row["x"])) == overlap
            and row["series"] == "largest eigenvalue"
        )
        b_error = max(b_error, abs(reconstructed - recorded))
    check("finite Gram eigenvalues independently rebuilt", b_error < 3e-12, b_error)

    c_rows = [row for row in rows if row["panel"] == "C"]
    c_error = 0.0
    theta = float(metadata["parameters"]["theta"])
    viscosity = float(metadata["parameters"]["nu"])
    for row in c_rows:
        k = float(row["x"])
        critical = 0.5 * viscosity * k**2 / math.tanh(0.5 * viscosity * theta)
        expected = critical if row["series"] == "critical H^-1 heat cost" else critical / k**2
        c_error = max(c_error, abs(float(row["y"]) / expected - 1.0))
    check("adjoint heat constants independently rebuilt", c_error < 3e-14, c_error)

    d_rows = [row for row in rows if row["panel"] == "D"]
    d_error = 0.0
    for row in d_rows:
        exponent = int(float(row["x"]))
        half = 2.0 ** (4 * exponent) / (2.0 ** (4 * exponent) + 1.0)
        if row["series"] == "positive face response":
            expected = half
        elif row["series"] == "Jordan response":
            expected = 2.0 * half
        else:
            expected = 0.0
        d_error = max(d_error, abs(float(row["y"]) - expected))
    check("even-touch responses independently rebuilt", d_error < 3e-14, d_error)

    exact = json.loads((root / "exact-certificate.json").read_text(encoding="utf-8"))
    independent = json.loads((root / "independent-certificate.json").read_text(encoding="utf-8"))
    check(
        "embedded certificates passed",
        exact["release"] == independent["release"] == "R0.71S"
        and exact["status"] == independent["status"] == "passed",
        [exact["status"], independent["status"]],
    )
    check("PDF one page", len(PdfReader(str(root / "figure.pdf")).pages) == 1, 1)
    svg = (root / "figure.svg").read_text(encoding="utf-8")
    for token in (
        "Box mean",
        "Same-direction packet Gram",
        "Adjoint heat mean",
        "Even touch",
        "not an NSE trajectory",
    ):
        check(f"SVG contains {token}", token in svg, token)
    with Image.open(root / "figure.png") as image:
        check(
            "PNG sufficiently large",
            image.width >= 3500 and image.height >= 2400,
            [image.width, image.height],
        )
        dpi = image.info.get("dpi", (0, 0))
        check("PNG 600 dpi", min(dpi) > 590, dpi)
    boundary = metadata["claimBoundary"]
    check(
        "NSE initial-face boundary is metadata only",
        "a_K=a0*K" in boundary
        and "K^-2*A_plus=a0^2/4" in boundary
        and "not plotted as a positive-time result" in boundary,
        boundary,
    )
    result = {
        "status": "passed",
        "checkCount": len(checks),
        "method": (
            "standalone CSV reconstruction with NumPy plus independent "
            "PDF/SVG/PNG and certificate inspection"
        ),
        "checks": checks,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
