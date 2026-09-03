#!/usr/bin/env python3
"""Import only the twelve frozen R0.75G Step 32 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075G_STEP32_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "b4ec164eeae4ec79be3c517da98321b62294d991"
HANDOFF_COMMIT = "8ddccdefa292d0768f8594995553af4853923833"
HANDOFF_PATH = "research/r075g_publication_handoff.md"
HANDOFF_SHA256 = "628dbe1a1e0d53d87bcf782edba1425b130269722ecded882207549c232c9d1c"
HANDOFF_AUDIT_PATH = "research/r075g_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "4bf12a10837ea83b6e37f8f0413bdd31bedbd498cbd02da4e6008a7de4b066f7"

FROZEN = {
    "research/r075g_signed_flux_gain_threshold.md": "f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41",
    "research/r075g_signed_flux_gain_threshold_primary_audit.md": "4717b365e5a4dc1bff169db51708a8a74fe51e6dd414a9a68a448813d95541aa",
    "research/r075g_report-source.md": "2722d2801945a2ee074b0a9c4a973f592849ae012ddd4c264b7fea5ad76e9896",
    "scripts/r075g_signed_flux_gain_threshold_fixtures.json": "6bcf72a52763b04f98c21109fabbd570aa552cfe472280cff7ff4a0738eb0c9a",
    "scripts/r075g_signed_flux_gain_threshold_expected.json": "03b3475a3f8e82cb986e63ef52af6fdb899ac200b70024661c379542356b6ab0",
    "research/r075g_signed_flux_gain_threshold_certificate.json": "72cf4415368aa527699b4e1d23a11ff91dc41247a0474b0bc33845f90214be32",
    "research/r075g_signed_flux_gain_threshold_certificate_report.md": "8a7d42b877481593278ffd60ac98c0ce3dd11f4f242c96db96f561f41dac8744",
    "research/r075g_signed_flux_gain_threshold_independent_audit.md": "5e33e561d9d84d2acda364fffe988a7eeee769c1a24b27d6fce01f4159c005d2",
    "research/r075g_signed_flux_gain_threshold_qa_report.md": "15e50c29f8dd007249389b7c365630349eb690da400ac01123f2d1555f8941dc",
    "scripts/r075g_signed_flux_gain_threshold_certificate.py": "c08eb7f02b49864d5f46ba4fc7f14b5f815f03fa712a0ccb373e933be6f46cee",
    "scripts/r075g_signed_flux_gain_threshold_certificate_independent.rb": "c2d11ff71dd683a15cbb97892c028b3e861e47bde5e18cedd602d9967430da3c",
    "scripts/r075g_signed_flux_gain_threshold_qa.sh": "65add9d4c0b8b6569315b1cdb7e664a91c28bc60d1204cec028d8adbbb2e9190",
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
        "release": "R0.75G Step 32",
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
