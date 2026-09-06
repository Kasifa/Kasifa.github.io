#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Import the frozen ClayB-PressureWorkWindow package from committed bytes."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "navier-stokes-r074m"
SOURCE_COMMIT = "fd6fa4b2bcebb702ddc2e8c03884496dca139101"
BASE_COMMIT = "9771fa5b79b25824ce015c2e9174ae9bc9de6ae7"
FREEZE_COMMIT = "4c52c02026ce0191a121e03241d88fa6573d5536"
CHECK_ONLY = "--check-only" in sys.argv[1:]
SCIENTIFIC = [
    "research/clay_b_compact_pressure_work_preflight_20260906.md",
    "research/clay_b_short_time_pressure_work_preflight_20260906.md",
    "research/clay_b_pressure_work_internal_audit_20260906.md",
    "research/clay_b_pressure_work_freeze_audit_20260906.md",
    "research/clay_b_pressure_work_literature-boundary_20260906.md",
    "research/clay_b_pressure_work_report-source_20260906.md",
    "research/clay_b_signed_work_work_plan_20260906.md",
]
DEPENDENCIES = [
    "research/clay_b_pressure_sign_20260906.md",
    "research/clay_b_pressure_residual_obstruction_20260906.md",
    "research/clay_b_mature_l3_budget_preflight_20260906.md",
    "research/clay_b_prescribed_centre_contract_20260905.md",
]
ENVELOPE = [
    "research/clay_b_pressure_work_release_20260906.json",
    "research/clay_b_pressure_work_handoff_20260906.md",
]
LEDGER = ROOT / "research/clay_b_pressure_work_frozen_ledger_20260906.json"


def show(commit: str, path: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=SOURCE,
        check=True,
        stdout=subprocess.PIPE,
    )
    return completed.stdout


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


for commit in (SOURCE_COMMIT, BASE_COMMIT, FREEZE_COMMIT):
    subprocess.run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=SOURCE, check=True)

manifest_bytes = show(FREEZE_COMMIT, ENVELOPE[0])
manifest = json.loads(manifest_bytes)
if manifest["release_id"] != "ClayB-PressureWorkWindow-20260906":
    raise RuntimeError("release id drift")
if manifest["source_commit"] != SOURCE_COMMIT or manifest["base_commit"] != BASE_COMMIT:
    raise RuntimeError("source/base commit drift")
if digest(manifest_bytes) != "d3b0d12b782ba2fb74f86bd2202b87209a706e25c003fdcc856b5124b392f90c":
    raise RuntimeError("frozen manifest hash drift")

expected = {row["path"]: row["sha256"] for row in manifest["files"] + manifest["dependencies"]}
rows = []
for path in SCIENTIFIC + DEPENDENCIES:
    commit = SOURCE_COMMIT if path in SCIENTIFIC else BASE_COMMIT
    data = show(commit, path)
    sha = digest(data)
    if expected.get(path) != sha:
        raise RuntimeError(f"frozen hash drift: {path}")
    target = ROOT / path
    if CHECK_ONLY:
        if not target.is_file() or target.read_bytes() != data:
            raise RuntimeError(f"publication copy drift: {path}")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    rows.append({
        "path": path,
        "sha256": sha,
        "commit": commit,
        "role": "scientific-source" if path in SCIENTIFIC else "dependency",
    })

envelope_rows = []
for path in ENVELOPE:
    data = show(FREEZE_COMMIT, path)
    target = ROOT / path
    if CHECK_ONLY:
        if not target.is_file() or target.read_bytes() != data:
            raise RuntimeError(f"publication envelope drift: {path}")
    else:
        target.write_bytes(data)
    envelope_rows.append({"path": path, "sha256": digest(data), "commit": FREEZE_COMMIT})

ledger = {
    "schemaVersion": "clay-b-pressure-work-portable-ledger-v1",
    "releaseId": "ClayB-PressureWorkWindow-20260906",
    "sourceRepository": "navier-stokes-r074m",
    "sourceCommit": SOURCE_COMMIT,
    "baseCommit": BASE_COMMIT,
    "freezeCommit": FREEZE_COMMIT,
    "scientificFileCount": len(SCIENTIFIC),
    "dependencyFileCount": len(DEPENDENCIES),
    "formulaTagCount": sum(row["formula_tags"] for row in manifest["files"]),
    "files": rows,
    "handoffEnvelope": envelope_rows,
}
ledger_bytes = (json.dumps(ledger, ensure_ascii=False, indent=2) + "\n").encode()
if CHECK_ONLY:
    if not LEDGER.is_file() or LEDGER.read_bytes() != ledger_bytes:
        raise RuntimeError("portable ledger drift")
else:
    LEDGER.write_bytes(ledger_bytes)

print(json.dumps({
    "schemaVersion": "clay-b-pressure-work-frozen-import-v1",
    "releaseId": ledger["releaseId"],
    "status": "PASS",
    "mode": "check-only" if CHECK_ONLY else "apply",
    "scientificFiles": len(SCIENTIFIC),
    "dependencyFiles": len(DEPENDENCIES),
    "formulaTags": ledger["formulaTagCount"],
    "manifestSha256": digest(manifest_bytes),
    "handoffSha256": envelope_rows[1]["sha256"],
}, ensure_ascii=False))
