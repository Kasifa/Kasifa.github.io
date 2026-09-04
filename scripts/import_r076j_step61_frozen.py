#!/usr/bin/env python3
"""Import only the twelve frozen R0.76J Step 61 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R076J_STEP61_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "25d44e986d5283107816f910f89b94bceb1d5726"
CORE_PARENT_COMMIT = "72a5322f3ccb5cb53ad7cf489176c04e25148691"
HANDOFF_COMMIT = "8b3b67c9f9d1e796f6a1bbd8639ab25d80ed0470"
HANDOFF_PATH = "research/r076j_publication_handoff.md"
HANDOFF_SHA256 = "fedab351568d286247b90eb4fc314c41892de2deabf283ea82c69209fb9478fc"
HANDOFF_AUDIT_PATH = "research/r076j_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "9108064a741c595c52701be57a4e592dd62b453f54b89abbcf2742e47d32f0bf"

FROZEN = {
    "research/r076j_local_edge_extrapolation_reconstruction.md": "a3d67c8a27ef6ffb7068313732e8e8a08ba98931226df726ac4ee2140ab0f57f",
    "research/r076j_local_edge_extrapolation_reconstruction_primary_audit.md": "1b2a608c6ffe16c35489b95fd384f0f47a1d4a79b22491a7825ac53382a746d5",
    "research/r076j_report-source.md": "371eac6e3f053d4ba51ded16f35024ba805d10c5a81c1f01879704ce583763c7",
    "scripts/r076j_local_edge_extrapolation_reconstruction_fixtures.json": "f0957b65e763339d1ff8cc029a13e13231b22b44dff8796b3b21883ffb352c31",
    "scripts/r076j_local_edge_extrapolation_reconstruction_expected.json": "9e5ad2f9bed318cd1232319240d2e574f070eda0364f97957df9c013f35878e8",
    "scripts/r076j_local_edge_extrapolation_reconstruction_certificate.py": "ed969fa1730597ecf33bc530ec1e40509080730f0a59552a1309182cd698f771",
    "scripts/r076j_local_edge_extrapolation_reconstruction_certificate_independent.rb": "ab58a7e8d77434de9ef363b04c43a612d5b61e0504faf82299783f7ea1b171f3",
    "scripts/r076j_local_edge_extrapolation_reconstruction_qa.sh": "d6364ed1896264a21173b2feb6b98e9b34522686d6300bd8066ef9dda18f0538",
    "research/r076j_local_edge_extrapolation_reconstruction_certificate.json": "23db36bc873a47e1992c9650e5ea04c5c1874f2e2a0bd17b6353bcb4452be89f",
    "research/r076j_local_edge_extrapolation_reconstruction_certificate_report.md": "a6c140ca114e73d975eff57de1804d85ba59fa080720fd5ac17e05d1bf7896d2",
    "research/r076j_local_edge_extrapolation_reconstruction_independent_audit.md": "63231761c982914b79e9e3eac271e3602737222fae41b30ea347941eaad056c7",
    "research/r076j_local_edge_extrapolation_reconstruction_qa_report.md": "0a59566aad669f72e9c013f1b4a02b3d35a8232fcd4a2a3781b458cc0e26cf8c",
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
        resolved = subprocess.check_output(["git", "-C", str(SOURCE), "rev-parse", f"{commit}^{{commit}}"], text=True).strip()
        if resolved != commit:
            raise SystemExit(f"frozen commit drift: {resolved}")
    if subprocess.check_output(["git", "-C", str(SOURCE), "rev-parse", f"{SOURCE_COMMIT}^"], text=True).strip() != CORE_PARENT_COMMIT:
        raise SystemExit("core parent drift")
    if subprocess.check_output(["git", "-C", str(SOURCE), "rev-parse", f"{HANDOFF_COMMIT}^"], text=True).strip() != SOURCE_COMMIT:
        raise SystemExit("handoff parent drift")
    if sha256(git_bytes(HANDOFF_COMMIT, HANDOFF_PATH)) != HANDOFF_SHA256:
        raise SystemExit("handoff drift")
    if sha256(git_bytes(HANDOFF_COMMIT, HANDOFF_AUDIT_PATH)) != HANDOFF_AUDIT_SHA256:
        raise SystemExit("handoff independent-audit drift")
    changed = subprocess.check_output(["git", "-C", str(SOURCE), "show", "--pretty=format:", "--name-only", SOURCE_COMMIT], text=True).split()
    if set(changed) != set(FROZEN) or len(changed) != len(FROZEN):
        raise SystemExit("core changed-path whitelist drift")
    for relative, expected in FROZEN.items():
        write_exact(relative, git_bytes(SOURCE_COMMIT, relative), expected)
    print({
        "status": "PASS", "release": "R0.76J Step 61", "source": SOURCE_COMMIT,
        "coreParentCommit": CORE_PARENT_COMMIT, "handoffCommit": HANDOFF_COMMIT,
        "handoffSha256": HANDOFF_SHA256, "handoffIndependentAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN), "formalFigureRequired": False, "recapRequired": False,
    })


if __name__ == "__main__":
    main()
