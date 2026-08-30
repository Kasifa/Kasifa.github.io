#!/usr/bin/env python3
"""Independent raw-ODE corroboration on 83 frozen R0.73J natural boxes.

The program is self-contained apart from python-flint.  It does not import the
primary ODE core, contour driver, Clenshaw analyzer, or shared-grid auditor.
It reconstructs the 27 mandatory global-left boxes, 24 mandatory local-circle
boxes, and 32 digest-selected primary subdivision boxes from the design frozen
in ``independent_validation.json``.  Every box is integrated at its original
width; failures are recorded and are never repaired by shrinking a box.

This is corroborative spot checking, not a cover of either spectral contour.
Even a clean 83/83 result cannot replace the parameter-uniform certificate.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import platform
import resource
import shutil
import sys
import threading
import time
from typing import Any, Iterable, Sequence

import flint
from flint import acb, arb, ctx


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SCHEMA_VERSION = "r073j-independent-natural-box-ode-v1"
ORDER = 14
PRECISION_DPS = 120
GLOBAL_STEPS = 2048
LOCAL_STEPS = 1024
WORKERS = 16
RESOURCE_INTERVAL_SECONDS = 5
EXPECTED_BOX_COUNT = 83
EXPECTED_PYTHON_FLINT = "0.6.0"
WORKER_SETTINGS: dict[str, Any] = {}


class ValidationFailure(RuntimeError):
    """Fail-closed input, interval, or decision failure."""


class OdeAudit:
    def __init__(self, steps: int) -> None:
        self.steps = steps
        self.minimum_denominator: arb | None = None
        self.minimum_tube_slack: arb | None = None
        self.maximum_tube_attempt = 0

    def denominator(self, value: arb) -> None:
        if self.minimum_denominator is None or value.lower() < self.minimum_denominator.lower():
            self.minimum_denominator = value

    def slack(self, value: arb) -> None:
        if self.minimum_tube_slack is None or value.lower() < self.minimum_tube_slack.lower():
            self.minimum_tube_slack = value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def compact_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(canonical_json(value), encoding="utf-8")
    os.replace(temporary, path)


def append_ndjson(path: Path, value: object) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(compact_json(value) + "\n")


def initialize_ndjson(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(compact_json(value) + "\n", encoding="utf-8")


def expect_keys(
    value: Any,
    required: Iterable[str],
    label: str,
    optional: Iterable[str] = (),
) -> dict[str, Any]:
    require(type(value) is dict, f"{label} must be an object")
    required_set = set(required)
    allowed = required_set | set(optional)
    actual = set(value)
    require(not (required_set - actual),
            f"{label} missing keys: {sorted(required_set - actual)}")
    require(not (actual - allowed),
            f"{label} has unexpected keys: {sorted(actual - allowed)}")
    return value


def expect_int(value: Any, label: str, minimum: int | None = None) -> int:
    require(type(value) is int, f"{label} must be an integer")
    if minimum is not None:
        require(value >= minimum, f"{label} must be at least {minimum}")
    return value


def parse_fraction(value: Any, label: str) -> Fraction:
    require(type(value) is str and value != "", f"{label} must be a rational string")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ValidationFailure(f"{label} is not a rational") from error


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def arb_fraction(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def arb_interval(lower: Fraction, upper: Fraction) -> arb:
    require(lower <= upper, "reversed rational interval")
    return arb_fraction(lower).union(arb_fraction(upper))


def arb_text(value: arb, digits: int = 110) -> str:
    return value.str(digits, more=True)


def acb_record(value: acb) -> dict[str, str]:
    return {"real": arb_text(value.real), "imag": arb_text(value.imag)}


def fraction_interval_record(lower: Fraction, upper: Fraction) -> dict[str, str]:
    return {"lower": fraction_text(lower), "upper": fraction_text(upper)}


def component_hull(left: acb, right: acb) -> acb:
    return acb(left.real.union(right.real), left.imag.union(right.imag))


def vector_hull(left: Sequence[acb], right: Sequence[acb]) -> list[acb]:
    require(len(left) == len(right), "vector hull length mismatch")
    return [component_hull(a, b) for a, b in zip(left, right)]


def inflate_box(value: acb, multiplier: int, absolute: arb) -> acb:
    require(multiplier >= 1 and absolute.lower() > 0, "invalid box inflation")
    return acb(
        arb(value.real.mid(), multiplier * value.real.rad() + absolute),
        arb(value.imag.mid(), multiplier * value.imag.rad() + absolute),
    )


def vector_contains(outer: Sequence[acb], inner: Sequence[acb]) -> bool:
    return len(outer) == len(inner) and all(
        outer_value.contains(inner_value)
        for outer_value, inner_value in zip(outer, inner)
    )


def component_clearance(outer: acb, inner: acb) -> arb:
    return min(
        inner.real.lower() - outer.real.lower(),
        outer.real.upper() - inner.real.upper(),
        inner.imag.lower() - outer.imag.lower(),
        outer.imag.upper() - inner.imag.upper(),
        key=lambda value: value.lower(),
    )


def rhs(
    state: Sequence[acb],
    d_box: arb,
    spectral_box: acb,
    audit: OdeAudit,
) -> list[acb]:
    require(len(state) == 8, "ODE state must have eight components")
    sin_x, cos_x, sin_two_x, cos_two_x = state[:4]
    decay_one = (-d_box).exp()
    decay_four = (-4 * d_box).exp()
    velocity = -decay_one * sin_x / 2 + decay_four * sin_two_x / 4
    curvature = decay_one * sin_x / 2 - decay_four * sin_two_x
    denominator = velocity - 2j * spectral_box
    denominator_lower = denominator.abs_lower()
    audit.denominator(denominator_lower)
    require(denominator_lower.lower() > 0,
            "Rayleigh denominator interval contains zero")
    potential = arb(1) / 4 + curvature / denominator
    result = [cos_x, -sin_x, 2 * cos_two_x, -2 * sin_two_x]
    for offset in (4, 6):
        result.extend((state[offset + 1], potential * state[offset]))
    return result


def series_convolution(
    left: Sequence[acb], right: Sequence[acb], degree: int
) -> list[acb]:
    return [
        sum((left[index] * right[order - index]
             for index in range(order + 1)), acb(0))
        for order in range(degree + 1)
    ]


def reciprocal_series(values: Sequence[acb], degree: int) -> list[acb]:
    require(len(values) >= degree + 1, "short reciprocal input series")
    require(not values[0].contains(0), "series denominator constant contains zero")
    result = [acb(0) for _ in range(degree + 1)]
    result[0] = 1 / values[0]
    for order in range(1, degree + 1):
        convolution = sum(
            (values[index] * result[order - index]
             for index in range(1, order + 1)),
            acb(0),
        )
        result[order] = -result[0] * convolution
    return result


def normalized_series(
    initial: Sequence[acb],
    d_box: arb,
    spectral_box: acb,
    degree: int,
    audit: OdeAudit,
) -> list[list[acb]]:
    """Compute normalized time coefficients y^(k)/k! through ``degree``."""
    require(degree >= 1 and len(initial) == 8, "invalid Taylor series request")
    coefficients = [[acb(0) for _ in range(degree + 1)] for _ in range(8)]
    for component, value in enumerate(initial):
        coefficients[component][0] = value

    for order in range(degree):
        coefficients[0][order + 1] = coefficients[1][order] / (order + 1)
        coefficients[1][order + 1] = -coefficients[0][order] / (order + 1)
        coefficients[2][order + 1] = 2 * coefficients[3][order] / (order + 1)
        coefficients[3][order + 1] = -2 * coefficients[2][order] / (order + 1)

    decay_one = (-d_box).exp()
    decay_four = (-4 * d_box).exp()
    velocity = [
        -decay_one * coefficients[0][order] / 2
        + decay_four * coefficients[2][order] / 4
        for order in range(degree + 1)
    ]
    curvature = [
        decay_one * coefficients[0][order] / 2
        - decay_four * coefficients[2][order]
        for order in range(degree + 1)
    ]
    denominator = list(velocity)
    denominator[0] -= 2j * spectral_box
    denominator_lower = denominator[0].abs_lower()
    audit.denominator(denominator_lower)
    require(denominator_lower.lower() > 0,
            "Taylor-series denominator contains zero")
    potential = series_convolution(
        curvature, reciprocal_series(denominator, degree), degree
    )
    potential[0] += arb(1) / 4

    for offset in (4, 6):
        solution = [acb(0) for _ in range(degree + 2)]
        solution[0] = initial[offset]
        solution[1] = initial[offset + 1]
        for order in range(degree):
            acceleration = sum(
                (potential[index] * solution[order - index]
                 for index in range(order + 1)),
                acb(0),
            )
            solution[order + 2] = (
                acceleration / ((order + 2) * (order + 1))
            )
        for order in range(degree + 1):
            coefficients[offset][order] = solution[order]
            coefficients[offset + 1][order] = (order + 1) * solution[order + 1]
    return coefficients


def horner(coefficients: Sequence[acb], step: arb, stop: int) -> acb:
    require(0 <= stop < len(coefficients), "invalid Horner truncation")
    result = coefficients[stop]
    for order in range(stop - 1, -1, -1):
        result = coefficients[order] + step * result
    return result


def close_picard_tube(
    initial: Sequence[acb],
    d_box: arb,
    spectral_box: acb,
    step: arb,
    audit: OdeAudit,
    maximum_attempts: int = 32,
) -> list[acb]:
    initial_rhs = rhs(initial, d_box, spectral_box, audit)
    euler = [value + step * derivative
             for value, derivative in zip(initial, initial_rhs)]
    base = vector_hull(initial, euler)
    # Deliberately differs from the primary search constant.  It is only a
    # search policy; the two explicit containment tests below are decisive.
    absolute = 128 * step * step + arb("1e-100")
    for attempt in range(maximum_attempts):
        multiplier = 2 ** attempt
        candidate = [
            inflate_box(value, 1, absolute) for value in base[:4]
        ] + [
            inflate_box(value, multiplier, multiplier * absolute)
            for value in base[4:]
        ]
        candidate_rhs = rhs(candidate, d_box, spectral_box, audit)
        endpoint_image = [
            value + step * derivative
            for value, derivative in zip(initial, candidate_rhs)
        ]
        if vector_contains(candidate, initial) and vector_contains(
            candidate, endpoint_image
        ):
            clearances = [
                component_clearance(outer, inner)
                for outer, inner in zip(candidate, initial)
            ] + [
                component_clearance(outer, inner)
                for outer, inner in zip(candidate, endpoint_image)
            ]
            for clearance in clearances:
                audit.slack(clearance)
            audit.maximum_tube_attempt = max(audit.maximum_tube_attempt, attempt)
            return candidate
    raise ValidationFailure("Picard tube failed to close at frozen box width")


def validated_step(
    initial: Sequence[acb],
    d_box: arb,
    spectral_box: acb,
    step: arb,
    order: int,
    audit: OdeAudit,
) -> list[acb]:
    tube = close_picard_tube(initial, d_box, spectral_box, step, audit)
    launch = normalized_series(
        initial, d_box, spectral_box, order - 1, audit
    )
    remainder = normalized_series(
        tube, d_box, spectral_box, order, audit
    )
    return [
        horner(launch[component], step, order - 1)
        + step ** order * remainder[component][order]
        for component in range(8)
    ]


def exact_clock(x_value: arb) -> list[acb]:
    return [
        acb(x_value.sin()),
        acb(x_value.cos()),
        acb((2 * x_value).sin()),
        acb((2 * x_value).cos()),
    ]


def interval_evans(
    d_box: arb,
    spectral_box: acb,
    steps: int,
    order: int,
    audit: OdeAudit,
) -> acb:
    require(steps >= 1 and order >= 2, "invalid ODE discretization")
    step = 2 * arb.pi() / steps
    state = [acb(value) for value in (0, 1, 0, 1, 1, 0, 0, 1)]
    for step_index in range(steps):
        state = validated_step(
            state, d_box, spectral_box, step, order, audit
        )
        # The clock subsystem is known exactly and independent of parameters.
        # Resetting it to its rigorous trigonometric value avoids carrying
        # artificial wrapping into the next tube while leaving the fundamental
        # matrix enclosure untouched.
        x_next = (step_index + 1) * step
        state[:4] = exact_clock(x_next)
    return 2 - state[4] - state[7]


def panel_definitions(config: dict[str, Any]) -> list[dict[str, Any]]:
    global_config = config["global"]
    left = Fraction(global_config["boundary"]["left"])
    outer = Fraction(global_config["boundary"]["outer"])
    horizontal_count = global_config["horizontalPanelsPerEdge"]
    vertical_count = global_config["verticalPanelsPerEdge"]
    horizontal_width = (outer - left) / horizontal_count
    vertical_width = 2 * outer / vertical_count
    panels: list[dict[str, Any]] = []

    def line(
        panel_id: str,
        edge: str,
        center_real: Fraction,
        center_imag: Fraction,
        half_real: Fraction,
        half_imag: Fraction,
    ) -> dict[str, Any]:
        return {
            "id": panel_id,
            "family": "global",
            "kind": "line",
            "edge": edge,
            "centerReal": fraction_text(center_real),
            "centerImag": fraction_text(center_imag),
            "halfReal": fraction_text(half_real),
            "halfImag": fraction_text(half_imag),
        }

    for index in range(horizontal_count):
        center = left + Fraction(2 * index + 1, 2) * horizontal_width
        panels.append(line(f"G-bottom-{index:02d}", "bottom", center, -outer,
                           horizontal_width / 2, Fraction(0)))
    for index in range(vertical_count):
        center = -outer + Fraction(2 * index + 1, 2) * vertical_width
        panels.append(line(f"G-right-{index:02d}", "right", outer, center,
                           Fraction(0), vertical_width / 2))
    for index in range(horizontal_count):
        center = outer - Fraction(2 * index + 1, 2) * horizontal_width
        panels.append(line(f"G-top-{index:02d}", "top", center, outer,
                           -horizontal_width / 2, Fraction(0)))
    for index in range(vertical_count):
        center = outer - Fraction(2 * index + 1, 2) * vertical_width
        panels.append(line(f"G-left-{index:02d}", "left", left, center,
                           Fraction(0), -vertical_width / 2))
    local_count = config["local"]["panels"]
    for index in range(local_count):
        panels.append({
            "id": f"L-circle-{index:02d}",
            "family": "local",
            "kind": "circle",
            "thetaCenterPi": fraction_text(Fraction(2 * index + 1, local_count)),
            "thetaHalfPi": fraction_text(Fraction(1, local_count)),
        })
    return panels


def dyadic_bounds(index: int, depth: int) -> tuple[Fraction, Fraction]:
    require(depth >= 0 and 0 <= index < 2 ** depth, "invalid dyadic selector")
    denominator = 2 ** depth
    return (
        Fraction(-1) + Fraction(2 * index, denominator),
        Fraction(-1) + Fraction(2 * (index + 1), denominator),
    )


def build_cases(
    config: dict[str, Any], design: dict[str, Any]
) -> list[dict[str, Any]]:
    require(design["status"] == "design-only-not-executed",
            "natural-box design is not in its frozen pre-execution state")
    require(expect_int(design["totalBoxes"], "design.totalBoxes", 1)
            == EXPECTED_BOX_COUNT, "natural-box total is not 83")
    maximum_d = Fraction(1, 450)
    panels = panel_definitions(config)
    require(len(panels) == 64, "unexpected panel count")
    cases: list[dict[str, Any]] = []

    global_design = design["mandatoryGlobalLeftBoxes"]
    require(expect_int(global_design["boxCount"], "global boxCount", 1) == 27,
            "mandatory global-left count mismatch")
    d_centers = [parse_fraction(value, "global d center")
                 for value in global_design["dCenters"]]
    d_half = parse_fraction(global_design["dHalfWidthBeforeEndpointClipping"],
                            "global d half width")
    imaginary_half = parse_fraction(global_design["imaginaryHalfWidth"],
                                    "global imaginary half width")
    lambda_real = parse_fraction(global_design["lambdaReal"],
                                 "global lambda real")
    expected_outer = Fraction(config["global"]["boundary"]["outer"])
    expected_centers = [Fraction(k, 4) * expected_outer for k in range(-4, 5)]
    imaginary_centers = [parse_fraction(value, "global imaginary center")
                         for value in global_design["lambdaImaginaryCenters"]]
    require(d_centers == [Fraction(0), maximum_d / 2, maximum_d]
            and d_half == maximum_d / (2 ** 16)
            and imaginary_half == expected_outer / (2 ** 14)
            and lambda_real == Fraction(config["global"]["boundary"]["left"])
            and imaginary_centers == expected_centers,
            "mandatory global-left geometry differs from frozen design")
    for imaginary_index, imaginary_center in enumerate(imaginary_centers):
        for d_index, d_center in enumerate(d_centers):
            d_lower = max(Fraction(0), d_center - d_half)
            d_upper = min(maximum_d, d_center + d_half)
            cases.append({
                "id": f"GLEFT-y{imaginary_index:02d}-d{d_index}",
                "category": "mandatory-global-left",
                "family": "global",
                "steps": GLOBAL_STEPS,
                "parameterSpec": {
                    "kind": "global-left",
                    "d": fraction_interval_record(d_lower, d_upper),
                    "lambdaReal": fraction_text(lambda_real),
                    "lambdaImag": fraction_interval_record(
                        imaginary_center - imaginary_half,
                        imaginary_center + imaginary_half,
                    ),
                },
            })

    local_design = design["mandatoryLocalCircleBoxes"]
    require(expect_int(local_design["boxCount"], "local boxCount", 1) == 24,
            "mandatory local-circle count mismatch")
    local_d_centers = [parse_fraction(value, "local d center")
                       for value in local_design["dCenters"]]
    local_d_half = parse_fraction(
        local_design["dHalfWidthBeforeEndpointClipping"], "local d half width"
    )
    theta_half = parse_fraction(local_design["thetaHalfWidthInUnitsOfPi"],
                                "local theta half width")
    theta_centers = [parse_fraction(value, "local theta center")
                     for value in local_design["thetaCentersInUnitsOfPi"]]
    require(local_d_centers == d_centers and local_d_half == d_half
            and theta_half == Fraction(1, 2 ** 14)
            and theta_centers == [Fraction(k, 4) for k in range(8)],
            "mandatory local-circle geometry differs from frozen design")
    for theta_index, theta_center in enumerate(theta_centers):
        for d_index, d_center in enumerate(local_d_centers):
            d_lower = max(Fraction(0), d_center - local_d_half)
            d_upper = min(maximum_d, d_center + local_d_half)
            cases.append({
                "id": f"LCIRCLE-theta{theta_index:02d}-d{d_index}",
                "category": "mandatory-local-circle",
                "family": "local",
                "steps": LOCAL_STEPS,
                "parameterSpec": {
                    "kind": "theta-circle",
                    "d": fraction_interval_record(d_lower, d_upper),
                    "thetaPi": fraction_interval_record(
                        theta_center - theta_half, theta_center + theta_half
                    ),
                },
            })

    hash_design = design["hashSelectedPrimarySubdivisionBoxes"]
    require(expect_int(hash_design["count"], "hash box count", 1) == 32,
            "hash-selected count mismatch")
    seed = hash_design["selectionSeed"]
    require(type(seed) is str and len(seed) == 64,
            "invalid hash-selection seed")
    selectors = hash_design["selectors"]
    require(type(selectors) is list and len(selectors) == 32,
            "hash selector list mismatch")
    for ordinal, recorded in enumerate(selectors):
        block = hashlib.sha256(
            f"{seed}:natural-box:{ordinal}".encode("ascii")
        ).digest()
        expected = {
            "ordinal": ordinal,
            "panelSelector": int.from_bytes(block[0:4], "big"),
            "dCellSelector": int.from_bytes(block[4:8], "big"),
            "sCellSelector": int.from_bytes(block[8:12], "big"),
        }
        require(recorded == expected,
                f"hash selector {ordinal} does not match its digest")
        panel_index = expected["panelSelector"] % len(panels)
        panel = panels[panel_index]
        subdivision = config[panel["family"]]["subdivision"]
        d_depth = subdivision["dDepth"]
        s_depth = subdivision["sDepth"]
        d_index = expected["dCellSelector"] % (2 ** d_depth)
        s_index = expected["sCellSelector"] % (2 ** s_depth)
        d_lower = maximum_d * Fraction(d_index, 2 ** d_depth)
        d_upper = maximum_d * Fraction(d_index + 1, 2 ** d_depth)
        s_lower, s_upper = dyadic_bounds(s_index, s_depth)
        cases.append({
            "id": f"HASH-{ordinal:02d}-{panel['id']}-d{d_index}-s{s_index}",
            "category": "hash-selected-primary-cell",
            "family": panel["family"],
            "steps": GLOBAL_STEPS if panel["family"] == "global" else LOCAL_STEPS,
            "parameterSpec": {
                "kind": "panel-cell",
                "panel": panel,
                "panelIndex": panel_index,
                "dDepth": d_depth,
                "dIndex": d_index,
                "sDepth": s_depth,
                "sIndex": s_index,
                "d": fraction_interval_record(d_lower, d_upper),
                "s": fraction_interval_record(s_lower, s_upper),
                "selectors": expected,
            },
        })

    require(len(cases) == EXPECTED_BOX_COUNT,
            "constructed natural-box list does not contain 83 cases")
    require(len({case["id"] for case in cases}) == len(cases),
            "natural-box case identifiers are not unique")
    return cases


def interval_from_record(value: dict[str, str], label: str) -> arb:
    return arb_interval(
        parse_fraction(value["lower"], f"{label}.lower"),
        parse_fraction(value["upper"], f"{label}.upper"),
    )


def parameters_for_case(case: dict[str, Any]) -> tuple[arb, acb]:
    spec = case["parameterSpec"]
    d_lower = parse_fraction(spec["d"]["lower"], f"{case['id']}.d.lower")
    d_upper = parse_fraction(spec["d"]["upper"], f"{case['id']}.d.upper")
    require(Fraction(0) <= d_lower <= d_upper <= Fraction(1, 450),
            "exact rational d endpoints lie outside [0,1/450]")
    d_box = arb_interval(d_lower, d_upper)
    if spec["kind"] == "global-left":
        spectral = acb(
            arb_fraction(Fraction(spec["lambdaReal"])),
            interval_from_record(spec["lambdaImag"], f"{case['id']}.lambdaImag"),
        )
    elif spec["kind"] == "theta-circle":
        theta_pi = interval_from_record(spec["thetaPi"], f"{case['id']}.thetaPi")
        theta = arb.pi() * theta_pi
        spectral = acb(
            arb(17) / 100 + arb(3) / 1000 * theta.cos(),
            arb(3) / 1000 * theta.sin(),
        )
    elif spec["kind"] == "panel-cell":
        panel = spec["panel"]
        s_box = interval_from_record(spec["s"], f"{case['id']}.s")
        if panel["kind"] == "line":
            spectral = acb(
                arb_fraction(Fraction(panel["centerReal"]))
                + arb_fraction(Fraction(panel["halfReal"])) * s_box,
                arb_fraction(Fraction(panel["centerImag"]))
                + arb_fraction(Fraction(panel["halfImag"])) * s_box,
            )
        elif panel["kind"] == "circle":
            theta = arb.pi() * (
                arb_fraction(Fraction(panel["thetaCenterPi"]))
                + arb_fraction(Fraction(panel["thetaHalfPi"])) * s_box
            )
            spectral = acb(
                arb(17) / 100 + arb(3) / 1000 * theta.cos(),
                arb(3) / 1000 * theta.sin(),
            )
        else:
            raise ValidationFailure("unknown panel kind")
    else:
        raise ValidationFailure("unknown natural-box parameter kind")
    require(d_box.is_finite() and spectral.is_finite(),
            "constructed parameter box is not finite")
    # Arb's radius is deliberately rounded upward, so the machine enclosure of
    # an endpoint-touching interval can extend microscopically beyond the exact
    # rational endpoint.  Domain membership is therefore checked on the frozen
    # rational endpoints above; the wider Arb ball remains the proof input.
    require(spectral.real.lower() > 0,
            "spectral box reaches Re(lambda) <= 0")
    return d_box, spectral


def worker_initialize(settings: dict[str, Any]) -> None:
    global WORKER_SETTINGS
    WORKER_SETTINGS = dict(settings)
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    ctx.dps = settings["dps"]
    ctx.threads = 1


def worker_case(case: dict[str, Any]) -> dict[str, Any]:
    started = time.perf_counter()
    audit = OdeAudit(case["steps"])
    result: dict[str, Any] = {
        "id": case["id"],
        "category": case["category"],
        "family": case["family"],
        "parameterSpec": case["parameterSpec"],
        "steps": case["steps"],
        "order": WORKER_SETTINGS["order"],
        "precisionDecimalDigits": WORKER_SETTINGS["dps"],
        "workerPid": os.getpid(),
    }
    try:
        d_box, spectral_box = parameters_for_case(case)
        result["parameterBoxes"] = {
            "d": arb_text(d_box),
            "lambda": acb_record(spectral_box),
        }
        evans = interval_evans(
            d_box, spectral_box, case["steps"],
            WORKER_SETTINGS["order"], audit,
        )
        evans_lower = evans.abs_lower()
        result["evansBox"] = acb_record(evans)
        result["evansAbsoluteLower"] = arb_text(evans_lower)
        require(evans_lower.lower() > 0,
                "final Evans enclosure contains zero")
        require(audit.minimum_denominator is not None
                and audit.minimum_denominator.lower() > 0,
                "Rayleigh denominator audit is not positive")
        require(audit.minimum_tube_slack is not None
                and audit.minimum_tube_slack.lower() > 0,
                "Picard tube slack audit is not positive")
        result.update({
            "status": "passed",
            "minimumRayleighDenominatorLower": arb_text(
                audit.minimum_denominator
            ),
            "minimumPicardTubeSlack": arb_text(audit.minimum_tube_slack),
            "maximumPicardTubeAttempt": audit.maximum_tube_attempt,
        })
    except Exception as error:
        result.update({
            "status": "failed",
            "errorType": type(error).__name__,
            "error": str(error),
            "minimumRayleighDenominatorLower": (
                arb_text(audit.minimum_denominator)
                if audit.minimum_denominator is not None else None
            ),
            "minimumPicardTubeSlack": (
                arb_text(audit.minimum_tube_slack)
                if audit.minimum_tube_slack is not None else None
            ),
            "maximumPicardTubeAttempt": audit.maximum_tube_attempt,
        })
    result["elapsedSeconds"] = time.perf_counter() - started
    return result


def resource_snapshot(started: float, event: str) -> dict[str, Any]:
    own = resource.getrusage(resource.RUSAGE_SELF)
    children = resource.getrusage(resource.RUSAGE_CHILDREN)
    return {
        "time": utc_now(),
        "event": event,
        "elapsedSeconds": time.perf_counter() - started,
        "loadAverage": list(os.getloadavg()),
        "selfUserSeconds": own.ru_utime,
        "selfSystemSeconds": own.ru_stime,
        "childrenUserSeconds": children.ru_utime,
        "childrenSystemSeconds": children.ru_stime,
        "selfMaxRssRaw": own.ru_maxrss,
        "childrenMaxRssRaw": children.ru_maxrss,
        "diskFreeBytes": shutil.disk_usage(HERE).free,
    }


def resource_monitor(
    stop: threading.Event,
    path: Path,
    started: float,
) -> None:
    while not stop.wait(RESOURCE_INTERVAL_SECONDS):
        append_ndjson(path, resource_snapshot(started, "resource-sample"))


def parse_result_ball(value: str | None) -> arb | None:
    if value is None:
        return None
    parsed = arb(value)
    require(parsed.is_finite(), "nonfinite result ball")
    return parsed


def select_minimum(results: Sequence[dict[str, Any]], key: str) -> dict[str, Any] | None:
    available = [
        (parse_result_ball(result.get(key)), result)
        for result in results if result.get(key) is not None
    ]
    available = [(value, result) for value, result in available if value is not None]
    if not available:
        return None
    value, result = min(available, key=lambda item: item[0].lower())
    return {"caseId": result["id"], "value": arb_text(value)}


def run(
    config_path: Path,
    design_path: Path,
    output_path: Path,
    progress_path: Path,
    resource_path: Path,
) -> dict[str, Any]:
    require(config_path.is_file(), "config.json is missing")
    require(design_path.is_file(), "independent_validation.json is missing")
    require(getattr(flint, "__version__", None) == EXPECTED_PYTHON_FLINT,
            "runtime python-flint version differs from 0.6.0")
    # The parent process re-parses worker ball strings when selecting global
    # minima, so it must use the same precision as the workers.
    ctx.dps = PRECISION_DPS
    ctx.threads = 1
    config_bytes = config_path.read_bytes()
    design_bytes = design_path.read_bytes()
    script_path = Path(__file__).resolve()
    script_bytes = script_path.read_bytes()
    config = json.loads(config_bytes.decode("utf-8"))
    frozen_audit = json.loads(design_bytes.decode("utf-8"))
    require(frozen_audit.get("status") == "passed",
            "shared-grid independent audit is not passed")
    design = frozen_audit["naturalBoxSpotCheck"]
    cases = build_cases(config, design)
    run_id = sha256_bytes(
        (sha256_bytes(script_bytes) + sha256_bytes(design_bytes) + utc_now()).encode()
    )[:20]
    started = time.perf_counter()
    initialize_ndjson(progress_path, {
        "time": utc_now(),
        "event": "natural-box-run-started",
        "runId": run_id,
        "boxCount": len(cases),
        "workers": WORKERS,
        "order": ORDER,
        "precisionDecimalDigits": PRECISION_DPS,
        "globalSteps": GLOBAL_STEPS,
        "localSteps": LOCAL_STEPS,
    })
    initialize_ndjson(resource_path, resource_snapshot(started, "resource-start"))
    for ordinal, case in enumerate(cases):
        append_ndjson(progress_path, {
            "time": utc_now(),
            "event": "natural-box-planned",
            "runId": run_id,
            "ordinal": ordinal,
            "caseId": case["id"],
            "category": case["category"],
            "family": case["family"],
            "steps": case["steps"],
        })

    stop = threading.Event()
    monitor = threading.Thread(
        target=resource_monitor,
        args=(stop, resource_path, started),
        daemon=True,
    )
    monitor.start()
    results: list[dict[str, Any]] = []
    settings = {"dps": PRECISION_DPS, "order": ORDER}
    context = mp.get_context("spawn")
    try:
        with context.Pool(
            processes=WORKERS,
            initializer=worker_initialize,
            initargs=(settings,),
            maxtasksperchild=8,
        ) as pool:
            for result in pool.imap_unordered(worker_case, cases, chunksize=1):
                results.append(result)
                append_ndjson(progress_path, {
                    "time": utc_now(),
                    "event": "natural-box-complete",
                    "runId": run_id,
                    "completed": len(results),
                    "total": len(cases),
                    "caseId": result["id"],
                    "status": result["status"],
                    "elapsedSeconds": result["elapsedSeconds"],
                    "evansAbsoluteLower": result.get("evansAbsoluteLower"),
                    "minimumRayleighDenominatorLower": result.get(
                        "minimumRayleighDenominatorLower"
                    ),
                    "minimumPicardTubeSlack": result.get(
                        "minimumPicardTubeSlack"
                    ),
                    "error": result.get("error"),
                })
    finally:
        stop.set()
        monitor.join(timeout=10)
        append_ndjson(resource_path, resource_snapshot(started, "resource-stop"))

    result_order = {case["id"]: index for index, case in enumerate(cases)}
    results.sort(key=lambda result: result_order[result["id"]])
    require(len(results) == len(cases), "worker result count is incomplete")
    passed = [result for result in results if result["status"] == "passed"]
    failed = [result for result in results if result["status"] != "passed"]

    require(config_path.read_bytes() == config_bytes,
            "configuration changed during run")
    require(design_path.read_bytes() == design_bytes,
            "frozen natural-box design changed during run")
    require(script_path.read_bytes() == script_bytes,
            "natural-box validator source changed during run")
    decisions = {
        "all83BoxesPassed": len(passed) == EXPECTED_BOX_COUNT and not failed,
        "expectedBoxCount": EXPECTED_BOX_COUNT,
        "passedBoxCount": len(passed),
        "failedBoxCount": len(failed),
        "minimumEvansAbsoluteLower": select_minimum(
            passed, "evansAbsoluteLower"
        ),
        "minimumRayleighDenominatorLower": select_minimum(
            results, "minimumRayleighDenominatorLower"
        ),
        "minimumPicardTubeSlack": select_minimum(
            results, "minimumPicardTubeSlack"
        ),
    }
    output = {
        "schemaVersion": SCHEMA_VERSION,
        "status": "passed" if decisions["all83BoxesPassed"] else "failed",
        "completedAt": utc_now(),
        "runId": run_id,
        "classification": "independent-raw-ode-natural-box-corroboration",
        "provenance": {
            "scriptSha256": sha256_bytes(script_bytes),
            "configSha256": sha256_bytes(config_bytes),
            "frozenIndependentValidationSha256": sha256_bytes(design_bytes),
            "selectionSeed": design["hashSelectedPrimarySubdivisionBoxes"][
                "selectionSeed"
            ],
            "pythonFlintVersion": flint.__version__,
            "python": platform.python_version(),
            "pythonImplementation": platform.python_implementation(),
        },
        "method": {
            "arithmetic": "python-flint Arb/Acb outward-rounded ball arithmetic",
            "precisionDecimalDigits": PRECISION_DPS,
            "TaylorOrder": ORDER,
            "globalSteps": GLOBAL_STEPS,
            "localSteps": LOCAL_STEPS,
            "workers": WORKERS,
            "flintThreadsPerWorker": 1,
            "clockReset": (
                "rigorous exact trigonometric clock reset after every validated step"
            ),
            "boxPolicy": "frozen widths; no shrinking, subdivision, or relaxed decision",
        },
        "decisions": decisions,
        "cases": results,
        "interpretation": {
            "whatPassedMeans": (
                "each listed parameter box has a direct interval-ODE Evans enclosure "
                "strictly separated from zero, with positive Rayleigh-denominator and "
                "Picard-tube margins"
            ),
            "limitation": (
                "83 selected boxes are only independent raw-ODE corroboration; they do "
                "not cover either contour and cannot replace the uniform Clenshaw "
                "certificate"
            ),
            "failurePolicy": (
                "a wrapping or tube failure at the frozen width is recorded as failed "
                "and is not repaired by narrowing the box"
            ),
        },
        "artifacts": {
            "progress": str(progress_path.relative_to(ROOT)),
            "resources": str(resource_path.relative_to(ROOT)),
        },
        "elapsedSeconds": time.perf_counter() - started,
    }
    atomic_json(output_path, output)
    append_ndjson(progress_path, {
        "time": utc_now(),
        "event": "natural-box-run-complete",
        "runId": run_id,
        "status": output["status"],
        "elapsedSeconds": output["elapsedSeconds"],
        "decisions": decisions,
        "output": str(output_path.relative_to(ROOT)),
    })
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=HERE / "config.json")
    parser.add_argument("--design", type=Path,
                        default=HERE / "independent_validation.json")
    parser.add_argument("--output", type=Path,
                        default=HERE / "natural_box_validation.json")
    parser.add_argument("--progress", type=Path,
                        default=HERE / "natural_box_progress.ndjson")
    parser.add_argument("--resources", type=Path,
                        default=HERE / "natural_box_resources.ndjson")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        result = run(
            args.config.resolve(), args.design.resolve(), args.output.resolve(),
            args.progress.resolve(), args.resources.resolve(),
        )
    except Exception as error:
        failure = {
            "schemaVersion": SCHEMA_VERSION,
            "status": "failed",
            "completedAt": utc_now(),
            "errorType": type(error).__name__,
            "error": str(error),
            "interpretation": (
                "setup or orchestration failed before a complete 83-box decision"
            ),
        }
        atomic_json(args.output.resolve(), failure)
        print(canonical_json(failure), end="")
        raise SystemExit(1)
    summary = {
        "status": result["status"],
        "output": str(args.output.resolve()),
        "elapsedSeconds": result["elapsedSeconds"],
        "decisions": result["decisions"],
    }
    print(canonical_json(summary), end="")
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
