#!/usr/bin/env python3
"""Plot the R0.27 charge-one endpoint polarization audit.

Chart contract
--------------
Question: How does the normalized sharp coordinate on the exact negative-edge
endpoint behave across the finite dual-precision window N=2,...,75?
Takeaway: After the parity twist the computed coordinate rises toward one,
while both its unit-modulus defect and the inverse sharp/longitudinal ratio
decay approximately exponentially on the finite tail.
Family: two-panel line chart with a logarithmic diagnostic panel.
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
    REPOSITORY / "research/certificates/r027/edge-generating-function.json"
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
    high_run = payload["runs"][-1]
    stability = payload["checks"]["precisionStability"]
    rows = []
    for record in high_run["endpoints"]:
        parameter = int(record["parameter"])
        ratio = abs(float(record["sharpOverLAlpha"]))
        rows.append(
            {
                "N": parameter,
                "sigma": float(record["sigma"]),
                "parityNormalizedSigma": ((-1) ** parameter)
                * float(record["sigma"]),
                "absoluteSigma": float(record["absoluteSigma"]),
                "oneMinusAbsoluteSigma": float(record["oneMinusAbsoluteSigma"]),
                "absoluteSharpOverLAlpha": ratio,
                "inverseAbsoluteSharpOverLAlpha": 1 / ratio,
                "sigmaRelativePrecisionDifference": float(
                    stability[f"N{parameter}"]["sigmaRelativeDifference"]
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
    """Keep generated SVGs free of backend-specific trailing whitespace."""

    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(
        "\n".join(line.rstrip() for line in lines) + "\n",
        encoding="utf-8",
    )


def draw(rows: list[dict[str, float | int]]) -> None:
    parameters = [int(row["N"]) for row in rows]
    parity = [float(row["parityNormalizedSigma"]) for row in rows]
    defect = [float(row["oneMinusAbsoluteSigma"]) for row in rows]
    inverse_ratio = [
        float(row["inverseAbsoluteSharpOverLAlpha"]) for row in rows
    ]

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        figure, (left, right) = plt.subplots(
            1,
            2,
            figsize=(178 / 25.4, 72 / 25.4),
            gridspec_kw={"width_ratios": (1.05, 1)},
            layout="none",
        )
        left.axhline(1, color=MUTED, linewidth=.65, linestyle="--")
        left.axhline(0, color=INK, linewidth=.45)
        left.plot(
            parameters,
            parity,
            color=BLUE,
            linewidth=1.05,
            marker="o",
            markersize=2.4,
            markerfacecolor="white",
            markeredgewidth=.55,
            label=r"$(-1)^N\sigma_{B,N}$",
        )
        left.plot(
            [75],
            [parity[-1]],
            marker="*",
            markersize=7,
            markerfacecolor=GOLD,
            markeredgecolor=INK,
            markeredgewidth=.5,
            linestyle="none",
            zorder=4,
        )
        left.annotate(
            r"$0.9997789$",
            xy=(75, parity[-1]),
            xytext=(54, .82),
            arrowprops={"arrowstyle": "-", "color": MUTED, "linewidth": .55},
            fontsize=6.6,
        )
        left.set_xlim(2, 76)
        left.set_ylim(min(-.18, min(parity) - .04), 1.055)
        left.set_xlabel(r"endpoint parameter $N$")
        left.set_ylabel(r"$(-1)^N\sigma_{B,N}$")
        left.set_title("(a) Charge-one endpoint polarization", loc="left", pad=5)
        left.legend(loc="lower right", frameon=False)

        right.axvspan(56, 75, facecolor=PALE, edgecolor="none", alpha=.65)
        right.semilogy(
            parameters,
            defect,
            color=BLUE,
            linewidth=1.05,
            marker="o",
            markevery=4,
            markersize=2.7,
            markerfacecolor="white",
            markeredgewidth=.55,
            label=r"$1-|\sigma_{B,N}|$",
        )
        right.semilogy(
            parameters,
            inverse_ratio,
            color=GOLD,
            linewidth=1.05,
            linestyle="--",
            marker="s",
            markevery=4,
            markersize=2.5,
            markerfacecolor="white",
            markeredgewidth=.55,
            label=r"$|L\alpha/s|$",
        )
        right.text(65.5, .45, "fit window", color=MUTED, fontsize=6.4)
        right.set_xlim(2, 76)
        right.set_xlabel(r"endpoint parameter $N$")
        right.set_ylabel("value (log scale)")
        right.set_title("(b) Finite-tail decay diagnostics", loc="left", pad=5)
        right.legend(loc="lower left", frameon=False)

        figure.text(
            .01,
            .985,
            "R0.27 negative-edge endpoint audit · 160/224-bit MPFR · N=2--75",
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
            output = public_figures / f"r0-27-endpoint-polarization.{suffix}"
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
