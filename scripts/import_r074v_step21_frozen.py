#!/usr/bin/env python3
"""Import the frozen R0.74V Step 21 handoff without altering source bytes."""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R074V_STEP21_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
HANDOFF_COMMIT = "2bd41a53800b2d6f532b6843f4d70ad7fad7ed46"
HANDOFF_PATH = "research/r074v_publication_handoff.md"
HANDOFF_SHA256 = "3832ebf8b0fc84ecbb21d064ee3c94a73ce2f56966f29a0d911a6a411c2697ca"
SOURCE_COMMIT = "29f2b56d1a1a22b665de4b36736eeea20c0a0039"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(commit: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(SOURCE), "show", f"{commit}:{relative}"])


def write_exact(relative: str, data: bytes, expected: str) -> None:
    if sha256(data) != expected:
        raise SystemExit(f"source hash drift: {relative}")
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    if sha256(target.read_bytes()) != expected:
        raise SystemExit(f"import hash drift: {relative}")


def main() -> None:
    for commit in (HANDOFF_COMMIT, SOURCE_COMMIT):
        resolved = subprocess.check_output(
            ["git", "-C", str(SOURCE), "rev-parse", f"{commit}^{{commit}}"], text=True
        ).strip()
        if resolved != commit:
            raise SystemExit(f"frozen commit drift: {commit} -> {resolved}")
    if subprocess.run(
        ["git", "-C", str(SOURCE), "merge-base", "--is-ancestor", SOURCE_COMMIT, HANDOFF_COMMIT]
    ).returncode != 0:
        raise SystemExit("frozen source commit is not an ancestor of the handoff commit")

    handoff = git_bytes(HANDOFF_COMMIT, HANDOFF_PATH)
    write_exact(HANDOFF_PATH, handoff, HANDOFF_SHA256)
    ledger = re.findall(r"\| `([0-9a-f]{64})` \| `([^`]+)` \|", handoff.decode("utf-8"))
    if len(ledger) != 9:
        raise SystemExit(f"frozen ledger drift: {len(ledger)} != 9")

    for expected, source_path in ledger:
        write_exact(source_path, git_bytes(SOURCE_COMMIT, source_path), expected)

    print({
        "status": "PASS",
        "release": "R0.74V Step 21",
        "handoff": HANDOFF_COMMIT,
        "source": SOURCE_COMMIT,
        "frozenFiles": len(ledger),
        "formalFigure": False,
        "recap": False,
    })


if __name__ == "__main__":
    main()
