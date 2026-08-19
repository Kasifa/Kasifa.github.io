#!/usr/bin/env python3
"""R0.34 exact exclusion of bounded-degree polynomial Stieltjes backgrounds.

R0.33 rules out a direct positive-measure Markov/Stieltjes representation
for the sign-transformed transport series B_U, B_V and their logarithmic
derivatives H_U, H_V.  This audit allows an arbitrary real polynomial
background:

    C(x) = P_d(x) + integral_[0,infinity) dmu(t)/(1-x*t),  mu >= 0.

If deg(P_d) <= d, every coefficient after index d is unchanged by the
subtraction.  Any negative principal minor of a shifted tail Hankel matrix
whose smallest coefficient index is greater than d therefore excludes every
possible choice of the polynomial coefficients at once.

Using the 50 exact R0.32 endpoint coefficients, the audit exhausts all tail
principal minors whose smallest coefficient index is at least 40.  It gives
exact universal exclusions through background degrees 43 for B_U, 44 for
B_V, 46 for H_U, and 45 for H_V.  The thresholds are maximal only within the
available coefficient window and the tested principal-minor family.  The
result does not exclude a genuinely infinite analytic background, other Pade
classes, the R0.32 candidate, or any behavior of full 3D Navier--Stokes.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
from itertools import combinations, permutations
import json
import os
from pathlib import Path
import platform
import sys
import time

import sympy as sp

import edge_rational_asymptotic_audit as r028


sys.set_int_max_str_digits(0)

R032_CERTIFICATE = Path(
    "research/certificates/r032/edge-singularity-candidates.json"
)
R033_CERTIFICATE = Path(
    "research/certificates/r033/edge-moment-structure.json"
)
R032_EXPECTED_SHA256 = (
    "bd70ed05779631b729e89c269f82d287da361fdcea34e3c42703a712222f5575"
)
R033_EXPECTED_SHA256 = (
    "ccbf8ab05615378f6d4b9824e86b679b6d0df2882cbc6e563b063b8769292367"
)
EXPECTED_WITNESSES = {
    "B_U": {
        "shift": 44,
        "monomialIndices": (0, 1, 2),
        "determinantSha256": (
            "c8fb036dea3c66834b07b39666537f0b85ea138ac105b6315f7519d0488a3e2a"
        ),
    },
    "B_V": {
        "shift": 45,
        "monomialIndices": (0, 1, 2),
        "determinantSha256": (
            "516aaee23c11bcf030247d5d3d657ad754289d83ade88d1a70bafba1fb782ccb"
        ),
    },
    "H_U": {
        "shift": 47,
        "monomialIndices": (0,),
        "determinantSha256": (
            "0f9c04e0620e89dd27f5a440b4cb7787ce22f22d0545595e14063415fdad8b66"
        ),
    },
    "H_V": {
        "shift": 46,
        "monomialIndices": (0, 1),
        "determinantSha256": (
            "815da2c07cddb84f25ed8cdbfc4f7a5c8aa96b81f9420077522eb83fbc8680ae"
        ),
    },
}
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.34 +{elapsed:8.2f}s] {stage}{suffix}",
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


def string_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("ascii")).hexdigest()


def sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def decimal(value: Fraction, digits: int = 18) -> str:
    return format(float(value), f".{digits}g")


def dlog_coefficients(coefficients: list[Fraction]) -> list[Fraction]:
    if not coefficients or coefficients[0] == 0:
        raise ValueError("the logarithmic derivative needs a nonzero constant term")
    result: list[Fraction] = []
    for n in range(len(coefficients) - 1):
        numerator = Fraction(n + 1) * coefficients[n + 1]
        numerator -= sum(
            result[k] * coefficients[n - k] for k in range(n)
        )
        result.append(numerator / coefficients[0])
    return result


def load_sequences() -> tuple[dict[str, list[Fraction]], dict[str, object]]:
    r032_hash = sha256(R032_CERTIFICATE)
    r033_hash = sha256(R033_CERTIFICATE)
    if r032_hash != R032_EXPECTED_SHA256:
        raise AssertionError("R0.32 certificate hash mismatch")
    if r033_hash != R033_EXPECTED_SHA256:
        raise AssertionError("R0.33 certificate hash mismatch")

    r032 = json.loads(R032_CERTIFICATE.read_text(encoding="utf-8"))
    r033 = json.loads(R033_CERTIFICATE.read_text(encoding="utf-8"))
    endpoints = r032["exactEndpoints"]
    if len(endpoints) != 50:
        raise AssertionError("R0.34 requires all 50 exact R0.32 endpoints")

    b_u: list[Fraction] = []
    b_v: list[Fraction] = []
    for parameter, record in enumerate(endpoints, start=1):
        if int(record["parameter"]) != parameter:
            raise AssertionError("nonconsecutive R0.32 endpoint parameters")
        n = parameter - 1
        b_u.append((-1) ** n * Fraction(record["u"]))
        b_v.append(-(-1) ** n * Fraction(record["v"]))
    sequences = {
        "B_U": b_u,
        "B_V": b_v,
        "H_U": dlog_coefficients(b_u),
        "H_V": dlog_coefficients(b_v),
    }

    r033_summaries = {
        record["sequence"]: record
        for record in r033["finiteDiagnostics"]["sequenceSummaries"]
    }
    for name, coefficients in sequences.items():
        summary = r033_summaries[name]
        if len(coefficients) != int(summary["coefficientCount"]):
            raise AssertionError(f"R0.33 length regression failed for {name}")
        if [sign(value) for value in coefficients] != summary["coefficientSigns"]:
            raise AssertionError(f"R0.33 sign regression failed for {name}")
        if [str(value) for value in coefficients[:6]] != summary["firstSixExact"]:
            raise AssertionError(f"R0.33 coefficient regression failed for {name}")

    provenance = {
        "r032": {
            "path": str(R032_CERTIFICATE),
            "sha256": r032_hash,
            "sourceCommit": r032["git"]["commit"],
            "endpointCount": len(endpoints),
            "maximumTotalDegree": int(endpoints[-1]["totalDegree"]),
        },
        "r033": {
            "path": str(R033_CERTIFICATE),
            "sha256": r033_hash,
            "sourceCommit": r033["git"]["commit"],
            "allChecksPassed": all(r033["checks"].values()),
        },
    }
    return sequences, provenance


def hankel_matrix(
    coefficients: list[Fraction], shift: int, monomial_indices: tuple[int, ...]
) -> list[list[Fraction]]:
    return [
        [coefficients[shift + left + right] for right in monomial_indices]
        for left in monomial_indices
    ]


def sympy_determinant(matrix: list[list[Fraction]]) -> Fraction:
    exact = sp.Matrix(
        [
            [sp.Rational(value.numerator, value.denominator) for value in row]
            for row in matrix
        ]
    ).det(method="domain-ge")
    return Fraction(int(exact.p), int(exact.q))


def leibniz_determinant(matrix: list[list[Fraction]]) -> Fraction:
    order = len(matrix)
    result = Fraction(0)
    for permutation in permutations(range(order)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(order)
            for j in range(i + 1, order)
        )
        term = Fraction(-1 if inversions % 2 else 1)
        for row, column in enumerate(permutation):
            term *= matrix[row][column]
        result += term
    return result


def principal_index_sets(
    coefficient_count: int, shift: int
) -> list[tuple[int, ...]]:
    maximum_monomial = (coefficient_count - 1 - shift) // 2
    result: list[tuple[int, ...]] = []
    for order in range(1, maximum_monomial + 2):
        for tail in combinations(range(1, maximum_monomial + 1), order - 1):
            result.append((0, *tail))
    return result


def determinant_record(
    name: str,
    coefficients: list[Fraction],
    shift: int,
    indices: tuple[int, ...],
) -> dict[str, object]:
    matrix = hankel_matrix(coefficients, shift, indices)
    determinant = sympy_determinant(matrix)
    exact = str(determinant)
    return {
        "sequence": name,
        "shift": shift,
        "monomialIndices": list(indices),
        "order": len(indices),
        "coefficientIndexMatrix": [
            [shift + left + right for right in indices] for left in indices
        ],
        "determinant": exact,
        "determinantSha256": string_sha256(exact),
        "numeratorDigits": len(str(abs(determinant.numerator))),
        "denominatorDigits": len(str(determinant.denominator)),
        "decimal": decimal(determinant),
        "sign": sign(determinant),
    }


def tail_search(
    name: str, coefficients: list[Fraction], minimum_shift: int
) -> dict[str, object]:
    records: list[dict[str, object]] = []
    summaries: list[dict[str, object]] = []
    for shift in range(minimum_shift, len(coefficients)):
        shift_records = [
            determinant_record(name, coefficients, shift, indices)
            for indices in principal_index_sets(len(coefficients), shift)
        ]
        records.extend(shift_records)
        negative = [record for record in shift_records if record["sign"] < 0]
        summaries.append(
            {
                "shift": shift,
                "coefficientCountAvailable": len(coefficients) - shift,
                "principalMinorCount": len(shift_records),
                "negativeCount": len(negative),
                "negativeOrders": sorted({record["order"] for record in negative}),
            }
        )

    negative_records = [record for record in records if record["sign"] < 0]
    if not negative_records:
        raise AssertionError(f"no negative tail witness found for {name}")
    maximum_negative_shift = max(record["shift"] for record in negative_records)
    maximal_witnesses = [
        record
        for record in negative_records
        if record["shift"] == maximum_negative_shift
    ]
    expected = EXPECTED_WITNESSES[name]
    matching = [
        record
        for record in maximal_witnesses
        if tuple(record["monomialIndices"]) == expected["monomialIndices"]
    ]
    if len(matching) != 1:
        raise AssertionError(f"expected unique maximal witness for {name}")
    witness = matching[0]
    if maximum_negative_shift != expected["shift"]:
        raise AssertionError(f"unexpected maximal negative shift for {name}")
    if witness["determinantSha256"] != expected["determinantSha256"]:
        raise AssertionError(f"determinant digest mismatch for {name}")

    matrix = hankel_matrix(
        coefficients, maximum_negative_shift, tuple(witness["monomialIndices"])
    )
    independent = leibniz_determinant(matrix)
    if str(independent) != witness["determinant"]:
        raise AssertionError(f"independent determinant regression failed for {name}")
    if any(
        record["sign"] < 0 and record["shift"] > maximum_negative_shift
        for record in records
    ):
        raise AssertionError(f"maximality scan failed for {name}")

    return {
        "sequence": name,
        "coefficientCount": len(coefficients),
        "minimumTailShiftSearched": minimum_shift,
        "maximumTailShiftSearched": len(coefficients) - 1,
        "backgroundDegreeExcludedThrough": maximum_negative_shift - 1,
        "maximalNegativeShift": maximum_negative_shift,
        "witness": {
            **witness,
            "matrix": [[str(value) for value in row] for row in matrix],
            "independentLeibnizAgreement": True,
        },
        "higherShiftsHaveNoNegativeTestedPrincipalMinor": all(
            record["sign"] >= 0
            for record in records
            if record["shift"] > maximum_negative_shift
        ),
        "shiftSummaries": summaries,
        "principalMinors": records,
    }


def theorem_record(search: dict[str, object]) -> dict[str, object]:
    name = str(search["sequence"])
    degree = int(search["backgroundDegreeExcludedThrough"])
    return {
        "sequence": name,
        "statement": (
            f"for every real polynomial P with degree at most {degree}, "
            f"{name}-P is not a Stieltjes moment generating series"
        ),
        "quantifier": "all real polynomial coefficients, without fitting",
        "maximumExcludedBackgroundDegree": degree,
        "proof": (
            "all coefficients with index greater than deg(P) are unchanged; "
            "the archived exact tail Gram matrix is required to be positive "
            "semidefinite for a nonnegative measure but has negative determinant"
        ),
        "witness": search["witness"],
    }


def build_payload(arguments: argparse.Namespace) -> dict[str, object]:
    started = time.perf_counter()
    sequences, provenance = load_sequences()
    progress(
        arguments.progress,
        started,
        "verified pinned R0.32 and R0.33 inputs",
        r032Sha256=provenance["r032"]["sha256"],
        r033Sha256=provenance["r033"]["sha256"],
    )

    searches: dict[str, dict[str, object]] = {}
    for name, coefficients in sequences.items():
        searches[name] = tail_search(name, coefficients, arguments.minimum_tail_start)
        progress(
            arguments.progress,
            started,
            "completed exact tail principal-minor search",
            sequence=name,
            coefficientCount=len(coefficients),
            maximumNegativeShift=searches[name]["maximalNegativeShift"],
            backgroundDegreeExcludedThrough=searches[name][
                "backgroundDegreeExcludedThrough"
            ],
        )

    theorems = [theorem_record(searches[name]) for name in sequences]
    expected_degrees = {"B_U": 43, "B_V": 44, "H_U": 46, "H_V": 45}
    checks = {
        "pinnedR032Hash": provenance["r032"]["sha256"] == R032_EXPECTED_SHA256,
        "pinnedR033Hash": provenance["r033"]["sha256"] == R033_EXPECTED_SHA256,
        "r033RegressionPassed": provenance["r033"]["allChecksPassed"] is True,
        "allWitnessesExactlyNegative": all(
            theorem["witness"]["sign"] == -1 for theorem in theorems
        ),
        "independentDeterminantsAgree": all(
            theorem["witness"]["independentLeibnizAgreement"] is True
            for theorem in theorems
        ),
        "expectedDegreeThresholds": all(
            searches[name]["backgroundDegreeExcludedThrough"] == degree
            for name, degree in expected_degrees.items()
        ),
        "higherTailSearchExhaustedWithinWindow": all(
            search["higherShiftsHaveNoNegativeTestedPrincipalMinor"] is True
            for search in searches.values()
        ),
        "allFourPolynomialClassesExcluded": len(theorems) == 4,
    }
    if not all(checks.values()):
        failures = [name for name, passed in checks.items() if not passed]
        raise AssertionError("R0.34 checks failed: " + ", ".join(failures))

    progress(
        arguments.progress,
        started,
        "completed R0.34 polynomial-background certificate",
        passed=True,
        thresholds=expected_degrees,
    )
    return {
        "scope": {
            "result": (
                "exact universal exclusion of four bounded-degree real "
                "polynomial-background Markov/Stieltjes representations"
            ),
            "classification": (
                "exact universal non-representation theorem for finite-dimensional "
                "background classes, with finite coefficient-window thresholds"
            ),
            "limitations": [
                "the theorem allows arbitrary real polynomial coefficients but only up to the stated degrees",
                "a genuinely infinite analytic background can change every tail coefficient and is not excluded",
                "absence of a later negative minor inside the current window does not prove that a higher-degree background works",
                "the degree thresholds are maximal only for the tested principal minors inside the 50/49-coefficient window",
                "the result does not prove convergence or divergence of any Pade sequence",
                "the result neither proves nor disproves the R0.32 singularity candidate near R=-0.7495",
                "the reduced edge system is not the full three-dimensional Navier-Stokes equation",
                "no Navier-Stokes regularity or blow-up conclusion is claimed",
            ],
        },
        "input": provenance,
        "definition": {
            "testedRepresentation": (
                "C(x)=P_d(x)+integral_[0,infinity) dmu(t)/(1-x*t), "
                "where P_d is an arbitrary real polynomial and mu is nonnegative"
            ),
            "tailInvariance": (
                "if deg(P_d)<=d, residual coefficients m_n equal the exact "
                "coefficients c_n for every n>d"
            ),
            "tailGramMatrix": (
                "G_(alpha,beta)=m_(s+i_alpha+i_beta) for a finite monomial "
                "index set I; if s>d then G is the Gram matrix of "
                "t^(s/2)*t^i in L2(mu) and must be positive semidefinite"
            ),
        },
        "theorems": theorems,
        "finiteWindowAudit": {
            "minimumTailStart": arguments.minimum_tail_start,
            "searches": searches,
            "boundary": (
                "the negative witness proves the universal bounded-degree "
                "exclusion; the claim that no later tested witness exists is "
                "only exhaustive within the available coefficient window"
            ),
        },
        "checks": checks,
        "computation": {
            "backend": (
                "Python Fraction, SymPy exact domain determinants, and an "
                "independent Fraction Leibniz determinant for each theorem witness"
            ),
            "randomSeed": None,
            "wallSeconds": time.perf_counter() - started,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "sympy": sp.__version__,
        },
        "git": r028.git_source_state(),
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--minimum-tail-start", type=int, default=40)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    if not 0 <= arguments.minimum_tail_start <= 40:
        parser.error("--minimum-tail-start must lie between 0 and 40")
    return arguments


def main() -> None:
    global PROGRESS_LOG
    arguments = parse_arguments()
    if arguments.progress_log is not None:
        if arguments.progress_log.exists():
            raise SystemExit("--progress-log already exists; choose a new path")
        arguments.progress_log.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG = arguments.progress_log
    payload = build_payload(arguments)
    if arguments.check and not all(payload["checks"].values()):
        raise AssertionError("R0.34 checks failed")
    if arguments.output is None:
        json.dump(
            payload,
            sys.stdout,
            ensure_ascii=False,
            indent=2 if arguments.pretty else None,
            sort_keys=True,
        )
        sys.stdout.write("\n")
    else:
        r028.atomic_json_write(arguments.output, payload, arguments.pretty)


if __name__ == "__main__":
    main()
