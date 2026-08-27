#!/usr/bin/env python3
"""Build the R0.72Q phase-robust-shape journal figure.

All curves are direct samples of exact analytic formulas. Runtime certificate
files gate lineage only; this script does not solve a PDE, fit an exponent, or
replace the continuous proof by numerical sampling.
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



def caustic(phi: np.ndarray) -> np.ndarray:
    """Exact 1:2 degeneracy caustic in the complex second-mode coefficient."""
    return 0.125 * np.exp(-3.0j * phi) - 0.375 * np.exp(-1.0j * phi)


def caustic_implicit_residual(z_value: np.ndarray) -> np.ndarray:
    """Residual of the exact implicit caustic equation."""
    return (
        (np.abs(z_value) ** 2 - 1.0 / 16.0) ** 3
        - (27.0 / 1024.0) * np.imag(z_value) ** 2
    )


def normalized_curvature_lower(distance: np.ndarray) -> np.ndarray:
    """Fixed-M lower bound |F''| >= cos(d)-Q2 with Q2<=1/2."""
    return np.cos(distance) - 0.5


def normalized_away_gradient_lower(distance: np.ndarray) -> np.ndarray:
    """Fixed-M lower bound |F'| >= sin(d)-Q1 with Q1<=1/4."""
    return np.sin(distance) - 0.25


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
    ax.text(-0.02, 1.095, letter, transform=ax.transAxes, ha="right", va="top",
            fontsize=11.0, fontweight="bold", color=palette["ink"])
    ax.text(0.0, 1.095, title, transform=ax.transAxes, ha="left", va="top",
            fontsize=8.8, fontweight="bold", color=palette["ink"])
    ax.text(0.0, 1.025, subtitle, transform=ax.transAxes, ha="left", va="top",
            fontsize=6.3, color=palette["muted"])


def research_blossom(fig: mpl.figure.Figure, config: dict[str, Any]) -> None:
    palette = config["palette"]
    ax = fig.add_axes([0.925, 0.902, 0.055, 0.065], zorder=20)
    ax.set_axis_off()
    angles = np.linspace(0.0, 2.0 * np.pi, 7)[:-1]
    for angle in angles:
        x = np.array([0.5, 0.5 + 0.34 * math.cos(angle)])
        y = np.array([0.5, 0.5 + 0.34 * math.sin(angle)])
        ax.plot(x, y, color=palette["ochre"], linewidth=0.8)
        ax.plot([x[-1]], [y[-1]], marker="o", markersize=2.8,
                markerfacecolor=palette["paper"], markeredgecolor=palette["blue"],
                markeredgewidth=0.7)
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
    phi: float | str = "",
    theta: float | str = "",
    radius: float | str = "",
    distance: float | str = "",
) -> None:
    if not math.isfinite(float(x)) or not math.isfinite(float(y)):
        raise ValueError(f"non-finite plotted row: x={x}, y={y}")
    rows.append({
        "panel": panel,
        "route": route,
        "series": series,
        "kind": kind,
        "x": f"{float(x):.17g}",
        "y": f"{float(y):.17g}",
        "phi": phi,
        "theta": theta,
        "radius": radius,
        "distance": distance,
        "source": source,
        "pointer": pointer,
        "status": status,
        "note": note,
    })


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
        args.producer_result, "producer result", json_required=True, passed_required=True
    )
    independent_config_path, independent_config = load_lineage(
        args.independent_config, "independent config", json_required=True
    )
    independent_path, independent = load_lineage(
        args.independent_result, "independent result", json_required=True, passed_required=True
    )
    crosscheck_path, crosscheck = load_lineage(
        args.crosscheck, "crosscheck", json_required=True, passed_required=True
    )
    assert all(value is not None for value in (
        producer_config, producer, independent_config, independent, crosscheck
    ))
    source_commit = require_formal_source_lineage(
        producer_config, independent_config, crosscheck
    )

    certificate_inputs = (
        producer_config_path, producer_path, independent_config_path,
        independent_path, crosscheck_path,
    )
    bindings = config["formalGitBindings"]
    certificate_roles = bindings["certificateCommitRoles"]
    canonical_certificate_directory = (
        REPOSITORY / Path(bindings["certificateLedgerPath"]).parent
    ).resolve()
    if {path.parent for path in certificate_inputs} != {canonical_certificate_directory}:
        raise RuntimeError(
            "all runtime certificate JSON files must come from the canonical bundle directory"
        )
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
    append_ndjson(progress, {
        "time": utc_now(), "event": "start",
        "figureId": "fig-r072q-phase-robust-shape",
        "lineageInputs": len(lineage_paths),
    })

    palette = config["palette"]
    mpl.rcParams.update({
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
    })
    width = float(config["figure"]["widthMillimetres"]) / 25.4
    height = float(config["figure"]["heightMillimetres"]) / 25.4
    fig = plt.figure(figsize=(width, height), facecolor=palette["paper"])
    grid = fig.add_gridspec(
        1, 3, left=0.062, right=0.978, bottom=0.185, top=0.805, wspace=0.34
    )
    axes = [fig.add_subplot(grid[0, index]) for index in range(3)]
    for ax in axes:
        set_surface(ax, config)

    rows: list[dict[str, Any]] = []
    analytic_source = str(analytic_path)
    parameters = config["parameters"]

    # Panel A: exact 1:2 caustic and two analytic safe disks.
    ax = axes[0]
    panel = config["panels"]["A"]
    phi_a = np.linspace(
        float(panel["phiMinimum"]), float(panel["phiMaximum"]), int(panel["samples"])
    )
    z_a = caustic(phi_a)
    circle_angle = np.linspace(0.0, 2.0 * np.pi, int(panel["circleSamples"]))
    outer_radius = float(parameters["oneTwoCausticFreeRadius"])
    contract_radius = float(parameters["oneTwoContractRadius"])
    outer_circle = outer_radius * np.exp(1.0j * circle_angle)
    contract_circle = contract_radius * np.exp(1.0j * circle_angle)

    ax.fill(np.real(outer_circle), np.imag(outer_circle), color=palette["blueLight"],
            alpha=0.56, linewidth=0.0, label=r"phase-safe disk $|z|<1/4$")
    ax.fill(np.real(contract_circle), np.imag(contract_circle),
            color=palette["theoremFill"], alpha=0.98, linewidth=0.0,
            label=r"$Q_2\leq1/2$: $|z|\leq1/8$")
    ax.plot(np.real(outer_circle), np.imag(outer_circle), color=palette["blue"],
            linewidth=0.85, linestyle="--")
    ax.plot(np.real(contract_circle), np.imag(contract_circle),
            color=palette["blueDark"], linewidth=0.95)
    ax.plot(np.real(z_a), np.imag(z_a), color=palette["ochre"],
            linewidth=1.65, label="exact degeneracy caustic")
    ax.scatter([-0.25, 0.25], [0.0, 0.0], s=20, marker="s",
               facecolor=palette["paper"], edgecolor=palette["ochre"],
               linewidth=0.9, zorder=5)
    for x_value, y_value, phi_value, radius_value in zip(
        np.real(z_a), np.imag(z_a), phi_a, np.abs(z_a), strict=True
    ):
        add_row(
            rows, panel="A", route="exact 1:2 degeneracy algebra",
            series="caustic", kind="exact formula sample", x=x_value, y=y_value,
            phi=phi_value, radius=radius_value, source=analytic_source,
            pointer="z(phi)=exp(-3i phi)/8-3 exp(-i phi)/8",
            status="exact degeneracy locus",
            note="Sampled only for display; the implicit identity and radius bounds are continuous.",
        )
    for series, values, radius_value, status in (
        ("arbitrary-phase safe circle", outer_circle, outer_radius,
         "open disk is caustic-free"),
        ("Q2 contract circle", contract_circle, contract_radius,
         "closed general-contract slice"),
    ):
        for x_value, y_value, angle_value in zip(
            np.real(values), np.imag(values), circle_angle, strict=True
        ):
            add_row(
                rows, panel="A", route="analytic radial contract",
                series=series, kind="exact circle sample", x=x_value, y=y_value,
                theta=angle_value, radius=radius_value, source=analytic_source,
                pointer="|z|<1/4 and Q2=4|z|<=1/2", status=status,
                note="The sampled circle is a display of an exact analytic boundary.",
            )
    axis_limit = float(panel["axisLimit"])
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-axis_limit, axis_limit)
    ax.set_ylim(-axis_limit, axis_limit)
    ax.set_xlabel(r"$\operatorname{Re} z$", fontsize=7.2)
    ax.set_ylabel(r"$\operatorname{Im} z$", fontsize=7.2)
    ax.legend(loc="lower left", frameon=False, fontsize=5.55, handlelength=1.4)
    panel_title(
        ax, "A", "Exact 1:2 caustic",
        r"$|z|<1/4$ phase-safe; $Q_2\leq1/2$ gives $|z|\leq1/8$", config
    )

    # Panel B: exact radial graph of the same caustic.
    ax = axes[1]
    panel = config["panels"]["B"]
    phi_b = np.linspace(
        float(panel["phiMinimum"]), float(panel["phiMaximum"]), int(panel["samples"])
    )
    z_b = caustic(phi_b)
    theta_unwrapped = np.unwrap(np.angle(z_b))
    if float(theta_unwrapped[0]) < 0.0:
        theta_unwrapped = theta_unwrapped + 2.0 * np.pi
    radius_b = np.abs(z_b)
    ordering = np.argsort(theta_unwrapped)
    theta_b = theta_unwrapped[ordering]
    radius_star = radius_b[ordering]

    ax.fill_between(theta_b, 0.0, radius_star, color=palette["blueLight"],
                    alpha=0.62, label="radially caustic-free component")
    ax.plot(theta_b, radius_star, color=palette["ochre"], linewidth=1.65,
            label=r"unique wall $r_*(\theta)$")
    ax.axhline(outer_radius, color=palette["blue"], linewidth=0.9, linestyle="--")
    ax.axhline(float(parameters["oneTwoWallMaximumRadius"]),
               color=palette["muted"], linewidth=0.75, linestyle=":")
    for phi_value, theta_value, radius_value in zip(
        phi_b, theta_unwrapped, radius_b, strict=True
    ):
        add_row(
            rows, panel="B", route="exact caustic polar graph",
            series="phase-ray wall radius", kind="exact formula sample",
            x=theta_value, y=radius_value, phi=phi_value, theta=theta_value,
            radius=radius_value, source=analytic_source,
            pointer="polar form of the exact 1:2 caustic",
            status="one wall on every phase ray",
            note="Strict phase monotonicity is proved analytically; samples only display r_star.",
        )
    ax.set_xlim(float(panel["thetaMinimum"]), float(panel["thetaMaximum"]))
    ax.set_ylim(0.0, 0.54)
    ax.set_xticks(
        [-math.pi, -math.pi / 2.0, 0.0, math.pi / 2.0, math.pi],
        [r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"],
    )
    ax.set_xlabel(r"phase ray $\theta$", fontsize=7.2)
    ax.set_ylabel(r"first wall radius $r_*(\theta)$", fontsize=7.0)
    ax.legend(loc="lower center", frameon=False, fontsize=5.65, handlelength=1.5)
    panel_title(
        ax, "B", "One wall per phase ray",
        r"analytic radial graph: $1/4\leq r_*(\theta)\leq1/2$", config
    )

    # Panel C: fixed-M shape margins for F and formal W=e^{-y}F.
    ax = axes[2]
    panel = config["panels"]["C"]
    distance = np.linspace(
        float(panel["distanceMinimum"]), float(panel["distanceMaximum"]),
        int(panel["samples"]),
    )
    curvature = normalized_curvature_lower(distance)
    away_gradient = normalized_away_gradient_lower(distance)
    localization = float(parameters["criticalLocalization"])
    curvature_zone = float(parameters["curvatureZone"])
    mu = float(parameters["curvatureMu"])

    ax.axvspan(0.0, localization, color=palette["theoremFill"], alpha=0.9,
               label=r"localization $d\leq\pi/12$")
    ax.axvspan(localization, curvature_zone, color=palette["ochreLight"],
               alpha=0.45, label=r"curvature zone $d\leq\pi/6$")
    ax.axvspan(curvature_zone, math.pi / 2.0, color=palette["blueLight"],
               alpha=0.24, label=r"away zone $d\geq\pi/6$")
    ax.plot(distance, curvature, color=palette["blueDark"], linewidth=1.5,
            label=r"$\cos d-1/2$")
    ax.plot(distance, away_gradient, color=palette["ochre"], linewidth=1.35,
            linestyle="--", label=r"$\sin d-1/4$")
    ax.axhline(mu, color=palette["blue"], linewidth=0.8, linestyle=":")
    ax.axhline(1.0 / 12.0, color=palette["ochre"], linewidth=0.75, linestyle=":")
    ax.axhline(1.0 / 36.0, color=palette["muted"], linewidth=0.75, linestyle=":")
    ax.text(0.56, 0.85, r"$F$: away gap $>1/12$", transform=ax.transAxes,
            fontsize=5.9, color=palette["ochre"])
    ax.text(0.56, 0.76, r"$W=e^{-y}F$: $C_1=36$", transform=ax.transAxes,
            fontsize=5.9, color=palette["muted"])
    ax.text(0.56, 0.67, r"$C_0=81$", transform=ax.transAxes,
            fontsize=5.9, color=palette["blueDark"])
    for series, values, pointer, status in (
        ("normalized curvature lower bound", curvature,
         "|F''|>=cos(d)-Q2 with Q2<=1/2", "mu lower bound on d<=pi/6"),
        ("normalized away-gradient lower bound", away_gradient,
         "|F'|>=sin(d)-Q1 with Q1<=1/4",
         "normalized F away gap exceeds 1/12 only on d>=pi/6"),
    ):
        for distance_value, value in zip(distance, values, strict=True):
            add_row(
                rows, panel="C", route="fixed-M quantitative Morse inequalities",
                series=series, kind="exact lower-bound formula sample",
                x=distance_value, y=value, distance=distance_value,
                source=analytic_source, pointer=pointer, status=status,
                note=(
                    "The formal shear is W=e^{-y}F on 0<=y<=1; "
                    "its declared shape constants are C0=81 and C1=36."
                ),
            )
    ax.set_xlim(0.0, math.pi / 2.0)
    ax.set_ylim(-0.28, 0.78)
    ax.set_xticks(
        [0.0, math.pi / 12.0, math.pi / 6.0, math.pi / 2.0],
        ["0", r"$\pi/12$", r"$\pi/6$", r"$\pi/2$"],
    )
    ax.set_xlabel(r"distance $d$ to $\{0,\pi\}$", fontsize=7.0)
    ax.set_ylabel("analytic lower margin", fontsize=7.0)
    ax.legend(loc="lower right", frameon=False, fontsize=5.35, handlelength=1.45)
    panel_title(
        ax, "C", "Fixed-M analytic margins",
        r"$\mu=(\sqrt{3}-1)/2$; formal $W$: $(C_0,C_1)=(81,36)$", config
    )

    fig.text(0.062, 0.952, "PHASE-ROBUST MORSE SHAPE · EXACT CONTRACT",
             ha="left", va="top", fontsize=11.5, fontweight="bold",
             color=palette["ink"])
    fig.text(
        0.062, 0.909,
        r"Fixed $M$ and $Q_2\leq1/2$ give arbitrary-phase critical-point control; the 1:2 caustic is exact.",
        ha="left", va="top", fontsize=7.05, color=palette["muted"],
    )
    fig.text(
        0.062, 0.040,
        "All curves are samples of exact formulas for display; they cannot replace the continuous proof.",
        ha="left", va="bottom", fontsize=5.85, color=palette["muted"],
    )
    fig.text(
        0.062, 0.017,
        "Formal Coble shear: W=e^{-y}F on 0<=y<=1, with (r,C0,C1)=(pi/12,81,36).",
        ha="left", va="bottom", fontsize=5.85, color=palette["muted"],
    )
    research_blossom(fig, config)

    fieldnames = [
        "panel", "route", "series", "kind", "x", "y", "phi", "theta",
        "radius", "distance", "source", "pointer", "status", "note",
    ]
    with (output / "data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    append_ndjson(progress, {
        "time": utc_now(), "event": "data-ready", "rows": len(rows),
        "panels": {name: sum(row["panel"] == name for row in rows) for name in "ABC"},
    })

    pdf_metadata = {
        "Title": contract["title"],
        "Author": "Kasifa Navier-Stokes research log",
        "Subject": contract["supportedTakeaway"],
        "Keywords": "Navier-Stokes, enhanced dissipation, Morse shear, arbitrary phase",
    }
    svg_metadata = {
        "Title": contract["title"],
        "Creator": "Kasifa Navier-Stokes research log",
        "Description": contract["supportedTakeaway"],
        "Keywords": ["Navier-Stokes", "enhanced dissipation", "Morse shear", "arbitrary phase"],
    }
    fig.savefig(output / "figure.pdf", metadata=pdf_metadata)
    fig.savefig(output / "figure.svg", metadata=svg_metadata)
    fig.savefig(output / "figure.png", dpi=int(config["figure"]["pngDpi"]),
                metadata={"Software": "Matplotlib"})
    plt.close(fig)

    residual = caustic_implicit_residual(z_a)
    monotone_differences = np.diff(theta_unwrapped)
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
        name: {"path": str(path), "sha256": sha256(path), "status": lineage_status[name]}
        for name, path in lineage_paths.items()
    }
    results = {
        "schemaVersion": "r072q-figure-results-v1",
        "figureId": "fig-r072q-phase-robust-shape",
        "status": "passed",
        "rowCount": len(rows),
        "panelRowCounts": {
            name: sum(row["panel"] == name for row in rows) for name in "ABC"
        },
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
            "fixedMRequired": parameters["fixedMRequired"],
            "q2Maximum": parameters["q2Maximum"],
            "q1Maximum": parameters["q1Maximum"],
            "oneTwoCausticFreeRadius": outer_radius,
            "oneTwoContractRadius": contract_radius,
            "criticalLocalization": localization,
            "curvatureZone": curvature_zone,
            "curvatureMu": mu,
            "shapeC0": parameters["shapeC0"],
            "shapeC1": parameters["shapeC1"],
            "normalizedFShapeC1": parameters["normalizedFShapeC1"],
            "normalizedFAwayGapLower": parameters["normalizedFAwayGapLower"],
        },
        "formulaChecks": {
            "maxCausticImplicitResidual": float(np.max(np.abs(residual))),
            "minimumWallRadius": float(np.min(radius_b)),
            "maximumWallRadius": float(np.max(radius_b)),
            "phaseParameterStrictlyMonotone": bool(
                np.all(monotone_differences < 0.0)
            ),
            "q2AtContractRadius": 4.0 * contract_radius,
            "curvatureAtZoneBoundary": float(
                normalized_curvature_lower(np.array([curvature_zone]))[0]
            ),
            "expectedCurvatureMu": (math.sqrt(3.0) - 1.0) / 2.0,
            "normalizedAwayAtZoneBoundary": float(
                normalized_away_gradient_lower(np.array([curvature_zone]))[0]
            ),
            "numericCurvesAreExactFormulaSamples": True,
            "continuousProofRequired": True,
        },
        "noPdeEvolution": True,
        "noFiniteFit": True,
        "numericSamplingDoesNotReplaceContinuousProof": True,
        "verifiedTrackedTreeClean": True,
        "verifiedPackageSourcesAtBuildCommit": True,
        "packageSourceGitBlobs": source_git_blobs,
        "elapsedSeconds": elapsed,
        "maxRssMb": max_rss_mb(),
        "repositoryCommitAtBuild": build_commit,
        "packageSourceHashes": {
            name: sha256(ROOT / name) for name in PACKAGE_SOURCES
            if (ROOT / name).is_file()
        },
    }
    (output / "results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output / "environment.txt").write_text(
        "\n".join([
            f"Python {platform.python_version()}",
            f"Matplotlib {mpl.__version__}",
            f"NumPy {np.__version__}",
            f"Platform {platform.platform()}",
            f"Repository commit {results['repositoryCommitAtBuild']}",
            "Runtime lineage is recorded in results.json.",
            "",
        ]),
        encoding="utf-8",
    )
    append_ndjson(resources, {
        "time": utc_now(), "elapsedSeconds": elapsed,
        "maxRssMb": max_rss_mb(), "rows": len(rows),
    })
    append_ndjson(progress, {
        "time": utc_now(), "event": "complete", "status": "passed"
    })
    print(json.dumps(
        {"status": "passed", "rows": len(rows), "output": str(output)},
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()
