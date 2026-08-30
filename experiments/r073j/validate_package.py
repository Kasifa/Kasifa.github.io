#!/usr/bin/env python3
"""Fail-closed validator for the sealed R0.73J experiment package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

import seal_package as seal


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def verify_record(row: dict, *, committed: bool = False, commit: str = "") -> None:
    relative = str(row.get("path", ""))
    path = ROOT / relative
    seal.require(path.is_file() and not path.is_symlink(),
                 "manifest target is absent: " + relative)
    seal.require(path.stat().st_size == row.get("bytes"),
                 "manifest byte count drift: " + relative)
    seal.require(seal.sha256(path) == row.get("sha256"),
                 "manifest SHA-256 drift: " + relative)
    if committed:
        seal.require(seal.commit_bytes(commit, relative) == path.read_bytes(),
                     "committed binding drift: " + relative)


def verify_ledger() -> int:
    ledger = HERE / "SHA256SUMS"
    seal.require(ledger.is_file() and not ledger.is_symlink(),
                 "SHA256SUMS is absent")
    rows: list[str] = []
    for line in ledger.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\\r\n]+)", line)
        seal.require(match is not None, "malformed SHA256SUMS row: " + line)
        expected, name = match.groups()
        path = HERE / name
        seal.require(path.is_file() and not path.is_symlink(),
                     "SHA256SUMS target is absent: " + name)
        seal.require(seal.sha256(path) == expected,
                     "SHA256SUMS mismatch: " + name)
        rows.append(name)
    actual = sorted(
        path.name for path in HERE.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    seal.require(rows == sorted(set(rows)) == actual,
                 "SHA256SUMS is not an exact flat inventory")
    return len(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-commit", action="store_true")
    args = parser.parse_args()
    payloads = seal.validate_frozen_inputs()
    manifest = seal.strict_json(HERE / "manifest.json")
    summary = seal.strict_json(HERE / "summary.json")
    environment = seal.strict_json(HERE / "environment.json")

    seal.require(manifest.get("schemaVersion") ==
                 "r073j-validated-computation-manifest-v1",
                 "manifest schema drift")
    seal.require(manifest.get("status") == "passed" and
                 manifest.get("allChecksPass") is True,
                 "manifest is not passed")
    seal.require(manifest.get("diagnosticOnly") is False,
                 "continuum theorem was mislabeled diagnostic-only")
    commit = str(manifest.get("sourceCommit", ""))
    seal.require(commit == summary.get("sourceCommit") ==
                 environment.get("sourceCommit"),
                 "source-commit binding drift")
    seal.require_commit(commit)

    expected_sources = set(seal.SOURCE_PATHS)
    expected_evidence = {f"experiments/r073j/{name}" for name in seal.EVIDENCE_NAMES}
    source_rows = manifest.get("sourceBindings", [])
    evidence_rows = manifest.get("evidenceBindings", [])
    generated_rows = manifest.get("generatedBindings", [])
    seal.require({row.get("path") for row in source_rows} == expected_sources,
                 "source inventory drift")
    seal.require({row.get("path") for row in evidence_rows} == expected_evidence,
                 "evidence inventory drift")
    seal.require({row.get("path") for row in generated_rows} ==
                 {"environment.json", "summary.json"},
                 "generated inventory drift")
    for row in source_rows + evidence_rows:
        verify_record(row, committed=args.require_commit, commit=commit)
    for row in generated_rows:
        path = HERE / row["path"]
        seal.require(path.stat().st_size == row.get("bytes") and
                     seal.sha256(path) == row.get("sha256"),
                     "generated binding drift: " + row["path"])

    theorem = summary.get("theorem", {})
    seal.require(theorem.get("rootInterval") ==
                 "167/1000 < lambda_0(d) < 173/1000",
                 "root interval drift")
    seal.require(theorem.get("onlySpectrumRightOf") == "Re(lambda) > 11/100",
                 "rightmost threshold drift")
    seal.require(theorem.get("conservativeGap") == "1/20",
                 "gap constant drift")
    boundary = summary.get("claimBoundary", {})
    seal.require(boundary.get("continuumSpectralBranchCertified") is True,
                 "supported continuum claim missing")
    for key in (
        "viscousRankOneBranchCertified",
        "nonselfadjointAdiabaticRemainderCertified",
        "transverseThreeDimensionalClosureCertified",
        "finiteTimeSingularityCertified",
        "clayProblemSolved",
    ):
        seal.require(boundary.get(key) is False, "claim boundary escaped: " + key)
    seal.require(manifest.get("sharedRawGridLimitationDeclared") is True,
                 "shared-grid limitation absent")
    seal.require(manifest.get("naturalBoxAuditIsPrerequisite") is False,
                 "natural-box spot audit was promoted to a prerequisite")
    seal.require(payloads["deep"].get("status") in {"passed", "inconclusive"},
                 "deep natural-box state drift")

    ledger_count = verify_ledger()
    print(json.dumps({
        "status": "passed",
        "sourceCommit": commit,
        "sourceBindings": len(source_rows),
        "evidenceBindings": len(evidence_rows),
        "ledgerFiles": ledger_count,
        "commitBindingsChecked": args.require_commit,
        "deepNaturalBoxStatus": payloads["deep"]["status"],
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
