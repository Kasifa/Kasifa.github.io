#!/usr/bin/env python3
"""Independent fixed-step real-lattice audit for R0.72A.

This program imports neither ``r072a_exact_audit`` nor its output.  It uses
the invariant real phase representation and a fixed-step classical RK4
scheme, whereas the producer uses complex DOP853 and predetermined Bessel
brackets.  Roots are discovered from sign changes and refined by cubic
Hermite interpolation.

The calculation is finite-dimensional corroboration, not interval arithmetic
and not a proof of the bilateral infinite-lattice theorem.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import platform
import sys
import time

import numpy as np
from scipy.optimize import brentq
from scipy.special import j0, jn_zeros


R_VALUES = (8, 16, 32, 64)
STEP = 0.004
RIGHT_MARGIN = 0.30


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit(message: str) -> None:
    print(f"[{utc_now()}] {message}", file=sys.stderr, flush=True)


def check(name: str, passed: bool, value: object, requirement: str) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def rhs(tau: float, state: np.ndarray, indices: np.ndarray, delta: float) -> np.ndarray:
    """Real invariant system for F_r=(-i)^r u_r."""

    derivative = -((indices**2 + 1.0) / delta) * state
    amplitude = math.exp(-tau / delta)
    derivative[1:] += amplitude * state[:-1]
    derivative[:-1] -= amplitude * state[1:]
    return derivative


def rk4_step(
    tau: float,
    state: np.ndarray,
    step: float,
    indices: np.ndarray,
    delta: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    k1 = rhs(tau, state, indices, delta)
    k2 = rhs(tau + step / 2.0, state + step * k1 / 2.0, indices, delta)
    k3 = rhs(tau + step / 2.0, state + step * k2 / 2.0, indices, delta)
    k4 = rhs(tau + step, state + step * k3, indices, delta)
    next_state = state + step * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
    next_derivative = rhs(tau + step, next_state, indices, delta)
    return next_state, k1, next_derivative


def hermite_state(
    fraction: float,
    left: np.ndarray,
    right: np.ndarray,
    left_derivative: np.ndarray,
    right_derivative: np.ndarray,
    step: float,
) -> np.ndarray:
    s = fraction
    h00 = 2.0 * s**3 - 3.0 * s**2 + 1.0
    h10 = s**3 - 2.0 * s**2 + s
    h01 = -2.0 * s**3 + 3.0 * s**2
    h11 = s**3 - s**2
    return (
        h00 * left
        + h10 * step * left_derivative
        + h01 * right
        + h11 * step * right_derivative
    )


def solve_one(r_value: int) -> dict[str, object]:
    delta = float(r_value**4)
    radius = 5 * r_value + 30
    indices = np.arange(-radius, radius + 1, dtype=float)
    target = radius
    state = np.zeros(indices.size, dtype=float)
    state[target - 1] = 1.0

    limiting_zeros = jn_zeros(1, r_value)
    final_tau = float(limiting_zeros[-1] / 2.0 + RIGHT_MARGIN)
    tau = 0.0
    previous_target = float(state[target])
    roots: list[dict[str, float]] = []
    maximum_norm = float(np.linalg.norm(state))
    minimum_norm = maximum_norm
    started = time.perf_counter()
    steps = 0

    while tau < final_tau - 1.0e-15:
        step = min(STEP, final_tau - tau)
        next_state, left_derivative, right_derivative = rk4_step(
            tau, state, step, indices, delta
        )
        next_target = float(next_state[target])

        # Exclude the launch zero. Every positive simple crossing changes sign.
        if tau > 0.0 and previous_target * next_target < 0.0:
            def interpolated_target(fraction: float) -> float:
                return float(
                    hermite_state(
                        fraction,
                        state,
                        next_state,
                        left_derivative,
                        right_derivative,
                        step,
                    )[target]
                )

            fraction = float(
                brentq(interpolated_target, 0.0, 1.0, xtol=2.0e-14, rtol=2.0e-14)
            )
            root_tau = tau + fraction * step
            root_state = hermite_state(
                fraction,
                state,
                next_state,
                left_derivative,
                right_derivative,
                step,
            )
            amplitude = math.exp(-root_tau / delta)
            h_value = amplitude * (
                root_state[target - 1] - root_state[target + 1]
            )
            roots.append(
                {
                    "tau": root_tau,
                    "h": float(h_value),
                    "hSquare": float(h_value**2),
                    "interpolatedTargetResidual": abs(interpolated_target(fraction)),
                }
            )

        norm = float(np.linalg.norm(next_state))
        maximum_norm = max(maximum_norm, norm)
        minimum_norm = min(minimum_norm, norm)
        tau += step
        state = next_state
        previous_target = next_target
        steps += 1

    elapsed = time.perf_counter() - started
    if len(roots) != r_value:
        raise AssertionError(
            f"independent sign scan found {len(roots)} roots for R={r_value}"
        )

    exact_mass = float(sum(row["hSquare"] for row in roots))
    bessel_mass = float(4.0 * np.sum(j0(limiting_zeros) ** 2))
    limiting_roots = limiting_zeros / 2.0
    root_shifts = [
        float(row["tau"] - limiting)
        for row, limiting in zip(roots, limiting_roots, strict=True)
    ]
    layer_length = final_tau / delta

    # Independent quadrature of ell_2: ||V(x)||=2e^{-x}, Omega=2.
    x_grid = np.linspace(0.0, layer_length, 2001)
    norm_square = 4.0 * np.exp(-2.0 * x_grid)
    ell_two_trapezoid = float(np.trapezoid(norm_square, x_grid) / 4.0)
    ell_two_exact = 0.5 * (1.0 - math.exp(-2.0 * layer_length))

    return {
        "R": r_value,
        "delta": delta,
        "eta": 2.0 * delta,
        "radius": radius,
        "dimension": int(indices.size),
        "step": STEP,
        "steps": steps,
        "finalTau": final_tau,
        "layerLength": layer_length,
        "exactSelectedMass": exact_mass,
        "besselMass": bessel_mass,
        "massDifference": exact_mass - bessel_mass,
        "relativeMassDifference": (exact_mass - bessel_mass) / bessel_mass,
        "maximumRootShift": max(abs(value) for value in root_shifts),
        "R2TimesMaximumRootShift": r_value**2 * max(abs(value) for value in root_shifts),
        "maximumNorm": maximum_norm,
        "minimumNorm": minimum_norm,
        "ell2Trapezoid": ell_two_trapezoid,
        "ell2ClosedForm": ell_two_exact,
        "ell2Defect": abs(ell_two_trapezoid - ell_two_exact),
        "elapsedSeconds": elapsed,
        "roots": roots,
    }


def main() -> None:
    args = parse_args()
    emit("R0.72A independent RK4 audit started")
    started = time.perf_counter()
    rows: list[dict[str, object]] = []
    for r_value in R_VALUES:
        emit(f"independent R={r_value} sign-scan started")
        row = solve_one(r_value)
        rows.append(row)
        emit(
            "independent R={} complete: roots={}, mass={:.10f}".format(
                r_value, len(row["roots"]), float(row["exactSelectedMass"])
            )
        )

    log_coefficient = 8.0 / math.pi**2
    log_rows = [
        {
            "R": row["R"],
            "massMinusLeadingLog": float(row["exactSelectedMass"])
            - log_coefficient * math.log(float(row["R"])),
        }
        for row in rows
    ]

    # Re-derive the alpha boundary without sharing producer code.
    boundary_rows = []
    for beta in (0.0, 0.75, 1.5, 2.25):
        constraints = (1.5, (2.0 + beta) * 3.0 / 7.0)
        boundary_rows.append(
            {"beta": beta, "alphaBoundary": min(constraints), "constraints": constraints}
        )

    checks = [
        check(
            "discovered_root_count",
            all(len(row["roots"]) == row["R"] for row in rows),
            [len(row["roots"]) for row in rows],
            "unseeded sign scan finds exactly R positive crossings",
        ),
        check(
            "contractive_real_evolution",
            max(float(row["maximumNorm"]) for row in rows) <= 1.0 + 2.0e-10,
            max(float(row["maximumNorm"]) for row in rows),
            "real invariant RK4 evolution stays contractive to numerical tolerance",
        ),
        check(
            "local_exposure_quadrature",
            max(float(row["ell2Defect"]) for row in rows) < 2.0e-14,
            max(float(row["ell2Defect"]) for row in rows),
            "trapezoid and closed-form local exposure agree below 2e-14",
        ),
        check(
            "R64_bessel_mass",
            abs(float(rows[-1]["relativeMassDifference"])) < 3.0e-5,
            rows[-1]["relativeMassDifference"],
            "independent R=64 mass is within 3e-5 relative of frozen Bessel mass",
        ),
        check(
            "root_shift_decay",
            all(
                float(later["maximumRootShift"]) < float(earlier["maximumRootShift"])
                for earlier, later in zip(rows[:-1], rows[1:], strict=True)
            ),
            [row["maximumRootShift"] for row in rows],
            "maximum root shift decreases along dyadic R",
        ),
        check(
            "shrinking_physical_layer",
            all(
                float(later["layerLength"]) < float(earlier["layerLength"])
                for earlier, later in zip(rows[:-1], rows[1:], strict=True)
            ),
            [row["layerLength"] for row in rows],
            "physical layer decreases along dyadic R",
        ),
        check(
            "phase_boundary_endpoints",
            abs(boundary_rows[0]["alphaBoundary"] - 6.0 / 7.0) < 1.0e-15
            and abs(boundary_rows[2]["alphaBoundary"] - 1.5) < 1.0e-15,
            boundary_rows,
            "independent exponent algebra recovers 6/7 and 3/2 endpoints",
        ),
    ]

    payload = {
        "schemaVersion": "r072a-independent-audit-v1",
        "generatedAt": utc_now(),
        "algorithm": {
            "state": "real invariant phase F_r=(-i)^r u_r",
            "integrator": "fixed-step classical RK4",
            "rootDiscovery": "unseeded sign changes plus cubic Hermite interpolation",
            "step": STEP,
            "importsProducer": False,
            "readsProducerOutput": False,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
        },
        "phaseBoundary": boundary_rows,
        "logCoefficient": log_coefficient,
        "logResiduals": log_rows,
        "finiteLattice": rows,
        "checks": checks,
        "allPassed": all(row["passed"] for row in checks),
        "elapsedSeconds": time.perf_counter() - started,
        "scope": {
            "intervalArithmetic": False,
            "provesInfiniteLattice": False,
            "provesNSERegularity": False,
            "note": "Independent finite real-lattice corroboration only.",
        },
    }
    if not payload["allPassed"]:
        failed = [row["name"] for row in checks if not row["passed"]]
        raise AssertionError(f"independent checks failed: {failed}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    emit(f"R0.72A independent audit passed in {payload['elapsedSeconds']:.2f}s")


if __name__ == "__main__":
    main()
