#!/usr/bin/env python3
"""Independent final-asset validation for the R0.71T figure package."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--producer", type=Path, required=True)
    parser.add_argument("--independent", type=Path, required=True)
    parser.add_argument("--progress", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.data.parent
    rows = list(csv.DictReader(args.data.open(encoding="utf-8")))
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    producer = json.loads(args.producer.read_text(encoding="utf-8"))
    independent = json.loads(args.independent.read_text(encoding="utf-8"))
    progress = [
        json.loads(line) for line in args.progress.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    checks: list[dict[str, object]] = []

    def check(label: str, condition: bool, detail: object) -> None:
        if not condition:
            raise AssertionError(f"{label}: {detail}")
        checks.append({"label": label, "passed": True, "detail": detail})

    check("metadata row count", len(rows) == metadata["rows"], len(rows))
    check(
        "classification repeated across raw inputs",
        all(item["finiteGalerkin"] is True for item in (producer["model"], independent))
        and all(item["pdeTimeStepping"] is True for item in (producer["model"], independent))
        and all(item["dns"] is False for item in (producer["model"], independent)),
        {
            "producer": {key: producer["model"][key] for key in ("finiteGalerkin", "pdeTimeStepping", "dns")},
            "independent": {key: independent[key] for key in ("finiteGalerkin", "pdeTimeStepping", "dns")},
        },
    )
    same = next(run for run in independent["runs"] if run["cutoff"] == 2)
    refined = next(run for run in independent["runs"] if run["cutoff"] == 3)
    primary = next(run for run in producer["tauRuns"] if math.isclose(run["tau"], 0.04))
    check(
        "same-truncation independent equality",
        abs(same["APlus"] - primary["APlus"]) < 1e-10
        and abs(same["precompensationRatio"] - primary["precompensationRatio"]) < 1e-10,
        independent["comparisons"],
    )
    check(
        "refined direct-convolution stability",
        abs(refined["APlus"] - primary["APlus"]) < 2e-4
        and abs(refined["precompensationRatio"] - primary["precompensationRatio"]) < 2e-4,
        independent["comparisons"],
    )

    d_rows = [row for row in rows if row["panel"] == "D"]
    maximum_formula_error = 0.0
    viscosity = 1.0
    tau = 0.04
    for frequency in (1, 2, 4, 8, 16, 32, 64):
        group = {
            row["series"]: float(row["y"])
            for row in d_rows if int(float(row["x"])) == frequency
        }
        expected_atom = math.exp(-2.0 * viscosity * tau) / (4.0 * frequency**4)
        expected_budget = (
            1.0 - math.exp(-4.0 * viscosity * tau)
        ) / (16.0 * viscosity * frequency**6)
        expected_ratio = 2.0 * viscosity * frequency**2 / math.sinh(2.0 * viscosity * tau)
        maximum_formula_error = max(
            maximum_formula_error,
            abs(group["leading internal atom"] / expected_atom - 1.0),
            abs(group["leading bare budget"] / expected_budget - 1.0),
            abs(group["atom-to-budget ratio"] / expected_ratio - 1.0),
        )
    check("double-scaling formulas independently rebuilt", maximum_formula_error < 3e-14, maximum_formula_error)

    events = [record["event"] for record in progress]
    check(
        "progress monitoring complete",
        events[0] == "producer-start"
        and "trajectory-complete" in events
        and "independent-start" in events
        and events[-1] == "independent-complete",
        events,
    )
    check("progress has ETA and residuals", any("etaSeconds" in record and "targetResidual" in record for record in progress), len(progress))
    check("PDF one page", len(PdfReader(str(root / "figure.pdf")).pages) == 1, 1)
    svg = (root / "figure.svg").read_text(encoding="utf-8")
    for token in (
        "Precompensation approaches",
        "target shell crosses zero",
        "scale-zero slope charge",
        "Double scaling separates",
        "not DNS",
    ):
        check(f"SVG contains {token}", token in svg, token)
    with Image.open(root / "figure.png") as image:
        check("PNG sufficiently large", image.width >= 3900 and image.height >= 2700, [image.width, image.height])
        dpi = image.info.get("dpi", (0, 0))
        check("PNG 600 dpi", min(dpi) > 590, dpi)
    for preview in ("qa-original.png", "qa-grayscale.png", "qa-pdf.png"):
        with Image.open(root / preview) as image:
            check(f"{preview} nonempty", image.width > 1000 and image.height > 600, [image.width, image.height])
    boundary = metadata["claimBoundary"]
    check(
        "claim boundary excludes continuum and DNS claims",
        "no continuum Galerkin error bound" in boundary and "DNS claim" in boundary,
        boundary,
    )
    result = {
        "status": "passed",
        "checkCount": len(checks),
        "method": (
            "standalone raw-run comparison, direct reconstruction of panel D, "
            "progress-log inspection, and independent PDF/SVG/PNG checks"
        ),
        "checks": checks,
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
