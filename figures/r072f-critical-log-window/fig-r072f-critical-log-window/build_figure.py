#!/usr/bin/env python3
"""Build the formal R0.72F critical-log-window figure package."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
import numpy as np


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )


def write_ndjson(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def require_exact_grid(values: list[int], expected: list[int], label: str) -> None:
    if values != expected:
        raise RuntimeError(f"{label} grid {values} != expected {expected}")


def chart_row(
    panel: str,
    series: str,
    x: float,
    y: float,
    raw_value: object,
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


def prepare_data(
    producer: dict[str, Any],
    independent: dict[str, Any],
    config: dict[str, Any],
) -> tuple[list[dict[str, object]], dict[str, Any]]:
    if not producer.get("allRequiredChecksPassed"):
        raise RuntimeError("producer certificate did not pass")
    if not independent.get("allRequiredChecksPassed"):
        raise RuntimeError("independent certificate did not pass")
    expected_deltas = [int(value) for value in config["expected"]["deltas"]]
    producer_rows = producer["weightedActionRows"]
    independent_rows = independent["weightedActionRows"]
    require_exact_grid(
        [int(item["delta"]) for item in producer_rows],
        expected_deltas,
        "producer",
    )
    require_exact_grid(
        [int(item["delta"]) for item in independent_rows],
        expected_deltas,
        "independent",
    )

    beta_critical = float(config["expected"]["criticalBeta"])
    gamma_critical = float(config["expected"]["criticalGamma"])
    beta_leray = float(config["expected"]["lerayBeta"])
    rows: list[dict[str, object]] = []

    # Panel A contains exact analytic boundary data, not sampled numerics.
    region_corners = (
        (beta_critical, 0.0),
        (beta_leray, 0.0),
        (beta_leray, 2.0),
        (beta_critical, 2.0),
    )
    for index, (beta, gamma) in enumerate(region_corners):
        rows.append(
            chart_row(
                "A",
                "admissible interior closure",
                beta,
                gamma,
                f"({beta:.16g},{gamma:.16g})",
                "closure used only to draw 1/3 < beta < 1/2",
                "R0.72F analytic screen",
                "research/r072f_report-source.md",
                f"regionCorner[{index}]",
                "open beta boundaries are drawn separately",
            )
        )
    for gamma in (gamma_critical, 2.0):
        rows.append(
            chart_row(
                "A",
                "included critical endpoint ray",
                beta_critical,
                gamma,
                gamma,
                "beta=1/3 and gamma>=1",
                "R0.72F selected-family exponent ledger",
                "research/r072f_report-source.md",
                "critical endpoint ray",
                "included only for gamma>=1",
            )
        )
    for gamma in (0.0, 2.0):
        rows.append(
            chart_row(
                "A",
                "excluded Leray boundary",
                beta_leray,
                gamma,
                gamma,
                "beta=1/2",
                "R0.72F Leray energy-payment screen",
                "research/r072f_report-source.md",
                "energy boundary",
                "excluded for gamma>=0",
            )
        )
    rows.extend(
        (
            chart_row(
                "A",
                "critical-log endpoint",
                beta_critical,
                gamma_critical,
                "(1/3,1)",
                "minimal selected-family power-log endpoint",
                "R0.72F analytic screen",
                "research/r072f_report-source.md",
                "critical endpoint",
                "passes both displayed screens",
            ),
            chart_row(
                "A",
                "plain endpoint failure",
                beta_critical,
                0.0,
                "(1/3,0)",
                "plain beta=1/3 endpoint",
                "R0.72F analytic screen",
                "research/r072f_report-source.md",
                "plain endpoint",
                "fails selected-family logarithmic test",
            ),
        )
    )

    producer_normalized: list[float] = []
    independent_normalized: list[float] = []
    producer_plain_ratio: list[float] = []
    independent_plain_ratio: list[float] = []
    for index, (left, right) in enumerate(zip(producer_rows, independent_rows, strict=True)):
        delta = float(left["delta"])
        if delta != float(right["delta"]):
            raise RuntimeError("certificate delta mismatch")
        producer_q = float(left["actions"]["critical-log"])
        independent_q = float(right["actions"]["critical-log"])
        producer_value = producer_q * delta ** (2.0 / 3.0) / math.log(delta)
        independent_value = (
            independent_q * delta ** (2.0 / 3.0) / math.log(delta)
        )
        producer_declared = float(
            left["asymptoticNormalizations"]["critical-log"]
        )
        independent_declared = float(
            right["asymptoticNormalizations"]["critical-log"]
        )
        if abs(producer_value - producer_declared) > 5.0e-14:
            raise RuntimeError("producer normalization does not reproduce")
        if abs(independent_value - independent_declared) > 5.0e-14:
            raise RuntimeError("independent normalization does not reproduce")
        producer_ratio = float(left["actions"]["plain-one-third"]) / producer_q
        independent_ratio = (
            float(right["actions"]["plain-one-third"]) / independent_q
        )
        producer_normalized.append(producer_value)
        independent_normalized.append(independent_value)
        producer_plain_ratio.append(producer_ratio)
        independent_plain_ratio.append(independent_ratio)
        rows.extend(
            (
                chart_row(
                    "B",
                    "producer critical-log normalization",
                    delta,
                    producer_value,
                    producer_q,
                    "Q_* delta^(2/3)/log(delta)",
                    "time-dependent Strang split-step Fourier",
                    config["sourceCertificates"]["producer"],
                    f"weightedActionRows[{index}]",
                    (
                        "fine/coarse relative difference="
                        f"{left['fineCoarseRelativeDifferences']['critical-log']:.6e}"
                    ),
                ),
                chart_row(
                    "B",
                    "independent critical-log normalization",
                    delta,
                    independent_value,
                    independent_q,
                    "Q_* delta^(2/3)/log(delta)",
                    "independent adaptive real-lattice BDF",
                    config["sourceCertificates"]["independent"],
                    f"weightedActionRows[{index}]",
                    (
                        "quadrature relative defect="
                        f"{right['quadratureRelativeDefects']['critical-log']:.6e}"
                    ),
                ),
                chart_row(
                    "B",
                    "producer plain-to-critical annotation",
                    delta,
                    producer_ratio,
                    float(left["actions"]["plain-one-third"]),
                    "Q_(1/3,0)/Q_*",
                    "same producer evolution and quadrature",
                    config["sourceCertificates"]["producer"],
                    f"weightedActionRows[{index}].actions",
                    "annotation only; not plotted on the main y-axis",
                ),
            )
        )

    declared_vertices = producer["frontier"]["vertices"]
    vertex_coordinates = {
        "critical-log-action": (0.5, math.sqrt(3.0) / 2.0),
        "explicit-coupling": (0.0, 0.0),
        "root-weight": (1.0, 0.0),
    }
    for index, item in enumerate(declared_vertices):
        name = str(item["name"])
        if name not in vertex_coordinates:
            raise RuntimeError(f"unexpected frontier vertex {name}")
        x, y = vertex_coordinates[name]
        rows.append(
            chart_row(
                "C",
                name,
                x,
                y,
                json.dumps(item, sort_keys=True),
                "barycentric repair coordinate at fixed a=1/3",
                "exact rational exponent ledger",
                config["sourceCertificates"]["producer"],
                f"frontier.vertices[{index}]",
                (
                    "changes LHS observable"
                    if name == "root-weight"
                    else "retains original selected-ledger LHS"
                ),
            )
        )

    relative_gaps = [
        abs(left - right) / max(abs(left), abs(right))
        for left, right in zip(
            producer_normalized, independent_normalized, strict=True
        )
    ]
    producer_l2 = next(
        item["value"]
        for item in producer["checks"]
        if item["name"] == "critical_weight_l2_identity"
    )
    results = {
        "schemaVersion": "r072f-figure-results-v1",
        "sourceStatus": {
            "producerPassed": bool(producer["allRequiredChecksPassed"]),
            "independentPassed": bool(independent["allRequiredChecksPassed"]),
            "independentImportsProducer": bool(
                independent["scope"]["importsProducer"]
            ),
            "independentReadsProducerOutput": bool(
                independent["scope"]["readsProducerOutput"]
            ),
        },
        "panels": {
            "A": {
                "admissibleInterior": "1/3 < beta < 1/2, gamma >= 0",
                "includedEndpointRay": "beta=1/3, gamma>=1",
                "excludedEnergyBoundary": "beta=1/2 for gamma>=0",
                "scope": "selected-family obstruction plus Leray energy payment only",
            },
            "B": {
                "deltas": expected_deltas,
                "producerCriticalNormalization": producer_normalized,
                "independentCriticalNormalization": independent_normalized,
                "producerPlainToCritical": producer_plain_ratio,
                "independentPlainToCritical": independent_plain_ratio,
                "producerSpread": max(producer_normalized) / min(producer_normalized),
                "independentSpread": max(independent_normalized)
                / min(independent_normalized),
                "maximumRelativeCrossAuditGap": max(relative_gaps),
                "producerCriticalWeightL2Squared": producer_l2,
                "independentCriticalWeightL2Squared": independent[
                    "criticalWeightL2"
                ]["value"],
            },
            "C": {
                "fixedA": "1/3",
                "frontierEquation": "2*a+c+beta+3*alpha/4=1",
                "vertices": declared_vertices,
                "rootAtomChangesLHS": True,
            },
        },
        "rowCount": len(rows),
        "panelCounts": {
            panel: sum(item["panel"] == panel for item in rows)
            for panel in ("A", "B", "C")
        },
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
            "font.size": 6.15,
            "axes.titlesize": 6.7,
            "axes.labelsize": 5.6,
            "xtick.labelsize": 4.9,
            "ytick.labelsize": 4.9,
            "legend.fontsize": 4.25,
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
            "hatch.linewidth": 0.38,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "r072f-critical-log-window",
        }
    )


def blossom(fig: plt.Figure, palette: dict[str, str]) -> None:
    center_x, center_y = 0.979, 0.953
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
                alpha=0.86,
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


def render(
    rows: list[dict[str, object]],
    results: dict[str, Any],
    config: dict[str, Any],
) -> None:
    palette = config["palette"]
    configure(palette)
    width = float(config["figure"]["widthMillimetres"]) / 25.4
    height = float(config["figure"]["heightMillimetres"]) / 25.4
    fig = plt.figure(figsize=(width, height), constrained_layout=False)
    grid = fig.add_gridspec(
        1,
        3,
        left=0.065,
        right=0.985,
        bottom=0.205,
        top=0.765,
        wspace=0.38,
        width_ratios=(1.02, 1.10, 1.03),
    )
    axa, axb, axc = [fig.add_subplot(grid[0, index]) for index in range(3)]

    fig.suptitle(
        "Critical-log initial-layer window and repair frontier",
        x=0.065,
        y=0.954,
        ha="left",
        fontsize=9.4,
        fontweight="bold",
    )
    fig.text(
        0.065,
        0.894,
        (
            r"selected-family screen  $\cdot$  shared $\delta=16,\ldots,512$ "
            r" $\cdot$  finite audit, not a regularity result"
        ),
        ha="left",
        fontsize=5.45,
        color=palette["gray"],
    )
    blossom(fig, palette)

    # Panel A: analytic window.
    beta0 = float(config["expected"]["criticalBeta"])
    beta1 = float(config["expected"]["lerayBeta"])
    gamma0 = float(config["expected"]["criticalGamma"])
    region = Polygon(
        [(beta0, 0.0), (beta1, 0.0), (beta1, 2.0), (beta0, 2.0)],
        closed=True,
        facecolor=palette["region"],
        edgecolor=palette["navy"],
        linewidth=0.0,
        hatch="////",
        alpha=0.72,
        zorder=1,
    )
    axa.add_patch(region)
    axa.plot(
        [beta0, beta0],
        [gamma0, 2.02],
        color=palette["navy"],
        linewidth=1.35,
        solid_capstyle="round",
        zorder=5,
    )
    axa.plot(
        [beta0, beta0],
        [-0.02, gamma0],
        color=palette["rust"],
        linewidth=0.82,
        linestyle=(0, (1.5, 1.5)),
        zorder=4,
    )
    axa.axvline(
        beta1,
        color=palette["ink"],
        linewidth=0.8,
        linestyle=(0, (3, 2)),
        zorder=4,
    )
    axa.scatter(
        [beta0],
        [gamma0],
        marker="*",
        s=48,
        facecolor=palette["rust"],
        edgecolor=palette["ink"],
        linewidth=0.45,
        zorder=7,
    )
    axa.scatter(
        [beta0],
        [0.0],
        marker="o",
        s=21,
        facecolor=palette["open"],
        edgecolor=palette["rust"],
        linewidth=0.9,
        zorder=7,
    )
    axa.text(
        0.405,
        1.53,
        "admissible\ninterior",
        ha="center",
        va="center",
        fontsize=5.0,
        color=palette["navy"],
        fontweight="bold",
    )
    axa.annotate(
        r"critical $(1/3,1)$",
        xy=(beta0, gamma0),
        xytext=(0.351, 0.79),
        fontsize=4.45,
        arrowprops={"arrowstyle": "-", "lw": 0.48, "color": palette["ink"]},
    )
    axa.annotate(
        "plain endpoint fails",
        xy=(beta0, 0.0),
        xytext=(0.354, 0.19),
        fontsize=4.35,
        color=palette["rust"],
        arrowprops={"arrowstyle": "-", "lw": 0.45, "color": palette["rust"]},
    )
    axa.text(
        beta1 + 0.004,
        1.03,
        r"Leray boundary $\beta=1/2$" + "\n(excluded)",
        rotation=90,
        va="center",
        fontsize=4.2,
        color=palette["gray"],
    )
    axa.set_xlim(0.285, 0.545)
    axa.set_ylim(-0.12, 2.08)
    axa.set_xticks([1.0 / 3.0, 0.4, 0.5])
    axa.set_xticklabels([r"$1/3$", "0.4", r"$1/2$"])
    axa.set_yticks([0, 1, 2])
    axa.set_xlabel(r"power exponent $\beta$")
    axa.set_ylabel(r"log exponent $\gamma$")
    axa.set_title("A   Two-screen window", loc="left", fontweight="bold")
    axa.text(
        0.02,
        0.98,
        "selected obstruction + energy payment",
        transform=axa.transAxes,
        va="top",
        fontsize=4.2,
        color=palette["gray"],
    )
    common_axes(axa, palette)

    # Panel B: two independently produced finite sequences.
    xp, yp = select(rows, "B", "producer critical-log normalization")
    xi, yi = select(rows, "B", "independent critical-log normalization")
    axb.plot(
        xi,
        yi,
        color=palette["rust"],
        linestyle="--",
        marker="s",
        markersize=3.35,
        markerfacecolor=palette["open"],
        markeredgecolor=palette["rust"],
        markeredgewidth=0.75,
        label="independent BDF",
        zorder=3,
    )
    axb.plot(
        xp,
        yp,
        color=palette["navy"],
        linestyle="-",
        marker="o",
        markersize=2.75,
        markerfacecolor=palette["navy"],
        markeredgecolor=palette["open"],
        markeredgewidth=0.35,
        label="split-step producer",
        zorder=5,
    )
    axb.set_xscale("log", base=2)
    axb.set_xlim(14.3, 574.0)
    axb.set_ylim(40.55, 44.72)
    axb.set_xticks(xp)
    axb.set_xticklabels([str(int(value)) for value in xp])
    axb.set_yticks([41, 42, 43, 44])
    axb.set_xlabel(r"coupling $\delta$  (log base 2)")
    axb.set_ylabel(r"$Q_*\,\delta^{2/3}/\log\delta$")
    axb.set_title("B   Critical-log normalization", loc="left", fontweight="bold")
    axb.legend(loc="upper left", frameon=False, handlelength=2.1, labelspacing=0.22)
    max_gap = float(results["panels"]["B"]["maximumRelativeCrossAuditGap"])
    plain = results["panels"]["B"]["producerPlainToCritical"]
    axb.text(
        0.97,
        0.08,
        (
            f"max cross-audit gap: {max_gap:.2e}\n"
            rf"plain $Q_{{1/3,0}}/Q_*$: {plain[0]:.3f} $\to$ {plain[-1]:.3f}"
        ),
        transform=axb.transAxes,
        ha="right",
        va="bottom",
        fontsize=4.25,
        color=palette["gray"],
        bbox={
            "facecolor": palette["paper"],
            "edgecolor": palette["light"],
            "linewidth": 0.45,
            "pad": 2.0,
        },
    )
    common_axes(axb, palette)

    # Panel C: exact rational frontier as a barycentric schematic.
    height_tri = math.sqrt(3.0) / 2.0
    vertices = np.asarray([(0.0, 0.0), (1.0, 0.0), (0.5, height_tri)])
    axc.add_patch(
        Polygon(
            vertices,
            closed=True,
            facecolor=palette["region"],
            edgecolor=palette["ink"],
            linewidth=0.8,
            hatch="..",
            alpha=0.55,
            zorder=1,
        )
    )
    axc.scatter(
        [0.5],
        [height_tri],
        marker="*",
        s=58,
        facecolor=palette["navy"],
        edgecolor=palette["ink"],
        linewidth=0.45,
        zorder=5,
    )
    axc.scatter(
        [0.0],
        [0.0],
        marker="s",
        s=30,
        facecolor=palette["rust"],
        edgecolor=palette["ink"],
        linewidth=0.45,
        zorder=5,
    )
    axc.scatter(
        [1.0],
        [0.0],
        marker="^",
        s=38,
        facecolor=palette["open"],
        edgecolor=palette["ink"],
        linewidth=0.9,
        zorder=5,
    )
    axc.text(
        0.5,
        height_tri + 0.075,
        "temporal action",
        ha="center",
        va="bottom",
        fontsize=4.85,
        fontweight="bold",
    )
    axc.text(
        0.5,
        height_tri + 0.015,
        r"$\beta=1/3,\ \gamma=1$",
        ha="center",
        va="bottom",
        fontsize=4.5,
        color=palette["navy"],
    )
    axc.text(
        -0.02,
        -0.105,
        "coupling scale",
        ha="left",
        va="top",
        fontsize=4.75,
        fontweight="bold",
    )
    axc.text(
        -0.02,
        -0.175,
        r"$c=1/3$",
        ha="left",
        va="top",
        fontsize=4.5,
        color=palette["rust"],
    )
    axc.text(
        1.02,
        -0.105,
        "root-atom weight",
        ha="right",
        va="top",
        fontsize=4.75,
        fontweight="bold",
    )
    axc.text(
        1.02,
        -0.175,
        r"$\alpha=4/9$  ·  CHANGES LHS",
        ha="right",
        va="top",
        fontsize=4.35,
        color=palette["ink"],
    )
    axc.text(
        0.5,
        0.39,
        r"fixed $a=1/3$" + "\n" + r"repair budget $=1/3$",
        ha="center",
        va="center",
        fontsize=4.7,
        color=palette["gray"],
    )
    axc.text(
        0.5,
        0.13,
        r"$\beta+c+3\alpha/4=1/3$",
        ha="center",
        va="center",
        fontsize=4.55,
        color=palette["ink"],
    )
    axc.set_xlim(-0.10, 1.10)
    axc.set_ylim(-0.23, 1.04)
    axc.set_aspect("equal", adjustable="box")
    axc.set_axis_off()
    axc.set_title("C   Three exact frontier vertices", loc="left", fontweight="bold")

    fig.text(
        0.065,
        0.075,
        (
            "Scope: selected-root scaling and finite corroboration only; no complete-root, "
            "restart, R_Y, regularity, or Millennium conclusion."
        ),
        ha="left",
        fontsize=4.45,
        color=palette["gray"],
    )
    fig.text(
        0.985,
        0.075,
        "R0.72F-1",
        ha="right",
        fontsize=4.8,
        color=palette["gray"],
    )

    fixed_pdf_time = datetime(2026, 8, 27, tzinfo=timezone.utc)
    creator = "R0.72F deterministic figure workflow"
    output = ROOT / "figure"
    fig.savefig(
        output.with_suffix(".pdf"),
        metadata={
            "Creator": creator,
            "CreationDate": fixed_pdf_time,
            "ModDate": fixed_pdf_time,
        },
        bbox_inches=None,
    )
    svg_path = output.with_suffix(".svg")
    fig.savefig(svg_path, metadata={"Creator": creator, "Date": None}, bbox_inches=None)
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )
    fig.savefig(
        output.with_suffix(".png"),
        dpi=int(config["figure"]["pngDpi"]),
        metadata={"Software": creator},
        bbox_inches=None,
    )
    plt.close(fig)


def write_lineage(config: dict[str, Any], results: dict[str, Any]) -> None:
    source_paths = [
        REPOSITORY / config["sourceCertificates"]["producer"],
        REPOSITORY / config["sourceCertificates"]["independent"],
        ROOT / "contract.json",
        ROOT / "config.json",
    ]
    payload = {
        "schemaVersion": "r072f-figure-data-metadata-v1",
        "generatedAtUtc": utc_now(),
        "rowCount": results["rowCount"],
        "panelCounts": results["panelCounts"],
        "randomness": False,
        "claimBoundary": load_json(ROOT / "contract.json")["claimBoundary"],
        "dataFiles": {
            "data.csv": sha256(ROOT / "data.csv"),
            "results.json": sha256(ROOT / "results.json"),
        },
        "sourceFiles": [
            {
                "path": str(path.relative_to(REPOSITORY)),
                "sha256": sha256(path),
            }
            for path in source_paths
        ],
    }
    (ROOT / "figure-data-metadata.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def write_environment(elapsed: float) -> None:
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        commit = "unknown"
    lines = [
        f"generatedAtUtc={utc_now()}",
        f"gitCommit={commit}",
        f"python={sys.version.splitlines()[0]}",
        f"platform={platform.platform()}",
        f"logicalCpus={os.cpu_count()}",
        f"matplotlib={mpl.__version__}",
        f"numpy={np.__version__}",
        "renderer=Matplotlib Agg-compatible static export",
        "precision=IEEE-754 binary64 source certificates",
        "gpu=false",
        "dgx=false",
        f"wallSeconds={elapsed:.6f}",
    ]
    (ROOT / "environment.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "config.json")
    parser.add_argument("--data-only", action="store_true")
    args = parser.parse_args()
    started = time.perf_counter()
    events: list[dict[str, object]] = [
        {"atUtc": utc_now(), "event": "start", "figureId": "R0.72F-1"}
    ]
    config_path = args.config if args.config.is_absolute() else Path.cwd() / args.config
    if not config_path.exists():
        config_path = ROOT / args.config
    config = load_json(config_path)
    producer = load_json(REPOSITORY / config["sourceCertificates"]["producer"])
    independent = load_json(
        REPOSITORY / config["sourceCertificates"]["independent"]
    )
    events.append(
        {
            "atUtc": utc_now(),
            "event": "sources-loaded",
            "producerPassed": producer["allRequiredChecksPassed"],
            "independentPassed": independent["allRequiredChecksPassed"],
        }
    )
    rows, results = prepare_data(producer, independent, config)
    write_data(rows, results)
    events.append(
        {
            "atUtc": utc_now(),
            "event": "data-written",
            "rows": len(rows),
            "panelCounts": results["panelCounts"],
        }
    )
    if not args.data_only:
        render(rows, results, config)
        events.append(
            {
                "atUtc": utc_now(),
                "event": "exports-written",
                "outputs": ["figure.pdf", "figure.svg", "figure.png"],
            }
        )
    write_lineage(config, results)
    elapsed = time.perf_counter() - started
    write_environment(elapsed)
    events.append(
        {
            "atUtc": utc_now(),
            "event": "complete",
            "wallSeconds": elapsed,
            "maximumResidentSetKiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        }
    )
    write_ndjson(ROOT / "progress.ndjson", events)
    write_ndjson(
        ROOT / "resource-log.ndjson",
        [
            {
                "atUtc": utc_now(),
                "logicalCpus": os.cpu_count(),
                "maximumResidentSetKiB": resource.getrusage(
                    resource.RUSAGE_SELF
                ).ru_maxrss,
                "wallSeconds": elapsed,
                "gpu": False,
                "dgx": False,
                "workload": "static figure build and finite JSON reduction",
            }
        ],
    )
    print(
        f"R0.72F-1 data and exports built: {len(rows)} rows in {elapsed:.3f} s"
    )


if __name__ == "__main__":
    main()
