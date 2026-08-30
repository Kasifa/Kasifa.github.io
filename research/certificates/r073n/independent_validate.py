#!/usr/bin/env python3
"""Independent Decimal/Fraction reconstruction of the R0.73N diagnostic."""

from __future__ import annotations

import csv
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fraction(value: str) -> Fraction:
    return Fraction(value)


def dec_fraction(value: Fraction) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


def exp_negative(argument: Decimal, threshold: Decimal) -> Decimal:
    """Compute exp(-argument) by range-reduced Taylor series."""
    if argument < 0:
        raise ValueError("argument must be nonnegative")
    reduced = +argument
    squarings = 0
    while reduced > Decimal("0.125"):
        reduced /= 2
        squarings += 1
    term = Decimal(1)
    total = Decimal(1)
    index = 0
    while True:
        index += 1
        term *= -reduced / index
        total += term
        if abs(term) < threshold:
            break
        if index > 10000:
            raise RuntimeError("Taylor series did not converge")
    for _ in range(squarings):
        total *= total
    return +total


def main() -> None:
    config_path = HERE / "config.json"
    diagnostic_path = HERE / "diagnostic.json"
    csv_path = HERE / "source-data.csv"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    diagnostic = json.loads(diagnostic_path.read_text(encoding="utf-8"))
    precision = 120
    with localcontext() as context:
        context.prec = precision
        threshold = Decimal(1).scaleb(-(precision + 5))
        t_star_q = fraction(config["physicalTimeEnd"])
        d_star_q = fraction(config["profileTimeEnd"])
        rational_lower_q = fraction(config["jStarRationalLower"])
        action_upper_q = fraction(config["inheritedActionUpper"])
        action_lower_q = fraction(config["inheritedActionLower"])
        t_star = dec_fraction(t_star_q)

        def strain(t: Decimal) -> Decimal:
            return exp_negative(4 * t, threshold) + exp_negative(16 * t, threshold)

        def cumulative(t: Decimal) -> Decimal:
            return ((1 - exp_negative(4 * t, threshold)) / 4
                    + (1 - exp_negative(16 * t, threshold)) / 16)

        j_star = cumulative(t_star)
        primary_j_star = Decimal(diagnostic["highPrecision"]["jStar"])
        j_tolerance = Decimal(config["tolerances"]["independentJStarAbs"])
        sentinel_tolerance = Decimal(config["tolerances"]["independentSentinelAbs"])
        validations = []
        maximum_difference = Decimal(0)
        for label in config["independentSentinelTimes"]:
            t_q = fraction(label)
            t = dec_fraction(t_q)
            value = cumulative(t)
            identity_derivative = strain(t)
            # Independent centered differences only diagnose the derivative;
            # the exact formula itself is reconstructed above.
            h = Decimal("1e-25") if t != 0 else Decimal("1e-25")
            if t == 0:
                difference_quotient = (4 * cumulative(h) - cumulative(2 * h)) / (2 * h)
            else:
                difference_quotient = (cumulative(t + h) - cumulative(t - h)) / (2 * h)
            derivative_difference = abs(difference_quotient - identity_derivative)
            maximum_difference = max(maximum_difference, derivative_difference)
            validations.append({
                "time": label,
                "cumulativeJ": format(value, ".90E"),
                "strainEnvelope": format(identity_derivative, ".90E"),
                "finiteDifferenceDerivativeAbs": format(derivative_difference, ".30E"),
            })

        with csv_path.open("r", encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        counts = {
            "strainSamples": sum(row["record_type"] == "strain_sample" for row in rows),
            "cumulativeSamples": sum(row["record_type"] == "cumulative_sample" for row in rows),
            "markedBasepointSamples": sum(
                row["record_type"] == "marked_basepoint_sample" for row in rows
            ),
            "totalRows": len(rows),
        }
        configured_strain = int(config["strainGrid"]["count"])
        configured_basepoints = (
            (int(config["markedBasepointGrid"]["lambdaEnd"])
             - int(config["markedBasepointGrid"]["lambdaStart"]))
            // int(config["markedBasepointGrid"]["lambdaStep"]) + 1
        )
        checks = {
            "independentImplementationDoesNotImportPrimary": True,
            "profilePhysicalEndpointIdentityExact": 4 * t_star_q == d_star_q,
            "independentJStarAgrees": abs(j_star - primary_j_star) < j_tolerance,
            "jInfinityExactFraction": fraction(config["jInfinity"]) == Fraction(5, 16),
            "analyticLowerWitnessExact": (
                d_star_q / 2 - 5 * d_star_q * d_star_q / 8
                == rational_lower_q == Fraction(359, 324000)
            ),
            "rationalChainExact": rational_lower_q > action_upper_q > action_lower_q,
            "independentJStarStrictlyAboveWitness": j_star > dec_fraction(rational_lower_q),
            "sentinelDerivativeChecks": maximum_difference < sentinel_tolerance,
            "sourceDataHashBound": sha256(csv_path) == diagnostic["sourceData"]["sha256"],
            "sourceDataCountsExact": (
                counts["strainSamples"] == configured_strain
                and counts["markedBasepointSamples"] == configured_basepoints
                and counts == {
                    key: diagnostic["sourceData"][key] for key in counts
                }
            ),
        }
        if not all(checks.values()):
            failed = [key for key, value in checks.items() if not value]
            raise RuntimeError("independent validation failed: " + ", ".join(failed))
        result = {
            "schemaVersion": "r073n-independent-decimal-validation-v1",
            "release": "R0.73N",
            "status": "passed",
            "allChecksPass": True,
            "method": {
                "arithmetic": "Python Decimal at 120 digits plus exact Fraction comparisons",
                "exponential": "range-reduced Taylor series; no mpmath import",
                "derivativeDiagnostic": "centered finite difference at six sentinel times",
                "importsPrimaryProducer": False,
            },
            "jStar": format(j_star, ".100E"),
            "primaryJStarAbsoluteDifference": format(abs(j_star - primary_j_star), ".30E"),
            "maximumSentinelDerivativeDifference": format(maximum_difference, ".30E"),
            "validations": validations,
            "sourceData": {
                "path": "research/certificates/r073n/source-data.csv",
                "sha256": sha256(csv_path),
                **counts,
            },
            "checks": checks,
            "claimBoundary": config["claimBoundary"],
        }
    (HERE / "independent_validation.json").write_text(canonical(result), encoding="utf-8")
    print(canonical({"status": "passed", "checks": len(checks)}), end="")


if __name__ == "__main__":
    main()
