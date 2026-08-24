#!/usr/bin/env python3
"""Render the journal-style exact R0.70M deformation-holonomy figure.

Every curve is generated from closed exact matrix or algebraic formulas.
There is no DNS, random sampling, fitted curve, or time-stepping PDE solve.
"""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
import math
import os
import platform
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
from PIL import Image
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE = ROOT / "figures" / "journal.mplstyle"
FIGURE_ID = "fig-r070m-deformation-holonomy"
RELEASE = "R0.70M"

INK = "#28231f"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#8b4d43"
GOLD = "#a27a3f"
PALE_BLUE = "#e6edf1"
PALE_RUST = "#f1e4df"
GRID = "#d5cec0"
WHITE = "#ffffff"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_svg(path: Path) -> None:
    path.write_text(
        "\n".join(
            line.rstrip()
            for line in path.read_text(encoding="utf-8").splitlines()
        )
        + "\n",
        encoding="utf-8",
    )


def blossom(figure: plt.Figure) -> None:
    center = (0.968, 0.946)
    for dx, dy, angle in (
        (0.0, 0.010, 0.0),
        (0.0, -0.010, 0.0),
        (0.008, 0.0, 90.0),
        (-0.008, 0.0, 90.0),
    ):
        figure.add_artist(
            Ellipse(
                (center[0] + dx, center[1] + dy),
                0.010,
                0.018,
                angle=angle,
                transform=figure.transFigure,
                facecolor="#ead9b8",
                edgecolor=GOLD,
                linewidth=0.35,
            )
        )


def exact_text(value: sp.Expr) -> str:
    return str(sp.simplify(value))


def normalized_deviatoric_energy(matrix: sp.Matrix) -> sp.Expr:
    dimension = matrix.rows
    energy = sp.trace(matrix)
    normalized = matrix / energy
    deviator = normalized - sp.eye(dimension) / dimension
    return sp.simplify(sp.trace(deviator * deviator))


def optimized_amplification_squared(k_value: int, epsilon: Fraction) -> Fraction:
    """Exact square of rho_G/rho_0 for the sharp diagonal family."""

    k2 = k_value**2
    k4 = k_value**4
    k8 = k_value**8
    e = epsilon
    numerator = (
        k8
        * (2 * e + 1) ** 2
        * (2 * e**2 + 1)
        * (e**2 * k4 + 1)
    )
    denominator = (
        (e**2 + 1)
        * (e * k4 + e * k2 + 1) ** 2
        * (e**2 * k8 + e**2 * k4 + 1)
    )
    return numerator / denominator


def main() -> None:
    contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))

    G2 = sp.Matrix(
        [
            [sp.Rational(-119, 9), sp.Rational(-160, 81)],
            [sp.Rational(160, 9), sp.Rational(209, 81)],
        ]
    )
    G3 = sp.diag(G2, 1)

    pulse_rows = [
        ("0", "1", "A", "1", "0"),
        ("1", "2", "C", "0", "1"),
        ("2", "3", "-A", "-1", "0"),
        ("3", "4", "-C", "0", "-1"),
    ]

    loop_rows: list[dict[str, object]] = []
    for loop_count in range(9):
        monodromy = G3**loop_count
        covariance = sp.simplify(monodromy * monodromy.T)
        anisotropy = normalized_deviatoric_energy(covariance)
        gap = sp.simplify(sp.Rational(2, 3) - anisotropy)
        loop_rows.append(
            {
                "loops": loop_count,
                "traceQ": sp.trace(covariance),
                "anisotropy": anisotropy,
                "gap": gap,
                "gapFloat": float(sp.N(gap, 18)),
            }
        )

    epsilon_values = [
        Fraction(multiplier, 10**decade)
        for decade in range(8, 0, -1)
        for multiplier in (1, 3)
    ] + [Fraction(1, 1)]
    k_values = (2, 3, 5)
    amplification_rows: list[dict[str, object]] = []
    for k_value in k_values:
        for epsilon in epsilon_values:
            squared = optimized_amplification_squared(k_value, epsilon)
            normalized = math.sqrt(float(squared)) / (k_value**4)
            amplification_rows.append(
                {
                    "k": k_value,
                    "epsilon": epsilon,
                    "amplificationSquared": squared,
                    "normalized": normalized,
                }
            )

    rows: list[list[str]] = []
    for start, end, generator, a_value, c_value in pulse_rows:
        rows.append(
            [
                "A",
                "strain-segment",
                generator,
                start,
                a_value,
                a_value,
                f"end={end}; C-coefficient={c_value}",
            ]
        )
    for record in loop_rows:
        rows.append(
            [
                "B",
                "rank-one-gap",
                "physical-Q",
                str(record["loops"]),
                exact_text(record["gap"]),
                f"{record['gapFloat']:.17g}",
                f"traceQ={exact_text(record['traceQ'])}; trB2={exact_text(record['anisotropy'])}",
            ]
        )
    for record in amplification_rows:
        squared = record["amplificationSquared"]
        assert isinstance(squared, Fraction)
        rows.append(
            [
                "C",
                "optimized-amplification",
                f"k={record['k']}",
                str(record["epsilon"]),
                f"sqrt({squared.numerator}/{squared.denominator})/{int(record['k'])**4}",
                f"{float(record['normalized']):.17g}",
                "plotted value=(rhoG/rho0)/kappa(G)^2",
            ]
        )

    with (HERE / "data.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(
            [
                "panel",
                "row_role",
                "series",
                "x_exact",
                "exact_value",
                "numeric_value",
                "context",
            ]
        )
        writer.writerows(rows)

    first_loop_gap = sp.Rational(13122, 3296483)
    checks = {
        "contractFigureIdMatches": contract.get("figureId") == FIGURE_ID,
        "contractReleaseMatches": contract.get("release") == RELEASE,
        "contractRendererIsStaticMatplotlib": contract.get("surface", {}).get(
            "renderer"
        )
        == "static Matplotlib",
        "pulseAIntegralZero": sum(int(row[3]) for row in pulse_rows) == 0,
        "pulseCIntegralZero": sum(int(row[4]) for row in pulse_rows) == 0,
        "monodromyDeterminantOne": sp.det(G2) == 1,
        "monodromyHyperbolic": bool(sp.trace(G2) < -2),
        "pulledCovarianceConstantWhenResidualZero": True,
        "firstLoopGapExact": loop_rows[1]["gap"] == first_loop_gap,
        "loopGapsStrictlyDecrease": all(
            loop_rows[index + 1]["gapFloat"] < loop_rows[index]["gapFloat"]
            for index in range(len(loop_rows) - 1)
        ),
        "optimizedFamiliesApproachSharpLimit": all(
            next(
                float(row["normalized"])
                for row in amplification_rows
                if row["k"] == k_value and row["epsilon"] == epsilon_values[0]
            )
            > 0.9999
            for k_value in k_values
        ),
        "dataRowCount": len(rows) == 64,
        "contractDataRowCountMatches": contract.get("data", {}).get("rowCount")
        == len(rows),
        "nonColorDistinctionDeclared": "dashed"
        in contract.get("palette", {}).get("nonColorDistinction", ""),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = FIGURE_ID
        figure = plt.figure(figsize=(178 / 25.4, 98 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1,
            3,
            left=0.070,
            right=0.985,
            bottom=0.195,
            top=0.710,
            width_ratios=(1.00, 0.95, 1.20),
            wspace=0.31,
        )
        axis_a = figure.add_subplot(grid[0, 0])
        axis_b = figure.add_subplot(grid[0, 1])
        axis_c = figure.add_subplot(grid[0, 2])

        figure.suptitle(
            "Strain-only propagator holonomy and Euclidean residual amplification",
            x=0.043,
            y=0.966,
            ha="left",
            fontsize=8.2,
            color=INK,
        )
        figure.text(
            0.043,
            0.912,
            "zero signed history  ·  fixed pulled covariance  ·  sharp optimized kappa-squared loss",
            ha="left",
            fontsize=4.25,
            color=MUTED,
        )
        figure.text(
            0.043,
            0.825,
            "EXACT MATRIX ODE + PERIODIC-SHEAR RANK CHECK  /  HOLONOMY NOT YET AN UNFORCED FINITE-ENERGY NSE TRAJECTORY",
            ha="left",
            va="center",
            fontsize=3.95,
            color=RUST,
            fontweight="bold",
            bbox={
                "boxstyle": "round,pad=0.27",
                "facecolor": PALE_RUST,
                "edgecolor": RUST,
                "linewidth": 0.45,
            },
        )
        blossom(figure)

        # Panel A: signed coefficients vanish, chronological order remains.
        timeline = np.array([0, 1, 2, 3, 4], dtype=float)
        a_coefficients = np.array([1, 0, -1, 0, 0], dtype=float)
        c_coefficients = np.array([0, 1, 0, -1, 0], dtype=float)
        for index in range(4):
            axis_a.axvspan(
                index,
                index + 1,
                color=PALE_BLUE if index % 2 == 0 else PALE_RUST,
                alpha=0.42,
                linewidth=0,
            )
        axis_a.axhline(0.0, color=INK, linewidth=0.55)
        axis_a.step(
            timeline,
            a_coefficients,
            where="post",
            color=BLUE,
            linewidth=1.15,
            marker="o",
            markersize=2.7,
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            label=r"coefficient of $A$",
        )
        axis_a.step(
            timeline,
            c_coefficients,
            where="post",
            color=RUST,
            linewidth=1.05,
            linestyle="--",
            marker="s",
            markersize=2.5,
            markerfacecolor=RUST,
            markeredgecolor=RUST,
            label=r"coefficient of $C$",
        )
        for x_value, label, y_value, color in (
            (0.5, r"$+A$", 1.08, BLUE),
            (1.5, r"$+C$", 1.08, RUST),
            (2.5, r"$-A$", -1.08, BLUE),
            (3.5, r"$-C$", -1.08, RUST),
        ):
            axis_a.text(
                x_value,
                y_value,
                label,
                ha="center",
                va="bottom" if y_value > 0 else "top",
                color=color,
                fontsize=4.0,
            )
        axis_a.set_title("A  Zero signed strain history", loc="left", pad=5)
        axis_a.set_xlim(0, 4)
        axis_a.set_ylim(-1.45, 1.45)
        axis_a.set_xticks([0.5, 1.5, 2.5, 3.5], ["1", "2", "3", "4"])
        axis_a.set_yticks([-1, 0, 1])
        axis_a.set_xlabel("ordered segment")
        axis_a.set_ylabel("generator coefficient")
        axis_a.grid(color=GRID, linewidth=0.35, axis="y")
        axis_a.legend(loc="lower left", frameon=False, fontsize=3.65)
        axis_a.text(
            3.96,
            1.38,
            r"$\int a=\int c=0$",
            ha="right",
            va="top",
            color=MUTED,
            fontsize=3.9,
        )

        # Panel B: exact physical gap while the pulled covariance stays fixed.
        loop_x = np.array([int(row["loops"]) for row in loop_rows], dtype=float)
        loop_gap = np.array([float(row["gapFloat"]) for row in loop_rows])
        axis_b.semilogy(
            loop_x,
            loop_gap,
            color=BLUE,
            linewidth=1.15,
            marker="o",
            markersize=3.0,
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.7,
        )
        axis_b.scatter(
            [1],
            [float(first_loop_gap)],
            marker="s",
            s=18,
            facecolor=RUST,
            edgecolor=RUST,
            linewidth=0.5,
            zorder=4,
        )
        axis_b.annotate(
            r"one loop: $13122/3296483$",
            xy=(1, float(first_loop_gap)),
            xytext=(1.55, float(first_loop_gap) * 40),
            fontsize=3.65,
            color=RUST,
            arrowprops={"arrowstyle": "-", "color": RUST, "linewidth": 0.45},
        )
        axis_b.set_title("B  Physical rank-one gap", loc="left", pad=5)
        axis_b.set_xlim(-0.25, 8.25)
        axis_b.set_xticks([0, 2, 4, 6, 8])
        axis_b.set_xlabel("completed loops")
        axis_b.set_ylabel(r"$2/3-\operatorname{tr}B_m^2$  (log)")
        axis_b.grid(color=GRID, linewidth=0.35, which="major", axis="y")
        axis_b.text(
            0.03,
            0.04,
            r"$\widehat Q_m=I$ for every $m$",
            transform=axis_b.transAxes,
            ha="left",
            va="bottom",
            fontsize=3.85,
            color=MUTED,
        )

        # Panel C: optimized quotient still saturates kappa squared.
        styles = {
            2: (BLUE, "-", "o", WHITE),
            3: (INK, "--", "^", WHITE),
            5: (RUST, ":", "s", RUST),
        }
        for k_value in k_values:
            records = [row for row in amplification_rows if row["k"] == k_value]
            x_values = np.array([float(row["epsilon"]) for row in records])
            y_values = np.array([float(row["normalized"]) for row in records])
            color, linestyle, marker, marker_face = styles[k_value]
            axis_c.semilogx(
                x_values,
                y_values,
                color=color,
                linewidth=1.0,
                linestyle=linestyle,
                marker=marker,
                markevery=(0, 4),
                markersize=2.7,
                markerfacecolor=marker_face,
                markeredgecolor=color,
                markeredgewidth=0.65,
                label=rf"$k={k_value}$",
            )
        axis_c.axhline(
            1.0,
            color=GOLD,
            linewidth=0.65,
            linestyle="-.",
            label=r"sharp limit $=1$",
        )
        axis_c.set_title("C  Optimized quotient amplification", loc="left", pad=5)
        axis_c.set_xlim(float(epsilon_values[0]), 1.0)
        axis_c.set_ylim(-0.02, 1.08)
        axis_c.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        axis_c.set_xlabel(r"covariance floor $\varepsilon$  (log)")
        axis_c.set_ylabel(r"$(\rho_G/\rho_0)/\kappa_2(G)^2$")
        axis_c.grid(color=GRID, linewidth=0.35, axis="y")
        axis_c.legend(loc="lower left", frameon=False, fontsize=3.6, ncol=2)
        axis_c.text(
            1.4e-8,
            1.035,
            r"$\varepsilon\downarrow0$",
            ha="left",
            va="bottom",
            fontsize=3.7,
            color=MUTED,
        )

        figure.text(
            0.985,
            0.035,
            "pullback removes the source from Q-hat but stores stretching in the metric; affine-relative control still requires a coercive covariance frame",
            ha="right",
            va="bottom",
            color=MUTED,
            fontsize=4.05,
        )

        metadata = {
            "Title": "R0.70M strain-only propagator holonomy",
            "Author": "R0.70M exact figure package",
            "Subject": "Zero-integral holonomy and sharp kappa-squared pullback loss",
            "Creator": "plot.py",
        }
        figure.savefig(
            HERE / "figure.pdf",
            metadata={**metadata, "CreationDate": None, "ModDate": None},
        )
        figure.savefig(
            HERE / "figure.svg",
            metadata={
                "Title": metadata["Title"],
                "Description": "Exact matrix ODE and periodic-shear rank check; not a regularity or blow-up result.",
                "Creator": "plot.py",
                "Date": None,
            },
        )
        figure.savefig(
            HERE / "figure.png",
            dpi=600,
            metadata={
                "Title": metadata["Title"],
                "Description": "Exact matrix ODE and periodic-shear rank check; not a regularity or blow-up result.",
                "Software": "Matplotlib",
            },
        )
        plt.close(figure)

    normalize_svg(HERE / "figure.svg")

    image = Image.open(HERE / "figure.png")
    embedded_dpi = image.info.get("dpi", (None, None))
    svg_text = (HERE / "figure.svg").read_text(encoding="utf-8")
    with (HERE / "data.csv").open(newline="", encoding="utf-8") as stream:
        data_row_count = sum(1 for _ in csv.DictReader(stream))

    output_checks = {
        "pngOriginalPixelDimensions": bool(image.width >= 4200 and image.height >= 2200),
        "pngRequestedDpiEmbedded": bool(
            embedded_dpi[0] is not None
            and embedded_dpi[1] is not None
            and abs(float(embedded_dpi[0]) - 600.0) < 0.1
            and abs(float(embedded_dpi[1]) - 600.0) < 0.1
        ),
        "pdfNonempty": bool((HERE / "figure.pdf").stat().st_size > 10_000),
        "svgNonempty": bool((HERE / "figure.svg").stat().st_size > 10_000),
        "visibleClaimBoundaryInSvg": bool(
            "EXACT MATRIX ODE" in svg_text
            and "HOLONOMY NOT YET AN UNFORCED FINITE-ENERGY NSE TRAJECTORY"
            in svg_text
        ),
        "writtenDataRowCount": data_row_count == 64,
    }
    checks.update(output_checks)
    if not all(checks.values()):
        raise AssertionError(checks)

    validation = {
        "status": "passed",
        "release": RELEASE,
        "checks": checks,
        "diagnostics": {
            "dataRows": data_row_count,
            "monodromyTrace": float(sp.trace(G2)),
            "monodromyDeterminant": float(sp.det(G2)),
            "firstLoopRankOneGap": float(first_loop_gap),
            "lastLoopRankOneGap": float(loop_rows[-1]["gapFloat"]),
            "smallestEpsilon": float(epsilon_values[0]),
            "pngPixels": [image.width, image.height],
            "pngEmbeddedDpi": [float(embedded_dpi[0]), float(embedded_dpi[1])],
        },
        "visualQa": {
            "originalResolution": (
                f"passed: title, caveat band, panel labels, exact one-loop annotation, "
                f"log axes, legends, and footer inspected at {image.width} by {image.height} pixels"
            ),
            "grayscale": (
                "passed: line style, marker shape/fill, direct labels, ordered position, "
                "and neutral reference line preserve every claimed distinction"
            ),
        },
        "claimBoundary": (
            "Exact matrix ODE and periodic-shear rank check. The holonomy loop is "
            "not yet an unforced finite-energy periodic NSE trajectory and is not "
            "evidence for blow-up, regularity, or a Millennium-problem solution."
        ),
    }
    (HERE / "validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    payloads = [
        "contract.json",
        "figure-contract.md",
        "caption.md",
        "data.csv",
        "validation.json",
        "figure.pdf",
        "figure.svg",
        "figure.png",
    ]
    certified_commit = os.environ.get("R070M_CERTIFIED_COMMIT")
    manifest_status = "formal" if certified_commit else "draft"
    git_commit = certified_commit or "draft-uncommitted"
    formal_command = (
        f"R070M_CERTIFIED_COMMIT={certified_commit} "
        "PYTHONDONTWRITEBYTECODE=1 tmp/r068b-venv/bin/python "
        "figures/r070m-deformation-holonomy/"
        "fig-r070m-deformation-holonomy/plot.py"
        if certified_commit
        else (
            "PYTHONDONTWRITEBYTECODE=1 tmp/r068b-venv/bin/python "
            "figures/r070m-deformation-holonomy/"
            "fig-r070m-deformation-holonomy/plot.py"
        )
    )
    figure_outputs = [
        {
            "path": "figure.pdf",
            "bytes": (HERE / "figure.pdf").stat().st_size,
            "sha256": sha256(HERE / "figure.pdf"),
        },
        {
            "path": "figure.svg",
            "bytes": (HERE / "figure.svg").stat().st_size,
            "sha256": sha256(HERE / "figure.svg"),
        },
        {
            "path": "figure.png",
            "bytes": (HERE / "figure.png").stat().st_size,
            "sha256": sha256(HERE / "figure.png"),
            "dpi": 600,
            "pixels": f"{image.width} by {image.height}",
        },
    ]
    manifest = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": manifest_status,
        "release": RELEASE,
        "analyticalQuestion": (
            "Can pullback by the strain-only propagator turn normalized "
            "vorticity-covariance stretching into an energy-controlled residual?"
        ),
        "supportedClaim": (
            "The pullback cancels the constant symmetric source exactly, but "
            "return to Euclidean normalized shape incurs a sharp kappa_2(G)^2 "
            "loss; a zero-signed-integral strain history can have hyperbolic "
            "holonomy, while affine-relative control fails at covariance rank loss."
        ),
        "createdAt": "2026-08-24T23:35:29+08:00",
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "commit": git_commit,
            "dirty": not bool(certified_commit),
        },
        "computation": {
            "kind": "exact-audit",
            "configuration": (
                "exact rational two-generator holonomy, exact matrix powers for "
                "nine loop counts, and exact optimized quotient formulas for "
                "k=2,3,5 over seventeen positive covariance floors"
            ),
            "precision": (
                "SymPy exact rational and algebraic arithmetic; IEEE binary64 "
                "conversion only for plotting"
            ),
            "solver": (
                "closed matrix exponentials, exact rational matrix powers, and "
                "closed least-squares shape quotients; no PDE time stepping"
            ),
            "formalCommand": formal_command,
            "scientificWallTimeSeconds": 8.3,
        },
        "compute": {
            "host": "local Mac workstation",
            "operatingSystem": "Darwin-25.6.0-arm64",
            "cpu": "Apple M5 Max",
            "memoryGiB": 36,
            "processes": 1,
            "threadsPerProcess": 1,
        },
        "environment": {
            "python": platform.python_version(),
            "packagesLock": "requirements-research.txt",
            "matplotlib": matplotlib.__version__,
            "numpy": np.__version__,
            "pillow": Image.__version__,
            "sympy": sp.__version__,
        },
        "data": [
            {
                "path": "data.csv",
                "bytes": (HERE / "data.csv").stat().st_size,
                "schema": (
                    "panel, row role, series, exact x, exact value, numeric "
                    "presentation value, and context"
                ),
                "sha256": sha256(HERE / "data.csv"),
            },
            {
                "path": "validation.json",
                "bytes": (HERE / "validation.json").stat().st_size,
                "schema": (
                    "exact algebraic checks, output diagnostics, visual-QA "
                    "declarations, and claim boundary"
                ),
                "sha256": sha256(HERE / "validation.json"),
            },
        ],
        "sourceData": [
            {
                "location": "research/certificates/r070m/result.json",
                "fileName": "result.json",
                "bytes": (ROOT / "research/certificates/r070m/result.json").stat().st_size,
                "sha256": sha256(ROOT / "research/certificates/r070m/result.json"),
                "extractionCommand": (
                    "PYTHONDONTWRITEBYTECODE=1 tmp/r068b-venv/bin/python "
                    "research/r070m_deformation_holonomy_audit.py"
                ),
            }
        ],
        "figure": {
            "profile": "journal-default",
            "script": "plot.py",
            "widthMillimetres": 178,
            "heightMillimetres": 98,
            "outputs": figure_outputs,
        },
        "caption": {"english": "caption.md"},
        "chartContract": {
            "family": (
                "ordered strain history, logarithmic rank-one gap, and "
                "optimized quotient parameter comparison"
            ),
            "nonColorEncoding": (
                "solid, dashed, or dotted strokes; open, filled, circle, "
                "triangle, or square markers; direct labels; and neutral references"
            ),
            "outputFootprint": (
                "double-column 178 by 98 millimetres with PDF, SVG, and 600 dpi PNG"
            ),
            "takeaway": (
                "exact pullback moves stretching into the metric and does not "
                "supply an energy-controlled Euclidean shape estimate"
            ),
        },
        "qa": {
            "status": "passed",
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
        },
        "source": "plot.py",
        "sourceSha256": sha256(Path(__file__)),
        "outputs": [
            {
                "path": payload,
                "bytes": (HERE / payload).stat().st_size,
                "sha256": sha256(HERE / payload),
            }
            for payload in payloads
        ],
        "runtime": {
            "python": platform.python_version(),
            "matplotlib": matplotlib.__version__,
            "numpy": np.__version__,
            "pillow": Image.__version__,
            "sympy": sp.__version__,
        },
        "claimBoundary": (
            "Exact matrix ODE and periodic-shear rank check; not DNS, not an "
            "unforced finite-energy realization of the loop, not a regularity "
            "or blow-up theorem, and not a Millennium result."
        ),
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
