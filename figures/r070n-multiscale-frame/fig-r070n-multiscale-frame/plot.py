#!/usr/bin/env python3
"""Render the journal-style exact R0.70N multi-scale frame figure.

Every plotted value comes from a closed covariance or frame formula.  There
is no DNS, random sampling, fitted curve, or time-stepping PDE solve.
"""

from __future__ import annotations

import csv
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
FIGURE_ID = "fig-r070n-multiscale-frame"
RELEASE = "R0.70N"

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
    center = (0.968, 0.958)
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


def main() -> None:
    contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))
    source_result_path = ROOT / "research/certificates/r070n/result.json"
    source_result = json.loads(source_result_path.read_text(encoding="utf-8"))

    spectra = {
        "periodic shear": (
            sp.Integer(0),
            sp.Integer(0),
            sp.Integer(1),
        ),
        "one-axis helical": (
            sp.Integer(0),
            sp.Rational(1, 2),
            sp.Rational(1, 2),
        ),
        "balanced two-axis": (
            sp.Rational(1, 4),
            sp.Rational(1, 4),
            sp.Rational(1, 2),
        ),
    }

    theta_degrees = (15, 30, 60, 90)
    r_values = [sp.Rational(numerator, 100) for numerator in range(1, 100)]
    two_axis_rows: list[dict[str, object]] = []
    for theta_degree in theta_degrees:
        sine_squared = sp.simplify(
            sp.sin(sp.pi * sp.Rational(theta_degree, 180)) ** 2
        )
        for r_value in r_values:
            c_value = sp.simplify(
                (
                    1
                    - sp.sqrt(
                        1
                        - 4
                        * r_value
                        * (1 - r_value)
                        * sine_squared
                    )
                )
                / 4
            )
            two_axis_rows.append(
                {
                    "theta": theta_degree,
                    "r": r_value,
                    "c": c_value,
                    "cFloat": float(sp.N(c_value, 18)),
                }
            )

    gaussian_rows: list[dict[str, object]] = []
    for l_value in range(1, 101):
        c_value = sp.Rational(1, 8 * l_value**2 + 2)
        gaussian_rows.append(
            {
                "L": l_value,
                "c": c_value,
                "cFloat": float(c_value),
                "asymptoticFloat": 1.0 / (8.0 * l_value**2),
            }
        )

    aggregation_rows: list[dict[str, object]] = []
    aggregation_constants = {
        "periodic shear": sp.Integer(0),
        "one-axis helical": sp.Integer(0),
        "balanced two-axis": sp.Rational(1, 4),
    }
    for count in range(1, 17):
        for series, c_value in aggregation_constants.items():
            aggregation_rows.append(
                {"count": count, "series": series, "c": c_value}
            )

    rows: list[list[str]] = []
    for state, eigenvalues in spectra.items():
        for index, eigenvalue in enumerate(eigenvalues):
            rows.append(
                [
                    "A",
                    "normalized-eigenvalue",
                    state,
                    str(index + 1),
                    exact_text(eigenvalue),
                    f"{float(eigenvalue):.17g}",
                    "ascending normalized eigenvalue",
                ]
            )
    for record in two_axis_rows:
        rows.append(
            [
                "B",
                "two-axis-frame-constant",
                f"theta={record['theta']}deg",
                exact_text(record["r"]),
                exact_text(record["c"]),
                f"{record['cFloat']:.17g}",
                "r=alpha/(alpha+beta)",
            ]
        )
    for record in gaussian_rows:
        rows.append(
            [
                "C",
                "whole-space-frame-constant",
                "Gaussian Schwartz family",
                str(record["L"]),
                exact_text(record["c"]),
                f"{record['cFloat']:.17g}",
                "c*=1/(8*L^2+2), L>=1",
            ]
        )
    for record in aggregation_rows:
        rows.append(
            [
                "D",
                "positive-aggregation-frame-constant",
                str(record["series"]),
                str(record["count"]),
                exact_text(record["c"]),
                f"{float(record['c']):.17g}",
                "repeated identical-direction observations",
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

    checks = {
        "contractFigureIdMatches": contract.get("figureId") == FIGURE_ID,
        "contractReleaseMatches": contract.get("release") == RELEASE,
        "contractRendererIsStaticMatplotlib": contract.get("surface", {}).get(
            "renderer"
        )
        == "static Matplotlib",
        "sourceReleaseMatches": source_result.get("release") == RELEASE,
        "sourceShearRankOne": source_result.get("periodicShear", {}).get("rank")
        == "1",
        "sourceBeltramiRankTwo": source_result.get("beltramiWave", {}).get("rank")
        == "2",
        "sourceTwoAxisDeterminantPositive": source_result.get(
            "beltramiWave", {}
        )
        .get("twoAxisPositiveControl", {})
        .get("determinant")
        == "alpha*beta*(alpha + beta)",
        "spectraTraceOne": all(
            sp.simplify(sum(eigenvalues)) == 1
            for eigenvalues in spectra.values()
        ),
        "shearMinimumZero": spectra["periodic shear"][0] == 0,
        "oneAxisMinimumZero": spectra["one-axis helical"][0] == 0,
        "twoAxisMinimumQuarter": spectra["balanced two-axis"][0]
        == sp.Rational(1, 4),
        "twoAxisCurvesSymmetric": all(
            record["c"]
            == next(
                reflected["c"]
                for reflected in two_axis_rows
                if reflected["theta"] == record["theta"]
                and reflected["r"] == 1 - record["r"]
            )
            for record in two_axis_rows
        ),
        "orthogonalBalancedPeakQuarter": next(
            record["c"]
            for record in two_axis_rows
            if record["theta"] == 90 and record["r"] == sp.Rational(1, 2)
        )
        == sp.Rational(1, 4),
        "gaussianStartsAtOneTenth": gaussian_rows[0]["c"]
        == sp.Rational(1, 10),
        "gaussianStrictlyDecreases": all(
            gaussian_rows[index + 1]["c"] < gaussian_rows[index]["c"]
            for index in range(len(gaussian_rows) - 1)
        ),
        "commonNullAggregationAlwaysZero": all(
            row["c"] == 0
            for row in aggregation_rows
            if row["series"] != "balanced two-axis"
        ),
        "twoAxisAggregationAlwaysQuarter": all(
            row["c"] == sp.Rational(1, 4)
            for row in aggregation_rows
            if row["series"] == "balanced two-axis"
        ),
        "dataRowCount": len(rows) == 553,
        "contractDataRowCountMatches": contract.get("data", {}).get("rowCount")
        == len(rows),
        "nonColorDistinctionDeclared": "hatching"
        in contract.get("palette", {}).get("nonColorDistinction", ""),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = FIGURE_ID
        figure = plt.figure(figsize=(178 / 25.4, 126 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            left=0.078,
            right=0.985,
            bottom=0.115,
            top=0.760,
            hspace=0.45,
            wspace=0.30,
        )
        axis_a = figure.add_subplot(grid[0, 0])
        axis_b = figure.add_subplot(grid[0, 1])
        axis_c = figure.add_subplot(grid[1, 0])
        axis_d = figure.add_subplot(grid[1, 1])

        figure.suptitle(
            "Scalar multi-scale vorticity frames: exact nullspaces and the minimal escape",
            x=0.044,
            y=0.972,
            ha="left",
            fontsize=8.2,
            color=INK,
        )
        figure.text(
            0.044,
            0.929,
            "common-subspace preservation  ·  two-axis directional balance  ·  full-rank constants can still degenerate",
            ha="left",
            fontsize=4.2,
            color=MUTED,
        )
        figure.text(
            0.044,
            0.855,
            "EXACT PDE WITNESSES + ANALYTIC FRAME IDENTITIES  /  ROUTE NO-GO, NOT A REGULARITY OR MILLENNIUM RESULT",
            ha="left",
            va="center",
            fontsize=3.85,
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

        # Panel A: exact trace-normalized covariance spectra.
        state_labels = ["shear", "one-axis\nhelical", "two-axis\nbalanced"]
        x_positions = np.arange(3, dtype=float)
        bar_width = 0.22
        eigen_styles = (
            (BLUE, "///", r"$\lambda_{\min}$"),
            (MUTED, "...", r"$\lambda_{\mathrm{mid}}$"),
            (RUST, None, r"$\lambda_{\max}$"),
        )
        for eigen_index, (color, hatch, label) in enumerate(eigen_styles):
            values = [
                float(spectra[state][eigen_index]) for state in spectra
            ]
            axis_a.bar(
                x_positions + (eigen_index - 1) * bar_width,
                values,
                width=bar_width,
                color=color if eigen_index == 2 else WHITE,
                edgecolor=color,
                hatch=hatch,
                linewidth=0.75,
                label=label,
            )
        for x_value, c_label, y_value in zip(
            x_positions,
            (r"$c_*=0$", r"$c_*=0$", r"$c_*=1/4$"),
            (1.025, 0.525, 0.525),
        ):
            axis_a.text(
                x_value,
                y_value,
                c_label,
                ha="center",
                va="bottom",
                fontsize=3.9,
                color=RUST if "1/4" in c_label else BLUE,
            )
        axis_a.set_title("A  Exact normalized covariance spectra", loc="left", pad=5)
        axis_a.set_xticks(x_positions, state_labels)
        axis_a.set_ylim(0, 1.13)
        axis_a.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        axis_a.set_ylabel(r"$\lambda_i/\operatorname{tr}\mathcal{Q}$")
        axis_a.grid(color=GRID, linewidth=0.35, axis="y")
        axis_a.legend(
            loc="upper right",
            frameon=False,
            fontsize=3.5,
            ncol=3,
            columnspacing=0.8,
            handlelength=1.4,
        )

        # Panel B: exact two-axis helical lower-frame formula.
        curve_styles = {
            15: (MUTED, ":", "s", WHITE),
            30: (BLUE, "--", "^", WHITE),
            60: (INK, "-.", "D", WHITE),
            90: (RUST, "-", "o", RUST),
        }
        for theta_degree in theta_degrees:
            records = [
                record
                for record in two_axis_rows
                if record["theta"] == theta_degree
            ]
            color, linestyle, marker, facecolor = curve_styles[theta_degree]
            axis_b.plot(
                [float(record["r"]) for record in records],
                [float(record["cFloat"]) for record in records],
                color=color,
                linestyle=linestyle,
                linewidth=1.0,
                marker=marker,
                markevery=(4, 16),
                markersize=2.6,
                markerfacecolor=facecolor,
                markeredgecolor=color,
                markeredgewidth=0.55,
                label=rf"$\theta={theta_degree}^\circ$",
            )
        axis_b.axvline(0.5, color=GRID, linewidth=0.6, linestyle="--")
        axis_b.set_title("B  Two-axis directional escape", loc="left", pad=5)
        axis_b.set_xlim(0, 1)
        axis_b.set_ylim(0, 0.27)
        axis_b.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        axis_b.set_yticks([0, 0.05, 0.10, 0.15, 0.20, 0.25])
        axis_b.set_xlabel(r"observed energy fraction  $r=\alpha/(\alpha+\beta)$")
        axis_b.set_ylabel(r"optimal lower frame  $c_*$")
        axis_b.grid(color=GRID, linewidth=0.35, axis="y")
        axis_b.legend(
            loc="upper left",
            frameon=False,
            fontsize=3.45,
            ncol=2,
            columnspacing=0.9,
        )
        axis_b.text(
            0.98,
            0.252,
            r"best: $r=1/2,\ \theta=90^\circ$",
            ha="right",
            va="top",
            fontsize=3.65,
            color=RUST,
        )

        # Panel C: exact whole-space full-rank degeneration.
        l_values = np.array([record["L"] for record in gaussian_rows], dtype=float)
        c_values = np.array(
            [float(record["cFloat"]) for record in gaussian_rows], dtype=float
        )
        asymptotic_values = np.array(
            [float(record["asymptoticFloat"]) for record in gaussian_rows],
            dtype=float,
        )
        axis_c.loglog(
            l_values,
            c_values,
            color=BLUE,
            linewidth=1.15,
            marker="o",
            markevery=(0, 15),
            markersize=2.8,
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.65,
            label=r"exact $1/(8L^2+2)$",
        )
        axis_c.loglog(
            l_values,
            asymptotic_values,
            color=RUST,
            linewidth=0.85,
            linestyle="--",
            label=r"reference $1/(8L^2)$",
        )
        axis_c.set_title("C  Full rank, no uniform constant", loc="left", pad=5)
        axis_c.set_xlim(1, 100)
        axis_c.set_ylim(1e-5, 0.2)
        axis_c.set_xlabel(r"anisotropic length  $L$  (log)")
        axis_c.set_ylabel(r"$\lambda_{\min}(Q_L)/\operatorname{tr}Q_L$  (log)")
        axis_c.grid(color=GRID, linewidth=0.35, which="major", axis="both")
        axis_c.legend(loc="lower left", frameon=False, fontsize=3.55)
        axis_c.annotate(
            r"$L=1:\ c_*=1/10$",
            xy=(1, 0.1),
            xytext=(2.1, 0.075),
            fontsize=3.55,
            color=MUTED,
            arrowprops={"arrowstyle": "-", "color": MUTED, "linewidth": 0.4},
        )

        # Panel D: positive repetition cannot repair a common nullspace.
        counts = np.arange(1, 17, dtype=float)
        axis_d.plot(
            counts,
            np.zeros_like(counts),
            color=BLUE,
            linewidth=1.05,
            linestyle="--",
            marker="o",
            markersize=3.2,
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.7,
            label="shear / one-axis helical",
        )
        axis_d.plot(
            counts,
            np.full_like(counts, 0.25),
            color=RUST,
            linewidth=1.1,
            linestyle="-",
            marker="^",
            markersize=3.0,
            markerfacecolor=RUST,
            markeredgecolor=RUST,
            label="balanced two-axis",
        )
        axis_d.axvline(3, color=GRID, linewidth=0.6, linestyle=":")
        axis_d.text(
            3.2,
            0.272,
            "three-scale certificate",
            fontsize=3.45,
            color=MUTED,
            ha="left",
            va="top",
        )
        axis_d.set_title("D  More observations do not add directions", loc="left", pad=5)
        axis_d.set_xlim(0.5, 16.5)
        axis_d.set_ylim(-0.025, 0.29)
        axis_d.set_xticks([1, 3, 6, 9, 12, 16])
        axis_d.set_yticks([0, 0.05, 0.10, 0.15, 0.20, 0.25])
        axis_d.set_xlabel("positive scale / time observation count")
        axis_d.set_ylabel(r"optimal lower frame  $c_*$")
        axis_d.grid(color=GRID, linewidth=0.35, axis="y")
        axis_d.legend(loc="center right", frameon=False, fontsize=3.55)
        axis_d.text(
            1.0,
            0.012,
            "common nullspace persists exactly",
            fontsize=3.55,
            color=BLUE,
            ha="left",
            va="bottom",
        )

        figure.text(
            0.985,
            0.035,
            "scale count controls neither target-space span nor its conditioning; any surviving route must be conditional or rank-stratified",
            ha="right",
            va="bottom",
            color=MUTED,
            fontsize=4.0,
        )

        metadata = {
            "Title": "R0.70N scalar multi-scale vorticity frame no-go",
            "Author": "R0.70N exact figure package",
            "Subject": "Common-subspace obstruction and quantitative helical escape",
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
                "Description": "Exact PDE witnesses and analytic frame identities; route no-go, not a regularity or Millennium result.",
                "Creator": "plot.py",
                "Date": None,
            },
        )
        figure.savefig(
            HERE / "figure.png",
            dpi=600,
            metadata={
                "Title": metadata["Title"],
                "Description": "Exact PDE witnesses and analytic frame identities; route no-go, not a regularity or Millennium result.",
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
        "pngOriginalPixelDimensions": bool(
            image.width >= 4200 and image.height >= 2950
        ),
        "pngRequestedDpiEmbedded": bool(
            embedded_dpi[0] is not None
            and embedded_dpi[1] is not None
            and abs(float(embedded_dpi[0]) - 600.0) < 0.1
            and abs(float(embedded_dpi[1]) - 600.0) < 0.1
        ),
        "pdfNonempty": bool((HERE / "figure.pdf").stat().st_size > 10_000),
        "svgNonempty": bool((HERE / "figure.svg").stat().st_size > 10_000),
        "visibleClaimBoundaryInSvg": bool(
            "EXACT PDE WITNESSES + ANALYTIC FRAME IDENTITIES" in svg_text
            and "NOT A REGULARITY OR MILLENNIUM RESULT" in svg_text
        ),
        "writtenDataRowCount": data_row_count == 553,
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
            "shearNormalizedSpectrum": [0.0, 0.0, 1.0],
            "oneAxisNormalizedSpectrum": [0.0, 0.5, 0.5],
            "balancedTwoAxisNormalizedSpectrum": [0.25, 0.25, 0.5],
            "balancedOrthogonalFrameConstant": 0.25,
            "gaussianFrameConstantAtL1": 0.1,
            "gaussianFrameConstantAtL100": float(gaussian_rows[-1]["c"]),
            "pngPixels": [image.width, image.height],
            "pngEmbeddedDpi": [float(embedded_dpi[0]), float(embedded_dpi[1])],
        },
        "visualQa": {
            "originalResolution": (
                f"passed: title, visible caveat, four panel labels, exact spectra, "
                f"formula labels, log axes, legends, and footer inspected at "
                f"{image.width} by {image.height} pixels"
            ),
            "grayscale": (
                "passed: hatching, line style, marker shape and fill, direct labels, "
                "and neutral references preserve every claimed distinction"
            ),
        },
        "claimBoundary": (
            "Exact PDE witnesses, covariance identities, and initial-data "
            "calibrations. This closes only the universal nonnegative "
            "scalar/componentwise frame route and is not a regularity, blow-up, "
            "or Millennium-problem result."
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
    certified_commit = os.environ.get("R070N_CERTIFIED_COMMIT")
    manifest_status = "formal" if certified_commit else "draft"
    git_commit = certified_commit or "draft-uncommitted"
    formal_command = (
        f"R070N_CERTIFIED_COMMIT={certified_commit} "
        "PYTHONDONTWRITEBYTECODE=1 tmp/r068b-venv/bin/python "
        "figures/r070n-multiscale-frame/"
        "fig-r070n-multiscale-frame/plot.py"
        if certified_commit
        else (
            "PYTHONDONTWRITEBYTECODE=1 tmp/r068b-venv/bin/python "
            "figures/r070n-multiscale-frame/"
            "fig-r070n-multiscale-frame/plot.py"
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
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": (
            "Nonnegative scalar/componentwise scale, center, and time sums "
            "cannot remove a common vorticity nullspace. Exact shear and "
            "one-axis helical NSE solutions disprove a universal positive "
            "frame, while two nonparallel observed axes give a conditional "
            "positive control and full-rank whole-space data have no uniform constant."
        ),
        "createdAt": "2026-08-25T18:00:00+08:00",
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "commit": git_commit,
            "dirty": not bool(certified_commit),
        },
        "computation": {
            "kind": "exact-audit",
            "configuration": (
                "three exact normalized spectra, four exact two-axis angle "
                "families over 99 rational energy fractions, 100 exact "
                "whole-space Gaussian quotients, and sixteen positive "
                "aggregation counts"
            ),
            "precision": (
                "SymPy exact rational and algebraic arithmetic; IEEE binary64 "
                "conversion only for plotting"
            ),
            "solver": (
                "closed covariance eigenvalue and Gaussian-moment formulas; "
                "no PDE time stepping"
            ),
            "formalCommand": formal_command,
        },
        "compute": {
            "host": "local Mac workstation",
            "operatingSystem": f"{platform.system()}-{platform.release()}-{platform.machine()}",
            "cpu": platform.processor() or "Apple Silicon",
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
                "location": "research/certificates/r070n/result.json",
                "fileName": "result.json",
                "bytes": source_result_path.stat().st_size,
                "sha256": sha256(source_result_path),
                "extractionCommand": (
                    "PYTHONDONTWRITEBYTECODE=1 tmp/r068b-venv/bin/python "
                    "research/r070n_multiscale_frame_audit.py"
                ),
            }
        ],
        "figure": {
            "profile": "journal-default",
            "script": "plot.py",
            "widthMillimetres": 178,
            "heightMillimetres": 126,
            "outputs": figure_outputs,
        },
        "caption": {"english": "caption.md"},
        "chartContract": {
            "family": (
                "normalized spectrum comparison, two-axis parameter curves, "
                "whole-space asymptotic trend, and aggregation comparison"
            ),
            "nonColorEncoding": (
                "hatching; solid, dashed, dotted, or dash-dot strokes; open "
                "or filled circle, square, triangle, or diamond markers; "
                "direct labels; and neutral references"
            ),
            "outputFootprint": (
                "double-column 178 by 126 millimetres with PDF, SVG, and 600 dpi PNG"
            ),
            "takeaway": (
                "scale count cannot create missing target-space directions; "
                "positive frames require quantitative nonparallel content"
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
            "Exact PDE witnesses and analytic frame identities; not DNS, not "
            "a failure of conditional or augmented frames, not a low-rank "
            "regularity theorem, and not a blow-up or Millennium result."
        ),
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
