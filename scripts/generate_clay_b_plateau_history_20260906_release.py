#!/usr/bin/env python3
"""Materialize and validate the ClayB PlateauHistory HTML-only release."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECK_ONLY = "--check-only" in sys.argv[1:]


def require_text(path: str, markers: list[str]) -> None:
    text = (ROOT / path).read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            raise RuntimeError(f"{path} is missing {marker!r}")


if not CHECK_ONLY:
    subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)

require_text(
    "public/notes/clay-b-plateau-history-20260906.html",
    [
        "ClayB-PlateauHistory-20260906",
        "平台时间内能量历史的准确代价",
        "The exact cost of energy history inside the plateau",
        "X.1–X.4",
        "Y.1–Y.2",
        "Y.3–Y.8",
        "Y.9",
        "Y.10–Y.12",
        "total dissipation",
        "right-hand side may be nonpositive",
        "A+P",
        "not the target A+Z",
        "PROVED LOCALLY",
        "CONDITIONAL",
        "FINITE: NONE",
        "OPEN",
        "NOT CLAY",
    ],
)
require_text(
    "public/research-review.html",
    [
        'class="tree-row clay-b-plateau-history-row"',
        "从平台终点归约到 A+P 历史成本",
        "首次奇点文献适用性核查",
        "/notes/clay-b-plateau-history-20260906.html",
    ],
)
require_text(
    "public/literature-review.html",
    ['id="clay-b-plateau-history-boundary"', "ClayB-PlateauHistory-20260906 公开边界"],
)
require_text(
    "public/notes/index.html",
    ['data-note="clay-b-plateau-history-20260906"', "按政策不生成 PDF", "5 NOTES"],
)

site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
if site.get("version") != "2.47" or site.get("latestRelease") != "R0.76L":
    raise RuntimeError("site version or canonical endpoint drift")
if site.get("latestIndependentNote") != "ClayB-PlateauHistory-20260906":
    raise RuntimeError("latest independent note drift")
if site.get("latestIndependentResearchPdf") is not None:
    raise RuntimeError("HTML-only release must keep latestIndependentResearchPdf null")
if manifest.get("latestPublication", {}).get("releaseId") != "clay-b-plateau-history-20260906":
    raise RuntimeError("release manifest latestPublication drift")
if (ROOT / "public/notes/clay-b-plateau-history-20260906.pdf").exists():
    raise RuntimeError("new PlateauHistory PDF must remain absent")

print(json.dumps({
    "schemaVersion": "clay-b-plateau-history-generation-v1",
    "releaseId": "ClayB-PlateauHistory-20260906",
    "status": "PASS",
    "mode": "check-only" if CHECK_ONLY else "apply",
    "readerPdf": "OMIT_NEW",
    "canonicalR0Endpoint": "R0.76L",
    "homepageRoadmap": "MERGED_X_Y",
}, ensure_ascii=False))
