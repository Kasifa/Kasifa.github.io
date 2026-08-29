#!/usr/bin/env python3
"""Compare the two R0.73D certificate paths and seal the manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "research/certificates/r073d"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(commit: str, relative: str) -> dict[str, object]:
    path = ROOT / relative
    committed = subprocess.check_output(["git", "show", f"{commit}:{relative}"], cwd=ROOT)
    working = path.read_bytes()
    if committed != working:
        raise RuntimeError(f"source changed after sealing commit: {relative}")
    blob = subprocess.check_output(
        ["git", "rev-parse", f"{commit}:{relative}"], cwd=ROOT, text=True
    ).strip()
    return {
        "path": relative,
        "commit": commit,
        "gitBlob": blob,
        "sha256": sha256(path),
        "bytes": len(working),
        "workingTreeBytesMatch": True,
    }


def main() -> int:
    certificate = json.loads((OUT / "certificate.json").read_text())
    independent = json.loads((OUT / "independent_recompute.json").read_text())
    commit = certificate["sourceCommit"]
    checks = {
        "sourceCommitAgreement": independent["sourceCommit"] == commit,
        "primaryAllChecksPass": all(certificate["checks"].values()),
        "independentAllChecksPass": independent["allChecksPass"] is True,
        "commutatorSentinel": independent["exactSentinels"]["commutatorFourierL1Sum"] == [1, 1],
        "compactBoundSentinel": independent["exactSentinels"]["roughCompactTermBound"] == [4, 1],
        "staticStatusClosed": certificate["theorem"]["staticVanishingViscosityPersistence"] == "CLOSED",
        "projectionStatusClosed": certificate["theorem"]["fixedClusterRieszProjectionNormConvergence"] == "CLOSED",
        "fastTimeFailClosed": certificate["claimBoundary"]["logFastTimeTransfer"] is False,
        "nonlinearFailClosed": certificate["claimBoundary"]["nonlinearNavierStokes"] is False,
        "clayFailClosed": certificate["claimBoundary"]["clayProblemSolved"] is False,
    }
    validation = {
        "schemaVersion": "r073d-certificate-validation-v1",
        "release": "R0.73D",
        "sourceCommit": commit,
        "checks": checks,
        "allChecksPass": all(checks.values()),
    }
    (OUT / "validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n"
    )
    if not validation["allChecksPass"]:
        return 2

    source_paths = [
        "research/r073d_problem_freeze.md",
        "research/r073d_viscous_persistence_proof.md",
        "research/r073d_independent_analytic_audit.md",
        "research/r073d_literature_audit.md",
        "research/r073d_gap_matrix.md",
        "research/r073d_report-source.md",
        "research/r073d_viscous_cluster_diagnostic.py",
        "experiments/r073d/README.md",
        "experiments/r073d/command.txt",
        "experiments/r073d/environment.json",
        "experiments/r073d/requirements.txt",
        "experiments/r073d/viscous_cluster_diagnostic.json",
        "experiments/r073d/progress.ndjson",
        "experiments/r073d/independent_validate.py",
        "experiments/r073d/independent_validation.json",
        "research/certificates/r073d/generate_certificate.py",
        "research/certificates/r073d/independent_recompute.py",
        "research/certificates/r073d/validate_certificate.py",
        "research/certificates/r073d/README.md",
        "research/certificates/r073d/command.txt",
        "research/certificates/r073d/environment.txt",
    ]
    output_names = [
        "certificate.json",
        "independent_recompute.json",
        "validation.json",
        "progress.ndjson",
    ]
    manifest = {
        "schemaVersion": "r073d-certificate-manifest-v1",
        "release": "R0.73D",
        "created": "2026-08-30",
        "sourceCommit": commit,
        "sourceBindingKind": "exact Git commit blobs and byte-identical working sources",
        "sourceBindings": [binding(commit, path) for path in source_paths],
        "outputBindings": [
            {
                "path": f"research/certificates/r073d/{name}",
                "sha256": sha256(OUT / name),
                "bytes": len((OUT / name).read_bytes()),
            }
            for name in output_names
        ],
        "outputs": output_names + ["manifest.json", "SHA256SUMS"],
        "limitations": [
            "the isolating radius and viscosity threshold are existential",
            "the inviscid algebraic multiplicity is not identified",
            "finite Fourier rows are diagnostics only",
            "the whole right-half-plane complement and fast-time transfer remain open",
            "no nonlinear Navier-Stokes or Clay conclusion is claimed",
        ],
    }
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    checksum_names = output_names + ["manifest.json"]
    (OUT / "SHA256SUMS").write_text(
        "".join(f"{sha256(OUT / name)}  {name}\n" for name in checksum_names)
    )
    print(json.dumps({"event": "certificate-validated", "allChecksPass": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
