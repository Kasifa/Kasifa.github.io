#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read frozen R0.73W sources and expose fail-closed reader content.

This module does not decide mathematical truth and does not write files.  It
parses the canonical report and bilingual dictionary, checks the
CLASSICAL/INTERNAL/FINITE/OPEN boundary, and supplies compact retro HTML
fragments for the later release transaction.
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


RELEASE = "R0.73W"
RELEASE_ID = "r073w"
SITE_VERSION = "1.63"
NEXT_RELEASE = "R0.73X"
PUBLIC_TITLE_ZH = "R0.73W｜带符号亚滤波 production：heat-plane 特征线、能量类边界与精确反例"
RELEASE_TITLE_EN = "R0.73W | Signed subfilter production: heat-plane characteristics, the energy-class boundary, and exact counterexamples"
FIGURE_ID = "fig-r073w-signed-production"
FIGURE_SOURCE_RELATIVE = f"figures/r073w/{FIGURE_ID}"
FIGURE_ARCHIVE_RELATIVE = f"figures/r073w/{FIGURE_ID}"

R073V_BASELINE = {
    "latestCompletedRelease": "r073v",
    "siteVersion": "1.62",
    "publicHtmlNoteCount": 198,
    "postR060RecapNodeCount": 138,
    "nextRelease": "r073w",
    "postR070APublishedReleaseCount": 100,
    "postR070AFormalSealedReleaseCount": 76,
    "legacyFormalFigureBacklogCount": 24,
}

R073W_TARGET = {
    "latestCompletedRelease": RELEASE_ID,
    "siteVersion": SITE_VERSION,
    "publicHtmlNoteCount": 199,
    "postR060RecapNodeCount": 139,
    "nextRelease": "r073x",
    "postR070APublishedReleaseCount": 101,
    "postR070AFormalSealedReleaseCount": 77,
    "legacyFormalFigureBacklogCount": 24,
}

CANONICAL_SOURCE_PATHS = (
    "research/r073w_problem_freeze.md",
    "research/r073w_signed_production_heat_characteristic.md",
    "research/r073w_independent_analytic_audit.md",
    "research/r073w_primary_literature_audit.md",
    "research/r073w_claim_source_ledger.md",
    "research/r073w_evidence_gap_matrix.md",
    "research/r073w_finite_diagnostic_audit.md",
    "research/r073w_report-source.md",
    "research/r073w_bilingual_dictionary.md",
)
PLANNED_AUDIT_PATHS = (
    "research/r073w_figure_source_audit.md",
    "research/r073w_figure_source_reaudit.md",
)
REPORT_SOURCE = "research/r073w_report-source.md"
DICTIONARY_SOURCE = "research/r073w_bilingual_dictionary.md"

PUBLIC_VOICE_BANS = (
    "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计",
    "杀死错误想法", "颠覆性", "世界首个", "接近解决",
    "解决了千禧年", "证明了全局正则性", "原创性定理", "首次证明",
)

FORBIDDEN_CLAIM_FLAGS = (
    "gaussianStressDuhamel=INTERNAL_NOVEL",
    "gaussianStressDuhamel=NEW",
    "universalProductionSign=TRUE",
    "amplitudeIndependentQuadraticAbsorption=TRUE",
    "fixedScaleUniformEnergyClassControl=CLOSED",
    "localizedScaleCriticalControl=CLOSED",
    "arbitraryThreeDimensionalGlobalRegularity=CLOSED",
    "arbitraryThreeDimensionalGlobalRegularity=SOLVED",
    "clayConclusion=CLOSED",
    "clayConclusion=SOLVED",
    "noveltyOrPriorityClaim=TRUE",
)

FORBIDDEN_PUBLIC_CLAIMS = (
    "positive stress makes the cascade positive",
    "viscosity absorbs production",
    "energy controls the flux uniformly",
    "the Fourier mode proves blow-up",
    "new exact Gaussian stress formula",
    "near a Clay solution",
    "proves a singularity",
    "proves global regularity",
    "solves the Clay Millennium problem",
    "direct numerical simulation proves",
    "DNS proves",
    "generic turbulence is proved",
    "the exponent 1/4 is optimal",
    "正应力推出正 production",
    "粘性吸收 production",
    "能量一致控制通量",
    "Fourier 模态证明爆破",
    "新的精确 Gaussian stress 公式",
    "接近 Clay 解答",
    "证明奇性",
    "证明任意初值全局正则",
)

REQUIRED_SOURCE_MARKERS = (
    "gaussianStressDuhamel=VERIFIED_CLASSICAL_REDERIVED",
    "deviatoricProductionIdentity=VERIFIED_CLASSICAL_REDERIVED",
    "heatPlaneCharacteristicIdentity=INTERNAL_EXACT_AUDITED",
    "characteristicMeanPayment=INTERNAL_EXACT_AUDITED",
    "energyClassFixedScaleEstimate=INTERNAL_UNCONDITIONAL_AUDITED",
    "energyClassScaleIntegral=INTERNAL_UNCONDITIONAL_AUDITED",
    "centeredIncrementSplit=INTERNAL_EXACT_AUDITED",
    "traceFluxCancellation=INTERNAL_EXACT_AUDITED",
    "gradientCovarianceCarreDuChamp=INTERNAL_EXACT_AUDITED",
    "weightedMeanMultiplierIdentity=INTERNAL_EXACT_AUDITED",
    "criticalHalfScaleAverage=INTERNAL_CRITICAL_AUDITED",
    "universalProductionSign=FALSE",
    "amplitudeIndependentQuadraticAbsorption=FALSE",
    "formalFiniteCertificate=SEALED_COMMIT_BOUND",
    "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX",
    "dgxUsed=false",
    "localizedScaleCriticalControl=OPEN",
    "arbitraryThreeDimensionalGlobalRegularity=OPEN",
    "clayConclusion=OPEN",
    "noveltyOrPriorityClaim=FORBIDDEN",
    "NOT CLAY",
)

CLOSED_LEDGER = (
    "CLASSICAL：gaussianStressDuhamel=VERIFIED_CLASSICAL_REDERIVED；"
    "deviatoricProductionIdentity=VERIFIED_CLASSICAL_REDERIVED。"
    "INTERNAL：heatPlaneCharacteristicIdentity=INTERNAL_EXACT_AUDITED；"
    "energyClassFixedScaleEstimate=INTERNAL_UNCONDITIONAL_AUDITED；"
    "centeredIncrementSplit=INTERNAL_EXACT_AUDITED；"
    "criticalHalfScaleAverage=INTERNAL_CRITICAL_AUDITED"
)
FINITE_LEDGER = (
    "FINITE：formalFiniteCertificate=SEALED_COMMIT_BOUND；"
    "formalFiniteCertificateChecks=56+56；primaryWitnessFrequencyRank=3；"
    "formalFigurePackage=SEALED_COMMIT_BOUND；navierStokesSimulation=NOT_RUN；"
    "directNumericalSimulation=NOT_RUN；ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX；"
    "dgxUsed=false"
)
OPEN_LEDGER = (
    "OPEN：fixedScaleUniformEnergyClassControl=OPEN；localizedScaleCriticalControl=OPEN；"
    "arbitraryThreeDimensionalGlobalRegularity=OPEN；clayConclusion=OPEN"
)
EXACT_SCOPE_BOUNDARY_ZH = (
    "有限证书是光滑三角多项式上的精确 Fourier 代数，不是 DNS、"
    "Navier--Stokes 时间仿真、generic turbulence、奇性或 blow-up 候选；"
    "它排除指定的普适单边符号律和同时刻振幅无关二次吸收，不排除非线性、"
    "时间积分或局部化估计。"
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
            '      <div><div class="eyebrow">研究笔记 R0.73W · '
            'SIGNED SUBFILTER PRODUCTION / HEAT-PLANE CHARACTERISTICS</div>\n'
            f'        <h1>{html.escape(self.public_title_zh)}</h1>\n'
            f'        <p class="lead">{html.escape(self.lead_zh)}</p></div>\n'
            '      <div class="stamp"><span class="state">状态 · R0.73W 完成</span>'
            '<strong>Signed mean payment + exact rank-three counterexample</strong>'
            f'<p>版本 R0.73W · {html.escape(self.date)}</p>'
            '<p>Gaussian stress identity：CLASSICAL / REDERIVED</p>'
            '<p>heat-plane and energy-class rows：INTERNAL AUDITED</p>'
            '<p>finite witness：FINITE EXACT / NOT DNS</p>'
            '<p>localized control / arbitrary 3D regularity：OPEN</p>'
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
            '<h2>特征线支付、能量类尺度损失与精确符号反例</h2>'
            f'<p><img src="/assets/r073w/{FIGURE_ID}.svg" '
            'alt="R0.73W heat-plane characteristic, energy-class envelopes, and exact signed-production witnesses"></p>'
            f'<p><a href="/assets/r073w/{FIGURE_ID}.pdf">下载矢量 PDF</a> · '
            f'<a href="/assets/r073w/{FIGURE_ID}.png">下载 600 dpi PNG</a> · '
            f'<a href="/assets/r073w/{FIGURE_ID}.svg">打开 SVG</a></p>'
            '<p>附图 A--B 是解析恒等式与上界形状，C--D 是精确 Fourier 代数。'
            '这些曲线不是观测、拟合、DNS、时间仿真、奇性或 blow-up 候选。</p></section>'
        )
        boundary = (
            '        <section id="release-boundary">'
            '<div class="section-no">B / Exact release boundary</div>'
            '<h2>CLASSICAL、INTERNAL、FINITE 与 OPEN 分开列示</h2>'
            f'<p>{html.escape(CLOSED_LEDGER)}</p>'
            f'<p>{html.escape(FINITE_LEDGER)}</p>'
            f'<p>{html.escape(OPEN_LEDGER)}</p>'
            f'<p>{html.escape(EXACT_SCOPE_BOUNDARY_ZH)} NOT CLAY。</p></section>'
        )
        reproduction = (
            '        <section id="reproduce"><div class="section-no">R / Reproduction</div>'
            '<h2>证明、文献、有限证书和附图入口</h2>'
            '<p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073w_signed_production_heat_characteristic.md">analytic derivation</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073w_primary_literature_audit.md">primary literature audit</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/'
            'research/certificates/r073w">two-path finite certificate</a></p>'
            '<p><a href="/research/r073w/r073w_figure_source_audit.md">figure source audit</a> · '
            '<a href="/research/r073w/r073w_figure_source_reaudit.md">figure source re-audit</a></p>'
            f'<p><a href="/assets/r073w/{FIGURE_ID}.pdf">journal figure PDF</a> · '
            '<a href="/notes/r0-73w.pdf">synchronized note PDF</a> · '
            '<a href="/recap-r0-61-r0-73w.html">139-node cumulative recap</a> · '
            '<a href="/recap-r0-61-r0-73w.pdf">synchronized recap PDF</a></p></section>'
        )
        return "      <article>\n" + body + "\n" + figure + "\n" + boundary + "\n" + reproduction + "\n      </article>"

    @property
    def home_card(self) -> str:
        return (
            '          <div class="task-one" id="r073w" data-release="r073w" style="margin-top:2rem">\n'
            f'            <p class="eyebrow">研究笔记 R0.73W · {html.escape(self.date)}</p>'
            f'<h3>{html.escape(self.public_title_zh)}</h3>\n'
            f'            <p>{html.escape(self.home_zh)}</p>\n'
            f'            <p><strong>已核验边界：</strong>{html.escape(CLOSED_LEDGER)}</p>\n'
            f'            <p><strong>有限边界：</strong>{html.escape(FINITE_LEDGER)}</p>\n'
            f'            <p><strong>开放边界：</strong>{html.escape(OPEN_LEDGER)}。NOT CLAY。</p>\n'
            f'            <p>{html.escape(EXACT_SCOPE_BOUNDARY_ZH)}</p>\n'
            '            <p><a href="/notes/r0-73w.html"><strong>阅读 R0.73W 研究笔记 →</strong></a>'
            '<br><a href="/notes/r0-73w.pdf">下载同步 PDF</a> · '
            f'<a href="/assets/r073w/{FIGURE_ID}.pdf">下载期刊附图 PDF</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073w_signed_production_heat_characteristic.md">查看解析证明</a> · '
            '<a href="/recap-r0-61-r0-73w.html">打开累计回顾</a></p>\n'
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
            '<div class="links"><a href="/notes/r0-73w.html">R0.73W</a>'
            f'<a href="/assets/r073w/{FIGURE_ID}.pdf">R0.73W 附图</a>'
            '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/'
            'research/certificates/r073w">R0.73W 有限证书</a></div></article>'
        )

    @property
    def literature_update(self) -> str:
        return (
            '<span class="route-r073w-deck-update">'
            + _inline(self.literature_zh)
            + ' Gaussian stress formula=CLASSICAL；heat-coordinate identity=INTERNAL；'
            'rank-three witness=FINITE；localized scale-critical control=OPEN；'
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


def _metadata_block(value: str, label: str) -> str:
    escaped = re.escape(label)
    return _compact(_one(
        rf"(?ms)^\*\*{escaped}:\*\*\s*(.+?)(?=\n\s*\n)",
        value,
        label,
    ))


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
        raise CanonicalSourceError("unterminated display math in R0.73W report")
    if in_code:
        raise CanonicalSourceError("unterminated code fence in R0.73W report")
    return "".join(output)


def _sections(report: str) -> tuple[ReportSection, ...]:
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", report))
    if len(matches) != 11:
        raise CanonicalSourceError(f"R0.73W report must contain 11 sections, found {len(matches)}")
    used: set[str] = set()
    sections: list[ReportSection] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(report)
        title_match = re.match(r"^(\d+)\.\s+(.+)$", match.group(1))
        if title_match is None or int(title_match.group(1)) != index + 1:
            raise CanonicalSourceError("report section numbering drift: " + match.group(1))
        title = title_match.group(2).strip()
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


def _bullet_items(section: str) -> list[str]:
    values: list[str] = []
    current: list[str] = []
    for row in section.splitlines() + [""]:
        match = re.match(r"^-\s+(.+)$", row)
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
    path = root / "research/certificates/r073w/manifest.json"
    if not path.is_file() or path.is_symlink():
        return False, "finite-certificate-manifest-missing"
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False, "finite-certificate-manifest-invalid"
    source_commit = manifest.get("sourceCommit")
    final = (
        manifest.get("schemaVersion") == "r073w-signed-production-exact-manifest-v1"
        and manifest.get("release") == RELEASE
        and manifest.get("status") == "SEALED_COMMIT_BOUND"
        and manifest.get("finalSeal") is True
        and manifest.get("sourceCommitAssigned") is True
        and source_commit == "b9f3b3943df1e2abf6abc2f51c1fb25d1f1e8440"
        and manifest.get("allPrerequisiteChecksPass") is True
        and manifest.get("primaryWitnessKey") == "rankThreeExtension"
        and manifest.get("checkInventory") == {
            "exactPerPath": 56, "requiredPerPath": 56, "twoPathComparisons": 2,
        }
        and manifest.get("inventory") == {
            "boundFileCount": 11,
            "generatedFileCount": 4,
            "packageFileCount": 13,
            "sha256SumsLineCount": 12,
            "sourceFileCount": 9,
        }
        and manifest.get("scopeFlags", {}).get("primaryWitnessFrequencyRank") == 3
        and manifest.get("scopeFlags", {}).get("notClay") is True
        and manifest.get("scopeFlags", {}).get("ordinaryTranslationPath")
        == "LOCAL_DIRECT_NO_DGX"
        and manifest.get("scopeFlags", {}).get("dgxUsed") is False
        and isinstance(manifest.get("files"), list)
        and len(manifest["files"]) == 11
        and isinstance(manifest.get("sourceBindings"), list)
        and len(manifest["sourceBindings"]) == 9
        and isinstance(manifest.get("sourceCommitBindings"), list)
        and len(manifest["sourceCommitBindings"]) == 9
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
        and manifest.get("figureSchemaVersion") == "r073w-signed-production-manifest-v1"
        and manifest.get("figureId") == FIGURE_ID
        and manifest.get("status") == "formal"
        and manifest.get("publicationStatus") == "staged"
        and isinstance(seal, dict)
        and seal.get("figureSourceCommitAssigned") is True
        and seal.get("requiresParentFigureSourceCommitFinalReseal") is False
        and re.fullmatch(r"[0-9a-f]{40}", str(seal.get("figureSourceCommit"))) is not None
        and seal.get("state") == "formal-figure-source-seal"
        and isinstance(qa, dict)
        and qa.get("status") == "passed"
        and qa.get("validationChecks") == required
        and validation.get("schemaVersion") == "r073w-signed-production-validation-v1"
        and validation.get("status") == "PASS"
        and isinstance(required, int) and required > 0
        and passed == required
        and isinstance(validation.get("checks"), list)
        and len(validation["checks"]) == required
        and all(isinstance(row, dict) and row.get("pass") is True for row in validation["checks"])
    )
    return final, "formal-figure-final-seal-pending" if not final else ""


def load_release_content(root: Path | None = None) -> ReleaseContent:
    source_root = (root or Path(os.environ.get(
        "R073W_RELEASE_ROOT", Path(__file__).resolve().parents[1]
    ))).resolve()
    texts = {relative: _regular_text(source_root, relative) for relative in CANONICAL_SOURCE_PATHS}
    report = texts[REPORT_SOURCE]
    dictionary = texts[DICTIONARY_SOURCE]
    combined = "\n".join(texts.values())
    combined_compact = re.sub(r"\s+", " ", combined)
    combined_nowhitespace = re.sub(r"\s+", "", combined)

    report_title = _one(r"(?m)^#\s+(.+?)\s*$", report, "report H1")
    if report_title != RELEASE_TITLE_EN:
        raise CanonicalSourceError("R0.73W report title drift: " + report_title)
    public_title = _metadata_block(report, "Public title (zh)")
    if public_title != PUBLIC_TITLE_ZH:
        raise CanonicalSourceError("R0.73W public title drift: " + public_title)
    date = _metadata_block(report, "Date")
    status = _metadata_block(report, "Status")
    dictionary_release_title = _metadata_block(dictionary, "Release title")
    dictionary_public_title = _metadata_block(dictionary, "Public title (zh)")
    if dictionary_release_title != report_title:
        raise CanonicalSourceError("bilingual release title differs from report H1")
    if dictionary_public_title != public_title:
        raise CanonicalSourceError("bilingual public title differs from report public title")

    for marker in REQUIRED_SOURCE_MARKERS:
        if marker not in combined_compact:
            raise CanonicalSourceError("canonical sources missing boundary marker: " + marker)
    if not any(
        marker in combined_compact
        for marker in (
            "formalFigurePackage=PENDING",
            "formalFigurePackage=SEALED_COMMIT_BOUND",
            "formalFigurePackage=PASS",
        )
    ):
        raise CanonicalSourceError("canonical sources missing formal-figure state marker")
    for formula in (
        r"\Pi_s=-\tau_s:\nablav_s",
        r"(\partial_t-\nu\partial_s)e_s",
        r"\Pi_s=\partial_jK_{j,s}+\mathscrS_s",
        r"s^{-1/2}\langle\Pi_s\rangle",
        r"R(x,y,z)=\big",
        r"{A^3\over4}q^2(1-q^2)",
        r"{Aq^2\over2\nu(13+12q^2+10q^4+4q^6)}",
    ):
        if formula not in combined_nowhitespace:
            raise CanonicalSourceError("canonical sources missing formula marker: " + formula)
    for phrase in PUBLIC_VOICE_BANS:
        if phrase in report:
            raise CanonicalSourceError("report source violates public voice: " + phrase)
    for flag in FORBIDDEN_CLAIM_FLAGS:
        if flag in combined_compact:
            raise CanonicalSourceError("forbidden R0.73W claim flag: " + flag)
    folded_report = report.casefold()
    for phrase in FORBIDDEN_PUBLIC_CLAIMS:
        if phrase.casefold() in folded_report:
            raise CanonicalSourceError("forbidden R0.73W public claim: " + phrase)

    parsed_sections = _sections(report)
    section_one = _prose_paragraphs(_section_body(report, 1))
    literature_section = _prose_paragraphs(_section_body(report, 8))
    value_section = _prose_paragraphs(_section_body(report, 9))
    next_section_source = _section_body(report, 10)
    next_section = _prose_paragraphs(next_section_source)
    next_items = _bullet_items(next_section_source)
    if len(section_one) < 20:
        raise CanonicalSourceError("R0.73W direct-result section lacks required public-copy paragraphs")
    if len(literature_section) != 3 or len(value_section) != 3 or len(next_section) != 2:
        raise CanonicalSourceError("R0.73W summary-section paragraph inventory drift")
    if len(next_items) != 5:
        raise CanonicalSourceError(f"R0.73W next-step list must contain five items, found {len(next_items)}")

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
    if "formalFigurePackage=PENDING" in combined_compact:
        failures.append("canonical-ledger-formal-figure-pending")
    if "publicReleaseTransaction=PENDING" in combined_compact:
        failures.append("canonical-ledger-public-release-pending")
    if "待 immutable pin" in report or "当前未封印计算中" in report:
        failures.append("reader-facing-certificate-wording-pending")

    source_sha256 = {
        relative: hashlib.sha256((source_root / relative).read_bytes()).hexdigest()
        for relative in texts
    }
    return ReleaseContent(
        report_title=report_title,
        public_title_zh=public_title,
        release_title_en=report_title,
        date=date,
        status=status,
        lead_zh=section_one[6] + " " + section_one[8] + " " + section_one[19],
        home_zh=section_one[17] + " " + section_one[18] + " " + section_one[19],
        recap_zh=" ".join(value_section),
        literature_zh=literature_section[2],
        next_release=NEXT_RELEASE,
        next_gate_zh=(
            next_section[0]
            + " "
            + "；".join(item.rstrip("；;。 ") for item in next_items)
            + "。"
        ),
        sections=parsed_sections,
        source_sha256=source_sha256,
        publication_ready=not failures,
        readiness_failures=tuple(dict.fromkeys(failures)),
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read and validate canonical R0.73W release content without writing."
    )
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if not args.check_only:
        parser.print_help()
        return
    content = load_release_content()
    figure_pending = any(
        failure.startswith(("formal-figure-", "planned-audit-missing:"))
        or failure == "canonical-ledger-formal-figure-pending"
        for failure in content.readiness_failures
    )
    print(json.dumps({
        "release": RELEASE,
        "siteVersion": SITE_VERSION,
        "title": content.release_title_en,
        "publicTitleZh": content.public_title_zh,
        "canonicalSources": len(content.source_sha256),
        "canonicalSourcesPlanned": len(CANONICAL_SOURCE_PATHS) + len(PLANNED_AUDIT_PATHS),
        "sections": len(content.sections),
        "baselineAccounting": R073V_BASELINE,
        "targetAccounting": R073W_TARGET,
        "publicationReady": content.publication_ready,
        "readinessFailures": list(content.readiness_failures),
        "gaussianStressDuhamel": "VERIFIED_CLASSICAL_REDERIVED",
        "heatPlaneCharacteristicIdentity": "INTERNAL_EXACT_AUDITED",
        "energyClassFixedScaleEstimate": "INTERNAL_UNCONDITIONAL_AUDITED",
        "formalFiniteCertificate": "SEALED_COMMIT_BOUND",
        "primaryWitnessKey": "rankThreeExtension",
        "formalFigurePackage": (
            "PENDING" if figure_pending else "SEALED_COMMIT_BOUND"
        ),
        "localizedScaleCriticalControl": "OPEN",
        "arbitraryThreeDimensionalGlobalRegularity": "OPEN",
        "clayConclusion": "OPEN",
        "navierStokesSimulation": "NOT_RUN",
        "directNumericalSimulation": "NOT_RUN",
        "translationPath": "LOCAL_DIRECT_NO_DGX",
        "dgxUsed": False,
        "writes": 0,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
