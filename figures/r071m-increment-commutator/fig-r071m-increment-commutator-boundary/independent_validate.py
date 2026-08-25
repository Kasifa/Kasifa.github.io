#!/usr/bin/env python3
"""Independent Decimal and binary-archive audit for the R0.71M figure."""

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

    components = grouped[("A", "signedPairingComponent")]
    total = grouped[("A", "signedPairingTotal")][0]
    component_residual = abs(
        sum(Decimal(row["value"]) for row in components) - Decimal(total["value"])
    )
    require(component_residual < Decimal("5e-12"), "decimalPairingComponents", checks)

    fractions = grouped[("B", "normalizedCriticalRowSquare")]
    fraction_residual = abs(
        sum(Decimal(row["value"]) for row in fractions) - Decimal(1)
    )
    require(fraction_residual < Decimal("5e-15"), "decimalRowFractions", checks)

    for series, exponent in (
        ("energy", 0),
        ("YuQuarticDefect", -2),
        ("velocityCarleson", -1),
        ("normalizedLamb", -1),
    ):
        for row in grouped[("C", series)]:
            radius = Decimal(row["x"])
            expected = radius**exponent
            require(
                abs(Decimal(row["value"]) - expected)
                < Decimal("1e-12") * max(expected, Decimal(1)),
                f"decimalScaling_{series}_{row['x']}",
                checks,
            )

    for name, signature in (("figure.pdf", b"%PDF"), ("figure.svg", b"<?xml")):
        require(Path(name).read_bytes().startswith(signature), f"{name}Signature", checks)
    width, height = png_info(Path("figure.png"))
    require(width >= 4200, "pngWidthAtLeast4200", checks)
    require(height >= 2600, "pngHeightAtLeast2600", checks)

    payload = {
        "release": "R0.71M",
        "status": "pass",
        "method": (
            "separate Python-standard-library Decimal and binary archive path; "
            "no producer or certificate import"
        ),
        "checks": checks,
        "metrics": {
            "decimalPairingComponentResidual": str(component_residual),
            "decimalRowFractionResidual": str(fraction_residual),
            "pngPixels": f"{width} by {height}",
        },
    }
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
