#!/usr/bin/env python3
"""Render the source-bound R0.74U intrinsic certified-residence figure."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
from fractions import Fraction
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
FORMULA_SOURCE = "core d74e7b29, equations (U.11)-(U.45)"
FROZEN_NOTE_PATH = "research/r074u_intrinsic_certified_residence.md"
FROZEN_NOTE_SHA256 = "e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99"
FROZEN_NOTE_COMMIT = "d74e7b297928147334136f4c3cb29c5226d66381"
FROZEN_NOTE_BLOB = "3359036a04afd87eb51123d9b9d9a321a5bfc898"
PALETTE = {
    "navy": "#244C70", "navy_dark": "#18364F", "navy_open": "#DCE8F0",
    "orange": "#B45A36", "orange_dark": "#7E3E27", "orange_open": "#F3E2D8",
    "charcoal": "#283238", "gray": "#737E85", "mid_gray": "#AAB2B8",
    "light_gray": "#DDE1E4", "xlight_gray": "#F2F4F5", "paper": "#FFFFFF",
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
        ["git", "-C", str(repository), *args], stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    need(result.returncode == 0,
         "git failed: " + result.stderr.decode("utf-8", "replace").strip())
    return result.stdout


def git_text(repository: Path, args: list[str]) -> str:
    return git_bytes(repository, args).decode("utf-8").strip()


def verify_source_binding(repository: Path, config: dict[str, Any]) -> dict[str, bytes]:
    source = config["sourceBinding"]
    need(source == {
        "byteCount": 19956,
        "commit": FROZEN_NOTE_COMMIT,
        "formulaLocator": FROZEN_NOTE_PATH + ", equations (U.11)-(U.45)",
        "gitBlobObjectId": FROZEN_NOTE_BLOB,
        "mode": "frozen-git-core",
        "path": FROZEN_NOTE_PATH,
        "sha256": FROZEN_NOTE_SHA256,
    }, "frozen source-binding configuration drift")
    git_text(repository, ["cat-file", "-e", FROZEN_NOTE_COMMIT + "^{commit}"])
    ancestor = subprocess.run(
        ["git", "-C", str(repository), "merge-base", "--is-ancestor", FROZEN_NOTE_COMMIT, "HEAD"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(ancestor.returncode == 0, "frozen mathematical core is not an ancestor of HEAD")
    payload = git_bytes(repository, ["cat-file", "blob", FROZEN_NOTE_COMMIT + ":" + FROZEN_NOTE_PATH])
    actual_blob = git_text(repository, ["rev-parse", FROZEN_NOTE_COMMIT + ":" + FROZEN_NOTE_PATH])
    need(actual_blob == FROZEN_NOTE_BLOB, "frozen theorem-note Git blob drift")
    need(len(payload) == source["byteCount"], "frozen theorem-note byte-count drift")
    need(sha256_bytes(payload) == FROZEN_NOTE_SHA256, "frozen theorem-note SHA-256 drift")
    live_path = repository / FROZEN_NOTE_PATH
    need(live_path.is_file() and not live_path.is_symlink(), "live theorem note missing or symlinked")
    need(live_path.read_bytes() == payload, "live theorem note differs from frozen Git blob")
    note = payload.decode("utf-8")
    for locator in ("\\tag{U.11}", "\\tag{U.23}", "\\tag{U.24}", "\\tag{U.35}",
                    "\\tag{U.36}", "\\tag{U.39}", "\\tag{U.40}", "\\tag{U.45}",
                    "R074U_STEP20_STATUS_K_SUPERLEVEL_LOWER_ONLY", "**NOT CLAY.**"):
        need(locator in note, "frozen theorem-note locator drift: " + locator)
    return {FROZEN_NOTE_PATH: payload}


def insert_dependencies(path: Path) -> None:
    resolved = path.expanduser().resolve()
    need(resolved.is_dir(), "--deps is not a directory")
    sys.path.insert(0, str(resolved))


def live_runtime_versions(config: dict[str, Any]) -> dict[str, str]:
    actual = {
        "python": platform.python_version(), "numpy": importlib.metadata.version("numpy"),
        "matplotlib": importlib.metadata.version("matplotlib"),
        "pillow": importlib.metadata.version("pillow"), "pypdf": importlib.metadata.version("pypdf"),
        "pypdfium2": importlib.metadata.version("pypdfium2"),
    }
    need(actual == config["runtime"], f"runtime drift: expected {config['runtime']}, got {actual}")
    return actual


def preflight_archive() -> None:
    actual = {path.name for path in HERE.iterdir()}
    allowed = set(SOURCE_FILES + RAW_FILES + METADATA_FILES)
    need(set(SOURCE_FILES).issubset(actual), "source inventory is incomplete")
    need(actual.issubset(allowed), "unexpected package entry: " + repr(sorted(actual - allowed)))
    need(all((HERE / name).is_file() and not (HERE / name).is_symlink() for name in SOURCE_FILES),
         "source file or symlink drift")


def number(value: float) -> str:
    value = float(value)
    if value == 0.0:
        return "0"
    return format(value, ".17g")


def annular_margin(l_value: float) -> float:
    lam = 63.0 / 32.0
    c_h = 15.0 / 16.0
    b_2 = 3.0 / 2.0
    return math.sqrt((2.0 / lam) ** 2 - 1.0 / 256.0 - (c_h + 1.0 / l_value) ** 2) - b_2 / l_value


def generate_payload(config: dict[str, Any], np: Any) -> tuple[list[dict[str, str]], dict[str, Any], dict[str, Any]]:
    rows: list[dict[str, str]] = []

    def row(panel: str, record: str, series: str, x: float, y: float, x_unit: str,
            y_unit: str, evidence: str, method: str) -> None:
        rows.append({
            "panel": panel, "record": record, "series": series,
            "x": number(x), "y": number(y), "x_unit": x_unit, "y_unit": y_unit,
            "evidence_class": evidence, "formula_source": FORMULA_SOURCE, "method": method,
        })

    panel_a = config["panelA"]
    l_min = int(panel_a["illustrativeL"])
    a_min = annular_margin(float(l_min))
    row("A", "centre-left", "symmetric_Q_corridor", -1.0, -a_min,
        "normalized_endpoint", "Q_over_r", "derived-analytic-value", "equations-U.14-U.20; L=9216")
    row("A", "centre-zero", "symmetric_Q_corridor", 0.0, 0.0,
        "normalized_endpoint", "Q_over_r", "exact-analytic-schematic", "Q_i(tau_i)=0")
    row("A", "centre-right", "symmetric_Q_corridor", 1.0, a_min,
        "normalized_endpoint", "Q_over_r", "derived-analytic-value", "equations-U.14-U.20; L=9216")
    row("A", "slab-start", "terminal_slab", 64.0, 0.0,
        "t_over_R_squared", "set_boundary", "exact-analytic-schematic", "equation-U.5")
    row("A", "slab-end", "terminal_slab", 65.0, 0.0,
        "t_over_R_squared", "set_boundary", "exact-analytic-schematic", "equation-U.5")
    row("A", "uniform-one-side-allowance", "slab_truncation_lower", 0.0, 72.0 / 5.0,
        "constant_index", "coefficient_of_LR3", "exact-rational", "equations-U.22-U.23")

    exponent_ledger = (
        ("speed-R", "speed_Q_prime", 0.0, -2.0, "Q_i' has R exponent -2"),
        ("inverse-speed-R", "reciprocal_speed", 1.0, 2.0, "1/Q_i' has R exponent 2"),
        ("room-L", "horizontal_room", 2.0, 1.0, "A(L_i)L_iR has L_i exponent 1"),
        ("room-R", "horizontal_room", 3.0, 1.0, "A(L_i)L_iR has R exponent 1"),
        ("residence-L", "residence_scale", 4.0, 1.0, "room times reciprocal speed") ,
        ("residence-R", "residence_scale", 5.0, 3.0, "room times reciprocal speed"),
    )
    for record, series, x_value, y_value, method in exponent_ledger:
        row("B", record, series, x_value, y_value, "ledger_index", "monomial_exponent",
            "exact-algebra", method)

    lower_fraction = Fraction(int(config["panelC"]["corridorLower"]["numerator"]),
                              int(config["panelC"]["corridorLower"]["denominator"]))
    upper_fraction = Fraction(int(config["panelC"]["corridorStrictUpper"]["numerator"]),
                              int(config["panelC"]["corridorStrictUpper"]["denominator"]))
    panel_c_rows = (
        ("geometry-lower", "certified_geometric_corridor", 0.0, float(lower_fraction),
         "equation-U.23; non-strict lower"),
        ("geometry-upper", "certified_geometric_corridor", 1.0, float(upper_fraction),
         "equation-U.24; strict upper"),
        ("inclusion", "corridor_subset_K_superlevel", 2.0, 1.0, "equation-U.35; proved inclusion"),
        ("K-lower", "full_K_superlevel", 3.0, float(lower_fraction),
         "equation-U.35; lower measure only"),
        ("K-converse", "full_K_superlevel", 4.0, 0.0, "converse inclusion not proved"),
        ("K-upper", "full_K_superlevel", 5.0, 0.0, "upper residence bound not proved"),
    )
    for record, series, x_value, y_value, method in panel_c_rows:
        row("C", record, series, x_value, y_value, "claim_index", "coefficient_or_truth_flag",
            "exact-analytic-claim-boundary", method)

    panel_d = config["panelD"]
    c_gamma = Fraction(int(panel_d["cGamma"]["numerator"]),
                       int(panel_d["cGamma"]["denominator"]))
    a_s = Fraction(int(panel_d["aS"]["numerator"]), int(panel_d["aS"]["denominator"]))
    exponential_margin_fraction = 5 * c_gamma - a_s
    exponential_margin = float(exponential_margin_fraction)
    l1_values = np.linspace(float(panel_d["l1Minimum"]), float(panel_d["l1Maximum"]),
                            int(panel_d["points"]))
    l2_values = float(panel_d["l2OverL1"]) * l1_values
    d_l = np.log(l1_values)
    log_lower = math.log(float(lower_fraction)) + np.log(l2_values)
    log_upper = (math.log(float(panel_d["dwellConstantC"])) + 0.5 * np.log(l2_values)
                 - exponential_margin * l1_values ** 2 - d_l)
    log_gap = log_lower - log_upper
    conversion = math.log(10.0)
    log10_lower = log_lower / conversion
    log10_upper = log_upper / conversion
    log10_gap = log_gap / conversion
    for index, l1 in enumerate(l1_values):
        row("D", f"certified-lower-{index:03d}", "log10_theta_cert_lower", l1,
            log10_lower[index], "L_1", "log10_normalized_dwell", "derived-analytic-value",
            "equation-U.36; theta_cert,2 >= (72/5)L_2; L_2=2L_1")
        row("D", f"necessary-upper-{index:03d}", "log10_theta_necessary_upper_C_equals_1", l1,
            log10_upper[index], "L_1", "log10_normalized_dwell", "derived-analytic-value",
            "equation-U.40; d_L=log(L_1); C=1")
        row("D", f"log-gap-{index:03d}", "log10_lower_over_upper", l1,
            log10_gap[index], "L_1", "log10_ratio", "derived-analytic-value",
            "equations-U.36-U.41; exact logarithmic difference")

    margin_square = Fraction(15232043, 1849688064)
    inner_margin = Fraction(9235, 21504)
    a_d_l2 = Fraction(49, 14625) * l_min * l_min
    identity_residual = float(np.max(np.abs(log_gap - (log_lower - log_upper))))
    exponents = {
        "speedR": -2.0, "inverseSpeedR": 2.0, "roomL": 1.0,
        "roomR": 1.0, "residenceL": 1.0, "residenceR": 3.0,
    }
    audit = {
        "annularMarginAtLMinimum": a_min,
        "annularMarginExactTests": {
            "innerDenominator": inner_margin.denominator,
            "innerNumerator": inner_margin.numerator,
            "squareDenominator": margin_square.denominator,
            "squareNumerator": margin_square.numerator,
        },
        "checksPassed": bool(
            margin_square > 0 and inner_margin > 0 and 3.0 / 8.0 < a_min < 1.0
            and a_d_l2 == Fraction(462422016, 1625) and a_d_l2 > 4
            and lower_fraction == Fraction(72, 5) and upper_fraction == Fraction(1024, 3)
            and exponents == {"speedR": -2.0, "inverseSpeedR": 2.0, "roomL": 1.0,
                              "roomR": 1.0, "residenceL": 1.0, "residenceR": 3.0}
            and exponential_margin_fraction == Fraction(603445, 89413632)
            and exponential_margin_fraction > 0
            and np.all(log_lower > log_upper) and np.all(np.diff(log_lower) > 0.0)
            and np.all(np.diff(log_upper) < 0.0) and np.all(np.diff(log_gap) > 0.0)
            and identity_residual == 0.0
        ),
        "corridorCoefficients": {
            "lower": {"numerator": lower_fraction.numerator, "denominator": lower_fraction.denominator},
            "strictUpper": {"numerator": upper_fraction.numerator, "denominator": upper_fraction.denominator},
        },
        "dLPath": "log(L1)",
        "exponentLedger": exponents,
        "exponentialMargin": {
            "decimal": exponential_margin, "denominator": exponential_margin_fraction.denominator,
            "numerator": exponential_margin_fraction.numerator,
        },
        "fullKSuperlevel": {"converseProved": False, "lowerOnly": True, "upperBoundProved": False},
        "log10CertifiedLowerEndpoints": [float(log10_lower[0]), float(log10_lower[-1])],
        "log10ConflictGapEndpoints": [float(log10_gap[0]), float(log10_gap[-1])],
        "log10NecessaryUpperEndpoints": [float(log10_upper[0]), float(log10_upper[-1])],
        "logGapIdentityMaximumResidual": identity_residual,
        "panelPointCount": int(panel_d["points"]),
        "platformExponentAtLMinimum": {
            "denominator": a_d_l2.denominator, "numerator": a_d_l2.numerator,
        },
        "sourceNoteSha256": FROZEN_NOTE_SHA256,
        "tolerances": {"logGapIdentity": 0.0},
    }
    arrays = {
        "l1": l1_values, "log10Lower": log10_lower,
        "log10Upper": log10_upper, "log10Gap": log10_gap,
    }
    return rows, arrays, audit


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def apply_axes_style(ax: Any) -> None:
    ax.set_facecolor(PALETTE["paper"])
    ax.tick_params(axis="both", colors=PALETTE["charcoal"], labelsize=6.0,
                   length=2.5, width=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for name in ("left", "bottom"):
        ax.spines[name].set_color(PALETTE["gray"])
        ax.spines[name].set_linewidth(0.75)
    ax.grid(axis="both", color=PALETTE["light_gray"], linewidth=0.55, alpha=0.9, zorder=0)


def panel_title(ax: Any, letter: str, title: str) -> None:
    ax.set_title(r"$\bf{" + letter + r"}$  " + title, loc="left", fontsize=7.9,
                 color=PALETTE["charcoal"], pad=7.0, fontweight="normal")


def scope_badge(ax: Any, text: str) -> None:
    ax.text(0.985, 0.975, text, transform=ax.transAxes, ha="right", va="top",
            fontsize=4.25, color=PALETTE["orange_dark"], fontweight="bold",
            bbox={"boxstyle": "round,pad=0.22", "facecolor": PALETTE["orange_open"],
                  "edgecolor": PALETTE["orange"], "linewidth": 0.55}, zorder=20)


def draw_blossom(fig: Any, patches: Any) -> None:
    center = (0.958, 0.936)
    radius = 0.0105
    for index, angle in enumerate((90, 18, -54, -126, 162)):
        radians = math.radians(angle)
        color = PALETTE["navy"] if index % 2 == 0 else PALETTE["orange"]
        fig.add_artist(patches.Ellipse(
            (center[0] + 0.014 * math.cos(radians), center[1] + 0.020 * math.sin(radians)),
            width=radius, height=radius * 1.55, angle=angle - 90,
            transform=fig.transFigure, facecolor="none", edgecolor=color,
            linewidth=0.9, zorder=30,
        ))
    fig.add_artist(patches.Circle(center, radius=0.0035, transform=fig.transFigure,
                                  facecolor=PALETTE["charcoal"], edgecolor="none", zorder=31))


def card(ax: Any, patches: Any, x: float, width: float, title: str, formula: str,
         edge: str, fill: str) -> None:
    ax.add_patch(patches.FancyBboxPatch(
        (x, 0.48), width, 0.29, boxstyle="round,pad=0.012,rounding_size=0.018",
        facecolor=fill, edgecolor=edge, linewidth=0.85, transform=ax.transAxes,
    ))
    ax.text(x + width / 2.0, 0.69, title, transform=ax.transAxes, ha="center", va="center",
            fontsize=4.8, color=PALETTE["gray"])
    ax.text(x + width / 2.0, 0.565, formula, transform=ax.transAxes, ha="center", va="center",
            fontsize=7.0, color=PALETTE["charcoal"])


def render_figure(config: dict[str, Any], arrays: dict[str, Any], audit: dict[str, Any],
                  np: Any, plt: Any, patches: Any) -> tuple[Any, dict[str, Any]]:
    width_in = float(config["widthMillimetres"]) / 25.4
    height_in = float(config["heightMillimetres"]) / 25.4
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 7.0,
        "axes.labelcolor": PALETTE["charcoal"], "axes.titlecolor": PALETTE["charcoal"],
        "figure.facecolor": PALETTE["paper"], "savefig.facecolor": PALETTE["paper"],
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
        "svg.hashsalt": "r074u-intrinsic-certified-residence", "axes.unicode_minus": False,
    })
    fig, axes = plt.subplots(2, 2, figsize=(width_in, height_in), dpi=int(config["pngDpi"]))
    fig.subplots_adjust(left=0.075, right=0.975, bottom=0.105, top=0.815,
                        wspace=0.27, hspace=0.49)
    ax_a, ax_b, ax_c, ax_d = axes.ravel()
    fig.text(0.040, 0.955, "Intrinsic certified residence of the canonical common-shear lobe",
             ha="left", va="top", fontsize=11.3, color=PALETTE["charcoal"], fontweight="bold")
    fig.text(0.040, 0.913,
             "R0.74U Step 20 | ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NOT CLAY",
             ha="left", va="top", fontsize=6.25, color=PALETTE["gray"])
    draw_blossom(fig, patches)

    # A: exact symmetry is in Q-space; the time preimage is then slab-truncated.
    panel_title(ax_a, "A", "Symmetric centre corridor and slab truncation")
    ax_a.set_xlim(0.0, 1.0); ax_a.set_ylim(0.0, 1.0); ax_a.axis("off")
    scope_badge(ax_a, "ANALYTIC SCHEMATIC / NOT DNS")
    ax_a.text(0.055, 0.82, r"centre displacement $Q_i(t)/r_i$", transform=ax_a.transAxes,
              ha="left", va="center", fontsize=5.2, color=PALETTE["gray"])
    ax_a.plot([0.08, 0.92], [0.68, 0.68], color=PALETTE["charcoal"], linewidth=0.9,
              transform=ax_a.transAxes)
    ax_a.add_patch(patches.Rectangle((0.26, 0.61), 0.48, 0.14, transform=ax_a.transAxes,
                                     facecolor=PALETTE["navy_open"], edgecolor=PALETTE["navy"],
                                     linewidth=1.0, hatch="///"))
    for x, label in ((0.26, r"$-A(L_i)$"), (0.50, r"$0$"), (0.74, r"$+A(L_i)$")):
        ax_a.plot([x, x], [0.59, 0.77], color=PALETTE["charcoal"], linewidth=0.65,
                  transform=ax_a.transAxes)
        ax_a.text(x, 0.54, label, transform=ax_a.transAxes, ha="center", va="top",
                  fontsize=5.2, color=PALETTE["charcoal"])
    ax_a.text(0.50, 0.69, r"$|Q_i(t)|<A(L_i)r_i$", transform=ax_a.transAxes,
              ha="center", va="center", fontsize=6.0, color=PALETTE["navy_dark"], fontweight="bold")
    ax_a.text(0.50, 0.47, r"$Q_i(\tau_i)=0$; exact symmetry in $Q$", transform=ax_a.transAxes,
              ha="center", va="center", fontsize=5.2, color=PALETTE["navy_dark"])
    ax_a.plot([0.08, 0.92], [0.25, 0.25], color=PALETTE["charcoal"], linewidth=0.9,
              transform=ax_a.transAxes)
    ax_a.add_patch(patches.Rectangle((0.16, 0.19), 0.57, 0.12, transform=ax_a.transAxes,
                                     facecolor=PALETTE["navy_open"], edgecolor=PALETTE["navy"],
                                     linewidth=0.9, linestyle="--"))
    ax_a.add_patch(patches.Rectangle((0.31, 0.14), 0.58, 0.22, transform=ax_a.transAxes,
                                     facecolor="none", edgecolor=PALETTE["gray"], linewidth=0.9,
                                     hatch="...."))
    ax_a.add_patch(patches.Rectangle((0.31, 0.19), 0.42, 0.12, transform=ax_a.transAxes,
                                     facecolor=PALETTE["orange_open"], edgecolor=PALETTE["orange"],
                                     linewidth=1.1, hatch="\\\\"))
    ax_a.text(0.60, 0.38, r"$I_R=(64R^2,65R^2)$", transform=ax_a.transAxes,
              ha="center", va="bottom", fontsize=5.3, color=PALETTE["gray"])
    ax_a.text(0.52, 0.25, r"$\mathcal{R}_i^{\rm cert}=Q_i^{-1}((-Ar_i,Ar_i))\cap I_R$",
              transform=ax_a.transAxes, ha="center", va="center", fontsize=5.5,
              color=PALETTE["orange_dark"])
    ax_a.text(0.50, 0.015, "SCHEMATIC / NOT TO SCALE | slab may truncate one side",
              transform=ax_a.transAxes, ha="center", va="bottom", fontsize=4.85,
              color=PALETTE["orange_dark"], fontweight="bold")

    # B: the exact kinematic exponent product.
    panel_title(ax_b, "B", r"Why the time scale is $L_iR^3$")
    ax_b.set_xlim(0.0, 1.0); ax_b.set_ylim(0.0, 1.0); ax_b.axis("off")
    scope_badge(ax_b, "EXACT ALGEBRA / NOT PDE DATA")
    card(ax_b, patches, 0.035, 0.25, "horizontal room", r"$A(L_i)L_iR$",
         PALETTE["navy"], PALETTE["navy_open"])
    card(ax_b, patches, 0.375, 0.25, "reciprocal speed", r"$R^2$",
         PALETTE["orange"], PALETTE["orange_open"])
    card(ax_b, patches, 0.715, 0.25, "travel time", r"$A(L_i)L_iR^3$",
         PALETTE["charcoal"], PALETTE["xlight_gray"])
    ax_b.text(0.33, 0.62, r"$\times$", transform=ax_b.transAxes, ha="center", va="center",
              fontsize=10.0, color=PALETTE["charcoal"])
    ax_b.text(0.67, 0.62, r"$=$", transform=ax_b.transAxes, ha="center", va="center",
              fontsize=10.0, color=PALETTE["charcoal"])
    ax_b.text(0.50, 0.855, r"$Q_i'(t)\asymp R^{-2}$  so  $(Q_i')^{-1}\asymp R^2$",
              transform=ax_b.transAxes, ha="center", va="center", fontsize=6.1,
              color=PALETTE["charcoal"])
    ax_b.add_patch(patches.FancyBboxPatch(
        (0.06, 0.155), 0.88, 0.20, boxstyle="round,pad=0.018,rounding_size=0.02",
        facecolor=PALETTE["paper"], edgecolor=PALETTE["mid_gray"], linewidth=0.75,
        transform=ax_b.transAxes,
    ))
    ax_b.text(0.50, 0.285,
              r"$\frac{1-\varepsilon_i}{128R^2}\leq Q_i'\leq"
              r"\frac{1}{128(1-\varepsilon_1)R^2}$",
              transform=ax_b.transAxes, ha="center", va="center", fontsize=6.0,
              color=PALETTE["charcoal"])
    ax_b.text(0.50, 0.205,
              r"$128A(L_i)(1-\varepsilon_1)L_iR^3$ per side; total $\leq"
              r"256A(L_i)(1-\varepsilon_i)^{-1}L_iR^3$",
              transform=ax_b.transAxes, ha="center", va="center", fontsize=4.75,
              color=PALETTE["gray"])
    ax_b.text(0.50, 0.045, r"room exponent $(L,R)=(1,1)$ + reciprocal-speed $R^2$"
              r" $\Rightarrow$ residence $(L,R)=(1,3)$",
              transform=ax_b.transAxes, ha="center", va="bottom", fontsize=5.0,
              color=PALETTE["navy_dark"], fontweight="bold")

    # C: strict set/claim boundary.
    panel_title(ax_c, "C", r"Two-sided geometry; lower-only full $K$ residence")
    ax_c.set_xlim(0.0, 1.0); ax_c.set_ylim(0.0, 1.0); ax_c.axis("off")
    scope_badge(ax_c, "ANALYTIC CLAIM BOUNDARY")
    ax_c.add_patch(patches.FancyBboxPatch(
        (0.06, 0.10), 0.88, 0.72, boxstyle="round,pad=0.018,rounding_size=0.028",
        facecolor=PALETTE["xlight_gray"], edgecolor=PALETTE["gray"], linewidth=1.0,
        linestyle=(0, (4, 2)), transform=ax_c.transAxes,
    ))
    ax_c.text(0.50, 0.75, r"full set $\{t\in I_R:K_{k_i,R}(t)\geq c_KT\}$",
              transform=ax_c.transAxes, ha="center", va="center", fontsize=6.1,
              color=PALETTE["charcoal"], fontweight="bold")
    ax_c.add_patch(patches.FancyBboxPatch(
        (0.19, 0.29), 0.55, 0.31, boxstyle="round,pad=0.018,rounding_size=0.025",
        facecolor=PALETTE["navy_open"], edgecolor=PALETTE["navy"], linewidth=1.2,
        hatch="///", transform=ax_c.transAxes,
    ))
    ax_c.text(0.465, 0.515, r"certified geometric corridor $\mathcal{R}_i^{\rm cert}$",
              transform=ax_c.transAxes, ha="center", va="center", fontsize=5.7,
              color=PALETTE["navy_dark"], fontweight="bold")
    ax_c.text(0.465, 0.415,
              r"$\frac{72}{5}L_iR^3\leq|\mathcal{R}_i^{\rm cert}|"
              r"<\frac{1024}{3}L_iR^3$",
              transform=ax_c.transAxes, ha="center", va="center", fontsize=6.2,
              color=PALETTE["navy_dark"])
    ax_c.text(0.465, 0.335, r"two-sided $\Theta(L_iR^3)$", transform=ax_c.transAxes,
              ha="center", va="center", fontsize=5.6, color=PALETTE["navy_dark"])
    ax_c.text(0.79, 0.45, r"$\subset$", transform=ax_c.transAxes, ha="center", va="center",
              fontsize=11.0, color=PALETTE["orange_dark"])
    ax_c.text(0.50, 0.205,
              r"therefore $|\{K\geq c_KT\}\cap I_R|\geq\frac{72}{5}L_iR^3"
              r"=\Omega(L_iR^3)$",
              transform=ax_c.transAxes, ha="center", va="center", fontsize=5.5,
              color=PALETTE["charcoal"])
    ax_c.text(0.50, 0.035, "NO CONVERSE / NO UPPER BOUND FOR FULL K-SUPERLEVEL",
              transform=ax_c.transAxes, ha="center", va="bottom", fontsize=5.0,
              color=PALETTE["orange_dark"], fontweight="bold")

    # D: lower and necessary upper dwell on the same explicit path.
    panel_title(ax_d, "D", "Certified dwell versus necessary short dwell")
    apply_axes_style(ax_d)
    scope_badge(ax_d, "DERIVED ANALYTIC VALUES / C=1")
    x_scaled = arrays["l1"] / 10000.0
    lower_scaled = arrays["log10Lower"] / 100000.0
    upper_scaled = arrays["log10Upper"] / 100000.0
    ax_d.plot(x_scaled, lower_scaled, color=PALETTE["navy"], linewidth=1.5,
              linestyle="-", label="certified lower", zorder=4)
    ax_d.plot(x_scaled, upper_scaled, color=PALETTE["orange"], linewidth=1.45,
              linestyle=(0, (5, 2)), label="necessary upper (C=1)", zorder=3)
    checkpoints = np.array([0, 30, 60, 90, 120])
    ax_d.plot(x_scaled[checkpoints], lower_scaled[checkpoints], linestyle="none", marker="o",
              markersize=3.5, markerfacecolor=PALETTE["paper"], markeredgecolor=PALETTE["navy"],
              markeredgewidth=0.9, zorder=5)
    ax_d.plot(x_scaled[checkpoints], upper_scaled[checkpoints], linestyle="none", marker="s",
              markersize=3.4, markerfacecolor=PALETTE["orange"], markeredgecolor=PALETTE["orange_dark"],
              markeredgewidth=0.7, zorder=5)
    ax_d.axhline(0.0, color=PALETTE["mid_gray"], linewidth=0.65, linestyle=(0, (2, 2)), zorder=1)
    ax_d.set_xlim(0.90, 2.03)
    ax_d.set_ylim(min(upper_scaled) * 1.07, 0.70)
    ax_d.set_xticks([1.0, 1.25, 1.5, 1.75, 2.0])
    ax_d.set_xlabel(r"$L_1/10^4$", fontsize=6.3, labelpad=2)
    ax_d.set_ylabel(r"$\log_{10}(\mathrm{dwell})/10^5$", fontsize=6.0, labelpad=3)
    ax_d.text(0.035, 0.92, r"$\theta_{\rm cert,2}\geq(72/5)L_2$",
              transform=ax_d.transAxes, ha="left", va="top", fontsize=5.2,
              color=PALETTE["navy_dark"], fontweight="bold")
    ax_d.text(0.035, 0.80,
              r"$\theta_{\rm needed}\leq L_2^{1/2}e^{-mL_1^2-d_L}$"
              "\n" + r"$m=603445/89413632>0$; $d_L=\log L_1$",
              transform=ax_d.transAxes, ha="left", va="top", fontsize=4.9,
              color=PALETTE["orange_dark"], linespacing=1.25,
              bbox={"boxstyle": "round,pad=0.22", "facecolor": PALETTE["paper"],
                    "edgecolor": PALETTE["light_gray"], "linewidth": 0.55})
    ax_d.annotate("log gap grows like $mL_1^2$",
                  xy=(x_scaled[-10], upper_scaled[-10]), xytext=(1.20, -5.6),
                  fontsize=5.0, color=PALETTE["charcoal"],
                  arrowprops={"arrowstyle": "->", "color": PALETTE["charcoal"], "linewidth": 0.7})
    ax_d.legend(loc="lower left", frameon=False, fontsize=4.8, handlelength=2.5,
                borderpad=0.2, labelspacing=0.35)

    fig.text(0.040, 0.025,
             "Source: frozen core d74e7b29, R0.74U (U.11)-(U.45) | exact formulas and explicit analytic path",
             ha="left", va="bottom", fontsize=5.05, color=PALETTE["gray"])
    fig.text(0.975, 0.025, "NOT CLAY / maximal full-clock dwell remains open",
             ha="right", va="bottom", fontsize=5.05, color=PALETTE["orange_dark"], fontweight="bold")

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    canvas_box = fig.bbox
    overflow: list[dict[str, float | str]] = []
    from matplotlib.text import Text
    for artist in fig.findobj(match=lambda item: isinstance(item, Text)):
        if not artist.get_visible() or not artist.get_text():
            continue
        box = artist.get_window_extent(renderer=renderer)
        if (box.x0 < canvas_box.x0 - 2.0 or box.y0 < canvas_box.y0 - 2.0
                or box.x1 > canvas_box.x1 + 2.0 or box.y1 > canvas_box.y1 + 2.0):
            overflow.append({"text": artist.get_text(), "x0": float(box.x0), "y0": float(box.y0),
                             "x1": float(box.x1), "y1": float(box.y1)})
    return fig, {"artistBoundsPass": not overflow, "textOverflow": overflow,
                 "renderedAnnularMarginAtLMinimum": audit["annularMarginAtLMinimum"]}


def render_outputs(config: dict[str, Any], rows: list[dict[str, str]], arrays: dict[str, Any],
                   audit: dict[str, Any], runtime: dict[str, str], source_blobs: dict[str, bytes],
                   repository: Path) -> None:
    started = time.perf_counter(); cpu_started = time.process_time()
    progress_rows: list[dict[str, object]] = []

    def progress(event: str) -> None:
        record = {"elapsedSeconds": time.perf_counter() - started, "event": event,
                  "pid": os.getpid(),
                  "utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds")}
        progress_rows.append(record)
        print(f"[{record['elapsedSeconds']:.3f}s] {event}", flush=True)

    progress("render-start")
    with tempfile.TemporaryDirectory(prefix="r074u-residence-figure-render-") as temporary:
        stage = Path(temporary)
        mpl_directory = stage / "mplconfig"; mpl_directory.mkdir()
        os.environ["MPLCONFIGDIR"] = str(mpl_directory)
        os.environ["SOURCE_DATE_EPOCH"] = "0"; os.environ["TZ"] = "UTC"
        import numpy as np
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib import patches
        from PIL import Image, ImageOps
        import pypdfium2 as pdfium

        progress("runtime-loaded")
        write_csv(stage / "source-data.csv", rows); progress("source-data-written")
        fig, render_audit = render_figure(config, arrays, audit, np, plt, patches)
        need(render_audit["artistBoundsPass"],
             "rendered text exceeds canvas: " + repr(render_audit["textOverflow"]))
        progress("figure-composed")

        width_mm = float(config["widthMillimetres"]); height_mm = float(config["heightMillimetres"])
        png_dpi = int(config["pngDpi"]); qa_dpi = int(config["qaDpi"])
        figure_metadata = {
            "Creator": "R0.74U deterministic analytic-figure renderer",
            "Title": "Intrinsic certified residence of the canonical common-shear lobe",
            "Subject": "Analytic schematic and derived analytic values; not PDE data; not DNS; not Clay",
        }
        fig.savefig(stage / "figure.png", dpi=png_dpi,
                    metadata={"Software": "R0.74U deterministic analytic-figure renderer"})
        fig.savefig(stage / "figure.pdf", metadata={**figure_metadata, "CreationDate": None, "ModDate": None})
        fig.savefig(stage / "figure.svg", metadata={
            "Creator": figure_metadata["Creator"], "Title": figure_metadata["Title"],
            "Description": figure_metadata["Subject"], "Date": None,
        })
        plt.close(fig); progress("master-exports-written")

        master_expected = (int(width_mm / 25.4 * png_dpi), int(height_mm / 25.4 * png_dpi))
        qa_expected = (int(width_mm / 25.4 * qa_dpi), int(height_mm / 25.4 * qa_dpi))
        with Image.open(stage / "figure.png") as opened:
            master = opened.convert("RGB")
        need(master.size == master_expected, f"master PNG size drift: {master.size} != {master_expected}")
        final_size = master.resize(qa_expected, Image.Resampling.LANCZOS)
        final_size.save(stage / "qa-final-size.png", dpi=(qa_dpi, qa_dpi), optimize=False, compress_level=6)
        ImageOps.grayscale(final_size).convert("RGB").save(
            stage / "qa-grayscale.png", dpi=(qa_dpi, qa_dpi), optimize=False, compress_level=6)
        progress("png-qa-assets-written")

        document = pdfium.PdfDocument(str(stage / "figure.pdf")); page = document[0]
        width_points, _ = page.get_size()
        pdf_image = page.render(scale=qa_expected[0] / float(width_points)).to_pil().convert("RGB")
        page.close(); document.close()
        if pdf_image.size != qa_expected:
            pdf_image = pdf_image.resize(qa_expected, Image.Resampling.LANCZOS)
        pdf_image.save(stage / "qa-pdf.png", dpi=(qa_dpi, qa_dpi), optimize=False, compress_level=6)
        progress("pdf-qa-asset-written")

        results = {
            "claimBoundary": {
                "certifiedGeometricCorridorTwoSided": True, "fullKSuperlevelLowerOnly": True,
                "fullKSuperlevelUpperBound": False, "notClay": True,
            },
            "data": {
                "csvRowCount": len(rows),
                "panelARowCount": sum(row["panel"] == "A" for row in rows),
                "panelBRowCount": sum(row["panel"] == "B" for row in rows),
                "panelCRowCount": sum(row["panel"] == "C" for row in rows),
                "panelDRowCount": sum(row["panel"] == "D" for row in rows),
            },
            "formulaAudit": audit, "notClay": True, "render": render_audit,
            "schema": "r074u-intrinsic-certified-residence-results-v1",
            "sourceBinding": {
                "commit": config["sourceBinding"]["commit"],
                "fileCount": len(source_blobs),
                "gitBlobObjectId": config["sourceBinding"]["gitBlobObjectId"],
                "sha256": config["sourceBinding"]["sha256"],
            },
            "status": "PASS" if audit["checksPassed"] and render_audit["artistBoundsPass"] else "FAIL",
        }
        (stage / "results.json").write_text(canonical(results), encoding="utf-8", newline="\n")
        progress("results-written")
        environment = {
            "createdAtUtc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds"),
            "dependencyLocatorPolicy": "external version-pinned directory supplied by PYTHONPATH and --deps; absolute path omitted",
            "logicalCpuCount": os.cpu_count(), "machine": platform.machine(),
            "matplotlibConfigPolicy": "system temporary directory removed after render",
            "memoryBytes": int(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")),
            "operatingSystem": platform.platform(), "packages": runtime, "python": runtime["python"],
            "pythonLocatorPolicy": "bundled Python 3.12.13 executable; absolute path omitted",
            "repositoryHead": git_text(repository, ["rev-parse", "HEAD"]),
            "schema": "r074u-figure-environment-v1",
        }
        (stage / "environment.json").write_text(canonical(environment), encoding="utf-8", newline="\n")
        progress("environment-recorded")
        resource_row = {
            "cpuSeconds": time.process_time() - cpu_started,
            "maximumResidentSetSizeRaw": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "pid": os.getpid(), "schema": "r074u-figure-resource-v1",
            "utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds"),
            "wallSeconds": time.perf_counter() - started,
        }
        (stage / "resource-log.ndjson").write_text(
            canonical(resource_row).replace("\n", " ").strip() + "\n", encoding="utf-8", newline="\n")
        progress("render-complete")
        (stage / "progress.ndjson").write_text(
            "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n"
                    for row in progress_rows), encoding="utf-8", newline="\n")
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
    insert_dependencies(args.deps); preflight_archive()
    config = load_json(HERE / "config.json"); repository = args.repository.expanduser().resolve()
    runtime = live_runtime_versions(config); source_blobs = verify_source_binding(repository, config)
    import numpy as np
    rows, arrays, audit = generate_payload(config, np)
    need(audit["checksPassed"], "formula audit failed")
    render_outputs(config, rows, arrays, audit, runtime, source_blobs, repository)


if __name__ == "__main__":
    main()
