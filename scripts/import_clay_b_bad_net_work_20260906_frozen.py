#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Import the frozen ClayB-BadTimeNetWork package from committed bytes."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "navier-stokes-r074m"
SOURCE_COMMIT = "22c0064338dbad20a6cc37cf054c24850cd2dc2e"
BASE_COMMIT = "8843d99338d62cdbc3067eaaead81ad93d7326ba"
FREEZE_COMMIT = "ca1bf2ecad5716ef9a4a653806e4a27fbfb2957f"
CHECK_ONLY = "--check-only" in sys.argv[1:]
SCIENTIFIC = [
    "research/clay_b_mature_frequency_preflight_20260906.md",
    "research/clay_b_periodic_dissipation_wavenumber_preflight_20260906.md",
    "research/clay_b_separated_pressure_pair_preflight_20260906.md",
    "research/clay_b_global_high_high_pressure_preflight_20260906.md",
    "research/clay_b_local_high_high_pressure_preflight_20260906.md",
    "research/clay_b_fixed_regular_annulus_interface_20260906.md",
    "research/clay_b_bad_time_net_work_necessity_20260906.md",
    "research/clay_b_mature_frequency_literature_bridge_20260906.md",
    "research/clay_b_mature_frequency_internal_audit_20260906.md",
    "research/clay_b_frequency_interaction_internal_audit_20260906.md",
    "research/clay_b_local_pressure_budget_internal_audit_20260906.md",
    "research/clay_b_bad_net_work_report_20260906.md",
    "research/clay_b_bad_net_work_work_plan_20260906.md",
    "research/clay_b_bad_net_work_source_qa_20260906.json",
]
DEPENDENCIES = [
    "research/clay_b_mature_l3_budget_preflight_20260906.md",
    "research/clay_b_prescribed_centre_contract_20260905.md",
    "research/clay_b_localisation_force_ledger_20260905.md",
]
ENVELOPE = [
    "research/clay_b_bad_net_work_release_20260906.json",
    "research/clay_b_bad_net_work_handoff_20260906.md",
]
LEDGER = ROOT / "research/clay_b_bad_net_work_frozen_ledger_20260906.json"


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
if manifest["release_id"] != "ClayB-BadTimeNetWork-20260906":
    raise RuntimeError("release id drift")
if manifest["source_commit"] != SOURCE_COMMIT or manifest["base_commit"] != BASE_COMMIT:
    raise RuntimeError("source/base commit drift")
if digest(manifest_bytes) != "0bec077da9d1c64e29d7319795c730a2c710e93b8eb80cb19da864cb73527843":
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
    rows.append({"path": path, "sha256": sha, "commit": commit, "role": "scientific-source" if path in SCIENTIFIC else "dependency"})

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
    "schemaVersion": "clay-b-bad-net-work-portable-ledger-v1",
    "releaseId": "ClayB-BadTimeNetWork-20260906",
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
    "schemaVersion": "clay-b-bad-net-work-frozen-import-v1",
    "releaseId": ledger["releaseId"],
    "status": "PASS",
    "mode": "check-only" if CHECK_ONLY else "apply",
    "scientificFiles": len(SCIENTIFIC),
    "dependencyFiles": len(DEPENDENCIES),
    "formulaTags": ledger["formulaTagCount"],
    "manifestSha256": digest(manifest_bytes),
    "handoffSha256": envelope_rows[1]["sha256"],
}, ensure_ascii=False))
