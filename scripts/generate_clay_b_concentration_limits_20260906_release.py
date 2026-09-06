#!/usr/bin/env python3
"""Materialize and validate the ClayB ConcentrationLimits HTML-only release."""

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
    "public/notes/clay-b-concentration-limits-20260906.html",
    [
        "ClayB-ConcentrationLimits-20260906",
        "固定球集中之后，还缺少什么",
        "What remains after fixed-ball concentration",
        "LITERATURE CONDITIONAL",
        "typographical interpretation",
        "solution-dependent",
        "not an NS",
        "growing initial energy",
        "t_B/r²→0",
        "bare far-source pressure impulse",
        "not velocity-weighted pressure work",
        "AA.18",
        "FINITE: NONE",
        "OPEN",
        "NOT CLAY",
    ],
)
require_text(
    "public/research-review.html",
    [
        'class="route-overview independent-release-spotlight"',
        'id="clay-b-concentration-limits"',
        'class="tree-row clay-b-concentration-limits-row"',
        "从固定球集中到局部持留的准确缺口",
        "解依赖慢对角半径",
        "裸远源压力冲量",
        "近源压力与黏性 OPEN",
        "/notes/clay-b-concentration-limits-20260906.html",
        "/notes/clay-b-plateau-history-20260906.html",
    ],
)
home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
if home.count('class="route-overview independent-release-spotlight"') != 1:
    raise RuntimeError("homepage must retain exactly one independent topic spotlight")
if '<article class="tree-node current">' not in home[home.index('class="tree-row clay-b-concentration-limits-row"'):]:
    raise RuntimeError("latest independent roadmap row must be current")
require_text(
    "public/literature-review.html",
    [
        'id="clay-b-concentration-limits-boundary"',
        "ClayB-ConcentrationLimits-20260906 公开边界",
        "不是作者发布的勘误",
        "AA.18 不是速度加权压力功",
    ],
)
require_text(
    "public/notes/index.html",
    [
        'data-note="clay-b-concentration-limits-20260906"',
        "按政策不生成 PDF",
        "6 NOTES",
    ],
)

site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
if site.get("version") != "2.49" or site.get("latestRelease") != "R0.76L":
    raise RuntimeError("site version or canonical endpoint drift")
if site.get("publicIndependentNoteCount") != 6:
    raise RuntimeError("independent note count drift")
if site.get("latestIndependentNote") != "ClayB-ConcentrationLimits-20260906":
    raise RuntimeError("latest independent note drift")
if site.get("latestIndependentResearchPdf") is not None:
    raise RuntimeError("HTML-only release must keep latestIndependentResearchPdf null")
if manifest.get("latestPublication", {}).get("releaseId") != "clay-b-concentration-limits-20260906":
    raise RuntimeError("release manifest latestPublication drift")
if (ROOT / "public/notes/clay-b-concentration-limits-20260906.pdf").exists():
    raise RuntimeError("new ConcentrationLimits PDF must remain absent")

print(json.dumps({
    "schemaVersion": "clay-b-concentration-limits-generation-v1",
    "releaseId": "ClayB-ConcentrationLimits-20260906",
    "status": "PASS",
    "mode": "check-only" if CHECK_ONLY else "apply",
    "readerPdf": "OMIT_NEW",
    "canonicalR0Endpoint": "R0.76L",
    "homepageRoadmap": "MERGED_L_P_D_I_M_N_AA",
    "independentSpotlightCount": 1,
}, ensure_ascii=False))

