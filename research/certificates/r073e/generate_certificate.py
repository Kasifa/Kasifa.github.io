#!/usr/bin/env python3
"""Generate the deterministic, source-bound R0.73E certificate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "research/certificates/r073e"
SOURCE_COMMIT = "803279d72c24a54db27c40dcdad97593636788fc"

CLOSED = (
    "fixedPositiveHalfPlaneNoPollution",
    "allModesRightOfBProjectionNormPersistence",
    "topInviscidClusterExists",
    "topViscousClusterPersistence",
    "topReducedHalfPlaneResolventUniform",
    "frozenTopClusterRelativeDichotomy",
    "fixedFrozenGeneratorVolterraTransfer",
    "logFastTimeTransfer",
    "superPolynomialCompleteRowNoGo",
)
OPEN = (
    "certifiedSigmaStarIsRightmost",
    "selectedSigmaStarComplementDichotomy",
    "uniformHalfPlaneBoundAtBEqualsZero",
    "globalRightHalfPlaneNoPollution",
    "absoluteUniformComplementDecay",
    "explicitHalfPlaneGap",
    "explicitViscosityThreshold",
    "quantitativeEigenvalueRate",
    "movingProfileUniformContour",
    "graphDomainKatoTransport",
    "movingProfileEvolutionDichotomy",
    "inviscidRootUnique",
    "inviscidEigenvalueSimple",
    "completeOSSquireA2DirectSum",
    "fixedWindowExponentialLowerLaw",
    "nonlinearNavierStokes",
    "Clay",
)

SOURCE_PATHS = (
    "research/r073e_problem_freeze.md",
    "research/r073e_halfplane_transfer_proof.md",
    "research/r073e_independent_analytic_audit.md",
    "research/r073e_literature_audit.md",
    "research/r073e_gap_matrix.md",
    "research/r073e_report-source.md",
    "experiments/r073e/README.md",
    "experiments/r073e/command.txt",
    "experiments/r073e/environment.json",
    "experiments/r073e/requirements.txt",
    "experiments/r073e/diagnose_complement.py",
    "experiments/r073e/complement_diagnostic.json",
    "experiments/r073e/progress.ndjson",
    "experiments/r073e/independent_validate.py",
    "experiments/r073e/independent_validation.json",
    "experiments/r073e/SHA256SUMS",
    "figures/r073e/fig-r073e-complement-transfer/manifest.json",
    "figures/r073e/fig-r073e-complement-transfer/validation.json",
)


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def source_binding(relative: str) -> dict[str, object]:
    working = (ROOT / relative).read_bytes()
    committed = subprocess.check_output(
        ["git", "show", f"{SOURCE_COMMIT}:{relative}"], cwd=ROOT
    )
    require(working == committed, f"working source differs from {SOURCE_COMMIT}: {relative}")
    return {
        "path": relative,
        "commit": SOURCE_COMMIT,
        "gitBlob": run("git", "rev-parse", f"{SOURCE_COMMIT}:{relative}"),
        "sha256": sha256_bytes(working),
        "bytes": len(working),
        "workingTreeBytesMatch": True,
    }


def statuses(text: str) -> dict[str, str]:
    return dict(re.findall(r"^([A-Za-z][A-Za-z0-9]*)=(CLOSED|OPEN)$", text, re.MULTILINE))


def exact_statuses(text: str) -> bool:
    observed = statuses(text)
    expected = {**{name: "CLOSED" for name in CLOSED}, **{name: "OPEN" for name in OPEN}}
    return observed == expected


def verify_flat_checksum_ledger(relative: str) -> bool:
    rows = (ROOT / relative).read_text().splitlines()
    if not rows:
        return False
    for row in rows:
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", row)
        if match is None:
            return False
        path = ROOT / match.group(2)
        if not path.is_file() or sha256(path) != match.group(1):
            return False
    return True


def figure_manifest_passes(manifest: dict, validation: dict) -> bool:
    if manifest.get("status") != "formal" or validation.get("status") != "passed":
        return False
    if not all(validation.get("checks", {}).values()):
        return False
    for section in ("inputs", "sources", "outputs"):
        for entry in manifest.get(section, []):
            relative = entry["path"]
            path = ROOT / relative if "/" in relative else ROOT / "figures/r073e/fig-r073e-complement-transfer" / relative
            if not path.is_file() or sha256(path) != entry["sha256"] or len(path.read_bytes()) != entry["bytes"]:
                return False
    return True


def main() -> int:
    require(run("git", "rev-parse", "HEAD") == SOURCE_COMMIT, "generator must run at the sealed source commit")
    sources = {path: (ROOT / path).read_text() for path in SOURCE_PATHS if path.endswith((".md", ".txt"))}
    proof = sources["research/r073e_halfplane_transfer_proof.md"]
    audit = sources["research/r073e_independent_analytic_audit.md"]
    literature = sources["research/r073e_literature_audit.md"]
    finite = json.loads((ROOT / "experiments/r073e/complement_diagnostic.json").read_text())
    independent = json.loads((ROOT / "experiments/r073e/independent_validation.json").read_text())
    figure_manifest = json.loads((ROOT / "figures/r073e/fig-r073e-complement-transfer/manifest.json").read_text())
    figure_validation = json.loads((ROOT / "figures/r073e/fig-r073e-complement-transfer/validation.json").read_text())

    ledger_paths = (
        "research/r073e_problem_freeze.md",
        "research/r073e_halfplane_transfer_proof.md",
        "research/r073e_gap_matrix.md",
        "research/r073e_report-source.md",
    )
    finite_false_keys = (
        "additionalContinuumEigenpairProvedHere",
        "clayProblemSolved",
        "continuousTimeSemigroupBoundProvedHere",
        "continuumComplementaryDichotomyProvedHere",
        "movingProfileUniformityProvedHere",
        "nonautonomousTransferProvedHere",
        "nonlinearNavierStokesProvedHere",
        "ordinaryCutoffAgreementIsContinuumProof",
    )
    checks = {
        "sourceHeadIsSealedCommit": run("git", "rev-parse", "HEAD") == SOURCE_COMMIT,
        "fourAnalyticLedgersExact": all(exact_statuses(sources[path]) for path in ledger_paths),
        "independentAuditFinalPass": "r073eIndependentAnalyticAudit=PASS" in audit and "**FINAL PASS**" in audit,
        "auditClosesExactlyNineClaims": all(f"{name}=CLOSED" in audit for name in CLOSED),
        "fixedPositiveHalfPlaneQuantifiersPresent": r"Fix \(b>0\)" in proof and "need not\nremain bounded as " + r"\(b\downarrow0\)" in proof,
        "relativeDichotomyAndBromwichPresent": "uniform relative exponential dichotomy" in proof and "inverse Laplace formula" in proof,
        "boundedDriftConstantPresent": "C_A=\\frac{49}{4}" in proof,
        "logarithmicTransferPresent": "T_\\varepsilon=M\\log(1/\\varepsilon)" in proof,
        "completeRowEmbeddingPresent": "initial Squire\nvorticity" in proof and "embeds isometrically" in proof,
        "literatureNoPriorityClaim": "No originality or priority claim" in literature,
        "finitePrimaryAllChecksPass": finite.get("allChecksPass") is True and all(finite.get("checks", {}).values()),
        "finiteIndependentAllChecksPass": independent.get("allChecksPass") is True and all(independent.get("checks", {}).values()),
        "finiteEvidenceFailClosed": (
            finite["claimBoundary"].get("finiteBinary64Diagnostic") is True
            and all(finite["claimBoundary"].get(key) is False for key in finite_false_keys)
            and independent["claimBoundary"].get("independentFiniteRecomputation") is True
            and independent["claimBoundary"].get("continuumDichotomyCertified") is False
            and independent["claimBoundary"].get("continuousTimeBoundCertified") is False
        ),
        "finiteChecksumLedgerPasses": verify_flat_checksum_ledger("experiments/r073e/SHA256SUMS"),
        "formalFigureValidationPasses": figure_manifest_passes(figure_manifest, figure_validation),
        "figureClaimBoundaryFailClosed": (
            figure_manifest["claimBoundary"].get("formalFiniteDiagnosticFigure") is True
            and figure_manifest["claimBoundary"].get("continuumComplementDichotomyProvedHere") is False
            and figure_manifest["claimBoundary"].get("nonautonomousTransferProvedHere") is False
            and figure_manifest["claimBoundary"].get("nonlinearNavierStokesProvedHere") is False
            and figure_manifest["claimBoundary"].get("clayProblemSolved") is False
        ),
    }
    require(all(checks.values()), f"certificate checks failed: {[key for key, value in checks.items() if not value]}")

    largest_n = max(finite["parameters"]["cutoffs"])
    selected = next(row for row in finite["rows"] if row["N"] == largest_n and row["epsilon"] == 1e-6)
    bindings = [source_binding(path) for path in SOURCE_PATHS]
    certificate = {
        "schemaVersion": "r073e-deterministic-analytic-certificate-v1",
        "release": "R0.73E",
        "created": "2026-08-30",
        "sourceCommit": SOURCE_COMMIT,
        "sourceBindings": bindings,
        "closedClaims": {name: "CLOSED" for name in CLOSED},
        "openClaims": {name: "OPEN" for name in OPEN},
        "checks": checks,
        "analyticSentinels": {
            "certifiedEigenvalueBracket": [0.17035, 0.17050],
            "profileDriftBound": [49, 4],
            "positiveHalfPlaneUniformityAtZero": False,
            "fixedWindowExponentialLaw": False,
        },
        "finiteDiagnostics": {
            "evidenceClass": "finite IEEE-754 binary64 diagnostic only",
            "largestCutoff": largest_n,
            "rowCount": len(finite["rows"]),
            "epsilon": selected["epsilon"],
            "clusterEigenvalueReal": selected["clusterEigenvalue"]["real"],
            "movingComplementSpectralAbscissa": selected["qSpectrum"]["spectralAbscissa"],
            "movingComplementEndpointNorm": selected["semigroup"]["intrinsicMovingQ"]["endpointNorm"],
            "fixedComplementEndpointNorm": selected["semigroup"]["ambientFixedQ0"]["endpointNorm"],
            "maximumAlgebraicResidual": finite["maximums"]["allAlgebraicResiduals"],
            "independentMaximumErrors": independent["maximumErrors"],
            "continuumConclusion": False,
        },
        "formalFigure": {
            "figureId": figure_manifest["figureId"],
            "status": figure_manifest["status"],
            "validationStatus": figure_validation["status"],
            "pdf": next(item for item in figure_manifest["outputs"] if item["path"] == "figure.pdf"),
            "svg": next(item for item in figure_manifest["outputs"] if item["path"] == "figure.svg"),
            "png": next(item for item in figure_manifest["outputs"] if item["path"] == "figure.png"),
        },
        "claimBoundary": {name: False for name in OPEN},
    }
    progress = [
        {"event": "start", "release": "R0.73E", "sourceCommit": SOURCE_COMMIT},
        {"event": "source-bindings", "count": len(bindings), "passed": True},
        {"event": "analytic-ledger", "closed": len(CLOSED), "open": len(OPEN), "passed": True},
        {"event": "finite-diagnostic", "rows": len(finite["rows"]), "independentPass": True, "finiteOnly": True},
        {"event": "formal-figure", "status": "passed", "formats": ["PDF", "SVG", "PNG-600dpi"]},
        {"event": "complete", "certificate": "certificate.json"},
    ]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "certificate.json").write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    (OUT / "progress.ndjson").write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in progress))
    print(json.dumps({"event": "certificate-generated", "checks": len(checks), "closed": 9, "open": 17}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
