#!/usr/bin/env python3
"""Build the R0.72R caustic-free-core journal figure.

All curves are presentation samples of exact formulas.  This script runs no
PDE solver, root fit, regression, or numerical chamber classification.
"""

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
import re
import resource
import subprocess
import sys
import time
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
import numpy as np

from certificate_ledger import verify_flat_certificate_ledger


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
PACKAGE_SOURCES = (
    "README.md", "caption.md", "figure-contract.md", "contract.json",
    "config.json", "command.txt", "requirements.txt", "certificate_ledger.py",
    "plot.py", "qa_images.py", "publish_assets.py", "validate.py",
    "build_manifest.py",
)
FIELDS = (
    "panel", "route", "series", "kind", "x", "y", "phi", "theta",
    "radius", "distance", "source", "pointer", "status", "note",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def max_rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024.0 * 1024.0) if sys.platform == "darwin" else value / 1024.0


def git_commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True
    ).strip()


def require_tracked_tree_clean() -> None:
    for command in (
        ("git", "diff", "--quiet", "--"),
        ("git", "diff", "--cached", "--quiet", "--"),
    ):
        completed = subprocess.run(command, cwd=REPOSITORY, check=False)
        if completed.returncode == 1:
            raise RuntimeError("formal figure build rejects tracked or staged drift")
        if completed.returncode != 0:
            raise RuntimeError("unable to verify tracked-tree cleanliness")


def package_source_git_blobs(commit: str) -> dict[str, str]:
    if FULL_SHA.fullmatch(commit) is None:
        raise RuntimeError("formal figure build requires a full HEAD commit")
    records: dict[str, str] = {}
    for name in PACKAGE_SOURCES:
        path = (ROOT / name).resolve()
        relative = str(path.relative_to(REPOSITORY.resolve()))
        try:
            object_type = subprocess.check_output(
                ["git", "cat-file", "-t", f"{commit}:{relative}"],
                cwd=REPOSITORY, text=True, stderr=subprocess.DEVNULL,
            ).strip()
            committed = subprocess.check_output(
                ["git", "rev-parse", f"{commit}:{relative}"],
                cwd=REPOSITORY, text=True, stderr=subprocess.DEVNULL,
            ).strip()
            working = subprocess.check_output(
                ["git", "hash-object", f"--path={relative}", str(path)],
                cwd=REPOSITORY, text=True, stderr=subprocess.DEVNULL,
            ).strip()
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(f"package source is not tracked at {commit}: {relative}") from exc
        if object_type != "blob" or committed != working:
            raise RuntimeError(f"package source does not match {commit}:{relative}")
        records[relative] = committed
    return records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analytic-source", required=True)
    parser.add_argument("--producer-config", required=True)
    parser.add_argument("--producer-result", required=True)
    parser.add_argument("--independent-config", required=True)
    parser.add_argument("--independent-result", required=True)
    parser.add_argument("--crosscheck", required=True)
    return parser.parse_args()


def load_json(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"{label} does not exist: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} must be a JSON object")
    return value


def runtime_lineage(args: argparse.Namespace, config: dict[str, Any]) -> tuple[dict[str, Any], str, dict[str, Any]]:
    bindings = config["formalGitBindings"]
    paths = {
        "analyticSource": Path(args.analytic_source).expanduser().resolve(),
        "producerConfig": Path(args.producer_config).expanduser().resolve(),
        "producerResult": Path(args.producer_result).expanduser().resolve(),
        "independentConfig": Path(args.independent_config).expanduser().resolve(),
        "independentResult": Path(args.independent_result).expanduser().resolve(),
        "crosscheck": Path(args.crosscheck).expanduser().resolve(),
        "certificateLedger": (REPOSITORY / bindings["certificateLedgerPath"]).resolve(),
    }
    canonical = {
        "analyticSource": (REPOSITORY / bindings["sourceCommitPaths"][0]).resolve(),
        **{
            role: (REPOSITORY / relative).resolve()
            for role, relative in bindings["certificateCommitRoles"].items()
        },
        "certificateLedger": (REPOSITORY / bindings["certificateLedgerPath"]).resolve(),
    }
    if paths != canonical:
        raise RuntimeError("formal figure inputs must be the canonical repository files")
    if not paths["analyticSource"].is_file():
        raise FileNotFoundError(paths["analyticSource"])

    producer_config = load_json(paths["producerConfig"], "producer config")
    independent_config = load_json(paths["independentConfig"], "independent config")
    producer_result = load_json(paths["producerResult"], "producer result")
    independent_result = load_json(paths["independentResult"], "independent result")
    crosscheck = load_json(paths["crosscheck"], "crosscheck")
    checks = crosscheck.get("checks")
    source_commit = crosscheck.get("sourceCommit")
    if (
        crosscheck.get("status") != "passed"
        or not isinstance(checks, dict)
        or not checks
        or not all(value is True for value in checks.values())
        or crosscheck.get("temporaryUnsealedSourceAllowed") is not False
        or not isinstance(source_commit, str)
        or FULL_SHA.fullmatch(source_commit) is None
        or producer_config.get("gitCommit") != source_commit
        or independent_config.get("gitCommit") != source_commit
        or producer_config.get("sourceTracked") is not True
        or independent_config.get("sourceTracked") is not True
        or producer_config.get("trackedChangesDirty") is not False
        or independent_config.get("trackedChangesDirty") is not False
        or producer_result.get("status") != "passed"
        or independent_result.get("status") != "passed"
    ):
        raise RuntimeError("formal R0.72R certificate lineage is not sealed")

    ledger = verify_flat_certificate_ledger(
        paths["certificateLedger"].parent,
        required_files={
            Path(relative).name
            for relative in bindings["certificateCommitRoles"].values()
        },
    )
    statuses = {
        "analyticSource": "source",
        "producerConfig": "formal-ready-config",
        "producerResult": "passed",
        "independentConfig": "formal-ready-config",
        "independentResult": "passed",
        "crosscheck": "passed-formal-source-only",
        "certificateLedger": "passed-flat-ledger",
    }
    records = {
        name: {"path": str(path), "sha256": sha256(path), "status": statuses[name]}
        for name, path in paths.items()
    }
    return records, source_commit, ledger


def add_row(rows: list[dict[str, str]], *, panel: str, route: str, series: str,
            kind: str, x: float, y: float, source: str, pointer: str,
            status: str, note: str, phi: float | str = "",
            theta: float | str = "", radius: float | str = "",
            distance: float | str = "") -> None:
    if not math.isfinite(float(x)) or not math.isfinite(float(y)):
        raise ValueError("non-finite figure datum")
    rows.append({
        "panel": panel, "route": route, "series": series, "kind": kind,
        "x": f"{float(x):.17g}", "y": f"{float(y):.17g}",
        "phi": str(phi), "theta": str(theta), "radius": str(radius),
        "distance": str(distance), "source": source, "pointer": pointer,
        "status": status, "note": note,
    })


def surface(ax: mpl.axes.Axes, palette: dict[str, str]) -> None:
    ax.set_facecolor(palette["paper"])
    ax.grid(True, color=palette["grid"], linewidth=0.45, alpha=0.75)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(palette["muted"])
        ax.spines[side].set_linewidth(0.65)
    ax.tick_params(labelsize=6.3, colors=palette["ink"], width=0.55)


def title(ax: mpl.axes.Axes, letter: str, heading: str, subheading: str,
          palette: dict[str, str]) -> None:
    ax.text(-0.04, 1.105, letter, transform=ax.transAxes, ha="right", va="top",
            fontsize=10.5, fontweight="bold", color=palette["ink"])
    ax.text(0.0, 1.105, heading, transform=ax.transAxes, ha="left", va="top",
            fontsize=8.6, fontweight="bold", color=palette["ink"])
    ax.text(0.0, 1.035, subheading, transform=ax.transAxes, ha="left", va="top",
            fontsize=6.0, color=palette["muted"])


def main() -> None:
    started = time.perf_counter()
    require_tracked_tree_clean()
    commit = git_commit()
    source_blobs = package_source_git_blobs(commit)
    args = parse_args()
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    lineage, source_commit, ledger = runtime_lineage(args, config)
    palette = config["palette"]
    parameters = config["parameters"]

    for name in ("progress.ndjson", "resource-log.ndjson"):
        (ROOT / name).write_text("", encoding="utf-8")
    with (ROOT / "progress.ndjson").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"time": utc_now(), "event": "start", "commit": commit}) + "\n")

    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "axes.unicode_minus": True,
    })
    width = float(config["figure"]["widthMillimetres"]) / 25.4
    height = float(config["figure"]["heightMillimetres"]) / 25.4
    fig, axes = plt.subplots(1, 3, figsize=(width, height), constrained_layout=False)
    fig.patch.set_facecolor(palette["paper"])
    fig.subplots_adjust(left=0.055, right=0.985, bottom=0.18, top=0.80, wspace=0.31)
    rows: list[dict[str, str]] = []

    # Panel A: exact real slice.
    ax = axes[0]
    surface(ax, palette)
    panel_a = config["panels"]["A"]
    a_values = np.linspace(-0.62, 0.62, int(panel_a["lineSamples"]))
    line_zero = -(1.0 + 4.0 * a_values) / 9.0
    line_pi = -(1.0 - 4.0 * a_values) / 9.0
    ax.plot(a_values, line_zero, color=palette["ochre"], lw=1.0, label=r"endpoint walls")
    ax.plot(a_values, line_pi, color=palette["ochre"], lw=1.0)
    for series, values in (("endpoint phi=0", line_zero), ("endpoint phi=pi", line_pi)):
        for a_value, b_value in zip(a_values, values):
            add_row(rows, panel="A", route="exact-real-slice", series=series,
                    kind="analytic-curve", x=a_value, y=b_value,
                    source="research/r072r_report-source.md", pointer="(7.4)",
                    status="proved", note="exact endpoint wall")

    x_values = np.linspace(-1.0, 1.0, int(panel_a["arcSamples"]))
    arc_a = -2.0 * x_values / (1.0 + 4.0 * x_values**2)
    arc_b = 1.0 / (3.0 * (1.0 + 4.0 * x_values**2))
    ax.plot(arc_a, arc_b, color=palette["red"], lw=1.25, label=r"internal unit-circle arc")
    for x_value, a_value, b_value in zip(x_values, arc_a, arc_b):
        add_row(rows, panel="A", route="exact-real-slice", series="internal arc",
                kind="analytic-curve", x=a_value, y=b_value, phi=x_value,
                source="research/r072r_report-source.md", pointer="(7.5)",
                status="proved", note="x=cos(phi) parameter")

    old_q2_boundary = float(parameters["oldQ2Boundary"])
    vertices = np.array([
        [old_q2_boundary / 4.0, 0.0],
        [0.0, old_q2_boundary / 9.0],
        [-old_q2_boundary / 4.0, 0.0],
        [0.0, -old_q2_boundary / 9.0],
    ])
    ax.add_patch(Polygon(vertices, closed=True, facecolor=palette["blueLight"],
                         edgecolor=palette["blue"], linestyle="--", linewidth=0.9,
                         alpha=0.55, label=r"old $Q_2\leq1/2$ slice"))
    edge_samples = int(panel_a["coneSamplesPerEdge"])
    for edge in range(4):
        start_vertex = vertices[edge]
        end_vertex = vertices[(edge + 1) % 4]
        for parameter in np.linspace(0.0, 1.0, edge_samples):
            point = (1.0 - parameter) * start_vertex + parameter * end_vertex
            add_row(rows, panel="A", route="old-sufficient-cone", series=f"cone edge {edge}",
                    kind="analytic-boundary", x=point[0], y=point[1],
                    theta=parameter, source="research/r072r_report-source.md",
                    pointer="(0.1)", status="prior-sufficient-condition",
                    note="4|a|+9|b|=1/2")

    center_z2 = float(parameters["centerZ2"])
    radius_z2 = float(parameters["radiusZ2"])
    radius_z3 = float(parameters["radiusZ3"])
    z2_lower = center_z2 - radius_z2
    z2_upper = center_z2 + radius_z2
    k_rectangle = Rectangle((z2_lower, -radius_z3), 2.0 * radius_z2, 2.0 * radius_z3,
                            facecolor=palette["blueDark"], edgecolor=palette["ink"],
                            linewidth=1.0, alpha=0.9, zorder=6)
    ax.add_patch(k_rectangle)
    for edge, (start_point, end_point) in enumerate((
        ((z2_lower, -radius_z3), (z2_upper, -radius_z3)),
        ((z2_upper, -radius_z3), (z2_upper, radius_z3)),
        ((z2_upper, radius_z3), (z2_lower, radius_z3)),
        ((z2_lower, radius_z3), (z2_lower, -radius_z3)),
    )):
        for parameter in np.linspace(0.0, 1.0, 61):
            x_point = (1.0 - parameter) * start_point[0] + parameter * end_point[0]
            y_point = (1.0 - parameter) * start_point[1] + parameter * end_point[1]
            add_row(rows, panel="A", route="certified-core", series=f"K edge {edge}",
                    kind="exact-domain-boundary", x=x_point, y=y_point,
                    theta=parameter, source="research/r072r_report-source.md",
                    pointer="(0.2)", status="proved", note="real trace of complex polydisc K")
    ax.annotate(r"real trace of $K$", xy=(center_z2, 0.0), xytext=(0.25, 0.09),
                fontsize=6.0, color=palette["blueDark"],
                arrowprops={"arrowstyle": "->", "lw": 0.65, "color": palette["blueDark"]})
    ax.set_xlim(-0.62, 0.62)
    ax.set_ylim(-0.17, 0.38)
    ax.set_xlabel(r"second coefficient $a$", fontsize=7.0)
    ax.set_ylabel(r"third coefficient $b$", fontsize=7.0)
    title(ax, "A", "Exact real slice", "caustic, old sufficient cone, and the real trace of K", palette)
    ax.legend(loc="lower left", fontsize=5.5, frameon=False, handlelength=2.2)

    # Panel B: exact heat envelopes.
    ax = axes[1]
    surface(ax, palette)
    panel_b = config["panels"]["B"]
    y_values = np.linspace(float(panel_b["yMinimum"]), float(panel_b["yMaximum"]), int(panel_b["samples"]))
    q2_lower = 4.0 * z2_lower * np.exp(-3.0 * y_values)
    q2_center = 4.0 * center_z2 * np.exp(-3.0 * y_values)
    q2_upper = (
        4.0 * z2_upper * np.exp(-3.0 * y_values)
        + 9.0 * radius_z3 * np.exp(-8.0 * y_values)
    )
    ax.fill_between(y_values, q2_lower, q2_upper, color=palette["blueLight"], alpha=0.65,
                    label=r"all $K$ heat paths")
    ax.plot(y_values, q2_lower, color=palette["blue"], lw=0.9, linestyle="--")
    ax.plot(y_values, q2_center, color=palette["blueDark"], lw=1.2, label="center path")
    ax.plot(y_values, q2_upper, color=palette["blue"], lw=0.9, linestyle="--")
    ax.axhline(old_q2_boundary, color=palette["ochre"], lw=1.0, linestyle=":",
               label=r"old $Q_2=1/2$ boundary")
    for series, values, note in (
        ("lower heat envelope", q2_lower, "4*(7/50)*exp(-3y)"),
        ("center heat path", q2_center, "4*(3/20)*exp(-3y)"),
        ("upper heat envelope", q2_upper, "4*(4/25)*exp(-3y)+9/1000*exp(-8y)"),
        ("old Q2 boundary", np.full_like(y_values, old_q2_boundary), "Q2=1/2"),
    ):
        for y_value, q_value in zip(y_values, values):
            add_row(rows, panel="B", route="heat-path", series=series,
                    kind="analytic-curve", x=y_value, y=q_value, phi=y_value,
                    source="research/r072r_report-source.md", pointer="(0.6)-(0.7)",
                    status="proved", note=note)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 0.69)
    ax.set_xlabel(r"heat variable $y$", fontsize=7.0)
    ax.set_ylabel(r"weighted jet $Q_2(y)$", fontsize=7.0)
    title(ax, "B", "Crossing a sufficient boundary", "all paths enter the old cone without a caustic", palette)
    ax.legend(loc="upper right", fontsize=5.5, frameon=False, handlelength=2.2)

    # Panel C: conservative shape envelopes.
    ax = axes[2]
    surface(ax, palette)
    panel_c = config["panels"]["C"]
    distances = np.linspace(float(panel_c["distanceMinimum"]), float(panel_c["distanceMaximum"]), int(panel_c["samples"]))
    r_value = float(parameters["criticalLocalization"])
    normalized_local_lower = float(parameters["normalizedLocalSlopeLower"])
    normalized_local_upper = float(parameters["normalizedLocalSlopeUpper"])
    normalized_away_gap = float(parameters["normalizedAwayGap"])
    physical_local_lower = 1.0 / math.sqrt(float(parameters["shapeC0"]))
    physical_away_gap = 1.0 / float(parameters["shapeC1"])
    normalized_lower = np.where(
        distances <= r_value, normalized_local_lower * distances, normalized_away_gap
    )
    physical_lower = np.where(
        distances <= r_value, physical_local_lower * distances, physical_away_gap
    )
    local_upper = normalized_local_upper * np.minimum(distances, r_value)
    scaled_distance = distances / r_value
    ax.plot(scaled_distance, normalized_lower, color=palette["ink"], lw=1.15,
            label=r"normalized $F$: certified lower")
    ax.plot(scaled_distance, physical_lower, color=palette["blue"], lw=1.2,
            label=r"physical $W$: certified lower")
    ax.plot(scaled_distance, local_upper, color=palette["muted"], lw=0.85,
            linestyle="--", label=r"local upper envelope")
    ax.axvline(1.0, color=palette["ochre"], lw=0.9, linestyle=":")
    for series, values, note in (
        ("normalized certified lower", normalized_lower, "d/4 locally; 1/80 away"),
        ("physical certified lower", physical_lower, "d/12 locally; 1/240 away"),
        ("local upper envelope", local_upper, "(5/3)*min(d,r)"),
    ):
        for distance, value in zip(distances, values):
            add_row(rows, panel="C", route="shape-contract", series=series,
                    kind="analytic-envelope", x=distance, y=value, distance=distance,
                    source="research/r072r_report-source.md", pointer="(4.5)-(4.12)",
                    status="proved", note=note)
    ax.text(1.06, max(local_upper) * 0.63, r"$d=r=\pi/48$",
            fontsize=5.8, color=palette["ochre"], va="center", ha="left")
    ax.set_xlim(0.0, float(panel_c["distanceMaximum"]) / r_value)
    ax.set_ylim(0.0, max(local_upper) * 1.08)
    ax.set_xlabel(r"distance from the critical set, $d/r$", fontsize=7.0)
    ax.set_ylabel(r"certified bound for $|\partial_\phi(\cdot)|$", fontsize=7.0)
    title(ax, "C", "Quantitative shape contract", "normalized and physical lower bounds kept distinct", palette)
    ax.legend(loc="center right", fontsize=5.4, frameon=False, handlelength=2.2)

    fig.text(0.055, 0.055,
             "R0.72R  |  exact-formula presentation; no PDE solve or chamber fit  |  Clay problem remains open",
             fontsize=5.4, color=palette["muted"], ha="left")

    with (ROOT / "data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    fig.savefig(ROOT / "figure.pdf", facecolor=palette["paper"])
    fig.savefig(ROOT / "figure.svg", facecolor=palette["paper"])
    fig.savefig(ROOT / "figure.png", dpi=int(config["figure"]["pngDpi"]), facecolor=palette["paper"])
    plt.close(fig)

    arc_residual = np.max(np.abs(12.0 * arc_b * x_values**2 + 4.0 * arc_a * x_values + 1.0 - 3.0 * arc_b))
    arc_derivative_residual = np.max(np.abs(24.0 * arc_b * x_values + 4.0 * arc_a))
    formula_checks = {
        "realSliceArcQResidualMaximum": float(arc_residual),
        "realSliceArcQPrimeResidualMaximum": float(arc_derivative_residual),
        "lowerEnvelopeAtZero": float(q2_lower[0]),
        "upperEnvelopeAtZero": float(q2_upper[0]),
        "upperEnvelopeAtOne": float(q2_upper[-1]),
        "allHeatEnvelopesStartAboveOldBoundary": bool(q2_lower[0] > old_q2_boundary),
        "allHeatEnvelopesEndBelowOldBoundary": bool(q2_upper[-1] < old_q2_boundary),
        "normalizedLocalSlopeAtR": float(normalized_local_lower * r_value),
        "physicalAwayFloor": physical_away_gap,
    }
    counts = {panel: sum(row["panel"] == panel for row in rows) for panel in "ABC"}
    elapsed = time.perf_counter() - started
    results = {
        "schemaVersion": "r072r-figure-results-v1",
        "status": "passed",
        "rowCount": len(rows),
        "panelRowCounts": counts,
        "formulaChecks": formula_checks,
        "elapsedSeconds": elapsed,
        "maxRssMb": max_rss_mb(),
        "noPdeEvolution": True,
        "noFiniteFit": True,
        "numericSamplingDoesNotReplaceContinuousProof": True,
        "repositoryCommitAtBuild": commit,
        "formalSourceCommit": source_commit,
        "verifiedTrackedTreeClean": True,
        "verifiedPackageSourcesAtBuildCommit": True,
        "packageSourceGitBlobs": source_blobs,
        "packageSourceHashes": {name: sha256(ROOT / name) for name in PACKAGE_SOURCES},
        "runtimeLineage": lineage,
        "lineageStatuses": {
            "producer": "passed", "independent": "passed", "crosscheck": "passed",
            "formalSourceReady": True, "temporaryUnsealedSourceAllowed": False,
        },
        "certificateLedgerAudit": ledger,
        "claimBoundary": contract["claimBoundary"],
    }
    (ROOT / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    environment = [
        "bundle=R0.72R exact-formula journal figure",
        f"pythonExecutable={sys.executable}",
        f"pythonVersion={sys.version.replace(chr(10), ' ')}",
        f"numpyVersion={np.__version__}",
        f"matplotlibVersion={mpl.__version__}",
        f"platform={platform.platform()}",
        f"machine={platform.machine()}",
        f"cpuCount={os.cpu_count()}",
        f"repositoryCommit={commit}",
        "gpu=not used",
        "dgx=not used",
    ]
    (ROOT / "environment.txt").write_text("\n".join(environment) + "\n", encoding="utf-8")
    with (ROOT / "progress.ndjson").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"time": utc_now(), "event": "data-ready", "rows": len(rows), "counts": counts}) + "\n")
        handle.write(json.dumps({"time": utc_now(), "event": "complete", "elapsedSeconds": elapsed}) + "\n")
    (ROOT / "resource-log.ndjson").write_text(
        json.dumps({"time": utc_now(), "event": "complete", "elapsedSeconds": elapsed,
                    "maxRssMb": results["maxRssMb"], "rows": len(rows), "pid": os.getpid()}) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "passed", "rows": len(rows), "counts": counts,
                      "elapsedSeconds": elapsed}, indent=2))


if __name__ == "__main__":
    main()
