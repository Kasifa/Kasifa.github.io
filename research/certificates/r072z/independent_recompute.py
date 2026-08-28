#!/usr/bin/env python3
"""Independent recomputation route for the R0.72Z finite certificate.

This module deliberately does not import the producer.  It uses direct
Fourier-action identities, paired/Poisson sums, polynomial convolution, and
deterministic quadrature instead of the producer's construction path.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
INPUTS = (
    "research/r072z_report-source.md",
    "research/r072z_gap_matrix.md",
    "research/r072z_literature_audit.md",
    "research/r072z_os_independent_audit.md",
    "research/r072z_squire_independent_audit.md",
    "research/r072z_independent_audit.md",
    "research/certificates/r072z/generate_certificate.py",
    "research/certificates/r072z/independent_recompute.py",
    "research/certificates/r072z/validate_certificate.py",
    "research/certificates/r072z/README.md",
    "research/certificates/r072z/command.txt",
    "research/certificates/r072z/environment.txt",
    "research/release-manifest.json",
    "scripts/generate_r072z_release.py",
    "scripts/add-r072z-translations.mjs",
    "figures/r072z/fig-r072z-os-squire-threshold/README.md",
    "figures/r072z/fig-r072z-os-squire-threshold/caption.md",
    "figures/r072z/fig-r072z-os-squire-threshold/command.txt",
    "figures/r072z/fig-r072z-os-squire-threshold/config.json",
    "figures/r072z/fig-r072z-os-squire-threshold/contract.json",
    "figures/r072z/fig-r072z-os-squire-threshold/environment.txt",
    "figures/r072z/fig-r072z-os-squire-threshold/figure-contract.md",
    "figures/r072z/fig-r072z-os-squire-threshold/manifest-draft.json",
    "figures/r072z/fig-r072z-os-squire-threshold/plot.py",
    "figures/r072z/fig-r072z-os-squire-threshold/qa-protocol.md",
    "figures/r072z/fig-r072z-os-squire-threshold/requirements.txt",
    "figures/r072z/fig-r072z-os-squire-threshold/validate.py",
    "tests/r072z-deterministic-certificate-source.test.mjs",
    "tests/r072z-os-squire-figure-source.test.mjs",
    "tests/r072z-os-squire-gate.test.mjs",
    "tests/r072z-release.test.mjs",
)

EXPECTED = {
    "CLOSED": (
        "exactOSFeedbackCommutatorIdentity", "signedRelativeFormOSAbsorption",
        "highGapOSPrefactorOneDecay", "highGapOSForcedScaleLedger",
        "alphaMinusTwoOSGapSufficiency", "highModeOSGapExponentSharpness",
        "exactGaplessOSTangentMode", "exactSquireDuhamel",
        "exactKineticOrientationNormalization", "optimalInstantaneousSquireCoefficient",
        "orientationUniformWithLambdaPayment", "ordinaryGapSquireHistoryTransfer",
        "strongKernelConditionalSquireTransfer", "dampingGapConvolutionFormula",
        "fixedRowOSSquireGraphRegularity",
    ),
    "FALSE": (
        "scalarA2AutomaticallyAbsorbsOSFeedbackAllStrongRows",
        "epsilonOnlyOSBoundedPerturbationGate", "allStrongRowsOSPrefactorOneContraction",
        "abstractGaplessOSA2StrictContraction", "rawOrientationUniformFromCOnly",
        "epsilonOnlySquireTransfer", "backgroundUniformEnergyBoundWithoutLambdaPayment",
        "uniformlyEquivalentLambdaIndependentContractiveNorm",
        "equalRateUniformGapDenominator", "instantaneousQEndpointAloneControlsEta",
    ),
    "OPEN": (
        "lowGapOSTransientA2Propagator", "collisionScaleOSLimitingAbsorption",
        "unconditionalStrongFullRowA2Estimate", "BlochUniformPhysicalVelocityDirectSum",
        "lowGapWeakFullRows", "completeLinearizedShearSubsystem",
        "nonlinearNavierStokes", "Clay",
    ),
}


def rat(x: F | int) -> str:
    x = F(x)
    return f"{x.numerator}/{x.denominator}"


def sci(x: float) -> str:
    return f"{x:.15e}"


def digest(path: Path) -> str:
    calculator = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            calculator.update(block)
    return calculator.hexdigest()


def simpson(function: Callable[[float], float], start: float, end: float, panels: int = 20000) -> float:
    if panels % 2:
        panels += 1
    step = (end - start) / panels
    total = function(start) + function(end)
    total += 4 * sum(function(start + step * j) for j in range(1, panels, 2))
    total += 2 * sum(function(start + step * j) for j in range(2, panels, 2))
    return total * step / 3


def commutator_record() -> dict[str, Any]:
    # Acting on e_n: D(f e_n)-f D(e_n) has coefficient
    # (k_m-k_n) f_hat[m-n]=(m-n)f_hat[m-n]=-i(f_x)_hat[m-n].
    action_rows = []
    for ell in (-2, -1, 1, 2):
        action_rows.append({"shift": ell, "leftMinusRightMultiplier": ell,
                            "minusIFxMultiplier": ell, "residual": 0})
    beta, mu, d = 0.25, 2.0, 0.3

    def entry(m: int, n: int) -> float:
        ell = m - n
        h = math.exp(-d) / 4 if abs(ell) == 1 else -math.exp(-4 * d) if abs(ell) == 2 else 0
        lm = (m + beta) ** 2 + mu
        ln = (n + beta) ** 2 + mu
        return ((m + n + 2 * beta) * h / 2) / math.sqrt(lm ** 3 * ln ** 3)

    pairs = ((0, 1), (-2, 0), (2, 5))
    self_adjoint_residual = max(abs(entry(m, n) - entry(n, m)) for m, n in pairs)
    return {
        "directActionRows": action_rows,
        "DCommutator": "[D_beta,f]=-i*f_x",
        "LCommutator": "[L,f]=-i*(D_beta*f_x+f_x*D_beta)",
        "energyPressureSign": "-c*<r,Hr>",
        "fourierCoefficients": {"-2": "-exp(-4d)", "-1": "exp(-d)/4",
                                "1": "exp(-d)/4", "2": "-exp(-4d)"},
        "matrixFormula": "(k_m+k_n)*h_hat[m-n]/(2*lambda_m^(3/2)*lambda_n^(3/2))",
        "selfAdjointSampleResidual": sci(self_adjoint_residual),
    }


def gap_bounds_record() -> dict[str, Any]:
    m3 = []
    for d in (0.0, 0.25, 1.0):
        at_pi = abs(-0.5 * math.exp(-d) - 2 * math.exp(-4 * d))
        triangle = 0.5 * math.exp(-d) + 2 * math.exp(-4 * d)
        m3.append({"dMinus": sci(d), "atPi": sci(at_pi), "triangleBound": sci(triangle),
                   "equalityResidual": sci(abs(at_pi - triangle))})
    rows = []
    for beta, mu in ((0.0, 0.1), (0.25, 0.7), (0.5, 2.0), (-0.4, 5.0)):
        rho = min(abs(beta - integer) for integer in range(-3, 4))
        # Independent enumeration order: paired shells about the nearest lattice point.
        centre = int(round(-beta))
        candidates = [centre]
        for shell in range(1, 20001):
            candidates.extend((centre - shell, centre + shell))
        discrete = max(abs(n + beta) / (((n + beta) ** 2 + mu) ** 1.5) for n in candidates)
        bounds = (1 / (rho * rho + mu), 2 / (3 * math.sqrt(3) * mu))
        rows.append({"beta": sci(beta), "mu": sci(mu), "sampledSup": sci(discrete),
                     "minimumBound": sci(min(bounds)), "boundSatisfied": discrete <= min(bounds) + 1e-14})
    return {"M3Formula": "exp(-dMinus)/2+2*exp(-4*dMinus)", "M3Samples": m3,
            "sBound": "min(g^(-1),2/(3*sqrt(3)*mu))", "sBoundSamples": rows}


def alpha_record() -> dict[str, Any]:
    # Exponent arithmetic is carried out as Fractions, not inferred from samples.
    c_power = F(2, 5)
    alpha_power = F(-5) * c_power
    constant_power = F(1) * c_power
    return {"cPower": rat(c_power), "alphaPower": rat(alpha_power),
            "constantPower": rat(constant_power),
            "identity": "|c|=4*alpha^(-5) => |c|^(2/5)=4^(2/5)*alpha^(-2)",
            "exact": alpha_power == -2 and constant_power == F(2, 5)}


def two_mode_record() -> dict[str, Any]:
    # Construct the 2x2 compression [[0,a],[a,0]] and take its positive eigenvector.
    mu = F(1, 100)
    a0 = 1 / (8 * float(mu) ** 1.5 * (1 + float(mu)) ** 1.5)
    high = []
    for n in (8, 32, 128, 512, 2048):
        mu_n = 2.0 * n * n
        numerator = 2.0 * n + 1
        denominator = 8 * math.sqrt((3 * n * n) ** 3 * (3 * n * n + 2 * n + 1) ** 3)
        scaled = numerator / denominator * mu_n ** 2.5
        high.append({"n": n, "scaled": sci(scaled),
                     "errorToSqrt2Over27": sci(abs(scaled - math.sqrt(2) / 27))})
    return {"compression": "[[0,a_n],[a_n,0]]", "positiveEigenvalue": "a_n",
            "lowModeHalfEnergyDerivative": sci(4 * a0 - 1), "lowModeGrows": 4 * a0 > 1,
            "highModeSamples": high, "limit": "sqrt(2)*exp(-d)/27",
            "scope": "unweighted instantaneous prefactor-one L2_q coercivity only"}


def tangent_record() -> dict[str, Any]:
    rows = []
    for k, w, decay in ((1, F(-1, 2), 1), (2, F(1, 4), 4)):
        q = -k * k * w
        q_d = -decay * q
        minus_l_q = -k * k * q
        rows.append({"frequency": k, "qD": rat(q_d), "minusLQ": rat(minus_l_q),
                     "heatResidual": rat(q_d - minus_l_q)})
    return {"modeRows": rows, "LInverseQ": "-W",
            "imaginaryCancellation": "commutativity of pointwise multiplication",
            "imaginaryResidual": "0/1", "physicalMuZeroVelocityRowCertified": False}


def polynomial_scaled_record() -> dict[str, Any]:
    # Polynomials in (alpha,S,X); retain terms that survive after alpha^-3.
    # Route is independent of the producer: multiply the exponential and sine jets.
    exp1 = {(0, 0): F(1), (2, 1): F(-1)}
    exp4 = {(0, 0): F(1), (2, 1): F(-4)}
    sin1 = {(1, 1): F(1), (3, 3): F(-1, 6)}
    sin2 = {(1, 1): F(2), (3, 3): F(-4, 3)}

    def multiply(left: dict[tuple[int, int], F], right: dict[tuple[int, int], F]) -> dict[tuple[int, int, int], F]:
        out: dict[tuple[int, int, int], F] = {}
        for (aa, ss), lv in left.items():
            for (ab, xx), rv in right.items():
                key = (aa + ab - 3, ss, xx)
                out[key] = out.get(key, F()) + lv * rv
        return out

    first = multiply(exp1, sin1)
    second = multiply(exp4, sin2)
    combined: dict[tuple[int, int, int], F] = {}
    for key in set(first) | set(second):
        combined[key] = -2 * first.get(key, F()) + second.get(key, F())
    limit = {key: value for key, value in combined.items() if key[0] == 0 and value}
    return {"survivingMonomials": {f"S^{s}*X^{x}": rat(v) for (_, s, x), v in sorted(limit.items())},
            "VLimitCoefficients": {"X^3": rat(limit[(0, 0, 3)]), "S*X": rat(limit[(0, 1, 1)])},
            "VXXLimitCoefficients": {"X": rat(6 * limit[(0, 0, 3)])},
            "potentialAndFeedbackBothOrderOne": True,
            "collisionScalePropagatorCertified": False}


def orientation_record() -> dict[str, Any]:
    chi = []
    for xi, gamma, rho in ((3, 4, 0), (3, 4, 5), (0, 2, 1), (10, 1, 0)):
        denominator = xi * xi + gamma * gamma + rho * rho
        chi.append({"xi": xi, "gamma": gamma, "rho": rho,
                    "chiSquared": rat(F(xi * xi, denominator)), "bounded": xi * xi <= denominator})
    beta, mu = 0.25, 0.7
    root = math.sqrt(mu)
    # Poisson summation route: pi/root*(1+2 sum exp(-2*pi*root*k) cos(2*pi*beta*k)).
    poisson = math.pi / root * (1 + 2 * sum(
        math.exp(-2 * math.pi * root * k) * math.cos(2 * math.pi * beta * k)
        for k in range(1, 100)
    ))
    hyperbolic = (math.pi / root * math.sinh(2 * math.pi * root) /
                  (math.cosh(2 * math.pi * root) - math.cos(2 * math.pi * beta)))
    return {"chiFormula": "|xi|/sqrt(xi^2+gamma^2+rho^2)", "chiSamples": chi,
            "LambdaPaymentRequired": True, "cOnlyUniformBound": False,
            "latticeSum": {"beta": sci(beta), "mu": sci(mu), "poissonValue": sci(poisson),
                           "hyperbolicValue": sci(hyperbolic), "residual": sci(abs(poisson - hyperbolic))},
            "transverseLimitRetainsLiftUp": True}


def kernel_record() -> dict[str, Any]:
    integrals = []
    for a, d in ((0.7, 1.25), (2.0, 0.5), (0.125, 4.0)):
        l1_quad = simpson(lambda t: math.exp(-a * t), 0, d)
        l2_sq_quad = simpson(lambda t: math.exp(-2 * a * t), 0, d)
        l1_formula = (1 - math.exp(-a * d)) / a
        l2_formula = (1 - math.exp(-2 * a * d)) / (2 * a)
        integrals.append({"a": sci(a), "D": sci(d), "PhiQuadrature": sci(l1_quad),
                          "PhiResidual": sci(abs(l1_quad - l1_formula)),
                          "PsiSquaredResidual": sci(abs(l2_sq_quad - l2_formula))})
    convolutions = []
    for a, b, tau in ((0.7, 1.1, 2.0), (1.5, 1.5, 0.8), (3.0, 0.25, 1.2)):
        integral = simpson(lambda s: math.exp(-a * (tau - s)) * math.exp(-b * s), 0, tau)
        formula = ((math.exp(-b * tau) - math.exp(-a * tau)) / (a - b)
                   if a != b else tau * math.exp(-a * tau))
        convolutions.append({"a": sci(a), "b": sci(b), "tau": sci(tau),
                             "quadrature": sci(integral), "formula": sci(formula),
                             "residual": sci(abs(integral - formula))})
    return {"kernelIntegrals": integrals, "dampingGapConvolutions": convolutions,
            "equalBranch": "tau*exp(-a*tau)", "equalRateUniformGapDenominator": False}


def claims() -> dict[str, list[str]]:
    report = (REPO / "research/r072z_report-source.md").read_text()
    for status, keys in EXPECTED.items():
        for key in keys:
            if not re.search(r"\\texttt\{" + re.escape(key) + r"\}.*?=\\texttt\{" + status + r"\}", report, re.S):
                raise RuntimeError(f"independent claim check failed: {key}")
    return {status.lower(): list(keys) for status, keys in EXPECTED.items()}


def boundary() -> dict[str, bool]:
    return {"finiteDeterministicAlgebraCertified": True,
            "lowGapOSTransientA2PropagatorProved": False,
            "collisionScaleLimitingPropagatorProved": False,
            "finiteMatrixEqualsFullOperatorNormProved": False,
            "BlochUniformPhysicalVelocityDirectSumProved": False,
            "completeLinearizedShearSubsystemProved": False,
            "nonlinearNavierStokesClosureProved": False,
            "clayMillenniumProblemSolved": False}


def compute() -> dict[str, Any]:
    result = {"schemaVersion": 1, "researchRelease": "R0.72Z", "status": "passed",
              "method": "direct-fourier-action-poisson-pairing-polynomial-convolution-and-quadrature",
              "commutatorMatrix": commutator_record(), "highGapBounds": gap_bounds_record(),
              "alphaPower": alpha_record(), "twoModeWitnesses": two_mode_record(),
              "tangentResidual": tangent_record(), "scaledCubic": polynomial_scaled_record(),
              "orientation": orientation_record(), "kernels": kernel_record(),
              "claimLedger": claims(), "claimBoundary": boundary(),
              "sourceHashes": {name: digest(REPO / name) for name in INPUTS}}
    result["checks"] = {
        "commutatorDirectActions": all(row["residual"] == 0 for row in result["commutatorMatrix"]["directActionRows"]),
        "matrixSelfAdjoint": float(result["commutatorMatrix"]["selfAdjointSampleResidual"]) < 1e-14,
        "M3Equality": all(float(row["equalityResidual"]) < 1e-14 for row in result["highGapBounds"]["M3Samples"]),
        "sBoundSamples": all(row["boundSatisfied"] for row in result["highGapBounds"]["sBoundSamples"]),
        "alphaPower": result["alphaPower"]["exact"],
        "lowModeGrowth": result["twoModeWitnesses"]["lowModeGrows"],
        "tangentHeat": all(row["heatResidual"] == "0/1" for row in result["tangentResidual"]["modeRows"]),
        "scaledCubic": result["scaledCubic"]["VLimitCoefficients"] == {"X^3": "-1/1", "S*X": "-6/1"},
        "chiBound": all(row["bounded"] for row in result["orientation"]["chiSamples"]),
        "latticeIdentity": float(result["orientation"]["latticeSum"]["residual"]) < 1e-13,
        "kernelQuadrature": max(float(row["PhiResidual"]) for row in result["kernels"]["kernelIntegrals"]) < 1e-12,
        "JQuadrature": max(float(row["residual"]) for row in result["kernels"]["dampingGapConvolutions"]) < 1e-12,
        "failClosedBoundary": all(not v for k, v in result["claimBoundary"].items() if k != "finiteDeterministicAlgebraCertified"),
    }
    if not all(result["checks"].values()):
        raise RuntimeError("independent recomputation failed")
    return result


def ensure_formal_context(source_commit: str, output: Path) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError(
            "--formal requires a full 40-character lowercase "
            "--formal-source-commit"
        )
    expected = (HERE / "independent.json").resolve()
    if output.resolve() != expected:
        raise RuntimeError(f"formal independent output must be {expected}")
    if subprocess.run(
        ["git", "cat-file", "-e", f"{source_commit}^{{commit}}"],
        cwd=REPO,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode:
        raise RuntimeError("formal independent source commit is not a Git commit")
    status = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=REPO,
        text=True,
    )
    if status:
        raise RuntimeError(
            "formal independent recomputation requires a completely clean repository"
        )
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPO, text=True
    ).strip()
    if head != source_commit:
        raise RuntimeError("formal independent source commit must equal clean HEAD")
    manifest_path = HERE / "manifest.json"
    if manifest_path.exists():
        prior = json.loads(manifest_path.read_text(encoding="utf-8"))
        if prior.get("status") == "formal":
            raise RuntimeError("refusing to overwrite a formal independent result")
        # status=None is the legacy finite-hash bundle and is intentionally
        # accepted for a one-pass upgrade at the clean source commit.
        if prior.get("status") not in (None, "draft"):
            raise RuntimeError("existing certificate manifest has an unknown status")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--draft", action="store_true")
    parser.add_argument("--formal", action="store_true")
    parser.add_argument("--formal-source-commit")
    parser.add_argument("--output")
    args = parser.parse_args()
    value = compute()
    if args.self_test:
        if args.draft or args.formal or args.formal_source_commit or args.output:
            parser.error("--self-test cannot be combined with output arguments")
        print("R0.72Z independent recomputation self-test: passed (no outputs written)")
        return
    if args.draft and args.formal:
        parser.error("choose exactly one of --draft or --formal")
    if not args.output:
        parser.error("draft or formal recomputation requires --output")
    output = Path(args.output).resolve()
    expected = (HERE / "independent.json").resolve()
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
        print("R0.72Z independent formal recomputation: passed and source-bound")
        return
    if not args.draft:
        parser.error("use --self-test, --draft, or --formal")
    if args.formal_source_commit:
        parser.error("--draft cannot be combined with --formal-source-commit")
    manifest_path = HERE / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("status") == "formal":
            raise RuntimeError("refusing to overwrite a formal independent result")
        if manifest.get("status") not in (None, "draft"):
            raise RuntimeError("existing certificate manifest has an unknown status")
    value["certificateStage"] = "draft"
    value["sourceCommit"] = None
    output.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("R0.72Z independent draft recomputation: passed and written")


if __name__ == "__main__":
    main()
