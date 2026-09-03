#!/usr/bin/env python3
"""Render the source-bound R0.74T schedule-invariant dwell-barrier figure."""

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
FORMULA_SOURCE = "core b120598d, equations (T.9)-(T.43)"
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
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(result.returncode == 0,
         "git failed: " + result.stderr.decode("utf-8", "replace").strip())
    return result.stdout


def git_text(repository: Path, args: list[str]) -> str:
    return git_bytes(repository, args).decode("utf-8").strip()


def verify_source_binding(repository: Path, config: dict[str, Any]) -> dict[str, bytes]:
    source = config["sourceBinding"]
    commit = source["commit"]
    need(len(commit) == 40 and all(character in "0123456789abcdef" for character in commit),
         "mathematical source commit is not a full lowercase Git hash")
    git_text(repository, ["cat-file", "-e", commit + "^{commit}"])
    ancestor = subprocess.run(
        ["git", "-C", str(repository), "merge-base", "--is-ancestor", commit, "HEAD"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(ancestor.returncode == 0, "frozen mathematical core is not an ancestor of HEAD")

    blobs: dict[str, bytes] = {}
    for relative, lock in source["files"].items():
        payload = git_bytes(repository, ["cat-file", "blob", commit + ":" + relative])
        actual_oid = git_text(repository, ["rev-parse", commit + ":" + relative])
        need(actual_oid == lock["gitBlobObjectId"], "Git blob drift: " + relative)
        need(sha256_bytes(payload) == lock["sha256"], "SHA-256 drift: " + relative)
        blobs[relative] = payload

    note_path = "research/r074t_schedule_invariant_dwell_coercivity.md"
    cert_path = "research/r074t_schedule_invariant_dwell_certificate.json"
    report_path = "research/r074t_schedule_invariant_dwell_certificate_report.md"
    independent_path = "research/r074t_schedule_invariant_dwell_independent_audit.md"
    primary_path = "research/r074t_schedule_invariant_dwell_primary_audit.md"
    literature_path = "research/r074t_schedule_invariant_literature_audit.md"
    qa_path = "research/r074t_schedule_invariant_dwell_qa_report.md"
    certificate = json.loads(blobs[cert_path])
    note = blobs[note_path].decode("utf-8")
    report = blobs[report_path].decode("utf-8")
    independent = blobs[independent_path].decode("utf-8")
    primary = blobs[primary_path].decode("utf-8")
    literature = blobs[literature_path].decode("utf-8")
    qa_report = blobs[qa_path].decode("utf-8")
    need(certificate.get("verdict") == "PASS", "main certificate verdict drift")
    need(certificate.get("note", {}).get("sha256") == source["files"][note_path]["sha256"],
         "certificate-to-note binding drift")
    need("**PASS**" in report and "18933" in report, "certificate report drift")
    need("**PASS**" in independent and "9201" in independent, "independent audit drift")
    need("**Verdict: PASS.**" in primary, "primary audit verdict drift")
    need("finite primary-source non-hit" in literature and "does not prove novelty" in literature,
         "literature boundary drift")
    need("31/31" in qa_report and "26/26" in qa_report, "QA report drift")
    need("\\tag{T.43}" in note and "**NOT CLAY.**" in note,
         "note formula or scope locator drift")
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
    need(all((HERE / name).is_file() and not (HERE / name).is_symlink() for name in SOURCE_FILES),
         "source file or symlink drift")


def number(value: float) -> str:
    value = float(value)
    if value == 0.0:
        return "0"
    return format(value, ".17g")


def generate_payload(config: dict[str, Any], np: Any) -> tuple[list[dict[str, str]], dict[str, Any], dict[str, Any]]:
    rows: list[dict[str, str]] = []

    panel_a = config["panelA"]
    r_fraction = Fraction(int(panel_a["rNumerator"]), int(panel_a["rDenominator"]))
    r_value = float(r_fraction)
    schedule = [
        ("slab-start", "I_R", 64.0, 0.0, "equation-T.34"),
        ("slab-end", "I_R", 65.0, 0.0, "equation-T.34"),
        ("J1-start", "J_1", float(Fraction(64) + r_fraction), 1.0, "equation-T.42"),
        ("J1-end", "J_1", float(Fraction(64) + 2 * r_fraction), 1.0, "equation-T.42"),
        ("J2-start", "J_2", float(Fraction(65) - r_fraction), 2.0, "equation-T.42"),
        ("J2-end", "J_2", 65.0, 2.0, "equation-T.42"),
    ]
    for record, series, x_value, y_value, method in schedule:
        rows.append({
            "panel": "A", "record": record, "series": series,
            "x": number(x_value), "y": number(y_value), "x_unit": "t_over_R_squared",
            "y_unit": "schedule_row", "evidence_class": "exact-analytic-schedule",
            "formula_source": FORMULA_SOURCE, "method": method,
        })

    factor_rows = [
        ("factor-01", "payment_prefactor", 0.0, 0.25, "(2R)^-2"),
        ("factor-02", "volume_inverse_sqrt", 1.0, 4.0, "(L_2 R^3/16)^-1/2"),
        ("factor-03", "kinetic_unnormalization", 2.0, 2.0 ** 1.5, "(2R/Gamma_2)^(3/2)"),
        ("factor-04", "dwell_length", 3.0, 1.0, "theta R^3"),
        ("factor-05", "shell_weight", 4.0, 1.0, "Gamma_2^(1/4)"),
        ("factor-product", "exact_constant", 5.0, 2.0 * math.sqrt(2.0), "2*sqrt(2)"),
    ]
    exponent_rows = [
        ("exponent-theta", "theta", 0.0, 1.0),
        ("exponent-h", "h_2", 1.0, 1.5),
        ("exponent-R", "R", 2.0, 1.0),
        ("exponent-Gamma", "Gamma_2", 3.0, -1.25),
        ("exponent-L", "L_2", 4.0, -0.5),
    ]
    for record, series, x_value, y_value, method in factor_rows:
        rows.append({
            "panel": "B", "record": record, "series": series,
            "x": number(x_value), "y": number(y_value), "x_unit": "factor_index",
            "y_unit": "exact_coefficient", "evidence_class": "exact-algebra",
            "formula_source": FORMULA_SOURCE, "method": method,
        })
    for record, series, x_value, y_value in exponent_rows:
        rows.append({
            "panel": "B", "record": record, "series": series,
            "x": number(x_value), "y": number(y_value), "x_unit": "monomial_index",
            "y_unit": "exact_exponent", "evidence_class": "exact-algebra",
            "formula_source": FORMULA_SOURCE, "method": "equations-T.9-T.13",
        })

    panel_cd = config["panelCD"]
    c_gamma = Fraction(int(panel_cd["cGamma"]["numerator"]),
                       int(panel_cd["cGamma"]["denominator"]))
    a_s = Fraction(int(panel_cd["aS"]["numerator"]),
                   int(panel_cd["aS"]["denominator"]))
    margin_fraction = 5 * c_gamma - a_s
    margin = float(margin_fraction)
    l1_values = np.linspace(float(panel_cd["l1Minimum"]), float(panel_cd["l1Maximum"]),
                            int(panel_cd["points"]))
    d_l = np.log(l1_values)
    l2_values = 2.0 * l1_values
    theta = float(panel_cd["theta"])
    log_lambda = (2.0 / 3.0) * (
        math.log(theta) + margin * l1_values ** 2 + d_l - 0.5 * np.log(l2_values)
    )
    log_theta_ceiling = (
        math.log(float(panel_cd["dwellConstantC"])) + 0.5 * np.log(l2_values)
        - margin * l1_values ** 2 - d_l
    )
    log10_theta_ceiling = log_theta_ceiling / math.log(10.0)

    for index, (l1, value) in enumerate(zip(l1_values, log_lambda, strict=True)):
        rows.append({
            "panel": "C", "record": f"log-lambda-{index:03d}", "series": "log_Lambda_2",
            "x": number(l1), "y": number(value), "x_unit": "L_1",
            "y_unit": "natural_log", "evidence_class": "derived-analytic-value",
            "formula_source": FORMULA_SOURCE, "method": "equation-T.24; d_L=log(L_1); theta=1",
        })
    for index, (l1, value) in enumerate(zip(l1_values, log10_theta_ceiling, strict=True)):
        rows.append({
            "panel": "D", "record": f"dwell-ceiling-{index:03d}", "series": "log10_theta_max_C_equals_1",
            "x": number(l1), "y": number(value), "x_unit": "L_1",
            "y_unit": "log10_normalized_dwell", "evidence_class": "derived-analytic-value",
            "formula_source": FORMULA_SOURCE, "method": "equation-T.28; d_L=log(L_1); C=1",
        })

    j1_start = Fraction(64) + r_fraction
    j1_end = Fraction(64) + 2 * r_fraction
    j2_start = Fraction(65) - r_fraction
    j2_end = Fraction(65)
    atom_product = Fraction(1, 4) * 4 * (2.0 ** 1.5)
    duality_residual = np.max(np.abs(log_lambda + (2.0 / 3.0) * log_theta_ceiling))
    audit = {
        "checksPassed": bool(
            margin_fraction == Fraction(603445, 89413632)
            and margin_fraction > 0
            and j1_end < j2_start
            and j1_start > 64 and j2_end <= 65
            and (j1_end - j1_start) == r_fraction
            and (j2_end - j2_start) == r_fraction
            and int(panel_a["illustrativeL1"]) * 2 * r_fraction == Fraction(1, 64)
            and abs(float(atom_product) - 2.0 * math.sqrt(2.0)) <= 1.0e-15
            and np.all(np.diff(log_lambda) > 0.0)
            and np.all(np.diff(log10_theta_ceiling) < 0.0)
            and float(np.min(log_lambda)) > 0.0
            and float(np.max(log10_theta_ceiling)) < 0.0
            and float(duality_residual) <= 1.0e-9
        ),
        "atomicConstant": float(atom_product),
        "atomicConstantExpected": 2.0 * math.sqrt(2.0),
        "atomicExponents": {"theta": 1.0, "h_2": 1.5, "R": 1.0,
                            "Gamma_2": -1.25, "L_2": -0.5},
        "dLPath": "log(L1)",
        "dwellConstantC": float(panel_cd["dwellConstantC"]),
        "dualIdentityMaximumResidual": float(duality_residual),
        "illustrativeL1": int(panel_a["illustrativeL1"]),
        "illustrativeR": {"numerator": r_fraction.numerator, "denominator": r_fraction.denominator},
        "l2TimesR": {"numerator": 1, "denominator": 64},
        "logLambdaEndpoints": [float(log_lambda[0]), float(log_lambda[-1])],
        "log10DwellCeilingEndpoints": [float(log10_theta_ceiling[0]), float(log10_theta_ceiling[-1])],
        "margin": {
            "decimal": margin,
            "denominator": margin_fraction.denominator,
            "numerator": margin_fraction.numerator,
        },
        "panelPointCount": int(panel_cd["points"]),
        "schedule": {
            "gapOverR3": int(1 / r_fraction - 3),
            "j1LengthOverR3": 1,
            "j2LengthOverR3": 1,
            "strictlyDisjoint": bool(j1_end < j2_start),
            "withinTerminalSlab": bool(j1_start > 64 and j2_end <= 65),
        },
        "theta": theta,
        "tolerances": {"atomicConstant": 1.0e-15, "dualIdentity": 1.0e-9},
    }
    arrays = {
        "l1": l1_values,
        "logLambda": log_lambda,
        "log10ThetaCeiling": log10_theta_ceiling,
        "r": r_value,
    }
    return rows, arrays, audit


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def apply_axes_style(ax: Any) -> None:
    ax.set_facecolor(PALETTE["paper"])
    ax.tick_params(axis="both", colors=PALETTE["charcoal"], labelsize=6.2,
                   length=2.5, width=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for name in ("left", "bottom"):
        ax.spines[name].set_color(PALETTE["gray"])
        ax.spines[name].set_linewidth(0.75)
    ax.grid(axis="both", color=PALETTE["light_gray"], linewidth=0.55, alpha=0.9, zorder=0)


def panel_title(ax: Any, letter: str, title: str) -> None:
    ax.set_title(r"$\bf{" + letter + r"}$  " + title, loc="left", fontsize=8.0,
                 color=PALETTE["charcoal"], pad=7.0, fontweight="normal")


def scope_badge(ax: Any, text: str) -> None:
    ax.text(0.985, 0.975, text, transform=ax.transAxes, ha="right", va="top",
            fontsize=4.45, color=PALETTE["orange_dark"], fontweight="bold",
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


def factor_card(ax: Any, patches: Any, x: float, title: str, formula: str,
                edge: str, fill: str) -> None:
    ax.add_patch(patches.FancyBboxPatch(
        (x, 0.61), 0.172, 0.25, boxstyle="round,pad=0.012,rounding_size=0.018",
        facecolor=fill, edgecolor=edge, linewidth=0.8, transform=ax.transAxes,
    ))
    ax.text(x + 0.086, 0.79, title, transform=ax.transAxes, ha="center", va="center",
            fontsize=4.65, color=PALETTE["gray"])
    ax.text(x + 0.086, 0.68, formula, transform=ax.transAxes, ha="center", va="center",
            fontsize=6.1, color=PALETTE["charcoal"])


def render_figure(config: dict[str, Any], arrays: dict[str, Any], audit: dict[str, Any],
                  np: Any, plt: Any, patches: Any) -> tuple[Any, dict[str, Any]]:
    width_in = float(config["widthMillimetres"]) / 25.4
    height_in = float(config["heightMillimetres"]) / 25.4
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 7.0,
        "axes.labelcolor": PALETTE["charcoal"], "axes.titlecolor": PALETTE["charcoal"],
        "figure.facecolor": PALETTE["paper"], "savefig.facecolor": PALETTE["paper"],
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
        "svg.hashsalt": "r074t-schedule-invariant-dwell-barrier",
        "axes.unicode_minus": False,
    })
    fig, axes = plt.subplots(2, 2, figsize=(width_in, height_in), dpi=int(config["pngDpi"]))
    fig.subplots_adjust(left=0.085, right=0.975, bottom=0.108, top=0.815,
                        wspace=0.30, hspace=0.49)
    ax_a, ax_b, ax_c, ax_d = axes.ravel()

    fig.text(0.045, 0.955, "Schedule-invariant lobe coercivity and the dwell barrier",
             ha="left", va="top", fontsize=11.8, color=PALETTE["charcoal"], fontweight="bold")
    fig.text(0.045, 0.913,
             "R0.74T Step 19  |  ANALYTIC SCHEMATIC · DERIVED ANALYTIC VALUES · NOT PDE DATA · NOT DNS · NOT CLAY",
             ha="left", va="top", fontsize=6.55, color=PALETTE["gray"])
    draw_blossom(fig, patches)

    # A: exact schedule topology, with the asymptotically enormous gap compressed.
    panel_title(ax_a, "A", "Two disjoint lobe windows in one terminal slab")
    ax_a.set_xlim(0.0, 1.0)
    ax_a.set_ylim(0.0, 1.0)
    ax_a.axis("off")
    scope_badge(ax_a, "ANALYTIC SCHEDULE / NOT DNS")
    ax_a.plot([0.055, 0.945], [0.39, 0.39], color=PALETTE["charcoal"], linewidth=1.0,
              transform=ax_a.transAxes, clip_on=False)
    ax_a.text(0.055, 0.29, r"$64R^2$", transform=ax_a.transAxes, ha="center", va="top",
              fontsize=5.7, color=PALETTE["charcoal"])
    ax_a.text(0.945, 0.29, r"$65R^2$", transform=ax_a.transAxes, ha="center", va="top",
              fontsize=5.7, color=PALETTE["charcoal"])
    ax_a.text(0.50, 0.17, r"$I_R=(64R^2,65R^2)$", transform=ax_a.transAxes,
              ha="center", va="center", fontsize=6.2, color=PALETTE["gray"])
    ax_a.add_patch(patches.Rectangle((0.105, 0.34), 0.185, 0.22, transform=ax_a.transAxes,
                                     facecolor=PALETTE["navy_open"], edgecolor=PALETTE["navy"],
                                     linewidth=1.0, hatch="///"))
    ax_a.add_patch(patches.Rectangle((0.710, 0.34), 0.185, 0.22, transform=ax_a.transAxes,
                                     facecolor=PALETTE["orange_open"], edgecolor=PALETTE["orange"],
                                     linewidth=1.0, hatch="\\\\"))
    ax_a.text(0.1975, 0.63, r"$J_1$", transform=ax_a.transAxes, ha="center", va="bottom",
              fontsize=7.0, color=PALETTE["navy_dark"], fontweight="bold")
    ax_a.text(0.8025, 0.63, r"$J_2$", transform=ax_a.transAxes, ha="center", va="bottom",
              fontsize=7.0, color=PALETTE["orange_dark"], fontweight="bold")
    ax_a.text(0.1975, 0.45, r"$|J_1|=R^3$", transform=ax_a.transAxes, ha="center", va="center",
              fontsize=5.8, color=PALETTE["navy_dark"])
    ax_a.text(0.8025, 0.45, r"$|J_2|=R^3$", transform=ax_a.transAxes, ha="center", va="center",
              fontsize=5.8, color=PALETTE["orange_dark"])
    for offset in (-0.018, 0.018):
        ax_a.plot([0.49 + offset, 0.505 + offset], [0.33, 0.45], color=PALETTE["gray"],
                  linewidth=1.0, transform=ax_a.transAxes, clip_on=False)
    ax_a.annotate("", xy=(0.70, 0.76), xytext=(0.30, 0.76), xycoords=ax_a.transAxes,
                  arrowprops={"arrowstyle": "<->", "color": PALETTE["charcoal"], "linewidth": 0.8})
    ax_a.text(0.50, 0.79, r"exact gap $=R^2-3R^3>0$", transform=ax_a.transAxes,
              ha="center", va="bottom", fontsize=5.7, color=PALETTE["charcoal"])
    ax_a.text(0.50, 0.02,
              "GAP COMPRESSED / NOT TO SCALE\none common-shear solution; no independent time translation",
              transform=ax_a.transAxes, ha="center", va="bottom", fontsize=5.0,
              color=PALETTE["orange_dark"], linespacing=1.3, fontweight="bold")

    # B: atomic exact constant and exponent ledger.
    panel_title(ax_b, "B", "Exact Hölder coefficient and exponent ledger")
    ax_b.set_xlim(0.0, 1.0)
    ax_b.set_ylim(0.0, 1.0)
    ax_b.axis("off")
    scope_badge(ax_b, "EXACT ALGEBRA / NOT PDE DATA")
    factor_card(ax_b, patches, 0.015, "payment", r"$2^{-2}$" + "\n" + r"$R^{-2}$",
                PALETTE["navy"], PALETTE["navy_open"])
    factor_card(ax_b, patches, 0.212, "volume", r"$4L_2^{-1/2}$" + "\n" + r"$R^{-3/2}$",
                PALETTE["navy"], PALETTE["navy_open"])
    factor_card(ax_b, patches, 0.409, "kinetic", r"$2^{3/2}R^{3/2}$" + "\n" + r"$\Gamma_2^{-3/2}$",
                PALETTE["orange"], PALETTE["orange_open"])
    factor_card(ax_b, patches, 0.606, "dwell", r"$\theta R^3$",
                PALETTE["gray"], PALETTE["xlight_gray"])
    factor_card(ax_b, patches, 0.803, "weight", r"$\Gamma_2^{1/4}$",
                PALETTE["gray"], PALETTE["xlight_gray"])
    for x_value in (0.197, 0.394, 0.591, 0.788):
        ax_b.text(x_value, 0.735, r"$\times$", transform=ax_b.transAxes,
                  ha="center", va="center", fontsize=7.0, color=PALETTE["charcoal"])
    ax_b.annotate("", xy=(0.50, 0.50), xytext=(0.50, 0.59), xycoords=ax_b.transAxes,
                  arrowprops={"arrowstyle": "-|>", "color": PALETTE["charcoal"],
                              "linewidth": 0.8, "mutation_scale": 8})
    ax_b.add_patch(patches.FancyBboxPatch(
        (0.055, 0.245), 0.89, 0.25, boxstyle="round,pad=0.018,rounding_size=0.025",
        facecolor=PALETTE["paper"], edgecolor=PALETTE["charcoal"], linewidth=0.9,
        transform=ax_b.transAxes,
    ))
    ax_b.text(0.50, 0.420, r"exact coefficient: $2\sqrt{2}$",
              transform=ax_b.transAxes, ha="center", va="center", fontsize=7.0,
              color=PALETTE["charcoal"], fontweight="bold")
    ax_b.text(0.50, 0.315,
              r"$P_R^M\geq2\sqrt{2}\,\theta h_2^{3/2}R\,\Gamma_2^{-5/4}L_2^{-1/2}$",
              transform=ax_b.transAxes, ha="center", va="center", fontsize=6.8,
              color=PALETTE["navy_dark"])
    ax_b.text(0.50, 0.10,
              r"powers $(\theta,h_2,R,\Gamma_2,L_2)=(1,3/2,1,-5/4,-1/2)$" + "\n" +
              "schedule of any inner lobe is absent",
              transform=ax_b.transAxes, ha="center", va="center", fontsize=5.25,
              color=PALETTE["gray"], linespacing=1.3)

    # C: positive reserve and divergence for theta=1.
    panel_title(ax_c, "C", r"Unit-dwell factor $\log\Lambda_2$")
    apply_axes_style(ax_c)
    scope_badge(ax_c, "DERIVED ANALYTIC VALUES")
    x_scaled = arrays["l1"] / 10000.0
    y_scaled = arrays["logLambda"] / 100000.0
    ax_c.plot(x_scaled, y_scaled, color=PALETTE["navy"], linewidth=1.45, zorder=3)
    checkpoints = np.array([0, 30, 60, 90, 120])
    ax_c.plot(x_scaled[checkpoints], y_scaled[checkpoints], linestyle="none", marker="o",
              markersize=4.0, markerfacecolor=PALETTE["paper"], markeredgecolor=PALETTE["orange"],
              markeredgewidth=1.0, zorder=4)
    ax_c.set_xlim(0.90, 2.03)
    ax_c.set_ylim(0.0, max(y_scaled) * 1.10)
    ax_c.set_xticks([1.0, 1.25, 1.5, 1.75, 2.0])
    ax_c.set_xlabel(r"$L_1/10^4$", fontsize=6.4, labelpad=2)
    ax_c.set_ylabel(r"$\log\Lambda_2/10^5$", fontsize=6.4, labelpad=3)
    ax_c.text(0.035, 0.78,
              r"$d_L=\log L_1,\ \theta=1,\ L_2=2L_1$" + "\n" +
              r"$5c_\gamma-a_S=603445/89413632>0$",
              transform=ax_c.transAxes, ha="left", va="top", fontsize=5.15,
              color=PALETTE["charcoal"],
              bbox={"boxstyle": "round,pad=0.25", "facecolor": PALETTE["paper"],
                    "edgecolor": PALETTE["light_gray"], "linewidth": 0.55})
    ax_c.annotate(r"quadratic reserve $\Rightarrow\Lambda_2\to\infty$",
                  xy=(x_scaled[-8], y_scaled[-8]), xytext=(1.18, max(y_scaled) * 0.55),
                  fontsize=5.15, color=PALETTE["orange_dark"],
                  arrowprops={"arrowstyle": "->", "color": PALETTE["orange"], "linewidth": 0.75})

    # D: necessary normalized dwell ceiling on the same path.
    panel_title(ax_d, "D", r"Necessary dwell ceiling from (T.28)")
    apply_axes_style(ax_d)
    scope_badge(ax_d, "DERIVED ANALYTIC VALUES / C=1")
    dwell_scaled = arrays["log10ThetaCeiling"] / 100000.0
    ax_d.plot(x_scaled, dwell_scaled, color=PALETTE["orange"], linewidth=1.45,
              linestyle="-", zorder=3)
    ax_d.plot(x_scaled[checkpoints], dwell_scaled[checkpoints], linestyle="none", marker="s",
              markersize=3.8, markerfacecolor=PALETTE["paper"], markeredgecolor=PALETTE["navy"],
              markeredgewidth=0.95, zorder=4)
    ax_d.axhline(0.0, color=PALETTE["charcoal"], linewidth=0.8,
                 linestyle=(0, (4, 2)), zorder=2)
    ax_d.text(0.97, 0.18, r"$\theta=1$ reference", ha="left", va="bottom",
              fontsize=5.15, color=PALETTE["charcoal"])
    ax_d.set_xlim(0.90, 2.03)
    ax_d.set_ylim(min(dwell_scaled) * 1.08, 0.65)
    ax_d.set_xticks([1.0, 1.25, 1.5, 1.75, 2.0])
    ax_d.set_xlabel(r"$L_1/10^4$", fontsize=6.4, labelpad=2)
    ax_d.set_ylabel(r"$\log_{10}\theta_{\max}/10^5$", fontsize=6.4, labelpad=3)
    ax_d.text(0.035, 0.12,
              r"$d_L=\log L_1$; illustrative $C=1$" + "\n" +
              r"general $C$: vertical shift by $\log_{10}C$",
              transform=ax_d.transAxes, ha="left", va="bottom", fontsize=5.15,
              color=PALETTE["charcoal"],
              bbox={"boxstyle": "round,pad=0.25", "facecolor": PALETTE["paper"],
                    "edgecolor": PALETTE["light_gray"], "linewidth": 0.55})
    ax_d.annotate("exponential-in-$L_1^2$ collapse",
                  xy=(x_scaled[-8], dwell_scaled[-8]), xytext=(1.17, min(dwell_scaled) * 0.52),
                  fontsize=5.15, color=PALETTE["navy_dark"],
                  arrowprops={"arrowstyle": "->", "color": PALETTE["navy"], "linewidth": 0.75})

    fig.text(0.045, 0.025,
             "Source: frozen core b120598d, R0.74T (T.9)–(T.43)  |  exact algebra and displayed analytic path",
             ha="left", va="bottom", fontsize=5.15, color=PALETTE["gray"])
    fig.text(0.975, 0.025, "NOT CLAY / full-clock gate remains open",
             ha="right", va="bottom", fontsize=5.15, color=PALETTE["orange_dark"], fontweight="bold")

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
                 "renderedAuditMargin": audit["margin"]}


def render_outputs(config: dict[str, Any], rows: list[dict[str, str]], arrays: dict[str, Any],
                   audit: dict[str, Any], runtime: dict[str, str], source_blobs: dict[str, bytes],
                   repository: Path) -> None:
    started = time.perf_counter()
    cpu_started = time.process_time()
    progress_rows: list[dict[str, object]] = []

    def progress(event: str) -> None:
        record = {"elapsedSeconds": time.perf_counter() - started, "event": event,
                  "pid": os.getpid(),
                  "utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds")}
        progress_rows.append(record)
        print(f"[{record['elapsedSeconds']:.3f}s] {event}", flush=True)

    progress("render-start")
    with tempfile.TemporaryDirectory(prefix="r074t-dwell-figure-render-") as temporary:
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
        from matplotlib import patches
        from PIL import Image, ImageOps
        import pypdfium2 as pdfium

        progress("runtime-loaded")
        write_csv(stage / "source-data.csv", rows)
        progress("source-data-written")
        fig, render_audit = render_figure(config, arrays, audit, np, plt, patches)
        need(render_audit["artistBoundsPass"],
             "rendered text exceeds canvas: " + repr(render_audit["textOverflow"]))
        progress("figure-composed")

        width_mm = float(config["widthMillimetres"])
        height_mm = float(config["heightMillimetres"])
        png_dpi = int(config["pngDpi"])
        qa_dpi = int(config["qaDpi"])
        figure_metadata = {
            "Creator": "R0.74T deterministic analytic-figure renderer",
            "Title": "Schedule-invariant lobe coercivity and the dwell barrier",
            "Subject": "Analytic schematic and derived analytic values; not PDE data; not DNS; not Clay",
        }
        fig.savefig(stage / "figure.png", dpi=png_dpi,
                    metadata={"Software": "R0.74T deterministic analytic-figure renderer"})
        fig.savefig(stage / "figure.pdf",
                    metadata={**figure_metadata, "CreationDate": None, "ModDate": None})
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
        need(master.size == master_expected,
             f"master PNG size drift: {master.size} != {master_expected}")
        final_size = master.resize(qa_expected, Image.Resampling.LANCZOS)
        final_size.save(stage / "qa-final-size.png", dpi=(qa_dpi, qa_dpi),
                        optimize=False, compress_level=6)
        ImageOps.grayscale(final_size).convert("RGB").save(
            stage / "qa-grayscale.png", dpi=(qa_dpi, qa_dpi), optimize=False, compress_level=6)
        progress("png-qa-assets-written")

        document = pdfium.PdfDocument(str(stage / "figure.pdf"))
        page = document[0]
        width_points, _ = page.get_size()
        pdf_image = page.render(scale=qa_expected[0] / float(width_points)).to_pil().convert("RGB")
        page.close()
        document.close()
        if pdf_image.size != qa_expected:
            pdf_image = pdf_image.resize(qa_expected, Image.Resampling.LANCZOS)
        pdf_image.save(stage / "qa-pdf.png", dpi=(qa_dpi, qa_dpi),
                       optimize=False, compress_level=6)
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
            "schema": "r074t-schedule-invariant-dwell-barrier-results-v1",
            "sourceBinding": {"commit": config["sourceBinding"]["commit"],
                              "fileCount": len(source_blobs)},
            "status": "PASS" if audit["checksPassed"] and render_audit["artistBoundsPass"] else "FAIL",
        }
        (stage / "results.json").write_text(canonical(results), encoding="utf-8", newline="\n")
        progress("results-written")

        environment = {
            "createdAtUtc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds"),
            "logicalCpuCount": os.cpu_count(), "machine": platform.machine(),
            "matplotlibConfigPolicy": "system temporary directory removed after render",
            "memoryBytes": int(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")),
            "operatingSystem": platform.platform(), "packages": runtime, "python": runtime["python"],
            "repositoryHead": git_text(repository, ["rev-parse", "HEAD"]),
            "schema": "r074t-figure-environment-v1",
        }
        (stage / "environment.json").write_text(canonical(environment), encoding="utf-8", newline="\n")
        progress("environment-recorded")

        resource_row = {
            "cpuSeconds": time.process_time() - cpu_started,
            "maximumResidentSetSizeRaw": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "pid": os.getpid(), "schema": "r074t-figure-resource-v1",
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
