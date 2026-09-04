#!/usr/bin/env python3
"""Import only the twelve frozen R0.75Y Step 50 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075Y_STEP50_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "cb150f97a6c2595066360c0d4c6aca3c4062bdbe"
CORE_PARENT_COMMIT = "4d12592f991e2cbb7db65f5470579783c2791fab"
HANDOFF_PATH = "research/r075y_publication_handoff.md"
HANDOFF_SHA256 = "945d918d54b0309c340b8aa3048e0ddd2f624c302eb687331b8a9312807a1c17"
HANDOFF_AUDIT_PATH = "research/r075y_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "327cefd9cefe0c1878c5f5b2b4ba96105e2a1b0376a23a29cb8d3acb65ee0763"

FROZEN = {
    "research/r075y_strongly_separated_multimode_flux_payment.md": "74790f910b596c86b204291d997ef723cabbc85d14a89e3fe900814fcd88b0a6",
    "research/r075y_strongly_separated_multimode_flux_payment_primary_audit.md": "f7e1feedd1fa359877554eff4fa20c470f727ae7743c990136525ad22d6cdf3b",
    "research/r075y_report-source.md": "e6d6b1ed2830b46fc901a9ab09ef368f258f13dfc8c0961076baedd5b46e1589",
    "scripts/r075y_strongly_separated_multimode_flux_payment_fixtures.json": "45448bf75c867b3f9654db79c77ae52b9bd35d7e781b240f564a9d871faab32b",
    "scripts/r075y_strongly_separated_multimode_flux_payment_expected.json": "324e92dd32d6e1ca76b22c47a201206e1c924e1100b92de1c8429ffd17ac25d3",
    "scripts/r075y_strongly_separated_multimode_flux_payment_certificate.py": "126e97f7d248c7d5516b927816fed3cb3269b59fd2d0def3ec410d4502e7d078",
    "scripts/r075y_strongly_separated_multimode_flux_payment_certificate_independent.rb": "69c1dfdd9149fc89a0c14407a9373f03e418cfd0b3c5b2fda1d9a96261141e70",
    "scripts/r075y_strongly_separated_multimode_flux_payment_qa.sh": "dc73c406ac40d6b64f7f9164cf0d4cf494bbb3eddc31ff5f69a662da00316517",
    "research/r075y_strongly_separated_multimode_flux_payment_certificate.json": "2c74a9bf2bd9b1f24dd66fdc330bd4dd814d63ec1bce36e7efa1e337cfa4fdfe",
    "research/r075y_strongly_separated_multimode_flux_payment_certificate_report.md": "cd3b1bf9aff7b326c92a1e40a0f3ae0fc363e734be7d859e6a7d6c62fae7a0a7",
    "research/r075y_strongly_separated_multimode_flux_payment_independent_audit.md": "e45e30a34253905b24acafdf18b9dfcf3d6ffd6163cd38996a1c4991335c8d21",
    "research/r075y_strongly_separated_multimode_flux_payment_qa_report.md": "f2a49eafe9317aba8bdb582b4f0e0852e8cb7603fb8a415ec3df78ed5be5e67a",
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
        "release": "R0.75Y Step 50",
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
