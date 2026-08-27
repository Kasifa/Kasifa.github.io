#!/usr/bin/env python3
"""Build the formal R0.72E fixed-q0 supercritical-ledger figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import resource
import time
from typing import Any, Sequence
from zoneinfo import ZoneInfo

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
TIMEZONE = ZoneInfo("Asia/Shanghai")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def timestamp() -> str:
    return datetime.now(TIMEZONE).isoformat(timespec="milliseconds")


def peak_rss_bytes() -> int:
    raw = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return raw if platform.system() == "Darwin" else raw * 1024


class Monitor:
    def __init__(self) -> None:
        self.started_wall = time.perf_counter()
        self.started_cpu = time.process_time()
        (ROOT / "progress.ndjson").write_text("", encoding="utf-8")
        (ROOT / "resource-log.ndjson").write_text("", encoding="utf-8")

    @property
    def elapsed(self) -> float:
        return time.perf_counter() - self.started_wall

    def event(self, stage: str, **fields: object) -> None:
        now = timestamp()
        elapsed = self.elapsed
        progress_row = {
            "timestamp": now,
            "stage": stage,
            "elapsedSeconds": elapsed,
            **fields,
        }
        with (ROOT / "progress.ndjson").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(progress_row, sort_keys=True) + "\n")

        cpu = time.process_time() - self.started_cpu
        resource_row = {
            "timestamp": now,
            "stage": stage,
            "elapsedSeconds": elapsed,
            "processCpuSeconds": cpu,
            "averageCpuPercentOfOneCore": 100.0 * cpu / max(elapsed, 1.0e-12),
            "peakRssBytes": peak_rss_bytes(),
            "logicalCpuCount": os.cpu_count(),
            "gpu": False,
            "dgx": False,
            **fields,
        }
        with (ROOT / "resource-log.ndjson").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(resource_row, sort_keys=True) + "\n")
        print(f"[{now}] {stage} | elapsed={elapsed:.2f}s", flush=True)


def log_fit(xs: Sequence[float], ys: Sequence[float]) -> dict[str, float]:
    log_x = np.log(np.asarray(xs, dtype=float))
    log_y = np.log(np.asarray(ys, dtype=float))
    slope, intercept = np.polyfit(log_x, log_y, 1)
    prediction = slope * log_x + intercept
    residual = log_y - prediction
    centered = log_y - np.mean(log_y)
    denominator = float(np.dot(centered, centered))
    r_squared = 1.0 - float(np.dot(residual, residual)) / denominator
    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "rSquared": r_squared,
    }


def require_exact_grid(actual: Sequence[int], expected: Sequence[int], label: str) -> None:
    if list(actual) != list(expected):
        raise RuntimeError(f"{label} grid mismatch: {list(actual)} != {list(expected)}")


def row(
    panel: str,
    series: str,
    x: float,
    y: float,
    raw_value: float,
    normalization: str,
    evidence: str,
    source: str,
    pointer: str,
    note: str,
) -> dict[str, object]:
    return {
        "panel": panel,
        "series": series,
        "x": x,
        "y": y,
        "rawValue": raw_value,
        "normalization": normalization,
        "evidence": evidence,
        "source": source,
        "sourcePointer": pointer,
        "note": note,
    }


def rows_and_results(
    config: dict[str, Any],
    producer: dict[str, Any],
    independent: dict[str, Any],
) -> tuple[list[dict[str, object]], dict[str, Any]]:
    expected = config["expected"]
    expected_r = [int(value) for value in expected["besselR"]]
    expected_producer_delta = [
        int(value) for value in expected["producerActionDeltas"]
    ]
    expected_independent_delta = [
        int(value) for value in expected["independentActionDeltas"]
    ]

    if int(producer["configuration"]["q0"]) != 4:
        raise RuntimeError("producer q0 is not 4")
    if int(independent["configuration"]["q0"]) != 4:
        raise RuntimeError("independent q0 is not 4")
    producer_passed = bool(
        producer["status"] == "passed"
        and producer["allRequiredChecksPassed"]
        and producer["defaultGridComplete"]
    )
    independent_passed = bool(
        independent["allPassed"] and not independent.get("smokeMode", False)
    )
    if not producer_passed or not independent_passed:
        raise RuntimeError("both full R0.72E certificates must pass")

    rows: list[dict[str, object]] = []

    producer_bessel = producer["bessel"]["prefixRows"]
    independent_roots = independent["rootFiniteLattice"]
    require_exact_grid(
        [int(item["R"]) for item in producer_bessel], expected_r, "producer Bessel"
    )
    require_exact_grid(
        [int(item["R"]) for item in independent_roots], expected_r, "independent roots"
    )
    for index, item in enumerate(producer_bessel):
        r_value = int(item["R"])
        rows.append(
            row(
                "A",
                "producer frozen Bessel mass",
                r_value,
                float(item["massOverLogR"]),
                float(item["selectedSlopeMass"]),
                "G_R^frozen/log(R)",
                "direct Bessel zeros and slopes",
                config["sourceCertificates"]["producer"],
                f"bessel.prefixRows[{index}]",
                "frozen slope mass; finite R",
            )
        )
    for index, item in enumerate(independent_roots):
        r_value = int(item["R"])
        exact_mass = float(item["exactSelectedMass"])
        rows.append(
            row(
                "A",
                "independent dissipative-root mass",
                r_value,
                exact_mass / math.log(r_value),
                exact_mass,
                "G_R^exact/log(R)",
                "independent fixed-step RK4 root scan",
                config["sourceCertificates"]["independent"],
                f"rootFiniteLattice[{index}]",
                f"relative frozen-mass defect={item['relativeMassDifference']:.6e}",
            )
        )
    mass_target = 8.0 / math.pi**2
    for r_value in (expected_r[0], expected_r[-1]):
        rows.append(
            row(
                "A",
                "analytic 8/pi^2 reference",
                r_value,
                mass_target,
                mass_target,
                "8/pi^2",
                "analytic Bessel asymptotic coefficient",
                "R0.72E analytic ledger",
                "equation (2.10)",
                "reference level; not a regression fit",
            )
        )

    producer_action = producer["negativeSobolevAction"]["rows"]
    independent_action = independent["actionFiniteLattice"]
    require_exact_grid(
        [int(item["delta"]) for item in producer_action],
        expected_producer_delta,
        "producer action",
    )
    require_exact_grid(
        [int(item["delta"]) for item in independent_action],
        expected_independent_delta,
        "independent action",
    )
    producer_x = float(producer["configuration"]["xMax"])
    independent_x = float(independent["configuration"]["actionFinalX"])
    for index, item in enumerate(producer_action):
        delta = float(item["delta"])
        q_value = float(item["Q"])
        rows.append(
            row(
                "B",
                "producer split-step action",
                delta,
                delta * q_value / math.log(delta),
                q_value,
                "Q_X/[(log(delta))/delta]",
                "fine split-step Fourier action",
                config["sourceCertificates"]["producer"],
                f"negativeSobolevAction.rows[{index}]",
                f"X={producer_x:g}; fine/coarse={item['fineCoarseRelativeDifference']:.3e}",
            )
        )
    for index, item in enumerate(independent_action):
        delta = float(item["delta"])
        q_value = float(item["actionFine"])
        rows.append(
            row(
                "B",
                "independent BDF action",
                delta,
                delta * q_value / math.log(delta),
                q_value,
                "Q_X/[(log(delta))/delta]",
                "independent BDF and composite Simpson action",
                config["sourceCertificates"]["independent"],
                f"actionFiniteLattice[{index}]",
                f"X={independent_x:g}; quadrature={item['quadratureRelativeDefect']:.3e}",
            )
        )

    producer_ledger = producer["physicalLedger"]["rows"]
    independent_ledger = independent["physicalLedger"]["rootLedgers"]
    require_exact_grid(
        [int(item["R"]) for item in producer_ledger], expected_r, "producer ledger"
    )
    require_exact_grid(
        [int(item["R"]) for item in independent_ledger],
        expected_r,
        "independent ledger",
    )
    producer_ratio_0 = float(
        producer_ledger[0]["rootLedgerScaling"]["besselWeightedRatioProxy"]
    )
    independent_ratio_0 = float(independent_ledger[0]["ledgerOverDOneThird"])
    producer_ratios: list[float] = []
    independent_ratios: list[float] = []
    for index, item in enumerate(producer_ledger):
        r_value = int(item["R"])
        raw_ratio = float(item["rootLedgerScaling"]["besselWeightedRatioProxy"])
        producer_ratios.append(raw_ratio)
        rows.append(
            row(
                "C",
                "producer selected-ledger proxy",
                r_value,
                raw_ratio / producer_ratio_0,
                raw_ratio,
                "(S^2 G_R^frozen/D^(1/3)) / value_at_R=8",
                "producer raw-amplitude and frozen-mass ledger",
                config["sourceCertificates"]["producer"],
                f"physicalLedger.rows[{index}].rootLedgerScaling",
                "bounded Lambda1 and fixed multiplier constant omitted",
            )
        )
    for index, item in enumerate(independent_ledger):
        r_value = int(item["R"])
        raw_ratio = float(item["ledgerOverDOneThird"])
        independent_ratios.append(raw_ratio)
        rows.append(
            row(
                "C",
                "independent selected-ledger lower bound",
                r_value,
                raw_ratio / independent_ratio_0,
                raw_ratio,
                "(selected exact-root ledger/D^(1/3)) / value_at_R=8",
                "independent evolved roots and exact full Y at each root",
                config["sourceCertificates"]["independent"],
                f"physicalLedger.rootLedgers[{index}]",
                "complete nonnegative ledger is at least the selected ledger",
            )
        )
    for r_value in expected_r:
        reference = (r_value / expected_r[0]) ** (4.0 / 3.0)
        rows.append(
            row(
                "C",
                "analytic R^(4/3) reference",
                r_value,
                reference,
                reference,
                "(R/8)^(4/3)",
                "exact exponent ledger",
                "R0.72E analytic ledger",
                "Theorem 7.1 power ledger",
                "reference power; not a regression fit",
            )
        )

    shared_action_deltas = sorted(
        set(expected_producer_delta).intersection(expected_independent_delta)
    )
    producer_action_map = {
        int(item["delta"]): float(item["Q"]) for item in producer_action
    }
    independent_action_map = {
        int(item["delta"]): float(item["actionFine"])
        for item in independent_action
    }
    horizon_order_defects = [
        producer_action_map[value] - independent_action_map[value]
        for value in shared_action_deltas
    ]
    frozen_mass_defects = [
        abs(float(left["selectedSlopeMass"]) - float(right["besselMass"]))
        for left, right in zip(producer_bessel, independent_roots, strict=True)
    ]
    producer_action_normalized = [
        float(item["delta"]) * float(item["Q"]) / math.log(float(item["delta"]))
        for item in producer_action
    ]
    independent_action_normalized = [
        float(item["delta"])
        * float(item["actionFine"])
        / math.log(float(item["delta"]))
        for item in independent_action
    ]
    producer_fit = log_fit(expected_r, producer_ratios)
    independent_fit = log_fit(expected_r, independent_ratios)
    panel_counts = {
        panel: sum(item["panel"] == panel for item in rows)
        for panel in ("A", "B", "C")
    }
    results = {
        "schemaVersion": "r072e-figure-results-v1",
        "sourceStatus": {
            "producerPassed": producer_passed,
            "independentPassed": independent_passed,
            "producerDefaultGridComplete": bool(producer["defaultGridComplete"]),
            "independentSmokeMode": bool(independent.get("smokeMode", False)),
        },
        "panels": {
            "A": {
                "RValues": expected_r,
                "targetEightOverPiSquared": mass_target,
                "producerMassOverLogR": [
                    float(item["massOverLogR"]) for item in producer_bessel
                ],
                "independentMassOverLogR": [
                    float(item["exactSelectedMass"]) / math.log(float(item["R"]))
                    for item in independent_roots
                ],
                "maximumFrozenMassCopyDefect": max(frozen_mass_defects),
                "terminalIndependentRelativeFrozenMassDefect": float(
                    independent_roots[-1]["relativeMassDifference"]
                ),
            },
            "B": {
                "producerFinalX": producer_x,
                "independentFinalX": independent_x,
                "producerDeltas": expected_producer_delta,
                "independentDeltas": expected_independent_delta,
                "producerNormalizedAction": producer_action_normalized,
                "independentNormalizedAction": independent_action_normalized,
                "sharedDeltaHorizonOrderDifferences": horizon_order_defects,
                "comparisonBoundary": (
                    "Producer Q(0,6) and independent Q(0,1) are separate finite-"
                    "window sequences, not same-endpoint replications."
                ),
            },
            "C": {
                "RValues": expected_r,
                "producerRawRatios": producer_ratios,
                "independentRawRatios": independent_ratios,
                "producerRExponentFit": producer_fit,
                "independentRExponentFit": independent_fit,
                "analyticReferenceExponent": 4.0 / 3.0,
                "normalizationR": expected_r[0],
                "completeLedgerRelation": (
                    "complete nonnegative ledger >= selected-root ledger"
                ),
            },
        },
        "rowCount": len(rows),
        "panelCounts": panel_counts,
        "randomness": False,
        "regressionUsedForPlottedClaim": False,
        "finiteFitsAreDiagnostics": True,
    }
    return rows, results


def write_data(rows: list[dict[str, object]], results: dict[str, Any]) -> None:
    fields = [
        "panel",
        "series",
        "x",
        "y",
        "rawValue",
        "normalization",
        "evidence",
        "source",
        "sourcePointer",
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
    rows: list[dict[str, object]], panel: str, series_name: str
) -> tuple[np.ndarray, np.ndarray]:
    selected = sorted(
        (
            item
            for item in rows
            if item["panel"] == panel and item["series"] == series_name
        ),
        key=lambda item: float(item["x"]),
    )
    return (
        np.asarray([float(item["x"]) for item in selected]),
        np.asarray([float(item["y"]) for item in selected]),
    )


def configure(palette: dict[str, str]) -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 6.2,
            "axes.titlesize": 6.7,
            "axes.labelsize": 5.7,
            "xtick.labelsize": 4.9,
            "ytick.labelsize": 4.9,
            "legend.fontsize": 4.35,
            "axes.edgecolor": palette["ink"],
            "axes.labelcolor": palette["ink"],
            "text.color": palette["ink"],
            "xtick.color": palette["ink"],
            "ytick.color": palette["ink"],
            "axes.facecolor": palette["paper"],
            "figure.facecolor": palette["paper"],
            "savefig.facecolor": palette["paper"],
            "axes.linewidth": 0.62,
            "lines.linewidth": 1.0,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "r072e-supercritical-ledger",
        }
    )


def blossom(fig: plt.Figure, palette: dict[str, str]) -> None:
    center_x, center_y = 0.978, 0.952
    colors = (
        palette["navy"],
        palette["rust"],
        palette["gray"],
        palette["navy"],
        palette["rust"],
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


def common_axes(ax: plt.Axes, palette: dict[str, str]) -> None:
    ax.grid(True, color=palette["light"], linewidth=0.34, zorder=0)
    ax.tick_params(width=0.55, length=2.2, pad=1.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def plot_certificate_series(
    ax: plt.Axes,
    x: np.ndarray,
    y: np.ndarray,
    label: str,
    color: str,
    independent: bool,
) -> None:
    ax.plot(
        x,
        y,
        color=color,
        linestyle="--" if independent else "-",
        marker="s" if independent else "o",
        markersize=3.0,
        markerfacecolor="white" if independent else color,
        markeredgecolor=color,
        markeredgewidth=0.65,
        label=label,
        zorder=4,
    )


def render(
    rows: list[dict[str, object]],
    results: dict[str, Any],
    config: dict[str, Any],
) -> None:
    palette = config["palette"]
    configure(palette)
    figure_config = config["figure"]
    width = float(figure_config["widthMillimetres"]) / 25.4
    height = float(figure_config["heightMillimetres"]) / 25.4
    fig = plt.figure(figsize=(width, height), constrained_layout=False)
    grid = fig.add_gridspec(
        1,
        3,
        left=0.068,
        right=0.987,
        bottom=0.225,
        top=0.765,
        wspace=0.39,
        width_ratios=(1.0, 1.03, 1.0),
    )
    axa, axb, axc = [fig.add_subplot(grid[0, index]) for index in range(3)]

    fig.suptitle(
        "Finite diagnostics for the R0.72E supercritical ledger",
        x=0.068,
        y=0.955,
        ha="left",
        fontsize=9.5,
        fontweight="bold",
    )
    fig.text(
        0.068,
        0.895,
        r"fixed $q_0=4$  $\cdot$  deterministic binary64 certificates  $\cdot$  finite audit, not proof",
        ha="left",
        fontsize=5.55,
        color=palette["gray"],
    )
    blossom(fig, palette)

    x_p, y_p = select(rows, "A", "producer frozen Bessel mass")
    x_i, y_i = select(rows, "A", "independent dissipative-root mass")
    x_ref, y_ref = select(rows, "A", "analytic 8/pi^2 reference")
    plot_certificate_series(axa, x_p, y_p, "frozen Bessel", palette["navy"], False)
    plot_certificate_series(
        axa, x_i, y_i, "dissipative roots", palette["rust"], True
    )
    axa.plot(
        x_ref,
        y_ref,
        color=palette["ink"],
        linestyle=(0, (2, 2)),
        linewidth=0.60,
        label=r"$8/\pi^2$",
        zorder=2,
    )
    axa.set_xscale("log", base=2)
    axa.set_xlim(7.2, 71)
    axa.set_ylim(0.79, 0.96)
    axa.set_xticks(x_p)
    axa.set_xticklabels([str(int(value)) for value in x_p])
    axa.set_yticks([0.80, 0.84, 0.88, 0.92, 0.96])
    axa.set_xlabel(r"selected-root count $R$  (log base 2)")
    axa.set_ylabel(r"selected slope mass $/\log R$")
    axa.set_title("A   Bessel mass coefficient", loc="left", fontweight="bold")
    axa.legend(loc="upper right", frameon=False, handlelength=2.0, labelspacing=0.24)
    common_axes(axa, palette)

    x_p, y_p = select(rows, "B", "producer split-step action")
    x_i, y_i = select(rows, "B", "independent BDF action")
    plot_certificate_series(
        axb, x_p, y_p, r"split-step, $X=6$", palette["navy"], False
    )
    plot_certificate_series(axb, x_i, y_i, r"BDF, $X=1$", palette["rust"], True)
    axb.set_xscale("log", base=2)
    axb.set_xlim(14.0, 570.0)
    axb.set_ylim(7.35, 8.25)
    axb.set_xticks(x_p)
    axb.set_xticklabels([str(int(value)) for value in x_p], rotation=0)
    axb.set_yticks([7.4, 7.6, 7.8, 8.0, 8.2])
    axb.set_xlabel(r"coupling $\delta$  (log base 2)")
    axb.set_ylabel(r"$\delta Q_X/\log\delta$")
    axb.set_title("B   Negative-Sobolev action", loc="left", fontweight="bold")
    axb.legend(loc="lower right", frameon=False, handlelength=2.0, labelspacing=0.24)
    axb.text(
        0.03,
        0.955,
        "different finite horizons",
        transform=axb.transAxes,
        va="top",
        fontsize=4.35,
        color=palette["gray"],
    )
    common_axes(axb, palette)

    x_p, y_p = select(rows, "C", "producer selected-ledger proxy")
    x_i, y_i = select(rows, "C", "independent selected-ledger lower bound")
    x_ref, y_ref = select(rows, "C", "analytic R^(4/3) reference")
    plot_certificate_series(axc, x_p, y_p, "frozen-mass proxy", palette["navy"], False)
    plot_certificate_series(axc, x_i, y_i, "exact-root lower bound", palette["rust"], True)
    axc.plot(
        x_ref,
        y_ref,
        color=palette["ink"],
        linestyle=(0, (2, 2)),
        linewidth=0.70,
        label=r"$(R/8)^{4/3}$",
        zorder=2,
    )
    axc.set_xscale("log", base=2)
    axc.set_yscale("log", base=2)
    axc.set_xlim(7.2, 71)
    axc.set_ylim(0.82, 19.5)
    axc.set_xticks(x_p)
    axc.set_xticklabels([str(int(value)) for value in x_p])
    axc.set_yticks([1, 2, 4, 8, 16])
    axc.set_yticklabels(["1", "2", "4", "8", "16"])
    axc.set_xlabel(r"selected-root count $R$  (log base 2)")
    axc.set_ylabel(r"ledger ratio $/$ value at $R=8$")
    axc.set_title("C   Ledger lower-bound growth", loc="left", fontweight="bold")
    axc.legend(loc="upper left", frameon=False, handlelength=2.0, labelspacing=0.22)
    producer_slope = results["panels"]["C"]["producerRExponentFit"]["slope"]
    independent_slope = results["panels"]["C"]["independentRExponentFit"]["slope"]
    axc.text(
        0.97,
        0.055,
        f"finite slopes {producer_slope:.3f} / {independent_slope:.3f}",
        transform=axc.transAxes,
        ha="right",
        fontsize=4.35,
        color=palette["gray"],
    )
    common_axes(axc, palette)

    fig.text(
        0.068,
        0.083,
        (
            "Finite audits only: selected roots give a complete-ledger lower-bound "
            "mechanism; bounded Lambda1 is omitted. No regularity or Millennium claim."
        ),
        ha="left",
        fontsize=4.55,
        color=palette["gray"],
    )
    fig.text(0.987, 0.083, "R0.72E-1", ha="right", fontsize=4.9, color=palette["gray"])

    creator = "R0.72E deterministic figure workflow"
    fixed_pdf_time = datetime(2026, 8, 27, tzinfo=TIMEZONE)
    pdf_metadata = {
        "Creator": creator,
        "CreationDate": fixed_pdf_time,
        "ModDate": fixed_pdf_time,
    }
    svg_metadata = {"Creator": creator, "Date": None}
    output = ROOT / "figure"
    fig.savefig(
        output.with_suffix(".pdf"), metadata=pdf_metadata, bbox_inches=None
    )
    svg_path = output.with_suffix(".svg")
    fig.savefig(svg_path, metadata=svg_metadata, bbox_inches=None)
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )
    fig.savefig(
        output.with_suffix(".png"),
        dpi=int(figure_config["pngDpi"]),
        metadata={"Software": "R0.72E deterministic figure workflow"},
        bbox_inches=None,
    )
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "config.json")
    parser.add_argument(
        "--data-only",
        action="store_true",
        help="prepare CSV/results/lineage without creating PDF, SVG, or PNG",
    )
    args = parser.parse_args()
    config_path = args.config if args.config.is_absolute() else Path.cwd() / args.config
    if not config_path.exists():
        config_path = ROOT / args.config
    config = load_json(config_path)
    producer_path = REPOSITORY / config["sourceCertificates"]["producer"]
    independent_path = REPOSITORY / config["sourceCertificates"]["independent"]
    for path in (producer_path, independent_path):
        if not path.exists():
            raise FileNotFoundError(f"required certificate has not landed: {path}")

    monitor = Monitor()
    monitor.event("figure-build-start", randomness=False, q0=4)
    producer = load_json(producer_path)
    independent = load_json(independent_path)
    rows, results = rows_and_results(config, producer, independent)
    write_data(rows, results)
    monitor.event(
        "figure-data-complete",
        rowCount=len(rows),
        panelCounts=results["panelCounts"],
    )
    if args.data_only:
        monitor.event("figure-render-skipped", reason="--data-only")
    else:
        render(rows, results, config)
        monitor.event(
            "figure-render-complete",
            outputs=["figure.pdf", "figure.svg", "figure.png"],
        )

    contract_path = ROOT / "contract.json"
    source_paths = (producer_path, independent_path, contract_path, config_path)
    metadata = {
        "schemaVersion": "r072e-figure-data-metadata-v1",
        "generatedAt": datetime.now(TIMEZONE).isoformat(timespec="seconds"),
        "sourceFiles": [
            {"path": str(path.relative_to(REPOSITORY)), "sha256": sha256(path)}
            for path in source_paths
        ],
        "dataFiles": {
            name: sha256(ROOT / name) for name in ("data.csv", "results.json")
        },
        "rowCount": len(rows),
        "panelCounts": results["panelCounts"],
        "randomness": False,
        "claimBoundary": load_json(contract_path)["claimBoundary"],
    }
    (ROOT / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    environment = (
        f"generatedAt={datetime.now(TIMEZONE).isoformat(timespec='seconds')}\n"
        f"python={platform.python_version()}\n"
        f"platform={platform.platform()}\n"
        f"numpy={np.__version__}\n"
        f"matplotlib={mpl.__version__}\n"
        f"logicalCpuCount={os.cpu_count()}\n"
        "randomness=false\nintervalArithmetic=false\ngpu=false\ndgx=false\n"
    )
    (ROOT / "environment.txt").write_text(environment, encoding="utf-8")
    final_stage = "figure-data-only-complete" if args.data_only else "figure-build-complete"
    monitor.event(final_stage, elapsedSeconds=monitor.elapsed)
    action = "data preparation" if args.data_only else "figure build"
    print(f"R0.72E {action} passed in {monitor.elapsed:.2f}s; rows={len(rows)}")


if __name__ == "__main__":
    main()
