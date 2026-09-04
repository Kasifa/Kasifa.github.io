#!/usr/bin/env python3
"""Import only the twelve frozen R0.75L Step 37 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075L_STEP37_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "8eef1888735a7e08bd0e9c988e01677a197f437a"
HANDOFF_COMMIT = "cd65721cf2b8d33d4cd97edab92c87daa1daf068"
HANDOFF_PATH = "research/r075l_publication_handoff.md"
HANDOFF_SHA256 = "caafa97240fcdf52cf8fd58d120d291a13933c89d8adcb79dde655c8f76b273e"
HANDOFF_AUDIT_PATH = "research/r075l_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "e08bc86dc42014057520fb5ce97e6bd81a16a93d739fd887ec71308e27aaf4c9"

FROZEN = {
    "research/r075l_single_harmonic_diffusive_signed_flux_gain.md": "52e25b2fdf1a224609c9e8fafa1c041b7f09a361f75f4b3e44ebcdddb756cdf5",
    "research/r075l_single_harmonic_diffusive_signed_flux_gain_primary_audit.md": "a7578e5370d182decc39f0da2f2fb581e5ef842ae7b914a120b5784bc32bd302",
    "research/r075l_report-source.md": "a300de54b9fe06e94455a055bbb42bdce8ec7bb004080389a95412966a5b941a",
    "scripts/r075l_single_harmonic_diffusive_signed_flux_gain_fixtures.json": "0b9ba1f018b6e52414f20dee6687f5ff55c5ea0ef247ddbd905bc8c204245ad9",
    "scripts/r075l_single_harmonic_diffusive_signed_flux_gain_expected.json": "9178489eaf9f44c5b182b6080cce7212591b1a3dd86459ecbd82c1382b38db9a",
    "research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate.json": "318136308fb0b1e46046b6483269e70b0a2d57dc44be18616236a10c5271a567",
    "research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate_report.md": "00c490616bdb6641a862152a315ac76861ff345d8654137dea1d5fce552b2772",
    "research/r075l_single_harmonic_diffusive_signed_flux_gain_independent_audit.md": "31a67ab57a7c3f591f3e4dbd446dada04720ed62170e7cd0773123acc8d20604",
    "research/r075l_single_harmonic_diffusive_signed_flux_gain_qa_report.md": "387e80857b32e5048210b77a4a685be7a69c8f8e9f8da1514305a1ae96368e63",
    "scripts/r075l_single_harmonic_diffusive_signed_flux_gain_certificate.py": "a521194d3ab26e23ffc13450244dcd92c52ac774bfb647348ebb2fac09c2571f",
    "scripts/r075l_single_harmonic_diffusive_signed_flux_gain_certificate_independent.rb": "50888ee85e72c472881eab10145020888eda1558a7a5eb067aaaf5c61b3c307c",
    "scripts/r075l_single_harmonic_diffusive_signed_flux_gain_qa.sh": "fa336a8dad20a400494eeb0b28a91bbb5077396238d094f5bf1621e367b7a175",
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
        "release": "R0.75L Step 37",
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
