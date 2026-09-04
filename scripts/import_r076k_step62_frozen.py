#!/usr/bin/env python3
"""Import only the twelve frozen R0.76K Step 62 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R076K_STEP62_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "8a89aee4fe0839de44e21a90ba827a9cc77b3062"
CORE_PARENT_COMMIT = "8b3b67c9f9d1e796f6a1bbd8639ab25d80ed0470"
HANDOFF_COMMIT = "17bec49703836115f2e8a32a4bae516071433902"
HANDOFF_PATH = "research/r076k_publication_handoff.md"
HANDOFF_SHA256 = "e178c96e3041877d2c436ae33f12b2671d4366cad711eb9b3e1f18381aecc4d3"
HANDOFF_AUDIT_PATH = "research/r076k_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "e7afdedbd19c687afc8a32d4ab51d2765e92407ebb2d1a97112e081201253869"

FROZEN = {
    "research/r076k_real_dyadic_edge_sharpness.md": "e293a3aa3e9c1dde443ed7a8c07afd2c709d3855d8b469b38033b04d71116bf2",
    "research/r076k_real_dyadic_edge_sharpness_primary_audit.md": "36a26cb421a108127b516e47a0008625d67ec43a1d009a14bef9d7684ef03671",
    "research/r076k_report-source.md": "21dbd71aae07ecbe910d4bcefbf6e1caccc3cddc41171a57ffd239c6eed34f3e",
    "scripts/r076k_real_dyadic_edge_sharpness_fixtures.json": "16acf468a6722ee1e66e36a855fdd1e84e56bdc3519e6e2326d6bec0a3b82518",
    "scripts/r076k_real_dyadic_edge_sharpness_expected.json": "8f32d96856fdf5d0a86030737f5bf049b227f976661089ed6d31d4a41a1c5b50",
    "scripts/r076k_real_dyadic_edge_sharpness_certificate.py": "c05ab480973a418e69cb40984b1da5c7210c5e4916e2fa1d6fb6281a9b53d1d9",
    "scripts/r076k_real_dyadic_edge_sharpness_certificate_independent.rb": "893b0b5e18e3a3fca06ef10e7879e361894dafbb845d09264373e92f116210bb",
    "scripts/r076k_real_dyadic_edge_sharpness_qa.sh": "5968f4b6a08d982c4345165e7fc0bc04c33dca66ab7cf8c1dba0be30a5212a79",
    "research/r076k_real_dyadic_edge_sharpness_certificate.json": "4d5247ca82869758c01a398f9a4858bfce87e3bd7ab3ad2a37eac0e6bdea7f1d",
    "research/r076k_real_dyadic_edge_sharpness_certificate_report.md": "43131539e1fd4105fe0215739003b7819379e87d44ddab4aa772a40bcc47daaa",
    "research/r076k_real_dyadic_edge_sharpness_independent_audit.md": "7d87a4b543051e08cc6a348c5b7f261cd433fdf8efba4986ed01514c13c78b1a",
    "research/r076k_real_dyadic_edge_sharpness_qa_report.md": "b888919d4f1992c22e5206d6350983dbd89885df29bb62b3408b581298c511ec",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(commit: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(SOURCE), "show", f"{commit}:{relative}"])


def write_exact(relative: str, data: bytes, expected: str) -> None:
    if sha256(data) != expected:
        raise SystemExit(f"source hash drift: {relative}")
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    if target.read_bytes() != data:
        raise SystemExit(f"import byte drift: {relative}")


def main() -> None:
    for commit in (SOURCE_COMMIT, CORE_PARENT_COMMIT, HANDOFF_COMMIT):
        resolved = subprocess.check_output(["git", "-C", str(SOURCE), "rev-parse", f"{commit}^{{commit}}"], text=True).strip()
        if resolved != commit:
            raise SystemExit(f"frozen commit drift: {resolved}")
    if subprocess.check_output(["git", "-C", str(SOURCE), "rev-parse", f"{SOURCE_COMMIT}^"], text=True).strip() != CORE_PARENT_COMMIT:
        raise SystemExit("core parent drift")
    if subprocess.check_output(["git", "-C", str(SOURCE), "rev-parse", f"{HANDOFF_COMMIT}^"], text=True).strip() != SOURCE_COMMIT:
        raise SystemExit("handoff parent drift")
    if sha256(git_bytes(HANDOFF_COMMIT, HANDOFF_PATH)) != HANDOFF_SHA256:
        raise SystemExit("handoff drift")
    if sha256(git_bytes(HANDOFF_COMMIT, HANDOFF_AUDIT_PATH)) != HANDOFF_AUDIT_SHA256:
        raise SystemExit("handoff independent-audit drift")
    changed = subprocess.check_output(["git", "-C", str(SOURCE), "show", "--pretty=format:", "--name-only", SOURCE_COMMIT], text=True).split()
    if set(changed) != set(FROZEN) or len(changed) != len(FROZEN):
        raise SystemExit("core changed-path whitelist drift")
    for relative, expected in FROZEN.items():
        write_exact(relative, git_bytes(SOURCE_COMMIT, relative), expected)
    print({
        "status": "PASS", "release": "R0.76K Step 62", "source": SOURCE_COMMIT,
        "coreParentCommit": CORE_PARENT_COMMIT, "handoffCommit": HANDOFF_COMMIT,
        "handoffSha256": HANDOFF_SHA256, "handoffIndependentAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN), "formalFigureRequired": False, "recapRequired": False,
    })


if __name__ == "__main__":
    main()
