#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail-closed reader content for the note-only R0.73Y release.

This module reads frozen research sources and the later reviewed bilingual
dictionary. It never writes files. The cumulative recap deliberately remains
the R0.73X milestone; no R0.73Y recap fragment is exposed here.
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
import subprocess
import unicodedata


RELEASE = "R0.73Y"
RELEASE_ID = "r073y"
SITE_VERSION = "1.65"
NEXT_RELEASE = "R0.73Z"
PUBLIC_TITLE_ZH = "R0.73Y｜Exact shear 类否定 production-only coercivity"
RELEASE_TITLE_EN = "R0.73Y | Exact shear class rules out production-only coercivity"
SUBTITLE_ZH = "全尺度零生产、严格正 heat covariance 与最小修复边界"
PUBLIC_SUBTITLE_ZH = "全尺度零 production、A≠0 时严格正 heat covariance 与最小修复边界"
FIGURE_ID = "fig-r073y-exact-shear-obstruction"
FIGURE_SOURCE_RELATIVE = f"figures/r073y/{FIGURE_ID}"
FIGURE_ARCHIVE_RELATIVE = FIGURE_SOURCE_RELATIVE
RESEARCH_SOURCE_COMMIT = "1ecc6fe20a921db9d0876dbd4484a3aa4ca7ec66"
CERTIFICATE_PACKAGE_COMMIT = "1811bb8e93c17b570ab58b10842f22695f0e2b3c"
FIGURE_SOURCE_COMMIT = "e37bf12cb5c2a8eb975e5097229dbc48fa597b35"
FIGURE_PACKAGE_COMMIT = "05fdbc717a02be9f88fafc2b67a658e706b40be4"
LATEST_RECAP_RELEASE = "r073x"
LATEST_RECAP_HTML = "public/recap-r0-61-r0-73x.html"
LATEST_RECAP_PDF = "public/recap-r0-61-r0-73x.pdf"

R073X_BASELINE = {
    "latestCompletedRelease": "r073x",
    "siteVersion": "1.64",
    "publicHtmlNoteCount": 200,
    "postR060PublishedNodeCount": 140,
    "postR060RecapNodeCount": 140,
    "latestRecapRelease": "r073x",
    "nextRelease": "r073y",
    "postR070APublishedReleaseCount": 102,
    "postR070AFormalSealedReleaseCount": 78,
    "legacyFormalFigureBacklogCount": 24,
    "publicPdfNoteCount": 157,
}

R073Y_TARGET = {
    "latestCompletedRelease": RELEASE_ID,
    "siteVersion": SITE_VERSION,
    "publicHtmlNoteCount": 201,
    "postR060PublishedNodeCount": 141,
    "postR060RecapNodeCount": 140,
    "latestRecapRelease": LATEST_RECAP_RELEASE,
    "nextRelease": "r073z",
    "postR070APublishedReleaseCount": 103,
    "postR070AFormalSealedReleaseCount": 79,
    "legacyFormalFigureBacklogCount": 24,
    "publicPdfNoteCount": 158,
}

FROZEN_RESEARCH_SOURCE_PATHS = (
    "research/r073y_exact_shear_no_go.md",
    "scripts/r073y_exact_shear_certificate.py",
    "research/r073y_exact_shear_certificate.json",
    "research/r073y_exact_shear_certificate_report.md",
    "research/r073y_primary_literature_audit.md",
    "research/r073y_evidence_gap_matrix.md",
    "research/r073y_report-source.md",
    "research/r073y_exact_shear_independent_reaudit.md",
)
DICTIONARY_SOURCE = "research/r073y_bilingual_dictionary.md"
CORRECTION_SOURCE = "research/r073y_reader_quantifier_correction.md"
CANONICAL_SOURCE_PATHS = FROZEN_RESEARCH_SOURCE_PATHS + (
    DICTIONARY_SOURCE,
    CORRECTION_SOURCE,
)
PLANNED_AUDIT_PATHS = (
    "research/r073y_figure_source_audit.md",
    "research/r073y_figure_source_reaudit.md",
)
REPORT_SOURCE = "research/r073y_report-source.md"

FIGURE_SOURCE_NAMES = (
    "README.md", "caption.md", "chart-contract-and-source-data.md", "command.txt",
    "config.json", "contract.json", "plot.py", "qa-protocol.md", "requirements.txt",
    "validate.py",
)
FIGURE_RAW_NAMES = (
    "environment.json", "figure.pdf", "figure.png", "figure.svg", "progress.ndjson",
    "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "resource-log.ndjson",
    "results.json", "source-data.csv",
)
FIGURE_METADATA_SHA256 = {
    "manifest.json": "8ab3a2875cac69f7d208673731eff03f0635f95c8fcb90fb0641f7663c53fe23",
    "validation.json": "0dfc353afae9f7e2152f2175d6a2ebe452841fa15f8e968691513e9f0c7c5f8e",
    "qa-report.md": "21d85686f2feec15f0ac6b3af6782cb72c3f009ff2c0b38d4ee157914d2a1b85",
    "SHA256SUMS": "6ef06e492d0e280ec8df431b7e02fe97bdc53614e95f232a1114efd17be99ce7",
}
# Filled only after the four reader-owned files are reviewed. These digests do
# not include this module, so they do not create a self-hash cycle.
PUBLICATION_SOURCE_SHA256 = {
    DICTIONARY_SOURCE: "bde70adc2a6721bdccba72594e643c485e335c97a821032ea5677a3b555ed914",
    CORRECTION_SOURCE: "3d096fd2d419864fd9b59a6147a097ad2debabbec168d237fdd976091a882c41",
    PLANNED_AUDIT_PATHS[0]: "bec2d287e31897fc2311519b9fb47b2f1344f69f81080ca8b9c440073b4e664d",
    PLANNED_AUDIT_PATHS[1]: "3d596d24e71ba63f4a142a6a8081588e649eca92330c76c7f4e7cac1b853b5b5",
}

PUBLIC_VOICE_BANS = (
    "我们", "攻关", "主攻", "研究纪律", "三重审计", "杀死错误想法",
    "颠覆性", "世界首个", "接近解决", "解决了千禧年", "首次证明",
)
FORBIDDEN_PUBLIC_CLAIMS = (
    "solves the Clay Millennium problem", "proves global regularity",
    "proves a singularity", "generic turbulence is proved", "DNS proves",
    "证明任意初值全局正则", "证明奇性", "接近 Clay 解答",
    "exact shear 机制是首次发现", "Vreman 没有发现 simple shear",
)
REQUIRED_REPORT_PHRASES = (
    "production-only 形式下是假的",
    r"\Pi_s=\mathscr S_s=Q_s=0",
    r"D_{ii,s}>0",
    "production-only no-go package",
    "直接重合",
    "不能申报为新发现",
    "本节对整个 Clay 问题的直接推进很小",
    "NOT CLAY",
    "LOCAL_DIRECT_NO_DGX",
    "false",
)
EXPECTED_MACHINE_LEDGER = (
    "exactShearNSE=PROVED_ANALYTICALLY",
    "allPositiveHeatScalesZeroProduction=PROVED_ANALYTICALLY",
    "gradientCovarianceStrictlyPositiveForAneq0AndSgt0=PROVED_ANALYTICALLY",
    "zeroAmplitudeMemberCovariance=ZERO",
    "positiveSizeCubicHomogeneity=PROVED_ANALYTICALLY",
    "productionOnlyCoercivity=REFUTED_FOR_ZERO_PRESERVING_FUNCTIONALS",
    "singleFourierCertificate=FINITE_CROSS_CHECK_ONLY",
    "strictPositivityFromSampling=FALSE",
    "basicShearNoveltyOrPriority=NOT_CLAIMED",
    "quotientCoercivity=OPEN",
    "pressureActiveInvisibleFamily=OPEN",
    "suitableWeakZeroScaleEndpoint=OPEN",
    "epsilonRegularity=OPEN",
    "formalEvidenceCertificate=SOURCE_COMMIT_BOUND_PACKAGE_HASH_SEALED",
    "formalFigurePackage=SEALED_COMMIT_BOUND_25_FILES",
    "navierStokesSimulation=NOT_RUN",
    "directNumericalSimulation=NOT_RUN",
    "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX",
    "dgxUsed=false",
    "latestPublishedRelease=r073y",
    "latestRecapRelease=r073x",
    "recapPolicy=MILESTONE_ONLY",
    "arbitraryThreeDimensionalGlobalRegularity=OPEN",
    "clayConclusion=OPEN",
    "NOT CLAY",
)
REQUIRED_LEDGER_MARKERS = EXPECTED_MACHINE_LEDGER
FORBIDDEN_LEDGER_MARKERS = (
    "productionOnlyCoercivity=PROVED",
    "basicShearNoveltyOrPriority=TRUE",
    "strictPositivityFromSampling=TRUE",
    "epsilonRegularity=CLOSED",
    "arbitraryThreeDimensionalGlobalRegularity=CLOSED",
    "clayConclusion=CLOSED",
    "clayConclusion=SOLVED",
)

CLOSED_LEDGER = (
    "PROVED：exactShearNSE=PROVED_ANALYTICALLY；"
    "allPositiveHeatScalesZeroProduction=PROVED_ANALYTICALLY；"
    "gradientCovarianceStrictlyPositiveForAneq0AndSgt0=PROVED_ANALYTICALLY；"
    "zeroAmplitudeMemberCovariance=ZERO；"
    "positiveSizeCubicHomogeneity=PROVED_ANALYTICALLY；"
    "productionOnlyCoercivity=REFUTED_FOR_ZERO_PRESERVING_FUNCTIONALS"
)
FINITE_LEDGER = (
    "FINITE：singleFourierCertificate=FINITE_CROSS_CHECK_ONLY；"
    "formalEvidenceCertificate=SOURCE_COMMIT_BOUND_PACKAGE_HASH_SEALED；"
    "formalFigurePackage=SEALED_COMMIT_BOUND_25_FILES；"
    "navierStokesSimulation=NOT_RUN；directNumericalSimulation=NOT_RUN；"
    "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX；dgxUsed=false"
)
OPEN_LEDGER = (
    "OPEN：quotientCoercivity=OPEN；pressureActiveInvisibleFamily=OPEN；"
    "suitableWeakZeroScaleEndpoint=OPEN；epsilonRegularity=OPEN；"
    "arbitraryThreeDimensionalGlobalRegularity=OPEN；clayConclusion=OPEN"
)
EXACT_SCOPE_BOUNDARY_ZH = (
    "本节只否定在零输入处取零的 production-only functional 对 R0.73X 正尺度大小的"
    "振幅无关有限模量。它不否定加入 covariance、endpoint 或 cutoff debt 的估计，"
    "也不提供奇性、epsilon regularity 或任意三维初值全局正则结论。"
)


class CanonicalSourceError(RuntimeError):
    """A canonical source, ledger marker, or public boundary is invalid."""


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
    subtitle_zh: str
    date: str
    status: str
    lead_zh: str
    home_zh: str
    literature_zh: str
    next_release: str
    next_gate_zh: str
    sections: tuple[ReportSection, ...]
    references_html: str
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
            '      <div><div class="eyebrow">研究笔记 R0.73Y · '
            'EXACT ANALYTIC NO-GO / LITERATURE-CALIBRATED</div>\n'
            f'        <h1>{html.escape(self.public_title_zh)}</h1>\n'
            f'        <p class="lead">{html.escape(self.subtitle_zh)}</p>'
            f'<p>{html.escape(self.lead_zh)}</p></div>\n'
            '      <div class="stamp"><span class="state">状态 · R0.73Y 完成</span>'
            '<strong>analytic exact witness / not DNS</strong>'
            f'<p>版本 R0.73Y · {html.escape(self.date)}</p>'
            '<p>exact shear NSE：PROVED ANALYTICALLY</p>'
            '<p>production channels：ZERO AT EVERY POSITIVE SCALE</p>'
            '<p>gradient covariance：STRICTLY POSITIVE FOR A ≠ 0; ZERO FOR A = 0</p>'
            '<p>basic shear novelty / priority：NOT CLAIMED</p>'
            '<p>NOT CLAY</p></div>\n'
            '    </div></header>'
        )

    @property
    def note_article(self) -> str:
        correction = (
            '        <section id="quantifier-correction" class="callout">'
            '<div class="section-no">Q / Quantifier correction</div>'
            '<h2>严格正性只对非零振幅成员陈述</h2>'
            '<p>冻结 theorem 的精确量词是：production 对所有实振幅为零；'
            '当 A ≠ 0 时 D<sub>ii,s</sub> &gt; 0；A = 0 时为平凡零场且 D<sub>ii,s</sub> = 0。'
            '本页按受审纠错源对原 reader report 的三处省略量词做精确替换，'
            '不改动已冻结的证明字节。</p></section>'
        )
        body = "\n".join(
            f'        <section id="{section.anchor}">'
            f'<div class="section-no">{section.number:02d} / canonical report</div>'
            f'<h2>{html.escape(section.title)}</h2>{section.html}</section>'
            for section in self.sections
        )
        figure = (
            '        <section id="figure"><div class="section-no">F / Journal figure</div>'
            '<h2>解析 exact shear kernel，不是 DNS</h2>'
            f'<p><img src="/assets/r073y/{FIGURE_ID}.svg" '
            'alt="R0.73Y analytic exact shear witness: zero production, positive heat covariance, and cubic amplitude homogeneity"></p>'
            f'<p><a href="/assets/r073y/{FIGURE_ID}.pdf">下载矢量 PDF</a> · '
            f'<a href="/assets/r073y/{FIGURE_ID}.png">下载 600 dpi PNG</a> · '
            f'<a href="/assets/r073y/{FIGURE_ID}.svg">打开 SVG</a></p>'
            '<p>附图只画解析公式和由解析公式导出的 source data。它是 analytic exact witness，'
            '不是 simulation 或 DNS，也不是奇性或 blow-up 候选。</p></section>'
        )
        boundary = (
            '        <section id="release-boundary">'
            '<div class="section-no">B / Exact claim boundary</div>'
            '<h2>文献事实、本节证明、有限核验与开放问题分开</h2>'
            '<p>文献直接碰撞：Vreman 已包含 simple shear 的零 exact SGS dissipation；'
            'Jeong--Yoneda 已使用周期 heat-evolving shear；Germano 与 Eyink--Aluie 已分开 signed production 和 nonnegative covariance。'
            '因此不申报 basic shear mechanism 的新颖性或优先权。</p>'
            f'<p>{html.escape(CLOSED_LEDGER)}</p>'
            f'<p>{html.escape(FINITE_LEDGER)}</p>'
            f'<p>{html.escape(OPEN_LEDGER)}</p>'
            f'<p>{html.escape(EXACT_SCOPE_BOUNDARY_ZH)} NOT CLAY。</p></section>'
        )
        reproduction = (
            '        <section id="reproduce"><div class="section-no">R / Reproduction</div>'
            '<h2>证明、证书、审计与复现</h2>'
            '<p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073y_exact_shear_no_go.md">解析定理</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073y_exact_shear_independent_reaudit.md">独立复审</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073y_primary_literature_audit.md">一手文献审计</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/'
            'research/r073y_reader_quantifier_correction.md">读者层量词纠错</a> · '
            '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/'
            'research/certificates/r073y">证书档案</a></p>'
            '<p><a href="/research/r073y/r073y_figure_source_audit.md">附图 source audit</a> · '
            '<a href="/research/r073y/r073y_figure_source_reaudit.md">附图 re-audit</a></p>'
            f'<p><a href="/assets/r073y/{FIGURE_ID}.pdf">期刊附图 PDF</a> · '
            '<a href="/notes/r0-73y.pdf">同步研究笔记 PDF</a> · '
            '<a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（截止 R0.73X）</a> · '
            '<a href="/recap-r0-61-r0-73x.pdf">recap PDF</a></p></section>'
        )
        references = (
            '        <section id="references"><div class="section-no">References</div>'
            '<h2>参考文献</h2>' + self.references_html + '</section>'
        )
        return (
            "      <article>\n" + correction + "\n" + body + "\n" + figure + "\n" + boundary
            + "\n" + reproduction + "\n" + references + "\n      </article>"
        )

    @property
    def home_card(self) -> str:
        return (
            '          <div class="task-one" id="r073y" data-release="r073y" style="margin-top:2rem">\n'
            f'            <p class="eyebrow">研究笔记 R0.73Y · {html.escape(self.date)}</p>'
            f'<h3>{html.escape(self.public_title_zh)}</h3>\n'
            f'            <p>{html.escape(self.home_zh)}</p>\n'
            '<p><strong>文献边界：</strong>simple shear 的零 SGS dissipation 已在 Vreman（2004）直接出现；'
            '不申报 basic mechanism 的新颖性或优先权。</p>\n'
            f'            <p><strong>解析边界：</strong>{html.escape(CLOSED_LEDGER)}</p>\n'
            f'            <p><strong>有限边界：</strong>{html.escape(FINITE_LEDGER)}</p>\n'
            f'            <p><strong>开放边界：</strong>{html.escape(OPEN_LEDGER)}。NOT CLAY。</p>\n'
            '            <p><a href="/notes/r0-73y.html"><strong>阅读 R0.73Y 研究笔记 →</strong></a>'
            '<br><a href="/notes/r0-73y.pdf">下载同步 PDF</a> · '
            f'<a href="/assets/r073y/{FIGURE_ID}.pdf">下载期刊附图 PDF</a> · '
            '<a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（截止 R0.73X）</a></p>\n'
            f'            <p><strong style="color:var(--gold)">下一发布门（{self.next_release}）：</strong>'
            f'&nbsp;{html.escape(self.next_gate_zh)}</p>\n'
            '          </div>'
        )

    @property
    def literature_update(self) -> str:
        return (
            '<span class="route-r073y-deck-update">' + _inline(self.literature_zh)
            + ' 直接碰撞：Vreman（2004）已含 simple shear 零 SGS dissipation；'
            'basicShearNoveltyOrPriority=NOT_CLAIMED；productionOnlyCoercivity=REFUTED_FOR_ZERO_PRESERVING_FUNCTIONALS；'
            'quotientCoercivity=OPEN；NOT CLAY。</span>'
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
    return _compact(_one(
        rf"(?ms)^\*\*{re.escape(label)}：\*\*\s*(.+?)(?=\n\s*\n)",
        value, label,
    )).strip("`")


def _dictionary_value(value: str, label: str) -> str:
    escaped = re.escape(label)
    patterns = (
        rf"(?ms)^\*\*{escaped}:\*\*\s*(.+?)(?=\n\s*\n)",
        rf"(?m)^-\s*{escaped}:\s*`?(.+?)`?\s*$",
    )
    for pattern in patterns:
        matches = re.findall(pattern, value)
        if len(matches) == 1:
            return _compact(matches[0]).strip("`")
    raise CanonicalSourceError("dictionary metadata absent or ambiguous: " + label)


def _compact(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return re.sub(r"(?<=[\u3400-\u9fff]) (?=[\u3400-\u9fff])", "", value)


def _machine_ledger(value: str, heading: str) -> tuple[str, ...]:
    pattern = (
        rf"(?ms)^##\s+{re.escape(heading)}\s*$.*?"
        r"^```text\s*$\n(.*?)\n^```\s*$"
    )
    block = _one(pattern, value, heading + " machine ledger")
    rows = tuple(row.strip() for row in block.splitlines() if row.strip())
    if len(rows) != len(set(rows)):
        raise CanonicalSourceError(heading + ": duplicate machine-ledger row")
    return rows


def _replace_exact_once(value: str, old: str, new: str, label: str) -> str:
    count = value.count(old)
    if count != 1:
        raise CanonicalSourceError(f"{label}: expected one frozen snippet, found {count}")
    result = value.replace(old, new, 1)
    if old in result:
        raise CanonicalSourceError(label + ": frozen snippet survived correction")
    return result


def _correct_reader_report(report: str, correction: str) -> str:
    required = (
        "readerCorrectionVersion=1",
        "frozenReportBytesPreserved=true",
        "publicTransformation=EXACT_COUNTED_REPLACEMENTS",
        "typesettingNormalization=EXACT_COUNTED_NONSEMANTIC_REPAIRS",
        "zeroProduction=ALL_REAL_A",
        "strictGradientCovariance=ONLY_A_NE_0",
        "zeroAmplitudeGradientCovariance=0",
        "gradientCovarianceStrictlyPositiveForAneq0AndSgt0=PROVED_ANALYTICALLY",
        "strictPositivityFromSampling=FALSE",
        "recapPolicy=MILESTONE_ONLY",
        "latestPublishedRelease=r073y",
        "latestRecapRelease=r073x",
        "clayConclusion=OPEN",
        "NOT CLAY",
    )
    if _machine_ledger(correction, "3. Machine-readable correction boundary") != required:
        raise CanonicalSourceError("reader correction machine ledger drift")
    if hashlib.sha256(report.encode("utf-8")).hexdigest() != "d2f4df01b51ec613affc4b14a3544f6f702584de1ba1a94b2ec241e31d5efd01":
        raise CanonicalSourceError("frozen reader report bytes drifted")

    result = _replace_exact_once(
        report,
        "存在一整个光滑、零均值、任意振幅的\n周期 Navier--Stokes exact shear 类，使",
        "存在一整个光滑、零均值的\n周期 Navier--Stokes exact shear 类。对任意实振幅 \\(A\\in\\mathbb R\\)，",
        "Q1 exact-family introduction",
    )
    result = _replace_exact_once(
        result,
        "\n同时\n\n\\[\n D_{ii,s}>0\n\\tag{1.2}\n\\]\n\n逐点严格成立",
        "\n而且\n\n\\[\n A\\ne0\\Longrightarrow D_{ii,s}>0,\\qquad A=0\\Longrightarrow D_{ii,s}=0\n\\tag{1.2}\n\\]\n\n逐点成立",
        "Q1 strict-covariance display",
    )
    result = _replace_exact_once(
        result,
        "相反，gradient covariance 是严格正的 heat variance：",
        "当 \\(A\\ne0\\) 时，gradient covariance 是严格正的 heat variance；"
        "当 \\(A=0\\) 时，它恒等于零：",
        "Q2 structural-covariance prose",
    )
    result = _replace_exact_once(
        result,
        " \\boxed{\n D_{ii,s}=A^2|a|^2|k|^2",
        " \\boxed{\n A\\ne0\\Longrightarrow D_{ii,s}=A^2|a|^2|k|^2",
        "Q2 structural-covariance formula",
    )
    result = _replace_exact_once(
        result,
        "\\[\n D_{ii,s}={b_A(t)^2n^2\\over2}\n (1-\\rho^2)(1-\\rho^2\\cos(2nx_2))\n \\ge {b_A(t)^2n^2\\over2}(1-\\rho^2)^2>0.\n\\tag{3.3}\n\\]",
        "\\[\n \\begin{aligned}\n A\\ne0\\Longrightarrow D_{ii,s}\n &= {b_A(t)^2n^2\\over2}(1-\\rho^2)\n    (1-\\rho^2\\cos(2nx_2))\\\\\n &\\ge {b_A(t)^2n^2\\over2}(1-\\rho^2)^2>0,\\\\\n A=0&\\Longrightarrow D_{ii,s}=0.\n \\end{aligned}\n\\tag{3.3}\n\\]",
        "Q3 single-mode covariance formula",
    )
    for old, new, label in (
        ("=|A|^3C,qquad C>0.", "=|A|^3C,\\qquad C>0.", "Q5 formula 1.3 spacing"),
        ("u^A(t,x)=AaF(t,k\\cdot x),qquad p^A=0.",
         "u^A(t,x)=AaF(t,k\\cdot x),\\qquad p^A=0.", "Q5 formula 2.2 spacing"),
        ("u^A(t,x)=Ae^{-\\nu n^2t}\\sin(nx_2)e_1,qquad n\\ge1.",
         "u^A(t,x)=Ae^{-\\nu n^2t}\\sin(nx_2)e_1,\\qquad n\\ge1.",
         "Q5 formula 3.1 spacing"),
    ):
        result = _replace_exact_once(result, old, new, label)
    for forbidden in (
        "零均值、任意振幅的\n周期 Navier--Stokes exact shear 类，使",
        "\n D_{ii,s}>0\n",
        "相反，gradient covariance 是严格正的 heat variance",
    ):
        if forbidden in result:
            raise CanonicalSourceError("uncorrected A=0 reader shorthand survived")
    return result


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
    output: list[str] = []
    cursor = 0
    tokens = re.compile(
        r"\[([^\]\n]+)\]\((https?://[^)\s]+)\)|`([^`\n]+)`|"
        r"\*\*([^*\n]+)\*\*|\*([^*\n]+)\*"
    )
    for match in tokens.finditer(value):
        output.append(html.escape(value[cursor:match.start()], quote=False))
        if match.group(1) is not None:
            output.append(f'<a href="{html.escape(match.group(2), quote=True)}">{html.escape(match.group(1))}</a>')
        elif match.group(3) is not None:
            output.append(f"<code>{html.escape(match.group(3))}</code>")
        elif match.group(4) is not None:
            output.append(f"<strong>{html.escape(match.group(4))}</strong>")
        else:
            output.append(f"<em>{html.escape(match.group(5))}</em>")
        cursor = match.end()
    output.append(html.escape(value[cursor:], quote=False))
    return "".join(output)


def _markdown_blocks(markdown: str) -> str:
    rows = markdown.strip().splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    bullets: list[str] = []
    ordered: list[str] = []
    math_rows: list[str] = []
    in_math = False

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
        if stripped == r"\[":
            flush()
            in_math = True
            math_rows = [r"\["]
            continue
        if in_math:
            math_rows.append(row)
            if stripped == r"\]":
                output.append('<div class="equation result">' + html.escape("\n".join(math_rows), quote=False) + "</div>")
                math_rows = []
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
            (bullets if bullets else ordered)[-1] += " " + stripped
            continue
        if not stripped:
            flush()
            continue
        paragraph.append(row)
    if in_math:
        raise CanonicalSourceError("unterminated display math in R0.73Y report")
    return "".join(output)


def _section_body(report: str, number: int) -> str:
    match = re.search(rf"(?ms)^##\s+{number}\.\s+.+?$\n(.*?)(?=^##\s+|\Z)", report)
    if match is None:
        raise CanonicalSourceError(f"report section {number} is absent")
    return match.group(1).strip()


def _sections(report: str) -> tuple[tuple[ReportSection, ...], str]:
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", report))
    if len(matches) != 8:
        raise CanonicalSourceError(f"R0.73Y report must contain seven numbered sections plus references, found {len(matches)}")
    used: set[str] = set()
    sections: list[ReportSection] = []
    references = ""
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(report)
        body = report[match.end():end].strip()
        if index < 7:
            title_match = re.match(r"^(\d+)\.\s+(.+)$", match.group(1))
            if title_match is None or int(title_match.group(1)) != index + 1:
                raise CanonicalSourceError("report section numbering drift: " + match.group(1))
            title = title_match.group(2).strip()
            sections.append(ReportSection(index + 1, title, _slug(title, used), body, _markdown_blocks(body)))
        elif match.group(1).strip() != "参考文献":
            raise CanonicalSourceError("last report section must be unnumbered references")
        else:
            references = _markdown_blocks(body)
    return tuple(sections), references


def _prose_paragraphs(section: str) -> list[str]:
    without_math = re.sub(r"(?ms)\\\[.*?\\\]", " ", section)
    values: list[str] = []
    for block in re.split(r"\n\s*\n", without_math):
        stripped = block.strip()
        if not stripped or re.match(r"^(?:-|\d+\.)\s", stripped):
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


def _strict_json(path: Path, label: str) -> dict:
    def reject(value: str) -> None:
        raise ValueError("non-finite JSON constant: " + value)
    try:
        value = json.loads(path.read_text(encoding="utf-8"), parse_constant=reject)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise CanonicalSourceError(label + ": invalid JSON") from exc
    if not isinstance(value, dict):
        raise CanonicalSourceError(label + ": expected object")
    return value


def _git(root: Path, arguments: list[str], label: str, *, binary: bool = False) -> str | bytes:
    completed = subprocess.run(
        ["git", *arguments], cwd=root, check=False,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if completed.returncode:
        raise CanonicalSourceError(
            label + ": git " + " ".join(arguments) + " failed: "
            + completed.stderr.decode("utf-8", "replace").strip()
        )
    return completed.stdout if binary else completed.stdout.decode("utf-8").strip()


def _git_bytes(root: Path, commit: str, relative: str) -> bytes:
    value = _git(root, ["cat-file", "blob", f"{commit}:{relative}"], relative, binary=True)
    assert isinstance(value, bytes)
    return value


def _git_paths(root: Path, commit: str, prefix: str) -> tuple[str, ...]:
    value = _git(root, ["ls-tree", "-r", "--name-only", commit, "--", prefix], prefix)
    assert isinstance(value, str)
    return tuple(sorted(row for row in value.splitlines() if row))


def _git_blob_oid(root: Path, commit: str, relative: str) -> str:
    value = _git(root, ["rev-parse", f"{commit}:{relative}"], relative + " blob")
    assert isinstance(value, str)
    if re.fullmatch(r"[0-9a-f]{40}", value) is None:
        raise CanonicalSourceError(relative + ": malformed Git blob OID")
    return value


def _git_is_ancestor(root: Path, older: str, newer: str, label: str) -> None:
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", older, newer], cwd=root,
        check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if completed.returncode:
        raise CanonicalSourceError(label + ": commit ancestry mismatch")


def _current_regular_paths(root: Path, prefix: str) -> tuple[str, ...]:
    base = root / prefix
    if not base.is_dir() or base.is_symlink():
        raise CanonicalSourceError(prefix + ": expected regular directory")
    values: list[str] = []
    for path in base.rglob("*"):
        if path.is_symlink() or (path.exists() and not path.is_file() and not path.is_dir()):
            raise CanonicalSourceError(prefix + ": symlink or special file present")
        if path.is_file():
            values.append(path.relative_to(root).as_posix())
    return tuple(sorted(values))


def _parse_sha256sums(payload: bytes, label: str) -> dict[str, str]:
    values: dict[str, str] = {}
    try:
        rows = payload.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise CanonicalSourceError(label + ": SHA256SUMS is not UTF-8") from exc
    for row in rows:
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/]+)", row)
        if match is None or match.group(2) in values:
            raise CanonicalSourceError(label + ": malformed or duplicate SHA256SUMS row")
        values[match.group(2)] = match.group(1)
    return values


def _verify_frozen_research(root: Path) -> None:
    for relative in FROZEN_RESEARCH_SOURCE_PATHS:
        current = (root / relative).read_bytes()
        if current != _git_bytes(root, RESEARCH_SOURCE_COMMIT, relative):
            raise CanonicalSourceError("frozen research byte drift: " + relative)


def _verify_publication_sources(root: Path) -> None:
    for relative, expected in PUBLICATION_SOURCE_SHA256.items():
        if re.fullmatch(r"[0-9a-f]{64}", expected) is None:
            raise CanonicalSourceError("publication source digest is not frozen: " + relative)
        path = root / relative
        if not path.is_file() or path.is_symlink():
            raise CanonicalSourceError("publication source is missing or unsafe: " + relative)
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise CanonicalSourceError("publication source hash drift: " + relative)


def _verify_tree_at_commit(root: Path, commit: str, prefix: str) -> tuple[str, ...]:
    committed = _git_paths(root, commit, prefix)
    current = _current_regular_paths(root, prefix)
    if not committed or current != committed:
        raise CanonicalSourceError(prefix + ": current/commit inventory mismatch")
    for relative in committed:
        if (root / relative).read_bytes() != _git_bytes(root, commit, relative):
            raise CanonicalSourceError(prefix + ": current/commit byte mismatch: " + relative)
    return committed


def _verify_figure_git_seal(root: Path, manifest: dict) -> None:
    prefix = FIGURE_SOURCE_RELATIVE
    source_names = set(FIGURE_SOURCE_NAMES + FIGURE_RAW_NAMES)
    metadata_names = set(FIGURE_METADATA_SHA256)
    expected_names = source_names | metadata_names
    _git_is_ancestor(root, RESEARCH_SOURCE_COMMIT, FIGURE_SOURCE_COMMIT, "figure formula/source ancestry")
    parent = _git(root, ["rev-parse", FIGURE_PACKAGE_COMMIT + "^"], "figure package parent")
    assert isinstance(parent, str)
    if parent != FIGURE_SOURCE_COMMIT:
        raise CanonicalSourceError("figure package is not the direct metadata child")
    source_paths = _git_paths(root, FIGURE_SOURCE_COMMIT, prefix)
    package_paths = _verify_tree_at_commit(root, FIGURE_PACKAGE_COMMIT, prefix)
    if {Path(path).name for path in source_paths} != source_names or len(source_paths) != 21:
        raise CanonicalSourceError("figure source commit is not the exact 21-file layer")
    if {Path(path).name for path in package_paths} != expected_names or len(package_paths) != 25:
        raise CanonicalSourceError("figure package commit is not the exact 25-file layer")
    changed = _git(
        root,
        ["diff-tree", "--no-commit-id", "--name-only", "-r", FIGURE_SOURCE_COMMIT,
         FIGURE_PACKAGE_COMMIT, "--", prefix],
        "figure metadata-child diff",
    )
    assert isinstance(changed, str)
    if {Path(row).name for row in changed.splitlines() if row} != metadata_names:
        raise CanonicalSourceError("figure package child changed files outside four metadata rows")

    bindings = manifest.get("seal", {}).get("figureSourceBindings")
    if not isinstance(bindings, list) or len(bindings) != 21:
        raise CanonicalSourceError("figure source binding count drift")
    by_name = {row.get("path"): row for row in bindings if isinstance(row, dict)}
    if set(by_name) != source_names:
        raise CanonicalSourceError("figure source binding inventory drift")
    for name in sorted(source_names):
        relative = f"{prefix}/{name}"
        payload = (root / relative).read_bytes()
        row = by_name[name]
        if (
            payload != _git_bytes(root, FIGURE_SOURCE_COMMIT, relative)
            or row.get("repositoryPath") != relative
            or row.get("bytes") != len(payload)
            or row.get("sha256") != hashlib.sha256(payload).hexdigest()
            or row.get("gitBlobObjectId") != _git_blob_oid(root, FIGURE_SOURCE_COMMIT, relative)
        ):
            raise CanonicalSourceError("figure source binding drift: " + name)

    for name, expected in FIGURE_METADATA_SHA256.items():
        payload = (root / prefix / name).read_bytes()
        if hashlib.sha256(payload).hexdigest() != expected:
            raise CanonicalSourceError("figure metadata hash drift: " + name)
    sums = _parse_sha256sums((root / prefix / "SHA256SUMS").read_bytes(), "R0.73Y figure")
    if set(sums) != expected_names - {"SHA256SUMS"} or len(sums) != 24:
        raise CanonicalSourceError("figure SHA256SUMS inventory drift")
    for name, digest in sums.items():
        if hashlib.sha256((root / prefix / name).read_bytes()).hexdigest() != digest:
            raise CanonicalSourceError("figure SHA256SUMS mismatch: " + name)


def _certificate_final(root: Path) -> tuple[bool, str]:
    path = root / "research/certificates/r073y/manifest.json"
    if not path.is_file() or path.is_symlink():
        return False, "formal-certificate-manifest-missing"
    manifest = _strict_json(path, "R0.73Y certificate manifest")
    contract_path = path.parent / "contract.json"
    if not contract_path.is_file() or contract_path.is_symlink():
        return False, "formal-certificate-contract-missing"
    contract = _strict_json(contract_path, "R0.73Y certificate contract")
    inventory = manifest.get("inventory")
    files = manifest.get("files")
    bindings = contract.get("source", {}).get("inputs")
    actual = sorted(item.name for item in path.parent.iterdir() if item.is_file() and not item.is_symlink())
    try:
        _git_is_ancestor(root, RESEARCH_SOURCE_COMMIT, CERTIFICATE_PACKAGE_COMMIT, "certificate ancestry")
        committed = _verify_tree_at_commit(root, CERTIFICATE_PACKAGE_COMMIT, "research/certificates/r073y")
    except CanonicalSourceError:
        return False, "formal-certificate-package-commit-or-byte-binding-drift"
    final = (
        len(committed) == 13
        and manifest.get("schema") == "r073y-formal-certificate-manifest-v1"
        and manifest.get("release") == RELEASE
        and manifest.get("status") == "SEALED"
        and manifest.get("source", {}).get("git_commit_sha1") == RESEARCH_SOURCE_COMMIT
        and isinstance(inventory, dict)
        and inventory.get("package_file_count") == len(actual)
        and isinstance(files, list) and inventory.get("manifest_entry_count") == len(files)
        and inventory.get("sha256sums_entry_count") == len(actual) - 1
        and isinstance(bindings, list) and len(bindings) == len(FROZEN_RESEARCH_SOURCE_PATHS)
        and manifest.get("claim_boundary", {}).get("not_clay") is True
        and manifest.get("claim_boundary", {}).get("clay_problem_solved") is False
    )
    return final, "formal-certificate-source-bound-hash-seal-pending" if not final else ""


def _figure_final(root: Path) -> tuple[bool, str]:
    base = root / FIGURE_SOURCE_RELATIVE
    manifest_path = base / "manifest.json"
    validation_path = base / "validation.json"
    contract_path = base / "contract.json"
    if not all(path.is_file() and not path.is_symlink() for path in (manifest_path, validation_path, contract_path)):
        return False, "formal-figure-manifest-validation-or-contract-missing"
    manifest = _strict_json(manifest_path, "R0.73Y figure manifest")
    validation = _strict_json(validation_path, "R0.73Y figure validation")
    contract = _strict_json(contract_path, "R0.73Y figure contract")
    files = sorted(item.name for item in base.iterdir() if item.is_file() and not item.is_symlink())
    seal = manifest.get("seal", {})
    bindings = seal.get("figureSourceBindings")
    try:
        _verify_figure_git_seal(root, manifest)
        deep_seal = True
    except CanonicalSourceError:
        deep_seal = False
    final = (
        deep_seal
        and len(files) == 25
        and manifest.get("schemaVersion") == "research-figure-manifest-v1"
        and manifest.get("figureSchemaVersion") == "r073y-exact-shear-obstruction-manifest-v1"
        and contract.get("figureId") == FIGURE_ID
        and contract.get("sourceAuthority", {}).get("commit") == RESEARCH_SOURCE_COMMIT
        and contract.get("claimBoundary", {}).get("analyticExactWitness") is True
        and contract.get("claimBoundary", {}).get("navierStokesSimulation") is False
        and contract.get("claimBoundary", {}).get("dns") is False
        and contract.get("claimBoundary", {}).get("notClay") is True
        and contract.get("claimBoundary", {}).get("strictGradientCovarianceRequiresNonzeroAmplitude") is True
        and contract.get("claimBoundary", {}).get("zeroAmplitudeMemberCovariance") == "zero"
        and manifest.get("figureId") == FIGURE_ID and manifest.get("release") == RELEASE
        and manifest.get("status") == "formal" and manifest.get("publicationStatus") == "staged"
        and seal.get("figureSourceCommitAssigned") is True
        and seal.get("figureSourceCommit") == FIGURE_SOURCE_COMMIT
        and seal.get("figureSourceCommitBound") is True
        and seal.get("requiresFigureSourceCommitFinalReseal") is False
        and isinstance(bindings, list) and len(bindings) == 21
        and manifest.get("qa", {}).get("status") == "passed"
        and manifest.get("git", {}).get("sourceEvidenceCommit") == RESEARCH_SOURCE_COMMIT
        and validation.get("schemaVersion") == "r073y-exact-shear-validation-v3"
        and validation.get("status") == "PASS"
        and validation.get("sealState") == "formal-figure-source-seal"
    )
    return final, "formal-figure-final-seal-pending" if not final else ""


def load_release_content(root: Path | None = None) -> ReleaseContent:
    source_root = (root or Path(os.environ.get("R073Y_RELEASE_ROOT", Path(__file__).resolve().parents[1]))).resolve()
    _verify_frozen_research(source_root)
    _verify_publication_sources(source_root)
    texts = {relative: _regular_text(source_root, relative) for relative in CANONICAL_SOURCE_PATHS}
    audit_texts = {relative: _regular_text(source_root, relative) for relative in PLANNED_AUDIT_PATHS}
    report = texts[REPORT_SOURCE]
    dictionary = texts[DICTIONARY_SOURCE]
    correction = texts[CORRECTION_SOURCE]
    public_report = _correct_reader_report(report, correction)
    if public_report.count(",qquad") != 0 or public_report.count(",\\qquad") < 3:
        raise CanonicalSourceError("reader typesetting normalization drifted")
    combined = "\n".join((*texts.values(), *audit_texts.values()))
    compact = re.sub(r"\s+", " ", combined)
    report_compact = re.sub(r"\s+", "", report)

    report_title = _one(r"(?m)^#\s+(.+?)\s*$", report, "report H1")
    if report_title != PUBLIC_TITLE_ZH:
        raise CanonicalSourceError("R0.73Y report H1 drift: " + report_title)
    subtitle = _metadata_block(report, "副标题")
    date = _metadata_block(report, "日期")
    status = _metadata_block(report, "状态")
    if subtitle != SUBTITLE_ZH:
        raise CanonicalSourceError("R0.73Y report subtitle drift")
    if _dictionary_value(dictionary, "Release title") != RELEASE_TITLE_EN:
        raise CanonicalSourceError("reviewed English release title drift")
    if _dictionary_value(dictionary, "Public title (zh)") != PUBLIC_TITLE_ZH:
        raise CanonicalSourceError("dictionary Chinese public title drift")
    if _dictionary_value(dictionary, "Latest recap release") != LATEST_RECAP_RELEASE:
        raise CanonicalSourceError("dictionary must preserve R0.73X as latest recap")
    if _dictionary_value(correction, "Public subtitle (zh)") != PUBLIC_SUBTITLE_ZH:
        raise CanonicalSourceError("reader correction public subtitle drift")
    if _machine_ledger(dictionary, "5. Machine-readable release boundary") != EXPECTED_MACHINE_LEDGER:
        raise CanonicalSourceError("dictionary machine ledger must equal the frozen ordered ledger")
    for marker in REQUIRED_REPORT_PHRASES:
        if re.sub(r"\s+", "", marker) not in report_compact:
            raise CanonicalSourceError("canonical report missing phrase: " + marker)
    for marker in REQUIRED_LEDGER_MARKERS:
        if marker not in compact:
            raise CanonicalSourceError("canonical sources missing boundary marker: " + marker)
    for marker in FORBIDDEN_LEDGER_MARKERS:
        if marker in compact:
            raise CanonicalSourceError("forbidden R0.73Y ledger marker: " + marker)
    for phrase in PUBLIC_VOICE_BANS:
        if phrase in report:
            raise CanonicalSourceError("report source violates first-person public voice: " + phrase)
    folded = report.casefold()
    for phrase in FORBIDDEN_PUBLIC_CLAIMS:
        if phrase.casefold() in folded:
            raise CanonicalSourceError("forbidden R0.73Y public claim: " + phrase)

    sections, references_html = _sections(public_report)
    if "**" in references_html or "*Proc." in references_html or "*Phys." in references_html:
        raise CanonicalSourceError("reference Markdown emphasis leaked into reader HTML")
    section_one = _prose_paragraphs(_section_body(public_report, 1))
    literature = _prose_paragraphs(_section_body(public_report, 5))
    value = _prose_paragraphs(_section_body(public_report, 6))
    next_source = _section_body(public_report, 7)
    next_paragraphs = _prose_paragraphs(next_source)
    next_items = _ordered_items(next_source)
    if len(section_one) < 3 or len(literature) < 2 or len(value) < 2 or not next_paragraphs:
        raise CanonicalSourceError("R0.73Y public-copy paragraph inventory drift")
    if len(next_items) != 5:
        raise CanonicalSourceError(f"R0.73Y next-step list must contain five items, found {len(next_items)}")
    for number in (1, 2, 3):
        section = _section_body(public_report, number)
        if "A\\ne0" not in section:
            raise CanonicalSourceError(f"reader section {number} lacks the nonzero-amplitude qualifier")
    if "\\begin{aligned}" not in _section_body(public_report, 3):
        raise CanonicalSourceError("single-mode covariance display is not A4-safe")
    if "exact shear 类，使 这是一条" in public_report or "exact shear 类，使 本节" in public_report:
        raise CanonicalSourceError("formula-stripped reader fragment survived")

    lead_zh = _dictionary_value(correction, "Lead (zh)")
    home_zh = _dictionary_value(correction, "Home summary (zh)")
    for label, value_text in (("lead", lead_zh), ("home", home_zh)):
        if "A\\ne0" not in value_text:
            raise CanonicalSourceError(label + " summary lost the corrected quantifier")
        if label == "lead" and "D_{ii,s}" not in value_text:
            raise CanonicalSourceError("lead summary lost the covariance endpoint")

    certificate_ready, certificate_failure = _certificate_final(source_root)
    figure_ready, figure_failure = _figure_final(source_root)
    failures = [failure for ready, failure in ((certificate_ready, certificate_failure), (figure_ready, figure_failure)) if not ready]
    source_sha256 = {
        relative: hashlib.sha256((source_root / relative).read_bytes()).hexdigest()
        for relative in (*texts, *audit_texts)
    }
    return ReleaseContent(
        report_title=report_title,
        public_title_zh=PUBLIC_TITLE_ZH,
        release_title_en=RELEASE_TITLE_EN,
        subtitle_zh=PUBLIC_SUBTITLE_ZH,
        date=date,
        status=status,
        lead_zh=lead_zh,
        home_zh=home_zh,
        literature_zh=literature[-1],
        next_release=NEXT_RELEASE,
        next_gate_zh=next_paragraphs[0] + " " + "；".join(item.rstrip("；;。 ") for item in next_items) + "。",
        sections=sections,
        references_html=references_html,
        source_sha256=source_sha256,
        publication_ready=not failures,
        readiness_failures=tuple(dict.fromkeys(failures)),
    )


def source_status(root: Path | None = None) -> dict[str, object]:
    source_root = (root or Path(os.environ.get("R073Y_RELEASE_ROOT", Path(__file__).resolve().parents[1]))).resolve()
    missing = [relative for relative in CANONICAL_SOURCE_PATHS + PLANNED_AUDIT_PATHS if not (source_root / relative).is_file() or (source_root / relative).is_symlink()]
    return {
        "release": RELEASE,
        "siteVersion": SITE_VERSION,
        "baselineAccounting": R073X_BASELINE,
        "targetAccounting": R073Y_TARGET,
        "latestRecapRelease": LATEST_RECAP_RELEASE,
        "recapPolicy": "MILESTONE_ONLY_NO_R073Y_RECAP",
        "canonicalSources": list(CANONICAL_SOURCE_PATHS),
        "plannedAuditPaths": list(PLANNED_AUDIT_PATHS),
        "missing": missing,
        "writes": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Read and validate canonical R0.73Y reader content without writing.")
    parser.add_argument("--source-status", action="store_true")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if args.source_status:
        print(json.dumps(source_status(), ensure_ascii=False, sort_keys=True))
        return
    if not args.check_only:
        parser.print_help()
        return
    content = load_release_content()
    print(json.dumps({
        "release": RELEASE,
        "siteVersion": SITE_VERSION,
        "title": content.release_title_en,
        "publicTitleZh": content.public_title_zh,
        "sections": len(content.sections),
        "baselineAccounting": R073X_BASELINE,
        "targetAccounting": R073Y_TARGET,
        "latestRecapRelease": LATEST_RECAP_RELEASE,
        "recapGenerated": False,
        "publicationReady": content.publication_ready,
        "readinessFailures": list(content.readiness_failures),
        "writes": 0,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
