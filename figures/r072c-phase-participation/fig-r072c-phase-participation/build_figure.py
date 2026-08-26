#!/usr/bin/env python3
"""Build data and render the formal R0.72C phase-participation figure."""

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


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def log(stage: str, **fields: object) -> None:
    payload = {
        "timestamp": datetime.now(TIMEZONE).isoformat(timespec="milliseconds"),
        "stage": stage,
        **fields,
    }
    with (ROOT / "progress.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, sort_keys=True) + "\n")


def sum_of_squares(count: int) -> int:
    return count * (count + 1) * (2 * count + 1) // 6


def coherent_prefactor(count: int) -> float:
    """Exact equal-modulus coherent Phi at K_z=1 and A_0=0."""
    carrier_sum = sum_of_squares(count)
    return (
        2.0 ** (-1.0 / 3.0)
        * count ** (2.0 / 3.0)
        * carrier_sum ** (-4.0 / 3.0)
    )


def rudin_shapiro_prefactor(count: int) -> float:
    """Exact odd-generation Rudin--Shapiro Phi at K_z=1 and A_0=0."""
    carrier_sum = sum_of_squares(count)
    return 0.5 * (count / carrier_sum) ** (4.0 / 3.0)


def relative_defect(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def certificate_cross_audit(
    producer: dict[str, object], independent: dict[str, object]
) -> dict[str, object]:
    producer_rows = producer["rudinShapiro"]["oddGenerationExactFamily"]["rows"]
    producer_defects = [
        relative_defect(
            float(row["Phi"]), rudin_shapiro_prefactor(int(row["M"]))
        )
        for row in producer_rows
    ]

    independent_rows = independent["rudinShapiro"]["rows"]
    independent_defects: list[float] = []
    inferred_kz_values: list[float] = []
    for row in independent_rows:
        count = int(row["M"])
        inferred_kz = math.sqrt(float(row["rhoSquared"]) / (2.0 * count))
        inferred_kz_values.append(inferred_kz)
        normalized = float(row["normalizedGeometricPrefactor"]) / inferred_kz ** (
            2.0 / 3.0
        )
        independent_defects.append(
            relative_defect(normalized, rudin_shapiro_prefactor(count))
        )

    return {
        "producerRowCount": len(producer_rows),
        "producerMaximumRelativeDefect": max(producer_defects),
        "independentRowCount": len(independent_rows),
        "independentMaximumRelativeDefectAfterKzNormalization": max(
            independent_defects
        ),
        "independentInferredKzMinimum": min(inferred_kz_values),
        "independentInferredKzMaximum": max(inferred_kz_values),
    }


def build_rows(
    config: dict[str, object],
    producer: dict[str, object],
    independent: dict[str, object],
) -> tuple[list[dict[str, object]], dict[str, object]]:
    rows: list[dict[str, object]] = []
    generations = [int(value) for value in config["carrierGenerations"]]
    counts = [1 << generation for generation in generations]

    coherent_constant = (81.0 / 2.0) ** (1.0 / 3.0)
    rudin_shapiro_constant = 3.0 ** (4.0 / 3.0) / 2.0
    for generation, count in zip(generations, counts, strict=True):
        carrier_sum = sum_of_squares(count)
        series_values = (
            (
                "coherent exact launch",
                coherent_prefactor(count),
                "exact formula",
                "2^(-1/3) M^(2/3) S_M^(-4/3)",
                "R0.72B coherent equal-modulus identity",
            ),
            (
                "Rudin-Shapiro exact launch",
                rudin_shapiro_prefactor(count),
                "exact formula",
                "(1/2)(M/S_M)^(4/3)",
                "R0.72C odd-generation endpoint identity",
            ),
            (
                "coherent asymptotic reference",
                coherent_constant * count ** (-10.0 / 3.0),
                "analytic power reference",
                "(81/2)^(1/3) M^(-10/3)",
                "reference slope only",
            ),
            (
                "Rudin-Shapiro asymptotic reference",
                rudin_shapiro_constant * count ** (-8.0 / 3.0),
                "analytic power reference",
                "3^(4/3) M^(-8/3)/2",
                "reference slope only",
            ),
        )
        for series, value, evidence, formula, note in series_values:
            rows.append(
                {
                    "panel": "A",
                    "series": series,
                    "x": count,
                    "y": value,
                    "xUnit": "carrier count M=2^n, odd n",
                    "yUnit": "Phi at Kz=1",
                    "evidence": evidence,
                    "formula": formula,
                    "source": "R0.72C theorem and deterministic certificates",
                    "note": f"n={generation}; S_M={carrier_sum}; {note}",
                }
            )

    phase = config["phaseGrid"]
    beta_grid = np.linspace(
        float(phase["betaMinimum"]),
        float(phase["betaMaximum"]),
        int(phase["points"]),
    )
    for beta in beta_grid:
        boundaries = (
            (
                "coherent exact launch",
                min(2.5, (10.0 + 3.0 * beta) / 7.0),
                "min(5/2,(10+3 beta)/7)",
                "M^-10/3 coherent prefactor",
            ),
            (
                "arbitrary-phase exact launch",
                min(2.0, (8.0 + 3.0 * beta) / 7.0),
                "min(2,(8+3 beta)/7)",
                "sharp phase-uniform M^-8/3 prefactor",
            ),
            (
                "fixed-positive-time tail",
                min(2.25, (9.0 + 3.0 * beta) / 7.0),
                "min(9/4,(9+3 beta)/7)",
                "M^-3 tail prefactor; excludes the pre-ledger",
            ),
        )
        for series, value, formula, note in boundaries:
            rows.append(
                {
                    "panel": "B",
                    "series": series,
                    "x": float(beta),
                    "y": float(value),
                    "xUnit": "beta in L=M^-beta",
                    "yUnit": "alpha in eta=M^alpha",
                    "evidence": "analytic sufficient boundary",
                    "formula": formula,
                    "source": "R0.72C power-law corollary",
                    "note": f"strict inequality below curve; {note}",
                }
            )

    cross_audit = certificate_cross_audit(producer, independent)
    results = {
        "schemaVersion": "r072c-figure-results-v1",
        "sourceStatus": {
            "producerAllPassed": bool(producer["allPassed"]),
            "independentAllPassed": bool(independent["allPassed"]),
        },
        "exactLaunchPrefactors": {
            "normalization": "Kz=1",
            "carrierSum": "S_M=M(M+1)(2M+1)/6",
            "coherentFormula": "2^(-1/3) M^(2/3) S_M^(-4/3)",
            "coherentPower": "-10/3",
            "coherentAsymptoticConstant": coherent_constant,
            "rudinShapiroFormula": "(1/2)(M/S_M)^(4/3)",
            "rudinShapiroPower": "-8/3",
            "rudinShapiroAsymptoticConstant": rudin_shapiro_constant,
            "generationCount": len(generations),
            "generations": generations,
        },
        "phaseBoundaries": {
            "coherentExactLaunch": "min(5/2,(10+3 beta)/7)",
            "arbitraryPhaseExactLaunch": "min(2,(8+3 beta)/7)",
            "fixedPositiveTimeTail": "min(9/4,(9+3 beta)/7)",
            "strictRegion": "alpha lies strictly below the displayed curve",
        },
        "certificateCrossAudit": cross_audit,
        "randomness": False,
        "regressionOrFittedMaximumUsed": False,
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
        "formula",
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


def configure(palette: dict[str, str]) -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 6.7,
            "axes.titlesize": 7.35,
            "axes.labelsize": 6.25,
            "xtick.labelsize": 5.35,
            "ytick.labelsize": 5.35,
            "legend.fontsize": 5.0,
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
            "svg.hashsalt": "r072c-phase-participation",
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


def render(rows: list[dict[str, object]], config: dict[str, object]) -> None:
    palette = config["palette"]
    configure(palette)
    figure_config = config["figure"]
    width = float(figure_config["widthMillimetres"]) / 25.4
    height = float(figure_config["heightMillimetres"]) / 25.4
    fig = plt.figure(figsize=(width, height), constrained_layout=False)
    grid = fig.add_gridspec(
        1,
        2,
        left=0.072,
        right=0.985,
        bottom=0.225,
        top=0.765,
        wspace=0.30,
        width_ratios=(1.08, 1.0),
    )
    axa, axb = [fig.add_subplot(grid[0, index]) for index in range(2)]

    fig.suptitle(
        "Physical phase participation and the carrier-prefactor boundary",
        x=0.072,
        y=0.955,
        ha="left",
        fontsize=10.0,
        fontweight="bold",
    )
    fig.text(
        0.072,
        0.895,
        r"Exact formulas  $\cdot$  odd Rudin--Shapiro generations  $\cdot$  strict sufficient regions  $\cdot$  no DNS",
        ha="left",
        fontsize=6.05,
        color=palette["gray"],
    )
    blossom(fig, palette)

    m_coherent, coherent = select(rows, "A", "coherent exact launch")
    m_rs, rudin_shapiro = select(rows, "A", "Rudin-Shapiro exact launch")
    m_coherent_ref, coherent_ref = select(
        rows, "A", "coherent asymptotic reference"
    )
    m_rs_ref, rudin_shapiro_ref = select(
        rows, "A", "Rudin-Shapiro asymptotic reference"
    )
    axa.plot(
        m_coherent,
        coherent,
        color=palette["blue"],
        linestyle="-",
        marker="o",
        markersize=3.0,
        markerfacecolor=palette["blue"],
        markeredgecolor=palette["paper"],
        markeredgewidth=0.4,
        label="coherent exact",
        zorder=4,
    )
    axa.plot(
        m_rs,
        rudin_shapiro,
        color=palette["ochre"],
        linestyle="--",
        marker="s",
        markersize=3.0,
        markerfacecolor=palette["paper"],
        markeredgecolor=palette["ochre"],
        markeredgewidth=0.7,
        label="Rudin--Shapiro exact",
        zorder=4,
    )
    axa.plot(
        m_coherent_ref,
        coherent_ref,
        color=palette["gray"],
        linestyle=(0, (1.4, 1.8)),
        linewidth=0.62,
        alpha=0.86,
        zorder=2,
    )
    axa.plot(
        m_rs_ref,
        rudin_shapiro_ref,
        color=palette["gray"],
        linestyle=(0, (4.0, 2.1)),
        linewidth=0.62,
        alpha=0.86,
        zorder=2,
    )
    axa.text(
        0.61,
        0.29,
        r"$M^{-10/3}$",
        transform=axa.transAxes,
        fontsize=5.4,
        color=palette["blue"],
        rotation=-27,
    )
    axa.text(
        0.65,
        0.54,
        r"$M^{-8/3}$",
        transform=axa.transAxes,
        fontsize=5.4,
        color=palette["ochre"],
        rotation=-22,
    )
    axa.set_xscale("log", base=2)
    axa.set_yscale("log")
    axa.set_xlim(1.55, 7.0e5)
    axa.set_ylim(7.0e-20, 0.65)
    axa.set_xticks([2, 32, 512, 8192, 131072, 524288])
    axa.set_xticklabels(["2", "32", "512", "8k", "131k", "524k"])
    axa.set_xlabel(r"carrier count $M=2^n$, odd $n$")
    axa.set_ylabel(r"normalized prefactor $\Phi_{0,M}$  ($K_z=1$)")
    axa.grid(True, which="major", color=palette["light"], linewidth=0.35)
    axa.grid(
        True,
        which="minor",
        axis="y",
        color=palette["light"],
        linewidth=0.2,
        alpha=0.4,
    )
    axa.legend(loc="lower left", frameon=False, handlelength=2.5)
    panel_title(axa, "A", "Exact-launch prefactors")

    beta_coherent, alpha_coherent = select(rows, "B", "coherent exact launch")
    beta_arbitrary, alpha_arbitrary = select(
        rows, "B", "arbitrary-phase exact launch"
    )
    beta_fixed, alpha_fixed = select(rows, "B", "fixed-positive-time tail")
    axb.plot(
        beta_coherent,
        alpha_coherent,
        color=palette["blue"],
        linestyle="-",
        marker="o",
        markevery=20,
        markersize=2.8,
        markerfacecolor=palette["blue"],
        markeredgecolor=palette["paper"],
        markeredgewidth=0.35,
        label=r"coherent exact  $p=10/3$",
    )
    axb.plot(
        beta_arbitrary,
        alpha_arbitrary,
        color=palette["ochre"],
        linestyle="--",
        marker="s",
        markevery=20,
        markersize=2.8,
        markerfacecolor=palette["paper"],
        markeredgecolor=palette["ochre"],
        markeredgewidth=0.7,
        label=r"arbitrary exact  $p=8/3$",
    )
    axb.plot(
        beta_fixed,
        alpha_fixed,
        color=palette["gray"],
        linestyle=":",
        marker="^",
        markevery=20,
        markersize=3.0,
        markerfacecolor="none",
        markeredgecolor=palette["ink"],
        markeredgewidth=0.65,
        label=r"positive-time tail  $p=3$",
    )
    axb.scatter(
        [0.0, 0.0, 0.0],
        [10.0 / 7.0, 8.0 / 7.0, 9.0 / 7.0],
        s=[15, 17, 16],
        marker="o",
        color=[palette["blue"], palette["ochre"], palette["gray"]],
        edgecolor=palette["paper"],
        linewidth=0.35,
        zorder=5,
    )
    axb.annotate(
        r"$10/7$",
        (0.0, 10.0 / 7.0),
        xytext=(5, 4),
        textcoords="offset points",
        fontsize=5.05,
        color=palette["blue"],
    )
    axb.annotate(
        r"$9/7$",
        (0.0, 9.0 / 7.0),
        xytext=(5, -1),
        textcoords="offset points",
        fontsize=5.05,
        color=palette["gray"],
    )
    axb.annotate(
        r"$8/7$",
        (0.0, 8.0 / 7.0),
        xytext=(5, -7),
        textcoords="offset points",
        fontsize=5.05,
        color=palette["ochre"],
    )
    axb.set_xlim(0.0, 4.0)
    axb.set_ylim(0.9, 2.68)
    axb.set_xticks([0, 1, 2, 3, 4])
    axb.set_yticks([1.0, 1.5, 2.0, 2.5])
    axb.set_xlabel(r"layer exponent $\beta$ in $L=M^{-\beta}$")
    axb.set_ylabel(r"boundary for coupling exponent $\alpha$")
    axb.grid(True, color=palette["light"], linewidth=0.35)
    axb.legend(loc="lower right", frameon=False, handlelength=2.5)
    panel_title(axb, "B", "Strict sufficient regions")

    fig.text(
        0.072,
        0.092,
        "Analytic formulas + two deterministic audits. Prefactor sharpness is algebraic, not root-ledger saturation; burn-in controls only the tail.",
        ha="left",
        fontsize=5.05,
        color=palette["gray"],
    )
    fig.text(
        0.985,
        0.092,
        "R0.72C-1",
        ha="right",
        fontsize=5.2,
        color=palette["gray"],
    )

    output_stem = ROOT / "figure"
    fig.savefig(output_stem.with_suffix(".pdf"), bbox_inches=None)
    svg_path = output_stem.with_suffix(".svg")
    fig.savefig(svg_path, bbox_inches=None)
    svg_path.write_text(
        "\n".join(
            line.rstrip()
            for line in svg_path.read_text(encoding="utf-8").splitlines()
        )
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
    if not bool(producer["allPassed"]) or not bool(independent["allPassed"]):
        raise RuntimeError("source certificate did not pass")

    (ROOT / "progress.ndjson").write_text("", encoding="utf-8")
    log("figure-build-start", randomness=False)
    rows, results = build_rows(config, producer, independent)
    write_data(rows, results)
    log("figure-data-complete", rowCount=len(rows))
    render(rows, config)
    log("figure-render-complete", outputs=["figure.pdf", "figure.svg", "figure.png"])

    metadata = {
        "schemaVersion": "r072c-figure-data-metadata-v1",
        "generatedAt": datetime.now(TIMEZONE).isoformat(timespec="seconds"),
        "sourceFiles": [
            {"path": str(path.relative_to(REPOSITORY)), "sha256": sha256(path)}
            for path in (producer_path, independent_path)
        ],
        "dataFiles": {
            name: sha256(ROOT / name) for name in ("data.csv", "results.json")
        },
        "rowCount": len(rows),
        "randomness": False,
        "claimBoundary": load_json(ROOT / "contract.json")["claimBoundary"],
    }
    (ROOT / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    elapsed = time.perf_counter() - started
    log("figure-build-complete", elapsedSeconds=elapsed)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    resource_payload = {
        "timestamp": datetime.now(TIMEZONE).isoformat(timespec="milliseconds"),
        "stage": "figure-build-complete",
        "elapsedSeconds": elapsed,
        "processUserCpuSeconds": usage.ru_utime,
        "processSystemCpuSeconds": usage.ru_stime,
        "maximumResidentSetRaw": usage.ru_maxrss,
        "randomness": False,
        "dgx": False,
        "gpu": False,
    }
    (ROOT / "resource-log.ndjson").write_text(
        json.dumps(resource_payload, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"figure build passed in {elapsed:.2f}s; rows={len(rows)}")


if __name__ == "__main__":
    main()
