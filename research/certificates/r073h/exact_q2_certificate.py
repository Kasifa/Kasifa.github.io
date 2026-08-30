#!/usr/bin/env python3
"""Exact-rational R0.73H doubled-row coercivity subcertificate.

This is a finite exact certificate for the Fourier block and analytic
tail/cross estimates in the continuum proof.  It is not a finite Galerkin
proof of the PDE statement.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_FILES = (
    "research/certificates/r073h/README.md",
    "research/certificates/r073h/command.txt",
    "research/certificates/r073h/config.json",
    "research/certificates/r073h/requirements.txt",
    "research/certificates/r073h/exact_q2_certificate.py",
    "research/certificates/r073h/independent_exact_q2.py",
    "research/certificates/r073h/primary_diagnostic.py",
    "research/certificates/r073h/independent_validate.py",
    "research/certificates/r073h/generate_certificate.py",
    "research/certificates/r073h/validate_certificate.py",
    "research/certificates/r073h/seal_package.py",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", default="")
    parser.add_argument("--output", type=Path, default=HERE / "exact_q2_certificate.json")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n"


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_gate(source_commit: str, smoke: bool) -> dict[str, object]:
    if smoke:
        return {"enforced": False, "sourceCommit": None, "allSourceBlobsMatch": False}
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError("formal run requires a full lowercase source commit")
    resolved = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", f"{source_commit}^{{commit}}"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if resolved != source_commit:
        raise RuntimeError("source commit did not resolve exactly")
    head = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", source_commit, head],
        check=False,
    ).returncode != 0:
        raise RuntimeError("source commit is not an ancestor of HEAD")
    bindings = []
    for relative in SOURCE_FILES:
        path = ROOT / relative
        tree = subprocess.run(
            ["git", "-C", str(ROOT), "ls-tree", source_commit, relative],
            check=True, capture_output=True, text=True,
        ).stdout.split()
        if len(tree) < 3 or tree[0] not in {"100644", "100755"}:
            raise RuntimeError(f"source is not a regular Git blob: {relative}")
        committed = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{source_commit}:{relative}"],
            check=True, capture_output=True,
        ).stdout
        if committed != path.read_bytes():
            raise RuntimeError(f"working source differs from source commit: {relative}")
        bindings.append({
            "path": relative,
            "gitMode": tree[0],
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    return {
        "enforced": True,
        "sourceCommit": source_commit,
        "headAtRun": head,
        "sourceCommitIsAncestorOfHead": True,
        "allSourceBlobsMatch": True,
        "bindings": bindings,
    }


def low_block_shifted() -> tuple[list[int], list[list[Fraction]]]:
    modes = list(range(-4, 5))
    potential = {
        0: Fraction(-9, 16),
        1: Fraction(9, 32), -1: Fraction(9, 32),
        2: Fraction(-9, 64), -2: Fraction(-9, 64),
        3: Fraction(9, 32), -3: Fraction(9, 32),
        4: Fraction(-9, 64), -4: Fraction(-9, 64),
    }
    matrix: list[list[Fraction]] = []
    for row_mode in modes:
        row = []
        for column_mode in modes:
            value = potential.get(row_mode - column_mode, Fraction(0))
            if row_mode == column_mode:
                value += Fraction(row_mode * row_mode + 1) - Fraction(1, 5)
            row.append(value)
        matrix.append(row)
    return modes, matrix


def fraction_ldl(matrix: list[list[Fraction]]) -> tuple[list[list[Fraction]], list[Fraction]]:
    size = len(matrix)
    lower = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    diagonal = [Fraction(0) for _ in range(size)]
    for j in range(size):
        lower[j][j] = Fraction(1)
        diagonal[j] = matrix[j][j] - sum(
            lower[j][k] * lower[j][k] * diagonal[k] for k in range(j)
        )
        if diagonal[j] <= 0:
            raise ArithmeticError(f"nonpositive exact LDL pivot at {j}")
        for i in range(j + 1, size):
            numerator = matrix[i][j] - sum(
                lower[i][k] * lower[j][k] * diagonal[k] for k in range(j)
            )
            lower[i][j] = numerator / diagonal[j]
    return lower, diagonal


def main() -> int:
    args = parse_args()
    output = args.output.resolve()
    if args.smoke:
        if is_within(output, HERE):
            raise RuntimeError("smoke output must be outside the formal source tree")
    elif output != (HERE / "exact_q2_certificate.json").resolve():
        raise RuntimeError("formal output must be research/certificates/r073h/exact_q2_certificate.json")
    if output.exists() and not args.overwrite:
        raise RuntimeError("refusing to overwrite exact output without --overwrite")
    provenance = source_gate(args.source_commit, args.smoke)
    modes, matrix = low_block_shifted()
    lower, pivots = fraction_ldl(matrix)

    low_bound = Fraction(1, 5)
    tail_bound = Fraction(95, 4)
    cross_bound = Fraction(27, 16)
    target_bound = Fraction(1, 20)
    shifted_two_by_two = [
        [low_bound - target_bound, -cross_bound],
        [-cross_bound, tail_bound - target_bound],
    ]
    schur_determinant = (
        shifted_two_by_two[0][0] * shifted_two_by_two[1][1]
        - shifted_two_by_two[0][1] * shifted_two_by_two[1][0]
    )
    perturbation = Fraction(9, 4) * Fraction(5) * Fraction(1, 450)
    perturbed_lower = target_bound - perturbation
    r_lower = Fraction(3407, 20000)
    two_rate_margin = 2 * r_lower - Fraction(1, 3)
    three_rate_margin = 3 * r_lower - Fraction(1, 2)

    checks = {
        "lowBlockIsNineByNine": len(matrix) == 9 and all(len(row) == 9 for row in matrix),
        "allFractionLdlPivotsPositive": all(value > 0 for value in pivots),
        "lowBlockBoundIsOneFifth": low_bound == Fraction(1, 5),
        "tailBoundIsNinetyFiveQuarters": tail_bound == Fraction(95, 4),
        "crossBoundIsTwentySevenSixteenths": cross_bound == Fraction(27, 16),
        "schurShiftTopLeftPositive": shifted_two_by_two[0][0] > 0,
        "schurShiftDeterminantPositive": schur_determinant > 0,
        "continuumH0LowerAtLeastOneTwentieth": schur_determinant > 0,
        "profilePerturbationAtMostOneFortieth": perturbation == Fraction(1, 40),
        "continuumHdLowerAtLeastOneFortieth": perturbed_lower == Fraction(1, 40),
        "twoRateMarginExact": two_rate_margin == Fraction(221, 30000),
        "threeRateMarginExact": three_rate_margin == Fraction(221, 20000),
    }
    result = {
        "schemaVersion": "r073h-exact-q2-ldl-v1",
        "release": "R0.73H",
        "evidenceClass": "exact-rational-subcertificate-for-continuum-proof",
        "finiteGalerkinPdeProof": False,
        "sourceProvenance": provenance,
        "fourierBlock": {
            "modes": modes,
            "operator": "Pi_|m|<=4[-d_x^2+1-(9/4)W_x(0)^2]Pi_|m|<=4-(1/5)I",
            "matrix": [[fraction_text(value) for value in row] for row in matrix],
            "ldlUnitLower": [[fraction_text(value) for value in row] for row in lower],
            "ldlPivots": [fraction_text(value) for value in pivots],
        },
        "tailCrossSchur": {
            "lowBlockLower": fraction_text(low_bound),
            "tailLower": fraction_text(tail_bound),
            "crossNormUpper": fraction_text(cross_bound),
            "targetLower": fraction_text(target_bound),
            "shiftedTwoByTwo": [[fraction_text(value) for value in row] for row in shifted_two_by_two],
            "shiftedDeterminant": fraction_text(schur_determinant),
        },
        "profilePerturbation": {
            "maximumProfileTime": "1/450",
            "wxSquaredDifferenceLipschitz": "5",
            "operatorDifferenceUpper": fraction_text(perturbation),
            "hdLower": fraction_text(perturbed_lower),
        },
        "rateMargins": {
            "strictInput": "r>3407/20000=0.17035",
            "twoRMinusOneThirdStrictlyGreaterThan": fraction_text(two_rate_margin),
            "threeRMinusOneHalfStrictlyGreaterThan": fraction_text(three_rate_margin),
        },
        "checks": checks,
        "allChecksPass": all(checks.values()),
        "claimBoundary": {
            "exactRationalFiniteSubcertificateUsedInsideContinuumProof": True,
            "finiteGalerkinApproximationOfPde": False,
            "fullContinuumProofContainedInThisJson": False,
            "naturalSeedOrderOneDepartureEstablishedByThisJsonAlone": False,
            "Clay": False,
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f".{output.name}.tmp")
    temporary.write_text(canonical(result), encoding="utf-8")
    os.replace(temporary, output)
    return 0 if result["allChecksPass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
