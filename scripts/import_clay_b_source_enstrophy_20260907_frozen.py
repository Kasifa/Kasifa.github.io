#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Import the frozen ClayB-SourceEnstrophy package from committed bytes."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "navier-stokes-r074m"
SOURCE_COMMIT = "53f167438c058c77aa218216a014c3e504300300"
BASE_COMMIT = "363bb4b83b2b3c3db605e42e05491072cb073bf5"
FREEZE_COMMIT = "6c6186d86d22c925eb2f7e7d03ad39f291f4dfac"
RELEASE_ID = "ClayB-SourceEnstrophy-20260907"
PREDECESSOR = "ClayB-SignedMixedPressure-20260907"
MANIFEST_PATH = "research/clay_b_source_enstrophy_release_20260907.json"
MANIFEST_HASH = "9f90254f6dcbcce7c6066b4f90d6fae63d797502901ef35014531700f63eae58"
MANIFEST_BYTES = 41497
CHECK_ONLY = "--check-only" in sys.argv[1:]
LEDGER = ROOT / "research/clay_b_source_enstrophy_frozen_ledger_20260907.json"


def show(commit: str, path: str) -> bytes:
    return subprocess.run(["git", "show", f"{commit}:{path}"], cwd=SOURCE, check=True, stdout=subprocess.PIPE).stdout


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


for commit in (SOURCE_COMMIT, BASE_COMMIT, FREEZE_COMMIT):
    subprocess.run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=SOURCE, check=True)

manifest_bytes = show(FREEZE_COMMIT, MANIFEST_PATH)
manifest = json.loads(manifest_bytes)
if manifest["release_id"] != RELEASE_ID or manifest["logical_predecessor"] != PREDECESSOR:
    raise RuntimeError("release identity or logical predecessor drift")
if manifest["source_commit"] != SOURCE_COMMIT or manifest["base_commit"] != BASE_COMMIT:
    raise RuntimeError("source/base commit drift")
if manifest["status"] != "RESEARCH_FREEZE_COMPLETE":
    raise RuntimeError("frozen manifest status drift")
if digest(manifest_bytes) != MANIFEST_HASH or len(manifest_bytes) != MANIFEST_BYTES:
    raise RuntimeError("frozen manifest byte/hash drift")
if len(manifest["files"]) != 7 or len(manifest["dependencies"]) != 157:
    raise RuntimeError("frozen file count drift")

previous_path = "research/clay_b_signed_mixed_pressure_release_20260907.json"
previous_bytes = show(BASE_COMMIT, previous_path)
previous = json.loads(previous_bytes)
expected_dependencies = previous["files"] + previous["dependencies"] + [{
    "path": previous_path, "sha256": digest(previous_bytes), "bytes": len(previous_bytes),
}]
if manifest["dependencies"] != expected_dependencies:
    raise RuntimeError("dependency base identity drift")

rows = []
for role, source_rows in (("scientific-source", manifest["files"]), ("dependency", manifest["dependencies"])):
    for row in source_rows:
        path = row["path"]
        data = show(SOURCE_COMMIT, path)
        if role == "dependency" and data != show(BASE_COMMIT, path):
            raise RuntimeError(f"dependency base byte drift: {path}")
        if digest(data) != row["sha256"] or len(data) != row["bytes"]:
            raise RuntimeError(f"frozen byte/hash/size drift: {path}")
        target = ROOT / path
        if CHECK_ONLY:
            if not target.is_file() or target.read_bytes() != data:
                raise RuntimeError(f"publication copy drift: {path}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        rows.append({"path": path, "sha256": digest(data), "bytes": len(data), "commit": SOURCE_COMMIT, "role": role})

target_manifest = ROOT / MANIFEST_PATH
if CHECK_ONLY:
    if not target_manifest.is_file() or target_manifest.read_bytes() != manifest_bytes:
        raise RuntimeError("publication manifest envelope drift")
else:
    target_manifest.write_bytes(manifest_bytes)

formula_tags = manifest["claims"]["formula_tags"]["total"]
if formula_tags != 18 or len(rows) != 164 or len({row["path"] for row in rows}) != 164:
    raise RuntimeError("formula or ledger row count drift")

envelope = [{"path": MANIFEST_PATH, "sha256": digest(manifest_bytes), "bytes": len(manifest_bytes), "commit": FREEZE_COMMIT}]
ledger = {
    "schemaVersion": "clay-b-source-enstrophy-portable-ledger-v1", "releaseId": RELEASE_ID,
    "sourceRepository": "navier-stokes-r074m", "sourceCommit": SOURCE_COMMIT,
    "baseCommit": BASE_COMMIT, "freezeCommit": FREEZE_COMMIT,
    "scientificFileCount": len(manifest["files"]), "dependencyFileCount": len(manifest["dependencies"]),
    "verifiedFileCount": len(rows), "textSourceFileCount": manifest["qa"]["text_sources_checked"],
    "formulaTagCount": formula_tags, "arithmeticCheckCount": manifest["qa"]["exact_arithmetic_checks"],
    "negativeControlCount": manifest["qa"]["limited_negative_controls"],
    "previousFrozenRowCount": manifest["qa"]["prior_frozen_rows_unchanged"],
    "additionalHistoricalSourceCount": manifest["qa"]["additional_historical_sources_unchanged"],
    "files": rows, "handoffEnvelope": envelope,
}
ledger_bytes = (json.dumps(ledger, ensure_ascii=False, indent=2) + "\n").encode()
if CHECK_ONLY:
    if not LEDGER.is_file() or LEDGER.read_bytes() != ledger_bytes:
        raise RuntimeError("portable ledger drift")
else:
    LEDGER.write_bytes(ledger_bytes)

print(json.dumps({
    "schemaVersion": "clay-b-source-enstrophy-frozen-import-v1", "releaseId": RELEASE_ID,
    "status": "PASS", "mode": "check-only" if CHECK_ONLY else "apply",
    "scientificFiles": len(manifest["files"]), "dependencyFiles": len(manifest["dependencies"]),
    "verifiedFiles": len(rows), "textSources": manifest["qa"]["text_sources_checked"],
    "formulaTags": formula_tags, "arithmeticChecks": manifest["qa"]["exact_arithmetic_checks"],
    "manifestSha256": digest(manifest_bytes),
}, ensure_ascii=False))
