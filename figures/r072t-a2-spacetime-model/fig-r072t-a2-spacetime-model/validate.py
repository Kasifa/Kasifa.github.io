#!/usr/bin/env python3
"""Strict validation of the R0.72T analytic figure package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import re


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-formal", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    certificate = json.loads(
        (REPOSITORY / "research/certificates/r072t/certificate.json").read_text(encoding="utf-8")
    )
    if args.require_formal and manifest.get("status") != "formal":
        raise RuntimeError("formal R0.72T package required")
    if manifest.get("status") not in {"draft", "formal"}:
        raise RuntimeError("unexpected package status")
    if validation.get("status") != "passed" or not all(validation.get("checks", {}).values()):
        raise RuntimeError("automatic figure validation failed")
    if certificate.get("status") != "passed":
        raise RuntimeError("exact certificate did not pass")
    if args.require_formal:
        certificate_manifest = json.loads(
            (REPOSITORY / "research/certificates/r072t/manifest.json").read_text(encoding="utf-8")
        )
        git = manifest.get("git", {})
        certificate_commit = str(git.get("certificateCommit", ""))
        if (
            certificate_manifest.get("status") != "formal"
            or git.get("sourceCommit") != certificate_manifest.get("sourceCommit")
            or not re.fullmatch(r"[0-9a-f]{40}", certificate_commit)
            or manifest.get("qa", {}).get("visualInspectionExplicit") is not True
        ):
            raise RuntimeError("formal source/certificate/visual-QA lineage is inconsistent")
        if subprocess.run(
            ["git", "cat-file", "-e", f"{certificate_commit}^{{commit}}"],
            cwd=REPOSITORY, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        ).returncode != 0:
            raise RuntimeError("certificateCommit is not a valid Git commit")
        for name in (
            "manifest.json", "certificate.json", "independent.json",
            "crosscheck.json", "SHA256SUMS",
        ):
            relative = f"research/certificates/r072t/{name}"
            committed = subprocess.check_output(
                ["git", "show", f"{certificate_commit}:{relative}"], cwd=REPOSITORY,
            )
            working = (REPOSITORY / relative).read_bytes()
            if committed != working:
                raise RuntimeError(
                    f"working formal certificate differs from {certificate_commit}:{relative}"
                )
        subprocess.run(
            [sys.executable, "research/certificates/r072t/validate_certificate.py", "--require-formal"],
            cwd=REPOSITORY, check=True,
        )
    required_false = {
        "blockContractionProved", "periodicTransferProved", "allStartSemigroupEstimateProved",
        "combinedCubicAndTimeDriftEstimateProved", "clayMillenniumProblemSolved",
    }
    for boundary in (manifest["claimBoundary"], contract["claimBoundary"], certificate["claimBoundary"]):
        if any(boundary.get(key) is not False for key in required_false if key in boundary or boundary is not certificate["claimBoundary"]):
            raise RuntimeError("claim boundary drift")
    rows = list(csv.DictReader((ROOT / "data.csv").open(encoding="utf-8")))
    if len(rows) != 948 or {row["panel"] for row in rows} != {"A", "B", "C"}:
        raise RuntimeError("analytic sample ledger drift")
    if any(row["status"] not in {"analytic sample", "exact leading polynomial", "exact drift-only calibration"} for row in rows):
        raise RuntimeError("non-analytic figure row detected")
    for record in manifest["figure"]["outputs"]:
        path = ROOT / record["path"]
        if digest(path) != record["sha256"]:
            raise RuntimeError(f"figure output drift: {path.name}")
    for record in manifest["publication"]["assets"]:
        path = REPOSITORY / record["path"]
        master = ROOT / f"figure{path.suffix}"
        if digest(path) != digest(master) or record.get("byteIdenticalToMaster") is not True:
            raise RuntimeError(f"public asset drift: {path.name}")
    ledger_rows = (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    names = []
    for row in ledger_rows:
        expected, name = row.split("  ", 1)
        if expected != digest(ROOT / name):
            raise RuntimeError(f"SHA256SUMS drift: {name}")
        names.append(name)
    actual = sorted(path.name for path in ROOT.iterdir() if path.is_file() and path.name != "SHA256SUMS")
    if names != actual:
        raise RuntimeError("SHA256SUMS must cover every package file exactly once")
    generic = subprocess.run(
        [sys.executable, "research/validate_figure_package.py", str(ROOT)],
        cwd=REPOSITORY, text=True, capture_output=True,
    )
    if generic.returncode:
        raise RuntimeError(f"generic archive validation failed:\n{generic.stdout}\n{generic.stderr}")
    print(f"R0.72T strict figure validation: passed ({manifest['status']})")


if __name__ == "__main__":
    main()
