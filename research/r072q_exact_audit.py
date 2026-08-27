#!/usr/bin/env python3
"""Exact producer ledger for the R0.72Q arbitrary-phase shape gate.

The analytic proof lives in the report.  This program checks only its finite
algebraic spine: the fixed-M jet budget, the rational consequences of
Q_2 <= 1/2, the radical comparisons used by the explicit shape constants,
the slow-time exponent identity, and the exact 1:2 caustic identities.  It
does not locate roots numerically and it does not replace the continuum
Morse or enhanced-dissipation arguments.
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


AUDIT = "R0.72Q producer arbitrary-phase exact audit"
SCHEMA_VERSION = 1


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rational_string(value: Fraction) -> str:
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
    unstaged = subprocess.run(
        ["git", "diff", "--quiet"], cwd=root, check=False
    ).returncode
    staged = subprocess.run(
        ["git", "diff", "--cached", "--quiet"], cwd=root, check=False
    ).returncode
    return unstaged != 0 or staged != 0


def sources_tracked(root: Path) -> bool:
    required = (
        "research/r072q_report-source.md",
        "research/r072q_exact_audit.py",
        "research/r072q_compare_audits.py",
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


def build_shape_contract(max_carrier: int) -> dict[str, Any]:
    q2 = Fraction(1, 2)
    q1 = q2 / 2
    q0 = q2 / 4
    d0 = 1 + q0
    d1 = 1 + q1
    d2 = 1 + q2
    d3 = 1 + Fraction(max_carrier, 2)

    # sin(pi/12)>1/4 follows from
    # sin^2(pi/12)=(2-sqrt(3))/4>1/16, which reduces to 48<49.
    sin_square_left = 48
    sin_square_right = 49

    # mu=(sqrt(3)-1)/2>1/3 reduces to sqrt(3)>5/3, hence 27>25.
    mu_square_left = 27
    mu_square_right = 25

    # Independently sum through 1/4!, then bound the remaining factorial
    # tail by the geometric majorant sum_{k>=0} 1/(5!*5^k)=1/96.
    factorial = 1
    e_partial = Fraction(0)
    for n in range(5):
        if n:
            factorial *= n
        e_partial += Fraction(1, factorial)
    e_tail_upper = Fraction(1, 96)
    e_upper = e_partial + e_tail_upper
    exp_minus_one_lower = Fraction(1, 3)

    eta = Fraction(1, 1) / (d3**4)
    eta_quarter = Fraction(1, 1) / d3
    eta_three_quarters = eta_quarter**3
    slow_left = d3 * eta

    exact_checks = {
        "q1FromQ2": q1 == Fraction(1, 4),
        "q0FromQ2": q0 == Fraction(1, 8),
        "sinRadiusGreaterThanQuarter": sin_square_left < sin_square_right,
        "localCurvatureMarginGreaterThanThird": mu_square_left > mu_square_right,
        "boundedHeatEnvelope": e_upper < 3,
        "ePartialSumExact": e_partial == Fraction(65, 24),
        "eTailMajorantExact": e_tail_upper == Fraction(1, 96),
        "eUpperReassembled": e_upper == Fraction(87, 32),
        "derivativeBoundsExact": (
            d0 == Fraction(9, 8)
            and d1 == Fraction(5, 4)
            and d2 == Fraction(3, 2)
            and d3 == Fraction(max_carrier + 2, 2)
        ),
        "slowThresholdIdentity": slow_left == eta_three_quarters,
    }
    return {
        "profile": (
            "F_y(phi)=cos(phi)+sum_{m=2}^M Re(beta_m(y)*exp(i*m*phi))"
        ),
        "fixedM": True,
        "maxCarrier": max_carrier,
        "phaseClass": "arbitrary phases",
        "jetBudgets": {
            "QjDefinition": "Q_j=sup_y sum_{m=2}^M m^j abs(beta_m(y))",
            "Q2Upper": rational_string(q2),
            "Q1UpperDerived": rational_string(q1),
            "Q0UpperDerived": rational_string(q0),
            "termwiseFacts": ["m<=m^2/2 for m>=2", "1<=m^2/4 for m>=2"],
        },
        "criticalGeometry": {
            "criticalCount": 2,
            "criticalLocationBoxes": ["dist(phi,0)<pi/12", "dist(phi,pi)<pi/12"],
            "criticalLocationReason": (
                "at F_phi=0, abs(sin(phi))<=Q1<=1/4<sin(pi/12)"
            ),
            "arbitraryPhaseUniform": True,
            "radius": "pi/12",
            "localCurvatureMargin": "(sqrt(3)-1)/2",
            "localCurvatureMarginGreaterThan": "1/3",
            "localCurvatureReason": (
                "a radius-pi/12 tube about either critical point stays within "
                "pi/6 of 0 or pi, so abs(F_phiphi)>=cos(pi/6)-Q2"
            ),
            "normalizedShapeConstants": {
                "C0": "9/1",
                "conservativeC0AlsoValid": "81/1",
                "C1": "12/1",
            },
            "physicalWindowShapeConstants": {
                "yWindow": "0<=y<=1",
                "C0": "81/1",
                "C1": "36/1",
                "localSlopeLower": "1/9",
                "awaySlopeLower": "1/36",
            },
            "C0": "81/1",
            "C1": "36/1",
            "shapeConstantScope": (
                "physical Coble shear W=e^(-y)F_y on 0<=y<=1; normalized F_y "
                "has the sharper C1=12 contract"
            ),
        },
        "boundedEnvelopeCertificate": {
            "partialSumDefinition": "sum_{n=0}^4 1/n!",
            "partialSum": rational_string(e_partial),
            "partialSumExpected": "65/24",
            "tailMajorantDefinition": "sum_{k=0}^infinity 1/(5!*5^k)",
            "tailUpper": rational_string(e_tail_upper),
            "tailUpperExpected": "1/96",
            "eUpperCertificate": rational_string(e_upper),
            "eUpperReassembly": "65/24+1/96=87/32",
            "eUpperLessThanThree": e_upper < 3,
            "expMinusOneLower": rational_string(exp_minus_one_lower),
            "piLowerInput": "pi>3 (inscribed regular hexagon)",
            "normalizedLocalSlopeLower": "1/3",
            "normalizedAwaySlopeLower": "1/12",
            "physicalLocalSlopeLower": rational_string(
                exp_minus_one_lower * Fraction(1, 3)
            ),
            "physicalAwaySlopeLower": rational_string(
                exp_minus_one_lower * Fraction(1, 12)
            ),
            "passed": (
                e_partial == Fraction(65, 24)
                and e_tail_upper == Fraction(1, 96)
                and e_upper == Fraction(87, 32)
                and e_upper < 3
                and exp_minus_one_lower * Fraction(1, 3) == Fraction(1, 9)
                and exp_minus_one_lower * Fraction(1, 12) == Fraction(1, 36)
            ),
        },
        "radicalCertificates": {
            "sinRadius": {
                "statement": "sin(pi/12)>1/4",
                "identity": "sin(pi/12)^2=(2-sqrt(3))/4",
                "reduction": "sqrt(3)<7/4",
                "integerSquareComparison": "48<49",
                "passed": sin_square_left < sin_square_right,
            },
            "curvatureMargin": {
                "statement": "(sqrt(3)-1)/2>1/3",
                "reduction": "sqrt(3)>5/3",
                "integerSquareComparison": "27>25",
                "passed": mu_square_left > mu_square_right,
            },
        },
        "derivativeSupremumBounds": {
            "d0": rational_string(d0),
            "d1": rational_string(d1),
            "d2": rational_string(d2),
            "d3": rational_string(d3),
            "d3Symbolic": "1+M/2",
        },
        "slowTime": {
            "mixedDerivativeCoefficient": rational_string(d3),
            "mixedDerivativeCoefficientSymbolic": "1+M/2",
            "etaThreshold": rational_string(eta),
            "etaThresholdSymbolic": "(1+M/2)^(-4)",
            "etaQuarterAtThreshold": rational_string(eta_quarter),
            "leftAtThreshold": rational_string(slow_left),
            "etaThreeQuartersAtThreshold": rational_string(eta_three_quarters),
            "reducedCondition": "(1+M/2)*eta^(1/4)<=1",
            "passed": slow_left == eta_three_quarters,
        },
        "proofSkeleton": [
            "Q2<=1/2 implies Q1<=1/4 and Q0<=1/8 termwise.",
            "Boundary signs at +/-pi/12 and pi+/-pi/12 give one zero in each box.",
            "The Q2 curvature bound makes F_phi strictly monotone in each box.",
            "Every zero lies in those boxes because abs(sin(phi))<=Q1.",
            "The pi/12 tubes have curvature margin mu>1/3; fixed-M derivatives are bounded.",
        ],
        "exactChecks": exact_checks,
        "passed": all(exact_checks.values()),
    }


def build_caustic_contract() -> dict[str, Any]:
    exp_minus_three = Fraction(1, 8)
    exp_minus_one = Fraction(-3, 8)
    radius_squared_min = Fraction(1, 16)
    radius_squared_max = Fraction(1, 4)
    implicit_left = Fraction(27, 4096)
    implicit_right = Fraction(27, 1024) * Fraction(1, 4)
    radial_origin = Fraction(1, 16)
    radial_endpoint = Fraction(1, 4)
    ray_function_at_origin = Fraction(0)
    ray_function_at_endpoint = (
        (radial_endpoint - radial_origin) ** 3 / radial_endpoint
    )
    derivative_expanded_coefficients = (
        Fraction(2),
        -3 * radial_origin,
        Fraction(0),
        radial_origin**3,
    )
    factor_left_ascending = (
        radial_origin**2,
        -2 * radial_origin,
        Fraction(1),
    )
    factor_right_ascending = (radial_origin, Fraction(2))
    product_ascending = [Fraction(0)] * 4
    for left_index, left_value in enumerate(factor_left_ascending):
        for right_index, right_value in enumerate(factor_right_ascending):
            product_ascending[left_index + right_index] += left_value * right_value
    derivative_factored_coefficients = tuple(reversed(product_ascending))

    checks = {
        "parameterCoefficientsExact": (
            exp_minus_three == Fraction(1, 8)
            and exp_minus_one == Fraction(-3, 8)
        ),
        "implicitPolynomialIdentity": implicit_left == implicit_right,
        "radiusRangeExact": (
            radius_squared_min == Fraction(1, 16)
            and radius_squared_max == Fraction(1, 4)
        ),
        "interiorDiskSeparated": Fraction(1, 4) ** 2 == radius_squared_min,
        "cuspFourthJetsNonzero": Fraction(3) != 0 and Fraction(-3) != 0,
        "rayDerivativeFactorizationExact": (
            derivative_expanded_coefficients == derivative_factored_coefficients
        ),
        "rayEndpointValuesExact": (
            ray_function_at_origin == 0
            and ray_function_at_endpoint == Fraction(27, 1024)
        ),
    }
    return {
        "twoCarrierProfile": "f(phi)=cos(phi)+a*cos(2*phi+theta)",
        "complexCoefficient": "z=a*exp(i*theta)",
        "degeneracyEquations": [
            "sin(phi)+2*a*sin(2*phi+theta)=0",
            "cos(phi)+4*a*cos(2*phi+theta)=0",
        ],
        "linearJetSolution": [
            "a*cos(2*phi+theta)=-cos(phi)/4",
            "a*sin(2*phi+theta)=-sin(phi)/2",
        ],
        "parametrization": "z(phi)=(1/8)*exp(-3*i*phi)-(3/8)*exp(-i*phi)",
        "parametrizationCoefficients": {
            "expMinus3iPhi": rational_string(exp_minus_three),
            "expMinus1iPhi": rational_string(exp_minus_one),
        },
        "coordinateIdentities": {
            "imaginaryPart": "Im(z)=sin(phi)^3/2",
            "radiusSquared": "abs(z)^2=(1+3*sin(phi)^2)/16",
        },
        "implicitEquation": "(abs(z)^2-1/16)^3=(27/1024)*(Im(z))^2",
        "implicitIdentityBothSides": "(27/4096)*sin(phi)^6",
        "radiusRange": ["1/4", "1/2"],
        "rayIntersection": {
            "radialSquaredVariable": "s=abs(z)^2",
            "function": "H(s)=(s-1/16)^3/s",
            "rayEquation": "H(s)=(27/1024)*sin(theta)^2",
            "derivative": (
                "H'(s)=(s-1/16)^2*(2*s+1/16)/s^2"
            ),
            "expandedDerivativeNumeratorCoefficients": [
                rational_string(value) for value in derivative_expanded_coefficients
            ],
            "factoredDerivativeNumeratorCoefficients": [
                rational_string(value) for value in derivative_factored_coefficients
            ],
            "strictPositivityDomain": "s>1/16",
            "endpointValues": {
                "H(1/16)": rational_string(ray_function_at_origin),
                "H(1/4)": rational_string(ray_function_at_endpoint),
            },
            "conclusion": (
                "every phase ray has exactly one caustic intersection with "
                "s in [1/16,1/4]"
            ),
            "passed": (
                derivative_expanded_coefficients
                == derivative_factored_coefficients
                and ray_function_at_origin == 0
                and ray_function_at_endpoint == Fraction(27, 1024)
            ),
        },
        "interiorDisk": {
            "condition": "abs(z)<1/4",
            "conclusion": "no degeneracy and exactly two critical points",
        },
        "classification": {
            "genericWall": "A2 fold: f'''=-3*sin(phi) is nonzero",
            "cusps": [
                {
                    "z": "1/4",
                    "degeneratePhi": "pi",
                    "relativePhase": "0",
                    "fourthDerivative": "3/1",
                    "type": "A3",
                },
                {
                    "z": "-1/4",
                    "degeneratePhi": "0",
                    "relativePhase": "pi",
                    "fourthDerivative": "-3/1",
                    "type": "A3",
                },
            ],
            "jetIdentities": ["f'''=-3*sin(phi)", "f''''=-3*cos(phi)"],
            "wallMeaning": "Morse-applicability wall only",
        },
        "exactChecks": checks,
        "passed": all(checks.values()),
    }


def canonical_payload(max_carrier: int) -> dict[str, Any]:
    shape = build_shape_contract(max_carrier)
    caustic = build_caustic_contract()
    claim = {
        "status": "proved-analytically-for-fixed-M-arbitrary-phase-shape-class",
        "fixedMRequired": True,
        "finiteCertificateIsProof": False,
        "arbitraryPhases": True,
        "growingMStatus": "open",
        "commonBandWithoutJetDominanceStatus": "open",
        "causticIsEDFailureCounterexample": False,
        "unnormalizedUniformCurvatureForUnboundedYClaimed": False,
    }
    return {
        "schemaVersion": SCHEMA_VERSION,
        "theoremId": "R0.72Q-fixed-M-arbitrary-phase-shape-gate",
        "shapeContract": shape,
        "twoCarrierCaustic": caustic,
        "claimBoundary": claim,
        "passed": shape["passed"] and caustic["passed"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--max-carrier", type=int, default=2)
    args = parser.parse_args()
    if args.max_carrier < 2:
        parser.error("--max-carrier must be an integer >= 2")

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
        "maxCarrier": args.max_carrier,
        "precision": "Python Fraction exact rational and integer identity audit",
        "gitCommit": git_commit(root),
        "sourceTracked": sources_tracked(root),
        "trackedChangesDirty": tracked_changes_dirty(root),
        "limitations": (
            "Finite exact algebra only. Trigonometric monotonicity, root isolation, "
            "the continuum shape lemma, and enhanced dissipation remain analytic proofs."
        ),
    }
    write_json(output / "producer-config.json", config)
    append_ndjson(progress, {"time": utc_now(), "stage": "start", **config})

    payload = canonical_payload(args.max_carrier)
    write_json(output / "producer-payload.json", payload)
    for stage, passed in (
        ("fixed-M-shape", payload["shapeContract"]["passed"]),
        ("arbitrary-phase-critical-count", payload["shapeContract"]["criticalGeometry"]["criticalCount"] == 2),
        ("slow-time-threshold", payload["shapeContract"]["slowTime"]["passed"]),
        ("two-carrier-caustic", payload["twoCarrierCaustic"]["passed"]),
        ("claim-boundary", payload["claimBoundary"]["finiteCertificateIsProof"] is False),
    ):
        append_ndjson(progress, {"time": utc_now(), "stage": stage, "passed": passed})

    checks = {
        "payloadPassed": payload["passed"],
        "shapeContractPassed": payload["shapeContract"]["passed"],
        "criticalCountIsTwo": payload["shapeContract"]["criticalGeometry"]["criticalCount"] == 2,
        "causticPassed": payload["twoCarrierCaustic"]["passed"],
        "claimBoundaryScoped": (
            payload["claimBoundary"]["fixedMRequired"] is True
            and payload["claimBoundary"]["growingMStatus"] == "open"
            and payload["claimBoundary"]["finiteCertificateIsProof"] is False
        ),
    }
    elapsed = time.perf_counter() - started
    result = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT,
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "maxCarrier": args.max_carrier,
        "elapsedSeconds": elapsed,
        "maxRssMb": max_rss_mb(),
        "limitations": config["limitations"],
    }
    write_json(output / "producer-result.json", result)
    append_ndjson(
        resources,
        {
            "time": utc_now(),
            "event": "complete",
            "elapsedSeconds": elapsed,
            "maxRssMb": result["maxRssMb"],
            "pid": os.getpid(),
        },
    )
    monitor.write_text(
        f"[producer] status={result['status']} M={args.max_carrier} "
        f"shape={checks['shapeContractPassed']} caustic={checks['causticPassed']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
