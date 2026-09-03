#!/usr/bin/env python3
"""Import only the frozen R0.74Y Step 24 handoff whitelist."""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R074Y_STEP24_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
HANDOFF_COMMIT = "87e32a45c78ee7131a919ebb51768714cd561b62"
HANDOFF_PATH = "research/r074y_publication_handoff.md"
HANDOFF_SHA256 = "d333ba1223bce44b4d5dd5d23fa123a185402560945899e4416e7a4ab27d53b4"
SOURCE_COMMIT = "e75ccf1197484d0e551e8073f409e6a39b248564"
FROZEN = {
    "research/r074y_payment_compatible_route_screen.md": "6144fe796d6c59a286fc32b3b0aa2b794c50006fdc7879d4595b5958c9646954",
    "research/r074y_payment_compatible_route_screen_primary_audit.md": "c9b8ef6f78d0d196c2f17c6c7b83fe54667a6c80135553695dd7c68325af6f49",
    "research/r074y_payment_compatible_route_literature_audit.md": "e93275e31b1f04b1878071123fa3471a90e88fee5bb2b0dfd26afa6abf8d43a6",
    "research/r074y_payment_compatible_route_screen_certificate.json": "372779f48a53c0333f1d736528aab6eb74997dc9eac3da0634178052501dd80a",
    "research/r074y_payment_compatible_route_screen_certificate_report.md": "782c694f9edb49d668a473837d9c43f60b311ace9a9f9175b8870cac4291f2ae",
    "research/r074y_payment_compatible_route_screen_independent_audit.md": "b17af2ab982a85cd29a0fc7f3a632b390594505dd3c26e4afdff3ad0f5636d9e",
    "research/r074y_payment_compatible_route_screen_qa_report.md": "4ad724a6bd9ab9a344cb1ef579ba7ef47ebf3fa8cc8832c2c45cbe4be50fefbf",
    "scripts/r074y_payment_compatible_route_screen_certificate.py": "c0d6ee583bdc08fb42cf5cbf9b1e7fced3447b410434193d5004cc4b335a2dd2",
    "scripts/r074y_payment_compatible_route_screen_certificate_independent.rb": "d8e0d303e31b676eb143e94aab111d7c1126de6c26c34258103610fccdaa5435",
    "scripts/r074y_payment_compatible_route_screen_qa.sh": "675cbfe8e81be74b01d65a2dd035deaa4dee5d2d09ca20f7491b42e2d67c1a04",
}


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
    ledger = re.findall(r"\| ([0-9a-f]{64}) \| ([^|]+?) \|", handoff.decode("utf-8"))
    if len(ledger) != 10:
        raise SystemExit(f"frozen ledger drift: {len(ledger)} != 10")
    parsed = {relative.strip(): expected for expected, relative in ledger}
    if parsed != FROZEN:
        raise SystemExit("handoff whitelist drift")

    for source_path, expected in FROZEN.items():
        write_exact(source_path, git_bytes(SOURCE_COMMIT, source_path), expected)

    print({
        "status": "PASS",
        "release": "R0.74Y Step 24",
        "handoff": HANDOFF_COMMIT,
        "source": SOURCE_COMMIT,
        "frozenFiles": len(FROZEN),
        "formalFigure": False,
        "recap": False,
    })


if __name__ == "__main__":
    main()
