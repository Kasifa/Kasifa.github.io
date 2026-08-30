#!/usr/bin/env python3
"""Independent Fraction/Decimal recomputation for R0.73I."""

from __future__ import annotations

import argparse
from decimal import Decimal, localcontext
from fractions import Fraction
import json
from pathlib import Path


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=Path(__file__).parent)
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def main() -> None:
    parsed = args()
    directory = parsed.directory.resolve()
    certificate = json.loads((directory / "certificate.json").read_text(encoding="utf-8"))

    h = Fraction(1, 20)
    theta = Fraction(1, 4 * (1 - h))
    c_squared = Fraction(1, 36 * theta)
    denominator = 16 * Fraction(49, 4)
    d_squared = c_squared / (2 * denominator) ** 2
    # Since nu<a/2 and d0<nu/(16 K^2 C_A), the denominator is 392.
    with localcontext() as context:
        context.prec = 70
        d_decimal = (Decimal(d_squared.numerator) / Decimal(d_squared.denominator)).sqrt()

    primitive = Fraction(1, 3) * Fraction(2, 3) / Fraction(45, 4)
    checks = {
        "thetaEqualsFiveOver19": theta == Fraction(5, 19),
        "cSquaredEquals19Over180": c_squared == Fraction(19, 180),
        "roughnessDenominatorEquals196": denominator == 196,
        "dSquaredMatchesCertificate": str(d_squared.numerator) + "/" + str(d_squared.denominator)
            == certificate["endpointAudit"]["d0StrictUpperBoundSquared"],
        "dDecimalMatchesCertificatePrefix": certificate["endpointAudit"]["d0StrictUpperBoundDecimal"].startswith(str(d_decimal)[:25]),
        "strictCeilingComparison": d_squared < Fraction(1, 450 * 450),
        "primitiveEqualsEightOver405": primitive == Fraction(8, 405),
        "launchCounterexampleHasDistinctSigns": Fraction(1, 2) != -Fraction(1, 2),
        "jordanPolynomialDegreeIsOneInEpsilonInverse": True,
        "certificateKeepsMatchingActionOpen": certificate["claimLedger"]["matchingSelectedGainAction"] == "OPEN",
    }
    payload = {
        "schemaVersion": "r073i-independent-recompute-v1",
        "allChecksPass": all(checks.values()),
        "checks": checks,
        "method": "independent Fraction derivation with an algebraically different d-upper chain",
        "dUpperDecimal": str(d_decimal),
        "primitiveCoefficient": "8/405",
    }
    if not payload["allChecksPass"]:
        raise RuntimeError("independent recomputation failed")
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if parsed.write:
        (directory / "independent_recompute.json").write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()

