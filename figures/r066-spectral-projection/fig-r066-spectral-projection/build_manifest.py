#!/usr/bin/env python3
"""Build the formal R0.66 spectral-projection figure manifest."""

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
    finite_wall_seconds = 669.4400034999999
    spectral_wall_seconds = 0.32733912498224527
    data = [
        asset(
            HERE / "cycle-normalized.csv",
            "24 complete finite quartic coefficients normalized by the midpoint of the certified dominant-root interval",
            "csv",
        ),
        asset(
            HERE / "coefficient-intervals.csv",
            "cycle-100 degree-48 polynomial interval and complete outward dominant-coefficient interval",
            "csv",
        ),
        asset(
            HERE / "error-budget.csv",
            "three independent outward errors, their sum, and the certified distance of the dominant coefficient from zero",
            "csv",
        ),
        asset(
            HERE / "figure-data-metadata.json",
            "pinned source and certificate commits, certificate hashes, theorem intervals, environment, and extraction time",
            "json",
        ),
        asset(
            HERE / "figure-data-resources.csv",
            "elapsed time, resident memory, and exit status for deterministic figure-data extraction",
            "csv",
        ),
        asset(
            HERE / "plot-resources.csv",
            "elapsed time, resident memory, and exit status for final journal rendering",
            "csv",
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
        "figureId": "fig-r066-spectral-projection",
        "status": "formal",
        "analyticalQuestion": (
            "Does the complete heat-weighted coefficient for the explicit 0100 periodic packet "
            "have a nonzero projection onto the dominant affine-block eigenmode?"
        ),
        "supportedClaim": (
            "Exact affine-branch arithmetic and strict outward intervals prove "
            "S_r=C_* lambda^r+O(r 16^r), where 25.1515893341015<lambda<25.1515893341016 "
            "and -2.304456798896e-5<C_*<-2.286527505484e-5. Therefore |S_r|/16^r tends "
            "to infinity for this explicit quartic packet. Higher Picard orders and the full "
            "mild solution are not controlled."
        ),
        "createdAt": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": arguments.source_commit,
            "certificateCommit": arguments.certificate_commit,
            "dirtyAtCertifiedRun": False,
        },
        "chartContract": {
            "family": "one ordered-axis convergence diagnostic and two focused horizontal comparisons",
            "variants": [
                "signed complete finite coefficient normalized by lambda^r on a symmetric-log scale",
                "cycle-100 polynomial interval versus the complete dominant-coefficient interval",
                "logarithmic outward-error budget versus certified distance to zero",
            ],
            "takeaway": (
                "The normalized complete finite coefficients enter a negative band, while the "
                "complete outward dominant-coefficient interval stays strictly below zero."
            ),
            "dataSufficiency": (
                "Twenty-four consecutive complete finite coefficients, one exact degree-48 cycle-100 "
                "polynomial interval, 21 passing spectral checks, and three disjoint outward errors."
            ),
            "palettePolicy": (
                "hard two-root cap: blue/open markers for finite or structural values, rust/filled "
                "markers for the negative theorem, and neutral references"
            ),
            "nonColorEncoding": (
                "open circles versus filled squares and a diamond, zero rules, interval whiskers, "
                "direct annotations, and a shaded certified band"
            ),
            "outputFootprint": (
                "double-column journal figure at 178 by 108 millimetres, with PDF, SVG, and 600 dpi PNG exports"
            ),
            "finalQaSurface": "color PNG, true grayscale conversion, and Poppler-rendered PDF at final size",
        },
        "computation": {
            "kind": "exact-audit plus high-precision presentation sampling",
            "command": (
                "python3 research/quartic_weighted_cycle_finite_iterate.py --profile publication "
                "--cycles 100 --order 24 --output research/certificates/r066/exact-finite-iterate.json && "
                "python3 research/quartic_weighted_cycle_spectral_audit.py --profile publication "
                "--finite-input research/certificates/r066/exact-finite-iterate.json "
                "--output research/certificates/r066/spectral-audit.json"
            ),
            "configuration": (
                "48 sign/carry states, 12,288 exact affine branches, bivariate integer moments through "
                "total degree 48 at cycle 100, order-24 rational heat expansion, and strict decimal "
                "spectral/resolvent enclosures"
            ),
            "precision": (
                "Python integers and Fractions for finite endpoints; 80-digit Decimal arithmetic with "
                "directed outward rounding for spectral and error bounds; display values only in the plotted CSV files"
            ),
            "solver": (
                "exact affine-branch aggregation, characteristic-polynomial isolation, left/right dominant "
                "eigenprojection, weighted zero-mass Kantorovich contraction, and a Neumann-resolvent tail bound"
            ),
            "wallTimeSeconds": (
                finite_wall_seconds
                + spectral_wall_seconds
                + metadata["samplingWallSeconds"]
                + elapsed(HERE / "plot-resources.csv")
            ),
            "randomSeed": "not applicable; no randomness",
            "monitoring": {
                "enabled": True,
                "reportIntervalSeconds": 0.1,
                "resourceLogs": [
                    "research/certificates/r066/exact-finite-iterate.stderr.log",
                    "research/certificates/r066/spectral-audit.stderr.log",
                    "figure-data-resources.csv",
                    "plot-resources.csv",
                ],
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
            "maximumObservedFormalAuditRssMiB": 564232192 / (1024 * 1024),
            "maximumObservedFinalPlotRssMiB": maximum_rss(HERE / "plot-resources.csv"),
        },
        "environment": {
            "python": "3.12.13",
            "matplotlib": "3.11.1",
            "packagesLock": "requirements-research.txt",
        },
        "sourceData": [
            {
                "location": "research/certificates/r065/weighted-cycle-audit.json",
                "fileName": "weighted-cycle-audit.json",
                "bytes": 193686,
                "sha256": "6fc8b439b6aea1848fd86e45ed948bcbe5e8515c5558509da072287d6477911f",
                "extractionCommand": "python3 figures/r066-spectral-projection/fig-r066-spectral-projection/prepare_data.py",
            },
            {
                "location": "research/certificates/r066/exact-finite-iterate.json",
                "fileName": "exact-finite-iterate.json",
                "bytes": 48018,
                "sha256": "7ef26fbd29a996ad6a74b1db79ef05625170aa66cea7bf76dc1e06f0870bac3b",
                "extractionCommand": "python3 figures/r066-spectral-projection/fig-r066-spectral-projection/prepare_data.py",
            },
            {
                "location": "research/certificates/r066/spectral-audit.json",
                "fileName": "spectral-audit.json",
                "bytes": 156184,
                "sha256": "a6f66c8bea8806fee3716b8d6611a2e0720e29969d94d991672cf3626ba8bcb2",
                "extractionCommand": "python3 figures/r066-spectral-projection/fig-r066-spectral-projection/prepare_data.py",
            },
        ],
        "data": data,
        "figure": {
            "script": "plot.py",
            "scriptSha256": sha256(HERE / "plot.py"),
            "command": (
                "PYTHONPATH=tmp/r062-python MPLCONFIGDIR=tmp/r066-mplconfig python3 "
                "figures/r066-spectral-projection/fig-r066-spectral-projection/plot.py"
            ),
            "profile": "journal-default",
            "widthMillimetres": 178,
            "heightMillimetres": 108,
            "outputs": outputs,
        },
        "caption": {
            "english": "caption.md",
            "chineseSiteSummary": (
                "R0.66 用精确仿射分支、谱投影和严格向外误差界证明了一个显式四次包满足 "
                "S_r=C_*lambda^r+O(r16^r)，且 C_*<0；该结论不控制更高 Picard 阶或完整温和解。"
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
                "The final color export, true grayscale conversion, and Poppler-rendered PDF were "
                "inspected at 178 by 108 mm. The sign change, negative coefficient interval, zero rule, "
                "error separation, and higher-order claim boundary remain legible."
            ),
        },
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
