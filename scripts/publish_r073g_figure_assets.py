#!/usr/bin/env python3
"""Publish the sealed R0.73G figure assets with a metadata-only overlay."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIGURE_ID = "fig-r073g-nonlinear-row-leakage"
FIGURE_RELATIVE = "figures/r073g/fig-r073g-nonlinear-row-leakage"
FIGURE_DIRECTORY = ROOT / FIGURE_RELATIVE
PUBLIC_RELATIVE = "public/assets/r073g"
PUBLIC_DIRECTORY = ROOT / PUBLIC_RELATIVE
PUBLIC_PARENT = PUBLIC_DIRECTORY.parent
OVERLAY_FILES = frozenset({"manifest.json", "SHA256SUMS"})
SUFFIXES = ("pdf", "svg", "png")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def full_commit(value: str) -> str:
    if re.fullmatch(r"[0-9a-f]{40}", value) is None:
        raise argparse.ArgumentTypeError(
            "use a full lowercase 40-character Git commit"
        )
    return value


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--figure-seal-commit",
        required=True,
        type=full_commit,
        help="full 40-character commit for the metadata-only figure seal S",
    )
    return parser.parse_args()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def reject_json_constant(value: str) -> None:
    raise ValueError("non-finite JSON constant is forbidden: " + value)


def unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def load_json(payload: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            payload,
            object_pairs_hook=unique_json_object,
            parse_constant=reject_json_constant,
        )
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        raise RuntimeError(label + " is not strict JSON") from exc
    require(isinstance(value, dict), label + " must contain a JSON object")
    return value


def json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    ).encode("utf-8")


def git_bytes(commit: str, relative: str) -> bytes:
    try:
        return subprocess.check_output(
            ["git", "show", f"{commit}:{relative}"],
            cwd=ROOT,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"sealed file is absent from {commit}: {relative}"
        ) from exc


def require_commit(commit: str) -> None:
    object_type = subprocess.run(
        ["git", "cat-file", "-t", commit],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    require(
        object_type.returncode == 0 and object_type.stdout.strip() == "commit",
        "figure seal must name a Git commit object directly",
    )
    resolved = subprocess.run(
        ["git", "rev-parse", commit + "^{commit}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    require(
        resolved.returncode == 0 and resolved.stdout.strip() == commit,
        "figure seal commit must resolve exactly to the supplied object ID",
    )


def current_head() -> str:
    value = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    require(
        re.fullmatch(r"[0-9a-f]{40}", value) is not None,
        "current HEAD is not a full Git commit",
    )
    return value


def require_real_directory(path: Path, label: str) -> None:
    try:
        relative = path.relative_to(ROOT)
    except ValueError as exc:
        raise RuntimeError(label + " escapes the repository") from exc
    cursor = ROOT
    require(
        cursor.is_dir() and not cursor.is_symlink(),
        "repository root is not a real directory",
    )
    for component in relative.parts:
        cursor /= component
        require(
            not cursor.is_symlink(),
            label + " contains a symlink component: " + str(cursor),
        )
    require(path.is_dir(), label + " is missing or is not a directory")


def require_strict_ancestor(older: str, newer: str) -> None:
    require(older != newer, "current HEAD must be later than figure seal S")
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", older, newer],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    require(
        result.returncode == 0,
        "figure seal S is not an ancestor of current HEAD",
    )


def sealed_package_names(commit: str) -> list[str]:
    raw = subprocess.check_output(
        [
            "git",
            "ls-tree",
            "-r",
            "-z",
            "--full-tree",
            commit,
            "--",
            FIGURE_RELATIVE,
        ],
        cwd=ROOT,
    )
    prefix = FIGURE_RELATIVE + "/"
    names: list[str] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        try:
            metadata, encoded_path = item.split(b"\t", 1)
            mode, object_type, _object_id = metadata.decode("ascii").split(" ")
            relative = encoded_path.decode("utf-8")
        except (UnicodeDecodeError, ValueError) as exc:
            raise RuntimeError("malformed Git tree entry in figure seal S") from exc
        require(
            mode in {"100644", "100755"} and object_type == "blob",
            "figure seal S contains a non-regular package entry: " + relative,
        )
        require(
            relative.startswith(prefix),
            "figure seal S returned an out-of-scope package entry",
        )
        name = relative.removeprefix(prefix)
        require(
            name and "/" not in name,
            "figure seal S package is not flat: " + relative,
        )
        names.append(name)
    require(names, "figure seal S does not contain the R0.73G package")
    require(len(names) == len(set(names)), "figure seal S package has duplicates")
    return sorted(names)


def current_package_names() -> list[str]:
    require_real_directory(FIGURE_DIRECTORY, "working R0.73G figure package")
    names: list[str] = []
    for path in FIGURE_DIRECTORY.iterdir():
        require(
            path.is_file() and not path.is_symlink(),
            "working figure package contains a non-regular entry: " + path.name,
        )
        names.append(path.name)
    require(len(names) == len(set(names)), "working figure inventory has duplicates")
    return sorted(names)


def verify_sealed_package(commit: str) -> tuple[bytes, bytes, dict[str, Any]]:
    sealed_names = sealed_package_names(commit)
    current_names = current_package_names()
    require(
        sealed_names == current_names,
        "working figure inventory differs from figure seal S",
    )
    require(
        OVERLAY_FILES.issubset(sealed_names),
        "figure seal S is missing manifest.json or SHA256SUMS",
    )
    for name in sealed_names:
        if name in OVERLAY_FILES:
            continue
        current = (FIGURE_DIRECTORY / name).read_bytes()
        sealed = git_bytes(commit, f"{FIGURE_RELATIVE}/{name}")
        require(
            current == sealed,
            "working figure file differs byte-for-byte from S: " + name,
        )

    manifest_path = FIGURE_DIRECTORY / "manifest.json"
    ledger_path = FIGURE_DIRECTORY / "SHA256SUMS"
    manifest_bytes = manifest_path.read_bytes()
    ledger_bytes = ledger_path.read_bytes()
    require(
        manifest_bytes
        == git_bytes(commit, f"{FIGURE_RELATIVE}/manifest.json"),
        "working manifest already differs from figure seal S",
    )
    require(
        ledger_bytes
        == git_bytes(commit, f"{FIGURE_RELATIVE}/SHA256SUMS"),
        "working SHA256SUMS already differs from figure seal S",
    )
    manifest = load_json(manifest_bytes, "sealed figure manifest")
    require(
        json_bytes(manifest) == manifest_bytes,
        "sealed figure manifest is not in canonical repository formatting",
    )
    require(
        manifest.get("figureId") == FIGURE_ID,
        "sealed figure manifest has the wrong figureId",
    )
    require(
        manifest.get("status") == "formal",
        "sealed figure manifest is not formal",
    )
    require(
        "publication" not in manifest,
        "sealed figure manifest already contains a publication overlay",
    )
    verify_ledger(ledger_bytes, current_names, manifest_bytes)
    return manifest_bytes, ledger_bytes, manifest


def output_records(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = manifest.get("outputs")
    if not isinstance(rows, list):
        figure = manifest.get("figure")
        require(isinstance(figure, dict), "figure manifest has no output ledger")
        rows = figure.get("outputs")
    require(isinstance(rows, list), "figure manifest outputs must be a list")

    records: dict[str, dict[str, Any]] = {}
    for suffix in SUFFIXES:
        expected_name = f"figure.{suffix}"
        matches = [
            row
            for row in rows
            if isinstance(row, dict)
            and Path(str(row.get("path", ""))).name == expected_name
        ]
        require(
            len(matches) == 1,
            "figure manifest must bind exactly one " + expected_name,
        )
        row = matches[0]
        source = FIGURE_DIRECTORY / expected_name
        payload = source.read_bytes()
        require(
            row.get("bytes") == len(payload)
            and row.get("sha256") == sha256_bytes(payload),
            "figure manifest output binding mismatch: " + expected_name,
        )
        records[suffix] = row
    return records


def parse_ledger(payload: bytes) -> list[tuple[str, str, bytes]]:
    require(payload.endswith(b"\n"), "SHA256SUMS must end with a newline")
    parsed: list[tuple[str, str, bytes]] = []
    for raw_row in payload.splitlines(keepends=True):
        match = re.fullmatch(
            rb"([0-9a-f]{64})  ([^/\\\r\n]+)(\r?\n)", raw_row
        )
        require(match is not None, "malformed SHA256SUMS row")
        try:
            name = match.group(2).decode("utf-8")
            digest = match.group(1).decode("ascii")
        except UnicodeDecodeError as exc:
            raise RuntimeError("SHA256SUMS contains a non-UTF-8 name") from exc
        parsed.append((name, digest, raw_row))
    names = [name for name, _digest, _raw in parsed]
    require(names == sorted(names), "SHA256SUMS rows are not sorted")
    require(len(names) == len(set(names)), "SHA256SUMS has duplicate rows")
    return parsed


def verify_ledger(
    payload: bytes,
    package_names: list[str],
    planned_manifest: bytes | None = None,
) -> None:
    rows = parse_ledger(payload)
    expected = sorted(name for name in package_names if name != "SHA256SUMS")
    require(
        [name for name, _digest, _raw in rows] == expected,
        "SHA256SUMS does not exactly cover the flat figure package",
    )
    for name, expected_hash, _raw in rows:
        if name == "manifest.json" and planned_manifest is not None:
            actual_hash = sha256_bytes(planned_manifest)
        else:
            actual_hash = sha256_file(FIGURE_DIRECTORY / name)
        require(actual_hash == expected_hash, "SHA256SUMS mismatch: " + name)


def replace_manifest_hash(ledger: bytes, manifest: bytes) -> bytes:
    replacement = sha256_bytes(manifest).encode("ascii")
    output: list[bytes] = []
    matches = 0
    for name, _digest, raw_row in parse_ledger(ledger):
        if name == "manifest.json":
            output.append(replacement + raw_row[64:])
            matches += 1
        else:
            output.append(raw_row)
    require(matches == 1, "SHA256SUMS must contain one manifest.json row")
    return b"".join(output)


def strip_manifest_hash_row(ledger: bytes) -> bytes:
    output = [
        raw_row
        for name, _digest, raw_row in parse_ledger(ledger)
        if name != "manifest.json"
    ]
    require(
        len(output) + 1 == len(parse_ledger(ledger)),
        "SHA256SUMS must contain exactly one manifest.json row",
    )
    return b"".join(output)


def publication_overlay() -> tuple[dict[str, Any], dict[Path, bytes]]:
    records = output_records(
        load_json((FIGURE_DIRECTORY / "manifest.json").read_bytes(), "manifest")
    )
    assets: list[dict[str, Any]] = []
    payloads: dict[Path, bytes] = {}
    for suffix in SUFFIXES:
        source = FIGURE_DIRECTORY / f"figure.{suffix}"
        payload = source.read_bytes()
        relative = f"{PUBLIC_RELATIVE}/{FIGURE_ID}.{suffix}"
        row = {
            "path": relative,
            "bytes": len(payload),
            "sha256": sha256_bytes(payload),
        }
        require(
            records[suffix].get("bytes") == row["bytes"]
            and records[suffix].get("sha256") == row["sha256"],
            "public asset does not match the sealed output record: " + suffix,
        )
        assets.append(row)
        payloads[ROOT / relative] = payload
    overlay = {
        "byteIdentityRequired": True,
        "publicCopiesComplete": True,
        "directory": PUBLIC_RELATIVE,
        "fileStem": FIGURE_ID,
        "assets": assets,
    }
    return overlay, payloads


def verify_publication_contract(
    manifest_bytes: bytes,
    sealed_manifest_bytes: bytes,
    public_payloads: dict[Path, bytes],
) -> None:
    manifest = load_json(manifest_bytes, "publication figure manifest")
    publication = manifest.get("publication")
    require(isinstance(publication, dict), "publication overlay is missing")
    require(
        set(publication)
        == {
            "byteIdentityRequired",
            "publicCopiesComplete",
            "directory",
            "fileStem",
            "assets",
        },
        "publication overlay has an unexpected field inventory",
    )
    require(
        publication.get("byteIdentityRequired") is True
        and publication.get("publicCopiesComplete") is True
        and publication.get("directory") == PUBLIC_RELATIVE
        and publication.get("fileStem") == FIGURE_ID,
        "publication overlay contract is inconsistent",
    )
    rows = publication.get("assets")
    require(isinstance(rows, list) and len(rows) == 3,
            "publication overlay must bind exactly three assets")
    by_path = {
        str(row.get("path", "")): row
        for row in rows
        if isinstance(row, dict)
    }
    expected_paths = {path.relative_to(ROOT).as_posix() for path in public_payloads}
    require(
        set(by_path) == expected_paths and len(by_path) == len(rows),
        "publication asset path set is not exact",
    )
    for path, payload in public_payloads.items():
        relative = path.relative_to(ROOT).as_posix()
        row = by_path[relative]
        require(
            set(row) == {"path", "bytes", "sha256"}
            and row.get("bytes") == len(payload)
            and row.get("sha256") == sha256_bytes(payload),
            "publication asset binding mismatch: " + relative,
        )
    publication_free = dict(manifest)
    del publication_free["publication"]
    require(
        json_bytes(publication_free) == sealed_manifest_bytes,
        "publication overlay changed sealed manifest metadata",
    )


def require_target_parent() -> bool:
    require_real_directory(PUBLIC_PARENT, "public/assets")
    if os.path.lexists(PUBLIC_DIRECTORY):
        require_real_directory(PUBLIC_DIRECTORY, "public/assets/r073g")
        return False
    return True


def write_staged(path: Path, payload: bytes, mode: int) -> None:
    path.write_bytes(payload)
    os.chmod(path, mode)
    require(path.read_bytes() == payload, "temporary staging write failed")


def snapshot_mode(path: Path, fallback: int = 0o644) -> int:
    if os.path.lexists(path):
        require(
            path.is_file() and not path.is_symlink(),
            "transaction target is not a regular file: " + str(path),
        )
        return stat.S_IMODE(path.stat().st_mode)
    return fallback


def snapshot_is_unchanged(path: Path, backup: Path | None) -> bool:
    if backup is None:
        return not os.path.lexists(path)
    return (
        path.is_file()
        and not path.is_symlink()
        and path.read_bytes() == backup.read_bytes()
    )


def rollback(
    applied: list[Path],
    backups: dict[Path, Path | None],
    created_public_directory: bool,
    temporary_root: Path,
) -> list[str]:
    failures: list[str] = []
    for index, target in enumerate(reversed(applied)):
        try:
            backup = backups[target]
            if backup is None:
                target.unlink(missing_ok=True)
                require(
                    not os.path.lexists(target),
                    "rollback could not restore target absence",
                )
            else:
                expected = backup.read_bytes()
                restore = temporary_root / f"restore-{index:02d}"
                shutil.copy2(backup, restore, follow_symlinks=False)
                os.replace(restore, target)
                require(
                    target.is_file()
                    and not target.is_symlink()
                    and target.read_bytes() == expected,
                    "rollback read-back mismatch",
                )
        except (OSError, RuntimeError) as exc:
            failures.append(str(target) + ": " + str(exc))
    if created_public_directory:
        try:
            PUBLIC_DIRECTORY.rmdir()
        except OSError as exc:
            failures.append(str(PUBLIC_DIRECTORY) + ": " + str(exc))
    return failures


def publish(figure_seal_commit: str) -> None:
    require_commit(figure_seal_commit)
    head = current_head()
    require_strict_ancestor(figure_seal_commit, head)
    sealed_manifest_bytes, sealed_ledger_bytes, sealed_manifest = (
        verify_sealed_package(figure_seal_commit)
    )
    output_records(sealed_manifest)

    overlay, public_payloads = publication_overlay()
    updated_manifest = dict(sealed_manifest)
    updated_manifest["publication"] = overlay
    updated_manifest_bytes = json_bytes(updated_manifest)
    verify_publication_contract(
        updated_manifest_bytes, sealed_manifest_bytes, public_payloads
    )
    updated_ledger_bytes = replace_manifest_hash(
        sealed_ledger_bytes, updated_manifest_bytes
    )
    require(
        strip_manifest_hash_row(updated_ledger_bytes)
        == strip_manifest_hash_row(sealed_ledger_bytes),
        "SHA256SUMS changed beyond the manifest.json hash row",
    )
    package_names = current_package_names()
    verify_ledger(updated_ledger_bytes, package_names, updated_manifest_bytes)

    manifest_path = FIGURE_DIRECTORY / "manifest.json"
    ledger_path = FIGURE_DIRECTORY / "SHA256SUMS"
    planned: list[tuple[Path, bytes]] = [
        *public_payloads.items(),
        (manifest_path, updated_manifest_bytes),
        (ledger_path, updated_ledger_bytes),
    ]
    required_originals = {
        manifest_path: sealed_manifest_bytes,
        ledger_path: sealed_ledger_bytes,
    }
    create_public_directory = require_target_parent()

    temporary_root = Path(
        tempfile.mkdtemp(prefix=".r073g-figure-publication-", dir=ROOT)
    )
    staged: dict[Path, Path] = {}
    backups: dict[Path, Path | None] = {}
    applied: list[Path] = []
    created_public_directory = False
    preserve_temporary = False
    try:
        for index, (target, payload) in enumerate(planned):
            mode = snapshot_mode(target)
            if target in required_originals:
                require(
                    target.read_bytes() == required_originals[target],
                    "sealed metadata changed during publication preflight: "
                    + str(target),
                )
            stage = temporary_root / f"stage-{index:02d}"
            write_staged(stage, payload, mode)
            staged[target] = stage
            if os.path.lexists(target):
                backup = temporary_root / f"backup-{index:02d}"
                shutil.copy2(target, backup, follow_symlinks=False)
                require(
                    backup.read_bytes() == target.read_bytes(),
                    "transaction backup failed: " + str(target),
                )
                backups[target] = backup
            else:
                backups[target] = None

        if create_public_directory:
            PUBLIC_DIRECTORY.mkdir(mode=0o755)
            created_public_directory = True
        require_real_directory(
            PUBLIC_DIRECTORY, "public asset directory during staging"
        )

        for target, _payload in planned:
            require_real_directory(
                target.parent, "transaction target parent"
            )
            require(
                snapshot_is_unchanged(target, backups[target]),
                "transaction target changed during staging: " + str(target),
            )
            applied.append(target)
            os.replace(staged[target], target)

        for path, payload in public_payloads.items():
            require(
                path.is_file()
                and not path.is_symlink()
                and path.read_bytes() == payload
                and path.read_bytes()
                == (FIGURE_DIRECTORY / ("figure" + path.suffix)).read_bytes(),
                "public asset read-back is not byte-identical: " + path.name,
            )
        require(
            manifest_path.read_bytes() == updated_manifest_bytes,
            "manifest read-back mismatch",
        )
        require(
            ledger_path.read_bytes() == updated_ledger_bytes,
            "SHA256SUMS read-back mismatch",
        )
        verify_publication_contract(
            manifest_path.read_bytes(), sealed_manifest_bytes, public_payloads
        )
        verify_ledger(ledger_path.read_bytes(), package_names)
        require(
            strip_manifest_hash_row(ledger_path.read_bytes())
            == strip_manifest_hash_row(sealed_ledger_bytes),
            "committed ledger changed beyond the manifest.json row",
        )
        for name in package_names:
            if name in OVERLAY_FILES:
                continue
            require(
                (FIGURE_DIRECTORY / name).read_bytes()
                == git_bytes(
                    figure_seal_commit, f"{FIGURE_RELATIVE}/{name}"
                ),
                "sealed figure file changed during publication: " + name,
            )
    except BaseException as exc:
        failures = rollback(
            applied, backups, created_public_directory, temporary_root
        )
        if failures:
            preserve_temporary = True
            raise RuntimeError(
                "R0.73G publication failed and rollback was incomplete: "
                + "; ".join(failures)
                + "; recovery files preserved at "
                + str(temporary_root)
            ) from exc
        raise
    finally:
        if not preserve_temporary:
            shutil.rmtree(temporary_root, ignore_errors=True)

    print(
        json.dumps(
            {
                "status": "published",
                "figureSealCommit": figure_seal_commit,
                "head": head,
                "assets": [
                    path.relative_to(ROOT).as_posix() for path in public_payloads
                ],
                "manifestSha256": sha256_bytes(updated_manifest_bytes),
                "ledgerChange": "manifest.json row only",
            },
            indent=2,
            sort_keys=True,
        )
    )


def main() -> int:
    try:
        args = arguments()
        publish(args.figure_seal_commit)
    except (OSError, RuntimeError, subprocess.SubprocessError, ValueError) as exc:
        print("R0.73G figure publication refused: " + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
