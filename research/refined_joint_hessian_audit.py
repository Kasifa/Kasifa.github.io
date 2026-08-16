#!/usr/bin/env python3
"""Exact joint Hessian at the refined rational R0.17 point.

R0.18 isolates a unique stationary point on the antisymmetric (p,q,x)
chart.  The stationary coordinates are not rational.  This companion audit
therefore evaluates the full five-variable amplitude--polarization Hessian at
the nearby rational R0.17 point, where the conic parametrization makes every
normalization coefficient rational.

Positive definiteness here is exact, but it is not by itself a proof of
positive definiteness at the isolated stationary point.  Transferring the
two common-rotation curvatures across that remaining gap requires a separate
interval derivative bound.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json

import finite_candidate_second_variation_audit as joint


joint.M_PARAMETER = Fraction(429, 2500)
joint.N_PARAMETER = Fraction(4271, 10000)
joint.X_CANDIDATE = Fraction(26213, 10000)


def audit() -> dict[str, object]:
    result = joint.audit()
    result["scope"] = "joint second variations at the refined R0.17 point"
    return result


def validate(result: dict[str, object]) -> None:
    assert result["parameters"]["m"] == "429/2500"
    assert result["parameters"]["n"] == "4271/10000"
    assert result["parameters"]["x"] == "26213/10000"
    assert result["derivativeKeyCount"] == 15
    assert result["aggregatedFrequencyCount"] == 334
    assert all(
        count == 0
        for count in result["uncancelledLaurentPoleCounts"].values()
    )
    quotient = result["quotient"]
    assert abs(
        quotient["externalOverTargetDecimal"] - 15.801443619697901
    ) < 1e-12
    assert all(quotient["exactPairSymmetryChecks"].values())
    assert all(
        record["sign"] > 0
        for record in quotient["jointHessianSylvesterMinors"].values()
    )
    assert quotient["jointHessianSylvesterMinors"][
        "symmetricDeterminant"
    ]["exactDigest"] == (
        "274e2bffa776637ce9e5b98e0d14f8b0cbbaac9d2a3cced64acfc82d36a172dd"
    )
    assert quotient["jointHessianSylvesterMinors"][
        "antisymmetricJointDeterminant"
    ]["exactDigest"] == (
        "c0a9079bdb461dd10f5ae78f2c95a869ba384713b80c229c01148c4e0bc02de0"
    )
    assert quotient["jointHessianPositiveDefiniteCertified"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    result = audit()
    if arguments.check:
        validate(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
