#!/usr/bin/env python3
"""Build data and render the formal R0.72B target-row coherence figure."""

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
            "axes.labelsize": 6.25,
            "xtick.labelsize": 5.35,
            "ytick.labelsize": 5.35,
            "legend.fontsize": 4.8,
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
            "svg.hashsalt": "r072b-row-coherence",
        }
    )


def blossom(fig: plt.Figure, palette: dict[str, str]) -> None:
    center_x, center_y = 0.977, 0.952
    colors = (
        palette["blue"],
        palette["ochre"],
        palette["blue"],
        palette["ochre"],
        palette["blue"],
    )
    for index, color in enumerate(colors):
        angle = 2.0 * np.pi * index / 5.0 + np.pi / 2.0
        fig.add_artist(
            Circle(
                (
                    center_x + 0.0085 * np.cos(angle),
                    center_y + 0.0085 * np.sin(angle),
                ),
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
) -> tuple[list[dict[str, object]], dict[str, object]]:
    rows: list[dict[str, object]] = []
    phase = config["phaseGrid"]
    beta_grid = np.linspace(
        float(phase["betaMinimum"]),
        float(phase["betaMaximum"]),
        int(phase["points"]),
    )
    for beta in beta_grid:
        series_values = (
            ("old M^-2", min(1.5, (6.0 + 3.0 * beta) / 7.0)),
            (
                "target participation M^-3",
                min(2.25, (9.0 + 3.0 * beta) / 7.0),
            ),
            (
                "coherent M^-10/3",
                min(2.5, (10.0 + 3.0 * beta) / 7.0),
            ),
        )
        for series, value in series_values:
            rows.append(
                {
                    "panel": "A",
                    "series": series,
                    "x": float(beta),
                    "y": float(value),
                    "xUnit": "beta in L=M^-beta",
                    "yUnit": "alpha in eta=M^alpha",
                    "evidence": "analytic formula",
                    "source": "R0.72B power-law corollary",
                    "note": "strict inequality below the displayed boundary",
                }
            )

    uniform_multiplier_constant = 2.0 * math.pi**2 / 3.0
    for row in producer["equalCarrierLedger"]["rows"]:
        m_value = int(row["M"])
        chi = float(row["chi"])
        multiplier = float(row["OmegaSquaredOverKv"])
        combined_gain = chi * (multiplier / uniform_multiplier_constant) ** (1.0 / 3.0)
        for series, value, note in (
            ("target-row factor chi", chi, "exactly 1/(2M)"),
            (
                "multiplier/enstrophy factor",
                multiplier,
                "exactly 24M/[(M+1)(2M+1)] for Kz=1",
            ),
            (
                "combined gain vs old constants",
                combined_gain,
                "chi*(Omega^2/Kv/(2pi^2/3))^(1/3)",
            ),
        ):
            rows.append(
                {
                    "panel": "B",
                    "series": series,
                    "x": m_value,
                    "y": value,
                    "xUnit": "equal positive carriers M",
                    "yUnit": "dimensionless factor",
                    "evidence": "exact finite-sum formula",
                    "source": "research/certificates/r072b/result.json",
                    "note": note,
                }
            )

    bessel_keys = (
        (
            "layer x frozen ED rate",
            "ThetaLayerTimesFrozenRate",
            "L_R*R^2/(log R)^2",
        ),
        (
            "heat-freezing Xi",
            "heatFreezingXi",
            "2R^4[L_R-(1-exp(-L_R))]",
        ),
        (
            "energy-loss upper bound",
            "energyLossUpper",
            "[4T_R+4T_R^2+(8/3)T_R^3]/R^4",
        ),
    )
    for row in producer["besselNoGo"]["rows"]:
        for series, key, note in bessel_keys:
            rows.append(
                {
                    "panel": "C",
                    "series": series,
                    "x": int(row["R"]),
                    "y": float(row[key]),
                    "xUnit": "selected Bessel roots R",
                    "yUnit": "dimensionless upper indicator",
                    "evidence": "analytic formula evaluated at mpmath Bessel zero",
                    "source": "research/certificates/r072b/result.json",
                    "note": note,
                }
            )

    results = {
        "schemaVersion": "r072b-figure-results-v1",
        "sourceStatus": {"producerAllPassed": bool(producer["allPassed"])},
        "phaseBoundary": {
            "oldFixedLayer": 6.0 / 7.0,
            "targetParticipationFixedLayer": 9.0 / 7.0,
            "coherentFixedLayer": 10.0 / 7.0,
            "coherentCap": 2.5,
            "coherentFormula": "min(5/2,(10+3 beta)/7)",
        },
        "equalCarrier": {
            "chi": "1/(2M)",
            "OmegaSquaredOverKv": "24M/[(M+1)(2M+1)]",
            "normalizedGeometricPower": "-10/3",
            "largestM": int(producer["equalCarrierLedger"]["rows"][-1]["M"]),
        },
        "bessel": {
            "largestR": int(producer["besselNoGo"]["rows"][-1]["R"]),
            "tailPowers": producer["besselNoGo"]["tailPowers"],
        },
        "rowCount": len(rows),
    }
    return rows, results


def write_data(rows: list[dict[str, object]], results: dict[str, object]) -> None:
    fields = [
        "panel",
        "series",
        "x",
        "y",
        "xUnit",
        "yUnit",
        "evidence",
        "source",
        "note",
    ]
    with (ROOT / "data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def select(
    rows: list[dict[str, object]], panel: str, series: str
) -> tuple[np.ndarray, np.ndarray]:
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
    width = float(figure_config["widthMillimetres"]) / 25.4
    height = float(figure_config["heightMillimetres"]) / 25.4
    fig = plt.figure(figsize=(width, height), constrained_layout=False)
    grid = fig.add_gridspec(
        1,
        3,
        left=0.072,
        right=0.985,
        bottom=0.235,
        top=0.765,
        wspace=0.38,
        width_ratios=(1.0, 1.06, 1.03),
    )
    axa, axb, axc = [fig.add_subplot(grid[0, index]) for index in range(3)]
    fig.suptitle(
        "Target-row participation and coherent carrier scaling",
        x=0.072,
        y=0.955,
        ha="left",
        fontsize=10.0,
        fontweight="bold",
    )
    fig.text(
        0.072,
        0.895,
        r"Exact launch  $\cdot$  $r_l=l,\ z_l=1$  $\cdot$  sufficient upper-bound region  $\cdot$  no DNS",
        ha="left",
        fontsize=6.05,
        color=palette["gray"],
    )
    blossom(fig, palette)

    beta_old, old = select(rows, "A", "old M^-2")
    beta_part, participation = select(rows, "A", "target participation M^-3")
    beta_coh, coherent = select(rows, "A", "coherent M^-10/3")
    axa.plot(beta_old, old, color=palette["gray"], linestyle=":", label=r"old $M^{-2}$")
    axa.plot(
        beta_part,
        participation,
        color=palette["ochre"],
        linestyle="--",
        label=r"row $M^{-3}$",
    )
    axa.plot(
        beta_coh,
        coherent,
        color=palette["blue"],
        linestyle="-",
        label=r"coherent $M^{-10/3}$",
    )
    axa.scatter(
        [0.0, 2.5],
        [10.0 / 7.0, 2.5],
        s=14,
        color=palette["blue"],
        edgecolor=palette["paper"],
        linewidth=0.4,
        zorder=5,
    )
    axa.annotate(r"$10/7$", (0.0, 10.0 / 7.0), xytext=(5, -8), textcoords="offset points", fontsize=5.15)
    axa.annotate(r"$5/2$", (2.5, 2.5), xytext=(4, 3), textcoords="offset points", fontsize=5.15)
    axa.set_xlim(0.0, 4.0)
    axa.set_ylim(0.0, 2.75)
    axa.set_xticks([0, 1, 2, 3, 4])
    axa.set_xlabel(r"layer exponent $\beta$ in $L=M^{-\beta}$")
    axa.set_ylabel(r"coupling exponent $\alpha$")
    axa.grid(True, color=palette["light"], linewidth=0.35)
    axa.legend(loc="lower right", frameon=False, handlelength=2.4)
    panel_title(axa, "A", "Sufficient phase boundaries")

    m_chi, chi = select(rows, "B", "target-row factor chi")
    m_mult, multiplier = select(rows, "B", "multiplier/enstrophy factor")
    m_gain, gain = select(rows, "B", "combined gain vs old constants")
    axb.plot(
        m_chi,
        chi,
        color=palette["blue"],
        marker="o",
        markevery=2,
        markersize=2.8,
        markerfacecolor=palette["blue"],
        markeredgecolor=palette["paper"],
        markeredgewidth=0.35,
        label=r"$\chi_M$",
    )
    axb.plot(
        m_mult,
        multiplier,
        color=palette["ochre"],
        linestyle="--",
        marker="s",
        markevery=2,
        markersize=2.8,
        markerfacecolor=palette["paper"],
        markeredgecolor=palette["ochre"],
        markeredgewidth=0.65,
        label=r"$\Omega^2/K_v$",
    )
    axb.plot(
        m_gain,
        gain,
        color=palette["ink"],
        linestyle=":",
        marker="^",
        markevery=2,
        markersize=2.9,
        markerfacecolor="none",
        markeredgecolor=palette["ink"],
        markeredgewidth=0.65,
        label="combined / old",
    )
    guide_m = np.geomspace(16.0, 1.0e6, 100)
    axb.plot(
        guide_m,
        0.18 * (guide_m / 16.0) ** -1.0,
        color=palette["gray"],
        linestyle=(0, (3, 2)),
        linewidth=0.65,
        alpha=0.8,
    )
    axb.text(0.70, 0.61, r"$M^{-1}$", transform=axb.transAxes, fontsize=5.15, color=palette["gray"])
    axb.text(
        0.47,
        0.91,
        r"$-2-1-1/3=-10/3$",
        transform=axb.transAxes,
        fontsize=5.0,
        color=palette["gray"],
    )
    axb.set_xscale("log", base=2)
    axb.set_yscale("log")
    axb.set_xticks([1, 16, 256, 4096, 65536, 1048576])
    axb.set_xticklabels(["1", "16", "256", "4k", "65k", "1m"])
    axb.set_xlim(0.8, 1.35e6)
    axb.set_ylim(2e-9, 8.0)
    axb.set_xlabel(r"carrier count $M$")
    axb.set_ylabel("dimensionless factor")
    axb.grid(True, which="major", color=palette["light"], linewidth=0.35)
    axb.legend(loc="lower left", frameon=False, handlelength=2.3)
    panel_title(axb, "B", "Exact-launch factors")

    r_theta, theta = select(rows, "C", "layer x frozen ED rate")
    r_xi, xi = select(rows, "C", "heat-freezing Xi")
    r_energy, energy = select(rows, "C", "energy-loss upper bound")
    axc.plot(
        r_theta,
        theta,
        color=palette["blue"],
        marker="o",
        markersize=3.1,
        markerfacecolor=palette["blue"],
        markeredgecolor=palette["paper"],
        markeredgewidth=0.4,
        label=r"$\Theta_R=L_R\Gamma_{\rm fr}$",
    )
    axc.plot(
        r_xi,
        xi,
        color=palette["ochre"],
        linestyle="--",
        marker="s",
        markersize=3.0,
        markerfacecolor=palette["paper"],
        markeredgecolor=palette["ochre"],
        markeredgewidth=0.7,
        label=r"heat freezing $\Xi_R$",
    )
    axc.plot(
        r_energy,
        energy,
        color=palette["gray"],
        linestyle=":",
        marker="^",
        markersize=3.1,
        markerfacecolor="none",
        markeredgecolor=palette["ink"],
        markeredgewidth=0.65,
        label="energy-loss bound",
    )
    axc.set_xscale("log", base=2)
    axc.set_yscale("log")
    axc.set_xticks([8, 16, 32, 64, 128, 256, 512])
    axc.set_xticklabels(["8", "16", "32", "64", "128", "256", "512"])
    axc.set_xlim(6.8, 610)
    axc.set_xlabel(r"Bessel root count $R$")
    axc.set_ylabel("dimensionless upper indicator")
    axc.grid(True, which="major", color=palette["light"], linewidth=0.35)
    axc.grid(True, which="minor", axis="y", color=palette["light"], linewidth=0.2, alpha=0.45)
    axc.legend(loc="lower left", frameon=False, handlelength=2.2)
    panel_title(axc, "C", "Pre-burn-in comparisons")

    fig.text(
        0.072,
        0.095,
        "Analytic formulas + deterministic cross-audit. Burn-in controls only the remaining tail; no interval proof, DNS, or NSE endpoint claim.",
        ha="left",
        fontsize=5.15,
        color=palette["gray"],
    )
    fig.text(
        0.985,
        0.095,
        "R0.72B-1",
        ha="right",
        fontsize=5.25,
        color=palette["gray"],
    )

    output_stem = ROOT / "figure"
    fig.savefig(output_stem.with_suffix(".pdf"), bbox_inches=None)
    svg_path = output_stem.with_suffix(".svg")
    fig.savefig(svg_path, bbox_inches=None)
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines())
        + "\n",
        encoding="utf-8",
    )
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
    config_path = args.config if args.config.is_absolute() else ROOT / args.config
    config = load_json(config_path)
    producer_path = REPOSITORY / config["sourceCertificates"]["producer"]
    independent_path = REPOSITORY / config["sourceCertificates"]["independent"]
    producer = load_json(producer_path)
    independent = load_json(independent_path)
    if not producer["allPassed"] or not independent["allPassed"]:
        raise RuntimeError("source certificate did not pass")
    log("figure-build-start")
    rows, results = build_rows(config, producer)
    results["sourceStatus"]["independentAllPassed"] = bool(independent["allPassed"])
    write_data(rows, results)
    log("figure-data-complete", rowCount=len(rows))
    render(rows, config)
    metadata = {
        "schemaVersion": "r072b-figure-data-metadata-v1",
        "generatedAt": datetime.now(TIMEZONE).isoformat(timespec="seconds"),
        "sourceFiles": [
            {"path": str(path.relative_to(REPOSITORY)), "sha256": sha256(path)}
            for path in (producer_path, independent_path)
        ],
        "dataFiles": {
            name: sha256(ROOT / name) for name in ("data.csv", "results.json")
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
    print(f"figure build passed in {elapsed:.2f}s; rows={len(rows)}")


if __name__ == "__main__":
    main()
