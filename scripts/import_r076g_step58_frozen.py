#!/usr/bin/env python3
"""Import only the twelve frozen R0.76G Step 58 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R076G_STEP58_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "17b366e477c46d11b4caa5e2026381bbf08e7d62"
CORE_PARENT_COMMIT = "52ee189e3dfaa2ea0924ed44cd2e1196b2ec3a5b"
HANDOFF_COMMIT = "6f203611dc13b7343005bcab3a429b6c68b10add"
HANDOFF_PATH = "research/r076g_publication_handoff.md"
HANDOFF_SHA256 = "2f1811e02b4fc6685dd543ae9844382f3bac077df58d9bae9395f49864a2c1ea"
HANDOFF_AUDIT_PATH = "research/r076g_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "7b1230ec13b4ea894e19eef372a8816a947eda2af73262328aa7d62362f54a22"

FROZEN = {
    "research/r076g_complete_clock_central_fibre_flux_lower_bound.md": "20f32790b53f2b0f5cb39b7071bd2cda96ddb4e15f75211e1682f4ba37dd0bb2",
    "research/r076g_complete_clock_central_fibre_flux_lower_bound_primary_audit.md": "af47153c4e1f4c5749f68c3f89d7533c5d95f3c0c6f15b0c775a9e35317c807e",
    "research/r076g_report-source.md": "3aea1d04dce4987c3883c1b93bec04e714ee17b540fb6a99546d084efa326f74",
    "scripts/r076g_complete_clock_central_fibre_flux_lower_bound_fixtures.json": "32e1dcf71a77ba0d28e3924fcb7e7aeb4d2840aa08ba2b2e352bb4d20d0464af",
    "scripts/r076g_complete_clock_central_fibre_flux_lower_bound_expected.json": "0a2d3d086381029941310ae502b4cf9462e025d0c75e62dd87c07334728a6ba8",
    "scripts/r076g_complete_clock_central_fibre_flux_lower_bound_certificate.py": "0afbee1f11de12cefc85aee64cbdb8c92925ad2db33cdae8d0582b79dbc01f85",
    "scripts/r076g_complete_clock_central_fibre_flux_lower_bound_certificate_independent.rb": "ea5036ffed18ce5d1ff33addeff6086ab3603bcedf2373ca6dec7ca3e4963fa2",
    "scripts/r076g_complete_clock_central_fibre_flux_lower_bound_qa.sh": "4fdbce0ab1b3b81dd87a07d4852c9b00ba3b3e6790e714f26124aabf2784ff1e",
    "research/r076g_complete_clock_central_fibre_flux_lower_bound_certificate.json": "dcca5611f40b5de9cfcc76fccc3ed35a0219a8baedbb488574223809686c652d",
    "research/r076g_complete_clock_central_fibre_flux_lower_bound_certificate_report.md": "f77d2e636e65ff07f662adc72fa16f13ab4edb57addf8422536fa67a0b36660c",
    "research/r076g_complete_clock_central_fibre_flux_lower_bound_independent_audit.md": "c034a9d3f01e784733fd35052ec4b9574c9ee4596ad44e466d07a78773953a68",
    "research/r076g_complete_clock_central_fibre_flux_lower_bound_qa_report.md": "d12f43049dc3bf151708561a0e8129a0c49d2dd0ca470e008818763519e2ae53",
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
        "release": "R0.76G Step 58",
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
