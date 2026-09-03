#!/usr/bin/env python3
"""Import the frozen R0.74U Step 20 handoff without altering source bytes."""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R074U_STEP20_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
HANDOFF_COMMIT = "f3031095b7dfa51837df511f5b015bacb34c473b"
HANDOFF_PATH = "research/r074u_publication_handoff.md"
HANDOFF_SHA256 = "115620fe742b3321c7d1422743b202ab83886beb4016fd8da45c81142d66a22b"
SOURCE_COMMIT = "735030d9e51068518796a79571ada291c5414a06"
CORE_COMMIT = "d74e7b297928147334136f4c3cb29c5226d66381"
FIGURE_COMMIT = "8b75193df63a962392f89fcf1dbc20a8411334ba"
FIGURE_ID = "fig-r074u-intrinsic-certified-residence"
FIGURE_PREFIX = f"research/figures/r074u/{FIGURE_ID}/"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(SOURCE), "show", f"{commit}:{path}"])


def write_exact(relative: str, data: bytes, expected: str) -> None:
    if sha256(data) != expected:
        raise SystemExit(f"source hash drift: {relative}")
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    if sha256(target.read_bytes()) != expected:
        raise SystemExit(f"import hash drift: {relative}")


def main() -> None:
    for commit in (HANDOFF_COMMIT, SOURCE_COMMIT, CORE_COMMIT, FIGURE_COMMIT):
        resolved = subprocess.check_output(
            ["git", "-C", str(SOURCE), "rev-parse", f"{commit}^{{commit}}"], text=True
        ).strip()
        if resolved != commit:
            raise SystemExit(f"frozen commit drift: {commit} -> {resolved}")

    handoff = git_bytes(HANDOFF_COMMIT, HANDOFF_PATH)
    write_exact(HANDOFF_PATH, handoff, HANDOFF_SHA256)
    ledger = re.findall(r"\| `([0-9a-f]{64})` \| `([^`]+)` \|", handoff.decode("utf-8"))
    if len(ledger) != 35:
        raise SystemExit(f"frozen ledger drift: {len(ledger)} != 35")

    figure_rows: list[tuple[str, bytes, str]] = []
    for expected, source_path in ledger:
        data = git_bytes(SOURCE_COMMIT, source_path)
        write_exact(source_path, data, expected)
        if source_path.startswith(FIGURE_PREFIX):
            name = source_path.removeprefix(FIGURE_PREFIX)
            figure_rows.append((name, data, expected))
            for mirror in (
                f"figures/r074u/{FIGURE_ID}/{name}",
                f"public/figures/r074u/{FIGURE_ID}/{name}",
            ):
                write_exact(mirror, data, expected)

    if len(figure_rows) != 25:
        raise SystemExit(f"figure inventory drift: {len(figure_rows)} != 25")
    for extension in ("svg", "pdf", "png"):
        name = f"figure.{extension}"
        data, expected = next((data, expected) for item, data, expected in figure_rows if item == name)
        write_exact(f"public/assets/r074u/{FIGURE_ID}.{extension}", data, expected)

    print({
        "status": "PASS",
        "release": "R0.74U Step 20",
        "handoff": HANDOFF_COMMIT,
        "source": SOURCE_COMMIT,
        "frozenFiles": len(ledger),
        "figureFiles": len(figure_rows),
    })


if __name__ == "__main__":
    main()
