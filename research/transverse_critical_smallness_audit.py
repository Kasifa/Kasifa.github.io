#!/usr/bin/env python3
"""Source-bound audit for the R0.69B critical transverse-stability gate.

The audit certifies the packet-specific algebra and numerical intervals.  It
records, but does not numerically instantiate, the universal small-data
threshold from the Koch--Tataru theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import gmpy2
from gmpy2 import mpfr, mpq


ROOT = Path(__file__).resolve().parents[1]
R059 = ROOT / "research/certificates/r059/multi-output-critical-saturation.json"
R066 = ROOT / "research/certificates/r066/spectral-audit.json"
EXPECTED_R059_SHA = "88774c0d5647f46700ed499409754f4207fdcef5a0193e5a337e7887eb3c6dce"
EXPECTED_R066_SHA = "a6f66c8bea8806fee3716b8d6611a2e0720e29969d94d991672cf3626ba8bcb2"
LAMBDA_LOWER = mpq(50303178668203, 2000000000000)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def directed_sqrt(value: mpq) -> tuple[mpfr, mpfr]:
    lower_context = gmpy2.context(precision=256, round=gmpy2.RoundDown)
    upper_context = gmpy2.context(precision=256, round=gmpy2.RoundUp)
    with gmpy2.local_context(lower_context):
        lower = gmpy2.sqrt(mpfr(value))
    with gmpy2.local_context(upper_context):
        upper = gmpy2.sqrt(mpfr(value))
    return lower, upper


def decimal(value: mpfr, digits: int = 50) -> str:
    return f"{value:.{digits}g}"


def first_below(k_upper: mpfr, rho_upper: mpfr, threshold: mpq) -> int:
    value = mpfr(k_upper)
    target = mpfr(threshold)
    depth = 0
    while value >= target:
        value *= rho_upper
        depth += 1
        if depth > 100000:
            raise RuntimeError("geometric threshold search did not terminate")
    return depth


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def build_payload(source_commit: str) -> dict[str, object]:
    r059 = json.loads(R059.read_text())
    r066 = json.loads(R066.read_text())

    ratio_squared = mpq(16) / LAMBDA_LOWER
    rho_lower, rho_upper = directed_sqrt(ratio_squared)
    sqrt2_lower, sqrt2_upper = directed_sqrt(mpq(2))
    with gmpy2.local_context(
        gmpy2.context(precision=256, round=gmpy2.RoundDown)
    ):
        k_lower = mpfr(6) + mpfr(4) * sqrt2_lower
    with gmpy2.local_context(
        gmpy2.context(precision=256, round=gmpy2.RoundUp)
    ):
        k_upper = mpfr(6) + mpfr(4) * sqrt2_upper

    thresholds = {
        "1": first_below(k_upper, rho_upper, mpq(1)),
        "1e-1": first_below(k_upper, rho_upper, mpq(1, 10)),
        "1e-2": first_below(k_upper, rho_upper, mpq(1, 100)),
        "1e-3": first_below(k_upper, rho_upper, mpq(1, 1000)),
        "1e-6": first_below(k_upper, rho_upper, mpq(1, 1000000)),
    }

    checks = {
        "pinnedR059CertificateHashMatches": sha256(R059) == EXPECTED_R059_SHA,
        "pinnedR066CertificateHashMatches": sha256(R066) == EXPECTED_R066_SHA,
        "r059PeriodicBmoBoundIsFormal": (
            r059["checks"]["formalPeriodicBmoMultiOutputSaturation"]
            and r059["checks"]["formalWeightedAbelBoundForBothInputs"]
        ),
        "r059ConstantMatchesTensorPrefixFormula": (
            r059["normComparison"]["constant"]
            == "C_T=(1+sqrt(2))*(2+sqrt(2))"
        ),
        "r066DominantRootLowerBoundIsCertified": (
            r066["checks"]["dominantRootHasTightExactRationalEnclosure"]
            and r066["checks"]["dominantRootExceedsTwentyFive"]
        ),
        "lambdaLowerExceedsSixteen": LAMBDA_LOWER > 16,
        "criticalContractionRateIsStrictlyBelowOne": rho_upper < 1,
        "bmoConstantIsStrictlyPositive": k_lower > 0,
        "thresholdDepthsAreStrictlyIncreasing": (
            thresholds["1"]
            < thresholds["1e-1"]
            < thresholds["1e-2"]
            < thresholds["1e-3"]
            < thresholds["1e-6"]
        ),
        "oneThresholdFirstCrossingIsEleven": thresholds["1"] == 11,
        "tenthThresholdFirstCrossingIsTwentyTwo": thresholds["1e-1"] == 22,
        "hundredthThresholdFirstCrossingIsThirtyTwo": thresholds["1e-2"] == 32,
        "thousandthThresholdFirstCrossingIsFortyTwo": thresholds["1e-3"] == 42,
    }

    payload = {
        "schemaVersion": "1.0",
        "status": "passed" if all(checks.values()) else "failed",
        "classification": (
            "source-bound critical-smallness and transverse-stability reduction "
            "for the R0.69A periodic packet; not a singularity or general "
            "three-dimensional regularity theorem"
        ),
        "checks": checks,
        "packetFamily": {
            "M_r": "16^r",
            "H_r": "4M_r",
            "epsilonSquared": "(16/lambda)^r",
            "amplitude": "A_r=epsilon_r*sqrt(H_r)",
            "physicalAmplitudeBehavior": "A_r grows exponentially",
        },
        "criticalNormBound": {
            "norm": "periodic heat-Carleson BMO^-1",
            "r059Formula": "sqrt(2)*C_T*A_r/sqrt(H_r)",
            "C_T": "4+3sqrt(2)",
            "prefactor": "6+4sqrt(2)",
            "prefactorInterval": {
                "lower": decimal(k_lower),
                "upper": decimal(k_upper),
            },
            "lambdaLower": {
                "exact": f"{LAMBDA_LOWER.numerator}/{LAMBDA_LOWER.denominator}",
                "decimal": decimal(mpfr(LAMBDA_LOWER)),
            },
            "rhoSquared": {
                "exact": f"{ratio_squared.numerator}/{ratio_squared.denominator}",
                "decimal": decimal(mpfr(ratio_squared)),
            },
            "rho": {
                "definition": "sqrt(16/lambdaLower)",
                "lower": decimal(rho_lower),
                "upper": decimal(rho_upper),
            },
            "bound": "||U_r(0)|| <= (6+4sqrt(2))*rho^r",
            "firstDepthStrictlyBelow": thresholds,
        },
        "perturbationEquation": {
            "equation": (
                "w_t-Delta w+(U dot grad)w+(w dot grad)U"
                "+(w dot grad)w+grad q=0, div w=0"
            ),
            "energyIdentity": (
                "(1/2)d||w||_2^2/dt+||grad w||_2^2"
                "=-integral w_i partial_i U_j w_j"
            ),
            "criticalBallCondition": (
                "(6+4sqrt(2))*rho^r+||w_0,r||_BMO^-1"
                "<eta_KT_per"
            ),
        },
        "externalTheoremBoundary": {
            "threshold": (
                "eta_KT_per is existential; this audit assigns no numerical value"
            ),
            "use": (
                "the standard periodic Koch-Tataru small-data fixed-point theorem "
                "turns the certified packet bound into a global regularity ball"
            ),
            "notAuditedHere": (
                "the external functional-analytic proof of the Koch-Tataru theorem"
            ),
        },
        "decision": {
            "closedGate": (
                "all sufficiently deep packets and all transverse perturbations "
                "inside a fixed critical small-data ball are globally regular"
            ),
            "nextGate": (
                "construct an order-one critical transverse sideband and test the "
                "linearized non-normal propagator in a scaling-critical norm"
            ),
        },
        "boundary": [
            "The result does not provide a numerical Koch-Tataru threshold.",
            "It controls only perturbations whose total critical norm is small.",
            "It does not prove instability or singularity for order-one perturbations.",
            "It is not a solution of the Navier-Stokes Millennium problem.",
        ],
        "provenance": {
            "sourceCommit": source_commit,
            "python": sys.version.split()[0],
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
            "inputCertificates": {
                "r059": {
                    "path": str(R059.relative_to(ROOT)),
                    "sha256": EXPECTED_R059_SHA,
                },
                "r066": {
                    "path": str(R066.relative_to(ROOT)),
                    "sha256": EXPECTED_R066_SHA,
                },
            },
        },
    }
    return payload


def main() -> int:
    args = parse_args()
    payload = build_payload(args.source_commit)
    encoded = json.dumps(
        payload,
        indent=2 if args.pretty else None,
        sort_keys=args.pretty,
    ) + "\n"
    if args.output:
        Path(args.output).write_text(encoded)
    else:
        sys.stdout.write(encoded)
    if args.check and payload["status"] != "passed":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

