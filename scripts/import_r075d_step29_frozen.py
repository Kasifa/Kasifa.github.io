#!/usr/bin/env python3
"""Import only the ten frozen R0.75D Step 29 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075D_STEP29_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "1e010e638569f14f74fea6c1db89e08c1f63d622"
HANDOFF_PATH = "research/r075d_publication_handoff.md"
HANDOFF_SHA256 = "bf442c5cf271115aa505cd8755bb4dda0999f9147d4177fa419b1aaaf3305536"
HANDOFF_AUDIT_PATH = "research/r075d_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "56de52ad43fdfcc5f308fc949c5f4eb93a51d8b5716490a47996fbffc2527001"

FROZEN = {
    "research/r075d_passive_gradient_route_screen.md": "54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6",
    "research/r075d_passive_gradient_route_screen_primary_audit.md": "f06e29971ea3f0b05c7a1c39983a2ae21aa241a8e46f02e2450632e07c5eaef7",
    "research/r075d_report-source.md": "5c415c3e280fea1569a42d64d99400fe4dfaf440d2808d637ca57cfc1d386c1f",
    "research/r075d_passive_gradient_route_screen_certificate.json": "9222dfa3c7051fbe7d5d78405f6ad8071e54b4eed736cd2afae97f96f617c639",
    "research/r075d_passive_gradient_route_screen_certificate_report.md": "24dfb6fa2ce6e1bce280a34a4f16c0d7aa84e75e08fb2408d7c4edae78f506a1",
    "research/r075d_passive_gradient_route_screen_independent_audit.md": "1b1c5e6ba1826b291d7fc649ac0db0cf1e5ae91ce3e8800d36c3ffce5f395439",
    "research/r075d_passive_gradient_route_screen_qa_report.md": "f9c97884fa29ab7151f675ca45eb48e1449ce8fd0cd7fee8997df882528cf940",
    "scripts/r075d_passive_gradient_route_screen_certificate.py": "5a79cafe4c7794367b23447cdfc09ba0ee49536e756074aa28aa219173fb0823",
    "scripts/r075d_passive_gradient_route_screen_certificate_independent.rb": "1a8066cfc4fe90266ff38163a60e752988699b21871482308bb307455be3b090",
    "scripts/r075d_passive_gradient_route_screen_qa.sh": "2c3b9e359b41f27733b29e301b105c56e73b2435e8d1c7f40a6615cdcef19557",
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
        "release": "R0.75D Step 29",
        "source": SOURCE_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "handoffAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": False,
    })


if __name__ == "__main__":
    main()
