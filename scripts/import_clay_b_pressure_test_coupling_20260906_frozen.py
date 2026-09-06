#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Import the frozen ClayB-PressureTestCoupling package from committed bytes."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "navier-stokes-r074m"
SOURCE_COMMIT = "ebaf7e8a51cf08f890caf727850f1b65d6fbd0fd"
BASE_COMMIT = "e887f8fdfee7f1e88d5724d1233832db39fbf1bf"
FREEZE_COMMIT = "2e3706c5fe1f43586b1e9a59a24cb41d04935c9a"
RELEASE_ID = "ClayB-PressureTestCoupling-20260906"
MANIFEST_HASH = "8feb586d6e948d592e92c5a4583467a816e231071aec30b826324e3f9b4f90df"
HANDOFF_HASH = "c766e5bb172abaa1434abe74aed0e37f3b563e94dcff53441cd8823bd9ae0d4d"
CHECK_ONLY = "--check-only" in sys.argv[1:]
ENVELOPE = [
    "research/clay_b_pressure_test_coupling_release_20260906.json",
    "research/clay_b_pressure_test_coupling_handoff_20260906.md",
]
LEDGER = ROOT / "research/clay_b_pressure_test_coupling_frozen_ledger_20260906.json"


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
if manifest["release_id"] != RELEASE_ID:
    raise RuntimeError("release id drift")
if manifest["source_commit"] != SOURCE_COMMIT or manifest["base_commit"] != BASE_COMMIT:
    raise RuntimeError("source/base commit drift")
if digest(manifest_bytes) != MANIFEST_HASH:
    raise RuntimeError("frozen manifest hash drift")
if len(manifest["files"]) != 12 or len(manifest["dependencies"]) != 25:
    raise RuntimeError("frozen file count drift")

rows = []
for role, source_rows in (("scientific-source", manifest["files"]), ("dependency", manifest["dependencies"])):
    for row in source_rows:
        path = row["path"]
        commit = row.get("commit", SOURCE_COMMIT)
        data = show(commit, path)
        sha = digest(data)
        if sha != row["sha256"] or len(data) != row["bytes"]:
            raise RuntimeError(f"frozen byte/hash drift: {path}")
        target = ROOT / path
        if CHECK_ONLY:
            if not target.is_file() or target.read_bytes() != data:
                raise RuntimeError(f"publication copy drift: {path}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        rows.append({"path": path, "sha256": sha, "bytes": len(data), "commit": commit, "role": role})

envelope_rows = []
for path, expected_hash in zip(ENVELOPE, (MANIFEST_HASH, HANDOFF_HASH)):
    data = show(FREEZE_COMMIT, path)
    sha = digest(data)
    if sha != expected_hash:
        raise RuntimeError(f"frozen envelope drift: {path}")
    target = ROOT / path
    if CHECK_ONLY:
        if not target.is_file() or target.read_bytes() != data:
            raise RuntimeError(f"publication envelope drift: {path}")
    else:
        target.write_bytes(data)
    envelope_rows.append({"path": path, "sha256": sha, "bytes": len(data), "commit": FREEZE_COMMIT})

formula_tags = sum(row["formula_tags"] for row in manifest["files"])
if formula_tags != 202 or len(rows) != 37:
    raise RuntimeError("formula or ledger row count drift")

ledger = {
    "schemaVersion": "clay-b-pressure-test-coupling-portable-ledger-v1",
    "releaseId": RELEASE_ID,
    "sourceRepository": "navier-stokes-r074m",
    "sourceCommit": SOURCE_COMMIT,
    "baseCommit": BASE_COMMIT,
    "freezeCommit": FREEZE_COMMIT,
    "scientificFileCount": len(manifest["files"]),
    "dependencyFileCount": len(manifest["dependencies"]),
    "verifiedFileCount": len(rows),
    "formulaTagCount": formula_tags,
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
    "schemaVersion": "clay-b-pressure-test-coupling-frozen-import-v1",
    "releaseId": RELEASE_ID,
    "status": "PASS",
    "mode": "check-only" if CHECK_ONLY else "apply",
    "scientificFiles": len(manifest["files"]),
    "dependencyFiles": len(manifest["dependencies"]),
    "verifiedFiles": len(rows),
    "formulaTags": formula_tags,
    "manifestSha256": digest(manifest_bytes),
    "handoffSha256": envelope_rows[1]["sha256"],
}, ensure_ascii=False))
