#!/usr/bin/env python3
"""Deterministic renderer for the R0.74Z analytic four-panel figure."""

from __future__ import annotations

import argparse
import atexit
import csv
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import resource
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any


_MPL_CONFIG = Path(tempfile.mkdtemp(prefix="r074z-mpl-"))
os.environ["MPLCONFIGDIR"] = str(_MPL_CONFIG)
atexit.register(lambda: shutil.rmtree(_MPL_CONFIG, ignore_errors=True))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import patches  # noqa: E402
from PIL import Image  # noqa: E402
import pypdfium2 as pdfium  # noqa: E402


HERE = Path(__file__).resolve().parent
DEFAULT_REPOSITORY = HERE.parents[3]
ARTIFACT_ID = "fig-r074z-remote-persistence-gate"
REQUIRED_LABEL = (
    "ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | "
    "NOT PDE DATA | NOT DNS | NO NOVELTY CLAIM | NOT CLAY"
)
FIXED_DATE = datetime(2026, 9, 3, 0, 0, 0, tzinfo=timezone.utc)

SOURCE_FILES = (
    "README.md",
    "caption.md",
    "chart-contract-and-source-data.md",
    "command.txt",
    "config.json",
    "contract.json",
    "plot.py",
    "qa-protocol.md",
    "requirements.txt",
    "validate.py",
)
RAW_FILES = (
    "environment.json",
    "figure.pdf",
    "figure.png",
    "figure.svg",
    "progress.ndjson",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "resource-log.ndjson",
    "results.json",
    "source-data.csv",
)
DETERMINISTIC_GENERATED_FILES = (
    "figure.pdf",
    "figure.png",
    "figure.svg",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "results.json",
    "source-data.csv",
)

PALETTE = {
    "root": "#244C70",
    "root_dark": "#173149",
    "root_light": "#AEBFCC",
    "root_open": "#E8EEF2",
    "ink": "#1F2529",
    "mid": "#747C82",
    "light": "#D9DDE0",
    "pale": "#F2F4F5",
    "paper": "#FFFFFF",
}

C_GAMMA = Fraction(8, 3969)
RHO = Fraction(9, 10000)
D = Fraction(7, 32)
A0 = Fraction(131, 2)
CLOCK_WEIGHT_EXPONENT = Fraction(1, 4)
PAYMENT_WEIGHT_EXPONENT = Fraction(1, 16)
BETA = D * D / (4 * A0)
TIME_TAME_RESERVE = RHO / 4 - BETA
DELTA_REMOTE = Fraction(5, 24) * C_GAMMA - RHO / 6
KAPPA_STAR = Fraction(3, 2) * DELTA_REMOTE
TWO_CENTER_RATE = D * D / (2 * A0)
TWO_CENTER_MARGIN = TWO_CENTER_RATE - Fraction(1, 5000)
COMPLEXITY_ESCAPE = TIME_TAME_RESERVE + KAPPA_STAR


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary_path = Path(temporary)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def atomic_json(path: Path, value: Any) -> None:
    atomic_text(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_ndjson(path: Path, payload: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def rss_bytes() -> int:
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value if platform.system() == "Darwin" else value * 1024


def log_progress(out_dir: Path, phase: str, ordinal: int, started: float) -> None:
    append_ndjson(
        out_dir / "progress.ndjson",
        {
            "artifactId": ARTIFACT_ID,
            "elapsedSeconds": round(time.monotonic() - started, 6),
            "ordinal": ordinal,
            "phase": phase,
            "timestampUtc": utc_now(),
        },
    )
    append_ndjson(
        out_dir / "resource-log.ndjson",
        {
            "artifactId": ARTIFACT_ID,
            "elapsedSeconds": round(time.monotonic() - started, 6),
            "ordinal": ordinal,
            "phase": phase,
            "residentSetBytes": rss_bytes(),
            "timestampUtc": utc_now(),
        },
    )


def repository_head(repository: Path) -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def total_memory_bytes() -> int | None:
    if platform.system() == "Darwin":
        try:
            return int(
                subprocess.run(
                    ["sysctl", "-n", "hw.memsize"],
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip()
            )
        except (OSError, subprocess.CalledProcessError, ValueError):
            return None
    meminfo = Path("/proc/meminfo")
    if meminfo.exists():
        for line in meminfo.read_text(encoding="utf-8").splitlines():
            if line.startswith("MemTotal:"):
                return int(line.split()[1]) * 1024
    return None


def package_version(distribution: str) -> str:
    return importlib.metadata.version(distribution)


def validate_source_binding(repository: Path, config: dict[str, Any]) -> dict[str, Any]:
    binding = config["sourceBinding"]
    observed: dict[str, Any] = {}
    for key in ("main", "primaryAudit", "literatureAudit"):
        expected = binding[key]
        path = repository / expected["path"]
        if not path.is_file():
            raise RuntimeError(f"bound input is missing: {expected['path']}")
        digest = sha256_file(path)
        size = path.stat().st_size
        if digest != expected["sha256"] or size != int(expected["byteCount"]):
            raise RuntimeError(
                f"bound input mismatch for {expected['path']}: "
                f"sha256={digest}, bytes={size}"
            )
        observed[key] = {
            "path": expected["path"],
            "sha256": digest,
            "byteCount": size,
        }
    return observed


def build_source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(
        panel: str,
        series: str,
        x: str,
        y: str,
        x_unit: str,
        y_unit: str,
        exact_value: str,
        role: str,
        source_locator: str,
        note: str,
    ) -> None:
        rows.append(
            {
                "panel": panel,
                "series": series,
                "x": x,
                "y": y,
                "x_unit": x_unit,
                "y_unit": y_unit,
                "exact_value": exact_value,
                "role": role,
                "source_locator": source_locator,
                "note": note,
            }
        )

    for series, x, y, exact, locator, note in (
        ("outer packet clock", "0", "1", "Gamma=gamma_{k_2}", "Z.4", "reference packet weight"),
        ("remote clock", "1", "1/4", "omega=gamma_{k_2-1}=Gamma^(1/4)", "Z.11", "first fourth-root shift"),
        ("doubled-radius payment", "2", "1/16", "gamma_{k_2-2}=Gamma^(1/16)", "Z.12", "second fourth-root shift"),
        ("physical-shell identity", "1", "", "A_{k_2-1}(R)=A_{k_2-2}(2R)", "Z.12", "same remote physical annulus"),
        ("clock-to-remote shift", "0.5", "", "gamma_{j-1}=gamma_j^(1/4)", "Z.11", "exact dyadic weight rule"),
        ("remote-to-payment shift", "1.5", "", "omega^(1/4)=Gamma^(1/16)", "Z.12", "exact doubled-radius rule"),
        ("remote strip volume", "1", "", "|S_rem(t)|=(1/16)*sqrt(pL)*R^3", "Z.12b", "analytic geometry, not sampled data"),
    ):
        add("A", series, x, y, "ladder step", "exponent of Gamma", exact, "weight identity", locator, note)

    for index in range(81):
        kappa = Fraction(index, 100000)
        rate = DELTA_REMOTE - Fraction(2, 3) * kappa
        add(
            "B",
            "Holder lower-rate curve",
            f"{1000 * float(kappa):.12g}",
            f"{1000 * float(rate):.12g}",
            "kappa times 10^-3",
            "L^-2 log(P^(2/3)/h) lower rate times 10^-3",
            str(rate),
            "derived analytic curve",
            "Z.18--Z.19a",
            "affine leading-rate lower bound",
        )
    for series, x, y, exact, locator, note in (
        ("delta remote", "0", f"{1000 * float(DELTA_REMOTE):.12g}", str(DELTA_REMOTE), "Z.1", "rate at kappa=0"),
        ("kappa star", f"{1000 * float(KAPPA_STAR):.12g}", "0", str(KAPPA_STAR), "Z.19", "unique zero of affine rate"),
        ("strict theorem region", f"{1000 * float(KAPPA_STAR):.12g}", "", "limsup kappa_L < kappa_*", "Z.19a", "exponential W-kinetic no-go"),
        ("critical layer", f"{1000 * float(KAPPA_STAR):.12g}", "", "kappa_L=kappa_*+o(1)", "Z.19a", "OPEN; lower-order factors decide"),
    ):
        add("B", series, x, y, "kappa times 10^-3", "rate times 10^-3", exact, "threshold/reference", locator, note)

    for series, x, exact, locator, role, note in (
        ("time-tame reserve", f"{1000 * float(TIME_TAME_RESERVE):.12g}", str(TIME_TAME_RESERVE), "Z.21", "complexity component", "rho/4-beta"),
        ("critical residence cost", f"{1000 * float(KAPPA_STAR):.12g}", str(KAPPA_STAR), "Z.19", "complexity component", "kappa_*"),
        ("necessary complexity rate", f"{1000 * float(COMPLEXITY_ESCAPE):.12g}", str(COMPLEXITY_ESCAPE), "Z.36", "complexity total", "necessary, not sufficient; equality open"),
        ("endpoint preservation", "0", "C(t_2)=o(A_rem) on enlarged strip", "Z.23", "conditional proof node", "uniform endpoint hypothesis"),
        ("moving-frame envelope", "1", "R^2|D_2 C|<=|a_2|e^{o(L^2)}", "Z.22", "conditional proof node", "time-tame hypothesis"),
        ("moving-strip all-winding", "2", "uniform moving-strip all-winding comparison", "Z.24--Z.25", "conditional proof node", "required; not proved generically"),
        ("R^3 persistence", "3", "theta_L asymp 1", "Z.25", "conditional conclusion", "follows only from all three hypotheses"),
        ("complexity scope", "4", "log N_L/L^2 >= 476239/1064835072+o(1)", "Z.36", "scope boundary", "necessary within derivative/conditioning model"),
    ):
        add("C", series, x, "", "proof step or rate times 10^-3", "", exact, role, locator, note)

    for index, (series, exact, locator, note) in enumerate((
        ("PROVED", "same-b admissibility; Gamma ladder; shell-tube Holder coercivity", "Z.6--Z.16", "exact deterministic statements"),
        ("CONDITIONAL", "endpoint + Z.22 + moving-strip all-winding => R^3 persistence", "Z.22--Z.25", "not an unconditional theorem"),
        ("OPEN", "critical layer; accumulated rows; full-clock Y.57; arbitrary ill-conditioned finite family", "Z.19a; Z.39", "kinetic floor h is not an upper bound for K"),
        ("NEXT Z.39", "spectral/observability persistence-payment dichotomy", "Z.39", "must control critical time focusing and complete payment/clock ledger"),
    )):
        add("D", series, str(index), "", "claim order", "", exact, "claim hierarchy", locator, note)
    return rows

CSV_FIELDS = (
    "panel",
    "series",
    "x",
    "y",
    "x_unit",
    "y_unit",
    "exact_value",
    "role",
    "source_locator",
    "note",
)


def rows_to_csv(rows: list[dict[str, str]]) -> str:
    import io

    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=CSV_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def panel_title(ax: Any, label: str, title: str) -> None:
    ax.set_title(
        f"{label}  {title}",
        loc="left",
        fontsize=8.15,
        fontweight="bold",
        color=PALETTE["ink"],
        pad=5,
    )


def scope_badge(ax: Any, text: str) -> None:
    ax.text(
        0.985,
        0.975,
        text,
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=4.05,
        color=PALETTE["root_dark"],
        fontweight="bold",
        bbox={
            "boxstyle": "round,pad=0.20",
            "facecolor": PALETTE["root_open"],
            "edgecolor": PALETTE["root_light"],
            "linewidth": 0.55,
        },
        zorder=20,
    )


def draw_blossom(fig: Any) -> None:
    center = (0.958, 0.936)
    radius = 0.0105
    for index, angle in enumerate((90, 18, -54, -126, 162)):
        radians = math.radians(angle)
        color = PALETTE["root_dark"] if index % 2 == 0 else PALETTE["root_light"]
        fig.add_artist(
            patches.Ellipse(
                (center[0] + 0.014 * math.cos(radians), center[1] + 0.020 * math.sin(radians)),
                width=radius,
                height=radius * 1.55,
                angle=angle - 90,
                transform=fig.transFigure,
                facecolor="none",
                edgecolor=color,
                linewidth=0.9,
                zorder=30,
            )
        )
    fig.add_artist(
        patches.Circle(
            center,
            radius=0.0035,
            transform=fig.transFigure,
            facecolor=PALETTE["ink"],
            edgecolor="none",
            zorder=31,
        )
    )


def draw_arrow(ax: Any, start: tuple[float, float], end: tuple[float, float], **kwargs: Any) -> None:
    properties = {
        "arrowstyle": "-|>",
        "color": PALETTE["mid"],
        "linewidth": 0.75,
        "mutation_scale": 7,
        "shrinkA": 3,
        "shrinkB": 3,
    }
    properties.update(kwargs)
    ax.annotate("", xy=end, xytext=start, xycoords=ax.transAxes, arrowprops=properties)


def proof_box(
    ax: Any,
    x: float,
    y: float,
    width: float,
    height: float,
    text: str,
    *,
    filled: bool = False,
    dashed: bool = False,
    fontsize: float = 4.7,
) -> None:
    ax.add_patch(
        patches.FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.010,rounding_size=0.014",
            transform=ax.transAxes,
            facecolor=PALETTE["root_open"] if filled else PALETTE["paper"],
            edgecolor=PALETTE["root"] if filled else PALETTE["mid"],
            linewidth=0.8,
            linestyle="--" if dashed else "-",
            zorder=2,
        )
    )
    ax.text(
        x + width / 2,
        y + height / 2,
        text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=PALETTE["root_dark"] if filled else PALETTE["ink"],
        linespacing=1.16,
        zorder=3,
    )


def render_figure(config: dict[str, Any], rows: list[dict[str, str]]) -> Any:
    width_in = float(config["figure"]["widthMm"]) / 25.4
    height_in = float(config["figure"]["heightMm"]) / 25.4
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 6.3,
            "axes.labelcolor": PALETTE["ink"],
            "axes.titlecolor": PALETTE["ink"],
            "figure.facecolor": PALETTE["paper"],
            "savefig.facecolor": PALETTE["paper"],
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": ARTIFACT_ID,
            "axes.unicode_minus": False,
            "hatch.color": PALETTE["mid"],
            "hatch.linewidth": 0.45,
        }
    )
    fig, axes = plt.subplots(
        2,
        2,
        figsize=(width_in, height_in),
        dpi=int(config["figure"]["publicationDpi"]),
    )
    fig.subplots_adjust(left=0.067, right=0.975, bottom=0.105, top=0.815, wspace=0.29, hspace=0.47)
    ax_a, ax_b, ax_c, ax_d = axes.ravel()

    fig.text(
        0.040,
        0.955,
        "Remote persistence gate: kinetic coercivity versus the full clock",
        ha="left",
        va="top",
        fontsize=11.0,
        color=PALETTE["ink"],
        fontweight="bold",
    )
    fig.text(
        0.040,
        0.913,
        "R0.74Z | exact weight ladder | strict W-kinetic threshold | critical and full-clock branches open",
        ha="left",
        va="top",
        fontsize=6.0,
        color=PALETTE["mid"],
    )
    draw_blossom(fig)

    # Panel A: exact two-step fourth-root ladder.
    panel_title(ax_a, "A", "Exact remote-shell weight ladder")
    ax_a.set_xlim(0, 1)
    ax_a.set_ylim(0, 1)
    ax_a.axis("off")
    scope_badge(ax_a, "EXACT DYADIC WEIGHTS")
    ladder = (
        (0.03, "PACKET CLOCK", r"$\Gamma=\gamma_{k_2}$", r"$\Gamma^{1}$", False),
        (0.355, "REMOTE CLOCK", r"$\omega=\gamma_{k_2-1}$", r"$\Gamma^{1/4}$", True),
        (0.68, "PAYMENT @ $2R$", r"$\gamma_{k_2-2}$", r"$\Gamma^{1/16}$", False),
    )
    for x, title, symbol, exponent, filled in ladder:
        ax_a.add_patch(
            patches.FancyBboxPatch(
                (x, 0.43), 0.285, 0.30,
                boxstyle="round,pad=0.012,rounding_size=0.018",
                transform=ax_a.transAxes,
                facecolor=PALETTE["root_open"] if filled else PALETTE["paper"],
                edgecolor=PALETTE["root"] if filled else PALETTE["mid"],
                linewidth=0.9,
            )
        )
        ax_a.text(x + 0.1425, 0.675, title, transform=ax_a.transAxes,
                  ha="center", va="center", fontsize=4.45, color=PALETTE["mid"],
                  fontweight="bold")
        ax_a.text(x + 0.1425, 0.585, symbol, transform=ax_a.transAxes,
                  ha="center", va="center", fontsize=5.1, color=PALETTE["ink"])
        ax_a.text(x + 0.1425, 0.485, exponent, transform=ax_a.transAxes,
                  ha="center", va="center", fontsize=7.2, color=PALETTE["root_dark"],
                  fontweight="bold")
    draw_arrow(ax_a, (0.315, 0.58), (0.355, 0.58), color=PALETTE["root"])
    draw_arrow(ax_a, (0.64, 0.58), (0.68, 0.58), color=PALETTE["root"])
    ax_a.text(0.335, 0.77, "fourth root", transform=ax_a.transAxes,
              ha="center", va="center", fontsize=4.15, color=PALETTE["root_dark"])
    ax_a.text(0.66, 0.77, "fourth root", transform=ax_a.transAxes,
              ha="center", va="center", fontsize=4.15, color=PALETTE["root_dark"])
    ax_a.add_patch(
        patches.FancyBboxPatch(
            (0.10, 0.15), 0.80, 0.15,
            boxstyle="round,pad=0.012,rounding_size=0.016",
            transform=ax_a.transAxes, facecolor=PALETTE["pale"],
            edgecolor=PALETTE["mid"], linewidth=0.7,
        )
    )
    ax_a.text(
        0.50, 0.225,
        r"same physical annulus:  $A_{k_2-1}(R)=A_{k_2-2}(2R)$",
        transform=ax_a.transAxes, ha="center", va="center",
        fontsize=5.0, color=PALETTE["ink"], fontweight="bold",
    )
    ax_a.text(
        0.50, 0.045,
        r"CLOCK WEIGHT $\omega=\Gamma^{1/4}$   |   PAYMENT WEIGHT $\omega^{1/4}=\Gamma^{1/16}$",
        transform=ax_a.transAxes, ha="center", va="bottom",
        fontsize=4.45, color=PALETTE["root_dark"],
    )

    # Panel B: exact affine rate and strict/open boundary.
    panel_title(ax_b, "B", "Strict W-kinetic persistence threshold")
    b_curve = [row for row in rows if row["panel"] == "B" and row["series"] == "Holder lower-rate curve"]
    bx = np.array([float(row["x"]) for row in b_curve])
    by = np.array([float(row["y"]) for row in b_curve])
    kappa_scaled = 1000.0 * float(KAPPA_STAR)
    ax_b.axvspan(0, kappa_scaled, facecolor=PALETTE["root_open"], edgecolor="none", zorder=0)
    ax_b.axvspan(kappa_scaled, 0.80, facecolor=PALETTE["pale"], edgecolor=PALETTE["light"],
                 hatch="////", linewidth=0.0, zorder=0)
    ax_b.plot(bx, by, color=PALETTE["root_dark"], linewidth=1.4, zorder=4)
    ax_b.axhline(0, color=PALETTE["mid"], linewidth=0.75, zorder=2)
    ax_b.axvline(kappa_scaled, color=PALETTE["mid"], linewidth=0.85,
                 linestyle="--", zorder=3)
    ax_b.plot([kappa_scaled], [0], marker="o", markersize=5.5,
              markerfacecolor=PALETTE["paper"], markeredgecolor=PALETTE["root_dark"],
              markeredgewidth=1.0, linestyle="None", zorder=5)
    ax_b.set_xlim(0, 0.80)
    ax_b.set_ylim(-0.30, 0.33)
    ax_b.set_xticks([0, 0.2, 0.4, 0.6, 0.8])
    ax_b.set_yticks([-0.2, 0, 0.2])
    ax_b.set_xlabel(r"residence exponent $\kappa$  ($\times10^{-3}$)", fontsize=5.0, labelpad=2)
    ax_b.set_ylabel(r"lower rate  ($\times10^{-3}$)", fontsize=5.0, labelpad=2)
    ax_b.tick_params(axis="both", labelsize=4.6, length=2.5, width=0.6)
    ax_b.grid(color=PALETTE["light"], linewidth=0.4, linestyle=(0, (2, 2)), zorder=1)
    for spine in ("top", "right"):
        ax_b.spines[spine].set_visible(False)
    ax_b.spines["left"].set_color(PALETTE["mid"])
    ax_b.spines["bottom"].set_color(PALETTE["mid"])
    scope_badge(ax_b, "STRICT SIDE ONLY")
    ax_b.text(
        0.025, 0.965,
        r"$\Delta_{\rm rem}-\frac{2}{3}\kappa=\frac{2}{3}(\kappa_*-\kappa)$",
        transform=ax_b.transAxes, ha="left", va="top",
        fontsize=5.15, color=PALETTE["root_dark"], fontweight="bold",
        bbox={"boxstyle": "square,pad=0.10", "facecolor": PALETTE["paper"],
              "edgecolor": "none", "alpha": 0.92},
        zorder=7,
    )
    ax_b.text(
        0.14, 0.105,
        "PROVED\nexponential payment / h",
        ha="center", va="center", fontsize=4.45,
        color=PALETTE["root_dark"], fontweight="bold",
    )
    ax_b.annotate(
        r"$\kappa_*=\frac{64279}{158760000}$" + "\n" + r"$\kappa_*+o(1)$: OPEN",
        xy=(kappa_scaled, 0), xycoords="data",
        xytext=(0.49, -0.19), textcoords="data",
        fontsize=4.45, color=PALETTE["ink"], ha="left", va="center",
        arrowprops={"arrowstyle": "->", "color": PALETTE["mid"], "linewidth": 0.7},
        bbox={"boxstyle": "round,pad=0.20", "facecolor": PALETTE["paper"],
              "edgecolor": PALETTE["mid"], "linewidth": 0.55},
        zorder=6,
    )
    ax_b.text(
        0.62, 0.20,
        "NOT CLASSIFIED\nby this coercivity",
        ha="center", va="center", fontsize=4.2,
        color=PALETTE["mid"], fontweight="bold",
    )

    # Panel C: conditional time-tame route and necessary complexity.
    panel_title(ax_c, "C", "Conditional persistence and necessary complexity")
    ax_c.set_xlim(0, 1)
    ax_c.set_ylim(0, 1)
    ax_c.axis("off")
    scope_badge(ax_c, "CONDITIONAL / NECESSARY ONLY")
    nodes = (
        (0.025, "endpoint\npreservation\n(Z.23)"),
        (0.365, "moving-frame\nenvelope\n(Z.22)"),
        (0.705, "moving-strip\nall-winding\nuniformity"),
    )
    for index, (x, text_value) in enumerate(nodes):
        proof_box(ax_c, x, 0.70, 0.27, 0.18, text_value,
                  filled=index == 1, dashed=index == 2, fontsize=4.45)
    draw_arrow(ax_c, (0.295, 0.79), (0.365, 0.79), color=PALETTE["root"])
    draw_arrow(ax_c, (0.635, 0.79), (0.705, 0.79), color=PALETTE["mid"], linestyle="--")
    proof_box(
        ax_c, 0.20, 0.45, 0.60, 0.14,
        r"all three hypotheses  $\Longrightarrow$  $R^3$ persistence",
        filled=True, fontsize=4.8,
    )
    for x in (0.16, 0.50, 0.84):
        draw_arrow(ax_c, (x, 0.70), (0.50, 0.59),
                   color=PALETTE["mid"], linestyle="--" if x == 0.84 else "-")
    total = float(COMPLEXITY_ESCAPE)
    reserve_share = float(TIME_TAME_RESERVE) / total
    bar_x, bar_y, bar_w, bar_h = 0.08, 0.205, 0.84, 0.105
    ax_c.add_patch(
        patches.Rectangle(
            (bar_x, bar_y), bar_w * reserve_share, bar_h,
            transform=ax_c.transAxes, facecolor=PALETTE["root_dark"],
            edgecolor=PALETTE["root_dark"], linewidth=0.7,
        )
    )
    ax_c.add_patch(
        patches.Rectangle(
            (bar_x + bar_w * reserve_share, bar_y),
            bar_w * (1 - reserve_share), bar_h,
            transform=ax_c.transAxes, facecolor=PALETTE["paper"],
            edgecolor=PALETTE["mid"], linewidth=0.8, hatch="////",
        )
    )
    ax_c.text(
        0.50, 0.36,
        r"necessary:  $\liminf_{L\to\infty} L^{-2}\log\mathcal{N}_L\geq"
        r"\frac{476239}{1064835072}$",
        transform=ax_c.transAxes, ha="center", va="center",
        fontsize=4.85, color=PALETTE["root_dark"], fontweight="bold",
    )
    ax_c.text(
        0.08, 0.145,
        r"reserve $\frac{7103}{167680000}$",
        transform=ax_c.transAxes, ha="left", va="center",
        fontsize=4.25, color=PALETTE["ink"],
    )
    ax_c.text(
        0.92, 0.145,
        r"$+\ \kappa_*=\frac{64279}{158760000}$",
        transform=ax_c.transAxes, ha="right", va="center",
        fontsize=4.25, color=PALETTE["ink"],
    )
    ax_c.text(
        0.50, 0.045,
        "NECESSARY, NOT SUFFICIENT  |  EQUALITY OPEN",
        transform=ax_c.transAxes, ha="center", va="bottom",
        fontsize=4.45, color=PALETTE["ink"], fontweight="bold",
        bbox={"boxstyle": "round,pad=0.20", "facecolor": PALETTE["pale"],
              "edgecolor": PALETTE["mid"], "linewidth": 0.55},
    )

    # Panel D: proof status and fail-closed boundary.
    panel_title(ax_d, "D", "W-kinetic result versus the full clock")
    ax_d.set_xlim(0, 1)
    ax_d.set_ylim(0, 1)
    ax_d.axis("off")
    scope_badge(ax_d, "FAIL-CLOSED CLAIM HIERARCHY")
    cards = (
        (0.72, "PROVED",
         "same-b exact family | weight ladder\nshell-tube Holder coercivity (Z.15--Z.16)",
         True, False),
        (0.51, "CONDITIONAL",
         "endpoint + Z.22 + moving-strip all-winding\nimplies R^3 persistence",
         False, True),
        (0.30, "OPEN",
         r"critical $\kappa_*+o(1)$ | accumulated clock rows"
         + "\n" + r"full-clock Y.57 | arbitrary exponential finite family",
         False, False),
        (0.065, "NEXT Z.39",
         "spectral / observability persistence-payment dichotomy\nmust control the complete clock and payment ledger",
         True, True),
    )
    for y, status, detail, filled, dashed in cards:
        ax_d.add_patch(
            patches.FancyBboxPatch(
                (0.035, y), 0.205, 0.145,
                boxstyle="round,pad=0.010,rounding_size=0.014",
                transform=ax_d.transAxes,
                facecolor=PALETTE["root_dark"] if status == "PROVED" else
                          (PALETTE["root_open"] if filled else PALETTE["paper"]),
                edgecolor=PALETTE["root"] if filled else PALETTE["mid"],
                linewidth=0.85, linestyle="--" if dashed else "-",
            )
        )
        ax_d.text(
            0.1375, y + 0.0725, status, transform=ax_d.transAxes,
            ha="center", va="center", fontsize=4.45,
            color=PALETTE["paper"] if status == "PROVED" else PALETTE["root_dark"],
            fontweight="bold",
        )
        ax_d.add_patch(
            patches.FancyBboxPatch(
                (0.265, y), 0.70, 0.145,
                boxstyle="round,pad=0.010,rounding_size=0.014",
                transform=ax_d.transAxes,
                facecolor=PALETTE["root_open"] if filled else PALETTE["pale"],
                edgecolor=PALETTE["root"] if filled else PALETTE["mid"],
                linewidth=0.75, linestyle="--" if dashed else "-",
            )
        )
        ax_d.text(
            0.615, y + 0.0725, detail, transform=ax_d.transAxes,
            ha="center", va="center", fontsize=4.15,
            color=PALETTE["ink"], linespacing=1.16,
        )
    ax_d.text(
        0.50, 0.005,
        r"kinetic floor $h$ is not an upper bound for completed clock $K$",
        transform=ax_d.transAxes, ha="center", va="bottom",
        fontsize=4.15, color=PALETTE["mid"],
    )

    fig.text(
        0.50,
        0.035,
        REQUIRED_LABEL,
        ha="center",
        va="center",
        fontsize=5.35,
        color=PALETTE["root_dark"],
        fontweight="bold",
        family="DejaVu Sans Mono",
    )
    fig.text(
        0.50,
        0.014,
        "Live-file SHA-256 precommit binding | independent audit: PASS, blockers 0 | literature screen: bounded non-hit only",
        ha="center",
        va="center",
        fontsize=4.3,
        color=PALETTE["mid"],
    )
    return fig

def write_exports(fig: Any, out_dir: Path, config: dict[str, Any]) -> dict[str, Any]:
    png_dpi = int(config["figure"]["publicationDpi"])
    qa_dpi = int(config["figure"]["qaDpi"])
    common_metadata = {
        "Title": "R0.74Z remote persistence gate",
        "Author": "C. K. Zeng",
        "Subject": REQUIRED_LABEL,
        "Keywords": "Navier-Stokes, analytic schematic, remote persistence, cubic payment, NOT CLAY",
        "Creator": f"Matplotlib {matplotlib.__version__}; {ARTIFACT_ID}",
    }
    fig.savefig(
        out_dir / "figure.png",
        dpi=png_dpi,
        facecolor=PALETTE["paper"],
        edgecolor="none",
        metadata={
            "Title": common_metadata["Title"],
            "Author": common_metadata["Author"],
            "Description": REQUIRED_LABEL,
            "Software": common_metadata["Creator"],
        },
    )
    fig.savefig(
        out_dir / "figure.svg",
        format="svg",
        facecolor=PALETTE["paper"],
        edgecolor="none",
        metadata={
            "Date": "2026-09-03",
            "Title": common_metadata["Title"],
            "Creator": common_metadata["Creator"],
            "Description": REQUIRED_LABEL,
        },
    )
    fig.savefig(
        out_dir / "figure.pdf",
        format="pdf",
        facecolor=PALETTE["paper"],
        edgecolor="none",
        metadata={**common_metadata, "CreationDate": FIXED_DATE, "ModDate": FIXED_DATE},
    )
    plt.close(fig)

    with Image.open(out_dir / "figure.png") as publication:
        publication.load()
        expected_qa = (
            int(float(config["figure"]["widthMm"]) / 25.4 * qa_dpi),
            int(float(config["figure"]["heightMm"]) / 25.4 * qa_dpi),
        )
        final_size = publication.resize(expected_qa, Image.Resampling.LANCZOS)
        final_size.save(
            out_dir / "qa-final-size.png",
            dpi=(qa_dpi, qa_dpi),
            optimize=False,
            compress_level=6,
        )
        final_size.convert("L").convert("RGB").save(
            out_dir / "qa-grayscale.png",
            dpi=(qa_dpi, qa_dpi),
            optimize=False,
            compress_level=6,
        )

    document = pdfium.PdfDocument(str(out_dir / "figure.pdf"))
    if len(document) != 1:
        raise RuntimeError("figure.pdf must contain exactly one page")
    page = document[0]
    bitmap = page.render(scale=qa_dpi / 72.0, rotation=0)
    pdf_image = bitmap.to_pil().convert("RGB")
    if pdf_image.size != expected_qa:
        pdf_image = pdf_image.resize(expected_qa, Image.Resampling.LANCZOS)
    pdf_image.save(
        out_dir / "qa-pdf.png",
        dpi=(qa_dpi, qa_dpi),
        optimize=False,
        compress_level=6,
    )
    page.close()
    document.close()

    with Image.open(out_dir / "figure.png") as image:
        png_size = list(image.size)
        png_dpi_observed = [round(float(value), 3) for value in image.info.get("dpi", (0, 0))]
    with Image.open(out_dir / "qa-final-size.png") as image:
        qa_size = list(image.size)
    return {
        "publicationPngPixels": png_size,
        "publicationPngDpi": png_dpi_observed,
        "qaPixels": qa_size,
        "pdfPageCount": 1,
    }


def write_environment(out_dir: Path, repository: Path, dependency_root_supplied: bool) -> None:
    environment = {
        "artifactId": ARTIFACT_ID,
        "schema": "r074z-figure-environment-v1",
        "createdAtUtc": utc_now(),
        "python": platform.python_version(),
        "pythonLocatorPolicy": "bundled Python executable; absolute path omitted",
        "dependencyLocatorPolicy": (
            "external version-pinned directory supplied; absolute path omitted"
            if dependency_root_supplied
            else "bundled workspace dependency environment; absolute path omitted"
        ),
        "matplotlibConfigPolicy": "system temporary directory removed after render",
        "operatingSystem": platform.platform(),
        "machine": platform.machine(),
        "logicalCpuCount": os.cpu_count(),
        "memoryBytes": total_memory_bytes(),
        "repositoryHead": repository_head(repository),
        "packages": {
            "python": platform.python_version(),
            "numpy": package_version("numpy"),
            "matplotlib": package_version("matplotlib"),
            "pillow": package_version("pillow"),
            "pypdf": package_version("pypdf"),
            "pypdfium2": package_version("pypdfium2"),
        },
    }
    atomic_json(out_dir / "environment.json", environment)


def build_results(config: dict[str, Any], binding: dict[str, Any], rows: list[dict[str, str]], export: dict[str, Any]) -> dict[str, Any]:
    counts = {panel: sum(row["panel"] == panel for row in rows) for panel in "ABCD"}
    return {
        "artifactId": ARTIFACT_ID,
        "schema": "r074z-figure-results-v1",
        "sourceBinding": binding,
        "bindingMode": config["sourceBinding"]["mode"],
        "mainIndependentAuditSealed": True,
        "mainIndependentAuditVerdict": "PASS",
        "mainIndependentAuditBlockerCount": 0,
        "exactConstants": {
            "cGamma": str(C_GAMMA),
            "rho": str(RHO),
            "d": str(D),
            "a0": str(A0),
            "clockWeightExponent": str(CLOCK_WEIGHT_EXPONENT),
            "paymentWeightExponent": str(PAYMENT_WEIGHT_EXPONENT),
            "beta": str(BETA),
            "timeTameReserve": str(TIME_TAME_RESERVE),
            "deltaRemote": str(DELTA_REMOTE),
            "kappaStar": str(KAPPA_STAR),
            "twoCenterRate": str(TWO_CENTER_RATE),
            "twoCenterMargin": str(TWO_CENTER_MARGIN),
            "complexityEscapeCoefficient": str(COMPLEXITY_ESCAPE),
        },
        "derivedComparisons": {
            "holderLeadingRate": "deltaRemote-(2/3)kappa=(2/3)(kappaStar-kappa)",
            "strictSubcriticalRegion": "limsup kappa_L < kappaStar",
            "criticalLayer": "kappa_L=kappaStar+o(1): OPEN",
            "complexityDecomposition": "timeTameReserve+kappaStar",
            "complexityCondition": "necessary within derivative/conditioning model; not sufficient; equality open",
        },
        "panelRowCounts": counts,
        "sourceDataRows": len(rows),
        "exports": export,
        "requiredVisibleLabel": REQUIRED_LABEL,
        "claimBoundary": {
            "analyticSchematic": True,
            "derivedAnalyticValues": True,
            "pdeData": False,
            "dnsData": False,
            "clayClaim": False,
            "exactCommonShearAdmissibility": True,
            "remoteClockWeightGammaQuarter": True,
            "doubledRadiusPaymentWeightGammaSixteenth": True,
            "shellTubeHolderCoercivity": True,
            "strictSubcriticalKappaNoGoForWKinetic": True,
            "timeTamePersistenceConditional": True,
            "movingStripAllWindingUniformityProved": False,
            "endpointToTubeUnconditional": False,
            "criticalLayerResolved": False,
            "fullClockY57Blocked": False,
            "accumulatedClockRowsControlled": False,
            "arbitraryFiniteEndpointFocusedBlocked": False,
            "noveltyClaim": False,
            "mainIndependentAuditSealed": True,
            "mainIndependentAuditVerdict": "PASS",
            "mainIndependentAuditBlockerCount": 0,
        },
    }


def render_package(
    out_dir: Path = HERE,
    *,
    repository: Path = DEFAULT_REPOSITORY,
    dependency_root_supplied: bool = False,
    write_logs: bool = True,
) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    if write_logs:
        atomic_text(out_dir / "progress.ndjson", "")
        atomic_text(out_dir / "resource-log.ndjson", "")
        log_progress(out_dir, "start", 1, started)

    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    binding = validate_source_binding(repository, config)
    if write_logs:
        log_progress(out_dir, "source-binding-verified", 2, started)

    rows = build_source_rows()
    atomic_text(out_dir / "source-data.csv", rows_to_csv(rows))
    if write_logs:
        log_progress(out_dir, "source-data-written", 3, started)

    figure = render_figure(config, rows)
    if write_logs:
        log_progress(out_dir, "figure-composed", 4, started)
    export = write_exports(figure, out_dir, config)
    if write_logs:
        log_progress(out_dir, "vector-raster-pdf-exported", 5, started)

    results = build_results(config, binding, rows, export)
    atomic_json(out_dir / "results.json", results)
    write_environment(out_dir, repository, dependency_root_supplied)
    if write_logs:
        log_progress(out_dir, "complete", 6, started)
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render", action="store_true", help="render the complete raw figure archive")
    parser.add_argument("--repository", type=Path, default=DEFAULT_REPOSITORY, help="repository root")
    parser.add_argument("--deps", type=Path, default=None, help="version-pinned dependency root (provenance only)")
    parser.add_argument("--output", type=Path, default=HERE, help="output directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.render:
        raise SystemExit("pass --render")
    render_package(
        args.output.resolve(),
        repository=args.repository.resolve(),
        dependency_root_supplied=args.deps is not None,
        write_logs=True,
    )
    print(json.dumps({"artifactId": ARTIFACT_ID, "status": "rendered", "output": str(args.output.resolve())}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
