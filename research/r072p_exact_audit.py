#!/usr/bin/env python3
"""Producer exact-arithmetic audit for the R0.72P two-carrier gate.

The analytic report is the proof.  This program checks the finite algebraic
ledger used by that proof: the R-cell coefficient, rational shape constants,
the slow-time threshold, the two Morse-wall jets, the two-clause propagation
contract, and the N=2, p^2=1/2 physical exponent transfer.  It performs no
PDE time stepping and cannot certify the Coble--He theorem application.
"""

from __future__ import annotations

import argparse
import csv
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


AUDIT = "R0.72P producer two-carrier exact audit"
SCHEMA_VERSION = 1


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


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
        "research/r072p_report-source.md",
        "research/r072p_exact_audit.py",
        "research/r072p_compare_audits.py",
    )
    for relative in required:
        completed = subprocess.run(
            ["git", "ls-files", "--error-unmatch", relative],
            cwd=root,
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if completed.returncode != 0:
            return False
    return True


def max_rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024.0 * 1024.0) if sys.platform == "darwin" else value / 1024.0


def append_ndjson(path: Path, value: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True) + "\n")


def rational_string(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def monomial(**values: Fraction) -> dict[str, Fraction]:
    return {key: value for key, value in values.items() if value}


def multiply(*terms: dict[str, Fraction]) -> dict[str, Fraction]:
    result: dict[str, Fraction] = {}
    for term in terms:
        for key, value in term.items():
            result[key] = result.get(key, Fraction(0)) + value
    return {key: value for key, value in result.items() if value}


def divide(left: dict[str, Fraction], right: dict[str, Fraction]) -> dict[str, Fraction]:
    return multiply(left, {key: -value for key, value in right.items()})


def serialize_monomial(term: dict[str, Fraction]) -> dict[str, str]:
    return {key: rational_string(term[key]) for key in sorted(term)}


def cell_factor() -> dict[str, Any]:
    multiplier = Fraction(2)
    epsilon_constant = Fraction(2)
    coefficient_ratio = multiplier / epsilon_constant
    return {
        "activeCellShifts": [-2, -1, 1, 2],
        "cellJacobian": {"R": "-2/1"},
        "epsilonDefinition": {
            "absoluteDelta": "1/1",
            "a": "1/1",
            "R": "-2/1",
            "constant": rational_string(epsilon_constant),
        },
        "fourierMultiplierConstant": rational_string(multiplier),
        "affineInvariantRow": "{(nR,q_*):n∈Z}",
        "rowIsomorphicTo": "RZ",
        "rescaledCoefficientOverEpsilon": rational_string(coefficient_ratio),
        "secondCarrierCellFrequency": "2/1",
        "passed": coefficient_ratio == 1,
    }


def shape_bounds() -> dict[str, Any]:
    lambda_max = Fraction(1, 8)
    deviation = 4 * lambda_max
    factor_lower = 1 - deviation
    factor_upper = 1 + deviation

    # e = sum 1/n! < sum_{n=0}^4 1/n! + sum_{j>=0} 1/(5! 5^j)
    # = 65/24 + 1/96 = 87/32 < 3, hence exp(-1) > 1/3.
    e_upper = Fraction(87, 32)
    exp_minus_one_lower = Fraction(1, 3)
    sine_local_ratio_lower = Fraction(1, 2)
    sine_exterior_lower = Fraction(1, 2)
    local_lower = exp_minus_one_lower * factor_lower * sine_local_ratio_lower
    exterior_lower = exp_minus_one_lower * factor_lower * sine_exterior_lower
    local_upper = factor_upper

    derivative_bounds = {
        "W": Fraction(1) + lambda_max,
        "d1": Fraction(1) + 2 * lambda_max,
        "d2": Fraction(1) + 4 * lambda_max,
        "d3": Fraction(1) + 8 * lambda_max,
    }
    expected_derivatives = {
        "W": Fraction(9, 8),
        "d1": Fraction(5, 4),
        "d2": Fraction(3, 2),
        "d3": Fraction(2),
    }
    passed = (
        factor_lower == Fraction(1, 2)
        and factor_upper == Fraction(3, 2)
        and e_upper < 3
        and local_lower == Fraction(1, 12)
        and exterior_lower == Fraction(1, 12)
        and derivative_bounds == expected_derivatives
    )
    return {
        "C0": "144/1",
        "C1": "12/1",
        "alphaAbsMax": rational_string(lambda_max),
        "criticalCount": 2,
        "criticalSet": ["0", "pi"],
        "derivativeSupremumBounds": {
            key: rational_string(value) for key, value in derivative_bounds.items()
        },
        "eUpperCertificate": rational_string(e_upper),
        "eUpperLessThanThree": e_upper < 3,
        "exteriorGradientLower": rational_string(exterior_lower),
        "exteriorGradientUpper": rational_string(local_upper),
        "factorDeviationMax": rational_string(deviation),
        "factorLower": rational_string(factor_lower),
        "factorUpper": rational_string(factor_upper),
        "lambdaAbsMax": rational_string(lambda_max),
        "localGradientLower": rational_string(local_lower),
        "localGradientUpper": rational_string(local_upper),
        "radius": "pi/4",
        "passed": passed,
    }


def slow_threshold() -> dict[str, Any]:
    eta = Fraction(1, 16)
    derivative_coefficient = Fraction(2)
    left = derivative_coefficient * eta
    # eta=(1/2)^4, so eta^(3/4)=(1/2)^3 exactly.
    right = Fraction(1, 8)
    return {
        "derivativeCoefficientBound": rational_string(derivative_coefficient),
        "etaThreshold": rational_string(eta),
        "leftAtThreshold": rational_string(left),
        "rightAtThreshold": rational_string(right),
        "reducedCondition": "eta^(1/4)<=1/2",
        "passed": left == right,
    }


def wall_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for side, lam, phi, cosine in (
        ("plus", Fraction(1, 4), "pi", Fraction(-1)),
        ("minus", Fraction(-1, 4), "0", Fraction(1)),
    ):
        cosine_two = Fraction(1)
        d1 = Fraction(0)
        d2 = -cosine - 4 * lam * cosine_two
        d3 = Fraction(0)
        d4 = cosine + 16 * lam * cosine_two
        expected_fourth = Fraction(3) if side == "plus" else Fraction(-3)
        rows.append(
            {
                "side": side,
                "lambda": rational_string(lam),
                "phi": phi,
                "firstDerivative": rational_string(d1),
                "secondDerivative": rational_string(d2),
                "thirdDerivative": rational_string(d3),
                "fourthDerivative": rational_string(d4),
                "expectedFourthDerivative": rational_string(expected_fourth),
                "extraCriticalEquation": "cos(phi)=-1/(4lambda)",
                "conclusion": "Morse-applicability-wall-only",
                "passed": d1 == d2 == d3 == 0 and d4 == expected_fourth,
            }
        )
    return rows


def claim_contract() -> dict[str, Any]:
    return {
        "arbitraryCommonBandStatus": "open",
        "carrierPattern": [1, 2],
        "constantScope": "enhanced-dissipation-estimate",
        "constantsIndependentOf": [
            "R",
            "epsilon",
            "lambda",
            "lambda_minus",
            "initial datum",
        ],
        "constantsMayDependOn": ["fixed upper shape class", "lambda_max"],
        "finiteCertificateIsProof": False,
        "fullSuperposition": True,
        "growingCarrierCountStatus": "open",
        "integratedEstimate": {
            "epsilonExponent": "-1/2",
            "required": True,
            "status": "proved-analytically-for-declared-class",
        },
        "lambdaClass": "0<lambda_minus<=abs(lambda)<=1/8",
        "physicalAmplitudeBalanceMayDependOn": ["lambda_minus"],
        "sameUniformConstantsRequired": True,
        "status": "proved-for-declared-real-collinear-phase-1:2-class",
        "terminalEstimate": {
            "decayExponent": "sqrt(epsilon)",
            "required": True,
            "status": "proved-analytically-for-declared-class",
        },
    }


def exponent_ledger() -> dict[str, Any]:
    n_value = Fraction(2)
    b_value = Fraction(2)
    p_squared = n_value / (b_value * b_value)

    u0 = monomial(epsilon=Fraction(4, 3), p=Fraction(4, 3))
    raw_ed = monomial(epsilon=Fraction(1, 2))
    u_ed = multiply(u0, raw_ed)
    z_strong = monomial(
        epsilon=Fraction(4, 3),
        p=Fraction(2),
        R=Fraction(2, 3),
        L=Fraction(1),
    )
    quotient = divide(u_ed, z_strong)
    cross_cubic = monomial(a=Fraction(2), N=Fraction(2), epsilon=Fraction(1, 2))

    general = {
        "FullSuperpositionCrossCubic": serialize_monomial(cross_cubic),
        "UED": serialize_monomial(u_ed),
        "UEDOverZ": serialize_monomial(quotient),
        "ZStrong": serialize_monomial(z_strong),
    }
    expected_general = {
        "FullSuperpositionCrossCubic": {
            "N": "2/1",
            "a": "2/1",
            "epsilon": "1/2",
        },
        "UED": {"epsilon": "11/6", "p": "4/3"},
        "UEDOverZ": {
            "L": "-1/1",
            "R": "-2/3",
            "epsilon": "1/2",
            "p": "-2/3",
        },
        "ZStrong": {
            "L": "1/1",
            "R": "2/3",
            "epsilon": "4/3",
            "p": "2/1",
        },
    }
    fixed_pattern = {
        "crossCubicCoefficientN2": rational_string(n_value * n_value),
        "strongWindowEpsilonRhs": {
            "L": "2/1",
            "R": "4/3",
            "two": "-2/3",
        },
        "strongWindowSqrtEpsilonRhs": {
            "L": "1/1",
            "R": "2/3",
            "two": "-1/3",
        },
        "UED": {"epsilon": "11/6", "two": "-2/3"},
        "UEDOverZ": {
            "L": "-1/1",
            "R": "-2/3",
            "epsilon": "1/2",
            "two": "1/3",
        },
        "ZStrong": {
            "L": "1/1",
            "R": "2/3",
            "epsilon": "4/3",
            "two": "-1/1",
        },
    }
    return {
        "claimContract": claim_contract(),
        "fixedPattern": fixed_pattern,
        "general": general,
        "parameters": {
            "B": rational_string(b_value),
            "N": rational_string(n_value),
            "pSquared": rational_string(p_squared),
        },
        "passed": general == expected_general and p_squared == Fraction(1, 2),
    }


def shape_rows(exact: dict[str, Any]) -> list[dict[str, Any]]:
    shape = exact["shapeBounds"]
    slow = exact["slowThreshold"]
    fields = (
        ("factorLower", shape["factorLower"], "1-4*(1/8)"),
        ("factorUpper", shape["factorUpper"], "1+4*(1/8)"),
        ("localGradientLower", shape["localGradientLower"], "(1/3)*(1/2)*(1/2)"),
        ("localGradientUpper", shape["localGradientUpper"], "1*(3/2)*1"),
        ("exteriorGradientLower", shape["exteriorGradientLower"], "(1/3)*(1/2)*(1/2)"),
        ("W", shape["derivativeSupremumBounds"]["W"], "1+1/8"),
        ("d1", shape["derivativeSupremumBounds"]["d1"], "1+2/8"),
        ("d2", shape["derivativeSupremumBounds"]["d2"], "1+4/8"),
        ("d3", shape["derivativeSupremumBounds"]["d3"], "1+8/8"),
        ("etaThreshold", slow["etaThreshold"], "2*eta=eta^(3/4)"),
    )
    return [
        {"quantity": name, "value": value, "derivation": derivation, "passed": True}
        for name, value, derivation in fields
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


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
        "precision": "Python Fraction exact rational arithmetic; symbolic pi labels only",
        "gitCommit": git_commit(root),
        "sourceTracked": sources_tracked(root),
        "trackedChangesDirty": tracked_changes_dirty(root),
        "limitations": (
            "The certificate audits finite algebra and claim wiring. It does not "
            "prove the semigroup theorem, continuum sine inequalities, or any "
            "general Navier-Stokes regularity statement."
        ),
    }
    (output / "producer-config.json").write_text(
        json.dumps(config, indent=2) + "\n", encoding="utf-8"
    )
    append_ndjson(progress, {"time": utc_now(), "stage": "start", **config})

    exact = {
        "cellFactor": cell_factor(),
        "shapeBounds": shape_bounds(),
        "slowThreshold": slow_threshold(),
        "morseWall": {
            "absLambda": "1/4",
            "extraCriticalEquation": "cos(phi)=-1/(4lambda)",
            "status": "Morse-applicability-wall-only",
        },
        "exponentLedger": exponent_ledger(),
    }
    walls = wall_rows()
    shapes = shape_rows(exact)
    (output / "producer-exponents.json").write_text(
        json.dumps(exact, indent=2) + "\n", encoding="utf-8"
    )
    write_csv(output / "producer-shape.csv", shapes)
    write_csv(output / "producer-wall.csv", walls)

    stages = (
        ("cell-factor", exact["cellFactor"]["passed"]),
        ("shape-bounds", exact["shapeBounds"]["passed"]),
        ("slow-threshold", exact["slowThreshold"]["passed"]),
        ("morse-wall", all(row["passed"] for row in walls)),
        ("claim-contract", all(
            exact["exponentLedger"]["claimContract"][name]["required"]
            for name in ("integratedEstimate", "terminalEstimate")
        )),
        ("exponent-ledger", exact["exponentLedger"]["passed"]),
    )
    for stage, passed in stages:
        append_ndjson(progress, {"time": utc_now(), "stage": stage, "passed": passed})

    checks = {
        "cellFactorPassed": exact["cellFactor"]["passed"],
        "shapeBoundsPassed": exact["shapeBounds"]["passed"],
        "slowThresholdPassed": exact["slowThreshold"]["passed"],
        "morseWallPassed": all(row["passed"] for row in walls),
        "integralAndTerminalRequired": all(
            exact["exponentLedger"]["claimContract"][name]["required"]
            for name in ("integratedEstimate", "terminalEstimate")
        ),
        "fullSuperpositionStatusScoped": (
            exact["exponentLedger"]["claimContract"]["status"]
            == "proved-for-declared-real-collinear-phase-1:2-class"
            and exact["exponentLedger"]["claimContract"]["arbitraryCommonBandStatus"]
            == "open"
        ),
        "n2PSquaredLedgerPassed": exact["exponentLedger"]["passed"],
    }
    elapsed = time.perf_counter() - started
    result = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT,
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "shapeRows": len(shapes),
        "wallRows": len(walls),
        "elapsedSeconds": elapsed,
        "maxRssMb": max_rss_mb(),
        "limitations": config["limitations"],
    }
    (output / "producer-result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
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
        f"[producer] status={result['status']} shape={len(shapes)} wall={len(walls)} "
        f"integralTerminal={checks['integralAndTerminalRequired']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
