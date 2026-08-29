#!/usr/bin/env python3
"""Materialize an independent standard-library recomputation for R0.73C.

This program imports neither the certificate producer nor either numerical
producer.  It independently reads the serialized proof objects, redoes the
exact C3 ledger, resolves the C4 endpoint signs from exact binary/Decimal
endpoints, checks the Decimal implementation's import boundary, and records
the finite diagnostics without promoting them to a theorem.
"""

from __future__ import annotations

import argparse
import ast
from decimal import Decimal
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
EXPERIMENT = ROOT / "experiments/r073c"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "independent_recompute.json")
    parser.add_argument("--check-only", action="store_true")
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_record(path: Path, display: str) -> dict[str, Any]:
    return {"bytes": path.stat().st_size, "path": display, "sha256": sha256(path)}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> Any:
    def reject_constant(value: str) -> None:
        raise ValueError(f"non-finite JSON constant {value} in {path}")

    return json.loads(path.read_text(), parse_constant=reject_constant)


def binary_value(record: dict[str, Any]) -> Fraction:
    require(set(record) == {"bitcount", "exponent", "mantissa", "sign"},
            "unexpected binary endpoint fields")
    mantissa = record["mantissa"]
    exponent = record["exponent"]
    require(type(mantissa) is int and mantissa > 0, "invalid mantissa")
    require(type(exponent) is int and type(record["bitcount"]) is int,
            "invalid binary integer field")
    require(record["bitcount"] == mantissa.bit_length(), "bitcount mismatch")
    require(type(record["sign"]) is int and record["sign"] in (0, 1), "invalid sign")
    value = Fraction(mantissa) * (
        2 ** exponent if exponent >= 0 else Fraction(1, 2 ** (-exponent))
    )
    return -value if record["sign"] else value


def primary_interval(row: dict[str, Any], key: str) -> tuple[Fraction, Fraction]:
    result = tuple(binary_value(item) for item in row[key]["binaryEndpoints"])
    require(len(result) == 2 and result[0] <= result[1], f"invalid {key}")
    return result[0], result[1]


def decimal_interval(row: dict[str, Any], key: str) -> tuple[Fraction, Fraction]:
    result = (
        Fraction(Decimal(row[key]["lower"])),
        Fraction(Decimal(row[key]["upper"])),
    )
    require(result[0] <= result[1], f"invalid Decimal {key}")
    return result


def imported_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def exact_c3() -> dict[str, Any]:
    # phi_xx=(3/2)s-(9/4)s^3 and (W''/W)phi=(3/2)s-4s^3.
    h_coefficients = (
        -Fraction(3, 2) + Fraction(3, 2),
        Fraction(9, 4) - Fraction(4),
    )
    spectrum = [Fraction((n + 3) ** 2 - 16, 4) for n in range(8)]
    checks = {
        "factorization": (
            -Fraction(1, 2) * 2 + Fraction(1, 4) * 4 == 0
            and Fraction(1, 4) * 4 * (-2) == -2
        ),
        "neutralIdentity": h_coefficients == (Fraction(0), Fraction(-7, 4)),
        "periodicC2NotC3": Fraction(-3, 4) != Fraction(3, 4),
        "spectrumFirstFour": spectrum[:4] == [
            Fraction(-7, 4), Fraction(0), Fraction(9, 4), Fraction(5)
        ],
        "uniqueNegativeFromFormula": spectrum[0] < 0 <= spectrum[1]
            and all(spectrum[index] < spectrum[index + 1]
                    for index in range(len(spectrum) - 1)),
    }
    require(all(checks.values()), "independent C3 algebra failed")
    return {
        "checks": checks,
        "gammaSquared": "7/4",
        "mode": "abs(sin(x/2))^3",
        "singularEigenvalue": "-7/4",
        "spectrumFormula": "((n+3)^2-16)/4",
    }


def main() -> int:
    args = parse_args()
    source = Path(__file__).resolve()
    source_hash_before = sha256(source)
    c3 = exact_c3()

    primary: dict[str, Any] = {}
    primary_intervals: dict[str, dict[str, tuple[Fraction, Fraction]]] = {}
    for filename, run_id in (
        ("canonical_interval_run_a.json", "partition-a"),
        ("canonical_interval_run_b.json", "partition-b"),
    ):
        path = EXPERIMENT / filename
        data = load_json(path)
        require(data["status"] == "passed" and data["runId"] == run_id,
                f"primary run failed: {run_id}")
        require(len(data["results"]) == 2, f"primary result count failed: {run_id}")
        by_eta: dict[str, tuple[Fraction, Fraction]] = {}
        records: dict[str, Any] = {}
        for row in data["results"]:
            eta = row["eta"]
            require(eta not in by_eta, f"duplicate primary eta: {run_id}/{eta}")
            trace = primary_interval(row, "traceMinusTwo")
            imag = primary_interval(row, "traceImag")
            require(imag[0] <= 0 <= imag[1], f"primary trace-imag failed: {run_id}/{eta}")
            expected = "negative" if eta == "0.3407" else "positive" if eta == "0.3410" else ""
            sign = "negative" if trace[1] < 0 else "positive" if trace[0] > 0 else "unresolved"
            require(expected and sign == expected == row["sign"],
                    f"primary sign failed: {run_id}/{eta}")
            by_eta[eta] = trace
            records[eta] = {
                "lower": f"{trace[0].numerator}/{trace[0].denominator}",
                "strictSign": sign,
                "upper": f"{trace[1].numerator}/{trace[1].denominator}",
            }
        require(set(by_eta) == {"0.3407", "0.3410"}, "primary eta inventory failed")
        primary_intervals[run_id] = by_eta
        primary[run_id] = {"file": file_record(path, f"experiments/r073c/{filename}"),
                           "traceMinusTwo": records}

    decimal_path = EXPERIMENT / "canonical_decimal_interval_validation.json"
    decimal_source = EXPERIMENT / "independent_decimal_monodromy_validator.py"
    decimal_data = load_json(decimal_path)
    forbidden = {"mpmath", "numpy", "scipy", "research"}
    require(decimal_data["status"] == "passed"
            and all(decimal_data["checks"].values())
            and all(decimal_data["arithmetic"]["checks"].values())
            and decimal_data["source"]["sha256"] == sha256(decimal_source)
            and decimal_data["source"]["bytes"] == decimal_source.stat().st_size
            and not (forbidden & imported_roots(decimal_source)),
            "Decimal status or independence boundary failed")
    require(len(decimal_data["results"]) == 2, "Decimal result count failed")
    decimal_by_eta: dict[str, tuple[Fraction, Fraction]] = {}
    decimal_records: dict[str, Any] = {}
    for row in decimal_data["results"]:
        eta = row["eta"]
        require(eta not in decimal_by_eta, f"duplicate Decimal eta: {eta}")
        trace = decimal_interval(row, "traceMinusTwo")
        imag = decimal_interval(row, "traceImag")
        det_real = decimal_interval(row, "determinantReal")
        det_imag = decimal_interval(row, "determinantImag")
        require(imag[0] <= 0 <= imag[1]
                and det_real[0] <= 1 <= det_real[1]
                and det_imag[0] <= 0 <= det_imag[1],
                f"Decimal sentinel failed: {eta}")
        expected = "negative" if eta == "0.3407" else "positive" if eta == "0.3410" else ""
        sign = "negative" if trace[1] < 0 else "positive" if trace[0] > 0 else "unresolved"
        require(expected and sign == expected == row["sign"], f"Decimal sign failed: {eta}")
        require(all(row["checks"].values()), f"Decimal row checks failed: {eta}")
        decimal_by_eta[eta] = trace
        decimal_records[eta] = {
            "determinantContainsOnePlusZeroI": True,
            "lower": row["traceMinusTwo"]["lower"],
            "strictSign": sign,
            "traceImagContainsZero": True,
            "upper": row["traceMinusTwo"]["upper"],
        }
    require(set(decimal_by_eta) == {"0.3407", "0.3410"},
            "Decimal eta inventory failed")
    require(all(
        decimal_by_eta[eta][0] <= interval[0] <= interval[1] <= decimal_by_eta[eta][1]
        for eta in decimal_by_eta
        for interval in (primary_intervals["partition-a"][eta],
                         primary_intervals["partition-b"][eta])
    ), "primary/Decimal containment failed")

    finite_path = EXPERIMENT / "canonical_independent_fourier_validation.json"
    finite = load_json(finite_path)
    require(finite["status"] == "passed" and all(finite["checks"].values()),
            "finite diagnostic validation failed")
    require(finite["claimBoundary"]["infiniteDimensionalSpectrumProved"] is False
            and finite["claimBoundary"]["continuousContourEnclosed"] is False,
            "finite evidence boundary failed")
    candidate = next(row for row in finite["recomputedSentinels"] if row["N"] == 128)
    require(0.17035 < candidate["leadingReal"] < 0.17050,
            "finite candidate outside certified bracket")

    require(sha256(source) == source_hash_before, "independent source changed during run")
    result = {
        "c3": c3,
        "c4": {
            "analyticBridgeRequired": True,
            "etaOpenInterval": ["0.3407", "0.3410"],
            "independentDecimal": {
                "file": file_record(decimal_path, "experiments/r073c/canonical_decimal_interval_validation.json"),
                "importsMpmath": False,
                "importsPrimaryProducer": False,
                "source": file_record(decimal_source,
                                      "experiments/r073c/independent_decimal_monodromy_validator.py"),
                "traceMinusTwo": decimal_records,
            },
            "primary": primary,
            "sigmaOpenInterval": ["0.17035", "0.17050"],
            "strictOppositeSigns": True,
        },
        "claimBoundary": {
            "c5FastTimeTransferProved": False,
            "clayProblemSolved": False,
            "finiteFourierEvidenceIsProof": False,
            "nonlinearNavierStokesProved": False,
            "rootUniquenessProved": False,
        },
        "finiteDiagnostic": {
            "candidateAtN128": candidate["leadingReal"],
            "file": file_record(finite_path,
                                "experiments/r073c/canonical_independent_fourier_validation.json"),
            "scope": "finite matrices and sampled contour only",
        },
        "schemaVersion": "r073c-independent-recompute-v1",
        "source": file_record(source, "research/certificates/r073c/independent_recompute.py"),
        "status": "passed",
    }
    if not args.check_only:
        args.output.write_text(canonical(result))
    print(canonical(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
