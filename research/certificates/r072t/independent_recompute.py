#!/usr/bin/env python3
"""Independent integer-ratio recomputation of the R0.72T exact spine."""

from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def ratio(value: F | int) -> str:
    value = F(value)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    # Direct series coefficients of -(1/2)sin(x)+(1/4)sin(2x).
    taylor = {
        "x": ratio(-F(1, 2) + F(2, 4)),
        "x^3": ratio(F(1, 12) - F(8, 24)),
        "x^5": ratio(-F(1, 240) + F(32, 480)),
        "x^7": ratio(F(1, 10080) - F(128, 20160)),
    }
    # Solve the two pairs after subtracting balance equations.
    gamma = F(1, 5); alpha = -3 * gamma
    delta = -F(1, 5); beta = 2 * delta
    # Centered moments on [-h/2,h/2], with h powers suppressed.
    action_fifth = F(1, 4) * F(1, 80) - F(1, 24) ** 2
    centered_second = F(1, 12)
    centered_quadratic_square = F(1, 80) - F(1, 144)
    centered_with_half_a = F(1, 4) * centered_quadratic_square
    value = {
        "schemaVersion": 1,
        "status": "passed",
        "collisionTaylor": taylor,
        "scaleExponents": {
            "alpha": ratio(alpha), "beta": ratio(beta),
            "gamma": ratio(gamma), "delta": ratio(delta),
        },
        "moments": {"second": "h^3/12", "fourth": "h^5/80"},
        "actionFifthCoefficient": ratio(action_fifth),
        "translation": {"hSquaredCoefficient": "-2/1", "hTimesHPrime": "-1/1"},
        "combinedFixedFunctionMagneticForm": {
            "potential": "V(S,X)=a*S*X+b*X^3",
            "symmetricInterval": "[-T/2,T/2]",
            "M": "M(X)=a*c+3*b*X^2",
            "A_r": "A_r(X)=M(X)*r+(a/2)*r^2",
            "A_av": "A_av=a*T^2/24",
            "D_r": "D_r=partial_X-i*A_r(X)",
            "D_av": "D_av=partial_X-i*A_av",
            "centeredMagneticShift": "A_r-A_av=M(X)*r+(a/2)*(r^2-T^2/12)",
            "moments": {
                "integral_r_squared_coefficient": ratio(centered_second),
                "integral_centered_r_squared_squared_coefficient": ratio(centered_quadratic_square),
                "after_multiplying_by_(a/2)^2": ratio(centered_with_half_a),
                "oddCross": ratio(0),
            },
            "fixedFunctionIdentity": "integral ||D_r f||_2^2 dr=T||D_av f||_2^2+integral_R[(M(X)^2*T^3/12)+(a^2*T^5/720)]|f(X)|^2 dX",
            "identityOnlyNotEvolvingSolutionObservability": True,
            "blockContractionProved": False,
        },
        "physicalDriftCoefficient": {"definition": "a=k*A*nu", "nuExponent": 1, "absKExponent": 1},
        "canonicalLift": {
            "X1": "partial_X",
            "X0": "partial_S-(X^3+6*S*X)*partial_theta",
            "brackets": [
                "[X1,X0]=-(3*X^2+6*S)*partial_theta",
                "[X0,[X1,X0]]=-6*partial_theta",
                "[X1,[X1,X0]]=-6*X*partial_theta",
                "[X1,[X1,[X1,X0]]]=-6*partial_theta",
            ],
        },
        "claimBoundary": {
            "blockContractionProved": False,
            "periodicTransferProved": False,
            "allStartSemigroupEstimateProved": False,
            "clayMillenniumProblemSolved": False,
        },
    }
    if taylor != {"x": "0/1", "x^3": "-1/4", "x^5": "1/16", "x^7": "-1/160"}:
        raise RuntimeError("independent Taylor check failed")
    if action_fifth != F(1, 720):
        raise RuntimeError("independent action check failed")
    if (
        centered_second != F(1, 12)
        or centered_quadratic_square != F(1, 180)
        or centered_with_half_a != F(1, 720)
    ):
        raise RuntimeError("independent centered magnetic moment check failed")
    (ROOT / "independent.json").write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("R0.72T independent recomputation: passed")


if __name__ == "__main__":
    main()
