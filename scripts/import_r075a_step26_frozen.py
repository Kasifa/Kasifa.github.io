#!/usr/bin/env python3
"""Import only the frozen R0.75A Step 26 handoff whitelist, recap delta, and figure archive."""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075A_STEP26_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
HANDOFF_COMMIT = "8c3c7e617d486abb31ae7207f38a97282d06b047"
HANDOFF_PATH = "research/r075a_publication_handoff.md"
HANDOFF_SHA256 = "489b2f4b67d88974c555ea22e543906b9cd5cd469f135562fdca6c2aad0ad581"
SOURCE_COMMIT = "d15b7d8f9a3b16b63b4f324c75c9e156e9d03ff8"
FIGURE_COMMIT = "243969b9d75d71224070bbdb3da64ce0103c1441"
RECAP_COMMIT = "9f01a3a8df2f60633a16e41eb2a1cb606c750198"
FIGURE_ID = "fig-r075a-local-persistence-payment"
FIGURE_PREFIX = f"research/figures/r075a/{FIGURE_ID}/"

FROZEN = {
    "research/r075a_spectral_persistence_payment_dichotomy.md": "f8117a7ff6380676d2ed05e749119579cc3f6972463834dcc6ad2a0b03026388",
    "research/r075a_spectral_persistence_payment_dichotomy_primary_audit.md": "c599a1dcee8a82ec1c91512d5b664b1394707fd6d69ac2ca7ba022ebf715d3f6",
    "research/r075a_spectral_persistence_payment_dichotomy_literature_audit.md": "169eff2e607338ae990fb9994db3f75e11830246a36ee5cce8a7376e64302cea",
    "research/r075a_spectral_route_risk_audit.md": "ff712f4a846e70a35a5936348574b77ca59ca78c46e56c488ebb4731650afd35",
    "research/r075a_spectral_persistence_payment_dichotomy_certificate.json": "7f504c91bcfcb8ba463c0dec977d946d8f36b26b4f732a2082863bbe5221a38e",
    "research/r075a_spectral_persistence_payment_dichotomy_certificate_report.md": "bfb87b97e661703c4a7ddd6231b50058dfe116d0d9343d9a6e4c1554714ef238",
    "research/r075a_spectral_persistence_payment_dichotomy_certificate_independent_audit.md": "966335bf8a6e759abda01c61d17ef3be4ee3c76e6dd4396b33d6488874dc4960",
    "research/r075a_spectral_persistence_payment_dichotomy_certificate_qa_report.md": "83cc4ff615823d1ce8b1b87d60004bf310f86b4faac2d876fb49b8deef2f0d84",
    "scripts/r075a_spectral_persistence_payment_dichotomy_certificate.py": "d5256d8ea9db81adc5133e3cce69b9f7089f8ab8a2c5d39f30877815e6052e5a",
    "scripts/r075a_spectral_persistence_payment_dichotomy_certificate_independent.rb": "30d28440b4cba3b0578fa7644cf5539ff6a2806f449c020d6cd1718e553ade27",
    "scripts/r075a_spectral_persistence_payment_dichotomy_certificate_qa.sh": "b9b07e3d1a8d1303111cf1978481530e791f3e14d81b6865674d16f73caa2538",
}

RECAP = {
    "research/r075a_milestone_recap_delta.md": "7dd9ac686d0c599b21992bf7622e862f88caf0480f6e27f2cb82b9aaf844eee1",
    "research/r075a_milestone_recap_delta_independent_audit.md": "f727eb01002772936b5f8aa6e7212e238c7e0e04ab546261232f4abcee9d9b82",
}

KEY_FIGURE_HASHES = {
    "SHA256SUMS": "bc8ecc26ed0cd934dc7d74060ac94960ecde9a7fcbeb8364b19739023f152373",
    "figure.svg": "cfbb92394ebbcb5ce9603b3f7df32568e37837c5b2238112b69bfec31f8dfe27",
    "figure.png": "81546061c9febeac81ff683e8a7bd0811d7a9f3c10a90db05037febc0ee25d70",
    "figure.pdf": "ab588b17586d556744bebe8a5957725f4f92033bc1d0133619710c76aee13f5f",
    "manifest.json": "f354dc90a34f8f322bfce0a6f9879487f417e483b0fe128d875e7dec3e9c7a38",
    "validation.json": "91cfa04c6f807b5112c08cd1d11fc34e5fa760634158de8520439b159b589f98",
    "qa-report.md": "098a99edfaf30f8df50ab4605774d714c56fc32b88a448aa5805d82a393c6aa0",
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
    for commit in (HANDOFF_COMMIT, SOURCE_COMMIT, FIGURE_COMMIT, RECAP_COMMIT):
        resolved = subprocess.check_output(
            ["git", "-C", str(SOURCE), "rev-parse", f"{commit}^{{commit}}"], text=True
        ).strip()
        if resolved != commit:
            raise SystemExit(f"frozen commit drift: {commit} -> {resolved}")
    for ancestor in (SOURCE_COMMIT, FIGURE_COMMIT, RECAP_COMMIT):
        if subprocess.run(
            ["git", "-C", str(SOURCE), "merge-base", "--is-ancestor", ancestor, HANDOFF_COMMIT],
            check=False,
        ).returncode != 0:
            raise SystemExit(f"frozen commit is not an ancestor of handoff: {ancestor}")

    handoff = git_bytes(HANDOFF_COMMIT, HANDOFF_PATH)
    write_exact(HANDOFF_PATH, handoff, HANDOFF_SHA256)
    ledger = re.findall(r"\| `([0-9a-f]{64})` \| `([^`]+)` \|", handoff.decode("utf-8"))
    parsed = {relative: expected for expected, relative in ledger}
    if parsed != {**FROZEN, **RECAP}:
        raise SystemExit(f"handoff whitelist drift: {len(parsed)} entries")

    for source_path, expected in FROZEN.items():
        write_exact(source_path, git_bytes(SOURCE_COMMIT, source_path), expected)
    for source_path, expected in RECAP.items():
        write_exact(source_path, git_bytes(RECAP_COMMIT, source_path), expected)

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
    if len(rows) != 25 or sum(row[1] for row in rows) != 2_588_462:
        raise SystemExit("figure inventory drift")
    if not set(KEY_FIGURE_HASHES).issubset({row[0] for row in rows}):
        raise SystemExit("key figure inventory drift")

    for name, _, data in rows:
        expected = KEY_FIGURE_HASHES.get(name)
        for mirror in (
            f"research/figures/r075a/{FIGURE_ID}/{name}",
            f"figures/r075a/{FIGURE_ID}/{name}",
            f"public/figures/r075a/{FIGURE_ID}/{name}",
        ):
            write_exact(mirror, data, expected)

    for extension in ("svg", "png", "pdf"):
        name = f"figure.{extension}"
        data = next(payload for item, _, payload in rows if item == name)
        write_exact(f"public/assets/r075a/{FIGURE_ID}.{extension}", data, KEY_FIGURE_HASHES[name])

    print({
        "status": "PASS",
        "release": "R0.75A Step 26",
        "handoff": HANDOFF_COMMIT,
        "source": SOURCE_COMMIT,
        "figure": FIGURE_COMMIT,
        "recap": RECAP_COMMIT,
        "frozenResearchFiles": len(FROZEN),
        "recapFiles": len(RECAP),
        "figureFiles": len(rows),
        "figureBytes": sum(row[1] for row in rows),
    })


if __name__ == "__main__":
    main()
