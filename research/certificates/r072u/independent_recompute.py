#!/usr/bin/env python3
"""Independent rational recomputation for the R0.72U certificate.

This route obtains the probe moments from the beta-integral recurrence rather
than expanding the degree-eight polynomial used by the primary producer.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def q(value: F | int) -> str:
    value = F(value)
    return f"{value.numerator}/{value.denominator}"


def compute() -> dict:
    # For I_n=int_{-1}^{1} x^(2n)(1-x^2)^4 dx,
    # I_(n+1)/I_n=(2n+1)/(2n+11).  Normalization makes mu_0=1.
    mu0 = F(1)
    mu2 = mu0 * F(1, 11)
    mu4 = mu2 * F(3, 13)
    t_half = F(1)
    threshold = 2 * t_half + mu4 / (3 * mu2)
    floor = 3 * mu2 * threshold
    positive_edge = mu4 + 6 * (threshold - t_half) * mu2
    negative_edge = mu4 + 6 * (-threshold + t_half) * mu2

    mean_s2 = F(1, 3)
    mean_s4 = F(1, 5)
    gauge_floor = 9 * mean_s4 - 6 * mean_s2 + 1

    return {
        "schemaVersion": 1,
        "status": "passed",
        "method": "beta-integral recurrence for rho moments; direct centered time moments for the fixed gauge",
        "probe": {
            "formula": "rho(X)=(315/256)*(1-X^2)^4*1_{[-1,1]}(X)",
            "normalization": q(mu0),
            "momentRecurrence": "mu_(2n+2)/mu_(2n)=(2*n+1)/(2*n+11)",
        },
        "moments": {
            "mu0": q(mu0),
            "mu2": q(mu2),
            "mu4": q(mu4),
            "definition": "mu_j=integral_{-1}^{1} X^j*rho(X) dX",
        },
        "twoMomentLargeCenter": {
            "timeHalfLengthT": q(t_half),
            "timeInterval": "[-1,1]",
            "coefficient": "K_c(s)=3/143+6*(c+s)/11",
            "generalThreshold": "C_*=2*T+mu4/(3*mu2)",
            "threshold": q(threshold),
            "conclusion": "if abs(c)>=27/13 and abs(s)<=1 then K_c has fixed sign and abs(K_c)>=3*mu2*abs(c)",
            "thresholdFloor": q(floor),
            "positiveThresholdMinimum": q(positive_edge),
            "negativeThresholdMaximum": q(negative_edge),
            "signs": {"c>=27/13": "positive", "c<=-27/13": "negative"},
        },
        "fixedGaugeInviscidCalibration": {
            "timeHalfLengthT": q(t_half),
            "optimizedVariable": "one time-independent initial phase gradient a for each fixed X",
            "minimizingPhaseGradient": "a=-sigma*T^2",
            "oddComponent": "3*sigma*s*(X^2+2*c)",
            "centeredEvenComponent": "sigma*(3*s^2-T^2)",
            "orthogonalOnSymmetricBlock": True,
            "meanSquareIdentity": "min_a (1/(2*T))*integral_{-T}^{T}|a+sigma*(3*s*(X^2+2*c)+3*s^2)|^2 ds=3*T^2*(X^2+2*c)^2+(4/5)*T^4",
            "unitBlockFloor": q(gauge_floor),
            "isViscousContraction": False,
        },
        "claimBoundary": {
            "exactRationalProbeCertified": True,
            "twoMomentLargeCenterAlgebraCertified": True,
            "fixedGaugeInviscidFloorCertified": True,
            "boundedChartFunctionalAnalysisMachineChecked": False,
            "wholeLineBlockContractionProved": False,
            "periodicTransferProved": False,
            "nonlinearNavierStokesClosureProved": False,
            "clayMillenniumProblemSolved": False,
        },
    }


def validate(value: dict) -> None:
    if value["moments"] != {
        "mu0": "1/1",
        "mu2": "1/11",
        "mu4": "3/143",
        "definition": "mu_j=integral_{-1}^{1} X^j*rho(X) dX",
    }:
        raise RuntimeError("independent probe moments failed")
    large = value["twoMomentLargeCenter"]
    if (
        large["threshold"] != "27/13"
        or large["thresholdFloor"] != "81/143"
        or large["positiveThresholdMinimum"] != "87/143"
        or large["negativeThresholdMaximum"] != "-81/143"
    ):
        raise RuntimeError("independent large-centre threshold failed")
    if value["fixedGaugeInviscidCalibration"]["unitBlockFloor"] != "4/5":
        raise RuntimeError("independent fixed-gauge floor failed")
    if value["claimBoundary"]["wholeLineBlockContractionProved"] is not False:
        raise RuntimeError("whole-line claim boundary drifted")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    value = compute()
    validate(value)
    if args.output:
        output = Path(args.output).resolve()
        expected = (ROOT / "independent.json").resolve()
        if output != expected:
            raise RuntimeError(f"independent output must be {expected}")
        output.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("R0.72U independent recomputation: passed and written")
        return
    print("R0.72U independent recomputation self-test: passed (no outputs written)")


if __name__ == "__main__":
    main()
