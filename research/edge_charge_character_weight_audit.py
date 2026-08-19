#!/usr/bin/env python3
"""R0.49 exact multiplicative charge-character weight audit.

R0.48 identifies the unique sharp threshold of the current two-block norm.
This audit changes the Banach space rather than tightening the same column
estimate.  For a monomial Z^m W^n with degree i=m+n and charge q=2n-m, set

    ||f||_(r,c) = sum (m+n)|f_mn| r^(m+n) c^(2n-m),   c=4/5.

Equivalently this is the one-total-derivative Wiener norm on the anisotropic
polydisc

    rho_Z = r/c,   rho_W = r*c^2.

The charge weight omega_s=c^s is multiplicative:

    omega_(a+b)=omega_a omega_b.

It therefore preserves convolution exactly.  Since
rho_Z^2 rho_W=r^3, changing c redistributes the two polyradii while preserving
the fixed-charge R=Z^2 W radius at a given r.

For every input charge s, a center term of charge q receives the exact
output/input ratio

    omega_(s+q)/omega_s = c^q.

Thus the weighted induced-column problem is isometric to the ordinary column
problem for the charge-scaled degree-80 center.  The exact R0.47 lattice
endpoint and parity arguments can then be reused without a charge or
tail-degree grid.

The audit proves:

* the active s=162,j=81 column has a globally unique positive threshold;
* the root lies in the exact width-10^-18 interval

  0.382618642388680778 < r_*^(4/5)
                       < 0.382618642388680779;

* throughout [0.382618,0.382619], the same true column dominates all 243
  competitors covered by the all-order lattice theorem;
* at r=0.382618 the anisotropic Newton ball, Lipschitz condition, and
  inherited canonical-stretch construction all close;
* at r=0.382619 the same true column is above one.

This is an anisotropic Banach-algebra theorem for the reduced generating
system.  It does not enlarge the certified isotropic bidisc, prove a theorem
for arbitrary three-dimensional velocity fields, or solve the Navier-Stokes
Millennium Problem.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time

import gmpy2

import edge_charge_degree_lattice_audit as r047
import edge_charge_resolved_audit as r039
import edge_charge_threshold_root_audit as r048
import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036
import edge_two_block_weight_audit as r046
import edge_weighted_restart_audit as r037


Rational = gmpy2.mpq
Polynomial = dict[tuple[int, int], Rational]
Poly = list[Rational]

R048_CERTIFICATE = Path(
    "research/certificates/r048/edge-charge-threshold-root.json"
)
R048_EXPECTED_SHA256 = (
    "246bcfa6623b1050511554312c32e9973b42b620a20ff571a1b5f340041c9af0"
)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.49 +{elapsed:8.2f}s] {stage}{suffix}",
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


def rational(value: str | int | Rational) -> Rational:
    return Rational(value)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def charge_scale(
    polynomial: Polynomial,
    character: Rational,
) -> Polynomial:
    """Apply the exact charge character S_c[Z^m W^n]=c^(2n-m)Z^mW^n."""

    return {
        exponent: coefficient * character ** r039.charge(exponent)
        for exponent, coefficient in polynomial.items()
    }


def active_charge_contributions(
    terms: list[tuple[int, int, Rational]],
    radius: Rational,
    input_degree: int,
    input_charge: int,
) -> dict[str, object]:
    """Group the exact active weighted column by center/output charge."""

    grouped: dict[int, Rational] = defaultdict(lambda: Rational(0))
    term_counts: dict[int, int] = defaultdict(int)
    for degree, charge, coefficient in terms:
        factor = (
            Rational(degree + input_degree, input_degree)
            * abs(
                r039.monomial_derivative_coefficient(
                    degree,
                    charge,
                    input_degree,
                    input_charge,
                )
            )
        )
        grouped[charge] += coefficient * factor * radius**degree
        term_counts[charge] += 1
    total = sum(grouped.values(), Rational(0))
    records = []
    digest_records = []
    for charge in sorted(grouped):
        contribution = grouped[charge]
        records.append(
            {
                "centerCharge": charge,
                "outputCharge": input_charge + charge,
                "centerTermCount": term_counts[charge],
                "contribution": r037.rational_record(contribution),
                "shareOfActiveColumn": r037.rational_record(
                    contribution / total
                ),
            }
        )
        digest_records.append((str(charge), contribution))
    return {
        "inputCharge": input_charge,
        "inputDegree": input_degree,
        "centerChargeRange": [min(grouped), max(grouped)],
        "distinctCenterCharges": len(grouped),
        "total": r037.rational_record(total),
        "records": records,
        "exactContributionDigestSha256": r039.digest_records(digest_records),
    }


def full_window_competitors(
    terms: list[tuple[int, int, Rational]],
    maximum_degree: int,
    charge_cutoff: int,
    window_lower: Rational,
    window_upper: Rational,
    active_column: Poly,
    upper_tail: dict[str, object],
) -> dict[str, object]:
    """Exact monotone sandwich for every non-active all-order sector."""

    active_lower = r047.poly_evaluate(active_column, window_lower)
    fixed_by_charge = {
        record["inputCharge"]: record
        for record in upper_tail["fixedPositiveChargeColumns"]
    }
    if len(fixed_by_charge) != charge_cutoff - 2:
        raise AssertionError("fixed-charge theorem list is incomplete")

    records: list[dict[str, object]] = []
    for input_charge in range(2, charge_cutoff):
        infinity, minimum, degree_floor = (
            r048.fixed_charge_endpoint_polynomials(
                terms,
                maximum_degree,
                input_charge,
            )
        )
        infinity_upper = r047.poly_evaluate(infinity, window_upper)
        minimum_upper = r047.poly_evaluate(minimum, window_upper)
        pinned = rational(fixed_by_charge[input_charge]["bound"]["exact"])
        if max(infinity_upper, minimum_upper) != pinned:
            raise AssertionError(
                f"fixed-charge endpoint mismatch at s={input_charge}"
            )
        if input_charge == 162:
            candidates = [
                (
                    "fixed s=162 inactive x=0 endpoint",
                    infinity_upper,
                    infinity,
                    "x=0",
                )
            ]
        elif infinity_upper >= minimum_upper:
            candidates = [
                (
                    f"fixed s={input_charge}",
                    infinity_upper,
                    infinity,
                    "x=0",
                )
            ]
        else:
            candidates = [
                (
                    f"fixed s={input_charge}",
                    minimum_upper,
                    minimum,
                    "x=s/J_s",
                )
            ]
        for label, upper_bound, endpoint_poly, endpoint_name in candidates:
            records.append(
                {
                    "label": label,
                    "sector": "fixed positive charge",
                    "inputCharge": input_charge,
                    "minimumTailDegree": degree_floor,
                    "endpoint": endpoint_name,
                    "upperBoundAtWindowRight": r037.rational_record(
                        upper_bound
                    ),
                    "gapBelowActiveAtWindowLeft": r037.rational_record(
                        active_lower - upper_bound
                    ),
                    "coefficientCount": len(endpoint_poly),
                    "allCoefficientsNonnegative": r048.all_nonnegative(
                        endpoint_poly
                    ),
                    "coefficientSha256": r047.polynomial_digest(endpoint_poly),
                }
            )

    zero_poly = r048.zero_sector_polynomial(
        terms,
        maximum_degree,
        Rational(1),
    )
    minus_poly = r048.exact_column_polynomial(
        terms,
        maximum_degree,
        82,
        -1,
        Rational(1),
    )
    plus_poly = r048.plus_one_sector_polynomial(
        terms,
        maximum_degree,
        Rational(1),
    )
    for label, key, poly in [
        ("s=0", "zeroInputColumn", zero_poly),
        ("s=-1", "minusOneColumn", minus_poly),
        ("s=1", "plusOneColumn", plus_poly),
    ]:
        if not r048.all_nonnegative(poly):
            raise AssertionError(f"{label} polynomial lost nonnegativity")
        upper_bound = r047.poly_evaluate(poly, window_upper)
        pinned = rational(upper_tail[key]["bound"]["exact"])
        if upper_bound != pinned:
            raise AssertionError(f"{label} upper-tail value mismatch")
        records.append(
            {
                "label": label,
                "sector": label,
                "upperBoundAtWindowRight": r037.rational_record(upper_bound),
                "gapBelowActiveAtWindowLeft": r037.rational_record(
                    active_lower - upper_bound
                ),
                "coefficientCount": len(poly),
                "allCoefficientsNonnegative": True,
                "coefficientSha256": r047.polynomial_digest(poly),
            }
        )

    large_upper = rational(
        upper_tail["largeChargeLatticeSector"]["bound"]["exact"]
    )
    large_record = upper_tail["largeChargeLatticeSector"]
    records.append(
        {
            "label": f"s>={charge_cutoff}",
            "sector": "large positive charge",
            "upperBoundAtWindowRight": r037.rational_record(large_upper),
            "gapBelowActiveAtWindowLeft": r037.rational_record(
                active_lower - large_upper
            ),
            "allExactColumnsMonotoneInRadius": True,
            "rightEndpointAllOrderCertificate": {
                "maximumSource": large_record["maximumSource"],
                "evenDerivativeCertificatePasses": (
                    large_record["evenEndpoint"]["derivativeCertificate"]
                    ["allSignedBernsteinCoefficientsPositive"]
                ),
                "oddDerivativeCertificatePasses": (
                    large_record["oddEndpoint"]["derivativeCertificate"]
                    ["allSignedBernsteinCoefficientsPositive"]
                ),
            },
        }
    )

    values = [
        (
            record["label"],
            rational(record["upperBoundAtWindowRight"]["exact"]),
        )
        for record in records
    ]
    nearest_label, nearest_upper = max(values, key=lambda item: item[1])
    minimum_gap = active_lower - nearest_upper
    return {
        "activeLowerBoundAtWindowLeft": r037.rational_record(active_lower),
        "competitorUpperRadius": r037.rational_record(window_upper),
        "competitorsCovered": len(records),
        "otherFixedPositiveCharges": 238,
        "inactiveEndpointOfActiveCharge": 1,
        "otherExhaustiveChargeSectors": 4,
        "nearestCompetitor": nearest_label,
        "nearestCompetitorUpperBoundAtWindowRight": r037.rational_record(
            nearest_upper
        ),
        "minimumDominanceGap": r037.rational_record(minimum_gap),
        "records": records,
        "competitorBoundDigestSha256": r039.digest_records(values),
        "tailDegreeGridUsed": False,
        "chargeGridBeyondFiniteTheoremListUsed": False,
        "monotoneSandwichProof": (
            "every charge-character weighted column is a nonnegative sum "
            "of powers of r; each competitor on the window is therefore at "
            "most its exact all-order right-endpoint bound, while the active "
            "column is at least its exact left-endpoint value"
        ),
    }


def build_payload(
    maximum_degree: int,
    character: Rational,
    window_lower: Rational,
    window_upper: Rational,
    root_decimal_digits: int,
    charge_cutoff: int,
    ball_divisor: int,
    regression_charges: list[int],
    regression_degree_offsets: list[int],
    show_progress: bool,
    source_commit: str | None,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "loading pinned R0.48 certificate")
    if sha256(R048_CERTIFICATE) != R048_EXPECTED_SHA256:
        raise AssertionError("R0.48 certificate hash mismatch")
    r048_certificate = json.loads(R048_CERTIFICATE.read_text(encoding="utf-8"))
    previous_root_lower = rational(
        r048_certificate["thresholdTheorem"]["rootIsolation"]["lower"]["exact"]
    )
    previous_root_upper = rational(
        r048_certificate["thresholdTheorem"]["rootIsolation"]["upper"]["exact"]
    )
    if character != Rational(4, 5):
        raise AssertionError("R0.49 is pinned to c=4/5")
    if maximum_degree != 80 or charge_cutoff != 241:
        raise AssertionError("R0.49 is pinned to N=80 and S=241")
    if window_lower != Rational(382618, 1_000_000):
        raise AssertionError("R0.49 lower endpoint changed")
    if window_upper != Rational(382619, 1_000_000):
        raise AssertionError("R0.49 upper endpoint changed")
    if window_upper - window_lower != Rational(1, 1_000_000):
        raise AssertionError("R0.49 window is not an adjacent millionth")

    progress(
        show_progress,
        started,
        "constructing exact center and residual",
        maximumDegree=maximum_degree,
    )
    active_field, _, _, recurrence_interactions = (
        r028.rational_edge_recurrence(
            maximum_degree,
            show_progress,
            started,
        )
    )
    polynomial = r036.field_to_polynomial(active_field, maximum_degree)
    seed = {(1, 0): Rational(1), (0, 1): Rational(1)}
    residual = r036.add(
        polynomial,
        r036.scale(seed, -1),
        r036.scale(r036.phi(polynomial), -1),
    )
    if r036.truncate(residual, maximum_degree):
        raise AssertionError("degree recurrence has residual below cutoff")
    polynomial_digest = r037.polynomial_digest(polynomial)
    pinned_digest = r048_certificate["finiteConstruction"][
        "degreeEightyPolynomialSha256"
    ]
    if polynomial_digest != pinned_digest:
        raise AssertionError("degree-80 polynomial digest changed")

    progress(show_progress, started, "applying exact charge character")
    scaled_polynomial = charge_scale(polynomial, character)
    scaled_seed = charge_scale(seed, character)
    scaled_residual = charge_scale(residual, character)
    product_covariance = (
        charge_scale(r036.multiply(polynomial, seed), character)
        == r036.multiply(scaled_polynomial, scaled_seed)
    )
    bracket_covariance = (
        charge_scale(r036.bracket(polynomial, seed), character)
        == r036.bracket(scaled_polynomial, scaled_seed)
    )
    x_minus_y = r036.add(
        r036.euler_x(polynomial),
        r036.scale(r036.euler_y(polynomial), -1),
    )
    scaled_x_minus_y = r036.add(
        r036.euler_x(scaled_polynomial),
        r036.scale(r036.euler_y(scaled_polynomial), -1),
    )
    euler_covariance = (
        charge_scale(x_minus_y, character) == scaled_x_minus_y
    )
    covariance_residual = r036.add(
        scaled_polynomial,
        r036.scale(scaled_seed, -1),
        r036.scale(r036.phi(scaled_polynomial), -1),
    )
    if covariance_residual != scaled_residual:
        raise AssertionError("charge scaling does not commute with Phi")
    terms = r048.independent_terms(scaled_polynomial)

    progress(show_progress, started, "forming active weighted polynomial")
    active_column = r048.exact_column_polynomial(
        terms,
        maximum_degree,
        81,
        162,
        Rational(1),
    )
    fixed_infinity, fixed_minimum, minimum_degree = (
        r048.fixed_charge_endpoint_polynomials(
            terms,
            maximum_degree,
            162,
        )
    )
    if active_column != fixed_minimum or minimum_degree != 81:
        raise AssertionError("active weighted column is not the true endpoint")
    threshold = r048.threshold_polynomial(active_column)
    derivative = r047.poly_derivative(threshold)
    primitive = r048.primitive_integer_polynomial(threshold)
    if threshold[0] != -1:
        raise AssertionError("threshold constant is not -1")
    if not all(coefficient > 0 for coefficient in threshold[1:]):
        raise AssertionError("active weighted polynomial lost positive coefficients")
    if not all(coefficient > 0 for coefficient in derivative):
        raise AssertionError("active weighted derivative lost positivity")
    lower_value = r047.poly_evaluate(active_column, window_lower)
    upper_value = r047.poly_evaluate(active_column, window_upper)

    progress(
        show_progress,
        started,
        "isolating weighted threshold root",
        decimalDigits=root_decimal_digits,
    )
    root_lower, root_upper, bisection_decisions = (
        r048.decimal_root_isolation(
            threshold,
            window_lower,
            window_upper,
            root_decimal_digits,
        )
    )
    lower_sign_value = r047.poly_evaluate(threshold, root_lower)
    upper_sign_value = r047.poly_evaluate(threshold, root_upper)

    progress(show_progress, started, "building exact weighted Sturm sequence")
    sturm = r048.sturm_sequence(threshold)
    sturm_lower = r048.sturm_endpoint_record(sturm, root_lower)
    sturm_upper = r048.sturm_endpoint_record(sturm, root_upper)
    sturm_root_count = (
        sturm_lower["variations"] - sturm_upper["variations"]
    )

    progress(show_progress, started, "certifying both all-order endpoints")
    lower_tail = r047.lattice_tail_bound(
        scaled_polynomial,
        window_lower,
        maximum_degree,
        charge_cutoff,
        Rational(1),
    )
    upper_tail = r047.lattice_tail_bound(
        scaled_polynomial,
        window_upper,
        maximum_degree,
        charge_cutoff,
        Rational(1),
    )
    lower_tail_value = rational(lower_tail["maximumBound"]["exact"])
    upper_tail_value = rational(upper_tail["maximumBound"]["exact"])
    lower_fixed = lower_tail["fixedPositiveChargeMaximum"]
    upper_fixed = upper_tail["fixedPositiveChargeMaximum"]
    if lower_fixed["inputCharge"] != 162 or upper_fixed["inputCharge"] != 162:
        raise AssertionError("active fixed-charge identity changed")
    if lower_tail_value != lower_value or upper_tail_value != upper_value:
        raise AssertionError("all-order tail maximum is not the active column")

    progress(show_progress, started, "certifying full-window dominance")
    dominance = full_window_competitors(
        terms,
        maximum_degree,
        charge_cutoff,
        window_lower,
        window_upper,
        active_column,
        upper_tail,
    )

    progress(show_progress, started, "checking anisotropic Newton restart")
    restart = r046.block_restart_diagnostics(
        scaled_polynomial,
        scaled_residual,
        window_lower,
        lower_tail,
        maximum_degree,
        ball_divisor,
        Rational(1),
    )
    unweighted_polynomial_diagnostic = rational(
        restart.pop("twoBlockPolynomialNorm")["exact"]
    )
    unweighted_residual_diagnostic = rational(
        restart.pop("twoBlockResidualNorm")["exact"]
    )
    anisotropic_polynomial_norm = r037.weighted_wiener_norm(
        scaled_polynomial,
        window_lower,
    )
    anisotropic_residual_norm = r037.weighted_wiener_norm(
        scaled_residual,
        window_lower,
    )
    contraction_margin = 1 - lower_tail_value
    ball_radius = contraction_margin / ball_divisor
    quadratic_constant = Rational(3)
    residual_allowance = (
        contraction_margin * ball_radius
        - quadratic_constant * ball_radius**2
    )
    mapping_upper = (
        anisotropic_residual_norm
        + lower_tail_value * ball_radius
        + quadratic_constant * ball_radius**2
    )
    lipschitz_upper = (
        lower_tail_value + 2 * quadratic_constant * ball_radius
    )
    fixed_point = (
        contraction_margin > 0
        and ball_radius > 0
        and anisotropic_residual_norm < residual_allowance
        and mapping_upper < ball_radius
        and lipschitz_upper < 1
    )
    restart["chosenAnisotropicBallRadius"] = r037.rational_record(ball_radius)
    restart["anisotropicPolynomialNorm"] = r037.rational_record(
        anisotropic_polynomial_norm
    )
    restart["anisotropicResidualNorm"] = r037.rational_record(
        anisotropic_residual_norm
    )
    restart["anisotropicCorrectionNormUpperBound"] = r037.rational_record(
        ball_radius
    )
    restart["contractionMargin"] = r037.rational_record(contraction_margin)
    restart["quadraticConstant"] = r037.rational_record(quadratic_constant)
    restart["residualAllowance"] = r037.rational_record(residual_allowance)
    restart["mappingUpperBound"] = r037.rational_record(mapping_upper)
    restart["lipschitzUpperBound"] = r037.rational_record(lipschitz_upper)
    restart["fixedPointPasses"] = fixed_point
    restart["canonicalFieldsPass"] = fixed_point and restart["stretchPasses"]
    restart.pop("zeroChargeWeight")
    restart.pop("chosenTwoBlockBallRadius")
    restart.pop("ordinaryCorrectionNormUpperBound")
    restart["quadraticProof"] = (
        "S_c is a multiplicative algebra automorphism and the ordinary "
        "Wiener estimate ||Phi(h)||_(B_r)<=3||h||_(B_r)^2 therefore gives "
        "||Phi(h)||_(r,c)<=3||h||_(r,c)^2 exactly"
    )
    restart["normEquivalence"] = (
        "||S_c f||_(B_r)=||f||_(r,c) exactly; no isotropic norm "
        "comparison is used"
    )
    restart["interpretation"] = {
        "chargeCharacter": "c=4/5 is already absorbed into the coefficients",
        "quadraticConstant": (
            "3 because omega_(a+b)=omega_a omega_b gives an exact "
            "multiplicative Wiener algebra"
        ),
        "norm": "ordinary B_r norm of S_c f equals anisotropic ||f||_(r,c)",
        "canonicalTransfer": (
            "S_c commutes with products, the log-canonical bracket, X-Y, L, "
            "and coefficientwise exponentials; the scaled stretch and "
            "canonical fields therefore pull back exactly by S_c^(-1)"
        ),
    }
    restart["classification"] = (
        "exact anisotropic fixed-point and conjugated canonical-stretch "
        "certificate for the reduced generating system"
    )
    restart["degreeWeightAudit"] = {
        "definition": (
            "||f||_(r,c)=sum_(m+n>0) "
            "(m+n)|f_mn|r^(m+n)c^(2n-m)"
        ),
        "unweightedPolynomialDiagnosticExcludedFromProof": (
            r037.rational_record(unweighted_polynomial_diagnostic)
        ),
        "unweightedResidualDiagnosticExcludedFromProof": (
            r037.rational_record(unweighted_residual_diagnostic)
        ),
        "residualUsesTotalDegreeWeight": True,
    }

    progress(show_progress, started, "checking finite exact regressions")
    regression = r047.finite_column_regression(
        scaled_polynomial,
        window_lower,
        lower_tail,
        Rational(1),
        charge_cutoff,
        regression_charges,
        regression_degree_offsets,
    )
    contributions = active_charge_contributions(
        terms,
        window_lower,
        81,
        162,
    )

    rho_z = window_lower / character
    rho_w = window_lower * character**2
    fixed_charge_radius = rho_z**2 * rho_w
    previous_fixed_charge_upper = previous_root_upper**3
    fixed_charge_gain_lower = (
        fixed_charge_radius / previous_fixed_charge_upper
    )
    minimum_gap = rational(dominance["minimumDominanceGap"]["exact"])
    lower_large = rational(
        lower_tail["largeChargeLatticeSector"]["bound"]["exact"]
    )
    upper_large = rational(
        upper_tail["largeChargeLatticeSector"]["bound"]["exact"]
    )

    checks = {
        "r048CertificateHashMatches": True,
        "weightIsPinnedFourFifths": character == Rational(4, 5),
        "weightIsExactMultiplicativeCharacter": True,
        "anisotropicProductIdentityIsExact": fixed_charge_radius == window_lower**3,
        "chargeScalingPreservesProductsOnExactCenter": product_covariance,
        "chargeScalingPreservesBracketOnExactCenter": bracket_covariance,
        "chargeScalingCommutesWithXMinusYOnExactCenter": euler_covariance,
        "chargeScalingCommutesWithPhi": covariance_residual == scaled_residual,
        "restartResidualUsesTotalDegreeWeight": (
            anisotropic_residual_norm
            >= Rational(maximum_degree + 1) * unweighted_residual_diagnostic
        ),
        "polynomialDigestMatchesR048": polynomial_digest == pinned_digest,
        "newWindowIsAbovePreviousExactThreshold": (
            window_lower > previous_root_upper
        ),
        "activeColumnIsTrueS162J81": (
            active_column == fixed_minimum and minimum_degree == 81
        ),
        "thresholdConstantIsMinusOne": threshold[0] == -1,
        "allEightyNonconstantCoefficientsPositive": (
            len(threshold) == 81
            and all(coefficient > 0 for coefficient in threshold[1:])
        ),
        "derivativePositiveOnPositiveAxis": all(
            coefficient > 0 for coefficient in derivative
        ),
        "windowLowerPasses": lower_tail_value < 1,
        "windowUpperFailsOnTrueColumn": upper_tail_value > 1,
        "bothEndpointMaximaAreS162": (
            lower_tail["maximumSector"] == "162"
            and upper_tail["maximumSector"] == "162"
        ),
        "largeChargeSectorPassesAtBothEndpoints": (
            lower_large < 1 and upper_large < 1
        ),
        "bothEvenBernsteinCertificatesPass": (
            lower_tail["largeChargeLatticeSector"]["evenEndpoint"]
            ["derivativeCertificate"]
            ["allSignedBernsteinCoefficientsPositive"]
            and upper_tail["largeChargeLatticeSector"]["evenEndpoint"]
            ["derivativeCertificate"]
            ["allSignedBernsteinCoefficientsPositive"]
        ),
        "bothOddBernsteinCertificatesPass": (
            lower_tail["largeChargeLatticeSector"]["oddEndpoint"]
            ["derivativeCertificate"]
            ["allSignedBernsteinCoefficientsPositive"]
            and upper_tail["largeChargeLatticeSector"]["oddEndpoint"]
            ["derivativeCertificate"]
            ["allSignedBernsteinCoefficientsPositive"]
        ),
        "decimalRootSignsAreStrict": (
            lower_sign_value < 0 < upper_sign_value
        ),
        "rootBracketHasRequestedWidth": (
            root_upper - root_lower
            == Rational(1, 10**root_decimal_digits)
        ),
        "sturmCountsExactlyOneRoot": sturm_root_count == 1,
        "noSturmEndpointZeros": (
            sturm_lower["zeroValues"] == 0
            and sturm_upper["zeroValues"] == 0
        ),
        "allCompetitorsCovered": dominance["competitorsCovered"] == 243,
        "fullWindowDominanceGapIsPositive": minimum_gap > 0,
        "finiteExactRegressionsPass": regression["allBelowSectorBounds"],
        "anisotropicFixedPointPasses": restart["fixedPointPasses"],
        "anisotropicStretchPasses": restart["stretchPasses"],
        "anisotropicCanonicalFieldsPass": restart["canonicalFieldsPass"],
        "fixedChargeRadiusGainIsStrict": fixed_charge_gain_lower > 1,
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"R0.49 checks failed: {failed}")

    elapsed = time.perf_counter() - started
    progress(
        show_progress,
        started,
        "all exact checks passed",
        checks=len(checks),
        rootLower=str(root_lower),
        rootUpper=str(root_upper),
        competitors=dominance["competitorsCovered"],
        nearestCompetitor=dominance["nearestCompetitor"],
        fixedPoint=restart["fixedPointPasses"],
    )
    return {
        "scope": {
            "system": "reduced canonical edge generating system",
            "norm": (
                "||f||_(r,c)=sum (m+n)|f_mn| "
                "r^(m+n)c^(2n-m), c=4/5"
            ),
            "equivalentPolydisc": (
                "rho_Z=r/c, rho_W=r*c^2, rho_Z^2*rho_W=r^3"
            ),
            "claim": (
                "exact anisotropic multiplicative-charge-character restart "
                "and unique sharp threshold on the adjacent millionth window"
            ),
            "notClaimed": [
                "a larger isotropic bidisc",
                "optimality among all charge-diagonal weights",
                "optimality of c=4/5",
                "three-dimensional Navier-Stokes global regularity",
                "finite-time blow-up",
                "a PDE singularity at the weighted norm threshold",
                "control of arbitrary smooth three-dimensional initial data",
            ],
        },
        "git": r039.git_state(source_commit),
        "input": {
            "r048": {
                "path": str(R048_CERTIFICATE),
                "sha256": R048_EXPECTED_SHA256,
                "sourceCommit": r048_certificate["git"]["commit"],
                "previousRootLower": r037.rational_record(previous_root_lower),
                "previousRootUpper": r037.rational_record(previous_root_upper),
            }
        },
        "chargeCharacter": {
            "definition": "omega_s=c^s",
            "c": r037.rational_record(character),
            "multiplicativeIdentity": "omega_(a+b)=omega_a*omega_b",
            "columnSimilarityRatio": "omega_(s+q)/omega_s=c^q",
            "algebraConstant": "1",
            "selectionStatus": (
                "simple rational candidate selected after finite exploratory "
                "balancing; no optimality claim"
            ),
            "chargeScaledPolynomialSha256": r037.polynomial_digest(
                scaled_polynomial
            ),
            "chargeScaledResidualSha256": r037.polynomial_digest(
                scaled_residual
            ),
            "finiteCovarianceRegression": (
                "S_c[p-Z-W-Phi(p)] equals "
                "S_c[p]-S_c[Z+W]-Phi(S_c[p]) exactly"
            ),
            "canonicalStretchConjugacy": {
                "productCovarianceOnExactCenter": product_covariance,
                "bracketCovarianceOnExactCenter": bracket_covariance,
                "xMinusYCovarianceOnExactCenter": euler_covariance,
                "formalProof": (
                    "charge is additive under multiplication and the "
                    "log-canonical bracket; S_c also commutes with X, Y, L, "
                    "and coefficientwise exponentials, so the complete "
                    "stretch equation and U,V reconstruction are conjugate"
                ),
            },
        },
        "anisotropicGeometry": {
            "targetRadius": r037.rational_record(window_lower),
            "rhoZ": r037.rational_record(rho_z),
            "rhoW": r037.rational_record(rho_w),
            "rhoZSquaredTimesRhoW": r037.rational_record(
                fixed_charge_radius
            ),
            "targetRadiusCubed": r037.rational_record(window_lower**3),
            "previousThresholdFixedChargeRadiusUpper": r037.rational_record(
                previous_fixed_charge_upper
            ),
            "certifiedFixedChargeRadiusGainLowerFactor": r037.rational_record(
                fixed_charge_gain_lower
            ),
            "interpretation": (
                "the fixed-charge R=Z^2W disk grows because its radius is "
                "rho_Z^2 rho_W=r^3; the smaller polyradius rho_W means this "
                "is not an isotropic-bidisc enlargement"
            ),
        },
        "thresholdTheorem": {
            "window": {
                "lower": r037.rational_record(window_lower),
                "upper": r037.rational_record(window_upper),
                "width": r037.rational_record(window_upper - window_lower),
            },
            "activeColumn": {
                "inputCharge": 162,
                "inputDegree": 81,
                "isTrueInducedColumn": True,
                "coefficientCount": len(active_column),
                "coefficientSha256": r047.polynomial_digest(active_column),
                "allNonconstantCoefficientsPositive": True,
                "valueAtWindowLower": r037.rational_record(lower_value),
                "valueAtWindowUpper": r037.rational_record(upper_value),
                "chargeDistribution": contributions,
            },
            "polynomial": {
                "definition": "P_c(r)=C_(r,c)(81,162)-1",
                "degree": len(threshold) - 1,
                "rationalCoefficientSha256": r047.polynomial_digest(
                    threshold
                ),
                "primitiveIntegerCoefficientSha256": r048.coefficient_digest(
                    primitive
                ),
                "primitiveIntegerCoefficientsAscending": [
                    str(coefficient) for coefficient in primitive
                ],
                "primitiveCoefficientCount": len(primitive),
                "primitiveMaximumCoefficientDigits": max(
                    len(str(abs(coefficient))) for coefficient in primitive
                ),
                "derivativePositiveForEveryPositiveRadius": True,
                "positiveRootIsGloballyUnique": True,
            },
            "rootIsolation": {
                "lower": r037.rational_record(root_lower),
                "upper": r037.rational_record(root_upper),
                "width": r037.rational_record(root_upper - root_lower),
                "display": (
                    "0.382618642388680778 < r_*^(4/5) < "
                    "0.382618642388680779"
                ),
                "midpointDisplayOnly": r048.terminating_decimal(
                    (root_lower + root_upper) / 2,
                    root_decimal_digits + 1,
                ),
                "lowerPolynomialValue": r037.rational_record(
                    lower_sign_value
                ),
                "upperPolynomialValue": r037.rational_record(
                    upper_sign_value
                ),
                "exactBisectionDecisions": bisection_decisions,
                "floatingPointSignDecisionUsed": False,
            },
            "sturmCertificate": {
                "sequenceLength": len(sturm),
                "degrees": [len(poly) - 1 for poly in sturm],
                "lowerEndpoint": sturm_lower,
                "upperEndpoint": sturm_upper,
                "rootCount": sturm_root_count,
                "polynomialSha256BySequenceIndex": [
                    r047.polynomial_digest(poly) for poly in sturm
                ],
                "classification": "formal exact Sturm root-count certificate",
            },
            "fullWindowDominance": dominance,
            "conclusion": {
                "belowRoot": (
                    "on [0.382618,r_*^(4/5)) the full weighted induced norm "
                    "equals the active true column and is below one"
                ),
                "atRoot": (
                    "at r_*^(4/5) the full weighted induced norm equals one"
                ),
                "aboveRoot": (
                    "on (r_*^(4/5),0.382619] the same true column exceeds "
                    "one, so this weighted sufficient contraction criterion "
                    "fails"
                ),
                "classification": (
                    "formal local sharp-threshold theorem for the c=4/5 "
                    "multiplicative charge-character norm"
                ),
            },
        },
        "endpointCertificates": {
            "lower": r047.public_tail_record(lower_tail),
            "upper": r047.public_tail_record(upper_tail),
        },
        "restartCertificate": restart,
        "finiteRegression": regression,
        "finiteConstruction": {
            "degreeEightyPolynomialTerms": len(polynomial),
            "degreeEightyPolynomialSha256": polynomial_digest,
            "degreeEightyScaledPolynomialTerms": len(scaled_polynomial),
            "recurrenceOrderedInteractions": recurrence_interactions,
            "classification": (
                "finite exact center and covariance regression; tail charge "
                "and degree coverage is all-order"
            ),
        },
        "checks": checks,
        "computation": {
            "exactBackend": "gmpy2.mpq/mpz (GMP rational and integer arithmetic)",
            "decimalDecisionUse": False,
            "randomness": False,
            "gpu": False,
            "wallSeconds": elapsed,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "createdUtc": datetime.now(timezone.utc).isoformat(),
        },
    }


def main() -> None:
    global PROGRESS_LOG
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-total-degree", type=int, default=80)
    parser.add_argument("--charge-character", default="4/5")
    parser.add_argument("--window-lower", default="382618/1000000")
    parser.add_argument("--window-upper", default="382619/1000000")
    parser.add_argument("--root-decimal-digits", type=int, default=18)
    parser.add_argument("--charge-cutoff", type=int, default=241)
    parser.add_argument("--ball-divisor", type=int, default=1_000_000)
    parser.add_argument(
        "--regression-charges",
        default="-1,0,1,2,162,164,240,241,242,300",
    )
    parser.add_argument("--regression-degree-offsets", default="0,3,18")
    parser.add_argument("--source-commit")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    if arguments.max_total_degree != 80:
        raise SystemExit("R0.49 is pinned to --max-total-degree 80")
    if arguments.charge_cutoff != 241:
        raise SystemExit("R0.49 is pinned to --charge-cutoff 241")
    if arguments.root_decimal_digits < 7:
        raise SystemExit("--root-decimal-digits must be at least 7")
    if arguments.ball_divisor <= 0:
        raise SystemExit("--ball-divisor must be positive")

    charges = [
        int(value) for value in arguments.regression_charges.split(",")
    ]
    offsets = [
        int(value)
        for value in arguments.regression_degree_offsets.split(",")
    ]
    PROGRESS_LOG = arguments.progress_log
    if PROGRESS_LOG is not None:
        PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG.write_text("", encoding="utf-8")

    payload = build_payload(
        arguments.max_total_degree,
        rational(arguments.charge_character),
        rational(arguments.window_lower),
        rational(arguments.window_upper),
        arguments.root_decimal_digits,
        arguments.charge_cutoff,
        arguments.ball_divisor,
        charges,
        offsets,
        arguments.progress,
        arguments.source_commit,
    )
    if arguments.check and not all(payload["checks"].values()):
        raise SystemExit("R0.49 checks failed")
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
