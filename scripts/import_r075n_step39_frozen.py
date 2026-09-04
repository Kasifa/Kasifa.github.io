#!/usr/bin/env python3
"""Import only the twelve frozen R0.75N Step 39 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075N_STEP39_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "90a0d654447ba40865797669e5e5ad21ad9baa54"
HANDOFF_COMMIT = "43a9b617df0b2478dbdfa649335d6b4040e926b7"
HANDOFF_PATH = "research/r075n_publication_handoff.md"
HANDOFF_SHA256 = "07995870a834c9999f952443b71b46c13e9931187c7a04850f8db17c4b82a9d4"
HANDOFF_AUDIT_PATH = "research/r075n_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "f0690d04ad983a22669764dfd9066f2e584774854206362095a6c3d1149b4a8c"

FROZEN = {
    "research/r075n_radial_collar_averaged_wiener_row.md": "ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318",
    "research/r075n_radial_collar_averaged_wiener_row_primary_audit.md": "c43c063b1c003be22782e7d8e1ce0b3f42cdd3ef4d01912c9de34c876d8c9aba",
    "research/r075n_report-source.md": "ae9d5d630ee0549193c016fcbc07c599b0c678fbaf9c15c5d3c7f24bdf18e27c",
    "scripts/r075n_radial_collar_averaged_wiener_row_fixtures.json": "2dee2146f94f3fa6d0d0c5828d8d6f354f0856f620e1261a133c9a2c81f8a0cb",
    "scripts/r075n_radial_collar_averaged_wiener_row_expected.json": "31614fc11bc4355723fff7773bec8ab13bc44808ffffa0958c78ec1cfe2bba48",
    "research/r075n_radial_collar_averaged_wiener_row_certificate.json": "891774ec5c7e747a4f9c172f0b71e4f6f2af40d8a983bc7c69ebbd1756f405d7",
    "research/r075n_radial_collar_averaged_wiener_row_certificate_report.md": "cad991130fb614d923c224a891001010119a746f9d32c1d17d0fbc5f6c56c0b5",
    "research/r075n_radial_collar_averaged_wiener_row_independent_audit.md": "779d359b62c2860a07e8889826d038d88cad8356af9c53ce31f5bfd1d85441b6",
    "research/r075n_radial_collar_averaged_wiener_row_qa_report.md": "d45d0eef91dab59db773940e2b47caea282781671e186709d7c58f0111c4c4ef",
    "scripts/r075n_radial_collar_averaged_wiener_row_certificate.py": "47256d34a25a188a32147e4cb9f0388819238f2c854e1e814612b9bfd217950e",
    "scripts/r075n_radial_collar_averaged_wiener_row_certificate_independent.rb": "63836294b2924433afa0e95d07baee6427446c7c26c14a34dcd9a5818e0fed56",
    "scripts/r075n_radial_collar_averaged_wiener_row_qa.sh": "568b7934a403e076fb51ae0f18b142547f621a1a514c6ced14e01635c540c66e",
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
        "release": "R0.75N Step 39",
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
