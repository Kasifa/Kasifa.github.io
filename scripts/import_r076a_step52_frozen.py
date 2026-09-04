#!/usr/bin/env python3
"""Import only the twelve frozen R0.76A Step 52 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R076A_STEP52_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "1f15e31b56c37a6a3941a1c4961321b7b1745e6c"
CORE_PARENT_COMMIT = "69d65cd5cf897c90a9943d1b29090a11dc3c4f03"
HANDOFF_PATH = "research/r076a_publication_handoff.md"
HANDOFF_SHA256 = "ddf207b3785cab74bedebca695f48660a69b71412eb6427ebc4e9b174d00c46c"
HANDOFF_AUDIT_PATH = "research/r076a_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "3ea9f69740496eb1d15a259cffe62d8961fd76296b1dd8b208796cb940643513"

FROZEN = {
    "research/r076a_complete_clock_localized_current_sign_obstruction.md": "d23532f84702be1630daa0b8d56d02242571dd8a1f8024c59a7f71bec30f26eb",
    "research/r076a_complete_clock_localized_current_sign_obstruction_primary_audit.md": "0f7f56d32025f4cd86218f54dfcf5155675f316d2afecdd0007b13ad70240a8d",
    "research/r076a_report-source.md": "0bbf94774c7d76e623c025a731e0238eca39080c4720a039f080afb038ecad8b",
    "scripts/r076a_complete_clock_localized_current_sign_obstruction_fixtures.json": "f3644b2a7a641bc92c6c1936f1c05cbed88a6a3e94e25d650c7258ce07b30a31",
    "scripts/r076a_complete_clock_localized_current_sign_obstruction_expected.json": "32d0f99d07d842bf6c9161698249c186c4d23d2f1f33e7f8bd7fc18804887697",
    "scripts/r076a_complete_clock_localized_current_sign_obstruction_certificate.py": "7dfff7dfb26ccfb9399c0a9cc32a914d5e1d94f3a81ed172f4ec245343d43ab5",
    "scripts/r076a_complete_clock_localized_current_sign_obstruction_certificate_independent.rb": "5633861e614cba477f59e8ca4d6f52bc9c29e561178ae07117af53d83cc13366",
    "scripts/r076a_complete_clock_localized_current_sign_obstruction_qa.sh": "d34a0275f6b321c84db14fd47219701ef5a3caa53572b941f37343c88d680539",
    "research/r076a_complete_clock_localized_current_sign_obstruction_certificate.json": "cd09488885f0e31d95f94c7f46bf0c80b1ad476a438a3fa081d3ec83d4c2949c",
    "research/r076a_complete_clock_localized_current_sign_obstruction_certificate_report.md": "665e69226763e2df99615714829387309a3f66a1ec1e35b19f4af35d005c0d12",
    "research/r076a_complete_clock_localized_current_sign_obstruction_independent_audit.md": "cd5608262b4f9c35f30afec9af2a108621f4f89cf8f4a69d973e1e07b6ee670d",
    "research/r076a_complete_clock_localized_current_sign_obstruction_qa_report.md": "fb8681c63bfa83bc26fadeb867c0c25c6167b28789bda9480e061dcdf0409a82",
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
    for commit in (SOURCE_COMMIT, CORE_PARENT_COMMIT):
        resolved = subprocess.check_output(
            ["git", "-C", str(SOURCE), "rev-parse", f"{commit}^{{commit}}"], text=True
        ).strip()
        if resolved != commit:
            raise SystemExit(f"frozen commit drift: {resolved}")
    core_parent = subprocess.check_output(
        ["git", "-C", str(SOURCE), "rev-parse", f"{SOURCE_COMMIT}^"], text=True
    ).strip()
    if core_parent != CORE_PARENT_COMMIT:
        raise SystemExit(f"core parent drift: {core_parent}")
    if sha256((SOURCE / HANDOFF_PATH).read_bytes()) != HANDOFF_SHA256:
        raise SystemExit("handoff drift")
    if sha256((SOURCE / HANDOFF_AUDIT_PATH).read_bytes()) != HANDOFF_AUDIT_SHA256:
        raise SystemExit("handoff independent-audit drift")
    changed = subprocess.check_output(
        ["git", "-C", str(SOURCE), "show", "--pretty=format:", "--name-only", SOURCE_COMMIT], text=True
    ).split()
    if set(changed) != set(FROZEN) or len(changed) != len(FROZEN):
        raise SystemExit("core changed-path whitelist drift")
    for relative, expected in FROZEN.items():
        write_exact(relative, git_bytes(SOURCE_COMMIT, relative), expected)
    print({
        "status": "PASS",
        "release": "R0.76A Step 52",
        "source": SOURCE_COMMIT,
        "coreParentCommit": CORE_PARENT_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "handoffIndependentAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": False,
    })


if __name__ == "__main__":
    main()
