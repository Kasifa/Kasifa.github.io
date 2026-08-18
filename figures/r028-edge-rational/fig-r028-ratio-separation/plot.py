#!/usr/bin/env python3
"""Plot the R0.28 exact finite coefficient-ratio separation.

Chart contract
--------------
Question: Do the exact root-box intervals separate the sharp and in-plane
coefficient-radius proxies on the certified finite window?
Takeaway: The sharp proxy stays below the in-plane proxy for N=18,...,40;
the relative block factor stays strictly above one on that same window.
Family: two-panel line chart with exact interval bands.
Palette: restrained blue and gold, with marker and line-style redundancy.
Footprint: 178 mm by 72 mm; PDF/SVG plus 600 dpi PNG.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
STYLE = PACKAGE.parents[1] / "journal.mplstyle"
DEFAULT_CERTIFICATE = (
    REPOSITORY / "research/certificates/r028/edge-rational-asymptotic.json"
)
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
GOLD = "#a16f27"
PALE = "#e9e1d1"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    return parser.parse_args()


def extract_rows(certificate: Path) -> list[dict[str, float | int]]:
    payload = json.loads(certificate.read_text(encoding="utf-8"))
    rows: list[dict[str, float | int]] = []
    for record in payload["endpoints"]:
        parameter = int(record["parameter"])
        if parameter < 18:
            continue
        ratios = record["consecutiveRatios"]
        rows.append(
            {
                "N": parameter,
                "rhoA": float(ratios["normalizedRadiusProxyA"]["decimal"]),
                "rhoDLower": float(
                    ratios["normalizedRadiusProxyD"]["decimal"][0]
                ),
                "rhoDUpper": float(
                    ratios["normalizedRadiusProxyD"]["decimal"][1]
                ),
                "gammaLower": float(
                    ratios["sharpToAlphaBlockFactorRootBox"]["decimal"][0]
                ),
                "gammaUpper": float(
                    ratios["sharpToAlphaBlockFactorRootBox"]["decimal"][1]
                ),
            }
        )
    return rows


def write_data(rows: list[dict[str, float | int]]) -> None:
    with (PACKAGE / "data.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=list(rows[0]),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def normalize_svg(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(
        "\n".join(line.rstrip() for line in lines) + "\n",
        encoding="utf-8",
    )


def draw(rows: list[dict[str, float | int]]) -> None:
    parameters = [int(row["N"]) for row in rows]
    rho_a = [float(row["rhoA"]) for row in rows]
    rho_d_lower = [float(row["rhoDLower"]) for row in rows]
    rho_d_upper = [float(row["rhoDUpper"]) for row in rows]
    rho_d_center = [
        (lower + upper) / 2
        for lower, upper in zip(rho_d_lower, rho_d_upper, strict=True)
    ]
    gamma_lower = [float(row["gammaLower"]) for row in rows]
    gamma_upper = [float(row["gammaUpper"]) for row in rows]
    gamma_center = [
        (lower + upper) / 2
        for lower, upper in zip(gamma_lower, gamma_upper, strict=True)
    ]

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        figure, (left, right) = plt.subplots(
            1,
            2,
            figsize=(178 / 25.4, 72 / 25.4),
            gridspec_kw={"width_ratios": (1, 1)},
            layout="none",
        )

        for axis in (left, right):
            axis.axvspan(29, 40, facecolor=PALE, edgecolor="none", alpha=.7)

        left.plot(
            parameters,
            rho_a,
            color=BLUE,
            marker="o",
            markersize=2.8,
            markerfacecolor="white",
            markeredgewidth=.55,
            label=r"$\rho^A_N$",
        )
        left.fill_between(
            parameters,
            rho_d_lower,
            rho_d_upper,
            color=GOLD,
            alpha=.24,
            linewidth=0,
        )
        left.plot(
            parameters,
            rho_d_center,
            color=GOLD,
            linestyle="--",
            marker="s",
            markersize=2.5,
            markerfacecolor="white",
            markeredgewidth=.55,
            label=r"root-box $\rho^D_N$",
        )
        left.set_xlim(17.5, 40.5)
        left.set_ylim(.55, 1.01)
        left.set_xlabel(r"endpoint parameter $N$")
        left.set_ylabel("coefficient-radius proxy")
        left.set_title("(a) Exact finite ratio separation", loc="left", pad=5)
        left.legend(loc="lower right", frameon=False)

        right.axhline(1, color=INK, linewidth=.65, linestyle=":")
        right.fill_between(
            parameters,
            gamma_lower,
            gamma_upper,
            color=BLUE,
            alpha=.2,
            linewidth=0,
        )
        right.plot(
            parameters,
            gamma_center,
            color=BLUE,
            marker="o",
            markersize=2.8,
            markerfacecolor="white",
            markeredgewidth=.55,
            label=r"root-box $\Gamma_N$",
        )
        right.set_xlim(17.5, 40.5)
        right.set_ylim(.98, 1.64)
        right.set_xlabel(r"endpoint parameter $N$")
        right.set_ylabel(r"relative block factor $\Gamma_N$")
        right.set_title("(b) Sharp-to-in-plane relative growth", loc="left", pad=5)
        right.legend(loc="upper right", frameon=False)

        figure.text(
            .01,
            .985,
            "R0.28 exact GMP rational audit · full certified root box · N=18–40",
            ha="left",
            va="top",
            fontsize=7.2,
            color=INK,
        )
        figure.subplots_adjust(left=.075, right=.985, bottom=.19, top=.82, wspace=.28)

        for suffix in ("pdf", "svg", "png"):
            output = PACKAGE / f"figure.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        public_figures = REPOSITORY / "public/figures"
        public_figures.mkdir(parents=True, exist_ok=True)
        for suffix in ("svg", "png"):
            output = public_figures / f"r0-28-ratio-separation.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        plt.close(figure)


def main() -> None:
    arguments = parse_arguments()
    rows = extract_rows(arguments.certificate)
    write_data(rows)
    draw(rows)


if __name__ == "__main__":
    main()
