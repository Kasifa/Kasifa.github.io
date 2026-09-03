#!/usr/bin/env python3
"""Import the frozen R0.74T Step 19 handoff without altering source bytes."""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R074T_STEP19_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
HANDOFF_COMMIT = "cbe52bd5df2dfdb948b0ac8bb761ccd8774004f1"
HANDOFF_PATH = "research/r074t_publication_handoff.md"
HANDOFF_SHA256 = "13ff4edeeebf1da9c9356246c3308e67109857bf36fbceb67fcba5188c1fa71f"
SOURCE_COMMIT = "2a3a59d4626face7b883159ee9b18500005e41d7"
CORE_COMMIT = "b120598d36140385676bb4a9922d46abcdff0ba4"
FIGURE_COMMIT = "0433c129868ddf349c7b64d427747f590fa06898"
FIGURE_ID = "fig-r074t-schedule-invariant-dwell-barrier"
FIGURE_PREFIX = f"research/figures/r074t/{FIGURE_ID}/"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(SOURCE), "show", f"{commit}:{path}"])


def git_text(commit: str, path: str) -> str:
    return git_bytes(commit, path).decode("utf-8")


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
    ledger = re.findall(
        r"\| `([0-9a-f]{64})` \| `([^`]+)` \|",
        handoff.decode("utf-8"),
    )
    if len(ledger) != 35:
        raise SystemExit(f"frozen ledger drift: {len(ledger)} != 35")

    figure_rows = []
    for expected, source_path in ledger:
        data = git_bytes(SOURCE_COMMIT, source_path)
        write_exact(source_path, data, expected)
        if source_path.startswith(FIGURE_PREFIX):
            name = source_path.removeprefix(FIGURE_PREFIX)
            figure_rows.append((name, data, expected))
            for mirror in (
                f"figures/r074t/{FIGURE_ID}/{name}",
                f"public/figures/r074t/{FIGURE_ID}/{name}",
            ):
                write_exact(mirror, data, expected)

    if len(figure_rows) != 25:
        raise SystemExit(f"figure inventory drift: {len(figure_rows)} != 25")
    for extension in ("svg", "pdf", "png"):
        name = f"figure.{extension}"
        data, expected = next((data, expected) for item, data, expected in figure_rows if item == name)
        write_exact(f"public/assets/r074t/{FIGURE_ID}.{extension}", data, expected)

    print({
        "status": "PASS",
        "release": "R0.74T Step 19",
        "handoff": HANDOFF_COMMIT,
        "source": SOURCE_COMMIT,
        "frozenFiles": len(ledger),
        "figureFiles": len(figure_rows),
    })


if __name__ == "__main__":
    main()
