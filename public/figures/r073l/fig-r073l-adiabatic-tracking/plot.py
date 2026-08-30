#!/usr/bin/env python3
"""Render the formal R0.73L finite adiabatic-tracking figure."""

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
import resource
import sys
import time


def bootstrap() -> None:
    for index, value in enumerate(sys.argv):
        if value == "--deps" and index + 1 < len(sys.argv):
            sys.path.insert(0, str(Path(sys.argv[index + 1]).resolve()))
            return
        if value.startswith("--deps="):
            sys.path.insert(0, str(Path(value.split("=", 1)[1]).resolve()))
            return


bootstrap()

import matplotlib as mpl  # noqa: E402

mpl.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Ellipse  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image, ImageOps  # noqa: E402
import pypdfium2 as pdfium  # noqa: E402


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PRIMARY = ROOT / "experiments/r073l/adiabatic_diagnostic.json"
INDEPENDENT = ROOT / "experiments/r073l/independent_validation.json"
EXPERIMENT_CONFIG = ROOT / "experiments/r073l/config.json"
EXPERIMENT_ENVIRONMENT = ROOT / "experiments/r073l/environment.json"
PACKAGE_VALIDATION = ROOT / "experiments/r073l/package_validation.json"
PRIMARY_PROGRESS = ROOT / "experiments/r073l/progress.ndjson"
PRIMARY_RESOURCES = ROOT / "experiments/r073l/resources.ndjson"
INDEPENDENT_PROGRESS = ROOT / "experiments/r073l/independent_progress.ndjson"
INDEPENDENT_RESOURCES = ROOT / "experiments/r073l/independent_resources.ndjson"
INPUTS = (
    PRIMARY, INDEPENDENT, EXPERIMENT_CONFIG, EXPERIMENT_ENVIRONMENT,
    PACKAGE_VALIDATION, PRIMARY_PROGRESS, PRIMARY_RESOURCES,
    INDEPENDENT_PROGRESS, INDEPENDENT_RESOURCES,
)
START = time.monotonic()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError("JSON root is not an object: " + str(path))
    return value


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024.0 * 1024.0) if sys.platform == "darwin" else value / 1024.0


class Monitor:
    def __init__(self) -> None:
        self.progress = HERE / "progress.ndjson"
        self.resources = HERE / "resource-log.ndjson"
        self.progress.write_text("", encoding="utf-8")
        self.resources.write_text("", encoding="utf-8")

    def event(self, stage: str, **fields: object) -> None:
        row = {
            "stage": stage,
            "timestampUtc": utc_now(),
            "elapsedSeconds": time.monotonic() - START,
            **fields,
        }
        with self.progress.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(row, sort_keys=True) + "\n")
        resource_row = {
            "stage": stage,
            "timestampUtc": row["timestampUtc"],
            "elapsedSeconds": row["elapsedSeconds"],
            "maximumResidentSetMiB": rss_mib(),
            "processes": 1,
            "gpu": "not used",
        }
        with self.resources.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(resource_row, sort_keys=True) + "\n")


CSV_FIELDS = (
    "record_type", "record_id", "N", "epsilon", "sample_index", "d",
    "slow_fraction", "fast_time", "lambda", "action", "gain",
    "action_normalized_gain", "selected_norm", "complement_norm",
    "complement_to_selected_ratio", "leakage_ratio_over_epsilon",
    "backward_action_residual", "metric", "value", "tolerance",
    "ratio_to_tolerance", "upstream_path", "upstream_sha256",
)


def empty_row(record_type: str, record_id: str) -> dict[str, object]:
    row: dict[str, object] = {field: "" for field in CSV_FIELDS}
    row["record_type"] = record_type
    row["record_id"] = record_id
    return row


def validation_metrics(primary: dict, independent: dict,
                       experiment_config: dict) -> list[dict[str, object]]:
    pmax = primary["maximums"]
    imax = independent["maximums"]
    ptol = experiment_config["tolerances"]
    itol = experiment_config["independentValidation"]["tolerances"]
    return [
        {
            "metric": "cutoff gain", "short": "cutoff\ngain",
            "value": pmax["largestPairTerminalNormalizedGainDifference"],
            "tolerance": ptol["cutoffNormalizedGain"], "group": "cutoff",
        },
        {
            "metric": "cutoff leakage", "short": "cutoff\nleakage",
            "value": pmax["largestPairTerminalLeakageRatioDifference"],
            "tolerance": ptol["cutoffLeakage"], "group": "cutoff",
        },
        {
            "metric": "independent gain", "short": "indep.\ngain",
            "value": imax["finestVsPrimaryNormalizedGain"],
            "tolerance": itol["primaryNormalizedGain"], "group": "independent",
        },
        {
            "metric": "independent leakage", "short": "indep.\nleakage",
            "value": imax["finestVsPrimaryLeakage"],
            "tolerance": itol["primaryLeakage"], "group": "independent",
        },
        {
            "metric": "refinement gain", "short": "refine.\ngain",
            "value": imax["lastTwoNormalizedGain"],
            "tolerance": itol["refinementNormalizedGain"], "group": "refinement",
        },
        {
            "metric": "refinement leakage", "short": "refine.\nleakage",
            "value": imax["lastTwoLeakage"],
            "tolerance": itol["refinementLeakage"], "group": "refinement",
        },
    ]


def source_rows(primary: dict, independent: dict, figure_config: dict,
                experiment_config: dict) -> list[dict[str, object]]:
    display = int(figure_config["displayCutoff"])
    primary_path = str(PRIMARY.relative_to(ROOT))
    primary_hash = sha256(PRIMARY)
    rows: list[dict[str, object]] = []
    cases = [case for case in primary["cases"] if int(case["N"]) == display]
    for case in cases:
        epsilon = float(case["epsilon"])
        for item in case["trajectory"]:
            row = empty_row(
                "display_trajectory",
                f"N{display}-e{epsilon:.10g}-d{int(item['sampleIndex']):02d}",
            )
            row.update({
                "N": display,
                "epsilon": epsilon,
                "sample_index": int(item["sampleIndex"]),
                "d": item["d"],
                "slow_fraction": item["slowFraction"],
                "fast_time": item["fastTime"],
                "lambda": item["lambda"],
                "action": item["action"],
                "gain": item["gain"],
                "action_normalized_gain": item["actionNormalizedGain"],
                "selected_norm": item["selectedNorm"],
                "complement_norm": item["complementNorm"],
                "complement_to_selected_ratio": item[
                    "complementToSelectedRatio"
                ],
                "leakage_ratio_over_epsilon": item["leakageRatioOverEpsilon"],
                "backward_action_residual": item["backwardActionResidual"],
                "upstream_path": primary_path,
                "upstream_sha256": primary_hash,
            })
            rows.append(row)
    for case in primary["cases"]:
        row = empty_row(
            "terminal_case",
            f"N{int(case['N'])}-e{float(case['epsilon']):.10g}",
        )
        summary = case["summary"]
        row.update({
            "N": int(case["N"]),
            "epsilon": case["epsilon"],
            "action": summary["terminalAction"],
            "gain": summary["terminalGain"],
            "action_normalized_gain": summary[
                "terminalActionNormalizedGain"
            ],
            "complement_to_selected_ratio": summary[
                "terminalComplementToSelectedRatio"
            ],
            "leakage_ratio_over_epsilon": summary[
                "terminalLeakageRatioOverEpsilon"
            ],
            "upstream_path": primary_path,
            "upstream_sha256": primary_hash,
        })
        rows.append(row)
    independent_path = str(INDEPENDENT.relative_to(ROOT))
    independent_hash = sha256(INDEPENDENT)
    for item in validation_metrics(primary, independent, experiment_config):
        row = empty_row("validation_metric", str(item["metric"]))
        ratio = float(item["value"]) / float(item["tolerance"])
        upstream_path = (
            primary_path if item["group"] == "cutoff" else independent_path
        )
        upstream_hash = (
            primary_hash if item["group"] == "cutoff" else independent_hash
        )
        row.update({
            "metric": item["metric"],
            "value": item["value"],
            "tolerance": item["tolerance"],
            "ratio_to_tolerance": ratio,
            "upstream_path": upstream_path,
            "upstream_sha256": upstream_hash,
        })
        rows.append(row)
    return rows


def write_source_data(rows: list[dict[str, object]]) -> None:
    with (HERE / "source-data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def style_axes(axis: plt.Axes, palette: dict[str, str]) -> None:
    axis.set_facecolor(palette["paper"])
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["left"].set_color(palette["ink"])
    axis.spines["bottom"].set_color(palette["ink"])
    axis.tick_params(colors=palette["ink"], labelsize=7, width=0.7)
    axis.grid(axis="y", color=palette["lightGrey"], linewidth=0.55, alpha=0.8)
    axis.set_axisbelow(True)
    axis.title.set_color(palette["ink"])


def add_blossom(figure: plt.Figure, palette: dict[str, str]) -> None:
    center = (0.963, 0.958)
    for angle in range(0, 360, 72):
        theta = math.radians(angle)
        petal = Ellipse(
            (center[0] + 0.011 * math.cos(theta),
             center[1] + 0.011 * math.sin(theta)),
            width=0.014,
            height=0.006,
            angle=angle,
            facecolor=palette["blueOpen"],
            edgecolor=palette["blueDark"],
            linewidth=0.45,
            transform=figure.transFigure,
            zorder=20,
        )
        figure.add_artist(petal)
    figure.text(center[0], center[1], "·", ha="center", va="center",
                color=palette["gold"], fontsize=8, zorder=21)


def render(primary: dict, independent: dict, config: dict,
           experiment_config: dict) -> dict[str, object]:
    palette = config["palette"]
    width = float(config["widthMillimetres"]) / 25.4
    height = float(config["heightMillimetres"]) / 25.4
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 7.5,
        "axes.linewidth": 0.7,
        "lines.linewidth": 1.25,
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
    })
    figure, axes = plt.subplots(2, 2, figsize=(width, height), facecolor=palette["paper"])
    figure.subplots_adjust(left=0.09, right=0.975, bottom=0.105, top=0.855,
                           wspace=0.33, hspace=0.44)
    figure.text(0.09, 0.952, "R0.73L finite adiabatic tracking diagnostic",
                ha="left", va="top", fontsize=11.2, fontweight="semibold",
                color=palette["ink"])
    figure.text(
        0.09, 0.912,
        "Complete slow window d ∈ [0, 1/450] · finite Fourier evidence · focused scales declared",
        ha="left", va="top", fontsize=7.2, color=palette["midGrey"],
    )
    add_blossom(figure, palette)

    display = int(config["displayCutoff"])
    compare = int(config["comparisonCutoff"])
    epsilon_order = [float(value) for value in config["epsilonOrder"]]
    colors = [
        palette["blueOpen"], palette["blueLight"], palette["blueMid"],
        palette["blue"], palette["blueDark"],
    ]
    epsilon_labels = [
        r"$10^{-3}$", r"$5\!\times\!10^{-4}$",
        r"$2.5\!\times\!10^{-4}$", r"$1.25\!\times\!10^{-4}$",
        r"$6.25\!\times\!10^{-5}$",
    ]
    linestyles = [(0, (1, 1)), (0, (4, 2)), "-.", "--", "-"]
    markers = ["D", "s", "^", "o", "o"]
    cases = {
        (int(case["N"]), float(case["epsilon"])): case
        for case in primary["cases"]
    }

    axis = axes[0, 0]
    style_axes(axis, palette)
    for epsilon, epsilon_label, color, linestyle, marker in zip(
        epsilon_order, epsilon_labels, colors, linestyles, markers
    ):
        trajectory = cases[(display, epsilon)]["trajectory"]
        axis.plot(
            [row["slowFraction"] for row in trajectory],
            [row["actionNormalizedGain"] for row in trajectory],
            color=color, linestyle=linestyle, marker=marker,
            markevery=16, markersize=3.0,
            markerfacecolor=(palette["paper"] if epsilon >= 0.00025 else color),
            markeredgecolor=palette["blueDark"], markeredgewidth=0.55,
            label=epsilon_label,
        )
    axis.axhline(1.0, color=palette["midGrey"], linestyle=(0, (3, 2)),
                 linewidth=0.8, label="benchmark 1")
    axis.set_xlim(0.0, 1.0)
    axis.set_ylim(0.99920, 1.000035)
    axis.set_xlabel("slow fraction  d / D*", color=palette["ink"])
    axis.set_ylabel(r"$G_N(d)\,e^{-\Phi_N(d)}$", color=palette["ink"])
    axis.set_title("(a) Action-normalized gain", loc="left", fontsize=8.5,
                   pad=5, fontweight="semibold")
    axis.text(0.98, 0.94, "focused vertical scale", transform=axis.transAxes,
              ha="right", va="top", fontsize=6.5,
              color=palette["midGrey"])
    handles, labels = axis.get_legend_handles_labels()
    legend_order = [0, 3, 1, 4, 2, 5]
    axis.legend(
        [handles[index] for index in legend_order],
        [labels[index] for index in legend_order],
        title=r"$\varepsilon$", ncol=3, frameon=False, fontsize=5.6,
        title_fontsize=6.2, loc="lower left", handlelength=1.8,
        columnspacing=0.55, handletextpad=0.35,
    )

    axis = axes[0, 1]
    style_axes(axis, palette)
    for cutoff, marker, filled, color, linestyle in (
        (compare, "s", False, palette["blueMid"], "--"),
        (display, "o", True, palette["blueDark"], "-"),
    ):
        eps_sorted = sorted(epsilon_order)
        leakage = [
            cases[(cutoff, epsilon)]["summary"][
                "terminalComplementToSelectedRatio"
            ]
            for epsilon in eps_sorted
        ]
        axis.loglog(
            eps_sorted, leakage, color=color,
            marker=marker,
            markersize=(5.5 if cutoff == compare else 3.5),
            linewidth=(1.0 if cutoff == compare else 1.2),
            markerfacecolor=(color if filled else palette["paper"]),
            markeredgecolor=color, linestyle=linestyle, label=f"N={cutoff}",
        )
    eps_sorted = np.array(sorted(epsilon_order), dtype=float)
    smallest = float(eps_sorted[0])
    anchor = cases[(display, smallest)]["summary"][
        "terminalComplementToSelectedRatio"
    ]
    reference = anchor * eps_sorted / smallest
    axis.loglog(eps_sorted, reference, color=palette["gold"],
                linestyle="--", linewidth=1.0, label=r"$O(\varepsilon)$")
    tail_slope = primary["epsilonScalingByCutoff"][str(display)][
        "terminalLeakageTailThreeLogLogSlope"
    ]
    axis.text(0.05, 0.08, f"tail-3 slope = {tail_slope:.3f}",
              transform=axis.transAxes, fontsize=6.7, color=palette["ink"])
    axis.set_xlabel(r"$\varepsilon$", color=palette["ink"])
    axis.set_ylabel(r"terminal  $\|Q_Nu\|/\|P_Nu\|$", color=palette["ink"])
    axis.set_title("(b) Terminal complementary leakage", loc="left",
                   fontsize=8.5, pad=5, fontweight="semibold")
    axis.legend(frameon=False, fontsize=6.4, loc="upper left")

    axis = axes[1, 0]
    style_axes(axis, palette)
    for epsilon, color, linestyle, marker in zip(
        epsilon_order, colors, linestyles, markers
    ):
        trajectory = cases[(display, epsilon)]["trajectory"]
        axis.plot(
            [row["slowFraction"] for row in trajectory],
            [row["backwardActionResidual"] for row in trajectory],
            color=color, linestyle=linestyle, marker=marker,
            markevery=16, markersize=2.8,
            markerfacecolor=(palette["paper"] if epsilon >= 0.00025 else color),
            markeredgecolor=palette["blueDark"], markeredgewidth=0.5,
        )
    axis.axhline(0.0, color=palette["midGrey"], linestyle=(0, (3, 2)),
                 linewidth=0.8)
    axis.set_xlim(0.0, 1.0)
    axis.ticklabel_format(axis="y", style="sci", scilimits=(-3, -3))
    axis.set_xlabel("slow fraction  d / D*", color=palette["ink"])
    axis.set_ylabel("backward-action residual", color=palette["ink"])
    axis.set_title("(c) Forward-orbit localization residual", loc="left",
                   fontsize=8.5, pad=5, fontweight="semibold")
    axis.text(0.02, 0.09, "computed from one forward orbit",
              transform=axis.transAxes, fontsize=6.5,
              color=palette["midGrey"])

    axis = axes[1, 1]
    style_axes(axis, palette)
    metrics = validation_metrics(primary, independent, experiment_config)
    x = np.arange(len(metrics))
    ratios = np.array([
        float(item["value"]) / float(item["tolerance"]) for item in metrics
    ])
    marker_list = ["o", "s", "o", "s", "^", "D"]
    color_list = [
        palette["blue"], palette["blue"], palette["gold"], palette["gold"],
        palette["blueDark"], palette["blueDark"],
    ]
    for index, (ratio, marker, color) in enumerate(
        zip(ratios, marker_list, color_list)
    ):
        axis.plot(index, ratio, marker=marker, markersize=5.0,
                  markerfacecolor=(palette["paper"] if index % 2 else color),
                  markeredgecolor=color, markeredgewidth=0.9,
                  linestyle="none")
        axis.vlines(index, max(ratio, 1e-12), 1.0, color=palette["lightGrey"],
                    linewidth=0.7, zorder=0)
    axis.axhline(1.0, color=palette["midGrey"], linestyle="--", linewidth=0.9)
    axis.set_yscale("log")
    axis.set_ylim(1e-12, 2.5)
    axis.set_xticks(x, [item["short"] for item in metrics])
    axis.tick_params(axis="x", labelsize=6.0)
    axis.set_ylabel("maximum discrepancy / tolerance", color=palette["ink"])
    axis.set_title("(d) Validation margins", loc="left", fontsize=8.5,
                   pad=5, fontweight="semibold")
    axis.text(0.98, 0.93, "fail threshold", transform=axis.transAxes,
              ha="right", va="top", fontsize=6.5, color=palette["midGrey"])

    png_dpi = int(config["pngDpi"])
    figure.savefig(HERE / "figure.pdf", facecolor=palette["paper"])
    figure.savefig(HERE / "figure.svg", facecolor=palette["paper"])
    figure.savefig(HERE / "figure.png", dpi=png_dpi,
                   facecolor=palette["paper"])
    plt.close(figure)

    qa_dpi = int(config["qaDpi"])
    with Image.open(HERE / "figure.png") as image:
        target = (
            round(float(config["widthMillimetres"]) / 25.4 * qa_dpi),
            round(float(config["heightMillimetres"]) / 25.4 * qa_dpi),
        )
        final_size = image.convert("RGB").resize(target, Image.Resampling.LANCZOS)
        final_size.save(HERE / "qa-final-size.png", dpi=(qa_dpi, qa_dpi))
        ImageOps.grayscale(final_size).save(
            HERE / "qa-grayscale.png", dpi=(qa_dpi, qa_dpi)
        )
    document = pdfium.PdfDocument(str(HERE / "figure.pdf"))
    page = document[0]
    rendered = page.render(scale=qa_dpi / 72.0).to_pil().convert("RGB")
    rendered.save(HERE / "qa-pdf.png", dpi=(qa_dpi, qa_dpi))
    document.close()

    return {
        "displayCutoff": display,
        "comparisonCutoff": compare,
        "epsilonLevels": epsilon_order,
        "tailThreeLeakageSlope": float(tail_slope),
        "terminalNormalizedGainRange": primary["epsilonScalingByCutoff"][
            str(display)
        ]["terminalNormalizedGainRange"],
        "maximumBackwardActionResidualAbs": primary["maximums"][
            "backwardActionResidualAbs"
        ],
        "validationMetrics": [
            {
                "metric": item["metric"],
                "value": item["value"],
                "tolerance": item["tolerance"],
                "ratioToTolerance": (
                    float(item["value"]) / float(item["tolerance"])
                ),
            }
            for item in metrics
        ],
    }


def main() -> int:
    parse_args()
    monitor = Monitor()
    monitor.event("start")
    for path in INPUTS:
        if not path.is_file():
            raise RuntimeError("missing figure input: " + str(path))
    primary = load_json(PRIMARY)
    independent = load_json(INDEPENDENT)
    config = load_json(HERE / "config.json")
    experiment_config = load_json(EXPERIMENT_CONFIG)
    if primary.get("status") != "passed" or independent.get("status") != "passed":
        raise RuntimeError("upstream diagnostic package did not pass")
    monitor.event("inputs-validated", files=len(INPUTS))
    rows = source_rows(primary, independent, config, experiment_config)
    write_source_data(rows)
    monitor.event("source-data-written", rows=len(rows))
    summary = render(primary, independent, config, experiment_config)
    monitor.event("exports-rendered")
    environment = {
        "schemaVersion": "r073l-figure-environment-v1",
        "createdUtc": utc_now(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "matplotlib": mpl.__version__,
        "numpy": np.__version__,
        "inputs": [
            {
                "path": str(path.relative_to(ROOT)),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in INPUTS
        ],
        "gpu": "not used",
    }
    (HERE / "environment.json").write_text(canonical(environment), encoding="utf-8")
    results = {
        "schemaVersion": "r073l-figure-results-v1",
        "createdUtc": utc_now(),
        "status": "rendered",
        "sourceRows": len(rows),
        "summary": summary,
        "claimBoundary": {
            "formalValidatedDiagnosticFigure": True,
            "finiteDimensionalDiagnostic": True,
            "independentFiniteRecomputationPassed": True,
            "continuumAdiabaticTheoremCertifiedByFigure": False,
            "explicitContinuumEpsilonThresholdCertified": False,
            "prefactorLimitCertified": False,
            "nonlinearNavierStokesCertified": False,
            "transverseThreeDimensionalClosureCertified": False,
            "finiteTimeSingularityCertified": False,
            "clayProblemSolved": False,
        },
    }
    (HERE / "results.json").write_text(canonical(results), encoding="utf-8")
    monitor.event("complete", sourceRows=len(rows))
    print(json.dumps({"event": "rendered", "sourceRows": len(rows)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
