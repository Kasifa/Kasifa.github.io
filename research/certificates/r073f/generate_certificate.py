#!/usr/bin/env python3
"""Generate the primary R0.73F provenance and claim-boundary certificate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "research/certificates/r073f"
SOURCE_COMMIT = "5edb1702314feca3e9d47a186b30fc53079cd67a"
ANALYTIC_PATHS = (
    "research/r073f_problem_freeze.md",
    "research/r073f_moving_dichotomy_proof.md",
    "research/r073f_gap_matrix.md",
    "research/r073f_literature_audit.md",
    "research/r073f_independent_analytic_audit.md",
    "research/r073f_report-source.md",
)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def committed(relative: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{SOURCE_COMMIT}:{relative}"], cwd=ROOT
    )


def source_binding(relative: str) -> dict[str, object]:
    payload = committed(relative)
    blob = subprocess.check_output(
        ["git", "rev-parse", f"{SOURCE_COMMIT}:{relative}"],
        cwd=ROOT, text=True,
    ).strip()
    working = ROOT / relative
    return {
        "path": relative,
        "sourceCommit": SOURCE_COMMIT,
        "gitBlob": blob,
        "bytes": len(payload),
        "sha256": sha256_bytes(payload),
        "workingTreeMatchesCommitted": working.is_file() and working.read_bytes() == payload,
    }


def content_binding(relative: str) -> dict[str, object]:
    path = ROOT / relative
    return {"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)}


def ledger_passes(directory: Path) -> bool:
    ledger = directory / "SHA256SUMS"
    rows = {}
    for line in ledger.read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        rows[name] = digest
    expected = {path.name for path in directory.iterdir()
                if path.is_file() and path.name != "SHA256SUMS"}
    return set(rows) == expected and all(
        sha256(directory / name) == digest for name, digest in rows.items()
    )


def main() -> int:
    resolved = subprocess.check_output(
        ["git", "rev-parse", "5edb170^{commit}"], cwd=ROOT, text=True
    ).strip()
    if resolved != SOURCE_COMMIT:
        raise RuntimeError("analytic source commit resolution changed")

    texts = {path: committed(path).decode("utf-8") for path in ANALYTIC_PATHS}
    proof = texts["research/r073f_moving_dichotomy_proof.md"]
    gap = texts["research/r073f_gap_matrix.md"]
    audit = texts["research/r073f_independent_analytic_audit.md"]
    literature = texts["research/r073f_literature_audit.md"]

    finite_dir = ROOT / "experiments/r073f"
    figure_dir = ROOT / "figures/r073f/fig-r073f-fixed-window-roughness"
    finite_manifest = json.loads((finite_dir / "manifest.json").read_text(encoding="utf-8"))
    finite_summary = json.loads((finite_dir / "summary.json").read_text(encoding="utf-8"))
    finite_independent = json.loads((finite_dir / "independent_validation.json").read_text(encoding="utf-8"))
    figure_manifest = json.loads((figure_dir / "manifest.json").read_text(encoding="utf-8"))
    figure_validation = json.loads((figure_dir / "validation.json").read_text(encoding="utf-8"))

    closed_claims = {
        "boundedPerturbationRoughnessWithNoninvertibleStableSemigroup": "CLOSED",
        "movingProfileUniformSpectralStrip": "CLOSED",
        "movingProfileUniformContour": "CLOSED",
        "movingInstantaneousProjectionNormC1": "CLOSED",
        "movingProfileEvolutionDichotomy": "CLOSED",
        "movingUnstableFiberStartsAtFrozenTopSpace": "CLOSED",
        "fixedSmallEndpointExponentialLowerLaw": "CLOSED",
        "fixedWindowExponentialLowerLaw": "CLOSED",
        "fixedWindowLogGainThetaLambda": "CLOSED",
    }
    false_shortcuts = {
        "spectralGapPlusCommonDomainImpliesUniformMovingDichotomy": "FALSE_IN_GENERAL",
        "positiveInstantaneousSpectralAbscissaImpliesFixedWindowGrowth": "FALSE_IN_GENERAL",
    }
    open_claims = {
        "explicitWindowSize": "OPEN",
        "sharpExponentialRate": "OPEN",
        "normalizedLogGainLimitExists": "OPEN",
        "arbitraryEndpointBeyondSmallWindow": "OPEN",
        "dynamicProjectionEqualsInstantaneousRieszProjection": "OPEN",
        "graphDomainKatoTransport": "OPEN_NOT_USED",
        "singleEpsilonIndependentInitialOrbit": "OPEN",
        "certifiedSigmaStarIsRightmost": "OPEN",
        "inviscidEigenvalueSimple": "OPEN",
        "completeOSSquireA2DirectSum": "OPEN",
        "nonlinearNavierStokes": "OPEN",
        "Clay": "OPEN",
    }
    claim_boundary = {name: False for name in open_claims}
    claim_boundary.update({
        "finiteDiagnosticProvesContinuumTheorem": False,
        "diagnosticDIsCertifiedD0": False,
        "counterexamplesDescribeExactFourierRow": False,
    })

    checks = {
        "analyticSourceCommitResolvedExactly": resolved == SOURCE_COMMIT,
        "auditFinalPassAtSourceCommit": "**FINAL PASS.**" in audit,
        "gapTableF1ThroughF8Closed": all(f"| F{index} |" in gap and "CLOSED" in gap.split(f"| F{index} |", 1)[1].splitlines()[0] for index in range(1, 9)),
        "releaseDecisionNineClaimsClosed": all(
            f"{name}=CLOSED" in gap for name in closed_claims
        ),
        "twoInvalidShortcutsRecorded": "| F9 |" in gap and "FALSE IN GENERAL" in gap and "| F10 |" in gap,
        "roughnessRadiusPresent": r"\rho<\frac{\nu}{16K^2}" in proof,
        "graphSmallnessPresent": "1/20" in audit,
        "commonContourAndNormC1Present": "one fixed contour" in proof and r"\partial_dP_\varepsilon" in proof,
        "movingDichotomyPresent": r"\widehat P_\varepsilon(t)" in proof and r"K_1e^{-(\alpha+\eta)(t-r)}" in proof,
        "fixedWindowLowerLawPresent": r"d_D=\min\{D,d_0\}" in proof and r"(\alpha+\eta)d_D|\Lambda|" in proof,
        "r073bFiveSixteenthsInterfacePresent": r"\frac5{16}" in proof,
        "graphDomainBoundaryPresent": r"unscaled \(H^2\) graph-norm" in proof,
        "literaturePriorityFailClosed": "No priority claim" in literature or "no priority claim" in literature,
        "finitePrimaryChecksPass": finite_summary["allPrimaryChecksPass"] is True,
        "finiteIndependentChecksPass": finite_independent["allChecksPass"] is True,
        "finiteLedgerInventoryPasses": ledger_passes(finite_dir),
        "finiteDiagnosticDNotCertifiedD0": finite_manifest["diagnosticEndpointIsCertifiedD0"] is False,
        "figureValidationPasses": figure_validation["status"] == "passed",
        "figureVisualQaPasses": figure_manifest["qa"]["status"] == "passed",
        "figureLedgerInventoryPasses": ledger_passes(figure_dir),
        "claimBoundaryFailClosed": all(value is False for value in claim_boundary.values()),
    }

    certificate = {
        "schemaVersion": "r073f-conditional-operator-certificate-v1",
        "release": "R0.73F",
        "created": "2026-08-30",
        "status": "validated" if all(checks.values()) else "failed",
        "evidenceClass": "conditional exact operator theorem with independent analytic audit; deterministic provenance and consistency certificate",
        "sourceCommit": SOURCE_COMMIT,
        "sourceBindings": [source_binding(path) for path in ANALYTIC_PATHS],
        "checks": checks,
        "exactRationalSentinels": {
            "etaOverNu": [1, 2],
            "rhoScaledUpper": {"quantity": "rho*K^2/nu", "strictUpper": [1, 16]},
            "contraction": {"formula": "q=8*K*rho/(3*nu)", "strictUpper": "1/(6*K)", "globalStrictUpper": [1, 6]},
            "stableAndUnstableGraphNormStrictUpper": [1, 20],
            "graphProductStrictUpper": [1, 400],
            "profileDriftConstant": [49, 4],
            "r073bUpperExponent": [5, 16],
            "rotatingCounterexampleBranchIntegral": [-1, 4],
            "rotatingCounterexamplePointwiseMaximumLower": [1, 4],
        },
        "theorem": {
            "row": {"gamma": [1, 2], "beta": 0, "xi": 0, "bothSignsOfLambda": True},
            "commonDomain": "H^2_per",
            "instantaneousUniformContourOnExistentialLocalWindow": True,
            "instantaneousRieszProjectionNormC1InBH": True,
            "movingDynamicalDichotomy": True,
            "fixedWindowLowerLaw": "G >= K1^{-1} exp((alpha+eta) min(D,d0) |Lambda|)",
            "logGainOrder": "Theta(|Lambda|)",
            "conditionalInputs": ["R0.73C certified eigenvalue", "R0.73E uniform frozen dichotomy", "R0.73B complete-row upper bound"],
        },
        "closedClaims": closed_claims,
        "falseShortcuts": false_shortcuts,
        "openClaims": open_claims,
        "claimBoundary": claim_boundary,
        "finiteDiagnostics": {
            "status": finite_manifest["status"],
            "primaryCutoff": finite_summary["primaryGrid"]["N"],
            "epsilons": finite_summary["primaryGrid"]["epsilons"],
            "diagnosticPhysicalEndpoint": finite_summary["diagnosticPhysicalEndpoint"],
            "diagnosticEndpointIsCertifiedD0": False,
            "continuumConclusion": False,
            "maximumIndependentNormalizedRateError": finite_independent["maximums"]["normalizedRateAbsolute"],
            "scientificWallTimeSeconds": finite_summary["scientificWallTimeSeconds"],
            "independentWallTimeSeconds": finite_independent["wallTimeSeconds"],
        },
        "journalFigure": {
            "figureId": figure_manifest["figureId"],
            "status": figure_manifest["status"],
            "gitSealed": False,
            "validationStatus": figure_validation["status"],
            "visualQaStatus": figure_manifest["qa"]["status"],
            "pdf": content_binding("figures/r073f/fig-r073f-fixed-window-roughness/figure.pdf"),
            "svg": content_binding("figures/r073f/fig-r073f-fixed-window-roughness/figure.svg"),
            "png": {**content_binding("figures/r073f/fig-r073f-fixed-window-roughness/figure.png"), "dpi": 600},
        },
        "contentBindings": [
            content_binding("experiments/r073f/manifest.json"),
            content_binding("experiments/r073f/SHA256SUMS"),
            content_binding("experiments/r073f/summary.json"),
            content_binding("experiments/r073f/independent_validation.json"),
            content_binding("figures/r073f/fig-r073f-fixed-window-roughness/figure.pdf"),
            content_binding("figures/r073f/fig-r073f-fixed-window-roughness/figure.svg"),
            content_binding("figures/r073f/fig-r073f-fixed-window-roughness/figure.png"),
        ],
        "sealState": {
            "analyticSourcesAtImmutableGitCommit": True,
            "finiteAndFigureArtifactsContentAddressed": True,
            "finiteAndFigureArtifactsGitSealed": False,
            "certificatePackageGitSealed": False,
        },
    }
    (OUT / "certificate.json").write_text(canonical(certificate), encoding="utf-8")
    progress = [
        {"event": "analytic-source-bound", "sourceCommit": SOURCE_COMMIT, "bindingCount": len(ANALYTIC_PATHS)},
        {"event": "finite-and-figure-bound", "finiteChecksPass": finite_summary["allPrimaryChecksPass"], "figureValidation": figure_validation["status"]},
        {"event": "primary-certificate-generated", "allChecksPass": all(checks.values())},
    ]
    (OUT / "progress.ndjson").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in progress),
        encoding="utf-8",
    )
    return 0 if certificate["status"] == "validated" else 2


if __name__ == "__main__":
    raise SystemExit(main())
