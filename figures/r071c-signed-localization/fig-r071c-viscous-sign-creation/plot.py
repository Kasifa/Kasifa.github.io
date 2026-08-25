#!/usr/bin/env python3
"""Build the formal R0.71C viscous sign-creation figure.

Every plotted curve is a high-precision evaluation of a closed exact Stokes
formula.  There is no random sampling, fitting, DNS, or numerical time
integration.  Exact identities are checked with SymPy before rendering.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import platform
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
from PIL import Image, ImageOps
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE = ROOT / "figures" / "journal.mplstyle"
FIGURE_ID = "fig-r071c-viscous-sign-creation"
RELEASE = "R0.71C"
WIDTH_MM = 178
HEIGHT_MM = 92
PNG_DPI = 600
TAU_STAR = sp.log(2) / 6

INK = "#28231f"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#985943"
PALE_BLUE = "#e7eef2"
PALE_RUST = "#f2e5df"
GRID = "#d5cec0"
WHITE = "#ffffff"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_float(value: sp.Expr) -> float:
    """Evaluate to 50 decimal digits before conversion to binary64."""

    return float(sp.N(value, 50))


def witness_values(tau: sp.Expr) -> dict[str, sp.Expr]:
    decay8 = sp.exp(-8 * tau)
    decay14 = sp.exp(-14 * tau)
    work1 = 2 * decay8
    work2 = -2 * decay14
    parent = sp.simplify(work1 + work2)
    denominator = 16 * decay8
    if tau == 0:
        root = sp.Integer(0)
    else:
        root = sp.simplify(parent**2 / denominator)
    fine = sp.simplify(work1**2 / (8 * decay8))
    defect = sp.simplify(fine - root)
    return {
        "decay8": decay8,
        "decay14": decay14,
        "w1": work1,
        "w2": work2,
        "W": parent,
        "D_root": denominator,
        "E_root": root,
        "E_fine": fine,
        "delta": defect,
    }


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
    """Place the restrained research mark at the locked top-right anchor."""

    center = (0.970, 0.952)
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
                edgecolor="#9a7742",
                linewidth=0.35,
            )
        )


def git_text(*arguments: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *arguments], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def file_record(path: Path) -> dict[str, object]:
    return {
        "path": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def main() -> None:
    started = time.perf_counter()
    contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))

    tau_symbol = sp.symbols("tau", nonnegative=True)
    decay8_symbol = sp.exp(-8 * tau_symbol)
    decay14_symbol = sp.exp(-14 * tau_symbol)
    work1_symbol = 2 * decay8_symbol
    work2_symbol = -2 * decay14_symbol
    parent_symbol = sp.simplify(work1_symbol + work2_symbol)
    root_positive_symbol = sp.simplify(parent_symbol**2 / (16 * decay8_symbol))
    fine_symbol = sp.simplify(work1_symbol**2 / (8 * decay8_symbol))
    defect_symbol = sp.simplify(fine_symbol - root_positive_symbol)
    explicit_defect_symbol = sp.exp(-8 * tau_symbol) * (
        1 + 2 * sp.exp(-6 * tau_symbol) - sp.exp(-12 * tau_symbol)
    ) / 4

    grid_taus = [sp.Rational(index, 500) for index in range(251)]
    row_taus: list[tuple[str, sp.Expr, str]] = [
        (
            "grid",
            tau,
            "initial exact cancellation" if tau == 0 else "",
        )
        for tau in grid_taus
    ]
    row_taus.append(("exact-marker", TAU_STAR, "tau_star exact ledger checkpoint"))
    row_taus.sort(key=lambda item: exact_float(item[1]))

    rows: list[list[str]] = []
    numeric_rows: list[dict[str, float | str]] = []
    for index, (row_role, tau, event) in enumerate(row_taus):
        exact_values = witness_values(tau)
        numeric = {key: exact_float(value) for key, value in exact_values.items()}
        numeric_rows.append(
            {
                "row_role": row_role,
                "tau": exact_float(tau),
                **numeric,
            }
        )
        rows.append(
            [
                row_role,
                str(index),
                sp.sstr(tau),
                f"{exact_float(tau):.17g}",
                *(f"{numeric[name]:.17g}" for name in (
                    "decay8",
                    "decay14",
                    "w1",
                    "w2",
                    "W",
                    "D_root",
                    "E_root",
                    "E_fine",
                    "delta",
                )),
                event,
            ]
        )

    data_path = HERE / "data.csv"
    with data_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(
            [
                "row_role",
                "index",
                "tau_exact",
                "tau_numeric",
                "decay8",
                "decay14",
                "w1",
                "w2",
                "W",
                "D_root",
                "E_root",
                "E_fine",
                "delta",
                "event",
            ]
        )
        writer.writerows(rows)

    initial = witness_values(sp.Integer(0))
    star = witness_values(TAU_STAR)
    grid_numeric = [record for record in numeric_rows if record["row_role"] == "grid"]
    positive_grid = [record for record in grid_numeric if float(record["tau"]) > 0]

    checks: dict[str, bool] = {
        "contractFigureIdMatches": contract.get("figureId") == FIGURE_ID,
        "contractReleaseMatches": contract.get("release") == RELEASE,
        "contractRendererIsStaticMatplotlib": contract.get("surface", {}).get(
            "renderer"
        )
        == "static Matplotlib",
        "contractDataRowCountMatches": contract.get("data", {}).get("rowCount")
        == len(rows),
        "initialParentCancellationExact": initial["W"] == 0,
        "initialParentLedgerZeroExact": initial["E_root"] == 0,
        "initialFineLedgerHalfExact": initial["E_fine"] == sp.Rational(1, 2),
        "initialDefectHalfExact": initial["delta"] == sp.Rational(1, 2),
        "initialParentDerivativeTwelveExact": sp.diff(
            parent_symbol, tau_symbol
        ).subs(tau_symbol, 0)
        == 12,
        "parentPositiveForPositiveTauAlgebra": sp.simplify(
            parent_symbol
            - 2 * sp.exp(-14 * tau_symbol) * (sp.exp(6 * tau_symbol) - 1)
        )
        == 0,
        "parentPositiveAtEveryPositiveGridTime": all(
            float(record["W"]) > 0 for record in positive_grid
        ),
        "ledgerIdentityExact": sp.simplify(
            fine_symbol - root_positive_symbol - defect_symbol
        )
        == 0,
        "defectClosedFormExact": sp.simplify(
            defect_symbol - explicit_defect_symbol
        )
        == 0,
        "defectNonnegativeAtEveryGridTime": all(
            float(record["delta"]) >= 0 for record in grid_numeric
        ),
        "tauStarRootExact": sp.simplify(
            star["E_root"] - 2 ** sp.Rational(-16, 3)
        )
        == 0,
        "tauStarFineExact": sp.simplify(
            star["E_fine"] - 2 ** sp.Rational(-7, 3)
        )
        == 0,
        "tauStarDefectExact": sp.simplify(
            star["delta"] - 7 * 2 ** sp.Rational(-16, 3)
        )
        == 0,
        "writtenDataRowCount252": len(rows) == 252,
        "noRandomnessUsed": True,
        "nonColorDistinctionDeclared": "line styles"
        in contract.get("palette", {}).get("nonColorDistinction", ""),
    }
    if not all(checks.values()):
        raise AssertionError(
            {name: passed for name, passed in checks.items() if not passed}
        )

    tau_grid = np.asarray([float(record["tau"]) for record in grid_numeric])
    w1_grid = np.asarray([float(record["w1"]) for record in grid_numeric])
    w2_grid = np.asarray([float(record["w2"]) for record in grid_numeric])
    parent_grid = np.asarray([float(record["W"]) for record in grid_numeric])
    root_grid = np.asarray([float(record["E_root"]) for record in grid_numeric])
    fine_grid = np.asarray([float(record["E_fine"]) for record in grid_numeric])
    defect_grid = np.asarray([float(record["delta"]) for record in grid_numeric])
    tau_star_float = exact_float(TAU_STAR)
    star_root = exact_float(star["E_root"])
    star_fine = exact_float(star["E_fine"])
    star_defect = exact_float(star["delta"])

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = FIGURE_ID
        figure = plt.figure(
            figsize=(WIDTH_MM / 25.4, HEIGHT_MM / 25.4), layout="none"
        )
        grid = figure.add_gridspec(
            1,
            2,
            left=0.086,
            right=0.982,
            bottom=0.205,
            top=0.735,
            wspace=0.29,
        )
        axis_a = figure.add_subplot(grid[0, 0])
        axis_b = figure.add_subplot(grid[0, 1])

        figure.suptitle(
            "Viscous creation of positive signed packet work",
            x=0.042,
            y=0.970,
            ha="left",
            fontsize=8.5,
            color=INK,
        )
        figure.text(
            0.042,
            0.917,
            r"two exact output packets  $\cdot$  dimensionless time $\tau=\nu t$  $\cdot$  closed Stokes witness",
            ha="left",
            fontsize=4.35,
            color=MUTED,
        )
        figure.text(
            0.042,
            0.846,
            "EXACT HEAT-SEMIGROUP WITNESS  /  NOT A NAVIER-STOKES CONTINUATION OR REGULARITY RESULT",
            ha="left",
            va="center",
            fontsize=3.65,
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

        axis_a.plot(
            tau_grid,
            w1_grid,
            color=BLUE,
            linestyle="-",
            marker="o",
            markevery=25,
            markersize=2.8,
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.65,
            label=r"positive child  $w_1=2e^{-8\tau}$",
        )
        axis_a.plot(
            tau_grid,
            w2_grid,
            color=RUST,
            linestyle="--",
            marker="^",
            markevery=25,
            markersize=2.8,
            markerfacecolor=RUST,
            markeredgecolor=RUST,
            label=r"negative child  $w_2=-2e^{-14\tau}$",
        )
        axis_a.plot(
            tau_grid,
            parent_grid,
            color=INK,
            linestyle="-.",
            marker="s",
            markevery=25,
            markersize=2.5,
            markerfacecolor=WHITE,
            markeredgecolor=INK,
            markeredgewidth=0.6,
            label=r"parent sum  $W=w_1+w_2$",
        )
        axis_a.axhline(0, color=INK, linewidth=0.75)
        axis_a.scatter([0], [0], s=12, facecolor=WHITE, edgecolor=INK, zorder=6)
        axis_a.annotate(
            r"exact cancellation  $W(0)=0$",
            xy=(0, 0),
            xytext=(0.075, -0.72),
            fontsize=3.7,
            color=INK,
            arrowprops={"arrowstyle": "-", "color": MUTED, "linewidth": 0.5},
        )
        peak_index = int(np.argmax(parent_grid))
        axis_a.annotate(
            r"$W(\tau)>0$ for every $\tau>0$",
            xy=(tau_grid[peak_index], parent_grid[peak_index]),
            xytext=(0.19, 0.80),
            fontsize=3.75,
            color=INK,
            arrowprops={"arrowstyle": "-", "color": MUTED, "linewidth": 0.5},
        )
        axis_a.set_title("A  Signed child and parent work", loc="left", pad=5)
        axis_a.set_xlim(0, 0.5)
        axis_a.set_ylim(-2.12, 2.12)
        axis_a.set_xticks(np.arange(0, 0.51, 0.1))
        axis_a.set_yticks([-2, -1, 0, 1, 2])
        axis_a.set_xlabel(r"dimensionless time  $\tau=\nu t$")
        axis_a.set_ylabel("signed packet work")
        axis_a.grid(color=GRID, linewidth=0.35, axis="y")
        axis_a.legend(loc="upper right", frameon=False, fontsize=3.55)

        axis_b.plot(
            tau_grid,
            fine_grid,
            color=BLUE,
            linestyle="-",
            marker="o",
            markevery=25,
            markersize=2.8,
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.65,
            label=r"fine ledger  $E_{\rm fine}$",
        )
        axis_b.plot(
            tau_grid,
            defect_grid,
            color=RUST,
            linestyle="--",
            marker="^",
            markevery=25,
            markersize=2.8,
            markerfacecolor=RUST,
            markeredgecolor=RUST,
            label=r"refinement defect  $\delta$",
        )
        axis_b.plot(
            tau_grid,
            root_grid,
            color=INK,
            linestyle="-.",
            marker="D",
            markevery=25,
            markersize=2.4,
            markerfacecolor=WHITE,
            markeredgecolor=INK,
            markeredgewidth=0.6,
            label=r"parent ledger  $E_{\rm root}$",
        )
        axis_b.axvline(tau_star_float, color=MUTED, linewidth=0.7, linestyle=":")
        axis_b.scatter(
            [tau_star_float] * 3,
            [star_fine, star_defect, star_root],
            s=[12, 12, 11],
            facecolor=[WHITE, RUST, WHITE],
            edgecolor=[BLUE, RUST, INK],
            linewidth=0.65,
            zorder=6,
        )
        axis_b.text(
            0.48,
            0.92,
            r"$\tau_*=\log 2/6$" + "\n"
            + r"$E_{\rm root}=2^{-16/3}$" + "\n"
            + r"$E_{\rm fine}=2^{-7/3}$" + "\n"
            + r"$\delta=7\,2^{-16/3}$",
            transform=axis_b.transAxes,
            ha="left",
            va="top",
            fontsize=3.7,
            color=INK,
        )
        axis_b.text(
            0.97,
            0.15,
            r"$E_{\rm fine}=E_{\rm root}+\delta$" + "\n" + r"$\delta\geq0$",
            transform=axis_b.transAxes,
            ha="right",
            va="bottom",
            fontsize=3.85,
            color=INK,
        )
        axis_b.set_title("B  Parent ledger and refinement defect", loc="left", pad=5)
        axis_b.set_xlim(0, 0.5)
        axis_b.set_ylim(0, 0.53)
        axis_b.set_xticks(np.arange(0, 0.51, 0.1))
        axis_b.set_yticks(np.arange(0, 0.51, 0.1))
        axis_b.set_xlabel(r"dimensionless time  $\tau=\nu t$")
        axis_b.set_ylabel("ledger mass")
        axis_b.grid(color=GRID, linewidth=0.35, axis="y")
        axis_b.legend(loc="upper right", bbox_to_anchor=(0.995, 0.63), frameon=False, fontsize=3.55)

        figure.text(
            0.042,
            0.095,
            r"At $\tau=0$:  $W=E_{\rm root}=0$ but $E_{\rm fine}=\delta=1/2$.  Unequal viscous decay reveals latent fine-ledger mass at the parent.",
            ha="left",
            fontsize=3.7,
            color=MUTED,
        )
        figure.text(
            0.042,
            0.043,
            "Scope: exact two-packet Stokes evolution and refinement identity; no Navier-Stokes time-integrability or continuation bound is proved.",
            ha="left",
            fontsize=3.72,
            color=INK,
        )

        pdf_metadata = {
            "Title": "R0.71C viscous creation of positive signed packet work",
            "Author": "Chuikuan Zeng",
            "Subject": "Exact two-packet Stokes witness and ledger refinement identity",
            "Keywords": "Navier-Stokes; Stokes; Fourier packets; signed ledger; exact audit",
            "Creator": "Matplotlib reproducible figure script",
            "CreationDate": datetime(2026, 8, 25, tzinfo=timezone.utc),
            "ModDate": datetime(2026, 8, 25, tzinfo=timezone.utc),
        }
        svg_metadata = {
            "Title": "R0.71C viscous creation of positive signed packet work",
            "Description": "Two exact Stokes-work curves and their signed-before-square ledger decomposition.",
            "Creator": "Matplotlib reproducible figure script",
            "Date": "2026-08-25",
        }
        png_metadata = {
            "Title": "R0.71C viscous creation of positive signed packet work",
            "Author": "Chuikuan Zeng",
            "Description": "Closed exact Stokes formulas; no simulation or fitted data.",
            "Software": "Matplotlib reproducible figure script",
        }
        figure.savefig(HERE / "figure.pdf", metadata=pdf_metadata)
        figure.savefig(HERE / "figure.svg", metadata=svg_metadata)
        figure.savefig(HERE / "figure.png", dpi=PNG_DPI, metadata=png_metadata)
        plt.close(figure)

    normalize_svg(HERE / "figure.svg")
    shutil.copyfile(HERE / "figure.png", HERE / "qa-original.png")
    with Image.open(HERE / "figure.png") as image:
        pixel_dimensions = image.size
        embedded_dpi = image.info.get("dpi", (0.0, 0.0))
        ImageOps.grayscale(image).convert("RGB").save(
            HERE / "qa-grayscale.png", dpi=(PNG_DPI, PNG_DPI)
        )
    with Image.open(HERE / "qa-grayscale.png") as gray_image:
        gray_array = np.asarray(gray_image)
        grayscale_dimensions = gray_image.size
        grayscale_is_rgb_gray = bool(
            np.array_equal(gray_array[:, :, 0], gray_array[:, :, 1])
            and np.array_equal(gray_array[:, :, 1], gray_array[:, :, 2])
        )

    svg_text = (HERE / "figure.svg").read_text(encoding="utf-8")
    automatic_output_checks = {
        "pdfNonempty": (HERE / "figure.pdf").stat().st_size > 1000,
        "svgNonempty": (HERE / "figure.svg").stat().st_size > 1000,
        "pngNonempty": (HERE / "figure.png").stat().st_size > 1000,
        "pngWidthMatches178mmAt600dpi": pixel_dimensions[0]
        in {round(WIDTH_MM / 25.4 * PNG_DPI), math.floor(WIDTH_MM / 25.4 * PNG_DPI)},
        "pngHeightMatches92mmAt600dpi": pixel_dimensions[1]
        in {round(HEIGHT_MM / 25.4 * PNG_DPI), math.floor(HEIGHT_MM / 25.4 * PNG_DPI)},
        "pngEmbeddedDpiNear600": all(
            abs(float(value) - PNG_DPI) < 0.02 for value in embedded_dpi
        ),
        "qaOriginalMatchesFigure": sha256(HERE / "qa-original.png")
        == sha256(HERE / "figure.png"),
        "qaGrayscaleDimensionsMatch": grayscale_dimensions == pixel_dimensions,
        "qaGrayscaleIsRgbGray": grayscale_is_rgb_gray,
        "visibleClaimBoundaryInSvg": "NOT A NAVIER-STOKES CONTINUATION OR REGULARITY RESULT"
        in svg_text,
        "visiblePanelLabelsInSvg": all(
            label in svg_text
            for label in (
                "A  Signed child and parent work",
                "B  Parent ledger and refinement defect",
            )
        ),
    }
    checks.update(automatic_output_checks)
    if not all(automatic_output_checks.values()):
        raise AssertionError(
            {
                name: passed
                for name, passed in automatic_output_checks.items()
                if not passed
            }
        )

    independent_path = HERE / "independent-validation.json"
    independent_passed = False
    if independent_path.exists():
        independent_payload = json.loads(independent_path.read_text(encoding="utf-8"))
        independent_passed = (
            independent_payload.get("status") == "passed"
            and independent_payload.get("data", {}).get("sha256") == sha256(data_path)
        )
        checks["independentValidationPassedAndMatchesData"] = independent_passed

    qa_report_path = HERE / "qa-report.md"
    manual_qa_passed = qa_report_path.exists() and "Status: passed" in qa_report_path.read_text(
        encoding="utf-8"
    )
    elapsed = time.perf_counter() - started

    validation = {
        "release": RELEASE,
        "status": "passed"
        if manual_qa_passed and independent_passed
        else "automatic-passed-manual-or-independent-pending",
        "checks": checks,
        "diagnostics": {
            "dataRows": len(rows),
            "tauRange": [0.0, 0.5],
            "tauStep": 1 / 500,
            "tauStar": tau_star_float,
            "initialParentDerivative": 12.0,
            "parentPeakOnGrid": float(parent_grid.max()),
            "parentPeakTauOnGrid": float(tau_grid[int(np.argmax(parent_grid))]),
            "tauStarRoot": star_root,
            "tauStarFine": star_fine,
            "tauStarDefect": star_defect,
            "minimumDefectOnGrid": float(defect_grid.min()),
            "maximumLedgerIdentityResidual": float(
                np.max(np.abs(fine_grid - root_grid - defect_grid))
            ),
            "pngPixels": list(pixel_dimensions),
            "pngEmbeddedDpi": [float(value) for value in embedded_dpi],
            "wallTimeSeconds": round(elapsed, 3),
        },
        "claimBoundary": contract["claimBoundary"],
        "independentValidation": "passed" if independent_passed else "pending",
        "manualVisualQa": "passed" if manual_qa_passed else "pending",
    }
    (HERE / "validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    memory_gib: float | None = None
    try:
        memory_gib = (
            os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 2**30
        )
    except (AttributeError, OSError, ValueError):
        pass
    git_commit = git_text("rev-parse", "HEAD")
    git_dirty = git_text("status", "--short") not in {"", "unavailable"}
    environment_lines = [
        "# R0.71C figure environment",
        "",
        f"- Release: {RELEASE}",
        f"- Figure: {FIGURE_ID}",
        f"- Git core commit: {git_commit}",
        f"- Git worktree dirty at render: {str(git_dirty).lower()}",
        f"- Host: local Mac workstation ({platform.machine()})",
        f"- Operating system: {platform.platform()}",
        f"- Logical CPUs visible: {os.cpu_count()}",
        f"- Physical memory GiB: {memory_gib:.2f}" if memory_gib is not None else "- Physical memory GiB: unavailable",
        "- Processes: 1",
        "- Threads per process: 1",
        "- GPU: not used",
        "- DGX: not used",
        "- Random seed: none; no random operation is present",
        "- Solver: closed formulas and exact identities; no PDE time stepping",
        "- Precision: SymPy exact expressions; 50-digit evaluation followed by binary64 plotting",
        f"- Python: {platform.python_version()}",
        f"- SymPy: {sp.__version__}",
        f"- NumPy: {np.__version__}",
        f"- Matplotlib: {matplotlib.__version__}",
        f"- Pillow: {Image.__version__ if hasattr(Image, '__version__') else 'unknown'}",
        f"- Wall time seconds: {elapsed:.3f}",
    ]
    (HERE / "environment.txt").write_text("\n".join(environment_lines) + "\n", encoding="utf-8")

    metadata = {
        "schemaVersion": "1.0",
        "release": RELEASE,
        "figureId": FIGURE_ID,
        "dataPath": "data.csv",
        "rowCount": len(rows),
        "grain": "251 exact rational tau grid values on [0,1/2], plus the exact marker tau=log(2)/6",
        "formulaSource": "closed exact formulas stated in figure-contract.md",
        "transformations": [
            "Dimensionless time tau=nu*t removes viscosity from the displayed exponents.",
            "The parent ledger applies the positive part before squaring; W(0)=0 is therefore represented exactly, not by a floating threshold.",
            "The refinement defect is computed as E_fine-E_root and independently checked row by row.",
            "The exact marker tau=log(2)/6 is retained as a dedicated CSV row rather than snapped to the uniform plotting grid.",
        ],
        "randomSeed": None,
        "fitting": None,
        "simulation": None,
        "precision": "exact SymPy source formulas; 50-digit evaluation; binary64 plotting",
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    output_names = [
        "plot.py",
        "validate_data.py",
        "contract.json",
        "figure-contract.md",
        "caption.md",
        "command.txt",
        "data.csv",
        "figure-data-metadata.json",
        "environment.txt",
        "validation.json",
        "figure.pdf",
        "figure.svg",
        "figure.png",
        "qa-original.png",
        "qa-grayscale.png",
    ]
    if independent_path.exists():
        output_names.append("independent-validation.json")
    if qa_report_path.exists():
        output_names.append("qa-report.md")
    output_records = [file_record(HERE / name) for name in output_names]

    formal = manual_qa_passed and independent_passed
    manifest = {
        "schemaVersion": "1.0",
        "release": RELEASE,
        "figureId": FIGURE_ID,
        "status": "formal" if formal else "provisional",
        "createdAt": "2026-08-25T00:00:00+08:00",
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": contract["takeaway"],
        "claimBoundary": contract["claimBoundary"],
        "figure": {
            "widthMillimetres": WIDTH_MM,
            "heightMillimetres": HEIGHT_MM,
            "profile": "journal-default",
            "script": "plot.py",
            "outputs": [
                file_record(HERE / "figure.pdf"),
                file_record(HERE / "figure.svg"),
                {**file_record(HERE / "figure.png"), "dpi": PNG_DPI, "pixels": f"{pixel_dimensions[0]} by {pixel_dimensions[1]}"},
                file_record(HERE / "qa-original.png"),
                file_record(HERE / "qa-grayscale.png"),
            ],
        },
        "data": [file_record(data_path), file_record(HERE / "figure-data-metadata.json")],
        "sourceData": [
            {
                **file_record(data_path),
                "generationCommand": (HERE / "command.txt").read_text(encoding="utf-8").strip(),
                "formulaSource": "figure-contract.md",
            }
        ],
        "computation": {
            "kind": "exact-formula figure",
            "formalCommand": (HERE / "command.txt").read_text(encoding="utf-8").strip(),
            "independentValidationCommand": "PYTHONDONTWRITEBYTECODE=1 tmp/r068b-venv/bin/python figures/r071c-signed-localization/fig-r071c-viscous-sign-creation/validate_data.py",
            "precision": "SymPy exact expressions; 50-digit evaluation; binary64 plotting",
            "solver": "closed Stokes formulas; no PDE time stepping",
            "wallTimeSeconds": round(elapsed, 3),
        },
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
            "pillow": Image.__version__ if hasattr(Image, "__version__") else "unknown",
        },
        "compute": {
            "host": "local Mac workstation",
            "cpu": platform.machine(),
            "logicalCpus": os.cpu_count(),
            "memoryGiB": round(memory_gib, 2) if memory_gib is not None else None,
            "processes": 1,
            "threadsPerProcess": 1,
            "gpu": "not used",
            "dgx": "not used",
        },
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "commit": git_commit,
            "dirtyAtRender": git_dirty,
        },
        "chartContract": {
            "family": "two-panel signed trend and exact ledger decomposition",
            "takeaway": contract["takeaway"],
            "nonColorEncoding": contract["palette"]["nonColorDistinction"],
            "outputFootprint": "double-column 178 by 92 millimetres with PDF, SVG, 600 dpi PNG, and original/grayscale QA images",
        },
        "caption": {"english": "caption.md"},
        "qa": {
            "status": "passed" if formal else "pending-manual-or-independent-inspection",
            "automaticChecks": "validation.json",
            "independentChecks": "independent-validation.json" if independent_path.exists() else None,
            "manualReport": "qa-report.md" if qa_report_path.exists() else None,
            "originalImage": "qa-original.png",
            "grayscaleImage": "qa-grayscale.png",
        },
        "outputs": output_records,
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    checksum_paths = sorted(
        path for path in HERE.iterdir() if path.is_file() and path.name != "SHA256SUMS"
    )
    (HERE / "SHA256SUMS").write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in checksum_paths),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "release": RELEASE,
                "figureId": FIGURE_ID,
                "status": manifest["status"],
                "dataRows": len(rows),
                "checksPassed": sum(bool(value) for value in checks.values()),
                "checksTotal": len(checks),
                "pngPixels": list(pixel_dimensions),
                "wallTimeSeconds": round(elapsed, 3),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
