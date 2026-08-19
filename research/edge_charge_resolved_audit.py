#!/usr/bin/env python3
"""R0.39 exact charge-resolved tail and transport audit.

For a base monomial of degree i and charge q and a tail monomial of degree
j and charge s, the derivative of the reduced active map has the exact
coefficient

    gamma = (i*s-q*j)*(s-q) / (3*(s+q)*(i+j-1)),  s+q != 0,

and

    gamma = (i*s-q*j)*(j-i) / (3*(i+j)*(i+j-1)),  s+q = 0.

The weighted l1 column ratio is ((i+j)/j)*abs(gamma).  This script keeps
the input charge s instead of replacing every column by the charge-blind
mixed-layer constant.  Charges -1 through S-1 are bounded separately, and
all s >= S are closed by one analytic tail estimate.  The resulting bound
controls every degree j>N; finite column scans are regressions only.

The same degree-charge coordinates sharpen the normalized transport bound.
For T_a f=(L-1)^(-1){a,f}, an active base monomial contributes at most

    tau(i,q) = (i+1)/i * max(i+q, 2*i-q) / 3

to the induced weighted Wiener norm.  The unknown active correction is
still controlled by the general 2*||h|| bound.

All decisions use exact GMP rationals.  This concerns the reduced edge
generating system.  It is not a regularity or blow-up result for the full
three-dimensional Navier--Stokes equation.
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
import edge_weighted_restart_audit as r037
import edge_tail_newton_audit as r038


Rational = gmpy2.mpq
Exponent = tuple[int, int]
Polynomial = dict[Exponent, Rational]

R038_CERTIFICATE = Path(
    "research/certificates/r038/edge-tail-newton.json"
)
R038_EXPECTED_SHA256 = (
    "3eb320e8cef0289c7fa2fef00a38c3c66b6b4c5006375bf6386d784f6b95dbf4"
)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.39 +{elapsed:8.2f}s] {stage}{suffix}",
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


def rational(value: str | int | Rational) -> Rational:
    return Rational(value)


def degree(exponent: Exponent) -> int:
    return exponent[0] + exponent[1]


def charge(exponent: Exponent) -> int:
    return 2 * exponent[1] - exponent[0]


def monomial_derivative_coefficient(
    base_degree: int,
    base_charge: int,
    input_degree: int,
    input_charge: int,
) -> Rational:
    """Exact coefficient of one base/input monomial pair in D Phi."""

    output_charge = base_charge + input_charge
    determinant_factor = (
        base_degree * input_charge - base_charge * input_degree
    )
    if output_charge:
        return Rational(
            determinant_factor * (input_charge - base_charge),
            3 * output_charge * (base_degree + input_degree - 1),
        )
    return Rational(
        determinant_factor * (input_degree - base_degree),
        3
        * (base_degree + input_degree)
        * (base_degree + input_degree - 1),
    )


def minimum_tail_degree(input_charge: int, cutoff: int) -> int:
    """Smallest admissible j>N with charge s for a bivariate monomial."""

    candidate = max(cutoff + 1, (input_charge + 1) // 2)
    while (candidate + input_charge) % 3:
        candidate += 1
    return candidate


def finite_charge_factor(
    base_degree: int,
    base_charge: int,
    input_charge: int,
    minimum_degree: int,
) -> Rational:
    """Uniform column factor for one fixed input charge and every j>=J."""

    if input_charge + base_charge == 0:
        if base_charge == 0:
            return Rational(0)
        return Rational(
            abs(base_charge) * (base_degree + minimum_degree),
            3 * (base_degree + minimum_degree - 1),
        )
    return Rational(
        (base_degree + minimum_degree)
        * (abs(base_charge) * minimum_degree + base_degree * abs(input_charge))
        * abs(input_charge - base_charge),
        3
        * (base_degree + minimum_degree - 1)
        * minimum_degree
        * abs(input_charge + base_charge),
    )


def large_charge_factor(
    base_degree: int,
    base_charge: int,
    cutoff: int,
    charge_cutoff: int,
) -> Rational:
    """Uniform factor for every input charge s>=charge_cutoff."""

    degree_factor = Rational(
        base_degree + cutoff + 1,
        base_degree + cutoff,
    )
    if base_charge == -1:
        return (
            degree_factor
            * (2 * base_degree + 1)
            * Rational(charge_cutoff + 1, 3 * (charge_cutoff - 1))
        )
    if base_charge < -1:
        raise AssertionError("large-charge bound received q<-1")
    return (
        degree_factor
        * max(base_charge, abs(2 * base_degree - base_charge))
        / 3
    )


def transport_factor(base_degree: int, base_charge: int) -> Rational:
    """Uniform T_a column factor for every monomial input."""

    if base_charge < -1 or base_charge > 2 * base_degree:
        raise AssertionError("transport factor received an inadmissible charge")
    return Rational(
        (base_degree + 1)
        * max(base_degree + base_charge, 2 * base_degree - base_charge),
        3 * base_degree,
    )


def weighted_base_terms(
    polynomial: Polynomial,
    radius: Rational,
) -> list[tuple[int, int, Rational]]:
    return [
        (
            degree(exponent),
            charge(exponent),
            abs(value) * radius ** degree(exponent),
        )
        for exponent, value in polynomial.items()
    ]


def digest_records(records: list[tuple[str, Rational]]) -> str:
    serialized = "".join(f"{label}:{value}\n" for label, value in records)
    return hashlib.sha256(serialized.encode("ascii")).hexdigest()


def charge_resolved_tail_bound(
    polynomial: Polynomial,
    radius: Rational,
    cutoff: int,
    charge_cutoff: int,
) -> dict[str, object]:
    """Finite charge columns plus one analytic infinite-charge closure."""

    terms = weighted_base_terms(polynomial, radius)
    columns: list[dict[str, object]] = []
    digest_input: list[tuple[str, Rational]] = []
    maximum = Rational(0)
    maximum_label = ""

    for input_charge in range(-1, charge_cutoff):
        minimum_degree = minimum_tail_degree(input_charge, cutoff)
        value = sum(
            (
                weighted_coefficient
                * finite_charge_factor(
                    base_degree,
                    base_charge,
                    input_charge,
                    minimum_degree,
                )
                for base_degree, base_charge, weighted_coefficient in terms
            ),
            Rational(0),
        )
        label = str(input_charge)
        digest_input.append((label, value))
        columns.append(
            {
                "inputCharge": input_charge,
                "minimumTailDegree": minimum_degree,
                "bound": r037.rational_record(value),
            }
        )
        if value > maximum:
            maximum = value
            maximum_label = label

    large_value = sum(
        (
            weighted_coefficient
            * large_charge_factor(
                base_degree,
                base_charge,
                cutoff,
                charge_cutoff,
            )
            for base_degree, base_charge, weighted_coefficient in terms
        ),
        Rational(0),
    )
    large_label = f">={charge_cutoff}"
    digest_input.append((large_label, large_value))
    if large_value > maximum:
        maximum = large_value
        maximum_label = large_label

    return {
        "finiteChargeRange": [-1, charge_cutoff - 1],
        "finiteColumns": columns,
        "finiteColumnCount": len(columns),
        "largeChargeSector": {
            "inputChargeRange": [charge_cutoff, None],
            "bound": r037.rational_record(large_value),
            "proof": (
                "write x=s/j in [0,2]; for q>=0 use "
                "abs(s-q)/(s+q)<=1 and abs(i*x-q)<=max(q,abs(2*i-q)); "
                "for q=-1 use (s+1)/(s-1)<=(S+1)/(S-1)"
            ),
        },
        "maximumBound": r037.rational_record(maximum),
        "maximumSector": maximum_label,
        "columnBoundsSha256": digest_records(digest_input),
        "classification": (
            "all-order induced-l1 bound: fixed charge columns are uniform in "
            "every admissible degree and the final sector contains all s>=S"
        ),
    }


def refined_transport_bound(
    polynomial: Polynomial,
    radius: Rational,
) -> Rational:
    return sum(
        (
            abs(value)
            * radius ** degree(exponent)
            * transport_factor(degree(exponent), charge(exponent))
            for exponent, value in polynomial.items()
        ),
        Rational(0),
    )


def exact_tail_column_scan(
    polynomial: Polynomial,
    radius: Rational,
    input_degree: int,
) -> dict[str, object]:
    """Finite exact columns; not used in the infinite-dimensional proof."""

    basis = [
        (input_degree - w_degree, w_degree)
        for w_degree in range(input_degree + 1)
        if 3 * w_degree - input_degree >= -1
    ]
    maximum = Rational(0)
    maximum_exponent: Exponent | None = None
    interactions = 0
    for input_exponent in basis:
        input_charge = charge(input_exponent)
        ratio = Rational(0)
        for base_exponent, value in polynomial.items():
            coefficient = monomial_derivative_coefficient(
                degree(base_exponent),
                charge(base_exponent),
                input_degree,
                input_charge,
            )
            ratio += (
                Rational(degree(base_exponent) + input_degree, input_degree)
                * abs(coefficient)
                * abs(value)
                * radius ** degree(base_exponent)
            )
            interactions += 1
        if ratio > maximum:
            maximum = ratio
            maximum_exponent = input_exponent
    return {
        "inputDegree": input_degree,
        "admissibleColumns": len(basis),
        "exactInteractions": interactions,
        "maximumWeightedColumnRatio": r037.rational_record(maximum),
        "maximumColumnExponent": list(maximum_exponent or ()),
        "maximumColumnCharge": (
            charge(maximum_exponent) if maximum_exponent is not None else None
        ),
        "classification": "finite exact regression only",
    }


def monomial_formula_regression(maximum_degree: int) -> dict[str, object]:
    basis = [
        (total_degree - w_degree, w_degree)
        for total_degree in range(1, maximum_degree + 1)
        for w_degree in range(total_degree + 1)
        if 3 * w_degree - total_degree >= -1
    ]
    checked = 0
    zero_images = 0
    for base_exponent in basis:
        for input_exponent in basis:
            expected_exponent = (
                base_exponent[0] + input_exponent[0],
                base_exponent[1] + input_exponent[1],
            )
            expected = monomial_derivative_coefficient(
                degree(base_exponent),
                charge(base_exponent),
                degree(input_exponent),
                charge(input_exponent),
            )
            image = r036.dphi(
                {base_exponent: Rational(1)},
                {input_exponent: Rational(1)},
            )
            if image.get(expected_exponent, Rational(0)) != expected:
                raise AssertionError("closed coefficient formula mismatch")
            if any(exponent != expected_exponent for exponent in image):
                raise AssertionError("monomial derivative produced another exponent")
            if not image:
                zero_images += 1
            checked += 1
    return {
        "maximumInputDegree": maximum_degree,
        "admissibleBasisDimension": len(basis),
        "orderedPairsChecked": checked,
        "zeroImages": zero_images,
        "passed": True,
        "classification": "finite exact implementation regression",
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
    target_radius: Rational,
    charge_cutoff: int,
    failure_probe_radius: Rational,
    finite_column_degrees: list[int],
    formula_regression_degree: int,
    ball_divisor: int,
    show_progress: bool,
    source_commit: str | None,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "loading pinned R0.38 certificate")
    if sha256(R038_CERTIFICATE) != R038_EXPECTED_SHA256:
        raise AssertionError("R0.38 certificate hash mismatch")
    r038_certificate = json.loads(R038_CERTIFICATE.read_text(encoding="utf-8"))
    previous_radius = rational(
        r038_certificate["restartCertificate"]["targetRadius"]["exact"]
    )
    r031_radius = rational(
        r038_certificate["restartCertificate"]["r031Radius"]["exact"]
    )
    if target_radius <= previous_radius:
        raise AssertionError("R0.39 target must exceed the R0.38 radius")

    progress(
        show_progress,
        started,
        "constructing exact degree recurrence",
        maximumDegree=maximum_degree,
    )
    active_field, _, _, recurrence_interactions = r028.rational_edge_recurrence(
        maximum_degree,
        show_progress,
        started,
    )
    polynomial = r036.field_to_polynomial(active_field, maximum_degree)
    if any(charge(exponent) < -1 for exponent in polynomial):
        raise AssertionError("degree polynomial left the active support cone")

    seed = {(1, 0): Rational(1), (0, 1): Rational(1)}
    progress(
        show_progress,
        started,
        "forming complete polynomial residual",
        maximumResidualDegree=2 * maximum_degree,
    )
    residual = r036.add(
        polynomial,
        r036.scale(seed, -1),
        r036.scale(r036.phi(polynomial), -1),
    )
    low_residual = r036.truncate(residual, maximum_degree)
    if low_residual:
        raise AssertionError("degree recurrence has a residual below the cutoff")
    residual_degrees = sorted({degree(exponent) for exponent in residual})

    progress(
        show_progress,
        started,
        "forming all-order charge-resolved tail bounds",
        finiteCharges=charge_cutoff + 1,
    )
    tail = charge_resolved_tail_bound(
        polynomial,
        target_radius,
        maximum_degree,
        charge_cutoff,
    )
    probe_tail = charge_resolved_tail_bound(
        polynomial,
        failure_probe_radius,
        maximum_degree,
        charge_cutoff,
    )
    tail_bound = rational(tail["maximumBound"]["exact"])
    probe_tail_bound = rational(probe_tail["maximumBound"]["exact"])
    old_tail = r038.tail_linearization_quantities(
        polynomial,
        target_radius,
        maximum_degree,
    )

    polynomial_norm = r037.weighted_wiener_norm(polynomial, target_radius)
    residual_norm = r037.weighted_wiener_norm(residual, target_radius)
    contraction_margin = 1 - tail_bound
    ball_radius = contraction_margin / ball_divisor
    residual_allowance = (
        contraction_margin * ball_radius - 3 * ball_radius**2
    )
    mapping_upper_bound = (
        residual_norm + tail_bound * ball_radius + 3 * ball_radius**2
    )
    lipschitz_upper_bound = tail_bound + 6 * ball_radius
    solution_norm_upper_bound = polynomial_norm + ball_radius

    polynomial_transport_bound = refined_transport_bound(
        polynomial,
        target_radius,
    )
    transport_operator_bound = polynomial_transport_bound + 2 * ball_radius
    transport_inverse_bound = 1 / (1 - transport_operator_bound)
    old_scalar_transport_bound = 2 * solution_norm_upper_bound

    probe_margin = 1 - probe_tail_bound
    probe_ball_radius = (
        probe_margin / ball_divisor if probe_margin > 0 else Rational(0)
    )
    probe_polynomial_transport_bound = refined_transport_bound(
        polynomial,
        failure_probe_radius,
    )
    probe_transport_bound = (
        probe_polynomial_transport_bound + 2 * probe_ball_radius
    )

    progress(
        show_progress,
        started,
        "checking exact monomial coefficient formula",
        maximumDegree=formula_regression_degree,
    )
    formula_regression = monomial_formula_regression(formula_regression_degree)

    finite_columns = []
    for input_degree in finite_column_degrees:
        progress(
            show_progress,
            started,
            "auditing finite exact tail columns",
            inputDegree=input_degree,
        )
        finite_columns.append(
            exact_tail_column_scan(polynomial, target_radius, input_degree)
        )

    candidate_fixed_charge_lower = rational(
        r038_certificate["candidateComparison"][
            "tailTransportCandidateModulusLower"
        ]["exact"]
    )
    candidate_gap_factor = candidate_fixed_charge_lower / target_radius**3

    checks = {
        "pinnedInputHash": True,
        "activeSupportConePreserved": all(
            charge(exponent) >= -1 for exponent in polynomial
        ),
        "originRecurrenceThroughCutoff": not low_residual,
        "residualBeginsAboveCutoff": min(residual_degrees) > maximum_degree,
        "residualEndsAtTwiceCutoff": max(residual_degrees) <= 2 * maximum_degree,
        "targetRadiusExceedsR038": target_radius > previous_radius,
        "closedMonomialCoefficientFormulaExact": formula_regression["passed"],
        "oldR038TailBoundFailsAtTarget": (
            old_tail["tailLinearizationBound"] > 1
        ),
        "chargeResolvedTailBoundBelowOne": tail_bound < 1,
        "finiteAndInfiniteChargeSectorsCoverAllInputs": (
            tail["finiteChargeRange"] == [-1, charge_cutoff - 1]
            and tail["largeChargeSector"]["inputChargeRange"]
            == [charge_cutoff, None]
        ),
        "residualFitsContractionBall": residual_norm < residual_allowance,
        "ballMapsStrictlyInsideItself": mapping_upper_bound < ball_radius,
        "ballLipschitzConstantBelowOne": lipschitz_upper_bound < 1,
        "chargeResolvedTransportBoundBelowOne": transport_operator_bound < 1,
        "oldScalarTransportBoundFailsAtTarget": old_scalar_transport_bound > 1,
        "nearbyProbeFailsRefinedTransportCondition": (
            failure_probe_radius > target_radius
            and probe_tail_bound < 1
            and probe_transport_bound > 1
        ),
        "finiteExactColumnsBelowAllOrderBound": all(
            rational(column["maximumWeightedColumnRatio"]["exact"])
            <= tail_bound
            for column in finite_columns
        ),
        "finiteCandidateRemainsOutsideCertifiedDisk": candidate_gap_factor > 1,
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        diagnostics = {
            "failed": failed,
            "targetTail": r037.rational_record(tail_bound),
            "targetTransport": r037.rational_record(transport_operator_bound),
            "probeTail": r037.rational_record(probe_tail_bound),
            "probeTransport": r037.rational_record(probe_transport_bound),
        }
        raise AssertionError(
            "one or more R0.39 checks failed: "
            + json.dumps(diagnostics, sort_keys=True)
        )

    payload = {
        "scope": {
            "result": (
                "an all-order charge-resolved tail theorem and refined transport "
                "bound extending the common analytic radius of the reduced fields"
            ),
            "classification": (
                "all-order Banach-space theorem, exact rational degree-80 restart "
                "certificate, and finite exact implementation regressions"
            ),
            "limitations": [
                "the theorem is restricted to active corrections on q>=-1",
                "the finite charge table is paired with an analytic infinite-charge closure",
                "the result concerns the reduced edge generating equation rather than the full PDE",
                "the R0.32 finite Pade candidate remains outside the certified fixed-charge disk",
                "the nearby negative control is failure of a sufficient transport inequality only",
                "no Navier-Stokes regularity or blow-up conclusion is claimed",
            ],
        },
        "input": {
            "r038": {
                "path": str(R038_CERTIFICATE),
                "sha256": R038_EXPECTED_SHA256,
                "sourceCommit": r038_certificate["git"]["commit"],
            }
        },
        "allOrderTheorem": {
            "space": r038_certificate["allOrderTheorem"]["space"],
            "tailHypothesis": (
                "p=sum_(1<=i<=N,q>=-1) p_(i,q) and "
                "h=sum_(j>N,s>=-1) h_(j,s)"
            ),
            "exactMonomialCoefficient": {
                "nonzeroOutputCharge": (
                    "gamma_(i,q;j,s)=(i*s-q*j)*(s-q)/"
                    "(3*(s+q)*(i+j-1))"
                ),
                "zeroOutputCharge": (
                    "gamma_(i,q;j,s)=(i*s-q*j)*(j-i)/"
                    "(3*(i+j)*(i+j-1))"
                ),
                "weightedColumnFactor": "((i+j)/j)*abs(gamma)",
            },
            "finiteChargeBound": (
                "for each -1<=s<S, use its smallest admissible tail degree J_s; "
                "the factors (i+j)/(i+j-1) and 1/j decrease for j>=J_s"
            ),
            "largeChargeClosure": tail["largeChargeSector"]["proof"],
            "inducedNormConclusion": (
                "the supremum of the finite charge-column bounds and the analytic "
                "large-charge bound controls D Phi(p_N) on every uncomputed degree"
            ),
            "quadraticTailBound": "||Phi(h)||_(B_r)<=3||h||_(B_r)^2",
            "transportMonomialFactor": (
                "tau(i,q)=((i+1)/i)*max(i+q,2*i-q)/3"
            ),
            "transportProof": (
                "for an arbitrary transport input, x=s/j lies in [-1,2], so "
                "abs(i*x-q)<=max(i+q,2*i-q) and "
                "(i+j)/(i+j-1)<=(i+1)/i"
            ),
        },
        "chargeResolvedKernel": tail,
        "restartCertificate": {
            "polynomialCutoff": maximum_degree,
            "chargeCutoff": charge_cutoff,
            "targetRadius": r037.rational_record(target_radius),
            "r038Radius": r037.rational_record(previous_radius),
            "r031Radius": r037.rational_record(r031_radius),
            "radiusGainFromR038": r037.rational_record(
                target_radius / previous_radius
            ),
            "radiusGainFromR031": r037.rational_record(
                target_radius / r031_radius
            ),
            "fixedChargeGainFromR038": r037.rational_record(
                (target_radius / previous_radius) ** 3
            ),
            "fixedChargeGainFromR031": r037.rational_record(
                (target_radius / r031_radius) ** 3
            ),
            "degreeEightyPolynomialSha256": r037.polynomial_digest(polynomial),
            "degreeEightyPolynomialTerms": len(polynomial),
            "degreeEightyPolynomialNorm": r037.rational_record(polynomial_norm),
            "oldR038TailLinearizationBound": r037.rational_record(
                old_tail["tailLinearizationBound"]
            ),
            "chargeResolvedTailLinearizationBound": r037.rational_record(
                tail_bound
            ),
            "contractionMargin": r037.rational_record(contraction_margin),
            "exactResidualSha256": r037.polynomial_digest(residual),
            "exactResidualTerms": len(residual),
            "residualDegreeRange": [
                min(residual_degrees),
                max(residual_degrees),
            ],
            "exactResidualNorm": r037.rational_record(residual_norm),
            "ballDivisor": ball_divisor,
            "chosenBallRadius": r037.rational_record(ball_radius),
            "residualAllowance": r037.rational_record(residual_allowance),
            "residualToAllowanceRatio": r037.rational_record(
                residual_norm / residual_allowance
            ),
            "mappingUpperBound": r037.rational_record(mapping_upper_bound),
            "lipschitzUpperBound": r037.rational_record(lipschitz_upper_bound),
            "solutionNormUpperBound": r037.rational_record(
                solution_norm_upper_bound
            ),
            "polynomialTransportNormUpperBound": r037.rational_record(
                polynomial_transport_bound
            ),
            "tailTransportContributionUpperBound": r037.rational_record(
                2 * ball_radius
            ),
            "transportOperatorNormUpperBound": r037.rational_record(
                transport_operator_bound
            ),
            "transportInverseNormUpperBound": r037.rational_record(
                transport_inverse_bound
            ),
            "oldScalarTransportBound": r037.rational_record(
                old_scalar_transport_bound
            ),
            "statement": (
                "there is a unique degree-greater-than-80 active correction; "
                "triangular formal uniqueness identifies it with the canonical "
                "active series, and the charge-resolved transport Neumann bound "
                "constructs canonical U and V at the same radius"
            ),
        },
        "negativeControl": {
            "radius": r037.rational_record(failure_probe_radius),
            "tailLinearizationBound": r037.rational_record(probe_tail_bound),
            "polynomialTransportBound": r037.rational_record(
                probe_polynomial_transport_bound
            ),
            "chosenBallRadius": r037.rational_record(probe_ball_radius),
            "transportOperatorBound": r037.rational_record(
                probe_transport_bound
            ),
            "classification": (
                "failure of the present sufficient transport inequality only; "
                "it is not evidence of nonanalyticity or a singularity"
            ),
        },
        "candidateComparison": {
            "classification": "finite R0.32 diagnostic only",
            "tailTransportCandidateModulusLower": r037.rational_record(
                candidate_fixed_charge_lower
            ),
            "certifiedFixedChargeRadius": r037.rational_record(
                target_radius**3
            ),
            "candidateGapFactorLower": r037.rational_record(
                candidate_gap_factor
            ),
            "meaning": (
                "the finite candidate remains outside the proved disk and is not "
                "certified as a singularity"
            ),
        },
        "finiteRegression": {
            "monomialCoefficientFormula": formula_regression,
            "tailColumns": finite_columns,
            "recurrenceMaximumDegree": maximum_degree,
            "recurrenceOrderedInteractions": recurrence_interactions,
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
        "completed R0.39 charge-resolved certificate",
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


def parse_degree_list(value: str) -> list[int]:
    try:
        degrees = [int(item.strip()) for item in value.split(",") if item.strip()]
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error
    if not degrees:
        raise argparse.ArgumentTypeError("at least one degree is required")
    return degrees


def main() -> None:
    global PROGRESS_LOG
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-total-degree", type=int, default=80)
    parser.add_argument("--target-radius", default="397/2000")
    parser.add_argument("--charge-cutoff", type=int, default=241)
    parser.add_argument("--failure-probe-radius", default="199/1000")
    parser.add_argument(
        "--finite-column-degrees",
        type=parse_degree_list,
        default=parse_degree_list("81,82,160,241"),
    )
    parser.add_argument("--formula-regression-degree", type=int, default=10)
    parser.add_argument("--ball-divisor", type=int, default=1_000_000)
    parser.add_argument("--source-commit")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    if arguments.max_total_degree < 2:
        raise SystemExit("--max-total-degree must be at least 2")
    if arguments.charge_cutoff < 2:
        raise SystemExit("--charge-cutoff must be at least 2")
    if arguments.formula_regression_degree < 1:
        raise SystemExit("--formula-regression-degree must be positive")
    if arguments.ball_divisor <= 6:
        raise SystemExit("--ball-divisor must exceed 6")
    if any(
        item <= arguments.max_total_degree
        for item in arguments.finite_column_degrees
    ):
        raise SystemExit("finite column degrees must exceed the recurrence cutoff")

    target_radius = rational(arguments.target_radius)
    failure_probe_radius = rational(arguments.failure_probe_radius)
    if target_radius <= 0:
        raise SystemExit("--target-radius must be positive")
    if failure_probe_radius <= target_radius:
        raise SystemExit("--failure-probe-radius must exceed the target")

    PROGRESS_LOG = arguments.progress_log
    if PROGRESS_LOG is not None:
        PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG.write_text("", encoding="utf-8")

    payload = build_payload(
        arguments.max_total_degree,
        target_radius,
        arguments.charge_cutoff,
        failure_probe_radius,
        arguments.finite_column_degrees,
        arguments.formula_regression_degree,
        arguments.ball_divisor,
        arguments.progress,
        arguments.source_commit,
    )
    if arguments.check and not all(payload["checks"].values()):
        raise SystemExit("R0.39 checks failed")
    if arguments.output:
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
