#!/usr/bin/env python3
"""Build the reviewed R0.74A Chinese-report to English translation map.

The Chinese and frozen English reports share the same Markdown structure and
the same 52 display equations.  This tool renders both through the production
note renderer, aligns their reader-facing text nodes, and records only nodes
that contain Chinese.  It never changes mathematical claims or source data.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

from generate_r074a_release import NOTE, REPORT, REPORT_ZH, note_html


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "research/r074a_full_zh_translation_map.json"
CHINESE_RE = re.compile(r"[\u3400-\u9fff\uf900-\ufaff]")
TAG_RE = re.compile(r"(<!--[\s\S]*?-->|<![^>]*>|</?[A-Za-z][^>]*>)")
PROTECTED_PATTERNS = (
    re.compile(r"\\\([\s\S]*?\\\)"),
    re.compile(r"\\\[[\s\S]*?\\\]"),
    re.compile(r"https?://[^\s<]+"),
)

MANUAL_ENGLISH = {
    **{f"{number:02d} / 规范报告": f"{number:02d} / canonical report" for number in range(1, 7)},
    "F / 论文图": "F / Journal figure",
    "B / 结论边界": "B / Exact claim boundary",
    "R / 复现材料": "R / Reproduction materials",
    "英文规范源文": "Canonical English source",
    "中文完整译文": "Complete Chinese translation",
    "所以": "Therefore,",
    (
        "本笔记只新引入 \\(\\mathcal U_{\\rm ext}^{\\infty,\\square}\\)。"
        "下文继续使用 \\(\\mathcal D_{\\rm ext}^{\\square}\\) 的记号。"
    ): (
        "Only \\(\\mathcal U_{\\rm ext}^{\\infty,\\square}\\) is newly introduced in this note. "
        "The notation \\(\\mathcal D_{\\rm ext}^{\\square}\\) is used from now on."
    ),
}


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def reader_text_nodes(document: str) -> list[str]:
    article = document.split("<article>", 1)[1].split('<section id="figure">', 1)[0]
    output: list[str] = []
    skipped: str | None = None
    for part in TAG_RE.split(article):
        if not part:
            continue
        if part.startswith("<"):
            closing = re.match(r"^</\s*([a-z0-9-]+)", part, re.I)
            if closing and closing.group(1).lower() == skipped:
                skipped = None
                continue
            if skipped:
                continue
            opening = re.match(r"^<\s*([a-z0-9-]+)", part, re.I)
            if opening and opening.group(1).lower() in {"script", "style", "noscript"}:
                skipped = opening.group(1).lower()
            continue
        if skipped:
            continue
        value = normalize(part)
        if value:
            output.append(value)
    return output


def protected(value: str) -> list[str]:
    output: list[str] = []
    for pattern in PROTECTED_PATTERNS:
        output.extend(pattern.findall(value))
    return output


def build_map() -> list[dict[str, object]]:
    chinese = reader_text_nodes(note_html(REPORT_ZH.read_text(encoding="utf-8")))
    english = reader_text_nodes(note_html(REPORT.read_text(encoding="utf-8")))
    if len(chinese) != len(english):
        raise RuntimeError(f"R0.74A bilingual report node-count drift: {len(chinese)} != {len(english)}")

    rows: list[dict[str, object]] = []
    for index, (zh, en) in enumerate(zip(chinese, english), 1):
        if not CHINESE_RE.search(zh):
            continue
        en = MANUAL_ENGLISH.get(zh, en)
        if CHINESE_RE.search(en):
            raise RuntimeError(f"English node {index} still contains Chinese: {en}")
        if protected(zh) != protected(en):
            raise RuntimeError(f"protected-token drift at bilingual report node {index}: {zh}")
        rows.append({
            "zh": zh,
            "en": en,
            "count": 1,
            "files": [str(NOTE.relative_to(ROOT))],
            "provenance": "local-direct-structural-alignment-reviewed",
        })

    existing = {row["zh"] for row in rows}
    for zh, en in MANUAL_ENGLISH.items():
        if zh not in existing:
            rows.append({
                "zh": zh,
                "en": en,
                "count": 1,
                "files": [str(NOTE.relative_to(ROOT))],
                "provenance": "local-direct-manual-interface-label",
            })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    value = build_map()
    serialized = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if args.check_only:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != serialized:
            raise RuntimeError("R0.74A full Chinese translation map is stale")
    else:
        OUTPUT.write_text(serialized, encoding="utf-8")
    print(json.dumps({"checked": True, "rows": len(value), "output": str(OUTPUT.relative_to(ROOT))}))


if __name__ == "__main__":
    main()
