#!/usr/bin/env python3
"""Import only the twelve frozen R0.75V Step 47 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075V_STEP47_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "fc676ef2c0bf501e14c6a0e1f84558e470de6eb8"
HANDOFF_COMMIT = "038abd31f55795198ed8bebd9ba96823337c1621"
CORE_PARENT_COMMIT = "73bcc4cd928370a7355b88f953e96082c58ebf69"
HANDOFF_PATH = "research/r075v_publication_handoff.md"
HANDOFF_SHA256 = "dbfe82c22ce710fe176e3fffbc53e7b0c234d80d95afc97effc5ee9e42b87a76"
HANDOFF_AUDIT_PATH = "research/r075v_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "bfb234b1fb2cddb746df19dcd987e4554786e6e1e9e1b1d0d24d589ccd767a3d"

FROZEN = {
    "research/r075v_complete_two_harmonic_flux_payment.md": "6917ff77099b6271b005ca90335df589434a38b0a57001893dcae8b02fd34824",
    "research/r075v_complete_two_harmonic_flux_payment_primary_audit.md": "cf23652951c5e1721270577c9a32bc476142b439aefa8ee5f62112cfd8bf5cbd",
    "research/r075v_report-source.md": "a099949ad6968468389b412e1d250c5e1a788ac046b949d4d69fbcf1501e9811",
    "scripts/r075v_complete_two_harmonic_flux_payment_fixtures.json": "d2a16f6e718931aebca696d4934fa497be6bceef8c4e301a9851d04d11e622bc",
    "scripts/r075v_complete_two_harmonic_flux_payment_expected.json": "ebe2cd2b8aad095730eca4b59e5b79e630a28a0f0215fd2cec0024a4593386c6",
    "scripts/r075v_complete_two_harmonic_flux_payment_certificate.py": "c224095be7795a0236575ecc69143e525f652fcfc45236f51751ac25ee68b0d2",
    "scripts/r075v_complete_two_harmonic_flux_payment_certificate_independent.rb": "d12e36c8aa30cf39a8184a401e929d42a843aa5a0bdeb4f374543cfd3c88dc92",
    "scripts/r075v_complete_two_harmonic_flux_payment_qa.sh": "9683be163d5a933f77ae092544341f2b7d91993cd6f50137483edeb9b42eeeb1",
    "research/r075v_complete_two_harmonic_flux_payment_certificate.json": "daa3649b42363368d9db1139a9168d46a7ec44df591e696ea36011288f5a1da5",
    "research/r075v_complete_two_harmonic_flux_payment_certificate_report.md": "9618e0a14bfc36a184381e448e17a59238ad8a02d10c22a8fb7be3546e723c7a",
    "research/r075v_complete_two_harmonic_flux_payment_independent_audit.md": "0c8ab0c24a201b53cc9bfd9eaa0c38848e5978ca47ce915493601cf4199aa9da",
    "research/r075v_complete_two_harmonic_flux_payment_qa_report.md": "d5c877711b59c6a29b11f821710bc7d04ec34a5a7d48d782695abfba566c1a30",
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
        "release": "R0.75V Step 47",
        "source": SOURCE_COMMIT,
        "handoffCommit": HANDOFF_COMMIT,
        "coreParentCommit": CORE_PARENT_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "handoffIndependentAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": True,
    })


if __name__ == "__main__":
    main()
