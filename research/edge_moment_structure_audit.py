#!/usr/bin/env python3
"""R0.33 exact Hankel obstruction to a positive-measure Pade route.

The R0.32 certificate contains 50 exact charge-one endpoint coefficients.
After the sign change x=-R, this audit constructs the normalized transport
series

    B_U(x) = hat U_1(-x),       B_V(x) = -hat V_1(-x),

and their logarithmic derivatives H_F=B_F'/B_F.  A Markov/Stieltjes moment
representation M(x)=integral (1-x*t)^(-1) dmu(t), with nonnegative mu on
[0,infinity), forces both the ordinary and shifted Hankel moment matrices to
be positive semidefinite.  Four exact low-order witnesses disprove that
representation for B_U, B_V, H_U, and H_V.

The exclusion is an all-order function-class theorem: later coefficients
cannot repair a negative principal minor made from the first few exact
coefficients.  It does not rule out other Pade convergence classes, analytic
background subtraction, signed or complex measures, or the R0.32 candidate
near R=-0.7495.  It has no direct Navier--Stokes regularity consequence.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
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
R032_EXPECTED_SHA256 = (
    "bd70ed05779631b729e89c269f82d287da361fdcea34e3c42703a712222f5575"
)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.33 +{elapsed:8.2f}s] {stage}{suffix}",
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


def sign(value: Fraction | sp.Rational) -> int:
    return (value > 0) - (value < 0)


def decimal(value: Fraction, digits: int = 18) -> str:
    return format(float(value), f".{digits}g")


def fraction_record(value: Fraction) -> dict[str, object]:
    return {
        "exact": str(value),
        "decimal": decimal(value),
        "sign": sign(value),
    }


def load_endpoint_sequences() -> tuple[dict[str, list[Fraction]], dict[str, object]]:
    actual_hash = sha256(R032_CERTIFICATE)
    if actual_hash != R032_EXPECTED_SHA256:
        raise AssertionError(
            "R0.32 certificate hash mismatch: "
            f"expected {R032_EXPECTED_SHA256}, got {actual_hash}"
        )
    payload = json.loads(R032_CERTIFICATE.read_text(encoding="utf-8"))
    endpoints = payload["exactEndpoints"]
    if len(endpoints) != 50:
        raise AssertionError("R0.33 requires the 50 exact R0.32 endpoints")

    u: list[Fraction] = []
    v: list[Fraction] = []
    for index, record in enumerate(endpoints, start=1):
        if int(record["parameter"]) != index:
            raise AssertionError("R0.32 endpoint parameters are not consecutive")
        if int(record["totalDegree"]) != 3 * index - 1:
            raise AssertionError("R0.32 endpoint total degree is inconsistent")
        n = index - 1
        u.append((-1) ** n * Fraction(record["u"]))
        v.append(-(-1) ** n * Fraction(record["v"]))

    provenance = {
        "path": str(R032_CERTIFICATE),
        "sha256": actual_hash,
        "sourceCommit": payload["git"]["commit"],
        "sourceDirty": payload["git"]["dirty"],
        "endpointCount": len(endpoints),
        "maximumEndpointParameter": int(endpoints[-1]["parameter"]),
        "maximumTotalDegree": int(endpoints[-1]["totalDegree"]),
    }
    return {"B_U": u, "B_V": v}, provenance


def dlog_coefficients(coefficients: list[Fraction]) -> list[Fraction]:
    """Return coefficients of B'/B through the available exact order."""

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


def exact_determinant(matrix: list[list[Fraction]]) -> Fraction:
    sympy_matrix = sp.Matrix(
        [
            [sp.Rational(value.numerator, value.denominator) for value in row]
            for row in matrix
        ]
    )
    determinant = sympy_matrix.det(method="domain-ge")
    return Fraction(int(determinant.p), int(determinant.q))


def hankel_matrix(
    coefficients: list[Fraction], order: int, shift: int
) -> list[list[Fraction]]:
    return [
        [coefficients[i + j + shift] for j in range(order)]
        for i in range(order)
    ]


def hankel_determinant(
    coefficients: list[Fraction], order: int, shift: int
) -> Fraction:
    return exact_determinant(hankel_matrix(coefficients, order, shift))


def witness_record(
    name: str,
    coefficients: list[Fraction],
    order: int,
    shift: int,
    expected: Fraction,
) -> dict[str, object]:
    matrix = hankel_matrix(coefficients, order, shift)
    determinant = exact_determinant(matrix)
    if determinant != expected or determinant >= 0:
        raise AssertionError(f"unexpected witness for {name}: {determinant}")
    return {
        "sequence": name,
        "matrixKind": "shifted Hankel" if shift else "ordinary Hankel",
        "order": order,
        "shift": shift,
        "matrix": [[str(value) for value in row] for row in matrix],
        "determinant": fraction_record(determinant),
        "consequence": (
            "not a Stieltjes moment sequence; hence no nonnegative-measure "
            "Markov representation M(x)=integral dmu(t)/(1-x*t)"
        ),
    }


def turan_records(name: str, coefficients: list[Fraction]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for n in range(1, len(coefficients) - 1):
        minor = coefficients[n - 1] * coefficients[n + 1] - coefficients[n] ** 2
        normalized = minor / coefficients[n] ** 2
        records.append(
            {
                "sequence": name,
                "index": n,
                "minor": str(minor),
                "minorSign": sign(minor),
                "normalized": str(normalized),
                "normalizedDecimal": decimal(normalized),
            }
        )
    return records


def leading_hankel_records(
    sequences: dict[str, list[Fraction]], maximum_order: int
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for name, coefficients in sequences.items():
        for shift in (0, 1):
            for order in range(1, maximum_order + 1):
                if 2 * (order - 1) + shift >= len(coefficients):
                    raise ValueError("not enough coefficients for requested Hankel order")
                determinant = hankel_determinant(coefficients, order, shift)
                records.append(
                    {
                        "sequence": name,
                        "matrixKind": "shifted" if shift else "ordinary",
                        "shift": shift,
                        "order": order,
                        "determinant": str(determinant),
                        "sign": sign(determinant),
                    }
                )
    return records


def sequence_summary(name: str, coefficients: list[Fraction]) -> dict[str, object]:
    signs = [sign(value) for value in coefficients]
    return {
        "sequence": name,
        "coefficientCount": len(coefficients),
        "positiveCount": signs.count(1),
        "negativeCount": signs.count(-1),
        "zeroCount": signs.count(0),
        "firstSixExact": [str(value) for value in coefficients[:6]],
        "coefficientSigns": signs,
    }


def build_payload(arguments: argparse.Namespace) -> dict[str, object]:
    started = time.perf_counter()
    base, provenance = load_endpoint_sequences()
    progress(
        arguments.progress,
        started,
        "verified pinned R0.32 certificate",
        sha256=provenance["sha256"],
        endpointCount=provenance["endpointCount"],
    )

    sequences = {
        **base,
        "H_U": dlog_coefficients(base["B_U"]),
        "H_V": dlog_coefficients(base["B_V"]),
    }
    progress(
        arguments.progress,
        started,
        "constructed sign-transformed and D-log sequences",
        baseCoefficientCount=len(base["B_U"]),
        dlogCoefficientCount=len(sequences["H_U"]),
    )

    witnesses = [
        witness_record(
            "B_U", base["B_U"], 2, 0, Fraction(-437, 24192)
        ),
        witness_record(
            "B_V", base["B_V"], 2, 1, Fraction(-43522897, 685843200)
        ),
        witness_record("H_U", sequences["H_U"], 1, 1, Fraction(-32, 63)),
        witness_record(
            "H_V", sequences["H_V"], 2, 0, Fraction(-29699111, 12700800)
        ),
    ]
    progress(
        arguments.progress,
        started,
        "certified four exact negative moment witnesses",
        rejectedSequences=[record["sequence"] for record in witnesses],
    )

    turan = (
        turan_records("B_U", base["B_U"])
        + turan_records("B_V", base["B_V"])
    )
    hankel = leading_hankel_records(sequences, arguments.maximum_hankel_order)
    progress(
        arguments.progress,
        started,
        "completed finite exact sign diagnostics",
        turanRecordCount=len(turan),
        hankelRecordCount=len(hankel),
        maximumHankelOrder=arguments.maximum_hankel_order,
    )

    witness_by_name = {record["sequence"]: record for record in witnesses}
    checks = {
        "pinnedInputHash": provenance["sha256"] == R032_EXPECTED_SHA256,
        "consecutiveFiftyEndpoints": provenance["endpointCount"] == 50,
        "baseCoefficientsPositiveThroughIndex49": all(
            value > 0 for coefficients in base.values() for value in coefficients
        ),
        "B_UOrdinaryHankelWitness": witness_by_name["B_U"]["determinant"]["exact"]
        == "-437/24192",
        "B_VShiftedHankelWitness": witness_by_name["B_V"]["determinant"]["exact"]
        == "-43522897/685843200",
        "H_UShiftedOrderOneWitness": witness_by_name["H_U"]["determinant"]["exact"]
        == "-32/63",
        "H_VOrdinaryHankelWitness": witness_by_name["H_V"]["determinant"]["exact"]
        == "-29699111/12700800",
        "allFourRepresentationsRejected": all(
            record["determinant"]["sign"] == -1 for record in witnesses
        ),
        "finiteHUAlternationThroughIndex48": all(
            sign(value) == (1 if index % 2 == 0 else -1)
            for index, value in enumerate(sequences["H_U"])
        ),
        "finiteHVPositivityThroughIndex48": all(
            value > 0 for value in sequences["H_V"]
        ),
    }
    if not all(checks.values()):
        failures = [name for name, passed in checks.items() if not passed]
        raise AssertionError("R0.33 checks failed: " + ", ".join(failures))

    u_turan = [record for record in turan if record["sequence"] == "B_U"]
    v_turan = [record for record in turan if record["sequence"] == "B_V"]
    payload = {
        "scope": {
            "result": (
                "exact exclusion of the direct nonnegative-measure "
                "Markov/Stieltjes representation for B_U, B_V, H_U, and H_V"
            ),
            "classification": (
                "all-order function-class exclusion from exact low-order "
                "witnesses, plus finite degree-49 diagnostics"
            ),
            "limitations": [
                "the theorem excludes only the direct positive-measure Markov/Stieltjes moment class",
                "it does not exclude generalized Stieltjes forms after subtraction or another transform",
                "it does not exclude signed or complex measures or other Pade convergence theorems",
                "it neither proves nor disproves the R0.32 singularity candidate near R=-0.7495",
                "positivity and sign patterns observed through 50 coefficients remain finite diagnostics",
                "the reduced edge system is not the full three-dimensional Navier-Stokes equation",
                "no Navier-Stokes regularity or blow-up conclusion is claimed",
            ],
        },
        "input": provenance,
        "definition": {
            "normalizedTransport": "hat F_1(R)=F_1(R)/R",
            "signTransformed": {
                "B_U": "B_U(x)=hat U_1(-x)=sum_(n>=0) b^U_n x^n",
                "B_V": "B_V(x)=-hat V_1(-x)=sum_(n>=0) b^V_n x^n",
            },
            "dlog": "H_F(x)=B_F'(x)/B_F(x)",
            "testedRepresentation": (
                "M(x)=integral_[0,infinity) dmu(t)/(1-x*t), mu nonnegative; "
                "then m_n=integral t^n dmu(t)"
            ),
            "necessaryCondition": (
                "both (m_(i+j)) and (m_(i+j+1)) are positive semidefinite "
                "because their quadratic forms are integrals of p(t)^2 "
                "and t*p(t)^2 against nonnegative mu"
            ),
        },
        "theorem": {
            "statement": (
                "None of B_U, B_V, H_U, or H_V admits the tested direct "
                "nonnegative-measure Markov/Stieltjes representation"
            ),
            "proofBoundary": (
                "each exact negative determinant is a principal minor of a "
                "required positive-semidefinite moment matrix; higher "
                "coefficients cannot change that minor"
            ),
            "witnesses": witnesses,
        },
        "finiteDiagnostics": {
            "sequenceSummaries": [
                sequence_summary(name, coefficients)
                for name, coefficients in sequences.items()
            ],
            "turanDefinition": "Delta_n=b_(n-1)*b_(n+1)-b_n^2",
            "turanRecords": turan,
            "negativeTuranCounts": {
                "B_U": sum(record["minorSign"] < 0 for record in u_turan),
                "B_V": sum(record["minorSign"] < 0 for record in v_turan),
            },
            "hankelDeterminants": hankel,
            "maximumHankelOrder": arguments.maximum_hankel_order,
            "boundary": (
                "all coefficient-sign, Turan, and higher-order Hankel tables "
                "are finite exact diagnostics; only the four displayed "
                "negative witnesses are used for the class-exclusion theorem"
            ),
        },
        "checks": checks,
        "computation": {
            "backend": "Python Fraction plus SymPy exact rational determinants",
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
    progress(
        arguments.progress,
        started,
        "completed R0.33 moment-structure certificate",
        passed=True,
        wallSeconds=payload["computation"]["wallSeconds"],
    )
    return payload


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-hankel-order", type=int, default=12)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    if not 2 <= arguments.maximum_hankel_order <= 24:
        parser.error("--maximum-hankel-order must lie between 2 and 24")
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
        raise AssertionError("R0.33 checks failed")
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
