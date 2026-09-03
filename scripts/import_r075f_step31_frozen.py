#!/usr/bin/env python3
"""Import only the twelve frozen R0.75F Step 31 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075F_STEP31_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "be9a79a1d2b1fd2b7ee0e33f1f6e18f23b63958c"
HANDOFF_COMMIT = "97706831d95f82664c9693773c79e111a12fce35"
HANDOFF_PATH = "research/r075f_publication_handoff.md"
HANDOFF_SHA256 = "1c150c22663850a3b21f47e1df3e1606796aa1a8edabad362d619fa81acf4afc"
HANDOFF_AUDIT_PATH = "research/r075f_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "92c45d8fe449a846ec3f02d1d5bcbe2dfe9b9a27f3cb981c8cafb3761560751b"

FROZEN = {
    "research/r075f_modal_phase_integration_identity.md": "f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440",
    "research/r075f_modal_phase_integration_identity_primary_audit.md": "4320ac5544b51888eb8088db98e500a9877ecfe9a984f156783cac096a27c99a",
    "research/r075f_report-source.md": "3838603ea143b2efe1e96995fac34d7e8565211dc91dd244ab01cf6d526f3481",
    "scripts/r075f_modal_phase_integration_identity_fixtures.json": "0ce9b3bf060f4b38fe497be7bcdad3d1bdbd51ea27ff9aab146c8b10f5a0aced",
    "scripts/r075f_modal_phase_integration_identity_expected.json": "3946cb2cc992f4d1e55b88a7be9b7ecd8529e76a437093af6583f8fdacf2ddc9",
    "research/r075f_modal_phase_integration_identity_certificate.json": "107c59254b8f2e0ffa5e7a04ab8bdc97158191e99fca0f02ed08e0973c46fcf5",
    "research/r075f_modal_phase_integration_identity_certificate_report.md": "a756e4cf3e4d44012dde1588ca2150fb58c1669e6218e602aa2fba916b2c2834",
    "research/r075f_modal_phase_integration_identity_independent_audit.md": "eb7fac3ac148a41c43040c758028eb6552aa952639b54e0e1e47842604631fe8",
    "research/r075f_modal_phase_integration_identity_qa_report.md": "f40a103b4b0a6cb85d684c7ff50d418402f857d8b77064d7f6c61139c77605f0",
    "scripts/r075f_modal_phase_integration_identity_certificate.py": "c86d85bb468b9bd953247520e2de53cd18eb7362ef63dc60ae7895b01defb768",
    "scripts/r075f_modal_phase_integration_identity_certificate_independent.rb": "7499e5fa9544a805eb0675566224a77f4d99a196f3e1582a87bb4af724d269c2",
    "scripts/r075f_modal_phase_integration_identity_qa.sh": "b05e7eca1fae71955b27bc4fc6d3ddf1554f488dffe91cf081affe39c8e5932c",
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
        "release": "R0.75F Step 31",
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
