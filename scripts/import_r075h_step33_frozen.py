#!/usr/bin/env python3
"""Import only the twelve frozen R0.75H Step 33 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075H_STEP32_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "41e138f1770bbc3f06a69ba67fa7d1ec59c1c397"
HANDOFF_COMMIT = "07b03ea63d05e8de4d20d2ea489d3373cb6251a5"
HANDOFF_PATH = "research/r075h_publication_handoff.md"
HANDOFF_SHA256 = "008b1f64f566165dc0fcf5fc3f2978c6e6519ae1d2285392cd8fc3dd4b1eb1ec"
HANDOFF_AUDIT_PATH = "research/r075h_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "fb9785d8d282ba09bfa6a5de5f349ecd7a7c37b08060ad155f074eb3474376c9"

FROZEN = {
    "research/r075h_single_pass_transport_flux_closure.md": "849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9",
    "research/r075h_single_pass_transport_flux_closure_primary_audit.md": "3c85368e051102997e66ae36fa43290b6200e688db886380215fb40ec0bb757e",
    "research/r075h_report-source.md": "5b0b05b2ce903986ef8439a766766e8bdb97e2fe4d9eb6035f73102583b1b779",
    "scripts/r075h_single_pass_transport_flux_closure_fixtures.json": "7e4b5691d6929c97f72146c293a55e3b6fcf5875bc51f78bd1a58e9f84a0b217",
    "scripts/r075h_single_pass_transport_flux_closure_expected.json": "099d017cb7ff61d5a9dff54449c9a91a12e8657343bb11579ad135e9cd350573",
    "research/r075h_single_pass_transport_flux_closure_certificate.json": "1fda0c2e812a50a4f183b78ba503ce766553cd1dcbb1206384e07e3b1f0b0b38",
    "research/r075h_single_pass_transport_flux_closure_certificate_report.md": "c77dd0ea2896ad3914bf6d74c647d5b1ebae91cfaa522df16bf2196aa13ca5a0",
    "research/r075h_single_pass_transport_flux_closure_independent_audit.md": "9c1b09a5c996c371a4ed9bcb302fc211b9ea2e97014e4c5f3f985c23207e411b",
    "research/r075h_single_pass_transport_flux_closure_qa_report.md": "ed134d1411905dd052550ea932e9ca7c4d70c5f49b1f7194002844f950b35911",
    "scripts/r075h_single_pass_transport_flux_closure_certificate.py": "68fc20b109f6017940f8f137bc79a387076c2990b52fdfe44ad5b2c4a4beead5",
    "scripts/r075h_single_pass_transport_flux_closure_certificate_independent.rb": "0b5b591b84aba87bb7cb37d119abadc108217a3d77af1eeeb08a10d3178195af",
    "scripts/r075h_single_pass_transport_flux_closure_qa.sh": "bfaa1c8e3107c33a340c066178ea2e70edd74c4afcd16784996847703b6a941a",
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
        "release": "R0.75H Step 33",
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
