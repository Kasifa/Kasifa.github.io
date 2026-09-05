#!/usr/bin/env python3
"""Generate/check the deterministic R0.76L parabolic-edge diagnostic.

This is a finite presentation diagnostic, not a PDE solver and not a proof.
Formal mode writes data.csv, figure.svg, progress.ndjson, and resources.csv.
Check mode recomputes data.csv and figure.svg in memory and fails on any byte
difference.  The separate render.cjs converts the SVG to PDF and 600 dpi PNG.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import math
import os
from pathlib import Path
import platform
import resource
import sys
import time

import numpy as np


PACKAGE = Path(__file__).resolve().parent
CONFIG = PACKAGE / "config.json"
DATA = PACKAGE / "data.csv"
SVG = PACKAGE / "figure.svg"
PROGRESS = PACKAGE / "progress.ndjson"
RESOURCES = PACKAGE / "resources.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--formal", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.formal == args.check:
        parser.error("choose exactly one of --formal or --check")
    return args


def validate_config(config: dict) -> None:
    if config.get("schema") != "r076l-parabolic-edge-diagnostic-v1":
        raise ValueError("unexpected figure schema")
    if not math.isclose(float(config["heatTime"]), 4.0, rel_tol=0.0, abs_tol=0.0):
        raise ValueError("the frozen caption and panel labels require heatTime=4")
    if [float(value) for value in config["edgeCoordinates"]] != [0.0, 1.0]:
        raise ValueError("the frozen unit-tilt diagnostic requires edgeCoordinates=[0,1]")
    A_values = [int(value) for value in config["AValues"]]
    if len(A_values) < 2 or A_values != sorted(set(A_values)) or A_values[0] <= 1:
        raise ValueError("AValues must be strictly increasing integers greater than one")
    powers = [float(value) for value in config["degreePowers"]]
    if len(powers) != 4 or powers != sorted(set(powers)):
        raise ValueError("the frozen four-style figure requires four increasing powers")
    fine = int(config["fineGridPoints"])
    coarse = int(config["coarseGridPoints"])
    if coarse < 1001 or fine <= coarse:
        raise ValueError("fineGridPoints must exceed a coarse grid of at least 1001 points")
    if float(config["phaseDrop"]) < 32.0:
        raise ValueError("phaseDrop must be at least 32")
    if int(config["figureWidthMillimetres"]) != 178 or int(
        config["figureHeightMillimetres"]
    ) != 72:
        raise ValueError("the frozen journal figure size is 178 mm x 72 mm")


def log_cosh(value: float) -> float:
    absolute = abs(value)
    return absolute + math.log1p(math.exp(-2.0 * absolute)) - math.log(2.0)


def phase(y: float, A: int, m: int, c: float, heat_time: float) -> float:
    angle = math.acosh(1.0 + y / A)
    return log_cosh(m * angle) - (y - c) ** 2 / (4.0 * heat_time)


def phase_derivative(y: float, A: int, m: int, c: float, heat_time: float) -> float:
    angle = math.acosh(1.0 + y / A)
    chebyshev = m * math.tanh(m * angle) / math.sqrt(y * (2.0 * A + y))
    return chebyshev - (y - c) / (2.0 * heat_time)


def saddle(A: int, m: int, c: float, heat_time: float) -> float:
    lower = max(c, 1.0e-14)
    upper = max(1.0, c + 1.0)
    while phase_derivative(upper, A, m, c, heat_time) > 0.0:
        upper *= 2.0
    for _ in range(120):
        middle = 0.5 * (lower + upper)
        if phase_derivative(middle, A, m, c, heat_time) > 0.0:
            lower = middle
        else:
            upper = middle
    return 0.5 * (lower + upper)


def log_positive_integral(
    A: int, m: int, c: float, heat_time: float, points: int, phase_drop: float
) -> tuple[float, float]:
    optimum = saddle(A, m, c, heat_time)
    maximum = phase(optimum, A, m, c, heat_time)
    if phase(0.0, A, m, c, heat_time) > maximum - phase_drop:
        left = 0.0
    else:
        left = optimum
        while phase(left, A, m, c, heat_time) > maximum - phase_drop:
            left *= 0.75
    right = optimum
    while phase(right, A, m, c, heat_time) > maximum - phase_drop:
        right *= 1.25
    grid = np.linspace(max(0.0, left), right, points)
    angle = np.arccosh(1.0 + grid / A)
    argument = m * angle
    values = (
        np.logaddexp(argument, -argument)
        - math.log(2.0)
        - (grid - c) ** 2 / (4.0 * heat_time)
    )
    integral = np.trapezoid(np.exp(values - maximum), grid)
    logarithm = maximum + math.log(float(integral)) - 0.5 * math.log(
        4.0 * math.pi * heat_time
    )
    return logarithm, optimum


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds")


def rss_mib() -> float:
    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # macOS reports bytes; Linux reports KiB.
    divisor = 1024.0**2 if sys.platform == "darwin" else 1024.0
    return raw / divisor


def even_degree(A: int, power: float) -> int:
    return max(2, 2 * int(round((A**power) / 2.0)))


def compute(config: dict, progress_callback=None) -> list[dict[str, str]]:
    heat_time = float(config["heatTime"])
    c0, c1 = map(float, config["edgeCoordinates"])
    fine_points = int(config["fineGridPoints"])
    coarse_points = int(config["coarseGridPoints"])
    phase_drop = float(config["phaseDrop"])
    edge_width = c1 - c0
    z_limit = 2.0 ** (1.0 / 3.0) * heat_time ** (2.0 / 3.0)
    amplitude_limit = 3.0 * 2.0 ** (-4.0 / 3.0) * heat_time ** (1.0 / 3.0)
    tilt_limit = 2.0 ** (-2.0 / 3.0) * heat_time ** (-1.0 / 3.0)
    cases = [
        (int(A), float(power))
        for A in config["AValues"]
        for power in config["degreePowers"]
    ]
    rows: list[dict[str, str]] = []
    for index, (A, power) in enumerate(cases, start=1):
        m = even_degree(A, power)
        mu = (m * m / A) ** (1.0 / 3.0)
        fine0, y0 = log_positive_integral(
            A, m, c0, heat_time, fine_points, phase_drop
        )
        fine1, _ = log_positive_integral(
            A, m, c1, heat_time, fine_points, phase_drop
        )
        coarse0, _ = log_positive_integral(
            A, m, c0, heat_time, coarse_points, phase_drop
        )
        coarse1, _ = log_positive_integral(
            A, m, c1, heat_time, coarse_points, phase_drop
        )
        deep0, _ = log_positive_integral(
            A, m, c0, heat_time, fine_points, phase_drop + 16.0
        )
        deep1, _ = log_positive_integral(
            A, m, c1, heat_time, fine_points, phase_drop + 16.0
        )
        y_scaled = y0 / mu
        amplitude_scaled = fine0 / (mu * mu)
        tilt_scaled = (fine1 - fine0) / (mu * edge_width)
        coarse_amplitude = coarse0 / (mu * mu)
        coarse_tilt = (coarse1 - coarse0) / (mu * edge_width)
        deep_amplitude = deep0 / (mu * mu)
        deep_tilt = (deep1 - deep0) / (mu * edge_width)
        rows.append(
            {
                "A": str(A),
                "degreePower": f"{power:.2f}",
                "m": str(m),
                "mu": f"{mu:.12f}",
                "saddleOverMu": f"{y_scaled:.12f}",
                "logIntegralOverMuSquared": f"{amplitude_scaled:.12f}",
                "unitTiltOverMu": f"{tilt_scaled:.12f}",
                "saddleLimit": f"{z_limit:.12f}",
                "amplitudeLimit": f"{amplitude_limit:.12f}",
                "tiltLimit": f"{tilt_limit:.12f}",
                "saddleError": f"{y_scaled-z_limit:.12e}",
                "amplitudeError": f"{amplitude_scaled-amplitude_limit:.12e}",
                "tiltError": f"{tilt_scaled-tilt_limit:.12e}",
                "saddleDerivativeResidual": f"{abs(phase_derivative(y0, A, m, c0, heat_time)):.12e}",
                "coarseFineAmplitudeDelta": f"{abs(amplitude_scaled-coarse_amplitude):.12e}",
                "coarseFineTiltDelta": f"{abs(tilt_scaled-coarse_tilt):.12e}",
                "phaseDropAmplitudeDelta": f"{abs(amplitude_scaled-deep_amplitude):.12e}",
                "phaseDropTiltDelta": f"{abs(tilt_scaled-deep_tilt):.12e}",
            }
        )
        if progress_callback:
            progress_callback(index, len(cases), A, power, m, mu)
    return rows


def validate_rows(rows: list[dict[str, str]], config: dict) -> dict[str, float]:
    expected = len(config["AValues"]) * len(config["degreePowers"])
    if len(rows) != expected:
        raise ValueError(f"expected {expected} rows, found {len(rows)}")
    nonnumeric = {""}
    for row in rows:
        for field, value in row.items():
            if value in nonnumeric:
                raise ValueError(f"empty numeric field: {field}")
            if not math.isfinite(float(value)):
                raise ValueError(f"non-finite numeric field: {field}={value}")
    max_saddle = max(float(row["saddleDerivativeResidual"]) for row in rows)
    max_grid = max(
        max(float(row["coarseFineAmplitudeDelta"]), float(row["coarseFineTiltDelta"]))
        for row in rows
    )
    max_tail = max(
        max(float(row["phaseDropAmplitudeDelta"]), float(row["phaseDropTiltDelta"]))
        for row in rows
    )
    if max_saddle > 1.0e-9:
        raise ValueError(f"saddle residual gate failed: {max_saddle:.3e}")
    if max_grid > 1.0e-8:
        raise ValueError(f"coarse/fine gate failed: {max_grid:.3e}")
    if max_tail > 1.0e-8:
        raise ValueError(f"phase-drop sensitivity gate failed: {max_tail:.3e}")
    return {
        "maximumSaddleResidual": max_saddle,
        "maximumCoarseFineDelta": max_grid,
        "maximumPhaseDropDelta": max_tail,
    }


def csv_bytes(rows: list[dict[str, str]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def svg_bytes(rows: list[dict[str, str]], config: dict) -> bytes:
    width, height = 1780, 720
    left, right, top, bottom, gap = 150, 25, 125, 105, 150
    panel_width = (width - left - right - 2 * gap) / 3.0
    panel_height = height - top - bottom
    panels = [
        ("saddleOverMu", (2.90, 3.205), "y* / μ", "(a)"),
        ("logIntegralOverMuSquared", (1.70, 1.905), "ln I(4,0) / μ²", "(b)"),
        (
            "unitTiltOverMu",
            (0.360, 0.4005),
            "[ln I(4,1) − ln I(4,0)] / μ",
            "(c)",
        ),
    ]
    limits = {
        "saddleOverMu": float(rows[0]["saddleLimit"]),
        "logIntegralOverMuSquared": float(rows[0]["amplitudeLimit"]),
        "unitTiltOverMu": float(rows[0]["tiltLimit"]),
    }
    powers = sorted({float(row["degreePower"]) for row in rows})
    styles = {
        powers[0]: ("#111111", "", "circle"),
        powers[1]: ("#444444", "10 5", "square"),
        powers[2]: ("#777777", "3 4", "triangle"),
        powers[3]: ("#999999", "12 4 2 4", "diamond"),
    }
    x_ticks = sorted({math.log2(int(row["A"])) for row in rows})
    x_min, x_max = min(x_ticks), max(x_ticks)

    def sx(value: float, panel: int) -> float:
        x0 = left + panel * (panel_width + gap)
        return x0 + (value - x_min) / (x_max - x_min) * panel_width

    def sy(value: float, bounds: tuple[float, float]) -> float:
        lower, upper = bounds
        return top + (upper - value) / (upper - lower) * panel_height

    def marker(kind: str, x: float, y: float, color: str) -> str:
        radius = 7.0
        if kind == "circle":
            return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius}" fill="white" stroke="{color}" stroke-width="2.6"/>'
        if kind == "square":
            return f'<rect x="{x-radius:.2f}" y="{y-radius:.2f}" width="{2*radius}" height="{2*radius}" fill="white" stroke="{color}" stroke-width="2.6"/>'
        if kind == "triangle":
            points = f"{x:.2f},{y-radius-1:.2f} {x-radius-1:.2f},{y+radius:.2f} {x+radius+1:.2f},{y+radius:.2f}"
            return f'<polygon points="{points}" fill="white" stroke="{color}" stroke-width="2.6"/>'
        points = f"{x:.2f},{y-radius-2:.2f} {x+radius+2:.2f},{y:.2f} {x:.2f},{y+radius+2:.2f} {x-radius-2:.2f},{y:.2f}"
        return f'<polygon points="{points}" fill="white" stroke="{color}" stroke-width="2.6"/>'

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="178mm" height="72mm" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<g font-family="Georgia, Times New Roman, serif" fill="#222222">',
    ]
    for panel_index, (field, bounds, ylabel, label) in enumerate(panels):
        x0 = left + panel_index * (panel_width + gap)
        x1 = x0 + panel_width
        y0 = top
        y1 = top + panel_height
        elements.append(
            f'<path d="M{x0:.2f},{y0:.2f} V{y1:.2f} H{x1:.2f}" fill="none" stroke="#222222" stroke-width="2.2"/>'
        )
        for tick in x_ticks:
            x = sx(tick, panel_index)
            tick_label = f"{tick:g}"
            elements.append(f'<path d="M{x:.2f},{y1:.2f} v8" stroke="#222222" stroke-width="1.8"/>')
            elements.append(f'<text x="{x:.2f}" y="{y1+35:.2f}" text-anchor="middle" font-size="25">{tick_label}</text>')
        lower, upper = bounds
        for fraction in (0.0, 0.5, 1.0):
            value = lower + fraction * (upper - lower)
            y = sy(value, bounds)
            elements.append(f'<path d="M{x0-8:.2f},{y:.2f} h8" stroke="#222222" stroke-width="1.8"/>')
            elements.append(f'<text x="{x0-14:.2f}" y="{y+8:.2f}" text-anchor="end" font-size="23">{value:.3f}</text>')
        theory_y = sy(limits[field], bounds)
        elements.append(
            f'<path d="M{x0:.2f},{theory_y:.2f} H{x1:.2f}" stroke="#111111" stroke-width="2.0" stroke-dasharray="5 5"/>'
        )
        for power in powers:
            color, dash, kind = styles[power]
            series = sorted(
                (row for row in rows if float(row["degreePower"]) == power),
                key=lambda row: int(row["A"]),
            )
            points = [
                (sx(math.log2(int(row["A"])), panel_index), sy(float(row[field]), bounds))
                for row in series
            ]
            path = " ".join(
                ("M" if index == 0 else "L") + f"{x:.2f},{y:.2f}"
                for index, (x, y) in enumerate(points)
            )
            dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
            elements.append(
                f'<path d="{path}" fill="none" stroke="{color}" stroke-width="3.0"{dash_attr}/>'
            )
            elements.extend(marker(kind, x, y, color) for x, y in points)
        elements.append(f'<text x="{x0:.2f}" y="{y0-20:.2f}" font-size="30" font-weight="bold">{label}</text>')
        elements.append(f'<text x="{(x0+x1)/2:.2f}" y="{height-25:.2f}" text-anchor="middle" font-size="27">log₂ A</text>')
        elements.append(
            f'<text x="{x0-105:.2f}" y="{(y0+y1)/2:.2f}" text-anchor="middle" font-size="24" transform="rotate(-90 {x0-105:.2f} {(y0+y1)/2:.2f})">{ylabel}</text>'
        )
    legend_y = 43.0
    legend_x = 300.0
    for index, power in enumerate(powers):
        color, dash, kind = styles[power]
        x = legend_x + index * 240.0
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        elements.append(f'<path d="M{x:.2f},{legend_y:.2f} h55" stroke="{color}" stroke-width="3"{dash_attr}/>')
        elements.append(marker(kind, x + 27.5, legend_y, color))
        elements.append(f'<text x="{x+68:.2f}" y="{legend_y+9:.2f}" font-size="27">p = {power:.2f}</text>')
    elements.append('<path d="M1260,43 h55" stroke="#111111" stroke-width="2" stroke-dasharray="5 5"/>')
    elements.append('<text x="1328" y="52" font-size="27">analytic limit</text>')
    elements.extend(["</g>", "</svg>", ""])
    return "\n".join(elements).encode("utf-8")


def main() -> int:
    args = parse_args()
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    start_wall = time.perf_counter()
    start_cpu = time.process_time()
    progress_records: list[dict] = []
    resource_records: list[dict] = []

    def snapshot(stage: str, **extra) -> None:
        elapsed = time.perf_counter() - start_wall
        cpu = time.process_time() - start_cpu
        progress_records.append(
            {
                "timestampUtc": utc_now(),
                "elapsedSeconds": round(elapsed, 6),
                "stage": stage,
                **extra,
            }
        )
        resource_records.append(
            {
                "timestampUtc": utc_now(),
                "elapsedSeconds": f"{elapsed:.6f}",
                "stage": stage,
                "processes": "1",
                "logicalCpuCount": str(os.cpu_count() or 1),
                "cpuPercentProcessApprox": f"{(100.0*cpu/max(elapsed,1e-9)):.3f}",
                "rssMiB": f"{rss_mib():.3f}",
                "gpuUtilPercent": "",
                "gpuMemoryMiB": "",
                "gpuTemperatureC": "",
            }
        )

    snapshot("start", cases=len(config["AValues"]) * len(config["degreePowers"]))

    def progress(index: int, total: int, A: int, power: float, m: int, mu: float) -> None:
        snapshot(
            "quadrature",
            step=index,
            totalSteps=total,
            A=A,
            degreePower=power,
            m=m,
            mu=round(mu, 8),
            estimatedSecondsRemaining=round(
                (time.perf_counter() - start_wall) / index * (total - index), 6
            ),
        )

    validate_config(config)
    rows = compute(config, progress if args.formal else None)
    gates = validate_rows(rows, config)
    rendered_csv = csv_bytes(rows)
    rendered_svg = svg_bytes(rows, config)
    if args.check:
        failures = []
        for path, rendered in ((DATA, rendered_csv), (SVG, rendered_svg)):
            if not path.is_file() or path.read_bytes() != rendered:
                failures.append(path.name)
        if failures:
            print("R0.76L figure check failed:", ", ".join(failures), file=sys.stderr)
            return 1
        print(
            json.dumps(
                {
                    "verdict": "PASS",
                    "rows": len(rows),
                    "checked": [DATA.name, SVG.name],
                    "python": platform.python_version(),
                    "numpy": np.__version__,
                    **gates,
                },
                sort_keys=True,
            )
        )
        return 0
    DATA.write_bytes(rendered_csv)
    SVG.write_bytes(rendered_svg)
    snapshot(
        "complete",
        rows=len(rows),
        outputData=DATA.name,
        outputFigure=SVG.name,
        status="PASS",
    )
    PROGRESS.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in progress_records),
        encoding="utf-8",
    )
    with RESOURCES.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=list(resource_records[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(resource_records)
    wall = time.perf_counter() - start_wall
    print(
        json.dumps(
            {
                "verdict": "PASS",
                "rows": len(rows),
                "wallTimeSeconds": round(wall, 6),
                **gates,
                "progressEvents": len(progress_records),
                "resourceSamples": len(resource_records),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
