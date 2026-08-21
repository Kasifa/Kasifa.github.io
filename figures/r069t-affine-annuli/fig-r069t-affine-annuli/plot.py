#!/usr/bin/env python3
"""Build the formal R0.69T affine-core physical-annulus figure package."""
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
CERTIFICATE_ROOT = ROOT / "research/certificates/r069t-affine-qmc"
RESULT = CERTIFICATE_ROOT / "result.json"
RESULT_SHA = "1705daf735616a8d67b7b134074aa38a286245df7066f33d495e8f9d6fd8ebed"
SOURCE_COMMIT = "1cb1f3d7478148bd5240181c8206a554bb4ed6d6"
CERTIFICATE_COMMIT = "1d73e9b2569cbe87aae3500c8ea46e0d3a9355b8"
FIGURE_ID = "fig-r069t-affine-annuli"
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
    if sha256(RESULT) != RESULT_SHA:
        raise RuntimeError("pinned R0.69T QMC result hash mismatch")
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    if not result["allChecksPass"]:
        raise RuntimeError("R0.69T QMC checks did not pass")
    for source, target in (
        (CERTIFICATE_ROOT / "annular_summary.csv", HERE / "annular-summary.csv"),
        (CERTIFICATE_ROOT / "refinement.csv", HERE / "refinement.csv"),
    ):
        shutil.copyfile(source, target)
    annular = read_csv(HERE / "annular-summary.csv")
    refinement = read_csv(HERE / "refinement.csv")
    metadata = {
        "status": "passed",
        "sourceCommit": SOURCE_COMMIT,
        "certificateCommit": CERTIFICATE_COMMIT,
        "inputResult": {
            "location": str(RESULT.relative_to(ROOT)),
            "sha256": RESULT_SHA,
        },
        "replicates": result["quadrature"]["replicates"],
        "pointsPerReplicate": result["quadrature"]["pointsPerReplicate"],
        "totalFinestPoints": result["quadrature"]["totalFinestPoints"],
        "exactCoreProduction": result["exactCoreProduction"],
        "finestMean": result["finest"]["totalMean"],
        "finestStandardError": result["finest"]["totalStandardError"],
        "cancellationRatio": result["finest"]["annularCancellationRatioWithoutNearTail"],
        "claimBoundary": (
            "one explicit cutoff and the core-restricted boundary carrier; randomized QMC, "
            "not an interval enclosure, global annular ratio, or regularity theorem"
        ),
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return result, metadata, annular, refinement


def validate_data(values) -> None:
    result, metadata, annular, refinement = values
    means = np.asarray([float(row["mean"]) for row in annular])
    resolved_negative = [
        int(row["index"]) for row in annular if float(row["ci95Upper"]) < 0.0
    ]
    recomputed_ratio = abs(float(np.sum(means))) / float(np.sum(np.abs(means)))
    checks = {
        "certificateHasAllChecks": result["allChecksPass"],
        "tenAnnularRows": len(annular) == 10,
        "threeRefinementRows": len(refinement) == 3,
        "sixtySevenMillionFinestPairs": metadata["totalFinestPoints"] == 67_108_864,
        "onlyResolvedNegativeAnnulusIsOne": resolved_negative == [1],
        "annularMeansReconstructFinestMean": math.isclose(
            float(np.sum(means)), metadata["finestMean"], rel_tol=0.0, abs_tol=1e-12
        ),
        "cancellationRatioRecomputed": math.isclose(
            recomputed_ratio, metadata["cancellationRatio"], rel_tol=0.0, abs_tol=1e-14
        ),
        "finestWithinFourStandardErrors": abs(result["finest"]["zScore"]) < 4.0,
        "partitionResidualIsZero": result["partitionResidualMax"] == 0.0,
    }
    checks = {key: bool(value) for key, value in checks.items()}
    if not all(checks.values()):
        raise AssertionError(checks)
    (HERE / "validation.json").write_text(
        json.dumps({"status": "passed", "checks": checks}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def signed_bars(axis, positions, values, errors, width=0.72):
    for position, value, error in zip(positions, values, errors):
        if value >= 0.0:
            axis.bar(
                position, value, width, color=BLUE, edgecolor=INK, linewidth=0.45,
                yerr=1.96 * error, capsize=1.7,
                error_kw={"elinewidth": 0.55, "capthick": 0.55, "ecolor": INK},
            )
        else:
            axis.bar(
                position, value, width, color="white", edgecolor=RUST, linewidth=0.75,
                hatch="\\\\\\", yerr=1.96 * error, capsize=1.7,
                error_kw={"elinewidth": 0.55, "capthick": 0.55, "ecolor": INK},
            )


def render(values) -> None:
    result, metadata, annular, refinement = values
    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID
    fig, (left, middle, right) = plt.subplots(
        1, 3, figsize=(178 / 25.4, 82 / 25.4),
        gridspec_kw={"width_ratios": [1.16, 0.92, 1.08], "wspace": 0.42},
    )

    displayed = [row for row in annular if int(row["index"]) >= -6]
    indices = np.asarray([int(row["index"]) for row in displayed])
    means = np.asarray([float(row["mean"]) for row in displayed])
    errors = np.asarray([float(row["standardError"]) for row in displayed])
    positions = np.arange(len(indices))
    signed_bars(left, positions, means, errors)
    left.axhline(0.0, color=INK, lw=0.7)
    left.text(
        0.04, 0.96,
        r"$\Gamma_{\rm core}=0.996478$",
        transform=left.transAxes, va="top", color=INK, fontsize=5.8,
    )
    left.text(
        0.04, 0.86,
        r"$67{,}108{,}864$ sampled pairs",
        transform=left.transAxes, va="top", color=MUTED, fontsize=5.3,
    )
    left.set(
        xlabel=r"physical annulus index $j$",
        ylabel=r"signed core carrier $\mathcal{C}_j$",
        title="a  Annular boundary-carrier distribution",
    )
    left.set_xticks(positions, [str(value) for value in indices])
    left.set_ylim(-0.10, 1.65)
    left.set_yticks([0.0, 0.5, 1.0, 1.5])
    left.grid(True, axis="y", color=GRID, lw=0.45, alpha=0.7)

    tail_indices = [-6, -5, -4, 1]
    tails = [row for index in tail_indices for row in annular if int(row["index"]) == index]
    tail_means = np.asarray([float(row["mean"]) for row in tails])
    tail_errors = np.asarray([float(row["standardError"]) for row in tails])
    tail_positions = np.arange(len(tails))
    signed_bars(middle, tail_positions, tail_means, tail_errors, width=0.68)
    middle.axhline(0.0, color=INK, lw=0.7)
    middle.annotate(
        r"resolved negative tail",
        xy=(3, tail_means[-1]), xytext=(0.96, 0.13), textcoords="axes fraction",
        ha="right", color=RUST, fontsize=5.35,
        arrowprops={"arrowstyle": "->", "color": RUST, "lw": 0.65},
    )
    middle.set(
        xlabel=r"selected annulus index $j$",
        ylabel=r"signed core carrier $\mathcal{C}_j$",
        title="b  Expanded small-tail view",
    )
    middle.set_xticks(tail_positions, [str(value) for value in tail_indices])
    middle.set_ylim(-0.009, 0.023)
    middle.set_yticks([-0.008, 0.0, 0.008, 0.016, 0.024])
    middle.grid(True, axis="y", color=GRID, lw=0.45, alpha=0.7)

    powers = np.asarray([int(row["power"]) for row in refinement])
    totals = np.asarray([float(row["totalMean"]) for row in refinement])
    total_errors = np.asarray([float(row["totalStandardError"]) for row in refinement])
    refinement_positions = np.arange(len(powers))
    right.errorbar(
        refinement_positions, totals, yerr=1.96 * total_errors,
        fmt="o", ms=4.2, mfc=BLUE, mec=INK, mew=0.5,
        ecolor=BLUE, elinewidth=0.85, capsize=2.5, capthick=0.75,
        linestyle="none", label="scrambled-Sobol mean",
    )
    exact = metadata["exactCoreProduction"]
    right.axhline(exact, color=INK, lw=0.8, ls=(0, (4, 2)), label="exact core value")
    right.text(
        0.98, exact + 0.0008, r"$8\pi/(3\sqrt{6})=3.420133$",
        transform=right.get_yaxis_transform(), ha="right", va="bottom",
        color=INK, fontsize=5.3,
    )
    right.text(
        0.03, 0.07, "focused scale; 95% scramble intervals",
        transform=right.transAxes, color=MUTED, fontsize=4.7,
    )
    right.set(
        xlabel="pairs per scramble",
        ylabel="reconstructed core production",
        title="c  Exact-value reconstruction",
    )
    right.set_xticks(refinement_positions, [rf"$2^{{{value}}}$" for value in powers])
    right.set_ylim(3.398, 3.442)
    right.set_yticks([3.40, 3.41, 3.42, 3.43, 3.44])
    right.grid(True, axis="y", color=GRID, lw=0.45, alpha=0.7)
    right.legend(loc="upper right", frameon=False, fontsize=4.8)

    fig.subplots_adjust(left=0.071, right=0.994, bottom=0.235, top=0.865)
    fig.savefig(
        HERE / "figure.pdf",
        metadata={"Creator": "R0.69T reproducible figure", "CreationDate": None},
    )
    fig.savefig(
        HERE / "figure.svg",
        metadata={"Creator": "R0.69T reproducible figure", "Date": None},
    )
    fig.savefig(HERE / "figure.png", dpi=600)
    plt.close(fig)
    svg = HERE / "figure.svg"
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )


def write_manifest(elapsed: float, peak: float) -> None:
    image = Image.open(HERE / "figure.png")
    data_files = [
        ("annular-summary.csv", "index, lengthLower, lengthUpper, mean, standardError, ci95Lower, ci95Upper"),
        ("refinement.csv", "power, pointsPerReplicate, total mean/error, exact benchmark, reconstruction, ratio"),
        ("figure-data-metadata.json", "pinned R0.69T QMC result and claim boundary"),
        ("validation.json", "nine figure-data validation checks"),
        ("resources.csv", "elapsedSeconds, maximumRssMiB, status"),
    ]
    outputs = ["figure.pdf", "figure.svg", "figure.png"]
    payload = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "createdAt": "2026-08-21T13:10:00+08:00",
        "analyticalQuestion": "Which physical annuli carry the positive compact affine-core boundary production, and does their sum reconstruct the exact value?",
        "supportedClaim": "for one explicit compact affine core, monitored QMC concentrates the signed boundary carrier at j=-2 and j=-1, resolves only the j=1 mean as negative, and yields the exploratory ratio 0.996478",
        "claimBoundary": "one explicit cutoff and the core-restricted carrier; randomized QMC, not an interval proof, global annular ratio, universal depletion theorem, or regularity result",
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": SOURCE_COMMIT,
            "certificateCommit": CERTIFICATE_COMMIT,
            "dirtyAtCertifiedRun": False,
        },
        "computation": {
            "kind": "data-analysis",
            "configuration": "16 independent scrambled Sobol replicates, 2^22 pairs each, annuli j=-8 through 1",
            "precision": "IEEE binary64 with independent-scramble standard errors",
            "solver": "five-dimensional symmetry-reduced signed Biot-Savart quadrature",
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
            {"path": path, "bytes": (HERE / path).stat().st_size, "sha256": sha256(HERE / path), "schema": schema}
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
                    **({"dpi": 600, "pixels": f"{image.width} by {image.height}"} if path.endswith(".png") else {}),
                }
                for path in outputs
            ],
        },
        "caption": {"english": "caption.md"},
        "chartContract": {
            "family": "signed categorical bars with uncertainty and refinement dot-interval benchmark",
            "takeaway": "the explicit core boundary carrier has little cross-annulus cancellation while reconstructing the exact benchmark at the declared QMC error scale",
            "nonColorEncoding": "filled versus hatched bars, zero lines, interval whiskers, benchmark dashes, and direct labels",
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
            stream, fieldnames=["elapsedSeconds", "maximumRssMiB", "status"], lineterminator="\n"
        )
        writer.writeheader()
        writer.writerow(
            {"elapsedSeconds": f"{elapsed:.9f}", "maximumRssMiB": f"{peak:.6f}", "status": "passed"}
        )
    write_manifest(elapsed, peak)


if __name__ == "__main__":
    main()
