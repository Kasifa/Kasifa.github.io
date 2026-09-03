#!/usr/bin/env python3
"""Import only the ten frozen R0.75B Step 27 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075B_STEP27_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "29ade05d496c93e5eb9db74e3f462e2207d505f0"
HANDOFF_PATH = "research/r075b_publication_handoff.md"
HANDOFF_SHA256 = "78513e06c613cee87eed15626ac73863586021f87d83a48600c2c6519f043a3a"
HANDOFF_AUDIT_PATH = "research/r075b_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "0c347af15b682b71009830e437e61040058fe76f8206e210f8cea7a7ce869087"

FROZEN = {
    "research/r075b_bulk_clock_outer_padding_gate.md": "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075b_bulk_clock_outer_padding_gate_primary_audit.md": "8f4c2b6c28c63acce86a191ec3bc32602ce9e64e3df80eef8534f2e15a255209",
    "research/r075b_literature_collision_note.md": "6cef708d967fc0e7f47bc87d14496a1d2ff67aa6101a49ebe0f29c4f2d7a023a",
    "research/r075b_bulk_clock_outer_padding_gate_certificate.json": "04ba3c9971defcf87971fc1d7722ca925074445826c437da9baa5438b9b4d0c0",
    "research/r075b_bulk_clock_outer_padding_gate_certificate_report.md": "ae5f533e57e4588b1d973a1abb34fbde3f9547f01577be8f8121b840d3e44ae2",
    "research/r075b_bulk_clock_outer_padding_gate_independent_audit.md": "9d18cc14a72030e6e98d17f9f51ef26515ceecebd80b020ef0c86d1d74715c7f",
    "research/r075b_bulk_clock_outer_padding_gate_qa_report.md": "14e6d7159d32b3b11c58651e3e89513f46d69f0ebc40c4ec8a76e4cae2db6a45",
    "scripts/r075b_bulk_clock_outer_padding_gate_certificate.py": "35cd3e2608fe143a4c092e48e16563b237fe39622bd06b5712f6b5eae18b9a08",
    "scripts/r075b_bulk_clock_outer_padding_gate_certificate_independent.rb": "0004da4bc794a6dbc844529db6c0e572e5ad05d9ee9948aaf82ef95ae6f72146",
    "scripts/r075b_bulk_clock_outer_padding_gate_qa.sh": "8ab21a4b11c4d56e88e7e405acbc9cf6d748a276d304336b10d3cd32f5226794",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(relative: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(SOURCE), "show", f"{SOURCE_COMMIT}:{relative}"])


def write_exact(relative: str, data: bytes, expected: str) -> None:
    if sha256(data) != expected:
        raise SystemExit(f"source hash drift: {relative}")
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    if target.read_bytes() != data:
        raise SystemExit(f"import byte drift: {relative}")


def main() -> None:
    resolved = subprocess.check_output(
        ["git", "-C", str(SOURCE), "rev-parse", f"{SOURCE_COMMIT}^{{commit}}"], text=True
    ).strip()
    if resolved != SOURCE_COMMIT:
        raise SystemExit(f"frozen commit drift: {resolved}")
    if sha256((SOURCE / HANDOFF_PATH).read_bytes()) != HANDOFF_SHA256:
        raise SystemExit("handoff drift")
    if sha256((SOURCE / HANDOFF_AUDIT_PATH).read_bytes()) != HANDOFF_AUDIT_SHA256:
        raise SystemExit("handoff independent audit drift")
    for relative, expected in FROZEN.items():
        write_exact(relative, git_bytes(relative), expected)
    print({
        "status": "PASS",
        "release": "R0.75B Step 27",
        "source": SOURCE_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "handoffAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": False,
    })


if __name__ == "__main__":
    main()
