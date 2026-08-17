#!/usr/bin/env python3
"""Polish and locally certify finite-face stationary candidates for R0.20.

For every numerical candidate this script applies arbitrary-precision Newton
iteration followed by an exact rational two-dimensional Krawczyk inclusion.
It also bounds the face target fraction and certifies the Hessian inertia at
the unique root.  The result is local: whole-face completeness still depends
on resultant pairing or an interval exclusion of the remaining domain.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from fractions import Fraction
import gzip
import json
from pathlib import Path
import sys
import time

import mpmath as mp
import numpy as np


Rational = Fraction
Term = tuple[tuple[int, int], Rational]


def emit(stage: str, started: float, **fields: object) -> None:
    print(
        json.dumps(
            {
                "timestampUtc": datetime.now(timezone.utc).isoformat(),
                "elapsedSeconds": round(time.perf_counter() - started, 3),
                "stage": stage,
                **fields,
            },
            separators=(",", ":"),
        ),
        file=sys.stderr,
        flush=True,
    )


def load_gzip(path: Path) -> dict[str, object]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        return json.load(stream)


def parse(rows: list[list[object]]) -> list[Term]:
    return [
        ((int(row[0]), int(row[1])), Rational(int(row[2]), int(row[3])))
        for row in rows
    ]


def derivative(terms: list[Term], axis: int) -> list[Term]:
    result = []
    for powers, coefficient in terms:
        if powers[axis]:
            reduced = list(powers)
            reduced[axis] -= 1
            result.append((tuple(reduced), coefficient * powers[axis]))
    return result


def combine(left: list[Term], right: list[Term], right_sign: int = 1) -> list[Term]:
    values: dict[tuple[int, int], Rational] = {}
    for powers, coefficient in left:
        values[powers] = values.get(powers, Rational(0)) + coefficient
    for powers, coefficient in right:
        values[powers] = values.get(powers, Rational(0)) + right_sign * coefficient
    return [(powers, coefficient) for powers, coefficient in values.items() if coefficient]


def multiply(left: list[Term], right: list[Term]) -> list[Term]:
    values: dict[tuple[int, int], Rational] = {}
    for left_powers, left_coefficient in left:
        for right_powers, right_coefficient in right:
            powers = (left_powers[0] + right_powers[0], left_powers[1] + right_powers[1])
            values[powers] = values.get(powers, Rational(0)) + left_coefficient * right_coefficient
    return [(powers, coefficient) for powers, coefficient in values.items() if coefficient]


def rational_value(terms: list[Term], point: tuple[Rational, Rational]) -> Rational:
    degrees = tuple(max((powers[axis] for powers, _ in terms), default=0) for axis in range(2))
    powers = [[Rational(1)] * (degree + 1) for degree in degrees]
    for axis in range(2):
        for exponent in range(1, degrees[axis] + 1):
            powers[axis][exponent] = powers[axis][exponent - 1] * point[axis]
    return sum(
        (coefficient * powers[0][monomial[0]] * powers[1][monomial[1]] for monomial, coefficient in terms),
        start=Rational(0),
    )


def mp_value(terms: list[Term], point: tuple[mp.mpf, mp.mpf]) -> mp.mpf:
    degrees = tuple(max((powers[axis] for powers, _ in terms), default=0) for axis in range(2))
    powers = [[mp.mpf(1)] * (degree + 1) for degree in degrees]
    for axis in range(2):
        for exponent in range(1, degrees[axis] + 1):
            powers[axis][exponent] = powers[axis][exponent - 1] * point[axis]
    return mp.fsum(
        mp.mpf(coefficient.numerator) / coefficient.denominator
        * powers[0][monomial[0]] * powers[1][monomial[1]]
        for monomial, coefficient in terms
    )


def absolute_bound(terms: list[Term], upper: tuple[Rational, Rational]) -> Rational:
    return rational_value(
        [(powers, abs(coefficient)) for powers, coefficient in terms],
        upper,
    )


def invert2(matrix: list[list[Rational]]) -> list[list[Rational]]:
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if determinant == 0:
        raise ArithmeticError("singular center Jacobian")
    return [
        [matrix[1][1] / determinant, -matrix[0][1] / determinant],
        [-matrix[1][0] / determinant, matrix[0][0] / determinant],
    ]


def decimal_string(value: Rational, precision: int = 65) -> str:
    with localcontext() as context:
        context.prec = precision
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def polish(functions: list[list[Term]], initial: list[float], digits: int) -> tuple[tuple[mp.mpf, mp.mpf], int]:
    mp.mp.dps = digits
    jacobian = [[derivative(function, axis) for axis in range(2)] for function in functions]
    point = mp.matrix([mp.mpf(str(value)) for value in initial])
    tolerance = mp.power(10, -(digits - 18))
    for iteration in range(1, 31):
        point_tuple = (point[0], point[1])
        values = mp.matrix([mp_value(function, point_tuple) for function in functions])
        matrix = mp.matrix([[mp_value(jacobian[row][column], point_tuple) for column in range(2)] for row in range(2)])
        delta = mp.lu_solve(matrix, values)
        point -= delta
        if max(abs(delta[0]), abs(delta[1])) < tolerance:
            return (point[0], point[1]), iteration
    raise ArithmeticError("high-precision Newton iteration did not converge")


def krawczyk(functions: list[list[Term]], center: tuple[Rational, Rational], radius: Rational) -> dict[str, object]:
    jacobian = [[derivative(function, axis) for axis in range(2)] for function in functions]
    upper = tuple(abs(value) + radius for value in center)
    values = [rational_value(function, center) for function in functions]
    center_jacobian = [[rational_value(jacobian[row][column], center) for column in range(2)] for row in range(2)]
    inverse = invert2(center_jacobian)
    variation = [
        [
            sum(
                (absolute_bound(derivative(jacobian[row][column], axis), upper) * radius for axis in range(2)),
                start=Rational(0),
            )
            for column in range(2)
        ]
        for row in range(2)
    ]
    contraction = [
        [sum((abs(inverse[row][inner]) * variation[inner][column] for inner in range(2)), start=Rational(0)) for column in range(2)]
        for row in range(2)
    ]
    shift = [
        -sum((inverse[row][column] * values[column] for column in range(2)), start=Rational(0))
        for row in range(2)
    ]
    ratios = [
        (abs(shift[row]) + sum(contraction[row], start=Rational(0)) * radius) / radius
        for row in range(2)
    ]
    row_sums = [sum(row, start=Rational(0)) for row in contraction]
    return {
        "method": "exact rational Krawczyk bound",
        "radius": str(radius),
        "boxDecimal": [[decimal_string(value - radius), decimal_string(value + radius)] for value in center],
        "strictInteriorInclusion": all(value < 1 for value in ratios),
        "contractionCertified": all(value < 1 for value in row_sums),
        "inclusionRatios": [float(value) for value in ratios],
        "contractionRowSums": [float(value) for value in row_sums],
    }


def interval_value(terms: list[Term], center: tuple[Rational, Rational], radius: Rational) -> tuple[Rational, Rational]:
    value = rational_value(terms, center)
    upper = tuple(abs(entry) + radius for entry in center)
    variation = sum(
        (absolute_bound(derivative(terms, axis), upper) * radius for axis in range(2)),
        start=Rational(0),
    )
    return value - variation, value + variation


def multiply_intervals(left: tuple[Rational, Rational], right: tuple[Rational, Rational]) -> tuple[Rational, Rational]:
    values = [left[a] * right[b] for a in range(2) for b in range(2)]
    return min(values), max(values)


def objective_certificate(
    target: list[Term],
    total: list[Term],
    center: tuple[Rational, Rational],
    radius: Rational,
) -> dict[str, object]:
    target_interval = interval_value(target, center, radius)
    total_interval = interval_value(total, center, radius)
    if target_interval[0] <= 0 or total_interval[0] <= 0:
        raise AssertionError("target or total energy crossed zero")
    fraction_interval = (
        target_interval[0] / total_interval[1],
        target_interval[1] / total_interval[0],
    )
    stationary = [
        combine(
            multiply(derivative(target, axis), total),
            multiply(target, derivative(total, axis)),
            -1,
        )
        for axis in range(2)
    ]
    jacobian = [[derivative(stationary[row], column) for column in range(2)] for row in range(2)]
    denominator = (total_interval[0] ** 2, total_interval[1] ** 2)
    entry_intervals: list[list[tuple[Rational, Rational]]] = []
    centers: list[list[Rational]] = []
    for row in range(2):
        interval_row = []
        center_row = []
        for column in range(2):
            numerator = interval_value(jacobian[row][column], center, radius)
            values = [numerator[a] / denominator[b] for a in range(2) for b in range(2)]
            interval_row.append((min(values), max(values)))
            center_row.append(rational_value(jacobian[row][column], center) / rational_value(total, center) ** 2)
        entry_intervals.append(interval_row)
        centers.append(center_row)
    symmetric_center = [[Rational(0)] * 2 for _ in range(2)]
    errors = [[Rational(0)] * 2 for _ in range(2)]
    for row in range(2):
        for column in range(row, 2):
            central = Rational(1, 2) * (centers[row][column] + centers[column][row])
            low = min(entry_intervals[row][column][0], entry_intervals[column][row][0])
            high = max(entry_intervals[row][column][1], entry_intervals[column][row][1])
            error = max(central - low, high - central)
            symmetric_center[row][column] = symmetric_center[column][row] = central
            errors[row][column] = errors[column][row] = error
    a = (symmetric_center[0][0] - errors[0][0], symmetric_center[0][0] + errors[0][0])
    b = (symmetric_center[0][1] - errors[0][1], symmetric_center[0][1] + errors[0][1])
    d = (symmetric_center[1][1] - errors[1][1], symmetric_center[1][1] + errors[1][1])
    ad = multiply_intervals(a, d)
    bb = multiply_intervals(b, b)
    determinant = (ad[0] - bb[1], ad[1] - bb[0])
    positive = a[0] > 0 and determinant[0] > 0
    negative = a[1] < 0 and determinant[0] > 0
    indefinite = determinant[1] < 0
    classification = "strict local maximum" if negative else "strict local minimum" if positive else "nondegenerate saddle" if indefinite else "unresolved"
    eigenvalues = np.linalg.eigvalsh(np.array([[float(value) for value in row] for row in symmetric_center]))
    return {
        "targetFractionInterval": {
            "lower": decimal_string(fraction_interval[0]),
            "upper": decimal_string(fraction_interval[1]),
        },
        "targetFractionPercentAtCenter": float(100 * rational_value(target, center) / rational_value(total, center)),
        "hessianClassification": classification,
        "positiveDefiniteCertified": positive,
        "negativeDefiniteCertified": negative,
        "indefiniteCertified": indefinite,
        "hessianEigenvaluesAtCenter": [float(value) for value in eigenvalues],
        "hessianDeterminantInterval": [float(value) for value in determinant],
        "entryErrorUpperBounds": [[float(value) for value in row] for row in errors],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--digits", type=int, default=90)
    parser.add_argument("--center-digits", type=int, default=55)
    parser.add_argument("--radius-exponent", type=int, default=40)
    arguments = parser.parse_args()
    started = time.perf_counter()
    cache = load_gzip(arguments.cache)
    scans = json.loads(arguments.candidates.read_text(encoding="utf-8"))
    scan_by_face = {face["face"]: face for face in scans["faces"]}
    radius = Rational(1, 10**arguments.radius_exponent)
    reports = []
    for face_name, face in cache["faces"].items():
        functions = [parse(rows) for rows in face["reducedStationary"]]
        target = parse(face["target"])
        total = parse(face["total"])
        roots = []
        for index, candidate in enumerate(scan_by_face[face_name]["candidates"], start=1):
            polished, iterations = polish(functions, candidate["physical"], arguments.digits)
            center = tuple(Rational(mp.nstr(value, arguments.center_digits, strip_zeros=False)) for value in polished)
            certificate = krawczyk(functions, center, radius)
            objective = objective_certificate(target, total, center, radius)
            if not certificate["strictInteriorInclusion"] or not certificate["contractionCertified"]:
                raise AssertionError(f"{face_name} candidate {index} failed Krawczyk inclusion")
            exact_center_fraction = objective["targetFractionPercentAtCenter"] / 100.0
            scan_fraction = float(candidate["targetFraction"])
            if abs(scan_fraction - exact_center_fraction) > 1.0e-11 * max(
                1.0,
                abs(exact_center_fraction),
            ):
                raise AssertionError(
                    f"{face_name} candidate {index} compact/physical objective mismatch"
                )
            objective["scanCrossCheckAbsoluteError"] = abs(
                scan_fraction - exact_center_fraction
            )
            roots.append(
                {
                    "index": index,
                    "polishedRoot": {
                        name: mp.nstr(polished[axis], arguments.digits - 10)
                        for axis, name in enumerate(face["freeVariables"])
                    },
                    "newtonIterations": iterations,
                    "stationarySystemCertificate": certificate,
                    "objectiveAndHessian": objective,
                }
            )
            emit("certified finite-face root", started, face=face_name, index=index)
        reports.append(
            {
                "face": face_name,
                "fixedVariable": face["fixedVariable"],
                "side": face["side"],
                "freeVariables": face["freeVariables"],
                "roots": roots,
            }
        )
    result = {
        "schemaVersion": 1,
        "scope": "finite-face local root certificates",
        "proofStatus": "local existence, uniqueness and Hessian classification; whole-face completeness pending",
        "configuration": {
            "digits": arguments.digits,
            "centerDigits": arguments.center_digits,
            "radiusExponent": arguments.radius_exponent,
        },
        "faces": reports,
        "wallSeconds": time.perf_counter() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    emit("all finite-face local certificates completed", started, roots=sum(len(face["roots"]) for face in reports))


if __name__ == "__main__":
    main()
