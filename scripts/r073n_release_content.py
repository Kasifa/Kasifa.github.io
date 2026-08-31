#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Canonical-source reader and UI fragments for the fail-closed R0.73N release.

Mathematical prose is read from the frozen report source and release ledgers.
This module owns only the small, retro HTML shell.  It deliberately refuses
to synthesize substitute claims when a canonical source is absent.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import html
import json
import os
from pathlib import Path
import re
import unicodedata


RELEASE = "R0.73N"
RELEASE_SLUG = "r073n"
SITE_VERSION = "1.54"
FIGURE_ID = "fig-r073n-finite-strain-bracket"
FIGURE_SOURCE_RELATIVE = f"research/figures/r073n/{FIGURE_ID}"
FIGURE_ARCHIVE_RELATIVE = f"figures/r073n/{FIGURE_ID}"

R073M_BASELINE = {
    "latestCompletedRelease": "r073m",
    "siteVersion": "1.53",
    "publicHtmlNoteCount": 189,
    "postR060RecapNodeCount": 129,
    "nextRelease": "r073n",
    "postR070APublishedReleaseCount": 91,
    "postR070AFormalSealedReleaseCount": 67,
    "legacyFormalFigureBacklogCount": 24,
}

R073N_TARGET = {
    "latestCompletedRelease": "r073n",
    "siteVersion": SITE_VERSION,
    "publicHtmlNoteCount": 190,
    "postR060RecapNodeCount": 130,
    "nextRelease": "r073o",
    "postR070APublishedReleaseCount": 92,
    "postR070AFormalSealedReleaseCount": 68,
    "legacyFormalFigureBacklogCount": 24,
}

CANONICAL_SOURCE_PATHS = (
    "research/r073n_problem_freeze.md",
    "research/r073n_fixed_background_no_go_proof.md",
    "research/r073n_scaling_obstruction.md",
    "research/r073n_independent_analytic_audit.md",
    "research/r073n_adversarial_audit.md",
    "research/r073n_literature_audit.md",
    "research/r073n_claim_source_ledger.md",
    "research/r073n_gap_matrix.md",
    "research/r073n_finite_diagnostic_audit.md",
    "research/r073n_report-source.md",
    "research/r073n_bilingual_dictionary.md",
)

REPORT_SOURCE = "research/r073n_report-source.md"
DICTIONARY_SOURCE = "research/r073n_bilingual_dictionary.md"

REQUIRED_BOUNDARY_TOKENS = (
    "fixedMemberThreeDimensionalH3SynchronizedStability=CLOSED",
    "fullThreeDimensionalH3InputL2Output=CLOSED_AS_COROLLARY",
    "fixedMemberPlanarL2SynchronizedStability=CLOSED",
    "fullThreeDimensionalFPSH3L2Stability=OPEN",
    "Clay=OPEN",
)

PUBLIC_VOICE_BANS = (
    "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计",
    "杀死错误想法", "颠覆性", "世界首个", "接近解决",
    "解决了千禧年", "证明了全局正则性", "原创性定理", "首次证明",
)


class CanonicalSourceError(RuntimeError):
    """A source contract is absent, ambiguous, or claim-unsafe."""


@dataclass(frozen=True)
class ReportSection:
    number: int
    title: str
    anchor: str
    markdown: str
    html: str


@dataclass(frozen=True)
class ReleaseContent:
    report_title: str
    public_title_zh: str
    release_title_en: str
    date: str
    status: str
    lead_zh: str
    home_zh: str
    recap_zh: str
    literature_zh: str
    next_release: str
    next_gate_zh: str
    sections: tuple[ReportSection, ...]
    closed_ledger: str
    finite_ledger: str
    open_ledger: str
    source_sha256: dict[str, str]

    @property
    def document_title_en(self) -> str:
        """Site/PDF title derived from the canonical ASCII ledger title."""
        return self.release_title_en.replace(" | ", "｜", 1)

    @property
    def math_next_gate_zh(self) -> str:
        """Keep the mathematical R0.73O gate, without the pre-deploy handoff."""
        marker = f"数学上的下一发布门是 {self.next_release}："
        if marker not in self.next_gate_zh:
            raise CanonicalSourceError("R0.73N mathematical next-gate marker drift")
        return self.next_gate_zh.split(marker, 1)[1].strip()

    @property
    def note_hero(self) -> str:
        return (
            '    <header class="hero"><div class="hero-inner">\n'
            '      <div><div class="eyebrow">研究笔记 R0.73N · '
            'FIXED-TRAJECTORY FINITE-STRAIN NO-GO</div>\n'
            f'        <h1>{html.escape(self.public_title_zh)}</h1>\n'
            f'        <p class="lead">{html.escape(self.lead_zh)}</p></div>\n'
            '      <div class="stamp"><span class="state">状态 · R0.73N 完成</span>'
            '<strong>Internal continuum theorem + claim-boundary audits</strong>'
            f'<p>版本 v0.73N · {html.escape(self.date)}</p>'
            '<p>full 3D synchronized (H3,H3)：INTERNAL THEOREM</p>'
            '<p>planar synchronized (H3pl,L2pl)：INTERNAL THEOREM</p>'
            '<p>full 3D FPS (H3,L2)：OPEN</p>'
            '<p>FINITE / FIGURE：separate gates</p><p>NOT CLAY</p></div>\n'
            '    </div></header>'
        )

    @property
    def note_article(self) -> str:
        body = "\n".join(
            (
                f'        <section id="{section.anchor}">'
                f'<div class="section-no">{section.number:02d} / canonical report</div>'
                f'<h2>{html.escape(section.title)}</h2>{section.html}</section>'
            )
            for section in self.sections
        )
        boundary = (
            '        <section id="release-boundary">'
            '<div class="section-no">B / Exact release boundary</div>'
            '<h2>固定成员、平面子系统与开放拓扑严格分列</h2>'
            f'<p>{html.escape(self.closed_ledger)}</p>'
            f'<p>{html.escape(self.finite_ledger)}</p>'
            f'<p>{html.escape(self.open_ledger)}</p>'
            '<p>有限诊断不承担连续证明权重；bounded search 不承担原创性或'
            '优先权声明。NOT CLAY。</p></section>'
        )
        figure = (
            '        <section id="figure"><div class="section-no">F / Journal figure</div>'
            '<h2>有限应变包络、累积系数与标记基点指数括号</h2>'
            f'<p><img src="/assets/r073n/{FIGURE_ID}.svg" '
            'alt="R0.73N finite-strain envelope, cumulative coefficient, and marked-basepoint exponent bracket"></p>'
            f'<p><a href="/assets/r073n/{FIGURE_ID}.pdf">下载矢量 PDF</a> · '
            f'<a href="/assets/r073n/{FIGURE_ID}.png">下载 600 dpi PNG</a> · '
            f'<a href="/assets/r073n/{FIGURE_ID}.svg">打开 SVG</a></p>'
            '<p>附图只呈现已经封存的有限诊断；不认证连续能量估计、固定成员稳定管、'
            '尖锐模量、全三维 FPS (H3,L2)、奇性或 Clay。</p></section>'
        )
        reproduction = (
            '        <section id="reproduce"><div class="section-no">R / Reproduction</div>'
            '<h2>报告、证明、审计、证书与附图入口</h2>'
            '<p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073n_report-source.md">canonical report source</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073n_fixed_background_no_go_proof.md">continuum proof</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073n_literature_audit.md">bounded literature audit</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/'
            'research/certificates/r073n">finite diagnostic package</a></p>'
            f'<p><a href="/assets/r073n/{FIGURE_ID}.pdf">journal figure PDF</a> · '
            '<a href="/notes/r0-73n.pdf">synchronized note PDF</a> · '
            '<a href="/recap-r0-61-r0-73n.html">130-node cumulative recap</a></p>'
            '</section>'
        )
        return (
            "      <article>\n" + body + "\n" + figure + "\n" + boundary
            + "\n" + reproduction + "\n      </article>"
        )

    @property
    def home_card(self) -> str:
        return (
            '          <div class="task-one" id="r073n" data-release="r073n" '
            'style="margin-top:2rem">\n'
            f'            <p class="eyebrow">研究笔记 R0.73N · {html.escape(self.date)}</p>'
            f'<h3>{html.escape(self.public_title_zh)}</h3>\n'
            f'            <p>{html.escape(self.home_zh)}</p>\n'
            f'            <p><strong>连续边界：</strong>{html.escape(self.closed_ledger)}</p>\n'
            f'            <p><strong>开放边界：</strong>{html.escape(self.open_ledger)}。'
            'NOT CLAY。</p>\n'
            '            <p><a href="/notes/r0-73n.html"><strong>阅读 R0.73N '
            '研究笔记 →</strong></a><br><a href="/notes/r0-73n.pdf">下载同步 PDF</a> · '
            f'<a href="/assets/r073n/{FIGURE_ID}.pdf">下载期刊附图 PDF</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073n_report-source.md">查看 canonical report</a> · '
            '<a href="/recap-r0-61-r0-73n.html">打开累计回顾</a></p>\n'
            f'            <p><strong style="color:var(--gold)">下一发布门（{html.escape(self.next_release)}）：</strong>'
            f'&nbsp;{html.escape(self.math_next_gate_zh)}</p>\n'
            '          </div>'
        )

    @property
    def latest_spotlight(self) -> str:
        return (
            '    <section class="route-overview latest-release-spotlight" '
            'id="latest-release" aria-labelledby="latest-release-title">\n'
            '      <div class="route-overview-inner"><header class="route-map-header">\n'
            f'        <div><p class="eyebrow">LATEST RELEASE · R0.73N · '
            f'{html.escape(self.date)}</p><h2 class="route-map-title" '
            f'id="latest-release-title">{html.escape(self.public_title_zh)}</h2>'
            f'<p class="route-map-intro">{html.escape(self.lead_zh)}</p></div>\n'
            '        <nav class="route-map-actions" aria-label="最新发布快捷入口">'
            '<a class="route-map-latest" href="/notes/r0-73n.pdf">阅读最新 R0.73N '
            '研究笔记 →</a><a href="/recap-r0-61-r0-73n.html">130 节累计回顾</a>'
            '<a href="/notes/">190 篇研究笔记总索引</a>'
            '<a href="#r073n">查看首页完整 R0.73N 卡片</a></nav>\n'
            '      </header><div class="route-legend" aria-label="最新发布计数">'
            '<span><i class="route-legend-mark kept" aria-hidden="true"></i>'
            'R0.70A–R0.73N · 92 节已公开</span>'
            '<span><i class="route-legend-mark kept" aria-hidden="true"></i>'
            '68 节完整封存</span><span><i class="route-legend-mark current" '
            'aria-hidden="true"></i>当前端点 R0.73N</span></div></div>\n'
            '    </section>'
        )

    @property
    def recap_phase(self) -> str:
        return (
            f'            <article class="phase"><h3>R0.73N · '
            f'{html.escape(self.release_title_en)}</h3>'
            f'<p>{html.escape(self.recap_zh)}</p>'
            f'<p>{html.escape(self.closed_ledger)}。{html.escape(self.finite_ledger)}。'
            f'{html.escape(self.open_ledger)}。NOT CLAY。</p>'
            '<div class="links"><a href="/notes/r0-73n.html">R0.73N</a>'
            f'<a href="/assets/r073n/{FIGURE_ID}.pdf">R0.73N 附图</a>'
            '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/'
            'research/certificates/r073n">R0.73N 有限诊断包</a></div></article>'
        )

    @property
    def literature_update(self) -> str:
        return (
            '<span class="route-r073n-deck-update">'
            + html.escape(self.literature_zh)
            + ' full-three-dimensional FPS (H3,L2)=OPEN；bounded search '
            '不承担首创性或优先权声明。</span>'
        )


def _regular_text(root: Path, relative: str) -> str:
    path = root / relative
    if not path.is_file() or path.is_symlink():
        raise CanonicalSourceError("missing regular canonical source: " + relative)
    try:
        value = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise CanonicalSourceError("canonical source is not UTF-8: " + relative) from exc
    if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", value):
        raise CanonicalSourceError("canonical source contains control characters: " + relative)
    return value


def _one(pattern: str, value: str, label: str, flags: int = 0) -> str:
    matches = re.findall(pattern, value, flags)
    if len(matches) != 1:
        raise CanonicalSourceError(f"{label}: expected one match, found {len(matches)}")
    found = matches[0]
    return found if isinstance(found, str) else found[0]


def _slug(title: str, used: set[str]) -> str:
    normalized = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-") or "section"
    base = value
    index = 2
    while value in used:
        value = f"{base}-{index}"
        index += 1
    used.add(value)
    return value


def _inline(value: str) -> str:
    output: list[str] = []
    cursor = 0
    token = re.compile(
        r"\[([^\]\n]+)\]\((https?://[^)\s]+)\)"
        r"|\*\*([^*\n]+)\*\*"
        r"|`([^`\n]+)`"
    )
    for match in token.finditer(value):
        output.append(html.escape(value[cursor:match.start()], quote=False))
        if match.group(1) is not None:
            output.append(
                f'<a href="{html.escape(match.group(2), quote=True)}">'
                f'{html.escape(match.group(1))}</a>'
            )
        elif match.group(3) is not None:
            output.append(f"<strong>{html.escape(match.group(3))}</strong>")
        else:
            output.append(f"<code>{html.escape(match.group(4))}</code>")
        cursor = match.end()
    output.append(html.escape(value[cursor:], quote=False))
    return "".join(output)


def _markdown_blocks(value: str) -> str:
    lines = value.strip().splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    bullets: list[str] = []
    ordered: list[str] = []
    quote_lines: list[str] = []
    table_lines: list[str] = []
    math_lines: list[str] = []
    in_math = False
    fence = chr(96) * 3
    in_fence = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            output.append("<p>" + _inline(" ".join(row.strip() for row in paragraph)) + "</p>")
            paragraph.clear()

    def flush_bullets() -> None:
        if bullets:
            output.append(
                '<ul class="report-list">'
                + "".join(f"<li>{_inline(row)}</li>" for row in bullets)
                + "</ul>"
            )
            bullets.clear()

    def flush_ordered() -> None:
        if ordered:
            output.append(
                '<ol class="report-list report-list-ordered">'
                + "".join(f"<li>{_inline(row)}</li>" for row in ordered)
                + "</ol>"
            )
            ordered.clear()

    def flush_quote() -> None:
        if quote_lines:
            quote = " ".join(row.strip() for row in quote_lines if row.strip())
            if not quote:
                raise CanonicalSourceError("empty blockquote in report source")
            output.append(f"<blockquote><p>{_inline(quote)}</p></blockquote>")
            quote_lines.clear()

    def table_cells(row: str) -> list[str]:
        stripped = row.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            raise CanonicalSourceError("malformed Markdown table row in report source")
        # A TeX norm such as ``\|u\|`` contains escaped pipes that belong to
        # the cell rather than to Markdown's column syntax.
        return [
            cell.strip()
            for cell in re.split(r"(?<!\\)\|", stripped[1:-1])
        ]

    def is_table_separator(cells: list[str]) -> bool:
        return bool(cells) and all(
            re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) is not None
            for cell in cells
        )

    def flush_table() -> None:
        if not table_lines:
            return
        rows = [table_cells(row) for row in table_lines]
        if len(rows) < 3:
            raise CanonicalSourceError(
                "Markdown table needs a header, separator, and body row"
            )
        width = len(rows[0])
        if width < 2 or any(len(row) != width for row in rows):
            raise CanonicalSourceError("Markdown table column-count mismatch")
        if not is_table_separator(rows[1]):
            raise CanonicalSourceError("Markdown table is missing its header separator")
        if any(is_table_separator(row) for row in rows[2:]):
            raise CanonicalSourceError("Markdown table has an unexpected separator row")
        header = "".join(
            f'<th scope="col">{_inline(cell)}</th>' for cell in rows[0]
        )
        body = "".join(
            "<tr>" + "".join(f"<td>{_inline(cell)}</td>" for cell in row) + "</tr>"
            for row in rows[2:]
        )
        output.append(
            '<div class="table-wrap"><table class="report-table">'
            f"<thead><tr>{header}</tr></thead><tbody>{body}</tbody></table></div>"
        )
        table_lines.clear()

    def flush_blocks() -> None:
        flush_paragraph()
        flush_bullets()
        flush_ordered()
        flush_quote()
        flush_table()

    for row in lines + [""]:
        stripped = row.strip()
        if stripped.startswith(fence):
            flush_blocks()
            if in_fence:
                output.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines.clear()
                in_fence = False
            else:
                in_fence = True
            continue
        if in_fence:
            code_lines.append(row)
            continue
        if stripped == r"\[":
            flush_blocks()
            in_math = True
            math_lines = [r"\["]
            continue
        if in_math:
            math_lines.append(row)
            if stripped == r"\]":
                output.append(
                    '<div class="equation result">' +
                    html.escape("\n".join(math_lines), quote=False) +
                    "</div>"
                )
                math_lines = []
                in_math = False
            continue
        if re.fullmatch(r"###\s+.+", stripped):
            flush_blocks()
            output.append(f"<h3>{_inline(stripped[4:].strip())}</h3>")
            continue
        if stripped.startswith("- "):
            flush_paragraph()
            flush_ordered()
            flush_quote()
            flush_table()
            bullets.append(stripped[2:].strip())
            continue
        ordered_match = re.match(r"^\d+\.\s+(.+)$", stripped)
        if ordered_match:
            flush_paragraph()
            flush_bullets()
            flush_quote()
            flush_table()
            ordered.append(ordered_match.group(1).strip())
            continue
        if bullets and row.startswith(("  ", "\t")):
            bullets[-1] += " " + stripped
            continue
        if ordered and row.startswith(("  ", "\t")):
            ordered[-1] += " " + stripped
            continue
        if stripped.startswith(">"):
            flush_paragraph()
            flush_bullets()
            flush_ordered()
            flush_table()
            quote_lines.append(stripped[1:].lstrip())
            continue
        if not stripped:
            flush_blocks()
            continue
        if stripped.startswith("|") or stripped.endswith("|"):
            if not (stripped.startswith("|") and stripped.endswith("|")):
                raise CanonicalSourceError("malformed Markdown table row in report source")
            flush_paragraph()
            flush_bullets()
            flush_ordered()
            flush_quote()
            table_lines.append(stripped)
            continue
        flush_bullets()
        flush_ordered()
        flush_quote()
        flush_table()
        paragraph.append(row)
    if in_fence or in_math:
        raise CanonicalSourceError("unterminated fenced or display-math block in report source")
    return "".join(output)


def _parse_sections(report: str) -> tuple[ReportSection, ...]:
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", report))
    if not matches:
        raise CanonicalSourceError("R0.73N report source has no level-two sections")
    sections: list[ReportSection] = []
    used: set[str] = set()
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(report)
        title = re.sub(r"^\d+(?:\.\d+)*\.\s*", "", match.group(1)).strip()
        markdown = report[match.end():end].strip()
        if not markdown:
            raise CanonicalSourceError("empty report section: " + title)
        sections.append(ReportSection(
            number=index,
            title=title,
            anchor=_slug(title, used),
            markdown=markdown,
            html=_markdown_blocks(markdown),
        ))
    return tuple(sections)


def _paragraph_under(report: str, heading_pattern: str, label: str) -> str:
    match = re.search(
        rf"(?ms)^##\s+{heading_pattern}\s*$\n(.*?)(?=^##\s+|\Z)",
        report,
    )
    if match is None:
        raise CanonicalSourceError("report source missing " + label)
    body = re.sub(r"(?ms)\\\[.*?\\\]", " ", match.group(1))
    paragraphs = [
        re.sub(r"\s+", " ", row).strip()
        for row in re.split(r"\n\s*\n", body)
        if row.strip() and not row.lstrip().startswith(("-", "|", "#"))
    ]
    if not paragraphs:
        raise CanonicalSourceError("report source has no prose under " + label)
    return paragraphs[0]


def _machine_ledgers(combined: str) -> tuple[str, str, str]:
    rows = re.findall(r"(?m)^[A-Za-z][A-Za-z0-9_]*(?:=[A-Z0-9_]+|=\d+)\s*$", combined)
    rows = list(dict.fromkeys(row.strip() for row in rows))
    closed = [row for row in rows if row.endswith(("=CLOSED", "=CLOSED_AS_COROLLARY"))]
    finite = [
        row for row in rows
        if re.match(r"(?:finite|sourceCommit|finalSeal|formalFigure|publicRelease)", row)
    ]
    opened = [row for row in rows if row.endswith(("=OPEN", "=FALSE", "=FALSE_AS_INFERENCE"))]
    if not closed or not opened:
        raise CanonicalSourceError("canonical sources do not expose closed/open machine ledgers")
    return "；".join(closed), "；".join(finite) or "finitePublicationGate=PENDING", "；".join(opened)


def _public_copy(report: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^###\s+{re.escape(heading)}\s*$\n(.+?)(?=^###\s+|^##\s+|\Z)",
        report,
    )
    if match is None:
        raise CanonicalSourceError("report source missing public copy: " + heading)
    value = re.sub(r"\s+", " ", match.group(1)).strip()
    if not value:
        raise CanonicalSourceError("empty public copy: " + heading)
    return value


def load_release_content(root: Path | None = None) -> ReleaseContent:
    source_root = (root or Path(os.environ.get(
        "R073N_RELEASE_ROOT", Path(__file__).resolve().parents[1]
    ))).resolve()
    texts = {relative: _regular_text(source_root, relative) for relative in CANONICAL_SOURCE_PATHS}
    report = texts[REPORT_SOURCE]
    dictionary = texts[DICTIONARY_SOURCE]
    combined = "\n".join(texts.values())

    for token in REQUIRED_BOUNDARY_TOKENS:
        if token not in combined:
            raise CanonicalSourceError("canonical sources missing boundary token: " + token)
    if "bounded" not in combined.lower() or "priority" not in combined.lower():
        raise CanonicalSourceError("canonical sources lost bounded-search/non-priority boundary")
    for phrase in PUBLIC_VOICE_BANS:
        if phrase in report:
            raise CanonicalSourceError("report source violates public voice: " + phrase)

    report_title = _one(r"(?m)^#\s+(.+?)\s*$", report, "report H1")
    status = _one(
        r"(?ms)\A#\s+[^\n]+\n\s*\*\*Status:\*\*\s*(.+?)(?=\n\n)",
        report,
        "report top-level status",
    )
    date_match = re.search(r"(?m)^\*\*(?:Date|Release date):\*\*\s*(.+?)\s*$", report)
    date = date_match.group(1).split(" ", 1)[0] if date_match else "2026-08-31"
    release_title_en = _one(
        r"(?m)^\*\*Release title:\*\*\s*\*?(.+?)\*?\s*$",
        dictionary,
        "dictionary release title",
    ).strip("* ")
    next_release = _one(
        r"(?m)^\*\*Next release:\*\*\s*(.+?)\s*$",
        dictionary,
        "dictionary next release",
    ).strip("* ")
    public_title_match = re.search(
        r"(?m)^\*\*Public title \(zh\):\*\*\s*(.+?)\s*$",
        report + "\n" + dictionary,
    )
    public_title_zh = (
        public_title_match.group(1).strip("* ")
        if public_title_match
        else "固定轨道有限应变稳定与变背景族非等度连续性"
    )
    lead_zh = _public_copy(report, "Lead")
    home_zh = _public_copy(report, "Home")
    recap_zh = _public_copy(report, "Recap")
    literature_zh = _public_copy(report, "Literature")
    next_gate_zh = _public_copy(report, "Next")
    closed, finite, opened = _machine_ledgers(combined)
    source_sha256 = {
        relative: hashlib.sha256(texts[relative].encode("utf-8")).hexdigest()
        for relative in CANONICAL_SOURCE_PATHS
    }
    return ReleaseContent(
        report_title=report_title,
        public_title_zh=public_title_zh,
        release_title_en=release_title_en,
        date=date,
        status=re.sub(r"\s+", " ", status).strip(),
        lead_zh=lead_zh,
        home_zh=home_zh,
        recap_zh=recap_zh,
        literature_zh=literature_zh,
        next_release=next_release,
        next_gate_zh=next_gate_zh,
        sections=_parse_sections(report),
        closed_ledger=closed,
        finite_ledger=finite,
        open_ledger=opened,
        source_sha256=source_sha256,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read and validate canonical R0.73N release content without writing."
    )
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if not args.check_only:
        parser.print_help()
        return
    content = load_release_content()
    print(json.dumps({
        "release": RELEASE,
        "canonicalSources": len(content.source_sha256),
        "sections": len(content.sections),
        "title": content.release_title_en,
        "fullThreeDimensionalFPS_H3_L2": "OPEN",
        "writes": 0,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
