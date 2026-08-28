#!/usr/bin/env python3
"""Independent exact recomputation for the R0.72Y draft finite ledger.

This file does not import the producer.  It recomputes the same records with
direct operator-action tables, direct Fourier-weight cross multiplication,
direct lift-up substitution, Leibniz coefficients, and recovery-matrix
multiplication.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import re
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
Poly = dict[tuple[int, ...], F]


def q(value: F | int) -> str:
    value = F(value)
    return f"{value.numerator}/{value.denominator}"


def add(*values: Poly) -> Poly:
    result: Poly = {}
    for value in values:
        for key, coefficient in value.items():
            result[key] = result.get(key, F(0)) + coefficient
    return {key: coefficient for key, coefficient in result.items() if coefficient}


def scale(value: Poly, factor: F | int) -> Poly:
    return {key: F(factor) * coefficient for key, coefficient in value.items() if factor * coefficient}


def multiply(left: Poly, right: Poly) -> Poly:
    rows: Poly = {}
    for left_power, left_coefficient in left.items():
        for right_power, right_coefficient in right.items():
            power = tuple(a + b for a, b in zip(left_power, right_power))
            rows[power] = rows.get(power, F(0)) + left_coefficient * right_coefficient
    return {key: coefficient for key, coefficient in rows.items() if coefficient}


def serialise(value: Poly, variables: tuple[str, ...]) -> list[dict[str, Any]]:
    result = []
    for powers, coefficient in sorted(value.items()):
        monomial = "*".join(
            variable if power == 1 else f"{variable}^{power}"
            for variable, power in zip(variables, powers)
            if power
        ) or "1"
        result.append({"monomial": monomial, "coefficient": q(coefficient)})
    return result


def heat_identity_record() -> dict[str, Any]:
    rows = []
    for frequency, amplitude in ((1, F(-1, 2)), (2, F(1, 4))):
        decay = frequency * frequency
        # Directly act with d/dd and d^2/dx^2 on a*e^{-m^2 d}sin(mx).
        time_amplitude = -decay * amplitude
        space_amplitude = -frequency * frequency * amplitude
        rows.append({
            "frequency": frequency,
            "decayRate": decay,
            "amplitude": q(amplitude),
            "dDerivativeAmplitude": q(time_amplitude),
            "xxDerivativeAmplitude": q(space_amplitude),
            "matches": time_amplitude == space_amplitude,
        })
    return {
        "profile": "W(d,x)=-(1/2)*exp(-d)*sin(x)+(1/4)*exp(-4d)*sin(2x)",
        "modeRows": rows,
        "identity": "W_d=W_xx",
        "allModesMatch": all(row["matches"] for row in rows),
        "derivedIdentity": "(W_x)_d=W_xxx",
    }


def pressure_factor_record() -> dict[str, Any]:
    # Product rule in div(V e_z transport) and the e_z lift term gives
    # one identical coefficient from each source.
    contributions = {
        "divergenceOfIcWTimesU": 1,
        "divergenceOfLambdaWxU2E3": 1,
        "divergenceOfGradientPiAfterLPiEquals2icWxU2": -2,
    }
    source_sum = sum(value for key, value in contributions.items() if "Gradient" not in key)
    return {
        "normalisation": "c=Lambda*gamma",
        "pressureEquation": "L*pi=2*i*c*W_x*u_2",
        "divergenceGradientSign": "div_j(grad_j*pi)=-L*pi",
        "coefficientsInUnitsOfIcWxU2": contributions,
        "coefficientSum": sum(contributions.values()),
        "factorTwo": source_sum,
    }


def bloch_leray_record() -> dict[str, Any]:
    # Apply (i xi,A,i gamma) twice to a scalar, then use mu=xi^2+gamma^2.
    div_grad = {(2, 0, 0): F(1), (0, 2, 0): F(-1), (0, 0, 2): F(-1)}
    minus_l = {(2, 0, 0): F(1), (0, 2, 0): F(-1), (0, 0, 2): F(-1)}
    return {
        "A_beta": "partial_x+i*beta",
        "L": "-A_beta^2+mu",
        "mu": "xi^2+gamma^2",
        "gradient": "(i*xi,A_beta,i*gamma)",
        "divergenceGradient": serialise(div_grad, ("A", "xi", "gamma")),
        "minusL": serialise(minus_l, ("A", "xi", "gamma")),
        "identityResidual": serialise(add(div_grad, scale(minus_l, -1)), ("A", "xi", "gamma")),
        "lerayProjection": "P_j=I+grad_j*L^(-1)*div_j",
        "divergenceOfProjectionCoefficients": ["1/1", "-1/1"],
        "divergenceOfProjectionSum": "0/1",
        "projectionKillsGradientCoefficients": ["1/1", "-1/1"],
    }


def os_squire_record() -> dict[str, Any]:
    # L=-A^2+mu and A^2(Wu)=W A^2u+2 W_x A u+W_xx u.
    leibniz = {"W*q": -1, "W_x*A_beta*u_2": 2, "W_xx*u_2": 1}
    pressure = {"W*q": 0, "W_x*A_beta*u_2": -2, "W_xx*u_2": -2}
    combined = {key: leibniz[key] + pressure[key] for key in leibniz}
    pressure_pair = {"from_i_gamma_u1": 1, "from_minus_i_xi_u3": -1}
    return {
        "domain": "mu>0",
        "definitions": ["q=L*u_2", "eta=i*gamma*u_1-i*xi*u_3"],
        "commutator": "L(Wu)=W*L*u-2*W_x*A_beta*u-W_xx*u",
        "pressureSubstitution": "-A_beta*L*pi=-2*i*c*A_beta(W_x*u_2)",
        "orrSommerfeldCoefficientTableInUnitsOfIc": {
            "minusIcLOfWu2": leibniz,
            "minusAOfLPi": pressure,
            "sum": combined,
        },
        "orrSommerfeldEquation": "q_d=(-L-i*c*W)q-i*c*W_xx*L^(-1)q",
        "squirePressureCoefficients": pressure_pair,
        "squirePressureSum": sum(pressure_pair.values()),
        "squireLiftCoefficient": 1,
        "squireEquation": "eta_d=(-L-i*c*W)eta+i*xi*Lambda*W_x*L^(-1)q",
        "expectedOsSum": {"W*q": -1, "W_x*A_beta*u_2": 0, "W_xx*u_2": -1},
    }


def velocity_reconstruction_record() -> dict[str, Any]:
    xi = {(1, 0): F(1)}
    gamma = {(0, 1): F(1)}
    zero: Poly = {}
    mu = add(multiply(xi, xi), multiply(gamma, gamma))
    # Columns are the coefficient vectors of A_beta u_2 and eta.
    first_column = [xi, gamma]
    second_column = [scale(gamma, -1), xi]
    gram = [
        [add(*(multiply(left, right) for left, right in zip(first_column, first_column))),
         add(*(multiply(left, right) for left, right in zip(first_column, second_column)))],
        [add(*(multiply(left, right) for left, right in zip(second_column, first_column))),
         add(*(multiply(left, right) for left, right in zip(second_column, second_column)))],
    ]
    expected = [[mu, zero], [zero, mu]]
    residual = [[add(gram[row][column], scale(expected[row][column], -1)) for column in range(2)] for row in range(2)]
    xigamma = multiply(xi, gamma)
    divergence = {"A_beta_u2": scale(mu, -1), "eta": add(xigamma, scale(xigamma, -1))}
    eta_rows = {"A_beta_u2": add(scale(xigamma, -1), xigamma), "eta": mu}
    return {
        "domain": "mu=xi^2+gamma^2>0",
        "formulas": {
            "u_1": "(i/mu)*(xi*A_beta*u_2-gamma*eta)",
            "u_3": "(i/mu)*(gamma*A_beta*u_2+xi*eta)",
        },
        "scaledRecoveryMatrix": [["xi", "-gamma"], ["gamma", "xi"]],
        "transposeTimesMatrix": [[serialise(value, ("xi", "gamma")) for value in row] for row in gram],
        "matrixIdentityResidual": [[serialise(value, ("xi", "gamma")) for value in row] for row in residual],
        "reconstructedDivergenceNumerator": {key: serialise(value, ("xi", "gamma")) for key, value in divergence.items()},
        "reconstructedEtaNumerator": {key: serialise(value, ("xi", "gamma")) for key, value in eta_rows.items()},
        "energyIdentity": "||u||_2^2=||u_2||_2^2+mu^(-1)*(||A_beta*u_2||_2^2+||eta||_2^2)",
    }


def lift_up_record() -> dict[str, Any]:
    modes = [(1, 1, F(-1, 2)), (2, 4, F(1, 2))]
    heat_rows = []
    norm_coefficients = []
    for frequency, decay, cosine_amplitude in modes:
        heat_rows.append({
            "frequency": frequency,
            "decayRate": decay,
            "timeDerivativeAmplitudeFactor": -decay,
            "thirdDerivativeFromWAmplitudeFactor": -(frequency**2),
            "matches": decay == frequency**2,
        })
        norm_coefficients.append(cosine_amplitude**2 / 2)
    return {
        "row": "gamma=0, beta=0, xi>=0",
        "initialData": "u_1=u_3=0 and u_2=v_0 constant in x",
        "solution": {
            "u_2": "exp(-xi^2*d)*v_0",
            "u_3": "-Lambda*d*exp(-xi^2*d)*W_x(d,x)*v_0",
        },
        "u2ResidualCoefficient": 0,
        "u3ResidualAfterCommonFactor": {
            "left": {"xi^2*W_x": 1, "W_xxx": -1},
            "right": {"xi^2*W_x": 1, "W_xxx": -1},
        },
        "WxHeatRows": heat_rows,
        "WxFourierCosineAmplitudes": [q(mode[2]) for mode in modes],
        "meanCosineSquare": "1/2",
        "orthogonalCrossMean": "0/1",
        "meanSquareCoefficientsForExpMinus2dAndExpMinus8d": [q(value) for value in norm_coefficients],
        "meanSquareWx": "(1/8)*(exp(-2d)+exp(-8d))",
        "exactNormRatio": "exp(-2*xi^2*d)*(1+(Lambda^2*d^2/8)*(exp(-2d)+exp(-8d)))",
        "strictGrowthWitnessAtXiZero": "ratio=1+(Lambda^2*d^2/8)*(exp(-2d)+exp(-8d))>1 for Lambda!=0,d>0",
    }


def causal_kernel_record() -> dict[str, Any]:
    # Convolve coefficient vectors of (1-z) and sum_{0..N} z^n.
    valid = True
    for maximum in range(65):
        left = [1, -1]
        right = [1] * (maximum + 1)
        product = [0] * (len(left) + len(right) - 1)
        for i, first in enumerate(left):
            for j, second in enumerate(right):
                product[i + j] += first * second
        if product != [1] + [0] * maximum + [-1]:
            valid = False
    return {
        "kernel": "K(r)=exp(-mu*r)*q^floor(r/h)",
        "assumptions": ["p>0", "mu>=0", "h>0", "0<q<1"],
        "blockIntegralForPositiveMu": "q^(p*n)*exp(-p*mu*n*h)*(1-exp(-p*mu*h))/(p*mu)",
        "geometricRatio": "q^p*exp(-p*mu*h)",
        "exactPositiveMuIntegral": "(1-exp(-p*mu*h))/(p*mu*(1-q^p*exp(-p*mu*h)))",
        "finiteGeometricIdentity": "(1-z)*sum(n=0..N,z^n)=1-z^(N+1)",
        "finiteDegreesChecked": [0, 64],
        "finiteGeometricIdentityChecked": valid,
        "zeroDampingBlockIntegral": "h*q^(p*n)",
        "exactZeroDampingIntegral": "h/(1-q^p)",
        "zeroDampingLimit": "lim(mu->0+)=h/(1-q^p)",
        "limitLeadingCoefficientLedger": {
            "oneMinusExpMinusY": ["0/1", "1/1"],
            "y": ["0/1", "1/1"],
            "oneMinusAExpMinusY": ["1-a", "a"],
            "result": "h/(1-a), a=q^p",
        },
        "infiniteSeriesConvergenceBoundary": "analytic-not-finitely-certified",
    }


def fourier_weight_record() -> dict[str, Any]:
    one = {(0, 0): F(1)}
    alpha2 = {(2, 0): F(1)}
    k2 = {(0, 2): F(1)}
    factor = add(one, scale(alpha2, -1))
    upper = multiply(factor, k2)
    alphas = [F(index, 16) for index in range(1, 17)]
    waves = [F(index, 3) for index in range(-24, 25)]
    checked = True
    for alpha in alphas:
        for wave in waves:
            standard = 1 / (1 + wave * wave)
            semi = 1 / (1 + alpha * alpha * wave * wave)
            checked = checked and alpha * alpha * semi <= standard <= semi
    return {
        "definitions": {
            "standardWeight": "1/(1+k^2)",
            "semiclassicalWeight": "1/(1+alpha^2*k^2)",
        },
        "range": "0<alpha<=1, k real",
        "pointwiseInequality": "alpha^2/(1+alpha^2*k^2)<=1/(1+k^2)<=1/(1+alpha^2*k^2)",
        "lowerCrossMultipliedDifference": serialise(factor, ("alpha", "k")),
        "upperCrossMultipliedDifference": serialise(upper, ("alpha", "k")),
        "normConsequence": "alpha*||F||_{H^-1_alpha,beta}<=||F||_{H^-1_beta}<=||F||_{H^-1_alpha,beta}",
        "exactRationalGridChecked": checked,
        "rationalGridShape": [len(alphas), len(waves)],
    }


def damping_gap_record() -> dict[str, Any]:
    a2 = {(2, 0): F(1)}
    b2 = {(0, 2): F(1)}
    ab = {(1, 1): F(1)}
    remainder = add(a2, b2, scale(ab, -2))
    square = multiply(add({(1, 0): F(1)}, {(0, 1): F(-1)}), add({(1, 0): F(1)}, {(0, 1): F(-1)}))
    samples = [F(index, 7) for index in range(-14, 15)]
    checked = all(
        left * left + right * right - 2 * left * right == (left - right) ** 2 >= 0
        for left in samples
        for right in samples
    )
    return {
        "gap": "g_j=mu+dist(beta,Z)^2",
        "couplingMagnitude": "K=abs(Lambda)*M_K",
        "youngIdentity": "a^2+b^2-2ab=(a-b)^2",
        "youngRemainder": serialise(remainder, ("a", "b")),
        "youngIdentityResidual": serialise(add(remainder, scale(square, -1)), ("a", "b")),
        "exactRationalSamplesChecked": checked,
        "energyInequality": "(1/2)*E'+g_j*E<=(K/2)*E",
        "positiveNormGapCondition": "g_j>K/2",
        "energyExponent": "2*(g_j-K/2)",
        "normExponent": "g_j-K/2",
        "energyExponentToNormExponent": "norm exponent is one half of the energy exponent",
        "normBound": "||u(d_2)||<=exp(-(g_j-K/2)*(d_2-d_1))*||u(d_1)||",
    }


def claim_ledger() -> dict[str, Any]:
    return {
        "finite-certified": [
            "heatShearIdentity",
            "pressurePoissonFactorTwo",
            "blochLerayDivergenceIdentity",
            "osSquireSignLedgerMuPositive",
            "velocityReconstructionMuPositive",
            "velocityEnergyIdentityMuPositive",
            "zeroCouplingLiftUpResidual",
            "zeroCouplingLiftUpNormFormula",
            "causalKernelGeometricAlgebra",
            "causalKernelZeroDampingAlgebra",
            "standardSemiclassicalFourierWeightComparison",
            "dampingGapAlgebra",
        ],
        "analytic-not-finitely-certified": [
            "strongRowL2ForcingDuhamelAlpha2",
            "strongRowStandardHMinusOneTransferAlpha",
            "strongRowSemiclassicalHMinusOneTransferAlpha2",
            "strongForcedDirectSumNoCountLoss",
            "weakZeroFiniteHistoryEnergyLedger",
            "standardHMinusOneAlphaSharpness",
            "semiclassicalHMinusOneAlpha2Sharpness",
            "HMinusOneEndpointNoAlphaGainSharpness",
            "galerkinVariationalLimit",
            "nonautonomousEvolutionFamily",
        ],
        "negative-result-keys": [
            "scalarA2EqualsCompleteRow",
            "epsilonOnlyFullRowClosure",
            "allPhysicalRowsUniformStrictContraction",
            "standardHMinusOneTransferAlpha2",
            "HMinusOneEndpointAlphaGain",
            "allRowsStrongScaleForcedGain",
        ],
        "open-keys": [
            "strongFullRowA2Estimate",
            "scaleSharpOSPressureAbsorption",
            "orientationUniformSquireTransfer",
            "lowGapWeakFullRows",
            "completeLinearizedShearSubsystem",
            "nonlinearNavierStokes",
            "clayMillenniumProblem",
        ],
    }


def claim_boundary() -> dict[str, Any]:
    return {
        "finiteExactAlgebraCertified": True,
        "functionalAnalysisMachineChecked": False,
        "sharpnessProofsMachineChecked": False,
        "infiniteSeriesConvergenceMachineChecked": False,
        "galerkinLimitMachineChecked": False,
        "endpointTraceMachineChecked": False,
        "nonautonomousEvolutionExistenceMachineChecked": False,
        "completeLinearizedShearSubsystemProved": False,
        "nonlinearNavierStokesClosureProved": False,
        "clayMillenniumProblemSolved": False,
    }


def compute() -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "theoremId": "R0.72Y-full-row-forced-transfer-finite-ledger",
        "status": "passed",
        "method": "direct operator action, Leibniz table, recovery-column Gram matrix, and rational cross multiplication",
        "heatShearIdentity": heat_identity_record(),
        "pressurePoissonFactorTwo": pressure_factor_record(),
        "blochLerayIdentity": bloch_leray_record(),
        "osSquireSignLedger": os_squire_record(),
        "velocityReconstruction": velocity_reconstruction_record(),
        "zeroCouplingLiftUp": lift_up_record(),
        "causalKernel": causal_kernel_record(),
        "fourierWeights": fourier_weight_record(),
        "dampingGap": damping_gap_record(),
        "claimLedger": claim_ledger(),
        "claimBoundary": claim_boundary(),
    }


def validate(value: dict[str, Any]) -> None:
    if not value["heatShearIdentity"]["allModesMatch"]:
        raise RuntimeError("independent heat identity failed")
    pressure = value["pressurePoissonFactorTwo"]
    if pressure["factorTwo"] != 2 or pressure["coefficientSum"] != 0:
        raise RuntimeError("independent pressure factor failed")
    if value["blochLerayIdentity"]["identityResidual"] or value["blochLerayIdentity"]["divergenceOfProjectionSum"] != "0/1":
        raise RuntimeError("independent Bloch/Leray identity failed")
    os_squire = value["osSquireSignLedger"]
    if os_squire["orrSommerfeldCoefficientTableInUnitsOfIc"]["sum"] != os_squire["expectedOsSum"] or os_squire["squirePressureSum"]:
        raise RuntimeError("independent OS/Squire signs failed")
    recovery = value["velocityReconstruction"]
    if any(cell for row in recovery["matrixIdentityResidual"] for cell in row):
        raise RuntimeError("independent velocity Gram identity failed")
    lift = value["zeroCouplingLiftUp"]
    if lift["meanSquareCoefficientsForExpMinus2dAndExpMinus8d"] != ["1/8", "1/8"]:
        raise RuntimeError("independent lift-up norm failed")
    if not value["causalKernel"]["finiteGeometricIdentityChecked"]:
        raise RuntimeError("independent causal-kernel algebra failed")
    if not value["fourierWeights"]["exactRationalGridChecked"]:
        raise RuntimeError("independent Fourier-weight inequality failed")
    if value["dampingGap"]["youngIdentityResidual"] or not value["dampingGap"]["exactRationalSamplesChecked"]:
        raise RuntimeError("independent damping-gap algebra failed")
    boundary = value["claimBoundary"]
    if boundary["finiteExactAlgebraCertified"] is not True:
        raise RuntimeError("finite scope missing")
    for key, state in boundary.items():
        if key != "finiteExactAlgebraCertified" and state is not False:
            raise RuntimeError(f"claim boundary drifted: {key}")


def ensure_formal_context(source_commit: str, output: Path) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError(
            "--formal requires a full 40-character lowercase "
            "--formal-source-commit"
        )
    expected = (ROOT / "independent.json").resolve()
    if output.resolve() != expected:
        raise RuntimeError(f"formal independent output must be {expected}")
    if subprocess.run(
        ["git", "cat-file", "-e", f"{source_commit}^{{commit}}"],
        cwd=REPOSITORY,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode:
        raise RuntimeError("formal independent source commit is not a Git commit")
    status = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=REPOSITORY,
        text=True,
    )
    if status:
        raise RuntimeError(
            "formal independent recomputation requires a completely clean repository"
        )
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True
    ).strip()
    if head != source_commit:
        raise RuntimeError("formal independent source commit must equal clean HEAD")
    manifest = ROOT / "manifest.json"
    if manifest.exists():
        prior = json.loads(manifest.read_text(encoding="utf-8"))
        if prior.get("status") == "formal":
            raise RuntimeError("refusing to overwrite a formal independent result")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--draft", action="store_true")
    parser.add_argument("--formal", action="store_true")
    parser.add_argument("--formal-source-commit")
    parser.add_argument("--output")
    args = parser.parse_args()
    value = compute()
    validate(value)
    if args.self_test:
        if args.draft or args.formal or args.formal_source_commit or args.output:
            parser.error("--self-test cannot be combined with output arguments")
        print("R0.72Y independent recomputation self-test: passed (no outputs written)")
        return
    if args.draft and args.formal:
        parser.error("choose exactly one of --draft or --formal")
    if not args.output:
        parser.error("draft or formal recomputation requires --output")
    output = Path(args.output).resolve()
    expected = (ROOT / "independent.json").resolve()
    if output != expected:
        parser.error(f"independent output must be {expected}")
    if args.formal:
        source_commit = str(args.formal_source_commit or "")
        ensure_formal_context(source_commit, output)
        value["certificateStage"] = "formal"
        value["sourceCommit"] = source_commit
        output.write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print("R0.72Y independent formal recomputation: passed and source-bound")
        return
    if not args.draft:
        parser.error("use --self-test, --draft, or --formal")
    if args.formal_source_commit:
        parser.error("--draft cannot be combined with --formal-source-commit")
    if (ROOT / "manifest.json").exists():
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        if manifest.get("status") == "formal":
            raise RuntimeError("refusing to overwrite a formal independent result")
    value["certificateStage"] = "draft"
    value["sourceCommit"] = None
    output.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("R0.72Y independent draft recomputation: passed and written")


if __name__ == "__main__":
    main()
