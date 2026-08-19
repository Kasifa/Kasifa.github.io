#!/usr/bin/env python3
"""Render the R0.35 continuation-distance and radius-loss figure."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
STYLE = PACKAGE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
GOLD = "#a16f27"
PALE_BLUE = "#dce6ec"
GRID = "#d5cec0"


def normalize_svg(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(
        "\n".join(line.rstrip() for line in lines) + "\n",
        encoding="utf-8",
    )


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def draw() -> None:
    geometry = {record["metric"]: record for record in rows("geometry.csv")}
    witnesses = rows("operator-witness.csv")
    constants = {record["name"]: record for record in rows("operator-constants.csv")}

    rho = float(geometry["r031_bivariate_radius"]["decimal_lower"])
    r_radius = float(geometry["r031_fixed_charge_radius"]["decimal_lower"])
    candidate_r_lower = float(geometry["r032_candidate_abs_R"]["decimal_lower"])
    candidate_r_upper = float(geometry["r032_candidate_abs_R"]["decimal_upper"])
    candidate_b_lower = float(
        geometry["r032_candidate_balanced_radius"]["decimal_lower"]
    )
    candidate_b_upper = float(
        geometry["r032_candidate_balanced_radius"]["decimal_upper"]
    )
    radius_ratio_lower = float(geometry["balanced_radius_ratio"]["decimal_lower"])
    radius_ratio_upper = float(geometry["balanced_radius_ratio"]["decimal_upper"])
    ns = np.array([int(record["N"]) for record in witnesses])
    same_radius = np.array(
        [float(record["same_radius_decimal"]) for record in witnesses]
    )
    half_bound = float(constants["half_radius_bilinear_bound"]["decimal"])

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        figure, (left, right) = plt.subplots(
            1,
            2,
            figsize=(178 / 25.4, 84 / 25.4),
            gridspec_kw={"width_ratios": (1.02, 0.98)},
            layout="none",
        )

        left.set_title("(a) Fixed-charge contour geometry", loc="left", pad=5)
        r_values = np.geomspace(r_radius / 2, 1.0, 500)
        balanced = np.cbrt(r_values)
        left.loglog(r_values, balanced, color=BLUE, label=r"required $|R|^{1/3}$")
        left.fill_between(
            [candidate_r_lower, candidate_r_upper],
            [candidate_b_lower, candidate_b_lower],
            [candidate_b_upper, candidate_b_upper],
            color=GOLD,
            alpha=0.7,
            linewidth=0,
            label="R0.32 finite candidate hull",
        )
        left.scatter(
            [r_radius],
            [rho],
            s=27,
            facecolor="white",
            edgecolor=INK,
            marker="o",
            linewidth=0.8,
            zorder=5,
            label="R0.31 certified boundary",
        )
        left.axhline(rho, color=INK, linestyle=(0, (4, 2)), linewidth=0.8)
        left.annotate(
            rf"candidate needs $>{radius_ratio_lower:.3f}\,\rho$",
            xy=(candidate_r_lower, candidate_b_lower),
            xytext=(0.014, 0.43),
            arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.7},
            color=MUTED,
            fontsize=6.3,
        )
        left.text(
            r_radius * 1.25,
            rho * 0.87,
            "certified radius = 4/81",
            color=INK,
            fontsize=6.2,
            va="top",
        )
        left.set_xlabel(r"fixed-charge modulus $|R|$")
        left.set_ylabel("minimum balanced bivariate radius")
        left.set_xlim(r_radius / 2, 1.12)
        left.set_ylim(rho / 1.6, 1.12)
        left.grid(which="major", color=GRID, linewidth=0.42)
        left.grid(which="minor", color=GRID, linewidth=0.25, alpha=0.45)
        left.legend(loc="upper left", bbox_to_anchor=(0.0, 0.94))

        right.set_title("(b) Same-radius obstruction", loc="left", pad=5)
        right.plot(
            ns,
            same_radius,
            color=GOLD,
            label=r"same-radius $\|\Phi(f_N)\|_\rho$",
        )
        right.axhline(
            half_bound,
            color=BLUE,
            linestyle=(0, (5, 2)),
            linewidth=1.15,
            label=r"outer$\to$half-radius bound $121/48$",
        )
        right.fill_between(
            ns,
            0,
            half_bound,
            color=PALE_BLUE,
            alpha=0.55,
            linewidth=0,
        )
        right.scatter(
            [128],
            [same_radius[-1]],
            s=23,
            facecolor="white",
            edgecolor=GOLD,
            linewidth=0.9,
            zorder=5,
        )
        right.annotate(
            r"$4096/85\approx48.19$",
            xy=(128, same_radius[-1]),
            xytext=(76, 39),
            arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.7},
            color=MUTED,
            fontsize=6.3,
        )
        right.text(
            126,
            half_bound + 0.9,
            r"valid in the smaller norm $\mathcal{A}_{\rho/2}$",
            ha="right",
            va="bottom",
            fontsize=6.05,
            color=BLUE,
        )
        right.set_xlabel(r"witness degree $N$")
        right.set_ylabel("operator output norm / bound")
        right.set_xlim(1, 132)
        right.set_ylim(0, 52)
        right.set_xticks([1, 32, 64, 96, 128])
        right.set_yticks([0, 10, 20, 30, 40, 50])
        right.grid(axis="y", color=GRID, linewidth=0.42)
        right.legend(loc="upper left")

        figure.text(
            0.012,
            0.986,
            "R0.35 continuation geometry and analytic-radius loss",
            ha="left",
            va="top",
            fontsize=7.1,
            color=INK,
        )
        figure.text(0.985, 0.986, r"$\nu$", ha="right", va="top", fontsize=8.0, color=MUTED)
        figure.text(
            0.985,
            0.053,
            rf"Candidate balanced-radius ratio: [{radius_ratio_lower:.4f}, {radius_ratio_upper:.4f}].  "
            r"Same-radius witness: $3N^2/[4(2N-1)]$; smaller-radius estimate is a different norm.",
            fontsize=5.45,
            color=MUTED,
            ha="right",
            va="bottom",
        )
        figure.text(
            0.985,
            0.016,
            "All curves use exact R0.35 formulas; the R0.32 hull remains a finite Pade diagnostic, not a certified singularity.",
            fontsize=5.55,
            color=MUTED,
            ha="right",
            va="bottom",
        )
        figure.subplots_adjust(left=0.072, right=0.985, bottom=0.22, top=0.82, wspace=0.28)

        for suffix in ("pdf", "svg", "png"):
            output = PACKAGE / f"figure.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        public_figures = REPOSITORY / "public/figures"
        public_figures.mkdir(parents=True, exist_ok=True)
        for suffix in ("svg", "png"):
            output = public_figures / f"r0-35-continuation-scale.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        plt.close(figure)


if __name__ == "__main__":
    draw()
