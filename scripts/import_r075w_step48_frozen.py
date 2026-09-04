#!/usr/bin/env python3
"""Import only the twelve frozen R0.75W Step 48 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075W_STEP48_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "e8e48a510db0c0ed86626c238e4c81c281bcc998"
CORE_PARENT_COMMIT = "038abd31f55795198ed8bebd9ba96823337c1621"
HANDOFF_PATH = "research/r075w_publication_handoff.md"
HANDOFF_SHA256 = "8fa54b5d2bea00d24d53ab8cfde2693df41c0c1f7d66428ba575a26e53366aee"
HANDOFF_AUDIT_PATH = "research/r075w_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "8e700fd1647fca55168ad341f50a34379f62bb977a473c738323b059a77c1e54"

FROZEN = {
    "research/r075w_full_frequency_two_harmonic_flux_payment.md": "571b8152e3e5f81becec4dd691488fb5889fac23e94ca7c99bd546399dc320d4",
    "research/r075w_full_frequency_two_harmonic_flux_payment_primary_audit.md": "78255a0d84020d1d1c9dc6509ed1cc8eb9a9fdaced21d93e4f586383e4fc9ea0",
    "research/r075w_report-source.md": "461ab29f02072eb039c9b57c497a87d04ff95255af68d561c68f4d3224726d7a",
    "scripts/r075w_full_frequency_two_harmonic_flux_payment_fixtures.json": "2b59973a6901b0a70068a2952e1324fd1780f853508c250821daaab659aa8b1f",
    "scripts/r075w_full_frequency_two_harmonic_flux_payment_expected.json": "44afc8aebea8e15a4d54adf28fd48f8da28dd61c74e6f87a9ded21667d61867f",
    "scripts/r075w_full_frequency_two_harmonic_flux_payment_certificate.py": "7d517b429fa0d08f5f2fc61597eb926b12d72fe5543444ea9e4a49094d89a29f",
    "scripts/r075w_full_frequency_two_harmonic_flux_payment_certificate_independent.rb": "3ecd32cb10eb29f84220fd0110556071bc9637ef06457577291931173bc1e9c4",
    "scripts/r075w_full_frequency_two_harmonic_flux_payment_qa.sh": "3090e129431c03f43fd7aa518d9abe0f6ce74af3e97f50b2c19c65497d1d711a",
    "research/r075w_full_frequency_two_harmonic_flux_payment_certificate.json": "cd18eca477eb0938703446c6ab9939b4bccaf1f3465e450dfa35cdee758b76c8",
    "research/r075w_full_frequency_two_harmonic_flux_payment_certificate_report.md": "5b5fc6efb2de3e5817c7299cf2b71b3df15eca8caf393e8ccbc85a4796d08284",
    "research/r075w_full_frequency_two_harmonic_flux_payment_independent_audit.md": "0e7462c2912bb4be6c63198692014d753d9f57bced48e65543c53e25193315aa",
    "research/r075w_full_frequency_two_harmonic_flux_payment_qa_report.md": "2a6f0b9171b2e1511519510d732c6c4c032fd877e4aa44be480bdc54d799793b",
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
        "release": "R0.75W Step 48",
        "source": SOURCE_COMMIT,
        "coreParentCommit": CORE_PARENT_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "handoffIndependentAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": True,
    })


if __name__ == "__main__":
    main()
