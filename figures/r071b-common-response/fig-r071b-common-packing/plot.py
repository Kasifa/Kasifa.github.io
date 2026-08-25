#!/usr/bin/env python3
"""Build the formal R0.71B common-response packing figure.

All plotted values are evaluations of closed exact formulas.  There is no
random sampling, fitting, DNS, or PDE time stepping.  SymPy keeps the source
formula exact; IEEE binary64 conversion is used only at the plotting boundary.
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
import sys
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
SOURCE_RESULT = ROOT / "research" / "certificates" / "r071b" / "result.json"
FIGURE_ID = "fig-r071b-common-packing"
RELEASE = "R0.71B"
WIDTH_MM = 178
HEIGHT_MM = 136
PNG_DPI = 600

INK = "#28231f"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#985943"
PALE_BLUE = "#e7eef2"
PALE_RUST = "#f2e5df"
GRID = "#d5cec0"
WHITE = "#ffffff"

M_VALUES = tuple(2**power for power in range(2, 17))
N_VALUES = (1, 2, 4, 8, 16, 32, 64)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_float(value: sp.Expr) -> float:
    """Convert an exact expression to binary64 only after 50-digit evaluation."""

    return float(sp.N(value, 50))


def common_response(m_value: int | sp.Symbol) -> sp.Expr:
    radius_square = 2 * m_value**2 + 2 * m_value + 1
    return (
        sp.sqrt(2)
        * m_value
        * (m_value + 1)
        * (2 * m_value + 1)
        / radius_square ** sp.Rational(3, 2)
    )


def chord_response(m_value: int | sp.Symbol) -> sp.Expr:
    radius_square = 2 * m_value**2 + 2 * m_value + 1
    return (
        -sp.sqrt(2)
        * (2 * m_value + 1)
        / (2 * radius_square ** sp.Rational(3, 2))
    )


def same_low_values(count: int) -> tuple[sp.Expr, sp.Expr]:
    terms = [common_response(8**index) for index in range(1, count + 1)]
    total = sp.Add(*terms, evaluate=False) / (4 * count)
    shell_l2 = sp.sqrt(sp.Add(*(term**2 for term in terms), evaluate=False)) / (
        4 * count
    )
    return total, shell_l2


def shared_high_ratio(count: int) -> sp.Expr:
    terms = [
        sp.Rational(16**index, 1) / sp.sqrt(1 + 16 ** (2 * index))
        for index in range(1, count + 1)
    ]
    return sp.Add(*terms, evaluate=False) / (4 * sp.sqrt(count))


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

    center = (0.970, 0.958)
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
    source_result = json.loads(SOURCE_RESULT.read_text(encoding="utf-8"))

    m_symbol = sp.symbols("M", positive=True)
    common_symbol = common_response(m_symbol)
    scaled_chord_symbol = -m_symbol**2 * chord_response(m_symbol)

    common_values = [exact_float(common_response(value)) for value in M_VALUES]
    scaled_chord_values = [
        exact_float(-value**2 * chord_response(value)) for value in M_VALUES
    ]

    same_low_total: list[float] = []
    same_low_l2: list[float] = []
    for count in N_VALUES:
        total, shell_l2 = same_low_values(count)
        same_low_total.append(exact_float(total))
        same_low_l2.append(exact_float(shell_l2))

    shared_ratio = [exact_float(shared_high_ratio(count)) for count in N_VALUES]
    root_tent_norm = [math.sqrt(count / 2) for count in N_VALUES]

    positive_work = 3 * sp.sqrt(2) / 40
    negative_work = -positive_work
    positive_square = sp.Rational(9, 800)
    normalized_positive = sp.Rational(3, 39940400)

    rows: list[list[str]] = []

    def add_row(
        panel: str,
        row_role: str,
        series: str,
        index: int,
        x_exact: str,
        x_numeric: float,
        y_exact: str,
        y_numeric: float,
        context: str,
    ) -> None:
        rows.append(
            [
                panel,
                row_role,
                series,
                str(index),
                x_exact,
                f"{x_numeric:.17g}",
                y_exact,
                f"{y_numeric:.17g}",
                context,
            ]
        )

    for index, (m_value, common_value, chord_value) in enumerate(
        zip(M_VALUES, common_values, scaled_chord_values)
    ):
        add_row(
            "A",
            "exact-curve",
            "common response U_M",
            index,
            str(m_value),
            float(m_value),
            "sqrt(2)*M*(M+1)*(2*M+1)/(2*M^2+2*M+1)^(3/2)",
            common_value,
            f"M={m_value}; exact two-shell HHL formula",
        )
        add_row(
            "A",
            "exact-curve",
            "scaled chord M^2 |C_M|",
            index,
            str(m_value),
            float(m_value),
            "sqrt(2)*M^2*(2*M+1)/(2*(2*M^2+2*M+1)^(3/2))",
            chord_value,
            f"M={m_value}; chord shown after exact M^2 scaling",
        )
        add_row(
            "A",
            "asymptotic-reference",
            "common limit",
            index,
            str(m_value),
            float(m_value),
            "1",
            1.0,
            "lim_(M->infinity) U_M=1",
        )
        add_row(
            "A",
            "asymptotic-reference",
            "scaled chord limit",
            index,
            str(m_value),
            float(m_value),
            "1/2",
            0.5,
            "lim_(M->infinity) M^2|C_M|=1/2",
        )

    for index, (count, total, shell_l2) in enumerate(
        zip(N_VALUES, same_low_total, same_low_l2)
    ):
        total_formula = (
            "sum_(j=1)^N U_(8^j)/(4*N), "
            "U_M=sqrt(2)*M*(M+1)*(2*M+1)/(2*M^2+2*M+1)^(3/2)"
        )
        l2_formula = (
            "sqrt(sum_(j=1)^N U_(8^j)^2)/(4*N), "
            "U_M=sqrt(2)*M*(M+1)*(2*M+1)/(2*M^2+2*M+1)^(3/2)"
        )
        add_row(
            "B",
            "exact-curve",
            "total common work",
            index,
            str(count),
            float(count),
            total_formula,
            total,
            f"N={count}; M_j=8^j",
        )
        add_row(
            "B",
            "exact-curve",
            "shell-work l2",
            index,
            str(count),
            float(count),
            l2_formula,
            shell_l2,
            f"N={count}; M_j=8^j",
        )
        add_row(
            "B",
            "asymptotic-reference",
            "total limit",
            index,
            str(count),
            float(count),
            "1/4",
            0.25,
            "lim_(N->infinity) total common work=1/4",
        )
        add_row(
            "B",
            "asymptotic-reference",
            "shell l2 asymptotic",
            index,
            str(count),
            float(count),
            "1/(4*sqrt(N))",
            1 / (4 * math.sqrt(count)),
            "shell-work l2 is asymptotic to 1/(4*sqrt(N))",
        )

    for index, (count, ratio, tent_norm) in enumerate(
        zip(N_VALUES, shared_ratio, root_tent_norm)
    ):
        add_row(
            "C",
            "exact-curve",
            "normalized polarized operator ratio",
            index,
            str(count),
            float(count),
            "sum_(j=1)^N 16^j/sqrt(1+16^(2*j))/(4*sqrt(N))",
            ratio,
            f"N={count}; M_j=16^j; equal high radii",
        )
        add_row(
            "C",
            "exact-curve",
            "root tent norm",
            index,
            str(count),
            float(count),
            "sqrt(N/2)",
            tent_norm,
            "exact root-tent square mass N/2",
        )
        add_row(
            "C",
            "exact-reference",
            "frame shell supremum upper bound",
            index,
            str(count),
            float(count),
            "1",
            1.0,
            "strict support separation gives shell supremum <=1",
        )

    for index, (label, signed_value, square_value, coefficient) in enumerate(
        (
            ("positive field", positive_work, positive_square, normalized_positive),
            ("negative field", negative_work, sp.Integer(0), sp.Integer(0)),
        )
    ):
        add_row(
            "D",
            "signed-bar",
            "signed output work",
            index,
            str(index),
            float(index),
            str(signed_value),
            exact_float(signed_value),
            f"{label}; sole output k=(1,0,1)",
        )
        add_row(
            "D",
            "annotation",
            "positive-output square",
            index,
            str(index),
            float(index),
            str(square_value),
            exact_float(square_value),
            f"{label}; T_+^2",
        )
        add_row(
            "D",
            "annotation",
            "normalized positive coefficient",
            index,
            str(index),
            float(index),
            str(coefficient),
            exact_float(coefficient),
            f"{label}; a_+=T_+^2/||omega||_2^2",
        )

    data_path = HERE / "data.csv"
    with data_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(
            [
                "panel",
                "row_role",
                "series",
                "index",
                "x_exact",
                "x_numeric",
                "y_exact",
                "y_numeric",
                "context",
            ]
        )
        writer.writerows(rows)

    source_same_low = {
        int(record["N"]): record
        for record in source_result["sameLowFanLedger"]["sequence"]
    }
    source_shared = {
        int(record["N"]): record
        for record in source_result["sharedHighFanLedger"]["sequence"]
    }
    source_positive = source_result["positiveOutputLedger"]["r071aPositive"]
    source_negative = source_result["positiveOutputLedger"]["r071aNegative"]

    checks: dict[str, bool] = {
        "contractFigureIdMatches": contract.get("figureId") == FIGURE_ID,
        "contractReleaseMatches": contract.get("release") == RELEASE,
        "contractRendererIsStaticMatplotlib": contract.get("surface", {}).get(
            "renderer"
        )
        == "static Matplotlib",
        "contractDataRowCountMatches": contract.get("data", {}).get("rowCount")
        == len(rows),
        "sourceReleaseMatches": source_result.get("release") == RELEASE,
        "sourceStatusMatches": source_result.get("status")
        == "common-response-packing-and-positive-output-gate",
        "twoShellCommonLimitExact": sp.limit(common_symbol, m_symbol, sp.oo) == 1,
        "twoShellScaledChordLimitExact": sp.limit(
            scaled_chord_symbol, m_symbol, sp.oo
        )
        == sp.Rational(1, 2),
        "twoShellSampleMonotone": all(
            later > earlier for earlier, later in zip(common_values, common_values[1:])
        )
        and all(
            later > earlier
            for earlier, later in zip(scaled_chord_values, scaled_chord_values[1:])
        ),
        "sameLowTotalApproachesQuarter": abs(same_low_total[-1] - 0.25) < 4e-5,
        "sameLowL2HasRootNScale": abs(
            same_low_l2[-1] * math.sqrt(N_VALUES[-1]) - 0.25
        )
        < 4e-5,
        "sharedRatioHasRootNScale": abs(
            shared_ratio[-1] / math.sqrt(N_VALUES[-1]) - 0.25
        )
        < 4e-5,
        "rootTentSquareMassExact": all(
            abs(value**2 - count / 2) < 1e-14
            for count, value in zip(N_VALUES, root_tent_norm)
        ),
        "positiveOutputPairIsOpposite": sp.simplify(
            positive_work + negative_work
        )
        == 0,
        "positiveSquareExact": positive_square == sp.Rational(9, 800),
        "negativePositiveSquareZero": source_negative["positiveSquare"] == "0",
        "normalizedPositiveExact": normalized_positive
        == sp.Rational(3, 39940400),
        "sourcePositiveWorkMatches": sp.sympify(
            source_positive["signedOutputs"][0]["work"]
        )
        == positive_work,
        "sourceNegativeWorkMatches": sp.sympify(
            source_negative["signedOutputs"][0]["work"]
        )
        == negative_work,
        "sourcePositiveSquareMatches": sp.sympify(source_positive["positiveSquare"])
        == positive_square,
        "sourceNormalizedPositiveMatches": sp.sympify(
            source_positive["normalizedCoefficient"]
        )
        == normalized_positive,
        "sourceSameLowSequenceMatches": all(
            math.isclose(
                same_low_total[N_VALUES.index(count)],
                source_same_low[count]["totalCommonWorkFloat"],
                rel_tol=0,
                abs_tol=2e-15,
            )
            and math.isclose(
                same_low_l2[N_VALUES.index(count)],
                source_same_low[count]["shellWorkL2Float"],
                rel_tol=0,
                abs_tol=2e-15,
            )
            for count in (1, 2, 4, 8)
        ),
        "sourceSharedSequenceMatches": all(
            math.isclose(
                shared_ratio[N_VALUES.index(count)],
                source_shared[count]["normalizedOperatorRatioFloat"],
                rel_tol=0,
                abs_tol=2e-15,
            )
            and math.isclose(
                root_tent_norm[N_VALUES.index(count)],
                source_shared[count]["rootTentNormLower"],
                rel_tol=0,
                abs_tol=2e-15,
            )
            for count in (1, 2, 4, 8)
        ),
        "writtenDataRowCount": len(rows) == 115,
        "noRandomnessUsed": True,
        "nonColorDistinctionDeclared": "line style"
        in contract.get("palette", {}).get("nonColorDistinction", ""),
    }
    if not all(checks.values()):
        raise AssertionError(
            {name: passed for name, passed in checks.items() if not passed}
        )

    x_m = np.asarray(M_VALUES, dtype=float)
    x_n = np.asarray(N_VALUES, dtype=float)

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = FIGURE_ID
        figure = plt.figure(
            figsize=(WIDTH_MM / 25.4, HEIGHT_MM / 25.4), layout="none"
        )
        grid = figure.add_gridspec(
            2,
            2,
            left=0.095,
            right=0.982,
            bottom=0.155,
            top=0.792,
            hspace=0.55,
            wspace=0.30,
        )
        axis_a = figure.add_subplot(grid[0, 0])
        axis_b = figure.add_subplot(grid[0, 1])
        axis_c = figure.add_subplot(grid[1, 0])
        axis_d = figure.add_subplot(grid[1, 1])

        figure.suptitle(
            "Common-response packing and signed output",
            x=0.042,
            y=0.969,
            ha="left",
            fontsize=8.5,
            color=INK,
        )
        figure.text(
            0.042,
            0.929,
            "closed exact formulas  ·  lacunary finite-mode families  ·  R0.71A sign pair",
            ha="left",
            fontsize=4.35,
            color=MUTED,
        )
        figure.text(
            0.042,
            0.875,
            "FINITE-MODE PACKING OBSTRUCTIONS + ONE CONDITIONAL CONSUMER  /  NOT A CONTINUATION OR REGULARITY RESULT",
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

        # A: both quantities have honest dimensionless scaling on one axis.
        axis_a.set_xscale("log", base=2)
        axis_a.plot(
            x_m,
            common_values,
            color=BLUE,
            linestyle="-",
            marker="o",
            markersize=2.7,
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.65,
            label=r"common  $\mathcal{U}_M$",
        )
        axis_a.plot(
            x_m,
            scaled_chord_values,
            color=RUST,
            linestyle="--",
            marker="^",
            markersize=2.7,
            markerfacecolor=RUST,
            markeredgecolor=RUST,
            label=r"scaled chord  $M^2|\mathcal{C}_M|$",
        )
        axis_a.axhline(1.0, color=INK, linewidth=0.65, linestyle=":")
        axis_a.axhline(0.5, color=MUTED, linewidth=0.65, linestyle=":")
        axis_a.set_title("A  Two-shell response channels", loc="left", pad=5)
        axis_a.set_xlim(M_VALUES[0], M_VALUES[-1])
        axis_a.set_ylim(0.34, 1.045)
        axis_a.set_xticks(
            [4, 16, 256, 4096, 65536], ["4", "16", "256", "4096", "65536"]
        )
        axis_a.set_yticks([0.4, 0.5, 0.6, 0.8, 1.0])
        axis_a.set_xlabel(r"separation parameter  $M$  (log$_2$)")
        axis_a.set_ylabel("dimensionless response")
        axis_a.grid(color=GRID, linewidth=0.35, axis="y")
        axis_a.legend(loc="lower right", frameon=False, fontsize=3.65)
        axis_a.text(
            0.03,
            0.60,
            r"$\mathcal{U}_M\to1$;  $M^2\mathcal{C}_M\to-1/2$",
            transform=axis_a.transAxes,
            ha="left",
            va="top",
            fontsize=3.65,
            color=INK,
        )

        # B: exact finite-N evaluations and their closed asymptotic references.
        axis_b.set_xscale("log", base=2)
        axis_b.set_yscale("log", base=2)
        axis_b.plot(
            x_n,
            same_low_total,
            color=BLUE,
            linestyle="-",
            marker="o",
            markersize=2.9,
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.65,
            label=r"total common work  $W_N$",
        )
        axis_b.plot(
            x_n,
            same_low_l2,
            color=RUST,
            linestyle="--",
            marker="^",
            markersize=2.8,
            markerfacecolor=RUST,
            markeredgecolor=RUST,
            label=r"shell work  $\ell^2$",
        )
        axis_b.plot(
            x_n,
            np.full_like(x_n, 0.25),
            color=INK,
            linestyle=":",
            linewidth=0.65,
            label=r"reference  $1/4$",
        )
        axis_b.plot(
            x_n,
            1 / (4 * np.sqrt(x_n)),
            color=MUTED,
            linestyle="-.",
            linewidth=0.7,
            label=r"reference  $1/(4\sqrt{N})$",
        )
        axis_b.set_title("B  Same-low fan: total versus shell packing", loc="left", pad=5)
        axis_b.set_xlim(1, 64)
        axis_b.set_ylim(0.026, 0.285)
        axis_b.set_xticks(N_VALUES, [str(value) for value in N_VALUES])
        axis_b.set_yticks(
            [0.03125, 0.0625, 0.125, 0.25],
            ["0.031", "0.063", "0.125", "0.250"],
        )
        axis_b.set_xlabel(r"fan size  $N$  (log$_2$)")
        axis_b.set_ylabel("work magnitude  (log$_2$)")
        axis_b.grid(color=GRID, linewidth=0.35, axis="y")
        axis_b.legend(loc="lower left", frameon=False, fontsize=3.25, ncol=2)

        # C: the divergent operator ratio tracks square packing, not shell sup.
        axis_c.set_xscale("log", base=2)
        axis_c.set_yscale("log", base=2)
        axis_c.plot(
            x_n,
            shared_ratio,
            color=BLUE,
            linestyle="-",
            marker="o",
            markersize=2.9,
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.65,
            label=r"operator ratio  $\rho_N$",
        )
        axis_c.plot(
            x_n,
            root_tent_norm,
            color=RUST,
            linestyle="--",
            marker="^",
            markersize=2.8,
            markerfacecolor=RUST,
            markeredgecolor=RUST,
            label=r"root tent norm  $\sqrt{N/2}$",
        )
        axis_c.axhline(
            1.0,
            color=INK,
            linewidth=0.7,
            linestyle=":",
            label="shell-sup upper bound  1",
        )
        axis_c.set_title("C  Shared-high equal-radius fan", loc="left", pad=5)
        axis_c.set_xlim(1, 64)
        axis_c.set_ylim(0.20, 7.3)
        axis_c.set_xticks(N_VALUES, [str(value) for value in N_VALUES])
        axis_c.set_yticks(
            [0.25, 0.5, 1, 2, 4], ["0.25", "0.5", "1", "2", "4"]
        )
        axis_c.set_xlabel(r"fan size  $N$  (log$_2$)")
        axis_c.set_ylabel("normalized magnitude  (log$_2$)")
        axis_c.grid(color=GRID, linewidth=0.35, axis="y")
        axis_c.legend(loc="upper left", frameon=False, fontsize=3.45)
        axis_c.text(
            0.98,
            0.05,
            r"$\rho_N\sim\sqrt{N}/4$",
            transform=axis_c.transAxes,
            ha="right",
            va="bottom",
            fontsize=3.75,
            color=INK,
        )

        # D: signed bars show the sign pair; T_+^2 is carried by direct labels.
        bar_values = [exact_float(positive_work), exact_float(negative_work)]
        bars = axis_d.bar(
            [0, 1],
            bar_values,
            width=0.48,
            color=[PALE_BLUE, PALE_RUST],
            edgecolor=[BLUE, RUST],
            linewidth=0.8,
        )
        bars[1].set_hatch("///")
        axis_d.axhline(0, color=INK, linewidth=0.75)
        axis_d.set_title("D  R0.71A sign-pair output", loc="left", pad=5)
        axis_d.set_xlim(-0.55, 1.55)
        axis_d.set_ylim(-0.145, 0.145)
        axis_d.set_xticks(
            [0, 1],
            [
                "positive field\n$\\mathcal{T}_+^2=9/800$",
                "negative field\n$\\mathcal{T}_+^2=0$",
            ],
        )
        axis_d.set_ylabel(r"signed output  $w_{(1,0,1)}$")
        axis_d.grid(color=GRID, linewidth=0.35, axis="y")
        axis_d.text(
            0,
            bar_values[0] + 0.008,
            r"$+3\sqrt{2}/40$",
            ha="center",
            va="bottom",
            fontsize=3.9,
            color=BLUE,
        )
        axis_d.text(
            1,
            bar_values[1] - 0.008,
            r"$-3\sqrt{2}/40$",
            ha="center",
            va="top",
            fontsize=3.9,
            color=RUST,
        )
        axis_d.text(
            0.98,
            0.96,
            r"positive:  $a_+=3/39940400$" + "\n" + r"negative:  $a_+=0$",
            transform=axis_d.transAxes,
            ha="right",
            va="top",
            fontsize=3.45,
            color=INK,
        )

        figure.text(
            0.042,
            0.082,
            "A-C use arbitrary-N closed families; the producer exhaustively audits resonance support at N=8.  D is the exact one-output R0.71A pair.",
            ha="left",
            fontsize=3.7,
            color=MUTED,
        )
        figure.text(
            0.042,
            0.040,
            "Scope: two packing no-go examples and an exact Cauchy-Young consumer coefficient; no Navier-Stokes propagation bound is proved.",
            ha="left",
            fontsize=3.75,
            color=INK,
        )

        pdf_metadata = {
            "Title": "R0.71B common-response packing and signed output",
            "Author": "Chuikuan Zeng",
            "Subject": "Exact finite-mode response and packing diagnostics",
            "Keywords": "Navier-Stokes; Fourier; Carleson packing; exact audit",
            "Creator": "Matplotlib reproducible figure script",
            "CreationDate": datetime(2026, 8, 25, tzinfo=timezone.utc),
            "ModDate": datetime(2026, 8, 25, tzinfo=timezone.utc),
        }
        svg_metadata = {
            "Title": "R0.71B common-response packing and signed output",
            "Description": "Four exact finite-mode comparisons with a visible claim boundary.",
            "Creator": "Matplotlib reproducible figure script",
            "Date": "2026-08-25",
        }
        png_metadata = {
            "Title": "R0.71B common-response packing and signed output",
            "Author": "Chuikuan Zeng",
            "Description": "Exact formula evaluations; no simulation or fitted data.",
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
        "pngHeightMatches136mmAt600dpi": pixel_dimensions[1]
        in {
            round(HEIGHT_MM / 25.4 * PNG_DPI),
            math.floor(HEIGHT_MM / 25.4 * PNG_DPI),
        },
        "pngEmbeddedDpiNear600": all(
            abs(float(value) - PNG_DPI) < 0.02 for value in embedded_dpi
        ),
        "qaOriginalMatchesFigure": sha256(HERE / "qa-original.png")
        == sha256(HERE / "figure.png"),
        "qaGrayscaleDimensionsMatch": grayscale_dimensions == pixel_dimensions,
        "qaGrayscaleIsRgbGray": grayscale_is_rgb_gray,
        "visibleClaimBoundaryInSvg": "NOT A CONTINUATION OR REGULARITY RESULT"
        in svg_text,
        "visiblePanelLabelsInSvg": all(
            label in svg_text
            for label in (
                "A  Two-shell response channels",
                "B  Same-low fan: total versus shell packing",
                "C  Shared-high equal-radius fan",
                "D  R0.71A sign-pair output",
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

    qa_report_path = HERE / "qa-report.md"
    manual_qa_passed = qa_report_path.exists() and "Status: passed" in qa_report_path.read_text(
        encoding="utf-8"
    )
    elapsed = time.perf_counter() - started

    validation = {
        "release": RELEASE,
        "status": "passed" if manual_qa_passed else "automatic-passed-manual-pending",
        "checks": checks,
        "diagnostics": {
            "dataRows": len(rows),
            "MRange": [M_VALUES[0], M_VALUES[-1]],
            "NValues": list(N_VALUES),
            "commonAtM4": common_values[0],
            "scaledChordAtM4": scaled_chord_values[0],
            "sameLowTotalAtN64": same_low_total[-1],
            "sameLowShellL2AtN64": same_low_l2[-1],
            "sharedRatioAtN64": shared_ratio[-1],
            "rootTentNormAtN64": root_tent_norm[-1],
            "positiveWork": exact_float(positive_work),
            "positiveSquare": exact_float(positive_square),
            "normalizedPositive": exact_float(normalized_positive),
            "pngPixels": list(pixel_dimensions),
            "pngEmbeddedDpi": [float(value) for value in embedded_dpi],
            "wallTimeSeconds": round(elapsed, 3),
        },
        "claimBoundary": "Exact finite-mode formulas show two direct packing failures and a sign-sensitive positive-output coefficient. They do not prove time integrability, a continuation theorem, a singularity, global regularity, or a Millennium-problem solution.",
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
    environment_text = (
        "# R0.71B figure environment\n\n"
        f"- Release: {RELEASE}\n"
        f"- Figure: {FIGURE_ID}\n"
        f"- Git core commit: {git_commit}\n"
        f"- Git worktree dirty at render: {str(git_dirty).lower()}\n"
        f"- Host: local Mac workstation ({platform.machine()})\n"
        f"- Operating system: {platform.platform()}\n"
        f"- Logical CPUs visible: {os.cpu_count()}\n"
        f"- Physical memory GiB: {memory_gib:.2f}\n"
        if memory_gib is not None
        else "- Physical memory GiB: unavailable\n"
    )
    environment_text += (
        "- Processes: 1\n"
        "- Threads per process: 1\n"
        "- GPU: not used\n"
        "- DGX: not used\n"
        "- Random seed: none; no random operation is present\n"
        "- Solver: closed formulas and exact identities; no PDE time stepping\n"
        "- Precision: SymPy exact expressions; 50-digit evaluation followed by binary64 plotting\n"
        f"- Python: {platform.python_version()}\n"
        f"- SymPy: {sp.__version__}\n"
        f"- NumPy: {np.__version__}\n"
        f"- Matplotlib: {matplotlib.__version__}\n"
        f"- Pillow: {Image.__version__ if hasattr(Image, '__version__') else 'unknown'}\n"
        f"- Wall time seconds: {elapsed:.3f}\n"
    )
    (HERE / "environment.txt").write_text(environment_text, encoding="utf-8")

    metadata = {
        "schemaVersion": "1.0",
        "release": RELEASE,
        "figureId": FIGURE_ID,
        "dataPath": "data.csv",
        "rowCount": len(rows),
        "grain": "15 exact M evaluations for each two-shell series; seven dyadic fan sizes for each packing series; and the two exact R0.71A sign states",
        "formulaSource": "closed formulas stated in research/r071b_report-source.md and certified by research/certificates/r071b/result.json",
        "sourceResult": {
            "path": str(SOURCE_RESULT.relative_to(ROOT)),
            "sha256": sha256(SOURCE_RESULT),
        },
        "transformations": [
            "Panel A displays the exact chord magnitude after multiplication by M^2 so its nonzero asymptotic coefficient shares an honest dimensionless axis with the common response.",
            "Panel B evaluates exact finite sums at N=1,2,4,8,16,32,64 and overlays the proved asymptotic references 1/4 and 1/(4 sqrt(N)).",
            "Panel C evaluates the exact equal-radius fan ratio and the exact root-tent norm sqrt(N/2).",
            "Panel D plots the sole signed output; T_+^2 and a_+ are direct exact annotations and are retained as separate CSV rows.",
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
    if qa_report_path.exists():
        output_names.append("qa-report.md")
    output_records = [file_record(HERE / name) for name in output_names]

    manifest = {
        "schemaVersion": "1.0",
        "release": RELEASE,
        "figureId": FIGURE_ID,
        "status": "formal" if manual_qa_passed else "provisional",
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
                "path": str(SOURCE_RESULT.relative_to(ROOT)),
                "sha256": sha256(SOURCE_RESULT),
                "extractionCommand": "PYTHONDONTWRITEBYTECODE=1 tmp/r068b-venv/bin/python research/r071b_exact_audit.py --output research/certificates/r071b/result.json",
            }
        ],
        "computation": {
            "kind": "exact-formula figure",
            "formalCommand": (HERE / "command.txt").read_text(encoding="utf-8").strip(),
            "precision": "SymPy exact expressions; 50-digit evaluation; binary64 plotting",
            "solver": "closed formulas and finite sums; no PDE time stepping",
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
            "family": "four-panel exact asymptotic comparison and signed bar",
            "takeaway": contract["takeaway"],
            "nonColorEncoding": contract["palette"]["nonColorDistinction"],
            "outputFootprint": "double-column 178 by 136 millimetres with PDF, SVG, 600 dpi PNG, and original/grayscale QA images",
        },
        "caption": {"english": "caption.md"},
        "qa": {
            "status": "passed" if manual_qa_passed else "pending-manual-inspection",
            "automaticChecks": "validation.json",
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
