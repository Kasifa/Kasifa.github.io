#!/usr/bin/env python3
"""Standalone validation of R0.71U raw data, formulas, and final artifacts.

This validator uses the bundled Python runtime and does not import either
solver or Matplotlib. It checks the independently generated sparse-lattice
result, recomputes formula identities, and inspects PDF/SVG/PNG outputs.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
import json
import math
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent


def timestamp() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="milliseconds")


def cpair(values: list[float]) -> complex:
    return complex(float(values[0]), float(values[1]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--independent", type=Path, required=True)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--progress", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    primary = json.loads(args.primary.read_text(encoding="utf-8"))
    independent = json.loads(args.independent.read_text(encoding="utf-8"))
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(args.data.open(encoding="utf-8")))
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, observed: object, criterion: str) -> None:
        checks.append({
            "name": name,
            "passed": bool(passed),
            "observed": observed,
            "criterion": criterion,
        })

    # Independent algebraic reconstruction of the p=0 response matrix.
    nu = float(config["viscosity"])
    K = int(config["K"])
    L = int(config["L"])
    d = int(config["modulus"])
    times = np.asarray(config["targetTimes"], dtype=float)
    n = d * np.asarray(config["modeMultipliers"], dtype=float)
    A = np.asarray([1j if value == "1j" else complex(value) for value in config["initialAmplitudes"]])
    beta = 2.0 * nu * n * (n - K)
    mu = nu * (K * K + L * L)
    phi = np.exp(-mu * times[:, None]) * (1.0 - np.exp(-beta[None, :] * times[:, None])) / beta[None, :]
    response = -1j * L * A[None, :] * phi
    free_matrix = np.vstack((response[:, 1:].real, response[:, 1:].imag))
    check(
        "independent analytic response rank",
        int(np.linalg.matrix_rank(free_matrix)) == 6,
        {
            "rank": int(np.linalg.matrix_rank(free_matrix)),
            "conditionNumber": float(np.linalg.cond(free_matrix)),
            "beta": beta.tolist(),
        },
        "six free real columns have full rank",
    )
    check(
        "real and imaginary response blocks",
        float(np.max(np.abs(response[:, :4].imag))) == 0.0
        and float(np.max(np.abs(response[:, 4:].real))) == 0.0,
        {
            "firstBlockImaginaryMaximum": float(np.max(np.abs(response[:, :4].imag))),
            "secondBlockRealMaximum": float(np.max(np.abs(response[:, 4:].real))),
        },
        "A_1,...,A_4=i give real columns; A_5,...,A_7=1 give imaginary columns",
    )

    pde = independent["pdeReductionGridCheck"]
    pde_residual = max(float(value) for key, value in pde.items() if "Residual" in key)
    check(
        "PDE reduction formula",
        pde_residual <= 1e-14
        and primary["pdeReduction"]["reducedEquations"]
        == ["v_t=nu v_yy", "f_t+v f_z=nu(f_yy+f_zz)"],
        {"gridCheck": pde, "formula": primary["pdeReduction"]},
        "div u=0 and (u dot grad)u=(v f_z,0,0), giving the two reduced equations",
    )
    check(
        "finite-lattice ODE includes both shifts",
        "a_(m-l)+a_(m+l)" in primary["latticeFormula"]
        and "-nu[(K+dm)^2+L^2]" in primary["latticeFormula"],
        primary["latticeFormula"],
        "heat diagonal and both modular neighbors are present",
    )

    independent_residual = float(independent["shooting"]["targetResidualMaximum"])
    check(
        "independent prescribed roots",
        bool(independent["shooting"]["success"]) and independent_residual <= 1e-12,
        independent["shooting"],
        "fresh sparse mcut=36 shoot succeeds and max |a_0(t_m)| <= 1e-12",
    )
    independent_slopes = np.asarray([cpair(item["slope"]) for item in independent["events"]])
    check(
        "independent nonzero slopes",
        independent_slopes.size == 3 and float(np.min(np.abs(independent_slopes))) >= 1e-7,
        {
            "minimumMagnitude": float(np.min(np.abs(independent_slopes))),
            "slopes": [[float(value.real), float(value.imag)] for value in independent_slopes],
        },
        "three slopes with minimum magnitude at least 1e-7",
    )
    check(
        "independent parameter replication",
        float(independent["maximumParameterAbsoluteDifference"]) <= 1e-9,
        {
            "maximumAbsolute": independent["maximumParameterAbsoluteDifference"],
            "maximumRelative": independent["maximumParameterRelativeDifference"],
        },
        "mcut=36 versus primary max parameter difference <= 1e-9",
    )
    check(
        "independent slope replication",
        float(independent["maximumSlopeRelativeDifferenceFromPrimary"]) <= 1e-5,
        independent["maximumSlopeRelativeDifferenceFromPrimary"],
        "maximum relative slope difference <= 1e-5",
    )
    check(
        "fixed primary parameters at independent cutoff",
        float(independent["primaryParametersAtIndependentCutoff"]["maximumTargetResidual"]) <= 1e-10,
        independent["primaryParametersAtIndependentCutoff"],
        "primary parameters evaluated at mcut=36 have max root residual <= 1e-10",
    )

    primary_events = primary["main"]["events"]
    atom_relative_errors: list[float] = []
    trace_relative_errors: list[float] = []
    ratio_errors: list[float] = []
    for item in independent["events"]:
        slope = cpair(item["slope"])
        Y = float(item["enstrophy"])
        atom_expected = 2.0 * abs(slope) ** 2 / Y
        trace_expected = 8.0 * abs(slope) ** 2 / Y
        atom_relative_errors.append(abs(float(item["jetAtom"]) - atom_expected) / atom_expected)
        trace_relative_errors.append(abs(float(item["firstJetTrace"]) - trace_expected) / trace_expected)
        ratio_errors.append(abs(float(item["atomToFirstJetTraceRatio"]) - 0.25))
    check(
        "independent atom formula",
        max(atom_relative_errors) <= 1e-10,
        max(atom_relative_errors),
        "J=2|a_0'|^2/Y at kappa=m_*=1",
    )
    check(
        "independent first-jet trace formula",
        max(trace_relative_errors) <= 1e-10,
        max(trace_relative_errors),
        "P=kappa^-6||C_t||^2/Y=8|a_0'|^2/Y",
    )
    check(
        "one-shell atom identity",
        max(ratio_errors) <= 1e-10,
        max(ratio_errors),
        "J=P/4 because rho^2=2 kappa^2",
    )
    check(
        "positive finite atoms",
        min(float(item["jetAtom"]) for item in independent["events"]) > 0.0,
        [float(item["jetAtom"]) for item in independent["events"]],
        "all three independent atoms are positive",
    )

    # Directional first-order passage at delta=1e-4.
    trace_times = np.asarray([float(item["time"]) for item in primary["main"]["trace"]])
    trace_values = np.asarray([
        complex(float(item["real"]), float(item["imag"]))
        for item in primary["main"]["trace"]
    ])
    directional: list[dict[str, float]] = []
    delta = 1e-4
    for event in primary_events:
        time = float(event["time"])
        slope = cpair(event["slope"])
        direction = slope / abs(slope)
        left = trace_values[np.argmin(np.abs(trace_times - (time - delta)))]
        right = trace_values[np.argmin(np.abs(trace_times - (time + delta)))]
        left_projection = float(np.real(np.conjugate(direction) * left))
        right_projection = float(np.real(np.conjugate(direction) * right))
        left_error = float(abs(left + delta * slope) / (delta * abs(slope)))
        right_error = float(abs(right - delta * slope) / (delta * abs(slope)))
        directional.append({
            "time": time,
            "leftProjection": left_projection,
            "rightProjection": right_projection,
            "leftLinearizationError": left_error,
            "rightLinearizationError": right_error,
        })
    check(
        "three first-order complex passages",
        all(
            item["leftProjection"] < 0.0 < item["rightProjection"]
            and max(item["leftLinearizationError"], item["rightLinearizationError"]) < 0.01
            for item in directional
        ),
        directional,
        "directional signs straddle zero and normalized linearization error is below 1e-2",
    )

    exponents = [float(item["logLogExponent"]) for item in primary["scalingFits"]]
    check(
        "multi-shot quadratic boundary",
        len(primary["parameterSweep"]) == 5 and all(abs(value - 2.0) < 0.02 for value in exponents),
        {"shootCount": len(primary["parameterSweep"]), "exponents": exponents},
        "five separately shot p1 cases and each descriptive exponent within 0.02 of two",
    )
    check(
        "no C_tt ledger overclaim",
        "secondJetSample" not in args.primary.read_text(encoding="utf-8")
        and "secondJetSample" not in args.independent.read_text(encoding="utf-8")
        and "C_{tt}" in (ROOT / "caption.md").read_text(encoding="utf-8")
        and "This is not" in (ROOT / "caption.md").read_text(encoding="utf-8"),
        "firstJetTrace keys used; caption explicitly excludes a C_tt payment ledger",
        "P is labeled as a first-jet trace, while Panel C uses the O(p1^2) alternative",
    )

    radius = float(config["annulusSupportRadius"])
    check(
        "annulus modular inequality",
        d > radius + abs(K),
        {"d": d, "RstarPlusAbsK": radius + abs(K)},
        "d > R_* + |K|",
    )
    support: set[tuple[int, int]] = set()
    for r in range(-40, 41):
        support.add((K + d * r, L))
        support.add((-K + d * r, -L))
        support.add((d * r, 0))
    inside = sorted(
        (q, z) for q, z in support
        if q * q + z * z > 0 and q * q + z * z <= radius * radius
    )
    other_squared = sorted(
        q * q + z * z for q, z in support
        if (q, z) not in {(-1, -1), (1, 1)} and q * q + z * z > 0
    )
    check(
        "annulus modular isolation",
        inside == [(-1, -1), (1, 1)] and other_squared[0] == 50,
        {"inside": inside, "nearestNonTargetSquaredRadius": other_squared[0]},
        "only the conjugate target pair lies inside R_*=3; nearest non-target squared radius is 50",
    )

    cutoff = {int(item["cutoff"]): item for item in primary["cutoffSweep"]}
    check(
        "cutoff target convergence",
        float(cutoff[24]["maximumTargetDifferenceToM36"]) <= 1e-10,
        cutoff[24]["maximumTargetDifferenceToM36"],
        "fixed-parameter mcut=24 versus 36 target difference <= 1e-10",
    )
    check(
        "cutoff slope convergence",
        float(cutoff[24]["maximumRelativeSlopeDifferenceToM36"]) <= 1e-5,
        cutoff[24]["maximumRelativeSlopeDifferenceToM36"],
        "mcut=24 versus 36 relative slope difference <= 1e-5",
    )
    check(
        "cutoff boundary tail",
        float(cutoff[24]["maximumBoundaryCoefficient"]) <= 1e-14,
        cutoff[24]["maximumBoundaryCoefficient"],
        "mcut=24 boundary coefficient <= 1e-14",
    )

    check(
        "plot data integrity",
        len(rows) == int(metadata["rowCount"])
        and {item["panel"] for item in rows} == {"A", "B", "C", "D"},
        {"rows": len(rows), "metadataRows": metadata["rowCount"], "panels": sorted({item["panel"] for item in rows})},
        "CSV row count matches metadata and panels A-D are populated",
    )
    classification = config["classification"]
    check(
        "claim classification",
        classification["finiteGalerkin"] is True
        and classification["pdeTimeStepping"] is True
        and classification["dns"] is False
        and classification["analyticProofFromNumerics"] is False,
        classification,
        "finiteGalerkin=true, pdeTimeStepping=true, dns=false, analyticProofFromNumerics=false",
    )

    pdf = PdfReader(ROOT / "figure.pdf")
    box = pdf.pages[0].mediabox
    width_mm = float(box.width) * 25.4 / 72.0
    height_mm = float(box.height) * 25.4 / 72.0
    resources = pdf.pages[0].get("/Resources", {})
    has_fonts = bool(resources.get("/Font")) if hasattr(resources, "get") else False
    check(
        "PDF page and physical size",
        len(pdf.pages) == 1 and abs(width_mm - 178.05) < 0.25 and abs(height_mm - 134.11) < 0.25,
        {"pages": len(pdf.pages), "widthMm": width_mm, "heightMm": height_mm},
        "one page at 178.05 by 134.11 mm within 0.25 mm",
    )
    check(
        "PDF vector font resources",
        has_fonts,
        {"hasFontResources": has_fonts, "metadata": dict(pdf.metadata or {})},
        "PDF page declares font resources",
    )
    with Image.open(ROOT / "figure.png") as image:
        png_size = image.size
        png_dpi = image.info.get("dpi", (0.0, 0.0))
    check(
        "600 dpi PNG",
        4190 <= png_size[0] <= 4220
        and 3160 <= png_size[1] <= 3180
        and min(png_dpi) >= 599.0,
        {"pixels": png_size, "dpi": png_dpi},
        "archival dimensions at reported 600 dpi",
    )
    svg = (ROOT / "figure.svg").read_text(encoding="utf-8")
    check(
        "SVG remains vector",
        "<svg" in svg and "viewBox=" in svg and "<image" not in svg,
        {"bytes": len(svg.encode("utf-8")), "containsRasterImage": "<image" in svg},
        "SVG has a viewBox and no embedded raster image",
    )
    qa_files = ["qa-original.png", "qa-grayscale.png", "qa-pdf.png", "qa-report.md"]
    qa_report = (ROOT / "qa-report.md").read_text(encoding="utf-8") if (ROOT / "qa-report.md").is_file() else ""
    check(
        "visual QA assets and declarations",
        all((ROOT / name).is_file() for name in qa_files)
        and "PENDING" not in qa_report
        and qa_report.count("PASS") >= 10,
        {"files": qa_files, "passCount": qa_report.count("PASS"), "pending": "PENDING" in qa_report},
        "all QA previews exist and manual checks are PASS",
    )
    progress_records = [
        json.loads(line) for line in args.progress.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    stages = [item.get("stage") for item in progress_records]
    check(
        "progress monitoring",
        len(progress_records) >= 17
        and "complete-primary" in stages
        and "complete-independent" in stages,
        {"recordCount": len(progress_records), "stages": stages},
        "timestamped primary and independent completion records are present",
    )
    resource_records = [
        json.loads(line) for line in (ROOT / "resource-log.ndjson").read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    check(
        "resource monitoring",
        len(resource_records) >= 8
        and all("processUserCpuSeconds" in item for item in resource_records),
        {"recordCount": len(resource_records), "stages": [item.get("stage") for item in resource_records]},
        "resource log contains primary stages and independent completion",
    )

    failed = [item for item in checks if not item["passed"]]
    payload = {
        "release": config["release"],
        "method": "standalone bundled-runtime reconstruction of analytic response, modular gap, raw residual/slope/atom/cutoff checks, and PDF/SVG/PNG/QA inspection",
        "passed": not failed,
        "checkCount": len(checks),
        "failedCount": len(failed),
        "checks": checks,
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with args.progress.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({
            "timestamp": timestamp(),
            "stage": "complete-independent-validation",
            "passed": not failed,
            "checkCount": len(checks),
            "failedCount": len(failed),
        }, sort_keys=True) + "\n")
    if failed:
        raise SystemExit("failed checks: " + ", ".join(item["name"] for item in failed))


if __name__ == "__main__":
    main()
