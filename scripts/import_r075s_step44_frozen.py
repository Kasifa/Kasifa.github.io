#!/usr/bin/env python3
"""Import only the twelve frozen R0.75S Step 44 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075S_STEP44_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "0afac1ea57d26466883d89b39b19965dcaaa1e58"
HANDOFF_COMMIT = "1c7432ac79521f26aab3b32a0dd4a272484f2776"
HANDOFF_PATH = "research/r075s_publication_handoff.md"
HANDOFF_SHA256 = "dbbbc1474751fa6a7ddaa4ff6eed21756688809bfdd8b2d7a69303acd52377a0"
HANDOFF_AUDIT_PATH = "research/r075s_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "e24548e99ed1ccb4c98aac541e86f2381c78af1b60216cdfc927c7d2ef32641b"

FROZEN = {
    "research/r075s_full_frequency_single_harmonic_clock_payment.md": "d2736eaa43443048bd620567c4acd72024dc4c662320a8aa58af31ccc6047ccd",
    "research/r075s_full_frequency_single_harmonic_clock_payment_primary_audit.md": "38e2bc95b5785b97df5d85474f3ed6105458a117249710b2c052cebbd769b5eb",
    "research/r075s_report-source.md": "ab9771e732204f28d3493ae9db73e7aa62aa980cc15b69dfefb39f226520b2a7",
    "scripts/r075s_full_frequency_single_harmonic_clock_payment_fixtures.json": "82874592703552c1639c69066ddbf1ab531c135cd92eeae775c20be66cd8260f",
    "scripts/r075s_full_frequency_single_harmonic_clock_payment_expected.json": "e806089d4649b73649edeed5c0204b81a42dbef79c758283b128ec49a57abd8b",
    "research/r075s_full_frequency_single_harmonic_clock_payment_certificate.json": "da70756ebf873bd9ac9d36cc676e059621cf63069ec8a8c8efc9d2ebe5473b6a",
    "research/r075s_full_frequency_single_harmonic_clock_payment_certificate_report.md": "6580726e22fa1b4af3ab3cfabdb3731b65674cb83479d7524124b456ab132987",
    "research/r075s_full_frequency_single_harmonic_clock_payment_independent_audit.md": "2ff691c30692d4742b10d5f28bda4b05f95691ecfd083941e638aef491911462",
    "research/r075s_full_frequency_single_harmonic_clock_payment_qa_report.md": "af318d1aacaa615cbf428631e0da61860668c5ee10c22e418e46df1c7e2e3378",
    "scripts/r075s_full_frequency_single_harmonic_clock_payment_certificate.py": "3a64a105f8cb01e20d2ec66ac4946beaf66dc726c05c0e9b72c2097fd0947243",
    "scripts/r075s_full_frequency_single_harmonic_clock_payment_certificate_independent.rb": "93cdcd359c7491a2bd8e48a8f092cad798efac050fd3e806e56f9a3cddbe696e",
    "scripts/r075s_full_frequency_single_harmonic_clock_payment_qa.sh": "b7d8629ea27dd7330784a43965387a8cdea03dc1b1468569260195a1cbcbcaaa",
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
        "release": "R0.75S Step 44",
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
