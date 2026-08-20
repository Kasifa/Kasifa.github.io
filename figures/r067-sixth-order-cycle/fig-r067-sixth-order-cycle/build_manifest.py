#!/usr/bin/env python3
"""Build the formal R0.67A sixth-order figure manifest."""

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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--certificate-commit", required=True)
    arguments = parser.parse_args()
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text(encoding="utf-8"))
    png = Image.open(HERE / "figure.png")
    data = [
        asset(
            HERE / "reachable-sequence.csv",
            "40 exact target values with display normalizations by mu^r and 256^r",
            "csv",
        ),
        asset(
            HERE / "spectral-enclosures.csv",
            "four exact quartic root intervals and one strict degree-ten Schur disk",
            "csv",
        ),
        asset(
            HERE / "thresholds.csv",
            "C2 zero-affine threshold, dominant-root interval, and absolute carry eigenvalue",
            "csv",
        ),
        asset(
            HERE / "figure-data-metadata.json",
            "pinned commits, certificate hash, theorem intervals, and extraction environment",
            "json",
        ),
        asset(
            HERE / "figure-data-resources.csv",
            "elapsed time, resident memory, and exit status for deterministic extraction",
            "csv",
        ),
        asset(
            HERE / "plot-resources.csv",
            "elapsed time, resident memory, and exit status for final rendering",
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
    resources = resource_rows(HERE / "plot-resources.csv")
    manifest = {
        "schemaVersion": "1.0",
        "figureId": "fig-r067-sixth-order-cycle",
        "status": "formal",
        "analyticalQuestion": (
            "Does the exact reachable zero-time sixth-order target contain a spectral mode "
            "above the conditional four-free-coordinate C1,1 zero-affine scale?"
        ),
        "supportedClaim": (
            "Exact 320-state arithmetic proves Y_r=C6,0 mu^r+O(300^r), with C6,0 strictly "
            "negative and 402.425429345624<mu<402.4254293456256. Hence |Y_r|/256^r tends "
            "to infinity. The complete heat-weighted five-simplex projection is not certified."
        ),
        "createdAt": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": arguments.source_commit,
            "certificateCommit": arguments.certificate_commit,
            "dirtyAtCertifiedRun": False,
        },
        "chartContract": {
            "family": "one convergence diagnostic, one spectral-enclosure strip, and one threshold-growth panel",
            "takeaway": "the reachable dominant root lies above both the conditional 256 C2 zero-affine scale and every degree-ten mode",
            "dataSufficiency": "40 exact recurrence values, seven direct levels, two-prime rank checks, ten Schur transforms, and 14 passing checks",
            "palettePolicy": "blue/open for finite and structural values; rust/filled for the dominant theorem; neutral references",
            "nonColorEncoding": "marker shape and fill, interval bars, a shaded disk, dashed asymptotic guide, and direct labels",
            "outputFootprint": "double-column 178 by 108 millimetres with PDF, SVG, and 600 dpi PNG",
            "finalQaSurface": "color PNG, true grayscale conversion, and Poppler-rendered PDF at final size",
        },
        "computation": {
            "kind": "exact-audit",
            "command": "python3 research/sixth_order_cycle_audit.py --max-direct-level 7 --sequence-terms 40 --progress --output research/certificates/r067/sixth-order-cycle-audit.json",
            "configuration": "320 direct sign/carry states, 36-dimensional cycle image, 40 target terms, and exact C2 carry weight",
            "precision": "Python integers and Fractions for proof fields; 80-digit Decimal only for plotted display values",
            "solver": "exact digit transfer, two-prime rank audits, exact characteristic polynomial, Schur transforms, rational recurrence, and interval spectral projection",
            "wallTimeSeconds": (
                0.72
                + metadata["samplingWallSeconds"]
                + max(float(row["elapsedSeconds"]) for row in resources)
            ),
            "randomSeed": "not applicable; no randomness",
            "monitoring": {
                "enabled": True,
                "resourceLogs": [
                    "research/certificates/r067/sixth-order-cycle-audit.stderr.log",
                    "figure-data-resources.csv",
                    "plot-resources.csv",
                ],
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
            "maximumObservedFormalAuditRssMiB": 45760512 / (1024 * 1024),
            "maximumObservedFinalPlotRssMiB": max(float(row["rssMiB"]) for row in resources),
        },
        "environment": {
            "python": metadata["environment"]["python"],
            "matplotlib": "3.11.1",
            "packagesLock": "requirements-research.txt",
        },
        "sourceData": [
            {
                "location": metadata["certificate"],
                "fileName": "sixth-order-cycle-audit.json",
                "bytes": 20442,
                "sha256": metadata["certificateSha256"],
                "extractionCommand": "python3 figures/r067-sixth-order-cycle/fig-r067-sixth-order-cycle/prepare_data.py",
            }
        ],
        "data": data,
        "figure": {
            "script": "plot.py",
            "scriptSha256": sha256(HERE / "plot.py"),
            "command": (
                "PYTHONPATH=tmp/r062-python MPLCONFIGDIR=tmp/r067-mplconfig python3 "
                "figures/r067-sixth-order-cycle/fig-r067-sixth-order-cycle/plot.py"
            ),
            "profile": "journal-default",
            "widthMillimetres": 178,
            "heightMillimetres": 108,
            "outputs": outputs,
        },
        "caption": {
            "english": "caption.md",
            "chineseSiteSummary": (
                "R0.67A 用精确 320 状态转移证明零时间六阶可达标量满足 "
                "Y_r=C_{6,0}mu^r+O(300^r)，且 C_{6,0}<0、mu>400；完整热核投影仍待证明。"
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
            "pdfTextExtracted": False,
            "notes": (
                "The final color export, true grayscale conversion, and Poppler-rendered PDF were "
                "inspected at 178 by 108 mm. The sign change, four quartic intervals, complete "
                "radius-300 Schur disk, conditional 256 zero-affine scale, asymptotic guide, and "
                "heat-projection claim boundary remain legible. PDF text extraction was unavailable "
                "in the local bundle; vector rendering was verified directly."
            ),
        },
        "claimBoundary": (
            "Zero-time fixed-order correlation only; no complete heat projection, full Picard-series control, "
            "norm inflation, singularity, global regularity, or Millennium-problem claim."
        ),
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
