#!/usr/bin/env python3
"""Independent decision and provenance checker for an R0.69W certificate."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def interval_multiply(
    left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    products = (
        left[0] * right[0],
        left[0] * right[1],
        left[1] * right[0],
        left[1] * right[1],
    )
    return min(products), max(products)


def interval_subtract(
    left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    return left[0] - right[1], left[1] - right[0]


def exact_interval(values: list[float]) -> tuple[Fraction, Fraction]:
    return Fraction.from_float(values[0]), Fraction.from_float(values[1])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--source-root", type=Path, default=Path.cwd())
    parser.add_argument("--require-head", action="store_true")
    arguments = parser.parse_args()
    document = json.loads(arguments.certificate.read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}
    checks["release"] = document.get("release") == "R0.69W"
    checks["reportedStatus"] = document.get("status") == "passed"
    mollifier = document.get("mollifier", {})
    checks["trueConvolution"] = mollifier.get("trueConvolutionCertified") is True
    checks["noFloatingQuadrature"] = mollifier.get("floatingQuadratureNodesUsed") == 0
    checks["sixthOrderEndpointTerms"] = (
        mollifier.get("endpointDistributionTermsThroughOrderSix") is True
    )
    checks["exactDyadicDistanceNodes"] = (
        mollifier.get("distanceMomentGridUsesExactDyadicEndpoints") is True
    )
    checks["centerPointDerivativeTaylor"] = (
        mollifier.get("centerMomentDerivativesUseCertifiedPointTaylor") is True
    )
    checks["pointDerivativeTaylorDocumented"] = (
        "fourth-derivative remainder"
        in mollifier.get("cutoffPointDerivatives", "")
    )
    method = document.get("method", {})
    checks["cutoffDerivativeOrderSix"] = (
        method.get("maximumCertifiedCutoffDerivativeOrder") == 6
    )
    audits = document.get("symbolicAudits", {})
    checks["angularPolynomial"] = audits.get("angularDegree") == 4
    checks["squareRootEliminated"] = audits.get("commonRotationSquareRootEliminated") is True
    checks["coreCoreZero"] = audits.get("coreCoreExactlyZero") is True
    checks["momentReductionExact"] = audits.get("directAngularToDistanceMomentsExact") is True

    coefficients = document["coefficientIntervals"]
    c0 = exact_interval(coefficients["j0"]["c0"])
    c1 = exact_interval(coefficients["j0"]["c1"])
    c2 = exact_interval(coefficients["j0"]["c2"])
    c3 = exact_interval(coefficients["j0"]["c3"])
    endpoint = exact_interval(coefficients["jMinus2"]["c0"])
    discriminant = interval_subtract(
        interval_multiply(c2, c2),
        tuple(4 * value for value in interval_multiply(c1, c3)),
    )
    checks["constantContainsZero"] = c0[0] <= 0 <= c0[1]
    checks["leadingCoefficientNegative"] = c3[1] < 0
    checks["discriminantNegative"] = discriminant[1] < 0
    checks["endpointNegative"] = endpoint[1] < 0

    partial = document.get("partial", {})
    checks["allPartialRowsCovered"] = (
        partial.get("allRowsCoveredExactlyOnce") is True
    )
    integration_audits = document.get("integrationAudits", {})
    checks["allJ0RowsCovered"] = (
        integration_audits.get("0", {}).get("allRowsCoveredExactlyOnce") is True
    )
    checks["allJMinus2RowsCovered"] = (
        integration_audits.get("-2", {}).get("allRowsCoveredExactlyOnce") is True
    )

    provenance = document.get("provenance", {})
    script = arguments.source_root / provenance.get("script", "")
    checks["scriptExists"] = script.is_file()
    checks["scriptHash"] = checks["scriptExists"] and sha256(script) == provenance.get("scriptSha256")
    checks["sourceTreeCleanDuringProduction"] = (
        provenance.get("sourceTreeDirty") is False
    )
    checks["requestedSourceMatched"] = (
        provenance.get("requestedSourceCommit")
        == provenance.get("sourceCommit")
    )
    if arguments.require_head:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=arguments.source_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        checks["sourceCommitIsHead"] = provenance.get("sourceCommit") == head

    failed = sorted(name for name, passed in checks.items() if not passed)
    report = {
        "certificate": str(arguments.certificate),
        "checks": checks,
        "exactRecomputedDiscriminant": [
            str(discriminant[0]),
            str(discriminant[1]),
        ],
        "passed": not failed,
        "failed": failed,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
