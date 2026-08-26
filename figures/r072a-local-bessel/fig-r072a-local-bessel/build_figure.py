#!/usr/bin/env python3
"""Build data and render the formal R0.72A journal figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import resource
import time
from zoneinfo import ZoneInfo

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from scipy.special import j0, jn_zeros


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
TIMEZONE = ZoneInfo("Asia/Shanghai")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def log(stage: str, **fields: object) -> None:
    payload = {
        "timestamp": datetime.now(TIMEZONE).isoformat(timespec="milliseconds"),
        "stage": stage,
        **fields,
    }
    with (ROOT / "progress.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, sort_keys=True) + "\n")


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def configure(palette: dict[str, str]) -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 6.7,
            "axes.titlesize": 7.35,
            "axes.labelsize": 6.35,
            "xtick.labelsize": 5.45,
            "ytick.labelsize": 5.45,
            "legend.fontsize": 4.95,
            "axes.edgecolor": palette["ink"],
            "axes.labelcolor": palette["ink"],
            "text.color": palette["ink"],
            "xtick.color": palette["ink"],
            "ytick.color": palette["ink"],
            "axes.facecolor": palette["paper"],
            "figure.facecolor": palette["paper"],
            "savefig.facecolor": palette["paper"],
            "axes.linewidth": 0.68,
            "lines.linewidth": 1.1,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "r072a-local-bessel",
        }
    )


def blossom(fig: plt.Figure, palette: dict[str, str]) -> None:
    center_x, center_y = 0.977, 0.952
    for index, color in enumerate(
        (palette["blue"], palette["ochre"], palette["blue"], palette["ochre"], palette["blue"])
    ):
        angle = 2.0 * np.pi * index / 5.0 + np.pi / 2.0
        fig.add_artist(
            Circle(
                (center_x + 0.0085 * np.cos(angle), center_y + 0.0085 * np.sin(angle)),
                0.0058,
                transform=fig.transFigure,
                facecolor=color,
                edgecolor=palette["paper"],
                linewidth=0.3,
                alpha=0.84,
                zorder=20,
            )
        )
    fig.add_artist(
        Circle(
            (center_x, center_y),
            0.0045,
            transform=fig.transFigure,
            facecolor=palette["ink"],
            edgecolor=palette["paper"],
            linewidth=0.3,
            zorder=21,
        )
    )


def panel_title(axis: plt.Axes, letter: str, title: str) -> None:
    axis.set_title(f"{letter}   {title}", loc="left", fontweight="bold", pad=4.0)


def build_rows(
    config: dict[str, object],
    producer: dict[str, object],
    independent: dict[str, object],
) -> tuple[list[dict[str, object]], dict[str, object]]:
    rows: list[dict[str, object]] = []
    phase = config["phaseGrid"]
    beta_grid = np.linspace(
        float(phase["betaMinimum"]),
        float(phase["betaMaximum"]),
        int(phase["points"]),
    )
    for beta in beta_grid:
        exposure = (6.0 + 3.0 * float(beta)) / 7.0
        certified = min(1.5, exposure)
        for series, value in (
            ("certified boundary", certified),
            ("local exposure constraint", exposure),
            ("first-root cap", 1.5),
        ):
            rows.append(
                {
                    "panel": "A",
                    "series": series,
                    "x": float(beta),
                    "y": float(value),
                    "xUnit": "beta in L=M^-beta",
                    "yUnit": "alpha in eta=M^alpha",
                    "evidence": "analytic formula",
                    "source": "R0.72A equation (0.7)",
                }
            )

    bessel_values: dict[int, float] = {}
    for r_value in [int(value) for value in config["besselRValues"]]:
        zeros = jn_zeros(1, r_value)
        mass = float(4.0 * np.sum(j0(zeros) ** 2))
        bessel_values[r_value] = mass
    coefficient = 8.0 / math.pi**2
    largest_r = max(bessel_values)
    asymptotic_constant = bessel_values[largest_r] - coefficient * math.log(largest_r)
    for r_value, mass in bessel_values.items():
        rows.extend(
            [
                {
                    "panel": "B",
                    "series": "frozen Bessel sum",
                    "x": r_value,
                    "y": mass,
                    "xUnit": "positive selected roots R",
                    "yUnit": "rescaled row mass G",
                    "evidence": "Bessel formula",
                    "source": "4 sum J0(j_1,k)^2",
                },
                {
                    "panel": "B",
                    "series": "leading logarithm",
                    "x": r_value,
                    "y": coefficient * math.log(r_value) + asymptotic_constant,
                    "xUnit": "positive selected roots R",
                    "yUnit": "rescaled row mass G",
                    "evidence": "analytic asymptote",
                    "source": "(8/pi^2) log R plus fitted display intercept",
                },
            ]
        )

    for row in producer["finiteLattice"]:
        rows.append(
            {
                "panel": "B",
                "series": "producer exact finite lattice",
                "x": int(row["R"]),
                "y": float(row["exactSelectedMass"]),
                "xUnit": "positive selected roots R",
                "yUnit": "rescaled row mass G",
                "evidence": "deterministic finite calculation",
                "source": "research/certificates/r072a/result.json",
            }
        )
        rows.extend(
            [
                {
                    "panel": "C",
                    "series": "observation layer L_R",
                    "x": int(row["R"]),
                    "y": float(row["layerLength"]),
                    "xUnit": "positive selected roots R",
                    "yUnit": "physical x-coordinate length",
                    "evidence": "deterministic finite calculation",
                    "source": "research/certificates/r072a/result.json",
                },
                {
                    "panel": "C",
                    "series": "maximum root displacement",
                    "x": int(row["R"]),
                    "y": float(row["maximumRootShift"]) / float(row["delta"]),
                    "xUnit": "positive selected roots R",
                    "yUnit": "physical x-coordinate length",
                    "evidence": "deterministic finite calculation",
                    "source": "research/certificates/r072a/result.json",
                },
            ]
        )
    for row in independent["finiteLattice"]:
        rows.append(
            {
                "panel": "B",
                "series": "independent exact finite lattice",
                "x": int(row["R"]),
                "y": float(row["exactSelectedMass"]),
                "xUnit": "positive selected roots R",
                "yUnit": "rescaled row mass G",
                "evidence": "independent deterministic finite calculation",
                "source": "research/certificates/r072a/independent-result.json",
            }
        )

    cross_rows = []
    for left in producer["finiteLattice"]:
        matches = [right for right in independent["finiteLattice"] if right["R"] == left["R"]]
        if matches:
            right = matches[0]
            cross_rows.append(
                {
                    "R": int(left["R"]),
                    "massDifference": abs(
                        float(left["exactSelectedMass"])
                        - float(right["exactSelectedMass"])
                    ),
                    "maximumRootDifference": max(
                        abs(float(a["exactRootTau"]) - float(b["tau"]))
                        for a, b in zip(left["roots"], right["roots"], strict=True)
                    ),
                }
            )

    results = {
        "schemaVersion": "r072a-figure-results-v1",
        "sourceStatus": {
            "producerAllPassed": bool(producer["allPassed"]),
            "independentAllPassed": bool(independent["allPassed"]),
        },
        "phaseBoundary": {
            "fixedLength": 6.0 / 7.0,
            "fastShrinking": 1.5,
            "formula": "min(3/2,(6+3 beta)/7)",
        },
        "bessel": {
            "leadingCoefficient": coefficient,
            "displayIntercept": asymptotic_constant,
            "largestR": largest_r,
        },
        "crossAudit": cross_rows,
        "rowCount": len(rows),
    }
    return rows, results


def write_data(rows: list[dict[str, object]], results: dict[str, object]) -> None:
    fields = ["panel", "series", "x", "y", "xUnit", "yUnit", "evidence", "source"]
    with (ROOT / "data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "data.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (ROOT / "results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def select(rows: list[dict[str, object]], panel: str, series: str) -> tuple[np.ndarray, np.ndarray]:
    selected = sorted(
        [row for row in rows if row["panel"] == panel and row["series"] == series],
        key=lambda row: float(row["x"]),
    )
    return (
        np.asarray([float(row["x"]) for row in selected], dtype=float),
        np.asarray([float(row["y"]) for row in selected], dtype=float),
    )


def render(rows: list[dict[str, object]], config: dict[str, object]) -> None:
    palette = config["palette"]
    configure(palette)
    figure_config = config["figure"]
    width = round(float(figure_config["widthMillimetres"]) / 25.4, 2)
    height = round(float(figure_config["heightMillimetres"]) / 25.4, 2)
    fig = plt.figure(figsize=(width, height), constrained_layout=False)
    grid = fig.add_gridspec(
        1,
        3,
        left=0.072,
        right=0.985,
        bottom=0.235,
        top=0.765,
        wspace=0.36,
        width_ratios=(1.0, 1.08, 1.0),
    )
    axa, axb, axc = [fig.add_subplot(grid[0, index]) for index in range(3)]
    fig.suptitle(
        "Local exposure and an exact Bessel obstruction",
        x=0.072,
        y=0.955,
        ha="left",
        fontsize=10.0,
        fontweight="bold",
    )
    fig.text(
        0.072,
        0.895,
        r"Real triangular lattice  $\cdot$  selected positive roots  $\cdot$  rescaled row mass  $\cdot$  no DNS",
        ha="left",
        fontsize=6.05,
        color=palette["gray"],
    )
    blossom(fig, palette)

    beta, certified = select(rows, "A", "certified boundary")
    _, exposure = select(rows, "A", "local exposure constraint")
    _, first = select(rows, "A", "first-root cap")
    axa.fill_between(beta, 0.0, certified, color=palette["blue"], alpha=0.13, linewidth=0)
    axa.plot(beta, certified, color=palette["blue"], label="certified boundary")
    axa.plot(beta, exposure, color=palette["ochre"], linestyle="--", label="local exposure")
    axa.plot(beta, first, color=palette["gray"], linestyle=":", label="first-root cap")
    axa.scatter([0.0, 1.5], [6.0 / 7.0, 1.5], s=13, color=palette["blue"], zorder=4)
    axa.annotate(r"$6/7$", (0.0, 6.0 / 7.0), xytext=(5, -8), textcoords="offset points", fontsize=5.2)
    axa.annotate(r"$3/2$", (1.5, 1.5), xytext=(4, 4), textcoords="offset points", fontsize=5.2)
    axa.set_xlim(0.0, 3.0)
    axa.set_ylim(0.0, 2.2)
    axa.set_xlabel(r"layer exponent $\beta$ in $L=M^{-\beta}$")
    axa.set_ylabel(r"coupling exponent $\alpha$")
    axa.grid(True, color=palette["light"], linewidth=0.35)
    axa.legend(loc="lower right", frameon=False, handlelength=2.3)
    panel_title(axa, "A", "Power-law certificate")

    r_bes, mass_bes = select(rows, "B", "frozen Bessel sum")
    r_log, mass_log = select(rows, "B", "leading logarithm")
    r_prod, mass_prod = select(rows, "B", "producer exact finite lattice")
    r_ind, mass_ind = select(rows, "B", "independent exact finite lattice")
    axb.plot(r_bes, mass_bes, color=palette["blue"], label="frozen Bessel sum")
    axb.plot(r_log, mass_log, color=palette["gray"], linestyle=":", label=r"$(8/\pi^2)\log R+C$")
    axb.plot(
        r_prod,
        mass_prod,
        linestyle="none",
        marker="o",
        markersize=3.6,
        markerfacecolor=palette["ochre"],
        markeredgecolor=palette["paper"],
        markeredgewidth=0.45,
        label="producer",
        zorder=4,
    )
    axb.plot(
        r_ind,
        mass_ind,
        linestyle="none",
        marker="s",
        markersize=3.5,
        markerfacecolor="none",
        markeredgecolor=palette["ink"],
        markeredgewidth=0.75,
        label="independent",
        zorder=5,
    )
    axb.set_xscale("log", base=2)
    axb.set_xticks([4, 16, 64, 256, 1024])
    axb.set_xticklabels(["4", "16", "64", "256", "1024"])
    axb.set_xlim(3.3, 2500)
    axb.set_ylim(0.9, 6.8)
    axb.set_xlabel(r"selected positive roots $R$")
    axb.set_ylabel(r"row mass $G_R^{\rm sel}$")
    axb.grid(True, which="major", color=palette["light"], linewidth=0.35)
    axb.legend(loc="lower right", frameon=False, handlelength=2.2)
    panel_title(axb, "B", "Exact-root mass")

    r_layer, layer = select(rows, "C", "observation layer L_R")
    r_shift, shift = select(rows, "C", "maximum root displacement")
    axc.plot(
        r_layer,
        layer,
        color=palette["blue"],
        marker="o",
        markersize=3.2,
        markerfacecolor=palette["blue"],
        markeredgecolor=palette["paper"],
        markeredgewidth=0.4,
        label=r"layer $L_R$",
    )
    axc.plot(
        r_shift,
        shift,
        color=palette["ochre"],
        linestyle="--",
        marker="s",
        markersize=3.2,
        markerfacecolor=palette["paper"],
        markeredgecolor=palette["ochre"],
        markeredgewidth=0.75,
        label=r"max physical $|\Delta x|$",
    )
    guide_r = np.geomspace(4.0, 64.0, 80)
    axc.plot(
        guide_r,
        layer[-1] * (guide_r / 64.0) ** -3,
        color=palette["gray"],
        linestyle=":",
        linewidth=0.7,
    )
    axc.plot(
        guide_r,
        shift[-1] * (guide_r / 64.0) ** -6,
        color=palette["gray"],
        linestyle=(0, (3, 2)),
        linewidth=0.7,
    )
    axc.text(0.66, 0.66, r"$R^{-3}$", transform=axc.transAxes, fontsize=5.25, color=palette["gray"])
    axc.text(0.66, 0.18, r"$R^{-6}$", transform=axc.transAxes, fontsize=5.25, color=palette["gray"])
    axc.set_xscale("log", base=2)
    axc.set_yscale("log")
    axc.set_xticks([4, 8, 16, 32, 64])
    axc.set_xticklabels(["4", "8", "16", "32", "64"])
    axc.set_xlabel(r"selected positive roots $R$")
    axc.set_ylabel(r"physical $x$ length")
    axc.grid(True, which="major", color=palette["light"], linewidth=0.35)
    axc.grid(True, which="minor", axis="y", color=palette["light"], linewidth=0.2, alpha=0.45)
    axc.legend(loc="lower left", frameon=False, handlelength=2.2)
    panel_title(axc, "C", "Shrinking scales")

    fig.text(
        0.072,
        0.095,
        "Analytic region + deterministic certificates. Bessel markers use one carrier and do not establish nonlinear normalized divergence.",
        ha="left",
        fontsize=5.3,
        color=palette["gray"],
    )
    fig.text(
        0.985,
        0.095,
        "R0.72A-1",
        ha="right",
        fontsize=5.3,
        color=palette["gray"],
    )

    output_stem = ROOT / "figure"
    fig.savefig(output_stem.with_suffix(".pdf"), bbox_inches=None)
    fig.savefig(output_stem.with_suffix(".svg"), bbox_inches=None)
    fig.savefig(
        output_stem.with_suffix(".png"),
        dpi=int(figure_config["pngDpi"]),
        bbox_inches=None,
    )
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    config = load_json(args.config)
    producer_path = REPOSITORY / config["sourceCertificates"]["producer"]
    independent_path = REPOSITORY / config["sourceCertificates"]["independent"]
    producer = load_json(producer_path)
    independent = load_json(independent_path)
    if not producer["allPassed"] or not independent["allPassed"]:
        raise RuntimeError("source certificate did not pass")
    log("figure-build-start")
    rows, results = build_rows(config, producer, independent)
    write_data(rows, results)
    log("figure-data-complete", rowCount=len(rows))
    render(rows, config)
    metadata = {
        "schemaVersion": "r072a-figure-data-metadata-v1",
        "generatedAt": datetime.now(TIMEZONE).isoformat(timespec="seconds"),
        "sourceFiles": [
            {"path": str(path.relative_to(REPOSITORY)), "sha256": sha256(path)}
            for path in (producer_path, independent_path)
        ],
        "dataFiles": {
            name: sha256(ROOT / name)
            for name in ("data.csv", "data.json", "results.json")
        },
        "rowCount": len(rows),
        "claimBoundary": load_json(ROOT / "contract.json")["claimBoundary"],
    }
    (ROOT / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    elapsed = time.perf_counter() - started
    log("figure-build-complete", elapsedSeconds=elapsed)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    with (ROOT / "resource-log.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(
            json.dumps(
                {
                    "timestamp": datetime.now(TIMEZONE).isoformat(timespec="milliseconds"),
                    "stage": "figure-build-complete",
                    "elapsedSeconds": elapsed,
                    "processUserCpuSeconds": usage.ru_utime,
                    "processSystemCpuSeconds": usage.ru_stime,
                    "maximumResidentSetRaw": usage.ru_maxrss,
                },
                sort_keys=True,
            )
            + "\n"
        )
    print(json.dumps({"status": "passed", "rowCount": len(rows), "elapsedSeconds": elapsed}, indent=2))


if __name__ == "__main__":
    main()
