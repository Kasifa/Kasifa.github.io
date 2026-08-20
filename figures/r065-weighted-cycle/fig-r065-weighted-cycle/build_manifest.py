#!/usr/bin/env python3
"""Build the formal R0.65 weighted-cycle figure manifest."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def asset(path: Path, schema: str, format_name: str) -> dict[str, object]:
    return {
        "path": path.name,
        "format": format_name,
        "schema": schema,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def resource_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def maximum_rss(path: Path) -> float:
    return max(float(row["rssMiB"]) for row in resource_rows(path))


def elapsed(path: Path) -> float:
    return max(float(row["elapsedSeconds"]) for row in resource_rows(path))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--certificate-commit", required=True)
    arguments = parser.parse_args()
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text(encoding="utf-8"))
    png = Image.open(HERE / "figure.png")
    data = [
        asset(
            HERE / "cycle-enclosures.csv",
            "24 exact finite-scale intervals with signs, normalized coefficients, Taylor tails, and 23 certified block-ratio intervals",
            "csv",
        ),
        asset(
            HERE / "figure-data-metadata.json",
            "pinned source and certificate commits, certificate hash, final interval summary, environment, and extraction time",
            "json",
        ),
    ]
    outputs = [
        {
            "path": name,
            "bytes": (HERE / name).stat().st_size,
            "sha256": sha256(HERE / name),
        }
        for name in ("figure.pdf", "figure.svg", "figure.png")
    ]
    outputs[-1].update({"dpi": 600, "pixels": f"{png.width} by {png.height}"})
    manifest = {
        "schemaVersion": "1.0",
        "figureId": "fig-r065-weighted-cycle",
        "status": "formal",
        "analyticalQuestion": (
            "What happens to the complete heat-integrated quartic scalar along "
            "the explicit 0100 target cycle through r=24?"
        ),
        "supportedClaim": (
            "Exact integer moments and rational simplex enclosures certify that the sign changes at r=14; "
            "all ten block transitions r=15 through r=24 have absolute growth above 16; "
            "the final ratio lies in (25.29,25.30). This finite certificate does not prove asymptotic growth "
            "or failure of a uniform quartic estimate."
        ),
        "createdAt": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": arguments.source_commit,
            "certificateCommit": arguments.certificate_commit,
            "dirtyAtCertifiedRun": False,
        },
        "chartContract": {
            "family": "two coordinated ordered-axis diagnostics",
            "variants": [
                "signed normalized coefficient on a symmetric-log scale",
                "absolute four-level block ratio on a logarithmic scale with two exact references",
            ],
            "takeaway": (
                "The heat-integrated scalar changes phase and exhibits a ten-block certified supercritical run, "
                "while the finite inference boundary remains explicit."
            ),
            "dataSufficiency": (
                "Twenty-four consecutive cycle counts, twenty-three ratio intervals, exact integer moments through "
                "degree 96, an order-48 rational Taylor enclosure, and four direct-path cross-checks."
            ),
            "palettePolicy": "hard two-root cap: blue for positive/structural data, rust for negative/supercritical emphasis, neutral references",
            "nonColorEncoding": "open circles versus filled squares, zero and dashed threshold rules, direct annotations, and a shaded certified run",
            "outputFootprint": "double-column journal figure at 178 by 96 millimetres, with PDF, SVG, and 600 dpi PNG exports",
            "finalQaSurface": "color PNG, true grayscale conversion, and Poppler-rendered PDF at final size",
        },
        "computation": {
            "kind": "exact-moment rational-interval audit",
            "command": (
                "python3 research/quartic_weighted_cycle_audit.py --profile publication --max-r 24 "
                "--order 48 --time-series-terms 120 --output research/certificates/r065/weighted-cycle-audit.json"
            ),
            "configuration": (
                "48 sign/carry states, bivariate raw moments through total degree 96, target word 0100 repeated "
                "24 times, order-48 simplex series, and exact rational time and remainder bounds"
            ),
            "precision": "Python integers and Fractions for certified endpoints; decimal values only for display",
            "solver": "exact binomial moment transport, complete-homogeneous rate polynomials, and rational interval evaluation",
            "wallTimeSeconds": metadata["samplingWallSeconds"] + elapsed(HERE / "plot-resources.csv"),
            "randomSeed": "not applicable; no randomness",
            "monitoring": {
                "enabled": True,
                "reportIntervalSeconds": 0.1,
                "resourceLogs": ["figure-data-resources.csv", "plot-resources.csv"],
                "failedAttempts": [],
            },
        },
        "compute": {
            "host": "local Mac workstation",
            "operatingSystem": "macOS 26.6.1 arm64",
            "cpu": "Apple M5 Max",
            "gpu": "not used",
            "memoryGiB": 36,
            "processes": 1,
            "threadsPerProcess": 1,
            "maximumObservedFinalPlotRssMiB": maximum_rss(HERE / "plot-resources.csv"),
        },
        "environment": {
            "python": "3.12.13",
            "matplotlib": "3.11.1",
            "packagesLock": "requirements-research.txt",
        },
        "sourceData": [],
        "data": data,
        "figure": {
            "script": "plot.py",
            "scriptSha256": sha256(HERE / "plot.py"),
            "command": (
                "PYTHONPATH=tmp/r062-python MPLCONFIGDIR=tmp/r065-mplconfig python3 "
                "figures/r065-weighted-cycle/fig-r065-weighted-cycle/plot.py"
            ),
            "profile": "journal-default",
            "widthMillimetres": 178,
            "heightMillimetres": 96,
            "outputs": outputs,
        },
        "caption": {
            "english": "caption.md",
            "chineseSiteSummary": (
                "R0.65 用精确矩和有理余项认证了热加权周期族在 r=14 变号、随后十个四层块绝对增长均超过 16；有限证书不等于渐近定理。"
            ),
        },
        "qa": {
            "status": "passed",
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
            "pdfFontsEmbedded": True,
            "pdfTextExtracted": True,
            "notes": (
                "The final color export, true grayscale conversion, and Poppler-rendered PDF were inspected at "
                "178 by 96 mm. Sign markers, threshold lines, annotations, and the finite inference boundary remain legible."
            ),
        },
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
