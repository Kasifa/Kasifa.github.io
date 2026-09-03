#!/usr/bin/env python3
"""Render the source-bound R0.74S fixed-deletion figure archive."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import resource
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REPOSITORY_DEFAULT = HERE.parents[3]
SOURCE_FILES = (
    "README.md", "caption.md", "chart-contract-and-source-data.md", "command.txt",
    "config.json", "contract.json", "plot.py", "qa-protocol.md", "requirements.txt",
    "validate.py",
)
RAW_FILES = (
    "environment.json", "figure.pdf", "figure.png", "figure.svg",
    "progress.ndjson", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
    "resource-log.ndjson", "results.json", "source-data.csv",
)
METADATA_FILES = ("SHA256SUMS", "manifest.json", "qa-report.md", "validation.json")
CSV_FIELDS = (
    "panel", "record", "series", "x", "y", "x_unit", "y_unit",
    "evidence_class", "formula_source", "method",
)
FORMULA_SOURCE = "core 5a9c172e, equations (S.477)-(S.492)"
PALETTE = {
    "navy": "#244C70",
    "navy_dark": "#18364F",
    "navy_open": "#DCE8F0",
    "orange": "#B45A36",
    "orange_dark": "#7E3E27",
    "orange_open": "#F3E2D8",
    "charcoal": "#283238",
    "gray": "#737E85",
    "mid_gray": "#AAB2B8",
    "light_gray": "#DDE1E4",
    "xlight_gray": "#F2F4F5",
    "paper": "#FFFFFF",
}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    need(isinstance(value, dict), "JSON root must be an object: " + path.name)
    return value


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def git_bytes(repository: Path, args: list[str]) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repository), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    need(
        result.returncode == 0,
        "git failed: " + result.stderr.decode("utf-8", "replace").strip(),
    )
    return result.stdout


def git_text(repository: Path, args: list[str]) -> str:
    return git_bytes(repository, args).decode("utf-8").strip()


def verify_source_binding(repository: Path, config: dict[str, Any]) -> dict[str, bytes]:
    source = config["sourceBinding"]
    commit = source["commit"]
    git_text(repository, ["cat-file", "-e", commit + "^{commit}"])
    ancestor = subprocess.run(
        ["git", "-C", str(repository), "merge-base", "--is-ancestor", commit, "HEAD"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    need(ancestor.returncode == 0, "frozen core commit is not an ancestor of HEAD")
    blobs: dict[str, bytes] = {}
    for relative, lock in source["files"].items():
        payload = git_bytes(repository, ["cat-file", "blob", commit + ":" + relative])
        actual_oid = git_text(repository, ["rev-parse", commit + ":" + relative])
        need(actual_oid == lock["gitBlobObjectId"], "Git blob drift: " + relative)
        need(sha256_bytes(payload) == lock["sha256"], "SHA-256 drift: " + relative)
        blobs[relative] = payload

    certificate = json.loads(blobs["research/r074s_fixed_deletion_certificate.json"])
    note_path = "research/r074s_fixed_deletion_simultaneous_height.md"
    need(certificate.get("verdict") == "PASS", "main certificate verdict drift")
    need(
        certificate.get("note", {}).get("sha256") == source["files"][note_path]["sha256"],
        "certificate-to-note binding drift",
    )
    report = blobs["research/r074s_fixed_deletion_certificate_report.md"].decode("utf-8")
    note = blobs[note_path].decode("utf-8")
    independent = blobs["research/r074s_fixed_deletion_independent_audit.md"].decode("utf-8")
    primary = blobs["research/r074s_fixed_deletion_primary_audit.md"].decode("utf-8")
    literature = blobs["research/r074s_fixed_deletion_literature_audit.md"].decode("utf-8")
    qa_report = blobs["research/r074s_fixed_deletion_qa_report.md"].decode("utf-8")
    need("**PASS**" in report, "main certificate report status drift")
    need("**PASS**" in independent and "72144" in independent,
         "independent audit status drift")
    need("**Verdict: PASS within the stated route-reduction scope.**" in primary,
         "primary audit status drift")
    need("No inspected source proves the full Step 18 quantifier package" in literature,
         "literature audit boundary drift")
    need("**PASS**" in qa_report and "283,157" in qa_report,
         "QA report status drift")
    need("**NOT CLAY.**" in note, "note claim boundary drift")
    need("\\tag{S.492}" in note and "ABSTRACT CLOCK STRESS TESTS" in note,
         "note formula/scope locator drift")
    return blobs


def insert_dependencies(path: Path) -> None:
    resolved = path.expanduser().resolve()
    need(resolved.is_dir(), "--deps is not a directory")
    sys.path.insert(0, str(resolved))


def live_runtime_versions(config: dict[str, Any]) -> dict[str, str]:
    actual = {
        "python": platform.python_version(),
        "numpy": importlib.metadata.version("numpy"),
        "matplotlib": importlib.metadata.version("matplotlib"),
        "pillow": importlib.metadata.version("pillow"),
        "pypdf": importlib.metadata.version("pypdf"),
        "pypdfium2": importlib.metadata.version("pypdfium2"),
    }
    need(actual == config["runtime"], f"runtime drift: expected {config['runtime']}, got {actual}")
    return actual


def preflight_archive() -> None:
    actual = {path.name for path in HERE.iterdir()}
    allowed = set(SOURCE_FILES + RAW_FILES + METADATA_FILES)
    need(set(SOURCE_FILES).issubset(actual), "source inventory is incomplete")
    need(actual.issubset(allowed), "unexpected package entry: " + repr(sorted(actual - allowed)))
    need(
        all((HERE / name).is_file() and not (HERE / name).is_symlink() for name in SOURCE_FILES),
        "source file or symlink drift",
    )


def number(value: float) -> str:
    value = float(value)
    if value == 0.0:
        return "0"
    return format(value, ".17g")


def generate_payload(config: dict[str, Any], np: Any) -> tuple[list[dict[str, str]], dict[str, Any], dict[str, Any]]:
    rows: list[dict[str, str]] = []

    panel_a_nodes = [
        ("H_hyb", 0.20, 1.35),
        ("H_fix", 1.45, 1.35),
        ("O_F_plus", 2.70, 1.35),
        ("H1_F", 3.95, 1.35),
        ("L_K", 1.45, 0.35),
        ("M_K", 2.70, 0.35),
    ]
    for index, (series, x, y) in enumerate(panel_a_nodes, start=1):
        rows.append({
            "panel": "A", "record": f"node-{index:02d}", "series": series,
            "x": number(x), "y": number(y), "x_unit": "schematic",
            "y_unit": "schematic", "evidence_class": "proved-relation-diagram",
            "formula_source": FORMULA_SOURCE, "method": "exact-layout-coordinate",
        })
    panel_a_edges = [
        ("literal_hyb_to_fix", 0.20, 1.45),
        ("literal_fix_to_O", 1.45, 2.70),
        ("literal_O_to_H1", 2.70, 3.95),
        ("literal_L_to_M", 1.45, 2.70),
        ("payment_fix_to_L", 1.45, 1.45),
        ("payment_L_to_fix", 1.45, 1.45),
        ("payment_M_to_O", 2.70, 2.70),
    ]
    for index, (series, x, y) in enumerate(panel_a_edges, start=1):
        rows.append({
            "panel": "A", "record": f"edge-{index:02d}", "series": series,
            "x": number(x), "y": number(y), "x_unit": "schematic_source_x",
            "y_unit": "schematic_target_x", "evidence_class": "proved-relation-diagram",
            "formula_source": FORMULA_SOURCE,
            "method": "literal-inequality" if series.startswith("literal") else "known-payment-estimate",
        })

    panel_b = config["panelB"]
    n = int(panel_b["n"])
    m = int(panel_b["m"])
    height = float(panel_b["height"])
    times = np.linspace(0.0, 1.0, int(panel_b["points"]))
    clocks = []
    for j in range(1, m + 1):
        center = (2.0 * j - 1.0) / (2.0 * m)
        values = height * np.maximum(1.0 - 2.0 * m * np.abs(times - center), 0.0)
        clocks.append(values)
        for index, (time_value, clock_value) in enumerate(zip(times, values, strict=True)):
            rows.append({
                "panel": "B", "record": f"clock-{j:02d}-{index:04d}",
                "series": f"K_{j}", "x": number(time_value), "y": number(clock_value),
                "x_unit": "normalized_time", "y_unit": "clock_height",
                "evidence_class": "exact-abstract-clock",
                "formula_source": FORMULA_SOURCE, "method": "equation-S.489",
            })
    clock_array = np.asarray(clocks, dtype=float)

    exact_values = [
        ("H_hyb", 0.0),
        ("H_fix", height),
        ("L_K", height),
        ("O_F_plus", (m - n) * height),
        ("M_K", (m - n) * height),
        ("H1_F", 2.0 * (m - n) * height),
    ]
    for index, (series, value) in enumerate(exact_values, start=1):
        rows.append({
            "panel": "C", "record": f"functional-{index:02d}", "series": series,
            "x": number(float(index - 1)), "y": number(value),
            "x_unit": "ordered_functional", "y_unit": "exact_value",
            "evidence_class": "exact-abstract-clock",
            "formula_source": FORMULA_SOURCE, "method": "equation-S.490",
        })

    panel_d = config["panelD"]
    d_n = int(panel_d["n"])
    d_m = int(panel_d["m"])
    heights = np.logspace(
        math.log10(float(panel_d["heightMinimum"])),
        math.log10(float(panel_d["heightMaximum"])),
        int(panel_d["points"]),
    )
    ratios = heights ** (1.0 / 3.0) / (2.0 * d_m) ** (2.0 / 3.0)
    for index, (height_value, ratio) in enumerate(zip(heights, ratios, strict=True)):
        rows.append({
            "panel": "D", "record": f"ratio-{index:03d}",
            "series": "H_fix_over_P_to_2_over_3", "x": number(height_value),
            "y": number(ratio), "x_unit": "clock_height_H",
            "y_unit": "dimensionless_ratio", "evidence_class": "exact-abstract-clock",
            "formula_source": FORMULA_SOURCE, "method": "equation-S.492",
        })

    positive_counts = np.sum(clock_array > 1.0e-14, axis=0)
    slope, intercept = np.polyfit(np.log(heights), np.log(ratios), 1)
    expected_values = {
        "H_hyb": 0.0,
        "H_fix": 1.0,
        "L_K": 1.0,
        "O_F_plus": 3.0,
        "M_K": 3.0,
        "H1_F": 6.0,
    }
    checkpoint_heights = np.asarray([1.0, 8.0, 64.0, 512.0, 4096.0])
    checkpoint_ratios = checkpoint_heights ** (1.0 / 3.0) / 4.0
    exact_checkpoint_ratios = np.asarray([0.25, 0.5, 1.0, 2.0, 4.0])
    audit = {
        "checksPassed": bool(
            n == 2 and m == 5 and height == 1.0
            and d_n == 2 and d_m == 4
            and int(np.max(positive_counts)) <= 1
            and float(np.max(np.abs(np.max(clock_array, axis=1) - height))) <= 1.0e-14
            and max(abs(dict(exact_values)[key] - value) for key, value in expected_values.items()) <= 1.0e-14
            and abs(float(slope) - 1.0 / 3.0) <= 1.0e-13
            and float(np.max(np.abs(checkpoint_ratios - exact_checkpoint_ratios))) <= 1.0e-13
        ),
        "clockCount": m,
        "clockHeight": height,
        "clockPeaks": [float(value) for value in np.max(clock_array, axis=1)],
        "clockTotalVariations": [2.0 * height] * m,
        "deletedCoordinateBudget": n,
        "exactFunctionalValues": {key: value for key, value in exact_values},
        "fullAbsoluteLedger": 2.0 * m * height,
        "maximumSimultaneouslyPositiveClocks": int(np.max(positive_counts)),
        "panelDCheckpointHeights": [float(value) for value in checkpoint_heights],
        "panelDCheckpointRatios": [float(value) for value in checkpoint_ratios],
        "panelDExpectedCheckpointRatios": [float(value) for value in exact_checkpoint_ratios],
        "panelDFixedM": d_m,
        "panelDFixedN": d_n,
        "panelDLogIntercept": float(intercept),
        "panelDLogSlope": float(slope),
        "panelDMaximumSlopeError": abs(float(slope) - 1.0 / 3.0),
        "strictClockOrder": bool(0.0 < height < (m - n) * height < 2.0 * (m - n) * height),
        "tolerances": {
            "clockPeakError": 1.0e-14,
            "functionalValueError": 1.0e-14,
            "slopeError": 1.0e-13,
        },
    }
    arrays = {
        "panelANodes": panel_a_nodes,
        "times": times,
        "clocks": clock_array,
        "exactValues": exact_values,
        "heights": heights,
        "ratios": ratios,
        "checkpointHeights": checkpoint_heights,
        "checkpointRatios": checkpoint_ratios,
    }
    return rows, arrays, audit


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def apply_axes_style(ax: Any) -> None:
    ax.set_facecolor(PALETTE["paper"])
    ax.tick_params(axis="both", colors=PALETTE["charcoal"], labelsize=6.4, length=2.5, width=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for name in ("left", "bottom"):
        ax.spines[name].set_color(PALETTE["gray"])
        ax.spines[name].set_linewidth(0.75)
    ax.grid(axis="both", color=PALETTE["light_gray"], linewidth=0.55, alpha=0.9, zorder=0)


def panel_title(ax: Any, letter: str, title: str) -> None:
    ax.set_title(r"$\bf{" + letter + r"}$  " + title, loc="left", fontsize=8.2,
                 color=PALETTE["charcoal"], pad=7.0, fontweight="normal")


def scope_badge(ax: Any) -> None:
    ax.text(
        0.985, 0.975, "ABSTRACT CLOCK TEST / NOT PDE DATA",
        transform=ax.transAxes, ha="right", va="top", fontsize=4.7,
        color=PALETTE["orange_dark"], fontweight="bold",
        bbox={"boxstyle": "round,pad=0.22", "facecolor": PALETTE["orange_open"],
              "edgecolor": PALETTE["orange"], "linewidth": 0.55},
        zorder=10,
    )


def draw_blossom(fig: Any, patches: Any) -> None:
    center = (0.958, 0.936)
    radius = 0.0105
    for index, angle in enumerate((90, 18, -54, -126, 162)):
        radians = math.radians(angle)
        color = PALETTE["navy"] if index % 2 == 0 else PALETTE["orange"]
        petal = patches.Ellipse(
            (center[0] + 0.014 * math.cos(radians), center[1] + 0.020 * math.sin(radians)),
            width=radius, height=radius * 1.55, angle=angle - 90,
            transform=fig.transFigure, facecolor="none", edgecolor=color,
            linewidth=0.9, zorder=30,
        )
        fig.add_artist(petal)
    fig.add_artist(patches.Circle(center, radius=0.0035, transform=fig.transFigure,
                                  facecolor=PALETTE["charcoal"], edgecolor="none", zorder=31))


def draw_relation_node(ax: Any, patches: Any, x: float, y: float, label: str,
                       edge: str, fill: str) -> None:
    box = patches.FancyBboxPatch(
        (x - 0.43, y - 0.19), 0.86, 0.38,
        boxstyle="round,pad=0.035,rounding_size=0.055",
        facecolor=fill, edgecolor=edge, linewidth=1.05, zorder=3,
    )
    ax.add_patch(box)
    ax.text(x, y, label, ha="center", va="center", fontsize=7.1,
            color=PALETTE["charcoal"], zorder=4)


def render_figure(config: dict[str, Any], arrays: dict[str, Any], np: Any,
                  plt: Any, patches: Any, lines: Any) -> tuple[Any, dict[str, Any]]:
    width_in = float(config["widthMillimetres"]) / 25.4
    height_in = float(config["heightMillimetres"]) / 25.4
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 7.0,
        "axes.labelcolor": PALETTE["charcoal"],
        "axes.titlecolor": PALETTE["charcoal"],
        "figure.facecolor": PALETTE["paper"],
        "savefig.facecolor": PALETTE["paper"],
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "svg.hashsalt": "r074s-fixed-deletion-quantifier-gap",
        "axes.unicode_minus": False,
    })
    fig, axes = plt.subplots(2, 2, figsize=(width_in, height_in), dpi=int(config["pngDpi"]))
    fig.subplots_adjust(left=0.085, right=0.975, bottom=0.105, top=0.815,
                        wspace=0.30, hspace=0.48)
    ax_a, ax_b, ax_c, ax_d = axes.ravel()

    fig.text(0.045, 0.955, "Fixed-deletion functionals and the temporal quantifier gap",
             ha="left", va="top", fontsize=12.0, color=PALETTE["charcoal"],
             fontweight="bold")
    fig.text(0.045, 0.913,
             "R0.74S Step 18  |  ANALYTIC SCHEMATIC · ABSTRACT CLOCK TEST · NOT PDE DATA · NOT DNS · NOT CLAY",
             ha="left", va="top", fontsize=6.7, color=PALETTE["gray"])
    draw_blossom(fig, patches)

    # Panel A: only literal inequalities receive solid arrows.  The other
    # relations are explicitly payment-shifted, never drawn as equalities.
    panel_title(ax_a, "A", "General hierarchy and known-payment links")
    ax_a.set_xlim(-0.35, 4.50)
    ax_a.set_ylim(-0.27, 1.77)
    ax_a.axis("off")
    node_map = {name: (x, y) for name, x, y in arrays["panelANodes"]}
    labels = {
        "H_hyb": r"$\mathfrak{H}^{\rm hyb}$",
        "H_fix": r"$\mathfrak{H}^{\rm fix}$",
        "O_F_plus": r"$\mathfrak{O}^{F,+}$",
        "H1_F": r"$\mathfrak{H}^F_1$",
        "L_K": r"$\mathfrak{L}^K$",
        "M_K": r"$\mathfrak{M}^K$",
    }
    for key in ("H_hyb", "H_fix", "O_F_plus", "H1_F"):
        x, y = node_map[key]
        draw_relation_node(ax_a, patches, x, y, labels[key], PALETTE["navy"], PALETTE["navy_open"])
    for key in ("L_K", "M_K"):
        x, y = node_map[key]
        draw_relation_node(ax_a, patches, x, y, labels[key], PALETTE["orange"], PALETTE["orange_open"])
    for left, right in (("H_hyb", "H_fix"), ("H_fix", "O_F_plus"), ("O_F_plus", "H1_F")):
        x0, y0 = node_map[left]
        x1, y1 = node_map[right]
        ax_a.annotate("", xy=(x1 - 0.45, y1), xytext=(x0 + 0.45, y0),
                      arrowprops={"arrowstyle": "-|>", "color": PALETTE["charcoal"],
                                  "linewidth": 0.85, "mutation_scale": 8})
        ax_a.text((x0 + x1) / 2.0, y0 + 0.08, r"$\leq$", ha="center", va="bottom",
                  fontsize=7.0, color=PALETTE["charcoal"])
    x0, y0 = node_map["L_K"]
    x1, y1 = node_map["M_K"]
    ax_a.annotate("", xy=(x1 - 0.45, y1), xytext=(x0 + 0.45, y0),
                  arrowprops={"arrowstyle": "-|>", "color": PALETTE["charcoal"],
                              "linewidth": 0.85, "mutation_scale": 8})
    ax_a.text((x0 + x1) / 2.0, y0 + 0.08, r"$\leq$", ha="center", va="bottom",
              fontsize=7.0, color=PALETTE["charcoal"])
    # Payment-shifted vertical links, with both directions written literally.
    ax_a.plot([1.45, 1.45], [0.56, 1.13], color=PALETTE["orange"], linewidth=0.85,
              linestyle=(0, (3, 2)), zorder=1)
    ax_a.text(1.51, 0.81,
              r"$\mathfrak{H}^{\rm fix}\leq\mathfrak{L}^K+B_Q$" + "\n" +
              r"$\mathfrak{L}^K\leq\Pi+6\mathfrak{H}^{\rm fix}$",
              ha="left", va="center", fontsize=5.15, color=PALETTE["orange_dark"],
              bbox={"facecolor": PALETTE["paper"], "edgecolor": "none", "pad": 1.0})
    ax_a.plot([2.70, 2.70], [0.56, 1.13], color=PALETTE["orange"], linewidth=0.85,
              linestyle=(0, (3, 2)), zorder=1)
    ax_a.text(2.76, 0.77, r"$\mathfrak{M}^K\leq\mathfrak{O}^{F,+}+B_Q$",
              ha="left", va="center", fontsize=5.15, color=PALETTE["orange_dark"],
              bbox={"facecolor": PALETTE["paper"], "edgecolor": "none", "pad": 1.0})
    ax_a.text(0.20, 0.83, "solid = literal inequality\ndashed = known-payment estimate",
              ha="center", va="center", fontsize=5.15, color=PALETTE["gray"],
              linespacing=1.25)
    ax_a.text(0.02, -0.18,
              r"$o_k^F:=\sup_{a<b}[F_k(b)-F_k(a)]_+$;  "
              r"$\mathfrak{O}^{F,+}:=\inf_{|S|\leq N}\sum_{k\notin S}o_k^F$",
              ha="left", va="bottom", fontsize=5.25, color=PALETTE["charcoal"])

    # Panel B: exact disjoint triangular clocks.
    panel_title(ax_b, "B", "Five disjoint triangular clocks")
    apply_axes_style(ax_b)
    scope_badge(ax_b)
    times = arrays["times"]
    deleted = set(int(value) for value in config["panelB"]["deletedCoordinates"])
    for index, values in enumerate(arrays["clocks"], start=1):
        if index in deleted:
            color, style, fill = PALETTE["mid_gray"], (0, (3, 2)), PALETTE["xlight_gray"]
            width, alpha = 0.9, 0.65
        else:
            color, style, fill = PALETTE["navy"], "-", PALETTE["navy_open"]
            width, alpha = 1.15, 0.82
        ax_b.fill_between(times, values, 0.0, facecolor=fill, edgecolor="none", alpha=alpha, zorder=1)
        ax_b.plot(times, values, color=color, linewidth=width, linestyle=style, zorder=2)
        center = (2.0 * index - 1.0) / (2.0 * int(config["panelB"]["m"]))
        ax_b.text(center, 1.035, rf"$K_{index}$", ha="center", va="bottom", fontsize=5.4,
                  color=color)
    ax_b.set_xlim(0.0, 1.0)
    ax_b.set_ylim(0.0, 1.22)
    ax_b.set_xticks(np.linspace(0.0, 1.0, 6))
    ax_b.set_yticks([0.0, 0.5, 1.0])
    ax_b.set_xlabel(r"normalized time $t\in[0,1]$", fontsize=6.5, labelpad=2)
    ax_b.set_ylabel(r"$K_j(t)=\phi_j(t)$", fontsize=6.5, labelpad=3)
    ax_b.text(0.015, 0.77, r"$N=2,\ M=5,\ H=1$" + "\ninteriors disjoint",
              transform=ax_b.transAxes, ha="left", va="top", fontsize=5.4,
              color=PALETTE["charcoal"])
    legend_handles = [
        lines.Line2D([0], [0], color=PALETTE["mid_gray"], linewidth=1.0,
                     linestyle=(0, (3, 2)), label=r"one illustrative $S$"),
        lines.Line2D([0], [0], color=PALETTE["navy"], linewidth=1.2,
                     linestyle="-", label=r"coordinates outside $S$"),
    ]
    ax_b.legend(handles=legend_handles, loc="upper center", bbox_to_anchor=(0.53, -0.23),
                ncol=2, frameon=False, fontsize=5.2, handlelength=2.1,
                columnspacing=1.2)

    # Panel C: exact values, direct labels, marker and line-style redundancy.
    panel_title(ax_c, "C", "Exact functional values at N=2, M=5, H=1")
    apply_axes_style(ax_c)
    scope_badge(ax_c)
    category_labels = {
        "H_hyb": r"$\mathfrak{H}^{\rm hyb}$",
        "H_fix": r"$\mathfrak{H}^{\rm fix}$",
        "L_K": r"$\mathfrak{L}^K$",
        "O_F_plus": r"$\mathfrak{O}^{F,+}$",
        "M_K": r"$\mathfrak{M}^K$",
        "H1_F": r"$\mathfrak{H}^F_1$",
    }
    styles = {
        "H_hyb": (PALETTE["gray"], "x", (0, (1, 2))),
        "H_fix": (PALETTE["navy"], "s", "-"),
        "L_K": (PALETTE["navy"], "o", (0, (4, 2))),
        "O_F_plus": (PALETTE["orange"], "^", "-"),
        "M_K": (PALETTE["orange"], "D", (0, (4, 2))),
        "H1_F": (PALETTE["charcoal"], "*", "-"),
    }
    values = arrays["exactValues"]
    y_positions = np.arange(len(values))[::-1]
    for y_pos, (key, value) in zip(y_positions, values, strict=True):
        color, marker, linestyle = styles[key]
        ax_c.plot([0.0, value], [y_pos, y_pos], color=color, linewidth=1.15,
                  linestyle=linestyle, zorder=2)
        ax_c.plot(value, y_pos, marker=marker, markersize=5.2, color=color,
                  markerfacecolor=PALETTE["paper"] if marker not in ("*", "x") else color,
                  markeredgewidth=0.9, zorder=3)
        ax_c.text(value + 0.14, y_pos, f"{value:g}", ha="left", va="center",
                  fontsize=6.2, color=PALETTE["charcoal"], fontweight="bold")
    ax_c.set_yticks(y_positions, [category_labels[key] for key, _ in values])
    ax_c.set_xlim(-0.05, 6.75)
    ax_c.set_ylim(-0.55, len(values) - 0.20)
    ax_c.set_xticks([0, 1, 2, 3, 4, 5, 6])
    ax_c.set_xlabel("exact value", fontsize=6.5, labelpad=2)
    ax_c.grid(axis="x", color=PALETTE["light_gray"], linewidth=0.55)
    ax_c.grid(axis="y", visible=False)
    ax_c.text(0.98, 0.08,
              r"$0=\mathfrak{H}^{\rm hyb}<\mathfrak{H}^{\rm fix}=\mathfrak{L}^K$"
              "\n" + r"$<\mathfrak{O}^{F,+}=\mathfrak{M}^K$",
              transform=ax_c.transAxes, ha="right", va="bottom", fontsize=5.25,
              color=PALETTE["charcoal"],
              bbox={"boxstyle": "round,pad=0.28", "facecolor": PALETTE["xlight_gray"],
                    "edgecolor": PALETTE["light_gray"], "linewidth": 0.55})

    # Panel D: exact fixed-N ledger obstruction.
    panel_title(ax_d, "D", "Fixed-budget ledger-normalized height")
    apply_axes_style(ax_d)
    scope_badge(ax_d)
    ax_d.loglog(arrays["heights"], arrays["ratios"], color=PALETTE["navy"],
                linewidth=1.35, linestyle="-", zorder=3,
                label=r"$H^{1/3}/(2M)^{2/3}$")
    ax_d.loglog(arrays["checkpointHeights"], arrays["checkpointRatios"], linestyle="none",
                marker="o", markersize=4.0, markerfacecolor=PALETTE["paper"],
                markeredgecolor=PALETTE["orange"], markeredgewidth=1.0, zorder=4,
                label="exact checkpoints")
    ax_d.set_xlim(float(config["panelD"]["heightMinimum"]),
                  float(config["panelD"]["heightMaximum"]))
    ax_d.set_ylim(0.18, 360.0)
    ax_d.set_xticks([1.0, 1.0e3, 1.0e6, 1.0e9],
                    [r"$1$", r"$10^3$", r"$10^6$", r"$10^9$"])
    ax_d.set_yticks([0.25, 1.0, 4.0, 16.0, 64.0, 256.0],
                    ["1/4", "1", "4", "16", "64", "256"])
    ax_d.set_xlabel(r"clock height $H$ (log scale)", fontsize=6.5, labelpad=2)
    ax_d.set_ylabel(r"$\mathfrak{H}^{\rm fix}/\mathcal{P}^{2/3}$ (log scale)",
                    fontsize=6.5, labelpad=3)
    ax_d.text(0.035, 0.80,
              r"fixed $N=2$, $M=N+2=4$" + "\n" +
              r"$\mathcal{P}=2MH$; exact slope $=1/3$",
              transform=ax_d.transAxes, ha="left", va="top", fontsize=5.35,
              color=PALETTE["charcoal"],
              bbox={"boxstyle": "round,pad=0.25", "facecolor": PALETTE["paper"],
                    "edgecolor": PALETTE["light_gray"], "linewidth": 0.55})
    ax_d.annotate(r"$H\to\infty$: ratio diverges",
                  xy=(1.0e8, (1.0e8 ** (1.0 / 3.0)) / 4.0),
                  xytext=(2.0e5, 95.0), fontsize=5.3, color=PALETTE["orange_dark"],
                  arrowprops={"arrowstyle": "->", "color": PALETTE["orange"],
                              "linewidth": 0.75})
    ax_d.legend(loc="lower right", frameon=False, fontsize=5.25, handlelength=2.3)

    fig.text(0.045, 0.025,
             "Source: R0.74S Step 18, (S.477)–(S.492)  |  exact abstract clocks; constants shown literally",
             ha="left", va="bottom", fontsize=5.25, color=PALETTE["gray"])
    fig.text(0.975, 0.025, "NOT CLAY / open targets remain open",
             ha="right", va="bottom", fontsize=5.25, color=PALETTE["orange_dark"],
             fontweight="bold")

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    canvas_box = fig.bbox
    overflow: list[dict[str, float | str]] = []
    from matplotlib.text import Text
    for artist in fig.findobj(match=lambda item: isinstance(item, Text)):
        if not artist.get_visible() or not artist.get_text():
            continue
        box = artist.get_window_extent(renderer=renderer)
        if box.x0 < canvas_box.x0 - 2.0 or box.y0 < canvas_box.y0 - 2.0 \
                or box.x1 > canvas_box.x1 + 2.0 or box.y1 > canvas_box.y1 + 2.0:
            overflow.append({"text": artist.get_text(), "x0": float(box.x0),
                             "y0": float(box.y0), "x1": float(box.x1), "y1": float(box.y1)})
    return fig, {"artistBoundsPass": not overflow, "textOverflow": overflow}


def render_outputs(config: dict[str, Any], rows: list[dict[str, str]],
                   arrays: dict[str, Any], audit: dict[str, Any], runtime: dict[str, str],
                   source_blobs: dict[str, bytes], repository: Path) -> None:
    started = time.perf_counter()
    cpu_started = time.process_time()
    progress_rows: list[dict[str, object]] = []

    def progress(event: str) -> None:
        record = {
            "elapsedSeconds": time.perf_counter() - started,
            "event": event,
            "pid": os.getpid(),
            "utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds"),
        }
        progress_rows.append(record)
        print(f"[{record['elapsedSeconds']:.3f}s] {event}", flush=True)

    progress("render-start")
    with tempfile.TemporaryDirectory(prefix="r074s-fixed-figure-render-") as temporary:
        stage = Path(temporary)
        mpl_directory = stage / "mplconfig"
        mpl_directory.mkdir()
        os.environ["MPLCONFIGDIR"] = str(mpl_directory)
        os.environ["SOURCE_DATE_EPOCH"] = "0"
        os.environ["TZ"] = "UTC"

        import numpy as np
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib import lines, patches
        from PIL import Image, ImageOps
        import pypdfium2 as pdfium

        progress("runtime-loaded")
        write_csv(stage / "source-data.csv", rows)
        progress("source-data-written")
        fig, render_audit = render_figure(config, arrays, np, plt, patches, lines)
        need(render_audit["artistBoundsPass"], "rendered text exceeds canvas: " + repr(render_audit["textOverflow"]))
        progress("figure-composed")

        width_mm = float(config["widthMillimetres"])
        height_mm = float(config["heightMillimetres"])
        png_dpi = int(config["pngDpi"])
        qa_dpi = int(config["qaDpi"])
        figure_metadata = {
            "Creator": "R0.74S deterministic figure renderer",
            "Title": "Fixed-deletion functionals and the temporal quantifier gap",
            "Subject": "Abstract clock test; not PDE data; not a Clay claim",
        }
        fig.savefig(stage / "figure.png", dpi=png_dpi,
                    metadata={"Software": "R0.74S deterministic figure renderer"})
        fig.savefig(stage / "figure.pdf", metadata={**figure_metadata, "CreationDate": None, "ModDate": None})
        fig.savefig(stage / "figure.svg", metadata={
            "Creator": figure_metadata["Creator"], "Title": figure_metadata["Title"],
            "Description": figure_metadata["Subject"], "Date": None,
        })
        plt.close(fig)
        progress("master-exports-written")

        master_expected = (int(width_mm / 25.4 * png_dpi), int(height_mm / 25.4 * png_dpi))
        qa_expected = (int(width_mm / 25.4 * qa_dpi), int(height_mm / 25.4 * qa_dpi))
        with Image.open(stage / "figure.png") as opened:
            master = opened.convert("RGB")
        need(master.size == master_expected, f"master PNG size drift: {master.size} != {master_expected}")
        final_size = master.resize(qa_expected, Image.Resampling.LANCZOS)
        final_size.save(stage / "qa-final-size.png", dpi=(qa_dpi, qa_dpi),
                        optimize=False, compress_level=6)
        ImageOps.grayscale(final_size).convert("RGB").save(
            stage / "qa-grayscale.png", dpi=(qa_dpi, qa_dpi), optimize=False, compress_level=6,
        )
        progress("png-qa-assets-written")

        document = pdfium.PdfDocument(str(stage / "figure.pdf"))
        page = document[0]
        width_points, _ = page.get_size()
        pdf_image = page.render(scale=qa_expected[0] / float(width_points)).to_pil().convert("RGB")
        page.close()
        document.close()
        if pdf_image.size != qa_expected:
            pdf_image = pdf_image.resize(qa_expected, Image.Resampling.LANCZOS)
        pdf_image.save(stage / "qa-pdf.png", dpi=(qa_dpi, qa_dpi), optimize=False, compress_level=6)
        progress("pdf-qa-asset-written")

        results = {
            "data": {
                "csvRowCount": len(rows),
                "panelARowCount": sum(row["panel"] == "A" for row in rows),
                "panelBRowCount": sum(row["panel"] == "B" for row in rows),
                "panelCRowCount": sum(row["panel"] == "C" for row in rows),
                "panelDRowCount": sum(row["panel"] == "D" for row in rows),
            },
            "formulaAudit": audit,
            "notClay": True,
            "render": render_audit,
            "schema": "r074s-fixed-deletion-quantifier-gap-results-v1",
            "sourceBinding": {
                "commit": config["sourceBinding"]["commit"],
                "fileCount": len(source_blobs),
            },
            "status": "PASS" if audit["checksPassed"] and render_audit["artistBoundsPass"] else "FAIL",
        }
        (stage / "results.json").write_text(canonical(results), encoding="utf-8", newline="\n")
        progress("results-written")

        environment = {
            "createdAtUtc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds"),
            "logicalCpuCount": os.cpu_count(),
            "machine": platform.machine(),
            "matplotlibConfigPolicy": "system temporary directory removed after render",
            "memoryBytes": int(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")),
            "operatingSystem": platform.platform(),
            "packages": runtime,
            "python": runtime["python"],
            "repositoryHead": git_text(repository, ["rev-parse", "HEAD"]),
            "schema": "r074s-figure-environment-v1",
        }
        (stage / "environment.json").write_text(canonical(environment), encoding="utf-8", newline="\n")
        progress("environment-recorded")

        resource_row = {
            "cpuSeconds": time.process_time() - cpu_started,
            "maximumResidentSetSizeRaw": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "pid": os.getpid(),
            "schema": "r074s-figure-resource-v1",
            "utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds"),
            "wallSeconds": time.perf_counter() - started,
        }
        (stage / "resource-log.ndjson").write_text(canonical(resource_row).replace("\n", " ").strip() + "\n",
                                                    encoding="utf-8", newline="\n")
        progress("render-complete")
        (stage / "progress.ndjson").write_text(
            "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in progress_rows),
            encoding="utf-8", newline="\n",
        )

        for name in RAW_FILES:
            need((stage / name).is_file(), "staged raw/result missing: " + name)
            os.replace(stage / name, HERE / name)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deps", required=True, type=Path)
    parser.add_argument("--repository", type=Path, default=REPOSITORY_DEFAULT)
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    need(args.render, "--render is required")
    insert_dependencies(args.deps)
    preflight_archive()
    config = load_json(HERE / "config.json")
    repository = args.repository.expanduser().resolve()
    runtime = live_runtime_versions(config)
    source_blobs = verify_source_binding(repository, config)
    import numpy as np
    rows, arrays, audit = generate_payload(config, np)
    need(audit["checksPassed"], "formula audit failed")
    render_outputs(config, rows, arrays, audit, runtime, source_blobs, repository)


if __name__ == "__main__":
    main()
