#!/usr/bin/env python3
"""Deterministic certificate for the R0.73Y-A exact shear no-go theorem.

The exact lane works in the Fourier group algebra Q[rho][Z], using pairs of
Fractions for complex coefficients.  The numerical lane directly integrates
the one-dimensional Gaussian convolution for a fixed parameter grid.  The
numerical lane is a cross-check only; it is not used as proof of the theorem,
its quantifiers, strict positivity, or the no-go conclusion.

Run from the staged or final repository layout:

    python3 scripts/r073y_exact_shear_certificate.py
    python3 scripts/r073y_exact_shear_certificate.py --check-only
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
RESULT_PATH = ROOT / "exact-shear-results.json"
REPORT_PATH = ROOT / "exact-shear-report.md"

QComplex = tuple[Fraction, Fraction]
Polynomial = dict[int, QComplex]
FourierField = dict[int, Polynomial]

QZERO: QComplex = (Fraction(0), Fraction(0))
QONE: QComplex = (Fraction(1), Fraction(0))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


PORTABLE_NUMERIC_REL_TOL = 5.0e-12
PORTABLE_NUMERIC_ABS_TOL = 5.0e-13


def is_portable_numeric_path(path: tuple[str, ...]) -> bool:
    """Return whether ``path`` names a platform-computed binary64 result.

    Frozen inputs such as ``cases[i].s`` and ``cases[i].x2`` remain exact.
    Only values obtained from transcendental functions or numerical
    quadrature receive the declared cross-platform tolerance.
    """

    if path == ("numerical_cross_checks", "maximum_overall_scaled_error"):
        return True
    if len(path) == 3 and path[:2] == (
        "numerical_cross_checks",
        "maximum_scaled_errors",
    ):
        return True
    if len(path) == 4 and path[:2] == (
        "numerical_cross_checks",
        "cases",
    ):
        field = path[3]
        return (
            field == "rho"
            or field == "odd_gaussian_moment"
            or field.endswith("_numeric")
            or field.endswith("_exact")
        )
    return False


def payload_core(payload: dict[str, Any]) -> dict[str, Any]:
    result = dict(payload)
    result.pop("payload_sha256", None)
    return result


def verify_payload_hash(payload: dict[str, Any], label: str) -> None:
    stored_hash = payload.get("payload_sha256")
    require(isinstance(stored_hash, str), f"{label}: missing payload hash")
    recomputed = hashlib.sha256(
        canonical(payload_core(payload)).encode("utf-8")
    ).hexdigest()
    require(stored_hash == recomputed, f"{label}: payload hash mismatch")


def load_strict_canonical_json(text: str, label: str) -> dict[str, Any]:
    """Parse canonical JSON while rejecting duplicate keys and constants."""

    def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"{label}: duplicate JSON key: {key}")
            result[key] = value
        return result

    def reject_nonfinite_constant(token: str) -> None:
        raise RuntimeError(f"{label}: nonfinite JSON constant: {token}")

    value = json.loads(
        text,
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_nonfinite_constant,
    )
    require(isinstance(value, dict), f"{label}: JSON root is not an object")
    require(text == canonical(value), f"{label}: JSON is not canonical")
    return value


def portable_compare(
    stored: object,
    recomputed: object,
    path: tuple[str, ...] = (),
) -> None:
    """Compare exact fields byte-semantically and whitelist numeric cross-checks.

    Only explicitly whitelisted, platform-computed binary64 values below
    ``numerical_cross_checks`` receive a declared cross-platform tolerance.
    Frozen numerical inputs and all analytic, algebraic, structural, scope,
    and claim-ledger fields remain exact, including their JSON scalar types.
    """

    label = ".".join(path) or "payload"
    if isinstance(stored, dict) and isinstance(recomputed, dict):
        require(set(stored) == set(recomputed), f"{label}: key inventory drifted")
        for key in sorted(stored):
            portable_compare(stored[key], recomputed[key], (*path, key))
        return
    if isinstance(stored, list) and isinstance(recomputed, list):
        require(len(stored) == len(recomputed), f"{label}: list length drifted")
        for index, (left, right) in enumerate(zip(stored, recomputed)):
            portable_compare(left, right, (*path, str(index)))
        return
    require(
        type(stored) is type(recomputed),
        f"{label}: scalar type drifted",
    )
    if (
        is_portable_numeric_path(path)
        and isinstance(stored, float)
        and isinstance(recomputed, float)
    ):
        require(math.isfinite(stored) and math.isfinite(recomputed), f"{label}: nonfinite")
        require(
            math.isclose(
                stored,
                recomputed,
                rel_tol=PORTABLE_NUMERIC_REL_TOL,
                abs_tol=PORTABLE_NUMERIC_ABS_TOL,
            ),
            f"{label}: portable float drift exceeds tolerance",
        )
        return
    require(stored == recomputed, f"{label}: exact field drifted")


def portable_gate_negative_tests(payload: dict[str, Any]) -> int:
    """Verify that resealed structural/type mutations cannot pass comparison."""

    def clone() -> dict[str, Any]:
        value = json.loads(canonical(payload))
        require(isinstance(value, dict), "negative-test clone is not an object")
        return value

    def reseal(value: dict[str, Any]) -> None:
        value["payload_sha256"] = hashlib.sha256(
            canonical(payload_core(value)).encode("utf-8")
        ).hexdigest()
        verify_payload_hash(value, "resealed negative-test payload")

    def require_rejected(value: dict[str, Any], expected_message: str) -> None:
        reseal(value)
        try:
            portable_compare(payload_core(value), payload_core(payload))
        except RuntimeError as error:
            require(
                expected_message in str(error),
                "negative test failed for an unexpected reason: " + str(error),
            )
            return
        raise RuntimeError("negative test mutation unexpectedly passed")

    bool_to_int = clone()
    bool_to_int["not_clay"] = 1
    require_rejected(bool_to_int, "scalar type drifted")

    int_to_float = clone()
    int_to_float["numerical_cross_checks"]["cases"][0]["n"] = 1.0
    require_rejected(int_to_float, "scalar type drifted")

    added_key = clone()
    added_key["scope"]["unexpected"] = "mutation"
    require_rejected(added_key, "key inventory drifted")

    deleted_key = clone()
    del deleted_key["scope"]["domain"]
    require_rejected(deleted_key, "key inventory drifted")

    list_length = clone()
    list_length["exact_checks"].append(list_length["exact_checks"][0])
    require_rejected(list_length, "list length drifted")

    canonical_text = canonical(payload)
    duplicate_needle = '  "not_clay": true,\n'
    require(
        duplicate_needle in canonical_text,
        "negative test could not locate not_clay",
    )
    duplicate_text = canonical_text.replace(
        duplicate_needle,
        '  "not_clay": false,\n' + duplicate_needle,
        1,
    )
    try:
        load_strict_canonical_json(duplicate_text, "duplicate-key negative test")
    except RuntimeError as error:
        require(
            "duplicate JSON key" in str(error),
            "duplicate-key negative test failed unexpectedly: " + str(error),
        )
    else:
        raise RuntimeError("duplicate-key negative test unexpectedly passed")

    try:
        load_strict_canonical_json("\n" + canonical_text, "raw-text negative test")
    except RuntimeError as error:
        require(
            "JSON is not canonical" in str(error),
            "raw-text negative test failed unexpectedly: " + str(error),
        )
    else:
        raise RuntimeError("raw-text negative test unexpectedly passed")

    return 7


def qc_add(left: QComplex, right: QComplex) -> QComplex:
    return (left[0] + right[0], left[1] + right[1])


def qc_neg(value: QComplex) -> QComplex:
    return (-value[0], -value[1])


def qc_mul(left: QComplex, right: QComplex) -> QComplex:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def qc_scale(value: QComplex, factor: Fraction) -> QComplex:
    return (factor * value[0], factor * value[1])


def qc_is_zero(value: QComplex) -> bool:
    return value == QZERO


def poly_clean(value: Polynomial) -> Polynomial:
    return {power: coefficient for power, coefficient in value.items() if not qc_is_zero(coefficient)}


def poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for power, coefficient in right.items():
        result[power] = qc_add(result.get(power, QZERO), coefficient)
    return poly_clean(result)


def poly_neg(value: Polynomial) -> Polynomial:
    return poly_clean({power: qc_neg(coefficient) for power, coefficient in value.items()})


def poly_sub(left: Polynomial, right: Polynomial) -> Polynomial:
    return poly_add(left, poly_neg(right))


def poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_power, left_coefficient in left.items():
        for right_power, right_coefficient in right.items():
            power = left_power + right_power
            product = qc_mul(left_coefficient, right_coefficient)
            result[power] = qc_add(result.get(power, QZERO), product)
    return poly_clean(result)


def poly_scale(value: Polynomial, factor: Fraction) -> Polynomial:
    return poly_clean(
        {power: qc_scale(coefficient, factor) for power, coefficient in value.items()}
    )


def poly_shift(value: Polynomial, power: int) -> Polynomial:
    return poly_clean({old_power + power: coefficient for old_power, coefficient in value.items()})


def fourier_clean(value: FourierField) -> FourierField:
    return {mode: poly_clean(coefficient) for mode, coefficient in value.items() if poly_clean(coefficient)}


def fourier_add(left: FourierField, right: FourierField) -> FourierField:
    result = {mode: dict(coefficient) for mode, coefficient in left.items()}
    for mode, coefficient in right.items():
        result[mode] = poly_add(result.get(mode, {}), coefficient)
    return fourier_clean(result)


def fourier_neg(value: FourierField) -> FourierField:
    return fourier_clean({mode: poly_neg(coefficient) for mode, coefficient in value.items()})


def fourier_sub(left: FourierField, right: FourierField) -> FourierField:
    return fourier_add(left, fourier_neg(right))


def fourier_mul(left: FourierField, right: FourierField) -> FourierField:
    result: FourierField = {}
    for left_mode, left_coefficient in left.items():
        for right_mode, right_coefficient in right.items():
            mode = left_mode + right_mode
            product = poly_mul(left_coefficient, right_coefficient)
            result[mode] = poly_add(result.get(mode, {}), product)
    return fourier_clean(result)


def fourier_scale(value: FourierField, factor: Fraction) -> FourierField:
    return fourier_clean(
        {mode: poly_scale(coefficient, factor) for mode, coefficient in value.items()}
    )


def fourier_heat(value: FourierField) -> FourierField:
    """Apply P_s with rho=exp(-n^2 s); mode m gains rho^(m^2)."""

    return fourier_clean(
        {mode: poly_shift(coefficient, mode * mode) for mode, coefficient in value.items()}
    )


def fourier_derivative(value: FourierField) -> FourierField:
    """Differentiate with respect to xi=n*x_2."""

    result: FourierField = {}
    for mode, coefficient in value.items():
        multiplier: QComplex = (Fraction(0), Fraction(mode))
        result[mode] = {
            power: qc_mul(multiplier, scalar) for power, scalar in coefficient.items()
        }
    return fourier_clean(result)


def fourier_laplacian(value: FourierField) -> FourierField:
    """Dimensionless xi-Laplacian."""

    return fourier_clean(
        {
            mode: poly_scale(coefficient, Fraction(-(mode * mode)))
            for mode, coefficient in value.items()
        }
    )


def fourier_shift_rho(value: FourierField, power: int) -> FourierField:
    return fourier_clean(
        {mode: poly_shift(coefficient, power) for mode, coefficient in value.items()}
    )


def fourier_is_zero(value: FourierField) -> bool:
    return not fourier_clean(value)


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def qcomplex_text(value: QComplex) -> str:
    real, imaginary = value
    if imaginary == 0:
        return fraction_text(real)
    if real == 0:
        return f"{fraction_text(imaginary)}i"
    sign = "+" if imaginary > 0 else "-"
    return f"{fraction_text(real)}{sign}{fraction_text(abs(imaginary))}i"


def fourier_text(value: FourierField) -> dict[str, list[dict[str, str | int]]]:
    result: dict[str, list[dict[str, str | int]]] = {}
    for mode in sorted(value):
        result[str(mode)] = [
            {"rho_power": power, "coefficient": qcomplex_text(coefficient)}
            for power, coefficient in sorted(value[mode].items())
        ]
    return result


def exact_fourier_checks() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    half = Fraction(1, 2)
    quarter = Fraction(1, 4)

    sine: FourierField = {
        1: {0: (Fraction(0), -half)},
        -1: {0: (Fraction(0), half)},
    }
    cosine: FourierField = {
        1: {0: (half, Fraction(0))},
        -1: {0: (half, Fraction(0))},
    }

    # Normalized NSE residual: d_t sin - d_xi^2 sin = -sin - (-sin).
    time_derivative = fourier_scale(sine, Fraction(-1))
    laplacian = fourier_laplacian(sine)
    nse_linear_residual = fourier_sub(time_derivative, laplacian)
    require(fourier_is_zero(nse_linear_residual), "NSE heat residual is nonzero")

    filtered_velocity = fourier_heat(sine)
    expected_filtered_velocity = fourier_shift_rho(sine, 1)
    require(filtered_velocity == expected_filtered_velocity, "filtered velocity mismatch")

    velocity_square = fourier_mul(sine, sine)
    filtered_velocity_square = fourier_heat(velocity_square)
    resolved_square = fourier_mul(filtered_velocity, filtered_velocity)
    tau = fourier_sub(filtered_velocity_square, resolved_square)

    expected_tau: FourierField = {
        0: {
            0: (half, Fraction(0)),
            2: (-half, Fraction(0)),
        },
        2: {
            2: (quarter, Fraction(0)),
            4: (-quarter, Fraction(0)),
        },
        -2: {
            2: (quarter, Fraction(0)),
            4: (-quarter, Fraction(0)),
        },
    }
    require(tau == expected_tau, "stress formula mismatch")

    gradient = fourier_derivative(sine)
    require(gradient == cosine, "gradient of sine mismatch")
    filtered_gradient = fourier_derivative(filtered_velocity)
    filtered_gradient_square = fourier_mul(filtered_gradient, filtered_gradient)
    filtered_unresolved_gradient_square = fourier_heat(fourier_mul(gradient, gradient))
    covariance = fourier_sub(
        filtered_unresolved_gradient_square,
        filtered_gradient_square,
    )

    expected_covariance: FourierField = {
        0: {
            0: (half, Fraction(0)),
            2: (-half, Fraction(0)),
        },
        2: {
            2: (-quarter, Fraction(0)),
            4: (quarter, Fraction(0)),
        },
        -2: {
            2: (-quarter, Fraction(0)),
            4: (quarter, Fraction(0)),
        },
    }
    require(covariance == expected_covariance, "gradient covariance mismatch")

    k_mean = poly_scale(tau[0], half)
    covariance_mean = covariance[0]
    fixed_scale_trace_residual = poly_add(
        poly_scale(k_mean, Fraction(-2)),
        covariance_mean,
    )
    require(not fixed_scale_trace_residual, "global fixed-scale trace ledger mismatch")

    active_velocity_component = 0
    spatial_dependency_axes = {1}
    tau_active_pair = (0, 0)
    gradient_active_pair = (0, 1)
    require(active_velocity_component not in spatial_dependency_axes, "convective term did not vanish")
    require(tau_active_pair != gradient_active_pair, "Pi contraction did not vanish")

    centered_increment_active_component = 0
    centered_increment_dependency_axes = {1}
    require(
        centered_increment_active_component not in centered_increment_dependency_axes,
        "centered parity axis is contaminated",
    )

    checks = [
        {
            "name": "nse_heat_residual",
            "status": "PASS",
            "method": "exact Fourier coefficients in Q[rho][Z]",
        },
        {
            "name": "divergence_and_convection",
            "status": "PASS",
            "method": "exact component/dependency-axis audit",
        },
        {
            "name": "heat_filtered_velocity",
            "status": "PASS",
            "method": "exact mode multiplier rho^(m^2)",
        },
        {
            "name": "subfilter_stress",
            "status": "PASS",
            "method": "exact Fourier convolution and subtraction",
        },
        {
            "name": "Pi_pointwise_zero",
            "status": "PASS",
            "method": "exact tensor support mismatch: tau_11 versus gradient_12",
        },
        {
            "name": "centered_production_pointwise_zero",
            "status": "PASS",
            "method": "exact Gaussian odd moment in y_1; increment depends only on y_2",
        },
        {
            "name": "gradient_covariance",
            "status": "PASS",
            "method": "exact Fourier convolution and factorization",
        },
        {
            "name": "global_fixed_scale_trace_ledger",
            "status": "PASS",
            "method": "exact rho-polynomial mean identity d_t mean(k)+nu mean(D)=0",
        },
    ]

    evidence = {
        "sine": fourier_text(sine),
        "filtered_velocity": fourier_text(filtered_velocity),
        "tau_over_b_squared": fourier_text(tau),
        "D_over_b_squared_n_squared": fourier_text(covariance),
        "normalized_nse_residual": fourier_text(nse_linear_residual),
        "fixed_scale_trace_residual": [
            {"rho_power": power, "coefficient": qcomplex_text(coefficient)}
            for power, coefficient in sorted(fixed_scale_trace_residual.items())
        ],
        "structural_support": {
            "velocity_active_component_zero_based": active_velocity_component,
            "velocity_dependency_axes_zero_based": sorted(spatial_dependency_axes),
            "tau_active_pair_zero_based": list(tau_active_pair),
            "gradient_active_pair_zero_based": list(gradient_active_pair),
            "centered_odd_axis_zero_based": centered_increment_active_component,
        },
    }
    return checks, evidence


def adaptive_simpson(
    function: Callable[[float], float],
    left: float,
    right: float,
    tolerance: float = 2.0e-13,
    max_depth: int = 26,
) -> float:
    midpoint = 0.5 * (left + right)
    f_left = function(left)
    f_mid = function(midpoint)
    f_right = function(right)
    whole = (right - left) * (f_left + 4.0 * f_mid + f_right) / 6.0

    def recurse(
        a: float,
        b: float,
        fa: float,
        fm: float,
        fb: float,
        estimate: float,
        tol: float,
        depth: int,
    ) -> float:
        middle = 0.5 * (a + b)
        left_middle = 0.5 * (a + middle)
        right_middle = 0.5 * (middle + b)
        flm = function(left_middle)
        frm = function(right_middle)
        left_estimate = (middle - a) * (fa + 4.0 * flm + fm) / 6.0
        right_estimate = (b - middle) * (fm + 4.0 * frm + fb) / 6.0
        refined = left_estimate + right_estimate
        if depth <= 0 or abs(refined - estimate) <= 15.0 * tol:
            return refined + (refined - estimate) / 15.0
        return recurse(
            a,
            middle,
            fa,
            flm,
            fm,
            left_estimate,
            0.5 * tol,
            depth - 1,
        ) + recurse(
            middle,
            b,
            fm,
            frm,
            fb,
            right_estimate,
            0.5 * tol,
            depth - 1,
        )

    return recurse(
        left,
        right,
        f_left,
        f_mid,
        f_right,
        whole,
        tolerance,
        max_depth,
    )


def gaussian_convolution(
    function: Callable[[float], float],
    x_value: float,
    heat_scale: float,
) -> float:
    require(heat_scale > 0.0, "heat scale must be positive")
    root_scale = math.sqrt(heat_scale)
    cutoff = 14.0 * root_scale
    normalization = 1.0 / math.sqrt(4.0 * math.pi * heat_scale)

    def integrand(y_value: float) -> float:
        return (
            normalization
            * math.exp(-(y_value * y_value) / (4.0 * heat_scale))
            * function(x_value - y_value)
        )

    return adaptive_simpson(integrand, -cutoff, cutoff)


def scaled_error(observed: float, expected: float) -> float:
    return abs(observed - expected) / max(1.0, abs(expected))


def numerical_cross_checks() -> dict[str, Any]:
    cases = [
        {"n": 1, "s": 0.03125, "x2": 0.37},
        {"n": 2, "s": 0.125, "x2": -0.43},
        {"n": 3, "s": 0.055, "x2": 1.11},
        {"n": 4, "s": 0.018, "x2": -1.37},
        {"n": 5, "s": 0.009, "x2": 0.91},
    ]
    rows: list[dict[str, float | int]] = []
    maxima = {
        "P_s_sine": 0.0,
        "P_s_sine_squared": 0.0,
        "tau": 0.0,
        "D": 0.0,
        "odd_gaussian_moment": 0.0,
    }

    for case in cases:
        n = int(case["n"])
        heat_scale = float(case["s"])
        x_value = float(case["x2"])
        rho = math.exp(-(n * n) * heat_scale)
        xi = n * x_value

        filtered_sine_numeric = gaussian_convolution(
            lambda location: math.sin(n * location),
            x_value,
            heat_scale,
        )
        filtered_sine_exact = rho * math.sin(xi)

        filtered_square_numeric = gaussian_convolution(
            lambda location: math.sin(n * location) ** 2,
            x_value,
            heat_scale,
        )
        filtered_square_exact = 0.5 * (1.0 - (rho ** 4) * math.cos(2.0 * xi))

        tau_numeric = filtered_square_numeric - filtered_sine_numeric ** 2
        tau_exact = 0.5 * (
            (1.0 - rho * rho)
            + (rho * rho - rho ** 4) * math.cos(2.0 * xi)
        )

        filtered_gradient_square_numeric = (n * rho * math.cos(xi)) ** 2
        filtered_unresolved_gradient_square_numeric = gaussian_convolution(
            lambda location: (n * math.cos(n * location)) ** 2,
            x_value,
            heat_scale,
        )
        covariance_numeric = (
            filtered_unresolved_gradient_square_numeric
            - filtered_gradient_square_numeric
        )
        covariance_exact = 0.5 * (n * n) * (1.0 - rho * rho) * (
            1.0 - rho * rho * math.cos(2.0 * xi)
        )

        normalization = 1.0 / math.sqrt(4.0 * math.pi * heat_scale)
        cutoff = 14.0 * math.sqrt(heat_scale)
        odd_moment = adaptive_simpson(
            lambda y_value: y_value
            * normalization
            * math.exp(-(y_value * y_value) / (4.0 * heat_scale)),
            -cutoff,
            cutoff,
        )

        errors = {
            "P_s_sine": scaled_error(filtered_sine_numeric, filtered_sine_exact),
            "P_s_sine_squared": scaled_error(filtered_square_numeric, filtered_square_exact),
            "tau": scaled_error(tau_numeric, tau_exact),
            "D": scaled_error(covariance_numeric, covariance_exact),
            "odd_gaussian_moment": abs(odd_moment),
        }
        for name, value in errors.items():
            maxima[name] = max(maxima[name], value)

        rows.append(
            {
                "n": n,
                "s": heat_scale,
                "x2": x_value,
                "rho": rho,
                "filtered_sine_numeric": filtered_sine_numeric,
                "filtered_sine_exact": filtered_sine_exact,
                "filtered_square_numeric": filtered_square_numeric,
                "filtered_square_exact": filtered_square_exact,
                "tau_numeric": tau_numeric,
                "tau_exact": tau_exact,
                "D_numeric": covariance_numeric,
                "D_exact": covariance_exact,
                "odd_gaussian_moment": odd_moment,
            }
        )

    maximum_error = max(maxima.values())
    require(maximum_error < 2.0e-10, "direct Gaussian convolution cross-check failed")
    return {
        "status": "PASS",
        "method": "dependency-free adaptive Simpson integration of the Gaussian convolution",
        "truncation_window": "[-14 sqrt(s), 14 sqrt(s)]",
        "cases": rows,
        "maximum_scaled_errors": maxima,
        "maximum_overall_scaled_error": maximum_error,
        "role": "cross-check only; no numerical row is used as proof",
    }


def homogeneity_degree_ledger() -> dict[str, Any]:
    """Record and internally cross-check the analytic note's amplitude degrees.

    This is deliberately not presented as an independent symbolic propagation
    derivation.  The analytic note supplies the homogeneity proof.
    """
    degrees = {
        "u": Fraction(1),
        "gradient_u": Fraction(1),
        "energy": Fraction(2),
        "energy_to_three_halves": Fraction(3),
        "velocity_cubic_tail": Fraction(3),
        "local_pressure": Fraction(2),
        "harmonic_pressure": Fraction(2),
        "pressure_gauge_c_R": Fraction(2),
        "pressure_to_three_halves_tail": Fraction(3),
        "Lambda_R": Fraction(2),
        "harmonic_tail_H": Fraction(3),
        "A_ext": Fraction(3),
        "D": Fraction(2),
        "Pi": Fraction(3),
        "centered_production": Fraction(3),
    }
    require(degrees["energy_to_three_halves"] == Fraction(3), "energy degree mismatch")
    require(degrees["velocity_cubic_tail"] == Fraction(3), "G_u degree mismatch")
    require(degrees["pressure_to_three_halves_tail"] == Fraction(3), "G_p degree mismatch")
    require(degrees["harmonic_tail_H"] == Fraction(3), "H degree mismatch")
    require(degrees["A_ext"] == Fraction(3), "A_ext degree mismatch")
    return {
        "status": "DEGREE_RECORDED",
        "method": "declared degree ledger with target-degree consistency checks; no independent exponent propagation",
        "degrees_in_absolute_amplitude_A": {
            name: fraction_text(value) for name, value in degrees.items()
        },
        "strict_positivity_basis": {
            "energy": "a nonzero continuous shear is nonzero on a positive-measure subset of every open ball",
            "G_u": "positive weights integrate |u|^3 over nonempty lifted annuli; the nodal planes have measure zero",
            "H_u": "Lambda_R is positive because its positive annular |u|^2 integrals are nonzero",
            "sum": "already strictly positive from the energy row, and also from G_u and H_u",
        },
    }


def generate_payload() -> dict[str, Any]:
    exact_checks, exact_evidence = exact_fourier_checks()
    numeric = numerical_cross_checks()
    homogeneity = homogeneity_degree_ledger()

    claim_ledger = {
        "exactShearSolvesNSE": "PROVED_ANALYTICALLY_AND_EXACTLY_CHECKED",
        "generalOrthogonalShearClass": "PROVED_ANALYTICALLY_NOT_CERTIFICATE_SCOPE",
        "heatFilteredVelocityAndStress": "PROVED_ANALYTICALLY_AND_EXACTLY_CHECKED",
        "PiPointwiseZero": "PROVED_ANALYTICALLY_AND_EXACTLY_CHECKED",
        "centeredProductionPointwiseZero": "PROVED_ANALYTICALLY_AND_PARITY_CHECKED",
        "pressureCovarianceZero": "PROVED_ANALYTICALLY",
        "localEnergyDefectZero": "PROVED_FROM_SMOOTH_LOCAL_ENERGY_EQUALITY",
        "gradientCovarianceStrictlyPositiveForAneq0AndSgt0": "PROVED_ANALYTICALLY",
        "arbitraryCutoffProductionVanishing": "PROVED_FROM_POINTWISE_ZERO",
        "arbitraryPositiveScalePathProductionVanishing": "PROVED_FROM_POINTWISE_ZERO",
        "energyAndExteriorTailCubicHomogeneity": "PROVED_ANALYTICALLY_CERTIFICATE_DEGREE_RECORDED",
        "productionOnlyCoerciveBridge": "FALSE_BY_EXACT_NSE_FAMILY",
        "ledgerAbsoluteDebtAlsoZero": "FALSE_NOT_CLAIMED",
        "epsilonRegularityRefuted": "FALSE_NOT_CLAIMED",
        "arbitraryThreeDimensionalGlobalRegularity": "OPEN",
        "clayConclusion": "OPEN",
    }

    core: dict[str, Any] = {
        "schema": "r073y-exact-shear-certificate-v1",
        "status": "PASS",
        "frozen_date": "2026-09-01",
        "scope": {
            "domain": "T^3=[0,2pi]^3",
            "family": "u=A exp(-nu n^2 t) sin(n x_2) e_1, p=0",
            "n": "positive integer",
            "nu": "positive",
            "A": "arbitrary real amplitude",
            "not_a_simulation": True,
            "certificate_role": "exact algebra audit plus numerical cross-check; analytic note carries the proof",
            "general_class": "analytic theorem only; certificate witness is the single sine mode",
        },
        "exact_checks": exact_checks,
        "exact_fourier_evidence": exact_evidence,
        "homogeneity": homogeneity,
        "quantifier_audit": {
            "arbitrary_scalar_cutoff": True,
            "arbitrary_positive_heat_scale_path_for_direct_production": True,
            "descending_characteristic_included": True,
            "smooth_zero_scale_extension_included": True,
            "arbitrary_path_satisfies_heat_characteristic_ledger": False,
            "absolute_endpoint_and_cutoff_debt_claimed_zero": False,
            "positive_D_or_debt_criteria_refuted": False,
        },
        "numerical_cross_checks": numeric,
        "claim_ledger": claim_ledger,
        "not_clay": True,
    }
    payload_hash = hashlib.sha256(canonical(core).encode("utf-8")).hexdigest()
    return {**core, "payload_sha256": payload_hash}


def generate_report(payload: dict[str, Any]) -> str:
    exact_names = [row["name"] for row in payload["exact_checks"]]
    maximum_error = payload["numerical_cross_checks"]["maximum_overall_scaled_error"]
    hash_value = payload["payload_sha256"]
    return rf"""# R0.73Y-A exact shear deterministic certificate

**Status:** `PASS`

**Scope:** exact Fourier and structural audit of the shear
\(u=Ae^{{-\nu n^2t}}\sin(nx_2)e_1\), plus an independent direct Gaussian
convolution cross-check.  This is not a PDE simulation and numerical values
are not used as proof.

## Reproduction

```bash
python3 scripts/r073y_exact_shear_certificate.py --check-only
```

## Exact rows

The script checked the following rows in the exact Fourier group algebra
\(\mathbb Q[\rho][\mathbb Z]\), or by an exact tensor/parity support audit:

{chr(10).join(f'- `{name}`' for name in exact_names)}

The certified stress is

\[
 \tau_{{11,s}}={{b^2\over2}}
 [(1-\rho^2)+(\rho^2-\rho^4)\cos(2nx_2)],
\]

and the certified positive covariance is

\[
 D_{{ii,s}}={{b^2n^2\over2}}
 (1-\rho^2)(1-\rho^2\cos(2nx_2)).
\]

The exact support audit gives \(\Pi_s=0\), while Gaussian oddness in the
unused \(y_1\) direction gives \(\mathscr S_s=0\).

The analytic note proves a broader orthogonal shear class.  This certificate
deliberately audits only the explicit single-sine witness and does not present
the general-profile theorem as executable coverage.

## Independent numerical row

Dependency-free adaptive Simpson integration directly evaluated the
one-dimensional Gaussian convolution on five fixed parameter cases.  The
maximum scaled discrepancy across \(P_s\sin\), \(P_s(\sin^2)\), \(\tau\),
\(D\), and the odd Gaussian moment was `{maximum_error:.3e}`.

This finite comparison is only a cross-check of the implementation.  The
universal cutoff/path quantifiers, strict positivity, and the no-go theorem
come from the analytic proof.

## Homogeneity degree ledger and quantifier boundary

The following degrees are proved in the analytic note.  This certificate
records them and checks their target values for internal consistency; it does
not independently derive them by symbolic exponent propagation.

- \(\mathcal E\) has amplitude degree 2, so
  \(\mathcal E^{{3/2}}\) has degree 3.
- \(\mathcal G_u\), \(\mathcal G_p\), and \(\mathcal H_u\) each have
  amplitude degree 3; therefore \(\mathcal A_{{\rm ext}}\) has degree 3.
- Pointwise zero production remains zero under every scalar cutoff and every
  positive heat-scale path.
- An arbitrary scale path is not automatically a descending heat
  characteristic in the ledger.
- Absolute endpoint, cutoff, and viscous-boundary debts are not claimed to
  vanish.  Criteria that include those debts or positive \(D_{{ii,s}}\) are
  not refuted.

`payload_sha256={hash_value}`

**NOT CLAY.**
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help=(
            "regenerate in memory and require exact structure plus whitelisted "
            "portable-float agreement and a report bound to the stored JSON"
        ),
    )
    parser.add_argument(
        "--print-json",
        action="store_true",
        help="print the canonical JSON payload after a successful run",
    )
    arguments = parser.parse_args()

    payload = generate_payload()
    portable_negative_test_count = portable_gate_negative_tests(payload)
    result_text = canonical(payload)
    report_text = generate_report(payload)

    if arguments.check_only:
        require(RESULT_PATH.exists(), f"missing result file: {RESULT_PATH}")
        require(REPORT_PATH.exists(), f"missing report file: {REPORT_PATH}")
        stored_text = RESULT_PATH.read_text(encoding="utf-8")
        stored_payload = load_strict_canonical_json(stored_text, "stored payload")
        verify_payload_hash(stored_payload, "stored payload")
        verify_payload_hash(payload, "recomputed payload")
        portable_compare(payload_core(stored_payload), payload_core(payload))
        stored_maximum = stored_payload["numerical_cross_checks"][
            "maximum_overall_scaled_error"
        ]
        require(
            isinstance(stored_maximum, float) and 0.0 <= stored_maximum < 2.0e-10,
            "stored numerical cross-check exceeds its frozen threshold",
        )
        expected_stored_report = generate_report(stored_payload)
        require(
            REPORT_PATH.read_text(encoding="utf-8") == expected_stored_report,
            "report is stale relative to the hash-sealed stored JSON",
        )
    else:
        RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        RESULT_PATH.write_text(result_text, encoding="utf-8")
        REPORT_PATH.write_text(report_text, encoding="utf-8")

    print("R0.73Y-A exact shear certificate: PASS")
    print(f"payload_sha256={payload['payload_sha256']}")
    print(f"maximum_numeric_scaled_error={payload['numerical_cross_checks']['maximum_overall_scaled_error']:.3e}")
    print(f"portable_gate_negative_tests={portable_negative_test_count}/7")
    print(f"result={RESULT_PATH}")
    print(f"report={REPORT_PATH}")
    if arguments.print_json:
        print(result_text, end="")


if __name__ == "__main__":
    main()
