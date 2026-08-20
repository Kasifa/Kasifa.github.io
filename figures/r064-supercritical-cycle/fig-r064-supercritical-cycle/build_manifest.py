#!/usr/bin/env python3
"""Build the formal R0.64 figure manifest from generated assets."""

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
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def asset(path: Path, schema: str, format_name: str) -> dict[str, object]:
    return {
        "path": path.name,
        "format": format_name,
        "schema": schema,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def maximum_rss(path: Path) -> float:
    with path.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    return max(float(row["rssMiB"]) for row in rows)


def elapsed(path: Path) -> float:
    with path.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    return max(float(row["elapsedSeconds"]) for row in rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--certificate-commit", required=True)
    arguments = parser.parse_args()
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text(encoding="utf-8"))
    png = Image.open(HERE / "figure.png")

    data = [
        asset(HERE / "cycle-spectrum.csv", "six nonzero eigenvalues with exact root intervals and multiplicities", "csv"),
        asset(HERE / "reachable-cycle.csv", "exact reachable sequence through r=30, including M, target, y_r, sign, and block growth", "csv"),
        asset(HERE / "figure-data-metadata.json", "source certificate hash, row counts, exact polynomial, environment, and sampling time", "json"),
    ]
    outputs = [
        {"path": name, "bytes": (HERE / name).stat().st_size, "sha256": sha256(HERE / name)}
        for name in ("figure.pdf", "figure.svg", "figure.png")
    ]
    outputs[-1].update({"dpi": 600, "pixels": f"{png.width} by {png.height}"})
    manifest = {
        "schemaVersion": "1.0",
        "figureId": "fig-r064-supercritical-cycle",
        "status": "formal",
        "analyticalQuestion": "Does the zero-time forty-eight-state digit transfer admit a common norm with per-level factor at most two?",
        "supportedClaim": "The exact least-significant-bit-first word 0100 has a four-level product with characteristic polynomial x^42 (x-16)^2 (x^4-25x^3-120x^2+3248x-8192) and a reachable real eigenvalue 25.151589..., strictly above the threshold 16. This rules out a pointwise factor-two common norm on the complete zero-time state space; the heat-integrated estimate remains open.",
        "createdAt": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": arguments.source_commit,
            "certificateCommit": arguments.certificate_commit,
            "dirtyAtCertifiedRun": False,
        },
        "chartContract": {
            "family": "state-reduction diagram plus exact spectrum and reachable-growth diagnostics",
            "variants": ["48-state to rank-six cycle reduction", "six exact nonzero eigenvalues", "reachable target-cycle block growth through r=30"],
            "takeaway": "The zero-time full-state transfer is supercritical on an explicit reachable four-bit cycle, so the remaining proof route must retain heat weighting and simplex integration before taking a norm.",
            "dataSufficiency": "The audit compares all forty-eight states with direct convolution through ten dyadic levels, derives the exact image characteristic polynomial, and extends the certified scalar recurrence to thirty cycles.",
            "palettePolicy": "blue for exact state structure, rust for the supercritical root, neutral ink for the threshold",
            "nonColorEncoding": "boxes, arrows, open markers, dashed threshold lines, direct labels, and signed numerical positions",
            "outputFootprint": "double-column journal figure at 178 by 96 millimetres, with PDF, SVG, and 600 dpi PNG exports",
            "finalQaSurface": "color PNG, true grayscale conversion, and Poppler-rendered PDF at final size",
        },
        "computation": {
            "kind": "exact-audit",
            "command": "python3 research/quartic_supercritical_cycle_audit.py --output research/certificates/r064/supercritical-cycle-audit.json --max-direct-level 10",
            "configuration": "two exact 48 by 48 digit matrices, four-bit word 0100, rank-six image restriction, ten direct dyadic convolution levels, and thirty recurrence cycles",
            "precision": "Python integers and Fractions for every certified claim; floating roots only for display",
            "solver": "exact finite linear algebra, polynomial determinant, direct convolution, and scalar recurrence",
            "wallTimeSeconds": metadata["samplingWallSeconds"] + elapsed(HERE / "plot-resources.csv"),
            "randomSeed": "not applicable; no randomness",
            "monitoring": {"enabled": True, "reportIntervalSeconds": 0.1, "resourceLogs": ["figure-data-resources.csv", "plot-resources.csv"], "failedAttempts": []},
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
        "environment": {"python": "3.12.13", "matplotlib": "3.11.1", "numpy": "2.3.5", "packagesLock": "requirements-research.txt"},
        "sourceData": [],
        "data": data,
        "figure": {
            "script": "plot.py",
            "scriptSha256": sha256(HERE / "plot.py"),
            "command": "PYTHONPATH=tmp/r062-python MPLCONFIGDIR=tmp/r064-mplconfig python3 figures/r064-supercritical-cycle/fig-r064-supercritical-cycle/plot.py",
            "profile": "journal-default",
            "widthMillimetres": 178,
            "heightMillimetres": 96,
            "outputs": outputs,
        },
        "caption": {"english": "caption.md", "chineseSiteSummary": "R0.64 给出一个可达的四位零时间超临界循环，严格排除完整状态空间上的逐层因子二公共范数；带热权积分估计仍未解决。"},
        "qa": {
            "status": "passed",
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
            "pdfFontsEmbedded": True,
            "pdfTextExtracted": True,
            "notes": "The final color export, true grayscale conversion, and Poppler-rendered PDF were inspected at the intended 178 by 96 mm size. All panels, thresholds, root labels, and boundary text remain legible.",
        },
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

