#!/usr/bin/env python3
"""Build the R0.72P two-carrier superposition-gate journal figure.

All curves are direct evaluations of analytic formulas. Runtime certificate
files gate lineage only; this script does not solve a PDE, fit an exponent, or
interpolate certificate rows.
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
from matplotlib.lines import Line2D
import numpy as np

from certificate_ledger import verify_flat_certificate_ledger


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
PACKAGE_SOURCES = (
    "README.md",
    "caption.md",
    "figure-contract.md",
    "contract.json",
    "config.json",
    "command.txt",
    "requirements.txt",
    "certificate_ledger.py",
    "plot.py",
    "qa_images.py",
    "publish_assets.py",
    "validate.py",
    "build_manifest.py",
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
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=REPOSITORY,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unavailable"


def require_tracked_tree_clean() -> None:
    for command in (
        ("git", "diff", "--quiet", "--"),
        ("git", "diff", "--cached", "--quiet", "--"),
    ):
        completed = subprocess.run(command, cwd=REPOSITORY, check=False)
        if completed.returncode == 1:
            raise RuntimeError("formal figure build rejects tracked or staged repository drift")
        if completed.returncode != 0:
            raise RuntimeError(f"unable to verify tracked-tree cleanliness: {' '.join(command)}")


def package_source_git_blobs(commit: str) -> dict[str, str]:
    if FULL_SHA.fullmatch(commit) is None:
        raise RuntimeError("formal figure build requires a full repository HEAD commit")
    records: dict[str, str] = {}
    for name in PACKAGE_SOURCES:
        path = (ROOT / name).resolve()
        relative = str(path.relative_to(REPOSITORY.resolve()))
        try:
            object_type = subprocess.check_output(
                ["git", "cat-file", "-t", f"{commit}:{relative}"],
                cwd=REPOSITORY,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
            commit_blob = subprocess.check_output(
                ["git", "rev-parse", f"{commit}:{relative}"],
                cwd=REPOSITORY,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
            working_blob = subprocess.check_output(
                ["git", "hash-object", f"--path={relative}", str(path)],
                cwd=REPOSITORY,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(f"package source is not tracked at {commit}: {relative}") from exc
        if object_type != "blob" or commit_blob != working_blob:
            raise RuntimeError(f"package source does not match {commit}:{relative}")
        records[relative] = commit_blob
    return records


def append_ndjson(path: Path, value: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True) + "\n")


def load_lineage(
    path_text: str,
    label: str,
    *,
    json_required: bool,
    passed_required: bool = False,
) -> tuple[Path, dict[str, Any] | None]:
    path = Path(path_text).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"{label} does not exist: {path}")
    if not json_required:
        return path, None
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} must be a JSON object: {path}")
    if passed_required and value.get("status") != "passed":
        raise RuntimeError(f"{label} must be a JSON object with status=passed: {path}")
    return path, value


def require_formal_source_lineage(
    producer_config: dict[str, Any],
    independent_config: dict[str, Any],
    crosscheck: dict[str, Any],
) -> str:
    checks = crosscheck.get("checks")
    if not isinstance(checks, dict):
        raise RuntimeError("crosscheck.checks must be an object")
    source_commit = crosscheck.get("sourceCommit")
    if not isinstance(source_commit, str) or FULL_SHA.fullmatch(source_commit) is None:
        raise RuntimeError("crosscheck.sourceCommit must be 40 lowercase hexadecimal characters")
    if checks.get("formalSourceReady") is not True:
        raise RuntimeError("crosscheck.checks.formalSourceReady must be true")
    if checks.get("sourceCommitMatches") is not True:
        raise RuntimeError("crosscheck.checks.sourceCommitMatches must be true")
    if checks.get("sourceReadyOrExplicitlyAllowed") is not True:
        raise RuntimeError("crosscheck.checks.sourceReadyOrExplicitlyAllowed must be true")
    if checks.get("producerPassed") is not True or checks.get("independentPassed") is not True:
        raise RuntimeError("crosscheck must bind two passed audit routes")
    if crosscheck.get("temporaryUnsealedSourceAllowed") is not False:
        raise RuntimeError("temporary or unsealed crosschecks are forbidden")
    for label, route_config in (
        ("producer", producer_config),
        ("independent", independent_config),
    ):
        if route_config.get("gitCommit") != source_commit:
            raise RuntimeError(f"{label} config does not bind crosscheck.sourceCommit")
        if route_config.get("sourceTracked") is not True:
            raise RuntimeError(f"{label} config sourceTracked must be true")
        if route_config.get("trackedChangesDirty") is not False:
            raise RuntimeError(f"{label} config trackedChangesDirty must be false")
    return source_commit


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analytic-source", required=True)
    parser.add_argument("--producer-config", required=True)
    parser.add_argument("--producer-result", required=True)
    parser.add_argument("--independent-config", required=True)
    parser.add_argument("--independent-result", required=True)
    parser.add_argument("--crosscheck", required=True)
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    return parser.parse_args()


def full_profile(y_value: float | np.ndarray, phi: np.ndarray, lam: float) -> np.ndarray:
    return np.exp(-y_value) * np.cos(phi) + lam * np.exp(-4.0 * y_value) * np.cos(2.0 * phi)


def bracket(y_value: float | np.ndarray, phi: np.ndarray, lam: float) -> np.ndarray:
    return 1.0 + 4.0 * lam * np.exp(-3.0 * y_value) * np.cos(phi)


def l_r(r_value: np.ndarray | float) -> np.ndarray | float:
    return 1.0 + np.log(r_value)


def set_surface(ax: mpl.axes.Axes, config: dict[str, Any]) -> None:
    palette = config["palette"]
    ax.set_facecolor(palette["paper"])
    ax.grid(True, which="major", color=palette["grid"], linewidth=0.55, alpha=0.8)
    ax.grid(True, which="minor", color=palette["grid"], linewidth=0.35, alpha=0.35)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(palette["muted"])
        ax.spines[side].set_linewidth(0.65)
    ax.tick_params(axis="both", which="both", colors=palette["ink"], labelsize=7.0)


def panel_title(
    ax: mpl.axes.Axes,
    letter: str,
    title: str,
    subtitle: str,
    config: dict[str, Any],
) -> None:
    palette = config["palette"]
    ax.text(
        -0.02,
        1.095,
        letter,
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=11.0,
        fontweight="bold",
        color=palette["ink"],
    )
    ax.text(
        0.0,
        1.095,
        title,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9.2,
        fontweight="bold",
        color=palette["ink"],
    )
    ax.text(
        0.0,
        1.025,
        subtitle,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=6.7,
        color=palette["muted"],
    )


def research_blossom(fig: mpl.figure.Figure, config: dict[str, Any]) -> None:
    palette = config["palette"]
    ax = fig.add_axes([0.925, 0.902, 0.055, 0.065], zorder=20)
    ax.set_axis_off()
    angles = np.linspace(0.0, 2.0 * np.pi, 7)[:-1]
    for angle in angles:
        x = np.array([0.5, 0.5 + 0.34 * math.cos(angle)])
        y = np.array([0.5, 0.5 + 0.34 * math.sin(angle)])
        ax.plot(x, y, color=palette["ochre"], linewidth=0.8)
        ax.plot(
            [x[-1]],
            [y[-1]],
            marker="o",
            markersize=2.8,
            markerfacecolor=palette["paper"],
            markeredgecolor=palette["blue"],
            markeredgewidth=0.7,
        )
    ax.plot([0.5], [0.5], marker="o", markersize=3.2, color=palette["ink"])
    ax.set_xlim(0.05, 0.95)
    ax.set_ylim(0.05, 0.95)


def add_row(
    rows: list[dict[str, Any]],
    *,
    panel: str,
    route: str,
    series: str,
    kind: str,
    x: float,
    y: float,
    source: str,
    pointer: str,
    status: str,
    note: str,
    y_parameter: float | str = "",
    lambda_value: float | str = "",
    r_value: float | str = "",
    p_value: float | str = "",
) -> None:
    if not math.isfinite(float(x)) or not math.isfinite(float(y)):
        raise ValueError(f"non-finite plotted row: x={x}, y={y}")
    rows.append(
        {
            "panel": panel,
            "route": route,
            "series": series,
            "kind": kind,
            "x": f"{float(x):.17g}",
            "y": f"{float(y):.17g}",
            "yParameter": y_parameter,
            "lambda": lambda_value,
            "R": r_value,
            "p": p_value,
            "source": source,
            "pointer": pointer,
            "status": status,
            "note": note,
        }
    )


def main() -> None:
    started = time.perf_counter()
    require_tracked_tree_clean()
    build_commit = git_commit()
    source_git_blobs = package_source_git_blobs(build_commit)
    args = parse_args()
    output = args.output_dir.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))

    analytic_path, _ = load_lineage(args.analytic_source, "analytic source", json_required=False)
    producer_config_path, producer_config = load_lineage(
        args.producer_config, "producer config", json_required=True
    )
    producer_path, producer = load_lineage(
        args.producer_result,
        "producer result",
        json_required=True,
        passed_required=True,
    )
    independent_config_path, independent_config = load_lineage(
        args.independent_config, "independent config", json_required=True
    )
    independent_path, independent = load_lineage(
        args.independent_result,
        "independent result",
        json_required=True,
        passed_required=True,
    )
    crosscheck_path, crosscheck = load_lineage(
        args.crosscheck,
        "crosscheck",
        json_required=True,
        passed_required=True,
    )
    assert (
        producer_config is not None
        and producer is not None
        and independent_config is not None
        and independent is not None
        and crosscheck is not None
    )
    source_commit = require_formal_source_lineage(
        producer_config, independent_config, crosscheck
    )
    certificate_inputs = (
        producer_config_path,
        producer_path,
        independent_config_path,
        independent_path,
        crosscheck_path,
    )
    bindings = config["formalGitBindings"]
    certificate_roles = bindings["certificateCommitRoles"]
    canonical_certificate_directory = (
        REPOSITORY / Path(bindings["certificateLedgerPath"]).parent
    ).resolve()
    if {path.parent for path in certificate_inputs} != {
        canonical_certificate_directory
    }:
        raise RuntimeError("all runtime certificate JSON files must come from the canonical bundle directory")
    runtime_role_paths = {
        "producerConfig": producer_config_path,
        "producerResult": producer_path,
        "independentConfig": independent_config_path,
        "independentResult": independent_path,
        "crosscheck": crosscheck_path,
    }
    for role, relative in certificate_roles.items():
        if runtime_role_paths.get(role) != (REPOSITORY / relative).resolve():
            raise RuntimeError(f"runtime {role} is not the canonical certificate JSON")
    ledger_audit = verify_flat_certificate_ledger(
        canonical_certificate_directory,
        required_files={Path(relative).name for relative in certificate_roles.values()},
    )
    ledger_path = Path(ledger_audit["ledgerPath"])
    lineage_paths = {
        "analyticSource": analytic_path,
        "producerConfig": producer_config_path,
        "producerResult": producer_path,
        "independentConfig": independent_config_path,
        "independentResult": independent_path,
        "crosscheck": crosscheck_path,
        "certificateLedger": ledger_path,
    }

    progress = output / "progress.ndjson"
    resources = output / "resource-log.ndjson"
    progress.write_text("", encoding="utf-8")
    resources.write_text("", encoding="utf-8")
    append_ndjson(
        progress,
        {
            "time": utc_now(),
            "event": "start",
            "figureId": "fig-r072p-superposition-gate",
            "lineageInputs": len(lineage_paths),
        },
    )

    palette = config["palette"]
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8.0,
            "axes.labelcolor": palette["ink"],
            "text.color": palette["ink"],
            "figure.facecolor": palette["paper"],
            "savefig.facecolor": palette["paper"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "axes.unicode_minus": False,
        }
    )
    width = float(config["figure"]["widthMillimetres"]) / 25.4
    height = float(config["figure"]["heightMillimetres"]) / 25.4
    fig = plt.figure(figsize=(width, height), facecolor=palette["paper"])
    grid = fig.add_gridspec(
        2,
        2,
        left=0.085,
        right=0.975,
        bottom=0.105,
        top=0.815,
        wspace=0.27,
        hspace=0.43,
    )
    axes = [fig.add_subplot(grid[index // 2, index % 2]) for index in range(4)]
    for ax in axes:
        set_surface(ax, config)
    rows: list[dict[str, Any]] = []
    analytic_source = str(analytic_path)
    parameters = config["parameters"]
    lam = float(parameters["lambdaExample"])

    # Panel A: exact affine-cell reduction and full profile.
    ax = axes[0]
    panel = config["panels"]["A"]
    phi = np.linspace(panel["phiMinimum"], panel["phiMaximum"], panel["samples"])
    styles = (("-", 1.0), ("--", 0.78), (":", 0.58))
    for y_value, (linestyle, alpha) in zip(panel["ySlices"], styles, strict=True):
        values = full_profile(float(y_value), phi, lam)
        ax.plot(
            phi,
            values,
            color=palette["blue"],
            linewidth=1.65,
            linestyle=linestyle,
            alpha=alpha,
            label=rf"$y={float(y_value):g}$",
        )
        for x_value, value in zip(phi, values, strict=True):
            add_row(
                rows,
                panel="A",
                route="exact cell reduction",
                series=f"full profile y={float(y_value):g}",
                kind="proved analytic identity",
                x=x_value,
                y=value,
                source=analytic_source,
                pointer="R0.72P affine-row reduction",
                status="proved declared two-carrier class",
                note="Direct formula evaluation; no PDE evolution.",
                y_parameter=float(y_value),
                lambda_value=lam,
                p_value=parameters["p"],
            )
    ax.axhline(0.0, color=palette["muted"], linewidth=0.7)
    ax.text(
        0.03,
        0.06,
        r"$\pm R,\pm2R\ \mapsto\ \cos\phi,\cos2\phi$",
        transform=ax.transAxes,
        fontsize=6.4,
        color=palette["muted"],
    )
    ax.set_xlabel(r"cell coordinate $\phi$", fontsize=7.4)
    ax.set_ylabel(r"full shear $W(y,\phi)$", fontsize=7.4)
    ax.set_xticks([-math.pi, 0.0, math.pi], [r"$-\pi$", "0", r"$\pi$"])
    ax.legend(loc="upper right", frameon=False, fontsize=6.2, handlelength=2.0)
    panel_title(
        ax,
        "A",
        "Exact two-carrier cell reduction",
        r"paired $\pm$ shifts give factor $2$; $\varepsilon$ absorbs it",
        config,
    )

    # Panel B: uniform bracket and fixed critical set.
    ax = axes[1]
    panel = config["panels"]["B"]
    phi_b = np.linspace(panel["phiMinimum"], panel["phiMaximum"], panel["samples"])
    lower = 1.0 - 0.5 * np.abs(np.cos(phi_b))
    upper = 1.0 + 0.5 * np.abs(np.cos(phi_b))
    example = bracket(0.0, phi_b, lam)
    ax.fill_between(phi_b, lower, upper, color=palette["blueLight"], alpha=0.9, label="safe-cone envelope")
    ax.plot(phi_b, lower, color=palette["blue"], linewidth=1.05, linestyle="--")
    ax.plot(phi_b, upper, color=palette["blue"], linewidth=1.05, linestyle="--")
    ax.plot(phi_b, example, color=palette["ink"], linewidth=1.25, linestyle="-.", label=r"$\lambda=1/8,y=0$")
    for critical in (-math.pi, 0.0, math.pi):
        ax.axvline(critical, color=palette["ochre"], linewidth=0.75, linestyle=":")
    ax.text(0.5, 0.08, r"fixed critical set $\{0,\pi\}$", transform=ax.transAxes, ha="center", fontsize=6.25, color=palette["ochre"])
    for series, values, kind, status in (
        ("bracket lower envelope", lower, "proved envelope", "proved safe cone"),
        ("bracket upper envelope", upper, "proved envelope", "proved safe cone"),
        ("positive-boundary bracket", example, "analytic reference", "proved boundary member"),
    ):
        for x_value, value in zip(phi_b, values, strict=True):
            add_row(
                rows,
                panel="B",
                route="exact bracket algebra",
                series=series,
                kind=kind,
                x=x_value,
                y=value,
                source=analytic_source,
                pointer="W_phi factorization and shape bounds",
                status=status,
                note="Envelope is analytic over all |lambda|<=1/8 and 0<=y<=1.",
                lambda_value=lam if series == "positive-boundary bracket" else "safe cone",
            )
    ax.set_ylim(0.35, 1.65)
    ax.set_xlabel(r"cell coordinate $\phi$", fontsize=7.4)
    ax.set_ylabel(r"shape bracket $|1+4\lambda e^{-3y}\cos\phi|$", fontsize=7.15)
    ax.set_xticks([-math.pi, 0.0, math.pi], [r"$-\pi$", "0", r"$\pi$"])
    ax.legend(loc="upper center", frameon=False, fontsize=6.1, ncol=2, handlelength=1.8)
    panel_title(
        ax,
        "B",
        "Uniform shape bracket",
        r"bracket $\in[1/2,3/2]$ leaves only the two sine zeros",
        config,
    )

    # Panel C: exact time-slice Morse wall and safe cone.
    ax = axes[2]
    panel = config["panels"]["C"]
    y_grid = np.linspace(panel["yMinimum"], panel["yMaximum"], panel["samples"])
    wall = 0.25 * np.exp(3.0 * y_grid)
    safe = np.full_like(y_grid, float(parameters["lambdaSafe"]))
    display_floor = 1.0 / 32.0
    ax.semilogy(y_grid, wall, color=palette["ochre"], linewidth=1.75, label=r"Morse wall $e^{3y}/4$")
    ax.semilogy(y_grid, safe, color=palette["blue"], linewidth=1.45, label=r"safe ceiling $1/8$")
    ax.fill_between(y_grid, display_floor, safe, color=palette["blueLight"], alpha=0.85)
    ax.scatter([0.0], [0.25], s=28, marker="s", facecolor=palette["paper"], edgecolor=palette["ochre"], linewidth=0.9, zorder=5)
    ax.text(0.035, 0.87, r"first wall: $|\lambda|=1/4$", transform=ax.transAxes, fontsize=6.3, color=palette["ochre"])
    ax.text(0.62, 0.12, "shading lower edge is\na display cutoff only", transform=ax.transAxes, fontsize=5.8, color=palette["muted"], ha="center")
    for series, values, kind, status in (
        ("time-slice Morse wall", wall, "exact applicability boundary", "exact wall; not ED failure"),
        ("safe-cone ceiling", safe, "proved sufficient boundary", "proved safe cone"),
    ):
        for x_value, value in zip(y_grid, values, strict=True):
            add_row(
                rows,
                panel="C",
                route="exact critical-point algebra",
                series=series,
                kind=kind,
                x=x_value,
                y=value,
                source=analytic_source,
                pointer="1+4 lambda exp(-3y) cos(phi)=0",
                status=status,
                note="Wall controls this Morse certificate only.",
                y_parameter=x_value,
                lambda_value=value,
            )
    ax.set_ylim(display_floor, 8.0)
    ax.set_xlabel(r"parabolic cell time $y$", fontsize=7.4)
    ax.set_ylabel(r"coefficient magnitude $|\lambda|$", fontsize=7.4)
    ax.legend(loc="lower right", frameon=False, fontsize=6.15, handlelength=2.0)
    panel_title(
        ax,
        "C",
        "Exact Morse wall",
        r"safe cone stays separated; the wall is not an ED counterexample",
        config,
    )

    # Panel D: R0.72O conditional ledger promoted in the declared P class.
    # The curve is only the fixed-polynomial-coupling representative
    # L_(R,epsilon) asymp 1+log R; the exact ledger retains L_(R,epsilon).
    ax = axes[3]
    panel = config["panels"]["D"]
    r_grid = np.geomspace(panel["rMinimum"], panel["rMaximum"], panel["samples"])
    p_value = float(parameters["p"])
    window = p_value ** (4.0 / 3.0) * r_grid ** (4.0 / 3.0) * l_r(r_grid) ** 2
    ax.loglog(
        r_grid,
        window,
        color=palette["blue"],
        linewidth=1.8,
        label="fixed-polynomial representative",
    )
    anchors = np.array(panel["statusAnchors"], dtype=float)
    anchor_window = p_value ** (4.0 / 3.0) * anchors ** (4.0 / 3.0) * l_r(anchors) ** 2
    ax.scatter(anchors, anchor_window, s=43, marker="s", facecolor=palette["paper"], edgecolor=palette["ochre"], linewidth=1.0, zorder=5)
    ax.scatter(anchors, anchor_window, s=18, marker="o", facecolor=palette["blue"], edgecolor=palette["ink"], linewidth=0.55, zorder=6)
    ax.text(
        0.04,
        0.08,
        r"full IED $\Rightarrow\ \mathcal C_\times\lesssim4a^2\sqrt\varepsilon$",
        transform=ax.transAxes,
        fontsize=6.1,
        color=palette["blue"],
    )
    for x_value, value in zip(r_grid, window, strict=True):
        add_row(
            rows,
            panel="D",
            route="R0.72P fixed-polynomial asymptotic algebra",
            series="proved-class physical-window representative",
            kind="proved-class asymptotic representative",
            x=x_value,
            y=value,
            source=analytic_source,
            pointer="exact ledger uses L_(R,epsilon)^2; fixed-polynomial coupling gives L_(R,epsilon) asymp 1+log R",
            status="proved declared two-carrier class",
            note="Not an exact all-epsilon window; theorem and comparability constants are suppressed.",
            r_value=x_value,
            p_value=p_value,
        )
    for x_value, value in zip(anchors, anchor_window, strict=True):
        for series, kind, status in (
            ("R0.72O conditional status marker", "historical conditional marker", "conditional before R0.72P shape proof"),
            ("R0.72P proved status marker", "proved theorem marker", "proved declared two-carrier class"),
        ):
            add_row(
                rows,
                panel="D",
                route="claim-status comparison",
                series=series,
                kind=kind,
                x=x_value,
                y=value,
                source=analytic_source,
                pointer="same p-ledger value; claim status changed",
                status=status,
                note="Open and filled marks share the same asymptotic representative value; there is no fitted uplift.",
                r_value=x_value,
                p_value=p_value,
            )
    legend_handles = [
        Line2D([0], [0], color=palette["blue"], linewidth=1.8, label="P proved-class representative"),
        Line2D([0], [0], marker="s", linestyle="none", markerfacecolor=palette["paper"], markeredgecolor=palette["ochre"], label="O conditional status"),
        Line2D([0], [0], marker="o", linestyle="none", markerfacecolor=palette["blue"], markeredgecolor=palette["ink"], label="P proved status"),
    ]
    ax.set_xlabel(r"carrier scale $R$", fontsize=7.4)
    ax.set_ylabel(r"physical-window representative", fontsize=7.4)
    ax.legend(handles=legend_handles, loc="upper left", frameon=False, fontsize=5.95, handlelength=1.9, labelspacing=0.25)
    panel_title(
        ax,
        "D",
        "Physical ledger proved in one class",
        r"fixed-polynomial coupling: $L_{R,\varepsilon}\asymp1+\log R$ only",
        config,
    )

    fig.text(
        0.085,
        0.952,
        "TWO-CARRIER SUPERPOSITION · VERIFIED MORSE GATE",
        ha="left",
        va="top",
        fontsize=11.8,
        fontweight="bold",
        color=palette["ink"],
    )
    fig.text(
        0.085,
        0.910,
        r"The full $(R,2R)$ profile closes the R0.72O ED hypothesis only inside a declared coefficient cone and affine row.",
        ha="left",
        va="top",
        fontsize=7.25,
        color=palette["muted"],
    )
    fig.text(
        0.085,
        0.030,
        "Blue/filled = proved in R0.72P; ochre/open = boundary or prior conditional status.",
        ha="left",
        va="bottom",
        fontsize=5.9,
        color=palette["muted"],
    )
    fig.text(
        0.085,
        0.012,
        "Panel D is a fixed-polynomial asymptotic representative; constants are suppressed and the exact ledger retains L(R,epsilon).",
        ha="left",
        va="bottom",
        fontsize=5.9,
        color=palette["muted"],
    )
    research_blossom(fig, config)

    fieldnames = [
        "panel",
        "route",
        "series",
        "kind",
        "x",
        "y",
        "yParameter",
        "lambda",
        "R",
        "p",
        "source",
        "pointer",
        "status",
        "note",
    ]
    with (output / "data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    append_ndjson(
        progress,
        {
            "time": utc_now(),
            "event": "data-ready",
            "rows": len(rows),
            "panels": {name: sum(row["panel"] == name for row in rows) for name in "ABCD"},
        },
    )

    pdf_metadata = {
        "Title": contract["title"],
        "Author": "Kasifa Navier-Stokes research log",
        "Subject": contract["supportedTakeaway"],
        "Keywords": "Navier-Stokes, enhanced dissipation, Morse shear, two-carrier superposition",
    }
    svg_metadata = {
        "Title": contract["title"],
        "Creator": "Kasifa Navier-Stokes research log",
        "Description": contract["supportedTakeaway"],
        "Keywords": ["Navier-Stokes", "enhanced dissipation", "Morse shear", "two-carrier"],
    }
    fig.savefig(output / "figure.pdf", metadata=pdf_metadata)
    fig.savefig(output / "figure.svg", metadata=svg_metadata)
    fig.savefig(
        output / "figure.png",
        dpi=int(config["figure"]["pngDpi"]),
        metadata={"Software": "Matplotlib"},
    )
    plt.close(fig)

    elapsed = time.perf_counter() - started
    lineage_status = {
        "analyticSource": "source",
        "producerConfig": "formal-ready-config",
        "producerResult": "passed",
        "independentConfig": "formal-ready-config",
        "independentResult": "passed",
        "crosscheck": "passed-formal-source-only",
        "certificateLedger": "passed-flat-ledger",
    }
    lineage = {
        name: {
            "path": str(path),
            "sha256": sha256(path),
            "status": lineage_status[name],
        }
        for name, path in lineage_paths.items()
    }
    results = {
        "schemaVersion": "r072p-figure-results-v1",
        "figureId": "fig-r072p-superposition-gate",
        "status": "passed",
        "rowCount": len(rows),
        "panelRowCounts": {name: sum(row["panel"] == name for row in rows) for name in "ABCD"},
        "runtimeLineage": lineage,
        "lineageStatuses": {
            "producer": producer.get("status"),
            "independent": independent.get("status"),
            "crosscheck": crosscheck.get("status"),
            "formalSourceReady": crosscheck["checks"].get("formalSourceReady"),
            "temporaryUnsealedSourceAllowed": crosscheck.get(
                "temporaryUnsealedSourceAllowed"
            ),
        },
        "formalSourceCommit": source_commit,
        "certificateLedgerAudit": ledger_audit,
        "parameters": {
            "N": 2,
            "B": 2,
            "p": p_value,
            "lambdaSafe": parameters["lambdaSafe"],
            "shapeC0": parameters["shapeC0"],
            "shapeC1": parameters["shapeC1"],
        },
        "formulaChecks": {
            "bracketLower": float(np.min(lower)),
            "bracketUpper": float(np.max(upper)),
            "morseWallAtYZero": float(wall[0]),
            "windowRepresentativePFactor": p_value ** (4.0 / 3.0),
            "expectedWindowRepresentativePFactor": 2.0 ** (-2.0 / 3.0),
            "exactLedgerRetainsLREpsilon": True,
            "displayedWindowIsFixedPolynomialAsymptoticRepresentative": True,
        },
        "noPdeEvolution": True,
        "noFiniteFit": True,
        "formulaCurvesNotCertificateInterpolation": True,
        "verifiedTrackedTreeClean": True,
        "verifiedPackageSourcesAtBuildCommit": True,
        "packageSourceGitBlobs": source_git_blobs,
        "elapsedSeconds": elapsed,
        "maxRssMb": max_rss_mb(),
        "repositoryCommitAtBuild": build_commit,
        "packageSourceHashes": {
            name: sha256(ROOT / name) for name in PACKAGE_SOURCES if (ROOT / name).is_file()
        },
    }
    (output / "results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output / "environment.txt").write_text(
        "\n".join(
            [
                f"Python {platform.python_version()}",
                f"Matplotlib {mpl.__version__}",
                f"NumPy {np.__version__}",
                f"Platform {platform.platform()}",
                f"Repository commit {results['repositoryCommitAtBuild']}",
                "Runtime lineage is recorded in results.json.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    append_ndjson(
        resources,
        {
            "time": utc_now(),
            "elapsedSeconds": elapsed,
            "maxRssMb": max_rss_mb(),
            "rows": len(rows),
        },
    )
    append_ndjson(progress, {"time": utc_now(), "event": "complete", "status": "passed"})
    print(json.dumps({"status": "passed", "rows": len(rows), "output": str(output)}, sort_keys=True))


if __name__ == "__main__":
    main()
