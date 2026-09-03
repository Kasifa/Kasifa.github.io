#!/usr/bin/env python3
"""Import only the frozen R0.74Z Step 25 handoff whitelist and figure archive."""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R074Z_STEP25_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
HANDOFF_COMMIT = "90c6ceedb0e1f9fff02a32a81356376e138cc428"
HANDOFF_PATH = "research/r074z_publication_handoff.md"
HANDOFF_SHA256 = "decf708987cd3f210ca672397c566e7006b7fae3cba5b1079410af56a588a091"
SOURCE_COMMIT = "91aaac829c6b54a0ad24cf10ff3f533f58a10035"
FIGURE_COMMIT = "30ed47c9ae2334a9e9cb3468a5094dfb3dc65907"
FIGURE_ID = "fig-r074z-remote-persistence-gate"
FIGURE_PREFIX = f"research/figures/r074z/{FIGURE_ID}/"

FROZEN = {
    "research/r074z_cancellation_cell_gate.md": "bb766da4002da760c35185294081f80df97c349ea08b198a5f76db31663aaf6a",
    "research/r074z_cancellation_cell_gate_primary_audit.md": "6b867551bce840cb382cd13cb2ff298affbf0c0d8b1357a8163c5cedc9bace08",
    "research/r074z_cancellation_cell_gate_literature_audit.md": "8e5346ecf3c2beef4a620e0844e790703b628388ca7f0a6997aae88818caa82f",
    "research/r074z_cancellation_cell_gate_certificate.json": "aff6d6d39b2163a263bc2a5055225d9c25d5b46d0b2704bdfcb276976dcc2285",
    "research/r074z_cancellation_cell_gate_certificate_report.md": "91602c567e612759baf9bd03c7c688465c39997b90e445de13cc159f44cf5154",
    "research/r074z_cancellation_cell_gate_independent_audit.md": "cd44004a02c3486b734b17e2261dcd725a3d287f5462d7480ec7b294e2f43420",
    "research/r074z_cancellation_cell_gate_qa_report.md": "868afc8a69413e3176553acdb97bc03451de2181671684a207b01e7367d4e71f",
    "scripts/r074z_cancellation_cell_gate_certificate.py": "512cefac3d22dcc6836b128c052a9a528203be1e7ffd7217f16556193448631a",
    "scripts/r074z_cancellation_cell_gate_certificate_independent.rb": "766edac40dc9a3686067cad1ea31c01972075f1aa453e02e7fa4b461629a706c",
    "scripts/r074z_cancellation_cell_gate_qa.sh": "beaef0722e27813e4a0a164372355b2d5521413dad35e7f34d8b177f5842689a",
}

KEY_FIGURE_HASHES = {
    "figure.svg": "31cfcd6e5e8e57729a8c5bce7459def3a618cd5bbda842a066331770ad0ffd42",
    "figure.png": "0414ade9d42a899830affe8ae730212946362ba72bc3a39bcf05c61df509368c",
    "figure.pdf": "4918a691914b23fd3570847510e57663d8db3ddad8a5707873943434b400d7b0",
    "manifest.json": "692cb2b9e4e4973e7daff2320196bd56aed424ceba671a749c1dc7e833155d9c",
    "validation.json": "827499c45aabce04624913311535218bec14e5310c27b3797b25957cbded48e1",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(commit: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(SOURCE), "show", f"{commit}:{relative}"])


def write_exact(relative: str, data: bytes, expected: str | None = None) -> None:
    if expected is not None and sha256(data) != expected:
        raise SystemExit(f"source hash drift: {relative}")
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    if target.read_bytes() != data:
        raise SystemExit(f"import byte drift: {relative}")


def main() -> None:
    for commit in (HANDOFF_COMMIT, SOURCE_COMMIT, FIGURE_COMMIT):
        resolved = subprocess.check_output(
            ["git", "-C", str(SOURCE), "rev-parse", f"{commit}^{{commit}}"], text=True
        ).strip()
        if resolved != commit:
            raise SystemExit(f"frozen commit drift: {commit} -> {resolved}")
    for ancestor in (SOURCE_COMMIT, FIGURE_COMMIT):
        if subprocess.run(
            ["git", "-C", str(SOURCE), "merge-base", "--is-ancestor", ancestor, HANDOFF_COMMIT],
            check=False,
        ).returncode != 0:
            raise SystemExit(f"frozen commit is not an ancestor of handoff: {ancestor}")

    handoff = git_bytes(HANDOFF_COMMIT, HANDOFF_PATH)
    write_exact(HANDOFF_PATH, handoff, HANDOFF_SHA256)
    ledger = re.findall(r"\| ([0-9a-f]{64}) \| ([^|]+?) \|", handoff.decode("utf-8"))
    if len(ledger) != 10:
        raise SystemExit(f"frozen ledger drift: {len(ledger)} != 10")
    parsed = {relative.strip(): expected for expected, relative in ledger}
    if parsed != FROZEN:
        raise SystemExit("handoff whitelist drift")

    for source_path, expected in FROZEN.items():
        write_exact(source_path, git_bytes(SOURCE_COMMIT, source_path), expected)

    listing = subprocess.check_output(
        ["git", "-C", str(SOURCE), "ls-tree", "-r", "--long", FIGURE_COMMIT, "--", FIGURE_PREFIX],
        text=True,
    ).splitlines()
    rows: list[tuple[str, int, bytes]] = []
    for row in listing:
        metadata, repository_path = row.split("\t", 1)
        byte_count = int(metadata.split()[3])
        name = repository_path.removeprefix(FIGURE_PREFIX)
        if not name or "/" in name or name in {".", ".."}:
            raise SystemExit(f"figure path drift: {repository_path}")
        data = git_bytes(FIGURE_COMMIT, repository_path)
        if len(data) != byte_count:
            raise SystemExit(f"figure byte-count drift: {name}")
        rows.append((name, byte_count, data))
    if len(rows) != 25 or sum(row[1] for row in rows) != 3_032_354:
        raise SystemExit("figure inventory drift")
    row_names = {row[0] for row in rows}
    if not set(KEY_FIGURE_HASHES).issubset(row_names):
        raise SystemExit("key figure inventory drift")

    for name, _, data in rows:
        expected = KEY_FIGURE_HASHES.get(name)
        for mirror in (
            f"research/figures/r074z/{FIGURE_ID}/{name}",
            f"figures/r074z/{FIGURE_ID}/{name}",
            f"public/figures/r074z/{FIGURE_ID}/{name}",
        ):
            write_exact(mirror, data, expected)

    for extension in ("svg", "png", "pdf"):
        name = f"figure.{extension}"
        data = next(payload for item, _, payload in rows if item == name)
        write_exact(f"public/assets/r074z/{FIGURE_ID}.{extension}", data, KEY_FIGURE_HASHES[name])

    print({
        "status": "PASS",
        "release": "R0.74Z Step 25",
        "handoff": HANDOFF_COMMIT,
        "source": SOURCE_COMMIT,
        "figure": FIGURE_COMMIT,
        "frozenResearchFiles": len(FROZEN),
        "figureFiles": len(rows),
        "figureBytes": sum(row[1] for row in rows),
    })


if __name__ == "__main__":
    main()
