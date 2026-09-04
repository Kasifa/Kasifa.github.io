#!/usr/bin/env python3
"""Import only the twelve frozen R0.75Q Step 42 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075Q_STEP42_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "1b1d092e96aaca9afe723c40994accbe1aee5031"
HANDOFF_COMMIT = "780596a1b431a695cbed0978714f721b8577af81"
HANDOFF_PATH = "research/r075q_publication_handoff.md"
HANDOFF_SHA256 = "998fa28d8d0f6d3c2cb205a51309014c00f566d74190fe3335f1818bd365da7b"

FROZEN = {
    "research/r075q_spatially_spread_harmonic_collar_payment.md": "9d7058fd7fbc61136967227507e47b0e866c7a4eeafebae198ab05a23645ed9c",
    "research/r075q_spatially_spread_harmonic_collar_payment_primary_audit.md": "92255869e165efdbe72557187dd1fe6e7e4449264dcf8033b285286d50f725be",
    "research/r075q_report-source.md": "b1fcfece0396b04ae9f59e42ef09957a422c36fa0843730a9fb22919bc24c600",
    "scripts/r075q_spatially_spread_harmonic_collar_payment_fixtures.json": "a0954f102de2fbc5ac5fb57fd68ba2ae084cc27743240fac6e3297b81d4410f5",
    "scripts/r075q_spatially_spread_harmonic_collar_payment_expected.json": "8f3e45bb4a62e2a5bd506fd3cc522610d59115f34411fd85b04c7b72081cb444",
    "research/r075q_spatially_spread_harmonic_collar_payment_certificate.json": "fc53a51af160befea1ffc146256aba31792cd4bd3de36004ff851f3b57d7cc12",
    "research/r075q_spatially_spread_harmonic_collar_payment_certificate_report.md": "b5f8fdd24f7bf4911eadf1fe6fb1aa25ac255dcd0bd7a36dcc239d2e023b591d",
    "research/r075q_spatially_spread_harmonic_collar_payment_independent_audit.md": "932d1ef7e14701a08584c926a68951e878a2e3f1a74e03a4a22a8a590faa6c8f",
    "research/r075q_spatially_spread_harmonic_collar_payment_qa_report.md": "356796d82e9857ef94642871509dfcacf2c699c4e683fe00ed2cd946a6fdc6b6",
    "scripts/r075q_spatially_spread_harmonic_collar_payment_certificate.py": "e9a2758fd7688be5bd5970c28385ef501a1716095c1d673fb81071989e0fe09e",
    "scripts/r075q_spatially_spread_harmonic_collar_payment_certificate_independent.rb": "4d0a81b580bba7061faefe98777d5ad55330d3b60f6563774e73ec8da9a17bbd",
    "scripts/r075q_spatially_spread_harmonic_collar_payment_qa.sh": "f34eee300896e19372983f027a4a52821872f9f63df2df0fa5236d888f5b9ddc",
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
        "release": "R0.75Q Step 42",
        "source": SOURCE_COMMIT,
        "handoffCommit": HANDOFF_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": False,
    })


if __name__ == "__main__":
    main()
