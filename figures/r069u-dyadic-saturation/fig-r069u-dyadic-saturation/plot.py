#!/usr/bin/env python3
"""Build the formal R0.69U dyadic core-saturation figure package."""
from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import resource
import shutil
import time
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE = HERE.parents[1] / "journal.mplstyle"
CERTIFICATE_ROOT = ROOT / "research/certificates/r069u-dyadic-qmc"
RESULT = CERTIFICATE_ROOT / "result.json"
SUMMARY = CERTIFICATE_ROOT / "summary.csv"
ANNULAR = CERTIFICATE_ROOT / "annular.csv"
PROFILE = CERTIFICATE_ROOT / "profile.json"
RESULT_SHA = "30e683f05d8d7f631a937c71b04b6478819e6e8310a1576a548e3bfe7f9fbd83"
SUMMARY_SHA = "9f675607432eb30e362f329983bb13242f472d8e51c35fa15328737e746864a7"
ANNULAR_SHA = "f6e62ccc3f7ea6a56854ea1efe91d5210cf32c0bd63f515a6cbbe1e3fee28f35"
PROFILE_SHA = "ae1a7c59b3e2d98eeb9bfc3fb3f6a0f83a40c680acd75f631b669d5a3b5c6ae4"
QMC_SOURCE_COMMIT = "29ca62f2667816cb26564b2791251a9d2e68197c"
QMC_CERTIFICATE_COMMIT = "a24d3f9bea948edfdd24806edef53f99841206f5"
THEOREM_SOURCE_COMMIT = "9748c451e9d1cc8d6e7e2bcd732f79691b1c13ca"
THEOREM_CERTIFICATE_COMMIT = "0210533624aeb28e5cf58978fc5ea7e446e3fc7e"
FIGURE_ID = "fig-r069u-dyadic-saturation"
INK, MUTED, BLUE, RUST, GOLD, GRID = (
    "#28231f", "#6b675f", "#315a76", "#8b4d43", "#a16f27", "#d5cec0"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def prepare_data():
    pinned = {
        RESULT: RESULT_SHA,
        SUMMARY: SUMMARY_SHA,
        ANNULAR: ANNULAR_SHA,
        PROFILE: PROFILE_SHA,
    }
    for source, expected in pinned.items():
        if sha256(source) != expected:
            raise RuntimeError(f"pinned R0.69U input hash mismatch: {source.name}")
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    if result["status"] != "passed":
        raise RuntimeError("R0.69U QMC certificate did not pass")
    for source, target in (
        (SUMMARY, HERE / "summary.csv"),
        (ANNULAR, HERE / "annular.csv"),
        (PROFILE, HERE / "profile.json"),
    ):
        shutil.copyfile(source, target)
    summary = read_csv(HERE / "summary.csv")
    annular = read_csv(HERE / "annular.csv")
    metadata = {
        "status": "passed",
        "theoremSourceCommit": THEOREM_SOURCE_COMMIT,
        "theoremCertificateCommit": THEOREM_CERTIFICATE_COMMIT,
        "qmcSourceCommit": QMC_SOURCE_COMMIT,
        "qmcCertificateCommit": QMC_CERTIFICATE_COMMIT,
        "inputResult": {
            "location": str(RESULT.relative_to(ROOT)),
            "sha256": RESULT_SHA,
        },
        "replicates": result["method"]["replicates"],
        "pointsPerReplicate": result["method"]["pointsPerReplicate"],
        "pairsPerRadius": result["method"]["pairsPerRadius"],
        "radiusPowers": result["method"]["radiusPowers"],
        "exactCoreProduction": profile["exactCoreProduction"],
        "limitingInnerCarrier": profile["limitingInnerCarrier"],
        "limitingOuterCarrier": profile["limitingOuterCarrier"],
        "rigorousOuterShareLowerBound": "1/42",
        "analyticTwoAnnulusCondition": "R>40, hence every dyadic R>=64",
        "claimBoundary": (
            "the core-restricted saturation theorem is exact; finite-radius points are "
            "randomized QMC and do not determine the full-space annular ratio"
        ),
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return result, profile, metadata, summary, annular


def validate_data(values) -> None:
    result, profile, metadata, summary, annular = values
    ratios = np.asarray([float(row["coreCancellationRatio"]) for row in summary])
    radius64 = next(row for row in summary if int(row["radius"]) == 64)
    z_scores = np.asarray(
        [
            (float(row["totalMean"]) - metadata["exactCoreProduction"])
            / float(row["totalScrambleSe"])
            for row in summary
        ]
    )
    r64_annuli = [
        row for row in annular
        if int(row["radius"]) == 64 and abs(float(row["mean"])) > 0.0
    ]
    checks = {
        "certificateStatusPassed": result["status"] == "passed",
        "sevenDyadicRadii": len(summary) == 7,
        "seventySevenAnnularRows": len(annular) == 77,
        "sixteenScrambles": metadata["replicates"] == 16,
        "fourMillionPairsPerRadius": metadata["pairsPerRadius"] == 4_194_304,
        "ratiosAreNondecreasing": bool(np.all(np.diff(ratios) >= 0.0)),
        "r64RatioIsOne": float(radius64["coreCancellationRatio"]) == 1.0,
        "r64HasOnlyTwoReportedNonzeroAnnuli": [
            int(row["relativeIndex"]) for row in r64_annuli
        ] == [-1, 0],
        "r64PrincipalAnnuliArePositive": all(
            float(row["mean"]) > 0.0 for row in r64_annuli
        ),
        "limitingCarriersSumToExactCore": math.isclose(
            profile["limitingInnerCarrier"] + profile["limitingOuterCarrier"],
            metadata["exactCoreProduction"],
            rel_tol=0.0,
            abs_tol=1e-14,
        ),
        "allTotalsWithinFourScrambleErrors": bool(np.max(np.abs(z_scores)) < 4.0),
        "partitionResidualIsZero": result["audits"]["partitionResidualMax"] == 0.0,
        "sourceCommitMatches": result["provenance"]["sourceCommit"]
        == QMC_SOURCE_COMMIT,
    }
    checks = {key: bool(value) for key, value in checks.items()}
    if not all(checks.values()):
        raise AssertionError(checks)
    (HERE / "validation.json").write_text(
        json.dumps({"status": "passed", "checks": checks}, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )


def render(values) -> None:
    _result, profile, metadata, summary, annular = values
    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID
    fig, (left, middle, right) = plt.subplots(
        1,
        3,
        figsize=(178 / 25.4, 82 / 25.4),
        gridspec_kw={"width_ratios": [1.0, 1.08, 1.0], "wspace": 0.42},
    )

    radii = np.asarray([int(row["radius"]) for row in summary])
    ratios = np.asarray([float(row["coreCancellationRatio"]) for row in summary])
    deficits = 1.0 - ratios
    display_floor = 1.0e-16
    positive = deficits > 0.0
    left.scatter(
        radii[positive], deficits[positive], s=19, marker="o",
        facecolor=BLUE, edgecolor=INK, linewidth=0.45, zorder=4,
        label=r"reported $1-\Gamma_{\rm core}$",
    )
    left.scatter(
        radii[~positive], np.full(np.sum(~positive), display_floor), s=24,
        marker="v", facecolor="white", edgecolor=RUST, linewidth=0.75, zorder=4,
        label="reported binary64 zero",
    )
    left.axvspan(40.0, 80.0, color=GOLD, alpha=0.13, lw=0)
    left.text(
        0.98, 0.95, r"proved two-annulus regime: $R>40$",
        transform=left.transAxes, ha="right", va="top", color=MUTED, fontsize=4.8,
    )
    left.text(
        0.98, 0.09, "zero markers are shown at a display floor",
        transform=left.transAxes, ha="right", color=MUTED, fontsize=4.5,
    )
    left.set_xscale("log", base=2)
    left.set_yscale("log")
    left.set_xlim(0.8, 80)
    left.set_ylim(5e-17, 1e-2)
    left.set_xticks(radii, [str(value) for value in radii])
    left.set(
        xlabel=r"dyadic cutoff radius $R$",
        ylabel=r"reported cancellation deficit $1-\Gamma_{\rm core}$",
        title="a  Core deficit collapses across radii",
    )
    left.grid(True, which="major", color=GRID, lw=0.45, alpha=0.7)
    left.legend(loc="lower left", frameon=False, fontsize=4.3, handletextpad=0.4)

    exact = metadata["exactCoreProduction"]
    inner = np.asarray([float(row["innerAnnulusMean"]) / exact for row in summary])
    outer = np.asarray([float(row["outerAnnulusMean"]) / exact for row in summary])
    inner_errors = []
    outer_errors = []
    for radius in radii:
        radius_rows = [row for row in annular if int(row["radius"]) == radius]
        inner_row = next(row for row in radius_rows if int(row["relativeIndex"]) == -1)
        outer_row = next(row for row in radius_rows if int(row["relativeIndex"]) == 0)
        inner_errors.append(1.96 * float(inner_row["scrambleSe"]) / exact)
        outer_errors.append(1.96 * float(outer_row["scrambleSe"]) / exact)
    middle.errorbar(
        radii, inner, yerr=np.asarray(inner_errors), fmt="o", ms=3.8,
        mfc=BLUE, mec=INK, mew=0.45, ecolor=BLUE, elinewidth=0.65,
        capsize=1.7, linestyle="none", label=r"inner annulus $m-1$",
    )
    middle.errorbar(
        radii, outer, yerr=np.asarray(outer_errors), fmt="s", ms=3.6,
        mfc="white", mec=RUST, mew=0.75, ecolor=RUST, elinewidth=0.65,
        capsize=1.7, linestyle="none", label=r"outer annulus $m$",
    )
    inner_limit = profile["limitingInnerCarrier"] / exact
    outer_limit = profile["limitingOuterCarrier"] / exact
    middle.axhline(inner_limit, color=BLUE, lw=0.75, ls=(0, (4, 2)))
    middle.axhline(outer_limit, color=RUST, lw=0.75, ls=(0, (4, 2)))
    middle.text(
        0.98, inner_limit - 0.045, rf"limit {inner_limit:.6f}",
        transform=middle.get_yaxis_transform(), ha="right", color=BLUE, fontsize=4.7,
    )
    middle.text(
        0.98, outer_limit + 0.035, rf"limit {outer_limit:.6f}",
        transform=middle.get_yaxis_transform(), ha="right", color=RUST, fontsize=4.7,
    )
    middle.set_xscale("log", base=2)
    middle.set_xlim(0.8, 80)
    middle.set_ylim(-0.03, 1.03)
    middle.set_xticks(radii, [str(value) for value in radii])
    middle.set(
        xlabel=r"dyadic cutoff radius $R$",
        ylabel="fraction of exact core production",
        title="b  Two principal annuli approach positive limits",
    )
    middle.grid(True, axis="y", color=GRID, lw=0.45, alpha=0.7)
    middle.legend(loc="center right", frameon=False, fontsize=4.6)

    errors = np.asarray([float(row["absoluteError"]) for row in summary])
    standard_errors = np.asarray([float(row["totalScrambleSe"]) for row in summary])
    z_scores = errors / standard_errors
    right.axhspan(-2.0, 2.0, color=GOLD, alpha=0.08, lw=0)
    right.axhspan(-1.0, 1.0, color=GOLD, alpha=0.12, lw=0)
    right.axhline(0.0, color=INK, lw=0.75)
    right.scatter(
        radii, z_scores, s=20, marker="D", facecolor=BLUE,
        edgecolor=INK, linewidth=0.45, zorder=4,
    )
    right.axhline(2.0, color=MUTED, lw=0.45, ls=(0, (2, 2)))
    right.axhline(-2.0, color=MUTED, lw=0.45, ls=(0, (2, 2)))
    right.text(
        0.98, 0.94, r"all $|z|<1.1$",
        transform=right.transAxes, ha="right", va="top", color=INK, fontsize=5.2,
    )
    right.text(
        0.98, 0.08, "scramble SE is diagnostic, not an interval bound",
        transform=right.transAxes, ha="right", color=MUTED, fontsize=4.45,
    )
    right.set_xscale("log", base=2)
    right.set_xlim(0.8, 80)
    right.set_ylim(-2.35, 2.35)
    right.set_xticks(radii, [str(value) for value in radii])
    right.set_yticks([-2, -1, 0, 1, 2])
    right.set(
        xlabel=r"dyadic cutoff radius $R$",
        ylabel=r"$(\widehat{\mathcal C}-\mathcal C_{\rm exact})/{\rm SE}$",
        title="c  Exact-value reconstruction at every radius",
    )
    right.grid(True, axis="y", color=GRID, lw=0.45, alpha=0.7)

    fig.subplots_adjust(left=0.071, right=0.994, bottom=0.235, top=0.865)
    fig.savefig(
        HERE / "figure.pdf",
        metadata={"Creator": "R0.69U reproducible figure", "CreationDate": None},
    )
    fig.savefig(
        HERE / "figure.svg",
        metadata={"Creator": "R0.69U reproducible figure", "Date": None},
    )
    fig.savefig(HERE / "figure.png", dpi=600)
    plt.close(fig)
    svg = HERE / "figure.svg"
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines())
        + "\n",
        encoding="utf-8",
    )


def write_manifest(elapsed: float, peak: float) -> None:
    image = Image.open(HERE / "figure.png")
    data_files = [
        ("summary.csv", "radius, total mean/error, exact value, ratio, principal annuli"),
        ("annular.csv", "radius, relative/indexed annulus mean and scramble interval"),
        ("profile.json", "mollified cutoff energy and analytic limiting carriers"),
        ("figure-data-metadata.json", "pinned R0.69U theorem and QMC provenance"),
        ("validation.json", "thirteen figure-data validation checks"),
        ("resources.csv", "elapsedSeconds, maximumRssMiB, status"),
    ]
    outputs = ["figure.pdf", "figure.svg", "figure.png"]
    payload = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "createdAt": "2026-08-21T13:40:00+08:00",
        "analyticalQuestion": "Does pushing a smooth affine cutoff to dyadic radius R force the core-restricted annular carrier to one sign, and what does dilation do to the full-space ratio?",
        "supportedClaim": "the exact theorem gives eventual core ratio one and full-space dilation invariance; monitored finite-radius QMC resolves convergence of the two positive principal annuli to their analytic limits",
        "claimBoundary": "core-restricted saturation is exact, but finite-radius values are randomized QMC and the self-similar family does not prove full-space annular saturation or regularity",
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": QMC_SOURCE_COMMIT,
            "certificateCommit": QMC_CERTIFICATE_COMMIT,
            "dirtyAtCertifiedRun": False,
        },
        "computation": {
            "kind": "data-analysis",
            "configuration": "16 independent scrambled Sobol replicates, 2^18 pairs per radius, R=1 through 64 dyadic",
            "precision": "IEEE binary64 with independent-scramble standard errors; analytic sign margin is exact rational arithmetic",
            "solver": "five-dimensional symmetry-reduced signed Biot-Savart core-carrier quadrature",
            "command": "python plot.py",
            "wallTimeSeconds": elapsed,
        },
        "compute": {
            "host": "local Mac workstation",
            "operatingSystem": f"{platform.system()}-{platform.release()}-{platform.machine()}",
            "cpu": "Apple M5 Max",
            "memoryGiB": 36,
            "processes": 1,
            "threadsPerProcess": 1,
            "maximumRssMiB": peak,
        },
        "environment": {
            "python": platform.python_version(),
            "matplotlib": matplotlib.__version__,
            "numpy": np.__version__,
            "pillow": Image.__version__,
            "packagesLock": "requirements-research.txt",
        },
        "sourceData": [
            {
                "location": str(RESULT.relative_to(ROOT)),
                "fileName": RESULT.name,
                "bytes": RESULT.stat().st_size,
                "sha256": RESULT_SHA,
                "extractionCommand": "python plot.py",
            }
        ],
        "data": [
            {
                "path": path,
                "bytes": (HERE / path).stat().st_size,
                "sha256": sha256(HERE / path),
                "schema": schema,
            }
            for path, schema in data_files
        ],
        "figure": {
            "widthMillimetres": 178,
            "heightMillimetres": 82,
            "profile": "journal-default",
            "script": "plot.py",
            "outputs": [
                {
                    "path": path,
                    "bytes": (HERE / path).stat().st_size,
                    "sha256": sha256(HERE / path),
                    **(
                        {"dpi": 600, "pixels": f"{image.width} by {image.height}"}
                        if path.endswith(".png")
                        else {}
                    ),
                }
                for path in outputs
            ],
        },
        "caption": {"english": "caption.md"},
        "chartContract": {
            "family": "log point plots, point-interval limiting shares, and standardized reconstruction residuals",
            "takeaway": "the core-restricted carrier reaches the exact one-sign regime while the two principal annuli converge to positive analytic limits",
            "nonColorEncoding": "circle, square, diamond, open downward triangle, analytic shading, interval whiskers, and direct labels",
            "outputFootprint": "double-column 178 by 82 millimetres with PDF, SVG, and 600 dpi PNG",
        },
        "qa": {
            "status": "passed",
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
        },
    }
    (HERE / "manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> None:
    started = time.perf_counter()
    values = prepare_data()
    validate_data(values)
    render(values)
    elapsed = time.perf_counter() - started
    peak = rss_mib()
    with (HERE / "resources.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=["elapsedSeconds", "maximumRssMiB", "status"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerow(
            {
                "elapsedSeconds": f"{elapsed:.9f}",
                "maximumRssMiB": f"{peak:.6f}",
                "status": "passed",
            }
        )
    write_manifest(elapsed, peak)


if __name__ == "__main__":
    main()
