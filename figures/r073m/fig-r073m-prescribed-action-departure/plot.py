#!/usr/bin/env python3
"""Render the formal R0.73M prescribed-action finite diagnostic figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import platform
from pathlib import Path
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
CERTIFICATE_DIR = ROOT / "research/certificates/r073m"
PRIMARY = CERTIFICATE_DIR / "primary_results.json"
INDEPENDENT_LINEAR = CERTIFICATE_DIR / "independent_linear.json"
INDEPENDENT_HIERARCHY = CERTIFICATE_DIR / "independent_hierarchy.json"
EXPERIMENT_CONFIG = CERTIFICATE_DIR / "config.json"
CERTIFICATE = CERTIFICATE_DIR / "certificate.json"
PACKAGE_VALIDATION = CERTIFICATE_DIR / "validation.json"
PACKAGE_MANIFEST = CERTIFICATE_DIR / "manifest.json"
INPUTS = (
    PRIMARY,
    INDEPENDENT_LINEAR,
    INDEPENDENT_HIERARCHY,
    EXPERIMENT_CONFIG,
    CERTIFICATE,
    PACKAGE_VALIDATION,
    PACKAGE_MANIFEST,
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
    "record_type",
    "record_id",
    "N",
    "epsilon",
    "finite_inviscid_action_proxy",
    "actual_physical_linear_gain",
    "finite_inviscid_action_prefactor",
    "a_endpoint_l2",
    "b_endpoint_l2",
    "b_over_epsilon",
    "c_target_endpoint_l2",
    "c_target_over_epsilon_squared",
    "c_mean_path_signed_parallel",
    "c_mean_path_signed_parallel_over_epsilon_squared",
    "c_double_path_signed_parallel",
    "c_double_path_signed_parallel_over_epsilon_squared",
    "gate_family",
    "metric",
    "value",
    "tolerance",
    "ratio_to_tolerance",
    "is_family_max",
    "upstream_path",
    "upstream_sha256",
)


def empty_row(record_type: str, record_id: str) -> dict[str, object]:
    row: dict[str, object] = {field: "" for field in CSV_FIELDS}
    row["record_type"] = record_type
    row["record_id"] = record_id
    return row


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def gate_components(
    primary: dict,
    independent_linear: dict,
    independent_hierarchy: dict,
    experiment_config: dict,
) -> list[dict[str, object]]:
    pmax = primary["maximums"]
    lmax = independent_linear["maximums"]
    tolerances = experiment_config["tolerances"]
    return [
        {
            "family": "cutoff",
            "metric": "cutoff action proxy",
            "short": "action proxy",
            "value": pmax["largestCutoffActionProxyAbsolute"],
            "tolerance": tolerances["largestCutoffActionProxyAbsolute"],
            "path": PRIMARY,
        },
        {
            "family": "cutoff",
            "metric": "cutoff prefactor",
            "short": "prefactor",
            "value": pmax["largestCutoffPrefactorAbsolute"],
            "tolerance": tolerances["largestCutoffPrefactorAbsolute"],
            "path": PRIMARY,
        },
        {
            "family": "cutoff",
            "metric": "cutoff hierarchy observables",
            "short": "hierarchy",
            "value": pmax["hierarchyFinestCutoffRelative"],
            "tolerance": tolerances["hierarchyFinestCutoffRelative"],
            "path": PRIMARY,
        },
        {
            "family": "step",
            "metric": "hierarchy time step",
            "short": "hierarchy",
            "value": pmax["hierarchyStepRelative"],
            "tolerance": tolerances["hierarchyStepRelative"],
            "path": PRIMARY,
        },
        {
            "family": "physical-kinetic",
            "metric": "physical versus kinetic gain",
            "short": "gain",
            "value": pmax["physicalKineticGainRelative"],
            "tolerance": tolerances["physicalKineticGainRelative"],
            "path": PRIMARY,
        },
        {
            "family": "independent",
            "metric": "independent inviscid action",
            "short": "inviscid action",
            "value": lmax["finiteInviscidActionProxyRelative"],
            "tolerance": tolerances["independentLinearActionRelative"],
            "path": INDEPENDENT_LINEAR,
        },
        {
            "family": "independent",
            "metric": "independent viscous action",
            "short": "viscous action",
            "value": lmax["finiteViscousActionRelative"],
            "tolerance": tolerances["independentLinearActionRelative"],
            "path": INDEPENDENT_LINEAR,
        },
        {
            "family": "independent",
            "metric": "independent linear gain",
            "short": "linear gain",
            "value": lmax["gainRelative"],
            "tolerance": tolerances["independentLinearGainRelative"],
            "path": INDEPENDENT_LINEAR,
        },
        {
            "family": "independent",
            "metric": "independent prefactor",
            "short": "prefactor",
            "value": lmax["finiteInviscidActionPrefactorAbsolute"],
            "tolerance": tolerances["independentLinearPrefactorAbsolute"],
            "path": INDEPENDENT_LINEAR,
        },
        {
            "family": "independent",
            "metric": "independent step refinement",
            "short": "refinement",
            "value": lmax["stepRefinement"],
            "tolerance": tolerances["independentLinearRefinement"],
            "path": INDEPENDENT_LINEAR,
        },
        {
            "family": "independent",
            "metric": "independent hierarchy coefficients",
            "short": "hierarchy",
            "value": independent_hierarchy["maximumCoefficientRelativeError"],
            "tolerance": tolerances["independentHierarchyCoefficientRelative"],
            "path": INDEPENDENT_HIERARCHY,
        },
        {
            "family": "independent",
            "metric": "independent forbidden parity",
            "short": "parity",
            "value": independent_hierarchy["maximumForbiddenParityRelative"],
            "tolerance": tolerances["independentHierarchyForbiddenParityRelative"],
            "path": INDEPENDENT_HIERARCHY,
        },
    ]


def source_rows(
    primary: dict,
    independent_linear: dict,
    independent_hierarchy: dict,
    experiment_config: dict,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    primary_path = relative(PRIMARY)
    primary_hash = sha256(PRIMARY)
    for case in primary["cases"]:
        epsilon = float(case["epsilon"])
        hierarchy = case["hierarchy"]
        row = empty_row(
            "finite_case",
            f"N{int(case['N'])}-e{epsilon:.10g}",
        )
        row.update({
            "N": int(case["N"]),
            "epsilon": epsilon,
            "finite_inviscid_action_proxy": case["linear"][
                "finiteInviscidActionProxy"
            ],
            "actual_physical_linear_gain": hierarchy[
                "actualPhysicalLinearGain"
            ],
            "finite_inviscid_action_prefactor": case[
                "finiteInviscidActionPrefactor"
            ],
            "a_endpoint_l2": hierarchy["aEndpointL2"],
            "b_endpoint_l2": hierarchy["bEndpointL2"],
            "b_over_epsilon": hierarchy["bEndpointL2"] / epsilon,
            "c_target_endpoint_l2": hierarchy["cTargetEndpointL2"],
            "c_target_over_epsilon_squared": (
                hierarchy["cTargetEndpointL2"] / epsilon**2
            ),
            "c_mean_path_signed_parallel": hierarchy[
                "cMeanPathSignedParallel"
            ],
            "c_mean_path_signed_parallel_over_epsilon_squared": (
                hierarchy["cMeanPathSignedParallel"] / epsilon**2
            ),
            "c_double_path_signed_parallel": hierarchy[
                "cDoublePathSignedParallel"
            ],
            "c_double_path_signed_parallel_over_epsilon_squared": (
                hierarchy["cDoublePathSignedParallel"] / epsilon**2
            ),
            "upstream_path": primary_path,
            "upstream_sha256": primary_hash,
        })
        rows.append(row)

    components = gate_components(
        primary, independent_linear, independent_hierarchy, experiment_config
    )
    maxima = {
        family: max(
            float(item["value"]) / float(item["tolerance"])
            for item in components
            if item["family"] == family
        )
        for family in {str(item["family"]) for item in components}
    }
    for item in components:
        ratio = float(item["value"]) / float(item["tolerance"])
        path = item["path"]
        row = empty_row(
            "gate_component",
            str(item["family"]) + "-" + str(item["metric"]),
        )
        row.update({
            "gate_family": item["family"],
            "metric": item["metric"],
            "value": item["value"],
            "tolerance": item["tolerance"],
            "ratio_to_tolerance": ratio,
            "is_family_max": str(math.isclose(
                ratio, maxima[str(item["family"])], rel_tol=0.0, abs_tol=0.0
            )).lower(),
            "upstream_path": relative(path),
            "upstream_sha256": sha256(path),
        })
        rows.append(row)
    return rows, components


def write_source_data(rows: list[dict[str, object]]) -> None:
    with (HERE / "source-data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def style_axes(axis: plt.Axes, palette: dict[str, str]) -> None:
    axis.set_facecolor(palette["paper"])
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["left"].set_color(palette["ink"])
    axis.spines["bottom"].set_color(palette["ink"])
    axis.tick_params(colors=palette["ink"], labelsize=6.6, width=0.7)
    axis.grid(axis="y", color=palette["lightGrey"], linewidth=0.55, alpha=0.8)
    axis.set_axisbelow(True)
    axis.title.set_color(palette["ink"])


def add_blossom(figure: plt.Figure, palette: dict[str, str]) -> None:
    center = (0.963, 0.958)
    for angle in range(0, 360, 72):
        theta = math.radians(angle)
        petal = Ellipse(
            (
                center[0] + 0.011 * math.cos(theta),
                center[1] + 0.011 * math.sin(theta),
            ),
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
    figure.text(
        center[0], center[1], "·", ha="center", va="center",
        color=palette["gold"], fontsize=8, zorder=21,
    )


def epsilon_axis(axis: plt.Axes, epsilon_order: list[float]) -> None:
    values = sorted(epsilon_order)
    labels = [
        r"$6.25\!\times\!10^{-5}$",
        r"$1.25\!\times\!10^{-4}$",
        r"$2.5\!\times\!10^{-4}$",
        r"$5\!\times\!10^{-4}$",
        r"$10^{-3}$",
    ]
    axis.set_xscale("log")
    axis.set_xlim(values[0] / 1.18, values[-1] * 1.18)
    axis.set_xticks(values, labels)
    axis.get_xaxis().set_minor_locator(mpl.ticker.NullLocator())
    axis.tick_params(axis="x", labelsize=5.7, pad=2)
    axis.set_xlabel(r"viscous parameter  $\varepsilon$", color="#1f2933")


def render(
    primary: dict,
    independent_linear: dict,
    independent_hierarchy: dict,
    config: dict,
    experiment_config: dict,
) -> dict[str, object]:
    palette = config["palette"]
    width = float(config["widthMillimetres"]) / 25.4
    height = float(config["heightMillimetres"]) / 25.4
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 7.5,
        "axes.linewidth": 0.7,
        "lines.linewidth": 1.2,
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
    })
    figure, axes = plt.subplots(
        2, 2, figsize=(width, height), facecolor=palette["paper"]
    )
    figure.subplots_adjust(
        left=0.09, right=0.975, bottom=0.11, top=0.855,
        wspace=0.32, hspace=0.47,
    )
    figure.text(
        0.09, 0.952, "R0.73M finite prescribed-action recoding diagnostic",
        ha="left", va="top", fontsize=11.2, fontweight="semibold",
        color=palette["ink"],
    )
    figure.text(
        0.09, 0.912,
        r"15 finite cases · $N=40,48,64$ · $6.25\!\times\!10^{-5}\leq\varepsilon\leq10^{-3}$ · focused scales declared",
        ha="left", va="top", fontsize=7.2, color=palette["midGrey"],
    )
    add_blossom(figure, palette)

    epsilon_order = [float(value) for value in config["epsilonOrder"]]
    eps_sorted = sorted(epsilon_order)
    cases = {
        (int(case["N"]), float(case["epsilon"])): case
        for case in primary["cases"]
    }

    axis = axes[0, 0]
    style_axes(axis, palette)
    cutoff_styles = [
        (40, palette["blueLight"], (0, (1, 1)), "s", 7.0, False, 1),
        (48, palette["blueMid"], "--", "D", 5.2, False, 2),
        (64, palette["blueDark"], "-", "o", 2.9, True, 3),
    ]
    for cutoff, color, linestyle, marker, size, filled, zorder in cutoff_styles:
        values = [
            cases[(cutoff, epsilon)]["finiteInviscidActionPrefactor"]
            for epsilon in eps_sorted
        ]
        axis.plot(
            eps_sorted,
            values,
            color=color,
            linestyle=linestyle,
            marker=marker,
            markersize=size,
            markerfacecolor=(color if filled else palette["paper"]),
            markeredgecolor=color,
            markeredgewidth=0.8,
            label=f"N={cutoff}",
            zorder=zorder,
        )
    axis.axhline(
        1.0, color=palette["midGrey"], linestyle=(0, (3, 2)),
        linewidth=0.8, label="benchmark 1",
    )
    axis.set_ylim(0.99592, 1.00018)
    epsilon_axis(axis, epsilon_order)
    axis.set_ylabel(r"$g^{(0)}_{N,\varepsilon}$", color=palette["ink"])
    axis.set_title(
        "(a) Finite action-normalized gain", loc="left", fontsize=8.5,
        pad=5, fontweight="semibold",
    )
    axis.text(
        0.98, 0.94, "focused vertical scale", transform=axis.transAxes,
        ha="right", va="top", fontsize=6.3, color=palette["midGrey"],
    )
    axis.text(
        0.03, 0.10, "cutoffs coincide to plotting precision",
        transform=axis.transAxes, ha="left", va="bottom", fontsize=6.2,
        color=palette["midGrey"],
    )
    axis.legend(
        frameon=False, fontsize=5.8, loc="center left", ncol=2,
        handlelength=1.7, columnspacing=0.7, handletextpad=0.35,
    )

    display = int(config["displayCutoff"])
    axis = axes[0, 1]
    style_axes(axis, palette)
    b_scaled = [
        cases[(display, epsilon)]["hierarchy"]["bEndpointL2"] / epsilon
        for epsilon in eps_sorted
    ]
    c_scaled = [
        cases[(display, epsilon)]["hierarchy"]["cTargetEndpointL2"] / epsilon**2
        for epsilon in eps_sorted
    ]
    axis.plot(
        eps_sorted, b_scaled, color=palette["blueDark"], linestyle="-",
        marker="o", markersize=4.1, markerfacecolor=palette["blueDark"],
        markeredgecolor=palette["blueDark"],
        label=r"$\|b_N\|/\varepsilon$",
    )
    axis.plot(
        eps_sorted, c_scaled, color=palette["gold"], linestyle="--",
        marker="s", markersize=4.5, markerfacecolor=palette["paper"],
        markeredgecolor=palette["gold"], markeredgewidth=0.9,
        label=r"$\|\Pi_{\pm1}c_N\|/\varepsilon^2$",
    )
    axis.axhline(
        1.0, color=palette["midGrey"], linestyle=(0, (3, 2)), linewidth=0.8,
    )
    axis.set_ylim(0.0, 1.06)
    epsilon_axis(axis, epsilon_order)
    axis.set_ylabel("registered coefficient ratio", color=palette["ink"])
    axis.set_title(
        "(b) Second- and third-order recoding", loc="left", fontsize=8.5,
        pad=5, fontweight="semibold",
    )
    axis.text(
        0.97, 0.91, "finite grid · no limit fit", transform=axis.transAxes,
        ha="right", va="top", fontsize=6.2, color=palette["midGrey"],
    )
    axis.legend(
        frameon=False, fontsize=6.2, loc="lower right", handlelength=2.0,
    )

    axis = axes[1, 0]
    style_axes(axis, palette)
    mean_scaled = [
        cases[(display, epsilon)]["hierarchy"]["cMeanPathSignedParallel"]
        / epsilon**2
        for epsilon in eps_sorted
    ]
    double_scaled = [
        cases[(display, epsilon)]["hierarchy"]["cDoublePathSignedParallel"]
        / epsilon**2
        for epsilon in eps_sorted
    ]
    axis.plot(
        eps_sorted, mean_scaled, color=palette["blueDark"], linestyle="-",
        marker="o", markersize=4.1, markerfacecolor=palette["blueDark"],
        markeredgecolor=palette["blueDark"], label="mean-mediated path",
    )
    axis.plot(
        eps_sorted, double_scaled, color=palette["gold"], linestyle="--",
        marker="s", markersize=4.5, markerfacecolor=palette["paper"],
        markeredgecolor=palette["gold"], markeredgewidth=0.9,
        label="doubled-harmonic path",
    )
    axis.axhline(
        0.0, color=palette["midGrey"], linestyle=(0, (3, 2)), linewidth=0.8,
    )
    axis.set_ylim(-0.58, 0.035)
    epsilon_axis(axis, epsilon_order)
    axis.set_ylabel(r"signed alignment $/\,\varepsilon^2$", color=palette["ink"])
    axis.set_title(
        "(c) Signed cubic path alignment", loc="left", fontsize=8.5,
        pad=5, fontweight="semibold",
    )
    axis.text(
        0.97, 0.91, "sign retained · no absolute value",
        transform=axis.transAxes, ha="right", va="top", fontsize=6.2,
        color=palette["midGrey"],
    )
    axis.legend(
        frameon=False, fontsize=6.0, loc="lower right", handlelength=2.0,
    )

    axis = axes[1, 1]
    style_axes(axis, palette)
    components = gate_components(
        primary, independent_linear, independent_hierarchy, experiment_config
    )
    family_order = [str(value) for value in config["gateFamilyOrder"]]
    family_maxima = []
    family_winners = []
    for family in family_order:
        candidates = [
            item for item in components if str(item["family"]) == family
        ]
        winner = max(
            candidates,
            key=lambda item: float(item["value"]) / float(item["tolerance"]),
        )
        family_winners.append(winner)
        family_maxima.append(
            float(winner["value"]) / float(winner["tolerance"])
        )
    x = np.arange(len(family_order))
    colors = [
        palette["blueMid"], palette["blueDark"],
        palette["gold"], palette["blue"],
    ]
    markers = ["s", "o", "D", "^"]
    filled = [False, True, False, True]
    for index, (ratio, color, marker, fill) in enumerate(
        zip(family_maxima, colors, markers, filled)
    ):
        axis.plot(
            index, ratio, marker=marker, markersize=5.2,
            markerfacecolor=(color if fill else palette["paper"]),
            markeredgecolor=color, markeredgewidth=0.9, linestyle="none",
            zorder=3,
        )
        axis.vlines(
            index, ratio, 1.0, color=palette["lightGrey"], linewidth=0.75,
            zorder=0,
        )
        label = f"{ratio:.3g}" if ratio >= 1e-3 else f"{ratio:.1e}"
        axis.text(
            index, ratio * 1.65, label, ha="center", va="bottom",
            fontsize=5.8, color=palette["ink"],
        )
    axis.axhline(
        1.0, color=palette["midGrey"], linestyle="--", linewidth=0.9,
    )
    axis.set_yscale("log")
    axis.set_ylim(1e-9, 2.4)
    axis.set_xlim(-0.45, len(family_order) - 0.55)
    axis.set_xticks(
        x,
        ["cutoff", "time step", "physical–\nkinetic", "independent"],
    )
    axis.tick_params(axis="x", labelsize=6.2)
    axis.set_ylabel("family maximum / tolerance", color=palette["ink"])
    axis.set_title(
        "(d) Numerical gate-family maxima", loc="left", fontsize=8.5,
        pad=5, fontweight="semibold",
    )
    axis.text(
        0.98, 0.93, "fail threshold", transform=axis.transAxes,
        ha="right", va="top", fontsize=6.2, color=palette["midGrey"],
    )

    png_dpi = int(config["pngDpi"])
    figure.savefig(HERE / "figure.pdf", facecolor=palette["paper"])
    figure.savefig(HERE / "figure.svg", facecolor=palette["paper"])
    figure.savefig(HERE / "figure.png", dpi=png_dpi, facecolor=palette["paper"])
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

    all_g0 = [
        float(case["finiteInviscidActionPrefactor"])
        for case in primary["cases"]
    ]
    return {
        "displayCutoff": display,
        "cutoffs": [int(value) for value in config["cutoffOrder"]],
        "epsilonLevels": epsilon_order,
        "finiteInviscidActionPrefactorRange": [min(all_g0), max(all_g0)],
        "displayBOverEpsilonRange": [min(b_scaled), max(b_scaled)],
        "displayCTargetOverEpsilonSquaredRange": [min(c_scaled), max(c_scaled)],
        "displayCMeanSignedOverEpsilonSquaredRange": [
            min(mean_scaled), max(mean_scaled)
        ],
        "displayCDoubleSignedOverEpsilonSquaredRange": [
            min(double_scaled), max(double_scaled)
        ],
        "gateFamilyMaximums": [
            {
                "family": family,
                "metric": winner["metric"],
                "value": winner["value"],
                "tolerance": winner["tolerance"],
                "ratioToTolerance": ratio,
            }
            for family, winner, ratio in zip(
                family_order, family_winners, family_maxima
            )
        ],
        "largestGateFamilyRatio": max(family_maxima),
    }


def main() -> int:
    parse_args()
    monitor = Monitor()
    monitor.event("start")
    for path in INPUTS:
        if not path.is_file():
            raise RuntimeError("missing figure input: " + str(path))
    primary = load_json(PRIMARY)
    independent_linear = load_json(INDEPENDENT_LINEAR)
    independent_hierarchy = load_json(INDEPENDENT_HIERARCHY)
    experiment_config = load_json(EXPERIMENT_CONFIG)
    certificate = load_json(CERTIFICATE)
    package_validation = load_json(PACKAGE_VALIDATION)
    package_manifest = load_json(PACKAGE_MANIFEST)
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    required_passes = (
        primary.get("status") == "passed",
        independent_linear.get("status") == "passed",
        independent_hierarchy.get("status") == "passed",
        certificate.get("allChecksPass") is True,
        package_validation.get("allChecksPass") is True,
        package_manifest.get("allPrerequisiteChecksPass") is True,
    )
    if not all(required_passes):
        raise RuntimeError("sealed upstream diagnostic package did not pass")
    if primary.get("smokeMode") or certificate.get("smokeMode"):
        raise RuntimeError("formal figure cannot use smoke-mode inputs")
    monitor.event("inputs-validated", files=len(INPUTS))
    rows, components = source_rows(
        primary, independent_linear, independent_hierarchy, experiment_config
    )
    write_source_data(rows)
    monitor.event("source-data-written", rows=len(rows))
    summary = render(
        primary,
        independent_linear,
        independent_hierarchy,
        config,
        experiment_config,
    )
    monitor.event("exports-rendered")
    environment = {
        "schemaVersion": "r073m-figure-environment-v1",
        "createdUtc": utc_now(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "matplotlib": mpl.__version__,
        "numpy": np.__version__,
        "inputs": [
            {
                "path": relative(path),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in INPUTS
        ],
        "gpu": "not used",
    }
    (HERE / "environment.json").write_text(
        canonical(environment), encoding="utf-8"
    )
    results = {
        "schemaVersion": "r073m-figure-results-v1",
        "createdUtc": utc_now(),
        "status": "rendered",
        "sourceRows": len(rows),
        "finiteCaseRows": len(primary["cases"]),
        "gateComponentRows": len(components),
        "summary": summary,
        "claimBoundary": contract["claimBoundary"],
    }
    (HERE / "results.json").write_text(canonical(results), encoding="utf-8")
    monitor.event("complete", sourceRows=len(rows))
    print(json.dumps({"event": "rendered", "sourceRows": len(rows)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
