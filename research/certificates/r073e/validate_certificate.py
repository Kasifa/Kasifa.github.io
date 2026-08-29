#!/usr/bin/env python3
"""Compare the two R0.73E paths and seal manifest and checksums."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "research/certificates/r073e"
SOURCE_COMMIT = "803279d72c24a54db27c40dcdad97593636788fc"
SOURCE_PATHS = (
    "research/r073e_problem_freeze.md", "research/r073e_halfplane_transfer_proof.md",
    "research/r073e_independent_analytic_audit.md", "research/r073e_literature_audit.md",
    "research/r073e_gap_matrix.md", "research/r073e_report-source.md",
    "experiments/r073e/README.md", "experiments/r073e/command.txt",
    "experiments/r073e/environment.json", "experiments/r073e/requirements.txt",
    "experiments/r073e/diagnose_complement.py", "experiments/r073e/complement_diagnostic.json",
    "experiments/r073e/progress.ndjson", "experiments/r073e/independent_validate.py",
    "experiments/r073e/independent_validation.json", "experiments/r073e/SHA256SUMS",
    "figures/r073e/fig-r073e-complement-transfer/manifest.json",
    "figures/r073e/fig-r073e-complement-transfer/validation.json",
)
PACKAGE_PATHS = (
    "research/certificates/r073e/README.md", "research/certificates/r073e/command.txt",
    "research/certificates/r073e/environment.txt", "research/certificates/r073e/generate_certificate.py",
    "research/certificates/r073e/independent_recompute.py", "research/certificates/r073e/validate_certificate.py",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(relative: str) -> dict[str, object]:
    path = ROOT / relative
    working = path.read_bytes()
    committed = subprocess.check_output(["git", "show", f"{SOURCE_COMMIT}:{relative}"], cwd=ROOT)
    if committed != working:
        raise RuntimeError(f"source changed after source commit: {relative}")
    blob = subprocess.check_output(["git", "rev-parse", f"{SOURCE_COMMIT}:{relative}"], cwd=ROOT, text=True).strip()
    return {"path": relative, "commit": SOURCE_COMMIT, "gitBlob": blob, "sha256": sha256(path), "bytes": len(working), "workingTreeBytesMatch": True}


def file_binding(relative: str) -> dict[str, object]:
    path = ROOT / relative
    return {"path": relative, "sha256": sha256(path), "bytes": len(path.read_bytes())}


def main() -> int:
    certificate = json.loads((OUT / "certificate.json").read_text())
    independent = json.loads((OUT / "independent_recompute.json").read_text())
    closed = certificate["closedClaims"]
    open_claims = certificate["openClaims"]
    checks = {
        "sourceCommitAgreement": certificate["sourceCommit"] == independent["sourceCommit"] == SOURCE_COMMIT,
        "primaryAllChecksPass": all(certificate["checks"].values()),
        "independentAllChecksPass": independent["allChecksPass"] is True and all(independent["checks"].values()),
        "exactNineClosed": len(closed) == 9 and set(closed.values()) == {"CLOSED"},
        "exactSeventeenOpen": len(open_claims) == 17 and set(open_claims.values()) == {"OPEN"},
        "claimBoundaryMatchesOpenClaims": certificate["claimBoundary"] == {name: False for name in open_claims},
        "profileDriftSentinelAgreement": certificate["analyticSentinels"]["profileDriftBound"] == independent["exactSentinels"]["profileDriftBound"] == [49, 4],
        "finiteOnlyFailClosed": certificate["finiteDiagnostics"]["continuumConclusion"] is False and independent["claimBoundary"]["continuumSpectrumCertified"] is False,
        "formalFigurePass": certificate["formalFigure"]["status"] == "formal" and certificate["formalFigure"]["validationStatus"] == "passed",
        "nonlinearFailClosed": certificate["claimBoundary"]["nonlinearNavierStokes"] is False,
        "clayFailClosed": certificate["claimBoundary"]["Clay"] is False,
        "sourceBindingInventoryExact": [row["path"] for row in certificate["sourceBindings"]] == list(SOURCE_PATHS),
    }
    validation = {
        "schemaVersion": "r073e-certificate-validation-v1",
        "release": "R0.73E",
        "sourceCommit": SOURCE_COMMIT,
        "checks": checks,
        "allChecksPass": all(checks.values()),
    }
    (OUT / "validation.json").write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n")
    if not validation["allChecksPass"]:
        return 2

    source_bindings = [binding(path) for path in SOURCE_PATHS]
    if source_bindings != certificate["sourceBindings"]:
        raise RuntimeError("certificate source bindings differ from independently recomputed bindings")
    output_names = ("certificate.json", "independent_recompute.json", "validation.json", "progress.ndjson")
    manifest = {
        "schemaVersion": "r073e-certificate-manifest-v1",
        "release": "R0.73E",
        "created": "2026-08-30",
        "sourceCommit": SOURCE_COMMIT,
        "sourceBindingKind": "exact Git commit blobs and byte-identical working sources",
        "sourceBindings": source_bindings,
        "packageBindings": [file_binding(path) for path in PACKAGE_PATHS],
        "outputBindings": [file_binding(f"research/certificates/r073e/{name}") for name in output_names],
        "outputs": [*output_names, "manifest.json", "SHA256SUMS"],
        "limitations": [
            "the theorem is uniform only on each fixed half-plane Re z >= b > 0",
            "the certified sigma-star is not proved to be the rightmost or a simple eigenvalue",
            "the moving-profile lower bound does not prove a moving evolution dichotomy or a fixed-window exponential law",
            "finite Fourier diagnostics and the formal figure prove no continuum spectral or continuous-time statement",
            "the complete OS-Squire A2 direct sum, nonlinear Navier-Stokes problem, and Clay problem remain open",
        ],
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    ledger_names = (*output_names, "manifest.json")
    (OUT / "SHA256SUMS").write_text("".join(f"{sha256(OUT / name)}  {name}\n" for name in ledger_names))
    print(json.dumps({"event": "certificate-validated", "allChecksPass": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
