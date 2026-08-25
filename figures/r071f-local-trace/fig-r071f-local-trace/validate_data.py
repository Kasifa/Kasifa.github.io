#!/usr/bin/env python3
"""Independent reconstruction and archive validation for R0.71F figure data."""

from __future__ import annotations

import csv
import json
import math
import subprocess
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
FFT_WAVENUMBERS = [1, 2, 4, 8]
WAVENUMBERS = [1, 2, 4, 8, 16, 32, 64, 128]
FFT_TAU = [0.0, 0.125, 0.5, 1.0, 2.0]
RADII = [2.0 ** (-index) for index in range(8)]


def close(first: float, second: float, tolerance: float = 5e-13) -> bool:
    return abs(first - second) <= tolerance * max(1.0, abs(first), abs(second))


with (ROOT / "data.csv").open(newline="", encoding="utf-8") as stream:
    rows = list(csv.DictReader(stream))

profiles = [row for row in rows if row["kind"] == "profile_exact"]
fft = [row for row in rows if row["kind"] == "profile_fft"]
multipliers = [row for row in rows if row["kind"] == "trace_multiplier"]
partitions = [row for row in rows if row["kind"] == "partition_envelope"]
geometry = [row for row in rows if row["kind"] == "geometry_scaling"]

pdf_info = subprocess.run(
    ["pdfinfo", str(ROOT / "figure.pdf")],
    check=True,
    capture_output=True,
    text=True,
).stdout
png = Image.open(ROOT / "figure.png")
metadata = json.loads((ROOT / "figure-data-metadata.json").read_text(encoding="utf-8"))

checks = {
    "rowCount": len(rows) == 526,
    "profileCount": len(profiles) == 241,
    "fftCount": len(fft) == len(FFT_WAVENUMBERS) * len(FFT_TAU),
    "multiplierCount": len(multipliers) == 241,
    "partitionCount": len(partitions) == 2 * len(WAVENUMBERS),
    "geometryCount": len(geometry) == len(RADII),
    "profileReconstruction": all(
        close(float(row["exact_q_ratio"]), math.exp(-2.0 * float(row["tau"])))
        for row in profiles
    ),
    "profileStartsAtOne": close(float(profiles[0]["exact_q_ratio"]), 1.0),
    "fftWavenumbers": sorted({int(row["k"]) for row in fft}) == FFT_WAVENUMBERS,
    "fftTau": sorted({float(row["tau"]) for row in fft}) == FFT_TAU,
    "fftReconstruction": all(
        close(float(row["observed_q_ratio"]), math.exp(-2.0 * float(row["tau"])), 2e-12)
        and close(float(row["exact_q_ratio"]), math.exp(-2.0 * float(row["tau"])))
        for row in fft
    ),
    "fftResidual": max(float(row["relative_error"]) for row in fft) < 2e-12,
    "multiplierReconstruction": all(
        close(
            float(row["trace_multiplier_over_k2"]),
            2.0 / (-math.expm1(-2.0 * float(row["theta"]))),
        )
        and close(float(row["small_theta_reference"]), 1.0 / float(row["theta"]))
        and close(float(row["large_theta_limit"]), 2.0)
        for row in multipliers
    ),
    "partitionReconstruction": all(
        close(float(row["normalized_bottom"]), 1.0)
        and close(float(row["normalized_bulk"]), 1.0 / (2.0 * int(row["k"]) ** 2))
        for row in partitions
    ),
    "partitionWavenumbers": all(
        sorted(int(row["k"]) for row in partitions if row["envelope"] == envelope) == WAVENUMBERS
        for envelope in ("lower", "upper")
    ),
    "geometryReconstruction": all(
        close(float(row["critical_ratio"]), float(row["radius"]) ** -2.0)
        and close(float(row["subcritical_ratio"]), float(row["radius"]) ** -1.5)
        for row in geometry
    ),
    "geometryRadii": [float(row["radius"]) for row in geometry] == RADII,
    "metadataRowCount": metadata["rows"] == len(rows),
    "metadataNoDns": metadata["dns"] is False,
    "metadataNoTimeStepping": metadata["pdeTimeStepping"] is False,
    "pdfOnePage": "Pages:           1" in pdf_info,
    "pdfPageSize178By104Millimetres": "504.567 x 294.803 pts" in pdf_info,
    "pdfNotEncrypted": "Encrypted:       no" in pdf_info,
    "pngDimensions": png.width in (4204, 4205) and png.height in (2456, 2457),
    "pngDpi": all(abs(value - 600) < 1 for value in png.info.get("dpi", (0, 0))),
    "svgPresent": (ROOT / "figure.svg").stat().st_size > 10_000,
    "grayscalePresent": (ROOT / "qa-grayscale.png").stat().st_size > 100_000,
}

if not all(checks.values()):
    raise AssertionError({key: value for key, value in checks.items() if not value})

payload = {
    "release": "R0.71F-independent-figure",
    "status": "pass",
    "method": "fresh CSV formula reconstruction, provenance checks, PDF metadata inspection, and raster dimension checks without importing plot.py",
    "checks": checks,
    "claimBoundary": "Checks displayed formulas and finite FFT points only; no DNS, persistence, critical-trace rejection, singularity, or regularity claim.",
}
(ROOT / "independent-validation.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(payload, indent=2, sort_keys=True))
