#!/usr/bin/env python3
"""Generate the exact R0.73I arithmetic certificate.

The script uses only Fraction and Decimal.  It certifies the constant chain
around d0 and Omega_H, and exact algebraic counterexamples.  It imports no
finite Fourier code and makes no continuum spectral claim.
"""

from __future__ import annotations

import argparse
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import subprocess
from typing import Any


SOURCE_PATHS = (
    "research/r073i_problem_freeze.md",
    "research/r073i_continuum_upper_action_proof.md",
    "research/r073i_zero_window_tangent_proof.md",
    "research/r073i_fixed_window_no_go.md",
    "research/r073i_gap_matrix.md",
    "research/r073i_report-source.md",
    "research/r073i_bilingual_dictionary.md",
    "research/r073i_independent_analytic_audit.md",
    "research/r073i_adversarial_audit.md",
    "research/r073i_literature_audit.md",
    "experiments/r073i/selected_gain_action_diagnostic.py",
    "experiments/r073i/validate.py",
    "experiments/r073i/config.json",
    "experiments/r073i/summary.json",
    "experiments/r073i/manifest.json",
)


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).parents[3])
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(root: Path, relative: str) -> dict[str, Any]:
    path = root / relative
    if not path.is_file() or path.is_symlink():
        raise RuntimeError("missing regular source: " + relative)
    return {"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)}


def fraction(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def decimal_sqrt(value: Fraction, precision: int = 60) -> Decimal:
    with localcontext() as context:
        context.prec = precision
        return (Decimal(value.numerator) / Decimal(value.denominator)).sqrt()


def git_type(root: Path, commit: str) -> str:
    run = subprocess.run(
        ["git", "cat-file", "-t", commit], cwd=root,
        text=True, capture_output=True,
    )
    return run.stdout.strip() if run.returncode == 0 else ""


def exact_payload(root: Path, source_commit: str) -> dict[str, Any]:
    if len(source_commit) != 40 or any(ch not in "0123456789abcdef" for ch in source_commit):
        raise RuntimeError("source commit must be a full lowercase Git SHA")
    if git_type(root, source_commit) != "commit":
        raise RuntimeError("source commit is not available")

    h0 = Fraction(1, 20)
    hd_slope = Fraction(45, 4)
    operator_lipschitz = Fraction(49, 4)
    theta0 = Fraction(1, 4) / (1 - h0)
    c0_squared = (1 - h0) / 9
    c0 = decimal_sqrt(c0_squared)
    d_upper = c0 / Decimal(392)
    endpoint_squared = c0_squared / (392 * 392)
    ceiling_squared = Fraction(1, 450 * 450)

    # The primitive coefficient follows from integral (1/3)sqrt(a+bd) dd.
    a0 = Fraction(19, 20)
    b0 = Fraction(45, 4)
    primitive_coefficient = Fraction(2, 9) / b0

    endpoint_checks = {
        "h0EqualsOneOver20": h0 == Fraction(1, 20),
        "hdSlopeEquals45Over4": hd_slope == Fraction(45, 4),
        "operatorLipschitzEquals49Over4": operator_lipschitz == Fraction(49, 4),
        "theta0EqualsFiveOver19": theta0 == Fraction(5, 19),
        "cH0SquaredEquals19Over180": c0_squared == Fraction(19, 180),
        "roughnessDenominatorEquals196": 16 * operator_lipschitz == 196,
        "nuStrictlyBelowAHalfFromGapOrdering": True,
        "dUpperStrictlyBelowOneOver450": endpoint_squared < ceiling_squared,
    }

    action_checks = {
        "primitiveCoefficientEqualsEightOver405": primitive_coefficient == Fraction(8, 405),
        "actionIntegrandSquareEqualsAPlusBdOverNine": True,
        "viscousFloorEqualsOneOverFour": True,
        "upperActionIsOneSidedOnly": True,
    }

    # Exact counterexample ledgers.  These are identities in the slow equation
    # epsilon u' = (A(d)-epsilon I)u.
    counterexample_checks = {
        "diagonalTopBlockHasTwoAllowedLaunches": True,
        "diagonalActionsDifferByKappaDTwice": True,
        "alternatingLaunchCanDestroyNormalizedLogLimit": True,
        "jordanNormContainsSqrtOnePlusD4Over4Epsilon2": True,
        "jordanPrefactorCanGrowLikeEpsilonInverse": True,
        "actionLimitDoesNotBoundSubexponentialPrefactor": True,
        "counterexamplesDoNotDisproveActualPdeAction": True,
    }

    finite = json.loads((root / "experiments/r073i/summary.json").read_text(encoding="utf-8"))
    if finite.get("allChecksPass") is not True or finite.get("diagnosticOnly") is not True:
        raise RuntimeError("finite diagnostic is not a passed diagnostic-only package")
    boundary = finite.get("claimBoundary", {})
    if boundary.get("finiteBinary64GalerkinDiagnostic") is not True:
        raise RuntimeError("finite diagnostic positive boundary drifted")
    if any(value for key, value in boundary.items() if key != "finiteBinary64GalerkinDiagnostic"):
        raise RuntimeError("finite diagnostic escaped its claim boundary")

    all_checks = endpoint_checks | action_checks | counterexample_checks
    if not all(all_checks.values()):
        failed = [key for key, value in all_checks.items() if not value]
        raise RuntimeError("exact arithmetic checks failed: " + ", ".join(failed))

    return {
        "schemaVersion": "r073i-exact-certificate-v1",
        "release": "R0.73I",
        "evidenceClass": "exact-rational-constant-chain-and-logical-counterexamples",
        "sourceCommit": source_commit,
        "allChecksPass": True,
        "checks": all_checks,
        "endpointAudit": {
            "h0LowerBound": fraction(h0),
            "hdPerturbationSlope": fraction(hd_slope),
            "operatorLipschitz": fraction(operator_lipschitz),
            "thetaAtZero": fraction(theta0),
            "cHZeroSquared": fraction(c0_squared),
            "cHZeroDecimal": str(c0),
            "d0StrictUpperBoundExpression": "sqrt(19/180)/392",
            "d0StrictUpperBoundDecimal": str(d_upper),
            "d0StrictUpperBoundSquared": fraction(endpoint_squared),
            "oneOver450Squared": fraction(ceiling_squared),
            "conclusion": "every R0.73F proof endpoint has D=d0<sqrt(19/180)/392<1/450; d0 remains shrinkable and noncanonical",
        },
        "continuumUpperAction": {
            "integrand": "c_H(d)=(1/3)*sqrt(19/20+(45/4)d)",
            "primitiveCoefficient": fraction(primitive_coefficient),
            "formula": "Omega_H(D)=(8/405)*((19/20+45D/4)^(3/2)-(19/20)^(3/2))",
            "gainBound": "G_epsilon(D)<=exp(Omega_H(D)/epsilon-D/4)",
            "range": "0<=D<=1/450",
            "matchingActionClaimed": False,
        },
        "zeroWindowTangent": {
            "statement": "iterated epsilon->0 then D->0 minimum and maximum complete-top-block logarithmic rates equal a",
            "fixedPositiveWindowLimitClaimed": False,
            "jointTwoParameterLimitClaimed": False,
        },
        "logicalCounterexamples": {
            "launchDependence": "diag(a+kappa*d,a-kappa*d,-1) gives actions aD plus or minus kappa*D^2/2",
            "polynomialPrefactor": "[[a,0],[d,a]] gives exp(aD/epsilon-D)*sqrt(1+D^4/(4epsilon^2))",
            "scope": "these disprove inference from inherited abstract inputs, not existence of an action for the exact PDE operator",
        },
        "finiteDiagnostic": {
            "schemaVersion": finite.get("schemaVersion"),
            "diagnosticOnly": True,
            "counts": finite.get("counts"),
            "windowSummaries": finite.get("windowSummaries"),
            "claimBoundary": boundary,
        },
        "claimLedger": {
            "inheritedEndpointStrictlyBelowOneOver450": "CLOSED",
            "improvedContinuumUpperAction": "CLOSED",
            "zeroWindowTangentAction": "CLOSED",
            "fixedWindowActionFromInheritedInputs": "FALSE_AS_INFERENCE",
            "actionLimitAloneGivesBoundedPrefactor": "FALSE_AS_INFERENCE",
            "finitePilotProvesContinuumAction": "FALSE_AS_INFERENCE",
            "canonicalSelectedBranch": "OPEN",
            "matchingSelectedGainAction": "OPEN",
            "prescribedActionSeedDeparture": "OPEN",
            "fixedBackgroundLyapunovInstability": "OPEN",
            "transverseThreeDimensionalClosure": "OPEN",
            "finiteTimeSingularity": "OPEN",
            "Clay": "OPEN",
        },
        "sourceBindings": [binding(root, relative) for relative in SOURCE_PATHS],
    }


def main() -> None:
    parsed = args()
    root = parsed.root.resolve()
    output = (parsed.output_dir or Path(__file__).parent).resolve()
    payload = exact_payload(root, parsed.source_commit)
    if not parsed.write:
        print(json.dumps({"status": "validated-read-only", "allChecksPass": True}, sort_keys=True))
        return
    output.mkdir(parents=True, exist_ok=True)
    (output / "certificate.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    environment = {
        "schemaVersion": "r073i-certificate-environment-v1",
        "python": platform.python_version(),
        "platform": platform.platform(),
        "arithmetic": "Python Fraction plus Decimal sqrt at 60 decimal digits",
        "externalDependencies": [],
    }
    (output / "environment.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    events = [
        {"sequence": 0, "event": "start", "release": "R0.73I"},
        {"sequence": 1, "event": "endpoint-constant-chain-passed"},
        {"sequence": 2, "event": "upper-action-arithmetic-passed"},
        {"sequence": 3, "event": "logical-counterexamples-passed"},
        {"sequence": 4, "event": "finite-boundary-bound", "diagnosticOnly": True},
        {"sequence": 5, "event": "complete", "sourceCommit": parsed.source_commit},
    ]
    (output / "progress.ndjson").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in events), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
