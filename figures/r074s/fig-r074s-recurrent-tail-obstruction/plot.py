#!/usr/bin/env python3
"""Render the source-bound R0.74S recurrent-tail analytic figure archive."""

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
FORMULA_SOURCE = "core 7355c01d, equations (S.445)-(S.475)"
PALETTE = {
    "navy": "#244C70",
    "navy_open": "#DCE8F0",
    "orange": "#B45A36",
    "orange_open": "#F3E2D8",
    "charcoal": "#283238",
    "gray": "#737E85",
    "mid_gray": "#AAB2B8",
    "light_gray": "#DDE1E4",
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

    certificate = json.loads(blobs["research/r074s_recurrent_streamline_certificate.json"])
    need(certificate.get("verdict") == "PASS", "main certificate verdict drift")
    need(
        certificate.get("note", {}).get("sha256")
        == source["files"]["research/r074s_recurrent_streamline_temporal_tail_obstruction.md"]["sha256"],
        "certificate-to-note binding drift",
    )
    report = blobs["research/r074s_recurrent_streamline_certificate_report.md"].decode("utf-8")
    note = blobs["research/r074s_recurrent_streamline_temporal_tail_obstruction.md"].decode("utf-8")
    need("**PASS**" in report, "main certificate report status drift")
    need("**(S.444 is false)**" in note and "**NOT CLAY.**" in note, "note claim boundary drift")
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


def stable_period_integrand(phi: Any, np: Any) -> Any:
    """Return ds/dphi for the exact level-set parametrization.

    The factored radicand avoids cancellation at all four turning points.
    Gauss nodes do not include the endpoints themselves.
    """
    scale = math.pi / 3.0
    cosine_phi = np.cos(phi)
    delta = np.where(
        cosine_phi >= 0.0,
        2.0 * np.sin(phi / 2.0) ** 2,
        2.0 * np.cos(phi / 2.0) ** 2,
    )
    nearest_angle = scale * (1.0 - delta)
    cosine_difference = (
        2.0
        * np.sin((nearest_angle + scale) / 2.0)
        * np.sin(scale * delta / 2.0)
    )
    radicand = cosine_difference * (np.cos(nearest_angle) + 0.5)
    need(bool(np.all(radicand > 0.0)), "period integrand lost positivity")
    return scale * np.abs(np.sin(phi)) / np.sqrt(radicand)


def orbit_period(order: int, np: Any) -> float:
    nodes, weights = np.polynomial.legendre.leggauss(order)
    phi = math.pi * (nodes + 1.0)
    return float(math.pi * np.dot(weights, stable_period_integrand(phi, np)))


def velocity(points: Any, np: Any) -> Any:
    x = points[..., 0]
    y = points[..., 1]
    return np.stack((np.sin(x) * np.cos(y), -np.cos(x) * np.sin(y)), axis=-1)


def rk4_orbit(period: float, steps: int, start: Any, np: Any) -> dict[str, Any]:
    step = period / steps
    points = np.empty((steps + 1, 2), dtype=float)
    points[0] = start
    for index in range(steps):
        current = points[index]
        k1 = velocity(current, np)
        k2 = velocity(current + 0.5 * step * k1, np)
        k3 = velocity(current + 0.5 * step * k2, np)
        k4 = velocity(current + step * k3, np)
        points[index + 1] = current + step * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
    times = np.linspace(0.0, period, steps + 1)
    field = velocity(points, np)
    x, y = points[:, 0], points[:, 1]
    g = np.sum(field * field, axis=1)
    grad_g_x = np.sin(2.0 * x) * np.cos(2.0 * y)
    grad_g_y = np.sin(2.0 * y) * np.cos(2.0 * x)
    q = field[:, 0] * grad_g_x + field[:, 1] * grad_g_y
    cumulative_variation = np.concatenate((
        np.array([0.0]), np.cumsum(np.abs(np.diff(g))),
    ))
    return {
        "times": times,
        "points": points,
        "field": field,
        "g": g,
        "q": q,
        "cumulativeVariation": cumulative_variation,
        "step": step,
    }


def exact_level_curve(points: int, np: Any) -> dict[str, Any]:
    phi = np.linspace(0.0, 2.0 * math.pi, points)
    x = math.pi / 2.0 - (math.pi / 3.0) * np.cos(phi)
    lower = np.arcsin(np.clip(1.0 / (2.0 * np.sin(x)), -1.0, 1.0))
    y = np.where(phi <= math.pi, lower, math.pi - lower)
    xy = np.column_stack((x, y))
    field = velocity(xy, np)
    g = np.sum(field * field, axis=1)
    return {"phi": phi, "points": xy, "field": field, "g": g}


def generate_payload(config: dict[str, Any], np: Any) -> tuple[list[dict[str, str]], dict[str, Any], dict[str, Any]]:
    orbit_config = config["orbit"]
    period = orbit_period(int(orbit_config["periodQuadratureOrder"]), np)
    reference_period = orbit_period(int(orbit_config["periodQuadratureReferenceOrder"]), np)
    start = np.asarray(orbit_config["witnessStart"], dtype=float)
    high = np.asarray(orbit_config["witnessHigh"], dtype=float)
    orbit = rk4_orbit(period, int(orbit_config["rk4StepsPerPeriod"]), start, np)
    level_curve = exact_level_curve(int(orbit_config["levelSetPoints"]), np)

    points = orbit["points"]
    g = orbit["g"]
    q = orbit["q"]
    times = orbit["times"]
    cumulative = orbit["cumulativeVariation"]
    step = orbit["step"]
    level_residual = np.abs(np.sin(points[:, 0]) * np.sin(points[:, 1]) - 0.5)
    analytic_level_residual = np.abs(
        np.sin(level_curve["points"][:, 0]) * np.sin(level_curve["points"][:, 1]) - 0.5
    )
    q_central = (g[2:] - g[:-2]) / (2.0 * step)
    high_index = int(np.argmin(np.linalg.norm(points - high, axis=1)))
    variation = float(cumulative[-1])
    increment_minimum = float(np.min(np.diff(cumulative)))
    audit = {
        "checksPassed": True,
        "period": period,
        "periodReference": reference_period,
        "periodQuadratureDifference": abs(period - reference_period),
        "rk4Step": step,
        "rk4StepsPerPeriod": int(orbit_config["rk4StepsPerPeriod"]),
        "closureErrorL2": float(np.linalg.norm(points[-1] - start)),
        "maximumRk4LevelResidual": float(np.max(level_residual)),
        "maximumAnalyticLevelResidual": float(np.max(analytic_level_residual)),
        "gMinimum": float(np.min(g)),
        "gMaximum": float(np.max(g)),
        "gMinimumError": abs(float(np.min(g)) - 0.5),
        "gMaximumError": abs(float(np.max(g)) - 0.75),
        "endpointGDrift": abs(float(g[-1] - g[0])),
        "endpointQDrift": abs(float(q[-1] - q[0])),
        "maximumCentralDerivativeError": float(np.max(np.abs(q_central - q[1:-1]))),
        "onePeriodAbsoluteVariation": variation,
        "onePeriodVariationError": abs(variation - 2.0),
        "signedOnePeriodDrift": abs(float(g[-1] - g[0])),
        "minimumCumulativeVariationIncrement": increment_minimum,
        "highWitnessNearestTimeFraction": float(times[high_index] / period),
        "highWitnessPositionErrorL2": float(np.linalg.norm(points[high_index] - high)),
        "tolerances": {
            "periodQuadratureDifference": 5.0e-11,
            "closureErrorL2": 1.0e-11,
            "levelResidual": 1.0e-12,
            "gExtremaError": 2.0e-11,
            "endpointDrift": 1.0e-11,
            "centralDerivativeError": 1.0e-6,
            "variationError": 2.0e-10,
            "monotonicitySlack": 1.0e-15,
            "highWitnessPositionErrorL2": 2.0e-4,
        },
    }
    tolerance = audit["tolerances"]
    conditions = (
        audit["periodQuadratureDifference"] <= tolerance["periodQuadratureDifference"],
        audit["closureErrorL2"] <= tolerance["closureErrorL2"],
        audit["maximumRk4LevelResidual"] <= tolerance["levelResidual"],
        audit["maximumAnalyticLevelResidual"] <= tolerance["levelResidual"],
        audit["gMinimumError"] <= tolerance["gExtremaError"],
        audit["gMaximumError"] <= tolerance["gExtremaError"],
        audit["endpointGDrift"] <= tolerance["endpointDrift"],
        audit["endpointQDrift"] <= tolerance["endpointDrift"],
        audit["maximumCentralDerivativeError"] <= tolerance["centralDerivativeError"],
        audit["onePeriodVariationError"] <= tolerance["variationError"],
        audit["minimumCumulativeVariationIncrement"] >= -tolerance["monotonicitySlack"],
        audit["highWitnessPositionErrorL2"] <= tolerance["highWitnessPositionErrorL2"],
    )
    audit["conditions"] = [bool(value) for value in conditions]
    audit["checksPassed"] = bool(all(conditions))
    need(audit["checksPassed"], "orbit/period audit failed: " + repr(audit))

    rows: list[dict[str, str]] = []

    def add_row(panel: str, record: str, series: str, x: float, y: float,
                x_unit: str, y_unit: str, evidence: str, method: str) -> None:
        rows.append({
            "panel": panel,
            "record": record,
            "series": series,
            "x": number(x),
            "y": number(y),
            "x_unit": x_unit,
            "y_unit": y_unit,
            "evidence_class": evidence,
            "formula_source": FORMULA_SOURCE,
            "method": method,
        })

    for index, (x, y) in enumerate(level_curve["points"]):
        add_row("A", f"a-orbit-{index:04d}", "Gamma", x, y, "radian", "radian",
                "analytic exact level set", "closed level-set parametrization")
    add_row("A", "a-witness-start", "witness-x-star", start[0], start[1],
            "radian", "radian", "analytic exact point", "exact trigonometric witness")
    add_row("A", "a-witness-high", "witness-x-dagger", high[0], high[1],
            "radian", "radian", "analytic exact point", "exact trigonometric witness")

    stride = int(orbit_config["storedStride"])
    stored_indices = range(0, len(times), stride)
    for index in stored_indices:
        add_row("B", f"b-g-{index:05d}", "g", times[index] / period, g[index],
                "period", "squared velocity", "deterministic numerical rendering",
                "fixed-step RK4 of exact analytic ODE")

    circuits = int(config["panelC"]["circuits"])
    for circuit in range(circuits):
        first = 0 if circuit == 0 else stride
        for index in range(first, len(times), stride):
            normalized_time = circuit + times[index] / period
            add_row("C", f"c-signed-{circuit}-{index:05d}", "signed-primitive",
                    normalized_time, g[index] - g[0], "circuit", "squared velocity",
                    "deterministic numerical rendering", "periodic exact primitive g-g0")
            add_row("C", f"c-absolute-{circuit}-{index:05d}", "cumulative-absolute-variation",
                    normalized_time, circuit * variation + cumulative[index],
                    "circuit", "total variation", "deterministic numerical rendering",
                    "cumulative absolute primitive increments")

    panel_d = config["panelD"]
    amplitudes = np.geomspace(
        float(panel_d["amplitudeMinimum"]),
        float(panel_d["amplitudeMaximum"]),
        int(panel_d["points"]),
    )
    scaling_series = {
        "positive-excursion-O-plus": (amplitudes ** 2, "quadratic proved asymptotic class"),
        "maximal-clock-height-M": (amplitudes ** 2, "quadratic successor scale guide"),
        "payment-two-thirds": (amplitudes ** 2, "quadratic exact exponent transform"),
        "absolute-variation-H1": (amplitudes ** 3, "cubic proved asymptotic class"),
        "complete-payment-P": (amplitudes ** 3, "cubic proved asymptotic class"),
    }
    for series, (values, evidence) in scaling_series.items():
        for index, (amplitude, value) in enumerate(zip(amplitudes, values)):
            add_row("D", f"d-{series}-{index:03d}", series, amplitude, value,
                    "amplitude", "normalized magnitude", evidence,
                    "normalized exponent guide; multiplicative constants suppressed")

    log_amplitude = np.log(amplitudes)
    quadratic_slope_error = float(np.max(np.abs(np.diff(np.log(amplitudes ** 2)) / np.diff(log_amplitude) - 2.0)))
    cubic_slope_error = float(np.max(np.abs(np.diff(np.log(amplitudes ** 3)) / np.diff(log_amplitude) - 3.0)))
    audit["maximumQuadraticLogSlopeError"] = quadratic_slope_error
    audit["maximumCubicLogSlopeError"] = cubic_slope_error
    audit["checksPassed"] = bool(
        audit["checksPassed"] and quadratic_slope_error <= 5.0e-13 and cubic_slope_error <= 5.0e-13
    )
    need(audit["checksPassed"], "amplitude slope audit failed")
    arrays = {
        "levelCurve": level_curve,
        "orbit": orbit,
        "period": period,
        "highIndex": high_index,
        "amplitudes": amplitudes,
        "quadratic": amplitudes ** 2,
        "cubic": amplitudes ** 3,
        "circuits": circuits,
        "variation": variation,
        "stride": stride,
    }
    return rows, arrays, audit


def add_blossom(fig: Any, Circle: Any, np: Any) -> None:
    center = np.array([0.977, 0.963])
    for angle in np.linspace(0.0, 2.0 * math.pi, 5, endpoint=False):
        position = center + 0.008 * np.array([math.cos(angle), math.sin(angle)])
        fig.add_artist(Circle(
            position, 0.0058, transform=fig.transFigure,
            facecolor=PALETTE["navy_open"], edgecolor=PALETTE["navy"],
            linewidth=0.45, clip_on=False, zorder=30,
        ))
    fig.add_artist(Circle(
        center, 0.0036, transform=fig.transFigure,
        facecolor=PALETTE["orange"], edgecolor=PALETTE["charcoal"],
        linewidth=0.4, clip_on=False, zorder=31,
    ))


def render_figure(config: dict[str, Any], arrays: dict[str, Any], output: Path,
                  np: Any, matplotlib: Any, plt: Any, Circle: Any) -> dict[str, Any]:
    matplotlib.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 6.7,
        "axes.titlesize": 7.5,
        "axes.labelsize": 6.7,
        "xtick.labelsize": 5.9,
        "ytick.labelsize": 5.9,
        "legend.fontsize": 5.4,
        "axes.linewidth": 0.62,
        "lines.linewidth": 1.2,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "svg.hashsalt": "r074s-recurrent-tail-obstruction-v1",
    })
    width = float(config["widthMillimetres"]) / 25.4
    height = float(config["heightMillimetres"]) / 25.4
    fig, axes = plt.subplots(2, 2, figsize=(width, height), constrained_layout=False)
    fig.subplots_adjust(left=0.085, right=0.885, bottom=0.115, top=0.805, wspace=0.43, hspace=0.57)
    fig.patch.set_facecolor(PALETTE["paper"])
    fig.suptitle(
        "Recurrent streamline: signed excursion versus absolute temporal variation",
        x=0.085, y=0.972, ha="left", va="top", fontsize=10.1,
        fontweight="bold", color=PALETTE["charcoal"],
    )
    fig.text(
        0.085, 0.895,
        "ANALYTIC EXACT FIELD · DETERMINISTIC NUMERICAL RENDERING · NOT DNS · NOT CLAY",
        ha="left", va="center", fontsize=6.05, fontweight="bold",
        color=PALETTE["charcoal"],
        bbox={"boxstyle": "round,pad=0.24", "facecolor": "white",
              "edgecolor": PALETTE["gray"], "linewidth": 0.55},
    )
    fig.text(
        0.955, 0.895,
        r"$\psi=\sin x_1\sin x_2=1/2,\quad g=|W|^2,\quad q=g'$",
        ha="right", va="center", fontsize=6.3, color=PALETTE["charcoal"],
    )
    add_blossom(fig, Circle, np)

    ax_a, ax_b = axes[0]
    ax_c, ax_d = axes[1]

    level = arrays["levelCurve"]
    xy = level["points"]
    ax_a.plot(xy[:, 0] / math.pi, xy[:, 1] / math.pi,
              color=PALETTE["navy"], linewidth=1.45, label=r"$\Gamma: \psi=1/2$")
    for index in (105, 405, 705, 1005):
        ax_a.annotate(
            "", xy=(xy[index + 22, 0] / math.pi, xy[index + 22, 1] / math.pi),
            xytext=(xy[index, 0] / math.pi, xy[index, 1] / math.pi),
            arrowprops={"arrowstyle": "-|>", "color": PALETTE["orange"],
                        "linewidth": 0.85, "mutation_scale": 6.5},
        )
    start = np.asarray(config["orbit"]["witnessStart"])
    high = np.asarray(config["orbit"]["witnessHigh"])
    ax_a.plot(start[0] / math.pi, start[1] / math.pi, marker="o", markersize=5.0,
              markerfacecolor="white", markeredgecolor=PALETTE["orange"],
              markeredgewidth=1.0, linestyle="none", label=r"$x_*,\ g=1/2$")
    ax_a.plot(high[0] / math.pi, high[1] / math.pi, marker="s", markersize=4.2,
              markerfacecolor=PALETTE["navy"], markeredgecolor="white",
              markeredgewidth=0.55, linestyle="none", label=r"$x^\dagger,\ g=3/4$")
    ax_a.plot(0.5, 0.5, marker="+", color=PALETTE["gray"], markersize=5.0, linestyle="none")
    ax_a.set_title("Regular closed streamline", loc="left", pad=4)
    ax_a.set_xlabel(r"$x_1/\pi$")
    ax_a.set_ylabel(r"$x_2/\pi$")
    ax_a.set_xlim(0.12, 0.88)
    ax_a.set_ylim(0.12, 0.88)
    ax_a.set_aspect("equal", adjustable="box")
    ax_a.set_xticks([1 / 6, 1 / 2, 5 / 6])
    ax_a.set_xticklabels([r"$1/6$", r"$1/2$", r"$5/6$"])
    ax_a.set_yticks([1 / 6, 1 / 2, 5 / 6])
    ax_a.set_yticklabels([r"$1/6$", r"$1/2$", r"$5/6$"])
    ax_a.legend(loc="upper right", frameon=False, handlelength=1.8, borderaxespad=0.1)

    orbit = arrays["orbit"]
    normalized_time = orbit["times"] / arrays["period"]
    ax_b.plot(normalized_time, orbit["g"], color=PALETTE["navy"], linewidth=1.35,
              label=r"$g(s)=|W(\chi(s))|^2$")
    ax_b.axhline(0.5, color=PALETTE["gray"], linestyle=(0, (2, 2)), linewidth=0.65)
    ax_b.axhline(0.75, color=PALETTE["gray"], linestyle=(0, (2, 2)), linewidth=0.65)
    ax_b.plot(0.0, 0.5, marker="o", markersize=4.6, markerfacecolor="white",
              markeredgecolor=PALETTE["orange"], markeredgewidth=0.9, linestyle="none")
    high_index = int(arrays["highIndex"])
    ax_b.plot(normalized_time[high_index], orbit["g"][high_index], marker="s",
              markersize=4.0, markerfacecolor=PALETTE["navy"],
              markeredgecolor="white", markeredgewidth=0.5, linestyle="none")
    ax_b.text(0.99, 0.742, r"$3/4$", ha="right", va="top", fontsize=5.4, color=PALETTE["gray"])
    ax_b.text(0.99, 0.505, r"$1/2$", ha="right", va="bottom", fontsize=5.4, color=PALETTE["gray"])
    ax_b.set_title("One period of the flux phase", loc="left", pad=4)
    ax_b.set_xlabel(r"orbit time $s/T_*$")
    ax_b.set_ylabel(r"$g(s)$")
    ax_b.set_xlim(0.0, 1.0)
    ax_b.set_ylim(0.475, 0.775)
    ax_b.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax_b.text(0.64, 0.515, r"$g(s)=|W(\chi(s))|^2$", ha="left", va="bottom",
              fontsize=5.45, color=PALETTE["navy"])

    circuits = int(arrays["circuits"])
    stride = int(arrays["stride"])
    c_time: list[float] = []
    c_signed: list[float] = []
    c_absolute: list[float] = []
    for circuit in range(circuits):
        first = 0 if circuit == 0 else stride
        for index in range(first, len(orbit["times"]), stride):
            c_time.append(circuit + orbit["times"][index] / arrays["period"])
            c_signed.append(orbit["g"][index] - orbit["g"][0])
            c_absolute.append(circuit * arrays["variation"] + orbit["cumulativeVariation"][index])
    absolute_line = ax_c.plot(
        c_time, c_absolute, color=PALETTE["orange"], linewidth=1.4,
        label=r"$\int_0^s |q(r)|\,dr$",
    )[0]
    ax_c.set_title("Four returns: cancellation versus debt", loc="left", pad=4)
    ax_c.set_xlabel("completed circuits")
    ax_c.set_ylabel("cumulative absolute variation", color=PALETTE["charcoal"])
    ax_c.set_xlim(0.0, float(circuits))
    ax_c.set_ylim(-0.18, circuits * arrays["variation"] + 0.32)
    ax_c.set_xticks(range(circuits + 1))
    signed_axis = ax_c.twinx()
    signed_line = signed_axis.plot(
        c_time, c_signed, color=PALETTE["navy"], linestyle=(0, (4, 2)),
        linewidth=1.05, label=r"$g(s)-g(0)$",
    )[0]
    signed_axis.set_ylabel("signed primitive", color=PALETTE["charcoal"], labelpad=1.0)
    signed_axis.set_ylim(-0.025, 0.285)
    signed_axis.tick_params(colors=PALETTE["charcoal"], width=0.55, length=2.4, pad=1.0)
    signed_axis.spines["top"].set_visible(False)
    signed_axis.spines["right"].set_color(PALETTE["gray"])
    ax_c.legend([absolute_line, signed_line], [absolute_line.get_label(), signed_line.get_label()],
                loc="upper left", frameon=False, handlelength=2.35)

    amplitude = arrays["amplitudes"]
    quadratic = arrays["quadratic"]
    cubic = arrays["cubic"]
    ax_d.loglog(amplitude, quadratic, color=PALETTE["navy"], linewidth=1.35,
                label="_quadratic-guide")
    ax_d.loglog(amplitude, cubic, color=PALETTE["orange"], linestyle="--", linewidth=1.35,
                label="_cubic-guide")
    marker_contract = (
        (r"$\mathfrak{O}^{F,+}$", quadratic, "o", PALETTE["navy"], "white", 0),
        (r"$\mathfrak{M}^K$", quadratic, "s", PALETTE["navy"], PALETTE["navy_open"], 3),
        (r"$(P_R^M)^{2/3}$", quadratic, "^", PALETTE["navy"], PALETTE["navy"], 6),
        (r"$\mathfrak{H}^F_1$", cubic, "D", PALETTE["orange"], "white", 1),
        (r"$P_R^M$", cubic, "x", PALETTE["orange"], PALETTE["orange"], 5),
    )
    for label, values, marker, edge, face, offset in marker_contract:
        indices = np.arange(offset, len(amplitude), 10)
        ax_d.plot(amplitude[indices], values[indices], linestyle="none", marker=marker,
                  markersize=3.5, markeredgewidth=0.75, markeredgecolor=edge,
                  markerfacecolor=face, label=label)
    ax_d.set_title("Normalized amplitude exponent classes", loc="left", pad=4)
    ax_d.set_xlabel("amplitude $A$")
    ax_d.set_ylabel("normalized magnitude")
    ax_d.set_xlim(1.0, 1000.0)
    ax_d.set_ylim(0.7, 2.0e9)
    ax_d.set_xticks([1.0, 10.0, 100.0, 1000.0])
    ax_d.set_yticks([1.0, 1.0e3, 1.0e6, 1.0e9])
    ax_d.minorticks_off()
    ax_d.legend(loc="upper left", frameon=False, ncol=1, handlelength=1.5,
                borderaxespad=0.1, fontsize=5.0, labelspacing=0.25)
    ax_d.text(270.0, 1.45 * 270.0 ** 3, "slope 3", ha="left", va="bottom",
              fontsize=5.5, color=PALETTE["orange"])
    ax_d.text(270.0, 270.0 ** 2 / 1.8, "slope 2", ha="left", va="top",
              fontsize=5.5, color=PALETTE["navy"])
    ax_d.text(0.98, 0.04, "constants suppressed", transform=ax_d.transAxes,
              ha="right", va="bottom", fontsize=5.2, color=PALETTE["gray"])

    for marker, axis in zip(("(A)", "(B)", "(C)", "(D)"), (ax_a, ax_b, ax_c, ax_d)):
        axis.text(-0.16, 1.10, marker, transform=axis.transAxes, ha="left", va="bottom",
                  fontsize=7.2, fontweight="bold", color=PALETTE["charcoal"])
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        axis.spines["left"].set_color(PALETTE["gray"])
        axis.spines["bottom"].set_color(PALETTE["gray"])
        axis.tick_params(colors=PALETTE["charcoal"], width=0.55, length=2.4)
        axis.grid(True, which="major", axis="both", color=PALETTE["light_gray"],
                  linewidth=0.42, alpha=0.72)
        axis.set_axisbelow(True)
    ax_a.grid(False)
    fig.text(
        0.085, 0.035,
        "Frozen exact family, core 7355c01d. Orbit-time curves are deterministic renderings, not DNS; panel D compares proved and target exponent classes, not constants.",
        ha="left", va="bottom", fontsize=5.25, color=PALETTE["gray"],
    )

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    figure_bounds = fig.bbox
    failures: list[dict[str, float | str]] = []
    for artist in fig.findobj(match=lambda item: hasattr(item, "get_window_extent") and item.get_visible()):
        try:
            bounds = artist.get_window_extent(renderer)
        except Exception:
            continue
        if bounds.width == 0.0 and bounds.height == 0.0:
            continue
        if (
            bounds.x0 < figure_bounds.x0 - 1.0
            or bounds.y0 < figure_bounds.y0 - 1.0
            or bounds.x1 > figure_bounds.x1 + 1.0
            or bounds.y1 > figure_bounds.y1 + 1.0
        ):
            failures.append({
                "artist": type(artist).__name__, "x0": float(bounds.x0),
                "y0": float(bounds.y0), "x1": float(bounds.x1), "y1": float(bounds.y1),
                "label": str(artist.get_label()) if hasattr(artist, "get_label") else "",
                "text": str(artist.get_text()) if hasattr(artist, "get_text") else "",
            })
    need(not failures, "artist bounds overflow: " + repr(failures[:4]))

    fixed_date = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    metadata = {
        "Title": "R0.74S recurrent-tail obstruction",
        "Author": "C. K. Zeng",
        "Subject": "Analytic exact field and deterministic rendering; not DNS; not Clay",
        "Creator": "r074s-recurrent-tail-obstruction-v1",
        "Producer": "Matplotlib",
        "CreationDate": fixed_date,
        "ModDate": fixed_date,
    }
    fig.savefig(output / "figure.pdf", format="pdf", metadata=metadata)
    fig.savefig(output / "figure.svg", format="svg", metadata={
        "Title": metadata["Title"], "Creator": metadata["Creator"], "Date": None,
    })
    fig.savefig(output / "figure.png", format="png", dpi=int(config["pngDpi"]),
                facecolor="white", metadata={"Software": metadata["Creator"]})
    plt.close(fig)
    return {"artistBoundsFailures": failures, "artistBoundsPass": not failures}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds")


def write_ndjson(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8", newline="\n",
    )


def create_qa(config: dict[str, Any], output: Path, Image: Any, ImageOps: Any,
              pdfium: Any) -> dict[str, Any]:
    qa_width = int(float(config["widthMillimetres"]) / 25.4 * int(config["qaDpi"]))
    qa_height = int(float(config["heightMillimetres"]) / 25.4 * int(config["qaDpi"]))
    with Image.open(output / "figure.png") as opened:
        master = opened.convert("RGB")
        final_size = master.resize((qa_width, qa_height), Image.Resampling.LANCZOS)
        final_size.save(output / "qa-final-size.png", dpi=(config["qaDpi"], config["qaDpi"]), optimize=False)
        grayscale = ImageOps.grayscale(final_size).convert("RGB")
        grayscale.save(output / "qa-grayscale.png", dpi=(config["qaDpi"], config["qaDpi"]), optimize=False)
    document = pdfium.PdfDocument(str(output / "figure.pdf"))
    need(len(document) == 1, "PDF must have one page")
    page = document[0]
    width_points, _ = page.get_size()
    pdf_image = page.render(scale=qa_width / float(width_points)).to_pil().convert("RGB")
    page.close()
    document.close()
    if pdf_image.size != (qa_width, qa_height):
        pdf_image = pdf_image.resize((qa_width, qa_height), Image.Resampling.LANCZOS)
    pdf_image.save(output / "qa-pdf.png", dpi=(config["qaDpi"], config["qaDpi"]), optimize=False)
    return {"qaPixels": [qa_width, qa_height]}


def render(config: dict[str, Any], repository: Path, runtime: dict[str, str],
           mpl_policy: str) -> None:
    started_wall = time.perf_counter()
    started_cpu = time.process_time()
    pid = os.getpid()
    progress: list[dict[str, object]] = []

    def event(name: str, **details: object) -> None:
        progress.append({
            "elapsedSeconds": time.perf_counter() - started_wall,
            "event": name,
            "pid": pid,
            "utc": utc_now(),
            **details,
        })

    source_blobs = verify_source_binding(repository, config)
    event("source-binding-pass", sourceCommit=config["sourceBinding"]["commit"],
          sourceBlobs=len(source_blobs), runtime=runtime)
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle
    from PIL import Image, ImageOps
    import pypdfium2 as pdfium

    with tempfile.TemporaryDirectory(prefix="r074s-figure-output-") as temporary:
        output = Path(temporary)
        rows, arrays, audit = generate_payload(config, np)
        event("orbit-audit-pass", period=audit["period"], closureError=audit["closureErrorL2"],
              variation=audit["onePeriodAbsoluteVariation"])
        write_csv(output / "source-data.csv", rows)
        event("source-data-generated", rows=len(rows))
        render_audit = render_figure(config, arrays, output, np, matplotlib, plt, Circle)
        event("journal-exports-rendered", outputs=["figure.pdf", "figure.png", "figure.svg"])
        qa = create_qa(config, output, Image, ImageOps, pdfium)
        event("qa-assets-rendered", outputs=["qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"])

        row_counts = {panel: sum(row["panel"] == panel for row in rows) for panel in "ABCD"}
        results = {
            "claimBoundary": {
                "analyticExactField": True,
                "deterministicNumericalRendering": True,
                "dns": False,
                "notClay": True,
                "openS472Proved": False,
            },
            "formulaAudit": audit,
            "render": {
                **render_audit,
                "figurePhysicalSizeMillimetres": [config["widthMillimetres"], config["heightMillimetres"]],
                "pngDpi": config["pngDpi"],
                **qa,
            },
            "rowCounts": {**row_counts, "total": len(rows)},
            "schema": "r074s-recurrent-tail-results-v1",
            "sourceBinding": {
                "commit": config["sourceBinding"]["commit"],
                "fileCount": len(source_blobs),
                "status": "PASS",
            },
            "status": "PASS",
        }
        (output / "results.json").write_text(canonical(results), encoding="utf-8", newline="\n")

        memory_bytes = None
        try:
            memory_bytes = int(os.sysconf("SC_PAGE_SIZE")) * int(os.sysconf("SC_PHYS_PAGES"))
        except (ValueError, OSError, AttributeError):
            pass
        environment = {
            "createdAtUtc": utc_now(),
            "logicalCpuCount": os.cpu_count(),
            "machine": platform.machine(),
            "matplotlibConfigPolicy": mpl_policy,
            "memoryBytes": memory_bytes,
            "operatingSystem": platform.platform(),
            "packages": {key: runtime[key] for key in ("numpy", "matplotlib", "pillow", "pypdf", "pypdfium2")},
            "processes": 1,
            "python": runtime["python"],
            "schema": "r074s-recurrent-tail-environment-v1",
            "sourceRootPolicy": "repository supplied at runtime; absolute path intentionally not recorded",
            "threadsPerProcess": 1,
        }
        (output / "environment.json").write_text(canonical(environment), encoding="utf-8", newline="\n")
        event("raw-layer-complete", deterministicOutputs=8, observabilityOutputs=3)
        write_ndjson(output / "progress.ndjson", progress)
        usage = resource.getrusage(resource.RUSAGE_SELF)
        write_ndjson(output / "resource-log.ndjson", [{
            "cpuSeconds": time.process_time() - started_cpu,
            "maximumResidentSetSizeRaw": float(usage.ru_maxrss),
            "maximumResidentSetSizeRawUnit": "bytes" if sys.platform == "darwin" else "kilobytes",
            "pid": pid,
            "processes": 1,
            "schema": "r074s-recurrent-tail-resource-v1",
            "threadsPerProcess": 1,
            "utc": utc_now(),
            "wallSeconds": time.perf_counter() - started_wall,
        }])
        for name in RAW_FILES:
            need((output / name).is_file(), "renderer omitted raw/result file: " + name)
        for name in RAW_FILES:
            os.replace(output / name, HERE / name)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deps", required=True, type=Path)
    parser.add_argument("--repository", type=Path, default=REPOSITORY_DEFAULT)
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    need(args.render, "use --render")
    preflight_archive()
    insert_dependencies(args.deps)
    config = load_json(HERE / "config.json")
    runtime = live_runtime_versions(config)
    repository = args.repository.expanduser().resolve()
    need(repository.is_dir(), "--repository is not a directory")
    raw_mpl = os.environ.get("MPLCONFIGDIR")
    owner: tempfile.TemporaryDirectory[str] | None = None
    if raw_mpl:
        mpl_path = Path(raw_mpl).expanduser().resolve()
        need(mpl_path != HERE and HERE not in mpl_path.parents, "MPLCONFIGDIR must be outside archive")
        mpl_path.mkdir(parents=True, exist_ok=True)
        mpl_policy = "explicit external environment directory"
    else:
        owner = tempfile.TemporaryDirectory(prefix="r074s-mpl-config-")
        os.environ["MPLCONFIGDIR"] = owner.name
        mpl_policy = "system temporary directory removed after render"
    try:
        render(config, repository, runtime, mpl_policy)
    finally:
        if owner is not None:
            owner.cleanup()
    print("PASS: source-bound analytic figure raw layer rendered")


if __name__ == "__main__":
    main()
