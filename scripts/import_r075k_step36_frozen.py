#!/usr/bin/env python3
"""Import only the twelve frozen R0.75K Step 36 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075K_STEP36_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "69f3989c46f0ff09c8a20cb0c387625beae42d45"
HANDOFF_COMMIT = "b6a41917fa2b30051f7c8550d313326da128d3b9"
HANDOFF_PATH = "research/r075k_publication_handoff.md"
HANDOFF_SHA256 = "07a0b2db03bfcf9f31f418af820f805d8a10abf2f70d06a91a5628c68618e71b"
HANDOFF_AUDIT_PATH = "research/r075k_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "58d998edf141ea38672643bc97b1fb171c7512acf7d835da5ef8ca03bd042b04"

FROZEN = {
    "research/r075k_positive_majorant_high_frequency_trace_loss.md": "9282fb30eb7517853759fb835579220e0da763974d5543e2fb260ec8ca6daebf",
    "research/r075k_positive_majorant_high_frequency_trace_loss_primary_audit.md": "401f12d9a5f35646638ae08446a1177a0b0485b9bbb54206702dee9fc7e7a4a2",
    "research/r075k_report-source.md": "5a45521ecb5e85b69b077af9d4db3cbb1c52dc1b61cccf8fb3bbb9daabac7001",
    "scripts/r075k_positive_majorant_high_frequency_trace_loss_fixtures.json": "f15df9bf59d6a96151f84ae2fa11a12b3965820450fbad526d4f71f11a6f7328",
    "scripts/r075k_positive_majorant_high_frequency_trace_loss_expected.json": "5ad1107080ccf033e842521e8f985196357d6cb858f945b007a5df50c2a12d77",
    "research/r075k_positive_majorant_high_frequency_trace_loss_certificate.json": "50e278d5307a85c515f1f879e7ff38438678b709e6a18c14791c60289c5c55eb",
    "research/r075k_positive_majorant_high_frequency_trace_loss_certificate_report.md": "2dee099eabc2a3db8a9ee48cc6c4a3f2b64cbc930444268d925b0ec70a376919",
    "research/r075k_positive_majorant_high_frequency_trace_loss_independent_audit.md": "107cfbaab6f29b596f9f9a3d6808e733f63d6cf9ec0dfd7c6b391391ca4cd92a",
    "research/r075k_positive_majorant_high_frequency_trace_loss_qa_report.md": "4fb4a993a3d975a303717a98a2dc306291b9fcef4a2ac734c4d0e90273163c75",
    "scripts/r075k_positive_majorant_high_frequency_trace_loss_certificate.py": "0093790920b5ed66fac3fbc808b1ea34e311124f201d54b60d71c3bd57f44661",
    "scripts/r075k_positive_majorant_high_frequency_trace_loss_certificate_independent.rb": "9caa3aa1b3ca13ff7cc8403a352c55089809ff237c0939c42cadcd8d11e52564",
    "scripts/r075k_positive_majorant_high_frequency_trace_loss_qa.sh": "a31c9c8f566d33f169f9a6b63a77770f104b74471efd8483549544ef10095212",
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
    for commit in (SOURCE_COMMIT, HANDOFF_COMMIT):
        resolved = subprocess.check_output(
            ["git", "-C", str(SOURCE), "rev-parse", f"{commit}^{{commit}}"], text=True
        ).strip()
        if resolved != commit:
            raise SystemExit(f"frozen commit drift: {resolved}")
    if sha256(git_bytes(HANDOFF_COMMIT, HANDOFF_PATH)) != HANDOFF_SHA256:
        raise SystemExit("handoff drift")
    if sha256(git_bytes(HANDOFF_COMMIT, HANDOFF_AUDIT_PATH)) != HANDOFF_AUDIT_SHA256:
        raise SystemExit("handoff independent audit drift")
    for relative, expected in FROZEN.items():
        write_exact(relative, git_bytes(SOURCE_COMMIT, relative), expected)
    print({
        "status": "PASS",
        "release": "R0.75K Step 36",
        "source": SOURCE_COMMIT,
        "handoffCommit": HANDOFF_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "handoffAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": False,
    })


if __name__ == "__main__":
    main()
