#!/usr/bin/env python3
"""Materialize and validate the ClayB WindowLocalisation HTML-only release."""

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
    "public/notes/clay-b-window-localisation-20260906.html",
    [
        "ClayB-WindowLocalisation-20260906",
        "短窗口的局部耗散与压力余项",
        "Local dissipation and pressure remainders on short windows",
        "U.1–U.9",
        "V.1–V.12",
        "W.1–W.6",
        "W.7–W.10",
        "W.11–W.14",
        "negative cutoff correction",
        "doubled-radius dissipation ledger",
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
        'class="tree-row clay-b-window-localisation-row"',
        "从正变差窗口到扩大域耗散债务",
        "首次奇点量词复评",
        "/notes/clay-b-window-localisation-20260906.html",
    ],
)
require_text(
    "public/literature-review.html",
    [
        'id="clay-b-window-localisation-boundary"',
        "ClayB-WindowLocalisation-20260906 公开边界",
    ],
)
require_text(
    "public/notes/index.html",
    [
        'data-note="clay-b-window-localisation-20260906"',
        "按政策不生成 PDF",
        "4 NOTES",
    ],
)

site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
if site.get("version") != "2.46" or site.get("latestRelease") != "R0.76L":
    raise RuntimeError("site version or canonical endpoint drift")
if site.get("latestIndependentNote") != "ClayB-WindowLocalisation-20260906":
    raise RuntimeError("latest independent note drift")
if site.get("latestIndependentResearchPdf") is not None:
    raise RuntimeError("HTML-only release must keep latestIndependentResearchPdf null")
if manifest.get("latestPublication", {}).get("releaseId") != "clay-b-window-localisation-20260906":
    raise RuntimeError("release manifest latestPublication drift")
if (ROOT / "public/notes/clay-b-window-localisation-20260906.pdf").exists():
    raise RuntimeError("new WindowLocalisation PDF must remain absent")

print(json.dumps({
    "schemaVersion": "clay-b-window-localisation-generation-v1",
    "releaseId": "ClayB-WindowLocalisation-20260906",
    "status": "PASS",
    "mode": "check-only" if CHECK_ONLY else "apply",
    "readerPdf": "OMIT_NEW",
    "canonicalR0Endpoint": "R0.76L",
    "homepageRoadmap": "MERGED_U_V_W",
}, ensure_ascii=False))
