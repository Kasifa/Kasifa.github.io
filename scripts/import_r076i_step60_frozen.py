#!/usr/bin/env python3
"""Import only the twelve frozen R0.76I Step 60 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R076I_STEP60_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "0b73f68e072e573d9aaaa824e137e29a49d3cd67"
CORE_PARENT_COMMIT = "8626f085f3220a79d19816ec220eacc8909971cc"
HANDOFF_COMMIT = "72a5322f3ccb5cb53ad7cf489176c04e25148691"
HANDOFF_PATH = "research/r076i_publication_handoff.md"
HANDOFF_SHA256 = "b69e0f736de1253c277852aeb40f81733dbe32e34e2c2df19f8e2fd2581c9d29"
HANDOFF_AUDIT_PATH = "research/r076i_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "271a3adc20ce41ce9c63e31cfbc1a79a95a109b57cc6ed03036b13c265f9adaf"

FROZEN = {
    "research/r076i_chebyshev_scale_full_plateau_window.md": "6277cb69dfad94cae89088c6a8c007967bdde97aceee7b19954d10ec53f6efce",
    "research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md": "65adf8bc77f33c5d18184c612acc67246e48e7ad3c9059b85f269e92c9372dbe",
    "research/r076i_report-source.md": "0ee0fbd75f9691e2ac898a57921f8a0574ba9af9ea652f85d0199856d7e3d423",
    "scripts/r076i_chebyshev_scale_full_plateau_window_fixtures.json": "f1475b2549490c3639c15a4fc103e704d0de98a518f50249b732a8e0a135d776",
    "scripts/r076i_chebyshev_scale_full_plateau_window_expected.json": "26485db072bf886fae88f0737546d7090f77b9b23e55c356bf8affe6aeba1da5",
    "scripts/r076i_chebyshev_scale_full_plateau_window_certificate.py": "a14e7fe3bc3b118232328a6d9e4d9d4cedb1e685c057483e12416725024af538",
    "scripts/r076i_chebyshev_scale_full_plateau_window_certificate_independent.rb": "5e1ead81eb0f036d41addf2dd203527c3ae49aa497d483002a3973b69d88225c",
    "scripts/r076i_chebyshev_scale_full_plateau_window_qa.sh": "d23b771cd0e7c5253ba592f9efd2e7c0c2396cd928641f6463559b2b20953458",
    "research/r076i_chebyshev_scale_full_plateau_window_certificate.json": "6ae521f88a1e6116f466641bde60939e458b043b43ca025a10a83001613c590b",
    "research/r076i_chebyshev_scale_full_plateau_window_certificate_report.md": "b5d1f7b0e36f724522bc5b18442bad97ffe778e7be6ca579c0ca0bd89d9d061c",
    "research/r076i_chebyshev_scale_full_plateau_window_independent_audit.md": "f8c735e654031b8d5ae7029879086bf95086e7745317b7faa0e6750151093b4d",
    "research/r076i_chebyshev_scale_full_plateau_window_qa_report.md": "7f709110b3191508541367846c9ef0358016cfcb91c160e00b9db123664dd34a",
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
    for commit in (SOURCE_COMMIT, CORE_PARENT_COMMIT, HANDOFF_COMMIT):
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
    handoff_parent = subprocess.check_output(
        ["git", "-C", str(SOURCE), "rev-parse", f"{HANDOFF_COMMIT}^"], text=True
    ).strip()
    if handoff_parent != SOURCE_COMMIT:
        raise SystemExit(f"handoff parent drift: {handoff_parent}")
    if sha256(git_bytes(HANDOFF_COMMIT, HANDOFF_PATH)) != HANDOFF_SHA256:
        raise SystemExit("handoff drift")
    if sha256(git_bytes(HANDOFF_COMMIT, HANDOFF_AUDIT_PATH)) != HANDOFF_AUDIT_SHA256:
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
        "release": "R0.76I Step 60",
        "source": SOURCE_COMMIT,
        "coreParentCommit": CORE_PARENT_COMMIT,
        "handoffCommit": HANDOFF_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "handoffIndependentAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": True,
    })


if __name__ == "__main__":
    main()
