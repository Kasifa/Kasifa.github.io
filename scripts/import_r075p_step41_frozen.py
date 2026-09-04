#!/usr/bin/env python3
"""Import only the twelve frozen R0.75P Step 41 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075P_STEP41_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "272b4d29a419becd5188721dfdfc88d2a4194082"
HANDOFF_COMMIT = "2e6c8de0278ebb74aea3dac5c12093a61b13c5ac"
HANDOFF_PATH = "research/r075p_publication_handoff.md"
HANDOFF_SHA256 = "5b35e9981b53402602fc5261b3546a1ead2762b7ad1f348e361c6512e037ef1c"

FROZEN = {
    "research/r075p_buffered_collar_entrance_concentration.md": "8df38e54514d82102cd3e568e89ec1db93913da3ceac52f1371d77fd79c1b7a6",
    "research/r075p_buffered_collar_entrance_concentration_primary_audit.md": "e065759a1df3c118f71dd47ac9b5ded9df40536217f557b3c1155e8bf64d3390",
    "research/r075p_report-source.md": "fcde6bed847b0628aff7de90a49e8150e4a279fca8e46d7053943fdadf0478ca",
    "scripts/r075p_buffered_collar_entrance_concentration_fixtures.json": "9d9bf2a00fbdf58eb85a01a3f7fe931f289a5bc1166430dac1f704e4406ec6d7",
    "scripts/r075p_buffered_collar_entrance_concentration_expected.json": "cc472fb797c98d61e004c09fb84ba4a29029d72665f60507628c166134b39d31",
    "research/r075p_buffered_collar_entrance_concentration_certificate.json": "acbb41a489120b00a32f75999909f0cabce4f96ac5e8650c3ebfd2e0a35dc0a8",
    "research/r075p_buffered_collar_entrance_concentration_certificate_report.md": "1c9bc9553d1facdab0b385a59480c378dfd516412c38eb3a20e76049745560ac",
    "research/r075p_buffered_collar_entrance_concentration_independent_audit.md": "60b042b5830167508f096fe7d990f7d2b5fca99da312f0e6116b8c39c0c7923d",
    "research/r075p_buffered_collar_entrance_concentration_qa_report.md": "81e6ff0eefc1fd4d65b1cd7fc8c950b0e284f7b9c54c4542b1e79c9c6dec1dd7",
    "scripts/r075p_buffered_collar_entrance_concentration_certificate.py": "5c13e8bb480e4565a4b7be6f6d86a0a963cea5ce9d53495f5e0cf3c7983b1c6c",
    "scripts/r075p_buffered_collar_entrance_concentration_certificate_independent.rb": "5fb32514dc125462239adc31bc5da58460946d8caaed0d3a1c76d6620b8bfd2c",
    "scripts/r075p_buffered_collar_entrance_concentration_qa.sh": "8c4fbeb7667bdb4f937e66cd73d663fa8cd85538412e538259b9a0128f9a27fb",
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
    parent = subprocess.check_output(
        ["git", "-C", str(SOURCE), "rev-parse", f"{HANDOFF_COMMIT}^"], text=True
    ).strip()
    if parent != SOURCE_COMMIT:
        raise SystemExit(f"handoff parent drift: {parent}")
    for relative, expected in FROZEN.items():
        write_exact(relative, git_bytes(SOURCE_COMMIT, relative), expected)
    print({
        "status": "PASS",
        "release": "R0.75P Step 41",
        "source": SOURCE_COMMIT,
        "handoffCommit": HANDOFF_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": False,
    })


if __name__ == "__main__":
    main()
