#!/usr/bin/env python3
"""Exact polarization relay and reverse-edge obstruction audit.

For the cone-chain matrix

    M = I + 1 1^T,

write a_n=M^n e_1, b_n=M^n e_2, d_n=M^n e_3 and

    P_n=a_n+b_n=-c_n,  Q_n=a_n+d_n=-e_n.

The three directed frequency gates are

    (P_n,Q_n) -> a_{n+1},
    (a_n,b_n) -> P_n,
    (a_n,d_n) -> Q_n.

This script constructs unit polarizations for which all three desired center
interactions are nonzero, their three conjugate difference-frequency centers
vanish, and the complex phases repeat from one shell to the next.  It also
computes the reverse interactions.  Those reverse edges leave the selected
one-dimensional polarization lines with a nonzero, scale-uniform defect.

The calculations are exact vector identities checked in floating point.  They
do not estimate dense-packet errors, heat timing, nonlinear Picard remainders,
or Navier--Stokes regularity.
"""

from __future__ import annotations

import json
import math

import numpy as np


MATRIX = np.asarray(
    [
        [2, 1, 1],
        [1, 2, 1],
        [1, 1, 2],
    ],
    dtype=np.int64,
)

A_BASE = np.asarray([1, 0, 0], dtype=np.int64)
B_BASE = np.asarray([0, 1, 0], dtype=np.int64)
D_BASE = np.asarray([0, 0, 1], dtype=np.int64)
ASYMPTOTIC_GATE = math.sqrt(3.0 / 2.0)
ASYMPTOTIC_REVERSE_DEFECT = 3.0 / (2.0 * math.sqrt(2.0))


def transformed(base: np.ndarray, level: int) -> np.ndarray:
    """Return M**level times an integer base vector."""

    return np.linalg.matrix_power(MATRIX, level) @ base


def unit(vector: np.ndarray) -> np.ndarray:
    """Return a real or complex Euclidean unit vector."""

    value = np.asarray(vector)
    return value / np.linalg.norm(value)


def project(wavevector: np.ndarray, coefficient: np.ndarray) -> np.ndarray:
    """Apply the Leray projector at one nonzero wavevector."""

    frequency = np.asarray(wavevector, dtype=float)
    value = np.asarray(coefficient, dtype=np.complex128)
    return value - frequency * (
        np.dot(frequency, value) / np.dot(frequency, frequency)
    )


def center_kernel(
    first_wavevector: np.ndarray,
    second_wavevector: np.ndarray,
    first_polarization: np.ndarray,
    second_polarization: np.ndarray,
) -> np.ndarray:
    """Return the symmetrized Fourier--Leray interaction at p+q."""

    first = np.asarray(first_wavevector, dtype=float)
    second = np.asarray(second_wavevector, dtype=float)
    output = first + second
    raw = 1.0j * (
        np.dot(second, first_polarization) * second_polarization
        + np.dot(first, second_polarization) * first_polarization
    )
    return project(output, raw)


def line_defect(value: np.ndarray, direction: np.ndarray) -> float:
    """Return the norm perpendicular to a complex one-dimensional line."""

    normalized = unit(direction)
    scalar = np.vdot(normalized, value)
    return float(np.linalg.norm(value - scalar * normalized))


def geometry(level: int) -> dict[str, np.ndarray]:
    """Return the shell modes and their three forced range directions."""

    a_mode = transformed(A_BASE, level)
    b_mode = transformed(B_BASE, level)
    d_mode = transformed(D_BASE, level)
    p_mode = a_mode + b_mode
    q_mode = a_mode + d_mode
    return {
        "a": a_mode,
        "b": b_mode,
        "d": d_mode,
        "P": p_mode,
        "Q": q_mode,
        "nextA": p_mode + q_mode,
        "pi": np.cross(a_mode, b_mode),
        "theta": np.cross(a_mode, d_mode),
        "eta": np.cross(p_mode, q_mode),
    }


def closed_geometry(level: int) -> dict[str, object]:
    """Return the closed coordinate and norm formulas at one shell."""

    x_value = float(4**level)
    return {
        "x": x_value,
        "a": [(x_value + 2.0) / 3.0, (x_value - 1.0) / 3.0, (x_value - 1.0) / 3.0],
        "b": [(x_value - 1.0) / 3.0, (x_value + 2.0) / 3.0, (x_value - 1.0) / 3.0],
        "d": [(x_value - 1.0) / 3.0, (x_value - 1.0) / 3.0, (x_value + 2.0) / 3.0],
        "pi": [(1.0 - x_value) / 3.0, (1.0 - x_value) / 3.0, (2.0 * x_value + 1.0) / 3.0],
        "theta": [(x_value - 1.0) / 3.0, -(2.0 * x_value + 1.0) / 3.0, (x_value - 1.0) / 3.0],
        "eta": [(4.0 * x_value - 1.0) / 3.0, -(2.0 * x_value + 1.0) / 3.0, -(2.0 * x_value + 1.0) / 3.0],
        "aSquared": (x_value**2 + 2.0) / 3.0,
        "piSquared": (2.0 * x_value**2 + 1.0) / 3.0,
        "etaSquared": (8.0 * x_value**2 + 1.0) / 3.0,
    }


def wing_gate_scalar(level: int) -> float:
    """Return the difference-cancelled a+b -> P gate coefficient."""

    x_value = float(4**level)
    return math.sqrt(3.0) * x_value / math.sqrt(2.0 * x_value**2 + 1.0)


def cross_gate_scalar(level: int) -> float:
    """Return the P+Q -> a_next gate coefficient."""

    x_value = float(4**level)
    return 2.0 * math.sqrt(3.0) * x_value / math.sqrt(8.0 * x_value**2 + 1.0)


def relay_polarizations(level: int) -> dict[str, np.ndarray]:
    """Return the phase-compatible relay polarizations at shell n >= 1."""

    if level < 1:
        raise ValueError("The relay polarization A_n uses eta_(n-1), so n >= 1.")
    current = geometry(level)
    previous = geometry(level - 1)
    a_polarization = unit(previous["eta"])
    return {
        "A": a_polarization,
        # Coordinate reflections map a_n^perp isometrically to b_n^perp and
        # d_n^perp.  The first sign makes both wing outputs point in the
        # chosen pi/theta orientations.
        "B": -a_polarization[[1, 0, 2]],
        "D": a_polarization[[2, 1, 0]],
        "P": unit(current["pi"]),
        "Q": unit(current["theta"]),
        "nextA": unit(current["eta"]),
    }


def relay_record(level: int) -> dict[str, object]:
    """Compute all directed, difference, and reverse gates at one shell."""

    current = geometry(level)
    polarizations = relay_polarizations(level)
    a_mode = current["a"]
    b_mode = current["b"]
    d_mode = current["d"]
    p_mode = current["P"]
    q_mode = current["Q"]
    next_a_mode = current["nextA"]
    a_polarization = polarizations["A"]
    b_polarization = polarizations["B"]
    d_polarization = polarizations["D"]
    p_polarization = polarizations["P"]
    q_polarization = polarizations["Q"]
    next_a_polarization = polarizations["nextA"]
    wing_scalar = wing_gate_scalar(level)
    cross_scalar = cross_gate_scalar(level)
    previous_cross_scalar = cross_gate_scalar(level - 1)

    wing_p = center_kernel(
        a_mode,
        b_mode,
        1.0j * a_polarization,
        b_polarization,
    )
    wing_q = center_kernel(
        a_mode,
        d_mode,
        1.0j * a_polarization,
        d_polarization,
    )
    cross = center_kernel(
        p_mode,
        q_mode,
        p_polarization,
        q_polarization,
    )

    differences = {
        "aMinusB": center_kernel(
            a_mode,
            -b_mode,
            1.0j * a_polarization,
            np.conjugate(b_polarization),
        ),
        "aMinusD": center_kernel(
            a_mode,
            -d_mode,
            1.0j * a_polarization,
            np.conjugate(d_polarization),
        ),
        "PMinusQ": center_kernel(
            p_mode,
            -q_mode,
            p_polarization,
            np.conjugate(q_polarization),
        ),
    }

    cross_reverse_p = center_kernel(
        next_a_mode,
        -q_mode,
        1.0j * next_a_polarization,
        np.conjugate(q_polarization),
    )
    cross_reverse_q = center_kernel(
        next_a_mode,
        -p_mode,
        1.0j * next_a_polarization,
        np.conjugate(p_polarization),
    )
    wing_reverse_a_from_p = center_kernel(
        p_mode,
        -b_mode,
        p_polarization,
        np.conjugate(b_polarization),
    )
    wing_reverse_a_from_q = center_kernel(
        q_mode,
        -d_mode,
        q_polarization,
        np.conjugate(d_polarization),
    )
    wing_reverse_b = center_kernel(
        p_mode,
        -a_mode,
        p_polarization,
        np.conjugate(1.0j * a_polarization),
    )
    wing_reverse_d = center_kernel(
        q_mode,
        -a_mode,
        q_polarization,
        np.conjugate(1.0j * a_polarization),
    )

    maximum_difference = max(float(np.linalg.norm(value)) for value in differences.values())
    forward_errors = {
        "wingP": float(np.linalg.norm(wing_p - wing_scalar * p_polarization)),
        "wingQ": float(np.linalg.norm(wing_q - wing_scalar * q_polarization)),
        "cross": float(
            np.linalg.norm(cross - 1.0j * cross_scalar * next_a_polarization)
        ),
    }
    reverse_errors = {
        "crossToP": float(
            np.linalg.norm(cross_reverse_p - wing_scalar * next_a_polarization)
        ),
        "crossToQ": float(
            np.linalg.norm(cross_reverse_q + wing_scalar * next_a_polarization)
        ),
        "wingPToA": float(
            np.linalg.norm(
                wing_reverse_a_from_p
                - 1.0j * previous_cross_scalar * p_polarization
            )
        ),
        "wingQToA": float(
            np.linalg.norm(
                wing_reverse_a_from_q
                + 1.0j * previous_cross_scalar * q_polarization
            )
        ),
    }

    combined_wing_reverse = wing_reverse_a_from_p + wing_reverse_a_from_q
    return {
        "level": level,
        "x": 4**level,
        "closureResidual": float(np.linalg.norm(next_a_mode - transformed(A_BASE, level + 1))),
        "divergenceResidual": max(
            float(abs(np.dot(a_mode, a_polarization))),
            float(abs(np.dot(b_mode, b_polarization))),
            float(abs(np.dot(d_mode, d_polarization))),
            float(abs(np.dot(p_mode, p_polarization))),
            float(abs(np.dot(q_mode, q_polarization))),
            float(abs(np.dot(next_a_mode, next_a_polarization))),
        ),
        "wingGateScalar": wing_scalar,
        "crossGateScalar": cross_scalar,
        "forwardMaximumError": max(forward_errors.values()),
        "forwardErrors": forward_errors,
        "differenceMaximumNorm": maximum_difference,
        "crossReverseNorm": float(np.linalg.norm(cross_reverse_p)),
        "crossReverseLineDefect": line_defect(cross_reverse_p, p_polarization),
        "crossReverseDefectToForward": line_defect(
            cross_reverse_p,
            p_polarization,
        )
        / cross_scalar,
        "wingCatalystReverseNorm": float(np.linalg.norm(wing_reverse_b)),
        "wingCatalystReverseLineDefect": line_defect(
            wing_reverse_b,
            b_polarization,
        ),
        "combinedWingReverseToALineDefect": line_defect(
            combined_wing_reverse,
            1.0j * a_polarization,
        ),
        "reverseMaximumFormulaError": max(reverse_errors.values()),
        "reverseErrors": reverse_errors,
    }


def rank_one_random_audit(samples: int = 2000) -> dict[str, float]:
    """Check the equal-length range lemma on random complex polarizations."""

    random = np.random.default_rng(20260816)
    p_mode = np.asarray([2.0, 1.0, 0.0])
    q_mode = np.asarray([2.0, -1.0, 0.0])
    normal = unit(np.cross(p_mode, q_mode))
    maximum_range_error = 0.0
    maximum_difference_coordinate_error = 0.0
    for _ in range(samples):
        u_tangent, u_normal, v_tangent, v_normal = (
            random.normal(size=4) + 1.0j * random.normal(size=4)
        )
        p_tangent = unit(np.asarray([-1.0, 2.0, 0.0]))
        q_tangent = unit(np.asarray([1.0, 2.0, 0.0]))
        first = u_tangent * p_tangent + u_normal * normal
        second = v_tangent * q_tangent + v_normal * normal
        output = center_kernel(p_mode, q_mode, first, second)
        maximum_range_error = max(
            maximum_range_error,
            line_defect(output, normal),
        )

        difference = center_kernel(
            p_mode,
            -q_mode,
            first,
            np.conjugate(second),
        )
        length_factor = abs(np.dot(q_mode, p_tangent))
        predicted = 1.0j * length_factor * (
            u_tangent * np.conjugate(v_normal)
            + np.conjugate(v_tangent) * u_normal
        ) * normal
        maximum_difference_coordinate_error = max(
            maximum_difference_coordinate_error,
            float(np.linalg.norm(difference - predicted)),
        )
    return {
        "samples": samples,
        "maximumRangeError": maximum_range_error,
        "maximumDifferenceCoordinateError": maximum_difference_coordinate_error,
    }


def run_audit(levels: tuple[int, ...] = (1, 2, 3, 4, 5, 6)) -> dict[str, object]:
    """Return the full relay audit as JSON-serializable data."""

    return {
        "statement": (
            "exact center polarization relay and reverse-line obstruction; "
            "no dense-packet timing or nonlinear remainder estimate"
        ),
        "equalLengthLemma": {
            "range": "for |p|=|q|, the p+q kernel lies in span(p cross q)",
            "coordinateSumScalar": "v*x-u*y",
            "coordinateDifferenceScalar": "u*conj(y)+conj(v)*x",
            "reversePScalar": "conj(v)",
            "reverseQScalar": "conj(u)",
            "consequence": (
                "nonzero sum plus zero difference is incompatible with "
                "one-line closure of both reverse edges"
            ),
        },
        "limits": {
            "wingGateScalar": ASYMPTOTIC_GATE,
            "crossGateScalar": ASYMPTOTIC_GATE,
            "reverseLineDefect": ASYMPTOTIC_REVERSE_DEFECT,
        },
        "closedGeometry": [closed_geometry(level) for level in levels],
        "records": [relay_record(level) for level in levels],
        "rankOneRandomAudit": rank_one_random_audit(),
    }


def validate(audit: dict[str, object]) -> None:
    """Validate direct calculations against all closed formulas."""

    rank_one = audit["rankOneRandomAudit"]
    assert rank_one["maximumRangeError"] < 2e-14
    assert rank_one["maximumDifferenceCoordinateError"] < 2e-14
    for geometry_record, record in zip(
        audit["closedGeometry"],
        audit["records"],
        strict=True,
    ):
        level = int(record["level"])
        direct = geometry(level)
        for name in ("a", "b", "d", "pi", "theta", "eta"):
            assert np.linalg.norm(
                direct[name] - np.asarray(geometry_record[name])
            ) < 2e-10
        assert record["closureResidual"] == 0.0
        assert record["divergenceResidual"] < 2e-10
        assert record["forwardMaximumError"] < 2e-10
        assert record["differenceMaximumNorm"] < 2e-10
        assert record["reverseMaximumFormulaError"] < 2e-10
        assert record["combinedWingReverseToALineDefect"] < 2e-10
        assert record["crossReverseLineDefect"] > 0.8
        assert record["wingCatalystReverseLineDefect"] > 0.8
    final = audit["records"][-1]
    assert abs(final["wingGateScalar"] - ASYMPTOTIC_GATE) < 2e-7
    assert abs(final["crossGateScalar"] - ASYMPTOTIC_GATE) < 2e-8
    assert abs(final["crossReverseLineDefect"] - ASYMPTOTIC_REVERSE_DEFECT) < 3e-7


def main() -> None:
    audit = run_audit()
    validate(audit)
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
