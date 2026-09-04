#!/usr/bin/env python3
"""Import only the twelve frozen R0.76D Step 55 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R076D_STEP55_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "c0cfe20b1970d9abbc32c191a5fad71dfdad1465"
CORE_PARENT_COMMIT = "675638c96b204b7d853407fc2b0ace64ba5e061d"
HANDOFF_PATH = "research/r076d_publication_handoff.md"
HANDOFF_SHA256 = "8fb0b43aea6958a5fa40c36e118aa5dc7a9d275597f6ecb07ca9b719d97d9452"
HANDOFF_AUDIT_PATH = "research/r076d_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "1231b3bf4de7e097f9e3cec947fa16716a5f4e3772365bfcecd2a3b6905f279e"

FROZEN = {
    "research/r076d_quantitative_growing_mode_entropy_window.md": "cd94e3384f01963cb7b8a14fdb8376c6197c361473447f15500db0acac5e958e",
    "research/r076d_quantitative_growing_mode_entropy_window_primary_audit.md": "9b99247ceb34cadc12c7f4f0858be642316ca80d1ff83d05dfd745a9906356d8",
    "research/r076d_report-source.md": "f2358780d382dcace69b7ebef855bf3c8e63d15b581dc86b62b7e3c751fbd310",
    "scripts/r076d_quantitative_growing_mode_entropy_window_fixtures.json": "ffe5c2b9a1a6b0c20b710dc45fcac9543069ea6af38dce34804665012984b374",
    "scripts/r076d_quantitative_growing_mode_entropy_window_expected.json": "eb5dd9ebaa6a74cbc7f999fdbd55ee54a50588342c3dfba9412ac53c935ba2dd",
    "scripts/r076d_quantitative_growing_mode_entropy_window_certificate.py": "ed96f55b1326f1e7c1330670c132c523c7861f53edcb046b662159d83e60ce54",
    "scripts/r076d_quantitative_growing_mode_entropy_window_certificate_independent.rb": "9f12fa2aadc35dfb228e8f0ab60eec420c5c6bdfa306f1b66ca4828cdde4d391",
    "scripts/r076d_quantitative_growing_mode_entropy_window_qa.sh": "b69b5380ffd60ad713c3971311cf6197bc5254a44abbb8e65f3d19990ec5e592",
    "research/r076d_quantitative_growing_mode_entropy_window_certificate.json": "e57d160e8b3b37ed714e884750f50abbaaaac25a1e3ec3ba395a0193e0b6757d",
    "research/r076d_quantitative_growing_mode_entropy_window_certificate_report.md": "460917d50cd9aeeb4af5898322915d67fa8ec3e1971f2e5945becf858ccd9c94",
    "research/r076d_quantitative_growing_mode_entropy_window_independent_audit.md": "0d6e3b7f363fdb9e031a228038ae7af4152d51d101e6050f39c4de7dc21fa69a",
    "research/r076d_quantitative_growing_mode_entropy_window_qa_report.md": "e0313b591dee896aae87930dfd01cfa2c6cd3f1e7a82875b439ba0399402fab6",
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
        "release": "R0.76D Step 55",
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
