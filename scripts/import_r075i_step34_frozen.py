#!/usr/bin/env python3
"""Import only the twelve frozen R0.75I Step 34 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075I_STEP34_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "066ebe8007518eae2d542a7a3729541677cedcd8"
HANDOFF_COMMIT = "25b06bb84190d2c29748881ac1af2bb56e929565"
HANDOFF_PATH = "research/r075i_publication_handoff.md"
HANDOFF_SHA256 = "0ce777ed11fc98e3aa87c6c8ae7decb8802312c354da934271474f6a4d0f8795"
HANDOFF_AUDIT_PATH = "research/r075i_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "fb018ed2684dc4b7ccc96565c36a0b34fa0da15aeb3724ff8942fd1d83188441"

FROZEN = {
    "research/r075i_diffusion_safe_block_participation.md": "c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7",
    "research/r075i_diffusion_safe_block_participation_primary_audit.md": "a8e481bfa28ba244a6022b782880ce9a86c40de29e3b0064474841eca99cecbd",
    "research/r075i_report-source.md": "8459adb6735caa2ee6c6e9c27202125cda34ad9072e2d78167f3f961e34f5de3",
    "scripts/r075i_diffusion_safe_block_participation_fixtures.json": "afda306afcf26640be72978b654a1a7dd1b23c0df5e92137f450520a6c7d515b",
    "scripts/r075i_diffusion_safe_block_participation_expected.json": "27514a38beec5c5e949a2a639faa5db539a4fbdeefec175e9e6e90a0507afd2a",
    "research/r075i_diffusion_safe_block_participation_certificate.json": "fc31d5b56d7d651885116d9624258075173e78476d8a173f99a20f2a5197f027",
    "research/r075i_diffusion_safe_block_participation_certificate_report.md": "dd775b48be540c91619b9e2254f0f93ef297e513f6a99beb9d63ba393dedfc3b",
    "research/r075i_diffusion_safe_block_participation_independent_audit.md": "e23174aa885311d07a097cdf9d8f571d0d6d1f59f33bdb6e4ceafb0ab4f5e4b2",
    "research/r075i_diffusion_safe_block_participation_qa_report.md": "5907f5dbf95d216bc5a2ac7bfbe989a8ae23f3509ed2570a0c38907e50ec01fb",
    "scripts/r075i_diffusion_safe_block_participation_certificate.py": "a9e006ee41fcb818bf8403f60efceb0fd08e62c42e5973065d853967ae7218df",
    "scripts/r075i_diffusion_safe_block_participation_certificate_independent.rb": "f4b3ceb0534a4bbd4861fd441accfaeb95374d5e9d91682b7fb66462519c73d0",
    "scripts/r075i_diffusion_safe_block_participation_qa.sh": "a24faf1abe00423f5c1e245efddcad59c4876989a671a19cee8066aed6f06e7e",
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
        "release": "R0.75I Step 34",
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
