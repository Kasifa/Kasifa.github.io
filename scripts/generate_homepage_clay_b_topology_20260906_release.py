#!/usr/bin/env python3
"""Normalize and validate the R0/Clay-B split-roadmap maintenance release."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECK_ONLY = "--check-only" in sys.argv[1:]
VERSION = "2.50"
RELEASE_ID = "Homepage-ClayB-Topology-20260906"
CHAPTERS = {
    "clay-b-two-scale-20260905": "CB.1",
    "clay-b-signed-scale-20260905": "CB.2",
    "clay-b-physical-adjoint-20260906": "CB.3",
    "clay-b-window-localisation-20260906": "CB.4",
    "clay-b-plateau-history-20260906": "CB.5",
    "clay-b-concentration-limits-20260906": "CB.6",
}
LITERATURE_HEADINGS = {
    "clay-b-two-scale-boundary": ("CB.1", "Clay-B 两尺度差能量的 filtering 文献与主张边界", "ClayB-TwoScale-20260905"),
    "clay-b-signed-scale-boundary": ("CB.2", "Clay-B 有符号尺度预算的 filtering 文献与主张边界", "ClayB-SignedScale-20260905"),
    "clay-b-physical-adjoint-boundary": ("CB.3", "Clay-B 物理时间伴随测试的文献与主张边界", "ClayB-PhysicalAdjoint-20260906"),
    "clay-b-window-localisation-boundary": ("CB.4", "Clay-B 短窗口局部耗散的文献与主张边界", "ClayB-WindowLocalisation-20260906"),
    "clay-b-plateau-history-boundary": ("CB.5", "Clay-B 平台时间能量历史的文献与主张边界", "ClayB-PlateauHistory-20260906"),
    "clay-b-concentration-limits-boundary": ("CB.6", "Clay-B 固定球集中、原路径与持留成本的文献和主张边界", "ClayB-ConcentrationLimits-20260906"),
}


def set_version(value: str, *, refresh: bool = False) -> str:
    value = re.sub(r'data-site-version="\d+\.\d+"', f'data-site-version="{VERSION}"', value, count=1)
    value = re.sub(r'/i18n-en\.js\?v=\d+\.\d+', f'/i18n-en.js?v={VERSION}', value, count=1)
    if refresh:
        value = re.sub(r'/site-refresh\.js\?v=\d+\.\d+', f'/site-refresh.js?v={VERSION}', value, count=1)
    return value


def normalize_literature(value: str) -> str:
    value = set_version(value)
    for anchor, (chapter, title, release_id) in LITERATURE_HEADINGS.items():
        bare_heading = f'<h3 id="{anchor}">{title}</h3>'
        numbered_heading = f'<h3 id="{anchor}">{chapter} · {title}</h3>'
        if bare_heading in value:
            value = value.replace(bare_heading, numbered_heading, 1)
        elif numbered_heading not in value:
            raise RuntimeError(f"literature heading drift: {anchor}")
        bare_boundary = f'<strong>{release_id} 公开边界</strong>'
        numbered_boundary = f'<strong>{chapter} · {release_id} 公开边界</strong>'
        if bare_boundary in value:
            value = value.replace(bare_boundary, numbered_boundary, 1)
        elif numbered_boundary not in value:
            raise RuntimeError(f"literature boundary drift: {release_id}")

    lines = value.splitlines(keepends=True)
    indices = []
    rows = []
    for anchor in LITERATURE_HEADINGS:
        matches = [index for index, line in enumerate(lines) if f'id="{anchor}"' in line]
        if len(matches) != 1:
            raise RuntimeError(f"literature chapter line count drift: {anchor}")
        indices.append(matches[0])
        rows.append(lines[matches[0]])
    insertion = min(indices)
    for index in sorted(indices, reverse=True):
        del lines[index]
    lines[insertion:insertion] = rows
    return "".join(lines)


def update_json(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload["independentChapterScheme"] = "CB.n"
    payload["latestIndependentChapter"] = "CB.6"
    payload["nextIndependentChapter"] = "CB.7"
    if path.name == "release-manifest.json":
        payload["latestPublication"]["chapter"] = "CB.6"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate() -> None:
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    required_home = [
        'class="route-tree r0-route-tree"',
        'class="route-lane-divider"',
        'class="route-tree clay-b-route-tree"',
        "border-left-style: dashed",
        "不声明由 R0.76L 直接推出",
        "R0 主序列停在 R0.76L",
        "Clay-B 独立路线停在 CB.6",
    ]
    for marker in required_home:
        if marker not in home:
            raise RuntimeError(f"homepage topology marker missing: {marker}")
    if home.index('class="route-tree r0-route-tree"') >= home.index('class="route-tree clay-b-route-tree"'):
        raise RuntimeError("R0 and Clay-B lane order drift")
    chapter_positions = []
    for slug, chapter in CHAPTERS.items():
        row_marker = f'class="tree-row {slug.removesuffix("-20260905").removesuffix("-20260906")}-row"'
        if row_marker not in home:
            raise RuntimeError(f"homepage chapter row missing: {row_marker}")
        row_position = home.index(row_marker)
        chapter_positions.append(row_position)
        if home.find(chapter, row_position, row_position + 850) < 0:
            raise RuntimeError(f"homepage chapter label missing near {slug}: {chapter}")
        note = (ROOT / f"public/notes/{slug}.html").read_text(encoding="utf-8")
        if chapter not in note:
            raise RuntimeError(f"note chapter label missing: {slug}")
        if f'data-site-version="{VERSION}"' not in note or f'/i18n-en.js?v={VERSION}' not in note:
            raise RuntimeError(f"note version drift: {slug}")
    if chapter_positions != sorted(chapter_positions):
        raise RuntimeError("Clay-B chapter order drift")
    if (home.count('class="route-overview independent-release-spotlight"') != 1 or
            "/notes/clay-b-concentration-limits-20260906.html" not in home):
        raise RuntimeError("latest independent spotlight policy drift")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    for anchor, (chapter, _, release_id) in LITERATURE_HEADINGS.items():
        if f'id="{anchor}">{chapter} ·' not in literature:
            raise RuntimeError(f"literature heading number missing: {chapter}")
        if f'<strong>{chapter} · {release_id} 公开边界</strong>' not in literature:
            raise RuntimeError(f"literature boundary number missing: {chapter}")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    for slug, chapter in CHAPTERS.items():
        if not re.search(rf'data-note="{re.escape(slug)}"[\s\S]*?class="note-code">{re.escape(chapter)} ·', index):
            raise RuntimeError(f"index chapter number missing: {chapter}")
    if (ROOT / "VERSION").read_text(encoding="utf-8").strip() != VERSION:
        raise RuntimeError("VERSION drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    for payload in (site, manifest):
        if payload.get("version", payload.get("siteVersion")) != VERSION:
            raise RuntimeError("site metadata version drift")
        if payload.get("latestIndependentChapter") != "CB.6" or payload.get("nextIndependentChapter") != "CB.7":
            raise RuntimeError("independent chapter metadata drift")


if not CHECK_ONLY:
    home_path = ROOT / "public/research-review.html"
    home = set_version(home_path.read_text(encoding="utf-8"), refresh=True)
    home = re.sub(r'<strong>v\d+\.\d+</strong>网页版本', f'<strong>v{VERSION}</strong>网页版本', home, count=1)
    home = re.sub(r'(?<!上次)综述 v\d+\.\d+ ·', f'综述 v{VERSION} ·', home, count=1)
    home_path.write_text(home, encoding="utf-8")

    literature_path = ROOT / "public/literature-review.html"
    literature = normalize_literature(literature_path.read_text(encoding="utf-8"))
    literature = re.sub(r'(?<!上次)文献综述 v\d+\.\d+ ·', f'文献综述 v{VERSION} ·', literature, count=1)
    literature_path.write_text(literature, encoding="utf-8")

    for slug in CHAPTERS:
        path = ROOT / f"public/notes/{slug}.html"
        path.write_text(set_version(path.read_text(encoding="utf-8")), encoding="utf-8")

    (ROOT / "VERSION").write_text(VERSION + "\n", encoding="utf-8")
    update_json(ROOT / "public/site-version.json")
    update_json(ROOT / "research/release-manifest.json")
    subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)

validate()
print(json.dumps({
    "schemaVersion": "homepage-clay-b-topology-generation-v1",
    "releaseId": RELEASE_ID,
    "status": "PASS",
    "mode": "check-only" if CHECK_ONLY else "apply",
    "siteVersion": VERSION,
    "r0Lane": "SOLID",
    "clayBLane": "DASHED",
    "chapters": list(CHAPTERS.values()),
    "newReaderPdf": "OMITTED",
}, ensure_ascii=False))
