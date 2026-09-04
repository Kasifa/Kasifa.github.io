#!/usr/bin/env python3
"""Import only the twelve frozen R0.76F Step 57 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R076F_STEP57_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "ff0254315b2fc4f2aaab1ee6f3f2ddcaaeac7366"
CORE_PARENT_COMMIT = "01473589257b882c5b35e0d04fb58a71b36c9093"
HANDOFF_COMMIT = "52ee189e3dfaa2ea0924ed44cd2e1196b2ec3a5b"
HANDOFF_PATH = "research/r076f_publication_handoff.md"
HANDOFF_SHA256 = "5bf493b8703bb33233d846d4db8d1c621320d565a80e02a339b17431325bf06c"
HANDOFF_AUDIT_PATH = "research/r076f_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "8a2ee0b0d69aa5002119da6db10f685230d2af48e2ed09f099fcd5c5153ca45b"

FROZEN = {
    "research/r076f_exponential_spatial_observation_lower_bound.md": "48204fcbf8fe9af3f0fdc7720844c3dd8362d8767caf73de016eda7250b70973",
    "research/r076f_exponential_spatial_observation_lower_bound_primary_audit.md": "abcaa220c56d1f90c4b34061191e7cd009b8d911be3f83d705e95aa51b4d84cc",
    "research/r076f_report-source.md": "5e3939710dcfefcbc08b93761d8cdda1e655656a1bcd404b63fcea251ffd5e1e",
    "scripts/r076f_exponential_spatial_observation_lower_bound_fixtures.json": "1b11049ab482eb9b6d6b99cfdabfb4cd0a34ac4f483e3e69c5ec178dce752b5a",
    "scripts/r076f_exponential_spatial_observation_lower_bound_expected.json": "9703be8236b77e556085f9b358f4128ace4e32920a5391ebc1e2a900b232d37a",
    "scripts/r076f_exponential_spatial_observation_lower_bound_certificate.py": "2882146fba7376d1f2d83d324c816b763729c59443fa4cb1f5fbcc47778c6994",
    "scripts/r076f_exponential_spatial_observation_lower_bound_certificate_independent.rb": "191b7ee7c0e7ed9157a33606c0ed00e3d0bd1db374260b26d8d5d5b64807bf32",
    "scripts/r076f_exponential_spatial_observation_lower_bound_qa.sh": "ba4fb4db589a502fa28f4f4d307a46b046b5fe253e12e57487c5da0c52d51546",
    "research/r076f_exponential_spatial_observation_lower_bound_certificate.json": "0558eab8a7ce5ae36e1614fe0c2184debfa8550c655a86baab590fbb9ee6f259",
    "research/r076f_exponential_spatial_observation_lower_bound_certificate_report.md": "7de8bb9ce8b59704c4097616a14e09366c8cc9031acf2e2692b51bce9a785ea0",
    "research/r076f_exponential_spatial_observation_lower_bound_independent_audit.md": "8b90a9ab9b60a17f6e5cfc097f658c80ce4cb410142d72123b72bef6895ab7de",
    "research/r076f_exponential_spatial_observation_lower_bound_qa_report.md": "6cf856c79f89e759eec05f51a8aa80e5abad4c7f04bc743aea26b6d8933eb13d",
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
        "release": "R0.76F Step 57",
        "source": SOURCE_COMMIT,
        "coreParentCommit": CORE_PARENT_COMMIT,
        "handoffCommit": HANDOFF_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "handoffIndependentAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": False,
    })


if __name__ == "__main__":
    main()
