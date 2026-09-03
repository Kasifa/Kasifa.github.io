#!/usr/bin/env python3
"""Import only the twelve frozen R0.75J Step 35 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075J_STEP35_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "6c81786ea2977234de1ebb3286334d418fa0090b"
HANDOFF_COMMIT = "af29a609b21714ad9360d511351e8388f7038ec4"
HANDOFF_PATH = "research/r075j_publication_handoff.md"
HANDOFF_SHA256 = "29a8bb1ea736e7e0d1d18d6b775aed08276da5563a2b1143dab56624723caae2"
HANDOFF_AUDIT_PATH = "research/r075j_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "1056af95444eab42b416f7dd1a64c94476e6a92b9ed7054c49f9917f20da270b"

FROZEN = {
    "research/r075j_mean_zero_adjoint_flux_obstruction.md": "960e3cbc18ac8207253a8802da215b3eac07a714ddbcc7209985f27a00c9ff4d",
    "research/r075j_mean_zero_adjoint_flux_obstruction_primary_audit.md": "f2de2d439d428ccd2885f7d3fc333496cb9753896c772a54df04622e4c52c76e",
    "research/r075j_report-source.md": "1d195b0bc6760a4458fd3b4f7d11c5c892ca259c88aa5de3b014b4986ad166ca",
    "scripts/r075j_mean_zero_adjoint_flux_obstruction_fixtures.json": "754d585bab0b194adaa3f945dc8b14950e3c078564f38dc63919cf733fcfea2c",
    "scripts/r075j_mean_zero_adjoint_flux_obstruction_expected.json": "6c32cd1ff38895c5e3b0a580ad9a5e789fc3d9d8e672ba6644dceeb29befe5b8",
    "research/r075j_mean_zero_adjoint_flux_obstruction_certificate.json": "79e1fe204992b86f495c6d9c2f77084714ad905844776019befc2cc0c0577fd4",
    "research/r075j_mean_zero_adjoint_flux_obstruction_certificate_report.md": "ac258fd160fd1c9a9d96b4daebd8d4ce56df0c47d1fc667b8387347801f1629f",
    "research/r075j_mean_zero_adjoint_flux_obstruction_independent_audit.md": "945be036b61a9682c31e18e3502ddedc4947b2caae2ee5b1c40927bd62bf638c",
    "research/r075j_mean_zero_adjoint_flux_obstruction_qa_report.md": "ca26acda3a20d3e641d1cf0d859382bb726e893f389494eaacd4402c78466895",
    "scripts/r075j_mean_zero_adjoint_flux_obstruction_certificate.py": "390964c4116ece9002114d399b2c715fc7835cf7407f3788c426bc6c1d6b7d1f",
    "scripts/r075j_mean_zero_adjoint_flux_obstruction_certificate_independent.rb": "d84e7997c08f4ca11f88072217f7b0117bf1bd78db07fdc558a4e47e595f8147",
    "scripts/r075j_mean_zero_adjoint_flux_obstruction_qa.sh": "66b6bbe3ba5efc3ffc4d89fc733f36bd32f198574ab2131da332ac7fb4209a3b",
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
        "release": "R0.75J Step 35",
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
