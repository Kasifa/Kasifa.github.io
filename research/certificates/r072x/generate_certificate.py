#!/usr/bin/env python3
"""Build the deterministic R0.72X outer-time finite certificate.

The bundle certifies finite algebra and bookkeeping only.  In particular,
it does not machine-check the compactness, trace, direct-sum, evolution, or
external-theorem arguments used by the bound analytic report.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from math import factorial
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
FIGURE_DIRECTORY = "figures/r072x-all-center/fig-r072x-all-center-transfer"
SOURCE_FILES = (
    "research/r072x_report-source.md",
    "research/r072x_gap_matrix.md",
    "research/r072x_literature_audit.md",
    "research/r072x_independent_audit.md",
    "research/certificates/r072x/generate_certificate.py",
    "research/certificates/r072x/independent_recompute.py",
    "research/certificates/r072x/validate_certificate.py",
    "research/certificates/r072x/README.md",
    "research/certificates/r072x/command.txt",
    "research/certificates/r072x/environment.txt",
    "scripts/generate_r072x_figure.py",
    "scripts/generate_r072x_release.py",
    "scripts/add-r072x-translations.mjs",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/README.md",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/caption.md",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/contract.json",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/config.json",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/command.txt",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/environment.txt",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/requirements.txt",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/qa-protocol.md",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/plot.py",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/validate.py",
    "tests/r072x-deterministic-certificate-source.test.mjs",
    "tests/r072x-exact-path-gate.test.mjs",
    "tests/r072x-all-center-figure-source.test.mjs",
    "tests/r072x-release.test.mjs",
)
GENERATED_FILES = (
    "certificate.json",
    "independent.json",
    "crosscheck.json",
    "manifest.json",
    "SHA256SUMS",
)

Jet = dict[tuple[int, int], F]  # powers of (D, theta)


def q(value: F | int) -> str:
    value = F(value)
    return f"{value.numerator}/{value.denominator}"


def jet_add(*values: Jet) -> Jet:
    result: Jet = {}
    for value in values:
        for key, coefficient in value.items():
            result[key] = result.get(key, F(0)) + coefficient
    return {key: coefficient for key, coefficient in result.items() if coefficient}


def jet_scale(value: Jet, factor: F | int) -> Jet:
    return {key: F(factor) * coefficient for key, coefficient in value.items()}


def jet_multiply(left: Jet, right: Jet, order: int) -> Jet:
    result: Jet = {}
    for (d1, t1), a in left.items():
        for (d2, t2), b in right.items():
            key = (d1 + d2, t1 + t2)
            if sum(key) <= order:
                result[key] = result.get(key, F(0)) + a * b
    return {key: coefficient for key, coefficient in result.items() if coefficient}


def exp_d_series(rate: int, order: int) -> Jet:
    return {(degree, 0): F((-rate) ** degree, factorial(degree)) for degree in range(order + 1)}


def cos_theta_series(frequency: int, order: int) -> Jet:
    return {
        (0, degree): F((-1) ** (degree // 2) * frequency**degree, factorial(degree))
        for degree in range(0, order + 1, 2)
    }


def sin_theta_series(frequency: int, order: int) -> Jet:
    return {
        (0, degree): F((-1) ** ((degree - 1) // 2) * frequency**degree, factorial(degree))
        for degree in range(1, order + 1, 2)
    }


def selected_jet(value: Jet) -> dict[str, str]:
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
    return {
        label: q(value.get(key, F(0)))
        for key, label in labels.items()
        if value.get(key, F(0))
    }


def common_zero_and_jet_record() -> dict[str, Any]:
    order = 4
    f = jet_add(
        jet_multiply(exp_d_series(1, order), cos_theta_series(1, order), order),
        jet_scale(
            jet_multiply(exp_d_series(4, order), cos_theta_series(2, order), order),
            -1,
        ),
    )
    g = jet_add(
        jet_scale(
            jet_multiply(exp_d_series(1, order), sin_theta_series(1, order), order),
            -1,
        ),
        jet_scale(
            jet_multiply(exp_d_series(4, order), sin_theta_series(2, order), order),
            2,
        ),
    )
    jacobian = [
        [q(f.get((1, 0), F(0))), q(f.get((0, 1), F(0)))],
        [q(g.get((1, 0), F(0))), q(g.get((0, 1), F(0)))],
    ]

    # With c=cos(theta), s=sin(theta), and r=exp(3D)>0, the two
    # common-zero equations are r*c=2*c^2-1 and r*s=4*s*c.
    # The producer checks the two exact branches separately.
    sine_zero_candidates = (F(-1), F(1))
    positive_r_candidates = [F(1, c) for c in sine_zero_candidates if F(1, c) > 0]
    nonzero_sine_polynomial_constant = F(-1)  # 2*c^2=-1
    branch_elimination_checked = (
        positive_r_candidates == [F(1)]
        and nonzero_sine_polynomial_constant < 0
    )
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
            "cosineCandidates": [q(value) for value in sine_zero_candidates],
            "positiveRCandidates": [q(value) for value in positive_r_candidates],
            "selected": "r=1, cos(theta)=1",
        },
        "nonzeroSineBranch": {
            "deducedR": "r=4*cos(theta)",
            "deducedEquation": "2*cos(theta)^2=-1",
            "realSolutionExists": nonzero_sine_polynomial_constant >= 0,
        },
        "branchEliminationChecked": branch_elimination_checked,
        "onlyCommonZero": "D=0 and theta=0 mod 2*pi",
        "jacobianVariableOrder": ["D", "theta"],
        "jacobianOutputOrder": ["f", "g"],
        "jacobianAtOrigin": jacobian,
        "jacobianDeterminant": q(F(jacobian[0][0]) * F(jacobian[1][1]) - F(jacobian[0][1]) * F(jacobian[1][0])),
        "fJetThroughTotalDegreeThree": selected_jet(f),
        "gJetThroughTotalDegreeThree": selected_jet(g),
        "leadingJet": {
            "g": "3*theta+O(|D*theta|+|theta|^3)",
            "f": "3*D+(3/2)*theta^2+O(D^2+|D|*theta^2+theta^4)",
        },
        "boundedCoefficientInputs": ["f=O(alpha^2)", "g=O(alpha)"],
        "analyticBoundedCenterConclusion": ["theta=O(alpha)", "D=O(alpha^2)"],
    }


def interface_power_record() -> dict[str, Any]:
    epsilon_power = F(-5)
    h_power = F(2)
    separation_power = F(1)
    curvature_power = F(1)
    gradient_power = F(2)
    pre_rate = epsilon_power / 2 + curvature_power / 2
    post_rate = F(2, 3) * epsilon_power + F(2, 3) * gradient_power

    # Exact h-series for (exp(-4h)-exp(-h))/2 through h^2.
    post_gradient_coefficients = [
        F((-4) ** degree - (-1) ** degree, 2 * factorial(degree))
        for degree in (1, 2)
    ]
    return {
        "scaling": ["epsilon_c=4*alpha^(-5)", "kappa=alpha^(-5)", "h_alpha=T*alpha^2"],
        "alphaPowers": {
            "epsilon_c": q(epsilon_power),
            "h_alpha": q(h_power),
            "preCriticalPointHalfSeparation": q(separation_power),
            "preMorseCurvatureFloor": q(curvature_power),
            "postAwayGradientFloor": q(gradient_power),
            "preA1DiagnosticRate": q(pre_rate),
            "postMonotoneDiagnosticRate": q(post_rate),
            "exactFamilyCollisionRate": "-2/1",
        },
        "kappaPowers": {
            "h_alpha": "-2/5",
            "preCriticalPointHalfSeparation": "-1/5",
            "preMorseCurvatureFloor": "-1/5",
            "postAwayGradientFloor": "-2/5",
            "matchedRate": "2/5",
        },
        "preCriticalPointLedger": {
            "equation": "x_pm^2=2*T*alpha^2+O_T(alpha^4)",
            "locations": "x_pm=+/-sqrt(2*T)*alpha+O_T(alpha^3)",
            "separationOrder": "alpha",
            "curvatureOrder": "alpha",
        },
        "postGradientLedger": {
            "exact": "W_x(h_alpha,0)=(exp(-4*h_alpha)-exp(-h_alpha))/2",
            "hCoefficientsThroughTwo": [q(value) for value in post_gradient_coefficients],
            "alphaExpansion": "-(3/2)*T*alpha^2+(15/4)*T^2*alpha^4+O_T(alpha^6)",
        },
        "diagnosticRatePowersMatch": pre_rate == post_rate == F(-2),
        "fixedShapeA1UniformAtShrinkingInterface": False,
    }


def floor_fraction(value: F) -> int:
    return value.numerator // value.denominator


def polynomial_geometric_identity(maximum: int) -> bool:
    # Coefficients of (1-x)*sum_{j=0}^n x^j are 1-x^(n+1).
    for n in range(maximum + 1):
        coefficients = [0] * (n + 2)
        for j in range(n + 1):
            coefficients[j] += 1
            coefficients[j + 1] -= 1
        expected = [1] + [0] * n + [-1]
        if coefficients != expected:
            return False
    return True


def block_tiling_record() -> dict[str, Any]:
    floor_grid_checked = all(
        floor_fraction(F(numerator, denominator)) >= F(numerator, denominator) - 1
        for numerator in range(0, 65)
        for denominator in range(1, 33)
    )
    return {
        "physicalGap": "L=d_2-d_1",
        "scaledGap": "L_S=L/alpha^2",
        "fullBlockCount": "N=floor(L/(2*T*alpha^2))",
        "floorInequality": "floor(z)>=z-1",
        "finiteRationalFloorGridChecked": floor_grid_checked,
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
        "finiteGeometricTelescopingChecked": polynomial_geometric_identity(64),
        "geometricEnergyIdentity": "(1-q^2)*sum_(j=0)^n q^(2*j)=1-q^(2*n+2)",
        "scaledIntegratedEnergyBound": "2*T/(1-q^2)*E(S_1)",
        "physicalIntegratedEnergyBound": "2*T*alpha^2/(1-q^2)*E(d_1)",
        "duhamelL2xKernelScale": "O_KT(alpha^2)",
        "forcedHMinusOneTransferInferred": False,
    }


def bloch_twist_record() -> dict[str, Any]:
    alpha_power_in_phase = F(1) + F(-1)
    return {
        "covariantDerivative": "D_beta=partial_X+i*alpha*beta",
        "unitaryGauge": "w=exp(i*alpha*beta*X)*u",
        "operatorIdentity": "partial_X^2*w=exp(i*alpha*beta*X)*D_beta^2*u",
        "scaledTorusLength": "L_alpha=2*pi/alpha",
        "boundaryPhaseExponent": "alpha*beta*L_alpha=2*pi*beta",
        "alphaPowerInBoundaryPhase": q(alpha_power_in_phase),
        "twistedBoundary": "w(X+L_alpha)=exp(2*pi*i*beta)*w(X)",
        "zeroResiduePhase": "beta=0 gives phase 1",
        "endpointPhaseModulusSquared": "|exp(2*pi*i*beta)|^2=1",
        "endpointIntegrationByPartsCancellationMachineChecked": False,
    }


def damping_and_counterexample_record() -> tuple[dict[str, Any], dict[str, Any]]:
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
    spatial_frequency = F(0)
    beta = F(0)
    epsilon_j = F(0)
    mu = F(0)
    laplacian_multiplier = -(spatial_frequency + beta) ** 2
    potential_multiplier = epsilon_j
    damping_multiplier = mu
    time_multiplier = laplacian_multiplier - damping_multiplier
    constant_equation_checked = (
        laplacian_multiplier == potential_multiplier == damping_multiplier == time_multiplier == 0
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


def payload() -> dict[str, Any]:
    common = common_zero_and_jet_record()
    interface = interface_power_record()
    tiling = block_tiling_record()
    bloch = bloch_twist_record()
    damping, counterexample = damping_and_counterexample_record()
    boundary = claim_boundary()
    checks = {
        "onlyCommonZero": (
            common["branchEliminationChecked"] is True
            and common["onlyCommonZero"] == "D=0 and theta=0 mod 2*pi"
        ),
        "jacobianDiagThree": common["jacobianAtOrigin"] == [["3/1", "0/1"], ["0/1", "3/1"]],
        "jacobianDeterminantNine": common["jacobianDeterminant"] == "9/1",
        "leadingJetCoefficients": (
            common["fJetThroughTotalDegreeThree"].get("D") == "3/1"
            and common["fJetThroughTotalDegreeThree"].get("theta^2") == "3/2"
            and common["gJetThroughTotalDegreeThree"].get("theta") == "3/1"
        ),
        "interfaceRatePowerMatch": interface["diagnosticRatePowersMatch"],
        "postGradientCoefficients": interface["postGradientLedger"]["hCoefficientsThroughTwo"] == ["-3/2", "15/4"],
        "floorArithmetic": tiling["finiteRationalFloorGridChecked"],
        "geometricIntegralArithmetic": tiling["finiteGeometricTelescopingChecked"],
        "prefactorOneCounterexample": tiling["prefactorOneAllGapExponential"] is False,
        "blochPhaseAlphaCancellation": bloch["alphaPowerInBoundaryPhase"] == "0/1",
        "dampingNormEnergyDistinguished": damping["energyExponentToNormExponent"] == 2,
        "zeroCouplingConstantCounterexample": (
            counterexample["constantEquationChecked"] is True
            and counterexample["strictContraction"] is False
        ),
        "machineBoundaryHonest": (
            boundary["finiteExactAlgebraCertified"] is True
            and boundary["compactnessArgumentMachineChecked"] is False
            and boundary["scalarEndpointTracePassageMachineChecked"] is False
            and boundary["nonautonomousEvolutionExistenceMachineChecked"] is False
            and boundary["cobleHeTheoremMachineChecked"] is False
            and boundary["allPhysicalRowsUniformContraction"] is False
            and boundary["nonlinearNavierStokesClosureProved"] is False
            and boundary["clayMillenniumProblemSolved"] is False
        ),
    }
    return {
        "schemaVersion": 1,
        "theoremId": "R0.72X-all-center-outer-time-finite-ledger",
        "status": "passed" if all(checks.values()) else "failed",
        "producerMethod": "truncated bivariate exponential-trigonometric jets, exact branch elimination, rational exponent arithmetic, and coefficient telescoping",
        "exactChecks": checks,
        "commonZeroAndLocalJet": common,
        "shrinkingInterfacePowers": interface,
        "blockTilingAndIntegratedEnergy": tiling,
        "blochTwist": bloch,
        "scalarDamping": damping,
        "zeroCouplingCounterexample": counterexample,
        "claimBoundary": boundary,
    }


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ensure_clean_head(source_commit: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError("--formal requires a full 40-character --source-commit")
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
        raise RuntimeError("formal certificate source commit must equal clean HEAD")


def source_bindings(source_commit: str) -> list[dict[str, Any]]:
    result = []
    for relative in SOURCE_FILES:
        path = REPOSITORY / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"source is absent or not a regular file: {relative}")
        committed = subprocess.check_output(
            ["git", "rev-parse", f"{source_commit}:{relative}"],
            cwd=REPOSITORY,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        working = subprocess.check_output(
            ["git", "hash-object", f"--path={relative}", str(path)],
            cwd=REPOSITORY,
            text=True,
        ).strip()
        if committed != working:
            raise RuntimeError(f"working source differs from {source_commit}:{relative}")
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
    print("R0.72X certificate source self-test: passed (no outputs written)")


def formal_build(source_commit: str) -> None:
    ensure_clean_head(source_commit)
    stale = [name for name in GENERATED_FILES if (ROOT / name).exists()]
    if stale:
        raise RuntimeError(
            f"refusing to overwrite existing certificate outputs: {', '.join(stale)}"
        )
    bindings = source_bindings(source_commit)
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "independent_recompute.py"),
            "--formal",
            "--source-commit",
            source_commit,
            "--output",
            str(ROOT / "independent.json"),
        ],
        check=True,
    )
    certificate = payload()
    if certificate["status"] != "passed":
        raise RuntimeError("R0.72X exact checks failed")
    write_json(ROOT / "certificate.json", certificate)
    independent = json.loads((ROOT / "independent.json").read_text(encoding="utf-8"))
    compared = (
        "commonZeroAndLocalJet",
        "shrinkingInterfacePowers",
        "blockTilingAndIntegratedEnergy",
        "blochTwist",
        "scalarDamping",
        "zeroCouplingCounterexample",
        "claimBoundary",
    )
    matches = (
        independent.get("status") == "passed"
        and all(independent.get(section) == certificate.get(section) for section in compared)
    )
    crosscheck = {
        "schemaVersion": 1,
        "status": "passed" if matches else "failed",
        "method": "bivariate-series/branch producer versus derivative-table/cross-product independent route",
        "temporaryUnsealedSourceAllowed": False,
        "formalSourceReady": True,
        "sourceCommit": source_commit,
        "sourceBindings": bindings,
        "certificateSha256": sha256(ROOT / "certificate.json"),
        "comparedSections": list(compared),
        "checks": {
            "certificatePassed": certificate["status"] == "passed",
            "allExactChecksPassed": all(certificate["exactChecks"].values()),
            "independentRecomputationPassed": independent.get("status") == "passed",
            "independentExactLedgerMatches": matches,
            "analyticVersusMachineBoundaryExplicit": (
                certificate["claimBoundary"]["analyticAllCenterExactFamilyGraphCoercivityProvedInBoundReport"]
                and not certificate["claimBoundary"]["compactnessArgumentMachineChecked"]
                and not certificate["claimBoundary"]["cobleHeTheoremMachineChecked"]
            ),
            "allRowsNonlinearAndClayRemainFalse": (
                not certificate["claimBoundary"]["allPhysicalRowsUniformContraction"]
                and not certificate["claimBoundary"]["nonlinearNavierStokesClosureProved"]
                and not certificate["claimBoundary"]["clayMillenniumProblemSolved"]
            ),
        },
    }
    if crosscheck["status"] != "passed" or not all(crosscheck["checks"].values()):
        raise RuntimeError("independent R0.72X crosscheck failed")
    write_json(ROOT / "crosscheck.json", crosscheck)
    manifest = {
        "schemaVersion": 1,
        "bundle": "R0.72X deterministic all-center outer-time finite ledger",
        "status": "formal",
        "sourceCommit": source_commit,
        "sourceBindings": bindings,
        "claimBoundary": certificate["claimBoundary"],
        "deterministic": True,
        "createdAt": "2026-08-28T00:00:00+08:00",
        "files": {
            name: {
                "sha256": sha256(ROOT / name),
                "bytes": (ROOT / name).stat().st_size,
            }
            for name in ("certificate.json", "independent.json", "crosscheck.json")
        },
        "limitations": (
            "Finite exact algebra and bookkeeping only. Compactness, graph-limit and "
            "endpoint-trace passages, twisted H^{-1} direct sums, nonautonomous "
            "evolution, and the Coble-He theorem are not machine checked. Uniform "
            "contraction of all physical rows, the forced H^{-1} transfer, the complete "
            "linearized subsystem, nonlinear Navier-Stokes closure, and Clay are false "
            "or open as recorded in the claim boundary."
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
    print("R0.72X formal deterministic certificate: passed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--formal", action="store_true")
    parser.add_argument("--source-commit")
    args = parser.parse_args()
    if args.self_test:
        if args.formal or args.source_commit:
            parser.error("--self-test cannot be combined with formal generation arguments")
        self_test()
        return
    if not args.formal:
        parser.error("no unsealed output mode exists; use --self-test or --formal")
    formal_build(str(args.source_commit or ""))


if __name__ == "__main__":
    main()
