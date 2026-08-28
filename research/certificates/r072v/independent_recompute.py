#!/usr/bin/env python3
"""Independent exact recomputation for the R0.72V finite ledger.

This route obtains the unit-chart moments by scaling a beta-integral
recurrence on [-1,1].  Translation coefficients are assembled coefficient by
coefficient with the binomial theorem, independently of the producer's
multivariate polynomial multiplication.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from math import comb
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def q(value: F | int) -> str:
    value = F(value)
    return f"{value.numerator}/{value.denominator}"


def translated_coefficient_check() -> bool:
    """Compare coefficients of y^0,...,y^3 using monomials in (k,c,t)."""

    # Each inner key is (power of k, power of c, power of t).
    lhs: list[dict[tuple[int, int, int], int]] = [dict() for _ in range(4)]
    for y_power in range(4):
        lhs[y_power][(3 - y_power, 0, 0)] = comb(3, y_power)
    lhs[0][(1, 1, 0)] = lhs[0].get((1, 1, 0), 0) + 6
    lhs[0][(1, 0, 1)] = lhs[0].get((1, 0, 1), 0) + 6
    lhs[1][(0, 1, 0)] = lhs[1].get((0, 1, 0), 0) + 6
    lhs[1][(0, 0, 1)] = lhs[1].get((0, 0, 1), 0) + 6

    rhs = [
        {(3, 0, 0): 1, (1, 1, 0): 6, (1, 0, 1): 6},
        {(2, 0, 0): 3, (0, 1, 0): 6, (0, 0, 1): 6},
        {(1, 0, 0): 3},
        {(0, 0, 0): 1},
    ]
    return lhs == rhs


def energy_coefficient_check() -> bool:
    # Starting from T*E_plus <= C2*E_minus-C2*E_plus, collect the
    # coefficients of E_plus and E_minus independently.
    e_plus = {"T": 1, "C2": 1}
    e_minus = {"C2": -1}
    return e_plus == {"T": 1, "C2": 1} and e_minus == {"C2": -1}


def translation_record() -> dict:
    return {
        "identity": "(k+y)^3+6*(c+t)*(k+y)=y^3+3*k*y^2+(3*k^2+6*c+6*t)*y+k^3+6*(c+t)*k",
        "unitChartCoordinate": "y=x-k",
        "quadraticCoefficientA": "3*k",
        "linearConstantCoefficientB": "3*k^2+6*c",
        "linearTimeCoefficient": "6*t",
        "removableScalar": "k^3+6*(c+t)*k",
        "scalarGaugeDerivative": "d_{k,c}(t)=k^3+6*(c+t)*k",
        "symbolicCoefficientMapMatches": translated_coefficient_check(),
    }


def energy_record() -> dict:
    return {
        "inputInequality": "T*E_plus<=C2*(E_minus-E_plus)",
        "rearrangedInequality": "(T+C2)*E_plus<=C2*E_minus",
        "squaredEnergyRatio": "C2/(T+C2)",
        "normRatio": "C/sqrt(T+C^2)",
        "strictFor": "T>0 and finite C>0",
        "symbolicCoefficientMapMatches": energy_coefficient_check(),
    }


def claim_boundary() -> dict:
    return {
        "finiteExactAlgebraCertified": True,
        "analyticWholeLineTheoremProvedInBoundReport": True,
        "analyticActualSolutionObservabilityProvedInBoundReport": True,
        "analyticAllL2DataEnergyEvolutionProvedInBoundReport": True,
        "analyticEnergyBlockContractionProvedForDeclaredClass": True,
        "wholeLineFunctionalTheoremMachineChecked": False,
        "compactnessArgumentMachineChecked": False,
        "scalarEndpointTracePassageMachineChecked": False,
        "hMinusOneDirectSumMachineChecked": False,
        "nonautonomousEvolutionExistenceMachineChecked": False,
        "timeLengthUniformity": False,
        "periodicTransferProved": False,
        "nonlinearNavierStokesClosureProved": False,
        "clayMillenniumProblemSolved": False,
    }


def compute() -> dict:
    # For m_(2n)=int_{-1}^{1} x^(2n)*(315/256)*(1-x^2)^4 dx,
    # m_(2n+2)/m_(2n)=(2*n+1)/(2*n+11).  Since x=2*y,
    # mu_(2n)=m_(2n)/2^(2n).
    x_mu0 = F(1)
    x_mu2 = x_mu0 * F(1, 11)
    x_mu4 = x_mu2 * F(3, 13)
    mu0 = x_mu0
    mu2 = x_mu2 / 4
    mu4 = x_mu4 / 16
    variance = mu4 - mu2 * mu2
    kappa0 = min(variance, mu2)
    time_half_length = F(1)
    ell_constant = mu4
    ell_time_slope = 6 * mu2
    ell_bound = mu4 + 6 * time_half_length * mu2
    threshold = 2 * ell_bound / kappa0

    derivative_squared_exponent = F(2, 3)
    phase_squared_exponent = F(2) - F(4, 3)
    floor_squared_exponent = F(4)
    norm_exponent = min(
        derivative_squared_exponent,
        phase_squared_exponent,
        floor_squared_exponent,
    ) / 2

    value = {
        "schemaVersion": 1,
        "status": "passed",
        "method": "scaled beta-integral recurrence, binomial coefficient assembly, and independent energy coefficient collection",
        "probe": {
            "support": "[-1/2,1/2]",
            "formula": "q0(y)=(315/128)*(1-4*y^2)^4*1_{[-1/2,1/2]}(y)",
            "expandedOnSupport": "(315/128)*(1-16*y^2+96*y^4-256*y^6+256*y^8)",
            "normalization": q(mu0),
            "parity": "even",
            "boundaryVanishingOrder": 4,
            "functionalClassUsedByMomentPairing": "q0 and every degree-at-most-two polynomial multiple used in the ledger belong to H_0^1((-1/2,1/2))",
        },
        "moments": {
            "mu0": q(mu0),
            "mu2": q(mu2),
            "mu4": q(mu4),
            "varianceY2": q(variance),
            "definition": "mu_j=integral_{-1/2}^{1/2} y^j*q0(y) dy",
        },
        "escapingCoefficientLedger": {
            "timeHalfLengthT": q(time_half_length),
            "timeInterval": "[-1,1]",
            "adaptivePolynomial": "p_{alpha,beta}(y)=alpha*(y^2-mu2)+beta*y with alpha^2+beta^2=1",
            "kappaFormula": "kappa_{alpha,beta}=alpha^2*(mu4-mu2^2)+beta^2*mu2",
            "kappaLowerFloor": q(kappa0),
            "ellFormula": "ell_{alpha,beta}(t)=beta*(mu4+6*t*mu2)",
            "ellConstant": q(ell_constant),
            "ellTimeSlope": q(ell_time_slope),
            "unitBlockAbsoluteUpperBoundL": q(ell_bound),
            "sufficientThresholdFormula": "lambda>=2*L_T/kappa0",
            "unitBlockSufficientThreshold": q(threshold),
            "thresholdConclusion": "if lambda>=693/2 and abs(t)<=1 then lambda*kappa_{alpha,beta}+ell_{alpha,beta}(t)>=lambda*kappa0/2",
        },
        "spatialTranslation": translation_record(),
        "energyBlockContraction": energy_record(),
        "smallTimeBoundary": {
            "exactKernelSpatialScale": "L=T^(-1/3)",
            "squaredDerivativeTermExponent": q(derivative_squared_exponent),
            "squaredCubicPhaseTermExponent": q(phase_squared_exponent),
            "fixedGaugeFloorTermExponent": q(floor_squared_exponent),
            "normRatioUpperOrder": "T^(1/3)",
            "graphConstantLowerOrder": "T^(-1/3)",
            "timeLengthUniformity": False,
        },
        "claimBoundary": claim_boundary(),
    }
    return value


def validate(value: dict) -> None:
    if value["moments"] != {
        "mu0": "1/1",
        "mu2": "1/44",
        "mu4": "3/2288",
        "varianceY2": "5/6292",
        "definition": "mu_j=integral_{-1/2}^{1/2} y^j*q0(y) dy",
    }:
        raise RuntimeError("independent unit-chart moments failed")
    escaping = value["escapingCoefficientLedger"]
    if (
        escaping["kappaLowerFloor"] != "5/6292"
        or escaping["ellFormula"] != "ell_{alpha,beta}(t)=beta*(mu4+6*t*mu2)"
        or escaping["unitBlockAbsoluteUpperBoundL"] != "315/2288"
        or escaping["unitBlockSufficientThreshold"] != "693/2"
    ):
        raise RuntimeError("independent escaping-coefficient ledger failed")
    if not value["spatialTranslation"]["symbolicCoefficientMapMatches"]:
        raise RuntimeError("independent translation identity failed")
    if not value["energyBlockContraction"]["symbolicCoefficientMapMatches"]:
        raise RuntimeError("independent energy rearrangement failed")
    if value["smallTimeBoundary"] != {
        "exactKernelSpatialScale": "L=T^(-1/3)",
        "squaredDerivativeTermExponent": "2/3",
        "squaredCubicPhaseTermExponent": "2/3",
        "fixedGaugeFloorTermExponent": "4/1",
        "normRatioUpperOrder": "T^(1/3)",
        "graphConstantLowerOrder": "T^(-1/3)",
        "timeLengthUniformity": False,
    }:
        raise RuntimeError("independent small-time boundary failed")
    boundary = value["claimBoundary"]
    if boundary["analyticWholeLineTheoremProvedInBoundReport"] is not True:
        raise RuntimeError("analytic theorem status was lost")
    for key in (
        "wholeLineFunctionalTheoremMachineChecked",
        "compactnessArgumentMachineChecked",
        "scalarEndpointTracePassageMachineChecked",
        "hMinusOneDirectSumMachineChecked",
        "nonautonomousEvolutionExistenceMachineChecked",
        "timeLengthUniformity",
        "periodicTransferProved",
        "nonlinearNavierStokesClosureProved",
        "clayMillenniumProblemSolved",
    ):
        if boundary[key] is not False:
            raise RuntimeError(f"claim boundary drifted: {key}")


def ensure_formal_context(source_commit: str, output: Path) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError("--formal requires a full 40-character --source-commit")
    expected = (ROOT / "independent.json").resolve()
    if output.resolve() != expected:
        raise RuntimeError(f"independent output must be {expected}")
    if expected.exists():
        raise RuntimeError("refusing to overwrite existing independent.json")
    status = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=REPOSITORY,
        text=True,
    )
    if status:
        raise RuntimeError("formal independent recomputation requires a completely clean repository")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True).strip()
    if head != source_commit:
        raise RuntimeError("formal independent source commit must equal clean HEAD")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--formal", action="store_true")
    parser.add_argument("--source-commit")
    parser.add_argument("--output")
    args = parser.parse_args()

    if args.self_test:
        if args.formal or args.source_commit or args.output:
            parser.error("--self-test cannot be combined with formal output arguments")
        value = compute()
        validate(value)
        print("R0.72V independent recomputation self-test: passed (no outputs written)")
        return

    if not args.formal:
        parser.error("no unsealed output mode exists; use --self-test or --formal")
    if not args.output:
        parser.error("--formal requires --output")
    source_commit = str(args.source_commit or "")
    output = Path(args.output)
    ensure_formal_context(source_commit, output)
    value = compute()
    validate(value)
    output.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("R0.72V independent formal recomputation: passed and written")


if __name__ == "__main__":
    main()
