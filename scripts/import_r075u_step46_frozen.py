#!/usr/bin/env python3
"""Import only the twelve frozen R0.75U Step 46 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075U_STEP46_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "4bc33028aa27e6f47fb3464022a500556f3e34e4"
HANDOFF_COMMIT = "73bcc4cd928370a7355b88f953e96082c58ebf69"
CORE_PARENT_COMMIT = "a7d599bf9068f346e4d02c4bfce8324e2f4a823a"
HANDOFF_PATH = "research/r075u_publication_handoff.md"
HANDOFF_SHA256 = "33ae9d6d7d5b10aa5878e2b9e24c2f2f8bf1c5b1b668874dcac35d8e5cacf653"
HANDOFF_AUDIT_PATH = "research/r075u_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "6991ed0b3d0d3ca4db923f9b816dd91a2adc196f61de88fb10461c5708889259"

FROZEN = {
    "research/r075u_two_harmonic_difference_frequency_payment.md": "f9fb331cf880b20f3b407fe66453bce71517ac1ef2af4fa0863c00325c1022a4",
    "research/r075u_two_harmonic_difference_frequency_payment_primary_audit.md": "3687decf19ff49016e101a174d066b355689dcca7a4dc36a941b84994b118d6a",
    "research/r075u_report-source.md": "d0e9356a162b683a33c5b4c49692a62962d2a9c63cccba9eb9d84040aaf4a01f",
    "scripts/r075u_two_harmonic_difference_frequency_payment_fixtures.json": "c654b79a1b3b69078df01000c43fee54fdff39ea64c7bc47e206b114dc20b0c6",
    "scripts/r075u_two_harmonic_difference_frequency_payment_expected.json": "381e80ca54eee51fb3aab823837f0bfdc28e84353e02c8f41fceed261d6aec12",
    "scripts/r075u_two_harmonic_difference_frequency_payment_certificate.py": "040474723e1380ac6983c1fe165b910aa94751f7b8884cb7d015848d990a77a3",
    "scripts/r075u_two_harmonic_difference_frequency_payment_certificate_independent.rb": "77f2b4a6bbf389c54694dfdbf8759264ed10c89cfa2e9d085378f084810f263b",
    "scripts/r075u_two_harmonic_difference_frequency_payment_qa.sh": "26ab61750ecb1bfb5961479543fe32bc2338ae0bccfcf7c977cc26f71165c318",
    "research/r075u_two_harmonic_difference_frequency_payment_certificate.json": "87e6eb73c58a695a88ddc81948ddfea8257cb3844a1e4412068c28985ee28f5a",
    "research/r075u_two_harmonic_difference_frequency_payment_certificate_report.md": "3d0774651733e2f803cf3b679a0c8ba36a50029a27e88366c5d8bee2344d8b0d",
    "research/r075u_two_harmonic_difference_frequency_payment_independent_audit.md": "659dacda5aa67c502b3b6db315d06e9aed8cf4aa8fcd06aa45967b8de57950f8",
    "research/r075u_two_harmonic_difference_frequency_payment_qa_report.md": "180b9301689a510544c8a4b3bf74c3625767cd9f89cb84c4069c1cd56ea8132e",
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
    for commit in (SOURCE_COMMIT, HANDOFF_COMMIT, CORE_PARENT_COMMIT):
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
    if sha256(git_bytes(HANDOFF_COMMIT, HANDOFF_PATH)) != HANDOFF_SHA256:
        raise SystemExit("handoff drift")
    if sha256(git_bytes(HANDOFF_COMMIT, HANDOFF_AUDIT_PATH)) != HANDOFF_AUDIT_SHA256:
        raise SystemExit("handoff independent-audit drift")
    parent = subprocess.check_output(
        ["git", "-C", str(SOURCE), "rev-parse", f"{HANDOFF_COMMIT}^"], text=True
    ).strip()
    if parent != SOURCE_COMMIT:
        raise SystemExit(f"handoff parent drift: {parent}")
    changed = subprocess.check_output(
        ["git", "-C", str(SOURCE), "show", "--pretty=format:", "--name-only", SOURCE_COMMIT], text=True
    ).split()
    if set(changed) != set(FROZEN):
        raise SystemExit("core changed-path whitelist drift")
    for relative, expected in FROZEN.items():
        write_exact(relative, git_bytes(SOURCE_COMMIT, relative), expected)
    print({
        "status": "PASS",
        "release": "R0.75U Step 46",
        "source": SOURCE_COMMIT,
        "handoffCommit": HANDOFF_COMMIT,
        "coreParentCommit": CORE_PARENT_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "handoffIndependentAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": False,
    })


if __name__ == "__main__":
    main()
