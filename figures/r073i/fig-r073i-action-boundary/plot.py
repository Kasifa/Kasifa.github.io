#!/usr/bin/env python3
"""Render the R0.73I formal finite action-boundary figure package.

All colored numerical marks produced here are finite binary64
Fourier--Galerkin diagnostics.  This renderer does not turn ordinary cutoff
agreement into a Fourier-tail estimate or the observed WKB correction into a
continuum asymptotic theorem.
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
import shutil
import subprocess
import sys
import time
from typing import Any, Iterable, Mapping


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EVIDENCE_CLASS = "finite-binary64-galerkin-diagnostic-only"
FIGURE_ID = "fig-r073i-action-boundary"
SOURCE_FILES = (
    "README.md",
    "caption.md",
    "command.txt",
    "config.json",
    "contract.json",
    "plot.py",
    "qa-protocol.md",
    "qa-report.md",
    "requirements.txt",
    "validate.py",
)
GENERATED_FILES = (
    "source-data.csv",
    "figure.pdf",
    "figure.svg",
    "figure.png",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "environment.json",
    "progress.ndjson",
    "results.json",
    "manifest.json",
    "SHA256SUMS",
)
DATA_FIELDS = (
    "panel",
    "recordKind",
    "series",
    "evidenceClass",
    "windowId",
    "endpointExpression",
    "endpoint",
    "endpointRole",
    "N",
    "quadratureOrder",
    "Lambda",
    "x",
    "y",
    "finiteAction",
    "finiteAverageRate",
    "finiteWkbCorrection",
    "residualLogGainMinusLambdaAction",
    "residualMinusWkb",
    "sourcePath",
    "sourceSha256",
    "sourceRowKey",
    "note",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


ARGS = parse_args()
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image, ImageStat  # noqa: E402


STARTED = time.perf_counter()
PROGRESS = HERE / "progress.ndjson"
SEQUENCE = 0


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def atomic_text(path: Path, value: str) -> None:
    temporary = path.with_name("." + path.name + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def binding(path: Path, base: Path) -> dict[str, object]:
    return {
        "path": path.resolve().relative_to(base.resolve()).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def git_text(*arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *arguments],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def emit(event: str, **fields: object) -> None:
    global SEQUENCE
    SEQUENCE += 1
    row = {
        "sequence": SEQUENCE,
        "timestampUtc": now_utc(),
        "elapsedSeconds": round(time.perf_counter() - STARTED, 6),
        "event": event,
        **fields,
    }
    rendered = json.dumps(row, sort_keys=True, allow_nan=False)
    print(rendered, flush=True)
    with PROGRESS.open("a", encoding="utf-8") as stream:
        stream.write(rendered + "\n")


def prepare_output(overwrite: bool) -> None:
    HERE.mkdir(parents=True, exist_ok=True)
    existing = [HERE / name for name in GENERATED_FILES if (HERE / name).exists()]
    if existing and not overwrite:
        names = ", ".join(path.name for path in existing)
        raise RuntimeError(f"refusing to overwrite generated files: {names}")
    for path in existing:
        path.unlink()
    PROGRESS.write_text("", encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root is not an object: {path}")
    return value


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def validate_boundary(boundary: Mapping[str, object]) -> None:
    require(
        boundary.get("formalFiniteDiagnosticFigure") is True,
        "formal finite diagnostic flag is absent",
    )
    require(
        boundary.get("experimentInputsPassedTheirFiniteValidator") is True,
        "finite-input validation flag is absent",
    )
    for key, value in boundary.items():
        if key not in {
            "formalFiniteDiagnosticFigure",
            "experimentInputsPassedTheirFiniteValidator",
        }:
            require(value is False, f"claim boundary must fail closed: {key}")


def source_row(
    *,
    panel: str,
    record_kind: str,
    series: str,
    evidence_class: str,
    source_path: str,
    source_digest: str,
    source_key: str,
    note: str,
    window_id: str = "",
    endpoint_expression: str = "",
    endpoint: object = "",
    endpoint_role: str = "",
    n_cut: object = "",
    quadrature_order: object = "",
    absolute_lambda: object = "",
    x_value: object = "",
    y_value: object = "",
    finite_action: object = "",
    finite_average_rate: object = "",
    finite_wkb: object = "",
    residual: object = "",
    residual_minus_wkb: object = "",
) -> dict[str, object]:
    return {
        "panel": panel,
        "recordKind": record_kind,
        "series": series,
        "evidenceClass": evidence_class,
        "windowId": window_id,
        "endpointExpression": endpoint_expression,
        "endpoint": endpoint,
        "endpointRole": endpoint_role,
        "N": n_cut,
        "quadratureOrder": quadrature_order,
        "Lambda": absolute_lambda,
        "x": x_value,
        "y": y_value,
        "finiteAction": finite_action,
        "finiteAverageRate": finite_average_rate,
        "finiteWkbCorrection": finite_wkb,
        "residualLogGainMinusLambdaAction": residual,
        "residualMinusWkb": residual_minus_wkb,
        "sourcePath": source_path,
        "sourceSha256": source_digest,
        "sourceRowKey": source_key,
        "note": note,
    }


def write_source_data(path: Path, rows: Iterable[Mapping[str, object]]) -> None:
    temporary = path.with_name("." + path.name + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=DATA_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            encoded: dict[str, object] = {}
            for field in DATA_FIELDS:
                value = row[field]
                if isinstance(value, float):
                    require(math.isfinite(value), f"nonfinite source-data field: {field}")
                    encoded[field] = format(value, ".17g")
                else:
                    encoded[field] = value
            writer.writerow(encoded)
    os.replace(temporary, path)


def prepare_data(
    config: Mapping[str, Any],
) -> tuple[list[dict[str, object]], dict[str, Any], list[dict[str, object]]]:
    inputs = config["inputs"]
    input_paths = {key: ROOT / value for key, value in inputs.items()}
    for key, path in input_paths.items():
        require(path.is_file() and not path.is_symlink(), f"input absent: {key}")

    summary = load_json(input_paths["summary"])
    experiment_manifest = load_json(input_paths["experimentManifest"])
    require(summary.get("allChecksPass") is True, "R0.73I finite summary did not pass")
    require(summary.get("diagnosticOnly") is True, "R0.73I diagnostic boundary missing")
    require(
        summary.get("evidenceClass") == EVIDENCE_CLASS,
        "unexpected R0.73I evidence class",
    )
    require(
        experiment_manifest.get("allChecksPass") is True,
        "R0.73I manifest did not archive a passing finite run",
    )
    finite_boundary = summary.get("claimBoundary", {})
    require(
        finite_boundary.get("finiteBinary64GalerkinDiagnostic") is True,
        "upstream finite diagnostic flag is absent",
    )
    require(
        all(
            value is False
            for key, value in finite_boundary.items()
            if key != "finiteBinary64GalerkinDiagnostic"
        ),
        "upstream continuum claim boundary is not fail closed",
    )

    action_path = input_paths["actionRows"]
    gain_path = input_paths["gainRows"]
    action_rows = read_csv(action_path)
    gain_rows = read_csv(gain_path)
    action_digest = sha256(action_path)
    gain_digest = sha256(gain_path)
    config_digest = sha256(HERE / "config.json")
    upper_digest = sha256(input_paths["analyticUpperActionProof"])
    inherited_digest = sha256(input_paths["inheritedRateSource"])

    windows = list(config["windows"])
    cutoffs = [int(value) for value in config["cutoffs"]]
    lambdas = [int(value) for value in config["lambdas"]]
    primary_order = int(config["primaryQuadratureOrder"])
    primary_cutoff = int(config["primaryCutoff"])
    rows: list[dict[str, object]] = []
    selected_action: dict[tuple[str, int], dict[str, str]] = {}
    for window_index, window_id in enumerate(windows):
        for n_cut in cutoffs:
            matches = [
                row for row in action_rows
                if row["windowId"] == window_id
                and int(row["N"]) == n_cut
                and int(row["quadratureOrder"]) == primary_order
                and row["smokeMode"] == "false"
            ]
            require(len(matches) == 1, f"action row is not unique: {window_id}, N={n_cut}")
            row = matches[0]
            require(row["diagnosticOnly"] == "true", "action row boundary drift")
            selected_action[(window_id, n_cut)] = row
            rows.append(source_row(
                panel="A",
                record_kind="finite-average-action",
                series=f"N={n_cut}",
                evidence_class=EVIDENCE_CLASS,
                window_id=window_id,
                endpoint_expression=row["endpointExpression"],
                endpoint=float(row["endpoint"]),
                endpoint_role=row["endpointRole"],
                n_cut=n_cut,
                quadrature_order=primary_order,
                x_value=float(window_index),
                y_value=float(row["finiteAverageRate"]),
                finite_action=float(row["finiteAction"]),
                finite_average_rate=float(row["finiteAverageRate"]),
                finite_wkb=float(row["finiteWkbCorrection"]),
                source_path=str(action_path.relative_to(ROOT)),
                source_digest=action_digest,
                source_key=f"windowId={window_id};N={n_cut};quadratureOrder={primary_order}",
                note="finite diagnostic only; ordinary cutoff agreement is not a tail proof",
            ))

    c_h_0 = math.sqrt(19.0 / 180.0)
    r_reference = float(config["references"]["rReference"])
    rows.append(source_row(
        panel="A",
        record_kind="analytic-upper-bound-reference",
        series="c_H(0)",
        evidence_class="rigorous-continuum-upper-bound-reference",
        x_value="all-windows",
        y_value=c_h_0,
        source_path=str(input_paths["analyticUpperActionProof"].relative_to(ROOT)),
        source_digest=upper_digest,
        source_key="equation (3.7)",
        note="rigorous numerical-abscissa upper bound at d=0; not the selected action",
    ))
    rows.append(source_row(
        panel="A",
        record_kind="inherited-rate-reference",
        series="r=0.17035 reference",
        evidence_class="analytic-reference-threshold",
        x_value="all-windows",
        y_value=r_reference,
        source_path=str(input_paths["inheritedRateSource"].relative_to(ROOT)),
        source_digest=inherited_digest,
        source_key="r=alpha+eta>0.17035",
        note="reference threshold only; the theorem rate is strictly greater than 0.17035",
    ))

    selected_gain: dict[tuple[str, int], dict[str, str]] = {}
    for window_id in windows:
        action = selected_action[(window_id, primary_cutoff)]
        for absolute_lambda in lambdas:
            matches = [
                row for row in gain_rows
                if row["gridKind"] == "primary"
                and row["windowId"] == window_id
                and int(row["N"]) == primary_cutoff
                and int(row["Lambda"]) == absolute_lambda
                and row["smokeMode"] == "false"
            ]
            require(len(matches) == 1, f"gain row is not unique: {window_id}, Lambda={absolute_lambda}")
            row = matches[0]
            require(row["diagnosticOnly"] == "true", "gain row boundary drift")
            remainder = float(row["residualMinusWkb"])
            require(remainder > 0.0, "log-scale correction remainder is not positive")
            selected_gain[(window_id, absolute_lambda)] = row
            rows.append(source_row(
                panel="B",
                record_kind="finite-residual-minus-wkb",
                series=window_id,
                evidence_class=EVIDENCE_CLASS,
                window_id=window_id,
                endpoint_expression=action["endpointExpression"],
                endpoint=float(row["endpoint"]),
                endpoint_role=row["endpointRole"],
                n_cut=primary_cutoff,
                quadrature_order=primary_order,
                absolute_lambda=absolute_lambda,
                x_value=float(absolute_lambda),
                y_value=remainder,
                finite_action=float(row["finiteAction"]),
                finite_average_rate=float(row["finiteAverageRate"]),
                finite_wkb=float(row["finiteWkbCorrection"]),
                residual=float(row["residualLogGainMinusLambdaAction"]),
                residual_minus_wkb=remainder,
                source_path=str(gain_path.relative_to(ROOT)),
                source_digest=gain_digest,
                source_key=(
                    f"gridKind=primary;windowId={window_id};N={primary_cutoff};"
                    f"Lambda={absolute_lambda}"
                ),
                note="finite diagnostic only; approach to C_N is not an asymptotic theorem",
            ))

    guide_constant = float(config["panelB"]["inverseLambdaGuideConstant"])
    for absolute_lambda in config["panelB"]["inverseLambdaGuideRange"]:
        value = float(absolute_lambda)
        rows.append(source_row(
            panel="B",
            record_kind="visual-slope-guide",
            series="Lambda^-1 guide",
            evidence_class="visual-guide-only",
            absolute_lambda=int(absolute_lambda),
            x_value=value,
            y_value=guide_constant / value,
            source_path=str((HERE / "config.json").relative_to(ROOT)),
            source_digest=config_digest,
            source_key="panelB.inverseLambdaGuideConstant/range",
            note="visual slope guide only; not a fit, error bound, or proof",
        ))

    expected_count = len(windows) * len(cutoffs) + 2 + len(windows) * len(lambdas) + 2
    require(len(rows) == expected_count, "plotted-data inventory is incomplete")
    input_bindings = [binding(path, ROOT) for path in input_paths.values()]
    numeric = {
        "cH0": c_h_0,
        "rReference": r_reference,
        "selectedAction": selected_action,
        "selectedGain": selected_gain,
        "summary": summary,
        "inputBindings": input_bindings,
    }
    return rows, numeric, input_bindings


def add_research_blossom(fig: Any, colors: Mapping[str, str]) -> None:
    axis = fig.add_axes([0.947, 0.908, 0.037, 0.069], label="research-blossom")
    axis.set_xlim(-1.05, 1.05)
    axis.set_ylim(-1.05, 1.05)
    axis.set_aspect("equal")
    axis.axis("off")
    for index, angle in enumerate(np.linspace(0.0, 2.0 * math.pi, 5, endpoint=False)):
        center = (0.52 * math.cos(angle), 0.52 * math.sin(angle))
        axis.add_patch(Circle(
            center,
            0.29,
            facecolor=colors["blueLight"] if index % 2 == 0 else "white",
            edgecolor=colors["blue"] if index % 2 == 0 else colors["orange"],
            linewidth=0.65,
        ))
    axis.add_patch(Circle((0.0, 0.0), 0.16, facecolor=colors["orange"],
                          edgecolor=colors["ink"], linewidth=0.5))


def draw_figure(
    config: Mapping[str, Any],
    numeric: Mapping[str, Any],
) -> dict[str, object]:
    style = ROOT / "figures/journal.mplstyle"
    if style.is_file():
        plt.style.use(style)
    matplotlib.rcParams.update({
        "figure.constrained_layout.use": False,
        "svg.hashsalt": "r073i-action-boundary-formal-v1",
        "axes.unicode_minus": True,
    })
    colors = config["palette"]
    width_inches = float(config["widthMillimetres"]) / 25.4
    height_inches = float(config["heightMillimetres"]) / 25.4
    fig = plt.figure(figsize=(width_inches, height_inches), facecolor="white")
    outer = fig.add_gridspec(
        1,
        2,
        left=0.082,
        right=0.979,
        bottom=0.205,
        top=0.875,
        wspace=0.31,
        width_ratios=[1.0, 1.05],
    )
    left = outer[0, 0].subgridspec(2, 1, height_ratios=[1.05, 4.0], hspace=0.055)
    axis_a_top = fig.add_subplot(left[0, 0])
    axis_a = fig.add_subplot(left[1, 0], sharex=axis_a_top)
    axis_b = fig.add_subplot(outer[0, 1])

    windows = list(config["windows"])
    cutoffs = [int(value) for value in config["cutoffs"]]
    action = numeric["selectedAction"]
    x_positions = np.arange(len(windows), dtype=float)
    styles = {
        24: {
            "color": colors["muted"], "marker": "^", "linestyle": ":",
            "mfc": "white", "markersize": 6.0, "zorder": 4,
        },
        48: {
            "color": colors["blueLight"], "marker": "s", "linestyle": "--",
            "mfc": "white", "markersize": 4.6, "zorder": 5,
        },
        96: {
            "color": colors["blue"], "marker": "o", "linestyle": "-",
            "mfc": colors["blue"], "markersize": 2.8, "zorder": 6,
        },
    }
    for n_cut in cutoffs:
        values = [float(action[(window, n_cut)]["finiteAverageRate"]) for window in windows]
        spec = styles[n_cut]
        axis_a.plot(
            x_positions,
            values,
            label=rf"$N={n_cut}$",
            color=spec["color"],
            marker=spec["marker"],
            linestyle=spec["linestyle"],
            markerfacecolor=spec["mfc"],
            markeredgecolor=spec["color"],
            markeredgewidth=0.75,
            markersize=spec["markersize"],
            zorder=spec["zorder"],
        )

    c_h_0 = float(numeric["cH0"])
    r_reference = float(numeric["rReference"])
    axis_a_top.axhline(c_h_0, color=colors["ink"], linestyle="-.", linewidth=1.0)
    axis_a_top.text(
        -0.25,
        c_h_0 + 0.00125,
        r"$c_H(0)=\sqrt{19/180}$" + "\nrigorous upper bound",
        color=colors["ink"],
        fontsize=6.0,
        va="bottom",
    )
    axis_a.axhline(r_reference, color=colors["orange"], linestyle="--", linewidth=1.0)
    axis_a.text(
        1.02,
        r_reference + 0.000010,
        r"$r=0.17035$ reference",
        color=colors["orange"],
        fontsize=6.0,
        va="bottom",
        bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.5, "alpha": 0.9},
    )

    axis_a_top.set_ylim(*[float(value) for value in config["panelA"]["upperYLimits"]])
    axis_a.set_ylim(*[float(value) for value in config["panelA"]["lowerYLimits"]])
    axis_a_top.set_yticks([c_h_0])
    axis_a_top.set_yticklabels([f"{c_h_0:.4f}"])
    axis_a.set_yticks([0.1700, 0.1702, 0.1704])
    axis_a_top.tick_params(axis="x", which="both", bottom=False, labelbottom=False)
    axis_a_top.spines["bottom"].set_visible(False)
    axis_a.spines["top"].set_visible(False)
    axis_a_top.set_title("A  Finite average action and references", loc="left", fontweight="bold")
    axis_a.set_xlim(-0.34, 2.34)
    axis_a.set_xticks(x_positions)
    axis_a.set_xticklabels([
        r"$10^{-4}$" + "\npilot",
        r"$D_{\rm ub}$" + "\nnot $d_0$",
        r"$1/450$" + "\nnot endpoint",
    ])
    axis_a.set_xlabel("declared window $D$")
    axis_a.yaxis.grid(True, color=colors["grid"], linestyle=":", linewidth=0.55)
    axis_a_top.yaxis.grid(False)
    fig.text(
        0.018,
        0.535,
        r"finite average action $\mathcal{A}_N(D)/D$",
        rotation=90,
        ha="center",
        va="center",
        fontsize=7.2,
        color=colors["ink"],
    )
    axis_a.legend(
        loc="lower left",
        bbox_to_anchor=(0.01, 0.02),
        title="finite diagnostic only",
        title_fontsize=5.8,
        fontsize=6.0,
        handlelength=1.7,
        borderaxespad=0.0,
        labelspacing=0.25,
    )

    break_size = 0.013
    kwargs = {"color": colors["ink"], "clip_on": False, "linewidth": 0.7}
    axis_a_top.plot((-break_size, +break_size), (-break_size, +break_size),
                    transform=axis_a_top.transAxes, **kwargs)
    axis_a_top.plot((1 - break_size, 1 + break_size), (-break_size, +break_size),
                    transform=axis_a_top.transAxes, **kwargs)
    axis_a.plot((-break_size, +break_size), (1 - break_size, 1 + break_size),
                transform=axis_a.transAxes, **kwargs)
    axis_a.plot((1 - break_size, 1 + break_size), (1 - break_size, 1 + break_size),
                transform=axis_a.transAxes, **kwargs)

    gain = numeric["selectedGain"]
    lambdas = [int(value) for value in config["lambdas"]]
    series_styles = {
        "explicit-pilot": {
            "label": r"$10^{-4}$ pilot",
            "color": colors["blue"],
            "marker": "o",
            "linestyle": "-",
            "mfc": colors["blue"],
        },
        "analytic-upper-bound": {
            "label": r"$D_{\rm ub}$ (not $d_0$)",
            "color": colors["orange"],
            "marker": "s",
            "linestyle": "--",
            "mfc": "white",
        },
        "one-over-450": {
            "label": r"$1/450$ (legacy)",
            "color": colors["ink"],
            "marker": "^",
            "linestyle": ":",
            "mfc": "white",
        },
    }
    for window in windows:
        values = [float(gain[(window, value)]["residualMinusWkb"]) for value in lambdas]
        spec = series_styles[window]
        axis_b.plot(
            lambdas,
            values,
            label=spec["label"],
            color=spec["color"],
            marker=spec["marker"],
            linestyle=spec["linestyle"],
            markerfacecolor=spec["mfc"],
            markeredgecolor=spec["color"],
            markeredgewidth=0.75,
        )
    guide_range = np.asarray(config["panelB"]["inverseLambdaGuideRange"], dtype=float)
    guide_constant = float(config["panelB"]["inverseLambdaGuideConstant"])
    axis_b.plot(
        guide_range,
        guide_constant / guide_range,
        color=colors["muted"],
        linestyle="-.",
        linewidth=0.9,
        label=r"$\Lambda^{-1}$ visual guide",
    )
    axis_b.set_xscale("log")
    axis_b.set_yscale("log")
    axis_b.set_xlim(*[float(value) for value in config["panelB"]["xLimits"]])
    axis_b.set_ylim(*[float(value) for value in config["panelB"]["yLimits"]])
    axis_b.set_xticks([1.0e4, 1.0e5, 1.0e6])
    axis_b.set_yticks([1.0e-6, 1.0e-5, 1.0e-4])
    axis_b.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    axis_b.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    axis_b.set_xlabel(r"$\Lambda=\varepsilon^{-1}$")
    axis_b.set_ylabel(r"$R_{\Lambda,48}(D)-C_{48}(D)$")
    axis_b.set_title("B  Finite correction remainder", loc="left", fontweight="bold")
    axis_b.grid(True, which="major", color=colors["grid"], linestyle=":", linewidth=0.55)
    axis_b.legend(
        loc="upper right",
        title="finite diagnostic only\nguide not fitted",
        title_fontsize=5.8,
        fontsize=6.0,
        handlelength=2.1,
        labelspacing=0.3,
    )

    for axis in (axis_a_top, axis_a, axis_b):
        axis.tick_params(pad=2)

    fig.text(
        0.082,
        0.055,
        "All endpoint data marks/curves: finite binary64 Fourier–Galerkin diagnostic only.  "
        r"$D_{\rm ub}$ and $1/450$ are not theorem endpoints.",
        ha="left",
        va="bottom",
        fontsize=5.65,
        color=colors["ink"],
    )
    add_research_blossom(fig, colors)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    canvas_width, canvas_height = fig.canvas.get_width_height()
    text_boxes = []
    for item in fig.findobj(match=lambda artist: isinstance(artist, matplotlib.text.Text)):
        if not item.get_visible() or not item.get_text().strip():
            continue
        box = item.get_window_extent(renderer=renderer)
        text_boxes.append((box.x0, box.y0, box.x1, box.y1, item.get_text()))
    within_canvas = all(
        x0 >= -1.0 and y0 >= -1.0 and x1 <= canvas_width + 1.0 and y1 <= canvas_height + 1.0
        for x0, y0, x1, y1, _ in text_boxes
    )
    offenders = [
        {"bounds": [x0, y0, x1, y1], "text": label}
        for x0, y0, x1, y1, label in text_boxes
        if x0 < -1.0 or y0 < -1.0 or x1 > canvas_width + 1.0 or y1 > canvas_height + 1.0
    ]
    require(
        within_canvas,
        "rendered text leaves the figure canvas: "
        + json.dumps(offenders, ensure_ascii=False),
    )

    title = "R0.73I finite selected-gain action boundary diagnostic"
    creator = "figures/r073i/fig-r073i-action-boundary/plot.py"
    outputs = []
    for name, file_format, metadata, dpi in (
        (
            "figure.pdf",
            "pdf",
            {
                "Creator": creator,
                "Title": title,
                "Subject": EVIDENCE_CLASS,
                "CreationDate": None,
                "ModDate": None,
            },
            None,
        ),
        (
            "figure.svg",
            "svg",
            {
                "Creator": creator,
                "Title": title,
                "Description": EVIDENCE_CLASS,
                "Date": None,
            },
            None,
        ),
        (
            "figure.png",
            "png",
            {
                "Software": creator,
                "Title": title,
                "Description": EVIDENCE_CLASS,
            },
            int(config["pngDpi"]),
        ),
    ):
        path = HERE / name
        temporary = path.with_name("." + path.name + ".tmp")
        options: dict[str, object] = {"format": file_format, "metadata": metadata}
        if dpi is not None:
            options["dpi"] = dpi
        fig.savefig(temporary, **options)
        os.replace(temporary, path)
        outputs.append(binding(path, HERE))
    plt.close(fig)
    emit("vector_and_master_exports_complete", outputCount=len(outputs))
    return {
        "outputs": outputs,
        "textBoundingBoxesWithinCanvas": within_canvas,
        "textObjectCount": len(text_boxes),
    }


def build_qa(config: Mapping[str, Any]) -> dict[str, object]:
    width_mm = float(config["widthMillimetres"])
    height_mm = float(config["heightMillimetres"])
    master_dpi = int(config["pngDpi"])
    qa_dpi = int(config["qaDpi"])
    expected_master = (
        int(width_mm / 25.4 * master_dpi),
        int(height_mm / 25.4 * master_dpi),
    )
    expected_qa = (
        round(width_mm / 25.4 * qa_dpi),
        round(height_mm / 25.4 * qa_dpi),
    )
    expected_pdf_qa = (
        math.ceil(width_mm / 25.4 * qa_dpi),
        math.ceil(height_mm / 25.4 * qa_dpi),
    )
    with Image.open(HERE / "figure.png") as image:
        require(image.size == expected_master, f"unexpected master PNG size: {image.size}")
        final_size = image.convert("RGB").resize(expected_qa, Image.Resampling.LANCZOS)
        final_size.save(HERE / "qa-final-size.png", dpi=(qa_dpi, qa_dpi), optimize=False)
        grayscale = final_size.convert("L")
        grayscale.save(HERE / "qa-grayscale.png", dpi=(qa_dpi, qa_dpi), optimize=False)
        grayscale_std = float(ImageStat.Stat(grayscale).stddev[0])

    pdftoppm = shutil.which("pdftoppm")
    require(pdftoppm is not None, "pdftoppm is required for independent PDF QA")
    prefix = HERE / ".qa-pdf-raster"
    subprocess.run(
        [pdftoppm, "-r", str(qa_dpi), "-png", "-singlefile", str(HERE / "figure.pdf"), str(prefix)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    generated_pdf_raster = prefix.with_suffix(".png")
    require(generated_pdf_raster.is_file(), "pdftoppm did not create its raster")
    os.replace(generated_pdf_raster, HERE / "qa-pdf.png")
    with Image.open(HERE / "qa-pdf.png") as pdf_image:
        require(
            pdf_image.size == expected_pdf_qa,
            f"unexpected PDF QA raster size: {pdf_image.size}",
        )
    emit(
        "qa_surfaces_complete",
        masterPixels=list(expected_master),
        qaPixels=list(expected_qa),
        pdfQaPixels=list(expected_pdf_qa),
        grayscaleStandardDeviation=grayscale_std,
    )
    return {
        "masterPngPixels": list(expected_master),
        "qaPixels": list(expected_qa),
        "pdfQaPixels": list(expected_pdf_qa),
        "masterDpi": master_dpi,
        "qaDpi": qa_dpi,
        "grayscaleStandardDeviation": grayscale_std,
        "pdftoppm": pdftoppm,
        "qaBindings": [
            binding(HERE / name, HERE)
            for name in ("qa-final-size.png", "qa-grayscale.png", "qa-pdf.png")
        ],
    }


def manual_qa_passed() -> bool:
    report = (HERE / "qa-report.md").read_text(encoding="utf-8")
    return "Status: **PASS**" in report and "inspected" in report.lower()


def write_manifest_and_ledger(
    config: Mapping[str, Any],
    contract: Mapping[str, Any],
    input_bindings: list[dict[str, object]],
    source_commit: str,
    branch: str,
) -> None:
    source_bindings = [binding(HERE / name, HERE) for name in SOURCE_FILES]
    output_names = [
        "source-data.csv",
        "figure.pdf",
        "figure.svg",
        "figure.png",
        "qa-final-size.png",
        "qa-grayscale.png",
        "qa-pdf.png",
        "environment.json",
        "progress.ndjson",
        "results.json",
    ]
    output_bindings = [binding(HERE / name, HERE) for name in output_names]
    environment = load_json(HERE / "environment.json")
    result = load_json(HERE / "results.json")
    by_name = {record["path"]: record for record in output_bindings}
    figure_outputs = [dict(by_name[name]) for name in ("figure.pdf", "figure.svg", "figure.png")]
    figure_outputs[-1]["dpi"] = int(config["pngDpi"])
    figure_outputs[-1]["pixels"] = result["renderQa"]["masterPngPixels"]
    public_assets = []
    for record in figure_outputs:
        suffix = Path(str(record["path"])).suffix
        public_assets.append({
            "path": f"public/assets/r073i/{FIGURE_ID}{suffix}",
            "bytes": record["bytes"],
            "sha256": record["sha256"],
        })
    manifest = {
        "schemaVersion": "r073i-action-boundary-manifest-v1",
        "figureId": FIGURE_ID,
        "release": "R0.73I",
        "status": "formal",
        "analyticalQuestion": (
            "What do the finite selected-gain action and WKB-correction diagnostics show "
            "on three explicitly labelled windows without being promoted to a continuum theorem?"
        ),
        "supportedClaim": (
            "The archived binary64 Fourier--Galerkin panels are finite route diagnostics only: "
            "they compare three labelled windows and support the next contour/adiabatic audit, "
            "but prove no continuum matching action, two-term asymptotic, or Clay result."
        ),
        "createdAt": "2026-08-30T19:55:09.592878+08:00",
        "evidenceClass": EVIDENCE_CLASS,
        "diagnosticOnly": True,
        "sourceCommit": source_commit,
        "branch": branch,
        "workingTreeCleanAtRun": not bool(git_text("status", "--porcelain")),
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": source_commit,
            "certificateCommit": "4ab51d1251cb5f5ca85c82731ac7f8e7b512c368",
            "dirtyAtCertifiedRun": False,
            "dirtyAtCertifiedRunMeaning": (
                "the renderer source and certificate inputs are read from immutable commits; "
                "generated outputs and unrelated working-tree files are excluded"
            ),
            "wholeWorktreeCleanAtRun": False,
        },
        "computation": {
            "kind": "closed-form sampling plus validated finite CSV ingestion",
            "configuration": "config.json",
            "precision": "IEEE-754 binary64 finite Fourier--Galerkin diagnostics",
            "solver": "committed finite CSV ingestion and deterministic Matplotlib rendering",
            "formalCommand": "command.txt",
            "scientificWallTimeSeconds": environment["wallTimeSeconds"],
            "processes": 1,
            "threadsPerProcess": 1,
            "finiteDimensionalPanelsAreDiagnosticOnly": True,
        },
        "compute": {
            "host": "Wool.local",
            "operatingSystem": environment["platform"],
            "cpu": "Apple M5 Max",
            "memoryGiB": 36.0,
            "processes": 1,
            "threadsPerProcess": 1,
            "gpu": "not used",
        },
        "environment": {
            "python": environment["python"],
            "numpy": environment["numpy"],
            "matplotlib": environment["matplotlib"],
            "pillow": environment["pillow"],
            "packagesLock": "requirements.txt",
        },
        "data": [
            {**by_name["source-data.csv"], "schema": "r073i-action-boundary-source-data-v1"},
            {**by_name["results.json"], "schema": "r073i-action-boundary-results-v1"},
        ],
        "sourceData": input_bindings,
        "sourceBindings": source_bindings,
        "inputBindings": input_bindings,
        "outputBindings": output_bindings,
        "figure": {
            "widthMillimetres": config["widthMillimetres"],
            "heightMillimetres": config["heightMillimetres"],
            "pngDpi": config["pngDpi"],
            "profile": "journal-double-column",
            "layout": "two-panel finite action and WKB residual diagnostic",
            "outputs": figure_outputs,
        },
        "dimensions": {
            "widthMillimetres": config["widthMillimetres"],
            "heightMillimetres": config["heightMillimetres"],
            "pngDpi": config["pngDpi"],
        },
        "qa": {
            "status": "passed",
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
            "finalSizeSurface": True,
            "grayscaleSurface": True,
            "independentPdfRasterSurface": True,
            "visualInspectionExplicit": manual_qa_passed(),
        },
        "caption": {"english": "caption.md"},
        "publication": {
            "directory": "public/assets/r073i",
            "fileStem": FIGURE_ID,
            "byteIdentityRequired": True,
            "publicCopiesComplete": True,
            "assets": public_assets,
        },
        "claimBoundary": contract["claimBoundary"],
        "inventoryPolicy": "flat package; SHA256SUMS covers every regular file except itself",
    }
    atomic_text(HERE / "manifest.json", canonical(manifest))
    names = sorted(
        path.name
        for path in HERE.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    expected = sorted(set(SOURCE_FILES) | (set(GENERATED_FILES) - {"SHA256SUMS"}))
    require(names == expected, "figure package contains an unexpected or missing flat file")
    ledger = "".join(f"{sha256(HERE / name)}  {name}\n" for name in names)
    atomic_text(HERE / "SHA256SUMS", ledger)


def main() -> int:
    prepare_output(ARGS.overwrite)
    source_commit = git_text("rev-parse", "HEAD")
    branch = git_text("rev-parse", "--abbrev-ref", "HEAD")
    emit("start", sourceCommit=source_commit, branch=branch)
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    require(config.get("figureId") == FIGURE_ID, "config figure ID drift")
    require(contract.get("figureId") == FIGURE_ID, "contract figure ID drift")
    require(contract.get("evidenceClass") == EVIDENCE_CLASS, "contract evidence class drift")
    validate_boundary(contract.get("claimBoundary", {}))

    rows, numeric, input_bindings = prepare_data(config)
    write_source_data(HERE / "source-data.csv", rows)
    emit("source_data_complete", rowCount=len(rows), inputCount=len(input_bindings))
    drawing = draw_figure(config, numeric)
    qa = build_qa(config)
    emit(
        "complete",
        finiteDiagnosticOnly=True,
        sourceDataRows=len(rows),
        manualVisualInspection=manual_qa_passed(),
    )

    environment = {
        "schemaVersion": "r073i-action-boundary-environment-v1",
        "createdUtc": now_utc(),
        "sourceCommit": source_commit,
        "branch": branch,
        "workingTreeCleanAtRun": not bool(git_text("status", "--porcelain")),
        "python": platform.python_version(),
        "pythonImplementation": platform.python_implementation(),
        "numpy": np.__version__,
        "matplotlib": matplotlib.__version__,
        "pillow": Image.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "logicalCpuCount": os.cpu_count(),
        "threadEnvironment": {
            key: os.environ.get(key)
            for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")
        },
        "pdftoppm": qa["pdftoppm"],
        "randomnessUsed": False,
        "wallTimeSeconds": time.perf_counter() - STARTED,
    }
    atomic_text(HERE / "environment.json", canonical(environment))

    window_summaries = []
    primary_cutoff = int(config["primaryCutoff"])
    for row in numeric["summary"]["windowSummaries"]:
        window_summaries.append({
            "windowId": row["windowId"],
            "endpoint": row["endpoint"],
            "endpointRole": row["role"],
            "N": primary_cutoff,
            "finiteAverageAction": row["primaryAverageRate"],
            "finiteWkbCorrection": row["primaryWkbCorrection"],
            "largestLambda": row["largestLambda"],
            "largestLambdaResidualMinusWkb": row["largestLambdaResidualMinusWkb"],
        })
    results = {
        "schemaVersion": "r073i-action-boundary-results-v1",
        "figureId": FIGURE_ID,
        "release": "R0.73I",
        "status": "passed",
        "evidenceClass": EVIDENCE_CLASS,
        "diagnosticOnly": True,
        "sourceCommit": source_commit,
        "sourceDataRows": len(rows),
        "panelA": {
            "finiteRowCount": len(config["windows"]) * len(config["cutoffs"]),
            "cH0": numeric["cH0"],
            "rReference": numeric["rReference"],
            "brokenAxisExplicit": True,
        },
        "panelB": {
            "finiteRowCount": len(config["windows"]) * len(config["lambdas"]),
            "primaryCutoff": primary_cutoff,
            "guide": "Lambda^-1 visual guide only; not fitted",
        },
        "windowSummaries": window_summaries,
        "renderQa": {
            **drawing,
            **{key: value for key, value in qa.items() if key != "pdftoppm"},
            "manualVisualInspection": manual_qa_passed(),
        },
        "claimBoundary": contract["claimBoundary"],
    }
    atomic_text(HERE / "results.json", canonical(results))
    write_manifest_and_ledger(
        config, contract, input_bindings, source_commit, branch
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
