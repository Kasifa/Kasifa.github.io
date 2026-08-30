#!/usr/bin/env python3
"""Prepare the fail-closed metadata-only formal seal for the R0.73G figure."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "figures/r073g/fig-r073g-nonlinear-row-leakage"
SOURCE_COMMIT = "21c11ba3eef7f2b5dc3f107957e0744a0471745d"
FIGURE_PACKAGE_COMMIT = "0d311d22a62cfbc9253e95580de10d33898ecddc"
FIGURE_RELATIVE = "figures/r073g/fig-r073g-nonlinear-row-leakage"
CERTIFICATE_RELATIVE = "research/certificates/r073g/certificate.json"
CHANGED_METADATA = {
    "SHA256SUMS",
    "command.txt",
    "manifest.json",
    "validate.py",
    "validation.json",
}
ADDED_METADATA = {"contract.json"}
EXPECTED_IMMUTABLE_COUNT = 14


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"


def full_commit(value: str) -> str:
    if re.fullmatch(r"[0-9a-f]{40}", value) is None:
        raise argparse.ArgumentTypeError(
            "use a full lowercase 40-character Git commit"
        )
    return value


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True, type=full_commit)
    parser.add_argument("--figure-package-commit", required=True, type=full_commit)
    parser.add_argument("--certificate-commit", required=True, type=full_commit)
    parser.add_argument(
        "--deps",
        default=None,
        help="optional directory containing Pillow and pypdf",
    )
    return parser.parse_args()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def git_bytes(commit: str, relative: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{commit}:{relative}"], cwd=ROOT
    )


def require_commit(commit: str, label: str) -> None:
    result = subprocess.run(
        ["git", "cat-file", "-e", commit + "^{commit}"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, label + " is not a Git commit")


def require_strict_ancestor(older: str, newer: str, message: str) -> None:
    require(older != newer, message + " (commits are equal)")
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", older, newer],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, message)


def package_names(commit: str) -> list[str]:
    rows = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", commit, FIGURE_RELATIVE],
        cwd=ROOT,
        text=True,
    ).splitlines()
    prefix = FIGURE_RELATIVE + "/"
    require(rows and all(row.startswith(prefix) for row in rows),
            "F does not contain the expected flat figure package")
    names = sorted(row.removeprefix(prefix) for row in rows)
    require(all("/" not in name for name in names),
            "F figure package unexpectedly contains a subdirectory")
    return names


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def output_record(commit: str, name: str) -> dict[str, object]:
    relative = f"{FIGURE_RELATIVE}/{name}"
    payload = git_bytes(commit, relative)
    return {
        "path": relative,
        "bytes": len(payload),
        "sha256": sha256_bytes(payload),
    }


def certificate_output_matches(
    journal: dict[str, object], suffix: str, expected: dict[str, object]
) -> bool:
    row = journal.get(suffix)
    if not isinstance(row, dict):
        return False
    keys = {"path", "bytes", "sha256"} | ({"dpi"} if suffix == "png" else set())
    if set(row) != keys:
        return False
    if any(row.get(key) != expected[key] for key in ("path", "bytes", "sha256")):
        return False
    return suffix != "png" or row.get("dpi") == 600


def preflight(args: argparse.Namespace) -> tuple[str, dict[str, object]]:
    require(args.source_commit == SOURCE_COMMIT,
            "source commit differs from the frozen R0.73G analytic source")
    require(args.figure_package_commit == FIGURE_PACKAGE_COMMIT,
            "figure-package commit differs from the frozen R0.73G F commit")
    for value, label in (
        (args.source_commit, "source commit"),
        (args.figure_package_commit, "figure-package commit"),
        (args.certificate_commit, "certificate commit"),
    ):
        require_commit(value, label)
    require_strict_ancestor(
        args.source_commit,
        args.figure_package_commit,
        "S is not a strict ancestor of F",
    )
    require_strict_ancestor(
        args.figure_package_commit,
        args.certificate_commit,
        "F is not a strict ancestor of C",
    )

    previous_manifest_bytes = git_bytes(
        args.figure_package_commit, f"{FIGURE_RELATIVE}/manifest.json"
    )
    previous_manifest = json.loads(previous_manifest_bytes)
    require(previous_manifest.get("figureId") == "fig-r073g-nonlinear-row-leakage",
            "F manifest figure identity mismatch")
    require(previous_manifest.get("status") == "validated",
            "F manifest is not validated")
    require(previous_manifest.get("git", {}).get("sourceCommit") == SOURCE_COMMIT,
            "F manifest source binding mismatch")

    original_names = package_names(args.figure_package_commit)
    immutable = sorted(set(original_names) - CHANGED_METADATA)
    require(len(original_names) == 19, "F inventory must contain exactly 19 files")
    require(len(immutable) == EXPECTED_IMMUTABLE_COUNT,
            "F inventory does not leave exactly 14 immutable files")
    unexpected = [
        path.name for path in HERE.iterdir()
        if not path.is_file() or path.is_symlink()
    ]
    require(not unexpected,
            "working package contains a directory or symlink: "
            + ", ".join(sorted(unexpected)))
    current_names = sorted(path.name for path in HERE.iterdir())
    allowed = [sorted(original_names), sorted(set(original_names) | ADDED_METADATA)]
    require(current_names in allowed,
            "working package inventory differs from F or F plus contract.json")
    for name in immutable:
        require(not (HERE / name).is_symlink(), "immutable file is a symlink: " + name)
        require(
            (HERE / name).read_bytes()
            == git_bytes(args.figure_package_commit, f"{FIGURE_RELATIVE}/{name}"),
            "immutable working file differs from F: " + name,
        )

    certificate_blob = git_bytes(args.certificate_commit, CERTIFICATE_RELATIVE)
    certificate_path = ROOT / CERTIFICATE_RELATIVE
    require(certificate_path.is_file(), "R0.73G certificate is missing")
    require(certificate_path.read_bytes() == certificate_blob,
            "working certificate differs from C")
    certificate = json.loads(certificate_blob)
    require(certificate.get("sourceCommit") == SOURCE_COMMIT,
            "certificate source commit mismatch")
    require(certificate.get("figurePackageCommit") == args.figure_package_commit,
            "certificate figure-package commit mismatch")
    require(certificate.get("status") == "validated",
            "certificate is not validated")
    checks = certificate.get("checks")
    require(isinstance(checks, dict) and checks
            and all(value is True for value in checks.values()),
            "certificate contains a failed or empty check ledger")
    require("formalFigure" not in certificate,
            "historical C unexpectedly contains formalFigure")
    journal = certificate.get("journalFigure")
    require(isinstance(journal, dict), "certificate journalFigure is missing")
    require(set(journal) == {
        "figureId", "status", "pdf", "svg", "png",
        "validationStatus", "visualQaStatus", "gitSealed",
    }, "certificate journalFigure field inventory mismatch")
    require(journal.get("figureId") == previous_manifest["figureId"],
            "certificate journalFigure identity mismatch")
    require(journal.get("status") == "validated",
            "certificate journalFigure status mismatch")
    require(journal.get("validationStatus") == "passed",
            "certificate journalFigure validation did not pass")
    require(journal.get("visualQaStatus") == "passed",
            "certificate journalFigure visual QA did not pass")
    require(journal.get("gitSealed") is False,
            "certificate journalFigure historical gitSealed state changed")
    for suffix in ("pdf", "svg", "png"):
        expected = output_record(args.figure_package_commit, f"figure.{suffix}")
        if suffix == "png":
            expected["dpi"] = 600
        require(certificate_output_matches(journal, suffix, expected),
                "certificate journalFigure does not exactly bind figure." + suffix)

    figure_bindings = certificate.get("figureBindings")
    require(isinstance(figure_bindings, list),
            "certificate figureBindings is missing")
    binding_paths = [row.get("path") for row in figure_bindings
                     if isinstance(row, dict)]
    require(binding_paths == [f"{FIGURE_RELATIVE}/{name}" for name in original_names],
            "certificate figureBindings inventory differs from F")
    for row in figure_bindings:
        relative = str(row["path"])
        payload = git_bytes(args.figure_package_commit, relative)
        require(row.get("commit") == args.figure_package_commit,
                "certificate figure binding commit mismatch: " + relative)
        require(row.get("bytes") == len(payload),
                "certificate figure binding size mismatch: " + relative)
        require(row.get("sha256") == sha256_bytes(payload),
                "certificate figure binding hash mismatch: " + relative)

    return sha256_bytes(previous_manifest_bytes), previous_manifest


def atomic_write(path: Path, payload: str) -> None:
    temporary = path.with_name(path.name + ".tmp-r073g-seal")
    try:
        temporary.write_text(payload, encoding="utf-8")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


VALIDATOR_TEMPLATE = r'''#!/usr/bin/env python3
"""Fail-closed metadata-only formal seal for the R0.73G figure package."""

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

SOURCE_COMMIT = "@@SOURCE_COMMIT@@"
FIGURE_PACKAGE_COMMIT = "@@FIGURE_PACKAGE_COMMIT@@"
CERTIFICATE_COMMIT = "@@CERTIFICATE_COMMIT@@"
PREVIOUS_MANIFEST_SHA256 = "@@PREVIOUS_MANIFEST_SHA256@@"
FIGURE_RELATIVE = "figures/r073g/fig-r073g-nonlinear-row-leakage"
CERTIFICATE_RELATIVE = "research/certificates/r073g/certificate.json"
ANALYTIC_PATHS = (
    "research/r073g_problem_freeze.md",
    "research/r073g_nonlinear_shadowing_proof.md",
    "research/r073g_operator_derivation.md",
    "research/r073g_adversarial_audit.md",
    "research/r073g_independent_analytic_audit.md",
    "research/r073g_literature_audit.md",
    "research/r073g_gap_matrix.md",
    "research/r073g_report-source.md",
)
CHANGED_METADATA = {
    "SHA256SUMS",
    "command.txt",
    "manifest.json",
    "validate.py",
    "validation.json",
}
ADDED_METADATA = {"contract.json"}
EXPECTED_IMMUTABLE_COUNT = 14


def configure_dependencies(path: str | None) -> None:
    if path:
        sys.path.insert(0, path)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"


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


def atomic_write(path: Path, payload: str) -> None:
    temporary = path.with_name(path.name + ".tmp-r073g-formal-seal")
    try:
        temporary.write_text(payload, encoding="utf-8")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


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
        check=False,
    )
    require(result.returncode == 0, label + " is not a Git commit")


def require_strict_ancestor(older: str, newer: str, message: str) -> None:
    require(older != newer, message + " (commits are equal)")
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", older, newer],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
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
    names = sorted(row.removeprefix(prefix) for row in rows)
    require(all("/" not in name for name in names),
            "original figure package unexpectedly contains subdirectories")
    return names


def current_package_names() -> list[str]:
    unexpected = [
        path.name for path in HERE.iterdir()
        if not path.is_file() or path.is_symlink()
    ]
    require(not unexpected,
            "figure package contains a directory or symlink: " + ", ".join(unexpected))
    return sorted(path.name for path in HERE.iterdir())


def verify_immutable_figure_package(original_names: list[str]) -> None:
    expected = sorted(set(original_names) | ADDED_METADATA)
    require(current_package_names() == expected,
            "figure inventory differs from F plus the allowed contract metadata")
    immutable = sorted(set(original_names) - CHANGED_METADATA)
    require(len(immutable) == EXPECTED_IMMUTABLE_COUNT,
            "metadata migration does not preserve exactly 14 immutable files")
    for name in immutable:
        current = (HERE / name).read_bytes()
        frozen = git_bytes(FIGURE_PACKAGE_COMMIT, f"{FIGURE_RELATIVE}/{name}")
        require(current == frozen,
                "immutable figure-package file differs from F: " + name)


def verify_complete_ledger() -> None:
    rows: list[tuple[str, str]] = []
    for line in (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\\r\n]+)", line)
        require(match is not None, "malformed SHA256SUMS row")
        rows.append((match.group(2), match.group(1)))
    names = [name for name, _ in rows]
    require(names == sorted(names), "SHA256SUMS is not sorted")
    require(len(names) == len(set(names)), "SHA256SUMS has duplicate entries")
    expected = sorted(name for name in current_package_names()
                      if name != "SHA256SUMS")
    require(names == expected, "SHA256SUMS inventory is incomplete")
    for name, expected_hash in rows:
        require(sha256(HERE / name) == expected_hash,
                "SHA256SUMS hash mismatch: " + name)


def certificate_output(
    journal: dict[str, Any], suffix: str, expected: dict[str, Any]
) -> None:
    row = journal.get(suffix)
    require(isinstance(row, dict),
            "certificate journalFigure output is missing: " + suffix)
    keys = {"path", "bytes", "sha256"} | ({"dpi"} if suffix == "png" else set())
    require(set(row) == keys,
            "certificate journalFigure output schema mismatch: " + suffix)
    for key in ("path", "bytes", "sha256"):
        require(row.get(key) == expected[key],
                "certificate journalFigure output mismatch: " + suffix + "/" + key)
    if suffix == "png":
        require(row.get("dpi") == 600,
                "certificate journalFigure PNG dpi mismatch")


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
            "source commit differs from the R0.73G analytic source")
    require(args.figure_package_commit == FIGURE_PACKAGE_COMMIT,
            "figure-package commit differs from F")
    require(args.certificate_commit == CERTIFICATE_COMMIT,
            "certificate commit differs from C")
    require_strict_ancestor(SOURCE_COMMIT, FIGURE_PACKAGE_COMMIT,
                            "S is not a strict ancestor of F")
    require_strict_ancestor(FIGURE_PACKAGE_COMMIT, CERTIFICATE_COMMIT,
                            "F is not a strict ancestor of C")

    previous_manifest_bytes = git_bytes(
        FIGURE_PACKAGE_COMMIT, f"{FIGURE_RELATIVE}/manifest.json"
    )
    require(sha256_bytes(previous_manifest_bytes) == PREVIOUS_MANIFEST_SHA256,
            "historical F manifest hash mismatch")
    previous_manifest = json.loads(previous_manifest_bytes)
    require(previous_manifest.get("figureId") == "fig-r073g-nonlinear-row-leakage",
            "historical F figure identity mismatch")
    require(previous_manifest.get("status") == "validated",
            "historical F manifest was not validated")
    require(previous_manifest.get("git", {}).get("sourceCommit") == SOURCE_COMMIT,
            "historical F manifest source commit mismatch")

    original_names = package_names_at_figure_commit()
    require(len(original_names) == 19,
            "historical F package must contain exactly 19 files")
    verify_immutable_figure_package(original_names)

    previous_validation = json.loads(git_bytes(
        FIGURE_PACKAGE_COMMIT, f"{FIGURE_RELATIVE}/validation.json"
    ))
    require(previous_validation.get("status") == "passed",
            "historical F validation was not passed")
    previous_checks = previous_validation.get("checks")
    require(isinstance(previous_checks, dict) and previous_checks
            and all(value is True for value in previous_checks.values()),
            "historical F validation contains a failed or empty check ledger")

    certificate_path = ROOT / CERTIFICATE_RELATIVE
    require(certificate_path.is_file(), "R0.73G certificate is missing")
    committed_certificate = git_bytes(CERTIFICATE_COMMIT, CERTIFICATE_RELATIVE)
    require(certificate_path.read_bytes() == committed_certificate,
            "current certificate differs from C")
    certificate = json.loads(committed_certificate)
    require(certificate.get("sourceCommit") == SOURCE_COMMIT,
            "certificate source commit mismatch")
    require(certificate.get("figurePackageCommit") == FIGURE_PACKAGE_COMMIT,
            "certificate figure-package commit mismatch")
    require(certificate.get("status") == "validated",
            "certificate is not validated")
    certificate_checks = certificate.get("checks")
    require(isinstance(certificate_checks, dict) and certificate_checks
            and all(value is True for value in certificate_checks.values()),
            "certificate contains a failed or empty check ledger")
    require("formalFigure" not in certificate,
            "historical C unexpectedly contains a formalFigure field")
    journal_figure = certificate.get("journalFigure")
    require(isinstance(journal_figure, dict),
            "certificate journalFigure is missing")
    require(set(journal_figure) == {
        "figureId", "status", "pdf", "svg", "png",
        "validationStatus", "visualQaStatus", "gitSealed",
    }, "certificate journalFigure field inventory mismatch")
    require(journal_figure.get("figureId") == previous_manifest["figureId"],
            "certificate journalFigure identity mismatch")
    require(journal_figure.get("status") == "validated",
            "certificate journalFigure historical status mismatch")
    require(journal_figure.get("validationStatus") == "passed",
            "certificate journalFigure validation did not pass")
    require(journal_figure.get("visualQaStatus") == "passed",
            "certificate journalFigure visual QA did not pass")
    require(journal_figure.get("gitSealed") is False,
            "certificate journalFigure historical gitSealed state changed")

    figure_bindings = certificate.get("figureBindings")
    require(isinstance(figure_bindings, list),
            "certificate figureBindings is missing")
    expected_binding_paths = [
        f"{FIGURE_RELATIVE}/{name}" for name in original_names
    ]
    require([row.get("path") for row in figure_bindings]
            == expected_binding_paths,
            "certificate figureBindings inventory differs from F")
    for row in figure_bindings:
        relative = row["path"]
        payload = git_bytes(FIGURE_PACKAGE_COMMIT, relative)
        require(row.get("commit") == FIGURE_PACKAGE_COMMIT,
                "certificate figure binding commit mismatch: " + relative)
        require(row.get("bytes") == len(payload),
                "certificate figure binding size mismatch: " + relative)
        require(row.get("sha256") == sha256_bytes(payload),
                "certificate figure binding hash mismatch: " + relative)
        if "gitBlob" in row:
            require(row["gitBlob"] == git_blob(FIGURE_PACKAGE_COMMIT, relative),
                    "certificate figure binding blob mismatch: " + relative)

    certificate_source_rows = {
        row["path"]: row for row in certificate.get("sourceBindings", [])
    }
    analytic_bindings = [historical_binding(path) for path in ANALYTIC_PATHS]
    require(analytic_bindings == previous_manifest.get("sourceBindings"),
            "historical F source bindings changed")
    for binding in analytic_bindings:
        row = certificate_source_rows.get(binding["path"], {})
        bound_commit = row.get("commit", row.get("sourceCommit"))
        require(bound_commit == SOURCE_COMMIT,
                "certificate source binding commit mismatch: " + binding["path"])
        require(row.get("bytes") == binding["bytes"],
                "certificate source binding size mismatch: " + binding["path"])
        require(row.get("sha256") == binding["sha256"],
                "certificate source binding hash mismatch: " + binding["path"])
        if "gitBlob" in row:
            require(row["gitBlob"] == git_blob(SOURCE_COMMIT, binding["path"]),
                    "certificate source binding blob mismatch: " + binding["path"])

    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    results = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    for item in results["inputs"]:
        path = ROOT / item["path"]
        require(path.is_file(), "missing source-data input: " + item["path"])
        require(path.stat().st_size == item["bytes"],
                "source-data size changed: " + item["path"])
        require(sha256(path) == item["sha256"],
                "source-data hash changed: " + item["path"])
        require(path.read_bytes() == git_bytes(FIGURE_PACKAGE_COMMIT, item["path"]),
                "source-data input differs from F: " + item["path"])
    require(previous_manifest.get("sourceData") == results["inputs"],
            "historical sourceData binding changed")
    require(results["configBinding"]["sha256"] == sha256(HERE / "config.json"),
            "figure config changed after rendering")

    boundary = results["claimBoundary"]
    require(boundary == previous_manifest.get("claimBoundary"),
            "historical claim boundary changed")
    require(boundary.get("formalFiniteDiagnosticFigure") is True,
            "formal finite diagnostic declaration missing")
    for key, value in boundary.items():
        if key != "formalFiniteDiagnosticFigure":
            require(value is False, "escaped claim boundary: " + key)
    facts = results["diagnosticFacts"]
    require(facts == previous_manifest.get("diagnosticFacts"),
            "historical diagnostic facts changed")
    require(facts and all(facts.values()), "a declared diagnostic fact is false")

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
        "Frozen top eigenvalue",
        "Physical Sobolev cost",
        "Generated rows",
        "Numerical cross-checks",
        "diagnostic only",
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
    for token in ("Frozen top eigenvalue", "Generated rows", "diagnostic only"):
        require(token in svg, "SVG text missing: " + token)

    observed = results["observed"]
    require(abs(observed["maximumFinestCutoffRelativeChange"]
                - 5.749359085030244e-14) < 1e-26,
            "cutoff-comparison sentinel changed")
    require(results["crossValidation"]["allChecksPass"] is True,
            "figure cross-validation status failed")
    require(results["crossValidation"]["primaryMaximumScaleOneDifference"] < 1e-12,
            "primary kernel discrepancy exceeded tolerance")
    require(results["crossValidation"]["independentMaximumScaleOneError"] < 1e-12,
            "independent kernel discrepancy exceeded tolerance")

    output_records: list[dict[str, Any]] = []
    for suffix in ("pdf", "svg", "png"):
        name = f"figure.{suffix}"
        item = record(HERE / name, HERE)
        if suffix == "png":
            item.update({"dpi": 600, "pixels": pixels})
        output_records.append(item)
        expected_certificate = {
            "path": f"{FIGURE_RELATIVE}/{name}",
            "bytes": item["bytes"],
            "sha256": item["sha256"],
        }
        if suffix == "png":
            expected_certificate["dpi"] = 600
        certificate_output(journal_figure, suffix, expected_certificate)
    require(output_records == previous_manifest["figure"]["outputs"],
            "formal output records differ from F")

    contract = {
        "schemaVersion": "r073g-figure-contract-v1",
        "release": "R0.73G",
        "figureId": previous_manifest["figureId"],
        "requiredOutputs": ["figure.pdf", "figure.svg", "figure.png"],
        "requiredDiagnostics": ["results.json", "validation.json"],
        "claimBoundary": boundary,
    }
    atomic_write(HERE / "contract.json", canonical(contract))

    checks = {
        "provenanceChainPassed": True,
        "historicalManifestBindingPassed": True,
        "originalPackageInventoryPreserved": True,
        "fourteenImmutableFilesByteIdenticalToF": True,
        "metadataOnlyMigrationPassed": True,
        "certificateBlobPassed": True,
        "certificateSourceBindingPassed": True,
        "certificateFullFigurePackageBindingPassed": True,
        "certificateJournalFigureBindingPassed": True,
        "certificateFormalFigureAbsentRecorded": True,
        "inputHashesPassed": True,
        "claimBoundaryFailClosed": True,
        "diagnosticFactsPassed": True,
        "singlePagePdf": True,
        "physicalDimensionsPassed": True,
        "pdfTextPassed": True,
        "png600DpiPassed": True,
        "svgVectorTextPassed": True,
        "finiteSentinelsPassed": True,
        "qaArtifactsByteIdenticalToFigureCommit": True,
        "visualQaPassedAtFigureCommitAndCertificateRun": True,
        "formalContractPassed": True,
    }
    validation = {
        "schemaVersion": "r073g-figure-validation-v1",
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
            "immutableOriginalFilesVerified": EXPECTED_IMMUTABLE_COUNT,
        },
        "pdfPoints": points,
        "pngPixels": pixels,
        "claimBoundary": boundary,
    }
    atomic_write(HERE / "validation.json", canonical(validation))

    command = (
        "From the repository root, run the metadata-only formal seal. This command does\n"
        "not invoke plot.py or rewrite scientific, figure, or QA artifacts.\n\n"
        "R073G_DEPS_DIR=/tmp/r073c-deps\n"
        "PYTHON=/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/"
        "dependencies/python/bin/python3\n\n"
        "env PYTHONPATH=\"$R073G_DEPS_DIR\" \"$PYTHON\" "
        f"{FIGURE_RELATIVE}/validate.py --deps \"$R073G_DEPS_DIR\" "
        f"--source-commit {SOURCE_COMMIT} "
        f"--figure-package-commit {FIGURE_PACKAGE_COMMIT} "
        f"--certificate-commit {CERTIFICATE_COMMIT}\n"
    )
    atomic_write(HERE / "command.txt", command)

    file_names = sorted(
        name for name in current_package_names()
        if name not in ("manifest.json", "SHA256SUMS")
    )
    require(len(file_names) == 18,
            "formal manifest must cover exactly 18 non-ledger files")
    file_records = [record(HERE / name) for name in file_names]

    previous_computation = previous_manifest["computation"]
    computation = {
        key: value for key, value in previous_computation.items() if key != "command"
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

    previous_git = previous_manifest["git"]
    manifest = {
        "schemaVersion": previous_manifest["schemaVersion"],
        "release": "R0.73G",
        "figureId": previous_manifest["figureId"],
        "status": "formal",
        "analyticalQuestion": previous_manifest["analyticalQuestion"],
        "supportedClaim": previous_manifest["supportedClaim"],
        "createdAt": previous_manifest["createdAt"],
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": SOURCE_COMMIT,
            "experimentCommit": previous_git["experimentCommit"],
            "rendererSourceCommit": previous_git["rendererSourceCommit"],
            "figurePackageCommit": FIGURE_PACKAGE_COMMIT,
            "certificateCommit": CERTIFICATE_COMMIT,
            "dirtyAtCertifiedRun": False,
            "dirtyAtFigureGeneration": True,
            "figureSourcesBoundBySha256": True,
            "certificateBindsFigurePackage": True,
            "certificateBindsFigureOutputsBySha256": True,
            "certificateFigureLedger": "journalFigure",
            "certificateJournalFigureGitSealed": journal_figure["gitSealed"],
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
                "certificate package C binds the full F package and the journalFigure "
                "outputs by SHA-256; it does not contain a formalFigure field or "
                "attest this later metadata-only formal status"
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
            "immutableOriginalFilesVerified": EXPECTED_IMMUTABLE_COUNT,
            "scientificInputsChanged": False,
            "plotOrResultsChanged": False,
            "formalOutputsChanged": False,
            "qaArtifactsChanged": False,
            "certificatePayloadChanged": False,
        },
        "certificateBinding": {
            "path": CERTIFICATE_RELATIVE,
            "commit": CERTIFICATE_COMMIT,
            "figurePackageCommit": FIGURE_PACKAGE_COMMIT,
            "figureLedgerField": "journalFigure",
            "figureStatusAtCertificateRun": "validated",
            "validationStatusAtCertificateRun": "passed",
            "visualQaStatusAtCertificateRun": "passed",
            "outputsBoundBySha256": True,
            "fullFigurePackageBound": True,
            "formalFigureFieldPresent": False,
            "formalStatusAttestedByCertificate": False,
        },
        "sourceBindings": analytic_bindings,
        "experimentManifestBinding": previous_manifest["experimentManifestBinding"],
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
        "diagnosticFacts": facts,
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
        "experimentManifestBinding",
        "compute",
        "environment",
        "data",
        "sourceData",
        "figure",
        "caption",
        "qa",
        "diagnosticFacts",
        "claimBoundary",
    ):
        require(manifest[key] == previous_manifest[key],
                "metadata seal changed frozen manifest field: " + key)
    require(manifest["outputs"] == previous_manifest["figure"]["outputs"],
            "top-level output ledger differs from F")
    require(contract["claimBoundary"] == manifest["claimBoundary"],
            "contract and manifest claim boundaries differ")
    require(validation["status"] == "passed", "formal validation failed")

    atomic_write(HERE / "manifest.json", canonical(manifest))
    ledger_names = sorted(name for name in current_package_names()
                          if name != "SHA256SUMS")
    atomic_write(
        HERE / "SHA256SUMS",
        "".join(f"{sha256(HERE / name)}  {name}\n" for name in ledger_names),
    )

    verify_complete_ledger()
    verify_immutable_figure_package(original_names)
    stored_manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    require(stored_manifest["status"] == "formal",
            "stored manifest did not retain formal status")
    require(stored_manifest["git"]["sourceCommit"] == SOURCE_COMMIT,
            "stored manifest lost S binding")
    require(stored_manifest["git"]["figurePackageCommit"] == FIGURE_PACKAGE_COMMIT,
            "stored manifest lost F binding")
    require(stored_manifest["git"]["certificateCommit"] == CERTIFICATE_COMMIT,
            "stored manifest lost C binding")
    require(stored_manifest["contract"]["sha256"] == sha256(HERE / "contract.json"),
            "stored manifest contract binding changed")

    print(canonical({
        "event": "r073g-figure-formal-metadata-seal",
        "status": "formal",
        "package": str(HERE.relative_to(ROOT)),
        "sourceCommit": SOURCE_COMMIT,
        "figurePackageCommit": FIGURE_PACKAGE_COMMIT,
        "certificateCommit": CERTIFICATE_COMMIT,
        "immutableOriginalFilesVerified": EXPECTED_IMMUTABLE_COUNT,
        "errors": [],
        "warnings": [],
    }), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def validator_source(
    source_commit: str,
    figure_package_commit: str,
    certificate_commit: str,
    previous_manifest_sha256: str,
) -> str:
    substitutions = {
        "@@SOURCE_COMMIT@@": source_commit,
        "@@FIGURE_PACKAGE_COMMIT@@": figure_package_commit,
        "@@CERTIFICATE_COMMIT@@": certificate_commit,
        "@@PREVIOUS_MANIFEST_SHA256@@": previous_manifest_sha256,
    }
    result = VALIDATOR_TEMPLATE
    for marker, value in substitutions.items():
        require(result.count(marker) == 1, "validator template marker count changed")
        result = result.replace(marker, value)
    require("@@" not in result, "validator template contains an unresolved marker")
    compile(result, str(HERE / "validate.py"), "exec")
    return result


def main() -> int:
    args = arguments()
    previous_manifest_sha256, previous_manifest = preflight(args)
    contract = {
        "schemaVersion": "r073g-figure-contract-v1",
        "release": "R0.73G",
        "figureId": previous_manifest["figureId"],
        "requiredOutputs": ["figure.pdf", "figure.svg", "figure.png"],
        "requiredDiagnostics": ["results.json", "validation.json"],
        "claimBoundary": previous_manifest["claimBoundary"],
    }
    atomic_write(HERE / "contract.json", canonical(contract))
    atomic_write(
        HERE / "validate.py",
        validator_source(
            args.source_commit,
            args.figure_package_commit,
            args.certificate_commit,
            previous_manifest_sha256,
        ),
    )

    command = [
        sys.executable,
        "-B",
        str(HERE / "validate.py"),
        "--source-commit",
        args.source_commit,
        "--figure-package-commit",
        args.figure_package_commit,
        "--certificate-commit",
        args.certificate_commit,
    ]
    if args.deps:
        command.extend(["--deps", args.deps])
    subprocess.run(command, cwd=ROOT, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
