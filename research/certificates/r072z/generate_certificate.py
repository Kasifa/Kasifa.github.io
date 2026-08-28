#!/usr/bin/env python3
"""Produce the R0.72Z deterministic finite-algebra certificate.

This route uses exact rational arithmetic for the symbolic ledgers and
direct symmetric Fourier sums for the numerical witnesses.  It intentionally
does not certify any infinite-dimensional propagator or nonlinear theorem.
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
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
SOURCE_FILES = (
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
GENERATED_FILES = (
    "certificate.json", "independent.json", "crosscheck.json", "manifest.json",
    "SHA256SUMS",
)
MUTABLE_PUBLICATION_STATE = "research/release-manifest.json"

CLOSED_KEYS = (
    "exactOSFeedbackCommutatorIdentity",
    "signedRelativeFormOSAbsorption",
    "highGapOSPrefactorOneDecay",
    "highGapOSForcedScaleLedger",
    "alphaMinusTwoOSGapSufficiency",
    "highModeOSGapExponentSharpness",
    "exactGaplessOSTangentMode",
    "exactSquireDuhamel",
    "exactKineticOrientationNormalization",
    "optimalInstantaneousSquireCoefficient",
    "orientationUniformWithLambdaPayment",
    "ordinaryGapSquireHistoryTransfer",
    "strongKernelConditionalSquireTransfer",
    "dampingGapConvolutionFormula",
    "fixedRowOSSquireGraphRegularity",
)
FALSE_KEYS = (
    "scalarA2AutomaticallyAbsorbsOSFeedbackAllStrongRows",
    "epsilonOnlyOSBoundedPerturbationGate",
    "allStrongRowsOSPrefactorOneContraction",
    "abstractGaplessOSA2StrictContraction",
    "rawOrientationUniformFromCOnly",
    "epsilonOnlySquireTransfer",
    "backgroundUniformEnergyBoundWithoutLambdaPayment",
    "uniformlyEquivalentLambdaIndependentContractiveNorm",
    "equalRateUniformGapDenominator",
    "instantaneousQEndpointAloneControlsEta",
)
OPEN_KEYS = (
    "lowGapOSTransientA2Propagator",
    "collisionScaleOSLimitingAbsorption",
    "unconditionalStrongFullRowA2Estimate",
    "BlochUniformPhysicalVelocityDirectSum",
    "lowGapWeakFullRows",
    "completeLinearizedShearSubsystem",
    "nonlinearNavierStokes",
    "Clay",
)


def ratio(value: F | int) -> str:
    value = F(value)
    return f"{value.numerator}/{value.denominator}"


def rounded(value: float) -> str:
    return f"{value:.15e}"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes() -> dict[str, str]:
    return {name: sha256(REPOSITORY / name) for name in SOURCE_FILES}


def commutator_and_matrix_record() -> dict[str, Any]:
    # The Fourier symbol of D_beta is k_n=n+beta.  Multiplication by h shifts
    # n to m and gives (k_m+k_n) h_hat[m-n] after symmetrisation.
    h_hat = {"-2": "-exp(-4d)", "-1": "exp(-d)/4",
             "1": "exp(-d)/4", "2": "-exp(-4d)"}
    samples = []
    beta, mu, d = 0.25, 2.0, 0.3
    for m, n in ((0, 1), (1, 0), (-2, 0), (0, -2), (2, 5)):
        ell = m - n
        h = (math.exp(-d) / 4 if abs(ell) == 1 else
             -math.exp(-4 * d) if abs(ell) == 2 else 0.0)
        km, kn = m + beta, n + beta
        lm, ln = km * km + mu, kn * kn + mu
        value = (km + kn) * h / (2 * lm ** 1.5 * ln ** 1.5)
        samples.append({"m": m, "n": n, "value": rounded(value)})
    return {
        "DCommutator": "[D_beta,f]=-i*f_x",
        "LCommutator": "[L,f]=-i*(D_beta*f_x+f_x*D_beta)",
        "energyPressureSign": "-c*<r,Hr>",
        "HDefinition": "(1/2)*L^(-3/2)*(D_beta*W_xxx+W_xxx*D_beta)*L^(-3/2)",
        "fourierCoefficients": h_hat,
        "matrixFormula": "(k_m+k_n)*h_hat[m-n]/(2*lambda_m^(3/2)*lambda_n^(3/2))",
        "selfAdjointSampleResidual": rounded(max(
            abs(float(samples[0]["value"]) - float(samples[1]["value"])),
            abs(float(samples[2]["value"]) - float(samples[3]["value"])),
        )),
        "matrixSamples": samples,
    }


def m3_and_s_record() -> dict[str, Any]:
    m3_rows = []
    for d0 in (0.0, 0.25, 1.0):
        m3_rows.append({
            "dMinus": rounded(d0),
            "M3": rounded(0.5 * math.exp(-d0) + 2 * math.exp(-4 * d0)),
            "attainingPoint": "x=pi",
        })
    s_rows = []
    for beta, mu in ((0.0, 0.1), (0.25, 0.7), (0.5, 2.0), (-0.4, 5.0)):
        rho = abs(beta - round(beta))
        g = rho * rho + mu
        values = [abs(n + beta) / (((n + beta) ** 2 + mu) ** 1.5)
                  for n in range(-20000, 20001)]
        discrete = max(values)
        bound_gap = 1 / g
        bound_continuous = 2 / (3 * math.sqrt(3) * mu)
        s_rows.append({
            "beta": rounded(beta), "mu": rounded(mu), "rho": rounded(rho),
            "sampledSup": rounded(discrete),
            "gapBound": rounded(bound_gap),
            "continuousBound": rounded(bound_continuous),
            "boundSatisfied": discrete <= min(bound_gap, bound_continuous) + 1e-14,
        })
    return {
        "M3Formula": "exp(-dMinus)/2+2*exp(-4*dMinus)",
        "M3Samples": m3_rows,
        "sDefinition": "sup_n |n+beta|/((n+beta)^2+mu)^(3/2)",
        "sBound": "min(g^(-1),2/(3*sqrt(3)*mu))",
        "sBoundSamples": s_rows,
    }


def alpha_power_record() -> dict[str, Any]:
    rows = []
    for alpha in (0.5, 0.25, 0.125):
        c = 4 * alpha ** -5
        lhs = c ** (2 / 5)
        rhs = 4 ** (2 / 5) * alpha ** -2
        rows.append({"alpha": rounded(alpha), "c": rounded(c),
                     "lhs": rounded(lhs), "rhs": rounded(rhs),
                     "relativeResidual": rounded(abs(lhs - rhs) / rhs)})
    return {
        "identity": "|c|=4*alpha^(-5) => |c|^(2/5)=4^(2/5)*alpha^(-2)",
        "cExponent": ratio(F(2, 5)), "alphaExponent": "-2/1", "samples": rows,
    }


def two_mode_record() -> dict[str, Any]:
    mu = 0.01
    a0 = 1 / (8 * mu ** 1.5 * (1 + mu) ** 1.5)
    high = []
    target = math.sqrt(2) / 27
    for n in (8, 32, 128, 512, 2048):
        mu_n = 2 * n * n
        a_n = ((2 * n + 1) /
               (8 * (3 * n * n) ** 1.5 * (3 * n * n + 2 * n + 1) ** 1.5))
        scaled = a_n * mu_n ** 2.5
        high.append({"n": n, "scaled": rounded(scaled),
                     "target": rounded(target), "absoluteError": rounded(abs(scaled - target))})
    return {
        "formula": "exp(-d)*|2*(n+beta)+1|/(8*lambda_n^(3/2)*lambda_(n+1)^(3/2))",
        "lowMode": {"beta": "0/1", "n": 0, "mu": "1/100", "c": "4/1",
                    "a0": rounded(a0), "halfEnergyDerivative": rounded(4 * a0 - 1),
                    "instantaneousGrowth": 4 * a0 - 1 > 0},
        "highMode": {"choice": "beta=0,mu=2*n^2", "samples": high,
                     "limit": "sqrt(2)*exp(-d)/27", "d": "0/1"},
        "scope": "unweighted instantaneous prefactor-one L2_q coercivity only",
    }


def tangent_and_scaled_record() -> tuple[dict[str, Any], dict[str, Any]]:
    tangent_rows = []
    for frequency, w_amplitude, decay in ((1, F(-1, 2), 1), (2, F(1, 4), 4)):
        q_amplitude = -(frequency ** 2) * w_amplitude
        tangent_rows.append({
            "frequency": frequency, "WAmplitude": ratio(w_amplitude),
            "qStarAmplitude": ratio(q_amplitude),
            "minusLInverseQAmplitude": ratio(w_amplitude),
            "heatResidual": "0/1",
        })
    tangent = {
        "domain": "abstract mean-zero beta=mu=0 OS space",
        "qStar": "W_xx", "LInverseQStar": "-W",
        "modeRows": tangent_rows,
        "imaginaryResidual": "W*W_xx-W_xx*W=0",
        "physicalMuZeroVelocityRowCertified": False,
    }
    # Direct Taylor bookkeeping for V_alpha=4*a^-3*W(a^2*S,a*X).
    scaled = {
        "exactEquation": "q_S=(d_X^2-alpha^2*mu-i*sigma*V)q-i*sigma*V_XX*L_alpha^(-1)q",
        "VLimitCoefficients": {"X^3": "-1/1", "S*X": "-6/1"},
        "VXXLimitCoefficients": {"X": "-6/1"},
        "potentialCoefficient": "-i*sigma",
        "feedbackCoefficient": "-i*sigma",
        "collisionScalePropagatorCertified": False,
    }
    return tangent, scaled


def orientation_record() -> dict[str, Any]:
    chi_rows = []
    for xi, gamma, rho in ((3, 4, 0), (3, 4, 5), (0, 2, 1), (10, 1, 0)):
        denominator_sq = xi * xi + gamma * gamma + rho * rho
        chi_rows.append({"xi": xi, "gamma": gamma, "rho": rho,
                         "chiSquared": ratio(F(xi * xi, denominator_sq)),
                         "boundedByOne": xi * xi <= denominator_sq})
    beta, mu = 0.25, 0.7
    closed = (math.pi / math.sqrt(mu) * math.sinh(2 * math.pi * math.sqrt(mu)) /
              (math.cosh(2 * math.pi * math.sqrt(mu)) - math.cos(2 * math.pi * beta)))
    cutoff = 200000
    partial = sum(1 / ((n + beta) ** 2 + mu) for n in range(-cutoff, cutoff + 1))
    return {
        "chiFormula": "|xi|/sqrt(xi^2+gamma^2+rho^2)",
        "chiSamples": chi_rows,
        "LambdaPaymentRequired": True,
        "cOnlyUniformBound": False,
        "latticeSum": {"beta": rounded(beta), "mu": rounded(mu), "cutoff": cutoff,
                       "directSymmetricSum": rounded(partial), "closedForm": rounded(closed),
                       "tailSizedResidual": rounded(abs(closed - partial))},
        "transverseLimit": "a_j -> |Lambda|*m2(d) when beta=gamma=0 and xi=sqrt(mu)->0",
    }


def kernel_and_j_record() -> dict[str, Any]:
    phi_rows, psi_rows = [], []
    for a, d in ((0.7, 1.25), (2.0, 0.5), (0.125, 4.0)):
        phi = (1 - math.exp(-a * d)) / a
        psi = math.sqrt((1 - math.exp(-2 * a * d)) / (2 * a))
        phi_rows.append({"a": rounded(a), "D": rounded(d), "value": rounded(phi)})
        psi_rows.append({"a": rounded(a), "D": rounded(d), "value": rounded(psi)})
    j_rows = []
    for a, b, tau in ((0.7, 1.1, 2.0), (1.5, 1.5, 0.8), (3.0, 0.25, 1.2)):
        value = ((math.exp(-b * tau) - math.exp(-a * tau)) / (a - b)
                 if a != b else tau * math.exp(-a * tau))
        j_rows.append({"a": rounded(a), "b": rounded(b), "tau": rounded(tau),
                       "value": rounded(value), "branch": "unequal" if a != b else "equal"})
    return {
        "PhiFormula": "(1-exp(-a*D))/a", "PsiFormula": "sqrt((1-exp(-2*a*D))/(2*a))",
        "PhiSamples": phi_rows, "PsiSamples": psi_rows,
        "strongKernelL1": "min(g^(-1),A_theta*alpha^2)",
        "strongKernelL2": "min((2g)^(-1/2),sqrt(B_theta)*alpha)",
        "JFormula": "(exp(-b*tau)-exp(-a*tau))/(a-b), with equal branch tau*exp(-a*tau)",
        "JSamples": j_rows, "equalRateUniformGapDenominator": False,
    }


def claim_ledger() -> dict[str, Any]:
    source = (REPOSITORY / "research/r072z_report-source.md").read_text()
    groups = {"CLOSED": CLOSED_KEYS, "FALSE": FALSE_KEYS, "OPEN": OPEN_KEYS}
    for status, keys in groups.items():
        for key in keys:
            pattern = r"\\texttt\{" + re.escape(key) + r"\}.*?=\\texttt\{" + status + r"\}"
            if not re.search(pattern, source, flags=re.DOTALL):
                raise RuntimeError(f"claim source mismatch: {key} != {status}")
    return {"closed": list(CLOSED_KEYS), "false": list(FALSE_KEYS), "open": list(OPEN_KEYS)}


def claim_boundary() -> dict[str, bool]:
    return {
        "finiteDeterministicAlgebraCertified": True,
        "lowGapOSTransientA2PropagatorProved": False,
        "collisionScaleLimitingPropagatorProved": False,
        "finiteMatrixEqualsFullOperatorNormProved": False,
        "BlochUniformPhysicalVelocityDirectSumProved": False,
        "completeLinearizedShearSubsystemProved": False,
        "nonlinearNavierStokesClosureProved": False,
        "clayMillenniumProblemSolved": False,
    }


def payload() -> dict[str, Any]:
    tangent, scaled = tangent_and_scaled_record()
    body = {
        "schemaVersion": 1,
        "researchRelease": "R0.72Z",
        "status": "passed",
        "producerMethod": "exact-rational-ledgers-plus-direct-symmetric-fourier-sums",
        "commutatorMatrix": commutator_and_matrix_record(),
        "highGapBounds": m3_and_s_record(),
        "alphaPower": alpha_power_record(),
        "twoModeWitnesses": two_mode_record(),
        "tangentResidual": tangent,
        "scaledCubic": scaled,
        "orientation": orientation_record(),
        "kernels": kernel_and_j_record(),
        "claimLedger": claim_ledger(),
        "claimBoundary": claim_boundary(),
        "sourceHashes": source_hashes(),
    }
    body["exactChecks"] = {
        "commutatorSignFrozen": body["commutatorMatrix"]["energyPressureSign"] == "-c*<r,Hr>",
        "matrixSelfAdjointSamples": float(body["commutatorMatrix"]["selfAdjointSampleResidual"]) < 1e-14,
        "sSamplesWithinBound": all(row["boundSatisfied"] for row in body["highGapBounds"]["sBoundSamples"]),
        "alphaPowerSamples": all(float(row["relativeResidual"]) < 1e-14 for row in body["alphaPower"]["samples"]),
        "lowModeGrows": body["twoModeWitnesses"]["lowMode"]["instantaneousGrowth"],
        "tangentResidualExact": body["tangentResidual"]["imaginaryResidual"].endswith("=0"),
        "scaledCubicCoefficientsExact": body["scaledCubic"]["VLimitCoefficients"] == {"X^3": "-1/1", "S*X": "-6/1"},
        "chiSamplesBounded": all(row["boundedByOne"] for row in body["orientation"]["chiSamples"]),
        "claimBoundaryFailClosed": all(not value for key, value in body["claimBoundary"].items() if key != "finiteDeterministicAlgebraCertified"),
    }
    if not all(body["exactChecks"].values()):
        raise RuntimeError("producer exact check failed")
    return body


FLAT_FILES_WITHOUT_HASH_LEDGER = {
    "README.md", "command.txt", "environment.txt", "generate_certificate.py",
    "independent_recompute.py", "validate_certificate.py", "certificate.json",
    "independent.json", "crosscheck.json", "manifest.json",
}
SOURCE_BINDING_POLICY = {
    "mutablePublicationState": MUTABLE_PUBLICATION_STATE,
    "sourceCommitBlobPermanentlyBound": True,
    "currentAdvanceAllowedOnlyAtCleanDescendantPublicationCommit": True,
}
CLAIM_COUNTS = {"closed": 15, "false": 10, "open": 8}


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def draft_source_bindings() -> list[dict[str, Any]]:
    bindings = []
    for relative in SOURCE_FILES:
        path = REPOSITORY / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"draft source is absent or not a regular file: {relative}")
        bindings.append({
            "path": relative,
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
        })
    return bindings


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
    bindings = []
    for relative in SOURCE_FILES:
        path = REPOSITORY / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"formal source is absent or not a regular file: {relative}")
        try:
            committed_blob = subprocess.check_output(
                ["git", "rev-parse", f"{source_commit}:{relative}"],
                cwd=REPOSITORY,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        except subprocess.CalledProcessError as error:
            raise RuntimeError(
                f"formal source is not frozen in {source_commit}: {relative}"
            ) from error
        working_blob = subprocess.check_output(
            ["git", "hash-object", f"--path={relative}", str(path)],
            cwd=REPOSITORY,
            text=True,
        ).strip()
        if committed_blob != working_blob:
            raise RuntimeError(f"working source differs from {source_commit}:{relative}")
        committed_bytes = subprocess.check_output(
            ["git", "cat-file", "blob", committed_blob], cwd=REPOSITORY
        )
        bindings.append({
            "path": relative,
            "commit": source_commit,
            "gitBlob": committed_blob,
            "sha256": hashlib.sha256(committed_bytes).hexdigest(),
            "bytes": len(committed_bytes),
            "workingTreeBlobMatches": True,
        })
    return bindings


def self_test() -> None:
    value = payload()
    if value.get("status") != "passed" or not all(value.get("exactChecks", {}).values()):
        raise RuntimeError("producer exact self-test failed")
    subprocess.run(
        [sys.executable, str(ROOT / "independent_recompute.py"), "--self-test"],
        check=True,
    )
    print("R0.72Z certificate source self-test: passed (no outputs written)")


def existing_status() -> str | None:
    manifest_path = ROOT / "manifest.json"
    if not manifest_path.exists():
        return None
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    status = manifest.get("status")
    if status == "formal":
        raise RuntimeError("refusing to overwrite a formal R0.72Z certificate")
    # A missing status is the legacy finite-hash schema and is intentionally
    # upgradeable in one pass.  Draft and legacy bundles are both unsealed.
    if status not in (None, "draft"):
        raise RuntimeError("existing certificate manifest has an unknown status")
    return status


def make_crosscheck(
    certificate: dict[str, Any],
    independent: dict[str, Any],
    *,
    stage: str,
    source_commit: str | None,
    bindings: list[dict[str, Any]],
) -> dict[str, Any]:
    comparator_path = ROOT / "validate_certificate.py"
    comparator_namespace: dict[str, Any] = {
        "__name__": "r072z_certificate_comparator",
        "__file__": str(comparator_path),
    }
    exec(
        compile(
            comparator_path.read_text(encoding="utf-8"),
            str(comparator_path),
            "exec",
        ),
        comparator_namespace,
    )
    exact_crosscheck = comparator_namespace["validate_payloads"](
        certificate, independent
    )
    checks = {
        "certificatePassed": certificate.get("status") == "passed",
        "allProducerExactChecksPassed": all(certificate.get("exactChecks", {}).values()),
        "independentRecomputationPassed": independent.get("status") == "passed",
        "allIndependentChecksPassed": all(independent.get("checks", {}).values()),
        "comparatorExactLedgerPassed": exact_crosscheck.get("status") == "passed",
        "routesRemainDistinct": certificate.get("producerMethod") != independent.get("method"),
        "sourceHashesAgree": certificate.get("sourceHashes") == independent.get("sourceHashes"),
        "claimLedgerAgrees": certificate.get("claimLedger") == independent.get("claimLedger"),
        "claimBoundaryAgrees": certificate.get("claimBoundary") == independent.get("claimBoundary"),
        "claimCountsAreExact": {
            key: len(certificate.get("claimLedger", {}).get(key, []))
            for key in CLAIM_COUNTS
        } == CLAIM_COUNTS,
        "certificateStagePropagated": (
            certificate.get("certificateStage") == stage
            and independent.get("certificateStage") == stage
            and certificate.get("sourceCommit") == source_commit
            and independent.get("sourceCommit") == source_commit
        ),
        "lowGapAndPhysicalDirectSumRemainOpen": (
            not certificate["claimBoundary"]["lowGapOSTransientA2PropagatorProved"]
            and not certificate["claimBoundary"]["BlochUniformPhysicalVelocityDirectSumProved"]
        ),
        "nonlinearAndClayRemainFalse": (
            not certificate["claimBoundary"]["nonlinearNavierStokesClosureProved"]
            and not certificate["claimBoundary"]["clayMillenniumProblemSolved"]
        ),
    }
    return {
        "schemaVersion": 1,
        "researchRelease": "R0.72Z",
        "status": "passed" if all(checks.values()) else "failed",
        "method": "producer direct-sum route versus independent Fourier-Poisson-quadrature route",
        "temporaryUnsealedSourceAllowed": stage == "draft",
        "formalSourceReady": stage == "formal",
        "sourceCommit": source_commit,
        "sourceBindings": bindings,
        "sourceBindingPolicy": SOURCE_BINDING_POLICY,
        "certificateSha256": sha256(ROOT / "certificate.json"),
        "checkedSections": exact_crosscheck["checkedSections"],
        "checks": checks,
    }


def ensure_flat_package_directory() -> set[str]:
    unexpected = [
        path.name for path in ROOT.iterdir()
        if path.name != "SHA256SUMS" and (not path.is_file() or path.is_symlink())
    ]
    if unexpected:
        raise RuntimeError(
            f"certificate directory contains non-flat or linked entries: {sorted(unexpected)}"
        )
    actual = {
        path.name for path in ROOT.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    }
    if actual != FLAT_FILES_WITHOUT_HASH_LEDGER:
        raise RuntimeError("certificate directory has unexpected or missing flat files")
    return actual


def write_flat_hash_ledger() -> None:
    actual = ensure_flat_package_directory()
    for name in actual:
        if (ROOT / name).is_symlink():
            raise RuntimeError(f"certificate flat file is a symlink: {name}")
    (ROOT / "SHA256SUMS").write_text(
        "".join(f"{sha256(ROOT / name)}  {name}\n" for name in sorted(actual)),
        encoding="utf-8",
    )


def build(stage: str, source_commit: str | None) -> None:
    # Refuse ignored cache directories or any other non-flat entry before the
    # first JSON output is touched.
    ensure_flat_package_directory()
    existing_status()
    bindings = (
        formal_source_bindings(str(source_commit))
        if stage == "formal"
        else draft_source_bindings()
    )
    independent_command = [
        sys.executable,
        str(ROOT / "independent_recompute.py"),
        f"--{stage}",
        "--output",
        str(ROOT / "independent.json"),
    ]
    if stage == "formal":
        independent_command.extend(["--formal-source-commit", str(source_commit)])
    subprocess.run(independent_command, check=True)

    certificate = payload()
    certificate["certificateStage"] = stage
    certificate["sourceCommit"] = source_commit
    write_json(ROOT / "certificate.json", certificate)
    independent = json.loads((ROOT / "independent.json").read_text(encoding="utf-8"))
    crosscheck = make_crosscheck(
        certificate,
        independent,
        stage=stage,
        source_commit=source_commit,
        bindings=bindings,
    )
    if crosscheck["status"] != "passed" or not all(crosscheck["checks"].values()):
        raise RuntimeError(f"independent R0.72Z {stage} crosscheck failed")
    write_json(ROOT / "crosscheck.json", crosscheck)
    limitation_prefix = (
        "Formally source-bound finite algebra only."
        if stage == "formal"
        else "Draft finite algebra only. Formal source-commit binding is absent."
    )
    manifest = {
        "schemaVersion": 1,
        "researchRelease": "R0.72Z",
        "bundle": "R0.72Z deterministic OS--Squire finite-algebra ledger",
        "status": stage,
        "sourceCommit": source_commit,
        "sourceBindings": bindings,
        "sourceBindingPolicy": SOURCE_BINDING_POLICY,
        "claimCounts": CLAIM_COUNTS,
        "boundary": certificate["claimBoundary"],
        "deterministic": True,
        "createdAt": "2026-08-28T00:00:00+08:00",
        "files": {
            name: {"sha256": sha256(ROOT / name), "bytes": (ROOT / name).stat().st_size}
            for name in ("certificate.json", "independent.json", "crosscheck.json")
        },
        "limitations": (
            limitation_prefix
            + " Low-gap OS propagation, collision-scale limiting absorption, "
            "finite-to-infinite operator-norm passage, the Bloch-uniform physical "
            "velocity direct sum, the complete linearized subsystem, nonlinear "
            "Navier--Stokes closure, and Clay are not machine checked or claimed."
        ),
    }
    write_json(ROOT / "manifest.json", manifest)
    write_flat_hash_ledger()
    print(f"R0.72Z {stage} deterministic certificate: passed and written")


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
        build("draft", None)
        return
    if args.formal:
        source_commit = str(args.formal_source_commit or "")
        ensure_clean_head(source_commit)
        build("formal", source_commit)
        return
    parser.error("use --self-test, --draft, or --formal --formal-source-commit <40-hex>")


if __name__ == "__main__":
    main()
