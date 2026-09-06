#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Import the frozen ClayB-FrequencyActivation package from committed bytes."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "navier-stokes-r074m"
SOURCE_COMMIT = "1674af0dc98825d0d0299fa69e3ae12398c3d8a0"
BASE_COMMIT = "c9bb03ff544c81cedeb3a6d116514d204033eb63"
FREEZE_COMMIT = "c688fca88da5a434aac5ca46971a7d800f146b39"
RELEASE_ID = "ClayB-FrequencyActivation-20260907"
PREDECESSOR = "ClayB-SourceEnstrophy-20260907"
MANIFEST_PATH = "research/clay_b_frequency_activation_release_20260907.json"
MANIFEST_HASH = "f362464072b1fcd7d8311d859aac12b4932841f40262c42343f7779ad1a64308"
MANIFEST_BYTES = 9949
CHECK_ONLY = "--check-only" in sys.argv[1:]
LEDGER = ROOT / "research/clay_b_frequency_activation_frozen_ledger_20260907.json"


def show(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"], cwd=SOURCE, check=True,
        stdout=subprocess.PIPE,
    ).stdout


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


for commit in (SOURCE_COMMIT, BASE_COMMIT, FREEZE_COMMIT):
    subprocess.run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=SOURCE, check=True)
subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE_COMMIT, FREEZE_COMMIT], cwd=SOURCE, check=True)

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
if (len(manifest["files"]), len(manifest["dependencies"]), len(manifest["provenance_records"])) != (3, 1, 4):
    raise RuntimeError("frozen file count drift")

rows = []
groups = (
    ("scientific-source", manifest["files"]),
    ("dependency", manifest["dependencies"]),
    ("provenance", manifest["provenance_records"]),
)
for role, source_rows in groups:
    for row in source_rows:
        path = row["path"]
        data = show(SOURCE_COMMIT, path)
        if digest(data) != row["sha256"] or len(data) != row["bytes"]:
            raise RuntimeError(f"frozen byte/hash/size drift: {path}")
        target = ROOT / path
        if CHECK_ONLY:
            if not target.is_file() or target.read_bytes() != data:
                raise RuntimeError(f"publication copy drift: {path}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        rows.append({
            "path": path, "sha256": digest(data), "bytes": len(data),
            "commit": SOURCE_COMMIT, "role": role,
        })

if len(rows) != 8 or len({row["path"] for row in rows}) != 8:
    raise RuntimeError("portable frozen row count drift")

target_manifest = ROOT / MANIFEST_PATH
if CHECK_ONLY:
    if not target_manifest.is_file() or target_manifest.read_bytes() != manifest_bytes:
        raise RuntimeError("publication manifest envelope drift")
else:
    target_manifest.write_bytes(manifest_bytes)

formula_tags = manifest["claims"]["formula_tags"]["total"]
if formula_tags != 17:
    raise RuntimeError("formula tag count drift")

envelope = [{
    "path": MANIFEST_PATH, "sha256": digest(manifest_bytes),
    "bytes": len(manifest_bytes), "commit": FREEZE_COMMIT,
}]
ledger = {
    "schemaVersion": "clay-b-frequency-activation-portable-ledger-v1",
    "releaseId": RELEASE_ID,
    "sourceRepository": "navier-stokes-r074m",
    "sourceCommit": SOURCE_COMMIT,
    "baseCommit": BASE_COMMIT,
    "freezeCommit": FREEZE_COMMIT,
    "scientificFileCount": len(manifest["files"]),
    "dependencyFileCount": len(manifest["dependencies"]),
    "provenanceFileCount": len(manifest["provenance_records"]),
    "verifiedFileCount": len(rows),
    "textSourceBindingCount": manifest["qa"]["text_source_bindings"],
    "formulaTagCount": formula_tags,
    "arithmeticCheckCount": manifest["qa"]["exact_arithmetic_checks"],
    "negativeControlCount": manifest["qa"]["limited_negative_controls"],
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
    "schemaVersion": "clay-b-frequency-activation-frozen-import-v1",
    "releaseId": RELEASE_ID,
    "status": "PASS",
    "mode": "check-only" if CHECK_ONLY else "apply",
    "scientificFiles": len(manifest["files"]),
    "dependencyFiles": len(manifest["dependencies"]),
    "provenanceFiles": len(manifest["provenance_records"]),
    "verifiedFiles": len(rows),
    "formulaTags": formula_tags,
    "arithmeticChecks": manifest["qa"]["exact_arithmetic_checks"],
    "manifestSha256": digest(manifest_bytes),
}, ensure_ascii=False))
