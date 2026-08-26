#!/usr/bin/env python3
"""Producer audit for R0.72A local exposure and the exact Bessel family.

The continuum proof is in ``research/r072a_report-source.md``.  This program
recomputes the phase boundary, Bessel constants, and finite bilateral-lattice
solutions from raw parameters.  The time integrations are corroborative: a
finite truncation does not prove the infinite-lattice theorem.
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

import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import j0, jn_zeros


MP_DIGITS = 80
mp.mp.dps = MP_DIGITS

R_VALUES = (4, 8, 16, 32, 64)
ROOT_RADIUS = 0.35
RTOL = 3.0e-11
ATOL = 3.0e-13
MAX_STEP = 0.03


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def check(name: str, passed: bool, value: object, requirement: str) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def emit(message: str) -> None:
    print(f"[{utc_now()}] {message}", file=sys.stderr, flush=True)


def phase_rows() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for beta in (0.0, 0.5, 1.0, 1.5, 2.0, 3.0):
        local_boundary = min(1.5, (6.0 + 3.0 * beta) / 7.0)
        rows.append(
            {
                "beta": beta,
                "fixed_first_root_boundary": 1.5,
                "local_exposure_boundary": (6.0 + 3.0 * beta) / 7.0,
                "certified_alpha_boundary": local_boundary,
            }
        )
    return rows


def bessel_asymptotic_rows() -> tuple[list[dict[str, float]], float]:
    rows: list[dict[str, float]] = []
    target = 8.0 / math.pi**2
    fit_r = np.array([128, 256, 512, 1024, 2048], dtype=float)
    fit_mass: list[float] = []
    for r_value in fit_r.astype(int):
        zeros = jn_zeros(1, int(r_value))
        mass = float(4.0 * np.sum(j0(zeros) ** 2))
        fit_mass.append(mass)
        rows.append(
            {
                "R": int(r_value),
                "besselMass": mass,
                "massMinusLeadingLog": mass - target * math.log(float(r_value)),
                "massOverLogR": mass / math.log(float(r_value)),
            }
        )
    # The dyadic increment cancels the nonzero O(1) term in the logarithmic
    # asymptotic more cleanly than a short uncorrected global regression.
    tail_slope = (fit_mass[-1] - fit_mass[-2]) / math.log(2.0)
    return rows, float(tail_slope)


def moment_identity_rows() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for tau in (0.0, 0.25, 1.0, 3.0, 8.0):
        cutoff = max(80, int(8.0 * tau + 80.0))
        indices = np.arange(-cutoff, cutoff + 1, dtype=int)
        # W_r = (-i)^r J_{r+1}(2 tau).
        coefficients = np.array(
            [float(mp.besselj(int(r) + 1, 2.0 * tau)) for r in indices],
            dtype=float,
        )
        numerical = float(
            np.sum(((indices.astype(float) ** 2 + 1.0) ** 2) * coefficients**2)
        )
        exact = 6.0 * tau**4 + 18.0 * tau**2 + 4.0
        rows.append(
            {
                "tau": tau,
                "truncationRadius": cutoff,
                "numericalMoment": numerical,
                "closedForm": exact,
                "absoluteDefect": abs(numerical - exact),
            }
        )
    return rows


def finite_rhs(radius: int, delta: float):
    indices = np.arange(-radius, radius + 1, dtype=float)
    diagonal = -(indices**2 + 1.0) / delta

    def rhs(tau: float, state: np.ndarray) -> np.ndarray:
        neighbors = np.zeros_like(state)
        neighbors[1:] += state[:-1]
        neighbors[:-1] += state[1:]
        return diagonal * state - 1j * math.exp(-tau / delta) * neighbors

    return rhs


def solve_family(r_value: int, radius: int | None = None) -> dict[str, object]:
    delta = float(r_value**4)
    if radius is None:
        radius = 4 * r_value + 24
    dimension = 2 * radius + 1
    target_index = radius
    initial = np.zeros(dimension, dtype=np.complex128)
    initial[target_index - 1] = 1j

    zeros = jn_zeros(1, r_value)
    limiting_roots = zeros / 2.0
    final_tau = float(limiting_roots[-1] + ROOT_RADIUS)
    rhs = finite_rhs(radius, delta)

    started = time.perf_counter()
    solution = solve_ivp(
        rhs,
        (0.0, final_tau),
        initial,
        method="DOP853",
        dense_output=True,
        rtol=RTOL,
        atol=ATOL,
        max_step=MAX_STEP,
    )
    elapsed = time.perf_counter() - started
    if not solution.success or solution.sol is None:
        raise RuntimeError(f"DOP853 failed for R={r_value}: {solution.message}")

    root_rows: list[dict[str, float]] = []
    exact_mass = 0.0
    maximum_shift = 0.0
    maximum_imaginary_target = 0.0
    for limiting_root in limiting_roots:
        left = max(0.0, float(limiting_root - ROOT_RADIUS))
        right = float(limiting_root + ROOT_RADIUS)

        def target_real(tau: float) -> float:
            return float(solution.sol(tau)[target_index].real)

        left_value = target_real(left)
        right_value = target_real(right)
        if left_value * right_value >= 0.0:
            raise AssertionError(
                f"root bracket failed for R={r_value}, tau={limiting_root}"
            )
        exact_root = float(brentq(target_real, left, right, xtol=2.0e-13, rtol=2.0e-14))
        state = solution.sol(exact_root)
        target = state[target_index]
        maximum_imaginary_target = max(maximum_imaginary_target, abs(float(target.imag)))
        h_value = -1j * math.exp(-exact_root / delta) * (
            state[target_index - 1] + state[target_index + 1]
        )
        slope_square = float(abs(h_value) ** 2)
        exact_mass += slope_square
        shift = exact_root - float(limiting_root)
        maximum_shift = max(maximum_shift, abs(shift))
        root_rows.append(
            {
                "limitingRootTau": float(limiting_root),
                "exactRootTau": exact_root,
                "rootShift": shift,
                "hReal": float(h_value.real),
                "hImag": float(h_value.imag),
                "hSquare": slope_square,
                "targetResidual": float(abs(target)),
            }
        )

    bessel_mass = float(4.0 * np.sum(j0(zeros) ** 2))
    layer_length = final_tau / delta
    omega = 2.0
    eta = omega * delta
    ell_two = 0.5 * (1.0 - math.exp(-2.0 * layer_length))
    local_exposure = eta * ell_two
    upper_dimensionless = 4.0 + local_exposure
    return {
        "R": r_value,
        "delta": delta,
        "eta": eta,
        "radius": radius,
        "dimension": dimension,
        "finalTau": final_tau,
        "layerLength": layer_length,
        "R3TimesLayerLength": layer_length * r_value**3,
        "ell2": ell_two,
        "etaEll2": local_exposure,
        "upperDimensionlessFactor": upper_dimensionless,
        "exactSelectedMass": exact_mass,
        "besselMass": bessel_mass,
        "massDifference": exact_mass - bessel_mass,
        "relativeMassDifference": (exact_mass - bessel_mass) / bessel_mass,
        "maximumRootShift": maximum_shift,
        "R2TimesMaximumRootShift": maximum_shift * r_value**2,
        "maximumImaginaryTargetAtRoot": maximum_imaginary_target,
        "solverSteps": int(solution.t.size),
        "elapsedSeconds": elapsed,
        "roots": root_rows,
    }


def main() -> None:
    args = parse_args()
    emit("R0.72A producer audit started")
    started = time.perf_counter()

    phases = phase_rows()
    emit("phase boundary rows complete")
    bessel_rows, fitted_slope = bessel_asymptotic_rows()
    emit("Bessel asymptotic ledger complete")
    moments = moment_identity_rows()
    emit("Bessel moment identities complete")

    simulation_rows: list[dict[str, object]] = []
    for r_value in R_VALUES:
        emit(f"finite bilateral solve R={r_value} started")
        row = solve_family(r_value)
        simulation_rows.append(row)
        emit(
            "finite bilateral solve R={} complete: mass={:.10f}, shift={:.3e}".format(
                r_value,
                float(row["exactSelectedMass"]),
                float(row["maximumRootShift"]),
            )
        )

    emit("truncation-doubling audit R=32 started")
    doubled = solve_family(32, radius=2 * (4 * 32 + 24))
    primary_32 = next(row for row in simulation_rows if row["R"] == 32)
    truncation_mass_defect = abs(
        float(primary_32["exactSelectedMass"]) - float(doubled["exactSelectedMass"])
    )
    truncation_root_defect = max(
        abs(float(a["exactRootTau"]) - float(b["exactRootTau"]))
        for a, b in zip(primary_32["roots"], doubled["roots"], strict=True)
    )
    emit("truncation-doubling audit complete")

    target_coefficient = 8.0 / math.pi**2
    checks = [
        check(
            "fixed_length_boundary",
            abs(phases[0]["certified_alpha_boundary"] - 6.0 / 7.0) < 1.0e-15,
            phases[0]["certified_alpha_boundary"],
            "beta=0 gives alpha=6/7",
        ),
        check(
            "fast_shrinking_boundary",
            abs(phases[3]["certified_alpha_boundary"] - 1.5) < 1.0e-15,
            phases[3]["certified_alpha_boundary"],
            "beta=3/2 reaches alpha=3/2",
        ),
        check(
            "bessel_log_coefficient",
            abs(fitted_slope - target_coefficient) < 5.0e-4,
            {"fitted": fitted_slope, "target": target_coefficient},
            "last dyadic increment differs from 8/pi^2 by less than 5e-4",
        ),
        check(
            "bessel_moment_identity",
            max(row["absoluteDefect"] for row in moments) < 2.0e-11,
            max(row["absoluteDefect"] for row in moments),
            "all sampled fourth-moment defects below 2e-11",
        ),
        check(
            "selected_root_brackets",
            all(len(row["roots"]) == row["R"] for row in simulation_rows),
            [len(row["roots"]) for row in simulation_rows],
            "one independently bracketed positive root per Bessel neighborhood",
        ),
        check(
            "target_reality",
            max(float(row["maximumImaginaryTargetAtRoot"]) for row in simulation_rows)
            < 2.0e-11,
            max(float(row["maximumImaginaryTargetAtRoot"]) for row in simulation_rows),
            "imaginary target residual at roots below 2e-11",
        ),
        check(
            "R64_mass_match",
            abs(float(simulation_rows[-1]["relativeMassDifference"])) < 2.0e-5,
            simulation_rows[-1]["relativeMassDifference"],
            "R=64 selected mass matches frozen Bessel mass within 2e-5 relative",
        ),
        check(
            "shrinking_layer",
            all(
                float(later["layerLength"]) < float(earlier["layerLength"])
                for earlier, later in zip(
                    simulation_rows[:-1], simulation_rows[1:], strict=True
                )
            ),
            [row["layerLength"] for row in simulation_rows],
            "layer length decreases over the dyadic R sequence",
        ),
        check(
            "truncation_mass_stability",
            truncation_mass_defect < 2.0e-10,
            truncation_mass_defect,
            "doubling the R=32 radius changes selected mass by less than 2e-10",
        ),
        check(
            "truncation_root_stability",
            truncation_root_defect < 2.0e-10,
            truncation_root_defect,
            "doubling the R=32 radius changes every root by less than 2e-10",
        ),
    ]

    payload = {
        "schemaVersion": "r072a-exact-audit-v1",
        "generatedAt": utc_now(),
        "precision": {
            "mpmathDigits": MP_DIGITS,
            "solver": "SciPy DOP853",
            "rtol": RTOL,
            "atol": ATOL,
            "maxStep": MAX_STEP,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
        },
        "parameters": {
            "nu": 1,
            "d": 1,
            "q": 1,
            "Ky": 0,
            "Kz": 1,
            "carrier": 1,
            "coefficient": 1,
            "launch": "i e_{-1}",
            "deltaRule": "R^4",
            "radiusRule": "4R+24",
        },
        "phaseBoundary": phases,
        "besselAsymptotic": {
            "targetCoefficient": target_coefficient,
            "fittedCoefficient": fitted_slope,
            "rows": bessel_rows,
        },
        "momentIdentity": moments,
        "finiteLattice": simulation_rows,
        "truncationDoubling": {
            "R": 32,
            "primaryRadius": primary_32["radius"],
            "doubledRadius": doubled["radius"],
            "massDefect": truncation_mass_defect,
            "maximumRootDefect": truncation_root_defect,
        },
        "checks": checks,
        "allPassed": all(row["passed"] for row in checks),
        "elapsedSeconds": time.perf_counter() - started,
        "scope": {
            "provesContinuumTheorem": False,
            "provesNSERegularity": False,
            "note": "Finite bilateral solves corroborate, but do not replace, the analytic infinite-lattice proof.",
        },
    }
    if not payload["allPassed"]:
        failed = [row["name"] for row in checks if not row["passed"]]
        raise AssertionError(f"producer checks failed: {failed}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    emit(f"R0.72A producer audit passed in {payload['elapsedSeconds']:.2f}s")


if __name__ == "__main__":
    main()
