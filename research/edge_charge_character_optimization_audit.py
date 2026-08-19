#!/usr/bin/env python3
"""R0.50 exact two-parameter multiplicative charge-character audit.

For the exact degree-80 center from R0.49 and the true input column
(j,s)=(81,162), write

    A(r,c) = sum_(i,q) b_(i,q) r^i c^q,        b_(i,q) >= 0.

The script certifies a unique simultaneous solution of

    A(r,c)=1,
    d A(r,e^t)/dt = 0

inside an exact rational rectangle.  Analytically, every degree is positive,
the charge support contains q=-1 and positive q, and the coefficients are
positive.  Hence A is strictly increasing in r, strictly convex and coercive
in t=log(c), and every fixed-c threshold root exists uniquely.  The isolated
simultaneous solution is therefore the unique global maximizer of the
active-column threshold over all c>0.

Existence in the rectangle is proved by an exact Poincare-Miranda sign box.
The two face polynomials are converted to exact Bernstein form on the complete
face intervals; no floating-point sign decision is used.

The script also constructs coefficientwise lower and upper charge envelopes
on the complete c interval.  It reuses the R0.47 all-order fixed-charge and
large-charge theorems to prove that the same true column dominates all 243
competitors throughout the entire (r,c) rectangle.  Finally it certifies a
Newton/canonical-field restart at the simple rational point

    r=0.382619, c=0.8024563827,

which lies beyond the exact R0.49 threshold for c=4/5.

All claims concern the reduced canonical edge generating system and its
degree-80 exact center.  They do not establish a critical-norm bridge for
arbitrary three-dimensional velocity fields and do not prove or disprove
three-dimensional Navier-Stokes regularity.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time

import gmpy2

import edge_charge_character_weight_audit as r049
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

R049_CERTIFICATE = Path(
    "research/certificates/r049/edge-charge-character-weight.json"
)
R049_EXPECTED_SHA256 = (
    "e36fce33f8a5edeb144cdbeda00a568b972d9a3a8ac0e96c04d7651e71a64578"
)
R049_POLYNOMIAL_SHA256 = (
    "056a0adba7f3cba41a6e9bd6d943a8f59be28f50f44c6035df1f68393ed26be7"
)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.50 +{elapsed:8.2f}s] {stage}{suffix}",
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


def active_laurent_terms(
    terms: list[tuple[int, int, Rational]],
    input_degree: int,
    input_charge: int,
) -> list[tuple[int, int, Rational]]:
    result = []
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
        weighted = coefficient * factor
        if weighted:
            result.append((degree, charge, weighted))
    return result


def threshold_face_polynomial_in_c(
    terms: list[tuple[int, int, Rational]],
    radius: Rational,
) -> Poly:
    """Return c*(A(r,c)-1), a polynomial because min(q)=-1."""

    maximum_charge = max(charge for _, charge, _ in terms)
    result = [Rational(0)] * (maximum_charge + 2)
    for degree, charge, coefficient in terms:
        result[charge + 1] += coefficient * radius**degree
    result[1] -= 1
    return r047.trim(result)


def stationarity_face_polynomial_in_r(
    terms: list[tuple[int, int, Rational]],
    character: Rational,
    maximum_degree: int,
) -> Poly:
    """Return c*d_t A(r,e^t), preserving the sign of d_t A."""

    result = [Rational(0)] * (maximum_degree + 1)
    for degree, charge, coefficient in terms:
        result[degree] += charge * coefficient * character ** (charge + 1)
    return r047.trim(result)


def bernstein_face_certificate(
    poly: Poly,
    lower: Rational,
    upper: Rational,
    expected_sign: int,
    variable: str,
    face: str,
) -> dict[str, object]:
    coefficients = r047.bernstein_coefficients(poly, lower, upper)
    signed = [expected_sign * coefficient for coefficient in coefficients]
    minimum = min(signed)
    maximum = max(signed)
    if minimum <= 0:
        raise AssertionError(f"Bernstein face sign failed on {face}")
    return {
        "face": face,
        "variable": variable,
        "interval": [
            r037.rational_record(lower),
            r037.rational_record(upper),
        ],
        "expectedSign": "+" if expected_sign == 1 else "-",
        "powerDegree": len(poly) - 1,
        "bernsteinDegree": len(coefficients) - 1,
        "coefficientCount": len(coefficients),
        "allSignedBernsteinCoefficientsPositive": True,
        "minimumSignedBernsteinCoefficient": r037.rational_record(minimum),
        "maximumSignedBernsteinCoefficient": r037.rational_record(maximum),
        "powerCoefficientSha256": r047.polynomial_digest(poly),
        "signedBernsteinSha256": r047.polynomial_digest(signed),
        "subdivisionCount": 1,
        "classification": "formal exact complete-face sign certificate",
    }


def charge_envelope(
    polynomial: Polynomial,
    lower_character: Rational,
    upper_character: Rational,
    mode: str,
) -> Polynomial:
    """Coefficientwise charge envelope valid on the complete c interval."""

    if mode not in {"lower", "upper"}:
        raise ValueError("mode must be lower or upper")
    result: Polynomial = {}
    for exponent, coefficient in polynomial.items():
        charge = r039.charge(exponent)
        if mode == "upper":
            character = lower_character if charge < 0 else upper_character
        else:
            character = upper_character if charge < 0 else lower_character
        result[exponent] = coefficient * character**charge
    return result


def corrected_restart(
    scaled_polynomial: Polynomial,
    scaled_residual: Polynomial,
    radius: Rational,
    tail: dict[str, object],
    maximum_degree: int,
    ball_divisor: int,
) -> dict[str, object]:
    restart = r046.block_restart_diagnostics(
        scaled_polynomial,
        scaled_residual,
        radius,
        tail,
        maximum_degree,
        ball_divisor,
        Rational(1),
    )
    unweighted_polynomial = rational(
        restart.pop("twoBlockPolynomialNorm")["exact"]
    )
    unweighted_residual = rational(
        restart.pop("twoBlockResidualNorm")["exact"]
    )
    polynomial_norm = r037.weighted_wiener_norm(scaled_polynomial, radius)
    residual_norm = r037.weighted_wiener_norm(scaled_residual, radius)
    linear_bound = rational(tail["maximumBound"]["exact"])
    margin = 1 - linear_bound
    ball_radius = margin / ball_divisor
    quadratic_constant = Rational(3)
    residual_allowance = (
        margin * ball_radius - quadratic_constant * ball_radius**2
    )
    mapping_upper = (
        residual_norm
        + linear_bound * ball_radius
        + quadratic_constant * ball_radius**2
    )
    lipschitz_upper = linear_bound + 2 * quadratic_constant * ball_radius
    fixed_point = (
        margin > 0
        and residual_norm < residual_allowance
        and mapping_upper < ball_radius
        and lipschitz_upper < 1
    )
    restart.pop("zeroChargeWeight")
    restart.pop("chosenTwoBlockBallRadius")
    restart.pop("ordinaryCorrectionNormUpperBound")
    restart.update(
        {
            "radius": r037.rational_record(radius),
            "chosenAnisotropicBallRadius": r037.rational_record(ball_radius),
            "anisotropicPolynomialNorm": r037.rational_record(polynomial_norm),
            "anisotropicResidualNorm": r037.rational_record(residual_norm),
            "anisotropicCorrectionNormUpperBound": r037.rational_record(
                ball_radius
            ),
            "contractionMargin": r037.rational_record(margin),
            "quadraticConstant": r037.rational_record(quadratic_constant),
            "residualAllowance": r037.rational_record(residual_allowance),
            "mappingUpperBound": r037.rational_record(mapping_upper),
            "lipschitzUpperBound": r037.rational_record(lipschitz_upper),
            "fixedPointPasses": fixed_point,
            "canonicalFieldsPass": fixed_point and restart["stretchPasses"],
            "degreeWeightAudit": {
                "residualUsesTotalDegreeWeight": True,
                "unweightedPolynomialDiagnosticExcludedFromProof": (
                    r037.rational_record(unweighted_polynomial)
                ),
                "unweightedResidualDiagnosticExcludedFromProof": (
                    r037.rational_record(unweighted_residual)
                ),
            },
            "classification": (
                "exact anisotropic fixed-point and conjugated canonical-field "
                "certificate at the rational R0.50 restart point"
            ),
        }
    )
    return restart


def build_payload(
    maximum_degree: int,
    radius_lower: Rational,
    radius_upper: Rational,
    character_lower: Rational,
    character_upper: Rational,
    restart_radius: Rational,
    ball_divisor: int,
    charge_cutoff: int,
    show_progress: bool,
    source_commit: str | None,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "loading pinned R0.49 certificate")
    if sha256(R049_CERTIFICATE) != R049_EXPECTED_SHA256:
        raise AssertionError("R0.49 certificate hash mismatch")
    r049_certificate = json.loads(R049_CERTIFICATE.read_text(encoding="utf-8"))
    if maximum_degree != 80 or charge_cutoff != 241:
        raise AssertionError("R0.50 is pinned to N=80 and S=241")
    if not 0 < radius_lower < radius_upper:
        raise AssertionError("invalid radius box")
    if not 0 < character_lower < character_upper:
        raise AssertionError("invalid character box")
    if radius_upper - radius_lower != Rational(1, 10**15):
        raise AssertionError("R0.50 radius box must have width 10^-15")
    if character_upper - character_lower != Rational(1, 10**10):
        raise AssertionError("R0.50 character box must have width 10^-10")
    if restart_radius != Rational(382619, 1_000_000):
        raise AssertionError("R0.50 restart radius changed")

    previous_root_lower = rational(
        r049_certificate["thresholdTheorem"]["rootIsolation"]["lower"]["exact"]
    )
    previous_root_upper = rational(
        r049_certificate["thresholdTheorem"]["rootIsolation"]["upper"]["exact"]
    )

    progress(show_progress, started, "constructing exact center and residual")
    active_field, _, _, recurrence_interactions = r028.rational_edge_recurrence(
        maximum_degree,
        show_progress,
        started,
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
    if polynomial_digest != R049_POLYNOMIAL_SHA256:
        raise AssertionError("degree-80 polynomial digest changed")

    base_terms = r048.independent_terms(polynomial)
    laurent = active_laurent_terms(base_terms, 81, 162)
    charges = sorted({charge for _, charge, _ in laurent})
    if charges[0] != -1 or charges[-1] != 157:
        raise AssertionError("active charge support changed")
    if not all(degree > 0 and coefficient > 0 for degree, _, coefficient in laurent):
        raise AssertionError("active Laurent positivity failed")

    progress(show_progress, started, "building exact Poincare-Miranda faces")
    p_radius_lower = threshold_face_polynomial_in_c(laurent, radius_lower)
    p_radius_upper = threshold_face_polynomial_in_c(laurent, radius_upper)
    q_character_lower = stationarity_face_polynomial_in_r(
        laurent,
        character_lower,
        maximum_degree,
    )
    q_character_upper = stationarity_face_polynomial_in_r(
        laurent,
        character_upper,
        maximum_degree,
    )
    face_certificates = {
        "radiusLower": bernstein_face_certificate(
            p_radius_lower,
            character_lower,
            character_upper,
            -1,
            "c",
            "r=r_L",
        ),
        "radiusUpper": bernstein_face_certificate(
            p_radius_upper,
            character_lower,
            character_upper,
            1,
            "c",
            "r=r_U",
        ),
        "characterLower": bernstein_face_certificate(
            q_character_lower,
            radius_lower,
            radius_upper,
            -1,
            "r",
            "c=c_L",
        ),
        "characterUpper": bernstein_face_certificate(
            q_character_upper,
            radius_lower,
            radius_upper,
            1,
            "r",
            "c=c_U",
        ),
    }

    progress(show_progress, started, "constructing uniform charge envelopes")
    lower_polynomial = charge_envelope(
        polynomial,
        character_lower,
        character_upper,
        "lower",
    )
    upper_polynomial = charge_envelope(
        polynomial,
        character_lower,
        character_upper,
        "upper",
    )
    lower_terms = r048.independent_terms(lower_polynomial)
    upper_terms = r048.independent_terms(upper_polynomial)
    active_lower_polynomial = r048.exact_column_polynomial(
        lower_terms,
        maximum_degree,
        81,
        162,
        Rational(1),
    )
    progress(show_progress, started, "certifying uniform all-order upper envelope")
    upper_tail = r047.lattice_tail_bound(
        upper_polynomial,
        radius_upper,
        maximum_degree,
        charge_cutoff,
        Rational(1),
    )
    dominance = r049.full_window_competitors(
        upper_terms,
        maximum_degree,
        charge_cutoff,
        radius_lower,
        radius_upper,
        active_lower_polynomial,
        upper_tail,
    )
    minimum_gap = rational(dominance["minimumDominanceGap"]["exact"])
    if minimum_gap <= 0:
        raise AssertionError("uniform rectangle dominance failed")
    dominance["parameterRectangle"] = {
        "radius": [
            r037.rational_record(radius_lower),
            r037.rational_record(radius_upper),
        ],
        "character": [
            r037.rational_record(character_lower),
            r037.rational_record(character_upper),
        ],
    }
    dominance["proof"] = (
        "for q=-1 the lower/upper coefficient envelopes use c_U/c_L; "
        "for q>=0 they use c_L/c_U.  Positivity makes these bounds uniform "
        "on the complete c interval.  Radius monotonicity, all fixed-charge "
        "convex endpoints, and the odd/even large-charge Bernstein theorems "
        "then cover all 243 non-active competitors on the full rectangle"
    )
    dominance["classification"] = (
        "formal exact all-order two-parameter rectangle dominance theorem"
    )

    progress(show_progress, started, "certifying rational optimized restart")
    restart_character = character_lower
    scaled_polynomial = r049.charge_scale(polynomial, restart_character)
    scaled_residual = r049.charge_scale(residual, restart_character)
    restart_tail = r047.lattice_tail_bound(
        scaled_polynomial,
        restart_radius,
        maximum_degree,
        charge_cutoff,
        Rational(1),
    )
    restart = corrected_restart(
        scaled_polynomial,
        scaled_residual,
        restart_radius,
        restart_tail,
        maximum_degree,
        ball_divisor,
    )
    restart["character"] = r037.rational_record(restart_character)
    restart["extendsR049FourFifthsThreshold"] = restart_radius > previous_root_upper
    restart["tailMaximumSector"] = restart_tail["maximumSector"]
    restart["tailLinearizationBound"] = restart_tail["maximumBound"]
    if not restart["canonicalFieldsPass"]:
        raise AssertionError("optimized rational restart failed")

    threshold_gain_lower = radius_lower / previous_root_upper
    fixed_charge_gain_lower = threshold_gain_lower**3
    face_passes = all(
        record["allSignedBernsteinCoefficientsPositive"]
        for record in face_certificates.values()
    )
    large_record = upper_tail["largeChargeLatticeSector"]
    large_passes = (
        large_record["evenEndpoint"]["derivativeCertificate"]
        ["allSignedBernsteinCoefficientsPositive"]
        and large_record["oddEndpoint"]["derivativeCertificate"]
        ["allSignedBernsteinCoefficientsPositive"]
    )

    checks = {
        "r049CertificateHashMatches": True,
        "polynomialDigestMatchesR049": polynomial_digest == R049_POLYNOMIAL_SHA256,
        "allActiveLaurentCoefficientsPositive": all(
            coefficient > 0 for _, _, coefficient in laurent
        ),
        "allActiveDegreesPositive": all(degree > 0 for degree, _, _ in laurent),
        "chargeSupportHasNegativeAndPositiveTerms": (
            min(charges) < 0 < max(charges)
        ),
        "minimumChargeIsMinusOne": min(charges) == -1,
        "activeColumnStrictlyIncreasesInRadius": True,
        "activeColumnStrictlyConvexInLogCharacter": True,
        "activeColumnCoerciveInLogCharacter": True,
        "allFourCompleteFaceBernsteinCertificatesPass": face_passes,
        "poincareMirandaGivesExistenceInBox": face_passes,
        "globalStructureGivesUniqueSimultaneousRoot": face_passes,
        "simultaneousRootIsUniqueGlobalThresholdMaximum": face_passes,
        "optimalRadiusBoxWidthIsOneEminusFifteen": (
            radius_upper - radius_lower == Rational(1, 10**15)
        ),
        "optimalCharacterBoxWidthIsOneEminusTen": (
            character_upper - character_lower == Rational(1, 10**10)
        ),
        "lowerOptimalRadiusExceedsR049UpperRoot": radius_lower > previous_root_upper,
        "lowerOptimalFixedChargeRadiusExceedsR049Upper": fixed_charge_gain_lower > 1,
        "coefficientwiseLowerEnvelopeIsBelowActiveColumn": True,
        "coefficientwiseUpperEnvelopeIsAboveEveryColumn": True,
        "allCompetitorsCoveredOnRectangle": dominance["competitorsCovered"] == 243,
        "uniformRectangleDominanceGapIsPositive": minimum_gap > 0,
        "uniformLargeChargeEvenBernsteinCertificatePasses": (
            large_record["evenEndpoint"]["derivativeCertificate"]
            ["allSignedBernsteinCoefficientsPositive"]
        ),
        "uniformLargeChargeOddBernsteinCertificatePasses": (
            large_record["oddEndpoint"]["derivativeCertificate"]
            ["allSignedBernsteinCoefficientsPositive"]
        ),
        "uniformLargeChargeCertificatePasses": large_passes,
        "restartRadiusExceedsR049UpperRoot": restart_radius > previous_root_upper,
        "restartTailMaximumIsTrueS162Column": restart_tail["maximumSector"] == "162",
        "restartTailPasses": rational(restart_tail["maximumBound"]["exact"]) < 1,
        "restartResidualUsesTotalDegreeWeight": restart["degreeWeightAudit"]
        ["residualUsesTotalDegreeWeight"],
        "optimizedRestartFixedPointPasses": restart["fixedPointPasses"],
        "optimizedRestartCanonicalFieldsPass": restart["canonicalFieldsPass"],
        "noChargeGridBeyondFiniteTheoremList": True,
        "noTailDegreeGridUsed": True,
        "noFloatingPointSignDecision": True,
    }
    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError("R0.50 checks failed: " + ", ".join(failed))

    progress(
        show_progress,
        started,
        "all exact checks passed",
        checks=len(checks),
        competitors=dominance["competitorsCovered"],
    )
    return {
        "schemaVersion": "1.0",
        "scope": {
            "system": "reduced canonical edge generating system",
            "theorem": (
                "unique global optimization of the degree-80 active threshold "
                "within the multiplicative charge-character family, with "
                "all-order tail-input and charge coverage on the isolating box"
            ),
            "notClaimed": [
                "an optimization over all possible Banach norms",
                "an isotropic-bidisc enlargement",
                "a control theorem for arbitrary three-dimensional velocity fields",
                "three-dimensional Navier-Stokes regularity or singularity",
            ],
        },
        "input": {
            "maximumTotalDegree": maximum_degree,
            "chargeCutoff": charge_cutoff,
            "activeInputDegree": 81,
            "activeInputCharge": 162,
            "radiusBox": [
                r037.rational_record(radius_lower),
                r037.rational_record(radius_upper),
            ],
            "characterBox": [
                r037.rational_record(character_lower),
                r037.rational_record(character_upper),
            ],
            "restartRadius": r037.rational_record(restart_radius),
            "restartCharacter": r037.rational_record(restart_character),
            "ballDivisor": ball_divisor,
        },
        "finiteConstruction": {
            "maximumTotalDegree": maximum_degree,
            "centerTerms": len(polynomial),
            "activeLaurentTerms": len(laurent),
            "recurrenceOrderedInteractions": recurrence_interactions,
            "degreeEightyPolynomialSha256": polynomial_digest,
            "chargeRange": [min(charges), max(charges)],
            "distinctCharges": len(charges),
            "negativeChargeTerms": sum(1 for _, q, _ in laurent if q < 0),
            "zeroChargeTerms": sum(1 for _, q, _ in laurent if q == 0),
            "positiveChargeTerms": sum(1 for _, q, _ in laurent if q > 0),
            "classification": "finite exact degree-80 construction",
        },
        "globalOptimizationTheorem": {
            "optimalRadiusLower": r037.rational_record(radius_lower),
            "optimalRadiusUpper": r037.rational_record(radius_upper),
            "optimalCharacterLower": r037.rational_record(character_lower),
            "optimalCharacterUpper": r037.rational_record(character_upper),
            "radiusMidpointDisplay": r037.rational_record(
                (radius_lower + radius_upper) / 2
            ),
            "characterMidpointDisplay": r037.rational_record(
                (character_lower + character_upper) / 2
            ),
            "equations": [
                "A(r,c)-1=0",
                "d A(r,e^t)/dt=sum q*b_iq*r^i*c^q=0",
            ],
            "faceCertificates": face_certificates,
            "existenceProof": (
                "P=c(A-1) is negative/positive on the complete r_L/r_U "
                "faces and Q=c*d_t A is negative/positive on the complete "
                "c_L/c_U faces; exact Poincare-Miranda gives a zero"
            ),
            "globalUniquenessProof": (
                "for each r>0, A(r,e^t) is strictly convex and coercive in t "
                "because the positive Laurent polynomial contains q=-1 and "
                "positive q. Its minimum M(r) is strictly increasing because "
                "every degree is positive. Thus A=1 and d_t A=0 have at most "
                "one solution. Every fixed-c threshold is unique, tends to "
                "zero as c tends to zero or infinity, and any global maximum "
                "must be stationary; the isolated solution is therefore the "
                "unique global threshold maximum"
            ),
            "classification": (
                "formal exact global theorem for the finite degree-80 active "
                "Laurent polynomial"
            ),
        },
        "comparisonWithR049": {
            "r049RootLower": r037.rational_record(previous_root_lower),
            "r049RootUpper": r037.rational_record(previous_root_upper),
            "optimalThresholdGainLowerFactor": r037.rational_record(
                threshold_gain_lower
            ),
            "optimalFixedChargeRadiusGainLowerFactor": r037.rational_record(
                fixed_charge_gain_lower
            ),
            "interpretation": (
                "the extra gain beyond c=4/5 is strict but small; it optimizes "
                "only the multiplicative-character family"
            ),
        },
        "rectangleDominance": dominance,
        "uniformUpperTail": r047.public_tail_record(upper_tail),
        "optimizedRestart": restart,
        "checks": checks,
        "git": r039.git_state(source_commit),
        "computation": {
            "createdUtc": datetime.now(timezone.utc).isoformat(),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "exactBackend": f"gmpy2 {gmpy2.version()} / GMP {gmpy2.mp_version()}",
            "randomness": False,
            "gpu": False,
            "decimalDecisionUse": False,
            "wallSeconds": time.perf_counter() - started,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-total-degree", type=int, default=80)
    parser.add_argument(
        "--radius-lower",
        default="382619813709565/1000000000000000",
    )
    parser.add_argument(
        "--radius-upper",
        default="382619813709566/1000000000000000",
    )
    parser.add_argument(
        "--character-lower",
        default="8024563827/10000000000",
    )
    parser.add_argument(
        "--character-upper",
        default="8024563828/10000000000",
    )
    parser.add_argument("--restart-radius", default="382619/1000000")
    parser.add_argument("--ball-divisor", type=int, default=1_000_000)
    parser.add_argument("--charge-cutoff", type=int, default=241)
    parser.add_argument("--source-commit")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    global PROGRESS_LOG
    PROGRESS_LOG = arguments.progress_log
    if PROGRESS_LOG is not None:
        PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG.write_text("", encoding="utf-8")

    payload = build_payload(
        arguments.max_total_degree,
        rational(arguments.radius_lower),
        rational(arguments.radius_upper),
        rational(arguments.character_lower),
        rational(arguments.character_upper),
        rational(arguments.restart_radius),
        arguments.ball_divisor,
        arguments.charge_cutoff,
        arguments.progress,
        arguments.source_commit,
    )
    if arguments.check:
        failed = [name for name, value in payload["checks"].items() if not value]
        if failed:
            raise SystemExit("failed checks: " + ", ".join(failed))
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
