#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Canonical-source reader and UI fragments for the fail-closed R0.73Q release.

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


RELEASE = "R0.73Q"
RELEASE_SLUG = "r073q"
SITE_VERSION = "1.57"
FIGURE_ID = "fig-r073q-heat-flow-separation"
FIGURE_SOURCE_RELATIVE = f"research/figures/r073q/{FIGURE_ID}"
FIGURE_ARCHIVE_RELATIVE = f"figures/r073q/{FIGURE_ID}"

R073P_BASELINE = {
    "latestCompletedRelease": "r073p",
    "siteVersion": "1.56",
    "publicHtmlNoteCount": 192,
    "postR060RecapNodeCount": 132,
    "nextRelease": "r073q",
    "postR070APublishedReleaseCount": 94,
    "postR070AFormalSealedReleaseCount": 70,
    "legacyFormalFigureBacklogCount": 24,
}

R073Q_TARGET = {
    "latestCompletedRelease": "r073q",
    "siteVersion": SITE_VERSION,
    "publicHtmlNoteCount": 193,
    "postR060RecapNodeCount": 133,
    "nextRelease": "r073r",
    "postR070APublishedReleaseCount": 95,
    "postR070AFormalSealedReleaseCount": 71,
    "legacyFormalFigureBacklogCount": 24,
}

CORE_CANONICAL_SOURCE_PATHS = (
    "research/r073q_problem_freeze.md",
    "research/r073q_heat_flow_stability_proof.md",
    "research/r073q_endpoint_no_go.md",
    "research/r073q_primary_literature_audit.md",
    "research/r073q_independent_literature_readback.md",
    "research/r073q_independent_analytic_audit.md",
    "research/r073q_claim_source_ledger.md",
    "research/r073q_gap_matrix.md",
)

FINAL_CANONICAL_SOURCE_PATHS = (
    "research/r073q_finite_diagnostic_audit.md",
    "research/r073q_report-source.md",
    "research/r073q_bilingual_dictionary.md",
)

CANONICAL_SOURCE_PATHS = CORE_CANONICAL_SOURCE_PATHS + FINAL_CANONICAL_SOURCE_PATHS
REPORT_SOURCE = "research/r073q_report-source.md"
DICTIONARY_SOURCE = "research/r073q_bilingual_dictionary.md"

REQUIRED_BOUNDARY_TOKENS = (
    "periodicOseenHLS=CLOSED_AFTER_AUDIT",
    "linearizedVolterraInverse=CLOSED_AFTER_AUDIT",
    "uniformAllRestartRadius=CLOSED_AFTER_AUDIT",
    "H3SerrinBridge=CLOSED_AFTER_AUDIT",
    "periodicHeatFlowTube=CLOSED_AFTER_AUDIT",
    "strictExtensionByUnion=CLOSED",
    "heatFlowBallContainsEntirePublishedH12Ball=NOT_PROVED",
    "bareKatoSupFromL4L6=BLOCKED_BY_ENDPOINT",
    "fullKochTataruTheory=NOT_REFUTED",
    "uniformL2Only=OPEN",
    "nonperturbativeBMOInverseUniqueness=FALSE_IN_GENERAL",
    "arbitraryThreeDimensionalGlobalRegularity=OPEN",
    "clayConclusion=OPEN",
    "noveltyOrPriorityClaim=FORBIDDEN",
)

# The canonical report is intentionally written once in a source-review state
# and changed only after the source-bound finite and figure packages are
# sealed.  A source dry-run must therefore be able to read either the PRESEAL
# or final value without accidentally opening the publication gate.  Only the
# value in ``FINAL_PUBLICATION_STATES`` contributes to ``publication_ready``.
ALLOWED_PUBLICATION_STATES = {
    "formulaDiagnosticValidation": frozenset(("PENDING", "PASS")),
    "formulaDiagnosticPackage": frozenset(("PENDING", "PRESEAL_PENDING", "PRESEAL_PASS", "CLOSED")),
    "sourceCommitAssigned": frozenset(("PENDING", "FALSE", "TRUE")),
    "finalSeal": frozenset(("PENDING", "FALSE", "TRUE")),
    "formalFigurePackage": frozenset(("PENDING", "PRESEAL_PENDING", "PRESEAL_PASS", "PASS")),
    "publicReleaseContent": frozenset(("PENDING", "READY")),
}
FINAL_PUBLICATION_STATES = {
    "formulaDiagnosticValidation": "PASS",
    "formulaDiagnosticPackage": "CLOSED",
    "sourceCommitAssigned": "TRUE",
    "finalSeal": "TRUE",
    "formalFigurePackage": "PASS",
    "publicReleaseContent": "READY",
}

ANALYTIC_FINAL_STATES = {
    "periodicOseenHLS": "CLOSED_AFTER_AUDIT",
    "linearizedVolterraInverse": "CLOSED_AFTER_AUDIT",
    "uniformAllRestartRadius": "CLOSED_AFTER_AUDIT",
    "H3SerrinBridge": "CLOSED_AFTER_AUDIT",
    "periodicHeatFlowTube": "CLOSED_AFTER_AUDIT",
    "strictExtensionByUnion": "CLOSED",
}

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
    publication_ready: bool
    readiness_detail: str
    missing_canonical_sources: tuple[str, ...]

    @property
    def document_title_en(self) -> str:
        """Site/PDF title derived from the canonical ASCII ledger title."""
        return re.sub(r"\\\((.*?)\\\)", r"\1", self.release_title_en).replace(" | ", "｜", 1)

    @property
    def math_next_gate_zh(self) -> str:
        """Keep the canonical mathematical R0.73R gate."""
        if self.next_release not in self.next_gate_zh:
            raise CanonicalSourceError("R0.73Q mathematical next-gate marker drift")
        return self.next_gate_zh

    @property
    def note_hero(self) -> str:
        return (
            '    <header class="hero"><div class="hero-inner">\n'
            '      <div><div class="eyebrow">研究笔记 R0.73Q · '
            'CRITICAL HEAT-FLOW TUBE / ENDPOINT NO-GO</div>\n'
            f'        <h1>{html.escape(self.public_title_zh)}</h1>\n'
            f'        <p class="lead">{html.escape(self.lead_zh)}</p></div>\n'
            '      <div class="stamp"><span class="state">状态 · R0.73Q 完成</span>'
            '<strong>Periodic Oseen--HLS + finite Volterra inversion</strong>'
            f'<p>版本 R0.73Q · {html.escape(self.date)}</p>'
            '<p>critical heat-flow tube：CLOSED AFTER AUDIT</p>'
            '<p>strict extension：BY UNION</p>'
            '<p>bare Kato-sup route：BLOCKED BY ENDPOINT</p>'
            '<p>L2-only / arbitrary 3D regularity / Clay：OPEN</p><p>NOT CLAY</p></div>\n'
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
            '<h2>热流稳定管、端点阻断与开放入口严格分列</h2>'
            f'<p>{html.escape(self.closed_ledger)}</p>'
            f'<p>{html.escape(self.finite_ledger)}</p>'
            f'<p>{html.escape(self.open_ledger)}</p>'
            '<p>连续体证明承担周期热流稳定结论；有限公式诊断只复算单模三范数和时间端点反例。'
            '它不证明任意 L2-small 数据安全，不否定完整 Koch--Tataru 理论，也不改变 Clay 状态。'
            'NOT CLAY。</p></section>'
        )
        figure = (
            '        <section id="figure"><div class="section-no">F / Journal figure</div>'
            '<h2>单模热流分离与端点时间映射反例</h2>'
            f'<p><img src="/assets/r073q/{FIGURE_ID}.svg" '
            'alt="R0.73Q exact heat-flow separation and endpoint-map diagnostic"></p>'
            f'<p><a href="/assets/r073q/{FIGURE_ID}.pdf">下载矢量 PDF</a> · '
            f'<a href="/assets/r073q/{FIGURE_ID}.png">下载 600 dpi PNG</a> · '
            f'<a href="/assets/r073q/{FIGURE_ID}.svg">打开 SVG</a></p>'
            '<p>附图只呈现精确单模范数幂律和标量时间端点反例。它不是 Navier--Stokes 仿真，'
            '不替代连续体双线性证明，也不认证任意数据全局正则。</p></section>'
        )
        reproduction = (
            '        <section id="reproduce"><div class="section-no">R / Reproduction</div>'
            '<h2>报告、证明、审计、证书与附图入口</h2>'
            '<p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073q_heat_flow_stability_proof.md">heat-flow stability proof</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073q_endpoint_no_go.md">endpoint no-go proof</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073q_primary_literature_audit.md">primary literature audit</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/'
            'research/certificates/r073q">finite diagnostic package</a></p>'
            f'<p><a href="/assets/r073q/{FIGURE_ID}.pdf">journal figure PDF</a> · '
            '<a href="/notes/r0-73q.pdf">synchronized note PDF</a> · '
            '<a href="/recap-r0-61-r0-73q.html">133-node cumulative recap</a> · '
            '<a href="/recap-r0-61-r0-73q.pdf">synchronized recap PDF</a></p>'
            '</section>'
        )
        return (
            "      <article>\n" + body + "\n" + figure + "\n" + boundary
            + "\n" + reproduction + "\n      </article>"
        )

    @property
    def home_card(self) -> str:
        return (
            '          <div class="task-one" id="r073q" data-release="r073q" '
            'style="margin-top:2rem">\n'
            f'            <p class="eyebrow">研究笔记 R0.73Q · {html.escape(self.date)}</p>'
            f'<h3>{html.escape(self.public_title_zh)}</h3>\n'
            f'            <p>{html.escape(self.home_zh)}</p>\n'
            f'            <p><strong>连续边界：</strong>{html.escape(self.closed_ledger)}</p>\n'
            f'            <p><strong>开放边界：</strong>{html.escape(self.open_ledger)}。'
            'NOT CLAY。</p>\n'
            '            <p><a href="/notes/r0-73q.html"><strong>阅读 R0.73Q '
            '研究笔记 →</strong></a><br><a href="/notes/r0-73q.pdf">下载同步 PDF</a> · '
            f'<a href="/assets/r073q/{FIGURE_ID}.pdf">下载期刊附图 PDF</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073q_heat_flow_stability_proof.md">查看连续证明</a> · '
            '<a href="/recap-r0-61-r0-73q.html">打开累计回顾</a></p>\n'
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
            f'        <div><p class="eyebrow">LATEST RELEASE · R0.73Q · '
            f'{html.escape(self.date)}</p><h2 class="route-map-title" '
            f'id="latest-release-title">{html.escape(self.public_title_zh)}</h2>'
            f'<p class="route-map-intro">{html.escape(self.lead_zh)}</p></div>\n'
            '        <nav class="route-map-actions" aria-label="最新发布快捷入口">'
            '<a class="route-map-latest" href="/notes/r0-73q.pdf">阅读最新 R0.73Q '
            '研究笔记 →</a><a href="/recap-r0-61-r0-73q.html">133 节累计回顾</a>'
            '<a href="/notes/">193 篇研究笔记总索引</a>'
            '<a href="#r073q">查看首页完整 R0.73Q 卡片</a></nav>\n'
            '      </header><div class="route-legend" aria-label="最新发布计数">'
            '<span><i class="route-legend-mark kept" aria-hidden="true"></i>'
            'R0.70A–R0.73Q · 95 节已公开</span>'
            '<span><i class="route-legend-mark kept" aria-hidden="true"></i>'
            '71 节完整封存</span><span><i class="route-legend-mark current" '
            'aria-hidden="true"></i>当前端点 R0.73Q</span></div></div>\n'
            '    </section>'
        )

    @property
    def recap_phase(self) -> str:
        return (
            f'            <article class="phase"><h3>R0.73Q · '
            f'{html.escape(self.release_title_en)}</h3>'
            f'<p>{html.escape(self.recap_zh)}</p>'
            f'<p>{html.escape(self.closed_ledger)}。{html.escape(self.finite_ledger)}。'
            f'{html.escape(self.open_ledger)}。NOT CLAY。</p>'
            '<div class="links"><a href="/notes/r0-73q.html">R0.73Q</a>'
            f'<a href="/assets/r073q/{FIGURE_ID}.pdf">R0.73Q 附图</a>'
            '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/'
            'research/certificates/r073q">R0.73Q 有限诊断包</a></div></article>'
        )

    @property
    def literature_update(self) -> str:
        return (
            '<span class="route-r073q-deck-update">'
            + html.escape(self.literature_zh)
            + ' uniform L2-only input threshold=OPEN；ADT 保持 ABSTRACT_ONLY_COLLISION；'
            '不承担新颖性或优先权声明。</span>'
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


def _compact_cjk_spaces(value: str) -> str:
    """Remove Markdown hard-wrap spaces only when both neighbours are CJK."""
    return re.sub(r"(?<=[\u3400-\u9fff])\s+(?=[\u3400-\u9fff])", "", value)


def _inline(value: str) -> str:
    value = _compact_cjk_spaces(value)
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
    fence_markers = (chr(96) * 3, "~~~")
    active_fence = ""
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
        matched_fence = next(
            (marker for marker in fence_markers if stripped.startswith(marker)),
            "",
        )
        if active_fence and matched_fence and matched_fence != active_fence:
            code_lines.append(row)
            continue
        if matched_fence:
            flush_blocks()
            if active_fence:
                output.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                code_lines.clear()
                active_fence = ""
            else:
                active_fence = matched_fence
            continue
        if active_fence:
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
    if active_fence or in_math:
        raise CanonicalSourceError("unterminated fenced or display-math block in report source")
    return "".join(output)


def _parse_sections(report: str) -> tuple[ReportSection, ...]:
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", report))
    if not matches:
        raise CanonicalSourceError("R0.73Q report source has no level-two sections")
    sections: list[ReportSection] = []
    used: set[str] = set()
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(report)
        title = re.sub(r"^\d+(?:\.\d+)*\.\s*", "", match.group(1)).strip()
        markdown = report[match.end():end].strip()
        if not markdown:
            raise CanonicalSourceError("empty report section: " + title)
        sections.append(ReportSection(
            number=index + 1,
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
    return _compact_cjk_spaces(paragraphs[0])


def _machine_ledgers(combined: str) -> tuple[str, str, str]:
    rows = re.findall(r"(?m)^[A-Za-z][A-Za-z0-9_]*(?:=[A-Z0-9_]+|=\d+)\s*$", combined)
    rows = list(dict.fromkeys(row.strip() for row in rows))
    closed = [
        row for row in rows
        if row.endswith(("=CLOSED", "=CLOSED_AFTER_AUDIT", "=CLOSED_EXACT"))
    ]
    finite = [
        row for row in rows
        if re.match(r"(?:finite|sourceCommit|finalSeal|formalFigure|publicRelease)", row)
    ]
    opened = [
        row for row in rows
        if row.endswith(("=OPEN", "=OPEN_COLLISION_SENSITIVE", "=NOT_PROVED", "=NOT_REFUTED", "=FALSE_IN_GENERAL"))
    ]
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
    value = _compact_cjk_spaces(re.sub(r"\s+", " ", match.group(1)).strip())
    if not value:
        raise CanonicalSourceError("empty public copy: " + heading)
    return value


def _metadata_field(value: str, label: str) -> str:
    match = re.search(
        rf"(?ms)^\*\*{re.escape(label)}:\*\*\s*(.+?)(?=\n\s*\n)",
        value,
    )
    if match is None:
        raise CanonicalSourceError("bilingual dictionary missing " + label)
    field = re.sub(r"\s+", " ", match.group(1)).strip("* ")
    if not field:
        raise CanonicalSourceError("empty bilingual dictionary field: " + label)
    return field


def _invariant_state(combined: str, key: str) -> str:
    states = set(re.findall(
        rf"(?m)^{re.escape(key)}=([A-Z0-9_]+)\s*$", combined
    ))
    if len(states) != 1:
        if any("PENDING" in state for state in states):
            return "MIXED_PENDING_" + "__".join(sorted(states))
        raise CanonicalSourceError(
            "publication invariant " + key
            + f": expected one unique state, found {sorted(states)}"
        )
    return states.pop()


def _publication_states(combined: str, key: str) -> tuple[str, ...]:
    """Read allowed PRESEAL/final provenance values, without opening the gate.

    During binding, the finite audit may already describe its sealed package
    while the reader-facing report still says PRESEAL/PENDING.  That mixed
    state is a valid review snapshot, but it is not publication-ready.  The
    gate opens only when every occurrence has the one final value.
    """
    states = set(re.findall(
        rf"(?m)^{re.escape(key)}=([A-Z0-9_]+)\s*$", combined
    ))
    if not states:
        raise CanonicalSourceError(
            "publication provenance " + key
            + ": expected at least one state, found none"
        )
    allowed = ALLOWED_PUBLICATION_STATES[key]
    unexpected = states - allowed
    if unexpected:
        raise CanonicalSourceError(
            "publication provenance " + key
            + f": expected only {sorted(allowed)}, found {sorted(unexpected)}"
        )
    return tuple(sorted(states))


def _build_public_report(*, forced_ready: bool) -> str:
    readiness = (
        "周期热流稳定证明已经通过解析复核；有限公式诊断和正式附图仍按独立发布门管理。"
        if forced_ready else
        "周期热流稳定证明仍在复核；发布生成器保持关闭。"
    )
    return r"""# R0.73Q | A critical heat-flow tube beyond the \(H^{1/2}\) entrance

## 1. 直接结论

固定一条先验全局周期强轨道。若初始差的线性热流在
\(L^4_tL^6_x\) 中足够小，则差分方程在同一临界空间闭合，并得到
对每个重启时刻统一的全局 \(H^3\) 稳定半径。

## 2. 临界闭合

周期 Oseen 核与 \(I_{1/4}:L^2_t\to L^4_t\) 给出双线性估计。
参考轨道的有限 \(M[u]=\|u\|_{L^4_tL^6_x}\) 作用量允许有限时间分段，
并构造显式的 Volterra 逆上界 \(K[u]\)。

## 3. 严格扩域

对 \(w_N=N^{-1/4}e_2\sin(Nx_1)\)，热流迹按 \(N^{-3/4}\) 衰减，
\(L^2\) 按 \(N^{-1/4}\) 衰减，而 \(H^{1/2}\) 按 \(N^{1/4}\) 增长。
旧管与新管的并集严格扩大稳定域；两个独立半径不作数值排序。

## 4. 端点边界

裸 Kato 上确界路线需要错误的 \(I_{1/4}:L^4_t\to L^\infty_t\) 映射。
精确时间反例只阻断这一证明路线，不否定完整 Koch--Tataru 理论。

## 5. 发布短文

### Lead

固定一条先验全局强轨道后，只要初始差的线性热流落入足够小的
\(L^4_tL^6_x\) 球，就得到对所有重启时刻统一的全局强稳定半径。

### Home

R0.73Q 增加一个周期临界热流入口；精确高频剪切模证明新旧稳定管的
并集严格扩大，但任意 \(L^2\)-small 数据仍未覆盖。

### Recap

本节闭合周期 Oseen--HLS 双线性估计、有限 Volterra 逆与二次固定点，
并用精确单模族和时间端点反例分开正结果与失败路线。NOT CLAY。

### Literature

whole-space Besov 开放性和周期各向异性扩域已有直接先例；ADT 只按
ABSTRACT_ONLY_COLLISION 引用，且不作新颖性或优先权声明。

### Next

R0.73R 将研究逐壳层模态数、相位相干和 \(L^6/L^2\) 集中怎样控制热流迹。

## 6. 发布状态

__READINESS__

精确标签为：
`periodicHeatFlowTube=CLOSED_AFTER_AUDIT`；
`strictExtensionByUnion=CLOSED`；
`bareKatoSupFromL4L6=BLOCKED_BY_ENDPOINT`；
`uniformL2Only=OPEN`；`clayConclusion=OPEN`。NOT CLAY。
""".replace("__READINESS__", readiness)

def load_release_content(root: Path | None = None) -> ReleaseContent:
    source_root = (root or Path(os.environ.get(
        "R073Q_RELEASE_ROOT", Path(__file__).resolve().parents[1]
    ))).resolve()
    texts = {
        relative: _regular_text(source_root, relative)
        for relative in CORE_CANONICAL_SOURCE_PATHS
    }
    missing_final = tuple(
        relative for relative in FINAL_CANONICAL_SOURCE_PATHS
        if not (source_root / relative).is_file()
    )
    for relative in FINAL_CANONICAL_SOURCE_PATHS:
        if relative not in missing_final:
            texts[relative] = _regular_text(source_root, relative)
    combined = "\n".join(texts.values())

    for token in REQUIRED_BOUNDARY_TOKENS:
        if token not in combined:
            raise CanonicalSourceError("canonical sources missing boundary token: " + token)
    publication_states: dict[str, tuple[str, ...]] = {}
    publication_tokens_ready = False
    if not missing_final:
        publication_states = {
            key: _publication_states(combined, key)
            for key in ALLOWED_PUBLICATION_STATES
        }
        publication_tokens_ready = all(
            publication_states[key] == (final_state,)
            for key, final_state in FINAL_PUBLICATION_STATES.items()
        )
    if "priority" not in combined.lower() or "ABSTRACT_ONLY_COLLISION" not in combined:
        raise CanonicalSourceError("canonical sources lost abstract-only/non-priority boundary")
    analytic_ledger = texts.get(DICTIONARY_SOURCE, combined)
    analytic_states = {
        key: _invariant_state(analytic_ledger, key)
        for key in ANALYTIC_FINAL_STATES
    }
    analytic_ready = all(
        analytic_states[key] == final_state
        for key, final_state in ANALYTIC_FINAL_STATES.items()
    )
    publication_ready = (
        analytic_ready and not missing_final
        and publication_tokens_ready
    )
    report = texts.get(REPORT_SOURCE, _build_public_report(forced_ready=analytic_ready))

    for expected in (
        "rho_{\\mathfrakX}[u]", "K[u]", "N^{-3/4}",
        "I_{1/4}:L^2_t\\toL^4_t", "BLOCKED_BY_ENDPOINT",
        "FALSE_IN_GENERAL",
    ):
        if expected not in combined.replace(" ", ""):
            raise CanonicalSourceError("canonical sources missing theorem interface: " + expected)
    for phrase in PUBLIC_VOICE_BANS:
        if phrase in report:
            raise CanonicalSourceError("report source violates public voice: " + phrase)

    report_title = _one(r"(?m)^#\s+(.+?)\s*$", report, "report H1")
    status = (
        _one(
            r"(?ms)\A#\s+[^\n]+\n\s*\*\*Status:\*\*\s*(.+?)(?=\n\n)",
            report,
            "report top-level status",
        )
        if REPORT_SOURCE in texts else
        "release scaffold only; formula diagnostic and final publication seals remain pending"
    )
    date = "2026-08-31"
    dictionary = texts.get(DICTIONARY_SOURCE, "")
    release_title_en = (
        _metadata_field(dictionary, "Release title")
        if dictionary else
        r"R0.73Q | A critical heat-flow tube beyond the \(H^{1/2}\) entrance"
    )
    next_release_match = re.search(
        r"(?m)^\*\*Next release:\*\*\s*(.+?)\s*$", dictionary
    )
    next_release = (
        next_release_match.group(1).strip("* ")
        if next_release_match else "R0.73R"
    )
    public_title_match = re.search(
        r"(?m)^\*\*Public title \(zh\):\*\*\s*(.+?)\s*$",
        report + "\n" + dictionary,
    )
    public_title_zh = (
        public_title_match.group(1).strip("* ")
        if public_title_match else
        r"R0.73Q｜越过 \(H^{1/2}\) 入口的临界热流稳定管"
    )
    fallback_lead = (
        "固定一条先验全局强轨道后，足够小的 L4_tL6_x 热流迹给出对全部重启时刻统一的稳定管。"
    )
    fallback_home = (
        "R0.73Q 增加一个周期临界热流入口；单模族证明新旧稳定管的并集严格扩大。"
    )
    fallback_recap = (
        "R0.73Q 用周期 Oseen--HLS 估计、有限 Volterra 递推和 Serrin 延拓闭合临界热流稳定管。"
    )
    fallback_literature = (
        "Gallagher--Iftimie--Planchon 与 Iftimie 给出直接碰撞；ADT 只按 ABSTRACT_ONLY_COLLISION 引用。"
    )
    fallback_next = (
        "R0.73R 将研究逐壳层模态数、相位相干和 L6/L2 集中怎样控制热流迹。"
    )
    if REPORT_SOURCE in texts:
        lead_zh = _public_copy(report, "Lead")
        home_zh = _public_copy(report, "Home")
        recap_zh = _public_copy(report, "Recap")
        literature_zh = _public_copy(report, "Literature")
        next_gate_zh = _public_copy(report, "Next")
    else:
        lead_zh = fallback_lead
        home_zh = fallback_home
        recap_zh = fallback_recap
        literature_zh = fallback_literature
        next_gate_zh = fallback_next

    closed = (
        "periodicOseenHLS=CLOSED_AFTER_AUDIT；"
        "linearizedVolterraInverse=CLOSED_AFTER_AUDIT；"
        "uniformAllRestartRadius=CLOSED_AFTER_AUDIT；"
        "H3SerrinBridge=CLOSED_AFTER_AUDIT；"
        "periodicHeatFlowTube=CLOSED_AFTER_AUDIT；strictExtensionByUnion=CLOSED"
    )
    finite = (
        "singleModeNormFormula=CLOSED_EXACT；endpointTimeMapNoGo=CLOSED_EXACT；"
        "navierStokesSimulation=NOT_RUN"
    )
    opened = (
        "heatFlowBallContainsEntirePublishedH12Ball=NOT_PROVED；"
        "fullKochTataruTheory=NOT_REFUTED；uniformL2Only=OPEN；"
        "nonperturbativeBMOInverseUniqueness=FALSE_IN_GENERAL；"
        "arbitraryThreeDimensionalGlobalRegularity=OPEN；clayConclusion=OPEN"
    )
    source_sha256 = {
        relative: hashlib.sha256(value.encode("utf-8")).hexdigest()
        for relative, value in texts.items()
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
        publication_ready=publication_ready,
        readiness_detail=(
            "analyticBoundary="
            + ",".join(f"{key}={analytic_states[key]}" for key in ANALYTIC_FINAL_STATES)
            + "; "
            + (
                "publicationProvenance="
                + ",".join(
                    f"{key}={'|'.join(publication_states[key])}"
                    for key in ALLOWED_PUBLICATION_STATES
                )
                if publication_states else
                "publicationProvenance=MISSING_FINAL_CANONICAL_SOURCES"
            )
        ),
        missing_canonical_sources=missing_final,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read and validate canonical R0.73Q release content without writing."
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
        "canonicalSourcesPlanned": len(CANONICAL_SOURCE_PATHS),
        "missingCanonicalSources": list(content.missing_canonical_sources),
        "sections": len(content.sections),
        "title": content.release_title_en,
        "publicationReady": content.publication_ready,
        "readinessDetail": content.readiness_detail,
        "uniformL2Only": "OPEN",
        "nonperturbativeBMOInverseUniqueness": "FALSE_IN_GENERAL",
        "writes": 0,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
