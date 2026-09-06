#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Import the frozen ClayB-EulerCompactnessScreen package from committed bytes."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "navier-stokes-r074m"
SOURCE_COMMIT = "14d5a44345c6835aff8dfd19123c979ae185b471"
BASE_COMMIT = "b85838c7139c7e6e248d3c1dfebd0866a92a166a"
FREEZE_COMMIT = "e22c9a5669dbc3cc29fa2e0d313d3656836774c2"
RELEASE_ID = "ClayB-EulerCompactnessScreen-20260906"
MANIFEST_PATH = "research/clay_b_euler_compactness_screen_release_20260906.json"
MANIFEST_HASH = "d2ed70e3b74ba7de548afb718f3cf7fc282c28b5aa4ccc2521555a90d84c6526"
CHECK_ONLY = "--check-only" in sys.argv[1:]
LEDGER = ROOT / "research/clay_b_euler_compactness_screen_frozen_ledger_20260906.json"


def show(commit: str, path: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{commit}:{path}"], cwd=SOURCE, check=True, stdout=subprocess.PIPE
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
if manifest["logical_predecessor"] != "ClayB-FixedHistoryScreen-20260906":
    raise RuntimeError("logical predecessor drift")
if manifest["source_commit"] != SOURCE_COMMIT or manifest["base_commit"] != BASE_COMMIT:
    raise RuntimeError("source/base commit drift")
if manifest["status"] != "RESEARCH_COMPLETE" or digest(manifest_bytes) != MANIFEST_HASH:
    raise RuntimeError("frozen manifest status or hash drift")
if len(manifest["files"]) != 14 or len(manifest["dependencies"]) != 90:
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
if formula_tags != 48 or len(rows) != 104:
    raise RuntimeError("formula or ledger row count drift")
envelope = [{
    "path": MANIFEST_PATH,
    "sha256": digest(manifest_bytes),
    "bytes": len(manifest_bytes),
    "commit": FREEZE_COMMIT,
}]
ledger = {
    "schemaVersion": "clay-b-euler-compactness-screen-portable-ledger-v1",
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
    "newFormulaTagCount": manifest["qa"]["new_formula_tags_checked"],
    "arithmeticCheckCount": manifest["qa"]["exact_arithmetic_checks"],
    "negativeControlCount": manifest["qa"]["limited_negative_controls"],
    "previousFrozenRowCount": manifest["qa"]["prior_frozen_rows_unchanged"],
    "historicalStageFileCount": manifest["qa"]["previous_internal_stage_files_unchanged"],
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
    "schemaVersion": "clay-b-euler-compactness-screen-frozen-import-v1",
    "releaseId": RELEASE_ID,
    "status": "PASS",
    "mode": "check-only" if CHECK_ONLY else "apply",
    "scientificFiles": len(manifest["files"]),
    "dependencyFiles": len(manifest["dependencies"]),
    "verifiedFiles": len(rows),
    "textSources": manifest["qa"]["text_sources_checked"],
    "formulaTags": formula_tags,
    "newFormulaTags": manifest["qa"]["new_formula_tags_checked"],
    "arithmeticChecks": manifest["qa"]["exact_arithmetic_checks"],
    "historicalStageFiles": manifest["qa"]["previous_internal_stage_files_unchanged"],
    "manifestSha256": digest(manifest_bytes),
}, ensure_ascii=False))
