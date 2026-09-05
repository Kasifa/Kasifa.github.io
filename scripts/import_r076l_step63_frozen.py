#!/usr/bin/env python3
"""Import the frozen R0.76L Step 63 research objects and formal figure package."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R076L_STEP63_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
PREDECESSOR_HANDOFF_COMMIT = "17bec49703836115f2e8a32a4bae516071433902"
INITIAL_SOURCE_COMMIT = "6fe15fac7db9c3befbb3bab021787dfd6e76639e"
SOURCE_COMMIT = "b234b63c24c7b19efc703367e23b092385066a1c"
CERTIFICATE_COMMIT = "2f3e0f466cc38fd2b61f2c79773352d95b2464e1"
HANDOFF_COMMIT = "a5edefb014ebc6dd13ce052aad196ff5115b9629"
HANDOFF_PATH = "research/r076l_publication_handoff.md"
HANDOFF_SHA256 = "3a02aaf0544a5cf68250894ae608820c8027d2af3435497002bdf7675a55cdf4"
HANDOFF_AUDIT_PATH = "research/r076l_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "c6fb0cd85dd136088f4e4d6dfafa3de759024b49606a243626e303eb7e795b03"
FIGURE_ID = "fig-r076l-parabolic-edge"
FIGURE_SOURCE_PREFIX = f"figures/r076l-parabolic-edge/{FIGURE_ID}/"

FROZEN = {
    "research/r076l_parabolic_edge_smoothing_complete_clock.md": "13492867aa83ead472d8db8d55c9a5d8c65a2418b1de397e0cffdd845b8a5c7a",
    "research/r076l_parabolic_edge_smoothing_complete_clock_certificate.json": "cdd0fd35a67e863cc767d889e2d1abc7332ee0c74939834423f2d4c66f62ae9b",
    "research/r076l_parabolic_edge_smoothing_complete_clock_certificate_report.md": "1b96a8e293f2fe43ea1c539e148525052e88c59aa2039788831ba96cb62cb6c9",
    "research/r076l_parabolic_edge_smoothing_complete_clock_independent_audit.md": "3c06bfb4ffe45c2b0dac17018e915841582f3ba06def65f15fa3a97b449c159d",
    "research/r076l_parabolic_edge_smoothing_complete_clock_primary_audit.md": "5fe138cb857ea9e4c34d8fbb404932be45ed809bd96337248839cd9bd67cd8cb",
    "research/r076l_parabolic_edge_smoothing_complete_clock_qa_report.md": "e607cf82699da1cdd541514535a970ed25507fbf0a70a43b2f31fc8e66a6ebff",
    "research/r076l_report-source.md": "dfa2f5087cb2729350886ad304fe04958c6b55e1610bf771d4a197c6846f5f80",
    "scripts/r076l_parabolic_edge_smoothing_complete_clock_certificate.py": "b0410c57bd31c8a9a955d1d88bd2eec634572addb7a0eeb40f5badb38964cb0d",
    "scripts/r076l_parabolic_edge_smoothing_complete_clock_certificate_independent.rb": "2bd698e00b62fdd85d2f601df22aa2e0199bf2c26de49fc3ff9bbcac3ca94904",
    "scripts/r076l_parabolic_edge_smoothing_complete_clock_expected.json": "48dc286d198512034aaee9ce65ef696fe367942c9ea9a6e840ac0e7c31c2f8ed",
    "scripts/r076l_parabolic_edge_smoothing_complete_clock_fixtures.json": "cf442a934bd713ef046f1aa5b6f41ea5a1cfe118e6cef91a30d20a26d16bd1a9",
    "scripts/r076l_parabolic_edge_smoothing_complete_clock_qa.sh": "b434be9cc181882d9dda5a5015a946f9417b173ca3082341bd52fb989a9d6ae9",
    f"{FIGURE_SOURCE_PREFIX}caption.md": "102e7d96396173cc56cacf0e1552241d617c3d9b94495f1404b74e07c3829316",
    f"{FIGURE_SOURCE_PREFIX}config.json": "ec613babd5ff988c732bbd9881962e93dc6e5ef2821832eb22a069b843fece28",
    f"{FIGURE_SOURCE_PREFIX}data.csv": "bbc7139237a9120d91284c0ddb80c0c73aa93708bb4a8f778f38e1d24d18c96d",
    f"{FIGURE_SOURCE_PREFIX}figure.pdf": "6de47c8df62ae35fc85e5b1ca2010038dd505d2e15b39caaa1f765b30cf4e7ea",
    f"{FIGURE_SOURCE_PREFIX}figure.png": "a5bff2596a6bf9ab0becc41cba0a985744c3b31878c6b11281ca2f4cf891fc75",
    f"{FIGURE_SOURCE_PREFIX}figure.svg": "5e9061d5b76b03c60d58cac98320513dc442b7a595604ee9c59697b2e4190662",
    f"{FIGURE_SOURCE_PREFIX}manifest.json": "c6c6e5e6ab980eddf254ec2462b73bc99cc351c05069adb6fb0aefd52719f29f",
    f"{FIGURE_SOURCE_PREFIX}plot.py": "079a32963e6f9bf72771b647683e83d6264e3c1c365ae0004ac58f29b48ba8a2",
    f"{FIGURE_SOURCE_PREFIX}progress.ndjson": "84569637a2602f6832bbbb2cf2b3fe3fcf9698af2aff088904f3f661ed00430d",
    f"{FIGURE_SOURCE_PREFIX}qa-report.md": "4c55f693c1ca644edc778d93f2ee232d8ae55a03b44b0c2d0dd20820260dfb2c",
    f"{FIGURE_SOURCE_PREFIX}render.cjs": "2981e7c156aa9b9807a6c7b92c16d9a99ee48aac4deeb362116eb3849b3fa99d",
    f"{FIGURE_SOURCE_PREFIX}resources.csv": "14f817a9bf9a28dc4f17541f94a26442bee8de83aa2571a6cf92e69cafd517c6",
}

FIGURE_NAMES = tuple(sorted(path.removeprefix(FIGURE_SOURCE_PREFIX) for path in FROZEN if path.startswith(FIGURE_SOURCE_PREFIX)))
FIGURE_BYTES = 599_429


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
    if target.read_bytes() != data:
        raise SystemExit(f"import byte drift: {relative}")


def main() -> None:
    for commit in (PREDECESSOR_HANDOFF_COMMIT, INITIAL_SOURCE_COMMIT, SOURCE_COMMIT, CERTIFICATE_COMMIT, HANDOFF_COMMIT):
        resolved = subprocess.check_output(["git", "-C", str(SOURCE), "rev-parse", f"{commit}^{{commit}}"], text=True).strip()
        if resolved != commit:
            raise SystemExit(f"frozen commit drift: {commit} -> {resolved}")
    if subprocess.check_output(["git", "-C", str(SOURCE), "rev-parse", f"{SOURCE_COMMIT}^"], text=True).strip() != INITIAL_SOURCE_COMMIT:
        raise SystemExit("corrected source parent drift")
    if subprocess.check_output(["git", "-C", str(SOURCE), "rev-parse", f"{CERTIFICATE_COMMIT}^"], text=True).strip() != SOURCE_COMMIT:
        raise SystemExit("certificate parent drift")
    if subprocess.check_output(["git", "-C", str(SOURCE), "rev-parse", f"{HANDOFF_COMMIT}^"], text=True).strip() != CERTIFICATE_COMMIT:
        raise SystemExit("handoff parent drift")
    handoff = git_bytes(HANDOFF_COMMIT, HANDOFF_PATH)
    audit = git_bytes(HANDOFF_COMMIT, HANDOFF_AUDIT_PATH)
    if sha256(handoff) != HANDOFF_SHA256 or sha256(audit) != HANDOFF_AUDIT_SHA256:
        raise SystemExit("handoff or independent-audit drift")
    rows = re.findall(rb"\| `([0-9a-f]{64})` \| `([^`]+)` \|", handoff)
    parsed = {path.decode(): digest.decode() for digest, path in rows}
    if parsed != FROZEN or len(parsed) != 24:
        raise SystemExit(f"handoff whitelist drift: {len(parsed)} entries")
    certificate_paths = set(subprocess.check_output(
        ["git", "-C", str(SOURCE), "diff", "--name-only", PREDECESSOR_HANDOFF_COMMIT, CERTIFICATE_COMMIT], text=True
    ).split())
    expected_certificate_paths = set(FROZEN) - {f"{FIGURE_SOURCE_PREFIX}manifest.json"}
    if certificate_paths != expected_certificate_paths:
        raise SystemExit("cumulative certificate changed-path whitelist drift")
    for relative, expected in FROZEN.items():
        commit = HANDOFF_COMMIT if relative.endswith("/manifest.json") else CERTIFICATE_COMMIT
        data = git_bytes(commit, relative)
        write_exact(relative, data, expected)
        if relative.startswith(FIGURE_SOURCE_PREFIX):
            name = relative.removeprefix(FIGURE_SOURCE_PREFIX)
            for mirror in (
                f"research/figures/r076l/{FIGURE_ID}/{name}",
                f"public/figures/r076l/{FIGURE_ID}/{name}",
            ):
                write_exact(mirror, data, expected)
            if name in {"figure.svg", "figure.png", "figure.pdf"}:
                extension = name.rsplit(".", 1)[1]
                write_exact(f"public/assets/r076l/{FIGURE_ID}.{extension}", data, expected)
    archive = ROOT / f"research/figures/r076l/{FIGURE_ID}"
    if len([path for path in archive.iterdir() if path.is_file()]) != 12:
        raise SystemExit("figure file-count drift")
    if sum(path.stat().st_size for path in archive.iterdir() if path.is_file()) != FIGURE_BYTES:
        raise SystemExit("figure byte-count drift")
    ledger = {
        "schemaVersion": "r076l-step63-frozen-ledger-v1",
        "release": "R0.76L",
        "step": 63,
        "sourceCommit": SOURCE_COMMIT,
        "certificateCommit": CERTIFICATE_COMMIT,
        "handoffCommit": HANDOFF_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "handoffIndependentAuditSha256": HANDOFF_AUDIT_SHA256,
        "fileCount": len(FROZEN),
        "files": [{"path": path, "sha256": digest} for path, digest in sorted(FROZEN.items())],
    }
    ledger_path = ROOT / "research/r076l_frozen_ledger.json"
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    print({
        "status": "PASS", "release": "R0.76L Step 63", "source": SOURCE_COMMIT,
        "certificateCommit": CERTIFICATE_COMMIT, "handoffCommit": HANDOFF_COMMIT,
        "handoffSha256": HANDOFF_SHA256, "handoffIndependentAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN), "formalFigureRequired": True, "figureFiles": len(FIGURE_NAMES),
        "figureBytes": FIGURE_BYTES, "recapRequired": False,
        "portableLedger": str(ledger_path.relative_to(ROOT)),
    })


if __name__ == "__main__":
    main()
