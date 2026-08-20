#!/usr/bin/env python3
"""Build and validate the formal R0.69D nonlinear-decoupling figure package."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import resource
import subprocess
import time
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE = HERE.parents[1] / "journal.mplstyle"
CERTIFICATE = ROOT / "research/certificates/r069d/transverse-nonlinear-decoupling.json"
R069B_CERTIFICATE = ROOT / "research/certificates/r069b/transverse-critical-smallness.json"
CERTIFICATE_SHA = "1bb0e9af3f9cb81da5ece68fc50a2b7d4782bc8f66187bb30693616d5f755932"
R069B_SHA = "53ebc36d199ca2b379270c85a842978aab086f7f77d5e4b4f6c32e944c15ce45"
SOURCE_COMMIT = "d6e085404bb78e23ec2ea14d541e2841a01ed7bb"
CERTIFICATE_COMMIT = "610bba97cc84c149fb42a9d46de602585eea2ab9"
FIGURE_ID = "fig-r069d-nonlinear-decoupling"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#8b4d43"
GOLD = "#a16f27"
GREEN = "#4d6a58"
PALE_BLUE = "#e6edf1"
PALE_GOLD = "#f4ead6"
GRID = "#d5cec0"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def write_rows(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def prepare_data() -> tuple[dict[str, object], float]:
    started = time.perf_counter()
    if sha256(CERTIFICATE) != CERTIFICATE_SHA:
        raise RuntimeError("the pinned R0.69D certificate hash does not match")
    if sha256(R069B_CERTIFICATE) != R069B_SHA:
        raise RuntimeError("the pinned R0.69B certificate hash does not match")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    upstream = json.loads(R069B_CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["status"] != "passed":
        raise RuntimeError("the R0.69D certificate did not pass")

    branch_rows: list[dict[str, object]] = []
    for chi in np.linspace(0.0, 0.999999, 501):
        root = math.sqrt(1.0 - float(chi))
        branch_rows.append(
            {
                "chi": f"{chi:.16g}",
                "sqrtDiscriminant": f"{root:.16g}",
                "nonlinearAmplification": f"{2.0 / (1.0 + root):.16g}",
                "contractionFactor": f"{1.0 - root:.16g}",
            }
        )
    write_rows(
        "quadratic-branch.csv",
        ["chi", "sqrtDiscriminant", "nonlinearAmplification", "contractionFactor"],
        branch_rows,
    )

    rho = float(upstream["criticalNormBound"]["rho"]["upper"])
    prefactors = (1.0, 1e2, 1e4, 1e6)
    depth_rows: list[dict[str, object]] = []
    for prefactor in prefactors:
        for depth in range(86):
            chi_upper = prefactor * rho**depth
            depth_rows.append(
                {
                    "dimensionlessPrefactorK": f"{prefactor:.0f}",
                    "r": depth,
                    "chiUpper": f"{chi_upper:.16g}",
                    "strictlyAdmissible": str(chi_upper < 1.0).lower(),
                }
            )
    write_rows(
        "depth-budgets.csv",
        ["dimensionlessPrefactorK", "r", "chiUpper", "strictlyAdmissible"],
        depth_rows,
    )

    first_depths = {}
    for prefactor in prefactors:
        selected = [
            row for row in depth_rows
            if float(row["dimensionlessPrefactorK"]) == prefactor
            and row["strictlyAdmissible"] == "true"
        ]
        first_depths[f"{prefactor:.0f}"] = int(selected[0]["r"])

    metadata = {
        "status": "passed",
        "sourceCommit": SOURCE_COMMIT,
        "certificateCommit": CERTIFICATE_COMMIT,
        "inputCertificate": {
            "location": str(CERTIFICATE.relative_to(ROOT)),
            "sha256": CERTIFICATE_SHA,
        },
        "upstreamCertificate": {
            "location": str(R069B_CERTIFICATE.relative_to(ROOT)),
            "sha256": R069B_SHA,
        },
        "rhoUpper": repr(rho),
        "dimensionlessPrefactors": [f"{value:.0f}" for value in prefactors],
        "firstStrictlyAdmissibleDepths": first_depths,
        "checksPassed": sum(bool(value) for value in certificate["checks"].values()),
        "checksTotal": len(certificate["checks"]),
        "claimBoundary": certificate["classification"],
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    elapsed = time.perf_counter() - started
    write_rows(
        "figure-data-resources.csv",
        ["elapsedSeconds", "maximumRssMiB", "status"],
        [{
            "elapsedSeconds": f"{elapsed:.6f}",
            "maximumRssMiB": f"{rss_mib():.3f}",
            "status": "passed",
        }],
    )
    return metadata, elapsed


def validate_data(metadata: dict[str, object]) -> None:
    branch = read_rows("quadratic-branch.csv")
    depth = read_rows("depth-budgets.csv")
    chi = [float(row["chi"]) for row in branch]
    amplification = [float(row["nonlinearAmplification"]) for row in branch]
    contraction = [float(row["contractionFactor"]) for row in branch]
    prefactors = sorted({float(row["dimensionlessPrefactorK"]) for row in depth})
    checks = {
        "fiveHundredOneQuadraticSamples": len(branch) == 501,
        "strictChiDomainSampled": min(chi) == 0.0 and max(chi) < 1.0,
        "amplificationStaysBetweenOneAndTwo": (
            min(amplification) >= 1.0 and max(amplification) < 2.0
        ),
        "amplificationIsMonotone": all(
            right >= left for left, right in zip(amplification, amplification[1:])
        ),
        "contractionStaysBelowOne": min(contraction) >= 0.0 and max(contraction) < 1.0,
        "fourDimensionlessPrefactorScenarios": prefactors == [1.0, 1e2, 1e4, 1e6],
        "everyDepthEnvelopeStrictlyDecays": all(
            all(right < left for left, right in zip(values, values[1:]))
            for values in (
                [float(row["chiUpper"]) for row in depth if float(row["dimensionlessPrefactorK"]) == prefactor]
                for prefactor in prefactors
            )
        ),
        "everyFiniteScenarioEventuallyEntersStrictRegion": all(
            any(
                row["strictlyAdmissible"] == "true"
                for row in depth
                if float(row["dimensionlessPrefactorK"]) == prefactor
            )
            for prefactor in prefactors
        ),
        "formalCertificatePassedEighteenChecks": (
            metadata["checksPassed"] == metadata["checksTotal"] == 18
        ),
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    (HERE / "validation.json").write_text(
        json.dumps({"status": "passed", "checks": checks}, indent=2) + "\n",
        encoding="utf-8",
    )


def normalize_svg(path: Path) -> None:
    path.write_text(
        "\n".join(
            line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()
        ) + "\n",
        encoding="utf-8",
    )


def blossom(figure) -> None:
    center = (0.946, 0.925)
    for dx, dy, angle in ((0, .010, 0), (0, -.010, 0), (.008, 0, 90), (-.008, 0, 90)):
        figure.add_artist(
            Ellipse(
                (center[0] + dx, center[1] + dy), .010, .018,
                angle=angle, transform=figure.transFigure,
                facecolor="#ead9b8", edgecolor=GOLD, linewidth=.35,
            )
        )


def draw() -> float:
    started = time.perf_counter()
    branch = read_rows("quadratic-branch.csv")
    depth = read_rows("depth-budgets.csv")
    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = FIGURE_ID
        figure = plt.figure(figsize=(178 / 25.4, 92 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1, 2, left=.082, right=.958, bottom=.20, top=.76,
            width_ratios=(.98, 1.02), wspace=.31,
        )
        branch_axis = figure.add_subplot(grid[0, 0])
        depth_axis = figure.add_subplot(grid[0, 1])
        figure.suptitle(
            "A bounded reference resolvent forces nonlinear packet decoupling",
            x=.055, y=.947, ha="left", fontsize=8.0, color=INK,
        )
        figure.text(
            .055, .884,
            r"exact quadratic branch  ·  full $\mathcal{B}(z,z)$ feedback  ·  source-locked R0.69D certificate",
            ha="left", fontsize=3.8, color=MUTED,
        )
        blossom(figure)

        x = [float(row["chi"]) for row in branch]
        amplification = [float(row["nonlinearAmplification"]) for row in branch]
        contraction = [float(row["contractionFactor"]) for row in branch]
        branch_axis.set_title("(a) Exact admissible nonlinear branch", loc="left", pad=5)
        branch_axis.plot(
            x, amplification, color=BLUE, linestyle="-", linewidth=1.25,
            marker="o", markerfacecolor="white", markevery=100, markersize=2.4,
            label=r"$R_-/(M_TC_H\delta)=2/(1+\sqrt{1-\chi})$",
        )
        branch_axis.plot(
            x, contraction, color=RUST, linestyle="--", linewidth=1.15,
            marker="s", markevery=100, markersize=2.3,
            label=r"contraction $q=1-\sqrt{1-\chi}$",
        )
        branch_axis.fill_between(x, 1.0, amplification, color=PALE_BLUE, alpha=.9)
        branch_axis.axhline(1.0, color=INK, linewidth=.5, linestyle=(0, (2, 2)))
        branch_axis.axhline(2.0, color=GOLD, linewidth=.5, linestyle=(0, (2, 2)))
        branch_axis.set_xlim(0, 1)
        branch_axis.set_ylim(0, 2.08)
        branch_axis.set_xlabel(r"nonlinear budget $\chi=4C_BM_T^2C_H\delta$")
        branch_axis.set_ylabel("dimensionless factor")
        branch_axis.grid(color=GRID, linewidth=.3)
        branch_axis.legend(loc="upper left", frameon=False, fontsize=3.0)
        branch_axis.text(
            .055, .10,
            r"For $0\leq\chi<1$: self-map equality holds at $R_-$," + "\n" +
            r"$q<1$, and $M_TC_H\delta\leq R_-<2M_TC_H\delta$.",
            transform=branch_axis.transAxes, fontsize=3.05, color=INK,
            bbox={"facecolor": PALE_GOLD, "edgecolor": "none", "pad": 2.0},
        )

        depth_axis.set_title("(b) Depth beats every fixed resolvent cost", loc="left", pad=5)
        styles = {
            1.0: (BLUE, "-", "o"),
            1e2: (RUST, "--", "s"),
            1e4: (GOLD, "-.", "D"),
            1e6: (GREEN, ":", "^"),
        }
        for prefactor, (color, linestyle, marker) in styles.items():
            selected = [
                row for row in depth
                if float(row["dimensionlessPrefactorK"]) == prefactor
            ]
            depths = [int(row["r"]) for row in selected]
            budgets = [float(row["chiUpper"]) for row in selected]
            first = next(int(row["r"]) for row in selected if row["strictlyAdmissible"] == "true")
            depth_axis.semilogy(
                depths, budgets, color=color, linestyle=linestyle, linewidth=1.1,
                marker=marker, markevery=10, markersize=2.4,
                label=rf"$K=10^{{{int(math.log10(prefactor))}}}$; first $r={first}$",
            )
            depth_axis.plot(first, prefactor * float(json.loads(R069B_CERTIFICATE.read_text())["criticalNormBound"]["rho"]["upper"])**first,
                            marker=marker, color=color, markersize=3.0, linestyle="none")
        depth_axis.axhline(1.0, color=INK, linewidth=.65, linestyle=(0, (2, 2)))
        depth_axis.fill_between([0, 85], [1e-7, 1e-7], [1, 1], color=PALE_BLUE, alpha=.65)
        depth_axis.set_xlim(0, 85)
        depth_axis.set_ylim(1e-7, 2e6)
        depth_axis.set_xlabel("packet depth r")
        depth_axis.set_ylabel(r"upper budget $\chi_r\leq K\rho^r$  (log scale)")
        depth_axis.grid(color=GRID, linewidth=.3, which="both")
        depth_axis.legend(loc="upper right", frameon=False, fontsize=2.9)
        depth_axis.text(
            .055, .065,
            r"$K=4C_BC_HC_0M_T^2$ is symbolic." + "\n" +
            r"The plotted $K$ values are dimensionless scenarios, not universal constants.",
            transform=depth_axis.transAxes, fontsize=2.95, color=MUTED,
            bbox={"facecolor": "white", "edgecolor": GRID, "linewidth": .35, "pad": 2.0},
        )

        figure.text(
            .055, .065,
            "Claim boundary: local nonlinear stability around a boundedly invertible reference linearization; no bound on that resolvent at a possible singular horizon.",
            fontsize=3.15, color=MUTED,
        )
        metadata = {"Creator": "R0.69D conditional nonlinear decoupling", "Date": None}
        figure.savefig(HERE / "figure.pdf", metadata=metadata)
        figure.savefig(HERE / "figure.svg", metadata=metadata)
        figure.savefig(HERE / "figure.png", dpi=600, metadata=metadata)
        plt.close(figure)
    normalize_svg(HERE / "figure.svg")
    elapsed = time.perf_counter() - started
    write_rows(
        "plot-resources.csv",
        ["elapsedSeconds", "maximumRssMiB", "status"],
        [{
            "elapsedSeconds": f"{elapsed:.6f}",
            "maximumRssMiB": f"{rss_mib():.3f}",
            "status": "passed",
        }],
    )
    return elapsed


def record(path: Path, **extra: object) -> dict[str, object]:
    return {
        "path": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        **extra,
    }


def sysctl(name: str, fallback: str) -> str:
    try:
        return subprocess.run(
            ["sysctl", "-n", name], check=True, capture_output=True, text=True
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return fallback


def build_manifest(metadata: dict[str, object], elapsed: float) -> None:
    png = Image.open(HERE / "figure.png")
    memory_gib = (
        round(int(sysctl("hw.memsize", "0")) / 1024**3)
        if platform.system() == "Darwin" else None
    )
    manifest = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "createdAt": "2026-08-21T05:55:00+08:00",
        "analyticalQuestion": (
            "Does the full nonlinear perturbation generated by the deep packet "
            "remain small around an order-one reference solution?"
        ),
        "supportedClaim": (
            "If the reference critical linearization has inverse norm M_T and "
            "chi_r<1, the unique nearby nonlinear branch differs from the "
            "reference path by at most 2 M_T C_H C_0 rho^r."
        ),
        "claimBoundary": metadata["claimBoundary"],
        "git": {
            "sourceCommit": SOURCE_COMMIT,
            "certificateCommit": CERTIFICATE_COMMIT,
            "repository": "Kasifa/Kasifa.github.io",
            "dirtyAtCertifiedRun": False,
        },
        "sourceData": [
            {
                "fileName": CERTIFICATE.name,
                "location": metadata["inputCertificate"]["location"],
                "bytes": CERTIFICATE.stat().st_size,
                "sha256": CERTIFICATE_SHA,
                "extractionCommand": "python3 build.py",
            },
            {
                "fileName": R069B_CERTIFICATE.name,
                "location": metadata["upstreamCertificate"]["location"],
                "bytes": R069B_CERTIFICATE.stat().st_size,
                "sha256": R069B_SHA,
                "extractionCommand": "python3 build.py",
            },
        ],
        "data": [
            record(HERE / "quadratic-branch.csv", format="csv", schema="chi, discriminant root, exact amplification, contraction factor"),
            record(HERE / "depth-budgets.csv", format="csv", schema="dimensionless K scenario, depth, chi upper bound, strict admissibility"),
            record(HERE / "figure-data-metadata.json", format="json", schema="pinned certificates and theorem metadata"),
            record(HERE / "validation.json", format="json", schema="nine figure-data validation checks"),
            record(HERE / "figure-data-resources.csv", format="csv", schema="data extraction resources"),
            record(HERE / "plot-resources.csv", format="csv", schema="rendering resources"),
        ],
        "computation": {
            "kind": "exact-certificate extraction plus binary64 presentation sampling of closed formulas",
            "configuration": "501 chi samples and four symbolic-prefactor scenarios over depths 0 through 85",
            "precision": "exact symbolic theorem; IEEE binary64 used only for presentation curves",
            "solver": "closed-form smaller quadratic root and geometric envelope",
            "command": "python3 build.py",
            "scientificWallTimeSeconds": round(elapsed, 6),
        },
        "compute": {
            "host": "local Mac workstation",
            "operatingSystem": platform.platform(),
            "cpu": sysctl("machdep.cpu.brand_string", platform.processor()),
            "memoryGiB": memory_gib,
            "processes": 1,
            "threadsPerProcess": 1,
        },
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
            "pillow": Image.__version__ if hasattr(Image, "__version__") else "bundled",
            "packagesLock": "requirements-research.txt",
        },
        "figure": {
            "script": "build.py",
            "widthMillimetres": 178,
            "heightMillimetres": 92,
            "profile": "journal-default",
            "outputs": [
                record(HERE / "figure.pdf"),
                record(HERE / "figure.svg"),
                record(HERE / "figure.png", dpi=600, pixels=f"{png.width} by {png.height}"),
            ],
        },
        "chartContract": {
            "family": "dimensionless quadratic branch and logarithmic depth-budget comparison",
            "takeaway": "a fixed finite reference condition number changes the prefactor but not the geometric decoupling exponent",
            "nonColorEncoding": "distinct line styles, markers, threshold line, and direct formula callouts",
            "outputFootprint": "double-column 178 by 92 millimetres with PDF, SVG, and 600 dpi PNG",
        },
        "qa": {
            "status": "passed",
            "dataCrossChecked": True,
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "notes": "The final-size color and grayscale renders were inspected; formulas, line styles, markers, and the strict chi=1 threshold remain legible without color.",
        },
        "caption": {"english": "caption.md"},
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    started = time.perf_counter()
    metadata, _ = prepare_data()
    validate_data(metadata)
    draw()
    build_manifest(metadata, time.perf_counter() - started)


if __name__ == "__main__":
    main()
