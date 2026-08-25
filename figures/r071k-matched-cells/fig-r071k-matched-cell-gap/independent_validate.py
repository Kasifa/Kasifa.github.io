#!/usr/bin/env python3
"""Independent Decimal and archive audit for the R0.71K figure."""

from __future__ import annotations

import argparse
import csv
import json
import math
import struct
from decimal import Decimal, getcontext
from pathlib import Path


getcontext().prec = 80


def require(condition: bool, label: str, checks: dict[str, bool]) -> None:
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def decimal_amplitude(theta: Decimal) -> Decimal:
    exp = lambda power: (-Decimal(power) * theta).exp()
    b_value = Decimal(4) * (exp(34) - exp(52))
    d_value = Decimal(32) * exp(32) + Decimal(1156) * exp(34) + Decimal(50) * exp(50) + Decimal(2704) * exp(52)
    y_value = Decimal(2) * exp(2) + Decimal(2) * exp(32) + Decimal(68) * exp(34) + Decimal(2) * exp(50) + Decimal(104) * exp(52)
    return Decimal(0) if b_value == 0 else b_value * b_value / (d_value * y_value)


def png_info(path: Path) -> tuple[int, int]:
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
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault((row["panel"], row["series"]), []).append(row)
    for selected in grouped.values():
        selected.sort(key=lambda row: Decimal(row["x"]))
    checks: dict[str, bool] = {}
    require(len(rows) == 1477, "rowCount", checks)
    require(len(grouped[("A", "partitionSum")]) == 301, "partitionRows", checks)
    partition_residual = max(abs(Decimal(row["value"]) - Decimal(1)) for row in grouped[("A", "partitionSum")])
    require(partition_residual < Decimal("4e-15"), "partitionUnity", checks)

    theta_star = Decimal(2).ln() / Decimal(18)
    a_star = decimal_amplitude(theta_star)
    global_endpoint = Decimal(grouped[("B", "globalEndpoint")][0]["value"])
    require(global_endpoint == Decimal(1), "globalEndpoint", checks)
    require(Decimal(grouped[("B", "globalAmplitude")][0]["value"]) == 0, "zeroEntry", checks)
    local_endpoint = Decimal(grouped[("B", "localTemplateEndpoint")][0]["value"])
    require(local_endpoint > global_endpoint, "localDiagnosticPositive", checks)

    maximum_power_error = Decimal(0)
    ratios = []
    for creation_row, heat_row in zip(grouped[("C", "creationPower")], grouped[("C", "heatPower")]):
        frequency = Decimal(creation_row["x"])
        creation = Decimal(creation_row["value"])
        heat = Decimal(heat_row["value"])
        maximum_power_error = max(maximum_power_error, abs(creation - frequency**-2), abs(heat - frequency**-4))
        ratios.append(creation / heat / frequency**2)
    require(maximum_power_error < Decimal("2e-20"), "exactPowers", checks)
    require(max(ratios) - min(ratios) < Decimal("2e-14"), "quadraticRatio", checks)

    archive_checks = {}
    for name, signature in (("figure.pdf", b"%PDF"), ("figure.svg", b"<?xml")):
        path = Path(name)
        archive_checks[f"{name}Exists"] = path.is_file()
        archive_checks[f"{name}Signature"] = path.read_bytes().startswith(signature) if path.is_file() else False
    png_path = Path("figure.png")
    archive_checks["figure.pngExists"] = png_path.is_file()
    if png_path.is_file():
        width, height = png_info(png_path)
        archive_checks["figure.pngWidthAtLeast4200"] = width >= 4200
        archive_checks["figure.pngHeightAtLeast2600"] = height >= 2600
    for key, value in archive_checks.items():
        require(value, key, checks)

    payload = {
        "release": "R0.71K",
        "status": "pass",
        "method": "separate Python-standard-library Decimal and binary archive path; no producer import",
        "checks": checks,
        "metrics": {
            "maximumPartitionResidual": str(partition_residual),
            "maximumDecimalPowerError": str(maximum_power_error),
            "AStar80Digit": str(a_star),
            "localEndpointOverAStarFromCsv": str(local_endpoint),
        },
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
