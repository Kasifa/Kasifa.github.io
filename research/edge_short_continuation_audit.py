#!/usr/bin/env python3
"""R0.36 exact short-step continuation and recentering audit.

The R0.35 nonlinear map is not bounded on one fixed Wiener radius.  This
audit conjugates a local Taylor problem back to the origin and uses two
different radii.  It records:

1. the exact rational geometry of a short center on the negative
   fixed-charge axis;
2. the all-order outer-to-inner constant 121/48 for that geometry;
3. an all-order R0.31 majorant enclosure of the translated exact solution
   around its degree-40 polynomial;
4. an exact finite polynomial regression of the conjugated Euler fields,
   projector, nonlinear map, and residual;
5. an exact inverse of the degree-2-through-8 Jacobian block.

The existence enclosure is wholly inside the R0.31 polydisc.  The finite
Jacobian inverse is a regression, not an inverse for the infinite operator.
Nothing here reaches the R0.32 Pade candidate or proves a statement about
the full three-dimensional Navier--Stokes equation.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

import gmpy2

import edge_rational_asymptotic_audit as r028


Rational = gmpy2.mpq
Exponent = tuple[int, int]
Polynomial = dict[Exponent, Rational]

R031_CERTIFICATE = Path(
    "research/certificates/r031/edge-optimized-majorant.json"
)
R035_CERTIFICATE = Path(
    "research/certificates/r035/edge-continuation-geometry.json"
)
R031_EXPECTED_SHA256 = (
    "32676dcefdf3c5285bdb18aab44bfdba385a84910d5e1d0df00f8ea9039ec395"
)
R035_EXPECTED_SHA256 = (
    "13d147790926f3f3d04ea8f6d93574e1c992dd2b30dc6e12c777e68868a4fede"
)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.36 +{elapsed:8.2f}s] {stage}{suffix}",
            file=sys.stderr,
            flush=True,
        )
    if PROGRESS_LOG is not None:
        record = {
            "timestampUtc": datetime.now(timezone.utc).isoformat(),
            "elapsedSeconds": elapsed,
            "stage": stage,
            **details,
        }
        with PROGRESS_LOG.open("a", encoding="utf-8") as target:
            target.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            target.flush()
            os.fsync(target.fileno())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rational_digest(value: Rational) -> str:
    return hashlib.sha256(str(value).encode("ascii")).hexdigest()


def rational_decimal(value: Rational, digits: int = 20) -> str:
    context = gmpy2.get_context()
    old_precision = context.precision
    context.precision = 256
    try:
        return format(gmpy2.mpfr(value), f".{digits}g")
    finally:
        context.precision = old_precision


def rational_record(value: Rational, digits: int = 20) -> dict[str, object]:
    numerator = gmpy2.numer(value)
    denominator = gmpy2.denom(value)
    return {
        "exact": str(value),
        "decimal": rational_decimal(value, digits),
        "numeratorDigits": len(str(abs(numerator))),
        "denominatorDigits": len(str(denominator)),
        "sha256": rational_digest(value),
    }


def polynomial_digest(polynomial: Polynomial) -> str:
    digest = hashlib.sha256()
    for (z_degree, w_degree), value in sorted(polynomial.items()):
        digest.update(f"{z_degree},{w_degree}:{value}\n".encode("ascii"))
    return digest.hexdigest()


def matrix_digest(matrix: list[list[Rational]]) -> str:
    digest = hashlib.sha256()
    for row_index, row in enumerate(matrix):
        for column_index, value in enumerate(row):
            if value:
                digest.update(
                    f"{row_index},{column_index}:{value}\n".encode("ascii")
                )
    return digest.hexdigest()


def git_state(source_commit: str | None) -> dict[str, object]:
    commit = source_commit or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True
    ).strip()
    dirty = bool(
        subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=normal"],
            text=True,
        ).strip()
    )
    return {"commit": commit, "dirty": dirty if source_commit is None else False}


def clean(polynomial: Polynomial) -> Polynomial:
    return {exponent: value for exponent, value in polynomial.items() if value}


def add(*polynomials: Polynomial) -> Polynomial:
    output: Polynomial = {}
    for polynomial in polynomials:
        for exponent, value in polynomial.items():
            output[exponent] = output.get(exponent, Rational(0)) + value
    return clean(output)


def scale(polynomial: Polynomial, factor: Rational | int) -> Polynomial:
    factor = Rational(factor)
    return clean({exponent: factor * value for exponent, value in polynomial.items()})


def truncate(polynomial: Polynomial, maximum_degree: int) -> Polynomial:
    return {
        exponent: value
        for exponent, value in polynomial.items()
        if sum(exponent) <= maximum_degree and value
    }


def select_degrees(
    polynomial: Polynomial, minimum_degree: int, maximum_degree: int
) -> Polynomial:
    return {
        exponent: value
        for exponent, value in polynomial.items()
        if minimum_degree <= sum(exponent) <= maximum_degree and value
    }


def euler_x(polynomial: Polynomial) -> Polynomial:
    return clean(
        {
            exponent: value * exponent[0]
            for exponent, value in polynomial.items()
        }
    )


def euler_y(polynomial: Polynomial) -> Polynomial:
    return clean(
        {
            exponent: value * exponent[1]
            for exponent, value in polynomial.items()
        }
    )


def euler_l(polynomial: Polynomial) -> Polynomial:
    return clean(
        {
            exponent: value * sum(exponent)
            for exponent, value in polynomial.items()
        }
    )


def euler_q(polynomial: Polynomial) -> Polynomial:
    return clean(
        {
            exponent: value * (2 * exponent[1] - exponent[0])
            for exponent, value in polynomial.items()
        }
    )


def local_euler_x(polynomial: Polynomial, z_center: Rational) -> Polynomial:
    output = euler_x(polynomial)
    for (z_degree, w_degree), value in polynomial.items():
        if z_degree:
            exponent = (z_degree - 1, w_degree)
            output[exponent] = output.get(exponent, Rational(0)) + (
                z_center * z_degree * value
            )
    return clean(output)


def local_euler_y(polynomial: Polynomial, w_center: Rational) -> Polynomial:
    output = euler_y(polynomial)
    for (z_degree, w_degree), value in polynomial.items():
        if w_degree:
            exponent = (z_degree, w_degree - 1)
            output[exponent] = output.get(exponent, Rational(0)) + (
                w_center * w_degree * value
            )
    return clean(output)


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    output: Polynomial = {}
    for (left_z, left_w), left_value in left.items():
        for (right_z, right_w), right_value in right.items():
            exponent = (left_z + right_z, left_w + right_w)
            output[exponent] = output.get(exponent, Rational(0)) + (
                left_value * right_value
            )
    return clean(output)


def bracket(left: Polynomial, right: Polynomial) -> Polynomial:
    output: Polynomial = {}
    for (left_z, left_w), left_value in left.items():
        for (right_z, right_w), right_value in right.items():
            determinant = left_z * right_w - left_w * right_z
            if determinant:
                exponent = (left_z + right_z, left_w + right_w)
                output[exponent] = output.get(exponent, Rational(0)) + (
                    determinant * left_value * right_value
                )
    return clean(output)


def local_bracket(
    left: Polynomial,
    right: Polynomial,
    z_center: Rational,
    w_center: Rational,
) -> Polynomial:
    return add(
        multiply(
            local_euler_x(left, z_center),
            local_euler_y(right, w_center),
        ),
        scale(
            multiply(
                local_euler_y(left, w_center),
                local_euler_x(right, z_center),
            ),
            -1,
        ),
    )


def charge_project(polynomial: Polynomial, charge: int) -> Polynomial:
    return {
        exponent: value
        for exponent, value in polynomial.items()
        if 2 * exponent[1] - exponent[0] == charge and value
    }


def nonzero_charge(polynomial: Polynomial) -> Polynomial:
    return {
        exponent: value
        for exponent, value in polynomial.items()
        if 2 * exponent[1] - exponent[0] != 0 and value
    }


def inverse_q(polynomial: Polynomial) -> Polynomial:
    output: Polynomial = {}
    for exponent, value in polynomial.items():
        charge = 2 * exponent[1] - exponent[0]
        if charge == 0:
            raise AssertionError("Q inverse received a charge-zero coefficient")
        output[exponent] = value / charge
    return clean(output)


def inverse_l(polynomial: Polynomial) -> Polynomial:
    output: Polynomial = {}
    for exponent, value in polynomial.items():
        degree = sum(exponent)
        if degree == 0:
            raise AssertionError("L inverse received a constant coefficient")
        output[exponent] = value / degree
    return clean(output)


def inverse_l_minus_one(polynomial: Polynomial) -> Polynomial:
    output: Polynomial = {}
    for exponent, value in polynomial.items():
        degree = sum(exponent)
        if degree == 1:
            raise AssertionError("(L-1) inverse received a degree-one coefficient")
        output[exponent] = value / (degree - 1)
    return clean(output)


def phi(polynomial: Polynomial) -> Polynomial:
    charge_part = inverse_q(nonzero_charge(bracket(polynomial, euler_q(polynomial))))
    zero_part = inverse_l(charge_project(bracket(polynomial, euler_l(polynomial)), 0))
    return inverse_l_minus_one(add(charge_part, zero_part))


def dphi(base: Polynomial, perturbation: Polynomial) -> Polynomial:
    charge_cross = add(
        bracket(perturbation, euler_q(base)),
        bracket(base, euler_q(perturbation)),
    )
    zero_cross = add(
        bracket(perturbation, euler_l(base)),
        bracket(base, euler_l(perturbation)),
    )
    return inverse_l_minus_one(
        add(
            inverse_q(nonzero_charge(charge_cross)),
            inverse_l(charge_project(zero_cross, 0)),
        )
    )


def translate(
    polynomial: Polynomial, z_center: Rational, w_center: Rational
) -> Polynomial:
    """Return f(z_center+zeta,w_center+omega) exactly."""

    output: Polynomial = {}
    for (z_degree, w_degree), value in polynomial.items():
        for local_z in range(z_degree + 1):
            z_factor = (
                math.comb(z_degree, local_z)
                * z_center ** (z_degree - local_z)
            )
            for local_w in range(w_degree + 1):
                exponent = (local_z, local_w)
                factor = (
                    z_factor
                    * math.comb(w_degree, local_w)
                    * w_center ** (w_degree - local_w)
                )
                output[exponent] = output.get(exponent, Rational(0)) + (
                    value * factor
                )
    return clean(output)


def local_projector(
    polynomial: Polynomial,
    charge: int,
    z_center: Rational,
    w_center: Rational,
) -> Polynomial:
    origin = translate(polynomial, -z_center, -w_center)
    return translate(charge_project(origin, charge), z_center, w_center)


def local_phi(
    polynomial: Polynomial, z_center: Rational, w_center: Rational
) -> Polynomial:
    origin = translate(polynomial, -z_center, -w_center)
    return translate(phi(origin), z_center, w_center)


def wiener_norm(
    polynomial: Polynomial, z_radius: Rational, w_radius: Rational
) -> Rational:
    return sum(
        (
            abs(value) * z_radius**exponent[0] * w_radius**exponent[1]
            for exponent, value in polynomial.items()
        ),
        Rational(0),
    )


def field_to_polynomial(
    field: list[list[Rational] | None], maximum_degree: int
) -> Polynomial:
    output: Polynomial = {}
    for degree in range(1, maximum_degree + 1):
        layer = field[degree]
        if layer is None:
            raise AssertionError("missing recurrence layer")
        for w_degree, value in enumerate(layer):
            if value:
                output[(degree - w_degree, w_degree)] = value
    return output


def majorant_tail(x: Rational, maximum_degree: int) -> Rational:
    """All-order tail from A_L <= 2 K^(L-1)/L^3."""

    majorant_constant = Rational(81, 4)
    return (
        Rational(2)
        / majorant_constant
        * x ** (maximum_degree + 1)
        / (maximum_degree + 1) ** 3
        / (1 - x)
    )


def exact_matrix_product(
    left: list[list[Rational]], right: list[list[Rational]]
) -> list[list[Rational]]:
    dimension = len(left)
    output = [
        [Rational(0) for _ in range(dimension)] for _ in range(dimension)
    ]
    for row in range(dimension):
        for middle in range(dimension):
            if left[row][middle] == 0:
                continue
            for column in range(dimension):
                if right[middle][column]:
                    output[row][column] += (
                        left[row][middle] * right[middle][column]
                    )
    return output


def is_identity(matrix: list[list[Rational]]) -> bool:
    return all(
        value == (1 if row == column else 0)
        for row, values in enumerate(matrix)
        for column, value in enumerate(values)
    )


def finite_jacobian_inverse(
    active: Polynomial, maximum_degree: int
) -> dict[str, object]:
    basis = [
        (degree - w_degree, w_degree)
        for degree in range(2, maximum_degree + 1)
        for w_degree in range(degree + 1)
    ]
    index = {exponent: position for position, exponent in enumerate(basis)}
    dimension = len(basis)
    jacobian = [
        [Rational(0) for _ in range(dimension)] for _ in range(dimension)
    ]

    for column, exponent in enumerate(basis):
        perturbation = {exponent: Rational(1)}
        image = select_degrees(
            add(perturbation, scale(dphi(active, perturbation), -1)),
            2,
            maximum_degree,
        )
        for output_exponent, value in image.items():
            jacobian[index[output_exponent]][column] = value

    diagonal_is_one = all(
        jacobian[position][position] == 1 for position in range(dimension)
    )
    strictly_lower = all(
        jacobian[row][column] == 0
        for row in range(dimension)
        for column in range(row + 1, dimension)
    )
    if not diagonal_is_one or not strictly_lower:
        raise AssertionError("finite Jacobian is not unit lower triangular")

    inverse = [
        [Rational(0) for _ in range(dimension)] for _ in range(dimension)
    ]
    for column in range(dimension):
        for row in range(dimension):
            right_hand_side = Rational(1 if row == column else 0)
            correction = sum(
                (
                    jacobian[row][previous] * inverse[previous][column]
                    for previous in range(row)
                ),
                Rational(0),
            )
            inverse[row][column] = right_hand_side - correction

    left_identity = is_identity(exact_matrix_product(inverse, jacobian))
    right_identity = is_identity(exact_matrix_product(jacobian, inverse))
    if not left_identity or not right_identity:
        raise AssertionError("finite Jacobian inverse regression failed")

    inverse_column_norms = [
        sum((abs(inverse[row][column]) for row in range(dimension)), Rational(0))
        for column in range(dimension)
    ]
    maximum_inverse_column_norm = max(inverse_column_norms)

    rho = Rational(4, 81)
    delta = rho / 7
    z_center = delta
    w_center = -delta
    conjugated_checks = 0
    for exponent in basis:
        local_basis = translate({exponent: Rational(1)}, z_center, w_center)
        returned_origin = translate(local_basis, -z_center, -w_center)
        if returned_origin != {exponent: Rational(1)}:
            raise AssertionError("translated structural basis is not invertible")
        conjugated_checks += 1

    nonzero_jacobian = sum(value != 0 for row in jacobian for value in row)
    nonzero_inverse = sum(value != 0 for row in inverse for value in row)
    return {
        "maximumTotalDegree": maximum_degree,
        "structuralSubspace": (
            "origin perturbations of total degrees 2 through M, conjugated "
            "to the local center by exact polynomial translation"
        ),
        "dimension": dimension,
        "jacobianUnitLowerTriangular": diagonal_is_one and strictly_lower,
        "jacobianNonzeroEntries": nonzero_jacobian,
        "inverseNonzeroEntries": nonzero_inverse,
        "leftInverseExact": left_identity,
        "rightInverseExact": right_identity,
        "conjugatedBasisChecks": conjugated_checks,
        "jacobianSha256": matrix_digest(jacobian),
        "inverseSha256": matrix_digest(inverse),
        "maximumUnweightedColumnL1Norm": rational_record(
            maximum_inverse_column_norm
        ),
        "classification": (
            "finite exact inverse regression only; no infinite-dimensional "
            "inverse or Newton ball is certified"
        ),
    }


def build_payload(
    maximum_degree: int,
    jacobian_degree: int,
    show_progress: bool,
    source_commit: str | None,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "loading pinned R0.31 and R0.35 certificates")
    if sha256(R031_CERTIFICATE) != R031_EXPECTED_SHA256:
        raise AssertionError("R0.31 certificate hash mismatch")
    if sha256(R035_CERTIFICATE) != R035_EXPECTED_SHA256:
        raise AssertionError("R0.35 certificate hash mismatch")
    r031 = json.loads(R031_CERTIFICATE.read_text(encoding="utf-8"))
    r035 = json.loads(R035_CERTIFICATE.read_text(encoding="utf-8"))

    rho = Rational(4, 81)
    delta = rho / 7
    inner_radius = delta
    outer_radius = 5 * delta
    global_inner = delta + inner_radius
    global_outer = outer_radius - delta
    containing_origin_radius = delta + outer_radius
    orbit_radius = inner_radius + 2 * delta
    radius_ratio = global_inner / global_outer
    if radius_ratio != Rational(1, 2):
        raise AssertionError("chosen short step does not realize the half-radius bound")
    if not orbit_radius < outer_radius:
        raise AssertionError("affine charge orbit does not fit in the outer local disc")
    if not containing_origin_radius < rho:
        raise AssertionError("outer local disc leaves the R0.31 polydisc")

    progress(
        show_progress,
        started,
        "constructing exact active recurrence",
        maximumDegree=maximum_degree,
    )
    active_field, _, _, recurrence_interactions = r028.rational_edge_recurrence(
        maximum_degree,
        False,
        started,
    )
    active = field_to_polynomial(active_field, maximum_degree)
    seed = {(1, 0): Rational(1), (0, 1): Rational(1)}

    progress(show_progress, started, "checking origin and conjugated polynomial equations")
    origin_residual = add(active, scale(seed, -1), scale(phi(active), -1))
    low_origin_residual = truncate(origin_residual, maximum_degree)
    if low_origin_residual:
        raise AssertionError("degree-truncated recurrence has a low-degree residual")

    z_center = delta
    w_center = -delta
    local_active = translate(active, z_center, w_center)
    recovered_active = translate(local_active, -z_center, -w_center)
    if recovered_active != active:
        raise AssertionError("exact translation inversion failed")
    local_seed = translate(seed, z_center, w_center)
    local_residual = add(
        local_active,
        scale(local_seed, -1),
        scale(local_phi(local_active, z_center, w_center), -1),
    )
    translated_origin_residual = translate(origin_residual, z_center, w_center)
    if local_residual != translated_origin_residual:
        raise AssertionError("conjugated nonlinear residual mismatch")

    local_x = local_euler_x(local_active, z_center)
    local_y = local_euler_y(local_active, w_center)
    if local_x != translate(euler_x(active), z_center, w_center):
        raise AssertionError("conjugated X field mismatch")
    if local_y != translate(euler_y(active), z_center, w_center):
        raise AssertionError("conjugated Y field mismatch")
    bracket_check = local_bracket(
        local_active, local_active, z_center, w_center
    )
    if bracket_check != translate(bracket(active, active), z_center, w_center):
        raise AssertionError("conjugated bracket mismatch")

    projector_checks = []
    for charge in (-1, 0, 1, 2, 3):
        projected = local_projector(local_active, charge, z_center, w_center)
        expected = translate(charge_project(active, charge), z_center, w_center)
        if projected != expected:
            raise AssertionError("conjugated projector mismatch")
        projector_checks.append(
            {
                "charge": charge,
                "nonzeroLocalCoefficients": len(projected),
                "sha256": polynomial_digest(projected),
            }
        )

    progress(show_progress, started, "forming all-order inclusion and residual bounds")
    x_outer = Rational(6, 7)
    x_inner = Rational(2, 7)
    outer_tail = majorant_tail(x_outer, maximum_degree)
    inner_tail = majorant_tail(x_inner, maximum_degree)
    solution_outer_bound = Rational(16, 27)
    operator_constant = Rational(121, 48)
    residual_bound = inner_tail + operator_constant * (
        2 * solution_outer_bound + outer_tail
    ) * outer_tail
    exact_local_residual_norm = wiener_norm(
        local_residual, inner_radius, inner_radius
    )
    if exact_local_residual_norm > residual_bound:
        raise AssertionError("exact finite residual exceeds the all-order bound")

    exact_local_outer_norm = wiener_norm(
        local_active, outer_radius, outer_radius
    )
    exact_local_inner_norm = wiener_norm(
        local_active, inner_radius, inner_radius
    )
    if exact_local_outer_norm > solution_outer_bound + outer_tail:
        raise AssertionError("translated polynomial exceeds the all-order norm enclosure")

    progress(
        show_progress,
        started,
        "constructing exact finite Jacobian inverse",
        maximumDegree=jacobian_degree,
    )
    jacobian = finite_jacobian_inverse(active, jacobian_degree)

    checks = {
        "pinnedInputHashes": True,
        "outerLocalDiscInsideR031": containing_origin_radius < rho,
        "innerAffineChargeOrbitInsideOuterDisc": orbit_radius < outer_radius,
        "conjugatedRadiusRatioIsOneHalf": radius_ratio == Rational(1, 2),
        "originRecurrenceThroughCutoff": not low_origin_residual,
        "translationInverseExact": recovered_active == active,
        "conjugatedEulerFieldsExact": True,
        "conjugatedBracketExact": True,
        "conjugatedProjectorsExact": len(projector_checks) == 5,
        "conjugatedNonlinearResidualExact": (
            local_residual == translated_origin_residual
        ),
        "finiteResidualWithinAllOrderBound": (
            exact_local_residual_norm <= residual_bound
        ),
        "finiteJacobianInverseExact": (
            jacobian["leftInverseExact"] and jacobian["rightInverseExact"]
        ),
    }
    if not all(checks.values()):
        raise AssertionError("one or more R0.36 checks failed")

    fixed_charge_center = z_center**2 * w_center
    fixed_charge_radius = rho**3
    payload = {
        "scope": {
            "result": (
                "all-order conjugated outer-to-inner operator theorem and "
                "an in-domain exact short-step recentering certificate"
            ),
            "classification": (
                "all-order functional-analytic theorem, all-order majorant "
                "inclusion, and finite exact polynomial/Jacobian regressions"
            ),
            "limitations": [
                "the short step remains wholly inside the R0.31 polydisc",
                "the finite Jacobian block is not an inverse for the infinite operator",
                "no Newton or radii-polynomial ball outside R0.31 is certified",
                "the R0.32 Pade candidate is not reached or upgraded to a singularity",
                "the result concerns a reduced edge generating equation rather than the full PDE",
                "no Navier-Stokes regularity or blow-up conclusion is claimed",
            ],
        },
        "input": {
            "r031": {
                "path": str(R031_CERTIFICATE),
                "sha256": R031_EXPECTED_SHA256,
                "sourceCommit": r031["git"]["commit"],
                "commonPolydiscRadius": r031["formalTheorem"][
                    "commonAnalyticDomain"
                ],
            },
            "r035": {
                "path": str(R035_CERTIFICATE),
                "sha256": R035_EXPECTED_SHA256,
                "sourceCommit": r035["git"]["commit"],
                "halfRadiusConstant": r035["operatorScale"][
                    "halfRadiusBilinearBound"
                ]["total"],
            },
        },
        "allOrderTheorem": {
            "translationNorm": (
                "||tau_c f||_r <= ||f||_(|c|+r), componentwise"
            ),
            "inverseTranslationNorm": (
                "||tau_c^(-1) g||_S <= ||g||_(|c|+S), componentwise"
            ),
            "generalConjugatedBound": (
                "if S=R-|c|, s=r+|c| and lambda=max_i(s_i/S_i)<1, "
                "then ||Phi_c(g)||_r <= C(lambda)||g||_R^2"
            ),
            "generalConstant": (
                "C(lambda)=(11/3) M1(lambda)"
                "*(M2(lambda)+M1(lambda)^2), "
                "Mj(lambda)=sup_(n>=0) n^j lambda^n"
            ),
            "generalLipschitzBound": (
                "||Phi_c(f)-Phi_c(g)||_r <= C(lambda)"
                "*(||f||_R+||g||_R)||f-g||_R"
            ),
            "chosenStepConstant": "C(1/2)=121/48",
            "proofMethod": (
                "binomial translation inequalities, conjugacy "
                "Phi_c=tau_c Phi tau_c^(-1), and the origin two-radius estimate"
            ),
        },
        "shortStep": {
            "r031Radius": rational_record(rho),
            "center": {
                "Z": rational_record(z_center),
                "W": rational_record(w_center),
                "fixedChargeR": rational_record(fixed_charge_center),
                "fractionOfR031FixedChargeRadius": rational_record(
                    abs(fixed_charge_center) / fixed_charge_radius
                ),
                "direction": "negative real fixed-charge axis",
            },
            "localRadii": {
                "inner": rational_record(inner_radius),
                "outer": rational_record(outer_radius),
                "outerDiscOriginExtent": rational_record(
                    containing_origin_radius
                ),
                "innerAffineOrbitExtent": rational_record(orbit_radius),
                "originInnerAfterConjugacy": rational_record(global_inner),
                "originOuterAfterConjugacy": rational_record(global_outer),
                "ratio": rational_record(radius_ratio),
            },
            "strictMargins": {
                "r031Containment": rational_record(
                    rho - containing_origin_radius
                ),
                "affineOrbitContainment": rational_record(
                    outer_radius - orbit_radius
                ),
            },
        },
        "inclusionCertificate": {
            "polynomialCutoff": maximum_degree,
            "centeredPolynomialSha256": polynomial_digest(local_active),
            "centeredPolynomialNonzeroCoefficients": len(local_active),
            "majorantFormula": (
                "E_N(x)=(2/K)*x^(N+1)/((N+1)^3*(1-x)), K=81/4"
            ),
            "outerMajorantVariable": rational_record(x_outer),
            "innerMajorantVariable": rational_record(x_inner),
            "solutionOuterNormBound": rational_record(solution_outer_bound),
            "outerTailBound": rational_record(outer_tail),
            "innerInclusionRadius": rational_record(inner_tail),
            "statement": (
                "the R0.31 exact solution translated to the short-step center "
                "lies in the inner-radius Wiener ball of radius E_N(2/7) "
                "around the exact translated degree-N polynomial"
            ),
            "exactPolynomialOuterNorm": rational_record(exact_local_outer_norm),
            "exactPolynomialInnerNorm": rational_record(exact_local_inner_norm),
            "exactConjugatedResidualNorm": rational_record(
                exact_local_residual_norm
            ),
            "allOrderResidualUpperBound": rational_record(residual_bound),
            "residualBoundFormula": (
                "E_N(2/7)+(121/48)*(2*(16/27)+E_N(6/7))*E_N(6/7)"
            ),
        },
        "finiteRegression": {
            "recurrenceMaximumDegree": maximum_degree,
            "recurrenceOrderedInteractions": recurrence_interactions,
            "originActiveSha256": polynomial_digest(active),
            "originResidualSha256": polynomial_digest(origin_residual),
            "localResidualSha256": polynomial_digest(local_residual),
            "projectorChecks": projector_checks,
            "jacobian": jacobian,
        },
        "checks": checks,
        "computation": {
            "backend": r028.base.RATIONAL_BACKEND,
            "randomSeed": None,
            "wallSeconds": time.perf_counter() - started,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "gmpy2": gmpy2.version(),
            "gmp": gmpy2.mp_version(),
        },
        "git": git_state(source_commit),
    }
    progress(
        show_progress,
        started,
        "completed R0.36 short-step certificate",
        checks=len(checks),
        passed=True,
    )
    return payload


def atomic_json_write(path: Path, payload: dict[str, object], pretty: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + f".tmp-{os.getpid()}")
    with temporary.open("w", encoding="utf-8") as target:
        json.dump(
            payload,
            target,
            ensure_ascii=False,
            indent=2 if pretty else None,
            sort_keys=True,
        )
        target.write("\n")
        target.flush()
        os.fsync(target.fileno())
    os.replace(temporary, path)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-total-degree", type=int, default=40)
    parser.add_argument("--jacobian-degree", type=int, default=8)
    parser.add_argument("--source-commit")
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--progress-log",
        type=Path,
        help="append-only NDJSON progress record; must not already exist",
    )
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> None:
    global PROGRESS_LOG
    arguments = parse_arguments()
    if arguments.max_total_degree < 8:
        raise SystemExit("--max-total-degree must be at least 8")
    if not 3 <= arguments.jacobian_degree <= arguments.max_total_degree:
        raise SystemExit("--jacobian-degree must lie between 3 and the recurrence cutoff")
    if arguments.progress_log is not None:
        if arguments.progress_log.exists():
            raise SystemExit("--progress-log already exists; choose a new path")
        arguments.progress_log.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG = arguments.progress_log
    payload = build_payload(
        arguments.max_total_degree,
        arguments.jacobian_degree,
        arguments.progress,
        arguments.source_commit,
    )
    if arguments.check and not all(payload["checks"].values()):
        raise AssertionError("R0.36 certificate checks failed")
    if arguments.output is not None:
        atomic_json_write(arguments.output, payload, arguments.pretty)
    else:
        json.dump(
            payload,
            sys.stdout,
            ensure_ascii=False,
            indent=2 if arguments.pretty else None,
            sort_keys=True,
        )
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
