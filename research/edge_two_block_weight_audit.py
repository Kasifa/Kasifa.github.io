#!/usr/bin/env python3
"""R0.46 exact zero/nonzero-charge two-block tail audit.

R0.45 proved that the exact unweighted input column with charge s=-1 first
fails at radius 372/1000.  Its exceptional q=1 center terms land in output
charge zero, whereas the positive terms that force monotonicity land in the
nonzero-charge block.  This script retains that output correlation by using

    ||f||_(r,kappa) = kappa ||P_0 f||_(B_r) + ||P_nz f||_(B_r),

with kappa=3/4.  For an input column (j,s), every coefficient is multiplied
by its exact output-block weight and divided by the input-block weight.

The all-order proof covers five disjoint sectors.  The s=0 column has zero
charge-zero image and is maximized at j=81.  The weighted s=-1 column is
strictly increasing in t=1/j because the R0.45 negative-derivative bound is
multiplied by kappa<1, so its maximum is the true j=82 column.  The s=1
column uses a uniform termwise bound.  Charges 2 through S-1 retain the
R0.41 endpoint theorem, and s>=S retains the R0.44 common-slope theorem.

An entrywise 2x2 matrix of separate block suprema is also recorded.  Its
Perron bound is too coarse because it combines different worst input
columns.  The successful norm is the exact weighted column supremum, not
the sum of independently maximized block norms.

All threshold decisions use GMP rationals.  Finite column evaluations are
implementation regressions only.  The result concerns the reduced canonical
edge generating system and does not prove regularity or singularity for the
three-dimensional Navier--Stokes equation.
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
import sys
import time

import gmpy2

import edge_charge_resolved_audit as r039
import edge_degree_resolved_tail_audit as r041
import edge_fixed_negative_charge_audit as r045
import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036
import edge_slope_resolved_transport_audit as r040
import edge_stretch_transport_audit as r042
import edge_weighted_restart_audit as r037


Rational = gmpy2.mpq
Polynomial = dict[tuple[int, int], Rational]

R045_CERTIFICATE = Path(
    "research/certificates/r045/edge-fixed-negative-charge.json"
)
R045_EXPECTED_SHA256 = (
    "abc588fb80a140cf78f0558119f50e7a15dce9b2d3fa5219a8b0f9456c8d0b7b"
)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.46 +{elapsed:8.2f}s] {stage}{suffix}",
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


def weighted_two_block_norm(
    polynomial: Polynomial,
    radius: Rational,
    zero_charge_weight: Rational,
) -> Rational:
    """Exact kappa-weighted Wiener norm split by output charge zero."""

    return sum(
        (
            abs(coefficient)
            * radius ** r039.degree(exponent)
            * (
                zero_charge_weight
                if r039.charge(exponent) == 0
                else Rational(1)
            )
            for exponent, coefficient in polynomial.items()
        ),
        Rational(0),
    )


def split_exact_column(
    polynomial: Polynomial,
    radius: Rational,
    input_degree: int,
    input_charge: int,
    zero_charge_weight: Rational,
) -> dict[str, Rational]:
    """Exact weighted column and its two output-block contributions."""

    zero_output = Rational(0)
    nonzero_output = Rational(0)
    for exponent, coefficient in polynomial.items():
        base_degree = r039.degree(exponent)
        base_charge = r039.charge(exponent)
        contribution = (
            Rational(base_degree + input_degree, input_degree)
            * abs(
                r039.monomial_derivative_coefficient(
                    base_degree,
                    base_charge,
                    input_degree,
                    input_charge,
                )
            )
            * abs(coefficient)
            * radius**base_degree
        )
        if base_charge + input_charge == 0:
            zero_output += contribution
        else:
            nonzero_output += contribution
    input_weight = zero_charge_weight if input_charge == 0 else Rational(1)
    weighted_ratio = (
        zero_charge_weight * zero_output + nonzero_output
    ) / input_weight
    return {
        "zeroOutput": zero_output,
        "nonzeroOutput": nonzero_output,
        "weightedRatio": weighted_ratio,
    }


def zero_input_endpoint(
    terms: list[tuple[int, int, Rational]],
    cutoff: int,
    zero_charge_weight: Rational,
) -> dict[str, object]:
    """Exact all-order s=0 endpoint; the q=0 image vanishes."""

    minimum_degree = r039.minimum_tail_degree(0, cutoff)
    nonzero_output = sum(
        (
            weighted_coefficient
            * Rational(
                base_degree + minimum_degree,
                base_degree + minimum_degree - 1,
            )
            * abs(base_charge)
            / 3
            for base_degree, base_charge, weighted_coefficient in terms
            if base_charge != 0
        ),
        Rational(0),
    )
    weighted_ratio = nonzero_output / zero_charge_weight
    return {
        "inputCharge": 0,
        "minimumTailDegree": minimum_degree,
        "zeroOutput": r037.rational_record(Rational(0)),
        "nonzeroOutputAtMinimumDegree": r037.rational_record(nonzero_output),
        "inputBlockWeight": r037.rational_record(zero_charge_weight),
        "bound": r037.rational_record(weighted_ratio),
        "maximumEndpoint": f"j={minimum_degree}",
        "proof": (
            "for s=q=0 the determinant factor vanishes; for q!=0 the exact "
            "column is c_iq (i+j)/(i+j-1)|q|/3, which decreases with j"
        ),
        "classification": "formal all-order exact zero-input endpoint",
    }


def minus_one_weighted_endpoint(
    terms: list[tuple[int, int, Rational]],
    polynomial: Polynomial,
    radius: Rational,
    cutoff: int,
    zero_charge_weight: Rational,
) -> dict[str, object]:
    """Exact all-order weighted s=-1 endpoint at the true degree j=82."""

    minimum_degree = r039.minimum_tail_degree(-1, cutoff)
    upper_t = Rational(1, minimum_degree)
    q_one_terms = [item for item in terms if item[1] == 1]
    negative_derivative = sum(
        (
            coefficient
            * (
                (degree - 1)
                + 2 * degree**2 * upper_t
                + degree**2 * (degree - 1) * upper_t**2
            )
            / 3
            for degree, _charge, coefficient in q_one_terms
        ),
        Rational(0),
    )
    seed = [
        coefficient
        for degree, charge, coefficient in terms
        if degree == 1 and charge == 2
    ]
    if len(seed) != 1:
        raise AssertionError("expected one degree-one q=2 seed")
    seed_derivative = 3 * seed[0]
    derivative_margin = (
        seed_derivative - zero_charge_weight * negative_derivative
    )
    if derivative_margin <= 0:
        raise AssertionError("weighted s=-1 derivative lower bound is not positive")
    endpoint = split_exact_column(
        polynomial,
        radius,
        minimum_degree,
        -1,
        zero_charge_weight,
    )
    return {
        "inputCharge": -1,
        "minimumTailDegree": minimum_degree,
        "inverseDegreeInterval": [
            r037.rational_record(Rational(0)),
            r037.rational_record(upper_t),
        ],
        "zeroChargeWeight": r037.rational_record(zero_charge_weight),
        "qOneTermCount": len(q_one_terms),
        "unweightedQOneDerivativeUpperBound": r037.rational_record(
            negative_derivative
        ),
        "weightedQOneDerivativeUpperBound": r037.rational_record(
            zero_charge_weight * negative_derivative
        ),
        "seedDerivativeLowerBound": r037.rational_record(seed_derivative),
        "fullDerivativeLowerBound": r037.rational_record(derivative_margin),
        "zeroOutputAtMinimumDegree": r037.rational_record(
            endpoint["zeroOutput"]
        ),
        "nonzeroOutputAtMinimumDegree": r037.rational_record(
            endpoint["nonzeroOutput"]
        ),
        "bound": r037.rational_record(endpoint["weightedRatio"]),
        "maximumEndpoint": f"j={minimum_degree}",
        "proof": (
            "q=-1 terms vanish; q=0 and q>=2 terms increase in t=1/j; "
            "only the zero-output q=1 terms decrease and their derivative "
            "is multiplied by kappa. Hence G'_r(t)>=3r-kappa Qhat_r>0"
        ),
        "coefficientSignCancellationUsed": False,
        "finiteDegreeGridUsedInProof": False,
        "classification": "formal all-order weighted fixed-charge theorem",
    }


def plus_one_uniform_bound(
    terms: list[tuple[int, int, Rational]],
    cutoff: int,
    zero_charge_weight: Rational,
) -> dict[str, object]:
    """All-order s=1 bound, weighting only the exceptional q=-1 output."""

    minimum_degree = r039.minimum_tail_degree(1, cutoff)
    zero_output = Rational(0)
    nonzero_output = Rational(0)
    for base_degree, base_charge, weighted_coefficient in terms:
        value = weighted_coefficient * r039.finite_charge_factor(
            base_degree,
            base_charge,
            1,
            minimum_degree,
        )
        if base_charge == -1:
            zero_output += value
        else:
            nonzero_output += value
    weighted_ratio = zero_charge_weight * zero_output + nonzero_output
    return {
        "inputCharge": 1,
        "minimumTailDegree": minimum_degree,
        "zeroOutputTermwiseBound": r037.rational_record(zero_output),
        "nonzeroOutputTermwiseBound": r037.rational_record(nonzero_output),
        "bound": r037.rational_record(weighted_ratio),
        "classification": (
            "formal all-order termwise degree bound; finite columns are "
            "regressions only"
        ),
    }


def coarse_block_matrix(
    terms: list[tuple[int, int, Rational]],
    polynomial: Polynomial,
    radius: Rational,
    cutoff: int,
    finite_records: list[dict[str, object]],
    large_record: dict[str, object],
    zero_record: dict[str, object],
) -> dict[str, object]:
    """Separate block suprema; this deliberately discards column correlation."""

    zero_from_minus = sum(
        (coefficient / 3 for _degree, charge, coefficient in terms if charge == 1),
        Rational(0),
    )
    zero_from_plus = sum(
        (
            coefficient / 3
            for _degree, charge, coefficient in terms
            if charge == -1
        ),
        Rational(0),
    )
    zero_from_nonzero = max(zero_from_minus, zero_from_plus)
    nonzero_from_zero = rational(
        zero_record["nonzeroOutputAtMinimumDegree"]["exact"]
    )

    minimum_minus = r039.minimum_tail_degree(-1, cutoff)
    minus_split = split_exact_column(
        polynomial,
        radius,
        minimum_minus,
        -1,
        Rational(1),
    )
    nonzero_from_minus = minus_split["nonzeroOutput"]
    minimum_plus = r039.minimum_tail_degree(1, cutoff)
    nonzero_from_plus = sum(
        (
            coefficient
            * r039.finite_charge_factor(
                degree,
                charge,
                1,
                minimum_plus,
            )
            for degree, charge, coefficient in terms
            if charge != -1
        ),
        Rational(0),
    )
    finite_maximum = max(
        finite_records,
        key=lambda record: rational(record["bound"]["exact"]),
    )
    finite_value = rational(finite_maximum["bound"]["exact"])
    large_value = rational(large_record["bound"]["exact"])
    nonzero_candidates = [
        ("s=-1", nonzero_from_minus),
        ("s=1", nonzero_from_plus),
        (f"s={finite_maximum['inputCharge']}", finite_value),
        (f"s>={large_record['inputChargeRange'][0]}", large_value),
    ]
    nonzero_source, nonzero_from_nonzero = max(
        nonzero_candidates,
        key=lambda item: item[1],
    )
    determinant_failure = (
        nonzero_from_nonzero
        + zero_from_nonzero * nonzero_from_zero
        - 1
    )
    perron_display = (
        float(nonzero_from_nonzero)
        + math.sqrt(
            float(nonzero_from_nonzero) ** 2
            + 4 * float(zero_from_nonzero) * float(nonzero_from_zero)
        )
    ) / 2
    return {
        "rowOrder": ["zero output", "nonzero output"],
        "columnOrder": ["zero input", "nonzero input"],
        "entries": [
            [
                r037.rational_record(Rational(0)),
                r037.rational_record(zero_from_nonzero),
            ],
            [
                r037.rational_record(nonzero_from_zero),
                r037.rational_record(nonzero_from_nonzero),
            ],
        ],
        "zeroFromNonzeroSource": (
            "s=-1,q=1"
            if zero_from_minus >= zero_from_plus
            else "s=1,q=-1"
        ),
        "nonzeroFromNonzeroSource": nonzero_source,
        "perronRootDisplayOnly": format(perron_display, ".17g"),
        "exactFailureTestDPlusBCMinusOne": r037.rational_record(
            determinant_failure
        ),
        "separateBlockSupremumMatrixFails": determinant_failure > 0,
        "proof": (
            "for M=[[0,B],[C,D]], rho(M)>1 iff D+BC-1>0. "
            "This matrix combines block suprema from different input columns "
            "and is not the correlated weighted-column theorem"
        ),
        "classification": "rigorous but deliberately coarse block majorant",
    }


def two_block_tail_bound(
    polynomial: Polynomial,
    radius: Rational,
    cutoff: int,
    charge_cutoff: int,
    zero_charge_weight: Rational,
) -> dict[str, object]:
    """All-order weighted-column bound over every tail degree and charge."""

    terms = r039.weighted_base_terms(polynomial, radius)
    inherited = r045.fixed_negative_charge_tail_bound(
        polynomial,
        radius,
        cutoff,
        charge_cutoff,
    )
    zero_record = zero_input_endpoint(terms, cutoff, zero_charge_weight)
    minus_record = minus_one_weighted_endpoint(
        terms,
        polynomial,
        radius,
        cutoff,
        zero_charge_weight,
    )
    plus_record = plus_one_uniform_bound(terms, cutoff, zero_charge_weight)
    finite_records = [
        record
        for record in inherited["finiteColumns"]
        if record["inputCharge"] >= 2
    ]
    finite_maximum = max(
        finite_records,
        key=lambda record: rational(record["bound"]["exact"]),
    )
    large_record = inherited["largeChargeSector"]
    candidates = [
        ("0", rational(zero_record["bound"]["exact"])),
        ("-1", rational(minus_record["bound"]["exact"])),
        ("1", rational(plus_record["bound"]["exact"])),
        (
            str(finite_maximum["inputCharge"]),
            rational(finite_maximum["bound"]["exact"]),
        ),
        (
            f">={charge_cutoff}",
            rational(large_record["bound"]["exact"]),
        ),
    ]
    maximum_sector, maximum_value = max(candidates, key=lambda item: item[1])
    digest_input = [(label, value) for label, value in candidates]
    matrix = coarse_block_matrix(
        terms,
        polynomial,
        radius,
        cutoff,
        finite_records,
        large_record,
        zero_record,
    )
    return {
        "zeroChargeWeight": r037.rational_record(zero_charge_weight),
        "zeroInputColumn": zero_record,
        "minusOneColumn": minus_record,
        "plusOneColumn": plus_record,
        "finitePositiveChargeMaximum": finite_maximum,
        "commonSlopeLargeSector": large_record,
        "maximumBound": r037.rational_record(maximum_value),
        "maximumSector": maximum_sector,
        "unweightedR045Bound": inherited["maximumBound"],
        "unweightedR045Sector": inherited["maximumSector"],
        "correlatedSectorDigestSha256": r041.digest_records(digest_input),
        "coarseSeparateBlockMatrix": matrix,
        "proof": (
            "s=0, s=-1, s=1, 2<=s<S, and s>=S are disjoint and exhaustive; "
            "each record is all-order, so their maximum is the induced "
            "two-block weighted-l1 bound over every tail monomial"
        ),
        "classification": (
            "formal all-order correlated two-block weighted-column theorem"
        ),
        "_finiteRecords": finite_records,
    }


def block_restart_diagnostics(
    polynomial: Polynomial,
    residual: Polynomial,
    radius: Rational,
    tail: dict[str, object],
    cutoff: int,
    ball_divisor: int,
    zero_charge_weight: Rational,
) -> dict[str, object]:
    """Newton ball in the two-block norm, then canonical fields in B_r."""

    tail_bound = rational(tail["maximumBound"]["exact"])
    margin = 1 - tail_bound
    ball_radius = margin / ball_divisor if margin > 0 else Rational(0)
    quadratic_constant = Rational(3) / zero_charge_weight**2
    polynomial_norm = weighted_two_block_norm(
        polynomial,
        radius,
        zero_charge_weight,
    )
    residual_norm = weighted_two_block_norm(
        residual,
        radius,
        zero_charge_weight,
    )
    residual_allowance = (
        margin * ball_radius - quadratic_constant * ball_radius**2
    )
    mapping_upper = (
        residual_norm
        + tail_bound * ball_radius
        + quadratic_constant * ball_radius**2
    )
    lipschitz_upper = tail_bound + 2 * quadratic_constant * ball_radius
    ordinary_correction = (
        ball_radius / zero_charge_weight if ball_radius > 0 else Rational(0)
    )
    stretch = r042.stretch_operator_bound(
        polynomial,
        radius,
        cutoff,
        ordinary_correction,
    )
    stretch_bound = rational(stretch["maximumTotalBound"]["exact"])
    rhs = r042.stretch_rhs_bound(polynomial, radius, ordinary_correction)
    rhs_bound = rational(rhs["totalBound"]["exact"])
    stretch_inverse = (
        Rational(1) / (1 - stretch_bound) if stretch_bound < 1 else None
    )
    phi_bound = rhs_bound * stretch_inverse if stretch_inverse is not None else None
    direct_transport = r040.slope_resolved_transport_bound(
        polynomial,
        radius,
        cutoff,
        ordinary_correction,
    )
    direct_transport_bound = rational(
        direct_transport["maximumTotalBound"]["exact"]
    )
    fixed_point = (
        margin > 0
        and ball_radius > 0
        and residual_norm < residual_allowance
        and mapping_upper < ball_radius
        and lipschitz_upper < 1
    )
    return {
        "radius": r037.rational_record(radius),
        "zeroChargeWeight": r037.rational_record(zero_charge_weight),
        "tailLinearizationBound": r037.rational_record(tail_bound),
        "tailMaximumSector": tail["maximumSector"],
        "contractionMargin": r037.rational_record(margin),
        "ballDivisor": ball_divisor,
        "chosenTwoBlockBallRadius": r037.rational_record(ball_radius),
        "twoBlockPolynomialNorm": r037.rational_record(polynomial_norm),
        "twoBlockResidualNorm": r037.rational_record(residual_norm),
        "quadraticConstant": r037.rational_record(quadratic_constant),
        "quadraticProof": (
            "kappa||h||_B<=||h||_kappa and ||Phi(h)||_B<=3||h||_B^2, "
            "hence ||Phi(h)||_kappa<=3 kappa^(-2)||h||_kappa^2"
        ),
        "residualAllowance": r037.rational_record(residual_allowance),
        "mappingUpperBound": r037.rational_record(mapping_upper),
        "lipschitzUpperBound": r037.rational_record(lipschitz_upper),
        "ordinaryCorrectionNormUpperBound": r037.rational_record(
            ordinary_correction
        ),
        "normEquivalence": (
            "kappa||f||_(B_r)<=||f||_(r,kappa)<=||f||_(B_r)"
        ),
        "stretchOperator": stretch,
        "stretchOperatorBound": r037.rational_record(stretch_bound),
        "stretchInverseNormUpperBound": (
            r037.rational_record(stretch_inverse)
            if stretch_inverse is not None
            else None
        ),
        "stretchRightHandSide": rhs,
        "stretchSolutionNormUpperBound": (
            r037.rational_record(phi_bound) if phi_bound is not None else None
        ),
        "directTransportComparison": direct_transport,
        "directTransportBound": r037.rational_record(direct_transport_bound),
        "fixedPointPasses": fixed_point,
        "stretchPasses": stretch_bound < 1,
        "canonicalFieldsPass": fixed_point and stretch_bound < 1,
    }


def finite_column_regression(
    polynomial: Polynomial,
    radius: Rational,
    tail: dict[str, object],
    charge_cutoff: int,
    zero_charge_weight: Rational,
    charges: list[int],
    degree_offsets: list[int],
) -> dict[str, object]:
    """Finite exact columns; no finite scan is used in the proof."""

    finite_by_charge = {
        record["inputCharge"]: record for record in tail["_finiteRecords"]
    }
    records = []
    digest_input = []
    for input_charge in charges:
        minimum_degree = r039.minimum_tail_degree(input_charge, 80)
        if input_charge == -1:
            sector = tail["minusOneColumn"]
        elif input_charge == 0:
            sector = tail["zeroInputColumn"]
        elif input_charge == 1:
            sector = tail["plusOneColumn"]
        elif input_charge < charge_cutoff:
            sector = finite_by_charge[input_charge]
        else:
            sector = tail["commonSlopeLargeSector"]
        sector_bound = rational(sector["bound"]["exact"])
        for offset in degree_offsets:
            input_degree = minimum_degree + offset
            split = split_exact_column(
                polynomial,
                radius,
                input_degree,
                input_charge,
                zero_charge_weight,
            )
            value = split["weightedRatio"]
            if value > sector_bound:
                raise AssertionError("finite two-block column exceeded sector bound")
            records.append(
                {
                    "inputCharge": input_charge,
                    "inputDegree": input_degree,
                    "exactWeightedColumn": r037.rational_record(value),
                    "allOrderSectorBound": r037.rational_record(sector_bound),
                    "belowSectorBound": True,
                }
            )
            digest_input.append((f"{input_charge}:{input_degree}", value))
    return {
        "charges": charges,
        "degreeOffsets": degree_offsets,
        "records": records,
        "columnsChecked": len(records),
        "allBelowSectorBounds": True,
        "exactColumnsSha256": r041.digest_records(digest_input),
        "classification": (
            "finite exact implementation regressions; all-order coverage "
            "comes from the five analytic sectors"
        ),
    }


def public_tail_record(tail: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in tail.items() if not key.startswith("_")}


def build_payload(
    maximum_degree: int,
    entry_radius: Rational,
    rescued_radius: Rational,
    target_radius: Rational,
    failure_probe_radius: Rational,
    zero_charge_weight: Rational,
    charge_cutoff: int,
    regression_charges: list[int],
    regression_degree_offsets: list[int],
    ball_divisor: int,
    show_progress: bool,
    source_commit: str | None,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "loading pinned R0.45 certificate")
    if sha256(R045_CERTIFICATE) != R045_EXPECTED_SHA256:
        raise AssertionError("R0.45 certificate hash mismatch")
    r045_certificate = json.loads(R045_CERTIFICATE.read_text(encoding="utf-8"))
    pinned_entry = rational(
        r045_certificate["restartCertificate"]["radius"]["exact"]
    )
    pinned_rescue = rational(r045_certificate["negativeControl"]["radius"]["exact"])
    pinned_failure = rational(
        r045_certificate["negativeControl"]["tailLinearizationBound"]["exact"]
    )
    if entry_radius != pinned_entry or rescued_radius != pinned_rescue:
        raise AssertionError("R0.46 entry radii must be pinned by R0.45")
    if not entry_radius < rescued_radius <= target_radius < failure_probe_radius:
        raise AssertionError("R0.46 radii are not ordered")
    if not 0 < zero_charge_weight < 1:
        raise AssertionError("zero-charge block weight must lie in (0,1)")

    progress(
        show_progress,
        started,
        "constructing exact degree recurrence",
        maximumDegree=maximum_degree,
    )
    active, _, _, recurrence_interactions = r028.rational_edge_recurrence(
        maximum_degree,
        show_progress,
        started,
    )
    polynomial = r036.field_to_polynomial(active, maximum_degree)
    seed = {(1, 0): Rational(1), (0, 1): Rational(1)}
    progress(show_progress, started, "forming complete polynomial residual")
    residual = r036.add(
        polynomial,
        r036.scale(seed, -1),
        r036.scale(r036.phi(polynomial), -1),
    )
    if r036.truncate(residual, maximum_degree):
        raise AssertionError("degree recurrence has a residual below the cutoff")
    residual_degrees = sorted({r039.degree(exponent) for exponent in residual})

    tails: dict[str, dict[str, object]] = {}
    restarts: dict[str, dict[str, object]] = {}
    for label, radius in (
        ("entry", entry_radius),
        ("rescued", rescued_radius),
        ("target", target_radius),
        ("failureProbe", failure_probe_radius),
    ):
        progress(
            show_progress,
            started,
            "forming correlated two-block tail and restart bounds",
            label=label,
            radius=str(radius),
        )
        tail = two_block_tail_bound(
            polynomial,
            radius,
            maximum_degree,
            charge_cutoff,
            zero_charge_weight,
        )
        tails[label] = tail
        restarts[label] = block_restart_diagnostics(
            polynomial,
            residual,
            radius,
            tail,
            maximum_degree,
            ball_divisor,
            zero_charge_weight,
        )

    progress(show_progress, started, "checking finite exact weighted columns")
    regression = finite_column_regression(
        polynomial,
        target_radius,
        tails["target"],
        charge_cutoff,
        zero_charge_weight,
        regression_charges,
        regression_degree_offsets,
    )

    entry = restarts["entry"]
    rescued = restarts["rescued"]
    target = restarts["target"]
    failure = restarts["failureProbe"]
    entry_tail = rational(entry["tailLinearizationBound"]["exact"])
    rescued_tail = rational(rescued["tailLinearizationBound"]["exact"])
    target_tail = rational(target["tailLinearizationBound"]["exact"])
    failure_tail = rational(failure["tailLinearizationBound"]["exact"])
    target_unweighted = rational(
        tails["target"]["unweightedR045Bound"]["exact"]
    )
    failure_large = rational(
        tails["failureProbe"]["commonSlopeLargeSector"]["bound"]["exact"]
    )
    target_matrix_delta = rational(
        tails["target"]["coarseSeparateBlockMatrix"]
        ["exactFailureTestDPlusBCMinusOne"]["exact"]
    )
    polynomial_digest = r037.polynomial_digest(polynomial)
    residual_digest = r037.polynomial_digest(residual)
    pinned_polynomial_digest = r045_certificate["restartCertificate"]
    pinned_polynomial_digest = pinned_polynomial_digest[
        "degreeEightyPolynomialSha256"
    ]
    pinned_residual_digest = r045_certificate["restartCertificate"]
    pinned_residual_digest = pinned_residual_digest["exactResidualSha256"]

    checks = {
        "r045CertificateHashMatches": True,
        "r045CertifiedRadiusBecomesEntry": entry_radius == pinned_entry,
        "r045FailedProbeBecomesRescuedRadius": rescued_radius == pinned_rescue,
        "r045UnweightedRescuedRadiusFails": pinned_failure > 1,
        "zeroChargeWeightIsThreeQuarters": zero_charge_weight == Rational(3, 4),
        "entryTwoBlockTailPasses": entry_tail < 1,
        "entryCanonicalFieldsPass": entry["canonicalFieldsPass"],
        "rescuedTwoBlockTailPasses": rescued_tail < 1,
        "rescuedCanonicalFieldsPass": rescued["canonicalFieldsPass"],
        "targetExtendsRescuedRadius": target_radius > rescued_radius,
        "targetTwoBlockTailPasses": target_tail < 1,
        "targetUnweightedTailFails": target_unweighted > 1,
        "targetWorstSectorIsLargeCharge": (
            tails["target"]["maximumSector"] == f">={charge_cutoff}"
        ),
        "targetMinusOneDerivativeMarginPositive": (
            rational(
                tails["target"]["minusOneColumn"]
                ["fullDerivativeLowerBound"]["exact"]
            )
            > 0
        ),
        "targetFixedPointPasses": target["fixedPointPasses"],
        "targetStretchPasses": target["stretchPasses"],
        "targetCanonicalFieldsPass": target["canonicalFieldsPass"],
        "targetDirectTransportStillFails": (
            rational(target["directTransportBound"]["exact"]) > 1
        ),
        "targetCoarseBlockMatrixFails": target_matrix_delta > 0,
        "failureProbeIsNextMillesimal": (
            failure_probe_radius - target_radius == Rational(1, 1000)
        ),
        "failureProbeLargeSectorFails": failure_large > 1,
        "failureProbeTwoBlockTailFails": failure_tail > 1,
        "failureProbeWorstSectorIsLargeCharge": (
            tails["failureProbe"]["maximumSector"] == f">={charge_cutoff}"
        ),
        "failureProbeFixedPointFails": not failure["fixedPointPasses"],
        "failureProbePolynomialStretchStillPasses": (
            rational(
                failure["stretchOperator"]["maximumPolynomialBound"]["exact"]
            )
            < 1
        ),
        "finiteWeightedColumnsBelowAllOrderBounds": regression[
            "allBelowSectorBounds"
        ],
        "polynomialDigestMatchesR045": polynomial_digest == pinned_polynomial_digest,
        "residualDigestMatchesR045": residual_digest == pinned_residual_digest,
        "residualStartsAboveCutoff": residual_degrees[0] == maximum_degree + 1,
        "residualEndsAtDoubleCutoff": residual_degrees[-1] == 2 * maximum_degree,
        "chargeCutoffExceedsAllCenterCharges": charge_cutoff > 2 * maximum_degree,
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"R0.46 checks failed: {failed}")

    elapsed = time.perf_counter() - started
    progress(
        show_progress,
        started,
        "all exact checks passed",
        checks=len(checks),
        targetRadius=str(target_radius),
        targetTail=target["tailLinearizationBound"]["exact"],
        failureTail=failure["tailLinearizationBound"]["exact"],
    )
    return {
        "scope": {
            "system": "reduced canonical edge generating system",
            "claim": (
                "all-order correlated two-block weighted-column theorem and "
                "exact common-radius restart at 94/250"
            ),
            "notClaimed": [
                "three-dimensional Navier-Stokes global regularity",
                "finite-time blow-up",
                "a singularity at the failed probe",
                "failure of every possible block norm at the failed probe",
                "an all-order theorem from finite column checks",
                "the true analytic radius of the reduced system",
            ],
        },
        "git": r039.git_state(source_commit),
        "input": {
            "r045": {
                "path": str(R045_CERTIFICATE),
                "sha256": R045_EXPECTED_SHA256,
                "sourceCommit": r045_certificate["git"]["commit"],
            }
        },
        "twoBlockTheorem": {
            "norm": (
                "||f||_(r,kappa)=kappa||P_0 f||_(B_r)+"
                "||P_nonzero f||_(B_r)"
            ),
            "zeroChargeWeight": r037.rational_record(zero_charge_weight),
            "exhaustiveSectors": ["s=0", "s=-1", "s=1", "2<=s<S", "s>=S"],
            "correlationPrinciple": (
                "take the supremum only after the zero and nonzero output "
                "contributions from the same input column are combined"
            ),
            "minusOneDerivativeConclusion": (
                "G'_r(t)>=3r-kappa Qhat_r(1/82)>0; the maximum is j=82"
            ),
            "quadraticConstant": (
                "3/kappa^2 by norm equivalence with the degree-weighted "
                "Wiener algebra"
            ),
            "coefficientSignCancellationUsed": False,
            "finiteDegreeGridUsedInProof": False,
            "classification": "formal all-order two-block theorem",
        },
        "entryControl": {
            **entry,
            "tail": public_tail_record(tails["entry"]),
            "statement": "the R0.45 certified radius remains a strict pass",
        },
        "rescuedControl": {
            **rescued,
            "tail": public_tail_record(tails["rescued"]),
            "r045UnweightedFailure": r045_certificate["negativeControl"]
            ["tailLinearizationBound"],
            "statement": (
                "the first R0.45 failed radius is certified after preserving "
                "zero/nonzero output correlation"
            ),
        },
        "restartCertificate": {
            **target,
            "entryRadius": r037.rational_record(entry_radius),
            "rescuedRadius": r037.rational_record(rescued_radius),
            "radiusGainFromR045": r037.rational_record(target_radius / entry_radius),
            "fixedChargeGainFromR045": r037.rational_record(
                (target_radius / entry_radius) ** 3
            ),
            "polynomialCutoff": maximum_degree,
            "chargeCutoff": charge_cutoff,
            "tail": public_tail_record(tails["target"]),
            "degreeEightyPolynomialTerms": len(polynomial),
            "degreeEightyPolynomialSha256": polynomial_digest,
            "exactResidualTerms": len(residual),
            "exactResidualSha256": residual_digest,
            "residualDegreeRange": [residual_degrees[0], residual_degrees[-1]],
            "statement": (
                "the two-block Banach restart and inherited canonical-stretch "
                "construction certify a, phi, U, and V at radius 94/250"
            ),
        },
        "negativeControl": {
            **failure,
            "tail": public_tail_record(tails["failureProbe"]),
            "classification": (
                "the next millesimal radius fails the inherited common-slope "
                "large-charge bound while polynomial stretch still passes; "
                "this is not evidence of a singularity or of exact-operator "
                "failure"
            ),
        },
        "finiteRegression": {
            "weightedColumns": regression,
            "recurrenceMaximumDegree": maximum_degree,
            "recurrenceOrderedInteractions": recurrence_interactions,
        },
        "checks": checks,
        "computation": {
            "exactBackend": "gmpy2.mpq (GMP rational arithmetic)",
            "decimalDecisionUse": False,
            "randomness": False,
            "wallSeconds": elapsed,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "createdUtc": datetime.now(timezone.utc).isoformat(),
        },
    }


def parse_int_list(value: str) -> list[int]:
    try:
        items = [int(item.strip()) for item in value.split(",") if item.strip()]
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error
    if not items:
        raise argparse.ArgumentTypeError("at least one integer is required")
    return items


def main() -> None:
    global PROGRESS_LOG
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-total-degree", type=int, default=80)
    parser.add_argument("--entry-radius", default="371/1000")
    parser.add_argument("--rescued-radius", default="372/1000")
    parser.add_argument("--target-radius", default="376/1000")
    parser.add_argument("--failure-probe-radius", default="377/1000")
    parser.add_argument("--zero-charge-weight", default="3/4")
    parser.add_argument("--charge-cutoff", type=int, default=241)
    parser.add_argument(
        "--regression-charges",
        type=parse_int_list,
        default=parse_int_list("-1,0,1,2,162,240,241,300"),
    )
    parser.add_argument(
        "--regression-degree-offsets",
        type=parse_int_list,
        default=parse_int_list("0,3,18"),
    )
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
    if arguments.charge_cutoff <= 2 * arguments.max_total_degree:
        raise SystemExit("--charge-cutoff must exceed twice the polynomial cutoff")
    if arguments.ball_divisor <= 6:
        raise SystemExit("--ball-divisor must exceed 6")
    if any(item % 3 for item in arguments.regression_degree_offsets):
        raise SystemExit("degree offsets must be multiples of 3")

    entry_radius = rational(arguments.entry_radius)
    rescued_radius = rational(arguments.rescued_radius)
    target_radius = rational(arguments.target_radius)
    failure_probe_radius = rational(arguments.failure_probe_radius)
    zero_charge_weight = rational(arguments.zero_charge_weight)

    PROGRESS_LOG = arguments.progress_log
    if PROGRESS_LOG is not None:
        PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG.write_text("", encoding="utf-8")

    payload = build_payload(
        arguments.max_total_degree,
        entry_radius,
        rescued_radius,
        target_radius,
        failure_probe_radius,
        zero_charge_weight,
        arguments.charge_cutoff,
        arguments.regression_charges,
        arguments.regression_degree_offsets,
        arguments.ball_divisor,
        arguments.progress,
        arguments.source_commit,
    )
    if arguments.check and not all(payload["checks"].values()):
        raise SystemExit("R0.46 checks failed")
    if arguments.output:
        r039.atomic_json_write(arguments.output, payload, arguments.pretty)
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
