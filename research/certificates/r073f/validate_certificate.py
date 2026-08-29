#!/usr/bin/env python3
"""Compare the two R0.73F certificate paths and write manifest and ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "research/certificates/r073f"
SOURCE_COMMIT = "5edb1702314feca3e9d47a186b30fc53079cd67a"
SOURCE_FILES = (
    "README.md", "command.txt", "environment.txt", "generate_certificate.py",
    "independent_recompute.py", "validate_certificate.py",
)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(path: Path, relative_to: Path = ROOT) -> dict[str, object]:
    return {"path": str(path.relative_to(relative_to)), "bytes": path.stat().st_size, "sha256": sha256(path)}


def committed_binding(relative: str) -> dict[str, object]:
    payload = subprocess.check_output(["git", "show", f"{SOURCE_COMMIT}:{relative}"], cwd=ROOT)
    blob = subprocess.check_output(["git", "rev-parse", f"{SOURCE_COMMIT}:{relative}"], cwd=ROOT, text=True).strip()
    working = ROOT / relative
    return {
        "path": relative,
        "sourceCommit": SOURCE_COMMIT,
        "gitBlob": blob,
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "workingTreeMatchesCommitted": working.is_file() and working.read_bytes() == payload,
    }


def main() -> int:
    certificate = json.loads((OUT / "certificate.json").read_text(encoding="utf-8"))
    independent = json.loads((OUT / "independent_recompute.json").read_text(encoding="utf-8"))
    expected_sources = [row["path"] for row in certificate["sourceBindings"]]
    independently_bound = [committed_binding(path) for path in expected_sources]

    graph = certificate["exactRationalSentinels"]
    checks = {
        "sourceCommitAgreement": certificate["sourceCommit"] == independent["sourceCommit"] == SOURCE_COMMIT,
        "sourceBindingsIndependentAgreement": certificate["sourceBindings"] == independent["sourceBindings"] == independently_bound,
        "primaryAllChecksPass": certificate["status"] == "validated" and all(certificate["checks"].values()),
        "independentAllChecksPass": independent["allChecksPass"] is True and all(independent["checks"].values()),
        "exactNineReleaseDecisionClaimsClosed": len(certificate["closedClaims"]) == 9 and set(certificate["closedClaims"].values()) == {"CLOSED"},
        "exactTwoFalseShortcuts": len(certificate["falseShortcuts"]) == 2 and set(certificate["falseShortcuts"].values()) == {"FALSE_IN_GENERAL"},
        "claimBoundaryFailClosed": all(value is False for value in certificate["claimBoundary"].values()),
        "graphRationalSentinelsAgree": graph["stableAndUnstableGraphNormStrictUpper"] == [1, 20] and graph["graphProductStrictUpper"] == [1, 400],
        "finiteDiagnosticNotD0": certificate["finiteDiagnostics"]["diagnosticEndpointIsCertifiedD0"] is False,
        "finiteNoContinuumConclusion": certificate["finiteDiagnostics"]["continuumConclusion"] is False,
        "journalFigureValidatedWithQa": certificate["journalFigure"]["validationStatus"] == "passed" and certificate["journalFigure"]["visualQaStatus"] == "passed",
        "gitSealStateHonest": certificate["sealState"]["analyticSourcesAtImmutableGitCommit"] is True and certificate["sealState"]["finiteAndFigureArtifactsGitSealed"] is False and certificate["sealState"]["certificatePackageGitSealed"] is False,
        "nonlinearAndClayOpen": certificate["openClaims"]["nonlinearNavierStokes"] == "OPEN" and certificate["openClaims"]["Clay"] == "OPEN",
    }
    validation = {
        "schemaVersion": "r073f-certificate-validation-v1",
        "release": "R0.73F",
        "sourceCommit": SOURCE_COMMIT,
        "checks": checks,
        "allChecksPass": all(checks.values()),
        "claimBoundary": certificate["claimBoundary"],
    }
    (OUT / "validation.json").write_text(canonical(validation), encoding="utf-8")
    with (OUT / "progress.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"event": "certificate-validation-complete", "allChecksPass": validation["allChecksPass"]}, sort_keys=True) + "\n")
    if not validation["allChecksPass"]:
        return 2

    output_names = ("certificate.json", "independent_recompute.json", "progress.ndjson", "validation.json")
    manifest = {
        "schemaVersion": "r073f-certificate-manifest-v1",
        "release": "R0.73F",
        "created": "2026-08-30",
        "status": "validated-content-addressed-unsealed",
        "sourceCommit": SOURCE_COMMIT,
        "sourceBindingKind": "immutable Git blobs at the exact analytic source commit",
        "sourceBindings": independently_bound,
        "contentBindings": certificate["contentBindings"],
        "packageSourceBindings": [binding(OUT / name) for name in SOURCE_FILES],
        "outputBindings": [binding(OUT / name) for name in output_names],
        "inventoryPolicy": {
            "scope": "all regular files directly inside research/certificates/r073f",
            "manifestFilesExcludes": ["manifest.json", "SHA256SUMS"],
            "sha256LedgerExcludes": ["SHA256SUMS"],
            "cacheDirectoriesForbidden": True,
        },
        "files": [*SOURCE_FILES, *output_names],
        "outputs": [*output_names, "manifest.json", "SHA256SUMS"],
        "sealState": certificate["sealState"],
        "limitations": [
            "the certificate checks provenance, exact rational implications, internal ledgers, and claim boundaries; it does not machine-prove the prose operator theorem",
            "the theorem is conditional on the stated R0.73B, R0.73C, and R0.73E inputs",
            "d_diag=0.01 is not the existential analytic d0, and finite Fourier diagnostics prove no continuum assertion",
            "the theorem concerns one invariant linear row and gives no all-row or nonlinear closure",
            "graph-domain Kato transport, sharp exponent, nonlinear Navier-Stokes, and the Clay problem remain open",
        ],
    }
    (OUT / "manifest.json").write_text(canonical(manifest), encoding="utf-8")
    unexpected_dirs = [path.name for path in OUT.iterdir() if path.is_dir()]
    if unexpected_dirs:
        raise RuntimeError("certificate archive contains subdirectories: " + ", ".join(unexpected_dirs))
    ledger_files = sorted(
        (path for path in OUT.iterdir() if path.is_file() and path.name != "SHA256SUMS"),
        key=lambda path: path.name,
    )
    (OUT / "SHA256SUMS").write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in ledger_files),
        encoding="utf-8",
    )
    print(canonical({"event": "r073f-certificate-validated", "allChecksPass": True}), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
