#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read frozen R0.73X sources and expose fail-closed reader content.

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


RELEASE = "R0.73X"
RELEASE_ID = "r073x"
SITE_VERSION = "1.64"
NEXT_RELEASE = "R0.73Y"
PUBLIC_TITLE_ZH = "R0.73X｜带显式外部尾项的局部热账本：Gaussian 速度控制、代数压力尾与未闭合 coercivity 桥"
RELEASE_TITLE_EN = "R0.73X | Localized heat ledgers with explicit exterior tails: Gaussian velocity control, algebraic pressure tails, and the open coercivity bridge"
FIGURE_ID = "fig-r073x-exterior-tail-ledger"
FIGURE_SOURCE_RELATIVE = f"figures/r073x/{FIGURE_ID}"
FIGURE_ARCHIVE_RELATIVE = f"figures/r073x/{FIGURE_ID}"

R073W_BASELINE = {
    "latestCompletedRelease": "r073w",
    "siteVersion": "1.63",
    "publicHtmlNoteCount": 199,
    "postR060RecapNodeCount": 139,
    "nextRelease": "r073x",
    "postR070APublishedReleaseCount": 101,
    "postR070AFormalSealedReleaseCount": 77,
    "legacyFormalFigureBacklogCount": 24,
}

R073X_TARGET = {
    "latestCompletedRelease": RELEASE_ID,
    "siteVersion": SITE_VERSION,
    "publicHtmlNoteCount": 200,
    "postR060RecapNodeCount": 140,
    "nextRelease": "r073y",
    "postR070APublishedReleaseCount": 102,
    "postR070AFormalSealedReleaseCount": 78,
    "legacyFormalFigureBacklogCount": 24,
}

CANONICAL_SOURCE_PATHS = (
    "research/r073x_problem_freeze.md",
    "research/r073x_primary_literature_audit.md",
    "research/r073x_localized_heat_characteristic.md",
    "research/r073x_finite_diagnostic_design.md",
    "research/r073x_finite_fourier_harness_report.md",
    "research/r073x_gaussian_velocity_tail_proof.md",
    "research/r073x_gaussian_tail_certificate_report.md",
    "research/r073x_gaussian_tail_independent_audit.md",
    "research/r073x_exterior_tail_counterexample_audit.md",
    "research/r073x_pressure_tail_primary_source_ledger.md",
    "research/r073x_exterior_tail_freeze.md",
    "research/r073x_pressure_tail_independent_audit.md",
    "research/r073x_claim_state_update.md",
    "research/r073x_release_candidate_manifest.json",
    "research/r073x_claim_source_ledger.md",
    "research/r073x_evidence_gap_matrix.md",
    "research/r073x_report-source.md",
    "research/r073x_bilingual_dictionary.md",
)
PLANNED_AUDIT_PATHS = (
    "research/r073x_figure_source_audit.md",
    "research/r073x_figure_source_reaudit.md",
)
REPORT_SOURCE = "research/r073x_report-source.md"
DICTIONARY_SOURCE = "research/r073x_bilingual_dictionary.md"

PUBLIC_VOICE_BANS = (
    "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计",
    "杀死错误想法", "颠覆性", "世界首个", "接近解决",
    "解决了千禧年", "证明了全局正则性", "原创性定理", "首次证明",
)

FORBIDDEN_CLAIM_FLAGS = (
    "pressureExteriorTailSizeLemma=COERCIVE",
    "positiveScaleAbsoluteSize=SMALL",
    "compactCutoffQuadraticAbsorption=CLOSED",
    "signedToAbsoluteCoercivity=CLOSED",
    "exteriorFunctionalLocallyControlled=CLOSED",
    "weightedTentCarlesonControl=CLOSED",
    "suitableWeakZeroScaleEndpoint=CLOSED",
    "epsilonRegularity=CLOSED",
    "translatedPacketCounterexample=NSE",
    "associatedPressureCounterexample=PROVED",
    "arbitraryThreeDimensionalGlobalRegularity=CLOSED",
    "arbitraryThreeDimensionalGlobalRegularity=SOLVED",
    "clayConclusion=CLOSED",
    "clayConclusion=SOLVED",
    "noveltyOrPriorityClaim=TRUE",
)

FORBIDDEN_PUBLIC_CLAIMS = (
    "the exterior functional is locally small",
    "Gaussian pressure decay closes the estimate",
    "the positive-scale size lemma is coercive",
    "the packet is a Navier--Stokes counterexample",
    "the harmonic probe settles compact cutoffs",
    "weighted tent control is proved",
    "near a Clay solution",
    "proves a singularity",
    "proves global regularity",
    "solves the Clay Millennium problem",
    "direct numerical simulation proves",
    "DNS proves",
    "generic turbulence is proved",
    "外部 functional 自动局部小",
    "Gaussian 压力尾关闭估计",
    "positive-scale size lemma 给出 coercivity",
    "packet 是 Navier--Stokes 反例",
    "harmonic probe 解决 compact cutoff",
    "weighted tent 已证明",
    "接近 Clay 解答",
    "证明奇性",
    "证明任意初值全局正则",
)

REQUIRED_SOURCE_MARKERS = (
    "localizedHeatCharacteristicLedger=PROVED_WITH_STATED_SOLUTION_CLASS",
    "centeredIncrementCutoffSplit=EXACT_AND_FINITE_CHECKED",
    "gaussianVelocityTailLemma=INDEPENDENT_AUDIT_PASS",
    "pressureExteriorTailSizeLemma=PASS_AT_POSITIVE_SCALE",
    "positiveScaleAbsoluteSize=PROVED",
    "fixedHarmonicProbeQuadraticAbsorption=REFUTED_EXACTLY",
    "compactCutoffQuadraticAbsorption=OPEN",
    "translatedPacketCounterexample=FUNCTIONAL_ONLY_NOT_NSE",
    "associatedPressureCounterexample=NOT_CLAIMED",
    "signedToAbsoluteCoercivity=OPEN",
    "exteriorFunctionalLocallyControlled=OPEN",
    "weightedTentCarlesonControl=OPEN",
    "suitableWeakZeroScaleEndpoint=OPEN",
    "epsilonRegularity=OPEN",
    "formalEvidenceCertificate=SOURCE_COMMIT_BOUND_PACKAGE_HASH_SEALED",
    "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX",
    "dgxUsed=false",
    "arbitraryThreeDimensionalGlobalRegularity=OPEN",
    "clayConclusion=OPEN",
    "noveltyOrPriorityClaim=FORBIDDEN",
    "NOT CLAY",
)

CLOSED_LEDGER = (
    "PROVED：localizedHeatCharacteristicLedger=PROVED_WITH_STATED_SOLUTION_CLASS；"
    "gaussianVelocityTailLemma=INDEPENDENT_AUDIT_PASS；"
    "pressureExteriorTailSizeLemma=PASS_AT_POSITIVE_SCALE；"
    "positiveScaleAbsoluteSize=PROVED"
)
FINITE_LEDGER = (
    "FINITE：gaussianTailCertificate=INDEPENDENT_SECOND_PRODUCER_PASS；"
    "finiteHarmonicProbe=REFUTED_EXACTLY；"
    "formalEvidenceCertificate=SOURCE_COMMIT_BOUND_PACKAGE_HASH_SEALED；"
    "formalFigurePackage=SEALED_COMMIT_BOUND；navierStokesSimulation=NOT_RUN；"
    "directNumericalSimulation=NOT_RUN；ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX；"
    "dgxUsed=false"
)
OPEN_LEDGER = (
    "OPEN：compactCutoffQuadraticAbsorption=OPEN；signedToAbsoluteCoercivity=OPEN；"
    "weightedTentCarlesonControl=OPEN；suitableWeakZeroScaleEndpoint=OPEN；"
    "epsilonRegularity=OPEN；"
    "arbitraryThreeDimensionalGlobalRegularity=OPEN；clayConclusion=OPEN"
)
EXACT_SCOPE_BOUNDARY_ZH = (
    "本节证明 finite, scale-compatible absolute size at positive heat scale，"
    "不证明 smallness、absorption、coercivity、weighted tent、s=0 endpoint 或 epsilon regularity；"
    "translated packet 是 p=mu=0 的静态 functional 见证，通常不是 NSE trajectory，"
    "不反驳 associated-pressure 或 NSE-only estimates。"
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
            '      <div><div class="eyebrow">研究笔记 R0.73X · '
            'EXPLICIT EXTERIOR TAILS / POSITIVE-SCALE SIZE</div>\n'
            f'        <h1>{html.escape(self.public_title_zh)}</h1>\n'
            f'        <p class="lead">{html.escape(self.lead_zh)}</p></div>\n'
            '      <div class="stamp"><span class="state">状态 · R0.73X 完成</span>'
            '<strong>Gaussian velocity tail + algebraic pressure tail</strong>'
            f'<p>版本 R0.73X · {html.escape(self.date)}</p>'
            '<p>Gaussian velocity-tail lemma：INDEPENDENT AUDIT PASS</p>'
            '<p>pressure/exterior size：POSITIVE-SCALE PASS</p>'
            '<p>static packet：FUNCTIONAL ONLY / NOT NSE</p>'
            '<p>coercivity / weighted tent / s=0 / epsilon regularity：OPEN</p>'
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
            '<h2>Gaussian heat 尾、代数 pressure 尾与 open coercivity bridge</h2>'
            f'<p><img src="/assets/r073x/{FIGURE_ID}.svg" '
            'alt="R0.73X exterior-tail ledger comparing Gaussian heat weights, algebraic harmonic-pressure weights, and the open signed-to-absolute bridge"></p>'
            f'<p><a href="/assets/r073x/{FIGURE_ID}.pdf">下载矢量 PDF</a> · '
            f'<a href="/assets/r073x/{FIGURE_ID}.png">下载 600 dpi PNG</a> · '
            f'<a href="/assets/r073x/{FIGURE_ID}.svg">打开 SVG</a></p>'
            '<p>附图只呈现冻结定义、解析 kernel weights、certificate rows 与明确的 OPEN bridge。'
            '它不是观测、拟合、DNS、Navier--Stokes 时间仿真、regularity theorem 或 blow-up 候选。</p></section>'
        )
        boundary = (
            '        <section id="release-boundary">'
            '<div class="section-no">B / Exact release boundary</div>'
            '<h2>PROVED、FINITE 与 OPEN 分开列示</h2>'
            f'<p>{html.escape(CLOSED_LEDGER)}</p>'
            f'<p>{html.escape(FINITE_LEDGER)}</p>'
            f'<p>{html.escape(OPEN_LEDGER)}</p>'
            f'<p>{html.escape(EXACT_SCOPE_BOUNDARY_ZH)} NOT CLAY。</p></section>'
        )
        reproduction = (
            '        <section id="reproduce"><div class="section-no">R / Reproduction</div>'
            '<h2>证明、审计、证书和附图入口</h2>'
            '<p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073x_claim_state_update.md">claim-state update</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073x_exterior_tail_freeze.md">exterior-tail proof</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073x_pressure_tail_independent_audit.md">pressure audit</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/'
            'research/certificates/r073x">formal certificate archive</a></p>'
            '<p><a href="/research/r073x/r073x_figure_source_audit.md">figure source audit</a> · '
            '<a href="/research/r073x/r073x_figure_source_reaudit.md">figure source re-audit</a></p>'
            f'<p><a href="/assets/r073x/{FIGURE_ID}.pdf">journal figure PDF</a> · '
            '<a href="/notes/r0-73x.pdf">synchronized note PDF</a> · '
            '<a href="/recap-r0-61-r0-73x.html">140-node cumulative recap</a> · '
            '<a href="/recap-r0-61-r0-73x.pdf">synchronized recap PDF</a></p></section>'
        )
        return "      <article>\n" + body + "\n" + figure + "\n" + boundary + "\n" + reproduction + "\n      </article>"

    @property
    def home_card(self) -> str:
        return (
            '          <div class="task-one" id="r073x" data-release="r073x" style="margin-top:2rem">\n'
            f'            <p class="eyebrow">研究笔记 R0.73X · {html.escape(self.date)}</p>'
            f'<h3>{html.escape(self.public_title_zh)}</h3>\n'
            f'            <p>{html.escape(self.home_zh)}</p>\n'
            f'            <p><strong>已核验边界：</strong>{html.escape(CLOSED_LEDGER)}</p>\n'
            f'            <p><strong>有限边界：</strong>{html.escape(FINITE_LEDGER)}</p>\n'
            f'            <p><strong>开放边界：</strong>{html.escape(OPEN_LEDGER)}。NOT CLAY。</p>\n'
            f'            <p>{html.escape(EXACT_SCOPE_BOUNDARY_ZH)}</p>\n'
            '            <p><a href="/notes/r0-73x.html"><strong>阅读 R0.73X 研究笔记 →</strong></a>'
            '<br><a href="/notes/r0-73x.pdf">下载同步 PDF</a> · '
            f'<a href="/assets/r073x/{FIGURE_ID}.pdf">下载期刊附图 PDF</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073x_claim_state_update.md">查看 claim-state update</a> · '
            '<a href="/recap-r0-61-r0-73x.html">打开累计回顾</a></p>\n'
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
            '<div class="links"><a href="/notes/r0-73x.html">R0.73X</a>'
            f'<a href="/assets/r073x/{FIGURE_ID}.pdf">R0.73X 附图</a>'
            '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/'
            'research/certificates/r073x">R0.73X 证书</a></div></article>'
        )

    @property
    def literature_update(self) -> str:
        return (
            '<span class="route-r073x-deck-update">'
            + _inline(self.literature_zh)
            + ' Gaussian velocity tail=INTERNAL AUDITED；pressure tail=ALGEBRAIC；'
            'positive-scale size=PROVED；signed-to-absolute coercivity=OPEN；'
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
        raise CanonicalSourceError("unterminated display math in R0.73X report")
    if in_code:
        raise CanonicalSourceError("unterminated code fence in R0.73X report")
    return "".join(output)


def _sections(report: str) -> tuple[ReportSection, ...]:
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", report))
    if len(matches) != 11:
        raise CanonicalSourceError(f"R0.73X report must contain 11 sections, found {len(matches)}")
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
    path = root / "research/certificates/r073x/manifest.json"
    if not path.is_file() or path.is_symlink():
        return False, "formal-certificate-manifest-missing"
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False, "formal-certificate-manifest-invalid"
    certificate_root = path.parent
    expected_names = {
        "README.md", "SHA256SUMS", "audit-checklist.json", "claim-boundary.md",
        "command.txt", "contract.json", "fourier-producer.py", "fourier-report.md",
        "fourier-results.json", "gaussian-independent-audit.md",
        "gaussian-producer.py", "gaussian-report.md", "gaussian-results.json",
        "manifest.json", "requirements.txt", "seal_package.py",
    }
    actual_names = {
        item.name for item in certificate_root.iterdir()
        if item.is_file() and not item.is_symlink()
        and re.search(r" \d+(?=\.[^.]+$|$)", item.name) is None
    }
    source_commit = manifest.get("sourceCommit")
    package_bound = manifest.get("packageCommitBound")
    scope = manifest.get("scope")
    bindings = manifest.get("sourceBindings")
    bound_rows = manifest.get("files")
    final = (
        manifest.get("schemaVersion") == "r073x-formal-evidence-manifest-v1"
        and manifest.get("release") == RELEASE
        and manifest.get("status") == "SOURCE_COMMIT_BOUND_PACKAGE_HASH_SEALED"
        and source_commit == "958b6b4216f6914a5d42f7712b6bc9b218caf801"
        and package_bound in (False, True)
        and (
            package_bound is False
            or re.fullmatch(r"[0-9a-f]{40}", str(manifest.get("packageCommit")))
            is not None
        )
        and manifest.get("inventory") == {
            "packageFileCount": 16,
            "boundFileCount": 14,
            "sha256SumsLineCount": 15,
            "archiveEvidenceFiles": 7,
        }
        and actual_names == expected_names
        and isinstance(scope, dict)
        and scope.get("notClay") is True
        and scope.get("clayConclusion") == "OPEN"
        and scope.get("compactCutoffAbsorption") == "OPEN"
        and scope.get("weightedTentCarleson") == "OPEN"
        and scope.get("navierStokesSimulation") is False
        and isinstance(bindings, list)
        and len(bindings) == 7
        and all(
            isinstance(row, dict)
            and isinstance(row.get("canonicalPath"), str)
            and re.fullmatch(r"[0-9a-f]{64}", str(row.get("sha256"))) is not None
            and re.fullmatch(r"[0-9a-f]{40}", str(row.get("gitBlobObjectId"))) is not None
            for row in bindings
        )
        and isinstance(bound_rows, list)
        and len(bound_rows) == 14
    )
    return final, "formal-certificate-source-bound-hash-seal-pending" if not final else ""


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
    contract_path = root / FIGURE_SOURCE_RELATIVE / "contract.json"
    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, UnicodeDecodeError, json.JSONDecodeError):
        return False, "formal-figure-contract-missing-or-invalid"
    seal = manifest.get("seal")
    qa = manifest.get("qa")
    checks = validation.get("checks")
    required = validation.get(
        "required", validation.get("checksRequired", validation.get("checkCount"))
    )
    passed = validation.get("passed", validation.get("checksPassed"))
    if passed is None and validation.get("allChecksPass") is True and isinstance(checks, list):
        passed = len(checks)
    expected_bound_paths = {
        f"{FIGURE_SOURCE_RELATIVE}/{name}" for name in (
            "README.md", "caption.md", "chart-contract-and-source-data.md",
            "command.txt", "config.json", "contract.json", "plot.py",
            "qa-protocol.md", "requirements.txt", "validate.py",
            "environment.json", "figure.pdf", "figure.png", "figure.svg",
            "progress.ndjson", "qa-final-size.png", "qa-grayscale.png",
            "qa-pdf.png", "resource-log.ndjson", "results.json",
            "source-data.csv",
        )
    }
    bindings = seal.get("figureSourceBindings") if isinstance(seal, dict) else None
    bound_paths = {
        row.get("path") for row in bindings
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    } if isinstance(bindings, list) else set()
    final = (
        manifest.get("schemaVersion") == "research-figure-manifest-v1"
        and manifest.get("figureSchemaVersion") == "r073x-exterior-tail-ledger-manifest-v1"
        and contract.get("schemaVersion") == "r073x-exterior-tail-ledger-contract-v1"
        and contract.get("sourceCommit") == "958b6b4216f6914a5d42f7712b6bc9b218caf801"
        and contract.get("release") == RELEASE
        and manifest.get("figureId") == FIGURE_ID
        and manifest.get("release") == RELEASE
        and manifest.get("status") == "formal"
        and manifest.get("publicationStatus") == "staged"
        and isinstance(seal, dict)
        and seal.get("figureSourceCommitAssigned") is True
        and seal.get("requiresParentFigureSourceCommitFinalReseal") is False
        and re.fullmatch(r"[0-9a-f]{40}", str(seal.get("figureSourceCommit"))) is not None
        and seal.get("state") == "formal-figure-source-seal"
        and isinstance(bindings, list)
        and len(bindings) == 21
        and len(bound_paths) == len(bindings)
        and bound_paths == expected_bound_paths
        and isinstance(qa, dict)
        and qa.get("status") == "passed"
        and qa.get("validationChecks") == required
        and validation.get("schemaVersion") == "r073x-exterior-tail-ledger-validation-v1"
        and validation.get("status") == "PASS"
        and isinstance(required, int) and required > 0
        and passed == required
        and isinstance(checks, list)
        and len(checks) == required
        and all(isinstance(row, dict) and row.get("pass") is True for row in checks)
    )
    return final, "formal-figure-final-seal-pending" if not final else ""


def load_release_content(root: Path | None = None) -> ReleaseContent:
    source_root = (root or Path(os.environ.get(
        "R073X_RELEASE_ROOT", Path(__file__).resolve().parents[1]
    ))).resolve()
    texts = {relative: _regular_text(source_root, relative) for relative in CANONICAL_SOURCE_PATHS}
    report = texts[REPORT_SOURCE]
    dictionary = texts[DICTIONARY_SOURCE]
    combined = "\n".join(texts.values())
    combined_compact = re.sub(r"\s+", " ", combined)
    combined_nowhitespace = re.sub(r"\s+", "", combined)

    report_title = _one(r"(?m)^#\s+(.+?)\s*$", report, "report H1")
    if report_title != RELEASE_TITLE_EN:
        raise CanonicalSourceError("R0.73X report title drift: " + report_title)
    public_title = _metadata_block(report, "Public title (zh)")
    if public_title != PUBLIC_TITLE_ZH:
        raise CanonicalSourceError("R0.73X public title drift: " + public_title)
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
    figure_states = (
        "formalFigurePackage=PENDING_REQUIRED",
        "formalFigurePackage=SEALED_COMMIT_BOUND",
    )
    if not any(state in combined_compact for state in figure_states):
        raise CanonicalSourceError("canonical sources missing formal-figure state marker")
    for formula in (
        r"\mathcalA_{\rmext}^{\square}",
        r"|\mathscrS_s(t,x)|\leC_0s^{-1/2}P_{2s}(|u(t)|^3)(x)",
        r"\gamma_m(\theta)=\theta^{-2}",
        r"\Lambda_R(t)=R\sum_{m\ge1}(2^mR)^{-4}",
        r"-i{k_\ellk_ik_j\over|k|^2}",
        r"\mathcalC_{\mathscrS,0,\theta}^{\rmabs,\square}",
    ):
        if formula not in combined_nowhitespace:
            raise CanonicalSourceError("canonical sources missing formula marker: " + formula)
    for phrase in PUBLIC_VOICE_BANS:
        if phrase in report:
            raise CanonicalSourceError("report source violates public voice: " + phrase)
    for flag in FORBIDDEN_CLAIM_FLAGS:
        if flag in combined_compact:
            raise CanonicalSourceError("forbidden R0.73X claim flag: " + flag)
    folded_report = report.casefold()
    for phrase in FORBIDDEN_PUBLIC_CLAIMS:
        if phrase.casefold() in folded_report:
            raise CanonicalSourceError("forbidden R0.73X public claim: " + phrase)

    parsed_sections = _sections(report)
    section_one = _prose_paragraphs(_section_body(report, 1))
    literature_section = _prose_paragraphs(_section_body(report, 9))
    value_section = _prose_paragraphs(_section_body(report, 10))
    next_section_source = _section_body(report, 11)
    next_section = _prose_paragraphs(next_section_source)
    next_items = _bullet_items(next_section_source)
    if len(section_one) < 12:
        raise CanonicalSourceError("R0.73X direct-result section lacks required public-copy paragraphs")
    if len(literature_section) < 4 or len(value_section) < 4 or len(next_section) < 2:
        raise CanonicalSourceError("R0.73X summary-section paragraph inventory drift")
    if len(next_items) != 5:
        raise CanonicalSourceError(f"R0.73X next-step list must contain five items, found {len(next_items)}")

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
    if "formalFigurePackage=PASS" in combined_compact:
        failures.append("canonical-ledger-formal-figure-unbound-pass")
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
        lead_zh=section_one[0] + " " + section_one[3] + " " + section_one[-1],
        home_zh=section_one[0] + " " + section_one[5] + " " + section_one[-2],
        recap_zh=" ".join(value_section),
        literature_zh=literature_section[-1],
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
        description="Read and validate canonical R0.73X release content without writing."
    )
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if not args.check_only:
        parser.print_help()
        return
    content = load_release_content()
    figure_pending = any(
        failure.startswith("formal-figure-")
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
        "baselineAccounting": R073W_BASELINE,
        "targetAccounting": R073X_TARGET,
        "publicationReady": content.publication_ready,
        "readinessFailures": list(content.readiness_failures),
        "localizedHeatCharacteristicLedger": "PROVED_WITH_STATED_SOLUTION_CLASS",
        "gaussianVelocityTailLemma": "INDEPENDENT_AUDIT_PASS",
        "pressureExteriorTailSizeLemma": "PASS_AT_POSITIVE_SCALE",
        "positiveScaleAbsoluteSize": "PROVED",
        "formalEvidenceCertificate": (
            "SOURCE_COMMIT_BOUND_PACKAGE_HASH_SEALED"
            if not any("formal-certificate" in failure for failure in content.readiness_failures)
            else "PENDING"
        ),
        "formalFigurePackage": (
            "PENDING" if figure_pending else "SEALED_COMMIT_BOUND"
        ),
        "compactCutoffQuadraticAbsorption": "OPEN",
        "signedToAbsoluteCoercivity": "OPEN",
        "weightedTentCarlesonControl": "OPEN",
        "suitableWeakZeroScaleEndpoint": "OPEN",
        "epsilonRegularity": "OPEN",
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
