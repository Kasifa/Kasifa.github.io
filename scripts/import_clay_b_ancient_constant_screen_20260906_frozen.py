#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Import the frozen ClayB-PressureMechanismScreen package from committed bytes."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "navier-stokes-r074m"
SOURCE_COMMIT = "4dfd49be08e9f8bb253432851669c9d632936b5c"
BASE_COMMIT = "9069f24128b0ef8db8192b1ddff998516b82a757"
FREEZE_COMMIT = "b44960f63d35f0fd269cf1fc412921df91523a9a"
RELEASE_ID = "ClayB-AncientConstantScreen-20260906"
MANIFEST_PATH = "research/clay_b_ancient_constant_screen_release_20260906.json"
MANIFEST_HASH = "9712e6cfc929cdf397428eca3c141df8720f4a0e3a7fae68fd4bc83d0db0fa33"
CHECK_ONLY = "--check-only" in sys.argv[1:]
LEDGER = ROOT / "research/clay_b_ancient_constant_screen_frozen_ledger_20260906.json"


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

manifest_bytes = show(FREEZE_COMMIT, MANIFEST_PATH)
manifest = json.loads(manifest_bytes)
if manifest["release_id"] != RELEASE_ID:
    raise RuntimeError("release id drift")
if manifest["logical_predecessor"] != "ClayB-PressureMechanismScreen-20260906":
    raise RuntimeError("logical predecessor drift")
if manifest["source_commit"] != SOURCE_COMMIT or manifest["base_commit"] != BASE_COMMIT:
    raise RuntimeError("source/base commit drift")
if manifest["status"] != "RESEARCH_COMPLETE" or digest(manifest_bytes) != MANIFEST_HASH:
    raise RuntimeError("frozen manifest status or hash drift")
if len(manifest["files"]) != 6 or len(manifest["dependencies"]) != 75:
    raise RuntimeError("frozen file count drift")

rows = []
for role, source_rows in (("scientific-source", manifest["files"]), ("dependency", manifest["dependencies"])):
    for row in source_rows:
        path = row["path"]
        data = show(SOURCE_COMMIT, path)
        sha = digest(data)
        if sha != row["sha256"] or len(data) != row["bytes"]:
            raise RuntimeError(f"frozen byte/hash/size drift: {path}")
        target = ROOT / path
        if CHECK_ONLY:
            if not target.is_file() or target.read_bytes() != data:
                raise RuntimeError(f"publication copy drift: {path}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        rows.append({"path": path, "sha256": sha, "bytes": len(data), "commit": SOURCE_COMMIT, "role": role})

target_manifest = ROOT / MANIFEST_PATH
if CHECK_ONLY:
    if not target_manifest.is_file() or target_manifest.read_bytes() != manifest_bytes:
        raise RuntimeError("publication manifest envelope drift")
else:
    target_manifest.write_bytes(manifest_bytes)

formula_tags = manifest["claims"]["formula_tags"]["total"]
if formula_tags != 18 or len(rows) != 81:
    raise RuntimeError("formula or ledger row count drift")
envelope = [{
    "path": MANIFEST_PATH,
    "sha256": digest(manifest_bytes),
    "bytes": len(manifest_bytes),
    "commit": FREEZE_COMMIT,
}]
ledger = {
    "schemaVersion": "clay-b-ancient-constant-screen-portable-ledger-v1",
    "releaseId": RELEASE_ID,
    "sourceRepository": "navier-stokes-r074m",
    "sourceCommit": SOURCE_COMMIT,
    "baseCommit": BASE_COMMIT,
    "freezeCommit": FREEZE_COMMIT,
    "scientificFileCount": len(manifest["files"]),
    "dependencyFileCount": len(manifest["dependencies"]),
    "verifiedFileCount": len(rows),
    "textSourceFileCount": manifest["qa"]["text_sources_checked"],
    "formulaTagCount": formula_tags,
    "scalingCheckCount": manifest["qa"]["exact_scaling_checks"],
    "files": rows,
    "handoffEnvelope": envelope,
}
ledger_bytes = (json.dumps(ledger, ensure_ascii=False, indent=2) + "\n").encode()
if CHECK_ONLY:
    if not LEDGER.is_file() or LEDGER.read_bytes() != ledger_bytes:
        raise RuntimeError("portable ledger drift")
else:
    LEDGER.write_bytes(ledger_bytes)

print(json.dumps({
    "schemaVersion": "clay-b-ancient-constant-screen-frozen-import-v1",
    "releaseId": RELEASE_ID,
    "status": "PASS",
    "mode": "check-only" if CHECK_ONLY else "apply",
    "scientificFiles": len(manifest["files"]),
    "dependencyFiles": len(manifest["dependencies"]),
    "verifiedFiles": len(rows),
    "textSources": manifest["qa"]["text_sources_checked"],
    "formulaTags": formula_tags,
    "scalingChecks": manifest["qa"]["exact_scaling_checks"],
    "manifestSha256": digest(manifest_bytes),
}, ensure_ascii=False))
