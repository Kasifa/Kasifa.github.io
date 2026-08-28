#!/usr/bin/env python3
"""Fail-closed validator for the draft R0.72Y finite certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
EXPECTED_SOURCE_FILES = (
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
COMPARED_SECTIONS = (
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
MUTABLE_PUBLICATION_STATE = "research/release-manifest.json"
EXPECTED_SOURCE_BINDING_POLICY = {
    "mutablePublicationState": MUTABLE_PUBLICATION_STATE,
    "sourceCommitBlobPermanentlyBound": True,
    "currentAdvanceAllowedOnlyAtCleanDescendantPublicationCommit": True,
}


def load(name: str) -> dict:
    path = ROOT / name
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"required regular file is absent: {name}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"{name} is not a JSON object")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_draft_bindings(manifest: dict, crosscheck: dict) -> None:
    bindings = manifest.get("sourceBindings")
    if manifest.get("sourceCommit") is not None or crosscheck.get("sourceCommit") is not None:
        raise RuntimeError("draft certificate must not claim a source commit")
    if not isinstance(bindings, list) or bindings != crosscheck.get("sourceBindings"):
        raise RuntimeError("draft source bindings are missing or inconsistent")
    if [row.get("path") for row in bindings] != list(EXPECTED_SOURCE_FILES):
        raise RuntimeError("draft source bindings do not cover the expected package sources")
    seen: set[str] = set()
    for row in bindings:
        relative = row.get("path")
        if (
            not isinstance(relative, str)
            or relative.startswith("/")
            or ".." in Path(relative).parts
            or relative in seen
        ):
            raise RuntimeError("malformed or duplicate draft source binding")
        seen.add(relative)
        path = (REPOSITORY / relative).resolve()
        if REPOSITORY.resolve() not in path.parents or not path.is_file() or path.is_symlink():
            raise RuntimeError(f"bound draft source is absent, linked, or escapes repository: {relative}")
        if row.get("sha256") != digest(path) or row.get("bytes") != path.stat().st_size:
            raise RuntimeError(f"draft source binding drift: {relative}")


def validate_formal_bindings(manifest: dict, crosscheck: dict) -> None:
    commit = str(manifest.get("sourceCommit", ""))
    bindings = manifest.get("sourceBindings")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise RuntimeError("formal source commit is missing or malformed")
    if not isinstance(bindings, list) or bindings != crosscheck.get("sourceBindings"):
        raise RuntimeError("formal source bindings are missing or inconsistent")
    if [row.get("path") for row in bindings] != list(EXPECTED_SOURCE_FILES):
        raise RuntimeError("formal source bindings do not cover the complete frozen source set")
    if crosscheck.get("sourceCommit") != commit:
        raise RuntimeError("formal crosscheck source commit drifted")
    if subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=REPOSITORY,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode:
        raise RuntimeError("formal sourceCommit is not a valid Git commit object")
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True
    ).strip()
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, head],
        cwd=REPOSITORY,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode:
        raise RuntimeError("formal sourceCommit is not an ancestor of current HEAD")

    status_rows = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=REPOSITORY,
        text=True,
    ).splitlines()
    status_paths: set[str] = set()
    for status_row in status_rows:
        relative = status_row[3:]
        if " -> " in relative:
            raise RuntimeError("formal validation refuses ambiguous rename status")
        status_paths.add(relative)

    seen: set[str] = set()
    mutable_publication_state_advanced = False
    for row in bindings:
        relative = row.get("path")
        if (
            not isinstance(relative, str)
            or relative.startswith("/")
            or ".." in Path(relative).parts
            or relative in seen
            or row.get("commit") != commit
            or row.get("workingTreeBlobMatches") is not True
        ):
            raise RuntimeError("malformed or duplicate formal source binding")
        seen.add(relative)
        path = (REPOSITORY / relative).resolve()
        if REPOSITORY.resolve() not in path.parents or not path.is_file() or path.is_symlink():
            raise RuntimeError(f"bound formal source is absent, linked, or escapes repository: {relative}")
        try:
            committed_blob = subprocess.check_output(
                ["git", "rev-parse", f"{commit}:{relative}"],
                cwd=REPOSITORY,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        except subprocess.CalledProcessError as error:
            raise RuntimeError(f"formal source is absent from sourceCommit: {relative}") from error
        source_blob_bytes = subprocess.check_output(
            ["git", "cat-file", "blob", committed_blob],
            cwd=REPOSITORY,
        )
        working_blob = subprocess.check_output(
            ["git", "hash-object", f"--path={relative}", str(path)],
            cwd=REPOSITORY,
            text=True,
        ).strip()
        if (
            row.get("gitBlob") != committed_blob
            or row.get("sha256") != hashlib.sha256(source_blob_bytes).hexdigest()
            or row.get("bytes") != len(source_blob_bytes)
            or row.get("workingTreeBlobMatches") is not True
        ):
            raise RuntimeError(f"formal source binding drift: {relative}")
        if working_blob == committed_blob:
            if row.get("sha256") != digest(path) or row.get("bytes") != path.stat().st_size:
                raise RuntimeError(f"formal working source digest drift: {relative}")
            continue
        if relative != MUTABLE_PUBLICATION_STATE or head == commit:
            raise RuntimeError(f"immutable formal source drift: {relative}")
        if relative in status_paths:
            raise RuntimeError("publication-state manifest drift must be clean-committed")
        try:
            head_blob = subprocess.check_output(
                ["git", "rev-parse", f"{head}:{relative}"],
                cwd=REPOSITORY,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        except subprocess.CalledProcessError as error:
            raise RuntimeError(
                "publication-state manifest is absent from descendant HEAD"
            ) from error
        if working_blob != head_blob:
            raise RuntimeError(
                "publication-state manifest does not equal its clean descendant blob"
            )
        mutable_publication_state_advanced = True

    allowed_generated_mutations = {
        "research/certificates/r072y/certificate.json",
        "research/certificates/r072y/independent.json",
        "research/certificates/r072y/crosscheck.json",
        "research/certificates/r072y/manifest.json",
        "research/certificates/r072y/SHA256SUMS",
    }
    source_set = set(EXPECTED_SOURCE_FILES)
    for relative in status_paths:
        if relative in source_set:
            raise RuntimeError(
                "formal validation found a frozen-source working-tree mutation: "
                f"{relative}"
            )
        if head == commit and relative not in allowed_generated_mutations:
            raise RuntimeError(
                "at source HEAD, formal validation permits only certificate outputs: "
                f"{relative}"
            )
    if mutable_publication_state_advanced and status_rows:
        raise RuntimeError(
            "an advanced publication-state manifest is accepted only at a completely "
            "clean descendant publication commit"
        )


def validate_claim_boundary(boundary: dict) -> None:
    expected = {
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
    if boundary != expected:
        raise RuntimeError("claim boundary is incomplete or has drifted")


def validate_claim_ledger(ledger: dict) -> None:
    expected_keys = {
        "finite-certified",
        "analytic-not-finitely-certified",
        "negative-result-keys",
        "open-keys",
    }
    if set(ledger) != expected_keys:
        raise RuntimeError("claim ledger categories drifted")
    for category, values in ledger.items():
        if not isinstance(values, list) or not values or len(values) != len(set(values)):
            raise RuntimeError(f"claim ledger category is empty or duplicated: {category}")
    required_finite = {
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
    }
    if set(ledger["finite-certified"]) != required_finite:
        raise RuntimeError("finite-certified claim keys drifted")
    required_analytic = {
        "strongRowL2ForcingDuhamelAlpha2",
        "strongRowStandardHMinusOneTransferAlpha",
        "strongRowSemiclassicalHMinusOneTransferAlpha2",
        "standardHMinusOneAlphaSharpness",
        "semiclassicalHMinusOneAlpha2Sharpness",
        "HMinusOneEndpointNoAlphaGainSharpness",
    }
    if not required_analytic.issubset(ledger["analytic-not-finitely-certified"]):
        raise RuntimeError("analytic-not-finitely-certified keys are incomplete")
    if "clayMillenniumProblem" not in ledger["open-keys"]:
        raise RuntimeError("Clay status is absent from the open ledger")


def validate_exact_ledger(certificate: dict) -> None:
    if certificate.get("status") != "passed" or not all(certificate.get("exactChecks", {}).values()):
        raise RuntimeError("certificate exact checks did not all pass")

    heat = certificate.get("heatShearIdentity", {})
    if (
        heat.get("identity") != "W_d=W_xx"
        or heat.get("derivedIdentity") != "(W_x)_d=W_xxx"
        or heat.get("allModesMatch") is not True
        or [row.get("frequency") for row in heat.get("modeRows", [])] != [1, 2]
        or [row.get("decayRate") for row in heat.get("modeRows", [])] != [1, 4]
    ):
        raise RuntimeError("heat-shear ledger drifted")

    pressure = certificate.get("pressurePoissonFactorTwo", {})
    if (
        pressure.get("pressureEquation") != "L*pi=2*i*c*W_x*u_2"
        or pressure.get("divergenceGradientSign") != "div_j(grad_j*pi)=-L*pi"
        or pressure.get("factorTwo") != 2
        or pressure.get("coefficientSum") != 0
    ):
        raise RuntimeError("pressure factor two or sign ledger drifted")

    leray = certificate.get("blochLerayIdentity", {})
    if (
        leray.get("L") != "-A_beta^2+mu"
        or leray.get("identityResidual") != []
        or leray.get("divergenceOfProjectionCoefficients") != ["1/1", "-1/1"]
        or leray.get("divergenceOfProjectionSum") != "0/1"
        or leray.get("projectionKillsGradientCoefficients") != ["1/1", "-1/1"]
    ):
        raise RuntimeError("Bloch/Leray identity drifted")

    os_squire = certificate.get("osSquireSignLedger", {})
    expected_os = {"W*q": -1, "W_x*A_beta*u_2": 0, "W_xx*u_2": -1}
    if (
        os_squire.get("domain") != "mu>0"
        or os_squire.get("orrSommerfeldCoefficientTableInUnitsOfIc", {}).get("sum") != expected_os
        or os_squire.get("expectedOsSum") != expected_os
        or os_squire.get("squirePressureSum") != 0
        or os_squire.get("squireLiftCoefficient") != 1
        or os_squire.get("orrSommerfeldEquation") != "q_d=(-L-i*c*W)q-i*c*W_xx*L^(-1)q"
        or os_squire.get("squireEquation") != "eta_d=(-L-i*c*W)eta+i*xi*Lambda*W_x*L^(-1)q"
    ):
        raise RuntimeError("Orr--Sommerfeld/Squire sign ledger drifted")

    recovery = certificate.get("velocityReconstruction", {})
    if recovery.get("domain") != "mu=xi^2+gamma^2>0":
        raise RuntimeError("velocity reconstruction domain drifted")
    if any(cell for row in recovery.get("matrixIdentityResidual", []) for cell in row):
        raise RuntimeError("velocity reconstruction ledger drifted")
    if (
        recovery.get("reconstructedDivergenceNumerator", {}).get("eta") != []
        or recovery.get("reconstructedEtaNumerator", {}).get("A_beta_u2") != []
        or "mu^(-1)" not in recovery.get("energyIdentity", "")
    ):
        raise RuntimeError("velocity reconstruction ledger drifted")

    lift = certificate.get("zeroCouplingLiftUp", {})
    if (
        lift.get("row") != "gamma=0, beta=0, xi>=0"
        or lift.get("u2ResidualCoefficient") != 0
        or lift.get("u3ResidualAfterCommonFactor", {}).get("left") != lift.get("u3ResidualAfterCommonFactor", {}).get("right")
        or not all(row.get("matches") for row in lift.get("WxHeatRows", []))
        or lift.get("meanSquareCoefficientsForExpMinus2dAndExpMinus8d") != ["1/8", "1/8"]
        or lift.get("meanSquareWx") != "(1/8)*(exp(-2d)+exp(-8d))"
    ):
        raise RuntimeError("lift-up residual or norm ledger drifted")

    kernel = certificate.get("causalKernel", {})
    if (
        kernel.get("finiteGeometricIdentityChecked") is not True
        or kernel.get("finiteDegreesChecked") != [0, 64]
        or kernel.get("exactPositiveMuIntegral") != "(1-exp(-p*mu*h))/(p*mu*(1-q^p*exp(-p*mu*h)))"
        or kernel.get("exactZeroDampingIntegral") != "h/(1-q^p)"
        or kernel.get("zeroDampingLimit") != "lim(mu->0+)=h/(1-q^p)"
        or kernel.get("infiniteSeriesConvergenceBoundary") != "analytic-not-finitely-certified"
    ):
        raise RuntimeError("causal-kernel algebra drifted")

    weights = certificate.get("fourierWeights", {})
    if (
        weights.get("range") != "0<alpha<=1, k real"
        or weights.get("lowerCrossMultipliedDifference") != [
            {"monomial": "1", "coefficient": "1/1"},
            {"monomial": "alpha^2", "coefficient": "-1/1"},
        ]
        or weights.get("exactRationalGridChecked") is not True
        or weights.get("normConsequence") != "alpha*||F||_{H^-1_alpha,beta}<=||F||_{H^-1_beta}<=||F||_{H^-1_alpha,beta}"
    ):
        raise RuntimeError("Fourier weight ledger drifted")

    damping = certificate.get("dampingGap", {})
    if (
        damping.get("youngIdentityResidual") != []
        or damping.get("exactRationalSamplesChecked") is not True
        or damping.get("positiveNormGapCondition") != "g_j>K/2"
        or damping.get("energyExponent") != "2*(g_j-K/2)"
        or damping.get("normExponent") != "g_j-K/2"
        or damping.get("energyExponentToNormExponent")
        != "norm exponent is one half of the energy exponent"
    ):
        raise RuntimeError("damping-gap ledger drifted")

    validate_claim_ledger(certificate.get("claimLedger", {}))
    validate_claim_boundary(certificate.get("claimBoundary", {}))


def validate_sha256_ledger() -> None:
    ledger = ROOT / "SHA256SUMS"
    if not ledger.is_file() or ledger.is_symlink():
        raise RuntimeError("flat SHA256SUMS ledger is absent")
    names: list[str] = []
    for row in ledger.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\\r\n]+)", row)
        if not match:
            raise RuntimeError(f"malformed SHA256SUMS row: {row}")
        expected, name = match.groups()
        path = ROOT / name
        if not path.is_file() or path.is_symlink() or digest(path) != expected:
            raise RuntimeError(f"SHA256SUMS drift: {name}")
        names.append(name)
    actual = sorted(path.name for path in ROOT.iterdir() if path.is_file() and path.name != "SHA256SUMS")
    if names != sorted(set(names)) or names != actual:
        raise RuntimeError("SHA256SUMS must cover every flat regular file exactly once")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-draft", action="store_true")
    parser.add_argument("--require-formal", action="store_true")
    args = parser.parse_args()
    if args.require_draft == args.require_formal:
        parser.error("choose exactly one of --require-draft or --require-formal")

    certificate = load("certificate.json")
    independent = load("independent.json")
    crosscheck = load("crosscheck.json")
    manifest = load("manifest.json")
    expected_status = "formal" if args.require_formal else "draft"
    if manifest.get("status") != expected_status or manifest.get("deterministic") is not True:
        raise RuntimeError(f"{expected_status} deterministic manifest required")
    if (
        manifest.get("sourceBindingPolicy") != EXPECTED_SOURCE_BINDING_POLICY
        or crosscheck.get("sourceBindingPolicy") != EXPECTED_SOURCE_BINDING_POLICY
    ):
        raise RuntimeError("source-binding mutable publication-state policy drifted")
    if args.require_formal:
        if (
            crosscheck.get("temporaryUnsealedSourceAllowed") is not False
            or crosscheck.get("formalSourceReady") is not True
        ):
            raise RuntimeError("formal source-ready flags are inconsistent")
        validate_formal_bindings(manifest, crosscheck)
    else:
        if (
            crosscheck.get("temporaryUnsealedSourceAllowed") is not True
            or crosscheck.get("formalSourceReady") is not False
        ):
            raise RuntimeError("draft/formal status boundary is inconsistent")
        validate_draft_bindings(manifest, crosscheck)
    validate_exact_ledger(certificate)
    if manifest.get("claimBoundary") != certificate.get("claimBoundary"):
        raise RuntimeError("manifest claim boundary drift")

    if independent.get("status") != "passed":
        raise RuntimeError("independent recomputation failed")
    expected_commit = manifest.get("sourceCommit")
    if (
        certificate.get("certificateStage") != expected_status
        or independent.get("certificateStage") != expected_status
        or certificate.get("sourceCommit") != expected_commit
        or independent.get("sourceCommit") != expected_commit
    ):
        raise RuntimeError("certificate stage or sourceCommit propagation drifted")
    for section in COMPARED_SECTIONS:
        if independent.get(section) != certificate.get(section):
            raise RuntimeError(f"independent ledger differs: {section}")

    if (
        crosscheck.get("status") != "passed"
        or crosscheck.get("comparedSections") != list(COMPARED_SECTIONS)
        or crosscheck.get("certificateSha256") != digest(ROOT / "certificate.json")
        or not all(crosscheck.get("checks", {}).values())
    ):
        raise RuntimeError(f"{expected_status} crosscheck is stale or incomplete")

    for name in ("certificate.json", "independent.json", "crosscheck.json"):
        path = ROOT / name
        row = manifest.get("files", {}).get(name, {})
        if row.get("sha256") != digest(path) or row.get("bytes") != path.stat().st_size:
            raise RuntimeError(f"manifest drift: {name}")
    if args.require_formal:
        if "Formally source-bound finite algebra only" not in manifest.get("limitations", ""):
            raise RuntimeError("formal limitation does not state the finite source-bound scope")
    elif "Formal source-commit binding is absent" not in manifest.get("limitations", ""):
        raise RuntimeError("draft limitation does not state missing formal binding")
    validate_sha256_ledger()
    print(f"R0.72Y strict {expected_status} certificate validation: passed")


if __name__ == "__main__":
    main()
