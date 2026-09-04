#!/usr/bin/env python3
"""Import only the twelve frozen R0.75O Step 40 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075O_STEP40_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "9ad6873ca91c756309d009ffba142e4545f6c4c3"
HANDOFF_COMMIT = "9bf705522928d390472e062f8d244d6b8b5220a0"
HANDOFF_PATH = "research/r075o_publication_handoff.md"
HANDOFF_SHA256 = "f0f5e667dca7be397782a750d8dff80b3e9c4c6fe13294846cfdf1a4d60d7cb5"
HANDOFF_AUDIT_PATH = "research/r075o_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "b68ad69da2d06796faf577a9bb9ea7297c9caf2c19c3e28dc4d72e4f664567a8"

FROZEN = {
    "research/r075o_vertical_diffusion_packet_gain.md": "3efb39d2624cf5b5a0e7f348f6cde2ef2416eca900f1aa3ecc90a6ad734849a9",
    "research/r075o_vertical_diffusion_packet_gain_primary_audit.md": "27f9341f93bd2b031dbd3fd0e8d745788d5ff36a085ddb8be4ef8e1c5553e69b",
    "research/r075o_report-source.md": "9d2c234b0ba2a33b0f573a7933c26bcc751db6fe85919f2e146a0e6a18128c2b",
    "scripts/r075o_vertical_diffusion_packet_gain_fixtures.json": "46dff6097c3a052dc968f1c712c3421105ea5be51d3c905c492cc463cc04f0ad",
    "scripts/r075o_vertical_diffusion_packet_gain_expected.json": "228ac56e500a32b1f7c64c04d4110c78c4105c4d2a997fa8b108bd7449d59833",
    "research/r075o_vertical_diffusion_packet_gain_certificate.json": "71a737b18d67cd01d494abfd0485b42fd78fce9a8bc2085931e17e2aa4be8055",
    "research/r075o_vertical_diffusion_packet_gain_certificate_report.md": "32267743fcfea2a88c5b971912db9f18dd76725b39bba5bf674bd920a8573379",
    "research/r075o_vertical_diffusion_packet_gain_independent_audit.md": "51fc9e834dbdc525b2c75c9430a87d1e8504666f7a65b0ac9e86a22baeb7dac7",
    "research/r075o_vertical_diffusion_packet_gain_qa_report.md": "69a48e0ced0ce74d8d68a94bc6df0bfb35416c35257870f9db73e39e718ec8ad",
    "scripts/r075o_vertical_diffusion_packet_gain_certificate.py": "a92864e15193139d2bfe4dd352c8a398bbe2dc2942fa0e3c2820331cb45f6e05",
    "scripts/r075o_vertical_diffusion_packet_gain_certificate_independent.rb": "33d0c8d15b34e8638160548b287f4db3acbae734b4523f09a700d0c66650f917",
    "scripts/r075o_vertical_diffusion_packet_gain_qa.sh": "084cf638304a98360aecbcefb1d074f8d67aef00c1fb2c49bfd3602db4b8496e",
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
        "release": "R0.75O Step 40",
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
