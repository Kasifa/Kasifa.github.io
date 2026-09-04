#!/usr/bin/env python3
"""Import only the twelve frozen R0.75R Step 43 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075R_STEP43_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "0b7a57c826823d14bfad66913556e8ed88584325"
HANDOFF_COMMIT = "9f99f88cdf8fb2d209401d8a6bc213df53bb2130"
HANDOFF_PATH = "research/r075r_publication_handoff.md"
HANDOFF_SHA256 = "7276d853ea41be03a638ff91faad79fe05da16cf15ab822a79acbbd76c965105"
HANDOFF_AUDIT_PATH = "research/r075r_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "8ce8bbc86a92bd43ce84d0db0c8bfb4630a094fd06a1a71481f695e7fc2e06b8"

FROZEN = {
    "research/r075r_outer_cap_spectral_concentration_obstruction.md": "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
    "research/r075r_outer_cap_spectral_concentration_obstruction_primary_audit.md": "9b52e3d54fce43c609f70f0b8e71c53def0b4b705144be39a7b62e88d5e07355",
    "research/r075r_report-source.md": "767bfc43f9510a2acdf7fbff9d52624ed23ed80e4c3af174c77a47c3824d87ed",
    "scripts/r075r_outer_cap_spectral_concentration_obstruction_fixtures.json": "226b7411967f2fa6f1960d29a03f32ef40945af47c6545c3f60e4115e507a1d1",
    "scripts/r075r_outer_cap_spectral_concentration_obstruction_expected.json": "25d46dc6276a42f764dc503100750186213186368aebc9d94be409cd80f3c251",
    "research/r075r_outer_cap_spectral_concentration_obstruction_certificate.json": "9dcd06306bef05f33f88c09e982e97f04b3fd5a3ee9542e2e063c083a535a3ac",
    "research/r075r_outer_cap_spectral_concentration_obstruction_certificate_report.md": "40d17a2b3ddc7c2ee024c0e6288101eded441effa468d22555a1a8cb38c4d65f",
    "research/r075r_outer_cap_spectral_concentration_obstruction_independent_audit.md": "aac8e1a9fb01f9ba5b1e41d2ac25c9ee40a97e001a65e7c16a1dc1521dcf89dc",
    "research/r075r_outer_cap_spectral_concentration_obstruction_qa_report.md": "f9fa78b9a4dc918a318a64cff38408e0b3508a83446225532989651718884b19",
    "scripts/r075r_outer_cap_spectral_concentration_obstruction_certificate.py": "2c712cc35f53063212466a9c26b094d100a39809b8d424cc4062eb5b062d4e86",
    "scripts/r075r_outer_cap_spectral_concentration_obstruction_certificate_independent.rb": "2da9b4d9cbc53c7e0bb33f834f658b72ec7cfe88bacb215d221612a2dfa4283e",
    "scripts/r075r_outer_cap_spectral_concentration_obstruction_qa.sh": "266b8c2143f02e6f47365859d1343fcc1668601b977521783cadf939f0458aa5",
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
        raise SystemExit("handoff independent-audit drift")
    parent = subprocess.check_output(
        ["git", "-C", str(SOURCE), "rev-parse", f"{HANDOFF_COMMIT}^"], text=True
    ).strip()
    if parent != SOURCE_COMMIT:
        raise SystemExit(f"handoff parent drift: {parent}")
    for relative, expected in FROZEN.items():
        write_exact(relative, git_bytes(SOURCE_COMMIT, relative), expected)
    print({
        "status": "PASS",
        "release": "R0.75R Step 43",
        "source": SOURCE_COMMIT,
        "handoffCommit": HANDOFF_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "handoffIndependentAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": False,
    })


if __name__ == "__main__":
    main()
