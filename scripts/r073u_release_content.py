#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read the frozen R0.73U sources and expose fail-closed release copy.

This module does not decide mathematical truth and does not write files.  It
extracts reader-facing copy from ``research/r073u_report-source.md``, checks
the classical/local/open boundary, and supplies the small retro HTML fragments
used by the later publication transaction.
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


RELEASE = "R0.73U"
RELEASE_ID = "r073u"
SITE_VERSION = "1.61"
NEXT_RELEASE = "R0.73V"
PUBLIC_TITLE_ZH = "R0.73U｜完整张量进入热层级：压力可以恢复，但偶二次状态的动力学并不闭合"
RELEASE_TITLE_EN = "R0.73U | Full tensors in the heat hierarchy: pressure is recoverable, but the even quadratic state is not dynamically closed"
FIGURE_ID = "fig-r073u-tensor-heat-hierarchy"
FIGURE_SOURCE_RELATIVE = f"research/figures/r073u/{FIGURE_ID}"
FIGURE_ARCHIVE_RELATIVE = f"figures/r073u/{FIGURE_ID}"

R073T_BASELINE = {
    "latestCompletedRelease": "r073t",
    "siteVersion": "1.60",
    "publicHtmlNoteCount": 196,
    "postR060RecapNodeCount": 136,
    "nextRelease": "r073u",
    "postR070APublishedReleaseCount": 98,
    "postR070AFormalSealedReleaseCount": 74,
    "legacyFormalFigureBacklogCount": 24,
}

R073U_TARGET = {
    "latestCompletedRelease": RELEASE_ID,
    "siteVersion": SITE_VERSION,
    "publicHtmlNoteCount": 197,
    "postR060RecapNodeCount": 137,
    "nextRelease": "r073v",
    "postR070APublishedReleaseCount": 99,
    "postR070AFormalSealedReleaseCount": 75,
    "legacyFormalFigureBacklogCount": 24,
}

CANONICAL_SOURCE_PATHS = (
    "research/r073u_problem_freeze.md",
    "research/r073u_tensor_heat_hierarchy.md",
    "research/r073u_independent_analytic_audit.md",
    "research/r073u_primary_literature_audit.md",
    "research/r073u_claim_source_ledger.md",
    "research/r073u_evidence_gap_matrix.md",
    "research/r073u_report-source.md",
    "research/r073u_bilingual_dictionary.md",
)
PLANNED_AUDIT_PATHS = (
    "research/r073u_finite_diagnostic_audit.md",
    "research/r073u_figure_source_audit.md",
    "research/r073u_figure_source_reaudit.md",
)
REPORT_SOURCE = "research/r073u_report-source.md"
DICTIONARY_SOURCE = "research/r073u_bilingual_dictionary.md"

PUBLIC_VOICE_BANS = (
    "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计",
    "杀死错误想法", "颠覆性", "世界首个", "接近解决",
    "解决了千禧年", "证明了全局正则性", "原创性定理", "首次证明",
)

REQUIRED_SOURCE_MARKERS = (
    "localProductTensorDistinctFromKHM=TRUE",
    "instantaneousPressureFromLocalProductTensor=VERIFIED_CLASSICAL",
    "heatCovariancePSD=INTERNAL_EXACT",
    "heatCovarianceScalePDE=INTERNAL_EXACT",
    "filteredEquation=VERIFIED_CLASSICAL_RECONSTRUCTION",
    "criticalTensorStressRow=INTERNAL_COROLLARY",
    "energyOnlyFixedScaleStress=INTERNAL_COROLLARY",
    "centeredPressureVarianceDirectClassicalCollision=TRUE",
    "fourSiteParityWitness=INTERNAL_EXACT",
    r"The comparison concerns Navier--Stokes tangents at the same initial time for \(u\) and \(-u\); it is not a trajectory symmetry.",
    "LOCAL_DIRECT_NO_DGX",
    "Tran--Yu--Dritschel",
    "Zambrano--Duraisamy",
    "NOT CLAY",
)

CLOSED_LEDGER = (
    "heatCovariancePSD=INTERNAL_EXACT；heatCovarianceScalePDE=INTERNAL_EXACT；"
    "sameScalePressureReconstruction=VERIFIED_CLASSICAL；"
    "filteredNSEAndSGSFlux=VERIFIED_CLASSICAL_RECONSTRUCTION；"
    "conditionalCriticalStressRow=INTERNAL_COROLLARY；"
    "fixedPositiveScaleEnergyStressBound=INTERNAL_COROLLARY；"
    "fourSiteQuadraticStateNonAutonomy=CLOSED_EXACT；"
    "parabolicCoefficientLoss=CLOSED_EXACT"
)
FINITE_LEDGER = (
    "finiteWitnessIsSimulation=FALSE；navierStokesSimulation=NOT_RUN；"
    "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX；dgxUsed=FALSE；"
    "formalFiniteCertificate=PASS；formalFiniteCertificateChecks=75；"
    "formalFigurePackage=PASS；formalFigureChecks=325"
)
OPEN_LEDGER = (
    "finiteGeneralTensorClosure=OPEN；zeroScaleEnergyCriticalStressControl=OPEN；"
    "arbitraryThreeDimensionalGlobalRegularity=OPEN；clayConclusion=OPEN"
)
INITIAL_TIME_BOUNDARY_ZH = (
    r"这里比较的是 \(u\) 和 \(-u\) 作为同一时刻初值时的 Navier--Stokes "
    "切向量，不是轨道对称性。"
)


class CanonicalSourceError(RuntimeError):
    """A required source or public-claim boundary is absent or ambiguous."""


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
    source_sha256: dict[str, str]
    publication_ready: bool
    readiness_failures: tuple[str, ...]

    @property
    def document_title_en(self) -> str:
        return self.release_title_en.replace(" | ", "｜", 1)

    @property
    def note_hero(self) -> str:
        return (
            '    <header class="hero"><div class="hero-inner">\n'
            '      <div><div class="eyebrow">研究笔记 R0.73U · '
            'FULL TENSOR HEAT HIERARCHY / SIGNED-FLUX BOUNDARY</div>\n'
            f'        <h1>{html.escape(self.public_title_zh)}</h1>\n'
            f'        <p class="lead">{html.escape(self.lead_zh)}</p></div>\n'
            '      <div class="stamp"><span class="state">状态 · R0.73U 完成</span>'
            '<strong>Pressure recovery + exact quadratic-state non-autonomy</strong>'
            f'<p>版本 R0.73U · {html.escape(self.date)}</p>'
            '<p>heat covariance / scale PDE：INTERNAL EXACT</p>'
            '<p>same-scale pressure reconstruction：VERIFIED CLASSICAL</p>'
            '<p>four-site quadratic-state no-go：CLOSED EXACT</p>'
            '<p>arbitrary 3D regularity / Clay：OPEN</p>'
            '<p>NOT CLAY</p></div>\n'
            '    </div></header>'
        )

    @property
    def note_article(self) -> str:
        body = "\n".join(
            f'        <section id="{section.anchor}">'
            f'<div class="section-no">{section.number:02d} / canonical report</div>'
            f'<h2>{html.escape(section.title)}</h2>{section.html}</section>'
            for section in self.sections
        )
        figure = (
            '        <section id="figure"><div class="section-no">F / Journal figure</div>'
            '<h2>张量热层级、四站点切向量与抛物尺度损失</h2>'
            f'<p><img src="/assets/r073u/{FIGURE_ID}.svg" '
            'alt="R0.73U tensor heat hierarchy and exact signed-tangent witness"></p>'
            f'<p><a href="/assets/r073u/{FIGURE_ID}.pdf">下载矢量 PDF</a> · '
            f'<a href="/assets/r073u/{FIGURE_ID}.png">下载 600 dpi PNG</a> · '
            f'<a href="/assets/r073u/{FIGURE_ID}.svg">打开 SVG</a></p>'
            '<p>附图只展示解析公式与有限精确稀疏 Fourier 复算。四站点场是光滑平面'
            '三角多项式；它不是 Navier--Stokes 仿真、奇性、近奇性或爆破解。</p></section>'
        )
        boundary = (
            '        <section id="release-boundary">'
            '<div class="section-no">B / Exact release boundary</div>'
            '<h2>经典不等式、本地综合和开放问题分别列示</h2>'
            f'<p>{html.escape(CLOSED_LEDGER)}</p>'
            f'<p>{html.escape(FINITE_LEDGER)}</p>'
            f'<p>{html.escape(OPEN_LEDGER)}</p>'
            '<p>完整局部二次张量可以在同一 heat 尺度重建瞬时压力，但这不闭合其'
            '物理时间动力学。一致临界 stress 行已经假设经典强范数，而能量行在'
            '<code>s↓0</code> 时损失 <code>s^(-1/2)</code>。'
            f'{html.escape(INITIAL_TIME_BOUNDARY_ZH)} NOT CLAY。</p></section>'
        )
        reproduction = (
            '        <section id="reproduce"><div class="section-no">R / Reproduction</div>'
            '<h2>证明、文献、有限证书和附图入口</h2>'
            '<p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073u_tensor_heat_hierarchy.md">analytic derivation</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073u_primary_literature_audit.md">primary literature audit</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/'
            'research/certificates/r073u">finite exact package</a></p>'
            f'<p><a href="/assets/r073u/{FIGURE_ID}.pdf">journal figure PDF</a> · '
            '<a href="/notes/r0-73u.pdf">synchronized note PDF</a> · '
            '<a href="/recap-r0-61-r0-73u.html">137-node cumulative recap</a> · '
            '<a href="/recap-r0-61-r0-73u.pdf">synchronized recap PDF</a></p></section>'
        )
        return "      <article>\n" + body + "\n" + figure + "\n" + boundary + "\n" + reproduction + "\n      </article>"

    @property
    def home_card(self) -> str:
        return (
            '          <div class="task-one" id="r073u" data-release="r073u" style="margin-top:2rem">\n'
            f'            <p class="eyebrow">研究笔记 R0.73U · {html.escape(self.date)}</p>'
            f'<h3>{html.escape(self.public_title_zh)}</h3>\n'
            f'            <p>{html.escape(self.home_zh)}</p>\n'
            f'            <p><strong>闭合边界：</strong>{html.escape(CLOSED_LEDGER)}</p>\n'
            f'            <p><strong>开放边界：</strong>{html.escape(OPEN_LEDGER)}。NOT CLAY。</p>\n'
            f'            <p>{html.escape(INITIAL_TIME_BOUNDARY_ZH)}</p>\n'
            '            <p><a href="/notes/r0-73u.html"><strong>阅读 R0.73U 研究笔记 →</strong></a>'
            '<br><a href="/notes/r0-73u.pdf">下载同步 PDF</a> · '
            f'<a href="/assets/r073u/{FIGURE_ID}.pdf">下载期刊附图 PDF</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073u_tensor_heat_hierarchy.md">查看解析证明</a> · '
            '<a href="/recap-r0-61-r0-73u.html">打开累计回顾</a></p>\n'
            f'            <p><strong style="color:var(--gold)">下一发布门（{self.next_release}）：</strong>'
            f'&nbsp;{html.escape(self.next_gate_zh)}</p>\n'
            '          </div>'
        )

    @property
    def recap_phase(self) -> str:
        return (
            f'            <article class="phase"><h3>{html.escape(self.release_title_en)}</h3>'
            f'<p>{html.escape(self.recap_zh)}</p>'
            f'<p>{html.escape(CLOSED_LEDGER)}。{html.escape(FINITE_LEDGER)}。'
            f'{html.escape(OPEN_LEDGER)}。{html.escape(INITIAL_TIME_BOUNDARY_ZH)} NOT CLAY。</p>'
            '<div class="links"><a href="/notes/r0-73u.html">R0.73U</a>'
            f'<a href="/assets/r073u/{FIGURE_ID}.pdf">R0.73U 附图</a>'
            '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/'
            'research/certificates/r073u">R0.73U 有限证书</a></div></article>'
        )

    @property
    def literature_update(self) -> str:
        return (
            '<span class="route-r073u-deck-update">'
            + _inline(self.literature_zh)
            + ' heat covariance / pressure reconstruction=EXACT OR CLASSICAL；'
            'quadratic-state non-autonomy=CLOSED_EXACT；general tensor closure=OPEN；'
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


def _compact(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return re.sub(r"(?<=[\u3400-\u9fff]) (?=[\u3400-\u9fff])", "", value)


def _slug(title: str, used: set[str]) -> str:
    normalized = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-") or "section"
    candidate = value
    counter = 2
    while candidate in used:
        candidate = f"{value}-{counter}"
        counter += 1
    used.add(candidate)
    return candidate


def _inline(value: str) -> str:
    value = value.replace(r"K\'arm\'an", "Kármán").replace(r'H\"older', "Hölder")
    output: list[str] = []
    cursor = 0
    tokens = re.compile(r"\[([^\]\n]+)\]\((https?://[^)\s]+)\)|`([^`\n]+)`")
    for match in tokens.finditer(value):
        output.append(html.escape(value[cursor:match.start()], quote=False))
        if match.group(1) is not None:
            output.append(
                f'<a href="{html.escape(match.group(2), quote=True)}">'
                f'{html.escape(match.group(1))}</a>'
            )
        else:
            output.append(f"<code>{html.escape(match.group(3))}</code>")
        cursor = match.end()
    output.append(html.escape(value[cursor:], quote=False))
    return "".join(output)


def _markdown_blocks(markdown: str) -> str:
    rows = markdown.strip().splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    bullets: list[str] = []
    ordered: list[str] = []
    math: list[str] = []
    code: list[str] = []
    in_math = False
    in_code = False

    def flush() -> None:
        if paragraph:
            output.append("<p>" + _inline(" ".join(row.strip() for row in paragraph)) + "</p>")
            paragraph.clear()
        if bullets:
            output.append('<ul class="report-list">' + "".join(f"<li>{_inline(row)}</li>" for row in bullets) + "</ul>")
            bullets.clear()
        if ordered:
            output.append('<ol class="report-list report-list-ordered">' + "".join(f"<li>{_inline(row)}</li>" for row in ordered) + "</ol>")
            ordered.clear()

    for row in rows + [""]:
        stripped = row.strip()
        if stripped.startswith("```"):
            if in_math:
                raise CanonicalSourceError("code fence opened inside display math")
            if in_code:
                output.append(
                    '<pre class="report-ledger"><code>'
                    + html.escape("\n".join(code), quote=False)
                    + "</code></pre>"
                )
                code = []
                in_code = False
            else:
                flush()
                in_code = True
            continue
        if in_code:
            code.append(row)
            continue
        if stripped == r"\[":
            flush()
            in_math = True
            math = [r"\["]
            continue
        if in_math:
            math.append(row)
            if stripped == r"\]":
                output.append('<div class="equation result">' + html.escape("\n".join(math), quote=False) + "</div>")
                math = []
                in_math = False
            continue
        if stripped.startswith("- "):
            if paragraph or ordered:
                flush()
            bullets.append(stripped[2:].strip())
            continue
        numbered = re.match(r"^\d+\.\s+(.+)$", stripped)
        if numbered:
            if paragraph or bullets:
                flush()
            ordered.append(numbered.group(1).strip())
            continue
        if (bullets or ordered) and row.startswith(("  ", "\t")):
            target = bullets if bullets else ordered
            target[-1] += " " + stripped
            continue
        if not stripped:
            flush()
            continue
        paragraph.append(row)
    if in_math:
        raise CanonicalSourceError("unterminated display math in R0.73U report")
    if in_code:
        raise CanonicalSourceError("unterminated code fence in R0.73U report")
    return "".join(output)


def _sections(report: str) -> tuple[ReportSection, ...]:
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", report))
    if len(matches) != 9:
        raise CanonicalSourceError(f"R0.73U report must contain 9 sections, found {len(matches)}")
    used: set[str] = set()
    sections: list[ReportSection] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(report)
        title = re.sub(r"^\d+(?:\.\d+)*\.\s*", "", match.group(1)).strip()
        body = report[match.end():end].strip()
        if not body:
            raise CanonicalSourceError("empty report section: " + title)
        sections.append(ReportSection(index + 1, title, _slug(title, used), body, _markdown_blocks(body)))
    return tuple(sections)


def _section_body(report: str, number: int) -> str:
    match = re.search(
        rf"(?ms)^##\s+{number}\.\s+.+?$\n(.*?)(?=^##\s+|\Z)",
        report,
    )
    if match is None:
        raise CanonicalSourceError(f"report section {number} is absent")
    return match.group(1).strip()


def _prose_paragraphs(section: str) -> list[str]:
    without_fences = re.sub(r"(?ms)^```[^\n]*\n.*?^```[ \t]*$", " ", section)
    without_math = re.sub(r"(?ms)\\\[.*?\\\]", " ", without_fences)
    values: list[str] = []
    for block in re.split(r"\n\s*\n", without_math):
        stripped = block.strip()
        if not stripped or stripped.startswith(("- ", "#", "1. ", "2. ", "3. ")):
            continue
        values.append(_compact(stripped))
    return values


def _ordered_items(section: str) -> list[str]:
    values: list[str] = []
    current: list[str] = []
    for row in section.splitlines() + [""]:
        match = re.match(r"^\d+\.\s+(.+)$", row)
        if match:
            if current:
                values.append(_compact(" ".join(current)))
            current = [match.group(1).strip()]
        elif current and row.startswith((" ", "\t")) and row.strip():
            current.append(row.strip())
        elif current:
            values.append(_compact(" ".join(current)))
            current = []
    return values


def _certificate_final(root: Path) -> tuple[bool, str]:
    path = root / "research/certificates/r073u/manifest.json"
    if not path.is_file() or path.is_symlink():
        return False, "finite-certificate-manifest-missing"
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False, "finite-certificate-manifest-invalid"
    final = (
        manifest.get("schemaVersion") == "r073u-exact-tensor-heat-manifest-v1"
        and manifest.get("release") == RELEASE
        and manifest.get("status") == "sealed"
        and manifest.get("finalSeal") is True
        and manifest.get("certificateSourceCommitAssigned") is True
        and manifest.get("sourceCommitAssigned") is True
        and manifest.get("sourceCommit")
        == "84e808dae473f6381cbf9df55a71f5fe81a1cfce"
        and manifest.get("allPrerequisiteChecksPass") is True
        and manifest.get("checkInventory") == {"exact": 75, "required": 75}
        and manifest.get("inventory") == {
            "analyticSourceFileCount": 4,
            "boundFileCount": 7,
            "generatedFileCount": 3,
            "packageFileCount": 9,
            "sha256SumsLineCount": 8,
            "sourceFileCount": 6,
        }
    )
    return final, "finite-certificate-final-seal-pending" if not final else ""


def _figure_final(root: Path) -> tuple[bool, str]:
    path = root / FIGURE_SOURCE_RELATIVE / "manifest.json"
    if not path.is_file() or path.is_symlink():
        return False, "formal-figure-manifest-missing"
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False, "formal-figure-manifest-invalid"
    final = (
        manifest.get("schemaVersion")
        == "r073u-tensor-heat-hierarchy-manifest-v1"
        and manifest.get("figureId") == FIGURE_ID
        and manifest.get("finalSeal") is True
        and manifest.get("sourceCommitAssigned") is True
        and manifest.get("sourceCommit")
        == "84e808dae473f6381cbf9df55a71f5fe81a1cfce"
        and manifest.get("validation") == {
            "checksPassed": 325,
            "checksRequired": 325,
            "status": "PASS",
        }
        and isinstance(manifest.get("files"), list)
        and len(manifest["files"]) == 23
    )
    return final, "formal-figure-final-seal-pending" if not final else ""


def load_release_content(root: Path | None = None) -> ReleaseContent:
    source_root = (root or Path(os.environ.get(
        "R073U_RELEASE_ROOT", Path(__file__).resolve().parents[1]
    ))).resolve()
    texts = {relative: _regular_text(source_root, relative) for relative in CANONICAL_SOURCE_PATHS}
    report = texts[REPORT_SOURCE]
    dictionary = texts[DICTIONARY_SOURCE]
    combined = "\n".join(texts.values())
    combined_compact = re.sub(r"\s+", " ", combined)
    combined_nowhitespace = re.sub(r"\s+", "", combined)

    report_title = _one(r"(?m)^#\s+(.+?)\s*$", report, "report H1")
    if report_title != RELEASE_TITLE_EN:
        raise CanonicalSourceError("R0.73U report title drift: " + report_title)
    public_title = _one(r"(?m)^\*\*Public title \(zh\):\*\*\s*(.+?)\s*$", report, "public title")
    if public_title != PUBLIC_TITLE_ZH:
        raise CanonicalSourceError("R0.73U public title drift: " + public_title)
    date = _one(r"(?m)^\*\*Date:\*\*\s*(.+?)\s*$", report, "date")
    status = _compact(_one(
        r"(?ms)\A#\s+[^\n]+\n\s*\*\*Status:\*\*\s*(.+?)(?=\n\s*\n)",
        report,
        "status",
    ))

    for marker in REQUIRED_SOURCE_MARKERS:
        if marker not in combined_compact:
            raise CanonicalSourceError("canonical sources missing boundary marker: " + marker)
    for formula in (
        r"(\partial_s-\Delta)\tau_s",
        r"p_s=R_iR_j\Theta_{s,ij}",
        r"\partial_tv_s+\mathbbP\nabla\cdot",
        r"\sup_{s\ge0}\|\tau_s\|_{L_t^2L_x^3}",
        r"s^{-1/2}",
        r"K=\begin{pmatrix}-2&1&0",
        r"2\sqrt6Le^{-5\theta}",
    ):
        if formula not in combined_nowhitespace:
            raise CanonicalSourceError("canonical sources missing formula marker: " + formula)
    for phrase in PUBLIC_VOICE_BANS:
        if phrase in report:
            raise CanonicalSourceError("report source violates public voice: " + phrase)

    section_one = _prose_paragraphs(_section_body(report, 1))
    section_nine_source = _section_body(report, 9)
    section_nine = _prose_paragraphs(section_nine_source)
    next_items = _ordered_items(section_nine_source)
    if len(section_one) < 2 or len(section_nine) < 4:
        raise CanonicalSourceError("R0.73U report lacks required public-copy paragraphs")
    if len(next_items) != 2:
        raise CanonicalSourceError(
            f"R0.73U report must contain two next-step items, found {len(next_items)}"
        )

    certificate_ready, certificate_failure = _certificate_final(source_root)
    figure_ready, figure_failure = _figure_final(source_root)
    failures = [failure for ready, failure in (
        (certificate_ready, certificate_failure),
        (figure_ready, figure_failure),
    ) if not ready]
    for relative in PLANNED_AUDIT_PATHS:
        path = source_root / relative
        if not path.is_file() or path.is_symlink():
            failures.append("planned-audit-missing:" + relative)
    if b"\x08" in (source_root / REPORT_SOURCE).read_bytes():
        failures.append("canonical-source-backspace-control-character")
    if "pending" in status.lower() or "candidate" in status.lower():
        failures.append("reader-facing-status-pending")
    if "sourceCommitAssigned=FALSE" in combined or "finalSeal=FALSE" in combined:
        failures.append("canonical-ledger-scientific-seal-pending")
    if "Release title" not in dictionary or "Public title (zh)" not in dictionary:
        failures.append("bilingual-canonical-title-ledger-pending")

    source_sha256 = {
        relative: hashlib.sha256((source_root / relative).read_bytes()).hexdigest()
        for relative in texts
    }
    return ReleaseContent(
        report_title=report_title,
        public_title_zh=public_title,
        release_title_en=RELEASE_TITLE_EN,
        date=date,
        status=status,
        lead_zh=section_one[0],
        home_zh=section_one[1],
        recap_zh=section_nine[3],
        literature_zh=section_nine[0],
        next_release=NEXT_RELEASE,
        next_gate_zh="；".join(item.rstrip("；;。 ") for item in next_items) + "。",
        sections=_sections(report),
        source_sha256=source_sha256,
        publication_ready=not failures,
        readiness_failures=tuple(dict.fromkeys(failures)),
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read and validate canonical R0.73U release content without writing."
    )
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if not args.check_only:
        parser.print_help()
        return
    content = load_release_content()
    print(json.dumps({
        "release": RELEASE,
        "title": content.release_title_en,
        "publicTitleZh": content.public_title_zh,
        "canonicalSources": len(content.source_sha256),
        "canonicalSourcesPlanned": len(CANONICAL_SOURCE_PATHS) + len(PLANNED_AUDIT_PATHS),
        "sections": len(content.sections),
        "publicationReady": content.publication_ready,
        "readinessFailures": list(content.readiness_failures),
        "heatCovariancePSD": "INTERNAL_EXACT",
        "heatCovarianceScalePDE": "INTERNAL_EXACT",
        "sameScalePressureReconstruction": "VERIFIED_CLASSICAL",
        "conditionalCriticalStressRow": "INTERNAL_COROLLARY",
        "fixedPositiveScaleEnergyStressBound": "INTERNAL_COROLLARY",
        "fourSiteQuadraticStateNonAutonomy": "CLOSED_EXACT",
        "finiteGeneralTensorClosure": "OPEN",
        "arbitraryThreeDimensionalGlobalRegularity": "OPEN",
        "clayConclusion": "OPEN",
        "translationPath": "LOCAL_DIRECT_NO_DGX",
        "writes": 0,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
