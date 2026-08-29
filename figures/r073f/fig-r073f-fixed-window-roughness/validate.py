#!/usr/bin/env python3
"""Fail-closed metadata-only formal seal for the R0.73F figure package."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

SOURCE_COMMIT = "5edb1702314feca3e9d47a186b30fc53079cd67a"
FIGURE_PACKAGE_COMMIT = "3a34494445de938c5cf01862b1db258e6a6d5ecf"
CERTIFICATE_COMMIT = "5f9c21f5443e5d5b7350a6d71df8ba417890291c"
PREVIOUS_MANIFEST_SHA256 = (
    "7f0296900cd6a65c01206d7344a7e6db9f869deeec5f42dfeb95ed526cd64366"
)
FIGURE_RELATIVE = "figures/r073f/fig-r073f-fixed-window-roughness"
CERTIFICATE_RELATIVE = "research/certificates/r073f/certificate.json"

ANALYTIC_PATHS = (
    "research/r073f_problem_freeze.md",
    "research/r073f_moving_dichotomy_proof.md",
    "research/r073f_gap_matrix.md",
    "research/r073f_literature_audit.md",
    "research/r073f_independent_analytic_audit.md",
    "research/r073f_report-source.md",
)

# These are the only files from the original F package that may differ. The
# added contract is metadata. Every other original blob is compared directly
# with F before any metadata is written.
CHANGED_METADATA = {
    "SHA256SUMS",
    "command.txt",
    "manifest.json",
    "validate.py",
    "validation.json",
}
ADDED_METADATA = {"contract.json"}


def configure_dependencies(path: str | None) -> None:
    if path:
        sys.path.insert(0, path)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def record(path: Path, relative_to: Path = ROOT) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(relative_to)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def git_bytes(commit: str, relative: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{commit}:{relative}"], cwd=ROOT
    )


def git_blob(commit: str, relative: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"{commit}:{relative}"], cwd=ROOT, text=True
    ).strip()


def require_commit(commit: str, label: str) -> None:
    result = subprocess.run(
        ["git", "cat-file", "-e", commit + "^{commit}"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(result.returncode == 0, label + " is not a Git commit")


def require_ancestor(older: str, newer: str, message: str) -> None:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", older, newer],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(result.returncode == 0, message)


def historical_binding(relative: str) -> dict[str, Any]:
    payload = git_bytes(SOURCE_COMMIT, relative)
    return {
        "path": relative,
        "bytes": len(payload),
        "sha256": sha256_bytes(payload),
        "sourceCommit": SOURCE_COMMIT,
    }


def package_names_at_figure_commit() -> list[str]:
    rows = subprocess.check_output(
        [
            "git",
            "ls-tree",
            "-r",
            "--name-only",
            FIGURE_PACKAGE_COMMIT,
            FIGURE_RELATIVE,
        ],
        cwd=ROOT,
        text=True,
    ).splitlines()
    prefix = FIGURE_RELATIVE + "/"
    require(rows and all(row.startswith(prefix) for row in rows),
            "original figure package is missing or not flat")
    names = [row.removeprefix(prefix) for row in rows]
    require(all("/" not in name for name in names),
            "original figure package unexpectedly contains subdirectories")
    return sorted(names)


def current_package_names() -> list[str]:
    unexpected = [
        path.name
        for path in HERE.iterdir()
        if not path.is_file() or path.is_symlink()
    ]
    require(not unexpected,
            "figure package contains a directory or symlink: " + ", ".join(unexpected))
    return sorted(path.name for path in HERE.iterdir())


def verify_immutable_figure_package(original_names: list[str]) -> None:
    expected = sorted(set(original_names) | ADDED_METADATA)
    require(current_package_names() == expected,
            "figure package inventory differs from F plus the allowed contract metadata")
    for name in original_names:
        if name in CHANGED_METADATA:
            continue
        current = (HERE / name).read_bytes()
        frozen = git_bytes(FIGURE_PACKAGE_COMMIT, f"{FIGURE_RELATIVE}/{name}")
        require(current == frozen,
                "immutable figure-package file differs from F: " + name)


def verify_complete_ledger() -> None:
    ledger = HERE / "SHA256SUMS"
    rows: list[tuple[str, str]] = []
    for line in ledger.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\\r\n]+)", line)
        require(match is not None, "malformed SHA256SUMS row")
        rows.append((match.group(2), match.group(1)))
    names = [name for name, _ in rows]
    require(names == sorted(names), "SHA256SUMS is not sorted")
    require(len(names) == len(set(names)), "SHA256SUMS has duplicate entries")
    expected = sorted(name for name in current_package_names() if name != "SHA256SUMS")
    require(names == expected, "SHA256SUMS inventory is incomplete")
    for name, expected_hash in rows:
        require(sha256(HERE / name) == expected_hash,
                "SHA256SUMS hash mismatch: " + name)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default=None)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--figure-package-commit", required=True)
    parser.add_argument("--certificate-commit", required=True)
    args = parser.parse_args()
    configure_dependencies(args.deps)

    from PIL import Image
    from pypdf import PdfReader

    for value, label in (
        (args.source_commit, "source commit"),
        (args.figure_package_commit, "figure-package commit"),
        (args.certificate_commit, "certificate commit"),
    ):
        require(bool(re.fullmatch(r"[0-9a-f]{40}", value)),
                label + " must be lowercase 40-hex")
        require_commit(value, label)
    require(args.source_commit == SOURCE_COMMIT,
            "source commit differs from the R0.73F analytic source")
    require(args.figure_package_commit == FIGURE_PACKAGE_COMMIT,
            "figure-package commit differs from F")
    require(args.certificate_commit == CERTIFICATE_COMMIT,
            "certificate commit differs from C")
    require_ancestor(SOURCE_COMMIT, FIGURE_PACKAGE_COMMIT,
                     "analytic source commit is not an ancestor of F")
    require_ancestor(FIGURE_PACKAGE_COMMIT, CERTIFICATE_COMMIT,
                     "F is not an ancestor of C")

    previous_manifest_bytes = git_bytes(
        FIGURE_PACKAGE_COMMIT, f"{FIGURE_RELATIVE}/manifest.json"
    )
    require(sha256_bytes(previous_manifest_bytes) == PREVIOUS_MANIFEST_SHA256,
            "historical F manifest hash mismatch")
    previous_manifest = json.loads(previous_manifest_bytes)
    require(previous_manifest.get("figureId") == "fig-r073f-fixed-window-roughness",
            "historical F figure identity mismatch")
    require(previous_manifest.get("status") == "validated",
            "historical F manifest was not the validated package")
    require(previous_manifest.get("git", {}).get("sourceCommit") == SOURCE_COMMIT,
            "historical F manifest source commit mismatch")

    original_names = package_names_at_figure_commit()
    verify_immutable_figure_package(original_names)

    certificate_path = ROOT / CERTIFICATE_RELATIVE
    require(certificate_path.is_file(), "R0.73F certificate is missing")
    committed_certificate = git_bytes(CERTIFICATE_COMMIT, CERTIFICATE_RELATIVE)
    require(certificate_path.read_bytes() == committed_certificate,
            "current certificate differs from C")
    certificate = json.loads(committed_certificate)
    require(certificate.get("sourceCommit") == SOURCE_COMMIT,
            "certificate source commit mismatch")
    require(certificate.get("status") == "validated",
            "certificate is not validated")
    require(all(certificate.get("checks", {}).values()),
            "certificate contains a failed check")
    require("formalFigure" not in certificate,
            "historical C unexpectedly contains a formalFigure field")
    journal_figure = certificate.get("journalFigure", {})
    require(journal_figure.get("figureId") == previous_manifest["figureId"],
            "certificate journalFigure identity mismatch")
    require(journal_figure.get("status") == "validated",
            "certificate journalFigure historical status mismatch")
    require(journal_figure.get("validationStatus") == "passed",
            "certificate journalFigure validation did not pass")
    require(journal_figure.get("visualQaStatus") == "passed",
            "certificate journalFigure visual QA did not pass")
    require(journal_figure.get("gitSealed") is False,
            "certificate journalFigure historical seal state changed")
    seal_state = certificate.get("sealState", {})
    require(seal_state.get("finiteAndFigureArtifactsContentAddressed") is True,
            "certificate does not content-address the figure")
    require(seal_state.get("finiteAndFigureArtifactsGitSealed") is False,
            "certificate historical figure seal state changed")

    certificate_source_rows = {
        row["path"]: row for row in certificate.get("sourceBindings", [])
    }
    analytic_bindings = [historical_binding(path) for path in ANALYTIC_PATHS]
    require(analytic_bindings == previous_manifest.get("sourceBindings"),
            "historical F source bindings changed")
    for binding in analytic_bindings:
        row = certificate_source_rows.get(binding["path"], {})
        require(row.get("sourceCommit") == SOURCE_COMMIT,
                "certificate source binding commit mismatch: " + binding["path"])
        require(row.get("bytes") == binding["bytes"],
                "certificate source binding size mismatch: " + binding["path"])
        require(row.get("sha256") == binding["sha256"],
                "certificate source binding hash mismatch: " + binding["path"])
        require(row.get("gitBlob") == git_blob(SOURCE_COMMIT, binding["path"]),
                "certificate source binding blob mismatch: " + binding["path"])

    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    results = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    summary = json.loads((ROOT / config["inputs"]["summary"]).read_text(encoding="utf-8"))
    independent = json.loads(
        (ROOT / config["inputs"]["independent"]).read_text(encoding="utf-8")
    )

    for item in results["inputs"]:
        path = ROOT / item["path"]
        require(path.is_file(), "missing input: " + item["path"])
        require(path.stat().st_size == item["bytes"],
                "input size changed: " + item["path"])
        require(sha256(path) == item["sha256"],
                "input hash changed: " + item["path"])
    require(previous_manifest.get("sourceData") == results["inputs"],
            "historical sourceData binding changed")
    require(results["configBinding"]["sha256"] == sha256(HERE / "config.json"),
            "figure config changed after rendering")
    require(summary["allPrimaryChecksPass"] is True, "primary checks failed")
    require(independent["allChecksPass"] is True, "independent checks failed")
    require(summary["diagnosticEndpointIsCertifiedD0"] is False,
            "diagnostic endpoint escaped its claim boundary")

    boundary = results["claimBoundary"]
    require(boundary == previous_manifest.get("claimBoundary"),
            "historical claim boundary changed")
    require(boundary["formalFiniteDiagnosticFigure"] is True,
            "formal finite diagnostic declaration missing")
    for key, value in boundary.items():
        if key != "formalFiniteDiagnosticFigure":
            require(value is False, "escaped claim boundary: " + key)

    reader = PdfReader(HERE / "figure.pdf")
    require(len(reader.pages) == 1, "PDF must contain exactly one page")
    page = reader.pages[0]
    points = [float(page.mediabox.width), float(page.mediabox.height)]
    expected_points = [
        config["widthMillimetres"] / 25.4 * 72,
        config["heightMillimetres"] / 25.4 * 72,
    ]
    require(max(abs(a - b) for a, b in zip(points, expected_points)) < 0.8,
            "PDF physical dimensions changed")
    pdf_text = page.extract_text() or ""
    for token in (
        "Fixed-window finite gains",
        "Numerical cross-checks",
        "Exact nonnormal prefactor trap",
        "Exact rotating-edge trap",
        "not certified",
    ):
        require(token in pdf_text, "PDF text missing: " + token)

    with Image.open(HERE / "figure.png") as image:
        pixels = list(image.size)
        dpi = image.info.get("dpi", (0, 0))
        require(abs(pixels[0] - 4205) <= 2 and abs(pixels[1] - 3118) <= 2,
                "PNG pixel dimensions changed")
        require(min(dpi) > 599 and max(dpi) < 601,
                "PNG is not tagged at 600 dpi")
    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    require("<image" not in svg, "SVG unexpectedly contains a raster image")
    for token in ("Fixed-window finite gains", "Exact rotating-edge trap"):
        require(token in svg, "SVG text missing: " + token)

    require(max(results["panelB"]["independentMaximumRateDifference"]) < 5e-5,
            "independent normalized-rate discrepancy exceeds threshold")
    require(summary["finiteSentinels"]["maximumDriftRatio"] <= 1.0 + 2e-12,
            "finite sampled drift exceeds the analytic comparison bound")
    require(summary["finiteSentinels"]["minimumR073BUpperSlack"] >= -2e-9,
            "R0.73B five-sixteenths sentinel failed")
    require(abs(results["panelD"]["exactBranchIntegral"] + 0.25) < 1e-15,
            "rotating counterexample exact integral changed")

    output_records: list[dict[str, Any]] = []
    content_bindings = {
        row["path"]: row for row in certificate.get("contentBindings", [])
    }
    for suffix in ("pdf", "svg", "png"):
        name = f"figure.{suffix}"
        item = record(HERE / name, HERE)
        if suffix == "png":
            item.update({"dpi": 600, "pixels": pixels})
        output_records.append(item)

        sealed = journal_figure.get(suffix, {})
        require(Path(str(sealed.get("path", ""))).name == name,
                "certificate journalFigure path mismatch: " + suffix)
        require(sealed.get("bytes") == item["bytes"],
                "certificate journalFigure size mismatch: " + suffix)
        require(sealed.get("sha256") == item["sha256"],
                "certificate journalFigure hash mismatch: " + suffix)
        if suffix == "png":
            require(sealed.get("dpi") == 600,
                    "certificate journalFigure PNG dpi mismatch")
        full_path = f"{FIGURE_RELATIVE}/{name}"
        content = content_bindings.get(full_path, {})
        require(content.get("bytes") == item["bytes"],
                "certificate content binding size mismatch: " + suffix)
        require(content.get("sha256") == item["sha256"],
                "certificate content binding hash mismatch: " + suffix)

    historical_outputs = previous_manifest.get("figure", {}).get("outputs")
    require(output_records == historical_outputs,
            "formal output records differ from F")
    previous_validation = json.loads(
        git_bytes(FIGURE_PACKAGE_COMMIT, f"{FIGURE_RELATIVE}/validation.json")
    )
    require(previous_validation.get("status") == "passed",
            "historical F validation was not passed")
    require(all(previous_validation.get("checks", {}).values()),
            "historical F validation contains a failed check")

    contract = {
        "schemaVersion": "r073f-figure-contract-v1",
        "release": "R0.73F",
        "figureId": previous_manifest["figureId"],
        "requiredOutputs": ["figure.pdf", "figure.svg", "figure.png"],
        "requiredDiagnostics": ["results.json", "validation.json"],
        "claimBoundary": boundary,
    }
    (HERE / "contract.json").write_text(canonical(contract), encoding="utf-8")

    checks = {
        "provenanceChainPassed": True,
        "historicalManifestBindingPassed": True,
        "originalPackageInventoryPreserved": True,
        "metadataOnlyMigrationPassed": True,
        "certificateBlobPassed": True,
        "certificateSourceBindingPassed": True,
        "certificateJournalFigureBindingPassed": True,
        "certificateFormalFigureAbsentRecorded": True,
        "inputHashesPassed": True,
        "primaryAndIndependentChecksPassed": True,
        "claimBoundaryFailClosed": True,
        "singlePagePdf": True,
        "physicalDimensionsPassed": True,
        "pdfTextPassed": True,
        "png600DpiPassed": True,
        "svgVectorTextPassed": True,
        "r073bFiveSixteenthsSentinelPassed": True,
        "driftRatioSentinelPassed": True,
        "exactCounterexamplesPassed": True,
        "qaArtifactsByteIdenticalToFigureCommit": True,
        "visualQaPassedAtFigureCommitAndCertificateRun": True,
        "formalContractPassed": True,
    }
    validation = {
        "schemaVersion": "r073f-figure-validation-v1",
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "provenance": {
            "sourceCommit": SOURCE_COMMIT,
            "figurePackageCommit": FIGURE_PACKAGE_COMMIT,
            "certificateCommit": CERTIFICATE_COMMIT,
            "previousManifestSha256": PREVIOUS_MANIFEST_SHA256,
            "certificateFigureLedger": "journalFigure",
            "certificateFormalFigureFieldPresent": False,
            "metadataOnlySeal": True,
        },
        "pdfPoints": points,
        "pngPixels": pixels,
        "claimBoundary": boundary,
    }
    (HERE / "validation.json").write_text(canonical(validation), encoding="utf-8")

    file_names = [
        "README.md",
        "caption.md",
        "command.txt",
        "config.json",
        "contract.json",
        "plot.py",
        "qa-protocol.md",
        "requirements.txt",
        "validate.py",
        "results.json",
        "validation.json",
        "qa-report.md",
        "figure.pdf",
        "figure.svg",
        "figure.png",
        "qa-final-size.png",
        "qa-grayscale.png",
        "qa-pdf.png",
    ]
    require(sorted(file_names) == sorted(
        name for name in current_package_names()
        if name not in ("manifest.json", "SHA256SUMS")
    ), "manifest file inventory is incomplete")
    file_records = [record(HERE / name) for name in file_names]

    previous_computation = previous_manifest["computation"]
    computation = {
        key: value
        for key, value in previous_computation.items()
        if key != "command"
    }
    computation.update({
        "formalCommand": (
            "python3 validate.py --source-commit <S> "
            "--figure-package-commit <F> --certificate-commit <C>"
        ),
        "originalGenerationCommand": previous_computation["command"],
        "metadataOnlySeal": True,
        "scientificComputationRerun": False,
    })

    manifest = {
        "schemaVersion": previous_manifest["schemaVersion"],
        "release": "R0.73F",
        "figureId": previous_manifest["figureId"],
        "status": "formal",
        "analyticalQuestion": previous_manifest["analyticalQuestion"],
        "supportedClaim": previous_manifest["supportedClaim"],
        "createdAt": previous_manifest["createdAt"],
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": SOURCE_COMMIT,
            "figurePackageCommit": FIGURE_PACKAGE_COMMIT,
            "certificateCommit": CERTIFICATE_COMMIT,
            "dirtyAtCertifiedRun": False,
            "dirtyAtFigureGeneration": True,
            "figureSourcesBoundBySha256": True,
            "certificateBindsFigureOutputsBySha256": True,
            "certificateFigureLedger": "journalFigure",
            "certificateFormalFigureFieldPresent": False,
            "certificateAttestsFormalStatus": False,
            "formalSealKind": "metadata-only",
            "originalFigureGenerationBaseCommit": SOURCE_COMMIT,
            "sourceCommitMeaning": (
                "clean analytic sources frozen at S and named by the C certificate"
            ),
            "figurePackageCommitMeaning": (
                "original validated figure package F; all scientific, figure, and "
                "QA blobs remain byte-identical"
            ),
            "certificateCommitMeaning": (
                "certificate package C binds the journalFigure outputs by SHA-256 "
                "and records passed validation and visual QA; it does not contain "
                "a formalFigure field or attest this later metadata-only status change"
            ),
            "dirtyAtCertifiedRunMeaning": (
                "certified provenance is read only from immutable S, F, and C Git blobs"
            ),
        },
        "manifestMigration": {
            "kind": "metadata-schema-only",
            "sealKind": "metadata-only",
            "previousManifestCommit": FIGURE_PACKAGE_COMMIT,
            "previousManifestSha256": PREVIOUS_MANIFEST_SHA256,
            "previousStatus": "validated",
            "currentStatus": "formal",
            "addedMetadataFiles": ["contract.json"],
            "changedMetadataFiles": sorted(CHANGED_METADATA),
            "scientificInputsChanged": False,
            "plotOrResultsChanged": False,
            "formalOutputsChanged": False,
            "qaArtifactsChanged": False,
            "certificatePayloadChanged": False,
        },
        "certificateBinding": {
            "path": CERTIFICATE_RELATIVE,
            "commit": CERTIFICATE_COMMIT,
            "figureLedgerField": "journalFigure",
            "figureStatusAtCertificateRun": "validated",
            "validationStatusAtCertificateRun": "passed",
            "visualQaStatusAtCertificateRun": "passed",
            "outputsBoundBySha256": True,
            "formalFigureFieldPresent": False,
            "formalStatusAttestedByCertificate": False,
        },
        "sourceBindings": analytic_bindings,
        "computation": computation,
        "compute": previous_manifest["compute"],
        "environment": previous_manifest["environment"],
        "data": previous_manifest["data"],
        "sourceData": previous_manifest["sourceData"],
        "inputs": previous_manifest["sourceData"],
        "figure": {**previous_manifest["figure"], "outputs": output_records},
        "outputs": output_records,
        "caption": previous_manifest["caption"],
        "qa": previous_manifest["qa"],
        "claimBoundary": boundary,
        "contract": record(HERE / "contract.json"),
        "validation": record(HERE / "validation.json"),
        "inventoryPolicy": {
            "scope": "all regular files directly inside the figure package",
            "manifestFilesExcludes": ["manifest.json", "SHA256SUMS"],
            "sha256LedgerExcludes": ["SHA256SUMS"],
            "cacheDirectoriesForbidden": True,
            "originalInventoryExtendedOnlyBy": ["contract.json"],
        },
        "files": file_records,
    }

    for key in (
        "schemaVersion",
        "figureId",
        "analyticalQuestion",
        "supportedClaim",
        "createdAt",
        "sourceBindings",
        "compute",
        "environment",
        "data",
        "sourceData",
        "figure",
        "caption",
        "qa",
        "claimBoundary",
    ):
        require(manifest[key] == previous_manifest[key],
                "metadata seal changed frozen manifest field: " + key)
    require(manifest["outputs"] == previous_manifest["figure"]["outputs"],
            "top-level output ledger differs from F")
    require(contract["claimBoundary"] == manifest["claimBoundary"],
            "contract and manifest claim boundaries differ")
    require(validation["status"] == "passed", "formal validation failed")

    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")
    ledger_names = sorted(
        name for name in current_package_names() if name != "SHA256SUMS"
    )
    (HERE / "SHA256SUMS").write_text(
        "".join(f"{sha256(HERE / name)}  {name}\n" for name in ledger_names),
        encoding="utf-8",
    )

    verify_complete_ledger()
    verify_immutable_figure_package(original_names)
    stored_manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    require(stored_manifest["status"] == "formal",
            "stored manifest did not retain formal status")
    require(stored_manifest["git"]["dirtyAtCertifiedRun"] is False,
            "stored manifest lost clean certified provenance")

    print(canonical({
        "event": "r073f-figure-formal-metadata-seal",
        "status": "formal",
        "package": str(HERE.relative_to(ROOT)),
        "sourceCommit": SOURCE_COMMIT,
        "figurePackageCommit": FIGURE_PACKAGE_COMMIT,
        "certificateCommit": CERTIFICATE_COMMIT,
        "immutableOriginalFilesVerified": len(original_names) - len(CHANGED_METADATA),
        "errors": [],
        "warnings": [],
    }), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
