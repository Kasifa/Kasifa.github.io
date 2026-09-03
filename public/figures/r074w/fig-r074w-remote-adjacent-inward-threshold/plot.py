#!/usr/bin/env python3
"""Deterministic renderer for the R0.74W analytic four-panel figure."""

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


_MPL_CONFIG = Path(tempfile.mkdtemp(prefix="r074w-mpl-"))
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
ARTIFACT_ID = "fig-r074w-remote-adjacent-inward-threshold"
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
Q64 = Fraction(4, 3969)
Q65 = Fraction(256, 257985)
RHO1 = Fraction(1, 320)
RHO2 = Fraction(1, 1280)
CHI65 = Fraction(12191, 132088320)


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
        ("inner shell radius", "0", "0.5", "p*L_m*R/2", "W.10--W.12", "normalized radius"),
        ("outer shell radius", "0", "1", "p*L_m*R", "W.10--W.12", "normalized radius"),
        ("remote strip lower face", "0", "", "p*L_m*R-R", "W.10", "schematic coordinate only"),
        ("remote strip upper face", "0", "", "p*L_m*R-R/2", "W.10", "schematic coordinate only"),
        ("x1 half-width", "", "", "sqrt(p*L_m)*R/4", "W.10", "schematic coordinate only"),
        ("x2 interval", "", "", "(5R/4,3R/2)", "W.10", "not displayed as a metric axis"),
        ("strip volume", "", "", "sqrt(p*L_m)*R^3/16", "W.13", "exact"),
        ("packet centre", "0", "", "h_m=c_h*L_m*R", "W.6", "outside adjacent shell face"),
        ("centre-to-face gap", "0", "", "d*L_m*R", "W.1,W.6", "d=433/1008"),
    ):
        add("A", series, x, y, "pL_mR-normalized", "pL_mR-normalized", exact, "geometry", locator, note)

    for index in range(101):
        ell = Fraction(6400 + index, 100)
        q_value = P * P / (4 * ell)
        add(
            "B",
            "q(ell)",
            f"{float(ell):.2f}",
            f"{float(q_value):.15g}",
            "ell=tau_m/R^2",
            "rho=log(1/R)/L_m^2",
            str(q_value),
            "threshold curve",
            "W.1--W.5,W.83",
            "exact rational evaluation",
        )
    for series, value, locator, note in (
        ("q64", Q64, "W.1", "uniform sweeping requires rho>q64"),
        ("q65", Q65, "W.2", "uniform survival requires rho<q65"),
        ("original packet 1", RHO1, "W.73--W.75", "swept on fixed free-comparator strip"),
        ("original packet 2", RHO2, "W.73--W.75", "survives on fixed free-comparator strip"),
    ):
        add("B", series, "", f"{float(value):.15g}", "", "rho", str(value), "reference rate", locator, note)

    proof_nodes = (
        ("exact all-winding identity", "sum_n w_n E_br,n[d_z K_T(z+S_t)]", "W.22--W.24b", "no winding deleted"),
        ("central bridge", "n=0; mu_s and v_s exact", "W.24", "conditional Gaussian bridge"),
        ("remote deficit", "-L^-2 log(A)->q(ell)", "W.30,W.33--W.40", "logarithmic scale"),
        ("short time layer", "s=O(R^2/L^2)", "W.36--W.38,W.43", "analytic localization"),
        ("displacement", "-L^-2 log(S_t)->q(ell)", "W.3,W.49b", "in central-bridge conditional probability"),
        ("noncentral windings", "omega_per<=C exp[-1/(11R^2)]", "W.25", "retained remainder"),
        ("survival branch", "S_t/R->0 implies G/H->1", "W.54--W.55", "relative comparator"),
        ("sweeping branch", "S_t/R->infinity implies G/H->0", "W.50--W.57", "relative comparator"),
    )
    for index, (series, exact, locator, note) in enumerate(proof_nodes):
        add("C", series, str(index), "", "diagram-order", "", exact, "proof-map node", locator, note)

    l_values = list(range(18432, 40001, 256))
    if l_values[-1] != 40000:
        l_values.append(40000)
    chi = float(CHI65)
    for l_value in l_values:
        log10_thousands = (
            chi * l_value * l_value - 0.5 * math.log(l_value)
        ) / (1000.0 * math.log(10.0))
        add(
            "D",
            "packet-2 leading endpoint scale",
            str(l_value),
            f"{log10_thousands:.15g}",
            "L_2",
            "10^-3 log10 scale",
            f"(12191/132088320*{l_value}^2-log({l_value})/2)/(1000*log(10))",
            "leading analytic scale",
            "W.76--W.80",
            "unknown prefactor c and -C*L_2 correction omitted; not a finite-L certified lower value",
        )
    add(
        "D", "all-shell conclusion", "", "", "", "", "matching all-shell O(T_*) upper bound is false",
        "proved boundary", "W.80", "frozen placement; packet 2 only"
    )
    add(
        "D", "fixed-deletion boundary", "", "", "", "", "fixed deletion remains open",
        "open boundary", "W.82--Section 10", "coordinate k_2-1=k_1 may be deleted"
    )
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
        "Remote adjacent-inward threshold for the common-shear packet",
        ha="left",
        va="top",
        fontsize=11.1,
        color=PALETTE["ink"],
        fontweight="bold",
    )
    fig.text(
        0.040,
        0.913,
        "R0.74W | exact all-winding bridge comparison | frozen two-packet family",
        ha="left",
        va="top",
        fontsize=6.05,
        color=PALETTE["mid"],
    )
    draw_blossom(fig)

    # Panel A: a deliberately enlarged x1-x3 projection of the very thin strip.
    panel_title(ax_a, "A", "Remote strip inside the adjacent physical shell")
    ax_a.set_xlim(-1.12, 1.12)
    ax_a.set_ylim(0.20, 1.49)
    ax_a.set_aspect("equal", adjustable="box")
    ax_a.axis("off")
    scope_badge(ax_a, "SCHEMATIC / NOT TO SCALE")
    shell = patches.Wedge(
        (0, 0),
        1.0,
        0,
        180,
        width=0.5,
        facecolor=PALETTE["pale"],
        edgecolor=PALETTE["mid"],
        linewidth=0.9,
        hatch="//",
    )
    ax_a.add_patch(shell)
    ax_a.add_patch(
        patches.Rectangle(
            (-0.105, 0.825),
            0.21,
            0.115,
            facecolor=PALETTE["root_open"],
            edgecolor=PALETTE["root_dark"],
            linewidth=1.1,
            hatch="....",
            zorder=5,
        )
    )
    ax_a.plot([-1.0, 1.0], [0, 0], color=PALETTE["ink"], linewidth=0.65)
    ax_a.plot([0, 0], [0.2, 1.44], color=PALETTE["light"], linewidth=0.55, zorder=0)
    ax_a.annotate(
        r"outer face $pL_mR$",
        xy=(0.48, 0.875),
        xytext=(0.72, 1.16),
        fontsize=5.3,
        color=PALETTE["ink"],
        arrowprops={"arrowstyle": "->", "color": PALETTE["mid"], "linewidth": 0.65},
    )
    ax_a.annotate(
        r"remote strip $\mathcal{S}_m$" + "\n" + r"width $R$ in $x_3$",
        xy=(0.10, 0.885),
        xytext=(0.23, 0.66),
        fontsize=5.25,
        color=PALETTE["root_dark"],
        fontweight="bold",
        arrowprops={"arrowstyle": "->", "color": PALETTE["root"], "linewidth": 0.75},
    )
    ax_a.text(
        -0.72,
        0.60,
        r"$A_{k_m-1}(R)$" + "\n" + r"$pL_mR/2<|x|<pL_mR$",
        ha="center",
        va="center",
        fontsize=5.3,
        color=PALETTE["ink"],
    )
    ax_a.plot([0], [1.34], marker="o", markersize=4.2, color=PALETTE["root_dark"], zorder=8)
    ax_a.text(
        0.04,
        1.35,
        r"packet centre $h_m=c_hL_mR$",
        ha="left",
        va="center",
        fontsize=5.15,
        color=PALETTE["root_dark"],
    )
    ax_a.annotate(
        "",
        xy=(0, 1.31),
        xytext=(0, 1.01),
        arrowprops={"arrowstyle": "<->", "color": PALETTE["root"], "linewidth": 0.8},
    )
    ax_a.text(0.055, 1.155, r"gap $dL_mR$", fontsize=5.1, color=PALETTE["root_dark"], va="center")
    ax_a.text(
        0.02,
        0.02,
        r"$|x_1|<\frac{1}{4}\sqrt{pL_m}R$;  $5R/4<x_2<3R/2$"
        + "\n"
        + r"$|\mathcal{S}_m|=\frac{1}{16}\sqrt{pL_m}R^3$;  $\Psi_{k_m-1}^R=1$",
        transform=ax_a.transAxes,
        ha="left",
        va="bottom",
        fontsize=4.75,
        color=PALETTE["mid"],
        bbox={"boxstyle": "round,pad=0.18", "facecolor": PALETTE["paper"], "edgecolor": "none", "alpha": 0.88},
    )

    # Panel B: threshold curve and strict uniform regimes.
    panel_title(ax_b, "B", "Logarithmic survival–sweeping threshold")
    ell_values = np.array([float(row["x"]) for row in rows if row["panel"] == "B" and row["series"] == "q(ell)"])
    q_values = 1000.0 * np.array([float(row["y"]) for row in rows if row["panel"] == "B" and row["series"] == "q(ell)"])
    y_q64 = 1000.0 * float(Q64)
    y_q65 = 1000.0 * float(Q65)
    y_rho1 = 1000.0 * float(RHO1)
    y_rho2 = 1000.0 * float(RHO2)
    ax_b.set_xlim(64.0, 65.0)
    ax_b.set_ylim(0.55, 3.35)
    ax_b.axhspan(0.55, y_q65, color=PALETTE["paper"], zorder=0)
    ax_b.axhspan(y_q65, y_q64, facecolor=PALETTE["light"], alpha=0.55, hatch="////", zorder=0)
    ax_b.axhspan(y_q64, 3.35, color=PALETTE["root_open"], zorder=0)
    ax_b.plot(ell_values, q_values, color=PALETTE["root_dark"], linewidth=1.45, zorder=4)
    ax_b.axhline(y_q64, color=PALETTE["ink"], linewidth=0.7, linestyle=(0, (4, 2)))
    ax_b.axhline(y_q65, color=PALETTE["mid"], linewidth=0.7, linestyle=(0, (1.5, 1.5)))
    ax_b.axhline(y_rho1, color=PALETTE["root_dark"], linewidth=0.95, linestyle=(0, (5, 2)), zorder=3)
    ax_b.axhline(y_rho2, color=PALETTE["mid"], linewidth=0.9, linestyle="-.", zorder=3)
    ax_b.plot([64.18], [y_rho1], marker="o", markersize=4.3, color=PALETTE["root_dark"], zorder=5)
    ax_b.plot([64.18], [y_rho2], marker="s", markersize=4.5, markerfacecolor=PALETTE["paper"], markeredgecolor=PALETTE["mid"], color=PALETTE["mid"], linestyle="None", zorder=5)
    ax_b.text(64.23, y_rho1 + 0.045, r"packet 1: $\rho_1=1/320$  → swept", fontsize=5.05, color=PALETTE["root_dark"], va="bottom")
    ax_b.text(64.23, y_rho2 - 0.055, r"packet 2: $\rho_2=1/1280$  → survives", fontsize=5.05, color=PALETTE["ink"], va="top")
    ax_b.text(64.97, 2.10, r"SWEEPING  $\rho>q_{64}$", fontsize=5.2, color=PALETTE["root_dark"], ha="right", fontweight="bold")
    ax_b.annotate(
        "q65–q64 band: UNCLASSIFIED BY\nUNIFORM SLAB ENDPOINT TESTS",
        xy=(64.55, (y_q64 + y_q65) / 2),
        xytext=(64.50, 1.46),
        ha="center",
        va="center",
        fontsize=4.15,
        color=PALETTE["ink"],
        arrowprops={"arrowstyle": "->", "color": PALETTE["mid"], "linewidth": 0.65},
    )
    ax_b.text(64.50, 1.20, r"fixed $\ell$: strict sides of $q(\ell)$ resolved; equality open", fontsize=4.25, color=PALETTE["mid"], ha="center", va="bottom")
    ax_b.text(64.97, 0.61, r"SURVIVAL  $\rho<q_{65}$", fontsize=5.2, color=PALETTE["ink"], ha="right", va="bottom", fontweight="bold")
    ax_b.text(64.03, y_q64 + 0.035, r"$q_{64}=4/3969$", fontsize=4.65, color=PALETTE["ink"], va="bottom")
    ax_b.text(64.97, y_q65 - 0.035, r"$q_{65}=256/257985$", fontsize=4.65, color=PALETTE["mid"], ha="right", va="top")
    ax_b.set_xlabel(r"heat age $\ell=\tau_m/R^2$", fontsize=5.4, labelpad=2)
    ax_b.set_ylabel(r"rate $\rho=\log(1/R)/L_m^2$  ($\times10^{-3}$)", fontsize=5.2, labelpad=3)
    ax_b.set_xticks([64.0, 64.5, 65.0])
    ax_b.tick_params(axis="both", labelsize=4.8, length=2.5, width=0.6)
    for spine in ("top", "right"):
        ax_b.spines[spine].set_visible(False)
    ax_b.spines["left"].set_color(PALETTE["mid"])
    ax_b.spines["bottom"].set_color(PALETTE["mid"])
    scope_badge(ax_b, r"$q(\ell)=p^2/(4\ell)$")

    # Panel C: a proof dependency map; there are intentionally no trajectories.
    panel_title(ax_c, "C", "Exact all-winding conditional-bridge proof map")
    ax_c.set_xlim(0, 1)
    ax_c.set_ylim(0, 1)
    ax_c.axis("off")
    scope_badge(ax_c, "NO SAMPLED PATHS")
    proof_box(
        ax_c,
        0.10,
        0.75,
        0.80,
        0.16,
        "exact all-winding conditional expectation"
        + "\n"
        + r"$\Sigma_{n\in\mathbb{Z}}w_n\mathbb{E}_{n,y}^{\mathrm{br}}[\partial_zK_T^{\mathrm{per}}(z+\mathfrak{S}_t)]$",
        filled=True,
        fontsize=4.75,
    )
    proof_box(ax_c, 0.06, 0.50, 0.38, 0.12, r"central bridge $n=0$" + "\n" + r"exact $(\mu_s,v_s)$", fontsize=5.0)
    proof_box(ax_c, 0.56, 0.50, 0.38, 0.12, r"all $n\ne0$ retained" + "\n" + r"weighted bridge copies", dashed=True, fontsize=4.9)
    proof_box(
        ax_c,
        0.05,
        0.21,
        0.40,
        0.20,
        r"$-L^{-2}\log A\to q(\ell)$"
        + "\n"
        + r"layer $s=O(R^2/L^2)$"
        + "\n"
        + r"$-L^{-2}\log\mathfrak{S}_t\to q(\ell)$"
        + "\n"
        + "in central-bridge conditional probability",
        filled=True,
        fontsize=4.05,
    )
    proof_box(
        ax_c,
        0.56,
        0.25,
        0.38,
        0.14,
        r"$\omega_{\mathrm{per}}\leq Ce^{-1/(11R^2)}$"
        + "\n"
        + r"$\leq Ce^{-75L^2}$",
        dashed=True,
        fontsize=4.8,
    )
    proof_box(
        ax_c,
        0.15,
        0.010,
        0.70,
        0.13,
        r"compare $\mathfrak{S}_t/R$:  $0\Rightarrow G/H\to1$   |   $\infty\Rightarrow G/H\to0$"
        + "\n"
        + "relative comparator; amplitude + inversion + other packet checked",
        filled=True,
        fontsize=4.55,
    )
    draw_arrow(ax_c, (0.38, 0.75), (0.25, 0.62))
    draw_arrow(ax_c, (0.62, 0.75), (0.75, 0.62))
    draw_arrow(ax_c, (0.25, 0.50), (0.25, 0.41))
    draw_arrow(ax_c, (0.75, 0.50), (0.75, 0.39), linestyle="--")
    draw_arrow(ax_c, (0.25, 0.21), (0.39, 0.14))
    draw_arrow(ax_c, (0.75, 0.25), (0.61, 0.14), linestyle="--")

    # Panel D: only the leading analytic scale is numerical; c and -CL are unknown.
    panel_title(ax_d, "D", "Endpoint divergence; fixed deletion open")
    d_rows = [row for row in rows if row["panel"] == "D" and row["series"] == "packet-2 leading endpoint scale"]
    l2 = np.array([float(row["x"]) for row in d_rows])
    leading = np.array([float(row["y"]) for row in d_rows])
    ax_d.plot(l2, leading, color=PALETTE["root_dark"], linewidth=1.55, zorder=3)
    ax_d.fill_between(l2, 0, leading, color=PALETTE["root_open"], alpha=0.70, hatch="..", edgecolor=PALETTE["root_light"], linewidth=0.0, zorder=1)
    ax_d.plot([l2[0]], [leading[0]], marker="s", markersize=4.3, markerfacecolor=PALETTE["paper"], markeredgecolor=PALETTE["root_dark"], color=PALETTE["root_dark"], linestyle="None", zorder=4)
    ax_d.text(l2[0] + 650, leading[0] + 1.6, r"$L_2=2L_1\geq18432$", fontsize=4.75, color=PALETTE["ink"])
    ax_d.set_xlim(18432, 40000)
    ax_d.set_ylim(0, max(leading) * 1.08)
    ax_d.set_xlabel(r"outer-packet scale $L_2$", fontsize=5.4, labelpad=2)
    ax_d.set_ylabel(r"$10^{-3}\log_{10}[L_2^{-1/2}e^{\chi(65)L_2^2}]$", fontsize=5.0, labelpad=3)
    ax_d.tick_params(axis="both", labelsize=4.8, length=2.5, width=0.6)
    ax_d.grid(axis="y", color=PALETTE["light"], linewidth=0.45, linestyle=(0, (2, 2)), zorder=0)
    for spine in ("top", "right"):
        ax_d.spines[spine].set_visible(False)
    ax_d.spines["left"].set_color(PALETTE["mid"])
    ax_d.spines["bottom"].set_color(PALETTE["mid"])
    ax_d.text(
        0.035,
        0.94,
        r"$\chi(65)=12191/132088320>0$"
        + "\n"
        + r"PROVED: $K_{k_2-1,R}(\tau_2)/T_*\to\infty$"
        + "\n"
        + r"all-shell $O(T_*)$: FALSE for frozen placement",
        transform=ax_d.transAxes,
        ha="left",
        va="top",
        fontsize=4.7,
        color=PALETTE["root_dark"],
        fontweight="bold",
        bbox={"boxstyle": "round,pad=0.25", "facecolor": PALETTE["paper"], "edgecolor": PALETTE["root_light"], "linewidth": 0.65},
        zorder=5,
    )
    ax_d.text(
        0.97,
        0.055,
        r"boundary: $k_2-1=k_1$ may be deleted"
        + "\n"
        + "FIXED DELETION REMAINS OPEN"
        + "\n"
        + r"plotted leading factor only; unknown $c$ and $-CL_2$ omitted",
        transform=ax_d.transAxes,
        ha="right",
        va="bottom",
        fontsize=4.55,
        color=PALETTE["ink"],
        bbox={"boxstyle": "round,pad=0.24", "facecolor": PALETTE["pale"], "edgecolor": PALETTE["mid"], "linewidth": 0.65},
        zorder=5,
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
        "Title": "R0.74W remote adjacent-inward threshold",
        "Author": "C. K. Zeng",
        "Subject": REQUIRED_LABEL,
        "Keywords": "Navier-Stokes, analytic schematic, Brownian bridge, remote strip, NOT CLAY",
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
        "schema": "r074w-figure-environment-v1",
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
    l2_rows = [row for row in rows if row["panel"] == "D" and row["series"] == "packet-2 leading endpoint scale"]
    return {
        "artifactId": ARTIFACT_ID,
        "schema": "r074w-figure-results-v1",
        "sourceBinding": binding,
        "bindingMode": config["sourceBinding"]["mode"],
        "mainIndependentAuditSealed": True,
        "mainIndependentAuditVerdict": "PASS",
        "mainIndependentAuditBlockerCount": 0,
        "exactConstants": {
            "p": str(P),
            "d": str(D),
            "q64": str(Q64),
            "q65": str(Q65),
            "rho1": str(RHO1),
            "rho2": str(RHO2),
            "chi65": str(CHI65),
        },
        "derivedComparisons": {
            "rho1MinusQ64": str(RHO1 - Q64),
            "q65MinusRho2": str(Q65 - RHO2),
            "originalPacket1Regime": "sweeping",
            "originalPacket2Regime": "survival",
            "criticalTransition": "open",
            "fixedDeletion": "open",
        },
        "panelRowCounts": counts,
        "sourceDataRows": len(rows),
        "panelD": {
            "xVariable": "L_2",
            "minimumL2": int(l2_rows[0]["x"]),
            "maximumL2": int(l2_rows[-1]["x"]),
            "quantity": "10^-3 log10[L_2^-1/2 exp(chi(65)L_2^2)]",
            "qualification": "leading analytic scale only; unknown c and -C*L_2 omitted",
        },
        "exports": export,
        "requiredVisibleLabel": REQUIRED_LABEL,
        "claimBoundary": {
            "analyticSchematic": True,
            "derivedAnalyticValues": True,
            "pdeData": False,
            "dnsData": False,
            "clayClaim": False,
            "allShellMatchingOTUpperBoundForFrozenPlacement": False,
            "fixedDeletionResolved": False,
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
