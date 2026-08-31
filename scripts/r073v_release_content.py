#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read the frozen R0.73V sources and expose fail-closed release copy.

This module does not decide mathematical truth and does not write files.  It
extracts reader-facing copy from ``research/r073v_report-source.md``, checks
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


RELEASE = "R0.73V"
RELEASE_ID = "r073v"
SITE_VERSION = "1.62"
NEXT_RELEASE = "R0.73W"
PUBLIC_TITLE_ZH = "R0.73V｜压力感知的有符号三阶热提升：精确尺度生成律与 3→4 物理时间边界"
RELEASE_TITLE_EN = "R0.73V | A pressure-aware signed third-order heat lift: exact scale generation and the 3→4 physical-time boundary"
FIGURE_ID = "fig-r073v-signed-third-order-interface"
FIGURE_SOURCE_RELATIVE = f"figures/r073v/{FIGURE_ID}"
FIGURE_ARCHIVE_RELATIVE = f"figures/r073v/{FIGURE_ID}"

R073U_BASELINE = {
    "latestCompletedRelease": "r073u",
    "siteVersion": "1.61",
    "publicHtmlNoteCount": 197,
    "postR060RecapNodeCount": 137,
    "nextRelease": "r073v",
    "postR070APublishedReleaseCount": 99,
    "postR070AFormalSealedReleaseCount": 75,
    "legacyFormalFigureBacklogCount": 24,
}

R073V_TARGET = {
    "latestCompletedRelease": RELEASE_ID,
    "siteVersion": SITE_VERSION,
    "publicHtmlNoteCount": 198,
    "postR060RecapNodeCount": 138,
    "nextRelease": "r073w",
    "postR070APublishedReleaseCount": 100,
    "postR070AFormalSealedReleaseCount": 76,
    "legacyFormalFigureBacklogCount": 24,
}

CANONICAL_SOURCE_PATHS = (
    "research/r073v_problem_freeze.md",
    "research/r073v_signed_third_order_heat_lift.md",
    "research/r073v_independent_analytic_audit.md",
    "research/r073v_primary_literature_audit.md",
    "research/r073v_claim_source_ledger.md",
    "research/r073v_evidence_gap_matrix.md",
    "research/r073v_report-source.md",
    "research/r073v_bilingual_dictionary.md",
)
PLANNED_AUDIT_PATHS = (
    "research/r073v_finite_diagnostic_audit.md",
    "research/r073v_figure_source_audit.md",
    "research/r073v_figure_source_reaudit.md",
)
REPORT_SOURCE = "research/r073v_report-source.md"
DICTIONARY_SOURCE = "research/r073v_bilingual_dictionary.md"

PUBLIC_VOICE_BANS = (
    "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计",
    "杀死错误想法", "颠覆性", "世界首个", "接近解决",
    "解决了千禧年", "证明了全局正则性", "原创性定理", "首次证明",
)

FORBIDDEN_CLAIM_FLAGS = (
    "signedLiftInformationTheoreticMinimality=TRUE",
    "signedLiftInformationTheoreticMinimality=ESTABLISHED",
    "signedLiftComponentwiseMinimality=TRUE",
    "signedLiftUniqueness=TRUE",
    "fullThirdCumulantStateNonAutonomy=CLOSED_EXACT",
    "wholeFieldKappaCollision=TRUE",
    "fourthOrderNonClosure=TRUE",
    "fourthOrderNonClosure=CLOSED_EXACT",
    "finiteMomentHierarchyNoGo=TRUE",
    "finiteMomentHierarchyNoGo=CLOSED_EXACT",
    "clayConclusion=CLOSED",
    "clayConclusion=SOLVED",
)

FORBIDDEN_PUBLIC_CLAIMS = (
    "proves information-theoretic minimality",
    "proves componentwise minimality",
    "two complete kappa fields coincide",
    "two complete κ fields coincide",
    "proves fourth-order non-closure",
    "proves fourth-order nonclosure",
    "no finite moment hierarchy can close",
    "solves the Clay Millennium problem",
    "三阶提升是最小的",
    "完整 κ 场碰撞",
    "证明四阶不闭合",
    "任意有限矩层级都不可能闭合",
    "解决 Clay 千禧年问题",
)

REQUIRED_SOURCE_MARKERS = (
    "pressureAwareSignedHeatLift=INTERNAL_EXACT_AUDITED",
    "signedCrossCovarianceScalePDE=INTERNAL_EXACT_AUDITED",
    "quadraticTensorOddSlotRecovered=INTERNAL_EXACT_AUDITED",
    "germanoStressEquation=VERIFIED_CLASSICAL_INDEX_AUDITED",
    "conditionalKappaCriticalRow=INTERNAL_CONDITIONAL_AUDITED",
    "conditionalPressureVelocityCriticalRow=INTERNAL_CONDITIONAL_AUDITED",
    "pressureStrainCriticalRow=OPEN",
    "formalFiniteCertificate=SEALED",
    "signedLiftInformationTheoreticMinimality=NOT_ESTABLISHED",
    "fourthOrderNonClosure=NOT_ESTABLISHED",
    "finiteMomentHierarchyNoGo=NOT_ESTABLISHED",
    "LOCAL_DIRECT_NO_DGX",
    "NOT CLAY",
)

CLOSED_LEDGER = (
    "pressureAwareSignedHeatLift=INTERNAL_EXACT_AUDITED；"
    "signedCrossCovarianceScalePDE=INTERNAL_EXACT_AUDITED；"
    "quadraticTensorOddSlotRecovered=INTERNAL_EXACT_AUDITED；"
    "germanoStressEquation=VERIFIED_CLASSICAL_INDEX_AUDITED；"
    "selectedQuarticNextLevelRemainder=INTERNAL_EXACT_FINITE_SEALED"
)
FINITE_LEDGER = (
    "finiteWitnessIsSimulation=FALSE；navierStokesSimulation=NOT_RUN；"
    "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX；dgxUsed=FALSE；"
    "formalFiniteCertificate=PASS；formalFiniteCertificateChecks=66；"
    "coefficientwisePressureNonRecovery=INTERNAL_EXACT_FINITE_SEALED；"
    "formalFigurePackage=PASS；formalFigureChecks=147；formalFigureRows=158"
)
OPEN_LEDGER = (
    "pressureStrainCriticalRow=OPEN；signedLiftInformationTheoreticMinimality=NOT_ESTABLISHED；"
    "fourthOrderNonClosure=NOT_ESTABLISHED；finiteMomentHierarchyNoGo=NOT_ESTABLISHED；"
    "arbitraryThreeDimensionalGlobalRegularity=OPEN；clayConclusion=OPEN"
)
EXACT_SCOPE_BOUNDARY_ZH = (
    "有限证书只支持选定 Fourier 系数的压力项不可吸收和一个非零四次下一层余项；"
    "它不证明整个 κ 场碰撞、三阶提升最小、四阶不闭合或任意有限层级不可能闭合。"
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
            '      <div><div class="eyebrow">研究笔记 R0.73V · '
            'SIGNED THIRD-ORDER HEAT LIFT / PRESSURE-AWARE INTERFACE</div>\n'
            f'        <h1>{html.escape(self.public_title_zh)}</h1>\n'
            f'        <p class="lead">{html.escape(self.lead_zh)}</p></div>\n'
            '      <div class="stamp"><span class="state">状态 · R0.73V 完成</span>'
            '<strong>Exact signed lift + pressure-aware third-order interface</strong>'
            f'<p>版本 R0.73V · {html.escape(self.date)}</p>'
            '<p>signed cross-covariance scale PDE：INTERNAL EXACT AUDITED</p>'
            '<p>Germano stress interface：VERIFIED CLASSICAL INDEX AUDITED</p>'
            '<p>finite witness：COEFFICIENTWISE ONLY</p>'
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
            '<h2>有符号三阶界面、压力分量与精确的下一层余项</h2>'
            f'<p><img src="/assets/r073v/{FIGURE_ID}.svg" '
            'alt="R0.73V signed third-order heat interface and exact finite witnesses"></p>'
            f'<p><a href="/assets/r073v/{FIGURE_ID}.pdf">下载矢量 PDF</a> · '
            f'<a href="/assets/r073v/{FIGURE_ID}.png">下载 600 dpi PNG</a> · '
            f'<a href="/assets/r073v/{FIGURE_ID}.svg">打开 SVG</a></p>'
            '<p>附图只展示解析恒等式与有限精确稀疏 Fourier 复算。四站点和六站点场'
            '都是光滑三角多项式；它们不是 Navier--Stokes 仿真、奇性、近奇性或爆破解。</p></section>'
        )
        boundary = (
            '        <section id="release-boundary">'
            '<div class="section-no">B / Exact release boundary</div>'
            '<h2>经典不等式、本地综合和开放问题分别列示</h2>'
            f'<p>{html.escape(CLOSED_LEDGER)}</p>'
            f'<p>{html.escape(FINITE_LEDGER)}</p>'
            f'<p>{html.escape(OPEN_LEDGER)}</p>'
            '<p>压缩提升 <code>χ_s</code> 精确填入二次张量切向量的有符号三次槽；'
            '透明的 Germano 分解还需要速度三阶累积量、压力–速度、压力–应变与梯度协方差。'
            '已证临界行假设经典强范数，压力–应变的无导数临界行仍然开放。'
            f'{html.escape(EXACT_SCOPE_BOUNDARY_ZH)} NOT CLAY。</p></section>'
        )
        reproduction = (
            '        <section id="reproduce"><div class="section-no">R / Reproduction</div>'
            '<h2>证明、文献、有限证书和附图入口</h2>'
            '<p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073v_signed_third_order_heat_lift.md">analytic derivation</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073v_primary_literature_audit.md">primary literature audit</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/'
            'research/certificates/r073v">finite exact package</a></p>'
            '<p><a href="/research/r073v/r073v_figure_source_audit.md">figure source audit</a> · '
            '<a href="/research/r073v/r073v_figure_source_reaudit.md">figure source re-audit</a></p>'
            f'<p><a href="/assets/r073v/{FIGURE_ID}.pdf">journal figure PDF</a> · '
            '<a href="/notes/r0-73v.pdf">synchronized note PDF</a> · '
            '<a href="/recap-r0-61-r0-73v.html">138-node cumulative recap</a> · '
            '<a href="/recap-r0-61-r0-73v.pdf">synchronized recap PDF</a></p></section>'
        )
        return "      <article>\n" + body + "\n" + figure + "\n" + boundary + "\n" + reproduction + "\n      </article>"

    @property
    def home_card(self) -> str:
        return (
            '          <div class="task-one" id="r073v" data-release="r073v" style="margin-top:2rem">\n'
            f'            <p class="eyebrow">研究笔记 R0.73V · {html.escape(self.date)}</p>'
            f'<h3>{html.escape(self.public_title_zh)}</h3>\n'
            f'            <p>{html.escape(self.home_zh)}</p>\n'
            f'            <p><strong>闭合边界：</strong>{html.escape(CLOSED_LEDGER)}</p>\n'
            f'            <p><strong>开放边界：</strong>{html.escape(OPEN_LEDGER)}。NOT CLAY。</p>\n'
            f'            <p>{html.escape(EXACT_SCOPE_BOUNDARY_ZH)}</p>\n'
            '            <p><a href="/notes/r0-73v.html"><strong>阅读 R0.73V 研究笔记 →</strong></a>'
            '<br><a href="/notes/r0-73v.pdf">下载同步 PDF</a> · '
            f'<a href="/assets/r073v/{FIGURE_ID}.pdf">下载期刊附图 PDF</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073v_signed_third_order_heat_lift.md">查看解析证明</a> · '
            '<a href="/recap-r0-61-r0-73v.html">打开累计回顾</a></p>\n'
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
            f'{html.escape(OPEN_LEDGER)}。{html.escape(EXACT_SCOPE_BOUNDARY_ZH)} NOT CLAY。</p>'
            '<div class="links"><a href="/notes/r0-73v.html">R0.73V</a>'
            f'<a href="/assets/r073v/{FIGURE_ID}.pdf">R0.73V 附图</a>'
            '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/'
            'research/certificates/r073v">R0.73V 有限证书</a></div></article>'
        )

    @property
    def literature_update(self) -> str:
        return (
            '<span class="route-r073v-deck-update">'
            + _inline(self.literature_zh)
            + ' signed heat lift=INTERNAL_EXACT_AUDITED；'
            'pressure-aware third-order interface=EXACT_OR_CLASSICAL；'
            'coefficientwise finite witness=SEALED；minimality / hierarchy no-go=NOT_ESTABLISHED；'
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
        raise CanonicalSourceError("unterminated display math in R0.73V report")
    if in_code:
        raise CanonicalSourceError("unterminated code fence in R0.73V report")
    return "".join(output)


def _sections(report: str) -> tuple[ReportSection, ...]:
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", report))
    if len(matches) != 9:
        raise CanonicalSourceError(f"R0.73V report must contain 9 sections, found {len(matches)}")
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
    path = root / "research/certificates/r073v/manifest.json"
    if not path.is_file() or path.is_symlink():
        return False, "finite-certificate-manifest-missing"
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False, "finite-certificate-manifest-invalid"
    final = (
        manifest.get("schemaVersion") == "r073v-signed-third-order-exact-manifest-v1"
        and manifest.get("release") == RELEASE
        and manifest.get("status") == "sealed"
        and manifest.get("finalSeal") is True
        and manifest.get("sourceCommitAssigned") is True
        and manifest.get("sourceCommit")
        == "7c445c522a241bdc8b867b6fce0f0fed9b82e97d"
        and manifest.get("allPrerequisiteChecksPass") is True
        and manifest.get("checkInventory") == {
            "exact": 66, "required": 66, "twoPathComparisons": 2,
        }
        and manifest.get("inventory") == {
            "boundFileCount": 10,
            "generatedFileCount": 4,
            "packageFileCount": 12,
            "sha256SumsLineCount": 11,
            "sourceFileCount": 8,
        }
        and manifest.get("scopeFlags", {}).get("coefficientwiseNonRecoveryOnly") is True
        and manifest.get("scopeFlags", {}).get("notClay") is True
        and manifest.get("scopeFlags", {}).get("ordinaryTranslationPath")
        == "LOCAL_DIRECT_NO_DGX"
        and isinstance(manifest.get("files"), list)
        and len(manifest["files"]) == 10
        and isinstance(manifest.get("sourceBindings"), list)
        and len(manifest["sourceBindings"]) == 8
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
    validation_path = root / FIGURE_SOURCE_RELATIVE / "validation.json"
    try:
        validation = json.loads(validation_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, UnicodeDecodeError, json.JSONDecodeError):
        return False, "formal-figure-validation-missing-or-invalid"
    seal = manifest.get("seal")
    qa = manifest.get("qa")
    passed = validation.get("passed")
    required = validation.get("required")
    final = (
        manifest.get("schemaVersion") == "research-figure-manifest-v1"
        and manifest.get("figureSchemaVersion")
        == "r073v-signed-third-order-interface-manifest-v1"
        and manifest.get("figureId") == FIGURE_ID
        and manifest.get("status") == "formal"
        and manifest.get("publicationStatus") == "staged"
        and isinstance(seal, dict)
        and seal.get("figureSourceCommitAssigned") is True
        and seal.get("requiresParentFigureSourceCommitFinalReseal") is False
        and seal.get("figureSourceCommit")
        == "f94915332ff405ae723711e8041acc2af07e896b"
        and seal.get("state") == "formal-figure-source-seal"
        and isinstance(qa, dict)
        and qa.get("status") == "passed"
        and qa.get("validationChecks") == required
        and validation.get("schemaVersion")
        == "r073v-signed-third-order-interface-validation-v1"
        and validation.get("status") == "PASS"
        and isinstance(required, int) and required > 0
        and passed == required
        and isinstance(validation.get("checks"), list)
        and len(validation["checks"]) == required
        and all(row.get("pass") is True for row in validation["checks"])
    )
    return final, "formal-figure-final-seal-pending" if not final else ""


def load_release_content(root: Path | None = None) -> ReleaseContent:
    source_root = (root or Path(os.environ.get(
        "R073V_RELEASE_ROOT", Path(__file__).resolve().parents[1]
    ))).resolve()
    texts = {relative: _regular_text(source_root, relative) for relative in CANONICAL_SOURCE_PATHS}
    report = texts[REPORT_SOURCE]
    dictionary = texts[DICTIONARY_SOURCE]
    combined = "\n".join(texts.values())
    combined_compact = re.sub(r"\s+", " ", combined)
    combined_nowhitespace = re.sub(r"\s+", "", combined)

    report_title = _one(r"(?m)^#\s+(.+?)\s*$", report, "report H1")
    if report_title != RELEASE_TITLE_EN:
        raise CanonicalSourceError("R0.73V report title drift: " + report_title)
    public_title = _one(r"(?m)^\*\*Public title \(zh\):\*\*\s*(.+?)\s*$", report, "public title")
    if public_title != PUBLIC_TITLE_ZH:
        raise CanonicalSourceError("R0.73V public title drift: " + public_title)
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
        r"\chi_s=\mathcalC_s-v_s\odotN_s",
        r"(\partial_s-\Delta)\chi_s",
        r"(\partial_t-\nu\partial_s)\Theta_s",
        r"L_s\kappa_{ijk,s}",
        r"Q_{i,s}=\tau_s(p,u_i)",
        r"R_{ij,s}=\tau_s(p,S_{ij})",
        r"2iq^2(1-q^2)^2",
    ):
        if formula not in combined_nowhitespace:
            raise CanonicalSourceError("canonical sources missing formula marker: " + formula)
    for phrase in PUBLIC_VOICE_BANS:
        if phrase in report:
            raise CanonicalSourceError("report source violates public voice: " + phrase)
    for flag in FORBIDDEN_CLAIM_FLAGS:
        if flag in combined_compact:
            raise CanonicalSourceError("forbidden R0.73V claim flag: " + flag)
    folded_report = report.casefold()
    for phrase in FORBIDDEN_PUBLIC_CLAIMS:
        if phrase.casefold() in folded_report:
            raise CanonicalSourceError("forbidden R0.73V public claim: " + phrase)

    parsed_sections = _sections(report)
    if len(parsed_sections) < 8:
        raise CanonicalSourceError("R0.73V report requires at least eight numbered sections")
    section_one = _prose_paragraphs(_section_body(report, 1))
    final_section_source = _section_body(report, parsed_sections[-1].number)
    final_section = _prose_paragraphs(final_section_source)
    next_block = _one(
        r"(?ms)下一阶段[^\n]*\n\n(1\..*?)(?=\n\n这条路线)",
        final_section_source,
        "two-item next-step block",
    )
    next_items = _ordered_items(next_block)
    if len(section_one) < 12 or len(final_section) < 4:
        raise CanonicalSourceError("R0.73V report lacks required public-copy paragraphs")
    if len(next_items) != 2:
        raise CanonicalSourceError(
            f"R0.73V report must contain two next-step items, found {len(next_items)}"
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
        lead_zh=section_one[9] + " " + section_one[11],
        home_zh=section_one[7] + " " + section_one[8],
        recap_zh=final_section[3].replace("、 ", "、"),
        literature_zh=final_section[0],
        next_release=NEXT_RELEASE,
        next_gate_zh="；".join(item.rstrip("；;。 ") for item in next_items) + "。",
        sections=parsed_sections,
        source_sha256=source_sha256,
        publication_ready=not failures,
        readiness_failures=tuple(dict.fromkeys(failures)),
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read and validate canonical R0.73V release content without writing."
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
        "pressureAwareSignedHeatLift": "INTERNAL_EXACT_AUDITED",
        "signedCrossCovarianceScalePDE": "INTERNAL_EXACT_AUDITED",
        "germanoStressEquation": "VERIFIED_CLASSICAL_INDEX_AUDITED",
        "conditionalKappaCriticalRow": "INTERNAL_CONDITIONAL_AUDITED",
        "conditionalPressureVelocityCriticalRow": "INTERNAL_CONDITIONAL_AUDITED",
        "pressureStrainCriticalRow": "OPEN",
        "signedLiftInformationTheoreticMinimality": "NOT_ESTABLISHED",
        "fullThirdCumulantStateNonAutonomy": "NOT_ESTABLISHED",
        "fourthOrderNonClosure": "NOT_ESTABLISHED",
        "finiteMomentHierarchyNoGo": "NOT_ESTABLISHED",
        "arbitraryThreeDimensionalGlobalRegularity": "OPEN",
        "clayConclusion": "OPEN",
        "translationPath": "LOCAL_DIRECT_NO_DGX",
        "writes": 0,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
