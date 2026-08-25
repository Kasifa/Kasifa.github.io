#!/usr/bin/env python3
"""Independent Decimal and binary-archive audit for the R0.71L figure."""

from __future__ import annotations

import argparse
import csv
import json
import struct
from decimal import Decimal, getcontext
from pathlib import Path


getcontext().prec = 80


def require(condition, label, checks):
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def png_info(path):
    payload = path.read_bytes()
    if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
        raise AssertionError("not PNG")
    return struct.unpack(">II", payload[16:24])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.csv"))
    parser.add_argument("--output", type=Path, default=Path("independent-validation.json"))
    args = parser.parse_args()
    with args.data.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    grouped = {}
    for row in rows:
        grouped.setdefault((row["panel"], row["series"]), []).append(row)
    checks = {}
    left = grouped[("A", "localizedLaplacian")]
    right = grouped[("A", "rawCollarContribution")]
    residual = max(abs(Decimal(a["value"]) + Decimal(b["value"])) for a, b in zip(left, right))
    require(residual == 0, "decimalExactCancellation", checks)
    bmap = {row["category"]: Decimal(row["value"]) for row in grouped[("B", "integratedCoefficient")]}
    tangent = abs(bmap["heat tangent"] + bmap["raw collar"] - bmap["fused tangent"])
    joint = abs(bmap["radial"] + bmap["fused tangent"] + bmap["normalization"] - bmap["joint source"])
    require(tangent < Decimal("2e-14"), "decimalTangentFusion", checks)
    require(joint < Decimal("2e-14"), "decimalJointFusion", checks)
    for name, signature in (("figure.pdf", b"%PDF"), ("figure.svg", b"<?xml")):
        require(Path(name).read_bytes().startswith(signature), f"{name}Signature", checks)
    width, height = png_info(Path("figure.png"))
    require(width >= 4200, "pngWidthAtLeast4200", checks)
    require(height >= 2600, "pngHeightAtLeast2600", checks)
    payload = {
        "release": "R0.71L",
        "status": "pass",
        "method": "separate Python-standard-library Decimal and binary archive path; no producer import",
        "checks": checks,
        "metrics": {
            "decimalCancellationResidual": str(residual),
            "decimalTangentFusionResidualScaled": str(tangent),
            "decimalJointFusionResidualScaled": str(joint),
            "pngPixels": f"{width} by {height}",
        },
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
