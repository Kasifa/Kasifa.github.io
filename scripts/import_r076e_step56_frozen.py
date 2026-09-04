#!/usr/bin/env python3
"""Import only the twelve frozen R0.76E Step 56 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R076E_STEP56_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "0e929c4066f2111545afa4683b363edac8440825"
CORE_PARENT_COMMIT = "1bb929241ebd5a889babce8e86b4641a665eb64a"
HANDOFF_PATH = "research/r076e_publication_handoff.md"
HANDOFF_SHA256 = "a6c640a20ab75981b6f21506f69917b4fa60ed1ce7c4b47c8dd62cfaec79ead8"
HANDOFF_AUDIT_PATH = "research/r076e_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "fb0498be663ff220ab99c04d861534cf8669ea8fed01e97ffedfa19301229519"

FROZEN = {
    "research/r076e_linear_modal_entropy_window.md": "1494cb7e3863ef934f87746412f2a64ef98f78deb5ce81be3cece7d5a7571ca4",
    "research/r076e_linear_modal_entropy_window_primary_audit.md": "5ce8fb3f2f2f487002b0e391db49855edb3cff72574058e26150813d69615d27",
    "research/r076e_report-source.md": "10e506fa9d250b14d9f42f6eac7c2c83cfca934a85a2da6e223cd473f21e0c12",
    "scripts/r076e_linear_modal_entropy_window_fixtures.json": "9b5b0a7d88fe31d4156a7fbc8f73b52a9b5a8271437ee1be867970cec244cf47",
    "scripts/r076e_linear_modal_entropy_window_expected.json": "af6c1fd49d57945306f5f97a99f160a8fcbaec21bce887b78fe74e0bbe4d4f80",
    "scripts/r076e_linear_modal_entropy_window_certificate.py": "57e629e0952131928e738501ee14f525daf3e2ac5fcb3b37fe02b118d7fb0f6c",
    "scripts/r076e_linear_modal_entropy_window_certificate_independent.rb": "e5f340e181b96a45d202ec88e5d98d71744b2ed23008e579c8c705c88fc30bdd",
    "scripts/r076e_linear_modal_entropy_window_qa.sh": "76859a4f6fc86652957336a096ec06c73f643cfac0e46df38e1c38bad1b9fee0",
    "research/r076e_linear_modal_entropy_window_certificate.json": "73daf5a6fe12096b29b87704a667e45c994cd2233244e6f2f8daba987b471245",
    "research/r076e_linear_modal_entropy_window_certificate_report.md": "8e3937b7b5843b49c53fbbc6b3cc0490a139b1c2ff2e469bb64758f112d11f31",
    "research/r076e_linear_modal_entropy_window_independent_audit.md": "bc5ed58d5a47a1c847ea626c85da49078a19ed148323c72eaf3d452b90ad3842",
    "research/r076e_linear_modal_entropy_window_qa_report.md": "0afdabc3805121ef593c1c2741b12d6011821a0cc98c7b07b76306c7f24ef631",
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
        "release": "R0.76E Step 56",
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
