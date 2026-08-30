#!/usr/bin/env python3
"""Render the formal R0.73K finite viscous-branch diagnostic figure."""

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
import socket
import subprocess
import sys
import time


def _bootstrap_dependencies() -> None:
    for index, argument in enumerate(sys.argv):
        if argument == "--deps" and index + 1 < len(sys.argv):
            sys.path.insert(0, str(Path(sys.argv[index + 1]).resolve()))
            return
        if argument.startswith("--deps="):
            sys.path.insert(0, str(Path(argument.split("=", 1)[1]).resolve()))
            return


_bootstrap_dependencies()

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Ellipse
import numpy as np


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
FIGURE_ID = "fig-r073k-uniform-viscous-branch"
PRIMARY_PATH = REPOSITORY / "experiments/r073k/viscous_branch_diagnostic.json"
INDEPENDENT_PATH = REPOSITORY / "experiments/r073k/independent_validation.json"
EXPERIMENT_CONFIG_PATH = REPOSITORY / "experiments/r073k/config.json"
EXPERIMENT_ENVIRONMENT_PATH = REPOSITORY / "experiments/r073k/environment.json"
PACKAGE_VALIDATION_PATH = REPOSITORY / "experiments/r073k/package_validation.json"
PRIMARY_PROGRESS_PATH = REPOSITORY / "experiments/r073k/progress.ndjson"
PRIMARY_RESOURCES_PATH = REPOSITORY / "experiments/r073k/resources.ndjson"
INDEPENDENT_PROGRESS_PATH = REPOSITORY / "experiments/r073k/independent_progress.ndjson"
INDEPENDENT_RESOURCES_PATH = REPOSITORY / "experiments/r073k/independent_resources.ndjson"
INPUT_PATHS = (
    PRIMARY_PATH,
    INDEPENDENT_PATH,
    EXPERIMENT_CONFIG_PATH,
    EXPERIMENT_ENVIRONMENT_PATH,
    PACKAGE_VALIDATION_PATH,
    PRIMARY_PROGRESS_PATH,
    PRIMARY_RESOURCES_PATH,
    INDEPENDENT_PROGRESS_PATH,
    INDEPENDENT_RESOURCES_PATH,
)
GENERATED = (
    "source-data.csv",
    "figure.pdf",
    "figure.svg",
    "figure.png",
    "results.json",
    "environment.json",
    "progress.ndjson",
    "resource-log.ndjson",
    "qa-report.md",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "validation.json",
    "manifest.json",
    "SHA256SUMS",
)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON root must be an object: {path}")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def process_rss_mib() -> float:
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return float(rss) / (1024.0 * 1024.0)
    return float(rss) / 1024.0


def git_text(*arguments: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *arguments], cwd=REPOSITORY, check=True,
            text=True, capture_output=True,
        )
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


class Monitor:
    def __init__(self) -> None:
        self.started = time.perf_counter()
        self.progress = HERE / "progress.ndjson"
        self.resources = HERE / "resource-log.ndjson"
        self.progress.write_text("", encoding="utf-8")
        self.resources.write_text("", encoding="utf-8")

    def event(self, stage: str, **fields: object) -> None:
        record = {
            "timestamp": utc_now(),
            "elapsedSeconds": round(time.perf_counter() - self.started, 6),
            "stage": stage,
            **fields,
        }
        with self.progress.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, sort_keys=True) + "\n")
        resource_record = {
            "timestamp": record["timestamp"],
            "elapsedSeconds": record["elapsedSeconds"],
            "stage": stage,
            "pid": os.getpid(),
            "processes": 1,
            "threadsPerProcess": 1,
            "maximumResidentSetMiB": round(process_rss_mib(), 3),
            "gpu": "not used",
        }
        with self.resources.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(resource_record, sort_keys=True) + "\n")


def input_record(path: Path) -> dict[str, object]:
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def float_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return format(float(value), ".17g")


CSV_FIELDS = (
    "record_type", "record_id", "order_index", "N", "dimension",
    "small_N", "large_N", "d_index", "d_label", "d", "epsilon",
    "regime", "lambda_real", "lambda_imag", "decay_rate",
    "first_order_decay_rate", "rate_error_abs", "projector_difference",
    "projector_norm", "left_right_overlap", "right_embedded_residual",
    "left_embedded_residual", "right_algebraic_residual",
    "left_algebraic_residual", "fixed_contour_count",
    "selected_inside_fixed_contour", "cross_projector_difference",
    "cross_lambda_difference", "upstream_path", "upstream_sha256",
)


def blank_row(record_type: str, record_id: str, order: int) -> dict[str, str]:
    row = {field: "" for field in CSV_FIELDS}
    row.update({
        "record_type": record_type,
        "record_id": record_id,
        "order_index": str(order),
    })
    return row


def build_source_rows(primary: dict, figure_config: dict) -> list[dict[str, str]]:
    upstream = str(PRIMARY_PATH.relative_to(REPOSITORY))
    upstream_hash = sha256(PRIMARY_PATH)
    display_cutoff = int(figure_config["analysis"]["displayCutoff"])
    core = sorted(
        (
            row for row in primary["rows"]
            if row["regime"] == "core" and int(row["N"]) == display_cutoff
        ),
        key=lambda row: (float(row["epsilon"]), int(row["dIndex"])),
    )
    rows: list[dict[str, str]] = []
    for item in core:
        order = len(rows) + 1
        epsilon = float(item["epsilon"])
        quotient = item["lambdaDifferenceOverEpsilon"]
        first_order = item["firstOrderAdjointFormulaAtZero"]
        decay_rate = None if quotient is None else -float(quotient["real"])
        first_order_rate = -float(first_order["real"])
        row = blank_row(
            "display_core_row",
            f"N{display_cutoff}-e{epsilon:.17g}-d{int(item['dIndex']):02d}",
            order,
        )
        row.update({
            "N": str(display_cutoff),
            "dimension": str(int(item["dimension"])),
            "d_index": str(int(item["dIndex"])),
            "d_label": str(item["dLabel"]),
            "d": float_text(item["d"]),
            "epsilon": float_text(epsilon),
            "regime": "core",
            "lambda_real": float_text(item["lambda"]["real"]),
            "lambda_imag": float_text(item["lambda"]["imag"]),
            "decay_rate": float_text(decay_rate),
            "first_order_decay_rate": float_text(first_order_rate),
            "rate_error_abs": float_text(
                None if decay_rate is None else abs(decay_rate - first_order_rate)
            ),
            "projector_difference": float_text(
                item["projectorDifferenceFromEpsilonZero"]
            ),
            "projector_norm": float_text(item["projectorNorm"]),
            "left_right_overlap": float_text(item["leftRightOverlap"]),
            "right_embedded_residual": float_text(item["rightEmbeddedResidual"]),
            "left_embedded_residual": float_text(item["leftEmbeddedResidual"]),
            "right_algebraic_residual": float_text(item["rightAlgebraicResidual"]),
            "left_algebraic_residual": float_text(item["leftAlgebraicResidual"]),
            "fixed_contour_count": str(int(item["fixedContourEigenvalueCount"])),
            "selected_inside_fixed_contour": float_text(
                item["selectedInsideFixedContour"]
            ),
            "upstream_path": upstream,
            "upstream_sha256": upstream_hash,
        })
        rows.append(row)

    all_core = [item for item in primary["rows"] if item["regime"] == "core"]
    for cutoff in sorted({int(item["N"]) for item in all_core}):
        subset = [item for item in all_core if int(item["N"]) == cutoff]
        row = blank_row("cutoff_summary", f"cutoff-N{cutoff}", len(rows) + 1)
        row.update({
            "N": str(cutoff),
            "dimension": str(2 * cutoff + 1),
            "regime": "core",
            "right_embedded_residual": float_text(max(
                float(item["rightEmbeddedResidual"]) for item in subset
            )),
            "left_embedded_residual": float_text(max(
                float(item["leftEmbeddedResidual"]) for item in subset
            )),
            "right_algebraic_residual": float_text(max(
                float(item["rightAlgebraicResidual"]) for item in subset
            )),
            "left_algebraic_residual": float_text(max(
                float(item["leftAlgebraicResidual"]) for item in subset
            )),
            "upstream_path": upstream,
            "upstream_sha256": upstream_hash,
        })
        rows.append(row)

    cross = primary["crossCutoffComparisons"]
    for small, large in figure_config["analysis"]["cutoffPairs"]:
        subset = [
            item for item in cross
            if item["regime"] == "core"
            and int(item["smallN"]) == int(small)
            and int(item["largeN"]) == int(large)
        ]
        require(subset, f"missing cross-cutoff pair {small}->{large}")
        row = blank_row(
            "cross_cutoff_summary", f"cross-N{small}-N{large}", len(rows) + 1
        )
        row.update({
            "small_N": str(int(small)),
            "large_N": str(int(large)),
            "regime": "core",
            "cross_projector_difference": float_text(max(
                float(item["embeddedProjectorDifference"]) for item in subset
            )),
            "cross_lambda_difference": float_text(max(
                float(item["lambdaAbsoluteDifference"]) for item in subset
            )),
            "upstream_path": upstream,
            "upstream_sha256": upstream_hash,
        })
        rows.append(row)

    return rows


def write_source_data(rows: list[dict[str, str]]) -> None:
    with (HERE / "source-data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def canonicalize_svg(path: Path) -> None:
    """Remove renderer-only line-end whitespace without changing SVG content."""
    text = path.read_text(encoding="utf-8")
    normalized = "\n".join(line.rstrip(" \t\r") for line in text.splitlines()) + "\n"
    path.write_text(normalized, encoding="utf-8", newline="\n")


def validate_inputs(
    figure_config: dict,
    contract: dict,
    primary: dict,
    independent: dict,
    experiment_config: dict,
    package_validation: dict,
) -> None:
    require(figure_config.get("figureId") == FIGURE_ID,
            "figure configuration identity drift")
    require(contract.get("figureId") == FIGURE_ID,
            "figure contract identity drift")
    require(primary.get("status") == "passed" and
            primary.get("allChecksPass") is True,
            "primary finite diagnostic is not passed")
    require(all(primary.get("checks", {}).values()),
            "a primary finite-diagnostic check is false")
    require(independent.get("status") == "passed" and
            independent.get("allChecksPass") is True,
            "independent finite recomputation is not passed")
    require(all(independent.get("checks", {}).values()),
            "an independent finite-recomputation check is false")
    require(package_validation.get("status") == "passed" and
            package_validation.get("allChecksPass") is True,
            "experiment package validation is not passed")
    require(all(package_validation.get("checks", {}).values()),
            "an experiment-package check is false")
    require(primary.get("release") == independent.get("release") ==
            package_validation.get("release") == "R0.73K",
            "release identity drift")
    require(primary["configurationBinding"]["sha256"] == sha256(EXPERIMENT_CONFIG_PATH),
            "primary configuration binding drift")
    require(independent["configuration"]["sha256"] == sha256(EXPERIMENT_CONFIG_PATH),
            "independent configuration binding drift")
    require(independent["primary"]["sha256"] == sha256(PRIMARY_PATH),
            "independent primary binding drift")
    require(primary["parameters"]["cutoffs"] == experiment_config["cutoffs"],
            "cutoff grid drift")
    require(primary["parameters"]["coreEpsilons"] == experiment_config["coreEpsilons"],
            "core epsilon grid drift")
    require(len(primary.get("rows", [])) == 1190, "expected 1190 primary rows")
    require(len(primary.get("crossCutoffComparisons", [])) == 952,
            "expected 952 cross-cutoff rows")
    display_cutoff = int(figure_config["analysis"]["displayCutoff"])
    display_rows = [
        row for row in primary["rows"]
        if row["regime"] == "core" and int(row["N"]) == display_cutoff
    ]
    require(len(display_rows) == 204, "expected 204 display-cutoff core rows")
    require({int(row["dIndex"]) for row in display_rows} == set(range(17)),
            "display-cutoff d grid is incomplete")
    require({float(row["epsilon"]) for row in display_rows} ==
            {float(value) for value in experiment_config["coreEpsilons"]},
            "display-cutoff core epsilon grid is incomplete")
    require(all(int(row["fixedContourEigenvalueCount"]) == 1 for row in display_rows),
            "a display-cutoff core row does not have fixed-circle count one")
    require(all(row["selectedInsideFixedContour"] is True for row in display_rows),
            "a display-cutoff core row is outside the fixed circle")
    require(max(abs(float(row["lambda"]["imag"])) for row in display_rows) < 1e-10,
            "display-cutoff branch is not numerically real")

    boundary = contract.get("claimBoundary", {})
    for key in (
        "formalValidatedDiagnosticFigure",
        "finiteDimensionalDiagnostic",
        "independentFiniteRecomputationPassed",
    ):
        require(boundary.get(key) is True, "missing supported claim: " + key)
    for key in (
        "continuumViscousBranchCertifiedByFigure",
        "explicitContinuumViscosityThresholdCertified",
        "adiabaticRemainderCertified",
        "nonlinearNavierStokesCertified",
        "transverseThreeDimensionalClosureCertified",
        "finiteTimeSingularityCertified",
        "clayProblemSolved",
    ):
        require(boundary.get(key) is False, "escaped claim boundary: " + key)


def style_axis(ax: plt.Axes, palette: dict) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(palette["muted"])
    ax.spines["bottom"].set_color(palette["muted"])
    ax.spines["left"].set_linewidth(0.65)
    ax.spines["bottom"].set_linewidth(0.65)
    ax.tick_params(labelsize=6.2, colors=palette["ink"], width=0.55, length=2.7)
    ax.grid(True, color=palette["grid"], linewidth=0.45, alpha=0.72)
    ax.set_axisbelow(True)


def add_blossom(fig: plt.Figure, palette: dict) -> None:
    center = (0.969, 0.966)
    for index, angle in enumerate(np.linspace(0.0, 360.0, 5, endpoint=False)):
        radians = math.radians(angle)
        petal_center = (
            center[0] + 0.0125 * math.cos(radians),
            center[1] + 0.0138 * math.sin(radians),
        )
        patch = Ellipse(
            petal_center, width=0.015, height=0.0085, angle=angle,
            transform=fig.transFigure,
            facecolor=palette["blueLight"] if index % 2 == 0 else palette["orangeLight"],
            edgecolor=palette["ink"], linewidth=0.35, alpha=0.88, zorder=20,
        )
        fig.add_artist(patch)
    fig.add_artist(Circle(
        center, radius=0.0041, transform=fig.transFigure,
        facecolor=palette["paper"], edgecolor=palette["ink"],
        linewidth=0.45, zorder=21,
    ))


def range_by_epsilon(rows: list[dict], field_fn) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    epsilons = np.array(sorted({float(row["epsilon"]) for row in rows if float(row["epsilon"]) > 0}))
    lower = []
    upper = []
    for epsilon in epsilons:
        values = [float(field_fn(row)) for row in rows if float(row["epsilon"]) == epsilon]
        lower.append(min(values))
        upper.append(max(values))
    return epsilons, np.asarray(lower), np.asarray(upper)


def render_figure(
    primary: dict,
    figure_config: dict,
    rows: list[dict[str, str]],
) -> None:
    width = float(figure_config["widthMillimetres"]) / 25.4
    height = float(figure_config["heightMillimetres"]) / 25.4
    palette = figure_config["palette"]
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 7.0,
        "axes.titlesize": 8.0,
        "axes.labelsize": 7.0,
        "legend.fontsize": 5.8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "axes.unicode_minus": True,
    })
    fig = plt.figure(figsize=(width, height), facecolor=palette["paper"])
    grid = fig.add_gridspec(
        2, 2, left=0.075, right=0.972, bottom=0.165, top=0.843,
        wspace=0.29, hspace=0.44,
    )
    ax_a = fig.add_subplot(grid[0, 0])
    ax_b = fig.add_subplot(grid[0, 1])
    c_grid = grid[1, 0].subgridspec(2, 1, hspace=0.18)
    ax_c1 = fig.add_subplot(c_grid[0, 0])
    ax_c2 = fig.add_subplot(c_grid[1, 0], sharex=ax_c1)
    ax_d = fig.add_subplot(grid[1, 1])

    fig.text(
        0.075, 0.966, "R0.73K  Parameter-uniform viscous branch",
        fontsize=11.0, fontweight="bold", color=palette["ink"], va="top",
    )
    fig.text(
        0.075, 0.932,
        "Largest-cutoff branch, first-order drift, projector conditioning, and cutoff closure",
        fontsize=7.0, color=palette["muted"], va="top",
    )
    fig.text(
        0.075, 0.902, "FINITE-DIMENSIONAL DIAGNOSTIC  /  NOT CONTINUUM PROOF",
        fontsize=6.45, fontweight="bold", color=palette["orange"], va="top",
    )
    add_blossom(fig, palette)

    display_cutoff = int(figure_config["analysis"]["displayCutoff"])
    display = [
        row for row in primary["rows"]
        if row["regime"] == "core" and int(row["N"]) == display_cutoff
    ]
    display.sort(key=lambda row: (float(row["epsilon"]), int(row["dIndex"])))

    series_styles = [
        (palette["blue"], "-", "o", palette["blue"], r"$\varepsilon=0$"),
        (palette["blueLight"], "--", "s", palette["paper"], r"$10^{-4}$"),
        (palette["orangeLight"], "-.", "^", palette["paper"], r"$3\times10^{-4}$"),
        (palette["orange"], ":", "D", palette["orange"], r"$10^{-3}$"),
    ]
    for epsilon, style in zip(figure_config["analysis"]["branchEpsilons"], series_styles):
        subset = sorted(
            (row for row in display if float(row["epsilon"]) == float(epsilon)),
            key=lambda row: int(row["dIndex"]),
        )
        x = np.array([450.0 * float(row["d"]) for row in subset])
        y = np.array([float(row["lambda"]["real"]) for row in subset])
        color, line, marker, face, label = style
        ax_a.plot(
            x, y, color=color, linestyle=line, linewidth=1.15,
            marker=marker, markersize=2.8, markerfacecolor=face,
            markeredgecolor=color, markeredgewidth=0.65, markevery=4,
            label=label,
        )
    style_axis(ax_a, palette)
    ax_a.set_title(r"$\bf{A}$  Selected eigenvalue across $d$", loc="left", pad=7.0)
    ax_a.text(
        0.0, 1.015, r"$N=160$; 17 nodes; focused vertical scale",
        transform=ax_a.transAxes, fontsize=5.8, color=palette["muted"], va="bottom",
    )
    ax_a.set_xlabel(r"scaled parameter $450d$")
    ax_a.set_ylabel(r"$\mathrm{Re}\,\lambda_N(\varepsilon,d)$")
    ax_a.set_xlim(-0.02, 1.02)
    ax_a.legend(
        loc="lower left", frameon=False, ncol=2, handlelength=2.3,
        columnspacing=1.1, borderaxespad=0.3,
    )

    eps, rate_low, rate_high = range_by_epsilon(
        display, lambda row: -float(row["lambdaDifferenceOverEpsilon"]["real"])
    )
    _, first_low, first_high = range_by_epsilon(
        display, lambda row: -float(row["firstOrderAdjointFormulaAtZero"]["real"])
    )
    rate_mid = 0.5 * (rate_low + rate_high)
    ax_b.fill_between(
        eps, rate_low, rate_high, color=palette["blueLight"], alpha=0.38,
        linewidth=0.0,
    )
    ax_b.plot(
        eps, rate_mid, color=palette["blue"], linewidth=1.2,
        marker="o", markersize=3.0, label="finite-difference rate",
    )
    first_min = float(np.min(first_low))
    first_max = float(np.max(first_high))
    ax_b.axhspan(
        first_min, first_max, facecolor=palette["orangeLight"], alpha=0.30,
        edgecolor="none",
    )
    ax_b.axhline(
        0.5 * (first_min + first_max), color=palette["orange"],
        linestyle="--", linewidth=1.05, label="inviscid-adjoint formula",
    )
    style_axis(ax_b, palette)
    ax_b.set_xscale("log")
    ax_b.set_title(r"$\bf{B}$  First-order viscous drift", loc="left", pad=7.0)
    ax_b.text(
        0.0, 1.015, r"bands span all 17 $d$ nodes at $N=160$",
        transform=ax_b.transAxes, fontsize=5.8, color=palette["muted"], va="bottom",
    )
    ax_b.set_xlabel(r"viscosity $\varepsilon$")
    ax_b.set_ylabel(r"$-[\mathrm{Re}\lambda_N(\varepsilon)-\mathrm{Re}\lambda_N(0)]/\varepsilon$")
    ax_b.legend(loc="lower left", frameon=False, handlelength=2.4)

    eps_p, pdiff_low, pdiff_high = range_by_epsilon(
        display, lambda row: float(row["projectorDifferenceFromEpsilonZero"])
    )
    pdiff_mid = np.sqrt(pdiff_low * pdiff_high)
    ax_c1.fill_between(
        eps_p, pdiff_low, pdiff_high, color=palette["blueLight"], alpha=0.38,
        linewidth=0.0,
    )
    ax_c1.plot(
        eps_p, pdiff_mid, color=palette["blue"], linewidth=1.15,
        marker="o", markersize=2.7,
    )
    style_axis(ax_c1, palette)
    ax_c1.set_xscale("log")
    ax_c1.set_yscale("log")
    ax_c1.set_title(r"$\bf{C}$  Projector difference and conditioning", loc="left", pad=7.0)
    ax_c1.text(
        0.0, 1.015, r"ranges over $d$ at $N=160$",
        transform=ax_c1.transAxes, fontsize=5.8, color=palette["muted"], va="bottom",
    )
    ax_c1.set_ylabel(r"$\|P_{\varepsilon,N}-P_{0,N}\|$")
    ax_c1.tick_params(labelbottom=False)

    eps_n, pnorm_low, pnorm_high = range_by_epsilon(
        display, lambda row: float(row["projectorNorm"])
    )
    pnorm_mid = 0.5 * (pnorm_low + pnorm_high)
    inviscid = [row for row in display if float(row["epsilon"]) == 0.0]
    inviscid_low = min(float(row["projectorNorm"]) for row in inviscid)
    inviscid_high = max(float(row["projectorNorm"]) for row in inviscid)
    ax_c2.axhspan(
        inviscid_low, inviscid_high, facecolor=palette["grid"], alpha=0.62,
        edgecolor="none", label=r"$\varepsilon=0$ range",
    )
    ax_c2.fill_between(
        eps_n, pnorm_low, pnorm_high, color=palette["orangeLight"], alpha=0.42,
        linewidth=0.0,
    )
    ax_c2.plot(
        eps_n, pnorm_mid, color=palette["orange"], linestyle="--",
        linewidth=1.15, marker="s", markerfacecolor=palette["paper"],
        markeredgecolor=palette["orange"], markeredgewidth=0.65, markersize=2.7,
    )
    style_axis(ax_c2, palette)
    ax_c2.set_xscale("log")
    ax_c2.set_xlabel(r"viscosity $\varepsilon$")
    ax_c2.set_ylabel(r"$\|P_{\varepsilon,N}\|$")
    ax_c2.legend(loc="lower left", frameon=False, handlelength=1.8)

    cutoff_rows = [row for row in rows if row["record_type"] == "cutoff_summary"]
    cutoff_rows.sort(key=lambda row: int(row["N"]))
    cutoffs = np.array([int(row["N"]) for row in cutoff_rows])
    right_residual = np.array([float(row["right_embedded_residual"]) for row in cutoff_rows])
    left_residual = np.array([float(row["left_embedded_residual"]) for row in cutoff_rows])
    cross_rows = [row for row in rows if row["record_type"] == "cross_cutoff_summary"]
    cross_rows.sort(key=lambda row: int(row["large_N"]))
    cross_x = np.array([int(row["large_N"]) for row in cross_rows])
    cross_p = np.array([float(row["cross_projector_difference"]) for row in cross_rows])
    display_floor = 1e-15
    ax_d.plot(
        cutoffs, np.maximum(right_residual, display_floor), color=palette["orange"],
        linewidth=1.1, marker="o", markersize=3.0, label="right embedded residual",
    )
    ax_d.plot(
        cutoffs, np.maximum(left_residual, display_floor), color=palette["orange"],
        linestyle="--", linewidth=1.1, marker="^", markerfacecolor=palette["paper"],
        markeredgewidth=0.65, markersize=3.2, label="left embedded residual",
    )
    ax_d.plot(
        cross_x, np.maximum(cross_p, display_floor), color=palette["blue"],
        linestyle="-.", linewidth=1.15, marker="s", markerfacecolor=palette["paper"],
        markeredgewidth=0.65, markersize=3.0, label=r"adjacent-cutoff $\Delta P$",
    )
    style_axis(ax_d, palette)
    ax_d.set_yscale("log")
    ax_d.set_title(r"$\bf{D}$  Cutoff closure", loc="left", pad=7.0)
    ax_d.text(
        0.0, 1.015, r"maximum over the complete core $(d,\varepsilon)$ grid",
        transform=ax_d.transAxes, fontsize=5.8, color=palette["muted"], va="bottom",
    )
    ax_d.set_xlabel(r"Fourier cutoff $N$ (pair endpoint for $\Delta P$)")
    ax_d.set_ylabel("maximum diagnostic")
    ax_d.set_xticks(cutoffs)
    ax_d.set_ylim(5e-16, 1e-2)
    ax_d.legend(loc="upper right", frameon=False, handlelength=2.4)

    fig.text(
        0.075, 0.035,
        "Source: sealed R0.73K finite Fourier diagnostic + independent coefficient-level recomputation.  "
        "Bands are sampled ranges, not rigorous continuum intervals.",
        fontsize=5.65, color=palette["muted"], ha="left", va="bottom",
    )
    fig.savefig(HERE / "figure.pdf", facecolor=palette["paper"])
    fig.savefig(HERE / "figure.svg", facecolor=palette["paper"])
    canonicalize_svg(HERE / "figure.svg")
    fig.savefig(
        HERE / "figure.png", dpi=int(figure_config["pngDpi"]),
        facecolor=palette["paper"], pil_kwargs={"compress_level": 7},
    )
    plt.close(fig)


def build_results(
    primary: dict,
    independent: dict,
    figure_config: dict,
    contract: dict,
    rows: list[dict[str, str]],
    wall_time: float,
    rendered_at: str,
) -> dict:
    display = [
        row for row in primary["rows"]
        if row["regime"] == "core"
        and int(row["N"]) == int(figure_config["analysis"]["displayCutoff"])
    ]
    positive = [row for row in display if float(row["epsilon"]) > 0.0]
    cutoff_rows = [row for row in rows if row["record_type"] == "cutoff_summary"]
    cross_rows = [row for row in rows if row["record_type"] == "cross_cutoff_summary"]
    last_cross = next(row for row in cross_rows if row["small_N"] == "128")
    last_cutoff = next(row for row in cutoff_rows if row["N"] == "160")
    decisions = {
        "displayCutoff": 160,
        "displayCoreRows": len(display),
        "dNodes": len({int(row["dIndex"]) for row in display}),
        "coreEpsilonLevels": len({float(row["epsilon"]) for row in display}),
        "coreFixedContourMultiplicityExactlyOne": all(
            int(row["fixedContourEigenvalueCount"]) == 1 for row in display
        ),
        "maximumCoreLambdaImaginaryAbs": max(
            abs(float(row["lambda"]["imag"])) for row in display
        ),
        "maximumCoreRateErrorAgainstFirstOrder": max(
            abs(
                -float(row["lambdaDifferenceOverEpsilon"]["real"])
                + float(row["firstOrderAdjointFormulaAtZero"]["real"])
            ) for row in positive
        ),
        "maximumCoreProjectorDifference": max(
            float(row["projectorDifferenceFromEpsilonZero"]) for row in display
        ),
        "maximumCoreProjectorNorm": max(float(row["projectorNorm"]) for row in display),
        "minimumCoreLeftRightOverlap": min(
            float(row["leftRightOverlap"]) for row in display
        ),
        "largestTwoCutoffsCoreEigenvalueDifference": float(
            last_cross["cross_lambda_difference"]
        ),
        "largestTwoCutoffsCoreEmbeddedProjectorDifference": float(
            last_cross["cross_projector_difference"]
        ),
        "largestCutoffCoreRightEmbeddedResidual": float(
            last_cutoff["right_embedded_residual"]
        ),
        "largestCutoffCoreLeftEmbeddedResidual": float(
            last_cutoff["left_embedded_residual"]
        ),
        "independentMaximumOrdinaryAbsoluteError": max(
            value for key, value in independent["maximumAbsoluteErrors"].items()
            if "Quotient" not in key and key not in (
                "lambdaQuotientImag", "lambdaQuotientReal",
                "quotientExactDifference", "quotientFirstDifference",
            )
        ),
        "independentMaximumDifferenceQuotientAbsoluteError": max(
            independent["maximumAbsoluteErrors"][key]
            for key in (
                "lambdaQuotientImag", "lambdaQuotientReal",
                "quotientExactDifference", "quotientFirstDifference",
            )
        ),
    }
    return {
        "schemaVersion": "r073k-uniform-viscous-branch-figure-results-v1",
        "figureId": FIGURE_ID,
        "release": "R0.73K",
        "status": "passed",
        "allChecksPass": True,
        "renderedAt": rendered_at,
        "wallTimeSeconds": wall_time,
        "inputBindings": [input_record(path) for path in INPUT_PATHS],
        "rowCounts": {
            "primary": len(primary["rows"]),
            "crossCutoff": len(primary["crossCutoffComparisons"]),
            "displayCore": len(display),
            "cutoffSummaries": len(cutoff_rows),
            "crossCutoffSummaries": len(cross_rows),
            "sourceData": len(rows),
        },
        "decisions": decisions,
        "upstreamStatus": {
            "primaryDiagnostic": primary["status"],
            "independentValidation": independent["status"],
            "experimentPackageValidation": "passed",
        },
        "claimBoundary": contract["claimBoundary"],
    }


def write_environment(rendered_at: str) -> None:
    status = git_text("status", "--porcelain", "--untracked-files=no")
    environment = {
        "schemaVersion": "r073k-uniform-viscous-branch-figure-environment-v1",
        "createdAt": rendered_at,
        "python": platform.python_version(),
        "pythonImplementation": platform.python_implementation(),
        "numpy": np.__version__,
        "matplotlib": mpl.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "host": socket.gethostname(),
        "cpuCount": os.cpu_count(),
        "threadEnvironment": {
            key: os.environ.get(key)
            for key in (
                "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS",
                "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS",
            )
        },
        "git": {
            "head": git_text("rev-parse", "HEAD"),
            "branch": git_text("branch", "--show-current"),
            "trackedWorktreeDirtyAtRender": bool(status),
            "wholeWorktreeCleanAtRender": False,
            "workingTreeBoundByInputAndPackageHashes": True,
        },
        "compute": {
            "processes": 1,
            "threadsPerProcess": 1,
            "gpu": "not used",
            "dgx": "not used; deterministic static rendering is local CPU work",
        },
        "claimBoundary": {
            "finiteDimensionalOnly": True,
            "continuumTheoremCertifiedByThisEnvironment": False,
        },
    }
    (HERE / "environment.json").write_text(canonical(environment), encoding="utf-8")


def write_pending_qa_report(results: dict) -> None:
    decisions = results["decisions"]
    text = f"""# R0.73K figure QA report

**Status:** pending manual visual inspection.

Automated extraction and export preparation completed. Inspect `figure.png`,
`qa-final-size.png`, `qa-grayscale.png`, and `qa-pdf.png` at original
resolution before changing this status to passed.

Automated facts:

- source rows: {results['rowCounts']['sourceData']} = {results['rowCounts']['displayCore']} display-core rows + {results['rowCounts']['cutoffSummaries']} cutoff summaries + {results['rowCounts']['crossCutoffSummaries']} cross-cutoff summaries;
- primary rows: {results['rowCounts']['primary']}; cross-cutoff rows: {results['rowCounts']['crossCutoff']};
- largest-two-cutoff eigenvalue difference: {decisions['largestTwoCutoffsCoreEigenvalueDifference']:.17g};
- largest-two-cutoff embedded projector difference: {decisions['largestTwoCutoffsCoreEmbeddedProjectorDifference']:.17g};
- largest-cutoff right/left embedded residuals: {decisions['largestCutoffCoreRightEmbeddedResidual']:.17g} / {decisions['largestCutoffCoreLeftEmbeddedResidual']:.17g}.

Manual inspection checklist:

- original 600 dpi PNG: pending;
- final-size raster: pending;
- grayscale distinctions: pending;
- independently rasterized PDF: pending;
- labels, focused-scale note, blossom anchor, and claim boundary: pending.
"""
    (HERE / "qa-report.md").write_text(text, encoding="utf-8")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deps", help="directory containing pinned Python packages")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    if arguments.overwrite:
        for name in GENERATED:
            path = HERE / name
            if path.exists():
                path.unlink()
    else:
        conflicts = [name for name in GENERATED if (HERE / name).exists()]
        require(not conflicts, "generated files already exist; use --overwrite: " + ", ".join(conflicts))

    monitor = Monitor()
    monitor.event("started")
    started = time.perf_counter()
    figure_config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    primary = load_json(PRIMARY_PATH)
    independent = load_json(INDEPENDENT_PATH)
    experiment_config = load_json(EXPERIMENT_CONFIG_PATH)
    package_validation = load_json(PACKAGE_VALIDATION_PATH)
    validate_inputs(
        figure_config, contract, primary, independent,
        experiment_config, package_validation,
    )
    monitor.event("inputs-validated", primaryRows=len(primary["rows"]),
                  crossCutoffRows=len(primary["crossCutoffComparisons"]))

    rows = build_source_rows(primary, figure_config)
    require(len(rows) == 213, "source row count drift")
    write_source_data(rows)
    monitor.event("source-data-written", rows=len(rows))

    render_figure(primary, figure_config, rows)
    monitor.event(
        "figure-rendered", pdfBytes=(HERE / "figure.pdf").stat().st_size,
        svgBytes=(HERE / "figure.svg").stat().st_size,
        pngBytes=(HERE / "figure.png").stat().st_size,
    )
    rendered_at = utc_now()
    wall_time = time.perf_counter() - started
    results = build_results(
        primary, independent, figure_config, contract, rows, wall_time, rendered_at
    )
    (HERE / "results.json").write_text(canonical(results), encoding="utf-8")
    write_environment(rendered_at)
    write_pending_qa_report(results)
    monitor.event("completed", status="passed", sourceRows=len(rows))
    print(canonical({
        "figureId": FIGURE_ID,
        "status": "passed",
        "sourceRows": len(rows),
        "wallTimeSeconds": wall_time,
        "outputs": ["figure.pdf", "figure.svg", "figure.png"],
    }), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
