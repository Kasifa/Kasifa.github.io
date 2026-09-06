#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Import the frozen ClayB-CommonAdjointScreen package from committed bytes."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "navier-stokes-r074m"
SOURCE_COMMIT = "32b12bff99e7a88d6be3d1317fd125cf30a72792"
BASE_COMMIT = "7ea29a64cc1ba081e703afec4b59b3adeb9758da"
FREEZE_COMMIT = "2a2b6c9ee51cab238b11b485ae1b6b5564a75395"
RELEASE_ID = "ClayB-CommonAdjointScreen-20260906"
MANIFEST_PATH = "research/clay_b_common_adjoint_screen_release_20260906.json"
MANIFEST_HASH = "5b96d48464f0380803617bacae049eb80bd072758f5a6556eff60bf1d8c3905a"
CHECK_ONLY = "--check-only" in sys.argv[1:]
LEDGER = ROOT / "research/clay_b_common_adjoint_screen_frozen_ledger_20260906.json"


def show(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=SOURCE,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


for commit in (SOURCE_COMMIT, BASE_COMMIT, FREEZE_COMMIT):
    subprocess.run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=SOURCE, check=True)

manifest_bytes = show(FREEZE_COMMIT, MANIFEST_PATH)
manifest = json.loads(manifest_bytes)
if manifest["release_id"] != RELEASE_ID:
    raise RuntimeError("release id drift")
if manifest["logical_predecessor"] != "ClayB-EnergyAtomCostScreen-20260906":
    raise RuntimeError("logical predecessor drift")
if manifest["source_commit"] != SOURCE_COMMIT or manifest["base_commit"] != BASE_COMMIT:
    raise RuntimeError("source/base commit drift")
if manifest["status"] != "RESEARCH_COMPLETE" or digest(manifest_bytes) != MANIFEST_HASH:
    raise RuntimeError("frozen manifest status or hash drift")
if len(manifest["files"]) != 8 or len(manifest["dependencies"]) != 117:
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
        rows.append({
            "path": path,
            "sha256": sha,
            "bytes": len(data),
            "commit": SOURCE_COMMIT,
            "role": role,
        })

target_manifest = ROOT / MANIFEST_PATH
if CHECK_ONLY:
    if not target_manifest.is_file() or target_manifest.read_bytes() != manifest_bytes:
        raise RuntimeError("publication manifest envelope drift")
else:
    target_manifest.write_bytes(manifest_bytes)

formula_tags = manifest["claims"]["formula_tags"]["total"]
if formula_tags != 57 or len(rows) != 125:
    raise RuntimeError("formula or ledger row count drift")
envelope = [{
    "path": MANIFEST_PATH,
    "sha256": digest(manifest_bytes),
    "bytes": len(manifest_bytes),
    "commit": FREEZE_COMMIT,
}]
ledger = {
    "schemaVersion": "clay-b-common-adjoint-screen-portable-ledger-v1",
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
    "arithmeticCheckCount": manifest["qa"]["exact_arithmetic_checks"],
    "negativeControlCount": manifest["qa"]["limited_negative_controls"],
    "previousFrozenRowCount": manifest["qa"]["prior_frozen_rows_unchanged"],
    "additionalHistoricalSourceCount": manifest["qa"]["additional_historical_sources_unchanged"],
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
    "schemaVersion": "clay-b-common-adjoint-screen-frozen-import-v1",
    "releaseId": RELEASE_ID,
    "status": "PASS",
    "mode": "check-only" if CHECK_ONLY else "apply",
    "scientificFiles": len(manifest["files"]),
    "dependencyFiles": len(manifest["dependencies"]),
    "verifiedFiles": len(rows),
    "textSources": manifest["qa"]["text_sources_checked"],
    "formulaTags": formula_tags,
    "arithmeticChecks": manifest["qa"]["exact_arithmetic_checks"],
    "historicalSources": manifest["qa"]["additional_historical_sources_unchanged"],
    "manifestSha256": digest(manifest_bytes),
}, ensure_ascii=False))
