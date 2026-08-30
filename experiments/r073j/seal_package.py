#!/usr/bin/env python3
"""Seal the complete R0.73J validated-computation package.

The scientific computations are not rerun here.  This script validates their
frozen decisions, binds every source/evidence file to an immutable git commit,
and writes environment.json, summary.json, manifest.json, and SHA256SUMS.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import socket
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

GENERATED = {"environment.json", "summary.json", "manifest.json", "SHA256SUMS"}

SOURCE_PATHS = (
    "experiments/r073j/README.md",
    "experiments/r073j/requirements.txt",
    "experiments/r073j/command.txt",
    "experiments/r073j/config.json",
    "experiments/r073j/overlap_config.json",
    "experiments/r073j/certify_contours.py",
    "experiments/r073j/analyze_contours_clenshaw.py",
    "experiments/r073j/certify_overlap.py",
    "experiments/r073j/analyze_overlap_midpoint_bernstein.py",
    "experiments/r073j/independent_validate.py",
    "experiments/r073j/independent_validate_overlap.py",
    "experiments/r073j/independent_natural_box_validate.py",
    "experiments/r073j/independent_natural_box_refine.py",
    "experiments/r073j/independent_natural_box_refine_deep.py",
    "experiments/r073j/seal_package.py",
    "experiments/r073j/validate_package.py",
    "research/r073j_interval_core.py",
    "research/r073j_chebyshev.py",
    "research/r073j_overlap_core.py",
    "research/r073j_analytic_proof.md",
    "research/r073j_analytic_audit.md",
    "research/r073j_overlap_analytic_proof.md",
    "research/r073j_continuum_branch_theorem.md",
    "research/r073j_adversarial_audit.md",
    "research/r073j_literature_audit.md",
    "research/r073j_gap_matrix.md",
    "research/r073j_bilingual_dictionary.md",
    "research/r073j_report-source.md",
)

EVIDENCE_NAMES = (
    "contour_grid_checkpoint.json",
    "contour_certificate.json",
    "progress.ndjson",
    "resources.ndjson",
    "analysis_progress.ndjson",
    "overlap_grid_checkpoint.json",
    "overlap_certificate.json",
    "overlap_progress.ndjson",
    "overlap_resources.ndjson",
    "overlap_analysis_progress.ndjson",
    "independent_validation.json",
    "independent_overlap_validation.json",
    "independent_overlap_validation.ndjson",
    "natural_box_validation.json",
    "natural_box_progress.ndjson",
    "natural_box_resources.ndjson",
    "natural_box_refinement.json",
    "natural_box_refinement_progress.ndjson",
    "natural_box_refinement_resources.ndjson",
    "natural_box_refinement_deep.json",
    "natural_box_refinement_deep_progress.ndjson",
    "natural_box_refinement_deep_resources.ndjson",
    "failure_ledger.json",
)

FROZEN_HASHES = {
    "research/r073j_analytic_proof.md":
        "81061d6f77e97fca33dafa0643820ab3860ae02b4042fe742eac1d91f1f108f0",
    "research/r073j_analytic_audit.md":
        "f134d4a828ed0f91c62899a41e9640b8e5ed211f375a4a92913e76a1f537de5e",
    "research/r073j_overlap_analytic_proof.md":
        "89c94e9d3ab9cd892f4f20ff8d2a3932b3f5fef6e82135ea2e64f39148c42f02",
    "experiments/r073j/contour_certificate.json":
        "60c770beaf0dc9a3da99ba6ab7bff234b506aa7d8bc72a0aad7b55471b571a38",
    "experiments/r073j/overlap_certificate.json":
        "12e1505cacb807d83a611b96d5b928bd4302c9faef16030566d3e178234180ab",
    "experiments/r073j/independent_validation.json":
        "203b7af48933cdb49c0a0b59751c0b0435cf26ae48ea01e08f203900ad554d57",
    "experiments/r073j/independent_natural_box_validate.py":
        "de1bd217204681af133a3f7c0a1441d33267bb07104093980edde9b3fd959dad",
    "experiments/r073j/natural_box_validation.json":
        "2d92b6055ba847ffeda2a36a11d7c294df6d65925fd5e7dd00ec0cf6f7645c9a",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def strict_json(path: Path) -> dict:
    def reject(value: str) -> None:
        raise ValueError("non-finite JSON constant: " + value)

    def unique(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key: " + key)
            result[key] = value
        return result

    value = json.loads(
        path.read_text(encoding="utf-8"),
        parse_constant=reject,
        object_pairs_hook=unique,
    )
    require(isinstance(value, dict), f"JSON root is not an object: {path}")
    return value


def record(path: Path, relative: Path) -> dict[str, object]:
    return {
        "path": relative.as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def git_output(*arguments: str) -> str:
    return subprocess.check_output(
        ["git", *arguments], cwd=ROOT, text=True
    ).strip()


def require_commit(commit: str) -> None:
    require(len(commit) == 40 and all(c in "0123456789abcdef" for c in commit),
            "source commit must be a full lowercase SHA-1")
    subprocess.run(
        ["git", "cat-file", "-e", commit + "^{commit}"],
        cwd=ROOT, check=True, capture_output=True,
    )


def commit_bytes(commit: str, relative: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{commit}:{relative}"], cwd=ROOT
    )


def validate_frozen_inputs() -> dict[str, dict]:
    for relative in SOURCE_PATHS:
        path = ROOT / relative
        require(path.is_file() and not path.is_symlink(),
                "required source is absent: " + relative)
    for name in EVIDENCE_NAMES:
        path = HERE / name
        require(path.is_file() and not path.is_symlink(),
                "required evidence is absent: " + name)
    for relative, expected in FROZEN_HASHES.items():
        require(sha256(ROOT / relative) == expected,
                "frozen SHA-256 drift: " + relative)

    contour = strict_json(HERE / "contour_certificate.json")
    overlap = strict_json(HERE / "overlap_certificate.json")
    independent = strict_json(HERE / "independent_validation.json")
    independent_overlap = strict_json(HERE / "independent_overlap_validation.json")
    natural = strict_json(HERE / "natural_box_validation.json")
    refine = strict_json(HERE / "natural_box_refinement.json")
    deep = strict_json(HERE / "natural_box_refinement_deep.json")
    failure = strict_json(HERE / "failure_ledger.json")

    require(contour.get("status") == "passed", "contour certificate did not pass")
    cd = contour.get("decisions", {})
    require(cd.get("globalBoundaryNonzeroForAllD") is True,
            "global boundary decision escaped")
    require(cd.get("localBoundaryNonzeroForAllD") is True,
            "local boundary decision escaped")
    require(cd.get("globalBasePositiveOrientationWinding") == 1,
            "global winding is not one")
    require(cd.get("localBasePositiveOrientationWinding") == 1,
            "local winding is not one")
    require(contour.get("arithmetic", {}).get("odePointCount") == 21632,
            "contour ODE point count drift")

    require(overlap.get("status") == "passed", "overlap certificate did not pass")
    od = overlap.get("decisions", {})
    require(od.get("auxiliaryRectangleKineticQuotientAtLeastOneHalf") is True,
            "overlap threshold decision escaped")
    require(od.get("auxiliaryRectanglePhaseAnchorNonzero") is True,
            "phase-anchor decision escaped")
    require(overlap.get("arithmetic", {}).get("pointCount") == 841,
            "overlap ODE point count drift")

    require(independent.get("status") == "passed", "contour audit did not pass")
    require(independent.get("classification") ==
            "independent-postprocessing-from-shared-raw-grid",
            "contour audit independence boundary drift")
    require(independent_overlap.get("status") == "passed",
            "overlap audit did not pass")
    boundary = independent_overlap.get("independenceBoundary", {})
    require(boundary.get("classification") ==
            "independent-post-processing-from-shared-raw-grid",
            "overlap audit failed to declare the shared raw grid")
    require("shared raw ODE grid" in boundary.get("limitation", ""),
            "overlap audit limitation text drift")
    require(independent_overlap.get("auditSource", {}).get("sha256") ==
            "30842ffbc4a5c343af38c01c7d41170531d75d94aae2188efd0ec40f1feb38e4",
            "independent overlap source hash drift")

    require(natural.get("status") == "failed", "initial natural-box history drift")
    nd = natural.get("decisions", {})
    require(nd.get("passedBoxCount") == 76 and nd.get("failedBoxCount") == 7,
            "initial natural-box 76/7 ledger drift")
    require(natural.get("interpretation", {}).get("limitation"),
            "initial natural-box limitation is absent")
    require(refine.get("status") == "inconclusive",
            "depth-two refinement history drift")
    rd = refine.get("decisions", {})
    require(rd.get("originalFailedParentCount") == 7,
            "refinement parent count drift")
    require(rd.get("secondLevelBoxCount") == 112 and
            rd.get("secondLevelPassedBoxCount") == 16 and
            rd.get("secondLevelFailedBoxCount") == 96,
            "depth-two refinement ledger drift")
    require(deep.get("status") in {"passed", "inconclusive"},
            "deep refinement has an unsupported status")
    require(deep.get("classification") ==
            "adaptive-full-cover-deep-refinement-of-natural-boxes",
            "deep refinement classification drift")

    entries = failure.get("entries", [])
    require(len(entries) == 2, "failure ledger must preserve exactly two rejected methods")
    require(all(entry.get("replacementDecision") == "passed" for entry in entries),
            "failure ledger replacement decision drift")
    require(failure.get("claimBoundary", {}).get("rawGridWasSilentlyOverwritten") is False,
            "failure ledger no-overwrite boundary drift")

    return {
        "contour": contour,
        "overlap": overlap,
        "independent": independent,
        "independentOverlap": independent_overlap,
        "natural": natural,
        "refine": refine,
        "deep": deep,
    }


def bind_commit(commit: str) -> None:
    require_commit(commit)
    for relative in SOURCE_PATHS:
        current = (ROOT / relative).read_bytes()
        require(commit_bytes(commit, relative) == current,
                "source is not byte-identical to commit: " + relative)
    for name in EVIDENCE_NAMES:
        relative = f"experiments/r073j/{name}"
        require(commit_bytes(commit, relative) == (HERE / name).read_bytes(),
                "evidence is not byte-identical to commit: " + relative)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    payloads = validate_frozen_inputs()
    source_commit = args.source_commit.strip()
    bind_commit(source_commit)

    created = datetime.now(timezone.utc).isoformat()
    environment = {
        "schemaVersion": "r073j-validated-computation-environment-v1",
        "createdAt": created,
        "host": socket.gethostname(),
        "operatingSystem": platform.platform(),
        "architecture": platform.machine(),
        "python": platform.python_version(),
        "pythonImplementation": platform.python_implementation(),
        "pythonFlint": "0.6.0",
        "arithmetic": "python-flint Arb/Acb outward-rounded ball arithmetic",
        "sourceCommit": source_commit,
        "branch": git_output("branch", "--show-current"),
        "dgxUsed": False,
        "dgxReason": "Arb arbitrary-precision interval ODE work is CPU-bound; the local 16-process run avoided transfer overhead",
        "workers": 16,
        "randomnessUsed": False,
        "selectionSeed": "f95fdac894a7ded9042c58950ea0f79603a5ef69341a01c91a36edc093de1729",
    }
    (HERE / "environment.json").write_text(canonical(environment), encoding="utf-8")

    cd = payloads["contour"]["decisions"]
    od = payloads["overlap"]["decisions"]
    iod = payloads["independentOverlap"]["decisions"]
    deep = payloads["deep"]
    summary = {
        "schemaVersion": "r073j-continuum-spectral-branch-summary-v1",
        "release": "R0.73J",
        "status": "passed",
        "evidenceClass": "validated-continuum-operator-theorem-with-interval-computation",
        "theorem": {
            "parameterInterval": "0 <= d <= 1/450",
            "rootInterval": "167/1000 < lambda_0(d) < 173/1000",
            "onlySpectrumRightOf": "Re(lambda) > 11/100",
            "otherSpectrumUpperRealPart": "11/100",
            "strictRealPartGap": "57/1000",
            "conservativeGap": "1/20",
            "algebraicallySimple": True,
            "realAnalyticBranch": True,
        },
        "contour": {
            "odePointCount": 21632,
            "globalMinimumAbsoluteLower": cd["globalMinimumAbsoluteLower"],
            "localMinimumAbsoluteLower": cd["localMinimumAbsoluteLower"],
            "globalBaseWinding": 1,
            "localBaseWinding": 1,
        },
        "overlap": {
            "odePointCount": 841,
            "primaryMinimumLower": od["minimumKineticOverlapLower"],
            "independentMinimumLower": iod["minimumKineticOverlapLower"],
            "primaryAnchorLower": od["minimumAnchorAbsoluteLower"],
            "threshold": "1/2",
        },
        "independentAudit": {
            "contour": "passed-independent-postprocessing-from-shared-raw-grid",
            "overlap": "passed-independent-postprocessing-from-shared-raw-grid",
            "naturalBoxInitial": "76 passed; 7 wrapping-inconclusive at frozen widths",
            "naturalBoxDepthTwo": "1 of 7 parents fully resolved; 6 remain wrapping-inconclusive",
            "naturalBoxDeepStatus": deep["status"],
            "naturalBoxRole": "corroborative spot audit only; not a theorem prerequisite",
        },
        "claimBoundary": {
            "continuumSpectralBranchCertified": True,
            "kineticOverlapAndPhaseAnchorCertified": True,
            "viscousRankOneBranchCertified": False,
            "nonselfadjointAdiabaticRemainderCertified": False,
            "transverseThreeDimensionalClosureCertified": False,
            "finiteTimeSingularityCertified": False,
            "clayProblemSolved": False,
        },
        "sourceCommit": source_commit,
    }
    (HERE / "summary.json").write_text(canonical(summary), encoding="utf-8")

    source_bindings = [
        record(ROOT / relative, Path(relative)) for relative in SOURCE_PATHS
    ]
    evidence_bindings = [
        record(HERE / name, Path("experiments/r073j") / name)
        for name in EVIDENCE_NAMES
    ]
    generated_bindings = [
        record(HERE / name, Path(name))
        for name in ("environment.json", "summary.json")
    ]
    manifest = {
        "schemaVersion": "r073j-validated-computation-manifest-v1",
        "release": "R0.73J",
        "status": "passed",
        "createdAt": created,
        "sourceCommit": source_commit,
        "branch": git_output("branch", "--show-current"),
        "allChecksPass": True,
        "evidenceClass": summary["evidenceClass"],
        "diagnosticOnly": False,
        "sourceBindings": source_bindings,
        "evidenceBindings": evidence_bindings,
        "generatedBindings": generated_bindings,
        "decisions": summary["theorem"],
        "claimBoundary": summary["claimBoundary"],
        "failureHistoryPreserved": True,
        "sharedRawGridLimitationDeclared": True,
        "naturalBoxAuditIsPrerequisite": False,
        "inventoryPolicy": "flat experiment package; SHA256SUMS covers every regular file except itself",
    }
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")

    names = sorted(
        path.name for path in HERE.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    (HERE / "SHA256SUMS").write_text(
        "".join(f"{sha256(HERE / name)}  {name}\n" for name in names),
        encoding="utf-8",
    )
    print(canonical({
        "status": "passed",
        "sourceCommit": source_commit,
        "sourceBindings": len(source_bindings),
        "evidenceBindings": len(evidence_bindings),
        "packageFiles": len(names) + 1,
        "deepNaturalBoxStatus": deep["status"],
    }), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
