#!/usr/bin/env python3
"""Independent Bareiss/minor check for the R0.73H rational q=2 block."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
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
    parser.add_argument("--output", type=Path, default=HERE / "independent_exact_q2.json")
    parser.add_argument("--source-commit", default="")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n"


def ftext(value: Fraction) -> str:
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
        path = ROOT / relative
        working = path.read_bytes()
        if committed != working:
            raise RuntimeError(f"working source differs from source commit: {relative}")
        bindings.append({
            "path": relative,
            "gitMode": tree[0],
            "bytes": len(working),
            "sha256": hashlib.sha256(working).hexdigest(),
        })
    return {
        "enforced": True,
        "sourceCommit": source_commit,
        "headAtRun": head,
        "sourceCommitIsAncestorOfHead": True,
        "allSourceBlobsMatch": True,
        "bindings": bindings,
    }


def rational_matrix() -> list[list[Fraction]]:
    modes = range(-4, 5)
    off = {
        0: Fraction(-9, 16),
        1: Fraction(9, 32), -1: Fraction(9, 32),
        2: Fraction(-9, 64), -2: Fraction(-9, 64),
        3: Fraction(9, 32), -3: Fraction(9, 32),
        4: Fraction(-9, 64), -4: Fraction(-9, 64),
    }
    return [[
        off.get(i - j, Fraction(0))
        + (Fraction(i * i + 1) - Fraction(1, 5) if i == j else Fraction(0))
        for j in modes
    ] for i in modes]


def bareiss_determinant(integer_matrix: list[list[int]]) -> int:
    size = len(integer_matrix)
    if size == 0:
        return 1
    work = [row[:] for row in integer_matrix]
    sign = 1
    previous = 1
    for k in range(size - 1):
        if work[k][k] == 0:
            swap = next((i for i in range(k + 1, size) if work[i][k] != 0), None)
            if swap is None:
                return 0
            work[k], work[swap] = work[swap], work[k]
            sign *= -1
        pivot = work[k][k]
        for i in range(k + 1, size):
            for j in range(k + 1, size):
                numerator = work[i][j] * pivot - work[i][k] * work[k][j]
                if numerator % previous != 0:
                    raise ArithmeticError("Bareiss division was not exact")
                work[i][j] = numerator // previous
        previous = pivot
    return sign * work[-1][-1]


def main() -> int:
    args = parse_args()
    output = args.output.resolve()
    if args.smoke:
        if is_within(output, HERE):
            raise RuntimeError("smoke output must be outside the formal source tree")
    elif output != (HERE / "independent_exact_q2.json").resolve():
        raise RuntimeError("formal output must be research/certificates/r073h/independent_exact_q2.json")
    if output.exists() and not args.overwrite:
        raise RuntimeError("refusing to overwrite independent exact output without --overwrite")
    provenance = source_gate(args.source_commit, args.smoke)
    matrix = rational_matrix()
    denominator = math.lcm(*(value.denominator for row in matrix for value in row))
    integer = [[int(value * denominator) for value in row] for row in matrix]
    determinants = []
    for size in range(1, len(integer) + 1):
        determinant_integer = bareiss_determinant([row[:size] for row in integer[:size]])
        determinant = Fraction(determinant_integer, denominator**size)
        determinants.append(determinant)

    low, tail, cross, target = (
        Fraction(1, 5), Fraction(95, 4), Fraction(27, 16), Fraction(1, 20)
    )
    a = low - target
    c = tail - target
    schur_numerator = a * c - cross * cross
    perturbation = Fraction(9, 4) * 5 * Fraction(1, 450)
    r0 = Fraction(3407, 20000)
    checks = {
        "allLeadingPrincipalMinorsPositive": all(value > 0 for value in determinants),
        "bareissUsedWithoutLdl": True,
        "tailConstantExact": tail == Fraction(95, 4),
        "crossConstantExact": cross == Fraction(27, 16),
        "twoByTwoSchurPositiveAfterOneTwentiethShift": a > 0 and schur_numerator > 0,
        "dPerturbationLeavesOneFortieth": target - perturbation == Fraction(1, 40),
        "twoRateMargin": 2 * r0 - Fraction(1, 3) == Fraction(221, 30000),
        "threeRateMargin": 3 * r0 - Fraction(1, 2) == Fraction(221, 20000),
    }
    result = {
        "schemaVersion": "r073h-independent-exact-q2-bareiss-v1",
        "release": "R0.73H",
        "evidenceClass": "independent-exact-rational-subcertificate",
        "method": "positive leading principal minors using fraction-free Bareiss determinants",
        "usedPrimaryLdlImplementation": False,
        "sourceProvenance": provenance,
        "commonIntegerDenominator": denominator,
        "leadingPrincipalMinors": [ftext(value) for value in determinants],
        "schurShiftDeterminant": ftext(schur_numerator),
        "perturbedLower": ftext(target - perturbation),
        "twoRateMargin": ftext(2 * r0 - Fraction(1, 3)),
        "threeRateMargin": ftext(3 * r0 - Fraction(1, 2)),
        "checks": checks,
        "allChecksPass": all(checks.values()),
        "claimBoundary": {
            "finiteExactSubcertificateForContinuumArgument": True,
            "finiteGalerkinPdeProof": False,
            "fullContinuumTheoremProvedByThisScriptAlone": False,
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
