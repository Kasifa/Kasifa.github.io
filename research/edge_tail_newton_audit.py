#!/usr/bin/env python3
"""R0.38 exact tail-aware Newton restart and low-block preconditioner audit.

R0.37 bounded the derivative on the full weighted Wiener space by

    ||D Phi(p) h|| <= 6 ||p|| ||h||.

For a degree-N polynomial p and a correction h supported strictly above
degree N, the degree supports are disjoint.  The same all-order mixed-layer
inequality then gives the sharper bound

    ||D Phi(p) h|| <= Z_N(r) ||h||,
    Z_N(r) = 3 (M_N(r) + S_N(r)/(N+1)),

where

    M_N(r) = sum_i i A_i r^i,
    S_N(r) = sum_i i^2 A_i r^i.

The audit uses N=80 and r=59/500.  All decision quantities are exact GMP
rationals.  A finite degree-12 inverse and degree-81 tail-column scan are
regressions only.  The infinite-dimensional result follows from the
degree-support argument and the all-order mixed-layer inequality.

The exact low block is also audited as a proposed preconditioner.  Grading
shows that it acts as the identity on the degree-greater-than-N correction
space, so it does not reduce the tail defect.  The radius gain comes from
the tail-aware all-order estimate, not from extrapolating the finite inverse.

This concerns the reduced edge generating equation.  It is not a regularity
or blow-up result for the full three-dimensional Navier--Stokes equation.
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


Rational = gmpy2.mpq
Exponent = tuple[int, int]
Polynomial = dict[Exponent, Rational]

R032_CERTIFICATE = Path(
    "research/certificates/r032/edge-singularity-candidates.json"
)
R037_CERTIFICATE = Path(
    "research/certificates/r037/edge-weighted-restart.json"
)
R032_EXPECTED_SHA256 = (
    "bd70ed05779631b729e89c269f82d287da361fdcea34e3c42703a712222f5575"
)
R037_EXPECTED_SHA256 = (
    "a4fe36192b80112c282b9388da65ffca625f7a84d0b64f294b24352f92870eda"
)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.38 +{elapsed:8.2f}s] {stage}{suffix}",
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


def layer_l1(polynomial: Polynomial) -> dict[int, Rational]:
    layers: dict[int, Rational] = {}
    for exponent, value in polynomial.items():
        total_degree = degree(exponent)
        layers[total_degree] = layers.get(total_degree, Rational(0)) + abs(value)
    return layers


def tail_linearization_quantities(
    polynomial: Polynomial,
    radius: Rational,
    cutoff: int,
) -> dict[str, Rational]:
    """Exact quantities in the all-order high-tail derivative bound."""

    layers = layer_l1(polynomial)
    weighted_norm = sum(
        (
            total_degree * coefficient_l1 * radius**total_degree
            for total_degree, coefficient_l1 in layers.items()
        ),
        Rational(0),
    )
    degree_moment = sum(
        (
            total_degree**2 * coefficient_l1 * radius**total_degree
            for total_degree, coefficient_l1 in layers.items()
        ),
        Rational(0),
    )
    tail_bound = 3 * (
        weighted_norm + degree_moment / Rational(cutoff + 1)
    )
    return {
        "weightedNorm": weighted_norm,
        "degreeMoment": degree_moment,
        "tailLinearizationBound": tail_bound,
        "oldFullSpaceLinearizationBound": 6 * weighted_norm,
    }


def finite_tail_column_audit(
    polynomial: Polynomial,
    radius: Rational,
    cutoff: int,
    input_degree: int,
    all_order_bound: Rational,
) -> dict[str, object]:
    """Finite exact columns; the all-order proof does not depend on this scan."""

    if input_degree <= cutoff:
        raise ValueError("tail-column input degree must exceed the cutoff")
    basis = [
        (input_degree - w_degree, w_degree)
        for w_degree in range(input_degree + 1)
        if 3 * w_degree - input_degree >= -1
    ]
    maximum_ratio = Rational(0)
    maximum_exponent: Exponent | None = None
    total_image_terms = 0
    minimum_output_degree: int | None = None
    maximum_output_degree: int | None = None
    low_projection_terms = 0

    input_weight = input_degree * radius**input_degree
    for exponent in basis:
        image = r036.dphi(polynomial, {exponent: Rational(1)})
        total_image_terms += len(image)
        image_degrees = [degree(output_exponent) for output_exponent in image]
        if image_degrees:
            current_minimum = min(image_degrees)
            current_maximum = max(image_degrees)
            minimum_output_degree = (
                current_minimum
                if minimum_output_degree is None
                else min(minimum_output_degree, current_minimum)
            )
            maximum_output_degree = (
                current_maximum
                if maximum_output_degree is None
                else max(maximum_output_degree, current_maximum)
            )
        low_projection_terms += sum(
            degree(output_exponent) <= cutoff for output_exponent in image
        )
        if any(charge(output_exponent) < -1 for output_exponent in image):
            raise AssertionError("tail derivative left the active support cone")
        ratio = r037.weighted_wiener_norm(image, radius) / input_weight
        if ratio > maximum_ratio:
            maximum_ratio = ratio
            maximum_exponent = exponent

    if maximum_ratio > all_order_bound:
        raise AssertionError("finite tail column exceeded the all-order bound")
    if low_projection_terms:
        raise AssertionError("the low projection of a high-tail derivative is nonzero")

    return {
        "classification": (
            "finite exact regression only; the infinite tail bound follows "
            "from disjoint degree support and the all-order mixed-layer inequality"
        ),
        "inputDegree": input_degree,
        "admissibleColumns": len(basis),
        "totalImageTerms": total_image_terms,
        "minimumOutputDegree": minimum_output_degree,
        "maximumOutputDegree": maximum_output_degree,
        "lowProjectionTerms": low_projection_terms,
        "maximumWeightedColumnRatio": r037.rational_record(maximum_ratio),
        "maximumColumnExponent": list(maximum_exponent or ()),
        "ratioToAllOrderBound": r037.rational_record(
            maximum_ratio / all_order_bound
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
    target_radius: Rational,
    low_block_degree: int,
    tail_column_degree: int,
    show_progress: bool,
    source_commit: str | None,
) -> dict[str, object]:
    started = time.perf_counter()
    progress(show_progress, started, "loading pinned R0.32 and R0.37 certificates")
    if sha256(R032_CERTIFICATE) != R032_EXPECTED_SHA256:
        raise AssertionError("R0.32 certificate hash mismatch")
    if sha256(R037_CERTIFICATE) != R037_EXPECTED_SHA256:
        raise AssertionError("R0.37 certificate hash mismatch")
    r032_certificate = json.loads(R032_CERTIFICATE.read_text(encoding="utf-8"))
    r037_certificate = json.loads(R037_CERTIFICATE.read_text(encoding="utf-8"))

    previous_radius = rational(
        r037_certificate["restartCertificate"]["targetRadius"]["exact"]
    )
    r031_radius = rational(
        r037_certificate["restartCertificate"]["r031Radius"]["exact"]
    )
    if target_radius <= previous_radius:
        raise AssertionError("R0.38 target must exceed the R0.37 radius")

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

    progress(show_progress, started, "forming exact tail contraction inequalities")
    tail = tail_linearization_quantities(
        polynomial,
        target_radius,
        maximum_degree,
    )
    failure_probe_radius = Rational(19, 160)
    failure_probe_tail = tail_linearization_quantities(
        polynomial,
        failure_probe_radius,
        maximum_degree,
    )
    polynomial_norm = tail["weightedNorm"]
    degree_moment = tail["degreeMoment"]
    tail_linearization_bound = tail["tailLinearizationBound"]
    old_full_space_bound = tail["oldFullSpaceLinearizationBound"]
    residual_norm = r037.weighted_wiener_norm(residual, target_radius)
    contraction_margin = 1 - tail_linearization_bound
    ball_radius = contraction_margin / 12
    residual_allowance = contraction_margin**2 / 16
    mapping_upper_bound = (
        residual_norm
        + tail_linearization_bound * ball_radius
        + 3 * ball_radius**2
    )
    lipschitz_upper_bound = tail_linearization_bound + 6 * ball_radius
    solution_norm_upper_bound = polynomial_norm + ball_radius
    transport_operator_bound = 2 * solution_norm_upper_bound
    transport_inverse_bound = 1 / (1 - transport_operator_bound)

    progress(
        show_progress,
        started,
        "auditing exact low block",
        maximumDegree=low_block_degree,
    )
    finite_low_block = r037.finite_jacobian_audit(
        polynomial,
        low_block_degree,
        {"targetRadius": target_radius},
    )
    previous_low_block = r037_certificate["finiteRegression"]["jacobian"]
    low_block_hashes_match = (
        finite_low_block["jacobianSha256"]
        == previous_low_block["jacobianSha256"]
        and finite_low_block["inverseSha256"]
        == previous_low_block["inverseSha256"]
    )
    if not low_block_hashes_match:
        raise AssertionError("the pinned degree-12 low block changed")

    progress(
        show_progress,
        started,
        "auditing finite tail columns",
        inputDegree=tail_column_degree,
    )
    finite_tail_columns = finite_tail_column_audit(
        polynomial,
        target_radius,
        maximum_degree,
        tail_column_degree,
        tail_linearization_bound,
    )

    candidate_fixed_charge_lower = -rational(
        r032_certificate["diagnostic"]["tailTransportClusterHull"]["upper"]
    )
    candidate_gap_factor = (
        candidate_fixed_charge_lower / target_radius**3
    )

    checks = {
        "pinnedInputHashes": True,
        "activeSupportConePreserved": all(
            charge(exponent) >= -1 for exponent in polynomial
        ),
        "originRecurrenceThroughCutoff": not low_residual,
        "residualBeginsAboveCutoff": min(residual_degrees) > maximum_degree,
        "residualEndsAtTwiceCutoff": max(residual_degrees) <= 2 * maximum_degree,
        "targetRadiusExceedsR037": target_radius > previous_radius,
        "oldFullSpaceBoundFailsAtTarget": old_full_space_bound > 1,
        "tailLinearizationBoundBelowOne": tail_linearization_bound < 1,
        "nearbyFailureProbeDoesNotClose": (
            failure_probe_radius > target_radius
            and failure_probe_tail["tailLinearizationBound"] > 1
        ),
        "residualFitsContractionBall": residual_norm <= residual_allowance,
        "ballMapsStrictlyInsideItself": mapping_upper_bound < ball_radius,
        "ballLipschitzConstantBelowOne": lipschitz_upper_bound < 1,
        "transportOperatorBoundBelowOne": transport_operator_bound < 1,
        "finiteLowBlockInverseExact": (
            finite_low_block["leftInverseExact"]
            and finite_low_block["rightInverseExact"]
            and low_block_hashes_match
        ),
        "lowBlockPreconditionerInertOnTailByGrading": (
            min(residual_degrees) > maximum_degree > low_block_degree
            and finite_tail_columns["lowProjectionTerms"] == 0
        ),
        "finiteTailColumnsBelowAllOrderBound": (
            rational(
                finite_tail_columns["maximumWeightedColumnRatio"]["exact"]
            )
            <= tail_linearization_bound
        ),
        "finiteCandidateRemainsOutsideCertifiedDisk": candidate_gap_factor > 1,
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"one or more R0.38 checks failed: {failed}")

    payload = {
        "scope": {
            "result": (
                "an all-order tail-aware contraction theorem extending the "
                "common analytic radius of the reduced active and transport fields"
            ),
            "classification": (
                "all-order Banach-space theorem, exact rational degree-80 "
                "restart certificate, and finite exact implementation regressions"
            ),
            "limitations": [
                "the theorem is restricted to the active support cone q>=-1",
                "the low-block inverse is inert on the certified tail correction space",
                "the result concerns the reduced edge generating equation rather than the full PDE",
                "the R0.32 finite Pade candidate remains outside the certified fixed-charge disk",
                "the candidate is not upgraded to a singularity",
                "no Navier-Stokes regularity or blow-up conclusion is claimed",
            ],
        },
        "input": {
            "r032": {
                "path": str(R032_CERTIFICATE),
                "sha256": R032_EXPECTED_SHA256,
                "sourceCommit": r032_certificate["git"]["commit"],
            },
            "r037": {
                "path": str(R037_CERTIFICATE),
                "sha256": R037_EXPECTED_SHA256,
                "sourceCommit": r037_certificate["git"]["commit"],
            },
        },
        "allOrderTheorem": {
            "space": r037_certificate["allOrderTheorem"]["space"],
            "mixedLayerBound": r037_certificate["allOrderTheorem"][
                "mixedLayerBound"
            ],
            "tailHypothesis": (
                "p=sum_(1<=i<=N) p_i and h=sum_(j>N) h_j on the active support cone"
            ),
            "tailLinearizationBound": (
                "||D Phi(p)h||_(B_r) <= 3(M_N(r)+S_N(r)/(N+1))||h||_(B_r)"
            ),
            "definitions": {
                "M_N": "sum_(1<=i<=N) i ||p_i||_1 r^i",
                "S_N": "sum_(1<=i<=N) i^2 ||p_i||_1 r^i",
            },
            "proof": (
                "the two ordered polarized sums agree; since i<=N<j, "
                "min(i,j)=i and (i+j)/j=1+i/j<=1+i/(N+1)"
            ),
            "quadraticTailBound": "||Phi(h)||_(B_r)<=3||h||_(B_r)^2",
            "tailInvariance": (
                "F(p_N) begins above N, D Phi(p_N) raises a degree-above-N "
                "input, and Phi(h) begins above 2N"
            ),
        },
        "lowBlockPreconditionerAudit": {
            "definition": (
                "A=P_m(P_m J P_m)^(-1)P_m+(I-P_m), with m=12 and "
                "J=I-D Phi(p_N)"
            ),
            "allOrderConclusion": (
                "for h supported above degree N, J h is supported above N, "
                "so A J h=J h and (I-AJ)h=D Phi(p_N)h; the low inverse "
                "does not improve the tail defect"
            ),
            "lowBlockDegree": low_block_degree,
            "finiteBlock": finite_low_block,
            "hashesMatchR037": low_block_hashes_match,
            "classification": (
                "the exact finite inverse is a valid low-block computation "
                "but is not the source of the R0.38 infinite-dimensional radius gain"
            ),
        },
        "restartCertificate": {
            "polynomialCutoff": maximum_degree,
            "targetRadius": r037.rational_record(target_radius),
            "r037Radius": r037.rational_record(previous_radius),
            "r031Radius": r037.rational_record(r031_radius),
            "radiusGainFromR037": r037.rational_record(
                target_radius / previous_radius
            ),
            "radiusGainFromR031": r037.rational_record(
                target_radius / r031_radius
            ),
            "fixedChargeGainFromR037": r037.rational_record(
                (target_radius / previous_radius) ** 3
            ),
            "fixedChargeGainFromR031": r037.rational_record(
                (target_radius / r031_radius) ** 3
            ),
            "degreeEightyPolynomialSha256": r037.polynomial_digest(polynomial),
            "degreeEightyPolynomialTerms": len(polynomial),
            "degreeEightyPolynomialNorm": r037.rational_record(polynomial_norm),
            "degreeMoment": r037.rational_record(degree_moment),
            "oldFullSpaceLinearizationBound": r037.rational_record(
                old_full_space_bound
            ),
            "tailLinearizationBound": r037.rational_record(
                tail_linearization_bound
            ),
            "nearbyFailureProbe": {
                "radius": r037.rational_record(failure_probe_radius),
                "tailLinearizationBound": r037.rational_record(
                    failure_probe_tail["tailLinearizationBound"]
                ),
                "classification": (
                    "negative control for this sufficient inequality only; "
                    "failure does not prove nonanalyticity"
                ),
            },
            "contractionMargin": r037.rational_record(contraction_margin),
            "exactResidualSha256": r037.polynomial_digest(residual),
            "exactResidualTerms": len(residual),
            "residualDegreeRange": [
                min(residual_degrees),
                max(residual_degrees),
            ],
            "exactResidualNorm": r037.rational_record(residual_norm),
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
            "transportOperatorNormUpperBound": r037.rational_record(
                transport_operator_bound
            ),
            "transportInverseNormUpperBound": r037.rational_record(
                transport_inverse_bound
            ),
            "statement": (
                "there is a unique correction in the closed degree-greater-than-80 "
                "tail ball; triangular formal uniqueness identifies the fixed point "
                "with the canonical active series, and the transport Neumann bound "
                "constructs the canonical normalized U and V fields at the same radius"
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
                "the finite candidate remains outside the proved disk and "
                "is not certified as a singularity"
            ),
        },
        "finiteRegression": {
            "recurrenceMaximumDegree": maximum_degree,
            "recurrenceOrderedInteractions": recurrence_interactions,
            "tailColumns": finite_tail_columns,
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
        "completed R0.38 tail-aware restart certificate",
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
    parser.add_argument("--max-total-degree", type=int, default=80)
    parser.add_argument("--target-radius", default="59/500")
    parser.add_argument("--low-block-degree", type=int, default=12)
    parser.add_argument("--tail-column-degree", type=int, default=81)
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
    if arguments.max_total_degree < 12:
        raise SystemExit("--max-total-degree must be at least 12")
    if not 3 <= arguments.low_block_degree < arguments.max_total_degree:
        raise SystemExit("--low-block-degree must lie below the recurrence cutoff")
    if arguments.tail_column_degree <= arguments.max_total_degree:
        raise SystemExit("--tail-column-degree must exceed the recurrence cutoff")
    target_radius = Rational(arguments.target_radius)
    if target_radius <= 0:
        raise SystemExit("--target-radius must be positive")
    if arguments.progress_log is not None:
        if arguments.progress_log.exists():
            raise SystemExit("--progress-log already exists; choose a new path")
        arguments.progress_log.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG = arguments.progress_log

    payload = build_payload(
        arguments.max_total_degree,
        target_radius,
        arguments.low_block_degree,
        arguments.tail_column_degree,
        arguments.progress,
        arguments.source_commit,
    )
    if arguments.check and not all(payload["checks"].values()):
        raise AssertionError("R0.38 certificate checks failed")
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
