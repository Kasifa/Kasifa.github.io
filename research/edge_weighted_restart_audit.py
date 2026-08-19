#!/usr/bin/env python3
"""R0.37 exact weighted-Wiener restart and infinite-inverse audit.

R0.35 showed that the quadratic active map is unbounded on an ordinary
same-radius Wiener ball.  The missing degree factor is restored here by the
weighted norm

    ||f||_{B_r} = sum_(n,k) (n+k) |f_(n,k)| r^(n+k)

on the active support cone q=2k-n >= -1.  The all-order mixed layer estimate
implies

    ||Phi(f)||_{B_r} <= 3 ||f||_{B_r}^2,
    ||D Phi(f) h||_{B_r} <= 6 ||f||_{B_r} ||h||_{B_r}.

The audit uses the exact degree-40 recurrence polynomial at the rational
radius 16/243.  A rational contraction ball then proves that the same formal
active solution is analytic on a polydisc whose radius is 4/3 times the
R0.31 radius.  The finite support-pair and Jacobian checks are regressions;
the weighted Banach estimate and contraction argument are the all-order
parts of the result.

This concerns the reduced edge equation, not the full three-dimensional
Navier--Stokes equation.  It does not reach or certify the R0.32 Pade
candidate.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

import gmpy2

import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036


Rational = gmpy2.mpq
Exponent = tuple[int, int]
Polynomial = dict[Exponent, Rational]

R031_CERTIFICATE = Path(
    "research/certificates/r031/edge-optimized-majorant.json"
)
R036_CERTIFICATE = Path(
    "research/certificates/r036/edge-short-continuation.json"
)
R031_EXPECTED_SHA256 = (
    "32676dcefdf3c5285bdb18aab44bfdba385a84910d5e1d0df00f8ea9039ec395"
)
R036_EXPECTED_SHA256 = (
    "dfe0395df8b9654f235207c71dda5a0de8a70a54908b76b92dca00ad83c38e48"
)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.37 +{elapsed:8.2f}s] {stage}{suffix}",
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
    return r036.polynomial_digest(polynomial)


def degree(exponent: Exponent) -> int:
    return exponent[0] + exponent[1]


def charge(exponent: Exponent) -> int:
    return 2 * exponent[1] - exponent[0]


def admissible_basis(
    minimum_degree: int, maximum_degree: int
) -> list[Exponent]:
    return [
        (total_degree - w_degree, w_degree)
        for total_degree in range(minimum_degree, maximum_degree + 1)
        for w_degree in range(total_degree + 1)
        if 3 * w_degree - total_degree >= -1
    ]


def weighted_wiener_norm(polynomial: Polynomial, radius: Rational) -> Rational:
    """One-total-derivative isotropic Wiener norm."""

    return sum(
        (
            degree(exponent)
            * abs(value)
            * radius ** degree(exponent)
            for exponent, value in polynomial.items()
        ),
        Rational(0),
    )


def exact_matrix_product(
    left: list[list[Rational]], right: list[list[Rational]]
) -> list[list[Rational]]:
    return r036.exact_matrix_product(left, right)


def is_identity(matrix: list[list[Rational]]) -> bool:
    return r036.is_identity(matrix)


def matrix_digest(matrix: list[list[Rational]]) -> str:
    return r036.matrix_digest(matrix)


def support_pair_audit(maximum_degree: int) -> dict[str, object]:
    """Finite exact regression of the all-order mixed support estimate."""

    basis = admissible_basis(1, maximum_degree)
    ordered_pairs = 0
    nonzero_images = 0
    cancellation_pairs = 0
    maximum_ratio = Rational(0)
    equality_pairs = 0
    image_terms = 0

    for left_exponent in basis:
        left = {left_exponent: Rational(1)}
        left_degree = degree(left_exponent)
        for right_exponent in basis:
            right = {right_exponent: Rational(1)}
            right_degree = degree(right_exponent)
            image = r036.dphi(left, right)
            ordered_pairs += 1
            if charge(left_exponent) == charge(right_exponent) == -1:
                cancellation_pairs += 1
                if image:
                    raise AssertionError("the q=-1 plus q=-1 branch did not cancel")
            if image:
                nonzero_images += 1
            image_terms += len(image)
            if any(charge(exponent) < -1 for exponent in image):
                raise AssertionError("the active support cone was not preserved")
            if any(
                degree(exponent) != left_degree + right_degree
                for exponent in image
            ):
                raise AssertionError("the mixed derivative did not preserve grading")
            image_l1 = sum((abs(value) for value in image.values()), Rational(0))
            bound = 3 * min(left_degree, right_degree)
            if image_l1 > bound:
                raise AssertionError("finite mixed layer estimate failed")
            ratio = image_l1 / bound
            maximum_ratio = max(maximum_ratio, ratio)
            if image_l1 == bound:
                equality_pairs += 1

    return {
        "maximumInputDegree": maximum_degree,
        "basisDimension": len(basis),
        "orderedBasisPairs": ordered_pairs,
        "nonzeroImages": nonzero_images,
        "imageTerms": image_terms,
        "qMinusOnePairCancellations": cancellation_pairs,
        "maximumRatioToThreeTimesMinimumDegree": rational_record(maximum_ratio),
        "equalityPairs": equality_pairs,
        "classification": (
            "finite exact regression only; the all-order proof is the "
            "charge symmetrization and weighted layer inequality"
        ),
    }


def invert_unit_lower_triangular(
    matrix: list[list[Rational]],
) -> list[list[Rational]]:
    dimension = len(matrix)
    inverse = [
        [Rational(0) for _ in range(dimension)] for _ in range(dimension)
    ]
    for column in range(dimension):
        for row in range(dimension):
            correction = sum(
                (
                    matrix[row][previous] * inverse[previous][column]
                    for previous in range(row)
                ),
                Rational(0),
            )
            inverse[row][column] = Rational(row == column) - correction
    return inverse


def weighted_column_norm(
    matrix: list[list[Rational]],
    basis: list[Exponent],
    radius: Rational,
) -> Rational:
    column_norms = []
    for column, input_exponent in enumerate(basis):
        input_weight = degree(input_exponent) * radius ** degree(input_exponent)
        output_norm = sum(
            (
                abs(matrix[row][column])
                * degree(output_exponent)
                * radius ** degree(output_exponent)
                for row, output_exponent in enumerate(basis)
            ),
            Rational(0),
        )
        column_norms.append(output_norm / input_weight)
    return max(column_norms, default=Rational(0))


def finite_jacobian_audit(
    active: Polynomial,
    maximum_degree: int,
    radii: dict[str, Rational],
) -> dict[str, object]:
    """Exact low block on the support cone; not the infinite inverse proof."""

    basis = admissible_basis(2, maximum_degree)
    index = {exponent: position for position, exponent in enumerate(basis)}
    dimension = len(basis)
    jacobian = [
        [Rational(0) for _ in range(dimension)] for _ in range(dimension)
    ]

    for column, exponent in enumerate(basis):
        image = r036.select_degrees(
            r036.add(
                {exponent: Rational(1)},
                r036.scale(r036.dphi(active, {exponent: Rational(1)}), -1),
            ),
            2,
            maximum_degree,
        )
        if any(output_exponent not in index for output_exponent in image):
            raise AssertionError("finite Jacobian left the active support cone")
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
        raise AssertionError("finite support-cone Jacobian is not unit lower triangular")

    inverse = invert_unit_lower_triangular(jacobian)
    left_identity = is_identity(exact_matrix_product(inverse, jacobian))
    right_identity = is_identity(exact_matrix_product(jacobian, inverse))
    if not left_identity or not right_identity:
        raise AssertionError("finite support-cone inverse failed")

    identity = [
        [Rational(row == column) for column in range(dimension)]
        for row in range(dimension)
    ]
    derivative = [
        [identity[row][column] - jacobian[row][column] for column in range(dimension)]
        for row in range(dimension)
    ]
    radius_records = {}
    for name, radius in radii.items():
        derivative_norm = weighted_column_norm(derivative, basis, radius)
        inverse_norm = weighted_column_norm(inverse, basis, radius)
        active_norm = weighted_wiener_norm(active, radius)
        all_order_linearization_bound = 6 * active_norm
        if derivative_norm > all_order_linearization_bound:
            raise AssertionError("finite derivative norm exceeded the Banach bound")
        radius_records[name] = {
            "radius": rational_record(radius),
            "finiteDerivativeWeightedColumnNorm": rational_record(derivative_norm),
            "finiteInverseWeightedColumnNorm": rational_record(inverse_norm),
            "sixTimesDegreeFortyPolynomialNorm": rational_record(
                all_order_linearization_bound
            ),
        }

    return {
        "maximumTotalDegree": maximum_degree,
        "basis": "total degree 2 through M with charge q>=-1",
        "dimension": dimension,
        "jacobianUnitLowerTriangular": diagonal_is_one and strictly_lower,
        "jacobianNonzeroEntries": sum(
            value != 0 for row in jacobian for value in row
        ),
        "inverseNonzeroEntries": sum(
            value != 0 for row in inverse for value in row
        ),
        "leftInverseExact": left_identity,
        "rightInverseExact": right_identity,
        "jacobianSha256": matrix_digest(jacobian),
        "inverseSha256": matrix_digest(inverse),
        "radii": radius_records,
        "classification": (
            "finite exact low-block regression; the infinite inverse follows "
            "from the all-order Neumann bound, not from this matrix"
        ),
    }


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


def build_payload(
    maximum_degree: int,
    pair_audit_degree: int,
    jacobian_degree: int,
    show_progress: bool,
    source_commit: str | None,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "loading pinned R0.31 and R0.36 certificates")
    if sha256(R031_CERTIFICATE) != R031_EXPECTED_SHA256:
        raise AssertionError("R0.31 certificate hash mismatch")
    if sha256(R036_CERTIFICATE) != R036_EXPECTED_SHA256:
        raise AssertionError("R0.36 certificate hash mismatch")
    r031 = json.loads(R031_CERTIFICATE.read_text(encoding="utf-8"))
    r036_certificate = json.loads(R036_CERTIFICATE.read_text(encoding="utf-8"))

    rho = Rational(4, 81)
    majorant_constant = Rational(81, 4)
    target_radius = Rational(4, 3) * rho
    if target_radius != Rational(16, 243):
        raise AssertionError("unexpected target radius")

    progress(
        show_progress,
        started,
        "constructing exact degree recurrence",
        maximumDegree=maximum_degree,
    )
    active_field, _, _, recurrence_interactions = r028.rational_edge_recurrence(
        maximum_degree,
        False,
        started,
    )
    active = r036.field_to_polynomial(active_field, maximum_degree)
    seed = {(1, 0): Rational(1), (0, 1): Rational(1)}
    residual = r036.add(
        active,
        r036.scale(seed, -1),
        r036.scale(r036.phi(active), -1),
    )
    low_residual = r036.truncate(residual, maximum_degree)
    if low_residual:
        raise AssertionError("degree recurrence has a residual below the cutoff")

    progress(
        show_progress,
        started,
        "auditing support-cone mixed basis pairs",
        maximumDegree=pair_audit_degree,
    )
    pair_audit = support_pair_audit(pair_audit_degree)
    outside_left = {(0, 2): Rational(1)}
    outside_right = {(3, 0): Rational(1)}
    outside_image = r036.dphi(outside_left, outside_right)
    outside_image_norm = sum(
        (abs(value) for value in outside_image.values()), Rational(0)
    )
    outside_mixed_bound = Rational(3) * min(2, 3)
    outside_ratio = outside_image_norm / outside_mixed_bound
    if outside_image != {(3, 2): Rational(21, 2)} or outside_ratio != Rational(7, 4):
        raise AssertionError("support-cone scope counterexample changed")

    progress(show_progress, started, "forming exact contraction inequalities")
    polynomial_norm = weighted_wiener_norm(active, target_radius)
    residual_norm = weighted_wiener_norm(residual, target_radius)
    linearization_bound = 6 * polynomial_norm
    contraction_margin = 1 - linearization_bound
    ball_radius = contraction_margin / 12
    residual_allowance = contraction_margin**2 / 16
    mapping_upper_bound = (
        residual_norm
        + linearization_bound * ball_radius
        + 3 * ball_radius**2
    )
    lipschitz_upper_bound = linearization_bound + 6 * ball_radius
    solution_norm_upper_bound = polynomial_norm + ball_radius
    transport_operator_bound = 2 * solution_norm_upper_bound
    transport_inverse_bound = 1 / (1 - transport_operator_bound)
    transport_field_norm_bound = target_radius * transport_inverse_bound

    boundary_partial_norm = weighted_wiener_norm(active, rho)
    boundary_tail_bound = Rational(2) / majorant_constant / maximum_degree
    boundary_solution_norm_bound = boundary_partial_norm + boundary_tail_bound
    boundary_jacobian_norm_bound = 6 * boundary_solution_norm_bound
    boundary_inverse_norm_bound = 1 / (1 - boundary_jacobian_norm_bound)

    progress(
        show_progress,
        started,
        "constructing exact support-cone Jacobian block",
        maximumDegree=jacobian_degree,
    )
    finite_jacobian = finite_jacobian_audit(
        active,
        jacobian_degree,
        {"r031Boundary": rho, "restartRadius": target_radius},
    )

    residual_degrees = sorted({degree(exponent) for exponent in residual})
    checks = {
        "pinnedInputHashes": True,
        "supportPairRegressionExact": (
            pair_audit["orderedBasisPairs"] > 0
            and pair_audit["qMinusOnePairCancellations"] > 0
        ),
        "unrestrictedScopeCounterexampleExact": outside_ratio > 1,
        "originRecurrenceThroughCutoff": not low_residual,
        "residualBeginsAboveCutoff": min(residual_degrees) > maximum_degree,
        "targetRadiusIsFourThirdsR031": target_radius / rho == Rational(4, 3),
        "linearizationBoundBelowOne": linearization_bound < 1,
        "residualFitsContractionBall": residual_norm <= residual_allowance,
        "ballMapsStrictlyInsideItself": mapping_upper_bound < ball_radius,
        "ballLipschitzConstantBelowOne": lipschitz_upper_bound < 1,
        "transportOperatorBoundBelowOne": transport_operator_bound < 1,
        "boundaryInfiniteJacobianNeumannBound": (
            boundary_jacobian_norm_bound < 1
        ),
        "finiteSupportJacobianInverseExact": (
            finite_jacobian["leftInverseExact"]
            and finite_jacobian["rightInverseExact"]
        ),
    }
    if not all(checks.values()):
        raise AssertionError("one or more R0.37 checks failed")

    payload = {
        "scope": {
            "result": (
                "an all-order weighted-Wiener contraction theorem extending "
                "the common analytic radius of the reduced active and transport fields"
            ),
            "classification": (
                "all-order Banach-space theorem, exact rational degree-40 "
                "restart certificate, and finite exact implementation regressions"
            ),
            "limitations": [
                "the theorem is restricted to the active support cone q>=-1",
                "the result concerns the reduced edge generating equation rather than the full PDE",
                "the new radius remains far inside the finite R0.32 Pade candidate",
                "the candidate is not upgraded to a singularity",
                "no Navier-Stokes regularity or blow-up conclusion is claimed",
            ],
        },
        "input": {
            "r031": {
                "path": str(R031_CERTIFICATE),
                "sha256": R031_EXPECTED_SHA256,
                "sourceCommit": r031["git"]["commit"],
            },
            "r036": {
                "path": str(R036_CERTIFICATE),
                "sha256": R036_EXPECTED_SHA256,
                "sourceCommit": r036_certificate["git"]["commit"],
            },
        },
        "allOrderTheorem": {
            "space": (
                "B_r^+={f=sum f_(n,k)Z^nW^k: q=2k-n>=-1, "
                "||f||=sum (n+k)|f_(n,k)|r^(n+k)<infinity}"
            ),
            "supportPreservation": (
                "the q=-1 plus q=-1 contribution cancels after charge "
                "symmetrization; every remaining output has q>=-1"
            ),
            "mixedLayerBound": (
                "||(D Phi(f)h)_L||_1 <= (3/2) sum_(i+j=L) "
                "min(i,j)(A_i H_j+H_i A_j)"
            ),
            "weightedQuadraticBound": "||Phi(f)||_(B_r) <= 3||f||_(B_r)^2",
            "weightedDerivativeBound": (
                "||D Phi(f)h||_(B_r) <= 6||f||_(B_r)||h||_(B_r)"
            ),
            "transportOperatorBound": (
                "||T_a f||_(B_r) <= 2||a||_(B_r)||f||_(B_r)"
            ),
            "proofInequality": "(i+j)min(i,j)<=2ij",
            "r031UniversalSolutionNormBound": "||a||_(B_r)<40/243 for r<=4/81",
            "r031UniversalJacobianBound": "||D Phi(a)||_(B_r)<80/81",
            "r031UniversalInverseBound": (
                "||(I-D Phi(a))^(-1)||_(B_r->B_r)<=81 by the Neumann series"
            ),
            "proofMethod": (
                "charge symmetrization, the R0.31 all-order coefficient majorant, "
                "and Banach's fixed-point theorem"
            ),
        },
        "boundaryInfiniteInverse": {
            "radius": rational_record(rho),
            "degreeFortyPartialSolutionNorm": rational_record(
                boundary_partial_norm
            ),
            "allOrderTailBound": rational_record(boundary_tail_bound),
            "solutionNormUpperBound": rational_record(
                boundary_solution_norm_bound
            ),
            "jacobianNormUpperBound": rational_record(
                boundary_jacobian_norm_bound
            ),
            "inverseNormUpperBound": rational_record(
                boundary_inverse_norm_bound
            ),
            "tailProof": (
                "sum_(L>N) 1/L^2 <= integral_N^infinity x^(-2) dx=1/N"
            ),
        },
        "restartCertificate": {
            "polynomialCutoff": maximum_degree,
            "targetRadius": rational_record(target_radius),
            "r031Radius": rational_record(rho),
            "radiusGain": rational_record(target_radius / rho),
            "fixedChargeRadiusGain": rational_record((target_radius / rho) ** 3),
            "degreeFortyPolynomialSha256": polynomial_digest(active),
            "degreeFortyPolynomialTerms": len(active),
            "degreeFortyPolynomialNorm": rational_record(polynomial_norm),
            "exactResidualSha256": polynomial_digest(residual),
            "exactResidualTerms": len(residual),
            "residualDegreeRange": [min(residual_degrees), max(residual_degrees)],
            "exactResidualNorm": rational_record(residual_norm),
            "linearizationNormUpperBound": rational_record(linearization_bound),
            "contractionMargin": rational_record(contraction_margin),
            "chosenBallRadius": rational_record(ball_radius),
            "correctionSpace": (
                "the closed support-cone tail subspace of B_r with total "
                "degrees strictly greater than 40"
            ),
            "residualAllowance": rational_record(residual_allowance),
            "residualToAllowanceRatio": rational_record(
                residual_norm / residual_allowance
            ),
            "mappingUpperBound": rational_record(mapping_upper_bound),
            "lipschitzUpperBound": rational_record(lipschitz_upper_bound),
            "solutionNormUpperBound": rational_record(solution_norm_upper_bound),
            "transportOperatorNormUpperBound": rational_record(
                transport_operator_bound
            ),
            "transportInverseNormUpperBound": rational_record(
                transport_inverse_bound
            ),
            "eachNormalizedTransportFieldNormUpperBound": rational_record(
                transport_field_norm_bound
            ),
            "statement": (
                "there is a unique fixed point in the closed degree-greater-than-40 "
                "B_r tail ball of the stated radius around the polynomial; "
                "triangular formal uniqueness identifies it with the canonical "
                "active series, and the transport bound constructs the canonical "
                "normalized U and V series on the same radius"
            ),
        },
        "finiteRegression": {
            "recurrenceMaximumDegree": maximum_degree,
            "recurrenceOrderedInteractions": recurrence_interactions,
            "supportPairs": pair_audit,
            "supportRestrictionCounterexample": {
                "leftMonomial": "W^2",
                "leftCharge": 4,
                "rightMonomial": "Z^3",
                "rightCharge": -3,
                "mixedImage": "(21/2) Z^3 W^2",
                "ratioToThreeTimesMinimumDegree": rational_record(
                    outside_ratio
                ),
                "meaning": (
                    "outside q>=-1 the mixed constant three already fails; "
                    "the support restriction is a theorem hypothesis, not decoration"
                ),
            },
            "jacobian": finite_jacobian,
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
        "completed R0.37 weighted restart certificate",
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
    parser.add_argument("--pair-audit-degree", type=int, default=12)
    parser.add_argument("--jacobian-degree", type=int, default=12)
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
    if not 2 <= arguments.pair_audit_degree <= arguments.max_total_degree:
        raise SystemExit("--pair-audit-degree must lie between 2 and the recurrence cutoff")
    if not 3 <= arguments.jacobian_degree <= arguments.max_total_degree:
        raise SystemExit("--jacobian-degree must lie between 3 and the recurrence cutoff")
    if arguments.progress_log is not None:
        if arguments.progress_log.exists():
            raise SystemExit("--progress-log already exists; choose a new path")
        arguments.progress_log.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG = arguments.progress_log
    payload = build_payload(
        arguments.max_total_degree,
        arguments.pair_audit_degree,
        arguments.jacobian_degree,
        arguments.progress,
        arguments.source_commit,
    )
    if arguments.check and not all(payload["checks"].values()):
        raise AssertionError("R0.37 certificate checks failed")
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
