#!/usr/bin/env python3
"""Materialize and validate the ClayB PhysicalAdjoint HTML-only release."""

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
    subprocess.run(
        [sys.executable, "scripts/generate_note_index.py"],
        cwd=ROOT,
        check=True,
    )

require_text(
    "public/notes/clay-b-physical-adjoint-20260906.html",
    [
        "ClayB-PhysicalAdjoint-20260906",
        "伴随测试的定位代价",
        "The localization cost of an adjoint test",
        "B.1–B.5",
        "B.6–B.13",
        "B.14–B.16",
        "C.1–C.6",
        "PROVED LOCALLY",
        "FINITE: NONE",
        "OPEN",
        "NOT CLAY",
    ],
)
require_text(
    "public/research-review.html",
    [
        'class="tree-row clay-b-physical-adjoint-row"',
        "有符号尺度相消 → 放弃零失配热对偶 → 真实时间伴随弱端点",
        "原计时合同的持留/上穿控制",
        "/notes/clay-b-physical-adjoint-20260906.html",
    ],
)
require_text(
    "public/literature-review.html",
    [
        'id="clay-b-physical-adjoint-boundary"',
        "ClayB-PhysicalAdjoint-20260906 公开边界",
    ],
)
require_text(
    "public/notes/index.html",
    [
        'data-note="clay-b-physical-adjoint-20260906"',
        "按政策不生成 PDF",
        "3 NOTES",
    ],
)

site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
if site.get("version") != "2.45" or site.get("latestRelease") != "R0.76L":
    raise RuntimeError("site version or canonical endpoint drift")
if site.get("latestIndependentNote") != "ClayB-PhysicalAdjoint-20260906":
    raise RuntimeError("latest independent note drift")
if site.get("latestIndependentResearchPdf") is not None:
    raise RuntimeError("HTML-only release must keep latestIndependentResearchPdf null")
if manifest.get("latestPublication", {}).get("releaseId") != "clay-b-physical-adjoint-20260906":
    raise RuntimeError("release manifest latestPublication drift")
if (ROOT / "public/notes/clay-b-physical-adjoint-20260906.pdf").exists():
    raise RuntimeError("new PhysicalAdjoint PDF must remain absent")

print(json.dumps({
    "schemaVersion": "clay-b-physical-adjoint-generation-v1",
    "releaseId": "ClayB-PhysicalAdjoint-20260906",
    "status": "PASS",
    "mode": "check-only" if CHECK_ONLY else "apply",
    "readerPdf": "OMIT_NEW",
    "canonicalR0Endpoint": "R0.76L",
}, ensure_ascii=False))
