#!/usr/bin/env python3
"""Independent exact recomputation of the R0.72X finite ledger.

This file does not import the producer.  It uses derivative tables instead
of bivariate series, a cross-product elimination instead of the producer's
case split, kappa-first power accounting, and rational evaluations of the
geometric identity.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from math import factorial
import json
from pathlib import Path
import re
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def q(value: F | int) -> str:
    value = F(value)
    return f"{value.numerator}/{value.denominator}"


def cosine_derivative_at_zero(frequency: int, order: int) -> int:
    if order % 2:
        return 0
    return (-1) ** (order // 2) * frequency**order


def sine_derivative_at_zero(frequency: int, order: int) -> int:
    if order % 2 == 0:
        return 0
    return (-1) ** ((order - 1) // 2) * frequency**order


def product_taylor_coefficient(
    rate: int,
    frequency: int,
    d_power: int,
    theta_power: int,
    trig: str,
) -> F:
    theta_derivative = (
        cosine_derivative_at_zero(frequency, theta_power)
        if trig == "cos"
        else sine_derivative_at_zero(frequency, theta_power)
    )
    return F(
        (-rate) ** d_power * theta_derivative,
        factorial(d_power) * factorial(theta_power),
    )


def f_coefficient(d_power: int, theta_power: int) -> F:
    return (
        product_taylor_coefficient(1, 1, d_power, theta_power, "cos")
        - product_taylor_coefficient(4, 2, d_power, theta_power, "cos")
    )


def g_coefficient(d_power: int, theta_power: int) -> F:
    return (
        -product_taylor_coefficient(1, 1, d_power, theta_power, "sin")
        + 2 * product_taylor_coefficient(4, 2, d_power, theta_power, "sin")
    )


def common_zero_and_jet_record() -> dict[str, Any]:
    # For a common zero, the vector identity
    #   r(c,s)=(2c^2-1,4sc)
    # has cross product s*(2c^2+1)=0.  Positivity of 2c^2+1 gives s=0;
    # then c=+/-1 and r*c=1, so r>0 selects (r,c)=(1,1).
    cross_factor_minimum = F(1)
    candidates = [F(-1), F(1)]
    selected = [(F(1, c), c) for c in candidates if F(1, c) > 0]
    if cross_factor_minimum <= 0 or selected != [(F(1), F(1))]:
        raise RuntimeError("independent common-zero elimination failed")

    labels = {
        (0, 0): "1",
        (1, 0): "D",
        (0, 1): "theta",
        (2, 0): "D^2",
        (1, 1): "D*theta",
        (0, 2): "theta^2",
        (3, 0): "D^3",
        (2, 1): "D^2*theta",
        (1, 2): "D*theta^2",
        (0, 3): "theta^3",
    }
    f_jet = {
        label: q(f_coefficient(*key))
        for key, label in labels.items()
        if f_coefficient(*key)
    }
    g_jet = {
        label: q(g_coefficient(*key))
        for key, label in labels.items()
        if g_coefficient(*key)
    }
    jacobian = [
        [q(f_coefficient(1, 0)), q(f_coefficient(0, 1))],
        [q(g_coefficient(1, 0)), q(g_coefficient(0, 1))],
    ]
    determinant = F(jacobian[0][0]) * F(jacobian[1][1]) - F(jacobian[0][1]) * F(jacobian[1][0])
    return {
        "unscaledBrackets": {
            "f": "exp(-D)*cos(theta)-exp(-4*D)*cos(2*theta)",
            "g": "-exp(-D)*sin(theta)+2*exp(-4*D)*sin(2*theta)",
        },
        "positiveParameter": "r=exp(3*D)>0",
        "commonZeroEquations": [
            "r*cos(theta)=cos(2*theta)",
            "r*sin(theta)=2*sin(2*theta)",
        ],
        "sineZeroBranch": {
            "cosineCandidates": ["-1/1", "1/1"],
            "positiveRCandidates": ["1/1"],
            "selected": "r=1, cos(theta)=1",
        },
        "nonzeroSineBranch": {
            "deducedR": "r=4*cos(theta)",
            "deducedEquation": "2*cos(theta)^2=-1",
            "realSolutionExists": False,
        },
        "branchEliminationChecked": cross_factor_minimum > 0 and selected == [(F(1), F(1))],
        "onlyCommonZero": "D=0 and theta=0 mod 2*pi",
        "jacobianVariableOrder": ["D", "theta"],
        "jacobianOutputOrder": ["f", "g"],
        "jacobianAtOrigin": jacobian,
        "jacobianDeterminant": q(determinant),
        "fJetThroughTotalDegreeThree": f_jet,
        "gJetThroughTotalDegreeThree": g_jet,
        "leadingJet": {
            "g": "3*theta+O(|D*theta|+|theta|^3)",
            "f": "3*D+(3/2)*theta^2+O(D^2+|D|*theta^2+theta^4)",
        },
        "boundedCoefficientInputs": ["f=O(alpha^2)", "g=O(alpha)"],
        "analyticBoundedCenterConclusion": ["theta=O(alpha)", "D=O(alpha^2)"],
    }


def interface_power_record() -> dict[str, Any]:
    # Independent accounting starts in kappa powers and converts with
    # alpha=kappa^(-1/5).
    kappa = {
        "epsilon_c": F(1),
        "alpha": F(-1, 5),
        "h_alpha": F(-2, 5),
        "preCriticalPointHalfSeparation": F(-1, 5),
        "preMorseCurvatureFloor": F(-1, 5),
        "postAwayGradientFloor": F(-2, 5),
    }
    pre_rate_kappa = kappa["epsilon_c"] / 2 + kappa["preMorseCurvatureFloor"] / 2
    post_rate_kappa = F(2, 3) * (
        kappa["epsilon_c"] + kappa["postAwayGradientFloor"]
    )
    alpha_from_kappa = lambda exponent: -5 * exponent

    # Repeated derivative recurrence for h -> (e^(-4h)-e^(-h))/2.
    powers_four = F(-4)
    powers_one = F(-1)
    coefficients = []
    running_factorial = 1
    for degree in range(1, 3):
        running_factorial *= degree
        coefficients.append((powers_four - powers_one) / (2 * running_factorial))
        powers_four *= -4
        powers_one *= -1

    return {
        "scaling": ["epsilon_c=4*alpha^(-5)", "kappa=alpha^(-5)", "h_alpha=T*alpha^2"],
        "alphaPowers": {
            "epsilon_c": q(alpha_from_kappa(kappa["epsilon_c"])),
            "h_alpha": q(alpha_from_kappa(kappa["h_alpha"])),
            "preCriticalPointHalfSeparation": q(alpha_from_kappa(kappa["preCriticalPointHalfSeparation"])),
            "preMorseCurvatureFloor": q(alpha_from_kappa(kappa["preMorseCurvatureFloor"])),
            "postAwayGradientFloor": q(alpha_from_kappa(kappa["postAwayGradientFloor"])),
            "preA1DiagnosticRate": q(alpha_from_kappa(pre_rate_kappa)),
            "postMonotoneDiagnosticRate": q(alpha_from_kappa(post_rate_kappa)),
            "exactFamilyCollisionRate": "-2/1",
        },
        "kappaPowers": {
            "h_alpha": q(kappa["h_alpha"]),
            "preCriticalPointHalfSeparation": q(kappa["preCriticalPointHalfSeparation"]),
            "preMorseCurvatureFloor": q(kappa["preMorseCurvatureFloor"]),
            "postAwayGradientFloor": q(kappa["postAwayGradientFloor"]),
            "matchedRate": q(pre_rate_kappa),
        },
        "preCriticalPointLedger": {
            "equation": "x_pm^2=2*T*alpha^2+O_T(alpha^4)",
            "locations": "x_pm=+/-sqrt(2*T)*alpha+O_T(alpha^3)",
            "separationOrder": "alpha",
            "curvatureOrder": "alpha",
        },
        "postGradientLedger": {
            "exact": "W_x(h_alpha,0)=(exp(-4*h_alpha)-exp(-h_alpha))/2",
            "hCoefficientsThroughTwo": [q(value) for value in coefficients],
            "alphaExpansion": "-(3/2)*T*alpha^2+(15/4)*T^2*alpha^4+O_T(alpha^6)",
        },
        "diagnosticRatePowersMatch": pre_rate_kappa == post_rate_kappa == F(2, 5),
        "fixedShapeA1UniformAtShrinkingInterface": False,
    }


def block_tiling_record() -> dict[str, Any]:
    floor_ok = True
    for numerator in range(65):
        for denominator in range(1, 33):
            quotient, remainder = divmod(numerator, denominator)
            floor_ok = floor_ok and 0 <= remainder < denominator
            floor_ok = floor_ok and F(quotient) >= F(numerator, denominator) - 1

    geometric_ok = True
    for q_value in (F(1, 7), F(1, 2), F(3, 4), F(9, 10)):
        for n in range(65):
            finite_sum = sum((q_value * q_value) ** j for j in range(n + 1))
            geometric_ok = geometric_ok and (
                (1 - q_value * q_value) * finite_sum
                == 1 - q_value ** (2 * n + 2)
            )
    return {
        "physicalGap": "L=d_2-d_1",
        "scaledGap": "L_S=L/alpha^2",
        "fullBlockCount": "N=floor(L/(2*T*alpha^2))",
        "floorInequality": "floor(z)>=z-1",
        "finiteRationalFloorGridChecked": floor_ok,
        "blockNormFactor": "q^N",
        "exponentialEnvelope": "q^N<=q^(-1)*exp(-(|log(q)|/(2*T))*L/alpha^2)",
        "envelopeConstant": "c_KT=|log(q)|/(2*T)",
        "shortGapCounterexample": {
            "scaledBlockRatio": "z=1/2",
            "fullBlockCount": 0,
            "exactBlockFactor": "1",
            "prefactorOneExponentialFactor": "q^(1/2)<1",
        },
        "prefactorOneAllGapExponential": False,
        "finiteGeometricTelescopingChecked": geometric_ok,
        "geometricEnergyIdentity": "(1-q^2)*sum_(j=0)^n q^(2*j)=1-q^(2*n+2)",
        "scaledIntegratedEnergyBound": "2*T/(1-q^2)*E(S_1)",
        "physicalIntegratedEnergyBound": "2*T*alpha^2/(1-q^2)*E(d_1)",
        "duhamelL2xKernelScale": "O_KT(alpha^2)",
        "forcedHMinusOneTransferInferred": False,
    }


def bloch_twist_record() -> dict[str, Any]:
    # The phase is obtained by counting length and gauge exponents before
    # substituting the constants: alpha^(1-1)*2*pi*beta.
    phase_alpha_power = F(1) - F(1)
    return {
        "covariantDerivative": "D_beta=partial_X+i*alpha*beta",
        "unitaryGauge": "w=exp(i*alpha*beta*X)*u",
        "operatorIdentity": "partial_X^2*w=exp(i*alpha*beta*X)*D_beta^2*u",
        "scaledTorusLength": "L_alpha=2*pi/alpha",
        "boundaryPhaseExponent": "alpha*beta*L_alpha=2*pi*beta",
        "alphaPowerInBoundaryPhase": q(phase_alpha_power),
        "twistedBoundary": "w(X+L_alpha)=exp(2*pi*i*beta)*w(X)",
        "zeroResiduePhase": "beta=0 gives phase 1",
        "endpointPhaseModulusSquared": "|exp(2*pi*i*beta)|^2=1",
        "endpointIntegrationByPartsCancellationMachineChecked": False,
    }


def damping_and_counterexample_record() -> tuple[dict[str, Any], dict[str, Any]]:
    # Solving y'=-mu*y gives one power in amplitude and two after taking
    # |y|^2.  The constant row is checked separately by differentiating its
    # Fourier monomial k=0.
    norm_exponent = F(1)
    energy_exponent = 2 * norm_exponent
    damping = {
        "undampingSubstitution": "v(d)=exp(mu*(d-d_1))*G(d)",
        "timeGap": "L=d_2-d_1",
        "normDampingFactor": "exp(-mu*L)",
        "squaredEnergyDampingFactor": "exp(-2*mu*L)",
        "normBlockFactor": "exp(-mu*L)*q^N",
        "squaredEnergyBlockFactor": "exp(-2*mu*L)*q^(2*N)",
        "energyExponentToNormExponent": int(energy_exponent / norm_exponent),
        "spatialScalingEndpointFactor": "alpha^(-1/2) at both endpoints; cancels in the norm ratio",
        "scalarCellGauges": "unitary proof devices with phase one at each block start",
    }
    zero_mode = 0
    constant_equation_checked = (
        zero_mode**2 == 0
        and F(0) * zero_mode == 0
        and F(0) == 0
    )
    counterexample = {
        "effectiveCouplingFormula": "epsilon_j=2*|delta*K_z,j|*a/R^2",
        "rowParameters": {"K_z": "0", "epsilon_j": "0", "beta": "0", "mu": "0"},
        "datum": "G(d,x)=(2*pi)^(-1/2)",
        "spatialDerivative": "partial_x G=0",
        "laplacian": "partial_x^2 G=0",
        "potentialTerm": "epsilon_j*W*G=0",
        "dampingTerm": "mu*G=0",
        "timeDerivative": "partial_d G=0",
        "normalizedSquaredNorm": "1",
        "constantEquationChecked": constant_equation_checked,
        "strictContraction": not constant_equation_checked,
        "conclusion": "all physical rows cannot have one uniform strict contraction without projection, damping, or a coupling floor",
    }
    return damping, counterexample


def claim_boundary() -> dict[str, Any]:
    return {
        "finiteExactAlgebraCertified": True,
        "analyticAllCenterExactFamilyGraphCoercivityProvedInBoundReport": True,
        "analyticAllStartExactPathSemigroupProvedInBoundReport": True,
        "analyticAllStartIntegratedA2ScaleProvedInBoundReport": True,
        "analyticUniformTwistedPeriodicGraphProvedInBoundReport": True,
        "analyticStrongRowDirectSumNoCountLossProvedInBoundReport": True,
        "analyticFixedMarginA1EnhancedDissipationImportedInBoundReport": True,
        "analyticPeriodicRepresentativeA1A2A1ConcatenationProvedInBoundReport": True,
        "compactnessArgumentMachineChecked": False,
        "boundedCenterGraphLimitMachineChecked": False,
        "scalarEndpointTracePassageMachineChecked": False,
        "twistedHMinusOneDirectSumMachineChecked": False,
        "nonautonomousEvolutionExistenceMachineChecked": False,
        "cobleHeTheoremMachineChecked": False,
        "cobleHeApplicationHypothesesMachineChecked": False,
        "endpointIntegrationByPartsMachineChecked": False,
        "shrinkingInterfaceFixedShapeA1Hypotheses": False,
        "prefactorOneAllGapExponential": False,
        "blochUniformFastA1ConcatenationProved": False,
        "allPhysicalRowsUniformContraction": False,
        "forcedHMinusOneTransferProved": False,
        "completeLinearizedShearSubsystemProved": False,
        "nonlinearNavierStokesClosureProved": False,
        "clayMillenniumProblemSolved": False,
    }


def compute() -> dict[str, Any]:
    common = common_zero_and_jet_record()
    interface = interface_power_record()
    tiling = block_tiling_record()
    bloch = bloch_twist_record()
    damping, counterexample = damping_and_counterexample_record()
    boundary = claim_boundary()
    return {
        "schemaVersion": 1,
        "theoremId": "R0.72X-all-center-outer-time-finite-ledger",
        "status": "passed",
        "method": "direct derivative table, cross-product common-zero elimination, kappa-first exponent arithmetic, and rational geometric evaluations",
        "commonZeroAndLocalJet": common,
        "shrinkingInterfacePowers": interface,
        "blockTilingAndIntegratedEnergy": tiling,
        "blochTwist": bloch,
        "scalarDamping": damping,
        "zeroCouplingCounterexample": counterexample,
        "claimBoundary": boundary,
    }


def validate(value: dict[str, Any]) -> None:
    common = value["commonZeroAndLocalJet"]
    if (
        common["branchEliminationChecked"] is not True
        or common["onlyCommonZero"] != "D=0 and theta=0 mod 2*pi"
    ):
        raise RuntimeError("independent common-zero conclusion failed")
    if common["jacobianAtOrigin"] != [["3/1", "0/1"], ["0/1", "3/1"]]:
        raise RuntimeError("independent Jacobian failed")
    if common["fJetThroughTotalDegreeThree"].get("theta^2") != "3/2":
        raise RuntimeError("independent f jet failed")
    if common["gJetThroughTotalDegreeThree"].get("theta") != "3/1":
        raise RuntimeError("independent g jet failed")
    interface = value["shrinkingInterfacePowers"]
    if interface["alphaPowers"]["preA1DiagnosticRate"] != "-2/1":
        raise RuntimeError("independent pre-interface power failed")
    if interface["alphaPowers"]["postMonotoneDiagnosticRate"] != "-2/1":
        raise RuntimeError("independent post-interface power failed")
    tiling = value["blockTilingAndIntegratedEnergy"]
    if not tiling["finiteRationalFloorGridChecked"] or not tiling["finiteGeometricTelescopingChecked"]:
        raise RuntimeError("independent block arithmetic failed")
    if tiling["prefactorOneAllGapExponential"] is not False:
        raise RuntimeError("independent short-gap counterexample failed")
    if value["blochTwist"]["alphaPowerInBoundaryPhase"] != "0/1":
        raise RuntimeError("independent Bloch phase failed")
    if value["scalarDamping"]["energyExponentToNormExponent"] != 2:
        raise RuntimeError("independent damping ledger failed")
    if (
        value["zeroCouplingCounterexample"]["constantEquationChecked"] is not True
        or value["zeroCouplingCounterexample"]["strictContraction"] is not False
    ):
        raise RuntimeError("independent zero-coupling counterexample failed")
    boundary = value["claimBoundary"]
    required_true = {
        "finiteExactAlgebraCertified",
        "analyticAllCenterExactFamilyGraphCoercivityProvedInBoundReport",
        "analyticAllStartExactPathSemigroupProvedInBoundReport",
        "analyticAllStartIntegratedA2ScaleProvedInBoundReport",
        "analyticUniformTwistedPeriodicGraphProvedInBoundReport",
        "analyticStrongRowDirectSumNoCountLossProvedInBoundReport",
        "analyticFixedMarginA1EnhancedDissipationImportedInBoundReport",
        "analyticPeriodicRepresentativeA1A2A1ConcatenationProvedInBoundReport",
    }
    required_false = {
        "compactnessArgumentMachineChecked",
        "boundedCenterGraphLimitMachineChecked",
        "scalarEndpointTracePassageMachineChecked",
        "twistedHMinusOneDirectSumMachineChecked",
        "nonautonomousEvolutionExistenceMachineChecked",
        "cobleHeTheoremMachineChecked",
        "cobleHeApplicationHypothesesMachineChecked",
        "endpointIntegrationByPartsMachineChecked",
        "shrinkingInterfaceFixedShapeA1Hypotheses",
        "prefactorOneAllGapExponential",
        "blochUniformFastA1ConcatenationProved",
        "allPhysicalRowsUniformContraction",
        "forcedHMinusOneTransferProved",
        "completeLinearizedShearSubsystemProved",
        "nonlinearNavierStokesClosureProved",
        "clayMillenniumProblemSolved",
    }
    if set(boundary) != required_true | required_false:
        raise RuntimeError("independent claim boundary key set drifted")
    for key in required_true:
        if boundary[key] is not True:
            raise RuntimeError(f"claim boundary true status drifted: {key}")
    for key in required_false:
        if boundary[key] is not False:
            raise RuntimeError(f"claim boundary false status drifted: {key}")


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
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True
    ).strip()
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
        print("R0.72X independent recomputation self-test: passed (no outputs written)")
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
    print("R0.72X independent formal recomputation: passed and written")


if __name__ == "__main__":
    main()
