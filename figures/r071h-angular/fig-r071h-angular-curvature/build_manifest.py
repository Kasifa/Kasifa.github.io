#!/usr/bin/env python3
"""Build the R0.71H manifest and SHA-256 ledger after validation."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
ASSET_NAMES = [
    "README.md",
    "caption.md",
    "figure-contract.md",
    "contract.json",
    "command.txt",
    "environment.txt",
    "generate_data.py",
    "plot.py",
    "validate_data.py",
    "independent_validate.py",
    "qa_images.py",
    "build_manifest.py",
    "data.csv",
    "figure-data-metadata.json",
    "validation.json",
    "independent-validation.json",
    "figure.pdf",
    "figure.svg",
    "figure.png",
    "qa-original.png",
    "qa-grayscale.png",
    "qa-report.md",
]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def description(name: str) -> dict[str, object]:
    path = ROOT / name
    result: dict[str, object] = {
        "path": name,
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }
    if name.endswith(".png"):
        with Image.open(path) as image:
            result["pixels"] = f"{image.width} by {image.height}"
        if name == "figure.png":
            result["dpi"] = 600
    return result


def main() -> None:
    missing = [name for name in ASSET_NAMES if not (ROOT / name).is_file()]
    if missing:
        raise FileNotFoundError(f"missing assets: {missing}")

    metadata = json.loads((ROOT / "figure-data-metadata.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "independent-validation.json").read_text(encoding="utf-8"))
    base_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    with Image.open(ROOT / "figure.png") as image:
        figure_pixels = f"{image.width} by {image.height}"

    outputs = [description(name) for name in ASSET_NAMES]
    by_name = {str(item["path"]): item for item in outputs}
    payload = {
        "schemaVersion": "1.0",
        "release": "R0.71H",
        "status": "formal",
        "figureId": "fig-r071h-angular-curvature",
        "createdAt": "2026-08-25T22:30:00+08:00",
        "repositoryBaseCommit": base_commit,
        "sourceState": "formal package generated during the R0.71H release construction",
        "analyticalQuestion": (
            "Does the exact projective heat identity yield the weighted-BV budget needed by R0.71G, "
            "or do pointwise angular growth, cutoff source saturation, and a two-power frequency gap remain?"
        ),
        "supportedClaim": (
            "Pure heat has an exact projective-curvature payment identity. A fixed-energy global-smooth "
            "2D3C family rules out a uniform energy-only pointwise angular-speed bound at t=0, while its "
            "source density stays finite. A fixed Fourier cutoff produces finite Rayleigh and source quotients. "
            "The direct weighted-BV Young estimate asks for two more powers of frequency than the known heat bulk."
        ),
        "claimBoundary": (
            "Closed-form finite-dimensional identities, exact initial-time Fourier algebra, and scaling "
            "bookkeeping only; no DNS, fitting, time-evolved 3D simulation, general integrated angular no-go, "
            "regularity theorem, singularity claim, originality claim, or Millennium-problem claim."
        ),
        "computation": {
            "kind": "closed-form formula evaluation with independent Decimal recomputation",
            "precision": "IEEE binary64 producer; 60-digit Decimal independent checker",
            "pdeTimeStepping": False,
            "dns": False,
            "fittedData": False,
            "randomSeed": None,
        },
        "compute": {
            "host": "local Mac workstation, Apple Silicon arm64",
            "processes": 1,
            "gpu": "not used",
            "dgx": "not used",
        },
        "data": {
            "path": "data.csv",
            "rows": metadata["rows"],
            "bytes": by_name["data.csv"]["bytes"],
            "sha256": by_name["data.csv"]["sha256"],
        },
        "figure": {
            "profile": "journal-default",
            "widthMillimetres": 178,
            "heightMillimetres": 108,
            "script": "plot.py",
            "outputs": [
                by_name["figure.pdf"],
                by_name["figure.svg"],
                {
                    **by_name["figure.png"],
                    "dpi": 600,
                    "pixels": figure_pixels,
                },
            ],
        },
        "qa": {
            "automaticChecks": "validation.json",
            "automaticCheckCount": len(validation["checks"]),
            "independentChecks": "independent-validation.json",
            "independentCheckCount": len(independent["checks"]),
            "manualReport": "qa-report.md",
            "originalPreview": "qa-original.png",
            "grayscalePreview": "qa-grayscale.png",
            "status": "passed",
            "maximumFormulaError": validation["metrics"]["maximumFormulaError"],
            "maximumIndependentDecimalFormulaError": independent["metrics"]["maximumDecimalFormulaError"],
        },
        "outputs": outputs,
    }
    (ROOT / "manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    ledger_names = sorted(ASSET_NAMES + ["manifest.json"])
    ledger = "".join(f"{digest(ROOT / name)}  {name}\n" for name in ledger_names)
    (ROOT / "SHA256SUMS").write_text(ledger, encoding="utf-8")


if __name__ == "__main__":
    main()
