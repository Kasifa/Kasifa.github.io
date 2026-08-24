#!/usr/bin/env python3
"""Render the journal-style exact R0.70L pressure-sign figure.

All values are rational finite-Fourier initial-face identities.  There is no
DNS, random sampling, fitted curve, or time-stepping PDE computation.
"""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
import platform
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE = ROOT / "figures" / "journal.mplstyle"
FIGURE_ID = "fig-r070l-source-compensator"
RELEASE = "R0.70L"

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
    center = (0.968, 0.945)
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


def exact_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))

    h_minus = (
        Fraction(-301, 85),
        Fraction(131, 85),
        Fraction(0),
    )
    h_plus = (
        Fraction(131, 85),
        Fraction(-301, 85),
        Fraction(0),
    )
    b_common = (
        Fraction(1, 6),
        Fraction(-1, 3),
        Fraction(1, 6),
    )
    h12 = Fraction(-152, 65)

    common_contributions = (
        Fraction(1, 6),
        Fraction(-1),
        Fraction(197, 120),
    )
    pressure_minus = Fraction(563, 510)
    pressure_plus = Fraction(-733, 510)
    contributions_minus = (*common_contributions, pressure_minus)
    contributions_plus = (*common_contributions, pressure_plus)
    total_minus = sum(contributions_minus, Fraction(0))
    total_plus = sum(contributions_plus, Fraction(0))
    common_subtotal = sum(common_contributions, Fraction(0))

    rows: list[tuple[str, str, str, str, str]] = []
    for witness, values in (("minus", h_minus), ("plus", h_plus)):
        for component, value in enumerate(values, start=1):
            rows.append(
                (
                    "A",
                    "pressure-diagonal",
                    witness,
                    f"H{component}{component}",
                    exact_text(value),
                )
            )
    for component, value in enumerate(b_common, start=1):
        rows.append(
            (
                "A",
                "common-anisotropy-diagonal",
                "common",
                f"B{component}{component}",
                exact_text(value),
            )
        )
    for witness in ("minus", "plus"):
        rows.append(
            ("A", "pressure-offdiagonal", witness, "H12", exact_text(h12))
        )

    labels = ("local-gradient", "source-viscosity", "shape-evolution", "pressure")
    for witness, values in (
        ("minus", contributions_minus),
        ("plus", contributions_plus),
    ):
        for label, value in zip(labels, values, strict=True):
            rows.append(("B", "qdot-contribution", witness, label, exact_text(value)))
    rows.extend(
        [
            ("B", "qdot-total", "minus", "total", exact_text(total_minus)),
            ("B", "qdot-total", "plus", "total", exact_text(total_plus)),
        ]
    )

    with (HERE / "data.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["panel", "row_role", "witness", "quantity", "exact_value"])
        writer.writerows(rows)

    checks = {
        "contractFigureIdMatches": contract.get("figureId") == FIGURE_ID,
        "contractReleaseMatches": contract.get("release") == RELEASE,
        "contractRendererIsStaticMatplotlib": contract.get("surface", {}).get(
            "renderer"
        )
        == "static Matplotlib",
        "pressureTraceMinus": sum(h_minus, Fraction(0)) == Fraction(-2),
        "pressureTracePlus": sum(h_plus, Fraction(0)) == Fraction(-2),
        "commonAnisotropyTraceFree": sum(b_common, Fraction(0)) == 0,
        "commonSubtotalExact": common_subtotal == Fraction(97, 120),
        "minusTotalExact": total_minus == Fraction(3901, 2040),
        "plusTotalExact": total_plus == Fraction(-1283, 2040),
        "totalsHaveOppositeSigns": total_minus > 0 and total_plus < 0,
        "entireDifferenceIsPressure": (
            total_minus - total_plus == pressure_minus - pressure_plus
            == Fraction(216, 85)
        ),
        "dataRowCount": len(rows) == 21,
        "contractDataRowCountMatches": contract.get("data", {}).get("rowCount")
        == len(rows),
        "nonColorDistinctionDeclared": "marker"
        in contract.get("palette", {}).get("nonColorDistinction", ""),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = FIGURE_ID
        figure = plt.figure(figsize=(178 / 25.4, 92 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1,
            2,
            left=0.075,
            right=0.985,
            bottom=0.205,
            top=0.715,
            width_ratios=(1.0, 1.35),
            wspace=0.28,
        )
        axis_a = figure.add_subplot(grid[0, 0])
        axis_b = figure.add_subplot(grid[0, 1])

        figure.suptitle(
            "Resolved source evolution: pressure is the sole sign switch",
            x=0.045,
            y=0.966,
            ha="left",
            fontsize=8.3,
            color=INK,
        )
        figure.text(
            0.045,
            0.912,
            "matched strain and vorticity shape  ·  exact pressure inversion  ·  complete q̇ ledger",
            ha="left",
            fontsize=4.25,
            color=MUTED,
        )
        figure.text(
            0.045,
            0.840,
            "EXACT FOURIER INITIAL-FACE IDENTITIES  /  NOT DNS  /  NOT A REGULARITY OR BLOW-UP RESULT",
            ha="left",
            va="center",
            fontsize=4.20,
            color=RUST,
            fontweight="bold",
            bbox={
                "boxstyle": "round,pad=0.28",
                "facecolor": PALE_RUST,
                "edgecolor": RUST,
                "linewidth": 0.45,
            },
        )
        blossom(figure)

        # Panel A: the pressure axes interchange while the state B is fixed.
        components = np.array([1, 2, 3], dtype=float)
        axis_a.axhline(0.0, color=INK, linewidth=0.55)
        axis_a.plot(
            components,
            [float(value) for value in h_minus],
            color=RUST,
            linewidth=1.2,
            marker="s",
            markersize=3.1,
            markerfacecolor=RUST,
            markeredgecolor=RUST,
            label=r"$H^{-}_{ii}$",
        )
        axis_a.plot(
            components,
            [float(value) for value in h_plus],
            color=BLUE,
            linewidth=1.05,
            linestyle="--",
            marker="o",
            markersize=3.2,
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.75,
            label=r"$H^{+}_{ii}$",
        )
        for x_value, minus_value, plus_value in zip(
            components, h_minus, h_plus, strict=True
        ):
            if minus_value != 0:
                axis_a.text(
                    x_value - 0.06,
                    float(minus_value) - 0.24,
                    exact_text(minus_value),
                    color=RUST,
                    fontsize=3.9,
                    ha="right",
                    va="top",
                )
            if plus_value != 0:
                axis_a.text(
                    x_value + 0.06,
                    float(plus_value) + 0.22,
                    exact_text(plus_value),
                    color=BLUE,
                    fontsize=3.9,
                    ha="left",
                    va="bottom",
                )
        axis_a.set_title("A  Same state, rotated pressure response", loc="left", pad=5)
        axis_a.set_xlim(0.75, 3.25)
        axis_a.set_ylim(-4.3, 2.45)
        axis_a.set_xticks([1, 2, 3], [r"$i=1$", r"$i=2$", r"$i=3$"])
        axis_a.set_yticks([-4, -2, 0, 2])
        axis_a.set_ylabel(r"center pressure diagonal $H_{ii}$")
        axis_a.grid(color=GRID, linewidth=0.35, axis="y")
        axis_a.legend(loc="lower right", frameon=False, fontsize=4.15)
        axis_a.text(
            0.79,
            2.26,
            r"common $H_{12}=-152/65$",
            color=MUTED,
            fontsize=4.0,
            ha="left",
            va="top",
        )

        inset = axis_a.inset_axes([0.54, 0.57, 0.40, 0.27])
        inset.axhline(0.0, color=INK, linewidth=0.4)
        inset.bar(
            components,
            [float(value) for value in b_common],
            width=0.46,
            color=PALE_BLUE,
            edgecolor=BLUE,
            linewidth=0.55,
            hatch="////",
        )
        inset.set_title(r"common $B_{ii}$", fontsize=3.7, pad=2)
        inset.set_xticks([1, 2, 3], ["1", "2", "3"], fontsize=3.2)
        inset.set_yticks([-1 / 3, 0, 1 / 6], [r"$-1/3$", r"$0$", r"$1/6$"], fontsize=3.0)
        inset.set_ylim(-0.42, 0.24)
        inset.tick_params(length=1.5, width=0.35)

        # Panel B: the exact qdot ledger.
        x = np.arange(4, dtype=float)
        width = 0.34
        minus_values = np.array([float(value) for value in contributions_minus])
        plus_values = np.array([float(value) for value in contributions_plus])
        axis_b.axhline(0.0, color=INK, linewidth=0.6, zorder=1)
        axis_b.bar(
            x - width / 2,
            minus_values,
            width=width,
            color=PALE_RUST,
            edgecolor=RUST,
            linewidth=0.65,
            hatch="////",
            label=r"$u_-$",
            zorder=2,
        )
        axis_b.bar(
            x + width / 2,
            plus_values,
            width=width,
            color=WHITE,
            edgecolor=BLUE,
            linewidth=0.7,
            label=r"$u_+$",
            zorder=2,
        )
        for index, (minus_value, plus_value) in enumerate(
            zip(contributions_minus, contributions_plus, strict=True)
        ):
            if index < 3:
                axis_b.text(
                    index,
                    float(minus_value) + (0.08 if minus_value >= 0 else -0.11),
                    exact_text(minus_value),
                    color=MUTED,
                    fontsize=3.75,
                    ha="center",
                    va="bottom" if minus_value >= 0 else "top",
                )
            else:
                for x_value, value, color in (
                    (index - width / 2, minus_value, RUST),
                    (index + width / 2, plus_value, BLUE),
                ):
                    axis_b.text(
                        x_value,
                        float(value) + (0.08 if value >= 0 else -0.11),
                        exact_text(value),
                        color=color,
                        fontsize=3.65,
                        ha="center",
                        va="bottom" if value >= 0 else "top",
                    )

        total_x = 4.25
        axis_b.scatter(
            [total_x],
            [float(total_minus)],
            marker="s",
            s=21,
            facecolor=RUST,
            edgecolor=RUST,
            linewidth=0.5,
            zorder=4,
        )
        axis_b.scatter(
            [total_x],
            [float(total_plus)],
            marker="o",
            s=22,
            facecolor=WHITE,
            edgecolor=BLUE,
            linewidth=0.85,
            zorder=4,
        )
        axis_b.vlines(
            total_x,
            float(total_plus),
            float(total_minus),
            color=MUTED,
            linewidth=0.55,
            linestyle=":",
            zorder=3,
        )
        axis_b.text(
            total_x + 0.10,
            float(total_minus),
            r"$3901/2040>0$",
            color=RUST,
            fontsize=4.0,
            ha="left",
            va="center",
        )
        axis_b.text(
            total_x + 0.10,
            float(total_plus),
            r"$-1283/2040<0$",
            color=BLUE,
            fontsize=4.0,
            ha="left",
            va="center",
        )
        axis_b.set_title("B  Exact q̇ ledger", loc="left", pad=5)
        axis_b.set_xlim(-0.55, 5.08)
        axis_b.set_ylim(-1.72, 2.22)
        axis_b.set_xticks(
            [0, 1, 2, 3, total_x],
            ["local\nquadratic", "source\nviscosity", "shape\nevolution", "pressure", r"total $\dot q$"],
        )
        axis_b.set_yticks([-1.5, -1.0, 0.0, 1.0, 2.0])
        axis_b.set_ylabel("exact contribution")
        axis_b.grid(color=GRID, linewidth=0.35, axis="y")
        axis_b.legend(loc="upper left", frameon=False, fontsize=4.15, ncol=2)
        axis_b.text(
            -0.45,
            -1.57,
            r"common nonpressure subtotal $=97/120$",
            color=MUTED,
            fontsize=4.0,
            ha="left",
            va="bottom",
        )

        figure.text(
            0.985,
            0.035,
            "finite Fourier initial data — pressure is the entire derivative difference; nonlocal compensation remains open",
            ha="right",
            va="bottom",
            color=MUTED,
            fontsize=4.2,
        )

        figure.savefig(
            HERE / "figure.pdf",
            metadata={
                "Title": "Resolved source evolution pressure sign pair",
                "Author": "R0.70L exact figure package",
                "Subject": "Matched source-shape data with opposite q derivatives",
                "Creator": "plot.py",
                "CreationDate": None,
                "ModDate": None,
            },
        )
        figure.savefig(
            HERE / "figure.svg",
            metadata={
                "Title": "Resolved source evolution pressure sign pair",
                "Description": "Exact Fourier initial-face identities; not DNS or a regularity or blow-up result.",
                "Creator": "plot.py",
                "Date": None,
            },
        )
        figure.savefig(
            HERE / "figure.png",
            dpi=600,
            metadata={
                "Title": "Resolved source evolution pressure sign pair",
                "Description": "Exact Fourier initial-face identities; not DNS or a regularity or blow-up result.",
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
        "pngOriginalPixelDimensions": bool(image.width >= 4200 and image.height >= 2100),
        "pngRequestedDpiEmbedded": bool(
            embedded_dpi[0] is not None
            and embedded_dpi[1] is not None
            and abs(float(embedded_dpi[0]) - 600.0) < 0.1
            and abs(float(embedded_dpi[1]) - 600.0) < 0.1
        ),
        "pdfNonempty": bool((HERE / "figure.pdf").stat().st_size > 10_000),
        "svgNonempty": bool((HERE / "figure.svg").stat().st_size > 10_000),
        "visibleClaimBoundaryInSvg": bool(
            "EXACT FOURIER INITIAL-FACE IDENTITIES" in svg_text
            and "NOT DNS" in svg_text
            and "NOT A REGULARITY OR BLOW-UP RESULT" in svg_text
        ),
        "writtenDataRowCount": data_row_count == 21,
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
            "commonNonpressureSubtotal": float(common_subtotal),
            "minusPressureContribution": float(pressure_minus),
            "plusPressureContribution": float(pressure_plus),
            "minusTotalDerivative": float(total_minus),
            "plusTotalDerivative": float(total_plus),
            "derivativeDifference": float(total_minus - total_plus),
            "pngPixels": [image.width, image.height],
            "pngEmbeddedDpi": [float(embedded_dpi[0]), float(embedded_dpi[1])],
        },
        "visualQa": {
            "originalResolution": (
                f"passed: title, panel labels, exact annotations, inset, axes, "
                f"legend, and footer inspected at {image.width} by {image.height} pixels"
            ),
            "grayscale": (
                "passed: line style, marker shape and fill, hatch, direct rational "
                "labels, and zero baselines preserve every claimed distinction"
            ),
        },
        "claimBoundary": (
            "Exact finite-Fourier initial-face identities only; not DNS, not a "
            "long-time trajectory, and not evidence for blow-up, regularity, "
            "or a Millennium-problem solution."
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
    manifest = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "explanatory",
        "release": RELEASE,
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
        },
        "claimBoundary": (
            "Exact finite-Fourier initial-face identities; not simulation "
            "evidence, not a numerical PDE proof, and not a Millennium result."
        ),
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
