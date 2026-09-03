#!/usr/bin/env python3
"""Deterministic renderer for the R0.74X analytic four-panel figure."""

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


_MPL_CONFIG = Path(tempfile.mkdtemp(prefix="r074x-mpl-"))
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
ARTIFACT_ID = "fig-r074x-three-packet-payment-gate"
REQUIRED_LABEL = (
    "ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | "
    "NOT PDE DATA | NOT DNS | NOT CLAY"
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

P = Fraction(32, 63)
D = Fraction(433, 1008)
Q = Fraction(4, 3969)
Q65 = Fraction(256, 257985)
CHI65 = Fraction(12191, 132088320)
CHI66 = Fraction(15263, 134120448)
PAYMENT_RATE = Fraction(3306805, 134120448)
MAXIMUM_STRIP_RATE = 16 * CHI66
RATE_GAP = Fraction(3062597, 134120448)


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

    panel_a = (
        ("packet 1", "1", "0.72", "k_1; L_1", "X.1", "context packet"),
        ("packet 2", "2", "0.72", "k_2=k_1+1; L_2=2L_1", "X.1", "remote-strip survivor"),
        ("packet 3", "3", "0.72", "k_3=k_1+2; L_3=4L_1", "X.1", "remote-strip survivor"),
        ("clock coordinate from packet 2", "1", "0.25", "k_2-1=k_1", "X.40--X.44", "strip lower witness only"),
        ("clock coordinate from packet 3", "2", "0.25", "k_3-1=k_2", "X.40--X.44", "strip lower witness only"),
        ("equal target clock packet 1", "1", "", "Gamma_1*a_1^2*L_1*R^2=T_*", "X.17", "normalization"),
        ("equal target clock packet 2", "2", "", "Gamma_2*a_2^2*L_2*R^2=T_*", "X.17", "normalization"),
        ("equal target clock packet 3", "3", "", "Gamma_3*a_3^2*L_3*R^2=T_*", "X.17", "normalization"),
        ("packet 2 survival reserve", "2", "", "3719797/5811886080", "X.27", "strictly positive"),
        ("packet 3 survival reserve", "3", "", "72925813/5811886080", "X.28", "strictly positive"),
        ("cross 2 from 1", "", "", "3667/70447104", "X.32", "amplitude-weighted margin"),
        ("cross 2 from 3", "", "", "100043/29804544", "X.32--X.33", "amplitude-weighted margin"),
        ("cross 3 from 2", "", "", "3667/70447104", "X.32", "amplitude-weighted margin"),
        ("cross 3 from 1", "", "", "147359/281788416", "X.32", "amplitude-weighted margin"),
        ("inversion margin", "", "", "5/693", "X.34", "all intended inversion partners"),
        ("periodic margin", "", "", "123450676/1091475", "X.36", "all noncentral copies retained and bounded"),
    )
    for series, x, y, exact, locator, note in panel_a:
        add("A", series, x, y, "scale-index schematic", "diagram coordinate", exact, "packet/clock architecture", locator, note)

    panel_b = (
        ("fixed deletion order", "0", "", "inf_{#S<=1} sup_{t in D} sum_{k notin S} K_{k,R}(t)", "X.5", "S fixed before t"),
        ("branch k1 remains", "1", "", "k_1 notin S => choose t=tau_2", "X.43", "time chosen after fixed S"),
        ("branch k1 deleted", "2", "", "k_1 in S => k_2 notin S => choose t=tau_3", "X.43", "time chosen after fixed S"),
        ("pigeonhole lower bound", "3", "", "L^K_{1,R}(D)>=min{K_{k_1,R}(tau_2),K_{k_2,R}(tau_3)}", "X.43", "different times permitted"),
        ("optional equal schedule", "4", "", "tau_2=tau_3 is permitted but unnecessary", "X.42--X.43", "not a hypothesis of the pigeonhole"),
        ("terminal-domain consequence", "5", "", "L^K_{1,R}(T_R)/T_*->infinity", "X.44", "two-coordinate T_* obstruction"),
    )
    for series, x, y, exact, locator, note in panel_b:
        add("B", series, x, y, "proof-order", "", exact, "quantifier branch", locator, note)

    for series, value, locator, role, note in (
        ("payment lower rate", PAYMENT_RATE, "X.47--X.48", "rate bar", "lower exponential rate in L_1^2-units"),
        ("maximum audited strip rate", MAXIMUM_STRIP_RATE, "X.49", "rate bar", "16*chi(66); applies only to the two strip endpoint witnesses"),
        ("strict rate gap", RATE_GAP, "X.50", "derived gap", "payment minus maximum audited strip rate"),
    ):
        add("C", series, f"{float(value):.15g}", "", "L_1^2 exponent rate", "", str(value), role, locator, note)
    add(
        "C", "strip-to-payment conclusion", "", "", "", "", "(E_2^strip+E_3^strip)/(P_R^M)^(2/3)->0",
        "scope boundary", "X.51", "does not upper-bound either whole shell clock"
    )

    for index, (series, exact, locator, note) in enumerate((
        ("PROVED", "two-coordinate endpoint obstruction normalized by T_*", "X.40--X.44", "times may differ"),
        ("NOT PROVED", "counterexample to the actual (P_R^M)^(2/3)-normalized gate", "X.47--X.51", "whole-shell or dissipation enhancement remains possible"),
        ("NO-GO", "equal-target W-strip route is dominated by cubic payment", "X.50--X.51", "architecture-specific obstruction"),
        ("NEXT X.52", "min{K_r(t_r),K_s(t_s)}/(P_R^M)^(2/3)->infinity", "X.52", "distinct coordinates; witness times need not coincide"),
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
        "Three-packet fixed deletion: endpoint height versus cubic payment",
        ha="left",
        va="top",
        fontsize=11.1,
        color=PALETTE["ink"],
        fontweight="bold",
    )
    fig.text(
        0.040,
        0.913,
        "R0.74X | exact smooth frozen family | two-coordinate T* obstruction | payment gate remains open",
        ha="left",
        va="top",
        fontsize=6.05,
        color=PALETTE["mid"],
    )
    draw_blossom(fig)

    # Panel A: scale-index architecture and two adjacent-inward witnesses.
    panel_title(ax_a, "A", "Three packets and two adjacent-inward coordinates")
    ax_a.set_xlim(0, 1)
    ax_a.set_ylim(0, 1)
    ax_a.axis("off")
    scope_badge(ax_a, "ANALYTIC SCALE INDEX")
    ax_a.text(
        0.50,
        0.89,
        r"$\Gamma_m\mathfrak{a}_m^2L_mR^2=T_*$ for $m=1,2,3$",
        transform=ax_a.transAxes,
        ha="center",
        va="center",
        fontsize=5.45,
        color=PALETTE["root_dark"],
        fontweight="bold",
    )
    positions = {1: 0.18, 2: 0.50, 3: 0.82}
    ax_a.plot([0.10, 0.90], [0.57, 0.57], transform=ax_a.transAxes, color=PALETTE["mid"], linewidth=0.9)
    for index, label in ((1, r"$k_1$"), (2, r"$k_2=k_1+1$"), (3, r"$k_3=k_1+2$")):
        x = positions[index]
        ax_a.plot([x, x], [0.54, 0.60], transform=ax_a.transAxes, color=PALETTE["ink"], linewidth=0.75)
        ax_a.text(x, 0.49, label, transform=ax_a.transAxes, ha="center", va="top", fontsize=5.0, color=PALETTE["ink"])
    packet_styles = {
        1: ("o", PALETTE["paper"], PALETTE["mid"]),
        2: ("s", PALETTE["root_open"], PALETTE["root"]),
        3: ("D", PALETTE["root_dark"], PALETTE["root_dark"]),
    }
    for index, scale in ((1, r"$L_1$"), (2, r"$L_2=2L_1$"), (3, r"$L_3=4L_1$")):
        marker, face, edge = packet_styles[index]
        x = positions[index]
        ax_a.plot(
            [x], [0.73], transform=ax_a.transAxes, marker=marker, markersize=7.0,
            markerfacecolor=face, markeredgecolor=edge, markeredgewidth=1.0,
            color=edge, linestyle="None", zorder=5,
        )
        ax_a.text(x, 0.80, f"packet {index}", transform=ax_a.transAxes, ha="center", va="bottom",
                  fontsize=5.0, color=PALETTE["root_dark"] if index > 1 else PALETTE["mid"], fontweight="bold")
        ax_a.text(x, 0.66, scale, transform=ax_a.transAxes, ha="center", va="top", fontsize=4.8, color=PALETTE["mid"])
    for x, title, formula in (
        (0.18, "coordinate k1", r"$K_{k_1,R}(\tau_2)/T_*\to\infty$"),
        (0.50, "coordinate k2", r"$K_{k_2,R}(\tau_3)/T_*\to\infty$"),
    ):
        ax_a.add_patch(
            patches.FancyBboxPatch(
                (x - 0.145, 0.17), 0.29, 0.16,
                boxstyle="round,pad=0.012,rounding_size=0.015",
                transform=ax_a.transAxes, facecolor=PALETTE["root_open"],
                edgecolor=PALETTE["root"], linewidth=0.85,
            )
        )
        ax_a.text(x, 0.275, title, transform=ax_a.transAxes, ha="center", va="center",
                  fontsize=4.55, color=PALETTE["mid"])
        ax_a.text(x, 0.215, formula, transform=ax_a.transAxes, ha="center", va="center",
                  fontsize=4.75, color=PALETTE["root_dark"], fontweight="bold")
    draw_arrow(ax_a, (positions[2], 0.70), (0.23, 0.34), color=PALETTE["root"])
    draw_arrow(ax_a, (positions[3], 0.70), (0.55, 0.34), color=PALETTE["root_dark"])
    ax_a.text(
        0.82, 0.245,
        "packets 2 & 3 survive\ncross + inversion\n+ all windings controlled",
        transform=ax_a.transAxes, ha="center", va="center", fontsize=4.05, color=PALETTE["mid"],
    )
    ax_a.text(
        0.50, 0.035,
        "STRIP LOWER WITNESSES ONLY  |  NOT A WHOLE-SHELL UPPER BOUND",
        transform=ax_a.transAxes, ha="center", va="bottom", fontsize=4.4,
        color=PALETTE["ink"], fontweight="bold",
        bbox={"boxstyle": "round,pad=0.20", "facecolor": PALETTE["pale"],
              "edgecolor": PALETTE["mid"], "linewidth": 0.55},
    )

    # Panel B: the deletion set is fixed before the time supremum.
    panel_title(ax_b, "B", "Different-time fixed-deletion pigeonhole")
    ax_b.set_xlim(0, 1)
    ax_b.set_ylim(0, 1)
    ax_b.axis("off")
    scope_badge(ax_b, "TIMES MAY DIFFER")
    proof_box(
        ax_b, 0.08, 0.77, 0.84, 0.14,
        r"$\inf_{|S|\leq1}\ \sup_{t\in\mathcal{D}}\ \sum_{k\notin S}K_{k,R}(t)$"
        + "\n" + "fix S first; choose t afterwards",
        filled=True, fontsize=5.1,
    )
    proof_box(
        ax_b, 0.08, 0.48, 0.38, 0.17,
        r"$k_1\notin S$" + "\n" + r"choose $t=\tau_2$"
        + "\n" + r"use $K_{k_1,R}(\tau_2)$",
        fontsize=4.9,
    )
    proof_box(
        ax_b, 0.54, 0.48, 0.38, 0.17,
        r"$k_1\in S\Rightarrow k_2\notin S$"
        + "\n" + r"choose $t=\tau_3$"
        + "\n" + r"use $K_{k_2,R}(\tau_3)$",
        dashed=True, fontsize=4.65,
    )
    draw_arrow(ax_b, (0.36, 0.77), (0.27, 0.65), color=PALETTE["root"])
    draw_arrow(ax_b, (0.64, 0.77), (0.73, 0.65), color=PALETTE["mid"], linestyle="--")
    proof_box(
        ax_b, 0.10, 0.20, 0.80, 0.14,
        r"$\mathfrak{L}_{1,R}^{K}(\mathcal{D})\geq"
        r"\min\{K_{k_1,R}(\tau_2),K_{k_2,R}(\tau_3)\}$",
        filled=True, fontsize=5.2,
    )
    draw_arrow(ax_b, (0.27, 0.48), (0.40, 0.34), color=PALETTE["root"])
    draw_arrow(ax_b, (0.73, 0.48), (0.60, 0.34), color=PALETTE["mid"], linestyle="--")
    ax_b.text(
        0.50, 0.07,
        r"optional schedule: $\tau_2=\tau_3$ permitted; never required",
        transform=ax_b.transAxes, ha="center", va="center", fontsize=4.75,
        color=PALETTE["mid"],
    )

    # Panel C: exact exponential-rate comparison in L1^2 units.
    panel_title(ax_c, "C", "Payment rate dominates the two W-strip rates")
    c_rows = {row["series"]: Fraction(row["exact_value"]) for row in rows if row["panel"] == "C" and row["role"] in {"rate bar", "derived gap"}}
    payment = 1000.0 * float(c_rows["payment lower rate"])
    strip = 1000.0 * float(c_rows["maximum audited strip rate"])
    gap = 1000.0 * float(c_rows["strict rate gap"])
    ax_c.barh([1.0], [payment], height=0.34, color=PALETTE["root_dark"], edgecolor=PALETTE["root_dark"], linewidth=0.9, zorder=3)
    ax_c.barh([0.0], [strip], height=0.34, color=PALETTE["paper"], edgecolor=PALETTE["mid"], linewidth=1.0, hatch="////", zorder=3)
    ax_c.set_xlim(0, 27.0)
    ax_c.set_ylim(-0.62, 1.58)
    ax_c.set_yticks([])
    ax_c.set_xlabel(r"exponent coefficient in $L_1^2$  ($\times10^{-3}$)", fontsize=5.2, labelpad=2)
    ax_c.tick_params(axis="x", labelsize=4.8, length=2.5, width=0.6)
    ax_c.grid(axis="x", color=PALETTE["light"], linewidth=0.45, linestyle=(0, (2, 2)), zorder=0)
    for spine in ("top", "right", "left"):
        ax_c.spines[spine].set_visible(False)
    ax_c.spines["bottom"].set_color(PALETTE["mid"])
    ax_c.text(payment - 0.4, 1.0, r"$3306805/134120448$", ha="right", va="center",
              fontsize=4.8, color=PALETTE["paper"], fontweight="bold")
    ax_c.text(0.40, 1.0, "payment lower rate", ha="left", va="center",
              fontsize=4.65, color=PALETTE["paper"], fontweight="bold")
    ax_c.text(strip + 0.35, 0.0, r"$16\chi(66)=244208/134120448$", ha="left", va="center",
              fontsize=4.65, color=PALETTE["ink"])
    ax_c.text(0.10, -0.29, "maximum audited W-strip rate", ha="left", va="center",
              fontsize=4.45, color=PALETTE["mid"])
    ax_c.annotate(
        "", xy=(payment, 0.49), xytext=(strip, 0.49),
        arrowprops={"arrowstyle": "<->", "color": PALETTE["root"], "linewidth": 0.85},
    )
    ax_c.text(
        (payment + strip) / 2, 0.56,
        rf"strict gap $=3062597/134120448$  ($={gap:.3f}\times10^{{-3}}$)",
        ha="center", va="bottom", fontsize=4.65, color=PALETTE["root_dark"], fontweight="bold",
    )
    ax_c.text(
        0.985, 0.965,
        r"$(E_2^{\mathrm{strip}}+E_3^{\mathrm{strip}})/(P_R^M)^{2/3}\to0$"
        + "\n" + "UPPER COMPARISON: TWO STRIP INTEGRALS ONLY"
        + "\n" + "NO WHOLE-SHELL UPPER BOUND",
        transform=ax_c.transAxes, ha="right", va="top", fontsize=4.45,
        color=PALETTE["root_dark"], fontweight="bold",
        bbox={"boxstyle": "round,pad=0.22", "facecolor": PALETTE["root_open"],
              "edgecolor": PALETTE["root_light"], "linewidth": 0.6},
        zorder=5,
    )

    # Panel D: status hierarchy, not a quantitative ranking.
    panel_title(ax_d, "D", "Claim status and next payment gate")
    ax_d.set_xlim(0, 1)
    ax_d.set_ylim(0, 1)
    ax_d.axis("off")
    scope_badge(ax_d, "LOGICAL STATUS / NOT A RANKING")
    cards = (
        (0.72, "PROVED", r"$\mathfrak{L}_{1,R}^{K}(\mathcal{T}_R)/T_*\to\infty$"
         + "\n" + "two coordinates; witness times may differ", True, False),
        (0.51, "NOT PROVED", r"counterexample to the $(P_R^M)^{2/3}$-normalized gate"
         + "\n" + "whole-shell / dissipation enhancement remains open", False, False),
        (0.30, "NO-GO", "equal-target W-strip route"
         + "\n" + "outer cubic payment has the larger exponent", False, True),
        (0.065, "NEXT X.52", r"$\min\{K_r(t_r),K_s(t_s)\}/(P_R^M)^{2/3}\to\infty$"
         + "\n" + r"$r\ne s$; no requirement that $t_r=t_s$", True, True),
    )
    for y, status, detail, filled, dashed in cards:
        ax_d.add_patch(
            patches.FancyBboxPatch(
                (0.035, y), 0.205, 0.145,
                boxstyle="round,pad=0.010,rounding_size=0.014",
                transform=ax_d.transAxes,
                facecolor=PALETTE["root_dark"] if status == "PROVED" else (PALETTE["root_open"] if filled else PALETTE["paper"]),
                edgecolor=PALETTE["root"] if filled else PALETTE["mid"],
                linewidth=0.85, linestyle="--" if dashed else "-",
            )
        )
        ax_d.text(
            0.1375, y + 0.0725, status, transform=ax_d.transAxes,
            ha="center", va="center", fontsize=4.65,
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
            ha="center", va="center", fontsize=4.35, color=PALETTE["ink"],
            linespacing=1.18,
        )
    for y_start, y_end in ((0.72, 0.655), (0.51, 0.445), (0.30, 0.225)):
        draw_arrow(ax_d, (0.50, y_start), (0.50, y_end), color=PALETTE["mid"], linewidth=0.6)
    ax_d.text(
        0.50, 0.005,
        "construction-level obstruction only | no novelty or arbitrary-solution claim",
        transform=ax_d.transAxes, ha="center", va="bottom",
        fontsize=4.15, color=PALETTE["mid"],
    )

    fig.text(
        0.50,
        0.035,
        REQUIRED_LABEL,
        ha="center",
        va="center",
        fontsize=6.0,
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
        fontsize=4.35,
        color=PALETTE["mid"],
    )
    return fig


def write_exports(fig: Any, out_dir: Path, config: dict[str, Any]) -> dict[str, Any]:
    png_dpi = int(config["figure"]["publicationDpi"])
    qa_dpi = int(config["figure"]["qaDpi"])
    common_metadata = {
        "Title": "R0.74X three-packet payment gate",
        "Author": "C. K. Zeng",
        "Subject": REQUIRED_LABEL,
        "Keywords": "Navier-Stokes, analytic schematic, fixed deletion, cubic payment, NOT CLAY",
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
        "schema": "r074x-figure-environment-v1",
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
        "schema": "r074x-figure-results-v1",
        "sourceBinding": binding,
        "bindingMode": config["sourceBinding"]["mode"],
        "mainIndependentAuditSealed": True,
        "mainIndependentAuditVerdict": "PASS",
        "mainIndependentAuditBlockerCount": 0,
        "exactConstants": {
            "p": str(P),
            "d": str(D),
            "q": str(Q),
            "q65": str(Q65),
            "chi65": str(CHI65),
            "chi66": str(CHI66),
            "paymentRate": str(PAYMENT_RATE),
            "maximumStripRate": str(MAXIMUM_STRIP_RATE),
            "paymentMinusMaximumStrip": str(RATE_GAP),
        },
        "derivedComparisons": {
            "paymentMinusMaximumStrip": str(PAYMENT_RATE - MAXIMUM_STRIP_RATE),
            "paymentDominatesMaximumStrip": PAYMENT_RATE > MAXIMUM_STRIP_RATE,
            "stripToPaymentLimit": "(E_2^strip+E_3^strip)/(P_R^M)^(2/3)->0",
            "stripUpperScope": "two audited strip endpoint integrals only",
            "wholeShellUpperBound": False,
        },
        "panelRowCounts": counts,
        "sourceDataRows": len(rows),
        "quantifierOrder": "inf over fixed #S<=1, then sup over time",
        "witnessTimePolicy": "tau_2 and tau_3 may differ; equality is permitted but unnecessary",
        "exports": export,
        "requiredVisibleLabel": REQUIRED_LABEL,
        "claimBoundary": {
            "analyticSchematic": True,
            "derivedAnalyticValues": True,
            "pdeData": False,
            "dnsData": False,
            "clayClaim": False,
            "twoCoordinateTstarEndpointObstruction": True,
            "differentTimePigeonhole": True,
            "equalTargetWStripRouteNoGo": True,
            "actualPaymentNormalizedGateCounterexample": False,
            "stripUpperIsWholeShellUpper": False,
            "wholeShellClockBoundResolved": False,
            "noveltyClaim": False,
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
