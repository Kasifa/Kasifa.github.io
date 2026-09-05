#!/usr/bin/env python3
"""Import the frozen Clay-B two-scale handoff without widening its claims."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get(
    "CLAY_B_TWO_SCALE_SOURCE",
    "/Users/kasifa/Documents/Math/navier-stokes-r074m",
))
BASE_COMMIT = "bbe05cfc584b550d52b5f2c899dfc5e32491114d"
SOURCE_COMMIT = "59e628a44e71b5bc54317db16758d9e6efd91334"
HANDOFF_COMMIT = "a09229a714247c6f6e959661ba428e91c1cb3ab1"
HANDOFF_PATH = "research/clay_b_two_scale_handoff_20260905.md"
MANIFEST_PATH = "research/clay_b_two_scale_release_20260905.json"
HANDOFF_SHA256 = "615cb15e3ec6998e59c0380b83d93c1c1637c16ea6fa4a74dc05ae240f73437d"
MANIFEST_SHA256 = "a952832a51f5870d797d1e18aeb9e7306ed82ee31b78f100b535e67122ed87c1"

FROZEN = {
    "research/clay_b_two_scale_energy_working_20260905.md": (
        SOURCE_COMMIT, "c26b430c47df2f43096a099a99202ba1af315e0a59d59a50214779ca84038015"
    ),
    "research/clay_b_two_scale_paid_budget_20260905.md": (
        SOURCE_COMMIT, "656a100de072f834a8d1a64322bac4a099aba224b22b7578135b8a65fb94d0e5"
    ),
    "research/clay_b_two_scale_report-source_20260905.md": (
        SOURCE_COMMIT, "0d554d41488f4187d36d1c369c0eda172af5d71ac1a665caa7e981073a0d3f90"
    ),
    "research/clay_b_two_scale_independent_audit_20260905.md": (
        SOURCE_COMMIT, "8e44b259e80f9bfd4974e66c45928c4d539df17a1963ba0bc455f046ce8fa625"
    ),
    "research/clay_b_two_scale_work_plan_20260905.md": (
        SOURCE_COMMIT, "d73c7d850453fc3a7121ab087fc25679b3bf69ce173ee0677e56b3718fb8e827"
    ),
    "research/clay_b_two_scale_fourier_certificate_20260905.json": (
        SOURCE_COMMIT, "76f66cd51d5ab10b4140ccb6c8d042b5cb8317fdaeb5e8b805b1df55d734e48d"
    ),
    "scripts/clay_b_two_scale_fourier_check.py": (
        SOURCE_COMMIT, "473def4505df659ea393d7daee6e0dccaa082f3563f1033deacf9dceb314f90f"
    ),
    "research/clay_b_prescribed_centre_contract_20260905.md": (
        BASE_COMMIT, "d82a36827a7e4b956079db1d66101478ffbb6b743cb65b6d4d0b317c37119f2c"
    ),
    "research/clay_b_cross_scale_path_preflight_20260905.md": (
        BASE_COMMIT, "5e0d3535286413432181ff369d5328af9d3794e921c567808bfa92f381ddeab6"
    ),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(SOURCE), "show", f"{commit}:{path}"])


def resolve_commit(commit: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(SOURCE), "rev-parse", f"{commit}^{{commit}}"], text=True
    ).strip()


def write_exact(path: str, data: bytes, expected: str) -> None:
    if sha256(data) != expected:
        raise SystemExit(f"source hash drift: {path}")
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    if target.read_bytes() != data:
        raise SystemExit(f"import byte drift: {path}")


def main() -> None:
    for commit in (BASE_COMMIT, SOURCE_COMMIT, HANDOFF_COMMIT):
        if resolve_commit(commit) != commit:
            raise SystemExit(f"frozen commit drift: {commit}")
    for earlier, later, label in (
        (BASE_COMMIT, SOURCE_COMMIT, "base-to-source"),
        (SOURCE_COMMIT, HANDOFF_COMMIT, "source-to-handoff"),
    ):
        result = subprocess.run(
            ["git", "-C", str(SOURCE), "merge-base", "--is-ancestor", earlier, later],
            check=False,
        )
        if result.returncode != 0:
            raise SystemExit(f"commit ancestry drift: {label}")

    handoff = git_bytes(HANDOFF_COMMIT, HANDOFF_PATH)
    manifest_bytes = git_bytes(HANDOFF_COMMIT, MANIFEST_PATH)
    write_exact(HANDOFF_PATH, handoff, HANDOFF_SHA256)
    write_exact(MANIFEST_PATH, manifest_bytes, MANIFEST_SHA256)
    manifest = json.loads(manifest_bytes)
    if manifest.get("release_id") != "ClayB-TwoScale-20260905":
        raise SystemExit("release identity drift")
    declared = {
        row["path"]: (row.get("commit", SOURCE_COMMIT), row["sha256"])
        for row in [*manifest["files"], *manifest["dependencies"]]
    }
    if declared != FROZEN:
        raise SystemExit("manifest frozen whitelist drift")

    for path, (commit, expected) in FROZEN.items():
        write_exact(path, git_bytes(commit, path), expected)

    ledger = {
        "schemaVersion": "clay-b-two-scale-frozen-ledger-v1",
        "releaseId": "ClayB-TwoScale-20260905",
        "sourceCommit": SOURCE_COMMIT,
        "baseContractCommit": BASE_COMMIT,
        "handoffCommit": HANDOFF_COMMIT,
        "scientificFileCount": 7,
        "dependencyFileCount": 2,
        "handoffEnvelopeCount": 2,
        "files": [
            {"path": path, "commit": commit, "sha256": digest}
            for path, (commit, digest) in sorted(FROZEN.items())
        ],
        "handoffEnvelope": [
            {"path": HANDOFF_PATH, "commit": HANDOFF_COMMIT, "sha256": HANDOFF_SHA256},
            {"path": MANIFEST_PATH, "commit": HANDOFF_COMMIT, "sha256": MANIFEST_SHA256},
        ],
    }
    ledger_path = ROOT / "research/clay_b_two_scale_frozen_ledger_20260905.json"
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "PASS",
        "releaseId": ledger["releaseId"],
        "sourceCommit": SOURCE_COMMIT,
        "handoffCommit": HANDOFF_COMMIT,
        "scientificAndDependencyFiles": "7+2",
        "handoffEnvelopeFiles": 2,
        "formalFigureRequired": False,
        "simulationRequired": False,
        "recapRequired": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
