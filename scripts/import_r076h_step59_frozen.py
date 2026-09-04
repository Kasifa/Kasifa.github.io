#!/usr/bin/env python3
"""Import only the twelve frozen R0.76H Step 59 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R076H_STEP59_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "6f3ea9599de24902d6ddbfdcc45d1df7614fe31e"
CORE_PARENT_COMMIT = "6f203611dc13b7343005bcab3a429b6c68b10add"
HANDOFF_COMMIT = "8626f085f3220a79d19816ec220eacc8909971cc"
HANDOFF_PATH = "research/r076h_publication_handoff.md"
HANDOFF_SHA256 = "cb89fc65dcfdddcc816c958fca207e8cc75e45f0963aaef79837ca7d6870c2ca"
HANDOFF_AUDIT_PATH = "research/r076h_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "930404041d4b32b5eeac858ed92016ecc4f4b8f7287ec5ffa695bb877cd6b7b6"

FROZEN = {
    "research/r076h_full_plateau_absorption_for_shifted_packet.md": "11490112a1893400a1099dd9f45b906ce78d7dab1ebcf549eaa7870241dc0ef4",
    "research/r076h_full_plateau_absorption_for_shifted_packet_primary_audit.md": "91e1f31f3adf19a9f352a8cd6defc8988971e51f0905e4a634f949223992c58d",
    "research/r076h_report-source.md": "3e706ae12caace1118f941f92c85bc0a1a11ed4a6e158acf7258918a67616d87",
    "scripts/r076h_full_plateau_absorption_for_shifted_packet_fixtures.json": "035ff9b04f61c11744668c51e6fd8ef1e35da93de85fab2bd9b971acca79747d",
    "scripts/r076h_full_plateau_absorption_for_shifted_packet_expected.json": "f80cc1d8b6673a6f18069d6756f605de821ac661561d11295a40c468532e083b",
    "scripts/r076h_full_plateau_absorption_for_shifted_packet_certificate.py": "65cd03fa1420eaffbf1a0e795d178b13b46829f79811963a724f2c25a9c72b2f",
    "scripts/r076h_full_plateau_absorption_for_shifted_packet_certificate_independent.rb": "4b1d72ad23b82eb48eef6df96d98bb904aa8f72e4932724ac72557c881c46cb3",
    "scripts/r076h_full_plateau_absorption_for_shifted_packet_qa.sh": "eea1b5f41b4c3959d1bdab214dc4c3b07fa05a0ca0f9a659c7ed8fa4fc565a02",
    "research/r076h_full_plateau_absorption_for_shifted_packet_certificate.json": "452e46b75a10d7fcb637d85234e1d3f76c471cd4ea1cec6b69b568260a8ff55e",
    "research/r076h_full_plateau_absorption_for_shifted_packet_certificate_report.md": "d9c80bc4af24f7f55046e2b5d13484841d3c430232c586913c10b23cbd425267",
    "research/r076h_full_plateau_absorption_for_shifted_packet_independent_audit.md": "f3d301f7b29cd1d5ceb89604d4b14d306e3f1fb47c35a5cce1cd689fc8b16fbd",
    "research/r076h_full_plateau_absorption_for_shifted_packet_qa_report.md": "bff6f11944ce50a875ad5395576b55a0d777f2df41a61f969558c755732cb54c",
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
    handoff_parent = subprocess.check_output(
        ["git", "-C", str(SOURCE), "rev-parse", f"{HANDOFF_COMMIT}^"], text=True
    ).strip()
    if handoff_parent != SOURCE_COMMIT:
        raise SystemExit(f"handoff parent drift: {handoff_parent}")
    if sha256(git_bytes(HANDOFF_COMMIT, HANDOFF_PATH)) != HANDOFF_SHA256:
        raise SystemExit("handoff drift")
    if sha256(git_bytes(HANDOFF_COMMIT, HANDOFF_AUDIT_PATH)) != HANDOFF_AUDIT_SHA256:
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
        "release": "R0.76H Step 59",
        "source": SOURCE_COMMIT,
        "coreParentCommit": CORE_PARENT_COMMIT,
        "handoffCommit": HANDOFF_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "handoffIndependentAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": False,
    })


if __name__ == "__main__":
    main()
