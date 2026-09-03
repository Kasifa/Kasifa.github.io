#!/usr/bin/env python3
"""Import the frozen R0.74W Step 22 research and figure archives exactly."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R074W_STEP22_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
HANDOFF_COMMIT = "eb72349afeb5f7b02ee133b7c4d10466e2ae8ff4"
HANDOFF_PATH = "research/r074w_publication_handoff.md"
HANDOFF_SHA256 = "01a9d5cb2d9a5d2c7a8f57c8e8fca964f2c59b330eebc2975b0e968840e1ec5b"
SOURCE_COMMIT = "f581c46ee7759c190b6f407633549e7106ff60b5"
FIGURE_COMMIT = "0143d65322a3c854fe220aa9d3e4f93a1f6ca09e"
FIGURE_ID = "fig-r074w-remote-adjacent-inward-threshold"
FIGURE_PREFIX = f"research/figures/r074w/{FIGURE_ID}/"

FROZEN = {
    "research/r074w_remote_adjacent_inward_comparison.md": "d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10",
    "research/r074w_remote_adjacent_inward_comparison_primary_audit.md": "66ec78f67bba64c555a92e9a616c477d702ebb200b48bbfc08a353bdfde5bb73",
    "research/r074w_remote_adjacent_inward_literature_audit.md": "ec6259d95990fd6a8357d9685cc3f17e300e672c1add911a5eb64c6291f3bb99",
    "research/r074w_remote_adjacent_inward_comparison_certificate.json": "7c0b86b6f4f9a5782946f443bdf731445adbce9069fcba726a7b8fe75df9c171",
    "research/r074w_remote_adjacent_inward_comparison_certificate_report.md": "d70b18dbde23d49e51ec24c1cf8e0f764a5a639297ce783bcc23bf69d050b003",
    "research/r074w_remote_adjacent_inward_comparison_independent_audit.md": "dd6a2b1820da126e049aae97ab9b26bb9ef0d02bacca1dc248298303bb2748a3",
    "research/r074w_remote_adjacent_inward_comparison_qa_report.md": "26df7a1b5fbff87f752a8cebb98113b4fcc13f3b8828566b3fab2eda07e7f223",
    "scripts/r074w_remote_adjacent_inward_comparison_certificate.py": "33084928360a5b649ae862cc416679deca8e34574820095f7ffdac52bb760395",
    "scripts/r074w_remote_adjacent_inward_comparison_certificate_independent.rb": "ff69d1f31d90bea7ec4b6d935d75870bb633f027ffb91bacd073da2d7a4916a4",
    "scripts/r074w_remote_adjacent_inward_comparison_qa.sh": "40c798d56d3845753abc5fe5a2ee022f7a62716ed98ef5184c7f82e039d0f5db",
}

KEY_FIGURE_HASHES = {
    "figure.svg": "d5d3bb5aa4e407bbbd340482432ab055dd743026bb9286411e23914b1a35adef",
    "figure.png": "a20af302fa70828f4f9870b2afd14757ac858f30f0f4c618d6aa5af0b2c5b5c6",
    "figure.pdf": "85c0876206ac0976302858e2f588d7295ed3f2326616228c7394772e4e52a52c",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(commit: str, repository_path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(SOURCE), "show", f"{commit}:{repository_path}"])


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

    write_exact(HANDOFF_PATH, git_bytes(HANDOFF_COMMIT, HANDOFF_PATH), HANDOFF_SHA256)
    for repository_path, expected in FROZEN.items():
        write_exact(repository_path, git_bytes(SOURCE_COMMIT, repository_path), expected)

    listing = subprocess.check_output(
        ["git", "-C", str(SOURCE), "ls-tree", "-r", "--long", FIGURE_COMMIT, "--", FIGURE_PREFIX],
        text=True,
    ).splitlines()
    rows: list[tuple[str, int, bytes]] = []
    for row in listing:
        metadata, repository_path = row.split("\t", 1)
        byte_count = int(metadata.split()[3])
        name = repository_path.removeprefix(FIGURE_PREFIX)
        data = git_bytes(FIGURE_COMMIT, repository_path)
        if len(data) != byte_count:
            raise SystemExit(f"figure byte-count drift: {name}")
        rows.append((name, byte_count, data))
    if len(rows) != 25 or sum(row[1] for row in rows) != 3_774_363:
        raise SystemExit("figure inventory drift")

    for name, _, data in rows:
        expected = KEY_FIGURE_HASHES.get(name)
        for mirror in (
            f"research/figures/r074w/{FIGURE_ID}/{name}",
            f"figures/r074w/{FIGURE_ID}/{name}",
            f"public/figures/r074w/{FIGURE_ID}/{name}",
        ):
            write_exact(mirror, data, expected)

    for extension in ("svg", "png", "pdf"):
        name = f"figure.{extension}"
        data = next(payload for item, _, payload in rows if item == name)
        write_exact(f"public/assets/r074w/{FIGURE_ID}.{extension}", data, KEY_FIGURE_HASHES[name])

    print({
        "status": "PASS",
        "release": "R0.74W Step 22",
        "handoff": HANDOFF_COMMIT,
        "source": SOURCE_COMMIT,
        "figure": FIGURE_COMMIT,
        "frozenResearchFiles": len(FROZEN),
        "figureFiles": len(rows),
        "figureBytes": sum(row[1] for row in rows),
    })


if __name__ == "__main__":
    main()
