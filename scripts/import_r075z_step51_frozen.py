#!/usr/bin/env python3
"""Import only the twelve frozen R0.75Z Step 51 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075Z_STEP51_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "85e633132cbcde89ec78bfef465f3c0393c27994"
CORE_PARENT_COMMIT = "d1d9f261425804ecb53aa99ddb56705c87267c24"
HANDOFF_PATH = "research/r075z_publication_handoff.md"
HANDOFF_SHA256 = "295af460aa6f15624a1d41adeeb6c0974acb3ee4f2c194f47777755d41c7b639"
HANDOFF_AUDIT_PATH = "research/r075z_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "8aa60590a884f4be7ac85167f693420a934bc3e57d3ce4a8a7571088ab53d6ab"

FROZEN = {
    "research/r075z_unresolved_cluster_carrier_current_gate.md": "30d2811e8747aa2b40b4787e6f169af19d1381b66fc84610327da221168f3d97",
    "research/r075z_unresolved_cluster_carrier_current_gate_primary_audit.md": "895d09e0b403c0a6bcf216624527dd6c2bf76f15d7ce5f6b6b0a31b6f64a1eb0",
    "research/r075z_report-source.md": "9b071b3e020210922834435ea7e5806620479d400eb044f48f34e7b02c259d4c",
    "scripts/r075z_unresolved_cluster_carrier_current_gate_fixtures.json": "9bd703f41f4b4823a4b6fe38136bf2a5bef126cf15edb3b54036cf1b80e4f4b0",
    "scripts/r075z_unresolved_cluster_carrier_current_gate_expected.json": "6043f94b70b6068a58d7716877a5319edc9edfc90b47bfee23ea7baee0ad58d4",
    "scripts/r075z_unresolved_cluster_carrier_current_gate_certificate.py": "dce8afaee87120d042a046d220aeca5f345cb38d42e306d70f89a8fb211252a1",
    "scripts/r075z_unresolved_cluster_carrier_current_gate_certificate_independent.rb": "d4d1cc3445694b6eaac4857d812f9272e9a8214efce11e212d0d03f049d86578",
    "scripts/r075z_unresolved_cluster_carrier_current_gate_qa.sh": "6c5f50401ee0e77253f7b6df8b9e5802fac70e756b497457201d602645e5a1da",
    "research/r075z_unresolved_cluster_carrier_current_gate_certificate.json": "116b2f4a6bf343f602c3c624b1eac550449162aa43d7e4038e886ba2bbf7b839",
    "research/r075z_unresolved_cluster_carrier_current_gate_certificate_report.md": "861d4585b9969bc10d779552ccd0318e71a92700aa7c0c017e8d2e8fbfbd9163",
    "research/r075z_unresolved_cluster_carrier_current_gate_independent_audit.md": "9bffb2446e7d2fd5d85628f15079265e0e94252a61c430c59642a016dda6574c",
    "research/r075z_unresolved_cluster_carrier_current_gate_qa_report.md": "0e9e4286ac132a88f47675869ceb55c5c491ceb6c9a16bd6d6511b3bf9ba1f12",
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
    for commit in (SOURCE_COMMIT, CORE_PARENT_COMMIT):
        resolved = subprocess.check_output(
            ["git", "-C", str(SOURCE), "rev-parse", f"{commit}^{{commit}}"], text=True
        ).strip()
        if resolved != commit:
            raise SystemExit(f"frozen commit drift: {resolved}")
    core_parent = subprocess.check_output(
        ["git", "-C", str(SOURCE), "rev-parse", f"{SOURCE_COMMIT}^"], text=True
    ).strip()
    if core_parent != CORE_PARENT_COMMIT:
        raise SystemExit(f"core parent drift: {core_parent}")
    if sha256((SOURCE / HANDOFF_PATH).read_bytes()) != HANDOFF_SHA256:
        raise SystemExit("handoff drift")
    if sha256((SOURCE / HANDOFF_AUDIT_PATH).read_bytes()) != HANDOFF_AUDIT_SHA256:
        raise SystemExit("handoff independent-audit drift")
    changed = subprocess.check_output(
        ["git", "-C", str(SOURCE), "show", "--pretty=format:", "--name-only", SOURCE_COMMIT], text=True
    ).split()
    if set(changed) != set(FROZEN) or len(changed) != len(FROZEN):
        raise SystemExit("core changed-path whitelist drift")
    for relative, expected in FROZEN.items():
        write_exact(relative, git_bytes(SOURCE_COMMIT, relative), expected)
    print({
        "status": "PASS",
        "release": "R0.75Z Step 51",
        "source": SOURCE_COMMIT,
        "coreParentCommit": CORE_PARENT_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "handoffIndependentAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": False,
    })


if __name__ == "__main__":
    main()
