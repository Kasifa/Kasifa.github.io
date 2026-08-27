#!/usr/bin/env python3
"""Fail-closed verifier for the flat R0.72S certificate SHA-256 ledger."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
from typing import Any, Iterable


LEDGER_NAME = "SHA256SUMS"
EXCLUDED_NAMES = {LEDGER_NAME, ".DS_Store"}
ROW = re.compile(r"^([0-9a-f]{64})  ([^/\\\r\n]+)$")


class CertificateLedgerError(RuntimeError):
    """Raised when the certificate directory is not exactly ledger-sealed."""


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def verify_flat_certificate_ledger(
    directory: Path | str,
    *,
    required_files: Iterable[str],
) -> dict[str, Any]:
    supplied = Path(directory).expanduser()
    if supplied.is_symlink():
        raise CertificateLedgerError("certificate directory must not be a symlink")
    root = supplied.resolve()
    if not root.is_dir():
        raise CertificateLedgerError(f"certificate directory does not exist: {root}")

    required = set(required_files)
    if not required or any(
        not name or Path(name).name != name or name in EXCLUDED_NAMES
        for name in required
    ):
        raise CertificateLedgerError("required certificate names must be flat, nonempty files")

    ledger = root / LEDGER_NAME
    if ledger.is_symlink() or not ledger.is_file():
        raise CertificateLedgerError("SHA256SUMS must be one regular, non-symlink file")
    try:
        raw = ledger.read_bytes()
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CertificateLedgerError("SHA256SUMS must be UTF-8") from exc
    if not text or not text.endswith("\n") or "\r" in text:
        raise CertificateLedgerError("SHA256SUMS must be nonempty LF text with a final newline")

    rows = text[:-1].split("\n")
    if not rows or any(not row for row in rows):
        raise CertificateLedgerError("SHA256SUMS must not contain blank rows")
    names: list[str] = []
    expected_hashes: dict[str, str] = {}
    for row in rows:
        match = ROW.fullmatch(row)
        if match is None:
            raise CertificateLedgerError(f"malformed SHA256SUMS row: {row!r}")
        expected, name = match.groups()
        if name in EXCLUDED_NAMES or name in {".", ".."}:
            raise CertificateLedgerError(f"forbidden ledger entry: {name!r}")
        if name in expected_hashes:
            raise CertificateLedgerError(f"duplicate ledger entry: {name}")
        names.append(name)
        expected_hashes[name] = expected
    sorted_names = sorted(names, key=lambda name: name.encode("utf-8"))
    if names != sorted_names:
        raise CertificateLedgerError("SHA256SUMS rows must be uniquely byte-sorted")

    actual_files: dict[str, Path] = {}
    for path in root.iterdir():
        if path.is_symlink():
            raise CertificateLedgerError(f"symlink in certificate directory: {path.name}")
        if path.name == LEDGER_NAME:
            if not path.is_file():
                raise CertificateLedgerError("SHA256SUMS is not a regular file")
            continue
        if path.name == ".DS_Store":
            if not path.is_file():
                raise CertificateLedgerError(".DS_Store exclusion applies only to a regular file")
            continue
        if not path.is_file():
            raise CertificateLedgerError(f"non-file in flat certificate directory: {path.name}")
        actual_files[path.name] = path

    ledger_names = set(names)
    actual_names = set(actual_files)
    if ledger_names != actual_names:
        raise CertificateLedgerError(
            "SHA256SUMS does not exactly cover the certificate directory: "
            f"missing={sorted(actual_names - ledger_names)}, "
            f"stale={sorted(ledger_names - actual_names)}"
        )
    missing_required = sorted(required - ledger_names)
    if missing_required:
        raise CertificateLedgerError(
            f"runtime certificate JSON files missing from SHA256SUMS: {missing_required}"
        )

    mismatches = [
        name for name in names if sha256(actual_files[name]) != expected_hashes[name]
    ]
    if mismatches:
        raise CertificateLedgerError(f"SHA256SUMS digest mismatch: {mismatches}")

    return {
        "status": "passed",
        "directory": str(root),
        "ledgerPath": str(ledger),
        "ledgerSha256": sha256(ledger),
        "entryCount": len(names),
        "entries": [
            {"fileName": name, "sha256": expected_hashes[name]} for name in names
        ],
        "requiredRuntimeJson": sorted(required),
        "exactDirectoryCoverage": True,
        "uniqueByteSortedRows": True,
        "symlinksRejected": True,
    }
