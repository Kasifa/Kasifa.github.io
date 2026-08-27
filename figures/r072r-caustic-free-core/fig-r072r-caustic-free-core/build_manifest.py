#!/usr/bin/env python3
"""Build the R0.72R archive manifest and SHA-256 ledger."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
from typing import Any

from PIL import Image

from certificate_ledger import verify_flat_certificate_ledger


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
FIGURE_COMMAND = (
    "python3 figures/r072r-caustic-free-core/"
    "fig-r072r-caustic-free-core/plot.py with the six frozen lineage arguments"
)
PACKAGE_SOURCES = (
    "README.md",
    "caption.md",
    "figure-contract.md",
    "contract.json",
    "config.json",
    "command.txt",
    "requirements.txt",
    "certificate_ledger.py",
    "plot.py",
    "qa_images.py",
    "publish_assets.py",
    "validate.py",
    "build_manifest.py",
)
PACKAGE_ASSETS = [
    *PACKAGE_SOURCES,
    "environment.txt",
    "progress.ndjson",
    "resource-log.ndjson",
    "data.csv",
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
BUILDER_OUTPUTS = {"manifest.json", "SHA256SUMS"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def git_output(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=REPOSITORY, text=True, stderr=subprocess.DEVNULL
    ).strip()


def require_tracked_tree_clean() -> None:
    for args in (("diff", "--quiet", "--"), ("diff", "--cached", "--quiet", "--")):
        completed = subprocess.run(
            ["git", *args], cwd=REPOSITORY, check=False
        )
        if completed.returncode == 1:
            raise RuntimeError("formal manifest rejects tracked or staged repository drift")
        if completed.returncode != 0:
            raise RuntimeError(f"unable to verify tracked-tree cleanliness: git {' '.join(args)}")


def commit_blob_binding(commit: str, relative: str) -> dict[str, Any]:
    path = (REPOSITORY / relative).resolve()
    repository = REPOSITORY.resolve()
    if path == repository or repository not in path.parents or not path.is_file():
        raise RuntimeError(f"Git-bound file is absent or escapes repository: {relative}")
    object_type = git_output("cat-file", "-t", f"{commit}:{relative}")
    if object_type != "blob":
        raise RuntimeError(f"Git-bound path is not a blob at {commit}: {relative}")
    commit_blob = git_output("rev-parse", f"{commit}:{relative}")
    working_blob = git_output("hash-object", f"--path={relative}", str(path))
    if commit_blob != working_blob:
        raise RuntimeError(f"working file does not match {commit}:{relative}")
    return {
        "path": relative,
        "commit": commit,
        "gitBlob": commit_blob,
        "sha256": digest(path),
        "bytes": path.stat().st_size,
        "workingTreeBlobMatches": True,
    }


def require_formal_runtime_gate(
    results: dict[str, Any],
) -> tuple[str, dict[str, Path], dict[str, Any], dict[str, Any]]:
    lineage = results.get("runtimeLineage")
    if not isinstance(lineage, dict):
        raise RuntimeError("results.runtimeLineage must be an object")
    required = {
        "analyticSource",
        "producerConfig",
        "producerResult",
        "independentConfig",
        "independentResult",
        "crosscheck",
        "certificateLedger",
    }
    if set(lineage) != required:
        raise RuntimeError(
            "results.runtimeLineage must contain six explicit inputs plus the derived certificate ledger"
        )
    paths: dict[str, Path] = {}
    payloads: dict[str, Any] = {}
    expected_status = {
        "analyticSource": "source",
        "producerConfig": "formal-ready-config",
        "producerResult": "passed",
        "independentConfig": "formal-ready-config",
        "independentResult": "passed",
        "crosscheck": "passed-formal-source-only",
        "certificateLedger": "passed-flat-ledger",
    }
    for name, record in lineage.items():
        if not isinstance(record, dict) or record.get("status") != expected_status[name]:
            raise RuntimeError(f"unexpected runtime lineage status for {name}")
        path = Path(str(record.get("path", ""))).expanduser().resolve()
        if not path.is_file() or digest(path) != record.get("sha256"):
            raise RuntimeError(f"runtime lineage changed: {name}: {path}")
        paths[name] = path
        if name not in {"analyticSource", "certificateLedger"}:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                raise RuntimeError(f"runtime JSON must be an object: {name}")
            payloads[name] = payload

    runtime_json_names = {
        paths[name].name
        for name in (
            "producerConfig",
            "producerResult",
            "independentConfig",
            "independentResult",
            "crosscheck",
        )
    }
    ledger_audit = verify_flat_certificate_ledger(
        paths["certificateLedger"].parent,
        required_files=runtime_json_names,
    )
    recorded_ledger_audit = results.get("certificateLedgerAudit", {})
    if (
        Path(ledger_audit["ledgerPath"]) != paths["certificateLedger"]
        or ledger_audit.get("ledgerSha256")
        != results["runtimeLineage"]["certificateLedger"].get("sha256")
        or ledger_audit.get("ledgerSha256")
        != recorded_ledger_audit.get("ledgerSha256")
        or ledger_audit.get("entryCount") != recorded_ledger_audit.get("entryCount")
        or ledger_audit.get("requiredRuntimeJson")
        != recorded_ledger_audit.get("requiredRuntimeJson")
    ):
        raise RuntimeError("recorded flat certificate ledger audit is stale or inconsistent")

    producer_config = payloads["producerConfig"]
    independent_config = payloads["independentConfig"]
    producer_result = payloads["producerResult"]
    independent_result = payloads["independentResult"]
    crosscheck = payloads["crosscheck"]
    checks = crosscheck.get("checks")
    source_commit = crosscheck.get("sourceCommit")
    if (
        crosscheck.get("status") != "passed"
        or not isinstance(checks, dict)
        or checks.get("formalSourceReady") is not True
        or checks.get("sourceCommitMatches") is not True
        or checks.get("sourceReadyOrExplicitlyAllowed") is not True
        or checks.get("producerPassed") is not True
        or checks.get("independentPassed") is not True
        or crosscheck.get("temporaryUnsealedSourceAllowed") is not False
        or not isinstance(source_commit, str)
        or FULL_SHA.fullmatch(source_commit) is None
        or producer_config.get("gitCommit") != source_commit
        or independent_config.get("gitCommit") != source_commit
        or producer_config.get("sourceTracked") is not True
        or independent_config.get("sourceTracked") is not True
        or producer_config.get("trackedChangesDirty") is not False
        or independent_config.get("trackedChangesDirty") is not False
        or producer_result.get("status") != "passed"
        or independent_result.get("status") != "passed"
        or results.get("formalSourceCommit") != source_commit
    ):
        raise RuntimeError("temporary, dirty, untracked, or source-mismatched R0.72R certificates are forbidden")
    return source_commit, paths, payloads, ledger_audit


def package_version(distribution: str) -> str:
    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return "not installed"


def physical_memory_gib() -> float:
    try:
        raw = subprocess.check_output(
            ["sysctl", "-n", "hw.memsize"], text=True, stderr=subprocess.DEVNULL
        ).strip()
        memory_bytes = int(raw)
        if memory_bytes > 0:
            return round(memory_bytes / (1024**3), 3)
    except (OSError, subprocess.CalledProcessError, ValueError):
        pass
    try:
        page_size = int(os.sysconf("SC_PAGE_SIZE"))
        page_count = int(os.sysconf("SC_PHYS_PAGES"))
        if page_size > 0 and page_count > 0:
            return round(page_size * page_count / (1024**3), 3)
    except (OSError, TypeError, ValueError):
        pass
    raise RuntimeError("unable to determine physical memory for manifest")


def cpu_description() -> str:
    try:
        value = subprocess.check_output(
            ["sysctl", "-n", "machdep.cpu.brand_string"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        value = ""
    return value or platform.processor() or platform.machine()


def asset(name: str, *, declared_dpi: int | None = None) -> dict[str, Any]:
    path = ROOT / name
    record: dict[str, Any] = {
        "path": name,
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }
    if path.suffix.lower() == ".png":
        with Image.open(path) as image:
            record["pixels"] = [image.width, image.height]
            record["dpiMetadata"] = [
                float(value) for value in image.info.get("dpi", (0.0, 0.0))
            ]
        if declared_dpi is not None:
            record["dpi"] = declared_dpi
    return record


def assert_package_file_set(*, outputs_required: bool) -> None:
    expected = set(PACKAGE_ASSETS)
    allowed = expected | BUILDER_OUTPUTS
    entries = list(ROOT.iterdir())
    invalid = sorted(
        path.name for path in entries if path.is_symlink() or not path.is_file()
    )
    if invalid:
        raise RuntimeError(f"figure package contains symlinks or non-files: {invalid}")
    names = {path.name for path in entries}
    missing = sorted(expected - names)
    unexpected = sorted(names - allowed)
    missing_outputs = sorted(BUILDER_OUTPUTS - names) if outputs_required else []
    if missing or unexpected or missing_outputs:
        raise RuntimeError(
            "figure package file-set mismatch: "
            f"missing={missing}, unexpected={unexpected}, "
            f"missingBuilderOutputs={missing_outputs}"
        )


def rerun_custom_validation() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "validate.py")],
        cwd=REPOSITORY,
        env=os.environ.copy(),
        check=True,
    )


def main(status: str) -> None:
    assert_package_file_set(outputs_required=False)
    if status == "formal":
        require_tracked_tree_clean()
    visual = os.environ.get("R072R_VISUAL_QA_INSPECTED", "").strip().lower() == "true"
    if not visual:
        raise RuntimeError("R072R_VISUAL_QA_INSPECTED=true is required")
    rerun_custom_validation()
    assert_package_file_set(outputs_required=False)

    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))

    (
        runtime_source_commit,
        runtime_paths,
        _runtime_payloads,
        runtime_ledger_audit,
    ) = require_formal_runtime_gate(results)
    expected_lineage_statuses = {
        "producer": "passed",
        "independent": "passed",
        "crosscheck": "passed",
        "formalSourceReady": True,
        "temporaryUnsealedSourceAllowed": False,
    }
    if (
        results.get("status") != "passed"
        or results.get("noPdeEvolution") is not True
        or results.get("noFiniteFit") is not True
        or results.get("numericSamplingDoesNotReplaceContinuousProof") is not True
        or results.get("verifiedTrackedTreeClean") is not True
        or results.get("verifiedPackageSourcesAtBuildCommit") is not True
        or results.get("lineageStatuses") != expected_lineage_statuses
    ):
        raise RuntimeError(
            "results must record a passed no-PDE, no-fit formula extraction with three passed audit inputs"
        )
    if (
        validation.get("status") != "passed"
        or validation.get("allPassed") is not True
        or validation.get("automaticOnly") is not False
        or validation.get("automaticChecksPassed") is not True
    ):
        raise RuntimeError("fresh custom validation must pass before manifest construction")
    validated_package_hashes = {name: digest(ROOT / name) for name in PACKAGE_ASSETS}

    bindings = config["formalGitBindings"]
    source_paths = list(bindings["sourceCommitPaths"])
    certificate_roles = dict(bindings["certificateCommitRoles"])
    certificate_ledger_relative = str(bindings["certificateLedgerPath"])
    if not source_paths or source_paths[0] != "research/r072r_report-source.md":
        raise RuntimeError("formal source bindings must begin with the analytic report")
    if runtime_paths["analyticSource"] != (REPOSITORY / source_paths[0]).resolve():
        raise RuntimeError("runtime analytic source is not the canonical source-commit report")
    for role, relative in certificate_roles.items():
        if role not in runtime_paths or runtime_paths[role] != (REPOSITORY / relative).resolve():
            raise RuntimeError(f"runtime {role} is not the canonical certificate artifact")
    if runtime_paths["certificateLedger"] != (
        REPOSITORY / certificate_ledger_relative
    ).resolve():
        raise RuntimeError("runtime certificateLedger is not the canonical SHA256SUMS")
    if runtime_ledger_audit.get("directory") != str(
        (REPOSITORY / Path(certificate_ledger_relative).parent).resolve()
    ):
        raise RuntimeError("flat certificate ledger audit used a non-canonical directory")

    head = git_output("rev-parse", "HEAD")
    source_blob_bindings: list[dict[str, Any]] = []
    certificate_blob_bindings: list[dict[str, Any]] = []
    figure_source_blob_bindings: list[dict[str, Any]] = []
    if status == "formal":
        source_commit = os.environ.get("R072R_SOURCE_COMMIT", "").strip().lower()
        certificate_commit = os.environ.get("R072R_CERTIFICATE_COMMIT", "").strip().lower()
        dirty = os.environ.get("R072R_DIRTY_AT_CERTIFIED_RUN", "").strip().lower()
        if not FULL_SHA.fullmatch(source_commit) or not FULL_SHA.fullmatch(certificate_commit):
            raise ValueError("formal manifest requires full source and certificate commits")
        for commit in (source_commit, certificate_commit):
            git_output("cat-file", "-e", f"{commit}^{{commit}}")
        if source_commit != runtime_source_commit:
            raise RuntimeError("R072R_SOURCE_COMMIT does not match the formal runtime source commit")
        if results.get("repositoryCommitAtBuild") != certificate_commit:
            raise RuntimeError(
                "results.repositoryCommitAtBuild must equal R072R_CERTIFICATE_COMMIT"
            )
        git_output("merge-base", "--is-ancestor", source_commit, certificate_commit)
        if dirty != "false":
            raise RuntimeError("formal manifest requires dirtyAtCertifiedRun=false")
        source_blob_bindings = [
            commit_blob_binding(source_commit, relative) for relative in source_paths
        ]
        certificate_blob_bindings = [
            {
                "role": role,
                **commit_blob_binding(certificate_commit, relative),
            }
            for role, relative in sorted(certificate_roles.items())
        ]
        certificate_blob_bindings.append(
            {
                "role": "flatCertificateLedger",
                **commit_blob_binding(
                    certificate_commit, certificate_ledger_relative
                ),
            }
        )
        figure_source_blob_bindings = [
            commit_blob_binding(
                certificate_commit,
                str((ROOT / name).resolve().relative_to(REPOSITORY.resolve())),
            )
            for name in PACKAGE_SOURCES
        ]
        expected_figure_blobs = results.get("packageSourceGitBlobs", {})
        actual_figure_blobs = {
            record["path"]: record["gitBlob"]
            for record in figure_source_blob_bindings
        }
        if expected_figure_blobs != actual_figure_blobs:
            raise RuntimeError(
                "results.packageSourceGitBlobs do not match certificate-commit figure sources"
            )
        git_record = {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": source_commit,
            "certificateCommit": certificate_commit,
            "dirtyAtCertifiedRun": False,
            "manifestBuildHead": head,
            "sourceBlobBindings": source_blob_bindings,
            "certificateBlobBindings": certificate_blob_bindings,
            "figureSourceBlobBindings": figure_source_blob_bindings,
            "resultsRepositoryCommitMatchesCertificateCommit": True,
            "verifiedTrackedTreeClean": True,
        }
    else:
        git_record = {
            "repository": "Kasifa/Kasifa.github.io",
            "commit": head,
            "dirty": bool(git_output("status", "--porcelain=v1", "--untracked-files=normal")),
        }

    publication = config["publication"]
    public_assets: list[dict[str, Any]] = []
    for suffix in ("pdf", "svg", "png"):
        public = REPOSITORY / publication["directory"] / f"{publication['stem']}.{suffix}"
        master = ROOT / f"figure.{suffix}"
        if not public.is_file() or digest(public) != digest(master):
            raise RuntimeError(f"public {suffix} is absent or not byte-identical")
        public_assets.append(
            {
                "path": str(public.relative_to(REPOSITORY)),
                "bytes": public.stat().st_size,
                "sha256": digest(public),
                "byteIdenticalToMaster": True,
            }
        )

    runtime_sources: list[dict[str, Any]] = []
    formal_binding_by_path = {
        record["path"]: record
        for record in source_blob_bindings + certificate_blob_bindings
    }
    for name, record in sorted(results["runtimeLineage"].items()):
        path = runtime_paths[name]
        relative = path.relative_to(REPOSITORY.resolve())
        source_record = {
            "role": name,
            "location": "repository",
            "fileName": str(relative),
            "bytes": path.stat().st_size,
            "sha256": record["sha256"],
            "status": record["status"],
            "extractionCommand": FIGURE_COMMAND,
        }
        if status == "formal":
            binding = formal_binding_by_path.get(str(relative))
            if binding is None:
                raise RuntimeError(f"runtime source lacks a formal Git blob binding: {relative}")
            source_record["provenance"] = {
                "commit": binding["commit"],
                "gitBlob": binding["gitBlob"],
                "commitRole": (
                    "sourceCommit" if name == "analyticSource" else "certificateCommit"
                ),
            }
        runtime_sources.append(source_record)

    data_schemas = {
        "config.json": "runtime-input placeholders, exact theorem parameters, definitions for three panels, dimensions, validation thresholds, publication target, and palette",
        "contract.json": "analytical question, supported claims, finite-only policy, panel claims, render policy, and strict claim boundary",
        "results.json": "row counts, lineage hashes, exact formula checks, runtime, and package-source hashes",
        "data.csv": "panel, route, series, kind, Cartesian coordinates, real-slice or heat parameter, boundary interpolation parameter, optional radius or distance, source, pointer, claim status, and note",
        "validation.json": "asset, formula, lineage, status, publication, claim-boundary, and visual-QA checks",
        "progress.ndjson": "timestamped build start, data-ready, and completion events",
        "resource-log.ndjson": "timestamped wall time, peak resident set, and plotted-row count",
    }
    data_formats = {
        "config.json": "json",
        "contract.json": "json",
        "results.json": "json",
        "data.csv": "csv",
        "validation.json": "json",
        "progress.ndjson": "ndjson",
        "resource-log.ndjson": "ndjson",
    }
    data_names = tuple(data_schemas)
    output_records = [asset(name) for name in PACKAGE_ASSETS]
    parameters = config["parameters"]
    payload = {
        "schemaVersion": "1.0",
        "figureId": "fig-r072r-caustic-free-core",
        "release": "R0.72R",
        "status": status,
        "createdAt": datetime.now().astimezone().isoformat(timespec="seconds"),
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": contract["supportedTakeaway"],
        "claimBoundary": contract["claimBoundary"],
        "git": git_record,
        "computation": {
            "kind": "exact-audit plus high-precision presentation sampling",
            "configuration": (
                "the complex polydisc K={|z2-3/20|<=1/100, |z3|<=1/1000} beyond the old Q2<=1/2 sufficient cone; exact real 1:2:3 unit-circle slice, exact heat envelopes crossing the old sufficient boundary without degeneracy, and on 0<=y<=1 the physical W=e^{-y}F shape contract (r,C0,C1)=(pi/48,144,240); the canonical R0.72R certificate directory is independently closed by its flat SHA256SUMS"
            ),
            "precision": "dense IEEE binary64 presentation grids sampled from exact analytic formulas; sampling is presentation-only and cannot replace the continuous proof, while certificate files gate lineage and are not interpolated",
            "solver": "no PDE solver, no regression, no exponent fit, and no finite threshold inference",
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": float(results["elapsedSeconds"]),
            "continuumProofLocation": results["runtimeLineage"]["analyticSource"]["path"],
            "figureRunsNewPdeEvolution": False,
            "pdeTimeStepping": False,
            "finiteFitsAreDiagnostics": False,
            "finiteFitPlotted": False,
            "complexPolydiscBeyondOldQ2ConeClosed": True,
            "fullHeatPathTwoCriticalClosed": True,
            "physicalCellShapeClosed": True,
            "oldQ2BoundaryCrossedWithoutDegeneracy": True,
            "realUnitCircleSliceClosed": True,
            "completeFourDimensionalCausticClassified": False,
            "causticCrossingEnhancedDissipationClosed": False,
            "uniformThirdCarrierAmplitudeFloorProvided": False,
            "arbitraryFastPhaseClosed": False,
            "generalThreeDimensionalNavierStokesRegularityClosed": False,
            "randomSeed": None,
            "monitoring": {
                "enabled": True,
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
                "trackedFields": ["event", "rows", "elapsedSeconds", "maxRssMb"],
            },
        },
        "compute": {
            "host": platform.node() or "local host",
            "operatingSystem": platform.platform() or sys.platform,
            "cpu": cpu_description(),
            "memoryGiB": physical_memory_gib(),
            "logicalCpuCount": os.cpu_count(),
            "processes": 1,
            "threadsPerProcess": 1,
            "gpu": "not used by figure extraction",
            "dgx": "not used by figure extraction",
        },
        "environment": {
            "python": sys.version.split()[0],
            "numpy": package_version("numpy"),
            "matplotlib": package_version("matplotlib"),
            "pillow": package_version("pillow"),
            "pypdf": package_version("pypdf"),
            "packagesLock": "requirements.txt",
        },
        "data": [
            {
                "path": name,
                "bytes": (ROOT / name).stat().st_size,
                "sha256": digest(ROOT / name),
                "format": data_formats[name],
                "schema": data_schemas[name],
            }
            for name in data_names
        ],
        "dataSummary": {
            "rowCount": int(results["rowCount"]),
            "panelRowCounts": results["panelRowCounts"],
            "runtimeLineageStatuses": results["lineageStatuses"],
            "certificateLedgerAudit": runtime_ledger_audit,
            "parameters": {
                "centerZ2": float(parameters["centerZ2"]),
                "radiusZ2": float(parameters["radiusZ2"]),
                "radiusZ3": float(parameters["radiusZ3"]),
                "q2InitialLower": float(parameters["q2InitialLower"]),
                "q2Y1Upper": float(parameters["q2Y1Upper"]),
                "oldQ2Boundary": float(parameters["oldQ2Boundary"]),
                "criticalLocalization": float(parameters["criticalLocalization"]),
                "normalizedCurvatureLower": float(parameters["normalizedCurvatureLower"]),
                "normalizedLocalSlopeLower": float(parameters["normalizedLocalSlopeLower"]),
                "normalizedLocalSlopeUpper": float(parameters["normalizedLocalSlopeUpper"]),
                "normalizedAwayGap": float(parameters["normalizedAwayGap"]),
                "shapeC0": float(parameters["shapeC0"]),
                "shapeC1": float(parameters["shapeC1"]),
                "slowEta": float(parameters["slowEta"]),
                "derivativeSum": float(parameters["derivativeSum"]),
            },
            "formulaChecks": results["formulaChecks"],
        },
        "sourceData": runtime_sources,
        "figure": {
            "widthMillimetres": float(config["figure"]["widthMillimetres"]),
            "heightMillimetres": float(config["figure"]["heightMillimetres"]),
            "profile": "journal-default",
            "layout": "1x3",
            "script": "plot.py",
            "outputs": [
                asset(name)
                if name != "figure.png"
                else asset(name, declared_dpi=int(config["figure"]["pngDpi"]))
                for name in ("figure.pdf", "figure.svg", "figure.png")
            ],
        },
        "caption": {"english": "caption.md"},
        "publication": {
            "directory": publication["directory"],
            "stem": publication["stem"],
            "publisher": "publish_assets.py",
            "publicCopiesComplete": True,
            "assets": public_assets,
        },
        "qa": {
            "status": "passed",
            "automaticCheckCount": int(validation["checkCount"]),
            "automaticChecks": "validation.json",
            "visualInspectionExplicit": visual,
            "finalSizeInspected": visual,
            "grayscaleInspected": visual,
            "labelsAndLegendsInspected": visual,
            "realSliceCausticCoreAndOldConeInspected": visual,
            "heatEnvelopesAndSufficientBoundaryInspected": visual,
            "normalizedAndPhysicalShapeEnvelopesInspected": visual,
            "analyticMarginsInspected": visual,
            "scalesAndUnitsInspected": visual,
            "dataCrossChecked": True,
            "pdfRasterInspected": visual,
            "finalSizePreview": "qa-final-size.png",
            "grayscalePreview": "qa-grayscale.png",
            "pdfRenderPreview": "qa-pdf.png",
            "manualReport": "qa-report.md",
        },
        "outputs": output_records,
    }
    changed_after_validation = [
        name
        for name, expected in validated_package_hashes.items()
        if not (ROOT / name).is_file() or digest(ROOT / name) != expected
    ]
    changed_public = [
        record["path"]
        for record in public_assets
        if not (REPOSITORY / record["path"]).is_file()
        or digest(REPOSITORY / record["path"]) != record["sha256"]
    ]
    if changed_after_validation or changed_public:
        raise RuntimeError(
            "assets changed after fresh custom validation: "
            f"package={changed_after_validation}, public={changed_public}"
        )
    if status == "formal":
        require_tracked_tree_clean()

    (ROOT / "manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    names = sorted(PACKAGE_ASSETS + ["manifest.json"])
    (ROOT / "SHA256SUMS").write_text(
        "\n".join(f"{digest(ROOT / name)}  {name}" for name in names) + "\n",
        encoding="utf-8",
    )
    assert_package_file_set(outputs_required=True)
    print(
        json.dumps(
            {
                "status": status,
                "assets": len(output_records),
                "runtimeSources": len(runtime_sources),
                "publicAssets": len(public_assets),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", choices=("candidate", "formal"), default="candidate")
    args = parser.parse_args()
    main(args.status)
