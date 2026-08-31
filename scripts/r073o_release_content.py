#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Canonical-source reader and UI fragments for the fail-closed R0.73O release.

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


RELEASE = "R0.73O"
RELEASE_SLUG = "r073o"
SITE_VERSION = "1.55"
FIGURE_ID = "fig-r073o-kolmogorov-spectrum"
FIGURE_SOURCE_RELATIVE = f"research/figures/r073o/{FIGURE_ID}"
FIGURE_ARCHIVE_RELATIVE = f"figures/r073o/{FIGURE_ID}"

R073N_BASELINE = {
    "latestCompletedRelease": "r073n",
    "siteVersion": "1.54",
    "publicHtmlNoteCount": 190,
    "postR060RecapNodeCount": 130,
    "nextRelease": "r073o",
    "postR070APublishedReleaseCount": 92,
    "postR070AFormalSealedReleaseCount": 68,
    "legacyFormalFigureBacklogCount": 24,
}

R073O_TARGET = {
    "latestCompletedRelease": "r073o",
    "siteVersion": SITE_VERSION,
    "publicHtmlNoteCount": 191,
    "postR060RecapNodeCount": 131,
    "nextRelease": "r073p",
    "postR070APublishedReleaseCount": 93,
    "postR070AFormalSealedReleaseCount": 69,
    "legacyFormalFigureBacklogCount": 24,
}

CORE_CANONICAL_SOURCE_PATHS = (
    "research/r073o_problem_freeze.md",
    "research/r073o_global_orbit_stability_proof.md",
    "research/r073o_forced_kolmogorov_contrast.md",
    "research/r073o_independent_analytic_audit.md",
    "research/r073o_literature_audit.md",
    "research/r073o_claim_source_ledger.md",
    "research/r073o_gap_matrix.md",
)

FINAL_CANONICAL_SOURCE_PATHS = (
    "research/r073o_finite_diagnostic_audit.md",
    "research/r073o_report-source.md",
    "research/r073o_bilingual_dictionary.md",
)

CANONICAL_SOURCE_PATHS = CORE_CANONICAL_SOURCE_PATHS + FINAL_CANONICAL_SOURCE_PATHS
REPORT_SOURCE = "research/r073o_report-source.md"
DICTIONARY_SOURCE = "research/r073o_bilingual_dictionary.md"

REQUIRED_BOUNDARY_TOKENS = (
    "uniformL2OnlyInputThreshold=OPEN_COLLISION_SENSITIVE",
    "forcedWitnessSolutionsGlobalSmooth=PLANAR_ONLY",
    "clayConclusion=OPEN",
    "noveltyOrPriorityClaim=FORBIDDEN",
)

# The canonical report is intentionally written once in a source-review state
# and changed only after the source-bound finite and figure packages are
# sealed.  A source dry-run must therefore be able to read either the PRESEAL
# or final value without accidentally opening the publication gate.  Only the
# value in ``FINAL_PUBLICATION_STATES`` contributes to ``publication_ready``.
ALLOWED_PUBLICATION_STATES = {
    "finiteDiagnosticValidation": frozenset(("PASS",)),
    "finiteDiagnosticPackage": frozenset(("PRESEAL_PASS", "CLOSED")),
    "sourceCommitAssigned": frozenset(("FALSE", "TRUE")),
    "finalSeal": frozenset(("FALSE", "TRUE")),
    "formalFigurePackage": frozenset(("PRESEAL_PASS", "PASS")),
    "publicReleaseContent": frozenset(("PENDING", "READY")),
}
FINAL_PUBLICATION_STATES = {
    "finiteDiagnosticValidation": "PASS",
    "finiteDiagnosticPackage": "CLOSED",
    "sourceCommitAssigned": "TRUE",
    "finalSeal": "TRUE",
    "formalFigurePackage": "PASS",
    "publicReleaseContent": "READY",
}

UNFORCED_FINAL_STATES = {
    "CLOSED_AFTER_AUDIT",
    "CLOSED_CONDITIONALLY_AFTER_AUDIT",
}
FORCED_FINAL_STATES = {
    "CLOSED_BY_COMPOSITE_SPECTRAL_CERTIFICATE_AFTER_AUDIT",
    "CLOSED_BY_COMPOSITE_PRIMARY_SOURCE_CHAIN_AFTER_AUDIT",
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
        return self.release_title_en.replace(" | ", "｜", 1)

    @property
    def math_next_gate_zh(self) -> str:
        """Keep the mathematical R0.73P gate, without the pre-deploy handoff."""
        marker = f"数学上的下一发布门是 {self.next_release}："
        if marker not in self.next_gate_zh:
            raise CanonicalSourceError("R0.73O mathematical next-gate marker drift")
        return self.next_gate_zh.split(marker, 1)[1].strip()

    @property
    def note_hero(self) -> str:
        return (
            '    <header class="hero"><div class="hero-inner">\n'
            '      <div><div class="eyebrow">研究笔记 R0.73O · '
            'GLOBAL-ORBIT STABILITY / FORCED CONTRAST</div>\n'
            f'        <h1>{html.escape(self.public_title_zh)}</h1>\n'
            f'        <p class="lead">{html.escape(self.lead_zh)}</p></div>\n'
            '      <div class="stamp"><span class="state">状态 · R0.73O 完成</span>'
            '<strong>Classical route closure + forced comparison</strong>'
            f'<p>版本 v0.73O · {html.escape(self.date)}</p>'
            '<p>unforced global orbit (H3,H3)：CLOSED CONDITIONALLY</p>'
            '<p>forced planar witness H3→L2：PRIMARY-SOURCE CHAIN</p>'
            '<p>finite spectrum：DIAGNOSTIC ONLY</p>'
            '<p>L2-only 3D input / Clay：OPEN</p><p>NOT CLAY</p></div>\n'
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
            '<h2>条件稳定、强迫对照与开放问题严格分列</h2>'
            f'<p>{html.escape(self.closed_ledger)}</p>'
            f'<p>{html.escape(self.finite_ledger)}</p>'
            f'<p>{html.escape(self.open_ledger)}</p>'
            '<p>无强迫结论以前提轨道已经全局为条件。强迫对照属于不同方程。'
            '有限谱计算不证明无限维正实谱；有界检索不承担原创性或优先权声明。'
            'NOT CLAY。</p></section>'
        )
        figure = (
            '        <section id="figure"><div class="section-no">F / Journal figure</div>'
            '<h2>Kolmogorov 有限谱诊断与截断收敛</h2>'
            f'<p><img src="/assets/r073o/{FIGURE_ID}.svg" '
            'alt="R0.73O finite-dimensional Kolmogorov spectral diagnostic and truncation convergence"></p>'
            f'<p><a href="/assets/r073o/{FIGURE_ID}.pdf">下载矢量 PDF</a> · '
            f'<a href="/assets/r073o/{FIGURE_ID}.png">下载 600 dpi PNG</a> · '
            f'<a href="/assets/r073o/{FIGURE_ID}.svg">打开 SVG</a></p>'
            '<p>附图只呈现有限 Fourier 截断的谱横坐标、临界值诊断与残差。'
            '无限维正实谱只来自正文列出的组合主来源，不来自这幅有限图。'
            '附图不认证非线性逃逸、奇性或 Clay。</p></section>'
        )
        reproduction = (
            '        <section id="reproduce"><div class="section-no">R / Reproduction</div>'
            '<h2>报告、证明、审计、证书与附图入口</h2>'
            '<p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073o_global_orbit_stability_proof.md">unforced continuum proof</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073o_forced_kolmogorov_contrast.md">forced contrast</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073o_literature_audit.md">bounded literature audit</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/'
            'research/certificates/r073o">finite diagnostic package</a></p>'
            f'<p><a href="/assets/r073o/{FIGURE_ID}.pdf">journal figure PDF</a> · '
            '<a href="/notes/r0-73o.pdf">synchronized note PDF</a> · '
            '<a href="/recap-r0-61-r0-73o.html">131-node cumulative recap</a> · '
            '<a href="/recap-r0-61-r0-73o.pdf">synchronized recap PDF</a></p>'
            '</section>'
        )
        return (
            "      <article>\n" + body + "\n" + figure + "\n" + boundary
            + "\n" + reproduction + "\n      </article>"
        )

    @property
    def home_card(self) -> str:
        return (
            '          <div class="task-one" id="r073o" data-release="r073o" '
            'style="margin-top:2rem">\n'
            f'            <p class="eyebrow">研究笔记 R0.73O · {html.escape(self.date)}</p>'
            f'<h3>{html.escape(self.public_title_zh)}</h3>\n'
            f'            <p>{html.escape(self.home_zh)}</p>\n'
            f'            <p><strong>连续边界：</strong>{html.escape(self.closed_ledger)}</p>\n'
            f'            <p><strong>开放边界：</strong>{html.escape(self.open_ledger)}。'
            'NOT CLAY。</p>\n'
            '            <p><a href="/notes/r0-73o.html"><strong>阅读 R0.73O '
            '研究笔记 →</strong></a><br><a href="/notes/r0-73o.pdf">下载同步 PDF</a> · '
            f'<a href="/assets/r073o/{FIGURE_ID}.pdf">下载期刊附图 PDF</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073o_global_orbit_stability_proof.md">查看连续证明</a> · '
            '<a href="/recap-r0-61-r0-73o.html">打开累计回顾</a></p>\n'
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
            f'        <div><p class="eyebrow">LATEST RELEASE · R0.73O · '
            f'{html.escape(self.date)}</p><h2 class="route-map-title" '
            f'id="latest-release-title">{html.escape(self.public_title_zh)}</h2>'
            f'<p class="route-map-intro">{html.escape(self.lead_zh)}</p></div>\n'
            '        <nav class="route-map-actions" aria-label="最新发布快捷入口">'
            '<a class="route-map-latest" href="/notes/r0-73o.pdf">阅读最新 R0.73O '
            '研究笔记 →</a><a href="/recap-r0-61-r0-73o.html">131 节累计回顾</a>'
            '<a href="/notes/">191 篇研究笔记总索引</a>'
            '<a href="#r073o">查看首页完整 R0.73O 卡片</a></nav>\n'
            '      </header><div class="route-legend" aria-label="最新发布计数">'
            '<span><i class="route-legend-mark kept" aria-hidden="true"></i>'
            'R0.70A–R0.73O · 93 节已公开</span>'
            '<span><i class="route-legend-mark kept" aria-hidden="true"></i>'
            '69 节完整封存</span><span><i class="route-legend-mark current" '
            'aria-hidden="true"></i>当前端点 R0.73O</span></div></div>\n'
            '    </section>'
        )

    @property
    def recap_phase(self) -> str:
        return (
            f'            <article class="phase"><h3>R0.73O · '
            f'{html.escape(self.release_title_en)}</h3>'
            f'<p>{html.escape(self.recap_zh)}</p>'
            f'<p>{html.escape(self.closed_ledger)}。{html.escape(self.finite_ledger)}。'
            f'{html.escape(self.open_ledger)}。NOT CLAY。</p>'
            '<div class="links"><a href="/notes/r0-73o.html">R0.73O</a>'
            f'<a href="/assets/r073o/{FIGURE_ID}.pdf">R0.73O 附图</a>'
            '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/'
            'research/certificates/r073o">R0.73O 有限诊断包</a></div></article>'
        )

    @property
    def literature_update(self) -> str:
        return (
            '<span class="route-r073o-deck-update">'
            + html.escape(self.literature_zh)
            + ' uniform L2-only input threshold=OPEN；bounded search '
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
        raise CanonicalSourceError("R0.73O report source has no level-two sections")
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
    forced_gate = (
        "独立解析复核已经核对组合链的归一化、Riesz 投影秩、统一高频界和全部 Fourier 扇区。"
        if forced_ready else
        "组合链仍等待最终独立解析复核；发布生成器因此保持关闭。下述内容只登记待核对的证明接口。"
    )
    return r"""# R0.73O | Global-orbit stability and a forced Kolmogorov contrast

## 1. 直接结论

无强迫方程一侧，R0.73O 把 R0.73N 的显式有限应变机制扩展到任意一个**已经先验全局存在**的周期三维强解。每条这样的轨道都有有限的累积 \(H^4\) 作用量，并有一个对全部起始时刻有效的正 \(H^3\) 同步稳定半径。这个现象属于经典稳定理论在当前拓扑中的直接闭合，不作原创性或优先权声明。

强迫方程一侧，显式 Kolmogorov 平衡态提供相反对照：平衡态不衰减，累积应变发散，并有平面方向的 \(H^3\)-小扰动逃离固定 \(L^2\) 球。无限维正实谱来自组合主来源；有限 Fourier 计算只作诊断。

这两个结论不解决任意三维初值的全局正则性。强迫例子属于不同方程，所有逃逸见证仍然全局光滑。

## 2. 无强迫全局轨道的有限作用量

在标准三维环面、黏性系数一、零均值无散度相空间中，设

\[
 u\in C([0,\infty);H^3_{\sigma,0})
 \cap L^2_{\rm loc}([0,\infty);H^4_{\sigma,0})
\]

已经是全局强解。能量等式先给出有限的 \(L^2_tH^1_x\) 耗散。轨道随后进入通用的小 \(H^1\) 球；\(H^1\to H^2\to H^3\) 的能量阶梯给出指数衰减。带权 \(H^3\) 能量估计再推出

\[
 \mathcal A_4[u]=\int_0^\infty \lVert u(t)\rVert_{H^4}\,dt<\infty.
\]

有限初始区间使用假设中的 \(L^2_{\rm loc}H^4\)，无限尾部使用指数权重。这个论证不能倒过来证明一条尚不知道能否全局延拓的轨道。

## 3. 对所有起始时刻有效的稳定管

令 \(w=v-u\)、\(X=|w|_3^2\)、\(Y=|w|_4^2\)。周期交换子与 Moser 估计给出

\[
 {1\over2}X'+Y\le C_*|u|_4X+C_*X^{1/2}Y.
\]

于是 Stokes \(H^3\) 范数中的半径可取为

\[
 R_A[u]={1\over4C_*}\exp\!\bigl(-C_*\mathcal A_4[u]\bigr)>0.
\]

只要 \(|v(t_0)-u(t_0)|_3<R_A[u]\)，扰动解就全局存在，并满足

\[
 |v(t)-u(t)|_3\le e^{C_*\mathcal A_4[u]}
 e^{-(t-t_0)/2}|v(t_0)-u(t_0)|_3.
\]

同一个半径对每个 \(t_0\ge0\) 有效。通常 \(H^3\) 范数只引入固定等价常数，不能把两个数值半径直接认作相同。

## 4. 拓扑边界

这个定理关闭的是全三维同步 \((H^3,H^3)\) 稳定，并给出 \(H^3\)-输入、\(L^2\)-输出的直接推论。它没有关闭“初值只在 \(L^2\) 中小、但 \(H^3\) 可任意大”的全三维 FPS \((H^3,L^2)\) 单元。

全局强解初值集在 \(H^3\) 中是开集。其补集若非空则为闭集；这只是拓扑推论，不证明补集非空，也不证明所有光滑初值全局。

## 5. 强迫 Kolmogorov 平衡态

在同一标准三维环面上取

\[
 U_*=(30.12\sin 10y,0,0),\qquad
 f_*=(3012\sin 10y,0,0).
\]

非线性输运项恒为零，且 \(-\Delta U_*=f_*\)，所以 \(U_*\) 是强迫方程的精确稳态。它不随时间衰减，并满足

\[
 \int_0^\infty\lVert\nabla U_*\rVert_\infty\,dt=\infty.
\]

取物理横向波数 \(m=7\)、强迫波数 \(N=10\)，无量纲参数恰为 \(\alpha=m/N=0.7\) 和 \(R=30.12/10=3.012\)。

## 6. 无限维正实谱的来源

临界区间

\[
 R_c\in[3.011528364444,3.011528364446]
\]

来自 Nagatou 的计算机辅助定理及 Watanabe 等人的精确复述。正实谱的超临界方向不是由有限矩阵的正号决定，而由以下组合链决定：

1. [Nagatou](https://doi.org/10.1016/j.cam.2003.10.016) 排除非零虚轴穿越；
2. [Matsuda--Miyatake Proposition 1](https://doi.org/10.2748/tmj/1113247600) 唯一化零特征值的中性参数；
3. [Ilyin Theorem 5.1](https://doi.org/10.1070/SM2005v196n01ABEH000871) 在有限的大参数处提供正实谱锚点；
4. 公共定义域上的椭圆算子族、紧预解式、Riesz 投影秩连续性和统一高频界把非零右半平面谱传递到每个 \(R>R_c\)。

__FORCED_GATE__

因此正式发布只能陈述“至少一个正实平面特征值”，不能陈述本节找到了本质三维不稳定模态。

## 7. 从线性谱到全局光滑的非线性逃逸

[Friedlander--Pavlović--Shvydkoy](https://doi.org/10.1007/s00220-006-1526-7) 的非线性不稳定定理先应用在二维不变环面，取 \(n=2,p=2,q=4\)。光滑不稳定方向可使初始扰动在任意固定 \(H^s\) 中趋于零，而解仍逃离一个固定 \(L^2\) 球。

随后把二维解沿 \(z\) 常数延拓到三维环面。范数只乘一个固定因子，平面子空间严格不变，二维全局正则性保证每个三维见证解都全局光滑。这个存在性序列已经足以证明全相空间中的不稳定，但不说明一般非平面小扰动全局存在。

## 8. 有限谱诊断的边界

正式附图展示 Fourier 截断谱横坐标、临界穿越、截断收敛和残差。主计算在 \(R=3.012\) 得到正的有限维无量纲增长率；独立装配的广义特征值问题复现同一数值尺度。

这些结果检查缩放、符号、实现和收敛表现。它们不证明无限维正实谱，不代替 Nagatou 的临界区间，不计算非线性逃逸，也不认证奇性。图中和正文中的这条边界必须保持一致。

## 9. 文献边界

[Pizzocchero 2021](https://doi.org/10.1016/j.aml.2020.106970) 已直接给出周期光滑全局解的稳定半径；相关整体稳定、最终解析性与开放性现象也早已存在于文献中。因此无强迫部分应称为自包含的经典路线闭合。

[Mucha 2001](https://doi.org/10.1006/jdeq.2000.3863) 是 \(L^2\)-小扰动问题最接近的周期碰撞来源，但本次没有读取其完整定理量词。[Mucha 2008](https://doi.org/10.4064/bc81-0-18) 只证明其自身方法中的小 \(L^2\) 条件依赖高阶迹范数。这里不能据此断言整个文献不存在统一的 \(L^2\)-only 阈值。

## 10. 下一接口

另一个已知全局的无强迫背景不会改变瓶颈。R0.73P 应直接检查 \(L^2\)-only / 高频扰动接口：当初始 \(L^2\) 很小而 \(H^3\) 很大时，现有稳定管在哪一步失效，哪些附加频率局部化条件可以恢复可验证的结论。

强迫模型仍可作实验室，但任何结论转回 Clay 方程都必须另有去除外力的严格论证。

## 11. 明确排除

- 不证明任意三维光滑初值全局；
- 不证明全三维 \(L^2\)-only 输入稳定；
- 不证明本质三维不稳定模态；
- 不证明爆破、湍流、异常耗散或非唯一性；
- 不声称有限矩阵认证无限维谱；
- 不声称强迫对照直接推进 Clay 结论。

精确公开标签是 `NOT CLAY`。
""".replace("__FORCED_GATE__", forced_gate)


def load_release_content(root: Path | None = None) -> ReleaseContent:
    source_root = (root or Path(os.environ.get(
        "R073O_RELEASE_ROOT", Path(__file__).resolve().parents[1]
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
    if "bounded" not in combined.lower() or "priority" not in combined.lower():
        raise CanonicalSourceError("canonical sources lost bounded-search/non-priority boundary")
    unforced_state = _invariant_state(combined, "unforcedGlobalOrbitH3Stability")
    forced_state = _invariant_state(combined, "forcedKolmogorovH3InputL2Escape")
    unforced_ready = unforced_state in UNFORCED_FINAL_STATES
    forced_ready = forced_state in FORCED_FINAL_STATES
    publication_ready = (
        unforced_ready and forced_ready and not missing_final
        and publication_tokens_ready
    )
    report = texts.get(REPORT_SOURCE, _build_public_report(forced_ready=forced_ready))

    for expected in (
        "A_4[u]", "R_A[u]", "3.011528364444", "R=3.012",
        "n=2,p=2,q=4",
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
        "release scaffold only; final composite spectral audit remains pending"
    )
    date = "2026-08-31"
    dictionary = texts.get(DICTIONARY_SOURCE, "")
    release_title_en = (
        _one(
            r"(?m)^\*\*Release title:\*\*\s*\*?(.+?)\*?\s*$",
            dictionary,
            "dictionary release title",
        ).strip("* ")
        if dictionary else
        "Global-orbit stability and a forced Kolmogorov contrast"
    )
    next_release = (
        _one(
            r"(?m)^\*\*Next release:\*\*\s*(.+?)\s*$",
            dictionary,
            "dictionary next release",
        ).strip("* ")
        if dictionary else "R0.73P"
    )
    public_title_match = re.search(
        r"(?m)^\*\*Public title \(zh\):\*\*\s*(.+?)\s*$",
        report + "\n" + dictionary,
    )
    public_title_zh = (
        public_title_match.group(1).strip("* ")
        if public_title_match else
        "R0.73O｜全局轨道稳定管与强迫 Kolmogorov 对照"
    )
    fallback_lead = (
        "无强迫一侧，每条先验全局的周期 H3 强轨道都有正的同步稳定管；"
        "强迫一侧，一个非衰减 Kolmogorov 平衡态沿平面方向发生全局光滑的 L2 逃逸。"
        "前者是经典路线闭合，后者的无限维正实谱来自组合主来源，有限谱图只作诊断。"
    )
    fallback_home = (
        "我把固定成员的有限应变稳定机制扩展到任意先验全局的无强迫周期轨道，"
        "并用强迫 Kolmogorov 平衡态记录一个拓扑匹配的反向对照。"
        "两个结论都不改变任意三维初值的全局正则性问题。"
    )
    fallback_recap = (
        "R0.73O 关闭了已知全局无强迫背景上的 H3 小扰动不稳定路线："
        "每条轨道最终衰减、累积 H4 作用量有限，并有统一起始时刻的正稳定半径。"
        "强迫对照则保留无限累积应变，并由平面方向给出全局光滑的固定 L2 逃逸。"
    )
    fallback_literature = (
        "Pizzocchero 已给出直接的周期稳定定理；Mucha 2001 仍是 L2-only 阈值最接近且量词未完全核对的碰撞来源。"
        "Kolmogorov 正实谱使用 Nagatou、Matsuda--Miyatake、Ilyin 与 Watanabe 的组合链。"
    )
    fallback_next = (
        "数学上的下一发布门是 R0.73P：直接检查 L2-only / 高频输入接口，"
        "不再重复选择另一个已知全局的无强迫背景。"
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
        "unforcedGlobalOrbitH3Stability=CLOSED_CONDITIONALLY_ON_GLOBAL_REFERENCE；"
        "globalDataSetH3Open=CLOSED_AS_CLASSICAL_COROLLARY"
    )
    if forced_ready:
        closed += "；forcedKolmogorovPlanarH3InputL2Escape=CLOSED_BY_PRIMARY_SOURCE_COMBINATION"
    else:
        closed += "；forcedKolmogorovPlanarH3InputL2Escape=FINAL_REVIEW_PENDING"
    finite = (
        "finiteKolmogorovSpectrum=DIAGNOSTIC_ONLY；"
        "finiteComputationProvesPositiveInfiniteDimensionalSpectrum=FALSE"
    )
    opened = (
        "uniformL2OnlyInputThreshold=OPEN；arbitraryDataGlobalRegularity=OPEN；"
        "essentiallyThreeDimensionalInstability=OPEN_NOT_NEEDED；Clay=OPEN"
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
            f"unforcedGlobalOrbitH3Stability={unforced_state}; "
            f"forcedKolmogorovH3InputL2Escape={forced_state}; "
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
        description="Read and validate canonical R0.73O release content without writing."
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
        "fullThreeDimensionalFPS_H3_L2": "OPEN",
        "writes": 0,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
