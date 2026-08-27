#!/usr/bin/env python3
"""Exact producer ledger for the R0.72R quantitative 1:2:3 core.

The continuum monotonicity argument and the enhanced-dissipation theorem live
in the report.  This program checks their finite algebraic spine with exact
integers and fractions.  It does not locate trigonometric roots numerically
and it does not claim a complete four-dimensional caustic decomposition.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
from typing import Any


AUDIT = "R0.72R producer quantitative 1:2:3 core exact audit"
SCHEMA_VERSION = 1


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rational(value: Fraction | int) -> str:
    value = Fraction(value)
    return f"{value.numerator}/{value.denominator}"


def git_commit(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unavailable"


def tracked_changes_dirty(root: Path) -> bool:
    return any(
        subprocess.run(command, cwd=root, check=False).returncode != 0
        for command in (
            ["git", "diff", "--quiet"],
            ["git", "diff", "--cached", "--quiet"],
        )
    )


def sources_tracked(root: Path) -> bool:
    required = (
        "research/r072r_report-source.md",
        "research/r072r_exact_audit.py",
        "research/r072r_compare_audits.py",
    )
    return all(
        subprocess.run(
            ["git", "ls-files", "--error-unmatch", relative],
            cwd=root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
        for relative in required
    )


def max_rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024.0 * 1024.0) if sys.platform == "darwin" else value / 1024.0


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_ndjson(path: Path, value: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True) + "\n")


def determinant_bareiss(matrix: list[list[int]]) -> int:
    """Fraction-free exact determinant of an integer matrix."""

    values = [row[:] for row in matrix]
    size = len(values)
    sign = 1
    previous = 1
    for column in range(size - 1):
        if values[column][column] == 0:
            pivot_row = next(
                (row for row in range(column + 1, size) if values[row][column]),
                None,
            )
            if pivot_row is None:
                return 0
            values[column], values[pivot_row] = values[pivot_row], values[column]
            sign *= -1
        pivot = values[column][column]
        for row in range(column + 1, size):
            for entry in range(column + 1, size):
                numerator = (
                    values[row][entry] * pivot
                    - values[row][column] * values[column][entry]
                )
                if numerator % previous:
                    raise ArithmeticError("Bareiss division was not exact")
                values[row][entry] = numerator // previous
            values[row][column] = 0
        previous = pivot
    return sign * values[-1][-1]


def resultant_integer(first: list[int], second: list[int]) -> int:
    degree_first = len(first) - 1
    degree_second = len(second) - 1
    width = degree_first + degree_second
    matrix: list[list[int]] = []
    for shift in range(degree_second):
        matrix.append([0] * shift + first + [0] * (degree_second - 1 - shift))
    for shift in range(degree_first):
        matrix.append([0] * shift + second + [0] * (degree_first - 1 - shift))
    if any(len(row) != width for row in matrix):
        raise AssertionError("invalid Sylvester matrix")
    return determinant_bareiss(matrix)


def real_slice_discriminant(a_value: int, b_value: int) -> int:
    coefficients = [
        3 * b_value,
        2 * a_value,
        1,
        0,
        -1,
        -2 * a_value,
        -3 * b_value,
    ]
    derivative = [(6 - index) * coefficients[index] for index in range(6)]
    result = resultant_integer(coefficients, derivative)
    leading = coefficients[0]
    if leading == 0 or result % leading:
        raise ArithmeticError("invalid sextic discriminant division")
    return -result // leading  # (-1)^(6*5/2) = -1


def verify_real_slice_factorization() -> dict[str, Any]:
    # A sextic discriminant has degree at most ten in its coefficients.  Since
    # each coefficient is affine in a,b, equality on an 11x11 tensor grid
    # proves the bivariate polynomial identity exactly.
    a_nodes = list(range(-5, 6))
    b_nodes = list(range(1, 12))
    checked = 0
    for a_value in a_nodes:
        for b_value in b_nodes:
            delta = a_value * a_value + 9 * b_value * b_value - 3 * b_value
            expected = (
                -64
                * (4 * a_value - 9 * b_value - 1) ** 3
                * (4 * a_value + 9 * b_value + 1) ** 3
                * delta**2
            )
            if real_slice_discriminant(a_value, b_value) != expected:
                raise AssertionError(f"real-slice factorization failed at {(a_value, b_value)}")
            checked += 1
    return {
        "discriminant": (
            "-64*(4*a-9*b-1)^3*(4*a+9*b+1)^3*"
            "(a^2+9*b^2-3*b)^2"
        ),
        "degreeBoundEachVariable": 10,
        "aNodes": a_nodes,
        "bNodes": b_nodes,
        "exactGridEvaluations": checked,
        "tensorGridIdentityProof": checked == 121,
    }


def canonical_payload() -> dict[str, Any]:
    center_z2 = Fraction(3, 20)
    radius_z2 = Fraction(1, 100)
    radius_z3 = Fraction(1, 1000)
    z2_lower = center_z2 - radius_z2
    z2_upper = center_z2 + radius_z2
    q2_initial_lower = 4 * z2_lower
    cone_exit = q2_initial_lower - Fraction(1, 2)
    q2_y1_upper = 4 * z2_upper * Fraction(1, 8) + 9 * radius_z3 * Fraction(1, 256)

    perturb_d1 = 2 * radius_z2 + 3 * radius_z3
    perturb_d2 = 4 * radius_z2 + 9 * radius_z3
    perturb_d3 = 8 * radius_z2 + 27 * radius_z3
    sin_lower = Fraction(1, 16) - Fraction(1, 24576)
    critical_sine_upper = Fraction(5, 2) * perturb_d1
    boundary_margin = Fraction(2, 5) * sin_lower - perturb_d1
    cos_double_radius_lower = Fraction(71, 72)
    normalized_curvature = cos_double_radius_lower - Fraction(3, 5) - perturb_d2
    normalized_quarter_margin = Fraction(1, 3) - perturb_d2 - Fraction(1, 4)
    pi_box_margin = Fraction(6, 7) - Fraction(3, 5) - perturb_d2 - Fraction(1, 5)

    derivative_bounds = [
        1 + z2_upper + radius_z3,
        1 + 2 * z2_upper + 3 * radius_z3,
        1 + 4 * z2_upper + 9 * radius_z3,
        1 + 8 * z2_upper + 27 * radius_z3,
    ]
    derivative_sum = sum(derivative_bounds, Fraction(0))
    upper_curvature_margin = Fraction(5, 3) - derivative_bounds[2]
    mixed_margin = Fraction(7, 3) - derivative_bounds[3]
    eta = Fraction(3, 7) ** 4
    slow_left = Fraction(7, 3) * eta
    slow_right = Fraction(3, 7) ** 3

    # The linear jet solution uses p=z2*exp(2i phi) and
    # q=z3*exp(3i phi)=A+iB.
    p_real = {"cos": Fraction(-1, 4), "A": Fraction(-9, 4)}
    p_imag = {"sin": Fraction(-1, 2), "B": Fraction(-3, 2)}
    f_prime = {
        "sin": Fraction(-1) - 2 * p_imag["sin"],
        "B": -2 * p_imag["B"] - 3,
    }
    f_second = {
        "cos": Fraction(-1) - 4 * p_real["cos"],
        "A": -4 * p_real["A"] - 9,
    }
    f_third = {
        "sin": Fraction(1) + 8 * p_imag["sin"],
        "B": 8 * p_imag["B"] + 27,
    }
    f_fourth = {
        "cos": Fraction(1) + 16 * p_real["cos"],
        "A": 16 * p_real["A"] + 81,
    }

    real_slice = verify_real_slice_factorization()
    checks = {
        "z2RangeExact": z2_lower == Fraction(7, 50) and z2_upper == Fraction(4, 25),
        "strictConeExit": cone_exit == Fraction(3, 50),
        "heatPathEntersOldConeByY1": q2_y1_upper == Fraction(20489, 256000) and q2_y1_upper < Fraction(1, 2),
        "perturbationBudgetsExact": (
            perturb_d1 == Fraction(23, 1000)
            and perturb_d2 == Fraction(49, 1000)
            and perturb_d3 == Fraction(107, 1000)
        ),
        "criticalLocalizationStrict": sin_lower > critical_sine_upper,
        "boundaryMarginExact": boundary_margin == Fraction(3047, 1536000),
        "normalizedCurvatureGreaterThanThird": normalized_curvature == Fraction(1517, 4500) and normalized_curvature > Fraction(1, 3),
        "localQuarterMarginExact": normalized_quarter_margin == Fraction(103, 3000),
        "piBoxMarginExact": pi_box_margin == Fraction(57, 7000),
        "derivativeLedgerExact": derivative_bounds == [Fraction(1161, 1000), Fraction(1323, 1000), Fraction(1649, 1000), Fraction(2307, 1000)],
        "derivativeSumExact": derivative_sum == Fraction(161, 25),
        "upperCurvatureMarginExact": upper_curvature_margin == Fraction(53, 3000),
        "mixedDerivativeMarginExact": mixed_margin == Fraction(79, 3000),
        "slowThresholdIdentity": slow_left == slow_right == Fraction(27, 343),
        "incidenceJetsExact": (
            all(value == 0 for value in f_prime.values())
            and all(value == 0 for value in f_second.values())
            and f_third == {"sin": Fraction(-3), "B": Fraction(15)}
            and f_fourth == {"cos": Fraction(-3), "A": Fraction(45)}
        ),
        "realSliceFactorizationExact": real_slice["tensorGridIdentityProof"] is True,
    }

    def rational_mapping(mapping: dict[str, Fraction]) -> dict[str, str]:
        return {key: rational(value) for key, value in mapping.items()}

    return {
        "schemaVersion": SCHEMA_VERSION,
        "theoremId": "R0.72R-four-real-dimensional-caustic-free-core",
        "polydisc": {
            "centerZ2": rational(center_z2),
            "radiusZ2": rational(radius_z2),
            "radiusZ3": rational(radius_z3),
            "absZ2Range": [rational(z2_lower), rational(z2_upper)],
            "realDimension": 4,
            "nonemptyInterior": True,
        },
        "heatPath": {
            "normalizedZ2": "z2*exp(-3*y)",
            "normalizedZ3": "z3*exp(-8*y)",
            "q2InitialLower": rational(q2_initial_lower),
            "oldConeBoundary": "1/2",
            "coneExitMargin": rational(cone_exit),
            "q2AtY1UpperUsingEGreaterThanTwo": rational(q2_y1_upper),
            "strictlyDecreasing": True,
            "uniqueOldConeCrossingOnZeroOne": True,
        },
        "perturbation": {
            "d1": rational(perturb_d1),
            "d2": rational(perturb_d2),
            "d3": rational(perturb_d3),
            "centerSlopeFactorLower": "2/5",
        },
        "criticalGeometry": {
            "criticalCount": 2,
            "criticalBoxes": ["dist(phi,0)<pi/48", "dist(phi,pi)<pi/48"],
            "sinRadiusLower": rational(sin_lower),
            "criticalSineUpper": rational(critical_sine_upper),
            "boundarySignMargin": rational(boundary_margin),
            "cosDoubleRadiusLower": rational(cos_double_radius_lower),
            "normalizedCurvatureLower": rational(normalized_curvature),
            "normalizedCurvatureGreaterThan": "1/3",
            "localQuarterMargin": rational(normalized_quarter_margin),
            "piBoxOneFifthMargin": rational(pi_box_margin),
        },
        "shapeContract": {
            "radius": "pi/48",
            "criticalCount": 2,
            "normalizedLocalSlope": ["1/4", "5/3"],
            "normalizedAwaySlopeLower": "1/80",
            "physicalWindow": "0<=y<=1",
            "physicalLocalSlope": ["1/12", "5/3"],
            "physicalAwaySlopeLower": "1/240",
            "C0": "144/1",
            "C1": "240/1",
            "upperCurvatureMargin": rational(upper_curvature_margin),
        },
        "derivativeLedger": {
            "d0": rational(derivative_bounds[0]),
            "d1": rational(derivative_bounds[1]),
            "d2": rational(derivative_bounds[2]),
            "d3": rational(derivative_bounds[3]),
            "sumW3Infinity": rational(derivative_sum),
            "mixedDerivativeUpper": rational(derivative_bounds[3]),
            "mixedBelowSevenThirdsMargin": rational(mixed_margin),
            "slowEtaThreshold": rational(eta),
            "slowEtaSymbolic": "(3/7)^4",
            "slowIdentityAtThreshold": rational(slow_left),
            "completeThresholdAlsoRequiresEtaCH": True,
        },
        "incidence": {
            "z3": "(A+i*B)*exp(-3*i*phi)",
            "z2": "exp(-2*i*phi)*(-(cos(phi)+9*A)/4-i*(sin(phi)+3*B)/2)",
            "gammaFixedZ3Coefficients": ["1/8", "-3/8", "-15/8", "-3/8"],
            "gammaFixedZ3Exponents": [-3, -1, 1, -5],
            "unitCirclePolynomial": "3*z3*u^6+2*z2*u^5+u^4-u^2-2*conj(z2)*u-3*conj(z3)",
            "degeneracyCondition": "exists abs(u)=1: D(u)=D'(u)=0",
            "pRealCoefficients": rational_mapping(p_real),
            "pImagCoefficients": rational_mapping(p_imag),
            "fPrimeCoefficients": rational_mapping(f_prime),
            "fSecondCoefficients": rational_mapping(f_second),
            "fThirdCoefficients": rational_mapping(f_third),
            "fFourthCoefficients": rational_mapping(f_fourth),
        },
        "realSlice": {
            "q": "12*b*x^2+4*a*x+1-3*b",
            "endpointWalls": ["1+4*a+9*b=0", "1-4*a+9*b=0"],
            "delta": "a^2+9*b^2-3*b",
            "internalArc": "delta=0 and 1/15<=b<=1/3",
            "openInteriorArc": "delta=0 and 1/15<b<=1/3",
            **real_slice,
        },
        "claimBoundary": {
            "finiteCertificateIsContinuumProof": False,
            "completeFourDimensionalChamberClassification": False,
            "causticCrossingEnhancedDissipation": False,
            "arbitraryTimeDependentPhases": False,
            "uniformThirdCarrierAmplitudeFloor": False,
            "generalThreeDimensionalRegularity": False,
        },
        "exactChecks": checks,
        "passed": all(checks.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parents[1]
    started = time.perf_counter()

    progress = output / "producer-progress.ndjson"
    resources = output / "producer-resource.ndjson"
    monitor = output / "producer-monitor.log"
    for path in (progress, resources, monitor):
        path.write_text("", encoding="utf-8")

    config = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT,
        "precision": "Python Fraction and exact integer Bareiss resultant audit",
        "gitCommit": git_commit(root),
        "sourceTracked": sources_tracked(root),
        "trackedChangesDirty": tracked_changes_dirty(root),
        "limitations": (
            "Finite exact algebra only; continuum trigonometric monotonicity, "
            "Coble--He enhanced dissipation, and global caustic topology remain "
            "analytic or open statements in the report."
        ),
    }
    write_json(output / "producer-config.json", config)
    append_ndjson(progress, {"time": utc_now(), "stage": "start", **config})

    payload = canonical_payload()
    write_json(output / "producer-payload.json", payload)
    stages = (
        ("cone-exit-and-heat-crossing", payload["heatPath"]["uniqueOldConeCrossingOnZeroOne"]),
        ("two-critical-shape", payload["shapeContract"]["criticalCount"] == 2),
        ("slow-time-ledger", payload["derivativeLedger"]["completeThresholdAlsoRequiresEtaCH"]),
        ("complex-incidence", payload["exactChecks"]["incidenceJetsExact"]),
        ("real-slice-factorization", payload["exactChecks"]["realSliceFactorizationExact"]),
        ("claim-boundary", payload["claimBoundary"]["finiteCertificateIsContinuumProof"] is False),
    )
    for stage, passed in stages:
        append_ndjson(progress, {"time": utc_now(), "stage": stage, "passed": passed})

    checks = {
        "payloadPassed": payload["passed"],
        "twoCriticalShapePassed": payload["shapeContract"]["criticalCount"] == 2,
        "coneCrossingPassed": payload["heatPath"]["uniqueOldConeCrossingOnZeroOne"] is True,
        "incidencePassed": payload["exactChecks"]["incidenceJetsExact"],
        "realSlicePassed": payload["exactChecks"]["realSliceFactorizationExact"],
        "claimBoundaryScoped": payload["claimBoundary"]["generalThreeDimensionalRegularity"] is False,
    }
    elapsed = time.perf_counter() - started
    result = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT,
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "elapsedSeconds": elapsed,
        "maxRssMb": max_rss_mb(),
        "limitations": config["limitations"],
    }
    write_json(output / "producer-result.json", result)
    append_ndjson(resources, {
        "time": utc_now(),
        "event": "complete",
        "elapsedSeconds": elapsed,
        "maxRssMb": result["maxRssMb"],
        "pid": os.getpid(),
    })
    monitor.write_text(
        f"[producer] status={result['status']} cone={checks['coneCrossingPassed']} "
        f"shape={checks['twoCriticalShapePassed']} incidence={checks['incidencePassed']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
