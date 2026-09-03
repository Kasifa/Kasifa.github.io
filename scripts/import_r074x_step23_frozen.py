#!/usr/bin/env python3
"""Import the frozen R0.74X Step 23 research and figure archives exactly."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R074X_STEP23_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
HANDOFF_COMMIT = "9bddf4a591a159ac99f43602700a80f736dcc61b"
HANDOFF_PATH = "research/r074x_publication_handoff.md"
HANDOFF_SHA256 = "c5bf4fc67476a489f3f473635d4b2106590457f0308208046d937989967a2122"
SOURCE_COMMIT = "802e5572b3490b326a03706c512f35ef6f5afa31"
FIGURE_COMMIT = "a5670383091098331b557869a57c6ed9b6fa72e9"
FIGURE_ID = "fig-r074x-three-packet-payment-gate"
FIGURE_PREFIX = f"research/figures/r074x/{FIGURE_ID}/"

FROZEN = {
    "research/r074x_three_packet_fixed_deletion_gate.md": "4fdc9558605afd9557c557c4292ca1af50d52ff54f9aa11603f15c97a97b3ee3",
    "research/r074x_three_packet_fixed_deletion_gate_primary_audit.md": "834ec846c3f8629f9e7462caf4503bfa99ba6b88288da2dd525793206de9357e",
    "research/r074x_three_packet_fixed_deletion_literature_audit.md": "f58f7a1d095ba6bd8b27c41872301fd367fe784597160fe060f9cd332c64c422",
    "research/r074x_three_packet_fixed_deletion_gate_certificate.json": "61f379041752142e2d1dd6d20288643f92dc64e8df73d2c26b34f6c9b847b76e",
    "research/r074x_three_packet_fixed_deletion_gate_certificate_report.md": "39357cf2cfc40cb86244e7f6ce3bf5e742f7931c1f1398e2fca3ca28533475f3",
    "research/r074x_three_packet_fixed_deletion_gate_independent_audit.md": "6b28a7dd454b4b75c8cd2cdaa86cd2e2727913540d86babd8d011584aa35c1b6",
    "research/r074x_three_packet_fixed_deletion_gate_qa_report.md": "ba46f446634a3be0584b50fdfc035f26c83f8e013bab9ea92ae04230f9531fc4",
    "scripts/r074x_three_packet_fixed_deletion_gate_certificate.py": "3a8a028b8d66e04f41e728bdc639ae23dc8fddfd2b6d2528ddf51023b467b00d",
    "scripts/r074x_three_packet_fixed_deletion_gate_certificate_independent.rb": "c019cb65ef3be236be42e44e0840dce755f2d63fc77bb21fee6873f5cc9790ec",
    "scripts/r074x_three_packet_fixed_deletion_gate_qa.sh": "c44636c754004158788552755d1bbf1231bd91b78789de1120574a2fc959775c",
}

KEY_FIGURE_HASHES = {
    "figure.svg": "e0e858e33c799b567e39ce22735bbeb024c3b32b2ead54f6bc170efe3e497c5a",
    "figure.png": "cd8994befbbf2c0c84925de0a8c84c1c8a264c86a87efed85317b334cbf6e835",
    "figure.pdf": "a4dc69fb82457420d7883f9ba6785751e7d7c9f7465218ca89748ea0aa01301f",
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
    if len(rows) != 25 or sum(row[1] for row in rows) != 3_096_940:
        raise SystemExit("figure inventory drift")

    for name, _, data in rows:
        expected = KEY_FIGURE_HASHES.get(name)
        for mirror in (
            f"research/figures/r074x/{FIGURE_ID}/{name}",
            f"figures/r074x/{FIGURE_ID}/{name}",
            f"public/figures/r074x/{FIGURE_ID}/{name}",
        ):
            write_exact(mirror, data, expected)

    for extension in ("svg", "png", "pdf"):
        name = f"figure.{extension}"
        data = next(payload for item, _, payload in rows if item == name)
        write_exact(f"public/assets/r074x/{FIGURE_ID}.{extension}", data, KEY_FIGURE_HASHES[name])

    print({
        "status": "PASS",
        "release": "R0.74X Step 23",
        "handoff": HANDOFF_COMMIT,
        "source": SOURCE_COMMIT,
        "figure": FIGURE_COMMIT,
        "frozenResearchFiles": len(FROZEN),
        "figureFiles": len(rows),
        "figureBytes": sum(row[1] for row in rows),
    })


if __name__ == "__main__":
    main()
