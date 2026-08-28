#!/usr/bin/env python3
"""Generate the R0.72W exact-periodic transfer journal figure.

The source lifecycle exposes only a zero-write ``--self-test``.  Draft and
formal rendering require the formal R0.72W certificate.  The renderer then
computes a deterministic NumPy Fourier/Strang forward--adjoint diagnostic;
that numerical panel is explicitly non-probative.  Formal rendering also
binds a frozen source commit to a distinct clean certificate commit and
refuses to overwrite any package or public output.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
from pathlib import Path
import re
import resource
import shutil
import subprocess
import sys
import time
from typing import Any, Callable
from xml.sax.saxutils import escape


REPOSITORY = Path(__file__).resolve().parents[1]
PACKAGE = (
    REPOSITORY
    / "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer"
)
CERTIFICATE_DIR = REPOSITORY / "research/certificates/r072w"
CERTIFICATE = CERTIFICATE_DIR / "certificate.json"
PUBLIC = REPOSITORY / "public/assets/r072w"
FIGURE_ID = "fig-r072w-exact-tail-transfer"
WIDTH_MM = 178
HEIGHT_MM = 98
PNG_DPI = 600

PAPER = "#ffffff"
INK = "#17212b"
MUTED = "#66727e"
GRID = "#d9dde1"
BLUE = "#285f8f"
GOLD = "#a6781f"
PALE_GOLD = "#f4f0e6"

SOURCE_FILES = (
    "README.md",
    "caption.md",
    "command.txt",
    "config.json",
    "contract.json",
    "environment.txt",
    "plot.py",
    "qa-protocol.md",
    "requirements.txt",
    "validate.py",
)
GENERATED_FILES = (
    "data.csv",
    "results.json",
    "validation.json",
    "progress.ndjson",
    "resource-log.ndjson",
    "qa-report.md",
    "figure.svg",
    "figure.pdf",
    "figure.png",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "manifest.json",
    "SHA256SUMS",
)

DIAGNOSTIC_ALPHAS = (1.0, 0.75, 0.5, 0.35, 0.25)
DIAGNOSTIC_LEVELS = (
    ("coarse", 512, 1000),
    ("medium", 1024, 2000),
    ("fine", 2048, 4000),
)
DIAGNOSTIC_T = 1.0
POWER_ITERATIONS = 32
REFERENCE_FINE = {
    1.0: 0.071285,
    0.75: 0.119851,
    0.5: 0.101230,
    0.35: 0.080730,
    0.25: 0.069833,
}
EXPECTED_ANALYTIC_ROWS = 729
EXPECTED_NUMERICAL_ROWS = 15
EXPECTED_ROWS = EXPECTED_ANALYTIC_ROWS + EXPECTED_NUMERICAL_ROWS

DATA_FIELDS = (
    "panel",
    "kind",
    "series",
    "x",
    "y",
    "z",
    "alpha",
    "resolution",
    "timeSteps",
    "powerIterations",
    "normEstimate",
    "powerResidual",
    "adjointDefect",
    "relativeToFine",
    "formula",
    "status",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def linspace(left: float, right: float, count: int) -> list[float]:
    if count < 2:
        raise ValueError("linspace needs at least two points")
    return [
        left + (right - left) * index / (count - 1)
        for index in range(count)
    ]


def coefficient_a0(z_value: float) -> float:
    """Scaled spatial slope alpha^2 V_X at S=0."""
    return 2.0 * (math.cos(z_value) - math.cos(2.0 * z_value))


def coefficient_a1(z_value: float) -> float:
    """Temporal sweep V_SX at S=0."""
    return 2.0 * (-math.cos(z_value) + 4.0 * math.cos(2.0 * z_value))


def no_go_ratios() -> list[tuple[str, float, str]]:
    pi = math.pi
    polynomial = abs(-5.0 * pi**2 / 12.0 + 7.0 * pi**4 / 120.0)
    exact_gap = 1.0 + 4.0 / (3.0 * pi**2)
    exact_slope = -4.0
    truncated_slope = 3.0 * pi**2 - 1.25 * pi**4 + 0.175 * pi**6
    tail = abs(exact_slope - truncated_slope) / (3.0 * pi**2)
    return [
        ("alpha^2 H5 / 4", 5.0 * pi**2 / 12.0, "5*pi^2/12"),
        (
            "H5+H7 correction",
            polynomial,
            "abs(-5*pi^2/12+7*pi^4/120)",
        ),
        (
            "exact minus H3",
            exact_gap,
            "1+4/(3*pi^2)",
        ),
        (
            "exact tail after H7",
            tail,
            (
                "abs(-4-(3*pi^2-5*pi^4/4+7*pi^6/40))"
                "/(3*pi^2)"
            ),
        ),
    ]


def _empty_row() -> dict[str, str]:
    return {field: "" for field in DATA_FIELDS}


def analytic_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for z_value in linspace(-math.pi, math.pi, 721):
        row = _empty_row()
        row.update({
            "panel": "A",
            "kind": "exact-coefficient-geometry",
            "series": "(alpha^2 V_X, V_SX) at S=0",
            "x": f"{coefficient_a0(z_value):.17g}",
            "y": f"{coefficient_a1(z_value):.17g}",
            "z": f"{z_value:.17g}",
            "formula": "(2(cos(z)-cos(2z)),2(-cos(z)+4cos(2z)))",
            "status": "exact analytic identity",
        })
        rows.append(row)
    for label, value, formula in no_go_ratios():
        row = _empty_row()
        row.update({
            "panel": "A",
            "kind": "gauge-invariant-no-go-ratio",
            "series": label,
            "x": label,
            "y": f"{value:.17g}",
            "formula": formula,
            "status": "exact analytic ratio at y=pi",
        })
        rows.append(row)
    for index, (label, status) in enumerate((
        ("compact charts: alpha R -> 0", "local Taylor absorption only"),
        ("escaping charts: R=y/alpha", "termwise absorption false"),
        ("exact finite-type cell theorem", "analytic theorem in bound report"),
        ("expanding torus block contraction", "exact scalar-row theorem"),
    ), start=1):
        row = _empty_row()
        row.update({
            "panel": "B",
            "kind": "analytic-implication-chain",
            "series": label,
            "x": str(index),
            "y": str(index),
            "formula": status,
            "status": "analytic claim map",
        })
        rows.append(row)
    return rows


def _configure_numeric_threads() -> None:
    for name in (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
        "NUMEXPR_NUM_THREADS",
    ):
        os.environ.setdefault(name, "1")


def _diagnostic_initial_vectors(np: Any, z_grid: Any) -> tuple[Any, Any]:
    x_value = (
        1.0
        + 0.31 * np.cos(z_grid)
        + 0.17 * np.sin(2.0 * z_grid)
        + 1j * (0.23 * np.sin(z_grid) - 0.13 * np.cos(2.0 * z_grid))
    ).astype(np.complex128)
    y_value = (
        0.7
        - 0.19 * np.sin(z_grid)
        + 0.29 * np.cos(3.0 * z_grid)
        + 1j * (0.11 * np.cos(z_grid) + 0.07 * np.sin(4.0 * z_grid))
    ).astype(np.complex128)
    return x_value / np.linalg.norm(x_value), y_value / np.linalg.norm(y_value)


def _diffuse(np: Any, vector: Any, multiplier: Any) -> Any:
    return np.fft.ifft(np.fft.fft(vector) * multiplier)


def _propagators(
    np: Any,
    alpha: float,
    resolution: int,
    time_steps: int,
) -> tuple[Callable[[Any], Any], Callable[[Any], Any], Any]:
    dt = 2.0 * DIAGNOSTIC_T / time_steps
    z_grid = 2.0 * math.pi * np.arange(resolution) / resolution
    integer_modes = np.fft.fftfreq(resolution, d=1.0 / resolution)
    half_diffusion = np.exp(-0.5 * dt * (alpha * integer_modes) ** 2)
    full_diffusion = half_diffusion * half_diffusion
    midpoints = (
        -DIAGNOSTIC_T
        + (np.arange(time_steps, dtype=np.float64) + 0.5) * dt
    )
    first = 2.0 * np.exp(-alpha * alpha * midpoints)[:, None]
    second = -np.exp(-4.0 * alpha * alpha * midpoints)[:, None]
    potential = alpha ** -3 * (
        first * np.sin(z_grid)[None, :]
        + second * np.sin(2.0 * z_grid)[None, :]
    )
    phases = np.exp(1j * dt * potential)

    def forward(vector: Any) -> Any:
        value = _diffuse(np, vector, half_diffusion)
        last = time_steps - 1
        for index in range(time_steps):
            value *= phases[index]
            value = _diffuse(
                np,
                value,
                half_diffusion if index == last else full_diffusion,
            )
        return value

    def adjoint(vector: Any) -> Any:
        value = _diffuse(np, vector, half_diffusion)
        last = time_steps - 1
        for loop_index, phase_index in enumerate(range(last, -1, -1)):
            value *= phases[phase_index].conjugate()
            value = _diffuse(
                np,
                value,
                half_diffusion if loop_index == last else full_diffusion,
            )
        return value

    return forward, adjoint, z_grid


def _one_propagator_diagnostic(
    np: Any,
    alpha: float,
    resolution: int,
    time_steps: int,
    progress: Callable[[dict[str, Any]], None],
) -> dict[str, float]:
    forward, adjoint, z_grid = _propagators(
        np,
        alpha,
        resolution,
        time_steps,
    )
    vector, adjoint_probe = _diagnostic_initial_vectors(np, z_grid)
    for iteration in range(POWER_ITERATIONS):
        propagated = forward(vector)
        normal_value = adjoint(propagated)
        normal_norm = float(np.linalg.norm(normal_value))
        if not math.isfinite(normal_norm) or normal_norm <= 0.0:
            raise RuntimeError("forward-adjoint power iteration degenerated")
        vector = normal_value / normal_norm
        if iteration in (0, 7, 15, 23, POWER_ITERATIONS - 1):
            progress({
                "event": "power-iteration",
                "alpha": alpha,
                "resolution": resolution,
                "timeSteps": time_steps,
                "iteration": iteration + 1,
                "iterations": POWER_ITERATIONS,
            })
    propagated = forward(vector)
    normal_value = adjoint(propagated)
    norm_estimate = float(np.linalg.norm(propagated))
    eigenvalue = norm_estimate * norm_estimate
    power_residual = float(
        np.linalg.norm(normal_value - eigenvalue * vector)
        / max(eigenvalue, np.finfo(np.float64).tiny)
    )
    probe_forward = forward(vector)
    probe_adjoint = adjoint(adjoint_probe)
    left = np.vdot(probe_forward, adjoint_probe)
    right = np.vdot(vector, probe_adjoint)
    adjoint_defect = float(
        abs(left - right) / max(abs(left), abs(right), 1.0e-300)
    )
    return {
        "normEstimate": norm_estimate,
        "powerResidual": power_residual,
        "adjointDefect": adjoint_defect,
    }


def numerical_rows(
    progress: Callable[[dict[str, Any]], None],
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    _configure_numeric_threads()
    import numpy as np

    started = time.perf_counter()
    records: list[dict[str, Any]] = []
    total = len(DIAGNOSTIC_ALPHAS) * len(DIAGNOSTIC_LEVELS)
    completed = 0
    for alpha in DIAGNOSTIC_ALPHAS:
        for level, resolution, time_steps in DIAGNOSTIC_LEVELS:
            progress({
                "event": "diagnostic-start",
                "alpha": alpha,
                "level": level,
                "resolution": resolution,
                "timeSteps": time_steps,
                "completed": completed,
                "total": total,
            })
            values = _one_propagator_diagnostic(
                np,
                alpha,
                resolution,
                time_steps,
                progress,
            )
            completed += 1
            record = {
                "alpha": alpha,
                "level": level,
                "resolution": resolution,
                "timeSteps": time_steps,
                **values,
            }
            records.append(record)
            progress({
                "event": "diagnostic-complete",
                **record,
                "completed": completed,
                "total": total,
            })
            print(
                "R0.72W diagnostic "
                f"{completed}/{total}: alpha={alpha:.2f}, "
                f"N={resolution}, NS={time_steps}, "
                f"||U||~{values['normEstimate']:.9f}, "
                f"residual={values['powerResidual']:.3e}",
                flush=True,
            )

    fine = {
        record["alpha"]: record["normEstimate"]
        for record in records
        if record["level"] == "fine"
    }
    rows: list[dict[str, str]] = []
    for record in records:
        relative = abs(
            record["normEstimate"] - fine[record["alpha"]]
        ) / fine[record["alpha"]]
        row = _empty_row()
        row.update({
            "panel": "C",
            "kind": "forward-adjoint-propagator-norm",
            "series": record["level"],
            "x": f"{record['alpha']:.17g}",
            "y": f"{record['normEstimate']:.17g}",
            "alpha": f"{record['alpha']:.17g}",
            "resolution": str(record["resolution"]),
            "timeSteps": str(record["timeSteps"]),
            "powerIterations": str(POWER_ITERATIONS),
            "normEstimate": f"{record['normEstimate']:.17g}",
            "powerResidual": f"{record['powerResidual']:.17g}",
            "adjointDefect": f"{record['adjointDefect']:.17g}",
            "relativeToFine": f"{relative:.17g}",
            "formula": "Fourier Strang splitting plus power iteration on U*U",
            "status": "deterministic numerical diagnostic only; not proof",
        })
        rows.append(row)
    summary = {
        "numpyVersion": np.__version__,
        "wallTimeSeconds": time.perf_counter() - started,
        "maxRelativeToFine": max(
            float(row["relativeToFine"]) for row in rows
        ),
        "maxAdjointDefect": max(float(row["adjointDefect"]) for row in rows),
        "maxPowerResidual": max(float(row["powerResidual"]) for row in rows),
        "fineNorms": {f"{alpha:.2f}": fine[alpha] for alpha in fine},
        "referenceFine": {
            f"{alpha:.2f}": value for alpha, value in REFERENCE_FINE.items()
        },
        "maxFineReferenceDifference": max(
            abs(fine[alpha] - REFERENCE_FINE[alpha])
            for alpha in DIAGNOSTIC_ALPHAS
        ),
    }
    return rows, summary


class Scene:
    def __init__(self) -> None:
        self.items: list[tuple[Any, ...]] = []

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: str = INK,
        width: float = 2,
        dash: str | None = None,
    ) -> None:
        self.items.append(("line", x1, y1, x2, y2, color, width, dash))

    def polyline(
        self,
        points: list[tuple[float, float]],
        color: str = BLUE,
        width: float = 2,
        dash: str | None = None,
    ) -> None:
        self.items.append(("polyline", points, color, width, dash))

    def text(
        self,
        x: float,
        y: float,
        value: str,
        size: int = 18,
        color: str = INK,
        anchor: str = "start",
        bold: bool = False,
    ) -> None:
        self.items.append(("text", x, y, value, size, color, anchor, bold))

    def circle(
        self,
        x: float,
        y: float,
        radius: float,
        color: str = INK,
        open_marker: bool = False,
    ) -> None:
        self.items.append(("circle", x, y, radius, color, open_marker))

    def box(
        self,
        left: float,
        top: float,
        right: float,
        bottom: float,
        fill: str = PAPER,
        stroke: str = INK,
        width: float = 2,
    ) -> None:
        self.items.append(("box", left, top, right, bottom, fill, stroke, width))


def mapping(
    x0: float,
    x1: float,
    y0: float,
    y1: float,
    left: float,
    right: float,
    top: float,
    bottom: float,
) -> tuple[Callable[[float], float], Callable[[float], float]]:
    return (
        lambda x: left + (x - x0) * (right - left) / (x1 - x0),
        lambda y: bottom - (y - y0) * (bottom - top) / (y1 - y0),
    )


def axes(
    scene: Scene,
    box: tuple[float, float, float, float],
    x_ticks: list[tuple[float, str]],
    y_ticks: list[tuple[float, str]],
    x_map: Callable[[float], float],
    y_map: Callable[[float], float],
    xlabel: str,
    ylabel: str,
) -> None:
    left, right, top, bottom = box
    for value, label in x_ticks:
        x_value = x_map(value)
        scene.line(x_value, top, x_value, bottom, GRID, 1)
        scene.text(x_value, bottom + 25, label, 16, MUTED, "middle")
    for value, label in y_ticks:
        y_value = y_map(value)
        scene.line(left, y_value, right, y_value, GRID, 1)
        scene.text(left - 8, y_value + 5, label, 15, MUTED, "end")
    scene.line(left, bottom, right, bottom, INK, 2)
    scene.line(left, top, left, bottom, INK, 2)
    scene.text((left + right) / 2, bottom + 53, xlabel, 18, INK, "middle")
    scene.text(left, top - 12, ylabel, 17, INK)


def build_scene(numeric: list[dict[str, str]] | None) -> Scene:
    scene = Scene()
    headings = (
        (48, "A", "exact cell geometry and no-go ratios"),
        (622, "B", "compact versus escaping transfer"),
        (1190, "C", "forward-adjoint norm diagnostic"),
    )
    for left, letter, title in headings:
        scene.text(left, 58, letter, 31, INK, bold=True)
        scene.text(left + 40, 58, title, 21, INK, bold=True)

    # Panel A: exact finite-type coefficient curve and gauge-invariant ratios.
    box_a = (92, 560, 130, 490)
    xa, ya = mapping(-4.5, 4.5, -10.5, 10.5, *box_a)
    axes(
        scene,
        box_a,
        [(-4, "-4"), (-2, "-2"), (0, "0"), (2, "2"), (4, "4")],
        [(-10, "-10"), (-5, "-5"), (0, "0"), (5, "5"), (10, "10")],
        xa,
        ya,
        "A0 = alpha^2 V_X(0)",
        "A1 = V_SX(0)",
    )
    z_values = linspace(-math.pi, math.pi, 721)
    scene.polyline(
        [(xa(coefficient_a0(z)), ya(coefficient_a1(z))) for z in z_values],
        BLUE,
        4,
    )
    for z_value, label, dx, dy in (
        (0.0, "z=0", 8, -8),
        (2.0 * math.pi / 3.0, "2pi/3", 8, 20),
        (-2.0 * math.pi / 3.0, "-2pi/3", -8, -9),
        (math.pi, "pi", 8, -8),
    ):
        px = xa(coefficient_a0(z_value))
        py = ya(coefficient_a1(z_value))
        scene.circle(px, py, 6, GOLD)
        scene.text(px + dx, py + dy, label, 14, GOLD, "end" if dx < 0 else "start")
    scene.text(118, 153, "origin excluded: |alpha^2 V_X|+|V_SX| >= c_T", 14, INK, bold=True)

    ratio_left, ratio_right = 218, 555
    ratio_map, _ = mapping(0.0, 5.0, 0.0, 1.0, ratio_left, ratio_right, 0, 1)
    scene.text(92, 570, "centered ratios at y=pi", 17, INK, bold=True)
    scene.line(ratio_left, 585, ratio_right, 585, GRID, 1)
    for tick in range(6):
        x_value = ratio_map(float(tick))
        scene.line(x_value, 580, x_value, 590, MUTED, 1)
        scene.text(x_value, 609, str(tick), 13, MUTED, "middle")
    short_labels = ("H5/4", "H5+H7", "exact-H3", "tail after H7")
    for index, ((_, value, _), label) in enumerate(zip(no_go_ratios(), short_labels)):
        y_value = 638 + 47 * index
        scene.text(92, y_value + 5, label, 15, INK)
        scene.line(ratio_left, y_value, ratio_map(value), y_value, GOLD if index % 2 else BLUE, 4, "8,4" if index % 2 else None)
        scene.circle(ratio_map(value), y_value, 5, GOLD if index % 2 else BLUE, index % 2 == 1)
        scene.text(ratio_map(value) + 9, y_value + 5, f"{value:.3f}", 14, INK, bold=True)
    scene.text(92, 841, "time-only scalar gauges already removed", 14, MUTED)

    # Panel B: two analytic lanes and the nonperturbative exact route.
    scene.text(650, 119, "Taylor lane", 17, BLUE, bold=True)
    scene.box(650, 142, 1118, 213, PAPER, BLUE, 2)
    scene.text(884, 171, "compact chart: alpha R -> 0", 18, INK, "middle", True)
    scene.text(884, 197, "V_exact = H3 + local weighted remainder", 15, MUTED, "middle")
    scene.line(884, 213, 884, 255, BLUE, 3)
    scene.box(650, 255, 1118, 326, PAPER, BLUE, 2)
    scene.text(884, 284, "bounded-multiplier absorption", 18, INK, "middle", True)
    scene.text(884, 310, "only R = o(alpha^(-2/5))", 16, BLUE, "middle")

    scene.text(650, 384, "Escaping / torus lane", 17, GOLD, bold=True)
    scene.box(650, 407, 1118, 478, PALE_GOLD, GOLD, 2)
    scene.text(884, 436, "R = y/alpha: every Taylor term is leading", 17, INK, "middle", True)
    scene.text(884, 462, "centered H5/4 ratio -> 5 y^2 / 12", 15, GOLD, "middle")
    scene.line(884, 478, 884, 520, GOLD, 3, "8,5")
    scene.box(650, 520, 1118, 591, PALE_GOLD, GOLD, 2)
    scene.text(884, 549, "global termwise absorption: FALSE", 18, GOLD, "middle", True)
    scene.text(884, 575, "infinite trigonometric cancellation retained", 15, MUTED, "middle")

    scene.line(884, 625, 884, 664, INK, 3)
    scene.box(650, 664, 1118, 749, PAPER, INK, 2)
    scene.text(884, 695, "exact compact-escaping cell theorem", 18, INK, "middle", True)
    scene.text(884, 722, "unit cells -> full H^-1 direct sum", 15, MUTED, "middle")
    scene.text(884, 744, "-> expanding torus graph estimate", 15, MUTED, "middle")
    scene.line(884, 749, 884, 785, BLUE, 3)
    scene.box(650, 785, 1118, 852, PAPER, BLUE, 3)
    scene.text(884, 815, "exact periodic scalar-row block", 18, BLUE, "middle", True)
    scene.text(884, 840, "strict contraction: CLOSED", 18, BLUE, "middle", True)

    # Panel C: numerical diagnostic, generated only after certification.
    box_c = (1237, 1715, 150, 610)
    xc, yc = mapping(0.2, 1.05, 0.0, 0.14, *box_c)
    axes(
        scene,
        box_c,
        [(0.25, ".25"), (0.5, ".50"), (0.75, ".75"), (1.0, "1.0")],
        [(0.0, "0"), (0.04, ".04"), (0.08, ".08"), (0.12, ".12"), (0.14, ".14")],
        xc,
        yc,
        "alpha",
        "estimated ||U_alpha(1,-1)||_2->2",
    )
    styles = {
        "coarse": (MUTED, "3,4", "N=512, NS=1000", 44),
        "medium": (GOLD, "9,5", "N=1024, NS=2000", 16),
        "fine": (BLUE, None, "N=2048, NS=4000", -14),
    }
    if numeric:
        for level, (color, dash, label, label_offset) in styles.items():
            selected = sorted(
                (row for row in numeric if row["series"] == level),
                key=lambda row: float(row["alpha"]),
            )
            points = [
                (xc(float(row["alpha"])), yc(float(row["normEstimate"])))
                for row in selected
            ]
            scene.polyline(points, color, 3, dash)
            for px, py in points:
                scene.circle(px, py, 4.5, color, level != "fine")
            last = selected[-1]
            scene.text(
                xc(float(last["alpha"])) - 5,
                yc(float(last["normEstimate"])) + label_offset,
                label,
                13,
                color,
                "end",
                level == "fine",
            )
        max_relative = max(float(row["relativeToFine"]) for row in numeric)
        max_adjoint = max(float(row["adjointDefect"]) for row in numeric)
        max_residual = max(float(row["powerResidual"]) for row in numeric)
        audit_lines = (
            f"max relative-to-fine: {max_relative:.2e}",
            f"max adjoint defect: {max_adjoint:.2e}",
            f"max power residual: {max_residual:.2e}",
        )
    else:
        scene.text(1476, 370, "formal diagnostic generated after certificate", 16, MUTED, "middle")
        audit_lines = (
            "resolution audit: pending formal render",
            "deterministic initial vector; randomSeed=null",
            "full exact V_alpha; no polynomial truncation",
        )
    scene.box(1248, 670, 1714, 776, PAPER, GRID, 1)
    scene.text(1262, 696, "diagnostic ledger", 16, INK, bold=True)
    for index, value in enumerate(audit_lines):
        scene.text(1262, 722 + 23 * index, value, 14, MUTED)
    scene.text(1237, 815, "Fourier Strang + fixed power iteration on U*U", 14, INK)
    scene.text(1237, 840, "NUMERICAL DIAGNOSTIC ONLY — NOT PROOF", 16, GOLD, bold=True)

    scene.box(52, 885, 1062, 944, PAPER, BLUE, 3)
    scene.text(557, 921, "exact periodic scalar-row block contraction: CLOSED", 21, BLUE, "middle", True)
    scene.box(1092, 885, 1727, 944, PALE_GOLD, GOLD, 3)
    scene.text(1409, 912, "outer concatenation / nonlinear / Clay: OPEN", 17, GOLD, "middle", True)
    scene.text(1409, 934, "diagnostic does not evaluate C_T", 14, MUTED, "middle")

    # Locked decorative research blossom.
    blossom_x, blossom_y = 1740, 39
    for index in range(5):
        angle = -math.pi / 2 + 2 * math.pi * index / 5
        scene.circle(
            blossom_x + 11 * math.cos(angle),
            blossom_y + 11 * math.sin(angle),
            6,
            BLUE if index % 2 == 0 else GOLD,
        )
    scene.circle(blossom_x, blossom_y, 4, INK)
    return scene


def save_data(rows: list[dict[str, str]]) -> None:
    with (PACKAGE / "data.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=DATA_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def render_svg(scene: Scene) -> None:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'width="178mm" height="98mm" viewBox="0 0 1780 980">'
        ),
        f'<rect width="1780" height="980" fill="{PAPER}"/>',
    ]
    for item in scene.items:
        if item[0] == "line":
            _, x1, y1, x2, y2, color, width, dash = item
            extra = f' stroke-dasharray="{dash}"' if dash else ""
            parts.append(
                f'<line x1="{x1:.3f}" y1="{y1:.3f}" '
                f'x2="{x2:.3f}" y2="{y2:.3f}" stroke="{color}" '
                f'stroke-width="{width}"{extra}/>'
            )
        elif item[0] == "polyline":
            _, points, color, width, dash = item
            extra = f' stroke-dasharray="{dash}"' if dash else ""
            coordinates = " ".join(f"{x:.3f},{y:.3f}" for x, y in points)
            parts.append(
                f'<polyline points="{coordinates}" fill="none" '
                f'stroke="{color}" stroke-width="{width}"{extra}/>'
            )
        elif item[0] == "circle":
            _, x, y, radius, color, open_marker = item
            if open_marker:
                parts.append(
                    f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{radius}" '
                    f'fill="{PAPER}" stroke="{color}" stroke-width="2"/>'
                )
            else:
                parts.append(
                    f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{radius}" '
                    f'fill="{color}"/>'
                )
        elif item[0] == "box":
            _, left, top, right, bottom, fill, stroke, width = item
            parts.append(
                f'<rect x="{left:.3f}" y="{top:.3f}" '
                f'width="{right-left:.3f}" height="{bottom-top:.3f}" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'
            )
        else:
            _, x, y, value, size, color, anchor, bold = item
            parts.append(
                f'<text x="{x:.3f}" y="{y:.3f}" '
                'font-family="DejaVu Sans,Arial,sans-serif" '
                f'font-size="{size}" font-weight="{700 if bold else 400}" '
                f'text-anchor="{anchor}" fill="{color}">{escape(value)}</text>'
            )
    parts.append("</svg>")
    (PACKAGE / "figure.svg").write_text("\n".join(parts) + "\n", encoding="utf-8")


def render_pdf(scene: Scene) -> None:
    from reportlab.pdfgen import canvas

    width = WIDTH_MM / 25.4 * 72
    height = HEIGHT_MM / 25.4 * 72
    sx, sy = width / 1780, height / 980
    pdf = canvas.Canvas(
        str(PACKAGE / "figure.pdf"),
        pagesize=(width, height),
        invariant=1,
        pageCompression=1,
    )
    pdf.setTitle("R0.72W exact-periodic transfer and diagnostic")
    pdf.setAuthor("Kasifa")
    pdf.setSubject("Exact analytic transfer with a non-probative numerical diagnostic")
    for item in scene.items:
        if item[0] in ("line", "polyline"):
            if item[0] == "line":
                _, x1, y1, x2, y2, color, line_width, dash = item
                points = [(x1, y1), (x2, y2)]
            else:
                _, points, color, line_width, dash = item
            pdf.setStrokeColor(color)
            pdf.setLineWidth(line_width * sx)
            pdf.setDash([float(value) * sx for value in dash.split(",")] if dash else [])
            path = pdf.beginPath()
            path.moveTo(points[0][0] * sx, height - points[0][1] * sy)
            for x_value, y_value in points[1:]:
                path.lineTo(x_value * sx, height - y_value * sy)
            pdf.drawPath(path, stroke=1, fill=0)
        elif item[0] == "circle":
            _, x, y, radius, color, open_marker = item
            pdf.setStrokeColor(color)
            pdf.setFillColor(PAPER if open_marker else color)
            pdf.setLineWidth(2 * sx)
            pdf.circle(x * sx, height - y * sy, radius * sx, stroke=int(open_marker), fill=1)
        elif item[0] == "box":
            _, left, top, right, bottom, fill, stroke, line_width = item
            pdf.setFillColor(fill)
            pdf.setStrokeColor(stroke)
            pdf.setLineWidth(line_width * sx)
            pdf.rect(
                left * sx,
                height - bottom * sy,
                (right - left) * sx,
                (bottom - top) * sy,
                stroke=1,
                fill=1,
            )
        else:
            _, x, y, value, size, color, anchor, bold = item
            pdf.setFillColor(color)
            pdf.setFont("Helvetica-Bold" if bold else "Helvetica", size * sx)
            if anchor == "middle":
                pdf.drawCentredString(x * sx, height - y * sy, value)
            elif anchor == "end":
                pdf.drawRightString(x * sx, height - y * sy, value)
            else:
                pdf.drawString(x * sx, height - y * sy, value)
    pdf.showPage()
    pdf.save()


def _font_path(bold: bool) -> str | None:
    candidates = (
        [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
        if bold
        else [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    )
    return next((path for path in candidates if Path(path).is_file()), None)


def render_png(scene: Scene) -> None:
    from PIL import Image, ImageDraw, ImageFont

    pixel_width = round(WIDTH_MM / 25.4 * PNG_DPI)
    pixel_height = round(HEIGHT_MM / 25.4 * PNG_DPI)
    sx, sy = pixel_width / 1780, pixel_height / 980
    image = Image.new("RGB", (pixel_width, pixel_height), PAPER)
    draw = ImageDraw.Draw(image)
    font_cache: dict[tuple[int, bool], Any] = {}

    def selected_font(size: int, bold: bool) -> Any:
        key = (size, bold)
        if key not in font_cache:
            path = _font_path(bold)
            font_cache[key] = (
                ImageFont.truetype(path, max(8, round(size * sx)))
                if path
                else ImageFont.load_default()
            )
        return font_cache[key]

    def stroke(
        points: list[tuple[float, float]],
        color: str,
        line_width: float,
        dash: str | None,
    ) -> None:
        rendered_width = max(1, round(line_width * sx))
        if not dash:
            draw.line(points, fill=color, width=rendered_width)
            return
        pattern = [float(value) * sx for value in dash.split(",")]
        pattern_index = 0
        remaining = pattern[0]
        drawing = True
        for start, end in zip(points, points[1:]):
            x0, y0 = start
            x1, y1 = end
            length = math.hypot(x1 - x0, y1 - y0)
            consumed = 0.0
            while length and consumed < length:
                step = min(remaining, length - consumed)
                left = consumed / length
                right = (consumed + step) / length
                if drawing:
                    draw.line(
                        (
                            (x0 + (x1 - x0) * left, y0 + (y1 - y0) * left),
                            (x0 + (x1 - x0) * right, y0 + (y1 - y0) * right),
                        ),
                        fill=color,
                        width=rendered_width,
                    )
                consumed += step
                remaining -= step
                if remaining <= 1.0e-9:
                    pattern_index = (pattern_index + 1) % len(pattern)
                    remaining = pattern[pattern_index]
                    drawing = not drawing

    for item in scene.items:
        if item[0] in ("line", "polyline"):
            if item[0] == "line":
                _, x1, y1, x2, y2, color, line_width, dash = item
                points = [(x1 * sx, y1 * sy), (x2 * sx, y2 * sy)]
            else:
                _, raw, color, line_width, dash = item
                points = [(x * sx, y * sy) for x, y in raw]
            stroke(points, color, line_width, dash)
        elif item[0] == "circle":
            _, x, y, radius, color, open_marker = item
            draw.ellipse(
                ((x - radius) * sx, (y - radius) * sy, (x + radius) * sx, (y + radius) * sy),
                fill=PAPER if open_marker else color,
                outline=color,
                width=max(1, round(2 * sx)) if open_marker else 1,
            )
        elif item[0] == "box":
            _, left, top, right, bottom, fill, outline, line_width = item
            draw.rectangle(
                (left * sx, top * sy, right * sx, bottom * sy),
                fill=fill,
                outline=outline,
                width=max(1, round(line_width * sx)),
            )
        else:
            _, x, y, value, size, color, anchor, bold = item
            font = selected_font(size, bold)
            bounds = draw.textbbox((0, 0), value, font=font)
            text_width = bounds[2] - bounds[0]
            if anchor == "middle":
                tx = x * sx - text_width / 2
            elif anchor == "end":
                tx = x * sx - text_width
            else:
                tx = x * sx
            draw.text((tx, y * sy - size * sy), value, font=font, fill=color)
    image.save(
        PACKAGE / "figure.png",
        format="PNG",
        dpi=(PNG_DPI, PNG_DPI),
        optimize=False,
        title="R0.72W exact-periodic transfer and diagnostic",
        author="Kasifa",
    )


def build_qa() -> None:
    from PIL import Image

    image = Image.open(PACKAGE / "figure.png")
    preview = image.resize(
        (1260, round(1260 * image.height / image.width)),
        Image.Resampling.LANCZOS,
    )
    preview.save(PACKAGE / "qa-final-size.png", dpi=(180, 180))
    preview.convert("L").save(PACKAGE / "qa-grayscale.png", dpi=(180, 180))
    candidates = (
        REPOSITORY / ".openai/poppler/bin/pdftocairo",
        Path(
            "/Users/kasifa/.cache/codex-runtimes/"
            "codex-primary-runtime/dependencies/native/poppler/"
            "poppler/bin/pdftocairo"
        ),
    )
    pdftocairo = next((path for path in candidates if path.is_file()), None)
    if pdftocairo:
        subprocess.run(
            [
                str(pdftocairo),
                "-png",
                "-singlefile",
                "-r",
                "180",
                str(PACKAGE / "figure.pdf"),
                str(PACKAGE / "qa-pdf"),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        preview.save(PACKAGE / "qa-pdf.png", dpi=(180, 180))


def git_status_dirty() -> bool:
    return bool(
        subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=all"],
            cwd=REPOSITORY,
            text=True,
        ).strip()
    )


def reject_output_overwrite(include_public: bool) -> None:
    paths = [PACKAGE / name for name in GENERATED_FILES]
    if include_public:
        paths.extend(
            PUBLIC / f"{FIGURE_ID}.{extension}"
            for extension in ("pdf", "svg", "png")
        )
    present = [str(path.relative_to(REPOSITORY)) for path in paths if path.exists()]
    if present:
        raise RuntimeError(
            "refusing to overwrite pre-existing figure outputs: "
            + ", ".join(present)
        )


def validate_formal_certificate() -> tuple[dict[str, Any], dict[str, Any]]:
    if not CERTIFICATE.is_file():
        raise RuntimeError("formal R0.72W certificate is absent")
    subprocess.run(
        [
            sys.executable,
            "research/certificates/r072w/validate_certificate.py",
            "--require-formal",
        ],
        cwd=REPOSITORY,
        check=True,
    )
    manifest = json.loads(
        (CERTIFICATE_DIR / "manifest.json").read_text(encoding="utf-8")
    )
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if (
        manifest.get("status") != "formal"
        or not manifest.get("sourceBindings")
        or certificate.get("status") != "passed"
    ):
        raise RuntimeError("formal source-bound R0.72W certificate required")
    return manifest, certificate


def validate_formal_lineage(
    certificate_manifest: dict[str, Any],
    source_commit: str | None,
    certificate_commit: str | None,
) -> None:
    for label, commit in (
        ("--source-commit", source_commit),
        ("--certificate-commit", certificate_commit),
    ):
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
            raise RuntimeError(f"{label} must be a full Git commit")
    assert source_commit is not None and certificate_commit is not None
    if source_commit != certificate_manifest.get("sourceCommit"):
        raise RuntimeError("--source-commit must equal the formal certificate source commit")
    if certificate_commit == source_commit:
        raise RuntimeError("certificateCommit must be distinct from the frozen sourceCommit")
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True
    ).strip()
    if certificate_commit != head:
        raise RuntimeError("--certificate-commit must equal the clean HEAD containing the certificate")
    for commit in (source_commit, certificate_commit):
        if subprocess.run(
            ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
            cwd=REPOSITORY,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode:
            raise RuntimeError(f"invalid Git commit in formal lineage: {commit}")
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", source_commit, certificate_commit],
        cwd=REPOSITORY,
    ).returncode:
        raise RuntimeError("certificateCommit does not descend from sourceCommit")
    for name in (
        "manifest.json",
        "certificate.json",
        "independent.json",
        "crosscheck.json",
        "SHA256SUMS",
    ):
        relative = f"research/certificates/r072w/{name}"
        committed = subprocess.check_output(
            ["git", "show", f"{certificate_commit}:{relative}"],
            cwd=REPOSITORY,
        )
        if committed != (REPOSITORY / relative).read_bytes():
            raise RuntimeError(
                f"working certificate differs from {certificate_commit}:{relative}"
            )


def package_validation(
    rows: list[dict[str, str]],
    numerical_summary: dict[str, Any],
) -> dict[str, Any]:
    from PIL import Image

    image = Image.open(PACKAGE / "figure.png")
    width, height = image.size
    svg = (PACKAGE / "figure.svg").read_text(encoding="utf-8")
    svg_colors = set(re.findall(r"#[0-9a-fA-F]{6}", svg))
    allowed_colors = {PAPER, INK, MUTED, GRID, BLUE, GOLD, PALE_GOLD}
    numerical = [row for row in rows if row["kind"] == "forward-adjoint-propagator-norm"]
    checks = {
        "certificatePassed": json.loads(CERTIFICATE.read_text(encoding="utf-8")).get("status") == "passed",
        "threePanels": all(
            label in svg
            for label in (
                "exact cell geometry and no-go ratios",
                "compact versus escaping transfer",
                "forward-adjoint norm diagnostic",
            )
        ),
        "exactPeriodicClosedVisible": "exact periodic scalar-row block contraction: CLOSED" in svg,
        "outerNonlinearClayOpenVisible": "outer concatenation / nonlinear / Clay: OPEN" in svg,
        "diagnosticOnlyVisible": "NUMERICAL DIAGNOSTIC ONLY" in svg and "NOT PROOF" in svg,
        "termwiseFalseVisible": "global termwise absorption: FALSE" in svg,
        "noGoRatiosVisible": all(token in svg for token in ("H5/4", "H5+H7", "exact-H3", "tail after H7")),
        "rowCount": len(rows) == EXPECTED_ROWS,
        "numericalRowCount": len(numerical) == EXPECTED_NUMERICAL_ROWS,
        "deterministicContractions": all(0.0 < float(row["normEstimate"]) <= 1.0 + 5.0e-12 for row in numerical),
        "adjointAuditFinite": math.isfinite(numerical_summary["maxAdjointDefect"]),
        "powerAuditFinite": math.isfinite(numerical_summary["maxPowerResidual"]),
        "resolutionAuditReported": math.isfinite(numerical_summary["maxRelativeToFine"]),
        "referenceAuditReported": math.isfinite(numerical_summary["maxFineReferenceDifference"]),
        "hardTwoChromaticRootCap": svg_colors <= allowed_colors and BLUE in svg_colors and GOLD in svg_colors,
        "redundantLineEncoding": "stroke-dasharray" in svg and "N=2048, NS=4000" in svg,
        "lockedResearchBlossomVisible": svg.count("<circle ") >= 20,
        "pngAtLeast600DpiAt178mm": (
            width >= math.floor(WIDTH_MM / 25.4 * PNG_DPI)
            and image.info.get("dpi", (0, 0))[0] >= 599
        ),
        "vectorPdf": (PACKAGE / "figure.pdf").read_bytes().startswith(b"%PDF"),
        "vectorSvg": svg.lstrip().startswith("<?xml"),
    }
    value = {
        "schemaVersion": 1,
        "status": "passed",
        "checks": checks,
        "png": {
            "width": width,
            "height": height,
            "dpi": list(image.info.get("dpi", (0, 0))),
        },
        "rowCount": len(rows),
        "numericalSummary": numerical_summary,
    }
    if not all(checks.values()):
        raise RuntimeError(f"automatic R0.72W figure validation failed: {value}")
    return value


def build_archive(
    rows: list[dict[str, str]],
    numerical_summary: dict[str, Any],
    formal: bool,
    visual_inspected: bool,
    source_commit: str | None,
    certificate_commit: str | None,
    certificate: dict[str, Any],
    wall_time_seconds: float,
) -> None:
    validation = package_validation(rows, numerical_summary)
    write_json(PACKAGE / "validation.json", validation)
    claim_boundary = json.loads(
        (PACKAGE / "contract.json").read_text(encoding="utf-8")
    )["claimBoundary"]
    results = {
        "schemaVersion": 1,
        "status": "passed",
        "figureId": FIGURE_ID,
        "pdeSimulation": True,
        "diagnosticOnly": True,
        "deterministic": True,
        "randomSeed": None,
        "panels": {
            "A": "exact finite-type coefficient geometry and gauge-invariant no-go ratios",
            "B": "compact-versus-escaping analytic transfer and exact torus theorem chain",
            "C": "Fourier Strang forward-adjoint power-iteration diagnostic with refinement audit",
        },
        "numericalSummary": numerical_summary,
        "claimBoundary": claim_boundary,
        "claimsNotMade": [
            "numerical proof of graph coercivity or contraction",
            "numerical evaluation of the nonconstructive C_T",
            "optimal propagator norm",
            "outer-time concatenation",
            "nonlinear Navier-Stokes closure",
            "Clay Millennium problem",
        ],
    }
    write_json(PACKAGE / "results.json", results)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    (PACKAGE / "resource-log.ndjson").write_text(
        json.dumps({
            "event": "resource-summary",
            "processes": 1,
            "threadsPerProcess": 1,
            "gpuUsed": False,
            "numpyVersion": numerical_summary["numpyVersion"],
            "maxResidentSetPlatformUnits": usage.ru_maxrss,
            "wallTimeSeconds": wall_time_seconds,
            "diagnosticOnly": True,
        }, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with (PACKAGE / "progress.ndjson").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({
            "event": "archive-ready",
            "rows": len(rows),
            "numericalRows": EXPECTED_NUMERICAL_ROWS,
        }, sort_keys=True) + "\n")
    (PACKAGE / "qa-report.md").write_text(
        "".join((
            "# R0.72W figure QA\n\n",
            f"- formal build: {'yes' if formal else 'no'}\n",
            f"- explicit visual inspection: {'yes' if visual_inspected else 'no'}\n",
            "- final-size, grayscale, and PDF previews generated: yes\n",
            "- exact analytic and numerical-diagnostic evidence separated: yes\n",
            "- deterministic full-exact-potential PDE diagnostic: yes\n",
            "- numerical diagnostic labelled NOT PROOF: yes\n",
            "- exact periodic scalar-row contraction labelled CLOSED: yes\n",
            "- outer concatenation, nonlinear closure, and Clay labelled OPEN: yes\n",
        )),
        encoding="utf-8",
    )

    publication_assets: list[dict[str, Any]] = []
    if formal:
        PUBLIC.mkdir(parents=True, exist_ok=True)
        for extension in ("pdf", "svg", "png"):
            source = PACKAGE / f"figure.{extension}"
            target = PUBLIC / f"{FIGURE_ID}.{extension}"
            shutil.copyfile(source, target)
            publication_assets.append({
                "path": str(target.relative_to(REPOSITORY)),
                "sha256": sha256(target),
                "bytes": target.stat().st_size,
                "byteIdenticalToMaster": sha256(target) == sha256(source),
            })

    archived = [
        *SOURCE_FILES,
        "data.csv",
        "results.json",
        "validation.json",
        "progress.ndjson",
        "resource-log.ndjson",
        "qa-report.md",
        "figure.svg",
        "figure.pdf",
        "figure.png",
        "qa-final-size.png",
        "qa-grayscale.png",
        "qa-pdf.png",
    ]
    from PIL import Image

    image = Image.open(PACKAGE / "figure.png")
    manifest = {
        "schemaVersion": "1.1",
        "figureId": FIGURE_ID,
        "release": "R0.72W",
        "status": "formal" if formal else "draft",
        "createdAt": "2026-08-28T00:00:00+08:00",
        "analyticalQuestion": (
            "How does the exact finite-type cell geometry bypass globally false Taylor-term absorption, "
            "and what does a reproducible discrete propagator stress test show under refinement?"
        ),
        "supportedClaim": (
            "The bound analytic report closes the exact scalar-row periodic graph and block-contraction transfer; "
            "the displayed forward-adjoint norms are deterministic diagnostics only."
        ),
        "git": (
            {
                "repository": "Kasifa/Kasifa.github.io",
                "sourceCommit": source_commit,
                "certificateCommit": certificate_commit,
                "dirtyAtCertifiedRun": False,
            }
            if formal
            else {
                "repository": "Kasifa/Kasifa.github.io",
                "commit": subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True
                ).strip(),
                "dirty": git_status_dirty(),
            }
        ),
        "computation": {
            "kind": "exact analytic presentation plus deterministic PDE diagnostic",
            "pdeSimulation": True,
            "diagnosticOnly": True,
            "equation": "u_S=u_XX+i*V_alpha(S,X)*u on T_{2*pi/alpha}",
            "potential": "alpha^-3*(2*exp(-alpha^2*S)*sin(alpha*X)-exp(-4*alpha^2*S)*sin(2*alpha*X))",
            "solver": "Fourier Strang splitting; fixed power iteration on discrete U*U",
            "timeInterval": [-DIAGNOSTIC_T, DIAGNOSTIC_T],
            "alphas": list(DIAGNOSTIC_ALPHAS),
            "levels": [
                {"label": label, "spatialModes": n_value, "timeSteps": steps}
                for label, n_value, steps in DIAGNOSTIC_LEVELS
            ],
            "powerIterations": POWER_ITERATIONS,
            "precision": "NumPy float64/complex128",
            "randomSeed": None,
            "initialVector": "fixed trigonometric polynomial recorded in generator",
            "wallTimeSeconds": wall_time_seconds,
            "monitoring": {
                "enabled": True,
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
            },
        },
        "compute": {
            "host": platform.node() or "local",
            "operatingSystem": platform.platform(),
            "cpu": platform.machine(),
            "processes": 1,
            "threadsPerProcess": 1,
            "gpu": "not used",
            "dgx": "not used; deterministic CPU FFT diagnostic",
        },
        "environment": {
            "python": platform.python_version(),
            "packagesLock": "requirements.txt",
            "numpy": numerical_summary["numpyVersion"],
            "pillow": getattr(Image, "__version__", "installed"),
            "reportlab": "pinned in requirements.txt",
        },
        "data": [{
            "path": "data.csv",
            "schema": list(DATA_FIELDS),
            "rows": len(rows),
            "sha256": sha256(PACKAGE / "data.csv"),
            "bytes": (PACKAGE / "data.csv").stat().st_size,
        }, {
            "path": "results.json",
            "schema": "panel meanings, numerical audit, and claims not made",
            "sha256": sha256(PACKAGE / "results.json"),
            "bytes": (PACKAGE / "results.json").stat().st_size,
        }, {
            "path": "validation.json",
            "schema": "lineage, format, diagnostic, and visible-boundary checks",
            "sha256": sha256(PACKAGE / "validation.json"),
            "bytes": (PACKAGE / "validation.json").stat().st_size,
        }],
        "sourceData": [{
            "location": "repository",
            "fileName": str(CERTIFICATE.relative_to(REPOSITORY)),
            "bytes": CERTIFICATE.stat().st_size,
            "sha256": sha256(CERTIFICATE),
            "role": "formalExactCertificate",
        }, {
            "location": "repository",
            "fileName": "scripts/generate_r072w_figure.py",
            "bytes": Path(__file__).stat().st_size,
            "sha256": sha256(Path(__file__)),
            "role": "analyticAndDiagnosticGenerator",
        }],
        "figure": {
            "widthMillimetres": WIDTH_MM,
            "heightMillimetres": HEIGHT_MM,
            "layout": "1x3",
            "profile": "journal-double-column",
            "script": "plot.py",
            "outputs": [{
                "path": f"figure.{extension}",
                "sha256": sha256(PACKAGE / f"figure.{extension}"),
                "bytes": (PACKAGE / f"figure.{extension}").stat().st_size,
                **(
                    {"dpi": PNG_DPI, "pixels": list(image.size)}
                    if extension == "png"
                    else {}
                ),
            } for extension in ("pdf", "svg", "png")],
        },
        "caption": {"english": "caption.md"},
        "qa": {
            "status": "passed",
            "visualInspectionExplicit": visual_inspected,
            "finalSizeInspected": visual_inspected,
            "grayscaleInspected": visual_inspected,
            "labelsAndLegendsInspected": visual_inspected,
            "dataCrossChecked": True,
            "diagnosticBoundaryInspected": visual_inspected,
            "finalSizePreview": "qa-final-size.png",
            "grayscalePreview": "qa-grayscale.png",
            "pdfRenderPreview": "qa-pdf.png",
            "manualReport": "qa-report.md",
        },
        "publication": {
            "directory": "public/assets/r072w",
            "stem": FIGURE_ID,
            "publicCopiesComplete": formal,
            "assets": publication_assets,
        },
        "claimBoundary": claim_boundary,
        "certificateClaimBoundary": certificate.get("claimBoundary", {}),
        "deterministic": True,
        "outputs": [{
            "path": name,
            "sha256": sha256(PACKAGE / name),
            "bytes": (PACKAGE / name).stat().st_size,
        } for name in archived],
    }
    write_json(PACKAGE / "manifest.json", manifest)
    ledger_names = sorted(
        path.name
        for path in PACKAGE.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    (PACKAGE / "SHA256SUMS").write_text(
        "".join(f"{sha256(PACKAGE / name)}  {name}\n" for name in ledger_names),
        encoding="utf-8",
    )


def self_test() -> None:
    config = json.loads((PACKAGE / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((PACKAGE / "contract.json").read_text(encoding="utf-8"))
    rows = analytic_rows()
    scene = build_scene(None)
    scene_text = {item[3] for item in scene.items if item[0] == "text"}
    package_files = {path.name for path in PACKAGE.iterdir() if path.is_file()}
    coefficient_floor = min(
        math.hypot(coefficient_a0(z), coefficient_a1(z))
        for z in linspace(-math.pi, math.pi, 4001)
    )
    ratios = dict((label, value) for label, value, _ in no_go_ratios())
    checks = {
        "identity": config.get("figureId") == FIGURE_ID and contract.get("figureId") == FIGURE_ID,
        "dimensions": (
            config.get("widthMillimetres") == WIDTH_MM
            and config.get("heightMillimetres") == HEIGHT_MM
            and config.get("pngDpi") == PNG_DPI
        ),
        "exactLifecycleInventory": package_files in (
            set(SOURCE_FILES),
            set(SOURCE_FILES) | set(GENERATED_FILES),
        ),
        "analyticRows": len(rows) == EXPECTED_ANALYTIC_ROWS,
        "panelSet": {row["panel"] for row in rows} == {"A", "B"},
        "coefficientGeometryNonzero": coefficient_floor > 0.5,
        "h5NoGo": abs(ratios["alpha^2 H5 / 4"] - 5.0 * math.pi**2 / 12.0) < 1.0e-15,
        "h5RatioAboveOne": ratios["alpha^2 H5 / 4"] > 1.0,
        "diagnosticConfiguration": (
            config.get("panelC", {}).get("alphas") == list(DIAGNOSTIC_ALPHAS)
            and config.get("panelC", {}).get("levels")
            == [
                {"label": label, "spatialModes": n_value, "timeSteps": steps}
                for label, n_value, steps in DIAGNOSTIC_LEVELS
            ]
            and config.get("panelC", {}).get("powerIterations") == POWER_ITERATIONS
        ),
        "diagnosticDeferred": (
            contract.get("numericalDiagnosticPlanned") is True
            and contract.get("simulationPerformedAtSourceStage") is False
        ),
        "claimBoundary": (
            contract.get("claimBoundary", {}).get("exactPeriodicGraphCoercivityProved") is True
            and contract.get("claimBoundary", {}).get("exactPeriodicBlockContractionProved") is True
            and contract.get("claimBoundary", {}).get("numericalDiagnosticIsProof") is False
            and contract.get("claimBoundary", {}).get("outerTimeConcatenationProved") is False
            and contract.get("claimBoundary", {}).get("clayMillenniumProblemSolved") is False
        ),
        "hardTwoRootPalette": (
            contract.get("palette", {}).get("chromaticRoots") == [BLUE, GOLD]
            and contract.get("palette", {}).get("hardChromaticRootCap") == 2
        ),
        "blossomContract": contract.get("researchBlossom") == {
            "carriesData": False,
            "lockedAnchor": "top-right-header",
            "petalCount": 5,
        },
        "sceneBuilt": len(scene.items) > 100,
        "closedVisible": "exact periodic scalar-row block contraction: CLOSED" in scene_text,
        "openVisible": "outer concatenation / nonlinear / Clay: OPEN" in scene_text,
        "diagnosticVisible": "NUMERICAL DIAGNOSTIC ONLY — NOT PROOF" in scene_text,
    }
    if not all(checks.values()):
        raise RuntimeError(f"R0.72W figure source self-test failed: {checks}")
    print(
        "R0.72W figure source self-test: passed "
        f"({len(rows)} analytic in-memory rows; no outputs written)"
    )


def main() -> None:
    started = time.perf_counter()
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--draft", action="store_true")
    mode.add_argument("--formal", action="store_true")
    parser.add_argument("--visual-inspected", action="store_true")
    parser.add_argument("--source-commit")
    parser.add_argument("--certificate-commit")
    args = parser.parse_args()

    if args.self_test:
        if args.visual_inspected or args.source_commit or args.certificate_commit:
            parser.error("--self-test cannot be combined with generation arguments")
        self_test()
        return
    if not args.draft and not args.formal:
        parser.error("choose --self-test, --draft, or --formal")

    certificate_manifest, certificate = validate_formal_certificate()
    if args.formal:
        if git_status_dirty():
            raise RuntimeError("formal figure generation requires a completely clean tree")
        if not args.visual_inspected:
            raise RuntimeError("formal figure generation requires --visual-inspected")
        validate_formal_lineage(
            certificate_manifest,
            args.source_commit,
            args.certificate_commit,
        )
        reject_output_overwrite(include_public=True)
    else:
        if args.visual_inspected or args.source_commit or args.certificate_commit:
            parser.error("draft generation does not accept formal lineage flags")
        reject_output_overwrite(include_public=False)

    (PACKAGE / "progress.ndjson").write_text(
        json.dumps({
            "event": "build-start",
            "mode": "formal" if args.formal else "draft",
            "totalDiagnostics": EXPECTED_NUMERICAL_ROWS,
        }, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    def progress(event: dict[str, Any]) -> None:
        with (PACKAGE / "progress.ndjson").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True) + "\n")

    analytic = analytic_rows()
    numeric, numerical_summary = numerical_rows(progress)
    rows = analytic + numeric
    save_data(rows)
    scene = build_scene(numeric)
    render_svg(scene)
    render_pdf(scene)
    render_png(scene)
    build_qa()
    build_archive(
        rows,
        numerical_summary,
        formal=args.formal,
        visual_inspected=args.visual_inspected,
        source_commit=args.source_commit,
        certificate_commit=args.certificate_commit,
        certificate=certificate,
        wall_time_seconds=time.perf_counter() - started,
    )
    print(
        f"R0.72W {'formal' if args.formal else 'draft'} figure package: "
        f"passed ({len(rows)} rows; numerical diagnostic only)"
    )


if __name__ == "__main__":
    main()
