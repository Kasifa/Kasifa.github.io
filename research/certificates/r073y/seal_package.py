#!/usr/bin/env python3
"""Seal or read-only verify the R0.73Y formal certificate archive.

The archive is deliberately flat.  ``--seal`` is the only mode that writes,
and it writes only ``manifest.json`` and ``SHA256SUMS`` after every content,
source-binding, producer, claim-boundary, and negative-test gate passes.
``--check-only`` snapshots all package files and rejects any size, mtime, or
ctime change.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
from typing import Any, Callable, Dict, Iterable, List, Sequence, Tuple


HERE = Path(__file__).resolve().parent
MANIFEST_NAME = "manifest.json"
CHECKSUM_NAME = "SHA256SUMS"

CONTENT_FILES: Tuple[str, ...] = (
    "README.md",
    "audit-checklist.json",
    "claim-boundary.md",
    "command.txt",
    "contract.json",
    "exact-shear-producer.py",
    "exact-shear-results.json",
    "exact-shear-report.md",
    "independent-reaudit.md",
    "requirements.txt",
    "seal_package.py",
)
PACKAGE_FILES: Tuple[str, ...] = CONTENT_FILES + (
    MANIFEST_NAME,
    CHECKSUM_NAME,
)

SOURCE_COMMIT = "1ecc6fe20a921db9d0876dbd4484a3aa4ca7ec66"
SOURCE_TREE = "22301433ec51719e13363a595586913894b0be17"
SOURCE_PARENT = "cb0ab52b27891478e159d69cae1ce4ed8b96b522"
SOURCE_SCRIPT_SHA256 = (
    "f682784c64142f958a18936fc488dac6b83e28ce85610b27f07a669c8c61d417"
)
ARCHIVE_PRODUCER_SHA256 = (
    "d69a6a8b3afed7d25e0f1fc30d820b8cb380bb879ef628add3e8b25ec6ed7437"
)
RESULT_SHA256 = (
    "fe6bb0e8bb4674f63a579f6b2db92c12f75235c4d293594e115c7b49599ef4df"
)
REPORT_SHA256 = (
    "668177c61721600880cd85651f8481249c8f9a972d631dd4f5a3383bbb07c6aa"
)
REAUDIT_SHA256 = (
    "622c35cedf82a87dccdac1e2b9fb8247b79a1a99020a91d95447884deaf5b231"
)
PAYLOAD_SHA256 = (
    "51f721cf560df38fbeacdd093d4293adae10635e13dcaa6b9251616c4f7eca2c"
)

SOURCE_INPUTS: Tuple[Dict[str, str], ...] = (
    {
        "archive_binding": "contract-only",
        "path": "research/r073y_evidence_gap_matrix.md",
        "sha256": "76e5d8b6bf3f9efc4217b06cea1af2c6408eb9ad7b6dc953676828e33a7195fb",
    },
    {
        "archive_binding": "byte-identical:exact-shear-results.json",
        "path": "research/r073y_exact_shear_certificate.json",
        "sha256": RESULT_SHA256,
    },
    {
        "archive_binding": "byte-identical:exact-shear-report.md",
        "path": "research/r073y_exact_shear_certificate_report.md",
        "sha256": REPORT_SHA256,
    },
    {
        "archive_binding": "byte-identical:independent-reaudit.md",
        "path": "research/r073y_exact_shear_independent_reaudit.md",
        "sha256": REAUDIT_SHA256,
    },
    {
        "archive_binding": "contract-only",
        "path": "research/r073y_exact_shear_no_go.md",
        "sha256": "2574f2caf19248a17d25f811488db1c7b30295efd07e59852c3afa17cf8f69e4",
    },
    {
        "archive_binding": "contract-only",
        "path": "research/r073y_primary_literature_audit.md",
        "sha256": "13fcf43cfae17cbf4a5f0e171d3d602eccc9b4e0f24f093cfc3ab84187cf6871",
    },
    {
        "archive_binding": "contract-only",
        "path": "research/r073y_report-source.md",
        "sha256": "d2f4df01b51ec613affc4b14a3544f6f702584de1ba1a94b2ec241e31d5efd01",
    },
    {
        "archive_binding": "reversible-relocation:exact-shear-producer.py",
        "path": "scripts/r073y_exact_shear_certificate.py",
        "sha256": SOURCE_SCRIPT_SHA256,
    },
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(
        value,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def strict_json_bytes(data: bytes, label: str) -> Dict[str, Any]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise RuntimeError(label + ": invalid UTF-8") from error

    def reject_duplicates(pairs: List[Tuple[str, Any]]) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, label + ": duplicate JSON key: " + key)
            result[key] = value
        return result

    def reject_constant(token: str) -> None:
        raise RuntimeError(label + ": nonfinite JSON constant: " + token)

    try:
        value = json.loads(
            text,
            object_pairs_hook=reject_duplicates,
            parse_constant=reject_constant,
        )
    except json.JSONDecodeError as error:
        raise RuntimeError(label + ": invalid JSON") from error
    require(isinstance(value, dict), label + ": JSON root must be an object")
    require(text == canonical(value), label + ": JSON is not strict canonical form")
    return value


def strict_json_path(name: str) -> Dict[str, Any]:
    return strict_json_bytes((HERE / name).read_bytes(), name)


def payload_core(payload: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(payload)
    result.pop("payload_sha256", None)
    return result


def verify_payload_hash(payload: Dict[str, Any], label: str) -> None:
    stored = payload.get("payload_sha256")
    require(type(stored) is str, label + ": payload hash type drifted")
    recomputed = sha256_bytes(canonical(payload_core(payload)).encode("utf-8"))
    require(stored == recomputed, label + ": payload hash mismatch")


def verify_result_object(payload: Dict[str, Any], label: str) -> None:
    verify_payload_hash(payload, label)
    require(payload.get("schema") == "r073y-exact-shear-certificate-v1",
            label + ": schema drifted")
    require(type(payload.get("status")) is str and payload["status"] == "PASS",
            label + ": result status drifted")
    require(type(payload.get("not_clay")) is bool and payload["not_clay"] is True,
            label + ": not_clay scalar type or value drifted")
    require(payload.get("payload_sha256") == PAYLOAD_SHA256,
            label + ": frozen payload hash drifted")
    numeric = payload.get("numerical_cross_checks")
    require(type(numeric) is dict, label + ": numerical block type drifted")
    maximum = numeric.get("maximum_overall_scaled_error")
    require(type(maximum) is float and math.isfinite(maximum),
            label + ": numeric maximum type drifted")
    require(0.0 <= maximum < 2.0e-10,
            label + ": numerical threshold failed")
    ledger = payload.get("claim_ledger")
    require(type(ledger) is dict, label + ": claim ledger type drifted")
    require(ledger.get("productionOnlyCoerciveBridge")
            == "FALSE_BY_EXACT_NSE_FAMILY",
            label + ": production-only boundary drifted")
    require(ledger.get("epsilonRegularityRefuted") == "FALSE_NOT_CLAIMED",
            label + ": epsilon-regularity boundary drifted")
    require(ledger.get("arbitraryThreeDimensionalGlobalRegularity") == "OPEN",
            label + ": global-regularity boundary drifted")
    require(ledger.get("clayConclusion") == "OPEN",
            label + ": Clay boundary drifted")


def reconstruct_source_producer(archive_bytes: bytes) -> bytes:
    text = archive_bytes.decode("utf-8")
    archive_block = (
        'ROOT = Path(__file__).resolve().parent\n'
        'RESULT_PATH = ROOT / "exact-shear-results.json"\n'
        'REPORT_PATH = ROOT / "exact-shear-report.md"\n'
    )
    source_block = (
        'ROOT = Path(__file__).resolve().parents[1]\n'
        'RESULT_PATH = ROOT / "research" / "r073y_exact_shear_certificate.json"\n'
        'REPORT_PATH = ROOT / "research" / "r073y_exact_shear_certificate_report.md"\n'
    )
    require(text.count(archive_block) == 1,
            "archive producer: relocation block inventory drifted")
    return text.replace(archive_block, source_block, 1).encode("utf-8")


def verify_archive_producer_bytes(data: bytes) -> None:
    require(sha256_bytes(data) == ARCHIVE_PRODUCER_SHA256,
            "archive producer: archive hash mismatch")
    reconstructed = reconstruct_source_producer(data)
    require(sha256_bytes(reconstructed) == SOURCE_SCRIPT_SHA256,
            "archive producer: frozen source hash mismatch")


def verify_report_bytes(data: bytes) -> None:
    require(sha256_bytes(data) == REPORT_SHA256,
            "exact-shear-report.md: frozen report hash mismatch")
    text = data.decode("utf-8")
    require("payload_sha256=" + PAYLOAD_SHA256 in text,
            "exact-shear-report.md: payload binding missing")
    require(text.endswith("**NOT CLAY.**\n"),
            "exact-shear-report.md: NOT CLAY boundary missing")


def verify_contract_object(contract: Dict[str, Any]) -> None:
    require(contract.get("schema") == "r073y-formal-certificate-contract-v1",
            "contract.json: schema drifted")
    require(contract.get("release") == "R0.73Y",
            "contract.json: release drifted")
    require(contract.get("status") == "FROZEN",
            "contract.json: status drifted")
    source = contract.get("source")
    require(type(source) is dict, "contract.json: source type drifted")
    require(source.get("git_commit_sha1") == SOURCE_COMMIT,
            "contract.json: source commit drifted")
    require(source.get("git_tree_sha1") == SOURCE_TREE,
            "contract.json: source tree drifted")
    require(source.get("git_parent_sha1") == SOURCE_PARENT,
            "contract.json: source parent drifted")
    require(source.get("author_date") == "2026-09-01T13:22:02+08:00",
            "contract.json: source date drifted")
    require(source.get("subject") == "Freeze R0.73Y exact shear no-go research",
            "contract.json: source subject drifted")
    require(source.get("inputs") == list(SOURCE_INPUTS),
            "contract.json: frozen input inventory drifted")
    archive = contract.get("archive")
    require(type(archive) is dict, "contract.json: archive type drifted")
    flat = archive.get("flat_producer")
    require(type(flat) is dict, "contract.json: flat producer type drifted")
    require(flat.get("path") == "exact-shear-producer.py"
            and flat.get("sha256") == ARCHIVE_PRODUCER_SHA256,
            "contract.json: flat producer binding drifted")
    relocation = flat.get("relocation")
    require(type(relocation) is dict,
            "contract.json: relocation type drifted")
    require(relocation.get("changed_declarations") == 3
            and type(relocation.get("changed_declarations")) is int,
            "contract.json: relocation count drifted")
    require(relocation.get("kind") == "reversible-flat-path-relocation-v1",
            "contract.json: relocation kind drifted")
    require(relocation.get("mathematical_or_algorithmic_change") is False,
            "contract.json: relocation boundary drifted")
    policy = archive.get("inventory_policy")
    require(type(policy) is dict, "contract.json: inventory policy drifted")
    require(policy == {
        "manifest_entry_count": len(CONTENT_FILES),
        "manifest_excludes": [CHECKSUM_NAME, MANIFEST_NAME],
        "package_file_count": len(PACKAGE_FILES),
        "sha256sums_entry_count": len(CONTENT_FILES) + 1,
        "sha256sums_excludes_itself": True,
    }, "contract.json: inventory policy drifted")
    certificate = contract.get("certificate")
    require(type(certificate) is dict,
            "contract.json: certificate type drifted")
    require(certificate.get("payload_sha256") == PAYLOAD_SHA256,
            "contract.json: certificate payload drifted")
    require(certificate.get("status") == "PASS",
            "contract.json: certificate status drifted")
    require(certificate.get("schema") == "r073y-exact-shear-certificate-v1",
            "contract.json: certificate schema drifted")
    require(type(certificate.get("maximum_numeric_scaled_error")) is float,
            "contract.json: maximum numeric type drifted")
    require(certificate.get("maximum_numeric_scaled_error")
            == 1.2856382625159313e-13,
            "contract.json: maximum numeric value drifted")
    require(type(certificate.get("numeric_error_threshold_exclusive")) is float
            and certificate.get("numeric_error_threshold_exclusive") == 2.0e-10,
            "contract.json: numeric threshold drifted")
    boundary = contract.get("claim_boundary")
    require(type(boundary) is dict, "contract.json: claim boundary drifted")
    require(boundary == {
        "arbitrary_three_dimensional_global_regularity": "OPEN",
        "clay_problem_solved": False,
        "epsilon_regularity_refuted": False,
        "general_orthogonal_shear_class_executable_coverage": False,
        "not_clay": True,
        "production_only_coercive_bridge": "FALSE_BY_EXACT_NSE_FAMILY",
        "publication_artifacts_covered": False,
    }, "contract.json: claim boundary drifted")


def verify_audit_object(audit: Dict[str, Any]) -> None:
    require(audit.get("schema") == "r073y-formal-certificate-audit-v1",
            "audit-checklist.json: schema drifted")
    require(audit.get("release") == "R0.73Y"
            and audit.get("status") == "PASS",
            "audit-checklist.json: status drifted")
    require(type(audit.get("not_clay")) is bool and audit["not_clay"] is True,
            "audit-checklist.json: NOT CLAY type or value drifted")
    rows = audit.get("checks")
    require(type(rows) is list and len(rows) == 9,
            "audit-checklist.json: check inventory drifted")
    expected_ids = {
        "source_commit_and_hash_binding",
        "producer_relocation_binding",
        "strict_json",
        "producer_result_report_binding",
        "dual_runtime",
        "archive_negative_tests",
        "read_only_check_mode",
        "self_exclusion",
        "claim_boundary",
    }
    require({row.get("id") for row in rows if type(row) is dict} == expected_ids,
            "audit-checklist.json: check IDs drifted")
    require(all(type(row) is dict and row.get("status") == "PASS" for row in rows),
            "audit-checklist.json: a check did not pass")
    runtimes = audit.get("dual_runtime_evidence")
    require(type(runtimes) is list and runtimes == [
        {
            "implementation": "CPython",
            "label": "system-python3",
            "producer_check_only": "PASS",
            "version": "3.9.6",
        },
        {
            "implementation": "CPython",
            "label": "bundled-python3",
            "producer_check_only": "PASS",
            "version": "3.12.13",
        },
    ], "audit-checklist.json: dual-runtime evidence drifted")
    negative = audit.get("negative_tests")
    require(type(negative) is dict and negative == {
        "duplicate_key": "PASS_REJECTED",
        "inventory": "PASS_REJECTED",
        "report": "PASS_REJECTED",
        "result": "PASS_REJECTED",
        "source": "PASS_REJECTED",
        "source_commit": "PASS_REJECTED",
        "stored_hash": "PASS_REJECTED",
        "type": "PASS_REJECTED",
    }, "audit-checklist.json: negative-test evidence drifted")


def forbidden_path_scan(name: str, data: bytes) -> None:
    text = data.decode("utf-8")
    forbidden = (
        "/" + "Users" + "/",
        "/private/" + "tmp" + "/",
        "file:" + "//",
    )
    for needle in forbidden:
        require(needle not in text, name + ": host or temporary absolute path found")


def verify_inventory_names(names: Iterable[str]) -> None:
    actual = set(names)
    expected = set(PACKAGE_FILES)
    require(actual == expected,
            "package inventory mismatch: expected %d files, found %d"
            % (len(expected), len(actual)))


def root_file_names() -> List[str]:
    names: List[str] = []
    for path in HERE.iterdir():
        require(path.is_file() and not path.is_symlink(),
                "package contains a directory, special file, or symlink: " + path.name)
        names.append(path.name)
    return names


def verify_content_files() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    for name in CONTENT_FILES:
        path = HERE / name
        require(path.is_file() and not path.is_symlink(),
                "missing or unsafe content file: " + name)
        forbidden_path_scan(name, path.read_bytes())

    contract = strict_json_path("contract.json")
    audit = strict_json_path("audit-checklist.json")
    result_bytes = (HERE / "exact-shear-results.json").read_bytes()
    result = strict_json_bytes(result_bytes, "exact-shear-results.json")
    verify_contract_object(contract)
    verify_audit_object(audit)
    verify_result_object(result, "exact-shear-results.json")
    require(sha256_bytes(result_bytes) == RESULT_SHA256,
            "exact-shear-results.json: frozen file hash mismatch")
    verify_archive_producer_bytes((HERE / "exact-shear-producer.py").read_bytes())
    verify_report_bytes((HERE / "exact-shear-report.md").read_bytes())
    reaudit = (HERE / "independent-reaudit.md").read_bytes()
    require(sha256_bytes(reaudit) == REAUDIT_SHA256,
            "independent-reaudit.md: frozen file hash mismatch")
    require(reaudit.decode("utf-8").endswith("**NOT CLAY.**\n"),
            "independent-reaudit.md: NOT CLAY boundary missing")
    claim = (HERE / "claim-boundary.md").read_text(encoding="utf-8")
    require(claim.endswith("**NOT CLAY.**\n"),
            "claim-boundary.md: NOT CLAY boundary missing")
    require((HERE / "requirements.txt").read_text(encoding="utf-8")
            == "Python >= 3.9\nstdlib only; no third-party packages\n",
            "requirements.txt: dependency contract drifted")
    return contract, audit


def record(name: str) -> Dict[str, Any]:
    path = HERE / name
    require(path.is_file() and not path.is_symlink(),
            "cannot inventory missing or unsafe file: " + name)
    return {
        "bytes": path.stat().st_size,
        "path": name,
        "sha256": sha256_path(path),
    }


def expected_manifest(
    contract: Dict[str, Any],
    audit: Dict[str, Any],
) -> Dict[str, Any]:
    records = [record(name) for name in CONTENT_FILES]
    return {
        "claim_boundary": contract["claim_boundary"],
        "files": records,
        "inventory": {
            "manifest_entry_count": len(records),
            "package_file_count": len(PACKAGE_FILES),
            "sha256sums_entry_count": len(records) + 1,
        },
        "release": "R0.73Y",
        "schema": "r073y-formal-certificate-manifest-v1",
        "seal": {
            "archive_negative_tests": 8,
            "dual_runtime_evidence": audit["dual_runtime_evidence"],
            "producer_built_in_negative_tests": 7,
            "status": "PASS",
        },
        "self_exclusion": {
            "manifest_excluded_from_manifest_files": True,
            "sha256sums_excluded_from_manifest_files": True,
            "sha256sums_excluded_from_itself": True,
        },
        "source": {
            "git_commit_sha1": SOURCE_COMMIT,
            "git_tree_sha1": SOURCE_TREE,
            "payload_sha256": PAYLOAD_SHA256,
        },
        "status": "SEALED",
    }


def expected_checksums(manifest_bytes: bytes) -> bytes:
    lines = []
    for name in CONTENT_FILES:
        lines.append(sha256_path(HERE / name) + "  " + name + "\n")
    lines.append(sha256_bytes(manifest_bytes) + "  " + MANIFEST_NAME + "\n")
    return "".join(lines).encode("utf-8")


def verify_manifest_and_checksums(
    contract: Dict[str, Any],
    audit: Dict[str, Any],
) -> None:
    manifest_bytes = (HERE / MANIFEST_NAME).read_bytes()
    manifest = strict_json_bytes(manifest_bytes, MANIFEST_NAME)
    expected = expected_manifest(contract, audit)
    require(manifest == expected, "manifest.json: content or inventory drifted")
    require(len(manifest["files"]) == len(CONTENT_FILES),
            "manifest.json: derived record count drifted")
    checksum_bytes = (HERE / CHECKSUM_NAME).read_bytes()
    require(checksum_bytes == expected_checksums(manifest_bytes),
            "SHA256SUMS: checksum ledger drifted")
    lines = checksum_bytes.decode("utf-8").splitlines()
    require(len(lines) == len(CONTENT_FILES) + 1,
            "SHA256SUMS: derived line count drifted")
    require(not any(line.endswith("  " + CHECKSUM_NAME) for line in lines),
            "SHA256SUMS: self-entry is forbidden")


def expect_failure(name: str, action: Callable[[], None], needle: str) -> str:
    try:
        action()
    except RuntimeError as error:
        require(needle in str(error),
                name + ": rejected for unexpected reason: " + str(error))
        return name
    raise RuntimeError(name + ": mutation unexpectedly passed")


def archive_negative_tests(
    contract: Dict[str, Any],
    result: Dict[str, Any],
) -> List[str]:
    passed: List[str] = []

    source_mutation = (HERE / "exact-shear-producer.py").read_bytes() + b"\n"
    passed.append(expect_failure(
        "source",
        lambda: verify_archive_producer_bytes(source_mutation),
        "archive hash mismatch",
    ))

    result_mutation = copy.deepcopy(result)
    result_mutation["status"] = "FAIL"
    passed.append(expect_failure(
        "result",
        lambda: verify_result_object(result_mutation, "result mutation"),
        "payload hash mismatch",
    ))

    report_mutation = (HERE / "exact-shear-report.md").read_bytes() + b" "
    passed.append(expect_failure(
        "report",
        lambda: verify_report_bytes(report_mutation),
        "frozen report hash mismatch",
    ))

    hash_mutation = copy.deepcopy(result)
    hash_mutation["payload_sha256"] = "0" * 64
    passed.append(expect_failure(
        "stored_hash",
        lambda: verify_result_object(hash_mutation, "hash mutation"),
        "payload hash mismatch",
    ))

    type_mutation = copy.deepcopy(result)
    type_mutation["not_clay"] = 1
    type_mutation["payload_sha256"] = sha256_bytes(
        canonical(payload_core(type_mutation)).encode("utf-8")
    )
    passed.append(expect_failure(
        "type",
        lambda: verify_result_object(type_mutation, "type mutation"),
        "not_clay scalar type or value drifted",
    ))

    canonical_result = canonical(result)
    duplicate = canonical_result.replace(
        "{\n",
        '{\n  "not_clay": false,\n',
        1,
    ).encode("utf-8")
    passed.append(expect_failure(
        "duplicate_key",
        lambda: strict_json_bytes(duplicate, "duplicate mutation"),
        "duplicate JSON key",
    ))

    inventory_mutation = set(PACKAGE_FILES)
    inventory_mutation.add("unexpected-file")
    passed.append(expect_failure(
        "inventory",
        lambda: verify_inventory_names(inventory_mutation),
        "package inventory mismatch",
    ))

    contract_mutation = copy.deepcopy(contract)
    contract_mutation["source"]["git_commit_sha1"] = "0" * 40
    passed.append(expect_failure(
        "source_commit",
        lambda: verify_contract_object(contract_mutation),
        "source commit drifted",
    ))

    require(len(passed) == 8 and len(set(passed)) == 8,
            "archive negative-test inventory drifted")
    return passed


def snapshot(names: Sequence[str]) -> Dict[str, Tuple[int, int, int]]:
    result: Dict[str, Tuple[int, int, int]] = {}
    for name in names:
        stat = (HERE / name).stat()
        result[name] = (stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns)
    return result


def run_producer(command: str) -> Dict[str, str]:
    require(type(command) is str and command.strip() != "",
            "producer runtime command is empty")
    version_process = subprocess.run(
        [command, "-c", "import platform; print(platform.python_version())"],
        cwd=str(HERE),
        check=False,
        capture_output=True,
        text=True,
    )
    require(version_process.returncode == 0,
            "producer runtime version probe failed")
    version = version_process.stdout.strip()
    require(version != "", "producer runtime version probe was empty")
    process = subprocess.run(
        [command, "exact-shear-producer.py", "--check-only"],
        cwd=str(HERE),
        check=False,
        capture_output=True,
        text=True,
    )
    require(process.returncode == 0,
            "producer --check-only failed under Python " + version
            + ": " + process.stderr.strip())
    require("R0.73Y-A exact shear certificate: PASS" in process.stdout,
            "producer PASS marker missing under Python " + version)
    require("payload_sha256=" + PAYLOAD_SHA256 in process.stdout,
            "producer payload marker missing under Python " + version)
    require("portable_gate_negative_tests=7/7" in process.stdout,
            "producer negative-test marker missing under Python " + version)
    return {"implementation": "CPython", "status": "PASS", "version": version}


def verify_runtime_runs(
    runs: Sequence[Dict[str, str]],
    audit: Dict[str, Any],
    require_dual: bool,
) -> None:
    require(len(runs) >= 1, "no producer runtime was checked")
    require(all(row.get("status") == "PASS" for row in runs),
            "a producer runtime did not pass")
    if require_dual:
        versions = {row["version"] for row in runs}
        expected_versions = {
            row["version"] for row in audit["dual_runtime_evidence"]
        }
        require(len(runs) >= 2 and len(versions) >= 2,
                "seal mode requires two distinct Python runtime versions")
        require(expected_versions.issubset(versions),
                "seal runtimes do not reproduce the frozen dual-runtime evidence")


def seal(runtime_commands: Sequence[str]) -> Dict[str, Any]:
    existing = set(root_file_names())
    allowed_before = set(PACKAGE_FILES)
    require(existing.issubset(allowed_before),
            "seal mode found an unexpected package file")
    require(set(CONTENT_FILES).issubset(existing),
            "seal mode is missing a content file")
    contract, audit = verify_content_files()
    result = strict_json_path("exact-shear-results.json")
    negative = archive_negative_tests(contract, result)
    runs = [run_producer(command) for command in runtime_commands]
    verify_runtime_runs(runs, audit, require_dual=True)
    manifest = expected_manifest(contract, audit)
    manifest_bytes = canonical(manifest).encode("utf-8")
    (HERE / MANIFEST_NAME).write_bytes(manifest_bytes)
    (HERE / CHECKSUM_NAME).write_bytes(expected_checksums(manifest_bytes))
    verify_inventory_names(root_file_names())
    verify_manifest_and_checksums(contract, audit)
    return {
        "archive_negative_tests": len(negative),
        "files": len(PACKAGE_FILES),
        "manifest_sha256": sha256_bytes(manifest_bytes),
        "mode": "seal",
        "producer_runtimes": runs,
        "sha256sums_sha256": sha256_path(HERE / CHECKSUM_NAME),
        "status": "PASS",
    }


def check_only(runtime_commands: Sequence[str]) -> Dict[str, Any]:
    verify_inventory_names(root_file_names())
    before = snapshot(PACKAGE_FILES)
    contract, audit = verify_content_files()
    result = strict_json_path("exact-shear-results.json")
    negative = archive_negative_tests(contract, result)
    verify_manifest_and_checksums(contract, audit)
    runs = [run_producer(command) for command in runtime_commands]
    verify_runtime_runs(runs, audit, require_dual=len(runtime_commands) >= 2)
    after = snapshot(PACKAGE_FILES)
    require(before == after,
            "check-only changed package size, modification time, or change time")
    manifest_sha = sha256_path(HERE / MANIFEST_NAME)
    return {
        "archive_negative_tests": len(negative),
        "files": len(PACKAGE_FILES),
        "manifest_sha256": manifest_sha,
        "mode": "check-only-read-only",
        "producer_runtimes": runs,
        "sha256sums_sha256": sha256_path(HERE / CHECKSUM_NAME),
        "status": "PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check-only", action="store_true")
    mode.add_argument("--seal", action="store_true")
    parser.add_argument(
        "--python",
        action="append",
        dest="python_commands",
        help="Python interpreter command for producer --check-only; repeatable",
    )
    arguments = parser.parse_args()
    runtime_commands = arguments.python_commands or [sys.executable]
    if arguments.seal:
        report = seal(runtime_commands)
    else:
        report = check_only(runtime_commands)
    print(canonical(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
