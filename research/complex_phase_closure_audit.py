#!/usr/bin/env python3
"""Exact closure audit for the complex-amplitude gap left in R0.14.

Let X and T denote the external and target fifth-order energies from
``two_amplitude_global_audit.py``.  R0.14 proved the sharp real-amplitude
minimum and a rational lower bound for arbitrary complex amplitudes.  This
script closes the remaining gap by covering the compactified parameter cube
with two exact certificates.

Outside a small rational box around the real minimizer, a rational Bernstein
subdivision proves X/T >= 45.739349.  Inside that box, the exact algebraic
minimizer alpha is used only through a Sturm isolating interval.  Convexity in
the radial variable and a positive transverse divided difference prove
X-lambda_* T >= 0, where lambda_* = X(alpha,0,0)/T(alpha,0,0).

All sign decisions use rational arithmetic.  Decimal values are emitted only
after the exact inequalities have been checked.  The result concerns the
finite fifth-order interaction model with the fixed R0.11 polarizations; it
does not control a Navier--Stokes remainder.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
from itertools import product
import json
import math

import sympy as sp

import two_amplitude_global_audit as amplitude


Rational = sp.Rational
Interval = tuple[Rational, Rational]
Index3 = tuple[int, int, int]
Bounds3 = tuple[Interval, Interval, Interval]

X_VAR = amplitude.X_VAR
Y_VAR = amplitude.Y_VAR
H_VAR = amplitude.H_VAR
Z_VAR = amplitude.Z_VAR
A_VAR = amplitude.A_VAR
S_VAR = amplitude.S_VAR
LAMBDA_VAR = sp.symbols("lambda", positive=True)

EXTERIOR_RATIONAL_BOUND = Rational(45_739_349, 1_000_000)

# The z interval is a union of three depth-14 dyadic cells.  The a interval
# is one depth-10 cell adjacent to a=1.  These choices leave a comfortable
# exact sign margin in the local certificate while keeping the exterior
# partition small.
LOCAL_Z_LOW = Rational(2_433, 16_384)
LOCAL_Z_HIGH = Rational(2_436, 16_384)
LOCAL_A_LOW = Rational(1_023, 1_024)
MAXIMUM_SUBDIVISION_DEPTH = 80


def exact_complex_polynomials() -> tuple[sp.Expr, sp.Expr, dict[str, object]]:
    """Rebuild X and T from the signed order-five interaction tree."""

    by_frequency, pole_count = amplitude.aggregate_signed_complex_limit()
    total_trigonometric = amplitude.trigonometric_energy(
        amplitude.complex_energy_monomials(by_frequency)
    )
    target_trigonometric = amplitude.trigonometric_energy(
        amplitude.complex_energy_monomials(
            by_frequency,
            {
                amplitude.tree.NEXT_A_POSITIVE,
                amplitude.tree.NEXT_A_NEGATIVE,
            },
        )
    )
    total = amplitude.invariant_polynomial(total_trigonometric)
    target = amplitude.invariant_polynomial(target_trigonometric)
    external = sp.expand(total - target)
    metadata = {
        "aggregatedFrequencyCount": len(by_frequency),
        "uncancelledLaurentPoleCount": pole_count,
        "externalDigest": amplitude.polynomial_digest(
            sp.Poly(external, X_VAR, Y_VAR, H_VAR, domain=sp.QQ)
        ),
        "targetDigest": amplitude.polynomial_digest(
            sp.Poly(target, X_VAR, Y_VAR, H_VAR, domain=sp.QQ)
        ),
    }
    del by_frequency
    del total_trigonometric
    del target_trigonometric
    gc.collect()
    return external, target, metadata


def algebraic_minimum_record(
    external: sp.Expr,
    target: sp.Expr,
) -> tuple[dict[str, object], Interval, Interval]:
    """Isolate the real symmetric minimizer and its exact ratio."""

    external_axis = sp.expand(external.subs({Y_VAR: 0, H_VAR: 0}))
    target_axis = sp.expand(target.subs({Y_VAR: 0, H_VAR: 0}))
    stationary = amplitude.primitive_integer_polynomial(
        X_VAR * sp.diff(external_axis, X_VAR) - 2 * external_axis,
        X_VAR,
    )
    roots = amplitude.positive_root_intervals(stationary, 90)
    if len(roots) != 1:
        raise AssertionError("The same-phase axis must have one positive root.")
    alpha_interval = roots[0]
    lambda_interval = amplitude.interval_divide(
        amplitude.polynomial_interval(
            sp.Poly(external_axis, X_VAR, domain=sp.QQ),
            {X_VAR: alpha_interval},
        ),
        amplitude.polynomial_interval(
            sp.Poly(target_axis, X_VAR, domain=sp.QQ),
            {X_VAR: alpha_interval},
        ),
    )
    one = (Rational(1), Rational(1))
    z_interval = amplitude.interval_divide(
        alpha_interval,
        amplitude.interval_add(one, alpha_interval),
    )
    if not (
        LOCAL_Z_LOW < z_interval[0]
        and z_interval[1] < LOCAL_Z_HIGH
    ):
        raise AssertionError("The algebraic minimizer is outside the local box.")
    if not lambda_interval[1] < EXTERIOR_RATIONAL_BOUND:
        raise AssertionError("The exterior rational bound must exceed lambda_*.")
    return (
        {
            "stationaryDegree": stationary.degree(),
            "stationaryPolynomialDigest": amplitude.polynomial_digest(stationary),
            "stationaryPolynomial": [
                {
                    "power": stationary.degree() - index,
                    "coefficient": str(coefficient),
                }
                for index, coefficient in enumerate(stationary.all_coeffs())
                if coefficient != 0
            ],
            "positiveRootCount": int(stationary.count_roots(0, sp.oo)),
            "alpha": amplitude.compact_interval_record(alpha_interval),
            "compactifiedAlpha": amplitude.compact_interval_record(z_interval),
            "lambdaStar": amplitude.compact_interval_record(lambda_interval),
            "exteriorBound": str(EXTERIOR_RATIONAL_BOUND),
            "exteriorBoundDecimal": float(EXTERIOR_RATIONAL_BOUND),
            "strictExteriorMarginLower": float(
                EXTERIOR_RATIONAL_BOUND - lambda_interval[1]
            ),
        },
        alpha_interval,
        lambda_interval,
    )


def target_positivity_record(target: sp.Expr) -> dict[str, object]:
    """Certify T>0 on the admissible domain away from the origin."""

    target_poly = sp.Poly(target, X_VAR, Y_VAR, H_VAR, domain=sp.QQ)
    h_coefficient = Rational(target_poly.coeff_monomial(H_VAR))
    quadratic = sp.Poly(target.subs(H_VAR, 0), X_VAR, Y_VAR, domain=sp.QQ)
    x_squared = Rational(quadratic.coeff_monomial(X_VAR**2))
    xy = Rational(quadratic.coeff_monomial(X_VAR * Y_VAR))
    y_squared = Rational(quadratic.coeff_monomial(Y_VAR**2))
    determinant = sp.factor(x_squared * y_squared - (xy / 2) ** 2)
    if h_coefficient <= 0 or x_squared <= 0 or determinant <= 0:
        raise AssertionError("The target energy was not certified positive.")
    return {
        "hCoefficient": str(h_coefficient),
        "quadraticLeadingCoefficient": str(x_squared),
        "quadraticMatrixDeterminant": str(determinant),
        "strictAwayFromOrigin": True,
    }


def local_box_bounds() -> tuple[Interval, Interval]:
    """Return a rectangular x,y enclosure of the compact local box."""

    radial_low = LOCAL_Z_LOW / (1 - LOCAL_Z_LOW)
    radial_high = LOCAL_Z_HIGH / (1 - LOCAL_Z_HIGH)
    x_interval = radial_low * LOCAL_A_LOW, radial_high
    y_interval = Rational(0), radial_high * (1 - LOCAL_A_LOW)
    return x_interval, y_interval


def local_bernstein_interval(
    polynomial: sp.Poly,
    x_interval: Interval,
    y_interval: Interval,
    lambda_interval: Interval,
) -> tuple[Interval, Index3, int]:
    """Bound a local polynomial by Bernstein coefficients.

    The input may depend on x, y, s and linearly on lambda.  The rational
    x,y box is mapped to the unit cube.  Evaluating both endpoints of the
    isolating lambda interval is exact because every resulting Bernstein
    coefficient is affine in lambda.
    """

    transformed = sp.expand(
        polynomial.as_expr().subs(
            {
                X_VAR: x_interval[0]
                + (x_interval[1] - x_interval[0]) * Z_VAR,
                Y_VAR: y_interval[0]
                + (y_interval[1] - y_interval[0]) * A_VAR,
            }
        )
    )
    endpoint_coefficients: list[Rational] = []
    degrees: Index3 | None = None
    coefficient_count = 0
    for endpoint in lambda_interval:
        endpoint_poly = sp.Poly(
            transformed.subs(LAMBDA_VAR, endpoint),
            Z_VAR,
            A_VAR,
            S_VAR,
            domain=sp.QQ,
        )
        endpoint_degrees: Index3 = (
            endpoint_poly.degree(Z_VAR),
            endpoint_poly.degree(A_VAR),
            endpoint_poly.degree(S_VAR),
        )
        if degrees is None:
            degrees = endpoint_degrees
        elif degrees != endpoint_degrees:
            raise AssertionError("Endpoint Bernstein degrees changed.")
        coefficients = amplitude.power_to_bernstein(
            endpoint_poly,
            endpoint_degrees,
        )
        endpoint_coefficients.extend(coefficients.values())
        coefficient_count += len(coefficients)
    if degrees is None:
        raise AssertionError("No local Bernstein coefficients were produced.")
    return (
        (min(endpoint_coefficients), max(endpoint_coefficients)),
        degrees,
        coefficient_count,
    )


def local_certificate(
    external: sp.Expr,
    target: sp.Expr,
    alpha_interval: Interval,
    lambda_interval: Interval,
) -> dict[str, object]:
    """Prove X-lambda_* T >= 0 inside the rational local box."""

    difference = sp.expand(external - LAMBDA_VAR * target)
    axial = sp.expand(difference.subs({Y_VAR: 0, H_VAR: 0}))
    axial_second = sp.Poly(
        sp.diff(axial, X_VAR, 2),
        X_VAR,
        LAMBDA_VAR,
        domain=sp.QQ,
    )

    transverse_expression = sp.cancel(
        (
            difference.subs(H_VAR, X_VAR * Y_VAR * S_VAR)
            - axial
        )
        / Y_VAR
    )
    transverse = sp.Poly(
        transverse_expression,
        X_VAR,
        Y_VAR,
        S_VAR,
        LAMBDA_VAR,
        domain=sp.QQ,
    )
    x_interval, y_interval = local_box_bounds()
    if not (
        x_interval[0] < alpha_interval[0]
        and alpha_interval[1] < x_interval[1]
    ):
        raise AssertionError("The radial local interval does not contain alpha.")
    second_interval = amplitude.polynomial_interval(
        axial_second,
        {X_VAR: x_interval, LAMBDA_VAR: lambda_interval},
    )
    (
        transverse_interval,
        transverse_degrees,
        transverse_coefficient_count,
    ) = local_bernstein_interval(
        transverse,
        x_interval,
        y_interval,
        lambda_interval,
    )
    if second_interval[0] <= 0:
        raise AssertionError(
            f"Axial convexity was not certified: {second_interval}."
        )
    if transverse_interval[0] <= 0:
        raise AssertionError(
            "The transverse divided difference was not certified: "
            f"{float(transverse_interval[0])}, "
            f"{float(transverse_interval[1])}."
        )

    return {
        "compactBox": {
            "z": [str(LOCAL_Z_LOW), str(LOCAL_Z_HIGH)],
            "a": [str(LOCAL_A_LOW), "1"],
            "s": ["0", "1"],
        },
        "rectangularEnclosure": {
            "x": amplitude.interval_record(x_interval),
            "y": amplitude.interval_record(y_interval),
        },
        "axialSecondDerivative": amplitude.interval_record(second_interval),
        "transverseDividedDifference": amplitude.interval_record(
            transverse_interval
        ),
        "transverseBernsteinDegrees": list(transverse_degrees),
        "transverseBernsteinCoefficientCount": transverse_coefficient_count,
        "logic": (
            "D(x,0,0) is convex with a double zero at alpha; "
            "D(x,y,x*y*s)-D(x,0,0)=y*J and J>0"
        ),
    }


def split_bounds(bounds: Bounds3, axis: int) -> tuple[Bounds3, Bounds3]:
    midpoint = (bounds[axis][0] + bounds[axis][1]) / 2
    left = list(bounds)
    right = list(bounds)
    left[axis] = bounds[axis][0], midpoint
    right[axis] = midpoint, bounds[axis][1]
    return tuple(left), tuple(right)  # type: ignore[return-value]


def bounds_record(bounds: Bounds3) -> dict[str, list[str]]:
    return {
        label: [str(interval[0]), str(interval[1])]
        for label, interval in zip("zas", bounds, strict=True)
    }


def inside_local_box(bounds: Bounds3) -> bool:
    z_bounds, a_bounds, _ = bounds
    return (
        z_bounds[0] >= LOCAL_Z_LOW
        and z_bounds[1] <= LOCAL_Z_HIGH
        and a_bounds[0] >= LOCAL_A_LOW
    )


def boundary_split_axis(bounds: Bounds3) -> int | None:
    """Prefer splits that align a box with the rational local boundary."""

    z_bounds, a_bounds, _ = bounds
    for boundary in (LOCAL_Z_LOW, LOCAL_Z_HIGH):
        if z_bounds[0] < boundary < z_bounds[1]:
            return 0
    if a_bounds[0] < LOCAL_A_LOW < a_bounds[1]:
        return 1
    return None


def exterior_certificate(
    external: sp.Expr,
    target: sp.Expr,
) -> dict[str, object]:
    """Prove the stronger rational bound outside the local box."""

    radial = Z_VAR / (1 - Z_VAR)
    substitutions = {
        X_VAR: radial * A_VAR,
        Y_VAR: radial * (1 - A_VAR),
        H_VAR: radial**2 * A_VAR * (1 - A_VAR) * S_VAR,
    }
    compact_expression = sp.cancel(
        (external - EXTERIOR_RATIONAL_BOUND * target).subs(substitutions)
        * (1 - Z_VAR) ** 6
    )
    compact = sp.Poly(
        compact_expression,
        Z_VAR,
        A_VAR,
        S_VAR,
        domain=sp.QQ,
    )
    degrees: Index3 = (
        compact.degree(Z_VAR),
        compact.degree(A_VAR),
        compact.degree(S_VAR),
    )
    if degrees != (6, 6, 3):
        raise AssertionError("Unexpected compact polynomial degrees.")
    initial = amplitude.power_to_bernstein(compact, degrees)
    unit_bounds: Bounds3 = (
        (Rational(0), Rational(1)),
        (Rational(0), Rational(1)),
        (Rational(0), Rational(1)),
    )
    stack: list[
        tuple[dict[Index3, Rational], Bounds3, int, str]
    ] = [(initial, unit_bounds, 0, "")]
    certified: list[tuple[str, Rational, Rational]] = []
    local: list[tuple[str, Bounds3]] = []
    maximum_depth = 0
    while stack:
        coefficients, bounds, depth, path = stack.pop()
        if inside_local_box(bounds):
            local.append((path, bounds))
            maximum_depth = max(maximum_depth, depth)
            continue
        minimum = min(coefficients.values())
        maximum = max(coefficients.values())
        if minimum >= 0:
            certified.append((path, minimum, maximum))
            maximum_depth = max(maximum_depth, depth)
            continue
        if depth >= MAXIMUM_SUBDIVISION_DEPTH:
            raise AssertionError(
                f"Exterior subdivision failed at {path} with bounds {bounds}."
            )
        axis = boundary_split_axis(bounds)
        if axis is None:
            variations = [
                amplitude.bernstein_variation(coefficients, degrees, index)
                for index in range(3)
            ]
            axis = max(range(3), key=lambda index: variations[index])
        left_coefficients, right_coefficients = amplitude.split_bernstein(
            coefficients,
            degrees,
            axis,
        )
        left_bounds, right_bounds = split_bounds(bounds, axis)
        label = "zas"[axis]
        stack.append(
            (
                right_coefficients,
                right_bounds,
                depth + 1,
                f"{path}{label}R",
            )
        )
        stack.append(
            (
                left_coefficients,
                left_bounds,
                depth + 1,
                f"{path}{label}L",
            )
        )

    payload_lines = [
        f"C:{path}:{minimum}:{maximum}"
        for path, minimum, maximum in sorted(certified)
    ]
    payload_lines.extend(
        f"L:{path}:{bounds}"
        for path, bounds in sorted(local)
    )
    return {
        "rationalBound": str(EXTERIOR_RATIONAL_BOUND),
        "compactifiedDegrees": list(degrees),
        "compactifiedTermCount": len(compact.terms()),
        "compactifiedDigest": amplitude.polynomial_digest(compact),
        "initialNegativeBernsteinCount": sum(
            1 for value in initial.values() if bool(value < 0)
        ),
        "certifiedExteriorLeafCount": len(certified),
        "delegatedLocalLeafCount": len(local),
        "delegatedLocalLeaves": [
            {"path": path, "bounds": bounds_record(bounds)}
            for path, bounds in sorted(local)
        ],
        "maximumSubdivisionDepth": maximum_depth,
        "allExteriorLeafCoefficientsNonnegative": True,
        "partitionDigest": hashlib.sha256(
            "\n".join(sorted(payload_lines)).encode("ascii")
        ).hexdigest(),
    }


def audit() -> dict[str, object]:
    external, target, expansion = exact_complex_polynomials()
    target_positivity = target_positivity_record(target)
    minimum, alpha_interval, lambda_interval = algebraic_minimum_record(
        external,
        target,
    )
    local = local_certificate(
        external,
        target,
        alpha_interval,
        lambda_interval,
    )
    exterior = exterior_certificate(external, target)
    lambda_midpoint = (lambda_interval[0] + lambda_interval[1]) / 2
    return {
        "scope": (
            "fifth-order cone relay with fixed R0.11 polarizations"
        ),
        "complexExpansion": expansion,
        "targetPositivity": target_positivity,
        "algebraicMinimum": minimum,
        "localCertificate": local,
        "exteriorBernsteinCertificate": exterior,
        "conclusion": {
            "globalMinimizer": (
                "h=0, y=0, x=alpha, modulo amplitude symmetries"
            ),
            "minimumExternalOverTargetDecimal": float(lambda_midpoint),
            "maximumTargetFractionDecimal": float(
                1 / (1 + lambda_midpoint)
            ),
            "complexGapClosed": True,
        },
    }


def validate(result: dict[str, object]) -> None:
    expansion = result["complexExpansion"]
    assert expansion["uncancelledLaurentPoleCount"] == 0
    assert expansion["externalDigest"] == (
        "2e4fd6886d4e5b642cc0e85527ac4b0d5bab29ea7911032f0cbfcb4211a69df3"
    )
    assert result["targetPositivity"]["strictAwayFromOrigin"]
    minimum = result["algebraicMinimum"]
    assert minimum["positiveRootCount"] == 1
    assert minimum["strictExteriorMarginLower"] > 0
    local = result["localCertificate"]
    assert local["axialSecondDerivative"]["lowerDecimal"] > 0
    assert local["transverseDividedDifference"]["lowerDecimal"] > 0
    exterior = result["exteriorBernsteinCertificate"]
    assert exterior["allExteriorLeafCoefficientsNonnegative"]
    assert exterior["certifiedExteriorLeafCount"] == 24
    assert exterior["delegatedLocalLeafCount"] == 1
    assert exterior["maximumSubdivisionDepth"] == 23
    conclusion = result["conclusion"]
    assert conclusion["complexGapClosed"]
    assert abs(
        conclusion["minimumExternalOverTargetDecimal"]
        - 45.73934896472748
    ) < 2e-12


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    result = audit()
    if arguments.check:
        validate(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
