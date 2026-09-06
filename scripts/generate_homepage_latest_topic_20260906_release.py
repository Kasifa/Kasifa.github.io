#!/usr/bin/env python3
"""Apply and validate the one-latest-independent-topic homepage policy."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECK_ONLY = "--check-only" in sys.argv[1:]
VERSION = "2.48"
LATEST_HREF = "/notes/clay-b-plateau-history-20260906.html"
HISTORICAL_HREFS = (
    "/notes/clay-b-two-scale-20260905.html",
    "/notes/clay-b-signed-scale-20260905.html",
    "/notes/clay-b-physical-adjoint-20260906.html",
    "/notes/clay-b-window-localisation-20260906.html",
)
SPOTLIGHT = re.compile(
    r'^[ \t]*<section class="route-overview independent-release-spotlight"[\s\S]*?</section>[ \t]*(?:\n|$)',
    re.MULTILINE,
)


def replace_once(value: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, value)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return updated


def set_page_version(value: str, footer_label: str, *, site_refresh: bool) -> str:
    value = replace_once(value, r'data-site-version="\d+\.\d+"', f'data-site-version="{VERSION}"', "data version")
    value = replace_once(value, r'/i18n-en\.js\?v=\d+\.\d+', f'/i18n-en.js?v={VERSION}', "i18n version")
    if site_refresh:
        value = replace_once(value, r'/site-refresh\.js\?v=\d+\.\d+', f'/site-refresh.js?v={VERSION}', "refresh version")
    value = replace_once(value, rf'(?<!上次){re.escape(footer_label)} v\d+\.\d+ ·', f'{footer_label} v{VERSION} ·', "footer version")
    return value


def normalize_home(value: str) -> tuple[str, int]:
    matches = list(SPOTLIGHT.finditer(value))
    latest = [match for match in matches if LATEST_HREF in match.group(0)]
    if len(latest) != 1:
        raise RuntimeError(f"latest independent spotlight count is {len(latest)}")
    removed = 0

    def keep_latest(match: re.Match[str]) -> str:
        nonlocal removed
        if LATEST_HREF in match.group(0):
            return match.group(0)
        removed += 1
        return ""

    value = SPOTLIGHT.sub(keep_latest, value)
    value = set_page_version(value, "综述", site_refresh=True)
    value = replace_once(value, r'<strong>v\d+\.\d+</strong>网页版本', f'<strong>v{VERSION}</strong>网页版本', "status version")
    return value, removed


def update_json(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


home_path = ROOT / "public/research-review.html"
literature_path = ROOT / "public/literature-review.html"
note_path = ROOT / "public/notes/clay-b-plateau-history-20260906.html"
home_before = home_path.read_text(encoding="utf-8")
home_after, removed = normalize_home(home_before)

if not CHECK_ONLY:
    home_path.write_text(home_after, encoding="utf-8")
    literature = set_page_version(
        literature_path.read_text(encoding="utf-8"), "文献综述", site_refresh=False
    )
    literature_path.write_text(literature, encoding="utf-8")
    note = note_path.read_text(encoding="utf-8")
    note = replace_once(note, r'data-site-version="\d+\.\d+"', f'data-site-version="{VERSION}"', "note data version")
    note = replace_once(note, r'/i18n-en\.js\?v=\d+\.\d+', f'/i18n-en.js?v={VERSION}', "note i18n version")
    note_path.write_text(note, encoding="utf-8")
    (ROOT / "VERSION").write_text(VERSION + "\n", encoding="utf-8")
    update_json(ROOT / "public/site-version.json")
    update_json(ROOT / "research/release-manifest.json")
    subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
else:
    if home_after != home_before or removed != 0:
        raise RuntimeError("homepage is not normalized to the latest independent topic")

home = home_path.read_text(encoding="utf-8")
spotlights = SPOTLIGHT.findall(home)
if len(spotlights) != 1 or LATEST_HREF not in spotlights[0]:
    raise RuntimeError("homepage must contain exactly the latest independent spotlight")
for href in HISTORICAL_HREFS:
    if href not in home:
        raise RuntimeError(f"historical roadmap link missing: {href}")
for path in [home_path, literature_path, note_path, ROOT / "public/notes/index.html"]:
    text = path.read_text(encoding="utf-8")
    if f'v={VERSION}' not in text:
        raise RuntimeError(f"{path.relative_to(ROOT)} cache version drift")
site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
if (ROOT / "VERSION").read_text(encoding="utf-8").strip() != VERSION:
    raise RuntimeError("VERSION drift")
if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION:
    raise RuntimeError("site metadata version drift")
if site.get("latestIndependentResearchHtml") != LATEST_HREF:
    raise RuntimeError("latest independent note drift")

print(json.dumps({
    "schemaVersion": "homepage-latest-independent-topic-generation-v1",
    "releaseId": "Homepage-LatestTopic-20260906",
    "status": "PASS",
    "mode": "check-only" if CHECK_ONLY else "apply",
    "siteVersion": VERSION,
    "spotlightCount": 1,
    "removedSpotlights": removed,
    "historicalRoadmapLinks": "PRESERVED",
}, ensure_ascii=False))
