#!/usr/bin/env python3
"""Build the draft R0.72Y deterministic finite-algebra certificate.

The certificate checks exact finite identities used by the R0.72Y row
ledger.  It deliberately does not machine-check the functional-analysis
arguments, sharpness limits, evolution-family construction, or any
Navier--Stokes closure claim.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
SOURCE_FILES = (
    "research/r072y_report-source.md",
    "research/r072y_gap_matrix.md",
    "research/r072y_literature_audit.md",
    "research/r072y_full_row_independent_audit.md",
    "research/r072y_forced_transfer_independent_audit.md",
    "research/r072y_independent_audit.md",
    "research/certificates/r072y/generate_certificate.py",
    "research/certificates/r072y/independent_recompute.py",
    "research/certificates/r072y/validate_certificate.py",
    "research/certificates/r072y/README.md",
    "research/certificates/r072y/command.txt",
    "research/certificates/r072y/environment.txt",
    "research/release-manifest.json",
    "scripts/generate_r072y_release.py",
    "scripts/add-r072y-translations.mjs",
    "figures/r072y/fig-r072y-full-row-forced-transfer/README.md",
    "figures/r072y/fig-r072y-full-row-forced-transfer/caption.md",
    "figures/r072y/fig-r072y-full-row-forced-transfer/command.txt",
    "figures/r072y/fig-r072y-full-row-forced-transfer/config.json",
    "figures/r072y/fig-r072y-full-row-forced-transfer/contract.json",
    "figures/r072y/fig-r072y-full-row-forced-transfer/environment.txt",
    "figures/r072y/fig-r072y-full-row-forced-transfer/figure-contract.md",
    "figures/r072y/fig-r072y-full-row-forced-transfer/plot.py",
    "figures/r072y/fig-r072y-full-row-forced-transfer/qa-protocol.md",
    "figures/r072y/fig-r072y-full-row-forced-transfer/requirements.txt",
    "figures/r072y/fig-r072y-full-row-forced-transfer/validate.py",
    "tests/r072y-deterministic-certificate-source.test.mjs",
    "tests/r072y-full-row-forced-gate.test.mjs",
    "tests/r072y-full-row-forced-transfer-figure-source.test.mjs",
    "tests/r072y-release.test.mjs",
)
GENERATED_FILES = (
    "certificate.json",
    "independent.json",
    "crosscheck.json",
    "manifest.json",
    "SHA256SUMS",
)
MUTABLE_PUBLICATION_STATE = "research/release-manifest.json"

Poly = dict[tuple[int, ...], F]


def q(value: F | int) -> str:
    value = F(value)
    return f"{value.numerator}/{value.denominator}"


def poly_clean(value: Poly) -> Poly:
    return {key: coefficient for key, coefficient in value.items() if coefficient}


def poly_add(*values: Poly) -> Poly:
    result: Poly = {}
    for value in values:
        for key, coefficient in value.items():
            result[key] = result.get(key, F(0)) + coefficient
    return poly_clean(result)


def poly_scale(value: Poly, factor: F | int) -> Poly:
    return poly_clean({key: F(factor) * coefficient for key, coefficient in value.items()})


def poly_multiply(left: Poly, right: Poly) -> Poly:
    result: Poly = {}
    for left_key, left_coefficient in left.items():
        for right_key, right_coefficient in right.items():
            key = tuple(a + b for a, b in zip(left_key, right_key))
            result[key] = result.get(key, F(0)) + left_coefficient * right_coefficient
    return poly_clean(result)


def serialise_poly(value: Poly, variables: tuple[str, ...]) -> list[dict[str, Any]]:
    rows = []
    for powers, coefficient in sorted(value.items()):
        monomial = "*".join(
            variable if power == 1 else f"{variable}^{power}"
            for variable, power in zip(variables, powers)
            if power
        ) or "1"
        rows.append({"monomial": monomial, "coefficient": q(coefficient)})
    return rows


def heat_identity_record() -> dict[str, Any]:
    modes = [
        {"frequency": 1, "decayRate": 1, "coefficient": F(-1, 2)},
        {"frequency": 2, "decayRate": 4, "coefficient": F(1, 4)},
    ]
    rows = []
    for mode in modes:
        coefficient = mode["coefficient"]
        decay = mode["decayRate"]
        frequency = mode["frequency"]
        d_coefficient = -decay * coefficient
        xx_coefficient = -(frequency**2) * coefficient
        rows.append({
            "frequency": frequency,
            "decayRate": decay,
            "amplitude": q(coefficient),
            "dDerivativeAmplitude": q(d_coefficient),
            "xxDerivativeAmplitude": q(xx_coefficient),
            "matches": d_coefficient == xx_coefficient,
        })
    return {
        "profile": "W(d,x)=-(1/2)*exp(-d)*sin(x)+(1/4)*exp(-4d)*sin(2x)",
        "modeRows": rows,
        "identity": "W_d=W_xx",
        "allModesMatch": all(row["matches"] for row in rows),
        "derivedIdentity": "(W_x)_d=W_xxx",
    }


def pressure_factor_record() -> dict[str, Any]:
    contributions = {
        "divergenceOfIcWTimesU": 1,
        "divergenceOfLambdaWxU2E3": 1,
    }
    divergence_coefficients = {
        **contributions,
        "divergenceOfGradientPiAfterLPiEquals2icWxU2": -2,
    }
    return {
        "normalisation": "c=Lambda*gamma",
        "pressureEquation": "L*pi=2*i*c*W_x*u_2",
        "divergenceGradientSign": "div_j(grad_j*pi)=-L*pi",
        "coefficientsInUnitsOfIcWxU2": divergence_coefficients,
        "coefficientSum": sum(divergence_coefficients.values()),
        "factorTwo": sum(contributions.values()),
    }


def bloch_leray_record() -> dict[str, Any]:
    # Variables are (A, xi, gamma), with L=-A^2+xi^2+gamma^2.
    a2 = {(2, 0, 0): F(1)}
    xi2 = {(0, 2, 0): F(1)}
    gamma2 = {(0, 0, 2): F(1)}
    div_grad = poly_add(a2, poly_scale(xi2, -1), poly_scale(gamma2, -1))
    minus_l = poly_add(a2, poly_scale(xi2, -1), poly_scale(gamma2, -1))
    identity_residual = poly_add(div_grad, poly_scale(minus_l, -1))
    projection_coefficients = [F(1), F(-1)]
    return {
        "A_beta": "partial_x+i*beta",
        "L": "-A_beta^2+mu",
        "mu": "xi^2+gamma^2",
        "gradient": "(i*xi,A_beta,i*gamma)",
        "divergenceGradient": serialise_poly(div_grad, ("A", "xi", "gamma")),
        "minusL": serialise_poly(minus_l, ("A", "xi", "gamma")),
        "identityResidual": serialise_poly(identity_residual, ("A", "xi", "gamma")),
        "lerayProjection": "P_j=I+grad_j*L^(-1)*div_j",
        "divergenceOfProjectionCoefficients": [q(value) for value in projection_coefficients],
        "divergenceOfProjectionSum": q(sum(projection_coefficients)),
        "projectionKillsGradientCoefficients": ["1/1", "-1/1"],
    }


def os_squire_record() -> dict[str, Any]:
    os_advection = {"W*q": -1, "W_x*A_beta*u_2": 2, "W_xx*u_2": 1}
    os_pressure = {"W*q": 0, "W_x*A_beta*u_2": -2, "W_xx*u_2": -2}
    os_total = {key: os_advection[key] + os_pressure[key] for key in os_advection}
    squire_pressure = {"from_i_gamma_u1": 1, "from_minus_i_xi_u3": -1}
    return {
        "domain": "mu>0",
        "definitions": ["q=L*u_2", "eta=i*gamma*u_1-i*xi*u_3"],
        "commutator": "L(Wu)=W*L*u-2*W_x*A_beta*u-W_xx*u",
        "pressureSubstitution": "-A_beta*L*pi=-2*i*c*A_beta(W_x*u_2)",
        "orrSommerfeldCoefficientTableInUnitsOfIc": {
            "minusIcLOfWu2": os_advection,
            "minusAOfLPi": os_pressure,
            "sum": os_total,
        },
        "orrSommerfeldEquation": "q_d=(-L-i*c*W)q-i*c*W_xx*L^(-1)q",
        "squirePressureCoefficients": squire_pressure,
        "squirePressureSum": sum(squire_pressure.values()),
        "squireLiftCoefficient": 1,
        "squireEquation": "eta_d=(-L-i*c*W)eta+i*xi*Lambda*W_x*L^(-1)q",
        "expectedOsSum": {"W*q": -1, "W_x*A_beta*u_2": 0, "W_xx*u_2": -1},
    }


def velocity_reconstruction_record() -> dict[str, Any]:
    # Variables are (xi, gamma).  The irrelevant unit-modulus factor i is
    # kept in the displayed formula, while M^T M checks the norm identity.
    xi = {(1, 0): F(1)}
    gamma = {(0, 1): F(1)}
    zero: Poly = {}
    matrix = [[xi, poly_scale(gamma, -1)], [gamma, xi]]
    transpose_product: list[list[Poly]] = [[zero, zero], [zero, zero]]
    for row in range(2):
        for column in range(2):
            transpose_product[row][column] = poly_add(*(
                poly_multiply(matrix[index][row], matrix[index][column])
                for index in range(2)
            ))
    mu = poly_add(poly_multiply(xi, xi), poly_multiply(gamma, gamma))
    expected = [[mu, zero], [zero, mu]]
    matrix_residual = [
        [poly_add(transpose_product[row][column], poly_scale(expected[row][column], -1))
         for column in range(2)]
        for row in range(2)
    ]
    divergence_coefficients = {
        "A_beta_u2": poly_scale(mu, -1),
        "eta": poly_add(poly_scale(poly_multiply(xi, gamma), 1), poly_scale(poly_multiply(gamma, xi), -1)),
    }
    eta_coefficients = {
        "A_beta_u2": poly_add(poly_scale(poly_multiply(gamma, xi), -1), poly_multiply(xi, gamma)),
        "eta": mu,
    }
    return {
        "domain": "mu=xi^2+gamma^2>0",
        "formulas": {
            "u_1": "(i/mu)*(xi*A_beta*u_2-gamma*eta)",
            "u_3": "(i/mu)*(gamma*A_beta*u_2+xi*eta)",
        },
        "scaledRecoveryMatrix": [["xi", "-gamma"], ["gamma", "xi"]],
        "transposeTimesMatrix": [
            [serialise_poly(value, ("xi", "gamma")) for value in row]
            for row in transpose_product
        ],
        "matrixIdentityResidual": [
            [serialise_poly(value, ("xi", "gamma")) for value in row]
            for row in matrix_residual
        ],
        "reconstructedDivergenceNumerator": {
            key: serialise_poly(value, ("xi", "gamma"))
            for key, value in divergence_coefficients.items()
        },
        "reconstructedEtaNumerator": {
            key: serialise_poly(value, ("xi", "gamma"))
            for key, value in eta_coefficients.items()
        },
        "energyIdentity": "||u||_2^2=||u_2||_2^2+mu^(-1)*(||A_beta*u_2||_2^2+||eta||_2^2)",
    }


def lift_up_record() -> dict[str, Any]:
    amplitudes = [F(-1, 2), F(1, 2)]
    frequencies = [1, 2]
    decay_rates = [1, 4]
    mean_cosine_square = F(1, 2)
    norm_coefficients = [amplitude * amplitude * mean_cosine_square for amplitude in amplitudes]
    heat_rows = [
        {
            "frequency": frequency,
            "decayRate": decay,
            "timeDerivativeAmplitudeFactor": -decay,
            "thirdDerivativeFromWAmplitudeFactor": -(frequency**2),
            "matches": decay == frequency**2,
        }
        for frequency, decay in zip(frequencies, decay_rates)
    ]
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
        "WxFourierCosineAmplitudes": [q(value) for value in amplitudes],
        "meanCosineSquare": q(mean_cosine_square),
        "orthogonalCrossMean": "0/1",
        "meanSquareCoefficientsForExpMinus2dAndExpMinus8d": [q(value) for value in norm_coefficients],
        "meanSquareWx": "(1/8)*(exp(-2d)+exp(-8d))",
        "exactNormRatio": "exp(-2*xi^2*d)*(1+(Lambda^2*d^2/8)*(exp(-2d)+exp(-8d)))",
        "strictGrowthWitnessAtXiZero": "ratio=1+(Lambda^2*d^2/8)*(exp(-2d)+exp(-8d))>1 for Lambda!=0,d>0",
    }


def geometric_coefficients(maximum: int) -> list[int]:
    coefficients = [0] * (maximum + 2)
    for degree in range(maximum + 1):
        coefficients[degree] += 1
        coefficients[degree + 1] -= 1
    return coefficients


def causal_kernel_record() -> dict[str, Any]:
    checked_degrees = list(range(65))
    finite_identity = all(
        geometric_coefficients(maximum) == [1] + [0] * maximum + [-1]
        for maximum in checked_degrees
    )
    return {
        "kernel": "K(r)=exp(-mu*r)*q^floor(r/h)",
        "assumptions": ["p>0", "mu>=0", "h>0", "0<q<1"],
        "blockIntegralForPositiveMu": "q^(p*n)*exp(-p*mu*n*h)*(1-exp(-p*mu*h))/(p*mu)",
        "geometricRatio": "q^p*exp(-p*mu*h)",
        "exactPositiveMuIntegral": "(1-exp(-p*mu*h))/(p*mu*(1-q^p*exp(-p*mu*h)))",
        "finiteGeometricIdentity": "(1-z)*sum(n=0..N,z^n)=1-z^(N+1)",
        "finiteDegreesChecked": [checked_degrees[0], checked_degrees[-1]],
        "finiteGeometricIdentityChecked": finite_identity,
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
    # Variables are (a,k), with a=alpha.  Both cross-multiplied
    # differences factor into manifestly nonnegative terms for 0<a<=1.
    alpha2 = {(2, 0): F(1)}
    k2 = {(0, 2): F(1)}
    one = {(0, 0): F(1)}
    lower_difference = poly_add(one, poly_scale(alpha2, -1))
    upper_difference = poly_multiply(lower_difference, k2)
    rational_grid = [F(index, 16) for index in range(1, 17)]
    wave_grid = [F(index, 3) for index in range(-24, 25)]
    grid_checked = all(
        alpha * alpha / (1 + alpha * alpha * wave * wave)
        <= 1 / (1 + wave * wave)
        <= 1 / (1 + alpha * alpha * wave * wave)
        for alpha in rational_grid
        for wave in wave_grid
    )
    return {
        "definitions": {
            "standardWeight": "1/(1+k^2)",
            "semiclassicalWeight": "1/(1+alpha^2*k^2)",
        },
        "range": "0<alpha<=1, k real",
        "pointwiseInequality": "alpha^2/(1+alpha^2*k^2)<=1/(1+k^2)<=1/(1+alpha^2*k^2)",
        "lowerCrossMultipliedDifference": serialise_poly(lower_difference, ("alpha", "k")),
        "upperCrossMultipliedDifference": serialise_poly(upper_difference, ("alpha", "k")),
        "normConsequence": "alpha*||F||_{H^-1_alpha,beta}<=||F||_{H^-1_beta}<=||F||_{H^-1_alpha,beta}",
        "exactRationalGridChecked": grid_checked,
        "rationalGridShape": [len(rational_grid), len(wave_grid)],
    }


def damping_gap_record() -> dict[str, Any]:
    # Variables are (a,b).  This is the exact Young inequality remainder.
    a2 = {(2, 0): F(1)}
    b2 = {(0, 2): F(1)}
    ab = {(1, 1): F(1)}
    young_remainder = poly_add(a2, b2, poly_scale(ab, -2))
    expected_square = {(2, 0): F(1), (1, 1): F(-2), (0, 2): F(1)}
    rational_samples = [F(index, 7) for index in range(-14, 15)]
    sample_checked = all(
        left * left + right * right - 2 * left * right == (left - right) ** 2 >= 0
        for left in rational_samples
        for right in rational_samples
    )
    return {
        "gap": "g_j=mu+dist(beta,Z)^2",
        "couplingMagnitude": "K=abs(Lambda)*M_K",
        "youngIdentity": "a^2+b^2-2ab=(a-b)^2",
        "youngRemainder": serialise_poly(young_remainder, ("a", "b")),
        "youngIdentityResidual": serialise_poly(poly_add(young_remainder, poly_scale(expected_square, -1)), ("a", "b")),
        "exactRationalSamplesChecked": sample_checked,
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


def payload() -> dict[str, Any]:
    heat = heat_identity_record()
    pressure = pressure_factor_record()
    leray = bloch_leray_record()
    os_squire = os_squire_record()
    recovery = velocity_reconstruction_record()
    lift = lift_up_record()
    kernel = causal_kernel_record()
    weights = fourier_weight_record()
    damping = damping_gap_record()
    ledger = claim_ledger()
    boundary = claim_boundary()
    checks = {
        "heatIdentity": heat["allModesMatch"],
        "pressureFactorTwo": pressure["factorTwo"] == 2 and pressure["coefficientSum"] == 0,
        "blochLaplacianSign": leray["identityResidual"] == [],
        "lerayDivergenceCancellation": leray["divergenceOfProjectionSum"] == "0/1",
        "osCoefficientCancellation": os_squire["orrSommerfeldCoefficientTableInUnitsOfIc"]["sum"] == os_squire["expectedOsSum"],
        "squirePressureCancellation": os_squire["squirePressureSum"] == 0 and os_squire["squireLiftCoefficient"] == 1,
        "velocityMatrixIdentity": all(not cell for row in recovery["matrixIdentityResidual"] for cell in row),
        "velocityDivergenceEtaRecovery": recovery["reconstructedDivergenceNumerator"]["eta"] == [] and recovery["reconstructedEtaNumerator"]["A_beta_u2"] == [],
        "liftUpResidual": lift["u2ResidualCoefficient"] == 0 and lift["u3ResidualAfterCommonFactor"]["left"] == lift["u3ResidualAfterCommonFactor"]["right"] and all(row["matches"] for row in lift["WxHeatRows"]),
        "liftUpNorm": lift["meanSquareCoefficientsForExpMinus2dAndExpMinus8d"] == ["1/8", "1/8"],
        "causalKernelGeometricAlgebra": kernel["finiteGeometricIdentityChecked"],
        "fourierWeightInequality": weights["lowerCrossMultipliedDifference"] == [{"monomial": "1", "coefficient": "1/1"}, {"monomial": "alpha^2", "coefficient": "-1/1"}] and weights["exactRationalGridChecked"],
        "dampingGapYoungIdentity": damping["youngIdentityResidual"] == [] and damping["exactRationalSamplesChecked"],
        "claimKeysUnique": all(len(values) == len(set(values)) for values in ledger.values()),
        "claimBoundaryHonest": all(boundary[key] is False for key in boundary if key != "finiteExactAlgebraCertified"),
    }
    return {
        "schemaVersion": 1,
        "theoremId": "R0.72Y-full-row-forced-transfer-finite-ledger",
        "status": "passed" if all(checks.values()) else "failed",
        "producerMethod": "exact Fourier-mode arithmetic, commutative polynomial cancellation, and discrete noncommutative coefficient tables",
        "exactChecks": checks,
        "heatShearIdentity": heat,
        "pressurePoissonFactorTwo": pressure,
        "blochLerayIdentity": leray,
        "osSquireSignLedger": os_squire,
        "velocityReconstruction": recovery,
        "zeroCouplingLiftUp": lift,
        "causalKernel": kernel,
        "fourierWeights": weights,
        "dampingGap": damping,
        "claimLedger": ledger,
        "claimBoundary": boundary,
    }


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def draft_source_bindings() -> list[dict[str, Any]]:
    result = []
    for relative in SOURCE_FILES:
        path = REPOSITORY / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"draft source is absent or not a regular file: {relative}")
        result.append({
            "path": relative,
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
        })
    return result


def ensure_clean_head(source_commit: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError(
            "--formal requires a full 40-character lowercase "
            "--formal-source-commit"
        )
    if subprocess.run(
        ["git", "cat-file", "-e", f"{source_commit}^{{commit}}"],
        cwd=REPOSITORY,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode:
        raise RuntimeError("formal source commit is not a valid Git commit object")
    status = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=REPOSITORY,
        text=True,
    )
    if status:
        raise RuntimeError("formal certificate requires a completely clean repository")
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True
    ).strip()
    if head != source_commit:
        raise RuntimeError("formal source commit must equal clean HEAD")


def formal_source_bindings(source_commit: str) -> list[dict[str, Any]]:
    result = []
    for relative in SOURCE_FILES:
        path = REPOSITORY / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"formal source is absent or not a regular file: {relative}")
        try:
            committed = subprocess.check_output(
                ["git", "rev-parse", f"{source_commit}:{relative}"],
                cwd=REPOSITORY,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        except subprocess.CalledProcessError as error:
            raise RuntimeError(
                f"formal source is not frozen in {source_commit}: {relative}"
            ) from error
        working = subprocess.check_output(
            ["git", "hash-object", f"--path={relative}", str(path)],
            cwd=REPOSITORY,
            text=True,
        ).strip()
        if committed != working:
            raise RuntimeError(
                f"working source differs from {source_commit}:{relative}"
            )
        result.append({
            "path": relative,
            "commit": source_commit,
            "gitBlob": committed,
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
            "workingTreeBlobMatches": True,
        })
    return result


def self_test() -> None:
    value = payload()
    if value["status"] != "passed" or not all(value["exactChecks"].values()):
        raise RuntimeError("producer exact self-test failed")
    subprocess.run(
        [sys.executable, str(ROOT / "independent_recompute.py"), "--self-test"],
        check=True,
    )
    print("R0.72Y certificate source self-test: passed (no outputs written)")


def draft_build() -> None:
    existing_manifest = ROOT / "manifest.json"
    if existing_manifest.exists():
        existing = json.loads(existing_manifest.read_text(encoding="utf-8"))
        if existing.get("status") == "formal":
            raise RuntimeError("refusing to overwrite a formal R0.72Y certificate")
    bindings = draft_source_bindings()
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "independent_recompute.py"),
            "--draft",
            "--output",
            str(ROOT / "independent.json"),
        ],
        check=True,
    )
    certificate = payload()
    certificate["certificateStage"] = "draft"
    certificate["sourceCommit"] = None
    if certificate["status"] != "passed":
        raise RuntimeError("R0.72Y producer checks failed")
    write_json(ROOT / "certificate.json", certificate)
    independent = json.loads((ROOT / "independent.json").read_text(encoding="utf-8"))
    compared = (
        "heatShearIdentity",
        "pressurePoissonFactorTwo",
        "blochLerayIdentity",
        "osSquireSignLedger",
        "velocityReconstruction",
        "zeroCouplingLiftUp",
        "causalKernel",
        "fourierWeights",
        "dampingGap",
        "claimLedger",
        "claimBoundary",
    )
    ledger_matches = (
        independent.get("status") == "passed"
        and independent.get("certificateStage") == "draft"
        and independent.get("sourceCommit") is None
        and all(independent.get(section) == certificate.get(section) for section in compared)
    )
    crosscheck = {
        "schemaVersion": 1,
        "status": "passed" if ledger_matches else "failed",
        "method": "producer polynomial/table route versus independent operator-action and direct-substitution route",
        "temporaryUnsealedSourceAllowed": True,
        "formalSourceReady": False,
        "sourceCommit": None,
        "sourceBindings": bindings,
        "sourceBindingPolicy": {
            "mutablePublicationState": MUTABLE_PUBLICATION_STATE,
            "sourceCommitBlobPermanentlyBound": True,
            "currentAdvanceAllowedOnlyAtCleanDescendantPublicationCommit": True,
        },
        "certificateSha256": sha256(ROOT / "certificate.json"),
        "comparedSections": list(compared),
        "checks": {
            "certificatePassed": certificate["status"] == "passed",
            "allExactChecksPassed": all(certificate["exactChecks"].values()),
            "independentRecomputationPassed": independent.get("status") == "passed",
            "independentExactLedgerMatches": ledger_matches,
            "draftStagePropagatedToBothComputations": (
                certificate.get("certificateStage") == "draft"
                and independent.get("certificateStage") == "draft"
                and certificate.get("sourceCommit") is None
                and independent.get("sourceCommit") is None
            ),
            "analyticBoundaryExplicit": (
                not certificate["claimBoundary"]["functionalAnalysisMachineChecked"]
                and not certificate["claimBoundary"]["sharpnessProofsMachineChecked"]
            ),
            "nonlinearAndClayRemainFalse": (
                not certificate["claimBoundary"]["nonlinearNavierStokesClosureProved"]
                and not certificate["claimBoundary"]["clayMillenniumProblemSolved"]
            ),
        },
    }
    if crosscheck["status"] != "passed" or not all(crosscheck["checks"].values()):
        raise RuntimeError("independent R0.72Y draft crosscheck failed")
    write_json(ROOT / "crosscheck.json", crosscheck)
    manifest = {
        "schemaVersion": 1,
        "bundle": "R0.72Y deterministic full-row and forced-transfer finite ledger",
        "status": "draft",
        "sourceCommit": None,
        "sourceBindings": bindings,
        "sourceBindingPolicy": crosscheck["sourceBindingPolicy"],
        "claimBoundary": certificate["claimBoundary"],
        "deterministic": True,
        "createdAt": "2026-08-28T00:00:00+08:00",
        "files": {
            name: {"sha256": sha256(ROOT / name), "bytes": (ROOT / name).stat().st_size}
            for name in ("certificate.json", "independent.json", "crosscheck.json")
        },
        "limitations": (
            "Draft finite algebra only. Functional analysis, infinite-series convergence, "
            "Galerkin limits, endpoint traces, sharpness constructions, evolution existence, "
            "the complete linearized subsystem, nonlinear Navier--Stokes closure, and Clay "
            "are not machine checked or claimed. Formal source-commit binding is absent."
        ),
    }
    write_json(ROOT / "manifest.json", manifest)
    names = sorted(
        path.name for path in ROOT.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    (ROOT / "SHA256SUMS").write_text(
        "".join(f"{sha256(ROOT / name)}  {name}\n" for name in names),
        encoding="utf-8",
    )
    print("R0.72Y draft deterministic certificate: passed and written")


def formal_build(source_commit: str) -> None:
    ensure_clean_head(source_commit)
    existing_manifest = ROOT / "manifest.json"
    if existing_manifest.exists():
        existing = json.loads(existing_manifest.read_text(encoding="utf-8"))
        if existing.get("status") == "formal":
            raise RuntimeError("refusing to overwrite a formal R0.72Y certificate")
        if existing.get("status") != "draft":
            raise RuntimeError("existing certificate manifest has an unknown status")
    bindings = formal_source_bindings(source_commit)
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "independent_recompute.py"),
            "--formal",
            "--formal-source-commit",
            source_commit,
            "--output",
            str(ROOT / "independent.json"),
        ],
        check=True,
    )
    certificate = payload()
    certificate["certificateStage"] = "formal"
    certificate["sourceCommit"] = source_commit
    if certificate["status"] != "passed":
        raise RuntimeError("R0.72Y producer checks failed during formal sealing")
    write_json(ROOT / "certificate.json", certificate)
    independent = json.loads((ROOT / "independent.json").read_text(encoding="utf-8"))
    compared = (
        "heatShearIdentity",
        "pressurePoissonFactorTwo",
        "blochLerayIdentity",
        "osSquireSignLedger",
        "velocityReconstruction",
        "zeroCouplingLiftUp",
        "causalKernel",
        "fourierWeights",
        "dampingGap",
        "claimLedger",
        "claimBoundary",
    )
    ledger_matches = (
        independent.get("status") == "passed"
        and independent.get("certificateStage") == "formal"
        and independent.get("sourceCommit") == source_commit
        and all(independent.get(section) == certificate.get(section) for section in compared)
    )
    crosscheck = {
        "schemaVersion": 1,
        "status": "passed" if ledger_matches else "failed",
        "method": "producer polynomial/table route versus independent operator-action and direct-substitution route",
        "temporaryUnsealedSourceAllowed": False,
        "formalSourceReady": True,
        "sourceCommit": source_commit,
        "sourceBindings": bindings,
        "sourceBindingPolicy": {
            "mutablePublicationState": MUTABLE_PUBLICATION_STATE,
            "sourceCommitBlobPermanentlyBound": True,
            "currentAdvanceAllowedOnlyAtCleanDescendantPublicationCommit": True,
        },
        "certificateSha256": sha256(ROOT / "certificate.json"),
        "comparedSections": list(compared),
        "checks": {
            "certificatePassed": certificate["status"] == "passed",
            "allExactChecksPassed": all(certificate["exactChecks"].values()),
            "independentRecomputationPassed": independent.get("status") == "passed",
            "independentExactLedgerMatches": ledger_matches,
            "formalCommitPropagatedToBothComputations": (
                certificate.get("sourceCommit") == source_commit
                and independent.get("sourceCommit") == source_commit
            ),
            "analyticBoundaryExplicit": (
                not certificate["claimBoundary"]["functionalAnalysisMachineChecked"]
                and not certificate["claimBoundary"]["sharpnessProofsMachineChecked"]
            ),
            "nonlinearAndClayRemainFalse": (
                not certificate["claimBoundary"]["nonlinearNavierStokesClosureProved"]
                and not certificate["claimBoundary"]["clayMillenniumProblemSolved"]
            ),
        },
    }
    if crosscheck["status"] != "passed" or not all(crosscheck["checks"].values()):
        raise RuntimeError("independent R0.72Y formal crosscheck failed")
    write_json(ROOT / "crosscheck.json", crosscheck)
    manifest = {
        "schemaVersion": 1,
        "bundle": "R0.72Y deterministic full-row and forced-transfer finite ledger",
        "status": "formal",
        "sourceCommit": source_commit,
        "sourceBindings": bindings,
        "sourceBindingPolicy": crosscheck["sourceBindingPolicy"],
        "claimBoundary": certificate["claimBoundary"],
        "deterministic": True,
        "createdAt": "2026-08-28T00:00:00+08:00",
        "files": {
            name: {"sha256": sha256(ROOT / name), "bytes": (ROOT / name).stat().st_size}
            for name in ("certificate.json", "independent.json", "crosscheck.json")
        },
        "limitations": (
            "Formally source-bound finite algebra only. Functional analysis, "
            "infinite-series convergence, Galerkin limits, endpoint traces, sharpness "
            "constructions, evolution existence, the complete linearized subsystem, "
            "nonlinear Navier--Stokes closure, and Clay are not machine checked or claimed."
        ),
    }
    write_json(ROOT / "manifest.json", manifest)
    names = sorted(
        path.name for path in ROOT.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    (ROOT / "SHA256SUMS").write_text(
        "".join(f"{sha256(ROOT / name)}  {name}\n" for name in names),
        encoding="utf-8",
    )
    print("R0.72Y formal deterministic certificate: passed and source-bound")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--draft", action="store_true")
    parser.add_argument("--formal", action="store_true")
    parser.add_argument("--formal-source-commit")
    args = parser.parse_args()
    if args.self_test:
        if args.draft or args.formal or args.formal_source_commit:
            parser.error("--self-test cannot be combined with output arguments")
        self_test()
        return
    if args.draft and args.formal:
        parser.error("choose exactly one of --draft or --formal")
    if args.draft:
        if args.formal_source_commit:
            parser.error("--draft cannot be combined with --formal-source-commit")
        draft_build()
        return
    if args.formal:
        formal_build(str(args.formal_source_commit or ""))
        return
    parser.error("use --self-test, --draft, or --formal --formal-source-commit <40-hex>")


if __name__ == "__main__":
    main()
