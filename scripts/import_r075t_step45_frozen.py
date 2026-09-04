#!/usr/bin/env python3
"""Import only the twelve frozen R0.75T Step 45 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075T_STEP45_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "985b09647f726c420593d4d7fd61b7e9d045a80d"
HANDOFF_COMMIT = "a7d599bf9068f346e4d02c4bfce8324e2f4a823a"
HANDOFF_PATH = "research/r075t_publication_handoff.md"
HANDOFF_SHA256 = "3432f8214ccd529fd50cf902d5a1cbddc5bd63b7bca8235ec779b27c2e423c0b"
HANDOFF_AUDIT_PATH = "research/r075t_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "1f461acd199a6a698035d600af0254e23a7b8de5036bb04f1c6aa471b3de19bc"

FROZEN = {
    "research/r075t_two_harmonic_collar_coercivity.md": "822059f8a6248143ff3f36938a2333bee9f909b9166db951e227c426c2e8bc66",
    "research/r075t_two_harmonic_collar_coercivity_primary_audit.md": "97d804444737284d7ec40b3ce45389272b1a9f61d1901f7bcebf9ed0eab935e5",
    "research/r075t_report-source.md": "c2255cdd07f2e490921d93ba7e62a809c0348a9e6136b7fd5537cf3799e4e8d8",
    "scripts/r075t_two_harmonic_collar_coercivity_fixtures.json": "939b04eeccb9c96b6d5cb21d49ebc48e7a8387dfccdc08afd2dfd6db77fd4393",
    "scripts/r075t_two_harmonic_collar_coercivity_expected.json": "cd58217667129d5a2f01dd2b315b86a934de1258be2eefab401f5b66efc127c5",
    "scripts/r075t_two_harmonic_collar_coercivity_certificate.py": "75e31019f8fe05d35a025e727098e99ebe4e5d8eebd60865e559456650c3a439",
    "scripts/r075t_two_harmonic_collar_coercivity_certificate_independent.rb": "24ccdc21eca83d8cff18b3ae8a7e3ab293e92e4d765fc70008c9c3ca4f4ddb25",
    "scripts/r075t_two_harmonic_collar_coercivity_qa.sh": "1be6a16dc1bf7eb10900128c3e2b10005ba530e0a168460f8a5c2a3bb19b0fb3",
    "research/r075t_two_harmonic_collar_coercivity_certificate.json": "85a78058a71b6d381edc14336c05c608719f25b88bad39add88d1e4b853b8966",
    "research/r075t_two_harmonic_collar_coercivity_certificate_report.md": "863b6af73f397691b0b7af1a21c7caadd84f29817c47742d4e8553d2209298b9",
    "research/r075t_two_harmonic_collar_coercivity_independent_audit.md": "5b4f2e9d3c68b8f408e5737f5cb7769586e9934792ab110c1626b5e7dec2b50d",
    "research/r075t_two_harmonic_collar_coercivity_qa_report.md": "96fec40029dda57bf6b3ce1a8e50616047b0c92a8462cf6e5b1776236dc837a9",
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
        raise SystemExit("handoff independent-audit drift")
    parent = subprocess.check_output(
        ["git", "-C", str(SOURCE), "rev-parse", f"{HANDOFF_COMMIT}^"], text=True
    ).strip()
    if parent != SOURCE_COMMIT:
        raise SystemExit(f"handoff parent drift: {parent}")
    for relative, expected in FROZEN.items():
        write_exact(relative, git_bytes(SOURCE_COMMIT, relative), expected)
    print({
        "status": "PASS",
        "release": "R0.75T Step 45",
        "source": SOURCE_COMMIT,
        "handoffCommit": HANDOFF_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "handoffIndependentAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": False,
    })


if __name__ == "__main__":
    main()
