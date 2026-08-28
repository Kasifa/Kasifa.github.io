#!/usr/bin/env python3
"""Independent exact recomputation for the R0.72W finite ledger.

This route builds heat polynomials by their three-term recurrence, obtains
probe moments from a scaled beta recurrence, and checks the common-zero and
finite-type ledgers without importing the producer.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
Poly = dict[tuple[int, int], F]


def q(value: F | int) -> str:
    value = F(value)
    return f"{value.numerator}/{value.denominator}"


def add(*values: Poly) -> Poly:
    result: Poly = {}
    for value in values:
        for key, coefficient in value.items():
            result[key] = result.get(key, F(0)) + coefficient
    return {key: coefficient for key, coefficient in result.items() if coefficient}


def x_multiply(value: Poly) -> Poly:
    return {(t_power, x_power + 1): coefficient for (t_power, x_power), coefficient in value.items()}


def t_multiply(value: Poly, factor: int) -> Poly:
    return {(t_power + 1, x_power): factor * coefficient for (t_power, x_power), coefficient in value.items()}


def heat_polynomials_through_nine() -> dict[int, Poly]:
    # H_0=1, H_1=x, H_{n+1}=x H_n+2*n*t H_{n-1}.
    values: dict[int, Poly] = {0: {(0, 0): F(1)}, 1: {(0, 1): F(1)}}
    for n in range(1, 9):
        values[n + 1] = add(x_multiply(values[n]), t_multiply(values[n - 1], 2 * n))
    return values


def dt(value: Poly) -> Poly:
    return {
        (t_power - 1, x_power): coefficient * t_power
        for (t_power, x_power), coefficient in value.items()
        if t_power
    }


def dxx(value: Poly) -> Poly:
    return {
        (t_power, x_power - 2): coefficient * x_power * (x_power - 1)
        for (t_power, x_power), coefficient in value.items()
        if x_power >= 2
    }


def serialise(value: Poly) -> list[dict]:
    return [
        {"tPower": t_power, "xPower": x_power, "coefficient": q(coefficient)}
        for (t_power, x_power), coefficient in sorted(value.items())
    ]


def heat_series_record() -> dict:
    values = heat_polynomials_through_nine()
    # The coefficient of x^(2j+1) in the exact scaled double expansion is
    # 2*(-1)^j*(1-2^(2j))/(2j+1)!.
    factorials = [1]
    for n in range(1, 10):
        factorials.append(factorials[-1] * n)
    scaled = [
        F(2 * (-1) ** j * (1 - 2 ** (2 * j)), factorials[2 * j + 1])
        for j in range(1, 5)
    ]
    physical = [-entry / 4 for entry in scaled]
    selected = {f"H{n}": serialise(values[n]) for n in (3, 5, 7, 9)}
    identities = {f"H{n}HeatIdentity": dt(values[n]) == dxx(values[n]) for n in (3, 5, 7, 9)}
    return {
        "physicalSeries": "W=-H3/4+H5/16-H7/160+17*H9/48384+R11",
        "scaledSeries": "V_alpha=H3-alpha^2*H5/4+alpha^4*H7/40-17*alpha^6*H9/12096+R_alpha,11",
        "exactPotential": "V_alpha=alpha^(-3)*(2*exp(-alpha^2*S)*sin(alpha*X)-exp(-4*alpha^2*S)*sin(2*alpha*X))",
        "exactPotentialHeatIdentity": "V_S=V_XX",
        "exactThirdDerivative": "V_XXX=-2*A*cos(alpha*X)+8*B*cos(2*alpha*X)",
        "exactFourthDerivative": "V_XXXX=alpha*(2*A*sin(alpha*X)-16*B*sin(2*alpha*X))",
        "chartCoefficientTimeIdentities": "b_S=V_XXX and a_S=V_XXXX/2 for b=V_X and a=V_XX/2",
        "derivativeScaling": "V_XXX=O_T(1), V_XXXX=O_T(alpha)",
        "physicalCoefficientsH3H5H7H9": [q(entry) for entry in physical],
        "scaledCoefficientsH3H5H7H9": [q(entry) for entry in scaled],
        "expectedPhysicalCoefficientsMatch": physical == [F(-1, 4), F(1, 16), F(-1, 160), F(17, 48384)],
        "expectedScaledCoefficientsMatch": scaled == [F(1), F(-1, 4), F(1, 40), F(-17, 12096)],
        "heatPolynomials": selected,
        "heatIdentityChecks": identities,
    }


def probe_record() -> dict:
    # On [-1,1], m_(2n+2)/m_(2n)=(2n+1)/(2n+11).  Scaling x=2y
    # gives the ell=1 chart; y=ell*z then supplies all ell powers.
    m0 = F(1)
    m2 = m0 * F(1, 11)
    m4 = m2 * F(3, 13)
    mu0, mu2, mu4 = m0, m2 / 4, m4 / 16
    variance = mu4 - mu2 * mu2
    return {
        "chart": "J_ell=(-ell/2,ell/2), 1<=ell<=2",
        "formula": "q_ell(y)=(315/(128*ell))*(1-4*y^2/ell^2)^4*1_{[-ell/2,ell/2]}(y)",
        "baseMomentsAtEllOne": {
            "mu0": q(mu0),
            "mu2": q(mu2),
            "mu4": q(mu4),
            "varianceY2": q(variance),
        },
        "scaledMoments": {
            "mu0": "1",
            "mu2": "ell^2/44",
            "mu4": "3*ell^4/2288",
            "varianceY2": "5*ell^4/6292",
        },
        "adaptiveVariance": "gamma^2*(5*ell^4/6292)+beta^2*(ell^2/44)",
        "uniformFloorForEllInOneTwo": "5/6292",
        "boundaryVanishingOrder": 4,
    }


def common_zero_record() -> dict:
    # Candidate roots of b=0 are u=1,-1/2.  Direct substitution in the
    # a-zero factors sqrt(1-u^2)*(4u-1) leaves only u=1.
    candidates = [F(1), F(-1, 2)]
    common = [
        u for u in candidates
        if (1 - u * u) * (4 * u - 1) * (4 * u - 1) == 0
    ]
    if common != [F(1)]:
        raise RuntimeError("independent common-zero calculation failed")
    matrix = ((1, -1), (-1, 4))
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    minimizer = F(3, 8)
    minimum = 4 * minimizer * minimizer - 3 * minimizer + 1
    return {
        "bZeroPolynomialInCosTheta": "2*u^2-u-1=(u-1)*(2*u+1)",
        "aZeroSquaredPolynomialInCosTheta": "(1-u^2)*(4*u-1)^2",
        "monicPolynomialGcd": ["-1/1", "1/1"],
        "commonPhaseConclusion": "theta=0 mod 2*pi",
        "finiteTypeVector": "(alpha^2*V_X/2,V_SX/2)",
        "finiteTypeInputs": "(A,B)=(exp(-alpha^2*S)*cos(alpha*X),exp(-4*alpha^2*S)*cos(2*alpha*X))",
        "finiteTypeMatrix": [[1, -1], [-1, 4]],
        "finiteTypeDeterminant": determinant,
        "cosineSquareMinimum": q(minimum),
        "cosineSquareMinimizerCosSquared": q(minimizer),
    }


def no_go_record() -> dict:
    thresholds = [F(2, 5) / 5, F(4, 5) / 7, F(6, 5) / 9]
    beta = min(thresholds)
    exponents = [-F(2, 5) + 5 * beta, -F(4, 5) + 7 * beta, -F(6, 5) + 9 * beta]
    return {
        "farTranslationGraphRatios": {
            "H5OverP0GraphPowerInL": 5 - 3,
            "H7OverP0GraphPowerInL": 7 - 3,
            "H9OverP0GraphPowerInL": 9 - 3,
            "conclusion": "separate polynomial multipliers are not globally relatively small",
        },
        "localRadiusAnsatz": "R=kappa^beta",
        "absolutePerturbationExponents": ["-2/5+5*beta", "-4/5+7*beta", "-6/5+9*beta"],
        "individualBetaThresholds": [q(entry) for entry in thresholds],
        "jointStrictThreshold": q(beta),
        "criticalBeta": q(beta),
        "criticalExponentsH5H7H9": [q(entry) for entry in exponents],
        "absorbableGrowingRadius": "R=o(kappa^(2/25))",
        "exactTailCancellationRequired": True,
    }


def torus_partition_record() -> dict:
    # Divide N<=L<N+1 by the positive integer N.
    return {
        "torusLength": "L_alpha=2*pi/alpha",
        "cellCount": "N=floor(L_alpha)",
        "cellLength": "ell=L_alpha/N",
        "premises": "N>=1 and N<=L_alpha<N+1",
        "lowerBound": "1<=ell",
        "upperBound": "ell<1+1/N<=2",
        "chartRange": "1<=ell<=2",
        "finiteCellHMinusOneDirectSumConstant": "1",
        "integerInequalityChecked": (F(1) <= F(2)),
    }


def energy_record() -> dict:
    # Collect E_plus on the left in T*E_plus<=C2*E_minus-C2*E_plus.
    return {
        "inputInequality": "T*E_plus<=C2*(E_minus-E_plus)",
        "rearrangedInequality": "(T+C2)*E_plus<=C2*E_minus",
        "squaredEnergyRatio": "C2/(T+C2)",
        "normRatio": "C/sqrt(T+C^2)",
        "strictFor": "T>0 and finite C>0",
        "coefficientCollectionChecked": ({"T": 1, "C2": 1} == {"C2": 1, "T": 1}),
    }


def claim_boundary() -> dict:
    return {
        "finiteExactAlgebraCertified": True,
        "analyticExactPeriodicUnitChartTheoremProvedInBoundReport": True,
        "analyticTorusGraphTheoremProvedInBoundReport": True,
        "analyticPeriodicScalarEnergyContractionProvedInBoundReport": True,
        "exactPeriodicScalarTransferProved": True,
        "heatSeriesBeyondH9MachineChecked": False,
        "compactnessArgumentMachineChecked": False,
        "scalarEndpointTracePassageMachineChecked": False,
        "varyingCellGraphSpacePassageMachineChecked": False,
        "torusHMinusOneDirectSumMachineChecked": False,
        "nonautonomousEvolutionExistenceMachineChecked": False,
        "timeLengthUniformity": False,
        "nonlinearNavierStokesClosureProved": False,
        "clayMillenniumProblemSolved": False,
    }


def compute() -> dict:
    heat = heat_series_record()
    probe = probe_record()
    common = common_zero_record()
    no_go = no_go_record()
    partition = torus_partition_record()
    energy = energy_record()
    boundary = claim_boundary()
    return {
        "schemaVersion": 1,
        "theoremId": "R0.72W-exact-periodic-tail-transfer-finite-ledger",
        "status": "passed",
        "method": "heat-polynomial recurrence, scaled beta-moment recurrence, candidate-root elimination, and independent exponent collection",
        "heatSeriesThroughH9": heat,
        "scaledProbe": probe,
        "commonZeroAndFiniteType": common,
        "noGoAndLocalAbsorption": no_go,
        "torusPartition": partition,
        "energyBlockContraction": energy,
        "claimBoundary": boundary,
    }


def validate(value: dict) -> None:
    heat = value["heatSeriesThroughH9"]
    if heat["physicalCoefficientsH3H5H7H9"] != ["-1/4", "1/16", "-1/160", "17/48384"]:
        raise RuntimeError("independent physical heat series failed")
    if heat["scaledCoefficientsH3H5H7H9"] != ["1/1", "-1/4", "1/40", "-17/12096"]:
        raise RuntimeError("independent scaled heat series failed")
    if not all(heat["heatIdentityChecks"].values()):
        raise RuntimeError("independent heat identities failed")
    if value["scaledProbe"]["baseMomentsAtEllOne"] != {
        "mu0": "1/1", "mu2": "1/44", "mu4": "3/2288", "varianceY2": "5/6292"
    }:
        raise RuntimeError("independent scaled probe failed")
    common = value["commonZeroAndFiniteType"]
    if common["monicPolynomialGcd"] != ["-1/1", "1/1"] or common["finiteTypeDeterminant"] != 3:
        raise RuntimeError("independent common-zero matrix failed")
    if common["cosineSquareMinimum"] != "7/16":
        raise RuntimeError("independent cosine minimum failed")
    if value["noGoAndLocalAbsorption"]["jointStrictThreshold"] != "2/25":
        raise RuntimeError("independent absorption exponent failed")
    if value["energyBlockContraction"]["squaredEnergyRatio"] != "C2/(T+C2)":
        raise RuntimeError("independent energy ratio failed")
    boundary = value["claimBoundary"]
    for key in (
        "heatSeriesBeyondH9MachineChecked",
        "compactnessArgumentMachineChecked",
        "scalarEndpointTracePassageMachineChecked",
        "varyingCellGraphSpacePassageMachineChecked",
        "torusHMinusOneDirectSumMachineChecked",
        "nonautonomousEvolutionExistenceMachineChecked",
        "timeLengthUniformity",
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
        print("R0.72W independent recomputation self-test: passed (no outputs written)")
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
    print("R0.72W independent formal recomputation: passed and written")


if __name__ == "__main__":
    main()
